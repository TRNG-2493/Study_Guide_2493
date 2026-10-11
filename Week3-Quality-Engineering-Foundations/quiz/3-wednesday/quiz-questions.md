# Weekly Knowledge Check: Day 3 - Testing Fundamentals (Week3-Quality-Engineering-Foundations)

This practice quiz reviews today's seven lessons: Testing Mindset, QA vs. QC, Verification vs. Validation, Defect vs. Error vs. Failure, Manual vs. Automated Testing, Testing Principles, and Positive and Negative Testing. Attempt every question on your own first. Only open the solution under a question after you have committed to an answer, then use the explanation and source to review any lesson you missed.

---

## Part 1: Multiple Choice

### Question 1

Which question best captures the main focus of the tester mindset, compared with the developer mindset?

- [ ] A) "How could this fail, and does it work for everyone who needs it?"
- [ ] B) "How do I make this work?"
- [ ] C) "How do I build this as quickly as possible?"
- [ ] D) "How do I avoid reporting problems that upset the team?"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) "How could this fail, and does it work for everyone who needs it?"

**Explanation:** The lesson's comparison table gives the developer the question "How do I make this work?" and the tester the question about how it could fail and whether it works for everyone who needs it.
- **Why others are wrong:**
  - B) that is the developer mindset's main question.
  - C) speed of building is not the tester mindset's defining question.
  - D) testers reveal weaknesses while they are cheap to fix; the aim is not to avoid reporting them.
- **Source:** testing-mindset.md - 2. Developer mindset and tester mindset
</details>

---
### Question 2

A tester is told "this area is very stable" and therefore tests it only lightly. Which cognitive bias is this?

- [ ] A) Confirmation bias
- [ ] B) Familiarity and blind spots
- [ ] C) Anchoring
- [ ] D) "Works on my machine"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Anchoring

**Explanation:** Anchoring means relying too heavily on the first information received. The lesson gives "this area is very stable" as an example and suggests asking "What evidence supports that?"
- **Why others are wrong:**
  - A) that is looking only for evidence that supports a belief, such as running only tests expected to pass.
  - B) that is no longer noticing flaws in something seen many times.
  - D) that is assuming something works everywhere because it works in your own environment.
- **Source:** testing-mindset.md - 6. Cognitive biases in testing
</details>

---
### Question 3

Which arrangement lists testers from LEAST to MOST independent?

- [ ] A) An external firm, a separate test group, an embedded tester, another developer, the author
- [ ] B) The author, another developer, an embedded tester, a separate test group, an external firm
- [ ] C) The author, an embedded tester, another developer, an external firm, a separate test group
- [ ] D) Another developer, the author, a separate test group, an embedded tester, an external firm

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The author, another developer, an embedded tester, a separate test group, an external firm

**Explanation:** The five levels run from the author testing their own work (strongest blind spots) to external or third-party testers (highest objectivity).
- **Why others are wrong:**
  - A) this is the reverse order, most to least independent.
  - C) the order of several levels is mixed up.
  - D) the author is the least independent, so must come first.
- **Source:** testing-mindset.md - 7. Independence of testing
</details>

---
### Question 4

A colleague says "Testing is about proving the developers wrong, so testers and developers are rivals." What does the lesson say?

- [ ] A) Correct: testers exist to catch developers' mistakes
- [ ] B) Correct, but only in Agile teams
- [ ] C) Developers should never think like testers
- [ ] D) The mindsets are complementary; the tester reveals weaknesses that are already in the product while they are cheap to fix

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The mindsets are complementary; the tester reveals weaknesses that are already in the product while they are cheap to fix

**Explanation:** The lesson uses the bridge engineer and inspector analogy: the inspector is not the engineer's enemy, and the tester does not break the product; the weaknesses were already there.
- **Why others are wrong:**
  - A) the lesson calls this picture misleading and harmful.
  - B) the lesson does not limit the rivalry idea to any team type; it rejects it.
  - C) the lesson says developers can and should think like testers, for example by writing unit tests.
- **Source:** testing-mindset.md - 2. Developer mindset and tester mindset
</details>

---
### Question 5

Which statement correctly describes Quality Assurance (QA) as defined in the lesson?

- [ ] A) Examining the finished product to find defects before release
- [ ] B) Running test cases and logging defects
- [ ] C) Fixing defects after users report them
- [ ] D) Planned, systematic, process-oriented and preventive activities that help ensure the way of working will produce a good product

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Planned, systematic, process-oriented and preventive activities that help ensure the way of working will produce a good product

**Explanation:** QA's key word is process: it is preventive, proactive and spans the whole lifecycle, while QC's key word is product.
- **Why others are wrong:**
  - A) that describes Quality Control (QC).
  - B) this is testing, which is a QC activity.
  - C) that is reactive correction, not planned prevention.
- **Source:** quality-assurance-vs-quality-control.md - 4. Quality Assurance (QA)
</details>

---
### Question 6

Which of the following is a QC activity rather than a QA activity?

- [ ] A) Re-testing a bug after the developer says it is fixed
- [ ] B) Defining the Definition of Done
- [ ] C) Holding a sprint retrospective
- [ ] D) Creating a template for test cases

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Re-testing a bug after the developer says it is fixed

