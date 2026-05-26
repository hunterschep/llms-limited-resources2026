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


def score_row(label: str, rel: str) -> list[str]:
    data = read_json(rel)
    agg = data.get("aggregate", {})
    if not agg:
        return [label, rel, "missing", "", "", "", "", "", ""]
    return [
        label,
        rel,
        f"{agg.get('overall_score', 0):.3f}",
        f"{agg.get('MT_score', 0):.3f}",
        f"{agg.get('QA_score', 0):.3f}",
        f"{agg.get('SC_score', 0):.3f}",
        f"{agg.get('GC_score', 0):.3f}",
        f"{agg.get('MR_score', 0):.3f}",
        str(data.get("adapter_scale") if data.get("adapter") else ""),
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


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
    gated_rows = [
        score_row("UK prompt-only full anchor", "results/phase4/gated_eval/uk_prompt_only_anchor.json"),
        score_row("UK mr_preserve_kl@0.1", "results/phase4/gated_eval/uk_mr_preserve_kl_scale_0p1.json"),
        score_row("Sorbian prompt-only full anchor", "results/phase4/gated_eval/sorbian_prompt_only_anchor.json"),
        score_row("Sorbian edit_preserve_low_lr@0.35", "results/phase4/gated_eval/sorbian_edit_preserve_low_lr_scale_0p35.json"),
    ]
    dashboard.write_text(
        "# Phase 4 Dashboard\n\n"
        "Status: Phase 4 prompt sweep, micro-ablations, and gated full locked validation have completed. "
        "Ukrainian has no meaningful trained improvement, so prompt-only remains the safe Ukrainian fallback. "
        "Sorbian `edit_preserve_low_lr` at adapter scale 0.35 is a modest safe improvement and is the only "
        "Phase 4 checkpoint currently eligible for preservation.\n\n"
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
        "No prompt-sweep variant passed no-harm gates.\n\n"
        "## Gated Full Locked Validation\n\n"
        + markdown_table(["candidate", "path", "overall", "MT", "QA", "SC", "GC", "MR", "scale"], gated_rows)
        + "\n\n"
        "Full no-harm gate reports: `results/phase4/gates/full_uk_no_harm_report.md` and "
        "`results/phase4/gates/full_sorbian_no_harm_report.md`.\n\n"
        "Merge search remains blocked because only one Phase 4 candidate passed full locked validation. "
        "See `docs/53_phase4_gated_eval_results.md` and `docs/54_phase4_merge_readiness.md`.\n",
        encoding="utf-8",
    )
    print(dashboard)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
