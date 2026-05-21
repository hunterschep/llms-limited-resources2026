#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <command...>" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${PROJECT_ROOT:-$REPO_ROOT}" 2>/dev/null || cd "$REPO_ROOT"

source andromeda/env/activate.sh

echo "timestamp=$(date --iso-8601=seconds)"
echo "hostname=$(hostname)"
echo "user=$USER"
echo "workdir=$(pwd)"
echo "git_commit=$(git rev-parse HEAD 2>/dev/null || echo unknown)"
echo "scratch=${SCRATCH_ROOT}"
nvidia-smi || true

python3 scripts/validate_data_governance.py

exec "$@"
