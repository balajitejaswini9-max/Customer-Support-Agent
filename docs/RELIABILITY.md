# Reliability

## Purpose
Reliability principles apply across all phases.

## Core Principles
- **No fabrication:** never invent policies, prices, orders, shipping commitments, return conditions, or support actions.
- **Explicit evidence:** knowledge-grounded responses retain source metadata.
- **Deterministic safety guards:** critical escalation rules do not rely solely on free-form LLM confidence.
- **Bounded agent execution:** tool loops have explicit limits.
- **Controlled side effects:** ticket creation and email are isolated behind interfaces.
- **Failure isolation:** dependency failure must not become fabricated success.
- **Reproducible tests:** tests and evaluations run from a clean repository state.
- **Observability:** important decisions are traceable without logging secrets or unnecessary personal data.

## Reliability Checks
Every phase defines unit verification, integration verification where needed, behavioural verification, startup verification, and evidence capture.

## Escalation as Reliability
Escalation is a successful outcome when evidence or authority is insufficient. Escalation rate alone is not the reliability metric; correctness of escalation is.

## Definition of Reliable Behaviour
A reliable support agent answers when evidence is sufficient, cites evidence, refuses to invent, escalates when required, fails safely when dependencies fail, and remains testable as capabilities expand.
