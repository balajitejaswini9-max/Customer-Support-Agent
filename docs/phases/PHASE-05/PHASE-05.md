# Phase 5: Escalation and Human Handoff

## Purpose

Mature escalation into a complete, auditable human-handoff workflow. When the agent cannot safely resolve a request, it creates a structured escalation ticket and grounded handoff summary.

## Scope

### In scope
- Escalation decision integration
- Grounded LLM handoff summary
- EscalationTicket model
- EscalationRepository with SQLite
- NotificationService abstraction with mock implementation
- Customer-facing escalation response
- Evidence/reason preservation
- Duplicate-escalation protection
- Phase 1-4 regression

### Out of scope
- Conversation persistence
- Real email integration
- E-commerce write operations
- Refund/cancellation/return execution
- Frontend changes
- Observability API
- Benchmarking

## Phase Boundary

Only functionality explicitly required by this phase may be implemented. Future-phase capabilities may be documented for context but must not be implemented early.

## Definition of Done

- All feature acceptance criteria are satisfied.
- All phase evaluations pass.
- Regression coverage passes.
- `bash init.sh` succeeds.
- No out-of-scope functionality is introduced.
- Repository state is explicit enough for the next coding-agent session to continue.
