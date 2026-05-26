# Phase 3 Submission Readiness

Status: not ready. Specialist training is complete, but evaluation, merge search, polish, and final model selection are still pending.

## Current Artifact State

- Ukrainian specialist checkpoints exist under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/`.
- Sorbian specialist checkpoints exist under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/`.
- Baseline checkpoint training is in progress under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/{uk,sorbian}/baselines/`.
- Prompt-only base evaluations and specialist evaluations are running on Andromeda.
- Merge, polish, and final evaluation jobs are queued behind specialist evaluation jobs.

## Required Before Submission

- Final selected Ukrainian checkpoint.
- Final selected Sorbian checkpoint.
- Completed all-five-task evaluation for baselines, specialists, merged candidates, and polished candidates.
- Tokenizer/config/generation config path for each selected model.
- Prompt templates used for each task.
- Model card drafts finalized.
- Governance and data summaries attached.
- Training and evaluation summaries attached.
- Official evaluator reconciliation checked or documented unavailable.
- Packaging commands prepared.

No upload or submission should be executed without explicit instruction.
