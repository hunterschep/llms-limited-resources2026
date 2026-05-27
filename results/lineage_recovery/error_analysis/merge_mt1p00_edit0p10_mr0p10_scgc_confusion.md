# SC/GC Confusion Report

## GC

- Rows: `985`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.013`
- Categories: `{"correct_error_correction": 2, "false_positive_error": 489, "malformed_output": 13, "right_wrong_word_wrong_correction": 59, "wrong_wrong_word": 422}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_gc_dev:0003", "raw_prediction": "Wrong word: principoweho\nCorrect word: principowego"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_gc_dev:0005", "raw_prediction": "Wrong word: najnjewoblubowaniši\nCorrect word: najnjesmjeršy"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: Miłoraza\nCorrect word: Miłorazu", "id": "hsb_gc_dev:0006", "raw_prediction": "Wrong word: wjedźe\nCorrect word: wjedźe"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_gc_dev:0010", "raw_prediction": "Wrong word: prajił\nCorrect word: pisał"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: nowember\nCorrect word: nowembru", "id": "hsb_gc_dev:0011", "raw_prediction": "Wrong word: organizuje\nCorrect word: organizuje"}`

## SC

- Rows: `1167`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.010`
- Categories: `{"correct_error_correction": 17, "false_positive_error": 590, "malformed_output": 12, "right_wrong_word_wrong_correction": 87, "wrong_wrong_word": 461}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0001", "raw_prediction": "Wrong word: zamołwitosć\nCorrect word: rozmłownosć\n\nWrong word: zasadne\nCorrect word: zasadne"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0004", "raw_prediction": "Wrong word: Leonardo DiCaprio\nCorrect word: Leonardo DiCaprio"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: bcuhu\nCorrect word: buchu", "id": "hsb_sc_dev:0005", "raw_prediction": "Wrong word: statysacy\nCorrect word: staty"}`
  - `{"category": "right_wrong_word_wrong_correction", "gold_target": "Wrong word: mpłě\nCorrect word: małe", "id": "hsb_sc_dev:0006", "raw_prediction": "Wrong word: mpłě\nCorrect word: młode"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0008", "raw_prediction": "Wrong word: naprawy\nCorrect word: naprawy\n\nWrong word: medicinsko-fachowym\nCorrect word: medikinsko-fachowym\n\nWrong word: koncipować\nCorrect word: koncipować\n\nWrong word: přewjesć\nCorrect word: přewjesć"}`
