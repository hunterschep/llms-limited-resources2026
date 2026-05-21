# Andromeda Execution

The live Andromeda probe on 2026-05-21 confirmed:

- Login host: `a002.m31.bc.edu`
- User: `scheppat`
- Slurm: `23.11.10`
- Default account: `prudlab`
- Scratch root: `/scratch/scheppat`
- Recommended project root: `/scratch/scheppat/projects/<project_slug>` for data/checkpoints
- Project code root used by jobs: `/home/scheppat/workspace/projects/wmt26_lrllm`

The cluster has `h200`, `a100`, `l40s`, `v100`, and other GPU GRES visible in `short`, `medium`, and `long`. Job scripts request `gpu:h200:1` by default because H200 is fastest when available. If H200 queue time is too long, resubmit a job with:

```bash
sbatch --gres=gpu:a100:1 andromeda/jobs/train_uk_mt.slurm
sbatch --gres=gpu:l40s:1 andromeda/jobs/train_uk_mt.slurm
```

## Setup

Sync code:

```bash
rsync -avP --exclude .git/ /Users/hunterschep/llms-limited-resources2026/ andromeda:/home/scheppat/workspace/projects/wmt26_lrllm/
```

Create environment on an interactive/allocated node, not the login node:

```bash
cd /home/scheppat/workspace/projects/wmt26_lrllm
sbatch andromeda/jobs/00_create_env.slurm
sbatch andromeda/jobs/00_validate_env.slurm
# for dependency install, request an interactive allocation then:
bash andromeda/env/create_env.sh
```

Prepare data:

```bash
sbatch andromeda/jobs/01_prepare_data.slurm
```

The second-stage data layer can also be run as separate jobs:

```bash
sbatch andromeda/jobs/02_download_external_data.slurm
sbatch andromeda/jobs/03_filter_external_data.slurm
sbatch andromeda/jobs/04_compile_external_data.slurm
sbatch andromeda/jobs/05_report_data_quality.slurm
```

## Phase 3 Pause / Triage

The Phase 3 merge and polish campaign is paused as of 2026-05-21. Do not submit additional full training, merge, polish, or final-eval jobs until `docs/33_phase3_triage_remediation.md` gates pass.

Use these triage jobs first after syncing the current repo:

```bash
sbatch andromeda/jobs/triage_oracle.slurm
sbatch andromeda/jobs/triage_raw_predictions_uk.slurm
sbatch andromeda/jobs/triage_raw_predictions_sorbian.slurm
sbatch andromeda/jobs/triage_checkpoint_loading_uk.slurm
sbatch andromeda/jobs/triage_checkpoint_loading_sorbian.slurm
```

The raw-prediction and checkpoint-loading jobs request H200 by default. If H200 queue time is too long, use:

```bash
sbatch --gres=gpu:a100:1 andromeda/jobs/triage_raw_predictions_uk.slurm
sbatch --gres=gpu:l40s:1 andromeda/jobs/triage_raw_predictions_uk.slurm
```

## Launch Sequence

```bash
sbatch andromeda/jobs/train_uk_all.slurm
sbatch andromeda/jobs/train_sorbian_all.slurm
sbatch andromeda/jobs/eval_uk_final.slurm
sbatch andromeda/jobs/eval_sorbian_final.slurm
```

Full recommended sequence:

1. Sync repo.
2. `sbatch andromeda/jobs/00_create_env.slurm`
3. `sbatch andromeda/jobs/00_validate_env.slurm`
4. `sbatch andromeda/jobs/02_download_external_data.slurm`
5. `sbatch andromeda/jobs/03_filter_external_data.slurm`
6. `sbatch andromeda/jobs/04_compile_external_data.slurm`
7. `sbatch andromeda/jobs/05_report_data_quality.slurm`
8. `sbatch andromeda/jobs/01_prepare_data.slurm`
9. Train baselines/specialists.
10. Merge.
11. Polish.
12. Evaluate.

For more controlled runs, submit specialists individually:

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

Replace `uk` with `sorbian` for the Sorbian track.

## Monitoring

```bash
ssh andromeda 'squeue -u "$USER" -o "%i|%j|%P|%t|%M|%l|%D|%C|%m|%b|%R"'
ssh andromeda 'acct-chk "$USER"'
ssh andromeda 'tail -n 80 /home/scheppat/logs/<job>.out'
```

## Resume

Training configs write to `checkpoints/<track>/...`. Rerun the same Slurm job after verifying that the training script detects existing output or pass a future explicit resume flag when added. Never delete active `WorkDir`, `StdOut`, `StdErr`, or checkpoint roots while jobs are running.
