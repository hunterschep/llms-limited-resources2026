# Model Selection Policy

## Priority Order

1. WMT26 compliance: one Qwen3.5-family <=2B model per track, no forbidden data, no task-specific adapter switching.
2. Equal-weighted overall score.
3. MT improvement, because competitive low-resource systems must move translation quality.
4. Auxiliary stability: QA/MR/SC/GC cannot catastrophically collapse.
5. Robustness: no parser artifact or tiny-example dependency.
6. Packageability as one loadable model.

## Labels

- `competitive_candidate`
- `promising_but_needs_replay`
- `MT_strong_aux_damaged`
- `aux_strong_MT_flat`
- `prompt_only_fallback`
- `failed`
- `failed_for_competitive_purposes`

The Phase 4 Sorbian `+0.599` adapter is labeled `failed_for_competitive_purposes`.
