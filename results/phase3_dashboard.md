# Phase 3 Dashboard

Status: initialized.

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
