# Phase 6: Conversation Persistence

## Purpose

Persist conversation state so the agent can resume context across requests and restarts while keeping authoritative order and policy sources separate.

## Scope

### In scope
- Conversation/message models
- ConversationRepository interface
- SQLite persistence
- Persist user and assistant messages
- Retrieve by conversation_id
- Context reconstruction
- Stable IDs
- Conversation isolation
- Persistence failure handling
- Phase 1-5 regression

### Out of scope
- Advanced memory
- Customer profiling
- Semantic conversation memory
- Cross-customer identity resolution
- Changing StoreClient or policy authority
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
