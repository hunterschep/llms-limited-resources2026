#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=competitive_00_status
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{checkpoints/competitive_reboot,results/competitive_reboot,logs/competitive_reboot,tmp} results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  (cat REVISION 2>/dev/null || git rev-parse HEAD 2>/dev/null || echo unknown) | tee results/competitive_reboot/status/git_commit_${SLURM_JOB_ID:-local}.txt
  squeue -u "$USER" || true
  du -sh "$SCRATCH_ROOT"/checkpoints "$SCRATCH_ROOT"/results "$PROJECT_ROOT"/results || true
  find "$SCRATCH_ROOT"/checkpoints -maxdepth 3 -type d | sort | tee results/competitive_reboot/status/checkpoint_dirs_${SLURM_JOB_ID:-local}.txt
'
