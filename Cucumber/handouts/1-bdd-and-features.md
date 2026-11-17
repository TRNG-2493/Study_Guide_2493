# Cucumber In-Class Handout 1: BDD and Writing Features

**Topics:** 1.1 BDD fundamentals · 1.2 User stories and acceptance criteria · 1.3 Gherkin · 1.4 Features and scenarios

**How to use this handout:** the same layout as the Selenium handouts. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**This handout is about writing, not code.** You learn what BDD is, turn a requirement into rules and examples, and write them as **feature files** in Gherkin. Cucumber Handout 2 connects these files to Java and Selenium, so the feature files you write today will run there.

**Running example:** three Swag Labs user stories used throughout the BDD handouts.

```text
SL-101  As a registered shopper
        I want to log in with my username and password
        So that I can see the products and my cart

SL-102  As a shopper
        I want to add products to a cart and see how many I have chosen
        So that I can buy several products in one order

SL-104  As a shopper
        I want to sort products by price
        So that I can find affordable products quickly
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
| **Shared (ubiquitous) language** | The same words used by everyone, in conversation, stories, scenarios and code: *shopper*, *cart*, *product* |
| **Living documentation** | Scenarios that describe the system **and** are run as tests, so they can never silently go out of date |
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

- **Examples beat rules.** Everyone agrees with "tax is added"; only an example ("$39.98 → $3.20 tax") shows whether they mean the same thing.
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
Rule 1: A known user with the correct password reaches the products page.
Rule 2: A locked-out user is refused, with a message saying so.
Rule 3: A wrong password is refused, with a message.
```

**Step 3: Give each rule at least one concrete example** with real Swag Labs values.

| Rule | Username | Password | Expected result |
|---|---|---|---|
| 1 | `standard_user` | `secret_sauce` | The **Products** page is shown |
| 2 | `locked_out_user` | `secret_sauce` | *Epic sadface: Sorry, this user has been locked out.* |
| 3 | `standard_user` | `wrong_sauce` | *Epic sadface: Username and password do not match any user in this service* |

**Step 4: Write one example in the Given/When/Then shape.** This is the bridge to Gherkin (topic 1.3).

```text
Given I am on the Swag Labs login page
When I log in as "locked_out_user" with password "secret_sauce"
Then I should see the login error "Epic sadface: Sorry, this user has been locked out."
```

### Checkpoint

You have **3 rules**, **at least one example per rule** with real values, and one example written as Given/When/Then. Nobody on the team can read the examples in two different ways.

### Your turn

1. Write a rule and two examples for "the username is required" (hint: log in with an **empty** username; the message is *Epic sadface: Username is required*).
2. In groups of three, play the Three Amigos for SL-104 (sort by price): one product owner, one developer, one tester. Agree two rules and two examples for each.
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

**Step 1: Check the story with INVEST.** SL-101 is valuable ("see the products and my cart"), small enough for one sprint, and testable. ✔

**Step 2: Write the acceptance criteria as rules (blue cards).**

```text
SL-101  Acceptance criteria
  AC1  A known user with the correct password reaches the products page.
  AC2  A locked-out user is refused with a clear message.
  AC3  A wrong password is refused with a message.
  AC4  Username and password are both required.
```

**Step 3: Add examples under each rule (green cards).**

```text
[BLUE] AC1 Known user gets in     [BLUE] AC2 Locked out       [BLUE] AC3 Wrong password       [BLUE] AC4 Required
[GREEN] standard_user /           [GREEN] locked_out_user ->  [GREEN] standard_user /         [GREEN] empty username ->
        secret_sauce -> Products          "Sorry, this user           wrong_sauce ->                  "Username is required"
                                          has been locked out."       "Username and password  [GREEN] empty password ->
                                                                      do not match..."                "Password is required"
```

**Step 4: Write down the open questions (red cards).**

```text
[RED] After how many wrong passwords is a user locked out?
[RED] Should the error say whether the username or the password was wrong?
```

### Checkpoint

Your map has **1 yellow** card (SL-101), **4 blue** cards, **at least one green** card under each blue card, and **at least one red** card. Every green card contains real values.

### Your turn

1. Write a story in Connextra format for "removing a product from the cart", and check it against INVEST letter by letter.
2. Rewrite these weak criteria so they are testable: (a) "Login is easy." (b) "Errors are shown." (c) "The red badge in the top-right corner shows the count."
3. Make an example map for SL-102 (cart): at least two rules, with examples using real product names (e.g. *Sauce Labs Backpack*).

### Common errors

