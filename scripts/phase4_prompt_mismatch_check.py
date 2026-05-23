#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase4_common import read_jsonl, write_json


FILES = {
    "uk_train_sc": "data/processed/final/uk/sc_train_final.jsonl",
    "uk_eval_sc": "data/processed/uk/sc_locked_validation.jsonl",
    "uk_train_gc": "data/processed/final/uk/gc_train_final.jsonl",
    "uk_eval_gc": "data/processed/uk/gc_locked_validation.jsonl",
    "uk_train_mr": "data/processed/final/uk/mr_train_final.jsonl",
    "uk_eval_mr": "data/processed/uk/mr_locked_validation.jsonl",
    "sorbian_train_sc": "data/processed/final/sorbian/sc_train_final.jsonl",
    "sorbian_eval_sc": "data/processed/sorbian/sc_locked_validation.jsonl",
    "sorbian_train_gc": "data/processed/final/sorbian/gc_train_final.jsonl",
    "sorbian_eval_gc": "data/processed/sorbian/gc_locked_validation.jsonl",
    "sorbian_train_mr": "data/processed/final/sorbian/mr_train_final.jsonl",
    "sorbian_eval_mr": "data/processed/sorbian/mr_locked_validation.jsonl",
}


def first_messages(path: str) -> dict:
    rows = read_jsonl(ROOT / path, 25)
    systems = defaultdict(int)
    users = defaultdict(int)
    for row in rows:
        for msg in row.get("messages", []):
            if msg.get("role") == "system":
                systems[msg.get("content", "").strip()] += 1
            elif msg.get("role") == "user":
                users[msg.get("content", "").splitlines()[0].strip() if msg.get("content") else ""] += 1
    return {"system_prompts": dict(systems), "user_first_lines": dict(users)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/phase4/status/prompt_mismatch_report.json")
    args = parser.parse_args()
    report = {name: first_messages(path) for name, path in FILES.items()}
    write_json(ROOT / args.output, report)
    print(json.dumps({"output": args.output}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
