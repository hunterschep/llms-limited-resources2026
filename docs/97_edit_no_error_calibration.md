# Edit No-Error Calibration

Stage B and `edit_repair_tiny` still have weak SC/GC no-error behavior. The failed Stage C recipe destroyed edit performance, so calibration is tiny and targeted.

Data:

- hard no-error hsb/dsb examples
- near-miss examples where the model tends to hallucinate an error
- one-token SC correction examples
- one-token GC correction examples
- exact `Wrong word:` / `Correct word:` two-line targets
- official-style length distribution
- separate hsb/dsb balance where sources allow it

Ratio sweeps:

- 60/40 clean/error
- 50/50 clean/error
- 40/60 clean/error

Methods:

- prompt/decoding calibration first
- tiny LoRA calibration
- task-vector merge of the calibration delta into the best interpolated candidate

Gates:

- MT drop `<=1.0`
- SC and GC no-error accuracy improve
- correction F1 does not collapse
- MR does not regress
- overall improves or stays within 0.2 while fixing pathology

## Outcome

The tiny edit calibration did not solve no-error behavior. It preserved MT but left the model in an always-error edit regime:

| Candidate | Overall | MT | QA | SC | GC | MR | SC no-error | GC no-error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| prompt-only | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | 0.000 | 0.000 |
| reproduced Stage B | 33.628 | 44.094 | 48.428 | 35.876 | 33.493 | 6.250 | 0.000 | 0.000 |
| edit calibration tiny | 33.584 | 44.036 | 48.428 | 35.711 | 33.493 | 6.250 | 0.000 | 0.000 |
| selected merge | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 | 0.000 | 0.000 |

The selected merge improves SC aggregate relative to `edit_repair_tiny` and prompt-only, but the improvement comes from error-side detection/correction, not from no-error calibration. The raw audit for the selected merge shows:

- SC: 1167 rows, 597 clean rows, no-error accuracy `0.000`, malformed/verbose rate `0.010`.
- GC: 985 rows, 498 clean rows, no-error accuracy `0.000`, malformed/verbose rate `0.013`.
- The model predicts an edit for every SC and GC item.

Decision: edit calibration is not fixed. The selected model is stronger by WMT equal-weighted score and MR recovery, but future work must address the shared prompt/evaluator-level always-error edit behavior rather than more tiny repair on the same recipe.
