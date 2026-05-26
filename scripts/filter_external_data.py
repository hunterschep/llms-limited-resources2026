#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import re
import sys
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
_raw_root = Path(os.environ.get("WMT26_RAW_ROOT", "data/external/raw")).expanduser()
RAW_ROOT = _raw_root if _raw_root.is_absolute() else ROOT / _raw_root

from wmt26.compilers.common import (
    edit_example,
    mr_example,
    mt_example,
    qa_example,
    read_csv,
    read_jsonl,
    stable_rng,
    word_candidates,
    replace_first_word,
    write_jsonl,
)

FILTER_REPORT = ROOT / "data/manifests/external_data_filter_report.jsonl"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip())


def cyrillic_fraction(text: str) -> float:
    chars = [ch for ch in text if ch.isalpha()]
    if not chars:
        return 0.0
    return sum("\u0400" <= ch <= "\u04FF" for ch in chars) / len(chars)


def punct_fraction(text: str) -> float:
    if not text:
        return 0.0
    return sum(not ch.isalnum() and not ch.isspace() for ch in text) / len(text)


def digit_fraction(text: str) -> float:
    if not text:
        return 0.0
    return sum(ch.isdigit() for ch in text) / len(text)


def good_text(text: str, min_chars: int, max_chars: int) -> bool:
    text = norm(text)
    if len(text) < min_chars or len(text) > max_chars:
        return False
    if "http://" in text or "https://" in text:
        return False
    if re.search(r"(.)\1{6,}", text):
        return False
    if punct_fraction(text) > 0.45 or digit_fraction(text) > 0.45:
        return False
    return True


def find_opus_pair(source_id: str, source_lang: str, target_lang: str) -> tuple[Path, Path] | None:
    root = RAW_ROOT / source_id.replace(":", "__")
    extracted_dirs = [p for p in root.glob("*.txt") if p.is_dir()] + [p for p in root.glob("*.zip") if p.with_suffix("").exists()]
    dirs = []
    for item in root.iterdir() if root.exists() else []:
        if item.is_dir():
            dirs.append(item)
    for directory in dirs:
        source_files = list(directory.glob(f"*.{source_lang}"))
        target_files = list(directory.glob(f"*.{target_lang}"))
        if source_files and target_files:
            return source_files[0], target_files[0]
    return None


def load_opus(source_id: str, source_lang: str, target_lang: str, cap: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pair = find_opus_pair(source_id, source_lang, target_lang)
    if pair is None:
        return [], {"source_id": source_id, "row_count_raw": 0, "row_count_after_filtering": 0, "notes": "raw files missing"}
    src_path, tgt_path = pair
    raw = 0
    rows = []
    seen = set()
    with src_path.open("r", encoding="utf-8", errors="ignore") as src_handle, tgt_path.open("r", encoding="utf-8", errors="ignore") as tgt_handle:
        for idx, (src, tgt) in enumerate(zip(src_handle, tgt_handle)):
            raw += 1
            src = norm(src)
            tgt = norm(tgt)
            if not good_text(src, 3, 500) or not good_text(tgt, 3, 500):
                continue
            if cyrillic_fraction(tgt) < 0.35:
                continue
            ratio = max(len(src), len(tgt)) / max(1, min(len(src), len(tgt)))
            if ratio > 3.0 or src.lower() == tgt.lower():
                continue
            key = (src.lower(), tgt.lower())
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                mt_example(
                    idx=f"{source_id}:{idx:08d}:{source_lang}->{target_lang}",
                    track="ukrainian",
                    source_language=source_lang,
                    target_language="ukr",
                    source_text=src,
                    target_text=tgt,
                    split="train",
                    source_id=source_id,
                    source_type="external",
                    license_name="CC-BY 2.0 / mixed OPUS metadata",
                    generation_method="opus_moses_filtered",
                    metadata={"raw_index": idx, "source_lang": source_lang, "target_lang": target_lang},
                )
            )
            if len(rows) >= cap:
                break
    report = {
        "source_id": source_id,
        "row_count_raw": raw,
        "row_count_after_filtering": len(rows),
        "filtering_steps": ["length", "target_cyrillic_fraction", "length_ratio", "deduplicate_exact_pair"],
    }
    return rows, report


