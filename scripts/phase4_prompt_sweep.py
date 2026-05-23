#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from eval_model import generate_predictions, load_generation_bundle, read_jsonl, score_task
from phase4_common import read_yaml, write_json
from wmt26.eval.metrics import aggregate_wmt_scores


def apply_variant(row: dict, task: str, variant: dict) -> dict:
    row = copy.deepcopy(row)
    system_append = (variant.get("system_append_by_task") or {}).get(task, "")
    user_append = (variant.get("user_append_by_task") or {}).get(task, "")
    for message in row.get("messages", []):
        if message.get("role") == "system" and system_append:
            message["content"] = message.get("content", "").rstrip() + system_append + "\n"
        if message.get("role") == "user" and user_append:
            message["content"] = message.get("content", "").rstrip() + "\n" + user_append + "\n"
    return row


def evaluate_variant(probe_config: dict, model: str, variant: dict, oracle: bool, batch_size: int) -> dict:
    task_scores: dict[str, dict[str, float]] = {}
    bundle = None if oracle else load_generation_bundle(model)
    for task, files in probe_config.get("datasets", {}).items():
        rows: list[dict] = []
        for rel in files:
            rows.extend(read_jsonl(ROOT / rel))
        rows = [apply_variant(row, task, variant) for row in rows]
        refs = [str(row.get("target", "")) for row in rows]
        if oracle:
            preds = refs[:]
        else:
            max_new = int((variant.get("max_new_tokens_by_task") or {}).get(task, probe_config.get("max_new_tokens", 192)))
            preds = generate_predictions(bundle, rows, max_new, batch_size, task=task)
        task_scores[task] = score_task(task, preds, refs)
    return {
        "track": probe_config.get("track"),
        "model": model,
        "variant_id": variant["id"],
        "description": variant.get("description", ""),
        "task_scores": task_scores,
        "aggregate": aggregate_wmt_scores(task_scores),
        "oracle": oracle,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--oracle", action="store_true")
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    cfg = read_yaml(ROOT / args.config)
    probe = read_yaml(ROOT / cfg["probe_config"])
    sweep = read_yaml(ROOT / cfg["prompt_sweep_config"])
    model = args.model or cfg.get("model") or probe.get("model")
    out_dir = ROOT / cfg.get("output_dir", "results/phase4/prompt_sweep")
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    for variant in sweep.get("variants", []):
        result = evaluate_variant(probe, model, variant, args.oracle, args.batch_size)
        output = out_dir / f"{variant['id']}.json"
        write_json(output, result)
        summary.append({"variant": variant["id"], "overall": result["aggregate"].get("overall_score"), "output": str(output.relative_to(ROOT))})
    write_json(out_dir / "summary.json", {"config": args.config, "model": model, "oracle": args.oracle, "variants": summary})
    print(json.dumps({"output_dir": str(out_dir), "variants": summary}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
