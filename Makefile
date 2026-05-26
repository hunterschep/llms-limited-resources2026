.PHONY: validate inspect-data prepare-data smoke-test report-data-quality check-governance check-overlap build-final-mixtures eval-base-uk eval-base-sorbian build-andromeda-jobs triage-oracle triage-data-sanity triage-raw-oracle triage-raw-predictions triage-overfit triage-overfit-dry-run check-checkpoint-loading report-phase3-sanity report-edit-data-balance report-mr-data-quality retrain-uk-fixed-dryrun retrain-sorbian-fixed-dryrun eval-phase3-fixed-uk eval-phase3-fixed-sorbian report-phase3-fixed phase4-status phase4-cleanup-check phase4-build-probe phase4-eval-prompt-only phase4-prompt-sweep phase4-analyze-failures phase4-micro-ablation-dryrun phase4-rank-candidates phase4-check-gates phase4-report phase4-clean-failed competitive-cleanup competitive-download-data competitive-filter-data competitive-build-mixtures competitive-validate-data competitive-train-sorbian competitive-train-uk competitive-eval-sorbian competitive-eval-uk competitive-compare competitive-dashboard competitive-clean-failed competitive-package-sorbian competitive-package-uk stage-b-status stage-b-cleanup stage-b-error-analysis stage-b-build-repair-data stage-b-prompt-sweep stage-b-scale-sweep stage-b-train-mr-repair stage-b-train-edit-repair stage-b-train-combined-repair stage-b-merge-repairs stage-b-probe-eval stage-b-full-eval stage-b-dashboard stage-b-clean-failed stage-b-package

validate:
	python3 scripts/validate_data_governance.py
	python3 scripts/validate_setup.py

inspect-data:
	python3 scripts/inspect_repo_data.py

prepare-data:
	python3 scripts/create_local_splits.py
	python3 scripts/download_external_data.py --execute
	python3 scripts/compile_mt_data.py
	python3 scripts/compile_qa_data.py
	python3 scripts/compile_sc_data.py
	python3 scripts/compile_gc_data.py
	python3 scripts/compile_mr_data.py
	python3 scripts/build_language_curriculum.py
	python3 scripts/build_format_preference_data.py
	python3 scripts/filter_external_data.py
	python3 scripts/deduplicate_external_data.py
	python3 scripts/check_dev_overlap.py
	python3 scripts/build_external_training_sets.py

smoke-test:
	python3 scripts/smoke_test_data.py
	WMT26_RECORD_RUNS=0 python3 scripts/smoke_test_eval.py
	WMT26_RECORD_RUNS=0 python3 scripts/smoke_test_training.py
	rm -rf checkpoints/uk/specialists/qa
	WMT26_RECORD_RUNS=0 python3 scripts/merge_task_vectors.py --config configs/merge/competitive_uk.yaml --dry-run
	WMT26_RECORD_RUNS=0 python3 scripts/search_merge_weights.py --config configs/merge/competitive_sorbian.yaml --dry-run --limit 1
	python3 scripts/competitive_cleanup_failed.py --execute
	rm -f results/merge_search_sorbian.csv
	find checkpoints -type d -empty -delete 2>/dev/null || true

report-data-quality:
	python3 scripts/report_external_data_quality.py

check-governance:
	python3 scripts/validate_data_governance.py

check-overlap:
	python3 scripts/check_dev_overlap.py

build-final-mixtures:
	python3 scripts/build_external_training_sets.py

eval-base-uk:
	python3 scripts/eval_model.py --config configs/eval/uk.yaml --model Qwen/Qwen3.5-2B

eval-base-sorbian:
	python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model Qwen/Qwen3.5-2B

build-andromeda-jobs:
	python3 andromeda/scripts/generate_jobs.py

triage-oracle:
	WMT26_RECORD_RUNS=0 python3 scripts/triage_oracle_eval.py

triage-data-sanity:
	WMT26_RECORD_RUNS=0 python3 scripts/triage_data_sanity.py

triage-raw-oracle:
	WMT26_RECORD_RUNS=0 python3 scripts/dump_raw_predictions.py --config configs/eval/uk.yaml --oracle --per-task 5 --output results/triage/raw_predictions/uk_oracle.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/uk_oracle.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/dump_raw_predictions.py --config configs/eval/sorbian.yaml --oracle --per-task 5 --output results/triage/raw_predictions/sorbian_oracle.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/sorbian_oracle.jsonl

triage-raw-predictions:
	WMT26_RECORD_RUNS=0 python3 scripts/triage_raw_predictions.py --config configs/eval/uk.yaml --oracle --per-task 10 --output results/triage/raw_predictions/uk_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/uk_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/report_scgc_confusion.py --input results/triage/raw_predictions/uk_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/report_mr_raw_errors.py --input results/triage/raw_predictions/uk_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/triage_raw_predictions.py --config configs/eval/sorbian.yaml --oracle --per-task 10 --output results/triage/raw_predictions/sorbian_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/sorbian_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/report_scgc_confusion.py --input results/triage/raw_predictions/sorbian_oracle_compact.jsonl
	WMT26_RECORD_RUNS=0 python3 scripts/report_mr_raw_errors.py --input results/triage/raw_predictions/sorbian_oracle_compact.jsonl

