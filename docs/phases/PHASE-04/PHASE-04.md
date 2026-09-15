# Phase 4 — Return Eligibility

## Purpose

Introduce **return-eligibility reasoning** by combining approved return-policy evidence from the Knowledge Base with authoritative order facts from the Phase 3 `StoreClient`.

This phase introduces **decisioning, not action**.

> The agent may determine whether an order appears eligible for return. It must not claim that a return, refund, or cancellation has been completed.

## Goal

Support questions such as:

* "Can I return order ORD-1001?"
* "Is ORD-1002 eligible for a return?"
* "Why isn't my order eligible?"

The decision must be based on explicit policy evidence and retrieved order facts.

## In scope

* Return-policy retrieval
* Phase 3 order lookup
* Bounded `check_return_eligibility` capability
* Explicit, inspectable eligibility rules
* Eligibility decision and explanation
* Policy/order evidence provenance
* Missing or conflicting evidence handling
* Phase 1/3 regression coverage
* Phase 4 tests and behavioural evaluations

## Out of scope

* Return creation
* Refund processing
* Cancellation
* Return shipping execution
* Real e-commerce integration
* Human handoff workflow changes
* Conversation persistence
* Frontend changes
* Autonomous policy invention
* Probabilistic eligibility decisions without sufficient evidence

## Architecture

```text
Customer
   │
   ▼
FastAPI /chat
   │
   ▼
Customer Support Agent
   ├── Knowledge Retrieval ──► Return Policy
   ├── lookup_order ─────────► StoreClient
   │                              │
   │                              ▼
   │                        MockStoreClient
   ├── check_return_eligibility
   │          │
   │          ├── policy evidence
   │          └── order facts
   │
   └── Escalation
```

## Source-of-truth boundaries

```text
General return policy
        ↓
Knowledge Base

Order date / item / order state
        ↓
StoreClient

Eligibility decision
        ↓
Policy + order facts + explicit rules
```

Claude may help understand the request and explain the resulting decision, but it must not silently override explicit decision logic.

A useful boundary is:

```text
Claude
  ↓
Understand request / gather evidence
  ↓
Deterministic eligibility logic
  ↓
Decision
  ↓
Claude
  ↓
Explain decision
```

## Decision model

For the current seed policy, documented rules include:

* eligible items are generally returnable within 30 days;
* applicable conditions still apply;
* there is no general 90-day return period;
* return postage is normally the customer's responsibility unless the product or promotion says otherwise.

Do not silently introduce additional rules.

The implementation should only decide when the required facts are known, including:

* order date;
* relevant item;
* applicable documented policy conditions.

If a required fact is unavailable, do not infer it.

```text
Return request
     ↓
Identify order
     ↓
Retrieve order
     ↓
Retrieve policy
     ↓
Are required facts known?
   ┌─┴─┐
  Yes  No
   │    │
   ▼    ▼
Evaluate  Escalate
 rules
   │
┌──┴──────┐
▼         ▼
Eligible  Not eligible
   │         │
   └────┬────┘
        ▼
 Explain + evidence
```

## Structured result

Conceptually:

```json
{
  "eligible": true,
  "order_id": "ORD-1001",
  "reason": "Order is within the documented 30-day return period.",
  "policy_sources": [
    {
      "source": "return_policy.txt",
      "section": "Eligibility"
    }
  ]
}
```

The exact schema may evolve, but the result must preserve:

* decision;
* reason;
* order ID;
* supporting policy evidence;
* whether the decision was blocked by insufficient evidence.

## Customer response

A successful response should explain the outcome in plain language and cite the relevant policy evidence.

The agent must not claim:

* a return was created;
* a refund was issued;
* a refund is guaranteed;
* a cancellation was completed.

## Uncertainty and escalation

Escalate when:

* the order cannot be found;
* the order date is unavailable;
* the relevant item cannot be identified;
* required policy evidence cannot be retrieved;
* policy evidence conflicts materially;
* the customer requests an action rather than an eligibility decision;
* the request depends on an undocumented policy.

> **No decision is better than an unsupported decision.**

## API

The existing `/chat` contract remains unchanged:

```json
{
  "message": "Can I return order ORD-1001?",
  "conversation_id": "optional-id"
}
```

Example response:

```json
{
  "answer": "...",
  "sources": [
    {
      "source": "return_policy.txt",
      "section": "Eligibility"
    }
  ],
  "escalated": false,
  "escalation_reason": null
}
```

## Dependencies

```text
Phase 1
  │
  ├── Knowledge Base
  ├── grounded generation
  └── escalation
       │
       ▼
Phase 3
  │
  ├── StoreClient
  ├── order lookup
  └── order-grounded data
       │
       ▼
Phase 4
  ├── return policy retrieval
  ├── eligibility rules
  ├── decision explanation
  └── evidence
```

## Definition of Done

* [ ] Return-policy evidence can be retrieved.
* [ ] Order-specific facts come from StoreClient.
* [ ] `check_return_eligibility` exists as a bounded capability.
* [ ] Eligibility uses only explicit policy and known order facts.
* [ ] Deterministic decision logic is inspectable.
* [ ] Missing evidence causes safe handling or escalation.
* [ ] Conflicting policy evidence does not produce an arbitrary decision.
* [ ] Responses explain the decision and supporting policy.
* [ ] No return/refund/cancellation action is performed or claimed.
* [ ] Phase 1 and Phase 3 behaviour remains intact.
* [ ] Phase 4 feature ledger is complete.
* [ ] Phase 4 evaluations pass.
* [ ] Tests pass.
* [ ] `init.sh` initializes/verifies the environment.
* [ ] No Phase 5+ functionality is implemented.

## Engineering principle

> **Use AI to understand and explain; use explicit, authoritative evidence and deterministic rules to make auditable business decisions.**