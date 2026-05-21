# Prediction Dump Diagnostics

## GC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.0}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 2, "detection_fp": 0, "detection_tn": 3, "detection_tp": 0, "gold_correct": 3, "gold_error": 2, "pred_correct": 5, "pred_error": 0, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"CORRECT": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

## MR

- `rows`: `5`
- `accuracy`: `0.0`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "hsb_mr_dev:low-hsb-0", "normalized_prediction": "20", "normalized_reference": "18", "prediction": "20"}`
  - `{"gold": "3", "id": "hsb_mr_dev:low-hsb-1", "normalized_prediction": "20", "normalized_reference": "3", "prediction": "20"}`
  - `{"gold": "70000", "id": "hsb_mr_dev:low-hsb-2", "normalized_prediction": "50", "normalized_reference": "70000", "prediction": "50.000 US-dolarow."}`
  - `{"gold": "540", "id": "hsb_mr_dev:low-hsb-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 × 60 = 180"}`
  - `{"gold": "20", "id": "hsb_mr_dev:low-hsb-4", "normalized_prediction": "25", "normalized_reference": "20", "prediction": "25"}`

## MT

- `rows`: `5`

## QA

- `rows`: `5`
- `accuracy`: `0.6`
- `prediction_counts`: `{"1": 2, "2": 3}`
- `wrong_examples` sample:
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H01", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H9", "normalized_prediction": "2", "prediction": "2"}`

## SC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 1, "detection_fp": 1, "detection_tn": 2, "detection_tp": 1, "gold_correct": 3, "gold_error": 2, "pred_correct": 3, "pred_error": 2, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"CORRECT": 3, "ERROR": 2}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`
