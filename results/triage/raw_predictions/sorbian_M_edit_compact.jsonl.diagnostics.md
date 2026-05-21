# Prediction Dump Diagnostics

## GC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 2, "gold_correct": 3, "gold_error": 2, "pred_correct": 0, "pred_error": 5, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

## MR

- `rows`: `5`
- `accuracy`: `0.2`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "hsb_mr_dev:low-hsb-0", "normalized_prediction": "32", "normalized_reference": "18", "prediction": "32"}`
  - `{"gold": "3", "id": "hsb_mr_dev:low-hsb-1", "normalized_prediction": "5", "normalized_reference": "3", "prediction": "5"}`
  - `{"gold": "70000", "id": "hsb_mr_dev:low-hsb-2", "normalized_prediction": "50", "normalized_reference": "70000", "prediction": "50.000 US-dolarow."}`
  - `{"gold": "540", "id": "hsb_mr_dev:low-hsb-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 × 60 = 180"}`

## MT

- `rows`: `5`

## QA

- `rows`: `5`
- `accuracy`: `0.2`
- `prediction_counts`: `{"2": 5}`
- `wrong_examples` sample:
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H01", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H5", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H6", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H9", "normalized_prediction": "2", "prediction": "2"}`

## SC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 2, "gold_correct": 3, "gold_error": 2, "pred_correct": 0, "pred_error": 5, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

