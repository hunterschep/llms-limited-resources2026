#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def revision() -> str:
    env_rev = os.environ.get("WMT26_GIT_COMMIT", "").strip()
    if env_rev:
        return env_rev
    rev_file = ROOT / "REVISION"
    if rev_file.exists():
        text = rev_file.read_text(encoding="utf-8").strip()
        if text:
            return text
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-name", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--checkpoint-path", default="")
    parser.add_argument("--result-path", default="")
    args = parser.parse_args()

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    checksums = {}
    for rel in args.path:
        checksums[rel] = sha256(ROOT / rel)
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "job_name": args.job_name,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID", "local"),
        "git_commit": revision(),
        "project_root": str(ROOT),
        "scratch_root": os.environ.get("SCRATCH_ROOT", ""),
        "checkpoint_path": args.checkpoint_path,
        "result_path": args.result_path,
        "checksums": checksums,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "git_commit": payload["git_commit"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