triage-overfit-dry-run:
	python3 scripts/run_single_batch_overfit.py --track uk --task QA --examples 5 --dry-run
	python3 scripts/run_single_batch_overfit.py --track uk --task SC --examples 5 --dry-run
	python3 scripts/run_single_batch_overfit.py --track uk --task GC --examples 5 --dry-run
	python3 scripts/run_single_batch_overfit.py --track uk --task MR --examples 5 --dry-run
	python3 scripts/run_single_batch_overfit.py --track uk --task MT --examples 5 --dry-run

triage-overfit:
	python3 scripts/triage_single_task_overfit.py --track uk --task SC --examples 20 --dry-run
	python3 scripts/triage_single_task_overfit.py --track uk --task GC --examples 20 --dry-run
	python3 scripts/triage_single_task_overfit.py --track uk --task MR --examples 20 --dry-run
	python3 scripts/triage_single_task_overfit.py --track sorbian --task SC --examples 20 --dry-run
	python3 scripts/triage_single_task_overfit.py --track sorbian --task GC --examples 20 --dry-run
	python3 scripts/triage_single_task_overfit.py --track sorbian --task MR --examples 20 --dry-run

check-checkpoint-loading:
	python3 scripts/check_checkpoint_loading.py --help >/dev/null

report-edit-data-balance:
	python3 scripts/report_edit_data_balance.py --fail-on-warn

report-mr-data-quality:
	python3 scripts/report_mr_data_quality.py --fail-on-issues

report-phase3-sanity: report-edit-data-balance report-mr-data-quality
	python3 scripts/report_phase3_sanity.py

retrain-uk-fixed-dryrun:
	python3 scripts/train_sft.py --config configs/train/uk/edit_scgc.yaml --dry-run --max-examples 4
	python3 scripts/train_sft.py --config configs/train/uk/mr.yaml --dry-run --max-examples 4
	python3 scripts/train_sft.py --config configs/train/baseline_task_balanced_uk.yaml --dry-run --max-examples 8
	python3 scripts/train_sft.py --config configs/train/uk/external_enhanced_multitask.yaml --dry-run --max-examples 8

retrain-sorbian-fixed-dryrun:
	python3 scripts/train_sft.py --config configs/train/sorbian/edit_scgc.yaml --dry-run --max-examples 4
	python3 scripts/train_sft.py --config configs/train/sorbian/mr.yaml --dry-run --max-examples 4
	python3 scripts/train_sft.py --config configs/train/baseline_task_balanced_sorbian.yaml --dry-run --max-examples 8
	python3 scripts/train_sft.py --config configs/train/sorbian/external_enhanced_multitask.yaml --dry-run --max-examples 8

eval-phase3-fixed-uk:
	WMT26_RECORD_RUNS=0 python3 scripts/eval_model.py --config configs/eval/uk.yaml --oracle --limit 5 --output results/phase3_fixed/uk/oracle_smoke.json

eval-phase3-fixed-sorbian:
	WMT26_RECORD_RUNS=0 python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --oracle --limit 5 --output results/phase3_fixed/sorbian/oracle_smoke.json

