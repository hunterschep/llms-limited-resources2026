# Phase 4 Cleanup Summary

Timestamp: 2026-05-26T01:01:05Z

Purpose: prune failed Phase 4 micro-ablation checkpoints after gated full locked validation.

Decision:

- Preserve Sorbian `edit_preserve_low_lr` adapter because `adapter@scale=0.35` passed full no-harm validation.
- Delete Ukrainian Phase 4 adapters because the best candidate only tied prompt-only and failed the real task-gain gate.
- Delete Sorbian failed `format_preserve_tiny` and `mr_preserve_kl` adapters.
- Delete the large merged model under the preserved Sorbian candidate because evaluation and future adapter-scale use require only the LoRA adapter plus base Qwen3.5-2B.
- Delete old triage overfit checkpoints after preserving compact triage result summaries.
- Delete local dry-run checkpoints created by `make smoke-test`.
- Delete empty checkpoint directories left after remote pruning.

Before cleanup:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase4`: 22G
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints`: 22G
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/triage/overfit`: 22G
- `/home/scheppat/workspace/projects/wmt26_lrllm/results/phase4`: 464K

After cleanup:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints`: 20M
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase4`: 20M
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/triage`: empty directory only
- `/home/scheppat/workspace/projects/wmt26_lrllm/results/phase4`: 464K

The user-level scratch quota still reported 277.64GB immediately after deletion, so WekaFS accounting had not caught up yet. Directory-level `du` confirms the WMT26 checkpoint tree was reduced to 20M.
