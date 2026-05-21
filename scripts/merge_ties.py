#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from merge_task_vectors import write_dry_run


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--density", type=float, default=0.5)
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    if not args.dry_run:
        raise NotImplementedError("TIES real merge is intentionally gated; use dry-run until trained local checkpoints exist.")
    out = write_dry_run(config, "ties", {"density": args.density})
    print(f"TIES merge dry-run output: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
