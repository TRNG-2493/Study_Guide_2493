# Software Testing Life Cycle (STLC)

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define the Software Testing Life Cycle (STLC) and explain how it differs from, and relates to, the Software Development Life Cycle (SDLC).
2. Name and describe the six classic STLC phases: Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution, and Test Cycle Closure.
3. Explain, for each phase, its purpose, main activities, entry criteria, exit criteria, deliverables, roles, typical tools, and common pitfalls.
4. Define entry criteria, exit criteria, deliverables, suspension criteria, and resumption criteria in plain language.
5. Read and explain basic test metrics such as pass percentage, defect density, and requirement coverage.
6. Describe how the STLC is compressed and repeated inside Agile sprints.
7. Follow a single feature ("user login") through all six phases and recognize the sample artifacts produced at each step.
8. Describe, at a high level, where AI-assisted tools can help in the STLC and the cautions that go with them.
9. Draft entry and exit criteria for each STLC phase for your own "Project 1 - QE Foundations" application.

---

## Why This Matters

### In the industry

Software teams do not test "when there is time." Professional teams test **on purpose, in an organized way, and with evidence**. When a bank releases a new mobile app, when an online store changes its checkout, or when a hospital updates its scheduling system, someone has to be able to answer questions like:

- What exactly did we test?
- What did we skip, and why?
- How do we know we were done?
- Who decided it was safe to release?

The Software Testing Life Cycle is the structure that lets a team answer those questions with facts instead of opinions. Managers use it to plan time and people. Developers use it to know what will be checked and when. Auditors and customers use its artifacts as proof that quality work happened. Without it, testing becomes a last-minute scramble where bugs are found by customers instead of by the team.

Job descriptions for QA Engineers, SDETs, and Test Automation Engineers routinely include phrases such as "participate in test planning," "write and maintain test cases," "report on test results," and "work within the STLC." In interviews you will very likely be asked, "Walk me through the phases of the STLC." After this lesson you will be able to answer with confidence and with examples.

### In this week's journey

This is Week 3, **Quality Engineering Foundations**. Our weekly epic is to build the quality-engineering mindset (SDLC and STLC, Agile, the defect lifecycle, Jira, testing principles, and test-design techniques) and apply it every day to **Project 1 - QE Foundations**, a sample web application you will plan quality for.

Earlier today you learned how software is built (the SDLC phases) and the development models teams use (Waterfall, Agile, Scrum, Kanban, and Hybrid). The STLC is the **testing counterpart** of that story. It answers: "While the software is being built, what is the quality team doing, in what order, and how do we know each step is finished?"

Think of today as laying the map. Later in the week you will walk deeper into specific territories:

- **Tuesday:** requirements analysis, test planning, test execution, and the defect lifecycle, in depth.
- **Thursday:** test-design techniques, in depth.

In this lesson you get the **overview of every phase** so that, when those deeper lessons arrive, you already know where each one fits.

---

## The Concept

### 1. An analogy: quality checks in a restaurant kitchen

Imagine a busy restaurant that wants every plate to leave the kitchen safe and delicious. A well-run kitchen does not simply cook and hope. It follows a rhythm:

1. **Understand the order.** The chef reads the ticket: "Grilled chicken, no nuts, medium spice." (Requirement Analysis)
2. **Plan the checks.** The head chef decides who tastes what, which stations are checked, and what "ready to serve" means. (Test Planning)
3. **Write the checklist.** A tasting checklist is prepared: temperature, seasoning, presentation, allergen safety. (Test Case Development)
4. **Prepare the station.** Clean tools, working ovens, fresh ingredients. (Test Environment Setup)
5. **Do the tasting.** Dishes are checked against the checklist, and problems are reported to the cook. (Test Execution)
6. **Review the night.** At closing, the team reviews what went wrong, what was sent back, and what to improve tomorrow. (Test Cycle Closure)

Notice that the cooking (development) and the quality checking (testing) happen side by side. The kitchen does not finish all the cooking and then start thinking about quality. The tasting checklist is prepared while dishes are being designed. That "side by side" idea is exactly how the STLC relates to the SDLC. We will use the kitchen again as we go.

### 2. What is the STLC?

The **Software Testing Life Cycle (STLC)** is a **sequence of specific, planned activities carried out during testing to make sure software quality goals are met**. Each activity (phase) has its own goals, its own conditions for starting and finishing, and its own outputs.

Let us define the key words in that sentence:

- **Life cycle:** an ordered set of stages that something passes through from start to finish.
- **Phase:** one stage in that ordered set.
- **Activity:** a task performed inside a phase (for example, "review the requirements for missing details").
- **Quality goals:** the targets that describe "good enough to release," such as "no open critical defects" or "all high-priority requirements tested."

The STLC does not say *how* to test a particular feature (that is the job of test design techniques, which you will meet on Thursday). It says *what stages the testing effort moves through* and *what must be true at the start and end of each stage*.

> Important note: Different books and websites describe the STLC with slightly different names or numbers of phases. The six-phase version in this lesson is the most commonly taught and is widely recognized in interviews. If you meet a five- or seven-phase version, the same activities are simply grouped differently.

### 3. STLC versus SDLC

You learned earlier that the **Software Development Life Cycle (SDLC)** covers the whole journey of creating software: planning, requirements, design, development, testing, deployment, and maintenance. Notice that "testing" is *one phase* of the SDLC. The STLC zooms into that testing work and describes it in detail, and, importantly, shows that testing-related thinking begins much earlier than the "testing phase."

| Aspect | SDLC | STLC |
|---|---|---|
| Full name | Software Development Life Cycle | Software Testing Life Cycle |
| Main focus | Building the whole product from idea to retirement | Verifying and validating the quality of the product |
| Scope | Entire software lifecycle | Testing activities only |
| Typical phases | Planning, Requirements, Design, Development, Testing, Deployment, Maintenance | Requirement Analysis, Test Planning, Test Case Development, Environment Setup, Test Execution, Test Cycle Closure |
| Main goal | Deliver working software that meets business needs | Find defects and give confidence (or warnings) about quality |
| Main people | Business analysts, architects, developers, testers, operations, product owners | Testers, QA engineers, test leads, with input from developers and analysts |
| Key outputs | Requirements documents, designs, code, builds, release | Test plan, test cases, test data, defect reports, test summary report |
| Relationship | Contains testing as one phase | Runs in parallel with the SDLC phases and feeds back into them |

