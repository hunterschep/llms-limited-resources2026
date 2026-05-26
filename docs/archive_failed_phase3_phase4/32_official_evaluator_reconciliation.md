# Official Evaluator Reconciliation

Status: checked 2026-05-20; official WMT26 evaluator is not yet available in the public task repository.

The local harness currently computes MT chrF++/BLEU, QA/MR accuracy, SC/GC detection and correction F1, and the equal-weighted aggregate. When the organizers publish an official evaluation repository or update the official scripts, compare parsers and metrics against the local harness, then rerun final candidates if needed.

## 2026-05-20 Check

- `git ls-remote https://github.com/TUM-NLP/llms-limited-resources2026.git` reports public upstream `main` at `fba93a07d74051d7ab9add465599e891e65d3966`.
- `git ls-tree -r FETCH_HEAD` after fetching upstream shows the official repository currently contains README/data files only; no evaluator scripts, lm-evaluation-harness fork, or scoring wrapper are present in that repo.
- The upstream README still says the organizers will provide a repository to help with evaluation and that it will be a fork of `lm-evaluation-harness`.
- Web search for a WMT26/TUM-NLP limited-resources LLM evaluation harness did not locate a public WMT26 evaluator repository. Search results still surface the WMT25 evaluator/reference material and generic lm-evaluation-harness pages.

Sources to check:

- https://www2.statmt.org/wmt26/limited-resources-llm.html
- https://github.com/TUM-NLP/llms-limited-resources2026

Until the official evaluator is released, the internal scorer remains the active validation proxy. Final selected checkpoints should be rerun through the official harness once it appears, and any parser/metric discrepancies should be recorded here before submission.
