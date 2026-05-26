#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wmt26.data.schema import validate_example
from wmt26.prompts.templates import render_messages


REQUIRED_PATHS = [
    "docs/01_wmt26_rules_summary.md",
    "docs/02_repo_data_inventory.md",
    "docs/03_data_governance_policy.md",
    "docs/04_local_validation_policy.md",
    "docs/05_canonical_data_format.md",
    "docs/06_eval_protocol.md",
    "docs/07_baseline_training_plan.md",
    "docs/08_external_data_plan.md",
    "docs/09_task_compilers.md",
    "docs/10_language_acquisition_curriculum.md",
    "docs/11_specialist_training.md",
    "docs/12_skill_vector_merging.md",
    "docs/13_format_polish.md",
    "docs/14_final_execution_plan.md",
    "docs/15_expected_ablation_table.md",
    "docs/16_public_data_acquisition_plan.md",
    "docs/17_data_source_risk_assessment.md",
    "docs/18_external_data_filtering.md",
    "docs/19_final_data_mixture.md",
    "docs/20_second_stage_training_readiness.md",
    "docs/21_data_ablation_plan.md",
    "docs/22_expected_second_stage_ablation_table.md",
    "docs/33_phase3_triage_remediation.md",
    "docs/34_phase3_triage_findings.md",
    "docs/35_phase3_remediation_retrain_plan.md",
    "docs/36_phase3_cleanup_policy.md",
    "docs/37_phase3_sanity_gates.md",
    "docs/38_edit_data_remediation.md",
    "docs/39_mr_remediation.md",
    "docs/40_phase3_fixed_results.md",
    "docs/41_phase3_retrain_error_analysis.md",
    "docs/42_phase3_resume_or_block_merge_decision.md",
    "README_WMT26_RUNBOOK.md",
    "data/manifests/official_data_inventory.jsonl",
    "data/manifests/data_governance_registry.csv",
    "data/manifests/data_governance_registry.schema.json",
    "data/manifests/local_split_manifest.jsonl",
    "data/manifests/external_data_inventory.jsonl",
    "data/manifests/external_data_filter_report.jsonl",
    "data/manifests/external_data_quality_report.md",
    "data/manifests/final_training_data_summary.md",
    "src/wmt26/data/schema.py",
    "src/wmt26/prompts/templates.py",
    "src/wmt26/compilers/common.py",
    "src/wmt26/train/config.py",
    "src/wmt26/eval/metrics.py",
    "scripts/inspect_repo_data.py",
    "scripts/validate_data_governance.py",
    "scripts/download_external_data.py",
    "scripts/filter_external_data.py",
    "scripts/deduplicate_external_data.py",
    "scripts/check_dev_overlap.py",
    "scripts/build_external_training_sets.py",
    "scripts/report_external_data_quality.py",
    "scripts/create_local_splits.py",
    "scripts/compile_mt_data.py",
    "scripts/compile_sc_data.py",
    "scripts/compile_gc_data.py",
    "scripts/compile_qa_data.py",
    "scripts/compile_mr_data.py",
    "scripts/train_sft.py",
    "scripts/eval_model.py",
    "scripts/triage_eval_oracle.py",
    "scripts/triage_oracle_eval.py",
    "scripts/triage_data_sanity.py",
    "scripts/dump_raw_predictions.py",
    "scripts/triage_raw_predictions.py",
    "scripts/diagnose_prediction_dump.py",
    "scripts/check_checkpoint_loading.py",
    "scripts/run_single_batch_overfit.py",
    "scripts/triage_single_task_overfit.py",
    "scripts/report_phase3_sanity.py",
    "scripts/report_edit_data_balance.py",
    "scripts/report_scgc_confusion.py",
    "scripts/report_mr_data_quality.py",
    "scripts/report_mr_raw_errors.py",
    "andromeda/jobs/triage_oracle.slurm",
    "andromeda/jobs/triage_raw_predictions_uk.slurm",
    "andromeda/jobs/triage_raw_predictions_sorbian.slurm",
    "andromeda/jobs/triage_checkpoint_loading_uk.slurm",
    "andromeda/jobs/triage_checkpoint_loading_sorbian.slurm",
    "andromeda/jobs/phase3_remediation_cleanup.slurm",
    "andromeda/jobs/phase3_triage_oracle.slurm",
    "andromeda/jobs/phase3_triage_data_sanity.slurm",
    "andromeda/jobs/phase3_triage_raw_predictions_uk.slurm",
    "andromeda/jobs/phase3_triage_raw_predictions_sorbian.slurm",
    "andromeda/jobs/phase3_triage_overfit_uk.slurm",
    "andromeda/jobs/phase3_triage_overfit_sorbian.slurm",
    "andromeda/jobs/phase3_check_checkpoint_loading.slurm",
    "andromeda/jobs/retrain_uk_edit_fixed.slurm",
    "andromeda/jobs/retrain_uk_mr_fixed.slurm",
    "andromeda/jobs/retrain_uk_task_balanced_fixed.slurm",
    "andromeda/jobs/retrain_uk_external_enhanced_fixed.slurm",
    "andromeda/jobs/retrain_sorbian_edit_fixed.slurm",
    "andromeda/jobs/retrain_sorbian_mr_fixed.slurm",
    "andromeda/jobs/retrain_sorbian_task_balanced_fixed.slurm",
    "andromeda/jobs/retrain_sorbian_external_enhanced_fixed.slurm",
    "andromeda/jobs/eval_phase3_fixed_uk.slurm",
    "andromeda/jobs/eval_phase3_fixed_sorbian.slurm",
    "andromeda/jobs/merge_phase3_fixed_uk.slurm",
    "andromeda/jobs/merge_phase3_fixed_sorbian.slurm",
    "andromeda/jobs/polish_phase3_fixed_uk.slurm",
    "andromeda/jobs/polish_phase3_fixed_sorbian.slurm",
    "scripts/merge_task_vectors.py",
    "scripts/build_format_preference_data.py",
    "Makefile",
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def check_paths() -> list[str]:
    missing = []
    for path in REQUIRED_PATHS:
        if (ROOT / path).exists():
            continue
        if path.startswith("docs/33_") or path.startswith("docs/34_") or path.startswith("docs/35_") or path.startswith("docs/36_") or path.startswith("docs/37_") or path.startswith("docs/38_") or path.startswith("docs/39_") or path.startswith("docs/40_") or path.startswith("docs/41_") or path.startswith("docs/42_"):
            archived = ROOT / "docs/archive_failed_phase3_phase4" / Path(path).name
            if archived.exists():
                continue
        missing.append(path)
    return missing


def check_yaml_configs() -> list[str]:
    errors = []
    for path in sorted((ROOT / "configs").glob("**/*.yaml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors


def check_prompt_templates() -> list[str]:
    errors = []
    try:
        render_messages(ROOT / "configs/prompts/mt.yaml", target="Тест", source_language_name="English", target_language_name="Ukrainian", input="Test")
        render_messages(ROOT / "configs/prompts/qa.yaml", target="0", question="Q?", options="0. A")
        render_messages(ROOT / "configs/prompts/sc.yaml", target="Wrong word: CORRECT\nCorrect word: CORRECT", input_sentence="Sentence.")
        render_messages(ROOT / "configs/prompts/gc.yaml", target="Wrong word: CORRECT\nCorrect word: CORRECT", input_sentence="Sentence.")
        render_messages(ROOT / "configs/prompts/mr.yaml", target="1", question="1+0?")
    except Exception as exc:
        errors.append(str(exc))
    return errors


def check_canonical_samples() -> list[str]:
    errors = []
    for path in sorted((ROOT / "data/processed").glob("**/*.jsonl")):
        if path.name == "format_preferences.jsonl" or "format_preferences" in path.name or path.name == "format_polish_final.jsonl":
            continue
        with path.open("r", encoding="utf-8") as handle:
            for idx, line in enumerate(handle):
                if idx >= 3:
                    break
                if not line.strip():
                    continue
                row = json.loads(line)
                row_errors = validate_example(row)
                if row_errors:
                    errors.append(f"{path.relative_to(ROOT)}:{idx + 1}: {'; '.join(row_errors)}")
    return errors


def check_config_references() -> list[str]:
    errors = []
    for path in sorted((ROOT / "configs/train").glob("**/*.yaml")) + sorted((ROOT / "configs/eval").glob("*.yaml")):
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for key in ["train_files", "eval_files"]:
            for rel in cfg.get(key, []) or []:
                if not (ROOT / rel).exists():
                    errors.append(f"{path.relative_to(ROOT)} references missing {rel}")
        if "datasets" in cfg:
            for files in cfg["datasets"].values():
                for rel in files:
                    if not (ROOT / rel).exists():
                        errors.append(f"{path.relative_to(ROOT)} references missing {rel}")
    return errors


def main() -> int:
    errors = []
    missing = check_paths()
    errors.extend(f"missing required path: {p}" for p in missing)
    errors.extend(check_yaml_configs())
    errors.extend(check_prompt_templates())
    errors.extend(check_canonical_samples())
    errors.extend(check_config_references())
    try:
        run(["python3", "scripts/validate_data_governance.py"])
    except subprocess.CalledProcessError as exc:
        errors.append(f"governance validation failed: {exc}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Setup validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
