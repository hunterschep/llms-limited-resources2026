# Edit Data Remediation

The first-pass edit specialists learned an always-error prior because SC/GC train data had very few no-error rows. That made detection F1 near 66% meaningless because an always-error predictor receives almost the same detection score on the old distribution.

## Remediation

- `scripts/build_external_training_sets.py` derives clean no-error counterparts from one-token edit examples.
- No-error targets use exactly:

```text
Wrong word: CORRECT
Correct word: CORRECT
```

- `configs/train/uk/edit_scgc.yaml` and `configs/train/sorbian/edit_scgc.yaml` now write to `checkpoints/phase3_fixed/...`.
- Task-balanced/capped sampling is active in `train_sft.py`.
- `scripts/report_edit_data_balance.py` reports clean/error balance and always-error/always-CORRECT baselines.
- `scripts/report_scgc_confusion.py` categorizes no-error behavior, false positives, false negatives, wrong-word errors, correction errors, and malformed outputs.

## Completion Criteria

Fixed `M_edit` must show sane no-error behavior and useful SC/GC aggregate under the normalized evaluator before it can be merged.
