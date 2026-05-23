#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checkpoints = [str(p.relative_to(ROOT)) for p in (ROOT / "checkpoints").glob("**/*") if p.is_file()]
    bulky = [str(p.relative_to(ROOT)) for p in (ROOT / "results").glob("**/*") if p.is_file() and p.stat().st_size > 5_000_000]
    report = {
        "checkpoints_files": checkpoints,
        "bulky_result_files": bulky,
    }
    out = ROOT / "results/phase4/status/cleanup_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "checkpoint_files": len(checkpoints), "bulky_result_files": len(bulky)}, indent=2, sort_keys=True))
    return 0 if not checkpoints and not bulky else 1


if __name__ == "__main__":
    raise SystemExit(main())
