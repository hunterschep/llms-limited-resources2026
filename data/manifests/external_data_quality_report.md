# External Data Quality Report

This report summarizes executable seed sources, scripted large-source acquisition paths, filtering decisions, and final mixture counts.

## Executable Seed Sources

- OPUS Tatoeba en-uk/cs-uk: small public MT seed corpora, filtered by length, Cyrillic target ratio, length ratio, and exact deduplication.
- UA-GEC train M2: mined for one-token WMT-style SC/GC examples only.
- UD Ukrainian IU train: used for clean Ukrainian text, QA cloze generation, and morphology/typo examples.
- UniMorph hsb: registered for morphology; current final Sorbian GC uses public official monolingual plus suffix rules, with UniMorph available for expansion.
- GSM8K/SVAMP/ASDiv: public arithmetic preservation sources; small capped use only, no benchmark-derived math.

## Scripted But Not Yet Used

- Larger OPUS en-uk corpora, HPLT/OSCAR/CulturaX Ukrainian, Leipzig Sorbian, prior WMT Sorbian, and Czech/Polish transfer are registered but not marked final-train until source-specific license and overlap review is complete.

## Counts

| Path | Rows |
|---|---:|
| `data/processed/external/sorbian/gc_synthetic_dsb.jsonl` | 317 |
| `data/processed/external/sorbian/gc_synthetic_hsb.jsonl` | 316 |
| `data/processed/external/sorbian/monolingual_public.jsonl` | 2997 |
| `data/processed/external/sorbian/mr_non_benchmark_dsb.jsonl` | 120 |
| `data/processed/external/sorbian/mr_non_benchmark_hsb.jsonl` | 120 |
| `data/processed/external/sorbian/mt_prior_wmt.jsonl` | 0 |
| `data/processed/external/sorbian/qa_generated_public_dsb.jsonl` | 1186 |
| `data/processed/external/sorbian/qa_generated_public_hsb.jsonl` | 1190 |
| `data/processed/external/sorbian/related_transfer_cs_pl.jsonl` | 0 |
| `data/processed/external/sorbian/sc_synthetic_dsb.jsonl` | 1335 |
| `data/processed/external/sorbian/sc_synthetic_hsb.jsonl` | 1282 |
| `data/processed/external/uk/gc_real.jsonl` | 2587 |
| `data/processed/external/uk/gc_synthetic_public.jsonl` | 744 |
| `data/processed/external/uk/monolingual_train.jsonl` | 1996 |
| `data/processed/external/uk/mr_non_benchmark.jsonl` | 280 |
| `data/processed/external/uk/mt_doc_train.jsonl` | 2500 |
| `data/processed/external/uk/mt_train.jsonl` | 32978 |
| `data/processed/external/uk/qa_generated_public.jsonl` | 770 |
| `data/processed/external/uk/sc_real.jsonl` | 2844 |
| `data/processed/external/uk/sc_synthetic_public.jsonl` | 1463 |
| `data/processed/final/sorbian/format_polish_final.jsonl` | 972 |
| `data/processed/final/sorbian/gc_train_final.jsonl` | 1035 |
| `data/processed/final/sorbian/lang_curriculum_external.jsonl` | 4997 |
| `data/processed/final/sorbian/mr_train_final.jsonl` | 312 |
| `data/processed/final/sorbian/mt_train_final.jsonl` | 120000 |
| `data/processed/final/sorbian/qa_train_final.jsonl` | 2376 |
| `data/processed/final/sorbian/sc_train_final.jsonl` | 3075 |
| `data/processed/final/uk/format_polish_final.jsonl` | 815 |
| `data/processed/final/uk/gc_train_final.jsonl` | 3571 |
| `data/processed/final/uk/lang_curriculum_external.jsonl` | 3996 |
| `data/processed/final/uk/mr_train_final.jsonl` | 316 |
| `data/processed/final/uk/mt_train_final.jsonl` | 35478 |
| `data/processed/final/uk/qa_train_final.jsonl` | 12707 |
| `data/processed/final/uk/sc_train_final.jsonl` | 4546 |

## Contamination Notes

- No hidden WMT26 test data is used.
- No WMT2025 test sets are used.
- No held-out ZNO/MMLU splits are downloaded or used.
- No official math benchmark data, translations, modifications, or derivatives are used for training.
- No external Sorbian certificate or exam-question source is used.

## Recommended Sampling

- Cap MT in multitask mixtures despite large row counts.
- Keep MR small and format-focused.
- Keep generated QA separate from official QA in ablations.
- Use SC/GC compilers as a major equal-weighted task contribution, not an afterthought.
