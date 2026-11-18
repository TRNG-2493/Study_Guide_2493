# Cucumber In-Class Handout 1: BDD and Writing Features

**Topics:** 1.1 BDD fundamentals · 1.2 User stories and acceptance criteria · 1.3 Gherkin · 1.4 Features and scenarios

**How to use this handout:** the same layout as the Selenium handouts. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**This handout is about writing, not code.** You learn what BDD is, turn a requirement into rules and examples, and write them as a **feature file** in Gherkin. Cucumber Handout 2 connects that file to Java and Selenium.

**The Cucumber handouts at a glance**

| Handout | What you learn | You build |
|---|---|---|
| 1 | BDD, user stories, Gherkin, feature files | `login.feature` |
| 2 | Cucumber setup and step definitions | `LoginSteps` (plain Selenium) |
| 3 | Scenario Outline, Background, Rule, hooks | outlines, `sorting.feature`, `SortSteps`, `Hooks` |
| 4 | Tags, JUnit, Maven, reports | tags, suites, reports |
| 5 | **Putting it together** (self-study): page objects | the same project, refactored, plus `cart.feature` |

**Practice site:** Swag Labs, `https://www.saucedemo.com`. Every user has the password `secret_sauce`:

| User | What happens |
|---|---|
| `standard_user` | Logs in normally |
| `locked_out_user` | Refused: *Epic sadface: Sorry, this user has been locked out.* |
| `problem_user`, `visual_user`, `error_user` | Log in, but parts of the shop are deliberately broken |
| `performance_glitch_user` | Logs in, but **slowly** |

**User stories used in the Cucumber handouts:**

```text
SL-101  As a registered shopper
        I want to log in with my username and password
        So that I can see the products

SL-102  As a logged-in shopper
        I want to log out
        So that nobody else can use my session

SL-104  As a shopper
        I want to sort products by price or name
        So that I can find what I want quickly
```

---

## 1.1 BDD Fundamentals

### Definition

**Behaviour-Driven Development (BDD)** is a way of building software in which the team agrees how the system should **behave** by discussing **concrete examples** in a **shared, plain language** before the code is written, and then uses those examples to check the result automatically. It was described by Dan North in 2006, as a development of Test-Driven Development (TDD). BDD has three practices that repeat for every user story: **Discovery** (talk through examples together), **Formulation** (write them down as structured scenarios) and **Automation** (make the scenarios run against the real system). BDD is a way of working, not a tool; **Cucumber** is the most widely used tool that supports it.

### Key terms

| Term | Meaning |
|---|---|
| **Behaviour** | What the system does, seen from outside by a user. Not how the code is written. |
| **Example** | One concrete case with real values: "`locked_out_user` logs in → sees *Sorry, this user has been locked out.*" |
| **Rule** | A general statement that one or more examples illustrate: "Locked-out users cannot log in." |
| **Three Amigos** | The three viewpoints that discuss a story: **business** (product owner), **development** and **testing** |
| **Shared (ubiquitous) language** | The same words used by everyone, in conversation, stories, scenarios and code: *shopper*, *products*, *log in* |
| **Living documentation** | Scenarios that describe the system **and** are run as tests, so they can't silently go out of date |
| **TDD** | Test-Driven Development: developers write a failing unit test, then the code that makes it pass |
| **ATDD** | Acceptance Test-Driven Development: acceptance tests are agreed before development; BDD is a form of it |

**The three practices:**

| Practice | Question | Who | Output |
|---|---|---|---|
| **Discovery** | What could it do? | Three Amigos | Rules, examples, open questions |
| **Formulation** | How do we write it down? | Usually tester + developer | Gherkin scenarios in `.feature` files |
| **Automation** | How do we check it? | Developer / QE | Code that runs each scenario (Cucumber + Selenium) |

**BDD tools:** Cucumber (Java, JavaScript, Ruby), Reqnroll / SpecFlow (.NET), Behave (Python). They all read the same plain-language format, **Gherkin**.

### Key ideas

