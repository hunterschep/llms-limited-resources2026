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


def write_create_env_job() -> None:
    text = """#!/usr/bin/env bash
#SBATCH --account=prudlab
#SBATCH --partition=short
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --job-name=00_create_env
#SBATCH --output=/home/%u/logs/%x-%j.out
#SBATCH --error=/home/%u/logs/%x-%j.err

set -euo pipefail

export PROJECT_SLUG="${PROJECT_SLUG:-wmt26_lrllm}"
export PROJECT_ROOT="${PROJECT_ROOT:-/home/${USER}/workspace/projects/wmt26_lrllm}"
export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/${USER}/projects/${PROJECT_SLUG}}"
export WANDB_MODE="${WANDB_MODE:-offline}"

cd "$PROJECT_ROOT"
mkdir -p /home/"$USER"/logs "$SCRATCH_ROOT"/{data,checkpoints,logs,results,tmp}

bash andromeda/env/create_env.sh
"""
    path = JOBS / "00_create_env.slurm"
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)


def main() -> None:
    JOBS.mkdir(parents=True, exist_ok=True)
    write_create_env_job()
    write_job("00_validate_env", "bash andromeda/scripts/andromeda_probe.sh", gpu=False, cpus=2, mem="8G")
    write_job("00_validate_gpu_env", "bash andromeda/scripts/validate_gpu_env.sh", gpu=True, cpus=4, mem="32G")
    write_job("01_prepare_data", "make validate inspect-data prepare-data smoke-test", gpu=False, cpus=4, mem="32G")
    write_job("02_download_external_data", "python3 scripts/download_external_data.py --execute", gpu=False, cpus=2, mem="16G")
    write_job("03_filter_external_data", "python3 scripts/filter_external_data.py && python3 scripts/deduplicate_external_data.py && python3 scripts/check_dev_overlap.py", gpu=False, cpus=4, mem="32G")
    write_job("04_compile_external_data", "python3 scripts/build_external_training_sets.py", gpu=False, cpus=4, mem="32G")
    write_job("05_report_data_quality", "python3 scripts/report_external_data_quality.py", gpu=False, cpus=2, mem="8G")
    write_job(
        "phase3_remediation_cleanup",
        "mkdir -p results/cleanup && TS=$(date -u +%Y%m%dT%H%M%SZ) && "
        "MAN=results/cleanup/phase3_cleanup_manifest_${TS}.txt && "
        "SUMMARY=results/cleanup/phase3_cleanup_summary_${TS}.md && "
        "echo \"# Phase 3 remediation cleanup ${TS}\" > \"$MAN\" && "
        "echo \"git_before=$(git rev-parse HEAD)\" >> \"$MAN\" && "
        "echo \"queue_before\" >> \"$MAN\" && squeue -u \"$USER\" >> \"$MAN\" && "
        "echo \"storage_before\" >> \"$MAN\" && du -sh \"$SCRATCH_ROOT\" /home/$USER/logs results 2>/dev/null >> \"$MAN\" || true && "
        "rm -rf \"$SCRATCH_ROOT/checkpoints/uk/baselines\" \"$SCRATCH_ROOT/checkpoints/uk/specialists\" "
        "\"$SCRATCH_ROOT/checkpoints/sorbian/baselines\" \"$SCRATCH_ROOT/checkpoints/sorbian/specialists\" "
        "\"$SCRATCH_ROOT/checkpoints/phase3_invalid\" results/uk results/sorbian results/merge_search && "
        "find scripts src -type d -name __pycache__ -prune -exec rm -rf {} + && "
        "find /home/$USER/logs -maxdepth 1 -type f \\( -name 'train_uk_*24615*' -o -name 'train_sorbian_*24615*' -o -name 'eval_uk_*24615*' -o -name 'eval_sorbian_*24615*' \\) -delete && "
        "echo \"storage_after\" >> \"$MAN\" && du -sh \"$SCRATCH_ROOT\" /home/$USER/logs results 2>/dev/null >> \"$MAN\" || true && "
        "printf '# Phase 3 Cleanup Summary\\n\\nManifest: `%s`\\n' \"$MAN\" > \"$SUMMARY\" && "
        "echo \"$MAN\"",
        gpu=False,
        partition="short",
        time="01:00:00",
        cpus=2,
        mem="8G",
    )
    write_job("phase3_triage_oracle", "make triage-oracle", gpu=False, cpus=2, mem="8G")
    write_job("phase3_triage_data_sanity", "make triage-data-sanity report-edit-data-balance report-mr-data-quality report-phase3-sanity", gpu=False, cpus=2, mem="8G")
    write_job(
        "phase3_triage_raw_predictions_uk",
        "python3 scripts/triage_raw_predictions.py --config configs/eval/uk.yaml --model Qwen/Qwen3.5-2B --per-task 10 --output results/triage/raw_predictions/phase3_fixed_uk_base.jsonl && "
        "python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/phase3_fixed_uk_base.jsonl && "
        "python3 scripts/report_scgc_confusion.py --input results/triage/raw_predictions/phase3_fixed_uk_base.jsonl && "
        "python3 scripts/report_mr_raw_errors.py --input results/triage/raw_predictions/phase3_fixed_uk_base.jsonl",
        partition="short",
        time="12:00:00",
        mem="96G",
    )
    write_job(
        "phase3_triage_raw_predictions_sorbian",
        "python3 scripts/triage_raw_predictions.py --config configs/eval/sorbian.yaml --model Qwen/Qwen3.5-2B --per-task 5 --output results/triage/raw_predictions/phase3_fixed_sorbian_base.jsonl && "
        "python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/phase3_fixed_sorbian_base.jsonl && "
        "python3 scripts/report_scgc_confusion.py --input results/triage/raw_predictions/phase3_fixed_sorbian_base.jsonl && "
        "python3 scripts/report_mr_raw_errors.py --input results/triage/raw_predictions/phase3_fixed_sorbian_base.jsonl",
        partition="short",
        time="12:00:00",
        mem="96G",
    )
    write_job(
        "phase3_triage_overfit_uk",
        "python3 scripts/triage_single_task_overfit.py --track uk --task SC --examples 20 --steps 60 --execute && "
        "python3 scripts/triage_single_task_overfit.py --track uk --task GC --examples 20 --steps 60 --execute && "
        "python3 scripts/triage_single_task_overfit.py --track uk --task MR --examples 20 --steps 60 --execute",
        partition="short",
        time="12:00:00",
        mem="96G",
    )
    write_job(
        "phase3_triage_overfit_sorbian",
        "python3 scripts/triage_single_task_overfit.py --track sorbian --task SC --examples 20 --steps 60 --execute && "
        "python3 scripts/triage_single_task_overfit.py --track sorbian --task GC --examples 20 --steps 60 --execute && "
        "python3 scripts/triage_single_task_overfit.py --track sorbian --task MR --examples 20 --steps 60 --execute",
        partition="short",
        time="12:00:00",
        mem="96G",
    )
    write_job(
        "phase3_check_checkpoint_loading",
        "python3 scripts/check_checkpoint_loading.py --config configs/eval/uk.yaml --checkpoint checkpoints/phase3_fixed/uk/edit --tasks SC GC --per-task 5 --output results/triage/checkpoint_loading/phase3_fixed_uk_edit.jsonl && "
        "python3 scripts/check_checkpoint_loading.py --config configs/eval/uk.yaml --checkpoint checkpoints/phase3_fixed/uk/mr --tasks MR --per-task 5 --output results/triage/checkpoint_loading/phase3_fixed_uk_mr.jsonl && "
        "python3 scripts/check_checkpoint_loading.py --config configs/eval/sorbian.yaml --checkpoint checkpoints/phase3_fixed/sorbian/edit --tasks SC GC --per-task 5 --output results/triage/checkpoint_loading/phase3_fixed_sorbian_edit.jsonl && "
        "python3 scripts/check_checkpoint_loading.py --config configs/eval/sorbian.yaml --checkpoint checkpoints/phase3_fixed/sorbian/mr --tasks MR --per-task 5 --output results/triage/checkpoint_loading/phase3_fixed_sorbian_mr.jsonl",
        partition="short",
        time="12:00:00",
        mem="96G",
    )

    fixed_train = {
        "uk_edit": "configs/train/uk/edit_scgc.yaml",
        "uk_mr": "configs/train/uk/mr.yaml",
        "uk_task_balanced": "configs/train/baseline_task_balanced_uk.yaml",
        "uk_external_enhanced": "configs/train/uk/external_enhanced_multitask.yaml",
        "sorbian_edit": "configs/train/sorbian/edit_scgc.yaml",
        "sorbian_mr": "configs/train/sorbian/mr.yaml",
        "sorbian_task_balanced": "configs/train/baseline_task_balanced_sorbian.yaml",
        "sorbian_external_enhanced": "configs/train/sorbian/external_enhanced_multitask.yaml",
    }
    for job_key, config_path in fixed_train.items():
        write_job(
            f"retrain_{job_key}_fixed",
            f"make check-governance check-overlap triage-oracle triage-data-sanity report-edit-data-balance report-mr-data-quality && "
            f"sha256sum data/manifests/final_training_data_summary.md {config_path} && "
            f"python3 scripts/train_sft.py --config {config_path}",
            partition="medium",
            time="2-00:00:00",
            mem="128G",
        )
    write_job(
        "eval_phase3_fixed_uk",
        "python3 scripts/eval_model.py --config configs/eval/uk.yaml --model Qwen/Qwen3.5-2B --output results/phase3_fixed/uk/base_qwen35_2b.json && "
        "python3 scripts/eval_model.py --config configs/eval/uk.yaml --model checkpoints/phase3_fixed/uk/edit --output results/phase3_fixed/uk/edit.json && "
        "python3 scripts/eval_model.py --config configs/eval/uk.yaml --model checkpoints/phase3_fixed/uk/mr --output results/phase3_fixed/uk/mr.json && "
        "python3 scripts/eval_model.py --config configs/eval/uk.yaml --model checkpoints/phase3_fixed/uk/task_balanced --output results/phase3_fixed/uk/task_balanced.json && "
        "python3 scripts/eval_model.py --config configs/eval/uk.yaml --model checkpoints/phase3_fixed/uk/external_enhanced --output results/phase3_fixed/uk/external_enhanced.json",
        partition="medium",
        time="2-00:00:00",
        mem="128G",
    )
    write_job(
        "eval_phase3_fixed_sorbian",
        "python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model Qwen/Qwen3.5-2B --output results/phase3_fixed/sorbian/base_qwen35_2b.json && "
        "python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/edit --output results/phase3_fixed/sorbian/edit.json && "
        "python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/mr --output results/phase3_fixed/sorbian/mr.json && "
        "python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/task_balanced --output results/phase3_fixed/sorbian/task_balanced.json && "
        "python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model checkpoints/phase3_fixed/sorbian/external_enhanced --output results/phase3_fixed/sorbian/external_enhanced.json",
        partition="medium",
        time="2-00:00:00",
        mem="128G",
    )
    write_job(
        "merge_phase3_fixed_uk",
        "python3 scripts/search_merge_weights.py --config configs/merge/uk.yaml --limit 4 --execute --eval-limit 256",
        partition="medium",
        time="2-00:00:00",
        mem="128G",
    )
    write_job(
        "merge_phase3_fixed_sorbian",
        "python3 scripts/search_merge_weights.py --config configs/merge/sorbian.yaml --limit 4 --execute --eval-limit 256",
        partition="medium",
        time="2-00:00:00",
        mem="128G",
    )
    write_job("polish_phase3_fixed_uk", "python3 scripts/train_format_polish.py --config configs/train/uk/final_polish.yaml", partition="medium", time="2-00:00:00", mem="96G")
    write_job("polish_phase3_fixed_sorbian", "python3 scripts/train_format_polish.py --config configs/train/sorbian/final_polish.yaml", partition="medium", time="2-00:00:00", mem="96G")

    baseline_configs = {
        "uk": [
            ("official_only", "configs/train/baseline_official_only_uk.yaml"),
            ("naive_multitask", "configs/train/baseline_naive_multitask_uk.yaml"),
            ("task_balanced", "configs/train/baseline_task_balanced_uk.yaml"),
            ("external_enhanced", "configs/train/uk/external_enhanced_multitask.yaml"),
        ],
        "sorbian": [
            ("official_only", "configs/train/baseline_official_only_sorbian.yaml"),
            ("naive_multitask", "configs/train/baseline_naive_multitask_sorbian.yaml"),
            ("task_balanced", "configs/train/baseline_task_balanced_sorbian.yaml"),
            ("external_enhanced", "configs/train/sorbian/external_enhanced_multitask.yaml"),
        ],
    }
    eval_baseline_models = {
        "uk": [
            ("official_only", "checkpoints/uk/baselines/official_only"),
            ("naive_multitask", "checkpoints/uk/baselines/naive_multitask"),
            ("task_balanced", "checkpoints/uk/baselines/task_balanced"),
            ("external_enhanced", "checkpoints/uk/baselines/external_enhanced_multitask"),
        ],
        "sorbian": [
            ("official_only", "checkpoints/sorbian/baselines/official_only"),
            ("naive_multitask", "checkpoints/sorbian/baselines/naive_multitask"),
            ("task_balanced", "checkpoints/sorbian/baselines/task_balanced"),
            ("external_enhanced", "checkpoints/sorbian/baselines/external_enhanced_multitask"),
        ],
    }
    specialist_models = {
        "uk": ["lang", "mt", "edit_scgc", "qa", "mr", "format"],
        "sorbian": ["lang", "mt", "edit_scgc", "qa", "mr", "format"],
    }

    for track, prefix in [("uk", "uk"), ("sorbian", "sorbian")]:
        write_job(
            f"eval_base_{prefix}",
            f"python3 scripts/eval_model.py --config configs/eval/{prefix}.yaml --model Qwen/Qwen3.5-2B --output results/baselines/base_qwen35_2b_{prefix}.json",
            partition="medium",
            time="2-00:00:00",
            mem="96G",
        )
        for baseline_name, config_path in baseline_configs[prefix]:
            write_job(f"train_{prefix}_baseline_{baseline_name}", f"python3 scripts/train_sft.py --config {config_path}", partition="medium", time="2-00:00:00", mem="96G")
        write_job(
            f"train_{prefix}_baselines",
            " && ".join(f"python3 scripts/train_sft.py --config {config_path}" for _, config_path in baseline_configs[prefix]),
            partition="medium",
            time="2-00:00:00",
            mem="128G",
        )
        write_job(
            f"eval_{prefix}_baselines",
            " && ".join(
                f"python3 scripts/eval_model.py --config configs/eval/{prefix}.yaml --model {model_path} --output results/{prefix}/baselines/{baseline_name}.json"
                for baseline_name, model_path in eval_baseline_models[prefix]
            ),
            partition="medium",
            time="2-00:00:00",
            mem="128G",
        )
        for specialist, config_name in [
            ("lang", "lang"),
            ("mt", "mt"),
            ("edit", "edit_scgc"),
            ("qa", "qa"),
            ("mr", "mr"),
            ("format", "format"),
        ]:
            write_job(f"train_{prefix}_{specialist}", f"python3 scripts/train_qlora.py --config configs/train/{track}/{config_name}.yaml", partition="medium", time="2-00:00:00", mem="96G")
        write_job(
            f"eval_{prefix}_specialists",
            " && ".join(
                f"python3 scripts/eval_model.py --config configs/eval/{prefix}.yaml --model checkpoints/{prefix}/specialists/{name} --output results/{prefix}/specialists/{name}.json"
                for name in specialist_models[prefix]
            ),
            partition="medium",
            time="2-00:00:00",
            mem="128G",
        )
        write_job(
            f"merge_{prefix}",
            f"python3 scripts/search_merge_weights.py --config configs/merge/{prefix}.yaml --limit 8 --execute --eval-limit 256",
            gpu=True,
            partition="medium",
            time="2-00:00:00",
            cpus=8,
            mem="128G",
        )
        write_job(f"polish_{prefix}", f"python3 scripts/train_format_polish.py --config configs/train/{track}/final_polish.yaml", partition="medium", time="2-00:00:00", mem="96G")
        write_job(f"eval_{prefix}_final", f"python3 scripts/eval_model.py --config configs/eval/{prefix}.yaml --model checkpoints/{prefix}/final_polished --output results/{prefix}_final_eval.json", partition="medium", time="2-00:00:00", mem="96G")

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
