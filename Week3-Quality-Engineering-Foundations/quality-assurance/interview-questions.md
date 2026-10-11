# Interview Questions: Week 3 - Quality Engineering Foundations

**How to use this bank**

1. Read the question and try to answer out loud (as in a real interview) before looking at anything.
2. Check that you can hit the **Keywords**. Use the **Hint** if you are stuck.
3. Open the answer, compare, and re-read the lesson named in the **Source** line for any gaps.

Each day has 16 questions: **11 Beginner (recall), 4 Intermediate (scenario), 1 Advanced (deep dive)**, which is roughly the 70-25-5 distribution. Every answer comes from the Week 3 written lessons.

---

# Day 1 (Monday): SDLC, STLC & Agile

## Beginner (Foundational)

### Q1: What is the SDLC, and what are its phases?
**Keywords:** Life cycle, Idea to retirement, Seven phases, Quality in every phase
<details>
<summary>Click to Reveal Answer</summary>

The Software Development Life Cycle is the structured journey of software from idea to retirement. In this course it has seven phases: planning, requirements analysis, design (HLD and LLD), implementation, testing, deployment and maintenance. Each phase has a purpose, activities, inputs, outputs and people involved.

A strong answer adds that quality has a role in *every* phase, not only testing. For example, QEs review requirements, review designs, support unit testing, give go/no-go input at deployment and triage production issues in maintenance.

**Source:** `sdlc-fundamentals.md`
</details>

---

### Q2: What is the difference between requirements and design in the SDLC?
**Keywords:** What vs. how, Requirements, HLD, LLD
<details>
<summary>Click to Reveal Answer</summary>

Requirements say *what* the system must do (and how well). Design says *how* it will be built: high-level design (architecture, modules) and low-level design (detailed module logic), plus database design and UI wireframes. Implementation then builds it.

A short way to say it in an interview: requirements = what, design = how, implementation = build, testing = check, deployment = release, maintenance = sustain.

**Source:** `sdlc-fundamentals.md`
</details>

---

### Q3: Why do defects cost more the later they are found, and what is "shift-left"?
**Keywords:** Cost of defects, Early detection, Shift-left, Prevention
<details>
<summary>Click to Reveal Answer</summary>

A defect found late has been built upon: more code, tests, documents and sometimes customers depend on it, so fixing it means more rework. The lesson's illustration shows about 1x in Requirements, 5x in Design, 10x in Implementation, 20x in Testing and 50-100x or more in Production.

**Shift-left** means moving quality activities (requirement reviews, test design, early automation) earlier in the life cycle so defects are prevented or found while they are cheap. It does *not* mean "stop testing at the end"; it means start quality work at the beginning and continue throughout.

**Source:** `sdlc-fundamentals.md`, section "The cost of finding defects late"
</details>

---

### Q4: What is the difference between functional and non-functional requirements? Give an example of each.
**Keywords:** What the system does, How well, Performance, Security, Usability
<details>
<summary>Click to Reveal Answer</summary>

A **functional** requirement states what the system does (a capability), for example "a customer can place an order". A **non-functional** requirement states how well it does it (speed, security, usability, availability), for example "the menu page loads within 3 seconds on a standard mobile connection". Note that the non-functional example is measurable, which makes it testable.

**Source:** `sdlc-fundamentals.md`, "Phase 2: Requirements Analysis"
</details>

---

### Q5: Explain Waterfall and its biggest weakness for testing.
**Keywords:** Sequential, Document-driven, Late testing, Late feedback
<details>
<summary>Click to Reveal Answer</summary>

Waterfall is a sequential, document-driven model: each phase finishes before the next starts. It is predictable when requirements are stable (and can suit regulated, small or simple projects). In pure Waterfall, testing begins only after coding is finished, so defects, including ones introduced at requirements time, are found late when they are expensive to fix. This is the **late-testing problem**.

**Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`
</details>

---

### Q6: What is the V-Model?
**Keywords:** Test level per development phase, Early test planning, Still sequential
<details>
<summary>Click to Reveal Answer</summary>

The V-Model is a Waterfall variant that pairs every development phase with a test level: business requirements with acceptance testing, system requirements/design with system testing, architecture (high-level design) with integration testing, and module design with unit testing. Testing is therefore *planned* early, as soon as each left-side document exists. However, it is still sequential, so execution still happens later.

**Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`; `verification-vs-validation.md`
</details>

---

### Q7: What is Agile, and how is it different from Scrum?
**Keywords:** Values and principles, Framework, Manifesto, Kanban/XP
<details>
<summary>Click to Reveal Answer</summary>

Agile is a set of **values and principles** (the Agile Manifesto), not a single process. It values individuals and interactions over processes and tools, working software over comprehensive documentation, customer collaboration over contract negotiation and responding to change over following a plan. **Scrum** is one specific *framework* that applies those values (others include Kanban and XP).

Common misconception: Agile does not mean "no planning or documentation"; it means planning continuously and documenting "just enough". The items on the right still have value.

**Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`
</details>

---

### Q8: Name the three Scrum accountabilities and where a QE fits.
**Keywords:** Product Owner, Scrum Master, Developers, No separate tester role
<details>
<summary>Click to Reveal Answer</summary>

Scrum has three accountabilities: the **Product Owner** (maximizes value and orders the backlog), the **Scrum Master** (the team's effectiveness and the Scrum way of working: a servant leader who facilitates, coaches and removes impediments) and the **Developers** (build a quality Increment).

QA, QE and SDET professionals are part of the **Developers**; Scrum has no separate tester role, but testing skill is still essential and QEs lead and enable quality. Whole-team quality means everyone shares responsibility.

**Source:** `agile-roles-and-responsibilities.md`
</details>

---

### Q9: List the five Scrum events with their typical timeboxes for a 2-week sprint.
**Keywords:** Planning 4h, Daily Scrum 15 min, Review 2h, Retrospective 1.5h, Refinement
<details>
<summary>Click to Reveal Answer</summary>

- **Sprint Planning:** up to 4 hours; decide the Sprint Goal and the plan.
- **Daily Scrum:** 15 minutes; daily coordination and blockers.
- **Sprint Review:** up to 2 hours; inspect the Increment with stakeholders.
- **Sprint Retrospective:** up to 1.5 hours; improve how the team works.
- **Refinement:** ongoing; get stories ready.

The Review looks at the *product*; the Retrospective looks at the *way of working*.

**Source:** `scrum-ceremonies-and-sprint-lifecycle.md`
</details>

---

### Q10: What are the six phases of the STLC?
**Keywords:** Requirement Analysis, Test Planning, Test Case Development, Environment Setup, Execution, Closure
<details>
<summary>Click to Reveal Answer</summary>

In order: Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution and Test Cycle Closure. Each phase has entry criteria, exit criteria, activities, deliverables and roles. Typical deliverables are the question log and RTM draft, the test plan, test cases and data, the environment setup record with smoke result, defect reports and the closure report.

The STLC does not replace the SDLC; it runs *in parallel* with it, starting as early as requirements.

**Source:** `software-testing-life-cycle.md`
</details>

---

### Q11: What is a Definition of Done, and how is it different from a Definition of Ready?
**Keywords:** Exit standard, Front door, Official commitment, Team practice
<details>
<summary>Click to Reveal Answer</summary>

The **Definition of Done (DoD)** is the team's shared quality standard for finished work and is the official commitment of the Increment in Scrum. "Done means done": partial work does not count. The **Definition of Ready (DoR)** is a widely used team practice (not an official Scrum artifact) that checks a story is clear enough to start. A memorable phrase: "Ready is the front door; Done is the exit."

**Source:** `agile-roles-and-responsibilities.md`, `scrum-ceremonies-and-sprint-lifecycle.md`
</details>

---

## Intermediate (Application)

### Q12: Your team is building a regulated medical-records feature with stable requirements, but stakeholders also want frequent demos. Which delivery model would you suggest and why?
**Hint:** Think "hybrid" and what constraints exist.
**Keywords:** Hybrid, Regulation, Documentation, Iterations, Context
<details>
<summary>Click to Reveal Answer</summary>

A hybrid approach is a reasonable answer. Regulation and stable requirements favour Waterfall-style documentation and traceability (or the V-Model's early test planning), while frequent demos suggest Agile-style iterations (for example, Agile within a regulated framework). The lesson stresses there is no single best model: choose based on requirement stability, change frequency, regulation, customer availability and team context.

Whatever model is chosen, say the QE's mission is the same: involved early and preventing defects as well as finding them.

**Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`
</details>

---

### Q13: Mid-sprint you realise the Sprint Goal is at risk because testing is piling up. What do you do?
**Hint:** Transparency, not lowering quality.
**Keywords:** Speak up early, Negotiate scope, Swarm, Protect the DoD
<details>
<summary>Click to Reveal Answer</summary>

Speak up early (for example in the Daily Scrum), tell the Product Owner and team honestly, and negotiate *scope* with the Product Owner. Swarm on the key items so the team finishes work rather than starting more. Never lower the Definition of Done to "get it done" and never extend the Sprint, since the length is fixed. Also look at the cause: testing starting too late (mini-waterfall) rather than continuously.

**Source:** `scrum-ceremonies-and-sprint-lifecycle.md`
</details>

---

### Q14: How do you decide between Scrum and Kanban for a team handling unpredictable production support tickets?
**Keywords:** Continuous flow, WIP limits, Pull, Lead time, Cycle time
<details>
<summary>Click to Reveal Answer</summary>

Kanban is a better fit for continuous, unpredictable work: work is visualized on a board, **WIP limits** cap cards per column (reducing context switching and exposing bottlenecks), cards are **pulled** when there is capacity, and the team measures **lead time** (request to delivery) and **cycle time** (start of work to delivery). Scrum's fixed-length sprints suit planned, goal-based delivery. A hybrid such as Scrumban is also legitimate.

**Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`
</details>

---

### Q15: A story arrives in refinement with the line "The page should load quickly." How do you respond as a QE?
**Keywords:** Testability, Acceptance criteria, Measurable, Three Amigos
<details>
<summary>Click to Reveal Answer</summary>

"Quickly" is untestable. Raise it in refinement (or a Three Amigos conversation between business, development and testing) and ask for a measurable criterion, such as a target time under a defined condition (for example, "loads within 3 seconds on a standard mobile connection"). Then capture it as acceptance criteria, ideally in Given/When/Then form, which become the root of your test cases.

**Source:** `agile-roles-and-responsibilities.md`; `scrum-ceremonies-and-sprint-lifecycle.md`
</details>

---

## Advanced (Deep Dive)

### Q16: Explain how the SDLC, the chosen delivery model and the STLC relate to each other in an Agile sprint.
**Keywords:** Same phases, Compressed, Overlapped, Repeated each sprint, Continuous testing
<details>
<summary>Click to Reveal Answer</summary>

A delivery model does not change *which* SDLC phases exist; it changes their order, size and overlap. Waterfall runs them once in sequence; Agile runs a small version of all of them every sprint. The STLC is the testing slice of that, and in Agile its six phases are compressed, overlapped and repeated each sprint: testability questions in refinement (analysis), risk and effort in planning, test design alongside development, ready environments via CI, continuous execution with automation, and closure in the review and retrospective. Supports this: the Definition of Done, continuous testing and automation. The result is that testing is a continuous activity, not a phase at the end.

**Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`; `software-testing-life-cycle.md`; `scrum-ceremonies-and-sprint-lifecycle.md`
</details>

---

# Day 2 (Tuesday): Test Management & Defect Lifecycle

## Beginner (Foundational)

### Q17: What is a requirement and why is it important to a tester?
**Keywords:** Test basis, Test oracle, What/how well/limits
<details>
<summary>Click to Reveal Answer</summary>

A requirement states what the system must do, how well, or within what limits. For a tester it is the main **test basis** (what tests are derived from) and the **test oracle** (how we decide the expected result). Without clear requirements you cannot tell a correct behaviour from an incorrect one.

**Source:** `requirements-analysis.md`
</details>

---

### Q18: What makes a good requirement?
**Keywords:** Clear, Testable, Complete, Consistent, Traceable
<details>
<summary>Click to Reveal Answer</summary>

A good requirement is clear, unambiguous, complete, consistent, testable, feasible, traceable and prioritized. Warning words that signal weak requirements include "fast", "user-friendly", "etc." and "appropriate". Reviewing requirements this way is a form of **static testing** and a practical example of shift-left.

