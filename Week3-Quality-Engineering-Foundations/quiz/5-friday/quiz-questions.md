# Weekly Knowledge Check: Day 5 - Advanced Testing Concepts (Week3-Quality-Engineering-Foundations)

This practice quiz covers Friday's lessons: white-box testing, functional vs. non-functional testing, exploratory testing, data-driven testing, regression testing, performance and stress testing, and reliability and scalability. Attempt every question on your own first, write down your answer, and only then open the solution to check your work and read the explanation. Where a question depends on a convention (for example, how percentiles or downtime are calculated), the question states it.

---

## Part 1: Multiple Choice

### Question 1

Which statement best describes white-box testing?

- [ ] A) Designing tests only from the requirements, without looking at the code
- [ ] B) Designing and evaluating tests based on the internal structure of the software (its code, decisions, loops and paths)
- [ ] C) Testing performed only by end users in a production-like environment
- [ ] D) Measuring how quickly the system responds while many users are active

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Designing and evaluating tests based on the internal structure of the software (its code, decisions, loops and paths)

**Explanation:** White-box (also called glass-box, clear-box or structure-based) testing chooses and measures tests using the code's internal structure, while black-box testing uses requirements.
- **Why others are wrong:**
  - A) Describes black-box testing, where the code is not used to choose tests.
  - C) Describes acceptance testing, which is about business needs, not code structure.
  - D) Describes performance testing, which is a non-functional concern.
- **Source:** white-box-testing.md, section 1. What is white-box testing?
</details>

---

### Question 2

A function has 10 executable statements and the tests run 8 of them. What is the statement coverage?

- [ ] A) 8%
- [ ] B) 20%
- [ ] C) 100%
- [ ] D) 80%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 80%

**Explanation:** Statement coverage = executed statements / total executable statements x 100 = 8 / 10 x 100 = 80%.
- **Why others are wrong:**
  - A) 8 is the count of executed statements, not a percentage of 10.
  - B) 20% is the share of statements NOT executed (2 of 10).
  - C) 100% would require all 10 statements to be executed.
- **Source:** white-box-testing.md, section 7. Statement coverage; Knowledge Check answer 6
</details>

---

### Question 3

Which statement about statement coverage and branch coverage is correct?

- [ ] A) 100% branch coverage implies 100% statement coverage, but 100% statement coverage does not imply 100% branch coverage
- [ ] B) 100% statement coverage implies 100% branch coverage, but not the reverse
- [ ] C) Neither criterion implies the other
- [ ] D) The two are always equivalent for any function

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 100% branch coverage implies 100% statement coverage, but 100% statement coverage does not imply 100% branch coverage

**Explanation:** Taking every decision outcome runs every statement on any outcome, but running every statement can still leave a False outcome untested (for example, an `if` tested only with True).
- **Why others are wrong:**
  - B) This reverses the subsumption relationship.
  - C) They are related: branch coverage subsumes statement coverage.
  - D) A single test can run every statement while skipping a False outcome, so they differ.
- **Source:** white-box-testing.md, section 9. The subsumption relationship, with a counter-example
</details>

---

### Question 4

A control flow graph has 9 edges, 8 nodes and 1 connected component. Using V(G) = E - N + 2P, what is the cyclomatic complexity?

- [ ] A) 1
- [ ] B) 2
- [ ] C) 3
- [ ] D) 17

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 3

**Explanation:** V(G) = 9 - 8 + 2 x 1 = 3, meaning three linearly independent paths and at least three tests for the basis set.
- **Why others are wrong:**
  - A) 9 - 8 = 1 forgets to add 2P.
  - B) Uses 2P incorrectly; the formula gives 9 - 8 + 2 = 3.
  - D) 17 adds E and N instead of subtracting.
- **Source:** white-box-testing.md, section 13. Path coverage and cyclomatic complexity; Knowledge Check answer 8
</details>

---

### Question 5

Which of these is a NON-functional requirement?

- [ ] A) Password reset emails shall arrive within 60 seconds in 99% of cases
- [ ] B) The system shall allow a visitor to register with a unique email address
- [ ] C) An account locks after five failed login attempts
- [ ] D) The system shall let users change their email address

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Password reset emails shall arrive within 60 seconds in 99% of cases

**Explanation:** Non-functional requirements describe qualities and constraints, such as speed, that can be measured with numbers; the 60-seconds-in-99% requirement is a performance target.
- **Why others are wrong:**
  - B) This is a functional requirement: a feature.
  - C) This is a functional business rule, not a quality attribute.
  - D) This is a functional requirement: something the system does.
- **Source:** functional-vs-non-functional-testing.md, section 4. Non-Functional Testing Defined
</details>

---

### Question 6

What is the key difference between smoke testing and sanity testing?

- [ ] A) Sanity is broad and shallow while smoke is narrow and focused
- [ ] B) They are the same activity under two names
- [ ] C) Smoke is broad and shallow, checking the build is stable enough to test; sanity is narrow and focused on a specific fix or change
- [ ] D) Smoke testing is done only by business users before release

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Smoke is broad and shallow, checking the build is stable enough to test; sanity is narrow and focused on a specific fix or change

