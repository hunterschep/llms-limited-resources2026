#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys


COMMANDS = {
    "scgc-audit": [sys.executable, "scripts/final_salvage_scgc_audit.py"],
    "prompt-sweep": [sys.executable, "scripts/final_salvage_scgc_prompt_sweep.py"],
    "build-calibration-data": [sys.executable, "scripts/build_final_scgc_calibration_data.py"],
    "train-calibration": [sys.executable, "scripts/train_final_scgc_calibration.py"],
    "merge-calibration": [sys.executable, "scripts/merge_final_scgc_calibration.py"],
    "eval": [sys.executable, "scripts/final_salvage_eval_candidates.py"],
    "validate-package": [sys.executable, "scripts/final_salvage_validate_package.py"],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("args", nargs="*")
    ns = parser.parse_args()
    return subprocess.call(COMMANDS[ns.command] + ns.args)


if __name__ == "__main__":
    raise SystemExit(main())
