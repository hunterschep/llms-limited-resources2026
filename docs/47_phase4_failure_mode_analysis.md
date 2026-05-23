# Phase 4 Failure Mode Analysis

Phase 3 remediation made the evaluator and data gates sane, but the fixed full retrains still failed preservation gates.

| hypothesis | status | evidence | remediation |
| --- | --- | --- | --- |
| H1 overtraining/aggressive LoRA | supported | Fixed full retrains underperform despite compact overfit; old settings used LR 5e-5 to 2e-4 and hundreds of steps on narrow data. | low LR, low rank, assistant-only loss, early probe stopping |
| H2 synthetic edit mismatch | strongly supported | Balanced edit data still fails locked SC/GC exact correction and shifts priors. | official-style hard negatives and one-token real corrections before more volume |
| H3 prompt mismatch | partially supported | Raw outputs show malformed/MR verbosity for some candidates and CORRECT/CORRECT overuse. | prompt sweep and per-task decoding caps |
| H4 catastrophic forgetting | strongly supported | MR and GC collapse in multitask runs; prompt-only is strong after normalization. | KL-to-base, replay, adapter scaling |
| H5 bad mixture | supported | Task-balanced/external-enhanced hurt exact edit and MR even when QA/MT move. | strong caps and preservation-first ablations |
| H6 eval mismatch/noise | partially supported | MR is tiny and exact SC/GC is brittle, but failures are large enough to be real. | probe plus gated full eval only |

Key conclusion: the next training step must minimize drift from Qwen3.5-2B, use assistant-only target masking, and gate all candidates against prompt-only before full validation.

Sources preserved: https://www2.statmt.org/wmt26/limited-resources-llm.html and https://github.com/TUM-NLP/llms-limited-resources2026.
