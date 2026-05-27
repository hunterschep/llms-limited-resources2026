# MR Raw Error Report

- Rows: `48`
- Malformed/verbose rate: `0.167`
- Categories: `{"explanation_or_verbose_answer": 6, "nonnumeric_answer": 2, "parser_normalization_rescued": 5, "wrong_numeric_answer": 35}`
- Wrong examples:
  - `{"category": "explanation_or_verbose_answer", "gold_target": "18", "id": "hsb_mr_dev:low-hsb-0", "normalized_prediction": "56", "normalized_reference": "18", "raw_prediction": "16 * 3 + 4 * 2 = 48 + 8 = 56"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "3", "id": "hsb_mr_dev:low-hsb-1", "normalized_prediction": "10", "normalized_reference": "3", "raw_prediction": "10"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "70000", "id": "hsb_mr_dev:low-hsb-2", "normalized_prediction": "150", "normalized_reference": "70000", "raw_prediction": "150.000 US-dolarow"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "540", "id": "hsb_mr_dev:low-hsb-3", "normalized_prediction": "180", "normalized_reference": "540", "raw_prediction": "180"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "20", "id": "hsb_mr_dev:low-hsb-4", "normalized_prediction": "100", "normalized_reference": "20", "raw_prediction": "100"}`
