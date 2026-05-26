from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)


def stable_sample(rows: list[dict[str, Any]], cap: int | None, seed: int, key: str) -> list[dict[str, Any]]:
    selected = list(rows)
    random.Random(f"{seed}:{key}").shuffle(selected)
    if cap is not None:
        selected = selected[: max(0, int(cap))]
    return selected


def weighted_expand(rows: list[dict[str, Any]], weight: float) -> list[dict[str, Any]]:
    if weight <= 0:
        return []
    whole = int(weight)
    fraction = weight - whole
    expanded = []
    for _ in range(max(1, whole)):
        expanded.extend(rows)
    if fraction > 0:
        keep = int(round(len(rows) * fraction))
        expanded.extend(rows[:keep])
    return expanded


def build_stage_rows(stage: dict[str, Any], root: Path, seed: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    for source in stage.get("sources", []) or []:
        rel = str(source["path"])
        path = root / rel
        raw = read_jsonl(path)
        sampled = stable_sample(raw, source.get("cap"), seed, rel)
        weighted = weighted_expand(sampled, float(source.get("weight", 1.0)))
        rows.extend(weighted)
        manifest.append(
            {
                "path": rel,
                "task": source.get("task"),
                "raw_rows": len(raw),
                "sampled_rows": len(sampled),
                "weight": float(source.get("weight", 1.0)),
                "emitted_rows": len(weighted),
            }
        )
    random.Random(seed).shuffle(rows)
    return rows, manifest


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "UNKNOWN")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))
