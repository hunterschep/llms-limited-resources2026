#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        ["python3", "scripts/eval_model.py", "--config", "configs/eval/uk.yaml", "--oracle", "--limit", "2"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        ["python3", "scripts/eval_model.py", "--config", "configs/eval/sorbian.yaml", "--oracle", "--limit", "2"],
        cwd=ROOT,
        check=True,
    )
    print("Evaluation smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
