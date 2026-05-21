# Phase 3 Dashboard

Status: paused for triage/remediation. The Phase 3 goal is not complete yet.

## Current Snapshot

Last updated: 2026-05-21.

- Remote revision for the remediation retrain wave: `787aab3d45b4162d592def8040d01aab52b416ea`.
- Environment, governance validation, data preparation, and GPU smoke validation have passed on Andromeda.
- Completed specialist checkpoints from the first Phase 3 pass were deleted from Andromeda scratch after triage because they were trained/evaluated against known-bad edit mixtures and overly strict MR scoring.
- Active jobs: fixed Ukrainian evaluation `2462292` completed; fixed Sorbian evaluation `2462293` is still running on L40S.
- Latest retained results: prompt-only normalized fixed baselines, completed Ukrainian fixed retrain evaluations, Sorbian normalized prompt-only baseline, triage evidence, and local remediation sanity outputs.
- Current decision: Ukrainian merge remains blocked because all fixed Ukrainian retrains underperform the normalized prompt-only baseline. Sorbian merge decision remains pending fixed candidate results.
- Baseline suites were resubmitted as 2461539 and 2461541 because the earlier queued jobs carried an L40S-blocking exclusion list.
- Fixed retraining was submitted to `short` after the `medium` queue had no start estimate. H200 was draining and A100/L40S were not idle; compact sanity used V100 as allowed, while fixed retraining uses L40S fallback.

## Current Fixed Retrain Wave

| Job | ID | GPU Request | Status | Notes |
|---|---:|---|---|---|
| phase3_remediation_cleanup | 2462239 | CPU | completed | Wrote cleanup manifest `results/cleanup/phase3_cleanup_manifest_20260521T063217Z.txt`. |
| phase3_triage_oracle | 2462240 | CPU | completed | Oracle evaluator passed. |
| phase3_triage_data_sanity | 2462241 | CPU | completed | Data sanity passed. |
| phase3_triage_overfit_uk | 2462249 | V100 | completed | UK SC/GC/MR same-set overfit passed. |
| phase3_triage_overfit_sorbian | 2462250 | V100 | completed | Sorbian SC/GC/MR same-set overfit passed. |
| retrain_uk_edit_fixed | 2462264 | L40S | completed | Fixed balanced SC/GC edit specialist. |
| retrain_uk_mr_fixed | 2462265 | L40S | completed | Fixed MR final-answer preservation specialist. |
| retrain_uk_task_balanced_fixed | 2462266 | L40S | completed | Task-balanced baseline with fixed edit/MR mixtures. |
| retrain_uk_external_enhanced_fixed | 2462267 | L40S | completed | External-enhanced baseline with fixed edit/MR mixtures. |
| retrain_sorbian_edit_fixed | 2462268 | L40S | completed | Fixed balanced SC/GC edit specialist. |
| retrain_sorbian_mr_fixed | 2462269 | L40S | completed | Fixed MR final-answer preservation specialist. |
| retrain_sorbian_task_balanced_fixed | 2462270 | L40S | completed | Task-balanced baseline with fixed edit/MR mixtures. |
| retrain_sorbian_external_enhanced_fixed | 2462271 | L40S | completed | External-enhanced baseline with fixed edit/MR mixtures. |
| eval_phase3_fixed_uk | 2462272 | L40S | canceled | Canceled during MT generation because eval `batch_size: 4` was too slow. |
| eval_phase3_fixed_sorbian | 2462273 | L40S | canceled | Canceled during MT generation because eval `batch_size: 4` was too slow. |
| phase3_check_checkpoint_loading | 2462274 | L40S | completed | Confirmed fixed edit/MR outputs differ from base. |
| eval_phase3_fixed_uk | 2462292 | L40S | completed | All fixed Ukrainian retrains are blocked; prompt-only normalized baseline is best so far. |
| eval_phase3_fixed_sorbian | 2462293 | L40S | running | Sorbian prompt-only normalized baseline completed; fixed candidates still evaluating. |
| phase3_triage_raw_predictions_uk | 2462365 | L40S | dependency: 2462293 | Queued after Sorbian fixed eval to avoid competing for GPU. Dumps base plus fixed Ukrainian checkpoints. |
| phase3_triage_raw_predictions_sorbian | 2462366 | L40S | dependency: 2462293 | Queued after Sorbian fixed eval to avoid competing for GPU. Dumps base plus fixed Sorbian checkpoints. |

## Remote Jobs

