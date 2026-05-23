#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", nargs="*", default=[])
    parser.add_argument("--output", default="results/phase4/status/loss_curve_report.json")
    args = parser.parse_args()
    report = {}
    pattern = re.compile(r"train_step=(\d+)/(\d+) avg_loss=([0-9.]+)")
    for rel in args.logs:
        path = ROOT / rel
        points = []
        if path.exists():
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                match = pattern.search(line)
                if match:
                    points.append({"step": int(match.group(1)), "max_steps": int(match.group(2)), "loss": float(match.group(3))})
        report[rel] = {"points": points, "status": "found" if points else "no_points"}
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output, "logs": len(args.logs)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
