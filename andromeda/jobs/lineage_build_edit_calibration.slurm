#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --job-name=lineage_build_edit_calibration
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  python3 scripts/validate_data_governance.py
  python3 scripts/check_dev_overlap.py
  ! grep -R "stage_c_instruction_replay" configs/data/edit_calibration_sorbian.yaml configs/train/lineage_recovery/sorbian_edit_calibration_tiny.yaml
  sha256sum configs/data/edit_calibration_sorbian.yaml configs/data/stage_b_repair_sorbian.yaml data/manifests/data_governance_registry.csv | tee results/lineage_recovery/status/edit_calibration_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/build_edit_calibration_set.py
'
