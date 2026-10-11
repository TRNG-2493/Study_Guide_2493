# Weekly Knowledge Check: Day 2 - Test Management & Defect Lifecycle (Week3-Quality-Engineering-Foundations)

This knowledge check covers today's five lessons: Requirements Analysis, Test Planning and Test Execution, Defect Lifecycle, Jira Issues, Stories, Tasks and Bugs, and Jira Boards and Workflows. Attempt every question on your own first, using only what you remember and your own reasoning. Only after you have chosen an answer, open the solution under the question to check it and read the explanation. If you miss a question, go back to the lesson section named in its source line and review it.

---
## Part 1: Multiple Choice

Choose the single best answer for each question.

---

### Question 1

A requirements document says in Section 3.1 "Passwords must be at least 8 characters" and in Section 5.4 "Passwords of 6 or more characters are accepted." Which characteristic of a good requirement is violated?

- [ ] A) Testable
- [ ] B) Feasible
- [ ] C) Consistent
- [ ] D) Prioritized

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Consistent

**Explanation:** A consistent requirement does not contradict other requirements, other documents, or itself. Two different minimum lengths for the same rule is a contradiction.

- **Why others are wrong:**
  - A) Testable is about whether a definite pass/fail check can be defined; the problem here is two conflicting values, not an unmeasurable one.
  - B) Feasible is about whether the requirement can be built within technology, budget, schedule and legal limits; nothing here is impossible.
  - D) Prioritized is about stating how important a requirement is; the text says nothing about importance.

- **Source:** requirements-analysis.md, "4. Characteristics of a Good Requirement" (4.4 Consistent)
</details>

---

### Question 2

In MoSCoW prioritization, which category describes a requirement without which the release has no value or is illegal or unsafe?

- [ ] A) Must have
- [ ] B) Should have
- [ ] C) Could have
- [ ] D) Won't have (this time)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Must have

**Explanation:** Must have items are tested first and most thoroughly, and a failing Must blocks release. Registering with a valid email and password is the lesson's Project 1 example.

- **Why others are wrong:**
  - B) Should have is important but a workaround exists; it is painful to omit but not release-blocking.
  - C) Could have is nice to have and included only if time and budget allow.
  - D) Won't have (this time) is agreed to be out of scope for this release.

- **Source:** requirements-analysis.md, "10. Requirement Prioritization with MoSCoW"
</details>

---

### Question 3

What does backward traceability mean in a Requirement Traceability Matrix context?

- [ ] A) Following a requirement forward to the tests that cover it
- [ ] B) Maintaining forward and backward links together as one practice
- [ ] C) Looking up a requirement's priority in the MoSCoW list
- [ ] D) Following tests (or design) back to the requirements they serve

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Following tests (or design) back to the requirements they serve

**Explanation:** Backward traceability goes from tests or design back to requirements, so you can check that every test has a purpose. Forward traceability goes the other way.

- **Why others are wrong:**
  - A) That describes forward traceability (requirement to tests), used to check that all requirements are covered.
  - B) That describes bidirectional traceability, which is the usual goal but is a different term.
  - C) Priority lookup is unrelated to the direction of a traceability link.

- **Source:** requirements-analysis.md, "12. The Requirement Traceability Matrix (RTM)" (12.3 Directions of traceability)
</details>

---

### Question 4

A tester reads a requirements document line by line and marks every sentence that is ambiguous, incomplete or untestable, without running any software. What is this activity called?

- [ ] A) Dynamic testing
- [ ] B) Static testing
- [ ] C) Smoke testing
- [ ] D) Acceptance testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Static testing

**Explanation:** Static testing examines work products such as documents without executing them. Reviewing requirements is sometimes called requirement testing or requirement review.

- **Why others are wrong:**
  - A) Dynamic testing means running the software, which is not happening here.
  - C) Smoke testing is a quick, shallow check of a new build's most critical functions.
  - D) Acceptance testing checks whether the system meets business needs and is ready for use; it needs a running system.

- **Source:** requirements-analysis.md, "5. Requirement Testing: Static Review"
</details>

---

### Question 5

A story note says: "Login cannot be started until the Admin Dashboard story is done." Which INVEST letter does this story violate?

- [ ] A) Negotiable
- [ ] B) Independent
- [ ] C) Valuable
- [ ] D) Small

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Independent

**Explanation:** Independent means a story can be developed and delivered without depending too heavily on others. Waiting on another story breaks that.

- **Why others are wrong:**
  - A) Negotiable is about details being open for discussion, not about build order.
  - C) Valuable is about delivering value to a user or the business; the note does not question value.
  - D) Small is about fitting within one sprint; the problem here is a dependency, not size.

- **Source:** requirements-analysis.md, "9. User Stories and the INVEST Checklist"
</details>

---

### Question 6

A requirement says: "The system shall detect and block every fraudulent registration with 100 percent accuracy." Which characteristic is most directly in doubt?

- [ ] A) Traceable
- [ ] B) Prioritized
- [ ] C) Complete
- [ ] D) Feasible

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Feasible

**Explanation:** Words such as "every", "always", "never" and "100 percent" are warning signs that a requirement may not be achievable within real limits.

- **Why others are wrong:**
  - A) Traceable is about a unique ID and a known source; the sentence says nothing about either.
  - B) Prioritized is about ranking importance; there is no ranking issue in this sentence.
  - C) Complete is about missing inputs, outputs, errors and limits; the sentence's main flaw is the impossible absolute.

- **Source:** requirements-analysis.md, "4. Characteristics of a Good Requirement" (4.6 Feasible and 4.9 Summary table)
</details>

---

### Question 7

Which statement best describes a test strategy, as opposed to a test plan?

- [ ] A) A high-level, long-lived description of the general approach to testing for an organization or product line
- [ ] B) A project-specific document listing who tests which features in a particular release and by when
- [ ] C) A set of conditions, inputs and steps with an expected result for one behavior
- [ ] D) A final report that recommends whether to release

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A high-level, long-lived description of the general approach to testing for an organization or product line

**Explanation:** A test strategy answers "how do we test in general?" and rarely changes between projects. The plan answers what, who, when and where for one release.

