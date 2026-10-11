# Black-Box Testing: Testing What the Software Does, Not How It Is Built

## Learning Objectives

By the end of this lesson, you will be able to:

- Define black-box (specification-based, behavioral) testing and explain the input -> system -> output model.
- Describe the benefits and limitations of black-box testing and say where it applies across test levels and test types.
- Explain what a test design technique is and why systematic techniques are needed, building on the principle that exhaustive testing is impossible.
- Describe the flow from test basis to test condition, test case, test data and expected result, and explain what a test oracle is.
- Name the three families of test design techniques (black-box, white-box, experience-based) and the six techniques taught today.
- Choose a suitable technique for a given feature and combine techniques in layers.
- Derive test cases step by step from a written specification.
- Explain requirements traceability and requirements coverage in black-box terms.
- Compare black-box, white-box and grey-box testing.
- Write simple black-box tests in Python (pytest style) from a specification alone.
- Use AI tools to suggest test ideas, and verify those ideas responsibly.

---

## Why This Matters

### In the industry

Every day, testers receive software they did not write. Often they cannot, or should not, read the code. A bank tester checking a new transfer screen, a mobile app tester checking a checkout flow, and a healthcare tester checking a dosage calculator all do the same thing: they look at what the software is *supposed* to do (the specification), give it inputs, and compare the outputs with what was promised. This is **black-box testing**, and it is the most widely used approach in professional testing. Most of the test cases you will write, review or automate in your career will be black-box test cases.

Employers also look for testers who can explain *why* they chose a particular set of tests. "I tested a bunch of values" is a weak answer. "I used equivalence partitioning to cover each class of input and boundary value analysis to probe the edges" is a strong one. Today's lessons give you that vocabulary and that discipline.

### In our Weekly Epic

This week you are building a quality-engineering mindset and applying it daily to **Project 1 - QE Foundations**, a sample web app with **User Registration** and **Login**. On Monday you learned where testing fits in the lifecycle. On Tuesday you learned to analyse requirements, plan, write test cases and report defects. On Wednesday you learned the mindset and the seven testing principles, including the uncomfortable truth that *exhaustive testing is impossible*.

Today answers the natural next question: **if we cannot test everything, how do we choose what to test?** The answer is test design techniques. This lesson is the umbrella for the day: it explains black-box testing and gives you a map of every technique. The following lessons then teach each technique in depth, and the day ends with a pair-programming exercise where you and a partner design tests for Project 1 using three techniques and cross-review each other's work.

---

## The Concept

### 1. What is black-box testing?

**Black-box testing** is a way of testing in which the tester examines the *behavior* of the software from the outside, using only its inputs and outputs, without looking at or relying on the internal code or structure. It is also called:

- **Specification-based testing**, because test cases come from the specification (requirements, user stories, acceptance criteria, design documents).
- **Behavioral testing**, because it checks the behavior the user can observe.

Some definitions to keep handy:

| Term | Meaning |
|---|---|
| **Input** | Anything given to the system: typed text, a clicked button, a file, an API request, a sensor reading. |
| **Output** | Anything the system produces in response: a message on screen, a changed record, a returned value, a sent email. |
| **Specification** | A written description of what the system should do. |
| **Behavior** | What the system visibly does in response to inputs. |
| **Internal structure** | The code, branches, loops, database queries and architecture inside the system. |

#### The vending machine analogy

Picture a vending machine. You do not know how the coins are counted, how the spiral turns, or what software runs inside. You only know the rules written on the front: "Insert the right amount, press B3, receive crisps."

As a tester you could try:

- Insert exactly the right amount, press B3: crisps drop out.
- Insert too little money, press B3: nothing drops and the machine asks for more.
- Press a button that does not exist.
- Insert a foreign coin.
- Insert too much money: you should get change.

You never opened the machine. You compared **what you did (inputs)** and **what happened (outputs)** with **what the sign promised (specification)**. That is black-box testing.

#### The black-box model

```
            +-----------------------------------+
            |                                   |
  INPUTS    |        THE SYSTEM UNDER TEST      |    OUTPUTS
  --------> |      (contents hidden: a "box"    | -------->
  email     |       that we cannot see inside)  |  "Welcome!" page
  password  |                                   |  error message
  click     |                                   |  database record
            +-----------------------------------+
                  ^                          |
                  |                          v
           Tester controls           Tester observes and
           these                     compares with the
                                     specification
```

The tester controls the left side and observes the right side. The tester's question is always: **"Given this input, does the system produce the output the specification says it should?"**

> Why "black" and not "see-through"? A black box is opaque: you cannot see inside. A see-through ("glass-box" or "white-box") approach lets you view the code. You will meet that on Friday.

### 2. Why use black-box testing?

**Benefits**

1. **It reflects the user's perspective.** Users do not care about your code; they care whether the app works. Black-box tests ask the same questions users ask.
2. **No programming knowledge is required to design tests.** A business analyst, a domain expert or a new tester can contribute. (You will use a little Python today to *automate* tests, but designing them needs only the spec.)
3. **It is independent of the implementation.** If developers rewrite the internals (new language, new framework) without changing behavior, the same black-box tests still apply.
4. **It is based on requirements.** Tests trace directly to what was promised, which is exactly what stakeholders want verified. This supports *validation*: are we building the right product?
5. **It supports independence.** The tester is not biased by knowing how the code was written, so assumptions made by the developer are less likely to be repeated by the tester.
6. **It can start early.** Test cases can be designed as soon as requirements exist, before the code is finished (remember "early testing" from Wednesday).

