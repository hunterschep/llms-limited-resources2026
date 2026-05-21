# SC/GC Confusion Report

## GC

- Rows: `10`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.200`
- Categories: `{"false_positive_error": 2, "malformed_output": 2, "wrong_wrong_word": 6}`
- Failure sample:
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: радників\nCorrect word: радниками", "id": "ukr_gc_dev:0002", "raw_prediction": "Wrong word: мета\nCorrect word: мета"}`
  - `{"category": "malformed_output", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_gc_dev:0008", "raw_prediction": "Wrong word: роблять Correct word: роблять"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: проблемам\nCorrect word: проблем", "id": "ukr_gc_dev:0009", "raw_prediction": "Wrong word: цілої Correct word: цілої\nCorrect word: цілої"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_gc_dev:0011", "raw_prediction": "Wrong word: Ортеново намнєсті\nCorrect word: Ортеново-намнесті"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: забаві\nCorrect word: забава", "id": "ukr_gc_dev:0012", "raw_prediction": "Wrong word: найгірше Correct word: найгірше\nCorrect word: забаві"}`

## SC

- Rows: `10`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.100`
- Categories: `{"correct_error_correction": 1, "false_positive_error": 6, "malformed_output": 1, "wrong_wrong_word": 2}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0008", "raw_prediction": "Wrong word: законний Correct word: законний\nCorrect word: законний"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0012", "raw_prediction": "Wrong word: тренованих Correct word: тренованіх\nCorrect word: тренованих"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: котр\nCorrect word: котрій", "id": "ukr_sc_dev:0016", "raw_prediction": "Wrong word: котр Correct word: котрий\nCorrect word: залежить від того, о котрий зранку ви встаєте."}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0019", "raw_prediction": "Wrong word: нажене\nCorrect word: нажене"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0021", "raw_prediction": "Wrong word: речовина Correct word: речовина\nCorrect word: речовина"}`
