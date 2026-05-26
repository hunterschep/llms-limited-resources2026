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

## Reboot Run Outcome

The first full competitive Ukrainian run completed on Andromeda. It produced a small MT/QA signal but no competitive checkpoint.

- Stage A improved MT from `40.990` to `41.889` and QA from `34.278` to `37.960`, but overall fell to `34.636`.
- Stage B reached MT `41.999` and QA `39.093`, but GC collapsed to `4.954` and overall fell to `28.078`.
- Stage C kept MT near `41.979` and partly recovered SC, but GC remained weak at `11.053` and MR stayed below prompt-only.

Prompt-only remains the Ukrainian fallback. All Ukrainian competitive-reboot checkpoints were deleted from Andromeda after manifesting.
