#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import refuse_bad_reference  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/train/lineage_recovery/sorbian_edit_calibration_tiny.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    refuse_bad_reference(args.config)
    if not (ROOT / "data/processed/lineage_recovery/sorbian/edit_calibration/clean_60_error_40.jsonl").exists():
        subprocess.run([sys.executable, "scripts/build_edit_calibration_set.py"], cwd=ROOT, check=True)
    command = [sys.executable, "scripts/train_lineage_recovery.py", "--config", args.config]
    if args.dry_run:
        command.append("--dry-run")
    if args.max_examples is not None:
        command.extend(["--max-examples", str(args.max_examples)])
    env = dict(os.environ)
    env.setdefault("WMT26_LINEAGE_RECOVERY", "1")
    return subprocess.call(command, cwd=ROOT, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
