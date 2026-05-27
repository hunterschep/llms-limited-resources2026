#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=final_salvage_00_status
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  squeue -u "$USER" -o "%i|%j|%T|%M|%R" | tee results/final_salvage/status/queue_${SLURM_JOB_ID:-local}.txt
  du -sh "$SCRATCH_ROOT"/checkpoints/lineage_recovery "$SCRATCH_ROOT"/checkpoints/final_salvage "$PROJECT_ROOT"/results/final_salvage 2>/dev/null | tee results/final_salvage/status/storage_${SLURM_JOB_ID:-local}.txt || true
'
