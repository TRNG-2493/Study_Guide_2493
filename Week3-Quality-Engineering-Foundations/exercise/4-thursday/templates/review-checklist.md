# Cross-Review Checklist

Reviewing pair: ________  Reviewed pair: ________  Repo/branch: ________  Time-box: 25 min

Mark Yes / Partly / No and add one specific note per "Partly" or "No". Quote a file and line or test ID.

| # | Check | Yes / Partly / No | Note (file, test ID) |
|---|---|---|---|
| 1 | Technique selection table exists and each choice has a reason. | | |
| 2 | BVA: every range (age, promo length) has all boundary values for the stated convention (2-value or 3-value). | | |
| 3 | EP: partitions listed for each field, including invalid types and below/above range. | | |
| 4 | Decision table: n conditions listed and 2^n rules present before collapsing. | | |
| 5 | Collapsed table is correct (merged rules really have the same action). | | |
| 6 | State diagram matches the spec (all 4 states, 4 events, guards shown). | | |
| 7 | State coverage: all valid transitions, and at least 3 invalid transitions, and both guards. | | |
| 8 | Requirement IDs: every MEM, PRM, DSC, ACC ID is cited by at least one test. | | |
| 9 | Test names and IDs are readable and follow the convention (TECH-AREA-NN-meaning). | | |
| 10 | Expected values come from the spec, not copied from what the code returned. | | |
| 11 | No duplicate tests (same inputs and same expectation twice). | | |
| 12 | Tests are independent and run green or red for a clear reason. | | |
| 13 | DEFECTS_FOUND.md links each defect to a failing test and a requirement. | | |
| 14 | Commit history shows both partners driving and clear messages. | | |

Overall: two strengths, three improvements, one question for the authors (put them in REVIEW_COMMENTS.md).