**Source:** `requirements-analysis.md`
</details>

---

### Q19: What is a Requirement Traceability Matrix (RTM)?
**Keywords:** Requirements to tests, Coverage gaps, Impact analysis
<details>
<summary>Click to Reveal Answer</summary>

An RTM is a table linking each requirement to the tests (and defects) that cover it. It shows at a glance which requirements have no tests (coverage gaps) and supports **change impact analysis**: when a requirement changes, you can see which tests to update.

**Source:** `requirements-analysis.md`; `software-testing-life-cycle.md`
</details>

---

### Q20: What is the difference between a test plan and a test strategy?
**Keywords:** Specific vs. general, Long-lived, Release/feature
<details>
<summary>Click to Reveal Answer</summary>

A **test strategy** is the general, long-lived approach behind many projects or plans (how the organization tests). A **test plan** is specific to a release or feature and answers what, why, how, who, when, where and what-if, like a trip itinerary. Typical plan sections: objective, scope (in and out), approach, levels and types, environment, data, roles, schedule, estimates, tools, entry/exit/suspension/resumption criteria, risks, assumptions and dependencies, deliverables and approvals.

**Source:** `test-planning-and-test-execution.md`
</details>

---

### Q21: How is risk calculated in testing, and how does it guide effort?
**Keywords:** Likelihood x Impact, Highest-risk first, Prioritise
<details>
<summary>Click to Reveal Answer</summary>

**Risk = Likelihood x Impact.** Areas with high likelihood of failure and high impact if they fail (for example payment or login) are tested first and deepest; low-risk areas get lighter coverage. You must also be transparent about what was *not* tested.

**Source:** `test-planning-and-test-execution.md`
</details>

---

### Q22: What are the main parts of a good test case?
**Keywords:** ID, Preconditions, Steps, Data, Expected result, Priority, Traceability
<details>
<summary>Click to Reveal Answer</summary>

A good test case has an ID, a clear title, preconditions, precise numbered steps, specific data, observable expected results, a priority and traceability to a requirement. Test cases are grouped into suites, and a cycle is a round of executing them.

**Source:** `test-planning-and-test-execution.md`
</details>

---

### Q23: Name the standard test execution statuses.
**Keywords:** Pass, Fail, Blocked, Skipped, Not Run
<details>
<summary>Click to Reveal Answer</summary>

Pass, Fail, Blocked (cannot be executed because of an external obstacle such as a missing environment or an open blocking defect), Skipped (deliberately not run) and Not Run. Results must be recorded honestly, with evidence attached, and every failure should lead to a defect report.

**Source:** `test-planning-and-test-execution.md`
</details>

---

### Q24: Describe the typical defect lifecycle.
**Keywords:** New, Assigned, In Progress, Fixed, Retest, Closed, Reopened
<details>
<summary>Click to Reveal Answer</summary>

Main path: New -> Assigned -> Open -> In Progress -> Fixed -> Ready for Retest -> Verified/Closed. Side exits are Rejected, Duplicate, Not a Bug / Cannot Reproduce, Deferred and Won't Fix, with a loop back via Reopened if the fix fails retest. Developers fix; **testers verify** ("Fixed" is not "done" until retested). Every "not going to fix" outcome needs a recorded reason.

**Source:** `defect-lifecycle.md`
</details>

---

### Q25: What is the difference between severity and priority?
**Keywords:** Damage, Order, Technical impact, Business urgency
<details>
<summary>Click to Reveal Answer</summary>

**Severity** is about damage: the technical impact of the defect on the system. **Priority** is about order: how urgently the business wants it fixed. They often differ. For example, a typo in the company name on the home page is low severity but high priority, while a crash in a rarely used admin report could be high severity but low priority. Priority can change with context. In Jira, priority is a default field while severity is usually a custom field.

**Source:** `defect-lifecycle.md`; `jira-issues-stories-tasks-and-bugs.md`
</details>

---

### Q26: What should a good bug report contain?
**Keywords:** Specific title, Steps, Expected vs. actual, Environment, Evidence
<details>
<summary>Click to Reveal Answer</summary>

A specific summary, environment and build number, numbered reproduction steps, expected versus actual results, evidence (screenshots, logs, video), severity, priority, component and a link to the affected story or requirement and test case. It should be specific, reproducible, objective, minimal and evidence-backed, with one defect per report.

**Source:** `defect-lifecycle.md`; `jira-issues-stories-tasks-and-bugs.md`
</details>

---

### Q27: What is Jira's issue hierarchy and what are the main issue types?
**Keywords:** Epic, Story, Task, Bug, Sub-task
<details>
<summary>Click to Reveal Answer</summary>

The default hierarchy is **Epic > Story / Task / Bug > Sub-task**. Epics are big goals, Stories deliver user-facing value ("As a / I want / so that"), Tasks are non-feature work, Bugs are defects and Sub-tasks are small steps. A Spike is a time-boxed investigation. Issues are identified by a key such as QEA-12 (project key plus number).

**Source:** `jira-issues-stories-tasks-and-bugs.md`; `introduction-to-jira.md`
</details>

---

## Intermediate (Application)

### Q28: A developer marks your bug "Cannot Reproduce," but you saw it clearly. What do you do?
**Hint:** Reproducibility is about information.
**Keywords:** Environment, Build, Steps, Evidence, Triage
<details>
<summary>Click to Reveal Answer</summary>

Re-check that the defect report states the exact build, environment, data and steps, and attach logs, screenshots or a recording. Try to reproduce on the same build and share the evidence with the developer, ideally pairing with them. If it is intermittent, record the frequency and conditions. If there is still disagreement, raise it in triage so the team can decide (accept, defer, reject, ask for more information), and keep a recorded reason either way. Keep the tone factual and blame the product, not the person.

**Source:** `defect-lifecycle.md`
</details>

---

### Q29: Your execution results: 80 planned, 60 executed, 54 passed; before release, 6 defects were found in testing and 4 escaped to production. Compute execution %, pass % and defect leakage.
**Keywords:** Executed/planned, Passed/executed, Leakage
<details>
<summary>Click to Reveal Answer</summary>

- Execution % = executed / planned = 60 / 80 = **75%**
- Pass % = passed / executed = 54 / 60 = **90%**
- Defect leakage % = post-release defects / (test defects + post-release defects) = 4 / (6 + 4) = **40%**. Defect detection percentage (DDP) = 100% - 40% = 60%.

