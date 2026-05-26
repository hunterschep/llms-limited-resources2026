# Competitive Merging Plan

## Rule

Do not use merging as a substitute for a strong trained candidate. Merge only after Stage A/B/C produces real complementary signal.

## Allowed

- Checkpoint averaging among adjacent stage checkpoints.
- Model soup of top same-family checkpoints.
- Task-vector interpolation with base.
- TIES-style merge if implemented and validated.

## Ineligible

- Failed Phase 3/4 specialists.
- Tiny Phase 4 Sorbian edit adapter as a main vector.
- Forbidden/risky unreviewed data checkpoints.
- Partial/canceled checkpoints.
- Models whose loading was not verified.

## Comparisons

Every merge must be compared against prompt-only, best single candidate, Stage B MT, and Stage C replay.
