# Phase 4 Dashboard

Status: real prompt-only probe anchors and prompt sweeps have completed on Andromeda. No prompt variant has passed no-harm gates yet, so micro-ablations are the next active stage.

## Prompt-Only Probe Anchors

- Ukrainian prompt-only probe: overall 37.969; MT 41.757, QA 33.333, SC 52.252, GC 33.333, MR 29.167
- Sorbian prompt-only probe: overall 29.644; MT 31.553, QA 43.750, SC 33.333, GC 33.333, MR 6.250

## Prompt Sweep

- uk: best prompt variant `edit_guarded` overall 38.323
- sorbian: best prompt variant `mr_numeric` overall 29.147

No-harm gate reports: `results/phase4/gates/prompt_sweep_uk_no_harm_report.md` and `results/phase4/gates/prompt_sweep_sorbian_no_harm_report.md`.

See `docs/45_phase4_preservation_pivot_plan.md` through `docs/54_phase4_merge_readiness.md`.
