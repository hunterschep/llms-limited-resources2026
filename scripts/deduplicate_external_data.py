#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower())


def dedup_file(path: Path) -> tuple[int, int]:
    if not path.exists() or path.suffix != ".jsonl":
        return 0, 0
    rows = []
    seen = set()
    raw = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw += 1
        row = json.loads(line)
        key = (row.get("task"), norm(row.get("input", "")), norm(row.get("target", "")))
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return raw, len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="data/processed/external")
    args = parser.parse_args()
    report = []
    for path in sorted((ROOT / args.root).glob("**/*.jsonl")):
        raw, kept = dedup_file(path)
        report.append({"path": path.relative_to(ROOT).as_posix(), "raw": raw, "kept": kept, "removed": raw - kept})
    out = ROOT / "data/manifests/external_data_dedup_report.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in report), encoding="utf-8")
    print(f"Wrote dedup report to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
