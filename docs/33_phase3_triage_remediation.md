# Phase 3 Triage And Remediation

Status: active. The main Phase 3 training/merge campaign is paused.

## Why We Paused

The first measured Phase 3 results show useful learning signal, but also systematic failure modes that make merge search premature:

- Ukrainian `M_mt` is the best measured model so far at 34.541 overall versus 32.386 for prompt-only, so training is not inert.
- Sorbian `M_lang` improves MT from 27.527 to 30.818 chrF++, so language adaptation is useful.
- Every evaluated tuned Ukrainian model drops MR to 0.000, including the MR specialist.
- SC/GC detection F1 is suspiciously stable around the same value while correction F1 swings.
- Ukrainian `M_edit` does not behave like a reliable edit specialist.

The working hypothesis is pipeline/evaluation/data-mixture misalignment, not failure of the skill-vector idea.

## Remote Job Action Taken

On 2026-05-21, all remaining Andromeda Phase 3 jobs were canceled to prevent automatic merge/polish/final-eval execution against suspicious signals.

Canceled active eval jobs:

- `2461542` `eval_sorbian_baselines`
- `2461547` `eval_uk_specialists`
- `2461551` `eval_sorbian_specialists`

Canceled dependency-held jobs:

- `2461548` `merge_uk`
- `2461549` `polish_uk`
- `2461550` `eval_uk_final`
- `2461552` `merge_sorbian`
- `2461553` `polish_sorbian`
- `2461554` `eval_sorbian_final`

No further full training, merge search, or final polish should be launched until the gates below pass.

## Triage Gates

1. Oracle evaluator sanity:
   - `make triage-oracle`
   - QA, MR, SC, and GC must score 100 with gold targets as predictions.
   - MT oracle chrF++ should be very high; exact 100 is not required because corpus/tokenization behavior can produce minor deviations.

2. Raw prediction dumps:
   - Dump at least 20 examples per task for base, official-only, external-enhanced, `M_lang`, `M_mt`, `M_edit`, `M_qa`, and `M_mr`.
   - Each dump must include prompt, gold target, raw generation, parsed prediction, and metric decision.

3. MR normalization and output inspection:
   - Confirm whether model outputs are wrong, verbose-but-correct, language-formatted, boxed, decimal/integer variants, or parser failures.
   - The local evaluator now normalizes common forms such as `The answer is X`, `Відповідь: X`, boxed answers, thousands separators, and integer-like decimals.

4. SC/GC confusion matrices:
   - Inspect gold error versus predicted error.
   - Confirm whether detection F1 is a majority-class artifact or an actual detection signal.
   - Check wrong-word exact match and correction exact match separately.

5. Single-batch overfit:
   - Prepare/run 50-example same-set overfit tests for MT, QA, SC, GC, and MR.
   - A task that cannot overfit its own tiny training set is a training/checkpoint/prompt bug until proven otherwise.

6. Checkpoint loading:
   - Compare base versus trained checkpoint generations on the same prompts.
   - If outputs are identical or near-identical, inspect adapter saving/loading, checkpoint path resolution, and merge/unload behavior.

## New Triage Commands

Local no-model parser/oracle checks:

```bash
make triage-oracle
make triage-raw-oracle
```

Raw prediction dump on Andromeda or a GPU node:

```bash
python3 scripts/dump_raw_predictions.py --config configs/eval/uk.yaml --model checkpoints/uk/specialists/mr --per-task 20 --output results/triage/raw_predictions/uk_mr.jsonl
python3 scripts/diagnose_prediction_dump.py --input results/triage/raw_predictions/uk_mr.jsonl
```

Checkpoint loading comparison:

```bash
python3 scripts/check_checkpoint_loading.py --config configs/eval/uk.yaml --base-model Qwen/Qwen3.5-2B --checkpoint checkpoints/uk/specialists/mr --per-task 10
```

Single-batch overfit config preparation:

```bash
python3 scripts/run_single_batch_overfit.py --track uk --task MR --examples 50 --steps 80
```

On Andromeda, add `--execute` to actually train. Do not run those jobs until the oracle and raw-output checks have been inspected.

Prepared Andromeda triage jobs, not yet submitted:

```bash
sbatch andromeda/jobs/triage_oracle.slurm
sbatch andromeda/jobs/triage_raw_predictions_uk.slurm
sbatch andromeda/jobs/triage_raw_predictions_sorbian.slurm
sbatch andromeda/jobs/triage_checkpoint_loading_uk.slurm
sbatch andromeda/jobs/triage_checkpoint_loading_sorbian.slurm
```

If H200 placement blocks, use the documented fallback form:

```bash
sbatch --gres=gpu:a100:1 andromeda/jobs/triage_raw_predictions_uk.slurm
sbatch --gres=gpu:l40s:1 andromeda/jobs/triage_raw_predictions_uk.slurm
```

## First Oracle Result

Local oracle checks now pass after adding task-aware answer normalization:

- Ukrainian QA/MR/SC/GC oracle: 100.
- Sorbian QA/MR/SC/GC oracle: 100.
- Ukrainian MT oracle chrF++: 99.793.
- Sorbian MT oracle chrF++: 100.000.

This means the gross gold-target parser path is sane. The remaining question is whether trained model generations are semantically correct but parser-misaligned, or actually wrong.

## Restart Criteria

Resume Phase 3 merge/search only after:

- MR raw outputs explain the systematic 0.000 scores.
- SC/GC confusion matrices show detection is meaningful.
- `M_edit` overfits a tiny SC/GC set.
- `M_mr` overfits a tiny MR set or the MR curriculum/prompt is fixed.
- Checkpoint loading confirms trained checkpoints materially change outputs from base.
- The runbook records exactly which parser/training fixes were applied.
