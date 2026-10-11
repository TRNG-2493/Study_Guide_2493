# Exercise: Review Requirements, Plan, Test and Report Defects for "Account Profile and Password Reset"

## Scenario

The Project 1 team is adding two things to the QE Foundations web app: a **profile page** (change your name and email) and a **password reset** (the "I forgot my password" flow). The Product Owner has sent you a first draft of the requirements. The developers have already built a first version (build 0.5.0), and the team wants to start testing it today.

You are the Quality Engineer. Before anyone tests, you review the draft, because a problem found in a sentence is far cheaper than the same problem found in code. Then you write a lightweight test plan, run your test cases against the program, and report what you find as bugs in the Jira project you created on Monday. This is the whole test management loop in one afternoon, on a small scale.

## Project 1 milestone for today

**Milestone 2: Requirements review + Test Plan v1 + first defects logged in Jira.**

By the end you have (a) a question and issue log with rewritten, testable requirements and an RTM skeleton, (b) a test plan v1 with 8 test cases, (c) an execution log with metrics, and (d) four bugs filed in your QEA Jira project, one of them moved through the Bug workflow.

## Learning objectives

By the end of this exercise you can:

- Review a draft requirements document and classify problems as ambiguity, gap, contradiction, untestable wording or missing non-functional requirement.
- Rewrite a vague requirement as a testable one with Given/When/Then acceptance criteria.
- Build a Requirement Traceability Matrix (RTM) and keep it up to date.
- Write a lightweight test plan and test cases in the standard format.
- Execute test cases, record Pass, Fail or Blocked with evidence, and compute execution % and pass %.
- Write complete defect reports with severity and priority justified separately, file them in Jira, and move a bug through the workflow.

## Prerequisites

| Material | Sections to review first |
|---|---|
| Written lesson `requirements-analysis.md` | "4. Characteristics of a Good Requirement", "11. Defining Testable Conditions from Requirements", "12. The Requirement Traceability Matrix (RTM)" |
| Written lesson `test-planning-and-test-execution.md` | "3. The anatomy of a test plan", "4. Risk-based prioritization", "8. Test case basics", "12. Executing test cases step by step", "13. Recording results: the five statuses", "14. Evidence", "20. Traceability: linking tests back to requirements" |
| Written lesson `defect-lifecycle.md` | "3. The complete defect lifecycle", "9. How to write an excellent defect report", "10. Severity versus priority" |
| Written lesson `jira-issues-stories-tasks-and-bugs.md` | "3.4 Bug", "5. Creating Issues Step by Step" |
| Written lesson `jira-boards-and-workflows.md` | Part 2, "2.3 Designing a Bug workflow for QE" |
| Tuesday demo | The demo's test plan outline, defect report examples and Bug workflow (Open, In Progress, Ready for Retest, Closed) |
| Monday | Your Jira project **Project 1 - QE Foundations** (key QEA). Keep using it; do not create a new one. |

The lesson's own practice (a different draft about password reset) and the demo's registration and login excerpt are separate documents. Use the excerpt in this exercise, and write your own answers.

## Time estimate and plan

Total: about **2 hours 35 minutes** (range 2 to 3 hours).

| Part | Task | Time |
|---|---|---|
| 1 | Requirements analysis: issue log, 4 rewrites, RTM skeleton | 45 min |
| 2 | Test plan and 8 test cases | 40 min |
| 3 | Test execution, log and metrics | 25 min |
| 4 | Defect reports (4), Jira filing, workflow | 35 min |
| 5 | Reflection | 10 min |

## Tools needed

- Python 3.8 or newer (check with `python --version` or `python3 --version`) and a terminal.
- Your Jira Cloud site with project QEA from Monday.
- A text editor or spreadsheet for your documents; a screenshot tool.

## Starter files

