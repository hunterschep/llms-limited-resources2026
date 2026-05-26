#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from stage_b_rescue_common import (  # noqa: E402
    ERROR_ANALYSIS_DIR,
    STAGE_B_MODELS,
    compact_score_table,
    direction,
    git_commit,
    load_eval_result,
    load_raw_predictions,
    load_validation_by_task,
    markdown_table,
    numeric_like,
    prompt_text,
    raw_path,
    rel,
    target_text,
    write_json,
    write_jsonl,
)
from wmt26.eval.metrics import (  # noqa: E402
    fallback_chrf,
    normalize_mr_answer,
    parse_edit_output,
    scgc_diagnostics,
)


def _edit_malformed(text: str) -> bool:
    lines = [line.strip() for line in str(text).splitlines() if line.strip()]
    has_wrong = any(re.match(r"(?i)^\s*(?:wrong word|wrong|incorrect word|incorrect)\s*[:=-]", line) for line in lines)
    has_correct = any(re.match(r"(?i)^\s*(?:correct word|correct|correction)\s*[:=-]", line) for line in lines)
    if str(text).strip().upper() == "CORRECT":
        return False
    return not (has_wrong and has_correct)


def _looks_like_rewrite(text: str, gold_sentence: str) -> bool:
    parsed = parse_edit_output(text)
    for token in parsed:
        if token == "CORRECT":
            continue
        if len(token.split()) > 4:
            return True
        if len(token) > 60 and token in gold_sentence:
            return True
    return False


def mr_category(prediction: str, reference: str, correct: bool) -> str:
    if correct:
        return "correct"
    stripped = str(prediction).strip()
    if not stripped:
        return "empty_answer"
    parsed = normalize_mr_answer(prediction)
    if not numeric_like(parsed) and numeric_like(reference):
        return "nonnumeric_or_unparseable"
    if len(stripped.split()) > 12 or "\n" in stripped:
        return "verbose_or_explanation"
    return "wrong_final_numeric_answer"


