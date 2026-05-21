#!/usr/bin/env bash
set -euo pipefail

module load miniconda/3 2>/dev/null || true
module load cuda/12.4.1_gcc11.4.1-fq5rwhn 2>/dev/null || true

ENV_NAME="${ENV_NAME:-wmt26-lrllm}"
if command -v conda >/dev/null 2>&1; then
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh"
  if ! conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
    conda create -y -n "${ENV_NAME}" python=3.11
  fi
  conda activate "${ENV_NAME}"
else
  if [[ ! -d "${HOME}/.venvs/${ENV_NAME}" ]]; then
    python3 -m venv "${HOME}/.venvs/${ENV_NAME}"
  fi
  # shellcheck disable=SC1091
  source "${HOME}/.venvs/${ENV_NAME}/bin/activate"
fi

python -m pip install --upgrade pip wheel setuptools

# Andromeda's current NVIDIA driver advertises CUDA 12.9. The default PyPI
# torch wheel may move ahead of that driver, which leaves torch.cuda unusable
# on GPU nodes. Pin a CUDA 12.8 build that is compatible with the cluster
# driver, then install the rest of the stack without letting pip replace it.
python -m pip install --upgrade --index-url https://download.pytorch.org/whl/cu128 torch==2.8.0
python -m pip install --upgrade transformers accelerate peft bitsandbytes datasets pyyaml scikit-learn sacrebleu sentencepiece protobuf wandb tensorboard "kernels>=0.11.1"
python -m pip install -e .

python - <<'PY'
import torch
print(f"torch={torch.__version__} torch_cuda={torch.version.cuda}")
PY
