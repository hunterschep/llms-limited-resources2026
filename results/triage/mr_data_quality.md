# MR Data Quality Report

## Normalization Probes

- `42` -> `42` expected `42`: `True`
- `42.0` -> `42` expected `42`: `True`
- `The answer is 42.` -> `42` expected `42`: `True`
- `Answer: 42` -> `42` expected `42`: `True`
- `Відповідь: 42` -> `42` expected `42`: `True`
- `\boxed{42}` -> `42` expected `42`: `True`
- `  -3.0  ` -> `-3` expected `-3`: `True`
- `1/2` -> `0.5` expected `0.5`: `True`
- `50%` -> `50%` expected `50%`: `True`

## Files

| Track | File | Rows | Parseable | Bad Parse | Forbidden Metadata | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| uk | `data/processed/final/uk/mr_train_final.jsonl` | 315 | 315 | 0 | 0 | pass |
| uk | `data/processed/final/uk/mr_format_preservation.jsonl` | 315 | 315 | 0 | 0 | pass |
| sorbian | `data/processed/final/sorbian/mr_train_final.jsonl` | 312 | 312 | 0 | 0 | pass |
| sorbian | `data/processed/final/sorbian/mr_format_preservation.jsonl` | 312 | 312 | 0 | 0 | pass |
