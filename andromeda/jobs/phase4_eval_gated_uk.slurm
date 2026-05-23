#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=phase4_eval_gated_uk
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/wmt26_lrllm}"
cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{checkpoints,logs,results,tmp} results/phase4/gated_eval
andromeda/scripts/run_step.sh bash -lc 'python3 scripts/phase4_record_job_metadata.py --job-name phase4_eval_gated_uk --output results/phase4/status/phase4_eval_gated_uk_${SLURM_JOB_ID:-local}.json --path results/phase4/gates/uk_no_harm_report.json --result-path results/phase4/gated_eval && python3 scripts/phase4_eval_gated_candidates.py --track uk --candidates results/phase4/gates/uk_no_harm_report.json'
