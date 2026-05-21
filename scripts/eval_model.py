#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import aggregate_wmt_scores, exact_accuracy, mt_scores, scgc_scores


def resolve_model_name(model_name: str | None) -> str | None:
    if not model_name:
        return model_name
    path = Path(model_name)
    if path.is_absolute() and path.exists():
        return str(path)
    scratch_root = os.environ.get("SCRATCH_ROOT")
    if scratch_root and path.parts and path.parts[0] == "checkpoints":
        scratch_path = Path(scratch_root) / path
        if scratch_path.exists():
            return str(scratch_path)
    local_path = ROOT / path
    if local_path.exists():
        return str(local_path)
    return model_name


def read_jsonl(path: Path, limit: int | None = None) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
                if limit and len(rows) >= limit:
                    break
    return rows


def oracle_predictions(rows: list[dict]) -> list[str]:
    return [str(row.get("target", "")) for row in rows]


def generate_predictions(model_name: str, rows: list[dict], max_new_tokens: int) -> list[str]:
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:
        raise RuntimeError("Install torch and transformers for model evaluation, or use --oracle for smoke tests.") from exc
    model_name = resolve_model_name(model_name) or model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    outputs = []
    for row in rows:
        prompt_messages = [m for m in row["messages"] if m["role"] != "assistant"]
        try:
            prompt = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            prompt = "\n".join(f"{m['role']}: {m['content']}" for m in prompt_messages)
        encoded = tokenizer(prompt, return_tensors="pt").to(model.device)
        generated = model.generate(**encoded, max_new_tokens=max_new_tokens, do_sample=False)
        text = tokenizer.decode(generated[0][encoded["input_ids"].shape[-1] :], skip_special_tokens=True).strip()
        outputs.append(text)
    return outputs


def score_task(task: str, predictions: list[str], references: list[str]) -> dict[str, float]:
    if task == "MT":
        return mt_scores(predictions, references)
    if task in {"QA", "MR"}:
        return {"accuracy": exact_accuracy(predictions, references)}
    if task in {"SC", "GC"}:
        return scgc_scores(predictions, references)
    return {}


def append_eval_record(config_path: str, model_name: str | None, result: dict, output: str | None, limit: int | None) -> None:
    if os.environ.get("WMT26_RECORD_RUNS", "1") == "0":
        return
    aggregate = result.get("aggregate", {})
    task_scores = result.get("task_scores", {})
    record = {
        "eval_id": Path(output).stem if output else f"eval_{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "run_id": Path(str(model_name)).name if model_name else "unknown",
        "track": result.get("track"),
        "checkpoint_path": model_name,
        "config_path": config_path,
        "split": result.get("split", "locked_validation"),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "andromeda_job_id": os.environ.get("SLURM_JOB_ID"),
        "limit": limit,
        "MT_chrF": task_scores.get("MT", {}).get("chrf++"),
        "MT_BLEU": task_scores.get("MT", {}).get("bleu"),
        "QA_accuracy": task_scores.get("QA", {}).get("accuracy"),
        "SC_detection_F1": task_scores.get("SC", {}).get("detection_f1"),
        "SC_correction_F1": task_scores.get("SC", {}).get("correction_f1"),
        "GC_detection_F1": task_scores.get("GC", {}).get("detection_f1"),
        "GC_correction_F1": task_scores.get("GC", {}).get("correction_f1"),
        "MR_accuracy": task_scores.get("MR", {}).get("accuracy"),
        "MT_score": aggregate.get("MT_score"),
        "QA_score": aggregate.get("QA_score"),
        "SC_score": aggregate.get("SC_score"),
        "GC_score": aggregate.get("GC_score"),
        "MR_score": aggregate.get("MR_score"),
        "overall_equal_weighted_score": aggregate.get("overall_score"),
        "per_direction_scores": {},
        "notes": "oracle smoke evaluation" if result.get("oracle") else "",
    }
    out = ROOT / "results/eval_runs.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--oracle", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    model_name = args.model or config.get("model")
    max_new_tokens = int(config.get("max_new_tokens", 256))
    task_scores: dict[str, dict[str, float]] = {}
    for task, files in config.get("datasets", {}).items():
        rows: list[dict] = []
        for rel in files:
            rows.extend(read_jsonl(ROOT / rel, args.limit))
        if args.limit:
            rows = rows[: args.limit]
        if not rows:
            task_scores[task] = score_task(task, [], [])
            continue
        references = [str(row["target"]) for row in rows]
        predictions = oracle_predictions(rows) if args.oracle else generate_predictions(model_name, rows, max_new_tokens)
        task_scores[task] = score_task(task, predictions, references)
    result = {
        "track": config.get("track"),
        "split": config.get("split", "locked_validation"),
        "model": model_name,
        "oracle": args.oracle,
        "task_scores": task_scores,
        "aggregate": aggregate_wmt_scores(task_scores),
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        out = ROOT / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    append_eval_record(args.config, model_name, result, args.output, args.limit)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
