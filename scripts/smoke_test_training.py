#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(
        [
            "python3",
            "scripts/train_sft.py",
            "--config",
            "configs/train/uk/qa.yaml",
            "--dry-run",
            "--max-examples",
            "2",
        ],
        cwd=ROOT,
        check=True,
    )
    marker = ROOT / "checkpoints/uk/specialists/qa/DRY_RUN.json"
    if not marker.exists():
        raise SystemExit("Training dry-run marker was not created.")
    print("Training smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
