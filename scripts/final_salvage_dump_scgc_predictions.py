#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract SC/GC rows from a raw prediction JSONL.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()
    inp = Path(args.input)
    if not inp.is_absolute():
        inp = ROOT / inp
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with inp.open("r", encoding="utf-8") as handle, out.open("w", encoding="utf-8") as dest:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("task") not in {"SC", "GC"}:
                continue
            dest.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
            if args.limit and count >= args.limit:
                break
    print(json.dumps({"input": str(inp), "output": str(out), "rows": count}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
