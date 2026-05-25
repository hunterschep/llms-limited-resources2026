#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def score_line(label: str, rel: str) -> str:
    data = read_json(rel)
    agg = data.get("aggregate", {})
    if not agg:
        return f"- {label}: missing `{rel}`"
    return (
        f"- {label}: overall {agg.get('overall_score', 0):.3f}; "
        f"MT {agg.get('MT_score', 0):.3f}, QA {agg.get('QA_score', 0):.3f}, "
        f"SC {agg.get('SC_score', 0):.3f}, GC {agg.get('GC_score', 0):.3f}, "
        f"MR {agg.get('MR_score', 0):.3f}"
    )


def sweep_summary(track: str) -> str:
    data = read_json(f"results/phase4/prompt_sweep/{track}/summary.json")
    variants = data.get("variants", [])
    if not variants:
        return f"- {track}: prompt sweep missing"
    best = max(variants, key=lambda row: row.get("overall", float("-inf")))
    return f"- {track}: best prompt variant `{best.get('variant')}` overall {best.get('overall', 0):.3f}"


def main() -> int:
    dashboard = ROOT / "results/phase4/dashboard.md"
    dashboard.parent.mkdir(parents=True, exist_ok=True)
    dashboard.write_text(
        "# Phase 4 Dashboard\n\n"
        "Status: real prompt-only probe anchors and prompt sweeps have completed on Andromeda. "
        "No prompt variant has passed no-harm gates yet, so micro-ablations are the next active stage.\n\n"
        "## Prompt-Only Probe Anchors\n\n"
        + score_line("Ukrainian prompt-only probe", "results/phase4/probe/baseline_prompt_only_uk.json")
        + "\n"
        + score_line("Sorbian prompt-only probe", "results/phase4/probe/baseline_prompt_only_sorbian.json")
        + "\n\n"
        "## Prompt Sweep\n\n"
        + sweep_summary("uk")
        + "\n"
        + sweep_summary("sorbian")
        + "\n\n"
        "No-harm gate reports: `results/phase4/gates/prompt_sweep_uk_no_harm_report.md` and "
        "`results/phase4/gates/prompt_sweep_sorbian_no_harm_report.md`.\n\n"
        "See `docs/45_phase4_preservation_pivot_plan.md` through `docs/54_phase4_merge_readiness.md`.\n",
        encoding="utf-8",
    )
    print(dashboard)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
