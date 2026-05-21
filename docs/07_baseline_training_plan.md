# Baseline Training Plan

The research claim requires strong baselines. We will compare skill-vector merging against generic SFT strategies.

Required baselines:

1. Prompt-only Qwen3.5-2B.
2. Official-train-only SFT.
3. Naive multitask SFT using pooled examples.
4. Task-balanced SFT with capped/equal task sampling.
5. Optional language-adapted baseline if compute allows.

Base model:

- https://huggingface.co/Qwen/Qwen3.5-2B

Configs:

- `configs/train/baseline_official_only_uk.yaml`
- `configs/train/baseline_official_only_sorbian.yaml`
- `configs/train/baseline_naive_multitask_uk.yaml`
- `configs/train/baseline_naive_multitask_sorbian.yaml`
- `configs/train/baseline_task_balanced_uk.yaml`
- `configs/train/baseline_task_balanced_sorbian.yaml`

Training entrypoints:

- `scripts/train_sft.py`
- `scripts/train_lora.py`
- `scripts/train_qlora.py`

Local smoke tests use `--dry-run --max-examples N`; Andromeda jobs run the same configs without dry-run.

LoRA: https://arxiv.org/abs/2106.09685  
QLoRA: https://arxiv.org/abs/2305.14314
