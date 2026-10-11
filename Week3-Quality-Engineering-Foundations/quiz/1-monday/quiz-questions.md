# Weekly Knowledge Check: Day 1 - SDLC, STLC & Agile (Week3-Quality-Engineering-Foundations)

Welcome to the Monday practice quiz. It covers today's six lessons: SDLC fundamentals, Waterfall/Agile/Scrum/Kanban/Hybrid approaches, the Software Testing Life Cycle (STLC), Agile roles and responsibilities, Scrum ceremonies and the sprint lifecycle, and the introduction to Jira.

**How to use this quiz**

1. Attempt every question on your own first. Tick your answer (or write it down) before you open anything.
2. Only then click "Click for Solution" under the question to check your answer, read the explanation, and see which lesson section it comes from.
3. If you miss a question, re-read the lesson section named in its **Source** line, then try the question again the next day.
4. Questions are mixed: about 40% recall, 40% understanding and 20% application. Some facts are asked more than once in a different style on purpose, because seeing the same idea in a new form is good practice.
5. Sprint timeboxes in this quiz refer to a **2-week sprint** unless stated otherwise.

---

## Part 1: Multiple Choice

Choose the single best answer.

**Question 1.** What is the main focus of the Sprint Retrospective?

- [ ] A) Inspecting the Increment with stakeholders and gathering feedback
- [ ] B) How the Scrum Team worked: people, interactions, processes, tools and the Definition of Done, and what to improve
- [ ] C) Selecting items from the Product Backlog and agreeing the Sprint Goal
- [ ] D) Planning the next 24 hours and surfacing blockers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) How the Scrum Team worked: people, interactions, processes, tools and the Definition of Done, and what to improve

**Explanation:** The Retrospective inspects the way of working and commits to concrete improvements. The Review looks at the product; the Retrospective looks at the way of working.

- **Why others are wrong:**
  - A) That describes the Sprint Review.
  - C) That describes Sprint Planning.
  - D) That describes the Daily Scrum.
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "Event 5: Sprint Retrospective"
</details>

---

**Question 2.** Which of the following is a NON-FUNCTIONAL requirement for a food-ordering app?

- [ ] A) A customer can add a dish to the cart.
- [ ] B) A customer can save a delivery address.
- [ ] C) A customer can place an order.
- [ ] D) The menu page loads within 3 seconds on a standard mobile connection.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The menu page loads within 3 seconds on a standard mobile connection.

**Explanation:** Non-functional requirements describe how well the system does something (speed, security, usability, availability); a load-time target is one.

- **Why others are wrong:**
  - A) This says what the system does, so it is functional.
  - B) Saving an address is a capability, so it is functional.
  - C) Placing an order is a capability, so it is functional.
- **Source:** `sdlc-fundamentals.md`, section "7. Phase 2: Requirements Analysis"
</details>

---

**Question 3.** Which set of outputs is typical of the Design phase?

- [ ] A) HLD and LLD documents, architecture diagrams and UI wireframes
- [ ] B) Source code, unit tests and build artifacts
- [ ] C) Live system, release record and release notes
- [ ] D) Patches, new versions and retirement plans

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) HLD and LLD documents, architecture diagrams and UI wireframes

**Explanation:** Design produces HLD and LLD documents, architecture diagrams, database designs and UI wireframes or prototypes.

- **Why others are wrong:**
  - B) Those are outputs of Implementation.
  - C) Those are outputs of Deployment.
  - D) Those are outputs of Maintenance.
- **Source:** `sdlc-fundamentals.md`, section "8. Phase 3: Design"
</details>

---

**Question 4.** According to the lesson's illustrative table, a defect found during Testing costs about how many times as much to fix as one found in Requirements?

- [ ] A) About 5x
- [ ] B) About 10x
- [ ] C) About 20x
- [ ] D) About 50x to 100x

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) About 20x

**Explanation:** The illustration shows Requirements 1x, Design about 5x, Implementation about 10x, Testing about 20x, and Production 50x to 100x or more.

- **Why others are wrong:**
  - A) About 5x is the Design phase figure.
  - B) About 10x is the Implementation (coding) figure.
  - D) 50x to 100x or more is the figure for defects found after release.
- **Source:** `sdlc-fundamentals.md`, section "14. The cost of finding defects late"
</details>

---

**Question 5.** What does "shift-left" mean in quality engineering?

- [ ] A) Removing the testing phase and relying on developers' unit tests alone
- [ ] B) Running the same tests faster by using automation only
- [ ] C) Moving quality activities such as requirement reviews and test design earlier in the life cycle
- [ ] D) Moving defect fixing to the maintenance phase, where it is cheaper

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Moving quality activities such as requirement reviews and test design earlier in the life cycle

**Explanation:** Shift-left means starting quality work earlier (reviewing requirements and designs, writing tests early, automating checks early) to prevent or find defects while they are cheap to fix.

- **Why others are wrong:**
  - A) The lesson says shift-left does not mean stop testing at the end; it means start quality work at the beginning and keep going.
  - B) Automation can be part of shift-left, but the idea is about timing (earlier), not speed.
  - D) Late fixes cost more, not less, which is the very reason for shifting left.
- **Source:** `sdlc-fundamentals.md`, section "14. The cost of finding defects late"
</details>

---

**Question 6.** Which statement about the Definition of Ready (DoR) and the Definition of Done (DoD) is correct?

- [ ] A) The DoD is an official Scrum commitment for the Increment, while the DoR is a widely used team practice and not an official Scrum artifact
- [ ] B) The DoR is an official Scrum commitment, while the DoD is only an optional team practice
- [ ] C) They are two names for the same checklist
- [ ] D) The DoR applies when work is finished and the DoD applies before work starts

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The DoD is an official Scrum commitment for the Increment, while the DoR is a widely used team practice and not an official Scrum artifact

**Explanation:** The DoD is the official commitment of the Increment; the DoR is a common practice that checks a story is clear enough to start ("Ready is the front door; Done is the exit").

- **Why others are wrong:**
  - B) The roles are reversed: the DoD is official, the DoR is not.
  - C) They answer different questions at different times.
  - D) The timing is reversed: Ready applies before work starts, Done when it is finished.
