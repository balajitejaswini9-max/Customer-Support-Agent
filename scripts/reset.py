#!/usr/bin/env python3
"""Clean-state reset: removes generated runtime artefacts without touching source-controlled files."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def reset(chroma_dir: str, db_dir: str, dry_run: bool = False) -> None:
    targets = [
        Path(chroma_dir),
        Path(db_dir),
    ]
    for target in targets:
        if target.exists():
            if dry_run:
                print(f"[dry-run] would remove: {target}")
            else:
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
                print(f"removed: {target}")
        else:
            print(f"not found (skipped): {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset generated runtime state.")
    parser.add_argument("--chroma-dir", default=os.getenv("CHROMA_DIR", ".chroma"))
    parser.add_argument("--db-dir", default=os.getenv("DATA_DIR", "/data/db"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    reset(args.chroma_dir, args.db_dir, dry_run=args.dry_run)
    print("Reset complete.")


if __name__ == "__main__":
    main()
