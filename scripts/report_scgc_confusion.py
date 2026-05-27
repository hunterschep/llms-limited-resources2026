#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import parse_edit_output  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def classify(row: dict) -> str:
    pred = row.get("parsed_prediction") or {}
    gold = row.get("parsed_reference") or {}
    if not pred:
        wrong, correct = parse_edit_output(row.get("raw_prediction", row.get("prediction", "")))
        pred = {"wrong_word": wrong, "correct_word": correct}
    if not gold:
        wrong, correct = parse_edit_output(row.get("gold_target", row.get("reference", "")))
        gold = {"wrong_word": wrong, "correct_word": correct}
    pred_wrong = pred.get("wrong_word", "CORRECT")
    pred_correct = pred.get("correct_word", "CORRECT")
    gold_wrong = gold.get("wrong_word", "CORRECT")
    gold_correct = gold.get("correct_word", "CORRECT")
    raw = str(row.get("raw_prediction", row.get("prediction", "")))
    pred_error = pred_wrong != "CORRECT"
    gold_error = gold_wrong != "CORRECT"
    if "\n" not in raw or "Wrong word" not in raw or "Correct word" not in raw:
        if len(raw.split()) > 12:
            return "full_sentence_or_verbose_output"
        return "malformed_output"
    if not gold_error and not pred_error:
        return "correct_no_error"
    if not gold_error and pred_error:
        return "false_positive_error"
    if gold_error and not pred_error:
        return "false_negative_correct"
    if pred_wrong != gold_wrong:
        return "wrong_wrong_word"
    if pred_correct != gold_correct:
        return "right_wrong_word_wrong_correction"
    return "correct_error_correction"


def summarize(rows: list[dict]) -> dict:
    by_task: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("task") in {"SC", "GC"}:
            by_task[row["task"]].append(row)
    report = {}
    for task, task_rows in by_task.items():
        counts: dict[str, int] = defaultdict(int)
        for row in task_rows:
            counts[classify(row)] += 1
        clean_rows = []
        for row in task_rows:
            parsed_reference = row.get("parsed_reference") or {}
            if not parsed_reference:
                wrong, correct = parse_edit_output(row.get("gold_target", row.get("reference", "")))
                parsed_reference = {"wrong_word": wrong, "correct_word": correct}
            if parsed_reference.get("wrong_word") == "CORRECT":
                clean_rows.append(row)
        clean_ok = sum(1 for row in clean_rows if classify(row) == "correct_no_error")
        malformed = counts.get("malformed_output", 0) + counts.get("full_sentence_or_verbose_output", 0)
        report[task] = {
            "rows": len(task_rows),
            "category_counts": dict(sorted(counts.items())),
            "no_error_accuracy": clean_ok / max(1, len(clean_rows)),
            "malformed_output_rate": malformed / max(1, len(task_rows)),
            "sample_failures": [
                {
                    "id": row.get("id"),
                    "category": classify(row),
                    "gold_target": row.get("gold_target", row.get("reference")),
                    "raw_prediction": row.get("raw_prediction", row.get("prediction")),
                }
                for row in task_rows
                if classify(row) not in {"correct_no_error", "correct_error_correction"}
            ][:20],
        }
    return report


def markdown(report: dict) -> str:
    lines = ["# SC/GC Confusion Report", ""]
    for task, task_report in sorted(report.items()):
        lines.append(f"## {task}")
        lines.append("")
        lines.append(f"- Rows: `{task_report['rows']}`")
        lines.append(f"- No-error accuracy: `{task_report['no_error_accuracy']:.3f}`")
        lines.append(f"- Malformed/verbose rate: `{task_report['malformed_output_rate']:.3f}`")
        lines.append(f"- Categories: `{json.dumps(task_report['category_counts'], ensure_ascii=False, sort_keys=True)}`")
        if task_report["sample_failures"]:
            lines.append("- Failure sample:")
            for item in task_report["sample_failures"][:5]:
                lines.append(f"  - `{json.dumps(item, ensure_ascii=False, sort_keys=True)}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Categorize SC/GC errors from a raw prediction dump.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--output-md", default=None)
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    report = summarize(read_jsonl(input_path))
    json_path = ROOT / (args.output_json or f"{args.input}.scgc_confusion.json")
    md_path = ROOT / (args.output_md or f"{args.input}.scgc_confusion.md")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report) + "\n", encoding="utf-8")
    print(json.dumps({"output_json": str(json_path), "output_md": str(md_path)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
