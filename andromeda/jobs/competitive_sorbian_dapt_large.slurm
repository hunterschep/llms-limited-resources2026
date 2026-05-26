#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=medium
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=192G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=competitive_sorbian_dapt_large
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. If unavailable, resubmit with --gres=gpu:a100:1 or --gres=gpu:l40s:1.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/checkpoints/competitive_reboot/sorbian "$SCRATCH_ROOT"/results/competitive_reboot results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  ! grep -R "checkpoints/phase[34]\\|results/phase[34]" configs/train/competitive configs/merge/competitive_*.yaml
  test -s data/processed/competitive/sorbian/stage_a_dapt_large.jsonl
  sha256sum configs/train/competitive/sorbian_dapt_large.yaml data/manifests/competitive_mixture_sorbian.json data/manifests/data_governance_registry.csv configs/eval/sorbian.yaml | tee results/competitive_reboot/status/sorbian_dapt_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/train_competitive.py --config configs/train/competitive/sorbian_dapt_large.yaml
'
