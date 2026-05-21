#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import normalize_choice_answer, normalize_mr_answer, scgc_diagnostics, scgc_scores


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def diagnose(rows: list[dict]) -> dict:
    by_task: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_task[row.get("task", "UNKNOWN")].append(row)
    report: dict[str, dict] = {}
    for task, task_rows in by_task.items():
        predictions = [str(row.get("raw_prediction", "")) for row in task_rows]
        references = [str(row.get("gold_target", "")) for row in task_rows]
        task_report: dict = {"rows": len(task_rows)}
        if task in {"SC", "GC"}:
            task_report["scores"] = scgc_scores(predictions, references)
            task_report["confusion"] = scgc_diagnostics(predictions, references)
            parsed_pred = Counter("ERROR" if row.get("parsed_prediction", {}).get("wrong_word") != "CORRECT" else "CORRECT" for row in task_rows)
            parsed_gold = Counter("ERROR" if row.get("parsed_reference", {}).get("wrong_word") != "CORRECT" else "CORRECT" for row in task_rows)
            task_report["predicted_label_counts"] = dict(parsed_pred)
            task_report["gold_label_counts"] = dict(parsed_gold)
            task_report["format_failures"] = [
                {"id": row.get("id"), "raw_prediction": row.get("raw_prediction")}
                for row in task_rows
                if not isinstance(row.get("parsed_prediction"), dict)
            ][:20]
        elif task == "QA":
            pred_counts = Counter(normalize_choice_answer(row.get("raw_prediction", "")) for row in task_rows)
            correct = [
                normalize_choice_answer(row.get("raw_prediction", "")) == normalize_choice_answer(row.get("gold_target", ""))
                for row in task_rows
            ]
            task_report["accuracy"] = sum(correct) / max(1, len(correct))
            task_report["prediction_counts"] = dict(pred_counts)
            task_report["wrong_examples"] = [
                {
                    "id": row.get("id"),
                    "gold": row.get("gold_target"),
                    "prediction": row.get("raw_prediction"),
                    "normalized_prediction": normalize_choice_answer(row.get("raw_prediction", "")),
                }
                for row, ok in zip(task_rows, correct)
                if not ok
            ][:20]
        elif task == "MR":
            correct = [
                normalize_mr_answer(row.get("raw_prediction", "")) == normalize_mr_answer(row.get("gold_target", ""))
                for row in task_rows
            ]
            task_report["accuracy"] = sum(correct) / max(1, len(correct))
            task_report["wrong_examples"] = [
                {
                    "id": row.get("id"),
                    "gold": row.get("gold_target"),
                    "prediction": row.get("raw_prediction"),
                    "normalized_prediction": normalize_mr_answer(row.get("raw_prediction", "")),
                    "normalized_reference": normalize_mr_answer(row.get("gold_target", "")),
                }
                for row, ok in zip(task_rows, correct)
                if not ok
            ][:20]
        report[task] = task_report
    return report


def markdown(report: dict) -> str:
    lines = ["# Prediction Dump Diagnostics", ""]
    for task, task_report in sorted(report.items()):
        lines.append(f"## {task}")
        lines.append("")
        for key, value in task_report.items():
            if key.endswith("examples") or key == "format_failures":
                continue
            lines.append(f"- `{key}`: `{json.dumps(value, ensure_ascii=False, sort_keys=True)}`")
        for key in ("wrong_examples", "format_failures"):
            if task_report.get(key):
                lines.append(f"- `{key}` sample:")
                for item in task_report[key][:5]:
                    lines.append(f"  - `{json.dumps(item, ensure_ascii=False, sort_keys=True)}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize raw prediction dumps for parser, MR, QA, SC, and GC failures.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--output-md", default=None)
    args = parser.parse_args()

    rows = read_jsonl(ROOT / args.input if not Path(args.input).is_absolute() else Path(args.input))
    report = diagnose(rows)
    json_path = ROOT / (args.output_json or f"{args.input}.diagnostics.json")
    md_path = ROOT / (args.output_md or f"{args.input}.diagnostics.md")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report) + "\n", encoding="utf-8")
    print(json.dumps({"output_json": str(json_path), "output_md": str(md_path)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
