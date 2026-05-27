#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from lineage_common import aggregate_row, markdown_table, write_json  # noqa: E402
from wmt26.eval.metrics import scgc_diagnostics  # noqa: E402


DEFAULT_CANDIDATES = {
    "selected_lineage_merge": "/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10",
}


def no_error_from_raw(raw_path: Path) -> dict[str, float]:
    if not raw_path.exists():
        return {}
    rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    out = {}
    for task in ("SC", "GC"):
        preds = [row["prediction"] for row in rows if row.get("task") == task]
        refs = [row["reference"] for row in rows if row.get("task") == task]
        diag = scgc_diagnostics(preds, refs)
        out[f"{task}_no_error"] = diag["detection_tn"] / max(1, diag["gold_correct"])
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/eval/sorbian.yaml")
    parser.add_argument("--candidate", nargs=2, action="append", metavar=("NAME", "MODEL"))
    parser.add_argument("--output-dir", default="results/final_salvage/eval")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates = dict(DEFAULT_CANDIDATES)
    for item in args.candidate or []:
        candidates[item[0]] = item[1]
    rows = []
    for name, model in candidates.items():
        output = output_dir / f"{name}.json"
        raw = output_dir / f"{name}_raw.jsonl"
        if args.run:
            if not Path(model).exists() and not model.startswith("Qwen/"):
                rows.append({"model": name, "exists": False, "decision": "missing", "path": model})
                continue
            subprocess.run(
                [sys.executable, "scripts/competitive_eval.py", "--config", args.config, "--model", model, "--output", str(output.relative_to(ROOT)), "--raw-output", str(raw.relative_to(ROOT))],
                cwd=ROOT,
                check=True,
            )
        row = aggregate_row(name, output)
        row.update(no_error_from_raw(raw))
        rows.append(row)
    rows.sort(key=lambda row: float(row.get("overall") or -1), reverse=True)
    write_json(output_dir / "final_salvage_eval_summary.json", {"candidates": rows})
    doc = ROOT / "docs/110_final_salvage_eval_results.md"
    doc.write_text(
        "\n".join(
            [
                "# Final Salvage Eval Results",
                "",
                markdown_table(rows, ["model", "overall", "MT", "QA", "SC", "GC", "MR", "SC_no_error", "GC_no_error", "decision"]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(rows, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
