#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def score(row: dict, key: str) -> float:
    if key == "overall":
        return float((row.get("aggregate") or {}).get("overall_score", 0.0))
    return float((row.get("aggregate") or {}).get(key, 0.0))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidates", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    baseline = load(args.baseline)
    baseline_score = score(baseline, "overall")
    lines = ["# Competitive Comparison", "", f"Baseline: `{args.baseline}` overall={baseline_score:.3f}", ""]
    lines.append("| Candidate | Overall | Delta | MT | QA | SC | GC | MR |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for candidate_path in args.candidates:
        row = load(candidate_path)
        aggregate = row.get("aggregate") or {}
        overall = float(aggregate.get("overall_score", 0.0))
        lines.append(
            f"| `{candidate_path}` | {overall:.3f} | {overall - baseline_score:+.3f} | "
            f"{float(aggregate.get('MT_score', 0.0)):.3f} | {float(aggregate.get('QA_score', 0.0)):.3f} | "
            f"{float(aggregate.get('SC_score', 0.0)):.3f} | {float(aggregate.get('GC_score', 0.0)):.3f} | "
            f"{float(aggregate.get('MR_score', 0.0)):.3f} |"
        )
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
