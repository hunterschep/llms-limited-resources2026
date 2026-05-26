#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=competitive_final_eval_uk
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail
# GPU preference: H200 first; A100/L40S fallback.

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
export FINAL_MODEL="${FINAL_MODEL:-$SCRATCH_ROOT/checkpoints/competitive_reboot/uk/stage_c_doc_mt_format}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/competitive_reboot/eval/uk

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$FINAL_MODEL"
  sha256sum configs/eval/uk.yaml | tee results/competitive_reboot/status/uk_final_eval_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/competitive_eval.py --config configs/eval/uk.yaml --model "$FINAL_MODEL" --output results/competitive_reboot/eval/uk/final_candidate.json --raw-output results/competitive_reboot/eval/uk/final_candidate_raw.jsonl
'
