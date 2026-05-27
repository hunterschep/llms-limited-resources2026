# Final Salvage State

Current commit at phase start: `1839f6de8c2b861f99069ea13e235b5a931dd8e4`.

Current best Sorbian candidate:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10`

| Model | Overall | MT | QA | SC | GC | MR |
|---|---:|---:|---:|---:|---:|---:|
| prompt-only | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 |
| original Stage B | 32.826 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 |
| edit_repair_tiny | 33.177 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 |
| selected lineage merge | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 |

Selected merge deltas:

- `+5.222` overall vs prompt-only.
- `+1.591` overall vs original Stage B.
- `+1.240` overall vs `edit_repair_tiny`.

Selected merge MT directions:

| Direction | chrF++ |
|---|---:|
| de->hsb | 32.135 |
| de->dsb | 27.598 |
| hsb->de | 52.991 |
| dsb->de | 46.695 |
| hsb->dsb | 50.009 |
| dsb->hsb | 49.870 |

Known fatal weakness:

- SC no-error accuracy: `0.000`.
- GC no-error accuracy: `0.000`.
- The model predicts an edit for every SC/GC item.

Known strengths:

- MR recovered above prompt-only: `10.417` vs `8.333`.
- MT is strong: `44.035` average chrF++.
- Package dry-run passed during lineage recovery.
- Checkpoint lineage is preserved.
- Ukrainian remains frozen; prompt-only remains fallback.

WMT26 constraints preserved from the [official task page](https://www2.statmt.org/wmt26/limited-resources-llm.html) and [official GitHub](https://github.com/TUM-NLP/llms-limited-resources2026): one Qwen3.5-family <=2B model per submitted track, all five tasks per track, public/reproducible external data, no hidden test data, no WMT2025 test sets, and no original/translated/modified/derived [PolyMath](https://huggingface.co/datasets/Qwen/PolyMath).