| Mistake | Example | Fix |
|---|---|---|
| The story describes a solution | "I want a dropdown with four options" | Describe the need: "I want to sort products by price" |
| No *so that* | "As a shopper I want to sort products." | Ask *why*; the value guides the solution |
| Criteria describe implementation | "The Login button calls `POST /login`" | Describe the outcome: "The products page is shown" |

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

### Worked example: `login.feature` (SL-101)

**Step 1: The feature and a short description for readers.**

```gherkin
Feature: Log in to Swag Labs
  Customers must log in before they can browse products.
  Only known, unlocked users with the shared password get in.
```

**Step 2: The first scenario: the rule "a known user gets in".**

```gherkin
  Scenario: Standard user logs in
    Given I am on the Swag Labs login page
    When I log in as "standard_user" with password "secret_sauce"
    Then I should see the "Products" page
```

**Step 3: Two "refused" scenarios**, from the example map in 1.2.

```gherkin
  Scenario: Locked-out user is refused
    Given I am on the Swag Labs login page
    When I log in as "locked_out_user" with password "secret_sauce"
    Then I should see the login error "Epic sadface: Sorry, this user has been locked out."

  Scenario: Wrong password is refused
    Given I am on the Swag Labs login page
    When I log in as "standard_user" with password "wrong_sauce"
    Then I should see the login error "Epic sadface: Username and password do not match any user in this service"
```

**Complete file**

```gherkin
# src/test/resources/features/login.feature
Feature: Log in to Swag Labs
  Customers must log in before they can browse products.
  Only known, unlocked users with the shared password get in.

  Scenario: Standard user logs in
    Given I am on the Swag Labs login page
    When I log in as "standard_user" with password "secret_sauce"
    Then I should see the "Products" page

  Scenario: Locked-out user is refused
    Given I am on the Swag Labs login page
    When I log in as "locked_out_user" with password "secret_sauce"
    Then I should see the login error "Epic sadface: Sorry, this user has been locked out."

  Scenario: Wrong password is refused
    Given I am on the Swag Labs login page
    When I log in as "standard_user" with password "wrong_sauce"
    Then I should see the login error "Epic sadface: Username and password do not match any user in this service"
```

### Checkpoint

In VS Code with the official **Cucumber** extension installed (*Extensions* view, `Ctrl+Shift+X`, search "Cucumber", publisher **Cucumber**), the keywords are coloured and there are **no red error marks**. Steps may be underlined as having no step definition: that is expected until Cucumber Handout 2.

### Your turn

1. Add a fourth scenario to `login.feature` for an **empty username** (message: *Epic sadface: Username is required*). Hint: `"..."` with nothing between the quotes is an empty value.
2. Remove the colon after one `Scenario` and look at the file in the IDE. What changes?
3. Write a scenario that uses a **data table** to list two products a shopper adds to the cart:
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

A **feature** is one capability of the system, such as "Log in" or "Shopping cart", described in one `.feature` file; it usually matches one user story or one area of the product. A **scenario** is one concrete example of how that feature behaves: a starting situation, **one** action, and the expected outcome. Good scenarios are **declarative** (they say *what* the user does, not *which buttons* are clicked), **independent** (each one sets up its own starting situation and can run alone, in any order) and focused on **one behaviour**. Together, a project's feature files are its living documentation.

### Key terms

| Term | Meaning |
|---|---|
| **Feature file** | One `.feature` file describing one feature |
| **Feature description** | Free text under `Feature:` that explains the context to readers |
| **Declarative step** | Describes intent: `When I add "Sauce Labs Onesie" to the cart` |
| **Imperative step** | Describes UI mechanics: `When I click the button with id "add-to-cart-sauce-labs-onesie"` |
| **Independent scenario** | Does not rely on any other scenario having run first |

### Key ideas

| | Imperative (avoid) | Declarative (prefer) |
|---|---|---|
| Given | `Given I type "standard_user" in the username field` | `Given I am logged in as "standard_user"` |
| When | `When I click the button with id "add-to-cart-sauce-labs-onesie"` | `When I add "Sauce Labs Onesie" to the cart` |
| Then | `Then the element ".shopping_cart_badge" has text "1"` | `Then the cart badge should show 1` |

- **One `When` per scenario.** Several actions usually mean several behaviours; split them.
- Every scenario starts with its **own `Given`**, so it can run alone.
- Scenario titles describe the behaviour: "Locked-out user is refused", not "Test 3".

### Worked example: `cart.feature` (SL-102) and `sorting.feature` (SL-104)

**Step 1: The cart feature and its description.**

