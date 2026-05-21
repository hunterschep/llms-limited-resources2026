from __future__ import annotations

from pathlib import Path
from typing import Any


def load_torch_state(path: str | Path) -> dict[str, Any]:
    import torch

    path = Path(path)
    if path.is_dir():
        candidates = list(path.glob("*.bin")) + list(path.glob("*.pt"))
        if not candidates:
            raise FileNotFoundError(f"No .bin/.pt state dict found under {path}")
        path = candidates[0]
    return torch.load(path, map_location="cpu")


def save_torch_state(state: dict[str, Any], path: str | Path) -> None:
    import torch

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(state, path)
