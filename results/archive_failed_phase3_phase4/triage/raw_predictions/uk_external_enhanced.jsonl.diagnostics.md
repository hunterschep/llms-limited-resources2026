# Prediction Dump Diagnostics

## GC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 12, "detection_tn": 0, "detection_tp": 8, "gold_correct": 12, "gold_error": 8, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 2}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 12, "ERROR": 8}`

## MR

- `rows`: `20`
- `accuracy`: `0.3`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "8", "normalized_reference": "18", "prediction": "16 * 4 = 64 (яєць)\n64 / 16 = 4 (деньів)\n4 * 2 = 8 ($)\n\nВона заробляє 8 доларів на фермерському ринку щодня."}`
  - `{"gold": "3", "id": "ukr_mr_dev:low-ukr-1", "normalized_prediction": "2", "normalized_reference": "3", "prediction": "1. Нехай $x$ — кількість мотків синьої пряжі.\n2. Тоді кількість мотків білої пряжі дорівнює $\\frac{x}{2}$.\n3. За умовою, кількість мотків білої пряжі наполовину менша за кількість мотків синьої, тобто $\\frac{x}{2} = \\frac{x}{2} - \\text{нехильна частина}$? Ні, це означає, що кількість білої пряжі менша за кількість синьої на половину.\n   Формула: $x - \\frac{x}{2} = \\text{кількість білої}$.\n   Але за умовою сказано: \"наполовину менше\". Це означає, що кількість білої пряжі дорівнює половині кількості синьої.\n   Отже, $x - \\frac{x}{2} = \\text{кількість білої}$.\n   Перевіримо: якщо синього 2 мотки, то білого наполовину менше, то"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "0", "normalized_reference": "70000", "prediction": "1. Вартість будинку до ремонту: $80\\,000$.\n2. Вартість будинку після ремонту: $80\\,000 \\times (1 + 1.5) = 80\\,000 \\times 2.5 = 200\\,000$ $.\n3. Вартість будинку після перепродажу: $200\\,000 \\times 1.5 = 300\\,000$ $.\n4. Вартість будинку після ремонту: $200\\,000 - 80\\,000 = 120\\,000$ $.\n5. Вартість будинку після ремонту + ремонт: $120\\,000 + 50\\,000 = 170\\,000$ $.\n6. Вартість будинку після ремонту + ремонт + перепродажа: $170\\,000 + 300\\,000 = 470\\,000$ $."}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "40", "normalized_reference": "20", "prediction": "15 + 25 = 40"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "15", "normalized_reference": "64", "prediction": "16 склянок.\n\nПояснення:\n1.  **Перший раз:** Купити 1 склянку за 5 $.\n2.  **Другий раз:** Купити 1 склянку за 60 % від 5 $.\n    *   0.6 * 5 = 3 $.\n3.  **Третій раз:** Купити 1 склянку за 60 % від 3 $.\n    *   0.6 * 3 = 1.8 $.\n4.  **Четвертий раз:** Купити 1 склянку за 60 % від 1.8 $.\n    *   0.6 * 1.8 = 1.08 $.\n\nЗагальна сума: 5 + 3 + 1.8 + 1.08 = 10.88 $.\n\nАльтернативний спосіб:\nВсього склянок: 16.\nПерший раз: 1 склянка за 5 $.\nОстанні 15 склянок: 15 *"}`

## MT

- `rows`: `20`

## QA

- `rows`: `20`
- `accuracy`: `0.3`
- `prediction_counts`: `{"0": 12, "1": 1, "2": 4, "3": 2, "4": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000006", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000016", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `20`
- `scores`: `{"correction_f1": 0.5, "detection_f1": 0.7499999999999999}`
- `confusion`: `{"correction_exact": 4, "detection_fn": 0, "detection_fp": 8, "detection_tn": 0, "detection_tp": 12, "gold_correct": 8, "gold_error": 12, "pred_correct": 0, "pred_error": 20, "total": 20, "wrong_word_exact": 7}`
- `predicted_label_counts`: `{"ERROR": 20}`
- `gold_label_counts`: `{"CORRECT": 8, "ERROR": 12}`
