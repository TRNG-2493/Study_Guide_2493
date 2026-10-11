# Given / When / Then

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the purpose of **Given**, **When**, and **Then**, and the thinking pattern behind them (**Arrange, Act, Assert**).
- Write **Given** steps that set up *state* (not actions), **When** steps that describe a single *action or event*, and **Then** steps that describe an *observable outcome*.
- Use **And** and **But** correctly to keep scenarios readable.
- Recognize and fix the most common mistakes: assertions in Given/When, actions in Then, multiple Whens, UI-level wording, and missing context.
- Explain the difference between **declarative** and **imperative** step wording and choose the right level.
- Write steps that are **reusable** (consistent phrasing, parameters) and easy to map to step definitions.
- Trace how Cucumber turns one Given/When/Then line into one Java method call, and describe how the three keywords relate to **Arrange-Act-Assert** in unit testing and to your **page objects**.
- Read a scenario written by someone else and judge, with a checklist, whether it is well formed.

---

## Why This Matters

On the surface, Given/When/Then looks like decoration: three words at the start of lines. In reality, it is a **disciplined thinking tool**. It forces you to separate three questions that are easy to mix up:

1. **What is the situation?** (Given)
2. **What happens?** (When)
3. **What should result?** (Then)

When people skip this discipline, scenarios become tangled: assertions hide in the middle, actions appear in the "outcome" section, and nobody can tell what is being tested. When scenarios follow the pattern, they become **precise**: any reader can see the precondition, the trigger, and the expected outcome at a glance, and the automation layer maps cleanly to your page objects (Given and When call actions; Then calls queries and assertions).

There is also a very practical, selfish reason to care. Earlier this week you learned that a test that checks five things at once is hard to diagnose when it fails. Given/When/Then is the same lesson applied to *specifications*: a scenario with one situation, one action, and one outcome fails for one reason, so a red result points straight at the broken behavior. A scenario that tangles three actions and four checks fails with a message like "expected 2 but was 1" and nobody remembers which step caused it.

Where will you use this? Everywhere in today's work:

- In the **three-amigos pair activity**, where you and your partner turn a user story's acceptance criteria into scenarios for Project 2 (the Sauce Demo shop at `saucedemo.com`).
- In the **next lesson (Step Definitions)**, where every line you write here becomes a Java method.
- In the **Cucumber Framework Setup** lesson, where you run your first scenario end to end.

This lesson is the practical heart of today's work: it is the pattern you will use in every scenario you write for Project 2.

---

## The Concept

### 1. The Three Roles

| Keyword | Role | Question it answers | Tense / form | Test analogy |
|---|---|---|---|---|
| **Given** | Context | "What is already true?" | Past or present state: "the cart is empty", "the user has logged in" | **Arrange** |
| **When** | Action / event | "What does the user (or system) do?" | Present: "the shopper adds a product" | **Act** |
| **Then** | Outcome | "What should we observe?" | Present/future: "the cart count shows 1" | **Assert** |

A simple example mapped to roles:

```gherkin
Scenario: Adding a product increases the cart count
  Given the shopper has an empty cart              # context: state of the world
  When the shopper adds "Sauce Labs Backpack"      # action: the thing being tested
  Then the cart count shows 1                      # outcome: what we observe
```

(The `#` notes on the right are annotations for you, added for teaching. In a real feature file Gherkin only treats a `#` at the **start of a line** as a comment; a `#` after the step text becomes part of the step text and the step would be reported as undefined (see gherkin.md). Delete the notes before you copy the example into a `.feature` file.)

**Line by line:**

- `Scenario: Adding a product increases the cart count` names the *behavior* being specified. Notice it is a sentence about the system, not "Test 1".
- `Given the shopper has an empty cart` is the **precondition**. We want to start from a known place: if the cart already had three items, "count shows 1" would be false for reasons unrelated to what we are testing.
- `When the shopper adds "Sauce Labs Backpack"` is the **single trigger**. Everything before it is setup; everything after it is checking. The `"Sauce Labs Backpack"` in quotes is a value that varies; in the next lesson you will see it become a method parameter.
- `Then the cart count shows 1` is the **expected result**. It will become an assertion that compares an expected number to what the page really shows.

#### Three analogies to make the roles stick

1. **A science experiment.** Set up the conditions (Given), perform the intervention (When), measure the result (Then). A scientist who changes two things at once cannot say which one caused the result; the same is true of a scenario with two Whens.
2. **A recipe test in a kitchen.** *Given* the oven is at 180 degrees and the tin is greased, *When* the cake goes in for 30 minutes, *Then* a skewer comes out clean. You would never write "Then put the cake in the oven" in the outcome section: the outcome section only describes what you can look at.
3. **A bank-machine receipt.** *Given* your balance is 100, *When* you withdraw 40, *Then* your balance is 60. Even non-technical people understand this three-beat structure. That is exactly why Cucumber chose it: product owners, testers, and developers can all read it.

#### How the keywords relate to Selenium work you already know

Earlier this week you wrote Selenium tests (and later page objects) with a natural rhythm: open the page and log in, click something, check something. You were already doing Arrange-Act-Assert; Given/When/Then simply gives each phase a *name inside the specification*.

