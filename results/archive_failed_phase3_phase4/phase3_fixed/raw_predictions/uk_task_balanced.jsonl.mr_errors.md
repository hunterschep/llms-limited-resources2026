# MR Raw Error Report

- Rows: `10`
- Malformed/verbose rate: `0.200`
- Categories: `{"explanation_or_verbose_answer": 2, "parser_normalization_rescued": 1, "wrong_numeric_answer": 7}`
- Wrong examples:
  - `{"category": "wrong_numeric_answer", "gold_target": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "24", "normalized_reference": "18", "raw_prediction": "24"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "25000", "normalized_reference": "70000", "raw_prediction": "25 000 $"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "raw_prediction": "3 * 60 = 180"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "60", "normalized_reference": "20", "raw_prediction": "20 * 3 = 60"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "240", "normalized_reference": "64", "raw_prediction": "240"}`
