# SC/GC Confusion Report

## GC

- Rows: `5`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.200`
- Categories: `{"false_positive_error": 3, "full_sentence_or_verbose_output": 1, "wrong_wrong_word": 1}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_gc_dev:0003", "raw_prediction": "Wrong word: Hłowny\nCorrect word: Hlavný\n\nWrong word: terminoweho\nCorrect word: termínového\n\nWrong word: planowanja\nCorrect word: plánovania\n\nWrong word: Nječiń\nCorrect word: Njich\n\nWrong word: štož\nCorrect word: čo\n\nWrong word: móža\nCorrect word: môže\n\nWrong word: druzy\nCorrect word: druhy\n\nWrong word: činić\nCorrect word: čini"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_gc_dev:0005", "raw_prediction": "Wrong word: najnjewoblubowaniši\nCorrect word: najljubowaniši"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: Miłoraza\nCorrect word: Miłorazu", "id": "hsb_gc_dev:0006", "raw_prediction": "Wrong word: wjedźe\nCorrect word: wjeździ"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_gc_dev:0010", "raw_prediction": "Wrong word: prajił Correct word: prajal\nCorrect word: zo Correct word: zo"}`
  - `{"category": "full_sentence_or_verbose_output", "gold_target": "Wrong word: nowember\nCorrect word: nowembru", "id": "hsb_gc_dev:0011", "raw_prediction": "Wrong word: Towarstwo Wrong word: Mohorjeva/Hermagoras Wrong word: organizuje Wrong word: w wrong word: nowember wrong word: rjad wrong word: \"Mjeńšiny – Wokno do swěta\". Wrong word: Mjeńšiny – Wokno do swěta."}`

## SC

- Rows: `5`
- No-error accuracy: `0.000`
- Malformed/verbose rate: `0.000`
- Categories: `{"false_positive_error": 3, "wrong_wrong_word": 2}`
- Failure sample:
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0001", "raw_prediction": "Wrong word: zamołwitosć Correct word: zamowlitosć\nCorrect word: wokrjes"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0004", "raw_prediction": "Wrong word: wuzna Correct word: wznaj\nCorrect word: koleso"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: bcuhu\nCorrect word: buchu", "id": "hsb_sc_dev:0005", "raw_prediction": "Wrong word: opozicionelnych Correct word: opozycyjnych\nCorrect word: lěhwow Correct word: lehwow"}`
  - `{"category": "wrong_wrong_word", "gold_target": "Wrong word: mpłě\nCorrect word: małe", "id": "hsb_sc_dev:0006", "raw_prediction": "Wrong word: mpłě Correct word: płě\nCorrect word: bolosćiwki"}`
  - `{"category": "false_positive_error", "gold_target": "Wrong word: CORRECT\nCorrect word: CORRECT", "id": "hsb_sc_dev:0008", "raw_prediction": "Wrong word: dyrbja\nCorrect word: dyrbja\n\nCorrect word: dyrbja"}`
