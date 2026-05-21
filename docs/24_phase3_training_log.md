# Phase 3 Training Log

This file records training launch and diagnosis notes. Machine-readable run records live in `results/training_runs.jsonl`.

## Launch Log

| Time | Track | Run | Slurm Job ID | Status | Notes |
|---|---|---|---:|---|---|
| 2026-05-20 | all | environment creation | 2461442 | submitted | Submitted `00_create_env.slurm` on Andromeda short partition. |
| pending | all | environment validation |  | planned | Submit `00_validate_env.slurm` after environment creation. |
| pending | all | data preparation |  | planned | Submit `01_prepare_data.slurm` after environment validation. |

## Run Fields

Each training run should record `run_id`, `track`, `model_type`, `base_checkpoint`, `config_path`, `data_mixture_id`, `seed`, `timestamp`, `git_commit`, `andromeda_job_id`, `gpu_type`, `train_steps`, `epochs`, `effective_batch_size`, `learning_rate`, `lora_config`, `precision`, `checkpoint_path`, `log_path`, `status`, and `notes`.
