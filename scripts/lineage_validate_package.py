#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output", default="results/lineage_recovery/package/package_validation.json")
    parser.add_argument("--load", action="store_true")
    args = parser.parse_args()
    model_dir = Path(args.model_dir)
    result = {
        "model_dir": str(model_dir),
        "exists": model_dir.exists(),
        "required_files": {name: (model_dir / name).exists() for name in ["config.json", "tokenizer_config.json"]},
        "load_checked": False,
        "load_ok": None,
    }
    if args.load:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
            AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, device_map="cpu")
            result["load_checked"] = True
            result["load_ok"] = True
        except Exception as exc:  # pragma: no cover - optional expensive path
            result["load_checked"] = True
            result["load_ok"] = False
            result["error"] = str(exc)
    result["ok"] = result["exists"] and all(result["required_files"].values()) and (result["load_ok"] is not False)
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
