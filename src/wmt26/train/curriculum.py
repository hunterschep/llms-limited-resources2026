from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from wmt26.train.config import load_yaml


INVALID_CHECKPOINT_TOKENS = ("phase3", "phase4", "archive_failed_phase3_phase4")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_competitive_paths(config: dict[str, Any]) -> None:
    for field in ("output_dir", "base_model_path"):
        value = str(config.get(field) or "")
        if not value:
            continue
        lowered = value.lower()
        if any(token in lowered for token in INVALID_CHECKPOINT_TOKENS):
            raise ValueError(f"Competitive config must not reference failed checkpoint path in {field}: {value}")
    for rel in config.get("train_files", []) or []:
        lowered = str(rel).lower()
        if "results/archive_failed_phase3_phase4" in lowered:
            raise ValueError(f"Competitive training file points into failed archive: {rel}")


def load_stage_configs(path: Path) -> list[tuple[str, Path, dict[str, Any]]]:
    config = load_yaml(path)
    stages = []
    for stage in config.get("stages", []) or []:
        stage_path = path.parents[2] / str(stage["config"]) if not Path(stage["config"]).is_absolute() else Path(stage["config"])
        if not stage_path.exists():
            stage_path = Path.cwd() / str(stage["config"])
        stage_config = load_yaml(stage_path)
        validate_competitive_paths(stage_config)
        stages.append((str(stage["name"]), stage_path, stage_config))
    return stages


def write_stage_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