- **Source:** `agile-roles-and-responsibilities.md`, section "7. Definition of Ready vs. Definition of Done"
</details>

---

**Question 7.** Which quality engineer activity does the lesson list for the Deployment phase?

- [ ] A) Reviewing wireframes against requirements
- [ ] B) Writing unit tests for the cart
- [ ] C) Estimating testing effort for the project plan
- [ ] D) Giving go/no-go input and running post-release smoke checks

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Giving go/no-go input and running post-release smoke checks

**Explanation:** For Deployment, the QE takes part in the go/no-go decision, verifies version and configuration, and runs smoke checks in production.

- **Why others are wrong:**
  - A) Reviewing wireframes is a Design-phase activity.
  - B) Unit tests are written by developers during Implementation.
  - C) Effort estimation belongs to the Planning phase.
- **Source:** `sdlc-fundamentals.md`, section "13. Phase summary table and 11. Phase 6: Deployment"
</details>

---

**Question 8.** In pure Waterfall, when does the testing phase begin?

- [ ] A) In parallel with requirements gathering
- [ ] B) Only after coding is finished
- [ ] C) After each two-week cycle
- [ ] D) After each module design is signed off

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Only after coding is finished

**Explanation:** In pure Waterfall testing is its own phase that begins only after coding is finished, which causes the late-testing problem.

- **Why others are wrong:**
  - A) Early test planning in parallel with phases is the V-Model idea, not pure Waterfall.
  - C) Two-week cycles describe Agile or Scrum, not Waterfall.
  - D) Pairing testing with each design phase is the V-Model; pure Waterfall waits until coding ends.
- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "2.5 Testing's role and the late-testing problem"
</details>

---

**Question 9.** In the V-Model, which test level is paired with architecture / high-level design?

- [ ] A) Integration testing
- [ ] B) Unit testing
- [ ] C) System testing
- [ ] D) Acceptance testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Integration testing

**Explanation:** The V-Model pairs architecture / high-level design with integration testing (do the modules work together?).

- **Why others are wrong:**
  - B) Unit testing is paired with module (detailed) design.
  - C) System testing is paired with system requirements / design.
  - D) Acceptance testing is paired with business requirements.
- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "3. The V-Model (a Waterfall variant)"
</details>

---

**Question 10.** Which Jira product family is mainly intended for IT support and service desks?

- [ ] A) Jira Software
- [ ] B) Jira Work Management
- [ ] C) Jira Data Center
- [ ] D) Jira Service Management

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Jira Service Management

**Explanation:** Jira Service Management is for IT support, customer support and service desks, with a request portal and SLA tracking.

- **Why others are wrong:**
  - A) Jira Software is for software and engineering teams (the product used in this course).
  - B) Jira Work Management is for business teams such as marketing, HR and finance.
  - C) Data Center is a way of delivering Jira (self-managed), not a product family.
- **Source:** `introduction-to-jira.md`, section "3. Jira Product Families"
</details>

---

**Question 11.** The Agile Manifesto says it values "working software" more than what?

- [ ] A) Individuals and interactions
- [ ] B) Customer collaboration
- [ ] C) Comprehensive documentation
- [ ] D) Responding to change

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Comprehensive documentation

**Explanation:** The four values are: individuals and interactions over processes and tools; working software over comprehensive documentation; customer collaboration over contract negotiation; responding to change over following a plan.

- **Why others are wrong:**
  - A) Individuals and interactions are valued over processes and tools, not over working software.
  - B) Customer collaboration is itself a valued item, placed over contract negotiation.
  - D) Responding to change is itself a valued item, placed over following a plan.
- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "4.2 The four values of the Agile Manifesto"
</details>

---

**Question 12.** Which description best fits the Scrum Master?

- [ ] A) A project manager who assigns tasks and tracks individual hours
- [ ] B) A servant leader who facilitates events, coaches the team and removes impediments
- [ ] C) The person who orders the Product Backlog and accepts finished work
- [ ] D) The tester who approves every story before it can be released

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A servant leader who facilitates events, coaches the team and removes impediments

**Explanation:** The Scrum Master is a servant leader accountable for establishing Scrum and the team's effectiveness: facilitating, coaching and removing impediments.

- **Why others are wrong:**
  - A) The lesson explicitly says the Scrum Master is not a project manager and does not assign tasks or track hours.
  - C) Ordering the backlog and accepting work are Product Owner responsibilities.
  - D) Scrum has no separate tester role, and the Scrum Master does not approve work.
- **Source:** `agile-roles-and-responsibilities.md`, section "3.2 The Scrum Master (SM)"
</details>

---

**Question 13.** Which Scrum artifact is paired with the commitment called the Sprint Goal?

- [ ] A) Product Backlog
- [ ] B) Sprint Backlog
- [ ] C) Increment
- [ ] D) Definition of Ready

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Sprint Backlog

**Explanation:** Product Backlog pairs with the Product Goal, Sprint Backlog with the Sprint Goal, and Increment with the Definition of Done.

- **Why others are wrong:**
  - A) The Product Backlog's commitment is the Product Goal.
  - C) The Increment's commitment is the Definition of Done.
  - D) The Definition of Ready is not an official Scrum artifact or commitment.
- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "5.4 The three artifacts; also scrum-ceremonies-and-sprint-lifecycle.md, 4. The Artifacts and Their Commitments"
</details>

---

**Question 14.** What is the main purpose of a WIP limit on a Kanban column?

- [ ] A) To cap the number of cards in the column so the team finishes work before starting more, which reduces context switching and exposes bottlenecks
- [ ] B) To set how many story points the team may commit to per sprint
- [ ] C) To limit how many testers may work on the board
- [ ] D) To fix how many days a card may stay in the Backlog column

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) To cap the number of cards in the column so the team finishes work before starting more, which reduces context switching and exposes bottlenecks

**Explanation:** A WIP limit caps work in progress. It reduces context switching, exposes bottlenecks and encourages finishing before starting ("stop starting, start finishing").

- **Why others are wrong:**
  - B) Story points per sprint relate to Scrum sprint scope and velocity, not Kanban WIP limits.
  - C) WIP limits count cards, not people.
  - D) A WIP limit caps how many cards are in a column, not how long a card may wait.
- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "6.4 WIP limits"
</details>

---

