# Results Tables

Status: partial remote evaluation in progress.

## Baselines

| Track | Model | MT chrF++ | MT BLEU | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ukrainian | Qwen3.5-2B prompt-only | 41.135 | 18.226 | 33.994 | 66.667 | 26.667 | 65.993 | 5.941 | 4.167 | 32.386 |
| Sorbian | Qwen3.5-2B prompt-only | 27.527 | 5.355 | 43.396 | 65.630 | 1.739 | 66.168 | 0.000 | 0.000 | 27.539 |
| Ukrainian | official-only SFT | 41.169 | 17.610 | 40.793 | 66.667 | 1.987 | 65.993 | 0.000 | 0.000 | 29.857 |
| Ukrainian | naive multitask SFT | 39.616 | 15.943 | 36.827 | 66.667 | 40.957 | 55.401 | 1.351 | 0.000 | 31.726 |
| Ukrainian | task-balanced SFT | 39.136 | 15.859 | 36.827 | 66.817 | 36.612 | 64.059 | 3.344 | 0.000 | 32.276 |
| Ukrainian | external-enhanced multitask SFT | 39.505 | 16.309 | 37.394 | 66.667 | 39.247 | 65.993 | 2.685 | 0.000 | 32.839 |
| Sorbian | official-only SFT | 27.261 | 5.524 | 44.654 | 65.591 | 0.000 | 66.213 | 0.000 | 0.000 | 27.563 |

## Specialists

| Track | Model | MT | QA | SC | GC | MR | Overall | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Ukrainian | M_lang | 41.583 | 30.878 | 56.271 | 35.967 | 0.000 | 32.940 | Improves MT/SC over prompt-only but MR collapses on this local eval. |
| Ukrainian | M_mt | 38.358 | 38.810 | 56.470 | 39.067 | 0.000 | 34.541 | Improves overall through QA/SC/GC transfer, but MT chrF++ drops below prompt-only and MR collapses. |
| Ukrainian | M_edit | 39.204 | 30.312 | 46.917 | 34.007 | 0.000 | 30.088 | Does not improve the intended edit aggregate over prompt-only enough to offset MT/QA/MR loss. |
| Ukrainian | M_qa | 40.995 | 36.827 | 54.233 | 34.997 | 0.000 | 33.410 | Improves overall and preserves MT better than M_mt, but still collapses MR. |
| Ukrainian | M_mr | 40.795 | 35.694 | 34.978 | 33.336 | 0.000 | 28.961 | Does not preserve MR on locked validation and damages SC correction. |
| Sorbian | M_lang | 30.818 | 36.478 | 32.990 | 33.061 | 0.000 | 26.669 | Improves MT over prompt-only but loses QA/SC enough to lower overall. |

## Merge Search

| Track | Method | Weights | MT | QA | SC | GC | MR | Overall | Selected |
|---|---|---|---:|---:|---:|---:|---:|---:|---|

## Final Polish

| Track | Candidate | Before Overall | After Overall | Invalid Output Change | Selected |
|---|---|---:|---:|---:|---|
