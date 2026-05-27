# SC/GC Logit Calibration

Log-probability or two-pass calibration is diagnostic unless WMT26 confirms deterministic inference rules are allowed during hidden evaluation.

Diagnostic idea:

- compare log probability of CORRECT/CORRECT against generated edit output
- learn a threshold on a tune split only
- apply threshold to produce no-error outputs when the model internally prefers CORRECT

This was not the first final-salvage path because a packageable one-model checkpoint is safer under the official model-submission framing.
