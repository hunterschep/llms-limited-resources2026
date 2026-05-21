# Prediction Dump Diagnostics

## GC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 2, "gold_correct": 3, "gold_error": 2, "pred_correct": 0, "pred_error": 5, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

## MR

- `rows`: `5`
- `accuracy`: `0.0`
- `wrong_examples` sample:
  - `{"gold": "18", "id": "hsb_mr_dev:low-hsb-0", "normalized_prediction": "5", "normalized_reference": "18", "prediction": "1. **Obliczono całkowitą ilość jajek:**\n   - 16 jajek dziennie.\n   - Czas trwania: 3 dni.\n   - Ilość jajek: $16 \\times 3 = 48$ jajek.\n\n2. **Obliczono ilość muffin:**\n   - 4 muffiny dziennie.\n   - Czas trwania: 3 dni.\n   - Ilość muffin: $4 \\times 3 = 12$ muffin.\n\n3. **Obliczono całkowitą ilość jedzenia:**\n   - Ilość jajek + Ilość muffin = $48 + 12 = 60$ jedzenia.\n\n4. **Obliczono cenę jedzenia w dolarach:**\n   - Cena za 1 jajko: $2$ USD.\n   - Cena za 1 muffin: $1$ USD.\n   - Ilość jedzenia w dolarach: $60 \\times 2 = 120$ USD.\n\n5. **Obliczono całkowitą wartość burskich wiksów:**\n   -"}`
  - `{"gold": "3", "id": "hsb_mr_dev:low-hsb-1", "normalized_prediction": "10", "normalized_reference": "3", "prediction": "10"}`
  - `{"gold": "70000", "id": "hsb_mr_dev:low-hsb-2", "normalized_prediction": "195000", "normalized_reference": "70000", "prediction": "1. Calculate the total cost of the house: 80,000 + 50,000 = 130,000 US dollars.\n2. Calculate the profit percentage: 150% of the total cost.\n3. Calculate the profit amount: 130,000 * 1.5 = 195,000 US dollars.\n\nThe final answer is 195,000 US dollars."}`
  - `{"gold": "540", "id": "hsb_mr_dev:low-hsb-3", "normalized_prediction": "180", "normalized_reference": "540", "prediction": "3 * 60 = 180"}`
  - `{"gold": "20", "id": "hsb_mr_dev:low-hsb-4", "normalized_prediction": "3", "normalized_reference": "20", "prediction": "1. Obliczamy całkowitą liczbę kokošów w końcowej grupie: $20 + 15 = 35$.\n2. W każdej jedyce jest 3 kółka. W sumie w 3 jedykach jest $3 \\times 3 = 9$ kółek.\n3. W każdym kółku jest 1 kółko. W sumie w 3 jedykach jest $3 \\times 1 = 3$ kółka.\n4. W każdym kółku jest 1 kółko. W sumie w 3 jedykach jest $3 \\times 1 = 3$ kółka.\n5. W każdym kółku jest 1 kółko. W sumie w 3 jedykach jest $3 \\times 1 = 3$ kółka.\n6. W każdym kółku jest 1 kółko. W sumie w 3 jedykach jest $3 \\times 1 = 3$ kółka.\n7. W każdym kółku jest 1 kółko. W sumie w 3 jedykach jest $3"}`

## MT

- `rows`: `5`

## QA

- `rows`: `5`
- `accuracy`: `0.4`
- `prediction_counts`: `{"1": 3, "2": 2}`
- `wrong_examples` sample:
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H01", "normalized_prediction": "2", "prediction": "2"}`
  - `{"gold": "2", "id": "hsb_qa_dev:A1.1.H1", "normalized_prediction": "1", "prediction": "1"}`
  - `{"gold": "1", "id": "hsb_qa_dev:A1.1.H9", "normalized_prediction": "2", "prediction": "2"}`

## SC

- `rows`: `5`
- `scores`: `{"correction_f1": 0.0, "detection_f1": 0.5714285714285715}`
- `confusion`: `{"correction_exact": 0, "detection_fn": 0, "detection_fp": 3, "detection_tn": 0, "detection_tp": 2, "gold_correct": 3, "gold_error": 2, "pred_correct": 0, "pred_error": 5, "total": 5, "wrong_word_exact": 0}`
- `predicted_label_counts`: `{"ERROR": 5}`
- `gold_label_counts`: `{"CORRECT": 3, "ERROR": 2}`

