# Lineage Recovery Plan

Starting commit recorded from prior closeout: `4ee7665a6f122168c853c4dddf726f7e9ca3c6ab`.

This phase starts from the completed Stage-B rescue state. The best retained Sorbian model is `edit_repair_tiny`, but it is not final-competitive. The structural failure to fix now is checkpoint lineage: the original Stage B adapter exists, but its Stage A parent was pruned, so adapter-scale and parent/interpolation surgery could not be run safely.

## Current Scores

| Model | Overall | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| prompt-only Sorbian | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | baseline anchor |
| Stage B MT-large | 32.826 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 | MT breakthrough, MR weak |
| Stage B short-96 | 32.945 | 43.929 | 48.428 | 34.708 | 33.493 | 4.167 | diagnostic prompt setting |
| MR repair tiny | 32.799 | 43.404 | 48.428 | 34.708 | 33.289 | 4.167 | rejected/pruned |
| edit_repair_tiny | 33.177 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 | best retained, not final |
| Stage C replay | 21.250 | 43.790 | 47.170 | 7.098 | 1.942 | 6.250 | hard reject |

## Active Remote Artifacts

- Original Stage B: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/competitive_reboot/sorbian/stage_b_mt_large`
- Best retained rescue model: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/stage_b_rescue/sorbian/edit_repair_tiny`

The previous cleanup reduced Stage-B rescue checkpoint storage from 11G to 3.6G and left no Andromeda jobs queued/running. The validation set at closeout was `make validate`, `make smoke-test`, `make check-governance`, `make check-overlap`, `git diff --check`, and `python3 -m compileall scripts src`.

## Goal

Reproduce the Sorbian Stage A/Stage B path while preserving lineage, then use adapter scaling, parent/StageB interpolation, edit calibration, MR recovery, and task-vector merge to find a stronger candidate than `edit_repair_tiny`.

Success target:

- Beat `edit_repair_tiny` overall, preferably `>=34.195`.
- Keep MT strong, preferably `>=41.0`.
- Recover MR toward prompt-only `8.333`.
- Materially improve SC/GC no-error behavior.
- Keep one packageable Qwen3.5-family <=2B model.

Hard rejects:

- Failed Stage C replay recipe.
- Phase 3/4 checkpoints.
- Any checkpoint trained on forbidden data.
- Candidate with collapsed SC/GC or MR without a stronger WMT-relevant tradeoff.

## Source Constraints

Official constraints are from the [WMT26 task page](https://www2.statmt.org/wmt26/limited-resources-llm.html) and [official WMT26 GitHub](https://github.com/TUM-NLP/llms-limited-resources2026). The base remains [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B). Forbidden data includes original, translated, modified, or derived [PolyMath](https://huggingface.co/datasets/Qwen/PolyMath).

## Closeout

Lineage recovery produced a stronger Sorbian candidate:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10`

| Model | Overall | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| edit_repair_tiny | 33.177 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 | prior best |
| selected lineage merge | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 | new best |

The selected merge clears the preferred overall threshold `34.195`, keeps MT above `41.0`, and recovers MR above prompt-only. The important remaining caveat is SC/GC no-error behavior: no-error accuracy remains `0.000` for both SC and GC, matching the prompt-only and Stage B pathology.
