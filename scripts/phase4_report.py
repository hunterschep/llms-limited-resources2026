#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    dashboard = ROOT / "results/phase4/dashboard.md"
    dashboard.parent.mkdir(parents=True, exist_ok=True)
    dashboard.write_text(
        "# Phase 4 Dashboard\n\n"
        "Status: preservation-first probe and ablation tooling is installed. "
        "Prompt-only remains the fallback until a candidate passes no-harm gates.\n\n"
        "See `docs/45_phase4_preservation_pivot_plan.md` through `docs/54_phase4_merge_readiness.md`.\n",
        encoding="utf-8",
    )
    print(dashboard)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