**Explanation:** Re-testing examines the corrected product, so it is QC. The other three shape or improve the way of working.
- **Why others are wrong:**
  - B) the Definition of Done is a process agreement, so it is QA.
  - C) a retrospective improves how the team works, so it is QA.
  - D) a template standardizes how the team works, so it is QA.
- **Source:** quality-assurance-vs-quality-control.md - Try It Activity, Part B: Answer Key
</details>

---
### Question 7

According to the lesson, how is a CI quality gate classified?

- [ ] A) Entirely QC, because it runs in the pipeline
- [ ] B) Entirely QA, including every test it runs
- [ ] C) The rule that enforces the gate is a QA mechanism; the checks it runs are QC activities
- [ ] D) Neither, because it is automated

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The rule that enforces the gate is a QA mechanism; the checks it runs are QC activities

**Explanation:** The knowledge check answer states the gate rule is a process control (QA) while the tests it runs are QC.
- **Why others are wrong:**
  - A) the gate rule is a process control, so it is not purely QC.
  - B) the tests the gate runs examine the product, which is QC.
  - D) automation does not remove an activity from QA or QC.
- **Source:** quality-assurance-vs-quality-control.md - Knowledge Check (answer 9)
</details>

---
### Question 8

The lesson states that testing is which kind of activity, and which pair of words describes QC?

- [ ] A) Testing is a QA activity; QC is preventive and proactive
- [ ] B) Testing is a QC activity; QC is detective and corrective
- [ ] C) Testing is a QA activity; QC is detective and corrective
- [ ] D) Testing is a QC activity; QC is preventive and proactive

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Testing is a QC activity; QC is detective and corrective

**Explanation:** The Key Takeaways say testing is a QC activity, and QC is product-oriented, detective and corrective, and reactive.
- **Why others are wrong:**
  - A) those words describe QA, and testing is QC.
  - C) testing is QC, not QA.
  - D) QC is detective and corrective; preventive and proactive describe QA.
- **Source:** quality-assurance-vs-quality-control.md - Key Takeaways
</details>

---
### Question 9

In the lesson's classic wording, what question does verification answer?

- [ ] A) "Are we building the right product?"
- [ ] B) "Are we building the product right?"
- [ ] C) "Will the users be happy after release?"
- [ ] D) "Is the release date realistic?"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) "Are we building the product right?"

**Explanation:** Verification checks work against specifications and standards (built right); validation checks against user needs (right product).
- **Why others are wrong:**
  - A) that is the validation question.
  - C) this is a validation concern about user satisfaction.
  - D) scheduling is not part of the V&V questions.
- **Source:** verification-vs-validation.md - 1. The Two Classic Questions
</details>

---
### Question 10

A team reviews a requirements document for contradictions and unclear wording. How is this activity best classified?

- [ ] A) Validation, and dynamic
- [ ] B) Verification, and dynamic
- [ ] C) Validation, and static
- [ ] D) Verification, and static

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Verification, and static

**Explanation:** The knowledge check answer: the software is not run, and a document is examined against quality criteria, so it is static verification.
- **Why others are wrong:**
  - A) nothing is executed and the document is checked for consistency, not against user fitness by running software.
  - B) the software is not run, so it is static.
  - C) the review checks the document's own quality against criteria, which is verification.
- **Source:** verification-vs-validation.md - Knowledge Check (answer 2)
</details>

---
### Question 11

In the V-Model, which test level is paired with the business/user requirements phase?

- [ ] A) Acceptance testing
- [ ] B) Unit (component) testing
- [ ] C) Integration testing
- [ ] D) System testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Acceptance testing

**Explanation:** The Key Takeaways pair requirements with acceptance testing, system design with system testing, architecture with integration testing, and module design with unit testing.
- **Why others are wrong:**
  - B) unit testing is paired with module (low-level) design.
  - C) integration testing is paired with architecture.
  - D) system testing is paired with system design.
- **Source:** verification-vs-validation.md - Key Takeaways (V-Model)
</details>

---
### Question 12

A product passes every test written against its specification, but real users dislike it. Which activity was weak?

- [ ] A) Verification, because the tests did not pass
- [ ] B) Static analysis, because it found no defects
- [ ] C) Validation, because the right product was not built or the specification missed the real need
- [ ] D) Neither, because passing all tests means the product is good

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Validation, because the right product was not built or the specification missed the real need

**Explanation:** The product met the specification (verification looked fine) but did not satisfy users, which points to weak validation.
- **Why others are wrong:**
  - A) the tests did pass, so verification against the specification looks fine.
  - B) static analysis is a verification technique and does not decide user fit.
  - D) passing tests against a spec does not prove the product meets user needs.
- **Source:** verification-vs-validation.md - Knowledge Check (answer 9)
</details>

---
### Question 13

A developer misreads "60 or above passes" and writes `if score > 60`. Which term correctly names the `>` operator in the code?

- [ ] A) Error
- [ ] B) Failure
- [ ] C) Defect
- [ ] D) Incident

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Defect