- **Examples beat rules.** Everyone agrees with "invalid logins are refused"; only examples show *which* message each case gets.
- **Discovery comes first.** Most of BDD's value comes from conversations that catch misunderstandings before coding.
- Installing Cucumber is **not** doing BDD. Without the conversations, it is just a longer way to write tests.

### Worked example: from a vague requirement to rules and examples (SL-101)

**Step 1: Start with the requirement as it was given.**

```text
"Only valid users can log in."
```

Ask: what does *valid* mean? What happens to everyone else?

**Step 2: Split it into rules** (what the Three Amigos agreed).

```text
Rule 1: A known user with the correct password sees the products.
Rule 2: A locked-out user is refused, with a message saying so.
Rule 3: A wrong password is refused, with a message saying so.
```

**Step 3: Give each rule at least one concrete example** with real values.

| Rule | Username | Password | Expected result |
|---|---|---|---|
| 1 | `standard_user` | `secret_sauce` | The **Products** page is shown |
| 2 | `locked_out_user` | `secret_sauce` | *Epic sadface: Sorry, this user has been locked out.* |
| 3 | `standard_user` | `wrong_sauce` | *Epic sadface: Username and password do not match any user in this service* |

**Step 4: Write one example in the Given/When/Then shape.** This is the bridge to Gherkin (topic 1.3).

```text
Given I am on the login page
When I log in with username "locked_out_user" and password "secret_sauce"
Then I should see the error "Epic sadface: Sorry, this user has been locked out."
```

### Checkpoint

You have **3 rules**, **one example per rule** with real values, and one example written as Given/When/Then. Nobody on the team can read the examples in two different ways.

### Your turn

1. Write a rule and an example for "the username is required". (Try it: click Login with an empty username. Which message appears?)
2. In groups of three, play the Three Amigos for SL-104 (sort products): one product owner, one developer, one tester. Agree two rules and an example for each.
3. Explain in your own words the difference between BDD and "using Cucumber".

### Common errors

| Mistake | Why it hurts | Better |
|---|---|---|
| Writing scenarios alone, after the code is done | No shared understanding; BDD becomes paperwork | Discuss examples **before** development |
| Rules without examples | Everyone agrees, but means different things | At least one concrete example per rule |
| Only "happy path" examples | Errors and edge cases stay hidden | Ask "what if...?" for each rule |

---

## 1.2 User Stories and Acceptance Criteria

### Definition

A **user story** is a short description of something a user needs, written from the user's point of view, usually as *As a ... I want ... So that ...*. A story is deliberately short: it is a promise to have a conversation, not a full specification. **Acceptance criteria** are the conditions the story must meet to be accepted by the product owner; they make the story **testable**. **Example Mapping** is a short workshop (about 25 minutes) in which the Three Amigos turn a story into rules (acceptance criteria), examples and open questions, using coloured cards. For a QE, stories and acceptance criteria are the raw material for every scenario.

### Key terms

| Term | Meaning |
|---|---|
| **Connextra format** | *As a* (who) / *I want* (what) / *So that* (why: the value) |
| **Three Cs** | **C**ard (the short story), **C**onversation (the details), **C**onfirmation (the acceptance criteria) |
| **INVEST** | A good story is **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall, **T**estable |
| **Acceptance criteria (AC)** | Conditions for **one** story to be accepted |
| **Definition of Done (DoD)** | Conditions for **every** story (code reviewed, tests pass, ...) |
| **Story ID** | A ticket number such as `SL-101`, used to trace scenarios back to stories |

**Example Mapping cards:**

| Colour | Holds |
|---|---|
| **Yellow** | The story |
| **Blue** | Rules (acceptance criteria) |
| **Green** | Examples, under the rule they illustrate |
| **Red** | Questions nobody can answer yet |

### Key ideas

- Good acceptance criteria are **testable** (pass/fail can be decided), **clear** (one meaning), and describe **outcomes**, not buttons or code.
- Many **red** cards: the story isn't ready. Many **blue** cards: the story is too big; split it.
- A story is finished when it meets **its** acceptance criteria **and** the team's Definition of Done.

### Worked example: an example map for SL-101 (log in)

