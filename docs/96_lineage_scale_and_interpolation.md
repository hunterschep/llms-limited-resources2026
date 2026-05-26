# Lineage Scale And Interpolation

Core experiment: find a point between Stage A and Stage B that keeps most Sorbian MT gain while recovering MR/edit behavior.

Adapter scale sweep:

- 0.20
- 0.30
- 0.40
- 0.50
- 0.60
- 0.70
- 0.80
- 0.90
- 1.00
- 1.10

Parent/StageB interpolation:

- alpha 0.20 through 1.00

Probe gates:

- exploratory MT `>=38.0`
- serious MT `>=41.0`
- MR above original Stage B `4.167`, preferred `>=8.333`
- SC/GC no-error behavior not worse than Stage B
- overall above Stage B on probe
- no malformed output spike

Full eval candidates:

- best adapter-scale candidate
- best StageA/StageB interpolation candidate
- reproduced Stage B
- original Stage B
- `edit_repair_tiny`
- prompt-only anchor
