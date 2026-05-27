# Final Salvage Eval Results

The only full-eval-positive candidate remains the selected lineage merge from lineage recovery. Final salvage ran SC/GC-specific audit, prompt/decoding probes, and a tiny model-level calibration sweep. No calibrated candidate passed the probe gate, so no failed calibration candidate was promoted to full locked evaluation.

| Model | Overall | MT | QA | SC | GC | MR | SC no-error | GC no-error | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | 0.000 | 0.000 | Baseline. |
| selected lineage merge | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 | 0.000 | 0.000 | Package fallback; best local overall, risky hidden SC/GC. |
| best prompt sweep, binary_precondition | diagnostic only | unchanged | unchanged | correction collapses | correction collapses | unchanged | 1.000 | 0.983 | Reject: always-CORRECT behavior. |
| best calibration probe, scgc_alpha_0p15 | 33.950 probe | 42.187 | 47.799 | 38.095 | 33.333 | 8.333 | 0.000 | 0.000 | Reject: no no-error recovery. |

Selected lineage merge MT directions:

| Direction | chrF++ |
|---|---:|
| de->hsb | 32.135 |
| de->dsb | 27.598 |
| hsb->de | 52.991 |
| dsb->de | 46.695 |
| hsb->dsb | 50.009 |
| dsb->hsb | 49.870 |

Final-salvage package validation passed for the selected lineage merge package.