| File | Purpose |
|---|---|
| `templates/requirements-excerpt-account-profile-password-reset.md` | The draft requirements you review (14 requirements) |
| `templates/product-owner-answers.md` | The Product Owner's answers. **Open only after Part 1 is finished.** |
| `templates/requirements-review-template.md` | Issue log, rewrite blocks and RTM tables |
| `templates/test-plan-template.md` | Test plan template |
| `templates/test-case-and-execution-log-template.md` | Test case format, execution log and metrics tables |
| `templates/defect-report-template.md` | Defect report fields |
| `templates/jira-bug-import-template.csv` | Optional: header row plus one example row for a Jira CSV import |
| `starter_code/` | The program under test (`account_service.py`, `try_it.py`) and its README. Read the README first. |

## Tasks

### Part 1: Requirements analysis (about 45 min)

1. Read the excerpt twice: once to understand it, once with the "characteristics of a good requirement" as a checklist.
2. Fill the **issue and question log**. For every flaw: requirement ID, the problem words, **category** (Ambiguity, Gap, Contradiction, Untestable wording, Missing NFR), **severity** (High, Medium, Low), why it is a problem, and a question for the Product Owner. Target: **at least 10 distinct flaws**. Some flaws involve two requirements, or the document as a whole.
3. Now open `product-owner-answers.md` and fill the "PO answer" column where it helps. Where there is no answer, write an assumption and label it "Assumption".
4. **Rewrite four requirements** as testable ones (one measurable sentence each) with at least two Given/When/Then acceptance criteria each (one positive, one negative). Choose four that you found flawed, from at least two different categories.
5. Build the **RTM skeleton**: one row per requirement, filling requirement ID, description, priority and Jira story (if any). Test case, result and defect columns stay empty for now.

Save as `01-requirements-review.md`.

### Part 2: Test plan and test cases (about 40 min)

1. Write a lightweight **test plan** with the template: scope (in and out), approach, environment, entry criteria, exit criteria, suspension criteria, risks (at least 4, each with likelihood x impact), roles, schedule and deliverables. Name it `TP-P1-PROFILE-v0.1`. Keep it to one or two pages; a plan nobody reads is not useful.
2. Write **8 test cases** in the standard format. They must cover **at least 7 different requirements**, include **at least 3 negative cases**, and use the Product Owner's answers for exact expected results. Write expected results before you run anything.
3. Update the RTM: add the test case IDs. Check for requirements with no test case and note why (for example "needs more information" or "cannot be executed in the console").

Save as `02-test-plan.md` and `03-test-cases-and-execution-log.md` (section A).

### Part 3: Test execution (about 25 min)

1. Read `starter_code/README.md` and run `python try_it.py help`.
2. Execute your test cases **against build 0.5.0** in the order of your plan. Run `python try_it.py reset-state` first when a case needs a clean start.
3. For each case record the status (**Pass, Fail, Blocked**; use Not Run or Skipped if you did not get to a case), the **actual result** copied from the program, and an evidence note (a saved output or a screenshot, named by the rule in the lesson section "14. Evidence").
4. If a case cannot be run with the program, mark it **Blocked** and write the reason. A Blocked case is not a Fail.
5. Compute the metrics: planned, Pass, Fail, Blocked, executed (Pass + Fail), **execution %**, **pass % of executed**. Check that the five status counts add up to 8.
6. Update the RTM: result column.

Save as `03-test-cases-and-execution-log.md` (sections B and C) and put evidence in the folder `evidence/`.

### Part 4: Defect logging (about 35 min)

1. Choose **four** failures from Part 3 (or from exploratory runs; see hints). Write one **defect report** each with **all fields** of the template, including severity and priority, **each with its own justification**.
2. **File the four bugs in Jira** project QEA as issue type **Bug**: summary, description with exact steps, expected and actual, severity and priority fields, labels `week3-tuesday`, and a link to the related story if one exists. Typing them in is fine; the optional CSV import template is for trainees who want to try it.
3. **Move at least one bug through the workflow**: Open, then In Progress, then Ready for Retest, then Closed. In the lifecycle lesson the step after In Progress is called Fixed; in Tuesday's demo workflow that moment is the transition **Ready for retest**. You play both roles: add a comment saying what the developer would change. For the retest, run the failing steps again on **build 0.5.1** (`python try_it.py --build 0.5.1 ...`), paste the output in a comment, and close the bug only if it now behaves as expected. If your Jira plan does not let you edit the workflow, keep a simulated status history table in your defect file (date, from-status, to-status, who, note).
4. Update the RTM: defect column with the Jira keys.

