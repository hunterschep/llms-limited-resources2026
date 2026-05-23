#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from phase4_common import read_jsonl, write_json
from wmt26.eval.metrics import normalize_mr_answer, parse_edit_output


def classify(row: dict) -> str:
    task = row.get("task")
    pred = str(row.get("raw_prediction", ""))
    gold = str(row.get("gold_target", ""))
    if task in {"SC", "GC"}:
        p_wrong, p_correct = parse_edit_output(pred)
        g_wrong, g_correct = parse_edit_output(gold)
        if p_wrong == g_wrong and p_correct == g_correct:
            return "exact"
        if p_wrong == "CORRECT" and g_wrong != "CORRECT":
            return "false_negative_correct"
        if p_wrong != "CORRECT" and g_wrong == "CORRECT":
            return "false_positive_error"
        if "\n" not in pred:
            return "malformed_single_line"
        if p_wrong == g_wrong:
            return "right_wrong_word_wrong_correction"
        return "wrong_word"
    if task == "MR":
        if normalize_mr_answer(pred) == normalize_mr_answer(gold):
            return "exact_normalized"
        if not normalize_mr_answer(pred):
            return "empty_or_unparseable"
        if len(pred.split()) > 8:
            return "verbose_or_explanation"
        return "wrong_numeric_or_value"
    if task == "QA":
        return "correct" if row.get("correct") else "wrong_or_invalid"
    return "not_classified"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="*", default=list(str(p.relative_to(ROOT)) for p in (ROOT / "results/phase3_fixed/raw_predictions").glob("*.jsonl")))
    parser.add_argument("--output", default="results/phase4/status/raw_error_taxonomy.json")
    args = parser.parse_args()
    report = {}
    for rel in args.inputs:
        rows = read_jsonl(ROOT / rel)
        report[rel] = dict(Counter(classify(row) for row in rows))
    write_json(ROOT / args.output, report)
    print(json.dumps({"output": args.output, "files": len(args.inputs)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
