#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", required=True)
    args = parser.parse_args()
    return subprocess.call([sys.executable, "scripts/competitive_validate_package.py", "--model-dir", args.package_dir], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
