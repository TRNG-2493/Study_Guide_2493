# Weekly Knowledge Check: Day 4 - Test Design Techniques (Week3-Quality-Engineering-Foundations)

Try every question on your own first. Write down your answer (or tick a box) before you open the solution under each question. The questions cover black-box testing, use-case testing, boundary value analysis, equivalence partitioning, error guessing, decision table testing and state transition testing. Where a question depends on a convention (for example 2-value or 3-value BVA), the question tells you which one to use.

---

## Part 1: Multiple Choice

Choose the single best answer.

**1.** Which statement best describes black-box testing?

- [ ] A) Checking that every branch and statement in the code has been executed
- [ ] B) Checking the behavior of the software through its inputs and outputs, compared against the specification, without relying on the internal code
- [ ] C) Choosing tests mainly from the tester's intuition and past defects
- [ ] D) Reading the source code together with the programmer to design each test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Checking the behavior of the software through its inputs and outputs, compared against the specification, without relying on the internal code

**Explanation:** Black-box testing examines behavior from the outside using inputs and outputs, with the specification as the oracle.
- **Why others are wrong:**
  - A) That describes white-box (structure-based) testing.
  - C) That describes experience-based testing such as error guessing.
  - D) Black-box tests do not depend on the code; they are derived from the specification.
- **Source:** black-box-testing.md, section 1. What is black-box testing?
</details>

---

**2.** Which pair lists other names for black-box testing?

- [ ] A) Structure-based testing and code-based testing
- [ ] B) Experience-based testing and exploratory testing
- [ ] C) Grey-box testing and unit testing
- [ ] D) Specification-based testing and behavioral testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Specification-based testing and behavioral testing

**Explanation:** Test cases come from the specification, and what is checked is the behavior the user can observe.
- **Why others are wrong:**
  - A) Those are names for white-box testing.
  - B) Those belong to the experience-based family, not black-box.
  - C) Grey-box is a mixed view, and unit testing is a test level, not a name for black-box.
- **Source:** black-box-testing.md, section 1. What is black-box testing?
</details>

---

**3.** A login page locks the account after three failed attempts, so the same wrong password gives a different result the first and third time. Which technique should you start with?

- [ ] A) State transition testing, because behavior depends on the history of failed attempts
- [ ] B) Equivalence partitioning alone, because the password is just one input field
- [ ] C) Error guessing alone, because lock-outs are unusual
- [ ] D) Use-case testing alone, because only the happy path matters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) State transition testing, because behavior depends on the history of failed attempts

**Explanation:** The lesson's selection table says behavior that depends on history or status starts with state transition testing, with decision tables added for rules at each state.
- **Why others are wrong:**
  - B) EP treats values, not history, so it cannot model the failed-attempt counter.
  - C) Error guessing supplements systematic techniques; it is not the starting point here.
  - D) Use-case testing covers journeys but is weak on history-dependent behavior; it is also not limited to the happy path.
- **Source:** black-box-testing.md, section 7. How to choose a technique
</details>

---

**4.** What is grey-box testing?

- [ ] A) Testing only with full access to every line of code
- [ ] B) Testing without any specification or knowledge of the system
- [ ] C) Designing tests from the outside as in black-box testing, but with partial knowledge of the internals, such as the database structure
- [ ] D) Testing done only by end users in production

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Designing tests from the outside as in black-box testing, but with partial knowledge of the internals, such as the database structure

**Explanation:** An example in the lesson is registering a user through the screen and then checking the database record directly.
- **Why others are wrong:**
  - A) Full code focus is white-box, not grey-box.
  - B) Grey-box still uses test design from outside and has partial internal knowledge.
  - D) Grey-box is defined by how much internal knowledge the tester has, not by who tests.
- **Source:** black-box-testing.md, section 13. Grey-box testing
</details>

---

**5.** In a use case, how does an alternative flow differ from an exception flow?

- [ ] A) An alternative flow is for errors and an exception flow is for successes
- [ ] B) An alternative flow is a valid variation that still leads to a successful or valid outcome; an exception flow is what happens when something goes wrong
- [ ] C) They are the same thing with different labels (A1 versus E1)
- [ ] D) An alternative flow is only for security tests and an exception flow is only for performance tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An alternative flow is a valid variation that still leads to a successful or valid outcome; an exception flow is what happens when something goes wrong

**Explanation:** Alternative flows (A1, A2...) such as Remember me still succeed; exception flows (E1, E2...) cover invalid input, failures and refusals and become your negative tests.
- **Why others are wrong:**
  - A) This reverses the two definitions.
  - C) The labels differ because the meaning differs: valid variation versus failure.
  - D) Neither flow type is limited to a test type.
- **Source:** use-case-testing.md, section 4. Anatomy of a use case
</details>

---

**6.** Which part of a use case is the main source of your expected results?

- [ ] A) The preconditions
- [ ] B) The trigger
- [ ] C) The list of actors
- [ ] D) The postconditions (success and failure guarantees)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The postconditions (success and failure guarantees)

