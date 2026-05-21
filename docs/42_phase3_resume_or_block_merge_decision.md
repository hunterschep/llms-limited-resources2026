# Phase 3 Resume Or Block Merge Decision

Status: blocked pending completion of Sorbian fixed evaluation. Ukrainian fixed evaluation is complete and disqualifies all fixed Ukrainian retrains.

Merge search is currently blocked because the fixed specialists that were supposed to repair the suspicious failure modes have not cleared the sanity gates.

## Decision From Ukrainian Fixed Eval

The normalized prompt-only Ukrainian baseline now scores 29.17 MR, confirming that the old near-zero MR picture was substantially parser-related. This makes the fixed specialist gates stricter:

- Fixed Ukrainian `M_edit` is blocked. It scores worse than prompt-only overall and collapses GC correction to 0.0. Checkpoint-loading diagnostics show it often emits `CORRECT/CORRECT`, so the remediation fixed the old always-error prior but overshot toward false negatives.
- Fixed Ukrainian `M_mr` is blocked. It does not recover prompt-only MR under the normalized evaluator: 20.83 vs 29.17 MR accuracy, while also damaging SC/GC correction.
- Fixed Ukrainian task-balanced is blocked. It drops to 23.92 overall and damages GC/MR.
- Fixed Ukrainian external-enhanced is blocked. It drops to 23.55 overall and damages SC/GC.

Sorbian fixed evaluation is still running. No merge search should run until those results finish and the candidate eligibility list is explicit.

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