- **Why others are wrong:**
  - B) That describes a test plan, which is project or release specific.
  - C) That describes a test case.
  - D) That describes the test closure (exit) report.

- **Source:** test-planning-and-test-execution.md, "2. Test strategy versus test plan"
</details>

---

### Question 8

Which of the following is an example of a suspension criterion?

- [ ] A) 100% of planned test cases executed and at least 95% passed
- [ ] B) Build deployed to the QA environment and smoke test passed
- [ ] C) More than 30% of executed tests fail on the same basic function
- [ ] D) A new build is deployed and the smoke test passes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) More than 30% of executed tests fail on the same basic function

**Explanation:** Suspension criteria define when testing must be paused, such as many tests failing on the same basic function or a login page that will not load.

- **Why others are wrong:**
  - A) That is an exit criterion: conditions for considering testing complete.
  - B) That is an entry criterion: conditions that must be true before testing begins.
  - D) That is a resumption criterion: what allows paused testing to restart.

- **Source:** test-planning-and-test-execution.md, "3. The anatomy of a test plan (IEEE 829 / ISO 29119 style)" (3.14 Suspension criteria and resumption criteria)
</details>

---

### Question 9

Using three-point estimation with PERT, a tester gives O = 2 days, M = 4 days and P = 9 days. What is the estimate E = (O + 4M + P) / 6?

- [ ] A) 5.0 days
- [ ] B) 4.0 days
- [ ] C) 4.5 days
- [ ] D) 9.0 days

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 4.5 days

**Explanation:** E = (2 + 4x4 + 9) / 6 = 27 / 6 = 4.5 days. The pessimistic value pulls the result above the most likely 4 days.

- **Why others are wrong:**
  - A) 5.0 is the plain average of the three values ((2+4+9)/3), which is not the PERT weighting.
  - B) 4.0 is just the most likely value, ignoring O and P.
  - D) 9.0 is only the pessimistic value.

- **Source:** test-planning-and-test-execution.md, "5. Estimation techniques: how long will testing take?" (5.2 Three-point estimation and PERT)
</details>

---

### Question 10

Login tests cannot be run because registration is failing, so no test user can be created. What status should these login tests receive?

- [ ] A) Blocked
- [ ] B) Fail
- [ ] C) Skipped
- [ ] D) Not Run

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Blocked

**Explanation:** Blocked means the test cannot be executed because something outside the test, such as an open defect, prevents it. The login behavior was never actually checked.

- **Why others are wrong:**
  - B) Fail means the test ran and the actual result differed from the expected result.
  - C) Skipped means the test was deliberately not executed for this cycle, with a reason such as descoping.
  - D) Not Run means planned but not yet attempted; here the attempt is prevented by a cause.

- **Source:** test-planning-and-test-execution.md, "13. Recording results: the five statuses"
</details>

---

### Question 11

After a developer fixes the wording of one password error message, a tester quickly checks that message and the surrounding form instead of running the whole suite. What is this check?

- [ ] A) Smoke test
- [ ] B) Full regression run
- [ ] C) Environment readiness check
- [ ] D) Sanity test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Sanity test

**Explanation:** A sanity test is a narrow, focused check after a small change or fix to confirm the change works and nothing obviously related is broken.

- **Why others are wrong:**
  - A) A smoke test is broad and shallow, run on every new build to decide whether it is testable at all.
  - B) A full regression run re-executes a large set of previously passing tests, not a narrow check.
  - C) An environment readiness check verifies the build, database, email service and similar items, not a specific fix.

- **Source:** test-planning-and-test-execution.md, "10. Smoke and sanity checks (introduction)"
</details>

---

### Question 12

Testing found 38 defects. After release, users found 2 more. What is the Defect Detection Percentage (DDP)?

- [ ] A) 5%
- [ ] B) 95%
- [ ] C) 5.3%
- [ ] D) 38%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 95%

**Explanation:** DDP = 38 / (38 + 2) x 100 = 95%. It equals 100% minus the defect leakage of 5%.

- **Why others are wrong:**
  - A) 5% is the defect leakage, the other side of the same fact.
  - C) 5.3% comes from dividing 2 by 38, using the wrong denominator.
  - D) 38% simply repeats the defect count as a percentage.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality" (19.5 Defect Detection Percentage)
</details>

---

### Question 13

A defect has been fixed, the fix is deployed to a test environment, and the tester confirms the original steps now pass. Who moves the defect to Verified/Closed?

- [ ] A) The developer who made the fix
- [ ] B) The dev lead
- [ ] C) The product owner
- [ ] D) The tester

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The tester

**Explanation:** Developers fix; testers verify. Only the tester (or the reporter) closes a fixed defect, so that a separate pair of eyes confirms the fix.

- **Why others are wrong:**
  - A) The developer moves a defect to Fixed and Ready for Retest, not to Verified/Closed.
  - B) The dev lead triages, assigns and detects duplicates; closing a fix is not their role.
  - C) The product owner decides business matters such as Won't Fix and Deferred, not verification.

- **Source:** defect-lifecycle.md, "5. Transition table: from, to, who, when"
</details>

---

### Question 14

The company name is misspelled on the home page on the day of a major marketing launch. Nothing stops working. How is this defect best classified?

- [ ] A) Low severity, high priority
- [ ] B) High severity, low priority
- [ ] C) High severity, high priority
- [ ] D) Low severity, low priority

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Low severity, high priority

**Explanation:** Nothing breaks, so severity (damage) is low; but the flaw is highly visible and embarrassing on launch day, so priority (order of repair) is high.

- **Why others are wrong:**
  - B) High severity would mean a major function is broken or the system crashes, which is not the case.
  - C) High severity is wrong because there is no functional damage.
  - D) Low priority is wrong because the launch day makes the fix urgent.

- **Source:** defect-lifecycle.md, "10. Severity versus priority" (Examples for each quadrant)
</details>

---

### Question 15

Who should decide that a valid defect will be deferred to a later release?

- [ ] A) The developer alone
- [ ] B) The tester who reported it
- [ ] C) The triage group, product owner or release manager
- [ ] D) Nobody; it happens automatically after 30 days

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The triage group, product owner or release manager

**Explanation:** Deferred is moved by the triage group, the product owner or the release manager. A developer alone should not defer a defect, and a recorded reason is required.