**Explanation:** The lesson states that the postcondition is your oracle, for example the user is on the dashboard and a session exists.
- **Why others are wrong:**
  - A) Preconditions describe what must be true before the use case starts, which is setup.
  - B) The trigger only defines the starting point.
  - C) Actors tell you who to simulate, not what the result should be.
- **Source:** use-case-testing.md, section 7. Deriving test cases from a use case
</details>

---

**7.** A login use case has 1 main, 4 alternative and 7 exception flows. Tests exercise the main flow, 2 alternatives and 5 exceptions. What is the use-case coverage (rounded to one decimal)?

- [ ] A) 66.7%
- [ ] B) 58.3%
- [ ] C) 80.0%
- [ ] D) 100%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 66.7%

**Explanation:** Total flows are 1 + 4 + 7 = 12. Covered flows are 1 + 2 + 5 = 8, so coverage is 8 / 12 x 100 = 66.7%.
- **Why others are wrong:**
  - B) That would be 7 of 12; you covered 8 flows, not 7.
  - C) That is not 8 of 12; the total of 12 flows includes uncovered ones.
  - D) Four flows are still uncovered.
- **Source:** use-case-testing.md, section 10. Coverage
</details>

---

**8.** Why should the Login messages for 'wrong email' and 'wrong password' be identical?

- [ ] A) Because two different messages would double the number of test cases
- [ ] B) Because the use case diagram only allows one error symbol
- [ ] C) So an attacker cannot discover which email addresses are registered (account enumeration)
- [ ] D) Because users find identical messages easier to type into the form

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) So an attacker cannot discover which email addresses are registered (account enumeration)

**Explanation:** If the messages differ, a tester or attacker can learn which emails exist. It is a business rule testers must verify.
- **Why others are wrong:**
  - A) Test effort is not the reason; the reason is security.
  - B) Diagrams do not set message wording.
  - D) The reason is not typing convenience.
- **Source:** use-case-testing.md, Knowledge Check answers (question 12)
</details>

---

**9.** Use 2-value BVA. A field accepts whole numbers from 18 to 60 inclusive. Which values do you test?

- [ ] A) 17, 18, 60, 61
- [ ] B) 17, 18, 19, 59, 60, 61
- [ ] C) 18, 19, 59, 60
- [ ] D) 0, 18, 35, 60, 100

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 17, 18, 60, 61

**Explanation:** 2-value BVA takes each boundary and its closest neighbour in the adjacent partition, giving 17, 18, 60, 61.
- **Why others are wrong:**
  - B) That is the 3-value set with six values.
  - C) These are only valid values; the outside neighbours 17 and 61 are missing.
  - D) These are arbitrary values, not boundaries with their closest neighbours.
- **Source:** boundary-value-analysis.md, section 5. Two flavours: 2-value BVA and 3-value BVA
</details>

---

**10.** Use 3-value BVA. A password must be 8 to 16 characters inclusive. Which lengths do you test?

- [ ] A) 7, 8, 16, 17
- [ ] B) 8, 9, 15, 16
- [ ] C) 7, 8, 9, 15, 16, 17
- [ ] D) 6, 8, 12, 16, 18

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 7, 8, 9, 15, 16, 17

**Explanation:** 3-value BVA gives below, on and above each boundary: 7, 8, 9 and 15, 16, 17.
- **Why others are wrong:**
  - A) This is the 2-value set.
  - B) These lengths are all valid; the outside lengths 7 and 17 are missing.
  - D) These are not the values next to the boundaries (7 and 17).
- **Source:** boundary-value-analysis.md, section 10. Worked Example 2: Password length 8 to 16
</details>

---

**11.** The rule is 'age 18 or older' but the code uses `age > 18`. Which single test value exposes the defect?

- [ ] A) 17
- [ ] B) 18
- [ ] C) 19
- [ ] D) 35

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 18

**Explanation:** 18 should be accepted but `age > 18` rejects it, which is the classic off-by-one defect BVA targets.
- **Why others are wrong:**
  - A) 17 is rejected by both the correct rule and the faulty code, so no difference shows.
  - C) 19 is accepted by both versions.
  - D) 35 is accepted by both versions; it is not at the boundary.
- **Source:** boundary-value-analysis.md, Knowledge Check answers (question 4) and section 9. Worked Example 1
</details>

---

**12.** A price field allows two decimal places with a maximum of 500.00. What is the first invalid value above the maximum?

- [ ] A) 500.00
- [ ] B) 501.00
- [ ] C) 500.10
- [ ] D) 500.01

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 500.01

**Explanation:** The step for two decimal places is 0.01, so the value just above max is max + step = 500.01.
- **Why others are wrong:**
  - A) That is the maximum itself and is valid.
  - B) This is not the closest neighbour; the step is 0.01.
  - C) This skips 500.01, so it is not the value immediately above the maximum.
- **Source:** boundary-value-analysis.md, section 6. How to calculate boundary values
</details>

---

**13.** What is the core idea of equivalence partitioning?

