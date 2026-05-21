# Public Data Acquisition Plan

This second-stage layer adds a governed public-data seed set and scripts larger sources for Andromeda-scale acquisition.

Executable seed sources:

- OPUS Tatoeba en-uk and cs-uk for Ukrainian MT.
- UA-GEC train M2 for Ukrainian one-token SC/GC mining.
- UD Ukrainian IU train for Ukrainian monolingual, generated QA, and morphology examples.
- UniMorph hsb for Upper Sorbian morphology expansion.
- GSM8K, ASDiv, and SVAMP for small non-benchmark math preservation.

Scripted but not final-train enabled:

- Larger OPUS en-uk corpora.
- HPLT/OSCAR/CulturaX Ukrainian samples.
- Leipzig hsb/dsb corpora.
- Prior WMT20-22 Sorbian train/support data, excluding all test sets.
- Czech/Polish transfer candidates.
- Lower Sorbian Hunspell candidate.

Commands:

```bash
python3 scripts/download_external_data.py --execute
python3 scripts/filter_external_data.py
python3 scripts/deduplicate_external_data.py
python3 scripts/check_dev_overlap.py
python3 scripts/build_external_training_sets.py
python3 scripts/report_external_data_quality.py
```

Sources preserve the links listed in the project goal, including WMT26, OPUS, UkrainianLT, ParaCrawl, UA-GEC, UD Ukrainian IU, UniMorph hsb, GSM8K, ASDiv, SVAMP, and the risky/forbidden references.
