# Phase 3 Resume Or Block Merge Decision

Status: blocked pending fixed retraining.

Merge search is currently blocked because no fixed retrained checkpoints have completed normalized evaluation.

## Merge May Resume Only If

- Fixed `M_edit` no longer behaves like an always-error predictor.
- Fixed `M_edit` has acceptable no-error `CORRECT/CORRECT` behavior.
- Fixed `M_mr` no longer systematically collapses under normalized evaluation.
- Checkpoint-loading comparison confirms the intended checkpoints are evaluated.
- Prompt-only and fixed candidates are evaluated under the same normalized evaluator.
- Governance, overlap, and data-sanity gates pass.

## Explicitly Ineligible

- First-pass `M_edit`.
- First-pass `M_mr`.
- Any model trained on unbalanced SC/GC mixtures.
- Any stale checkpoint from canceled jobs.
- Any result generated only under the old strict MR parser.

This file must be updated with a yes/no decision after fixed evaluation.
