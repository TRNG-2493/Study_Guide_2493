# US-420 Review Report (exemplar, built from the backup replies in evidence/)

Reviewer: a.trainee
Approver (a different person): b.peer
Date: 2026-10-21
AI tool: Claude

## 1. My manual review (written BEFORE prompting)
| # | AC | Problem | Category |
|---|---|---|---|
| 1 | AC1 | Upper/lower case in the code not stated | AMBIGUOUS |
| 2 | AC1 | Spaces or dashes typed inside the code not stated | INCOMPLETE |
| 3 | AC2 | "Order total" before or after shipping and tax? | AMBIGUOUS |
| 4 | AC2 | Balance larger than the total: what is paid, what happens to the rest? | INCOMPLETE |
| 5 | AC3/AC4 | Expired or blocked cards not covered | INCOMPLETE |
| 6 | AC5 | "Quickly" has no number | UNMEASURABLE |

## 2. Claude's requirements findings
| # | AC | Automatic check | My verdict | Why |
|---|---|---|---|---|
| 1 | AC1 | OK | keep | matches my item 1 |
| 2 | AC1 | OK | keep | matches my item 2 |
| 3 | AC2 | OK | keep | matches my item 4 |
| 4 | AC3 | OK | keep | expiry; matches item 5 |
| 5 | AC5 | OK | keep | matches item 6 |
| 6 | AC5 | FLAG: quote not in story | discard | "within 3 seconds" is invented, presented as a quote |
| 7 | AC6 | FLAG: AC6 does not exist | discard | US-420 has five ACs; "one gift card per order" is invented |

What Claude found that I missed: nothing new this run (finding 3 phrased the unused-balance question better than mine).
What I found that Claude missed: what "order total" includes (shipping, tax). Note: `reference_coverage` reports it as "found" because the keyword "order total" appears in finding 3. Keyword matching is crude; I checked by reading.

## 3. Question log and PO answers
5 questions from Claude plus 1 of mine (Q-6, shipping and tax). Answered: 5 (case, shipping/tax, larger balance, expiry out of scope, AC5 out of scope). Open: 1 (spaces/dashes). Answered by the instructor as PO.

## 4. My oracle
`python lab.py oracle`: 10 rows; spaces/dashes row "not decided: question for the PO".

## 5. Test case review
Draft: AC1 to AC5 all covered; boundary 15 missing; pointers on TC-02, TC-06, TC-07, TC-08, TC-09.
Metrics: 9 AI items, 4 accepted (44%), 2 edited, 3 rejected; usable as-is 44%, usable at all 67%; 3 added by me.

| | `--impl giftcard` | `--impl giftcard_buggy` |
|---|---|---|
| Claude draft (`--unreviewed`) | 3 failed, 5 passed, 1 skipped | 3 failed, 5 passed, 1 skipped |
| Approved suite | 9 passed | 1 failed (TC-H1) |

The draft fails on the correct app because three of its expectations are wrong (TC-02, TC-06, TC-07): its red results are noise, not defects. On the buggy app it fails in exactly the same way, so it says nothing about the real bug. The approved suite is green on the correct app and red only on the buggy one, through TC-H1, the 15-character boundary I added because the draft had only 17. AC5 is NOT COVERED in the approved suite on purpose: out of scope this sprint (PO).

## 6. Test data review
| Row | Problem reported | Who is right | Decision |
|---|---|---|---|
| TD-02 | pays 100.00 vs 80.00 | my oracle (a card cannot pay more than the total) | fix to 80.00 |
| TD-03 | not_recognised vs applied | my oracle (PO: case-insensitive) | fix label; move to VALID is correct |
| TD-06 | not QATEST prefix | the rule | remove: a realistic retailer card number could be live value (C8) |
| TD-09 | balance is a float | the rule | fix to "79.99" |
| TD-10 | undecided by oracle | PO question | remove row; spaces/dashes stay OPEN |
| TD-11 | changes 2 fields | the rule | split into two rows |

Found by reading only: TD-12 (9999.99) adds nothing over TD-01 for redemption (same partition); dropped as low value (C4). Claude asked no questions although it guessed dashes.

## 7. Responsible use
- Classification: the raw note mixes internal data with a customer's personal data and a production gift card code. As it stands it is not "internal". I deleted the customer line and the production code line by hand, then ran pre-flight as internal.
- GIFT_CARD rule: 15-17 upper-case letters and digits with at least one of each, excluding the QATEST prefix; it caught the production code and kept my test code readable.
- Redactor still missed: Priya's name, the staging URL, order 88213-A, Daniel Okafor and 7 Birch Road.
- Rotate: the staging password and bearer token (tell the staging owner); report the production gift card code to support so the card can be checked or reissued.
- Defect draft corrections: severity Critical to High (money, but not a crash or data loss; my team scale); removed "also affects 14-character codes" after checking: `python -c "from shopfront.giftcard_buggy import apply_gift_card as a; print(a(80,'QATEST26ABCD12',50))"` shows 14 characters are rejected.
- Disclosure: `# AI-assisted: Claude drafted test cases; reviewed by a.trainee 2026-10-21`

## 8. Reflection
- 44% usable as-is, 67% at all: a tidy draft is a starting point, not a suite.
- The bug was caught by the case the human added, not by any case Claude wrote.
- Two of Claude's "quotes" were not in the story: grounding checks are cheap and worth running every time.
- The data draft's labels and my oracle disagreed on 3 rows; each time the PO answer or the AC decided, never Claude.
- Redaction is a safety net; the customer line had to be removed by a person.
