# Final Submission Decision

Decision: submit Sorbian only if we accept the SC/GC hidden-test no-error risk. Do not submit a trained Ukrainian model.

Sorbian recommendation:

- Recommended package: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian_primary_package/`
- Model path: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian_primary_package/model`
- Decision label: `higher_local_score_risky`
- Public upload: not performed.

Scores:

| Model | Overall | MT | QA | SC | GC | MR | SC no-error | GC no-error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| prompt-only | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | 0.000 | 0.000 |
| selected lineage merge | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 | 0.000 | 0.000 |

Why submit Sorbian fallback:

- It is the only packageable model with a real full-eval improvement: `+5.222` overall over prompt-only.
- It has a strong MT gain: `+16.558` MT over prompt-only.
- It recovers MR above prompt-only.

Why this is risky:

- SC/GC no-error behavior is not fixed.
- Prompt and tiny model calibration did not produce a usable fix.
- Hidden test with many clean edit examples could punish false positives.

Ukrainian recommendation:

- Do not submit a trained Ukrainian checkpoint.
- If participating in Ukrainian is strategically required, submit prompt-only Qwen3.5-2B as a fallback baseline and label it honestly.

WMT26 compliance:

- Same Sorbian model for MT, QA, SC, GC, MR.
- Qwen3.5-family <=2B.
- No task-specific adapter switching.
- No live retrieval.
- No public upload without human approval.
- Forbidden data sources remain excluded, including PolyMath and WMT2025 test sets.

Human approval needed:

- Decide whether the Sorbian hidden-test SC/GC no-error risk is acceptable.
- Decide whether to submit Ukrainian prompt-only baseline or skip Ukrainian.
