# Stage B Packaging Policy

Do not package Stage B as final until repair succeeds or is explicitly abandoned.

Package only if:

- Candidate overall beats Stage B, or Stage B is deliberately kept as a diagnostic MT anchor.
- MT remains at or above `41.0`.
- MR improves over Stage B or the tradeoff is explicitly justified.
- SC/GC do not collapse.
- One model can run MT, QA, SC, GC, and MR.
- The model is Qwen3.5-family <=2B.
- No per-task adapter switching, live retrieval, hidden ensemble, or forbidden data is used.

The package must include tokenizer/config/generation config, data statement, contamination statement, eval table, exact generation settings, and a load test.

Do not upload publicly without explicit approval.

## Current Package Status

`edit_repair_tiny` passed dry-run packaging and `config.json` validation on Andromeda:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/sorbian/edit_repair_tiny`

This package is not an approved final submission yet. It is retained as `promising_needs_more_repair` because it beats Stage B overall and recovers some MR, but it does not beat prompt-only by `+5` overall and MR remains below prompt-only.
