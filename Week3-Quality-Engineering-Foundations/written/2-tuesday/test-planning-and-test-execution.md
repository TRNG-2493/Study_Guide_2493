# Test Planning and Test Execution

**Week 3 - Quality Engineering Foundations | Tuesday: Test Management and Defect Lifecycle**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain why test planning exists and what problems a good plan prevents.
2. Distinguish a **test strategy** from a **test plan**, and say who owns each.
3. Describe each section of an IEEE 829 / ISO 29119-style test plan in plain language.
4. Use a **likelihood x impact** matrix to prioritize testing by risk.
5. Apply four estimation techniques: work breakdown, three-point (PERT), experience-based, and story points.
6. Write a lightweight, one-page test plan suitable for an Agile team.
7. Name the four classic **test levels** (unit, integration, system, acceptance) and say what each is for.
8. Write a clear test case using the standard fields, and tell a good test case from a poor one.
9. Organize test cases into **test suites** and **test cycles**.
10. Check execution prerequisites, run a **smoke** or **sanity** check, and confirm the test environment is ready.
11. Execute test cases step by step, record results (Pass, Fail, Blocked, Skipped, Not Run), and attach evidence.
12. Calculate and interpret test metrics: execution %, pass %, defect density, defect leakage, and defect detection percentage (DDP).
13. Trace test cases back to requirements, write a daily status report, and produce a test closure (exit) report.
14. Handle blocked tests and schedule slippage professionally.

---

## Why This Matters

Imagine you are asked to organize a school trip for forty students. You would not simply put everyone on a bus and hope for the best. You would decide where you are going, what time you leave, who is responsible for which group, what to do if it rains, how many chaperones you need, and when the trip counts as "finished" (everyone back, headcount complete). You would also pack a checklist and tick things off as the day goes on.

Testing a software feature is the same. Without a plan, testers do one of two things: they test randomly and miss important areas, or they test forever because nobody agreed on what "done" looks like. Without disciplined execution, results are lost in someone's memory, bugs are reported without evidence, and managers have no idea whether the product is ready to release.

Yesterday you learned the big picture: the SDLC, development models, the six phases of the STLC (Software Testing Life Cycle), Agile roles, Scrum ceremonies, and a first look at Jira. This morning you practiced **requirements analysis**, the first STLC phase. Today you move into the next two phases, which are the heart of daily QE work:

- **Test planning** (and test design at a basic level): deciding what to test, how, by whom, and when.
- **Test execution**: actually running the tests, recording what happened, and telling the team the truth about quality.

In a real job, a hiring manager will ask you: "Can you write a test plan? Can you write test cases? How do you report progress?" After this lesson, you can answer yes, and you can show a sample for a real feature.

A note on boundaries: the **defect lifecycle** (what happens to a bug after you log it) is the next lesson. **Test design techniques** such as equivalence partitioning and boundary value analysis are taught on Thursday. **Testing principles** come on Wednesday, and **regression testing** is explored in depth on Friday. Today we introduce them only where needed.

---

## The Concept

### Part A: Test Planning

#### 1. What is test planning, and why do we do it?

**Test planning** is the activity of defining the objectives of testing and the approach for meeting those objectives within the constraints of the project (time, people, budget, tools, environments). The written result of this activity is a document called the **test plan**.

Think of a **trip itinerary**. An itinerary tells you:

| Trip itinerary | Test plan equivalent |
|---|---|
| Destination | Objective: what are we trying to achieve? |
| Places you will visit and places you will skip | Scope: what is in and out of testing |
| How you will travel (train, bus, walking) | Approach: how we will test |
| Who is traveling and who is the group leader | Roles and responsibilities |
| Departure and arrival times | Schedule and milestones |
| Budget and packing list | Resources, tools, and effort |
| "If it rains, we go to the museum" | Risks and mitigation, suspension and resumption criteria |
| "The trip ends when everyone is back at school" | Exit criteria |
| Permission slips signed by parents | Approvals |

A test plan answers the questions **what, why, how, who, when, where, and what if**. Its main purposes are:

1. **Align the team.** Developers, testers, product owners, and managers share one understanding of what will be tested.
2. **Reduce risk.** Planning forces us to think about what could go wrong before it does.
3. **Control effort.** We estimate time and people so that testing is neither starved nor wasteful.
4. **Define "done."** Entry and exit criteria prevent endless testing and premature release.
5. **Provide a communication tool.** Stakeholders who do not test (for example, a business sponsor) can read the plan and understand what quality work is happening.
6. **Create an audit trail.** In regulated industries (banking, healthcare, aviation), the plan is evidence that testing was done deliberately.

A plan is not a promise carved in stone. It is a living document. Requirements change, people get sick, environments break. A good plan is **updated** when reality changes. The famous saying applies: "Plans are useless, but planning is indispensable." The thinking is what matters most.

#### 2. Test strategy versus test plan

Beginners often confuse these two. Both are documents, and both talk about "how we test", but they live at different levels.

- A **test strategy** is a high-level, long-lived description of the general approach to testing for an organization or a product line. It rarely changes from project to project. It answers: "In general, how do we do testing here?"
- A **test plan** is a project-specific (or release-specific, or feature-specific) document. It answers: "For *this* release, what exactly will we test, who will do it, and by when?"

Think of the strategy as a company's **travel policy** ("we always book economy flights, we always buy travel insurance, receipts must be kept") and the plan as the **itinerary for one specific trip** to one specific city.

| Aspect | Test Strategy | Test Plan |
|---|---|---|
| Level | Organization or product-line level | Project, release, or feature level |
| Lifetime | Long-lived; changes rarely | Short-lived; changes with the project |
| Typical owner | QA manager, test architect, head of quality | Test lead, QE lead, or the tester for a small feature |
| Content | General principles, test levels used, tools standards, defect-management approach, metrics standards, automation approach | Specific scope, schedule, resources, environments, risks, entry/exit criteria for this project |
| Answers | "How do we test in general?" | "What, who, when, where for this release?" |
| Can be a separate document? | Yes, or part of a larger quality policy | Yes; often references the strategy |
| Example statement | "All web products are tested on the latest two versions of Chrome, Firefox, and Edge." | "For Release 1.2 the login feature will be tested on Chrome 126 and Firefox 127 between 3 and 14 March." |
| Reused? | Reused across many projects | Created (or copied and adapted) per project |

In small teams, you may see one combined document, or only a plan that quotes a few strategy rules. That is fine. What matters is that you understand the difference in level.

#### 3. The anatomy of a test plan (IEEE 829 / ISO 29119 style)

Two well-known standards describe test documentation:

- **IEEE 829** (IEEE Standard for Software and System Test Documentation). It defines a classic test plan outline.
- **ISO/IEC/IEEE 29119** (Software Testing standard series). It is the more modern international standard, and Part 3 covers test documentation, including test plans.

You do not need to memorize the standards' clause numbers. You need to know the **common sections** that appear in nearly every professional test plan. Each is explained below, with a plain-language question it answers.

**3.1 Test plan identifier and introduction.** A unique ID, a version number, an author, a date, and a short introduction. *Question: which document is this and what is it about?* Example: "TP-P1-LOGIN-v1.0, Test Plan for User Registration and Login, Project 1."

**3.2 Objective.** A short statement of what testing is meant to achieve. *Question: why are we testing?* A good objective is specific: "Verify that new users can register and log in securely according to requirements REQ-01 to REQ-10, and that no critical or high severity defects remain open at release."

**3.3 Scope: in scope and out of scope.** *In scope* lists the features, requirements, and quality aspects that will be tested. *Out of scope* lists what will deliberately **not** be tested (for example, features planned for a later release, third-party systems, or performance testing for this cycle). Writing the out-of-scope list protects you: when someone asks, "Why didn't you test password reset?", you can point to the plan, which was approved before testing began.

**3.4 Test approach (test strategy for this project).** *Question: how will we test?* It describes manual versus automated testing, the types of testing to be performed, how test cases will be designed (details are covered on Thursday), how defects will be reported, and how results will be tracked. It may also include the risk-based approach (explained below).

**3.5 Test levels and test types overview.** *Question: at which levels, and what kinds of testing?* Levels (unit, integration, system, acceptance) say *where in the build-up of the product* we test. Types (functional, usability, compatibility, security, performance, and so on) say *what quality characteristic* we examine. Details below.

**3.6 Test environment.** *Question: where will we test?* The hardware, operating systems, browsers, devices, servers, databases, network settings, and versions of the application under test. Include who owns the environment and how to request fixes. Environments are often named: DEV (developers), QA or TEST (testers), STAGING or UAT (final checks), PROD (live production).

