# Lineage Recovery Results

Lineage recovery produced a stronger Sorbian candidate than `edit_repair_tiny`.

Selected checkpoint:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10`

## Full Evaluation

| Model | Overall | Delta vs prompt | Delta vs Stage B | Delta vs edit_repair | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only | 29.195 | 0.000 | -3.631 | -3.982 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | baseline |
| original Stage B | 32.826 | +3.631 | 0.000 | -0.351 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 | MT anchor |
| edit_repair_tiny | 33.177 | +3.982 | +0.351 | 0.000 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 | prior best |
| reproduced Stage B | 33.628 | +4.433 | +0.802 | +0.451 | 44.094 | 48.428 | 35.876 | 33.493 | 6.250 | lineage reproduced |
| adapter scale 0.80 | 33.957 | +4.762 | +1.131 | +0.780 | 42.829 | 47.170 | 35.876 | 33.493 | 10.417 | MR recovered, lower MT |
| edit calibration tiny | 33.584 | +4.389 | +0.758 | +0.407 | 44.036 | 48.428 | 35.711 | 33.493 | 6.250 | edit aggregate improved, MR weak |
| selected task-vector merge | 34.417 | +5.222 | +1.591 | +1.240 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 | selected |

## MT Direction Breakdown

| Direction | Prompt-only chrF++ | Original Stage B chrF++ | Selected merge chrF++ | Selected delta vs prompt |
|---|---:|---:|---:|---:|
| de->hsb | 11.991 | 31.451 | 32.135 | +20.144 |
| de->dsb | 11.970 | 27.779 | 27.598 | +15.628 |
| hsb->de | 32.310 | 52.113 | 52.991 | +20.681 |
| dsb->de | 26.907 | 45.884 | 46.695 | +19.788 |
| hsb->dsb | 39.724 | 48.352 | 50.009 | +10.285 |
| dsb->hsb | 42.459 | 49.880 | 49.870 | +7.411 |

The selected merge preserves the Stage B MT breakthrough: average MT is `44.035`, which is `+16.558` over prompt-only and above the `41.0` rescue floor.

## Diagnostics

- MR recovered to `10.417`, above prompt-only `8.333`.
- SC aggregate improved over prompt-only and `edit_repair_tiny`, but no-error behavior did not improve.
- SC no-error accuracy remains `0.000`; GC no-error accuracy remains `0.000`.
- The selected model predicts an edit for every SC/GC item, matching the prompt-only always-error pathology.
- Package dry-run passed; no public upload was performed.

Decision: `mt1p00_edit0p10_mr0p10` is the best current Sorbian lineage-recovery candidate. It clears the +5 overall target and recovers MR, but it should be carried forward with an explicit edit no-error risk.
