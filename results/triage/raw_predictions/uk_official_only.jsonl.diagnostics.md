# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.3`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "128", "normalized_reference": "18", "prediction": "128"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "50", "normalized_reference": "70000", "prediction": "150% від 50 000 $ = 75 000 $.\nВідсоткова вигода = (75 000 - 50 000) / 50 000 = 25 000 / 50 000 = 0.5 = 50%.\nВідповідь: 50%"}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 * 60 = 180"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "100", "normalized_reference": "64", "prediction": "100$"}`
  - `{"gold": "260", "id": "ukr_mr_dev:low-ukr-6", "normalized_prediction": "240", "normalized_reference": "260", "prediction": "240"}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.45`
- `prediction_counts`: `{"0": 8, "1": 4, "2": 5, "3": 2, "4": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000020", "normalized_prediction": "1", "prediction": "1"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`

