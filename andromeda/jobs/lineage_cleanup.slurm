#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=lineage_cleanup
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/cleanup "$SCRATCH_ROOT"/checkpoints/lineage_recovery "$SCRATCH_ROOT"/results/lineage_recovery

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  ts=$(date -u +%Y%m%dT%H%M%SZ)
  manifest="results/lineage_recovery/cleanup/andromeda_cleanup_manifest_${ts}.txt"
  {
    echo "timestamp=${ts}"
    echo "git_commit=$(cat REVISION 2>/dev/null || git rev-parse HEAD)"
    echo "storage_before"
    du -sh "$SCRATCH_ROOT"/checkpoints "$SCRATCH_ROOT"/results /home/"$USER"/workspace/projects/wmt26_lrllm/results 2>/dev/null || true
    echo "preserved"
    echo "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large"
    echo "$SCRATCH_ROOT/checkpoints/stage_b_rescue/sorbian/edit_repair_tiny"
    echo "deleted"
    find "$SCRATCH_ROOT/checkpoints/lineage_recovery" -maxdepth 3 -type d -empty -print -delete 2>/dev/null || true
    echo "storage_after"
    du -sh "$SCRATCH_ROOT"/checkpoints "$SCRATCH_ROOT"/results /home/"$USER"/workspace/projects/wmt26_lrllm/results 2>/dev/null || true
  } | tee "$manifest"
  python3 scripts/run_lineage_recovery.py cleanup
'
