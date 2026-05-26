#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output-dir", default="results/stage_b_rescue/package")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    command = [
        sys.executable,
        "scripts/competitive_package_model.py",
        "--track",
        "sorbian",
        "--model-dir",
        args.model_dir,
        "--output-dir",
        args.output_dir,
    ]
    if args.dry_run:
        command.append("--dry-run")
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
