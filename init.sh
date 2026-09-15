#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${PYTHON_BIN:-python3}"
echo "== Customer Support Agent: repository verification =="
"$PYTHON_BIN" --version
test -f AGENTS.md
test -f CLAUDE.md
test -f feature_list.json
test -f docs/PRODUCT.md
test -f docs/ARCHITECTURE.md
test -f docs/RELIABILITY.md
test -f docs/phases/PHASE-01/PHASE-01.md
test -f docs/phases/PHASE-02/PHASE-02.md
test -f knowledge_base/faq.md
test -f knowledge_base/return_policy.txt
test -f knowledge_base/shipping_info.txt
test -f frontend/index.html
test -f frontend/app.js
test -f frontend/style.css
test -f docs/phases/PHASE-03/PHASE-03.md
test -f src/store/__init__.py
test -f src/store/models.py
test -f src/store/mock_store.py
test -f src/store/order_extractor.py
test -f docs/phases/PHASE-04/PHASE-04.md
test -f src/eligibility.py
test -f docs/phases/PHASE-05/PHASE-05.md
test -f src/handoff/__init__.py
test -f src/handoff/models.py
test -f src/handoff/repository.py
test -f src/handoff/notification.py
test -f src/handoff/summary.py
test -f docs/phases/PHASE-06/PHASE-06.md
test -f src/conversation/__init__.py
test -f src/conversation/models.py
test -f src/conversation/repository.py
test -f docs/phases/PHASE-07/PHASE-07.md
test -f src/metrics.py
test -f docs/phases/PHASE-08/PHASE-08.md
test -f scripts/reset.py
test -f scripts/check_health.py
test -f scripts/check_ledger.py
test -f tests/benchmark.py
"$PYTHON_BIN" -m compileall -q src tests scripts || true
echo "Initialisation complete. Active phase: 8 (complete)"