Interpret with context: a 90% pass rate hides risk if the 10% failures are critical or if 25% of tests are not yet run.

**Source:** `test-planning-and-test-execution.md`
</details>

---

### Q30: You are told the test phase will be cut by a week, but scope is unchanged. How do you respond?
**Keywords:** Escalate early, Re-prioritise by risk, Options, Honesty
<details>
<summary>Click to Reveal Answer</summary>

Escalate early and with data. Re-prioritise testing by risk (Likelihood x Impact), so the highest-risk areas are covered first. Present options (reduce scope, add people, accept documented risk, move the date) and let the business decide, while stating clearly what will not be tested. Never hide the truth or quietly lower quality; the closure report gives facts and a recommendation, and the business decides on release.

**Source:** `test-planning-and-test-execution.md`
</details>

---

### Q31: Design a minimal Jira Bug workflow and explain how it supports QE.
**Keywords:** Statuses, Transitions, Resolutions, Ready for Retest, Reopened
<details>
<summary>Click to Reveal Answer</summary>

A QE Bug workflow maps the defect lifecycle onto statuses such as Open, In Progress, Ready for Retest, Closed, Reopened, Rejected, Deferred and Duplicate. Each status belongs to a status category (To Do, In Progress, Done) and must be mapped to a board column, otherwise the card disappears. Resolutions record how work ended and should be cleared on reopen. A Story workflow adds In Review and In Testing so QA work is visible. Keep workflows simple, aligned with the real process and documented.

**Source:** `jira-boards-and-workflows.md`
</details>

---

## Advanced (Deep Dive)

### Q32: A requirements review finds ambiguity and a contradiction two days before development starts. Describe the process from finding to updated tests, and explain the value.
**Keywords:** Static testing, Question log, Change impact, RTM, Cost
<details>
<summary>Click to Reveal Answer</summary>

Record each finding in the **question log** with a specific, answerable, polite question (for example, which of two conflicting rules applies). Get the requirement clarified and versioned. Run **impact analysis** using the RTM to see which test conditions, cases and downstream work are affected, then update the RTM and test set. The review is **static testing** (reviews, walkthroughs, inspections) and finds defects at the lowest possible cost, which is shift-left in practice. Exit criteria for the phase include review report, clarified requirements, question log, RTM draft and testability notes.

**Source:** `requirements-analysis.md`
</details>

---

# Day 3 (Wednesday): Testing Fundamentals

## Beginner (Foundational)

### Q33: What is the difference between error, defect and failure?
**Keywords:** Human mistake, Flaw in work product, Observable wrong behavior
<details>
<summary>Click to Reveal Answer</summary>

An **error** (mistake) is a human action that produces something wrong. A **defect** (fault, bug) is the flaw that results in a work product (code, requirement, design). A **failure** is the observable wrong behavior when the defect is executed under the right conditions. Chain: Error -> Defect -> Failure. In the lifecycle: the tester observes and reports the failure, the developer finds and fixes the defect and the team learns from the error.

**Source:** `defect-vs-error-vs-failure.md`
</details>

---

### Q34: Can a defect exist without a failure? Can a failure occur without a defect?
**Keywords:** Conditions, Environment, Data, Misuse
<details>
<summary>Click to Reveal Answer</summary>

Yes to both. A defect only becomes a failure when specific inputs or conditions execute it (some never do). Some failures have no code defect, for example caused by the environment, data, hardware, misuse or unsupported platforms. That is why you check environment and data before reporting.

**Source:** `defect-vs-error-vs-failure.md`
</details>

---

### Q35: What are false positives and false negatives in testing?
**Keywords:** False alarm, Missed defect
<details>
<summary>Click to Reveal Answer</summary>

A **false positive** is a false alarm (a test reports a problem where there is none). A **false negative** is a missed defect (tests pass even though a defect exists). False negatives are more dangerous because they give false confidence.

**Source:** `defect-vs-error-vs-failure.md`
</details>

---

### Q36: What is the difference between Quality Assurance and Quality Control?
**Keywords:** Process, Product, Preventive, Detective
<details>
<summary>Click to Reveal Answer</summary>

**QA** is process-oriented, preventive and proactive and spans the life cycle (standards, audits, reviews, training, checklists, quality gates, Definition of Done, retrospectives). **QC** is product-oriented, detective and corrective, mostly reactive (testing, inspection, defect finding, measuring against criteria). **Testing is a QC activity.** You need both prevention and detection; neither alone is enough.

**Source:** `quality-assurance-vs-quality-control.md`
</details>

---

### Q37: What are the four parts of the cost of quality?
**Keywords:** Prevention, Appraisal, Internal failure, External failure
<details>
<summary>Click to Reveal Answer</summary>

Prevention costs (training, standards, reviews), appraisal costs (testing, inspection), internal failure costs (rework before release) and external failure costs (defects found by customers). Investing in prevention tends to reduce failure costs, and defects found late cost much more.

**Source:** `quality-assurance-vs-quality-control.md`
</details>

---

### Q38: What is the difference between verification and validation?
**Keywords:** Built right, Right product, Specifications, User needs
<details>
<summary>Click to Reveal Answer</summary>

**Verification** asks "Are we building the product right?" (checks work products against specifications and standards). **Validation** asks "Are we building the right product?" (checks the product against real user and business needs). House analogy: the inspector checking the blueprint is verification; the family living in the house is validation. Verification is mostly static (reviews, inspections, walkthroughs, linting) and validation mostly dynamic (acceptance testing, UAT, alpha/beta, usability testing).

**Source:** `verification-vs-validation.md`
</details>

---

### Q39: List the seven principles of testing.
**Keywords:** Presence of defects, Exhaustive impossible, Early testing, Clustering, Pesticide, Context, Absence-of-errors fallacy
<details>
<summary>Click to Reveal Answer</summary>

1. Testing shows the presence of defects, not their absence.
2. Exhaustive testing is impossible.
3. Early testing saves time and money.
4. Defects cluster together.
5. Tests wear out (the pesticide paradox).
6. Testing is context dependent.
7. Absence-of-errors is a fallacy: a defect-free product can still fail users if it is not what they need.