**Limitations**

1. **It cannot see untested code paths.** If the code contains a special branch the specification never mentions (for example, a hidden admin shortcut), black-box tests may never touch it.
2. **There is a risk of redundancy.** Without a systematic approach, testers may write ten tests that all exercise the same behavior and miss other behaviors. This is exactly why we need techniques.
3. **It depends on the quality of the specification.** If the requirements are vague, missing or wrong, the tests will be vague, missing or wrong too. "Garbage in, garbage out" applies. (Tuesday's requirements analysis skills matter here.)
4. **It is hard to know when you have tested enough** purely from the outside, so we use coverage measures based on the specification (covered later in this lesson).
5. **Finding the cause of a failure takes extra work.** A black-box test tells you *that* something is wrong, not *where* in the code.

### 3. Where black-box testing applies

#### Test levels

A **test level** is a group of test activities organised and managed together, usually tied to a stage of development. Black-box testing is used mainly at the higher levels but can appear at lower ones too.

| Test level | What is tested | How black-box fits |
|---|---|---|
| **Component (unit) testing** | A small piece such as a single function | Possible: you test the function's inputs and outputs from its specification, ignoring its code. (We do this in today's Python demo.) Developers often combine this with white-box tests. |
| **Integration testing** | Interactions between components or systems | Often black-box at the interface: send a request, check the response. |
| **System testing** | The whole system as one | The most common home of black-box testing. |
| **Acceptance testing** | Whether the system meets the business needs and is ready for use | Almost always black-box: users or customers check behavior against agreed criteria. |

#### Test types

A **test type** is a group of tests focused on a particular quality characteristic.

- **Functional testing** checks *what* the system does (features, calculations, rules). Black-box techniques fit this naturally.
- **Some non-functional testing** also uses black-box thinking, for example checking how long a page takes to respond or whether error messages are clear, without examining the code.

Friday's lesson covers functional versus non-functional testing in detail; for now, just remember that black-box describes *how you design the tests* (from the outside), while functional and non-functional describe *what quality you are checking*.

### 4. Test design techniques: the big idea

#### Why we need them

On Wednesday you learned the principle **"exhaustive testing is impossible."** Consider one innocent field in Project 1: a password of up to 20 characters from about 95 typeable characters. The number of possible passwords is astronomically large, far more than could ever be tried. Add the email field, the button and the browser, and the number of combinations is beyond counting.

So we must **choose a smart subset**: a small set of tests that gives us the best chance of finding defects and the most confidence in the software. Choosing randomly is unreliable. Choosing using a **test design technique** is systematic.

A **test design technique** is a defined procedure for deriving and selecting test cases. It tells you *how to turn a specification into a manageable, effective set of tests*.

Techniques give you:

- **Fewer tests** than guessing (less redundancy).
- **Better coverage** of the behaviors that matter.
- **Repeatability**: two testers using the same technique on the same spec produce similar results.
- **Justification**: you can explain and defend why those tests exist.

#### From idea to executable test: the flow

Test design is a chain of steps. Each step makes things more concrete:

```
  TEST BASIS  ->  TEST CONDITION  ->  TEST CASE  ->  TEST DATA  ->  EXPECTED RESULT
  (what the       (what could be      (a complete    (the actual    (what should
   spec says)      tested)             scenario)      values)        happen)
```

| Term | Definition | Project 1 example |
|---|---|---|
| **Test basis** | The documents or knowledge from which tests are derived: requirements, user stories, acceptance criteria, design documents. | "A password must be 8 to 20 characters." |
| **Test condition** | An item or event that could be verified by one or more test cases. | "Password length is accepted at the lower limit." |
| **Test case** | A set of preconditions, inputs, actions and expected results developed for a particular objective. | "Register with a password of exactly 8 characters." |
| **Test data** | The specific values used in the test. | Email `ana@example.com`, password `Abcdef1!` (8 characters). |
| **Expected result** | The outcome the specification says should occur. | "Account is created and a confirmation message appears." |

A **test oracle** is the source we trust to tell us the expected result: the specification, a requirement document, an existing system, a domain expert or a calculation we can verify by hand. Without an oracle, you cannot decide whether a test passed or failed. In black-box testing, the specification is usually the oracle. When the spec is silent or unclear, you must ask (a business analyst, product owner or developer) rather than guess.

> A quick reminder from Tuesday: a test case normally has an ID, title, preconditions, steps, test data, expected result and (after execution) actual result and status. We return to this shortly.

### 5. The three families of techniques

Test design techniques are usually grouped into three families:

