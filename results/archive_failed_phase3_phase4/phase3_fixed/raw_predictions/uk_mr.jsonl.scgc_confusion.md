# SC/GC Confusion Report

## GC

- Rows: `10`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.600`
- Categories: `{"false_positive_error": 1, "malformed_output": 6, "wrong_wrong_word": 3}`
- Failure sample:
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: радників\nCorrect word: радниками", "id": "ukr_gc_dev:0002", "raw_prediction": "Wrong word: створеного Correct word: створеного\nCorrect word: радників Correct word: радників"}`
  - `{"category": "malformed_output", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_gc_dev:0008", "raw_prediction": "Wrong word: роблять Correct word: роблять"}`
  - `{"category": "malformed_output", "gold_target": "Wrong word: проблемам\nCorrect word: проблем", "id": "ukr_gc_dev:0009", "raw_prediction": "Wrong word: цілої Correct word: цілого"}`
  - `{"category": "malformed_output", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_gc_dev:0011", "raw_prediction": "Wrong word: Ортеново намнєсті Correct word: Ортеново намисті"}`
  - `{"category": "malformed_output", "gold_target": "Wrong word: забаві\nCorrect word: забава", "id": "ukr_gc_dev:0012", "raw_prediction": "Wrong word: забаві Correct word: забавно"}`

## SC

- Rows: `10`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.100`
- Categories: `{"false_positive_error": 6, "malformed_output": 1, "wrong_wrong_word": 3}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0008", "raw_prediction": "Wrong word: законний Correct word: законний\nCorrect word: законний"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0012", "raw_prediction": "Wrong word: кілерів Correct word: китів\nCorrect word:"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: котр\nCorrect word: котрій", "id": "ukr_sc_dev:0016", "raw_prediction": "Wrong word: о котр Correct word: о котрі\nCorrect word: залежить від того, о котрі зранку ви встаєте."}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0019", "raw_prediction": "Wrong word: адреналіну Correct word: адреналіну\nCorrect word: адреналіну"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0021", "raw_prediction": "Wrong word: речовина Correct word: речовина\nCorrect word: речовина"}`
