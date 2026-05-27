#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import normalize_mr_answer  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def classify(row: dict) -> str:
    pred = str(row.get("raw_prediction", row.get("prediction", "")))
    norm_pred = str(row.get("normalized_prediction") or normalize_mr_answer(pred))
    norm_ref = str(row.get("normalized_reference") or normalize_mr_answer(row.get("gold_target", row.get("reference", ""))))
    if norm_pred == norm_ref:
        if pred.strip() == str(row.get("gold_target", "")).strip():
            return "exact_normalized_match"
        return "parser_normalization_rescued"
    if not pred.strip():
        return "empty_answer"
    if not re.search(r"[-+]?\d", pred):
        return "nonnumeric_answer"
    if len(pred.split()) > 8:
        return "explanation_or_verbose_answer"
    return "wrong_numeric_answer"


def summarize(rows: list[dict]) -> dict:
    mr_rows = [row for row in rows if row.get("task") == "MR"]
    counts = Counter(classify(row) for row in mr_rows)
    return {
        "rows": len(mr_rows),
        "category_counts": dict(sorted(counts.items())),
        "malformed_output_rate": (counts.get("empty_answer", 0) + counts.get("nonnumeric_answer", 0) + counts.get("explanation_or_verbose_answer", 0)) / max(1, len(mr_rows)),
        "wrong_examples": [
            {
                "id": row.get("id"),
                "category": classify(row),
                "gold_target": row.get("gold_target", row.get("reference")),
                "raw_prediction": row.get("raw_prediction", row.get("prediction")),
                "normalized_prediction": row.get("normalized_prediction") or normalize_mr_answer(row.get("raw_prediction", row.get("prediction", ""))),
                "normalized_reference": row.get("normalized_reference") or normalize_mr_answer(row.get("gold_target", row.get("reference", ""))),
            }
            for row in mr_rows
            if classify(row) not in {"exact_normalized_match", "parser_normalization_rescued"}
        ][:20],
    }


def markdown(report: dict) -> str:
    lines = ["# MR Raw Error Report", ""]
    lines.append(f"- Rows: `{report['rows']}`")
    lines.append(f"- Malformed/verbose rate: `{report['malformed_output_rate']:.3f}`")
    lines.append(f"- Categories: `{json.dumps(report['category_counts'], ensure_ascii=False, sort_keys=True)}`")
    if report["wrong_examples"]:
        lines.append("- Wrong examples:")
        for item in report["wrong_examples"][:5]:
            lines.append(f"  - `{json.dumps(item, ensure_ascii=False, sort_keys=True)}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Categorize MR errors from a raw prediction dump.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--output-md", default=None)
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    report = summarize(read_jsonl(input_path))
    json_path = ROOT / (args.output_json or f"{args.input}.mr_errors.json")
    md_path = ROOT / (args.output_md or f"{args.input}.mr_errors.md")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    print(json.dumps({"output_json": str(json_path), "output_md": str(md_path)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
