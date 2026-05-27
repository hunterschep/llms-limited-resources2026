#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import parse_edit_output, scgc_diagnostics, scgc_scores  # noqa: E402


DEFAULT_MODELS = {
    "prompt_only": "results/competitive_reboot/eval/sorbian/prompt_only_qwen35_2b_raw.jsonl",
    "selected_lineage_merge": "results/lineage_recovery/full_eval/merge_mt1p00_edit0p10_mr0p10_raw.jsonl",
    "edit_repair_tiny": "results/stage_b_rescue/full_eval/edit_repair_tiny_raw.jsonl",
    "reproduced_stage_b": "results/lineage_recovery/full_eval/reproduced_stage_b_raw.jsonl",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def validation_index(task: str) -> dict[str, dict[str, Any]]:
    path = ROOT / f"data/processed/sorbian/{task.lower()}_locked_validation.jsonl"
    return {str(row.get("id")): row for row in read_jsonl(path)}


def _prediction(row: dict[str, Any]) -> str:
    return str(row.get("raw_prediction", row.get("prediction", "")))


def _reference(row: dict[str, Any]) -> str:
    return str(row.get("gold_target", row.get("reference", "")))


def _exists_in_input(word: str, sentence: str) -> bool:
    if word == "CORRECT":
        return True
    return bool(word and re.search(rf"(?<!\w){re.escape(word)}(?!\w)", sentence))


def _malformed(raw: str) -> bool:
    return "Wrong word" not in raw or "Correct word" not in raw


def _verbose(raw: str) -> bool:
    return raw.count("Wrong word") > 1 or raw.count("Correct word") > 1 or len(raw.split()) > 24


def summarize_model(name: str, raw_path: Path) -> dict[str, Any]:
    rows = read_jsonl(raw_path)
    report: dict[str, Any] = {"model": name, "raw_path": str(raw_path), "tasks": {}}
    for task in ("SC", "GC"):
        task_rows = [row for row in rows if row.get("task") == task]
        index = validation_index(task)
        preds = [_prediction(row) for row in task_rows]
        refs = [_reference(row) for row in task_rows]
        diagnostics = scgc_diagnostics(preds, refs)
        scores = scgc_scores(preds, refs)
        false_positive_details = []
        pred_wrong_counter: Counter[str] = Counter()
        pred_correction_counter: Counter[str] = Counter()
        for row in task_rows:
            pred_wrong, pred_correct = parse_edit_output(_prediction(row))
            gold_wrong, gold_correct = parse_edit_output(_reference(row))
            pred_error = pred_wrong != "CORRECT"
            gold_error = gold_wrong != "CORRECT"
            source = index.get(str(row.get("id")), {})
            sentence = str(source.get("input", ""))
            if pred_error:
                pred_wrong_counter[pred_wrong] += 1
                pred_correction_counter[pred_correct] += 1
            if pred_error and not gold_error:
                false_positive_details.append(
                    {
                        "id": row.get("id"),
                        "language": source.get("language"),
                        "sentence": sentence,
                        "gold_target": _reference(row),
                        "raw_output": _prediction(row),
                        "parsed_output": {"wrong_word": pred_wrong, "correct_word": pred_correct},
                        "predicted_word_exists_in_input": _exists_in_input(pred_wrong, sentence),
                        "correction_same_as_word": pred_wrong == pred_correct,
                        "malformed": _malformed(_prediction(row)),
                        "verbose_or_multi_edit": _verbose(_prediction(row)),
                        "prompt_template": (source.get("messages") or [{}])[0].get("content", ""),
                        "generation_settings": {"do_sample": False, "temperature": 0, "max_new_tokens": 256},
                    }
                )
        clean_total = diagnostics["gold_correct"]
        clean_ok = diagnostics["detection_tn"]
        malformed_count = sum(1 for row in task_rows if _malformed(_prediction(row)))
        verbose_count = sum(1 for row in task_rows if _verbose(_prediction(row)))
        report["tasks"][task] = {
            "total": len(task_rows),
            "gold_error": diagnostics["gold_error"],
            "gold_correct": diagnostics["gold_correct"],
            "predicted_error": diagnostics["pred_error"],
            "predicted_correct": diagnostics["pred_correct"],
            "no_error_accuracy": clean_ok / max(1, clean_total),
            "detection_confusion": {
                "tp": diagnostics["detection_tp"],
                "fp": diagnostics["detection_fp"],
                "fn": diagnostics["detection_fn"],
                "tn": diagnostics["detection_tn"],
            },
            "detection_f1": scores["detection_f1"],
            "correction_f1": scores["correction_f1"],
            "wrong_word_exact": diagnostics["wrong_word_exact"],
            "correction_exact": diagnostics["correction_exact"],
            "malformed_output_rate": malformed_count / max(1, len(task_rows)),
            "full_sentence_or_multi_edit_rate": verbose_count / max(1, len(task_rows)),
            "top_false_positive_wrong_words": pred_wrong_counter.most_common(20),
            "top_hallucinated_corrections": pred_correction_counter.most_common(20),
            "false_positive_samples": false_positive_details[:80],
        }
    return report


def markdown(report: dict[str, Any]) -> str:
    lines = ["# Final Salvage SC/GC Audit", ""]
    for model in report["models"]:
        lines.append(f"## {model['model']}")
        lines.append("")
        lines.append("| Task | Total | Gold error | Gold CORRECT | Pred error | Pred CORRECT | No-error acc | Det F1 | Corr F1 | Malformed | Multi-edit |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for task, task_report in sorted(model["tasks"].items()):
            lines.append(
                f"| {task} | {task_report['total']} | {task_report['gold_error']} | {task_report['gold_correct']} | "
                f"{task_report['predicted_error']} | {task_report['predicted_correct']} | {task_report['no_error_accuracy']:.3f} | "
                f"{task_report['detection_f1']:.3f} | {task_report['correction_f1']:.3f} | "
                f"{task_report['malformed_output_rate']:.3f} | {task_report['full_sentence_or_multi_edit_rate']:.3f} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Diagnosis",
            "",
            "- Dominant failure: the evaluated models predict an edit for essentially every SC/GC item.",
            "- Parser misclassification is not the main issue; raw outputs are usually parseable two-line edit outputs.",
            "- The failure is consistent with a strong generation/training prior toward finding an error even when the target is CORRECT/CORRECT.",
            "- Official WMT26 SC/GC descriptions include no-error sentences, so this is a hidden-test risk.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results/final_salvage/scgc_audit")
    parser.add_argument("--model", nargs=2, action="append", metavar=("NAME", "RAW_JSONL"))
    args = parser.parse_args()
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    model_paths = dict(DEFAULT_MODELS)
    for item in args.model or []:
        model_paths[item[0]] = item[1]
    reports = []
    skipped = {}
    for name, rel in model_paths.items():
        path = Path(rel)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            skipped[name] = str(path)
            continue
        reports.append(summarize_model(name, path))
    final = {"models": reports, "skipped": skipped}
    (output_dir / "scgc_audit.json").write_text(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "scgc_audit.md").write_text(markdown(final), encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "models": [r["model"] for r in reports], "skipped": skipped}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
