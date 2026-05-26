# Phase 4 Micro-Ablation Grid

The Phase 4 grid is intentionally small. It is meant to discover whether any low-impact adaptation can beat prompt-only without damaging the other WMT tasks.

Initial configs:

- `configs/train/phase4/uk/edit_preserve_low_lr.yaml`
- `configs/train/phase4/uk/mr_preserve_kl.yaml`
- `configs/train/phase4/uk/format_preserve_tiny.yaml`
- `configs/train/phase4/sorbian/edit_preserve_low_lr.yaml`
- `configs/train/phase4/sorbian/mr_preserve_kl.yaml`
- `configs/train/phase4/sorbian/format_preserve_tiny.yaml`

Grid dimensions represented:

- low LR: `5e-6` and `1e-5`
- low LoRA rank: `r=4`
- attention-only targets
- assistant-only loss masking
- replay buffers
- KL-to-base on MR preservation candidates
- short step counts only

Use `scripts/phase4_run_micro_ablations.py` for dry-runs and controlled launches. Full locked validation is forbidden until a candidate passes probe gates.

Executed Andromeda jobs:

- Ukrainian micro-ablation job `2503775`
- Sorbian micro-ablation job `2503776`

Probe-gated outcomes:

- Ukrainian `mr_preserve_kl` at scales 0.05, 0.10, and 0.35 passed the probe no-harm gate. The best probe score was `mr_preserve_kl@0.10` at 38.526 versus the prompt-only probe anchor 37.969.
- Sorbian `edit_preserve_low_lr@0.35` was the best nonzero-scale probe candidate, scoring 30.997 versus the prompt-only probe anchor 29.644.

Full locked-validation outcomes:

- Ukrainian `mr_preserve_kl@0.10` did not produce a meaningful win and is diagnostic only.
- Sorbian `edit_preserve_low_lr@0.35` passed full no-harm validation and is the only Phase 4 checkpoint currently preserved as an eligible candidate.
