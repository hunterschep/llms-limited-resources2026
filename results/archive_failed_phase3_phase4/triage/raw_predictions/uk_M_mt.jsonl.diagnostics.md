# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.2222222222222222, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 1, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 4}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.2`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "32", "normalized_reference": "18", "prediction": "16 * 2 = 32"}`
  - `{"gold": "3", "id": "ukr_mr_dev:low-ukr-1", "normalized_prediction": "2", "normalized_reference": "3", "prediction": "Let $x$ be the number of spools of blue thread.\nThen the number of spools of white thread is $\\frac{x}{2}$.\nThe total number of spools is $x + \\frac{x}{2} = \\frac{3x}{2}$.\nWe are given that the total number of spools is 10.\nSo, $\\frac{3x}{2} = 10$.\n$3x = 20$.\n$x = \\frac{20}{3}$.\nThe number of blue spools is $\\frac{20}{3}$.\nThe number of white spools is $\\frac{10}{3}$.\nTotal number of spools is $\\frac{20}{3} + \\frac{10}{3} = \\frac{30}{3} = 10$.\n\nAlternatively, let $y$ be the number of white spools.\nThen the number of blue spools is $2y$.\nTotal spools: $2y + y = 3y$.\n$3y = 10$.\n$y = \\frac{10}{3}$.\nBlue spools: $2"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "0", "normalized_reference": "70000", "prediction": "1. Вартість будинку до ремонту: 80 000 $.\n2. Вартість будинку після ремонту: $80\\,000 \\times (1 + 1.5) = 80\\,000 \\times 2.5 = 200\\,000 $.\n3. Вартість ремонту: $200\\,000 - 80\\,000 = 120\\,000 $.\n4. Вартість будинку після продажу: $200\\,000 $.\n5. Вартість покупки: $80\\,000 $.\n6. Вартість продажу: $200\\,000 $.\n7. Прибуток: $200\\,000 - 80\\,000 = 120\\,000 $.\n8. Вартість ремонту: $50\\,000 $.\n9. Вартість вигоди (прибуток від ремонту): $120\\,000 - 50\\,000 ="}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 * 60 = 180"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "50", "normalized_reference": "64", "prediction": "1. **Визначимо ціну однієї склянки:**\n   - Вартість першої склянки = $5.\n\n2. **Визначимо ціну другої склянки:**\n   - Вартість другої склянки = 60% від ціни першої склянки.\n   - $5 \\times 0.60 = 3$ $.\n\n3. **Обчислимо вартість 16 склянок:**\n   - Перша склянка коштує $5.\n   - Решта 15 склянок (16 - 1) коштують $3.\n   - Загальна сума = $5 + (15 \\times 3)$.\n   - $15 \\times 3 = 45$.\n   - $5 + 45 = 50$.\n\nКайлар має за склянки заплатити 50 $."}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.3`
- `prediction_counts`: `{"0": 10, "1": 5, "2": 1, "3": 3, "4": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000001", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.5882352941176471, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 5, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 9}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`
