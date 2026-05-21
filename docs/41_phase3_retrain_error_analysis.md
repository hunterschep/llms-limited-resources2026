# Phase 3 Retrain Error Analysis

Status: pending fixed retraining.

Required analyses after fixed evaluation:

- SC/GC false-positive no-error failures.
- SC/GC false-negative missed-error failures.
- SC/GC wrong-word versus wrong-correction failures.
- SC/GC malformed or verbose outputs.
- MR normalized exact matches.
- MR parser-rescued answers.
- MR wrong numeric answers.
- MR nonnumeric, verbose, or empty outputs.
- Cross-task regressions versus prompt-only.

Use:

```bash
python3 scripts/report_scgc_confusion.py --input <raw_prediction_dump.jsonl>
python3 scripts/report_mr_raw_errors.py --input <raw_prediction_dump.jsonl>
```