Two terms from the table deserve a plain definition:

- **Verification:** checking "Are we building the product *right*?" It confirms the product follows its specification (for example, reviewing a document or checking code against a design).
- **Validation:** checking "Are we building the *right* product?" It confirms the product actually meets the user's real needs (for example, running the software as a user would).

### 4. How the STLC runs in parallel with the SDLC

A very common beginner belief is: "Developers build first, then testers test." That is the worst-case picture. In healthy teams, each STLC phase starts as soon as the matching SDLC phase produces something to work with.

| SDLC phase | What is happening | Parallel STLC activity |
|---|---|---|
| Requirements gathering | Business needs are written down | Requirement Analysis: testers review requirements for clarity and testability |
| Planning and design | The product's structure and screens are designed | Test Planning and early Test Case Development |
| Development | Code is written | Test Case Development completes; Test Environment Setup begins; test data prepared |
| Testing | The build is handed over for formal testing | Test Execution and defect reporting |
| Deployment and release | The product goes live | Test Cycle Closure and release sign-off input |
| Maintenance | Fixes and changes continue | Regression testing and new, smaller STLC cycles for every change |

Here is the same idea as a simple picture:

```
SDLC:   [Requirements]--[Design]--[Development]--[Testing]--[Deployment]--[Maintenance]
             |             |            |            |            |             |
             v             v            v            v            v             v
STLC:   [1 Req.      ][2 Test     ][3 Test Case ][5 Test    ][6 Test Cycle ][Regression /
         Analysis ]  [  Planning  ][ Development ][ Execution][ Closure     ] [ new cycles ]
                                   [4 Environment Setup  ]
```

This overlap is sometimes called **"shift left"**: moving quality activities earlier (to the left on a timeline) so defects are found when they are cheapest to fix. A mistake caught in a requirement review costs a conversation. The same mistake caught after release may cost a recall, a security incident, or an angry customer.

### 5. Key vocabulary used in every phase

Before we walk through the phases, we need a shared language. Each phase has the same "shape," so learn these terms once.

| Term | Plain-language meaning | Kitchen analogy |
|---|---|---|
| **Entry criteria** | The conditions that must be true *before* a phase can start. | The oven must be hot and the ingredients delivered before cooking begins. |
| **Exit criteria** | The conditions that must be true *before* a phase can be called finished. | The dish must reach the right temperature and pass the taste check before it leaves the kitchen. |
| **Deliverable (artifact)** | A tangible output a phase produces, such as a document, a list, a report, or a prepared system. | The tasting checklist, the prep list, the end-of-night report. |
| **Activity** | A task performed within the phase. | Chopping, seasoning, plating. |
| **Role** | A person or job type responsible for or involved in the work. | Head chef, line cook, food-safety inspector. |
| **Pitfall** | A common mistake or trap. | Forgetting to ask about allergies. |

Criteria are best written so that they can be answered with **yes or no**. "The requirements are mostly clear" is a feeling. "Requirements document version 1.0 is approved by the product owner" is a fact anyone can check.

There are also two special criteria used mainly during execution:

- **Suspension criteria:** conditions under which testing is **paused** because continuing would waste effort. Example: "The login page does not load at all in the test environment, so no further testing can be done."
- **Resumption criteria:** conditions that must be met before paused testing **restarts**. Example: "A new build is deployed and the login page loads; a quick sanity check passes."

Both are normally defined in the test plan so nobody has to argue about them in the middle of a stressful day.

### 6. Phase 1: Requirement Analysis

**Purpose.** To study what the software is supposed to do **from a testing point of view**, and to decide what is testable. The tester asks: "Can I clearly tell whether this requirement is satisfied or not?"

A **requirement** is a statement of something the software must do or a quality it must have. A **testable requirement** is one with clear, measurable behavior. "The system should be fast" is not testable. "The login page loads in under 3 seconds on a standard broadband connection" is testable.

**Main activities**

- Read and review requirements documents, user stories, and acceptance criteria. (An **acceptance criterion** is a condition the feature must meet to be accepted by the customer.)
- Identify what types of testing are needed (functional, security, performance, usability, and so on).
- List questions and ambiguities and take them to analysts, product owners, and developers.
- Spot missing, conflicting, or untestable requirements.
- Identify the test environment details needed and whether automation is likely to be feasible.
- Begin a **Requirement Traceability Matrix (RTM)**: a table linking each requirement to the tests that will check it (introduced fully in Phase 3).

**Entry criteria**

- Requirements documents or user stories are available.
- Acceptance criteria are available, at least in draft form.
- The application architecture or design overview is available, where applicable.
- Testers have access to someone who can answer questions (a product owner or analyst).

**Exit criteria**

- All requirements have been reviewed and questions are logged.
- Ambiguities are resolved or recorded as open items with owners.
- The list of testable requirements is agreed.
- The initial automation feasibility is noted.

**Deliverables**

- A list of reviewed requirements with comments.
- A question and clarification log.
- A draft RTM.
- An automation feasibility note (a short statement of what might be automated).

**Roles involved:** QA engineers and test leads (main), business analysts, product owners, and developers (clarification).

**Typical tools:** documentation tools (Confluence, Google Docs), Jira for user stories, spreadsheets for RTM drafts, and review comments.

**Common pitfalls**

- Treating requirements as "someone else's job" and starting too late.
- Accepting vague words like "fast," "user-friendly," or "secure" without asking for measurable meaning.
- Not recording the answers to questions, so the same debate repeats later.

**Worked mini-example**

Requirement as written: "Users can log in quickly."

| Tester's question | Why it matters | Clarified result |
|---|---|---|
| What does "quickly" mean? | Not measurable | Login result shown within 3 seconds |
| What counts as a valid login? | Defines expected behavior | Registered email plus correct password |
| What happens after 5 wrong attempts? | Missing behavior | Account locked for 15 minutes |

