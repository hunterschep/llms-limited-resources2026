#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase4_common import markdown_table, write_json


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-md", default="docs/47_phase4_failure_mode_analysis.md")
    parser.add_argument("--output-json", default="results/phase4/status/failure_mode_analysis.json")
    args = parser.parse_args()
    uk_base = load_json("results/phase3_fixed/uk/base_qwen35_2b.json")
    uk_edit = load_json("results/phase3_fixed/uk/edit.json")
    uk_mr = load_json("results/phase3_fixed/uk/mr.json")
    sb_base = load_json("results/phase3_fixed/sorbian/base_qwen35_2b.json")
    sb_ext = load_json("results/phase3_fixed/sorbian/external_enhanced.json")
    hypotheses = [
        ["H1 overtraining/aggressive LoRA", "supported", "Fixed full retrains underperform despite compact overfit; old settings used LR 5e-5 to 2e-4 and hundreds of steps on narrow data.", "low LR, low rank, assistant-only loss, early probe stopping"],
        ["H2 synthetic edit mismatch", "strongly supported", "Balanced edit data still fails locked SC/GC exact correction and shifts priors.", "official-style hard negatives and one-token real corrections before more volume"],
        ["H3 prompt mismatch", "partially supported", "Raw outputs show malformed/MR verbosity for some candidates and CORRECT/CORRECT overuse.", "prompt sweep and per-task decoding caps"],
        ["H4 catastrophic forgetting", "strongly supported", "MR and GC collapse in multitask runs; prompt-only is strong after normalization.", "KL-to-base, replay, adapter scaling"],
        ["H5 bad mixture", "supported", "Task-balanced/external-enhanced hurt exact edit and MR even when QA/MT move.", "strong caps and preservation-first ablations"],
        ["H6 eval mismatch/noise", "partially supported", "MR is tiny and exact SC/GC is brittle, but failures are large enough to be real.", "probe plus gated full eval only"],
    ]
    report = {
        "uk_prompt_only_overall": uk_base["aggregate"]["overall_score"],
        "uk_edit_delta": uk_edit["aggregate"]["overall_score"] - uk_base["aggregate"]["overall_score"],
        "uk_mr_delta": uk_mr["aggregate"]["overall_score"] - uk_base["aggregate"]["overall_score"],
        "sorbian_prompt_only_overall": sb_base["aggregate"]["overall_score"],
        "sorbian_external_delta": sb_ext["aggregate"]["overall_score"] - sb_base["aggregate"]["overall_score"],
        "hypotheses": hypotheses,
    }
    write_json(ROOT / args.output_json, report)
    md = [
        "# Phase 4 Failure Mode Analysis",
        "",
        "Phase 3 remediation made the evaluator and data gates sane, but the fixed full retrains still failed preservation gates.",
        "",
        markdown_table(["hypothesis", "status", "evidence", "remediation"], hypotheses),
        "",
        "Key conclusion: the next training step must minimize drift from Qwen3.5-2B, use assistant-only target masking, and gate all candidates against prompt-only before full validation.",
        "",
        "Sources preserved: https://www2.statmt.org/wmt26/limited-resources-llm.html and https://github.com/TUM-NLP/llms-limited-resources2026.",
    ]
    output = ROOT / args.output_md
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"output_md": args.output_md, "output_json": args.output_json}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
