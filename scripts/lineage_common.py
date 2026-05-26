#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
LINEAGE_RESULTS = ROOT / "results/lineage_recovery"
LINEAGE_STATUS = LINEAGE_RESULTS / "status"
LINEAGE_CLEANUP = LINEAGE_RESULTS / "cleanup"
LINEAGE_EVAL = LINEAGE_RESULTS / "eval"
LINEAGE_PROBE = LINEAGE_RESULTS / "probe_eval"
LINEAGE_SWEEP = LINEAGE_RESULTS / "scale_sweep"
LINEAGE_MERGE = LINEAGE_RESULTS / "merge"

PROMPT_ONLY_RESULT = ROOT / "results/competitive_reboot/eval/sorbian/prompt_only_qwen35_2b.json"
ORIGINAL_STAGE_B_RESULT = ROOT / "results/competitive_reboot/eval/sorbian/stage_b_mt_large.json"
EDIT_REPAIR_RESULT = ROOT / "results/stage_b_rescue/full_eval/edit_repair_tiny.json"

SCRATCH_ROOT = os.environ.get("SCRATCH_ROOT", "/scratch/scheppat/projects/wmt26_lrllm")
LINEAGE_REMOTE_ROOT = f"{SCRATCH_ROOT}/checkpoints/lineage_recovery/sorbian"
STAGE_A_PARENT = f"{LINEAGE_REMOTE_ROOT}/stage_a_dapt_parent/final_merged"
STAGE_A_ADAPTER = f"{LINEAGE_REMOTE_ROOT}/stage_a_dapt_adapter/final_adapter"
STAGE_B_ADAPTER = f"{LINEAGE_REMOTE_ROOT}/stage_b_mt/final_adapter"
STAGE_B_MERGED = f"{LINEAGE_REMOTE_ROOT}/stage_b_mt/final_merged"
ORIGINAL_STAGE_B = f"{SCRATCH_ROOT}/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
EDIT_REPAIR_TINY = f"{SCRATCH_ROOT}/checkpoints/stage_b_rescue/sorbian/edit_repair_tiny"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def git_commit() -> str:
    if os.environ.get("WMT26_RUN_REVISION"):
        return str(os.environ["WMT26_RUN_REVISION"]).strip()
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        pass
    rev_file = ROOT / "REVISION"
    if rev_file.exists():
        value = rev_file.read_text(encoding="utf-8").strip()
        if value:
            return value
    return "unknown"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_local_or_scratch(path: str) -> Path:
    expanded = os.path.expandvars(path)
    candidate = Path(expanded)
    if candidate.is_absolute():
        return candidate
    if candidate.parts and candidate.parts[0] == "checkpoints":
        return Path(SCRATCH_ROOT) / candidate
    return ROOT / candidate


def aggregate_row(name: str, path: Path, decision: str = "") -> dict[str, Any]:
    if not path.exists():
        return {"model": name, "path": str(path), "exists": False, "decision": decision}
    result = read_json(path)
    aggregate = result.get("aggregate") or {}
    return {
        "model": name,
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "exists": True,
        "overall": aggregate.get("overall_score"),
        "MT": aggregate.get("MT_score"),
        "QA": aggregate.get("QA_score"),
        "SC": aggregate.get("SC_score"),
        "GC": aggregate.get("GC_score"),
        "MR": aggregate.get("MR_score"),
        "decision": decision,
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        cells: list[str] = []
        for column in columns:
            value = row.get(column, "")
            if isinstance(value, float):
                cells.append(f"{value:.3f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def refuse_bad_reference(text: str) -> None:
    lowered = text.lower()
    bad = ["stage_c_instruction_replay", "checkpoints/phase3", "checkpoints/phase4", "results/phase3", "results/phase4"]
    for marker in bad:
        if marker in lowered:
            raise SystemExit(f"Refusing forbidden lineage reference: {marker}")
