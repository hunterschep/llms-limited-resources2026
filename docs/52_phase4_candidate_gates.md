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
