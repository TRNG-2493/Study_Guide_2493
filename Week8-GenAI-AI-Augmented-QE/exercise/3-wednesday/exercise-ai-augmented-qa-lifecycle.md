# Exercise: Generate and Review AI Test Cases and Test Data, Documenting Every Correction

**Week 8, Wednesday** | Time box: 2-3 hours | Individual work (a classmate signs off as approver in Stage 4) | Tools: Claude, Python 3.10+, pytest, Git | Mode: Hybrid (analysis and review, run through code)

## Objectives
By the end you can:
1. Review a user story yourself first, then with Claude, check that every Claude finding is grounded in the story, and turn findings into a question log the product owner answers.
2. Write your own oracle **before** reading any AI test case, and use it to recompute every expected result Claude proposes.
3. Generate test cases from the story plus the PO answers, review every case with the nine-point checklist, and record each decision in a correction log.
4. Pass a sign-off gate with a named reviewer and a different approver, so only approved tests run, and show which suite catches a real defect.
5. Generate constrained synthetic test data and prove it with independent checks, not Claude's own labels.
6. Run a pre-flight and redaction before pasting a real-looking artefact into Claude, and disclose AI assistance.

## Prerequisites and setup
- Read today's seven lessons in `written/3-wednesday/`. Keep `human-validation-of-ai-output.md` (sections 2, 4, 9 and 10) and `responsible-use-of-ai-in-qe.md` (sections 3, 4 and 8) open.
- Have the Wednesday demo to hand: `demos/3-wednesday/code/demo_ai_augmented_qa_lifecycle.md`, `lifecycle_lab.py` and `review_checklist.md`. Today's starter uses the **same commands and helpers**, pointed at a new story.
- Claude in a plain chat (no Project, custom instructions or memory), a **fresh chat for every prompt**.

1. Copy `starter_code/` to `week8-wednesday-<yourname>/`, `pip install -r requirements.txt`, `git init`, commit the starter.
2. `python lab.py lint` should print five lines. `python -m pytest -q` should show **5 failed, 1 skipped**: the failures are your oracle, still to be written.
3. Read `README.md` and `review/review_checklist.md`.

## Scenario
The ShopFront team is adding gift card payments at checkout (story **US-420** in `qa_flow/stories.py`). It is money at checkout, so the team lead wants the full AI-augmented flow with a human gate at every hand-over: story, findings, cases, data. Her rule from this morning's demo: **Claude may find problems and ask questions. It may not answer them.** Answers come from the product owner. Your instructor plays the product owner; if that is not possible, use `materials/po-answers.md` under the rule written at its top.

## Rules for using Claude today
1. Fresh chat per prompt. Paste exactly what `lab.py` prints; do not "improve" the prompts (that was Tuesday).
2. Save every reply in `evidence/` exactly as it came. Never edit a saved reply; corrections live in `review/`.
3. Synthetic material only, except in Stage 6, where you practise deciding what may go in.
4. Code **points**, you **decide**. A finding, case or row with no pointers is not approved until you have read it.
5. Every AI-assisted file you commit carries the disclosure line (`python lab.py disclose ...`). Log every prompt in `review/ai_usage_log.csv`.
6. Commit at the points marked **Commit**. The order of your commits is evidence that your review and oracle came first.

## Stage 1: Requirements analysis (about 35 min)
1. **Your review first.** Before any prompt, read US-420 and write at least **4** problems in `REFERENCE_ISSUES` in `qa_flow/stories.py` (name plus keywords) and in section 1 of `review/REVIEW.md`. Use the five defect categories from `ai-assisted-requirements-analysis.md`. **Commit.**
2. Run `python lab.py lint` (the deterministic baseline). Note what a word list can and cannot see.
3. `python lab.py review-prompt`, paste into a fresh Claude chat, save the reply as `evidence/findings.run1.txt`.
4. `python lab.py check-findings evidence/findings.run1.txt --log review/question_log.md`.
5. Give every finding a verdict in `REVIEW.md` section 2: keep or discard, and why. A FLAG (quote not in the story, AC that does not exist, invented number) is a discard unless you can show the checker is wrong. An OK finding is not automatically relevant.
6. Compare with your own review: what did Claude find that you missed, and what did you find that Claude missed? Do not trust the "found" lines blindly: they are keyword matches. Add any missing question to `review/question_log.md` by hand. **Commit** the question log with every question OPEN.
7. Get the answers from the product owner. Record them in the log (status ANSWERED, answer text), then copy **only** the answered ones into `PO_ANSWERS` and the rest into `OPEN_QUESTIONS` in `stories.py`. Never fill an answer yourself, and never let Claude answer one. **Commit.**

