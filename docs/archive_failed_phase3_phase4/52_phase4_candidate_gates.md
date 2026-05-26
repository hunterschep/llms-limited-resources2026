# Phase 4 Candidate Gates

Implemented by `scripts/phase4_check_no_harm_gates.py`.

A candidate passes the probe only if:

- overall score exceeds the prompt-only probe anchor
- no individual task drops more than 2.0 points by default
- at least one task improves by 1.0 point or more
- SC/GC do not collapse into always-error or always-CORRECT behavior
- MR remains at least prompt-only unless a documented tradeoff is intentionally accepted
- malformed output rates remain low

Candidates that fail are blocked, pruned, and excluded from merge/final polish.

Full locked-validation gate result:

- Ukrainian `mr_preserve_kl@0.10`: failed. It was numerically safe, but +0.002 overall versus prompt-only is not a real improvement and no task improved by at least 1.0 point.
- Sorbian `edit_preserve_low_lr@0.35`: passed. It improved overall by +0.599, improved MR by +4.167, kept MT slightly positive, left SC/GC unchanged, and kept QA drop within the 2.0 point no-harm threshold.
