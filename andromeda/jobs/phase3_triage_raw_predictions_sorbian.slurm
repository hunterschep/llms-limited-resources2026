#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=phase3_triage_raw_predictions_sorbian
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{data,checkpoints,logs,results,tmp}

# GPU preference for this project: h200 first, then a100, then l40s.
# If an h200 job waits too long, resubmit with:
#   sbatch --gres=gpu:a100:1 this_job.slurm
#   sbatch --gres=gpu:l40s:1 this_job.slurm

andromeda/scripts/run_step.sh bash -lc '
models=(
  "base|Qwen/Qwen3.5-2B"
  "edit|checkpoints/phase3_fixed/sorbian/edit"
  "mr|checkpoints/phase3_fixed/sorbian/mr"
  "task_balanced|checkpoints/phase3_fixed/sorbian/task_balanced"
  "external_enhanced|checkpoints/phase3_fixed/sorbian/external_enhanced"
)
for item in "${models[@]}"; do
  name="${item%%|*}"
  model="${item#*|}"
  output="results/phase3_fixed/raw_predictions/sorbian_${name}.jsonl"
  python3 scripts/triage_raw_predictions.py --config configs/eval/sorbian.yaml --model "$model" --per-task 5 --output "$output" --batch-size 5
  python3 scripts/diagnose_prediction_dump.py --input "$output"
  python3 scripts/report_scgc_confusion.py --input "$output"
  python3 scripts/report_mr_raw_errors.py --input "$output"
done
'
