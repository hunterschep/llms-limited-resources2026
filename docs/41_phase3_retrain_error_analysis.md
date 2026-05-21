# Phase 3 Retrain Error Analysis

Status: complete for the fixed remediation wave.

## What Is Explained

The first-pass suspicious results were not a global training/checkpoint failure:

- Gold-target oracle scoring reaches 100 for QA, MR, SC, and GC.
- Compact same-set overfit passes for Ukrainian and Sorbian SC, GC, and MR.
- Checkpoint-loading diagnostics confirm trained checkpoints produce different outputs from base.
- MR prompt-only scores rose after normalization: Ukrainian 4.17 to 29.17, Sorbian 0.00 to 8.33.
- SC/GC detection plateaus were traceable to the original edit mixtures being almost all error cases.

## Ukrainian Errors

The fixed Ukrainian models do not beat normalized prompt-only. The key failures are:

- Fixed `M_edit` changes the prior away from always-error, but now under-detects GC and collapses GC correction to 0.0.
- Fixed `M_mr` improves QA but does not recover prompt-only MR, and it destroys exact SC/GC correction.
- Fixed task-balanced and external-enhanced runs damage GC and MR too much to be fallback candidates.

Compact raw prediction diagnostics on 10 examples per task:

| Model | MT chrF | QA acc | SC det/corr | GC det/corr | MR acc | SC no-error acc | GC no-error acc | MR malformed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `uk_base` | 44.67 | 0.00 | 0.571 / 0.400 | 0.824 / 0.000 | 0.30 | 0.00 | 0.00 | 0.40 |
| `uk_edit` | 42.46 | 0.20 | 0.667 / 0.667 | 0.000 / 0.000 | 0.10 | 0.67 | 0.00 | 0.50 |
| `uk_mr` | 45.08 | 0.00 | 0.571 / 0.000 | 0.824 / 0.000 | 0.10 | 0.00 | 0.00 | 0.00 |
| `uk_task_balanced` | 42.82 | 0.30 | 0.667 / 0.400 | 0.000 / 0.000 | 0.10 | 1.00 | 0.33 | 0.20 |
| `uk_external_enhanced` | 43.34 | 0.30 | 0.400 / 0.400 | 0.000 / 0.000 | 0.10 | 1.00 | 1.00 | 0.90 |

These samples support the locked-validation result: the edit task is now dominated by missed real errors or exact-correction failures, while MR remains mostly wrong numeric answers or malformed/verbose answers depending on the model.

## Sorbian Errors

Sorbian external-enhanced is a small overall improvement over normalized prompt-only, mostly from MT and MR, but its edit correction remains poor. The specialists are not useful merge inputs:

- Fixed `M_edit` damages MT and GC detection while only slightly improving correction from near-zero.
- Fixed `M_mr` improves QA but leaves MR unchanged and reduces MT.
- Fixed task-balanced slightly improves MR and QA but damages GC too heavily.
- Fixed external-enhanced is a diagnostic fallback candidate, not a clean skill vector.

Compact raw prediction diagnostics on 5 examples per task:

| Model | MT chrF | QA acc | SC det/corr | GC det/corr | MR acc | SC no-error acc | GC no-error acc | MR malformed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `sorbian_base` | 10.11 | 0.60 | 0.571 / 0.000 | 0.571 / 0.000 | 0.00 | 0.00 | 0.00 | 0.00 |
| `sorbian_edit` | 8.65 | 0.60 | 0.500 / 0.000 | 0.000 / 0.000 | 0.00 | 0.67 | 1.00 | 0.00 |
| `sorbian_mr` | 14.02 | 0.80 | 0.571 / 0.000 | 0.571 / 0.000 | 0.00 | 0.00 | 0.00 | 0.00 |
| `sorbian_task_balanced` | 10.51 | 0.60 | 0.500 / 0.000 | 0.500 / 0.000 | 0.20 | 0.67 | 0.67 | 0.00 |
| `sorbian_external_enhanced` | 33.89 | 0.40 | 0.571 / 0.000 | 0.571 / 0.000 | 0.00 | 0.00 | 0.00 | 0.60 |

## Working Theory

The pipeline is sane, but the current fixed data/configs are still not a competitive training recipe:

- Edit data can be memorized but does not transfer to official locked validation. The balanced mixture fixed the prior artifact but introduced too many no-error behaviors and not enough realistic one-token grammatical/correction coverage.
- MR preservation data is parseable and overfittable but too small/narrow to preserve the base model's broader arithmetic under fine-tuning.
- Multitask fixed runs are brittle: they can improve QA or Sorbian MT while damaging exact edit correction and MR.
- Sorbian external-enhanced suggests the public-data layer helps language/MT, but not enough to make the specialists safe for task-vector merging.

## Actionable Next Remediation

- Do not merge these fixed specialists.
- Redesign edit training around harder clean/error contrastive examples, more real one-token corrections, and per-error-type caps.
- Redesign MR around a larger but still governed final-answer-only preservation set and evaluate on held-out arithmetic before full WMT-style locked validation.
- Keep Sorbian external-enhanced metrics as a diagnostic fallback, but prune its checkpoint until a deliberate fallback-model run is requested.
