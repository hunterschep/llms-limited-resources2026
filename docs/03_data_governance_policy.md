# Data Governance Policy

This project treats WMT26 as a contamination-sensitive model-submission task. All sources must be registered before they are used by compilers, training scripts, evaluation scripts, teacher generation, or final polishing.

Machine-readable registry:

- `data/manifests/data_governance_registry.csv`
- `data/manifests/data_governance_registry.schema.json`

Validator:

- `scripts/validate_data_governance.py`

## Source Categories

- `official_train`: official training files released by the organizers.
- `official_dev_tune`: deterministic tune split from official dev data.
- `official_dev_locked_validation`: deterministic locked validation split from official dev data.
- `official_monolingual`: official support corpora without task labels.
- `external_public`: external data with public URL, license, and reproducible download.
- `synthetic_generated`: deterministic examples generated from allowed sources.
- `teacher_generated`: outputs produced by approved teacher/retrieval pipelines from allowed sources.
- `distilled`: examples distilled from approved teacher outputs.
- `forbidden`: data that must not be used.

## Hard Bans

Do not use:

- Hidden test data.
- WMT2025 test sets.
- Ukrainian UNLP/MMLU test splits.
- Original, translated, modified, or benchmark-derived PolyMath data.
- Extra Sorbian certificate questions outside the official repo.
- Unlicensed/private data.
- Data whose public source cannot be documented.

## Validator Failures

The validator fails if:

- `allowed_status` is missing or invalid.
- External data is missing `license` or `source_url`.
- Forbidden data is marked for training or final training.
- Risky data is marked for training without a `JUSTIFICATION:` note.
- Official dev data is marked for training without an `OFFICIAL_DEV_TRAIN_OVERRIDE:` note.
- Any benchmark-derived math data is marked for training, tuning, final training, or inference use.
- External Sorbian certificate material is marked for training.

## Policy For Official Dev Data

Official dev files are not ordinary train files. During method development they are used for prompt inspection, tuning, and locked local validation. The default compilers put official dev rows into `tune` or `locked_validation` according to `data/manifests/local_split_manifest.jsonl`.

MR dev files are special because they reflect the official math benchmark format and contain only 24 examples per language. They are kept for format inspection and locked validation only.
