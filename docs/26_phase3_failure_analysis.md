# Phase 3 Failure Analysis

Status: pending evaluation outputs. Specialist checkpoints are trained, but failure analysis requires completed all-five-task evaluations.

## Taxonomy

- MT: mistranslation, omission, hallucination, summarization, paragraph loss, dialogue loss, named-entity error, number/date error, terminology error, morphology/agreement error, direction-specific weakness.
- QA: wrong label, invalid output, answer-order bias, distractor confusion, lack of knowledge, language-comprehension failure, Sorbian certificate-style mismatch, Ukrainian MMLU/ZNO domain mismatch.
- SC: failed detection, wrong correction, hallucinated error on clean sentence, multiple-word output, punctuation/tokenization issue, diacritic issue.
- GC: failed agreement/case detection, wrong correction, spelling-vs-grammar confusion, hallucinated error on clean sentence, full-sentence rewrite.
- MR: arithmetic error, reasoning error, translation/language-comprehension error, invalid output format, verbosity, answer-extraction failure.

## Current Notes

- Specialist training completed for both tracks.
- Prompt-only base evaluations are running.
- Ukrainian and Sorbian specialist all-task evaluations are running.
- Failure cases will be collected after `results/eval_runs.jsonl` and per-model result JSONs are available.
