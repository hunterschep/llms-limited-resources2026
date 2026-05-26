#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from eval_model import generate_predictions, load_generation_bundle, oracle_predictions, read_jsonl, score_task
from wmt26.eval.metrics import aggregate_wmt_scores, mt_scores


def direction(row: dict[str, Any]) -> str:
    src = row.get("source_language") or (row.get("metadata") or {}).get("source_language") or "unknown"
    tgt = row.get("target_language") or (row.get("metadata") or {}).get("target_language") or row.get("language") or "unknown"
    return f"{src}->{tgt}"


def eval_config(config_path: Path, model: str | None, adapter: str | None, adapter_scale: float, oracle: bool, limit: int | None) -> dict:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    model_name = model or config.get("model")
    bundle = None if oracle else load_generation_bundle(model_name, adapter, adapter_scale)
    task_scores: dict[str, dict[str, float]] = {}
    direction_scores: dict[str, dict[str, float]] = {}
    raw_rows = []
    for task, files in config.get("datasets", {}).items():
        rows: list[dict[str, Any]] = []
        for rel in files:
            rows.extend(read_jsonl(ROOT / rel, limit))
        if limit:
            rows = rows[:limit]
        refs = [str(row.get("target", "")) for row in rows]
        preds = oracle_predictions(rows) if oracle else generate_predictions(bundle, rows, int(config.get("max_new_tokens", 256)), int(config.get("batch_size", 4)), task=task)
        task_scores[task] = score_task(task, preds, refs)
        if task == "MT":
            by_direction: dict[str, tuple[list[str], list[str]]] = {}
            for row, pred, ref in zip(rows, preds, refs):
                key = direction(row)
                by_direction.setdefault(key, ([], []))
                by_direction[key][0].append(pred)
                by_direction[key][1].append(ref)
            direction_scores = {key: mt_scores(pair[0], pair[1]) for key, pair in sorted(by_direction.items())}
        for row, pred, ref in zip(rows, preds, refs):
            raw_rows.append(
                {
                    "id": row.get("id"),
                    "task": task,
                    "direction": direction(row) if task == "MT" else None,
                    "prediction": pred,
                    "reference": ref,
                }
            )
    return {
        "track": config.get("track"),
        "model": model_name,
        "adapter": adapter,
        "adapter_scale": adapter_scale if adapter else None,
        "oracle": oracle,
        "task_scores": task_scores,
        "direction_scores": direction_scores,
        "aggregate": aggregate_wmt_scores(task_scores),
        "raw_predictions": raw_rows,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--adapter-scale", type=float, default=1.0)
    parser.add_argument("--oracle", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-output", default=None)
    args = parser.parse_args()
    result = eval_config(ROOT / args.config, args.model, args.adapter, args.adapter_scale, args.oracle, args.limit)
    raw = result.pop("raw_predictions")
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.raw_output:
        raw_path = ROOT / args.raw_output
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        with raw_path.open("w", encoding="utf-8") as handle:
            for row in raw:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(result["aggregate"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
