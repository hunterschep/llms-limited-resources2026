# External Public Data Plan

External data is expected for competitiveness, especially Ukrainian MT, Sorbian QA, robust SC/GC, and non-benchmark math preservation. It must be registered before download/use.

Config:

- `configs/data/external_sources.yaml`

Scripts:

- `scripts/register_external_data.py`
- `scripts/download_external_data.py`
- `scripts/validate_data_governance.py`

Candidate categories:

- Ukrainian public en-uk and cs-uk parallel corpora.
- Ukrainian monolingual, educational, grammar, and spelling resources.
- Sorbian prior WMT training resources, explicitly excluding WMT2025 test sets.
- Public hsb/dsb text and grammar/orthography material.
- German, Czech, and Polish transfer data where licensing permits.
- Public non-benchmark math datasets that are not derived from the official MR benchmark.

Retrieval is allowed only as a training-time tool:

```text
public source text -> retrieval -> teacher generation/filtering -> verified example -> student model
```

The submitted model must not depend on live RAG.
