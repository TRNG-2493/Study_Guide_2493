# Use-Case Testing

**Week 3: Quality Engineering Foundations | Thursday: Test Design Techniques**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define a **use case** and explain who the **actor**, the **system**, and the **goal** are in it.
2. Explain **use-case testing** as a black-box technique that derives tests from use cases and scenarios.
3. Describe every part of a use case: name/ID, actors, goal, preconditions, trigger, main success scenario, alternative flows, exception flows, postconditions, and business rules.
4. Distinguish a use case from a user story and from a test case, and read a simple use case diagram (actors, system boundary, include, extend).
5. Derive test cases from a use case: one for the basic flow, one for each alternative flow, one for each exception flow, plus precondition and postcondition checks.
6. Enumerate scenarios by tracing paths through a flow, build a scenario matrix, and assign test data and expected results.
7. Calculate use-case coverage and explain what it does not cover.
8. Apply the technique to three worked examples (Login, ATM cash withdrawal, Register with email verification) and to two practice use cases of your own.
9. Review a use case for testability by finding missing exception flows and ambiguous steps.
10. Write Given/When/Then scenarios and a small Python test suite for a login flow.

---

## Why This Matters

Earlier today you learned that black-box testing checks what a system does without looking at how it is built. You also learned on Wednesday that testing has two sides: positive testing (does it work when used correctly?) and negative testing (does it fail safely when used incorrectly?). Use-case testing is the technique that ties those ideas to something every real user does: **a complete task from start to finish**.

Think about how real users experience Project 1. Nobody says, "I would like to test the email field in isolation." They say, "I want to log in," or "I want to create an account." Those are goals, and each goal is reached by a sequence of steps. A product can have every field validated perfectly and still fail the user, because step 3 hands the wrong data to step 4, or because nothing tells the user what to do when step 5 goes wrong.

Use-case testing protects the **whole journey**. It helps you:

- Find defects that live **between** steps, not just inside one screen or field.
- Make sure the **negative paths** (wrong password, locked account, service outage) were thought about, not only the happy path.
- Connect testing directly to **requirements**, so every test can be traced back to a documented behaviour.
- Speak the same language as business analysts, developers, and the customer, which makes **user acceptance testing (UAT)** much smoother.

In your Thursday pair exercise you will design tests with three techniques and cross-review each other's work. Use-case testing is the technique that works best when you start from a requirement written as a story about a user's goal, which is exactly how most of Project 1 is described.

---

## The Concept

### 1. The journey analogy

Imagine you are planning a road trip from your home to a friend's house.

- The **destination** is your goal: "arrive at my friend's house."
- The **best route** (the highway, no traffic) is the **main success scenario**.
- A **detour** you can choose on purpose (stopping for coffee, taking the scenic road) is an **alternative flow**. You still arrive, just differently.
- A **roadblock** (bridge closed, flat tyre, no fuel) is an **exception flow**. The trip cannot continue as planned, and what matters is what happens next: do you get a clear sign and a way around, or do you get lost?
- The **starting condition** (you have a car with fuel and you know the address) is the **precondition**.
- Being **at your friend's house** (or safely back home with a clear explanation if the trip failed) is the **postcondition**.

A good tester is like a trip inspector. You do not just drive the best route once and say "it works." You drive the detours, you simulate the roadblocks, and you check that every ending leaves the traveller in a safe, understandable place. That is use-case testing.

---

### 2. What is a use case?

A **use case** is a description of how an **actor** interacts with a **system** to achieve a **goal**.

Let us define each word carefully:

- **Actor**: anyone or anything outside the system that interacts with it. Most often a person (a customer, an administrator), but it can also be another system (a payment service, an email server) or a timer.
- **System**: the product being built or tested. For us, Project 1, the sample web app with User Registration and Login.
- **Goal**: the valuable outcome the actor wants, such as "get into my account" or "create an account."
- **Interaction**: the back-and-forth steps between actor and system: the actor does something, the system responds, and so on.

A use case is written from the **outside**. It says what the user does and what the system visibly does in response. It does not say how the code or the database works. This is exactly why it fits black-box testing.

**Where does the idea come from?** Use cases were popularised by **Ivar Jacobson** in the late 1980s and early 1990s while he worked on object-oriented software engineering. They later became a standard part of the **UML (Unified Modeling Language)**, a widely used visual language for describing software, which includes the **use case diagram**. Alistair Cockburn's book *Writing Effective Use Cases* made the written, step-by-step style (the one you will use today) very popular. Business analysts use them during **requirements analysis**, the activity you studied on Tuesday. So a use case is a requirements document first, and a source of tests second.

---

### 3. What is use-case testing?

**Use-case testing** is a **black-box test design technique** in which test cases are derived from use cases. Each test case exercises one **scenario**, which is one specific path through the use case from the trigger to an ending.

Key points:

- It is **black-box**: you only look at inputs, outputs, and visible behaviour.
- It is **requirements-based**: the use case is the test basis (the document you design tests from).
- It is **scenario-based**: you test complete paths, not isolated fields.
- It is strongest for **integration-level and system-level testing** and **acceptance testing**, where the question is "can the user finish the task?"

The ISTQB Foundation syllabus describes it exactly this way: tests are designed to exercise the defined behaviours of the use case, covering the basic flow and also the alternative and exception paths, and the technique helps uncover integration defects caused by interaction between components.

---

### 4. Anatomy of a use case

A well-written use case has a standard shape. Here is each part, what it means, and why a tester cares.

| Part | What it is | Why a tester cares |
|---|---|---|
| **Use case name / ID** | A short verb-plus-object name ("Log in to account") and a unique ID (UC-01). | The ID lets you trace every test back to its source, which supports traceability. |
| **Actor(s)** | **Primary actor**: the one whose goal it is (the visitor). **Secondary actors**: others who help (an email service, a database). | Tells you who to simulate and what outside systems might fail. |
| **Goal** | The outcome the primary actor wants. | Defines "success." Every test checks whether the goal was or was not reached. |
| **Preconditions** | What must already be true **before** the use case starts (the user is logged out, the site is online). | You must set these up before each test. Also test what happens when they are not true. |
| **Trigger** | The event that starts the use case (the user opens the login page). | Defines your starting point. |
| **Main success scenario** (basic flow, "happy path") | The numbered steps when everything goes right. | Becomes your first test case. |
| **Alternative flows** | Valid variations that still lead to success or a different valid outcome. Labelled by the step where they branch (A1 at step 4). | One test each. |
| **Exception flows** (error flows) | What happens when something goes wrong: invalid input, a failure, a refusal. Labelled E1, E2... | One test each. These are your negative tests. |
| **Postconditions** | What must be true **after** the use case ends. **Success guarantee** (after a good ending) and **failure guarantee** (after a failed ending). | The source of your **expected results**. |
| **Business rules** | Constraints from the business: "lock after 3 failed attempts," "passwords need 8+ characters." | Provide precise expected behaviour and test data. |

#### A blank template you can reuse

```
Use Case ID / Name : UC-xx  <Verb + object>
Primary Actor      : ...
Secondary Actors   : ...
Goal               : ...
Preconditions      : ...
Trigger            : ...
Main Success Scenario:
  1. ...
  2. ...
Alternative Flows:
  A1 (at step n): ...
Exception Flows:
  E1 (at step n): ...
Postconditions:
  Success: ...
  Failure: ...
Business Rules:
  BR1: ...
```

#### The numbering convention

Steps in the main scenario are numbered 1, 2, 3. Branches refer back to a step number: "E3 at step 6." When the branch ends, it either **resumes** the main flow ("return to step 7") or **ends** the use case ("use case ends with failure"). Being explicit about where each flow returns is what lets you trace paths later.

---

### 5. Use case vs user story vs test case

These three artifacts are often confused. You met user stories on Monday in Jira. Here is how they differ.

| Aspect | Use case | User story | Test case |
|---|---|---|---|
| **Purpose** | Describe a complete interaction to reach a goal, including errors. | Capture a small piece of value for a user, as a promise for a conversation. | Check one specific behaviour with specific data and an expected result. |
| **Typical format** | Structured document with steps and flows. | "As a [role], I want [feature], so that [benefit]" plus acceptance criteria. | ID, preconditions, steps, test data, expected result. |
| **Level of detail** | Detailed, step by step. | Short and deliberately light. | Very specific and executable. |
| **Covers errors?** | Yes, explicit exception flows. | Often only in acceptance criteria. | One case per outcome. |
| **Who writes it** | Business analyst, product owner. | Product owner, team. | Tester. |
| **Used for** | Requirements, design, and as a **test basis**. | Planning and backlog in Agile. | Executing and reporting. |
| **Lifespan** | Lives as long as the feature. | Often "done" when the sprint ends. | Reused (regression). |

