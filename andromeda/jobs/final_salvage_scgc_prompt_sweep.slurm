#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=final_salvage_scgc_prompt_sweep
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable. Never use V100 for this full-model eval.

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
export MODEL="${MODEL:-$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/prompt_sweep results/final_salvage/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$MODEL"
  sha256sum configs/prompts/final_salvage_scgc.yaml configs/eval/final_salvage_scgc_probe.yaml | tee results/final_salvage/status/prompt_sweep_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/final_salvage_scgc_prompt_sweep.py --model "$MODEL"
'