def build_doc_mt(rows: list[dict[str, Any]], group_size: int = 3, cap: int = 2000) -> list[dict[str, Any]]:
    out = []
    for idx in range(0, min(len(rows) - group_size + 1, cap * group_size), group_size):
        group = rows[idx : idx + group_size]
        if len(group) < group_size:
            continue
        src_lang = group[0]["source_language"]
        source = "\n".join(row["input"] for row in group)
        target = "\n".join(row["target"] for row in group)
        out.append(
            mt_example(
                idx=f"external:uk_doc_mt:{idx:08d}:{src_lang}->ukr",
                track="ukrainian",
                source_language=src_lang,
                target_language="ukr",
                source_text=source,
                target_text=target,
                split="train",
                source_id=group[0]["source_id"],
                source_type="external",
                license_name=group[0]["license"],
                generation_method="adjacent_sentence_document_grouping",
                metadata={"anti_summarization": True, "group_size": group_size},
            )
        )
    return out


def parse_m2(path: Path, cap: int = 3000) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    sc_rows: list[dict[str, Any]] = []
    gc_rows: list[dict[str, Any]] = []
    raw_blocks = 0
    if not path.exists():
        return sc_rows, gc_rows, {"source_id": "external:ua_gec_train", "row_count_raw": 0, "row_count_after_filtering": 0, "notes": "raw missing"}
    blocks = path.read_text(encoding="utf-8", errors="ignore").split("\n\n")
    for block_idx, block in enumerate(blocks):
        lines = [line for line in block.splitlines() if line]
        if not lines or not lines[0].startswith("S "):
            continue
        raw_blocks += 1
        tokens = lines[0][2:].split()
        for edit_idx, line in enumerate(lines[1:]):
            if not line.startswith("A "):
                continue
            parts = line.split("|||")
            span = parts[0].split()
            if len(span) < 3:
                continue
            try:
                start, end = int(span[1]), int(span[2])
            except ValueError:
                continue
            if end - start != 1 or start >= len(tokens):
                continue
            correction = parts[2].strip()
            error_type = parts[1].strip().lower()
            if not correction or correction == "-NONE-" or len(correction.split()) != 1:
                continue
            wrong = tokens[start]
            corrected_tokens = tokens[:]
            corrected_tokens[start] = correction
            input_sentence = " ".join(tokens)
            task = "SC" if "spell" in error_type or "orth" in error_type else "GC"
            target_rows = sc_rows if task == "SC" else gc_rows
            if len(target_rows) >= cap:
                continue
            target_rows.append(
                edit_example(
                    idx=f"ua-gec-{task.lower()}-{block_idx:07d}-{edit_idx}",
                    track="ukrainian",
                    task=task,
                    language="ukr",
                    input_sentence=input_sentence,
                    wrong_word=wrong,
                    correct_word=correction,
                    split="train",
                    source_id="external:ua_gec_train",
                    source_type="external",
                    license_name="CC BY-SA 4.0",
                    generation_method="ua_gec_one_token_m2_mining",
                    metadata={"error_type": error_type},
                )
            )
    report = {
        "source_id": "external:ua_gec_train",
        "row_count_raw": raw_blocks,
        "row_count_after_filtering": len(sc_rows) + len(gc_rows),
        "filtering_steps": ["one_token_span", "single_token_correction", "split_train_only"],
    }
    return sc_rows, gc_rows, report


def parse_ud_sentences(path: Path, cap: int = 3000) -> list[str]:
    sentences = []
    current = []
    if not path.exists():
        return sentences
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# text = "):
            text = norm(line.removeprefix("# text = "))
            if good_text(text, 20, 800):
                sentences.append(text)
                if len(sentences) >= cap:
                    break
    return sentences


def suffix_variant(word: str, language: str, seed_key: str) -> str | None:
    swaps = {
        "ukr": [("ами", "ів"), ("ів", "ами"), ("ого", "ому"), ("ому", "ого"), ("а", "у"), ("у", "а"), ("и", "ою")],
        "hsb": [("om", ""), ("eho", "emu"), ("emu", "eho"), ("a", "om"), ("ow", "ami")],
        "dsb": [("om", ""), ("ego", "emu"), ("emu", "ego"), ("a", "u"), ("ow", "ami")],
    }.get(language, [])
    rng = stable_rng(2606, seed_key)
    rng.shuffle(swaps)
    for old, new in swaps:
        if word.endswith(old) and len(word) > len(old) + 2:
            return word[: -len(old)] + new
    return None


