#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EDIT_TARGET_RE = re.compile(
    r"Wrong word:\s*(?P<wrong>.+?)\s*\nCorrect word:\s*(?P<correct>.+?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
NUMERIC_TARGET_RE = re.compile(r"^\s*[-+]?\d+(?:\.\d+)?\s*$")


def read_jsonl(path: Path, cap: int | None = None) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
            if cap and len(rows) >= cap:
                break
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return len(rows)


def parse_edit_target(target: str) -> tuple[str, str] | None:
    match = EDIT_TARGET_RE.match(str(target).strip())
    if not match:
        return None
    return match.group("wrong").strip(), match.group("correct").strip()


def replace_first(sentence: str, old: str, new: str) -> str:
    if old == "CORRECT":
        return sentence
    pattern = re.compile(rf"(?<!\w){re.escape(old)}(?!\w)")
    return pattern.sub(new, sentence, count=1)


def set_message_content(row: dict, clean_input: str, target: str) -> list[dict]:
    messages = []
    original_input = str(row.get("input", ""))
    for message in row.get("messages", []):
        updated = dict(message)
        if updated.get("role") == "user":
            updated["content"] = str(updated.get("content", "")).replace(original_input, clean_input)
        elif updated.get("role") == "assistant":
            updated["content"] = target
        messages.append(updated)
    return messages


def clean_counterpart(row: dict) -> dict | None:
    parsed = parse_edit_target(str(row.get("target", "")))
    if not parsed:
        return None
    wrong, correct = parsed
    if wrong == "CORRECT" and correct == "CORRECT":
        return None
    clean_input = replace_first(str(row.get("input", "")), wrong, correct)
    if clean_input == row.get("input"):
        return None
    target = "Wrong word: CORRECT\nCorrect word: CORRECT"
    clean = dict(row)
    clean["id"] = f"{row.get('id', 'edit')}:clean"
    clean["input"] = clean_input
    clean["target"] = target
    clean["messages"] = set_message_content(row, clean_input, target)
    clean["generation_method"] = "derived_clean_no_error_counterpart"
    metadata = dict(clean.get("metadata") or {})
    metadata.update(
        {
            "derived_clean_from": row.get("id"),
            "original_wrong_word": wrong,
            "original_correct_word": correct,
        }
    )
    clean["metadata"] = metadata
    return clean


def add_clean_counterparts(rows: list[dict]) -> list[dict]:
    clean_rows = [row for row in rows if parse_edit_target(str(row.get("target", ""))) == ("CORRECT", "CORRECT")]
    counterparts = []
    seen_inputs = {str(row.get("input", "")) for row in clean_rows}
    for row in rows:
        clean = clean_counterpart(row)
        if clean and str(clean.get("input", "")) not in seen_inputs:
            counterparts.append(clean)
            seen_inputs.add(str(clean.get("input", "")))
    return rows + counterparts


def numeric_mr_rows(rows: list[dict]) -> list[dict]:
    return [row for row in rows if NUMERIC_TARGET_RE.match(str(row.get("target", "")))]


def build_uk() -> dict[str, int]:
    out = ROOT / "data/processed/final/uk"
    ext = ROOT / "data/processed/external/uk"
    counts = {}
    counts["mt_train_final"] = write_jsonl(out / "mt_train_final.jsonl", read_jsonl(ext / "mt_train.jsonl") + read_jsonl(ext / "mt_doc_train.jsonl"))
    counts["qa_train_final"] = write_jsonl(out / "qa_train_final.jsonl", read_jsonl(ROOT / "data/processed/uk/qa_train.jsonl") + read_jsonl(ext / "qa_generated_public.jsonl", 2000))
    uk_sc = read_jsonl(ROOT / "data/processed/uk/sc_train.jsonl") + read_jsonl(ext / "sc_real.jsonl") + read_jsonl(ext / "sc_synthetic_public.jsonl")
    uk_gc = read_jsonl(ROOT / "data/processed/uk/gc_train.jsonl") + read_jsonl(ext / "gc_real.jsonl") + read_jsonl(ext / "gc_synthetic_public.jsonl")
    counts["sc_train_final"] = write_jsonl(out / "sc_train_final.jsonl", add_clean_counterparts(uk_sc))
    counts["gc_train_final"] = write_jsonl(out / "gc_train_final.jsonl", add_clean_counterparts(uk_gc))
    counts["mr_train_final"] = write_jsonl(out / "mr_train_final.jsonl", numeric_mr_rows(read_jsonl(ROOT / "data/processed/uk/mr_train.jsonl") + read_jsonl(ext / "mr_non_benchmark.jsonl")))
    counts["lang_curriculum_external"] = write_jsonl(out / "lang_curriculum_external.jsonl", read_jsonl(ROOT / "data/processed/uk/lang_train.jsonl") + read_jsonl(ext / "monolingual_train.jsonl"))
    counts["format_polish_final"] = write_jsonl(out / "format_polish_final.jsonl", read_jsonl(ROOT / "data/processed/uk/format_preferences.jsonl"))
    return counts


def build_sorbian() -> dict[str, int]:
    out = ROOT / "data/processed/final/sorbian"
    ext = ROOT / "data/processed/external/sorbian"
    counts = {}
    counts["mt_train_final"] = write_jsonl(out / "mt_train_final.jsonl", read_jsonl(ROOT / "data/processed/sorbian/mt_train.jsonl", 120000) + read_jsonl(ext / "mt_prior_wmt.jsonl"))
    counts["qa_train_final"] = write_jsonl(out / "qa_train_final.jsonl", read_jsonl(ext / "qa_generated_public_hsb.jsonl") + read_jsonl(ext / "qa_generated_public_dsb.jsonl"))
    sorb_sc = read_jsonl(ROOT / "data/processed/sorbian/sc_train.jsonl") + read_jsonl(ext / "sc_synthetic_hsb.jsonl") + read_jsonl(ext / "sc_synthetic_dsb.jsonl")
    sorb_gc = read_jsonl(ROOT / "data/processed/sorbian/gc_train.jsonl") + read_jsonl(ext / "gc_synthetic_hsb.jsonl") + read_jsonl(ext / "gc_synthetic_dsb.jsonl")
    counts["sc_train_final"] = write_jsonl(out / "sc_train_final.jsonl", add_clean_counterparts(sorb_sc))
    counts["gc_train_final"] = write_jsonl(out / "gc_train_final.jsonl", add_clean_counterparts(sorb_gc))
    counts["mr_train_final"] = write_jsonl(out / "mr_train_final.jsonl", numeric_mr_rows(read_jsonl(ROOT / "data/processed/sorbian/mr_train.jsonl") + read_jsonl(ext / "mr_non_benchmark_hsb.jsonl") + read_jsonl(ext / "mr_non_benchmark_dsb.jsonl")))
    counts["lang_curriculum_external"] = write_jsonl(out / "lang_curriculum_external.jsonl", read_jsonl(ROOT / "data/processed/sorbian/lang_train.jsonl") + read_jsonl(ext / "monolingual_public.jsonl"))
    counts["format_polish_final"] = write_jsonl(out / "format_polish_final.jsonl", read_jsonl(ROOT / "data/processed/sorbian/format_preferences.jsonl"))
    return counts


def main() -> int:
    uk = build_uk()
    sorb = build_sorbian()
    summary = ROOT / "data/manifests/final_training_data_summary.md"
    lines = ["# Final Training Data Summary", "", "## Ukrainian", ""]
    for name, count in uk.items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "## Sorbian", ""])
    for name, count in sorb.items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "Generated by `scripts/build_external_training_sets.py`."])
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