**Explanation:** The lesson's chain is error (human mistake), defect (flaw in the work product), failure (observable wrong behavior). The operator is the defect.
- **Why others are wrong:**
  - A) the error is the developer's misunderstanding, a human action.
  - B) a failure is the observable wrong behavior when the code runs.
  - D) an incident is a noticed and reported event, not the flaw in the code.
- **Source:** defect-vs-error-vs-failure.md - 2. The Core Chain
</details>

---
### Question 14

Which pair are formal synonyms in the lesson's terminology?

- [ ] A) Mistake and error
- [ ] B) Defect and failure
- [ ] C) Incident and defect
- [ ] D) Issue and error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Mistake and error

**Explanation:** The related-terms table lists mistake as a formal synonym of error, and fault and bug as synonyms of defect.
- **Why others are wrong:**
  - B) the lesson says failure is formally distinct from defect.
  - C) an incident is a noticed and reported event, related to failure.
  - D) a Jira issue is any work item, not a formal synonym of error.
- **Source:** defect-vs-error-vs-failure.md - 3. The Related Terms
</details>

---
### Question 15

Which situation is a failure that is NOT caused by a defect in the application code?

- [ ] A) A function uses `>` where the requirement says `>=`
- [ ] B) Login fails because the test database has no record for the test user
- [ ] C) A requirement document contradicts itself
- [ ] D) A misspelled label in the source file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Login fails because the test database has no record for the test user

**Explanation:** Bad or missing test data is one of the listed causes of failures with no code defect, along with hardware effects, environment configuration, misuse, and third-party outages.
- **Why others are wrong:**
  - A) this is a code defect.
  - C) this is a defect in a work product, not a failure caused by something other than a defect.
  - D) this is a defect in the code or resource file.
- **Source:** defect-vs-error-vs-failure.md - 6. Failures Not Caused by Defects in the Code
</details>

---
### Question 16

A module has 30 KLOC. Reviews and testing found 54 defects; 6 more were found after release. What is the DRE (defect removal efficiency)?

- [ ] A) 90%
- [ ] B) 10%
- [ ] C) 54%
- [ ] D) 80%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 90%

**Explanation:** Total defects = 60. DRE = defects found before release / total = 54 / 60 = 90%, as in the knowledge check answer.
- **Why others are wrong:**
  - B) this is the share of defects that escaped, not the share removed.
  - C) this uses the raw count as a percentage.
  - D) this does not match 54 out of 60.
- **Source:** defect-vs-error-vs-failure.md - Knowledge Check (answer 11)
</details>

---
### Question 17

What is a flaky test, according to the lesson?

- [ ] A) A test that always fails because of a real defect
- [ ] B) A test with no assertions
- [ ] C) A manual test that was run only once
- [ ] D) A test that sometimes passes and sometimes fails without any change to the product

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A test that sometimes passes and sometimes fails without any change to the product

**Explanation:** Flaky tests waste investigation time and teach the team to ignore failures, including real ones.
- **Why others are wrong:**
  - A) a consistently failing test is not flaky.
  - B) a missing assertion is a different problem from inconsistent results.
  - C) the number of runs does not define flakiness.
- **Source:** manual-vs-automated-testing.md - Knowledge Check (answer 4)
</details>

---
### Question 18

A check will be run only once or twice. What does the decision checklist suggest?

- [ ] A) Keep it manual, because the scripting cost will never be repaid
- [ ] B) Automate it, because automation is always cheaper
- [ ] C) Automate it, because machines are more accurate
- [ ] D) Skip it, because one-time tests have no value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Keep it manual, because the scripting cost will never be repaid

**Explanation:** One-time tests are listed under "Signs a test should stay manual" because the upfront scripting cost is not repaid.
- **Why others are wrong:**
  - B) automation has a high startup cost that needs many runs to repay.
  - C) accuracy does not outweigh cost for a one-time test.
  - D) the lesson says to keep it manual, not skip it.
- **Source:** manual-vs-automated-testing.md - 5. When to automate and when to keep manual
</details>

---
### Question 19

In the test automation pyramid, which level should have the MOST tests?

- [ ] A) UI / end-to-end tests
- [ ] B) Service / API tests
- [ ] C) Unit tests
- [ ] D) Manual exploratory tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Unit tests

**Explanation:** The pyramid has many fast, cheap unit tests at the base, some API tests in the middle, and few UI tests at the top.
- **Why others are wrong:**
  - A) these should be fewest: slow, costly and fragile.
  - B) these are the middle layer, "some" tests.
  - D) these are not a level of the automation pyramid.
- **Source:** manual-vs-automated-testing.md - 7. The test automation pyramid
</details>

---
### Question 20

Which statement about automated testing is TRUE according to the myths table?

- [ ] A) Automation finds more new defects than exploratory manual testing
- [ ] B) Automation saves money immediately
- [ ] C) Flaky tests are normal and should just be re-run
- [ ] D) If all automated tests pass, it proves only that those checks passed, not that the product is bug-free

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) If all automated tests pass, it proves only that those checks passed, not that the product is bug-free

**Explanation:** Tests only check what they were written to check, so passing tests do not guarantee a bug-free product.
- **Why others are wrong:**
  - A) humans, especially through exploration, usually find more new defects.
  - B) it costs more at first and pays back over time.
  - C) ignoring flakiness teaches the team to ignore real failures.
