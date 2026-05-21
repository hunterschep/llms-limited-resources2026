from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - validate_setup checks PyYAML.
    yaml = None


LANGUAGE_NAMES = {
    "uk": "Ukrainian",
    "ukr": "Ukrainian",
    "hsb": "Upper Sorbian",
    "dsb": "Lower Sorbian",
    "de": "German",
    "en": "English",
    "cs": "Czech",
    "pl": "Polish",
}


def load_prompt_config(path: str | Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load prompt configs.")
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if "system" not in data or "user" not in data:
        raise ValueError(f"{path} must contain system and user templates")
    return data


def render_template(template: str, **kwargs: Any) -> str:
    defaults = {k: LANGUAGE_NAMES.get(str(v), str(v)) for k, v in kwargs.items()}
    defaults.update(kwargs)
    return template.format(**defaults)


def render_messages(config_path: str | Path, target: str | None = None, **kwargs: Any) -> list[dict[str, str]]:
    config = load_prompt_config(config_path)
    messages = [
        {"role": "system", "content": render_template(config["system"], **kwargs)},
        {"role": "user", "content": render_template(config["user"], **kwargs)},
    ]
    if target is not None:
        messages.append({"role": "assistant", "content": target})
    return messages


def two_line_edit_target(wrong_word: str, correct_word: str) -> str:
    return f"Wrong word: {wrong_word}\nCorrect word: {correct_word}"
