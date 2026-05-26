#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=lineage_full_eval_sorbian
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable. Do not use V100.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export EXTRA_CANDIDATE_NAME="${EXTRA_CANDIDATE_NAME:-}"
export EXTRA_CANDIDATE_MODEL="${EXTRA_CANDIDATE_MODEL:-}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/full_eval results/lineage_recovery/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/eval/sorbian.yaml configs/train/lineage_recovery/sorbian_stage_b_eval_checkpoints.yaml | tee results/lineage_recovery/status/full_eval_checksums_${SLURM_JOB_ID:-local}.txt
  if [[ -n "$EXTRA_CANDIDATE_NAME" && -n "$EXTRA_CANDIDATE_MODEL" ]]; then
    python3 scripts/lineage_full_eval_candidates.py --run --candidate "$EXTRA_CANDIDATE_NAME" "$EXTRA_CANDIDATE_MODEL"
  else
    python3 scripts/lineage_full_eval_candidates.py --run
  fi
  python3 scripts/lineage_compare_candidates.py
'
