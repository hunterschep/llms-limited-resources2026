#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_b_rescue_common import (  # noqa: E402
    PROCESSED_REPAIR_DIR,
    assistant_row,
    count_by,
    deterministic_sample,
    direction,
    git_commit,
    grouped_sample,
    read_jsonl,
    sha256_path,
    write_json,
    write_jsonl,
)


def _load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _with_repair_metadata(row: dict[str, Any], generation_method: str, split: str = "train") -> dict[str, Any]:
    new_row = dict(row)
    new_row["split"] = split
    new_row["track"] = "sorbian"
    new_row["contamination_checked"] = True
    new_row["generation_method"] = generation_method
    metadata = dict(new_row.get("metadata") or {})
    metadata["stage_b_rescue"] = True
    new_row["metadata"] = metadata
    return new_row


def _target_from_task(task: str, sentence: str, language: str, source_id: str, idx: int) -> dict[str, Any]:
    task_word = "spelling-error" if task == "SC" else "grammatical-error"
    return {
        "id": f"stage-b-clean-{task.lower()}-{language}-{idx:06d}",
        "track": "sorbian",
        "task": task,
        "language": language,
        "source_language": None,
        "target_language": None,
        "source_type": "official_or_public_anchor",
        "source_id": source_id,
        "license": "inherited-from-source",
        "split": "train",
        "input": sentence,
        "target": "Wrong word: CORRECT\nCorrect word: CORRECT",
        "is_synthetic": True,
        "contamination_checked": True,
        "generation_method": "stage_b_rescue_hard_no_error_from_public_mt_anchor",
        "metadata": {"stage_b_rescue": True, "clean_no_error": True},
        "messages": [
            {
                "role": "system",
                "content": f'You perform {task_word} detection and correction. Return exactly two lines: "Wrong word: <word or CORRECT>" and "Correct word: <word or CORRECT>".\n',
            },
            {"role": "user", "content": f"Sentence:\n{sentence}\n"},
            {"role": "assistant", "content": "Wrong word: CORRECT\nCorrect word: CORRECT"},
        ],
    }


def _sorbian_side(row: dict[str, Any]) -> tuple[str, str] | None:
    src = row.get("source_language")
    tgt = row.get("target_language")
    if src in {"hsb", "dsb"} and row.get("input"):
        return str(row["input"]), str(src)
    if tgt in {"hsb", "dsb"} and row.get("target"):
        return str(row["target"]), str(tgt)
    return None


