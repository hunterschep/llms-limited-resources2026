# Stage B Failure Analysis

## A. MR Regression

Stage B MR is `4.167`, down from prompt-only `8.333`. The locked MR set is tiny, so this is likely one extra miss, but MR is equally weighted and cannot be ignored. The audit must distinguish wrong arithmetic from parser/format failures before any MR repair training.

Raw audit result: prompt-only gets `4/48` MR examples correct, Stage B gets `2/48`, and Stage C gets `3/48`. Stage B has fewer verbose outputs than prompt-only, but more wrong final numeric answers. This is a genuine capability/answer-quality regression, not just evaluator normalization.

## B. SC/GC Vulnerability

Stage B SC and GC are slightly above prompt-only. Stage C collapsed SC to `7.098` and GC to `1.942`, so edit behavior is fragile under broad replay. Repair must be small, hard-negative-heavy, and evaluated on no-error behavior and malformed output rate.

Raw audit result: prompt-only and Stage B both predict an error for every SC and GC locked-validation item. Stage B improves exact correction counts slightly and reduces SC malformed outputs, but no-error accuracy is still `0.0`. Stage C flips too far toward CORRECT, giving high no-error accuracy but catastrophic false negatives.

## C. Replay Instability

Stage C kept MT high (`43.790`) but destroyed edit detection and correction. Likely causes are mixture imbalance, replay examples that overrode the edit format, too many steps, too high effective impact, or malformed synthetic edit rows. The Stage C config is disqualified as a future training recipe.

## D. Ukrainian Failure

Ukrainian has real MT/QA signal, but trained checkpoints lose too much SC/GC/MR and remain below prompt-only. Ukrainian work is secondary until Sorbian Stage B rescue is attempted; no current Ukrainian checkpoint is a candidate.

## Blocking Tests

- Stage B raw MR audit.
- Stage B edit confusion and no-error audit.
- Stage B MT regression audit by direction.
- Prompt/decoding sweep on Stage B.
- Adapter-scale search only if a valid base+adapter pair exists.
- Tiny MR/edit repair probes from Stage B.
