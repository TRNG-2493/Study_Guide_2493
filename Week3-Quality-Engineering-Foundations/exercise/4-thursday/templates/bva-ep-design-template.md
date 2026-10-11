# BVA and EP Design

Pair: ______________  Convention used:  [ ] 2-value BVA   [ ] 3-value BVA   (state it and keep to it)

## 1. Equivalence partitions (one table per field)

| Field | Req ID | Partition ID | Description | Valid / Invalid | Representative value | Expected result |
|---|---|---|---|---|---|---|
| Age | MEM-01 | EP-AGE-01 | | | | |
| Age (type) | MEM-02 | | | | | |
| Student flag | MEM-03 | | | | | |
| Promo length | PRM-01 | | | | | |
| Promo characters / type / catalog | PRM-02, PRM-04, PRM-05 | | | | | |

## 2. Boundary values (one table per ordered range)

| Field | Req ID | Boundary | Value | Test ID | Expected result |
|---|---|---|---|---|---|
| Age | MEM-01 | below min | | BVA-AGE-01 | |
| | | min | | BVA-AGE-02 | |
| | | min + 1 (3-value only) | | | |
| | | max - 1 (3-value only) | | | |
| | | max | | | |
| | | above max | | | |
| Promo length | PRM-01 | (same rows) | | BVA-PRM-01 | |

## 3. Notes
- Other fields stay at a NOMINAL valid value while one field is tested.
- Assumptions or spec questions we raised:
