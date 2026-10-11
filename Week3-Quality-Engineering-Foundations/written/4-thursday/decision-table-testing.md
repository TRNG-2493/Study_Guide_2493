# Decision Table Testing

**Week 3 - Quality Engineering Foundations | Thursday: Test Design Techniques**

---

## Learning Objectives

By the end of this lesson you will be able to:

1. Explain the problem decision table testing solves and why Boundary Value Analysis (BVA) and Equivalence Partitioning (EP) alone can miss combination defects.
2. Describe the anatomy of a decision table: conditions, actions, rules, condition entries and action entries.
3. Distinguish a limited-entry decision table from an extended-entry decision table.
4. Build a decision table step by step, including calculating the number of rules, filling combinations with a repeatable pattern, marking impossible combinations and checking completeness and consistency.
5. Collapse (simplify) a decision table using don't-care entries without losing coverage.
6. Convert each rule (column) of a decision table into a concrete test case with test data and an expected result.
7. Calculate decision table coverage and explain why you must always state which table (full or simplified) the percentage refers to.
8. Translate requirement text containing words such as "if", "and", "or", "unless" and "otherwise" into a decision table, and use the process to discover missing or ambiguous requirements.
9. Combine decision tables with BVA and EP, and compare decision tables with flow charts and state tables.
10. Implement a rule function and a table-driven test list in Python, and use it to expose a deliberate defect.
11. Describe the strengths and limitations of the technique and strategies for handling a table that grows too large.

---

## Why This Matters

Imagine you join a team that is building an online store. The requirement says: "Members get 10% off. A valid coupon gives an extra 5%, but only on orders over $100. Orders over $100 ship free." You have already learned techniques that help here. Boundary Value Analysis tells you to test an order total of $100 and $100.01. Equivalence Partitioning tells you that one "member" and one "non-member" are enough to represent each group. Both are good techniques.

But look carefully at the requirement again. The outcome (the discount you pay and whether shipping is free) is not decided by one field. It is decided by the combination of three things at once: is the customer a member, is the order over $100, and is the coupon valid. There are eight possible combinations of those three yes/no answers. A tester who checks "a member" in one test, "an order over $100" in another test and "a valid coupon" in a third test has touched every individual input, yet may never have tried the specific combination "a member with a valid coupon on an order of $60", which is exactly where the code is most likely to be wrong.

Real-world software is full of business rules like this: banking approvals, insurance premiums, shipping charges, tax calculations, access permissions, login and registration validation. Defects love to hide in combinations of conditions, because developers often write the common combinations correctly and forget the odd ones. Decision table testing gives you a structured, visual, reviewable way to list every combination, decide the expected outcome for each, and turn each one into a test case. It also has a valuable side effect: while building the table you frequently discover that the requirement itself is incomplete or contradictory, which is the cheapest time to find a defect.

In this week's Project 1 (QE Foundations), the User Registration and Login features are rich in combined rules. Today's pair-programming exercise will have you apply this technique to them and cross-review each other's work, a very realistic practice in professional quality engineering teams.

---

## The Concept

### 1. The Problem: One Field at a Time Is Not Enough

Earlier today you learned two techniques that look at inputs **one at a time**:

- **Equivalence Partitioning (EP)** divides the possible values of one input into groups that the system should treat the same way, then tests one value per group.
- **Boundary Value Analysis (BVA)** tests the values at and next to the edges of those groups, because defects cluster at the edges.

Both techniques are excellent at answering: "Have I tried a good selection of values for this field?" They are not designed to answer: "Have I tried a good selection of combinations of fields?"

Consider a simple system with three yes/no inputs. If you test each input with "yes" once and "no" once, you can do it in as few as two tests (all yes, then all no), and every individual value has been exercised. But there are eight combinations, and six of them were never tried. If the business rule says "success requires A and B but not C", a defect in how A, B and C interact will slip straight through.

Decision table testing is a **black-box** technique (you design tests from the requirements, without looking at the code) that focuses on **business rules in which combinations of conditions determine the outcome**. It is the natural next step after use-case testing, BVA, EP and error guessing in today's sequence.

Use decision table testing when you see requirement language such as:

- "If the customer is a member and the order is over $100, then..."
- "Approval depends on age, income and credit rating."
- "The user can edit only if they own the record or are an administrator."

If the outcome depends on **one** input in isolation, EP and BVA are usually enough. If the outcome depends on **several inputs together**, reach for a decision table.

### 2. An Analogy: Truth Tables and House Rules

You may have met a **truth table** in a maths or programming class. A truth table lists every combination of true and false values for some statements and shows the result of combining them. For example, for "A AND B":

| A | B | A AND B |
|---|---|---------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

A decision table is a truth table that has grown up and gone to work in business. Instead of a bare "result" column, it shows the **actions** the system should take (show an error, grant a discount, send an email), and instead of abstract statements A and B, it uses real business **conditions** ("customer is a member", "order is over $100").

Another way to think about it: imagine a household with a set of "if-then" house rules.

- If it is a school night **and** homework is finished, then you may play games for one hour.
- If it is a school night **and** homework is not finished, then no games.
- If it is the weekend, then you may play games, whatever the homework situation.

Each house rule is a **rule** in a decision table. Written out as a table, anyone can check whether the family has covered every situation and whether two rules contradict each other ("games allowed" and "no games" for the same situation). That is precisely the power of a decision table: it makes rules **complete**, **consistent** and **testable**.

### 3. Definition and Anatomy of a Decision Table

A **decision table** (also called a cause-effect table) is a tabular representation of business logic that lists all relevant combinations of input conditions and shows the expected outcome for each combination. It is used both as a way to specify requirements and as a way to design tests.

Let us learn the vocabulary using a tiny example. Requirement: "Delivery is free when the order is over $50 or the customer is a member. Otherwise, delivery costs $5."

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| **Conditions** | | | | |
| Order over $50? | T | T | F | F |
| Customer is a member? | T | F | T | F |
| **Actions** | | | | |
| Free delivery | X | X | X | |
| Charge $5 delivery | | | | X |

Every part has a name:

