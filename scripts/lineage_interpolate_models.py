#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import aggregate_row, refuse_bad_reference, write_json  # noqa: E402


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def interpolate(model_a: str, model_b: str, alpha: float, output: Path) -> None:
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:  # pragma: no cover - exercised on Andromeda
        raise RuntimeError("Install torch and transformers for model interpolation.") from exc

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    device_map = "auto" if torch.cuda.is_available() else None
    a = AutoModelForCausalLM.from_pretrained(model_a, trust_remote_code=True, torch_dtype=dtype, device_map=device_map)
    b = AutoModelForCausalLM.from_pretrained(model_b, trust_remote_code=True, torch_dtype=dtype, device_map=device_map)
    state_a = a.state_dict()
    state_b = b.state_dict()
    with torch.no_grad():
        for name, tensor_a in state_a.items():
            tensor_b = state_b.get(name)
            if tensor_b is None:
                continue
            if tensor_a.is_floating_point():
                tensor_a.copy_(tensor_a.mul(1.0 - alpha).add(tensor_b.to(tensor_a.device, dtype=tensor_a.dtype), alpha=alpha))
            elif alpha >= 0.5:
                tensor_a.copy_(tensor_b.to(tensor_a.device, dtype=tensor_a.dtype))
    output.mkdir(parents=True, exist_ok=True)
    a.save_pretrained(output)
    tokenizer = AutoTokenizer.from_pretrained(model_b, trust_remote_code=True)
    tokenizer.save_pretrained(output)
    write_json(output / "lineage_interpolation_manifest.json", {"model_a": model_a, "model_b": model_b, "alpha": alpha})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/merge/lineage_sorbian_interpolation.yaml")
    parser.add_argument("--model-a", default=None)
    parser.add_argument("--model-b", default=None)
    parser.add_argument("--alphas", nargs="*", type=float, default=None)
    parser.add_argument("--eval-config", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--delete-failed", action="store_true")
    args = parser.parse_args()
    cfg = _load(ROOT / args.config)
    refuse_bad_reference(json.dumps(cfg, sort_keys=True))
    model_a = args.model_a or cfg["anchor_model"]
    model_b = args.model_b or cfg["stage_b_model"]
    alphas = args.alphas or [float(x) for x in cfg.get("stagea_stageb_alphas", [0.5, 1.0])]
    output_root = Path(args.output_dir or cfg.get("output_root"))
    results_dir = ROOT / (args.results_dir or cfg.get("results_dir", "results/lineage_recovery/interpolation"))
    eval_config = args.eval_config or cfg.get("probe_config", "configs/eval/lineage_sorbian_probe.yaml")
    results_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "model_a": model_a,
        "model_b": model_b,
        "alphas": alphas,
        "eval_config": eval_config,
        "execute": args.execute,
        "results": [],
    }
    if args.execute:
        if not Path(model_a).exists():
            raise FileNotFoundError(f"Missing interpolation anchor: {model_a}")
        if not Path(model_b).exists():
            raise FileNotFoundError(f"Missing interpolation target: {model_b}")
        for alpha in alphas:
            name = f"stagea_stageb_alpha_{alpha:.2f}"
            out_model = output_root / name
            out_result = results_dir / f"{name}.json"
            if not (out_model / "config.json").exists():
                interpolate(model_a, model_b, alpha, out_model)
            subprocess.run(
                [
                    sys.executable,
                    "scripts/competitive_eval.py",
                    "--config",
                    eval_config,
                    "--model",
                    str(out_model),
                    "--output",
                    str(out_result.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=True,
            )
            row = aggregate_row(name, out_result)
            summary["results"].append(row)
            if args.delete_failed and row.get("MT", 0) < 38.0 and out_model.exists():
                shutil.rmtree(out_model)
                row["checkpoint_deleted_after_probe"] = True
    write_json(results_dir / "interpolation_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
