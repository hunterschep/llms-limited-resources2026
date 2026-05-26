#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODELS = {
    "prompt_only": "Qwen/Qwen3.5-2B",
    "stage_b": "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large",
    "stage_c_diagnostic": "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_c_instruction_replay",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-key", choices=sorted(MODELS), default="stage_b")
    parser.add_argument("--config", default="configs/eval/sorbian.yaml")
    parser.add_argument("--output-dir", default="results/stage_b_rescue/error_analysis/raw_inputs")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    model_name = MODELS[args.model_key]
    stem = {
        "prompt_only": "prompt_only_qwen35_2b",
        "stage_b": "stage_b_mt_large",
        "stage_c_diagnostic": "stage_c_instruction_replay",
    }[args.model_key]
    command = [
        sys.executable,
        "scripts/competitive_eval.py",
        "--config",
        args.config,
        "--model",
        model_name,
        "--output",
        str(output_dir / f"{stem}.json"),
        "--raw-output",
        str(output_dir / f"{stem}_raw.jsonl"),
    ]
    if args.limit:
        command.extend(["--limit", str(args.limit)])
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
