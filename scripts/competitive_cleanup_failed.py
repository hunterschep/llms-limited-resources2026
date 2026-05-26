#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--root", default="checkpoints/competitive_reboot")
    args = parser.parse_args()
    root = ROOT / args.root
    removed = []
    if root.exists():
        for marker in root.rglob("DRY_RUN.json"):
            checkpoint_dir = marker.parent
            removed.append(str(checkpoint_dir.relative_to(ROOT)))
            if args.execute:
                shutil.rmtree(checkpoint_dir)
        for marker in root.rglob("MERGE_DRY_RUN.json"):
            checkpoint_dir = marker.parent
            removed.append(str(checkpoint_dir.relative_to(ROOT)))
            if args.execute:
                shutil.rmtree(checkpoint_dir)
        for marker in root.rglob("SKIPPED.json"):
            checkpoint_dir = marker.parent
            removed.append(str(checkpoint_dir.relative_to(ROOT)))
            if args.execute:
                shutil.rmtree(checkpoint_dir)
        for marker in root.rglob("candidate_weights.jsonl"):
            if "merged/search" in marker.as_posix():
                checkpoint_dir = marker.parent
                removed.append(str(checkpoint_dir.relative_to(ROOT)))
                if args.execute:
                    shutil.rmtree(checkpoint_dir)
        if args.execute:
            for directory in sorted(root.rglob("*"), reverse=True):
                if directory.is_dir():
                    try:
                        directory.rmdir()
                    except OSError:
                        pass
            try:
                root.rmdir()
            except OSError:
                pass
    out = ROOT / "results/competitive_reboot/cleanup/local_failed_checkpoint_cleanup.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"execute": args.execute, "removed_or_would_remove": removed}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
