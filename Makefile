.PHONY: validate inspect-data prepare-data smoke-test report-data-quality check-governance check-overlap build-final-mixtures eval-base-uk eval-base-sorbian build-andromeda-jobs

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
	WMT26_RECORD_RUNS=0 python3 scripts/merge_task_vectors.py --config configs/merge/uk.yaml --dry-run
	WMT26_RECORD_RUNS=0 python3 scripts/search_merge_weights.py --config configs/merge/sorbian.yaml --dry-run --limit 2

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
