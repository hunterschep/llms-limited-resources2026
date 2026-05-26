#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=competitive_uk_eval_stages
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable for evaluation.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/competitive_reboot/eval/uk results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/eval/uk.yaml data/manifests/competitive_mixture_uk.json | tee results/competitive_reboot/status/uk_eval_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/competitive_eval.py --config configs/eval/uk.yaml --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/uk/stage_a_mt_real_large" --output results/competitive_reboot/eval/uk/stage_a_mt_real_large.json --raw-output results/competitive_reboot/eval/uk/stage_a_mt_real_large_raw.jsonl
  python3 scripts/competitive_eval.py --config configs/eval/uk.yaml --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/uk/stage_b_instruction_replay" --output results/competitive_reboot/eval/uk/stage_b_instruction_replay.json --raw-output results/competitive_reboot/eval/uk/stage_b_instruction_replay_raw.jsonl
  python3 scripts/competitive_eval.py --config configs/eval/uk.yaml --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/uk/stage_c_doc_mt_format" --output results/competitive_reboot/eval/uk/stage_c_doc_mt_format.json --raw-output results/competitive_reboot/eval/uk/stage_c_doc_mt_format_raw.jsonl
'
