#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=triage_ckpt_sorb
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"
export WMT26_RECORD_RUNS=0

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{data,checkpoints,logs,results,tmp}

andromeda/scripts/run_step.sh bash -lc '
set -euo pipefail
for ckpt in checkpoints/sorbian/specialists/lang checkpoints/sorbian/specialists/mt checkpoints/sorbian/specialists/edit_scgc checkpoints/sorbian/specialists/qa checkpoints/sorbian/specialists/mr; do
  python3 scripts/check_checkpoint_loading.py --config configs/eval/sorbian.yaml --base-model Qwen/Qwen3.5-2B --checkpoint "$ckpt" --per-task 10
done
'
