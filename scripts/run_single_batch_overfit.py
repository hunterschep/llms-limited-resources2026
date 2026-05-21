#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


DEFAULT_TRAIN_FILES = {
    ("uk", "MT"): "data/processed/final/uk/mt_train_final.jsonl",
    ("uk", "QA"): "data/processed/final/uk/qa_train_final.jsonl",
    ("uk", "SC"): "data/processed/final/uk/sc_train_final.jsonl",
    ("uk", "GC"): "data/processed/final/uk/gc_train_final.jsonl",
    ("uk", "MR"): "data/processed/final/uk/mr_train_final.jsonl",
    ("sorbian", "MT"): "data/processed/final/sorbian/mt_train_final.jsonl",
    ("sorbian", "QA"): "data/processed/final/sorbian/qa_train_final.jsonl",
    ("sorbian", "SC"): "data/processed/final/sorbian/sc_train_final.jsonl",
    ("sorbian", "GC"): "data/processed/final/sorbian/gc_train_final.jsonl",
    ("sorbian", "MR"): "data/processed/final/sorbian/mr_train_final.jsonl",
}


def read_jsonl(path: Path, limit: int) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                rows.append(row)
                if len(rows) >= limit:
                    break
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare or run a tiny same-set overfit test for one WMT26 task.")
    parser.add_argument("--track", choices=["uk", "sorbian"], required=True)
    parser.add_argument("--task", choices=["MT", "QA", "SC", "GC", "MR"], required=True)
    parser.add_argument("--examples", type=int, default=50)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--base-model-path", default=None)
    parser.add_argument("--train-file", default=None)
    parser.add_argument("--execute", action="store_true", help="Actually train and evaluate. Default only writes the reproducible triage config.")
    parser.add_argument("--dry-run", action="store_true", help="Pass --dry-run to train_sft.py.")
    args = parser.parse_args()

    source = ROOT / (args.train_file or DEFAULT_TRAIN_FILES[(args.track, args.task)])
    rows = read_jsonl(source, args.examples)
    if not rows:
        raise ValueError(f"No rows available for overfit test: {source}")
    out_dir = ROOT / "results/triage/overfit" / args.track / args.task.lower()
    train_jsonl = out_dir / "train_eval.jsonl"
    train_config = out_dir / "train_config.yaml"
    eval_config = out_dir / "eval_config.yaml"
    checkpoint = f"checkpoints/triage/overfit/{args.track}/{args.task.lower()}"
    write_jsonl(train_jsonl, rows)

    train_cfg = {
        "run_name": f"triage_overfit_{args.track}_{args.task.lower()}",
        "track": "ukrainian" if args.track == "uk" else "sorbian",
        "method": "single_batch_overfit",
        "specialist": args.task.lower(),
        "model_config": "configs/model/qwen35_2b.yaml",
        "base_model_path": args.base_model_path,
        "fallback_to_base_if_missing": True,
        "train_files": [str(train_jsonl.relative_to(ROOT))],
        "output_dir": checkpoint,
        "adapter": "lora",
        "lora_r": 16,
        "lora_alpha": 32,
        "lora_dropout": 0.0,
        "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
        "learning_rate": 5e-4,
        "batch_size": 1,
        "gradient_accumulation_steps": 1,
        "max_steps": args.steps,
        "max_length": 1024,
        "log_every": 10,
        "seed": 2603,
    }
    eval_cfg = {
        "track": "ukrainian" if args.track == "uk" else "sorbian",
        "model": checkpoint,
        "max_new_tokens": 128 if args.task != "MT" else 256,
        "batch_size": 4,
        "datasets": {args.task: [str(train_jsonl.relative_to(ROOT))]},
        "scoring": {"convention": "0-100", "overall": "single_task_overfit"},
    }
    train_config.write_text(yaml.safe_dump(train_cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    eval_config.write_text(yaml.safe_dump(eval_cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    manifest = {
        "train_jsonl": str(train_jsonl.relative_to(ROOT)),
        "train_config": str(train_config.relative_to(ROOT)),
        "eval_config": str(eval_config.relative_to(ROOT)),
        "checkpoint": checkpoint,
        "rows": len(rows),
        "execute": args.execute,
        "dry_run": args.dry_run,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if not args.execute:
        return 0

    train_cmd = [sys.executable, "scripts/train_sft.py", "--config", str(train_config.relative_to(ROOT))]
    if args.dry_run:
        train_cmd.append("--dry-run")
    subprocess.run(train_cmd, cwd=ROOT, check=True)
    subprocess.run(
        [
            sys.executable,
            "scripts/eval_model.py",
            "--config",
            str(eval_config.relative_to(ROOT)),
            "--model",
            checkpoint,
            "--output",
            str((out_dir / "eval.json").relative_to(ROOT)),
        ],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
