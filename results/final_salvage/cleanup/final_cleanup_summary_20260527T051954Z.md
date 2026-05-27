# Final salvage failed-artifact cleanup
Wed May 27 05:19:57 AM UTC 2026

Storage before:
86G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints
8.0K	/scratch/scheppat/projects/wmt26_lrllm/results
60M	/home/scheppat/workspace/projects/wmt26_lrllm/results

Deleting failed final-salvage calibration checkpoints:
3.6G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian/scgc_calibration_tiny
DELETE_DIR /scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian/scgc_calibration_tiny
25G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian/scgc_calibration_merge
DELETE_DIR /scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian/scgc_calibration_merge

Preserving package and selected lineage model:
KEEP /scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian_primary_package
KEEP /scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10

Storage after:
58G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints
8.0K	/scratch/scheppat/projects/wmt26_lrllm/results
60M	/home/scheppat/workspace/projects/wmt26_lrllm/results