- **Source:** manual-vs-automated-testing.md - 9. Myths and misconceptions
</details>

---
### Question 21

A form has drop-downs with 4, 3, 2 and 5 options respectively. How many combinations of choices exist?

- [ ] A) 14
- [ ] B) 120
- [ ] C) 60
- [ ] D) 240

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 120

**Explanation:** Combinations are found by multiplying the options: 4 x 3 x 2 x 5 = 120, illustrating that exhaustive testing grows too fast.
- **Why others are wrong:**
  - A) this adds the options instead of multiplying.
  - C) this omits one of the factors.
  - D) this over-multiplies; 4 x 3 x 2 x 5 is 120.
- **Source:** testing-principles.md - Principle 2: Exhaustive Testing Is Impossible
</details>

---
### Question 22

Which principle does "the invoicing module accounts for most of the logged bugs, so assign extra reviewers there" illustrate?

- [ ] A) Beware of the pesticide paradox
- [ ] B) Defects cluster together
- [ ] C) Testing is context dependent
- [ ] D) Early testing saves time and money

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Defects cluster together

**Explanation:** A small number of modules usually hold most defects, so tracking defects by module and focusing there is the lesson's advice.
- **Why others are wrong:**
  - A) that is about unchanged tests losing power.
  - C) that is about different software needing different testing.
  - D) that is about starting testing early to lower the cost of fixes.
- **Source:** testing-principles.md - Principle 4: Defects Cluster Together
</details>

---
### Question 23

The pesticide paradox warns that:

- [ ] A) Running the same tests repeatedly eventually stops finding new defects, so tests must be reviewed and updated
- [ ] B) Testing can prove there are no defects if enough tests run
- [ ] C) Defect-free software will always fail with users
- [ ] D) Automated tests are always worse than manual tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Running the same tests repeatedly eventually stops finding new defects, so tests must be reviewed and updated

**Explanation:** Like pesticide-resistant insects, the remaining defects are those the old tests cannot catch; repeated tests still help confirm existing behavior.
- **Why others are wrong:**
  - B) this contradicts Principle 1.
  - C) Principle 7 says it can fail, not that it always will, and it is a different principle.
  - D) the principle makes no such claim.
- **Source:** testing-principles.md - Principle 5: Beware of the Pesticide Paradox
</details>

---
### Question 24

What does "positive" or "negative" describe in a test?

- [ ] A) Whether the test passed or failed
- [ ] B) Whether the tester expects a defect
- [ ] C) Whether the test was automated
- [ ] D) The test input and scenario, not whether the test passed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The test input and scenario, not whether the test passed

**Explanation:** A negative test uses invalid, unexpected or malicious input and passes when the system handles it gracefully.
- **Why others are wrong:**
  - A) the lesson says a negative test can pass or fail just as a positive test can.
  - B) expectation of a defect does not define the type.
  - C) automation is independent of positive or negative.
- **Source:** positive-and-negative-testing.md - 1. Definitions
</details>

---
### Question 25

A user registers with the longest allowed username (exactly at the maximum length). How is this test classified?

- [ ] A) Negative, because it is an unusual input
- [ ] B) Negative, as an exception path
- [ ] C) Positive, as an alternate path
- [ ] D) Neither, because it is a boundary case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Positive, as an alternate path

**Explanation:** Alternate paths are valid, different routes to success, and are positive tests.
- **Why others are wrong:**
  - A) unusual does not mean invalid; the lesson warns about this mistake.
  - B) an exception path is where something goes wrong, which is not the case here.
  - D) it is valid input expecting success, so it is positive.
- **Source:** positive-and-negative-testing.md - 4. Happy path, alternate paths and exception paths
</details>

---
### Question 26

A required Email field is left blank and the form is submitted. Which negative-test category is this?

- [ ] A) Missing required field
- [ ] B) Invalid data type
- [ ] C) Out of range
- [ ] D) Duplicate data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Missing required field

**Explanation:** The category table lists "Missing required field: required value left out". Blank is only negative when the field is required.
- **Why others are wrong:**
  - B) no wrong kind of data is entered.
  - C) no value outside an allowed range is entered.
  - D) no unique value is repeated.
- **Source:** positive-and-negative-testing.md - 5. Categories of negative tests
</details>

---
### Question 27

Why is the message "Password incorrect for jane.doe@example.com" a security problem?

- [ ] A) It is too short to be useful
- [ ] B) It reveals the account exists and that only the password was wrong, helping an attacker find valid accounts
- [ ] C) It uses the email in the message, which breaks formatting rules
- [ ] D) It should have crashed the system instead

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It reveals the account exists and that only the password was wrong, helping an attacker find valid accounts

**Explanation:** The recommended generic message is "Email or password is incorrect."
- **Why others are wrong:**
  - A) length is not the stated issue.
  - C) the problem is information disclosure, not formatting.
  - D) a graceful, controlled message is the goal, not a crash.
- **Source:** positive-and-negative-testing.md - Knowledge Check (answer 6)
</details>

