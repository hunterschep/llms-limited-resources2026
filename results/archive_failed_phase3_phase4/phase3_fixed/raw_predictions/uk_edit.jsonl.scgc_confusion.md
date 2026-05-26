# SC/GC Confusion Report

## GC

- Rows: `10`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.000`
- Categories: `{"false_negative_correct": 7, "false_positive_error": 3}`
- Failure sample:
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: радників\nCorrect word: радниками", "id": "ukr_gc_dev:0002", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_gc_dev:0008", "raw_prediction": "Wrong word: Чому\nCorrect word: Чому"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: проблемам\nCorrect word: проблем", "id": "ukr_gc_dev:0009", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_gc_dev:0011", "raw_prediction": "Wrong word: Ортеново\nCorrect word: Ортен"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: забаві\nCorrect word: забава", "id": "ukr_gc_dev:0012", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`

## SC

- Rows: `10`
- No-error accuracy: `0.667`
- Malformed/verbose rate: `0.000`
- Categories: `{"correct_error_correction": 2, "correct_no_error": 4, "false_negative_correct": 1, "false_positive_error": 2, "wrong_wrong_word": 1}`
- Failure sample:
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: котр\nCorrect word: котрій", "id": "ukr_sc_dev:0016", "raw_prediction": "Wrong word: о\nCorrect word: як"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0021", "raw_prediction": "Wrong word: речовина\nCorrect word: речовина"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "ukr_sc_dev:0023", "raw_prediction": "Wrong word: в\nCorrect word: в"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: троєл\nCorrect word: трохи", "id": "ukr_sc_dev:0026", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
