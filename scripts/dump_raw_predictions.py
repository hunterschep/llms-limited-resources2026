#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_model import generate_predictions, load_generation_bundle, read_jsonl, row_to_prompt, score_task
from wmt26.eval.metrics import (
    normalize_choice_answer,
    normalize_mr_answer,
    parse_edit_output,
    scgc_diagnostics,
)


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")[:120] or "model"


def fallback_prompt(row: dict) -> str:
    messages = [m for m in row.get("messages", []) if m.get("role") != "assistant"]
    if messages:
        return "\n".join(f"{m.get('role')}: {m.get('content')}" for m in messages)
    return str(row.get("input", ""))


def parse_for_task(task: str, prediction: str, reference: str) -> dict:
    if task in {"SC", "GC"}:
        pred_wrong, pred_correct = parse_edit_output(prediction)
        ref_wrong, ref_correct = parse_edit_output(reference)
        return {
            "parsed_prediction": {"wrong_word": pred_wrong, "correct_word": pred_correct},
            "parsed_reference": {"wrong_word": ref_wrong, "correct_word": ref_correct},
            "detection_correct": (pred_wrong != "CORRECT") == (ref_wrong != "CORRECT"),
            "correction_correct": pred_wrong == ref_wrong and pred_correct == ref_correct and ref_wrong != "CORRECT",
        }
    if task == "QA":
        pred = normalize_choice_answer(prediction)
        ref = normalize_choice_answer(reference)
        return {"normalized_prediction": pred, "normalized_reference": ref, "correct": pred == ref}
    if task == "MR":
        pred = normalize_mr_answer(prediction)
        ref = normalize_mr_answer(reference)
        return {"normalized_prediction": pred, "normalized_reference": ref, "correct": pred == ref}
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Dump prompts, gold targets, raw generations, parsed predictions, and per-example decisions.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--tasks", nargs="*", default=None)
    parser.add_argument("--per-task", type=int, default=20)
    parser.add_argument("--output", default=None)
    parser.add_argument("--oracle", action="store_true", help="Use gold targets as predictions; useful for parser debugging without a model.")
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    model_name = args.model or config.get("model")
    tasks = args.tasks or list(config.get("datasets", {}).keys())
    max_new_tokens = int(args.max_new_tokens or config.get("max_new_tokens", 256))
    batch_size = int(args.batch_size or config.get("batch_size", config.get("eval_batch_size", 4)))
    bundle = None if args.oracle else load_generation_bundle(model_name)

    output = ROOT / (args.output or f"results/triage/raw_predictions/{config.get('track', 'track')}_{safe_name(str(model_name or 'oracle'))}.jsonl")
    output.parent.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict] = {}
    with output.open("w", encoding="utf-8") as handle:
        for task in tasks:
            rows: list[dict] = []
            for rel in config.get("datasets", {}).get(task, []):
                rows.extend(read_jsonl(ROOT / rel, args.per_task))
            rows = rows[: args.per_task]
            references = [str(row.get("target", "")) for row in rows]
            predictions = references[:] if args.oracle else generate_predictions(bundle, rows, max_new_tokens, batch_size, task=task)
            task_scores = score_task(task, predictions, references)
            task_summary: dict = {"rows": len(rows), "scores": task_scores}
            if task in {"SC", "GC"}:
                task_summary["diagnostics"] = scgc_diagnostics(predictions, references)
            summary[task] = task_summary
            tokenizer = bundle[0] if bundle else None
            for row, prediction, reference in zip(rows, predictions, references):
                prompt = row_to_prompt(tokenizer, row) if tokenizer else fallback_prompt(row)
                record = {
                    "task": task,
                    "id": row.get("id"),
                    "track": row.get("track") or config.get("track"),
                    "language": row.get("language"),
                    "source_id": row.get("source_id"),
                    "prompt": prompt,
                    "gold_target": reference,
                    "raw_prediction": prediction,
                }
                record.update(parse_for_task(task, prediction, reference))
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    sidecar = output.with_suffix(output.suffix + ".summary.json")
    sidecar.write_text(json.dumps({"output": str(output), "model": model_name, "summary": summary}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "summary": summary}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
