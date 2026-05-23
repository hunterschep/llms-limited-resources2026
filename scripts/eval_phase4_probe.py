#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a model on a Phase 4 probe config.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--oracle", action="store_true")
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    cmd = [sys.executable, "scripts/eval_model.py", "--config", args.config, "--output", args.output]
    if args.model:
        cmd += ["--model", args.model]
    if args.oracle:
        cmd.append("--oracle")
    if args.limit:
        cmd += ["--limit", str(args.limit)]
    return subprocess.run(cmd, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
