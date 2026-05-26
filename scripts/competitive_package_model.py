#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=["uk", "sorbian"], required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    model_dir = Path(args.model_dir)
    if not model_dir.is_absolute():
        scratch = Path("/scratch/scheppat/projects/wmt26_lrllm")
        model_dir = scratch / model_dir
    manifest = {
        "track": args.track,
        "model_dir": str(model_dir),
        "dry_run": args.dry_run,
        "required_files_checked": ["config.json", "tokenizer_config.json"],
        "status": "dry_run_only" if args.dry_run else "ready_for_local_copy",
    }
    out = ROOT / args.output_dir / f"{args.track}_package_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
