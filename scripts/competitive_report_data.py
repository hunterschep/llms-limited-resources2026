#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MINIMUMS = {
    "uk": {
        "stagewise_all.jsonl": {"rows": 250000, "task_minimums": {"MT": 200000}},
        "stage_a_mt_real_large.jsonl": {"rows": 100000, "task_minimums": {"MT": 90000}},
    },
    "sorbian": {
        "stagewise_all.jsonl": {"rows": 320000, "task_minimums": {"MT": 250000, "LANG": 50000}},
        "stage_a_dapt_large.jsonl": {"rows": 30000, "task_minimums": {"LANG": 25000}},
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def count(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "UNKNOWN")
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def report_track(track: str) -> dict[str, Any]:
    root = ROOT / "data/processed/competitive" / track
    files = sorted(root.glob("*.jsonl"))
    report = {"track": track, "files": []}
    for path in files:
        rows = read_jsonl(path)
        report["files"].append(
            {
                "path": str(path.relative_to(ROOT)),
                "rows": len(rows),
                "by_task": count(rows, "task"),
                "by_source_id": count(rows, "source_id"),
            }
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results/competitive_reboot/data")
    parser.add_argument("--enforce-competitive-minimums", action="store_true")
    args = parser.parse_args()
    reports = [report_track("uk"), report_track("sorbian")]
    out_dir = ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "competitive_data_report.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = ["# Competitive Data Report", ""]
    for report in reports:
        lines.extend([f"## {report['track']}", ""])
        for item in report["files"]:
            lines.append(f"- `{item['path']}`: {item['rows']} rows; tasks={item['by_task']}")
        lines.append("")
    (out_dir / "competitive_data_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_dir / 'competitive_data_report.md'}")
    if args.enforce_competitive_minimums:
        failures = []
        by_track = {report["track"]: {Path(item["path"]).name: item for item in report["files"]} for report in reports}
        for track, file_checks in MINIMUMS.items():
            for name, check in file_checks.items():
                item = by_track.get(track, {}).get(name)
                if not item:
                    failures.append(f"{track}/{name}: missing")
                    continue
                if item["rows"] < check["rows"]:
                    failures.append(f"{track}/{name}: {item['rows']} rows < {check['rows']}")
                for task, minimum in check["task_minimums"].items():
                    actual = int(item["by_task"].get(task, 0))
                    if actual < minimum:
                        failures.append(f"{track}/{name}: {task} {actual} < {minimum}")
        if failures:
            for failure in failures:
                print(f"COMPETITIVE_DATA_MINIMUM_FAILED {failure}")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
