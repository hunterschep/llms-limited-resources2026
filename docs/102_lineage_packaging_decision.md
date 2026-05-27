# Lineage Packaging Decision

Packaging dry-run is cleared for the selected lineage-recovery Sorbian candidate.

Selected checkpoint:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10`

Selected score:

| Overall | MT | QA | SC | GC | MR |
|---:|---:|---:|---:|---:|---:|
| 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 |

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

Dry-run status:

- `scripts/lineage_package_candidate.py --dry-run`: passed.
- `scripts/lineage_validate_package.py`: passed.
- Required files checked: `config.json`, `tokenizer_config.json`.
- Public upload: not performed.

Known package risk:

- The selected checkpoint is packageable as one model, but SC/GC no-error behavior remains unresolved. The model predicts an edit for every SC/GC locked-validation item.

Do not upload publicly without explicit approval.
