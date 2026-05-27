#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=final_salvage_merge_scgc_calibration
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/calibration_merge results/final_salvage/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/merge/final_salvage/scgc_calibration_merge.yaml | tee results/final_salvage/status/merge_calibration_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/merge_final_scgc_calibration.py --execute
'
