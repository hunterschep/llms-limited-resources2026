from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: str | Path, limit: int | None = None) -> list[dict]:
    rows: list[dict] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
                if limit and len(rows) >= limit:
                    break
    return rows


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> int:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def read_yaml(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def write_yaml(path: str | Path, data: dict) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def write_json(path: str | Path, data: dict) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_eval_result(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def task_score_vector(result: dict) -> dict[str, float]:
    aggregate = result.get("aggregate", {})
    return {
        "MT": float(aggregate.get("MT_score", 0.0) or 0.0),
        "QA": float(aggregate.get("QA_score", 0.0) or 0.0),
        "SC": float(aggregate.get("SC_score", 0.0) or 0.0),
        "GC": float(aggregate.get("GC_score", 0.0) or 0.0),
        "MR": float(aggregate.get("MR_score", 0.0) or 0.0),
        "overall": float(aggregate.get("overall_score", 0.0) or 0.0),
    }


def git_revision() -> str:
    env_rev = os.environ.get("WMT26_GIT_COMMIT") or os.environ.get("WMT26_RUN_REVISION")
    if env_rev:
        return env_rev
    rev_file = ROOT / "REVISION"
    if rev_file.exists():
        text = rev_file.read_text(encoding="utf-8").strip()
        if text:
            return text
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)
