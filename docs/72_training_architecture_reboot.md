# Training Architecture Reboot

## Stages

Stage A: language acquisition or real MT acquisition.

- Sorbian: DAPT/continued pretraining on hsb/dsb monolingual and short instruction replay.
- Ukrainian: real MT adaptation on high-quality en-uk/cs-uk data.

Stage B: MT adaptation.

- Sorbian: all six directions with bidirectional expansion, prior WMT train/support, and optional backtranslation.
- Ukrainian: continued real MT with document/paragraph-preserving examples.

Stage C: instruction and auxiliary replay.

- QA, SC, GC, MR, and format examples are mixed to recover multitask behavior without erasing MT gains.

Stage D: format alignment.

- Tiny exact-format pass only after a competitive base candidate exists.

## Supported Modes

- `qlora_dapt`
- `qlora_sft`
- `lora_sft`
- `stagewise_resume`
- `adapter_scale_eval`
- `base_interpolation`
- `model_soup`
- `ties_merge` when implemented and justified

## Evaluation Policy

Evaluate after every stage. Do not wait until final polish to discover collapse. Direction-level MT is mandatory, and equal-weighted overall remains the model-selection target.
