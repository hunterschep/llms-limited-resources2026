#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from phase4_common import read_jsonl, write_json
from wmt26.eval.metrics import parse_edit_output


PAIRS = {
    "uk_sc": ("data/processed/final/uk/sc_train_final.jsonl", "data/processed/uk/sc_locked_validation.jsonl"),
    "uk_gc": ("data/processed/final/uk/gc_train_final.jsonl", "data/processed/uk/gc_locked_validation.jsonl"),
    "sorbian_sc": ("data/processed/final/sorbian/sc_train_final.jsonl", "data/processed/sorbian/sc_locked_validation.jsonl"),
    "sorbian_gc": ("data/processed/final/sorbian/gc_train_final.jsonl", "data/processed/sorbian/gc_locked_validation.jsonl"),
}


def summarize(path: str) -> dict:
    rows = read_jsonl(ROOT / path)
    labels = Counter()
    lengths = []
    for row in rows:
        wrong, _ = parse_edit_output(str(row.get("target", "")))
        labels["clean" if wrong == "CORRECT" else "error"] += 1
        lengths.append(len(str(row.get("input", "")).split()))
    return {
        "rows": len(rows),
        "labels": dict(labels),
        "avg_input_words": sum(lengths) / max(1, len(lengths)),
        "source_ids": dict(Counter(str(row.get("source_id")) for row in rows).most_common(20)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/phase4/status/train_eval_distribution_report.json")
    args = parser.parse_args()
    report = {name: {"train": summarize(train), "eval": summarize(eval_)} for name, (train, eval_) in PAIRS.items()}
    write_json(ROOT / args.output, report)
    md = ROOT / args.output.replace(".json", ".md")
    md.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Phase 4 Train/Eval Distribution Check", ""]
    for name, item in report.items():
        lines.append(f"## {name}")
        lines.append(f"- train: `{json.dumps(item['train'], ensure_ascii=False, sort_keys=True)}`")
        lines.append(f"- eval: `{json.dumps(item['eval'], ensure_ascii=False, sort_keys=True)}`")
        lines.append("")
    md.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output": args.output}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
