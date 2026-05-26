# Phase 4 Dashboard

Status: Phase 4 prompt sweep, micro-ablations, and gated full locked validation have completed. Ukrainian has no meaningful trained improvement, so prompt-only remains the safe Ukrainian fallback. Sorbian `edit_preserve_low_lr` at adapter scale 0.35 is a modest safe improvement and is the only Phase 4 checkpoint currently eligible for preservation.

## Prompt-Only Probe Anchors

- Ukrainian prompt-only probe: overall 37.969; MT 41.757, QA 33.333, SC 52.252, GC 33.333, MR 29.167
- Sorbian prompt-only probe: overall 29.644; MT 31.553, QA 43.750, SC 33.333, GC 33.333, MR 6.250

## Prompt Sweep

- uk: best prompt variant `edit_guarded` overall 38.323
- sorbian: best prompt variant `mr_numeric` overall 29.147

No prompt-sweep variant passed no-harm gates.

## Gated Full Locked Validation

| candidate | path | overall | MT | QA | SC | GC | MR | scale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UK prompt-only full anchor | results/phase4/gated_eval/uk_prompt_only_anchor.json | 37.399 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 |  |
| UK mr_preserve_kl@0.1 | results/phase4/gated_eval/uk_mr_preserve_kl_scale_0p1.json | 37.401 | 41.074 | 34.278 | 47.166 | 35.322 | 29.167 | 0.1 |
| Sorbian prompt-only full anchor | results/phase4/gated_eval/sorbian_prompt_only_anchor.json | 29.195 | 27.477 | 43.396 | 33.685 | 33.084 | 8.333 |  |
| Sorbian edit_preserve_low_lr@0.35 | results/phase4/gated_eval/sorbian_edit_preserve_low_lr_scale_0p35.json | 29.794 | 27.561 | 42.138 | 33.685 | 33.084 | 12.500 | 0.35 |

Full no-harm gate reports: `results/phase4/gates/full_uk_no_harm_report.md` and `results/phase4/gates/full_sorbian_no_harm_report.md`.

Merge search remains blocked because only one Phase 4 candidate passed full locked validation. See `docs/53_phase4_gated_eval_results.md` and `docs/54_phase4_merge_readiness.md`.
