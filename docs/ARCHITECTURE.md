# Architecture

## 1. Purpose
This document describes the complete target architecture for the Customer Support Agent across all phases. It is the architectural source of truth. Phase-specific implementation scope belongs in `docs/phases/PHASE-XX.md`.

## 2. Complete Target Architecture

```text
                         Customer
                            |
                            v
                    +----------------+
                    | FastAPI /chat  |
                    +----------------+
                            |
                            v
                 +-----------------------+
                 | Customer Support      |
                 | Agent / ReAct Loop    |
                 +-----------------------+
                   |       |       |
          ----------       |       ----------
         v                 v                 v
+----------------+ +----------------+ +----------------------+
| Knowledge/RAG  | | StoreClient    | | Escalation           |
| ingestion      | | order lookup   | | retrieval guard      |
| chunking       | | order data     | | grounding guard      |
| embeddings     | |                | | human-authority rule |
| vector store   | +----------------+ +----------+-----------+
| retrieval      |                            |
+-------+--------+                            v
        |                           +-----------------------+
        v                           | Human Handoff         |
+----------------+                  | summary generation    |
| Claude         |                  | ticket persistence    |
| Generation     |                  | email notification    |
+----------------+                  +-----------+-----------+
                                             |
                                             v
                                  +-----------------------+
                                  | Persistence           |
                                  | SQLite / repositories |
                                  +-----------------------+

                     +-----------------------+
                     | Observability         |
                     | logs / metrics / API  |
                     +-----------------------+

                     +-----------------------+
                     | Frontend              |
                     | consumes /chat        |
                     +-----------------------+
```

## 3. Architectural Layers
- Interface: FastAPI and future frontend
- Agent: intent detection, ReAct/tool loop, tool selection, answer generation, escalation
- Knowledge: ingestion, chunking, embeddings, ChromaDB, retrieval, source metadata
- Integration: StoreClient, email client, future services
- Persistence: conversation and escalation repositories
- Reliability: tests, evaluations, logs, metrics, benchmarks

## 4. Agent Core
The agent core is independent of FastAPI.

```text
AgentRequest -> detect_intent -> plan/act
                         |-> search_knowledge_base
                         |-> lookup_order
                         |-> check_return_eligibility
                         |-> assess_escalation_need
                         -> grounded response OR escalation
```

Only capabilities available in the active phase may be exposed.

## 5. Agent Execution Model
The long-term agent uses a bounded ReAct-style loop: reason -> select tool -> execute -> inspect -> repeat if needed -> answer/escalate.

## 6. Agent Tools
Target tools: `detect_intent`, `search_knowledge_base`, `lookup_order`, `check_return_eligibility`, `assess_escalation_need`, `escalate_to_human`.

## 7. Intent Detection
Intent detection helps route requests but is not permission to invent unsupported information. Uncertain or unsupported intents can escalate.

## 8. Knowledge Base / RAG Architecture

```text
Source Documents -> Loader -> Chunking -> Local Embedding Model -> ChromaDB
       -> Similarity Retrieval -> Retrieved Chunks + Metadata -> Claude
```

Initial embedding model: `all-MiniLM-L6-v2`, 384 dimensions, run locally via `fastembed` (ONNX Runtime, CPU-only — no GPU or PyTorch required). ChromaDB is persisted locally. Chunks retain source metadata for citation.

## 9. Grounding Architecture
Grounding is enforced through: retrieval-quality guard, grounding-integrity guard, and human-authority/scope guard.

## 10. Store Integration
External store access is hidden behind:
```text
StoreClient
  +-- MockStoreClient
  +-- Future production implementation
```

## 11. Order Lookup
Phase 3: Customer -> Agent -> lookup_order -> StoreClient -> Order.

## 12. Return Eligibility
Phase 4 combines order data with authoritative return policy and returns eligible/not eligible/insufficient evidence.

## 13. Escalation Architecture
Escalation is not based solely on an LLM self-reported confidence score.

```text
Agent decision
   +--> Retrieval guard
   +--> Grounding guard
   +--> Human rule
             |
             v
        Escalate? -> yes: human path / no: answer
```

## 14. Escalation Decision
Target response:
```json
{"answer":"...","sources":[],"escalated":true,"escalation_reason":"..."}
```

## 15. Full Human Handoff
Phase 5 adds handoff summary generation, escalation ticket creation, and support-team notification. Side effects are isolated behind interfaces.

## 16. Persistence Architecture
SQLite is the initial persistence target. Repositories isolate persistence from the agent: `ConversationRepository` and `EscalationRepository`.

## 17. Conversation History
Phase 6 introduces `conversation_id -> ConversationRepository -> SQLite`.

