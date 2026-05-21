from __future__ import annotations

import csv
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Any, Iterable

from wmt26.data.schema import CanonicalExample
from wmt26.prompts.templates import LANGUAGE_NAMES, render_messages, two_line_edit_target


ROOT = Path(__file__).resolve().parents[3]
PROMPT_DIR = ROOT / "configs/prompts"


def language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, code)


def stable_rng(seed: int, key: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}:{key}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


_SPLIT_MANIFEST_CACHE: dict[tuple[str, int], str] | None = None


def load_split_manifest() -> dict[tuple[str, int], str]:
    global _SPLIT_MANIFEST_CACHE
    if _SPLIT_MANIFEST_CACHE is not None:
        return _SPLIT_MANIFEST_CACHE
    manifest_path = ROOT / "data/manifests/local_split_manifest.jsonl"
    lookup: dict[tuple[str, int], str] = {}
    if not manifest_path.exists():
        _SPLIT_MANIFEST_CACHE = lookup
        return lookup
    with manifest_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            lookup[(row["relative_path"], int(row["row_index"]))] = row["split"]
    _SPLIT_MANIFEST_CACHE = lookup
    return lookup


def split_for(rel_path: str, row_index: int, default: str) -> str:
    return load_split_manifest().get((rel_path, row_index), default)


def license_for(rel_path: str) -> str:
    if rel_path.startswith("Ukrainian/MT"):
        return "Apache-2.0"
    if rel_path.startswith("Ukrainian/QA/ukr_qa"):
        return "MIT"
    if rel_path.startswith("Ukrainian/QA/ukr_mmlu"):
        return "unknown-upstream-mmlu_ukr"
    if rel_path.startswith("Ukrainian/SC") or rel_path.startswith("Ukrainian/GC") or rel_path.startswith("Ukrainian/MR"):
        return "Apache-2.0"
    if "monolingual" in rel_path or rel_path.startswith("Sorbian/MR"):
        return "Apache-2.0"
    if rel_path.startswith("Sorbian"):
        return "CC BY-NC-SA"
    return "unknown"


def mt_example(
    *,
    idx: str,
    track: str,
    source_language: str,
    target_language: str,
    source_text: str,
    target_text: str,
    split: str,
    source_id: str,
    source_type: str,
    license_name: str,
    generation_method: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    messages = render_messages(
        PROMPT_DIR / "mt.yaml",
        target=target_text,
        source_language=source_language,
        target_language=target_language,
        source_language_name=language_name(source_language),
        target_language_name=language_name(target_language),
        input=source_text,
    )
    return CanonicalExample(
        id=idx,
        track=track,
        task="MT",
        language=target_language,
        source_language=source_language,
        target_language=target_language,
        input=source_text,
        target=target_text,
        messages=messages,
        source_id=source_id,
        source_type=source_type,
        license=license_name,
        split=split,
        is_synthetic=source_type == "synthetic",
        generation_method=generation_method,
        contamination_checked=True,
        metadata=metadata or {},
    ).to_dict()


def edit_example(
    *,
    idx: str,
    track: str,
    task: str,
    language: str,
    input_sentence: str,
    wrong_word: str,
    correct_word: str,
    split: str,
    source_id: str,
    source_type: str,
    license_name: str,
    generation_method: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    target = two_line_edit_target(wrong_word, correct_word)
    prompt_name = "sc.yaml" if task == "SC" else "gc.yaml"
    messages = render_messages(
        PROMPT_DIR / prompt_name,
        target=target,
        input_sentence=input_sentence,
    )
    return CanonicalExample(
        id=idx,
        track=track,
        task=task,
        language=language,
        input=input_sentence,
        target=target,
        messages=messages,
        source_id=source_id,
        source_type=source_type,
        license=license_name,
        split=split,
        is_synthetic=source_type == "synthetic",
        generation_method=generation_method,
        contamination_checked=True,
        metadata=metadata or {},
    ).to_dict()


def qa_example(
    *,
    idx: str,
    track: str,
    language: str,
    question: str,
    options: dict[str, str],
    answer: str,
    split: str,
    source_id: str,
    source_type: str,
    license_name: str,
    generation_method: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    options_text = "\n".join(f"{label}. {text}" for label, text in options.items())
    messages = render_messages(
        PROMPT_DIR / "qa.yaml",
        target=str(answer),
        question=question,
        options=options_text,
    )
    return CanonicalExample(
        id=idx,
        track=track,
        task="QA",
        language=language,
        input=f"{question}\n\n{options_text}",
        target=str(answer),
        messages=messages,
        source_id=source_id,
        source_type=source_type,
        license=license_name,
        split=split,
        is_synthetic=source_type == "synthetic",
        generation_method=generation_method,
        contamination_checked=True,
        metadata=metadata or {},
    ).to_dict()


def mr_example(
    *,
    idx: str,
    track: str,
    language: str,
    question: str,
    answer: str,
    split: str,
    source_id: str,
    source_type: str,
    license_name: str,
    generation_method: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    messages = render_messages(PROMPT_DIR / "mr.yaml", target=str(answer), question=question)
    return CanonicalExample(
        id=idx,
        track=track,
        task="MR",
        language=language,
        input=question,
        target=str(answer),
        messages=messages,
        source_id=source_id,
        source_type=source_type,
        license=license_name,
        split=split,
        is_synthetic=source_type == "synthetic",
        generation_method=generation_method,
        contamination_checked=True,
        metadata=metadata or {},
    ).to_dict()


def clean_sentence(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip())


def word_candidates(sentence: str) -> list[str]:
    return [w.strip(".,;:!?\"'“”„()[]{}") for w in sentence.split() if len(w.strip(".,;:!?\"'“”„()[]{}")) >= 4]


def replace_first_word(sentence: str, old: str, new: str) -> str:
    pattern = re.compile(rf"(?<!\w){re.escape(old)}(?!\w)")
    return pattern.sub(new, sentence, count=1)
