# Prediction Dump Diagnostics

## GC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.8235294117647058}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 7, "gold_correct": 3, "gold_error": 7, "pred_correct": 0, "pred_error": 10, "total": 10, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 10}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 7}`

## MR

- `rows`: `10`
- `accuracy`: `0.1`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "12", "normalized_reference": "18", "prediction": "12"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "25000", "normalized_reference": "70000", "prediction": "25000$"}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "100", "normalized_reference": "20", "prediction": "100"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "10.4", "normalized_reference": "64", "prediction": "10.40"}`

## MT

- `rows`: `10`

## QA

- `rows`: `10`
- `accuracy`: `0.0`
- `prediction_counts`: `{"0": 9, "2": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000001", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 6, "detection_tn": 0, "detection_tp": 4, "gold_correct": 6, "gold_error": 4, "pred_correct": 0, "pred_error": 10, "total": 10, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 10}`
- `gold_label_counts`: `{"CORRECT": 6, "ERROR": 4}`
