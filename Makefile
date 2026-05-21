.PHONY: validate inspect-data prepare-data smoke-test eval-base-uk eval-base-sorbian build-andromeda-jobs

validate:
	python3 scripts/validate_data_governance.py
	python3 scripts/validate_setup.py

inspect-data:
	python3 scripts/inspect_repo_data.py

prepare-data:
	python3 scripts/create_local_splits.py
	python3 scripts/compile_mt_data.py
	python3 scripts/compile_qa_data.py
	python3 scripts/compile_sc_data.py
	python3 scripts/compile_gc_data.py
	python3 scripts/compile_mr_data.py
	python3 scripts/build_language_curriculum.py
	python3 scripts/build_format_preference_data.py

smoke-test:
	python3 scripts/smoke_test_data.py
	python3 scripts/smoke_test_eval.py
	python3 scripts/smoke_test_training.py
	python3 scripts/merge_task_vectors.py --config configs/merge/uk.yaml --dry-run
	python3 scripts/search_merge_weights.py --config configs/merge/sorbian.yaml --dry-run --limit 2

eval-base-uk:
	python3 scripts/eval_model.py --config configs/eval/uk.yaml --model Qwen/Qwen3.5-2B

eval-base-sorbian:
	python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --model Qwen/Qwen3.5-2B

build-andromeda-jobs:
	python3 andromeda/scripts/generate_jobs.py
