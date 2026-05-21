#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from eval_model import generate_predictions, load_generation_bundle, read_jsonl


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")[:100] or "model"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare base and trained-checkpoint generations on identical prompts.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--base-model", default="Qwen/Qwen3.5-2B")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--tasks", nargs="*", default=None)
    parser.add_argument("--per-task", type=int, default=10)
    parser.add_argument("--output", default=None)
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    tasks = args.tasks or list(config.get("datasets", {}).keys())
    rows: list[dict] = []
    for task in tasks:
        for rel in config.get("datasets", {}).get(task, []):
            task_rows = read_jsonl(ROOT / rel, args.per_task)
            for row in task_rows[: args.per_task]:
                row = dict(row)
                row["_triage_task"] = task
                rows.append(row)
    max_new_tokens = int(args.max_new_tokens or config.get("max_new_tokens", 128))
    batch_size = int(args.batch_size or config.get("batch_size", 4))

    base_bundle = load_generation_bundle(args.base_model)
    checkpoint_bundle = load_generation_bundle(args.checkpoint)
    base_predictions = generate_predictions(base_bundle, rows, max_new_tokens, batch_size, task="checkpoint_base")
    checkpoint_predictions = generate_predictions(checkpoint_bundle, rows, max_new_tokens, batch_size, task="checkpoint_candidate")

    records = []
    identical = 0
    for row, base_pred, checkpoint_pred in zip(rows, base_predictions, checkpoint_predictions):
        same = base_pred == checkpoint_pred
        identical += int(same)
        records.append(
            {
                "task": row.get("_triage_task"),
                "id": row.get("id"),
                "target": row.get("target"),
                "base_prediction": base_pred,
                "checkpoint_prediction": checkpoint_pred,
                "base_hash": digest(base_pred),
                "checkpoint_hash": digest(checkpoint_pred),
                "identical": same,
            }
        )
    summary = {
        "base_model": args.base_model,
        "checkpoint": args.checkpoint,
        "rows": len(records),
        "identical_outputs": identical,
        "identical_rate": identical / max(1, len(records)),
    }
    out = ROOT / (args.output or f"results/triage/checkpoint_loading/{safe_name(args.checkpoint)}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    out.with_suffix(out.suffix + ".summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "summary": summary}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
