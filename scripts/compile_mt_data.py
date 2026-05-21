#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.compilers.common import license_for, mt_example, read_csv, read_jsonl, split_for, write_jsonl


def compile_sorbian() -> list[dict]:
    rows: list[dict] = []
    pairs = [
        ("Sorbian/MT/train_de-hsb_2026.csv", "de", "hsb", "train"),
        ("Sorbian/MT/train_de-dsb_2026.csv", "de", "dsb", "train"),
        ("Sorbian/MT/train_hsb-dsb_2026.csv", "hsb", "dsb", "train"),
        ("Sorbian/MT/de-hsb_mt_dev.jsonl", "de", "hsb", "dev"),
        ("Sorbian/MT/de-dsb_mt_dev.jsonl", "de", "dsb", "dev"),
        ("Sorbian/MT/hsb-dsb_mt_dev.jsonl", "hsb", "dsb", "dev"),
    ]
    for rel, src, tgt, split_kind in pairs:
        path = ROOT / rel
        license_name = license_for(rel)
        if path.suffix == ".csv":
            data = read_csv(path)
        else:
            data = read_jsonl(path)
        for idx, row in enumerate(data):
            split = "train" if split_kind == "train" else split_for(rel, idx, "tune")
            row_id = row.get("sent_id") or f"{Path(rel).stem}-{idx:06d}"
            source_id = f"official:{Path(rel).stem}"
            rows.append(
                mt_example(
                    idx=f"{row_id}:{src}->{tgt}",
                    track="sorbian",
                    source_language=src,
                    target_language=tgt,
                    source_text=row[src],
                    target_text=row[tgt],
                    split=split,
                    source_id=source_id,
                    source_type="official",
                    license_name=license_name,
                    metadata={"relative_path": rel, "direction": f"{src}->{tgt}"},
                )
            )
            rows.append(
                mt_example(
                    idx=f"{row_id}:{tgt}->{src}",
                    track="sorbian",
                    source_language=tgt,
                    target_language=src,
                    source_text=row[tgt],
                    target_text=row[src],
                    split=split,
                    source_id=source_id,
                    source_type="official",
                    license_name=license_name,
                    metadata={"relative_path": rel, "direction": f"{tgt}->{src}"},
                )
            )
    return rows


def compile_ukrainian() -> list[dict]:
    rows: list[dict] = []
    for rel, src, tgt in [
        ("Ukrainian/MT/en-ukr_mt_dev.jsonl", "en", "ukr"),
        ("Ukrainian/MT/cs-ukr_mt_dev.jsonl", "cs", "ukr"),
    ]:
        data = read_jsonl(ROOT / rel)
        for idx, row in enumerate(data):
            split = split_for(rel, idx, "tune")
            row_id = row.get("sent_id") or f"{Path(rel).stem}-{idx:06d}"
            rows.append(
                mt_example(
                    idx=f"{row_id}:{src}->{tgt}",
                    track="ukrainian",
                    source_language=src,
                    target_language=tgt,
                    source_text=row[src],
                    target_text=row["uk"],
                    split=split,
                    source_id=f"official:{Path(rel).stem}",
                    source_type="official",
                    license_name=license_for(rel),
                    metadata={
                        "relative_path": rel,
                        "direction": f"{src}->{tgt}",
                        "official_dev_policy": "tune_or_locked_validation_only",
                    },
                )
            )
    return rows


def emit(rows: list[dict], track: str) -> None:
    out_dir = ROOT / "data/processed" / ("uk" if track == "ukrainian" else "sorbian")
    for split in ["train", "tune", "locked_validation"]:
        split_rows = [row for row in rows if row["track"] == track and row["split"] == split]
        count = write_jsonl(out_dir / f"mt_{split}.jsonl", split_rows)
        print(f"{track} MT {split}: {count}")


def main() -> None:
    config_path = ROOT / "configs/compilers/mt.yaml"
    if config_path.exists():
        yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    rows = compile_sorbian() + compile_ukrainian()
    emit(rows, "ukrainian")
    emit(rows, "sorbian")


if __name__ == "__main__":
    main()
