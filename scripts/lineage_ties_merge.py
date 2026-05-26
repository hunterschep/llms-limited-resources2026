#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    out = ROOT / "results/lineage_recovery/merge/ties_merge_plan.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "status": "deferred",
                "reason": "Run TIES only after lineage task-vector merge produces at least two probe-positive deltas. The current implementation keeps this as an explicit decision point rather than a blind merge.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