The vague requirement became three clear, testable statements, and nobody wrote a line of code yet. That is the value of this phase. (**Covered in depth on Tuesday.**)

### 7. Phase 2: Test Planning

**Purpose.** To decide **how the testing will be done**: what will be tested, what will not, by whom, with what, by when, and how we will know we are finished. The result is a plan that the whole team can read and agree on.

**Main activities**

- Define the **scope**: what is in and out of testing.
- Choose the test approach and types of testing.
- Estimate effort, time, and cost.
- Assign roles and responsibilities.
- Select tools (test management, automation, defect tracking).
- Identify **risks**: things that could go wrong and hurt the testing or the product (for example, "the test environment may be late").
- Define entry criteria, exit criteria, and suspension and resumption criteria for later phases.
- Decide the metrics that will be reported.

**Entry criteria**

- Requirement analysis is complete (or complete enough to plan).
- Requirement documents and the analysis output are available.
- Project timelines and team availability are known.

**Exit criteria**

- The test plan is written, reviewed, and approved by the stakeholders (people with an interest in the outcome, such as the project manager and product owner).
- The effort estimate is agreed.
- Tools and resources are confirmed.

**Deliverables**

- The **Test Plan** document (or a one-page test strategy in agile teams).
- The effort and schedule estimate.
- The resource and role assignment.
- A risk list.

**Roles involved:** test lead or test manager (main), project manager, QA engineers, and product owner for approval.

**Typical tools:** Jira, TestRail, Zephyr, Azure DevOps Test Plans, spreadsheets, and Confluence.

**Common pitfalls**

- Copying an old test plan without adapting it.
- Writing a plan nobody reads because it is too long.
- Ignoring risks or giving unrealistic time estimates.
- Forgetting to define "done."

**Worked mini-example**

A one-page plan extract for a login feature:

| Plan item | Decision |
|---|---|
| In scope | Login form, error messages, password reset link, account lock |
| Out of scope | Third-party single sign-on (planned for a later release) |
| Test types | Functional, basic security, basic usability |
| Browsers | Chrome and Firefox (latest versions) |
| Team | 2 QA engineers, 1 test lead |
| Duration | 3 working days of execution |
| Key risk | Test environment delivery may slip by one day |
| Exit criteria for execution | 100% of high-priority tests run; no open critical or high defects |

(**Covered in depth on Tuesday.**)

### 8. Phase 3: Test Case Development

**Purpose.** To create the detailed, repeatable checks (test cases) and the data they need, so that anyone on the team can run them and get comparable results.

Let us define the artifacts of this phase:

- **Test case:** a documented set of inputs, preconditions, steps, and expected results used to check one specific behavior. Think of it as one line on the tasting checklist.
- **Precondition:** what must be true before the test starts (for example, "a registered user exists").
- **Expected result:** what the software *should* do if it works correctly.
- **Test data:** the specific values used in testing, such as email addresses, passwords, product codes, or sample files. Good test data includes valid, invalid, empty, and boundary values.
- **Test suite:** a collection of related test cases run together (for example, "Login suite").
- **Test script:** instructions written as code that a tool runs automatically (relevant when tests are automated).
- **Traceability:** the ability to connect each requirement to the test cases that check it, and each test case back to its requirement. The **Requirement Traceability Matrix (RTM)** is the table that records those links. Its main benefit is **coverage**: it shows at a glance which requirements have tests and which have none.

**Main activities**

- Write test cases from the requirements, covering normal and unusual situations.
- Prepare or generate test data.
- Review test cases with peers, analysts, or developers (a peer review often catches missing cases).
- Update the RTM.
- Identify test cases that are good candidates for automation, and begin automation scripts.

**Entry criteria**

- Requirement analysis is complete.
- The test plan is approved.
- Requirements are stable enough that test cases will not be rewritten daily.

**Exit criteria**

- All planned test cases and test data are written.
- Test cases are reviewed and approved.
- The RTM is updated and shows no uncovered high-priority requirements.
- Automation scripts for planned candidates are ready (if automation is part of the plan).

**Deliverables**

- The test cases (or test scripts).
- The test data set.
- The updated RTM.
- Review comments and approvals.

**Roles involved:** QA engineers and test automation engineers (main), test lead (review), developers and business analysts (review).

**Typical tools:** TestRail, Zephyr, Xray (a Jira add-on), spreadsheets, and test data tools; automation tools later in the program.

**Common pitfalls**

- Writing only "happy path" cases (those where everything goes right) and forgetting errors and edge cases.
- Steps so vague that two testers interpret them differently.
- Test data that is unrealistic or that contains real customer information (a privacy risk).
- Never updating test cases after requirements change.

**Worked mini-example**

| ID | Requirement | Test case title | Steps | Test data | Expected result |
|---|---|---|---|---|---|
| TC-01 | REQ-01 | Login with valid credentials | Open login page; enter email and password; click Login | anna@test.com / Pass@1234 | User lands on dashboard |
| TC-02 | REQ-01 | Login with wrong password | Open login page; enter email and wrong password; click Login | anna@test.com / wrong | Error "Invalid email or password"; user stays on login page |
| TC-03 | REQ-01 | Login with empty fields | Open login page; click Login with nothing entered | (empty) | Field-level messages shown; no login attempt made |

Notice how each test case is small, specific, and has an observable expected result. How to *choose* good test cases systematically (equivalence partitioning, boundary values, and more) is the subject of Thursday's lesson. (**Test design techniques: covered in depth on Thursday.**)

### 9. Phase 4: Test Environment Setup

**Purpose.** To prepare the **place where testing will happen** so that it resembles the real world closely enough for results to be trusted.

A **test environment** is the combination of hardware, software, network settings, configuration, and data on which tests are run. Teams usually have several environments (for example, development, test or QA, staging, and production). Testing is normally done in the QA or staging environment, **not in production**, so real users are never affected.

A **build** is a version of the software packaged so it can be installed and run. A **smoke test** is a very quick check that the most basic functions work (for example, "Does the app start? Can I open the login page?") and decides whether deeper testing is worthwhile.

**Main activities**

