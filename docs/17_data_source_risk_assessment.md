# Data Source Risk Assessment

## Allowed Executable Sources

- OPUS Tatoeba en-uk/cs-uk: low risk after filtering and overlap checks.
- UA-GEC train: allowed train split only; no test files are downloaded.
- UD Ukrainian IU train: public treebank training file, used for monolingual/morphology generation.
- UniMorph hsb: public morphology table, used for Upper Sorbian morphology expansion.
- GSM8K: public non-benchmark math preservation source.

## Risky But Used Sparingly

- ASDiv and SVAMP: public arithmetic datasets with research-use/license notes. They are capped and used only for format-preservation MR. They are not related to the official MR benchmark.

## Registered But Not Used Yet

- Larger OPUS corpora: require corpus-level license notes and quality sampling.
- HPLT/OSCAR/CulturaX: web-crawl noise and license metadata require careful sampling.
- Leipzig Sorbian corpora: registered, but final training waits for terms review.
- Prior WMT Sorbian data: registered; final training waits for file-level review to exclude test sets.
- Czech/Polish transfer: registered; final training waits for capped transfer plan.
- Lower Sorbian Hunspell package: unknown until package/license review.

## Forbidden

- Hidden WMT26 test data.
- WMT2025 test sets.
- Held-out ZNO/UNLP/MMLU splits.
- The official math benchmark, translations, modifications, or derivatives.
- Extra Sorbian certificate/exam questions.
- Private or unlicensed data.
