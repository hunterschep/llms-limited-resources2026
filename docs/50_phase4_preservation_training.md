# Phase 4 Preservation Training

Phase 4 training differs from earlier SFT in three important ways:

1. Assistant-only loss masking: prompt/system/user tokens are masked out of the training loss.
2. Replay buffers: MR/format/QA examples can be mixed into narrow specialists to reduce drift.
3. Optional KL-to-base regularization: candidate logits can be penalized for diverging from frozen Qwen3.5-2B on the training batch.

Implemented files:

- `src/wmt26/train/preservation.py`
- `scripts/train_preservation_lora.py`
- `configs/train/phase4/`

Default Phase 4 configs use low-rank LoRA (`r=4`), low learning rates (`5e-6` to `1e-5`), attention-only target modules, short step counts, and clean `checkpoints/phase4/...` output paths.

No Phase 4 checkpoint is merge-eligible until it passes probe no-harm gates and then full locked validation.

Full locked-validation result:

- `checkpoints/phase4/uk/mr_preserve_kl/adapter@scale=0.10` is diagnostic only. It is safe but does not beat prompt-only by a meaningful margin.
- `checkpoints/phase4/sorbian/edit_preserve_low_lr/adapter@scale=0.35` is preserved as the only Phase 4 safe improved candidate.