- Define what the environment needs: servers, databases, browsers, devices, operating systems, and third-party services.
- Install or deploy the application build.
- Configure the system and load the prepared test data.
- Set up access and accounts for testers.
- Run a **smoke test** on the environment to confirm it is ready.
- Record the environment's configuration so results can be reproduced.

**Entry criteria**

- The test plan identifies the environment needs.
- A test build is available for deployment.
- Hardware, cloud resources, or devices are available.

**Exit criteria**

- The environment is set up and matches the plan.
- Test data is loaded.
- The smoke test passes.
- Testers confirm they can log in and use the environment.

**Deliverables**

- A ready, working test environment.
- An environment setup record (versions, URLs, and configuration notes).
- The smoke test result.

**Roles involved:** DevOps or system administrators (often main), test lead, QA engineers (for smoke testing), and developers (build support).

**Typical tools:** Docker, cloud platforms (AWS, Azure), CI/CD tools such as Jenkins or GitHub Actions, BrowserStack or Sauce Labs for browser and device coverage, and database tools.

**Common pitfalls**

- A test environment that differs strongly from production (different versions, smaller data), producing results that do not match reality.
- Several testers sharing one environment and overwriting each other's data.
- Starting execution without a smoke test and discovering after hours that the build was broken.

**Worked mini-example**

| Environment checklist item | Status |
|---|---|
| Application build 1.0.3 deployed to QA server | Done |
| Test database loaded with 10 sample users | Done |
| Chrome and Firefox (latest) available on test machines | Done |
| Email service in sandbox mode (for password-reset emails) | Done |
| Smoke test: app opens, login page loads | Passed |

Note that in many teams this phase can start **in parallel** with Phase 3 because the environment is independent of the test cases. The kitchen analogy: while the checklist is being written, someone is already cleaning and stocking the stations.

### 10. Phase 5: Test Execution

**Purpose.** To **run the prepared tests** in the prepared environment, compare actual results with expected results, and report any difference as a defect.

A **defect** (also called a **bug**) is a flaw in the software where the actual behavior does not match the expected behavior. A **defect report** is a written record of that flaw with enough detail for a developer to reproduce and fix it. The journey of a defect from discovery to closure is the **defect lifecycle**.

**Main activities**

- Execute test cases (manually or with automated scripts) and record the result of each: **Pass**, **Fail**, **Blocked** (could not run because of another problem), or **Skipped/Not Run**.
- Compare actual results with expected results.
- Log defects with clear steps, evidence (screenshots, logs), severity, and priority.
- Retest fixed defects (**confirmation testing**: running the same failing test again to check the fix worked).
- Run **regression testing** (re-running earlier tests to confirm that a fix or change did not break something that previously worked).
- Update the RTM and keep a daily status report.
- Apply suspension and resumption criteria when needed.

**Entry criteria**

- Test cases and test data are ready and approved.
- The test environment is ready and the smoke test passed.
- The build to be tested is deployed.
- The defect tracking tool is available.

**Exit criteria**

- All planned test cases are executed (or consciously skipped with a recorded reason).
- Defects are logged, and those that are fixed are retested.
- Results are recorded for every test case.
- The agreed pass level is reached, for example "no open critical or high defects."

**Deliverables**

- Executed test cases with results.
- Defect reports.
- Daily or periodic test status reports.
- Updated RTM showing test status per requirement.

**Roles involved:** QA engineers and automation engineers (main), developers (fix defects), test lead (monitor and report), product owner (decide priorities).

**Typical tools:** Jira (defects), TestRail, Zephyr, or Xray (execution tracking), browser developer tools, and automation tools.

**Common pitfalls**

- Poor defect reports ("login broken") that developers cannot reproduce.
- Skipping the retest or regression step to "save time."
- Updating results at the end of the day from memory rather than as work happens.
- Continuing to test on a build that is clearly unstable instead of invoking suspension criteria.

**Worked mini-example**

| ID | Result | Notes |
|---|---|---|
| TC-01 | Pass | Dashboard displayed |
| TC-02 | Pass | Correct error message shown |
| TC-03 | Fail | No messages shown; page reloads silently. Defect DEF-101 logged (Severity: Medium) |

A short defect report for the failing case:

| Field | Content |
|---|---|
| ID | DEF-101 |
| Title | No validation message when logging in with empty fields |
| Steps | 1. Open login page. 2. Leave both fields empty. 3. Click Login |
| Expected | Field-level messages ("Email is required") |
| Actual | Page reloads with no message |
| Environment | QA, build 1.0.3, Chrome latest |
| Severity | Medium |

Suspension example: if every login attempt crashes the server, testing of the rest of the application is **suspended** until a fixed build is deployed and a smoke test passes (**resumption**). (**Execution and the defect lifecycle: covered in depth on Tuesday.**)

### 11. Phase 6: Test Cycle Closure

**Purpose.** To **formally wrap up** the testing effort: confirm completion against the exit criteria, summarize results, and capture lessons for the future.

A **test cycle** is one round of executing tests against a build. A project may have several cycles (for example, Cycle 1 on the first build, Cycle 2 after fixes). Closure happens at the end of each cycle and at the end of the whole testing effort.

**Main activities**

- Check that all execution exit criteria are met.
- Analyze results and calculate **test metrics** (see below).
- Review open defects and agree what is accepted, deferred, or must be fixed.
- Prepare the **Test Closure Report** (also called the Test Summary Report).
- Hold a **retrospective** or lessons-learned meeting: what went well, what did not, and what to change.
- Archive test artifacts (test cases, data, scripts, reports) for reuse and audit.
- Give a quality summary to decision makers, who decide whether to release.

**Entry criteria**

- Test execution is complete.
- Defect statuses are up to date.
- Results are recorded for all executed tests.

**Exit criteria**

- The test closure report is prepared, reviewed, and signed off.
- Lessons learned are recorded.
- Test artifacts are archived.
- Remaining risks and known defects are communicated.

**Deliverables**

- Test Closure (Summary) Report.
- Test metrics and charts.
- Lessons-learned or retrospective notes.
- Archived test assets.

**Roles involved:** test lead or manager (main), QA engineers, project manager, and product owner (receives results and decides on release).

**Typical tools:** Jira dashboards, TestRail or Zephyr reports, Confluence, spreadsheets, and Power BI or Grafana for dashboards.

