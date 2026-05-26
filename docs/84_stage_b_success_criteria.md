# Stage B Success Criteria

## Minimum Rescue Target

- Keep average MT chrF++ at or above `41.0`.
- Prefer MT near Stage B: `43.335`.
- Improve MR above Stage B `4.167`, preferably back to prompt-only `8.333`.
- Keep SC and GC at or above prompt-only, or at least avoid any collapse.
- Reach overall `34.195` if possible, which is `+5` over prompt-only.
- Absolute minimum useful candidate: overall above Stage B `32.826` and MT at or above `41.0`.

## Hard Rejection

- MT below `38.0`, unless overall jumps dramatically and the tradeoff is explicitly selected.
- SC or GC collapse.
- Old Stage C replay recipe.
- Any Phase 3/4 checkpoint as a merge or training base.
- Any candidate that cannot run all five tasks as one model.
- Any forbidden or non-reproducible data.

## Candidate Labels

- `final_candidate`
- `promising_needs_more_repair`
- `MT_anchor_only`
- `rejected_MT_loss`
- `rejected_MR_loss`
- `rejected_edit_collapse`
- `rejected_not_packageable`
