# Lineage Task-Vector Merge

Task-vector merge is allowed only after lineage-preserved deltas exist. Failed Stage C is excluded.

Candidate deltas:

- `Delta_mt = StageB_MT - StageA_parent`
- `Delta_edit = EditCalibration - CandidateParent`
- `Delta_mr = MRRecovery - CandidateParent`
- `Delta_format = FormatCalibration - CandidateParent`, if available

Search:

- `M = StageA_parent + a Delta_mt`
- `M = StageA_parent + a Delta_mt + b Delta_edit`
- `M = StageA_parent + a Delta_mt + c Delta_mr`
- `M = StageA_parent + a Delta_mt + b Delta_edit + c Delta_mr`

Coefficients:

- `a in [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]`
- `b in [0.05, 0.10, 0.20, 0.30]`
- `c in [0.05, 0.10, 0.20, 0.30]`

Full eval only top 3-5 probe candidates.

Success target:

- overall above `edit_repair_tiny` `33.177`
- preferred overall `>=34.195`
- MT `>=41.0` preferred, `>=39.0` acceptable if overall improves strongly
- MR `>=8.333` preferred
- SC/GC no-error behavior materially improved

## Outcome

Task-vector merging produced the best lineage-recovery candidate.

Probe search top candidates:

| Candidate | Overall | MT | QA | SC | GC | MR |
|---|---:|---:|---:|---:|---:|---:|
| `mt1p00_edit0p10_mr0p10` | 34.904 | 44.248 | 48.428 | 38.095 | 33.333 | 10.417 |
| `mt1p00_edit0p10_mr0p05` | 34.867 | 44.065 | 48.428 | 38.095 | 33.333 | 10.417 |
| `mt0p90_edit0p05_mr0p05` | 34.296 | 43.920 | 47.799 | 38.095 | 33.333 | 8.333 |

The top probe candidate was full-evaluated and selected:

| Candidate | Overall | MT | QA | SC | GC | MR | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| `mt1p00_edit0p10_mr0p10` | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 | selected |

This is:

- `+5.222` overall versus prompt-only.
- `+1.591` overall versus original Stage B.
- `+1.240` overall versus `edit_repair_tiny`.
- `+16.558` MT versus prompt-only.
- `+4.167` MR versus `edit_repair_tiny`.

Failed task-vector probe model directories were deleted after manifesting. The selected merged checkpoint remains at:

`/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10`

Limit: task-vector merging did not fix SC/GC no-error behavior. The candidate is selected because it clears the overall target, preserves MT, and recovers MR above prompt-only.
