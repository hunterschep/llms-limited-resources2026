# Competitive Reboot Results And Decision

## Executive Summary

The competitive reboot produced a real Sorbian MT signal but no final submission-ready model.

Ukrainian remains blocked: real-data MT training improved MT by about `+1` chrF++ and QA by roughly `+3.7` to `+4.8`, but GC/MR regressions kept every trained checkpoint below prompt-only.

Sorbian Stage B is the first meaningful trained checkpoint in the project: average MT chrF++ improved from `27.477` to `43.335` (`+15.858`) and overall improved from `29.195` to `32.826` (`+3.631`). This beats the Phase 4 tiny adapter by a large margin on MT and by `+3.032` overall, but it misses the `+5` overall first milestone because MR drops from `8.333` to `4.167`. Stage C replay preserved MT but collapsed SC/GC, so it is disqualified.

## Ukrainian Results

| Model | Overall | Delta | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only Qwen3.5-2B | 37.399 | 0.000 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 | fallback |
| Stage A MT real-large | 34.636 | -2.763 | 41.889 | 37.960 | 38.825 | 33.672 | 20.833 | failed |
| Stage B instruction replay | 28.078 | -9.321 | 41.999 | 39.093 | 29.344 | 4.954 | 25.000 | failed |
| Stage C doc/format | 31.556 | -5.843 | 41.979 | 38.810 | 45.106 | 11.053 | 20.833 | failed |

Decision: keep prompt-only as the Ukrainian fallback. Delete trained Ukrainian checkpoints after manifesting, because none is competitive or needed for merge.

## Sorbian Results

| Model | Overall | Delta | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| prompt-only Qwen3.5-2B | 29.195 | 0.000 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | fallback |
| Phase 4 tiny adapter | 29.794 | +0.599 | 27.561 | 42.138 | 33.685 | 33.084 | 12.500 | failed_for_competitive_purposes |
| Stage A DAPT | 30.067 | +0.871 | 26.765 | 51.572 | 34.539 | 33.289 | 4.167 | aux_strong_MT_flat |
| Stage B MT-large | 32.826 | +3.631 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 | promising_but_needs_replay |
| Stage C instruction replay | 21.250 | -7.945 | 43.790 | 47.170 | 7.098 | 1.942 | 6.250 | failed |

Decision: preserve Sorbian Stage B as the only active competitive-reboot checkpoint. It is not final-packageable yet, but it is the first checkpoint with WMT25-like MT movement.

## Sorbian Stage B Direction Breakdown

| Direction | Prompt-only chrF++ | Stage B chrF++ | Delta |
|---|---:|---:|---:|
| de->hsb | 11.991 | 31.451 | +19.460 |
| de->dsb | 11.970 | 27.779 | +15.809 |
| hsb->de | 32.310 | 52.113 | +19.802 |
| dsb->de | 26.907 | 45.884 | +18.977 |
| hsb->dsb | 39.724 | 48.352 | +8.628 |
| dsb->hsb | 42.459 | 49.880 | +7.421 |

## Merge And Polish Decision

Merge search remains blocked. Stage B is a strong Sorbian MT/language checkpoint, but there is not yet a second complementary, validated checkpoint that repairs MR without damaging SC/GC. Stage C proves the current replay recipe is unsafe.

Final polish remains blocked. Polish should not run on Ukrainian failed checkpoints, Sorbian Stage A, or Sorbian Stage C. Sorbian Stage B needs a targeted MR/edit replay repair or base interpolation check before any format polish.

## Artifact Decision

Preserved:

- Sorbian Stage B checkpoint:
  `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large`
- Result JSONs and compact summaries under `results/competitive_reboot/`.
- Remote raw prediction JSONLs under the Andromeda project results tree for inspection.

Deleted remotely after manifesting:

- Ukrainian Stage A, Stage B, and Stage C checkpoints.
- Sorbian Stage A and Stage C checkpoints.

Storage:

- Remote competitive checkpoint storage before cleanup: 22G.
- Remote competitive checkpoint storage after cleanup: 3.7G.

## Next Research Move

Do not rerun broad SFT. The next experiment should start from Sorbian Stage B and test narrow repair mechanisms:

1. Base interpolation or adapter scale against Stage B to recover MR while preserving most MT.
2. Small MR-only final-answer replay with high base-preservation weight.
3. Official-style SC/GC replay calibrated to avoid the Stage C edit collapse.
4. Evaluate each repair against prompt-only and Stage B, with Stage B MT direction scores as the no-regression anchor.
