#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import normalize_mr_answer

MR_FILES = {
    "uk": ["data/processed/final/uk/mr_train_final.jsonl", "data/processed/final/uk/mr_format_preservation.jsonl"],
    "sorbian": ["data/processed/final/sorbian/mr_train_final.jsonl", "data/processed/final/sorbian/mr_format_preservation.jsonl"],
}

FORBIDDEN_RE = re.compile(r"polymath|wmt2025|wmt25 test|certificate|language certificate", re.IGNORECASE)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def target_for(row: dict) -> str:
    if row.get("chosen") is not None:
        return str(row.get("chosen", ""))
    return str(row.get("target", ""))


def report_file(rel: str) -> dict:
    rows = read_jsonl(ROOT / rel)
    bad_parse = []
    forbidden = []
    for row in rows:
        target = target_for(row)
        normalized = normalize_mr_answer(target)
        if not normalized or not re.fullmatch(r"[-+]?\d+(?:\.\d+)?%?", normalized):
            bad_parse.append({"id": row.get("id"), "target": target, "normalized": normalized})
        blob = json.dumps(row, ensure_ascii=False)
        if FORBIDDEN_RE.search(blob):
            forbidden.append({"id": row.get("id"), "source_id": row.get("source_id")})
    return {
        "rows": len(rows),
        "parseable_rows": len(rows) - len(bad_parse),
        "bad_parse_count": len(bad_parse),
        "bad_parse_examples": bad_parse[:20],
        "forbidden_metadata_count": len(forbidden),
        "forbidden_examples": forbidden[:20],
        "status": "pass" if not bad_parse and not forbidden else "fail",
    }


def normalization_probes() -> list[dict]:
    probes = [
        ("42", "42"),
        ("42.0", "42"),
        ("The answer is 42.", "42"),
        ("Answer: 42", "42"),
        ("Відповідь: 42", "42"),
        ("\\boxed{42}", "42"),
        ("  -3.0  ", "-3"),
        ("1/2", "0.5"),
        ("50%", "50%"),
    ]
    return [
        {"input": value, "normalized": normalize_mr_answer(value), "expected": expected, "pass": normalize_mr_answer(value) == expected}
        for value, expected in probes
    ]


def markdown(report: dict) -> str:
    lines = ["# MR Data Quality Report", ""]
    lines.append("## Normalization Probes")
    lines.append("")
    for probe in report["normalization_probes"]:
        lines.append(f"- `{probe['input']}` -> `{probe['normalized']}` expected `{probe['expected']}`: `{probe['pass']}`")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("| Track | File | Rows | Parseable | Bad Parse | Forbidden Metadata | Status |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- |")
    for track, files in report["tracks"].items():
        for rel, row in files.items():
            lines.append(f"| {track} | `{rel}` | {row['rows']} | {row['parseable_rows']} | {row['bad_parse_count']} | {row['forbidden_metadata_count']} | {row['status']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check MR targets and final-answer preservation rows.")
    parser.add_argument("--output-json", default="results/triage/mr_data_quality.json")
    parser.add_argument("--output-md", default="results/triage/mr_data_quality.md")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    report = {"normalization_probes": normalization_probes(), "tracks": {}}
    has_issue = not all(probe["pass"] for probe in report["normalization_probes"])
    for track, files in MR_FILES.items():
        report["tracks"][track] = {}
        for rel in files:
            file_report = report_file(rel)
            report["tracks"][track][rel] = file_report
            has_issue = has_issue or file_report["status"] != "pass"
    json_path = ROOT / args.output_json
    md_path = ROOT / args.output_md
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    print(json.dumps({"output_json": str(json_path), "output_md": str(md_path), "has_issue": has_issue}, indent=2, sort_keys=True))
    return 1 if args.fail_on_issues and has_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())
