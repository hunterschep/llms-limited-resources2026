# Official Evaluator Reconciliation

Status: pending check.

The local harness currently computes MT chrF++/BLEU, QA/MR accuracy, SC/GC detection and correction F1, and the equal-weighted aggregate. When the organizers publish an official evaluation repository or update the official scripts, compare parsers and metrics against the local harness, then rerun final candidates if needed.

Sources to check:

- https://www2.statmt.org/wmt26/limited-resources-llm.html
- https://github.com/TUM-NLP/llms-limited-resources2026

If no official evaluator is available, document that the internal scorer remains the active validation proxy.