**Step 1: Check the story with INVEST.** SL-101 is valuable ("see the products"), small and testable. ✔

**Step 2: Write the acceptance criteria as rules (blue cards).**

```text
SL-101  Acceptance criteria
  AC1  A known, unlocked user with the correct password sees the Products page.
  AC2  A locked-out user is refused with a clear message.
  AC3  A wrong password is refused with a message.
  AC4  Username and password are both required.
```

**Step 3: Add examples under each rule (green cards).**

```text
[BLUE] AC1 Known user      [BLUE] AC2 Locked out        [BLUE] AC3 Wrong password       [BLUE] AC4 Required
[GREEN] standard_user ->   [GREEN] locked_out_user ->   [GREEN] standard_user /         [GREEN] empty username ->
        Products page              "Sorry, this user            wrong_sauce ->                  "Username is required"
[GREEN] problem_user ->            has been locked out."        "Username and password  [GREEN] empty password ->
        Products page                                           do not match..."                "Password is required"
```

**Step 4: Write down the open questions (red cards).**

```text
[RED] After how many wrong passwords is a user locked out?
[RED] Should the error say whether the username or the password was wrong? (Security!)
```

### Checkpoint

Your map has **1 yellow** card (SL-101), **4 blue** cards, **at least one green** card under each blue card, and **at least one red** card. Every green card contains real values.

### Your turn

1. Write the acceptance criteria for SL-102 (log out) as one or two rules, each with an example.
2. Rewrite these weak criteria so they are testable: (a) "Login is easy." (b) "Errors are shown." (c) "The red box under the form shows a message."
3. Make an example map for SL-104 (sort products): at least two rules, with examples using real product names (the cheapest product is *Sauce Labs Onesie*, $7.99).

### Common errors

| Mistake | Example | Fix |
|---|---|---|
| The story describes a solution | "I want a dropdown with four options" | Describe the need: "I want to sort products by price" |
| No *so that* | "As a shopper I want to log in." | Ask *why*; the value guides the solution |
| Criteria describe implementation | "The Login button calls `POST /login`" | Describe the outcome: "The Products page is shown" |

---

## 1.3 Gherkin

### Definition

**Gherkin** is the plain-language format in which BDD scenarios are written so that a tool like Cucumber can read them. A Gherkin file has the extension `.feature`. It starts with the keyword `Feature:`, followed by one or more `Scenario:` blocks; each scenario is a list of **steps**, and every step starts with `Given`, `When`, `Then`, `And` or `But`. Gherkin is strict about its **keywords and structure** (colons, one feature per file, table formatting) but free about the **words** after each keyword; those words are matched to Java code later (Cucumber Handout 2).

### Key terms

| Keyword | Purpose |
|---|---|
| `Feature:` | Names the capability the file describes. Free text under it is a description for readers. |
| `Scenario:` | One concrete example of behaviour |
| `Given` | The starting situation |
| `When` | The action the user takes |
| `Then` | The expected outcome |
| `And`, `But` | Continue the previous kind of step |
| `#` | A comment line |
| `Background:`, `Rule:`, `Scenario Outline:`, `Examples:` | Structure keywords (Cucumber Handout 3) |
| `@tag` | A label on a feature or scenario (Cucumber Handout 4) |

**Step arguments**: extra data under a step:

| Kind | Looks like | Use for |
|---|---|---|
| **Data table** | `\| Sauce Labs Backpack \|` rows under the step | Lists and tables of values |
| **Doc string** | Text between two `"""` lines | A longer block of text |

### Key ideas

- **One feature per file**, named in lower case: `login.feature`. Feature files go in `src/test/resources/features`.
- Every keyword that starts a block **ends with a colon**: `Feature:`, `Scenario:`.
- Put values that may change **in quotes**, e.g. `"standard_user"`: Cucumber Handout 2 turns them into method parameters.

### Worked example: `login.feature`, first version (SL-101)

**Step 1: The feature and a short description for readers.**

```gherkin
Feature: Log in to Swag Labs
  Shoppers must log in before they can see the products.
  Only known, unlocked users with the shared password get in.
```

