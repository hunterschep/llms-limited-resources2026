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

If a prompt-only variant beats the anchor without training, it becomes a valid no-training baseline. If prompt variants only help the probe but are not compatible with official submission prompts, record them as diagnostic.
