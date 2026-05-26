# Phase 4 Artifact Hygiene

Status: initial local and remote hygiene checked on 2026-05-22.

Local state at Phase 4 start:

- Git was clean at commit `798b70ffcf1ba95dbe57f650e548007e8cff29e2`.
- `checkpoints/` was empty.
- Phase 3 fixed compact results were retained under `results/phase3_fixed/`.
- Cleanup manifests were retained under `results/cleanup/`.
- `.gitignore` ignores checkpoints, logs, caches, temporary artifacts, and generated data while allowing compact result JSON/JSONL/MD/CSV summaries.

Andromeda state at Phase 4 start:

- No WMT26 jobs were active.
- Other non-WMT Formosan jobs were active or queued; Phase 4 jobs must avoid flooding the queue.
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints`: 22G.
- `/scratch/scheppat/projects/wmt26_lrllm/results`: 0.
- `/home/scheppat/workspace/projects/wmt26_lrllm/results`: 3.2M.
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase3_fixed`: empty.

Phase 4 namespaces:

- Local compact outputs: `results/phase4/`.
- Local docs: `docs/45_*.md` onward.
- Remote checkpoints: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/phase4/`.
- Remote scratch results: `/scratch/scheppat/projects/wmt26_lrllm/results/phase4/`.
- Remote project results: `/home/scheppat/workspace/projects/wmt26_lrllm/results/phase4/`.

Deletion policy:

- Delete failed ablation checkpoints after their compact metrics and diagnostics are preserved.
- Do not delete official data, governance registry, split manifests, Phase 3 closeout summaries, prompt-only normalized results, or cleanup manifests.
