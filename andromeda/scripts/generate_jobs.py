#!/usr/bin/env python3
from __future__ import annotations

import shlex
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JOBS = ROOT / "andromeda/jobs"

COMMON = """#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition={partition}
#SBATCH --time={time}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={cpus}
#SBATCH --mem={mem}
{gres_line}#SBATCH --job-name={name}
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${{PROJECT_SLUG:-wmt26_lrllm}}"
export PROJECT_ROOT="${{PROJECT_ROOT:-/home/${{USER}}/workspace/projects/wmt26_lrllm}}"
export SCRATCH_ROOT="${{SCRATCH_ROOT:-/scratch/${{USER}}/projects/${{PROJECT_SLUG}}}}"
export WANDB_MODE="${{WANDB_MODE:-offline}}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{{data,checkpoints,logs,results,tmp}}

# GPU preference for this project: h200 first, then a100, then l40s.
# If an h200 job waits too long, resubmit with:
#   sbatch --gres=gpu:a100:1 this_job.slurm
#   sbatch --gres=gpu:l40s:1 this_job.slurm

andromeda/scripts/run_step.sh {command}
"""


def write_job(name: str, command: str, gpu: bool = True, partition: str = "short", time: str = "12:00:00", cpus: int = 8, mem: str = "64G") -> None:
    gres_line = "#SBATCH --gres=gpu:h200:1\n" if gpu else ""
    wrapped_command = f"bash -lc {shlex.quote(command)}"
    text = COMMON.format(name=name, command=wrapped_command, gres_line=gres_line, partition=partition, time=time, cpus=cpus, mem=mem)
    path = JOBS / f"{name}.slurm"
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)


def main() -> None:
    JOBS.mkdir(parents=True, exist_ok=True)
    write_job("00_validate_env", "bash andromeda/scripts/andromeda_probe.sh", gpu=False, cpus=2, mem="8G")
    write_job("01_prepare_data", "make validate inspect-data prepare-data smoke-test", gpu=False, cpus=4, mem="32G")
    write_job("02_download_external_data", "python3 scripts/download_external_data.py --execute", gpu=False, cpus=2, mem="16G")
    write_job("03_filter_external_data", "python3 scripts/filter_external_data.py && python3 scripts/deduplicate_external_data.py && python3 scripts/check_dev_overlap.py", gpu=False, cpus=4, mem="32G")
    write_job("04_compile_external_data", "python3 scripts/build_external_training_sets.py", gpu=False, cpus=4, mem="32G")
    write_job("05_report_data_quality", "python3 scripts/report_external_data_quality.py", gpu=False, cpus=2, mem="8G")

    for track, prefix in [("uk", "uk"), ("sorbian", "sorbian")]:
        write_job(f"train_{prefix}_baselines", f"python3 scripts/train_sft.py --config configs/train/{track}/external_enhanced_multitask.yaml", partition="medium", time="2-00:00:00", mem="96G")
        for specialist, config_name in [
            ("lang", "lang"),
            ("mt", "mt"),
            ("edit", "edit_scgc"),
            ("qa", "qa"),
            ("mr", "mr"),
            ("format", "format"),
        ]:
            write_job(f"train_{prefix}_{specialist}", f"python3 scripts/train_qlora.py --config configs/train/{track}/{config_name}.yaml", partition="medium", time="2-00:00:00", mem="96G")
        write_job(f"merge_{prefix}", f"python3 scripts/search_merge_weights.py --config configs/merge/{prefix}.yaml --limit 64", gpu=False, cpus=4, mem="32G")
        write_job(f"polish_{prefix}", f"python3 scripts/train_format_polish.py --config configs/train/{track}/final_polish.yaml", partition="short", time="12:00:00", mem="96G")
        write_job(f"eval_{prefix}_final", f"python3 scripts/eval_model.py --config configs/eval/{prefix}.yaml --model checkpoints/{prefix}/final_polished --output results/{prefix}_final_eval.json", partition="short", time="12:00:00", mem="96G")

    write_job(
        "train_uk_all",
        "python3 scripts/train_qlora.py --config configs/train/uk/lang.yaml && python3 scripts/train_qlora.py --config configs/train/uk/mt.yaml && python3 scripts/train_qlora.py --config configs/train/uk/edit_scgc.yaml && python3 scripts/train_qlora.py --config configs/train/uk/qa.yaml && python3 scripts/train_qlora.py --config configs/train/uk/mr.yaml && python3 scripts/train_qlora.py --config configs/train/uk/format.yaml && python3 scripts/search_merge_weights.py --config configs/merge/uk.yaml --limit 64 && python3 scripts/train_format_polish.py --config configs/train/uk/final_polish.yaml",
        partition="long",
        time="5-00:00:00",
        mem="128G",
    )
    write_job(
        "train_sorbian_all",
        "python3 scripts/train_qlora.py --config configs/train/sorbian/lang.yaml && python3 scripts/train_qlora.py --config configs/train/sorbian/mt.yaml && python3 scripts/train_qlora.py --config configs/train/sorbian/edit_scgc.yaml && python3 scripts/train_qlora.py --config configs/train/sorbian/qa.yaml && python3 scripts/train_qlora.py --config configs/train/sorbian/mr.yaml && python3 scripts/train_qlora.py --config configs/train/sorbian/format.yaml && python3 scripts/search_merge_weights.py --config configs/merge/sorbian.yaml --limit 64 && python3 scripts/train_format_polish.py --config configs/train/sorbian/final_polish.yaml",
        partition="long",
        time="5-00:00:00",
        mem="128G",
    )
    print(f"Wrote Slurm jobs to {JOBS}")


if __name__ == "__main__":
    main()
