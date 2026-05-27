# Lineage Scale And Interpolation

Core experiment: find a point between Stage A and Stage B that keeps most Sorbian MT gain while recovering MR/edit behavior.

The lineage-preserving reproduction made the core surgery experiment possible. Adapter scale and StageA/StageB interpolation both showed a real MT/MR tradeoff curve, but the best full-eval candidate came from task-vector merging rather than raw interpolation.

## Adapter Scale Probe

| Scale | Overall | MT | QA | SC | GC | MR |
|---:|---:|---:|---:|---:|---:|---:|
| 0.20 | 31.672 | 35.726 | 47.799 | 37.333 | 33.333 | 4.167 |
| 0.30 | 32.186 | 37.671 | 48.428 | 37.333 | 33.333 | 4.167 |
| 0.40 | 32.379 | 39.408 | 48.428 | 36.559 | 33.333 | 4.167 |
| 0.50 | 32.790 | 40.555 | 47.799 | 38.095 | 33.333 | 4.167 |
| 0.60 | 32.955 | 41.258 | 47.170 | 38.845 | 33.333 | 4.167 |
| 0.70 | 32.987 | 41.423 | 47.170 | 38.845 | 33.333 | 4.167 |
| 0.80 | 34.216 | 42.771 | 47.799 | 38.845 | 33.333 | 8.333 |
| 0.90 | 33.967 | 43.606 | 47.799 | 38.845 | 33.333 | 6.250 |
| 1.00 | 34.466 | 44.142 | 48.428 | 38.095 | 33.333 | 8.333 |
| 1.10 | 34.204 | 44.366 | 48.428 | 36.559 | 33.333 | 8.333 |

Full eval of adapter scale `0.80` scored `33.957` overall with MT `42.829` and MR `10.417`. It beat `edit_repair_tiny`, but the task-vector merge retained more MT and overall.

## Parent/StageB Interpolation Probe

| Alpha | Overall | MT | QA | SC | GC | MR |
|---:|---:|---:|---:|---:|---:|---:|
| 0.20 | 31.234 | 35.572 | 46.541 | 36.559 | 33.333 | 4.167 |
| 0.30 | 31.741 | 38.104 | 46.541 | 36.559 | 33.333 | 4.167 |
| 0.40 | 32.458 | 39.173 | 49.057 | 36.559 | 33.333 | 4.167 |
| 0.50 | 32.921 | 40.715 | 49.057 | 37.333 | 33.333 | 4.167 |
| 0.60 | 33.040 | 41.178 | 48.428 | 38.095 | 33.333 | 4.167 |
| 0.70 | 33.307 | 41.566 | 46.541 | 38.845 | 33.333 | 6.250 |
| 0.80 | 33.929 | 42.679 | 47.799 | 39.583 | 33.333 | 6.250 |
| 0.90 | 34.085 | 44.318 | 48.428 | 38.095 | 33.333 | 6.250 |
| 1.00 | 34.494 | 44.280 | 48.428 | 38.095 | 33.333 | 8.333 |

The interpolation curve confirmed that the reproduced Stage B endpoint was not an accident: MT stays above `41.0` from alpha `0.60`, and MR begins recovering around alpha `0.70` and above. Failed interpolation model directories were deleted after manifesting because they are reproducible from the preserved Stage A and Stage B checkpoints.