| Job | ID | Status | Notes |
|---|---:|---|---|
| 00_create_env | 2461442 | completed | Created/updated `wmt26-lrllm` on Andromeda. |
| 00_validate_env | 2461449 | completed | Environment and governance validation passed. |
| 01_prepare_data | 2461453 | completed | Data preparation and smoke tests passed on Andromeda. |
| 00_create_env repair | 2461496 | completed | Reinstalled `torch==2.8.0+cu128`; env reports `torch_cuda=12.8`. |
| 00_validate_gpu_env | 2461500 | completed | CUDA smoke test passed on V100; this validated the repaired torch build against Andromeda's driver. |
| train_uk_all |  | planned | Train Ukrainian specialists, merge, and polish if stable. |
| train_sorbian_all |  | planned | Train Sorbian specialists, merge, and polish if stable. |

## Canceled Phase 3 Jobs Pending Environment Repair

| Job | ID | GPU Request | Status |
|---|---:|---|---|
| eval_base_uk | 2461465 | L40S, 4 CPU, 64G | canceled: torch CUDA-driver mismatch |
| eval_base_sorbian | 2461466 | L40S, 4 CPU, 64G | canceled: torch CUDA-driver mismatch |
| train_uk_baselines | 2461467 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_baselines | 2461468 | L40S, 4 CPU, 64G | canceled before training |
| train_uk_lang | 2461469 | L40S, 4 CPU, 64G | canceled after startup CUDA failure |
| train_uk_mt | 2461470 | L40S, 4 CPU, 64G | canceled before training |
| train_uk_edit | 2461471 | L40S, 4 CPU, 64G | canceled before training |
| train_uk_qa | 2461472 | L40S, 4 CPU, 64G | canceled before training |
| train_uk_mr | 2461473 | L40S, 4 CPU, 64G | canceled before training |
| train_uk_format | 2461474 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_lang | 2461475 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_mt | 2461476 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_edit | 2461477 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_qa | 2461478 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_mr | 2461479 | L40S, 4 CPU, 64G | canceled before training |
| train_sorbian_format | 2461480 | L40S, 4 CPU, 64G | canceled before training |
| eval_uk_baselines | 2461482 | L40S, 4 CPU, 64G | canceled dependency chain |
| eval_sorbian_baselines | 2461483 | L40S, 4 CPU, 64G | canceled dependency chain |
| eval_uk_specialists | 2461484 | L40S, 4 CPU, 64G | canceled dependency chain |
| eval_sorbian_specialists | 2461485 | L40S, 4 CPU, 64G | canceled dependency chain |

## Relaunched Phase 3 Jobs

| Job | ID | GPU Request | Status |
|---|---:|---|---|
| eval_base_uk | 2461502 | L40S, 4 CPU, 64G | canceled after evaluator batching fix |
| eval_base_sorbian | 2461503 | L40S, 4 CPU, 64G | canceled after evaluator batching fix |
| eval_base_uk | 2461522 | L40S, 4 CPU, 64G | queued with batched evaluator |
| eval_base_sorbian | 2461523 | L40S, 4 CPU, 64G | queued with batched evaluator |
| train_uk_baselines | 2461504 | L40S, 4 CPU, 64G | queued |
| train_sorbian_baselines | 2461505 | L40S, 4 CPU, 64G | queued |
| train_uk_lang | 2461506 | L40S, 4 CPU, 64G | running on `g014` |
| train_uk_mt | 2461507 | L40S, 4 CPU, 64G | queued |
| train_uk_edit | 2461508 | L40S, 4 CPU, 64G | queued |
| train_uk_qa | 2461509 | L40S, 4 CPU, 64G | queued |
| train_uk_mr | 2461510 | L40S, 4 CPU, 64G | queued |
| train_uk_format | 2461511 | L40S, 4 CPU, 64G | queued |
| train_sorbian_lang | 2461512 | L40S, 4 CPU, 64G | queued |
| train_sorbian_mt | 2461513 | L40S, 4 CPU, 64G | queued |
| train_sorbian_edit | 2461514 | L40S, 4 CPU, 64G | queued |
| train_sorbian_qa | 2461515 | L40S, 4 CPU, 64G | queued |
| train_sorbian_mr | 2461516 | L40S, 4 CPU, 64G | queued |
| train_sorbian_format | 2461517 | L40S, 4 CPU, 64G | queued |
| eval_uk_baselines | 2461518 | L40S, 4 CPU, 64G | dependency: 2461504 |
| eval_sorbian_baselines | 2461519 | L40S, 4 CPU, 64G | dependency: 2461505 |
| eval_uk_specialists | 2461520 | L40S, 4 CPU, 64G | dependency: Ukrainian specialists |
| eval_sorbian_specialists | 2461521 | L40S, 4 CPU, 64G | dependency: Sorbian specialists |

## Updated Active Queue Records

