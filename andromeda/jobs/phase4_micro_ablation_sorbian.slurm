#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=phase4_micro_sorbian
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{checkpoints,logs,results,tmp} results/phase4/micro_ablations

# GPU preference: H200 first, A100 fallback, L40S fallback.

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -s results/phase4/probe/baseline_prompt_only_sorbian.json
  make check-governance check-overlap triage-oracle triage-data-sanity
  sha256sum configs/train/phase4/micro_ablation_grid.yaml configs/eval/phase4_probe_sorbian.yaml data/manifests/final_training_data_summary.md
  python3 scripts/phase4_run_micro_ablations.py --track sorbian --evaluate
'
