# Grading notes (instructor)

## How to use

Check the Definition of Done first (pass/fail items), then score the rubric in the README. Verify numbers by counting rows, not by trusting the summary.

## Quick checks

| Check | Pass when |
|---|---|
| Counts | At least 30 cases, at least 12 Positive, at least 18 Negative; unique IDs |
| Concrete data | Test data contains real values; no "valid email" placeholders |
| Expected results | Negative cases quote the exact message from the spec and the unchanged state |
| Traceability | R-01 to R-14 all present, each with at least one case, gap count 0; spot-check three rows against the case table |
| Execution | At least 10 cases have actual output pasted; Pass/Fail agrees with the spec (re-run two cases yourself) |
| Classification | Each Fail row has all three parts; failure is observable, defect is a product behaviour, error is a human mistake |
| Automation | 3 positive and 2 negative tests, named by case ID, exact-message asserts, state assert for negatives |
| Review | Three before/after fixes that are real (not renamed titles) |
| Reflection | 4-6 sentences, cites a case |

## Scoring guidance

* Part 2 (expected results, 15 points): 15 when all negatives name message and state; 10 when about half do; 5 when most are "error shown".
* Part 4 chain (15 points): 3 points per well-classified defect group up to 5 groups; deduct when failure and defect are merged into one sentence.
* Part 5 (12 points): 2 per test (correct pattern, exact assertions), 2 for running and recording the result.
* Do not penalise a trainee for finding fewer than six defects if the suite is strong; penalise a weak suite even if some defects were found by luck.
* Accept different but valid test data and titles. Duplicate cases cost points under Part 2 (up to 3).

## Typical weaknesses to give feedback on

1. Only 5-8 negative cases or all negatives on the password field.
2. "Error message appears" with no text.
3. Lockout covered only by a single case that mixes counting and unlocking.
4. Expected results copied from the program's actual output.
5. Defect described as "the code has a bug".
6. Mixed concerns: one case checking confirm password, terms and duplicate email together.

## Reference material

* `sample-test-suite-solution.md`: 36 cases with results on build 0.3.0.
* `traceability-solution.md`: rule mapping.
* `defect-chain-analysis-solution.md`: six defects SD-01 to SD-06.
* `sample-automated-tests-solution.py`: five tests; two fail on 0.3.0 on purpose (TC-014, TC-028).

## Feedback tone

Praise a specific strong case first, name one weakness and show how to fix it. Remind trainees that Thursday gives the formal tools for choosing test data.
