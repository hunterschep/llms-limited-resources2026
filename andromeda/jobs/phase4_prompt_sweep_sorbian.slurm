#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=phase4_prompt_sweep_sorbian
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{checkpoints,logs,results,tmp} results/phase4/{probe,prompt_sweep/status}

# GPU preference: H200 first, A100 fallback, L40S fallback.
# Fallback examples:
#   sbatch --gres=gpu:a100:1 andromeda/jobs/phase4_prompt_sweep_sorbian.slurm
#   sbatch --gres=gpu:l40s:1 andromeda/jobs/phase4_prompt_sweep_sorbian.slurm

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  make check-governance check-overlap phase4-build-probe
  sha256sum configs/eval/phase4_probe_sorbian.yaml configs/prompts/phase4_sweep.yaml data/manifests/final_training_data_summary.md
  WMT26_RECORD_RUNS=0 python3 scripts/eval_phase4_probe.py --config configs/eval/phase4_probe_sorbian.yaml --model Qwen/Qwen3.5-2B --output results/phase4/probe/baseline_prompt_only_sorbian.json
  WMT26_RECORD_RUNS=0 python3 scripts/phase4_prompt_sweep.py --config configs/eval/phase4_prompt_sweep_sorbian.yaml
'
