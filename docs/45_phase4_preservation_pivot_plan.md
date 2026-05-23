# Phase 4 Preservation Pivot Plan

Status: active.

Phase 3 remediation is complete. The MR parser normalization is fixed, the SC/GC edit class-balance issue was fixed, and oracle/data-sanity/compact-overfit/checkpoint-loading gates pass. The fixed retrains are still not merge-safe: Ukrainian fixed retrains all underperform the normalized prompt-only baseline, and Sorbian external-enhanced is only a weak diagnostic fallback rather than a clean skill vector. Merge search and final polish remain blocked.

The normalized Qwen3.5-2B prompt-only baseline is now the anchor to beat:

| Track | Candidate | Overall | Status |
|---|---:|---:|---|
| Ukrainian | prompt-only normalized | 37.399 | anchor |
| Ukrainian | fixed `M_edit` | 28.736 | blocked |
| Ukrainian | fixed `M_mr` | 33.527 | blocked |
| Ukrainian | fixed task-balanced | 23.922 | blocked |
| Ukrainian | fixed external-enhanced | 23.552 | blocked |
| Sorbian | prompt-only normalized | 29.195 | anchor |
| Sorbian | fixed `M_edit` | 22.684 | blocked |
| Sorbian | fixed `M_mr` | 29.187 | blocked |
| Sorbian | fixed task-balanced | 25.551 | blocked |
| Sorbian | fixed external-enhanced | 30.004 | diagnostic fallback only |

Phase 4 rule: no broad retraining. Every trained candidate must be preservation-first, evaluated on a small probe before full locked validation, and rejected if it improves one task by damaging the equal-weighted objective.

Allowed next steps:

- Build fixed Phase 4 probes.
- Run prompt/decoding sweeps before training.
- Train only small low-impact LoRA candidates with assistant-only loss masking, replay, optional KL-to-base, low rank, low LR, and short step counts.
- Evaluate adapter scale before assuming scale 1.0.
- Full-evaluate only candidates that pass no-harm probe gates.

Official constraints remain grounded in:

- https://www2.statmt.org/wmt26/limited-resources-llm.html
- https://github.com/TUM-NLP/llms-limited-resources2026
