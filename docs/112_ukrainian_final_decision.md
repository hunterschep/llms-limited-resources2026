# Ukrainian Final Decision

Decision: do not submit a trained Ukrainian model from this repo state.

| Model | Overall | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| prompt-only Qwen3.5-2B | 37.399 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 | Fallback baseline only. |
| best trained Stage A | 34.636 | 41.889 | 37.960 | 38.825 | 33.672 | 20.833 | Reject: overall, SC, and MR regress. |

No Ukrainian training was run in final salvage. If a Ukrainian track submission is required, use prompt-only Qwen3.5-2B as a clearly labeled fallback baseline. Otherwise, recommend submitting only Sorbian.
