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
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | queued as 2461528 | Relaunched on `medium` after short-partition placement issue. |
| base_prompt_sorbian | Sorbian | Qwen/Qwen3.5-2B | locked validation | queued as 2461529 | Relaunched on `medium` after short-partition placement issue. |
| uk_baselines | Ukrainian | baseline checkpoints | locked validation | queued as 2461540 | Depends on clean resubmission 2461539. |
| sorbian_baselines | Sorbian | baseline checkpoints | locked validation | queued as 2461542 | Depends on clean resubmission 2461541. |
| uk_specialists | Ukrainian | specialist checkpoints | locked validation | queued as 2461520 | Ukrainian specialist prerequisites are complete; waits only on priority/resources. |
| sorbian_specialists | Sorbian | specialist checkpoints | locked validation | queued as 2461521 | Depends on Sorbian specialist jobs 2461512-2461517. |
| merge_uk | Ukrainian | specialist task vectors | capped validation during search | queued as 2461531 | Depends on 2461520. |
| merge_sorbian | Sorbian | specialist task vectors | capped validation during search | queued as 2461534 | Depends on 2461521. |
| polish_uk | Ukrainian | best merged checkpoint | locked validation follow-up | queued as 2461532 | Moved to `medium`; depends on 2461531. |
| polish_sorbian | Sorbian | best merged checkpoint | locked validation follow-up | queued as 2461535 | Moved to `medium`; depends on 2461534. |
| uk_specialists | Ukrainian | specialist checkpoints | locked validation | resubmitted as 2461547 | Clean L40S submission with no excluded GPU nodes. |
| sorbian_specialists | Sorbian | specialist checkpoints | locked validation | resubmitted as 2461551 | Clean L40S submission with no excluded GPU nodes. |
| merge_uk | Ukrainian | specialist task vectors | capped validation during search | resubmitted as 2461548 | Depends on 2461547. |
| merge_sorbian | Sorbian | specialist task vectors | capped validation during search | resubmitted as 2461552 | Depends on 2461551. |
| polish_uk | Ukrainian | best merged checkpoint | locked validation follow-up | resubmitted as 2461549 | Depends on 2461548. |
| polish_sorbian | Sorbian | best merged checkpoint | locked validation follow-up | resubmitted as 2461553 | Depends on 2461552. |
| eval_uk_final | Ukrainian | final polished checkpoint | locked validation | resubmitted as 2461550 | Depends on 2461549. |
| eval_sorbian_final | Sorbian | final polished checkpoint | locked validation | resubmitted as 2461554 | Depends on 2461553. |
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | completed job 2461528 | Overall 32.386; MT chrF++ 41.135, QA 33.994, SC score 46.667, GC score 35.967, MR 4.167. |
| uk_baselines | Ukrainian | baseline checkpoints | locked validation | running job 2461540 | Started after baseline training job 2461539 completed. |
| uk_baseline_official_only | Ukrainian | checkpoints/uk/baselines/official_only | locked validation | completed within job 2461540 | Overall 29.857; QA improves to 40.793, but SC correction drops to 1.987, GC correction to 0.000, and MR to 0.000. |
| uk_specialist_lang | Ukrainian | checkpoints/uk/specialists/lang | locked validation | completed within job 2461547 | Overall 32.940; MT and SC improve over prompt-only, QA and MR regress. |
| uk_specialist_mt | Ukrainian | checkpoints/uk/specialists/mt | locked validation | completed within job 2461547 | Overall 34.541; despite lower MT chrF++ 38.358, it improves QA/SC/GC relative to prompt-only and again collapses MR to 0.000. |
| sorbian_baselines | Sorbian | baseline checkpoints | locked validation | running job 2461542 | Started after baseline training job 2461541 completed. |

## Required Metrics

MT chrF++, MT BLEU, QA accuracy, SC detection F1, SC correction F1, GC detection F1, GC correction F1, MR accuracy, task-normalized scores, and overall equal-weighted score.
