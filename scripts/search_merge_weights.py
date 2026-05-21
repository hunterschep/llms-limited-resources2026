#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from merge_task_vectors import write_dry_run


def candidate_weights(grid: dict[str, list[float]], limit: int) -> list[dict[str, float]]:
    keys = list(grid)
    values = [grid[k] for k in keys]
    out = []
    for combo in itertools.product(*values):
        out.append(dict(zip(keys, combo)))
        if len(out) >= limit:
            break
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=16)
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    candidates = candidate_weights(config.get("search_grid", {}), args.limit)
    out_dir = ROOT / config["output_dir"] / "search"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx, weights in enumerate(candidates):
        rows.append({"candidate_id": idx, "weights": weights, "objective": config.get("objective"), "status": "pending_eval"})
        if args.dry_run:
            write_dry_run(config, f"search_candidate_{idx:03d}", weights)
    (out_dir / "candidate_weights.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} merge candidates to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
