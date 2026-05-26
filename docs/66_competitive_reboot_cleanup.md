# Competitive Reboot Cleanup

## Decision

Phase 3 and Phase 4 are archived as failed exploratory branches. They remain useful diagnostics, but they are not active model-selection evidence for the competitive reboot.

Archived local diagnostics:

- `docs/archive_failed_phase3_phase4/`
- `results/archive_failed_phase3_phase4/`

Active competitive reboot namespaces:

- `docs/66_*.md` onward
- `results/competitive_reboot/`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/`
- `/scratch/scheppat/projects/wmt26_lrllm/results/competitive_reboot/`
- `/home/scheppat/workspace/projects/wmt26_lrllm/results/competitive_reboot/`

## Preserved

- Source code, evaluators, prompt templates, canonical schemas, governance registry, split manifests, official data, public-source configs, and Andromeda scaffolding.
- Compact Phase 3/4 diagnostics and prompt-only baselines, now archive-only.
- Data quality and cleanup manifests proving what was tried.

## Removed From Active Paths

- Phase 3 first-pass and fixed result JSONs.
- Phase 4 probe, prompt-sweep, micro-ablation, gated-eval, and no-harm gate result JSONs.
- Phase 3/4 dashboards and run logs from active result paths.
- Remote Phase 4 adapter checkpoint under `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase4`.

## Cleanup Manifests

- `results/competitive_reboot/cleanup/local_cleanup_manifest_20260526T051931Z.txt`
- `results/competitive_reboot/cleanup/andromeda_cleanup_manifest_20260526T051931Z.txt`
- `results/competitive_reboot/cleanup/cleanup_summary_20260526T051931Z.md`

## Storage Snapshot

Before remote cleanup:

- Scratch checkpoints: 20M
- Scratch results: 0
- Home results: 3.7M

After remote cleanup:

- Scratch checkpoints: 0, with empty `competitive_reboot/` namespace created
- Scratch competitive results: 0
- Home competitive results: 0

## Active Policy

Do not use or merge Phase 3/4 failed checkpoints. The Sorbian Phase 4 `edit_preserve_low_lr@0.35` adapter is diagnostic only and is labeled `failed_for_competitive_purposes`.
