# Phase 4 Gated Evaluation Results

Status: completed on Andromeda jobs `2504124` and `2504125`.

Full locked validation was run only for the current prompt-only anchor and the top nonzero-scale probe-gated candidate for each track.

| track | candidate | overall | MT | QA | SC | GC | MR | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ukrainian | prompt-only anchor | 37.399 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 | fallback |
| Ukrainian | `mr_preserve_kl@0.1` | 37.401 | 41.074 | 34.278 | 47.166 | 35.322 | 29.167 | blocked: +0.002 overall is not meaningful and has no >=1 point task gain |
| Sorbian | prompt-only anchor | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 | baseline |
| Sorbian | `edit_preserve_low_lr@0.35` | 29.794 | 27.561 | 42.138 | 33.685 | 33.084 | 12.500 | pass: modest safe improvement |

No-harm gate outputs:

- `results/phase4/gates/full_uk_no_harm_report.json`: no Ukrainian candidate passed full-gated no-harm because the tiny overall delta did not include a real task gain.
- `results/phase4/gates/full_sorbian_no_harm_report.json`: Sorbian `checkpoints/phase4/sorbian/edit_preserve_low_lr/adapter@scale=0.35` passed.

Interpretation:

- Ukrainian remains prompt-only for now. The Phase 4 MR-preservation adapter is safe but not useful enough to justify replacing the anchor.
- Sorbian has one safe improved candidate. It improves overall by +0.599, mainly through MR (+4.167) and a small MT gain (+0.084), while QA drops -1.258 and SC/GC are unchanged.
- The Sorbian result is a valid preservation-first recovery signal, but it is not enough to resume merge search by itself because there is only one full-gated candidate and no complementary validated vector.

Result files:

- `results/phase4/gated_eval/uk_prompt_only_anchor.json`
- `results/phase4/gated_eval/uk_mr_preserve_kl_scale_0p1.json`
- `results/phase4/gated_eval/sorbian_prompt_only_anchor.json`
- `results/phase4/gated_eval/sorbian_edit_preserve_low_lr_scale_0p35.json`
