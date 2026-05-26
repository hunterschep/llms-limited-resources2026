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