---
## Part 2: True/False

### Question 28

Developers should never test their own work, because testers are the only people responsible for quality.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Developers write unit tests and review each other's code, and quality is a whole-team responsibility, not the tester's alone.
- **Source:** testing-mindset.md - 10. Ownership of quality; Knowledge Check (answer 9)
</details>

---
### Question 29

Having a separate test group in the same company is more independent than having the developer who wrote the code test it.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Independence increases from the author, to another developer, to an embedded tester, to a separate group, to an external firm.
- **Source:** testing-mindset.md - 7. Independence of testing
</details>

---
### Question 30

In a QA vs. QC comparison, QA is the proactive, preventive one and QC is reactive and detective.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** QA acts before problems occur (prevention), while QC examines what has been produced to find defects.
- **Source:** quality-assurance-vs-quality-control.md - 7. Detailed Comparison: QA vs. QC
</details>

---
### Question 31

A code review checklist is a QC activity because it checks code.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Creating a checklist is a QA activity, a process tool that prevents forgotten steps; the checks themselves examine work products.
- **Source:** quality-assurance-vs-quality-control.md - Try It Activity, Part B (item 12) and 4. Quality Assurance
</details>

---
### Question 32

Validation is only performed during UAT.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Validation also includes prototype feedback, usability testing, demos, alpha/beta testing and post-release monitoring.
- **Source:** verification-vs-validation.md - Knowledge Check (answer 10)
</details>

---
### Question 33

A linter reporting an unused variable is a verification activity.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A linter checks code against technical rules (static analysis against standards), which is verification, not a judgment of user needs.
- **Source:** verification-vs-validation.md - Classification Exercise (item 3); Knowledge Check (answer 15)
</details>

---
### Question 34

A defect always causes a failure when the software is used.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A defect causes a failure only when executed under the right conditions. Dead code or an untriggered path can hold a defect that never fails.
- **Source:** defect-vs-error-vs-failure.md - 5. Defects That Never Cause Failures
</details>

---
### Question 35

One defect in shared code can cause many failures.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A single `>` in a reused function fails every time any customer triggers it, across many channels and days.
- **Source:** defect-vs-error-vs-failure.md - 7. One Error, Many Defects; One Defect, Many Failures
</details>

---
### Question 36

Automating every test case is the goal of a healthy automation strategy.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Trying to automate 100% is neither achievable nor economical; healthy teams target the right tests, and usability and exploratory work stay with people.
- **Source:** manual-vs-automated-testing.md - 8. What test automation is NOT
</details>

---
### Question 37

Too many UI tests is considered an anti-pattern in the test automation pyramid.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** UI tests are slow, costly and fragile, so most tests should sit at the lower levels.
- **Source:** manual-vs-automated-testing.md - 7. The test automation pyramid; Knowledge Check (answer 8)
</details>

---
### Question 38

If 500 tests all pass, you can state that the software contains no defects.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Principle 1: testing shows the presence of defects, not their absence. You can only say no defects were found by the tests that ran.
- **Source:** testing-principles.md - Principle 1
</details>

---
### Question 39

A software product that is almost free of defects can still fail if it does not meet users' needs.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is the absence-of-errors fallacy, which links to validation (building the right product).
- **Source:** testing-principles.md - Principle 7: Absence-of-Errors Fallacy
</details>

---
### Question 40

A negative test has failed whenever the system rejects the invalid input.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Rejecting invalid input gracefully is the expected result, so the negative test passes. It fails when the system handles the bad input badly, for example by accepting it.
- **Source:** positive-and-negative-testing.md - 1. Definitions
</details>

---
## Part 3: Fill-in-the-Blank

### Question 41

A human action that produces an incorrect result is called an ________; the flaw it leaves in a work product is called a ________.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** error (or mistake); defect (or fault, or bug)

**Explanation:** The chain is error, then defect, then failure.
- **Source:** defect-vs-error-vs-failure.md - 2. The Core Chain; 3. The Related Terms
</details>

---
### Question 42

The cognitive bias of looking only for evidence that supports what we already believe is called ________ bias.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** confirmation

**Explanation:** The counter is to design tests intended to disprove the claim, such as writing negative tests first.
- **Source:** testing-mindset.md - 6. Cognitive biases in testing
</details>

---
### Question 43

QA is ________-oriented and preventive, while QC is ________-oriented and detective.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** process; product

**Explanation:** QA's key word is process and QC's key word is product.
- **Source:** quality-assurance-vs-quality-control.md - 4. Quality Assurance (QA); 5. Quality Control (QC)
</details>

---
### Question 44

Verification asks "Are we building the product ________?" while validation asks "Are we building the ________ product?"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** right; right

**Explanation:** The two questions use almost identical words but check against the specification versus the user's real need.
- **Source:** verification-vs-validation.md - 1. The Two Classic Questions
</details>

---
### Question 45

The four review types from least formal to most formal are informal review, walkthrough, ________ review, and ________.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** technical; inspection

**Explanation:** The Key Takeaways list informal review, walkthrough, technical review and inspection.
- **Source:** verification-vs-validation.md - Key Takeaways
</details>

---
### Question 46

