# Prediction Dump Diagnostics

## GC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.0}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 7, "detection_fp": 2, "detection_tn": 1, "detection_tp": 0, "gold_correct": 3, "gold_error": 7, "pred_correct": 8, "pred_error": 2, "total": 10, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"CORRECT": 8, "ERROR": 2}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 7}`

## MR

- `rows`: `10`
- `accuracy`: `0.1`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "24", "normalized_reference": "18", "prediction": "24"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "25000", "normalized_reference": "70000", "prediction": "25 000 $"}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 * 60 = 180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "60", "normalized_reference": "20", "prediction": "20 * 3 = 60"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "240", "normalized_reference": "64", "prediction": "240"}`

## MT

- `rows`: `10`

## QA

- `rows`: `10`
- `accuracy`: `0.3`
- `prediction_counts`: `{"0": 2, "1": 1, "2": 6, "4": 1}`
- `wrong_examples` sample:
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "4", "prediction": "4"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000020", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000026", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.4, "detection_f1": 0.6666666666666666}`
- `confusion`: `{"correction_exact": 1, "detection_fn": 2, "detection_fp": 0, "detection_tn": 6, "detection_tp": 2, "gold_correct": 6, "gold_error": 4, "pred_correct": 8, "pred_error": 2, "total": 10, "wrong_word_exact": 1}`
- `predicted_label_counts`: `{"CORRECT": 8, "ERROR": 2}`
- `gold_label_counts`: `{"CORRECT": 6, "ERROR": 4}`
