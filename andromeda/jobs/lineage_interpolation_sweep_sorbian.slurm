#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=medium
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=192G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=lineage_interpolation_sweep_sorbian
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable. Do not use V100.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/interpolation results/lineage_recovery/status "$SCRATCH_ROOT"/checkpoints/lineage_recovery/sorbian/interpolation

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  test -d "$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/stage_a_dapt_parent/final_merged"
  test -d "$SCRATCH_ROOT/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_merged"
  sha256sum configs/merge/lineage_sorbian_interpolation.yaml configs/eval/lineage_sorbian_probe.yaml | tee results/lineage_recovery/status/interpolation_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/lineage_interpolate_models.py --execute --delete-failed
'