**Explanation:** Smoke asks 'is this build stable enough to test at all?' across critical functions, while sanity checks one changed area in more depth.
- **Why others are wrong:**
  - A) Reverses the two definitions.
  - B) The lesson treats them as distinct by purpose, scope and trigger.
  - D) Business users do acceptance testing; smoke runs on every new build, often automated.
- **Source:** functional-vs-non-functional-testing.md, section 3.10 Smoke vs. Sanity vs. Regression
</details>

---

### Question 7

Which of the following is a measurable (testable) non-functional requirement?

- [ ] A) The system should be fast
- [ ] B) 95% of login requests shall respond within 2 seconds under 500 concurrent users
- [ ] C) The system must be secure
- [ ] D) It should work on all devices

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 95% of login requests shall respond within 2 seconds under 500 concurrent users

**Explanation:** A testable requirement includes a number, a unit and the conditions, so two testers reach the same verdict.
- **Why others are wrong:**
  - A) 'Fast' has no number, scenario or condition.
  - C) 'Secure' does not name threats or checks.
  - D) 'All' is unbounded and cannot be tested.
- **Source:** functional-vs-non-functional-testing.md, section 7.1 Bad vs. Good
</details>

---

### Question 8

What is beta testing?

- [ ] A) Acceptance-style testing by internal staff outside the development team
- [ ] B) Quick check that the most critical functions of a new build work
- [ ] C) Re-running old tests after a code change
- [ ] D) Testing by a limited group of real external users in their own environments before general release

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Testing by a limited group of real external users in their own environments before general release

**Explanation:** Beta testing collects defect and usability feedback from real external users under real conditions.
- **Why others are wrong:**
  - A) That is alpha testing, performed inside the organization.
  - B) That is smoke testing.
  - C) That is regression testing.
- **Source:** functional-vs-non-functional-testing.md, section 3.6 Acceptance Testing
</details>

---

### Question 9

Which definition matches exploratory testing as taught in the lesson?

- [ ] A) Tests are all written in advance with steps and expected results, then executed later
- [ ] B) Informal, unplanned testing with no charter and usually no documentation
- [ ] C) Re-running a fixed list of checks on every build
- [ ] D) The tester simultaneously learns about the product, designs tests and executes them, using each result to decide the next step

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The tester simultaneously learns about the product, designs tests and executes them, using each result to decide the next step

**Explanation:** Learning, design and execution are interwoven, guided by a charter and the tester's skill.
- **Why others are wrong:**
  - A) That describes scripted testing.
  - B) That describes ad-hoc testing, which the course treats as different.
  - C) That describes automated smoke or regression checks.
- **Source:** exploratory-testing.md, section 1. What exploratory testing is
</details>

---

### Question 10

Which is Elisabeth Hendrickson's charter template?

- [ ] A) Explore <target> With <resources> To discover <information>
- [ ] B) Given <context> When <action> Then <outcome>
- [ ] C) Tag, Scale, Meter, Must, Plan, Wish
- [ ] D) Past, Results, Obstacles, Outlook, Feelings

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Explore <target> With <resources> To discover <information>

**Explanation:** A charter states the mission of a session: what to explore, with what, and what information to look for.
- **Why others are wrong:**
  - B) That is the Given/When/Then acceptance-criteria style.
  - C) That is the Planguage structure for quality requirements.
  - D) That is the PROOF debrief structure.
- **Source:** exploratory-testing.md, section 6. Test charters in depth (The standard template)
</details>

---

### Question 11

In session-based test management, about how long is a 'normal' session?

- [ ] A) About 5 minutes
- [ ] B) About 90 minutes
- [ ] C) About 4 hours
- [ ] D) About 24 hours

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) About 90 minutes

**Explanation:** The lesson gives short about 60, normal about 90 and long about 120 minutes, noting they are conventions.
- **Why others are wrong:**
  - A) Far too short to be a time-boxed session.
  - C) Far too long; focused thinking is tiring.
  - D) Sessions are uninterrupted blocks, not day-long runs.
- **Source:** exploratory-testing.md, section 7. Session-based test management (The session)
</details>

---

### Question 12

The registration page says 'Password must be at least 8 characters', but a 6-character password is accepted. Which HICCUPPS oracle does this violate?

- [ ] A) History
- [ ] B) Image
- [ ] C) Claims
- [ ] D) Statutes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Claims

**Explanation:** The Claims oracle says the product should be consistent with what it, its documentation or people say about it.
- **Why others are wrong:**
  - A) History compares with earlier behavior of the product.
  - B) Image concerns the brand and quality the organization wants to project.
  - D) Statutes concern laws, regulations and standards.
- **Source:** exploratory-testing.md, section 8. Heuristics and mnemonics (HICCUPPS)
</details>

---

### Question 13

What is the core idea of data-driven testing?

- [ ] A) Tests are assembled from reusable action words kept in a table
- [ ] B) Tests are generated automatically from a model such as a state machine
- [ ] C) Test logic is written once and kept separate from the test data, and the same logic runs against many data rows
- [ ] D) Tests are written as plain-language Given/When/Then scenarios linked to code

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Test logic is written once and kept separate from the test data, and the same logic runs against many data rows

