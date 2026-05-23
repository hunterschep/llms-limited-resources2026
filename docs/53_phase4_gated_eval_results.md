# Phase 4 Gated Evaluation Results

Status: no gated full-eval candidates yet.

Full locked validation should run only for prompt-only anchors and candidates that pass Phase 4 probe gates. Use:

```bash
python3 scripts/phase4_eval_gated_candidates.py --track uk --candidates results/phase4/gates/no_harm_report.json
python3 scripts/phase4_eval_gated_candidates.py --track sorbian --candidates results/phase4/gates/no_harm_report.json
```

If no candidates pass, prompt-only remains the fallback and merge remains blocked.
