#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from triage_data_sanity import FINAL_FILES, edit_report, read_jsonl
from wmt26.eval.metrics import scgc_scores


def always_correct_scores(refs: list[str]) -> dict[str, float]:
    return scgc_scores(["Wrong word: CORRECT\nCorrect word: CORRECT"] * len(refs), refs)


def markdown(report: dict) -> str:
    lines = ["# Edit Data Balance Report", ""]
    lines.append("| Track | Task | Rows | Error | Clean | Clean Ratio | Always-Error Detection F1 | Always-CORRECT Detection F1 | Status |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for track, tasks in report.items():
        for task, row in tasks.items():
            lines.append(
                "| {track} | {task} | {rows} | {error_rows} | {clean_rows} | {clean_ratio:.3f} | {always_error:.3f} | {always_correct:.3f} | {status} |".format(
                    track=track,
                    task=task,
                    rows=row["rows"],
                    error_rows=row["error_rows"],
                    clean_rows=row["clean_rows"],
                    clean_ratio=row["clean_ratio"],
                    always_error=row["always_error_scores"]["detection_f1"],
                    always_correct=row["always_correct_scores"]["detection_f1"],
                    status=row["status"],
                )
            )
    lines.append("")
    lines.append("Balanced edit data should keep clean/error ratio close to 0.5 so models cannot win detection by always predicting an error.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Report SC/GC clean/error balance and trivial-baseline scores.")
    parser.add_argument("--output-json", default="results/triage/edit_data_balance.json")
    parser.add_argument("--output-md", default="results/triage/edit_data_balance.md")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    report: dict[str, dict] = {}
    warn = False
    for track, tasks in FINAL_FILES.items():
        report[track] = {}
        for task, rel in tasks.items():
            if task not in {"SC", "GC"}:
                continue
            rows = read_jsonl(ROOT / rel)
            refs = [str(row.get("target", "")) for row in rows]
            task_report = edit_report(rows)
            task_report["always_correct_scores"] = always_correct_scores(refs)
            report[track][task] = task_report
            warn = warn or task_report["status"] != "pass"

    json_path = ROOT / args.output_json
    md_path = ROOT / args.output_md
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    print(json.dumps({"output_json": str(json_path), "output_md": str(md_path), "warn": warn}, indent=2, sort_keys=True))
    return 1 if args.fail_on_warn and warn else 0


if __name__ == "__main__":
    raise SystemExit(main())