**Common pitfalls**

- Skipping closure because "we are already late."
- Reporting only numbers without telling the story (what the numbers mean for risk).
- Not recording lessons, so the next project repeats the same mistakes.
- Hiding known risks to make the report look better.

**Test metrics introduced simply**

A **metric** is a measurement that turns activity into numbers so progress and quality can be discussed objectively. Common closure metrics:

| Metric | Plain meaning | Simple formula | Example |
|---|---|---|---|
| Execution percentage | How much of the planned testing was actually run | Executed tests / Planned tests x 100 | 18 / 20 x 100 = 90% |
| Pass percentage | How many executed tests passed | Passed tests / Executed tests x 100 | 16 / 18 x 100 = 88.9% |
| Requirement coverage | How many requirements have at least one test | Requirements with tests / Total requirements x 100 | 9 / 10 x 100 = 90% |
| Defect density | How many defects per unit of size (for example, per feature or per 1,000 lines of code) | Defects found / Size | 12 defects / 4 features = 3 per feature |
| Defect distribution | Where defects cluster (by module, severity, or cause) | Count defects per category | 7 of 12 defects in the password reset module |
| Defect leakage | Defects found by users after release rather than by testers | Defects found after release / Total defects x 100 | 2 / 50 x 100 = 4% |

A caution that serious teams always repeat: **numbers do not speak for themselves.** A 95% pass rate sounds excellent, but if the 5% that failed are critical payment bugs, the product is not ready. Always read metrics together with severity and risk.

**Worked mini-example: closure summary snapshot**

| Item | Value |
|---|---|
| Feature | User login, Cycle 1 |
| Planned / executed test cases | 20 / 20 |
| Passed / Failed / Blocked | 17 / 3 / 0 |
| Pass percentage | 85% |
| Defects found | 5 (0 critical, 1 high, 2 medium, 2 low) |
| Defects fixed and verified | 4 |
| Open defects | 1 low (accepted, deferred to next sprint) |
| Requirement coverage | 100% |
| Recommendation | Ready for release |

### 12. All six phases at a glance

Here is the complete flow:

```
 +----------------------+
 | 1. REQUIREMENT       |  Understand and question the requirements
 |    ANALYSIS          |  Output: reviewed requirements, question log, draft RTM
 +----------+-----------+
            |  exit criteria met
            v
 +----------------------+
 | 2. TEST PLANNING     |  Decide scope, approach, team, schedule, risks
 |                      |  Output: test plan, estimate, risk list
 +----------+-----------+
            |
            v
 +----------------------+        +----------------------+
 | 3. TEST CASE         |        | 4. TEST ENVIRONMENT  |
 |    DEVELOPMENT       | <----> |    SETUP             |  (often in parallel)
 |  Output: test cases, |        |  Output: ready       |
 |  test data, RTM      |        |  environment, smoke  |
 +----------+-----------+        |  test result         |
            |                    +----------+-----------+
            +------------+-------------------+
                         v
              +----------------------+
              | 5. TEST EXECUTION    |  Run tests, log defects, retest, regression
              |                      |  Output: results, defect reports, status reports
              +----------+-----------+   (suspend / resume if needed)
                         |
                         v
              +----------------------+
              | 6. TEST CYCLE        |  Metrics, closure report, lessons learned
              |    CLOSURE           |  Output: closure report, archived artifacts
              +----------------------+
                         |
                         v
               Release decision / next cycle
```

And a summary table you can keep beside your desk:

| Phase | Purpose in one line | Key entry criterion | Key exit criterion | Main deliverable |
|---|---|---|---|---|
| 1. Requirement Analysis | Understand what is testable | Requirements and acceptance criteria available | Questions resolved or logged | Reviewed requirements, draft RTM |
| 2. Test Planning | Decide how to test | Requirement analysis complete | Plan approved | Test plan, estimates |
| 3. Test Case Development | Create the checks and data | Plan approved, stable requirements | Test cases reviewed and approved | Test cases, test data, RTM |
| 4. Test Environment Setup | Prepare where tests run | Build available, environment needs known | Smoke test passes | Ready environment |
| 5. Test Execution | Run tests and report defects | Cases ready, environment ready | Planned tests run; defects handled | Results, defect reports |
| 6. Test Cycle Closure | Summarize and learn | Execution complete | Report signed off | Closure report, lessons learned |

### 13. Is the STLC strictly one-way?

On paper the phases look like a straight line. In real life, they overlap and loop:

- Requirements change, so test cases are updated (back from Phase 5 to Phase 3).
- A defect fix arrives, so a new build is deployed and a new smoke test runs (back to Phase 4).
- Closure of Cycle 1 is followed by the start of Cycle 2 on the next build.

The entry and exit criteria exist exactly because the phases can overlap: they tell the team **what is minimally required** to move forward safely, without forcing a rigid "finish everything first" rule. In a Waterfall project, the phases are often long and sequential. In Agile, they are short and repeated, as we see next.

### 14. How the STLC adapts inside Agile sprints

You learned that in Agile and Scrum, work happens in short time-boxed iterations called **sprints** (commonly one to four weeks). In each sprint the team plans, builds, tests, and delivers a small slice of working software. The six STLC phases do not disappear; they are **compressed, overlapped, and repeated every sprint**.

| STLC phase | In a traditional (Waterfall) project | Inside an Agile sprint |
|---|---|---|
| Requirement Analysis | Weeks, with a large requirements document | Happens in backlog refinement and sprint planning; testers help write **acceptance criteria** for each user story |
| Test Planning | Large, formal test plan for the whole project | A lightweight plan: a release-level test strategy plus a short sprint test plan (often a conversation and a few lines on the board) |
| Test Case Development | Done in a block before testing | Done continuously, in parallel with coding; often written as acceptance tests before or during development |
| Test Environment Setup | Once, at the start of the testing phase | Largely automated through CI/CD; a fresh environment per build |
| Test Execution | A long testing phase near the end | Daily, as each story becomes ready; heavy use of automated regression suites |
| Test Cycle Closure | One formal report at the end | A **sprint review** (demo) and **sprint retrospective**; a short quality summary each sprint |