| Family | Test cases are based on | Also called | When taught |
|---|---|---|---|
| **Black-box** | The specification: requirements, behavior, inputs and outputs | Specification-based, behavioral | Today (this lesson and the next four) |
| **White-box** | The internal structure: code statements, branches, paths | Structure-based | Friday (pointer only today) |
| **Experience-based** | The tester's knowledge, skill, intuition and past defects | Experience-based | Error guessing today; exploratory testing on Friday |

They are not rivals. Good testers use all three, the way a doctor uses lab tests (systematic), an examination of the body (structural) and clinical experience (intuition) together.

### 6. Overview of today's techniques

Below is a map of the six techniques you will study today. **Each is only introduced here.** Every one has its own full lesson that teaches it properly.

| Technique | One-line definition | Best used for | Tiny example |
|---|---|---|---|
| **Equivalence Partitioning (EP)** | Divide inputs into groups that the system should treat the same way, then test one value from each group. | Any input with ranges or categories | Age valid 18-60: test one age from "too young", "valid", "too old". |
| **Boundary Value Analysis (BVA)** | Test values at and next to the edges of ranges, where defects like to hide. | Numeric ranges, lengths, dates, limits | Age 18-60: try 17, 18, 60, 61. |
| **Decision Table testing** | List combinations of conditions in a table and the action each combination should cause. | Business rules with several conditions | Login: valid email? valid password? account locked? -> what happens. |
| **State Transition testing** | Model the system as states and events that move it between states, then test the transitions. | Workflows and things whose behavior depends on history | Account: Active -> Locked after 3 failed logins -> Active after reset. |
| **Use-case testing** | Derive tests from user scenarios: a main success path and alternative or failure paths. | End-to-end user journeys, acceptance tests | "New user registers, confirms email, logs in." |
| **Error Guessing** (experience-based) | Use experience to guess where defects are likely and design tests to expose them. | Supplementing systematic tests; finding unusual defects | Try an email with spaces, emoji or 300 characters. |

A little more about each, kept deliberately short.

**Equivalence Partitioning.** Imagine a school that gives the same grade to all marks from 50 to 59. Testing 50, 51, 52 ... 59 tells you little more than testing one of them. EP applies this idea to inputs: values in the same partition (group) should be handled identically, so one representative value per group is enough. This is the main weapon against redundancy. *See the Equivalence Partitioning lesson for the full method.*

**Boundary Value Analysis.** Developers often make "off by one" errors, writing `>` where `>=` was meant. These errors live at the edges of ranges. BVA tests the edge values and their neighbors. It pairs naturally with EP. *See the Boundary Value Analysis lesson.*

**Decision Table testing.** When the outcome depends on a *combination* of conditions, a table keeps the combinations organised so none is forgotten. For example, a discount that depends on membership *and* order size. *See the Decision Table lesson.*

**State Transition testing.** Some systems behave differently depending on what has already happened. A login form that locks after three failures is one: the same wrong password has a different result the first time and the third time. *See the State Transition lesson.*

**Use-case testing.** Instead of testing fields in isolation, you follow what a user is trying to accomplish from start to finish, including what happens when things go wrong along the way. *See the Use-Case testing lesson.*

**Error Guessing.** Experienced testers know that certain mistakes recur: empty fields, very long text, special characters, double-clicks, expired sessions. Error guessing turns that memory into tests. It is not random: it is informed. *See the Error Guessing lesson. Exploratory testing, a related experience-based approach, comes on Friday.*

### 7. How to choose a technique

No single technique finds every kind of defect. Choose based on the *nature of the feature*:

| If the feature involves... | Start with... | Add... |
|---|---|---|
| A single input with a range or categories (age, quantity, password length) | Equivalence Partitioning | Boundary Value Analysis |
| Numeric limits or length limits | Boundary Value Analysis | Equivalence Partitioning |
| Several conditions combining into different outcomes (discount rules, eligibility) | Decision Table testing | EP for each condition's values |
| Behavior that depends on history or status (lock-out, order status, session) | State Transition testing | Decision tables for rules at each state |
| A complete user journey (register, then log in, then buy) | Use-case testing | EP/BVA on the fields along the way |
| A spec that is thin, or a high-risk area with a history of defects | Error Guessing | Any systematic technique |
| Time pressure and a need for a fast safety net | Use-case testing for main flows, then EP | Error guessing for quick extra probes |

Other things that influence the choice: the **risk** of the feature (higher risk deserves more techniques), the **type of defects** you expect, the **documentation available**, the **time and budget**, and the **tester's skill**. If in doubt, start with EP and BVA: they are the most broadly useful.

### 8. Combining techniques: the layered approach

Real features are rarely simple, so testers **layer** techniques. Think of painting a wall: you do the broad coat first, then the details.

```
  Layer 1: Use-case testing       -> the user journeys (big picture)
  Layer 2: State / Decision table -> the rules and statuses behind the journey
  Layer 3: EP and BVA             -> the fields and values inside each step
  Layer 4: Error guessing         -> extra probes from experience
```

#### Worked example outline: Project 1 Login and Registration

**Step 1: List the requirements** (simplified for this example)

| ID | Requirement |
|---|---|
| REG-01 | A visitor can register with an email and a password. |
| REG-02 | The email must be in a valid format and not already registered. |
| REG-03 | The password must be 8 to 20 characters and include at least one digit. |
| LOG-01 | A registered user can log in with the correct email and password. |
| LOG-02 | Login fails with a generic error message for an incorrect email or password. |
| LOG-03 | After 3 consecutive failed login attempts, the account is locked. |

