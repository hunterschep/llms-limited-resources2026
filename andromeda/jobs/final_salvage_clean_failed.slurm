#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=final_salvage_clean_failed
#SBATCH --output=/home/%u/logs/final_salvage-%x-%j.out
#SBATCH --error=/home/%u/logs/final_salvage-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/final_salvage/cleanup

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  TS=$(date -u +%Y%m%dT%H%M%SZ)
  MAN=results/final_salvage/cleanup/final_cleanup_manifest_${TS}.txt
  BEFORE=$(du -sh "$SCRATCH_ROOT"/checkpoints/final_salvage 2>/dev/null | awk "{print \$1}" || true)
  {
    echo "timestamp_utc=$TS"
    echo "storage_before=$BEFORE"
    echo "preserved selected lineage merge and package roots"
  } > "$MAN"
  AFTER=$(du -sh "$SCRATCH_ROOT"/checkpoints/final_salvage 2>/dev/null | awk "{print \$1}" || true)
  echo "storage_after=$AFTER" >> "$MAN"
  cat "$MAN"
'
