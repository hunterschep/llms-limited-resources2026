#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
_raw_root = Path(os.environ.get("WMT26_RAW_ROOT", "data/external/raw")).expanduser()
RAW_ROOT = _raw_root if _raw_root.is_absolute() else ROOT / _raw_root

from wmt26.compilers.common import mt_example, write_jsonl
from scripts.filter_external_data import cyrillic_fraction, good_text, norm


def find_lang_file(root: Path, suffix: str) -> Path | None:
    matches = list(root.rglob(f"*.{suffix}"))
    return matches[0] if matches else None


def filter_opus_collection(source_id: str, src_lang: str, tgt_lang: str, cap: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = RAW_ROOT / source_id.replace(":", "__")
    rows: list[dict[str, Any]] = []
    raw = 0
    seen: set[tuple[str, str]] = set()
    if not root.exists():
        return [], {"source_id": source_id, "raw": 0, "filtered": 0, "notes": "raw collection missing"}
    for corpus_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        src_path = find_lang_file(corpus_dir, src_lang)
        tgt_path = find_lang_file(corpus_dir, tgt_lang)
        if not src_path or not tgt_path:
            continue
        with src_path.open("r", encoding="utf-8", errors="ignore") as src_handle, tgt_path.open(
            "r", encoding="utf-8", errors="ignore"
        ) as tgt_handle:
            for idx, (src, tgt) in enumerate(zip(src_handle, tgt_handle)):
                raw += 1
                src = norm(src)
                tgt = norm(tgt)
                if not good_text(src, 3, 800) or not good_text(tgt, 3, 800):
                    continue
                if cyrillic_fraction(tgt) < 0.35:
                    continue
                ratio = max(len(src), len(tgt)) / max(1, min(len(src), len(tgt)))
                if ratio > 3.0 or src.lower() == tgt.lower():
                    continue
                key = (src.lower(), tgt.lower())
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    mt_example(
                        idx=f"{source_id}:{corpus_dir.name}:{idx:08d}:{src_lang}->ukr",
                        track="ukrainian",
                        source_language=src_lang,
                        target_language="ukr",
                        source_text=src,
                        target_text=tgt,
                        split="train",
                        source_id=source_id,
                        source_type="external",
                        license_name="mixed OPUS corpus metadata",
                        generation_method="competitive_opus_collection_filtered",
                        metadata={"opus_corpus": corpus_dir.name, "raw_index": idx},
                    )
                )
                if len(rows) >= cap:
                    return rows, {"source_id": source_id, "raw": raw, "filtered": len(rows)}
    return rows, {"source_id": source_id, "raw": raw, "filtered": len(rows)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=["uk", "sorbian", "all"], default="all")
    args = parser.parse_args()
    subprocess.run([sys.executable, "scripts/filter_external_data.py"], cwd=ROOT, check=True)
    reports = []
    if args.track in {"uk", "all"}:
        rows, report = filter_opus_collection("external:opus_large_en_uk_scripted", "en", "uk", cap=350000)
        out = ROOT / "data/processed/external/uk/mt_competitive_large.jsonl"
        write_jsonl(out, rows)
        reports.append(report | {"output": str(out.relative_to(ROOT))})
    report_path = ROOT / "data/manifests/competitive_filter_report.jsonl"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        for report in reports:
            handle.write(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
