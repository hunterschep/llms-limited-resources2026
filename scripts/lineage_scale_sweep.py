#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import LINEAGE_SWEEP, STAGE_A_PARENT, STAGE_B_ADAPTER, aggregate_row, refuse_bad_reference, write_json  # noqa: E402


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/merge/lineage_sorbian_interpolation.yaml")
    parser.add_argument("--model", default=STAGE_A_PARENT)
    parser.add_argument("--adapter", default=STAGE_B_ADAPTER)
    parser.add_argument("--eval-config", default=None)
    parser.add_argument("--output-dir", default="results/lineage_recovery/scale_sweep")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    cfg = _load(ROOT / args.config)
    scales = [float(x) for x in cfg.get("adapter_scales", [0.2, 0.5, 1.0])]
    eval_config = args.eval_config or cfg.get("probe_config", "configs/eval/lineage_sorbian_probe.yaml")
    refuse_bad_reference(json.dumps(cfg, sort_keys=True))
    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    model_ok = Path(args.model).exists()
    adapter_ok = Path(args.adapter).exists()
    plan = {
        "model": args.model,
        "adapter": args.adapter,
        "model_exists": model_ok,
        "adapter_exists": adapter_ok,
        "eval_config": eval_config,
        "scales": scales,
        "execute": args.execute,
        "results": [],
    }
    if args.execute:
        if not model_ok:
            raise FileNotFoundError(f"Missing parent model for scale sweep: {args.model}")
        if not adapter_ok:
            raise FileNotFoundError(f"Missing Stage B adapter for scale sweep: {args.adapter}")
        for scale in scales:
            name = f"adapter_scale_{scale:.2f}"
            output = out_dir / f"{name}.json"
            raw = out_dir / f"{name}_raw.jsonl"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/lineage_eval_scaled_candidate.py",
                    "--config",
                    eval_config,
                    "--model",
                    args.model,
                    "--adapter",
                    args.adapter,
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
            plan["results"].append(aggregate_row(name, output))
    write_json(out_dir / "scale_sweep_summary.json", plan)
    write_json(LINEAGE_SWEEP / "scale_sweep_summary.json", plan)
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
