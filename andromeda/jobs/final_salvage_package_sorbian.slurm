#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --job-name=final_salvage_package_sorbian
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
export MODEL_DIR="${MODEL_DIR:-$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10}"
export PACKAGE_DIR="${PACKAGE_DIR:-$SCRATCH_ROOT/checkpoints/final_salvage/sorbian_primary_package}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/package results/final_salvage/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$MODEL_DIR"
  python3 scripts/final_salvage_package_model.py --model-dir "$MODEL_DIR" --package-dir "$PACKAGE_DIR" --track sorbian --label primary --copy
  python3 scripts/final_salvage_validate_package.py --model-dir "$PACKAGE_DIR/model" --output results/final_salvage/package/sorbian_primary_validation.json
'
