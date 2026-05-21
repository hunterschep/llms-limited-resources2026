# Phase 3 Fixed Results

Status: fixed retraining, normalized evaluation, compact raw-prediction dumps, and checkpoint cleanup are complete.

## Sanity Gates

| Gate | Job/command | Result |
|---|---:|---|
| Remote cleanup of invalid first-pass artifacts | `2462239` | passed |
| Oracle evaluator | `2462240` / `make triage-oracle` | passed |
| Data sanity | `2462241` / `make triage-data-sanity` | passed |
| Ukrainian compact overfit | `2462249` | passed |
| Sorbian compact overfit | `2462250` | passed |
| Checkpoint loading | `2462274` | passed |

Compact overfit showed the training/checkpoint path can learn same-set examples:

| Track | Task | Same-set result |
|---|---|---:|
| Ukrainian | SC | detection F1 100.0, correction F1 89.7 |
| Ukrainian | GC | detection F1 91.4, correction F1 93.3 |
| Ukrainian | MR | accuracy 100.0 |
| Sorbian | SC | detection F1 86.7, correction F1 89.7 |
| Sorbian | GC | detection F1 90.3, correction F1 93.3 |
| Sorbian | MR | accuracy 100.0 |

## Fixed Training And Eval Jobs

| Job | ID | Status | Notes |
|---|---:|---|---|
| retrain_uk_edit_fixed | 2462264 | completed | Balanced SC/GC edit specialist. |
| retrain_uk_mr_fixed | 2462265 | completed | MR final-answer preservation specialist. |
| retrain_uk_task_balanced_fixed | 2462266 | completed | Task-balanced with fixed edit/MR mixtures. |
| retrain_uk_external_enhanced_fixed | 2462267 | completed | External-enhanced with fixed edit/MR mixtures. |
| retrain_sorbian_edit_fixed | 2462268 | completed | Balanced SC/GC edit specialist. |
| retrain_sorbian_mr_fixed | 2462269 | completed | MR final-answer preservation specialist. |
| retrain_sorbian_task_balanced_fixed | 2462270 | completed | Task-balanced with fixed edit/MR mixtures. |
| retrain_sorbian_external_enhanced_fixed | 2462271 | completed | External-enhanced with fixed edit/MR mixtures. |
| eval_phase3_fixed_uk | 2462292 | completed | All fixed Ukrainian candidates evaluated. |
| eval_phase3_fixed_sorbian | 2462293 | completed | All fixed Sorbian candidates evaluated. |
| phase3_triage_raw_predictions_uk | 2462365 | completed | Compact raw predictions and diagnostics. |
| phase3_triage_raw_predictions_sorbian | 2462366 | completed | Compact raw predictions and diagnostics. |

The first submitted eval jobs, `2462272` and `2462273`, were canceled because `batch_size: 4` was too slow during MT generation. They were replaced by `2462292` and `2462293` after the fixed eval configs were updated to `batch_size: 16`.

## Ukrainian Fixed Results

The normalized MR parser changes the baseline interpretation: prompt-only MR is 29.17 under normalized parsing, not the old 4.17 strict-parser score. None of the fixed Ukrainian retrains clear the merge gates.

| Ukrainian model | MT chrF++ | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall | Gate status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only, normalized evaluator | 40.990 | 34.278 | 66.667 | 27.168 | 65.993 | 5.298 | 29.167 | 37.399 | reference |
| fixed `M_edit` | 39.487 | 29.178 | 61.488 | 17.683 | 29.187 | 0.000 | 20.833 | 28.736 | blocked |
| fixed `M_mr` | 40.997 | 38.810 | 66.667 | 1.329 | 65.993 | 0.000 | 20.833 | 33.527 | blocked |
| fixed task-balanced | 40.000 | 37.960 | 42.752 | 18.237 | 5.643 | 0.000 | 8.333 | 23.922 | blocked |
| fixed external-enhanced | 39.892 | 37.677 | 24.561 | 10.159 | 4.000 | 0.000 | 20.833 | 23.552 | blocked |

## Sorbian Fixed Results

Sorbian external-enhanced is the only fixed retrain that beats normalized prompt-only overall, but it is a multitask fallback result rather than a clean specialist vector for skill-vector merging. The fixed edit and MR specialists remain blocked.

| Sorbian model | MT chrF++ | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall | Gate status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only, normalized evaluator | 27.477 | 43.396 | 65.630 | 1.739 | 66.168 | 0.000 | 8.333 | 29.195 | reference |
| fixed `M_edit` | 21.644 | 42.138 | 45.507 | 3.787 | 32.497 | 0.818 | 8.333 | 22.684 | blocked |
| fixed `M_mr` | 23.522 | 47.799 | 65.630 | 0.350 | 66.168 | 0.410 | 8.333 | 29.187 | blocked |
| fixed task-balanced | 28.248 | 47.170 | 53.002 | 3.448 | 27.393 | 0.000 | 10.417 | 25.551 | blocked |
| fixed external-enhanced | 29.706 | 42.138 | 65.630 | 2.768 | 66.304 | 0.818 | 10.417 | 30.004 | diagnostic fallback only |

## Result Paths

- `results/phase3_fixed/uk/`
- `results/phase3_fixed/sorbian/`
- `results/phase3_fixed/comparisons/`
- `results/phase3_fixed/raw_predictions/`

## Conclusion

The suspicious first-pass MR zeroes were substantially explained by overly strict parsing, and the SC/GC plateau was explained by bad edit-data class balance. The remediation proved the training path can overfit compact slices, but the fixed full retrains still do not generalize well enough to merge. Merge search remains blocked.
