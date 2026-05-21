#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=long
#SBATCH --time=5-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=eval_sorbian_baselines
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{data,checkpoints,logs,results,tmp}

# GPU preference for this project: h200 first, then a100, then l40s.
# If an h200 job waits too long, resubmit with:
#   sbatch --gres=gpu:a100:1 this_job.slurm
#   sbatch --gres=gpu:l40s:1 this_job.slurm

andromeda/scripts/run_step.sh bash -lc 'python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/sorbian/baselines/official_only --output results/sorbian/baselines/official_only.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/sorbian/baselines/naive_multitask --output results/sorbian/baselines/naive_multitask.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/sorbian/baselines/task_balanced --output results/sorbian/baselines/task_balanced.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/sorbian/baselines/external_enhanced_multitask --output results/sorbian/baselines/external_enhanced.json'
