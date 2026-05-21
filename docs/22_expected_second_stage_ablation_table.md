# Expected Second-Stage Ablation Table

| System | Data mixture ID | Governance status | MT chrF++ | MT BLEU | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall | Notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Base Qwen prompt-only | none | official eval only | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Prompt-only |
| Official-only baseline | official_only | allowed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | No external |
| Official + Ukrainian MT external | uk_external_mt | allowed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | OPUS seed |
| Official + SC/GC external | edit_external | allowed/risky noted | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | UA-GEC/UD/monolingual |
| Official + QA generated | qa_generated | allowed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Public cloze MCQ |
| Official + MR preservation | mr_preservation | allowed/risky noted | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Non-benchmark math |
| External-enhanced multitask | uk_external_enhanced_v1 / sorbian_external_enhanced_v1 | passed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Task-balanced |
| Specialist merged model | merge_v1 | passed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Skill-vector merge |
| Merged + polish | final_polished | passed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Exact format |
