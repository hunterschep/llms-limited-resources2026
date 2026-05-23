#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = {
    "status": ["git", "status", "--short"],
    "cleanup-check": [sys.executable, "scripts/phase4_cleanup_check.py"],
    "build-probe": [sys.executable, "scripts/build_phase4_probe_suite.py"],
    "eval-prompt-only": [sys.executable, "scripts/eval_phase4_probe.py"],
    "prompt-sweep": [sys.executable, "scripts/phase4_prompt_sweep.py"],
    "analyze-failures": [sys.executable, "scripts/phase4_analyze_failures.py"],
    "micro-ablation": [sys.executable, "scripts/phase4_run_micro_ablations.py"],
    "rank-candidates": [sys.executable, "scripts/phase4_rank_ablation_candidates.py"],
    "check-gates": [sys.executable, "scripts/phase4_check_no_harm_gates.py"],
    "eval-gated": [sys.executable, "scripts/phase4_eval_gated_candidates.py"],
    "report": [sys.executable, "scripts/phase4_report.py"],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand", choices=sorted(COMMANDS))
    args, rest = parser.parse_known_args()
    return subprocess.run(COMMANDS[args.subcommand] + rest, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
