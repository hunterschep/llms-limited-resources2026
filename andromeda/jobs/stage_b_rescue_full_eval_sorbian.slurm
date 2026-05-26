#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=stage_b_full_eval_sorbian
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable. Do not use V100.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export CANDIDATE_NAME="${CANDIDATE_NAME:-stage_b_mt_large}"
export CANDIDATE_MODEL="${CANDIDATE_MODEL:-$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large}"
export FULL_EVAL_CONFIG="${FULL_EVAL_CONFIG:-configs/eval/sorbian.yaml}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/stage_b_rescue/full_eval results/stage_b_rescue/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$CANDIDATE_MODEL"
  sha256sum "$FULL_EVAL_CONFIG" | tee results/stage_b_rescue/status/full_eval_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/stage_b_full_eval_candidates.py --config "$FULL_EVAL_CONFIG" --run --candidate "$CANDIDATE_NAME" "$CANDIDATE_MODEL"
'
