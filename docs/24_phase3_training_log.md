# Phase 3 Training Log

This file records training launch and diagnosis notes. Machine-readable run records live in `results/training_runs.jsonl`.

## Launch Log

| Time | Track | Run | Slurm Job ID | Status | Notes |
|---|---|---|---:|---|---|
| 2026-05-20 | all | environment creation | 2461442 | completed | Created/updated `wmt26-lrllm` on Andromeda short partition. |
| 2026-05-20 | all | environment validation | 2461449 | completed | `00_validate_env.slurm` exited 0. |
| 2026-05-20 | all | data preparation | 2461453 | completed | `make validate inspect-data prepare-data smoke-test` exited 0 on Andromeda. |
| 2026-05-20 | uk | baseline suite | 2461467 | canceled | Canceled before training after GPU jobs showed PyTorch CUDA-driver mismatch. |
| 2026-05-20 | sorbian | baseline suite | 2461468 | canceled | Canceled before training after GPU jobs showed PyTorch CUDA-driver mismatch. |
| 2026-05-20 | uk | specialists | 2461469-2461474 | canceled | `train_uk_lang` began but PyTorch could not initialize CUDA; all specialist jobs were canceled for environment repair. |
| 2026-05-20 | sorbian | specialists | 2461475-2461480 | canceled | Canceled before training after GPU jobs showed PyTorch CUDA-driver mismatch. |
| 2026-05-20 | all | environment repair | local patch | ready to sync | `andromeda/env/create_env.sh` now pins PyTorch to CUDA 12.8 wheels and adds a GPU validation job. |
| 2026-05-20 | all | environment repair | 2461496 | completed | Reinstalled `torch==2.8.0+cu128`; env reports `torch_cuda=12.8`. |
| 2026-05-20 | all | GPU validation | 2461500 | completed | V100 CUDA smoke test passed with `cuda_available=True`; H200/A100/L40S duplicate probes were canceled while pending. |
| 2026-05-20 | uk | baseline suite | 2461504 | queued | L40S fallback request; runs official-only, naive, task-balanced, and external-enhanced baselines sequentially. |
| 2026-05-20 | sorbian | baseline suite | 2461505 | queued | L40S fallback request; runs official-only, naive, task-balanced, and external-enhanced baselines sequentially. |
| 2026-05-20 | uk | specialists | 2461506-2461511 | queued | Individual language, MT, edit, QA, MR, and format specialist jobs on L40S fallback. |
| 2026-05-20 | sorbian | specialists | 2461512-2461517 | queued | Individual language, MT, edit, QA, MR, and format specialist jobs on L40S fallback. |
| 2026-05-20 | uk | specialists | 2461506-2461511 | completed | All six Ukrainian specialists completed and wrote checkpoints under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/uk/specialists/`. |
| 2026-05-20 | sorbian | language specialist | 2461512 | completed | Completed in 4m30s and wrote `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/lang`. |
| 2026-05-20 | sorbian | MT specialist | 2461513 | completed | Completed in 5m08s and wrote `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/mt`. |
| 2026-05-20 | sorbian | edit specialist | 2461514 | completed | Completed in 3m05s and wrote `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/edit_scgc`. |
| 2026-05-20 | sorbian | QA specialist | 2461515 | completed | Completed in 1m36s and wrote `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/qa`. |
| 2026-05-20 | sorbian | MR specialist | 2461516 | completed | Completed in 1m02s and wrote `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/mr`. |
| 2026-05-20 | sorbian | format specialist | 2461517 | completed | Completed in 1m14s and wrote `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/sorbian/specialists/format`. |
| 2026-05-20 | uk | specialist eval/merge chain | 2461520, 2461531-2461533 | canceled/resubmitted | Old submissions carried an L40S-blocking exclusion list; resubmitted cleanly as 2461547-2461550. |
| 2026-05-20 | sorbian | specialist eval/merge chain | 2461521, 2461534-2461536 | canceled/resubmitted | Old submissions carried an L40S-blocking exclusion list; resubmitted cleanly as 2461551-2461554. |
| 2026-05-20 | all | scheduler adjustment | 83e1826 | synced | Regenerated Phase 3 baseline, eval, merge, polish, and final-eval jobs on `medium` to avoid the short-partition node availability issue. |
| 2026-05-20 | uk | baseline suite | 2461504 | canceled/resubmitted | Old submission carried an exclusion list that made L40S placement impossible; resubmitted cleanly as 2461539. |
| 2026-05-20 | sorbian | baseline suite | 2461505 | canceled/resubmitted | Old submission carried an exclusion list that made L40S placement impossible; resubmitted cleanly as 2461541. |
| 2026-05-20 | uk | baseline suite | 2461539 | running | Official-only, naive multitask, and task-balanced checkpoints have completed; external-enhanced is in progress. |
| 2026-05-20 | sorbian | baseline suite | 2461541 | running | Official-only and naive multitask checkpoints have completed; task-balanced/external-enhanced are in progress. |
| 2026-05-20 | all | eval progress logging | ee33882 | synced | Future eval jobs print task and batch progress; running eval jobs that started earlier will not show these progress lines. |

## Run Fields

Each training run should record `run_id`, `track`, `model_type`, `base_checkpoint`, `config_path`, `data_mixture_id`, `seed`, `timestamp`, `git_commit`, `andromeda_job_id`, `gpu_type`, `train_steps`, `epochs`, `effective_batch_size`, `learning_rate`, `lora_config`, `precision`, `checkpoint_path`, `log_path`, `status`, and `notes`.