| What you did on Monday to Wednesday | Phase | Gherkin keyword |
|---|---|---|
| Create the driver, `driver.get(url)`, log in as `standard_user` | Arrange | Given |
| Click "Add to cart" | Act | When |
| `assertEquals("1", badge.getText())` | Assert | Then |

### 2. Given: Setting the Scene

A **Given** step puts the system into a known **state** before the behavior under test happens.

**Characteristics:**

- Describes *state*, not *action*: "the user **is** logged in" rather than "the user **clicks** login".
- Is **not** the behavior being tested; it is the precondition.
- May be implemented in code by any convenient means (UI steps, API calls, database inserts). The scenario does not care how the state is reached, only that it is.
- Usually appears first; several Givens can be joined with `And`.

**Why state and not action?** Imagine two scenarios: one tests login, another tests the cart. The cart scenario needs a logged-in user, but it is not *about* logging in. If you wrote `Given the shopper clicks the login button`, a reader would think the login click matters to the cart rule. Writing `Given the shopper is logged in` says "this is just the starting point", and it leaves the automation free to reach that state in the fastest reliable way.

**Good Givens:**

```gherkin
Given the shopper is logged in
Given the shopper has "Sauce Labs Backpack" in the cart
Given a locked-out user named "locked_out_user" exists
Given the shop has 6 products in the catalog
```

**Weak Givens (and fixes):**

| Weak | Problem | Better |
|---|---|---|
| `Given the user clicks the login button` | An action, not a state | `Given the user is on the login page` |
| `Given I open Chrome` | Technical environment detail | (Hide in setup code, not in the scenario) |
| `Given the user is on the page` | Which page? | `Given the shopper is on the products page` |
| `Given the system is working` | Vague, untestable | Remove, or state the specific precondition |

**Tip:** Include only the context that **matters** for this scenario's outcome. If the result does not depend on the customer's address, leave the address out.

**A useful test for a Given:** Read it with the words "It is already true that..." in front. "It is already true that the shopper is logged in" reads fine. "It is already true that the user clicks the login button" does not. If the sentence only makes sense as something that *happens*, it belongs in a When.

#### "Which page?" and the Given that navigates

You will notice that `Given the customer is on the login page` involves an action in code (opening a URL), even though in the specification it is a state. That is fine. The *specification* states where we start; the *automation* decides how to get there (`driver.get("https://www.saucedemo.com")`). Givens are allowed to be implemented with actions; they just must not be *worded* as actions of the behavior under test.

### 3. When: The Action Under Test

A **When** step describes the **one key action or event** that triggers the behavior.

**Characteristics:**

- Describes what the **user does** (or what **event** occurs): "the shopper adds", "the customer submits the order", "the timer expires".
- Normally there is **exactly one** When per scenario (or one cohesive action expressed in one or two lines).
- Uses the **active voice** and present tense.
- Describes intention, not UI mechanics.

**Good Whens:**

```gherkin
When the shopper adds "Sauce Labs Backpack" to the cart
When the customer logs in with username "standard_user" and password "secret_sauce"
When the customer submits the order
When the shopper sorts the products by "Price (low to high)"
```

**Weak Whens:**

| Weak | Problem | Better |
|---|---|---|
| `When I click on the 2nd button and then the dropdown and select option 3` | UI choreography | `When the shopper sorts by "Price (high to low)"` |
| `When the user logs in and adds a product and checks out` | Three behaviors | One scenario per behavior; move the first two into Givens |
| `When the cart has 1 item` | A state, not an action (this is a Given) | Move to Given |

**More than one When?** A second When often signals a second behavior. However, a scenario about an *interaction over time* may legitimately have two (for example, "When the user adds an item. And the user undoes the action."). If you find yourself writing `When ... Then ... When ... Then ...`, split the scenario.

**Why one When?** Think of the When as the *subject of the scenario*. If a scenario's title is "Removing an item empties the cart", the When must be the removal. If you also add an item in a When, the scenario is now about two behaviors, and a failure could be caused by either. With one When, a red scenario always means: *given this situation, this action did not produce this outcome*.

**The "movie trailer" trick.** If you are unsure which step is the When, ask: "If I had to name this scenario after one thing the user does, what would it be?" That sentence is your When. Every step before it that merely prepares the ground is a Given.

### 4. Then: The Observable Outcome

A **Then** step states the **expected result**: what a user (or an observer) can **see or measure** after the action. In automation it becomes an **assertion**.

**Characteristics:**

- Describes **observable outcomes**: a message on screen, a changed count, a new page, an email sent. It should be something visible from outside the system, rather than "the database row was inserted" (unless the database is the observable interface).
- States expected results **specifically** (exact message, exact number).
- Focuses on **one outcome** (possibly several closely related facts joined by `And`).
- Does **not** perform actions.

**Good Thens:**

```gherkin
Then the cart count shows 1
Then the error message "Epic sadface: Username is required" is displayed
Then the customer sees the products page
Then the products are listed from the cheapest to the most expensive
```

**Weak Thens:**

| Weak | Problem | Better |
|---|---|---|
| `Then it works` | Not specific | State the exact observable result |
| `Then the user clicks the cart icon and sees one item` | Action inside Then | Make clicking a When in another scenario |
| `Then the database contains the order` | Implementation-level | `Then the customer sees an order confirmation` |
| `Then the text of element id=title equals "Products"` | Locator in business text | `Then the customer sees the products page` |

