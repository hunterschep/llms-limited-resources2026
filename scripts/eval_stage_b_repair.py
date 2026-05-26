#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-output", default=None)
    args = parser.parse_args()
    config = "configs/eval/stage_b_rescue_probe_sorbian.yaml" if args.probe else "configs/eval/sorbian.yaml"
    command = [
        sys.executable,
        "scripts/competitive_eval.py",
        "--config",
        config,
        "--model",
        args.model,
        "--output",
        args.output,
    ]
    if args.raw_output:
        command.extend(["--raw-output", args.raw_output])
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
