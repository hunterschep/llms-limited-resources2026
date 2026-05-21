#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def write_dry_run(config: dict, method: str, weights: dict[str, float] | None = None) -> Path:
    output_dir = resolve_output_dir(config["output_dir"]) / method
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = {
        "track": config["track"],
        "base_model": config["base_model"],
        "method": method,
        "specialists": config.get("specialists", {}),
        "weights": weights or {},
        "objective": config.get("objective"),
        "dry_run": True,
    }
    (output_dir / "MERGE_DRY_RUN.json").write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_dir


def scratch_root() -> Path | None:
    value = os.environ.get("SCRATCH_ROOT")
    return Path(value) if value else None


def resolve_checkpoint_ref(ref: str) -> str:
    """Resolve repo-relative checkpoint refs while allowing Hugging Face IDs."""
    path = Path(ref)
    candidates: list[Path] = []
    if path.is_absolute():
        candidates.append(path)
    else:
        if ref.startswith("checkpoints/") and scratch_root() is not None:
            candidates.append(scratch_root() / ref)
        candidates.append(ROOT / ref)
        candidates.append(path)
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    if ref.startswith("checkpoints/"):
        raise FileNotFoundError(f"Checkpoint path does not exist locally or under SCRATCH_ROOT: {ref}")
    return ref


def resolve_output_dir(ref: str) -> Path:
    path = Path(ref)
    if path.is_absolute():
        return path
    if ref.startswith("checkpoints/") and scratch_root() is not None:
        return scratch_root() / ref
    return ROOT / ref


def copy_tokenizer_and_generation_assets(source_ref: str, output_dir: Path) -> None:
    from transformers import AutoTokenizer

    try:
        tokenizer = AutoTokenizer.from_pretrained(source_ref, trust_remote_code=True)
        tokenizer.save_pretrained(output_dir)
    except Exception as exc:  # pragma: no cover - defensive for unusual model repos
        print(f"Warning: could not save tokenizer assets from {source_ref}: {exc}", file=sys.stderr)

    source_path = Path(source_ref)
    if source_path.is_dir():
        for name in ["generation_config.json", "preprocessor_config.json", "tokenizer_config.json", "chat_template.jinja"]:
            src = source_path / name
            if src.exists() and not (output_dir / name).exists():
                shutil.copy2(src, output_dir / name)


def append_merge_record(config: dict, config_path: str, method: str, weights: dict[str, float], output_dir: Path, status: str, notes: str = "") -> None:
    if os.environ.get("WMT26_RECORD_RUNS", "1") == "0":
        return
    record = {
        "merge_id": f"{config.get('track')}_{method}_{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "track": config.get("track"),
        "base_checkpoint": config.get("base_model"),
        "candidate_checkpoints": config.get("specialists", {}),
        "merge_method": method,
        "merge_weights": weights,
        "merge_config": config_path,
        "output_checkpoint": str(output_dir.relative_to(ROOT)) if output_dir.is_relative_to(ROOT) else str(output_dir),
        "eval_id": None,
        "overall_score": None,
        "per_task_scores": {},
        "status": status,
        "andromeda_job_id": os.environ.get("SLURM_JOB_ID"),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "notes": notes,
    }
    out = ROOT / "results/merge_runs.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def linear_task_vector_merge(config: dict, weights: dict[str, float]) -> Path:
    import gc

    import torch
    from transformers import AutoModelForCausalLM

    base_ref = resolve_checkpoint_ref(config["base_model"])
    output_dir = resolve_output_dir(config["output_dir"]) / "weighted_task_vector"
    output_dir.mkdir(parents=True, exist_ok=True)

    dtype_name = str(config.get("merge_dtype", "float32")).lower()
    dtype = {"float32": torch.float32, "fp32": torch.float32, "bfloat16": torch.bfloat16, "bf16": torch.bfloat16}.get(dtype_name, torch.float32)
    print(f"Loading base model for merge: {base_ref}")
    model = AutoModelForCausalLM.from_pretrained(
        base_ref,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        device_map=None,
    )
    state = model.state_dict()
    base_state = {
        k: (v.detach().cpu().to(torch.float32).clone() if torch.is_floating_point(v) else v.detach().cpu().clone())
        for k, v in state.items()
    }
    merged = {k: v.clone() for k, v in base_state.items()}

    for name, rel in config.get("specialists", {}).items():
        weight = float(weights.get(name, 1.0))
        specialist_ref = resolve_checkpoint_ref(rel)
        print(f"Applying specialist {name} with weight={weight}: {specialist_ref}")
        specialist = AutoModelForCausalLM.from_pretrained(
            specialist_ref,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            device_map=None,
        )
        spec_state = specialist.state_dict()
        applied = 0
        skipped = 0
        for key, base_tensor in base_state.items():
            spec_tensor = spec_state.get(key)
            if spec_tensor is None or spec_tensor.shape != base_tensor.shape:
                skipped += 1
                continue
            if not torch.is_floating_point(base_tensor) or not torch.is_floating_point(spec_tensor):
                skipped += 1
                continue
            merged[key].add_(weight * (spec_tensor.detach().cpu().to(torch.float32) - base_tensor))
            applied += 1
        print(f"Applied {applied} tensors for {name}; skipped {skipped}.")
        del specialist, spec_state
        gc.collect()

    load_state = {k: v.to(dtype if torch.is_floating_point(v) else v.dtype) for k, v in merged.items()}
    missing, unexpected = model.load_state_dict(load_state, strict=False)
    if missing or unexpected:
        print(f"Warning: load_state_dict missing={len(missing)} unexpected={len(unexpected)}", file=sys.stderr)
    print(f"Saving merged model to {output_dir}")
    model.save_pretrained(output_dir, safe_serialization=True, max_shard_size=str(config.get("max_shard_size", "2GB")))
    copy_tokenizer_and_generation_assets(base_ref, output_dir)
    metadata = {
        "track": config.get("track"),
        "base_model": config.get("base_model"),
        "resolved_base_model": base_ref,
        "specialists": config.get("specialists", {}),
        "weights": weights,
        "method": "weighted_task_vector",
        "merge_dtype": dtype_name,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    (output_dir / "merge_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--method", default="weighted_task_vector")
    parser.add_argument("--weights-json", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    weights = json.loads(args.weights_json) if args.weights_json else {k: 1.0 for k in config.get("specialists", {})}
    if args.dry_run:
        out = write_dry_run(config, args.method, weights)
        append_merge_record(config, args.config, args.method, weights, out, "dry_run")
    else:
        if args.method != "weighted_task_vector":
            raise NotImplementedError("Only weighted_task_vector real merge is implemented. Use --dry-run for other methods.")
        out = linear_task_vector_merge(config, weights)
        append_merge_record(config, args.config, args.method, weights, out, "completed")
    print(f"Merge output: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
