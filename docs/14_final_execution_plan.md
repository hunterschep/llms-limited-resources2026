# Final Execution Plan

## Local Gates

Run locally before Andromeda submission:

```bash
make validate
make inspect-data
make prepare-data
make smoke-test
make build-andromeda-jobs
```

These commands verify governance, create the official inventory, create deterministic local splits, compile canonical datasets, build format preference data, run oracle evaluation smoke tests, run training dry-runs, and validate merge dry-runs.

## Andromeda Setup

Sync repository:

```bash
rsync -avP --exclude .git/ /Users/hunterschep/llms-limited-resources2026/ andromeda:/home/scheppat/workspace/projects/wmt26_lrllm/
```

Validate cluster environment:

```bash
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/00_validate_env.slurm'
```

Prepare data:

```bash
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/01_prepare_data.slurm'
```

## Training

Primary launch:

```bash
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/train_uk_all.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/train_sorbian_all.slurm'
```

Controlled specialist launch:

```bash
sbatch andromeda/jobs/train_uk_lang.slurm
sbatch andromeda/jobs/train_uk_mt.slurm
sbatch andromeda/jobs/train_uk_edit.slurm
sbatch andromeda/jobs/train_uk_qa.slurm
sbatch andromeda/jobs/train_uk_mr.slurm
sbatch andromeda/jobs/train_uk_format.slurm
sbatch andromeda/jobs/merge_uk.slurm
sbatch andromeda/jobs/polish_uk.slurm
```

Repeat with `sorbian`.

Job scripts request H200 by default. If scheduling waits too long, resubmit with `--gres=gpu:a100:1` or `--gres=gpu:l40s:1`.

## Evaluation

```bash
sbatch andromeda/jobs/eval_uk_final.slurm
sbatch andromeda/jobs/eval_sorbian_final.slurm
```

Results should land in:

- `results/uk_final_eval.json`
- `results/sorbian_final_eval.json`

## Final Selection

Select the final model by locked-validation equal-weighted score, not MT alone. If scores are close, prefer the model with fewer format failures and less task collapse.

Final paths:

- `checkpoints/uk/final_polished/`
- `checkpoints/sorbian/final_polished/`
