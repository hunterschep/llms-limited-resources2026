#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    args = parser.parse_args()
    model_dir = Path(args.model_dir)
    missing = [name for name in ("config.json",) if not (model_dir / name).exists()]
    if missing:
        raise SystemExit(f"Missing package files in {model_dir}: {missing}")
    print(f"Package validation passed: {model_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
