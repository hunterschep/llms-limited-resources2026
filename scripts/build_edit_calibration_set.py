#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import git_commit, read_jsonl, sha256_path, write_json, write_jsonl  # noqa: E402


def _load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _ensure_stage_b_repair(config: dict[str, Any]) -> None:
    subprocess.run([sys.executable, "scripts/build_stage_b_repair_data.py", "--config", config["sources"]["stage_b_repair_config"]], cwd=ROOT, check=True)


def _is_clean(row: dict[str, Any]) -> bool:
    target = str(row.get("target", ""))
    metadata = row.get("metadata") or {}
    return bool(metadata.get("clean_no_error")) or "Wrong word: CORRECT" in target and "Correct word: CORRECT" in target


def _stamp(row: dict[str, Any], method: str) -> dict[str, Any]:
    new = dict(row)
    new["split"] = "train"
    new["track"] = "sorbian"
    new["contamination_checked"] = True
    new["generation_method"] = method
    metadata = dict(new.get("metadata") or {})
    metadata["lineage_recovery"] = True
    metadata["edit_calibration"] = True
    new["metadata"] = metadata
    return new


def _summary(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "rows": len(rows),
        "sha256": sha256_path(path),
        "by_task": dict(Counter(str(row.get("task", "unknown")) for row in rows)),
        "clean_rows": sum(1 for row in rows if _is_clean(row)),
        "error_rows": sum(1 for row in rows if not _is_clean(row)),
        "by_source_id_top20": dict(Counter(str(row.get("source_id", "unknown")) for row in rows).most_common(20)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data/edit_calibration_sorbian.yaml")
    args = parser.parse_args()
    config = _load(ROOT / args.config)
    _ensure_stage_b_repair(config)
    rng = random.Random(int(config.get("seed", 2631)))
    edit_rows = [_stamp(row, "lineage_edit_calibration_source") for row in read_jsonl(ROOT / config["sources"]["edit_repair"])]
    clean = [row for row in edit_rows if _is_clean(row)]
    errors = [row for row in edit_rows if not _is_clean(row)]
    rng.shuffle(clean)
    rng.shuffle(errors)
    out_root = ROOT / config["outputs"]["root"]
    out_root.mkdir(parents=True, exist_ok=True)
    manifest_outputs: dict[str, Any] = {}
    total = int(config["limits"]["total_examples_per_ratio"])
    for name, ratio in config.get("ratios", {}).items():
        clean_n = min(len(clean), int(round(total * float(ratio["clean"]))))
        error_n = min(len(errors), total - clean_n)
        rows = clean[:clean_n] + errors[:error_n]
        rng.shuffle(rows)
        path = out_root / f"{name}.jsonl"
        write_jsonl(path, rows)
        manifest_outputs[name] = _summary(path, rows)
    format_rows = [_stamp(row, "lineage_edit_format_repair") for row in read_jsonl(ROOT / config["sources"]["format_repair"])]
    rng.shuffle(format_rows)
    format_path = out_root / "format_repair.jsonl"
    write_jsonl(format_path, format_rows[: int(config["limits"]["format_examples"])])
    manifest_outputs["format_repair"] = _summary(format_path, read_jsonl(format_path))
    mt_rows = [_stamp(row, "lineage_edit_mt_anchor_replay") for row in read_jsonl(ROOT / config["sources"]["mt_anchor"])]
    rng.shuffle(mt_rows)
    mt_path = out_root / "mt_anchor.jsonl"
    write_jsonl(mt_path, mt_rows[: int(config["limits"]["mt_anchor_examples"])])
    manifest_outputs["mt_anchor"] = _summary(mt_path, read_jsonl(mt_path))
    manifest = {
        "config": args.config,
        "git_commit": git_commit(),
        "policy": config.get("policy", {}),
        "outputs": manifest_outputs,
    }
    write_json(ROOT / "data/manifests/lineage_edit_calibration_sorbian.json", manifest)
    write_json(ROOT / "results/lineage_recovery/status/edit_calibration_manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