Key ideas in agile STLC:

- **Continuous testing:** testing happens throughout the sprint, not at the end. As soon as a story is "ready for test," a tester picks it up.
- **Whole-team quality:** developers write unit tests, testers explore and automate, and everyone shares responsibility for quality.
- **Definition of Done (DoD):** a shared checklist that a story must satisfy to count as complete (for example, "code reviewed, tests passed, no open high defects, documentation updated"). The DoD works like a team-wide set of exit criteria.
- **Regression automation:** because the product changes every sprint, automated regression tests protect old features cheaply. This is a major reason test automation engineers are in demand.
- **Smaller batches, faster feedback:** defects are found within hours or days of being introduced.

A simplified two-week sprint:

```
Day 1-2   : Sprint planning; testers clarify acceptance criteria (Phase 1, 2)
Day 2-5   : Test cases written while developers code (Phase 3)
Day 3-9   : Stories delivered to test as ready; execute, log defects, retest (Phase 4, 5)
Day 9-10  : Regression run, sprint review, retrospective (Phase 6)
```

### 15. Worked example: "User Login" through all six phases

Let us follow one feature end to end. Imagine the Project 1 app is an online shop called "ShopEasy," and the team is delivering a new **User Login** feature in a two-week sprint.

**The user story:** "As a registered customer, I want to log in with my email and password so that I can see my account and orders."

**Acceptance criteria (draft):**
1. A registered user with valid credentials reaches the dashboard.
2. An invalid email or password shows the message "Invalid email or password" without saying which part is wrong.
3. After 5 consecutive failed attempts, the account locks for 15 minutes.
4. Empty fields show field-level validation messages.
5. The login result appears within 3 seconds.

#### Phase 1: Requirement Analysis

The tester reads the story and acceptance criteria and raises questions.

| Question | Answer from product owner | Outcome |
|---|---|---|
| Is the email case-sensitive? | No, treat emails as case-insensitive | New testable rule added |
| Does the lock message tell the user how long to wait? | Yes, "Try again in 15 minutes" | Acceptance criterion 3 updated |
| Is "Remember me" in scope? | Not this sprint | Added to out-of-scope list |
| Which browsers are supported? | Latest Chrome and Firefox | Recorded for planning |

Draft RTM at this point:

| Requirement ID | Requirement | Test cases |
|---|---|---|
| REQ-01 | Valid login reaches dashboard | (to be linked) |
| REQ-02 | Invalid credentials show a generic error | (to be linked) |
| REQ-03 | Account locks after 5 failed attempts | (to be linked) |
| REQ-04 | Empty-field validation | (to be linked) |
| REQ-05 | Login responds within 3 seconds | (to be linked) |

#### Phase 2: Test Planning

| Plan item | Decision |
|---|---|
| Scope | REQ-01 to REQ-05 on Chrome and Firefox |
| Out of scope | "Remember me," single sign-on |
| Approach | Manual functional testing first; automate the happy path and the lock scenario for regression |
| Team | 1 QA engineer (execution), 1 automation engineer (scripts) |
| Schedule | Test cases by Day 4; execution Days 5 to 9 |
| Risks | The lock feature depends on a time setting that may be hard to test; mitigation: ask developers for a configurable lock duration in the test environment |
| Execution exit criteria | All high-priority cases run; no open critical or high defects |
| Suspension criteria | Login page unavailable or server errors on more than half of attempts |
| Resumption criteria | New build deployed and smoke test passes |

#### Phase 3: Test Case Development

| ID | Req | Title | Test data | Expected result | Priority |
|---|---|---|---|---|---|
| TC-01 | REQ-01 | Valid login | anna@shop.com / Pass@1234 | Dashboard displayed | High |
| TC-02 | REQ-02 | Wrong password | anna@shop.com / wrong | "Invalid email or password" | High |
| TC-03 | REQ-02 | Unregistered email | ghost@shop.com / Pass@1234 | Same generic message | High |
| TC-04 | REQ-03 | Account locks after 5 failures | anna@shop.com / wrong, five times | Lock message with 15 minutes | High |
| TC-05 | REQ-04 | Both fields empty | (empty) | Field-level messages | Medium |
| TC-06 | REQ-05 | Response time | anna@shop.com / Pass@1234 | Result appears in 3 seconds or less | Medium |
| TC-07 | REQ-01 | Email in different letter case | ANNA@SHOP.COM / Pass@1234 | Login succeeds | Medium |

Updated RTM:

| Requirement ID | Test cases | Coverage |
|---|---|---|
| REQ-01 | TC-01, TC-07 | Covered |
| REQ-02 | TC-02, TC-03 | Covered |
| REQ-03 | TC-04 | Covered |
| REQ-04 | TC-05 | Covered |
| REQ-05 | TC-06 | Covered |

Test data prepared: five registered users (including one dedicated to the lock test, because that test locks the account), plus one unregistered email. A peer review adds TC-07 and a note to reset the locked account between runs.

#### Phase 4: Test Environment Setup

| Item | Status |
|---|---|
| QA server with build 1.0.3 | Deployed by CI pipeline |
| Test database with 5 users | Loaded |
| Lock duration configured to 2 minutes in QA (to keep tests fast) | Done and documented |
| Chrome and Firefox on tester machines | Available |
| Smoke test (open the app and display the login page) | Passed |

Documenting the changed lock duration matters: the tester must remember that TC-04 verifies the behavior using a shortened time, and a final check of the real 15-minute value should be arranged separately.

#### Phase 5: Test Execution

| ID | Result | Notes |
|---|---|---|
| TC-01 | Pass | |
| TC-02 | Pass | |
| TC-03 | Fail | Message says "Email not found," which reveals that the address is unregistered. Defect DEF-201 (Severity: High, a security concern) |
| TC-04 | Pass | |
| TC-05 | Fail | No validation messages. Defect DEF-202 (Medium) |
| TC-06 | Pass | 1.4 seconds |
| TC-07 | Pass | |

The developers fix DEF-201 and DEF-202 in build 1.0.4. The tester redeploys, runs the smoke test, **retests** TC-03 and TC-05 (both pass), then runs a short **regression** across TC-01, TC-02, and TC-04 to be sure nothing else broke. All pass.

