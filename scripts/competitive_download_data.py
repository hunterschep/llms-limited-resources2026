#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
_raw_root = Path(os.environ.get("WMT26_RAW_ROOT", "data/external/raw")).expanduser()
RAW_ROOT = _raw_root if _raw_root.is_absolute() else ROOT / _raw_root
INVENTORY = ROOT / "data/manifests/competitive_external_data_inventory.jsonl"


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def fetch(url: str, output: Path, timeout: int = 180) -> None:
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


def opus_latest_url(source: str, target: str, corpus: str) -> str:
    api = f"https://opus.nlpl.eu/opusapi/?source={source}&target={target}&corpus={corpus}&preprocessing=moses"
    with urllib.request.urlopen(api, timeout=90) as response:
        payload = json.loads(response.read().decode("utf-8"))
    corpora = payload.get("corpora") or []
    if not corpora:
        raise RuntimeError(f"No OPUS corpora for {corpus} {source}-{target}")
    latest = [row for row in corpora if str(row.get("latest")).lower() == "true"]
    chosen = latest[0] if latest else corpora[-1]
    return str(chosen["url"])


def download_opus_collection(source: dict[str, Any], execute: bool) -> list[dict[str, Any]]:
    spec = source.get("download", {})
    src = spec["source_language"]
    tgt = spec["target_language"]
    rows = []
    for corpus in source.get("corpora", []) or []:
        source_id = source["source_id"]
        target_dir = RAW_ROOT / source_id.replace(":", "__") / corpus
        if not execute:
            print(f"DRY-RUN OPUS {corpus} {src}-{tgt} -> {target_dir}")
            continue
        try:
            url = opus_latest_url(src, tgt, corpus)
            output = target_dir / Path(url).name
            fetch(url, output)
            if output.suffix == ".zip":
                extract_dir = output.with_suffix("")
                extract_dir.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(output) as zf:
                    zf.extractall(extract_dir)
            rows.append(
                {
                    "source_id": source_id,
                    "corpus": corpus,
                    "download_url": url,
                    "local_raw_path": manifest_path(target_dir),
                    "status": "downloaded",
                }
            )
        except Exception as exc:
            rows.append({"source_id": source_id, "corpus": corpus, "status": "failed", "error": str(exc)})
            print(f"WARNING: failed {source_id} {corpus}: {exc}", file=sys.stderr)
    return rows


def download_url_collection(source: dict[str, Any], execute: bool) -> list[dict[str, Any]]:
    spec = source.get("download", {})
    target_dir = RAW_ROOT / source["source_id"].replace(":", "__")
    if not execute:
        print(f"DRY-RUN URL {spec.get('url', '')} -> {target_dir}")
        return []
    url = spec["url"]
    output = target_dir / spec.get("filename", Path(url).name)
    fetch(url, output, timeout=300)
    return [
        {
            "source_id": source["source_id"],
            "download_url": url,
            "local_raw_path": manifest_path(output),
            "status": "downloaded",
        }
    ]


def download_github_contents(source: dict[str, Any], execute: bool) -> list[dict[str, Any]]:
    spec = source.get("download", {})
    api = spec["repo_api"]
    target_dir = RAW_ROOT / source["source_id"].replace(":", "__")
    if not execute:
        print(f"DRY-RUN GitHub contents {api} -> {target_dir}")
        return []
    with urllib.request.urlopen(api, timeout=120) as response:
        payload = json.loads(response.read().decode("utf-8"))
    rows = []
    for item in payload:
        name = str(item.get("name") or "")
        lower = name.lower()
        if item.get("type") != "file" or not name.endswith((".gz", ".tgz", ".tar.gz")):
            continue
        if any(marker in lower for marker in ["dev", "test", "valid"]):
            continue
        url = item.get("download_url")
        if not url:
            continue
        output = target_dir / name
        fetch(str(url), output, timeout=300)
        rows.append(
            {
                "source_id": source["source_id"],
                "download_url": url,
                "local_raw_path": manifest_path(output),
                "status": "downloaded",
                "github_size": item.get("size"),
            }
        )
    return rows


def write_inventory(rows: list[dict[str, Any]]) -> None:
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    with INVENTORY.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=["uk", "sorbian", "all"], default="all")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    config_paths = []
    if args.track in {"uk", "all"}:
        config_paths.append(ROOT / "configs/data/competitive_sources_uk.yaml")
    if args.track in {"sorbian", "all"}:
        config_paths.append(ROOT / "configs/data/competitive_sources_sorbian.yaml")

    base_configs = []
    if args.track in {"uk", "all"}:
        base_configs.append("configs/data/external_sources_uk.yaml")
    if args.track in {"sorbian", "all"}:
        base_configs.append("configs/data/external_sources_sorbian.yaml")
    if base_configs:
        cmd = [sys.executable, "scripts/download_external_data.py", *sum([["--config", p] for p in base_configs], []),
               *(["--execute"] if args.execute else [])]
        subprocess.run(cmd, cwd=ROOT, check=True)

    inventory_rows: list[dict[str, Any]] = []
    for path in config_paths:
        config = load_yaml(path)
        for source in config.get("sources", []) or []:
            if not source.get("enabled"):
                continue
            dtype = (source.get("download") or {}).get("type")
            if dtype == "opus_collection":
                inventory_rows.extend(download_opus_collection(source, args.execute))
            elif dtype == "git_or_url_collection" and (source.get("download") or {}).get("repo_api"):
                inventory_rows.extend(download_github_contents(source, args.execute))
            elif dtype == "scripted_only" and (source.get("download") or {}).get("url"):
                inventory_rows.extend(download_url_collection(source, args.execute))
            elif dtype in {"scripted_only", "git_or_url_collection", "opus_transfer_collection"}:
                if not args.execute:
                    print(f"DRY-RUN scripted source {source['source_id']} -> {source.get('local_path', '')}")
                    continue
                inventory_rows.append(
                    {
                        "source_id": source["source_id"],
                        "status": "registered_not_downloaded_by_local_script",
                        "local_raw_path": source.get("local_path", ""),
                        "notes": (source.get("download") or {}).get("notes", ""),
                    }
                )
    if inventory_rows:
        write_inventory(inventory_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
