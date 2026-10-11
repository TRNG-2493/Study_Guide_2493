# Data-quality findings (expected-findings template)

Copy this file to `docs/DATA_QUALITY_FINDINGS.md` in your qe-foundations repo and fill it in. `check_exercise.py --repo` (F8) requires:
all 20 check ids present (at least 18), and no `TODO` left. Replace every TODO with your own words. Plain ASCII text only.

## 1. Prediction round (do this BEFORE you run Part E, 5 minutes)

Open `sql/seed.sql` (or run `SELECT * FROM builds;` and the other three tables with `python lab_runner.py`) and read the data like a tester.
List up to 8 problems you can already SEE, and which check category you expect to catch each one.

| # | What I see (table, row, column) | Category I expect (reconciliation / missing rows / uniqueness / completeness / referential / validity / business rule) |
|---|---|---|
| 1 | TODO | TODO |
| 2 | TODO | TODO |
| 3 | TODO | TODO |

After Part E: how many of your predictions did the suite confirm? Which defects did you NOT see by eye? TODO

## 2. Findings per check (fill in after `python lab_runner.py --checks sql/part_e_checks.sql --show`)

Severity: High = wrong results or lost data reach users, Medium = reports are wrong in places, Low = cosmetic / hygiene.
Draft bug title: one line a developer could act on (what is wrong, where, how many).

| Check | Category | Violations | Offending ids | Severity | Suspected root cause | Draft bug title |
|---|---|---|---|---|---|---|
| E-01 | reconciliation | TODO | TODO | TODO | TODO | TODO |
| E-02 | reconciliation | TODO | TODO | TODO | TODO | TODO |
| E-03 | missing rows | TODO | TODO | TODO | TODO | TODO |
| E-04 | missing rows | TODO | TODO | TODO | TODO | TODO |
| E-05 | uniqueness | TODO | TODO | TODO | TODO | TODO |
| E-06 | uniqueness | TODO | TODO | TODO | TODO | TODO |
| E-07 | completeness | TODO | TODO | TODO | TODO | TODO |
| E-08 | completeness | TODO | TODO | TODO | TODO | TODO |
| E-09 | completeness + validity | TODO | TODO | TODO | TODO | TODO |
| E-10 | referential | TODO | TODO | TODO | TODO | TODO |
| E-11 | referential | TODO | TODO | TODO | TODO | TODO |
| E-12 | referential | TODO | TODO | TODO | TODO | TODO |
| E-13 | referential | TODO | TODO | TODO | TODO | TODO |
| E-14 | validity | TODO | TODO | TODO | TODO | TODO |
| E-15 | validity | TODO | TODO | TODO | TODO | TODO |
| E-16 | business rule | TODO | TODO | TODO | TODO | TODO |
| E-17 | business rule | TODO | TODO | TODO | TODO | TODO |
| E-18 | business rule | TODO | TODO | TODO | TODO | TODO |
| E-19 | cross-table consistency | TODO | TODO | TODO | TODO | TODO |
| E-20 | business rule | TODO | TODO | TODO | TODO | TODO |

## 3. Questions the data asked you (one or two sentences each)

1. **A1:** `PRAGMA foreign_key_check` listed 5 violations. Which of E-10 .. E-13 are they, and why did the database accept those rows in the first place? TODO
2. **B4 vs E-10:** B4 returned 3 runs, E-10 only 2. Which run is the difference and in which check does it belong? Why? TODO
3. **C2:** Why did the `NOT IN` query return zero rows? TODO
4. **B2 vs E-04:** B2 returned 3 cases, E-04 only 2. Which case is excluded and why is that correct? TODO
5. **C4a vs C4b:** why does one out-of-range duration change which runs look "slow"? TODO

## 4. Top 3 risks for the release (the message you would give the team lead)

1. TODO
2. TODO
3. TODO
