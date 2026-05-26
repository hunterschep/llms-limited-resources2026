# Ukrainian Targeted Next Steps

Ukrainian is secondary in Stage B rescue.

Current state:

| Model | Overall | MT | QA | SC | GC | MR |
|---|---:|---:|---:|---:|---:|---:|
| Prompt-only | 37.399 | 40.990 | 34.278 | 46.917 | 35.646 | 29.167 |
| Best trained Stage A | 34.636 | 41.889 | 37.960 | 38.825 | 33.672 | 20.833 |

The real-data Ukrainian MT/QA signal exists, but edit and MR damage destroys overall. No Ukrainian checkpoint is an active candidate.

Allowed Ukrainian work in this phase:

- Prompt/decoding sweep only.
- UA-GEC/UD edit calibration analysis.
- MT data audit by direction.

Disallowed for now:

- Another broad Ukrainian stagewise training wave.
- Packaging a Ukrainian trained checkpoint.
- Merging Ukrainian failed checkpoints.