- [ ] A) Test only the values at the edges of each range
- [ ] B) Test every possible input value so nothing is missed
- [ ] C) Divide inputs into groups the system should treat the same way and test one representative value from each group
- [ ] D) Choose inputs so that every line of code is executed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Divide inputs into groups the system should treat the same way and test one representative value from each group

**Explanation:** Values in the same partition should be handled identically, so one value per partition is enough.
- **Why others are wrong:**
  - A) That describes BVA.
  - B) Exhaustive testing is impossible; EP exists to avoid it.
  - D) That is a white-box (structure-based) idea.
- **Source:** equivalence-partitioning.md, Key Definitions and Knowledge Check answer 1
</details>

---

**14.** For a valid age partition of 18 to 60, which value would pure EP normally choose as the representative?

- [ ] A) 35, a typical interior value
- [ ] B) 18, because it is the lowest valid age
- [ ] C) 60, because it is the highest valid age
- [ ] D) 61, because it is the first age outside the range

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 35, a typical interior value

**Explanation:** The lesson says the representative should be a typical interior value; 18 and 60 are special and belong to BVA.
- **Why others are wrong:**
  - B) 18 is a boundary value, which belongs to BVA.
  - C) 60 is also a boundary value.
  - D) 61 is in the invalid partition above 60.
- **Source:** equivalence-partitioning.md, Example 1: Age Field (18 to 60)
</details>

---

**15.** A teammate defines age partitions as '18 to 30' and '30 to 60'. What is wrong?

- [ ] A) There is a gap at 30 so nothing handles that value
- [ ] B) Valid partitions must never be split into two
- [ ] C) The partitions should be exactly three for any range
- [ ] D) The partitions overlap at 30, so the expected result for 30 is unclear

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The partitions overlap at 30, so the expected result for 30 is unclear

**Explanation:** Partitions must not overlap. Fix by using 18 to 29 and 30 to 60 (or 18 to 30 and 31 to 60).
- **Why others are wrong:**
  - A) 30 is in both partitions, so there is an overlap, not a gap.
  - B) Valid partitions may be split when behavior differs (for example grades).
  - C) The number depends on the rules; for a range it is one valid plus invalid ones.
- **Source:** equivalence-partitioning.md, Knowledge Check answer 10
</details>

---

**16.** When combining several fields, why should each test contain only one invalid input?

- [ ] A) The form only accepts one field per submission
- [ ] B) Invalid inputs can mask each other, so you could not tell whether each check works
- [ ] C) It reduces the number of partitions you must define
- [ ] D) BVA forbids more than one invalid value per test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Invalid inputs can mask each other, so you could not tell whether each check works

**Explanation:** One error message or early exit can hide another check, so each invalid partition is tested with all other fields valid.
- **Why others are wrong:**
  - A) Forms accept many fields at once; the problem is diagnosis.
  - C) The partitions stay the same; only the test structure changes.
  - D) This is a testing-practice reason about masking, not a BVA rule.
- **Source:** equivalence-partitioning.md, Why Only One Invalid Input per Test? Masking
</details>

---

**17.** Which statement describes error guessing?

- [ ] A) A technique that derives tests from a formal state diagram
- [ ] B) An experience-based technique in which the tester anticipates likely defects and designs tests to expose them
- [ ] C) Entering random input with no thought about where defects might be
- [ ] D) A way to measure how many partitions have been covered

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An experience-based technique in which the tester anticipates likely defects and designs tests to expose them

**Explanation:** Error guessing uses knowledge, intuition and past defects, and it complements systematic techniques.
- **Why others are wrong:**
  - A) That describes state transition testing.
  - C) Error guessing is informed, not random.
  - D) That is EP coverage, not error guessing.
- **Source:** error-guessing.md, section 1. What is error guessing?
</details>

---

**18.** You are new and have no personal history of bugs. What does the lesson suggest for building error-guessing ideas?

- [ ] A) Borrow experience: read the bug list, talk to developers, read support tickets and use checklists
- [ ] B) Skip error guessing until you have years of experience
- [ ] C) Ask an AI for the expected results and use them without checking
- [ ] D) Test only random inputs and hope for failures

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Borrow experience: read the bug list, talk to developers, read support tickets and use checklists

**Explanation:** Sources such as defect logs, developer knowledge, user complaints and checklists let beginners start quickly.
- **Why others are wrong:**
  - B) The lesson says beginners can borrow experience from other sources.
  - C) Expected results come from requirements; AI output is only an idea to test.
  - D) Error guessing is informed by sources, not random.
- **Source:** error-guessing.md, section 4. Sources of experience
</details>

---

**19.** Which of these is a weakness of error guessing (not a strength)?

- [ ] A) It is fast and needs no preparation
- [ ] B) It finds unusual defects in areas the specification does not mention
- [ ] C) It has no coverage measure and depends on the tester's skill
- [ ] D) It can be used when requirements are poor or missing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It has no coverage measure and depends on the tester's skill

