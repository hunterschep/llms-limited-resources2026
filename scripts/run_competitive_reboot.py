#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> int:
    print("+ " + " ".join(args), flush=True)
    return subprocess.run(args, cwd=ROOT, check=False).returncode


def dashboard() -> int:
    out = ROOT / "results/competitive_reboot/dashboard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    sections = ["# Competitive Reboot Dashboard", ""]
    data_report = ROOT / "results/competitive_reboot/data/competitive_data_report.md"
    if data_report.exists():
        sections.append(data_report.read_text(encoding="utf-8"))
    else:
        sections.append("Data report has not been generated yet.")
    eval_dir = ROOT / "results/competitive_reboot/eval"
    sections.extend(["", "## Evaluation Files", ""])
    for path in sorted(eval_dir.rglob("*.json")) if eval_dir.exists() else []:
        sections.append(f"- `{path.relative_to(ROOT)}`")
    out.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "cleanup",
            "download-data",
            "filter-data",
            "build-mixtures",
            "validate-data",
            "train-sorbian",
            "train-uk",
            "eval-sorbian",
            "eval-uk",
            "compare",
            "dashboard",
            "clean-failed",
            "package",
        ],
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args, extra = parser.parse_known_args()
    if args.command == "cleanup":
        return run([sys.executable, "scripts/competitive_cleanup_failed.py", *extra])
    if args.command == "download-data":
        return run([sys.executable, "scripts/competitive_download_data.py", *(["--execute"] if args.execute else []), *extra])
    if args.command == "filter-data":
        return run([sys.executable, "scripts/competitive_filter_data.py", *extra])
    if args.command == "build-mixtures":
        return run([sys.executable, "scripts/competitive_build_mixtures.py", *extra])
    if args.command == "validate-data":
        code = run([sys.executable, "scripts/validate_data_governance.py"])
        if code:
            return code
        code = run([sys.executable, "scripts/check_dev_overlap.py"])
        if code:
            return code
        return run([sys.executable, "scripts/competitive_report_data.py"])
    if args.command == "train-sorbian":
        return run([sys.executable, "scripts/train_stagewise.py", "--config", "configs/train/competitive/sorbian_stagewise_tartu_style.yaml", *(["--dry-run"] if args.dry_run else []), *extra])
    if args.command == "train-uk":
        return run([sys.executable, "scripts/train_stagewise.py", "--config", "configs/train/competitive/uk_stagewise_realdata.yaml", *(["--dry-run"] if args.dry_run else []), *extra])
    if args.command == "eval-sorbian":
        return run([sys.executable, "scripts/competitive_eval.py", "--config", "configs/eval/sorbian.yaml", "--output", "results/competitive_reboot/eval/sorbian/prompt_or_candidate.json", *extra])
    if args.command == "eval-uk":
        return run([sys.executable, "scripts/competitive_eval.py", "--config", "configs/eval/uk.yaml", "--output", "results/competitive_reboot/eval/uk/prompt_or_candidate.json", *extra])
    if args.command == "compare":
        return dashboard()
    if args.command == "dashboard":
        return dashboard()
    if args.command == "clean-failed":
        return run([sys.executable, "scripts/competitive_cleanup_failed.py", *extra])
    if args.command == "package":
        return run([sys.executable, "scripts/competitive_package_model.py", *extra])
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
