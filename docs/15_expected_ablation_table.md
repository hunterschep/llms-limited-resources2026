# Expected Ablation Table

Use this table shape in reports and system papers.

| System | MT chrF++ | MT BLEU | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Base Qwen3.5-2B | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Prompt-only base model |
| Prompt-only baseline | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Track/task prompts only |
| Official-train-only SFT | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Ukrainian QA or Sorbian MT official train |
| Naive multitask SFT | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Pooled train examples |
| Task-balanced SFT | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Equal/capped task sampling |
| Language acquisition only | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Instruction-preserving language curriculum |
| MT specialist | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Specialist, not submitted directly |
| SC/GC specialist | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Edit specialist |
| QA specialist | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | QA robustness |
| MR specialist | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Math preservation |
| Merged model: uniform soup | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Equal specialist weights |
| Merged model: weighted task arithmetic | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Merge search |
| Merged model: TIES merge | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Sign-conflict-aware merge |
| Merged + format polish | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Small exact-format pass |
| Final selected model | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Best locked-validation overall |

Overall is the equal-weighted mean of MT, QA, SC, GC, and MR scores using the internal 0-100 convention.
