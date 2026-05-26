# Lineage Recovery Artifact Hygiene

Active local namespace:

- `docs/92_*.md` onward
- `results/lineage_recovery/`

Active Andromeda namespace:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/`
- `/scratch/scheppat/projects/wmt26_lrllm/results/lineage_recovery/`
- `/home/scheppat/workspace/projects/wmt26_lrllm/results/lineage_recovery/`

Preserve until the lineage decision is complete:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/sorbian/edit_repair_tiny`
- `docs/80_competitive_reboot_results_and_decision.md`
- `docs/89_stage_b_rescue_full_eval_results.md`
- `results/competitive_reboot/dashboard.md`
- `results/stage_b_rescue/dashboard.md`
- `results/stage_b_rescue/full_eval/full_eval_summary.json`
- prior cleanup manifests

Delete or archive only after manifesting:

- failed Stage C checkpoints
- failed MR/combined repair checkpoints
- Phase 3/4 checkpoints
- stale raw JSONLs already summarized
- duplicate generated probe/repair data
- stale logs not needed for diagnosis
- empty Ukrainian checkpoint directories

Required validation after cleanup:

```bash
make validate
make smoke-test
make check-governance
make check-overlap
git diff --check
python3 -m compileall scripts src
```

The lineage scripts refuse references to `stage_c_instruction_replay`, `checkpoints/phase3`, and `checkpoints/phase4` in active training/merge configs.