**Question 15.** A customer requests a feature on 2 May, the team starts work on 6 May and it is finished on 13 May. What is the LEAD time?

- [ ] A) 7 days
- [ ] B) 4 days
- [ ] C) 11 days
- [ ] D) 9 days

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 11 days

**Explanation:** Lead time runs from the request until delivery: 2 May to 13 May is 11 days. (Cycle time, from start of work, would be 7 days.)

- **Why others are wrong:**
  - A) 7 days is the cycle time (6 May to 13 May).
  - B) 4 days is only the waiting time before work started (2 May to 6 May).
  - D) 9 days does not match any pair of dates in the example; counting 2 May to 13 May gives 11.
- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "6.6 Cycle time and lead time"
</details>

---

**Question 16.** Which list shows the six classic STLC phases in the correct order?

- [ ] A) Test Planning, Requirement Analysis, Test Case Development, Test Environment Setup, Test Execution, Test Cycle Closure
- [ ] B) Requirement Analysis, Test Case Development, Test Planning, Test Environment Setup, Test Execution, Test Cycle Closure
- [ ] C) Requirement Analysis, Test Planning, Test Execution, Test Case Development, Test Environment Setup, Test Cycle Closure
- [ ] D) Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution, Test Cycle Closure

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution, Test Cycle Closure

**Explanation:** The six phases are Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution and Test Cycle Closure.

- **Why others are wrong:**
  - A) Requirement Analysis comes first; planning needs its output.
  - B) Test Planning comes before Test Case Development because the plan must be approved first.
  - C) Test Execution cannot come before the test cases and environment exist.
- **Source:** `software-testing-life-cycle.md`, section "6-11 (phases) and 12. All six phases at a glance"
</details>

---

**Question 17.** Which set of conditions describes the ENTRY criteria for Test Execution?

- [ ] A) The closure report is signed off and artifacts are archived
- [ ] B) The test plan is still being drafted and the environment is unknown
- [ ] C) Lessons learned are recorded and risks communicated
- [ ] D) Test cases and data are approved, the environment is ready with a passed smoke test, and the build is deployed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Test cases and data are approved, the environment is ready with a passed smoke test, and the build is deployed

**Explanation:** Execution may start when cases and data are ready and approved, the environment is ready and the smoke test passed, the build is deployed and the defect tracking tool is available.

- **Why others are wrong:**
  - A) Sign-off of the closure report is an exit criterion of Test Cycle Closure.
  - B) Execution cannot start while the plan and environment are unsettled.
  - C) Recording lessons learned and communicating risks are exit criteria of Test Cycle Closure.
- **Source:** `software-testing-life-cycle.md`, section "10. Phase 5: Test Execution"
</details>

---

**Question 18.** Which deliverable set belongs to the Test Environment Setup phase?

- [ ] A) A ready environment, an environment setup record and the smoke test result
- [ ] B) The test plan, effort estimate and risk list
- [ ] C) The test closure report and lessons learned
- [ ] D) A question log and a draft RTM

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A ready environment, an environment setup record and the smoke test result

**Explanation:** Environment setup delivers a ready working environment, a setup record (versions, URLs, configuration) and the smoke test result.

- **Why others are wrong:**
  - B) The test plan, estimate and risk list come from Test Planning.
  - C) The closure report and lessons learned come from Test Cycle Closure.
  - D) The question log and draft RTM come from Requirement Analysis.
- **Source:** `software-testing-life-cycle.md`, section "9. Phase 4: Test Environment Setup"
</details>

---

**Question 19.** What are SUSPENSION criteria?

- [ ] A) Conditions that must be true before a phase can start
- [ ] B) Conditions under which testing is paused because continuing would waste effort
- [ ] C) Conditions that confirm a defect has been fixed
- [ ] D) Conditions under which test cases are removed from the suite

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Conditions under which testing is paused because continuing would waste effort

**Explanation:** Suspension criteria say when testing is paused (for example, the login page does not load at all). Resumption criteria say what must be true to restart.

- **Why others are wrong:**
  - A) That describes entry criteria.
  - C) Confirming a fix is confirmation testing, not suspension criteria.
  - D) Suspension criteria pause testing; they do not delete test cases.
- **Source:** `software-testing-life-cycle.md`, section "5. Key vocabulary used in every phase"
</details>

---

**Question 20.** What is a Requirement Traceability Matrix (RTM)?

- [ ] A) A list of defects sorted by severity
- [ ] B) A schedule of test cycles per build
- [ ] C) A table that links each requirement to the tests that check it, showing coverage
- [ ] D) A list of the browsers and devices in the test environment

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A table that links each requirement to the tests that check it, showing coverage

**Explanation:** The RTM records links between requirements and test cases, so you can see at a glance which requirements have tests and which have none.

- **Why others are wrong:**
  - A) Defect lists are defect reports or distribution data, not the RTM.
  - B) A schedule is part of planning, not traceability.
  - D) Environment details are recorded in the environment setup record.
- **Source:** `software-testing-life-cycle.md`, section "8. Phase 3: Test Case Development"
</details>

---

**Question 21.** After a developer fixes a bug, the tester re-runs the exact test that failed to check that the fix worked. What is this called?

- [ ] A) Confirmation testing
- [ ] B) Regression testing
- [ ] C) Smoke testing
- [ ] D) Exploratory testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Confirmation testing

**Explanation:** Confirmation testing re-runs the failed test to check the specific defect is fixed.

- **Why others are wrong:**
  - B) Regression testing re-runs other tests to check the fix did not break existing behavior.
  - C) A smoke test is a very quick check that the most basic functions work.
  - D) Exploratory testing is learning, designing and executing at the same time without fully scripted steps.
- **Source:** `software-testing-life-cycle.md`, section "10. Phase 5: Test Execution and Knowledge Check Q12"
</details>

---

**Question 22.** Where does a QE or tester fit in the official Scrum framework?

- [ ] A) As a separate Tester role that reports to the Scrum Master
- [ ] B) Outside the Scrum Team, receiving finished builds
- [ ] C) As a stakeholder who attends the Sprint Review only
- [ ] D) Within the Developers, sharing accountability for the quality of the Increment

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Within the Developers, sharing accountability for the quality of the Increment