- **Why others are wrong:**
  - A) The lesson says a developer alone should not defer a defect.
  - B) The reporter provides information and evidence; deferral is a business and scheduling decision.
  - D) The lesson describes no automatic deferral; deferred defects must be reviewed regularly instead.

- **Source:** defect-lifecycle.md, "3. The complete defect lifecycle" (Deferred)
</details>

---

### Question 16

The checkout module has 6 KLOC and testing found 18 defects in it. What is its defect density?

- [ ] A) 0.33 defects per KLOC
- [ ] B) 3.0 defects per KLOC
- [ ] C) 12 defects per KLOC
- [ ] D) 24 defects per KLOC

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 3.0 defects per KLOC

**Explanation:** Defect density = number of defects / size = 18 / 6 = 3.0 defects per KLOC.

- **Why others are wrong:**
  - A) 0.33 comes from dividing the size by the defects (6 / 18), which inverts the formula.
  - C) 12 comes from subtracting (18 - 6), which is not the formula.
  - D) 24 comes from adding (18 + 6), which is not the formula.

- **Source:** defect-lifecycle.md, "12. Defect metrics: what the numbers tell us" (Defect density and Worked example)
</details>

---

### Question 17

A tester retests a defect in the Ready for Retest state and the original steps still fail. Which state does the tester move it to?

- [ ] A) Reopened
- [ ] B) Verified/Closed
- [ ] C) Deferred
- [ ] D) Won't Fix

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Reopened

**Explanation:** A failed retest moves the defect from Ready for Retest to Reopened, with a comment and evidence including the build number.

- **Why others are wrong:**
  - B) Verified/Closed is only for when the original steps pass and a regression check is clean.
  - C) Deferred means valid but fixed in a later release, decided by triage or the product owner.
  - D) Won't Fix is a business decision never to fix, made by the product owner or triage group.

- **Source:** defect-lifecycle.md, "5. Transition table: from, to, who, when" and "3. The complete defect lifecycle" (Reopened)
</details>

---

### Question 18

A developer follows the reporter's steps exactly, on the stated build and environment, and the problem does not occur. Which state describes this outcome?

- [ ] A) Rejected
- [ ] B) Duplicate
- [ ] C) Won't Fix
- [ ] D) Cannot Reproduce

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Cannot Reproduce

**Explanation:** Cannot Reproduce is used when honest attempts on the stated build and environment fail to recreate the problem. The reporter can add a video, logs or exact data to reopen it.

- **Why others are wrong:**
  - A) Rejected means the report describes behavior that is actually correct, a misunderstanding, or out of scope.
  - B) Duplicate means the same problem is already logged.
  - C) Won't Fix means the defect is valid but the organization decided never to fix it.

- **Source:** defect-lifecycle.md, "3. The complete defect lifecycle" (Not a Bug / Cannot Reproduce)
</details>

---

### Question 19

Which Jira issue type can never exist on its own and always requires a parent issue?

- [ ] A) Epic
- [ ] B) Task
- [ ] C) Sub-task
- [ ] D) Bug

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Sub-task

**Explanation:** A Sub-task is a smaller piece of work that belongs to a parent Story, Task or Bug, and its parent is required.

- **Why others are wrong:**
  - A) An Epic is the top of the default hierarchy and has no parent (or a higher level on some plans).
  - B) A Task can optionally sit under an Epic but does not require a parent.
  - D) A Bug can optionally sit under an Epic but does not require a parent.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "3. Each Issue Type in Depth" (3.5 Sub-task and Summary Table of Issue Types)
</details>

---

### Question 20

Which statement about Severity in Jira is correct?

- [ ] A) Severity is a default field that Jira provides with Critical, Major, Minor and Trivial values
- [ ] B) Severity is not a default field; teams usually add it as a custom field
- [ ] C) Severity and Priority are the same field with two names
- [ ] D) Jira sets Severity automatically from the number of affected users

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Severity is not a default field; teams usually add it as a custom field

**Explanation:** Priority is a default field. Severity is usually a custom field added by an administrator, often a dropdown, because it is not provided by default.

- **Why others are wrong:**
  - A) Severity is not a default field; Priority is.
  - C) They are different: severity is technical impact and priority is business urgency.
  - D) The lesson describes no automatic calculation of severity.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "11. Priority, Severity, Labels and Components" (11.1 Priority vs Severity)
</details>

---

### Question 21

The issue "Set up test environment" must be finished before "Test registration" can proceed. Which link type fits best?

- [ ] A) Relates to
- [ ] B) Duplicates
- [ ] C) Blocks
- [ ] D) Clones

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Blocks

**Explanation:** Blocks / is blocked by means one issue must be finished before the other can proceed, which is exactly this dependency.

- **Why others are wrong:**
  - A) Relates to is a general association without a dependency.
  - B) Duplicates means two issues describe the same problem.
  - D) Clones means one issue was created as a copy of another.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "9. Linking Issues"
</details>

---

### Question 22

What does this JQL return?

`project = QEF AND issuetype = Bug AND created >= -7d`

- [ ] A) Bugs in QEF that are due within 7 days
- [ ] B) Bugs in QEF that were created more than 7 days ago
- [ ] C) Stories and bugs in QEF created in the last 7 days
- [ ] D) Bugs in QEF that were created in the last 7 days

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Bugs in QEF that were created in the last 7 days

**Explanation:** The clause created >= -7d means created from seven days ago until now, and issuetype = Bug limits the result to bugs.

- **Why others are wrong:**
  - A) The query uses created, not the due date field.
  - B) >= -7d selects the recent period, the opposite of older than 7 days.
  - C) issuetype = Bug excludes stories.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "15. JQL Queries for Issues, Stories and Bugs" (Query 5)
</details>

---

### Question 23

Which of these values is best recorded as a component rather than a label?

- [ ] A) Registration
- [ ] B) regression
- [ ] C) smoke
- [ ] D) needs-ux

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Registration

**Explanation:** Components are formal, predefined parts of the product such as Registration, Login or Dashboard. Labels are flexible cross-cutting tags.

