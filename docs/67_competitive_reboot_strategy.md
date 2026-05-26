# Competitive Reboot Strategy

## Reset

The Phase 3/4 path is not competitive. Ukrainian reached only a meaningless `+0.002` tie over prompt-only, and Sorbian reached only `+0.599`, without the MT movement expected from serious low-resource adaptation. The reboot therefore stops optimizing around prompt-only preservation and rebuilds around large public data, language acquisition, MT adaptation, and controlled multitask replay.

## WMT26 Constraints

Official references:

- WMT26 task page: https://www2.statmt.org/wmt26/limited-resources-llm.html
- Official WMT26 GitHub: https://github.com/TUM-NLP/llms-limited-resources2026
- Qwen3.5-2B: https://huggingface.co/Qwen/Qwen3.5-2B

Each track must use one Qwen3.5-family model with no more than 2B parameters for all five tasks: MT, QA, SC, GC, and MR. External data must be public and reproducible. Hidden test data, WMT2025 test sets, Ukrainian UNLP/MMLU/ZNO test splits, PolyMath and derivatives, and extra Sorbian certificate questions are forbidden.

## Architecture

1. Data scale first: enable large governed public MT and monolingual corpora.
2. Language acquisition first for Sorbian; real MT first for Ukrainian.
3. Stagewise training: DAPT/language acquisition, MT SFT, instruction replay, format alignment.
4. Evaluation after every stage, with direction-level MT reporting.
5. Model soups or task-vector interpolation only after real candidates exist.
6. Final polish only after a competitive model exists.

## Selection Principle

A model may trade a few auxiliary-task points for large MT gains if equal-weighted overall improves materially. A model with no MT movement is not competitive unless it produces a large and robust auxiliary-task improvement.
