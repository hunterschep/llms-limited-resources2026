#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from train_sft import append_training_record, collect_examples, dry_run, resolve_output_dir  # noqa: E402
from wmt26.train.config import load_yaml  # noqa: E402
from wmt26.train.preservation import assistant_only_labels  # noqa: E402


def _resolve_model(path: str) -> str:
    p = Path(path)
    if p.exists() or p.is_absolute():
        return str(p)
    scratch = os.environ.get("SCRATCH_ROOT")
    if scratch and p.parts and p.parts[0] == "checkpoints":
        sp = Path(scratch) / p
        if sp.exists():
            return str(sp)
    return str(ROOT / p)


def real_train(config_path: Path, config: dict, examples: list[dict]) -> Path:
    try:
        import torch
        from torch.utils.data import DataLoader, Dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import LoraConfig, get_peft_model
    except Exception as exc:
        raise RuntimeError("Install torch, transformers, and peft for final salvage calibration.") from exc

    if not examples:
        raise ValueError("No calibration examples available.")
    model_cfg = load_yaml(ROOT / config.get("model_config", "configs/model/qwen35_2b.yaml"))
    model_name = _resolve_model(str(config["base_model_path"]))
    output_root = resolve_output_dir(str(config["output_dir"]))
    final_adapter = output_root / "final_adapter"
    final_merged = output_root / "final_merged"
    output_root.mkdir(parents=True, exist_ok=True)
    seed = int(config.get("seed", 2712))
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=model_cfg.get("trust_remote_code", True))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else (torch.float16 if torch.cuda.is_available() else torch.float32)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=dtype, device_map="auto" if torch.cuda.is_available() else None)
    lora = LoraConfig(
        r=int(config.get("lora_r", 8)),
        lora_alpha=int(config.get("lora_alpha", 16)),
        lora_dropout=float(config.get("lora_dropout", 0.05)),
        target_modules=config.get("target_modules", ["q_proj", "v_proj", "o_proj"]),
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)
    max_length = int(config.get("max_length", 1536))

    class CalibrationDataset(Dataset):
        def __init__(self, rows: list[dict]) -> None:
            self.rows = rows

        def __len__(self) -> int:
            return len(self.rows)

        def __getitem__(self, idx: int) -> dict:
            row = self.rows[idx]
            if row.get("messages"):
                messages = row["messages"]
            else:
                messages = [
                    {"role": "user", "content": str(row.get("input", ""))},
                    {"role": "assistant", "content": str(row.get("target", ""))},
                ]
            return assistant_only_labels(tokenizer, messages, max_length)

    def collate(batch: list[dict]) -> dict:
        max_len = max(item["input_ids"].numel() for item in batch)
        input_ids = []
        attention = []
        labels = []
        pad_id = tokenizer.pad_token_id
        for item in batch:
            pad = max_len - item["input_ids"].numel()
            input_ids.append(torch.cat([torch.full((pad,), pad_id, dtype=torch.long), item["input_ids"]]))
            attention.append(torch.cat([torch.zeros(pad, dtype=torch.long), item["attention_mask"]]))
            labels.append(torch.cat([torch.full((pad,), -100, dtype=torch.long), item["labels"]]))
        return {"input_ids": torch.stack(input_ids), "attention_mask": torch.stack(attention), "labels": torch.stack(labels)}

    rng = random.Random(seed)
    rng.shuffle(examples)
    loader = DataLoader(CalibrationDataset(examples), batch_size=int(config.get("batch_size", 1)), shuffle=True, collate_fn=collate)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(config.get("learning_rate", 3e-6)))
    max_steps = int(config.get("max_steps", 260))
    grad_accum = int(config.get("gradient_accumulation_steps", 16))
    model.train()
    step = 0
    optimizer.zero_grad()
    while step < max_steps:
        for batch in loader:
            device = next(model.parameters()).device
            out = model(input_ids=batch["input_ids"].to(device), attention_mask=batch["attention_mask"].to(device), labels=batch["labels"].to(device))
            (out.loss / grad_accum).backward()
            if (step + 1) % grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()
            step += 1
            if step == 1 or step % 25 == 0 or step >= max_steps:
                print(f"final_salvage_calibration_step={step}/{max_steps} loss={float(out.loss.detach().cpu()):.4f}", flush=True)
            if step >= max_steps:
                break
    final_adapter.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(final_adapter)
    tokenizer.save_pretrained(final_adapter)
    merged = model.merge_and_unload()
    final_merged.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(final_merged)
    tokenizer.save_pretrained(final_merged)
    manifest = {
        "config_path": str(config_path.relative_to(ROOT)),
        "base_model_path": model_name,
        "output_dir": str(output_root),
        "final_adapter": str(final_adapter),
        "final_merged": str(final_merged),
        "num_examples": len(examples),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
    }
    (output_root / "final_salvage_calibration_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return final_merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/train/final_salvage/scgc_calibration_tiny.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    if not (ROOT / "data/processed/final_salvage/sorbian/scgc_calibration/clean_70_error_30.jsonl").exists():
        import subprocess

        subprocess.run([sys.executable, "scripts/build_final_scgc_calibration_data.py"], cwd=ROOT, check=True)
    config_path = ROOT / args.config
    config = load_yaml(config_path)
    examples = collect_examples(config.get("train_files", []), args.max_examples, config)
    if args.dry_run or config.get("dry_run", False):
        out = dry_run(config, examples, "final salvage calibration dry run")
        append_training_record(config, args.config, "dry_run", out, len(examples), "final salvage calibration")
        return 0
    out = real_train(config_path, config, examples)
    append_training_record(config, args.config, "completed", out, len(examples), "final salvage calibration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
