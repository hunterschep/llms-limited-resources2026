# Hidden Test Risk Decision

Decision: package the selected lineage merge as the Sorbian submission fallback, but label it `higher_local_score_risky`.

Why:

- It is the only candidate with a meaningful full locked-validation improvement over prompt-only: `34.417` overall vs `29.195`, delta `+5.222`.
- It preserves the competitive Sorbian MT breakthrough: `44.035` MT vs `27.477` prompt-only.
- It recovers MR above prompt-only: `10.417` vs `8.333`.
- Final salvage failed to produce any calibrated candidate with nonzero SC/GC no-error accuracy and acceptable task performance.

Risk:

- SC no-error accuracy remains `0.000`.
- GC no-error accuracy remains `0.000`.
- The local SC/GC validation split contains many clean examples: SC has `597` clean of `1167`; GC has `498` clean of `985`.
- If hidden test has similar clean/error balance, SC/GC false-positive behavior can hurt substantially.

Why not use the calibrated model:

- All calibration merge coefficients still had `0.000` SC and GC no-error accuracy.
- The best calibration probe overall (`33.950`) was below the selected lineage merge and did not fix the fatal behavior.

Submission recommendation: submit Sorbian fallback selected lineage merge if participating; do not claim SC/GC no-error is fixed.