**Explanation:** Weaknesses include dependence on skill, poor repeatability, no coverage measure and bias.
- **Why others are wrong:**
  - A) That is a listed strength.
  - B) That is a listed strength.
  - D) That is a listed strength.
- **Source:** error-guessing.md, section 9. Strengths and weaknesses
</details>

---

**20.** A decision table has 5 Boolean conditions. How many rules are in the full table?

- [ ] A) 10
- [ ] B) 25
- [ ] C) 16
- [ ] D) 32

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 32

**Explanation:** A full limited-entry table has 2^n rules, so 2^5 = 32.
- **Why others are wrong:**
  - A) That adds instead of doubling for each condition.
  - B) That is 5 squared; the count is 2 raised to the number of conditions.
  - C) That is 2^4, one condition short.
- **Source:** decision-table-testing.md, Knowledge Check answer 2
</details>

---

**21.** What does a dash (-) in a condition cell of a decision table mean?

- [ ] A) The condition has not been defined yet
- [ ] B) Don't care: the condition's value does not change the outcome for that rule
- [ ] C) The combination is infeasible and cannot occur
- [ ] D) The condition is false

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Don't care: the condition's value does not change the outcome for that rule

**Explanation:** The dash is a promise from the requirement that T or F gives the same actions.
- **Why others are wrong:**
  - A) A dash is a deliberate claim about the outcome, not a placeholder.
  - C) Infeasible combinations are marked separately with a reason.
  - D) False is written F.
- **Source:** decision-table-testing.md, section 3. Definition and Anatomy of a Decision Table
</details>

---

**22.** Tests exercise 3 rules of a collapsed decision table that has 5 rules. What is the coverage against the collapsed table?

- [ ] A) 37.5%
- [ ] B) 60%
- [ ] C) 75%
- [ ] D) 3%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 60%

**Explanation:** Coverage = rules exercised / total feasible rules x 100 = 3 / 5 x 100 = 60%.
- **Why others are wrong:**
  - A) That is 3 of the 8 rules of the full table, a different denominator.
  - C) That would be 3 of 4.
  - D) That treats 3 as a percentage instead of 3 / 5 x 100.
- **Source:** decision-table-testing.md, section 8. Decision Table Coverage
</details>

---

**23.** An extended-entry decision table has conditions with 4, 3 and 2 possible values. How many rules are in the full table?

- [ ] A) 24
- [ ] B) 9
- [ ] C) 8
- [ ] D) 12

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 24

**Explanation:** The full table size is the product of the value counts: 4 x 3 x 2 = 24.
- **Why others are wrong:**
  - B) That adds the values (4 + 3 + 2).
  - C) That treats all conditions as Boolean (2^3).
  - D) That multiplies only two of the conditions.
- **Source:** decision-table-testing.md, Knowledge Check answer 3
</details>

---

**24.** In state transition testing, what is a guard condition?

- [ ] A) The state where the system starts
- [ ] B) The output the system shows after a transition
- [ ] C) A true/false condition, written in square brackets, that must be satisfied for the transition to fire
- [ ] D) A transition that returns to the same state

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A true/false condition, written in square brackets, that must be satisfied for the transition to fire

**Explanation:** Example from the lesson: return_request [within 30 days of delivery].
- **Why others are wrong:**
  - A) That is the initial state.
  - B) That is the action.
  - D) That is a self-transition (loop).
- **Source:** state-transition-testing.md, section 3. The vocabulary
</details>

---

**25.** A state model has 6 states and 5 events, and 11 cells of its state table are valid transitions. How many invalid cells are there?

- [ ] A) 30
- [ ] B) 11
- [ ] C) 25
- [ ] D) 19

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 19

**Explanation:** The table has 6 x 5 = 30 cells, so 30 - 11 = 19 are invalid.
- **Why others are wrong:**
  - A) That is the total number of cells (6 x 5), valid and invalid.
  - B) That is the number of valid transitions.
  - C) This does not match 6 x 5 - 11.
- **Source:** state-transition-testing.md, Knowledge Check answer 3
</details>

---

**26.** Which coverage level requires every valid transition to be exercised at least once?

- [ ] A) Valid transitions coverage (0-switch, all transitions)
- [ ] B) All states coverage
- [ ] C) Invalid transitions coverage
- [ ] D) 1-switch coverage

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Valid transitions coverage (0-switch, all transitions)

**Explanation:** 0-switch (all transitions) looks at each transition on its own and is the standard level most projects aim for.
- **Why others are wrong:**
  - B) That only requires each state to be visited, which is weaker.
  - C) That targets the invalid cells of the state table.
  - D) That counts sequences of two consecutive transitions.
- **Source:** state-transition-testing.md, section 9. Test coverage levels, Level 2
</details>

---

## Part 2: True or False

**27.** True or False: Black-box testing needs the tester to read the source code before designing tests.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. Black-box test cases are designed from the specification and observed behavior, not from the code.
- **Source:** black-box-testing.md, section 1. What is black-box testing?
</details>

---

