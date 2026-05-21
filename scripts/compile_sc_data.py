#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.compilers.common import clean_sentence, edit_example, license_for, read_csv, read_jsonl, replace_first_word, split_for, stable_rng, word_candidates, write_jsonl


CYRILLIC_CONFUSIONS = str.maketrans({"о": "0", "а": "a", "е": "є", "і": "ї", "и": "і"})
SORBIAN_DIACRITICS = {
    "č": "c",
    "ć": "c",
    "ě": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ř": "r",
    "š": "s",
    "ž": "z",
    "ź": "z",
    "ś": "s",
}


def corrupt_word(word: str, language: str, seed: int, key: str) -> str:
    rng = stable_rng(seed, key)
    operations = ["delete", "insert", "substitute", "transpose"]
    if language == "ukr":
        operations.append("cyrillic_confusion")
    if language in {"hsb", "dsb"}:
        operations.append("diacritic_delete")
    op = rng.choice(operations)
    if len(word) < 4:
        return word + "x"
    pos = rng.randrange(len(word))
    letters = "abcdefghijklmnopqrstuvwxyzабвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    if op == "delete":
        return word[:pos] + word[pos + 1 :]
    if op == "insert":
        return word[:pos] + rng.choice(letters) + word[pos:]
    if op == "substitute":
        return word[:pos] + rng.choice(letters) + word[pos + 1 :]
    if op == "transpose" and len(word) > 4 and pos < len(word) - 1:
        return word[:pos] + word[pos + 1] + word[pos] + word[pos + 2 :]
    if op == "cyrillic_confusion":
        changed = word.translate(CYRILLIC_CONFUSIONS)
        return changed if changed != word else word[:pos] + "і" + word[pos + 1 :]
    if op == "diacritic_delete":
        changed = "".join(SORBIAN_DIACRITICS.get(ch, ch) for ch in word)
        return changed if changed != word else word[:pos] + "c" + word[pos + 1 :]
    return word + "x"


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
        ("Ukrainian/SC/ukr_sc_dev.jsonl", "ukrainian", "ukr"),
        ("Sorbian/SC/hsb_sc_dev.jsonl", "sorbian", "hsb"),
        ("Sorbian/SC/dsb_sc_dev.jsonl", "sorbian", "dsb"),
    ]:
        for idx, row in enumerate(read_jsonl(ROOT / rel)):
            split = split_for(rel, idx, "tune")
            rows.append(
                edit_example(
                    idx=f"{Path(rel).stem}:{row.get('id', idx)}",
                    track=track,
                    task="SC",
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
            if not candidates:
                continue
            rng = stable_rng(seed, f"{language}:{idx}:{sentence}")
            correct = rng.choice(candidates)
            wrong = corrupt_word(correct, language, seed, f"{language}:{idx}:{correct}")
            if wrong == correct:
                continue
            corrupted = replace_first_word(sentence, correct, wrong)
            rows.append(
                edit_example(
                    idx=f"synthetic-sc-{language}-{idx:06d}",
                    track=track,
                    task="SC",
                    language=language,
                    input_sentence=corrupted,
                    wrong_word=wrong,
                    correct_word=correct,
                    split="train",
                    source_id="synthetic:scgc_compilers",
                    source_type="synthetic",
                    license_name="derived-from-source-license",
                    generation_method="language_aware_spelling_corruption",
                    metadata={"clean_sentence": sentence},
                )
            )
            if idx % 5 == 0:
                rows.append(
                    edit_example(
                        idx=f"synthetic-sc-clean-{language}-{idx:06d}",
                        track=track,
                        task="SC",
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
        count = write_jsonl(out_dir / f"sc_{split}.jsonl", split_rows)
        print(f"{track} SC {split}: {count}")


def main() -> None:
    config = yaml.safe_load((ROOT / "configs/compilers/sc.yaml").read_text(encoding="utf-8")) or {}
    rows = official_examples() + synthetic_examples(config)
    emit(rows, "ukrainian")
    emit(rows, "sorbian")


if __name__ == "__main__":
    main()
