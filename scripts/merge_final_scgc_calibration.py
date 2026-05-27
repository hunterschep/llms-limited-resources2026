#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from lineage_common import aggregate_row, write_json  # noqa: E402
from wmt26.eval.metrics import parse_edit_output, scgc_diagnostics  # noqa: E402


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def interpolate(anchor: str, calibrated: str, alpha: float, output: Path) -> None:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    device_map = "auto" if torch.cuda.is_available() else None
    anchor_model = AutoModelForCausalLM.from_pretrained(anchor, trust_remote_code=True, torch_dtype=dtype, device_map=device_map)
    calibrated_model = AutoModelForCausalLM.from_pretrained(calibrated, trust_remote_code=True, torch_dtype=dtype, device_map=device_map)
    a_state = anchor_model.state_dict()
    c_state = calibrated_model.state_dict()
    with torch.no_grad():
        for name, tensor in a_state.items():
            other = c_state.get(name)
            if other is None:
                continue
            if tensor.is_floating_point():
                tensor.copy_(tensor.mul(1.0 - alpha).add(other.to(tensor.device, dtype=tensor.dtype), alpha=alpha))
            elif alpha >= 0.5:
                tensor.copy_(other.to(tensor.device, dtype=tensor.dtype))
    output.mkdir(parents=True, exist_ok=True)
    anchor_model.save_pretrained(output)
    AutoTokenizer.from_pretrained(calibrated, trust_remote_code=True).save_pretrained(output)
    write_json(output / "final_salvage_merge_manifest.json", {"anchor": anchor, "calibrated": calibrated, "alpha": alpha})


def no_error_from_raw(raw_path: Path) -> dict[str, float]:
    rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    out = {}
    for task in ("SC", "GC"):
        preds = [row["prediction"] for row in rows if row.get("task") == task]
        refs = [row["reference"] for row in rows if row.get("task") == task]
        diag = scgc_diagnostics(preds, refs)
        out[f"{task}_no_error_accuracy"] = diag["detection_tn"] / max(1, diag["gold_correct"])
        out[f"{task}_predicted_correct"] = diag["pred_correct"]
        out[f"{task}_predicted_error"] = diag["pred_error"]
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/merge/final_salvage/scgc_calibration_merge.yaml")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    cfg = load_yaml(ROOT / args.config)
    anchor = cfg["anchor_model"]
    calibrated = cfg["calibrated_model"]
    output_root = Path(cfg["output_root"])
    results_dir = ROOT / cfg.get("results_dir", "results/final_salvage/calibration_merge")
    results_dir.mkdir(parents=True, exist_ok=True)
    alphas = [float(x) for x in cfg.get("alphas", [1.0])]
    if args.limit:
        alphas = alphas[: args.limit]
    summary = {"anchor_model": anchor, "calibrated_model": calibrated, "candidates": []}
    if args.execute:
        if not Path(anchor).exists():
            raise FileNotFoundError(anchor)
        if not Path(calibrated).exists():
            raise FileNotFoundError(calibrated)
        for alpha in alphas:
            name = f"scgc_alpha_{alpha:.2f}".replace(".", "p")
            model_dir = output_root / name
            result = results_dir / f"{name}.json"
            raw = results_dir / f"{name}_raw.jsonl"
            if not (model_dir / "config.json").exists():
                interpolate(anchor, calibrated, alpha, model_dir)
            subprocess.run(
                [
                    sys.executable,
                    "scripts/competitive_eval.py",
                    "--config",
                    cfg.get("probe_config", "configs/eval/final_salvage_scgc_probe.yaml"),
                    "--model",
                    str(model_dir),
                    "--output",
                    str(result.relative_to(ROOT)),
                    "--raw-output",
                    str(raw.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=True,
            )
            row = aggregate_row(name, result)
            row["alpha"] = alpha
            row.update(no_error_from_raw(raw))
            row["model_dir"] = str(model_dir)
            summary["candidates"].append(row)
    write_json(results_dir / "scgc_calibration_merge_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
