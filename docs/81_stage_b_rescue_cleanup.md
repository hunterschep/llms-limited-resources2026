# Stage B Rescue Cleanup

## Decision

Stage B rescue starts from the competitive reboot closeout, not from Phase 3/4. The only active checkpoint to preserve is:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large`

Prompt-only, Stage B, Stage C diagnostic result JSONs, direction breakdowns, compact raw summaries, governance manifests, data configs, and scripts are preserved.

## Cleaned Or Quarantined

- Failed Phase 3/4 docs and results are archived under `docs/archive_failed_phase3_phase4/` and `results/archive_failed_phase3_phase4/`.
- Failed Ukrainian competitive checkpoints were already removed in the competitive reboot cleanup.
- Sorbian Stage A and Stage C checkpoints were already removed; Stage C remains diagnostic only through compact results and raw predictions.
- Empty/stale remote checkpoint directories are removed after manifesting.

## Active Namespaces

- Local results: `results/stage_b_rescue/`
- Local generated data: `data/processed/stage_b_rescue/sorbian/`
- Remote checkpoints: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/`
- Remote results: `/scratch/scheppat/projects/wmt26_lrllm/results/stage_b_rescue/` and `/home/scheppat/workspace/projects/wmt26_lrllm/results/stage_b_rescue/`

## Validation

After cleanup, run:

```bash
make validate
make smoke-test
make check-governance
make check-overlap
git diff --check
python3 -m compileall scripts src
```
