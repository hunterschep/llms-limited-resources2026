#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        "data/processed/uk/qa_train.jsonl",
        "data/processed/uk/sc_train.jsonl",
        "data/processed/sorbian/mt_train.jsonl",
        "data/processed/sorbian/sc_train.jsonl",
    ]
    for rel in required:
        path = ROOT / rel
        if not path.exists() or path.stat().st_size == 0:
            raise SystemExit(f"Missing or empty processed data: {rel}")
        first = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
        assert first["contamination_checked"] is True
        assert first["messages"]
    print("Data smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
