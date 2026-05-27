#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=final_salvage_eval_sorbian
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
export EXTRA_CANDIDATE_NAME="${EXTRA_CANDIDATE_NAME:-}"
export EXTRA_CANDIDATE_MODEL="${EXTRA_CANDIDATE_MODEL:-}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/eval results/final_salvage/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/eval/sorbian.yaml | tee results/final_salvage/status/eval_checksums_${SLURM_JOB_ID:-local}.txt
  if [[ -n "$EXTRA_CANDIDATE_NAME" && -n "$EXTRA_CANDIDATE_MODEL" ]]; then
    python3 scripts/final_salvage_eval_candidates.py --run --candidate "$EXTRA_CANDIDATE_NAME" "$EXTRA_CANDIDATE_MODEL"
  else
    python3 scripts/final_salvage_eval_candidates.py --run
  fi
'
