# External Data Layer

This directory holds registered public sources for the second-stage WMT26 data layer.

Subdirectories:

- `raw/`: downloaded archives or raw text files.
- `filtered/`: source-specific filtered JSONL files.
- `reports/`: optional source inspection samples.

Rules:

- Every source must be registered in `data/manifests/data_governance_registry.csv`.
- Download with `scripts/download_external_data.py --execute`.
- Filter with `scripts/filter_external_data.py`.
- Deduplicate with `scripts/deduplicate_external_data.py`.
- Check overlap with `scripts/check_dev_overlap.py`.
- Build final mixtures with `scripts/build_external_training_sets.py`.

Large sources such as HPLT, OSCAR, CulturaX, larger OPUS corpora, and Leipzig corpora are scripted for Andromeda-scale acquisition and require source-specific license review before enabling training use.
