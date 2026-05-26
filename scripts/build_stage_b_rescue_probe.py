#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_b_rescue_common import (  # noqa: E402
    PROCESSED_REPAIR_DIR,
    count_by,
    deterministic_sample,
    direction,
    git_commit,
    grouped_sample,
    read_jsonl,
    sha256_path,
    validation_path,
    write_json,
    write_jsonl,
)


def _balanced_edit(rows: list[dict[str, Any]], limit: int, seed: int) -> list[dict[str, Any]]:
    clean = [row for row in rows if "Wrong word: CORRECT" in str(row.get("target", ""))]
    error = [row for row in rows if row not in clean]
    half = max(1, limit // 2)
    selected = deterministic_sample(clean, half, seed) + deterministic_sample(error, limit - half, seed + 1)
    random.Random(seed + 2).shuffle(selected)
    return selected


def write_eval_config(outputs: dict[str, Path], model: str = "Qwen/Qwen3.5-2B") -> None:
    config = {
        "track": "sorbian",
        "model": model,
        "max_new_tokens": 192,
        "batch_size": 16,
        "split": "stage_b_rescue_probe",
        "datasets": {task: [str(path.relative_to(ROOT))] for task, path in outputs.items()},
        "scoring": {"convention": "0-100", "overall": "equal_weighted_mean_of_MT_QA_SC_GC_MR"},
    }
    out = ROOT / "configs/eval/stage_b_rescue_probe_sorbian.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")


def write_markdown(manifest: dict[str, Any]) -> None:
    doc = ROOT / "docs/88_stage_b_rescue_probe.md"
    lines = [
        "# Stage B Rescue Probe",
        "",
        f"Generated at commit `{manifest['git_commit']}`.",
        "",
        "This probe is a fixed-seed, low-cost gate before full locked validation. It samples all five Sorbian tasks, keeps all MR rows because MR is tiny, and stratifies MT across all six directions.",
        "",
        "## Outputs",
        "",
    ]
    for task, info in manifest["outputs"].items():
        lines.append(f"- `{task}`: `{info['path']}` ({info['rows']} rows, sha256 `{info['sha256']}`)")
    lines.extend(
        [
            "",
            "## Probe Gates",
            "",
            "- MT average chrF++ must stay at or above `41.0`.",
            "- MR must be at least Stage B MR on the probe and preferably recover prompt-only.",
            "- SC/GC must not drop by more than one point relative to Stage B probe scores.",
            "- Malformed edit output must not spike.",
            "- Overall probe score must beat the Stage B probe before full evaluation.",
        ]
    )
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2606)
    parser.add_argument("--mt-per-direction", type=int, default=60)
    parser.add_argument("--qa", type=int, default=160)
    parser.add_argument("--edit", type=int, default=240)
    args = parser.parse_args()
    out_dir = PROCESSED_REPAIR_DIR / "probe"
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "MT": out_dir / "mt_probe.jsonl",
        "QA": out_dir / "qa_probe.jsonl",
        "SC": out_dir / "sc_probe.jsonl",
        "GC": out_dir / "gc_probe.jsonl",
        "MR": out_dir / "mr_probe.jsonl",
    }
    mt_rows = read_jsonl(validation_path("MT"))
    directions = sorted({direction(row) for row in mt_rows})
    mt_limit = max(args.mt_per_direction * max(1, len(directions)), args.mt_per_direction)
    rows_by_task = {
        "MT": grouped_sample(mt_rows, "direction", mt_limit, args.seed),
        "QA": deterministic_sample(read_jsonl(validation_path("QA")), args.qa, args.seed + 1),
        "SC": _balanced_edit(read_jsonl(validation_path("SC")), args.edit, args.seed + 2),
        "GC": _balanced_edit(read_jsonl(validation_path("GC")), args.edit, args.seed + 3),
        "MR": read_jsonl(validation_path("MR")),
    }
    manifest_outputs: dict[str, Any] = {}
    for task, path in outputs.items():
        rows = rows_by_task[task]
        write_jsonl(path, rows)
        manifest_outputs[task] = {
            "path": str(path.relative_to(ROOT)),
            "rows": len(rows),
            "sha256": sha256_path(path),
            "by_language": count_by(rows, "language"),
            "by_direction": count_by(rows, "direction") if task == "MT" else {},
        }
    write_eval_config(outputs)
    manifest = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "seed": args.seed,
        "outputs": manifest_outputs,
        "eval_config": "configs/eval/stage_b_rescue_probe_sorbian.yaml",
    }
    write_json(ROOT / "data/manifests/stage_b_rescue_probe_sorbian.json", manifest)
    write_json(ROOT / "results/stage_b_rescue/probe/probe_manifest.json", manifest)
    write_markdown(manifest)
    print(json.dumps({task: info["rows"] for task, info in manifest_outputs.items()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
