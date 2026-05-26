#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=stage_b_rescue_cleanup
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/stage_b_rescue/cleanup "$SCRATCH_ROOT"/results/stage_b_rescue "$SCRATCH_ROOT"/checkpoints/stage_b_rescue/sorbian

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  echo "config=stage_b_rescue_cleanup"
  test -d "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
  BEFORE=$(du -sh "$SCRATCH_ROOT/checkpoints" | cut -f1)
  DELETED=""
  if [ -d "$SCRATCH_ROOT/checkpoints/competitive_reboot/uk" ] && [ -z "$(find "$SCRATCH_ROOT/checkpoints/competitive_reboot/uk" -mindepth 1 -print -quit)" ]; then
    rmdir "$SCRATCH_ROOT/checkpoints/competitive_reboot/uk"
    DELETED="$SCRATCH_ROOT/checkpoints/competitive_reboot/uk"
  fi
  AFTER=$(du -sh "$SCRATCH_ROOT/checkpoints" | cut -f1)
  {
    echo "timestamp=$(date -u +%Y%m%dT%H%M%SZ)"
    echo "git_commit=$(cat REVISION 2>/dev/null || git rev-parse HEAD)"
    echo "checkpoint_storage_before=$BEFORE"
    echo "checkpoint_storage_after=$AFTER"
    echo "preserved=$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
    echo "deleted=$DELETED"
  } | tee results/stage_b_rescue/cleanup/andromeda_cleanup_manifest_${SLURM_JOB_ID:-local}.txt
  cp results/stage_b_rescue/cleanup/andromeda_cleanup_manifest_${SLURM_JOB_ID:-local}.txt "$SCRATCH_ROOT/results/stage_b_rescue/"
'
