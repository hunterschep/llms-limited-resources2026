#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.compilers.common import license_for, mr_example, read_jsonl, split_for, write_jsonl


TEMPLATES = {
    "ukr": [
        ("У Марії є {a} олівців. Вона купила ще {b}. Скільки олівців у неї тепер?", "{sum}"),
        ("Пакет містить {a} груп по {b} карток. Скільки карток у пакеті?", "{prod}"),
        ("У класі було {a} учнів, {b} пішли додому. Скільки учнів залишилось?", "{diff}"),
    ],
    "hsb": [
        ("Marija ma {a} pisakow. Přikupi hišće {b}. Kelko pisakow ma nětko?", "{sum}"),
        ("Pakćik ma {a} skupin po {b} kartach. Kelko kartow je w pakćiku?", "{prod}"),
        ("W rjadowni bě {a} šulerjow, {b} dźěše domoj. Kelko šulerjow wosta?", "{diff}"),
    ],
    "dsb": [
        ("Marija ma {a} pisakow. Dokupujo hyšći {b}. Kak wjele pisakow ma něnto?", "{sum}"),
        ("Pakśik ma {a} kupkow po {b} kartach. Kak wjele kartow jo w pakśiku?", "{prod}"),
        ("W klasownej bě {a} wuknikow, {b} su domoj šli. Kak wjele wuknikow jo wóstało?", "{diff}"),
    ],
}


def synthetic_examples(config: dict) -> list[dict]:
    count = int(config.get("synthetic_per_language", 36))
    rows: list[dict] = []
    for language, track in [("ukr", "ukrainian"), ("hsb", "sorbian"), ("dsb", "sorbian")]:
        for idx in range(count):
            a = 5 + idx % 17
            b = 2 + (idx * 3) % 11
            template, answer_template = TEMPLATES[language][idx % len(TEMPLATES[language])]
            values = {"a": a, "b": b, "sum": a + b, "prod": a * b, "diff": a - min(b, a)}
            rows.append(
                mr_example(
                    idx=f"synthetic-mr-{language}-{idx:04d}",
                    track=track,
                    language=language,
                    question=template.format(**values),
                    answer=answer_template.format(**values),
                    split="train",
                    source_id="synthetic:mr_arithmetic_preservation",
                    source_type="synthetic",
                    license_name="MIT",
                    generation_method="non_polymath_arithmetic_template",
                    metadata={"poly_math_policy": "not_used_not_derived"},
                )
            )
    return rows


def official_dev_examples() -> list[dict]:
    rows: list[dict] = []
    for rel, track, language in [
        ("Ukrainian/MR/ukr_mr_dev.jsonl", "ukrainian", "ukr"),
        ("Sorbian/MR/hsb_mr_dev.jsonl", "sorbian", "hsb"),
        ("Sorbian/MR/dsb_mr_dev.jsonl", "sorbian", "dsb"),
    ]:
        for idx, row in enumerate(read_jsonl(ROOT / rel)):
            rows.append(
                mr_example(
                    idx=f"{Path(rel).stem}:{row.get('id', idx)}",
                    track=track,
                    language=language,
                    question=row["question"],
                    answer=str(row["answer"]),
                    split=split_for(rel, idx, "locked_validation"),
                    source_id=f"official:{Path(rel).stem}",
                    source_type="official",
                    license_name=license_for(rel),
                    metadata={
                        "relative_path": rel,
                        "policy": "format inspection and locked validation only",
                        "poly_math_policy": "official dev examples are not used for training",
                    },
                )
            )
    return rows


def emit(rows: list[dict], track: str) -> None:
    out_dir = ROOT / "data/processed" / ("uk" if track == "ukrainian" else "sorbian")
    for split in ["train", "tune", "locked_validation"]:
        split_rows = [row for row in rows if row["track"] == track and row["split"] == split]
        count = write_jsonl(out_dir / f"mr_{split}.jsonl", split_rows)
        print(f"{track} MR {split}: {count}")


def main() -> None:
    config = yaml.safe_load((ROOT / "configs/compilers/mr.yaml").read_text(encoding="utf-8")) or {}
    rows = synthetic_examples(config) + official_dev_examples()
    emit(rows, "ukrainian")
    emit(rows, "sorbian")


if __name__ == "__main__":
    main()
