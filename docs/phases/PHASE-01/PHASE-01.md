# Phase 1 — Knowledge-Grounded Customer Support Agent

## Objective
Build the first usable backend agent. It answers customer support questions using a local knowledge base and Claude, with safeguards that prevent unsupported answers.

**Flagship behaviour:** the agent knows when not to answer.

## In Scope
- knowledge-base ingestion
- document chunking
- local embeddings
- ChromaDB
- similarity retrieval
- grounded Claude generation
- source citations
- layered escalation
- FastAPI `/chat`
- structured logging foundation
- 10-case behavioural evaluation

## Out of Scope
- frontend UI
- order lookup
- `products.json` lookup
- return-eligibility reasoning
- escalation ticket creation
- handoff email
- conversation persistence
- observability API
- benchmarking/cleanup tooling

## Phase Architecture
```text
Customer Message -> FastAPI /chat -> Agent Core
                                   +-> detect_intent
                                   +-> search_knowledge_base -> ChromaDB
                                   +-> grounded generation
                                   +-> layered escalation
                                   +-> response
```
The agent core must be independently callable without FastAPI.

## Knowledge Base
Initial files: `knowledge_base/faq.md`, `knowledge_base/return_policy.txt`, `knowledge_base/shipping_info.txt`. `products.json` is deferred.

## Ingestion
`Documents -> Loader -> Chunker -> all-MiniLM-L6-v2 -> ChromaDB`. Embeddings are local and 384-dimensional. Chunks retain source filename, chunk identifier, text, and citation metadata.

## Retrieval
1. Embed query.
2. Search ChromaDB.
3. Retrieve top-k chunks.
4. Preserve similarity information.
5. Preserve source metadata.
6. Pass evidence to generation.

## Grounded Generation
Claude receives the customer question and retrieved evidence with instructions to answer only from evidence. The response includes source references.

## Layered Escalation
Do not use a single LLM-generated confidence number.

### Layer 1 — Retrieval Quality
Insufficient evidence -> escalate.

### Layer 2 — Grounding Integrity
Draft cannot be supported by retrieved evidence -> escalate.

### Layer 3 — Human Authority / Scope
Complaints, disputes, unsupported requests, or requests requiring an irreversible human action -> escalate.

Record the escalation reason.

## API Contract
Request:
```json
{"message":"What is your return policy?","conversation_id":"optional"}
```
Response:
```json
{"answer":"Our return policy is ...","sources":[{"source":"return_policy.txt","section":"..."}],"escalated":false,"escalation_reason":null}
```

Escalated:
```json
{"answer":"I don't have enough information to answer that safely, so I've escalated it to a human support representative.","sources":[],"escalated":true,"escalation_reason":"insufficient_retrieval_evidence"}
```

## Behavioural Evaluation
10 cases:
- 4 grounded answers -> answer, not escalated, correct source
- 3 unsupported questions -> escalated, no fabrication
- 2 out-of-scope cases -> escalated by rule
- 1 grounding-integrity case -> escalated because the docs do not specify the requested detail

Use explicit assertions, not an LLM judge.

## Verification
```bash
bash init.sh
python -m pytest
python tests/eval_phase1.py
```

## Structured Logging
At minimum log request ID, conversation ID when supplied, intent, retrieval count, escalation status, escalation reason, latency, and errors. Do not log secrets.

## Definition of Done
All Phase 1 features are implemented; API works; grounded questions return supported answers; unsupported questions escalate; source metadata is returned; 10 behavioural evaluations pass; unit tests pass; `init.sh` passes; feature evidence is recorded; no future-phase functionality is added.

## Feature Mapping
| Feature | ID |
|---|---|
| KB ingestion | P1-F001 |
| Embeddings + vector store | P1-F002 |
| Similarity retrieval | P1-F003 |
| Grounded generation | P1-F004 |
| Layered escalation | P1-F005 |
| `/chat` API | P1-F006 |
| Structured logging | P1-F007 |
| Behavioural evaluation | P1-F008 |
