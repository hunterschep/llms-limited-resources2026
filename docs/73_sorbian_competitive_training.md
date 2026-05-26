# Sorbian Competitive Training

## Objective

Build a Sorbian candidate that moves MT substantially while preserving enough QA/SC/GC/MR to improve equal-weighted overall. The first milestone is `+8` average MT chrF++ and `+5` overall over prompt-only.

## Stage A: Language Acquisition

Data:

- Official hsb/dsb monolingual.
- Leipzig hsb/dsb after review.
- Prior WMT monolingual/support data after test exclusion.
- Low-weight Czech/Polish transfer.
- Short instruction replay.

Training:

- QLoRA/LoRA DAPT first.
- Serious token budget on H200/A100.
- Save stage checkpoints for evaluation and possible soup.

## Stage B: MT Adaptation

Data:

- Official de-hsb, de-dsb, hsb-dsb.
- Bidirectional expansion for all six directions.
- Prior WMT parallel train/support.
- Backtranslation/triangle consistency after quality checks.

## Stage C: Instruction Replay

Data:

- Public Sorbian QA from reading passages.
- SC/GC compiler examples.
- Public non-PolyMath MR.
- Format examples.

## Stage D: Format Alignment

Tiny alignment only if Stage B/C produces a competitive model. If polish reduces MT or overall, discard it.
