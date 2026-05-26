#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:45:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=stage_b_clean_failed
#SBATCH --output=/home/%u/logs/stage_b_rescue-%x-%j.out
#SBATCH --error=/home/%u/logs/stage_b_rescue-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/stage_b_rescue/cleanup "$SCRATCH_ROOT"/results/stage_b_rescue

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  BEFORE=$(du -sh "$SCRATCH_ROOT/checkpoints/stage_b_rescue" 2>/dev/null | cut -f1 || echo 0)
  find "$SCRATCH_ROOT/checkpoints/stage_b_rescue" -type d -name "checkpoint-*" -prune -print -exec rm -rf {} + 2>/dev/null | tee results/stage_b_rescue/cleanup/failed_checkpoint_prune_${SLURM_JOB_ID:-local}.txt || true
  AFTER=$(du -sh "$SCRATCH_ROOT/checkpoints/stage_b_rescue" 2>/dev/null | cut -f1 || echo 0)
  echo "before=$BEFORE after=$AFTER" | tee -a results/stage_b_rescue/cleanup/failed_checkpoint_prune_${SLURM_JOB_ID:-local}.txt
'
