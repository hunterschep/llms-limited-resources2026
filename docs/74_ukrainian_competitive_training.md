# Ukrainian Competitive Training

## Objective

Build a Ukrainian candidate with real MT movement and positive equal-weighted overall. The first milestone is `+2` to `+5` chrF++ on `en->uk` and `cs->uk`, and `+3` overall.

## Stage A: Real MT Adaptation

Data:

- High-quality OPUS en-uk and cs-uk.
- ParaCrawl en-uk after filtering.
- MaCoCu only after license/usage review.
- Paragraph/document MT examples.

## Stage B: Instruction Replay

Data:

- Official Ukrainian QA train.
- Train-only Ukrainian MMLU/ZNO material from official WMT files.
- UA-GEC one-token SC/GC.
- UD Ukrainian IU morphology and clean text.
- Public non-PolyMath MR.

## Stage C: Document And Format Alignment

Data:

- Grouped paragraph translation.
- Anti-summary translation examples.
- Exact QA/MR/SC/GC output format examples.

## Evaluation

Report `en->uk`, `cs->uk`, average MT, QA, SC, GC, MR, malformed output rates, and equal-weighted overall after each stage.
