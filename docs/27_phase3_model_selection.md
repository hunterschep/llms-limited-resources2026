# Phase 3 Model Selection

Status: paused pending triage. Merge search and polish are blocked until evaluator/raw-output/overfit/checkpoint-loading remediation passes.

## Selection Rule

Primary criterion: highest overall equal-weighted locked-validation score.

Tie-breakers:

- fewer invalid outputs
- less task collapse
- stronger SC/GC exactness
- stronger QA/MR preservation
- simpler model lineage
- cleaner governance
- easier packaging

## Current Selections

| Track | Selected Checkpoint | Status | Rationale |
|---|---|---|---|
| Ukrainian |  | pending | Awaiting baselines, specialists, merge search, and polish. |
| Sorbian |  | pending | Awaiting baselines, specialists, merge search, and polish. |

## Pause Rationale

Do not select or merge a final model from the current partial results. Ukrainian M_mt is promising overall, and Sorbian M_lang improves MT, but systematic MR collapse and suspicious SC/GC detection behavior make the current objective signal unreliable. Resume model selection only after the triage gates in `docs/33_phase3_triage_remediation.md` pass.
