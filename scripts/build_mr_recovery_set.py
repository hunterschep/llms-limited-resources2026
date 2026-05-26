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
    needed = [ROOT / config["sources"]["mr_repair"], ROOT / config["sources"]["mt_anchor"]]
    if all(path.exists() for path in needed):
        return
    subprocess.run([sys.executable, "scripts/build_stage_b_repair_data.py", "--config", config["sources"]["stage_b_repair_config"]], cwd=ROOT, check=True)


def _stamp(row: dict[str, Any], method: str) -> dict[str, Any]:
    new = dict(row)
    new["split"] = "train"
    new["track"] = "sorbian"
    new["contamination_checked"] = True
    new["generation_method"] = method
    metadata = dict(new.get("metadata") or {})
    metadata["lineage_recovery"] = True
    metadata["mr_recovery"] = True
    new["metadata"] = metadata
    return new


def _summary(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "rows": len(rows),
        "sha256": sha256_path(path),
        "by_task": dict(Counter(str(row.get("task", "unknown")) for row in rows)),
        "by_source_id_top20": dict(Counter(str(row.get("source_id", "unknown")) for row in rows).most_common(20)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data/mr_recovery_sorbian.yaml")
    args = parser.parse_args()
    config = _load(ROOT / args.config)
    _ensure_stage_b_repair(config)
    rng = random.Random(int(config.get("seed", 2641)))
    out_root = ROOT / config["outputs"]["root"]
    out_root.mkdir(parents=True, exist_ok=True)
    mr_rows = [_stamp(row, "lineage_mr_final_answer_recovery") for row in read_jsonl(ROOT / config["sources"]["mr_repair"])]
    rng.shuffle(mr_rows)
    mr_rows = mr_rows[: int(config["limits"]["mr_examples"])]
    mr_path = out_root / "mr_final_answer.jsonl"
    write_jsonl(mr_path, mr_rows)
    mt_rows = [_stamp(row, "lineage_mr_mt_anchor_replay") for row in read_jsonl(ROOT / config["sources"]["mt_anchor"])]
    rng.shuffle(mt_rows)
    mt_rows = mt_rows[: int(config["limits"]["mt_anchor_examples"])]
    mt_path = out_root / "mt_anchor.jsonl"
    write_jsonl(mt_path, mt_rows)
    manifest = {
        "config": args.config,
        "git_commit": git_commit(),
        "policy": config.get("policy", {}),
        "outputs": {
            "mr_final_answer": _summary(mr_path, mr_rows),
            "mt_anchor": _summary(mt_path, mt_rows),
        },
    }
    write_json(ROOT / "data/manifests/lineage_mr_recovery_sorbian.json", manifest)
    write_json(ROOT / "results/lineage_recovery/status/mr_recovery_manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
