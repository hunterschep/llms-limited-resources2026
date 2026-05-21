# Second-Stage Training Readiness

The repo now has a registered, filtered, deduplicated, overlap-checked external/synthetic data layer and final data mixtures.

Required local gates:

```bash
make validate
make inspect-data
make prepare-data
make smoke-test
make report-data-quality
make check-governance
make check-overlap
make build-final-mixtures
```

Training configs now point specialist and external-enhanced baselines at `data/processed/final/...`.

Andromeda execution remains:

```bash
rsync -avP --exclude .git/ /Users/hunterschep/llms-limited-resources2026/ andromeda:/home/scheppat/workspace/projects/wmt26_lrllm/
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/00_validate_env.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/01_prepare_data.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/train_uk_all.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/train_sorbian_all.slurm'
```

Jobs request H200 by default, with A100/L40S fallback documented in `andromeda/README.md`.