def analyze_mr(validation: list[dict[str, Any]], raw_by_model: dict[str, dict[tuple[str, str], dict[str, Any]]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    counters: dict[str, Counter[str]] = {model: Counter() for model in raw_by_model}
    for gold in validation:
        row = {
            "id": gold.get("id"),
            "language": gold.get("language"),
            "prompt": prompt_text(gold),
            "gold_answer": target_text(gold),
            "parsed_gold": normalize_mr_answer(target_text(gold)),
        }
        for model, raw in raw_by_model.items():
            pred = str((raw.get(("MR", str(gold.get("id")))) or {}).get("prediction", ""))
            parsed = normalize_mr_answer(pred)
            correct = parsed == row["parsed_gold"]
            category = mr_category(pred, row["gold_answer"], correct)
            row[f"{model}_raw"] = pred
            row[f"{model}_parsed"] = parsed
            row[f"{model}_correct"] = correct
            row[f"{model}_category"] = category
            counters[model][category] += 1
        rows.append(row)
    summary = {model: dict(counter) for model, counter in counters.items()}
    return rows, summary


def analyze_edit(task: str, validation: list[dict[str, Any]], raw_by_model: dict[str, dict[tuple[str, str], dict[str, Any]]]) -> dict[str, Any]:
    refs = [target_text(row) for row in validation]
    result: dict[str, Any] = {"task": task, "models": {}}
    for model, raw in raw_by_model.items():
        predictions = [str((raw.get((task, str(row.get("id")))) or {}).get("prediction", "")) for row in validation]
        diagnostics = scgc_diagnostics(predictions, refs)
        pred_pairs = [parse_edit_output(pred) for pred in predictions]
        ref_pairs = [parse_edit_output(ref) for ref in refs]
        no_error_total = sum(1 for wrong, _ in ref_pairs if wrong == "CORRECT")
        no_error_correct = sum(
            1
            for (p_wrong, p_correct), (r_wrong, r_correct) in zip(pred_pairs, ref_pairs)
            if r_wrong == "CORRECT" and p_wrong == "CORRECT" and p_correct == "CORRECT"
        )
        malformed = sum(1 for pred in predictions if _edit_malformed(pred))
        rewrites = sum(1 for pred, gold in zip(predictions, validation) if _looks_like_rewrite(pred, str(gold.get("input", ""))))
        false_positive_examples = []
        false_negative_examples = []
        for pred, pred_pair, ref_pair, gold in zip(predictions, pred_pairs, ref_pairs, validation):
            pred_error = pred_pair[0] != "CORRECT"
            ref_error = ref_pair[0] != "CORRECT"
            if pred_error and not ref_error and len(false_positive_examples) < 20:
                false_positive_examples.append(
                    {
                        "id": gold.get("id"),
                        "input": gold.get("input"),
                        "prediction": pred,
                        "reference": target_text(gold),
                    }
                )
            if (not pred_error) and ref_error and len(false_negative_examples) < 20:
                false_negative_examples.append(
                    {
                        "id": gold.get("id"),
                        "input": gold.get("input"),
                        "prediction": pred,
                        "reference": target_text(gold),
                    }
                )
        result["models"][model] = {
            **diagnostics,
            "no_error_accuracy": no_error_correct / max(1, no_error_total),
            "malformed_output_rate": malformed / max(1, len(predictions)),
            "full_sentence_rewrite_rate": rewrites / max(1, len(predictions)),
            "false_positive_examples": false_positive_examples,
            "false_negative_examples": false_negative_examples,
        }
    return result


def analyze_mt(validation: list[dict[str, Any]], raw_by_model: dict[str, dict[tuple[str, str], dict[str, Any]]]) -> dict[str, Any]:
    prompt_raw = raw_by_model.get("prompt_only_qwen35_2b", {})
    stage_b_raw = raw_by_model.get("stage_b_mt_large", {})
    by_direction: dict[str, list[dict[str, Any]]] = {}
    examples = []
    for gold in validation:
        key = ("MT", str(gold.get("id")))
        ref = target_text(gold)
        prompt_pred = str((prompt_raw.get(key) or {}).get("prediction", ""))
        stage_b_pred = str((stage_b_raw.get(key) or {}).get("prediction", ""))
        prompt_chrf = fallback_chrf([prompt_pred], [ref])
        stage_b_chrf = fallback_chrf([stage_b_pred], [ref])
        item = {
            "id": gold.get("id"),
            "direction": direction(gold),
            "source": gold.get("input"),
            "reference": ref,
            "prompt_only_prediction": prompt_pred,
            "stage_b_prediction": stage_b_pred,
            "prompt_only_chrf": prompt_chrf,
            "stage_b_chrf": stage_b_chrf,
            "delta_chrf": stage_b_chrf - prompt_chrf,
        }
        by_direction.setdefault(item["direction"], []).append(item)
        examples.append(item)
    direction_summary = {
        key: {
            "examples": len(items),
            "mean_prompt_only_chrf": sum(i["prompt_only_chrf"] for i in items) / max(1, len(items)),
            "mean_stage_b_chrf": sum(i["stage_b_chrf"] for i in items) / max(1, len(items)),
            "mean_delta_chrf": sum(i["delta_chrf"] for i in items) / max(1, len(items)),
        }
        for key, items in sorted(by_direction.items())
    }
    return {
        "direction_summary": direction_summary,
        "strong_improvements": sorted(examples, key=lambda row: row["delta_chrf"], reverse=True)[:25],
        "regressions": sorted(examples, key=lambda row: row["delta_chrf"])[:25],
    }


def write_markdown(summary: dict[str, Any]) -> None:
    doc = ROOT / "docs/85_stage_b_raw_error_analysis.md"
    lines = [
        "# Stage B Raw Error Analysis",
        "",
        f"Generated at commit `{summary['git_commit']}`.",
        "",
        "## Inputs",
        "",
    ]
    for model, path in summary["raw_inputs"].items():
        lines.append(f"- `{model}`: `{path}`")
    lines.extend(
        [
            "",
            "## MR Diagnosis",
            "",
            "The MR set is tiny, so the Stage B drop from `8.333` to `4.167` is likely one additional locked-validation miss. It still matters because MR is equally weighted.",
            "",
        ]
    )
    mr_rows = []
    for model, categories in summary["mr_categories"].items():
        mr_rows.append({"model": model, **categories})
    all_category_keys = sorted({key for row in mr_rows for key in row if key != "model"})
    lines.extend(markdown_table(mr_rows, ["model", *all_category_keys]))
    lines.extend(["", "## SC/GC Diagnosis", ""])
    for task in ("SC", "GC"):
        lines.append(f"### {task}")
        edit_rows = []
        for model, values in summary["edit"][task]["models"].items():
            edit_rows.append(
                {
                    "model": model,
                    "pred_error": values["pred_error"],
                    "tp": values["detection_tp"],
                    "fp": values["detection_fp"],
                    "fn": values["detection_fn"],
                    "tn": values["detection_tn"],
                    "no_error_acc": values["no_error_accuracy"],
                    "malformed": values["malformed_output_rate"],
                    "rewrite": values["full_sentence_rewrite_rate"],
                    "correction_exact": values["correction_exact"],
                }
            )
        lines.extend(markdown_table(edit_rows, ["model", "pred_error", "tp", "fp", "fn", "tn", "no_error_acc", "malformed", "rewrite", "correction_exact"]))
        lines.append("")
    lines.extend(["## MT Diagnosis", ""])
    mt_rows = []
    for key, values in summary["mt"]["direction_summary"].items():
        mt_rows.append(
            {
                "direction": key,
                "examples": values["examples"],
                "prompt_chrf": values["mean_prompt_only_chrf"],
                "stage_b_chrf": values["mean_stage_b_chrf"],
                "delta": values["mean_delta_chrf"],
            }
        )
    lines.extend(markdown_table(mt_rows, ["direction", "examples", "prompt_chrf", "stage_b_chrf", "delta"]))
    lines.extend(
        [
            "",
            "## Training Implication",
            "",
            "- Keep Stage B as the MT anchor.",
            "- Do not reuse Stage C replay: it preserved MT but collapsed edit detection.",
            "- Repair MR with final-answer-only examples plus MT anchor replay.",
            "- Repair edit behavior with hard no-error and one-word correction rows; keep the repair tiny and gated.",
        ]
    )
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=list(STAGE_B_MODELS))
    parser.add_argument("--output-dir", default="results/stage_b_rescue/error_analysis")
    args = parser.parse_args()
    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    validation = load_validation_by_task()
    raw_by_model = {model: load_raw_predictions(model) for model in args.models}
    missing = {model: str(raw_path(model)) for model, raw in raw_by_model.items() if not raw}
    if missing:
        raise SystemExit(f"Missing raw predictions: {json.dumps(missing, indent=2)}")

    mr_rows, mr_categories = analyze_mr(validation["MR"], raw_by_model)
    sc_summary = analyze_edit("SC", validation["SC"], raw_by_model)
    gc_summary = analyze_edit("GC", validation["GC"], raw_by_model)
    mt_summary = analyze_mt(validation["MT"], raw_by_model)
    eval_table = compact_score_table([ROOT / f"results/competitive_reboot/eval/sorbian/{model}.json" for model in args.models])
    summary = {
        "git_commit": git_commit(),
        "raw_inputs": {model: rel(raw_path(model)) for model in args.models},
        "eval_table": eval_table,
        "mr_categories": mr_categories,
        "edit": {"SC": sc_summary, "GC": gc_summary},
        "mt": mt_summary,
    }
    write_json(out_dir / "stage_b_raw_error_analysis_summary.json", summary)
    write_jsonl(out_dir / "stage_b_mr_audit.jsonl", mr_rows)
    write_json(out_dir / "stage_b_edit_audit.json", {"SC": sc_summary, "GC": gc_summary})
    write_json(out_dir / "stage_b_mt_regression_audit.json", mt_summary)
    write_markdown(summary)
    print(f"Wrote {out_dir / 'stage_b_raw_error_analysis_summary.json'}")
    print("Wrote docs/85_stage_b_raw_error_analysis.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
