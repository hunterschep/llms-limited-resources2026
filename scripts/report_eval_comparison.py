#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


FIELDS = [
    "report",
    "track",
    "model",
    "MT_chrF",
    "MT_BLEU",
    "QA_accuracy",
    "SC_detection_F1",
    "SC_correction_F1",
    "GC_detection_F1",
    "GC_correction_F1",
    "MR_accuracy",
    "MT_score",
    "QA_score",
    "SC_score",
    "GC_score",
    "MR_score",
    "overall_equal_weighted_score",
    "notes",
]


def pct(value):
    if value is None:
        return None
    return value * 100 if 0 <= value <= 1 else value


def row_from_report(rel: str, data: dict) -> dict:
    task_scores = data.get("task_scores", {})
    aggregate = data.get("aggregate", {})
    return {
        "report": rel,
        "track": data.get("track"),
        "model": data.get("model"),
        "MT_chrF": task_scores.get("MT", {}).get("chrf++"),
        "MT_BLEU": task_scores.get("MT", {}).get("bleu"),
        "QA_accuracy": pct(task_scores.get("QA", {}).get("accuracy")),
        "SC_detection_F1": pct(task_scores.get("SC", {}).get("detection_f1")),
        "SC_correction_F1": pct(task_scores.get("SC", {}).get("correction_f1")),
        "GC_detection_F1": pct(task_scores.get("GC", {}).get("detection_f1")),
        "GC_correction_F1": pct(task_scores.get("GC", {}).get("correction_f1")),
        "MR_accuracy": pct(task_scores.get("MR", {}).get("accuracy")),
        "MT_score": aggregate.get("MT_score"),
        "QA_score": aggregate.get("QA_score"),
        "SC_score": aggregate.get("SC_score"),
        "GC_score": aggregate.get("GC_score"),
        "MR_score": aggregate.get("MR_score"),
        "overall_equal_weighted_score": aggregate.get("overall_score"),
        "notes": "oracle" if data.get("oracle") else "",
    }


def row_from_eval_run(data: dict) -> dict:
    return {
        "report": data.get("eval_id"),
        "track": data.get("track"),
        "model": data.get("checkpoint_path"),
        "MT_chrF": data.get("MT_chrF"),
        "MT_BLEU": data.get("MT_BLEU"),
        "QA_accuracy": pct(data.get("QA_accuracy")),
        "SC_detection_F1": pct(data.get("SC_detection_F1")),
        "SC_correction_F1": pct(data.get("SC_correction_F1")),
        "GC_detection_F1": pct(data.get("GC_detection_F1")),
        "GC_correction_F1": pct(data.get("GC_correction_F1")),
        "MR_accuracy": pct(data.get("MR_accuracy")),
        "MT_score": data.get("MT_score"),
        "QA_score": data.get("QA_score"),
        "SC_score": data.get("SC_score"),
        "GC_score": data.get("GC_score"),
        "MR_score": data.get("MR_score"),
        "overall_equal_weighted_score": data.get("overall_equal_weighted_score"),
        "notes": data.get("notes", ""),
    }


def fmt(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def markdown_table(rows: list[dict]) -> str:
    headers = FIELDS
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field)).replace("|", "\\|") for field in headers) + " |")
    return "\n".join(lines)


def csv_table(rows: list[dict]) -> str:
    from io import StringIO

    handle = StringIO()
    writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="*")
    parser.add_argument("--eval-runs-jsonl", default=None, help="Read appended eval records from a JSONL file.")
    parser.add_argument("--format", choices=["json", "markdown", "csv"], default="json")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    rows = []
    if args.eval_runs_jsonl:
        path = ROOT / args.eval_runs_jsonl
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(row_from_eval_run(json.loads(line)))
    for rel in args.reports:
        path = ROOT / rel
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(row_from_report(rel, data))
    rows.sort(key=lambda row: (str(row.get("track")), str(row.get("report"))))
    if args.format == "json":
        text = json.dumps(rows, indent=2, sort_keys=True)
    elif args.format == "markdown":
        text = markdown_table(rows)
    else:
        text = csv_table(rows)
    if args.output:
        out = ROOT / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8")
    else:
        sys.stdout.write(text + ("" if text.endswith("\n") else "\n"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