**Explanation:** Scrum has three accountabilities (Product Owner, Scrum Master, Developers). Testers, QA engineers, QEs and SDETs are part of the Developers.

- **Why others are wrong:**
  - A) Scrum has no separate tester role.
  - B) A QE outside the team is listed as an anti-pattern.
  - C) A QE is a team member, involved from refinement to review.
- **Source:** `agile-roles-and-responsibilities.md`, section "3.4 Where Do Testers and QE Fit?"
</details>

---

**Question 23.** The "Three Amigos" conversation brings together which three perspectives, and when is it held?

- [ ] A) Product Owner, Scrum Master and stakeholder, after the sprint ends
- [ ] B) Business/Product, Development and Testing, before development starts
- [ ] C) Developer, DevOps and architect, during the Sprint Review
- [ ] D) Customer, manager and tester, during the Retrospective

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Business/Product, Development and Testing, before development starts

**Explanation:** The Three Amigos is a short conversation about a user story among business, development and testing perspectives, held before development starts.

- **Why others are wrong:**
  - A) The perspectives are business, development and testing, and it is held before development, not after the sprint.
  - C) Those are not the three perspectives, and it is not a Sprint Review activity.
  - D) The conversation is about a story before building, not a Retrospective item, and those roles are not the three perspectives.
- **Source:** `agile-roles-and-responsibilities.md`, section "5.3 The Three Amigos"
</details>

---

**Question 24.** What is the typical timebox of the Sprint Review in a 2-week sprint?

- [ ] A) 15 minutes
- [ ] B) Up to 1.5 hours
- [ ] C) Up to 2 hours
- [ ] D) Up to 4 hours

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Up to 2 hours

**Explanation:** For a 2-week sprint the Review is up to 2 hours (the Scrum Guide maximum is 4 hours for a one-month sprint).

- **Why others are wrong:**
  - A) 15 minutes is the Daily Scrum timebox.
  - B) Up to 1.5 hours is the Sprint Retrospective.
  - D) Up to 4 hours is the typical Sprint Planning timebox for a 2-week sprint (and the Review maximum for a one-month sprint).
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "Timeboxes at a Glance"
</details>

---

**Question 25.** In Scrum estimation, what do story points represent?

- [ ] A) Relative size: the overall effort, complexity and uncertainty of a story compared with other stories
- [ ] B) The exact number of hours a story will take
- [ ] C) The number of defects found in a story
- [ ] D) The number of acceptance criteria a story has

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Relative size: the overall effort, complexity and uncertainty of a story compared with other stories

**Explanation:** Story points are unit-less relative estimates. A story worth 8 points is not 8 hours; it is roughly twice as big and risky as a 4-point story.

- **Why others are wrong:**
  - B) The lesson says points are not hours.
  - C) Points estimate size before work, not defects found.
  - D) Points are not a count of acceptance criteria.
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "7. Estimation Basics: Story Points, Planning Poker, Velocity"
</details>

---

**Question 26.** In Jira, what does the issue key QEA-12 identify?

- [ ] A) The twelfth sprint of project QEA
- [ ] B) The twelfth issue created in the project whose key is QEA
- [ ] C) A story worth 12 story points in project QEA
- [ ] D) A bug with priority level 12

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The twelfth issue created in the project whose key is QEA

**Explanation:** An issue key is the project key, a hyphen and a number; QEA-12 is the twelfth issue created in project QEA.

- **Why others are wrong:**
  - A) Sprints are named separately (for example, QEA Sprint 1).
  - C) Story points are a separate field.
  - D) Priority is a scale such as Highest to Lowest, not a number in the key.
- **Source:** `introduction-to-jira.md`, section "5. Core Vocabulary"
</details>

---

**Question 27.** In JQL, which operator performs a text search meaning "contains"?

- [ ] A) =
- [ ] B) !=
- [ ] C) IN
- [ ] D) ~

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) ~

**Explanation:** The ~ operator means contains (text search), for example summary ~ "login".

- **Why others are wrong:**
  - A) = means equal to.
  - B) != means not equal to.
  - C) IN matches any value in a list, such as priority IN (Highest, High).
- **Source:** `introduction-to-jira.md`, section "12. Searching with JQL"
</details>

---

## Part 2: True / False

Decide whether each statement is true or false. Many of these target common misconceptions.

**Question 28.** "Shift-left" means stopping testing at the end of the project and doing it only at the beginning.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Shift-left means starting quality work earlier and continuing it. It does not mean stop testing at the end.

- **Source:** `sdlc-fundamentals.md`, section "14. The cost of finding defects late"
</details>

---

**Question 29.** A defect can be introduced in one phase (for example, a misunderstood requirement) but only found in a much later phase.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A defect is a mistake made at some point in the life cycle. It may be introduced early and found only later in testing or by a customer, and the longer it stays hidden the more it costs to fix.

- **Source:** `sdlc-fundamentals.md`, section "14. The cost of finding defects late"
</details>

---

**Question 30.** Agile means there is no planning and no documentation.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Agile plans continuously in small steps and documents "just enough". The Manifesto says there is value in the items on the right (documentation, plans, and so on), but it values the items on the left more.

- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "13. Common misconceptions and 4.2 The four values of the Agile Manifesto"
</details>

---

**Question 31.** Waterfall can still be a sound choice for stable, regulated or small projects.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Waterfall fits when requirements are well understood and stable, regulation demands heavy documentation, or the project is short, small and simple.

- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "2.6 When to use Waterfall and 13. Common misconceptions"
</details>

---

**Question 32.** Scrum and Agile are the same thing.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Agile is a set of values and principles; Scrum is one specific framework that puts those values into practice. Kanban and XP are other examples.

- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "4.1 Why Agile emerged and 13. Common misconceptions"
</details>

---

**Question 33.** In Kanban, a pull system means a team member pulls a new card into their column only when they have capacity.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Kanban is a pull system: work is pulled when there is capacity, rather than pushed onto people by a manager or the previous stage, which prevents overload.

- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "6.5 Pull system and flow"
</details>

---

**Question 34.** The Scrum Master assigns tasks to the Developers and tracks each person's hours.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The Scrum Master is a servant leader who facilitates, coaches and removes impediments. They do not assign tasks or track individual hours; the team self-organizes.

