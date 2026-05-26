# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 2}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.1`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "24", "normalized_reference": "18", "prediction": "24"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "25000", "normalized_reference": "70000", "prediction": "150% від 50 000 $ = 75 000 $.\nВідсоткова вигода = 75 000 $ - 50 000 $ = 25 000 $.\n\n25 000 $"}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "60", "normalized_reference": "20", "prediction": "20 * 3 = 60"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "8", "normalized_reference": "64", "prediction": "16 склянок.\n\n1.  **Обчислення ціни першої склянки:** 5 $.\n2.  **Обчислення ціни другої склянки:** 60% від 5 $ = 0.6 \\times 5 = 3 $.\n3.  **Обчислення кількості склянок за ціною 3 $:** 3 $ / 3 $ = 1 склянка.\n4.  **Обчислення кількості склянок за ціною 5 $:** 5 $ / 5 $ = 1 склянка.\n5.  **Обчислення загальної кількості склянок:** 1 + 1 = 2 склянки за ціну 5 $.\n6.  **Обчислення кількості склянок за ціною 6 $:** 6 $ / 6 $ = 1 склянка.\n7.  **Обчислення загальної кількості склянок:** 2 + 1 = 3 склянки за ціну 6 $.\n8.  **Обчислення загальної кількост"}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.35`
- `prediction_counts`: `{"0": 14, "2": 1, "3": 4, "4": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000016", "normalized_prediction": "3", "prediction": "3"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.5, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 4, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 8}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`
