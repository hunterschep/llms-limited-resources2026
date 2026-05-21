#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/data/local_splits.yaml"
MANIFEST = ROOT / "data/manifests/local_split_manifest.jsonl"


def stable_fraction(seed: int, key: str) -> float:
    digest = hashlib.sha256(f"{seed}:{key}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) / float(16**16)


def iter_rows(path: Path) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    if path.suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for idx, line in enumerate(handle):
                if not line.strip():
                    continue
                row = json.loads(line)
                row_id = (
                    row.get("sent_id")
                    or row.get("question_id")
                    or row.get("id")
                    or f"row-{idx:06d}"
                )
                rows.append((str(row_id), row))
    elif path.suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for idx, row in enumerate(reader):
                rows.append((str(row.get("id") or f"row-{idx:06d}"), dict(row)))
    return rows


def infer_split_type(path: Path) -> str:
    name = path.name
    if "train" in name:
        return "train"
    if "monolingual" in name:
        return "train"
    if "dev" in name:
        return "dev"
    return "unknown"


def task_for(path: Path) -> str:
    return path.parts[1] if len(path.parts) > 1 else "unknown"


def track_for(path: Path) -> str:
    return "ukrainian" if path.parts[0] == "Ukrainian" else "sorbian"


def split_for(path: Path, row_id: str, row_count: int, config: dict[str, Any]) -> str:
    split_type = infer_split_type(path)
    if split_type == "train":
        return "train"
    if split_type != "dev":
        return "tune"
    task = task_for(path)
    if task == "MR":
        return "locked_validation"
    seed = int(config.get("seed", 2606))
    ratio = float(config.get("large_dev_tune_ratio", 0.70))
    small_threshold = int(config.get("small_dev_threshold", 300))
    if row_count <= small_threshold:
        ratio = float(config.get("small_dev_tune_ratio", 0.50))
    fraction = stable_fraction(seed, f"{path.as_posix()}:{row_id}")
    return "tune" if fraction < ratio else "locked_validation"


def build_manifest(config: dict[str, Any]) -> list[dict[str, Any]]:
    data_paths = sorted(
        [p for p in (ROOT / "Ukrainian").glob("*/*.*") if p.suffix in {".jsonl", ".csv"}]
        + [p for p in (ROOT / "Sorbian").glob("*/*.*") if p.suffix in {".jsonl", ".csv"}]
    )
    rows_out: list[dict[str, Any]] = []
    for path in data_paths:
        rel = path.relative_to(ROOT)
        if infer_split_type(rel) != "dev":
            continue
        source_rows = iter_rows(path)
        row_count = len(source_rows)
        for row_idx, (row_id, _row) in enumerate(source_rows):
            split = split_for(rel, row_id, row_count, config)
            rows_out.append(
                {
                    "relative_path": rel.as_posix(),
                    "track": track_for(rel),
                    "task": task_for(rel),
                    "row_index": row_idx,
                    "row_id": row_id,
                    "split": split,
                    "policy": "official_train" if infer_split_type(rel) == "train" else "official_dev_split",
                    "seed": config.get("seed", 2606),
                }
            )
    return rows_out


def main() -> int:
    if not CONFIG.exists():
        print(f"Missing split config: {CONFIG}", file=sys.stderr)
        return 2
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    rows = build_manifest(config)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Wrote {len(rows)} split rows to {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
