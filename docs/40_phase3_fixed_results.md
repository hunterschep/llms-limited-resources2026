# Phase 3 Fixed Results

Status: fixed retraining queued on Andromeda after sanity gates passed.

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

## Fixed Jobs Queued

| Job | ID | Status |
|---|---:|---|
| retrain_uk_edit_fixed | 2462264 | queued |
| retrain_uk_mr_fixed | 2462265 | queued |
| retrain_uk_task_balanced_fixed | 2462266 | queued |
| retrain_uk_external_enhanced_fixed | 2462267 | queued |
| retrain_sorbian_edit_fixed | 2462268 | queued |
| retrain_sorbian_mr_fixed | 2462269 | queued |
| retrain_sorbian_task_balanced_fixed | 2462270 | queued |
| retrain_sorbian_external_enhanced_fixed | 2462271 | queued |
| eval_phase3_fixed_uk | 2462272 | dependency |
| eval_phase3_fixed_sorbian | 2462273 | dependency |
| phase3_check_checkpoint_loading | 2462274 | dependency |

Note: eval jobs `2462272` and `2462273` were canceled during MT generation because `batch_size: 4` was too slow for full locked validation. Evaluation configs were updated to `batch_size: 16` for L40S and resubmitted against the same completed checkpoints as `2462292` and `2462293`.

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

This file must be updated from actual fixed evaluations before merge search.
