#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True, help="JSON from phase4_check_no_harm_gates.py")
    parser.add_argument("--track", choices=["uk", "sorbian"], required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT / args.candidates).read_text(encoding="utf-8"))
    passed = [row for row in data.get("checks", []) if row.get("passed")]
    out_dir = ROOT / "results/phase4/gated_eval"
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.dry_run or not passed:
        (out_dir / f"{args.track}_gated_eval_plan.json").write_text(json.dumps({"passed": passed, "dry_run": args.dry_run}, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "planned", "passed": len(passed)}, indent=2))
        return 0
    config = "configs/eval/uk.yaml" if args.track == "uk" else "configs/eval/sorbian.yaml"
    for row in passed:
        model = row["candidate"]
        output = f"results/phase4/gated_eval/{args.track}_{Path(model).name}.json"
        subprocess.run([sys.executable, "scripts/eval_model.py", "--config", config, "--model", model, "--output", output], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
