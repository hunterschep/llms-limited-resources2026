# Phase 3 Experiment Plan

This phase runs the WMT26 experimental campaign for Skill-Vector Merged Curriculum Adaptation. The goal is to produce trained checkpoints, all-five-task evaluations, merge-search evidence, polished final candidates, and submission-readiness artifacts.

## Rules Preserved

- One Qwen3.5-family model with 2B parameters or less per submitted track.
- Every submitted track must cover MT, QA, SC, GC, and MR.
- A track's five task outputs must come from the same model weights.
- External data must remain public and registered.
- No hidden WMT26 test data, WMT2025 test sets, Ukrainian UNLP/ZNO test splits, Ukrainian MMLU test splits, PolyMath or derivatives, or extra Sorbian certificate questions.

## Experiment Ladder

1. Sync the repository and generated local data to Andromeda.
2. Validate environment and governance remotely.
3. Prepare or verify data remotely.
4. Evaluate prompt-only Qwen3.5-2B.
5. Train official-only, naive multitask, task-balanced, and external-enhanced baselines.
6. Train language, MT, edit, QA, MR, and format specialists for Ukrainian and Sorbian.
7. Evaluate every checkpoint on all five tasks.
8. Run skill-vector merge search using equal-weighted WMT-style score.
9. Run small final format polish.
10. Evaluate polished and unpolished candidates.
11. Select one final model per track.
12. Prepare model cards, packaging notes, and system-description tables.

## Initial Andromeda Commands

```bash
rsync -avP --exclude .git/ /Users/hunterschep/llms-limited-resources2026/ andromeda:/home/scheppat/workspace/projects/wmt26_lrllm/
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/00_validate_env.slurm'
ssh andromeda 'cd /home/scheppat/workspace/projects/wmt26_lrllm && sbatch andromeda/jobs/01_prepare_data.slurm'
```

Default GPU jobs request H200. If queue time blocks progress, resubmit individual training jobs with `--gres=gpu:a100:1` or `--gres=gpu:l40s:1`.
