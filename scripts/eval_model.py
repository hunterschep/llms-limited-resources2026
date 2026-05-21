#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import aggregate_wmt_scores, exact_accuracy, mt_scores, scgc_scores


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
    result = {"task_scores": task_scores, "aggregate": aggregate_wmt_scores(task_scores)}
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        out = ROOT / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