**Explanation:** Data-driven testing varies the values while the steps stay the same: one recipe, many ingredient lists.
- **Why others are wrong:**
  - A) That is keyword-driven testing.
  - B) That is model-based testing.
  - D) That is behavior-driven development (BDD).
- **Source:** data-driven-testing.md, section 2. Definition: separate the logic from the data; section 7
</details>

---

### Question 14

In pytest, what does the `ids` argument of `@pytest.mark.parametrize` give you?

- [ ] A) A readable name for each data row in the report, which also lets you select a row with -k
- [ ] B) The expected result for each row
- [ ] C) A way to skip rows automatically when they fail
- [ ] D) A random order in which rows run

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A readable name for each data row in the report, which also lets you select a row with -k

**Explanation:** Because the id becomes part of the test name, `-k "REG-018"` runs only that row.
- **Why others are wrong:**
  - B) Expected results are values in the data rows, not ids.
  - C) Skipping is done with pytest.param marks, not ids.
  - D) ids only label rows.
- **Source:** data-driven-testing.md, Knowledge Check answer 6; section 10 Step 3
</details>

---

### Question 15

How do test design techniques (BVA, EP, decision tables) relate to data-driven testing?

- [ ] A) Data-driven testing replaces the techniques
- [ ] B) The techniques apply only to manual testing, never to DDT
- [ ] C) Data-driven testing automatically discovers the boundaries
- [ ] D) The techniques decide which data to use; data-driven testing is the machinery that runs that data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The techniques decide which data to use; data-driven testing is the machinery that runs that data

**Explanation:** A table produced by BVA or EP is already a data set that DDT can run.
- **Why others are wrong:**
  - A) They are partners, not alternatives.
  - B) A design table is exactly a DDT data set.
  - C) Boundaries come from BVA applied by the tester.
- **Source:** data-driven-testing.md, section 6. Relationship to test design techniques
</details>

---

### Question 16

Where should the values in a data row's expected-result column come from?

- [ ] A) The output printed the first time the code is run
- [ ] B) The requirements, never from running the code under test
- [ ] C) Whatever makes the test pass
- [ ] D) A teammate's best guess without checking the specification

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The requirements, never from running the code under test

**Explanation:** Expected results must come from the requirements so a faulty implementation fails the test.
- **Why others are wrong:**
  - A) Copying output only confirms the code does what it already does, bugs included.
  - C) Fitting the data to pass hides defects.
  - D) Guessing is not a source; the requirement is.
- **Source:** data-driven-testing.md, section 9. Best practices for test data design; Knowledge Check answer 12
</details>

---

### Question 17

What is retesting (confirmation testing)?

- [ ] A) Re-running the exact test that failed after a fix to confirm that specific defect is gone
- [ ] B) Running a wide set of other tests to detect side effects of the change
- [ ] C) A quick shallow check that a new build is stable enough to test
- [ ] D) A narrow check of the changed area before deeper testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Re-running the exact test that failed after a fix to confirm that specific defect is gone

**Explanation:** Retesting answers 'is this specific bug really fixed?' using the original failing steps and data.
- **Why others are wrong:**
  - B) That is regression testing.
  - C) That is smoke testing.
  - D) That is sanity testing.
- **Source:** regression-testing.md, section 4. Regression Testing vs. Retesting vs. Smoke vs. Sanity
</details>

---

### Question 18

When is progressive regression testing needed?

- [ ] A) When nothing changed and existing tests are re-run unchanged
- [ ] B) When the entire suite is run before a major release
- [ ] C) When requirements or functionality have changed, so tests must be added or updated along with re-running valid old ones
- [ ] D) When one component's unit tests are re-run in isolation

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) When requirements or functionality have changed, so tests must be added or updated along with re-running valid old ones

**Explanation:** Example: the password rule changes from 8 to 12 characters, so the old 8-character test is updated.
- **Why others are wrong:**
  - A) That is corrective regression testing.
  - B) That is complete (full) regression testing.
  - D) That is unit-level regression testing.
- **Source:** regression-testing.md, section 6. Types of Regression Testing
</details>

---

### Question 19

Using defect leakage = production defects / (pre-release defects + production defects) x 100, what is the leakage when 36 defects were found before release and 4 in production?

- [ ] A) 4%
- [ ] B) 11.1%
- [ ] C) 90%
- [ ] D) 10%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 10%

**Explanation:** 4 / (36 + 4) x 100 = 10%.
- **Why others are wrong:**
  - A) 4 is the production count, not a percentage.
  - B) Divides by 36 only; the denominator must be 36 + 4 = 40.
  - C) 90% is the share caught before release (36/40).
- **Source:** regression-testing.md, section 15. Measuring Regression Effectiveness; Knowledge Check 14
</details>

---

### Question 20

A change has likelihood 4 and impact 5 on the lesson's 1-to-5 scales. Using risk score = L x I and the lesson's bands (20-25 critical, 12-19 high, 6-11 medium, 1-5 low), what is the result?

- [ ] A) 9, medium
- [ ] B) 12, high
- [ ] C) 20, critical
- [ ] D) 25, critical

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 20, critical

