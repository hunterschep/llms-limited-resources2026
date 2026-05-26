# Stage B Rescue Full Eval Results

## Decision

The best rescued checkpoint is `edit_repair_tiny`.

It beats Stage B overall by `+0.351`, keeps MT at `43.345`, and recovers MR from `4.167` to `6.250`. It does not reach the preferred `+5` over prompt-only target, and MR remains below the prompt-only `8.333`, so this is a `promising_needs_more_repair` checkpoint rather than a clean final candidate.

## Full Eval Table

| Model | Overall | Delta vs Prompt | Delta vs Stage B | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only | 29.195 | +0.000 | -3.631 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | fallback |
| Stage B MT-large | 32.826 | +3.631 | +0.000 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 | MT_anchor |
| Stage C replay | 21.250 | -7.945 | -11.576 | 43.790 | 47.170 | 7.098 | 1.942 | 6.250 | rejected_edit_collapse |
| Stage B short-96 decoding | 32.945 | +3.750 | +0.119 | 43.929 | 48.428 | 34.708 | 33.493 | 4.167 | rejected_MR_not_repaired |
| MR repair tiny | 32.799 | +3.604 | -0.027 | 43.404 | 48.428 | 34.708 | 33.289 | 4.167 | rejected_full_eval_no_gain |
| edit repair tiny | 33.177 | +3.982 | +0.351 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 | promising_needs_more_repair |

## MT Direction Scores

| Direction | Prompt-only | Stage B | edit repair tiny | Delta edit vs prompt | Delta edit vs Stage B |
|---|---:|---:|---:|---:|---:|
| de->dsb | 11.970 | 27.779 | 27.546 | +15.576 | -0.233 |
| de->hsb | 11.991 | 31.451 | 31.497 | +19.506 | +0.046 |
| dsb->de | 26.907 | 45.884 | 46.089 | +19.182 | +0.205 |
| dsb->hsb | 42.459 | 49.880 | 49.881 | +7.422 | +0.001 |
| hsb->de | 32.310 | 52.113 | 51.915 | +19.605 | -0.198 |
| hsb->dsb | 39.724 | 48.352 | 48.624 | +8.900 | +0.272 |

## Outcome

Outcome B: Stage B is partially rescued but not fully final. The retained edit-repair checkpoint improves the Stage B tradeoff and is packageable, but it misses the +5-over-prompt target and still does not recover prompt-only MR.
