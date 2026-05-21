# Phase 3 Sanity Gates

Status: all remediation sanity gates completed.

- Oracle evaluator: `PASS` Gold targets must score perfectly on QA/MR/SC/GC.
- Data sanity: `PASS` Final SC/GC balance and MR target parseability must pass.
- Edit balance: `PASS` Clean/error SC/GC mixtures must be close to balanced.
- MR data quality: `PASS` MR normalization probes and train targets must pass.
- Compact overfit: `PASS` Same-set SC/GC/MR overfit must pass for both tracks.

Remote gates:

- Checkpoint-loading comparison for retrained candidates: `PASS`, job `2462274`.
- Ukrainian raw prediction dumps: `PASS`, job `2462365`.
- Sorbian raw prediction dumps: `PASS`, job `2462366`.

Passing sanity gates means the pipeline is coherent enough to interpret the fixed results. It does not mean the fixed checkpoints are merge-eligible; merge eligibility is blocked in `docs/42_phase3_resume_or_block_merge_decision.md`.

## Current Data Sanity

- `sorbian GC`: rows=1875 error=966 clean=909 clean_ratio=0.485
- `sorbian MR`: rows=312 non_numeric_targets=0
- `sorbian SC`: rows=5757 error=2998 clean=2759 clean_ratio=0.479
- `uk GC`: rows=7062 error=3531 clean=3531 clean_ratio=0.500
- `uk MR`: rows=315 non_numeric_targets=0
- `uk SC`: rows=9009 error=4506 clean=4503 clean_ratio=0.500

## Compact Overfit Gate

- `uk SC`: `PASS` detection_f1=1.000 correction_f1=0.897
- `uk GC`: `PASS` detection_f1=0.914 correction_f1=0.933
- `uk MR`: `PASS` accuracy=1.000
- `sorbian SC`: `PASS` detection_f1=0.867 correction_f1=0.897
- `sorbian GC`: `PASS` detection_f1=0.903 correction_f1=0.933
- `sorbian MR`: `PASS` accuracy=1.000
