#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import aggregate_row, refuse_bad_reference, write_json  # noqa: E402


def _load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _available(path: str) -> bool:
    return Path(path).exists() and (Path(path) / "config.json").exists()


def merge_models(anchor: str, mt_model: str, edit_model: str | None, mr_model: str | None, coeffs: dict[str, float], output: Path) -> None:
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:  # pragma: no cover - exercised on Andromeda
        raise RuntimeError("Install torch and transformers for lineage task-vector merge.") from exc

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    device_map = "auto" if torch.cuda.is_available() else None
    anchor_model = AutoModelForCausalLM.from_pretrained(anchor, trust_remote_code=True, torch_dtype=dtype, device_map=device_map)
    mt = AutoModelForCausalLM.from_pretrained(mt_model, trust_remote_code=True, torch_dtype=dtype, device_map=device_map)
    edit = AutoModelForCausalLM.from_pretrained(edit_model, trust_remote_code=True, torch_dtype=dtype, device_map=device_map) if edit_model else None
    mr = AutoModelForCausalLM.from_pretrained(mr_model, trust_remote_code=True, torch_dtype=dtype, device_map=device_map) if mr_model else None
    state_anchor = anchor_model.state_dict()
    state_mt = mt.state_dict()
    state_edit = edit.state_dict() if edit else {}
    state_mr = mr.state_dict() if mr else {}
    with torch.no_grad():
        for name, tensor in state_anchor.items():
            if not tensor.is_floating_point():
                continue
            base = tensor.clone()
            updated = base + coeffs["mt"] * (state_mt[name].to(tensor.device, dtype=tensor.dtype) - base)
            if edit_model and name in state_edit:
                updated = updated + coeffs.get("edit", 0.0) * (state_edit[name].to(tensor.device, dtype=tensor.dtype) - state_mt[name].to(tensor.device, dtype=tensor.dtype))
            if mr_model and name in state_mr:
                updated = updated + coeffs.get("mr", 0.0) * (state_mr[name].to(tensor.device, dtype=tensor.dtype) - state_mt[name].to(tensor.device, dtype=tensor.dtype))
            tensor.copy_(updated)
    output.mkdir(parents=True, exist_ok=True)
    anchor_model.save_pretrained(output)
    AutoTokenizer.from_pretrained(mt_model, trust_remote_code=True).save_pretrained(output)
    write_json(output / "lineage_task_vector_manifest.json", {"anchor": anchor, "mt_model": mt_model, "edit_model": edit_model, "mr_model": mr_model, "coefficients": coeffs})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/merge/lineage_sorbian_task_vectors.yaml")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--delete-failed", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    cfg = _load(ROOT / args.config)
    refuse_bad_reference(json.dumps(cfg, sort_keys=True))
    anchor = cfg["anchor_model"]
    mt_model = cfg["mt_model"]
    edit_model = cfg.get("edit_model") if _available(str(cfg.get("edit_model", ""))) else None
    mr_model = cfg.get("mr_model") if _available(str(cfg.get("mr_model", ""))) else None
    output_root = Path(cfg["output_root"])
    results_dir = ROOT / cfg.get("results_dir", "results/lineage_recovery/merge")
    results_dir.mkdir(parents=True, exist_ok=True)
    mt_coeffs = [float(x) for x in cfg["coefficients"]["mt"]]
    edit_coeffs = [0.0] if not edit_model else [float(x) for x in cfg["coefficients"]["edit"]]
    mr_coeffs = [0.0] if not mr_model else [float(x) for x in cfg["coefficients"]["mr"]]
    combos = list(itertools.product(mt_coeffs, edit_coeffs, mr_coeffs))
    if args.limit:
        combos = combos[: args.limit]
    summary = {"anchor_model": anchor, "mt_model": mt_model, "edit_model": edit_model, "mr_model": mr_model, "execute": args.execute, "candidates": []}
    if args.execute:
        if not _available(anchor):
            raise FileNotFoundError(f"Missing merge anchor: {anchor}")
        if not _available(mt_model):
            raise FileNotFoundError(f"Missing MT model: {mt_model}")
        for mt_c, edit_c, mr_c in combos:
            name = f"mt{mt_c:.2f}_edit{edit_c:.2f}_mr{mr_c:.2f}".replace(".", "p")
            out_model = output_root / name
            result_path = results_dir / f"{name}.json"
            coeffs = {"mt": mt_c, "edit": edit_c, "mr": mr_c}
            if not (out_model / "config.json").exists():
                merge_models(anchor, mt_model, edit_model, mr_model, coeffs, out_model)
            subprocess.run(
                [sys.executable, "scripts/competitive_eval.py", "--config", cfg.get("probe_config", "configs/eval/lineage_sorbian_probe.yaml"), "--model", str(out_model), "--output", str(result_path.relative_to(ROOT))],
                cwd=ROOT,
                check=True,
            )
            row = aggregate_row(name, result_path)
            row["coefficients"] = coeffs
            summary["candidates"].append(row)
            if args.delete_failed and row.get("MT", 0) < 38.0 and out_model.exists():
                shutil.rmtree(out_model)
                row["checkpoint_deleted_after_probe"] = True
    write_json(results_dir / "task_vector_merge_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
