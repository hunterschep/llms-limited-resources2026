#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from phase4_common import read_jsonl, write_json, write_jsonl, write_yaml
from wmt26.eval.metrics import parse_edit_output


DEFAULT_CAPS = {
    "ukrainian": {"MT": 48, "QA": 48, "SC": 60, "GC": 60, "MR": 999},
    "sorbian": {"MT": 72, "QA": 48, "SC": 72, "GC": 72, "MR": 999},
}


SOURCE_CONFIGS = {
    "ukrainian": "configs/eval/uk.yaml",
    "sorbian": "configs/eval/sorbian.yaml",
}


def stratify_edit(rows: list[dict], cap: int, seed: int) -> list[dict]:
    error = []
    clean = []
    for row in rows:
        wrong, _ = parse_edit_output(str(row.get("target", "")))
        (clean if wrong == "CORRECT" else error).append(row)
    rng = random.Random(seed)
    rng.shuffle(error)
    rng.shuffle(clean)
    half = cap // 2
    selected = error[:half] + clean[: cap - half]
    if len(selected) < min(cap, len(rows)):
        seen = {row.get("id") for row in selected}
        rest = [row for row in error + clean if row.get("id") not in seen]
        selected.extend(rest[: min(cap, len(rows)) - len(selected)])
    rng.shuffle(selected)
    return selected


def sample_rows(task: str, rows: list[dict], cap: int, seed: int) -> list[dict]:
    if task in {"SC", "GC"}:
        return stratify_edit(rows, cap, seed)
    if task == "MR":
        return rows[:cap]
    rng = random.Random(seed)
    buckets: dict[str, list[dict]] = {}
    for row in rows:
        key = f"{row.get('source_language') or row.get('language')}->{row.get('target_language') or ''}:{row.get('source_id')}"
        buckets.setdefault(key, []).append(row)
    selected: list[dict] = []
    for key in sorted(buckets):
        bucket = list(buckets[key])
        rng.shuffle(bucket)
        selected.extend(bucket[: max(1, cap // max(1, len(buckets)))])
    if len(selected) < min(cap, len(rows)):
        seen = {row.get("id") for row in selected}
        rest = [row for row in rows if row.get("id") not in seen]
        rng.shuffle(rest)
        selected.extend(rest[: min(cap, len(rows)) - len(selected)])
    return selected[:cap]


def build_track(track: str, seed: int) -> dict:
    import yaml

    config = yaml.safe_load((ROOT / SOURCE_CONFIGS[track]).read_text(encoding="utf-8")) or {}
    slug = "uk" if track == "ukrainian" else "sorbian"
    out_dir = ROOT / "data/processed/phase4_probe"
    out_dir.mkdir(parents=True, exist_ok=True)
    combined: list[dict] = []
    config_datasets: dict[str, list[str]] = {}
    manifest_tasks = {}
    for idx, (task, files) in enumerate(config.get("datasets", {}).items()):
        rows: list[dict] = []
        for rel in files:
            rows.extend(read_jsonl(ROOT / rel))
        cap = DEFAULT_CAPS[track].get(task, 50)
        sampled = sample_rows(task, rows, cap, seed + idx)
        for row in sampled:
            row = dict(row)
            row["split"] = "locked_validation"
            row.setdefault("metadata", {})["phase4_probe"] = True
            combined.append(row)
        task_path = out_dir / f"{slug}_probe_{task.lower()}.jsonl"
        count = write_jsonl(task_path, sampled)
        config_datasets[task] = [str(task_path.relative_to(ROOT))]
        manifest_tasks[task] = {"source_rows": len(rows), "probe_rows": count}
    combined_path = out_dir / f"{slug}_probe.jsonl"
    write_jsonl(combined_path, combined)
    probe_config = {
        "track": track,
        "model": config.get("model", "Qwen/Qwen3.5-2B"),
        "max_new_tokens": 192,
        "batch_size": 16,
        "split": "phase4_probe",
        "datasets": config_datasets,
        "scoring": config.get("scoring", {}),
    }
    config_path = ROOT / f"configs/eval/phase4_probe_{slug}.yaml"
    write_yaml(config_path, probe_config)
    return {
        "track": track,
        "combined_path": str(combined_path.relative_to(ROOT)),
        "config_path": str(config_path.relative_to(ROOT)),
        "tasks": manifest_tasks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2606)
    args = parser.parse_args()
    reports = [build_track("ukrainian", args.seed), build_track("sorbian", args.seed)]
    out = ROOT / "results/phase4/probe/probe_manifest.json"
    write_json(out, {"seed": args.seed, "reports": reports})
    print(json.dumps({"output": str(out), "reports": reports}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