report-phase3-fixed:
	mkdir -p results/phase3_fixed/comparisons
	python3 scripts/report_eval_comparison.py results/baselines/base_qwen35_2b_uk.json results/phase3_fixed/uk/*.json --format markdown --output results/phase3_fixed/comparisons/uk_fixed_comparison.md
	python3 scripts/report_eval_comparison.py results/baselines/base_qwen35_2b_sorbian.json results/phase3_fixed/sorbian/*.json --format markdown --output results/phase3_fixed/comparisons/sorbian_fixed_comparison.md

phase4-status:
	python3 scripts/run_phase4.py status

phase4-cleanup-check:
	python3 scripts/phase4_cleanup_check.py

phase4-build-probe:
	python3 scripts/build_phase4_probe_suite.py

phase4-eval-prompt-only:
	WMT26_RECORD_RUNS=0 python3 scripts/eval_phase4_probe.py --config configs/eval/phase4_probe_uk.yaml --oracle --output results/phase4/probe/oracle_uk.json
	WMT26_RECORD_RUNS=0 python3 scripts/eval_phase4_probe.py --config configs/eval/phase4_probe_sorbian.yaml --oracle --output results/phase4/probe/oracle_sorbian.json

phase4-prompt-sweep:
	WMT26_RECORD_RUNS=0 python3 scripts/phase4_prompt_sweep.py --config configs/eval/phase4_prompt_sweep_uk.yaml --oracle
	WMT26_RECORD_RUNS=0 python3 scripts/phase4_prompt_sweep.py --config configs/eval/phase4_prompt_sweep_sorbian.yaml --oracle

phase4-analyze-failures:
	python3 scripts/phase4_analyze_failures.py
	python3 scripts/phase4_compare_train_eval_distributions.py
	python3 scripts/phase4_prompt_mismatch_check.py
	python3 scripts/phase4_raw_error_taxonomy.py
	python3 scripts/phase4_analyze_loss_curves.py

phase4-micro-ablation-dryrun:
	WMT26_RECORD_RUNS=0 python3 scripts/phase4_run_micro_ablations.py --dry-run --max-examples 8

phase4-rank-candidates:
	python3 scripts/phase4_rank_ablation_candidates.py

phase4-check-gates:
	python3 scripts/phase4_check_no_harm_gates.py --baseline results/phase3_fixed/uk/base_qwen35_2b.json --candidates results/phase3_fixed/uk/edit.json results/phase3_fixed/uk/mr.json --output results/phase4/gates/phase3_fixed_uk_gate_check.json || true
	python3 scripts/phase4_check_no_harm_gates.py --baseline results/phase3_fixed/sorbian/base_qwen35_2b.json --candidates results/phase3_fixed/sorbian/edit.json results/phase3_fixed/sorbian/mr.json results/phase3_fixed/sorbian/external_enhanced.json --output results/phase4/gates/phase3_fixed_sorbian_gate_check.json || true

phase4-report:
	python3 scripts/phase4_report.py

phase4-clean-failed:
	python3 scripts/phase4_cleanup_failed.py

competitive-cleanup:
	python3 scripts/run_competitive_reboot.py cleanup

competitive-download-data:
	python3 scripts/run_competitive_reboot.py download-data

competitive-filter-data:
	python3 scripts/run_competitive_reboot.py filter-data

competitive-build-mixtures:
	python3 scripts/run_competitive_reboot.py build-mixtures

competitive-validate-data:
	python3 scripts/run_competitive_reboot.py validate-data

competitive-train-sorbian:
	python3 scripts/run_competitive_reboot.py train-sorbian

competitive-train-uk:
	python3 scripts/run_competitive_reboot.py train-uk

competitive-eval-sorbian:
	python3 scripts/run_competitive_reboot.py eval-sorbian --oracle --output results/competitive_reboot/eval/sorbian/oracle_smoke.json

competitive-eval-uk:
	python3 scripts/run_competitive_reboot.py eval-uk --oracle --output results/competitive_reboot/eval/uk/oracle_smoke.json

competitive-compare:
	python3 scripts/run_competitive_reboot.py compare

competitive-dashboard:
	python3 scripts/run_competitive_reboot.py dashboard

competitive-clean-failed:
	python3 scripts/run_competitive_reboot.py clean-failed

competitive-package-sorbian:
	python3 scripts/competitive_package_model.py --track sorbian --model-dir checkpoints/competitive_reboot/sorbian/final --output-dir results/competitive_reboot/package --dry-run

competitive-package-uk:
	python3 scripts/competitive_package_model.py --track uk --model-dir checkpoints/competitive_reboot/uk/final --output-dir results/competitive_reboot/package --dry-run

stage-b-status:
	python3 scripts/run_stage_b_rescue.py status

stage-b-cleanup:
	python3 scripts/run_stage_b_rescue.py cleanup

stage-b-error-analysis:
	python3 scripts/stage_b_error_analysis.py

stage-b-build-repair-data:
	python3 scripts/build_stage_b_repair_data.py

stage-b-prompt-sweep:
	python3 scripts/stage_b_prompt_sweep.py

stage-b-scale-sweep:
	python3 scripts/stage_b_scale_sweep.py

stage-b-train-mr-repair:
	python3 scripts/train_stage_b_repair.py --config configs/train/stage_b_rescue/sorbian_mr_repair_tiny.yaml --dry-run --max-examples 8

stage-b-train-edit-repair:
	python3 scripts/train_stage_b_repair.py --config configs/train/stage_b_rescue/sorbian_edit_repair_tiny.yaml --dry-run --max-examples 8

stage-b-train-combined-repair:
	python3 scripts/train_stage_b_repair.py --config configs/train/stage_b_rescue/sorbian_combined_repair_tiny.yaml --dry-run --max-examples 8

stage-b-merge-repairs:
	python3 scripts/merge_stage_b_repair.py

stage-b-probe-eval:
	python3 scripts/build_stage_b_rescue_probe.py

stage-b-full-eval:
	python3 scripts/stage_b_full_eval_candidates.py --candidate stage_b_mt_large /scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large

stage-b-dashboard:
	python3 scripts/stage_b_error_analysis.py
	python3 scripts/merge_stage_b_repair.py

stage-b-clean-failed:
	python3 scripts/competitive_cleanup_failed.py --execute

stage-b-package:
	python3 scripts/stage_b_package_candidate.py --model-dir /scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large --dry-run
