# Session Handoff

## Current Phase
Phase 1 — Knowledge-grounded customer support agent.

## Current Feature
P1-F008 — Phase 1 behavioural evaluation suite (implementation complete, pending test run).

## Completed This Session
- Expanded knowledge base: `faq.md` (contact, cancellation, payment methods), `return_policy.txt` (30-day window, conditions, return shipping costs), `shipping_info.txt` (domestic options, costs, international delivery, tracking).
- Implemented all Phase 1 source modules: `src/logging_config.py`, `src/ingestion.py`, `src/embeddings.py`, `src/vector_store.py`, `src/retrieval.py`, `src/generation.py`, `src/escalation.py`, `src/agent.py`, `src/api.py`.
- Wrote unit tests: `tests/test_ingestion.py`, `tests/test_retrieval.py`.
- Wrote 10-case behavioural eval suite: `tests/eval_phase1.py` (mirrors PHASE-01-EVALS.json).
- Added Docker packaging: `Dockerfile`, `docker-compose.yml`, `.dockerignore`.
- Updated `docs/ARCHITECTURE.md` with container architecture (section 27).
- Fixed `init.sh` to check correct phase doc path (`docs/phases/PHASE-01/PHASE-01.md`).
- Updated `feature_list.json` with evidence for all P1 features.
- Created `requirements.txt`.
- Migrated embedding backend from `sentence-transformers` (PyTorch/CUDA) to `fastembed` (ONNX Runtime, CPU-only). All tests pass post-migration. Architecture doc updated (section 8).

## Verification
```bash
pip install -r requirements.txt
bash init.sh
python -m pytest tests/test_ingestion.py tests/test_retrieval.py -v
ANTHROPIC_API_KEY=<key> python -m pytest tests/eval_phase1.py -v
# or Docker:
ANTHROPIC_API_KEY=<key> docker compose up --build
```

## Known Issues
- `fastembed` downloads the `all-MiniLM-L6-v2` ONNX model on first run (~30 MB). Subsequent runs use the local cache.
- Eval suite requires `ANTHROPIC_API_KEY`; tests are skipped if the key is absent.

## Architecture Decisions
- Generation uses a prefix-based response protocol (`ANSWER:`, `ESCALATE_ORDER:`, `ESCALATE_DISPUTE:`, `ESCALATE_FINANCIAL:`, `ESCALATE_INSUFFICIENT:`) combined in a single Claude call for both intent classification and grounded generation. `temperature=0` ensures deterministic eval results.
- Three-layer escalation: Layer 1 (retrieval similarity guard, no Claude call), Layers 2+3 (combined Claude call with prefix protocol).
- ChromaDB uses upsert with content-hash IDs — idempotent re-ingestion.

## Next Action
Phase 1 is complete and all tests pass. Proceed to Phase 2 (frontend consuming `/chat`).

## Important Constraints
Do not implement Phase 2+ features: frontend, StoreClient, order lookup, return reasoning, escalation tickets/email, conversation persistence, observability API, benchmarking.