**Explanation:** 4 x 5 = 20, which falls in the 20 to 25 critical band.
- **Why others are wrong:**
  - A) 9 adds L and I instead of multiplying.
  - B) 12 is 3 x 4, not 4 x 5.
  - D) 25 would need likelihood 5 and impact 5.
- **Source:** regression-testing.md, section 9.1 Risk-based selection; Knowledge Check 9
</details>

---

### Question 21

What is the main goal of a stress test?

- [ ] A) To push the system beyond its expected limits to find the breaking point, see how it fails and check recovery
- [ ] B) To confirm targets are met under the expected load
- [ ] C) To check the system absorbs a sudden, brief surge
- [ ] D) To find memory leaks by running moderate load for many hours

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) To push the system beyond its expected limits to find the breaking point, see how it fails and check recovery

**Explanation:** Stress testing asks where the system breaks, whether it fails gracefully, and whether it recovers when pressure is removed.
- **Why others are wrong:**
  - B) That is load testing.
  - C) That is spike testing.
  - D) That is soak (endurance) testing.
- **Source:** performance-and-stress-testing.md, section 2.2 Stress testing
</details>

---

### Question 22

In 100 login requests, 95 took 200 ms and 5 took 8,000 ms. Using the nearest-rank method, what is p95?

- [ ] A) 590 ms
- [ ] B) 8,000 ms
- [ ] C) 200 ms
- [ ] D) 4,100 ms

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 200 ms

**Explanation:** Rank = ceiling(0.95 x 100) = 95, and the 95th sorted value is 200 ms; the average of 590 ms hides the slow tail.
- **Why others are wrong:**
  - A) 590 ms is the average, which describes no real user.
  - B) 8,000 ms is p99; p95 is the 95th sorted value (rank 95).
  - D) 4,100 ms is a midpoint that matches no measurement.
- **Source:** performance-and-stress-testing.md, section 3.5 Percentiles: average, median, p90, p95, p99
</details>

---

### Question 23

Using Little's Law (L = lambda x W), 5 new sessions start each second and each lasts 192 seconds on average. How many concurrent users on average?

- [ ] A) 38.4
- [ ] B) 197
- [ ] C) 5
- [ ] D) 960

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 960

**Explanation:** L = 5 x 192 = 960 concurrent users.
- **Why others are wrong:**
  - A) 38.4 divides 192 by 5 instead of multiplying.
  - B) 197 adds the numbers.
  - C) 5 is only the arrival rate.
- **Source:** performance-and-stress-testing.md, section 3.11 Little's Law (introductory)
</details>

---

### Question 24

Which formula gives availability using averages?

- [ ] A) Availability = MTTR / (MTBF + MTTR)
- [ ] B) Availability = MTBF / (MTBF + MTTR)
- [ ] C) Availability = MTBF x MTTR
- [ ] D) Availability = MTBF - MTTR

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Availability = MTBF / (MTBF + MTTR)

**Explanation:** Availability is uptime / (uptime + downtime), equivalently MTBF / (MTBF + MTTR).
- **Why others are wrong:**
  - A) That is the unavailable fraction (down time share).
  - C) A product has hours-squared units, not a fraction.
  - D) A difference in hours is not a fraction of time.
- **Source:** reliability-and-scalability.md, section A4. Key reliability metrics
</details>

---

### Question 25

Using a 30-day month (43,200 minutes), how much downtime does 99.9% availability allow?

- [ ] A) 43.2 minutes
- [ ] B) 4.32 minutes
- [ ] C) 7.2 hours
- [ ] D) 8.76 hours

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 43.2 minutes

**Explanation:** 43,200 x (1 - 0.999) = 43.2 minutes.
- **Why others are wrong:**
  - B) 4.32 minutes is the allowance for 99.99%.
  - C) 7.2 hours is the monthly allowance for 99%.
  - D) 8.76 hours is the yearly allowance for 99.9%.
- **Source:** reliability-and-scalability.md, section A5. 'The nines'
</details>

---

### Question 26

Which resilience pattern stops calling a failing dependency after repeated failures, fails fast for a while, then tries a trial call?

- [ ] A) Retry with backoff
- [ ] B) Bulkhead
- [ ] C) Idempotency
- [ ] D) Circuit breaker

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Circuit breaker

**Explanation:** After a threshold of failures the breaker opens, later goes half-open for a trial call, and closes if that succeeds.
- **Why others are wrong:**
  - A) Retry keeps trying with growing delays; it does not open to fail fast.
  - B) Bulkhead isolates resources so one failure cannot sink everything.
  - C) Idempotency makes repeating an operation safe, not stopping calls.
- **Source:** reliability-and-scalability.md, section A9. Resilience patterns; Knowledge Check answer 7
</details>

---

## Part 2: True/False

### Question 27

100% branch coverage guarantees 100% statement coverage.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** If every decision outcome has been taken, every statement reachable through any outcome has run.
- **Source:** white-box-testing.md, section 9. The subsumption relationship
</details>

---

### Question 28