- **Source:** `agile-roles-and-responsibilities.md`, section "3.2 The Scrum Master (SM) - What the Scrum Master is NOT"
</details>

---

**Question 35.** Scrum has no separate tester role, but testing skills are still essential and QEs are part of the Developers.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Scrum names three accountabilities only. Testers and QEs are part of the Developers and share accountability for quality, and their specialist skills are still needed.

- **Source:** `agile-roles-and-responsibilities.md`, section "3.4 Where Do Testers and QE Fit?"
</details>

---

**Question 36.** The Definition of Ready is an official Scrum artifact commitment, just like the Definition of Done.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The Definition of Ready is a widely used team practice, not an official Scrum artifact. The Definition of Done is the official commitment of the Increment.

- **Source:** `agile-roles-and-responsibilities.md`, section "7.1 Definition of Ready (DoR) and 7.3 Side-by-Side"
</details>

---

**Question 37.** Unfinished stories at the end of a sprint roll over automatically to the next sprint and still count toward velocity.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Unfinished stories are not counted toward velocity and are not part of the Increment. The Product Owner puts them back in the Product Backlog, and they do not automatically roll into the next sprint.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "What If the Goal Is Not Met by the End?"
</details>

---

**Question 38.** A 95% pass rate always means the product is ready to release.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** If the failed 5% include critical defects (for example, payment bugs) the product is not ready. Metrics must be read together with severity and risk.

- **Source:** `software-testing-life-cycle.md`, section "11. Phase 6: Test Cycle Closure (test metrics caution)"
</details>

---

**Question 39.** Entry criteria are the conditions that must be true before a phase can be called finished.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** That describes exit criteria. Entry criteria are the conditions that must be true before a phase can start.

- **Source:** `software-testing-life-cycle.md`, section "5. Key vocabulary used in every phase"
</details>

---

**Question 40.** Testing is normally done in the QA or staging environment, not in production, so that real users are never affected.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Tests can create, change or break data. A separate environment that resembles production keeps users safe while still giving trustworthy results.

- **Source:** `software-testing-life-cycle.md`, section "9. Phase 4: Test Environment Setup"
</details>

---

**Question 41.** In Jira, an "issue" is always a problem or bug.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** An issue is any single item of work: a feature, a task, a bug or a test activity. It is like one sticky note on the whiteboard.

- **Source:** `introduction-to-jira.md`, section "5. Core Vocabulary"
</details>

---

## Part 3: Fill-in-the-Blank

Write a short term in the blank.

**Question 42.** The seven SDLC phases are Planning, Requirements Analysis, Design, Implementation, ______, Deployment and Maintenance.

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Testing

**Accepted answers:** Testing; the Testing phase

**Explanation:** Testing is phase 5 of 7. The STLC then zooms into this single SDLC phase.

- **Source:** `sdlc-fundamentals.md`, section "3. What is the SDLC? and 10. Phase 5: Testing"
</details>

---

**Question 43.** The table that links each requirement to the test cases that check it is called the Requirement ______ Matrix (RTM).

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Traceability

**Accepted answers:** Traceability; Requirement Traceability Matrix

**Explanation:** The RTM shows coverage: which requirements have tests and which have none.

- **Source:** `software-testing-life-cycle.md`, section "8. Phase 3: Test Case Development"
</details>

---

**Question 44.** In Kanban, a ______ limit is the maximum number of cards allowed in a column at once. (Give the abbreviation or the full term.)

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** WIP (Work In Progress)

**Accepted answers:** WIP; Work In Progress; Work-in-Progress

**Explanation:** WIP limits reduce context switching and expose bottlenecks.

- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "6.4 WIP limits"
</details>

---

**Question 45.** In a 2-week sprint, Sprint Planning is typically timeboxed to up to ______ hours.

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 4

**Accepted answers:** 4; four

**Explanation:** Typical timeboxes for a 2-week sprint: Planning up to 4 hours, Daily Scrum 15 minutes, Review up to 2 hours, Retrospective up to 1.5 hours.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "Timeboxes at a Glance"
</details>

---

**Question 46.** The Scrum Increment is paired with the commitment called the ______ of Done.

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Definition

**Accepted answers:** Definition; Definition of Done (DoD)

**Explanation:** Every Increment must meet the team's Definition of Done; work that does not meet it is not part of the Increment.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "4. The Artifacts and Their Commitments"
</details>

---

**Question 47.** A user story follows the template: As a [type of user], I want [goal], ______ [benefit or reason].

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** So that

**Accepted answers:** So that

**Explanation:** The "So that" part states why, the value, and is the part teams most often forget.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "5. User Stories"
</details>

---

**Question 48.** In Given/When/Then acceptance criteria, the ______ clause describes the observable expected result.

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Then

**Accepted answers:** Then

**Explanation:** Given is the starting context, When is the action, Then is the observable outcome.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "6. Acceptance Criteria and Given/When/Then"
</details>

---

**Question 49.** In Jira, the unique identifier of an issue, made of the project key, a hyphen and a number (for example QEA-12), is called the issue ______.

Your answer: ______

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** key

**Accepted answers:** key; issue key

**Explanation:** Teams use issue keys in conversation, such as "Can you review QEA-12?".

- **Source:** `introduction-to-jira.md`, section "5. Core Vocabulary"
</details>

---

## Part 4: Code / Output Prediction

Work out the result by hand first. Use the data given in each question only.

**Question 50.** Project QEA in Jira contains exactly the six issues below ("Created" is month-day in the same year).

| Key | Type | Status | Priority | Assignee | Labels | Created |
|---|---|---|---|---|---|---|
| QEA-1 | Story | Done | High | Asha | (none) | 03-03 |
| QEA-2 | Bug | To Do | Highest | Ben | regression | 03-05 |
| QEA-3 | Bug | In Progress | Medium | Asha | login | 03-06 |
| QEA-4 | Bug | Done | High | Ben | regression | 03-04 |
| QEA-5 | Task | To Do | Low | Asha | (none) | 03-07 |
| QEA-6 | Bug | To Do | High | Asha | regression | 03-10 |

Which issue keys does this JQL query return?

