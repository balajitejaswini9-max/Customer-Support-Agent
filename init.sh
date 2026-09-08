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
test -f knowledge_base/faq.md
test -f knowledge_base/return_policy.txt
test -f knowledge_base/shipping_info.txt
"$PYTHON_BIN" -m compileall -q src tests || true
echo "Initialisation complete. Active phase: 1"
