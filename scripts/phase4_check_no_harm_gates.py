#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase4_common import load_eval_result, markdown_table, task_score_vector, write_json


def check_candidate(baseline: dict, candidate: dict, max_drop: float, min_gain: float) -> dict:
    base = task_score_vector(baseline)
    cand = task_score_vector(candidate)
    drops = {task: base[task] - cand[task] for task in ["MT", "QA", "SC", "GC", "MR"]}
    improvements = {task: cand[task] - base[task] for task in ["MT", "QA", "SC", "GC", "MR"]}
    passed = cand["overall"] > base["overall"] and max(drops.values()) <= max_drop and max(improvements.values()) >= min_gain
    return {
        "candidate": candidate.get("model") or candidate.get("variant_id") or "candidate",
        "baseline_overall": base["overall"],
        "candidate_overall": cand["overall"],
        "overall_delta": cand["overall"] - base["overall"],
        "task_drops": drops,
        "task_improvements": improvements,
        "passed": passed,
        "reasons": [] if passed else [
            *(["overall_not_above_prompt_only"] if cand["overall"] <= base["overall"] else []),
            *(["task_drop_exceeds_threshold"] if max(drops.values()) > max_drop else []),
            *(["no_task_gain_meets_minimum"] if max(improvements.values()) < min_gain else []),
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidates", nargs="+", required=True)
    parser.add_argument("--max-task-drop", type=float, default=2.0)
    parser.add_argument("--min-task-gain", type=float, default=1.0)
    parser.add_argument("--output", default="results/phase4/gates/no_harm_report.json")
    args = parser.parse_args()
    baseline = load_eval_result(ROOT / args.baseline)
    rows = [check_candidate(baseline, load_eval_result(ROOT / rel), args.max_task_drop, args.min_task_gain) for rel in args.candidates]
    output = ROOT / args.output
    write_json(output, {"baseline": args.baseline, "checks": rows})
    md = output.with_suffix(".md")
    table_rows = [
        [row["candidate"], f"{row['candidate_overall']:.3f}", f"{row['overall_delta']:+.3f}", row["passed"], ", ".join(row["reasons"])]
        for row in rows
    ]
    md.write_text("# Phase 4 No-Harm Gate Report\n\n" + markdown_table(["candidate", "overall", "delta", "passed", "reasons"], table_rows) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "passed": [row["candidate"] for row in rows if row["passed"]]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