| Job | ID | Status | Notes |
|---|---:|---|---|
| train_uk_lang | 2461506 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/lang`. |
| train_uk_mt | 2461507 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/mt`. |
| train_uk_edit | 2461508 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/edit_scgc`. |
| train_uk_qa | 2461509 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/qa`. |
| train_uk_mr | 2461510 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/mr`. |
| train_uk_format | 2461511 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/format`. |
| train_sorbian_lang | 2461512 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/lang`. |
| train_sorbian_mt | 2461513 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/mt`. |
| train_sorbian_edit | 2461514 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/edit_scgc`. |
| train_sorbian_qa | 2461515 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/qa`. |
| train_sorbian_mr | 2461516 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/mr`. |
| train_sorbian_format | 2461517 | completed | Checkpoint written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/format`. |
| eval_base_uk | 2461528 | completed | Overall 32.386 on locked validation. |
| eval_base_sorbian | 2461529 | completed | Overall 27.539 on locked validation. |
| train_uk_baselines | 2461539 | completed | Four baseline checkpoints written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/baselines/`. |
| eval_uk_baselines | 2461540 | completed | All four Ukrainian baselines evaluated; external-enhanced is the best baseline so far at 32.839 overall. |
| train_sorbian_baselines | 2461541 | completed | Four baseline checkpoints written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/baselines/`. |
| eval_sorbian_baselines | 2461542 | canceled | Paused for triage after official-only result landed at 27.563 overall. |
| eval_uk_specialists | 2461547 | canceled | Paused for triage after M_lang, M_mt, M_edit, M_qa, and M_mr results landed; M_format did not finish. |
| eval_sorbian_specialists | 2461551 | canceled | Paused for triage after M_lang result landed. |
| merge_uk | 2461548 | canceled | Canceled before start; merge search paused until MR and SC/GC triage passes. |
| merge_sorbian | 2461552 | canceled | Canceled before start; merge search paused until MR and SC/GC triage passes. |
| polish_uk | 2461549 | canceled | Canceled before start. |
| polish_sorbian | 2461553 | canceled | Canceled before start. |
| eval_uk_final | 2461550 | canceled | Canceled before start. |
| eval_sorbian_final | 2461554 | canceled | Canceled before start. |

## Current Decision State

- Ukrainian final model: none selected; first-pass trained artifacts were discarded.
- Sorbian final model: none selected; first-pass trained artifacts were discarded.
- Official evaluator reconciliation: pending organizer release/check.

## Triage Snapshot

- `make triage-oracle` passes locally.
- Gold-target oracle checks give 100 for QA, MR, SC, and GC on both tracks.
- MT oracle sanity is high: Ukrainian chrF++ 99.793, Sorbian chrF++ 100.000.
- Raw prediction dumps, SC/GC diagnostics, MR normalization inspection, and same-set overfit checks have run.
- Root cause found: first-pass SC/GC mixtures were almost all error cases, producing an always-error detector prior that matches the observed ~66% detection F1 plateau.
- MR zero scores were partly a parser/normalization artifact, but MR remains genuinely weak and needs a better final-answer-only preservation setup.
- Same-set Ukrainian overfit checks passed: SC detection/correction F1 100.0/89.7, GC detection/correction F1 91.4/93.3, MR accuracy 100.0 on 20 examples.
- Same-set Sorbian overfit checks passed: SC detection/correction F1 86.7/89.7, GC detection/correction F1 90.3/93.3, MR accuracy 100.0 on 20 examples.
- Local remediation gates now pass: `make validate`, `make check-governance`, `make check-overlap`, `make triage-oracle`, `make triage-data-sanity`, `make report-edit-data-balance`, `make report-mr-data-quality`, and `make smoke-test`.
- MR preservation data now includes final-answer-only SFT rows in `data/processed/final/*/mr_format_preservation.jsonl`.
- Active train configs write to `checkpoints/phase3_fixed/...` and no longer write into invalid first-pass checkpoint paths.

## Artifact Cleanup

Cleanup date: 2026-05-21.

- Removed remote stale checkpoints under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/{baselines,specialists}` and `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/{baselines,specialists}`.
- Remote triage overfit checkpoints are temporarily retained under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/triage/overfit/` for checkpoint-loading sanity and will be pruned after fixed retraining/evaluation evidence is captured.
- Removed stale first-pass local/remote tuned-model eval JSONs, `training_runs.jsonl`, `eval_runs.jsonl`, `merge_runs.jsonl`, `final_model_selection.json`, and specialist interference matrices.
- Removed old non-triage Slurm logs for canceled/bad first-pass Phase 3 jobs.
- Preserved prompt-only base result JSONs and all triage reports/raw diagnostics.
- Remote cleanup manifest: `/home/scheppat/workspace/projects/wmt26_lrllm/results/triage/cleanup_manifest_20260521T060636Z.txt`.

## Local Gate Baseline

The Phase 2 local gates passed before Phase 3 launch:

- `make validate`
- `make inspect-data`
- `make prepare-data`
- `make smoke-test`
- `make report-data-quality`
- `make check-governance`
- `make check-overlap`
- `make build-final-mixtures`
