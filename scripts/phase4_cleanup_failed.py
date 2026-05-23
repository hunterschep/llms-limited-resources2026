#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _prune_empty_dirs(path: Path, stop: Path) -> list[str]:
    removed: list[str] = []
    current = path
    while current != stop and current.exists():
        try:
            current.rmdir()
        except OSError:
            break
        removed.append(str(current.relative_to(ROOT)))
        current = current.parent
    return removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default="results/phase4/cleanup/phase4_cleanup_manifest_local.json")
    args = parser.parse_args()
    dir_candidates: set[Path] = set()
    file_candidates: set[Path] = set()
    checkpoints = ROOT / "checkpoints"
    if checkpoints.exists():
        for marker in checkpoints.glob("**/DRY_RUN.json"):
            dir_candidates.add(marker.parent)
        for marker in checkpoints.glob("**/MERGE_DRY_RUN.json"):
            dir_candidates.add(marker.parent)
        for marker in checkpoints.glob("**/SKIPPED.json"):
            dir_candidates.add(marker.parent)
        for file_path in checkpoints.glob("**/merged/search/candidate_weights.jsonl"):
            file_candidates.add(file_path)
    for root in [ROOT / "checkpoints/phase4"]:
        if root.exists():
            for marker in root.glob("**/DRY_RUN.json"):
                dir_candidates.add(marker.parent)
    deleted_dirs = []
    deleted_files = []
    pruned_dirs = []
    for path in sorted(dir_candidates):
        deleted_dirs.append(str(path.relative_to(ROOT)))
        if not args.dry_run:
            shutil.rmtree(path)
    for path in sorted(file_candidates):
        deleted_files.append(str(path.relative_to(ROOT)))
        if not args.dry_run and path.exists():
            path.unlink()
            pruned_dirs.extend(_prune_empty_dirs(path.parent, checkpoints))
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "dry_run": args.dry_run,
        "deleted_dirs_or_would_delete": deleted_dirs,
        "deleted_files_or_would_delete": deleted_files,
        "pruned_empty_dirs": pruned_dirs,
    }
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(out),
                "deleted_dirs": len(deleted_dirs),
                "deleted_files": len(deleted_files),
                "dry_run": args.dry_run,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
