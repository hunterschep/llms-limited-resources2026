#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
STAGE_B_CHECKPOINT = "/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
STAGE_B_REL_CHECKPOINT = "checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
COMPETITIVE_EVAL_DIR = ROOT / "results/competitive_reboot/eval/sorbian"
STAGE_B_RESCUE_DIR = ROOT / "results/stage_b_rescue"
ERROR_ANALYSIS_DIR = STAGE_B_RESCUE_DIR / "error_analysis"
RAW_INPUT_DIR = ERROR_ANALYSIS_DIR / "raw_inputs"
PROCESSED_REPAIR_DIR = ROOT / "data/processed/stage_b_rescue/sorbian"
STAGE_B_MODELS = ("prompt_only_qwen35_2b", "stage_b_mt_large", "stage_c_instruction_replay")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        rev = ROOT / "REVISION"
        return rev.read_text(encoding="utf-8").strip() if rev.exists() else "unknown"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
                if limit and len(rows) >= limit:
                    break
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validation_path(task: str) -> Path:
    return ROOT / f"data/processed/sorbian/{task.lower()}_locked_validation.jsonl"


def load_validation_by_task() -> dict[str, list[dict[str, Any]]]:
    return {task: read_jsonl(validation_path(task)) for task in ("MT", "QA", "SC", "GC", "MR")}


def raw_path(model_name: str) -> Path:
    candidates = [
        RAW_INPUT_DIR / f"{model_name}_raw.jsonl",
        COMPETITIVE_EVAL_DIR / f"{model_name}_raw.jsonl",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def load_raw_predictions(model_name: str) -> dict[tuple[str, str], dict[str, Any]]:
    path = raw_path(model_name)
    rows = read_jsonl(path)
    return {(str(row.get("task")), str(row.get("id"))): row for row in rows}


def load_eval_result(model_name: str) -> dict[str, Any]:
    path = COMPETITIVE_EVAL_DIR / f"{model_name}.json"
    if not path.exists():
        path = STAGE_B_RESCUE_DIR / "full_eval" / f"{model_name}.json"
    return read_json(path) if path.exists() else {}


def direction(row: dict[str, Any]) -> str:
    metadata = row.get("metadata") or {}
    if metadata.get("direction"):
        return str(metadata["direction"])
    src = row.get("source_language") or metadata.get("source_language") or "unknown"
    tgt = row.get("target_language") or metadata.get("target_language") or row.get("language") or "unknown"
    return f"{src}->{tgt}"


def prompt_text(row: dict[str, Any]) -> str:
    messages = row.get("messages") or []
    if messages:
        return "\n".join(str(m.get("content", "")).strip() for m in messages if m.get("role") != "assistant").strip()
    return str(row.get("input", "")).strip()


def target_text(row: dict[str, Any]) -> str:
    return str(row.get("target", "")).strip()


def assistant_row(row: dict[str, Any], content: str) -> dict[str, Any]:
    new_row = dict(row)
    messages = [dict(m) for m in row.get("messages", []) if m.get("role") != "assistant"]
    messages.append({"role": "assistant", "content": content})
    new_row["messages"] = messages
    new_row["target"] = content
    return new_row


def deterministic_sample(rows: list[dict[str, Any]], limit: int, seed: int) -> list[dict[str, Any]]:
    selected = list(rows)
    random.Random(seed).shuffle(selected)
    return selected[: min(limit, len(selected))]


def grouped_sample(rows: list[dict[str, Any]], key: str, total_limit: int, seed: int) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        value = row.get(key)
        if key == "direction":
            value = direction(row)
        buckets[str(value)].append(row)
    if not buckets:
        return []
    per_bucket = max(1, total_limit // len(buckets))
    rng = random.Random(seed)
    selected: list[dict[str, Any]] = []
    for _, bucket in sorted(buckets.items()):
        copy = list(bucket)
        rng.shuffle(copy)
        selected.extend(copy[:per_bucket])
    if len(selected) < total_limit:
        remaining = [row for row in rows if row not in selected]
        rng.shuffle(remaining)
        selected.extend(remaining[: total_limit - len(selected)])
    rng.shuffle(selected)
    return selected[:total_limit]


def count_by(rows: Iterable[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field, "unknown")) for row in rows).items()))


def numeric_like(value: str) -> bool:
    return bool(re.search(r"[-+]?\d", str(value)))


def compact_score_table(paths: list[Path]) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        if not path.exists():
            continue
        result = read_json(path)
        aggregate = result.get("aggregate") or {}
        rows.append(
            {
                "path": rel(path),
                "model": path.stem,
                "overall": aggregate.get("overall_score"),
                "MT": aggregate.get("MT_score"),
                "QA": aggregate.get("QA_score"),
                "SC": aggregate.get("SC_score"),
                "GC": aggregate.get("GC_score"),
                "MR": aggregate.get("MR_score"),
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        cells = []
        for column in columns:
            value = row.get(column, "")
            if isinstance(value, float):
                cells.append(f"{value:.3f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def ensure_not_failed_stage_c(path_or_config: str) -> None:
    lowered = path_or_config.lower()
    if "stage_c_instruction_replay" in lowered and "diagnostic" not in lowered:
        raise SystemExit("Refusing to use failed Stage C replay as a training base or candidate.")
