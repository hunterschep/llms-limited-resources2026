# Phase 4 Remote Cleanup Manifest

Remote cleanup was run in `/home/scheppat/workspace/projects/wmt26_lrllm` before Phase 4 prompt-sweep submission.

Deleted remote checkpoint directories:

- `checkpoints/sorbian/merged/search_candidate_001`
- `checkpoints/sorbian/merged/weighted_task_vector`
- `checkpoints/sorbian/merged/search_candidate_000`
- `checkpoints/sorbian/specialists/qa`
- `checkpoints/uk/specialists/mt`
- `checkpoints/uk/specialists/qa`
- `checkpoints/uk/merged/search_candidate_001`
- `checkpoints/uk/merged/weighted_task_vector`
- `checkpoints/uk/merged/search_candidate_000`

Deleted remote checkpoint files:

- `checkpoints/sorbian/merged/search/candidate_weights.jsonl`
- `checkpoints/uk/merged/search/candidate_weights.jsonl`

Remote cleanup validation after deletion:

- `make phase4-cleanup-check` passed.
- Remaining home-project checkpoint file: `checkpoints/.gitkeep`.