coverage.py measures condition coverage, so a coverage report shows whether each part of `A and B` was True and False.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** coverage.py measures statements and branches only; condition-level thinking is done by the tester by hand.
- **Source:** white-box-testing.md, section 11. Condition/decision coverage (Important note)
</details>

---

### Question 29

Functional testing is only about clicking buttons and does not check data.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Functional tests absolutely check data: saved records, calculations and trimming rules, as well as features, business rules and interactions.
- **Source:** functional-vs-non-functional-testing.md, section 2. Functional Testing Defined
</details>

---

### Question 30

A soak (endurance) test is a good way to find memory leaks.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Moderate load over many hours exposes memory leaks, resource exhaustion and gradual slowdowns.
- **Source:** performance-and-stress-testing.md, section 2.4 Soak (endurance) testing
</details>

---

### Question 31

To get the overall p95 of several test runs, you should average the p95 values of the runs.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Percentiles cannot be combined by averaging; compute the percentile from the combined raw measurements.
- **Source:** performance-and-stress-testing.md, section 3.5 Percentiles (caution about averaging percentiles)
</details>

---

### Question 32

A test charter states the mission of an exploratory session without prescribing the exact steps.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** It names what to explore and what information to look for, leaving the route to the tester.
- **Source:** exploratory-testing.md, section 6. Test charters in depth
</details>

---

### Question 33

In this course, ad-hoc testing and exploratory testing mean exactly the same thing.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Ad-hoc testing is informal with no charter and usually no documentation; exploratory testing has a charter, time box and notes.
- **Source:** exploratory-testing.md, section 3. Scripted vs exploratory vs ad-hoc testing
</details>

---

### Question 34

When parametrize decorators are stacked on one test, pytest runs every combination, so the counts multiply.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Two decorators with 2 and 6 values produce 2 x 6 = 12 tests.
- **Source:** data-driven-testing.md, section 10 Step 8: stacking decorators
</details>

---

### Question 35

Retesting and regression testing are the same thing.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Retesting re-runs the exact failed test to confirm one fix; regression testing runs other tests to check the change broke nothing else.
- **Source:** regression-testing.md, section 4. Regression Testing vs. Retesting vs. Smoke vs. Sanity
</details>

---

### Question 36

Teams usually set the SLO tighter than the SLA, so they get warning before they break the contract.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The SLO is an internal target and the SLA is the contractual promise with consequences.
- **Source:** reliability-and-scalability.md, section A6. SLI, SLO, SLA, and error budgets
</details>

---

### Question 37

A system cannot be available and unreliable at the same time.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A system can be up 99.9% of the time yet give wrong answers or fail many requests while up.
- **Source:** reliability-and-scalability.md, section A3. Related terms
</details>

---

### Question 38

Elasticity means resources are added and removed automatically to match demand.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Auto-scaling rules do this; a system can be scalable by hand without being elastic.
- **Source:** reliability-and-scalability.md, section B3. Elasticity and auto-scaling
</details>

---

## Part 3: Fill-in-the-Blank

Write your answer before opening the solution.

### Question 39

Branch coverage (%) = (number of decision outcomes exercised / total decision ______) x 100.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** outcomes (accepted: decision outcomes, outcomes)

**Explanation:** Each `if` contributes two outcomes, True and False.
- **Source:** white-box-testing.md, section 8. Branch (decision) coverage
</details>

---

### Question 40

The PROOF debrief stands for Past, Results, Obstacles, Outlook and ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Feelings

**Explanation:** PROOF structures the debrief after a session.
- **Source:** exploratory-testing.md, Knowledge Check answer 10
</details>

---

### Question 41

In pytest, the decorator `@pytest.mark.______` runs one test function once per data row.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** parametrize (accepted: parametrize)

**Explanation:** It turns each row into a separate test result with its own name.
- **Source:** data-driven-testing.md, section 10 Step 3
</details>

---

### Question 42

Re-running the exact failed test after a fix is called ______ testing (also called confirmation testing).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** retesting (accepted: retest, re-testing, confirmation)

**Explanation:** It verifies the specific defect is gone, unlike wide regression runs.
- **Source:** regression-testing.md, section 4
</details>

---

### Question 43

A p95 of 800 ms means 95 percent of requests completed in 800 ms or ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** less (accepted: less, below, faster, at or below)

**Explanation:** A percentile is the response time that N percent of requests were at or below.
- **Source:** performance-and-stress-testing.md, section 3.5 Percentiles
</details>

---

### Question 44

RPO is the maximum acceptable ______ measured in time, while RTO is the maximum acceptable time to restore service.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** data loss (accepted: data loss, loss of data)

**Explanation:** Example: 'we can lose at most the last 5 minutes of data'.
- **Source:** reliability-and-scalability.md, section A7. RTO and RPO
</details>

---

### Question 45

Speedup = throughput with n units / throughput with ______ unit(s), and efficiency = speedup / n.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 (accepted: 1, one, a single, 1 unit)

**Explanation:** 100% efficiency means perfect linear scaling.
- **Source:** reliability-and-scalability.md, section B6. Scalability factor and efficiency
</details>

---

### Question 46

Smoke testing is wide and ______, while sanity testing is narrow and ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** shallow; deep (accepted: shallow / deep; also 'focused' for the second blank)

