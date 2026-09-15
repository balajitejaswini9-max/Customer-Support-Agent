# Phase 7: Observability and Metrics

## Purpose

Make agent behaviour measurable and diagnosable with structured telemetry for requests, retrieval, tools, decisions, escalation, errors and latency.

## Scope

### In scope
- Structured request logging
- Request/correlation IDs
- Latency measurement
- Retrieval telemetry
- Tool telemetry
- Escalation metrics
- Error metrics
- Decision outcome metrics
- Health/readiness endpoint
- Minimal metrics API
- Sensitive-data minimisation
- Phase 1-6 regression

### Out of scope
- Production monitoring vendor integration
- Full distributed tracing
- BI dashboards
- Automatic remediation
- Model retraining
- Phase 8 benchmarking

## Phase Boundary

Only functionality explicitly required by this phase may be implemented. Future-phase capabilities may be documented for context but must not be implemented early.

## Definition of Done

- All feature acceptance criteria are satisfied.
- All phase evaluations pass.
- Regression coverage passes.
- `bash init.sh` succeeds.
- No out-of-scope functionality is introduced.
- Repository state is explicit enough for the next coding-agent session to continue.