**Step 2: Choose techniques**

| Requirement | Technique chosen | Reason |
|---|---|---|
| REG-03 (password length and digit) | EP + BVA | Range of lengths and a category rule |
| REG-02 (email format, duplicates) | EP (valid/invalid/duplicate) | Categories of input |
| LOG-01, LOG-02 (outcome depends on email and password correctness) | Decision table | Combination of two conditions |
| LOG-03 (lock after 3 failures) | State transition | Behavior depends on history |
| REG-01 followed by LOG-01 | Use-case testing | The full journey |
| All fields | Error guessing | Extra probes (spaces, long text, special characters) |

**Step 3: A small combined set of tests** (outlines only; the dedicated lessons show how to derive these fully)

| Test ID | Technique | Test idea | Expected result |
|---|---|---|---|
| TC-01 | Use-case | Register with a valid email and password, then log in | Account created; login succeeds |
| TC-02 | EP | Register with a password of 12 characters including a digit | Accepted |
| TC-03 | EP | Register with a password of 12 letters, no digit | Rejected with a message about digits |
| TC-04 | BVA | Register with a password of exactly 8 characters | Accepted |
| TC-05 | BVA | Register with a password of 7 characters | Rejected |
| TC-06 | BVA | Register with a password of 21 characters | Rejected |
| TC-07 | Decision table | Valid email, wrong password | Generic error shown |
| TC-08 | Decision table | Unregistered email, any password | Same generic error shown (no hint about which part is wrong) |
| TC-09 | State transition | Three wrong passwords in a row, then the right one | Account locked; correct password now refused |
| TC-10 | Error guessing | Register with an email containing leading spaces | Handled sensibly: trimmed or rejected with a clear message |

Ten tests, five techniques, every requirement touched. This is far better than ten tests chosen at random.

### 9. Deriving test cases from a specification, step by step

Let us walk through the process with a very simple specification. We are illustrating the *process* only; the formal techniques come in their own lessons.

**Specification:** *"The age field accepts whole numbers from 18 to 60 inclusive. Any other value is rejected with the message 'Invalid age'."*

**Step 1: Read and understand the specification.** Underline the rules: whole numbers, 18 to 60, *inclusive* (so 18 and 60 are allowed), everything else rejected, a specific message.

**Step 2: Ask clarifying questions.** What about empty input? Decimals such as 25.5? Letters? The spec does not say. Note these as questions for the product owner. (Spotting gaps is a valuable result of test design.)

**Step 3: Identify test conditions.** What could we verify?
- Ages inside the range are accepted.
- Ages below the range are rejected.
- Ages above the range are rejected.
- The edges of the range behave as stated.
- Non-numeric and non-whole input is handled.
- The error message text is correct.

**Step 4: Design test cases, one condition at a time, and select test data.**

| Condition | Test data | Why this value |
|---|---|---|
| Inside the range | 35 | A typical valid value |
| Lower edge | 18 | The spec says inclusive |
| Upper edge | 60 | The spec says inclusive |
| Just below | 17 | Closest invalid value below |
| Just above | 61 | Closest invalid value above |
| Far outside | -5 | A clearly wrong value |
| Wrong type | "abc" | Not a number |
| Not whole | 25.5 | Spec says whole numbers |

**Step 5: Define expected results** from the oracle (the spec). 35, 18 and 60 are accepted; the others are rejected with "Invalid age".

**Step 6: Review.** Is every sentence of the spec covered by at least one test? Are there tests that duplicate each other? Are the questions from Step 2 logged?

**Step 7: Document and execute.** Write the test cases in the agreed format, run them, record actual results and report any mismatch as a defect.

Notice that without naming techniques, you naturally picked "one typical value" and "values at the edges." Those instincts are exactly what Equivalence Partitioning and Boundary Value Analysis formalise.

### 10. Traceability and coverage in black-box terms

**Requirements traceability** is the ability to link each requirement to the test cases that verify it (and to any defects found). It is usually kept in a **traceability matrix**, a table with requirements on one axis and tests on the other.

| Requirement | TC-01 | TC-02 | TC-03 | TC-04 | TC-05 | TC-06 | TC-07 | TC-08 | TC-09 |
|---|---|---|---|---|---|---|---|---|---|
| REG-01 | X | | | | | | | | |
| REG-02 | | X | | | | | | | |
| REG-03 | | | X | X | X | X | | | |
| LOG-01 | X | | | | | | | | |
| LOG-02 | | | | | | | X | X | |
| LOG-03 | | | | | | | | | X |

Benefits:

- **Finding gaps:** a requirement with an empty row has no test.
- **Finding orphans:** a test linked to no requirement may be unnecessary (or may reveal an undocumented requirement).
- **Impact analysis:** when a requirement changes, you instantly see which tests to update.
- **Reporting:** you can show stakeholders exactly what has been verified.

**Coverage** measures how much of something your tests have exercised. In black-box testing, coverage is measured against the *specification*, not the code.