**Explanation:** This memory trick separates smoke, sanity and the wide, thorough regression testing.
- **Source:** functional-vs-non-functional-testing.md, section 3.10 Smoke vs. Sanity vs. Regression
</details>

---

## Part 4: Code/Output Prediction

Work these out by hand. Python code is deterministic; assume Python 3 and pytest.

### Question 47

Consider this function:

```python
def shipping_fee(total, is_member):
    fee = 10
    if total >= 100:
        fee = 0
    if is_member:
        fee = fee + 2
    return fee
```

(a) What is the minimum number of tests needed for 100% statement coverage, and give one input pair `(total, is_member)`? (b) What is the minimum number needed for 100% branch coverage, and give the input pairs?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** (a) 1 test, for example (150, True). (b) 2 tests, for example (150, True) and (50, False).

**Explanation:** (150, True) runs every statement (fee = 10, fee = 0, fee = fee + 2, return). It takes both `if` decisions True only, so branch coverage is 50% (2 of 4 outcomes). Adding (50, False) takes both decisions False, giving all 4 outcomes.
- **Source:** white-box-testing.md, sections 7, 8 and 9 (statement, branch and subsumption)
</details>

---

### Question 48

Using the lesson's convention (each `if`, `elif`, `for` and `while` is one decision point; `and`/`or` are not counted), what is the cyclomatic complexity V(G) of this function?

```python
def check(items, limit):
    count = 0
    for item in items:
        if item < 0:
            continue
        elif item > limit:
            break
        count += 1
    if count == 0:
        return "none"
    return "ok"
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 5

**Explanation:** Decision points: `for`, `if`, `elif`, and the final `if` = 4. V(G) = decision points + 1 = 5, so at least 5 independent paths and tests for the basis set.
- **Source:** white-box-testing.md, section 13. Cyclomatic complexity
</details>

---

### Question 49

The file `test_m.py` (markers `smoke`, `regression` and `bugfix` are registered) contains:

```python
import pytest

@pytest.mark.smoke
@pytest.mark.regression
def test_a(): pass

@pytest.mark.regression
def test_b(): pass

@pytest.mark.regression
@pytest.mark.bugfix
def test_c(): pass

@pytest.mark.smoke
@pytest.mark.parametrize("x", [1, 2, 3])
def test_d(x): pass

@pytest.mark.bugfix
def test_e(): pass

def test_f(): pass
```

pytest collects 8 tests in total (test_d expands to 3). How many tests are SELECTED by (a) `-m smoke`, (b) `-m "regression and not bugfix"`, (c) `-m "smoke or bugfix"`?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** (a) 4 selected (4 deselected); (b) 2 selected (6 deselected); (c) 6 selected (2 deselected).

**Explanation:** (a) test_a plus the three test_d rows = 4. (b) regression tests are a, b, c; removing the bugfix test c leaves a and b = 2. (c) smoke gives a and d x3; bugfix adds c and e = 6. Marker expressions combine with and, or, not.
- **Source:** regression-testing.md, Hands-On Demonstration: A Tagged Suite with pytest (Running subsets); data-driven-testing.md, section 10 Step 3
</details>

---

### Question 50

What does this program print? (A 30-day month and a 365-day year of 525,600 minutes are used, as in the lesson.)

```python
period_min = 30 * 24 * 60
availability = 0.999
print(round(period_min * (1 - availability), 1))
print(round(525600 * (1 - availability) / 60, 2))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
43.2
8.76
```

**Explanation:** The first line is the allowed downtime in minutes for a 30-day month (43,200 x 0.001 = 43.2). The second converts the yearly allowance (525,600 x 0.001 = 525.6 minutes) to hours (8.76).
- **Source:** reliability-and-scalability.md, section A5. 'The nines'
</details>

---

### Question 51

What does this program print? It uses the nearest-rank method from the lesson (rank = ceiling(P/100 x N)).

```python
import math
times = [120, 95, 310, 105, 140, 98, 2200, 130, 115, 125]
s = sorted(times)
def pct(p):
    return s[math.ceil(p / 100 * len(s)) - 1]
print(pct(50), pct(90), pct(95))
print(sum(times) / len(times))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
120 310 2200
343.8
```

**Explanation:** Sorted: 95, 98, 105, 115, 120, 125, 130, 140, 310, 2200. N = 10, so p50 uses rank 5 (120), p90 rank 9 (310), p95 rank ceiling(9.5) = 10 (2200). The sum is 3438, so the average is 343.8, a value no user actually experienced.
- **Source:** performance-and-stress-testing.md, section 3.5 Percentiles (nearest-rank method)
</details>

---

### Question 52

A load test sent 6,000 requests in 120 seconds and 90 of them failed. What does this program print, and what do the four lines mean?

```python
requests = 6000
failed = 90
seconds = 120
print(requests / seconds)
print(failed / requests * 100)
print((requests - failed) / seconds)
arrival_rate = 6
session_seconds = 120
print(arrival_rate * session_seconds)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
50.0
1.5
49.25
720
```
Throughput 50.0 requests per second; error rate 1.5 percent; successful throughput 49.25 requests per second; about 720 concurrent users (Little's Law).

**Explanation:** Error rate = failed / total x 100 = 90 / 6000 x 100 = 1.5. Successful throughput excludes the 90 failures. The last line is L = lambda x W = 6 x 120 = 720.
- **Source:** performance-and-stress-testing.md, sections 3.1 (RPS/throughput), 3.6 (Error rate) and 3.11 (Little's Law)
</details>

---

### Question 53

How many tests does pytest collect from this file?

```python
import pytest

