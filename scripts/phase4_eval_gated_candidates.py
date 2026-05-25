#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


SCALE_RE = re.compile(r"^(?P<adapter>.+)@scale=(?P<scale>[0-9.]+)$")


def scale_label(scale: float) -> str:
    return str(scale).replace(".", "p")


def safe_adapter_name(adapter: str) -> str:
    path = Path(adapter)
    parts = list(path.parts)
    if parts and parts[-1] == "adapter" and len(parts) >= 2:
        return parts[-2]
    return path.name or "adapter"


def parse_candidate(row: dict) -> dict | None:
    candidate = str(row.get("candidate", ""))
    match = SCALE_RE.match(candidate)
    if not match:
        return None
    scale = float(match.group("scale"))
    adapter = match.group("adapter")
    return {
        "candidate": candidate,
        "adapter": adapter,
        "adapter_scale": scale,
        "candidate_overall": float(row.get("candidate_overall", 0.0) or 0.0),
        "overall_delta": float(row.get("overall_delta", 0.0) or 0.0),
        "task_drops": row.get("task_drops", {}),
        "task_improvements": row.get("task_improvements", {}),
    }


def run_eval(config: str, model: str, output: str, adapter: str | None = None, adapter_scale: float | None = None) -> None:
    cmd = [sys.executable, "scripts/eval_model.py", "--config", config, "--model", model, "--output", output]
    if adapter:
        cmd.extend(["--adapter", adapter, "--adapter-scale", str(adapter_scale if adapter_scale is not None else 1.0)])
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True, help="JSON from phase4_check_no_harm_gates.py")
    parser.add_argument("--track", choices=["uk", "sorbian"], required=True)
    parser.add_argument("--limit-candidates", type=int, default=1)
    parser.add_argument("--min-adapter-scale", type=float, default=0.01)
    parser.add_argument("--skip-baseline", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT / args.candidates).read_text(encoding="utf-8"))
    parsed = [parse_candidate(row) for row in data.get("checks", []) if row.get("passed")]
    passed = [row for row in parsed if row and row["adapter_scale"] >= args.min_adapter_scale]
    passed.sort(key=lambda row: row["candidate_overall"], reverse=True)
    selected = passed[: max(0, args.limit_candidates)]
    out_dir = ROOT / "results/phase4/gated_eval"
    out_dir.mkdir(parents=True, exist_ok=True)
    config = "configs/eval/uk.yaml" if args.track == "uk" else "configs/eval/sorbian.yaml"
    eval_config = yaml.safe_load((ROOT / config).read_text(encoding="utf-8")) or {}
    base_model = eval_config.get("model", "Qwen/Qwen3.5-2B")
    plan = {
        "track": args.track,
        "config": config,
        "base_model": base_model,
        "candidate_report": args.candidates,
        "min_adapter_scale": args.min_adapter_scale,
        "limit_candidates": args.limit_candidates,
        "selected": selected,
        "dry_run": args.dry_run,
    }
    plan_path = out_dir / f"{args.track}_gated_eval_plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.dry_run:
        print(json.dumps({"status": "planned", "selected": len(selected), "plan": str(plan_path.relative_to(ROOT))}, indent=2))
        return 0
    if not selected:
        print(json.dumps({"status": "no_passed_candidates", "plan": str(plan_path.relative_to(ROOT))}, indent=2))
        return 0
    if not args.skip_baseline:
        baseline_output = f"results/phase4/gated_eval/{args.track}_prompt_only_anchor.json"
        if args.force or not (ROOT / baseline_output).exists():
            run_eval(config, base_model, baseline_output)
    for row in selected:
        name = f"{safe_adapter_name(row['adapter'])}_scale_{scale_label(row['adapter_scale'])}"
        output = f"results/phase4/gated_eval/{args.track}_{name}.json"
        if args.force or not (ROOT / output).exists():
            run_eval(config, base_model, output, row["adapter"], row["adapter_scale"])
    print(json.dumps({"status": "evaluated", "selected": len(selected), "plan": str(plan_path.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
