# Phase 4 Merge Readiness

Status: blocked.

Phase 4 found one full-gated safe improvement:

- Sorbian `checkpoints/phase4/sorbian/edit_preserve_low_lr/adapter@scale=0.35`

Phase 4 did not find a meaningful Ukrainian trained improvement:

- Ukrainian `mr_preserve_kl@0.1` scored 37.401 versus prompt-only 37.399, but the +0.002 delta is within noise and fails the full no-harm gate's real task-gain requirement.

Merge search remains blocked because the Phase 4 merge-readiness rule requires at least two valid full-gated candidates with complementary skills. Current state:

- Eligible for preservation: Sorbian `edit_preserve_low_lr@0.35`.
- Diagnostic only: Ukrainian `mr_preserve_kl@0.1`.
- Fallback: Ukrainian prompt-only Qwen3.5-2B.
- Ineligible: all invalid Phase 3 fixed specialists, all first-pass specialists trained on bad SC/GC data, all failed Phase 4 micro-ablation checkpoints, and any adapter-scale result that did not pass full locked validation.

Final polish remains deferred. It should not run for Ukrainian. For Sorbian, polish can be considered only after a targeted raw-output inspection confirms the candidate's MR gain is not a formatting artifact and SC/GC no-error behavior remains stable.

If merge resumes later, keep the base model as the dominant anchor:

```text
M_final = M_base + aΔ_candidate1 + bΔ_candidate2 + ...
```

Start with `a,b <= 0.1`, include adapter-scale sweeps, and compare against prompt-only every time. Do not mix invalid Phase 3 checkpoints into Phase 4 merge search.