**28.** True or False: Black-box tests are derived from the specification, while white-box tests are derived from the code structure.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** True. The comparison table lists specification and behavior for black-box, and code and internal structure for white-box.
- **Source:** black-box-testing.md, section 12. Black-box versus white-box
</details>

---

**29.** True or False: With 3-value BVA, a field that accepts 18 to 60 is tested with 17, 18, 19, 59, 60 and 61.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** True. 3-value BVA tests below, on and above each boundary, which gives six values.
- **Source:** boundary-value-analysis.md, section 5. Two flavours
</details>

---

**30.** True or False: With 2-value BVA, the values for the range 18 to 60 are 18, 19, 59 and 60.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. The 2-value set is 17, 18, 60, 61, which pairs each boundary with its closest neighbour in the adjacent (invalid) partition.
- **Source:** boundary-value-analysis.md, section 5. Two flavours
</details>

---

**31.** True or False: In pure equivalence partitioning, 18 and 60 are the best representatives of the valid age partition 18 to 60.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. 18 and 60 are boundary values (BVA). EP picks a typical interior value such as 35.
- **Source:** equivalence-partitioning.md, Knowledge Check answer 8
</details>

---

**32.** True or False: 100% EP coverage means every defect in the feature has been found.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. It only means every identified partition was sampled; wrong or incomplete partitions make the number misleading.
- **Source:** equivalence-partitioning.md, EP Coverage
</details>

---

**33.** True or False: A full decision table with 3 Boolean conditions has 8 rules.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** True. 2^3 = 8, and the lesson's login example has 8 rules in the full table.
- **Source:** decision-table-testing.md, section 6. Collapsing a Decision Table
</details>

---

**34.** True or False: It is safe to merge two decision table rules with a dash whenever it makes the table shorter.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. A dash is a promise from the requirement that the outcome is the same for T and F. If you are not sure, do not merge.
- **Source:** decision-table-testing.md, section 6. Collapsing a Decision Table
</details>

---

**35.** True or False: Executing every valid transition of a state model at least once gives 100% valid transitions (0-switch) coverage.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** True. Valid transition coverage = valid transitions executed / total valid transitions x 100.
- **Source:** state-transition-testing.md, section 9. Level 2
</details>

---

**36.** True or False: A self-transition (loop) in a state model does not need a test because the state does not change.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. It is still a transition and still needs a test, for example pushing a locked turnstile keeps it locked.
- **Source:** state-transition-testing.md, section 3. The vocabulary
</details>

---

**37.** True or False: 100% use-case coverage proves that the system has no defects.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. It only means each flow was exercised at least once; boundary, combination, state and missing-flow defects may remain.
- **Source:** use-case-testing.md, Knowledge Check answer 6
</details>

---

**38.** True or False: Error guessing can replace EP and BVA when time is short.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** False. Error guessing complements systematic techniques and never replaces them.
- **Source:** error-guessing.md, section 1. What is error guessing?
</details>

---

**39.** True or False: In use-case testing, each exception flow (E1, E2...) gets at least one test, which acts as a negative test.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** True. One test per exception flow checks the error message and the failure postcondition.
- **Source:** use-case-testing.md, section 7. Deriving test cases from a use case
</details>

---

## Part 3: Fill in the Blank

**40.** Black-box testing is also called ______ testing, because test cases come from the specification.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** specification-based (also accepted: specification based; behavioral is accepted as a second name)

**Explanation:** The lesson names specification-based testing and behavioral testing as other terms for black-box testing.
- **Source:** black-box-testing.md, section 1. What is black-box testing?
</details>

---

**41.** Use-case coverage (%) = (flows covered / total ______) x 100.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** flows (accepted: number of flows, total flows)

**Explanation:** Count flows as the main flow plus each alternative and each exception flow.
- **Source:** use-case-testing.md, section 10. Coverage
</details>

---

**42.** In 2-value BVA, each boundary produces ______ test values.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 2 (accepted: two)

**Explanation:** The boundary value itself and its closest neighbour in the adjacent partition.
- **Source:** boundary-value-analysis.md, section 5. Two flavours
</details>

---

**43.** For a price field with two decimal places, the step used in BVA formulas is ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 0.01

**Explanation:** Boundary formulas use min - step and max + step; two decimal places give a step of 0.01.
- **Source:** boundary-value-analysis.md, section 6. How to calculate boundary values
</details>

---

**44.** EP coverage (%) = (partitions covered / ______) x 100.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** total partitions (accepted: total number of partitions)

**Explanation:** Coverage is measured against the partitions you identified.
- **Source:** equivalence-partitioning.md, EP Coverage
</details>

---

**45.** A full limited-entry decision table with n Boolean conditions has ______ rules.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 2^n (accepted: 2 to the power n, 2**n)

**Explanation:** Each condition doubles the number of combinations.
- **Source:** decision-table-testing.md, Key Takeaways
</details>

---

**46.** In a state table, a state-by-event cell that the requirements do not allow is called an ______ transition.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** invalid

