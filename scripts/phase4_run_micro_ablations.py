#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase4_common import git_revision, read_yaml, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", default="configs/train/phase4/micro_ablation_grid.yaml")
    parser.add_argument("--track", choices=["ukrainian", "sorbian", "all"], default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--max-examples", type=int, default=16)
    args = parser.parse_args()
    grid = read_yaml(ROOT / args.grid)
    tracks = ["ukrainian", "sorbian"] if args.track == "all" else [args.track]
    runs = []
    for track in tracks:
        anchor = grid[track].get("prompt_anchor")
        for config in grid[track]["configs"]:
            cmd = [sys.executable, "scripts/train_preservation_lora.py", "--config", config]
            if args.dry_run:
                cmd.append("--dry-run")
                cmd += ["--max-examples", str(args.max_examples)]
            proc = subprocess.run(cmd, cwd=ROOT, check=False)
            record = {"track": track, "config": config, "returncode": proc.returncode, "dry_run": args.dry_run}
            if proc.returncode == 0 and args.evaluate and not args.dry_run:
                cfg = read_yaml(ROOT / config)
                adapter_path = Path(cfg["output_dir"]) / "adapter"
                base_model = cfg.get("base_model_path")
                if not base_model:
                    model_cfg = read_yaml(ROOT / cfg.get("model_config", "configs/model/qwen35_2b.yaml"))
                    base_model = model_cfg["model_name_or_path"]
                scale_records = []
                for scale in grid.get("adapter_scales", [1.0]):
                    scale_label = str(scale).replace(".", "p")
                    output = f"results/phase4/micro_ablations/{track}_{Path(config).stem}_scale_{scale_label}.json"
                    eval_cmd = [
                        sys.executable,
                        "scripts/eval_phase4_probe.py",
                        "--config",
                        grid[track]["probe_config"],
                        "--model",
                        str(base_model),
                        "--adapter",
                        str(adapter_path),
                        "--adapter-scale",
                        str(scale),
                        "--output",
                        output,
                    ]
                    eval_proc = subprocess.run(eval_cmd, cwd=ROOT, check=False)
                    scale_records.append({"scale": scale, "returncode": eval_proc.returncode, "output": output})
                    if eval_proc.returncode != 0:
                        proc.returncode = eval_proc.returncode
                        break
                record["anchor"] = anchor
                record["scale_evals"] = scale_records
            runs.append(record)
            if proc.returncode != 0:
                break
    out = ROOT / "results/phase4/micro_ablations/micro_ablation_runs.json"
    write_json(out, {"git_commit": git_revision(), "runs": runs})
    print(json.dumps({"output": str(out), "runs": runs}, indent=2, sort_keys=True))
    return 0 if all(run["returncode"] == 0 for run in runs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
