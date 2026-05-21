# Phase 3 Dashboard

Status: initialized.

## Remote Jobs

| Job | ID | Status | Notes |
|---|---:|---|---|
| 00_create_env | 2461442 | completed | Created/updated `wmt26-lrllm` on Andromeda. |
| 00_validate_env | 2461449 | completed | Environment and governance validation passed. |
| 01_prepare_data | 2461453 | completed | Data preparation and smoke tests passed on Andromeda. |
| train_uk_all |  | planned | Train Ukrainian specialists, merge, and polish if stable. |
| train_sorbian_all |  | planned | Train Sorbian specialists, merge, and polish if stable. |

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
