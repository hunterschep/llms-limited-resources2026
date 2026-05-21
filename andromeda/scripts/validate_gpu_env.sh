#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import torch

print(f"torch={torch.__version__}")
print(f"torch_cuda={torch.version.cuda}")
print(f"cuda_available={torch.cuda.is_available()}")
if not torch.cuda.is_available():
    raise SystemExit("CUDA is not available to PyTorch on this GPU node.")

device = torch.device("cuda")
x = torch.ones((128, 128), device=device, dtype=torch.float32)
y = x @ x
torch.cuda.synchronize()
print(f"cuda_device={torch.cuda.get_device_name(0)}")
print(f"cuda_smoke_sum={float(y.sum().item())}")
PY
