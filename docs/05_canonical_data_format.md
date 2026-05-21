# Canonical Data Format

Every compiler emits canonical JSONL examples compatible with `src/wmt26/data/schema.py`.

Required core fields:

```json
{
  "id": "...",
  "track": "ukrainian|sorbian",
  "task": "MT|QA|SC|GC|MR|LANG|FORMAT",
  "language": "uk|ukr|hsb|dsb|de|en|cs|pl",
  "source_language": "...",
  "target_language": "...",
  "input": "...",
  "target": "...",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "source_id": "...",
  "source_type": "official|external|synthetic|teacher_generated|distilled",
  "license": "...",
  "split": "train|tune|locked_validation|test_placeholder",
  "is_synthetic": false,
  "generation_method": null,
  "contamination_checked": true
}
```

Prompt templates live under `configs/prompts/` and are rendered by `src/wmt26/prompts/templates.py`.

Prompt rules:

- MT: return only the translation; preserve meaning, names, numbers, punctuation, paragraph breaks, and dialogue turns.
- QA: return only the correct answer identifier.
- SC/GC: return exactly `Wrong word: ...` and `Correct word: ...`.
- MR: return only the final answer; no chain-of-thought.

Prompt strings are config-driven. Training scripts should not hardcode task prompts.
