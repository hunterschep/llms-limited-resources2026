# Phase 3 Sanity Gates

Status reflects local/parser/data gates. GPU overfit/checkpoint-loading gates are recorded from Andromeda runs when available.

- Oracle evaluator: `PASS` Gold targets must score perfectly on QA/MR/SC/GC.
- Data sanity: `PASS` Final SC/GC balance and MR target parseability must pass.
- Edit balance: `PASS` Clean/error SC/GC mixtures must be close to balanced.
- MR data quality: `PASS` MR normalization probes and train targets must pass.

Required remote gates before merge search:

- Compact SC/GC/MR overfit for both tracks.
- Checkpoint-loading comparison for retrained candidates.
- Raw prediction dumps for retrained candidates before final evaluation.

## Current Data Sanity

- `sorbian GC`: rows=1875 error=966 clean=909 clean_ratio=0.485
- `sorbian MR`: rows=312 non_numeric_targets=0
- `sorbian SC`: rows=5757 error=2998 clean=2759 clean_ratio=0.479
- `uk GC`: rows=7062 error=3531 clean=3531 clean_ratio=0.500
- `uk MR`: rows=315 non_numeric_targets=0
- `uk SC`: rows=9009 error=4506 clean=4503 clean_ratio=0.500