def build_scgc_from_sentences(sentences: list[str], track: str, language: str, source_id: str, prefix: str, cap: int) -> tuple[list[dict], list[dict], list[dict]]:
    sc_rows: list[dict] = []
    gc_rows: list[dict] = []
    lang_rows: list[dict] = []
    for idx, sentence in enumerate(sentences[:cap]):
        candidates = word_candidates(sentence)
        if not candidates:
            continue
        rng = stable_rng(2606, f"{prefix}:{idx}:{sentence}")
        word = rng.choice(candidates)
        if len(word) > 4:
            wrong = word[:-1] + ("а" if language == "ukr" else "x")
            if wrong != word:
                sc_rows.append(
                    edit_example(
                        idx=f"{prefix}-sc-{idx:06d}",
                        track=track,
                        task="SC",
                        language=language,
                        input_sentence=replace_first_word(sentence, word, wrong),
                        wrong_word=wrong,
                        correct_word=word,
                        split="train",
                        source_id=source_id,
                        source_type="external",
                        license_name="derived-from-source-license",
                        generation_method="public_text_typo_generation",
                    )
                )
        variant = suffix_variant(word, language, f"{prefix}:gc:{idx}:{word}")
        if variant and variant != word:
            gc_rows.append(
                edit_example(
                    idx=f"{prefix}-gc-{idx:06d}",
                    track=track,
                    task="GC",
                    language=language,
                    input_sentence=replace_first_word(sentence, word, variant),
                    wrong_word=variant,
                    correct_word=word,
                    split="train",
                    source_id=source_id,
                    source_type="external",
                    license_name="derived-from-source-license",
                    generation_method="public_text_morphology_minimal_pair",
                )
            )
        if idx % 4 == 0:
            sc_rows.append(
                edit_example(
                    idx=f"{prefix}-sc-clean-{idx:06d}",
                    track=track,
                    task="SC",
                    language=language,
                    input_sentence=sentence,
                    wrong_word="CORRECT",
                    correct_word="CORRECT",
                    split="train",
                    source_id=source_id,
                    source_type="external",
                    license_name="derived-from-source-license",
                    generation_method="public_text_clean_case",
                )
            )
            gc_rows.append(
                edit_example(
                    idx=f"{prefix}-gc-clean-{idx:06d}",
                    track=track,
                    task="GC",
                    language=language,
                    input_sentence=sentence,
                    wrong_word="CORRECT",
                    correct_word="CORRECT",
                    split="train",
                    source_id=source_id,
                    source_type="external",
                    license_name="derived-from-source-license",
                    generation_method="public_text_clean_case",
                )
            )
    return sc_rows, gc_rows, lang_rows


def build_sorbian_qa(sentences: list[str], language: str, cap: int) -> list[dict]:
    rows = []
    words_pool = []
    for sentence in sentences:
        words_pool.extend(word_candidates(sentence))
    words_pool = list(dict.fromkeys(words_pool))
    if len(words_pool) < 8:
        return rows
    for idx, sentence in enumerate(sentences[:cap]):
        candidates = word_candidates(sentence)
        if len(candidates) < 2:
            continue
        rng = stable_rng(2606, f"sorbian-qa:{language}:{idx}:{sentence}")
        answer = rng.choice(candidates)
        distractors = [w for w in words_pool if w != answer and len(w) >= 4]
        rng.shuffle(distractors)
        options_list = [answer] + distractors[:3]
        rng.shuffle(options_list)
        labels = ["0", "1", "2", "3"]
        options = dict(zip(labels, options_list))
        correct_label = next(label for label, value in options.items() if value == answer)
        question = f"Context:\n{sentence}\n\nWhich option is a word that appears in the context?"
        rows.append(
            qa_example(
                idx=f"sorbian-public-qa-{language}-{idx:06d}",
                track="sorbian",
                language=language,
                question=question,
                options=options,
                answer=correct_label,
                split="train",
                source_id=f"official:sorb_mono_{language}",
                source_type="official",
                license_name="Apache-2.0",
                generation_method="public_monolingual_cloze_mcq",
                metadata={"evidence": answer, "source_url": "https://github.com/TUM-NLP/llms-limited-resources2026"},
            )
        )
    return rows