These are the ISTQB principles and guide prioritization, risk-based thinking and stopping decisions.

**Source:** `testing-principles.md`
</details>

---

### Q40: What is the difference between positive and negative testing?
**Keywords:** Valid input, Invalid input, Fail safely, Robustness
<details>
<summary>Click to Reveal Answer</summary>

**Positive** testing checks that the product works with valid input (builds confidence). **Negative** testing checks that it fails safely with invalid, unexpected or hostile input (builds robustness, security, good error messages and data integrity). "Positive" and "negative" describe the *input and scenario*, not whether the test passed. A negative test that correctly shows an error message is a passing test.

**Source:** `positive-and-negative-testing.md`
</details>

---

### Q41: What are the strengths and weaknesses of manual and automated testing?
**Keywords:** Exploration, Judgment, Speed, Repeatability, Maintenance
<details>
<summary>Click to Reveal Answer</summary>

**Manual:** strong at exploration, usability, visual checks and judgment; weak on speed, repetition and scalability. **Automated:** strong on speed, repeatability and CI/CD integration; weak on upfront cost, maintenance, flakiness and blindness to usability. Neither is better overall; use a hybrid: automate the repetitive, stable and high-risk checks; keep new, changing, subjective and exploratory work manual.

**Source:** `manual-vs-automated-testing.md`
</details>

---

### Q42: What is the test pyramid?
**Keywords:** Many unit, Some API, Few UI
<details>
<summary>Click to Reveal Answer</summary>

The test pyramid recommends many fast unit tests at the base, a moderate number of API/integration tests in the middle and few UI tests at the top. UI tests are slower and more brittle, so too many of them (the "ice cream cone") is an anti-pattern.

**Source:** `manual-vs-automated-testing.md`
</details>

---

### Q43: Name the traits of an effective tester.
**Keywords:** Curiosity, Critical thinking, Skepticism, Communication, Empathy
<details>
<summary>Click to Reveal Answer</summary>

Curiosity, critical thinking, skepticism, attention to detail, systems thinking, empathy for the user, communication, tenacity, humility, risk awareness and continuous learning. All of them can be practised. Testers question and challenge; developers lean toward building; both are partners, not rivals.

**Source:** `testing-mindset.md`
</details>

---

## Intermediate (Application)

### Q44: Classify: "A user enters 'abc' in the age field, the app crashes." Identify error, defect and failure, and positive or negative.
**Hint:** Walk the chain from cause to effect.
**Keywords:** Failure, Defect, Error, Negative test
<details>
<summary>Click to Reveal Answer</summary>

The crash is the **failure** (what the tester observes). The **defect** is the missing or faulty input validation in the code (or a requirement that never defined invalid-type handling). The **error** is the human mistake behind it, for example the developer assuming only numbers would be entered. The test is a **negative** test (invalid input). A good negative expected result is a clear message, no crash, no data loss and unchanged state.

**Source:** `defect-vs-error-vs-failure.md`; `positive-and-negative-testing.md`
</details>

---

### Q45: Should the team automate every test? How would you decide what to automate first?
**Keywords:** ROI, Break-even, Run frequency, Stable, High-risk
<details>
<summary>Click to Reveal Answer</summary>

No. Automation is not 100%, not a silver bullet and not a replacement for testers; a green run is not proof of quality. Use a checklist and an **ROI/break-even** estimate. The number of times a test will run is the biggest factor. Automate repetitive, stable, high-risk checks (such as login smoke and regression) and keep new, changing, visual and exploratory work manual. Follow the test pyramid, and remember maintenance is never finished (select, design, build, run, maintain, report).

**Source:** `manual-vs-automated-testing.md`
</details>

---

### Q46: A product passes all reviews and tests against its spec but users reject it. Which principle and concept explain this?
**Keywords:** Absence-of-errors fallacy, Validation, Verification
<details>
<summary>Click to Reveal Answer</summary>

It is the **absence-of-errors fallacy** (principle 7): a defect-free product can still fail if it is not what users need. It *passed verification* (built right) but *failed validation* (not the right product). The fix is validation activities earlier: involve users, demos, usability testing, Product Owner acceptance and UAT.

**Source:** `testing-principles.md`; `verification-vs-validation.md`
</details>

---

### Q47: Most bugs in a release come from the registration module. How do you adjust your plan?
**Keywords:** Defect clustering, Focus, Baseline, Risk
<details>
<summary>Click to Reveal Answer</summary>

This is **defect clustering**. Track defects by module and put extra testing effort where they concentrate (for example, deeper tests and more exploratory sessions for registration), but keep baseline testing in other areas because clusters can move. Also vary and refresh tests to avoid the pesticide paradox.

**Source:** `testing-principles.md`
</details>

---

## Advanced (Deep Dive)

### Q48: Why is exhaustive testing impossible, and how do we responsibly test anyway?
**Keywords:** Combinations, Risk-based, Techniques, Exit criteria
<details>
<summary>Click to Reveal Answer</summary>

