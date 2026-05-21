# Evaluation Protocol

Evaluation entrypoint:

```bash
python3 scripts/eval_model.py --config configs/eval/uk.yaml --oracle --limit 5
python3 scripts/eval_model.py --config configs/eval/sorbian.yaml --oracle --limit 5
```

`--oracle` uses references as predictions and is intended only for smoke testing. Real model evaluation omits `--oracle`.

Metrics:

- MT: chrF++ and BLEU. Uses `sacrebleu` when available; otherwise a small fallback metric is used for smoke tests only.
- QA: exact-match accuracy over answer identifiers.
- MR: exact-match accuracy after whitespace normalization.
- SC/GC: detection F1 and correction F1 parsed from the two-line output format.

Internal aggregate:

```text
MT_score = average chrF++ over required directions
QA_score = accuracy * 100
SC_score = mean(detection_F1, correction_F1) * 100
GC_score = mean(detection_F1, correction_F1) * 100
MR_score = accuracy * 100
overall_score = mean(MT_score, QA_score, SC_score, GC_score, MR_score)
```

The harness supports:

- Base Qwen3.5-2B prompt-only evaluation.
- Official-train-only baselines.
- Naive multitask and task-balanced SFT baselines.
- Language-adapted models.
- Specialist models.
- Merged candidates.
- Final polished models.

If the official WMT26 evaluator differs, this wrapper should call the official evaluator and record the difference here.
