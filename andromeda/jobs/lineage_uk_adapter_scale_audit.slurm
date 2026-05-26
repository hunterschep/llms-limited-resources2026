#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --job-name=lineage_uk_adapter_scale_audit
#SBATCH --output=/home/%u/logs/lineage_recovery-%x-%j.out
#SBATCH --error=/home/%u/logs/lineage_recovery-%x-%j.err

set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs results/lineage_recovery/status
andromeda/scripts/run_step.sh bash -lc 'python3 - <<'"'"'PY'"'"'
from pathlib import Path
out = Path("results/lineage_recovery/status/ukrainian_lineage_audit.txt")
out.write_text("Ukrainian remains frozen for lineage recovery; no full Ukrainian training launched. Prompt-only remains fallback unless a cheap adapter lineage audit is explicitly requested.\\n", encoding="utf-8")
print(out)
PY'