def lang_example(idx: str, track: str, language: str, text: str, source_id: str, license_name: str) -> dict[str, Any]:
    return {
        "id": idx,
        "track": track,
        "task": "LANG",
        "language": language,
        "source_language": None,
        "target_language": None,
        "input": text,
        "target": text,
        "messages": [
            {"role": "system", "content": f"Follow the instruction and preserve {language} text exactly."},
            {"role": "user", "content": f"Reproduce this text exactly:\n{text}"},
            {"role": "assistant", "content": text},
        ],
        "source_id": source_id,
        "source_type": "external",
        "license": license_name,
        "split": "train",
        "is_synthetic": False,
        "generation_method": "competitive_public_monolingual_language_curriculum",
        "contamination_checked": True,
        "metadata": {},
    }


def gzip_lines(path: Path) -> list[str]:
    with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as handle:
        return [norm(line) for line in handle if norm(line)]


def build_wmt22_sorbian(root: Path, cap_mt: int = 260000, cap_lang: int = 160000) -> tuple[list[dict], list[dict], dict[str, Any]]:
    mt_rows: list[dict] = []
    lang_rows: list[dict] = []
    raw_pairs = 0
    seen_pairs: set[tuple[str, str, str, str]] = set()
    if not root.exists():
        return mt_rows, lang_rows, {"source_id": "external:wmt22_sorbian_data_scripted", "row_count_raw": 0, "row_count_after_filtering": 0, "notes": "raw missing"}

    def add_pair(prefix: str, lang_a: str, lang_b: str, lines_a: list[str], lines_b: list[str]) -> None:
        nonlocal raw_pairs
        for idx, (text_a, text_b) in enumerate(zip(lines_a, lines_b)):
            raw_pairs += 1
            text_a = norm(text_a)
            text_b = norm(text_b)
            if not good_text(text_a, 3, 800) or not good_text(text_b, 3, 800):
                continue
            if text_a.lower() == text_b.lower():
                continue
            for src_lang, tgt_lang, src, tgt in [(lang_a, lang_b, text_a, text_b), (lang_b, lang_a, text_b, text_a)]:
                key = (src_lang, tgt_lang, src.lower(), tgt.lower())
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                mt_rows.append(
                    mt_example(
                        idx=f"external:wmt22:{prefix}:{idx:08d}:{src_lang}->{tgt_lang}",
                        track="sorbian",
                        source_language=src_lang,
                        target_language=tgt_lang,
                        source_text=src,
                        target_text=tgt,
                        split="train",
                        source_id="external:wmt22_sorbian_data_scripted",
                        source_type="external",
                        license_name="WMT22 public data repository",
                        generation_method="wmt22_train_support_parallel_filtered",
                        metadata={"raw_prefix": prefix, "raw_index": idx},
                    )
                )
                if len(mt_rows) >= cap_mt:
                    return

    grouped: dict[str, dict[str, Path]] = {}
    for path in sorted(root.glob("*.gz")):
        name = path.name
        lower = name.lower()
        if any(marker in lower for marker in ["dev", "test", "valid"]):
            continue
        if "monolingual" in lower or lower.startswith("mono.") or lower.startswith("web_") or lower.startswith("witaj_"):
            lang = "dsb" if "dsb" in lower else "hsb" if "hsb" in lower else ""
            if not lang:
                continue
            for idx, text in enumerate(gzip_lines(path)):
                if len(lang_rows) >= cap_lang:
                    break
                if good_text(text, 20, 900):
                    lang_rows.append(
                        lang_example(
                            idx=f"external-wmt22-lang-{lang}-{path.stem}-{idx:07d}",
                            track="sorbian",
                            language=lang,
                            text=text,
                            source_id="external:wmt22_sorbian_data_scripted",
                            license_name="WMT22 public data repository",
                        )
                    )
            continue
        stem = name[:-3]
        parts = stem.rsplit(".", 1)
        if len(parts) == 2 and parts[1] in {"de", "hsb", "dsb"}:
            grouped.setdefault(parts[0], {})[parts[1]] = path

    for prefix, files in sorted(grouped.items()):
        langs = [lang for lang in ["de", "hsb", "dsb"] if lang in files]
        if len(langs) != 2:
            continue
        add_pair(prefix, langs[0], langs[1], gzip_lines(files[langs[0]]), gzip_lines(files[langs[1]]))
        if len(mt_rows) >= cap_mt:
            break

    for path in sorted(root.glob("*train.tsv.gz")):
        lower = path.name.lower()
        if "hsb-de" not in lower:
            continue
        hsb_lines: list[str] = []
        de_lines: list[str] = []
        with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                parts = [norm(part) for part in line.split("\t")]
                if len(parts) >= 2:
                    hsb_lines.append(parts[0])
                    de_lines.append(parts[1])
        add_pair(path.stem, "hsb", "de", hsb_lines, de_lines)
        if len(mt_rows) >= cap_mt:
            break

    return mt_rows, lang_rows, {
        "source_id": "external:wmt22_sorbian_data_scripted",
        "row_count_raw": raw_pairs,
        "row_count_after_filtering": len(mt_rows) + len(lang_rows),
        "parallel_rows": len(mt_rows),
        "language_rows": len(lang_rows),
        "filtering_steps": ["exclude_dev_valid_test", "length", "exact_pair_dedup", "bidirectional_expansion"],
    }