Checkpoint: at least 3 questions answered by the PO, at least 1 still open, and your review committed before `findings.run1.txt`.

## Stage 2: Your oracle first (about 15 min)
1. Implement `oracle_us420()` in `qa_flow/stories.py` from AC1 to AC4 **plus** the PO answers. Return `None` for anything still open. Do not import `shopfront`: the application is never the oracle for its own tests.
2. `python -m pytest -q tests/test_oracle.py` must pass (5 passed).
3. Run `python lab.py oracle` and paste the table into `REVIEW.md` section 4. Check every row by hand. **Commit before Stage 3.**

Checkpoint: the oracle table exists in Git before any test case draft does.

## Stage 3: Generate test cases (about 20 min)
1. `python lab.py tc-prompt`. Check that it carries your PO answers and open questions. Paste into a fresh chat and save as `evidence/suite_draft.run1.txt`.
2. `python lab.py check-suite evidence/suite_draft.run1.txt`. Read the trace matrix (forward and backward), the mix, the code-length boundaries (15, 16, 17) and the pointers.
3. Copy the summary into `REVIEW.md` section 5. Write down, **before** Stage 4, your prediction of how many cases will be usable as-is.

## Stage 4: Human review and sign-off (about 40 min)
1. `python lab.py review-template evidence/suite_draft.run1.txt` writes a blank `review/review_decisions.json`. Fill in `reviewer` (you), `date`, and later `approver`.
2. For **every** case, apply the checklist in `review/review_checklist.md` (C1 to C9) and decide: ACCEPTED, EDITED (with `patch`), REJECTED or, for cases you write yourself, ADDED with a **new** id (for example `TC-H1`). Every non-accepted decision needs failed checks, a category and evidence (an AC or a PO answer). An item that enforces an undecided rule is REJECTED and linked to its open question, not flipped to the opposite guess.
3. Add the cases the draft is missing. The trace matrix and the boundary line tell you where to look; your oracle table tells you the expected values.
4. Ask a classmate to act as **approver**: they read your decisions file and correction reasons, and if they agree, you add their name. Money at checkout needs two people; the gate refuses the same name twice.
5. `python lab.py signoff evidence/suite_draft.run1.txt review/review_decisions.json`. Fix every refusal until it passes. It writes `review/approved_suite.json` and `review/correction_log.csv` and prints the metrics. Paste the metrics into `REVIEW.md` and compare them with your prediction.
6. **Which suite catches the bug?** Run all four and fill the 2x2 table in `REVIEW.md`:
   - `python -m pytest -q tests/test_suite_rows.py --suite evidence/suite_draft.run1.txt --unreviewed --impl giftcard`
   - the same with `--impl giftcard_buggy`
   - `python -m pytest -q tests/test_suite_rows.py --impl giftcard`
   - `python -m pytest -q tests/test_suite_rows.py --impl giftcard_buggy`
   Then explain in 3 to 5 sentences: which failures are real defects and which are wrong expectations, and which case caught the bug. Only after that, read the difference between `giftcard.py` and `giftcard_buggy.py`. **Commit.**

Checkpoint: sign-off passes, every AI item has exactly one decision, at least one ADDED case, and your approved suite is green on `giftcard` and red on `giftcard_buggy`.

## Stage 5: Test data (about 25 min)
1. `python lab.py data-prompt`, paste into a fresh chat, save as `evidence/data_draft.run1.txt`.
2. `python lab.py check-data evidence/data_draft.run1.txt`. The checks recompute every label with **your** oracle and enforce one change per row, strings only and the `QATEST` prefix.
3. For each reported problem, decide in `REVIEW.md` section 6 who is right: Claude, your oracle, or neither (a PO question). If your oracle is wrong, fix the oracle **and** say so; do not fix it to agree with Claude.
4. Read every row, including the ones with no problem. What would no script notice? (Relevance, duplicate partitions, values that look real.) Record what you found.

