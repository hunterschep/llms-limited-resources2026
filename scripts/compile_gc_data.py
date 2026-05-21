#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.compilers.common import clean_sentence, edit_example, license_for, read_csv, read_jsonl, replace_first_word, split_for, stable_rng, word_candidates, write_jsonl


SUFFIX_SWAPS = {
    "ukr": [("ами", "ів"), ("ів", "ами"), ("ого", "ому"), ("ому", "ого"), ("а", "у"), ("у", "а"), ("и", "ою")],
    "hsb": [("om", ""), ("eho", "emu"), ("emu", "eho"), ("a", "om"), ("ow", "ami")],
    "dsb": [("om", ""), ("ego", "emu"), ("emu", "ego"), ("a", "u"), ("ow", "ami")],
}


def grammar_variant(word: str, language: str, seed: int, key: str) -> str | None:
    rng = stable_rng(seed, key)
    swaps = SUFFIX_SWAPS.get(language, [])
    rng.shuffle(swaps)
    for old, new in swaps:
        if word.endswith(old) and len(word) > len(old) + 2:
            return word[: -len(old)] + new
    if len(word) > 5:
        return word[:-1] + rng.choice(["a", "u", "om", "e"])
    return None


def clean_sources(language: str, max_rows: int) -> list[str]:
    sources: list[str] = []
    if language == "ukr":
        for rel in ["Ukrainian/QA/ukr_qa_train.jsonl", "Ukrainian/QA/ukr_mmlu_qa_train.jsonl"]:
            for row in read_jsonl(ROOT / rel):
                sources.append(clean_sentence(row.get("question", "")))
                if len(sources) >= max_rows:
                    return sources
    elif language == "hsb":
        for row in read_csv(ROOT / "Sorbian/MT/hsb_monolingual_2026.csv"):
            sources.append(clean_sentence(row.get("hsb", "")))
            if len(sources) >= max_rows:
                return sources
    elif language == "dsb":
        for row in read_csv(ROOT / "Sorbian/MT/dsb_monolingual_2026.csv"):
            sources.append(clean_sentence(row.get("dsb", "")))
            if len(sources) >= max_rows:
                return sources
    return [s for s in sources if s]


def official_examples() -> list[dict]:
    rows: list[dict] = []
    for rel, track, language in [
        ("Ukrainian/GC/ukr_gc_dev.jsonl", "ukrainian", "ukr"),
        ("Sorbian/GC/hsb_gc_dev.jsonl", "sorbian", "hsb"),
        ("Sorbian/GC/dsb_gc_dev.jsonl", "sorbian", "dsb"),
    ]:
        for idx, row in enumerate(read_jsonl(ROOT / rel)):
            split = split_for(rel, idx, "tune")
            rows.append(
                edit_example(
                    idx=f"{Path(rel).stem}:{row.get('id', idx)}",
                    track=track,
                    task="GC",
                    language=language,
                    input_sentence=row["input_sentence"],
                    wrong_word=str(row["incorrect_word"]),
                    correct_word=str(row["correct_word"]),
                    split=split,
                    source_id=f"official:{Path(rel).stem}",
                    source_type="official",
                    license_name=license_for(rel),
                    metadata={"relative_path": rel},
                )
            )
    return rows


def synthetic_examples(config: dict) -> list[dict]:
    seed = int(config.get("seed", 2606))
    max_per_language = int(config.get("synthetic_per_language", 200))
    rows: list[dict] = []
    for language, track in [("ukr", "ukrainian"), ("hsb", "sorbian"), ("dsb", "sorbian")]:
        for idx, sentence in enumerate(clean_sources(language, max_per_language)):
            candidates = word_candidates(sentence)
            rng = stable_rng(seed, f"gc:{language}:{idx}:{sentence}")
            rng.shuffle(candidates)
            correct = None
            wrong = None
            for candidate in candidates:
                variant = grammar_variant(candidate, language, seed, f"{language}:{idx}:{candidate}")
                if variant and variant != candidate:
                    correct = candidate
                    wrong = variant
                    break
            if not correct or not wrong:
                continue
            corrupted = replace_first_word(sentence, correct, wrong)
            rows.append(
                edit_example(
                    idx=f"synthetic-gc-{language}-{idx:06d}",
                    track=track,
                    task="GC",
                    language=language,
                    input_sentence=corrupted,
                    wrong_word=wrong,
                    correct_word=correct,
                    split="train",
                    source_id="synthetic:scgc_compilers",
                    source_type="synthetic",
                    license_name="derived-from-source-license",
                    generation_method="morphology_suffix_minimal_pair",
                    metadata={"clean_sentence": sentence},
                )
            )
            if idx % 5 == 0:
                rows.append(
                    edit_example(
                        idx=f"synthetic-gc-clean-{language}-{idx:06d}",
                        track=track,
                        task="GC",
                        language=language,
                        input_sentence=sentence,
                        wrong_word="CORRECT",
                        correct_word="CORRECT",
                        split="train",
                        source_id="synthetic:scgc_compilers",
                        source_type="synthetic",
                        license_name="derived-from-source-license",
                        generation_method="clean_no_error_case",
                    )
                )
    return rows


def emit(rows: list[dict], track: str) -> None:
    out_dir = ROOT / "data/processed" / ("uk" if track == "ukrainian" else "sorbian")
    for split in ["train", "tune", "locked_validation"]:
        split_rows = [row for row in rows if row["track"] == track and row["split"] == split]
        count = write_jsonl(out_dir / f"gc_{split}.jsonl", split_rows)
        print(f"{track} GC {split}: {count}")


def main() -> None:
    config = yaml.safe_load((ROOT / "configs/compilers/gc.yaml").read_text(encoding="utf-8")) or {}
    rows = official_examples() + synthetic_examples(config)
    emit(rows, "ukrainian")
    emit(rows, "sorbian")


if __name__ == "__main__":
    main()
