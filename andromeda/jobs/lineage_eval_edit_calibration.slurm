#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=lineage_eval_edit_calibration
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/probe_eval results/lineage_recovery/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/edit_calibration_tiny/final_merged"
  python3 scripts/competitive_eval.py --config configs/eval/lineage_sorbian_probe.yaml --model "$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/edit_calibration_tiny/final_merged" --output results/lineage_recovery/probe_eval/edit_calibration_tiny.json --raw-output results/lineage_recovery/probe_eval/edit_calibration_tiny_raw.jsonl
'
