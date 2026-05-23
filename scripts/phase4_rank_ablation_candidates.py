#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase4_common import markdown_table, task_score_vector, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", default="results/phase4/**/*.json")
    parser.add_argument("--output", default="results/phase4/micro_ablations/ranked_candidates.json")
    args = parser.parse_args()
    rows = []
    for path in glob.glob(str(ROOT / args.pattern), recursive=True):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:
            continue
        if "aggregate" not in data:
            continue
        score = task_score_vector(data)
        rows.append({"path": str(Path(path).relative_to(ROOT)), "model": data.get("model") or data.get("variant_id"), **score})
    rows.sort(key=lambda row: row["overall"], reverse=True)
    output = ROOT / args.output
    write_json(output, {"candidates": rows})
    md = output.with_suffix(".md")
    md.write_text("# Phase 4 Ranked Candidates\n\n" + markdown_table(["path", "model", "overall", "MT", "QA", "SC", "GC", "MR"], [[r["path"], r["model"], f"{r['overall']:.3f}", f"{r['MT']:.3f}", f"{r['QA']:.3f}", f"{r['SC']:.3f}", f"{r['GC']:.3f}", f"{r['MR']:.3f}"] for r in rows]) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output, "count": len(rows)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