#### Phase 6: Test Cycle Closure

| Item | Value |
|---|---|
| Feature | User Login, Sprint 4 |
| Test cases planned / executed | 7 / 7 |
| Results in Cycle 1 (build 1.0.3) | 5 passed, 2 failed |
| Results after retest and regression (build 1.0.4) | 7 passed |
| Pass percentage (final) | 100% |
| Requirement coverage | 100% (5 of 5) |
| Defects found / fixed | 2 / 2 |
| Defect distribution | 1 High (security message), 1 Medium (validation) |
| Open defects | 0 |
| Known gap | Real 15-minute lock duration verified by a single manual check on staging, not repeated |
| Automation | TC-01 and TC-04 scripted for regression |
| Lessons learned | Ask about error-message wording during Requirement Analysis; keep a dedicated test user for lock tests |
| Recommendation | Ready for release |

Looking back across the whole example, you can see the six phases working as a chain: questions in Phase 1 shaped the plan in Phase 2, the plan shaped the cases in Phase 3, the environment in Phase 4 made them runnable, execution in Phase 5 produced evidence, and closure in Phase 6 turned evidence into a decision and into learning.

### 16. The role of AI-assisted tools in the STLC (high level)

Modern testing teams increasingly use AI assistants (for example, large-language-model tools and AI features built into test management or automation products). Used well, they act like a fast, tireless junior colleague who produces first drafts. Here is where they can help at each phase:

| STLC phase | How AI can help | Caution |
|---|---|---|
| Requirement Analysis | Summarize long documents; flag vague words ("fast," "easy"); suggest clarifying questions; spot possible conflicts between requirements | It may miss context only your team knows, or invent assumptions that sound reasonable |
| Test Planning | Draft a plan outline; suggest risks; propose effort estimates from similar projects | Estimates and risk ratings must be judged by someone who knows the project |
| Test Case Development | Generate draft test cases and test data variations from user stories; suggest edge cases you forgot; draft traceability links | Drafts can be repetitive, wrong, or untestable; they may miss business rules |
| Test Environment Setup | Help write configuration or scripts; generate synthetic test data | Never paste real customer data or secrets into an external tool |
| Test Execution | Assist with writing automation scripts; summarize failing logs; suggest likely causes; help draft defect reports | A suggested cause is a hypothesis, not a diagnosis; always reproduce the defect yourself |
| Test Cycle Closure | Summarize results into a report draft; spot patterns in defects | Never let it adjust or "smooth" the numbers; confirm every figure against the source |

Honest cautions that apply everywhere:

1. **AI can be confidently wrong.** It can produce plausible test cases that do not match your actual requirements. The tester remains accountable for correctness.
2. **Garbage in, garbage out.** Vague prompts and unclear requirements produce vague results. The clearer your Phase 1 work, the better any assistant performs.
3. **Protect confidential data.** Follow your organization's rules before sharing requirements, code, or data with any AI tool. Use synthetic or anonymized data.
4. **Review everything.** Treat AI output as a draft that needs peer review, just like a colleague's first attempt.
5. **Keep your skills sharp.** To judge AI output you must understand the underlying concepts. That is why you are learning the fundamentals first.
6. **Do not over-trust coverage claims.** "AI generated 200 test cases" is not the same as "200 meaningful tests." More is not automatically better.

A healthy mindset: **AI accelerates the drafting; the engineer owns the judgment.**

---

## Examples

### Example A: A quick contrast, "no STLC" versus "with STLC"

| Situation | Team without a structured STLC | Team following the STLC |
|---|---|---|
| Requirements are unclear | Discovered during testing, after code is written | Questions raised during Requirement Analysis, before coding |
| "What are we testing?" | Different opinions | Agreed in the test plan |
| Test cases | Kept in people's heads | Written, reviewed, and traceable |
| Environment fails mid-test | Hours wasted | Smoke test catches it first |
| Release decision | "I think it is fine" | Closure report with metrics and known risks |
| Next project | Same mistakes repeated | Lessons learned applied |

### Example B: Entry and exit criteria for an online store checkout (short version)

| Phase | Entry criteria | Exit criteria |
|---|---|---|
| Requirement Analysis | Checkout user stories and payment rules available | All questions about discounts, tax, and payment failure are answered or logged |
| Test Planning | Analysis complete; timeline known | Test plan approved by product owner |
| Test Case Development | Plan approved; payment sandbox details known | Cases reviewed; every checkout requirement has at least one test |
| Test Environment Setup | Build ready; payment sandbox account available | Smoke test (add to cart and reach payment page) passes |
| Test Execution | Cases, data, and environment ready | All high-priority cases run; no open critical defects |
| Test Cycle Closure | Execution complete | Closure report signed off; lessons recorded |

### Example C: When suspension criteria save the day

On Day 2 of execution, the test environment's database connection fails and every checkout attempt returns a server error. Because the plan already says "suspend testing if more than half of attempts fail with server errors," the tester does not waste hours logging fifty identical defects. They raise one blocking issue, pause, and wait. The resumption rule ("new build deployed and smoke test passes") tells everyone exactly when to restart. Testing time is protected, and the report to management explains the delay with facts.

---

## Knowledge Check

Try to answer each question before reading the short answer.

**1. What does STLC stand for, and what is its main purpose?**
*Answer:* Software Testing Life Cycle. It is the ordered set of testing phases, each with its own activities, criteria, and deliverables, used to make sure quality goals are met.

**2. Name the six classic STLC phases in order.**
*Answer:* Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution, Test Cycle Closure.

**3. How is the STLC different from the SDLC?**
*Answer:* The SDLC covers building the whole product from idea to maintenance; the STLC covers only the testing activities and describes them in detail. Testing is one phase of the SDLC, but STLC activities start earlier and run in parallel with the SDLC phases.

**4. What is an entry criterion? Give an example.**
*Answer:* A condition that must be true before a phase starts. Example: "The test build is deployed and the smoke test passed" before Test Execution begins.

**5. What is an exit criterion? Give an example.**
*Answer:* A condition that must be true before a phase can be considered finished. Example: "All high-priority test cases have been run and there are no open critical defects."

