# Lineage-Preserving Training

The training path reproduces the successful Sorbian competitive reboot without the previous lineage loss.

## Stage A

Config: `configs/train/lineage_recovery/sorbian_stage_a_dapt_preserve.yaml`

Input:

- `data/processed/competitive/sorbian/stage_a_dapt_large.jsonl`

Outputs:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_a_dapt_parent/final_merged`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_a_dapt_adapter/final_adapter`
- milestone adapters/merges at steps 1500, 3000, 4500, 6000

## Stage B

Config: `configs/train/lineage_recovery/sorbian_stage_b_mt_preserve.yaml`

Parent:

- Stage A final merged checkpoint

Input:

- `data/processed/competitive/sorbian/stage_b_mt_large.jsonl`

Outputs:

- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_adapter`
- `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_merged`
- milestone adapters/merges at steps 2000, 4000, 6000, 8000

Reproduction gate:

- MT `>=41.0`
- overall `>=31.5`
- no catastrophic SC/GC collapse
- valid adapter-scale and interpolation artifacts

If reproduction fails, stop and compare configs/data/checksums against the original competitive reboot before training repairs.

## Completed Reproduction

The lineage-preserving Stage A and Stage B run completed on Andromeda with all required parent, adapter, merged, intermediate, config, checksum, and result artifacts preserved.

Final lineage paths:

- Stage A parent: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_a_dapt_parent/final_merged`
- Stage A adapter: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_a_dapt_adapter/final_adapter`
- Stage B adapter: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_adapter`
- Stage B merged: `/scratch/scheppat/projects/wmt26_lrllm/checkpoints/lineage_recovery/sorbian/stage_b_mt/final_merged`

Reproduced Stage B full eval:

| Overall | MT | QA | SC | GC | MR |
|---:|---:|---:|---:|---:|---:|
| 33.628 | 44.094 | 48.428 | 35.876 | 33.493 | 6.250 |

The reproduction exceeded the required MT and overall gates and restored model-surgery handles that were missing from the earlier Stage B run.
