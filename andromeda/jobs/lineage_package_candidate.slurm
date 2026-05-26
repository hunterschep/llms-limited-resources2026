#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --job-name=lineage_package_candidate
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export CANDIDATE_MODEL="${CANDIDATE_MODEL:-$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_merged}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/package results/lineage_recovery/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$CANDIDATE_MODEL"
  python3 scripts/lineage_package_candidate.py --model-dir "$CANDIDATE_MODEL" --dry-run
  python3 scripts/lineage_validate_package.py --model-dir "$CANDIDATE_MODEL"
'
