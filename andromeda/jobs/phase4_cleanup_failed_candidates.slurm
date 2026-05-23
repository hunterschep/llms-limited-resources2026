#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --job-name=phase4_cleanup_failed
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/phase4/cleanup
andromeda/scripts/run_step.sh bash -lc 'python3 scripts/phase4_record_job_metadata.py --job-name phase4_cleanup_failed --output results/phase4/status/phase4_cleanup_failed_${SLURM_JOB_ID:-local}.json --path results/phase4/gates/uk_no_harm_report.json --path results/phase4/gates/sorbian_no_harm_report.json --result-path results/phase4/cleanup && python3 scripts/phase4_cleanup_failed.py --dry-run --output results/phase4/cleanup/phase4_cleanup_failed_dryrun.json'
