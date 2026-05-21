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


def write_dry_run(config: dict, method: str, weights: dict[str, float] | None = None) -> Path:
    output_dir = ROOT / config["output_dir"] / method
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


def load_state(path: Path):
    import torch

    if path.is_dir():
        for candidate in ["pytorch_model.bin", "adapter_model.bin", "model.pt", "state.pt"]:
            p = path / candidate
            if p.exists():
                return torch.load(p, map_location="cpu")
        candidates = list(path.glob("*.bin")) + list(path.glob("*.pt"))
        if candidates:
            return torch.load(candidates[0], map_location="cpu")
        raise FileNotFoundError(f"No mergeable state found under {path}")
    return torch.load(path, map_location="cpu")


def save_state(state, output_dir: Path) -> None:
    import torch

    output_dir.mkdir(parents=True, exist_ok=True)
    torch.save(state, output_dir / "pytorch_model.bin")


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
    base = load_state(Path(config["base_model"]))
    merged = {k: v.clone() for k, v in base.items()}
    for name, rel in config["specialists"].items():
        weight = float(weights.get(name, 1.0))
        spec = load_state(ROOT / rel)
        for key, base_tensor in base.items():
            if key in spec and hasattr(base_tensor, "shape") and spec[key].shape == base_tensor.shape:
                merged[key] = merged[key] + weight * (spec[key] - base_tensor)
    output_dir = ROOT / config["output_dir"] / "weighted_task_vector"
    save_state(merged, output_dir)
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
        if not Path(config["base_model"]).exists():
            raise FileNotFoundError("Real merge requires config base_model to be a local checkpoint path. Use --dry-run for config validation.")
        out = linear_task_vector_merge(config, weights)
        append_merge_record(config, args.config, args.method, weights, out, "completed")
    print(f"Merge output: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
