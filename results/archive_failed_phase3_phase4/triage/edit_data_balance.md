# Edit Data Balance Report

| Track | Task | Rows | Error | Clean | Clean Ratio | Always-Error Detection F1 | Always-CORRECT Detection F1 | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| uk | SC | 9009 | 4506 | 4503 | 0.500 | 0.667 | 0.000 | pass |
| uk | GC | 7062 | 3531 | 3531 | 0.500 | 0.667 | 0.000 | pass |
| sorbian | SC | 5757 | 2998 | 2759 | 0.479 | 0.685 | 0.000 | pass |
| sorbian | GC | 1875 | 966 | 909 | 0.485 | 0.680 | 0.000 | pass |

Balanced edit data should keep clean/error ratio close to 0.5 so models cannot win detection by always predicting an error.
