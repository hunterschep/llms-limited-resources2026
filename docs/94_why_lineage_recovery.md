# Why Lineage Recovery

The missing artifact is the Stage A DAPT parent used to create the successful Stage B MT-large LoRA/merged checkpoint. The Stage B adapter survived, but a LoRA adapter is only meaningful relative to the exact parent it was trained against. Applying it to base Qwen or a different parent would confound the MT delta with parent mismatch.

This blocked the critical rescue experiment:

Can we partially apply the MT adaptation to recover MR and SC/GC no-error behavior while retaining most of the `+15.858` MT chrF++ gain?

## Required Handles

The new run preserves:

- Base Qwen3.5-2B reference metadata
- Stage A DAPT parent checkpoint
- Stage A LoRA adapter
- Stage B MT adapter
- Stage B merged/full checkpoint
- Stage B intermediate adapters and materialized merged checkpoints
- tokenizer/config/generation config
- training configs
- data/source manifest checksums
- git commit
- eval config
- raw prediction samples
- full result JSON

## Deltas Needed

- `Delta_mt = StageB_MT - StageA_parent`
- `Delta_edit = EditCalibration - CandidateParent`
- `Delta_mr = MRRecovery - CandidateParent`

These allow:

- adapter-scale search over Stage B LoRA
- Stage A/Stage B interpolation
- base/StageB interpolation if meaningful
- task-vector merges anchored on Stage A
- later TIES/model soup only if real positive deltas exist

Parent checkpoints must not be pruned until `docs/100_lineage_recovery_results.md` and `docs/102_lineage_packaging_decision.md` make a final decision.
