# Phase 3 Remediation Retrain Plan

Status: remediation retrain wave complete. Merge search is blocked by `docs/42_phase3_resume_or_block_merge_decision.md`.

## What Failed

- First-pass tuned models produced suspicious MR collapse and SC/GC detection plateaus.
- SC/GC detection F1 around 66% was caused by edit training data that was nearly all error cases:
  - Ukrainian SC: 4506 error / 40 clean.
  - Ukrainian GC: 3531 error / 40 clean.
  - Sorbian SC: 2998 error / 77 clean.
  - Sorbian GC: 966 error / 69 clean.
- MR evaluation was initially too strict. It under-counted outputs such as `The answer is X`, `Відповідь: X`, boxed answers, and integer-like decimals.
- MR remains weak after parser normalization and needs stronger final-answer-only preservation.
- Ukrainian `M_edit` is invalid as an edit specialist because it was trained on the flawed edit mixture.
- Sorbian `M_lang` showed useful MT transfer but harmful auxiliary-task interference. It should not be merged until rerun or explicitly cleared.

## Already Fixed

- Final SC/GC mixtures now contain derived clean no-error counterparts:
  - Ukrainian SC: 9009 rows, 4506 error / 4503 clean.
  - Ukrainian GC: 7062 rows, 3531 error / 3531 clean.
  - Sorbian SC: 5757 rows, 2998 error / 2759 clean.
  - Sorbian GC: 1875 rows, 966 error / 909 clean.
- MR normalization now handles bare numbers, integer-like decimals, trailing punctuation, `The answer is`, `Answer:`, `Відповідь:`, boxed answers, fractions, and percentages.
- One malformed nonnumeric Ukrainian ASDiv target was removed from final MR data.
- Preference/chosen rows now append the chosen assistant response during SFT text construction.
- `train_sft.py` now honors task-balanced/capped sampling instead of blindly concatenating all train files.

## Resolved By Fixed Retraining

- Retrained `M_mr` did not recover prompt-only MR on Ukrainian and did not improve Sorbian MR enough to be useful.
- Balanced `M_edit` did not transfer to locked validation; it reduced the old always-error prior but produced too many missed errors and weak exact corrections.
- Ukrainian fixed task-balanced and external-enhanced models were worse than normalized prompt-only.
- Sorbian fixed external-enhanced modestly beat normalized prompt-only, but it is a diagnostic fallback result rather than a clean specialist vector.
- Merge search should not resume with this fixed wave.

## Artifact Eligibility

Eligible for comparison:

- Prompt-only base results in `results/baselines/`.
- Compact triage reports under `results/triage/`.
- Fixed normalized eval summaries under `results/phase3_fixed/`.
- Raw prediction diagnostics under `results/phase3_fixed/raw_predictions/`.

Preserved as diagnostics only:

- Raw first-pass prediction dumps under `results/triage/raw_predictions/`.
- Triage summaries and cleanup manifests.
- Sorbian fixed external-enhanced metric result.

Disqualified:

- First-pass Ukrainian/Sorbian baseline and specialist checkpoints.
- First-pass `M_edit`, `M_mr`, and any model trained on unbalanced SC/GC data.
- Any stale result JSON generated before normalized MR parsing.
- Any partial checkpoint from canceled jobs.
- Fixed retrain checkpoints from this wave; they were pruned from scratch after evaluation and are not merge inputs.

## Minimal Retraining Set Completed

Completed:

- Ukrainian fixed `M_edit`.
- Ukrainian fixed `M_mr`.
- Ukrainian fixed task-balanced baseline.
- Ukrainian fixed external-enhanced multitask baseline.
- Sorbian fixed `M_edit`.
- Sorbian fixed `M_mr`.
- Sorbian fixed task-balanced baseline.
- Sorbian fixed external-enhanced multitask baseline.

`M_lang`, `M_mt`, `M_qa`, and `M_format` were not retrained because the remediation targeted edit balance and MR parsing/preservation only.

## Must Not Be Merged

Do not merge any first-pass specialist, any fixed checkpoint from this wave, or any model whose checkpoint loading and normalized all-five-task eval have not been explicitly cleared. Merge search may only resume after a new, narrower remediation produces eligible checkpoints and `docs/42_phase3_resume_or_block_merge_decision.md` is updated.

References: WMT26 task page https://www2.statmt.org/wmt26/limited-resources-llm.html and official repository https://github.com/TUM-NLP/llms-limited-resources2026.
