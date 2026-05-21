# Specialist Training

Specialist configs:

- `configs/train/uk/lang.yaml`
- `configs/train/uk/mt.yaml`
- `configs/train/uk/edit_scgc.yaml`
- `configs/train/uk/qa.yaml`
- `configs/train/uk/mr.yaml`
- `configs/train/uk/format.yaml`
- `configs/train/sorbian/lang.yaml`
- `configs/train/sorbian/mt.yaml`
- `configs/train/sorbian/edit_scgc.yaml`
- `configs/train/sorbian/qa.yaml`
- `configs/train/sorbian/mr.yaml`
- `configs/train/sorbian/format.yaml`

Specialists:

- `M_lang`: language acquisition with instruction preservation.
- `M_mt`: translation.
- `M_edit`: spell checking and grammar checking.
- `M_qa`: multiple-choice QA.
- `M_mr`: math preservation and final-answer behavior.
- `M_format`: exact WMT output formatting.

These are training artifacts only. The final system must be one architecture, one set of weights, one model per track, no adapter switching, no hidden ensemble, and no inference-time RAG dependency.

The training entrypoints support dry-run, checkpoint output directories, seed control, gradient accumulation, mixed precision through Transformers/PyTorch, and config-driven runs. Andromeda jobs add environment setup, logs, caches, and resume-friendly checkpoint paths.
