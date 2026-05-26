# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.35`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "32", "normalized_reference": "18", "prediction": "16 * 2 = 32"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "0", "normalized_reference": "70000", "prediction": "150% = 1.5\nВартість будинку після ремонту = 80 000 + (80 000 * 1.5) = 80 000 + 120 000 = 200 000 $\nВартість будинку до ремонту = 80 000 $\nВідсоток втрати = (80 000 / 200 000) * 100% = 40%\nВідсоток втрати = (80 000 / 80 000) * 100% = 100%\nВідсоток втрати = (80 000 / 200 000) * 100% = 40%\nВідсоток втрати = (80 000 / 80 000) * 100% = 100%\nВідсоток втрати = (80 000 / 200 0"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "89", "normalized_reference": "64", "prediction": "16 * 5 = 80\n16 - 1 = 15\n15 * 0.6 = 9\n80 + 9 = 89"}`
  - `{"gold": "260", "id": "ukr_mr_dev:low-ukr-6", "normalized_prediction": "240", "normalized_reference": "260", "prediction": "240"}`
  - `{"gold": "160", "id": "ukr_mr_dev:low-ukr-7", "normalized_prediction": "120", "normalized_reference": "160", "prediction": "120 хвилин"}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.25`
- `prediction_counts`: `{"0": 18, "2": 1, "3": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000001", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.4, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 3, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 4}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`
