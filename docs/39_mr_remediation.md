# MR Remediation

MR was partly an evaluator-normalization artifact but remains a real weakness. The target is preservation and final-answer-only behavior, not broad math overfitting.

## Evaluator Normalization

`src/wmt26/eval/metrics.py` normalizes:

- bare integers and decimals
- integer-like decimals
- negative numbers
- simple fractions
- percentages
- trailing punctuation
- `The answer is X`
- `Answer: X`
- `Відповідь: X`
- boxed answers

Normalization is intentionally numeric and conservative; it does not convert arbitrary text into a correct answer.

## Data Remediation

- Final MR train files contain only parseable numeric targets.
- MR format-preservation rows are generated from non-PolyMath MR data and train the model to emit the final answer only.
- No PolyMath, translated PolyMath, modified PolyMath, or PolyMath-derived examples are allowed.

## Config Changes

- Fixed MR specialists write under `checkpoints/phase3_fixed/...`.
- MR specialists train on both `mr_train_final.jsonl` and `mr_format_preservation.jsonl`.
- Learning rate is lowered and max steps increased to reduce destructive format drift.

## Completion Criteria

Fixed `M_mr` should recover prompt-only MR on normalized locked validation, or the merge decision must explicitly block MR merging and document why.
