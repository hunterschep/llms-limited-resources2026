# Phase 3 Dashboard

Status: training in progress on Andromeda. The Phase 3 goal is not complete yet.

## Current Snapshot

Last updated: 2026-05-20.

- Remote revision: `57cfa94a9ba877c95df4ba13e87da38b47292816`.
- Environment, governance validation, data preparation, and GPU smoke validation have passed on Andromeda.
- Completed specialist checkpoints: all six Ukrainian specialists and all six Sorbian specialists.
- Active jobs: Ukrainian baseline eval 2461540, Sorbian baseline eval 2461542, Ukrainian specialist eval 2461547, and Sorbian specialist eval 2461551.
- Latest completed partial results: Sorbian prompt-only has overall 27.539 and Sorbian M_lang has 26.669. Ukrainian official-only SFT has overall 29.857, naive multitask has 31.726, task-balanced has 32.276, M_lang has 32.940, M_mt has 34.541, and M_edit has 30.088. M_mt is currently the best measured Ukrainian candidate, but it lowers MT chrF++ and collapses MR.
- Queued next: merge, polish, and final eval chains.
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
| eval_uk_baselines | 2461540 | running | Official-only, naive multitask, and task-balanced results landed; remaining Ukrainian baselines still evaluating. |
| train_sorbian_baselines | 2461541 | completed | Four baseline checkpoints written under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/baselines/`. |
| eval_sorbian_baselines | 2461542 | running | Started after 2461541 completed. |
| eval_uk_specialists | 2461547 | running | M_lang, M_mt, and M_edit results landed; remaining Ukrainian specialists still evaluating. |
| eval_sorbian_specialists | 2461551 | running | M_lang result landed; remaining Sorbian specialists still evaluating. |
| merge_uk | 2461548 | dependency | Depends on 2461547. |
| merge_sorbian | 2461552 | dependency | Depends on 2461551. |
| polish_uk | 2461549 | dependency | Depends on 2461548. |
| polish_sorbian | 2461553 | dependency | Depends on 2461552. |
| eval_uk_final | 2461550 | dependency | Depends on 2461549. |
| eval_sorbian_final | 2461554 | dependency | Depends on 2461553. |

## Current Decision State

- Ukrainian final model: pending.
- Sorbian final model: pending.
- Official evaluator reconciliation: pending organizer release/check.

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
