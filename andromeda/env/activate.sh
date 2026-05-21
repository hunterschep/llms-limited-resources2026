#!/usr/bin/env bash
set -euo pipefail

module load miniconda/3 2>/dev/null || true
module load cuda/12.4.1_gcc11.4.1-fq5rwhn 2>/dev/null || true

ENV_NAME="${ENV_NAME:-wmt26-lrllm}"
if command -v conda >/dev/null 2>&1; then
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate "${ENV_NAME}"
else
  # shellcheck disable=SC1091
  source "${HOME}/.venvs/${ENV_NAME}/bin/activate"
fi

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export HF_HOME="${HF_HOME:-/scratch/${USER}/.cache/huggingface}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-${HF_HOME}/transformers}"
export HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-${HF_HOME}/datasets}"
export WANDB_MODE="${WANDB_MODE:-offline}"
export TOKENIZERS_PARALLELISM=false

mkdir -p "${SCRATCH_ROOT}"/{data,checkpoints,logs,results,tmp} "${HF_HOME}" "${PROJECT_ROOT}"/andromeda/logs
