# Phase 3 Triage Findings

Date: 2026-05-21

Phase 3 training remains paused. The current evidence points to pipeline/data-mixture problems, not a failed research approach.

## Jobs Run

- `2462198` `triage_oracle`: completed. Oracle evaluation passed.
- `2462212` `triage_raw_uk`: completed on L40S. Dumped 20 examples per task for base, Ukrainian baselines, and Ukrainian specialists.
- `2462219` `triage_raw_sorbian`: canceled after base Sorbian evidence because full 20-example sweep on V100 was too slow.
- `2462225` `triage_raw_sorb5`: completed on V100. Dumped compact 5-example Sorbian diagnostics for base, official-only, `M_lang`, `M_edit`, and `M_mr`.
- `2462228` `triage_overfit_uk`: completed on V100. Ran same-set overfit tests for Ukrainian MR and SC.

## Sanity Gates

- Oracle evaluator gate passes for MT, QA, SC, GC, and MR on both tracks.
- QA/MR answer normalization now accepts common forms such as `The answer is X`, `Відповідь: X`, boxed answers, decimals, and trailing punctuation.
- SC/GC parser correctly handles the required two-line format and clean `CORRECT` cases.
- Same-set overfit is healthy:
  - Ukrainian MR overfit: 20 examples, 60 steps, same-set accuracy 100%.
  - Ukrainian SC overfit: 20 examples, 60 steps, same-set detection/correction F1 93.3%.

## Root Cause 1: Edit Data Was Almost All Error Cases

Before remediation, final SC/GC training data was badly imbalanced:

| Track | Task | Error Rows | Clean Rows |
| --- | ---: | ---: | ---: |
| Ukrainian | SC | 4506 | 40 |
| Ukrainian | GC | 3531 | 40 |
| Sorbian | SC | 2998 | 77 |
| Sorbian | GC | 966 | 69 |

This exactly explains the suspicious detection F1 plateau. On current locked validation, an always-error predictor scores:

- Ukrainian SC detection F1: 66.667
- Ukrainian GC detection F1: 65.993
- Sorbian SC detection F1: 65.630
- Sorbian GC detection F1: 66.168

Those values match the observed plateau. Raw predictions confirm the behavior: sampled models predict `pred_error == total` for SC/GC and almost never emit `CORRECT / CORRECT` on clean examples.

Remediation applied:

- `scripts/build_external_training_sets.py` now derives clean no-error counterparts from edit examples by replacing the wrong token with the correct token and setting:
  - `Wrong word: CORRECT`
  - `Correct word: CORRECT`
- `scripts/triage_data_sanity.py` now reports edit clean/error balance and always-error baselines.

Post-remediation final edit mixtures:

| Track | Task | Rows | Error Rows | Clean Rows |
| --- | ---: | ---: | ---: | ---: |
| Ukrainian | SC | 9009 | 4506 | 4503 |
| Ukrainian | GC | 7062 | 3531 | 3531 |
| Sorbian | SC | 5757 | 2998 | 2759 |
| Sorbian | GC | 1875 | 966 | 909 |

## Root Cause 2: MR Was Partly an Evaluator/Normalization Artifact

The earlier full Ukrainian evals showed every trained model at MR `0.000`. Raw dumps with normalized scoring show this was too pessimistic:

| Model | UK MR Accuracy, 20-example raw sample |
| --- | ---: |
| Base Qwen3.5-2B | 0.35 |
| Official-only | 0.30 |
| External-enhanced | 0.30 |
| `M_lang` | 0.20 |
| `M_mt` | 0.20 |
| `M_edit` | 0.15 |
| `M_qa` | 0.10 |
| `M_mr` | 0.15 |

The raw outputs often contain explanations or arithmetic expressions with the right final number embedded. The strict earlier evaluator counted those as wrong. Normalization fixes part of that.

MR is still genuinely weak:

- Ukrainian `M_mr` underperforms base on the 20-example raw sample.
- Sorbian compact MR remains poor:
  - base compact: 0/5
  - `M_lang`: 0/5
  - `M_mr`: 0/5
  - `M_edit`: 1/5
- Sorbian MR outputs often use Polish-like reasoning text or wrong arithmetic.

Remediation applied:

- `scripts/build_external_training_sets.py` now drops non-numeric MR targets. One bad Ukrainian ASDiv target (`Mrs.`) was removed.
- Final Ukrainian MR rows changed from 316 to 315.

## Root Cause 3: Checkpoints and Trainer Are Not Obviously Dead

Evidence against a dead training/eval loop:

- Trained checkpoint directories contain full `model.safetensors`, `config.json`, and generation config files.
- Training losses fall substantially in logs.
- Raw predictions differ across models.
- Same-set overfit succeeds for MR and SC.

This makes a global checkpoint-loading failure unlikely. The remaining failures are more plausibly caused by data balance, output-format behavior, and task interference.

## Current Interpretation

The concerning Phase 3 results should not be interpreted as approach failure.

What is real:

- Existing edit specialists were trained on an imbalanced all-error edit mixture, so their detection scores are mostly a class-prior artifact.
- Existing MR specialists did not preserve math well enough and often generate verbose/wrong reasoning.
- Sorbian MR remains weak even after normalization.

What was an artifact:

- Ukrainian MR was not truly zero across trained checkpoints under a normalized parser.
- SC/GC detection F1 around 66% was a majority/all-error baseline, not meaningful task competence.

## Recommended Next Step

Do not merge current specialists. Retrain at minimum:

1. Ukrainian and Sorbian `M_edit` from the balanced SC/GC mixtures.
2. Ukrainian and Sorbian multitask baselines that include the balanced edit mixtures.
3. MR specialists with stronger final-answer-only formatting and possibly lower learning rate / more preservation examples.

Before full retraining, run compact overfit checks for Sorbian SC/MR and optionally full checkpoint-loading comparison. Then rerun the locked validation evals using the normalized evaluator.
