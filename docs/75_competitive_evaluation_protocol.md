# Competitive Evaluation Protocol

## Baselines

- Prompt-only Qwen3.5-2B.
- Phase 4 tiny candidates as diagnostic-only comparisons.

## Candidates

Sorbian:

- Stage A DAPT.
- Stage B MT.
- Stage C instruction replay.
- Stage D format alignment if justified.
- Soups/interpolations if Stage B/C gives real signal.

Ukrainian:

- Stage A real MT.
- Stage B instruction replay.
- Stage C document/format.
- Soups/interpolations if useful.

## Metrics

- MT chrF++ and BLEU.
- MT direction breakdown.
- QA accuracy.
- SC detection F1, correction F1, no-error accuracy, malformed rate.
- GC detection F1, correction F1, no-error accuracy, malformed rate.
- MR accuracy and malformed rate.
- Equal-weighted overall.

## Reporting

Do not hide regressions. A controlled auxiliary-task drop may be acceptable if MT and overall improve materially. A model with no MT movement is not competitive unless auxiliary gains are large and robust.
