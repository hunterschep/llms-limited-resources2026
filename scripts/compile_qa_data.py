#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.compilers.common import license_for, qa_example, read_jsonl, split_for, stable_rng, write_jsonl


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def normalize_options(options: dict) -> dict[str, str]:
    return {str(k): str(v) for k, v in options.items()}


def shuffled_options(options: dict[str, str], answer: str, seed: int, key: str, labels: str) -> tuple[dict[str, str], str]:
    rng = stable_rng(seed, key)
    items = list(options.items())
    rng.shuffle(items)
    out: dict[str, str] = {}
    new_answer = ""
    for idx, (old_label, text) in enumerate(items):
        label = str(idx) if labels == "numeric" else LETTERS[idx]
        out[label] = text
        if str(old_label) == str(answer):
            new_answer = label
    return out, new_answer


def compile_ukrainian(config: dict) -> list[dict]:
    rows: list[dict] = []
    seed = int(config.get("seed", 2606))
    augment_train = bool(config.get("augment_answer_order", True))
    for rel, source_name, default_split in [
        ("Ukrainian/QA/ukr_qa_train.jsonl", "ukr_qa_train", "train"),
        ("Ukrainian/QA/ukr_mmlu_qa_train.jsonl", "ukr_mmlu_qa_train", "train"),
        ("Ukrainian/QA/ukr_qa_dev.jsonl", "ukr_qa_dev", "tune"),
        ("Ukrainian/QA/ukr_mmlu_qa_dev.jsonl", "ukr_mmlu_qa_dev", "tune"),
    ]:
        data = read_jsonl(ROOT / rel)
        for idx, row in enumerate(data):
            options = normalize_options(row.get("possible_answers") or {})
            if not options:
                continue
            split = default_split if "train" in rel else split_for(rel, idx, "tune")
            answer = str(row["correct_answer_num"])
            base_id = f"{source_name}:{idx:06d}"
            rows.append(
                qa_example(
                    idx=base_id,
                    track="ukrainian",
                    language="ukr",
                    question=row["question"],
                    options=options,
                    answer=answer,
                    split=split,
                    source_id=f"official:{source_name}",
                    source_type="official",
                    license_name=license_for(rel),
                    metadata={"relative_path": rel, "subject": row.get("subject")},
                )
            )
            if split == "train" and augment_train:
                for label_style in ["numeric", "alphabetic"]:
                    shuf, shuf_answer = shuffled_options(
                        options,
                        answer,
                        seed,
                        f"{rel}:{idx}:{label_style}",
                        label_style,
                    )
                    rows.append(
                        qa_example(
                            idx=f"{base_id}:shuffle-{label_style}",
                            track="ukrainian",
                            language="ukr",
                            question=row["question"],
                            options=shuf,
                            answer=shuf_answer,
                            split="train",
                            source_id=f"official:{source_name}",
                            source_type="official",
                            license_name=license_for(rel),
                            generation_method="answer_order_label_augmentation",
                            metadata={"relative_path": rel, "subject": row.get("subject")},
                        )
                    )
    return rows


def compile_sorbian(config: dict) -> list[dict]:
    rows: list[dict] = []
    for rel, language in [
        ("Sorbian/QA/hsb_qa_dev.jsonl", "hsb"),
        ("Sorbian/QA/dsb_qa_dev.jsonl", "dsb"),
    ]:
        data = read_jsonl(ROOT / rel)
        for idx, row in enumerate(data):
            split = split_for(rel, idx, "tune")
            context = row.get("context") or ""
            question = row["question"] if not context else f"{context}\n\n{row['question']}"
            rows.append(
                qa_example(
                    idx=f"{Path(rel).stem}:{row.get('question_id', idx)}",
                    track="sorbian",
                    language=language,
                    question=question,
                    options=normalize_options(row.get("possible_answers") or {}),
                    answer=str(row["correct_answer_num"]),
                    split=split,
                    source_id=f"official:{Path(rel).stem}",
                    source_type="official",
                    license_name=license_for(rel),
                    metadata={
                        "relative_path": rel,
                        "question_level": row.get("question_level"),
                        "question_type": row.get("question_type"),
                        "official_certificate_material": True,
                    },
                )
            )
    return rows


def emit(rows: list[dict], track: str) -> None:
    out_dir = ROOT / "data/processed" / ("uk" if track == "ukrainian" else "sorbian")
    for split in ["train", "tune", "locked_validation"]:
        split_rows = [row for row in rows if row["track"] == track and row["split"] == split]
        count = write_jsonl(out_dir / f"qa_{split}.jsonl", split_rows)
        print(f"{track} QA {split}: {count}")


def main() -> None:
    config = yaml.safe_load((ROOT / "configs/compilers/qa.yaml").read_text(encoding="utf-8")) or {}
    rows = compile_ukrainian(config) + compile_sorbian(config)
    emit(rows, "ukrainian")
    emit(rows, "sorbian")


if __name__ == "__main__":
    main()