**6. What is a deliverable?**
*Answer:* A tangible output produced by a phase, such as the test plan, test cases, defect reports, or the closure report.

**7. Why is the test environment usually not production?**
*Answer:* Testing can create, change, or break data and could affect real users. A separate environment that resembles production keeps users safe while still giving trustworthy results.

**8. What is the difference between suspension and resumption criteria?**
*Answer:* Suspension criteria define when testing is paused because it would be wasteful or impossible to continue; resumption criteria define what must be true before testing restarts.

**9. A test run has 40 executed tests and 34 passed. What is the pass percentage?**
*Answer:* 34 / 40 x 100 = 85%.

**10. Why might a 95% pass rate still be a bad sign?**
*Answer:* Because the failed 5% might include critical defects. Metrics must always be read with severity and risk.

**11. What is a Requirement Traceability Matrix and why is it useful?**
*Answer:* A table that links requirements to the test cases that verify them. It shows coverage and exposes requirements that have no tests.

**12. What is the difference between confirmation testing and regression testing?**
*Answer:* Confirmation testing re-runs the failed test to check that the specific defect is fixed. Regression testing re-runs other tests to check that the fix did not break existing functionality.

**13. How does the STLC change in an Agile sprint?**
*Answer:* The phases are compressed, overlapped, and repeated each sprint: testers join refinement to shape acceptance criteria, write test cases while developers code, test stories as they become ready, rely on automated regression, and close the cycle in the sprint review and retrospective.

**14. Give two ways AI tools can help in the STLC and one caution.**
*Answer:* They can draft test cases from user stories and flag vague requirements. A caution: AI output can be confidently wrong and must be reviewed, and confidential data must not be shared with unapproved tools.

**15. Which phases will be taught in more depth on Tuesday and Thursday?**
*Answer:* Tuesday covers requirements analysis, test planning, test execution, and the defect lifecycle in depth; Thursday covers test-design techniques.

---

## Try It: Project 1 STLC Criteria Workbook

**Goal:** Practice thinking like a test lead by writing clear, checkable entry and exit criteria for every STLC phase of **Project 1 - QE Foundations**.

**Time:** about 45 to 60 minutes. Work individually, then compare with a partner.

**Step 1: Choose a feature.** Pick one feature of your Project 1 web app (for example, login, registration, search, add to cart, or profile update). Write the feature name and a one-sentence user story at the top of your page.

**Step 2: Create this table in a document or spreadsheet.**

| Phase | Entry criteria (2 to 3 items) | Exit criteria (2 to 3 items) | Deliverables | Roles involved | Possible tools |
|---|---|---|---|---|---|
| 1. Requirement Analysis | | | | | |
| 2. Test Planning | | | | | |
| 3. Test Case Development | | | | | |
| 4. Test Environment Setup | | | | | |
| 5. Test Execution | | | | | |
| 6. Test Cycle Closure | | | | | |

**Step 3: Apply the "yes or no" test.** Read each criterion aloud. If a teammate could not answer it with a clear yes or no, rewrite it. Replace "requirements are clear" with "all open questions in the clarification log have an owner and an answer or a due date."

**Step 4: Add execution safety rules.** Write one **suspension criterion** and one **resumption criterion** for Test Execution of your chosen feature.

**Step 5: Draft a mini trace.** List three requirements for your feature and write at least one test case title for each. Build a three-row RTM like the one in the login example.

**Step 6: Sketch a closure summary.** Using invented but realistic numbers, fill in a short closure table (planned and executed tests, pass percentage, defects found by severity, open defects, recommendation). Calculate the pass percentage yourself.

**Step 7 (optional AI practice):** If your instructor approves a tool, ask an AI assistant to suggest additional entry and exit criteria for one phase. Then write down (a) one suggestion that was useful, (b) one that was wrong, vague, or unnecessary, and (c) how you decided. Do not paste any confidential information.

**Self-check list**

- Is every criterion specific enough to verify?
- Does each phase's exit connect logically to the next phase's entry?
- Did I include at least one deliverable for every phase?
- Does my RTM show every requirement covered by at least one test?
- Did I resist the temptation to describe test design or defect handling in depth? (Those come later in the week.)

Keep your workbook. On Tuesday you will deepen the Requirement Analysis, Test Planning, and Test Execution rows, and on Thursday you will improve your test case titles using design techniques.

---

## Key Takeaways

- The **STLC** is the planned sequence of testing phases: Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution, and Test Cycle Closure.
- The STLC is **not** a replacement for the SDLC. Testing is a phase of the SDLC, and the STLC runs in parallel with it, starting as early as requirements.
- Every phase has **entry criteria, exit criteria, activities, deliverables, roles, tools**, and common pitfalls. Write criteria so they can be answered with yes or no.
- **Deliverables** (test plan, test cases, test data, RTM, defect reports, closure report) are the evidence that quality work happened.
- **Suspension and resumption criteria** protect the team from wasting effort on unusable builds and tell everyone when to pause and restart.
- **Traceability** (the RTM) connects requirements to tests so coverage gaps become visible.
- **Metrics** such as pass percentage, requirement coverage, and defect density summarize progress, but they must be read alongside severity and risk.
- In **Agile**, the same six phases are compressed, overlapped, and repeated every sprint, supported by continuous testing, automation, and the Definition of Done.
- **AI tools** can speed up drafting and analysis, but they can be confidently wrong, so engineers must review, protect data, and remain accountable.
- Deeper detail is coming: **Tuesday** (requirements analysis, test planning, execution, defect lifecycle) and **Thursday** (test-design techniques).

---

## Additional Resources

- **ISTQB (International Software Testing Qualifications Board):** the international body behind the widely recognized Foundation Level certification and the testing glossary. Home page: https://www.istqb.org/ and glossary: https://glossary.istqb.org/
- **Guru99, "Software Testing Life Cycle (STLC)":** a beginner-friendly walkthrough of the phases with entry and exit criteria. https://www.guru99.com/software-testing-life-cycle.html
- **Atlassian, "Software Testing" (Continuous Delivery guides):** practical articles on testing types and how testing fits into modern delivery. https://www.atlassian.com/continuous-delivery/software-testing
