#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)


def rejected_for(row: dict) -> str:
    task = row["task"]
    if task in {"SC", "GC"}:
        return "Here is the corrected full sentence: " + row["input"]
    if task == "QA":
        return f"The answer is {row['target']} because that option is most likely correct."
    if task == "MR":
        return f"Let's solve step by step. Therefore the final answer is {row['target']}."
    if task == "MT":
        return "Summary: " + row["target"][:160]
    return row["target"] + "\n\nExplanation omitted."


def build_for(track_dir: str) -> None:
    processed = ROOT / "data/processed" / track_dir
    rows: list[dict] = []
    for file in processed.glob("*_train.jsonl"):
        for idx, row in enumerate(read_jsonl(file)[:300]):
            if row["task"] not in {"MT", "QA", "SC", "GC", "MR"}:
                continue
            rows.append(
                {
                    "id": f"format-pref-{track_dir}-{file.stem}-{idx:06d}",
                    "track": row["track"],
                    "task": "FORMAT",
                    "source_task": row["task"],
                    "messages": row["messages"][:-1],
                    "chosen": row["target"],
                    "rejected": rejected_for(row),
                    "source_id": "synthetic:format_preference",
                    "source_type": "synthetic",
                    "license": row["license"],
                    "split": "train",
                    "contamination_checked": True,
                    "generation_method": "format_contrastive_pair",
                }
            )
    count = write_jsonl(processed / "format_preferences.jsonl", rows)
    print(f"{track_dir} format preferences: {count}")


def main() -> None:
    build_for("uk")
    build_for("sorbian")


if __name__ == "__main__":
    main()
