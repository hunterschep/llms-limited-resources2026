# Phase 4 Andromeda Job Status

Submitted from local commit `4b82e7ec4e12d41a8e1c2c5338ba0a510e3504e2`.

## Prompt/Decoding Probe Sweep

| Track | Active Job ID | Job | Partition | GPU | Memory | Status at submission | Notes |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| Ukrainian | 2486271 | `phase4_prompt_sweep_uk` | `interactive` | `a100:1` | `32G` | `PD (Resources)` | H200 jobs `2486261`, `2486262`, A100-short jobs `2486263`, `2486264`, L40S-short jobs `2486265`, `2486266`, and 96G interactive jobs `2486269`, `2486270` were canceled after scheduler diagnostics showed unavailable nodes or per-user memory limits. |
| Sorbian | 2486272 | `phase4_prompt_sweep_sorbian` | `interactive` | `a100:1` | `32G` | `PD (Resources)` | Same fallback sequence as Ukrainian. |

Micro-ablations remain blocked until `results/phase4/probe/baseline_prompt_only_uk.json` and `results/phase4/probe/baseline_prompt_only_sorbian.json` exist from real model inference.
