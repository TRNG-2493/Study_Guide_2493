# User Stories and Acceptance Criteria

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **user story** is and why teams write requirements from the user's point of view.
- Write a user story in the standard **"As a... I want... so that..."** format.
- Apply the **INVEST** checklist to judge whether a story is good, and repair stories that fail it.
- Distinguish **acceptance criteria** from the story itself and from the general **Definition of Done**.
- Write acceptance criteria that are **specific, testable, and unambiguous**, in both rule-based (checklist) and example-based styles.
- Break a large story (an **epic**) into smaller stories using splitting techniques and vertical slices.
- Identify vague or untestable wording and rewrite it with numbers, lists, and exact messages.
- Run a complete three-amigos conversation on a story and record the outcome as rules, examples, and questions.
- Turn a story and its acceptance criteria into the starting point for Gherkin scenarios (the next lesson's topic).

---

## Why This Matters

In the BDD lesson you saw that the cycle starts with *Discovery*: a conversation about a piece of functionality. Before that conversation, someone has to **frame the piece of functionality**: who wants it, what they want, why they want it, and how we will know it is done. That framing is the **user story** and its **acceptance criteria**.

Stories and acceptance criteria are the inputs from which BDD scenarios are derived. If the input is vague ("The system should be fast and user friendly"), every downstream artifact (scenarios, step definitions, automated tests) will be vague too. Think of cooking: if the shopping list says "some vegetables and something for dinner", no cook, however skilled, can guarantee the family gets the meal they wanted. A precise list ("500 g potatoes, 2 onions, chicken thighs for a roast") makes the result predictable.

Test automation engineers are expected to **review stories and acceptance criteria early** and push back on anything that cannot be tested. That is one of the highest-value things a tester can do, because it prevents defects rather than finding them. A defect found while reading a story costs a sentence to fix. The same defect found in production costs a hotfix, a rollback, and an apology.

**Where you will use this:**

- **Today**, in the pair-programming three-amigos activity for **Project 2**: you will write stories and acceptance criteria for features of the practice site <https://www.saucedemo.com> before turning them into feature files and step definitions.
- **On the job**: stories live in tools such as Jira, Azure DevOps, or Trello. As an SDET you will be asked, "Is this story testable?" in almost every refinement meeting.
- **In your Project 2 report**: a clear traceability line from "story" to "scenario" to "automated test" demonstrates professional practice.

---

## The Concept

### 1. What Is a User Story?

A **user story** is a short, plain-language description of a feature **from the perspective of the person who wants it**. Stories came out of Agile methods such as Extreme Programming and Scrum, where they replaced long, rigid requirement documents.

The classic template:

> **As a** `<type of user>`,
> **I want** `<some goal or capability>`,
> **so that** `<benefit or value>`.

Example:

> As a **registered customer**,
> I want to **log in with my username and password**,
> so that **I can see my saved cart and place orders**.

Each part has a job:

| Part | Purpose | Weak example | Strong example |
|---|---|---|---|
| **As a** (role) | Who benefits; reminds us the feature is for a person | "As a user" (too vague) | "As a returning customer" |
| **I want** (goal) | What they want to *do*, not how the system will do it | "I want a dropdown with 5 items" (a solution) | "I want to sort products by price" |
| **So that** (benefit) | **Why** it matters; helps decide priority and alternatives | (missing) | "so that I can find affordable items quickly" |

The "so that" clause is often skipped, and it is the most valuable part: if nobody can say why the feature is wanted, maybe it should not be built.

> **A story is a promise for a conversation**, not a full specification. Ron Jeffries describes stories as the **3 Cs**: **Card** (a short written description), **Conversation** (the discussion that fills in the details), and **Confirmation** (the acceptance criteria/tests that prove it is done).

**Why "from the user's point of view"?** Old-style requirements said things like "The system shall validate the credentials." That sentence describes the system, not the person. It hides the question "validate for whom, and so that they can do what?" A story forces the writer to name a human and a goal. When a developer later has to choose between two designs, "which one serves the customer better?" is an easier question than "which one satisfies clause 4.2.1?".

**An analogy: the index card on the fridge.** A story is like a note on the fridge: "Dad: buy milk, so we can have breakfast tomorrow." The note is short, but it carries the person (Dad), the action (buy milk), and the reason (breakfast). If the shop is out of milk, Dad can use the reason to decide on an alternative (oat drink). A note that only says "milk" cannot guide him.

#### 1.1 Anatomy of a story, taken apart sentence by sentence

Take this story from an online shop:

> As a **returning customer**, I want to **save my shipping address**, so that **I do not have to type it again on my next order**.

- *As a returning customer*: Not "any user". A first-time visitor has nothing to save, so the role narrows the scope of the story.
- *I want to save my shipping address*: A goal expressed as an action. It does not say "a checkbox below the address form", which would be a solution.
- *so that I do not have to type it again on my next order*: The benefit. It tells the team the measure of success: fewer typing steps on the second order. It also suggests a simple test idea: place two orders and check the second address is prefilled.

#### 1.2 Roles: who are the "users"?

The role should be a real **type of person** (or system) who gets value. Examples for the Project 2 practice site:

| Role | Description |
|---|---|
| Standard customer | Logs in with `standard_user` and shops |
| Locked-out customer | A user whose account is blocked |
| Guest visitor | A person who has not logged in |
| Store administrator | Someone who manages products (may be out of scope for the site, but useful for practice) |

A role may be a **system** too ("As a payment gateway..."), but prefer human roles. If you can only write "As a developer, I want a database table...", you probably have a **task**, not a story (see Section 3).

#### 1.3 Good vs. bad: story rewrites

| Bad story | Why it is bad | Better story |
|---|---|---|
| "As a user, I want a login screen." | Describes a UI element, not a goal; no benefit | "As a registered customer, I want to log in, so that I can see my cart and place orders." |
| "As a customer, I want to use a dropdown with four sort options." | Dictates the solution (dropdown, four options) | "As a shopper, I want to sort products by price, so that I can find the cheapest first." |
| "As a developer, I want to create the `orders` table." | Technical task with no user value | "As a customer, I want my completed order to be recorded, so that I can view it later." (the table is a task inside this story) |
| "As a user, I want the system to be fast." | Not testable, no goal | "As a shopper, I want search results to appear within 2 seconds, so that I do not abandon the site." |
| "As a customer, I want to add, edit, remove items and apply coupons and check out." | Several stories glued together | Split into five stories (Section 3) |

### 2. The INVEST Checklist for Good Stories

Bill Wake's **INVEST** mnemonic gives six qualities of a well-formed story:

| Letter | Quality | Meaning | Violation example |
|---|---|---|---|
| **I** | **Independent** | Can be developed and delivered without depending on another story | "Checkout" cannot start until "Cart" is finished, with no way to separate them |
| **N** | **Negotiable** | Details are open for discussion; it is not a contract | A story that dictates the exact screen layout |
| **V** | **Valuable** | Delivers value to a user or the business | "Create the database table" (technical task, no user value) |
| **E** | **Estimable** | The team can roughly size it | "Make it work like Amazon" |
| **S** | **Small** | Fits in one iteration (days, not months) | "As a user I want a complete e-commerce site" |
| **T** | **Testable** | You can write tests that prove it works | "The page should be user friendly" |

**Testable** is the quality closest to your role: if you cannot think of a way to check it, the story is not ready.

#### 2.1 How to apply INVEST in a review (step by step)

When you receive a story, go through the letters like a pre-flight checklist:

1. **I**: "Could we ship this without finishing any other story first?" If the answer is no, can you reorder or combine?
2. **N**: "Does the text dictate a solution (a specific control, color, or technology)?" If so, ask for the underlying need.
3. **V**: "Who is better off when this ships?" If the answer is only "the developers", it is a task.
4. **E**: "Do we know enough to give a rough size?" If you are saying "it depends", write the unknowns as questions.
5. **S**: "Could we finish this in a few days?" If not, split.
6. **T**: "Can I write at least two concrete examples (one pass, one fail)?" If not, the story is not ready.

**A worked INVEST review.** Story: *"As a customer, I want to pay for my order and receive a confirmation email and get loyalty points and see a receipt PDF."*

| Letter | Finding |
|---|---|
| I | Loyalty points depend on a loyalty system that may not exist yet. Partly fails. |
| N | OK, no solution dictated. |
| V | OK, valuable overall. |
| E | Hard to estimate: four features in one. Fails. |
| S | Too big for one iteration. Fails. |
| T | Each part is testable, but together the story is large. Marginal. |

Result: split into "Pay for an order", "Receive an order confirmation email", "Earn loyalty points" (depends on a separate system, so a separate epic), and "Download a PDF receipt".

### 3. Epics, Stories, and Tasks

| Level | Size | Example |
|---|---|---|
| **Epic** | Weeks to months; too big for one iteration | "Customer account management" |
| **User story** | Days; deliverable in an iteration | "Customer can reset a forgotten password" |
| **Task** | Hours; technical work to implement a story | "Create `/reset` endpoint", "Write email template" |

(You have already met the word **Epic** in this course, as the weekly learning goal. The same idea: a large goal that is broken down into smaller deliverables.)

**Splitting large stories**, with some common techniques:

- **By workflow step:** "Browse products" -> "Add to cart" -> "Pay" -> "Receive confirmation".
- **By business rule / variation:** "Pay by card" and "Pay by gift certificate" separately.
- **By data type or input option:** "Search by name" and "Search by category" separately.
- **By simple vs. complex:** "Login with valid credentials" first; "Account lockout" later.
- **By happy path vs. exceptions:** deliver the main flow first, then error handling.

Aim for **vertical slices**: each story delivers something usable end to end (UI to database), not a horizontal layer ("build all the screens", then "build all the databases").

**Analogy: the layer cake.** A horizontal split is like serving the customer a layer of flour, then a layer of eggs, then a layer of sugar: nobody can taste anything until the end. A vertical slice is a thin wedge of the finished cake: small, but you can taste all the layers right away. A thin "log in and see the product list" slice delivers a usable result from the screen through to the data, so the team gets feedback early.

#### 3.1 Splitting walkthrough: "Customer account management" epic

Start with the epic. Ask: "What are the distinct things a customer does with their account?"

| Candidate story | Technique used |
|---|---|
| Customer can register with email and password | Workflow step (first step in lifecycle) |
| Customer can log in with valid credentials | Simple version first |
| Customer is refused after wrong password | Happy path vs. exception |
| Locked-out customer is blocked | Business rule |
| Customer can reset a forgotten password | Workflow step |
| Customer can update their shipping address | Data type |
| Customer can delete their account | Business rule (separate legal implications) |

Each one can be tested independently. They also suggest an order: registration and login first (the thinnest slice that delivers value), then exceptions, then convenience features.

**Tasks are not stories.** Within "Customer can reset a forgotten password" the team will create tasks like "build the reset-token table", "write the email template", and "add the `/reset` page". Tasks are for the team's planning; they do not need a "so that". If you notice you are writing a role like "As a developer, I want..." you are describing a task.

### 4. What Are Acceptance Criteria?

**Acceptance criteria (AC)** are the **conditions a story must satisfy** to be accepted by the business. They answer, "How will we know this story is done and correct?"

They:

- Define the **scope** and **boundaries** of the story (what is in, what is out).
- Give developers a clear target and testers a clear checklist.
- Form the basis of the BDD scenarios.

**Acceptance criteria vs. Definition of Done (DoD):**

| | Acceptance criteria | Definition of Done |
|---|---|---|
| Applies to | **One specific story** | **Every story** (team-wide standard) |
| Content | Functional behavior specific to this story | Quality steps: code reviewed, unit tests pass, documentation updated, deployed to test environment |
| Example | "A locked-out user sees an error message" | "All automated regression tests pass" |

**Analogy: a restaurant order versus the kitchen's hygiene rules.** The customer's order ("steak, medium-rare, no mushrooms") is the acceptance criteria: specific to this plate. The kitchen's rules ("clean hands, correct temperature, no cross-contamination") are the Definition of Done: they apply to every plate. A plate can match the order perfectly and still be rejected if hygiene rules were broken, and a perfectly clean plate is useless if it is the wrong dish. You need both.

**Where do acceptance criteria live?** Usually in the story ticket (Jira description or a dedicated field), written during or right after the three-amigos meeting. In BDD teams the criteria then become scenarios in the `.feature` file so the criteria and the tests are the same text.

### 5. Two Styles of Acceptance Criteria

#### Style 1: Rule-oriented (checklist)

A list of statements; each is a **rule** that must be true:

```
Story: As a registered customer, I want to log in, so that I can see my cart.

Acceptance criteria:
1. A user with valid credentials is taken to the products page.
2. A user with an incorrect password sees the message "Username and password do not match any user in this service".
3. A locked-out user sees the message "Sorry, this user has been locked out."
4. Username and password are both required; leaving either empty shows a "... is required" message.
5. The password field masks the characters typed.
```

Pros: quick to write, easy to scan. Cons: can hide ambiguity ("what exactly happens if both are empty?"), which is why teams add examples.

#### Style 2: Scenario-oriented (Given / When / Then)

Each criterion is written as a concrete example. This is exactly the BDD format and is covered in detail in the *Gherkin* and *Given/When/Then* lessons:

```
Scenario: Locked-out user cannot log in
  Given a locked-out user exists
  When that user attempts to log in with the correct password
  Then an error message "Sorry, this user has been locked out." is shown
  And the user remains on the login page
```

Pros: precise, testable, executable. Cons: longer; too many scenarios for trivial rules become noise.

Many teams use **both**: rule-oriented AC to capture the rules, with one or more examples per rule to pin down edge cases (this is the "example mapping" structure: rules in blue, examples in green).

**Reading the scenario line by line** (a first look; the Gherkin lesson goes deeper):

| Line | Meaning |
|---|---|
| `Scenario: Locked-out user cannot log in` | The name of this one example; it states the behavior being checked |
| `Given a locked-out user exists` | The starting situation: a user whose account is locked is available |
| `When that user attempts to log in with the correct password` | The action; we deliberately use the *correct* password so that the only reason to fail is the lock |
| `Then an error message "..." is shown` | The expected result, with the exact text |
| `And the user remains on the login page` | A second expected result; `And` continues the previous keyword (`Then`) |

#### 5.1 Converting a criterion into a scenario, step by step

Take criterion 3: *"A locked-out user sees the message 'Sorry, this user has been locked out.'"*

1. **Find the situation.** What must be true before? "A locked-out user is trying to log in" gives the `Given`.
2. **Find the trigger.** What does the user do? "Submits the login form with a valid password" gives the `When`.
3. **Find the outcome.** What can be observed? "The error message appears" gives the `Then`.
4. **Check for hidden rules.** "And they are not logged in" (user remains on the login page) gives an extra `Then`/`And`.
5. **Name it.** Give the scenario a title that states the behavior: "Locked-out user cannot log in".

Repeat for each criterion. If a criterion produces more than one `When`, it is probably two criteria glued together.

### 6. Qualities of Good Acceptance Criteria

| Quality | Meaning | Bad | Good |
|---|---|---|---|
| **Specific** | Exact behavior and values | "Shows an error" | "Shows the message 'Epic sadface: Username is required'" |
| **Testable** | Pass/fail can be decided objectively | "The page loads quickly" | "The product list appears within 3 seconds on a standard test environment" |
| **Unambiguous** | One interpretation only | "Appropriate discount applied" | "A 10% discount applies to orders of $100 or more" |
| **User-focused** | Describes observable behavior, not implementation | "The `users` table has a `locked` column" | "A locked-out user cannot log in" |
| **Independent / atomic** | One condition per criterion | "User can add, edit, and delete items" | Three separate criteria |
| **Complete** | Includes positive, negative, and boundary cases | Only the happy path | Also invalid input, empty values, limits |

**The "two testers" test.** Give a criterion to two different testers. If they could write two different tests that both honestly satisfy it, the criterion is ambiguous. "Appropriate discount applied": one tester checks 5%, the other 20%, both think they are right. "A 10% discount applies to orders of $100 or more" has only one reading.

**Boundary thinking.** Whenever a criterion contains a number, immediately ask about the **boundary**: the value exactly at the number, one below, and one above. For "free shipping for orders of $50 or more", test 49.99, 50.00, and 50.01. Most defects hide at boundaries because developers and business people disagree about "more than" versus "at least".

### 7. Words That Should Make You Suspicious

When reviewing stories, watch for **vague, untestable words**:

| Vague word | Ask |
|---|---|
| fast, quick, responsive | "How fast? Measured how, under what load?" |
| user friendly, intuitive, easy | "What can a user do in how many steps, with what success rate?" |
| appropriate, suitable, as needed | "Which exact value or behavior?" |
| etc., and so on | "List all of them." |
| should handle errors | "Which errors, and what should the user see?" |
| support multiple browsers | "Which browsers and versions?" |
| secure | "Which specific protections: password rules, lockout, encryption?" |

Turning vague terms into **numbers, lists, and exact messages** is a central test-engineering skill.

#### 7.1 Rewriting drill with answers

| Vague criterion | Questions to ask | Rewritten criterion |
|---|---|---|
| "The login page should be secure." | Which threats? Which protections? | "The password field masks characters. After 5 failed attempts within 10 minutes the account is locked for 15 minutes. Passwords are never shown in URLs." |
| "Errors should be shown appropriately." | Which errors? Where? In what words? | "An empty username shows 'Username is required' above the form, in red, and the cursor stays on the login page." |
| "The checkout should be quick." | Which part of checkout? How many steps? | "A logged-in customer with items in the cart can complete checkout in at most 3 screens (information, overview, confirmation)." |
| "The system supports various payment types." | Which? | "Payment by Visa, Mastercard, or gift certificate is supported. Other types are out of scope." |
| "Users can search for products easily." | What is easy? | "Typing at least 3 characters in the search box lists all products whose name contains those characters, case-insensitive." |

### 8. Worked Example: From Story to Criteria

**Story:** As a shopper, I want to sort the product list by price, so that I can find the cheapest items first.

**Questions asked during discovery (the three amigos):**

- Which sort options exist? (Name A-Z, Name Z-A, Price low-high, Price high-low.)
- What is the default order? (Name A-Z.)
- Does the sort persist if I navigate away and come back? (Business: not required in this release.)
- Are products with the same price ordered in any particular way? (Keep the default name order.)
- What about out-of-stock items? (They appear in normal order, marked as unavailable.)

**Acceptance criteria produced:**

1. The product list can be sorted by: Name (A to Z), Name (Z to A), Price (low to high), Price (high to low).
2. The default sort is Name (A to Z).
3. When "Price (low to high)" is selected, products appear in ascending price order.
4. When "Price (high to low)" is selected, products appear in descending price order.
5. Changing the sort option does not change which products are listed, only their order.
6. Products with identical prices are listed in name order (A to Z).
7. *Out of scope for this story:* remembering the selected sort after leaving the page.

Notice criterion 7: explicitly stating **what is out of scope** prevents arguments later.

These criteria already look like scenarios waiting to be written; in the next lessons we will convert them to Gherkin.

### 9. Non-Functional Acceptance Criteria

Acceptance criteria are not limited to functionality. They can also express quality attributes, but must still be **measurable**:

- **Performance:** "Search results are displayed within 2 seconds for catalogs up to 10,000 products."
- **Accessibility:** "All form fields have visible labels; the page can be used with keyboard only."
- **Security:** "After 5 failed login attempts the account is locked for 15 minutes."
- **Compatibility:** "Works on the latest two versions of Chrome, Firefox, and Edge."

Not every non-functional criterion belongs in a Gherkin scenario; some are better checked with specialized tools. The point is that they are written down and testable.

**Connection to Selenium.** You already know how to run the same Selenium test on different browsers. A compatibility criterion such as "works on Chrome and Firefox" is exactly what that capability exists to check, so such a criterion maps to a *configuration* of your framework rather than to many different scenarios.

### 10. Who Writes What?

| Item | Typically written by | Reviewed by |
|---|---|---|
| User story | Product owner / business analyst | Whole team |
| Acceptance criteria | Product owner with the team (often at the three-amigos meeting) | Developers, testers |
| Scenarios | Tester or developer, **with** the product owner's confirmation | Three amigos |
| Step definitions | Developers / automation engineers | Peers |

As the automation engineer, you will **challenge** stories ("Which error message exactly?") and **draft** scenarios for the others to confirm.

### 11. A Complete Three-Amigos Walkthrough: Checkout on an E-Commerce Site

This section follows one story from first draft to the criteria and scenario drafts that come out of a real-style conversation. The application is the Project 2 practice shop <https://www.saucedemo.com>, whose checkout flow has three stages: **Your Information** (first name, last name, postal code), **Overview** (items, price total, tax), and **Complete** ("Thank you for your order!").

**Participants:**

- **Dana**, product owner (business amigo)
- **Luis**, developer (development amigo)
- **Mei**, test automation engineer (testing amigo, this is your role)

**The draft story, as Dana first wrote it:**

> As a customer, I want to checkout, so that I can get my stuff.

**Step 1: Mei reviews the story before the meeting (INVEST).** She notes:

- Role "customer" is acceptable but could be more precise ("logged-in customer with items in the cart").
- "I want to checkout" is a goal but not a detail; "get my stuff" is a weak benefit.
- Testable? Not yet: "checkout" has no end condition.

Dana and Mei agree on a rewrite before the meeting:

> As a **logged-in customer with items in my cart**,
> I want to **provide my delivery details and confirm my order**,
> so that **the shop can ship my items to me**.

**Step 2: The meeting opens.** Dana reads the story. The facilitator (Mei) writes it on the yellow card. Then she asks for rules.

**Step 3: Rules (blue cards) from Dana:**

1. The customer must provide first name, last name, and postal code.
2. The customer sees an order overview with item total, tax, and grand total before confirming.
3. After confirming, the customer sees a confirmation message and the cart is emptied.
4. The customer can cancel at any stage and go back.

**Step 4: Examples (green cards) per rule.** Mei asks "Can you give me a concrete example for each?" and Luis joins in.

| Rule | Example |
|---|---|
| 1. Required details | Customer enters "Ana", "Silva", "12345": continues to the overview. |
| 1. Required details | First name empty, others filled: error "First Name is required". |
| 1. Required details | Last name empty: error "Last Name is required". |
| 1. Required details | Postal code empty: error "Postal Code is required". |
| 2. Overview | Cart contains Backpack (29.99) and Bike Light (9.99): item total 39.98. |
| 3. Confirmation | After "Finish", message "Thank you for your order!" is displayed and the cart badge disappears. |
| 4. Cancel | Pressing Cancel on the information page returns to the cart with items still there. |

**Step 5: Questions and edge cases (red cards).** Mei asks "what if" questions; Luis adds technical ones.

| Asked by | Question | Answer or status |
|---|---|---|
| Mei | What if the cart is empty and the customer opens the checkout page directly? | Unknown. Red card. |
| Mei | Are numbers allowed in the name fields? | Dana: "Not worried in this release." Out of scope, noted. |
| Luis | Is tax calculated by the site or fetched from a tax service? | Dana: "We use a fixed 8% in this release." Answered. |
| Mei | What is the order of validation when several fields are empty? | Unknown. Red card. (Observation from the site: it reports the first missing field, in the order First Name, Last Name, Postal Code.) |
| Luis | What if the customer double-clicks Finish? | Dana: "We must not create two orders." Becomes a new rule. |

**Step 6: The outcome.** The table now has 5 rules, 8 examples, and 2 red cards. Dana takes the red cards. Mei has a ready list for scenarios. The group agrees the story is small enough, since it has 5 rules, but notices that "cancel" (rule 4) could be its own story. They keep it in because it is small.

**Step 7: Mei writes the acceptance criteria (rule-oriented style) after the meeting:**

```
Story: Provide delivery details and confirm an order

AC1. The customer must provide First Name, Last Name, and Postal Code to continue.
AC2. If First Name is empty, the message "Error: First Name is required" is displayed.
AC3. If Last Name is empty, "Error: Last Name is required" is displayed.
AC4. If Postal Code is empty, "Error: Postal Code is required" is displayed.
AC5. The overview page shows the item total, tax (8%), and total.
AC6. After the customer confirms, "Thank you for your order!" is displayed and the cart is empty.
AC7. Cancel on the information page returns the customer to the cart with the items unchanged.
AC8. Confirming twice (double click) creates only one order.
Out of scope: validation of the characters in the name fields.
Open questions: behavior with an empty cart; order of validation messages.
```

**Step 8: Mei drafts scenarios from the criteria.**

```gherkin
Feature: Checkout
  As a logged-in customer with items in my cart
  I want to provide my delivery details and confirm my order
  so that the shop can ship my items to me

  Scenario: Customer completes checkout with all details
    Given the customer has the "Sauce Labs Backpack" in the cart
    When the customer checks out with first name "Ana", last name "Silva" and postal code "12345"
    And the customer confirms the order
    Then the customer sees the confirmation message "Thank you for your order!"

  Scenario: Checkout is refused when the first name is missing
    Given the customer has the "Sauce Labs Backpack" in the cart
    When the customer checks out without entering a first name
    Then the customer sees the error "Error: First Name is required"
```

**Line by line:**

- `Feature: Checkout` names the capability. The three indented lines below it are **free-text description**; they carry the story into the feature file so the story and its tests live together.
- `Scenario: Customer completes checkout with all details` is one example (the happy path from AC1, AC5-AC6).
- `Given the customer has the "Sauce Labs Backpack" in the cart`: the starting context. We describe *what must be true* ("the cart contains this product"), not how to achieve it (log in, find the product, click add). Step definitions will handle the clicks.
- `When the customer checks out with first name "Ana", last name "Silva" and postal code "12345"`: the main action, with the example data visible in the text.
- `And the customer confirms the order`: a second action in the same flow. `And` means "same keyword as the line above" (here, `When`).
- `Then the customer sees the confirmation message "..."`: the observable outcome.
- The second scenario covers AC2 and uses a similar structure with an error as the outcome.

Mei will bring these to Dana and Luis for confirmation. The scenarios for AC3, AC4 can be added the same way; AC8 (double-click) might become a scenario at a different level or be tested lower down, which the team will decide in refinement.

**What made this session work:** the draft story was fixed *before* the meeting; each rule received examples; unknowns became red cards rather than guesses; the criteria include exact messages and an explicit out-of-scope line.

### 12. More Worked Stories (Banking and Booking)

Seeing the story-to-criteria move in different domains helps you apply it to new work. Each below shows a story, a rule-style AC list, and one derived scenario.

#### 12.1 Banking: withdraw cash

**Story:** As an account holder, I want to withdraw cash from an ATM, so that I can pay for things that do not accept cards.

**Acceptance criteria:**

1. The withdrawal amount must be a multiple of 10.
2. The withdrawal must not exceed the available balance.
3. The daily withdrawal limit is 500.00 per account.
4. After a successful withdrawal the balance decreases by exactly the amount withdrawn.
5. If the withdrawal is refused, the balance does not change and the reason is shown.

**Boundaries to ask about:** a balance of exactly 100 with a request for 100 (allowed), a request for 105 (not a multiple of 10), a request that would bring the daily total to exactly 500 (allowed) or 510 (refused).

**Derived scenario:**

```gherkin
Scenario: Withdrawal larger than the balance is refused
  Given the account holder has a balance of 100.00
  When the account holder withdraws 150.00
  Then the withdrawal is refused with the message "Insufficient funds"
  And the balance remains 100.00
```

#### 12.2 Booking: reserve a hotel room

**Story:** As a traveller, I want to reserve a room for specific dates, so that I am sure to have somewhere to stay.

**Acceptance criteria:**

1. The check-out date must be after the check-in date.
2. The check-in date cannot be in the past.
3. A room that is already reserved on any night of the stay cannot be reserved.
4. The total price equals the nightly rate multiplied by the number of nights.
5. After the reservation, a confirmation number is shown.

**Derived scenario:**

```gherkin
Scenario: Total price is the nightly rate times the number of nights
  Given a room costs 120.00 per night
  When the traveller reserves the room for 3 nights
  Then the total price shown is 360.00
```

**Observe the pattern across all three domains:** each story has a role, a goal, and a benefit; the criteria contain concrete numbers, exact messages, and at least one boundary; and each criterion maps straight to a scenario.

### 13. Common Writing Patterns for Acceptance Criteria

| Pattern | Template | Example |
|---|---|---|
| Positive rule | "When X, then Y happens" | "When the customer adds a product, the cart badge increases by one." |
| Negative rule | "X is not allowed; the user sees Z" | "A quantity of 0 is not allowed; the user sees 'Quantity must be at least 1'." |
| Boundary | "At exactly N the behavior is..." | "An order of exactly $50.00 qualifies for free shipping." |
| State | "While in state S, X is true" | "While the account is locked, login is refused." |
| Out of scope | "Not included: ..." | "Not included: remembering the sort order." |

Writing criteria with these patterns keeps them atomic and makes them quick to convert into scenarios.

---

## Hands-On Guided Lab: From Vague Requirement to Criteria to Scenario Draft

**Goal:** Practice moving through the full chain (story, INVEST review, criteria, scenario) on a real feature of the Project 2 practice site.

**Time:** 45 minutes. **Prerequisite:** a browser and a text editor. No Java code is needed.

**Steps:**

1. **Open the site.** Go to <https://www.saucedemo.com> and log in with `standard_user` / `secret_sauce`.
2. **Receive the vague requirement.** Your product owner says: *"People need to be able to remove things from the cart."* Write it at the top of a new text file called `remove-from-cart.md`.
3. **Write the story.** Complete the template:
   ```
   As a shopper with items in my cart,
   I want to remove an item,
   so that I only buy what I really want.
   ```
4. **Run the INVEST review.** For each letter write "OK" or a problem. Expect: Small and Estimable pass; ask whether Independent holds (it depends on the "add to cart" story being finished).
5. **Explore the application to gather facts.** Add the Backpack and the Bike Light. Open the cart. Click **Remove** on the Backpack. Observe: what happens to the cart badge? What happens to the item list? What happens if you remove the last item? Write each observation as a candidate fact.
6. **Write the acceptance criteria.** Aim for five to seven, using the patterns of Section 13. A sample result:
   ```
   AC1. Each item in the cart has a Remove button.
   AC2. Removing an item deletes it from the cart list.
   AC3. The cart badge shows the number of items remaining.
   AC4. When the last item is removed, the cart badge disappears.
   AC5. Removing one item does not affect the other items.
   Out of scope: undoing a removal.
   ```
7. **Write two questions** you would take to the three amigos (for example, "Should we ask for confirmation before removal?" and "Does removal on the products page behave the same as on the cart page?").
8. **Draft a scenario for AC2 and AC3.**
   ```gherkin
   Scenario: Removing an item updates the cart
     Given the shopper has the "Sauce Labs Backpack" and the "Sauce Labs Bike Light" in the cart
     When the shopper removes the "Sauce Labs Backpack" from the cart
     Then the cart contains only the "Sauce Labs Bike Light"
     And the cart badge shows 1
   ```
9. **Check your scenario.** Does it avoid locators? Does it name concrete values? Does it have a single `When`? Fix anything that does not.

**Expected output:** a text file with one story, an INVEST table, 5-7 acceptance criteria with an out-of-scope line, two open questions, and one drafted scenario. If you can hand the file to a colleague and they could manually verify every criterion in the browser without asking you anything, the criteria are testable.

---

## Troubleshooting: Problems You Will Meet with Stories and Criteria

| Symptom | Likely cause | What to do |
|---|---|---|
| Developers and testers interpret a criterion differently | It is ambiguous | Add a concrete example with real values; apply the "two testers" test |
| A story keeps growing during the sprint | Scope was never stated | Add an explicit "Out of scope" list; split the story |
| You cannot write a single test for a story | The story is not testable | Ask for acceptance criteria with measurable outcomes; push back in refinement |
| Criteria read like implementation ("a `locked` column") | Written from the developer's view | Rewrite in terms of observable behavior |
| Too many criteria (more than about 10) | Story is too big | Split by rule or workflow step |
| Criteria and scenarios disagree after a while | They were copied, not shared | Keep scenarios as the single source of truth once they exist |
| Nobody can say what the "so that" is | The value is unclear | Park the story; ask the product owner why it matters |

---

## Common Mistakes

1. **Writing solutions instead of needs.** "I want a red button" is a design decision, not a goal.
2. **Skipping "so that".** Without the benefit, the team cannot judge alternatives or priority.
3. **Using "As a user" everywhere.** Different users have different needs; name the role.
4. **Mixing several stories in one.** "Add, edit, delete" is three stories.
5. **Leaving words like "appropriate" or "fast" in criteria.** Always replace them with numbers and exact messages.
6. **Only describing the happy path.** Include invalid input, empty values, and boundaries.
7. **Forgetting out-of-scope statements.** Unstated scope becomes an argument later.
8. **Confusing acceptance criteria with the Definition of Done.** Criteria are per story; the DoD is team-wide.
9. **Writing acceptance criteria after the code is built.** Then they only describe what was built, not what was needed.

---

## Code Example: Keeping Stories Next to the Tests

Cucumber lets you put the story text directly in the feature file's description, so that the specification stays together with the tests (covered in the *Features and Scenarios* lesson). A preview:

```gherkin
Feature: Sort products
  As a shopper
  I want to sort the product list by price
  so that I can find the cheapest items first

  Rule-of-thumb notes (free text is allowed here):
  - Default order is Name (A to Z)

  Scenario: Sort by price from low to high
    Given the shopper is on the products page
    When the shopper sorts the products by "Price (low to high)"
    Then the products are listed from the cheapest to the most expensive
```

The first lines after `Feature:` are free-text description (ignored by Cucumber's execution but read by humans), and each acceptance criterion becomes one or more scenarios. We study the exact syntax in the next lessons.

**Line-by-line:**

- `Feature: Sort products` is the title.
- The three lines `As a shopper / I want ... / so that ...` are the story, kept as description text.
- The "Rule-of-thumb notes" line and the bullet are free text. Cucumber ignores them when running, but they keep context handy for humans.
- `Scenario: Sort by price from low to high` turns criterion 3 of Section 8 into an example.
- `Given`, `When`, `Then` give context, action, outcome.
- The quoted text `"Price (low to high)"` is data that a step definition will receive as a parameter (the Step Definitions lesson shows how).

**Traceability.** Many teams put the ticket number into the feature title or description (for example `Feature: Sort products (SHOP-142)`) so each scenario can be traced back to its story.

---

## Practice Exercises

1. **Write stories.** Write user stories (with a role, goal, and benefit) for: (a) adding a product to a cart, (b) removing a product from a cart, (c) completing a checkout with shipping information, (d) logging out.
2. **INVEST review.** Evaluate this story against INVEST and rewrite it: *"As a user, I want a fast, modern, easy-to-use, fully integrated platform with every feature our competitors offer."*
3. **Repair vague criteria.** Rewrite these into testable criteria:
   - "The login page should be secure."
   - "Errors should be shown appropriately."
   - "The checkout should be quick."
4. **Split the epic.** Split the epic "Customer account management" into at least six independent stories, using at least three different splitting techniques. Name the technique used for each.
5. **Acceptance criteria drill.** For the story *"As a shopper, I want to add items to my cart, so that I can buy several things at once"* write at least seven acceptance criteria that cover: the happy path, a boundary (empty cart, maximum quantity), a negative case, and one explicit out-of-scope item.
6. **Ask the questions.** For the story "As an admin, I want to lock a user's account", list ten clarifying questions you would ask in the three amigos meeting.
7. **Project 2 prep.** For your Project 2 target application, write three user stories with acceptance criteria. These become raw material for today's pair-programming exercise.
8. **Role or task?** Decide whether each item is a story or a task and fix it if needed: (a) "As a developer, I want to upgrade the Selenium library", (b) "As a customer, I want to see my order history", (c) "Add an index to the orders table".
9. **Boundary hunt.** The criterion says "Free shipping applies to orders of $50 or more." List the boundary values you would test and the expected result of each.
10. **Criteria to scenarios.** Convert criteria AC2 and AC3 of the Section 8 sort story into two Gherkin scenarios (Given, When, Then). Use only keywords and ideas introduced so far.
11. **Definition of Done vs. AC.** Sort these into "acceptance criteria" or "Definition of Done": (a) "Code has been peer reviewed", (b) "A locked-out user sees an error", (c) "All regression scenarios pass in the pipeline", (d) "The discount is 10% for orders of $100 or more".
12. **Full mini three-amigos.** With a partner, take the story "As a shopper, I want to log out, so that nobody else can use my account on a shared computer". Hold a 15-minute session with roles (business, tester, developer). Produce: at least three rules, five examples, two questions, and a draft of acceptance criteria.

---

## Solutions and Hints

**1. Write stories.** (a) As a shopper, I want to add a product to my cart, so that I can buy it together with other items. (b) As a shopper, I want to remove a product from my cart, so that I only pay for what I still want. (c) As a customer with items in my cart, I want to enter my delivery details and confirm the order, so that the shop can ship it. (d) As a logged-in customer, I want to log out, so that nobody else can use my account on a shared computer. Hint: check each has a named role and a real benefit.

**2. INVEST review.** Fails Independent (everything at once), Estimable (no scope), Small (huge), Testable ("fast, modern, easy" are vague), and Valuable is unclear. Rewrite by choosing a single need, for example: "As a shopper, I want search results to appear within 2 seconds, so that I can compare products without waiting."

**3. Repair vague criteria.** See Section 7.1 for model answers. Hint: every rewrite should contain a number, a list, or an exact message.

**4. Split the epic.** See the table in Section 3.1. Any six independent stories with a named technique are acceptable.

**5. Acceptance criteria drill.** Sample: (1) Adding an item increases the cart count by one. (2) The added item appears in the cart with its name and price. (3) Adding two different items shows both. (4) Maximum quantity per item is 10; attempting an 11th shows "Maximum quantity is 10". (5) An empty cart shows "Your cart is empty". (6) An item already in the cart is shown as added; a second click does not duplicate it. (7) Out of scope: saving the cart for later sessions.

**6. Ask the questions.** Sample: Who can lock accounts? Is there a reason that must be recorded? Does the user get notified? What happens to a user currently logged in? Can a locked account be unlocked, and by whom? Is locking reversible automatically after a time? What message does the locked user see? Are admins themselves lockable? Is the action logged for audit? Does the lock apply to all devices and sessions?

**7. Project 2 prep.** Check each story against INVEST and each criterion against the "two testers" test.

**8. Role or task?** (a) Task (a technical upgrade with no user value); keep it in the backlog as a task. (b) Story. (c) Task; it belongs inside a story such as "customer sees order history".

**9. Boundary hunt.** 49.99: shipping charged. 50.00: free (the criterion says "or more"). 50.01: free. Also consider 0.00 and a very large order. Hint: confirm the boundary rule with the product owner.

**10. Criteria to scenarios.**

```gherkin
Scenario: Products can be sorted from the lowest price to the highest
  Given the shopper is on the products page
  When the shopper sorts the products by "Price (low to high)"
  Then the cheapest product is listed first and the most expensive product is listed last

Scenario: Products can be sorted from the highest price to the lowest
  Given the shopper is on the products page
  When the shopper sorts the products by "Price (high to low)"
  Then the most expensive product is listed first and the cheapest product is listed last
```

**11. DoD vs. AC.** (a) DoD. (b) AC. (c) DoD. (d) AC.

**12. Full mini three-amigos.** Sample rules: logging out ends the session; after logout the customer lands on the login page; pressing the browser Back button after logout must not show the products page. Sample questions: "Should the cart be kept for the next login?" "What if the session expired by itself?" Sample AC: "After logout the login page is displayed", "After logout, navigating back to the products page redirects to the login page."

---

## Self-Check Questions

1. **What are the three parts of a user story, and which one is most often skipped?** Role (As a), goal (I want), benefit (so that); the benefit is most often skipped.
2. **What do the 3 Cs stand for?** Card, Conversation, Confirmation.
3. **What does INVEST stand for?** Independent, Negotiable, Valuable, Estimable, Small, Testable.
4. **How do acceptance criteria differ from the Definition of Done?** Acceptance criteria apply to one story and describe its specific behavior; the Definition of Done applies to all stories and describes team-wide quality steps.
5. **Why is "The system should be fast" a poor criterion, and how do you repair it?** It is not measurable; replace it with a number and a context, for example "Search results appear within 2 seconds."
6. **What is a vertical slice?** A small piece of functionality that works end to end (UI through data), as opposed to a horizontal layer such as "all the screens".
7. **Why state "out of scope" in acceptance criteria?** To prevent unstated expectations and scope creep.
8. **How does one acceptance criterion become a scenario?** Find the starting situation (Given), the action (When), and the observable outcome (Then), and give the scenario a name that states the behavior.

---

## Summary

- A **user story** captures a need from the user's perspective: **As a ... I want ... so that ...**; the "so that" gives the value. A story is a **promise for a conversation** (Card, Conversation, Confirmation).
- Good stories follow **INVEST**: Independent, Negotiable, Valuable, Estimable, Small, Testable. Use it as a checklist when reviewing.
- **Epics** are split into stories by workflow step, rule, data variation, simple-vs-complex, or happy-vs-exception paths; prefer **vertical slices**. Tasks are technical work inside a story.
- **Acceptance criteria** define when a story is done for *that* story; the **Definition of Done** is the team-wide quality standard.
- Good criteria are **specific, testable, unambiguous, user-focused, atomic, and complete**, and state **out-of-scope** items explicitly.
- Replace vague words ("fast", "appropriate", "etc.") with **numbers, lists, and exact messages**, and always think about **boundaries**.
- A three-amigos session turns a story into rules, examples, and questions; the tester's role is to ask "what if" and to push for testable wording.
- Acceptance criteria written as examples lead directly to **Gherkin scenarios**, the subject of the next lesson. For Project 2 you will write stories and criteria for saucedemo.com features first, then scenarios and step definitions.

---

## Additional Resources

- Atlassian Agile Coach, *User Stories*: https://www.atlassian.com/agile/project-management/user-stories
- Cucumber documentation, *Writing better Gherkin / Example Mapping*: https://cucumber.io/docs/bdd/example-mapping/
- Mike Cohn, *User Stories Applied* overview at Mountain Goat Software: https://www.mountaingoatsoftware.com/agile/user-stories
- Cucumber documentation, *Better Gherkin*: https://cucumber.io/docs/bdd/better-gherkin/
