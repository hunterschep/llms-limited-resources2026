# Phase 3 Fixed Merge Search

Status: not run; explicitly blocked.

The fixed remediation wave did not produce safe skill vectors for merging. Running merge search now would optimize around specialists that still damage SC/GC, MR, or both.

Blocked inputs:

- Fixed Ukrainian `M_edit`, `M_mr`, task-balanced, and external-enhanced.
- Fixed Sorbian `M_edit`, `M_mr`, and task-balanced.
- Sorbian external-enhanced is retained only as a diagnostic metric, not as a skill-vector input.
- All first-pass edit/MR checkpoints and stale canceled-job checkpoints remain ineligible.

Future merge search should use only candidates that pass the gate in `docs/42_phase3_resume_or_block_merge_decision.md` and must still optimize:

```text
overall_score = mean(MT_score, QA_score, SC_score, GC_score, MR_score)
```

MT-only merge selection is not allowed.
