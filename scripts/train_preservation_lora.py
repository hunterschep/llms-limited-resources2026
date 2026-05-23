#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from phase4_common import git_revision, read_jsonl, read_yaml
from wmt26.train.preservation import assistant_only_labels, kl_to_base_loss


def resolve_output_dir(rel: str) -> Path:
    path = Path(rel)
    if path.is_absolute():
        return path
    scratch_root = os.environ.get("SCRATCH_ROOT")
    if scratch_root and path.parts and path.parts[0] == "checkpoints":
        return Path(scratch_root) / path
    return ROOT / path


def collect_examples(config: dict, max_examples: int | None = None) -> list[dict]:
    rng = random.Random(int(config.get("seed", 2606)))
    rows: list[dict] = []
    for rel in config.get("train_files", []):
        rows.extend(read_jsonl(ROOT / rel))
    replay_files = config.get("replay_files", []) or []
    replay_rows: list[dict] = []
    for rel in replay_files:
        replay_rows.extend(read_jsonl(ROOT / rel))
    if replay_rows:
        rng.shuffle(replay_rows)
        replay_cap = int(config.get("replay_max_examples", max(1, len(rows) // 4)))
        rows.extend(replay_rows[:replay_cap])
    rng.shuffle(rows)
    if max_examples:
        rows = rows[:max_examples]
    return rows


def append_record(config_path: str, config: dict, status: str, output_dir: Path | None, num_examples: int, notes: str = "") -> None:
    if os.environ.get("WMT26_RECORD_RUNS", "1") == "0":
        return
    record = {
        "run_id": config.get("run_name"),
        "track": config.get("track"),
        "model_type": config.get("specialist") or config.get("method"),
        "base_checkpoint": config.get("base_model_path") or config.get("model_config"),
        "config_path": config_path,
        "data_mixture_id": config.get("phase4_strategy", "preservation_lora"),
        "seed": config.get("seed"),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": git_revision(),
        "andromeda_job_id": os.environ.get("SLURM_JOB_ID"),
        "gpu_type": os.environ.get("SLURM_JOB_GPUS") or os.environ.get("CUDA_VISIBLE_DEVICES"),
        "train_steps": config.get("max_steps"),
        "effective_batch_size": int(config.get("batch_size", 1)) * int(config.get("gradient_accumulation_steps", 1)),
        "learning_rate": config.get("learning_rate"),
        "lora_config": {
            "adapter": config.get("adapter"),
            "r": config.get("lora_r"),
            "alpha": config.get("lora_alpha"),
            "dropout": config.get("lora_dropout"),
            "target_modules": config.get("target_modules"),
        },
        "checkpoint_path": str(output_dir) if output_dir else None,
        "status": status,
        "num_examples_seen": num_examples,
        "notes": notes,
    }
    out = ROOT / "results/training_runs.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def dry_run(config: dict, examples: list[dict]) -> Path:
    output_dir = resolve_output_dir(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = {
        "status": "dry_run",
        "run_name": config.get("run_name"),
        "num_examples_seen": len(examples),
        "preservation": {
            "assistant_only_loss": True,
            "kl_to_base_weight": config.get("kl_to_base_weight", 0.0),
            "replay_files": config.get("replay_files", []),
            "low_rank_lora": config.get("lora_r"),
        },
        "git_commit": git_revision(),
    }
    (output_dir / "DRY_RUN.json").write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_dir


def real_train(config: dict, examples: list[dict]) -> Path:
    import torch
    from torch.utils.data import DataLoader, Dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer

    try:
        from peft import LoraConfig, get_peft_model
    except Exception as exc:
        raise RuntimeError("PEFT is required for Phase 4 preservation LoRA training.") from exc

    model_cfg = read_yaml(ROOT / config.get("model_config", "configs/model/qwen35_2b.yaml"))
    model_name = config.get("base_model_path") or model_cfg["model_name_or_path"]
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=model_cfg.get("trust_remote_code", True))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else (torch.float16 if torch.cuda.is_available() else torch.float32)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=dtype, device_map="auto" if torch.cuda.is_available() else None)
    lora = LoraConfig(
        r=int(config.get("lora_r", 4)),
        lora_alpha=int(config.get("lora_alpha", 8)),
        lora_dropout=float(config.get("lora_dropout", 0.05)),
        target_modules=config.get("target_modules", ["q_proj", "v_proj"]),
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)
    base_model = None
    kl_weight = float(config.get("kl_to_base_weight", 0.0))
    if kl_weight > 0:
        base_model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=dtype, device_map="auto" if torch.cuda.is_available() else None)
        base_model.eval()
        for param in base_model.parameters():
            param.requires_grad_(False)
    max_length = int(config.get("max_length", 1024))

    class ChatDataset(Dataset):
        def __len__(self) -> int:
            return len(examples)

        def __getitem__(self, idx: int) -> dict:
            return assistant_only_labels(tokenizer, examples[idx]["messages"], max_length=max_length)

    def collate(batch: list[dict]) -> dict:
        input_ids = torch.nn.utils.rnn.pad_sequence([item["input_ids"] for item in batch], batch_first=True, padding_value=tokenizer.pad_token_id)
        attention_mask = torch.nn.utils.rnn.pad_sequence([item["attention_mask"] for item in batch], batch_first=True, padding_value=0)
        labels = torch.nn.utils.rnn.pad_sequence([item["labels"] for item in batch], batch_first=True, padding_value=-100)
        return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

    loader = DataLoader(ChatDataset(), batch_size=int(config.get("batch_size", 1)), shuffle=True, collate_fn=collate)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(config.get("learning_rate", 1e-5)), weight_decay=float(config.get("weight_decay", 0.0)))
    max_steps = int(config.get("max_steps", 20))
    grad_accum = int(config.get("gradient_accumulation_steps", 1))
    model.train()
    step = 0
    optimizer.zero_grad()
    while step < max_steps:
        for batch in loader:
            device = next(model.parameters()).device
            batch = {key: value.to(device) for key, value in batch.items()}
            out = model(**batch)
            loss = out.loss
            if base_model is not None:
                with torch.inference_mode():
                    base_out = base_model(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"])
                loss = loss + kl_weight * kl_to_base_loss(out.logits, base_out.logits.to(out.logits.device), batch["attention_mask"])
            (loss / grad_accum).backward()
            if (step + 1) % grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()
            step += 1
            if step == 1 or step % int(config.get("log_every", 10)) == 0 or step >= max_steps:
                print(f"train_step={step}/{max_steps} loss={float(loss.detach().cpu()):.4f}", flush=True)
            if step >= max_steps:
                break
    output_dir = resolve_output_dir(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    adapter_dir = output_dir / "adapter"
    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(output_dir)
    if config.get("save_merged", False) and hasattr(model, "merge_and_unload"):
        merged = model.merge_and_unload()
        merged.save_pretrained(output_dir / "merged")
    (output_dir / "PHASE4_METADATA.json").write_text(json.dumps({"config": config, "git_commit": git_revision()}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    config = read_yaml(ROOT / args.config)
    examples: list[dict] = []
    try:
        examples = collect_examples(config, args.max_examples or config.get("max_examples"))
        if args.dry_run or config.get("dry_run", False):
            out = dry_run(config, examples)
            append_record(args.config, config, "dry_run", out, len(examples), "phase4 dry-run")
            print(f"Dry-run complete: {out}")
            return 0
        out = real_train(config, examples)
        append_record(args.config, config, "completed", out, len(examples), "phase4 preservation training")
    except Exception as exc:
        append_record(args.config, config, "failed", None, len(examples), f"{exc}\n{traceback.format_exc(limit=8)}")
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
