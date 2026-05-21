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
| gpu_env_validation | all | environment | GPU node | completed job 2461500 | V100 CUDA smoke test passed after `torch==2.8.0+cu128` repair; H200/A100/L40S probes had no immediate resources and were canceled. |
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | canceled job 2461502 | Relaunched after CUDA repair, then canceled after evaluator batching fix to avoid slow one-by-one generation. |
| base_prompt_sorbian | Sorbian | Qwen/Qwen3.5-2B | locked validation | canceled job 2461503 | Relaunched after CUDA repair, then canceled after evaluator batching fix to avoid slow one-by-one generation. |
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | queued as 2461522 | Batched evaluator relaunch on L40S fallback. |
| base_prompt_sorbian | Sorbian | Qwen/Qwen3.5-2B | locked validation | queued as 2461523 | Batched evaluator relaunch on L40S fallback. |
| uk_baselines | Ukrainian | baseline checkpoints | locked validation | queued as 2461518 | Depends on 2461504. |
| sorbian_baselines | Sorbian | baseline checkpoints | locked validation | queued as 2461519 | Depends on 2461505. |
| uk_specialists | Ukrainian | specialist checkpoints | locked validation | queued as 2461520 | Depends on 2461506-2461511. |
| sorbian_specialists | Sorbian | specialist checkpoints | locked validation | queued as 2461521 | Depends on 2461512-2461517. |

## Required Metrics

MT chrF++, MT BLEU, QA accuracy, SC detection F1, SC correction F1, GC detection F1, GC correction F1, MR accuracy, task-normalized scores, and overall equal-weighted score.
