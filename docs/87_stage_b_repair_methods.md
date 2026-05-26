# Stage B Repair Methods

## Order

1. Prompt/decoding repair: change generation limits and task instructions before changing weights.
2. Adapter-scale/interpolation: only if the preserved Stage B adapter can be applied to its original base checkpoint.
3. Tiny MR repair from Stage B: final-answer-only MR data plus MT anchor replay.
4. Tiny edit repair from Stage B: hard no-error SC/GC, one-word corrections, exact two-line format, and MT anchor replay.
5. Combined tiny repair: only if separate MR/edit repairs pass the probe.
6. Task-vector merge: only if separate repair deltas are useful and sequential SFT hurts.

## Disallowed

- Failed Stage C broad replay as training base or recipe.
- Phase 3/4 specialists.
- Locked validation as training data.
- PolyMath, translated PolyMath, modified PolyMath, or PolyMath-derived rows.

## Probe Before Full Eval

Every trained candidate must pass the Stage B rescue probe before full locked validation. Probe gates are MT >= `41.0`, no SC/GC collapse, no malformed output spike, MR at least Stage B and preferably prompt-only, and overall above the Stage B probe.

## Current Method Status

- Prompt/decoding sweep plan exists under `results/stage_b_rescue/prompt_sweep/prompt_sweep_plan.json` and is ready to run on Andromeda.
- Adapter-scale search is currently ruled out because Stage B was preserved as a merged checkpoint while the original Stage A base checkpoint was pruned. The preserved `stage_b_mt_large/adapter` cannot be safely re-applied without that exact base.
- Tiny MR and edit repair configs trained on Andromeda. MR repair improved the probe but failed full eval; edit repair improved both probe and full eval.
- Combined repair trained after separate repairs passed probe, but its probe MR regressed to Stage B level and it was not full-evaluated.
- Repair merge remains blocked because there are not two full-eval-positive repair vectors. The failed Stage C replay remains excluded.
