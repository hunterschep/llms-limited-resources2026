# Phase 3 Cleanup Policy

Cleanup is conservative: remove invalid active artifacts, preserve compact evidence.

## Preserve

- Official/source data, governed external data, manifests, and split records.
- Prompt-only baseline results.
- `results/triage/` diagnostics and raw prediction samples.
- Cleanup manifests and summaries.
- Scripts, configs, docs, and Make targets needed to reproduce remediation.

## Delete Or Quarantine

- First-pass tuned checkpoints trained before edit-balance/MR-normalization remediation.
- Partial checkpoints from canceled jobs.
- Old tuned-model result JSONs and interference matrices based on invalid checkpoints.
- Old final-selection placeholders.
- Non-diagnostic Slurm logs from bad/canceled jobs.
- Local `__pycache__`, temporary files, and accidental generated junk.

## Namespaces

- Triage evidence: `results/triage/`.
- Cleanup records: `results/cleanup/`.
- Fixed retraining checkpoints: `checkpoints/phase3_fixed/` on Andromeda scratch.
- Fixed results: `results/phase3_fixed/`.

## Required Checks After Cleanup

Run:

```bash
make validate
git diff --check
git status --short
```

Remote cleanup must record a manifest before deletion and use only `ssh andromeda`.

## Completed Cleanup Records

- First-pass invalid artifact cleanup: `results/cleanup/phase3_cleanup_manifest_20260521T063217Z.txt`.
- Fixed checkpoint cleanup after blocked evals: `results/cleanup/phase3_fixed_checkpoint_cleanup_20260521T100927Z.txt`.
- Fixed checkpoint cleanup summary: `results/cleanup/phase3_fixed_checkpoint_cleanup_summary_20260521T100927Z.md`.

The fixed checkpoint cleanup removed `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase3_fixed` contents after compact eval JSON and raw diagnostics were preserved. The fixed checkpoint namespace went from 29G to 0; the total remote checkpoint root went from 50G to 22G.
