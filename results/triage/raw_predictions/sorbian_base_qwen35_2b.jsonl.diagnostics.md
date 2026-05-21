# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 2}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.05`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "hsb_mr_dev:low-hsb-0", "normalized_prediction": "12", "normalized_reference": "18", "prediction": "12"}`
  - `{"gold": "3", "id": "hsb_mr_dev:low-hsb-1", "normalized_prediction": "24", "normalized_reference": "3", "prediction": "24"}`
  - `{"gold": "70000", "id": "hsb_mr_dev:low-hsb-2", "normalized_prediction": "130000", "normalized_reference": "70000", "prediction": "130000"}`
  - `{"gold": "540", "id": "hsb_mr_dev:low-hsb-3", "normalized_prediction": "60", "normalized_reference": "540", "prediction": "60"}`
  - `{"gold": "20", "id": "hsb_mr_dev:low-hsb-4", "normalized_prediction": "40", "normalized_reference": "20", "prediction": "15 + 25 = 40"}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.65`
- `prediction_counts`: `{"1": 6, "2": 13, "3": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "hsb_qa_dev:A1.1.H1", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H9", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.L2", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.L12", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.L14", "normalized_prediction": "2", "prediction": "2"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.6666666666666666}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 10, "detection_tn": 0, "detection_tp": 10, "gold_correct": 10, "gold_error": 10, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 3}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 10, "ERROR": 10}`

