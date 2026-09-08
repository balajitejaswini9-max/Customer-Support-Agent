"""
Phase 1 Behavioural Evaluation Suite — 10 cases from PHASE-01-EVALS.json.

Run as pytest:  python -m pytest tests/eval_phase1.py -v
Run standalone: python tests/eval_phase1.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Allow running from project root without installing the package.
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import AgentRequest, AgentResponse, CustomerSupportAgent
from src.ingestion import load_knowledge_base
from src.vector_store import VectorStore

_NEEDS_API_KEY = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)

pytestmark = _NEEDS_API_KEY

KB_DIR = Path(__file__).parent.parent / "knowledge_base"


@pytest.fixture(scope="module")
def agent() -> CustomerSupportAgent:
    import anthropic

    chunks = load_knowledge_base(KB_DIR)
    store = VectorStore()  # in-memory — fresh state every run
    store.add_documents(chunks)
    return CustomerSupportAgent(store, anthropic.Anthropic())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assert_grounded(resp: AgentResponse, required_source: str | None = None) -> None:
    assert not resp.escalated, (
        f"Expected grounded answer but got escalation: {resp.escalation_reason!r}"
    )
    assert resp.answer.strip(), "Answer must not be empty"
    assert resp.sources, "Grounded response must include at least one source"
    if required_source:
        sources = [s.source for s in resp.sources]
        assert any(required_source in s for s in sources), (
            f"Expected a source containing {required_source!r}, got {sources}"
        )


def _assert_escalated(resp: AgentResponse) -> None:
    assert resp.escalated, (
        f"Expected escalation but got answer: {resp.answer!r}"
    )
    assert resp.escalation_reason, "Escalated response must include a reason"
    assert not resp.sources, "Escalated response must have empty sources"


# ---------------------------------------------------------------------------
# P1-E001 — Grounded: standard delivery time
# ---------------------------------------------------------------------------

def test_e001_standard_delivery(agent: CustomerSupportAgent):
    resp = agent.chat(AgentRequest("How long does standard delivery usually take?"))
    _assert_grounded(resp, required_source="shipping_info")


# ---------------------------------------------------------------------------
# P1-E002 — Grounded: cancellation policy
# ---------------------------------------------------------------------------

def test_e002_order_cancellation(agent: CustomerSupportAgent):
    resp = agent.chat(AgentRequest("Can I cancel my order before it ships?"))
    _assert_grounded(resp)


# ---------------------------------------------------------------------------
# P1-E003 — Escalate: real-time order status (out of phase scope)
# ---------------------------------------------------------------------------

def test_e003_order_status(agent: CustomerSupportAgent):
    resp = agent.chat(AgentRequest("My order is late. Where is it right now?"))
    _assert_escalated(resp)


# ---------------------------------------------------------------------------
# P1-E004 — Escalate: damaged product complaint
# ---------------------------------------------------------------------------

def test_e004_damaged_product(agent: CustomerSupportAgent):
    resp = agent.chat(
        AgentRequest("I want a refund because the product arrived damaged.")
    )
    _assert_escalated(resp)


# ---------------------------------------------------------------------------
# P1-E005 — Escalate: customer asserting unverified policy claim
# ---------------------------------------------------------------------------

def test_e005_unverified_claim(agent: CustomerSupportAgent):
    resp = agent.chat(
        AgentRequest(
            "Your website says I can return this after 90 days. Is that true?"
        )
    )
    _assert_escalated(resp)


# ---------------------------------------------------------------------------
# P1-E006 — Escalate: order-specific return (requires order lookup)
# ---------------------------------------------------------------------------

def test_e006_order_specific_return(agent: CustomerSupportAgent):
    resp = agent.chat(
        AgentRequest("Can I return this item? My order number is 12345.")
    )
    _assert_escalated(resp)


# ---------------------------------------------------------------------------
# P1-E007 — Grounded: payment methods
# ---------------------------------------------------------------------------

def test_e007_payment_methods(agent: CustomerSupportAgent):
    resp = agent.chat(AgentRequest("What payment methods do you accept?"))
    _assert_grounded(resp, required_source="faq")


# ---------------------------------------------------------------------------
# P1-E008 — Escalate: duplicate charge refund (financial action)
# ---------------------------------------------------------------------------

def test_e008_duplicate_charge(agent: CustomerSupportAgent):
    resp = agent.chat(
        AgentRequest(
            "I was charged twice for the same order. Can you refund one of the charges?"
        )
    )
    _assert_escalated(resp)


# ---------------------------------------------------------------------------
# P1-E009 — Grounded: international delivery
# ---------------------------------------------------------------------------

def test_e009_international_delivery(agent: CustomerSupportAgent):
    resp = agent.chat(AgentRequest("Do you deliver internationally?"))
    _assert_grounded(resp, required_source="shipping_info")


# ---------------------------------------------------------------------------
# P1-E010 — Escalate: grounding integrity / conflicting claims
# ---------------------------------------------------------------------------

def test_e010_conflicting_policy_claim(agent: CustomerSupportAgent):
    resp = agent.chat(
        AgentRequest(
            "The FAQ says returns are free, but another page says I have to pay "
            "postage. Which one applies?"
        )
    )
    _assert_escalated(resp)


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

def main() -> None:
    import anthropic

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY is not set.")
        sys.exit(1)

    chunks = load_knowledge_base(KB_DIR)
    store = VectorStore()
    store.add_documents(chunks)
    ag = CustomerSupportAgent(store, anthropic.Anthropic())

    cases = [
        ("E001", "How long does standard delivery usually take?", False),
        ("E002", "Can I cancel my order before it ships?", False),
        ("E003", "My order is late. Where is it right now?", True),
        ("E004", "I want a refund because the product arrived damaged.", True),
        ("E005", "Your website says I can return this after 90 days. Is that true?", True),
        ("E006", "Can I return this item? My order number is 12345.", True),
        ("E007", "What payment methods do you accept?", False),
        ("E008", "I was charged twice for the same order. Can you refund one of the charges?", True),
        ("E009", "Do you deliver internationally?", False),
        ("E010", "The FAQ says returns are free, but another page says I have to pay postage. Which one applies?", True),
    ]

    passed = 0
    failed = 0
    for case_id, question, expect_escalated in cases:
        resp = ag.chat(AgentRequest(question))
        ok = resp.escalated == expect_escalated
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"[{status}] {case_id}: {question[:60]}")
        if not ok:
            print(f"       expected escalated={expect_escalated}, got {resp.escalated}")
            print(f"       answer: {resp.answer[:120]}")

    print(f"\n{passed}/10 passed, {failed}/10 failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
