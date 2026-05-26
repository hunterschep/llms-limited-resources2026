#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --job-name=stage_b_merge_repairs_sorbian
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/stage_b_rescue/merge results/stage_b_rescue/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
  test "$(grep -R "stage_c_instruction_replay" configs/merge/stage_b_rescue/sorbian_repair_merge.yaml | grep -c "exclude")" -ge 1
  ! grep -R "checkpoints/phase[34]" configs/merge/stage_b_rescue
  sha256sum configs/merge/stage_b_rescue/sorbian_repair_merge.yaml | tee results/stage_b_rescue/status/merge_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/merge_stage_b_repair.py
'