Testing that never runs the software, such as a review or linting, is called ________ testing, while testing that runs the software is called ________ testing.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** static; dynamic

**Explanation:** Static and dynamic describe the technique, whereas verification and validation describe the purpose.
- **Source:** verification-vs-validation.md - 6. Static Testing vs. Dynamic Testing
</details>

---
### Question 47

The ISTQB principle that says we must choose a smaller smart set of tests because combinations multiply too fast is "________ testing is impossible".

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Exhaustive

**Explanation:** A seven-factor registration form already had 10,800 combinations.
- **Source:** testing-principles.md - Principle 2
</details>

---
### Question 48

The "________ path" is the simplest successful journey and counts as a ________ (positive/negative) test.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** happy; positive

**Explanation:** The happy path (main success scenario) is a positive test; exception paths are negative tests.
- **Source:** positive-and-negative-testing.md - 4. Happy path, alternate paths and exception paths
</details>

---
## Part 4: Code/Output Prediction

### Question 49

The requirement states: "Orders of $100 or more receive a 10% discount." Study the code and the loop that follows, then say what is printed and which input exposes the problem.

```python
def apply_discount(total):
    if total > 100:
        return total * 0.9
    return total

for t in [50, 100, 150]:
    print(t, apply_discount(t))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Prints `50 50`, `100 100`, then `150 135.0`. The input exactly 100 exposes the failure (expected 90.0, actual 100).

**Explanation:** The `>` should be `>=`. For exactly 100 the discount is not applied. The wrong operator is the defect, the developer's misreading is the error, and the wrong price for 100 is the failure.
- **Source:** defect-vs-error-vs-failure.md - 4. The Extended Story: A Discount Code in Python; Knowledge Check (answer 3)
</details>

---
### Question 50

How many lines of combinations does this program produce, what is the last tuple, and what is the new total if a fifth factor with 5 options is added?

```python
from itertools import product

browsers = ["Chrome", "Firefox", "Edge"]
devices = ["Desktop", "Phone"]
langs = ["EN", "ES", "FR", "DE"]

combos = list(product(browsers, devices, langs))
print(len(combos))
print(combos[-1])
print(len(list(product(browsers, devices, langs, ["Free", "Paid", "Trial", "Pro", "Team"]))))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 24; `('Edge', 'Phone', 'DE')`; 120.

**Explanation:** `itertools.product` produces every combination: 3 x 2 x 4 = 24. Adding a factor of 5 options multiplies the total, 24 x 5 = 120. This shows why exhaustive testing becomes impossible.
- **Source:** testing-principles.md - Principle 2 (itertools.product example)
</details>

---
### Question 51

The requirement says "a score of 60 or above passes". What does the program print, and classify the observation for score 60 as an error, defect or failure.

```python
def pass_result(score):
    return "PASS" if score > 60 else "FAIL"

for s in [59, 60, 61]:
    print(s, pass_result(s))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Prints `59 FAIL`, `60 FAIL`, `61 PASS`. The observed result for 60 (FAIL) is a failure.

**Explanation:** The observable wrong behavior is a failure. The `>` in the code is the defect, and the developer's misreading of "or above" is the error. The input that triggers it is exactly 60.
- **Source:** defect-vs-error-vs-failure.md - Knowledge Check (answer 3); 2. The Core Chain
</details>

---
### Question 52

The requirement says the minimum password length is 8, so a password of exactly 8 characters must be valid. What happens when this pytest-style check runs, and what does it tell you?

```python
def is_valid_password(p):
    return len(p) > 8

try:
    assert is_valid_password("abcd1234") is True
    print("ok")
except AssertionError:
    print("AssertionError")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** The `assert` raises `AssertionError` (the program prints `AssertionError`). The test fails, showing a defect.

**Explanation:** `len("abcd1234")` is 8, and `8 > 8` is False, so the function wrongly rejects a valid password. The check must use `>=`. This is a failing assert that reveals a defect.
- **Source:** defect-vs-error-vs-failure.md - Hands-On Python Mini-Lab: Find, Prove, and Fix a Defect
</details>

---
### Question 53

Predict the output for each password in the loop. Which result is surprising for a tester using the negative-testing categories?

```python
def check_password(p):
    if len(p) < 8:
        raise ValueError("Password must have at least 8 characters")
    return "accepted"

for p in ["abc1234", "abcd1234", "", "        "]:
    try:
        print(check_password(p))
    except ValueError as e:
        print("rejected:", e)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `rejected: Password must have at least 8 characters`, `accepted`, `rejected: Password must have at least 8 characters`, `accepted`. The surprise is that eight spaces are accepted.

**Explanation:** Only length is checked, so a password of eight spaces is accepted. This falls under the "empty, null and whitespace" negative-test category, and a whitespace-only value should normally be rejected by the product's rules.
- **Source:** positive-and-negative-testing.md - 5. Categories of negative tests; Worked Example 3: Python demonstration
</details>

---
### Question 54

A tester runs this check. The input is an invalid 7-character password `abc1234`, the function correctly raises `ValueError`, and the test prints `PASS`. Is this a positive or negative test, and did it pass or fail?

```python
import pytest

