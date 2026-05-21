#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/manifests/data_governance_registry.csv"
SCHEMA = ROOT / "data/manifests/data_governance_registry.schema.json"

REQUIRED_FIELDS = [
    "source_id",
    "source_name",
    "source_url",
    "track",
    "task",
    "language",
    "language_pair",
    "license",
    "public_availability",
    "download_method",
    "local_path",
    "split_type",
    "allowed_status",
    "contamination_risk",
    "used_for_train",
    "used_for_tune",
    "used_for_locked_validation",
    "used_for_final_training",
    "notes",
]

TRUTHY = {"true", "1", "yes", "y"}
POLYMATH_RE = re.compile(r"(?<!non[- ])(?:poly\s*math|polymath)", re.IGNORECASE)
SORBIAN_CERT_RE = re.compile(r"sorbian.*certificate|certificate.*sorbian|language certificate", re.IGNORECASE)
WMT2025_TEST_RE = re.compile(r"wmt\s*2025.*test|wmt2025.*test", re.IGNORECASE)
TEST_SPLIT_RE = re.compile(r"(mmlu|unlp|zno).*test|test.*(mmlu|unlp|zno)|hidden test", re.IGNORECASE)
UNKNOWN_LICENSE = {"", "unknown", "tbd", "none"}


def truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in TRUTHY


def row_text(row: dict[str, str]) -> str:
    return " ".join(str(v) for v in row.values())


def validate_row(row: dict[str, str], index: int) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in row:
            errors.append(f"row {index}: missing field {field}")
        elif field not in {"language_pair", "notes"} and row[field] == "":
            errors.append(f"row {index}: {field} is empty")
    status = row.get("allowed_status", "")
    if status not in {"allowed", "risky", "forbidden", "unknown"}:
        errors.append(f"row {index}: invalid allowed_status {status!r}")
    source_id = row.get("source_id", "")
    is_external = source_id.startswith("external:") or row.get("download_method", "").startswith("external")
    if is_external:
        license_value = row.get("license", "").strip().lower()
        if license_value in UNKNOWN_LICENSE and "LICENSE_RISK:" not in row.get("notes", ""):
            errors.append(f"row {index}: external data with unknown license requires LICENSE_RISK note")
        if not row.get("source_url"):
            errors.append(f"row {index}: external data must have source_url")
    used_train = truthy(row.get("used_for_train"))
    used_final = truthy(row.get("used_for_final_training"))
    if status == "forbidden" and (used_train or used_final):
        errors.append(f"row {index}: forbidden data marked for training/final training")
    if status == "risky" and used_train and "JUSTIFICATION:" not in row.get("notes", ""):
        errors.append(f"row {index}: risky data used for train without JUSTIFICATION note")
    if row.get("split_type") == "official_dev" and used_train and "OFFICIAL_DEV_TRAIN_OVERRIDE:" not in row.get("notes", ""):
        errors.append(f"row {index}: official dev data used for train without override note")
    text = row_text(row)
    if POLYMATH_RE.search(text) and (used_train or used_final or truthy(row.get("used_for_tune"))):
        errors.append(f"row {index}: PolyMath or PolyMath-derived data marked for training/tune/final use")
    if SORBIAN_CERT_RE.search(text) and source_id.startswith("external:") and (used_train or used_final):
        errors.append(f"row {index}: external Sorbian certificate material marked for training")
    if WMT2025_TEST_RE.search(text) and (used_train or used_final or truthy(row.get("used_for_tune"))):
        errors.append(f"row {index}: WMT2025 test material marked for use")
    if TEST_SPLIT_RE.search(text) and (used_train or used_final or truthy(row.get("used_for_tune"))):
        errors.append(f"row {index}: known test/hidden-test pattern marked for use")
    return errors


def main() -> int:
    if not SCHEMA.exists():
        print(f"Missing schema: {SCHEMA}", file=sys.stderr)
        return 2
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    expected = schema.get("required", REQUIRED_FIELDS)
    if expected != REQUIRED_FIELDS:
        print("Schema required fields differ from validator policy", file=sys.stderr)
        return 2
    if not REGISTRY.exists():
        print(f"Missing registry: {REGISTRY}", file=sys.stderr)
        return 2
    with REGISTRY.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    errors: list[str] = []
    if not rows:
        errors.append("registry is empty")
    for idx, row in enumerate(rows, start=2):
        errors.extend(validate_row(row, idx))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Data governance validation passed for {len(rows)} registered sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