**Explanation:** Testing it means proving the system refuses or ignores the event and stays in a sensible state.
- **Source:** state-transition-testing.md, section 3. The vocabulary
</details>

---

**47.** The experience-based technique in which the tester anticipates likely defects and designs tests to expose them is called ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** error guessing

**Explanation:** It uses past defects, knowledge and checklists, and complements systematic techniques.
- **Source:** error-guessing.md, section 1. What is error guessing?
</details>

---

## Part 4: Code and Output Prediction

Work out the result by reading the code. Do not run it until you have written down your prediction.

**48.** The requirement is 'age 18 to 60 inclusive'. The validator below has a defect. What does the script print?

```python
def is_valid_age(age):
    return age > 18 and age <= 60

cases = [(17, False), (18, True), (19, True), (59, True), (60, True), (61, False)]
for value, expected in cases:
    actual = is_valid_age(value)
    print(value, "PASS" if actual == expected else "FAIL")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
17 PASS
18 FAIL
19 PASS
59 PASS
60 PASS
61 PASS
```

Only the boundary 18 fails because the code uses `age > 18`, which wrongly rejects exactly 18.

**Explanation:** `age > 18` rejects 18, which should be accepted, so 18 prints FAIL; every other value matches its expected result.
- **Source:** boundary-value-analysis.md, section 9. Worked Example 1: Age field accepting 18 to 60
</details>

---

**49.** The requirement is 'password length 8 to 16 characters inclusive'. The 3-value BVA lengths are tested. What does the script print?

```python
def password_length_ok(pw):
    return 8 <= len(pw) < 16

lengths = [7, 8, 9, 15, 16, 17]
failures = [n for n in lengths if password_length_ok("x" * n) != (8 <= n <= 16)]
print(failures)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
[16]
```

The list shows that only length 16 is wrongly rejected.

**Explanation:** `8 <= len(pw) < 16` rejects 16, the maximum, so 16 is the only length where the result differs from the requirement.
- **Source:** boundary-value-analysis.md, section 10. Worked Example 2: Password length 8 to 16
</details>

---

**50.** How many rules does the full decision table have? What does the script print?

```python
conditions = {"member": 2, "coupon": 2, "order_over_100": 2, "first_order": 2, "region": 3}
total = 1
for count in conditions.values():
    total *= count
print(total)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
48
```

The full table has 48 rules.

**Explanation:** Four Boolean conditions give 2 x 2 x 2 x 2 = 16, and the 3-valued region multiplies that by 3, so 48.
- **Source:** decision-table-testing.md, Knowledge Check answer 3 (product of value counts)
</details>

---

**51.** Each rule in a collapsed decision table with three Boolean conditions covers 2 to the power of its dash count combinations. What does the script print?

```python
rules = [("T", "-", "-"), ("F", "T", "-"), ("F", "F", "T"), ("F", "F", "F")]
covered = sum(2 ** rule.count("-") for rule in rules)
print(covered, covered == 2 ** 3)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
8 True
```

The rules cover 8 combinations, which equals 2^3, so the table is complete.

**Explanation:** The rules cover 4 + 2 + 1 + 1 = 8 combinations. The lesson's completeness check says the covered counts must add up to 2^n.
- **Source:** decision-table-testing.md, section 6. Collapsing a Decision Table (completeness check)
</details>

---

**52.** Trace the event sequence through the state machine. An event with no entry in the table leaves the state unchanged. What does the script print?

```python
table = {
    ("Logged Out", "login_fail"): "Failed 1",
    ("Logged Out", "login_ok"): "Logged In",
    ("Failed 1", "login_fail"): "Failed 2",
    ("Failed 1", "login_ok"): "Logged In",
    ("Failed 2", "login_fail"): "Locked",
    ("Failed 2", "login_ok"): "Logged In",
    ("Locked", "unlock"): "Logged Out",
    ("Logged In", "logout"): "Logged Out",
}
state = "Logged Out"
for event in ["login_fail", "login_fail", "login_ok", "logout", "unlock", "login_fail"]:
    state = table.get((state, event), state)
print(state)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
Failed 1
```

The final state is Failed 1.

**Explanation:** Logged Out -> Failed 1 -> Failed 2 -> Logged In (login_ok) -> Logged Out (logout); unlock is invalid in Logged Out so the state stays; login_fail then gives Failed 1.
- **Source:** state-transition-testing.md, section 9 (login model transitions T1 to T8)
</details>

---

**53.** The EP design for an age field (18 to 60) has six partitions. Four tests are run. What does the script print?

```python
partitions = ["below_18", "18_to_60", "above_60", "non_numeric", "empty", "decimal"]
tests = {"15": "below_18", "35": "18_to_60", "abc": "non_numeric", "": "empty"}
covered = set(tests.values())
print(len(covered), len(partitions), round(len(covered) / len(partitions) * 100, 1))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
4 6 66.7
```

The script prints the number covered, the total, and the coverage percentage.

**Explanation:** Four partitions are covered (below_18, 18_to_60, non_numeric, empty) out of six: 4 / 6 x 100 = 66.7%.
- **Source:** equivalence-partitioning.md, EP Coverage (age field worked numbers)
</details>

