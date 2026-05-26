#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

VARIANTS = [
    {"name": "baseline_192", "max_new_tokens": 192, "notes": "probe default"},
    {"name": "short_96", "max_new_tokens": 96, "notes": "shorter QA/MR/edit generations; MT still usually fits probe sentences"},
    {"name": "compact_64", "max_new_tokens": 64, "notes": "strong anti-ramble cap; diagnostic only for MT"},
    {"name": "full_256", "max_new_tokens": 256, "notes": "current full-eval default"},
]


def _write_variant_config(base_config: Path, variant: dict, out_dir: Path) -> Path:
    config = yaml.safe_load(base_config.read_text(encoding="utf-8")) or {}
    config["max_new_tokens"] = int(variant["max_new_tokens"])
    config["stage_b_prompt_sweep_variant"] = variant
    out = out_dir / f"{variant['name']}.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", default="configs/eval/stage_b_rescue_probe_sorbian.yaml")
    parser.add_argument("--model", default="$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large")
    parser.add_argument("--output-dir", default="results/stage_b_rescue/prompt_sweep")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    base_config = ROOT / args.base_config
    out_dir = ROOT / args.output_dir
    cfg_dir = ROOT / "configs/eval/stage_b_rescue_prompt_sweep"
    plan = []
    for variant in VARIANTS:
        cfg = _write_variant_config(base_config, variant, cfg_dir)
        output = out_dir / f"{variant['name']}.json"
        raw = out_dir / f"{variant['name']}_raw.jsonl"
        row = {
            **variant,
            "config": str(cfg.relative_to(ROOT)),
            "model": args.model,
            "output": str(output.relative_to(ROOT)),
            "raw_output": str(raw.relative_to(ROOT)),
        }
        plan.append(row)
        if args.execute:
            subprocess.run(
                [
                    sys.executable,
                    "scripts/competitive_eval.py",
                    "--config",
                    row["config"],
                    "--model",
                    args.model,
                    "--output",
                    row["output"],
                    "--raw-output",
                    row["raw_output"],
                ],
                cwd=ROOT,
                check=True,
            )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "prompt_sweep_plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    doc = ROOT / "docs/87_stage_b_repair_methods.md"
    if not doc.exists():
        doc.write_text("# Stage B Repair Methods\n\n", encoding="utf-8")
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
