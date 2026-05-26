from __future__ import annotations

from typing import Any


def row_to_dapt_text(row: dict[str, Any]) -> str:
    """Return text for language-acquisition style causal LM training."""
    if row.get("task") == "LANG":
        return str(row.get("target") or row.get("input") or "").strip()
    if row.get("messages"):
        parts = []
        for message in row["messages"]:
            role = message.get("role", "user")
            content = str(message.get("content", "")).strip()
            if content:
                parts.append(f"{role}: {content}")
        return "\n".join(parts).strip()
    return f"{row.get('input', '')}\n{row.get('target', '')}".strip()


def is_language_acquisition_row(row: dict[str, Any]) -> bool:
    return str(row.get("task", "")).upper() in {"LANG", "MT", "QA", "SC", "GC", "MR", "FORMAT"}