---

**54.** These helper functions generate boundary values for the range 20 to 45 (integers, step 1). What does the script print?

```python
def two_value(lo, hi):
    return [lo - 1, lo, hi, hi + 1]

def three_value(lo, hi):
    return [lo - 1, lo, lo + 1, hi - 1, hi, hi + 1]

print(two_value(20, 45))
print(three_value(20, 45))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
[19, 20, 45, 46]
[19, 20, 21, 44, 45, 46]
```

The first list is the 2-value set and the second list is the 3-value set.

**Explanation:** 2-value BVA uses lo-1, lo, hi, hi+1; 3-value BVA uses below, on and above each boundary.
- **Source:** boundary-value-analysis.md, section 5. Two flavours
</details>

---

**55.** The login model has 5 states and 4 events. Two test paths are run from Logged Out. What does the script print (transitions executed, valid transition coverage percent, number of invalid cells)?

```python
table = {
    ("Logged Out", "login_fail"): "Failed 1",
    ("Logged Out", "login_ok"): "Logged In",
    ("Failed 1", "login_fail"): "Failed 2",
    ("Failed 1", "login_ok"): "Logged In",
    ("Failed 2", "login_fail"): "Locked",
    ("Failed 2", "login_ok"): "Logged In",
    ("Locked", "unlock"): "Logged Out",
    ("Logged In", "logout"): "Logged Out",
}
states = ["Logged Out", "Failed 1", "Failed 2", "Locked", "Logged In"]
events = ["login_fail", "login_ok", "unlock", "logout"]
paths = [["login_fail", "login_fail", "login_fail", "unlock"], ["login_ok", "logout"]]

executed = set()
for path in paths:
    state = "Logged Out"
    for event in path:
        executed.add((state, event))
        state = table[(state, event)]

invalid_total = len(states) * len(events) - len(table)
print(len(executed), round(len(executed) / len(table) * 100, 1), invalid_total)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Printed output:

```
6 75.0 12
```

The script prints 6 transitions executed, 75.0 percent coverage, and 12 invalid cells.

**Explanation:** The paths execute 6 distinct valid transitions out of 8 (75.0%). The state table has 5 x 4 = 20 cells, so 20 - 8 = 12 are invalid.
- **Source:** state-transition-testing.md, section 9. Test coverage levels (Level 2 and Level 3)
</details>

---

## Part 5: Matching and Scenarios

**56.** Match each feature to the technique you would start with.

1. Order quantity field that accepts 1 to 100
2. Discount that depends on membership, order size and coupon together
3. Account that locks after three failed logins
4. A new user registers, verifies the email and logs in
5. A thin specification for a high-risk area with a history of defects

A. Error guessing
B. State transition testing
C. Use-case testing
D. Boundary value analysis
E. Decision table testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-D, 2-E, 3-B, 4-C, 5-A

**Explanation:** Numeric limits use BVA, combined conditions use decision tables, history-dependent behavior uses state transition testing, a complete journey uses use-case testing, and a thin spec with defect history calls for error guessing.
- **Source:** black-box-testing.md, section 7. How to choose a technique
</details>

---

**57.** Match each technique to its one-line definition.

1. Equivalence partitioning
2. Boundary value analysis
3. Decision table testing
4. State transition testing
5. Use-case testing

A. Test values at and next to the edges of ranges
B. Model states and events and test the transitions
C. Divide inputs into groups treated the same way and test one value from each
D. Derive tests from user scenarios: main flow, alternatives and failures
E. List combinations of conditions and the action each should cause

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-A, 3-E, 4-B, 5-D

**Explanation:** Each definition is from the overview of today's techniques.
- **Source:** black-box-testing.md, section 6. Overview of today's techniques
</details>

---

**58.** Match each coverage measure to the technique it belongs to.

1. Flows covered / total flows
2. Partitions covered / total partitions
3. Rules exercised / total feasible rules
4. Valid transitions executed / total valid transitions
5. Requirements with tests / total requirements (for example 9 of 12 = 75%)

A. Equivalence partitioning
B. Decision table testing
C. Black-box traceability (requirements coverage)
D. State transition testing
E. Use-case testing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-A, 3-B, 4-D, 5-C

**Explanation:** Each formula is the coverage definition from the respective lesson.
- **Source:** use-case-testing.md section 10; equivalence-partitioning.md EP Coverage; decision-table-testing.md section 8; state-transition-testing.md section 9; black-box-testing.md Knowledge Check answer 9
</details>

---

**59.** Match each source of experience to an example of a guess it produces.

1. Past defects
2. Production incidents
3. User complaints
4. Domain knowledge
5. Developer knowledge

A. A customer in another time zone saw yesterday's date
B. The email field accepted spaces last release, so try spaces in the phone field
C. Several users say the password reset email never arrives
D. The developer says the date logic was rushed and time zones are uncertain
E. Currency must round to two decimals and a refund must not exceed the original payment

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-A, 3-C, 4-E, 5-D

**Explanation:** The examples come from the sources table in the lesson.
- **Source:** error-guessing.md, section 4. Sources of experience
</details>

---

**60.** Match each use-case part to what it means.

1. Precondition
2. Trigger
3. Alternative flow
4. Exception flow
5. Postcondition

A. A valid variation that still ends in a valid outcome
B. What must be true before the use case starts
C. What must be true after it ends; the source of expected results
D. The event that starts the use case
E. What happens when something goes wrong, such as invalid input

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-D, 3-A, 4-E, 5-C

**Explanation:** Definitions come from the anatomy table of a use case.
- **Source:** use-case-testing.md, section 4. Anatomy of a use case
</details>

---

## Part 6: Scenarios on Project 1 (Registration and Login)

**61.** Project 1 registration requires passwords of 8 to 16 characters with a capital letter, a digit and a symbol. You want to test the minimum-length rule cleanly. Which test string is best?

- [ ] A) `abcdefg` (7 characters, lower case only)
- [ ] B) `Abcdef1!` (8 characters)
- [ ] C) `Abcde1!` (7 characters, otherwise valid)
- [ ] D) An empty password

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Abcde1!` (7 characters, otherwise valid)

