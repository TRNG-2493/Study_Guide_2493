# Exercise: Positive and Negative Test Cases for Registration and Login

## Scenario

The Project 1 - QE Foundations team has a new build (0.3.0) of the Registration and Login feature. The Product Owner has just approved specification v2 and asks you, the quality engineer on the team, for a first real test suite before anyone writes a line of automation. A small Python version of the feature is available so you can check your thinking against running software. Your job is to design strong positive and negative cases, make sure no rule is left untested, run a good part of them, and explain every failure you find in terms of failure, defect and error.

This is an individual exercise. The new build is not the demo application from the workshop: it behaves differently, so do not assume you already know where the problems are.

## Project 1 milestone for today

**Milestone 3: Positive/negative test suite v1 for Registration and Login, reviewed and logged.**

By the end of the day Project 1 has (a) a suite of at least 30 cases traced to rules R-01 to R-14, (b) an execution record for at least 10 cases with every failure classified, (c) the two most important failures logged in your QEA Jira project, and (d) five of the cases automated as a first seed for later automation work.

## Learning objectives

By the end you can:

* generate test ideas with "what if" questions and the negative-testing checklist, and classify each as positive or negative with a reason;
* write test cases in the standard format with clear, observable, specific expected results;
* trace every business rule to at least one case and spot gaps;
* execute cases, record actual results and decide Pass or Fail against the specification;
* describe each failure as failure, defect and likely error;
* automate a few cases as simple pytest-style tests;
* review your own work against a checklist and improve it.

## Prerequisites

Written lessons for Wednesday (Week 3):

* "Positive and Negative Testing": section "5. Categories of negative tests", "6. Expected-result thinking for negative cases", "7. Deriving positive and negative test cases from requirements", "8. Writing good test cases: the standard fields", "9. Logging failures found by negative tests", and the "Checklist: Negative Testing for Forms".
* "Defect vs. Error vs. Failure": sections "2. The Core Chain" and "8. Where Do Errors Come From?".
* "Testing Mindset" and "Testing Principles" (for the what-if habit and "exhaustive testing is impossible").
* The Wednesday workshop demo (what-if prompt cards and the classification worksheet).
* From Tuesday: the test case format and the defect report template, plus your QEA Jira project.

You do not need any formal technique. Choose your test data by reasoning about the rule ("one more than allowed", "the same thing in capitals", "left empty"). Thursday introduces the formal techniques that make these choices systematic.

## Time estimate and plan (about 2 h 40 min)

| Part | Activity | Time |
|---|---|---|
| 1 | Test idea brainstorm and classification | 25 min |
| 2 | Write the 30+ test cases | 55 min |
| 3 | Traceability matrix | 10 min |
| 4 | Execute 10+ cases and classify failures | 30 min |
| 5 | Automate 5 cases | 25 min |
| 6 | Self-review and fix 3 weaknesses | 10 min |
| 7 | Reflection | 5 min |

If you run short of time, protect Parts 2, 3 and 4; Part 5 can be done with plain `assert` lines.

## Tools needed

A text editor, Python 3.8+, pytest (`pip install pytest`), your Jira QEA project, and a terminal.

## Provided files

| File | Purpose |
|---|---|
| `templates/feature-spec-registration-login-v2.md` | The specification with rule IDs R-01 to R-14. Read it fully first. |
| `templates/idea-brainstorm-template.md` | Part 1 |
| `templates/test-case-suite-template.md` | Parts 2, 3 and 4 (cases, traceability, execution) |
| `templates/failure-classification-template.md` | Part 4 |
| `templates/review-checklist.md` | Part 6 |
| `templates/reflection-template.md` | Part 7 |
| `starter_code/` | The build under test, a command-line runner and a starter pytest file. Read `starter_code/README.md`. |

## Tasks

### Part 1: Brainstorm (about 25 min)

Read the specification. Using the what-if prompts in the template and the "Checklist: Negative Testing for Forms", write at least 40 ideas. For every idea mark it positive or negative and add one sentence of rationale ("because the rule says ..."). Merge duplicates and keep at least 30 for Part 2.

### Part 2: Write the test cases (about 55 min)

Write at least 30 cases in `test-case-suite-template.md`: at least 12 positive and at least 18 negative. Use IDs TC-001, TC-002, and so on. Each case has: ID, title, type, rule ID(s), priority, preconditions, numbered steps, concrete test data, and an expected result.

Expected results must be checkable by someone else. For negative cases state the exact message, that the state is unchanged (for example, the number of accounts did not grow, no remember token is returned) and that nothing sensitive leaks (for example, the message must not reveal whether an account exists). Design each case to break one rule only.

Cover both Registration and Login, including lockout and remember me.

### Part 3: Traceability (about 10 min)

Fill the matrix in the template: for every rule R-01 to R-14 list the cases that cover it and count positive and negative ones. If a rule has no case, write one more. Submit with no gaps.

### Part 4: Execute and classify (about 30 min)

Execute at least 10 of your cases with `starter_code/run_cases.py` (see `starter_code/README.md`). Use `reset` between cases that need a clean start. Copy the actual output into "Actual result" and mark Pass or Fail by comparing with your expected result from the specification, not with what you feel the program should do.

For every failed case fill one row of `failure-classification-template.md`:

* **Failure**: what you observed, expected versus actual.
* **Defect**: the flaw in the product that most likely causes it, described as behaviour ("the check seems to use the text before trimming"), based on evidence from further experiments, not by reading the code.
* **Error**: the plausible human mistake that put the defect there (a misunderstanding, an oversight, a copy mistake).

Group failures that share one defect. File your two most important failures in your QEA Jira project with the Tuesday defect report template and put the keys in the suite. Choose cases that give you a mix of positive and negative results; if all your first 10 pass, run more cases until you have examined the whole suite or found failures.