Save as `04-defect-reports.md`, plus screenshots of the Jira bug list and of the bug's status history.

### Part 5: Reflection (about 10 min)

In 5 to 6 sentences: **which requirement problem would have caused the most expensive defect, and why?** Mention at least one requirement ID and when in the lifecycle the problem would have been found if nobody had reviewed the draft. Save as `05-reflection.md`.

## Deliverables (exact filenames)

| File | Content |
|---|---|
| `01-requirements-review.md` | Issue and question log, 4 rewrites with acceptance criteria, RTM |
| `02-test-plan.md` | Test plan TP-P1-PROFILE-v0.1 |
| `03-test-cases-and-execution-log.md` | 8 test cases, execution log, metrics |
| `04-defect-reports.md` | 4 defect reports and the workflow history of one bug |
| `05-reflection.md` | 5 to 6 sentence reflection |
| `evidence/` | Saved outputs or screenshots named by the evidence rule |
| `jira-bug-list.png` | Screenshot of the QEA bug list showing your four bugs |
| `jira-bug-history.png` | Screenshot of the bug that moved through the workflow (history or comments) |

## Definition of Done (checklist)

- [ ] `01-requirements-review.md` has at least 10 distinct flaws, each with requirement ID, category, severity and a question.
- [ ] At least 3 of the 5 categories are used, and at least one flaw involves two requirements or the whole document.
- [ ] Four requirements are rewritten as single measurable sentences, each with at least 2 Given/When/Then criteria (one positive, one negative).
- [ ] The RTM has one row for each of the 14 requirement IDs and no requirement is left without a coverage note.
- [ ] `02-test-plan.md` has every template section; at least 4 risks have likelihood, impact and score; entry, exit and suspension criteria are each at least 3 checkable items or conditions.
- [ ] `03-...` has exactly 8 test cases, with ID, requirement, preconditions, test data, steps and an exact expected result written before execution.
- [ ] The 8 cases cover at least 7 requirement IDs and include at least 3 negative cases.
- [ ] Every case has a status; every Fail has a Jira key; every Blocked case has a reason; actual results are copied from the program.
- [ ] The metrics table is complete, the five counts add up to 8, and execution % and pass % are calculated with the formulas shown.
- [ ] `04-...` has 4 reports with all template fields; severity and priority each have a separate justification.
- [ ] Four Bug issues exist in project QEA with steps, expected and actual results, and the label `week3-tuesday`.
- [ ] At least one bug shows the path Open, In Progress, Ready for Retest, Closed (real or simulated) with a retest comment that includes the output from build 0.5.1.
- [ ] Requirement IDs and test case IDs are the same in the RTM, the test cases, the execution log and the defect reports.
- [ ] `05-reflection.md` has 5 to 6 sentences and cites a requirement ID.
- [ ] Both Jira screenshots are included.

## Grading rubric (100 points)

| Area | Points | What earns full marks |
|---|---|---|
| Part 1: issue and question log | 12 | 10 or more real flaws, correct categories, reasoned severity, useful questions |
| Part 1: rewrites and acceptance criteria | 8 | 4 measurable rewrites with positive and negative criteria |
| Part 1: RTM skeleton | 5 | All 14 requirements listed, complete columns |
| Part 2: test plan | 12 | All sections, realistic scope, risks scored, checkable criteria |
| Part 2: test cases | 13 | 8 clear cases, exact expected results, good coverage, positive and negative |
| Part 3: execution and metrics | 15 | Honest statuses, copied evidence, correct arithmetic, RTM updated |
| Part 4: defect reports | 15 | Reproducible steps, expected vs actual, justified severity and priority |
| Part 4: Jira filing | 5 | Four well-formed Bug issues in QEA |
| Part 4: workflow | 5 | One bug moved through all statuses with a real retest |
| Part 5: reflection | 5 | Specific, reasoned, uses a requirement ID |
| Consistency and presentation | 5 | IDs consistent across files, clean tables, no unexplained gaps |

