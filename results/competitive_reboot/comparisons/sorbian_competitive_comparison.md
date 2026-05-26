# Competitive Comparison

Baseline: `results/competitive_reboot/eval/sorbian/prompt_only_qwen35_2b.json` overall=29.195

| Candidate | Overall | Delta | MT | QA | SC | GC | MR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `results/competitive_reboot/eval/sorbian/stage_a_dapt_large.json` | 30.067 | +0.871 | 26.765 | 51.572 | 34.539 | 33.289 | 4.167 |
| `results/competitive_reboot/eval/sorbian/stage_b_mt_large.json` | 32.826 | +3.631 | 43.335 | 48.428 | 34.708 | 33.493 | 4.167 |
| `results/competitive_reboot/eval/sorbian/stage_c_instruction_replay.json` | 21.250 | -7.945 | 43.790 | 47.170 | 7.098 | 1.942 | 6.250 |