**Requirements coverage** = (number of requirements with at least one test / total number of requirements) x 100%.

Simple example: Project 1 has 6 requirements above, and all 6 have at least one test, so requirements coverage is 6/6 = 100%. If LOG-03 had no test, coverage would be 5/6, about 83%.

Two warnings:

1. **100% requirements coverage does not mean no defects.** It means each requirement was *touched*, not that it was tested deeply. One test per requirement is a start, not an end.
2. **Technique-specific coverage** gives finer measures. For example, "every partition covered at least once" or "every decision-table column tested." Each technique lesson shows its own coverage measure.

### 11. Documenting black-box test cases (recap from Tuesday)

A well-written test case lets anyone execute it the same way. A standard structure:

| Field | Purpose | Example |
|---|---|---|
| **Test Case ID** | Unique reference | TC-REG-04 |
| **Title** | Short summary | Register with 8-character password (lower limit) |
| **Requirement ID** | Traceability link | REG-03 |
| **Technique** | (Optional but useful) how it was designed | BVA |
| **Preconditions** | State before the test | Registration page is open; email not yet registered |
| **Test steps** | Numbered actions | 1. Enter `ana@example.com`. 2. Enter `Abcdef1!`. 3. Click Register. |
| **Test data** | Values used | Email `ana@example.com`, password `Abcdef1!` |
| **Expected result** | What the spec requires | Account created; confirmation message shown |
| **Actual result** | What really happened (after execution) | (filled in later) |
| **Status** | Pass / Fail / Blocked | (filled in later) |

Good practice: one clear objective per test case, unambiguous steps, expected results taken from the spec (not from what the software happens to do), and recording which technique produced the test so reviewers can judge it.

### 12. Black-box versus white-box (brief)

You will learn white-box testing on Friday. Here is a quick comparison so that you understand where black-box sits.

| Aspect | Black-box | White-box |
|---|---|---|
| **Based on** | Specification and behavior | Code and internal structure |
| **Tester needs** | Domain and spec knowledge | Programming knowledge |
| **Question asked** | "Does it do what it should?" | "Have we exercised the code paths?" |
| **Typical levels** | System, acceptance (also component, integration) | Mainly component and integration |
| **Typically performed by** | Testers, users, analysts | Developers and technical testers |
| **Finds** | Missing or wrong behavior, spec mismatches | Dead code, untested branches, logic errors |
| **Misses** | Code the spec never mentions | Missing requirements (code can be perfect and still do the wrong thing) |
| **Example** | Check that a valid login succeeds | Ensure every `if` branch in the login code has run |

They complement each other: black-box asks whether we built the right thing; white-box asks whether we exercised everything we built.

### 13. Grey-box testing

**Grey-box testing** combines both views: the tester designs tests from the outside, as in black-box testing, but has *partial* knowledge of the internals, such as the database structure, the API design or the architecture. For example, a tester who knows that Project 1 stores registrations in a particular database table can register a user through the screen (black-box) and then check the database record (using internal knowledge) to confirm the data was saved correctly. Grey-box testing is common in web and API testing, where seeing a little of the inside makes tests sharper without requiring full code analysis.

### 14. Black-box testing in Agile, and with AI tools

#### In Agile teams

In Scrum, requirements arrive as **user stories** with **acceptance criteria**. These are a perfect test basis for black-box testing:

- **Story:** "As a visitor, I want to register so that I can access my account."
- **Acceptance criteria:** "Password must be 8-20 characters", "Duplicate emails are rejected," and so on.

Testers join backlog refinement to ask clarifying questions *before* development (early testing), derive tests directly from acceptance criteria, and run black-box regression tests every sprint because the software changes constantly. Because black-box tests do not depend on the internals, they survive refactoring well, which suits frequent change. Teams often turn the acceptance criteria into automated checks that run on every build.

#### With AI tools

Generative AI assistants can speed up the *idea* stage of black-box design. You can paste in a specification and ask for:

- Candidate test conditions and test cases.
- Suggested partitions and boundary values.
- Negative scenarios and edge cases you may have missed.
- Draft test data (for example, 20 invalid email formats).
- A first draft of an automated test in Python.

A helpful prompt pattern: *"Here is the requirement: [paste]. List test conditions using equivalence partitioning and boundary value analysis. Give each test an ID, input, and expected result. List any ambiguities in the requirement."*

**Cautions. AI is an assistant, not an oracle.**

1. **Verify every expected result against the real specification.** AI may invent rules the spec does not contain (for example, assuming a maximum password length that was never stated).
2. **Check for gaps and duplicates.** AI may produce many similar tests and still miss an important one. Use your traceability matrix to check coverage.
3. **Do not paste confidential data** (real customer information or proprietary requirements) into tools your organisation has not approved.
4. **Apply your own judgment and technique knowledge.** You must be able to explain *why* each test exists. If you cannot, do not include it.
5. **Treat generated code as a draft.** Run it, read it, and confirm it really checks what you intended.

The better you understand the techniques, the better you can direct the AI and judge its answers. Today's lessons make you a more capable reviewer of AI output.

---

## Examples

### Example 1: A hands-on Python demo, treating a function as a black box

