# Competitive Reboot Dashboard

## Status

- Competitive reboot data pipeline completed on Andromeda.
- Ukrainian stagewise training completed through Stage C; no Ukrainian checkpoint is competitive.
- Sorbian stagewise training completed through Stage C; Stage B is a strong MT checkpoint but not a final packageable model.
- Merge search remains blocked: only one strong valid vector exists, and it has unresolved MR tradeoff.
- Final polish remains blocked: no checkpoint is both overall-competitive and auxiliary-stable.

## Data Scale

### Ukrainian

- `stage_a_mt_real_large`: 390,411 rows; MT 385,480; LANG 4,600; FORMAT 331.
- `stage_b_instruction_replay`: 246,625 rows; MT 209,898; QA 15,884; SC 11,149; GC 9,354; MR 340.
- `stage_c_doc_format`: 242,222 rows; MT 240,994; FORMAT 1,228.
- `stagewise_all`: 879,258 rows.

### Sorbian

- `stage_a_dapt_large`: 296,543 rows; LANG 293,730; QA 2,495; FORMAT 318.
- `stage_b_mt_large`: 446,001 rows; MT 380,001; LANG 66,000.
- `stage_c_instruction_replay`: 186,859 rows; MT 174,000; SC 6,803; GC 2,877; QA 2,851; MR 328.
- `stage_d_format`: 81,509 rows; MT 80,000; FORMAT 1,509.
- `stagewise_all`: 1,010,912 rows.

## Ukrainian Evaluation

Prompt-only baseline: overall 37.399.

| Model | Overall | Delta | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only Qwen3.5-2B | 37.399 | 0.000 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 | fallback |
| Stage A MT real-large | 34.636 | -2.763 | 41.889 | 37.960 | 38.825 | 33.672 | 20.833 | failed; small MT/QA signal, MR/SC regression |
| Stage B instruction replay | 28.078 | -9.321 | 41.999 | 39.093 | 29.344 | 4.954 | 25.000 | failed; GC collapse |
| Stage C doc/format | 31.556 | -5.843 | 41.979 | 38.810 | 45.106 | 11.053 | 20.833 | failed; GC/MR damage |

Ukrainian conclusion: real-data MT training moved MT by about +1 chrF++ and improved QA, but the gains are not large enough to offset GC/MR damage. Prompt-only remains the Ukrainian fallback.

## Sorbian Evaluation

Prompt-only baseline: overall 29.195.

| Model | Overall | Delta | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only Qwen3.5-2B | 29.195 | 0.000 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | fallback |
| Phase 4 tiny adapter | 29.794 | +0.599 | 27.561 | 42.138 | 33.685 | 33.084 | 12.500 | failed for competitive purposes |
| Stage A DAPT | 30.067 | +0.871 | 26.765 | 51.572 | 34.539 | 33.289 | 4.167 | aux-strong, MT flat/down |
| Stage B MT-large | 32.826 | +3.631 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 | promising_but_needs_replay |
| Stage C instruction replay | 21.250 | -7.945 | 43.790 | 47.170 | 7.098 | 1.942 | 6.250 | failed; edit collapse |

Sorbian conclusion: Stage B validates the strategic reset with a large MT gain and positive overall movement, but it misses the +5 overall target and MR remains below prompt-only. Preserve Stage B as the only active checkpoint; block packaging until MR/replay is repaired.

## Sorbian Stage B MT Directions

| Direction | Prompt-only chrF++ | Stage B chrF++ | Delta |
|---|---:|---:|---:|
| de->hsb | 11.991 | 31.451 | +19.460 |
| de->dsb | 11.970 | 27.779 | +15.809 |
| hsb->de | 32.310 | 52.113 | +19.802 |
| dsb->de | 26.907 | 45.884 | +18.977 |
| hsb->dsb | 39.724 | 48.352 | +8.628 |
| dsb->hsb | 42.459 | 49.880 | +7.421 |

## Artifact Hygiene

- Remote checkpoint storage before cleanup: 22G.
- Remote checkpoint storage after cleanup: 3.7G.
- Deleted failed remote checkpoints:
  - Ukrainian Stage A, Stage B, Stage C.
  - Sorbian Stage A and Stage C.
- Preserved remote checkpoint:
  - `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large`
- Cleanup manifest:
  - `results/competitive_reboot/cleanup/andromeda_checkpoint_cleanup_20260526T102858Z.txt`

## Files

- Ukrainian comparison: `results/competitive_reboot/comparisons/uk_competitive_comparison.md`
- Sorbian comparison: `results/competitive_reboot/comparisons/sorbian_competitive_comparison.md`
- Sorbian Stage B direction breakdown: `results/competitive_reboot/comparisons/sorbian_stage_b_direction_breakdown.md`
- Compact raw-output summaries: `results/competitive_reboot/error_analysis/`
