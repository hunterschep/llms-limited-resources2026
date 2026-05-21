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
- Prompt-only base evaluations are complete for Ukrainian and Sorbian.
- Ukrainian and Sorbian specialist all-task evaluations are running.
- Failure cases will be collected after `results/eval_runs.jsonl` and per-model result JSONs are available.
- Sorbian prompt-only baseline is weak overall at 27.539, with QA as the strongest task and MR at 0. This gives the Sorbian merge/polish pipeline a low but clear baseline.
- Preliminary Ukrainian language specialist result: MT and SC improve slightly over prompt-only, but MR accuracy drops to 0 on locked validation. This suggests the language skill vector should receive a controlled merge weight and MR preservation must be monitored closely.
- Preliminary Ukrainian official-only baseline result: QA improves over prompt-only, but SC/GC correction and MR collapse. This is the first measured negative-transfer signal from supervised tuning and supports keeping official-only SFT as a comparison baseline rather than a likely final candidate.
- Preliminary Ukrainian naive multitask baseline result: SC improves, QA improves modestly, but MT, GC, and MR fall enough that overall remains below prompt-only. This is the expected baseline failure mode for the skill-vector thesis.
- Preliminary Ukrainian task-balanced baseline result: task balancing is stronger than naive multitask but still slightly below prompt-only because MR drops to 0 and MT falls. This suggests data balance helps but does not solve interference alone.
- Preliminary Ukrainian external-enhanced baseline result: governed external data improves the best baseline to 32.839, above prompt-only, but MT remains below base and MR remains 0. External data helps but still does not solve all-task interference.
- Preliminary Ukrainian MT specialist result: overall rises to 34.541 through QA/SC/GC gains, but MT chrF++ falls below prompt-only and MR remains 0. This specialist may be useful in a low-to-moderate weighted merge for editing/QA transfer, but should not be selected by its task name alone and should be paired with MR preservation.
- Preliminary Ukrainian edit specialist result: M_edit does not improve the intended edit aggregate over the stronger M_lang/M_mt candidates and drops overall to 30.088. Unless later merge search finds complementary behavior, this vector should receive a low weight.
- Preliminary Ukrainian QA specialist result: M_qa improves overall to 33.410 while keeping MT close to prompt-only and improving QA/SC, but MR remains 0. This looks safer than M_mt for MT preservation but still needs MR protection in merge search.
- Preliminary Sorbian language specialist result: M_lang improves MT by 3.290 chrF++ but loses 6.918 QA points and is below base overall. This vector should be considered for low MT-support weight rather than as a dominant Sorbian merge component.
