#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=medium
#SBATCH --time=2-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=eval_phase3_fixed_sorbian
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

andromeda/scripts/run_step.sh bash -lc 'python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model Qwen/Qwen3.5-2B --output results/phase3_fixed/sorbian/base_qwen35_2b.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/edit --output results/phase3_fixed/sorbian/edit.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/mr --output results/phase3_fixed/sorbian/mr.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/task_balanced --output results/phase3_fixed/sorbian/task_balanced.json && python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/external_enhanced --output results/phase3_fixed/sorbian/external_enhanced.json'
