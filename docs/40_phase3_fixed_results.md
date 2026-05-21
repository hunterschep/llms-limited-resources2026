# Phase 3 Fixed Results

Status: fixed retraining completed; normalized locked-validation evaluation is in progress on Andromeda.

## Sanity Gates Completed

- Cleanup: `2462239`, completed.
- Oracle evaluator: `2462240`, completed and passed.
- Data sanity: `2462241`, completed and passed.
- Ukrainian compact overfit: `2462249`, completed and passed.
- Sorbian compact overfit: `2462250`, completed and passed.

Compact overfit results:

| Track | Task | Same-set result |
|---|---|---:|
| Ukrainian | SC | detection F1 100.0, correction F1 89.7 |
| Ukrainian | GC | detection F1 91.4, correction F1 93.3 |
| Ukrainian | MR | accuracy 100.0 |
| Sorbian | SC | detection F1 86.7, correction F1 89.7 |
| Sorbian | GC | detection F1 90.3, correction F1 93.3 |
| Sorbian | MR | accuracy 100.0 |

## Fixed Training Jobs

| Job | ID | Status |
|---|---:|---|
| retrain_uk_edit_fixed | 2462264 | completed |
| retrain_uk_mr_fixed | 2462265 | completed |
| retrain_uk_task_balanced_fixed | 2462266 | completed |
| retrain_uk_external_enhanced_fixed | 2462267 | completed |
| retrain_sorbian_edit_fixed | 2462268 | completed |
| retrain_sorbian_mr_fixed | 2462269 | completed |
| retrain_sorbian_task_balanced_fixed | 2462270 | completed |
| retrain_sorbian_external_enhanced_fixed | 2462271 | completed |
| phase3_check_checkpoint_loading | 2462274 | completed |

Note: eval jobs `2462272` and `2462273` were canceled during MT generation because `batch_size: 4` was too slow for full locked validation. Evaluation configs were updated to `batch_size: 16` for L40S and resubmitted against the same completed checkpoints as `2462292` and `2462293`.

## Normalized Evaluation Status

| Job | ID | Status | Notes |
|---|---:|---|---|
| eval_phase3_fixed_uk | 2462292 | completed | All fixed Ukrainian candidates evaluated. |
| eval_phase3_fixed_sorbian | 2462293 | running | Prompt-only base completed; fixed Sorbian candidates are still evaluating. |
| phase3_triage_raw_predictions_uk | 2462365 | dependency: `2462293` | Queued to dump compact raw predictions after fixed eval finishes. |
| phase3_triage_raw_predictions_sorbian | 2462366 | dependency: `2462293` | Queued to dump compact raw predictions after fixed eval finishes. |

Ukrainian fixed results show that the corrected MR parser materially changes the baseline interpretation: prompt-only MR is 29.17 under normalized parsing, not the earlier near-zero/4.17 result. However, none of the fixed Ukrainian retrains clear the merge gates.

| Ukrainian model | MT chrF++ | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall | Gate status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only, normalized evaluator | 40.990 | 34.278 | 66.667 | 27.168 | 65.993 | 5.298 | 29.167 | 37.399 | reference |
| fixed `M_edit` | 39.487 | 29.178 | 61.488 | 17.683 | 29.187 | 0.000 | 20.833 | 28.736 | blocked |
| fixed `M_mr` | 40.997 | 38.810 | 66.667 | 1.329 | 65.993 | 0.000 | 20.833 | 33.527 | blocked |
| fixed task-balanced | 40.000 | 37.960 | 42.752 | 18.237 | 5.643 | 0.000 | 8.333 | 23.922 | blocked |
| fixed external-enhanced | 39.892 | 37.677 | 24.561 | 10.159 | 4.000 | 0.000 | 20.833 | 23.552 | blocked |

Interpretation:

- The old MR collapse was substantially an evaluator-normalization artifact, but MR specialist training is still not healthy because fixed `M_mr` remains below prompt-only MR.
- Balanced edit data removed the old always-error prior, but fixed `M_edit` overshot toward `CORRECT/CORRECT` and under-detects real GC errors. It is not a usable edit specialist vector.
- Fixed Ukrainian task-balanced and external-enhanced runs are worse than prompt-only and are not useful fallback models.

Partial Sorbian normalized baseline result:

| Sorbian model | MT chrF++ | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall | Gate status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only, normalized evaluator | 27.477 | 43.396 | 65.630 | 1.739 | 66.168 | 0.000 | 8.333 | 29.195 | reference |

Sorbian MR also increases under normalized parsing, from the old 0.0 to 8.33. Fixed Sorbian candidate evaluations are still running.

Expected result paths:

- `results/phase3_fixed/uk/`
- `results/phase3_fixed/sorbian/`
- `results/phase3_fixed/comparisons/`
- `results/phase3_fixed/raw_predictions/`
- `results/phase3_fixed/error_analysis/`

Report columns:

- MT chrF++
- MT BLEU
- QA accuracy
- SC detection F1
- SC correction F1
- GC detection F1
- GC correction F1
- MR accuracy
- SC/GC no-error accuracy
- SC/GC malformed output rate
- MR malformed output rate
- overall equal-weighted score

This file must be updated again after `2462292` and `2462293` finish.
