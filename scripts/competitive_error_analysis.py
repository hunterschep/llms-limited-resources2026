#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in (ROOT / args.raw).read_text(encoding="utf-8").splitlines() if line.strip()]
    counts: dict[str, int] = {}
    for row in rows:
        task = str(row.get("task") or "UNKNOWN")
        pred = str(row.get("prediction") or "").strip()
        if not pred:
            key = f"{task}:empty"
        elif task in {"SC", "GC"} and "Wrong word:" not in pred and pred.upper() != "CORRECT":
            key = f"{task}:malformed"
        elif task == "MR" and not any(ch.isdigit() for ch in pred):
            key = "MR:nonnumeric"
        else:
            key = f"{task}:nonempty"
        counts[key] = counts.get(key, 0) + 1
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(counts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
