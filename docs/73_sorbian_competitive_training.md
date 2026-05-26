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

## Reboot Run Outcome

The first full competitive Sorbian run completed on Andromeda using the large governed mixtures.

Stage B MT-large is the only checkpoint preserved for continued work:

- Overall improved from `29.195` to `32.826` (`+3.631`).
- Average MT chrF++ improved from `27.477` to `43.335` (`+15.858`).
- Direction gains were broad: `de->hsb +19.460`, `de->dsb +15.809`, `hsb->de +19.802`, `dsb->de +18.977`, `hsb->dsb +8.628`, `dsb->hsb +7.421`.
- QA, SC, and GC stayed above prompt-only, but MR fell from `8.333` to `4.167`.

Stage A was not MT-competitive, and Stage C collapsed SC/GC despite preserving MT. Stage B is labeled `promising_but_needs_replay`, not `competitive_candidate`.