- **Condition**: an input or circumstance that the system checks. Each row in the top half is one condition ("Order over $50?"). Conditions are the **causes**.
- **Action** (also called outcome or effect): something the system does or shows as a result. Each row in the bottom half is one action ("Free delivery"). Actions are the **effects**.
- **Rule**: one particular combination of condition values together with the actions that result. Each **column** (R1, R2, R3, R4) is a rule. A rule reads like a sentence: "If the order is over $50 and the customer is a member, then give free delivery."
- **Condition entry**: the value in a cell of the conditions section. In a limited-entry table the entries are:
  - **T** (True / Yes): the condition holds.
  - **F** (False / No): the condition does not hold.
  - **-** (don't care, also written as a dash, "N/A" or "irrelevant"): the condition's value has no influence on the outcome for this rule, so it can be either T or F.
- **Action entry**: the value in a cell of the actions section. Usually **X** means "this action happens" and a blank means "it does not happen". For actions that carry a value (such as a percentage), you can write the value itself instead (for example "10%").

Each column is a rule and each rule is a **test case waiting to be written**. That is the whole idea.

### 4. Limited-Entry vs Extended-Entry Decision Tables

**Limited-entry decision table.** Every condition is a Boolean question with only two possible answers: T or F (plus the don't-care dash). The delivery table above is limited-entry. This is the simplest and most common form.

**Extended-entry decision table.** A condition can take **more than two values**. Instead of T/F, the condition entry holds the actual value or range, such as an age bracket, a customer tier or a credit rating.

For example, in an extended-entry table the condition "Credit rating" could have the entries Poor, Fair or Good, and "Age bracket" could have 18-25, 26-60 or 61+. An extended-entry table is more compact than rewriting every multi-valued condition as several yes/no conditions, but it needs more care when counting rules (we will see how shortly).

Any extended-entry table can be converted into a limited-entry one. "Credit rating is Poor / Fair / Good" can become two Boolean conditions, "Credit is Poor?" and "Credit is Fair?" (if both are false, it is Good), but the conversion produces combinations that cannot exist (Poor and Fair at once). That is why many testers prefer to keep multi-valued conditions in extended form and avoid generating impossible combinations.

### 5. How to Build a Decision Table, Step by Step

Follow this repeatable recipe. We will use the delivery example when we need a quick illustration.

**Step 1: Identify the conditions and the actions.**
Read the requirement and list every input that influences the outcome (conditions) and every distinct result (actions). Ask: "What does the system check?" and "What does the system do or show?"

For the delivery rule: conditions = "order over $50", "customer is a member"; actions = "free delivery", "charge $5".

**Step 2: Compute the number of rules.**
For a limited-entry table with **n** Boolean conditions, the number of possible combinations is:

> **Number of rules = 2^n**

(two choices, multiplied together n times).

| Number of Boolean conditions (n) | Rules in the full table (2^n) |
|---|---|
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 5 | 32 |
| 6 | 64 |
| 10 | 1,024 |

For an **extended-entry** table, multiply the number of values of every condition:

> **Number of rules = (values of condition 1) x (values of condition 2) x ... x (values of condition n)**

Example: age bracket (3 values) x income level (3 values) x credit rating (3 values) = 27 rules. If a table mixes types, for example ticket type (3 values), matinee? (2) and student? (2), the full table has 3 x 2 x 2 = 12 rules.

Counting first gives you a target. When you finish filling the table you must have exactly that many combinations (before merging), no more and no fewer.

**Step 3: Fill in the condition combinations systematically.**
Never fill T/F values by gut feeling; you will skip or duplicate a combination. Use this repeatable pattern, working from the first condition (top row) to the last (bottom row):

- The **first** condition: the first half of the columns are T, the second half F. (That is 2^(n-1) T's followed by 2^(n-1) F's.)
- The **second** condition: alternate in blocks half as long: 2^(n-2) T's, then 2^(n-2) F's, repeating.
- Each following condition halves the block length again.
- The **last** condition simply alternates T, F, T, F, ...

For n = 3 (8 rules):

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Condition A (blocks of 4) | T | T | T | T | F | F | F | F |
| Condition B (blocks of 2) | T | T | F | F | T | T | F | F |
| Condition C (blocks of 1) | T | F | T | F | T | F | T | F |

For n = 4 (16 rules) the blocks are 8, 4, 2, 1. For n = 2 (4 rules) the blocks are 2 and 1, as in the delivery table. This is exactly the order of a truth table written from "all true" down to "all false", so every combination appears once and only once. After filling, do a quick check: scan across the columns and confirm no two columns are identical.

**Step 4: Define the expected actions for each rule.**
For every column, read the requirement and write down what the system should do. Put an X in each action that happens. If you cannot decide what should happen in a column, you have just found a **requirement gap**. Do not guess; write the question down and ask a business analyst or product owner. (More on this later.)

**Step 5: Mark impossible or infeasible combinations.**
Some combinations can never occur in real life. For example, "the account is locked" cannot be true if "the username exists" is false, because a non-existent account has no lock state. Mark such columns as **infeasible** (write "N/A" or "impossible" in the action section and shade or strike through the column) and give a one-line reason. Infeasible columns are removed from the number of tests, but keep them visible in the document so reviewers can confirm you reasoned about them. Be careful: only mark a combination impossible when the business or the design really prevents it. If it is merely unusual, it is a valid rule and may be an excellent negative test.

**Step 6: Merge rules with don't-care entries (collapse the table).**
Look for rules that have **identical actions** and differ in **exactly one** condition (one has T where the other has F). That condition does not influence the outcome in that situation, so the two columns can be merged into one with a dash in that position. Repeat until no more merges are possible. We demonstrate this in detail in the next section.

**Step 7: Check completeness.**
Completeness means every possible combination is covered by some rule. Verify with arithmetic: a rule with d dashes covers 2^d of the original combinations. The sum over all rules (including infeasible ones you set aside) must equal 2^n. If the total is too low, a combination is missing, which is a gap. If the total is too high, two rules overlap, which leads to the next check.

**Step 8: Check consistency (contradictions).**
Consistency means no combination of conditions has two different actions that cannot happen together. Overlapping rules that give different results are **contradictions**. For example, if one rule says "(T, -) gives 10% discount" and another says "(-, T) gives 5% discount", then the combination (T, T) is covered by both and the table does not say which applies. Either the requirement needs to specify a priority or the rules need to be rewritten so they do not overlap. Contradictions found at this stage are requirement defects, found without running a single test.

**Step 9: Turn rules into test cases.** Covered in section 7 below.

### 6. Collapsing a Decision Table: A Worked Demonstration (8 Rules to 5)

Let us take a login screen with three conditions. Requirement:

> "If the account is locked, show a 'locked' message, regardless of what was typed. Otherwise, if both username and password are valid, the user logs in successfully. Otherwise show an 'invalid credentials' error."

Conditions: **U** = username is valid, **P** = password is valid, **L** = account is locked. Actions: success, error message, locked message. n = 3, so 2^3 = 8 rules.

**Full table (8 rules):**

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| U: Username valid? | T | T | T | T | F | F | F | F |
| P: Password valid? | T | T | F | F | T | T | F | F |
| L: Account locked? | T | F | T | F | T | F | T | F |
| **Login success** | | X | | | | | | |
| **Invalid credentials error** | | | | X | | X | | X |
| **Locked message** | X | | X | | X | | X | |

Now apply Step 6. Find rules with the same action that differ in only one condition.

- R1, R3, R5 and R7 all have **L = T** and all lead to "Locked message". R1 and R3 differ only in P. Merge them: (T, -, T). R5 and R7 differ only in P: (F, -, T). Now (T, -, T) and (F, -, T) differ only in U: merge to (-, -, T). Four rules became one.
- The remaining rules (R2, R4, R6, R8) all have L = F. R2 is the only one leading to success; R4, R6 and R8 each lead to an error. Their condition values differ in both U and P in different ways, so none of them merge pairwise in a way that stays correct without further knowledge (we revisit this in Worked Example 1, where knowing some combinations are impossible allows more merging).

**Collapsed table (5 rules):**

| | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| U: Username valid? | - | T | T | F | F |
| P: Password valid? | - | T | F | T | F |
| L: Account locked? | T | F | F | F | F |
| **Login success** | | X | | | |
| **Invalid credentials error** | | | X | X | X |
| **Locked message** | X | | | | |

The completeness check: R1 has two dashes, so it covers 2^2 = 4 combinations. Each of the other four rules has no dashes, covering 1 each. 4 + 1 + 1 + 1 + 1 = 8 = 2^3. The table is complete. No two rules overlap (R1 requires L = T and every other rule requires L = F), so it is consistent. We reduced 8 rules to 5 without losing any information.

The "dash" is a promise: "for this rule, I claim the value of this condition does not change the outcome." That promise comes from the requirement, not from convenience. If you are not sure, do not merge.

### 7. Converting Each Rule into a Test Case

Each remaining rule (column) becomes at least one test case. The recipe is:

1. **Pick concrete data** that makes every condition in the rule true or false as specified. For a dash, you may choose any value (see tip below).
2. **Take the expected result** straight from the action entries of the rule.
3. **Write the test case** with an ID, a title, preconditions, steps, test data and expected result, and a reference back to the rule number so a reviewer can trace it (traceability).

For the collapsed login table:

| Test ID | Rule | Test data / setup | Expected result |
|---|---|---|---|
| TC-LOG-01 | R1 | Account `bob_locked` is locked; enter its correct username and correct password | Locked message shown; no login |
| TC-LOG-02 | R2 | Account `alice` is active; correct username, correct password | Login succeeds; user is taken to the home page |
| TC-LOG-03 | R3 | Account `alice` is active; correct username, wrong password | Invalid credentials error |
| TC-LOG-04 | R4 | Account `alice` is active; incorrect username, correct password | Invalid credentials error |
| TC-LOG-05 | R5 | Account `alice` is active; incorrect username, wrong password | Invalid credentials error |

Tip for dashes: when you test a rule that contains a don't-care, a sensible strategy is to pick the value that is **most likely to expose a defect** or that varies across tests. For example, in TC-LOG-01 you could use a correct password in one run and a wrong password in another, to confirm the locked message really does take priority over password checking. When tests are cheap, test several values of the don't-care; when they are expensive, test one.

### 8. Decision Table Coverage

**Coverage** is a measure of how much of something your tests have exercised. For decision tables the "something" is the set of rules. The formula is:

> **Decision table coverage (%) = (number of rules exercised by at least one test / total number of feasible rules in the table) x 100**

A rule is exercised when you run a test whose data satisfies that rule's conditions and you verify the actions of that rule.

**Which table is the denominator?** This is the critical detail. Coverage is always relative to a table, so always state it.

- **100% coverage of the full table** means one test per feasible original combination. For the login example in the previous section, the full table has 8 rules.
- **100% coverage of the simplified (collapsed) table** means one test per collapsed rule. The collapsed login table has 5 rules, so 5 tests give 100%.

Example: you run only TC-LOG-02, TC-LOG-03 and TC-LOG-04 from the list above. That exercises 3 of the 5 rules in the collapsed table:

> Coverage = 3 / 5 x 100 = **60%** (of the collapsed table)

Against the full table of 8 rules, the same three tests exercise 3 combinations (R2, R4, R6 in the full numbering): 3 / 8 = **37.5%**. Both numbers are correct; they answer different questions. In a test report, write "60% of the collapsed decision table (5 rules)" so nobody is misled.

A commonly accepted professional standard (and the one referenced in the ISTQB syllabus) is to aim for **100% coverage of the feasible rules in the (collapsed) table**, which is the minimum needed to say "every business rule has been tested at least once". Exercising the don't-care values on top of that is extra confidence for a small cost.

### 9. Worked Example 1: Login (Username, Password, Locked)

Let us now do the complete job for the login feature, including impossible combinations and a deeper collapse.

**Requirement (assumed for this lesson):**

1. If the username does not match an existing account, show "Invalid username or password".
2. If the username matches an account and the password does not match it, show "Invalid username or password" (the same message, so attackers cannot learn which usernames exist).
3. If the account is locked (for example after too many failed attempts), show "Your account is locked" even if the password is correct.
4. Otherwise (existing, unlocked account with a matching password), log the user in.

**Conditions:** U = username valid (an account with that username exists); P = password valid (matches the password stored for that account); L = account is locked.
**Actions:** Login success; Error message; Locked message.

**Step 1 - Full table (2^3 = 8 rules).** Notice we also mark infeasible columns.

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| U: Username valid? | T | T | T | T | F | F | F | F |
| P: Password valid? | T | T | F | F | T | T | F | F |
| L: Account locked? | T | F | T | F | T | F | T | F |
| **Feasible?** | Yes | Yes | Yes | Yes | **No** | **No** | **No** | Yes |
| **Login success** | | X | | | n/a | n/a | n/a | |
| **Error message** | | | | X | n/a | n/a | n/a | X |
| **Locked message** | X | | X | | n/a | n/a | n/a | |

**Why are R5, R6 and R7 impossible?**

- "Password valid" means "matches the password of the account that was found". If the username is not valid, no account was found, so there is nothing for the password to match: **U = F with P = T cannot happen** (R5 and R6).
- A locked state belongs to an account. If no account exists, nothing can be locked: **U = F with L = T cannot happen** (R5 and R7).

The union of the two impossible patterns is R5, R6 and R7. That leaves **5 feasible rules: R1, R2, R3, R4, R8.**

**Step 2 - Collapse the feasible rules.**

- R1 (T, T, T) and R3 (T, F, T) both give the locked message and differ only in P. Merge: **(T, -, T)**.
- R4 (T, F, F) and R8 (F, F, F) both give the error and differ only in U. Merge: **(-, F, F)**.
- R2 (T, T, F) is the only success rule and stays alone.

**Collapsed table (3 rules):**

| | R1 | R2 | R3 |
|---|---|---|---|
| U: Username valid? | T | T | - |
| P: Password valid? | - | T | F |
| L: Account locked? | T | F | F |
| **Login success** | | X | |
| **Error message** | | | X |
| **Locked message** | X | | |

**Completeness check.** R1 covers 2 combinations (original R1 and R3), R2 covers 1, R3 covers 2 (original R4 and R8). 2 + 1 + 2 = 5 feasible combinations, plus 3 infeasible ones set aside = 8 = 2^3. Complete. **Consistency check.** No combination appears under two rules. Consistent.

**Step 3 - Test cases.** One test per collapsed rule gives 100% coverage of the collapsed table. Because rule R3 has a dash for U, and the two U values behave differently in the system's logic (account lookup succeeds or fails), we choose to test both, which is cheap and also verifies that the message is identical for the two cases.

| Test ID | Rule | Username | Password | Account state | Expected result |
|---|---|---|---|---|---|
| TC-L-01 | R1 | bob_locked | (bob's correct password) | Locked | "Your account is locked" shown; not logged in |
| TC-L-02 | R2 | alice | (alice's correct password) | Active | Login succeeds; home page shown |
| TC-L-03a | R3 (U = T) | alice | WrongPass1 | Active | "Invalid username or password" |
| TC-L-03b | R3 (U = F) | nosuchuser | WrongPass1 | n/a | "Invalid username or password" (identical text) |

That is 4 tests covering 100% of the 3-rule collapsed table. To reach 100% of the 5-rule feasible full table you would add TC-L-04 (locked account, wrong password, expecting the locked message), which verifies that "locked" beats "wrong password". Many teams add that test anyway because it protects against a classic defect. Notice that the decision table made us think about it.

### 10. Worked Example 2: Online Store Discount

**Requirement:**

> "Members receive 10% off. A valid coupon gives an extra 5% off, but only on orders over $100. Orders over $100 ship free. Everything else is charged at the normal price and shipping."

**Conditions:** M = customer is a member; O = order total is over $100; C = coupon is valid.
**Actions:** discount percentage (0%, 5%, 10% or 15%); free shipping (X or blank).

**Full table (2^3 = 8 rules):**

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| M: Member? | T | T | T | T | F | F | F | F |
| O: Order over $100? | T | T | F | F | T | T | F | F |
| C: Coupon valid? | T | F | T | F | T | F | T | F |
| **Discount %** | 15% | 10% | 10% | 10% | 5% | 0% | 0% | 0% |
| **Free shipping** | X | X | | | X | X | | |

Look at R3 and R4: the order is not over $100, so the coupon has no effect; both give 10% and no free shipping. Likewise R7 and R8 both give 0% and no free shipping. These pairs differ only in C and have identical actions, so merge them with a dash.

**Collapsed table (6 rules):**

| | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|
| M: Member? | T | T | T | F | F | F |
| O: Order over $100? | T | T | F | T | T | F |
| C: Coupon valid? | T | F | - | T | F | - |
| **Discount %** | 15% | 10% | 10% | 5% | 0% | 0% |
| **Free shipping** | X | X | | X | X | |

Completeness: R3 and R6 have one dash each (2 combinations each); the other four rules cover 1 each. 2 + 2 + 1 + 1 + 1 + 1 = 8. Complete. We reduced 8 rules to 6.

**Test cases (one per collapsed rule, with chosen coupon for the dashes set to "valid" to try to provoke a defect):**

| Test ID | Rule | Member | Order total | Coupon | Expected discount | Expected free shipping |
|---|---|---|---|---|---|---|
| TC-D-01 | R1 | Yes | $150.00 | Valid | 15% | Yes |
| TC-D-02 | R2 | Yes | $150.00 | None | 10% | Yes |
| TC-D-03 | R3 | Yes | $60.00 | Valid (ignored) | 10% | No |
| TC-D-04 | R4 | No | $150.00 | Valid | 5% | Yes |
| TC-D-05 | R5 | No | $150.00 | None | 0% | Yes |
| TC-D-06 | R6 | No | $60.00 | Valid (ignored) | 0% | No |

Why choose "valid coupon" for the dash rules? Because that is the value most likely to trigger a defect: if a developer forgot "only on orders over $100", a valid coupon on a small order would wrongly add 5%. Notice that this is exactly the defect we will plant and catch in the Python demo.

**Connecting to BVA.** The condition "order over $100" is defined by a boundary. $150 and $60 are fine representatives for the rules, but BVA tells us the defect-prone values are exactly **$100.00** (not over) and **$100.01** (over). Add those as extra tests on top of the table; see the BVA lesson from earlier today.

### 11. Worked Example 3: Loan Eligibility (Extended-Entry Table)

**Requirement (simplified):**

- Applicants with a **Poor** credit rating are rejected.
- With **Good** credit: high income is approved; medium income is approved if the applicant is aged 26-60, otherwise referred to a human underwriter; low income is referred.
- With **Fair** credit: high income is approved if aged 26-60, otherwise referred; medium income is referred; low income is rejected.

**Conditions (extended entry):**

- Age bracket: 18-25, 26-60, 61+ (3 values)
- Income level: Low, Medium, High (3 values)
- Credit rating: Poor, Fair, Good (3 values)

**Actions:** Approve, Refer, Reject.

**Number of rules in the full table:** 3 x 3 x 3 = **27**. Writing out 27 columns is tedious and error-prone, so we go straight to a collapsed table, using "-" for "any value". Because an extended table with many rules is wide, we use the common **transposed layout**: each row is a rule, each column is a condition or action. (A decision table can be drawn either way; the content is the same.)

| Rule | Age | Income | Credit | Action | Original combinations covered |
|---|---|---|---|---|---|
| R1 | - | - | Poor | Reject | 9 |
| R2 | - | High | Good | Approve | 3 |
| R3 | 26-60 | Medium | Good | Approve | 1 |
| R4 | 18-25 | Medium | Good | Refer | 1 |
| R5 | 61+ | Medium | Good | Refer | 1 |
| R6 | - | Low | Good | Refer | 3 |
| R7 | 26-60 | High | Fair | Approve | 1 |
| R8 | 18-25 | High | Fair | Refer | 1 |
| R9 | 61+ | High | Fair | Refer | 1 |
| R10 | - | Medium | Fair | Refer | 3 |
| R11 | - | Low | Fair | Reject | 3 |
| **Total** | | | | | **27** |

Check: 9 + 3 + 1 + 1 + 1 + 3 + 1 + 1 + 1 + 3 + 3 = 27. The table is complete: it accounts for all 3 x 3 x 3 combinations. We reduced 27 original combinations to 11 rules. A quick look also shows no overlap (for example R2 requires Good credit and High income; no other rule with Good credit and High income exists), so it is consistent.

Could we merge more? R4 and R5 have the same action (Refer) under the same income and credit, differing in age (18-25 vs 61+). We could merge them into a single rule with the entry "18-25 or 61+" (equivalently "not 26-60"). Whether that is allowed depends on your team's notation. Doing so would give 10 rules; the same applies to R8 and R9, giving 9 rules. Both forms are valid. For the sake of testing, the two separate age brackets are different equivalence classes, so many testers keep them separate to ensure both are executed.

**Test cases for 100% coverage of the 11-rule table.** We use EP to choose a representative age for each bracket, and BVA suggestions are noted for the age edges.

| Test ID | Rule | Age | Income | Credit | Expected |
|---|---|---|---|---|---|
| TC-LN-01 | R1 | 40 | Medium | Poor | Reject |
| TC-LN-02 | R2 | 30 | High | Good | Approve |
| TC-LN-03 | R3 | 40 | Medium | Good | Approve |
| TC-LN-04 | R4 | 22 | Medium | Good | Refer |
| TC-LN-05 | R5 | 70 | Medium | Good | Refer |
| TC-LN-06 | R6 | 35 | Low | Good | Refer |
| TC-LN-07 | R7 | 50 | High | Fair | Approve |
| TC-LN-08 | R8 | 20 | High | Fair | Refer |
| TC-LN-09 | R9 | 65 | High | Fair | Refer |
| TC-LN-10 | R10 | 45 | Medium | Fair | Refer |
| TC-LN-11 | R11 | 33 | Low | Fair | Reject |

If we want to be thorough on the age boundaries (25 vs 26 and 60 vs 61), BVA suggests extra tests such as age 25 and 26 for R3/R4 and age 60 and 61 for R3/R5. The age brackets also hide a gap: what happens to an applicant aged 17 or younger? The requirement did not say. That is a requirement gap discovered while building the table.

### 12. Worked Example 4: Project 1 Registration Validity

Now let us apply the technique to the sample web app you are testing all week. Assume the following (to be confirmed against the actual Project 1 requirements, which is part of today's exercise):

> "When the user clicks **Register**, the system validates the form in this order and shows only the first problem it finds: (1) the email must be valid, (2) the password must be strong, (3) the terms and conditions must be accepted, (4) the username must be available. If all four checks pass, the account is created."

**Conditions:** E = email is valid; P = password is strong (meets the password policy); T = terms accepted; U = username is available.
**Actions:** Create account; Show email error; Show password error; Show terms error; Show username error.

n = 4, so the full table has 2^4 = **16 rules**. Using the fill pattern (blocks of 8, 4, 2, 1), and because only the first failing check is shown:

| Rule | E | P | T | U | Action |
|---|---|---|---|---|---|
| 1 | T | T | T | T | Create account |
| 2 | T | T | T | F | Username error |
| 3 | T | T | F | T | Terms error |
| 4 | T | T | F | F | Terms error |
| 5 | T | F | T | T | Password error |
| 6 | T | F | T | F | Password error |
| 7 | T | F | F | T | Password error |
| 8 | T | F | F | F | Password error |
| 9 | F | T | T | T | Email error |
| 10 | F | T | T | F | Email error |
| 11 | F | T | F | T | Email error |
| 12 | F | T | F | F | Email error |
| 13 | F | F | T | T | Email error |
| 14 | F | F | T | F | Email error |
| 15 | F | F | F | T | Email error |
| 16 | F | F | F | F | Email error |

Reading the table, the pattern jumps out: rules 9-16 are all identical in action, so E = F makes everything after it irrelevant. Rules 5-8 are identical when E = T and P = F. Rules 3-4 are identical when E, P = T and T = F. Collapse:

**Collapsed table (5 rules):**

| Rule | E | P | T | U | Action | Original rules covered |
|---|---|---|---|---|---|---|
| R1 | F | - | - | - | Show email error | 8 |
| R2 | T | F | - | - | Show password error | 4 |
| R3 | T | T | F | - | Show terms error | 2 |
| R4 | T | T | T | F | Show username error | 1 |
| R5 | T | T | T | T | Create account | 1 |
| **Total** | | | | | | **16** |

8 + 4 + 2 + 1 + 1 = 16. Complete. We reduced 16 rules to 5.

**Test cases:**

| Test ID | Rule | Email | Password | Terms | Username | Expected result |
|---|---|---|---|---|---|---|
| TC-REG-01 | R5 | trainee1@example.com | Str0ng!Pass9 | Checked | newlearner01 | Account created; confirmation or welcome page shown |
| TC-REG-02 | R1 | trainee1@@example | Str0ng!Pass9 | Checked | newlearner01 | Email error shown; no account created |
| TC-REG-03 | R2 | trainee1@example.com | abc | Checked | newlearner01 | Password error shown; no account created |
| TC-REG-04 | R3 | trainee1@example.com | Str0ng!Pass9 | Unchecked | newlearner01 | Terms error shown; no account created |
| TC-REG-05 | R4 | trainee1@example.com | Str0ng!Pass9 | Checked | admin (already taken) | Username error shown; no account created |
| TC-REG-06 | Don't-care check for R1 | invalid email | weak password | Unchecked | taken username | Only the email error is shown (verifies the priority assumption behind the dashes) |

Test TC-REG-06 is a bonus: the dashes in the collapsed table rely on the "first error only" rule. By deliberately making everything invalid at once, we verify that assumption instead of just trusting it. If the real Project 1 shows all errors at once, the table is different: the errors become independent and the actions per rule would list several errors together. That is a perfect example of why you confirm the rule with the business first.

For each condition you also need good test **data**. That is where EP and BVA come back: "email is valid" is itself an equivalence class with many invalid representatives (missing `@`, missing domain, spaces), and "password is strong" has length boundaries (for example, minimum 8 characters: test 7 and 8). Decision tables decide **which combinations** to test; EP and BVA decide **which values** to use.

### 13. Cause-Effect Graphs (A Name to Remember)

You may see the term **cause-effect graph** in textbooks and in the ISTQB glossary. It is a diagram that draws causes (conditions) and effects (actions) as nodes joined by logical operators such as AND, OR and NOT, and from which a decision table can be derived. We will not draw cause-effect graphs in this course; just remember that they are a related technique, and that a decision table is the usual end product of both approaches.

### 14. Decision Tables from Requirements Text: Reading Between the Lines

In real projects the requirement does not arrive as a neat table. It arrives as sentences, and your job is to extract the table. Here is a practical method.

**Step A: Highlight the logic words.** Read the requirement slowly and mark these words, which almost always signal conditions and rules:

| Word | What it usually means in a table |
|---|---|
| **if** | Introduces a condition (the "cause") |
| **and** | Two conditions must both be true: they sit in the **same rule (column)** |
| **or** | Either condition is enough: it produces **several rules** with the same action (or a dash arrangement) |
| **unless** | "If not": the condition after "unless" must be **false** for the main action to apply |
| **otherwise / else** | The default rule that covers everything not handled by the earlier rules |
| **only if / only when** | The condition is **required**: without it, the action must not happen |
| **at least / more than / up to** | A boundary: send the condition to BVA for edge values |
| **except** | Like "unless": an exception that overrides the general rule |
| **when / whenever** | Another way of writing "if" |

**Step B: Translate a sentence into a table.** Take this requirement:

> "Shipping is free for orders over $100 or for members, unless the item is oversized. Otherwise shipping costs $5."

Highlighting: **or** (over $100 or members), **unless** (oversized), **otherwise** ($5).

Conditions: O = order over $100; M = member; Z = item is oversized. Actions: free shipping; charge $5. n = 3 so 8 combinations in the full table.

Reading the sentence: "unless oversized" means that when Z is true, free shipping does not apply, so the $5 charge applies. When Z is false, free shipping applies if O or M is true; otherwise (neither) $5.

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| O: Order over $100? | - | T | F | F |
| M: Member? | - | - | T | F |
| Z: Oversized? | T | F | F | F |
| **Free shipping** | | X | X | |
| **Charge $5** | X | | | X |
| Original combinations covered | 4 | 2 | 1 | 1 |

4 + 2 + 1 + 1 = 8. Complete.

**Step C: Find the ambiguities.** Writing the table forces you to ask questions the prose never answered:

- Does "unless the item is oversized" apply to members as well as to big spenders? (We assumed yes. The sentence could also mean "unless oversized" applies only to the over-$100 group.)
- Is an oversized item charged $5 or some larger oversize fee? The text says "otherwise $5", but is that sensible?
- Does "over $100" include exactly $100? ("over" suggests not, but confirm; this is a BVA question.)
- Is the $100 measured before or after discounts and tax?

**Step D: Find the gaps (bonus).** A gap is a combination of conditions for which the requirement says nothing. Imagine the requirement: "Customers with a coupon get 5% off. Members get 10% off." Build the table and you immediately face a column where both are true: do they stack, does the better one win, or is only one allowed? The text is silent. Similarly, "What if the coupon is expired?" and "Does the coupon work on sale items?" are gaps. Every blank or unanswerable column in your table is a question for the product owner. Finding these before development is one of the most valuable things a tester can do, and it is a practical illustration of the principle you learned on Wednesday: testing starts early and prevention is cheaper than cure.

### 15. Reviewing a Decision Table with Business Stakeholders

A decision table is one of the friendliest test artefacts to review with non-technical people, because it is just a grid of business rules. Use this approach when you meet product owners, business analysts or developers:

1. **Explain the notation in one minute.** "Each column is one situation. T means yes, F means no, a dash means it does not matter. The bottom rows show what the system should do."
2. **Walk through the rules aloud** in plain English, one column at a time: "If the customer is a member and the order is not over $100, then the discount is 10% and shipping is charged. Is that right?"
3. **Ask about the dashes.** "I have marked the coupon as irrelevant when the order is under $100. Is that really true?"
4. **Show the impossible combinations** and the reasons, and ask them to confirm they truly cannot occur.
5. **Capture questions and decisions** on the document, and update the table. Agree who owns each open question.
6. **Get sign-off or acknowledgement** on the final table; it then becomes a shared source of truth, and your test cases trace back to it.

Keep tables small enough to read on one screen. If a stakeholder is struggling, split the table (see the strategies in Section 17) or read out the collapsed version first.

### 16. Decision Tables vs Flow Charts vs State Tables

You will meet three different ways to describe how a system behaves. They overlap, but each is best at something different.

| Aspect | Decision table | Flow chart | State table / state diagram |
|---|---|---|---|
| Main idea | Combinations of conditions lead to outcomes | A sequence of steps and decisions | The system moves between states when events happen |
| Best for | Business rules with several interacting conditions | Processes and workflows (what happens in what order) | Behaviour that depends on history (what happened before) |
| Order of checks | Does not matter (conditions are considered together) | Matters (each decision comes after the previous one) | Matters (events are sequenced) |
| Completeness check | Easy: count the combinations (2^n) | Harder: easy to forget a branch | Check every state against every event |
| Typical example | Discount rules, eligibility, validation | Order fulfilment, support triage | Order status (new, paid, shipped), account lock |
| Typical test design | One test per rule | One test per path | One test per transition or sequence |

An easy test: if the answer to "what should happen?" depends on a **set of facts true right now**, use a decision table. If it depends on **what has already happened** (for example "the account becomes locked after three failed attempts"), the system has memory and you need states; that is the topic of the **state transition testing** lesson, coming next. In the login feature you saw both: the decision table covers "what do we show given these three facts", and a state model will later cover "how does the account become locked in the first place".

### 17. Strengths, Limitations and Taming Large Tables

**Strengths**

- Gives **systematic, complete** coverage of combinations of conditions; nothing is left to memory.
- Shows **requirement gaps and contradictions** early, even before code exists.
- Easy to **review** with non-technical stakeholders; one table serves as requirement, test design and documentation.
- Produces **traceable** tests: each test links to a rule.
- Simple to turn into **automated** checks, as the Python demo below shows.

**Limitations**

- **Combination explosion.** The number of rules doubles with each Boolean condition (2^n). 10 conditions means 1,024 rules; 20 conditions means more than a million. Raw tables become unreadable and unmaintainable.
- Works best for **logic that is order-independent**; it does not naturally model sequences or history (use state transition testing).
- Needs **clear, discrete conditions**; continuous inputs must first be divided into classes using EP/BVA.
- Quality depends on the **quality of the requirement**. A wrong table gives wrong tests with great confidence.

**Strategies when a table gets too big**

1. **Collapse with don't-cares.** Always the first move. Many large tables shrink dramatically (the registration table went from 16 to 5).
2. **Remove infeasible combinations.** Document why they cannot occur.
3. **Split the table.** If the conditions fall into independent groups, build two or three small tables instead of one huge one. For example, a table for "discount rules" and a separate table for "shipping rules" when they do not depend on one another.
4. **Layer the table.** Treat a group of conditions as one derived condition. For example, instead of listing five password rules as five conditions, define "password is strong" as a single condition and test those five rules separately with EP/BVA.
5. **Prioritise by risk.** If you cannot test everything, test the rules with the highest business impact and likelihood of failure first (a Wednesday principle: exhaustive testing is impossible).
6. **Use a combinatorial technique.** There are methods that deliberately test only a well-chosen subset of combinations, such as **pairwise (all-pairs) testing**. We mention it by name only; you will meet it later in the programme.

### 18. A Python Demo: Rules as Code, Rules as Test Table

Now we make the decision table executable. We will implement the discount rule from Worked Example 2 as a Python function, write a **table-driven test list** (a list of tuples, one row per rule, mirroring the decision table), and see the table catch a deliberate defect.

You do not need to master Python for this; read the explanations line by line. Python is introduced properly in later weeks. Save the following as `discount_demo.py` and run it with `python3 discount_demo.py` (any Python 3.8 or newer works).

**Version 1: the code with a deliberate defect**

```python
"""Decision table demo: calculate_discount and a table-driven test list."""


def calculate_discount(is_member, order_total, has_coupon):
    """Return (discount_percent, free_shipping)."""
    discount = 0
    if is_member:
        discount = 10
    free_shipping = order_total > 100
    if has_coupon:  # BUG: coupon should only count when order_total > 100
        discount += 5
    return discount, free_shipping


TEST_CASES = [
    # (rule, is_member, order_total, has_coupon, expected_discount, expected_free_shipping)
    ("R1", True, 150.00, True, 15, True),
    ("R2", True, 150.00, False, 10, True),
    ("R3", True, 60.00, True, 10, False),
    ("R4", True, 60.00, False, 10, False),
    ("R5", False, 150.00, True, 5, True),
    ("R6", False, 150.00, False, 0, True),
    ("R7", False, 60.00, True, 0, False),
    ("R8", False, 60.00, False, 0, False),
    ("B1", False, 100.00, True, 0, False),
    ("B2", False, 100.01, True, 5, True),
]


def run_table(tests):
    failures = 0
    for rule, member, total, coupon, exp_discount, exp_ship in tests:
        actual = calculate_discount(member, total, coupon)
        expected = (exp_discount, exp_ship)
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{rule}: member={member!s:5} total={total:7.2f} coupon={coupon!s:5} "
              f"expected={expected} actual={actual} -> {status}")
    print(f"{len(tests) - failures} passed, {failures} failed")
    return failures


if __name__ == "__main__":
    run_table(TEST_CASES)
```

**Line-by-line explanation**

- `"""Decision table demo..."""` at the top: a **docstring**, a description of the file. Python ignores it when running; it is for humans.
- `def calculate_discount(is_member, order_total, has_coupon):` defines a **function** (a reusable block of code) called `calculate_discount`. It takes three **parameters**, which are exactly our three decision table conditions: M (`is_member`), O (`order_total`, from which "over $100" is derived) and C (`has_coupon`).
- `"""Return (discount_percent, free_shipping)."""` the function's own docstring, saying that it returns two values bundled together (a **tuple**): the percentage and whether shipping is free. These are our two action rows.
- `discount = 0` creates a variable holding the discount so far and starts it at zero (the default "no discount" outcome).
- `if is_member:` checks the first condition. In Python, a value of `True` makes the indented lines under it run.
- `discount = 10` members get 10%.
- `free_shipping = order_total > 100` evaluates the comparison "order total is greater than 100", which is either `True` or `False`, and stores it. Using `>` (not `>=`) matches the requirement "over $100": exactly $100 does not qualify. This is the boundary BVA warned us about.
- `if has_coupon:  # BUG: ...` the coupon check. Everything after `#` is a **comment**, a note ignored by Python. This line is deliberately wrong: it adds the coupon bonus whenever a coupon exists, without checking that the order is over $100.
- `discount += 5` adds 5 to the current discount (`discount = discount + 5`).
- `return discount, free_shipping` hands the two results back to whoever called the function, as a tuple.
- `TEST_CASES = [ ... ]` defines the **table-driven test list**: a list of tuples where each tuple is one row of the decision table, written as data. The first comment line names the columns. Rows R1-R8 are the **full** 8-rule table in the same order as Worked Example 2 (R1 = member, over $100, coupon ... R8 = non-member, not over $100, no coupon). The totals $150.00 and $60.00 are our "over" and "under" representatives. Rows B1 and B2 are the BVA additions: $100.00 must **not** count as over $100 (so no free shipping, and the coupon must not apply) and $100.01 must count.
- `def run_table(tests):` defines a second function that runs every row.
- `failures = 0` a counter for failed rows.
- `for rule, member, total, coupon, exp_discount, exp_ship in tests:` a **loop**. For each tuple in the list it **unpacks** the six values into six named variables. This single loop is what makes the test "table-driven": adding a rule means adding a row, not writing new code.
- `actual = calculate_discount(member, total, coupon)` calls the function under test with the row's inputs and stores what it returns.
- `expected = (exp_discount, exp_ship)` builds the expected result in the same shape (a tuple) as the actual result.
- `status = "PASS" if actual == expected else "FAIL"` compares them. `==` tests equality; the whole line chooses the word PASS or FAIL.
- `if status == "FAIL":` and `failures += 1` count the failures.
- The `print(f"...")` statement shows one result line. The `f` before the quote makes it an **f-string**, where `{ ... }` inserts values. `{member!s:5}` shows the value as text padded to 5 characters, and `{total:7.2f}` shows a number with 2 decimals padded to 7 characters, just to line columns up.
- `print(f"{len(tests) - failures} passed, {failures} failed")` prints a summary: the number of rows minus the failures, then the failures.
- `return failures` hands the count back so that other code (or later, an automation tool) could use it.
- `if __name__ == "__main__":` means "only run the next line when this file is executed directly". `run_table(TEST_CASES)` then runs the whole table.

**Run it. Expected output (the failing run):**

```
R1: member=True  total= 150.00 coupon=True  expected=(15, True) actual=(15, True) -> PASS
R2: member=True  total= 150.00 coupon=False expected=(10, True) actual=(10, True) -> PASS
R3: member=True  total=  60.00 coupon=True  expected=(10, False) actual=(15, False) -> FAIL
R4: member=True  total=  60.00 coupon=False expected=(10, False) actual=(10, False) -> PASS
R5: member=False total= 150.00 coupon=True  expected=(5, True) actual=(5, True) -> PASS
R6: member=False total= 150.00 coupon=False expected=(0, True) actual=(0, True) -> PASS
R7: member=False total=  60.00 coupon=True  expected=(0, False) actual=(5, False) -> FAIL
R8: member=False total=  60.00 coupon=False expected=(0, False) actual=(0, False) -> PASS
B1: member=False total= 100.00 coupon=True  expected=(0, False) actual=(5, False) -> FAIL
B2: member=False total= 100.01 coupon=True  expected=(5, True) actual=(5, True) -> PASS
7 passed, 3 failed
```

**Reading the result like a tester.** Three rows fail: R3, R7 and B1. What do they have in common? In every failing row, `has_coupon` is `True` and the order is **not** over $100. The passing rows with a coupon (R1, R5, B2) all have orders over $100. The table has pointed straight at the cause: the coupon is being applied to orders that are too small. Notice something else: a tester who tried only "member", "big order" and "coupon" as separate single-factor tests would likely have passed every one of them. Only the specific **combination** "coupon + small order" reveals the defect, which is exactly the class of bug decision tables are designed to catch. Note too that B1 (exactly $100.00) is just another small-order case here, so the boundary was not the real culprit; the combination was. A good defect report would read: "Coupon discount applied on orders of $100 or less; expected only on orders over $100 (rules R3, R7 of the discount table)."

**Version 2: the fix.** Change only the coupon line so it also checks the order total:

```python
    if has_coupon and order_total > 100:  # FIX: coupon only counts on orders over 100
        discount += 5
```

The only difference is `and order_total > 100`: the `and` requires **both** parts to be true, matching the requirement "a coupon gives an extra 5%, but only on orders over $100". Because `free_shipping` already holds the result of that same comparison, you could also write `if has_coupon and free_shipping:` but being explicit keeps the code readable.

**Run again. Expected output (the passing run):**

```
R1: member=True  total= 150.00 coupon=True  expected=(15, True) actual=(15, True) -> PASS
R2: member=True  total= 150.00 coupon=False expected=(10, True) actual=(10, True) -> PASS
R3: member=True  total=  60.00 coupon=True  expected=(10, False) actual=(10, False) -> PASS
R4: member=True  total=  60.00 coupon=False expected=(10, False) actual=(10, False) -> PASS
R5: member=False total= 150.00 coupon=True  expected=(5, True) actual=(5, True) -> PASS
R6: member=False total= 150.00 coupon=False expected=(0, True) actual=(0, True) -> PASS
R7: member=False total=  60.00 coupon=True  expected=(0, False) actual=(0, False) -> PASS
R8: member=False total=  60.00 coupon=False expected=(0, False) actual=(0, False) -> PASS
B1: member=False total= 100.00 coupon=True  expected=(0, False) actual=(0, False) -> PASS
B2: member=False total= 100.01 coupon=True  expected=(5, True) actual=(5, True) -> PASS
10 passed, 0 failed
```

All 10 rows pass. We have just practised the full cycle: table, rule function, table-driven tests, defect found, defect fixed, regression confirmed (the previously passing rows still pass).

Two observations about the design. First, the test list mirrors the decision table row for row, so a reviewer can compare them side by side; that is traceability in action. Second, to keep the demo faithful to the 6-rule collapsed table you could use only R1, R2, R3, R5, R6, R7 (with the coupon set to `True` on the dash rows), and you would still have caught the defect. Using all 8 full rows is cheap in code and shows what the collapse hides. This style of writing tests as rows of data is called **table-driven** testing; it is a close cousin of data-driven testing, which we will study properly on Friday. For now, remember only the idea: one piece of test logic, many rows of data.

### 19. Common Mistakes

1. **Counting rules wrongly.** Forgetting that n conditions give 2^n combinations (or, for extended entries, the product of the value counts). Always do the arithmetic first and again at the end.
2. **Filling combinations at random.** Producing duplicates and gaps. Use the halving pattern.
3. **Merging rules that look similar but have different actions.** A dash is only valid when the outcome is genuinely the same for both values.
4. **Merging when you are unsure.** Do not collapse on a hunch; confirm the business rule.
5. **Marking a rule impossible just because it is awkward to test.** Only mark it infeasible when the business or the design prevents it. A rare but possible combination is often where the defects are.
6. **Hiding contradictions.** Two overlapping rules with different actions need resolving with the business, not silent picking.
7. **Ignoring the "otherwise" rule.** The default case is a rule too, and must be tested.
8. **Quoting coverage without saying which table.** "100% coverage" of a 5-rule table is not the same as 100% of the 8-rule table.
9. **Using decision tables for everything.** If the outcome depends on one field, use EP/BVA. If it depends on history, use states.
10. **Treating conditions as vague.** "Good credit" must be defined precisely ("score of 700 or above") or it cannot be tested. Define conditions as clear yes/no questions or discrete values.
11. **Forgetting the data.** A rule says "password is not strong"; you still need to choose which weak password to enter. Use EP and BVA for the values.
12. **Skipping the review.** A table never reviewed by the business might perfectly encode the wrong rules.
13. **Overloading one table.** Mixing unrelated conditions into a single huge table instead of splitting.

---

## Examples

All four worked examples (login, discount, loan eligibility and registration), the don't-care collapse demonstration, the requirement-text translation of the shipping sentence and the complete Python demo appear in the sections above, each with the table, a completeness check and test cases. Return to them whenever you build your own table.

For your reference, here is a summary of how much each example reduced:

| Example | Conditions | Full rules | Infeasible | Collapsed rules |
|---|---|---|---|---|
| Collapse demonstration (login, locked first) | 3 Boolean | 8 | 0 | 5 |
| Worked Example 1 (login with impossible combos) | 3 Boolean | 8 | 3 | 3 |
| Worked Example 2 (discount) | 3 Boolean | 8 | 0 | 6 |
| Worked Example 3 (loan, extended entry) | 3 conditions with 3 values each | 27 | 0 | 11 |
| Worked Example 4 (registration, first error only) | 4 Boolean | 16 | 0 | 5 |
| Shipping sentence (or / unless) | 3 Boolean | 8 | 0 | 4 |

---

## Practice Exercises

Try each exercise on your own before looking at the answer key. For each one: (a) list conditions and actions, (b) compute the full number of rules, (c) build the full table, (d) collapse it, (e) check completeness, and (f) list the test cases.

### Exercise 1: ATM Withdrawal

**Requirement.** A customer has already inserted their card. The ATM checks, in this order of priority: (1) if the PIN is wrong, show "Wrong PIN" and do nothing else; (2) otherwise, if the requested amount is more than the account balance, show "Insufficient funds"; (3) otherwise, if the amount would exceed the $500 daily withdrawal limit, show "Daily limit exceeded"; (4) otherwise dispense the cash.

**Answer key.**

Conditions: P = PIN correct; B = balance sufficient; L = within daily limit. Actions: Dispense cash; Wrong PIN; Insufficient funds; Limit exceeded. n = 3 so 2^3 = 8 rules.

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| P: PIN correct? | T | T | T | T | F | F | F | F |
| B: Balance sufficient? | T | T | F | F | T | T | F | F |
| L: Within daily limit? | T | F | T | F | T | F | T | F |
| **Dispense cash** | X | | | | | | | |
| **Limit exceeded** | | X | | | | | | |
| **Insufficient funds** | | | X | X | | | | |
| **Wrong PIN** | | | | | X | X | X | X |

Collapsed (4 rules): R1 (F, -, -) Wrong PIN, covering 4; R2 (T, F, -) Insufficient funds, covering 2; R3 (T, T, F) Limit exceeded, covering 1; R4 (T, T, T) Dispense cash, covering 1. 4 + 2 + 1 + 1 = 8. Complete.

Test cases: (1) wrong PIN, any amount, expect "Wrong PIN" and no cash; (2) correct PIN, balance $100, request $200, expect "Insufficient funds"; (3) correct PIN, balance $1,000, request $600, expect "Daily limit exceeded"; (4) correct PIN, balance $1,000, request $100, expect cash dispensed. BVA additions: request exactly $500 (allowed) and $500.01... (ATMs dispense in whole notes so use $20 steps such as $500 and $520), and a request exactly equal to the balance. Gap spotted: the requirement does not say what happens when the balance is insufficient and the limit would also be exceeded; we assumed "Insufficient funds" wins. Also, "card is retained after three wrong PINs" needs a state model (next lesson).

### Exercise 2: Hotel Booking Cancellation Fee

**Requirement.** A hotel has two rate types: Flexible and Non-refundable. For a Flexible booking: cancelling more than 7 days before check-in is free; cancelling 2 to 7 days before costs 50% of the first night; cancelling less than 2 days before costs 100% of the first night. For a Non-refundable booking, any cancellation costs 100% of the whole stay.

**Answer key.**

Extended entry. Conditions: Rate type (2 values), Notice period (3 values: more than 7 days, 2-7 days, less than 2 days). Full table: 2 x 3 = **6 rules**.

| Rule | Rate type | Notice | Cancellation fee |
|---|---|---|---|
| R1 | Flexible | More than 7 days | $0 |
| R2 | Flexible | 2-7 days | 50% of first night |
| R3 | Flexible | Less than 2 days | 100% of first night |
| R4 | Non-refundable | More than 7 days | 100% of the stay |
| R5 | Non-refundable | 2-7 days | 100% of the stay |
| R6 | Non-refundable | Less than 2 days | 100% of the stay |

Collapsed (4 rules): R4, R5, R6 have the same action and differ only in notice, so merge into (Non-refundable, -) = 100% of the stay, covering 3. 1 + 1 + 1 + 3 = 6. Complete.

Test cases: (1) Flexible, cancel 14 days ahead, fee $0; (2) Flexible, 5 days ahead, 50% of night 1; (3) Flexible, 1 day ahead, 100% of night 1; (4) Non-refundable, any notice (try 14 days and perhaps 1 day), 100% of the stay. BVA additions: Flexible at 8, 7, 2 and 1 days. Questions for the business: does "7 days" mean 7 full 24-hour days? In which time zone is check-in measured? What happens on a cancellation after the check-in date (no-show)?

### Exercise 3: Cinema Ticket Pricing

**Requirement.** Child (under 12) tickets are $8 at any time. Senior (65 and over) tickets are $9 at any time. Adult tickets (12 to 64) cost $11 for matinee shows. For evening shows, adults pay $15, or $12 with a valid student ID.

**Answer key.**

Conditions: Age group (3 values: Child, Adult, Senior), Matinee show? (2), Student ID? (2). Full table: 3 x 2 x 2 = **12 rules**.

Collapsed (5 rules):

| Rule | Age group | Matinee? | Student ID? | Ticket price | Original combinations covered |
|---|---|---|---|---|---|
| R1 | Child | - | - | $8 | 4 |
| R2 | Senior | - | - | $9 | 4 |
| R3 | Adult | Yes | - | $11 | 2 |
| R4 | Adult | No | Yes | $12 | 1 |
| R5 | Adult | No | No | $15 | 1 |
| **Total** | | | | | **12** |

4 + 4 + 2 + 1 + 1 = 12. Complete.

Test cases: Child at an evening show (expect $8; also try matinee), Senior (expect $9), Adult matinee without student ID (expect $11), Adult evening with student ID (expect $12), Adult evening no student ID (expect $15). BVA additions on age: 11 (child), 12 (adult), 64 (adult), 65 (senior). Gap spotted: does a student discount ever apply to a child or senior? The requirement says nothing; we assumed no. Also, what about age 0 (infants) and negative or unrealistic ages? (Error guessing.)

### Exercise 4: Library Fine

**Requirement.** A returned item attracts a fine only if it is overdue. The fine per day is: for books $0.50 for adults and $0.25 for children (under 12); for DVDs $1.00 for adults and $0.50 for children. Items returned on time have no fine.

**Answer key.**

Conditions: O = item overdue; D = item is a DVD (F means book); C = borrower is a child. n = 3, so 8 rules.

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| O: Overdue? | T | T | T | T | F | F | F | F |
| D: DVD? | T | T | F | F | T | T | F | F |
| C: Child? | T | F | T | F | T | F | T | F |
| **Fine per day** | $0.50 | $1.00 | $0.25 | $0.50 | $0 | $0 | $0 | $0 |

Collapsed (5 rules): R1 (T, T, T) $0.50; R2 (T, T, F) $1.00; R3 (T, F, T) $0.25; R4 (T, F, F) $0.50; R5 (F, -, -) $0, covering 4. 1 + 1 + 1 + 1 + 4 = 8. Complete.

Test cases: DVD, child, overdue: $0.50/day; DVD, adult, overdue: $1.00/day; book, child, overdue: $0.25/day; book, adult, overdue: $0.50/day; any item returned on time: $0. Watch out: R1 and R4 give the same fine ($0.50) but are different rules; they do not merge because the conditions differ in two positions. BVA: returned exactly on the due date (not overdue) versus one day late; and a child aged 11 versus 12. Gap: is there a maximum fine (for example, the price of the item)? Not in the requirement.

### Exercise 5: Password Reset Eligibility

**Requirement.** When a user requests a password reset: if no account exists for the email, show the neutral message "If an account exists, we have sent an email" and send nothing. If the account exists but is suspended, show "Please contact support". If the account is active but the email address has not been verified, show "Please verify your email first". If the account is active and verified but a reset link was already sent in the last 15 minutes, show "Please wait before requesting another link". Otherwise, send the reset link.

**Answer key.**

Conditions: A = account exists; S = account suspended; V = email verified; R = reset already requested in the last 15 minutes. n = 4, so 2^4 = **16 rules**. Because the requirement is a priority chain, the collapsed table follows it directly:

| Rule | A | S | V | R | Action | Original combinations covered |
|---|---|---|---|---|---|---|
| R1 | F | - | - | - | Neutral message; nothing sent | 8 |
| R2 | T | T | - | - | "Contact support" | 4 |
| R3 | T | F | F | - | "Verify your email first" | 2 |
| R4 | T | F | T | T | "Please wait" | 1 |
| R5 | T | F | T | F | Send reset link | 1 |
| **Total** | | | | | | **16** |

8 + 4 + 2 + 1 + 1 = 16. Complete. (Several of the 16 are arguably infeasible, for example a non-existent account that is suspended; collapsing with dashes handles them without extra work.)

Test cases: unknown email; suspended account; unverified active account; verified account that just requested a link; verified account with no recent request (expect the email). Extra tests: R1 must give a message identical to a genuine request (to avoid revealing whether accounts exist), and a time-boundary test for the 15-minute window (14 minutes 59 seconds versus 15 minutes 01 seconds). Gap: does a suspended account's status take priority over a recent request? The chain says so; confirm with the business.

### Exercise 6: Shipping Charge

**Requirement.** Domestic standard shipping is free for orders of $50 or more and $5 otherwise. Domestic express shipping costs $12 regardless of the order total. International standard shipping costs $25 and international express costs $40, regardless of the order total.

**Answer key.**

Conditions: Destination (2 values: Domestic, International); Order total $50 or more? (2); Express? (2). Full table: 2 x 2 x 2 = **8 rules**.

| Rule | Destination | Total $50 or more? | Express? | Shipping charge | Original combinations covered |
|---|---|---|---|---|---|
| R1 | Domestic | Yes | No | $0 | 1 |
| R2 | Domestic | No | No | $5 | 1 |
| R3 | Domestic | - | Yes | $12 | 2 |
| R4 | International | - | No | $25 | 2 |
| R5 | International | - | Yes | $40 | 2 |
| **Total** | | | | | **8** |

1 + 1 + 2 + 2 + 2 = 8. Complete. Collapsed to 5 rules.

Test cases: Domestic, $80, standard: $0; Domestic, $30, standard: $5; Domestic express (try both $30 and $80): $12; International standard (try $30 and $80): $25; International express: $40. BVA additions: totals of $49.99, $50.00 and $50.01 for the domestic standard rules. Notice that "$50 or more" includes $50.00, unlike "over $100" in the earlier example, so the boundary values behave differently: read each requirement's wording carefully.

---

## Knowledge Check

Answer in your own words first, then check the key below.

1. Why can BVA and EP alone miss defects in business rules like discount eligibility?
2. A table has 5 Boolean conditions. How many rules are in the full table?
3. An extended-entry table has conditions with 4, 3 and 2 possible values. How many rules are in the full table?
4. In a decision table, what does a dash ("-") in a condition cell mean, and when is it safe to use?
5. Write the T/F pattern for the first, second and third rows of a 3-condition table, left to right (8 columns).
6. A collapsed table has rules that cover 4, 2, 1 and 1 original combinations. How many conditions does the original table have (assuming Boolean) and is it complete?
7. You run 4 tests that exercise 4 different rules of a simplified table that has 6 rules. What is the decision table coverage?
8. Why do we mark a combination "infeasible", and what must we do before marking it?
9. In a requirement, what does the word "unless" signal when you build the table, and what does "otherwise" become?
10. What two kinds of problems does a completeness check and a consistency check detect?
11. Name two reasons a large decision table becomes hard to use, and two strategies to deal with it.
12. A requirement says "A user may edit if they own the record or are an administrator." Build a 4-rule full table and collapse it.
13. When should you prefer a state transition approach over a decision table?
14. In the Python demo, why did rows R3, R7 and B1 fail while R1 and R5 passed?
15. What is the relationship between decision tables and BVA when a condition is "order total over $100"?

**Answer key**

1. Because EP and BVA choose values for one field at a time. Defects often arise only for a specific combination of conditions (for example a coupon applied to a small order); testing each field separately never produces that combination.
2. 2^5 = 32 rules.
3. 4 x 3 x 2 = 24 rules.
4. "Don't care": the value of that condition does not change the outcome for that rule, so it can be T or F. It is safe only when the requirement confirms the outcome is the same for both values (identical actions) and the rest of the rule is unchanged.
5. Row 1: T T T T F F F F. Row 2: T T F F T T F F. Row 3: T F T F T F T F.
6. 4 + 2 + 1 + 1 = 8 = 2^3, so there are 3 Boolean conditions, and the table is complete (assuming no overlaps).
7. 4 / 6 x 100 = 66.7% of the simplified table.
8. A combination is infeasible when it cannot occur because of the business rules or the system design (for example, a locked state for a username that does not exist). Before marking it, confirm that it truly cannot occur and write the reason down; if it can occur, it is a valid rule that needs an expected result.
9. "Unless" means "if not": the condition that follows must be false for the main action to apply, and its true case triggers the exception. "Otherwise" becomes the default rule covering all combinations not handled by the preceding rules.
10. Completeness finds missing combinations (gaps: nothing says what should happen). Consistency finds contradictions (overlapping rules that give different, incompatible actions).
11. Combination explosion (2^n growth) and loss of readability or maintainability. Strategies: collapse with don't-cares, remove infeasible combinations, split into smaller tables, define derived conditions, prioritise by risk, or use a combinatorial technique such as pairwise testing.
12. Conditions: Owner (O), Administrator (A). Full table: R1 (T, T) edit allowed; R2 (T, F) edit allowed; R3 (F, T) edit allowed; R4 (F, F) edit denied. Collapsed to 3 rules: (T, -) allowed (covers 2), (F, T) allowed (covers 1), (F, F) denied (covers 1). 2 + 1 + 1 = 4.
13. When the outcome depends on history or a sequence of events (for example an account locks after three failed attempts) and the system moves between states. That is the topic of the next lesson.
14. They were the rows where a coupon was present but the order was not over $100. The buggy code added the coupon bonus without checking the order total. R1 and R5 had orders over $100, where adding the coupon was correct.
15. The decision table decides which combinations of conditions to test; BVA decides the values to use for a condition defined by a boundary. For "order total over $100", use $100.00 (not over) and $100.01 (over) as the two representatives, combined with the other conditions' values according to the rules.

---

## Try It: Pair Programming Activity (Project 1)

**Format:** Work in pairs. One person is the **Driver** (types and writes the table); the other is the **Navigator** (reads the requirement aloud, questions each decision and checks the counts). Swap roles halfway. Allow about 45 minutes, then cross-review with another pair.

**Your task.** Design tests for Project 1's User Registration and Login using **three techniques from today** (choose three from: use-case testing, BVA, EP, error guessing, decision tables). At least one of the three must be decision table testing, and both of the features below should be covered.

1. **Gather the rules.** Open Project 1 and read the on-screen behaviour and any requirement or acceptance criteria. Copy the exact registration validation rules into your notes. Highlight every "if / and / or / unless / otherwise" word.
2. **Registration table.** Build the decision table for registration with conditions E (email valid), P (password strong), T (terms accepted), U (username available). First write the full 16-rule table using the fill pattern. Then explore the real application to answer: does it show the first error only, or all errors at once? Adjust the actions accordingly. Collapse the table and run the completeness check (the covered counts must add up to 16).
3. **Login table.** Build the login table with U, P and L (locked) from Worked Example 1. Does Project 1 have a lock rule? If not, drop L and build a 4-rule table, or record "lock behaviour not specified" as a requirement gap.
4. **Test cases.** Convert every collapsed rule into a test case with ID, rule reference, test data and expected result. For the data in each condition, use EP (which classes of invalid email, weak password?) and BVA (minimum and maximum password length, username length limits).
5. **Execute and record.** Run your tests against Project 1. For each, record Pass/Fail and any defect you find, written up with the defect lifecycle format you learned on Tuesday (title, steps, expected, actual, severity).
6. **List the gaps.** Write at least three questions that the requirement does not answer (for example: are usernames case sensitive? What happens when two errors occur at once?).
7. **Cross-review.** Swap documents with another pair. Review their table using this checklist: Did they compute 2^n correctly? Do the covered counts total the right number? Are the infeasible rules justified? Are any dashes unsafe? Do any rules overlap? Does each rule have a test case? Write your comments and discuss them.
8. **Reflect (5 minutes).** Which defects or gaps did the decision table reveal that the single-field techniques did not?

**Success criteria:** a full table, a collapsed table with a completeness check, a test case per rule, a decision table coverage figure stated against a named table, and a list of requirement gaps.

---

## Key Takeaways

- Decision table testing is a black-box technique for **business rules where combinations of conditions determine the outcome**. EP and BVA test one field at a time and can miss combination defects.
- A table has **conditions** (inputs), **actions** (outputs), **rules** (columns), **condition entries** (T / F / -) and **action entries** (X or blank).
- **Limited-entry** tables use only T/F; **extended-entry** tables use multiple values per condition.
- The full table has **2^n** rules for n Boolean conditions, or the **product of the value counts** for extended entries. Fill the combinations with the halving pattern (blocks of 2^(n-1), 2^(n-2), ... 1).
- Mark **infeasible** combinations with reasons, merge rules with **don't-care** dashes only when actions are genuinely identical, and verify **completeness** (the covered counts add up to the full total) and **consistency** (no contradictions).
- Each rule becomes at least one **test case**; trace it back to the rule.
- **Coverage = rules exercised / total feasible rules x 100**, and always state which table (full or collapsed) the denominator comes from.
- Translating requirement text (if, and, or, unless, otherwise) into a table is a powerful way to find **ambiguities and gaps** before any code exists.
- Review tables with stakeholders in plain language; they make a shared source of truth.
- Use decision tables for combinations, state transitions for history and sequences; combine with BVA and EP for the data values.
- Tables can be turned into **table-driven tests** in code, and a single combination defect (coupon on a small order) is exactly what they catch.
- Manage large tables by collapsing, removing infeasible rules, splitting, layering conditions, prioritising by risk or using combinatorial methods such as pairwise testing.

---

## Additional Resources

- ISTQB Glossary and Foundation Level materials (definitions of decision table testing, cause-effect graphing, and coverage): https://glossary.istqb.org/ and https://www.istqb.org/
- Guru99, "Decision Table Testing: Learn with Example": https://www.guru99.com/decision-table-testing.html
- Ministry of Testing, articles and community discussion on test design techniques: https://www.ministryoftesting.com/