@pytest.mark.parametrize("a", [1, 2, 3])
@pytest.mark.parametrize("b", ["x", "y"])
@pytest.mark.parametrize("c", [True, False, None, 0])
def test_g(a, b, c): pass

@pytest.mark.parametrize("v", [10, 20, 30, 40, 50])
def test_h(v): pass
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 29

**Explanation:** Stacked decorators multiply: test_g gives 3 x 2 x 4 = 24 tests; test_h has a single decorator with 5 values = 5 tests; total 24 + 5 = 29.
- **Source:** data-driven-testing.md, section 10 Step 8: stacking decorators for combinations; Knowledge Check answer 9
</details>

---

### Question 54

A service ran for 720 hours, failed 3 times and was down for 6 hours in total. What does this program print?

```python
hours = 720
failures = 3
down = 6
uptime = hours - down
mtbf = uptime / failures
mttr = down / failures
print(mtbf, mttr)
print(round(mtbf / (mtbf + mttr) * 100, 2))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
238.0 2.0
99.17
```

**Explanation:** Uptime = 714 hours, MTBF = 714 / 3 = 238.0, MTTR = 6 / 3 = 2.0. Availability = MTBF / (MTBF + MTTR) = 238 / 240 = 99.17%, which matches uptime / total = 714 / 720.
- **Source:** reliability-and-scalability.md, section A4. Key reliability metrics (Worked example 1)
</details>

---

## Part 5: Matching/Scenario

Each question lists items to match. Write your mapping before opening the solution.

### Question 55

Match each functional test type (1-5) to its description (A-E).

1. Smoke test
2. Sanity test
3. User acceptance test (UAT)
4. Alpha test
5. End-to-end test

A. Acceptance-style testing inside the organization by staff who are not on the development team
B. A complete user journey checked across the UI, server, database and email service
C. A quick, shallow check that the critical functions of a new build work
D. Real users or business representatives run realistic scenarios to decide whether to accept the system
E. A narrow, focused check after a small fix that the change works and the nearby area is intact

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-D, 4-A, 5-B

**Explanation:** Smoke is broad and shallow on every new build; sanity is narrow after a small fix; UAT decides acceptance; alpha is the internal pre-beta stage; end-to-end follows a full journey.
- **Source:** functional-vs-non-functional-testing.md, sections 3.4 to 3.7 and 3.9 Summary Table
</details>

---

### Question 56

Match each performance test type (1-5) to its load shape or main question (A-E).

1. Load test
2. Stress test
3. Spike test
4. Soak (endurance) test
5. Volume test

A. Sharp jump in load, brief hold, then a drop
B. Normal load against a huge amount of data
C. Moderate flat load held for many hours
D. Ramp up, then a flat plateau at the expected level
E. Staircase beyond the limit, then drop, to find the breaking point

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-D, 2-E, 3-A, 4-C, 5-B

**Explanation:** Load = expected load with ramp-up and steady state; stress = beyond the limit; spike = sudden surge; soak = long duration; volume = large data.
- **Source:** performance-and-stress-testing.md, section 2. The Performance Testing Umbrella (quick reference table)
</details>

---

### Question 57

Match each non-functional requirement (1-5) to the quality attribute it tests (A-E).

1. "95% of login requests shall respond within 2 seconds under 500 concurrent users."
2. "Accounts shall lock for 15 minutes after 5 consecutive failed logins."
3. "At least 90% of first-time test users shall complete registration without assistance in under 2 minutes."
4. "The registration page shall render and function correctly on the latest two major versions of Chrome, Firefox, Safari and Edge."
5. "A keyboard-only user presses Tab repeatedly and focus moves through every field in a logical order."

A. Compatibility
B. Accessibility
C. Performance
D. Usability
E. Security

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-D, 4-A, 5-B

**Explanation:** Response time under load is performance; lockout is a security control; unassisted completion is usability; browser coverage is compatibility; keyboard focus order is accessibility.
- **Source:** functional-vs-non-functional-testing.md, section 7.1 Bad vs. Good and section 7.4 Given/When/Then for NFRs
</details>

---

### Question 58

Match each resilience pattern (1-5) to the Project 1 test idea (A-E).

1. Timeout
2. Retry with backoff
3. Circuit breaker
4. Bulkhead
5. Idempotency

A. Slow down "forgot password" and confirm login still responds because they use separate pools
B. Submit the identical registration request twice and expect one account
C. Fail the dependency twice then succeed; expect 3 attempts with increasing gaps
D. Break the dependency and check that after N failures requests are rejected instantly
E. Make the email service respond after 30 seconds and expect registration to give up at the configured limit

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-C, 3-D, 4-A, 5-B

