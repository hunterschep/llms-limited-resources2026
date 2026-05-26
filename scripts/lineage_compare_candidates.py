#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "scripts"))

from lineage_common import aggregate_row, markdown_table, write_json  # noqa: E402


def main() -> int:
    result_paths = sorted((ROOT / "results/lineage_recovery").glob("**/*.json"))
    rows = []
    for path in result_paths:
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if "aggregate" not in result:
            continue
        rows.append(aggregate_row(path.stem, path))
    rows.sort(key=lambda row: float(row.get("overall") or -1), reverse=True)
    write_json(ROOT / "results/lineage_recovery/dashboard.json", {"candidates": rows})
    dashboard = ROOT / "results/lineage_recovery/dashboard.md"
    dashboard.parent.mkdir(parents=True, exist_ok=True)
    dashboard.write_text(
        "\n".join(
            [
                "# Lineage Recovery Dashboard",
                "",
                markdown_table(rows, ["model", "overall", "MT", "QA", "SC", "GC", "MR", "path"]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(dashboard)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
