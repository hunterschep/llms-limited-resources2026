#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result_json")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    result = json.loads((ROOT / args.result_json).read_text(encoding="utf-8"))
    lines = ["# MT Direction Breakdown", ""]
    for direction, scores in sorted((result.get("direction_scores") or {}).items()):
        lines.append(f"- `{direction}`: chrF++={scores.get('chrf++', 0):.3f}, BLEU={scores.get('bleu', 0):.3f}")
    text = "\n".join(lines) + "\n"
    if args.output:
        out = ROOT / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
