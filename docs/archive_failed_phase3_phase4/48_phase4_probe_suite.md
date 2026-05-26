# Phase 4 Probe Suite

The Phase 4 probe is a small fixed-seed subset of locked local validation. It is designed to catch obvious no-harm regressions before spending GPU time on full locked validation.

Generated files:

- `data/processed/phase4_probe/uk_probe.jsonl`
- `data/processed/phase4_probe/sorbian_probe.jsonl`
- per-task files under `data/processed/phase4_probe/*_probe_<task>.jsonl`
- `configs/eval/phase4_probe_uk.yaml`
- `configs/eval/phase4_probe_sorbian.yaml`
- `results/phase4/probe/probe_manifest.json`

Sampling policy:

- MR keeps all or nearly all rows because the local MR set is tiny.
- SC/GC are balanced by error/no-error labels.
- MT and QA use fixed-seed stratified samples by source/language metadata where available.

Metrics use the same internal WMT-style convention as full evaluation. Probe results do not replace full locked validation; they decide whether a candidate deserves full evaluation.
