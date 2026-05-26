#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_b_rescue_common import markdown_table, read_json, write_json  # noqa: E402


def _score_row(name: str, path: Path) -> dict:
    result = read_json(path)
    agg = result.get("aggregate") or {}
    return {
        "model": name,
        "overall": float(agg.get("overall_score", 0.0)),
        "MT": float(agg.get("MT_score", 0.0)),
        "QA": float(agg.get("QA_score", 0.0)),
        "SC": float(agg.get("SC_score", 0.0)),
        "GC": float(agg.get("GC_score", 0.0)),
        "MR": float(agg.get("MR_score", 0.0)),
    }


def write_report(rows: list[dict]) -> None:
    doc = ROOT / "docs/89_stage_b_rescue_full_eval_results.md"
    lines = [
        "# Stage B Rescue Full Eval Results",
        "",
        "Full locked-validation evaluation is reserved for Stage B plus candidates that pass the rescue probe.",
        "",
    ]
    lines.extend(markdown_table(rows, ["model", "overall", "MT", "QA", "SC", "GC", "MR"]))
    lines.extend(
        [
            "",
            "Selection rule: a final candidate must beat Stage B overall, keep MT at or above 41.0, avoid SC/GC collapse, and improve MR if possible.",
        ]
    )
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", action="append", nargs=2, metavar=("NAME", "MODEL_PATH"))
    parser.add_argument("--config", default="configs/eval/sorbian.yaml")
    parser.add_argument("--output-dir", default="results/stage_b_rescue/full_eval")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = args.candidate or []
    if args.run:
        for name, model in candidates:
            subprocess.run(
                [
                    sys.executable,
                    "scripts/competitive_eval.py",
                    "--config",
                    args.config,
                    "--model",
                    model,
                    "--output",
                    str((out_dir / f"{name}.json").relative_to(ROOT)),
                    "--raw-output",
                    str((out_dir / f"{name}_raw.jsonl").relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=True,
            )
    rows = []
    for name, _ in candidates:
        path = out_dir / f"{name}.json"
        if path.exists():
            rows.append(_score_row(name, path))
    write_json(out_dir / "full_eval_summary.json", {"rows": rows})
    write_report(rows)
    print(json.dumps(rows, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
