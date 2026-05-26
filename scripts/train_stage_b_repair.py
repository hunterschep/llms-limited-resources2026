#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from stage_b_rescue_common import STAGE_B_REL_CHECKPOINT, ensure_not_failed_stage_c  # noqa: E402
from wmt26.train.config import load_yaml  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-examples", type=int, default=None)
    args = parser.parse_args()
    config = load_yaml(ROOT / args.config)
    base = str(config.get("base_model_path", ""))
    ensure_not_failed_stage_c(base)
    if STAGE_B_REL_CHECKPOINT not in base and "competitive_reboot/sorbian/stage_b_mt_large" not in base:
        raise SystemExit(f"Stage-B repair must train from Stage B, got base_model_path={base!r}")
    env = dict(os.environ)
    env.setdefault("WMT26_STAGE_B_RESCUE", "1")
    command = [sys.executable, "scripts/train_sft.py", "--config", args.config]
    if args.dry_run:
        command.append("--dry-run")
    if args.max_examples is not None:
        command.extend(["--max-examples", str(args.max_examples)])
    return subprocess.call(command, cwd=ROOT, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
