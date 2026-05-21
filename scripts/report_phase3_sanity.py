#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(rel: str) -> object | None:
    path = ROOT / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def status_line(label: str, ok: bool, detail: str) -> str:
    return f"- {label}: `{'PASS' if ok else 'PENDING/FAIL'}` {detail}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a compact Phase 3 remediation sanity summary.")
    parser.add_argument("--output", default="results/triage/phase3_sanity_summary.md")
    parser.add_argument("--docs-output", default="docs/37_phase3_sanity_gates.md")
    parser.add_argument("--fail-on-pending", action="store_true")
    args = parser.parse_args()

    oracle = load_json("results/triage/oracle_eval_report.json")
    data = load_json("results/triage/data_sanity_report.json")
    edit = load_json("results/triage/edit_data_balance.json")
    mr = load_json("results/triage/mr_data_quality.json")

    oracle_ok = bool(oracle and oracle.get("passed"))
    data_ok = bool(data and all(task.get("status") == "pass" for track in data.values() for task in track.values()))
    edit_ok = bool(edit and all(task.get("status") == "pass" for track in edit.values() for task in track.values()))
    mr_ok = bool(
        mr
        and all(probe.get("pass") for probe in mr.get("normalization_probes", []))
        and all(row.get("status") == "pass" for track in mr.get("tracks", {}).values() for row in track.values())
    )

    lines = [
        "# Phase 3 Sanity Gates",
        "",
        "Status reflects local/parser/data gates. GPU overfit/checkpoint-loading gates are recorded from Andromeda runs when available.",
        "",
        status_line("Oracle evaluator", oracle_ok, "Gold targets must score perfectly on QA/MR/SC/GC."),
        status_line("Data sanity", data_ok, "Final SC/GC balance and MR target parseability must pass."),
        status_line("Edit balance", edit_ok, "Clean/error SC/GC mixtures must be close to balanced."),
        status_line("MR data quality", mr_ok, "MR normalization probes and train targets must pass."),
        "",
        "Required remote gates before merge search:",
        "",
        "- Compact SC/GC/MR overfit for both tracks.",
        "- Checkpoint-loading comparison for retrained candidates.",
        "- Raw prediction dumps for retrained candidates before final evaluation.",
        "",
    ]
    if data:
        lines.append("## Current Data Sanity")
        lines.append("")
        for track, tasks in data.items():
            for task, row in tasks.items():
                if task in {"SC", "GC"}:
                    lines.append(f"- `{track} {task}`: rows={row['rows']} error={row['error_rows']} clean={row['clean_rows']} clean_ratio={row['clean_ratio']:.3f}")
                elif task == "MR":
                    lines.append(f"- `{track} MR`: rows={row['rows']} non_numeric_targets={row['non_numeric_targets']}")
        lines.append("")

    text = "\n".join(lines)
    out = ROOT / args.output
    docs_out = ROOT / args.docs_output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    docs_out.write_text(text, encoding="utf-8")
    print(json.dumps({"output": str(out), "docs_output": str(docs_out), "passed": oracle_ok and data_ok and edit_ok and mr_ok}, indent=2, sort_keys=True))
    return 1 if args.fail_on_pending and not (oracle_ok and data_ok and edit_ok and mr_ok) else 0


if __name__ == "__main__":
    raise SystemExit(main())
