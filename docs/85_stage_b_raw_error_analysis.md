# Stage B Raw Error Analysis

Generated at commit `2c30c192934506d15864e4ad2f1d0a8a71d1eaa0`.

## Inputs

Raw prediction JSONLs were copied from Andromeda for this audit, summarized locally, and then pruned from the local repo. The preserved compact artifacts are:

- `results/stage_b_rescue/error_analysis/stage_b_raw_error_analysis_summary.json`
- `results/stage_b_rescue/error_analysis/stage_b_mr_audit.jsonl`
- `results/stage_b_rescue/error_analysis/stage_b_edit_audit.json`
- `results/stage_b_rescue/error_analysis/stage_b_mt_regression_audit.json`

Remote raw inputs remain under `/home/scheppat/workspace/projects/wmt26_lrllm/results/competitive_reboot/eval/sorbian/` and `/home/scheppat/workspace/projects/wmt26_lrllm/results/stage_b_rescue/` if another audit needs to be rerun.

## MR Diagnosis

The MR set is tiny, so the Stage B drop from `8.333` to `4.167` is likely one additional locked-validation miss. It still matters because MR is equally weighted.

| model | correct | verbose_or_explanation | wrong_final_numeric_answer |
|---|---|---|---|
| prompt_only_qwen35_2b | 4 | 12 | 32 |
| stage_b_mt_large | 2 | 5 | 41 |
| stage_c_instruction_replay | 3 | 7 | 38 |

## SC/GC Diagnosis

### SC
| model | pred_error | tp | fp | fn | tn | no_error_acc | malformed | rewrite | correction_exact |
|---|---|---|---|---|---|---|---|---|---|
| prompt_only_qwen35_2b | 1167 | 570 | 597 | 0 | 0 | 0.000 | 0.087 | 0.049 | 5 |
| stage_b_mt_large | 1167 | 570 | 597 | 0 | 0 | 0.000 | 0.000 | 0.021 | 11 |
| stage_c_instruction_replay | 82 | 44 | 38 | 526 | 559 | 0.936 | 0.000 | 0.000 | 2 |

### GC
| model | pred_error | tp | fp | fn | tn | no_error_acc | malformed | rewrite | correction_exact |
|---|---|---|---|---|---|---|---|---|---|
| prompt_only_qwen35_2b | 985 | 487 | 498 | 0 | 0 | 0.000 | 0.021 | 0.013 | 0 |
| stage_b_mt_large | 985 | 487 | 498 | 0 | 0 | 0.000 | 0.067 | 0.027 | 2 |
| stage_c_instruction_replay | 28 | 10 | 18 | 477 | 480 | 0.964 | 0.000 | 0.000 | 0 |

## MT Diagnosis

| direction | examples | prompt_chrf | stage_b_chrf | delta |
|---|---|---|---|---|
| de->dsb | 1204 | 16.846 | 33.260 | 16.414 |
| de->hsb | 1231 | 18.244 | 39.112 | 20.868 |
| dsb->de | 1204 | 29.268 | 49.675 | 20.406 |
| dsb->hsb | 1167 | 51.027 | 57.241 | 6.214 |
| hsb->de | 1231 | 37.324 | 58.108 | 20.783 |
| hsb->dsb | 1167 | 48.214 | 56.110 | 7.895 |

## Training Implication

- Keep Stage B as the MT anchor.
- Do not reuse Stage C replay: it preserved MT but collapsed edit detection.
- Repair MR with final-answer-only examples plus MT anchor replay.
- Repair edit behavior with hard no-error and one-word correction rows; keep the repair tiny and gated.