- **Why others are wrong:**
  - B) regression is a cross-cutting flag, which suits a label.
  - C) smoke is a cross-cutting theme, which suits a label.
  - D) needs-ux is a cross-cutting flag, which suits a label.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "11. Priority, Severity, Labels and Components" (11.2 Labels vs Components)
</details>

---

### Question 24

A status exists in the workflow but is not mapped to any board column. What happens to issues in that status?

- [ ] A) They are shown in the leftmost column
- [ ] B) They do not appear on the board
- [ ] C) Jira blocks any transition into that status
- [ ] D) They are shown in the Done column

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) They do not appear on the board

**Explanation:** A status not mapped to any column is unmapped, so its issues become invisible on the board, though they still exist in the project and in searches.

- **Why others are wrong:**
  - A) There is no automatic placement in the leftmost column.
  - C) Jira does not block transitions because of missing mapping; the board simply hides the cards.
  - D) Unmapped statuses are not shown in any column, including Done.

- **Source:** jira-boards-and-workflows.md, "1.4 Board configuration" (Columns and status mapping)
</details>

---

### Question 25

In Kanban flow metrics, what does cycle time measure?

- [ ] A) The time from when an issue is created until it is done
- [ ] B) The time an issue spends in the backlog
- [ ] C) The time an issue spends in the testing column only
- [ ] D) The time from when work begins (In Progress) until the issue is done

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The time from when work begins (In Progress) until the issue is done

**Explanation:** Cycle time is the team's view of effort: from the moment work begins until done. Lead time covers creation to done, including waiting.

- **Why others are wrong:**
  - A) That is lead time, the customer's view of waiting.
  - B) Backlog waiting is part of lead time, not cycle time.
  - C) Cycle time covers the whole active period, not one column.

- **Source:** jira-boards-and-workflows.md, "1.7 Kanban flow metrics, explained simply"
</details>

---

### Question 26

A team wants Jira to show an error and block the transition to Closed when no resolution has been set. Which transition feature does this?

- [ ] A) Condition
- [ ] B) Post function
- [ ] C) Validator
- [ ] D) Screen

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Validator

**Explanation:** A validator checks the data when the user tries the transition, and blocks it with an error message if the check fails, such as "Resolution must be set".

- **Why others are wrong:**
  - A) A condition decides whether the transition button is available to the user at all.
  - B) A post function runs automatically after the transition succeeds.
  - D) A screen is a form that asks the user for specific information when the transition is used.

- **Source:** jira-boards-and-workflows.md, "2.5 Transition features: conditions, validators, post functions and screens"
</details>

---

### Question 27

In the lesson's Bug workflow, which status category does the Ready for Retest status belong to?

- [ ] A) In Progress
- [ ] B) To Do
- [ ] C) Done
- [ ] D) None, because it is a custom status

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) In Progress

**Explanation:** Ready for Retest is in the In Progress category: the fix is deployed and a tester still has to verify it.

- **Why others are wrong:**
  - B) To Do holds Open, Reopened and Deferred.
  - C) Done holds Closed, Rejected and Duplicate.
  - D) Every status belongs to exactly one of the three categories, custom or not.

- **Source:** jira-boards-and-workflows.md, "2.3 Designing a Bug workflow for QE"
</details>

---

### Question 28

On a Kanban board, the In Testing column has a WIP limit of 2 and now holds 4 cards. What happens?

- [ ] A) Jira refuses to accept the extra cards
- [ ] B) The column turns red as a warning, but cards can still be dragged in
- [ ] C) Jira moves the oldest cards back to In Progress automatically
- [ ] D) The sprint is ended automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The column turns red as a warning, but cards can still be dragged in

**Explanation:** WIP limits are guidance. The column header turns red when the maximum is exceeded so the team can discuss it, but dragging is not blocked.

- **Why others are wrong:**
  - A) WIP limits do not stop you from dragging a card in.
  - C) Jira does not move cards automatically because of a WIP limit.
  - D) WIP limits are a Kanban concept and have no effect on sprints.

- **Source:** jira-boards-and-workflows.md, "1.4 Board configuration" (WIP limits and column constraints (Kanban))
</details>

---

## Part 2: True/False

Decide whether each statement is true or false. Many of these target common misconceptions.

---

### Question 29

**True or False:** Once a developer has fixed a defect, the developer should move it to Verified/Closed.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Developers fix; testers verify. Only the tester (or reporter) closes a fixed defect after retesting, so that a separate pair of eyes confirms the fix. The developer moves it to Fixed or Ready for Retest.

- **Source:** defect-lifecycle.md, "5. Transition table: from, to, who, when"
</details>

---

### Question 30

**True or False:** Severity and priority are two names for the same measure of how urgent a defect is.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Severity is how serious the technical impact is (damage); priority is how soon it should be fixed (order of repair), usually set by the product owner or triage.

- **Source:** defect-lifecycle.md, "10. Severity versus priority"
</details>

---

### Question 31

**True or False:** A test marked Blocked has not been executed, so it is not counted in the executed total used for execution percentage.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Executed usually means tests that reached Pass or Fail. Blocked, Skipped and Not Run tests have not been executed.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality" (19.1 Test execution percentage)
</details>

---

### Question 32

**True or False:** Acceptance criteria and test cases are the same thing, so once you have one you do not need the other.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Acceptance criteria define what "done" means from the business view. Test cases are the detailed steps and data used to check them, designed later. Good criteria give a strong starting point for test cases.

- **Source:** requirements-analysis.md, "8. Acceptance Criteria and Testability Analysis" (8.1 What are acceptance criteria?)
</details>

---

### Question 33

**True or False:** Defect Detection Percentage (DDP) equals 100% minus defect leakage %.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Leakage and DDP are two views of the same fact: DDP = defects found during testing / (found during testing + found after release) x 100.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality" (19.5 Defect Detection Percentage)
</details>

---

### Question 34

**True or False:** A test plan is a long-lived, organization-level document that rarely changes from project to project.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** That describes a test strategy. A test plan is project, release or feature specific and changes with the project.

- **Source:** test-planning-and-test-execution.md, "2. Test strategy versus test plan"
</details>

---

### Question 35

**True or False:** In Jira, Priority is a default field, while Severity is usually a custom field that an administrator adds.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Priority comes with levels such as Highest to Lowest. Severity is not a default field, so teams who want it add a custom field.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "11. Priority, Severity, Labels and Components" (11.1 Priority vs Severity)
</details>