**3.7 Test data.** *Question: what data do we need?* Valid and invalid user accounts, sample emails, product catalogs, and so on. Include how the data is created (manual, scripts, database seeding), whether it must be anonymized (never use real customers' personal data without protection), and how it is refreshed.

**3.8 Roles and responsibilities.** *Question: who does what?* Names (or role titles) and duties: test lead, testers, developers who fix bugs, product owner who approves, DevOps who maintains the environment.

**3.9 Schedule and milestones.** *Question: when?* Key dates: test design complete, environment ready, execution start, execution end, regression cycle, sign-off. Milestones are important checkpoints.

**3.10 Effort estimation.** *Question: how much work and how many people?* Hours or days for planning, designing, executing, retesting, and reporting. Estimation techniques are discussed below.

**3.11 Resources and tools.** *Question: what do we need?* People, test management tools, defect tracker (Jira), browsers, devices, automation frameworks, and communication tools.

**3.12 Entry criteria.** The conditions that must be true **before** a testing phase may begin. Example: "Build deployed to the QA environment; smoke test passed; test cases reviewed and approved; test data available." Like a stadium that opens its gates only when the security check is complete.

**3.13 Exit criteria.** The conditions that must be true for testing to be considered **complete**. Example: "100% of planned test cases executed; at least 95% passed; no open Critical or High defects; all Medium defects have an agreed plan; test summary report approved." Exit criteria are the answer to "when do we stop?"

**3.14 Suspension criteria and resumption criteria.** *Suspension criteria* define when testing must be **paused** (for example, "the login page does not load, so nothing else can be tested" or "more than 30% of executed tests fail on the same basic function"). *Resumption criteria* define when testing may **restart** (for example, "a new build is deployed and the smoke test passes"). Like a fire alarm during a school trip: everyone stops, and the visit only resumes when the area is declared safe.

**3.15 Risks and mitigation.** *Question: what could go wrong and what will we do about it?* Each risk gets a description, a likelihood, an impact, and a mitigation (an action to reduce the risk) or contingency (a backup action if it happens).

**3.16 Assumptions and dependencies.** An *assumption* is something we believe is true but have not confirmed ("the QA environment will be stable"). A *dependency* is something we rely on another team or system for ("the email service must be configured so confirmation emails arrive"). Writing these down turns hidden problems into visible, trackable items.

**3.17 Deliverables.** *Question: what will testing produce?* Test plan, test cases, execution logs, defect reports, daily status reports, traceability matrix, and the test closure report.

**3.18 Approvals.** Who must review and sign the plan: for example the product owner, the development lead, and the QE lead, with signature or approval dates. Approvals mean everyone agreed *before* work began.

At first, this list may look long. Do not worry. Many sections are a sentence or two, and you will see a complete example for Project 1 later in this lesson.

#### 4. Risk-based prioritization: where should we spend limited time?

In a perfect world we would test everything exhaustively. In reality, time and people are limited. (You will study why exhaustive testing is impossible tomorrow, in the testing principles lesson.) So we must decide **what to test first and most deeply**. The answer is **risk-based testing**.

A **risk** is a possible problem that might happen in the future and would hurt the project or product. To rate a risk we look at two things:

- **Likelihood**: how probable is it that a failure happens? (Complex code, new technology, a junior developer, and frequent changes raise the likelihood.)
- **Impact**: how bad is it if it does happen? (Lost money, lost data, security breach, legal trouble, angry customers.)

A simple rating scale is 1 (low), 2 (medium), 3 (high) for each. The **risk score** is:

> Risk score = Likelihood x Impact

| | Impact 1 (Low) | Impact 2 (Medium) | Impact 3 (High) |
|---|---|---|---|
| **Likelihood 3 (High)** | 3 - Medium | 6 - High | 9 - Critical |
| **Likelihood 2 (Medium)** | 2 - Low | 4 - Medium | 6 - High |
| **Likelihood 1 (Low)** | 1 - Low | 2 - Low | 3 - Medium |

Scores of 6 to 9 get the earliest and deepest testing. Scores of 3 to 4 get normal testing. Scores of 1 to 2 get light testing, or are tested last if time allows.

**Worked example for the Registration and Login feature:**

| Feature area | Likelihood (1-3) | Impact (1-3) | Score | Priority |
|---|---|---|---|---|
| Login with valid credentials | 2 (core, but simple) | 3 (nobody can use the app if broken) | 6 | High |
| Account lockout after failed attempts | 3 (timers and counters are tricky) | 3 (security issue if it fails) | 9 | Critical |
| Password rule validation | 3 (many rules, easy to miss one) | 2 (weak passwords accepted) | 6 | High |
| Duplicate email detection | 2 | 3 (two accounts, data integrity) | 6 | High |
| Confirmation email wording | 1 | 1 | 1 | Low |
| Page layout on a small phone | 2 | 1 | 2 | Low |

The result is a prioritized order of testing. If the schedule is cut by half, you still cover the critical areas first. This is how professional testers answer a manager who says, "We only have two days left. What do you test?"

Note that risk ratings are **judgments**, not exact science. Discuss them with developers and the product owner, because they know where the code is complicated and where the business would hurt most.

#### 5. Estimation techniques: how long will testing take?

**Estimation** means predicting the effort (person-hours or person-days) and the duration (calendar time) required. Estimates are always uncertain, but you should still give them with reasons. Four beginner-friendly techniques follow.

**5.1 Work Breakdown Structure (WBS).** Break the big job into small tasks, estimate each small task, then add them up. Small tasks are easier to estimate accurately than one big lump.

| Task for Login/Registration testing | Estimate (hours) |
|---|---|
| Review requirements and write test conditions | 6 |
| Write 40 test cases (about 15 minutes each) | 10 |
| Peer review and fix test cases | 4 |
| Prepare test data and environment checks | 4 |
| Smoke test on each new build (2 builds x 0.5 h) | 1 |
| Execute 40 test cases, first cycle (about 12 minutes each) | 8 |
| Log defects and write defect reports (about 8 defects x 0.5 h) | 4 |
| Retest fixes and run regression subset | 6 |
| Daily status reports (6 days x 0.5 h) | 3 |
| Test closure report | 2 |
| **Total** | **48 hours** |

At 6 productive hours per person per day (people do not spend all 8 hours testing; there are meetings and breaks), 48 hours is 8 person-days. With 2 testers that is about 4 calendar days, plus a buffer.

**5.2 Three-point estimation and PERT.** Instead of one guess, give three:

- **O** = Optimistic (everything goes well)
- **M** = Most likely (a normal outcome)
- **P** = Pessimistic (many things go wrong)

The **PERT** (Program Evaluation and Review Technique) weighted average is:

> Estimate E = (O + 4M + P) / 6

and the standard deviation (a measure of uncertainty) is:

> SD = (P - O) / 6

Example: test execution of the login feature could take 2 days at best, 4 days most likely, and 9 days at worst (for example, if the environment is unstable).

E = (2 + 4x4 + 9) / 6 = (2 + 16 + 9) / 6 = 27 / 6 = **4.5 days**

SD = (9 - 2) / 6 = 7 / 6 = about **1.17 days**

So you might tell your manager: "About 4.5 days, give or take just over one day. I would commit to 5.5 to 6 days to be safe." (Adding one SD to the estimate gives roughly 5.7 days.) Note how the pessimistic value pulls the average upward from the "most likely" 4 days. That reflects reality: things usually take longer than we hope.

**5.3 Experience-based estimation.** Use what happened on similar past projects or ask experienced colleagues. "Last release, the checkout feature had 55 test cases and took 3 days with 2 testers. Login is about the same size." Very practical, but only as good as the memory and the similarity of the past work. A structured form of this is the **Wideband Delphi** or **planning-poker-style** method: several experts estimate independently, then discuss differences and re-estimate until they converge.

**5.4 Story points in Agile.** In Scrum teams, work items (user stories) are not usually estimated in hours but in **story points**, a relative measure of size that combines effort, complexity, and uncertainty. The team compares a new story to reference stories ("this is about twice as hard as the login story, which we gave 3 points, so give it 5 or 8"). Many teams use the Fibonacci-like scale 1, 2, 3, 5, 8, 13. Testing effort is included in the story's points: the story is only "done" when it is tested. Over a few sprints, the team learns its **velocity** (average points completed per sprint) and can forecast how many stories fit into the next sprint. Testers take part in **planning poker**, and their voice is vital, because developers often forget how much test effort a story needs.

A quick reference:

| Technique | Best used when | Weakness |
|---|---|---|
| Work breakdown | Scope is reasonably known | Time-consuming; tasks may be forgotten |
| Three-point / PERT | Uncertainty is high | Still depends on honest O, M, P guesses |
| Experience-based | Similar past work exists | Memory is imperfect; every project differs |
| Story points | Agile teams with stable velocity | Relative, not in hours; needs team history |

**A practical rule:** always add a **buffer** (often 10 to 20 percent) for the unexpected, and always state your assumptions with the estimate ("assuming the environment is stable and 8 builds or fewer").

#### 6. Test levels overview (brief)

A **test level** is a group of test activities organized and managed together, matched to a stage of building the software. You can imagine the product being built like a car: first parts, then assemblies, then the whole car, then the customer's test drive.

| Level | What is tested | Typically done by | Example for login |
|---|---|---|---|
| **Unit (component) testing** | The smallest pieces of code (functions, classes) in isolation | Developers | A function that checks "is this password at least 8 characters?" returns false for "abc123" |
| **Integration testing** | How units/modules/systems work together; interfaces and data flow | Developers and testers | The registration form correctly saves the user into the database, and the email service receives the request |
| **System testing** | The complete, integrated application against the requirements, in a production-like environment | Independent testers (QE team) | A user can register, confirm, log in, get locked out after 5 failures, and log out, using the real UI |
| **Acceptance testing (UAT)** | Whether the system meets business needs and is ready for use; validation by users or customers | Business users, product owner, customers (QE assists) | The product owner confirms that a real new customer can sign up in under two minutes |

**Verification** asks "Are we building the product right?" (conformance to specification), while **validation** asks "Are we building the right product?" (fitness for the user's need). Unit, integration, and system testing lean toward verification; acceptance testing leans toward validation.

**Test types** (different from levels) describe the quality characteristic being checked. Brief definitions:

- **Functional testing**: does it do what it should? (Registering creates an account.)
- **Non-functional testing**: how well does it do it? Includes performance (speed), usability (ease of use), security, compatibility (different browsers/devices), and reliability.
- **Regression testing**: did a change break something that used to work? (Friday's topic.)
- **Smoke and sanity testing**: quick health checks (introduced below).
- **Retesting (confirmation testing)**: did the reported defect get fixed? (Introduced below.)

In the Project 1 plan, we focus on system-level functional testing with some basic security and compatibility checks, and we rely on developers' unit tests and integration tests as the earlier safety nets.

#### 7. The lightweight test plan in Agile

Agile teams value "working software over comprehensive documentation." That does not mean "no plan." It means **just enough planning**. In a two-week sprint nobody will read a 30-page document, and it would be out of date in three days.

A **one-page test plan** is a popular solution. It fits on a single page (or a single Confluence/Jira page) and answers the essentials:

| Section | One-line content |
|---|---|
| Goal | What quality outcome do we want this sprint/release? |
| Scope | In and out, as short bullet lists |
| Approach | Manual or automated, which test types, risk focus |
| Environment and data | Where and with what |
| Roles | Who tests, who fixes, who decides |
| Schedule | Key dates inside the sprint |
| Entry and exit (Definition of Ready and Definition of Done) | Short list of conditions |
| Top risks | Three to five, with mitigation |
| Reporting | Daily stand-up update, board status, sprint review demo |

In Scrum, the **Definition of Done (DoD)** often acts as the exit criteria: "code reviewed, unit tests pass, acceptance criteria tested, no open critical defects, documentation updated." Planning happens at **sprint planning**, progress is shared at the **daily scrum**, and results are reviewed at the **sprint review** and **retrospective** (all learned yesterday). The tester's plan lives close to the board: test tasks appear as sub-tasks on the Jira story.

Use a full formal plan when the project is large, regulated, contractual, or involves many teams. Use a one-page plan when the team is small and the iterations are short. Many organizations use both: a **master test plan** for the release and a **one-page plan per sprint or feature**.

#### 8. Test case basics

**8.1 What is a test case?**

A **test case** is a set of conditions, inputs, and steps, together with an **expected result**, used to check one particular behavior of the software. If the **test plan** is the trip itinerary, a **test case** is one line on your checklist: "Check that the passport is in the bag." It is a repeatable, documented question that has a clear right answer.

Why write test cases instead of just clicking around?

- **Repeatability**: anyone can run the same test and get comparable results.
- **Coverage**: you can show which requirements are checked.
- **Training**: a new tester can learn the product by running the cases.
- **Evidence**: the record of what was checked and the result.
- **Regression**: the same cases can be rerun after each change.

(Clicking around without a script is also valuable. It is called **exploratory testing**. It complements, but does not replace, planned test cases.)

**8.2 Standard test case fields**

| Field | Meaning | Example |
|---|---|---|
| **Test Case ID** | Unique identifier so everyone can refer to it | TC-REG-001 |
| **Title / Summary** | One short sentence saying what is verified | Register a new user with valid details |
| **Requirement reference** | Which requirement this covers (traceability) | REQ-01, REQ-05 |
| **Preconditions** | What must be true **before** step 1 | App is reachable; email not already registered |
| **Steps** | Numbered actions to perform | 1. Open /register 2. Enter... 3. Click "Create account" |
| **Test data** | Specific inputs to use | Email: new.user01@example.com; Password: Secure#2024 |
| **Expected result** | What should happen if the software is correct | Account created; message "Check your email to confirm"; confirmation email sent |
| **Actual result** | What really happened when executed | (filled during execution) |
| **Status** | Result of the latest execution | Pass / Fail / Blocked / Skipped / Not Run |
| **Priority** | How important to run (High/Medium/Low), often from risk | High |
| **Other optional fields** | Author, date, environment, build number, type (functional/negative), automation status, linked defect ID | |

Two terms to separate: **precondition** (the state *before* the test starts, such as "user is logged out") and **test data** (the specific values you type or use). A third idea, **postcondition**, is the state the system should be in after the test (for example, "one new user row exists in the database").

**8.3 Good versus poor test cases**

A good test case is **clear, specific, independent (or clearly dependent), repeatable, traceable, and has a verifiable expected result.**

Poor example:

| Field | Content |
|---|---|
| ID | 1 |
| Title | Test login |
| Steps | Try to log in |
| Expected result | It works |

Why is this poor? The title is vague. No preconditions. No data: which user, which password? The steps do not say where to go. "It works" cannot be verified: what does "works" look like? Two testers would run it two different ways and might disagree about the result.

Good example:

| Field | Content |
|---|---|
| ID | TC-LOG-001 |
| Title | Login succeeds with valid, confirmed account credentials |
| Requirement | REQ-06 |
| Priority | High |
| Preconditions | 1. Application is available at the QA URL. 2. User "login.user01@example.com" exists, is confirmed, and is not locked. 3. User is logged out. |
| Steps | 1. Open the Login page. 2. Enter email "login.user01@example.com". 3. Enter password "Secure#2024". 4. Click the "Log in" button. |
| Test data | Email: login.user01@example.com; Password: Secure#2024 |
| Expected result | User is redirected to the Dashboard page; the header shows "Welcome, Login User"; a "Log out" link is visible. |

Qualities to copy:

- **One clear purpose** per test case. If a test checks five different things and fails, you will not know which thing broke.
- **Precise steps** that any teammate can follow without guessing.
- **Observable expected results**: URL, message text, field state, data saved. Avoid "should work properly" or "appropriate message".
- **Independent where possible**: do not make TC-005 depend on TC-004 having been run unless the dependency is stated in preconditions.
- **Short and maintainable**: avoid 30-step monsters.
- **Both positive and negative**: positive tests use valid input and check normal behavior; **negative tests** use invalid input or unusual actions and check that the system handles them safely (a clear error message, no crash, no data corruption).

(How to *choose* the inputs for these cases systematically, with techniques such as equivalence partitioning and boundary value analysis, is the topic of Thursday's lesson. Today the test data is simply given to you.)

**8.4 Test suites and test cycles**

- A **test suite** is a **collection of test cases grouped for a purpose**. Examples: "Registration suite", "Login suite", "Smoke suite" (the few most important checks), "Regression suite" (cases rerun after each change). Think of suites as folders or playlists. One test case can belong to more than one suite.
- A **test cycle** (also called a test run or test execution cycle) is **one round of execution** of a set of test cases against a specific build in a specific period. "Cycle 1: executing the Registration and Login suites on Build 1.0.3, from Monday to Wednesday." After defects are fixed and a new build arrives, **Cycle 2** begins, and so on. The same test case can therefore have a separate result in each cycle.

In a tool such as Jira with a test-management add-on (Xray, Zephyr), or TestRail, you create the test cases once in a repository, group them into suites or test sets, and then create a **test execution** or **test run** for each cycle, with results stored per cycle.

---

### Part B: Test Execution

**Test execution** is the phase where testers run the planned tests on the actual software, compare actual results to expected results, record the outcome, and report defects. If planning is writing the itinerary and packing the bag, execution is actually taking the trip and writing down what happened at each stop.

#### 9. Execution prerequisites and entry criteria check

Before running a single test, confirm the **entry criteria** from the plan. Starting execution on an unready build wastes everyone's time. A typical checklist:

| Prerequisite | Check |
|---|---|
| Requirements are baselined (agreed and stable) | Yes / No |
| Test cases are written, reviewed, and approved | Yes / No |
| Test environment is available and configured | Yes / No |
| Test data is created and loaded | Yes / No |
| The build is deployed, and its version number is known | Yes / No |
| Access (accounts, VPN, permissions) is granted | Yes / No |
| Defect tracker and test-management tool are ready | Yes / No |
| Smoke test on the build has passed | Yes / No |

If an item is "No", report it right away to the test lead, instead of discovering it halfway through the day.

#### 10. Smoke and sanity checks (introduction)

- A **smoke test** is a **quick, shallow check of the most critical functions** of a new build to decide whether the build is stable enough for deeper testing. The name comes from hardware: turn on the new circuit board, and if smoke comes out, stop immediately. In software, ask: Does the app start? Does the login page load? Can I reach the main screen? A smoke test usually takes 15 to 30 minutes, covers the main flows broadly but shallowly, and ends in a simple decision: **accept the build for testing, or reject it** and send it back to the developers.
- A **sanity test** is a **narrow, focused check after a small change or bug fix** to confirm that the specific change works and nothing obviously related is broken, before spending time on full testing. Example: after a fix to the password error message, quickly check that message and the surrounding form, instead of running the whole suite.

| | Smoke test | Sanity test |
|---|---|---|
| Scope | Broad and shallow | Narrow and deeper in one area |
| When | On every new build | After a minor fix or small change |
| Purpose | Is the build testable at all? | Does the specific fix/change behave sensibly? |
| Typical outcome | Accept or reject the build | Proceed to detailed testing or send back |
| Scripted? | Often scripted and often automated | Often unscripted/quick |

(People sometimes use these two words loosely, and some books define them slightly differently. Learn the idea and check which meaning your team uses.)

A sample **smoke suite for Project 1**:

1. The application URL loads without error.
2. The Registration page opens.
3. The Login page opens.
4. A pre-created valid user can log in and reach the Dashboard.
5. The user can log out.

If any of these fails, stop and report: "Build rejected: smoke test failed."

#### 11. Test environment readiness

A **test environment** is the combination of hardware, software, network, data, and configuration in which testing happens. A shaky environment produces **false failures** (tests fail not because the software is wrong, but because the environment is wrong), which wastes time and erodes trust in testers.

Environment readiness checklist for Project 1:

| Item | Verify |
|---|---|
| Correct application version (build number visible in the footer or about page) | Matches the build announced by the developers |
| Database | Reachable; seeded with test users; no leftover data from earlier runs that conflicts |
| Email service | A test mailbox (or a "mail catcher" tool) receives confirmation emails |
| Browsers and devices | Required browser versions installed; screen sizes available |
| Network and URLs | QA URL reachable; no firewall block |
| Configuration | Lockout threshold and timers set to the specified values (or a test-friendly short value that is documented) |
| Accounts and access | Tester accounts and admin tools accessible |
| Monitoring and logs | Testers can read application logs or ask someone to |

A good habit: record the **environment details in every execution** (build number, browser and version, OS, date). When a developer asks, "Which build was that on?", you can answer immediately.

#### 12. Executing test cases step by step

The execution routine for each test case is simple and disciplined:

1. **Select** the next test case (in priority order from the plan: highest risk first).
2. **Confirm the preconditions.** Set up the user, data, and starting state.
3. **Follow the steps exactly** as written, using the stated test data. Do not "improve" the steps mid-run. If the steps are wrong or unclear, finish what you can, then raise a test case correction.
4. **Observe carefully.** Compare *everything* the expected result mentions: message text, page, field values, data saved, email received.
5. **Record the actual result** in your own words, factually: what you saw, not what you assumed.
6. **Decide the status** (below).
7. **Capture evidence** (below).
8. **If it failed, log a defect** and link it to the test case.
9. **Move on** to the next case, and update your progress.

A tip on mindset: be **honest and neutral**. A failed test is not bad news for you. It is the system working as intended: you found a problem before the customer did. Do not mark a test as passed because you are in a hurry, and do not mark it failed because you dislike the design. Compare to the **expected result** from the requirement, and when the requirement itself is unclear, ask.

#### 13. Recording results: the five statuses

| Status | Meaning | Example |
|---|---|---|
| **Pass** | Actual result matches the expected result for every check in the test case | The user logged in and reached the Dashboard as expected |
| **Fail** | Actual result differs from the expected result in at least one way | A 6-character password was accepted although the minimum is 8 |
| **Blocked** | The test **cannot be executed** because something outside the test prevents it (an open defect, missing environment, missing data, or a dependency not ready) | The lockout test cannot run because the QA environment's lockout setting is unavailable; or Login cannot be tested because registration fails |
| **Skipped** | The test was **deliberately not executed** for this cycle, with a reason (descoped, not applicable, deferred by decision) | The test applies to a browser that is no longer supported |
| **Not Run** (also "Not Executed", "Unexecuted", "To Do") | The test is planned but **has not been attempted yet** | Waiting its turn in the queue |

Be careful with **Blocked versus Fail**. A *Fail* means you ran the test and the software behaved wrongly. A *Blocked* test never reached the point of checking the behavior. Mixing them up distorts the metrics and hides the true picture.

Some tools add other statuses such as "In Progress" or "Passed with comments". Use only those your team has agreed on.

#### 14. Evidence: proving what happened

**Evidence** is any material that proves what you did and saw. It makes defects reproducible and shows auditors that tests were truly run.

| Evidence type | Use | Tips |
|---|---|---|
| **Screenshot** | Shows the visual state, such as an error message | Capture the whole screen, including the URL bar and clock if possible; annotate (arrow or box) the problem; never include real personal data |
| **Screen recording / video** | Shows a sequence of steps or intermittent issues | Keep it short, about 30 to 90 seconds; show the steps from the start |
| **Logs** | Application or server logs, browser console errors, network requests (from browser developer tools) | Copy the relevant lines with timestamps; do not paste thousands of lines |
| **Test data used** | The exact input values | Include in the defect and in the actual result |
| **Environment info** | Build, browser, OS, URL, date and time | Always |
| **Database or email proof** | A record created, or the email received | Mask sensitive data |

Name files meaningfully: `TC-REG-003_6char-password-accepted_2026-03-04.png`, not `Screenshot (17).png`.

#### 15. Logging defects when actual differs from expected

When a test **fails**, you have found a potential **defect** (also called a bug, issue, or fault: a flaw in the software that causes it to behave differently from what is required). Do these immediately while the details are fresh:

1. **Re-try once** (to see if it is reproducible, and to rule out a typing mistake or a data issue).
2. **Check it is not a known issue** (search the defect tracker for duplicates).
3. **Log a defect** in the tracker (Jira) with a clear title, steps to reproduce, expected versus actual result, environment and build, severity and priority suggestion, and attached evidence.
4. **Link** the defect ID to the failing test case (for example "Failed - DEF-101"), so everyone sees the connection.

A simple defect summary line might read: "DEF-101: Registration accepts 6-character password although minimum is 8 (REQ-03)". How to write a great defect report, what severity and priority mean, and the journey of a defect through New, Assigned, Fixed, Retest, Closed, and so on, are covered in detail in **the next lesson, the Defect Lifecycle**. For today, just remember the principle: **every failed test deserves a traceable defect, and every defect deserves evidence.**

#### 16. Retesting versus regression testing (brief introduction)

After a developer fixes a defect and a new build arrives, two different checks are needed:

- **Retesting (confirmation testing)** means re-running **the exact test case that failed** to confirm that the defect is now fixed. Question: "Is the thing that was broken now working?"
- **Regression testing** means re-running **other, previously passing tests** to confirm that the fix or any change **did not break something else**. Question: "Did the fix damage anything that used to work?"

Analogy: a mechanic fixes your car's brakes. *Retesting* is pressing the brake pedal to confirm that braking now works. *Regression testing* is checking that the lights, steering, and engine still work after the mechanic worked in that area.

| | Retesting | Regression testing |
|---|---|---|
| Purpose | Confirm a specific fix | Detect unintended side effects |
| Test cases | The ones that failed | Previously passed, related or broader set |
| Timing | After the defect is fixed | After any change (fix, new feature, configuration) |
| Predictable? | Yes, exactly the failed cases | Selected by risk and impact; often automated |

Selection of regression tests, regression suites and automation strategies are explored in depth on **Friday**. In today's planning, you simply reserve time for both in each cycle.

#### 17. Test progress tracking

While executing, you constantly answer: **"Are we on track?"** Track:

- How many tests are planned, executed, passed, failed, blocked, skipped, not run.
- How many defects are found, open, fixed, and retested, and their severities.
- Effort spent versus planned.
- Planned versus actual progress per day (an **execution burn-up** chart is common: the line of "tests executed" should rise toward the total).

Update the status of every test in the tool **as you finish it**, not at the end of the day, so the dashboard always shows the truth.

Compare **actual to plan** daily. If you planned 10 tests per day per tester and you are doing 6, you are falling behind. Raise it early.

#### 18. The daily status report

The **daily status report** (or daily test summary) is a short message to the team and stakeholders about the day's testing. It builds trust: no surprises. It should be **brief, factual, honest, and focused on what is needed from others**. Typical contents: period and build, planned vs. executed, results, new defects, blockers, risks, plan for tomorrow, help needed.

**Template:**

```
DAILY TEST STATUS REPORT
Project / Feature : ______________________   Date : ________
Build / Environment : ____________________   Prepared by : ________
Test cycle : _____

1. SUMMARY (one or two sentences)
   Overall status: GREEN (on track) / AMBER (at risk) / RED (off track)

2. EXECUTION PROGRESS (today / cumulative)
   Total planned | Executed | Passed | Failed | Blocked | Skipped | Not Run
   Execution % : ____    Pass % : ____

3. DEFECTS
   New today | Total open | Critical | High | Medium | Low | Fixed awaiting retest

4. BLOCKERS AND ISSUES (what, since when, who can help)

5. RISKS (new or changed)

6. ACTIVITIES COMPLETED TODAY

7. PLAN FOR TOMORROW

8. HELP / DECISIONS NEEDED
```

**Filled example (Project 1):**

```
DAILY TEST STATUS REPORT
Project / Feature : Project 1 - User Registration and Login   Date : Wed 04 Mar 2026
Build / Environment : v1.0.3 / QA                              Prepared by : A. Rivera
Test cycle : Cycle 1 (Day 3 of 4)

1. SUMMARY
   Registration suite complete. Login suite 60% done. One test blocked by an
   environment setting. Overall status: AMBER.

2. EXECUTION PROGRESS (cumulative)
   Total 40 | Executed 30 | Passed 26 | Failed 4 | Blocked 2 | Skipped 0 | Not Run 8
   Execution % : 75%    Pass % : 86.7% (of executed)

3. DEFECTS
   New today: 2 | Total open: 5 | Critical 0 | High 2 | Medium 2 | Low 1 | Awaiting retest: 1

4. BLOCKERS
   - TC-LOG-003 (lockout) and TC-LOG-007 (lockout timer) blocked: lockout threshold
     in QA is set to 50, not 5. Raised with DevOps (ticket OPS-212) on Tue 3 Mar.

5. RISKS
   - If the lockout setting is not corrected by Thu noon, the two highest-risk
     security tests cannot finish in Cycle 1.

6. COMPLETED TODAY
   - Executed 12 tests, logged DEF-103 and DEF-104, retested DEF-101 (fixed, closed).

7. PLAN FOR TOMORROW
   - Execute the remaining 8 Login tests, retest DEF-103, run smoke on build 1.0.4.

8. HELP NEEDED
   - DevOps: fix the lockout setting by Thu 10:00.
   - Dev lead: confirm target date for DEF-104 fix.
```

Notice that the report states **what is needed from whom, and by when**. A good status report is a request for action, not just a diary.

#### 19. Test metrics: measuring progress and quality

A **metric** is a measurable value that describes some aspect of testing or product quality. Metrics answer management questions such as "How far along are we?" and "How good is the product, and how good is our testing?" Always remember: **a number without context can mislead**. Use metrics as conversation starters, not as weapons against people.

Let us define five essential metrics, with formulas.

**19.1 Test execution percentage** (progress)

> Execution % = (Number of tests executed / Total number of planned tests) x 100

"Executed" usually means tests that reached a Pass or Fail result. (Blocked, Skipped, and Not Run tests have not been executed.)

**19.2 Pass percentage** (quality indicator of the product at this moment)

> Pass % = (Number of tests passed / Number of tests executed) x 100

(Some teams divide by total planned tests instead. State your definition in the plan so everyone reads the numbers the same way.)

**19.3 Defect density** (quality of the code relative to its size)

> Defect density = Number of confirmed defects / Size of the software

Size is measured as thousand lines of code (KLOC), function points, number of requirements, or number of user stories. A higher density suggests a more troubled area.

**19.4 Defect leakage** (defects that escaped testing)

> Defect leakage % = (Defects found after release or in a later phase such as UAT/production / (Defects found during testing + Defects found after release)) x 100

It measures how many defects "leaked" past the testing phase to users. Lower is better.

**19.5 Defect Detection Percentage (DDP)** (effectiveness of testing)

> DDP % = (Defects found during testing / (Defects found during testing + Defects found after release)) x 100

Note: **DDP = 100% - Defect leakage %**. They are two views of the same fact. A higher DDP means testing caught more of the defects that existed.

**Worked numeric example.**

The system testing of Project 1 for the release ends with these numbers:

| Item | Value |
|---|---|
| Total planned test cases | 120 |
| Passed | 90 |
| Failed | 12 |
| Blocked | 6 |
| Skipped | 4 |
| Not Run | 8 |
| Check: 90 + 12 + 6 + 4 + 8 | 120 (correct) |
| Defects found during testing | 45 |
| Size of the code under test | 15 KLOC |
| Defects found by UAT users and in the first month after release | 5 |

*Step 1 - Executed tests:* Passed + Failed = 90 + 12 = **102**.

*Step 2 - Execution %:* 102 / 120 x 100 = 0.85 x 100 = **85%**.

*Step 3 - Pass %:* 90 / 102 x 100 = 0.88235... x 100 = **88.2%** (rounded to one decimal). If your team defines it against all planned tests: 90 / 120 x 100 = 75%. Say which one you are using.

*Step 4 - Defect density:* 45 defects / 15 KLOC = **3.0 defects per KLOC**. (If sized by requirements instead: with 10 requirements, 45 / 10 = 4.5 defects per requirement.)

*Step 5 - Defect leakage:* 5 / (45 + 5) x 100 = 5 / 50 x 100 = **10%**.

*Step 6 - DDP:* 45 / (45 + 5) x 100 = 45 / 50 x 100 = **90%**. Check: 100% - 10% = 90%. Correct.

*Interpretation:* Testing is 85% complete in terms of execution, and 88.2% of what has run passed. The team found 3 defects per thousand lines, and testing caught 90% of the known defects, with 10% escaping. The 6 blocked tests and 8 not-run tests are a worry: they represent unknown quality. A responsible tester would say, "The pass rate looks healthy, but 14 tests (11.7%) still give us no information, so I cannot recommend release yet." That is the difference between reading numbers and understanding them.

A warning about **vanity metrics**: a high number of test cases executed or defects found is not automatically good. Measure outcomes, not just activity, and never reward testers for the *count* of bugs (it encourages splitting one bug into five).

#### 20. Traceability: linking tests back to requirements

**Traceability** is the ability to follow a link from a requirement to the tests that check it, and on to the defects found. The tool for this is the **Requirements Traceability Matrix (RTM)**, a table mapping requirements to test cases (and often to defects).

Why does traceability matter?

- **Coverage proof**: every requirement has at least one test. A requirement with no tests is a gap.
- **Impact analysis**: when a requirement changes, you can see instantly which tests must be updated.
- **Reporting**: you can say "8 of 10 requirements are fully passed."
- **Audit**: regulators and clients can see a complete chain.

Part of the RTM for Project 1:

| Requirement | Description | Test Cases | Status | Defects |
|---|---|---|---|---|
| REQ-01 | Register with email, password, confirm password | TC-REG-001 | Pass | - |
| REQ-02 | Email format is validated | TC-REG-004 | Pass | - |
| REQ-03 | Password must be 8+ chars with upper, lower, digit | TC-REG-003 | Fail | DEF-101 |
| REQ-04 | Duplicate email rejected | TC-REG-002 | Pass | - |
| REQ-05 | Confirmation email sent after registration | TC-REG-001 | Pass | - |
| REQ-06 | Login with valid credentials | TC-LOG-001 | Pass | - |
| REQ-07 | Invalid login shows a generic error message | TC-LOG-002 | Pass | - |
| REQ-08 | Lock account for 15 min after 5 failed attempts | TC-LOG-003 | Blocked | - |
| REQ-09 | Logout ends the session | TC-LOG-004 | Not Run | - |

Reading this table you can say instantly: "REQ-03 has a failed test; REQ-08 is blocked; REQ-09 has not yet been tested; the other six requirements are verified."

#### 21. Handling blocked tests and schedule slippage

Real projects never run perfectly. Two situations appear in almost every cycle.

**Blocked tests.** When a test cannot be executed:

1. **Confirm it is truly blocked** (not just a missed precondition).
2. **Identify the cause** and the owner (environment, defect, data, access).
3. **Mark it Blocked** and record the reason and linked defect or ticket ID.
4. **Escalate the blocker** the same day to the test lead (and to whoever can fix it). Do not wait quietly.
5. **Reorder the work.** Run unblocked tests first, so you stay productive. Idle time is the enemy.
6. **Re-test the blocked cases** as soon as the block is removed, and reflect the delay in the status report and the risk list.
7. If many tests are blocked by the same cause, check the **suspension criteria**: you may need to formally pause testing.

**Schedule slippage.** When the timeline is at risk (late build, many defects, blocked tests, sick team members):

1. **Detect early** by comparing planned versus actual progress each day.
2. **Report early and honestly.** Surprises at the last minute destroy trust. Say: "At the current rate we will finish on 12 March instead of 10 March."
3. **Re-prioritize using risk.** Run the highest-risk tests first. Defer low-risk ones.
4. **Offer options** to the manager: add a tester, reduce the scope (with product owner agreement), extend the date, run some tests in parallel, or accept a stated risk. Present the **trade-offs**, and let the decision-makers decide.
5. **Do not silently cut corners.** Never mark tests as passed without running them, or skip evidence to "catch up".
6. **Update the plan and the risk list**, and record the lesson learned for the retrospective.

#### 22. Test closure and the exit (summary) report

**Test closure** is the final activity of the testing phase. You verify that the exit criteria are met, finish the documents, archive everything, and learn lessons. The key deliverable is the **test closure report** (or **test summary report** or **exit report**). It tells decision-makers: what was tested, what was found, what remains, and whether testing recommends release.

Typical closure activities:

- Check that all planned tests are executed (or have an agreed reason for not being executed).
- Confirm all defects are closed, or deferred with the approval of the product owner.
- Compare results with the exit criteria.
- Archive test cases, data, scripts, environment configuration, and results for reuse.
- Hold a **lessons-learned** discussion (a retrospective).
- Obtain sign-off.

**Sample test closure report (Project 1):**

```
TEST CLOSURE (EXIT) REPORT
Document ID   : TCR-P1-LOGIN-v1.0
Project       : Project 1 - User Registration and Login, Release 1.0
Test period   : 02 Mar 2026 to 10 Mar 2026
Prepared by   : A. Rivera (QE)         Reviewed by : S. Patel (QE Lead)

1. SCOPE TESTED
   Requirements REQ-01 to REQ-09, system-level functional testing on Chrome
   and Firefox (latest versions), Windows 11. Out of scope: password reset,
   social login, performance testing (see test plan TP-P1-LOGIN-v1.0).

2. BUILDS TESTED
   1.0.2 (smoke failed, rejected), 1.0.3 (Cycle 1), 1.0.5 (Cycle 2 and regression)

3. EXECUTION SUMMARY (Cycle 2 final)
   Planned 40 | Executed 40 | Passed 38 | Failed 2 | Blocked 0 | Skipped 0 | Not Run 0
   Execution % 100% | Pass % 95%

4. DEFECT SUMMARY
   Total logged 14 | Closed 11 | Deferred 2 (Low, approved by Product Owner) |
   Open 1 (Medium: DEF-109 button misaligned on 320 px screens - workaround exists)
   Critical 0 open | High 0 open
   Defect density: 14 defects / 9 requirements = 1.56 per requirement

5. EXIT CRITERIA CHECK
   100% planned tests executed                    : MET
   Pass rate at least 95%                         : MET (95%)
   No open Critical or High defects               : MET
   All Medium defects fixed or approved deferral  : MET (DEF-109 accepted)
   Traceability: every requirement has a test     : MET

6. DEVIATIONS FROM PLAN
   Cycle 1 ended one day late because the lockout configuration in QA was incorrect.

7. RISKS REMAINING
   Not tested on Safari or mobile browsers (out of scope). Email delivery tested
   against a mail catcher, not the production email provider.

8. LESSONS LEARNED
   - Verify environment configuration before Cycle 1 (add to entry criteria).
   - Involve the developer in test case review to catch ambiguity early.

9. RECOMMENDATION
   Testing recommends RELEASE of Release 1.0, subject to the Product Owner's
   acceptance of the remaining risks listed in section 7.

10. SIGN-OFF
   QE Lead: ___________  Product Owner: ___________  Dev Lead: ___________
```

Notice the report **recommends** but does not decide. Release is a business decision. The tester provides information; the stakeholders choose, knowing the risks.

#### 23. Who does what? Roles across planning and execution

| Role | Planning responsibilities | Execution responsibilities |
|---|---|---|
| **QE / Test Engineer (Tester)** | Analyze requirements, write test cases, contribute estimates, review peers' tests | Execute tests, record results and evidence, log defects, retest, update status |
| **Test Lead / QE Lead / Test Manager** | Write and own the test plan, estimate, assign tasks, manage risks, get approvals | Monitor progress, remove blockers, report to stakeholders, decide on re-prioritization, produce the closure report |
| **Developer** | Provide technical details, write unit/integration tests, review test cases for accuracy | Fix defects, deploy builds, answer questions, support reproduction |
| **Product Owner / Business Analyst** | Clarify requirements, approve scope and priorities, take part in risk discussion | Answer requirement questions, decide on defects (fix or defer), perform acceptance, and approve release |
| **Scrum Master** | Help the team plan and remove impediments | Facilitate the daily scrum; escalate organizational blockers |
| **DevOps / Environment Support** | Prepare environments and pipelines | Deploy builds, fix environment issues, provide logs |
| **End users / UAT testers** | Provide scenarios and confirm acceptance criteria | Perform acceptance testing, give feedback |

In small Agile teams, one tester may wear several of these hats. What matters is that each responsibility has an owner.

---

## Examples

### Example 1: Complete sample test plan for Project 1 - User Registration and Login

This is a full plan in the IEEE 829 / ISO 29119 spirit, sized for a small team. Use it as a model.

---

**TEST PLAN: User Registration and Login**

| Field | Value |
|---|---|
| Document ID | TP-P1-LOGIN-v1.0 |
| Project | Project 1 - QE Foundations (sample web application) |
| Feature under test | User Registration and Login |
| Release | 1.0 |
| Author | A. Rivera, QE Engineer |
| Reviewers | S. Patel (QE Lead), J. Kim (Developer), M. Okoye (Product Owner) |
| Date / Version | 02 March 2026 / v1.0 (draft for approval) |

**1. Introduction**

This document describes how the User Registration and Login feature of the Project 1 web application will be tested for Release 1.0. It follows the organization's general test strategy (manual functional testing at system level, risk-based prioritization, defects tracked in Jira) and applies it to this feature.

**2. Objectives**

- Verify that the feature meets requirements REQ-01 to REQ-09.
- Provide the team and Product Owner with reliable information about quality so that they can make a release decision.
- Find defects, especially those affecting security and the ability to log in, as early as possible.
- Confirm that no Critical or High severity defect remains open at release.

**3. Items to Be Tested (references)**

- Requirements specification "Registration and Login" v1.2 (REQ-01 to REQ-09).
- User stories US-11 (Register), US-12 (Login), US-13 (Account lockout), US-14 (Logout) in Jira.
- Application build under test: first build 1.0.2 onward, deployed to the QA environment.

**4. Scope**

*In scope:*

| ID | Feature / requirement |
|---|---|
| REQ-01 | Registration with email, password, and confirm password |
| REQ-02 | Email format validation |
| REQ-03 | Password rules: 8 or more characters, with at least one uppercase letter, one lowercase letter, and one digit |
| REQ-04 | Duplicate email is rejected |
| REQ-05 | Confirmation email sent after registration |
| REQ-06 | Login with valid, confirmed credentials |
| REQ-07 | Invalid credentials produce a generic error message (does not reveal which field was wrong) |
| REQ-08 | Account locked for 15 minutes after 5 consecutive failed login attempts |
| REQ-09 | Logout ends the session |

*Also in scope:* basic field-level error messages, basic security checks (password hidden while typing, no password shown in URL or error text), and basic compatibility on the supported browsers.

*Out of scope for Release 1.0:*

- Forgot / reset password (planned for Release 1.1).
- Social login (Google, Facebook).
- Multi-factor authentication.
- Performance and load testing.
- Mobile native apps and Safari browser.
- Penetration testing (covered by a separate security team).
- Testing of the third-party email provider's internals.

**5. Test Approach**

- **Level and type:** system-level functional testing, primarily manual, with some negative and basic security and compatibility checks. Unit and integration tests are the developers' responsibility; their results are reviewed during planning.
- **Test design:** test cases are written from requirements and user-story acceptance criteria (formal design techniques such as equivalence partitioning and boundary value analysis are applied during test design, from the techniques learned this week). Both positive and negative cases are included.
- **Risk-based prioritization:** each requirement is scored by likelihood x impact. Highest scores (REQ-08 lockout: 9; REQ-03, REQ-04, REQ-06: 6) are tested first. See the risk table in section 15.
- **Execution:** two cycles planned. Cycle 1 covers all test cases on the first accepted build. Cycle 2 covers retests of fixed defects plus a regression subset on the newest build.
- **Smoke test:** a five-case smoke suite is run on every new build before deeper testing.
- **Defect management:** all defects are logged in Jira (project key DEF), linked to the failing test case, with evidence. Lifecycle and severity rules follow the team's defect management process.
- **Reporting:** daily status report posted to the team channel at 16:30; metrics reported are execution %, pass %, defect counts by severity, and blocked tests.
- **Traceability:** a requirements traceability matrix is maintained, linking REQ to test cases to defects.

**6. Test Levels and Types Overview**

| Level / type | Responsible | Covered in this plan? |
|---|---|---|
| Unit testing | Developers | No (inputs reviewed only) |
| Integration testing | Developers and QE | Partly (registration to database to email) via system tests |
| System testing | QE | Yes (main focus) |
| Acceptance testing (UAT) | Product Owner and business users | Supported: entry requires QE exit report |
| Functional, negative | QE | Yes |
| Security (basic), compatibility (basic) | QE | Yes |
| Retesting | QE | Yes |
| Regression | QE | Yes, selected subset (full strategy on Friday) |
| Performance, penetration | Not in this release | No |

**7. Test Environment**

| Item | Detail |
|---|---|
| Environment name | QA (separate from DEV and STAGING) |
| Application URL | https://qa.project1.example.com |
| Operating system | Windows 11 (primary), macOS (secondary) |
| Browsers | Chrome (latest), Firefox (latest) |
| Database | QA database, reset to a baseline on request |
| Email | Test mailbox via a mail-catcher tool (all emails from QA go there, none to real addresses) |
| Configuration | Lockout threshold 5 attempts, 15 minutes (a short-timer test setting may be requested for lockout expiry tests) |
| Owner / support | DevOps (D. Chen), request via ticket in Jira OPS project |
| Availability | Monday to Friday, 08:00 to 20:00 |

**8. Test Data**

- Five pre-created users: three confirmed and active, one unconfirmed, one locked, as listed in the shared test data sheet.
- Fresh, unique email addresses for registration tests (pattern: `new.user<nn>@example.com`).
- Password sets: valid, too short, missing uppercase, missing digit.
- All data is **synthetic**. No real personal data is used.
- Data is reset to baseline at the start of each cycle. Owner: QE Engineer.

**9. Roles and Responsibilities**

| Role | Name | Responsibility |
|---|---|---|
| QE Lead | S. Patel | Approve plan, review test cases, manage escalation, sign closure report |
| QE Engineer | A. Rivera | Write and execute test cases, log defects, daily reports, closure report |
| Developer | J. Kim | Fix defects, deploy builds, answer technical questions |
| Product Owner | M. Okoye | Clarify requirements, decide defect priority and deferral, UAT acceptance |
| DevOps | D. Chen | Environment setup and fixes |
| Scrum Master | L. Torres | Remove impediments; facilitate the daily scrum |

**10. Schedule and Milestones**

| Milestone | Planned date |
|---|---|
| Test plan approved | Mon 02 Mar |
| Test cases written and reviewed | Tue 03 Mar |
| Environment and data ready | Tue 03 Mar |
| Cycle 1 execution (builds 1.0.3 onward) | Mon 02 Mar to Wed 04 Mar (planned, see note) |
| Defect fixes and retesting | Thu 05 Mar |
| Cycle 2: retest and regression | Fri 06 Mar to Mon 09 Mar |
| Test closure report | Tue 10 Mar |
| UAT begins | Wed 11 Mar |

(Dates are illustrative for training; shift to the actual sprint calendar.)

**11. Effort Estimation**

Estimated using work breakdown with a 15% buffer. Cross-checked with a three-point estimate for execution (O = 2, M = 4, P = 9 days; PERT = 4.5 days).

| Activity | Hours |
|---|---|
| Requirements review and test conditions | 6 |
| Test case design (40 cases) | 10 |
| Review and rework | 4 |
| Data and environment preparation | 4 |
| Smoke tests (3 builds) | 1.5 |
| Cycle 1 execution | 8 |
| Defect logging | 4 |
| Retest and regression (Cycle 2) | 8 |
| Status reporting | 3 |
| Closure | 2 |
| Subtotal | 50.5 |
| Buffer (15%) | 7.6 |
| **Total** | **about 58 hours (about 10 person-days at 6 productive hours per day)** |

**12. Resources and Tools**

- People: 1 QE engineer (full time), QE lead (review, 20%), developer and DevOps support on demand.
- Tools: Jira (stories, test tasks, defects), a test management add-on or spreadsheet for test cases and execution logs, browser developer tools for logs and network inspection, a screen-capture and recording tool, the mail-catcher for emails.

**13. Entry Criteria** (before Cycle 1 starts)

- Requirements baselined (v1.2 approved).
- Test cases reviewed and approved by the QE Lead.
- A build is deployed to QA with a known build number.
- Smoke test passed.
- Test data loaded and the environment checklist completed.
- QE has access to Jira and the environment.

**14. Exit Criteria**

- 100% of planned test cases executed (any not executed have an approved reason).
- Pass rate of executed tests at least 95%.
- No open Critical or High severity defects.
- Medium and Low defects are either fixed or deferred with Product Owner approval.
- Every requirement has at least one executed test (traceability complete).
- Test closure report completed and reviewed.

*Suspension criteria:* testing pauses if (a) the smoke test fails, (b) the QA environment is down for more than 2 hours, (c) a Critical defect prevents access to the registration or login page, or (d) more than 30% of the tests executed in a day fail for the same reason.

*Resumption criteria:* testing resumes when (a) a new build is deployed and its smoke test passes, (b) the environment is restored and verified, and (c) the Critical defect is fixed and confirmed.

**15. Risks and Mitigation**

| # | Risk | Likelihood | Impact | Score | Mitigation / contingency |
|---|---|---|---|---|---|
| R1 | QA environment is unstable or misconfigured (for example lockout setting) | 3 | 3 | 9 | Environment checklist before Cycle 1; DevOps on-call; escalate within 1 hour |
| R2 | Requirements change late (for example, password rules) | 2 | 3 | 6 | Change control; update traceability matrix; reserve 15% buffer |
| R3 | Confirmation emails not delivered in QA | 2 | 3 | 6 | Verify mail catcher in environment checklist; fall back to database check of the confirmation token |
| R4 | Builds delivered late | 2 | 2 | 4 | Early agreement on build dates; re-prioritize by risk |
| R5 | Only one tester available (illness) | 2 | 3 | 6 | QE Lead as backup; clear test cases so others can execute |
| R6 | High defect volume overloads fixing capacity | 2 | 2 | 4 | Daily triage with developer; fix Critical and High first |

**16. Assumptions and Dependencies**

*Assumptions:* requirements v1.2 are stable; the QA environment is available per section 7; one tester is assigned full time; the product owner is reachable within one working day.

*Dependencies:* DevOps for environment changes; developer for fixes within the agreed turnaround (Critical: 1 day, High: 2 days); the mail-catcher service; Jira availability.

**17. Deliverables**

Test plan; test cases and suites; requirements traceability matrix; execution logs per cycle; defect reports in Jira; daily status reports; test closure report.

**18. Approvals**

| Name | Role | Decision | Date |
|---|---|---|---|
| S. Patel | QE Lead | Approved / Rejected | ________ |
| J. Kim | Developer | Approved / Rejected | ________ |
| M. Okoye | Product Owner | Approved / Rejected | ________ |

---

### Example 2: Sample test case table for Registration and Login

(Preconditions common to all: QA application is running; tester uses Chrome on Windows 11; build version is noted.)

| ID | Title | Req. | Preconditions | Steps | Test data | Expected result | Priority |
|---|---|---|---|---|---|---|---|
| TC-REG-001 | Register a new user with valid details | REQ-01, REQ-05 | Email not already registered; mail catcher active | 1. Open Registration page. 2. Enter email. 3. Enter password. 4. Enter same password in Confirm. 5. Click "Create account". | Email: new.user01@example.com; Password and Confirm: Secure#2024 | Success message "Check your email to confirm your account" is shown; account saved as unconfirmed; one confirmation email arrives at the mail catcher | High |
| TC-REG-002 | Registration rejects an email that is already registered | REQ-04 | User existing01@example.com exists | 1. Open Registration page. 2. Enter the existing email and a valid password and confirmation. 3. Click "Create account". | Email: existing01@example.com; Password and Confirm: Secure#2024 | Error "This email is already registered" appears next to the email field; no new account is created; no email sent | High |
| TC-REG-003 | Registration rejects a password shorter than 8 characters | REQ-03 | Email not already registered | 1. Open Registration page. 2. Enter a new email. 3. Enter the short password and the same value as confirmation. 4. Click "Create account". | Email: new.user02@example.com; Password and Confirm: Ab1xyz (6 characters) | Error "Password must be at least 8 characters with upper, lower, and a number" is shown; no account is created | High |
| TC-REG-004 | Registration rejects an invalid email format | REQ-02 | None | 1. Open Registration page. 2. Enter the invalid email. 3. Enter a valid password and confirmation. 4. Click "Create account". | Email: john.doe@; Password and Confirm: Secure#2024 | Error "Enter a valid email address" is shown; form is not submitted | Medium |
| TC-LOG-001 | Login succeeds with valid, confirmed credentials | REQ-06 | User login.user01@example.com exists, confirmed, not locked; user logged out | 1. Open Login page. 2. Enter email. 3. Enter password. 4. Click "Log in". | Email: login.user01@example.com; Password: Secure#2024 | User is redirected to the Dashboard; header shows "Welcome, Login User"; "Log out" link visible | High |
| TC-LOG-002 | Login fails with a wrong password and shows a generic error | REQ-07 | Same user exists and is not locked | 1. Open Login page. 2. Enter correct email. 3. Enter an incorrect password. 4. Click "Log in". | Email: login.user01@example.com; Password: Wrong#9999 | Error "Invalid email or password" shown; user stays on the Login page; message does not say which field was wrong | High |
| TC-LOG-003 | Account is locked after 5 consecutive failed login attempts | REQ-08 | User lock.user01@example.com exists, confirmed, 0 failed attempts | 1. Open Login page. 2. Attempt login with wrong password 5 times in a row. 3. On the 6th attempt, enter the correct password. | Email: lock.user01@example.com; wrong password: Wrong#0001; correct password: Secure#2024 | After the 5th failure (or on the 6th attempt) the message "Account locked. Try again in 15 minutes" is shown; the correct password is refused during the lock period | High |
| TC-LOG-004 | Logout ends the session | REQ-09 | User logged in on the Dashboard | 1. Click "Log out". 2. Click the browser Back button. | Logged in as login.user01@example.com | Login page is shown after logout; pressing Back does not show protected Dashboard content (the user is redirected to Login) | Medium |

Notice how every case: has one purpose, uses explicit data, has observable expected results, is linked to a requirement, and has a priority informed by the risk table. Most also include a negative scenario (invalid email, duplicate email, short password, wrong password).

### Example 3: Sample execution log

The log below shows one cycle (Cycle 1, build 1.0.3, Chrome 126 on Windows 11, QA environment) run by tester A. Rivera on Tuesday 03 March 2026. The log keeps one row per test case per execution.

| Test Case ID | Date | Tester | Build | Status | Actual result | Evidence | Defect ID / Notes |
|---|---|---|---|---|---|---|---|
| TC-REG-001 | 03 Mar | A. Rivera | 1.0.3 | Pass | Account created; success message shown exactly as expected; confirmation email received in 8 seconds | REG-001_success.png | - |
| TC-REG-002 | 03 Mar | A. Rivera | 1.0.3 | Pass | Error "This email is already registered" shown below the email field; no new row in the user table | REG-002_duplicate.png | - |
| TC-REG-003 | 03 Mar | A. Rivera | 1.0.3 | Fail | Password "Ab1xyz" (6 characters) was accepted; account created and confirmation email sent; no error shown | REG-003_accepted.png, REG-003_video.mp4 | DEF-101 (High) |
| TC-REG-004 | 03 Mar | A. Rivera | 1.0.3 | Pass | Message "Enter a valid email address" shown; no submission | REG-004_invalid-email.png | - |
| TC-LOG-001 | 03 Mar | A. Rivera | 1.0.3 | Pass | Redirected to Dashboard; header showed "Welcome, Login User"; "Log out" link visible | LOG-001_dashboard.png | - |
| TC-LOG-002 | 03 Mar | A. Rivera | 1.0.3 | Pass | Error "Invalid email or password" shown; stayed on Login page | LOG-002_error.png | - |
| TC-LOG-003 | 03 Mar | A. Rivera | 1.0.3 | Blocked | Could not run: QA lockout threshold is set to 50, so the lock cannot be reached in a reasonable time | - | OPS-212 raised to DevOps |
| TC-LOG-004 | 03 Mar | A. Rivera | 1.0.3 | Not Run | Planned for the afternoon session | - | - |

**Summary of this log:** Pass = TC-REG-001, TC-REG-002, TC-REG-004, TC-LOG-001, TC-LOG-002 = 5. Fail = 1 (TC-REG-003). Blocked = 1 (TC-LOG-003). Not Run = 1 (TC-LOG-004). Total = 5 + 1 + 1 + 1 = 8. Executed = 6 (Pass + Fail). Execution % = 6/8 = 75%. Pass % = 5/6 = 83.3%.

Notice a subtle point: the failed test TC-REG-003 also affects traceability. REQ-03 is linked to DEF-101, and the status report must mention that a High severity defect is open against a high-priority requirement.

---

## Try It: Project 1 Activities

### Activity 1: Write a one-page test plan

**Scenario.** Your Project 1 team is adding a new **Profile Update** feature to the sample web app, in a two-week sprint. The user story reads: "As a registered user, I want to update my display name and my phone number from the Profile page so that my information stays current." Acceptance criteria:

- AC1: The user can change the display name (2 to 30 characters) and save; the new name appears in the page header.
- AC2: The phone number must contain 10 digits; otherwise an error "Enter a 10-digit phone number" is shown.
- AC3: Changes are saved only after clicking "Save". If the user leaves without saving, nothing is changed.
- AC4: The user must be logged in to see the Profile page. A logged-out visitor is redirected to Login.

**Task.** Write a **one-page test plan** (maximum one page, about 300 to 400 words) containing:

1. Goal.
2. Scope: in and out (at least 3 items out of scope).
3. Approach (test levels and types, manual or automated, risk focus).
4. Environment and test data (at least one specific data example).
5. Roles.
6. Schedule: 4 key dates within the sprint (use "Day 1 to Day 10").
7. Entry and exit criteria (at least 3 each).
8. Top risks: at least three, each with likelihood, impact, score (likelihood x impact), and mitigation.
9. Reporting: how and how often.
10. One three-point estimate for test execution (O, M, P and the PERT result).

**Answer hints.**

- *Goal:* make it measurable, such as "Verify AC1 to AC4 with no open Critical or High defects by Day 9."
- *Out of scope candidates:* changing email or password, profile photo upload, performance testing, international phone formats, mobile apps.
- *Approach:* system-level functional testing, manual first; negative tests for AC2 and AC4; a short smoke suite on each build; plan to select regression tests for Login (the profile page depends on being logged in) and leave the design of regression suites for Friday.
- *Risk scoring:* the access control in AC4 (a logged-out user seeing someone's data) is a high-impact security risk, so probably likelihood 2 and impact 3, score 6. Phone validation has high likelihood (many format variations) but moderate impact (2), so score 6. Display name length is simple: likelihood 1, impact 1, score 1.
- *Entry criteria:* story accepted into the sprint with clear acceptance criteria; build deployed to QA; smoke test passed.
- *Exit criteria:* all acceptance criteria tested; 100% planned cases executed; no open Critical or High; Definition of Done met.
- *Estimate check:* if O = 1 day, M = 2 days, P = 5 days, then E = (1 + 4x2 + 5) / 6 = 14 / 6 = 2.33 days. If your numbers differ, re-check the formula: it is (O + 4M + P) / 6, not (O + M + P) / 3.
- *Common mistakes to avoid:* an empty out-of-scope list, vague exit criteria like "when testing is finished", missing risks, and no owner for the environment.

### Activity 2: Execute given test cases and fill the execution log

**Scenario.** You are the tester for the Registration and Login feature, Cycle 1, build 1.0.4, on Chrome. The application behaves as described in the "Observed behavior" column below (this is what you "saw" when you ran the steps; in a real run you would see it on the screen).

| Test Case ID | Test case summary (expected result) | Observed behavior when executed |
|---|---|---|
| TC-REG-001 | Valid registration creates an account, shows "Check your email to confirm your account", sends one confirmation email | Account created, message shown, email arrived. |
| TC-REG-002 | Duplicate email rejected with "This email is already registered" | The form accepted the duplicate email, and a second account with the same email was created. |
| TC-REG-004 | Email "john.doe@" is rejected with "Enter a valid email address" | Error shown as expected. |
| TC-LOG-001 | Valid login lands on the Dashboard with "Welcome, Login User" | Dashboard shown, but the header said "Welcome, undefined". |
| TC-LOG-002 | Wrong password shows "Invalid email or password" | Message shown as expected. |
| TC-LOG-003 | Lockout after 5 failures with "Account locked. Try again in 15 minutes" | Could not run: the Login page returned a server error (HTTP 500) for any user after the QA database restarted, so no login attempt was possible. |
| TC-LOG-004 | Logout returns to Login; Back button does not show Dashboard | You have not reached this test yet before the end of the day. |
| TC-LOG-005 (new) | Login with an unconfirmed account is refused with the message "Please confirm your email first" | This test was removed from this cycle by the Product Owner (feature moved to Release 1.1). |

**Task.**

1. Fill in a log with these columns: Test Case ID, Status (Pass, Fail, Blocked, Skipped, Not Run), Actual result, Evidence you would capture, Defect or note.
2. Calculate execution % and pass % for these 8 test cases (treat the skipped test as part of the 8 planned).
3. Write a three-line daily status summary with an overall RAG (red, amber, green) rating and one blocker with a "help needed" request.
4. Update the traceability: for each failed or blocked test, name the requirement affected (use REQ-04, REQ-06, REQ-08).

**Answer hints (check your work).**

| Test Case ID | Expected status | Reasoning |
|---|---|---|
| TC-REG-001 | Pass | Actual matches expected on all three checks (account, message, email) |
| TC-REG-002 | Fail | The duplicate was accepted, which violates REQ-04; log a defect (data integrity issue, likely High or Critical) |
| TC-REG-004 | Pass | As expected |
| TC-LOG-001 | Fail | Header text differs from expected ("undefined" instead of the user's name); even though login succeeded, one expected result was not met. Log a defect (probably Medium severity, because login still works) |
| TC-LOG-002 | Pass | As expected |
| TC-LOG-003 | Blocked | A server error on the Login page prevents running. Raise the issue (it may also become a defect or an environment ticket). Do not mark as Fail: the lockout behavior itself was never tested |
| TC-LOG-004 | Not Run | Simply not reached |
| TC-LOG-005 | Skipped | Deliberately not executed, with a reason (descoped by the Product Owner). Record the decision |

*Calculation hints:* Pass = 3 (REG-001, REG-004, LOG-002). Fail = 2 (REG-002, LOG-001). Blocked = 1. Skipped = 1. Not Run = 1. Total = 3 + 2 + 1 + 1 + 1 = 8. Executed = Pass + Fail = 5. **Execution % = 5/8 = 62.5%**. **Pass % = 3/5 = 60%** (of executed). Also valid if your team defines pass rate against all planned tests: 3/8 = 37.5%. State the definition used.

*Evidence hints:* screenshot of the duplicate account in the user list and of the form; screenshot of the header showing "Welcome, undefined"; a screenshot of the HTTP 500 error plus the browser's network tab and the server log line with timestamp.

*Status summary hint:* "Execution 62.5%, pass 60% of executed. Two defects raised (DEF-xxx duplicate email accepted, DEF-yyy header shows 'undefined'). Overall: RED because a High-risk lockout test is blocked and a data integrity defect is open. Help needed: DevOps to restore the Login endpoint (HTTP 500) by 10:00 tomorrow."

*Traceability hint:* REQ-04 (TC-REG-002, failed); REQ-06 (TC-LOG-001, failed); REQ-08 (TC-LOG-003, blocked).

*Stretch:* decide which tests you would run first tomorrow after the fix, using the risk matrix (lockout and duplicate retest first, then LOG-004).

---

## Knowledge Check

Try to answer each question before reading the answer.

**1. In one sentence each, what is the difference between a test strategy and a test plan?**
*Answer:* A test strategy is a high-level, long-lived description of how an organization or product line approaches testing in general; a test plan is a project- or release-specific document describing what will be tested, by whom, when, and where.

**2. Why should a test plan list what is out of scope?**
*Answer:* It sets clear expectations, protects the team from assumptions that "everything" will be tested, and gives stakeholders a chance to challenge exclusions before testing starts. It also helps explain why a problem found later in an out-of-scope area was not tested.

**3. What is the difference between entry criteria, exit criteria, suspension criteria and resumption criteria?**
*Answer:* Entry criteria are the conditions to be met before a testing phase can start. Exit criteria are the conditions that mean testing can be considered complete. Suspension criteria say when testing must be paused. Resumption criteria say what must happen before testing can restart.

**4. A feature has likelihood 3 and impact 2. What is its risk score and what does it mean for testing order?**
*Answer:* 3 x 2 = 6, which is High priority on the scale in this lesson. It should be tested early and thoroughly, though after any Critical (score 9) items.

**5. Use three-point estimation: O = 3 days, M = 5 days, P = 10 days. What is the PERT estimate and standard deviation?**
*Answer:* E = (3 + 4x5 + 10) / 6 = 33 / 6 = 5.5 days. SD = (10 - 3) / 6 = 1.17 days (approximately).

**6. What does a story point measure in Agile estimation?**
*Answer:* The relative size of a user story, combining effort, complexity, and uncertainty, not hours. Teams use it with their velocity to forecast how much they can complete in a sprint.

**7. Name the four classic test levels and who typically performs each.**
*Answer:* Unit (developers), integration (developers and testers), system (independent testers/QE), acceptance or UAT (business users, customers, product owner).

**8. List at least eight standard fields of a test case.**
*Answer:* Test case ID, title, requirement reference, preconditions, steps, test data, expected result, actual result, status, priority (also author, date, environment, linked defect).

**9. What is wrong with this test case: "Title: Check registration. Steps: Register a user. Expected result: Works fine"?**
*Answer:* The title is vague, there are no preconditions or test data, the steps are not specific, and "works fine" cannot be verified. A good version has precise steps, explicit data, and observable expected results (message text, page shown, data saved).

**10. What is the difference between a test suite and a test cycle?**
*Answer:* A suite is a grouped collection of test cases (for example, the Login suite). A cycle is one round of executing test cases against a particular build in a period of time.

**11. What is the difference between a smoke test and a sanity test?**
*Answer:* A smoke test is a broad, shallow check of critical functions on every new build to decide whether the build is stable enough to test. A sanity test is a narrow, focused check after a small change or fix to confirm that the change works and that nothing obvious nearby broke.

**12. When should a test be marked Blocked rather than Failed?**
*Answer:* When the test cannot be carried out because of something outside the behavior being tested (for example, environment down, missing data, or another open defect prevents reaching the step), so the expected behavior was never actually checked. Failed means it ran and the actual result differed from expected.

**13. Why is evidence important, and what are three kinds?**
*Answer:* Evidence makes defects reproducible, proves the test was run, and supports audits. Kinds include screenshots, screen recordings, logs (console, network, server), test data used, and environment details.

**14. What is the difference between retesting and regression testing?**
*Answer:* Retesting re-runs the exact failed test to confirm that a defect has been fixed. Regression testing re-runs other previously passing tests to confirm that the change did not break existing behavior.

**15. A cycle has 50 planned tests: 36 passed, 6 failed, 3 blocked, 1 skipped, 4 not run. Calculate execution % and pass %.**
*Answer:* Executed = 36 + 6 = 42. Execution % = 42/50 = 84%. Pass % = 36/42 = 85.7% (of executed), or 36/50 = 72% if against all planned tests.

**16. During testing 36 defects were found. After release, users reported 4 more. Calculate defect leakage and DDP.**
*Answer:* Total = 36 + 4 = 40. Leakage = 4/40 = 10%. DDP = 36/40 = 90%. (DDP + leakage = 100%.)

**17. A module of 8 KLOC has 24 defects. What is the defect density?**
*Answer:* 24 / 8 = 3 defects per KLOC.

**18. What is a Requirements Traceability Matrix and give two benefits.**
*Answer:* A table linking requirements to test cases and defects. Benefits: shows coverage (requirements with no tests), supports impact analysis when a requirement changes, and makes reporting and audit easier.

**19. Your build for today fails the smoke test. What should you do?**
*Answer:* Stop deeper testing, record the smoke failure with evidence, inform the developer and test lead immediately, mark the build as rejected, and wait for a new build (per the suspension and resumption criteria). Do not continue to execute the full suite.

**20. The release date is in two days, but the test plan needs four. What do you do?**
*Answer:* Report immediately with data, re-prioritize by risk so that the highest-risk tests run first, present options with trade-offs (reduce scope, extend date, add testers, accept stated risks), and let the product owner and stakeholders decide. Do not skip evidence or mark tests passed without running them.

**21. Who makes the final decision to release: the tester or the product owner?**
*Answer:* The product owner and stakeholders decide. The tester provides an honest, evidence-based recommendation in the closure report, including remaining risks.

---

## Key Takeaways

- A **test plan** answers what, why, how, who, when, where, and what-if for testing a release or feature, like a trip itinerary. A **test strategy** is the general, long-lived approach behind many plans.
- Standard plan sections (IEEE 829 / ISO 29119 style) include objective, scope in and out, approach, levels and types, environment, data, roles, schedule, estimation, tools, entry/exit/suspension/resumption criteria, risks, assumptions and dependencies, deliverables, and approvals.
- **Risk = Likelihood x Impact.** Test the highest-risk areas first and deepest.
- Estimate with work breakdown, three-point/PERT (E = (O + 4M + P) / 6), experience, or story points, and always state assumptions and add a buffer.
- In Agile, a **one-page plan** and the Definition of Done give just enough planning.
- Test levels are unit, integration, system, and acceptance. Levels (where) differ from types (what quality aspect).
- A good **test case** has an ID, a clear title, preconditions, precise steps, specific data, observable expected results, and a priority, and is traceable to a requirement. Suites group cases; cycles are rounds of execution.
- Before executing: check entry criteria, environment readiness, and run a **smoke test**.
- Record results honestly: **Pass, Fail, Blocked, Skipped, Not Run**; attach **evidence**; log a defect for every failure (details in the next lesson).
- **Retesting** confirms the fix; **regression testing** checks for side effects (Friday).
- Track progress daily; write a **status report** that includes blockers and needed help.
- Core metrics: Execution % = executed / planned; Pass % = passed / executed; Defect density = defects / size; Defect leakage % = post-release defects / (test defects + post-release defects); DDP = 100% - leakage. Interpret numbers with context.
- **Traceability** links requirements, tests, and defects. The **closure report** ends testing with facts and a recommendation, and the business decides on release.
- When tests are blocked or the schedule slips: escalate early, re-prioritize by risk, offer options, and never hide the truth.

---

## Additional Resources

1. **ISTQB (International Software Testing Qualifications Board)**: the Foundation Level syllabus and the glossary define test planning, test levels, test cases, and metrics terms used in this lesson. https://www.istqb.org and the glossary at https://glossary.istqb.org
2. **Guru99, "Test Plan: What is, How to Create (with Example)"**: a beginner-friendly walkthrough of test plan components with examples. https://www.guru99.com/test-planning.html
3. **Guru99, "How to Write Test Cases: Sample Template with Examples"**: practical guidance on test case fields and writing style. https://www.guru99.com/test-case.html

*Next lesson: the Defect Lifecycle, where you learn how a defect you log today travels from New to Closed, how to write a defect report that developers love, and how severity and priority differ.*
