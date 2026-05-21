#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.compilers.common import CanonicalExample, language_name, read_csv, read_jsonl, render_messages, write_jsonl


def make_lang_example(idx: str, track: str, language: str, text: str, source_id: str, license_name: str) -> dict:
    prompt = f"Read the following {language_name(language)} text and reproduce it exactly. This preserves language competence without changing task format.\n\n{text}"
    target = text
    return CanonicalExample(
        id=idx,
        track=track,
        task="LANG",
        language=language,
        input=prompt,
        target=target,
        messages=[
            {"role": "system", "content": "You preserve low-resource language competence while following instructions exactly."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": target},
        ],
        source_id=source_id,
        source_type="official",
        license=license_name,
        split="train",
        is_synthetic=False,
        generation_method="instruction_preserving_language_copy",
        contamination_checked=True,
    ).to_dict()


def build_track(config_path: Path, track_key: str) -> None:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    rows: list[dict] = []
    max_rows = int(config.get("max_rows_per_source", 1000))
    if track_key == "uk":
        for rel in ["Ukrainian/QA/ukr_qa_train.jsonl", "Ukrainian/QA/ukr_mmlu_qa_train.jsonl"]:
            for idx, row in enumerate(read_jsonl(ROOT / rel)[:max_rows]):
                text = str(row.get("question", "")).strip()
                if text:
                    rows.append(make_lang_example(f"lang-ukr-{Path(rel).stem}-{idx:06d}", "ukrainian", "ukr", text, f"official:{Path(rel).stem}", "MIT" if "ukr_qa_train" in rel else "unknown-upstream-mmlu_ukr"))
    else:
        for rel, language in [("Sorbian/MT/hsb_monolingual_2026.csv", "hsb"), ("Sorbian/MT/dsb_monolingual_2026.csv", "dsb")]:
            text_col = language
            for idx, row in enumerate(read_csv(ROOT / rel)[:max_rows]):
                text = str(row.get(text_col, "")).strip()
                if text:
                    rows.append(make_lang_example(f"lang-{language}-{idx:06d}", "sorbian", language, text, f"official:{Path(rel).stem}", "Apache-2.0"))
    out_dir = ROOT / "data/processed" / track_key
    count = write_jsonl(out_dir / "lang_train.jsonl", rows)
    print(f"{track_key} LANG train: {count}")


def main() -> None:
    build_track(ROOT / "configs/data/language_curriculum_uk.yaml", "uk")
    build_track(ROOT / "configs/data/language_curriculum_sorbian.yaml", "sorbian")


if __name__ == "__main__":
    main()
