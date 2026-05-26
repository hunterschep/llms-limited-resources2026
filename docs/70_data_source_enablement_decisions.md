# Data Source Enablement Decisions

## Enabled Immediately

- Official WMT26 train/support data.
- OPUS seed Ukrainian Tatoeba `en-uk` and `cs-uk`.
- UA-GEC train M2.
- UD Ukrainian IU train.
- GSM8K train, ASDiv, and SVAMP for small MR preservation, with existing risk notes.
- UniMorph Upper Sorbian.
- Existing official Sorbian MT/monolingual data.
- WMT22 Sorbian train/support repository files after filename-level exclusion of `dev`, `valid`, and `test` archives.
- Leipzig Upper Sorbian `hsb_mixed_2012_300K` and Lower Sorbian Wikipedia 2021 monolingual files for DAPT/language curriculum only.

## Enabled For Competitive Acquisition After Review

- OPUS large Ukrainian collections: ParaCrawl, CCMatrix, WikiMatrix, NLLB, MultiHPLT, KDE/GNOME/Ubuntu, TED/TED2020, and related high-quality public corpora.
- HPLT Ukrainian monolingual sampling.
- Older WMT20/21 Sorbian train/support files if direct public train/support downloads are verified.
- Czech/Polish transfer corpora from OPUS.
- MaCoCu Ukrainian-English only after license and redistribution review.

## Rejected Or Blocked

- PolyMath, translated PolyMath, modified PolyMath, and PolyMath-derived examples.
- WMT2025 test sets.
- Hidden WMT26 test data.
- Ukrainian UNLP/MMLU/ZNO test splits.
- External Sorbian certificate questions.
- Lower Sorbian Hunspell candidate until package contents and license are reviewed.

## Active Configs

- `configs/data/competitive_sources_uk.yaml`
- `configs/data/competitive_sources_sorbian.yaml`
- `configs/data/competitive_filtering.yaml`
- `configs/data/competitive_mixture_uk.yaml`
- `configs/data/competitive_mixture_sorbian.yaml`
