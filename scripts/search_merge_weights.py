#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import itertools
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from merge_task_vectors import linear_task_vector_merge, resolve_output_dir, write_dry_run


def candidate_weights(grid: dict[str, list[float]], limit: int) -> list[dict[str, float]]:
    if limit <= 0:
        return []
    keys = list(grid)
    values = [grid[k] for k in keys]
    out = []
    for combo in itertools.product(*values):
        out.append(dict(zip(keys, combo)))
        if len(out) >= limit:
            break
    return out


def configured_candidates(config: dict, limit: int) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    seen: set[str] = set()
    for row in config.get("candidate_weights", []) or []:
        weights = {str(k): float(v) for k, v in row.items()}
        key = json.dumps(weights, sort_keys=True)
        if key not in seen:
            rows.append(weights)
            seen.add(key)
        if len(rows) >= limit:
            return rows
    for weights in candidate_weights(config.get("search_grid", {}), max(0, limit - len(rows))):
        key = json.dumps(weights, sort_keys=True)
        if key not in seen:
            rows.append(weights)
            seen.add(key)
    return rows


def append_search_record(config: dict, config_path: str, out_dir: Path, rows: list[dict]) -> None:
    if os.environ.get("WMT26_RECORD_RUNS", "1") == "0":
        return
    record = {
        "merge_id": f"{config.get('track')}_search_{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "track": config.get("track"),
        "base_checkpoint": config.get("base_model"),
        "candidate_checkpoints": config.get("specialists", {}),
        "merge_method": "weight_search",
        "merge_weights": [row["weights"] for row in rows],
        "merge_config": config_path,
        "output_checkpoint": str(out_dir.relative_to(ROOT)) if out_dir.is_relative_to(ROOT) else str(out_dir),
        "eval_id": None,
        "overall_score": None,
        "per_task_scores": {},
        "status": "completed" if any(row.get("status") == "evaluated" for row in rows) else "pending_eval",
        "andromeda_job_id": os.environ.get("SLURM_JOB_ID"),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "notes": f"{len(rows)} candidates generated",
    }
    out = ROOT / "results/merge_runs.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def run_eval(config: dict, model_dir: Path, candidate_id: int, eval_limit: int | None) -> dict:
    eval_config = config["validation_config"]
    track = config["track"]
    result_dir = ROOT / "results" / "merge_search"
    result_dir.mkdir(parents=True, exist_ok=True)
    result_path = result_dir / f"{track}_candidate_{candidate_id:03d}.json"
    cmd = [
        sys.executable,
        "scripts/eval_model.py",
        "--config",
        eval_config,
        "--model",
        str(model_dir),
        "--output",
        str(result_path.relative_to(ROOT)),
    ]
    if eval_limit is not None:
        cmd.extend(["--limit", str(eval_limit)])
    subprocess.run(cmd, cwd=ROOT, check=True)
    return json.loads(result_path.read_text(encoding="utf-8"))


def update_best_pointer(out_dir: Path, best_dir: Path, best_row: dict) -> None:
    best_path = out_dir.parent / "best"
    if best_path.exists() or best_path.is_symlink():
        if best_path.is_symlink() or best_path.is_file():
            best_path.unlink()
        else:
            shutil.rmtree(best_path)
    try:
        best_path.symlink_to(best_dir, target_is_directory=True)
    except OSError:
        shutil.copytree(best_dir, best_path)
    (out_dir.parent / "best_candidate.json").write_text(json.dumps(best_row, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "candidate_id",
        "status",
        "overall_score",
        "MT_score",
        "QA_score",
        "SC_score",
        "GC_score",
        "MR_score",
        "checkpoint",
        "weights",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            aggregate = row.get("aggregate", {})
            writer.writerow(
                {
                    "candidate_id": row["candidate_id"],
                    "status": row.get("status"),
                    "overall_score": aggregate.get("overall_score"),
                    "MT_score": aggregate.get("MT_score"),
                    "QA_score": aggregate.get("QA_score"),
                    "SC_score": aggregate.get("SC_score"),
                    "GC_score": aggregate.get("GC_score"),
                    "MR_score": aggregate.get("MR_score"),
                    "checkpoint": row.get("checkpoint"),
                    "weights": json.dumps(row.get("weights", {}), sort_keys=True),
                    "notes": row.get("notes", ""),
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=16)
    parser.add_argument("--execute", action="store_true", help="Actually build and evaluate candidate merged models.")
    parser.add_argument("--eval-limit", type=int, default=None, help="Optional per-task evaluation limit for merge search.")
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    candidates = configured_candidates(config, args.limit)
    out_dir = resolve_output_dir(config["output_dir"]) / "search"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx, weights in enumerate(candidates):
        row = {"candidate_id": idx, "weights": weights, "objective": config.get("objective"), "status": "pending_eval"}
        if args.dry_run or not args.execute:
            write_dry_run(config, f"search_candidate_{idx:03d}", weights)
            if not args.execute:
                row["notes"] = "candidate generated; not executed"
        if args.execute and not args.dry_run:
            candidate_dir = linear_task_vector_merge(config, weights, output_name=f"search/candidate_{idx:03d}")
            row["checkpoint"] = str(candidate_dir)
            result = run_eval(config, candidate_dir, idx, args.eval_limit)
            row["aggregate"] = result.get("aggregate", {})
            row["task_scores"] = result.get("task_scores", {})
            row["status"] = "evaluated"
            row["notes"] = f"eval_limit={args.eval_limit}" if args.eval_limit is not None else "full evaluation"
        rows.append(row)
    (out_dir / "candidate_weights.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    write_csv(ROOT / "results" / f"merge_search_{config['track']}.csv", rows)
    evaluated = [row for row in rows if row.get("status") == "evaluated" and row.get("aggregate", {}).get("overall_score") is not None]
    if evaluated:
        best = max(evaluated, key=lambda row: float(row["aggregate"]["overall_score"]))
        update_best_pointer(out_dir, Path(best["checkpoint"]), best)
    append_search_record(config, args.config, out_dir, rows)
    print(f"Wrote {len(rows)} merge candidates to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
