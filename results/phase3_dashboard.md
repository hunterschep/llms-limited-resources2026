# Phase 3 Dashboard

Status: paused for triage/remediation. The Phase 3 goal is not complete yet.

## Current Snapshot

Last updated: 2026-05-21.

- Remote revision: `57cfa94a9ba877c95df4ba13e87da38b47292816`.
- Environment, governance validation, data preparation, and GPU smoke validation have passed on Andromeda.
- Completed specialist checkpoints from the first Phase 3 pass were deleted from Andromeda scratch after triage because they were trained/evaluated against known-bad edit mixtures and overly strict MR scoring.
- Active jobs: none. The remaining eval, merge, polish, and final-eval jobs were canceled for triage on 2026-05-21.
- Latest retained results: prompt-only base evaluations, triage evidence, and local remediation sanity outputs only. The stale first-pass tuned-model result JSONs and interference matrices were removed locally and remotely so the next run starts with clean experiment records.
- Queued next: fixed retraining only: `M_edit`, `M_mr`, task-balanced, and external-enhanced for each track. Merge search remains blocked until fixed evaluations clear the gates in `docs/42_phase3_resume_or_block_merge_decision.md`.
- Baseline suites were resubmitted as 2461539 and 2461541 because the earlier queued jobs carried an L40S-blocking exclusion list.
- All Phase 3 train/eval/merge/polish job templates now use the `medium` partition for better placement reliability.

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
- Raw prediction dumps, SC/GC diagnostics, MR normalization inspection, and Ukrainian same-set overfit checks have run.
- Root cause found: first-pass SC/GC mixtures were almost all error cases, producing an always-error detector prior that matches the observed ~66% detection F1 plateau.
- MR zero scores were partly a parser/normalization artifact, but MR remains genuinely weak and needs a better final-answer-only preservation setup.
- Same-set Ukrainian overfit checks passed: MR reached 100% on 20 examples; SC reached 93.3% detection/correction F1 on 20 examples.
- Local remediation gates now pass: `make validate`, `make check-governance`, `make check-overlap`, `make triage-oracle`, `make triage-data-sanity`, `make report-edit-data-balance`, `make report-mr-data-quality`, and `make smoke-test`.
- MR preservation data now includes final-answer-only SFT rows in `data/processed/final/*/mr_format_preservation.jsonl`.
- Active train configs write to `checkpoints/phase3_fixed/...` and no longer write into invalid first-pass checkpoint paths.

## Artifact Cleanup

Cleanup date: 2026-05-21.

- Removed remote stale checkpoints under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/{baselines,specialists}` and `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/{baselines,specialists}`.
- Removed remote triage overfit checkpoints after retaining the summarized evidence under `results/triage/`.
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
