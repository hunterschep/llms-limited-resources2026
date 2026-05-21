# Phase 3 Evaluation Log

This file records evaluation events. Machine-readable evaluation records live in `results/eval_runs.jsonl`.

## Evaluation Queue

| Eval | Track | Checkpoint | Split | Status | Notes |
|---|---|---|---|---|---|
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | planned | Prompt-only baseline. |
| base_prompt_sorbian | Sorbian | Qwen/Qwen3.5-2B | locked validation | planned | Prompt-only baseline. |
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | canceled job 2461465 | L40S fallback started, but PyTorch could not initialize CUDA because the installed torch wheel required a newer driver. |
| base_prompt_sorbian | Sorbian | Qwen/Qwen3.5-2B | locked validation | canceled job 2461466 | L40S fallback started, but PyTorch could not initialize CUDA because the installed torch wheel required a newer driver. |
| uk_baselines | Ukrainian | baseline checkpoints | locked validation | canceled job 2461482 | Dependency chain canceled for environment repair. |
| sorbian_baselines | Sorbian | baseline checkpoints | locked validation | canceled job 2461483 | Dependency chain canceled for environment repair. |
| uk_specialists | Ukrainian | specialist checkpoints | locked validation | canceled job 2461484 | Dependency chain canceled for environment repair. |
| sorbian_specialists | Sorbian | specialist checkpoints | locked validation | canceled job 2461485 | Dependency chain canceled for environment repair. |
| gpu_env_validation | all | environment | GPU node | pending relaunch | Added `andromeda/jobs/00_validate_gpu_env.slurm` to require `torch.cuda.is_available()` before restarting training. |

## Required Metrics

MT chrF++, MT BLEU, QA accuracy, SC detection F1, SC correction F1, GC detection F1, GC correction F1, MR accuracy, task-normalized scores, and overall equal-weighted score.
