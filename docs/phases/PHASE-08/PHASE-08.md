# Phase 8: Benchmarking and Repository Health

## Purpose

Establish repeatable end-to-end verification for the complete system and the harness itself, including benchmarking, clean-state reset and repository consistency checks.

## Scope

### In scope
- End-to-end benchmark suite
- Functional regression
- Latency/outcome measurement
- Evaluation reporting
- Clean-state/reset
- Generated-state cleanup
- Repository health checks
- Documentation consistency
- Ledger completion checks
- Deterministic initialization
- Final smoke test

### Out of scope
- New customer-support capabilities
- New business rules
- Production deployment automation
- Advanced optimisation
- Agent self-modification
- Replacing human escalation

## Phase Boundary

Only functionality explicitly required by this phase may be implemented. Future-phase capabilities may be documented for context but must not be implemented early.

## Definition of Done

- All feature acceptance criteria are satisfied.
- All phase evaluations pass.
- Regression coverage passes.
- `bash init.sh` succeeds.
- No out-of-scope functionality is introduced.
- Repository state is explicit enough for the next coding-agent session to continue.
