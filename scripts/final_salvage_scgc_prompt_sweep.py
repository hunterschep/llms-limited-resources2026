#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_model import generate_predictions, load_generation_bundle, read_jsonl, score_task  # noqa: E402
from wmt26.eval.metrics import aggregate_wmt_scores, parse_edit_output, scgc_diagnostics  # noqa: E402


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _balanced_rows(path: Path, limit: int, seed: int = 2713) -> list[dict[str, Any]]:
    import random

    rows = read_jsonl(path)
    clean = [row for row in rows if parse_edit_output(str(row.get("target", "")))[0] == "CORRECT"]
    error = [row for row in rows if parse_edit_output(str(row.get("target", "")))[0] != "CORRECT"]
    rng = random.Random(seed)
    rng.shuffle(clean)
    rng.shuffle(error)
    half = max(1, limit // 2)
    selected = clean[:half] + error[: limit - half]
    rng.shuffle(selected)
    return selected


def _apply_variant(row: dict[str, Any], task: str, variant: dict[str, Any]) -> dict[str, Any]:
    new = deepcopy(row)
    messages = [dict(message) for message in new.get("messages", []) if message.get("role") != "assistant"]
    if not messages:
        messages = [{"role": "system", "content": ""}, {"role": "user", "content": f"Sentence:\n{new.get('input', '')}\n"}]
    system = variant["sc_system"] if task == "SC" else variant["gc_system"]
    if messages[0].get("role") == "system":
        messages[0]["content"] = system
    else:
        messages.insert(0, {"role": "system", "content": system})
    new["messages"] = messages
    return new


def _no_error_accuracy(preds: list[str], refs: list[str]) -> float:
    total = 0
    ok = 0
    for pred, ref in zip(preds, refs):
        pred_wrong, _ = parse_edit_output(pred)
        ref_wrong, _ = parse_edit_output(ref)
        if ref_wrong == "CORRECT":
            total += 1
            ok += pred_wrong == "CORRECT"
    return ok / max(1, total)


def evaluate_variant(bundle, config: dict[str, Any], variant_name: str, variant: dict[str, Any], max_new_tokens: int, per_task_limit: int) -> dict[str, Any]:
    task_scores = {}
    extra = {}
    raw_rows = []
    for task in ("SC", "GC"):
        rel = config["datasets"][task][0]
        rows = _balanced_rows(ROOT / rel, per_task_limit, seed=2713 + (0 if task == "SC" else 100))
        rows = [_apply_variant(row, task, variant) for row in rows]
        refs = [str(row.get("target", "")) for row in rows]
        preds = generate_predictions(bundle, rows, max_new_tokens=max_new_tokens, batch_size=int(config.get("batch_size", 8)), task=f"{task}:{variant_name}:{max_new_tokens}")
        task_scores[task] = score_task(task, preds, refs)
        diag = scgc_diagnostics(preds, refs)
        extra[task] = {
            "no_error_accuracy": _no_error_accuracy(preds, refs),
            "diagnostics": diag,
        }
        for row, pred, ref in zip(rows, preds, refs):
            raw_rows.append({"id": row.get("id"), "task": task, "variant": variant_name, "max_new_tokens": max_new_tokens, "prediction": pred, "reference": ref})
    aggregate = aggregate_wmt_scores(task_scores)
    return {"variant": variant_name, "max_new_tokens": max_new_tokens, "task_scores": task_scores, "aggregate": aggregate, "extra": extra, "raw_predictions": raw_rows}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10")
    parser.add_argument("--eval-config", default="configs/eval/final_salvage_scgc_probe.yaml")
    parser.add_argument("--prompt-config", default="configs/prompts/final_salvage_scgc.yaml")
    parser.add_argument("--output-dir", default="results/final_salvage/prompt_sweep")
    parser.add_argument("--per-task-limit", type=int, default=240)
    args = parser.parse_args()
    eval_config = _load_yaml(ROOT / args.eval_config)
    prompt_config = _load_yaml(ROOT / args.prompt_config)
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = load_generation_bundle(args.model, None, 1.0)
    results = []
    raw_all = []
    for name, variant in prompt_config.get("variants", {}).items():
        for max_new_tokens in prompt_config.get("decoding", {}).get("max_new_tokens", [24]):
            result = evaluate_variant(bundle, eval_config, name, variant, int(max_new_tokens), args.per_task_limit)
            raw_all.extend(result.pop("raw_predictions"))
            results.append(result)
            print(json.dumps({"variant": name, "max_new_tokens": max_new_tokens, "extra": result["extra"], "aggregate": result["aggregate"]}, ensure_ascii=False), flush=True)
    results.sort(key=lambda row: (row["extra"]["SC"]["no_error_accuracy"] + row["extra"]["GC"]["no_error_accuracy"], row["aggregate"].get("overall_score", 0)), reverse=True)
    (output_dir / "prompt_sweep_summary.json").write_text(json.dumps({"model": args.model, "results": results}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (output_dir / "prompt_sweep_raw.jsonl").open("w", encoding="utf-8") as handle:
        for row in raw_all:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    lines = ["# Final Salvage SC/GC Prompt Sweep", "", "| Variant | max_new_tokens | SC no-error | GC no-error | SC det | SC corr | GC det | GC corr |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for row in results:
        sc = row["task_scores"]["SC"]
        gc = row["task_scores"]["GC"]
        lines.append(
            f"| {row['variant']} | {row['max_new_tokens']} | {row['extra']['SC']['no_error_accuracy']:.3f} | {row['extra']['GC']['no_error_accuracy']:.3f} | "
            f"{sc['detection_f1']:.3f} | {sc['correction_f1']:.3f} | {gc['detection_f1']:.3f} | {gc['correction_f1']:.3f} |"
        )
    (output_dir / "prompt_sweep_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output_dir / "prompt_sweep_summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