**Explanation:** Each pattern has one promise: stop waiting, retry with growing gaps, fail fast after repeated failures, isolate resources, and make repeats safe.
- **Source:** reliability-and-scalability.md, section A9. Resilience patterns testers should know
</details>

---

### Question 59

Match each coverage criterion (1-5) to what it requires (A-E).

1. Statement coverage
2. Branch (decision) coverage
3. Condition coverage
4. Path coverage
5. Multiple condition coverage

A. Every atomic condition is True at least once and False at least once
B. Every complete route through the control flow graph is executed
C. Every executable statement runs at least once
D. Every decision is taken both True and False at least once
E. All 2^n combinations of n conditions are tried

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-D, 3-A, 4-B, 5-E

**Explanation:** The criteria differ in what they count: statements, decision outcomes, condition outcomes, complete paths, and all condition combinations.
- **Source:** white-box-testing.md, sections 7, 8, 10, 12, 13 and Key Takeaways
</details>

---

## Part 6: Scenario Questions (Project 1: Registration and Login)

### Question 60

Project 1 scenario: a developer fixes the bug 'a password containing a space is wrongly accepted'. A tester rechecks the password rules and the registration flow around it, rather than running the whole suite. What is this called?

- [ ] A) Smoke testing
- [ ] B) Sanity testing
- [ ] C) User acceptance testing
- [ ] D) Load testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Sanity testing

**Explanation:** Sanity testing is a narrow, focused check after a small fix that the change works and the closely related area is intact.
- **Why others are wrong:**
  - A) Smoke is a broad, shallow check of a new build, not a narrow check of one fix.
  - C) UAT is done by business users to decide acceptance.
  - D) Load testing applies expected user volume to measure performance.
- **Source:** functional-vs-non-functional-testing.md, section 3.5 Sanity Testing
</details>

---

### Question 61

Project 1 scenario: which charter is best formed for an exploratory session on the login page?

- [ ] A) Test the application
- [ ] B) Enter 'abc' in the email field and check that an error appears
- [ ] C) Explore the login page with zero, one and many failed attempts to discover whether lock-out behavior matches the requirements
- [ ] D) Click around the login page for a while

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Explore the login page with zero, one and many failed attempts to discover whether lock-out behavior matches the requirements

**Explanation:** A good charter follows Explore / With / To discover and is open enough to explore yet focused; Zero-One-Many is a lesson heuristic for repeated actions.
- **Why others are wrong:**
  - A) Too broad: no focus and no way to know when done.
  - B) Too narrow: a single scripted check with a yes/no answer.
  - D) No target, resources or information sought; this is closer to ad-hoc testing.
- **Source:** exploratory-testing.md, sections 6 (charters) and 8 (Zero-One-Many)
</details>

---

### Question 62

Project 1 scenario: the password rule changes from 8 to 12 characters. The test 'password of 8 characters is accepted' is now wrong, so the team updates it, adds tests for 12 characters and re-runs the remaining valid tests. Which type of regression testing is this?

- [ ] A) Progressive regression testing
- [ ] B) Corrective regression testing
- [ ] C) Complete (full) regression testing
- [ ] D) Unit-level regression testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Progressive regression testing

**Explanation:** Requirements changed, so tests had to be written or updated as well as re-run, which defines progressive regression testing.
- **Why others are wrong:**
  - B) Corrective reuses existing tests unchanged because requirements did not change.
  - C) Complete means running the entire suite, which this scenario does not say.
  - D) Unit-level re-runs one module's unit tests in isolation.
- **Source:** regression-testing.md, section 6. Types of Regression Testing
</details>

---

### Question 63

Project 1 scenario: the login SLO is 99.9% over a 30-day month, giving an error budget of 43.2 minutes. The month already had a 30-minute outage. How much error budget remains?

- [ ] A) 43.2 minutes
- [ ] B) 30 minutes
- [ ] C) 69.4 minutes
- [ ] D) 13.2 minutes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 13.2 minutes

**Explanation:** 43.2 - 30 = 13.2 minutes remain; the team has used about 69.4% of the budget.
- **Why others are wrong:**
  - A) That is the whole budget, before the outage.
  - B) That is the downtime already used, not what remains.
  - C) 69.4 is the percentage of budget used (30 / 43.2), not minutes remaining.
- **Source:** reliability-and-scalability.md, section A6. Error budget
</details>

---

### Question 64

Project 1 scenario: one registration server handles 500 req/s at acceptable latency; with 2 servers the measured throughput is 900 req/s. What is the scaling efficiency?

- [ ] A) 180%
- [ ] B) 45%
- [ ] C) 90%
- [ ] D) 95%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 90%

**Explanation:** Speedup = 900 / 500 = 1.8; efficiency = 1.8 / 2 = 0.90 = 90%, which is sub-linear scaling.
- **Why others are wrong:**
  - A) 180% is the speedup written as a percentage; efficiency divides speedup by n.
  - B) 45% divides the speedup by n twice.
  - D) 95% is the efficiency in the lesson's own example (950 req/s), not this one.
- **Source:** reliability-and-scalability.md, section B6. Scalability factor and efficiency
</details>