def check_password(p):
    if len(p) < 8:
        raise ValueError("Password must have at least 8 characters")
    return "accepted"

def test_short_password_is_rejected():
    with pytest.raises(ValueError, match="at least 8"):
        check_password("abc1234")
    print("PASS")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Negative test; it passed.

**Explanation:** The input is invalid, so it is a negative test. The system rejected it with a clear error, which is the expected graceful handling, so the test passes. Positive or negative describes the input, not the result.
- **Source:** positive-and-negative-testing.md - 1. Definitions; Knowledge Check (answers 2, 13, 14)
</details>

---
## Part 5: Matching/Scenario

### Question 55

Match each activity to QA or QC.

| # | Activity |
|---|---|
| 1 | Writing a coding standard for the team |
| 2 | Executing a test case with a wrong password |
| 3 | Holding a sprint retrospective |
| 4 | Logging a defect with steps to reproduce |
| 5 | Auditing whether code reviews happen on every pull request |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 - QA; 2 - QC; 3 - QA; 4 - QC; 5 - QA

**Explanation:** Standards, retrospectives and process audits improve or enforce the way of working (QA). Running tests and logging defects examine the product (QC).
- **Source:** quality-assurance-vs-quality-control.md - Try It Activity, Part B: Answer Key
</details>

---
### Question 56

Match each activity to Verification (V) or Validation (VAL).

| # | Activity |
|---|---|
| 1 | A peer inspects the requirements document for contradictions |
| 2 | Real customers try the beta version and send feedback |
| 3 | A linter runs on every commit and flags unused variables |
| 4 | A business user performs UAT on the invoicing screen using real invoices |
| 5 | Paper wireframes are shown to potential users to ask whether the flow makes sense |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 - V; 2 - VAL; 3 - V; 4 - VAL; 5 - VAL

**Explanation:** Reviews and linters check work against specifications and standards. Beta, UAT and showing wireframes to users check against real needs, and item 5 shows validation can be static.
- **Source:** verification-vs-validation.md - Classification Exercise: Verification or Validation?
</details>

---
### Question 57

Match each scenario to one of these ISTQB principles: (P2) Exhaustive testing is impossible, (P3) Early testing saves time and money, (P5) Pesticide paradox, (P6) Context dependent, (P7) Absence-of-errors fallacy.

| # | Scenario |
|---|---|
| 1 | A tester asks about the maximum username length before any code is written |
| 2 | A suite unchanged for two years starts missing bugs in new features |
| 3 | A game studio relies on playtesting while a hospital vendor produces formal traceable evidence |
| 4 | A form with 6 drop-downs of 8 options is tested with a prioritized subset |
| 5 | An app has almost no defects, but customers abandon it because the main workflow does not fit their work |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 - P3; 2 - P5; 3 - P6; 4 - P2; 5 - P7

**Explanation:** Asking questions early is shift-left testing; an unchanged suite is the pesticide paradox; different contexts require different testing; 8^6 = 262,144 combinations cannot be tested exhaustively; and a defect-free product that users abandon is the absence-of-errors fallacy.
- **Source:** testing-principles.md - Scenario-Matching Exercise: Answer Key
</details>

---
### Question 58

Decide whether each test idea is Automate (A) or Keep manual (M).

| # | Scenario |
|---|---|
| 1 | Running the same 30 checkout checks on Chrome, Firefox and Edge every release |
| 2 | Checking whether a redesigned registration page feels intuitive to first-time users |
| 3 | A one-time check that data migrated correctly |
| 4 | Re-checking 150 existing features of a mature product after every code change |
| 5 | Exploring a brand-new, half-finished wishlist feature |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 - A; 2 - M; 3 - M; 4 - A; 5 - M

**Explanation:** Cross-browser and regression checks are repetitive and stable (automate). Usability, one-time and new exploratory work need human judgment or will not repay scripting cost.
- **Source:** manual-vs-automated-testing.md - Try It: Classification Exercise, Answer key
</details>

---
### Question 59

Classify each test idea as Positive (P) or Negative (N).

| # | Test idea |
|---|---|
| 1 | Log in with correct email and correct password |
| 2 | Upload an `.exe` file to a profile picture field that accepts `.png` |
| 3 | Leave the optional Middle name field blank (the requirement says it is optional) |
| 4 | Open a members-only page without logging in |
| 5 | Register with a 20-character username when 20 is the allowed maximum |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 - P; 2 - N; 3 - P; 4 - N; 5 - P

**Explanation:** Valid input and expected success is positive; unsupported file types and unauthorised access are negative. Leaving an optional field blank is valid (an alternate path), and the maximum allowed length is valid.
- **Source:** positive-and-negative-testing.md - Classification Exercise: Answer key
</details>

---
## Part 6: Scenario Questions (Project 1: Registration and Login)

### Question 60

The registration requirement says "Password must be at least 8 characters." The code uses `len(password) > 8`. A tester registers with a valid 8-character password and is rejected. What is the rejection?

- [ ] A) A defect, because the code is wrong
- [ ] B) An error, because a human made a mistake
- [ ] C) A failure; the `>` is the defect and the developer's misreading is the error
- [ ] D) An anomaly that proves the login is fine

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A failure; the `>` is the defect and the developer's misreading is the error

