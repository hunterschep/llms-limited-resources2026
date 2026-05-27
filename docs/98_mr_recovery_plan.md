# MR Recovery Plan

Stage B loses two correct MR items versus prompt-only on a tiny MR set. `edit_repair_tiny` recovers one item but remains below prompt-only. The goal is recovery, not numerical overfitting to locked validation.

Data policy:

- governed public non-PolyMath MR only
- no original PolyMath
- no translated PolyMath
- no modified PolyMath
- no PolyMath-derived examples
- no imitation of official MR dev
- final-answer-only targets
- no chain-of-thought targets

Methods:

- MR prompt/decoding repair on top candidates
- tiny MR adapter
- MR delta merged with small coefficient into the interpolated candidate
- base-output distillation only on public non-eval MR prompts where base is correct

Gates:

- MT drop `<=1.0`
- MR improves over candidate, preferred `>=8.333`
- no SC/GC collapse
- no QA collapse
- no malformed-answer spike

## Outcome

MR recovery succeeded only after lineage-preserving model surgery. The standalone MR-recovery adapter did not beat the reproduced Stage B full-eval MR score, but adapter scaling and the selected task-vector merge recovered MR above prompt-only while keeping the MT breakthrough.

| Candidate | Overall | MT | QA | SC | GC | MR |
|---|---:|---:|---:|---:|---:|---:|
| prompt-only | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 |
| original Stage B | 32.826 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 |
| edit_repair_tiny | 33.177 | 43.345 | 48.428 | 34.370 | 33.493 | 6.250 |
| adapter scale 0.80 | 33.957 | 42.829 | 47.170 | 35.876 | 33.493 | 10.417 |
| selected task-vector merge | 34.417 | 44.035 | 48.428 | 35.711 | 33.493 | 10.417 |

The selected merge reaches MR `10.417`, which is above the prompt-only MR anchor `8.333`. The MR raw-error audit still shows weak arithmetic behavior:

- 48 MR rows.
- 5 parser-normalization rescued matches.
- 35 wrong numeric answers.
- 6 verbose/explanation answers.
- 2 nonnumeric answers.
- malformed/verbose rate `0.167`.

Decision: MR is recovered enough for the current Sorbian candidate, but not solved as a capability. The remaining MR errors are mostly genuine wrong numeric answers, not parser artifacts.
