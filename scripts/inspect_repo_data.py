#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/manifests/official_data_inventory.jsonl"
DOC = ROOT / "docs/02_repo_data_inventory.md"


LICENSE_BY_PATH = {
    "Ukrainian/MT": "Apache-2.0",
    "Ukrainian/QA/ukr_qa": "MIT",
    "Ukrainian/QA/ukr_mmlu": "unknown-upstream-mmlu_ukr",
    "Ukrainian/SC": "Apache-2.0",
    "Ukrainian/GC": "Apache-2.0",
    "Ukrainian/MR": "Apache-2.0",
    "Sorbian/MT/train": "CC BY-NC-SA",
    "Sorbian/MT/de-": "CC BY-NC-SA",
    "Sorbian/MT/hsb-dsb": "CC BY-NC-SA",
    "Sorbian/MT/hsb_monolingual": "Apache-2.0",
    "Sorbian/MT/dsb_monolingual": "Apache-2.0",
    "Sorbian/QA": "CC BY-NC-SA",
    "Sorbian/SC": "CC BY-NC-SA",
    "Sorbian/GC": "CC BY-NC-SA",
    "Sorbian/MR": "Apache-2.0",
}


def license_for(rel: str) -> str:
    for prefix, license_name in sorted(LICENSE_BY_PATH.items(), key=lambda x: len(x[0]), reverse=True):
        if rel.startswith(prefix):
            return license_name
    return "unknown"


def infer_track(path: Path) -> str:
    if path.parts[0] == "Ukrainian":
        return "ukrainian"
    if path.parts[0] == "Sorbian":
        return "sorbian"
    return "unknown"


def infer_task(path: Path) -> str:
    parts = path.parts
    if len(parts) >= 2 and parts[1] in {"MT", "QA", "SC", "GC", "MR"}:
        return parts[1]
    return "unknown"


def infer_split(path: Path) -> str:
    name = path.name
    if "train" in name:
        return "train"
    if "dev" in name:
        return "dev"
    if "monolingual" in name:
        return "monolingual"
    return "unknown"


def infer_language(path: Path) -> str:
    stem = path.stem
    name = path.name
    if path.parts[0] == "Ukrainian":
        if path.parts[1] == "MT":
            return stem.split("_")[0].replace("-", "->")
        return "ukr"
    if path.parts[0] == "Sorbian":
        if path.parts[1] == "MT":
            if stem.startswith("train_"):
                return stem.removeprefix("train_").split("_")[0].replace("-", "<->")
            return stem.split("_")[0].replace("-", "<->")
        return name.split("_", 1)[0]
    return "unknown"


def has_gold(path: Path, split_type: str) -> bool:
    if split_type in {"train", "dev"}:
        return True
    return False


def recommended_use(path: Path, split_type: str) -> str:
    task = infer_task(path)
    if split_type == "train":
        return "safe official train data"
    if split_type == "monolingual":
        return "official monolingual support data for language curriculum/backtranslation"
    if split_type == "dev" and task == "MR":
        return "format inspection and locked validation; avoid broad supervised training"
    if split_type == "dev":
        return "official dev data; split into tune and locked validation"
    return "inspect manually before use"


def read_jsonl_summary(path: Path) -> tuple[int, list[str], dict[str, Any]]:
    count = 0
    fields: set[str] = set()
    example: dict[str, Any] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if not example:
                example = row
            fields.update(row.keys())
            count += 1
    return count, sorted(fields), example


