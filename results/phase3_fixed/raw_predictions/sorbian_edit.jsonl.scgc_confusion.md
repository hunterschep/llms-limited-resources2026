# SC/GC Confusion Report

## GC

- Rows: `5`
- No-error accuracy: `1.000`
- Malformed/verbose rate: `0.000`
- Categories: `{"correct_no_error": 3, "false_negative_correct": 2}`
- Failure sample:
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: Miłoraza\nCorrect word: Miłorazu", "id": "hsb_gc_dev:0006", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: nowember\nCorrect word: nowembru", "id": "hsb_gc_dev:0011", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`

## SC

- Rows: `5`
- No-error accuracy: `0.667`
- Malformed/verbose rate: `0.000`
- Categories: `{"correct_no_error": 2, "false_negative_correct": 1, "false_positive_error": 1, "wrong_wrong_word": 1}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0001", "raw_prediction": "Wrong word: dokelž\nCorrect word: dokelž"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: bcuhu\nCorrect word: buchu", "id": "hsb_sc_dev:0005", "raw_prediction": "Wrong word: statysacy\nCorrect word: statysacy"}`
  - `{"category": "false_negative_correct", "gold_target": "Wrong word: mpłě\nCorrect word: małe", "id": "hsb_sc_dev:0006", "raw_prediction": "Wrong word: CORRECT\nCorrect word: CORRECT"}`
