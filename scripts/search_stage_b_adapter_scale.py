#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    return subprocess.call([sys.executable, "scripts/stage_b_scale_sweep.py", *sys.argv[1:]], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
