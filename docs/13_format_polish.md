# Format Polish

Scripts:

- `scripts/build_format_preference_data.py`
- `scripts/train_format_polish.py`

Configs:

- `configs/train/uk/final_polish.yaml`
- `configs/train/sorbian/final_polish.yaml`

This stage is small and targeted. It should not add broad knowledge. It exists to eliminate metric-killing output behavior:

- SC/GC full-sentence rewrites instead of two-line output.
- Hallucinated corrections for clean cases.
- Verbose QA answers instead of answer identifiers.
- Chain-of-thought or long derivations for MR.
- Summary-like translations or omitted paragraphs.

Supported modes:

- Contrastive SFT using chosen/rejected pairs.
- Small format-alignment SFT.
- DPO when the full training environment supports it.

DPO source: https://papers.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html
