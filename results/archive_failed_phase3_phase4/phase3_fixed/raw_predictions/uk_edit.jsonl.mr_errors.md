# MR Raw Error Report

- Rows: `10`
- Malformed/verbose rate: `0.500`
- Categories: `{"explanation_or_verbose_answer": 5, "parser_normalization_rescued": 1, "wrong_numeric_answer": 4}`
- Wrong examples:
  - `{"category": "wrong_numeric_answer", "gold_target": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "32", "normalized_reference": "18", "raw_prediction": "16 * 2 = 32"}`
  - `{"category": "explanation_or_verbose_answer", "gold_target": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "187.5%", "normalized_reference": "70000", "raw_prediction": "150% від 50 000 $ = 75 000 $.\nВсього витрачено на будинок: 80 000 + 75 000 = 155 000 $.\nВартість будинку після ремонту: 80 000 + 150 000 = 230 000 $.\nВартість будинку до ремонту: 80 000 $.\nВідсоток прибутку: (230 000 - 80 000) / 80 000 = 150 000 / 80 000 = 1.875 = 187.5%."}`
  - `{"category": "wrong_numeric_answer", "gold_target": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "raw_prediction": "3 * 60 = 180"}`
  - `{"category": "wrong_numeric_answer", "gold_target": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "60", "normalized_reference": "20", "raw_prediction": "20 * 3 = 60"}`
  - `{"category": "explanation_or_verbose_answer", "gold_target": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "8", "normalized_reference": "64", "raw_prediction": "16 склянок — це 16 одиниць.\nПерша склянка коштує 5 $.\nОстанні 15 склянок коштують 60 % від ціни першої склянки.\nСума ціни першої склянки: $5$.\nСума ціни 15 склянок: $5 \\times 0.6 = 3$.\nЗагальна сума: $5 + 3 = 8$."}`
