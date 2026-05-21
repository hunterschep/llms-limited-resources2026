#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data/external_sources.yaml")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    enabled = [s for s in config.get("sources", []) if s.get("enabled")]
    if not enabled:
        print("No external sources are enabled. Register and approve sources before downloading.")
        return 0
    if not args.execute:
        for source in enabled:
            print(f"DRY-RUN would download {source['source_id']} from {source['source_url']}")
        return 0
    raise NotImplementedError("External downloads require per-source commands after governance approval.")


if __name__ == "__main__":
    raise SystemExit(main())
