#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=lineage_00_status
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/status "$SCRATCH_ROOT"/results/lineage_recovery

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  echo "git_commit=$(cat REVISION 2>/dev/null || git rev-parse HEAD)"
  squeue -u "$USER" -o "%i|%j|%P|%t|%M|%l|%D|%C|%m|%b|%R" | tee results/lineage_recovery/status/squeue_${SLURM_JOB_ID:-local}.txt
  acct-chk "$USER" | tee results/lineage_recovery/status/storage_${SLURM_JOB_ID:-local}.txt
  du -sh "$SCRATCH_ROOT"/checkpoints "$SCRATCH_ROOT"/results /home/"$USER"/workspace/projects/wmt26_lrllm/results 2>/dev/null | tee -a results/lineage_recovery/status/storage_${SLURM_JOB_ID:-local}.txt
  python3 scripts/run_lineage_recovery.py status
'
