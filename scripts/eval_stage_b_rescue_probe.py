#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/eval/stage_b_rescue_probe_sorbian.yaml")
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--adapter-scale", type=float, default=1.0)
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-output", default=None)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    command = [
        sys.executable,
        "scripts/competitive_eval.py",
        "--config",
        args.config,
        "--model",
        args.model,
        "--output",
        args.output,
    ]
    if args.adapter:
        command.extend(["--adapter", args.adapter, "--adapter-scale", str(args.adapter_scale)])
    if args.raw_output:
        command.extend(["--raw-output", args.raw_output])
    if args.limit:
        command.extend(["--limit", str(args.limit)])
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
