# Competitive Data Plan

## Sorbian

Priority sources:

- Official WMT26 Sorbian MT and monolingual data.
- Prior WMT very-low-resource Sorbian train/support data, excluding test sets:
  - WMT20 very-low-resource: https://www.statmt.org/wmt20/unsup_and_very_low_res/
  - WMT21 very-low-resource: https://www.statmt.org/wmt21/unsup_and_very_low_res.html
  - WMT22 very-low-resource: https://www.statmt.org/wmt22/unsup_and_very_low_res.html
  - WMT22 data repository: https://github.com/mariondimarco/WMT22_UnsupVeryLowResMT_Data
- Leipzig Upper Sorbian `hsb_mixed_2012`: https://corpora.uni-leipzig.de/en?corpusId=hsb_mixed_2012
- Leipzig Lower Sorbian `dsb_wikipedia_2021`: https://corpora.wortschatz-leipzig.de/en?corpusId=dsb_wikipedia_2021
- Controlled Czech/Polish transfer data from public OPUS sources.
- UniMorph Upper Sorbian: https://github.com/unimorph/hsb
- Hunspell candidates only after license review: https://github.com/hunspell/hunspell and https://github.com/wooorm/dictionaries
- Generated data only when grounded in public text: backtranslation, triangle consistency, pseudo-parallel hsb/dsb, SC/GC compiler examples, and QA from reading passages.

Target scale:

- Several hundred thousand clean MT instruction examples after bidirectional expansion.
- Hundreds of thousands to one million or more language-acquisition examples/tokens if feasible.
- All six MT directions represented.

## Ukrainian

Priority sources:

- OPUS English-Ukrainian and Czech-Ukrainian corpora: https://opus.nlpl.eu/
- UkrainianLT: https://github.com/Helsinki-NLP/UkrainianLT/
- ParaCrawl English-Ukrainian: https://paracrawl.eu/news/item/17-english-ukrainian-bonus-parallel-corpus
- MaCoCu Ukrainian-English if license/usage review passes: https://live.european-language-grid.eu/catalogue/corpus/23189
- HPLT: https://huggingface.co/datasets/HPLT/hplt_monolingual_v1_2
- OSCAR: https://huggingface.co/datasets/oscar-corpus/oscar
- CulturaX: https://huggingface.co/datasets/uonlp/CulturaX
- Ukrainian Wikipedia: https://uk.wikipedia.org/
- Ukrainian Wikisource: https://uk.wikisource.org/
- Ukrainian Wikibooks: https://uk.wikibooks.org/
- UA-GEC train: https://github.com/grammarly/ua-gec
- UD Ukrainian IU: https://universaldependencies.org/treebanks/uk_iu/index.html
- Official QA train files plus safe public train-only QA augmentation.
- GSM8K: https://huggingface.co/datasets/openai/gsm8k
- ASDiv: https://github.com/chaochun/nlu-asdiv-dataset
- SVAMP: https://github.com/arkilpatel/SVAMP
- MATH only if a safe non-PolyMath subset is explicitly reviewed: https://huggingface.co/datasets/EleutherAI/hendrycks_math

Target scale:

- Several hundred thousand high-quality en-uk/cs-uk MT pairs after filtering.
- Document-level/paragraph-preserving examples.
- Real SC/GC corrections from UA-GEC/UD-derived sources.
- Small, clean MR preservation data only.

## Contamination Policy

Every row must have `source_id`, source metadata, split, and contamination notes. No PolyMath, WMT2025 test, hidden WMT26 test, Ukrainian held-out benchmark tests, or extra Sorbian certificate data may enter training.

PolyMath is forbidden: https://huggingface.co/datasets/Qwen/PolyMath

Competitive-reference papers to preserve:

- TartuNLP WMT25: https://aclanthology.org/2025.wmt-1.88/
- JGU Mainz WMT25: https://aclanthology.org/2025.wmt-1.89/
- WMT25 findings: https://aclanthology.org/2025.wmt-1.27/
- LoRA: https://arxiv.org/abs/2106.09685
- QLoRA: https://arxiv.org/abs/2305.14314
- Model Soups: https://proceedings.mlr.press/v162/wortsman22a.html
- Task Arithmetic: https://openreview.net/forum?id=6t0Kwf8-jrj
- TIES-Merging: https://arxiv.org/abs/2306.01708
- DPO: https://papers.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html
