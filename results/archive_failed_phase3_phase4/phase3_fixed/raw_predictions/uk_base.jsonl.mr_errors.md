# MR Raw Error Report

- Rows: `10`
- Malformed/verbose rate: `0.400`
- Categories: `{"exact_normalized_match": 1, "explanation_or_verbose_answer": 4, "parser_normalization_rescued": 2, "wrong_numeric_answer": 3}`
- Wrong examples:
  - `{"category": "wrong_numeric_answer", "gold_target": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "32", "normalized_reference": "18", "raw_prediction": "16 * 2 = 32"}`
  - `{"category": "explanation_or_verbose_answer", "gold_target": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "0", "normalized_reference": "70000", "raw_prediction": "150% = 1.5\nВартість будинку після ремонту = 80 000 + (80 000 * 1.5) = 80 000 + 120 000 = 200 000 $\nВартість будинку до ремонту = 80 000 $\nВідсоток втрати = (80 000 / 200 000) * 100% = 40%\nВідсоток втрати = (80 000 / 80 000) * 100% = 100%\nВідсоток втрати = (80 000 / 200 000) * 100% = 40%\nВідсоток втрати = (80 000 / 80 000) * 100% = 100%\nВідсоток втрати = (80 000 / 200 0"}`
  - `{"category": "explanation_or_verbose_answer", "gold_target": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "89", "normalized_reference": "64", "raw_prediction": "16 * 5 = 80\n16 - 1 = 15\n15 * 0.6 = 9\n80 + 9 = 89"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "260", "id": "ukr_mr_dev:low-ukr-6", "normalized_prediction": "240", "normalized_reference": "260", "raw_prediction": "240"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "160", "id": "ukr_mr_dev:low-ukr-7", "normalized_prediction": "120", "normalized_reference": "160", "raw_prediction": "120 хвилин"}`
