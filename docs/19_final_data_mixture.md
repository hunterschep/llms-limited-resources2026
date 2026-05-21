# Final Data Mixture

Configs:

- `configs/data/final_mixture_uk.yaml`
- `configs/data/final_mixture_sorbian.yaml`

The mixture is task-aware rather than row-count proportional. MT is capped so it does not dominate the five-task objective.

## Ukrainian

- MT: OPUS Tatoeba en-uk/cs-uk plus document-grouped anti-summarization examples.
- QA: official WMT Ukrainian QA train plus public UD-derived cloze MCQs.
- SC: scaffold synthetic plus UA-GEC/UD public typo examples.
- GC: scaffold synthetic plus UA-GEC one-token corrections and UD morphology examples.
- MR: small GSM8K/SVAMP/ASDiv-derived non-benchmark preservation data.
- LANG: light UD Ukrainian instruction-preserving language curriculum.

## Sorbian

- MT: capped official bidirectional Sorbian MT backbone; prior WMT path registered but empty until file review.
- QA: public generated hsb/dsb reading/cloze MCQs from public official monolingual text; no external certificate source.
- SC: public monolingual hsb/dsb typo generation.
- GC: public monolingual hsb/dsb morphology minimal pairs; UniMorph hsb registered for expansion.
- MR: small non-benchmark preservation data.
- LANG: hsb/dsb instruction-preserving monolingual curriculum.

Final counts are in `data/manifests/final_training_data_summary.md`.
