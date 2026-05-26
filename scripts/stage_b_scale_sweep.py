#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCALES = [0.50, 0.65, 0.75, 0.85, 0.90, 1.00, 1.10]


def _resolve(path: str) -> Path:
    expanded = os.path.expandvars(path)
    candidate = Path(expanded)
    if candidate.exists():
        return candidate
    scratch = os.environ.get("SCRATCH_ROOT")
    if scratch and candidate.parts and candidate.parts[0] == "checkpoints":
        return Path(scratch) / candidate
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", default="$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_a_dapt_large")
    parser.add_argument("--adapter", default="$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large/adapter")
    parser.add_argument("--config", default="configs/eval/stage_b_rescue_probe_sorbian.yaml")
    parser.add_argument("--output-dir", default="results/stage_b_rescue/scale_sweep")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    base_path = _resolve(args.base_model)
    adapter_path = _resolve(args.adapter)
    plan = {
        "base_model": args.base_model,
        "adapter": args.adapter,
        "base_exists": base_path.exists(),
        "adapter_exists": adapter_path.exists(),
        "scales": SCALES,
        "status": "planned",
        "reason": "",
        "results": [],
    }
    if not base_path.exists() or not adapter_path.exists():
        plan["status"] = "ruled_out"
        plan["reason"] = "Stage B was preserved as a merged checkpoint but its original Stage A base checkpoint is not retained, so the LoRA adapter cannot be safely re-applied for scale search."
        (out_dir / "scale_sweep_plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0
    if args.execute:
        for scale in SCALES:
            output = out_dir / f"stage_b_adapter_scale_{scale:.2f}.json"
            raw = out_dir / f"stage_b_adapter_scale_{scale:.2f}_raw.jsonl"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/competitive_eval.py",
                    "--config",
                    args.config,
                    "--model",
                    str(base_path),
                    "--adapter",
                    str(adapter_path),
                    "--adapter-scale",
                    str(scale),
                    "--output",
                    str(output.relative_to(ROOT)),
                    "--raw-output",
                    str(raw.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=True,
            )
            plan["results"].append(str(output.relative_to(ROOT)))
    (out_dir / "scale_sweep_plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