def build_mr(config: dict[str, Any], seed: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rel in config["sources"]["mr"]:
        rows.extend(read_jsonl(ROOT / rel))
    rows = [_with_repair_metadata(row, "stage_b_rescue_mr_final_answer_repair") for row in rows]
    return deterministic_sample(rows, int(config["limits"]["mr_examples"]), seed)


def build_edit(config: dict[str, Any], seed: int) -> list[dict[str, Any]]:
    error_rows: list[dict[str, Any]] = []
    for rel in config["sources"]["edit_errors"]:
        for row in read_jsonl(ROOT / rel):
            task = row.get("task")
            if task in {"SC", "GC"}:
                error_rows.append(_with_repair_metadata(row, "stage_b_rescue_one_word_edit_error_repair"))
    mt_rows = [row for row in read_jsonl(ROOT / config["sources"]["mt_anchor"]) if row.get("task") == "MT"]
    clean_candidates: list[dict[str, Any]] = []
    seen_sentences: set[str] = set()
    for row in mt_rows:
        side = _sorbian_side(row)
        if not side:
            continue
        sentence, language = side
        normalized = " ".join(sentence.split())
        if len(normalized) < 20 or normalized in seen_sentences:
            continue
        seen_sentences.add(normalized)
        task = "SC" if len(clean_candidates) % 2 == 0 else "GC"
        clean_candidates.append(_target_from_task(task, normalized, language, str(row.get("source_id", "unknown")), len(clean_candidates)))
    rng = random.Random(seed)
    rng.shuffle(error_rows)
    rng.shuffle(clean_candidates)
    per_task_error_limit = int(config["limits"]["edit_error_examples_per_task"])
    per_task_clean_limit = int(config["limits"]["edit_clean_examples_per_task"])
    selected: list[dict[str, Any]] = []
    for task in ("SC", "GC"):
        task_errors = [row for row in error_rows if row.get("task") == task][:per_task_error_limit]
        task_clean = [row for row in clean_candidates if row.get("task") == task][:per_task_clean_limit]
        selected.extend(task_errors)
        selected.extend(task_clean)
    rng.shuffle(selected)
    return selected


def build_format(config: dict[str, Any], seed: int, mr_rows: list[dict[str, Any]], edit_rows: list[dict[str, Any]], mt_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rng = random.Random(seed)
    for row in deterministic_sample(mr_rows, min(24, len(mr_rows)), seed):
        rows.append(_with_repair_metadata(row, "stage_b_rescue_format_mr_final_answer"))
    for row in deterministic_sample(edit_rows, min(48, len(edit_rows)), seed + 1):
        rows.append(_with_repair_metadata(row, "stage_b_rescue_format_exact_edit_two_line"))
    for row in grouped_sample(mt_rows, "direction", min(60, len(mt_rows)), seed + 2):
        rows.append(_with_repair_metadata(row, "stage_b_rescue_format_mt_translation_only"))
    rng.shuffle(rows)
    return rows[: int(config["limits"]["format_examples"])]


def build_mt_anchor(config: dict[str, Any], seed: int) -> list[dict[str, Any]]:
    rows = [row for row in read_jsonl(ROOT / config["sources"]["mt_anchor"]) if row.get("task") == "MT"]
    selected = grouped_sample(rows, "direction", int(config["limits"]["mt_anchor_examples"]), seed)
    return [_with_repair_metadata(row, "stage_b_rescue_mt_anchor_replay") for row in selected]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "rows": len(rows),
        "by_task": count_by(rows, "task"),
        "by_language": count_by(rows, "language"),
        "by_generation_method": count_by(rows, "generation_method"),
        "by_source_id_top20": dict(Counter(str(row.get("source_id", "unknown")) for row in rows).most_common(20)),
    }


def write_markdown(summary: dict[str, Any]) -> None:
    doc = ROOT / "docs/86_stage_b_repair_data.md"
    lines = [
        "# Stage B Repair Data",
        "",
        f"Generated at commit `{summary['git_commit']}`.",
        "",
        "The repair dataset is intentionally small and targeted. It is not a repeat of the failed Stage C broad replay.",
        "",
        "## Outputs",
        "",
    ]
    for name, info in summary["outputs"].items():
        lines.append(f"- `{name}`: `{info['path']}` ({info['rows']} rows, sha256 `{info['sha256']}`)")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "- MR rows come from governed public non-PolyMath arithmetic sources and keep final-answer-only targets.",
            "- Edit errors come from governed synthetic SC/GC compilers; clean hard negatives are generated from public/official Sorbian MT anchor text, not locked validation.",
            "- MT anchor rows are sampled from the Stage B MT training pool across all six directions.",
            "- Every row carries `source_id`, `task`, `language`, `split`, `generation_method`, and `contamination_checked`.",
        ]
    )
    for name, info in summary["outputs"].items():
        lines.extend(["", f"## {name}", ""])
        lines.append("```json")
        lines.append(json.dumps(info["summary"], ensure_ascii=False, indent=2, sort_keys=True))
        lines.append("```")
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data/stage_b_repair_sorbian.yaml")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()
    config = _load_config(ROOT / args.config)
    seed = int(args.seed if args.seed is not None else config.get("seed", 2606))
    PROCESSED_REPAIR_DIR.mkdir(parents=True, exist_ok=True)

    mr_rows = build_mr(config, seed)
    edit_rows = build_edit(config, seed + 1)
    mt_rows = build_mt_anchor(config, seed + 2)
    format_rows = build_format(config, seed + 3, mr_rows, edit_rows, mt_rows)
    combined_rows = list(mr_rows) + list(edit_rows) + list(format_rows) + list(mt_rows)
    random.Random(seed + 4).shuffle(combined_rows)

    outputs = {
        "mr_repair": PROCESSED_REPAIR_DIR / "mr_repair.jsonl",
        "edit_repair": PROCESSED_REPAIR_DIR / "edit_repair.jsonl",
        "format_repair": PROCESSED_REPAIR_DIR / "format_repair.jsonl",
        "mt_anchor": PROCESSED_REPAIR_DIR / "mt_anchor.jsonl",
        "combined_repair": PROCESSED_REPAIR_DIR / "combined_repair.jsonl",
    }
    rows_by_name = {
        "mr_repair": mr_rows,
        "edit_repair": edit_rows,
        "format_repair": format_rows,
        "mt_anchor": mt_rows,
        "combined_repair": combined_rows,
    }
    manifest_outputs = {}
    for name, path in outputs.items():
        rows = rows_by_name[name]
        write_jsonl(path, rows)
        manifest_outputs[name] = {
            "path": str(path.relative_to(ROOT)),
            "rows": len(rows),
            "sha256": sha256_path(path),
            "summary": summarize(rows),
        }
    manifest = {
        "config": args.config,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "track": "sorbian",
        "stage_b_anchor": "checkpoints/competitive_reboot/sorbian/stage_b_mt_large",
        "outputs": manifest_outputs,
    }
    write_json(ROOT / "data/manifests/stage_b_repair_sorbian.json", manifest)
    write_json(ROOT / "results/stage_b_rescue/data/repair_data_summary.json", manifest)
    write_markdown(manifest)
    print(json.dumps({name: info["rows"] for name, info in manifest_outputs.items()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
