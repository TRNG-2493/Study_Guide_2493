# Exercise: Project 1 Test Design Document and Regression and Risk Plan (Week 3 Capstone)

Individual exercise. Estimated time: 2 h 40 min (range 2 to 3 h). Mode: design, analysis and documentation, with small optional hands-on parts.

## Scenario

Project 1 (the web app with User Registration and Login, plus Membership and Promo Codes) is close to its v1.0 release. Next week's release 1.1 is already planned. The product owner asks for a release readiness review and two documents the whole team can rely on:

1. a **Test Design Document** that shows what is tested, why, with which technique, and how well it is covered;
2. a **Regression and Risk Plan** that says what could go wrong, which tests protect against it, and when the release may go.

You are the QE for the review. You are not starting from nothing: you have four days of artifacts. Your job today is to consolidate, close the gaps (non-functional, exploratory, data-driven, performance) and decide what to run when time is short.

## Project 1 milestone for today

**Milestone 5 (Week 3 capstone): Project 1 Test Design Document v1.0 and Regression and Risk Plan v1.0 ready for review.**
Milestone 4 (Thursday's pair-designed suite for Membership and Promo Codes) is the main input.

## Learning objectives

By the end you can:

- consolidate requirements, techniques, test cases and results into one traceable test design document;
- write exploratory charters in the Explore / With / To discover format and record a session on a session sheet;
- write non-functional requirements that are measurable (a number, a condition and a way to test it);
- score risks with likelihood x impact and use them to tier a regression suite (smoke, core, full);
- run an impact analysis for a change request and select regression tests with a written justification;
- turn a test table into a data-driven dataset;
- describe a performance test scenario with a workload model and acceptance criteria without running it;
- review a peer document with a checklist and fix your own gaps.

## Prerequisites

Friday lessons (read or skim the sections named):

- `regression-testing.md`: sections 9 (selection and prioritization, including 9.1 risk-based and 9.2 impact analysis), 10 (test suite tiers), 11 (automation) and 17 (go/no-go and the sample release checklist).
- `exploratory-testing.md`: sections 6 (charters), 7 (session-based test management and the session sheet) and 8 (heuristics).
- Functional vs Non-Functional Testing; Performance and Stress Testing; Reliability and Scalability (availability and "nines"); Data-Driven Testing; White-Box Testing (for the coverage summary vocabulary).

Gather these artifacts from earlier in the week (use your own IDs and filenames):

| Day | What to bring |
|---|---|
| Monday | SDLC/STLC plan (`my-sdlc-stlc-plan.md`), Jira project and epic |
| Tuesday | Requirements review and RTM (`01-requirements-review.md`), test plan (`02-test-plan.md`), defect reports (`04-defect-reports.md`) |
| Wednesday | Positive/negative test suite (`02-test-case-suite.md`), execution results and failure classification (`03-failure-classification.md`), your five pytest tests |
| Thursday | Pair design documents (`design/technique-selection-table.md`, `design/bva-ep-design.md`, `design/decision-table.md`, `design/state-transition-design.md`), pytest tests, `DEFECTS_FOUND.md` |

If one artifact is missing or weak, say so in section 1.6 of your document ("Known gaps") instead of inventing content.

## Time plan

| Part | Task | Minutes |
|---|---|---|
| 1 | Consolidate the Test Design Document (including a 20-minute exploratory session) | 55 |
| 2 | Non-functional requirements and tests | 20 |
| 3 | Regression and Risk Plan | 45 |
| 4 | Data-driven dataset | 10 |
| 5 | Performance scenario (conceptual) | 15 |
| 6 | Peer review checklist, self-review fixes and reflection | 15 |
| | Total | 160 (2 h 40 min) |

Tools: a text editor, optionally Python 3 and pytest (`pip install pytest`). Everything can be done on paper-style markdown. Templates are in `templates/`; optional starter code is in `starter_code/` (see its README).

## New change scenario (for Part 3)

> **Release 1.1 change request.**
> (a) Add a **"Sign in with a partner account"** button on the login page. Partner users sign in with a partner token and do not need a Project 1 password.
> (b) Change the **session timeout from 30 to 15 minutes** of inactivity.
> (c) Update the **promo-code length rule from 6-10 to 8-12 characters**.

Impact hints (areas to think about, not answers):

- (a) New entry point to the system. What else shares the login page, the account store, the lockout rules and error messages? What happens to a user who has no password? What new data and security questions appear?
- (b) A number changes, but where is that number used? Think of activity that extends a session, what the user sees at expiry, and any place the old value may have been copied.
- (c) A validation rule changes. Think of boundaries, of codes that used to be valid and now are not (and the reverse), of where the rule is shown to the user, and of tests that hard-code the old limits.

## Tasks

### Part 1: Consolidate the Test Design Document (about 55 min)

Copy `templates/test-design-document-template.md` to `project1-test-design-document.md` and complete sections 1 to 6:

1. **Scope and test basis**: in/out of scope, the requirement list you actually used (IDs), references to Monday to Thursday artifacts.
2. **Test levels and types**: a table for Project 1 listing each level or type, whether it is functional or non-functional, which features it covers and how (manual, automated, exploratory).
3. **Techniques applied per feature**: a traceability table requirement -> technique -> test cases, taken from your Wednesday suite and Thursday design. Summarize counts (tests per feature, automated vs manual, executed, passed, failed).
4. **Coverage summary**: requirements covered / total, techniques used, and what you did NOT cover and why.
5. **Exploratory testing**: three charters in the Explore / With / To discover format, plus one filled session sheet from a 20-minute session. Use any practice site (a public site meant for practice) or your own Project 1 app or the starter module. Save the sheet as `exploratory-session-sheet.md` and link it from the document.
6. **Known gaps and assumptions.**

### Part 2: Non-functional requirements and tests (about 20 min)

Complete section 7 of the document using `templates/non-functional-requirements-template.md`. Write **six** measurable items for Project 1, one each for: performance (percentile target and load), security, usability or accessibility, compatibility, reliability (availability target with the downtime calculation shown), scalability. Each row needs an ID, the measure (number + condition), the way it would be tested, and a tool or method name.

### Part 3: Regression and Risk Plan (about 45 min)

Copy `templates/regression-and-risk-plan-template.md` to `regression-and-risk-plan.md` and complete it for the release 1.1 change request:

1. **Risk register**: at least 8 risks, each with likelihood (1-5), impact (1-5), score = L x I, mitigation and owner (a role is fine).
2. **Impact analysis** for changes (a), (b) and (c): what is touched, how, why it matters, linked tests.
3. **Selection and tiers** from your own suite: assign every selected test to smoke, core or full with a justification (risk score, history, change impact). Cover all three changes.
4. **Estimated execution time per tier**, with the assumption behind each estimate.
5. **Automation candidates** with reasons, and what stays manual or exploratory.
6. **Entry and exit criteria** and a **go/no-go checklist** for release 1.1.

### Part 4: Data-driven angle (about 10 min)

Convert one of your test tables (login or promo code is a good fit) into `test-data-login.csv` with at least **12 rows**, each with inputs and an expected result (use `templates/test-data-csv-template.csv`). In section 8 of the document, show 3 `pytest.mark.parametrize` lines (or a short CSV-driven snippet) that would run it. Running it is optional: `starter_code/` has a reader and a small module.

### Part 5: Performance overview (about 15 min, conceptual)

Write a one-page `performance-scenario-login.md` from `templates/performance-scenario-template.md`: workload model (users, think time, ramp-up, steady state), acceptance criteria (p95, throughput, error rate), environment and data. You do NOT have to run anything.

### Part 6: Review, fixes and reflection (about 15 min)

1. Swap with a peer (or review yourself after a break) using `templates/review-checklist.md`; save the result as `review-checklist.md`.
2. List at least three fixes you made after the review at the end of your document.
3. Write `reflection.md`: exactly 5 sentences on the biggest quality risk for Project 1 and what you would do about it.

## Deliverables (exact filenames)

Folder: `week3-friday-<your-name>/`

| File | Content |
|---|---|
| `project1-test-design-document.md` | Parts 1, 2 and the Part 4 snippet (sections 1 to 8, plus the fixes list) |
| `exploratory-session-sheet.md` | One filled session sheet (20 min) |
| `regression-and-risk-plan.md` | Part 3 |
| `test-data-login.csv` | Part 4 dataset (12+ rows) |
| `performance-scenario-login.md` | Part 5 |
| `review-checklist.md` | Part 6 completed checklist |
| `reflection.md` | Part 6, five sentences |

## Definition of Done

- [ ] Every requirement in your list has at least one test case and a named technique in the traceability table.
- [ ] Counts in the summary match the tables (number of tests per feature adds up to the total).
- [ ] Coverage summary states what is not covered and why.
- [ ] Three charters use Explore / With / To discover and each has a time box.
- [ ] The session sheet has charter, start time, duration, notes with timestamps, at least one bug or question, and one new test idea.
- [ ] Six NFRs exist, each with a number or condition (no words like "fast" or "secure" alone) and a test method.
- [ ] The availability item shows the arithmetic for allowed downtime per month (or year).
- [ ] Risk register has 8 or more risks, each scored L x I with mitigation and owner.
- [ ] Impact analysis covers changes (a), (b) and (c) separately.
- [ ] Regression selection covers all three changes with tier and rationale for every test.
- [ ] Execution time is estimated per tier with an assumption stated.
- [ ] At least 3 automation candidates with reasons, and at least 1 test kept manual or exploratory with a reason.
- [ ] Entry criteria, exit criteria and a go/no-go checklist with measurable thresholds are present.
- [ ] `test-data-login.csv` has 12 or more rows, a header, and an expected result in every row; the file has consistent column counts.
- [ ] Three parametrize lines or a CSV-driven snippet are included.
- [ ] Performance scenario has users, think time, ramp-up, steady state, p95, throughput and error-rate targets.
- [ ] Review checklist is completed and at least 3 fixes are listed.
- [ ] Reflection has exactly 5 sentences.
- [ ] IDs (REQ, TC, R, NFR) are used consistently across all files.

## Grading rubric (100 points)

| Area | Points | What earns full marks |
|---|---|---|
| Part 1: consolidation, traceability, coverage | 20 | Complete table, honest counts, gaps stated |
| Part 1: exploratory charters and session sheet | 8 | Good charters, real notes, follow-up ideas |
| Part 2: non-functional requirements | 12 | Six measurable items, correct downtime calculation |
| Part 3: risk register | 10 | 8+ risks, sensible scores, useful mitigations |
| Part 3: impact analysis and selection | 14 | All three changes, tiers justified |
| Part 3: time, automation, criteria, go/no-go | 6 | Checkable and realistic |
| Part 4: dataset and parametrize | 8 | 12+ rows with variety (valid, invalid, boundary) |
| Part 5: performance scenario | 10 | Complete workload model and measurable criteria |
| Part 6: review, fixes and reflection | 6 | Real fixes, focused reflection |
| Consistency and clarity | 6 | IDs match, tables readable, no contradictions |

## Hints (no answers)

- Start from your requirement IDs, not from test cases. Every row of the traceability table begins with a requirement.
- A risk is "something that could go wrong and hurt", not a test. Phrase it as "if X then Y".
- Likelihood asks "how probable given what changed and what has failed before?". Impact asks "how bad for the user or the business?". Use the lesson's 1 to 5 scale and say how you scored.
- For tiers, ask: "If I had five minutes, which tests would I run? Thirty minutes? A whole night?"
- A measurable NFR passes this test: could two people run it and agree on pass or fail?
- Downtime for availability A over a period T is (1 - A) x T. Show the unit conversion.
- Think time is the pause between a user's actions, not the server's response time.
- For the CSV, one row should be one test. Include the case that should be refused as well as the ones that should succeed.
- If the change touches shared code, look for tests of other features that call the same code.

## Common mistakes

- Pasting earlier work without connecting it (no traceability, counts that do not match).
- Risk scores that are all 3x3 or all high; no ranking means no prioritization.
- Putting every test in smoke, or running "everything" and calling it a plan.
- NFRs such as "the system should be fast" or "must be secure".
- Forgetting that a regression plan includes tests for behavior that did NOT change.
- Writing charters that are test cases ("Verify login works") or too broad ("Test the app").
- A CSV with an unexpected-result column left empty, or commas inside values without quotes.
- Reflection that lists many risks instead of choosing one.

## Stretch goals (optional)

1. **Tag and run**: put your tests into `starter_code/tests/`, tag them with `smoke`, `regression`, `bugfix` markers to match your tiers, and compare `pytest -m smoke`, `pytest -m "smoke or regression"` and `pytest`. Record what each tier would and would not have caught.
2. **Local load run**: run `starter_code/load_login_local.py` with 10 users and compare the printed p95 and error rate with your scenario's targets. Local runs only; read the warning in the script.
3. **AI-assisted risk brainstorm, then critical review**: ask an AI assistant for risks of release 1.1 and compare with yours. Review its output with three questions: (1) Which suggestions are specific to our app and which are generic? (2) Which ones did I miss, and which ones are wrong or already covered? (3) How would I verify each one it proposes, and what would I not accept without evidence? Keep your own scores; do not paste its output unchecked.

## Submission instructions

Put the seven files in the folder named above and submit it as your instructor directs (for example, a repository or a zipped folder). If you used the starter code, include your edited test file and CSV copies in a subfolder `code/`. Check the Definition of Done before you submit.

## Week 3 wrap-up

This week you moved from "what is quality" through lifecycle, requirements, test design techniques and today's advanced concepts. The two documents you produced are your Week 3 portfolio: they show you can plan, design, prioritize and communicate testing. Keep them tidy and versioned; later work in the program will build on them as the baseline for your project's tests and plans.