**Explanation:** Each boundary test should violate only one rule. `Abcde1!` has length 7 and satisfies all other password rules.
- **Why others are wrong:**
  - A) It also violates the capital, digit and symbol rules, so a rejection cannot be blamed on length.
  - B) This is the minimum and valid; it tests acceptance, not the rejection just below minimum.
  - D) Empty is an extra edge, but it does not isolate the length boundary at 7.
- **Source:** boundary-value-analysis.md, section 10. Worked Example 2 (Important: make the password otherwise valid)
</details>

---

**62.** The Project 1 login rules are: if the account is locked, show a locked message; otherwise if username and password are both valid, log in; otherwise show invalid credentials. How many tests give 100% coverage of the collapsed decision table?

- [ ] A) 5
- [ ] B) 8
- [ ] C) 3
- [ ] D) 2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 5

**Explanation:** The collapsed table has 5 rules: locked (any username and password), success, and three invalid-credential rules.
- **Why others are wrong:**
  - B) That is the number of rules in the full table, not the collapsed one.
  - C) That is the number of different actions, not rules.
  - D) That counts only success versus failure.
- **Source:** decision-table-testing.md, section 6. Collapsing a Decision Table (8 Rules to 5)
</details>

---

**63.** The Project 1 registration form has 33 EP partitions (7 valid, 26 invalid). A tester runs only the two valid tests, which cover the 7 valid partitions. What is the EP coverage?

- [ ] A) 100%
- [ ] B) 7%
- [ ] C) 78.8%
- [ ] D) 21.2%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 21.2%

**Explanation:** Coverage = 7 / 33 x 100 = 21.2%, which exposes the false confidence of happy-path-only testing.
- **Why others are wrong:**
  - A) Only the 7 valid partitions are covered; 26 invalid ones are untouched.
  - B) That divides by 100 instead of 33.
  - C) That is the uncovered share (26 of 33), not the covered share.
- **Source:** equivalence-partitioning.md, EP Coverage (Project 1 registration form)
</details>

---

**64.** The Project 1 Login use case has 1 main flow, 4 alternative flows (A1 to A4) and 8 exception flows (E1 to E8). Tests cover the main flow, A1 to A3 and E1 to E6. What is the coverage (rounded to one decimal)?

- [ ] A) 62.5%
- [ ] B) 76.9%
- [ ] C) 83.3%
- [ ] D) 100%

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 76.9%

**Explanation:** Total flows are 1 + 4 + 8 = 13. Covered flows are 1 + 3 + 6 = 10, so 10 / 13 x 100 = 76.9%.
- **Why others are wrong:**
  - A) That ignores the correct total; it is not 10 of 16.
  - C) That would use 10 of 12; the use case has 13 flows.
  - D) Three flows (A4, E7, E8) are uncovered.
- **Source:** use-case-testing.md, Worked Example 1: Login (Flows count) and section 10. Coverage
</details>

---

**65.** Registration fails for the name D'Angelo. What is the best next step using error guessing?

- [ ] A) Try apostrophes in other text fields that store or display user text, such as address, comments and search
- [ ] B) Ignore it because only one name failed
- [ ] C) Retest only the name field with the values 18 and 60
- [ ] D) Use an AI answer of 'reject' as the expected result without checking the requirement

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Try apostrophes in other text fields that store or display user text, such as address, comments and search

**Explanation:** The failure belongs to the quotes and apostrophes category; the lesson says to check every text field that stores or displays user text.
- **Why others are wrong:**
  - B) Defects cluster, so one failure suggests the same fault elsewhere.
  - C) Those are age boundary values and unrelated to apostrophes.
  - D) Expected results come from requirements or the product owner, not from AI output.
- **Source:** error-guessing.md, Knowledge Check answer 6 (and answer 12)
</details>
