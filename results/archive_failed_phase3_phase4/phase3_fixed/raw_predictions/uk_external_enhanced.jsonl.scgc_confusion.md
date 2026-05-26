# SC/GC Confusion Report

## GC

- Rows: `10`
- No-error accuracy: `1.000`
- Malformed/verbose rate: `0.000`
- Categories: `{"correct_no_error": 3, "false_negative_correct": 7}`
- Failure sample:
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: радників\nCorrect word: радниками", "id": "ukr_gc_dev:0002", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: проблемам\nCorrect word: проблем", "id": "ukr_gc_dev:0009", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: забаві\nCorrect word: забава", "id": "ukr_gc_dev:0012", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: купівлі\nCorrect word: купівлею", "id": "ukr_gc_dev:0017", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: місцям\nCorrect word: місць", "id": "ukr_gc_dev:0018", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`

## SC

- Rows: `10`
- No-error accuracy: `1.000`
- Malformed/verbose rate: `0.000`
- Categories: `{"correct_error_correction": 1, "correct_no_error": 6, "false_negative_correct": 3}`
- Failure sample:
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: котр\nCorrect word: котрій", "id": "ukr_sc_dev:0016", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: тваpини\nCorrect word: тварини", "id": "ukr_sc_dev:0022", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: троєл\nCorrect word: трохи", "id": "ukr_sc_dev:0026", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
