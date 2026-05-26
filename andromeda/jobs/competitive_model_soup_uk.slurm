#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=competitive_model_soup_uk
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail
# GPU preference: H200 first; A100/L40S fallback.

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/train/competitive/uk_model_soup.yaml configs/merge/competitive_uk.yaml | tee results/competitive_reboot/status/uk_soup_checksums_${SLURM_JOB_ID:-local}.txt
  test -s results/competitive_reboot/eval/uk/stage_a_mt_real_large.json
  echo "Model soup is blocked until at least two evaluated Ukrainian competitive candidates exist."
'