---

### Question 36

**True or False:** When a defect is a Duplicate, it is linked to the original defect, which becomes the single master defect.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The duplicate is linked to the original and later closed; when the original is fixed, duplicates are rechecked and closed.

- **Source:** defect-lifecycle.md, "3. The complete defect lifecycle" (Duplicate)
</details>

---

### Question 37

**True or False:** Rank and priority are the same thing: the issue with the highest priority is always at the top of the backlog.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Priority is a field describing urgency; rank is the actual order in which the team will work. Two High priority issues still have one that is first, and if they disagree you ask the Product Owner.

- **Source:** jira-boards-and-workflows.md, "1.5 Backlog management and ranking"
</details>

---

### Question 38

**True or False:** A burnup chart makes added scope visible because it shows total scope as a separate line.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A burnup chart has two lines, total scope and completed work. The scope line rises when work is added, making scope creep easy to see.

- **Source:** jira-boards-and-workflows.md, "1.8 Reports and dashboards" (Burndown vs burnup)
</details>

---

### Question 39

**True or False:** A story point is a measure of how many hours a story will take.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A story point is a relative measure of size combining effort, complexity and uncertainty, not hours. A team's velocity (points per sprint) is used for forecasting.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "12. Estimation and Story Points"
</details>

---

### Question 40

**True or False:** The priority of a requirement is decided by the business, typically the product owner, not by the tester.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The tester's role is to ask what priority each requirement has and to point out when everything is marked Must, which defeats the purpose.

- **Source:** requirements-analysis.md, "10. Requirement Prioritization with MoSCoW"
</details>

---

### Question 41

**True or False:** Retesting re-runs the exact test that failed, while regression testing re-runs other, previously passing tests to check that a change broke nothing else.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Retesting (confirmation testing) asks whether the specific defect is gone; regression testing asks whether the fix damaged anything that used to work.

- **Source:** test-planning-and-test-execution.md, "16. Retesting versus regression testing (brief introduction)"
</details>

---

## Part 3: Fill-in-the-Blank

Write the missing word or phrase. Accepted answers are given in the solution.

---

### Question 42

In risk-based prioritization, the risk score is calculated as ______ x ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Likelihood x Impact (the two blanks may be given in either order)

**Explanation:** The lesson rates each from 1 to 3, so a score of 9 is Critical and scores of 6 to 9 get the earliest and deepest testing.

- **Source:** test-planning-and-test-execution.md, "4. Risk-based prioritization: where should we spend limited time?"
</details>

---

### Question 43

A table that links each requirement to its test conditions, test cases and later defects is called a Requirement ______ Matrix.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Traceability (accepted: Requirements Traceability Matrix, RTM)

**Explanation:** The RTM supports coverage checks, impact analysis, progress reporting, audit and defect linking.

- **Source:** requirements-analysis.md, "12. The Requirement Traceability Matrix (RTM)"
</details>

---

### Question 44

Pass % is calculated as the number of tests passed divided by the number of tests ______, multiplied by 100.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** executed (accepted: run, executed tests; the lesson notes some teams divide by total planned tests instead and say to state your definition)

**Explanation:** Pass % = (tests passed / tests executed) x 100, where executed means tests that reached Pass or Fail.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality" (19.2 Pass percentage)
</details>

---

### Question 45

The defect state in which a fix is available in a test environment and is waiting for a tester to confirm it is called ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Ready for Retest (accepted: Retest, Pending Retest)

**Explanation:** The developer or the build process moves a defect to this state once the fix is deployed and the build number is recorded.

- **Source:** defect-lifecycle.md, "3. The complete defect lifecycle" (Ready for Retest)
</details>

---

### Question 46

A short way to remember the difference: severity is about damage, while priority is about ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** order (accepted: the order of repair, how soon it should be fixed, urgency)

**Explanation:** Severity describes technical impact; priority is the business and scheduling decision about which defect is treated first.

- **Source:** defect-lifecycle.md, "10. Severity versus priority"
</details>

---

### Question 47

In the Given/When/Then format, the ______ part describes the starting context of the scenario.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Given (accepted: Given)

**Explanation:** Given is the starting situation or precondition, When is the action, and Then is the observable result.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "7. Writing a Great Story with Acceptance Criteria" (7.2 Acceptance Criteria in Given/When/Then)
</details>

---

### Question 48

The JQL function that means "whoever is currently logged in" is ______().

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** currentUser (accepted: currentUser())

**Explanation:** For example, reporter = currentUser() lets the same filter work for everyone who runs it.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "15. JQL Queries for Issues, Stories and Bugs" (Query 3)
</details>

---

### Question 49

On a Kanban board, ______ time runs from when an issue is created until it is done, while ______ time runs from when work starts until it is done.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** First blank: lead. Second blank: cycle.

**Explanation:** Using the pizza shop analogy, lead time is from order to arrival and cycle time is from the cook starting to the pizza leaving the oven.

- **Source:** jira-boards-and-workflows.md, "1.7 Kanban flow metrics, explained simply"
</details>

---

## Part 4: Code/Output Prediction

Work out the result by hand, then check the solution. All snippets are deterministic.

---

### Question 50

What does this Python snippet print? It applies the execution and pass percentage formulas from the lesson.

```python
results = {
    "TC-01": "Pass", "TC-02": "Pass", "TC-03": "Fail", "TC-04": "Blocked",
    "TC-05": "Pass", "TC-06": "Skipped", "TC-07": "Not Run", "TC-08": "Pass",
    "TC-09": "Fail", "TC-10": "Pass",
}
planned = len(results)
executed = sum(1 for s in results.values() if s in ("Pass", "Fail"))
passed = sum(1 for s in results.values() if s == "Pass")
print(f"Executed: {executed}")
print(f"Execution %: {executed / planned * 100:.0f}")
print(f"Pass %: {passed / executed * 100:.1f}")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
Executed: 7
Execution %: 70
Pass %: 71.4
```

**Explanation:** Planned is 10. Executed counts only Pass and Fail: 5 passes plus 2 fails = 7. Execution % = 7/10 x 100 = 70. Pass % = 5/7 x 100 = 71.4. Blocked, Skipped and Not Run are not executed.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality"
</details>

