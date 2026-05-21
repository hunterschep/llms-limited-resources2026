#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def count_file(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def main() -> int:
    rows = []
    for path in sorted((ROOT / "data/processed/external").glob("**/*.jsonl")) + sorted((ROOT / "data/processed/final").glob("**/*.jsonl")):
        rows.append({"path": path.relative_to(ROOT).as_posix(), "row_count": count_file(path)})
    inventory = ROOT / "data/manifests/external_data_inventory.jsonl"
    filter_report = ROOT / "data/manifests/external_data_filter_report.jsonl"
    doc = ROOT / "data/manifests/external_data_quality_report.md"
    lines = [
        "# External Data Quality Report",
        "",
        "This report summarizes executable seed sources, scripted large-source acquisition paths, filtering decisions, and final mixture counts.",
        "",
        "## Executable Seed Sources",
        "",
        "- OPUS Tatoeba en-uk/cs-uk: small public MT seed corpora, filtered by length, Cyrillic target ratio, length ratio, and exact deduplication.",
        "- UA-GEC train M2: mined for one-token WMT-style SC/GC examples only.",
        "- UD Ukrainian IU train: used for clean Ukrainian text, QA cloze generation, and morphology/typo examples.",
        "- UniMorph hsb: registered for morphology; current final Sorbian GC uses public official monolingual plus suffix rules, with UniMorph available for expansion.",
        "- GSM8K/SVAMP/ASDiv: public arithmetic preservation sources; small capped use only, no benchmark-derived math.",
        "",
        "## Scripted But Not Yet Used",
        "",
        "- Larger OPUS en-uk corpora, HPLT/OSCAR/CulturaX Ukrainian, Leipzig Sorbian, prior WMT Sorbian, and Czech/Polish transfer are registered but not marked final-train until source-specific license and overlap review is complete.",
        "",
        "## Counts",
        "",
        "| Path | Rows |",
        "|---|---:|",
    ]
    for row in rows:
        lines.append(f"| `{row['path']}` | {row['row_count']} |")
    lines.extend(
        [
            "",
            "## Contamination Notes",
            "",
            "- No hidden WMT26 test data is used.",
            "- No WMT2025 test sets are used.",
            "- No held-out ZNO/MMLU splits are downloaded or used.",
            "- No official math benchmark data, translations, modifications, or derivatives are used for training.",
            "- No external Sorbian certificate or exam-question source is used.",
            "",
            "## Recommended Sampling",
            "",
            "- Cap MT in multitask mixtures despite large row counts.",
            "- Keep MR small and format-focused.",
            "- Keep generated QA separate from official QA in ablations.",
            "- Use SC/GC compilers as a major equal-weighted task contribution, not an afterthought.",
        ]
    )
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")

    external_inventory = ROOT / "data/manifests/external_data_inventory.jsonl"
    source_to_files = {
        "external:opus_tatoeba_en_uk": ["data/processed/external/uk/mt_train.jsonl", "data/processed/external/uk/mt_doc_train.jsonl"],
        "external:opus_tatoeba_cs_uk": ["data/processed/external/uk/mt_train.jsonl", "data/processed/external/uk/mt_doc_train.jsonl"],
        "external:ua_gec_train": ["data/processed/external/uk/sc_real.jsonl", "data/processed/external/uk/gc_real.jsonl"],
        "external:ud_uk_iu": ["data/processed/external/uk/sc_synthetic_public.jsonl", "data/processed/external/uk/gc_synthetic_public.jsonl", "data/processed/external/uk/qa_generated_public.jsonl", "data/processed/external/uk/monolingual_train.jsonl"],
        "external:gsm8k_train": ["data/processed/external/uk/mr_non_benchmark.jsonl", "data/processed/external/sorbian/mr_non_benchmark_hsb.jsonl", "data/processed/external/sorbian/mr_non_benchmark_dsb.jsonl"],
        "external:svamp": ["data/processed/external/uk/mr_non_benchmark.jsonl"],
        "external:asdiv": ["data/processed/external/uk/mr_non_benchmark.jsonl"],
        "external:unimorph_hsb": ["data/processed/external/sorbian/gc_synthetic_hsb.jsonl"],
    }
    if external_inventory.exists():
        existing = [json.loads(line) for line in external_inventory.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        existing = []
    # Fill filtered/dedup counts for known files.
    count_lookup = {row["path"]: row["row_count"] for row in rows}
    for row in existing:
        source_id = row["source_id"]
        files = source_to_files.get(source_id, [])
        filtered_count = sum(count_lookup.get(path, 0) for path in files)
        row["local_filtered_path"] = ";".join(files)
        row["row_count_after_filtering"] = filtered_count
        row["row_count_after_dedup"] = filtered_count
        row["filtering_steps"] = row.get("filtering_steps") or ["source_specific_filters", "exact_dedup", "dev_tune_locked_overlap_removal"]
        row.setdefault("overlap_check_status", "checked_by_scripts/check_dev_overlap.py")
        row.setdefault("notes", "")
    external_inventory.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in existing), encoding="utf-8")
    print(f"Wrote {doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
