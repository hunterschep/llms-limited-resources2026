#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=phase3_remediation_cleanup
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{data,checkpoints,logs,results,tmp}

# GPU preference for this project: h200 first, then a100, then l40s.
# If an h200 job waits too long, resubmit with:
#   sbatch --gres=gpu:a100:1 this_job.slurm
#   sbatch --gres=gpu:l40s:1 this_job.slurm

andromeda/scripts/run_step.sh bash -lc 'mkdir -p results/cleanup && TS=$(date -u +%Y%m%dT%H%M%SZ) && MAN=results/cleanup/phase3_cleanup_manifest_${TS}.txt && SUMMARY=results/cleanup/phase3_cleanup_summary_${TS}.md && echo "# Phase 3 remediation cleanup ${TS}" > "$MAN" && echo "git_before=$(git rev-parse HEAD)" >> "$MAN" && echo "queue_before" >> "$MAN" && squeue -u "$USER" >> "$MAN" && echo "storage_before" >> "$MAN" && du -sh "$SCRATCH_ROOT" /home/$USER/logs results 2>/dev/null >> "$MAN" || true && rm -rf "$SCRATCH_ROOT/checkpoints/uk/baselines" "$SCRATCH_ROOT/checkpoints/uk/specialists" "$SCRATCH_ROOT/checkpoints/sorbian/baselines" "$SCRATCH_ROOT/checkpoints/sorbian/specialists" "$SCRATCH_ROOT/checkpoints/phase3_invalid" results/uk results/sorbian results/merge_search && find scripts src -type d -name __pycache__ -prune -exec rm -rf {} + && find /home/$USER/logs -maxdepth 1 -type f \( -name '"'"'train_uk_*24615*'"'"' -o -name '"'"'train_sorbian_*24615*'"'"' -o -name '"'"'eval_uk_*24615*'"'"' -o -name '"'"'eval_sorbian_*24615*'"'"' \) -delete && echo "storage_after" >> "$MAN" && du -sh "$SCRATCH_ROOT" /home/$USER/logs results 2>/dev/null >> "$MAN" || true && printf '"'"'# Phase 3 Cleanup Summary\n\nManifest: `%s`\n'"'"' "$MAN" > "$SUMMARY" && echo "$MAN"'