---

### Question 51

What does this snippet print? It uses the defect density, leakage and DDP formulas.

```python
found_in_testing = 36
found_after_release = 9
size_kloc = 12
total = found_in_testing + found_after_release
density = found_in_testing / size_kloc
leakage = found_after_release / total * 100
ddp = found_in_testing / total * 100
print(f"{density:.1f} {leakage:.1f} {ddp:.1f}")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
3.0 20.0 80.0
```

**Explanation:** Density = 36 / 12 = 3.0 defects per KLOC. Total = 45. Leakage = 9 / 45 x 100 = 20.0. DDP = 36 / 45 x 100 = 80.0, which equals 100 minus leakage.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality" and defect-lifecycle.md, "12. Defect metrics: what the numbers tell us"
</details>

---

### Question 52

Using the issue table below, which issue keys does this JQL query return? Remember that Ready for Retest is in the In Progress status category and Closed is in the Done category.

`project = QEF AND issuetype = Bug AND priority in (Highest, High) AND assignee IS EMPTY AND statusCategory != Done`

| Key | Type | Priority | Status | Status category | Assignee |
|---|---|---|---|---|---|
| QEF-1 | Bug | Highest | Open | To Do | (empty) |
| QEF-2 | Bug | High | In Progress | In Progress | Ana |
| QEF-3 | Story | High | To Do | To Do | (empty) |
| QEF-4 | Bug | Low | Open | To Do | (empty) |
| QEF-5 | Bug | High | Closed | Done | (empty) |
| QEF-6 | Bug | Medium | Open | To Do | Ben |
| QEF-7 | Bug | Highest | Ready for Retest | In Progress | (empty) |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** QEF-1 and QEF-7

**Explanation:** QEF-2 has an assignee; QEF-3 is a Story; QEF-4 is Low priority; QEF-5 is in the Done category; QEF-6 is Medium and assigned. QEF-1 and QEF-7 are unassigned Highest-priority bugs not in the Done category.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "15. JQL Queries for Issues, Stories and Bugs" (Queries 2 and 4) and jira-boards-and-workflows.md, "2.3 Designing a Bug workflow for QE"
</details>

---

### Question 53

This snippet follows the Bug workflow from the lesson. What is the last line it prints, and which status category is that final status in?

```python
transitions = {
    ("Open", "Start progress"): "In Progress",
    ("In Progress", "Ready for retest"): "Ready for Retest",
    ("Ready for Retest", "Verify and close"): "Closed",
    ("Ready for Retest", "Retest failed"): "Reopened",
    ("Closed", "Reopen"): "Reopened",
    ("Reopened", "Start progress"): "In Progress",
}
status = "Open"
for step in ["Start progress", "Ready for retest", "Retest failed",
             "Start progress", "Ready for retest", "Verify and close", "Reopen"]:
    status = transitions[(status, step)]
    print(step, "->", status)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Last line: `Reopen -> Reopened`. The category of Reopened is To Do.

**Explanation:** The bug goes Open, In Progress, Ready for Retest, Reopened (retest failed), In Progress, Ready for Retest, Closed (verified), and then Reopened when it is found again. In the lesson's Bug workflow, Reopened is in the To Do category.

- **Source:** jira-boards-and-workflows.md, "2.3 Designing a Bug workflow for QE"
</details>

---

### Question 54

What does this snippet print? It computes requirement coverage from an RTM.

```python
rtm = {
    "REQ-01": ["TC-1", "TC-2"],
    "REQ-02": ["TC-3"],
    "REQ-03": [],
    "REQ-04": ["TC-4"],
    "REQ-05": [],
    "REQ-06": ["TC-5", "TC-6"],
    "REQ-07": ["TC-7"],
    "REQ-08": ["TC-8"],
}
covered = [r for r, tcs in rtm.items() if tcs]
gaps = [r for r, tcs in rtm.items() if not tcs]
print(f"Coverage: {len(covered) / len(rtm) * 100:.1f}%")
print("Gaps:", gaps)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
Coverage: 75.0%
Gaps: ['REQ-03', 'REQ-05']
```

**Explanation:** Six of the eight requirements have at least one test, so coverage is 6/8 = 75.0%. REQ-03 and REQ-05 have no tests, which is exactly the kind of coverage gap an RTM is used to spot.

- **Source:** requirements-analysis.md, "12. The Requirement Traceability Matrix (RTM)" (12.2 What it is used for)
</details>

---

### Question 55

What does this snippet print? It ranks feature areas by risk score (Likelihood x Impact), highest first. Equal scores keep their original order.

```python
areas = [("Lockout", 3, 3), ("Password rules", 3, 2), ("Logout", 1, 2),
         ("Email wording", 1, 1), ("Duplicate email", 2, 3)]
ranked = sorted(areas, key=lambda a: a[1] * a[2], reverse=True)
for name, likelihood, impact in ranked:
    print(name, likelihood * impact)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
