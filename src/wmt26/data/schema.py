from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


REQUIRED_FIELDS = {
    "id",
    "track",
    "task",
    "language",
    "input",
    "target",
    "messages",
    "source_id",
    "source_type",
    "license",
    "split",
    "is_synthetic",
    "contamination_checked",
}

VALID_TRACKS = {"ukrainian", "sorbian"}
VALID_TASKS = {"MT", "QA", "SC", "GC", "MR", "LANG", "FORMAT"}
VALID_SPLITS = {"train", "tune", "locked_validation", "test_placeholder"}
VALID_SOURCE_TYPES = {
    "official",
    "external",
    "synthetic",
    "teacher_generated",
    "distilled",
}


@dataclass
class CanonicalExample:
    id: str
    track: str
    task: str
    language: str
    input: str
    target: str
    messages: list[dict[str, str]]
    source_id: str
    source_type: str
    license: str
    split: str
    is_synthetic: bool
    contamination_checked: bool
    source_language: str | None = None
    target_language: str | None = None
    generation_method: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "track": self.track,
            "task": self.task,
            "language": self.language,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "input": self.input,
            "target": self.target,
            "messages": self.messages,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "license": self.license,
            "split": self.split,
            "is_synthetic": self.is_synthetic,
            "generation_method": self.generation_method,
            "contamination_checked": self.contamination_checked,
            "metadata": self.metadata,
        }


def validate_example(example: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(example))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if example.get("track") not in VALID_TRACKS:
        errors.append(f"invalid track: {example.get('track')!r}")
    if example.get("task") not in VALID_TASKS:
        errors.append(f"invalid task: {example.get('task')!r}")
    if example.get("split") not in VALID_SPLITS:
        errors.append(f"invalid split: {example.get('split')!r}")
    if example.get("source_type") not in VALID_SOURCE_TYPES:
        errors.append(f"invalid source_type: {example.get('source_type')!r}")
    if not isinstance(example.get("messages"), list) or not example.get("messages"):
        errors.append("messages must be a non-empty list")
    else:
        for idx, message in enumerate(example["messages"]):
            if set(message) != {"role", "content"}:
                errors.append(f"message {idx} must contain exactly role/content")
            if message.get("role") not in {"system", "user", "assistant"}:
                errors.append(f"message {idx} has invalid role {message.get('role')!r}")
            if not isinstance(message.get("content"), str):
                errors.append(f"message {idx} content must be a string")
    if not isinstance(example.get("contamination_checked"), bool):
        errors.append("contamination_checked must be boolean")
    if example.get("contamination_checked") is not True:
        errors.append("contamination_checked must be true before training/eval use")
    return errors


def read_jsonl(path: str | Path) -> Iterable[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc


def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> int:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count
