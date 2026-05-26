#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --job-name=competitive_cleanup_failed
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p results/competitive_reboot/cleanup

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  before=$(du -sh "$SCRATCH_ROOT/checkpoints" 2>/dev/null || true)
  find "$SCRATCH_ROOT/checkpoints/competitive_reboot" -type d \( -name "checkpoint-*" -o -name "*dry_run*" \) -print | tee results/competitive_reboot/cleanup/remote_failed_candidates_${SLURM_JOB_ID:-local}.txt
  after=$(du -sh "$SCRATCH_ROOT/checkpoints" 2>/dev/null || true)
  printf "before=%s\nafter=%s\n" "$before" "$after" | tee results/competitive_reboot/cleanup/remote_cleanup_storage_${SLURM_JOB_ID:-local}.txt
'
