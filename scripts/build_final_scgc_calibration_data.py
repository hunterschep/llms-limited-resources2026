#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.eval.metrics import parse_edit_output  # noqa: E402


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def is_clean(row: dict[str, Any]) -> bool:
    wrong, _ = parse_edit_output(str(row.get("target", "")))
    return wrong == "CORRECT"


def stamp(row: dict[str, Any], method: str) -> dict[str, Any]:
    new = dict(row)
    new["split"] = "train"
    new["track"] = "sorbian"
    new["contamination_checked"] = True
    new["generation_method"] = method
    md = dict(new.get("metadata") or {})
    md["final_salvage"] = True
    new["metadata"] = md
    return new


def take(rows: list[dict[str, Any]], n: int, rng: random.Random) -> list[dict[str, Any]]:
    if not rows or n <= 0:
        return []
    if n <= len(rows):
        return list(rows[:n])
    out = list(rows)
    while len(out) < n:
        out.append(dict(rng.choice(rows)))
    return out[:n]


def summary(rows: list[dict[str, Any]], path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "rows": len(rows),
        "by_task": dict(Counter(str(row.get("task", "unknown")) for row in rows)),
        "clean_rows": sum(1 for row in rows if row.get("task") in {"SC", "GC"} and is_clean(row)),
        "error_rows": sum(1 for row in rows if row.get("task") in {"SC", "GC"} and not is_clean(row)),
        "by_source_id_top20": dict(Counter(str(row.get("source_id", "unknown")) for row in rows).most_common(20)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data/final_scgc_calibration_sorbian.yaml")
    args = parser.parse_args()
    cfg = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8")) or {}
    rng = random.Random(int(cfg.get("seed", 2711)))
    out_root = ROOT / cfg["outputs"]["root"]
    out_root.mkdir(parents=True, exist_ok=True)

    edit_rows = [stamp(row, "final_salvage_scgc_calibration") for row in read_jsonl(ROOT / cfg["sources"]["lineage_edit_calibration"])]
    clean = [row for row in edit_rows if is_clean(row)]
    error = [row for row in edit_rows if not is_clean(row)]
    rng.shuffle(clean)
    rng.shuffle(error)
    outputs = {}
    total = int(cfg["limits"]["edit_examples_per_ratio"])
    for name, ratio in cfg["ratios"].items():
        clean_n = int(round(total * float(ratio["clean"])))
        error_n = total - clean_n
        rows = take(clean, clean_n, rng) + take(error, error_n, rng)
        rng.shuffle(rows)
        path = out_root / f"{name}.jsonl"
        write_jsonl(path, rows)
        outputs[name] = summary(rows, path)

    anchors: list[dict[str, Any]] = []
    for key, limit, method in [
        ("lineage_format_repair", int(cfg["limits"]["format_examples"]), "final_salvage_format_anchor"),
        ("mt_anchor", int(cfg["limits"]["mt_anchor_examples"]), "final_salvage_mt_anchor"),
        ("qa_anchor", int(cfg["limits"]["qa_anchor_examples"]), "final_salvage_qa_anchor"),
        ("mr_anchor", int(cfg["limits"]["mr_anchor_examples"]), "final_salvage_mr_anchor"),
    ]:
        rows = [stamp(row, method) for row in read_jsonl(ROOT / cfg["sources"][key])]
        rng.shuffle(rows)
        anchors.extend(rows[:limit])
    rng.shuffle(anchors)
    anchor_path = out_root / "anchor_replay.jsonl"
    write_jsonl(anchor_path, anchors)
    outputs["anchor_replay"] = summary(anchors, anchor_path)

    manifest = {"config": args.config, "policy": cfg.get("policy", {}), "outputs": outputs}
    (ROOT / "data/manifests/final_scgc_calibration_sorbian.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    status_dir = ROOT / "results/final_salvage/status"
    status_dir.mkdir(parents=True, exist_ok=True)
    (status_dir / "final_scgc_calibration_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
