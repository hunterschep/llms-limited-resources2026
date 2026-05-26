#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.train.mixed_objective import build_stage_rows, count_by, write_jsonl


def build_config(path: Path) -> dict:
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out_dir = ROOT / config["output_dir"]
    seed = int(config.get("seed", 2606))
    manifest = {"config": str(path.relative_to(ROOT)), "track": config["track"], "stages": {}}
    all_rows = []
    for name, stage in (config.get("stages") or {}).items():
        rows, source_manifest = build_stage_rows(stage, ROOT, seed)
        output = out_dir / stage["output"]
        write_jsonl(output, rows)
        all_rows.extend(rows)
        manifest["stages"][name] = {
            "output": str(output.relative_to(ROOT)),
            "rows": len(rows),
            "by_task": count_by(rows, "task"),
            "by_source_id": count_by(rows, "source_id"),
            "sources": source_manifest,
        }
    all_path = out_dir / "stagewise_all.jsonl"
    write_jsonl(all_path, all_rows)
    manifest["stagewise_all"] = {"output": str(all_path.relative_to(ROOT)), "rows": len(all_rows)}
    manifest_track = "uk" if config["track"] == "ukrainian" else config["track"]
    manifest_path = ROOT / "data/manifests" / f"competitive_mixture_{manifest_track}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=["uk", "sorbian", "all"], default="all")
    parser.add_argument("--skip-final-rebuild", action="store_true")
    args = parser.parse_args()
    if not args.skip_final_rebuild:
        subprocess.run([sys.executable, "scripts/build_external_training_sets.py"], cwd=ROOT, check=True)
    paths = []
    if args.track in {"uk", "all"}:
        paths.append(ROOT / "configs/data/competitive_mixture_uk.yaml")
    if args.track in {"sorbian", "all"}:
        paths.append(ROOT / "configs/data/competitive_mixture_sorbian.yaml")
    summaries = [build_config(path) for path in paths]
    out = ROOT / "results/competitive_reboot/data/mixture_build_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summaries, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
