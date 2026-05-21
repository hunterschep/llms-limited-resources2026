#!/usr/bin/env bash
set -euo pipefail

module load miniconda/3 2>/dev/null || true
module load cuda/12.4.1_gcc11.4.1-fq5rwhn 2>/dev/null || true

ENV_NAME="${ENV_NAME:-wmt26-lrllm}"
if command -v conda >/dev/null 2>&1; then
  conda create -y -n "${ENV_NAME}" python=3.11
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate "${ENV_NAME}"
else
  python3 -m venv "${HOME}/.venvs/${ENV_NAME}"
  # shellcheck disable=SC1091
  source "${HOME}/.venvs/${ENV_NAME}/bin/activate"
fi

python -m pip install --upgrade pip wheel setuptools
python -m pip install torch transformers accelerate peft bitsandbytes datasets pyyaml scikit-learn sacrebleu sentencepiece protobuf wandb tensorboard
python -m pip install -e .
