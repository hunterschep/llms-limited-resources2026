# WMT26 Skill-Vector Merged Curriculum Adaptation Runbook

This repository prepares competitive WMT26 submissions for Multitask LLMs with Limited Resources. The research thesis is that a WMT26-compliant 2B model can be improved by decomposing language/task ability into trainable skill vectors, then recomposing them through interference-aware merging.

## Constraints

- Two leaderboards: Ukrainian and Sorbian.
- Each submitted track must cover MT, QA, SC, GC, and MR.
- The five outputs for a track must come from the same model.
- Base model family: Qwen3.5 <=2B, including allowed quantized/Unsloth variants.
- External data must be public and reproducible.
- Do not use WMT2025 test sets, UNLP/MMLU test splits, the official math benchmark or derivatives, extra Sorbian certificate questions, private data, or unlicensed data.

Sources:

- https://www2.statmt.org/wmt26/limited-resources-llm.html
- https://github.com/TUM-NLP/llms-limited-resources2026
- https://huggingface.co/Qwen/Qwen3.5-2B

## Local Commands

```bash
make validate
make inspect-data
make prepare-data
make smoke-test
make build-andromeda-jobs
```

## Data

Official inventory:

- `data/manifests/official_data_inventory.jsonl`
- `docs/02_repo_data_inventory.md`

Governance:

- `data/manifests/data_governance_registry.csv`
- `docs/03_data_governance_policy.md`
- `scripts/validate_data_governance.py`

Processed canonical data:

- `data/processed/uk/*.jsonl`
- `data/processed/sorbian/*.jsonl`

External data must be registered with `scripts/register_external_data.py`, validated, then downloaded through a documented source-specific path.

## Models Trained

For each track:

- Baselines: official-only, naive multitask, task-balanced.
- Specialists: language, MT, SC/GC edit, QA, MR, format.
- Merged candidates: uniform, weighted task-vector, TIES-style dry-run/search scaffold.
- Final polished model: merged checkpoint plus small format polish.

## Scripts

Data:

- `scripts/inspect_repo_data.py`
- `scripts/create_local_splits.py`
- `scripts/compile_mt_data.py`
- `scripts/compile_sc_data.py`
- `scripts/compile_gc_data.py`
- `scripts/compile_qa_data.py`
- `scripts/compile_mr_data.py`
- `scripts/build_language_curriculum.py`
- `scripts/build_format_preference_data.py`

Training:

- `scripts/train_sft.py`
- `scripts/train_lora.py`
- `scripts/train_qlora.py`
- `scripts/train_format_polish.py`

Evaluation:

- `scripts/eval_model.py`
- `scripts/run_all_evals.py`

Merging:

- `scripts/merge_task_vectors.py`
- `scripts/merge_linear.py`
- `scripts/merge_ties.py`
- `scripts/search_merge_weights.py`

## Andromeda

Code root:

```text
/home/scheppat/workspace/projects/wmt26_lrllm
```

Scratch/cache root:

```text
/scratch/scheppat/projects/wmt26_lrllm
/scratch/scheppat/.cache/huggingface
```

Sync:

```bash
rsync -avP --exclude .git/ /Users/hunterschep/llms-limited-resources2026/ andromeda:/home/scheppat/workspace/projects/wmt26_lrllm/
```

Launch:

```bash
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/00_validate_env.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/01_prepare_data.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/train_uk_all.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/train_sorbian_all.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/eval_uk_final.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/eval_sorbian_final.slurm'
```

Jobs request `gpu:h200:1` by default. If wait time is bad, resubmit with `--gres=gpu:a100:1` or `--gres=gpu:l40s:1`.

## Output Directories

- `checkpoints/uk/baselines/`
- `checkpoints/uk/specialists/`
- `checkpoints/uk/merged/`
- `checkpoints/uk/final_polished/`
- `checkpoints/sorbian/baselines/`
- `checkpoints/sorbian/specialists/`
- `checkpoints/sorbian/merged/`
- `checkpoints/sorbian/final_polished/`
- `results/`

## Choosing The Final Model

Choose by locked-validation equal-weighted score:

```text
mean(MT_score, QA_score, SC_score, GC_score, MR_score)
```

Do not pick a model because MT alone is best if it damages QA, MR, SC, or GC.

## Known Risks

- Ukrainian MT has no official train file; competitive training needs registered public parallel data.
- Sorbian QA has only official certificate-derived dev material; competitive training needs public non-certificate QA generation.
- The first SC/GC synthetic compilers are conservative and should be improved with public lexicon/morphology resources.
- Real TIES merge is gated until trained checkpoints exist; current script validates config/search scaffolding.
- Official evaluator details may differ; update `scripts/eval_model.py` once the organizer evaluator is released.