**Why must Then be observable?** A Then is a promise that the behavior can be *verified by someone looking from outside*. "The data is saved correctly" cannot be verified without knowing where to look. "The order confirmation shows 'Thank you for your order!'" can be verified by anyone, in a browser, with no knowledge of the code.

**Why must Then be specific?** Compare `Then an error is shown` with `Then the error message "Epic sadface: Password is required" is displayed`. The first passes even if the wrong error appears (for example a missing-username message when the password was the problem). The second pins down the exact behavior the story promised.

### 5. `And` and `But`

`And` and `But` simply **continue the previous keyword's role**. They improve readability by avoiding repetition of Given/When/Then.

(The `#` notes in the next block are teaching annotations; remove them in a real file, as explained under the first example.)

```gherkin
Scenario: Locked-out customer cannot log in
  Given the customer is on the login page            # context
  And the user "locked_out_user" exists              # And = another Given
  When the customer logs in with a valid password    # action
  Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed   # outcome
  And the customer remains on the login page         # And = another Then
  But the customer does not see the products page    # But = a negative Then
```

- `And` = "and also (same kind of step)".
- `But` = same meaning, chosen when the sentence expresses **contrast or negation**.
- To Cucumber, `And`/`But` have no special meaning; matching is by text only.

**Line by line:**

- Lines 1-2 are both Givens: `And` repeats "Given" without typing it. You could write `Given` twice; the result is identical to Cucumber, but reads worse.
- The single `When` is the one action: logging in.
- The first `Then` is the main outcome (the message). The `And` adds a closely related fact (we are still on the login page). The `But` adds a negation. Notice that all three are *observations*.

**Important detail about the first step of a scenario:** the first step of a scenario should be a real keyword (`Given`, `When`, or `Then`), not `And`. The keyword on line one tells the reader what role is starting.

**Warning:** A long chain of `And`s is a smell. If a scenario has six `And`s in the Then section, you are verifying too many things; split or focus.

**A subtle trap: And after a When.** Consider:

```gherkin
When the shopper adds "Sauce Labs Backpack" to the cart
And the shopper adds "Sauce Labs Bike Light" to the cart
Then the cart count shows 2
```

This is legitimate: a cohesive action expressed in two lines ("adds two products"). Compare it with a scenario that adds a product, goes to the cart, and removes it. That second example crosses behavior boundaries and should be split. The question to ask is *"is this one behavior or two?"*, not *"how many Whens are there?"*.

### 6. Declarative vs. Imperative Steps: Choosing the Level

| Style | Describes | Example | Strength | Weakness |
|---|---|---|---|---|
| **Imperative** | *How* the user interacts with the UI | `When the user enters "ada" in the username field and clicks Login` | Very precise | Brittle, verbose, tied to UI |
| **Declarative** | *What* the user wants to achieve | `When the customer logs in as "ada"` | Stable, readable, business-friendly | Hides detail in code |

Guideline: **default to declarative**. Use more detail only when the detail is part of the rule being demonstrated. Example: in a login-validation scenario, the specific *empty username* matters, so it is shown (`When the customer logs in with an empty username`), but the fact that the username is typed into a text box is not.

**Level mixing is confusing.** Avoid a scenario that says `Given the shopper is logged in` (high level) and then `When the shopper clicks the third product tile` (very low level). Keep all steps at a consistent level of abstraction.

#### Why declarative wins: the redesign test

Suppose the Sauce Demo team redesigns the login page so the button says "Sign in" instead of "Login". With imperative steps, **every scenario text** that mentions "clicks Login" is now wrong and must be edited in dozens of feature files. With declarative steps, *no feature file changes at all*; only one page-object method changes. That is the Page Object Model idea (from Wednesday) applied to the specification itself: hide volatile details behind a stable name.

#### The same behavior at three levels

```gherkin
# Too low level (imperative)
When the user types "standard_user" into the field with id "user-name"
And the user types "secret_sauce" into the field with id "password"
And the user clicks the element with id "login-button"

# Good (declarative)
When the customer logs in with username "standard_user" and password "secret_sauce"

# Too high level (hides what matters for a validation scenario)
When the customer logs in
```

The last version is fine for a scenario that simply needs a logged-in user, but if the scenario is *about* credentials, the reader needs to see which credentials. Choose the level by asking: **does the reader need this detail to understand the rule?**

### 7. Wording for Reuse

Cucumber matches steps by their text. To keep the number of step definitions small:

1. **Use identical phrasing** for identical meaning: always `the shopper is logged in`, never alternate with `the user has logged in` / `I am logged in` / `the customer is authenticated` across files.
2. **Choose one grammatical person** across the project: third person ("the shopper...") is most common; first person ("I add...") is also used by many teams. Do not mix.
3. **Parameterize variable values** in quotes or as numbers: `adds "Sauce Labs Backpack"`, `shows 3 items`.
4. **Keep steps self-explanatory** (avoid pronouns referring to earlier steps, like "it" or "that one").
5. **Avoid steps that are too generic** ("the user does something with the thing") or too specific (an entire flow in one sentence).

#### Why this matters in numbers