def build_leipzig_rows(path: Path, language: str, source_id: str, cap: int = 120000) -> tuple[list[dict], dict[str, Any]]:
    rows: list[dict] = []
    raw = 0
    if not path.exists():
        return rows, {"source_id": source_id, "row_count_raw": 0, "row_count_after_filtering": 0, "notes": "raw missing"}
    if path.suffix == ".gz" and not path.name.endswith(".tar.gz"):
        texts = gzip_lines(path)
    else:
        texts = []
        with tarfile.open(path, "r:gz") as archive:
            for member in archive.getmembers():
                if "sentences" not in member.name or not member.isfile():
                    continue
                extracted = archive.extractfile(member)
                if extracted is None:
                    continue
                for raw_line in extracted:
                    line = raw_line.decode("utf-8", errors="ignore")
                    parts = line.rstrip("\n").split("\t")
                    texts.append(norm(parts[-1] if parts else line))
                break
    seen: set[str] = set()
    for idx, text in enumerate(texts):
        raw += 1
        if len(rows) >= cap:
            break
        if not good_text(text, 20, 900):
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        rows.append(lang_example(f"external-leipzig-{language}-{idx:07d}", "sorbian", language, text, source_id, "Leipzig Corpora Collection / source-specific terms"))
    return rows, {"source_id": source_id, "row_count_raw": raw, "row_count_after_filtering": len(rows), "filtering_steps": ["sentence_extraction", "length", "exact_dedup"]}


