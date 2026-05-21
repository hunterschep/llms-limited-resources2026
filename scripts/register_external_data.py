#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/manifests/data_governance_registry.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--track", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--language", default="unknown")
    parser.add_argument("--language-pair", default="")
    parser.add_argument("--license", required=True)
    parser.add_argument("--local-path", required=True)
    parser.add_argument("--allowed-status", default="unknown", choices=["allowed", "risky", "forbidden", "unknown"])
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames or []
    rows.append(
        {
            "source_id": args.source_id,
            "source_name": args.source_name,
            "source_url": args.source_url,
            "track": args.track,
            "task": args.task,
            "language": args.language,
            "language_pair": args.language_pair,
            "license": args.license,
            "public_availability": "public",
            "download_method": "external_manual",
            "local_path": args.local_path,
            "split_type": "external_public",
            "allowed_status": args.allowed_status,
            "contamination_risk": "pending_review",
            "used_for_train": "false",
            "used_for_tune": "false",
            "used_for_locked_validation": "false",
            "used_for_final_training": "false",
            "notes": args.notes,
        }
    )
    with REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Registered {args.source_id}; run scripts/validate_data_governance.py before use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
