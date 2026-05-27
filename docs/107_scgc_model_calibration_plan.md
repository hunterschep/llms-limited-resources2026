# SC/GC Model Calibration Plan

Final salvage trained one tiny assistant-only LoRA from the selected lineage merge to try to teach CORRECT/CORRECT behavior without broad replay.

Training base:

```text
/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10
```

Config:

```text
configs/train/final_salvage/scgc_calibration_tiny.yaml
```

Data:

- clean/error SC/GC calibration rows from governed lineage edit data
- hard no-error rows
- one-token SC/GC positives
- small MT, QA, and MR anchors
- no locked validation
- no Stage C replay
- no extra certificate questions
- no forbidden PolyMath

Executed result:

- Tiny calibration SFT completed successfully.
- Merge coefficients tested: `0.05`, `0.10`, `0.15`, `0.20`, `0.30`, `0.50`, `1.00`.
- Failed calibration checkpoints were deleted after manifesting.

Probe outcome:

| Candidate | Overall | MT | QA | SC | GC | MR | SC no-error | GC no-error | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| scgc_alpha_0p05 | 33.806 | 42.296 | 49.057 | 38.095 | 33.333 | 6.250 | 0.000 | 0.000 | Reject. |
| scgc_alpha_0p10 | 33.652 | 42.156 | 48.428 | 38.095 | 33.333 | 6.250 | 0.000 | 0.000 | Reject. |
| scgc_alpha_0p15 | 33.950 | 42.187 | 47.799 | 38.095 | 33.333 | 8.333 | 0.000 | 0.000 | Reject. |
| scgc_alpha_0p20 | 33.671 | 42.249 | 48.428 | 38.095 | 33.333 | 6.250 | 0.000 | 0.000 | Reject. |
| scgc_alpha_0p30 | 33.548 | 42.263 | 47.799 | 38.095 | 33.333 | 6.250 | 0.000 | 0.000 | Reject. |
| scgc_alpha_0p50 | 33.639 | 42.091 | 48.428 | 38.095 | 33.333 | 6.250 | 0.000 | 0.000 | Reject. |
| scgc_alpha_1p00 | 33.655 | 42.170 | 48.428 | 38.095 | 33.333 | 6.250 | 0.000 | 0.000 | Reject. |

The model-level calibration did not fix no-error behavior at any coefficient.
