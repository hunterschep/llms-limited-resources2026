#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --job-name=final_salvage_build_scgc_calibration
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/data/final_scgc_calibration_sorbian.yaml | tee results/final_salvage/status/build_calibration_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/build_final_scgc_calibration_data.py
  python3 scripts/validate_data_governance.py
  python3 scripts/check_dev_overlap.py
'
