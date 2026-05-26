#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=160G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=lineage_train_mr_recovery
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable. Do not use V100.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/status "$SCRATCH_ROOT"/checkpoints/lineage_recovery/sorbian

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_merged"
  python3 scripts/validate_data_governance.py
  python3 scripts/check_dev_overlap.py
  ! grep -R "stage_c_instruction_replay\\|checkpoints/phase[34]" configs/train/lineage_recovery/sorbian_mr_recovery_tiny.yaml
  sha256sum configs/train/lineage_recovery/sorbian_mr_recovery_tiny.yaml configs/data/mr_recovery_sorbian.yaml data/manifests/lineage_mr_recovery_sorbian.json configs/eval/lineage_sorbian_probe.yaml | tee results/lineage_recovery/status/mr_train_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/train_mr_recovery.py
'
