#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=160G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=stage_b_edit_repair_sorbian
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable. Never use V100 for this training.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/checkpoints/stage_b_rescue/sorbian results/stage_b_rescue/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
  test -s data/processed/stage_b_rescue/sorbian/edit_repair.jsonl
  test -s data/processed/stage_b_rescue/sorbian/format_repair.jsonl
  test -s data/processed/stage_b_rescue/sorbian/mt_anchor.jsonl
  ! grep -R "stage_c_instruction_replay\\|checkpoints/phase[34]" configs/train/stage_b_rescue/sorbian_edit_repair_tiny.yaml
  sha256sum configs/train/stage_b_rescue/sorbian_edit_repair_tiny.yaml data/manifests/stage_b_repair_sorbian.json configs/eval/stage_b_rescue_probe_sorbian.yaml | tee results/stage_b_rescue/status/edit_repair_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/train_stage_b_repair.py --config configs/train/stage_b_rescue/sorbian_edit_repair_tiny.yaml
'
