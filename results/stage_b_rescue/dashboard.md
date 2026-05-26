# Stage B Rescue Dashboard

## Current Best

`edit_repair_tiny` is the current best rescued Sorbian checkpoint:

- Overall: `33.177`
- Delta vs prompt-only: `+3.982`
- Delta vs Stage B: `+0.351`
- MT: `43.345`
- QA: `48.428`
- SC: `34.370`
- GC: `33.493`
- MR: `6.250`

It is better than Stage B, but not yet a final competitive candidate because overall is below the `+5` target and MR remains below prompt-only.

## Full Evaluation

| Model | Overall | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| prompt-only | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | fallback |
| Stage B MT-large | 32.826 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 | MT_anchor |
| Stage B short-96 | 32.945 | 43.929 | 48.428 | 34.708 | 33.493 | 4.167 | rejected_MR_not_repaired |
| MR repair tiny | 32.799 | 43.404 | 48.428 | 34.708 | 33.289 | 4.167 | rejected_full_eval_no_gain |
| edit repair tiny | 33.177 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 | promising_needs_more_repair |
| Stage C replay | 21.250 | 43.790 | 47.170 | 7.098 | 1.942 | 6.250 | rejected_edit_collapse |

## Cleanup

Kept checkpoints:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/sorbian/edit_repair_tiny`

Deleted checkpoints:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/sorbian/mr_repair_tiny`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/sorbian/combined_repair_tiny`

Remote Stage-B rescue checkpoint storage after cleanup: `3.6G`.