Imagine 30 scenarios that all begin with a logged-in shopper. If the team wrote that precondition five different ways, you would need five step definitions that all do the same thing, and each future change (say, a new login flow) must be made five times. If everyone wrote it one way, you need **one** method. Reuse is the main economy of BDD automation, and it is controlled entirely by how consistently the *text* is written.

#### A small team glossary (do this in your pair activity)

Before writing scenarios for Project 2, agree on a one-page vocabulary and stick to it:

| Concept | Agreed word | Avoid |
|---|---|---|
| Person using the site | the shopper (before login: the customer) | user, client, I, buyer |
| Product catalog page | the products page | inventory page, home page, main page |
| Logging in | logs in | signs in, authenticates, enters credentials |
| Adding to the basket | adds ... to the cart | puts, throws in, buys |

(The page object may still be called `InventoryPage`; the *business wording* in the feature file should use the language the product owner uses.)

### 8. Common Mistakes and Fixes (Gallery)

**Mistake 1: Assertion in Given or When.**

```gherkin
# Bad
Given the user logs in and sees the products page
```
Fix: Given describes state only (`Given the shopper is on the products page`); verify in a Then.

**Mistake 2: Action in Then.**

```gherkin
# Bad
Then the shopper clicks the cart and sees 1 item
```
Fix: Move the click to a When in a scenario about opening the cart; keep Then observational.

**Mistake 3: Multiple behaviors.**

```gherkin
# Bad
When the shopper adds an item and removes it and adds another
```
Fix: One behavior per scenario.

**Mistake 4: Incidental details.**

```gherkin
# Bad
Given the shopper "Ada", born 1815-12-10, address "10 Downing St", phone "555-0100", is logged in
```
Fix: `Given the shopper is logged in` (unless these details drive the rule).

**Mistake 5: Missing Given (hidden state).**

```gherkin
# Bad
When the shopper removes "Sauce Labs Backpack"
Then the cart is empty
```
Fix: Add `Given the shopper has "Sauce Labs Backpack" in the cart`, otherwise the scenario depends on invisible state.

**Mistake 6: Vague Then.**

```gherkin
# Bad
Then the page is correct
```
Fix: Name the specific expected title, message, or count.

**Mistake 7: Scenario titles that duplicate steps without adding meaning.**

```gherkin
# Bad title
Scenario: Given logged in when add item then count is 1
# Good title
Scenario: Adding a product increases the cart count
```
Fix: The title states the behavior; the steps give the example.

**Mistake 8: Technical wording in business language.**

```gherkin
# Bad
When the shopper sends a POST request to /cart/add
Then the response status is 200
```
Fix: Unless your audience is an API team and HTTP *is* the behavior, speak in the user's terms: `When the shopper adds "Sauce Labs Backpack" to the cart` and `Then the cart count shows 1`.

**Mistake 9: Negative phrasing that hides the point.**

```gherkin
# Bad
Then the shopper is not unable to see the products page
```
Fix: Use positive wording whenever possible: `Then the shopper sees the products page`. Use `But` or a clear negative only when the absence itself is the behavior.

### 9. How Cucumber Matches a Step (A Trace)

Understanding what happens when a scenario runs removes much of the mystery. Take this scenario:

```gherkin
Scenario: Adding a product increases the cart count
  Given the shopper has an empty cart
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1
```

and these step definitions (you will write them properly in the next lesson):

```java
@Given("the shopper has an empty cart")
@When("the shopper adds {string} to the cart")
@Then("the cart count shows {int}")
```

Cucumber executes the scenario like this:

| Order | What Cucumber does | Result |
|---|---|---|
| 1 | Reads the feature file and builds a scenario with three steps. | Steps are in a list, in file order. |
| 2 | **Strips the keyword.** `Given the shopper has an empty cart` becomes the text `the shopper has an empty cart`. | The keyword plays no part in matching. |
| 3 | Compares that text with every step-definition expression in the glue package. | One expression matches exactly: `the shopper has an empty cart`. |
| 4 | Creates a fresh instance of the class containing that method (and, as you will see below, the objects its constructor asks for). | Each scenario gets its own objects. |
| 5 | Calls the method. If it returns normally, the step is **passed**. | Console shows the step as passed. |
| 6 | Takes step 2: `the shopper adds "Sauce Labs Backpack" to the cart`. The expression `the shopper adds {string} to the cart` matches; `{string}` captures `Sauce Labs Backpack` (without quotes) and passes it to the method as a `String`. | `product = "Sauce Labs Backpack"` |
| 7 | Takes step 3: `{int}` captures `1`, converts to a Java `int`, calls the method. If the assertion inside throws `AssertionFailedError`, the step is **failed**. | Later steps (if any) become **skipped**. |

Three facts follow, and they explain many beginner errors:

1. **Keywords are not matched.** `Given`, `When`, and `Then` are for humans. If you wrote `Then the shopper adds "Sauce Labs Backpack" to the cart` in a feature file, it would still run the "adds" method. Discipline is on you, not on the tool.
2. **No match means undefined, not a crash.** If no expression fits, the step is *undefined* and Cucumber prints a snippet (see next lesson).
3. **Order is the order in the file.** A scenario is a script; steps run top to bottom and stop at the first failure.

### 10. The Link to Automation

Because of the roles, step definitions fall into natural categories, which maps cleanly onto your **page objects** from Wednesday:

