#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=medium
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=192G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=lineage_sorbian_stage_b_mt
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. If unavailable, resubmit with --gres=gpu:a100:1 or --gres=gpu:l40s:1. Do not use V100.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/status "$SCRATCH_ROOT"/checkpoints/lineage_recovery/sorbian "$SCRATCH_ROOT"/results/lineage_recovery

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  ! grep -R "stage_c_instruction_replay\\|checkpoints/phase[34]\\|results/phase[34]" configs/train/lineage_recovery configs/merge/lineage_*.yaml
  python3 scripts/validate_data_governance.py
  python3 scripts/check_dev_overlap.py
  test -d "$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/stage_a_dapt_parent/final_merged"
  test -s data/processed/competitive/sorbian/stage_b_mt_large.jsonl
  sha256sum configs/train/lineage_recovery/sorbian_stage_b_mt_preserve.yaml data/processed/competitive/sorbian/stage_b_mt_large.jsonl data/manifests/competitive_mixture_sorbian.json data/manifests/data_governance_registry.csv configs/eval/lineage_sorbian_probe.yaml | tee results/lineage_recovery/status/stage_b_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/train_lineage_recovery.py --config configs/train/lineage_recovery/sorbian_stage_b_mt_preserve.yaml
  python3 scripts/lineage_record_checkpoint.py --config configs/train/lineage_recovery/sorbian_stage_b_mt_preserve.yaml --materialize-all
  python3 scripts/lineage_verify_checkpoint_tree.py --strict
'
