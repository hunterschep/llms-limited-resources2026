# Edit No-Error Calibration

Stage B and `edit_repair_tiny` still have weak SC/GC no-error behavior. The failed Stage C recipe destroyed edit performance, so calibration is tiny and targeted.

Data:

- hard no-error hsb/dsb examples
- near-miss examples where the model tends to hallucinate an error
- one-token SC correction examples
- one-token GC correction examples
- exact `Wrong word:` / `Correct word:` two-line targets
- official-style length distribution
- separate hsb/dsb balance where sources allow it

Ratio sweeps:

- 60/40 clean/error
- 50/50 clean/error
- 40/60 clean/error

Methods:

- prompt/decoding calibration first
- tiny LoRA calibration
- task-vector merge of the calibration delta into the best interpolated candidate

Gates:

- MT drop `<=1.0`
- SC and GC no-error accuracy improve
- correction F1 does not collapse
- MR does not regress
- overall improves or stays within 0.2 while fixing pathology
