#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --job-name=competitive_01_download_data
#SBATCH --output=/home/%u/logs/competitive_reboot-%x-%j.out
#SBATCH --error=/home/%u/logs/competitive_reboot-%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WMT26_RAW_ROOT="${WMT26_RAW_ROOT:-${SCRATCH_ROOT}/data/external/raw}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/results/competitive_reboot "$WMT26_RAW_ROOT" results/competitive_reboot/status

andromeda/scripts/run_step.sh bash -lc '
  set -euo pipefail
  echo "WMT26_RAW_ROOT=${WMT26_RAW_ROOT}"
  ! grep -R "checkpoints/phase[34]\\|results/phase[34]" configs/train/competitive configs/merge/competitive_*.yaml
  sha256sum configs/data/competitive_sources_uk.yaml configs/data/competitive_sources_sorbian.yaml data/manifests/data_governance_registry.csv | tee results/competitive_reboot/status/download_checksums_${SLURM_JOB_ID:-local}.txt
  python3 scripts/competitive_download_data.py --execute
'