**Step 2: The first scenario: the rule "a known user gets in".**

```gherkin
  Scenario: Valid user logs in
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should see the "Products" page
```

**Step 3: Two "refused" scenarios**, from the example map in 1.2.

```gherkin
  Scenario: Locked-out user is refused
    Given I am on the login page
    When I log in with username "locked_out_user" and password "secret_sauce"
    Then I should see the error "Epic sadface: Sorry, this user has been locked out."

  Scenario: Wrong password is refused
    Given I am on the login page
    When I log in with username "standard_user" and password "wrong_sauce"
    Then I should see the error "Epic sadface: Username and password do not match any user in this service"
```

**Complete file: first version (3 scenarios).** Topic 1.4 adds a fourth scenario to this file.

```gherkin
# src/test/resources/features/login.feature   (first version)
Feature: Log in to Swag Labs
  Shoppers must log in before they can see the products.
  Only known, unlocked users with the shared password get in.

  Scenario: Valid user logs in
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should see the "Products" page

  Scenario: Locked-out user is refused
    Given I am on the login page
    When I log in with username "locked_out_user" and password "secret_sauce"
    Then I should see the error "Epic sadface: Sorry, this user has been locked out."

  Scenario: Wrong password is refused
    Given I am on the login page
    When I log in with username "standard_user" and password "wrong_sauce"
    Then I should see the error "Epic sadface: Username and password do not match any user in this service"
```

### Checkpoint

In VS Code with the official **Cucumber** extension installed (*Extensions* view, `Ctrl+Shift+X`, search "Cucumber", publisher **Cucumber**), the keywords are coloured and there are **no red error marks**. Steps may be underlined as having no step definition: that is expected until Cucumber Handout 2.

### Your turn

1. Write a scenario for an **empty username** (message: *Epic sadface: Username is required*). Hint: `""` (nothing between the quotes) is an empty value. Keep it in a separate file for now; Handout 3 adds it with an outline.
2. Remove the colon after one `Scenario` and look at the file. What changes?
3. Write a step with a **data table** that lists two products a shopper adds to the cart:
   ```gherkin
   Given I have added these products to the cart:
     | Sauce Labs Backpack   |
     | Sauce Labs Bike Light |
   ```

### Common errors

| You see | Why | Fix |
|---|---|---|
| A scenario is silently treated as text | `Scenario` without a colon | Every block keyword ends with `:` |
| Table error, e.g. "inconsistent cell count" | A row has a different number of `\|` | Every row needs the same columns |
| A comment becomes part of a step | `#` only starts a comment at the beginning of a line | Put comments on their own line |
| Two `Feature:` lines in one file | Only one feature per file is allowed | One `.feature` file per feature |

---

## 1.4 Features and Scenarios

### Definition

A **feature** is one capability of the system, such as "Log in to Swag Labs", described in one `.feature` file; it usually matches one user story or one area of the product. A **scenario** is one concrete example of how that feature behaves: a starting situation, **one** action, and the expected outcome. Good scenarios are **declarative** (they say *what* the user does, not *which buttons* are clicked), **independent** (each one sets up its own starting situation and can run alone, in any order) and focused on **one behaviour**. Together, a project's feature files are its living documentation.

### Key terms

| Term | Meaning |
|---|---|
| **Feature file** | One `.feature` file describing one feature |
| **Feature description** | Free text under `Feature:` that explains the context to readers |
| **Declarative step** | Describes intent: `When I log in with username "standard_user" and password "secret_sauce"` |
| **Imperative step** | Describes UI mechanics: `When I type "standard_user" into the field with id "user-name"` |
| **Independent scenario** | Does not rely on any other scenario having run first |

### Key ideas

| | Imperative (avoid) | Declarative (prefer) |
|---|---|---|
| Given | `Given I open "https://www.saucedemo.com"` | `Given I am on the login page` |
| When | `When I type "standard_user" into "#user-name" and click "#login-button"` | `When I log in with username "standard_user" and password "secret_sauce"` |
| Then | `Then the element ".title" has text "Products"` | `Then I should see the "Products" page` |

