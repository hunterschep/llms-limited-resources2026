#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=stage_b_prompt_sweep_sorbian
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. If unavailable, resubmit with --gres=gpu:a100:1 or --gres=gpu:l40s:1. Do not use V100.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/stage_b_rescue/prompt_sweep results/stage_b_rescue/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
  ! grep -R "stage_c_instruction_replay\\|checkpoints/phase[34]" configs/train/stage_b_rescue
  sha256sum configs/eval/stage_b_rescue_probe_sorbian.yaml configs/prompts/stage_b_rescue_sorbian.yaml data/manifests/stage_b_rescue_probe_sorbian.json | tee results/stage_b_rescue/status/prompt_sweep_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/stage_b_prompt_sweep.py --execute --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
'