### Part 5: Automate 5 cases (about 25 min)

In `starter_code/test_starter.py` there are two worked examples. Add five more tests: three from your positive cases and two from your negative cases. Name each test after the case ID (for example `test_tc_009_login_with_email`). Each test makes a fresh service, performs the steps, and uses `assert` on the exact message and on the state. Run `python -m pytest -v`. A failing test is useful information: decide if it is a product defect or a mistake in your test, and note which in a comment.

### Part 6: Self-review (about 10 min)

Apply `review-checklist.md` to your suite. Find three weaknesses (for example, a vague expected result, a duplicate, a case that checks two rules), fix them, and record before and after in the checklist.

### Part 7: Reflection (about 5 min)

Write 4-6 sentences in `reflection-template.md`: which mindset habits found the most defects for you?

## Deliverables (exact filenames)

Put these in a folder `week3-wednesday-<your-name>`:

| File | Content |
|---|---|
| `01-idea-brainstorm.md` | Part 1 |
| `02-test-case-suite.md` | Parts 2, 3 and 4 (cases, traceability matrix, execution results) |
| `03-failure-classification.md` | Part 4 classification table and grouping |
| `04-test_registration_login.py` | Part 5: a copy of `test_starter.py` with your five tests added |
| `05-review-checklist.md` | Part 6 |
| `06-reflection.md` | Part 7 |
| `07-jira-keys.txt` | The two QEA keys and one-line titles |

## Definition of Done (checklist)

* [ ] The suite has at least 30 cases, at least 12 Positive and at least 18 Negative.
* [ ] Every case has all fields filled and no duplicate IDs.
* [ ] No expected result is vague ("works", "shows error"); every negative expected result names the message or outcome and the unchanged state.
* [ ] The traceability matrix lists R-01 to R-14, every rule has at least one case and "Rules with a gap" is 0.
* [ ] At least 10 cases have an actual result and a status.
* [ ] Every Fail row appears in the failure classification with failure, defect and error filled, and Fail rows that share a defect are grouped.
* [ ] Two failures are logged in Jira and the keys are in `07-jira-keys.txt`.
* [ ] Five new automated tests (3 positive, 2 negative) are in the file and `python -m pytest -v` runs without errors in the file itself (a test may fail only because of a product defect, with a comment saying so).
* [ ] The review checklist is complete with three before/after fixes.
* [ ] The reflection has 4-6 sentences and cites at least one case ID.

## Grading rubric (100 points)

| Criterion | Points |
|---|---|
| Part 1: at least 40 ideas, classified with rationale | 10 |
| Part 2: 30+ cases, correct mix, complete fields, concrete data | 15 |
| Part 2: quality of expected results (exact, observable, state unchanged, no leak) | 15 |
| Part 3: complete, correct traceability, no gaps | 10 |
| Part 4: execution honest and accurate (Pass/Fail judged from the spec) | 10 |
| Part 4: failure/defect/error chain correct and grouped; Jira reports clear | 15 |
| Part 5: five tests, correct pattern, assertions exact | 12 |
| Part 6: three real weaknesses found and fixed | 8 |
| Part 7: reflection specific and honest | 5 |
| Total | 100 |

## Stuck? Hints (try first, then open)

* No ideas? Take one rule and ask the what-if prompts: empty, one shorter, exactly on the limit, one longer, different case, twice.
* Not sure what is positive? A positive case uses data the spec says is allowed and expects success; a negative case uses data the spec forbids and expects a safe refusal. A case that is "allowed but unusual" (for example, extra spaces that the spec says are removed) is positive.
* Vague expected result? Copy the exact message from the specification table.
* Not sure how to check "state unchanged"? Run `python run_cases.py show` before and after.
* A case failed but the program "looks right"? Reread the rule; then re-run with a slightly different input to see how general the behaviour is. If several inputs fail the same way, you have likely found the boundary of a defect.
* Not sure what the "error" is? Ask "what could a busy developer have misread, forgotten or mistyped?" Describe a human mistake, not a line of code.
* Lockout cases need several failed logins in a row; run them in order after one `reset` and one `register`.

## Common mistakes

* Only happy paths: 25 positive cases and 5 negative ones.
* Vague expected results: "an error is shown" instead of the exact message and state.
* Duplicate cases: three cases with the same data and the same check under different titles.
* One case that tests five rules at once, so you cannot tell which one failed.
* Setting the expected result from the actual program output instead of from the specification.
* Calling the failure the defect: the failure is what you see; the defect is in the product; the error is the human mistake.
* Forgetting preconditions (for example, "alice@example.com is registered").
* Leaving a rule uncovered because it seems trivial (R-08, R-12, R-14).

## Stretch goals (optional)

* Ask an AI assistant to brainstorm 20 extra test ideas from the specification, then review its output critically with these three questions: (1) Which expected results does it state that are not in the specification (hallucinated expectations)? (2) Which ideas duplicate yours, and which are new and valuable? (3) Which ideas are impossible or out of scope for this build? Add only the ideas you can justify from the specification and note the rest as rejected with reasons.
* Add two more automated tests for the lockout rule.
* Write down three questions you would ask the Product Owner about unclear parts of the specification (for example, how a lock is released).

## Submission instructions

Put all deliverables in one folder named `week3-wednesday-<your-name>` and submit it the way your cohort submits work (for example, a zip file or your course repository). Make sure your instructor can view the two Jira issues in the QEA project. Submit before the stated deadline.

## What's next

Thursday introduces formal test design techniques. You will return to your data choices (for example, why 7 and 65 characters, or 2 and 21) and see how the techniques make those choices systematic rather than a matter of judgement.