How they connect: a **user story** says why someone wants something; a **use case** spells out the interaction in detail; a **test case** proves a single path of that interaction works. One use case produces many test cases.

---

### 6. Use case diagrams (UML)

A **use case diagram** gives a one-page overview of who uses the system and what they can do. It does not show steps. The detailed steps live in the written use case.

Elements:

- **Actor**: drawn as a stick figure (we will use `[Actor]` in ASCII).
- **Use case**: drawn as an oval with a verb phrase inside (we will use `( )`).
- **System boundary**: a rectangle around the use cases. Everything inside is the system; actors stay outside.
- **Association**: a line connecting an actor to a use case they take part in.
- **Include** (`<<include>>`): the base use case **always** uses the included one. "Checkout always includes Pay."
- **Extend** (`<<extend>>`): the extending use case **optionally** adds behaviour under a condition. "Login may be extended by Reset password."

#### Diagram for Project 1

```
                 +-------------------- Project 1 Web App ---------------------+
                 |                                                            |
                 |      ( Register new user ) ----<<include>>----> ( Verify   |
                 |             ^                                    email )   |
 [Visitor] ------+-------------+                                       ^      |
     |           |                                                     |      |
     |           |      ( Log in ) <------<<extend>>------ ( Reset password ) |
     +-----------+-------------+                                              |
                 |             |                                              |
 [Registered     |             +----<<include>>----> ( Validate credentials ) |
  User] ---------+------> ( View dashboard )                                  |
                 |                                                            |
                 |      ( Log out )                                           |
 [Email Service]-+------> (Send verification email) <---- used by Register    |
                 |                                                            |
                 +------------------------------------------------------------+
```

Reading the diagram in plain words:

- The **Visitor** (not logged in) can register or log in.
- A **Registered User** can view the dashboard and log out.
- **Register new user** always includes **Verify email** (you cannot finish registering without it).
- **Reset password** is an optional extension of **Log in**; it only happens if the user cannot remember the password.
- The **Email Service** is a **secondary actor**: another system that takes part.
- Everything inside the rectangle is the product. Actors are outside it.

**How do diagrams help testers?** They give you a checklist of use cases to cover. If the diagram shows seven use cases and your test plan mentions four, you have a gap. Include relationships tell you which behaviours are shared (test them once thoroughly, then confirm they are reached from each caller). Extend relationships remind you to test the condition that triggers the extension.

---

### 7. Deriving test cases from a use case

The method is simple and repeatable:

**Step 1. Read the use case slowly.** Highlight actors, preconditions, steps, flows, postconditions, and business rules.

**Step 2. List all flows.** Give each flow a label: Main, A1, A2, E1, E2...

**Step 3. Create a test case for each flow.**

| Source in the use case | Test case you write |
|---|---|
| Main success scenario | One test: follow every step with valid data and check the success postcondition. |
| Each alternative flow | One test: take the branch, complete it, check the resulting outcome. |
| Each exception flow | One test: trigger the failure condition, check the error message and the failure postcondition. |
| Preconditions | Check the setup is correct; optionally try to start when a precondition is false. |
| Postconditions | Each test verifies the relevant postcondition (data saved, session created, nothing changed on failure). |
| Business rules | Pick test data that exercises each rule. |

**Step 4. Add test data and expected results** (see section 9).

**Step 5. Review for coverage** (see section 10).

A key idea: **the postcondition is your oracle**. An **oracle** is the source you use to decide whether a result is correct. If the use case says "after success, the user is on the dashboard and a session exists," then your expected result is exactly that.

Also check **what did not change**. After a failed login, the user should not be logged in, and no session should exist. Failure postconditions are often forgotten, and they are where security defects hide.

---

### 8. Scenario enumeration: tracing paths

A **scenario** is one complete path from the trigger to an ending. The main flow plus each branch gives you the list of scenarios. A **flow diagram** helps you see them.

#### Flow diagram for a simple login

```
            (Start: user opens login page)
                        |
                        v
                 [1. Enter email + password]
                        |
                        v
                 < Fields empty? > --Yes--> [E1: show "required" message] --> (End: failed)
                        | No
                        v
                 < Email format valid? > --No--> [E2: show format error] --> (End: failed)
                        | Yes
                        v
                 < Account found and password correct? >
                        | No                          | Yes
                        v                             v
           [E3: generic error, count+1]       < Account locked? > --Yes--> [E5: locked message] --> (End: failed)
                        |                             | No
                        v                             v
           < Count reached 3? > --Yes-->    < Email verified? > --No--> [E6: verify message] --> (End: failed)
                        | No      [E4: lock]          | Yes
                        v           |                 v
                 (End: failed)   (End: failed)  [Reset counter, create session]
                                                      |
                                                      v
                                          < "Remember me" ticked? >
                                           | Yes                | No
                                           v                    v
                                   [A1: long-lived session]   [normal session]
                                           |                    |
                                           +---------+----------+
                                                     v
                                          [Show dashboard] --> (End: success)
```

Each distinct path through the diagram is a scenario. Do not worry about the arrows being perfect. What matters is the habit: **every decision diamond must have each of its outgoing arrows tested at least once**.

#### The scenario matrix

A **scenario matrix** is a table that lists each scenario, the flows it passes through, the conditions that drive it, and the expected ending. It is the bridge between the use case and your test cases.

| Scenario | Flows traversed | Key condition | Expected ending |
|---|---|---|---|
| SC1 | Basic flow | Valid, verified, unlocked user | Success: dashboard |
| SC2 | Basic + A1 | "Remember me" ticked | Success: long session |
| SC3 | Basic up to step 5, then E1 | Empty fields | Failure: required message |
| SC4 | Basic up to step 6, then E3 | Wrong password (attempt 1 or 2) | Failure: generic error, counter +1 |
| SC5 | Basic up to step 6, then E3 + E4 | Wrong password, 3rd attempt | Failure: account locked |
| SC6 | Basic up to step 7, then E5 | Account already locked | Failure: locked message |

Notice the pattern in names: SC1 is the basic flow, SC2 is "basic plus alternative 1", SC3 and onward are exceptions. Some teams add scenarios that combine flows, such as "A1 then E3." Use judgement, as combinations multiply quickly; see the coverage section.

---

### 9. Test data and expected results per scenario

For each scenario, answer four questions:

1. **What must be set up?** (preconditions: which user exists, in what state)
2. **What exact data will I enter?** (test data)
3. **What exactly should happen?** (expected result from the use case steps and postconditions)
4. **How will I know the system state is correct afterward?** (postcondition check)

Example for SC5 (third wrong password locks the account):

- Setup: user `carol@example.com` exists, verified, unlocked, 2 failed attempts so far.
- Data: email `carol@example.com`, password `WrongPass9`.
- Expected on screen: message "Your account has been locked. Please reset your password."
- Postcondition check: the account is flagged locked; logging in with the **correct** password now also fails; no session cookie is created.

Tips for test data:

