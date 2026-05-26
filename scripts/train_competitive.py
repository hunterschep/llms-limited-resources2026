#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from train_sft import append_training_record, collect_examples, dry_run, real_train
from wmt26.train.config import load_yaml
from wmt26.train.curriculum import sha256_file, validate_competitive_paths, write_stage_manifest


def git_commit() -> str:
    revision = ROOT / "REVISION"
    if revision.exists():
        value = revision.read_text(encoding="utf-8").strip()
        if value:
            return value
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def manifest_for_config(config_path: Path, config: dict[str, Any], examples: list[dict[str, Any]]) -> dict[str, Any]:
    paths = [ROOT / rel for rel in config.get("train_files", []) or []]
    return {
        "run_name": config.get("run_name"),
        "track": config.get("track"),
        "stage": config.get("stage"),
        "config_path": str(config_path.relative_to(ROOT)),
        "config_sha256": sha256_file(config_path),
        "git_commit": git_commit(),
        "train_files": [
            {
                "path": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "sha256": sha256_file(path) if path.exists() else None,
                "bytes": path.stat().st_size if path.exists() else 0,
            }
            for path in paths
        ],
        "num_examples": len(examples),
        "output_dir": config.get("output_dir"),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
    }


def run_single(config_path: Path, dry: bool, max_examples: int | None) -> Path:
    config = load_yaml(config_path)
    validate_competitive_paths(config)
    examples = collect_examples(config.get("train_files", []), max_examples, config)
    if not examples:
        raise ValueError(f"No competitive examples available for {config_path}")
    manifest = manifest_for_config(config_path, config, examples)
    manifest_path = ROOT / "results/competitive_reboot/status" / f"{config.get('run_name', config_path.stem)}_manifest.json"
    write_stage_manifest(manifest_path, manifest)
    if dry or config.get("dry_run", False):
        output_dir = dry_run(config, examples, "competitive dry_run")
        append_training_record(config, str(config_path.relative_to(ROOT)), "dry_run", output_dir, len(examples), "competitive dry_run")
        return output_dir
    output_dir = real_train(config, examples, max_examples)
    append_training_record(config, str(config_path.relative_to(ROOT)), "completed", output_dir, len(examples), "competitive reboot")
    return output_dir


def run_stagewise(config_path: Path, dry: bool, max_examples: int | None, stop_after: str | None, start_at: str | None = None) -> None:
    config = load_yaml(config_path)
    if not config.get("stagewise"):
        run_single(config_path, dry, max_examples)
        return
    started = start_at is None
    for stage in config.get("stages", []) or []:
        name = str(stage["name"])
        stage_config = ROOT / str(stage["config"])
        if not started:
            if name == start_at:
                started = True
            else:
                print(f"competitive_stage_skip_before_start name={name} start_at={start_at}", flush=True)
                continue
        if stage.get("run_condition") == "competitive_candidate_exists":
            print(f"Skipping conditional stage {name}; run after competitive candidate gate passes.")
            continue
        print(f"competitive_stage_start name={name} config={stage_config}", flush=True)
        run_single(stage_config, dry, max_examples)
        print(f"competitive_stage_done name={name}", flush=True)
        if stop_after and stop_after == name:
            break
    if start_at and not started:
        raise ValueError(f"start_at stage not found in {config_path}: {start_at}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    parser.add_argument("--stop-after", default=None)
    parser.add_argument("--start-at", default=None)
    args = parser.parse_args()
    run_stagewise(ROOT / args.config, args.dry_run, args.max_examples, args.stop_after, args.start_at)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
