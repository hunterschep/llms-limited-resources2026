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
