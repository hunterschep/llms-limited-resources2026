# Task Compilers

Compilers are a core contribution. They turn official/public sources into reproducible canonical JSONL, not ad hoc scraped mixtures.

Scripts:

- `scripts/compile_mt_data.py`
- `scripts/compile_sc_data.py`
- `scripts/compile_gc_data.py`
- `scripts/compile_qa_data.py`
- `scripts/compile_mr_data.py`

Configs:

- `configs/compilers/mt.yaml`
- `configs/compilers/sc.yaml`
- `configs/compilers/gc.yaml`
- `configs/compilers/qa.yaml`
- `configs/compilers/mr.yaml`

## MT

The Sorbian compiler emits all six directions from official parallel data:

- de -> hsb
- hsb -> de
- de -> dsb
- dsb -> de
- hsb -> dsb
- dsb -> hsb

The config reserves governed inputs for future backtranslation, cycle consistency, triangle consistency, Czech transfer, and Polish transfer. Those inputs must be registered first.

Ukrainian MT currently uses official dev data only for tune/locked validation. Competitive Ukrainian MT training requires registered public en-uk/cs-uk corpora.

## SC

The SC compiler emits official dev tune/locked examples and synthetic train examples from allowed source text. It supports insertion, deletion, substitution, transposition, Ukrainian Cyrillic confusions, and Sorbian diacritic deletion/substitution.

Output:

```text
Wrong word: X
Correct word: Y
```

Clean cases use `CORRECT` / `CORRECT`.

## GC

The GC compiler emits official dev tune/locked examples and conservative synthetic morphology minimal pairs. The first implementation uses suffix swaps; future lexicon-backed generators should be registered as external public resources.

## QA

Ukrainian QA uses official train/dev files, skips malformed empty-option rows, and augments train rows with option shuffling and numeric/alphabetic labels.

Sorbian official QA is certificate-derived dev material and is tune/locked only. Competitive Sorbian QA needs public non-certificate reading-comprehension material.

## MR

The MR compiler uses small local arithmetic preservation templates and official MR dev only as locked validation. It does not use, translate, modify, or imitate the official benchmark.