Input combinations multiply into astronomical numbers (the lesson's 7-factor example alone has 10,800 combinations, and real systems add data values, states, timing and environments). So we choose tests wisely: apply **risk-based** thinking (Likelihood x Impact), use test design techniques (EP, BVA, decision tables, state transition) to select a small, justifiable set, and decide when to stop using exit criteria agreed in the test plan. We communicate coverage and remaining risk honestly because testing can show the presence but never the absence of defects.

**Source:** `testing-principles.md`; `testing-mindset.md`
</details>

---

# Day 4 (Thursday): Test Design Techniques

## Beginner (Foundational)

### Q49: What is black-box testing?
**Keywords:** Inputs and outputs, Specification, No code knowledge, Oracle
<details>
<summary>Click to Reveal Answer</summary>

Black-box testing checks behavior through inputs and outputs using the specification as the **oracle**, without relying on internal code. Strengths: user perspective, can start early, independent of implementation. Weaknesses: blind to unspecified code, possible redundancy and dependence on specification quality.

**Source:** `black-box-testing.md`
</details>

---

### Q50: Define Equivalence Partitioning.
**Keywords:** Classes, Same behavior, One representative, Valid and invalid
<details>
<summary>Click to Reveal Answer</summary>

EP divides inputs into classes that should behave the same way and tests one representative from each. It addresses "exhaustive testing is impossible". Partitions must not overlap and must not leave gaps. Always include invalid partitions (and empty). For an age field of 18 to 60, the partitions are below 18, 18 to 60 and above 60, plus non-numeric and empty.

**Source:** `equivalence-partitioning.md`
</details>

---

### Q51: What is Boundary Value Analysis and why does it work?
**Keywords:** Edges, Off-by-one, Defect clustering, 2-value vs 3-value
<details>
<summary>Click to Reveal Answer</summary>

BVA designs tests from values at and next to the edges of ranges, because defects cluster at boundaries (off-by-one errors, `<` vs `<=` confusion, fence-post errors, ambiguous wording). For 18 to 60: **2-value BVA** (ISTQB convention) tests 17, 18, 60, 61; **3-value BVA** (common industry practice) tests 17, 18, 19, 59, 60, 61. If the edges work, the middle almost certainly works.

**Source:** `boundary-value-analysis.md`
</details>

---

### Q52: Explain the test design chain from test basis to expected result.
**Keywords:** Test basis, Test condition, Test case, Test data, Expected result
<details>
<summary>Click to Reveal Answer</summary>

Test design flows from the **test basis** (requirements, stories, use cases) to **test conditions** (what to test), to **test cases**, to **test data** and the **expected result**, with a **test oracle** deciding what "correct" means. The expected result must be derived from the requirement, not from the code under test.

**Source:** `black-box-testing.md`
</details>

---

### Q53: What are the three families of test design techniques?
**Keywords:** Black-box, White-box, Experience-based
<details>
<summary>Click to Reveal Answer</summary>

Black-box (specification-based: EP, BVA, decision tables, state transition, use-case), white-box (structure-based, covered on Friday) and experience-based (error guessing, exploratory testing).

**Source:** `black-box-testing.md`
</details>

---

### Q54: When do you use decision table testing?
**Keywords:** Combinations of conditions, Business rules, Rules, 2^n
<details>
<summary>Click to Reveal Answer</summary>

Use it for business rules where **combinations of conditions** determine the outcome, since EP and BVA test one field at a time and can miss combination defects. A table has conditions (inputs), actions (outputs), rules (columns), condition entries (T/F/-) and action entries. A full limited-entry table has 2^n rules for n Boolean conditions. Each rule becomes at least one test case.

**Source:** `decision-table-testing.md`
</details>

---

### Q55: What is state transition testing, and what are the main vocabulary terms?
**Keywords:** State, Event, Transition, Action, Guard
<details>
<summary>Click to Reveal Answer</summary>

It is used when a system's response to an event depends on its **current state**, which depends on history (for example a login lockout after failed attempts). Vocabulary: state, event (trigger), transition, action (output), guard condition, initial and final state, valid and invalid transitions and self-transitions. Test cases are event sequences from the initial state; check the output and end state after each step.

**Source:** `state-transition-testing.md`
</details>

---

### Q56: What is error guessing and why does it work?
**Keywords:** Experience, Defects cluster, Developers repeat mistakes, Fault list
<details>
<summary>Click to Reveal Answer</summary>

An experience-based technique where you anticipate likely defects and design tests to expose them. It works because defects cluster, developers repeat mistakes, human errors are predictable and specifications are silent in many places. Typical ideas: empty and whitespace, very long input, special characters and Unicode, code-like text treated as plain data, double submit, Back button, session expiry, dates, files and permissions. It complements, never replaces, EP, BVA and use-case testing.

**Source:** `error-guessing.md`
</details>

---

### Q57: What is use-case testing?
**Keywords:** Actor, Goal, Main flow, Alternative flow, Exception flow
<details>
<summary>Click to Reveal Answer</summary>

Use-case testing derives black-box tests from how an actor and the system interact to reach a goal. Anatomy: name/ID, actors, goal, preconditions, trigger, main flow, alternative flows, exception flows, postconditions and business rules. Create one test for the main flow and one for each alternative and exception flow. Use-case coverage = flows covered / total flows.

**Source:** `use-case-testing.md`
</details>

---

### Q58: What is the difference between a user story, a use case and a test case?
**Keywords:** Value, Interaction, Verifies one path
<details>
<summary>Click to Reveal Answer</summary>

A **user story** is a short statement of value ("As a... I want... so that..."). A **use case** is a detailed description of the interaction between an actor and the system, including flows. A **test case** verifies one path (one scenario) with specific data and an expected result.

**Source:** `use-case-testing.md`
</details>

---

### Q59: What is a test oracle?
**Keywords:** Expected result, Source of truth, Specification
<details>
<summary>Click to Reveal Answer</summary>

A test oracle is the source that tells you what the correct result should be, typically the requirement, specification, user story acceptance criteria or use-case postconditions. Expected results should be written from the oracle *before* running the test, never copied from the program's actual output.

**Source:** `black-box-testing.md`; `data-driven-testing.md`
</details>

---

## Intermediate (Application)

### Q60: Apply EP and BVA to an age field accepting 18 to 60. How many tests does each approach need?
**Hint:** Count partitions, then add boundary values.
**Keywords:** 6 tests, 9 tests, Exhaustive, Complementary
<details>
<summary>Click to Reveal Answer</summary>

Per the lesson, EP needs **6 tests** (one per partition, including invalid ones such as non-numeric and empty), EP plus BVA needs **9**, and exhaustive testing needs well over 121. EP finds class-level defects; BVA finds edge-level defects, so they work best together. Boundary tests would be 17, 18, 19, 59, 60, 61 (3-value) and each should satisfy all other rules, with one boundary per test.

**Source:** `equivalence-partitioning.md`; `boundary-value-analysis.md`
</details>

---

### Q61: A discount applies if the customer is a member AND the order exceeds the minimum, OR if they have a coupon, unless the item is excluded. Which technique do you use and how do you build it?
**Hint:** Look at the words "and", "or", "unless".
**Keywords:** Decision table, 2^n, Infeasible, Collapse, Completeness
<details>
<summary>Click to Reveal Answer</summary>

A **decision table**, because combinations of conditions decide the outcome. List the conditions and actions, build the full set of 2^n rules (with the halving pattern for T/F values), mark infeasible combinations with reasons, merge rules with don't-care dashes only when actions are genuinely identical, then check **completeness** (covered counts add up to the full total) and **consistency** (no contradictions). Each rule becomes at least one test. Translating text with if/and/or/unless/otherwise into a table also exposes ambiguities and gaps before coding.

**Source:** `decision-table-testing.md`
</details>

---

### Q62: A login locks after 3 failed attempts. How do you test it?
**Keywords:** State transition, Guard condition, BVA, Invalid transitions
<details>
<summary>Click to Reveal Answer</summary>

Model it as states (for example Logged out, Locked) with events (failed attempt, correct login, unlock) and a **guard condition** (attempt count). Test the guard with both true and false outcomes, applying BVA to the boundary: 2, 3 and 4 attempts. Test valid transitions as event sequences, test invalid transitions (for example login while locked) in short separate tests, and confirm the state did not change. Where relevant, test important invalid transitions at the API level, not only in the UI. Also look for gaps such as a missing time-based unlock event.

**Source:** `state-transition-testing.md`
</details>

---

### Q63: You have 5 fields on a registration form. How do you design tests without a combinatorial explosion?
**Keywords:** Each valid partition once, One invalid at a time, Masking
<details>
<summary>Click to Reveal Answer</summary>

Do not take the cartesian product. Cover each valid partition at least once (each choice), then test **invalid partitions one at a time** with all other fields valid so one invalid value does not mask another. Use BVA per field, one field at a time. For real business-rule combinations use decision tables or pairwise testing.

**Source:** `equivalence-partitioning.md`; `boundary-value-analysis.md`
</details>

---

## Advanced (Deep Dive)

### Q64: You must choose test design techniques for an online checkout (quantity field, coupon rules, order status flow). Explain your layered approach and coverage measures.
**Keywords:** Layered, EP/BVA, Decision table, State transition, Coverage
<details>
<summary>Click to Reveal Answer</summary>

Real features need layered, combined techniques. Use **EP and BVA** for the quantity field (valid, invalid, and edge values like 0, 1, max, max+1), a **decision table** for the coupon/discount rule combinations (coverage = rules exercised / total feasible rules x 100, stating whether the table is full or collapsed), **state transition** testing for the order status flow (cover all states, valid transitions (0-switch), then invalid transitions or 1-switch sequences as risk demands), **use-case testing** for the end-to-end purchase (flows covered / total flows) and **error guessing** for experience-based extras (double-click on pay, Back button). Trace it all to requirements to show requirements coverage. Be aware of limitations: EP depends on a good requirement and state models can explode, so use focused models.

**Source:** `black-box-testing.md`; `state-transition-testing.md`; `decision-table-testing.md`
</details>

---

# Day 5 (Friday): Advanced Testing Concepts

## Beginner (Foundational)

### Q65: What is white-box testing and who usually does it?
**Keywords:** Internal structure, Developers/SDETs, Unit level, Coverage
<details>
<summary>Click to Reveal Answer</summary>

White-box (structure-based, glass-box, clear-box) testing designs and measures tests using the internal structure of the code. Black-box asks "does it do what it should?"; white-box asks "have we exercised what we built?" It is done mainly by developers and SDETs at unit, component and integration level, plus code reviews and static analysis.

**Source:** `white-box-testing.md`
</details>

---

### Q66: Define statement coverage and branch coverage.
**Keywords:** Executed/total statements, Decision outcomes, Branch implies statement
<details>
<summary>Click to Reveal Answer</summary>

**Statement coverage** = executed statements / total statements. **Branch coverage** = executed decision outcomes / total outcomes. 100% branch coverage implies 100% statement coverage, but not the reverse, so measure branches (for example `pytest --cov=module --cov-branch --cov-report=term-missing`).

**Source:** `white-box-testing.md`
</details>

---

### Q67: What is cyclomatic complexity?
**Keywords:** V(G) = E - N + 2P, Decision points + 1, Independent paths
<details>
<summary>Click to Reveal Answer</summary>

A measure of the number of independent paths through code: V(G) = E - N + 2P (edges, nodes, connected components), which equals decision points + 1. It gives the minimum number of tests for path coverage and a risk signal: higher complexity means harder to test and maintain.

**Source:** `white-box-testing.md`
</details>

---

### Q68: What is the difference between functional and non-functional testing?
**Keywords:** What it does, How well, Quality attributes
<details>
<summary>Click to Reveal Answer</summary>

**Functional** testing asks "what does the system do?" and verifies features, business rules and data handling against functional requirements. **Non-functional** testing asks "how well?" and verifies quality attributes such as performance, reliability, security, usability, accessibility, compatibility and maintainability. A feature that works but takes 30 seconds is still a failure from the user's viewpoint.

**Source:** `functional-vs-non-functional-testing.md`
</details>

---

### Q69: Differentiate smoke, sanity, retesting and regression testing.
**Keywords:** Broad shallow, Narrow focused, Confirm fix, Side effects
<details>
<summary>Click to Reveal Answer</summary>

- **Smoke:** broad and shallow; is the build alive and testable?
- **Sanity:** narrow and focused; does this specific fix or change work?
- **Retesting (confirmation):** re-run the failed test to confirm the specific defect is fixed.
- **Regression:** wide and thorough; did the change break anything that used to work?

After a fix the typical order is smoke, retest, sanity, then regression.

**Source:** `regression-testing.md`; `functional-vs-non-functional-testing.md`
</details>

---

### Q70: What is exploratory testing?
**Keywords:** Simultaneous learning, design, execution, Charter, Session
<details>
<summary>Click to Reveal Answer</summary>

Simultaneous learning, test design and execution, guided by the tester's skill. It is structured and purposeful, not random clicking. A **charter** states the mission: *Explore* target *with* resources *to discover* information. Session-based test management uses time-boxed, uninterrupted sessions, session sheets and PROOF debriefs. It differs from scripted testing (planned in advance, repeatable) and ad-hoc testing (unstructured, undocumented).

**Source:** `exploratory-testing.md`
</details>

---

### Q71: What is data-driven testing?
**Keywords:** Separate logic and data, Parametrize, CSV/JSON, Rows
<details>
<summary>Click to Reveal Answer</summary>

Separating test logic from test data: write the steps once and run them against many rows ("one recipe, many ingredient lists"). In pytest, `@pytest.mark.parametrize` creates one test per row, and every row runs even if another fails. Data can live in CSV/JSON (remember CSV values are text). Test design techniques decide *which* data; DDT is *how* you run it.

**Source:** `data-driven-testing.md`
</details>

---

### Q72: What is a regression and when should regression testing run?
**Keywords:** Used to work, Change, Selection, Tiers
<details>
<summary>Click to Reveal Answer</summary>

A regression is something that used to work and no longer does because of a change. Regression testing re-runs existing tests to catch such damage. Run it after fixes, features, refactoring, configuration and dependency changes, before release, nightly and on commits or pull requests. Regressions also come from shared code, configuration, dependency upgrades, data migrations and merge conflicts, not only edited code.

**Source:** `regression-testing.md`
</details>

---

### Q73: Define load, stress, spike and endurance (soak) testing.
**Keywords:** Expected load, Beyond limits, Sudden surge, Long duration
<details>
<summary>Click to Reveal Answer</summary>

**Load:** behavior under expected/realistic load. **Stress:** push beyond limits to find the breaking point and how the system recovers. **Spike:** sudden surges of users. **Endurance (soak):** sustained load over a long time to find memory leaks and degradation. Volume testing uses large data amounts.

**Source:** `performance-and-stress-testing.md`; `functional-vs-non-functional-testing.md`
</details>

---

### Q74: What are reliability, availability, SLI, SLO and SLA?
**Keywords:** Failure-free operation, MTBF/MTTR, Measure, Target, Promise
<details>
<summary>Click to Reveal Answer</summary>

**Reliability** is the probability of failure-free operation for a stated time in a stated environment (ISO 25010: maturity, availability, fault tolerance, recoverability). **Availability = MTBF / (MTBF + MTTR)** = uptime / (uptime + downtime). **SLI** is what you measure, **SLO** is the target, **SLA** is the promise to customers. The **error budget** is what the SLO allows you to "spend". RTO is how long you can be down; RPO is how much data you can lose.

**Source:** `reliability-and-scalability.md`
</details>

---

### Q75: What is the difference between scaling up and scaling out?
**Keywords:** Vertical, Horizontal, Elasticity, Stateless
<details>
<summary>Click to Reveal Answer</summary>

Scale **up** (vertical) means a bigger machine; scale **out** (horizontal) means more machines. **Elasticity** is automatic scaling to match demand. Stateless services scale out more easily; state must be managed with shared stores, watching for sticky sessions and replication lag.

**Source:** `reliability-and-scalability.md`
</details>

---

## Intermediate (Application)

### Q76: A 99.9% availability SLA is promised. How much downtime is allowed per year, and what about 99.99%?
**Keywords:** 8.76 hours, 52.56 minutes, Each nine tenfold
<details>
<summary>Click to Reveal Answer</summary>

99.9% allows about **8.76 hours** of downtime per year; 99.99% allows about **52.56 minutes**; 99.999% about 5.3 minutes. Each additional "nine" cuts the allowed downtime tenfold. Faster recovery (lower MTTR) is often the most efficient way to improve availability.

**Source:** `reliability-and-scalability.md`
</details>

---

### Q77: Your load test shows average response time of 1.2 seconds, so the team calls it a pass. What would you challenge?
**Hint:** Averages mislead.
**Keywords:** Percentiles, p95/p99, Error rate, Think time, Realistic workload
<details>
<summary>Click to Reveal Answer</summary>

Averages hide slow tails. Report percentiles (p50, p90, p95, p99), show the error rate beside them and never average percentiles. Check that there were measurable NFRs, a realistic workload model (journey mix, think time, pacing) and an environment representative of production. Look for common mistakes such as happy-path-only scripts, no server monitoring and load from a weak laptop on Wi-Fi. Find the bottleneck by asking which resource saturated first; rising response time with low CPU suggests something is waiting (pools, database, third party). Only test systems you own or have written permission to test.

**Source:** `performance-and-stress-testing.md`
</details>

---

### Q78: Your regression suite takes 8 hours and has flaky tests. How do you improve it?
**Keywords:** Risk-based selection, Tiers, Quarantine, Parallelize, Pesticide paradox
<details>
<summary>Click to Reveal Answer</summary>

Select tests using risk (Likelihood x Impact), impact analysis (changes, traceability), coverage, history and requirement priority. Organize tiers: smoke (minutes), core (about an hour), full (nightly, weekend, pre-release). Quarantine and fix flaky tests, parallelize and follow the test pyramid. Review the suite regularly (bloat, flakiness, obsolescence) and give it owners. Keep manual and exploratory testing for judgment. Measure leakage, pass rate, flakiness and execution time with thresholds agreed in advance.

**Source:** `regression-testing.md`
</details>

---

### Q79: You have a new feature, thin specifications and one day to test it. Which approach do you choose and how do you report it?
**Keywords:** Exploratory, Charters, Sessions, Heuristics, Debrief
<details>
<summary>Click to Reveal Answer</summary>

Exploratory testing shines for new features, thin specs, tight deadlines and unknown risks. Write focused charters (not too broad or narrow), run time-boxed sessions, use heuristics (SFDIPOT, CRUD, Goldilocks, Zero-One-Many, tours, HICCUPPS), capture time-stamped notes and evidence, and log bugs in Jira. Report it as a story of charters, sessions, findings, risks and what was *not* covered, rather than only a bug count, and convert findings into regression/automation candidates.

**Source:** `exploratory-testing.md`
</details>

---

## Advanced (Deep Dive)

### Q80: Your unit tests report 100% branch coverage but a serious bug reached production. Explain how, and what you would change.
**Keywords:** Assertions, Wrong expectations, Missing requirements, Mutation testing, Black-box
<details>
<summary>Click to Reveal Answer</summary>

100% coverage is not bug-free. Coverage only shows code was *executed*, not that behavior was *verified*. Tests with no assertions, wrong expectations or missing requirements (code that was never written) slip through. Remedies: check assertion quality and expected results against requirements, add **mutation testing** (deliberate small bugs to see whether tests detect them), add loop tests (zero, one, many, maximum), data-flow testing where relevant and use black-box techniques (requirements decide *what* to test; coverage shows what you have not yet looked at). Treat coverage targets as a context-dependent floor, not a goal.

**Source:** `white-box-testing.md`
</details>
