#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import EDIT_REPAIR_TINY, LINEAGE_CLEANUP, ORIGINAL_STAGE_B, STAGE_A_PARENT, STAGE_B_MERGED, git_commit, write_json  # noqa: E402


def run(command: list[str]) -> int:
    print("+ " + " ".join(command), flush=True)
    return subprocess.call(command, cwd=ROOT)


def status() -> int:
    data = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "paths": {
            "original_stage_b": ORIGINAL_STAGE_B,
            "edit_repair_tiny": EDIT_REPAIR_TINY,
            "lineage_stage_a_parent": STAGE_A_PARENT,
            "lineage_stage_b_merged": STAGE_B_MERGED,
        },
        "local_git_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
    }
    write_json(ROOT / "results/lineage_recovery/status/local_status.json", data)
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def cleanup() -> int:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    LINEAGE_CLEANUP.mkdir(parents=True, exist_ok=True)
    manifest = {
        "timestamp": timestamp,
        "git_commit_before_cleanup": git_commit(),
        "local_files_deleted": [],
        "local_files_archived": [],
        "preserved_remote_checkpoints": [ORIGINAL_STAGE_B, EDIT_REPAIR_TINY],
        "notes": "Lineage recovery cleanup is conservative locally; failed remote checkpoints are cleaned by andromeda/jobs/lineage_clean_failed.slurm after manifesting.",
    }
    path = LINEAGE_CLEANUP / f"local_cleanup_manifest_{timestamp}.txt"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = LINEAGE_CLEANUP / f"cleanup_summary_{timestamp}.md"
    summary.write_text(
        "\n".join(
            [
                "# Lineage Recovery Cleanup Summary",
                "",
                f"- Timestamp: `{timestamp}`",
                f"- Git commit: `{manifest['git_commit_before_cleanup']}`",
                "- Local cleanup was conservative because current Stage B and edit repair artifacts are remote-only and still needed.",
                "- Remote cleanup must preserve original Stage B and edit_repair_tiny until lineage recovery has a stronger candidate.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(path)
    print(summary)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("cleanup")
    sub.add_parser("train-stage-a")
    sub.add_parser("train-stage-b")
    sub.add_parser("verify-tree")
    sub.add_parser("scale-sweep")
    sub.add_parser("interpolation-sweep")
    sub.add_parser("build-edit-calibration")
    sub.add_parser("train-edit-calibration")
    sub.add_parser("build-mr-recovery")
    sub.add_parser("train-mr-recovery")
    sub.add_parser("task-vector-merge")
    sub.add_parser("probe-eval")
    sub.add_parser("full-eval")
    sub.add_parser("dashboard")
    sub.add_parser("clean-failed")
    sub.add_parser("package")
    args, extra = parser.parse_known_args()
    mapping = {
        "train-stage-a": [sys.executable, "scripts/train_lineage_recovery.py", "--config", "configs/train/lineage_recovery/sorbian_stage_a_dapt_preserve.yaml"],
        "train-stage-b": [sys.executable, "scripts/train_lineage_recovery.py", "--config", "configs/train/lineage_recovery/sorbian_stage_b_mt_preserve.yaml"],
        "verify-tree": [sys.executable, "scripts/lineage_verify_checkpoint_tree.py"],
        "scale-sweep": [sys.executable, "scripts/lineage_scale_sweep.py"],
        "interpolation-sweep": [sys.executable, "scripts/lineage_interpolate_models.py"],
        "build-edit-calibration": [sys.executable, "scripts/build_edit_calibration_set.py"],
        "train-edit-calibration": [sys.executable, "scripts/train_edit_calibration.py"],
        "build-mr-recovery": [sys.executable, "scripts/build_mr_recovery_set.py"],
        "train-mr-recovery": [sys.executable, "scripts/train_mr_recovery.py"],
        "task-vector-merge": [sys.executable, "scripts/lineage_task_vector_merge.py"],
        "probe-eval": [sys.executable, "scripts/lineage_scale_sweep.py"],
        "full-eval": [sys.executable, "scripts/lineage_full_eval_candidates.py"],
        "dashboard": [sys.executable, "scripts/lineage_compare_candidates.py"],
        "clean-failed": [sys.executable, "scripts/lineage_compare_candidates.py"],
        "package": [sys.executable, "scripts/lineage_package_candidate.py", "--model-dir", STAGE_B_MERGED, "--dry-run"],
    }
    if args.command == "status":
        return status()
    if args.command == "cleanup":
        return cleanup()
    return run([*mapping[args.command], *extra])


if __name__ == "__main__":
    raise SystemExit(main())
