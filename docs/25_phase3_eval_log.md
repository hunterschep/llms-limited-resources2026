# Phase 3 Evaluation Log

This file records evaluation events. Machine-readable evaluation records live in `results/eval_runs.jsonl`.

## Evaluation Queue

| Eval | Track | Checkpoint | Split | Status | Notes |
|---|---|---|---|---|---|
| base_prompt_uk | Ukrainian | Qwen/Qwen3.5-2B | locked validation | planned | Prompt-only baseline. |
| base_prompt_sorbian | Sorbian | Qwen/Qwen3.5-2B | locked validation | planned | Prompt-only baseline. |

## Required Metrics

MT chrF++, MT BLEU, QA accuracy, SC detection F1, SC correction F1, GC detection F1, GC correction F1, MR accuracy, task-normalized scores, and overall equal-weighted score.
