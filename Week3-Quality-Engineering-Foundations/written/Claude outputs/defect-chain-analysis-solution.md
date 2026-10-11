# Defect chain analysis (instructor solution)

Six defects are planted in build 0.3.0. Case IDs refer to `sample-test-suite-solution.md`. Trainees describe defects as behaviours; the "where" column is for the instructor only.

| ID | Rule | Trigger case(s) | Manual trigger (run_cases.py) | Failure (observed) | Defect (in the product) | Plausible error (human mistake) |
|---|---|---|---|---|---|---|
| SD-01 | R-03 | TC-023 (negative), TC-008 (positive) | `register --email a@b.com --username '  ab ' --password 'Abcdef1!' --confirm 'Abcdef1!' --terms yes` and `--username 'aaaaaaaaaaaaaaaaaaa  '` | Expected the username message; the 2-letter name is accepted and stored as "ab". The 19-letter name with 2 spaces is rejected though valid. | The 3-20 length check runs on the text before spaces are removed (check order: validate, then trim). | Developer misread "trim first, then validate" and applied the steps in the wrong order. |
| SD-02 | R-06 | TC-028 | `register --email a@b.com --username bob --password 'Abcdef1!' --confirm 'abcdef1!' --terms yes` | Expected "Passwords do not match."; account created. | Confirm password is compared case-insensitively. | Developer wanted to be "user friendly" or copied the email comparison, forgetting passwords are case-sensitive. |
| SD-03 | R-11 | TC-014 (positive), TC-035 (negative) | `register`, then four `login --id a@b.com --password wrong` | The 4th wrong attempt shows "Account locked." (expected the generic message; lock on the 5th), and the correct password is then rejected. | The lockout threshold is one lower than N (4 instead of 5): an off-by-one in the comparison. | Developer confused "after N attempts" with "before the Nth", an off-by-one mistake in counting. |
| SD-04 | R-05 | TC-026 | `register ... --password 'Abcdefg1' --confirm 'Abcdefg1' ...` | Expected the password-rule message; account created. | The special-character requirement is not enforced (only upper, lower, digit are checked). | Requirement changed or was partly read ("three of four types"); the fourth check was forgotten. |
| SD-05 | R-07 | TC-029 | `register ... --terms no` | Expected "You must accept the Terms and Conditions."; account created. | The terms checkbox value is never checked on submit. | Developer assumed the form layer already blocked unticked boxes, so the server rule was never written (an assumption error). |
| SD-06 | R-02 | TC-031 | `register` alice@example.com, then `register --email ALICE@Example.com --username bob_2 ...` | Expected "This email is already registered."; second account created (2 accounts). | The uniqueness check compares the email exactly as typed, not case-insensitively. | Developer forgot that email addresses are matched without regard to case (requirement oversight). |

## Failures by defect (on the 36 solution cases)

| Failing case | Defect |
|---|---|
| TC-008 | SD-01 |
| TC-014 | SD-03 |
| TC-023 | SD-01 |
| TC-026 | SD-04 |
| TC-028 | SD-02 |
| TC-029 | SD-05 |
| TC-031 | SD-06 |
| TC-035 | SD-03 |

Eight failures, six defects: one defect can cause many failures (SD-01, SD-03). Cases that pass but sit close to the defects (TC-007, TC-027, TC-030, TC-036) are good contrast data for trainees: the neighbouring behaviour is correct, so the defect is narrow.

## Coaching notes

* A trainee who only tests the happy paths finds none of the six; this is the point of the exercise.
* If a trainee reports "lockout happens after 4" as the defect, confirm and ask for the error: counting.
* Distinguish a wrong expectation from a defect: for example "username with spaces inside" is not covered by the spec; ask the trainee to log it as a question.
