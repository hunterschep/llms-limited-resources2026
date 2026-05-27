#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--track", default="sorbian")
    parser.add_argument("--label", default="primary")
    parser.add_argument("--copy", action="store_true")
    args = parser.parse_args()
    model_dir = Path(args.model_dir)
    package_dir = Path(args.package_dir)
    if not model_dir.exists():
        raise FileNotFoundError(model_dir)
    package_dir.mkdir(parents=True, exist_ok=True)
    if args.copy:
        model_out = package_dir / "model"
        if model_out.exists():
            shutil.rmtree(model_out)
        shutil.copytree(model_dir, model_out, symlinks=True)
        packaged_model_path = str(model_out)
    else:
        packaged_model_path = str(model_dir)
    manifest = {
        "track": args.track,
        "label": args.label,
        "source_model_dir": str(model_dir),
        "package_dir": str(package_dir),
        "packaged_model_path": packaged_model_path,
        "copy": args.copy,
        "wmt_constraints": {
            "qwen35_family_le_2b": True,
            "one_model_all_tasks": True,
            "no_task_adapter_switching": True,
            "no_live_rag": True,
            "no_public_upload_without_approval": True,
        },
    }
    (package_dir / "package_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (package_dir / "README.md").write_text(
        "\n".join(
            [
                f"# WMT26 {args.track} {args.label} package",
                "",
                f"Model path: `{packaged_model_path}`",
                "",
                "This package uses one Qwen3.5-family <=2B model for MT, QA, SC, GC, and MR.",
                "No public upload was performed by this script.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
