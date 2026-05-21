#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=triage_raw_uk
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"
export WMT26_RECORD_RUNS=0

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{data,checkpoints,logs,results,tmp}

# GPU preference: h200 first, then a100, then l40s.
# Fallback examples:
#   sbatch --gres=gpu:a100:1 andromeda/jobs/triage_raw_predictions_uk.slurm
#   sbatch --gres=gpu:l40s:1 andromeda/jobs/triage_raw_predictions_uk.slurm

andromeda/scripts/run_step.sh bash -lc '
set -euo pipefail
declare -A MODELS=(
  [base_qwen35_2b]="Qwen/Qwen3.5-2B"
  [official_only]="checkpoints/uk/baselines/official_only"
  [external_enhanced]="checkpoints/uk/baselines/external_enhanced_multitask"
  [M_lang]="checkpoints/uk/specialists/lang"
  [M_mt]="checkpoints/uk/specialists/mt"
  [M_edit]="checkpoints/uk/specialists/edit_scgc"
  [M_qa]="checkpoints/uk/specialists/qa"
  [M_mr]="checkpoints/uk/specialists/mr"
)
for name in base_qwen35_2b official_only external_enhanced M_lang M_mt M_edit M_qa M_mr; do
  out="results/triage/raw_predictions/uk_${name}.jsonl"
  python3 scripts/dump_raw_predictions.py --config configs/eval/uk.yaml --model "${MODELS[$name]}" --per-task 20 --output "$out"
  python3 scripts/diagnose_prediction_dump.py --input "$out"
done
'
