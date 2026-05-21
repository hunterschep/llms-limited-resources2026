# External Data Filtering

Scripts:

- `scripts/filter_external_data.py`
- `scripts/deduplicate_external_data.py`
- `scripts/check_dev_overlap.py`
- `configs/data/external_source_filters.yaml`

Filters:

- Generic text: min/max length, URL removal, repeated-character removal, punctuation/digit caps.
- MT: source/target length ratio, target Cyrillic fraction for Ukrainian, exact pair deduplication, no identical source/target pairs.
- QA: generated examples require non-empty options, one correct label, and source/evidence metadata.
- SC/GC: exactly one wrong word or `CORRECT`; no full-sentence rewrite targets.
- MR: non-benchmark source IDs only, concise final-answer targets, capped rows.

Overlap checking:

- Exact normalized overlap is removed against local tune and locked validation examples.
- Single-token/label targets are not used as overlap keys, preventing false positives for QA labels or short corrections.

Reports:

- `data/manifests/external_data_filter_report.jsonl`
- `data/manifests/external_data_dedup_report.jsonl`
- `data/manifests/external_data_overlap_report.jsonl`
- `data/manifests/external_data_quality_report.md`
