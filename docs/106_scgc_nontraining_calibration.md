# SC/GC Nontraining Calibration

Final salvage tested whether prompt wording and short decoding recover CORRECT/CORRECT behavior before changing weights.

Prompt variants:

- strict original
- conservative no-error
- evidence-first
- binary precondition
- no-rewrite hard constraint

Decoding caps:

- `max_new_tokens=16`
- `max_new_tokens=24`
- `max_new_tokens=48`

Result:

| Variant | max_new_tokens | SC no-error | GC no-error | SC detection F1 | SC correction F1 | GC detection F1 | GC correction F1 | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| binary_precondition | 16/24/48 | 1.000 | 0.983 | 0.017 | 0.000 | 0.000 | 0.000 | Reject: flips to almost always-CORRECT. |
| no_rewrite_hard | 16 | 0.050 | 0.025 | 0.659 | 0.017 | 0.653 | 0.017 | Reject: no-error recovery too small. |
| no_rewrite_hard | 24/48 | 0.050 | 0.025 | 0.659 | 0.033 | 0.653 | 0.000 | Reject: no-error recovery too small. |
| evidence_first | 16/24/48 | 0.000 | 0.008 | 0.667 | 0.000 | 0.669 | 0.000 | Reject. |
| strict/conservative | 16/24/48 | 0.000 | 0.000 | 0.667 | up to 0.095 | 0.667 | 0.000 | Reject. |

Non-training calibration did not produce a usable submission setting. The only prompt that recovered clean examples destroyed true-error detection and correction, so it is not a valid rescue.
