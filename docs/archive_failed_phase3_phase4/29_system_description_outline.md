# System Description Outline

## Working Title

Skill-Vector Merged Curriculum Adaptation for Low-Resource Multitask LLMs

## Core Claim

WMT26 requires one small model to perform five heterogeneous tasks under severe data scarcity. We construct public task curricula for missing supervision, train specialist skill adaptations, merge the learned task vectors into a single compliant model, and apply final behavior polish for exact output formats.

## Contributions

1. Public low-resource curriculum/data factory for MT, QA, SC, GC, and MR.
2. Morphology-aware SC/GC compilers.
3. Sorbian triangle-consistency MT setup.
4. RAG-to-weights QA distillation design without inference-time retrieval.
5. Interference-aware skill-vector merging.
6. Exact-format behavior polish.

## Evidence Tables

Dataset mixture, baselines, specialists, interference matrix, merge search, polish before/after, final selected results, and failure taxonomy counts.