## Stage 6: Responsible use and a defect report (about 20 min)
You want Claude to draft the defect report for the bug you caught in Stage 4. A colleague's raw note is in `materials/qa-bug-note.txt`.
1. **Classify** the note before anything else (`responsible-use-of-ai-in-qe.md` section 4): what kinds of data does it contain? Is it really "internal"? Write your answer in `REVIEW.md` section 7.
2. Gift card codes are bearer value, and the redactor in `qa_flow/responsible.py` does not catch them. Add a `GIFT_CARD` rule (see the TODO) and add it to `SECRET_LABELS`. Your rule must catch a real-looking code but leave codes with the team's `QATEST` prefix readable, because the defect report needs the test code.
3. `python lab.py preflight materials/qa-bug-note.txt --tool claude --cls <your classification>`. Then **read** the redacted text. Remove by hand anything the redactor missed that must not go in. Write a short list of what had to be removed and which secrets must be rotated or reported.
4. Paste only the cleaned note into a fresh chat with this request, and save the reply as `evidence/defect_draft.run1.txt`:

```text
Write a defect report from the tester's note below. Use these headings: Title, Severity,
Environment, Steps to reproduce, Expected result, Actual result, Notes.
Use only facts stated in the note and the requirement. If something is not stated, write
"Not stated" instead of guessing.

<requirement>
<paste US-420 AC1 and AC4 here>
</requirement>

<note>
<paste your cleaned note here>
</note>
```

5. Verify every claim in the draft before you accept it: reproduce the actual result with a one-line `python -c` call against `shopfront/giftcard_buggy.py`, check each extra claim the same way, and justify the severity yourself. Record what you corrected.
6. Add the disclosure line (`python lab.py disclose --tool Claude --reviewer <you> --what "defect report"`) to your corrected report `review/defect_report.md`, and complete `review/ai_usage_log.csv` with one row per prompt you sent today. **Commit.**

## Stage 7: Wrap-up (about 10 min)
Complete `REVIEW.md` section 8 (five bullets). Make sure every file Claude helped with has the disclosure line, and `git log --oneline` shows your review and oracle commits before the drafts.

## Stretch goals
- Run the test case prompt a second time (fresh chat) and review only the differences. Did the second run fix or repeat the first run's flaws?
- Write a "mutation" for the app (for example change `balance <= 0` to `balance < 0` in a copy) and check whether your approved suite catches it. If not, add the case.
- Generate 200 data rows **with code** from your reviewed data design (`ai-generated-test-data.md`), not by asking Claude for more rows, and run them through `check_rows`.
- Point gate G4 at code: ask Claude for a pytest file that runs `review/approved_suite.json`, then prove it can fail by running it against `giftcard_buggy` (`ai-assisted-automation-development.md`, sections 12 and 13).

## Deliverables
The Git repository `week8-wednesday-<yourname>/` (zip with `.git`, or a pushed branch) containing:
1. `qa_flow/stories.py` with your manual review, PO answers, open questions and oracle; `qa_flow/responsible.py` with your GIFT_CARD rule.
2. `evidence/` with `findings.run1.txt`, `suite_draft.run1.txt`, `data_draft.run1.txt`, `defect_draft.run1.txt`, unedited.
3. `review/question_log.md`, `review/review_decisions.json`, `review/approved_suite.json`, `review/correction_log.csv`, `review/defect_report.md`, `review/ai_usage_log.csv`.
4. `review/REVIEW.md`, all eight sections complete.

## Definition of Done
- [ ] Your manual review (4+ problems) is committed before `evidence/findings.run1.txt`
- [ ] Every Claude finding has a keep or discard verdict with a reason; flagged findings are explained
- [ ] The question log has every kept question plus any you added, with PO answers or OPEN status; `PO_ANSWERS` and `OPEN_QUESTIONS` match it; no answer came from you or Claude
- [ ] `oracle_us420` passes `tests/test_oracle.py`, returns `None` for open questions, does not import `shopfront`, and its table is committed before `evidence/suite_draft.run1.txt`
- [ ] Every AI test case has exactly one decision; every non-accepted one has failed checks, a category and evidence; at least one ADDED case with a new id
- [ ] `lab.py signoff` passes with a reviewer and a different approver
- [ ] The 2x2 table is filled from real runs and explained; the approved suite passes on `giftcard` and fails on `giftcard_buggy`
- [ ] Every `check-data` problem has a decision (Claude, your oracle or PO question), plus at least one finding from reading alone
- [ ] A GIFT_CARD redaction rule that catches a real-looking code and keeps `QATEST` codes readable
- [ ] The note was classified, read after redaction, and cleaned by hand before pasting; secrets to rotate are named
- [ ] Every claim in the defect draft was verified; corrections recorded; disclosure line present
- [ ] `review/ai_usage_log.csv` has a row for every prompt
- [ ] `python -m pytest -q` passes (with your approved suite); no real data in any prompt you sent; no emojis in any deliverable

