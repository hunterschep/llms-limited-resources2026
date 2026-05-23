# Phase 4 Merge Readiness

Status: blocked.

Merge search may resume only if at least two Phase 4 candidates pass full locked validation gates and represent complementary skills. Invalid Phase 3 fixed specialists and first-pass edit/MR specialists remain ineligible.

If merge resumes, use the base model as the dominant anchor:

```text
M_final = M_base + aΔ_candidate1 + bΔ_candidate2 + ...
```

Start with small coefficients, `a,b <= 0.1`, and compare against prompt-only every time. Do not run final polish until a merged or single candidate beats prompt-only and passes no-harm gates.
