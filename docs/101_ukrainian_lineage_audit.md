# Ukrainian Lineage Audit

Ukrainian is frozen for this goal except for a cheap adapter-lineage audit if explicitly requested.

Current facts:

| Model | Overall | MT | QA | SC | GC | MR |
|---|---:|---:|---:|---:|---:|---:|
| prompt-only | 37.399 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 |
| best trained Stage A | 34.636 | 41.889 | 37.960 | 38.825 | 33.672 | 20.833 |

Conclusion:

- Ukrainian real-data training improves MT/QA but damages SC/MR too much.
- Prompt-only remains fallback.
- No Ukrainian checkpoint is currently a candidate.
- No broad Ukrainian training should run in lineage recovery.
