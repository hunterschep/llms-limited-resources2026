#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
_raw_root = Path(os.environ.get("WMT26_RAW_ROOT", "data/external/raw")).expanduser()
RAW_ROOT = _raw_root if _raw_root.is_absolute() else ROOT / _raw_root
INVENTORY = ROOT / "data/manifests/external_data_inventory.jsonl"


def read_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def fetch_url(url: str, output: Path, timeout: int = 120) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.stat().st_size > 0:
        return
    print(f"Downloading {url} -> {output}", flush=True)
    tmp = output.with_suffix(output.suffix + ".part")
    if tmp.exists():
        tmp.unlink()
    with urllib.request.urlopen(url, timeout=timeout) as response:
        with tmp.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    tmp.replace(output)


def manifest_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def opus_latest_url(source: str, target: str, corpus: str) -> tuple[str, dict[str, Any]]:
    api = f"https://opus.nlpl.eu/opusapi/?source={source}&target={target}&corpus={corpus}&preprocessing=moses"
    with urllib.request.urlopen(api, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    corpora = payload.get("corpora") or []
    if not corpora:
        raise RuntimeError(f"OPUS API returned no corpora for {corpus} {source}-{target}")
    latest = [row for row in corpora if str(row.get("latest")).lower() == "true"]
    chosen = latest[0] if latest else corpora[-1]
    return chosen["url"], chosen


def download_opus(source: dict[str, Any]) -> dict[str, Any]:
    spec = source["download"]
    source_lang = spec["source_language"]
    target_lang = spec["target_language"]
    corpus = spec["opus_corpus"]
    url, meta = opus_latest_url(source_lang, target_lang, corpus)
    output = RAW_ROOT / source["source_id"].replace(":", "__") / Path(url).name
    fetch_url(url, output)
    if output.suffix == ".zip":
        extract_dir = output.with_suffix("")
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output) as zf:
            zf.extractall(extract_dir)
    return {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "download_url": url,
        "local_raw_path": manifest_path(output),
        "task": source["task"],
        "track": source["track"],
        "language": source.get("language", ""),
        "language_pair": source.get("language_pair", ""),
        "license": source["license"],
        "row_count_raw": meta.get("alignment_pairs"),
        "allowed_status": source["allowed_status"],
        "notes": f"OPUS metadata: {meta}",
    }


def download_url_source(source: dict[str, Any]) -> dict[str, Any]:
    spec = source["download"]
    url = spec["url"]
    output = RAW_ROOT / source["source_id"].replace(":", "__") / spec.get("filename", Path(url).name)
    fetch_url(url, output)
    return {
        "source_id": source["source_id"],
        "source_name": source["source_name"],
        "download_url": url,
        "local_raw_path": manifest_path(output),
        "task": source["task"],
        "track": source["track"],
        "language": source.get("language", ""),
        "language_pair": source.get("language_pair", ""),
        "license": source["license"],
        "row_count_raw": None,
        "allowed_status": source["allowed_status"],
        "notes": "Direct public URL download.",
    }


def write_inventory(rows: list[dict[str, Any]]) -> None:
    existing: dict[str, dict[str, Any]] = {}
    if INVENTORY.exists():
        for line in INVENTORY.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["source_id"]] = row
    for row in rows:
        existing[row["source_id"]] = row
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    with INVENTORY.open("w", encoding="utf-8") as handle:
        for row in sorted(existing.values(), key=lambda r: r["source_id"]):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[])
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--source-id", default=None)
    args = parser.parse_args()
    config_paths = [ROOT / p for p in (args.config or [])] or [
        ROOT / "configs/data/external_sources_uk.yaml",
        ROOT / "configs/data/external_sources_sorbian.yaml",
    ]
    sources: list[dict[str, Any]] = []
    for path in config_paths:
        config = read_config(path)
        sources.extend(config.get("sources", []))
    enabled = [s for s in sources if s.get("enabled")]
    if args.source_id:
        enabled = [s for s in enabled if s["source_id"] == args.source_id]
    if not enabled:
        print("No enabled external sources selected.")
        return 0
    downloaded = []
    for source in enabled:
        download = source.get("download", {})
        if not args.execute:
            print(f"DRY-RUN {source['source_id']} ({download.get('type', 'scripted')})")
            continue
        if source["allowed_status"] not in {"allowed", "risky"}:
            print(f"Skipping non-allowed source {source['source_id']}", file=sys.stderr)
            continue
        if download.get("type") == "opus":
            downloaded.append(download_opus(source))
        elif download.get("type") == "url":
            downloaded.append(download_url_source(source))
        elif download.get("type") == "scripted_only":
            downloaded.append(
                {
                    "source_id": source["source_id"],
                    "source_name": source["source_name"],
                    "download_url": source["source_url"],
                    "local_raw_path": source.get("local_path", ""),
                    "task": source["task"],
                    "track": source["track"],
                    "language": source.get("language", ""),
                    "language_pair": source.get("language_pair", ""),
                    "license": source["license"],
                    "row_count_raw": 0,
                    "allowed_status": source["allowed_status"],
                    "notes": "Scripted source retained for Andromeda-scale acquisition; not downloaded locally.",
                }
            )
        else:
            raise ValueError(f"Unknown download type for {source['source_id']}: {download}")
    if downloaded:
        write_inventory(downloaded)
        print(f"Updated {INVENTORY} with {len(downloaded)} sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
