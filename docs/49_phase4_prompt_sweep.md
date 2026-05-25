# Phase 4 Prompt And Decoding Sweep

Prompt/decoding sweep must run before more training because prompt-only Qwen3.5-2B is currently the safest baseline.

Implemented variants live in `configs/prompts/phase4_sweep.yaml`:

- `baseline`: current canonical prompts.
- `strict_short`: stricter exact-output instructions and shorter generation caps.
- `edit_guarded`: one-token SC/GC behavior and explicit no-error calibration.
- `mr_numeric`: shorter QA/MR output constraints.

Outputs:

- `results/phase4/prompt_sweep/uk/`
- `results/phase4/prompt_sweep/sorbian/`

Real Andromeda prompt-sweep jobs completed on 2026-05-23:

| Track | Job ID | Status | Best variant | Best probe overall | Gate status |
| --- | ---: | --- | --- | ---: | --- |
| Ukrainian | 2486271 | completed | `edit_guarded` | 38.323 | blocked: MR drop exceeds no-harm threshold |
| Sorbian | 2486272 | completed | `mr_numeric` | 29.147 | blocked: below prompt-only probe anchor |

Prompt-only probe anchors:

| Track | Overall | MT | QA | SC | GC | MR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ukrainian | 37.969 | 41.757 | 33.333 | 52.252 | 33.333 | 29.167 |
| Sorbian | 29.644 | 31.553 | 43.750 | 33.333 | 33.333 | 6.250 |

If a prompt-only variant beats the anchor without training, it becomes a valid no-training baseline. If prompt variants only help the probe but are not compatible with official submission prompts, record them as diagnostic.

Current status: no prompt variant has passed the no-harm gate.
