# Data Filtering And Quality Reboot

## Parallel MT

Filtering requirements:

- Language ID or script checks on both sides.
- Length, token-ratio, and copy-ratio filters.
- Exact and near-duplicate removal.
- Locked-validation overlap removal.
- URL, boilerplate, excessive punctuation, and excessive digit filters.
- Manual source samples before final training.

## Monolingual

Filtering requirements:

- Language ID or script checks.
- Paragraph/sentence segmentation.
- Min/max length filtering.
- Deduplication and boilerplate removal.
- Source tracking and sample notes.

## QA

Filtering requirements:

- Exactly one correct option.
- Non-empty and non-duplicate options.
- Balanced labels and shuffled options.
- Source evidence where possible.
- No held-out benchmark/test contamination.

## SC/GC

Filtering requirements:

- Exactly one wrong word or clean `CORRECT/CORRECT`.
- Wrong word appears in input.
- No full-sentence rewrite targets.
- Calibration against official-style error/no-error distribution.
- Hard no-error and near-miss false-positive examples.

## MR

Filtering requirements:

- Parseable final answer.
- Final-answer-only target.
- Low/medium difficulty.
- No PolyMath strings, metadata, translations, modifications, or derivatives.
