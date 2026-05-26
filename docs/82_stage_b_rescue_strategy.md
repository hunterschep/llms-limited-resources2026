# Stage B Rescue Strategy

Stage B is the first real competitive Sorbian signal in this project. It moves average Sorbian MT chrF++ from `27.477` to `43.335`, a `+15.858` gain, while improving QA and slightly improving SC/GC. It is not final because MR drops from `8.333` to `4.167` and overall reaches `32.826`, short of the `+5` overall rescue target.

The rescue strategy is therefore anchor-first:

1. Preserve Stage B as the MT/language checkpoint.
2. Do not use the failed Stage C broad replay recipe.
3. Diagnose MR and edit raw outputs before training.
4. Try prompt/decoding repair and adapter-scale/interpolation before weight updates.
5. If training is needed, use tiny MR/edit repair adapters from Stage B with MT anchor replay.
6. Full-evaluate only candidates that pass the Stage B rescue probe.

Official constraints remain active: WMT26 requires one Qwen3.5-family <=2B model per submitted track, all five tasks from that same model, public reproducible external data, chrF++ for MT, accuracy for QA/MR, SC/GC detection and correction F1, and equal weighting across the five task categories. The task page also prohibits using original or translated PolyMath for training or inference.

Sources preserved in this plan:

- WMT26 task page: https://www2.statmt.org/wmt26/limited-resources-llm.html
- Official repository: https://github.com/TUM-NLP/llms-limited-resources2026
- Qwen3.5-2B: https://huggingface.co/Qwen/Qwen3.5-2B
- LoRA: https://arxiv.org/abs/2106.09685
- QLoRA: https://arxiv.org/abs/2305.14314
- Model Soups: https://proceedings.mlr.press/v162/wortsman22a.html
- Task Arithmetic: https://openreview.net/forum?id=6t0Kwf8-jrj
- TIES-Merging: https://arxiv.org/abs/2306.01708
- DPO: https://papers.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html
- Forbidden PolyMath: https://huggingface.co/datasets/Qwen/PolyMath
