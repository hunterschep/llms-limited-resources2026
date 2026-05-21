# Phase 3 Retrain Error Analysis

Status: partial. Ukrainian normalized fixed evaluation is complete; Sorbian fixed candidate evaluation is still running.

## Ukrainian Findings So Far

The corrected evaluator raises prompt-only Ukrainian MR from the old 4.17 to 29.17, so the earlier "MR collapse to zero" was substantially a parser/normalization artifact. The retrained models still do not solve MR:

- Fixed `M_mr` MR accuracy is 20.83, below prompt-only 29.17.
- Fixed `M_mr` improves QA to 38.81 but nearly eliminates SC/GC correction, so it behaves like a narrow answer-format/QA-shift adapter rather than a robust math-preservation vector.
- Fixed task-balanced falls to 8.33 MR, suggesting the corrected mixture still causes negative transfer into math.

The edit remediation changed the failure mode:

- First-pass edit data encouraged always-error behavior.
- Balanced fixed `M_edit` no longer shows a pure always-error prior, but checkpoint-loading samples and locked validation show it often emits `CORRECT/CORRECT`.
- The result is false-negative-heavy behavior, especially for GC: fixed `M_edit` GC detection F1 is 29.19 and GC correction F1 is 0.0.

The fixed Ukrainian multitask runs are not fallback candidates:

- Fixed task-balanced: 23.92 overall.
- Fixed external-enhanced: 23.55 overall.
- Both severely damage GC and MR.

## Current Working Theory

The pipeline plumbing is sane: oracle, data sanity, same-set overfit, and checkpoint-loading gates passed. The failures look like data-mixture/generalization failures:

- SC/GC synthetic correction data can be overfit but does not match official locked validation well enough.
- Adding clean examples fixed the class-prior artifact but overcorrected toward no-error responses.
- MR preservation data is too small and too distributionally narrow; fine-tuning on it degrades the base model's broader arithmetic behavior.
- Task-balanced/external-enhanced configs are still too brittle: they improve some QA behavior but collapse exact edit correction and MR.

Required analyses after fixed evaluation:

- SC/GC false-positive no-error failures.
- SC/GC false-negative missed-error failures.
- SC/GC wrong-word versus wrong-correction failures.
- SC/GC malformed or verbose outputs.
- MR normalized exact matches.
- MR parser-rescued answers.
- MR wrong numeric answers.
- MR nonnumeric, verbose, or empty outputs.
- Cross-task regressions versus prompt-only.

Use:

```bash
python3 scripts/report_scgc_confusion.py --input <raw_prediction_dump.jsonl>
python3 scripts/report_mr_raw_errors.py --input <raw_prediction_dump.jsonl>
```
