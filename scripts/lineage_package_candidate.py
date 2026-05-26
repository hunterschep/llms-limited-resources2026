#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output-dir", default="results/lineage_recovery/package")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    model_dir = Path(args.model_dir)
    required = ["config.json", "tokenizer_config.json"]
    missing = [name for name in required if not (model_dir / name).exists()]
    manifest = {
        "model_dir": str(model_dir),
        "dry_run": args.dry_run,
        "packageable": not missing,
        "missing": missing,
        "policy": {
            "one_model": True,
            "qwen35_le_2b": True,
            "no_task_specific_adapter_switching": True,
            "no_live_rag": True,
            "no_public_upload_without_approval": True,
        },
    }
    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "lineage_package_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0 if manifest["packageable"] or args.dry_run else 1


if __name__ == "__main__":
    raise SystemExit(main())
