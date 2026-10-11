# Decision Table: Discount Rule (DSC-01..DSC-09)

Pair: ______________

## 1. Conditions and actions
| Symbol | Condition | Values |
|---|---|---|
| M | is a member | T / F |
| P | promo code is valid | T / F |
| L | order is large (DSC-07) | T / F |
| S | is a student | T / F |

Action: discount percent (one of 0, 5, 10, 15, 20).

## 2. Full table (2^n rules, n = number of conditions: ____ conditions, ____ rules)
| Rule | M | P | L | S | Expected discount % | Req ID |
|---|---|---|---|---|---|---|
| R1 | T | T | T | T | | |
| R2 | T | T | T | F | | |
| ... continue until all 2^n rows are listed | | | | | | |

## 3. Collapsed table (merge rules with the same action using "-" for "does not matter")
| Rule | M | P | L | S | Discount % | Merged from full rules | Req ID |
|---|---|---|---|---|---|---|---|
| C1 | | | | | | | |

## 4. Test plan
| Test ID | From rule | Concrete inputs (member, total, promo, student) | Expected |
|---|---|---|---|
| DT-DSC-01 | | | |

Decision: our tests implement the  [ ] full table   [ ] collapsed table  because: ____________________
Question to answer: if we implement the collapsed table, which "-" values did we have to choose, and could a defect hide behind them?
