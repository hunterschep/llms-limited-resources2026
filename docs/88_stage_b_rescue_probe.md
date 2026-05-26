# Stage B Rescue Probe

Generated at commit `6b389f1795aeabbb0dcf22c86ade71a12da54711`.

This probe is a fixed-seed, low-cost gate before full locked validation. It samples all five Sorbian tasks, keeps all MR rows because MR is tiny, and stratifies MT across all six directions.

## Outputs

- `MT`: `data/processed/stage_b_rescue/sorbian/probe/mt_probe.jsonl` (360 rows, sha256 `5bc63840cd40320b2ed5513a64b69ec07ec4e19b5a8d6c5153dcf82b99ff411a`)
- `QA`: `data/processed/stage_b_rescue/sorbian/probe/qa_probe.jsonl` (159 rows, sha256 `d9131e7182e95cc334dc3d27b337902a6353b0a6a2c84f12ee12b51da8430e6a`)
- `SC`: `data/processed/stage_b_rescue/sorbian/probe/sc_probe.jsonl` (240 rows, sha256 `137580898ceac32c39c4db39e684119efb154ebe7bc63bd5ad67f51abe92f1a8`)
- `GC`: `data/processed/stage_b_rescue/sorbian/probe/gc_probe.jsonl` (240 rows, sha256 `da6aa8ca27ff8093e4ffc02ab3365168357747203003634a806388673d8dfe3f`)
- `MR`: `data/processed/stage_b_rescue/sorbian/probe/mr_probe.jsonl` (48 rows, sha256 `80fa539824b10633d26e3d38db770ba8ca137525e669090ceee85f88a3f21649`)

## Probe Gates

- MT average chrF++ must stay at or above `41.0`.
- MR must be at least Stage B MR on the probe and preferably recover prompt-only.
- SC/GC must not drop by more than one point relative to Stage B probe scores.
- Malformed edit output must not spike.
- Overall probe score must beat the Stage B probe before full evaluation.
