# Final Sorbian Package

Primary package:

```text
/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian_primary_package/
```

Packaged model path:

```text
/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/sorbian_primary_package/model
```

Source model:

```text
/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/task_vector_merge_probe/mt1p00_edit0p10_mr0p10
```

Validation:

- Package creation job: `2505804`, completed.
- Package validation job: `2505805`, completed.
- Transformers load check: passed.
- Required files found: `config.json`, `tokenizer_config.json`.
- WMT constraints recorded: Qwen3.5-family <=2B, one model for all tasks, no task adapter switching, no live RAG.

Known risk:

- SC/GC no-error behavior is not fixed. The package is recommended only as the best available Sorbian fallback after final salvage.
