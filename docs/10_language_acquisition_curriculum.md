# Language Acquisition Curriculum

Builder:

- `scripts/build_language_curriculum.py`

Configs:

- `configs/data/language_curriculum_uk.yaml`
- `configs/data/language_curriculum_sorbian.yaml`

Goal:

Teach Ukrainian, Upper Sorbian, and Lower Sorbian while preserving instruction-following. We avoid blind LM-only continued pretraining that could overwrite the base model’s instruction behavior.

Sorbian sources:

- Official hsb monolingual.
- Official dsb monolingual.
- Official de-hsb/de-dsb/hsb-dsb parallel via MT compiler.
- Future registered prior WMT Sorbian resources.
- Future registered Czech/Polish transfer data.
- Grammar and orthography drills from SC/GC compilers.

Ukrainian sources:

- Official Ukrainian QA text for initial light curriculum.
- Future registered Ukrainian monolingual, en-uk, cs-uk, educational, grammar, and spelling resources.
- Document/conversation translation examples once registered.

This follows the WMT25 TartuNLP lesson: language acquisition and instruction-following should be trained together.

Source: https://aclanthology.org/2025.wmt-1.88/
