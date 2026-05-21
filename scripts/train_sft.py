#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.train.config import load_yaml


def resolve_output_dir(rel: str) -> Path:
    path = Path(rel)
    if path.is_absolute():
        return path
    scratch_root = os.environ.get("SCRATCH_ROOT")
    if scratch_root and path.parts and path.parts[0] == "checkpoints":
        return Path(scratch_root) / path
    return ROOT / path


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


def revision() -> str:
    git_rev = os.popen("git rev-parse HEAD 2>/dev/null").read().strip()
    if git_rev:
        return git_rev
    rev_file = ROOT / "REVISION"
    if rev_file.exists():
        return rev_file.read_text(encoding="utf-8").strip()
    return "unknown"


def append_training_record(config: dict, config_path: str, status: str, checkpoint_path: Path | None, num_examples: int, notes: str = "") -> None:
    if os.environ.get("WMT26_RECORD_RUNS", "1") == "0":
        return
    checkpoint_str = None
    if checkpoint_path:
        try:
            checkpoint_str = str(checkpoint_path.relative_to(ROOT))
        except ValueError:
            checkpoint_str = str(checkpoint_path)
    record = {
        "run_id": config.get("run_name"),
        "track": config.get("track"),
        "model_type": config.get("specialist") or config.get("method"),
        "base_checkpoint": config.get("base_model_path") or config.get("model_config"),
        "config_path": config_path,
        "data_mixture_id": config.get("mixture_config") or config.get("sampling") or "direct_files",
        "seed": config.get("seed"),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": revision(),
        "andromeda_job_id": os.environ.get("SLURM_JOB_ID"),
        "gpu_type": os.environ.get("SLURM_JOB_GPUS") or os.environ.get("CUDA_VISIBLE_DEVICES"),
        "train_steps": config.get("max_steps"),
        "epochs": config.get("num_train_epochs"),
        "effective_batch_size": int(config.get("batch_size", 1)) * int(config.get("gradient_accumulation_steps", 1)),
        "learning_rate": config.get("learning_rate"),
        "lora_config": {
            "adapter": config.get("adapter"),
            "r": config.get("lora_r"),
            "alpha": config.get("lora_alpha"),
            "dropout": config.get("lora_dropout"),
            "target_modules": config.get("target_modules"),
        },
        "precision": config.get("precision") or "bf16_if_cuda",
        "checkpoint_path": checkpoint_str,
        "log_path": f"/home/{os.environ.get('USER', '%u')}/logs/{os.environ.get('SLURM_JOB_NAME', 'local')}-{os.environ.get('SLURM_JOB_ID', 'local')}.out",
        "status": status,
        "num_examples_seen": num_examples,
        "notes": notes,
    }
    out = ROOT / "results/training_runs.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def dry_run(config: dict, examples: list[dict], reason: str) -> None:
    output_dir = resolve_output_dir(config.get("output_dir", "checkpoints/dry_run"))
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = {
        "run_name": config.get("run_name"),
        "track": config.get("track"),
        "method": config.get("method"),
        "adapter": config.get("adapter"),
        "num_examples_seen": len(examples),
        "reason": reason,
        "git_commit": revision(),
    }
    (output_dir / "DRY_RUN.json").write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "dummy_state.pt").write_text("dry-run placeholder; not a real checkpoint\n", encoding="utf-8")
    print(f"Dry-run complete: {output_dir}")
    return output_dir


def skipped_run(config: dict, reason: str) -> None:
    output_dir = resolve_output_dir(config.get("output_dir", "checkpoints/skipped"))
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = {
        "run_name": config.get("run_name"),
        "track": config.get("track"),
        "method": config.get("method"),
        "adapter": config.get("adapter"),
        "status": "skipped",
        "reason": reason,
        "git_commit": revision(),
    }
    (output_dir / "SKIPPED.json").write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Skipped training: {output_dir} ({reason})")
    return output_dir


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
        from torch.utils.data import DataLoader, Dataset
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

    max_length = int(config.get("max_length", 2048))

    class JsonlTextDataset(Dataset):
        def __init__(self, rows: list[dict]) -> None:
            self.rows = rows

        def __len__(self) -> int:
            return len(self.rows)

        def __getitem__(self, idx: int) -> dict:
            text = example_to_text(tokenizer, self.rows[idx])
            return tokenizer(text, truncation=True, max_length=max_length)

    def collate(batch: list[dict]) -> dict:
        padded = tokenizer.pad(batch, padding=True, return_tensors="pt")
        labels = padded["input_ids"].clone()
        labels[padded["attention_mask"] == 0] = -100
        padded["labels"] = labels
        return padded

    dataset = JsonlTextDataset(examples)
    loader = DataLoader(dataset, batch_size=int(config.get("batch_size", 1)), shuffle=True, collate_fn=collate)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(config.get("learning_rate", 2e-4)))
    max_steps = int(config.get("max_steps", 10))
    grad_accum = int(config.get("gradient_accumulation_steps", 1))
    model.train()
    step = 0
    optimizer.zero_grad()
    while step < max_steps:
        for batch in loader:
            device = next(model.parameters()).device
            out = model(
                input_ids=batch["input_ids"].to(device),
                attention_mask=batch["attention_mask"].to(device),
                labels=batch["labels"].to(device),
            )
            (out.loss / grad_accum).backward()
            if (step + 1) % grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()
            step += 1
            if step >= max_steps:
                break
    output_dir = resolve_output_dir(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    if config.get("adapter", "none") == "lora" and hasattr(model, "merge_and_unload"):
        adapter_dir = output_dir / "adapter"
        adapter_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(adapter_dir)
        model = model.merge_and_unload()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved checkpoint to {output_dir}")
    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    config = load_yaml(ROOT / args.config)
    max_examples = args.max_examples if args.max_examples is not None else config.get("max_examples")
    examples: list[dict] = []
    try:
        examples = collect_examples(config.get("train_files", []), max_examples)
        if not examples and config.get("allow_empty_train", False):
            out = skipped_run(config, "no training examples; waiting for registered external/public data")
            append_training_record(config, args.config, "skipped", out, len(examples), "no training examples")
            return 0
        if args.dry_run or config.get("dry_run", False):
            out = dry_run(config, examples, "explicit dry_run")
            append_training_record(config, args.config, "dry_run", out, len(examples), "explicit dry_run")
            return 0
        out = real_train(config, examples, max_examples)
        append_training_record(config, args.config, "completed", out, len(examples))
    except Exception as exc:
        append_training_record(config, args.config, "failed", None, len(examples), f"{exc}\n{traceback.format_exc(limit=8)}")
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
