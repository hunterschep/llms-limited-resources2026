#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=long
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=192G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=competitive_sorbian_stagewise
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. If unavailable, resubmit with --gres=gpu:a100:1 or --gres=gpu:l40s:1.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/checkpoints/competitive_reboot/sorbian "$SCRATCH_ROOT"/results/competitive_reboot results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  ! grep -R "checkpoints/phase[34]\\|results/phase[34]" configs/train/competitive configs/merge/competitive_*.yaml
  test -s data/processed/competitive/sorbian/stage_a_dapt_large.jsonl
  test -s data/processed/competitive/sorbian/stage_b_mt_large.jsonl
  test -s data/processed/competitive/sorbian/stage_c_instruction_replay.jsonl
  sha256sum configs/train/competitive/sorbian_stagewise_tartu_style.yaml configs/train/competitive/sorbian_dapt_large.yaml configs/train/competitive/sorbian_mt_large.yaml configs/train/competitive/sorbian_instruction_replay.yaml data/manifests/competitive_mixture_sorbian.json configs/eval/sorbian.yaml | tee results/competitive_reboot/status/sorbian_stagewise_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/train_stagewise.py --config configs/train/competitive/sorbian_stagewise_tartu_style.yaml ${STAGEWISE_EXTRA_ARGS:-}
'
