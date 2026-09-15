#!/usr/bin/env python3
"""Ledger consistency check: verifies feature_list.json and phase FEATURES.json files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FEATURE_LIST = ROOT / "feature_list.json"
VALID_STATUSES = {"todo", "active", "done"}


def check() -> int:
    failures: list[str] = []

    # Load feature_list.json
    ledger = json.loads(FEATURE_LIST.read_text())
    all_ids: list[str] = []
    for feature in ledger.get("features", []):
        fid = feature.get("id", "")
        if fid in all_ids:
            failures.append(f"Duplicate feature ID in feature_list.json: {fid}")
        all_ids.append(fid)
        status = feature.get("status", "")
        if status not in VALID_STATUSES:
            failures.append(f"Invalid status '{status}' for {fid}")
        for ev in feature.get("evidence", []):
            path = ROOT / ev
            if not path.exists():
                failures.append(f"Evidence file missing for {fid}: {ev}")

    # Check phase FEATURES.json files
    for phase_num in range(1, 9):
        phase_dir = ROOT / f"docs/phases/PHASE-0{phase_num}"
        features_file = phase_dir / f"PHASE-0{phase_num}-FEATURES.json"
        if not features_file.exists():
            failures.append(f"Missing: {features_file.relative_to(ROOT)}")
            continue

        phase_data = json.loads(features_file.read_text())
        phase_ids: list[str] = []
        all_done = True
        for feat in phase_data.get("features", []):
            fid = feat.get("id", "")
            if fid in phase_ids:
                failures.append(f"Duplicate ID in PHASE-0{phase_num}-FEATURES.json: {fid}")
            phase_ids.append(fid)
            status = feat.get("status", "")
            if status not in VALID_STATUSES:
                failures.append(f"Invalid status '{status}' for {fid} in PHASE-0{phase_num}")
            if status != "done":
                all_done = False

        phase_status = phase_data.get("status", "")
        if all_done and phase_status != "done":
            failures.append(
                f"PHASE-0{phase_num}: all features done but phase status is '{phase_status}'"
            )

    if failures:
        print("Ledger check FAILED:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("Ledger check PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(check())
