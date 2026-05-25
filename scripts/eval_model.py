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

from wmt26.eval.metrics import aggregate_wmt_scores, mt_scores, normalized_accuracy, scgc_scores
from wmt26.train.preservation import scale_lora_adapters


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


def load_generation_bundle(model_name: str, adapter_name: str | None = None, adapter_scale: float = 1.0):
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:
        raise RuntimeError("Install torch and transformers for model evaluation, or use --oracle for smoke tests.") from exc
    model_name = resolve_model_name(model_name) or model_name
    adapter_path = resolve_model_name(adapter_name) if adapter_name else None
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    if torch.cuda.is_available():
        try:
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        except Exception:
            dtype = torch.float16
    else:
        dtype = torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=dtype,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    if adapter_path:
        try:
            from peft import PeftModel
        except Exception as exc:
            raise RuntimeError("PEFT is required to evaluate LoRA adapters.") from exc
        model = PeftModel.from_pretrained(model, adapter_path)
        scale_lora_adapters(model, adapter_scale)
    model.eval()
    return tokenizer, model


def row_to_prompt(tokenizer, row: dict) -> str:
    prompt_messages = [m for m in row["messages"] if m["role"] != "assistant"]
    try:
        return tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
    except Exception:
        return "\n".join(f"{m['role']}: {m['content']}" for m in prompt_messages)


def generate_predictions(bundle, rows: list[dict], max_new_tokens: int, batch_size: int, task: str | None = None) -> list[str]:
    import torch

    tokenizer, model = bundle
    outputs = []
    prompts = [row_to_prompt(tokenizer, row) for row in rows]
    batch_size = max(1, int(batch_size))
    total_batches = (len(prompts) + batch_size - 1) // batch_size
    for start in range(0, len(prompts), batch_size):
        batch_prompts = prompts[start : start + batch_size]
        batch_index = start // batch_size + 1
        label = f" task={task}" if task else ""
        print(f"eval_batch{label} batch={batch_index}/{total_batches} rows={len(batch_prompts)}", flush=True)
        encoded = tokenizer(batch_prompts, return_tensors="pt", padding=True).to(model.device)
        with torch.inference_mode():
            generated = model.generate(
                **encoded,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
            )
        prompt_width = encoded["input_ids"].shape[-1]
        decoded = tokenizer.batch_decode(generated[:, prompt_width:], skip_special_tokens=True)
        outputs.extend(text.strip() for text in decoded)
    return outputs


def score_task(task: str, predictions: list[str], references: list[str]) -> dict[str, float]:
    if task == "MT":
        return mt_scores(predictions, references)
    if task in {"QA", "MR"}:
        return {"accuracy": normalized_accuracy(predictions, references, task)}
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
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--adapter-scale", type=float, default=1.0)
    parser.add_argument("--oracle", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    model_name = args.model or config.get("model")
    max_new_tokens = int(config.get("max_new_tokens", 256))
    batch_size = int(config.get("batch_size", config.get("eval_batch_size", 4)))
    task_scores: dict[str, dict[str, float]] = {}
    generation_bundle = None if args.oracle else load_generation_bundle(model_name, args.adapter, args.adapter_scale)
    for task, files in config.get("datasets", {}).items():
        rows: list[dict] = []
        for rel in files:
            rows.extend(read_jsonl(ROOT / rel, args.limit))
        if args.limit:
            rows = rows[: args.limit]
        print(f"eval_task_start task={task} rows={len(rows)} oracle={args.oracle}", flush=True)
        if not rows:
            task_scores[task] = score_task(task, [], [])
            print(f"eval_task_done task={task} empty=true scores={task_scores[task]}", flush=True)
            continue
        references = [str(row["target"]) for row in rows]
        predictions = oracle_predictions(rows) if args.oracle else generate_predictions(generation_bundle, rows, max_new_tokens, batch_size, task=task)
        task_scores[task] = score_task(task, predictions, references)
        print(f"eval_task_done task={task} scores={json.dumps(task_scores[task], sort_keys=True)}", flush=True)
    result = {
        "track": config.get("track"),
        "split": config.get("split", "locked_validation"),
        "model": model_name,
        "adapter": args.adapter,
        "adapter_scale": args.adapter_scale if args.adapter else None,
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
