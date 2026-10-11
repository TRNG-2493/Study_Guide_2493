# Feature Specification: Account Membership and Promo Codes

Project 1 - QE Foundations. Module under test: `membership.py` (starter_code). Design your tests from THIS document.
Every requirement has an ID. Your test IDs and design documents must cite these IDs.

## 1. Membership signup (function `signup(age, student)`)

| ID | Requirement |
|---|---|
| MEM-01 | Age must be from 16 to 65 inclusive. Any other whole number is rejected with `AGE_INVALID`. |
| MEM-02 | Age must be of type `int` (not `bool`). Any other type, including decimals such as 20.0 or 20.5, text and `None`, is rejected with `AGE_INVALID`. |
| MEM-03 | The student flag must be exactly `True` or `False`. Anything else is rejected with `STUDENT_INVALID`. |
| MEM-04 | When every field is valid the result is ok with code `MEMBER_CREATED`. When several fields are invalid, the first failing check is reported in this order: age, then student flag. |

## 2. Promo codes (function `validate_promo(code)`)

| ID | Requirement |
|---|---|
| PRM-01 | A code must be 6 to 10 characters long inclusive (after PRM-03 trimming). Otherwise `PROMO_LENGTH`. |
| PRM-02 | A code may contain only the letters A-Z and the digits 0-9. Otherwise `PROMO_CHARS`. |
| PRM-03 | Spaces at the start or end of a code are ignored, and letters are case-insensitive (`save10` equals `SAVE10`). |
| PRM-04 | A well-formed code must be in the catalog: `SAVE10`, `WELCOME10`, `MEGASALE10`. Otherwise `PROMO_UNKNOWN`. A catalog code gives ok with `PROMO_OK`. |
| PRM-05 | A code that is not text (for example `None` or a number) is rejected with `PROMO_TYPE`. |

Checks run in this order: type (PRM-05), trimming and case (PRM-03), length (PRM-01), characters (PRM-02), catalog (PRM-04).

## 3. Discount decision rule (function `discount_percent(is_member, order_total, promo_code, is_student)`)

Conditions: **M** = is a member, **P** = the promo code is valid (PRM-04 gives `PROMO_OK`), **L** = order is large, **S** = is a student.

| ID | Requirement |
|---|---|
| DSC-01 | A valid promo and a member: 20 percent. |
| DSC-02 | A valid promo and not a member: 10 percent. |
| DSC-03 | No valid promo, a member, large order: 15 percent. |
| DSC-04 | No valid promo, a member, not a large order: 5 percent. |
| DSC-05 | No valid promo, not a member, a student: 5 percent. |
| DSC-06 | No valid promo, not a member, not a student: 0 percent. |
| DSC-07 | An order is large when the total is 100 or more. |
| DSC-08 | An invalid or missing promo code is treated as "no valid promo". It never raises an error. |
| DSC-09 | A valid promo always takes priority over the student rule. |

## 4. Account lifecycle (class `Account`)

States: Pending, Active, Suspended, Closed. Events: `verify()`, `suspend(reason)`, `reactivate()`, `close()`.

| ID | Requirement |
|---|---|
| ACC-01 | A new account starts in Pending. |
| ACC-02 | `verify` moves Pending to Active (code `VERIFIED`). It is not allowed in any other state. |
| ACC-03 | `suspend` moves Active to Suspended (code `SUSPENDED`). It is not allowed in any other state. |
| ACC-04 | Guard: `suspend` needs a reason that is text and not blank. Otherwise `REASON_REQUIRED` and the state does not change. |
| ACC-05 | `reactivate` moves Suspended to Active (code `REACTIVATED`). It is not allowed in any other state. |
| ACC-06 | Closed is final: every event on a Closed account is refused. |
| ACC-07 | `close` moves Pending, Active or Suspended to Closed (code `CLOSED`). Guard: the account balance due must be 0, otherwise `BALANCE_OUTSTANDING`. The state is checked before the guard. |
| ACC-08 | A refused event returns ok False (code `INVALID_TRANSITION` unless another code is named), and the state does not change. |