## 18. API Contract
Request:
```json
{"message":"Where is my order?","conversation_id":"optional-id"}
```
Response:
```json
{"answer":"...","sources":[{"source":"faq.md","section":"..."}],"escalated":false,"escalation_reason":null}
```
The API remains thin.

## 19. Frontend Architecture
Phase 2: Browser -> Frontend -> HTTP -> FastAPI /chat -> Agent Core. The frontend contains no agent business logic.

## 20. Observability Architecture
Phase 7 adds structured logs, request IDs, conversation IDs, latency, retrieval metrics, escalation metrics, tool-call metrics, and error counts.

## 21. Logging Flow
Example:
```json
{"event":"agent_response","request_id":"...","conversation_id":"...","escalated":false,"retrieval_count":4,"latency_ms":842}
```
Do not log secrets or unnecessary personal data.

## 22. Reliability Tooling
Unit tests + behavioural evaluations + startup verification + structured logs + benchmarking.

## 23. Phase Evolution
- Phase 0: repository harness and engineering documentation
- Phase 1: KB ingestion, embeddings, ChromaDB, retrieval, Claude generation, citations, layered escalation, `/chat`, logging foundation, behavioural evaluations
- Phase 2: frontend consuming `/chat`
- Phase 3: StoreClient, mock store, order lookup
- Phase 4: return eligibility reasoning
- Phase 5: handoff summary, escalation ticket, email notification
- Phase 6: conversation persistence/history
- Phase 7: observability API and metrics
- Phase 8: benchmarking, clean-state, reset, generated-state cleanup, repository health checks

## 24. Phase Dependency Graph
`Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6 -> Phase 7 -> Phase 8`

## 25. Architectural Invariants
1. Agent core is independent of HTTP.
2. External integrations use interfaces.
3. RAG exposes evidence and source metadata.
4. Unsupported information is never fabricated.
5. Human-authority cases can force escalation.
6. Side effects are controlled and isolated.
7. Behaviour is independently testable.
8. Complexity is introduced progressively.
9. Observability does not become business logic.
10. Future-phase functionality is not implemented early.

## 26. Architecture-to-Phase Mapping
| Component | Phase |
|---|---:|
| Repository harness | 0 |
| Product/architecture/reliability docs | 0 |
| KB ingestion | 1 |
| Embeddings | 1 |
| ChromaDB | 1 |
| Retrieval | 1 |
| Claude generation | 1 |
| Grounding | 1 |
| Escalation foundation | 1 |
| FastAPI `/chat` | 1 |
| Behavioural evaluation | 1 |
| Frontend | 2 |
| StoreClient | 3 |
| Order lookup | 3 |
| Return eligibility | 4 |
| Escalation ticket | 5 |
| Handoff summary | 5 |
| Email notification | 5 |
| Conversation persistence | 6 |
| Observability API | 7 |
| Benchmarking/cleanup | 8 |

## 27. Container Architecture

The agent is packaged as a single Docker image and run via Docker Compose.

```text
docker-compose.yml
  |
  +-- agent (Dockerfile)
       |
       +-- src/api.py  (FastAPI, port 8000)
       |
       +-- knowledge_base/  (read-only, baked into image)
       |
       +-- /data/chroma      (named volume, persists ChromaDB)
```

### Image

- Base: `python:3.11-slim`
- Dependencies installed from `requirements.txt`.
- Source (`src/`) and knowledge base (`knowledge_base/`) are copied at build time.
- The `sentence-transformers` model (`all-MiniLM-L6-v2`) is downloaded on first run and cached by the container runtime.

### Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | required | Anthropic API authentication |
| `CLAUDE_MODEL` | `claude-opus-4-8` | Generation model |
| `RETRIEVAL_THRESHOLD` | `0.25` | Minimum cosine similarity for retrieval guard |
| `KB_DIR` | `knowledge_base` | Path to knowledge base directory |
| `CHROMA_DIR` | `/data/chroma` | Path for ChromaDB persistence |

### Volumes

- `chroma_data` — named volume mounted at `/data/chroma`. Persists the ChromaDB vector store across container restarts. Delete this volume to force a full re-ingestion on next startup.

### Build and run

```bash
# Build and start
ANTHROPIC_API_KEY=sk-... docker compose up --build

# Run in background
ANTHROPIC_API_KEY=sk-... docker compose up -d --build

# Rebuild after knowledge-base changes
docker compose down && docker compose up --build
```

### Container invariants

- The container contains no API keys at build time; `ANTHROPIC_API_KEY` is injected at runtime via environment variable.
- The ChromaDB vector store is external to the image (named volume), so image rebuilds do not destroy indexed data.
- The knowledge base is baked into the image; updating KB content requires a rebuild.
