# Phase 3 Fixed Merge Search

Status: not run.

Merge search remains blocked until `docs/42_phase3_resume_or_block_merge_decision.md` clears fixed checkpoints.

If cleared, use only eligible checkpoints under `checkpoints/phase3_fixed/` and optimize the equal-weighted WMT-style score:

```text
overall_score = mean(MT_score, QA_score, SC_score, GC_score, MR_score)
```

Do not optimize MT alone.
