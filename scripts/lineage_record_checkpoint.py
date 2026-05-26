#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from lineage_common import git_commit, refuse_bad_reference, resolve_local_or_scratch, sha256_path, write_json  # noqa: E402
from wmt26.train.config import load_yaml  # noqa: E402


def _base_for_config(config: dict) -> str:
    if config.get("base_model_path"):
        return str(resolve_local_or_scratch(str(config["base_model_path"])))
    model_cfg = load_yaml(ROOT / config.get("model_config", "configs/model/qwen35_2b.yaml"))
    return str(model_cfg["model_name_or_path"])


def materialize(base_model: str, adapter: Path, output: Path, trust_remote_code: bool = True) -> None:
    try:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as exc:  # pragma: no cover - exercised on Andromeda
        raise RuntimeError("Install torch, transformers, and peft to materialize lineage checkpoints.") from exc

    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else (torch.float16 if torch.cuda.is_available() else torch.float32)
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        trust_remote_code=trust_remote_code,
        torch_dtype=dtype,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=trust_remote_code)
    peft_model = PeftModel.from_pretrained(model, str(adapter))
    merged = peft_model.merge_and_unload()
    output.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(output)
    tokenizer.save_pretrained(output)


def manifest(output: Path, base_model: str, adapter: Path) -> None:
    adapter_config = adapter / "adapter_config.json"
    write_json(
        output / "lineage_materialization_manifest.json",
        {
            "git_commit": git_commit(),
            "base_model": base_model,
            "adapter": str(adapter),
            "adapter_config_sha256": sha256_path(adapter_config) if adapter_config.exists() else None,
            "output": str(output),
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--base-model")
    parser.add_argument("--adapter")
    parser.add_argument("--output")
    parser.add_argument("--materialize-all", action="store_true")
    args = parser.parse_args()
    if args.config:
        config_path = ROOT / args.config
        config = load_yaml(config_path)
        refuse_bad_reference(json.dumps(config, sort_keys=True))
        base_model = _base_for_config(config)
        output_root = resolve_local_or_scratch(str(config["output_dir"]))
        adapter_root = resolve_local_or_scratch(str(config.get("adapter_output_dir", config["output_dir"])))
        pairs: list[tuple[Path, Path]] = []
        if args.materialize_all:
            for step in config.get("save_milestones", []) or []:
                pairs.append((adapter_root / f"step_{int(step)}" / "adapter", output_root / f"step_{int(step)}" / "merged"))
        pairs.append((adapter_root / "final_adapter", output_root / "final_merged"))
    else:
        if not (args.base_model and args.adapter and args.output):
            raise SystemExit("Provide --config or --base-model/--adapter/--output.")
        base_model = args.base_model
        pairs = [(Path(args.adapter), Path(args.output))]
    for adapter, output in pairs:
        if not adapter.exists():
            raise FileNotFoundError(f"Missing adapter: {adapter}")
        if output.exists() and (output / "config.json").exists():
            print(f"lineage_materialize_skip existing={output}", flush=True)
        else:
            materialize(base_model, adapter, output)
        manifest(output, base_model, adapter)
        print(f"lineage_materialized adapter={adapter} output={output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
