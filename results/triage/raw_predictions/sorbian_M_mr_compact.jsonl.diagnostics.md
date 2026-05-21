# Prediction Dump Diagnostics

## GC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 2, "gold_correct": 3, "gold_error": 2, "pred_correct": 0, "pred_error": 5, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

## MR

- `rows`: `5`
- `accuracy`: `0.0`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "hsb_mr_dev:low-hsb-0", "normalized_prediction": "128", "normalized_reference": "18", "prediction": "128"}`
  - `{"gold": "3", "id": "hsb_mr_dev:low-hsb-1", "normalized_prediction": "10", "normalized_reference": "3", "prediction": "10"}`
  - `{"gold": "70000", "id": "hsb_mr_dev:low-hsb-2", "normalized_prediction": "130000", "normalized_reference": "70000", "prediction": "130000"}`
  - `{"gold": "540", "id": "hsb_mr_dev:low-hsb-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "180"}`
  - `{"gold": "20", "id": "hsb_mr_dev:low-hsb-4", "normalized_prediction": "100", "normalized_reference": "20", "prediction": "100"}`

## MT

- `rows`: `5`

## QA

- `rows`: `5`
- `accuracy`: `0.6`
- `prediction_counts`: `{"1": 4, "2": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "hsb_qa_dev:A1.1.H1", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H9", "normalized_prediction": "2", "prediction": "2"}`

## SC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 2, "gold_correct": 3, "gold_error": 2, "pred_correct": 0, "pred_error": 5, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