In this demo, a developer has written a function `validate_age(age)`. As the tester, you **are given only the specification**. You will not use the code to decide what to test.

**The specification (the only thing you may use):**

> `validate_age(age)` checks whether a person's age is acceptable for registration.
> - It returns `True` if `age` is a whole number from 18 to 60 inclusive.
> - It returns `False` if `age` is a whole number outside that range.
> - It raises a `TypeError` if `age` is not a whole number (for example text or a decimal).

#### Setup

Make sure Python 3 is installed, then install pytest:

```
pip install pytest
```

Create a folder (for example `blackbox_demo`) with two files.

**File 1: `age_validator.py`** (the developer's code; in real black-box testing you would pretend this is sealed)

```python
def validate_age(age):
    if isinstance(age, bool) or not isinstance(age, int):
        raise TypeError("age must be a whole number")
    return 18 <= age <= 60
```

Line by line:

- `def validate_age(age):` defines a function named `validate_age` that receives one input called `age`.
- `if isinstance(age, bool) or not isinstance(age, int):` checks the *type* of the input. In Python, `True` and `False` are technically integers too, so we exclude booleans explicitly; the second part is true when `age` is not an integer (text, decimal, and so on).
- `raise TypeError("age must be a whole number")` stops the function and signals an error with a message. This matches the spec's third rule.
- `return 18 <= age <= 60` evaluates to `True` when `age` is between 18 and 60 inclusive, and `False` otherwise. This matches the first two rules.

**File 2: `test_age_validator.py`** (your black-box tests, written from the specification only)

```python
import pytest
from age_validator import validate_age


def test_typical_age_is_accepted():
    assert validate_age(35) is True


def test_lowest_allowed_age_is_accepted():
    assert validate_age(18) is True


def test_highest_allowed_age_is_accepted():
    assert validate_age(60) is True


def test_age_just_below_range_is_rejected():
    assert validate_age(17) is False


def test_age_just_above_range_is_rejected():
    assert validate_age(61) is False


def test_negative_age_is_rejected():
    assert validate_age(-5) is False


def test_text_input_raises_type_error():
    with pytest.raises(TypeError):
        validate_age("thirty")


def test_decimal_input_raises_type_error():
    with pytest.raises(TypeError):
        validate_age(25.5)
```

Explanation of every line:

- `import pytest` loads the pytest library, which we need for `pytest.raises`.
- `from age_validator import validate_age` brings in the function under test. Notice that this is the *only* connection to the developer's code: we call it and observe results, like pressing the buttons on the vending machine.
- Two blank lines between functions are a Python style convention (PEP 8); they do not affect behavior.
- `def test_...():` pytest automatically discovers and runs any function whose name starts with `test_`. Each one is one test case. The long, descriptive names act as documentation: they state the condition and the expected outcome.
- `assert validate_age(35) is True` is the heart of a test. `validate_age(35)` is the **input and action**; `is True` is the **expected result**; `assert` makes the test fail if the actual result does not match. Our oracle is the spec: 35 is within 18-60, so `True`.
- The tests for 18 and 60 check that the range is *inclusive*, as the spec says.
- The tests for 17 and 61 check the nearest values outside the range.
- `-5` is a clearly invalid value, checking that negative numbers do not slip through.
- `with pytest.raises(TypeError):` says "the code inside this block *must* raise a `TypeError`; if it does not, fail the test." We use it for the third spec rule. `"thirty"` is text; `25.5` is a decimal.

Each test traces to a sentence of the specification:

| Spec statement | Tests that cover it |
|---|---|
| Returns `True` for whole numbers 18 to 60 inclusive | typical (35), lowest (18), highest (60) |
| Returns `False` for whole numbers outside the range | 17, 61, -5 |
| Raises `TypeError` for non-whole numbers | "thirty", 25.5 |

#### Running the tests

From inside the folder, run:

```
python -m pytest -v test_age_validator.py
```

Expected output (version numbers and timing will differ on your machine):

```
collected 8 items

test_age_validator.py::test_typical_age_is_accepted PASSED               [ 12%]
test_age_validator.py::test_lowest_allowed_age_is_accepted PASSED        [ 25%]
test_age_validator.py::test_highest_allowed_age_is_accepted PASSED       [ 37%]
test_age_validator.py::test_age_just_below_range_is_rejected PASSED      [ 50%]
test_age_validator.py::test_age_just_above_range_is_rejected PASSED      [ 62%]
test_age_validator.py::test_negative_age_is_rejected PASSED              [ 75%]
test_age_validator.py::test_text_input_raises_type_error PASSED          [ 87%]
test_age_validator.py::test_decimal_input_raises_type_error PASSED       [100%]

============================== 8 passed in 0.02s ===============================
```

#### Seeing a test catch a defect

Now imagine a developer makes a small mistake. In `age_validator.py`, change the last line to:

```python
    return 18 < age <= 60
```

Run the tests again. The lower-edge test now fails:

```
FAILED test_age_validator.py::test_lowest_allowed_age_is_accepted - assert False is True
```

You found the defect *without reading the code*: the spec says 18 is valid, the system said `False`. A test written only from the specification caught an "off by one" error. This is the power of black-box testing, and it shows why testing the edges matters. (Restore the `<=` afterwards.)

Notice also what black-box testing cannot do here: if the code had a hidden rule such as "also reject age 42", only a test for 42 would reveal it, and you would never think to test 42 from the spec alone. That is the "untested code path" limitation, and it is why white-box and experience-based techniques exist.

### Example 2: Black-box test ideas for a Project 1 registration screen

Using only what a user sees:

| Input | Output expected by the spec |
|---|---|
| Valid email, valid password | "Registration successful" page |
| Email missing the @ symbol | Error beside the email field |
| Email already registered | "Email already in use" message |
| Password of 5 characters | Error: password too short |
| Empty form submitted | Errors on required fields |

No code was needed to think of these.

---

## Try It Yourself

### Activity: Map the techniques onto Project 1

Time: about 20 minutes. Work alone first, then compare with a neighbor.

1. Open Project 1 (or its requirements) and find the **User Registration** and **Login** features.
2. Write down five requirements in the style used earlier (for example, "Password must be 8-20 characters"). Give each an ID.
3. For each requirement, choose the most suitable technique from the decision guide and write one sentence explaining why.
4. Write two test ideas per requirement, with input data and expected result, taken from the specification.
5. Build a small traceability matrix showing which test covers which requirement and calculate your requirements coverage.
6. Find at least two points where the requirements are unclear and write them as questions for a product owner.
7. Ask an AI assistant to suggest additional test ideas for the same requirements. Compare with yours, mark which suggestions are valid, which are wrong and which are duplicates.

### Practice Exercise: Discount calculator

**Specification:**

> An online shop applies a discount to the order total.
> - Orders under 50.00 receive no discount.
> - Orders from 50.00 up to and including 200.00 receive a 10% discount.
> - Orders over 200.00 receive a 20% discount.
> - Members receive an extra 5% off the discounted price.
> - The order total must be greater than zero; otherwise the order is rejected with the message "Invalid total".

**Task:** Using only the specification, write black-box test ideas (input, expected result and the reasoning). Aim for 10 to 12 ideas. Also list any ambiguities you find.

**Sample answer:**

| # | Input (total, member?) | Expected result | Reasoning |
|---|---|---|---|
| 1 | 30.00, no | No discount: 30.00 | Typical value in the "no discount" band |
| 2 | 49.99, no | No discount: 49.99 | Just below the first threshold |
| 3 | 50.00, no | 10% off: 45.00 | Lower edge of the 10% band (inclusive) |
| 4 | 100.00, no | 90.00 | Typical value in the middle band |
| 5 | 200.00, no | 180.00 | Upper edge of the 10% band (inclusive) |
| 6 | 200.01, no | About 160.01 (20% off) | Just above the upper edge |
| 7 | 500.00, no | 400.00 | Typical value in the top band |
| 8 | 100.00, yes | 85.50 (10% off gives 90.00, then 5% off that gives 85.50) | Tests the member rule combined with a band |
| 9 | 30.00, yes | 28.50 | Member discount applies even when there is no order discount (if the spec means this; see ambiguities) |
| 10 | 0.00, no | Rejected: "Invalid total" | Boundary of the "greater than zero" rule |
| 11 | -10.00, no | Rejected: "Invalid total" | Clearly invalid value |
| 12 | 0.01, no | Accepted, no discount | Smallest valid amount |

**Ambiguities to raise:**

- Is the 5% member discount taken off the *discounted price* (as written) or the original total? The spec says discounted price, but confirm.
- Does the member discount apply when the order itself earns no discount (test 9)?
- How should results be rounded (to the nearest cent)?
- What about non-numeric input such as text?

Which techniques were hiding in your ideas? Ideas 1, 4, 7 reflect *partitions*; ideas 2, 3, 5, 6, 10, 12 reflect *boundaries*; ideas 8 and 9 reflect *combinations* that a decision table would organise. The following lessons teach each in detail.

---

## Common Mistakes

| Mistake | Why it is a problem | Better approach |
|---|---|---|
| Designing tests from what the software *does* instead of what the *spec says* | You would "confirm" defects as correct behavior | Always take expected results from the specification or another trusted oracle |
| Testing only valid inputs | Misses error handling, where many defects live (recall positive and negative testing) | Include invalid, empty and unusual inputs |
| Writing many tests for the same behavior | Wastes time, gives false confidence | Use techniques to remove redundancy |
| Skipping edges of ranges | Off-by-one defects are very common | Always test limits and their neighbors |
| Assuming 100% requirements coverage means "done" | Coverage counts touched requirements, not depth | Use techniques and risk to deepen important areas |
| Guessing when the spec is unclear | The test may be wrong | Ask questions and document assumptions |
| Relying on only one technique | Each technique has blind spots | Combine techniques in layers |
| Trusting AI-generated tests without checking | AI can invent rules and miss gaps | Verify against the spec and your matrix |
| No traceability | Cannot show what has been verified | Link every test to a requirement |
| Vague expected results ("works fine") | Cannot decide pass or fail | State precise, observable outcomes |

---

## Day 4 Roadmap

Today's lessons build on each other. This lesson is the map; each following lesson teaches one technique in depth.

```
  1. Black-box testing (this lesson)   The umbrella: concepts, flow, families, map
            |
            v
  2. Equivalence Partitioning          Group inputs; one value per group
            |
            v
  3. Boundary Value Analysis           Probe the edges of those groups
            |
            v
  4. Decision Table testing            Combinations of conditions and rules
            |
            v
  5. State Transition testing          Behavior that depends on history
            |
            v
  6. Use-case testing                  Whole user journeys, end to end
            |
            v
  7. Error Guessing                    Experience-based extra probes
            |
            v
  PAIR PROGRAMMING EXERCISE            You and a partner design tests for Project 1
                                       using three techniques, then cross-review
```

Why this order? EP and BVA work on single inputs, so they come first and go together. Decision tables handle several inputs at once. State transitions add the dimension of time and history. Use-case testing zooms out to the whole journey, and error guessing adds human experience on top. By the time you reach the pair-programming exercise, you will have the full toolkit and will choose three techniques to apply, reviewing your partner's work as a critical friend.

Tomorrow (Friday) you will meet white-box techniques, exploratory testing and the difference between functional and non-functional testing, completing the picture of the three families.

---

## Knowledge Check

**Questions**

1. In your own words, what is black-box testing, and what does the tester *not* see?
2. Name two other terms for black-box testing.
3. List three benefits and two limitations of black-box testing.
4. Why does "exhaustive testing is impossible" lead us to use test design techniques?
5. Put these in order: test case, test basis, expected result, test condition, test data.
6. What is a test oracle? What is usually the oracle in black-box testing?
7. Name the three families of test design techniques and say which is covered by today's lessons.
8. Which technique would you start with for a lock-out after three failed logins? Why?
9. A project has 12 requirements and tests exist for 9 of them. What is the requirements coverage?
10. What is grey-box testing? Give an example.
11. Why can a black-box test miss a defect that sits in code the specification never mentions?
12. Give two cautions when using AI to generate test ideas.

**Answers**

1. Black-box testing checks software behavior using inputs and outputs compared against the specification. The tester does not see (and does not depend on) the internal code or structure.
2. Specification-based testing and behavioral testing.
3. Benefits (any three): user perspective; no programming knowledge needed for design; independent of implementation; based on requirements; can start early; independence from developer assumptions. Limitations (any two): cannot see untested code paths; redundancy risk; depends on spec quality; hard to locate the cause of a failure.
4. Because we cannot test every input combination, we must select a smaller set. Techniques give a systematic, repeatable and justifiable way to choose the subset with the best chance of finding defects.
5. Test basis -> test condition -> test case -> test data -> expected result (test data and expected result are both parts of the test case; the order shows increasing concreteness).
6. A test oracle is the source used to determine the expected result (and so decide pass or fail). In black-box testing it is usually the specification or requirements, or a domain expert when the spec is unclear.
7. Black-box (specification-based), white-box (structure-based), experience-based. Today covers black-box techniques plus error guessing from the experience-based family.
8. State transition testing, because the system's behavior depends on the history of failed attempts (its state). Decision tables could complement it for the rules at each state.
9. 9 / 12 x 100 = 75%.
10. Grey-box testing combines black-box test design with partial knowledge of the internals. Example: registering a user through the screen and then checking the database record directly.
11. Because black-box tests are derived from the specification; if code contains behavior the spec never mentions, no test is designed to reach it.
12. Any two: verify expected results against the real spec; check for gaps and duplicates; avoid sharing confidential data; apply your own judgment and technique knowledge; treat generated code as a draft to be run and reviewed.

---

## Key Takeaways

- Black-box testing checks behavior through inputs and outputs, using the specification as the oracle, without relying on internal code.
- Its strengths are the user perspective, early start and independence from implementation; its weaknesses are blind spots in unspecified code, redundancy and dependence on spec quality.
- Because exhaustive testing is impossible, test design techniques help us choose a small, effective, justifiable set of tests.
- Test design flows from test basis to test condition, test case, test data and expected result, with a test oracle deciding what "correct" means.
- The three families are black-box, white-box (Friday) and experience-based (error guessing today, exploratory testing Friday).
- Today's techniques are Equivalence Partitioning, Boundary Value Analysis, Decision Table testing, State Transition testing, Use-case testing and Error Guessing, each suited to a different kind of feature.
- Real features need layered, combined techniques, with traceability and requirements coverage showing what has been verified.
- AI can suggest test ideas quickly, but you remain responsible for verifying every one.
- Next: the dedicated technique lessons, then the pair-programming exercise on Project 1.

---

## Additional Resources

- ISTQB Glossary (definitions of test basis, test condition, test oracle, black-box testing and more): https://glossary.istqb.org
- ISTQB Certified Tester Foundation Level syllabus (test techniques chapter): https://www.istqb.org
- Guru99, "Black Box Testing: Types, Tools & Techniques": https://www.guru99.com/black-box-testing.html
- Ministry of Testing (community articles and talks on test design): https://www.ministryoftesting.com
- pytest documentation (for the Python demo): https://docs.pytest.org
