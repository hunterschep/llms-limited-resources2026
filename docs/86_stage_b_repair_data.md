# Stage B Repair Data

Generated at commit `6b389f1795aeabbb0dcf22c86ade71a12da54711`.

The repair dataset is intentionally small and targeted. It is not a repeat of the failed Stage C broad replay.

## Outputs

- `mr_repair`: `data/processed/stage_b_rescue/sorbian/mr_repair.jsonl` (240 rows, sha256 `d84aa33300638a98914efca36c0842131b99fed0c23eb97cf0b38c0efe9b28e5`)
- `edit_repair`: `data/processed/stage_b_rescue/sorbian/edit_repair.jsonl` (720 rows, sha256 `85ae0228145e4feca621aa9a259a29020d8a924722344f4c23bc29ac52d6e31a`)
- `format_repair`: `data/processed/stage_b_rescue/sorbian/format_repair.jsonl` (96 rows, sha256 `c354943cd93e2cc06de32b86f60e8329f0b9136aedfd39a1730aea62a6c1fa18`)
- `mt_anchor`: `data/processed/stage_b_rescue/sorbian/mt_anchor.jsonl` (12000 rows, sha256 `6ee2e65c38cfb7e0071493c6a889e8b395e656085afcfefd4923a478acd7dacd`)
- `combined_repair`: `data/processed/stage_b_rescue/sorbian/combined_repair.jsonl` (13056 rows, sha256 `52f66f10db3b2f85368ba7883022e7ca5ebbb0ddb407b0ccb574ccd72e1f0e28`)

## Policy

- MR rows come from governed public non-PolyMath arithmetic sources and keep final-answer-only targets.
- Edit errors come from governed synthetic SC/GC compilers; clean hard negatives are generated from public/official Sorbian MT anchor text, not locked validation.
- MT anchor rows are sampled from the Stage B MT training pool across all six directions.
- Every row carries `source_id`, `task`, `language`, `split`, `generation_method`, and `contamination_checked`.

## mr_repair

```json
{
  "by_generation_method": {
    "stage_b_rescue_mr_final_answer_repair": 240
  },
  "by_language": {
    "dsb": 120,
    "hsb": 120
  },
  "by_source_id_top20": {
    "external:gsm8k_train": 240
  },
  "by_task": {
    "MR": 240
  },
  "rows": 240
}
```

## edit_repair

```json
{
  "by_generation_method": {
    "stage_b_rescue_hard_no_error_from_public_mt_anchor": 360,
    "stage_b_rescue_one_word_edit_error_repair": 360
  },
  "by_language": {
    "dsb": 345,
    "hsb": 375
  },
  "by_source_id_top20": {
    "official:sorb_mono_dsb": 169,
    "official:sorb_mono_hsb": 191,
    "official:train_de-dsb_2026": 142,
    "official:train_de-hsb_2026": 151,
    "official:train_hsb-dsb_2026": 67
  },
  "by_task": {
    "GC": 360,
    "SC": 360
  },
  "rows": 720
}
```

## format_repair

```json
{
  "by_generation_method": {
    "stage_b_rescue_format_exact_edit_two_line": 35,
    "stage_b_rescue_format_mr_final_answer": 16,
    "stage_b_rescue_format_mt_translation_only": 45
  },
  "by_language": {
    "de": 15,
    "dsb": 46,
    "hsb": 35
  },
  "by_source_id_top20": {
    "external:gsm8k_train": 16,
    "official:sorb_mono_dsb": 7,
    "official:sorb_mono_hsb": 7,
    "official:train_de-dsb_2026": 27,
    "official:train_de-hsb_2026": 23,
    "official:train_hsb-dsb_2026": 16
  },
  "by_task": {
    "GC": 19,
    "MR": 16,
    "MT": 45,
    "SC": 16
  },
  "rows": 96
}
```

## mt_anchor

```json
{
  "by_generation_method": {
    "stage_b_rescue_mt_anchor_replay": 12000
  },
  "by_language": {
    "de": 4000,
    "dsb": 4000,
    "hsb": 4000
  },
  "by_source_id_top20": {
    "official:train_de-dsb_2026": 4000,
    "official:train_de-hsb_2026": 4000,
    "official:train_hsb-dsb_2026": 4000
  },
  "by_task": {
    "MT": 12000
  },
  "rows": 12000
}
```

## combined_repair

```json
{
  "by_generation_method": {
    "stage_b_rescue_format_exact_edit_two_line": 35,
    "stage_b_rescue_format_mr_final_answer": 16,
    "stage_b_rescue_format_mt_translation_only": 45,
    "stage_b_rescue_hard_no_error_from_public_mt_anchor": 360,
    "stage_b_rescue_mr_final_answer_repair": 240,
    "stage_b_rescue_mt_anchor_replay": 12000,
    "stage_b_rescue_one_word_edit_error_repair": 360
  },
  "by_language": {
    "de": 4015,
    "dsb": 4511,
    "hsb": 4530
  },
  "by_source_id_top20": {
    "external:gsm8k_train": 256,
    "official:sorb_mono_dsb": 176,
    "official:sorb_mono_hsb": 198,
    "official:train_de-dsb_2026": 4169,
    "official:train_de-hsb_2026": 4174,
    "official:train_hsb-dsb_2026": 4083
  },
  "by_task": {
    "GC": 379,
    "MR": 256,
    "MT": 12045,
    "SC": 376
  },
  "rows": 13056
}
```