## Stuck? Hints (try first, then open)

<details><summary>Part 1: I only found 5 flaws</summary>

Read each requirement and ask: "Could two testers read this and expect different results?" and "What would I type, and what exact message would I expect?" Then compare **pairs** of requirements: do any two say opposite things? Finally, look at what is not in the document at all (what happens before login, after success, under attack, under load).
</details>

<details><summary>Part 1: How do I choose a category?</summary>

Vague word with several meanings: ambiguity. A word nobody can measure ("fast", "easy"): untestable wording. Something a tester needs but is not written: gap. Two statements that cannot both be true: contradiction. A quality attribute (security, performance, usability) with no target: missing NFR.
</details>

<details><summary>Part 2: Where do I get exact expected results?</summary>

From the Product Owner's answers, after you have asked the question. Use the exact message text so that "close enough" is not a result.
</details>

<details><summary>Part 3: A case needs a token or an old token</summary>

Reset requests are "sent" to a simulated mailbox. Look at the command list for how to read it. The clock is simulated too, so you never wait in real time.
</details>

<details><summary>Part 3: The result looks right but I am not sure</summary>

Compare character by character with the Product Owner's text, and check the state after the action as well as the message on the screen.
</details>

<details><summary>Part 4: How do I pick severity and priority?</summary>

Severity is the damage if the user hits it. Priority is how soon the team should fix it. Two bugs can have the same severity and different priority, and your justification must explain each one separately. Use the table in the lesson section "10. Severity versus priority".
</details>

<details><summary>Part 4: I have fewer than four failures</summary>

Run a few extra checks around your cases (different input, a second account, a boundary of the rule you wrote) and also review whether any "Pass" hides a mismatch with the exact expected text.
</details>

## Common mistakes

- Copying the demo's flaws or answers instead of reading this excerpt.
- Logging a flaw as "bad requirement" without quoting the words or asking a question.
- Rewriting a requirement with a new vague word ("should respond fast enough").
- Writing expected results after seeing the program output.
- Marking a case Pass because "it did something", without comparing to the exact expected text.
- Using Blocked when the case simply failed, or marking Fail without a Jira key.
- Defect reports with steps like "reset the password and see the problem". Write the exact commands.
- Severity and priority justified with one shared sentence.
- Bundling two problems in one bug.
- Closing a bug without rerunning the steps on the fix build.

## Stretch goals (optional)

Ask an AI assistant to review the excerpt and list problems. Compare its list with yours and critique it:

1. Which real flaws did it miss, and what kind of flaw (gap, contradiction, missing NFR) does it tend to miss?
2. Did it invent problems that are not in the text, or "fix" a requirement by quietly adding facts the Product Owner never gave?
3. Would you trust its severity ratings? Which would you change, and why?

Write 6 to 8 sentences in `06-ai-review-critique.md`. Never paste confidential data into an AI tool; this excerpt is fictional training material.

## Submission instructions

Put all deliverables in one folder named `week3-tuesday-<your-name>` and submit it the way your cohort submits work (for example, a zip file or your course repository). Include the Jira site URL in a short `README.txt` and make sure your instructor can view the QEA project. Submit before the stated deadline.

## What's next

Wednesday builds on the bugs you found today. You will learn the formal definitions of error, defect and failure and apply test design techniques to the same feature, so keep your Jira project, your defect reports and your test cases. The bugs you filed today become the starting point for tomorrow's analysis.