| Gherkin keyword | Typical step-definition body | Page-object usage |
|---|---|---|
| **Given** | Navigate, log in, set up data | `loginPage.open()`, `loginPage.loginAs(...)`, `inventoryPage.addToCart(...)` |
| **When** | Perform the action under test | `inventoryPage.sortBy(...)`, `checkoutPage.submit(...)` |
| **Then** | Query the page and **assert** | `assertEquals(expected, cartPage.getItemNames())` |

Page objects **do not contain assertions** (Wednesday's rule); the **Then** step definitions are where assertions live. This neat split is one reason POM and BDD work well together.

```
  Feature file               Step definitions             Page objects          Selenium
  ────────────               ────────────────             ────────────          ────────
  Given (state)       ─────► call actions        ─────►   loginAs(), open()  ─► click(), sendKeys()
  When  (action)      ─────► call actions        ─────►   addToCart()        ─► click()
  Then  (outcome)     ─────► call queries+assert ─────►   getCartCount()     ─► getText()
```

### 11. A Worked Example, Step by Step

**Business rule:** "A shopper cannot check out without entering a postal code."

Draft (poor):

```gherkin
Scenario: Test checkout
  Given I open the browser
  And I go to saucedemo
  And I login
  And I add backpack
  And I click cart
  And I click checkout
  When I type Ada in first name
  And I type Lovelace in last name
  And I click continue
  Then I should see an error
```

Review: tech noise ("open the browser"), a vague title, a marathon of context steps, UI-level When, vague Then, and no mention of the *postal code* even though it is the rule.

Rewrite:

```gherkin
Scenario: Checkout is rejected when the postal code is missing
  Given the shopper has "Sauce Labs Backpack" in the cart
  And the shopper is on the checkout information page
  When the shopper continues with first name "Ada", last name "Lovelace" and no postal code
  Then the error message "Error: Postal Code is required" is displayed
  And the shopper remains on the checkout information page
```

Improvements: the title states the rule; Given sets only the relevant state; one When; Then verifies the exact message; the postal code, the point of the rule, is explicit.

#### How the rewrite was reached (the editing process)

Use these five moves whenever you improve a scenario:

1. **Name the rule** in one sentence. That becomes the title.
2. **Find the trigger.** Which one thing does the shopper do that the rule is about? ("Continues without a postal code.") That is the When.
3. **Find the observation.** What exactly does the shopper see? ("Error: Postal Code is required.") That is the Then.
4. **List what must already be true** for the trigger to even be possible: something in the cart, and being on the information page. Those are the Givens. Delete everything else.
5. **Re-read at one level of abstraction.** Remove locators, "open the browser", and any "I click..." choreography.

### 12. More Worked Examples (Login, Cart, Checkout)

#### 12a. Login: from imperative to declarative

Before:

```gherkin
Scenario: Login test 2
  Given I am on https://www.saucedemo.com
  When I enter "locked_out_user" in the Username box
  And I enter "secret_sauce" in the Password box
  And I click the Login button
  Then I should see the text "Epic sadface: Sorry, this user has been locked out." in the red box
```

After:

```gherkin
Scenario: A locked-out customer cannot log in
  Given the customer is on the login page
  When the customer logs in with username "locked_out_user" and password "secret_sauce"
  Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed
```

What changed: the URL left the scenario (it is configuration), three low-level When lines collapsed into one intent, and "the red box" became "the error message", which survives a color change.

#### 12b. Cart: hidden state exposed

Before (state is hidden in a previous scenario):

```gherkin
Scenario: Remove item
  When the shopper removes "Sauce Labs Backpack"
  Then the cart badge disappears
```

After:

```gherkin
Scenario: Removing the only item empties the cart
  Given the shopper is logged in
  And the shopper has "Sauce Labs Backpack" in the cart
  When the shopper removes "Sauce Labs Backpack" from the cart
  Then the cart count badge is not shown
```

What changed: the scenario now explains where it starts; it can run alone and in any order, which is a requirement for a trustworthy suite.

#### 12c. Checkout: too many behaviors in one

Before:

```gherkin
Scenario: Full purchase
  Given the shopper is logged in
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1
  When the shopper opens the cart
  Then the cart lists "Sauce Labs Backpack"
  When the shopper checks out with valid details
  Then the shopper sees "Thank you for your order!"
```

This has three When/Then pairs, so it is really three behaviors (add, view, purchase). When it fails on the last line, the title tells you nothing.

After (the last behavior stands on its own, with the previous ones moved into Givens):

```gherkin
Scenario: A shopper completes a purchase
  Given the shopper has "Sauce Labs Backpack" in the cart
  And the shopper is on the checkout information page
  When the shopper continues with first name "Ada", last name "Lovelace" and postal code "10001"
  And the shopper finishes the order
  Then the shopper sees the confirmation message "Thank you for your order!"
```

Notice that two consecutive When lines are allowed here because "continue then finish" is one cohesive purchase action.

### 13. A Quality Checklist for Every Scenario

Run every scenario you write through these questions:

| # | Question | If "no" |
|---|---|---|
| 1 | Does the title state a behavior (not "Test 1")? | Rewrite the title |
| 2 | Is every Given a state? | Reword or move to When |
| 3 | Is there one cohesive When? | Split the scenario |
| 4 | Does every Then describe something observable and specific? | Add the exact message, count, or page |
| 5 | Are there any locators, URLs, or browser names in the text? | Hide in code or configuration |
| 6 | Is the wording identical to similar steps elsewhere? | Standardize |
| 7 | Could this scenario run alone and in any order? | Add missing Givens |
| 8 | Can a non-programmer understand it without help? | Simplify the language |

---

## Code Example: How the Roles Look in Java (Preview)

You will write step definitions fully in the next lesson; here is a short preview so you can see how each keyword's *role* shows up in code. The shared browser is held by a small class called `TestContext`, which Cucumber hands to the step class through its **constructor** (this is called *constructor injection*). You will build `TestContext` properly in *Cucumber Framework Setup*; for now, treat `context.driver()` as "give me this scenario's browser".

```java
package com.revature.qea.steps;

import com.revature.qea.pages.InventoryPage;
import com.revature.qea.pages.LoginPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CartSteps {

    private final TestContext context;     // shared per-scenario state, injected by Cucumber
    private InventoryPage inventory;

    public CartSteps(TestContext context) { // constructor injection: Cucumber supplies the context
        this.context = context;
    }

    @Given("the shopper has an empty cart")                  // ARRANGE: put the system into a state
    public void theShopperHasAnEmptyCart() {
        inventory = new LoginPage(context.driver()).open().loginAs("standard_user", "secret_sauce");
    }

    @When("the shopper adds {string} to the cart")           // ACT: do the thing under test
    public void theShopperAddsToTheCart(String product) {
        inventory.addToCart(product);
    }

    @Then("the cart count shows {int}")                      // ASSERT: compare the observed result
    public void theCartCountShows(int expected) {
        assertEquals(expected, inventory.getCartCount());
    }
}
```

**Line by line:**

- `package ...steps;` places the class in the glue package (the folder Cucumber scans for step definitions; you will configure it in *Cucumber Framework Setup*).
- The imports bring in your page objects, the `TestContext`, the three Cucumber annotations, and JUnit's `assertEquals`.
- `private final TestContext context;` is a field that stores the shared object. `final` means it is set once.
- The **constructor** `public CartSteps(TestContext context)` is what Cucumber calls when it creates this class for a scenario. Because the constructor *asks for* a `TestContext`, the PicoContainer library (added to your `pom.xml` in the setup lesson) creates one and passes it in. If another step class (say `LoginSteps`) also asks for a `TestContext` in the same scenario, it receives the **same** one, so both see the same browser.
- `@Given("the shopper has an empty cart")` registers this method for that exact text. The method body arranges the state: open the login page, log in, and keep the resulting `InventoryPage`. (A fresh login has an empty cart on Sauce Demo, which is how "empty cart" is achieved here.)
- `@When("the shopper adds {string} to the cart")`: `{string}` captures the quoted product name into the `String product` parameter. The body only calls a page-object action.
- `@Then("the cart count shows {int}")`: `{int}` converts the captured digits into an `int`. This is the only method containing an assertion, comparing the expected value from the feature text to the actual value read by the page object.

Notice that the *Given* and *When* call page-object actions, and the *Then* is the only method with an assertion. Do not worry about the annotations and `{string}` / `{int}` yet; they are the subject of the next lesson. (How the driver is created, shared, and closed per scenario is covered in *Cucumber Framework Setup* today and fully with hooks on Friday.)

---

## Guided Lab: Rewrite and Run Three Scenarios

**Goal:** practice turning a rough idea into a clean Given/When/Then scenario, in the same style you will use for Project 2. No Java required for this lab; you will implement these in the next lessons.

1. Create a file `lab-gwt.feature` in a scratch folder (or in `src/test/resources/features` if your project exists).
2. Type the feature header:

   ```gherkin
   Feature: Shopping cart
     As a shopper
     I want to manage the items in my cart
     so that I only buy what I intend to
   ```

   (The three lines after `Feature:` are free-text description; Cucumber ignores them but readers do not.)
3. Open `https://www.saucedemo.com`, log in with `standard_user` / `secret_sauce`, and perform the action "add the Sauce Labs Backpack". **Observe** what changes on screen (the button text and the cart badge). Write those observations on paper: they are your Then material.
4. Write scenario 1 using only the observations from step 3:

   ```gherkin
   Scenario: Adding a product increases the cart count
     Given the shopper is on the products page
     When the shopper adds "Sauce Labs Backpack" to the cart
     Then the cart count shows 1
   ```
5. Now click **Remove** on the same product and observe again. Write scenario 2 yourself. The expected result is that the badge disappears. Use a Given that sets the starting state ("has the product in the cart"), one When, one Then.
6. Log out, try logging in with an empty username, and note the exact error text. Write scenario 3 for the login page using a declarative When.
7. Run the checklist from Section 13 on all three scenarios. Mark each question yes/no and fix every "no".
8. Swap files with your partner. Each of you reads the other's scenarios aloud *as a customer would* and says what they understood. Anything that needed explanation is a wording bug.

**Expected result:** three short scenarios, each with one When, observable Thens, no locators, and consistent wording such as "the shopper" and "the cart count". A model answer for scenario 3:

```gherkin
Scenario: Login is rejected when the username is empty
  Given the customer is on the login page
  When the customer logs in with an empty username and password "secret_sauce"
  Then the error message "Epic sadface: Username is required" is displayed
```

---

## Troubleshooting: Symptoms That Point to Given/When/Then Problems

These are problems you will notice once your scenarios start to run (next lessons). Learn to connect the symptom to the wording cause.

| Symptom | Likely wording cause | Fix |
|---|---|---|
| Scenario passes alone but fails after another scenario | A missing Given; hidden dependence on leftover state (for example a cart that was not empty) | Add explicit Givens; never rely on scenario order |
| Failure message is `expected: <1> but was: <2>` and nobody knows why | Several behaviors in one scenario | Split into scenarios with one When |
| Dozens of near-duplicate step definitions | Inconsistent wording | Agree a glossary; parameterize values |
| One UI change breaks 40 scenarios | Imperative wording tied to the UI | Rewrite declaratively; push the details into page objects |
| Stakeholders refuse to read the features | Technical wording (ids, URLs, HTTP) | Rewrite in business language |
| Cucumber reports `Undefined` for a step that "looks the same" | Curly quotes, an extra space, or different wording | Compare text character by character; copy from the snippet |
| `Then` step "passes" even when the app is wrong | The assertion is missing or too loose (for example only checks that an element exists) | Assert the exact expected value |

A real console fragment you will see when a Then is too loose and a scenario fails for the right reason, for contrast:

```
Scenario: Adding a product increases the cart count   # features/cart.feature:3
  Given the shopper has an empty cart                 # CartSteps.theShopperHasAnEmptyCart()
  When the shopper adds "Sauce Labs Backpack" to the cart   # CartSteps.theShopperAddsToTheCart(String)
  Then the cart count shows 1                         # CartSteps.theCartCountShows(int)
      org.opentest4j.AssertionFailedError: expected: <1> but was: <0>
```

Diagnosis: Given and When passed; the failing line is a **Then**, so the application did not produce the promised outcome (here, the click did not register or the badge was not updated). Because the scenario has one When, you know exactly which action to investigate.

---

## Practice Exercises

1. **Classify.** Label each line as Given, When, or Then (or "wrong keyword") and fix those that are misplaced:
   - `the cart has 2 items`
   - `the shopper clicks the checkout button`
   - `the shopper sees "Thank you for your order!"`
   - `the user logs in and sees the products page`
   - `the shopper removes the backpack and the cart is empty`
2. **Rewrite imperative to declarative.**
   - `When I type "Ada" in the first name field, type "Lovelace" in the last name field, type "10001" in the postal code field and click the Continue button`
   - `Then the h3 element with class "complete-header" has the text "Thank you for your order!"`
3. **Mistake hunt.** Identify and fix the problems in:

   ```gherkin
   Scenario: Cart stuff
     When the shopper adds a backpack
     Then the shopper clicks the cart and sees the backpack
     And it works
   ```
4. **One behavior.** Split into two scenarios: *"Given I am logged in, When I add a backpack, Then the count is 1, When I remove the backpack, Then the count is 0."*
5. **Write from a rule.** For the rule "An item that is already in the cart shows a Remove button instead of Add to cart", write a complete scenario.
6. **Reuse audit.** Here are five steps from different files. Standardize them to one wording: `the user has logged in`, `I am logged in`, `a logged-in customer`, `the customer logs into the site`, `user is authenticated`.
7. **Pair exercise.** One partner writes only Givens and Thens for a "remove item from cart" feature; the other adds the Whens. Discuss whether the scenario is still understandable.
8. **Map to code.** For each step in your login scenarios, decide which **page-object method** it would call, and whether it is an action or a query.
9. **Missing Given.** The following scenario fails when run after another scenario that left two items in the cart. Explain why and fix it:

   ```gherkin
   Scenario: Cart count after adding
     When the shopper adds "Sauce Labs Bike Light" to the cart
     Then the cart count shows 1
   ```
10. **Sort by hand.** On `saucedemo.com`, sort the products by "Price (low to high)". Write one scenario with an exact, observable Then. (Hint: what can a shopper *see* that proves the order is right?)
11. **Level check.** Rewrite this scenario so every step is at one level of abstraction:

    ```gherkin
    Scenario: Checkout
      Given the shopper is logged in
      When the shopper clicks the div with class "inventory_item_name" containing "Backpack"
      Then the customer buys it
    ```
12. **Project 2 draft.** From one acceptance criterion in your pair's Project 2 user story, write a Given/When/Then scenario, run the Section 13 checklist on it, and have the other pair review it as the "tester" amigo.

---

## Solutions and Hints

**1. Classify.**

- `the cart has 2 items` is a **Given** (state).
- `the shopper clicks the checkout button` is a **When** (action).
- `the shopper sees "Thank you for your order!"` is a **Then** (observation).
- `the user logs in and sees the products page` mixes a When and a Then in one line. Split: `When the user logs in with ...` and `Then the user sees the products page`.
- `the shopper removes the backpack and the cart is empty` mixes a When and a Then. Split into `When the shopper removes "Sauce Labs Backpack" from the cart` and `Then the cart is empty`.

**2. Declarative rewrites.**

- `When the shopper continues with first name "Ada", last name "Lovelace" and postal code "10001"`
- `Then the shopper sees the confirmation message "Thank you for your order!"`

The CSS class and element type are locators; they belong in a page object.

**3. Mistake hunt.** Problems: vague title; no Given (hidden state); `adds a backpack` is not parameterized or specific; the Then contains an action (`clicks the cart`); `it works` is not observable. Fix:

```gherkin
Scenario: Added product is listed in the cart
  Given the shopper is on the products page
  When the shopper adds "Sauce Labs Backpack" to the cart
  And the shopper opens the cart
  Then the cart lists "Sauce Labs Backpack"
```

(Two Whens are justified: adding and opening are one cohesive path to viewing; if you prefer strictness, put the add in a Given and keep one When: `opens the cart`.)

**4. One behavior.**

```gherkin
Scenario: Adding a product increases the cart count
  Given the shopper is logged in
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1

Scenario: Removing a product decreases the cart count
  Given the shopper is logged in
  And the shopper has "Sauce Labs Backpack" in the cart
  When the shopper removes "Sauce Labs Backpack" from the cart
  Then the cart is empty
```

**5. From a rule.**

```gherkin
Scenario: An added product offers Remove instead of Add to cart
  Given the shopper is on the products page
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the "Sauce Labs Backpack" product offers "Remove"
```

**6. Reuse audit.** Choose `the shopper is logged in` for all five (it is a state, third person, plain wording). One step definition replaces five.

**7. Pair exercise (hint).** Check the middle: if the reader cannot guess the When from the Given and Then alone, the scenario is under-specified; if they can, the Given/Then are doing their job. Either result is useful feedback.

**8. Map to code (sample).** `the customer is on the login page` calls `loginPage.open()` (action); `the customer logs in with ...` calls `loginPage.loginAs(...)` (action); `the customer sees the products page` calls `inventoryPage.isLoaded()` (query, then assert).

**9. Missing Given.** The scenario does not say how many items are in the cart before it starts, so the count after adding depends on previous scenarios (2 + 1 = 3). Add `Given the shopper is logged in` and `And the shopper has an empty cart`.

**10. Sort by hand (sample).**

```gherkin
Scenario: Products can be sorted from the cheapest to the most expensive
  Given the shopper is on the products page
  When the shopper sorts the products by "Price (low to high)"
  Then the first product listed is "Sauce Labs Onesie"
```

The cheapest product on Sauce Demo is the Onesie at 7.99 (check the site, since sample data can change). Alternative Then: `the product prices are listed in ascending order`.

**11. Level check.**

```gherkin
Scenario: A shopper can complete a purchase
  Given the shopper has "Sauce Labs Backpack" in the cart
  When the shopper completes checkout with valid details
  Then the shopper sees the confirmation message "Thank you for your order!"
```

`the customer buys it` was too vague to be an assertion, and the `div` class was a locator.

**12. Project 2 draft (hint).** Start from the acceptance criterion's *example data*. Each criterion usually becomes one scenario. If an acceptance criterion needs two Whens, it probably contains two criteria.

---

## Self-Check Questions

1. **Which keyword describes the state before the behavior, and which test phase does it correspond to?**
   Given; Arrange.
2. **Why should a Then be observable?**
   Because it states what can be verified from outside the system, which makes it testable by anyone and avoids tying the specification to implementation details.
3. **Does Cucumber treat `And` differently from `Given`?**
   No. Keywords are not used for matching; only the text after the keyword is.
4. **A scenario has `When`, `Then`, `When`, `Then`. What should you do?**
   Split it into two scenarios; each is one behavior with one When.
5. **Why is `Given the shopper clicks the login button` a weak Given?**
   It describes an action rather than a state, which blurs what the scenario is testing.
6. **Where should assertions live: page objects or Then step definitions?**
   In Then step definitions. Page objects only perform actions and return values.
7. **What does a missing Given usually cause?**
   Hidden dependence on leftover state, so the scenario passes or fails depending on what ran before it.
8. **How does constructor injection help step classes?**
   Cucumber passes the same `TestContext` object to every step class in a scenario, so all of them use the same browser without static variables.

---

## Summary

- **Given** = context/state (Arrange); **When** = the action under test (Act); **Then** = the observable outcome (Assert). `And`/`But` continue the previous role.
- **Given** describes state, not actions; **When** has typically **one** action; **Then** states **observable**, specific results and performs **no actions**.
- Cucumber matches steps by text only; the keywords are for **readers** and discipline.
- Prefer **declarative**, business-level wording, with a **consistent level of abstraction** across the scenario.
- Keep wording **consistent and parameterized** for reuse; include only the details that **matter** to the rule.
- Typical mistakes: assertions in Given/When, actions in Then, multiple behaviors, vague outcomes, hidden state, and UI scripting.
- In code, Given/When call **page-object actions**; Then performs **assertions**, which keeps page objects assertion-free. Step classes receive the shared `TestContext` through their constructor.
- Use the quality checklist on every scenario before you commit it. Scenario Outlines, Background, and tags, which reduce repetition further, are covered in depth on Friday.

---

## Additional Resources

- Cucumber documentation, *Gherkin reference: Given, When, Then*: https://cucumber.io/docs/gherkin/reference/#steps
- Martin Fowler, *GivenWhenThen*: https://martinfowler.com/bliki/GivenWhenThen.html
- Cucumber documentation, *Writing better Gherkin*: https://cucumber.io/docs/bdd/better-gherkin/