## Grading rubric (100 points)
| Criterion | Weight | Full marks when |
|---|---|---|
| Requirements analysis | 15 | own review first (commit order); every finding judged; flagged findings explained; misses in both directions named; question log complete and answered by the PO only |
| Oracle first | 10 | correct for AC1 to AC4 and the PO answers; returns `None` for open questions; committed before the draft |
| Test case review and correction log | 25 | every item decided against the checklist with specific failed checks, categories and evidence; undecided rules parked, not flipped; missing coverage added with new ids; reasons another tester could follow |
| Sign-off and "which suite catches the bug" | 15 | gate passes with two people; 2x2 from real runs; correct explanation of noise versus defect and of the case that caught it; prediction compared with metrics |
| Test data | 15 | every reported problem decided correctly; oracle not bent to match Claude; at least one finding from reading alone |
| Responsible use and defect report | 15 | sensible classification; working GIFT_CARD rule; residual personal data removed by hand; secrets named for rotation; every claim in the draft verified; disclosure and usage log complete |
| Report quality | 5 | `REVIEW.md` complete, concise, evidence-based |

## Common pitfalls and hints
- Writing your review or oracle after reading Claude's output is anchoring. The commit order will show it.
- "No pointers - still read it" means no mechanical problem was found, not that the item is approved. Relevance (C4) and the right AC (C7) have no code at all.
- If a draft case contradicts a PO answer, the PO answer wins, even if the case looks reasonable. If a case depends on an open question, park it.
- An ADDED case reuses no AI id. Look at the boundaries on **both** sides of every limit in AC1 and AC2.
- `signoff` refusing is the gate working. Read every line it prints; each one names the item and what is missing.
- A red test on the correct application is a wrong expectation until proven otherwise. Read the AC before blaming the code.
- If `check-data` says your oracle disagrees with Claude, re-read the AC and the PO answers before changing anything. Your oracle can be wrong too; say so if it is.
- The redactor works by pattern. Names, street addresses, order numbers and URLs have no pattern it knows. Read the output.
- A gift card code pattern that also matches `QATEST...` or ordinary 16-digit test card numbers needs another look: what makes a gift card code different from the other values in the note?
- Severity is your call, based on your team's definitions from Week 3, not Claude's adjective.
- Ask for help after 15 minutes stuck, with the command and its output ready.

## Reference: where to look (no solutions)
| Need | Look at |
|---|---|
| AI levels and gates across the STLC; error propagation | `ai-within-the-qa-lifecycle.md` sections 2 and 3; demo diagram `ai-qa-lifecycle-gates.mermaid` |
| Manual review, defect categories, grounding checks, question log | `ai-assisted-requirements-analysis.md` sections 4 to 10; demo cards 1.1 to 1.4 |
| Oracle first, test case prompt, traceability | `ai-generated-test-cases.md`; `human-validation-of-ai-output.md` section 2; demo cards 2.1 to 2.3 |
| The nine-point checklist, decisions, categories, sign-off | `human-validation-of-ai-output.md` sections 4, 9, 10 and 11; `review/review_checklist.md`; demo cards 3.1 to 3.3 |
| Constrained synthetic data and independent checks | `ai-generated-test-data.md` sections 3, 4, 5 and 7; demo cards 4.1 to 4.3 |
| Classification, redaction and its limits, disclosure | `responsible-use-of-ai-in-qe.md` sections 3, 4, 8 and 13; demo cards 5.1 and 5.2 |
| Gate G4 for automation code (stretch) | `ai-assisted-automation-development.md` sections 12 and 13 |

## Suggested working order and checkpoints
1. After Stage 1, `git log --oneline` shows your review before the findings file.
2. After Stage 2, `python lab.py oracle` prints a full table with exactly the open questions marked `?`.
3. After Stage 4, you can point at the one case that caught the bug and say who wrote it.
4. After Stage 6, nothing in any prompt you sent would embarrass you if the customer read it.
