# Refinement Log (exemplar, built from the backup replies in evidence/)

## TD-1 shipping test ideas: the ladder

Acceptance criteria written before v1: the 12 checks in `tools/score_reply.py`.

| Version | The ONE change | Lint | Score (run 1) | Criteria that flipped | Input problem or model limitation? |
|---|---|---|---|---|---|
| v1 | first version (vague) | 1/9 | 0/12 | none; 4 invented rules | input: no context |
| v2 | requirement in `<requirement>` tags | 3/9 | 5/12 | no invented rules, Canada, express, exact values, unsupported country | input |
| v3 | techniques, 8-10 ideas, cent precision | 4/9 | 10/12 | boundaries 74.99/75.00/75.01, on-feature, negative subtotal | input |
| v4 | audience, constraints, table format | 7/9 | 11/12 | automatable table | input |
| v5 | done-criteria, list assumptions first | 9/9 | 12/12 | assumptions listed | input |

Scorer limitations found by human review (not prompt problems):
- v2 "negative subtotal" failed only because the reply said "a negative subtotal" without a number. The idea was there; the scorer needs a number.
- v3 volunteered an assumption ("Note: the requirement does not say ...") that the `assum|question` pattern missed.

Final version (v5), three runs:

| Run | Score | Failed criteria | What differed from the other runs |
|---|---|---|---|
| 1 | 12/12 | none | 10 rows, 3 assumptions |
| 2 | 12/12 | none | adds 0.00 subtotal and express at both boundaries; MX as unsupported country |
| 3 | 12/12 | none | 9 rows; express on CA; DE as unsupported country |

Criteria that could still fail, and the check outside the model: expected-value arithmetic. Recompute each row by calling `shipping_cost` (all rows of the three runs matched).

## TD-2 format-locked cases

| Reply | Syntax | Structure | Re-ask needed? | Re-ask result | pytest result |
|---|---|---|---|---|---|
| run1 | OK (fenced, tolerated) | OK | no | n/a | 9 passed |
| drift-test (hand-made) | OK | 8 problems | yes (message printed) | n/a | collection error, 0 tests run |
| run2 | OK | OK | no | n/a | 3 failed, 3 passed |

| Case id | Claude expected | Code returns | Who is right? | Requirement sentence |
|---|---|---|---|---|
| run2 SC-03 | 0.0 (express on free stays free) | 10.0 | the code | 4 |
| run2 SC-04 | 0.0 for "us" | ValueError | invented rule; question for the product owner | none (silent) |
| run2 SC-05 | 0.0 for a 0.00 subtotal | 5.99 | the code | 2 |

## TD-3 few-shot Gherkin

| Version | Change | check_gherkin result | Leakage | What I corrected by reading |
|---|---|---|---|---|
| v1 run1 | first version | all OK | none | no hyphen-first username tested; noted for v2 |
| leak (backup) | search example with "ignores letter case" | 8 content FAIL | mila.ortiz, My account, ignores letter case | example smuggled a rule into registration |

## DB-1 structured debugging
- My reading before asking: express works on paid orders, fails only on free US orders, so the free-shipping rule must be overwriting the surcharge.
- Claude's ranked hypotheses: overwrite order (1), threshold comparison (2), rounding (3).
- Confirmation: `python -c "from shopfront.shipping_buggy import shipping_cost as s; print(s(80,'US',True), s(74.99,'US',True))"` printed `0.0 15.99`.
- Fix: move `if express: charge += 10.00` below the free-shipping rule. Suite: 5 passed.
- Weakening check: `git diff --stat` lists only `shopfront/shipping_buggy.py`. The "make it pass" reply changed the expected value to 0.0 and offered `xfail`: rejected, because requirement sentence 4 did not change.

## DB-2 CI triage

| Test | Claude category (run1) | My category | Evidence line correct? | Agree? |
|---|---|---|---|---|
| test_promo_code_applies_discount | test_bug | test_bug | yes | yes: "element is not enabled", click before fill |
| test_search_shows_no_results_message | needs_clarification | needs_clarification | yes | yes: no requirement for the message text |
| test_list_items_paginates | product_bug | product_bug (likely) | yes | yes, pending the API contract |

run2 (backup) failed the contract on 3 points; its "increase the timeout" hypothesis contradicts the log and only a human catches that.

## What I would tell a teammate
- Write what a good answer contains before you ask, and score every reply, not just the first.
- Context fixed most problems; checks outside the model caught the rest.
- A green check is a first filter. Read the reply against the requirement before using it.
