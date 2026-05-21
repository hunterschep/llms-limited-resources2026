# Results Tables

Status: pending remote training and evaluation.

## Baselines

| Track | Model | MT chrF++ | MT BLEU | QA acc | SC det F1 | SC corr F1 | GC det F1 | GC corr F1 | MR acc | Overall |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ukrainian | Qwen3.5-2B prompt-only | 41.135 | 18.226 | 33.994 | 66.667 | 26.667 | 65.993 | 5.941 | 4.167 | 32.386 |
| Ukrainian | official-only SFT | 41.169 | 17.610 | 40.793 | 66.667 | 1.987 | 65.993 | 0.000 | 0.000 | 29.857 |

## Specialists

| Track | Model | MT | QA | SC | GC | MR | Overall | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Ukrainian | M_lang | 41.583 | 30.878 | 56.271 | 35.967 | 0.000 | 32.940 | Improves MT/SC over prompt-only but MR collapses on this local eval. |

## Merge Search

| Track | Method | Weights | MT | QA | SC | GC | MR | Overall | Selected |
|---|---|---|---:|---:|---:|---:|---:|---:|---|

## Final Polish

| Track | Candidate | Before Overall | After Overall | Invalid Output Change | Selected |
|---|---|---:|---:|---:|---|
