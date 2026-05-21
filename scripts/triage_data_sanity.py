#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import scgc_diagnostics, scgc_scores


FINAL_FILES = {
    "uk": {
        "SC": "data/processed/final/uk/sc_train_final.jsonl",
        "GC": "data/processed/final/uk/gc_train_final.jsonl",
        "MR": "data/processed/final/uk/mr_train_final.jsonl",
    },
    "sorbian": {
        "SC": "data/processed/final/sorbian/sc_train_final.jsonl",
        "GC": "data/processed/final/sorbian/gc_train_final.jsonl",
        "MR": "data/processed/final/sorbian/mr_train_final.jsonl",
    },
}

EDIT_CORRECT_RE = re.compile(r"Wrong word:\s*CORRECT\s*\nCorrect word:\s*CORRECT\s*$", re.IGNORECASE)
NUMERIC_RE = re.compile(r"^\s*[-+]?\d+(?:\.\d+)?\s*$")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def edit_report(rows: list[dict]) -> dict:
    refs = [str(row.get("target", "")) for row in rows]
    always_error = ["Wrong word: X\nCorrect word: Y"] * len(refs)
    correct = sum(1 for target in refs if EDIT_CORRECT_RE.search(target))
    errors = len(refs) - correct
    clean_ratio = correct / max(1, len(refs))
    return {
        "rows": len(rows),
        "error_rows": errors,
        "clean_rows": correct,
        "clean_ratio": clean_ratio,
        "always_error_scores": scgc_scores(always_error, refs),
        "always_error_diagnostics": scgc_diagnostics(always_error, refs),
        "status": "pass" if 0.35 <= clean_ratio <= 0.65 else "warn",
    }


def mr_report(rows: list[dict]) -> dict:
    bad = [
        {
            "id": row.get("id"),
            "source_id": row.get("source_id"),
            "target": row.get("target"),
            "input": str(row.get("input", ""))[:200],
        }
        for row in rows
        if not NUMERIC_RE.match(str(row.get("target", "")))
    ]
    return {
        "rows": len(rows),
        "non_numeric_targets": len(bad),
        "bad_examples": bad[:20],
        "status": "pass" if not bad else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Report final-data sanity checks that explain suspicious Phase 3 metrics.")
    parser.add_argument("--output", default="results/triage/data_sanity_report.json")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    report: dict[str, dict] = {}
    has_issue = False
    for track, tasks in FINAL_FILES.items():
        report[track] = {}
        for task, rel in tasks.items():
            rows = read_jsonl(ROOT / rel)
            task_report = edit_report(rows) if task in {"SC", "GC"} else mr_report(rows)
            report[track][task] = task_report
            has_issue = has_issue or task_report["status"] in {"warn", "fail"}

    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "has_issue": has_issue, "report": report}, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if args.fail_on_issues and has_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())
