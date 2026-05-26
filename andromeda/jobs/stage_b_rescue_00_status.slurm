#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=stage_b_rescue_status
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/stage_b_rescue/status "$SCRATCH_ROOT"/results/stage_b_rescue

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  echo "config=stage_b_rescue_status"
  echo "revision=$(cat REVISION 2>/dev/null || git rev-parse HEAD)"
  squeue -u "$USER" -o "%i|%j|%P|%t|%M|%l|%D|%C|%m|%b|%R" | tee results/stage_b_rescue/status/squeue_${SLURM_JOB_ID:-local}.txt
  du -sh "$SCRATCH_ROOT/checkpoints" "$SCRATCH_ROOT/results" results | tee results/stage_b_rescue/status/storage_${SLURM_JOB_ID:-local}.txt
  test -d "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
  python3 scripts/run_stage_b_rescue.py status
'
