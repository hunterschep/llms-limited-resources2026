# Competitive Format Polish Policy

Final polish is blocked until a candidate meaningfully beats prompt-only, moves MT, preserves auxiliary tasks, and is packageable.

Allowed polish data:

- Exact SC/GC two-line output.
- `CORRECT/CORRECT` no-error cases.
- QA label only.
- MR final answer only.
- MT translation only.
- No explanation, no full-sentence edit rewrite, no chain-of-thought, no JSON/list formatting.

Polish must be tiny. Evaluate before and after. If polish reduces MT or overall, discard it.
