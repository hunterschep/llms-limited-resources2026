# Data Ablation Plan

Ukrainian ablations:

- Base Qwen prompt-only.
- Official-only baseline.
- Official + Ukrainian MT external.
- Official + SC/GC external.
- Official + generated QA.
- Official + MR preservation.
- External-enhanced multitask.
- Specialist merged model.
- Merged + polish.

Sorbian ablations:

- Base Qwen prompt-only.
- Official-only baseline.
- Official + prior WMT/Leipzig when manually approved.
- Official + generated Sorbian QA.
- Official + improved SC/GC synthetic.
- Official + MR preservation.
- External-enhanced multitask.
- Specialist merged model.
- Merged + polish.

Use `scripts/report_eval_comparison.py` to combine JSON eval outputs.
