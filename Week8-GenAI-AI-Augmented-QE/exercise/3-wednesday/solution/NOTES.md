# Wednesday solution notes (instructors only)

## Exercise mode and scope
Mode C (hybrid): review and analysis work driven through a small code lab. `starter_code/` is the scaffold, `solution/` the completed exemplar. Individual, with a classmate as second approver at the sign-off gate (money at checkout). Time box 2-3 hours: setup 10, stages 35 / 15 / 20 / 40 / 25 / 20 / 10 minutes. Solvable from Monday to Wednesday material only. The `qa_flow/` helpers are the demo's `reqs_review.py`, `suite_checks.py`, `review_log.py`, `data_checks.py` and `responsible.py`, adapted to a new story (US-420 gift cards) so trainees reuse the commands they saw this morning on a problem they have not seen solved. Agent instructions, templates and JSON Schema remain Thursday.

## Intentional deviations from the CMA log (do not flag in QA)
- **No Project 2 milestone.** The CMA log says "Generate and review AI test cases/data for Project 2, documenting corrections" and the demo bridge points at Project 2 stories. By instructor decision, Project 2 is ignored this week: trainees work on the synthetic ShopFront story US-420, the same system as Monday and Tuesday. Every element of the demo bridge is kept: one story with 3+ ACs, own expected results first, a question log with PO answers, test cases with a traceability matrix, checklist review, correction log with fixed categories and evidence, usable as-is / usable at all, a constrained data set checked by an independent oracle, disclosure in file headers, meaningful commits.
- **Claude as the AI tool.** All prompts are printed by `lab.py` and pasted into a fresh Claude chat. Every Claude output passes a code check and a human decision.
- **Product owner.** The instructor plays the PO (as in demo card 1.4). `materials/po-answers.md` is a fallback; trainees must commit their question log before opening it.

## Verified results (Python 3.10, pytest 9.1)
| Command | Starter | Solution |
|---|---|---|
| `python -m pytest -q` | 5 failed (oracle NotImplementedError), 1 skipped | 14 passed (5 oracle + 9 approved rows) |
| `python lab.py lint` | 5 lines; AC5 'quickly', 'should' | same |
| `python lab.py check-findings evidence/findings.run1.txt --log ...` | runs; asks for REFERENCE_ISSUES | 5 OK, 2 FLAG (invented quote "within 3 seconds"; AC6 does not exist) |
| `python lab.py oracle` | exits: write your oracle | 10 rows, dashes row "not decided" |
| `python lab.py check-suite evidence/suite_draft.run1.txt` | exits: needs oracle | pointers on TC-02, TC-06, TC-07, TC-08, TC-09; code length 15 NO |
| `python lab.py signoff evidence/suite_draft.run1.txt review/review_decisions.json` | n/a | 9 AI items: 4 accepted (44%), 2 edited, 3 rejected; usable at all 67%; 3 added |
| Draft `--unreviewed`, `--impl giftcard` / `giftcard_buggy` | n/a | 3 failed, 5 passed, 1 skipped / identical |
| Approved suite, `--impl giftcard` / `giftcard_buggy` | n/a | 9 passed / 1 failed (TC-H1) |
| Draft without `--unreviewed` | n/a | collection refused: not signed off |
| `python lab.py check-data evidence/data_draft.run1.txt` | exits: needs oracle | 7 problems on TD-02, TD-03, TD-06, TD-09, TD-10, TD-11 |
| `python lab.py preflight materials/qa-bug-note.txt --cls internal` | GIFT_CARD not caught | GIFT_CARD 1 (production code), QATEST code kept readable |

Everything in `solution/evidence/` is a **backup reply written for the course**, not live Claude output. Use the files when Claude is unavailable or to calibrate grading.

## The defect
`giftcard_buggy.py` accepts 15-character codes (`{15,16}` instead of `{16}`). Claude drafts usually test 17 characters and forget 15; the reviewer's ADDED boundary case is what catches it. The draft also fails on the **correct** application (wrong expectations TC-02, TC-06, TC-07), so its red results are noise: the point of the 2x2 table.

## Expected reasoning (grading anchors)
- **Findings:** "within 3 seconds" and "AC6 / one gift card per order" are invented and must be discarded. A trainee who keeps them loses most Stage 1 marks.
- **Coverage check is crude:** `reference_coverage` reports "order total includes shipping/tax" as found because the words "order total" appear in another finding. The exemplar `REVIEW.md` shows the reviewer catching this by reading. Reward trainees who notice.
- **Question log:** PO answers come from the PO only. Spaces/dashes must stay OPEN; any test or data row that depends on it is parked (TC/TD) or moved to questions.
- **Oracle:** must not import `shopfront`; must return `None` for spaces or dashes; must apply the case-insensitivity answer; `min(balance, total)` with cent rounding.
- **Decisions:** TC-02 EDITED (WRONG_EXPECTED, a card cannot pay more than the total); TC-06 EDITED (contradicts the PO answer it was given); TC-07 and TC-08 REJECTED (INVENTED_REQUIREMENT, out of scope per PO); TC-09 REJECTED (DUPLICATE). ADDED: the 15-character boundary is essential; balance at total minus 0.01 and equal to the total are strong additions. AC5 shows NOT COVERED in the approved suite on purpose (out of scope) and should be explained, not padded.
- **Sign-off:** approver must be a different person. Watch for trainees typing a fake second name; the classmate's name should also appear in their own submission or the commit history.
- **Data:** TD-06 is mechanically "applied" by the oracle but is a realistic retailer card number: it must go (C8). TD-10 depends on the open question. TD-12 is legal but low-value (same partition as TD-01): accept either keep with reason or drop.
- **Responsible use:** the raw note is not "internal" as written: it holds a customer's name, address and phone, a production gift card code, a staging password and a bearer token. Expected handling: delete the customer and production-code lines by hand, then pre-flight as internal; name the password and token for rotation and the production code for reporting to support. The redactor misses the name, street, order id and staging URL by design.
- **GIFT_CARD rule:** the exemplar is `\b(?!QATEST)(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{15,17}\b` placed before CARD and PHONE. Accept any rule that catches `Z7KQ4M2PX9LT3B8C`, leaves `QATEST...` readable and does not swallow the 16-digit test card number (which CARD should catch). Requiring a letter and a digit is what distinguishes it from card numbers.
- **Defect draft:** the backup draft overstates severity and adds an unverified claim (14-character codes). Trainees must check claims with a `python -c` call; the exemplar report shows the corrections.

## Known gotchas
- Run commands from the folder holding `pytest.ini` and `lab.py`.
- `review-template` writes the file itself (`--out`) and refuses to overwrite; this avoids PowerShell's UTF-16 redirection breaking the JSON.
- `tests/test_suite_rows.py` is skipped until `review/approved_suite.json` exists; after sign-off it runs 9 rows by default.
- If a live Claude draft uses different key names, `check-suite` will raise a KeyError or report missing fields: that is structure drift (Tuesday). Re-ask once in the same chat with the exact keys, or use the backup.
- If a trainee's oracle is wrong, `check-suite` and `check-data` will point at correct AI values. That is a good learning moment: the oracle is human work and gets reviewed too.