def read_csv_summary(path: Path) -> tuple[int, list[str], dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        count = 0
        example: dict[str, Any] = {}
        for row in reader:
            if not example:
                example = dict(row)
            count += 1
    return count, fields, example


def inspect_file(path: Path) -> dict[str, Any]:
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix == ".jsonl":
        row_count, schema_fields, example_row = read_jsonl_summary(path)
    elif path.suffix == ".csv":
        row_count, schema_fields, example_row = read_csv_summary(path)
    else:
        raise ValueError(path)
    split_type = infer_split(path.relative_to(ROOT))
    return {
        "relative_path": rel,
        "track": infer_track(path.relative_to(ROOT)),
        "task": infer_task(path.relative_to(ROOT)),
        "language_or_language_pair": infer_language(path.relative_to(ROOT)),
        "split_type": split_type,
        "row_count": row_count,
        "schema_fields": schema_fields,
        "example_row": example_row,
        "has_gold_labels": has_gold(path, split_type),
        "license_if_known": license_for(rel),
        "recommended_use": recommended_use(path, split_type),
        "notes": notes_for(path.relative_to(ROOT), row_count),
    }


def notes_for(path: Path, row_count: int) -> str:
    rel = path.as_posix()
    if rel == "Ukrainian/QA/ukr_qa_train.jsonl":
        return "Contains two rows with empty possible_answers; skip or repair before supervised QA training."
    if path.name.endswith("_dev.jsonl"):
        return "Treat as official development data, not ordinary training data."
    if "monolingual" in path.name:
        return "No task labels; use for instruction-preserving language curriculum or backtranslation inputs."
    if row_count <= 24:
        return "Tiny file; preserve for format inspection and locked validation."
    return ""


def build_inventory() -> list[dict[str, Any]]:
    paths = sorted(
        list((ROOT / "Ukrainian").glob("*/*.*"))
        + list((ROOT / "Sorbian").glob("*/*.*"))
    )
    return [inspect_file(path) for path in paths if path.suffix in {".jsonl", ".csv"}]


def write_manifest(rows: list[dict[str, Any]]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_doc(rows: list[dict[str, Any]]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Official Data Inventory",
        "",
        "Generated by `scripts/inspect_repo_data.py` from the local repository.",
        "",
        "The repository is asymmetric: Ukrainian has QA train files, Sorbian has MT train/monolingual files, and most other task files are official development files with gold labels. All `*_dev.jsonl` files are treated as development data until an explicit final-training policy overrides that.",
        "",
        "| Path | Track | Task | Lang/Pair | Split | Rows | Gold | License | Recommended use |",
        "|---|---|---|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['relative_path']}` | {row['track']} | {row['task']} | "
            f"{row['language_or_language_pair']} | {row['split_type']} | {row['row_count']} | "
            f"{row['has_gold_labels']} | {row['license_if_known']} | {row['recommended_use']} |"
        )
    lines.extend(
        [
            "",
            "## Safe Official Train Data",
            "",
            "- `Ukrainian/QA/ukr_qa_train.jsonl` and `Ukrainian/QA/ukr_mmlu_qa_train.jsonl` are official Ukrainian QA training data. The ZNO train file has two rows with empty `possible_answers`; compilers skip those unless repaired explicitly.",
            "- `Sorbian/MT/train_de-hsb_2026.csv`, `Sorbian/MT/train_de-dsb_2026.csv`, and `Sorbian/MT/train_hsb-dsb_2026.csv` are official Sorbian MT training corpora.",
            "",
            "## Official Monolingual Support Data",
            "",
            "- `Sorbian/MT/hsb_monolingual_2026.csv` and `Sorbian/MT/dsb_monolingual_2026.csv` are support corpora for language acquisition, synthetic SC/GC, and possible backtranslation inputs.",
            "",
            "## Official Dev Data",
            "",
            "- Every `*_dev.jsonl` file is initially reserved for prompt inspection, tuning, and locked validation. Larger dev files are split deterministically; MR dev files are kept mainly for format inspection and locked validation.",
            "",
            "## Manifest",
            "",
            f"The machine-readable inventory is `{MANIFEST.relative_to(ROOT)}`.",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_inventory()
    write_manifest(rows)
    write_doc(rows)
    print(f"Wrote {len(rows)} inventory rows to {MANIFEST}")
    print(f"Wrote {DOC}")


if __name__ == "__main__":
    main()
