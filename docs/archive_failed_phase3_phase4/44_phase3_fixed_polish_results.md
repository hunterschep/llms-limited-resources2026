# Phase 3 Fixed Polish Results

Status: not run; explicitly skipped.

Final format/behavior polish was skipped because no merged or otherwise selected base candidate cleared the fixed remediation gates.

Polish remains inappropriate for the current fixed wave because:

- Fixed Ukrainian candidates underperform normalized prompt-only.
- Fixed edit specialists still fail exact SC/GC correction on locked validation.
- Fixed MR specialists do not recover prompt-only MR.
- Sorbian external-enhanced is a diagnostic fallback result, not a selected final candidate.

If a future candidate clears the merge gate, polish should remain small and target only:

- exact SC/GC two-line output
- `CORRECT` / `CORRECT` no-error cases
- final-answer-only MR
- label-only QA
- translation-only MT
- no full-sentence rewrite for edit tasks
- no verbose explanation
- no chain-of-thought
- no JSON/list format
