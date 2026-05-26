#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:h200:1
#SBATCH --job-name=competitive_sorbian_eval_stages
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail
# GPU preference: H200 first. A100/L40S fallback acceptable for evaluation.

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/competitive_reboot/eval/sorbian results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  sha256sum configs/eval/sorbian.yaml data/manifests/competitive_mixture_sorbian.json | tee results/competitive_reboot/status/sorbian_eval_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/competitive_eval.py --config configs/eval/sorbian.yaml --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_a_dapt_large" --output results/competitive_reboot/eval/sorbian/stage_a_dapt_large.json --raw-output results/competitive_reboot/eval/sorbian/stage_a_dapt_large_raw.jsonl
  python3 scripts/competitive_eval.py --config configs/eval/sorbian.yaml --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_b_mt_large" --output results/competitive_reboot/eval/sorbian/stage_b_mt_large.json --raw-output results/competitive_reboot/eval/sorbian/stage_b_mt_large_raw.jsonl
  python3 scripts/competitive_eval.py --config configs/eval/sorbian.yaml --model "$SCRATCH_ROOT/checkpoints/competitive_reboot/sorbian/stage_c_instruction_replay" --output results/competitive_reboot/eval/sorbian/stage_c_instruction_replay.json --raw-output results/competitive_reboot/eval/sorbian/stage_c_instruction_replay_raw.jsonl
'
