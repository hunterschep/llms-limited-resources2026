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
