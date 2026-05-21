# Skill-Vector Merging

Scripts:

- `scripts/merge_linear.py`
- `scripts/merge_task_vectors.py`
- `scripts/merge_ties.py`
- `scripts/search_merge_weights.py`

Configs:

- `configs/merge/uk.yaml`
- `configs/merge/sorbian.yaml`

For each track:

```text
Delta_lang   = M_lang   - M_base
Delta_mt     = M_mt     - M_base
Delta_edit   = M_edit   - M_base
Delta_qa     = M_qa     - M_base
Delta_mr     = M_mr     - M_base
Delta_format = M_format - M_base
```

Search:

```text
M_final = M_base
        + a Delta_lang
        + b Delta_mt
        + c Delta_edit
        + d Delta_qa
        + e Delta_mr
        + f Delta_format
```

Objective:

```text
overall_score = mean(MT_score, QA_score, SC_score, GC_score, MR_score)
```

Never optimize only MT. The merge scripts have dry-run modes for config validation and real checkpoint modes once local trained checkpoints exist.

Background:

- Model Soups: https://proceedings.mlr.press/v162/wortsman22a.html
- Task Arithmetic: https://openreview.net/forum?id=6t0Kwf8-jrj
- TIES-Merging: https://arxiv.org/abs/2306.01708
