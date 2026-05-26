#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from lineage_common import git_commit, refuse_bad_reference, resolve_local_or_scratch, sha256_path, write_json  # noqa: E402
from train_sft import append_training_record, collect_examples, dry_run, example_to_text  # noqa: E402
from wmt26.train.config import load_yaml  # noqa: E402


def _model_name(config: dict, model_cfg: dict) -> str:
    model_name = str(model_cfg["model_name_or_path"])
    if config.get("base_model_path"):
        base = resolve_local_or_scratch(str(config["base_model_path"]))
        if base.exists():
            return str(base)
        if config.get("fallback_to_base_if_missing", False):
            print(f"WARNING: missing base_model_path={base}; falling back to {model_name}", flush=True)
            return model_name
        raise FileNotFoundError(f"Missing lineage base_model_path: {base}")
    return model_name


def _save_adapter(model, tokenizer, path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(path)
    tokenizer.save_pretrained(path)


def _manifest_for_config(config_path: Path, config: dict, examples: list[dict], output_root: Path, adapter_root: Path) -> dict:
    files = []
    for rel in config.get("train_files", []) or []:
        path = ROOT / rel
        files.append(
            {
                "path": rel,
                "exists": path.exists(),
                "bytes": path.stat().st_size if path.exists() else 0,
                "sha256": sha256_path(path) if path.exists() else None,
            }
        )
    return {
        "run_name": config.get("run_name"),
        "track": config.get("track"),
        "stage": config.get("stage"),
        "config_path": str(config_path.relative_to(ROOT)),
        "config_sha256": sha256_path(config_path),
        "git_commit": git_commit(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "base_model_path": config.get("base_model_path") or config.get("model_config"),
        "output_root": str(output_root),
        "adapter_root": str(adapter_root),
        "final_adapter": str(adapter_root / "final_adapter"),
        "final_merged": str(output_root / "final_merged"),
        "save_milestones": config.get("save_milestones", []),
        "num_examples": len(examples),
        "train_files": files,
        "policy": config.get("lineage_policy", {}),
    }


def real_train(config_path: Path, config: dict, examples: list[dict]) -> Path:
    try:
        import torch
        from torch.utils.data import DataLoader, Dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import LoraConfig, get_peft_model
    except Exception as exc:  # pragma: no cover - exercised on Andromeda
        raise RuntimeError("Install torch, transformers, and peft for lineage training.") from exc

    serialized_config = json.dumps(config, sort_keys=True)
    refuse_bad_reference(serialized_config)
    if not examples:
        raise ValueError("No training examples available for lineage training.")

    model_cfg = load_yaml(ROOT / config.get("model_config", "configs/model/qwen35_2b.yaml"))
    model_name = _model_name(config, model_cfg)
    output_root = resolve_local_or_scratch(str(config["output_dir"]))
    adapter_root = resolve_local_or_scratch(str(config.get("adapter_output_dir", config["output_dir"])))
    final_adapter = adapter_root / "final_adapter"
    final_merged = output_root / "final_merged"
    output_root.mkdir(parents=True, exist_ok=True)
    adapter_root.mkdir(parents=True, exist_ok=True)

    seed = int(config.get("seed", 2606))
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=model_cfg.get("trust_remote_code", True))
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    if torch.cuda.is_available():
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    else:
        dtype = torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=model_cfg.get("trust_remote_code", True),
        torch_dtype=dtype,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    if config.get("adapter", "none") == "lora":
        lora = LoraConfig(
            r=int(config.get("lora_r", 16)),
            lora_alpha=int(config.get("lora_alpha", 32)),
            lora_dropout=float(config.get("lora_dropout", 0.05)),
            target_modules=config.get("target_modules", ["q_proj", "k_proj", "v_proj", "o_proj"]),
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, lora)
    else:
        raise ValueError("Lineage recovery expects LoRA adapters so deltas can be preserved.")

    max_length = int(config.get("max_length", 2048))

    class JsonlTextDataset(Dataset):
        def __init__(self, rows: list[dict]) -> None:
            self.rows = rows

        def __len__(self) -> int:
            return len(self.rows)

        def __getitem__(self, idx: int) -> dict:
            return tokenizer(example_to_text(tokenizer, self.rows[idx]), truncation=True, max_length=max_length)

    def collate(batch: list[dict]) -> dict:
        padded = tokenizer.pad(batch, padding=True, return_tensors="pt")
        labels = padded["input_ids"].clone()
        labels[padded["attention_mask"] == 0] = -100
        padded["labels"] = labels
        return padded

    rng = random.Random(seed)
    rng.shuffle(examples)
    dataset = JsonlTextDataset(examples)
    loader = DataLoader(dataset, batch_size=int(config.get("batch_size", 1)), shuffle=True, collate_fn=collate)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(config.get("learning_rate", 2e-4)))
    max_steps = int(config.get("max_steps", 10))
    grad_accum = int(config.get("gradient_accumulation_steps", 1))
    log_every = int(config.get("log_every", 25))
    milestones = {int(step) for step in config.get("save_milestones", []) or []}
    manifest = _manifest_for_config(config_path, config, examples, output_root, adapter_root)
    write_json(output_root / "lineage_manifest.json", manifest)
    write_json(adapter_root / "lineage_manifest.json", manifest)

    model.train()
    step = 0
    running_loss = 0.0
    optimizer.zero_grad()
    saved_steps: list[int] = []
    while step < max_steps:
        for batch in loader:
            device = next(model.parameters()).device
            out = model(
                input_ids=batch["input_ids"].to(device),
                attention_mask=batch["attention_mask"].to(device),
                labels=batch["labels"].to(device),
            )
            loss = out.loss
            running_loss += float(loss.detach().cpu())
            (loss / grad_accum).backward()
            if (step + 1) % grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()
            step += 1
            if step in milestones:
                milestone_dir = adapter_root / f"step_{step}" / "adapter"
                _save_adapter(model, tokenizer, milestone_dir)
                saved_steps.append(step)
                print(f"lineage_saved_adapter step={step} path={milestone_dir}", flush=True)
            if log_every > 0 and (step == 1 or step % log_every == 0 or step >= max_steps):
                denom = log_every if step % log_every == 0 else max(1, step % log_every)
                print(f"lineage_train_step={step}/{max_steps} avg_loss={running_loss / denom:.4f}", flush=True)
                running_loss = 0.0
            if step >= max_steps:
                break

    _save_adapter(model, tokenizer, final_adapter)
    print(f"lineage_saved_final_adapter path={final_adapter}", flush=True)
    merged = model.merge_and_unload()
    final_merged.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(final_merged)
    tokenizer.save_pretrained(final_merged)
    manifest["saved_steps"] = saved_steps
    manifest["status"] = "completed"
    write_json(output_root / "lineage_manifest.json", manifest)
    write_json(final_merged / "lineage_manifest.json", manifest)
    write_json(final_adapter / "lineage_manifest.json", manifest)
    print(f"lineage_saved_final_merged path={final_merged}", flush=True)
    return final_merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    config_path = ROOT / args.config
    config = load_yaml(config_path)
    refuse_bad_reference(json.dumps(config, sort_keys=True))
    max_examples = args.max_examples if args.max_examples is not None else config.get("max_examples")
    examples = collect_examples(config.get("train_files", []), max_examples, config)
    if args.dry_run or config.get("dry_run", False):
        out = dry_run(config, examples, "lineage dry_run")
        append_training_record(config, args.config, "dry_run", out, len(examples), "lineage dry_run")
        return 0
    out = real_train(config_path, config, examples)
    append_training_record(config, args.config, "completed", out, len(examples), "lineage recovery")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
