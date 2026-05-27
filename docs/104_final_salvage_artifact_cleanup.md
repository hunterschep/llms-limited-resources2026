# Final Salvage Artifact Cleanup

Active local namespace:

- `docs/103_*.md` onward
- `results/final_salvage/`

Active Andromeda namespace:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/final_salvage/`
- `/scratch/scheppat/projects/wmt26_lrllm/results/final_salvage/`
- `/home/scheppat/workspace/projects/wmt26_lrllm/results/final_salvage/`

Protected artifacts:

- selected lineage merge
- Stage A parent
- Stage B adapter
- Stage B merged model
- edit/MR repair deltas needed to reproduce the selected merge
- lineage result JSONs and package dry-run logs
- governance/source/data manifests and package/eval scripts

Cleanup policy:

- Delete failed final-salvage calibration checkpoints after summaries exist.
- Delete nonselected calibration merges after final package validation.
- Keep compact JSON/Markdown summaries.
- Do not delete the selected lineage merge or its preserved lineage handles until a validated better package exists.