```jql
project = QEA AND issuetype = Bug AND status != Done
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** QEA-2, QEA-3 and QEA-6

**Explanation:** The Bug rows are QEA-2, QEA-3, QEA-4 and QEA-6. QEA-4 has status Done and is excluded by `status != Done`. QEA-1 is a Story and QEA-5 is a Task, so they are excluded by `issuetype = Bug`.

- **Source:** `introduction-to-jira.md`, section "12. Searching with JQL"
</details>

---

**Question 51.** Using the same six issues as in the previous question:

| Key | Type | Status | Priority | Assignee | Labels | Created |
|---|---|---|---|---|---|---|
| QEA-1 | Story | Done | High | Asha | (none) | 03-03 |
| QEA-2 | Bug | To Do | Highest | Ben | regression | 03-05 |
| QEA-3 | Bug | In Progress | Medium | Asha | login | 03-06 |
| QEA-4 | Bug | Done | High | Ben | regression | 03-04 |
| QEA-5 | Task | To Do | Low | Asha | (none) | 03-07 |
| QEA-6 | Bug | To Do | High | Asha | regression | 03-10 |

In what order does this JQL query return the issue keys?

```jql
project = QEA AND priority IN (Highest, High) AND labels = regression ORDER BY created DESC
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** QEA-6, QEA-2, QEA-4

**Explanation:** Issues with priority Highest or High AND label regression are QEA-2 (Highest), QEA-4 (High) and QEA-6 (High). QEA-1 is High but has no regression label, and QEA-3 has the wrong priority and label. `ORDER BY created DESC` puts the newest first: QEA-6 (03-10), QEA-2 (03-05), QEA-4 (03-04).

- **Source:** `introduction-to-jira.md`, section "12. Searching with JQL"
</details>

---

**Question 52.** A team's sprint contains six stories. Per the lesson, only work that meets the Definition of Done counts toward velocity. What does this code print?

```python
stories = [("QEA-1", 5, True), ("QEA-2", 8, True), ("QEA-3", 3, False),
           ("QEA-4", 5, True), ("QEA-5", 2, True), ("QEA-6", 13, False)]
velocity = sum(p for _, p, done in stories if done)
committed = sum(p for _, p, _ in stories)
print(velocity, committed)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `20 36`

**Explanation:** Done stories are QEA-1 (5), QEA-2 (8), QEA-4 (5) and QEA-5 (2), which total 20. All six stories total 5 + 8 + 3 + 5 + 2 + 13 = 36 points committed. The unfinished 3-point and 13-point stories do not count toward velocity.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "7. Estimation Basics: Story Points, Planning Poker, Velocity and What If the Goal Is Not Met by the End?"
</details>

---

**Question 53.** A 2-week (10-day) sprint commits to 20 story points. Points completed on days 1 to 10 are listed in `done_per_day`. What does this code print?

```python
total = 20
sprint_days = 10
done_per_day = [0, 2, 0, 3, 1, 0, 2, 0, 4, 8]
remaining = total
for day, done in enumerate(done_per_day, start=1):
    remaining -= done
    if day == 5:
        ideal = total - total * day / sprint_days
        print(remaining, ideal, remaining > ideal)
print(remaining)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Two lines: `14 10.0 True` then `0`

**Explanation:** By day 5 the team has completed 0 + 2 + 0 + 3 + 1 = 6 points, so 14 remain. The ideal line at day 5 is 20 - 20 x 5 / 10 = 10.0. Since 14 > 10.0 the actual line is above the ideal line (the team is behind). Everything is finished by day 10, so the final print is 0. The shape (little progress, then a big drop at the end) is the warning pattern described in the lesson.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "8. The Burndown Chart; also introduction-to-jira.md, Example 3: Reading the burndown chart"
</details>

---

**Question 54.** A closure report is calculated with the code below. What does it print (three lines)?

```python
planned, executed, passed = 25, 20, 17
post_release, total_defects = 3, 60
print(executed / planned * 100)
print(passed / executed * 100)
print(post_release / total_defects * 100)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `80.0`, `85.0`, `5.0` (one per line)

**Explanation:** Execution percentage = executed / planned x 100 = 20 / 25 x 100 = 80.0. Pass percentage = passed / executed x 100 = 17 / 20 x 100 = 85.0. Defect leakage = defects found after release / total defects x 100 = 3 / 60 x 100 = 5.0.

- **Source:** `software-testing-life-cycle.md`, section "11. Phase 6: Test Cycle Closure (test metrics table)"
</details>

---

**Question 55.** A team checks a story against its Definition of Done with this code. What does it print?

```python
dod = {"code_reviewed": True, "unit_tests_pass": True,
       "acceptance_verified": False, "no_open_critical_bugs": True,
       "po_accepted": True}
missing = [k for k, v in dod.items() if not v]
print("DONE" if not missing else "NOT DONE: " + ", ".join(missing))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `NOT DONE: acceptance_verified`

**Explanation:** Only `acceptance_verified` is False, so `missing` is `['acceptance_verified']` and the else branch prints it. In Scrum work is either Done or not; a story that misses even one DoD item is not Done and gets no partial credit.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "4. The Artifacts and Their Commitments (A closer look at the Definition of Done)"
</details>

---

## Part 5: Matching and Scenario Questions

For the matching questions, write the pairs (for example 1-C) before opening the solution.

**Question 56.** **Match each Scrum event (1-5) to its description (A-E).**

| # | Event | Letter | Description |
|---|---|---|---|
| 1 | Sprint Planning | A | A 15-minute event for the Developers to inspect progress toward the Sprint Goal and plan the next 24 hours |
| 2 | Daily Scrum | B | Ongoing activity that makes upcoming stories small, clear, estimated and testable |
| 3 | Sprint Review | C | Event where the Scrum Team agrees the Sprint Goal and selects and plans the work |
| 4 | Sprint Retrospective | D | Scrum Team inspects its way of working and agrees concrete improvements |
| 5 | Backlog Refinement | E | Team presents the Increment to stakeholders and gathers feedback |

(Columns 1-2 list the events; columns 3-4 list the descriptions. Pair each number with a letter.)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-A, 3-E, 4-D, 5-B

**Explanation:** Planning decides the Sprint Goal and the plan; the Daily Scrum is the 15-minute daily check on the Sprint Goal; the Review inspects the product with stakeholders; the Retrospective inspects the way of working; Refinement prepares future stories.

- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "The Events in Depth (Events 1-5)"
</details>

---

**Question 57.** **Match each STLC phase (1-5) to its main deliverable (A-E).**

| # | STLC phase | Letter | Main deliverable |
|---|---|---|---|
| 1 | Requirement Analysis | A | Test Closure (Summary) Report and lessons-learned notes |
| 2 | Test Planning | B | A ready environment, setup record and smoke test result |
| 3 | Test Case Development | C | Question and clarification log and a draft RTM |
| 4 | Test Environment Setup | D | Test cases, test data and updated RTM |
| 5 | Test Cycle Closure | E | Test plan, effort estimate and risk list |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-D, 4-B, 5-A

**Explanation:** Requirement Analysis yields reviewed requirements, a question log and a draft RTM; Test Planning yields the plan, estimate and risk list; Test Case Development yields test cases, data and the updated RTM; Environment Setup yields the ready environment and smoke test result; Closure yields the closure report and lessons learned.

- **Source:** `software-testing-life-cycle.md`, section "12. All six phases at a glance and phase sections 6-11"
</details>

---

**Question 58.** **Match each situation (1-5) to the delivery model that fits best (A-E).**

| # | Situation | Letter | Model |
|---|---|---|---|
| 1 | A hospital billing system where regulations demand traceable requirements and signed documents | A | Scrum |
| 2 | A start-up building a social-media app where nobody knows which features users will love | B | Kanban |
| 3 | An IT help-desk team receiving unpredictable daily requests, including urgent outages | C | Hybrid (Water-Scrum-Fall) |
| 4 | A small one-off event website with fixed content and a 3-week deadline | D | V-Model |
| 5 | A company with a required upfront budget approval and a final compliance check, but with sprints in between | E | Waterfall |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-D, 2-A, 3-B, 4-E, 5-C

**Explanation:** Regulated, traceable work suits the V-Model; uncertain, fast-changing product work suits Scrum; continuous unpredictable work suits Kanban; small stable work suits a simple Waterfall-style sequence; a project that starts and ends in a Waterfall way with Scrum in the middle is Water-Scrum-Fall (a hybrid).

- **Source:** `waterfall-agile-scrum-kanban-and-hybrid-approaches.md`, section "11. Practical scenarios, 9. Decision guide and 7.2 Water-Scrum-Fall"
</details>

---

**Question 59.** **Match each responsibility (1-5) to the role (A-E).**

| # | Responsibility | Letter | Role |
|---|---|---|---|
| 1 | Orders the Product Backlog and accepts or rejects finished work | A | DevOps / Release Engineer |
| 2 | Removes impediments and coaches the team on self-management | B | Developers (including the QE) |
| 3 | Creates the Sprint Backlog and is accountable for adhering to the Definition of Done | C | Product Owner |
| 4 | Builds and maintains the pipelines and environments used to build, test and deploy | D | Business Analyst |
| 5 | Clarifies business needs and helps turn them into backlog items and acceptance criteria | E | Scrum Master |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-B, 4-A, 5-D

**Explanation:** The Product Owner orders the backlog and accepts work; the Scrum Master removes impediments and coaches; the Developers (which include QEs) own the Sprint Backlog and the DoD; DevOps / Release Engineers maintain pipelines and environments; the Business Analyst clarifies needs and supports acceptance criteria.

- **Source:** `agile-roles-and-responsibilities.md`, section "3. The Three Official Scrum Roles and 4. The Broader Agile Team and Stakeholders"
</details>

---

**Question 60.** **Match each Jira term (1-5) to its meaning (A-E).**

| # | Jira term | Letter | Meaning |
|---|---|---|---|
| 1 | Label | A | An ordered list of work that has been identified but not yet scheduled into a sprint |
| 2 | Component | B | A saved search that can be reused and shared |
| 3 | Backlog | C | A customisable page of gadgets showing information from filters |
| 4 | Filter | D | A named part of a product, normally set up by an administrator and chosen from a list |
| 5 | Dashboard | E | A free-text tag used to group issues informally |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-D, 3-A, 4-B, 5-C

**Explanation:** Labels are free-text tags anyone can type; components are controlled, named parts of the product; the backlog is unscheduled work; a filter is a saved search; a dashboard is a page of gadgets.

- **Source:** `introduction-to-jira.md`, section "5. Core Vocabulary and 13. Filters, Dashboards, and Reports"
</details>

---

**Question 61.** **Scenario.** It is the last day of a 2-week sprint. The team has finished 8 of the 10 days' worth of planned work and asks the Scrum Master to extend the sprint by 3 days. What is the correct response?

- [ ] A) Extend the sprint by 3 days, because quality should not be rushed
- [ ] B) Mark the unfinished stories as Done so that velocity looks complete
- [ ] C) Do not extend the sprint: unfinished work returns to the Product Backlog, and the team discusses why in the Retrospective
- [ ] D) Cancel the sprint, because a missed goal means the Scrum Master has failed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Do not extend the sprint: unfinished work returns to the Product Backlog, and the team discusses why in the Retrospective

**Explanation:** Sprints have a fixed length. Unfinished work goes back to the Product Backlog (it does not count toward velocity), and the Retrospective asks what the team learned.

- **Why others are wrong:**
  - A) The timebox is fixed; never extend the sprint.
  - B) Work only counts when it meets the Definition of Done; there is no partial credit.
  - D) Only the Product Owner can cancel a sprint, and only if the Sprint Goal becomes obsolete; a missed goal is a learning event, not a failure to punish.
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "Knowledge Check Q1; What If the Goal Is Not Met by the End?; 3. The Sprint"
</details>

---

## Part 6: Scenario-Based Questions (Project 1)

Project 1 is a web application with user registration and login. Apply what you learned today as the quality engineer on the team.

**Question 62.** **Scenario.** During Requirements Analysis for Project 1 you read this requirement: "Users can log in quickly." What is the best thing for the QE to do?

- [ ] A) Wait until the build is ready and measure whatever login time the app has
- [ ] B) Write a test case titled "Login is fast" right away
- [ ] C) Ask what "quickly" means and agree a measurable target, such as the login result appearing within 3 seconds
- [ ] D) Declare the requirement untestable and exclude login from testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Ask what "quickly" means and agree a measurable target, such as the login result appearing within 3 seconds

