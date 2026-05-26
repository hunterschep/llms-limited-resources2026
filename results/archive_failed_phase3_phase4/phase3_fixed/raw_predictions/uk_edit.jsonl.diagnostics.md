# Prediction Dump Diagnostics

## GC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.0}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 7, "detection_fp": 3, "detection_tn": 0, "detection_tp": 0, "gold_correct": 3, "gold_error": 7, "pred_correct": 7, "pred_error": 3, "total": 10, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"CORRECT": 7, "ERROR": 3}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 7}`

## MR

- `rows`: `10`
- `accuracy`: `0.1`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "32", "normalized_reference": "18", "prediction": "16 * 2 = 32"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "187.5%", "normalized_reference": "70000", "prediction": "150% від 50 000 $ = 75 000 $.\nВсього витрачено на будинок: 80 000 + 75 000 = 155 000 $.\nВартість будинку після ремонту: 80 000 + 150 000 = 230 000 $.\nВартість будинку до ремонту: 80 000 $.\nВідсоток прибутку: (230 000 - 80 000) / 80 000 = 150 000 / 80 000 = 1.875 = 187.5%."}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 * 60 = 180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "60", "normalized_reference": "20", "prediction": "20 * 3 = 60"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "8", "normalized_reference": "64", "prediction": "16 склянок — це 16 одиниць.\nПерша склянка коштує 5 $.\nОстанні 15 склянок коштують 60 % від ціни першої склянки.\nСума ціни першої склянки: $5$.\nСума ціни 15 склянок: $5 \\times 0.6 = 3$.\nЗагальна сума: $5 + 3 = 8$."}`

## MT

- `rows`: `10`

## QA

- `rows`: `10`
- `accuracy`: `0.2`
- `prediction_counts`: `{"0": 7, "2": 3}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000001", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000020", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.6666666666666666, "detection_f1": 0.6666666666666665}`
- `confusion`: `{"correction_exact": 2, "detection_fn": 1, "detection_fp": 2, "detection_tn": 4, "detection_tp": 3, "gold_correct": 6, "gold_error": 4, "pred_correct": 5, "pred_error": 5, "total": 10, "wrong_word_exact": 2}`
- `predicted_label_counts`: `{"CORRECT": 5, "ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 6, "ERROR": 4}`
