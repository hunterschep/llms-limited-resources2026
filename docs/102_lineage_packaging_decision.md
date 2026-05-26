# Lineage Packaging Decision

Packaging is blocked until lineage recovery produces a candidate stronger than `edit_repair_tiny`, or until the project explicitly decides that `edit_repair_tiny` remains the best available model.

Requirements:

- one model
- Qwen3.5-family <=2B
- no per-task adapter switching
- no live RAG
- no forbidden data
- tokenizer/config/generation config included
- data statement included
- contamination statement included
- eval table included
- exact commands included
- package loads with Transformers
- package can run all five Sorbian tasks

Do not upload publicly without explicit approval.
