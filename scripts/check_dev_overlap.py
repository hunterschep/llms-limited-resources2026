#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower())


def load_locked_texts() -> set[str]:
    texts = set()
    for path in sorted((ROOT / "data/processed").glob("*/*_locked_validation.jsonl")) + sorted((ROOT / "data/processed").glob("*/*_tune.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            for value in [row.get("input", ""), row.get("target", "")]:
                text = norm(value)
                if len(text) >= 20:
                    texts.add(text)
    return texts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="data/processed/external")
    parser.add_argument("--fail-on-overlap", action="store_true")
    args = parser.parse_args()
    locked = load_locked_texts()
    report = []
    overlap_count = 0
    for path in sorted((ROOT / args.root).glob("**/*.jsonl")):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        overlaps = []
        kept = []
        for row in rows:
            input_text = norm(row.get("input", ""))
            target_text = norm(row.get("target", ""))
            has_overlap = (len(input_text) >= 20 and input_text in locked) or (len(target_text) >= 20 and target_text in locked)
            if has_overlap:
                overlaps.append(row.get("id"))
                overlap_count += 1
            else:
                kept.append(row)
        # Filter exact dev/tune overlaps out of trainable external files.
        with path.open("w", encoding="utf-8") as handle:
            for row in kept:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        report.append({"path": path.relative_to(ROOT).as_posix(), "rows": len(rows), "overlaps_removed": len(overlaps), "overlap_check_status": "removed_exact_overlaps"})
    out = ROOT / "data/manifests/external_data_overlap_report.jsonl"
    out.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in report), encoding="utf-8")
    print(f"Wrote overlap report to {out}; removed {overlap_count} exact overlaps")
    if args.fail_on_overlap and overlap_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
