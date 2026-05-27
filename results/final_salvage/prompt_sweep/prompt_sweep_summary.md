# Final Salvage SC/GC Prompt Sweep

| Variant | max_new_tokens | SC no-error | GC no-error | SC det | SC corr | GC det | GC corr |
|---|---:|---:|---:|---:|---:|---:|---:|
| binary_precondition | 16 | 1.000 | 0.983 | 0.017 | 0.000 | 0.000 | 0.000 |
| binary_precondition | 24 | 1.000 | 0.983 | 0.017 | 0.000 | 0.000 | 0.000 |
| binary_precondition | 48 | 1.000 | 0.983 | 0.017 | 0.000 | 0.000 | 0.000 |
| no_rewrite_hard | 16 | 0.050 | 0.025 | 0.659 | 0.017 | 0.653 | 0.017 |
| no_rewrite_hard | 24 | 0.050 | 0.025 | 0.659 | 0.033 | 0.653 | 0.000 |
| no_rewrite_hard | 48 | 0.050 | 0.025 | 0.659 | 0.033 | 0.653 | 0.000 |
| evidence_first | 16 | 0.000 | 0.008 | 0.667 | 0.000 | 0.669 | 0.000 |
| evidence_first | 24 | 0.000 | 0.008 | 0.667 | 0.000 | 0.669 | 0.000 |
| evidence_first | 48 | 0.000 | 0.008 | 0.667 | 0.000 | 0.669 | 0.000 |
| strict_original | 48 | 0.000 | 0.000 | 0.667 | 0.095 | 0.667 | 0.000 |
| conservative_no_error | 24 | 0.000 | 0.000 | 0.667 | 0.095 | 0.667 | 0.000 |
| conservative_no_error | 48 | 0.000 | 0.000 | 0.667 | 0.095 | 0.667 | 0.000 |
| strict_original | 24 | 0.000 | 0.000 | 0.667 | 0.080 | 0.667 | 0.000 |
| strict_original | 16 | 0.000 | 0.000 | 0.667 | 0.033 | 0.667 | 0.017 |
| conservative_no_error | 16 | 0.000 | 0.000 | 0.667 | 0.049 | 0.667 | 0.000 |
