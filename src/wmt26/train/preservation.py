from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch
import torch.nn.functional as F


@dataclass
class PreservationBatch:
    input_ids: torch.Tensor
    attention_mask: torch.Tensor
    labels: torch.Tensor


def assistant_only_labels(tokenizer: Any, messages: list[dict[str, str]], max_length: int) -> dict[str, torch.Tensor]:
    """Tokenize a chat row while masking prompt tokens out of the SFT loss."""
    prompt_messages = [message for message in messages if message.get("role") != "assistant"]
    try:
        prompt_text = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
        full_text = tokenizer.apply_chat_template(messages, tokenize=False)
    except Exception:
        prompt_text = "\n".join(f"{m.get('role')}: {m.get('content')}" for m in prompt_messages) + "\nassistant: "
        full_text = "\n".join(f"{m.get('role')}: {m.get('content')}" for m in messages)
    prompt_ids = tokenizer(prompt_text, truncation=True, max_length=max_length)["input_ids"]
    encoded = tokenizer(full_text, truncation=True, max_length=max_length)
    input_ids = torch.tensor(encoded["input_ids"], dtype=torch.long)
    labels = input_ids.clone()
    prompt_len = min(len(prompt_ids), labels.numel())
    labels[:prompt_len] = -100
    return {
        "input_ids": input_ids,
        "attention_mask": torch.tensor(encoded["attention_mask"], dtype=torch.long),
        "labels": labels,
    }


def kl_to_base_loss(student_logits: torch.Tensor, base_logits: torch.Tensor, attention_mask: torch.Tensor, temperature: float = 1.0) -> torch.Tensor:
    """Token-level KL(student || base) on non-padding tokens."""
    temp = max(float(temperature), 1e-6)
    student_logp = F.log_softmax(student_logits / temp, dim=-1)
    base_p = F.softmax(base_logits / temp, dim=-1)
    token_kl = F.kl_div(student_logp, base_p, reduction="none").sum(dim=-1)
    mask = attention_mask.to(token_kl.dtype)
    return (token_kl * mask).sum() / mask.sum().clamp_min(1.0)


def scale_lora_adapters(model: Any, scale: float) -> None:
    """Best-effort LoRA adapter scaling for PEFT models."""
    if hasattr(model, "set_adapter"):
        try:
            for module in model.modules():
                if hasattr(module, "scaling") and isinstance(module.scaling, dict):
                    for key in list(module.scaling):
                        module.scaling[key] *= float(scale)
        except Exception:
            return
