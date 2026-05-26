# Competitive Success Criteria

## Sorbian

First milestone:

- Average MT chrF++ improvement over prompt-only: at least `+8`.
- Equal-weighted overall improvement over prompt-only: at least `+5`.
- All six directions reported separately: `de->hsb`, `hsb->de`, `de->dsb`, `dsb->de`, `hsb->dsb`, `dsb->hsb`.

Stretch target:

- Average MT chrF++ improvement: `+15` to `+25`.
- Overall improvement: `+10` or more.

Auxiliary guardrails:

- QA should preserve within roughly `-3` unless MT and overall gains are strong.
- SC/GC correction F1 must not remain near zero.
- MR should preserve normalized prompt-only or have a documented tradeoff.

## Ukrainian

First milestone:

- `en->uk` and `cs->uk` MT chrF++ improve by `+2` to `+5`.
- Equal-weighted overall improves by at least `+3`.

Competitive target:

- Overall improves by `+5` to `+8` or more.
- SC/GC correction F1 improves using real UA-GEC/UD-derived examples.
- QA and MR do not catastrophically collapse.

## Failure Standard

Failure can be declared only after large public data is enabled, language/MT acquisition is run, instruction replay is run, full locked evaluation is completed, and failed checkpoints are cleaned. Tiny LoRA/no-harm ablations are not enough evidence.

## First Reboot Outcome

Ukrainian did not meet the first milestone. MT improved by about `+1` chrF++, below the `+2` to `+5` target, and overall stayed below prompt-only for every stage.

Sorbian partially met the first milestone. Stage B MT-large exceeded the MT requirement with `+15.858` average chrF++, but overall improved by only `+3.631`, below the `+5` target, because MR regressed from `8.333` to `4.167`. The checkpoint is therefore `promising_but_needs_replay`, not a final competitive candidate.