**Explanation:** Vague words such as "fast" must be turned into measurable statements before coding. The lesson turns "quickly" into "login result shown within 3 seconds".

- **Why others are wrong:**
  - A) Waiting means the defect (a vague requirement) is found late, when it is expensive to fix.
  - B) A test case without a measurable expected result cannot clearly pass or fail.
  - D) The requirement is fixable by asking questions; excluding login would leave a key feature untested.
- **Source:** `software-testing-life-cycle.md`, section "6. Phase 1: Requirement Analysis (worked mini-example); sdlc-fundamentals.md, 7. Phase 2: Requirements Analysis"
</details>

---

**Question 63.** **Scenario.** For the Project 1 story "As a new visitor, I want to register with my email and a password so that I can create an account", which acceptance criterion is written correctly in Given/When/Then form?

- [ ] A) Given I am on the registration page, When I submit a valid email and a valid password, Then I see a confirmation that my account was created
- [ ] B) Registration should be easy to use and fast
- [ ] C) Given a user, Then the account is created
- [ ] D) The developers will store new users in a table named users

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Given I am on the registration page, When I submit a valid email and a valid password, Then I see a confirmation that my account was created

**Explanation:** A good scenario has a starting context (Given), an action (When) and an observable result (Then).

- **Why others are wrong:**
  - B) "Easy" and "fast" are vague and not testable.
  - C) It has no When action and no concrete context, so nobody can tell what to do or observe.
  - D) It describes an implementation detail, not observable behavior; acceptance criteria say how we recognize success.
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "6. Acceptance Criteria and Given/When/Then"
</details>

---

**Question 64.** **Scenario.** In a Project 1 sprint the developers finish coding the login story on Day 8, and the QE has Days 9 and 10 to test everything. What is the best improvement?

- [ ] A) Extend the sprint by two days
- [ ] B) Ask the QE to work overtime on Days 9 and 10
- [ ] C) Mark the story Done on Day 8 and test it in the next sprint
- [ ] D) Slice stories small, test each slice as it is built, write test scenarios while developers code, and automate early

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Slice stories small, test each slice as it is built, write test scenarios while developers code, and automate early

**Explanation:** This is the "mini-waterfall inside the sprint" anti-pattern. The fix is continuous testing in small slices, early test design, pairing and early automation.

- **Why others are wrong:**
  - A) The sprint's fixed length is not extended.
  - B) Overtime does not fix the late arrival of work, and the Agile principles call for a sustainable pace.
  - C) A story that is not tested does not meet the Definition of Done, so it is not Done.
- **Source:** `agile-roles-and-responsibilities.md`, section "9. Common Anti-Patterns; scrum-ceremonies-and-sprint-lifecycle.md, Where Testing Fits Inside a Sprint"
</details>

---

**Question 65.** **Scenario.** In the Project 1 Jira project (key QEA) you want to list the bugs in the currently running sprint that are not yet finished. Which JQL query does this?

- [ ] A) project = QEA AND issuetype = Bug AND status = Done
- [ ] B) project = QEA AND issuetype = Bug AND sprint in openSprints() AND status != Done
- [ ] C) project = QEA AND issuetype = Story AND status != Done
- [ ] D) project = QEA AND assignee = currentUser() ORDER BY priority DESC

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) project = QEA AND issuetype = Bug AND sprint in openSprints() AND status != Done

**Explanation:** issuetype = Bug selects bugs, sprint in openSprints() limits to the active sprint, and status != Done keeps only unfinished ones.

- **Why others are wrong:**
  - A) This returns finished bugs (status = Done), the opposite of what is wanted, and has no sprint filter.
  - C) This returns unfinished stories, not bugs.
  - D) This returns issues assigned to you of any type and status, not open bugs in the current sprint.
- **Source:** `introduction-to-jira.md`, section "12. Searching with JQL and Example 1: A day in Jira for a QE"
</details>

---

**Question 66.** **Scenario.** At Sprint Planning for Project 1 the team's last three sprints finished 22, 26 and 24 points, and one developer will be on leave for part of the sprint. What is the most sensible plan?

- [ ] A) Plan about 24 points or slightly fewer, leaving room for the leave and for retesting
- [ ] B) Commit to 40 points so the sprint looks ambitious
- [ ] C) Switch to estimating in hours because points are unreliable
- [ ] D) Match the 35-point velocity of another team

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Plan about 24 points or slightly fewer, leaving room for the leave and for retesting

**Explanation:** Average velocity is (22 + 26 + 24) / 3 = 24 points. Velocity is a forecasting aid, and planning should account for leave and for fix-and-retest time (the lesson's QE suggests slightly fewer points than the maximum capacity).

- **Why others are wrong:**
  - B) Over-committing is a common planning mistake and squeezes testing at the end.
  - C) The lesson prefers relative story points, because hour estimates are often wrong and feel like promises.
  - D) Velocity belongs to one team and must never be used to compare teams.
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "7. Estimation Basics and Event 2: Sprint Planning (example script)"
</details>

---

**Question 67.** **Scenario.** On Day 9 of a Project 1 sprint the QE finds a serious defect in the registration story, which the developers believed was finished. What is the best response?

- [ ] A) Quietly wait and mention it at the Sprint Review
- [ ] B) Mark the story Done anyway and demo it
- [ ] C) Hold it until the Retrospective so the sprint is not disrupted
- [ ] D) Report it to the developer and team immediately, assess the impact on the Sprint Goal with the Product Owner, and keep the story not Done until it meets the Definition of Done

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Report it to the developer and team immediately, assess the impact on the Sprint Goal with the Product Owner, and keep the story not Done until it meets the Definition of Done

**Explanation:** The lesson's steps are: report immediately, assess impact, decide with the Product Owner (fix, reduce scope or return to backlog), keep the DoD, be transparent at the Review and learn in the Retrospective.

- **Why others are wrong:**
  - A) Hiding or delaying a late bug costs far more than reporting it.
  - B) A story with a serious open defect is not Done and is not demonstrated as complete.
  - C) The Retrospective is for learning afterwards; the defect must be raised at once.
- **Source:** `scrum-ceremonies-and-sprint-lifecycle.md`, section "What If a Bug Is Found Late?"
</details>
