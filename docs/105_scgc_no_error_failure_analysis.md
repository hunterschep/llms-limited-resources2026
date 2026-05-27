# SC/GC No-Error Failure Analysis

Audit command:

```bash
python3 scripts/final_salvage_scgc_audit.py
```

Outputs:

- `results/final_salvage/scgc_audit/scgc_audit.json`
- `results/final_salvage/scgc_audit/scgc_audit.md`

Key result:

| Model | SC no-error | GC no-error | SC pred CORRECT | GC pred CORRECT | Diagnosis |
|---|---:|---:|---:|---:|---|
| prompt-only | 0.000 | 0.000 | 0/1167 | 0/985 | Always predicts an edit under current prompt. |
| selected lineage merge | 0.000 | 0.000 | 0/1167 | 0/985 | Always predicts an edit under current prompt. |
| edit_repair_tiny | 0.000 | 0.000 | 0/1167 | 0/985 | Always predicts an edit under current prompt. |
| reproduced Stage B | 0.000 | 0.000 | 0/1167 | 0/985 | Always predicts an edit under current prompt. |

Conclusions:

- Parser misclassification is not the dominant failure; outputs are usually parseable two-line edit outputs.
- The no-error collapse is not unique to the selected merge. Prompt-only and Stage B also predict an edit for every SC/GC item under the current local prompt.
- The dominant failure is a prompt/model prior that treats SC/GC as "find an error" tasks rather than "find an error or return CORRECT/CORRECT."
- This is a hidden-test risk because the official WMT26 task description requires either correcting an error or indicating that there is no error.