```gherkin
Feature: Shopping cart
  Shoppers collect products in a cart before checking out.
  The badge on the cart icon shows how many products are in the cart.
```

**Step 2: A declarative scenario for adding products.**

```gherkin
  Scenario: Adding products shows the count on the cart badge
    Given I am logged in as "standard_user"
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show 2
```

**Step 3: An independent scenario.** It sets up its **own** cart; it does not continue from step 2.

```gherkin
  Scenario: Removing the only product hides the badge
    Given I am logged in as "standard_user"
    And I have added "Sauce Labs Onesie" to the cart
    When I remove "Sauce Labs Onesie" from the cart
    Then the cart badge should not be shown
```

**Step 4: A scenario with a data table.**

```gherkin
  Scenario: The cart lists the products that were added
    Given I am logged in as "standard_user"
    And I have added these products to the cart:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
    When I open the cart
    Then the cart should contain exactly:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
```

**Step 5: The sorting feature (SL-104).**

```gherkin
Feature: Sorting products
  Shoppers can sort the product list by name or by price.

  Scenario: Cheapest product first
    Given I am logged in as "standard_user"
    When I sort the products by "Price (low to high)"
    Then the first product should be "Sauce Labs Onesie"

  Scenario: Most expensive product first
    Given I am logged in as "standard_user"
    When I sort the products by "Price (high to low)"
    Then the first product should be "Sauce Labs Fleece Jacket"
```

**Complete files**

```gherkin
# src/test/resources/features/cart.feature
Feature: Shopping cart
  Shoppers collect products in a cart before checking out.
  The badge on the cart icon shows how many products are in the cart.

  Scenario: Adding products shows the count on the cart badge
    Given I am logged in as "standard_user"
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show 2

  Scenario: Removing the only product hides the badge
    Given I am logged in as "standard_user"
    And I have added "Sauce Labs Onesie" to the cart
    When I remove "Sauce Labs Onesie" from the cart
    Then the cart badge should not be shown

  Scenario: The cart lists the products that were added
    Given I am logged in as "standard_user"
    And I have added these products to the cart:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
    When I open the cart
    Then the cart should contain exactly:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
```

```gherkin
# src/test/resources/features/sorting.feature
Feature: Sorting products
  Shoppers can sort the product list by name or by price.

  Scenario: Cheapest product first
    Given I am logged in as "standard_user"
    When I sort the products by "Price (low to high)"
    Then the first product should be "Sauce Labs Onesie"

  Scenario: Most expensive product first
    Given I am logged in as "standard_user"
    When I sort the products by "Price (high to low)"
    Then the first product should be "Sauce Labs Fleece Jacket"
```

### Checkpoint

You now have three feature files in `src/test/resources/features`: `login.feature` (3 scenarios), `cart.feature` (3) and `sorting.feature` (2). Check every scenario against this list:

- [ ] Starts with its own `Given` (could run alone).
- [ ] Has exactly **one** kind of action (`When`, possibly continued with `And`).
- [ ] Every `Then` is something a user can **see**.
- [ ] No locators, ids or CSS in any step.

### Your turn

1. Rewrite this imperative scenario declaratively in at most four steps:
   ```gherkin
   Scenario: Buy
     Given I open "https://www.saucedemo.com"
     And I type "standard_user" into "#user-name"
     And I type "secret_sauce" into "#password"
     And I click "#login-button"
     And I click "#add-to-cart-sauce-labs-backpack"
     Then ".shopping_cart_badge" should be "1"
   ```
2. Add a scenario to `sorting.feature`: sorting by "Name (Z to A)" puts "Test.allTheThings() T-Shirt (Red)" first.
3. Scenario B starts with `When I remove "Sauce Labs Onesie" from the cart` and relies on scenario A having added it. Rewrite B so it is independent.

### Common errors

| Smell | Why it hurts | Fix |
|---|---|---|
| Several `When`s in one scenario | Tests more than one behaviour; unclear failures | Split it; move earlier actions into `Given` |
| Scenarios that depend on each other | Can't run alone; fail when the order changes | Each scenario sets up its own state |
| Ids, CSS or "click" in steps | Breaks when the UI changes; hard for business to read | Describe intent; hide details in code (Handout 2) |
| Vague titles ("Test 1") | Reports say nothing useful | Name the behaviour |

---

**End of Cucumber Handout 1.** You can explain BDD, turn a story into rules and examples, and write feature files in Gherkin: `login.feature`, `cart.feature` and `sorting.feature`. **Next:** Cucumber Handout 2, Automating Scenarios: connecting these steps to Java and Selenium.