- Create **dedicated test users** for each state (new, locked, unverified) so tests are repeatable.
- Use **realistic but fake data** (never real people's information).
- Record data in the test case so another person (your pair partner) can repeat it exactly.
- Where many different values could be tried for one input, that is the job of other techniques such as equivalence partitioning and boundary value analysis, which you will meet separately. Here you pick one sensible value per scenario.

---

### 10. Coverage: how much is enough, and what is missing?

**Use-case coverage** measures how much of the use case's behaviour your tests have exercised. The usual formula:

```
Use-case coverage (%) = (Number of flows covered by tests / Total number of flows) x 100
```

Count flows = main flow + each alternative + each exception.

**Example.** Imagine a login use case with 1 main + 4 alternative + 7 exception = 12 flows. If your tests exercise the main flow, 2 alternatives, and 5 exceptions, that is 1 + 2 + 5 = 8 flows, so coverage is 8 / 12 = 66.7%. The report should list the four flows not yet covered so the team can decide whether the risk is acceptable.

A typical goal is **100% of flows**, with priority on the main flow, then high-risk exceptions (security, money, data loss).

#### What use-case testing does NOT cover

Be honest about limits. Use-case coverage is a **flow coverage**, not a guarantee of correctness.

- **Boundary defects.** The use case says "password must be 8 to 20 characters." Testing one valid password does not check 7, 8, 20, or 21. That is what **boundary value analysis (BVA)** is for.
- **Many input values.** One valid email in the basic flow does not tell you whether other email types work. That is what **equivalence partitioning (EP)** is for.
- **Combinations of conditions.** Locked **and** unverified **and** wrong password at the same time? That is a job for **decision tables**.
- **State and history.** Behaviour that depends on what happened before (the counter of failed attempts, a session that expires) is better modelled with **state transition testing**.
- **Things not written down.** If the use case is missing a flow, your tests will miss it too. Later this week and tomorrow, techniques such as **exploratory testing** and **error guessing** help find the gaps. Regression testing, covered on Friday, then protects the flows you have already verified.
- **Non-functional qualities** such as speed, usability, and security depth need their own tests.

The healthy approach: **use-case testing gives you the skeleton of the test suite, and other techniques add the muscle** at the places where the risk is higher.

---

## Worked Example 1: Login (Project 1)

### The use case

**UC-02: Log in to account**

| Item | Detail |
|---|---|
| **Primary actor** | Registered User (called "User" below) |
| **Secondary actors** | Database (accounts store), Email service not used here |
| **Goal** | The User gains authenticated access to their account dashboard. |
| **Preconditions** | The site is available. The User is not already logged in. The User has a registered account. |
| **Trigger** | The User opens the Login page. |

**Business rules**

- BR1: Both email and password are mandatory.
- BR2: Email must be in a valid format (contains one `@` and a domain).
- BR3: After **3 consecutive** failed password attempts, the account is locked.
- BR4: Error messages for wrong email and wrong password must be the same ("Invalid email or password") so that attackers cannot discover which emails are registered.
- BR5: Only accounts with a verified email can log in.
- BR6: A normal session lasts 30 minutes of inactivity. With "Remember me," it lasts 30 days.

**Main success scenario**

1. The User opens the Login page.
2. The System displays a form with Email, Password, a "Remember me" checkbox, a Login button, and links to "Forgot password?" and "Register."
3. The User enters their email and password.
4. The User clicks Login.
5. The System checks that both fields are filled and the email format is valid.
6. The System finds the account and verifies the password.
7. The System checks that the account is not locked and the email is verified.
8. The System resets the failed-attempt counter to 0 and creates a session.
9. The System redirects the User to the dashboard, which shows "Welcome, <name>."

**Alternative flows**

- **A1 (at step 3): "Remember me" selected.** The User ticks "Remember me." At step 8 the System creates a 30-day session. Resume at step 9.
- **A2 (at step 3): User forgot password.** The User clicks "Forgot password?" The System starts the Reset Password use case. This use case ends.
- **A3 (at step 3): User chooses Register.** The User clicks "Register." The System opens the Register page. This use case ends.
- **A4 (at step 1): User already logged in.** The System redirects straight to the dashboard. This use case ends successfully.

**Exception flows**

- **E1 (at step 5): Empty field(s).** The System shows "Email and password are required" and highlights the empty fields. Return to step 3. No counter change.
- **E2 (at step 5): Invalid email format.** The System shows "Enter a valid email address." Return to step 3.
- **E3 (at step 6): Wrong password.** The System shows "Invalid email or password" and increases the failed-attempt counter by 1. Return to step 3.
- **E4 (at step 6): Unknown email.** The System shows the same "Invalid email or password." No counter exists. Return to step 3.
- **E5 (at step 6): Third consecutive failure.** The System locks the account and shows "Your account is locked. Reset your password to unlock it." The use case ends in failure.
- **E6 (at step 7): Account locked.** The System shows the locked message even if the password is correct. Ends in failure.
- **E7 (at step 7): Email not verified.** The System shows "Please verify your email first" with a "Resend email" link. Ends in failure.
- **E8 (at step 6): System unavailable.** The database cannot be reached. The System shows "Something went wrong. Please try again later." and logs the error. Ends in failure.

**Postconditions**

- **Success:** The User is authenticated; a session exists; the failed-attempt counter is 0; the dashboard is displayed.
- **Failure:** No session is created; the User stays on the Login page (or sees an error page); no account data is changed except the failed-attempt counter and the locked flag where the flows say so.

### Flows count

Main (1) + alternatives A1-A4 (4) + exceptions E1-E8 (8) = **13 flows**.

### Scenario matrix

| Scenario | Flows | Key condition | Expected ending |
|---|---|---|---|
| SC1 | Main | Valid verified user, unticked "Remember me" | Dashboard, 30-min session |
| SC2 | Main + A1 | "Remember me" ticked | Dashboard, 30-day session |
| SC3 | A2 | Click "Forgot password?" | Reset Password page |
| SC4 | A3 | Click "Register" | Register page |
| SC5 | A4 | Already logged in | Redirect to dashboard |
| SC6 | E1 | Both fields empty | "required" message |
| SC7 | E1 | Only password empty | "required" message, email kept |
| SC8 | E2 | Email `alice.example.com` (no @) | Format message |
| SC9 | E3 | Known email, wrong password (1st attempt) | Generic error, counter 1 |
| SC10 | E4 | Unknown email | Same generic error |
| SC11 | E5 | Wrong password, third in a row | Locked message, account locked |
| SC12 | E6 | Locked account, correct password | Locked message |
| SC13 | E7 | Unverified account, correct password | Verify-email message |
| SC14 | E8 | Database down | Friendly error, error logged |

### Test cases

| TC ID | Scenario | Preconditions | Test data | Steps (summary) | Expected result |
|---|---|---|---|---|---|
| TC-LOG-01 | SC1 | User `alice@example.com` verified, unlocked, logged out | Email `alice@example.com`, Password `Secret#123`, Remember me off | Open Login, enter data, click Login | Dashboard shows "Welcome, Alice"; session created; counter = 0 |
| TC-LOG-02 | SC2 | Same as TC-LOG-01 | Same data, Remember me on | Tick box, log in | Dashboard shown; session cookie expires in about 30 days |
| TC-LOG-03 | SC3 | Logged out | None | Click "Forgot password?" | Reset Password page opens |
| TC-LOG-04 | SC4 | Logged out | None | Click "Register" | Register page opens |
| TC-LOG-05 | SC5 | Alice logged in | None | Open `/login` URL | Redirected to dashboard; no second login prompt |
| TC-LOG-06 | SC6 | Logged out | Email empty, password empty | Click Login | "Email and password are required"; both fields highlighted; no request counted as failure |
| TC-LOG-07 | SC7 | Logged out | Email `alice@example.com`, password empty | Click Login | "required" message; email still filled in; counter unchanged |
| TC-LOG-08 | SC8 | Logged out | Email `alice.example.com`, password `Secret#123` | Click Login | "Enter a valid email address"; no login |
| TC-LOG-09 | SC9 | Alice counter = 0 | Email `alice@example.com`, password `Wrong#999` | Click Login | "Invalid email or password"; counter = 1; no session |
| TC-LOG-10 | SC10 | No account for `ghost@example.com` | Email `ghost@example.com`, password `Secret#123` | Click Login | Identical message to TC-LOG-09 (same wording, same page) |
| TC-LOG-11 | SC11 | Alice counter = 2 | Alice, password `Wrong#999` | Click Login | "Your account is locked..."; account flagged locked; no session |
| TC-LOG-12 | SC12 | Bob locked | `bob@example.com`, correct password | Click Login | Locked message; no session |
| TC-LOG-13 | SC13 | Dana registered, not verified | `dana@example.com`, correct password | Click Login | "Please verify your email first"; resend link present |
| TC-LOG-14 | SC14 | Database stopped (test environment) | Alice, correct password | Click Login | Friendly error; no stack trace shown; error logged |
| TC-LOG-15 | Postcondition (SC1) | Alice counter = 2 | Alice, correct password | Log in | Counter resets to 0 after success |
| TC-LOG-16 | Precondition check | Site down or user logged in | None | Try to start the use case | Behaviour is graceful (see TC-LOG-05 and TC-LOG-14) |

**Coverage check:** 14 scenarios cover all 13 flows (E1 is covered twice with different data). Coverage = 13 of 13 = 100% of flows. Notice what is still unchecked: a 129-character email, a password with unusual symbols, a locked account that becomes unlocked after a reset. Those are later jobs for BVA, EP, and state transition testing.

### Given/When/Then for two of these scenarios

```
Scenario: Valid login reaches the dashboard (SC1)
  Given the user "alice@example.com" is verified, unlocked and logged out
  When she enters her correct password and clicks Login
  Then she sees the dashboard with "Welcome, Alice"
  And a session is created
  And her failed-attempt counter is 0

Scenario: Third wrong password locks the account (SC11)
  Given "alice@example.com" has 2 failed attempts
  When she enters a wrong password and clicks Login
  Then she sees "Your account is locked. Reset your password to unlock it."
  And her account is flagged as locked
  And no session is created
```

---

## Worked Example 2: ATM Cash Withdrawal

An ATM example is classic because it has many branches, money is involved, and the order of steps matters.

**UC-ATM-01: Withdraw cash**

- **Primary actor:** Account Holder
- **Secondary actors:** Bank Host System (checks balance and debits), Cash Dispenser (hardware)
- **Goal:** Receive the requested cash and have the account debited correctly.
- **Preconditions:** The ATM is operational and has cash. The Account Holder has a valid card.
- **Trigger:** The Account Holder inserts the card.

**Business rules**

- BR1: PIN allows 3 attempts; after the third failure the card is retained.
- BR2: Withdrawals must be in multiples of 20.
- BR3: Daily withdrawal limit is 500.
- BR4: The ATM cannot dispense more than the balance (no overdraft).
- BR5: The card must be taken back within 30 seconds or it is retracted.

**Main success scenario**

1. The Account Holder inserts the card.
2. The ATM reads the card and asks for the PIN.
3. The Account Holder enters the PIN.
4. The ATM verifies the PIN with the Bank Host and shows the main menu.
5. The Account Holder selects "Withdraw cash."
6. The ATM asks for the amount.
7. The Account Holder enters an amount.
8. The ATM checks the amount rules, the daily limit, and the balance with the Bank Host.
9. The ATM asks whether a receipt is wanted; the Account Holder says yes.
10. The ATM returns the card; the Account Holder takes it.
11. The ATM dispenses the cash and prints the receipt.
12. The Bank Host debits the account; the ATM returns to the welcome screen.

**Alternative flows**

- **A1 (at step 7):** The Account Holder picks a preset amount (for example 100) instead of typing.
- **A2 (at step 9):** The Account Holder declines a receipt. No receipt is printed.
- **A3 (at step 5):** The Account Holder selects a different service (check balance). The Withdraw use case ends.
- **A4 (at step 7):** The Account Holder presses Cancel. The card is returned and the use case ends without debit.

**Exception flows**

- **E1 (at step 2):** Card unreadable or not recognised. The ATM ejects it with "Card not supported."
- **E2 (at step 4):** Wrong PIN. The ATM allows a retry (return to step 3).
- **E3 (at step 4):** Third wrong PIN. The ATM retains the card and ends.
- **E4 (at step 8):** Amount not a multiple of 20. The ATM asks for a new amount (return to step 7).
- **E5 (at step 8):** Insufficient funds. The ATM shows a message and offers another amount (return to step 7).
- **E6 (at step 8):** Daily limit exceeded. Same handling as E5 with a limit message.
- **E7 (at step 8):** ATM does not hold enough cash for the amount. It apologises and offers a smaller amount.
- **E8 (at step 10):** Card not taken within 30 seconds. The ATM retracts it and does not dispense cash.
- **E9 (at step 8 or 12):** Bank Host not reachable. The ATM cancels the transaction, returns the card, and dispenses nothing.

**Postconditions**

- **Success:** Cash dispensed equals the amount requested; the account is debited by exactly that amount; a receipt is printed if requested; the card has been returned.
- **Failure:** No cash dispensed; no debit; the card is returned (or retained after three PIN failures); the reason is shown.

Flow count: 1 main + 4 alternatives + 9 exceptions = **14 flows**.

### Scenario matrix

| Scenario | Flows | Condition | Expected ending |
|---|---|---|---|
| SC1 | Main | Valid card, correct PIN, amount 100, sufficient funds | Cash 100, debit 100, receipt, card returned |
| SC2 | Main + A1 | Preset amount selected | Same as SC1 |
| SC3 | Main + A2 | Receipt declined | Cash and debit; no receipt |
| SC4 | A3 | Choose check balance | Balance shown; no debit |
| SC5 | A4 | Cancel at amount screen | Card returned; no debit |
| SC6 | E1 | Unreadable card | Ejected with message |
| SC7 | E2 then Main | Wrong PIN once, then correct | Continues to success |
| SC8 | E2 + E3 | Wrong PIN three times | Card retained |
| SC9 | E4 then Main | Amount 50, then 60 | Error, then success |
| SC10 | E5 | Amount above balance | Message, no debit |
| SC11 | E6 | Over daily limit | Message, no debit |
| SC12 | E7 | ATM low on cash | Message, offers smaller amount |
| SC13 | E8 | Card left in slot | Card retracted, no cash |
| SC14 | E9 | Host connection lost | Cancel, card returned, no debit |

Notice SC7 and SC9 are **exception-then-recovery** scenarios: the flow loops back and succeeds. These are valuable because defects often hide in loops (for example, the PIN counter not resetting after a good entry).

### Selected test cases

| TC ID | Scenario | Preconditions | Test data | Expected result |
|---|---|---|---|---|
| TC-ATM-01 | SC1 | Balance 1000, daily total 0, ATM stocked | PIN 4821, amount 100 | 100 dispensed; balance 900; receipt shows 100 and 900; card returned before cash |
| TC-ATM-02 | SC2 | Same | Preset "100" | Same as TC-ATM-01 |
| TC-ATM-03 | SC3 | Same | Receipt = No | No receipt printed; balance 900 |
| TC-ATM-04 | SC4 | Same | Menu: Balance | Balance 1000 displayed; no debit |
| TC-ATM-05 | SC5 | Same | Press Cancel at amount screen | Card returned; balance 1000 |
| TC-ATM-06 | SC6 | Same | Damaged card | "Card not supported"; card ejected |
| TC-ATM-07 | SC7 | Same | PIN 0000 then 4821 | "Incorrect PIN" then success |
| TC-ATM-08 | SC8 | Same | PIN 0000 three times | Card retained; message to contact the bank |
| TC-ATM-09 | SC9 | Same | Amount 50 then 60 | "Amounts must be multiples of 20" then success with 60 |
| TC-ATM-10 | SC10 | Balance 80 | Amount 100 | "Insufficient funds"; no debit |
| TC-ATM-11 | SC11 | Daily total 450 | Amount 100 | Limit message; no debit |
| TC-ATM-12 | SC12 | ATM holds 40 in cash | Amount 100 | "Unable to dispense this amount"; offers smaller; no debit |
| TC-ATM-13 | SC13 | Same as TC-ATM-01 | Do not remove card for 31 seconds | Card retracted; no cash; no debit |
| TC-ATM-14 | SC14 | Bank host disconnected | Amount 100 | Transaction cancelled; no cash; no debit; card returned |
| TC-ATM-15 | Postcondition | After TC-ATM-07 | Check PIN counter | Counter reset to 0 after success |

Coverage: 14 of 14 flows = 100%. Not covered: what happens at the exact limit values (exactly 500 total, exactly the balance), which belongs to BVA, and the combination "insufficient funds and over limit at the same time," which belongs to decision tables.

---

## Worked Example 3: Register a New User with Email Verification

**UC-01: Register new user** (Project 1)

- **Primary actor:** Visitor
- **Secondary actors:** Email Service, Database
- **Goal:** Create an active account.
- **Preconditions:** The site is available; the Visitor is not logged in.
- **Trigger:** The Visitor opens the Register page.

**Business rules**

- BR1: Full name, email, password, confirm password are required; the terms checkbox must be ticked.
- BR2: Email must be unique across all accounts.
- BR3: Password must have at least 8 characters, one uppercase letter, one number, and one symbol.
- BR4: Password and confirmation must match.
- BR5: The verification link is valid for 24 hours and can be used once.
- BR6: An account cannot log in until verified.

**Main success scenario**

1. The Visitor opens the Register page.
2. The System shows the registration form.
3. The Visitor fills in name, email, password, confirm password, and ticks the terms box.
4. The Visitor clicks "Create account."
5. The System validates all fields against the business rules.
6. The System checks that the email is not already registered.
7. The System creates the account with status "Pending verification."
8. The System asks the Email Service to send a verification email containing a unique link.
9. The System displays "Check your inbox to verify your email."
10. The Visitor opens the email and clicks the link.
11. The System validates the link (exists, not expired, not used).
12. The System changes the account status to "Active" and shows "Email verified. You can now log in."

**Alternative flows**

- **A1 (at step 9): Resend verification.** The Visitor clicks "Resend email." The System invalidates the previous link, sends a new one, and shows a confirmation. Return to step 10.
- **A2 (at step 3): Optional newsletter.** The Visitor ticks "Send me updates." The preference is saved. Resume at step 4.
- **A3 (at step 12): Go to login.** The Visitor clicks "Log in." The Login use case begins.

**Exception flows**

- **E1 (at step 5): Required field missing.** The System shows which fields are required. Return to step 3.
- **E2 (at step 5): Password breaks the policy.** The System lists the unmet rules. Return to step 3.
- **E3 (at step 5): Passwords do not match.** The System shows "Passwords do not match." Return to step 3.
- **E4 (at step 5): Terms not accepted.** The System shows "You must accept the terms." Return to step 3.
- **E5 (at step 6): Email already registered.** The System shows a message that does not expose account details beyond what the business agreed (for example, "An account with this email may already exist. Try logging in.") and returns to step 3.
- **E6 (at step 8): Email Service unavailable.** The account is created, but the System shows "We could not send your email. Use Resend." and queues a retry. Continue at A1.
- **E7 (at step 11): Link expired (older than 24 hours).** The System shows "This link has expired" and offers a new link. Account stays Pending.
- **E8 (at step 11): Link already used.** The System shows "This link has already been used" and offers Login.
- **E9 (at step 11): Link invalid or tampered.** The System shows a generic invalid-link message. Account is not changed.

**Postconditions**

- **Success:** Exactly one Active account exists for the email; the password is stored securely (hashed); the verification link can no longer be used.
- **Failure:** No new Active account exists; no duplicate account for the email was created; the Visitor sees what to do next.

Flow count: 1 + 3 + 9 = **13 flows**.

### Scenario matrix

| Scenario | Flows | Condition | Expected ending |
|---|---|---|---|
| SC1 | Main | All valid, link clicked within 24 hours | Active account |
| SC2 | Main + A2 | Newsletter ticked | Active account, preference saved |
| SC3 | Main + A1 | Resend before clicking | Old link dead, new link works |
| SC4 | Main + A3 | Click "Log in" after verification | Login page opens |
| SC5 | E1 | Name left blank | Required message |
| SC6 | E2 | Password `abc` | Policy message listing unmet rules |
| SC7 | E3 | Confirm differs | Mismatch message |
| SC8 | E4 | Terms unticked | Terms message |
| SC9 | E5 | Email already in use | Safe duplicate message, no second account |
| SC10 | E6 | Email service down | Account Pending, resend offered |
| SC11 | E7 | Link older than 24 hours | Expired message, account Pending |
| SC12 | E8 | Link clicked twice | Second click shows "already used" |
| SC13 | E9 | Token altered | Invalid-link message, no change |

### Selected test cases

| TC ID | Scenario | Test data | Expected result |
|---|---|---|---|
| TC-REG-01 | SC1 | Name `Priya Rao`, email `priya@example.com`, password `Good#Pass1`, confirm same, terms on | "Check your inbox" page; account Pending; email received; clicking link shows "Email verified"; account Active; login now works |
| TC-REG-02 | SC2 | As above plus newsletter on | Preference stored as true |
| TC-REG-03 | SC3 | Click Resend, then use the first link | First link rejected; second link activates |
| TC-REG-04 | SC4 | After verification, click "Log in" | Login page shown |
| TC-REG-05 | SC5 | Name blank | "Full name is required"; no account created |
| TC-REG-06 | SC6 | Password `abc` | Message lists missing length, uppercase, number, symbol |
| TC-REG-07 | SC7 | Confirm `Good#Pass2` | "Passwords do not match" |
| TC-REG-08 | SC8 | Terms unticked | "You must accept the terms" |
| TC-REG-09 | SC9 | Email `priya@example.com` again | Safe duplicate message; still exactly one account |
| TC-REG-10 | SC10 | Email service stubbed to fail | Account Pending; message with Resend |
| TC-REG-11 | SC11 | Link with creation time set to 25 hours ago | "Link has expired"; still Pending |
| TC-REG-12 | SC12 | Click the link twice | Second click: "already used"; account stays Active |
| TC-REG-13 | SC13 | Remove last character from the token | Invalid-link message; no state change |
| TC-REG-14 | Postcondition on SC1 | Inspect stored password | Not stored in readable text |
| TC-REG-15 | Postcondition on login | Pending account tries to log in | Login refused with verify message (links to Login E7) |

This example shows an important feature of use cases: they **chain**. TC-REG-15 verifies the connection between Register and Login. That kind of cross-use-case check is where integration defects are found.

---

## End-to-End Testing, Acceptance Testing, and Given/When/Then

### End-to-end (business process) testing

A **business process** is a chain of use cases that together deliver business value. Example for Project 1: Register, verify email, log in, view dashboard, log out. **End-to-end (E2E) testing** runs a whole chain with realistic data and checks that the pieces work together. Use cases are the natural building blocks: you take the success scenarios of several use cases and link them, then add a few chosen exception paths in the middle ("what if the link is expired and the user requests a new one?").

A simple E2E scenario for Project 1:

```
Register (SC1) --> Verify email (SC1) --> Login (SC1) --> Dashboard --> Logout
```

### Link to user acceptance testing (UAT)

**User Acceptance Testing (UAT)** is the final testing phase in which the customer or business representatives confirm that the system supports their real needs. Because use cases are written in business language and describe real tasks, they are an ideal basis for UAT: each success scenario becomes an acceptance test, and users judge "Can I do my job with this?" You have already seen UAT as part of the V-model and the STLC.

### Given/When/Then: the same idea in a different notation

**Behaviour-Driven Development (BDD)** is a team practice in which people agree on behaviour using concrete examples before coding. Its scenarios use the keywords **Given** (the starting context, like preconditions), **When** (the action, like the trigger and steps), and **Then** (the visible result, like postconditions). This is called **Gherkin** notation. You will only get a short introduction today; deeper BDD and tools come later in the programme.

How the two notations map:

| Use case | Given/When/Then |
|---|---|
| Precondition | Given |
| Trigger and steps | When |
| Postcondition / expected result | Then |
| One scenario (a path) | One Scenario |
| Alternative or exception flow | A separate Scenario |

Example: the exception flow E2 (invalid email) from Login:

```
Scenario: Login with an email that has no @ sign
  Given I am on the Login page
  When I enter "alice.example.com" as email and "Secret#123" as password
  And I click Login
  Then I see "Enter a valid email address"
  And I am still on the Login page
```

Both notations are fine. Use cases give a complete picture of one goal; Given/When/Then gives short, precise, easy-to-automate examples. Many teams write use-case-style analysis and then record each scenario in Given/When/Then.

---

## Reviewing a Use Case for Testability

Testers are often the best reviewers of requirements because they ask, "How would I verify this?" A use case is **testable** when each step is specific, every decision has all its outcomes defined, and the expected results are observable.

### Review checklist

- Is there a single, clear **goal**, and a named **primary actor**?
- Are **preconditions** and **postconditions** stated (both success and failure)?
- Is every step a **single, observable action**, with the actor clearly identified?
- Are words like "appropriate," "quickly," "valid," "etc.," "as needed," or "user-friendly" replaced by exact rules or numbers?
- For every step that can fail, is there an **exception flow**? (Think: invalid input, no permission, timeout, outside system down, duplicate, cancelled.)
- Does every branch say where it **returns** or **ends**?
- Are **business rules** written down with values (limits, lengths, durations)?
- Are error messages specified, or at least their intent?
- Are **secondary actors** and their failures considered?

### A flawed use case

**UC-07: Transfer money**

- Actor: User
- Precondition: User is logged in.
- Main flow:
  1. User chooses Transfer.
  2. System shows the form.
  3. User fills in the details.
  4. System checks the details.
  5. System does the transfer quickly.
  6. System tells the user it worked.
- Alternative flow: User can cancel.
- Postcondition: Money is transferred.

**Your task:** find at least eight problems.

### Answer key

1. **No goal statement and no secondary actors.** The destination account's bank and the payment system are involved but not named.
2. **Step 3 "fills in the details" is ambiguous.** Which details? Recipient, amount, reference, date? Each needs a business rule.
3. **Step 4 "checks the details" is ambiguous.** Which checks? Balance, limits, valid account number, same-account transfers? No rules are given.
4. **Step 5 "quickly" is not measurable.** How quickly? A tester cannot assert it. (For example: "within 3 seconds.")
5. **The alternative flow "User can cancel" has no step number**, so we do not know when cancelling is allowed and what happens to the data.
6. **No exception flows at all.** Missing: insufficient funds, invalid recipient, limit exceeded, system timeout, duplicate submission, session expiry, secondary system down, user not authorised.
7. **Postcondition covers only success.** There is no failure guarantee: what happens to the balances when something fails halfway?
8. **No business rules.** Daily limit, minimum amount, currency, fees.
9. **No trigger** is explicitly stated.
10. **Step 6 "it worked" does not define the confirmation** (reference number? new balance?).
11. **No mention of security checks** such as re-entering a password or a one-time code, which a real money transfer would need. Ask the analyst.
12. **Main flow does not say which actor performs step 4 to 6 on which system.**

Reporting these as questions to the analyst, not as accusations, is part of professional QE practice. Reviewing requirements this way finds defects before any code exists, which is much cheaper to fix, as you learned in the V-model and the testing principles.

---

## Use-Case Testing in Agile

In Agile teams (Scrum, which you studied on Monday), formal use case documents are often replaced by lighter artifacts, but the **thinking is the same**:

- **User story** states the goal: "As a registered user, I want to log in so that I can see my dashboard."
- **Acceptance criteria** list the conditions the story must meet. These are effectively the main flow, the alternatives, and the exceptions in compressed form.
- **Scenarios** (often in Given/When/Then) are attached to the story and become the shared definition of "done."

Example acceptance criteria for a login story:

1. Valid credentials lead to the dashboard.
2. Wrong credentials show a generic error.
3. Three failed attempts lock the account.
4. Locked accounts cannot log in.
5. Empty fields show a required message.

A tester can turn these into scenarios and use the **use-case questions** to find the gaps: "What about unverified users? What if the system is down?" Raise them in backlog refinement and in the "Three Amigos" conversation (a short meeting among a business person, a developer, and a tester to agree on a story's behaviour). Tracking each scenario as a sub-task or a linked test case in Jira keeps traceability from story to test.

In Agile, use-case testing is applied **per story** and **per sprint**, and a growing set of scenarios becomes the regression suite (which you will learn about on Friday).

---

## Tools and Documentation Tips

- **Keep one use case per file or page**, with a stable ID. Wikis, Confluence pages, or Markdown files in the repository all work.
- **Write steps as "The System does X" or "The User does Y."** Avoid mixing two actions in one step.
- **Label every flow** (Main, A1, E1) and **reference step numbers** so you can trace paths.
- **Use a spreadsheet** (or a Jira test management add-on) for the scenario matrix and test cases. Columns: Scenario ID, Flows, Condition, Test case ID, Data, Expected.
- **Maintain traceability:** add the use case ID and flow label in each test case's "requirement" field.
- **Draw diagrams with simple tools:** draw.io (diagrams.net), Lucidchart, PlantUML, or Visual Paradigm for UML. Even a whiteboard photo is useful early on.
- **Version your use cases.** When a business rule changes, update the use case first, then the tests.
- **Review with a partner.** A second pair of eyes finds missing exception flows faster than one person alone. This is exactly what you will do in today's pair exercise.

---

## Common Mistakes

1. **Testing only the happy path.** The main flow is just one of many; most defects are in exception flows.
2. **Forgetting postconditions.** Checking the screen message but not the system state (is the session really absent after a failure?).
3. **Skipping preconditions.** Tests that fail because the data was not set up are confusing; tests that never check what happens when a precondition is false miss defects.
4. **Vague expected results** like "works fine" or "error shown." Write the exact message and state.
5. **Assuming the use case is complete.** It may have missing flows. Review it first and ask questions.
6. **Mixing several flows in one test.** If a combined test fails, you cannot tell which flow is broken. One flow, one test, then add combinations deliberately.
7. **Treating 100% flow coverage as proof of quality.** It only means each flow was tried once.
8. **Ignoring secondary actors.** Email servers, payment gateways, and databases fail in real life.
9. **Using real personal data** in test cases. Always use fictional data.
10. **Not returning to the step.** Exception flows that loop back (E2 then success) need a test that completes the loop.
11. **Confusing a use case with a user story or a test case.** Each has its own level of detail and purpose.

---

## Python Example: Modelling the Login Flow and Testing Each Scenario

To make the idea concrete, we model a small version of the Login use case as a Python function, and write one test per scenario. This is a **model**: a simplified stand-in that shows how scenarios turn into automated checks. You do not need to know advanced Python. We use plain `assert` statements, which stop the program with an error if the condition is False.

We cover the scenarios: basic flow (SC1), wrong password (SC2), locked account (SC3), empty fields (SC4), and the third wrong attempt locking the account (SC5).

### The code (`login_flow.py`)

```python
"""Login use case modelled as a function, with one test per scenario."""

MAX_FAILED_ATTEMPTS = 3


def make_users():
    """Return a fresh 'database' so tests never affect each other."""
    return {
        "alice@example.com": {"password": "Secret#123", "locked": False, "failed": 0},
        "bob@example.com": {"password": "Other#456", "locked": True, "failed": 3},
    }


def login(users, email, password):
    """Run the Login use case. Returns a result dictionary."""
    if not email or not password:                       # EX1: empty fields
        return {"ok": False, "message": "Email and password are required", "page": "login"}

    user = users.get(email)
    if user is None:                                    # EX2: unknown account
        return {"ok": False, "message": "Invalid email or password", "page": "login"}

    if user["locked"]:                                  # EX4: locked account
        return {"ok": False, "message": "Account locked", "page": "login"}

    if password != user["password"]:                    # EX3: wrong password
        user["failed"] += 1
        if user["failed"] >= MAX_FAILED_ATTEMPTS:
            user["locked"] = True
            return {"ok": False, "message": "Account locked", "page": "login"}
        return {"ok": False, "message": "Invalid email or password", "page": "login"}

    user["failed"] = 0                                  # success: reset counter
    return {"ok": True, "message": "Welcome", "page": "dashboard"}


def test_sc1_basic_flow_valid_login():
    users = make_users()
    result = login(users, "alice@example.com", "Secret#123")
    assert result["ok"] is True
    assert result["page"] == "dashboard"
    assert users["alice@example.com"]["failed"] == 0


def test_sc2_wrong_password():
    users = make_users()
    result = login(users, "alice@example.com", "WrongPass")
    assert result["ok"] is False
    assert result["message"] == "Invalid email or password"
    assert users["alice@example.com"]["failed"] == 1


def test_sc3_locked_account_even_with_correct_password():
    users = make_users()
    result = login(users, "bob@example.com", "Other#456")
    assert result["ok"] is False
    assert result["message"] == "Account locked"


def test_sc4_empty_fields():
    users = make_users()
    result = login(users, "", "")
    assert result["ok"] is False
    assert result["message"] == "Email and password are required"


def test_sc5_third_wrong_attempt_locks_account():
    users = make_users()
    for _ in range(3):
        result = login(users, "alice@example.com", "bad")
    assert result["message"] == "Account locked"
    assert users["alice@example.com"]["locked"] is True
    # Postcondition check: even the right password is now refused
    assert login(users, "alice@example.com", "Secret#123")["ok"] is False


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
            passed += 1
        except AssertionError:
            print("FAIL", t.__name__)
    print(f"{passed} of {len(tests)} tests passed")
```

### How to run it

Save the code as `login_flow.py` and run `python3 login_flow.py` in a terminal. (If you have pytest installed, `python3 -m pytest login_flow.py -q` also finds and runs the `test_` functions.)

### Expected output

```
PASS test_sc1_basic_flow_valid_login
PASS test_sc2_wrong_password
PASS test_sc3_locked_account_even_with_correct_password
PASS test_sc4_empty_fields
PASS test_sc5_third_wrong_attempt_locks_account
5 of 5 tests passed
```

### Line-by-line explanation

**The docstring and constant**

- `"""Login use case ... """` (line 1): a triple-quoted text at the top that describes the file. Python ignores it when running; it helps humans.
- `MAX_FAILED_ATTEMPTS = 3`: a named constant for the business rule "lock after 3 failures." Naming it means the rule lives in one place and the code reads clearly.

**`make_users()`**

- `def make_users():`: defines a function (a reusable block of code) named `make_users` that takes no inputs.
- The docstring explains it returns a fresh store, so one test cannot change the data of another. This is an important testing habit called **test independence**.
- `return { ... }`: gives back a dictionary (a collection of key-value pairs) that models our accounts table.
- Each email is a **key**; each value is another dictionary with three fields: `password`, `locked` (True or False), and `failed` (count of failed attempts so far).
- Alice is a normal active user; Bob is already locked after 3 failures. These are our **preconditions** for different scenarios.

**`login(users, email, password)`**

- `def login(users, email, password):`: defines the function that models the use case. It takes the data store and the two form fields.
- The docstring says what it does and that it returns a dictionary describing the result.
- `if not email or not password:`: True when either field is an empty string. In Python an empty string counts as False, so `not email` is True for empty. This is flow **E1**.
- `return {"ok": False, "message": ..., "page": "login"}`: ends the function early and reports failure, the exact message, and that the user stays on the login page. The returned dictionary models the **observable outcome** (a black-box view).
- `user = users.get(email)`: looks up the account by email; `get` returns `None` if it is missing instead of raising an error.
- `if user is None:`: the unknown account flow. It returns the **same** generic message as a wrong password, which follows business rule BR4 from our use case.
- `if user["locked"]:`: checks the locked flag before checking the password. The locked message comes back even if the password is correct, as required.
- `if password != user["password"]:`: true when the password is wrong. (Real systems store hashed passwords; we keep plain text for simplicity of the model.)
- `user["failed"] += 1`: adds 1 to the failed counter, which is a **postcondition** of the wrong-password flow.
- `if user["failed"] >= MAX_FAILED_ATTEMPTS:`: checks whether the lock rule is now triggered.
- `user["locked"] = True`: sets the locked flag.
- The nested `return` statements give the locked message when the limit is reached, or the generic error otherwise.
- `user["failed"] = 0`: reached only when all checks pass; resets the counter (success postcondition).
- The final `return {"ok": True, ...}` models the main success scenario: dashboard page.

**The tests**

- Each function name starts with `test_` so pytest (and our small runner) can find it. The name also states the scenario, which keeps tests readable and traceable to the scenario matrix.
- `users = make_users()`: arrange step, preparing a fresh state (the **precondition**).
- `result = login(...)`: act step, running the use case with the scenario's data.
- `assert result["ok"] is True`: checks the outcome flag. If it is not True, Python raises an `AssertionError` and the test fails.
- `assert result["page"] == "dashboard"`: checks where the user lands.
- `assert users["alice@example.com"]["failed"] == 0`: checks the **system state** (postcondition), not only what was displayed.
- In `test_sc2`, we check the message text and that the counter is exactly 1. Checking both output and state is the core of use-case test design.
- In `test_sc3`, we use Bob (already locked) and the **correct** password, to prove the locked state beats a correct password.
- In `test_sc4`, empty strings trigger the required-fields flow.
- In `test_sc5`, the `for _ in range(3):` loop repeats the wrong-password attempt three times. The underscore `_` means "I do not need the loop variable." After the loop, `result` holds the third response. We then assert the locked message, the locked flag, and a final postcondition check that even the correct password is refused afterwards.

**The runner (`if __name__ == "__main__":`)**

- This block runs only when the file is executed directly, not when pytest imports it.
- `tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]`: builds a list of every function in the file whose name starts with `test_`. `globals()` holds everything defined in the file; `sorted` gives a stable order.
- `passed = 0`: counts successes.
- `for t in tests:`: loops over each test function.
- `try: t()`: runs the test.
- `print("PASS", t.__name__)` and `passed += 1`: report and count a success.
- `except AssertionError:` catches a failed assert and prints `FAIL` instead of crashing, so we see all results.
- The final `print(f"...")` shows the total. The `f` before the quotes lets us insert variables in braces.

**Try this variation:** change `MAX_FAILED_ATTEMPTS` to 4 and re-run. Which tests fail? Why? (Answer: `test_sc5` fails, because after 3 wrong attempts the account is not locked yet. This shows how business rules and tests must stay in sync.)

---

## Practice Exercises

### Exercise A: Reset password

**Use case UC-03: Reset password**

- Primary actor: Registered User. Secondary actors: Email Service.
- Precondition: User has an account. Trigger: User clicks "Forgot password?" on the Login page.
- Business rules: Reset link valid for 1 hour and usable once. New password must follow the same policy as registration (8+ characters, uppercase, number, symbol). The new password must differ from the current one.
- Main flow:
  1. User clicks "Forgot password?"
  2. System shows an email entry page.
  3. User enters email and clicks "Send reset link."
  4. System checks that the email is registered.
  5. System emails a reset link.
  6. System shows "If this email is registered, a link has been sent."
  7. User opens the email and clicks the link.
  8. System validates the link and shows a new-password form.
  9. User enters a new password and confirmation, then submits.
  10. System validates the password and saves it.
  11. System unlocks the account if locked, invalidates the link, and shows "Password changed. Log in."
- Alternative flows: A1 (at step 9) the User cancels, and the password stays unchanged. A2 (at step 10 to 11) a locked account becomes unlocked.
- Exception flows: E1 empty email. E2 invalid email format. E3 email not registered (same message as step 6, no email sent). E4 link expired. E5 link already used. E6 passwords do not match. E7 password breaks the policy. E8 new password equals the old one. E9 email service down.

**Your task:** (1) list the scenarios, (2) build a scenario matrix, (3) write at least 10 test cases with data and expected results, (4) calculate your coverage.

**Sample answer**

Flow count: Main + A1 + A2 + E1 to E9 = 12 flows.

Scenario matrix:

| Scenario | Flows | Condition |
|---|---|---|
| SC1 | Main | Registered email, valid new password |
| SC2 | Main + A2 | Account was locked; reset unlocks it |
| SC3 | A1 | User cancels at the new-password form |
| SC4 | E1 | Email empty |
| SC5 | E2 | Email `bob.example` |
| SC6 | E3 | Unregistered email |
| SC7 | E4 | Link older than 1 hour |
| SC8 | E5 | Link used twice |
| SC9 | E6 | Confirmation differs |
| SC10 | E7 | Weak password `abc` |
| SC11 | E8 | New equals old |
| SC12 | E9 | Email service down |

Sample test cases:

| TC | Scenario | Data | Expected |
|---|---|---|---|
| TC-RST-01 | SC1 | `alice@example.com`; new password `NewPass#456` | Generic "link sent" message; email arrives; link shows form; password changes; login works with the new password and fails with the old; link no longer usable |
| TC-RST-02 | SC2 | Locked Bob, valid reset | Account unlocked; login works |
| TC-RST-03 | SC3 | Cancel at the form | Password unchanged; old password still works |
| TC-RST-04 | SC4 | Empty email | "Email is required"; no email sent |
| TC-RST-05 | SC5 | `bob.example` | Format error; no email sent |
| TC-RST-06 | SC6 | `nobody@example.com` | Same message as TC-RST-01 step 6; no email sent (do not reveal registration) |
| TC-RST-07 | SC7 | Link 61 minutes old | "Link has expired"; offers new link |
| TC-RST-08 | SC8 | Use link twice | Second use rejected |
| TC-RST-09 | SC9 | `NewPass#456` and `NewPass#457` | Mismatch message; password unchanged |
| TC-RST-10 | SC10 | `abc` | Policy message; password unchanged |
| TC-RST-11 | SC11 | Current password reused | "Choose a different password" |
| TC-RST-12 | SC12 | Email service failing | Friendly message with retry; no crash |

Coverage = 12 of 12 flows = 100%. Not covered: the exact 1-hour boundary (60 minutes versus 61 minutes) which BVA will handle, and security ideas not in the use case (for example, whether the same link works for another account), which exploratory testing may find.

### Exercise B: Book a movie ticket

**Use case UC-10: Book a movie ticket**

- Primary actor: Customer. Secondary actors: Payment Gateway, Email/SMS service.
- Preconditions: Customer is logged in; at least one show is scheduled.
- Business rules: Maximum 6 seats per booking. Seats are held for 5 minutes during payment. Cancelled payments release the seats. Tickets are sent by email after payment.
- Main flow:
  1. Customer selects a movie.
  2. System lists showtimes and theatres.
  3. Customer selects a showtime.
  4. System displays the seat map.
  5. Customer selects seats.
  6. System holds the seats for 5 minutes and shows the price.
  7. Customer clicks "Pay" and enters payment details.
  8. System sends the payment to the Payment Gateway.
  9. Gateway confirms payment.
  10. System confirms the booking and sends tickets by email.
- Alternative flows: A1 the Customer applies a valid discount code (at step 7). A2 the Customer chooses to pay with saved card (at step 7).
- Exception flows: E1 no showtimes available. E2 seat already taken when the Customer picks it. E3 more than 6 seats chosen. E4 the 5-minute hold expires. E5 payment declined. E6 gateway timeout. E7 invalid discount code. E8 Customer abandons the booking (closes the page). E9 email service fails.

**Your task:** write the scenario list, the matrix, and at least 10 test cases.

**Sample answer**

Flow count: 1 + 2 + 9 = 12 flows.

| Scenario | Flows | Condition | Expected ending |
|---|---|---|---|
| SC1 | Main | 2 seats, card payment succeeds | Booking confirmed, email sent |
| SC2 | Main + A1 | Valid code `SAVE10` | Discounted price; confirmed |
| SC3 | Main + A2 | Saved card | Confirmed |
| SC4 | E1 | Movie with no shows | "No showtimes" message |
| SC5 | E2 | Seat taken by someone else just before | Message; seat map refreshed; no hold on that seat |
| SC6 | E3 | 7 seats selected | Limit message; no hold |
| SC7 | E4 | Wait 6 minutes at payment | Hold expired message; seats released |
| SC8 | E5 | Card declined | Message; seats still held until timer; no booking |
| SC9 | E6 | Gateway times out | No double charge; clear status; seats handled per rule |
| SC10 | E7 | Code `BADCODE` | "Invalid code"; price unchanged; can continue |
| SC11 | E8 | Close page after choosing seats | Seats released after 5 minutes; no booking |
| SC12 | E9 | Email service fails | Booking confirmed; ticket visible in "My bookings"; resend offered |

Sample test cases:

| TC | Scenario | Data | Expected |
|---|---|---|---|
| TC-BK-01 | SC1 | Movie "Space Quest", 7 PM show, seats B4 and B5, test card approved | Confirmation number shown; email with 2 tickets; seats B4 and B5 now unavailable to others |
| TC-BK-02 | SC2 | Code `SAVE10` | Price reduced by 10%; booking confirmed |
| TC-BK-03 | SC3 | Saved test card | Booking confirmed without retyping card |
| TC-BK-04 | SC4 | Movie with no schedule | "No showtimes available" |
| TC-BK-05 | SC5 | Two sessions pick seat C3; second submits late | Second session sees "Seat no longer available"; only one booking for C3 |
| TC-BK-06 | SC6 | Select 7 seats | "Maximum 6 seats per booking" |
| TC-BK-07 | SC7 | Wait 6 minutes on payment page | "Your hold has expired"; seats available again |
| TC-BK-08 | SC8 | Decline-test card | "Payment declined"; no ticket email; no booking record |
| TC-BK-09 | SC9 | Gateway stub delays 60 seconds | User informed; no duplicate charge; consistent status |
| TC-BK-10 | SC10 | `BADCODE` | "Invalid discount code"; can retry or continue |
| TC-BK-11 | SC11 | Close tab after step 6 | After 5 minutes seats available; no booking |
| TC-BK-12 | SC12 | Email stub fails | Booking exists; appears in My bookings; resend option |

Coverage = 12 of 12 flows = 100%. SC5 (two users, one seat) is a concurrency scenario that a use case rarely spells out, which is why reviews and exploratory testing matter.

---

## Knowledge Check

1. In your own words, what is a use case?
2. Name the three things that every use case needs to describe (hint: who, what, why).
3. What is the difference between an alternative flow and an exception flow?
4. Which part of a use case provides the expected results for your tests?
5. A use case has 1 main flow, 3 alternative flows, and 6 exception flows. Your tests cover the main flow, 2 alternatives, and 4 exceptions. What is the use-case coverage?
6. True or false: 100% use-case coverage means the system has no defects. Explain.
7. Give two kinds of defects that use-case testing is unlikely to find, and name the technique that suits each.
8. How are use cases, user stories, and test cases related?
9. In a use case diagram, what is the difference between include and extend?
10. Rewrite this step so that it is testable: "The system validates the input appropriately."
11. Map these to Given/When/Then: precondition, trigger and steps, postcondition.
12. Why should the "wrong email" and "wrong password" messages be identical in Login?

### Answers

1. A use case describes how an actor interacts with a system to achieve a goal, written as steps from the actor's point of view, including variations and failures.
2. The actor (who), the system and the interaction steps (what), and the goal (why).
3. An alternative flow is a valid variation that still leads to a successful or valid outcome (for example, "Remember me"). An exception flow is what happens when something goes wrong (invalid input, failure, refusal).
4. The postconditions (success and failure guarantees), together with the business rules and the step descriptions.
5. Flows total 10. Covered: 1 + 2 + 4 = 7. Coverage = 7 / 10 = 70%.
6. False. It only means that each flow was exercised at least once with the chosen data. Boundary values, combinations, state history, missing flows, and non-functional problems may still hide defects.
7. Boundary defects (use boundary value analysis), defects with many input classes (equivalence partitioning), combinations of conditions (decision tables), behaviour depending on history (state transition testing). Any two are acceptable.
8. A user story states the user's need briefly; a use case details the interaction with all flows; test cases verify each path of that interaction. One story may map to one or more use cases; one use case produces many test cases.
9. Include: the base use case always uses the included one (mandatory sharing). Extend: an optional use case adds behaviour under a condition.
10. For example: "The system checks that the email contains one @ and a domain, and that the password has 8 to 20 characters; if not, it shows the message 'Enter a valid email' or 'Password must be 8 to 20 characters' next to the field." (Any specific, observable rewrite is fine.)
11. Precondition = Given; trigger and steps = When; postcondition or expected result = Then.
12. If messages differ, an attacker can discover which emails are registered (account enumeration). It is a business rule that testers must verify.

---

## Try It: Pair Activity for Project 1

This activity is designed for your Thursday pair-programming session. Work in pairs, using a driver and navigator, and **swap roles** halfway.

**Part 1 (about 30 minutes): Analyse the Register use case**

1. Open the Project 1 Register page and walk through it yourselves once as a user.
2. Using the template in this lesson, write down a use case for **User Registration** based on what the app does today and what your requirements say. Include preconditions, trigger, main flow, at least 3 alternative flows, and at least 6 exception flows.
3. List business rules you discovered (field lengths, password policy, and so on). If something is unclear, write it as a question to the product owner.

**Part 2 (about 30 minutes): Derive scenarios and tests**

1. Build a scenario matrix (SC1, SC2, ...).
2. Write at least 12 test cases with ID, scenario, preconditions, data, steps, and expected results. Include at least two postcondition checks.
3. Calculate your use-case coverage and list anything not yet covered.

**Part 3 (about 20 minutes): Cross-review with the other pair**

1. Exchange documents with another pair.
2. Using the testability checklist, find missing exception flows and ambiguous steps in their use case.
3. Write your findings as questions, not accusations, and discuss.

**Part 4 (optional stretch): Automate**

Copy the Python model from this lesson, adapt the function to model Registration (duplicate email, weak password, mismatched confirmation), and write one test per scenario.

**Deliverable:** one shared document (or Jira test cases) containing the use case, scenario matrix, test cases, coverage, and a short list of review findings.

---

## Key Takeaways

- A **use case** describes how an actor and a system interact to achieve a goal; **use-case testing** derives black-box tests from those interactions.
- Know the anatomy: name/ID, actors, goal, preconditions, trigger, main flow, alternative flows, exception flows, postconditions, and business rules.
- A **user story** is a short statement of value, a **use case** is a detailed interaction, and a **test case** verifies one path.
- Use case diagrams show actors, system boundary, and **include** (always) and **extend** (optional) relationships.
- Derive tests: one for the main flow, one for each alternative flow, one for each exception flow, plus precondition and postcondition checks.
- A **scenario matrix** traces each path and links flows to conditions, data, and expected results; the **postconditions** are your oracle.
- **Use-case coverage = flows covered / total flows.** It is a useful measure, but it does not find boundary, combination, or state-history defects; complement it with BVA, EP, decision tables, and state transition testing.
- Use cases chain into **end-to-end** processes and are an excellent basis for **UAT**; **Given/When/Then** is an equivalent, lighter notation.
- Review use cases for testability: look for missing exception flows, vague words, missing returns, and missing failure postconditions.
- In Agile, acceptance criteria and scenarios on stories carry the same thinking.
- Avoid the common traps: testing only the happy path, vague expected results, and forgetting state checks.

---

## Additional Resources

- ISTQB Glossary (definitions of use case, use case testing, and related terms): https://glossary.istqb.org/
- Atlassian guide to user stories (useful for comparing stories with use cases): https://www.atlassian.com/agile/project-management/user-stories
- Visual Paradigm's guide to UML use case diagrams: https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-use-case-diagram/
- Cucumber's Gherkin reference (the Given/When/Then syntax): https://cucumber.io/docs/gherkin/reference/
- pytest documentation (for running the Python tests in this lesson): https://docs.pytest.org/
