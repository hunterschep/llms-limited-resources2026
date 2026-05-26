#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --job-name=competitive_package_uk
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
export FINAL_MODEL="${FINAL_MODEL:-$SCRATCH_ROOT/checkpoints/competitive_reboot/uk/stage_c_doc_mt_format}"
cd "$PROJECT_ROOT"

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  python3 scripts/competitive_package_model.py --track uk --model-dir "$FINAL_MODEL" --output-dir results/competitive_reboot/package --dry-run
'
