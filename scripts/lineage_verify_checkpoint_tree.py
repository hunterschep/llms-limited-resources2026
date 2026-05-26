#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import (  # noqa: E402
    EDIT_REPAIR_TINY,
    LINEAGE_REMOTE_ROOT,
    LINEAGE_STATUS,
    ORIGINAL_STAGE_B,
    STAGE_A_ADAPTER,
    STAGE_A_PARENT,
    STAGE_B_ADAPTER,
    STAGE_B_MERGED,
    git_commit,
    write_json,
)


def _check(path: str, required_files: list[str] | None = None, any_files: list[str] | None = None) -> dict[str, Any]:
    p = Path(path)
    required_files = required_files or []
    any_files = any_files or []
    files = {name: (p / name).exists() for name in required_files}
    any_ok = True if not any_files else any((p / name).exists() for name in any_files)
    return {
        "path": path,
        "exists": p.exists(),
        "is_dir": p.is_dir(),
        "required_files": files,
        "any_files": {name: (p / name).exists() for name in any_files},
        "ok": p.exists() and all(files.values()) and any_ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/lineage_recovery/status/checkpoint_tree.json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    checks = {
        "original_stage_b_preserved": _check(ORIGINAL_STAGE_B, ["config.json"]),
        "edit_repair_tiny_preserved": _check(EDIT_REPAIR_TINY, ["config.json"]),
        "stage_a_parent": _check(STAGE_A_PARENT, ["config.json", "lineage_manifest.json"]),
        "stage_a_adapter": _check(STAGE_A_ADAPTER, ["adapter_config.json", "lineage_manifest.json"], ["adapter_model.safetensors", "adapter_model.bin"]),
        "stage_b_adapter": _check(STAGE_B_ADAPTER, ["adapter_config.json", "lineage_manifest.json"], ["adapter_model.safetensors", "adapter_model.bin"]),
        "stage_b_merged": _check(STAGE_B_MERGED, ["config.json", "lineage_manifest.json"]),
    }
    manifest = {
        "git_commit": git_commit(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "lineage_remote_root": LINEAGE_REMOTE_ROOT,
        "checks": checks,
        "ok": all(item["ok"] for item in checks.values()),
    }
    out = ROOT / args.output
    write_json(out, manifest)
    write_json(LINEAGE_STATUS / "checkpoint_tree_latest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if args.strict and not manifest["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
