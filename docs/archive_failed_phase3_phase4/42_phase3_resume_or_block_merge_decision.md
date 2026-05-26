# Phase 3 Resume Or Block Merge Decision

Status: blocked.

Merge search must not resume with the current fixed retrain wave. The remediation explained the suspicious first-pass results, but the retrained specialists do not clear the post-remediation gates.

## Decision

Do not run skill-vector/model merging from these fixed checkpoints.

## Reasons

- Ukrainian normalized prompt-only is the best Ukrainian model in the fixed wave: 37.399 overall.
- Every fixed Ukrainian retrain underperforms prompt-only, including fixed `M_edit`, fixed `M_mr`, task-balanced, and external-enhanced.
- Fixed Ukrainian `M_edit` still fails the edit-specialist gate: GC correction is 0.0 and GC detection drops to 29.187.
- Fixed Ukrainian `M_mr` does not recover prompt-only MR: 20.833 versus 29.167.
- Sorbian external-enhanced is a small diagnostic fallback improvement, 30.004 versus 29.195 prompt-only, but it is not a clean specialist vector.
- Fixed Sorbian `M_edit` is blocked: 22.684 overall and weak edit correction.
- Fixed Sorbian `M_mr` is blocked: MR stays at 8.333 and MT falls to 23.522.
- Fixed task-balanced Sorbian improves QA/MR slightly but damages GC too heavily.

## Eligible For Future Consideration

- Normalized prompt-only baselines as evaluation references.
- Compact triage overfit checkpoints only as debugging evidence, not merge inputs.
- Sorbian fixed external-enhanced result as a diagnostic fallback metric. Its checkpoint was pruned for storage hygiene and should be retrained intentionally if it becomes a fallback candidate.
- Unaffected first-pass `M_lang`, `M_mt`, or `M_qa` only after a separate checkpoint-loading and normalized-eval review. They are not automatically eligible.

## Explicitly Ineligible

- First-pass `M_edit`.
- First-pass `M_mr`.
- Any model trained on the unbalanced first-pass SC/GC mixtures.
- Any stale checkpoint from canceled jobs.
- Any result generated only under the old strict MR parser.
- Fixed `M_edit` and fixed `M_mr` checkpoints from this wave.
- Fixed Ukrainian task-balanced and external-enhanced checkpoints.
- Fixed Sorbian task-balanced checkpoint.

## Next Gate To Resume Merge

Merge can resume only after a narrower second remediation produces:

- An edit specialist with useful SC/GC correction and sane no-error behavior on locked validation.
- An MR specialist or MR-preserving multitask model that matches or beats normalized prompt-only MR.
- A checkpoint-loading report for the specific candidate checkpoints.
- Normalized all-five-task evals for every candidate under the same evaluator.

Until then, final polish also remains blocked.
