# Phase 3 Fixed Checkpoint Cleanup

Timestamp UTC: 20260521T100927Z

Deleted blocked fixed retrain checkpoints from /scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase3_fixed after normalized evaluation showed they should not be merged. Compact eval JSON, raw predictions, diagnostics, and cleanup manifests were preserved in the project results tree.

Manifest: results/cleanup/phase3_fixed_checkpoint_cleanup_20260521T100927Z.txt

before_phase3_fixed_checkpoints=29G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase3_fixed
before_checkpoint_root=50G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints
after_phase3_fixed_checkpoints=0	/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase3_fixed
after_checkpoint_root=22G	/scratch/scheppat/projects/wmt26_lrllm/checkpoints
