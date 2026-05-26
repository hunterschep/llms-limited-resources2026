#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_b_rescue_common import STAGE_B_CHECKPOINT, git_commit, write_json  # noqa: E402


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print("+ " + " ".join(command), flush=True)
    return subprocess.run(command, cwd=ROOT, check=check, text=True)


def status() -> int:
    data = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "stage_b_checkpoint": STAGE_B_CHECKPOINT,
        "local_git_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
        "stage_b_results": {
            "prompt_only": "results/competitive_reboot/eval/sorbian/prompt_only_qwen35_2b.json",
            "stage_b": "results/competitive_reboot/eval/sorbian/stage_b_mt_large.json",
            "stage_c_diagnostic": "results/competitive_reboot/eval/sorbian/stage_c_instruction_replay.json",
        },
    }
    write_json(ROOT / "results/stage_b_rescue/status/local_status.json", data)
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def cleanup() -> int:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cleanup_dir = ROOT / "results/stage_b_rescue/cleanup"
    cleanup_dir.mkdir(parents=True, exist_ok=True)
    deleted: list[str] = []
    archived: list[str] = []
    preserved = [
        STAGE_B_CHECKPOINT,
        "results/competitive_reboot/eval/sorbian/prompt_only_qwen35_2b.json",
        "results/competitive_reboot/eval/sorbian/stage_b_mt_large.json",
        "results/competitive_reboot/comparisons/sorbian_stage_b_direction_breakdown.md",
        "docs/80_competitive_reboot_results_and_decision.md",
    ]
    for rel in ["checkpoints"]:
        path = ROOT / rel
        if path.exists():
            for child in sorted(path.rglob("*"), reverse=True):
                if child.is_file() and child.name != ".gitkeep":
                    child.unlink()
                    deleted.append(str(child.relative_to(ROOT)))
                elif child.is_dir():
                    try:
                        child.rmdir()
                    except OSError:
                        pass
    for rel in ["results/phase4", "results/phase3_fixed", "results/triage"]:
        path = ROOT / rel
        if path.exists():
            archive = ROOT / "results/archive_failed_phase3_phase4" / path.name
            archive.parent.mkdir(parents=True, exist_ok=True)
            if archive.exists():
                shutil.rmtree(archive)
            shutil.move(str(path), str(archive))
            archived.append(f"{rel} -> {archive.relative_to(ROOT)}")
    manifest = {
        "timestamp": timestamp,
        "git_commit_before_cleanup": git_commit(),
        "local_files_deleted": deleted,
        "local_paths_archived": archived,
        "preserved": preserved,
        "notes": "Remote cleanup is recorded separately with the Andromeda manifest.",
    }
    manifest_path = cleanup_dir / f"local_cleanup_manifest_{timestamp}.txt"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary_path = cleanup_dir / f"cleanup_summary_{timestamp}.md"
    summary_path.write_text(
        "\n".join(
            [
                "# Stage B Rescue Cleanup Summary",
                "",
                f"- Timestamp: `{timestamp}`",
                f"- Git commit: `{manifest['git_commit_before_cleanup']}`",
                f"- Local files deleted: `{len(deleted)}`",
                f"- Local paths archived: `{len(archived)}`",
                "- Stage B checkpoint preserved on Andromeda.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {manifest_path}")
    print(f"Wrote {summary_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("cleanup")
    sub.add_parser("error-analysis")
    sub.add_parser("build-repair-data")
    sub.add_parser("build-probe")
    sub.add_parser("prompt-sweep")
    sub.add_parser("scale-sweep")
    args, extra = parser.parse_known_args()
    if args.command == "status":
        return status()
    if args.command == "cleanup":
        return cleanup()
    mapping = {
        "error-analysis": ["scripts/stage_b_error_analysis.py"],
        "build-repair-data": ["scripts/build_stage_b_repair_data.py"],
        "build-probe": ["scripts/build_stage_b_rescue_probe.py"],
        "prompt-sweep": ["scripts/stage_b_prompt_sweep.py"],
        "scale-sweep": ["scripts/stage_b_scale_sweep.py"],
    }
    return run([sys.executable, *mapping[args.command], *extra]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
