#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_model import read_jsonl, score_task
from wmt26.eval.metrics import (
    exact_accuracy,
    normalize_choice_answer,
    normalize_mr_answer,
    normalized_accuracy,
    scgc_diagnostics,
)


def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def evaluate_config(config_path: Path, limit: int | None) -> dict:
    config = load_config(config_path)
    tasks: dict[str, dict] = {}
    failures: list[str] = []
    for task, files in config.get("datasets", {}).items():
        rows: list[dict] = []
        for rel in files:
            rows.extend(read_jsonl(ROOT / rel, limit))
        if limit:
            rows = rows[:limit]
        references = [str(row.get("target", "")) for row in rows]
        predictions = references[:]
        scores = score_task(task, predictions, references)
        task_report: dict = {
            "rows": len(rows),
            "scores": scores,
        }
        if task in {"QA", "MR"}:
            task_report["exact_accuracy"] = exact_accuracy(predictions, references)
            task_report["normalized_accuracy"] = normalized_accuracy(predictions, references, task)
            if task == "QA":
                task_report["sample_normalized"] = [
                    {
                        "id": row.get("id"),
                        "target": row.get("target"),
                        "normalized": normalize_choice_answer(row.get("target", "")),
                    }
                    for row in rows[:5]
                ]
            else:
                task_report["sample_normalized"] = [
                    {
                        "id": row.get("id"),
                        "target": row.get("target"),
                        "normalized": normalize_mr_answer(row.get("target", "")),
                    }
                    for row in rows[:5]
                ]
            if task_report["normalized_accuracy"] < 1.0:
                failures.append(f"{config_path}:{task} oracle normalized accuracy {task_report['normalized_accuracy']:.6f}")
        elif task in {"SC", "GC"}:
            task_report["diagnostics"] = scgc_diagnostics(predictions, references)
            if scores.get("detection_f1", 0.0) < 1.0 or scores.get("correction_f1", 0.0) < 1.0:
                failures.append(f"{config_path}:{task} oracle SC/GC scores {scores}")
        elif task == "MT":
            if scores.get("chrf++", 0.0) < 99.0:
                failures.append(f"{config_path}:{task} oracle chrF++ {scores.get('chrf++')}")
        tasks[task] = task_report
    return {
        "config": str(config_path.relative_to(ROOT)),
        "track": config.get("track"),
        "tasks": tasks,
        "failures": failures,
        "passed": not failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Oracle-score WMT26 eval files by feeding gold targets into the evaluator.")
    parser.add_argument("--configs", nargs="+", default=["configs/eval/uk.yaml", "configs/eval/sorbian.yaml"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default="results/triage/oracle_eval_report.json")
    parser.add_argument("--no-fail", action="store_true", help="Write the report but return 0 even if an oracle check fails.")
    args = parser.parse_args()

    reports = [evaluate_config(ROOT / rel, args.limit) for rel in args.configs]
    output = {
        "passed": all(report["passed"] for report in reports),
        "reports": reports,
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    if output["passed"] or args.no_fail:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
