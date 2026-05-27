# Final Salvage Cleanup

Cleanup completed.

Remote cleanup manifests:

- `results/final_salvage/cleanup/misplaced_sync_cleanup_20260527T045746Z.txt`
- `results/final_salvage/cleanup/final_cleanup_manifest_20260527T051954Z.txt`
- `results/final_salvage/cleanup/final_cleanup_summary_20260527T051954Z.md`

Deleted on Andromeda:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian/scgc_calibration_tiny`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian/scgc_calibration_merge`

Preserved on Andromeda:

- Final Sorbian package: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian_primary_package`
- Selected lineage merge source model.
- Stage A parent, Stage B adapter, and Stage B merged lineage artifacts from lineage recovery.

Checkpoint storage:

- Before failed-calibration cleanup: `86G`
- After failed-calibration cleanup: `58G`

Queue note:

- No final-salvage jobs remain active after packaging and validation.
- One unrelated `hunter_full_repair` job in `/home/scheppat/workspace/scripts/formosan_audio_ingest` was active during cleanup and was not touched.
