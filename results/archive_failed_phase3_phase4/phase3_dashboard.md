# Phase 3 Dashboard

Status: remediation wave complete; merge and final polish are blocked.

Last updated: 2026-05-21.

## Current Snapshot

- Remote revision used for the fixed retrain wave: `787aab3d45b4162d592def8040d01aab52b416ea`.
- Andromeda environment validation, data preparation, governance checks, oracle scoring, data sanity, compact overfit, checkpoint-loading, fixed retraining, normalized evaluation, and compact raw-prediction dumps have all completed.
- Suspicious first-pass MR zeroes were substantially explained by strict answer normalization.
- Suspicious SC/GC detection plateaus were explained by unbalanced first-pass edit mixtures.
- The full fixed retrains still do not clear merge gates.
- No final model is selected.

## Fixed Wave Jobs

| Job | ID | Status | Notes |
|---|---:|---|---|
| phase3_remediation_cleanup | 2462239 | completed | Removed invalid first-pass active artifacts. |
| phase3_triage_oracle | 2462240 | completed | Oracle evaluator passed. |
| phase3_triage_data_sanity | 2462241 | completed | Data sanity passed. |
| phase3_triage_overfit_uk | 2462249 | completed | UK SC/GC/MR same-set overfit passed. |
| phase3_triage_overfit_sorbian | 2462250 | completed | Sorbian SC/GC/MR same-set overfit passed. |
| retrain_uk_edit_fixed | 2462264 | completed | Fixed edit specialist. |
| retrain_uk_mr_fixed | 2462265 | completed | Fixed MR specialist. |
| retrain_uk_task_balanced_fixed | 2462266 | completed | Fixed task-balanced baseline. |
| retrain_uk_external_enhanced_fixed | 2462267 | completed | Fixed external-enhanced baseline. |
| retrain_sorbian_edit_fixed | 2462268 | completed | Fixed edit specialist. |
| retrain_sorbian_mr_fixed | 2462269 | completed | Fixed MR specialist. |
| retrain_sorbian_task_balanced_fixed | 2462270 | completed | Fixed task-balanced baseline. |
| retrain_sorbian_external_enhanced_fixed | 2462271 | completed | Fixed external-enhanced baseline. |
| phase3_check_checkpoint_loading | 2462274 | completed | Confirmed trained outputs differ from base. |
| eval_phase3_fixed_uk | 2462292 | completed | All fixed Ukrainian candidates evaluated. |
| eval_phase3_fixed_sorbian | 2462293 | completed | All fixed Sorbian candidates evaluated. |
| phase3_triage_raw_predictions_uk | 2462365 | completed | Compact raw prediction diagnostics. |
| phase3_triage_raw_predictions_sorbian | 2462366 | completed | Compact raw prediction diagnostics. |
| wmt26_p3fix_cleanup | 2462400 | completed | Pruned blocked fixed checkpoints from scratch. |

Canceled eval jobs `2462272` and `2462273` were replaced by `2462292` and `2462293` after increasing eval batch size.

## Fixed Evaluation Summary

| Track | Model | MT chrF++ | QA acc | SC score | GC score | MR acc | Overall | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Ukrainian | prompt-only normalized | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 | 37.399 | reference |
| Ukrainian | fixed `M_edit` | 39.487 | 29.178 | 39.585 | 14.593 | 20.833 | 28.736 | blocked |
| Ukrainian | fixed `M_mr` | 40.997 | 38.810 | 33.998 | 32.997 | 20.833 | 33.527 | blocked |
| Ukrainian | fixed task-balanced | 40.000 | 37.960 | 30.494 | 2.821 | 8.333 | 23.922 | blocked |
| Ukrainian | fixed external-enhanced | 39.892 | 37.677 | 17.360 | 2.000 | 20.833 | 23.552 | blocked |
| Sorbian | prompt-only normalized | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | 29.195 | reference |
| Sorbian | fixed `M_edit` | 21.644 | 42.138 | 24.647 | 16.657 | 8.333 | 22.684 | blocked |
| Sorbian | fixed `M_mr` | 23.522 | 47.799 | 32.990 | 33.289 | 8.333 | 29.187 | blocked |
| Sorbian | fixed task-balanced | 28.248 | 47.170 | 28.225 | 13.697 | 10.417 | 25.551 | blocked |
| Sorbian | fixed external-enhanced | 29.706 | 42.138 | 34.199 | 33.561 | 10.417 | 30.004 | diagnostic fallback only |

## Sanity Gates

- `make triage-oracle`: passed.
- `make triage-data-sanity`: passed.
- Gold-target oracle checks give 100 for QA, MR, SC, and GC on both tracks.
- MT oracle sanity is high: Ukrainian chrF++ 99.793, Sorbian chrF++ 100.000.
- Same-set Ukrainian overfit: SC 100.0/89.7, GC 91.4/93.3, MR 100.0.
- Same-set Sorbian overfit: SC 86.7/89.7, GC 90.3/93.3, MR 100.0.
- Checkpoint-loading comparison passed for fixed edit/MR candidates.

## Cleanup

- Remote fixed checkpoint cleanup job: `2462400`.
- Remote checkpoint cleanup manifest: `results/cleanup/phase3_fixed_checkpoint_cleanup_20260521T100927Z.txt`.
- Phase 3 fixed checkpoint size before cleanup: 29G.
- Phase 3 fixed checkpoint size after cleanup: 0.
- Total remote checkpoint root before cleanup: 50G.
- Total remote checkpoint root after cleanup: 22G.
- Compact eval JSON, raw prediction diagnostics, cleanup manifests, and triage reports were preserved.

## Decision

Merge search is blocked. Final polish is skipped. The next useful step is a narrower data/model remediation for edit correction and MR preservation, not model merging.
