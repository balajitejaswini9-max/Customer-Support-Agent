#!/usr/bin/env python3
"""Repository health check: verifies required files and directory structure."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "feature_list.json",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "init.sh",
    "session-handoff.md",
    "docs/PRODUCT.md",
    "docs/ARCHITECTURE.md",
    "docs/RELIABILITY.md",
    "knowledge_base/faq.md",
    "knowledge_base/return_policy.txt",
    "knowledge_base/shipping_info.txt",
    "frontend/index.html",
    "frontend/app.js",
    "frontend/style.css",
    "src/ingestion.py",
    "src/vector_store.py",
    "src/retrieval.py",
    "src/embeddings.py",
    "src/escalation.py",
    "src/logging_config.py",
    "src/metrics.py",
    "src/eligibility.py",
    "src/store/__init__.py",
    "src/store/models.py",
    "src/store/mock_store.py",
    "src/store/order_extractor.py",
    "src/agent/__init__.py",
    "src/api/__init__.py",
    "src/generation/__init__.py",
    "src/handoff/__init__.py",
    "src/handoff/models.py",
    "src/handoff/repository.py",
    "src/handoff/notification.py",
    "src/handoff/summary.py",
    "src/conversation/__init__.py",
    "src/conversation/models.py",
    "src/conversation/repository.py",
]

REQUIRED_PHASE_DOCS = [f"docs/phases/PHASE-0{i}/PHASE-0{i}.md" for i in range(1, 9)]
REQUIRED_PHASE_FEATURES = [f"docs/phases/PHASE-0{i}/PHASE-0{i}-FEATURES.json" for i in range(1, 9)]


def check() -> int:
    failures: list[str] = []
    all_required = REQUIRED_FILES + REQUIRED_PHASE_DOCS + REQUIRED_PHASE_FEATURES
    for rel in all_required:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"MISSING: {rel}")
        else:
            print(f"  ok: {rel}")

    if failures:
        print("\nHealth check FAILED:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("\nHealth check PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(check())