def build_mr(path: Path, cap: int, track: str, language: str, source_id: str, prefix: str) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    if path.suffix == ".jsonl":
        source_rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for idx, row in enumerate(source_rows[:cap]):
            answer = str(row.get("answer", "")).split("####")[-1].strip()
            question = row.get("question", "")
            if not question or not answer:
                continue
            prompt = f"Answer this arithmetic problem. Return only the final answer.\n{question}"
            rows.append(mr_example(idx=f"{prefix}-{idx:05d}", track=track, language=language, question=prompt, answer=answer, split="train", source_id=source_id, source_type="external", license_name="MIT", generation_method="non_benchmark_math_preservation"))
    elif path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        for idx, row in enumerate(data[:cap]):
            question = norm(f"{row.get('Body', '')} {row.get('Question', '')}")
            answer = str(row.get("Answer", "")).strip()
            if question and answer:
                rows.append(mr_example(idx=f"{prefix}-{idx:05d}", track=track, language=language, question=question, answer=answer, split="train", source_id=source_id, source_type="external", license_name="MIT-like research-public", generation_method="non_benchmark_math_preservation"))
    elif path.suffix == ".xml":
        root = ET.parse(path).getroot()
        for idx, problem in enumerate(root.findall(".//Problem")[:cap]):
            body = norm(problem.findtext("Body") or "")
            question_text = norm(problem.findtext("Question") or "")
            answer = norm(problem.findtext("Answer") or "").split()[0]
            question = norm(f"{body} {question_text}")
            if question and answer:
                rows.append(mr_example(idx=f"{prefix}-{idx:05d}", track=track, language=language, question=question, answer=answer, split="train", source_id=source_id, source_type="external", license_name="research-public", generation_method="non_benchmark_math_preservation"))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data/external_source_filters.yaml")
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    reports = []

    uk_external = ROOT / "data/processed/external/uk"
    sorb_external = ROOT / "data/processed/external/sorbian"
    uk_external.mkdir(parents=True, exist_ok=True)
    sorb_external.mkdir(parents=True, exist_ok=True)

    en_rows, report = load_opus("external:opus_tatoeba_en_uk", "en", "uk", config["parallel_mt"]["cap_per_source"]["external:opus_tatoeba_en_uk"])
    reports.append(report)
    cs_rows, report = load_opus("external:opus_tatoeba_cs_uk", "cs", "uk", config["parallel_mt"]["cap_per_source"]["external:opus_tatoeba_cs_uk"])
    reports.append(report)
    mt_rows = en_rows + cs_rows
    write_jsonl(uk_external / "mt_train.jsonl", mt_rows)
    write_jsonl(uk_external / "mt_doc_train.jsonl", build_doc_mt(en_rows, cap=2000) + build_doc_mt(cs_rows, cap=500))

    sc_real, gc_real, report = parse_m2(RAW_ROOT / "external__ua_gec_train/gec-only.train.m2", cap=3000)
    reports.append(report)
    write_jsonl(uk_external / "sc_real.jsonl", sc_real)
    write_jsonl(uk_external / "gc_real.jsonl", gc_real)

    ud_sentences = parse_ud_sentences(RAW_ROOT / "external__ud_uk_iu/uk_iu-ud-train.conllu", cap=5000)
    sc_syn, gc_syn, _ = build_scgc_from_sentences(ud_sentences, "ukrainian", "ukr", "external:ud_uk_iu", "ud-uk", cap=2000)
    write_jsonl(uk_external / "sc_synthetic_public.jsonl", sc_syn)
    write_jsonl(uk_external / "gc_synthetic_public.jsonl", gc_syn)
    write_jsonl(uk_external / "monolingual_train.jsonl", [
        {
            "id": f"external-uk-lang-{idx:06d}",
            "track": "ukrainian",
            "task": "LANG",
            "language": "ukr",
            "source_language": None,
            "target_language": None,
            "input": text,
            "target": text,
            "messages": [
                {"role": "system", "content": "Follow the instruction and preserve Ukrainian text exactly."},
                {"role": "user", "content": f"Reproduce this Ukrainian text exactly:\n{text}"},
                {"role": "assistant", "content": text},
            ],
            "source_id": "external:ud_uk_iu",
            "source_type": "external",
            "license": "CC BY-SA 4.0",
            "split": "train",
            "is_synthetic": False,
            "generation_method": "ud_sentence_language_curriculum",
            "contamination_checked": True,
            "metadata": {},
        }
        for idx, text in enumerate(ud_sentences[:2000])
    ])

    # Lightweight public generated Ukrainian QA from UD sentences.
    uk_qa = []
    for idx, sentence in enumerate(ud_sentences[:1000]):
        words = word_candidates(sentence)
        if len(words) < 5:
            continue
        rng = stable_rng(2606, f"ukqa:{idx}:{sentence}")
        answer = rng.choice(words)
        distractors = [w for w in words if w != answer][:3]
        if len(distractors) < 3:
            continue
        options_list = [answer] + distractors
        rng.shuffle(options_list)
        options = {str(i): value for i, value in enumerate(options_list)}
        label = next(k for k, v in options.items() if v == answer)
        uk_qa.append(qa_example(idx=f"uk-public-qa-{idx:06d}", track="ukrainian", language="ukr", question=f"Контекст:\n{sentence}\n\nЯке слово є в цьому контексті?", options=options, answer=label, split="train", source_id="external:ud_uk_iu", source_type="external", license_name="CC BY-SA 4.0", generation_method="public_sentence_cloze_mcq", metadata={"evidence": answer}))
    write_jsonl(uk_external / "qa_generated_public.jsonl", uk_qa)

    # Sorbian public generated QA/SC/GC from official monolingual public corpora.
    hsb_sentences = [row["hsb"] for row in read_csv(ROOT / "Sorbian/MT/hsb_monolingual_2026.csv")[:3000] if good_text(row.get("hsb", ""), 20, 800)]
    dsb_sentences = [row["dsb"] for row in read_csv(ROOT / "Sorbian/MT/dsb_monolingual_2026.csv")[:3000] if good_text(row.get("dsb", ""), 20, 800)]
    write_jsonl(sorb_external / "qa_generated_public_hsb.jsonl", build_sorbian_qa(hsb_sentences, "hsb", 1200))
    write_jsonl(sorb_external / "qa_generated_public_dsb.jsonl", build_sorbian_qa(dsb_sentences, "dsb", 1200))
    hsb_sc, hsb_gc, _ = build_scgc_from_sentences(hsb_sentences, "sorbian", "hsb", "official:sorb_mono_hsb", "hsb-public", cap=1600)
    dsb_sc, dsb_gc, _ = build_scgc_from_sentences(dsb_sentences, "sorbian", "dsb", "official:sorb_mono_dsb", "dsb-public", cap=1600)
    write_jsonl(sorb_external / "sc_synthetic_hsb.jsonl", hsb_sc)
    write_jsonl(sorb_external / "sc_synthetic_dsb.jsonl", dsb_sc)
    write_jsonl(sorb_external / "gc_synthetic_hsb.jsonl", hsb_gc)
    write_jsonl(sorb_external / "gc_synthetic_dsb.jsonl", dsb_gc)
    wmt22_mt, wmt22_lang, report = build_wmt22_sorbian(RAW_ROOT / "external__wmt22_sorbian_data_scripted")
    reports.append(report)
    leipzig_hsb, report = build_leipzig_rows(RAW_ROOT / "external__leipzig_hsb_scripted/hsb_mixed_2012_300K.tar.gz", "hsb", "external:leipzig_hsb_scripted")
    reports.append(report)
    leipzig_dsb, report = build_leipzig_rows(RAW_ROOT / "external__leipzig_dsb_scripted/8815_DSB_wikipedia_2021.txt.gz", "dsb", "external:leipzig_dsb_scripted")
    reports.append(report)
    write_jsonl(sorb_external / "monolingual_public.jsonl", [
        {
            "id": f"sorbian-lang-{lang}-{idx:06d}",
            "track": "sorbian",
            "task": "LANG",
            "language": lang,
            "source_language": None,
            "target_language": None,
            "input": text,
            "target": text,
            "messages": [
                {"role": "system", "content": "Follow the instruction and preserve Sorbian text exactly."},
                {"role": "user", "content": f"Reproduce this text exactly:\n{text}"},
                {"role": "assistant", "content": text},
            ],
            "source_id": f"official:sorb_mono_{lang}",
            "source_type": "official",
            "license": "Apache-2.0",
            "split": "train",
            "is_synthetic": False,
            "generation_method": "public_monolingual_language_curriculum",
            "contamination_checked": True,
            "metadata": {},
        }
        for lang, sentences in [("hsb", hsb_sentences), ("dsb", dsb_sentences)]
        for idx, text in enumerate(sentences[:1500])
    ] + wmt22_lang + leipzig_hsb + leipzig_dsb)
    write_jsonl(sorb_external / "mt_prior_wmt.jsonl", wmt22_mt)
    write_jsonl(sorb_external / "related_transfer_cs_pl.jsonl", [])

    gsm_path = RAW_ROOT / "external__gsm8k_train/train.jsonl"
    svamp_path = RAW_ROOT / "external__svamp/SVAMP.json"
    asdiv_path = RAW_ROOT / "external__asdiv/ASDiv.xml"
    uk_mr = build_mr(gsm_path, 140, "ukrainian", "ukr", "external:gsm8k_train", "uk-gsm8k")
    uk_mr += build_mr(svamp_path, 70, "ukrainian", "ukr", "external:svamp", "uk-svamp")
    uk_mr += build_mr(asdiv_path, 70, "ukrainian", "ukr", "external:asdiv", "uk-asdiv")
    write_jsonl(uk_external / "mr_non_benchmark.jsonl", uk_mr)
    hsb_mr = build_mr(gsm_path, 120, "sorbian", "hsb", "external:gsm8k_train", "hsb-gsm8k")
    dsb_mr = build_mr(gsm_path, 120, "sorbian", "dsb", "external:gsm8k_train", "dsb-gsm8k")
    write_jsonl(sorb_external / "mr_non_benchmark_hsb.jsonl", hsb_mr)
    write_jsonl(sorb_external / "mr_non_benchmark_dsb.jsonl", dsb_mr)

    FILTER_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with FILTER_REPORT.open("w", encoding="utf-8") as handle:
        for report in reports:
            handle.write(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Wrote filter report to {FILTER_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
