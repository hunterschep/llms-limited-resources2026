#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --job-name=final_salvage_validate_package
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
export MODEL_DIR="${MODEL_DIR:-$SCRATCH_ROOT/checkpoints/final_salvage/sorbian_primary_package/model}"
export LOAD_CHECK="${LOAD_CHECK:-1}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/package

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  args=(--model-dir "$MODEL_DIR" --output results/final_salvage/package/package_validation_${SLURM_JOB_ID:-local}.json)
  if [[ "$LOAD_CHECK" == "1" ]]; then
    args+=(--load)
  fi
  python3 scripts/final_salvage_validate_package.py "${args[@]}"
'
