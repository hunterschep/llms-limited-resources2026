# Prediction Dump Diagnostics

## GC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.0}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 7, "detection_fp": 0, "detection_tn": 3, "detection_tp": 0, "gold_correct": 3, "gold_error": 7, "pred_correct": 10, "pred_error": 0, "total": 10, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"CORRECT": 10}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 7}`

## MR

- `rows`: `10`
- `accuracy`: `0.1`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "ukr_mr_dev:low-ukr-0", "normalized_prediction": "32", "normalized_reference": "18", "prediction": "16 * 4 = 64 (яєць)\n64 / 4 = 16 (яєць)\n16 * 2 = 32 ($)\n\nВона заробляє 32 долари на фермерському ринку щодня.\n\n32"}`
  - `{"gold": "70000", "id": "ukr_mr_dev:low-ukr-2", "normalized_prediction": "0", "normalized_reference": "70000", "prediction": "1. Вартість будинку до ремонту: 80 000 $.\n2. Вартість будинку після ремонту: 80 000 $ + (80 000 $ × 1,5) = 80 000 $ + 120 000 $ = 200 000 $.\n3. Вартість ремонту: 50 000 $.\n4. Вартість будинку після ремонту: 200 000 $.\n5. Вартість будинку до продажу: 80 000 $ + 50 000 $ = 130 000 $.\n6. Вартість будинку після продажу: 200 000 $.\n7. Вартість продажу: 200 000 $.\n8. Вартість покупки: 80 000 $.\n9. Вартість ремонту: 50 000 $.\n10. Вартість будинку до продажу: 80 000 $ + 50 0"}`
  - `{"gold": "540", "id": "ukr_mr_dev:low-ukr-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 спринти × 60 метрів = 180 метрів.\n\n180"}`
  - `{"gold": "20", "id": "ukr_mr_dev:low-ukr-4", "normalized_prediction": "5", "normalized_reference": "20", "prediction": "1. Розрахуємо загальну кількість чашок корму, яку Венді дає своїй зграї за день.\n   - Вранці: 15 чашок.\n   - Вдень: 25 чашок.\n   - Загальна кількість: $15 + 25 = 40$ чашок.\n\n2. Розрахуємо кількість чашок корму, які дає кожен прийом їжі.\n   - За умовою: кожен прийом їжі дає 3 чашки.\n\n3. Знайдемо кількість прийомів їжі за день.\n   - Загальна кількість чашок: 40.\n   - Кількість чашок на прийом: 3.\n   - Кількість прийомів: $40 \\div 3 = 13$ з половиною прийомів.\n\n4. Знайдемо кількість чашок корму, які дає кожен прийом їжі.\n   - За умовою: кожен прийом їжі дає 3 чашки.\n\n5. Зна"}`
  - `{"gold": "64", "id": "ukr_mr_dev:low-ukr-5", "normalized_prediction": "50", "normalized_reference": "64", "prediction": "1. Визначимо ціну однієї склянки.\n   - Перша склянка коштує 5 $.\n   - Друга склянка коштує 60 % від ціни першої.\n   - Ціна другої склянки = $5 \\times 0.6 = 3 $.\n\n2. Обчислимо загальну кількість склянок, які Кайлар купує.\n   - Він хоче купити 16 склянок.\n\n3. Обчислимо загальну суму.\n   - Сума = (ціна першої склянки) + (ціна другої склянки) + (ціна решти склянок).\n   - Сума = $5 + 3 + (16 - 2) \\times 3$.\n   - Сума = $8 + 14 \\times 3$.\n   - Сума = $8 + 42 = 50 $.\n\nВідповідь: 50 $."}`

## MT

- `rows`: `10`

## QA

- `rows`: `10`
- `accuracy`: `0.3`
- `prediction_counts`: `{"0": 4, "1": 1, "2": 4, "3": 1}`
- `wrong_examples` sample:
  - `{"gold": "2", "id": "ukr_qa_dev:000002", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000004", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "3", "id": "ukr_qa_dev:000015", "normalized_prediction": "0", "prediction": "0"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000020", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "2", "id": "ukr_qa_dev:000026", "normalized_prediction": "0", "prediction": "0"}`

## SC

- `rows`: `10`
- `scores`: `{"correction_f1": 0.4, "detection_f1": 0.4}`
- `confusion`: `{"correction_exact": 1, "detection_fn": 3, "detection_fp": 0, "detection_tn": 6, "detection_tp": 1, "gold_correct": 6, "gold_error": 4, "pred_correct": 9, "pred_error": 1, "total": 10, "wrong_word_exact": 1}`
- `predicted_label_counts`: `{"CORRECT": 9, "ERROR": 1}`
- `gold_label_counts`: `{"CORRECT": 6, "ERROR": 4}`
