# AGENTS.md

## Purpose
This repository is a phase-driven Customer Support Agent project. This file is the operating manual for coding agents.

## Startup
1. Read `AGENTS.md`.
2. Read `CLAUDE.md`.
3. Read `docs/ARCHITECTURE.md`.
4. Read `docs/PRODUCT.md`.
5. Read `docs/RELIABILITY.md`.
6. Read the active phase document under `docs/phases/`.
7. Run `bash init.sh`.
8. Read `feature_list.json`.

## Current Phase
The repository starts in Phase 1. Only implement features explicitly assigned to the active phase. Future-phase architecture may be documented, but future functionality must not be implemented early.

## Source of Truth
- `PRODUCT.md`: stable product vision and principles.
- `ARCHITECTURE.md`: complete target architecture across all phases.
- `RELIABILITY.md`: cross-phase reliability principles.
- `docs/phases/PHASE-XX.md`: implementation scope and verification for a phase.
- `feature_list.json`: machine-readable implementation/evidence ledger.
- `session-handoff.md`: state carried between sessions.

If documents disagree, stop and resolve the contradiction.

## Architecture Boundaries
### Agent Core
Owns request interpretation, tool selection/execution, grounded reasoning, response generation, and escalation. It must not depend directly on FastAPI.

### RAG
Owns ingestion, chunking, embeddings, vector storage, and retrieval.

### Generation
Owns Claude integration. Provider-specific code stays behind an interface.

### API
Owns HTTP validation, serialization, errors, and dependency wiring. Business logic belongs in the agent.

### External Integrations
Hide external systems behind interfaces such as `StoreClient`, email client, and persistence repositories.

## Phase Discipline
- One phase at a time.
- Do not implement future-phase functionality.
- Do not add infrastructure merely because the final architecture contains it.
- Prefer small, testable components.

## Definition of Done
A feature is complete only when implementation exists, behaviour matches the phase specification, relevant tests/evaluations pass, no future scope was introduced, evidence is recorded in `feature_list.json`, relevant docs are updated, `init.sh` works, and no known broken state remains.

## Coding Conventions
- Python 3.11+.
- Type hints for public interfaces.
- Small functions with explicit inputs/outputs.
- Avoid hidden global state.
- Isolate provider integrations.
- Prefer dependency injection for external services.
- Use structured logs.
- Fail explicitly rather than fabricating data.
- Tests verify observable behaviour.

## Grounding Rule
Never invent policy, product, order, shipping, refund, or eligibility information. If the knowledge base does not support an answer, escalate according to the active phase rules.

## Verification
Prefer unit tests, assertion-based behavioural evaluations, reproducible local commands, and explicit evidence in the feature ledger.

## Session Handoff
Before ending a substantial implementation session, update `session-handoff.md` with completed work, verification, active feature, issues, and next action.

## Clean State
Do not commit secrets, API keys, credentials, virtual environments, large vector-store artefacts, temporary files, or debug dumps.
