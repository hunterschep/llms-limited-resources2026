#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/merge/stage_b_rescue/sorbian_repair_merge.yaml")
    parser.add_argument("--output", default="results/stage_b_rescue/merge/merge_plan.json")
    args = parser.parse_args()
    config_path = ROOT / args.config
    status = {
        "config": args.config,
        "status": "blocked_until_individual_repairs_pass_probe",
        "reason": "Task-vector repair merge is only valid after separate MR and edit repair adapters show positive probe signal. Failed Stage C is explicitly excluded.",
        "config_exists": config_path.exists(),
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