Lockout 9
Password rules 6
Duplicate email 6
Logout 2
Email wording 1
```

**Explanation:** Scores: Lockout 9 (Critical), Password rules 6 (High), Logout 2 (Low), Email wording 1 (Low), Duplicate email 6 (High). Sorting highest first, with Python's stable sort keeping Password rules before Duplicate email, gives the output shown. The 6-to-9 areas get the earliest and deepest testing.

- **Source:** test-planning-and-test-execution.md, "4. Risk-based prioritization: where should we spend limited time?"
</details>

---

## Part 5: Matching/Scenario

Match each item in the left column with the best description in the right column. Each letter is used once.

---

### Question 56

**Match each defect state to its meaning.**

| # | State | | Letter | Meaning |
|---|---|---|---|---|
| 1 | New | | A | Valid defect that will be fixed in a later release, not the current one |
| 2 | Assigned | | B | Describes the same problem as one already logged; linked to the original |
| 3 | Reopened | | C | Just logged; nobody has reviewed it yet |
| 4 | Deferred | | D | Valid, but the organization decided it will never be fixed, with a business reason recorded |
| 5 | Won't Fix | | E | Judged not valid (correct behavior, misunderstanding or out of scope); no fix will be made |
| 6 | Duplicate | | F | Thought to be fixed or closed but shown to still exist or to have returned |
| 7 | Rejected | | G | Reviewed, accepted as valid and given to a specific developer or team |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-G, 3-F, 4-A, 5-D, 6-B, 7-E

**Explanation:** Each pairing comes straight from the state definitions in the lifecycle: New is just logged, Assigned has an owner, Reopened means the fix failed or the defect returned, Deferred means later release, Won't Fix means never, Duplicate links to a master defect, and Rejected means not valid.

- **Source:** defect-lifecycle.md, "3. The complete defect lifecycle"
</details>

---

### Question 57

**Match each severity/priority combination to the best example.**

| # | Combination | | Letter | Example |
|---|---|---|---|---|
| 1 | High severity, high priority | | A | A typo in the "Pay Now" button label on the main checkout page |
| 2 | High severity, low priority | | B | A crash when uploading a 2 GB photo that the UI already limits to 5 MB |
| 3 | Low severity, high priority | | C | Customers cannot log in at all after the latest release |
| 4 | Low severity, low priority | | D | A button 2 pixels out of alignment on a rarely visited settings page |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-B, 3-A, 4-D

**Explanation:** A complete login failure is damaging and urgent. The 2 GB upload crash is serious but nearly unreachable. The typo is harmless to function but highly visible and quick to fix. The 2-pixel misalignment is tiny and harmless.

- **Source:** defect-lifecycle.md, "10. Severity versus priority" (Examples for each quadrant)
</details>

---

### Question 58

**Match each Jira issue type to its use.**

| # | Issue type | | Letter | Use and example |
|---|---|---|---|---|
| 1 | Epic | | A | A step within a parent issue, such as "Write API tests for registration" |
| 2 | Story | | B | A time-boxed investigation, such as "Evaluate email verification options" |
| 3 | Task | | C | User-facing value that fits in a sprint, such as "User can register with email" |
| 4 | Bug | | D | Non-feature work, such as "Prepare test data for registration" |
| 5 | Sub-task | | E | A big goal or feature area, such as "User Account Management" |
| 6 | Spike | | F | A defect, such as "Registration accepts invalid email" |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-C, 3-D, 4-F, 5-A, 6-B

**Explanation:** The pairings follow the summary table of issue types: Epic is a large goal, Story is user value, Task is non-feature work, Bug is a defect, Sub-task is a step inside a parent, and Spike is a time-boxed investigation.

- **Source:** jira-issues-stories-tasks-and-bugs.md, "3. Each Issue Type in Depth" (Summary Table of Issue Types)
</details>

---

### Question 59

**Match each metric to its formula.**

| # | Metric | | Letter | Formula |
|---|---|---|---|---|
| 1 | Execution % | | A | Defects found during testing / (found during testing + found after release) x 100 |
| 2 | Pass % | | B | Tests executed / total planned tests x 100 |
| 3 | Defect density | | C | Defects found after release / (found during testing + found after release) x 100 |
| 4 | Defect leakage % | | D | Number of defects / size of the software (for example KLOC) |
| 5 | DDP | | E | Tests passed / tests executed x 100 |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-E, 3-D, 4-C, 5-A

**Explanation:** Execution % measures progress against the plan, Pass % measures results among executed tests, density relates defects to size, leakage counts defects that escaped to after release, and DDP counts the share caught during testing.

- **Source:** test-planning-and-test-execution.md, "19. Test metrics: measuring progress and quality"
</details>

---

### Question 60

**Match each requirement characteristic to its typical warning sign.**

| # | Characteristic | | Letter | Warning sign |
|---|---|---|---|---|
| 1 | Unambiguous | | A | Words such as "fast", "easy", "robust" and "user-friendly" |
| 2 | Complete | | B | Words such as "always", "never" and "100 percent" |
| 3 | Testable | | C | No numbering and an unknown origin |
| 4 | Feasible | | D | Everything is marked "high" or nothing is ranked |
| 5 | Traceable | | E | Words such as "appropriate", "as needed", "etc." and "and/or" |
| 6 | Prioritized | | F | No error handling, "TBD" or missing numbers |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-F, 3-A, 4-B, 5-C, 6-D

**Explanation:** These come from the summary table of the eight characteristics, which pairs each characteristic with the question to ask and its warning signs.

- **Source:** requirements-analysis.md, "4. Characteristics of a Good Requirement" (4.9 Summary table)
</details>

---

### Question 61

**Match each Jira workflow feature to what it does.**

| # | Feature | | Letter | What it does |
|---|---|---|---|---|
| 1 | Condition | | A | A pop-up form that asks the user for a comment and a fix build number |
| 2 | Validator | | B | Hides the "Verify and close" button from users who are not in the QA group |
| 3 | Post function | | C | Records how an issue ended, such as Fixed, Duplicate or Won't Do |
| 4 | Screen | | D | Blocks the transition with an error if the resolution is not set |
| 5 | Resolution | | E | Automatically clears the resolution after the transition to Reopened |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-D, 3-E, 4-A, 5-C

**Explanation:** A condition decides whether a transition is available; a validator checks data when the transition is tried; a post function runs after success; a screen collects information; a resolution records why work finished.

- **Source:** jira-boards-and-workflows.md, "2.5 Transition features: conditions, validators, post functions and screens" and "2.6 Resolutions"
</details>

---

## Part 6: Scenario Questions (Project 1: Registration and Login)

Apply what you learned to the Project 1 User Registration and Login feature.

---

### Question 62

While executing the Project 1 test case for REQ-03, you register with a 6-character password and the system accepts it, although the minimum is 8. The test fails. What is the best sequence of actions?

- [ ] A) Log a defect straight away titled "Registration broken" and move on to the next test
- [ ] B) Mark the test Blocked and wait for a developer to confirm the problem
- [ ] C) Mark the test Passed because registration still works, and mention the password in a comment
- [ ] D) Re-try once, search the tracker for a duplicate, then log a defect with steps, expected versus actual result, environment, build and evidence, and link it to the failing test case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Re-try once, search the tracker for a duplicate, then log a defect with steps, expected versus actual result, environment, build and evidence, and link it to the failing test case

**Explanation:** When a test fails you re-try once to rule out a mistake, check for known issues, log a defect with a clear title and evidence, and link the defect ID to the test case so everyone sees the connection.

- **Why others are wrong:**
  - A) A vague title and no steps or evidence make the defect hard to reproduce, and a duplicate search was skipped.
  - B) Blocked means the test could not be executed; this test ran and the behavior was wrong, which is a Fail.
  - C) The actual result differs from the expected result, so the status is Fail; marking it Pass would distort the metrics.

- **Source:** test-planning-and-test-execution.md, "15. Logging defects when actual differs from expected"
</details>

---

### Question 63

After the latest release, no customer can log in to Project 1. How should this defect be classified?

- [ ] A) Low severity, high priority
- [ ] B) High severity, high priority
- [ ] C) High severity, low priority
- [ ] D) Low severity, low priority

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) High severity, high priority

**Explanation:** A core function is completely unusable with no workaround, so the severity is high, and every customer is affected, so it must be fixed now. This is the fix-now quadrant.

- **Why others are wrong:**
  - A) Low severity would mean cosmetic damage; here a core function is down.
  - C) Low priority would suit a serious defect that is rare or off the main path, which is not the case.
  - D) Both low is for tiny, harmless flaws such as a 2-pixel misalignment.

- **Source:** defect-lifecycle.md, "10. Severity versus priority" and jira-issues-stories-tasks-and-bugs.md, "11. Priority, Severity, Labels and Components" (11.1 Priority vs Severity)
</details>

---

### Question 64

Your Project 1 smoke test on build 1.0.2 fails because the Login page does not load. What should you do?

- [ ] A) Stop deeper testing, record the failure with evidence, inform the developer and test lead, and mark the build as rejected
- [ ] B) Continue running the full suite and report all failures at the end of the day
- [ ] C) Mark the remaining test cases Passed so the schedule is not delayed
- [ ] D) Skip the smoke test next time to save time

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Stop deeper testing, record the failure with evidence, inform the developer and test lead, and mark the build as rejected

**Explanation:** A failed smoke test means the build is not stable enough for deeper testing, so you stop, report and wait for a new build (per suspension and resumption criteria).

- **Why others are wrong:**
  - B) Running the full suite on an untestable build wastes everyone's time.
  - C) Never mark tests as passed without running them.
  - D) The smoke test is exactly what protects the team from testing unready builds.

- **Source:** test-planning-and-test-execution.md, "10. Smoke and sanity checks (introduction)" and Knowledge Check question 19
</details>

---

### Question 65

In Project 1, the lockout test for REQ-08 (lock the account for 15 minutes after 5 failed attempts) cannot run today because the lockout setting in the QA environment is unavailable. What is the best handling?

- [ ] A) Mark it Fail, because the lockout did not happen
- [ ] B) Mark it Skipped, because it was deliberately left out
- [ ] C) Mark it Blocked with the reason recorded, escalate the same day to the test lead, and run unblocked tests first
- [ ] D) Leave it Not Run and say nothing until the next cycle

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Mark it Blocked with the reason recorded, escalate the same day to the test lead, and run unblocked tests first

**Explanation:** Blocked means something outside the test prevents it. Record the reason and ticket, escalate the blocker the same day, and reorder work so you stay productive.

- **Why others are wrong:**
  - A) The behavior was never checked, so it cannot be a Fail.
  - B) Skipped is a deliberate decision with a reason such as descoping, not an environment problem.
  - D) Not waiting quietly is the lesson's advice: blockers must be escalated and reflected in the status report.

- **Source:** test-planning-and-test-execution.md, "13. Recording results: the five statuses" and "21. Handling blocked tests and schedule slippage"
</details>

---

### Question 66

The product owner changes the Project 1 password rule (REQ-PW-01) from at least 8 characters to at least 10. What should the tester do first?

- [ ] A) Update only the requirement document and wait until execution to see what fails
- [ ] B) Change one test case by memory and leave the others untouched
- [ ] C) Ask the developers to find the affected tests, since testers do not use the RTM
- [ ] D) Use the RTM to find the linked conditions and test cases, update them and the test data and scripts, and add a regression check for existing users

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Use the RTM to find the linked conditions and test cases, update them and the test data and scripts, and add a regression check for existing users

**Explanation:** The RTM supports impact analysis: it shows which test conditions and cases are linked to the changed requirement, so they, the test data and any automated scripts can be updated, and existing users' old passwords can be checked.

- **Why others are wrong:**
  - A) Waiting means tests are written against the wrong version and problems are found late.
  - B) The same rule may also appear in other requirements such as REQ-REG-01, so a single change by memory misses linked items.
  - C) The tester takes part in impact analysis using the RTM to answer what is affected.

- **Source:** requirements-analysis.md, "13. Requirements Change Management and Its Impact on Testing" (Example)
</details>

---

### Question 67

A developer fixes the bug "Registration accepts invalid email" and moves it to Ready for Retest in Jira. What happens next in the lesson's Bug workflow?

- [ ] A) The developer moves it to Closed after merging the code
- [ ] B) The tester retests the exact steps on the build with the fix and checks nearby features; if it passes the bug is closed with resolution Fixed, and if it fails it goes to Reopened with a comment and evidence
- [ ] C) The product owner closes the bug, because only the business can accept a fix
- [ ] D) Jira closes the bug automatically once the build is deployed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The tester retests the exact steps on the build with the fix and checks nearby features; if it passes the bug is closed with resolution Fixed, and if it fails it goes to Reopened with a comment and evidence

**Explanation:** The tester performs the retest plus a regression check around the fix. Verify and close requires resolution Fixed; Retest failed leads to Reopened and requires a comment with evidence.

- **Why others are wrong:**
  - A) Only the tester (or the reporter) closes a fixed defect; developers fix and mark it ready for retest.
  - C) The product owner decides business matters such as Won't Fix and Deferred, not verification of fixes.
  - D) Automation can assign the bug back to the reporter, but the verification and the closing are done by the tester.

- **Source:** jira-boards-and-workflows.md, "2.3 Designing a Bug workflow for QE" (transition table) and defect-lifecycle.md, "15. Retesting and regression checks after a fix"
</details>
