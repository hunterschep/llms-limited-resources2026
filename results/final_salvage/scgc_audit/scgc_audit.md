# Final Salvage SC/GC Audit

## prompt_only

| Task | Total | Gold error | Gold CORRECT | Pred error | Pred CORRECT | No-error acc | Det F1 | Corr F1 | Malformed | Multi-edit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GC | 985 | 487 | 498 | 985 | 0 | 0.000 | 0.662 | 0.000 | 0.000 | 0.334 |
| SC | 1167 | 570 | 597 | 1167 | 0 | 0.000 | 0.656 | 0.017 | 0.000 | 0.709 |

## selected_lineage_merge

| Task | Total | Gold error | Gold CORRECT | Pred error | Pred CORRECT | No-error acc | Det F1 | Corr F1 | Malformed | Multi-edit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GC | 985 | 487 | 498 | 985 | 0 | 0.000 | 0.662 | 0.008 | 0.013 | 0.001 |
| SC | 1167 | 570 | 597 | 1167 | 0 | 0.000 | 0.656 | 0.058 | 0.001 | 0.129 |

## edit_repair_tiny

| Task | Total | Gold error | Gold CORRECT | Pred error | Pred CORRECT | No-error acc | Det F1 | Corr F1 | Malformed | Multi-edit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GC | 985 | 487 | 498 | 985 | 0 | 0.000 | 0.662 | 0.008 | 0.037 | 0.007 |
| SC | 1167 | 570 | 597 | 1167 | 0 | 0.000 | 0.656 | 0.031 | 0.000 | 0.004 |

## reproduced_stage_b

| Task | Total | Gold error | Gold CORRECT | Pred error | Pred CORRECT | No-error acc | Det F1 | Corr F1 | Malformed | Multi-edit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GC | 985 | 487 | 498 | 985 | 0 | 0.000 | 0.662 | 0.008 | 0.010 | 0.002 |
| SC | 1167 | 570 | 597 | 1167 | 0 | 0.000 | 0.656 | 0.061 | 0.000 | 0.133 |

## Diagnosis

- Dominant failure: the evaluated models predict an edit for essentially every SC/GC item.
- Parser misclassification is not the main issue; raw outputs are usually parseable two-line edit outputs.
- The failure is consistent with a strong generation/training prior toward finding an error even when the target is CORRECT/CORRECT.
- Official WMT26 SC/GC descriptions include no-error sentences, so this is a hidden-test risk.
