#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import refuse_bad_reference  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/eval/lineage_sorbian_probe.yaml")
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter")
    parser.add_argument("--adapter-scale", type=float, default=1.0)
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-output")
    args = parser.parse_args()
    refuse_bad_reference(" ".join(str(v) for v in vars(args).values() if v))
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
    subprocess.run(command, cwd=ROOT, check=True)
    result = json.loads((ROOT / args.output).read_text(encoding="utf-8"))
    print(json.dumps(result.get("aggregate", {}), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