**Explanation:** The tester observes wrong behavior of the running system, which is a failure. The root of the chain is the developer's error.
- **Why others are wrong:**
  - A) the code flaw is the defect, but the rejection the tester observes is the failure.
  - B) the error is the developer's earlier misreading, not the observed rejection.
  - D) an anomaly is a neutral word for something that looks odd and does not show the system is fine.
- **Source:** defect-vs-error-vs-failure.md - 2. The Core Chain
</details>

---
### Question 61

Before any code exists for the registration page, the team reviews the password rules for ambiguity. How does the lesson classify this?

- [ ] A) Validation, a dynamic acceptance test
- [ ] B) Validation, because users are involved
- [ ] C) A QC activity because it finds defects
- [ ] D) Verification, a static review that is also a QA-style preventive activity

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Verification, a static review that is also a QA-style preventive activity

**Explanation:** Reviews examine a work product without running the software (static verification), and the Early Testing principle says defects found this early cost the least to fix.
- **Why others are wrong:**
  - A) no software is run and the review checks the document.
  - B) the review checks work products against standards, not user fitness through use.
  - C) the course treats early reviews as QA because their goal is prevention.
- **Source:** verification-vs-validation.md - 3. Verification in Depth; quality-assurance-vs-quality-control.md - Part B (item 16)
</details>

---
### Question 62

The team has 12 login and registration regression checks that run on every build, are stable, and are business critical. What should they do with them?

- [ ] A) Keep them manual, because registration is business critical
- [ ] B) Automate them, because they are repetitive, stable and high risk
- [ ] C) Skip them, because passing tests cannot prove the absence of defects
- [ ] D) Automate them only as UI tests, with no lower-level tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Automate them, because they are repetitive, stable and high risk

**Explanation:** The decision checklist lists repetitive, stable, high risk, regression and smoke as signs for automation. A valid-login check run on every build is the lesson's first automation candidate.
- **Why others are wrong:**
  - A) business critical points to automation when the check is repetitive and stable.
  - C) passing tests are still valuable; the principle only limits what they prove.
  - D) too many UI tests is an anti-pattern; the pyramid recommends mostly lower-level tests.
- **Source:** manual-vs-automated-testing.md - 5. When to automate; Knowledge Check (answer 14)
</details>

---
### Question 63

A tester tries these registration inputs: an email without `@`, a 300-character email, a password of spaces only, and an already registered email. What is this set of tests?

- [ ] A) Positive tests, because the application is working
- [ ] B) Alternate paths, because they are valid but unusual
- [ ] C) Positive tests, because they should all pass
- [ ] D) Negative tests covering wrong format, too long, empty/whitespace and duplicate data categories

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Negative tests covering wrong format, too long, empty/whitespace and duplicate data categories

**Explanation:** Each input maps to a negative category: wrong format, too long, empty/whitespace and duplicate data.
- **Why others are wrong:**
  - A) positive tests use valid input and expect success.
  - B) these inputs are invalid, not alternate valid routes.
  - C) a negative test passes when the system rejects the input gracefully; it does not make them positive.
- **Source:** positive-and-negative-testing.md - 5. Categories of negative tests
</details>

---
### Question 64

After 15 passing registration tests, a manager says "Registration is bug-free, release it." Which response matches the testing principles?

- [ ] A) Passing tests show no defects were found by those tests; they cannot prove absence of defects, so report coverage and residual risk
- [ ] B) Agree: 15 tests is enough proof of no defects
- [ ] C) Run the same 15 tests again until a defect appears
- [ ] D) Agree, because registration usually has fewer defects than login

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Passing tests show no defects were found by those tests; they cannot prove absence of defects, so report coverage and residual risk

**Explanation:** Principle 1: testing shows the presence of defects, not their absence. The Project 1 example is exactly that 15 passing registration tests do not mean it is bug-free.
- **Why others are wrong:**
  - B) this contradicts Principle 1.
  - C) repeating identical tests is the pesticide paradox and gives diminishing returns.
  - D) the lesson expects registration to have more defects, because it has more fields and validations.
- **Source:** testing-principles.md - Summary Table; Knowledge Check (answers 14, 15)
</details>

---
### Question 65

The registration page passes every test against its written spec, but in a usability session first-time users cannot figure out where to enter the password confirmation and abandon the form. What does this show?

- [ ] A) The pesticide paradox: the tests are too old
- [ ] B) Defect clustering in the registration module
- [ ] C) The absence-of-errors fallacy: verification passed but validation, meeting real user needs, was weak
- [ ] D) Exhaustive testing is impossible

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The absence-of-errors fallacy: verification passed but validation, meeting real user needs, was weak

**Explanation:** Passing tests alone is not enough; Principle 7 links to validation (right product) versus verification (built right).
- **Why others are wrong:**
  - A) nothing in the scenario says tests are being repeated without update.
  - B) the scenario is about fit to user needs, not where defects are concentrated.
  - D) the problem is not too many combinations but fit for users.
- **Source:** testing-principles.md - Principle 7; verification-vs-validation.md - Story 1
</details>

---
