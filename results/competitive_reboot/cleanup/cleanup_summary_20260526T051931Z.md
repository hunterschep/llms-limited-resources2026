# Competitive Reboot Cleanup Summary

Timestamp: 2026-05-26T05:19:31Z

The failed Phase 3 and Phase 4 branches were removed from active decision paths.

Local archive actions:

- Moved `docs/23_*.md` through `docs/54_*.md` into `docs/archive_failed_phase3_phase4/`.
- Moved failed Phase 3/4 result trees into `results/archive_failed_phase3_phase4/`.
- Preserved prompt-only baselines in `results/baselines/`.
- Preserved source code, data governance, canonical schema, evaluators, training scripts, prompt/config scaffolding, and split manifests.

Andromeda cleanup actions:

- Deleted `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase4`.
- Created clean competitive namespaces:
  - `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/`
  - `/scratch/scheppat/projects/wmt26_lrllm/results/competitive_reboot/`
  - `/home/scheppat/workspace/projects/wmt26_lrllm/results/competitive_reboot/`

Storage:

- Remote WMT26 checkpoint tree before cleanup: 20M.
- Remote WMT26 checkpoint tree after cleanup: 0.
- Local failed result trees were archived, not deleted, because they are compact diagnostics.

Validation after cleanup: pending.