- **One `When` per scenario.** Several actions usually mean several behaviours; split them.
- Every scenario starts with its **own `Given`**, so it can run alone.
- Scenario titles describe the behaviour: "Locked-out user is refused", not "Test 2".

### Worked example: a logout scenario (SL-102)

Logging out needs a logged-in user first. The question is how to write that starting point.

**Step 1: The wrong way: depend on another scenario.**

```gherkin
  Scenario: User logs out
    When I log out
    Then I should be back on the login page
```

This only works if "Valid user logs in" happened to run just before it. Run it alone, or in a different order, and it fails.

**Step 2: The right way: set up the starting point with `Given` steps.** Logging in is now **context** (already done), so it is phrased in the past tense.

```gherkin
  Scenario: Logged-in user logs out
    Given I am on the login page
    And I have logged in with username "standard_user" and password "secret_sauce"
    When I log out
    Then I should be back on the login page
```

**Step 3: Check the shape:** `Given` + `And` (context), one `When` (the behaviour), one `Then` (what the user sees). ✔

**Step 4: Add it to `login.feature`.** This is the **final version** of the file, the one Cucumber Handout 2 uses.

**Complete file: final version (4 scenarios), used in Cucumber Handout 2**

```gherkin
# src/test/resources/features/login.feature   (final version for Handout 2)
Feature: Log in to Swag Labs
  Shoppers must log in before they can see the products.
  Only known, unlocked users with the shared password get in.

  Scenario: Valid user logs in
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should see the "Products" page

  Scenario: Locked-out user is refused
    Given I am on the login page
    When I log in with username "locked_out_user" and password "secret_sauce"
    Then I should see the error "Epic sadface: Sorry, this user has been locked out."

  Scenario: Wrong password is refused
    Given I am on the login page
    When I log in with username "standard_user" and password "wrong_sauce"
    Then I should see the error "Epic sadface: Username and password do not match any user in this service"

  Scenario: Logged-in user logs out
    Given I am on the login page
    And I have logged in with username "standard_user" and password "secret_sauce"
    When I log out
    Then I should be back on the login page
```

### Checkpoint

`login.feature` has **4 scenarios**. Check each one:

- [ ] Starts with its own `Given` (could run alone).
- [ ] Has exactly **one** `When`.
- [ ] Every `Then` is something a user can **see**.
- [ ] No ids, CSS or "click" in any step.

### Your turn

1. Rewrite this imperative scenario declaratively in three steps:
   ```gherkin
   Scenario: Login
     Given I open "https://www.saucedemo.com"
     And I type "standard_user" into "#user-name"
     And I type "secret_sauce" into "#password"
     And I click "#login-button"
     Then ".title" should be "Products"
   ```
2. **For Handout 3:** write `sorting.feature` for SL-104 with two scenarios. Each logs in first (same two `Given` steps as the logout scenario), then sorts: "Price (low to high)" puts *Sauce Labs Onesie* first; "Price (high to low)" puts *Sauce Labs Fleece Jacket* first. Use the steps `When I sort the products by "..."` and `Then the first product should be "..."`.
3. This scenario has two `When`s: `When I log in ... / And I log out / Then ...`. Which step should become a `Given`, and how would you phrase it?

### Common errors

| Smell | Why it hurts | Fix |
|---|---|---|
| Several `When`s in one scenario | Tests more than one behaviour; unclear failures | Split it; move earlier actions into `Given` |
| Scenarios that depend on each other | Can't run alone; fail when the order changes | Each scenario sets up its own state |
| Ids, CSS or "click" in steps | Breaks when the UI changes; hard for business to read | Describe intent; hide details in code (Handout 2) |
| Vague titles ("Test 1") | Reports say nothing useful | Name the behaviour |

---

**End of Cucumber Handout 1.** You can explain BDD, turn a story into rules and examples, and write a feature file in Gherkin. **Use the final version of `login.feature` (topic 1.4, 4 scenarios) in Cucumber Handout 2.** **Next:** Cucumber Handout 2, Automating Scenarios.
