#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.train.config import load_yaml


def read_jsonl(path: Path, limit: int | None = None) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
                if limit and len(rows) >= limit:
                    break
    return rows


def collect_examples(files: list[str], max_examples: int | None = None) -> list[dict]:
    rows: list[dict] = []
    for rel in files:
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(f"Missing train file: {path}")
        remaining = None if max_examples is None else max_examples - len(rows)
        if remaining is not None and remaining <= 0:
            break
        rows.extend(read_jsonl(path, remaining))
    return rows


def dry_run(config: dict, examples: list[dict], reason: str) -> None:
    output_dir = ROOT / config.get("output_dir", "checkpoints/dry_run")
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = {
        "run_name": config.get("run_name"),
        "track": config.get("track"),
        "method": config.get("method"),
        "adapter": config.get("adapter"),
        "num_examples_seen": len(examples),
        "reason": reason,
        "git_commit": os.popen("git rev-parse HEAD 2>/dev/null").read().strip(),
    }
    (output_dir / "DRY_RUN.json").write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "dummy_state.pt").write_text("dry-run placeholder; not a real checkpoint\n", encoding="utf-8")
    print(f"Dry-run complete: {output_dir}")


def skipped_run(config: dict, reason: str) -> None:
    output_dir = ROOT / config.get("output_dir", "checkpoints/skipped")
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = {
        "run_name": config.get("run_name"),
        "track": config.get("track"),
        "method": config.get("method"),
        "adapter": config.get("adapter"),
        "status": "skipped",
        "reason": reason,
        "git_commit": os.popen("git rev-parse HEAD 2>/dev/null").read().strip(),
    }
    (output_dir / "SKIPPED.json").write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Skipped training: {output_dir} ({reason})")


def example_to_text(tokenizer, row: dict) -> str:
    if "messages" in row and row["messages"]:
        try:
            return tokenizer.apply_chat_template(row["messages"], tokenize=False)
        except Exception:
            return "\n".join(f"{m['role']}: {m['content']}" for m in row["messages"])
    if "chosen" in row:
        prompt = "\n".join(m["content"] for m in row.get("messages", []))
        return f"{prompt}\n{row['chosen']}"
    return f"{row.get('input', '')}\n{row.get('target', '')}"


def real_train(config: dict, examples: list[dict], max_examples: int | None) -> None:
    try:
        import torch
        from torch.utils.data import DataLoader
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:
        raise RuntimeError("Install torch and transformers for real training. Use --dry-run for smoke tests.") from exc

    if not examples:
        raise ValueError("No training examples available for real training.")
    model_cfg = load_yaml(ROOT / config.get("model_config", "configs/model/qwen35_2b.yaml"))
    model_name = config.get("base_model_path") or model_cfg["model_name_or_path"]
    if config.get("base_model_path") and not (ROOT / str(config["base_model_path"])).exists():
        if config.get("fallback_to_base_if_missing", False):
            print(f"WARNING: {config['base_model_path']} missing; falling back to {model_cfg['model_name_or_path']}")
            model_name = model_cfg["model_name_or_path"]
        else:
            raise FileNotFoundError(f"Missing base_model_path: {config['base_model_path']}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=model_cfg.get("trust_remote_code", True))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=model_cfg.get("trust_remote_code", True),
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    try:
        from peft import LoraConfig, get_peft_model

        if config.get("adapter", "none") == "lora":
            lora = LoraConfig(
                r=int(config.get("lora_r", 16)),
                lora_alpha=int(config.get("lora_alpha", 32)),
                lora_dropout=float(config.get("lora_dropout", 0.05)),
                target_modules=config.get("target_modules", ["q_proj", "k_proj", "v_proj", "o_proj"]),
                task_type="CAUSAL_LM",
            )
            model = get_peft_model(model, lora)
    except Exception:
        if config.get("adapter", "none") == "lora":
            raise RuntimeError("PEFT is required for LoRA training.")

    texts = [example_to_text(tokenizer, row) for row in examples]
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=int(config.get("max_length", 2048)), return_tensors="pt")
    labels = encoded["input_ids"].clone()
    dataset = list(zip(encoded["input_ids"], encoded["attention_mask"], labels))
    loader = DataLoader(dataset, batch_size=int(config.get("batch_size", 1)), shuffle=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(config.get("learning_rate", 2e-4)))
    max_steps = int(config.get("max_steps", 10))
    grad_accum = int(config.get("gradient_accumulation_steps", 1))
    model.train()
    step = 0
    optimizer.zero_grad()
    while step < max_steps:
        for input_ids, attention_mask, labels in loader:
            device = next(model.parameters()).device
            out = model(input_ids=input_ids.to(device), attention_mask=attention_mask.to(device), labels=labels.to(device))
            (out.loss / grad_accum).backward()
            if (step + 1) % grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()
            step += 1
            if step >= max_steps:
                break
    output_dir = ROOT / config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved checkpoint to {output_dir}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    config = load_yaml(ROOT / args.config)
    max_examples = args.max_examples if args.max_examples is not None else config.get("max_examples")
    examples = collect_examples(config.get("train_files", []), max_examples)
    if not examples and config.get("allow_empty_train", False):
        skipped_run(config, "no training examples; waiting for registered external/public data")
        return 0
    if args.dry_run or config.get("dry_run", False):
        dry_run(config, examples, "explicit dry_run")
        return 0
    real_train(config, examples, max_examples)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
