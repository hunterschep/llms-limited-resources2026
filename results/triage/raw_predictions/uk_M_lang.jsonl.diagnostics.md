# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 3}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.2`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "64", "normalized_reference": "18", "prediction": "16 * 4 = 64"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "75000", "normalized_reference": "70000", "prediction": "150% від 50 000 $ = 75 000 $.\nВартість будинку після ремонту становить 80 000 + 75 000 = 155 000 $.\nВартість будинку до ремонту становила 80 000 $.\nВигода = 155 000 $ - 80 000 $ = 75 000 $.\n\n75 000"}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "120", "normalized_reference": "20", "prediction": "15 * 3 + 25 * 3 = 45 + 75 = 120"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "16", "normalized_reference": "64", "prediction": "16 склянок."}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.25`
- `prediction_counts`: `{"0": 18, "2": 2}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000001", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.5882352941176471, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 5, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 8}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`

