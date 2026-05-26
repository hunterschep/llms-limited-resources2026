# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.15`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "26", "normalized_reference": "18", "prediction": "16 - 3 = 13 (яєць залишається на продаж).\n13 * 2 = 26 (доларів)."}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "187.5", "normalized_reference": "70000", "prediction": "150% від 50 000 $ = 75 000 $.\nВсього витрачено на будинок: 80 000 $ + 75 000 $ = 155 000 $.\nВартість будинку після ремонту: 80 000 $ + 150 000 $ = 230 000 $.\nВартість будинку до ремонту: 80 000 $.\nВідсоткова вигода: $\\frac{230 000 - 80 000}{80 000} \\times 100\\% = \\frac{150 000}{80 000} \\times 100\\% = 1.875 \\times 100\\% = 187.5\\%$."}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "60 × 3 = 180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "60", "normalized_reference": "20", "prediction": "20 * 3 = 60"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "8", "normalized_reference": "64", "prediction": "16 склянок — це 16 одиниць.\nПерша склянка коштує 5 $.\nОстанні 15 склянок коштують 60 % від ціни першої склянки.\nСума для останніх 15 склянок: $5 \\times 0.6 = 3 $.\nВсього склянок: $1 + 15 = 16$.\nЗагальна сума: $5 + 3 = 8 $."}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.3`
- `prediction_counts`: `{"0": 17, "2": 3}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000001", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.5, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 4, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 5}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`
