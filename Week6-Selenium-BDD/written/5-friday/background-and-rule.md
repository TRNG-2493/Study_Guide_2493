# Background and Rule

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a `Background` is and how it removes **repeated Given steps** from a feature file.
- Describe **when** the background runs (before **each** scenario and each outline row) and how it interacts with **hooks**.
- Trace the exact **execution order** of hooks, Background steps, and scenario steps for ordinary scenarios and outline rows.
- Write a good background (short, relevant to **every** scenario, only Given steps) and recognize and rewrite bad ones.
- Explain what a `Rule` is, why it was added to Gherkin, and how it groups scenarios under the **business rule** they illustrate.
- Use `Background` inside a `Rule`, and predict the combined order of feature and rule backgrounds.
- Compare `Background` with alternatives (hooks, higher-level Given steps, Scenario Outlines) and choose the right one.
- Diagnose common problems (failing Background, slow suites caused by heavy Backgrounds, misplaced keywords).

---

## Why This Matters

### The repetition problem

In the *Features and Scenarios* lesson you wrote this cart feature, and we promised a better way for the repeated first line:

```gherkin
Scenario: Adding a product increases the cart count
  Given the shopper is logged in
  When ...

Scenario: Removing the only product empties the cart
  Given the shopper is logged in
  And the shopper has "Sauce Labs Backpack" in the cart
  When ...

Scenario: The cart is kept when the shopper continues shopping
  Given the shopper is logged in
  And ...
```

Each scenario repeats `Given the shopper is logged in`. It is a small repetition, but across a feature of ten scenarios it becomes noise that hides the interesting part of each scenario. A reader skimming the file has to read the same line ten times to learn nothing new. **`Background`** removes it.

### The structure problem

Larger features also contain several **business rules** (for example, "free shipping above $100", "maximum five items per order"), each illustrated by a handful of scenarios. A flat list of twelve scenarios hides this structure; the reader cannot see which scenarios belong together. **`Rule`** makes the structure visible. Together these two keywords make your Project 2 BDD layer shorter and clearer.

### Two analogies

- **Background is like setting the table before every meal.** Whatever is served (soup, pasta, dessert), the table is set the same way first. You do not repeat "set the table" in each recipe; you state it once as the standing preparation. But note: the table is set again for every meal, not once a week.
- **Rule is like the chapter headings in a rulebook.** A board-game rulebook does not list 40 loose examples; it has chapters ("Moving", "Capturing") and examples inside each chapter. A feature with `Rule`s reads like that rulebook.

### Where this fits in today's work

This lesson is part of the **Project 2 BDD layer milestone** ("complete the BDD layer with tags and a report"). Your saucedemo.com features for cart and checkout should end today with a Background that holds the login, Rules where a feature has several business rules, and no repeated lines. It builds on step definitions and page objects from Thursday, and it connects to the next two lessons: the *Hooks* lesson (technical setup that runs before the Background) and the *Tags* lesson (which can be placed on a Rule).

---

## The Concept

### 1. Background

**Definition.** A **`Background`** contains steps that are **run before each scenario** in the feature (or in the `Rule`, see below). It is the place for the **shared context** that every scenario needs.

**What it does, why, and where.** It *removes repeated Given steps* so each scenario can start with the interesting part. It lives directly after the `Feature:` line and description, before the first scenario.

```gherkin
Feature: Shopping cart
  As a shopper
  I want to manage the products in my cart
  so that I only buy the items I really want

  Background:
    Given the shopper is logged in

  Scenario: Adding a product increases the cart count
    When the shopper adds "Sauce Labs Backpack" to the cart
    Then the cart count shows 1

  Scenario: Removing the only product empties the cart
    Given the shopper has "Sauce Labs Backpack" in the cart
    When the shopper removes "Sauce Labs Backpack" from the cart
    Then the cart is empty
```

**Line-by-line explanation**

| Line | Meaning |
|---|---|
| `Feature: Shopping cart` and the three-line description | The feature title and the user story that motivates it |
| `Background:` | Starts the shared context; it has no title requirement (you may add one) |
| `Given the shopper is logged in` | A normal Given step, matched by an ordinary step definition (the one from Thursday that opens the login page, types the credentials, and clicks Login) |
| `Scenario: Adding a product ...` | First scenario. Notice it begins with `When`: the login is already provided by the Background |
| `When the shopper adds "Sauce Labs Backpack" to the cart` | The action under test |
| `Then the cart count shows 1` | The expected result |
| Second scenario's extra `Given the shopper has "Sauce Labs Backpack" in the cart` | Context needed only by this scenario, so it stays here and not in the Background |

How it behaves: Cucumber **prepends** the Background's steps to **every** scenario, as if you had typed them yourself. The second scenario above runs as `Given the shopper is logged in` then `Given the shopper has "Sauce Labs Backpack" in the cart` then `When ...` then `Then ...`.

Facts to remember:

| Fact | Detail |
|---|---|
| Position | After the `Feature:` line and description, **before** the first scenario |
| Number | **At most one** `Background` per feature (and one per `Rule`) |
| Runs | Before **every** scenario (and before every **row** of a `Scenario Outline`), **not** once per feature |
| Fresh state | Because it re-runs each time, each scenario starts from the same state, keeping scenarios independent |
| Reports | The background steps appear at the top of every scenario in console output and reports |
| Name | You may name it (`Background: Logged-in shopper`) and add a short description |
| Tags | A Background **cannot** be tagged; tags go on features, rules, scenarios, and examples |
| Failure | If a Background step fails, the scenario fails and its remaining steps are skipped |

**Important:** the Background runs **once per scenario**, not once per feature. A "login" background therefore logs in again for every scenario, which costs time (as it would if repeated manually), but keeps scenarios isolated. Independence is worth the time: if scenario 4 left the cart full, a shared single login would pass a dirty cart to scenario 5.

### 2. Background and Hooks: Order of Execution

For each scenario the order is:

```
1. @Before hooks            (e.g., start the browser)           -- Hooks lesson
2. Background steps         (shared Given steps)
3. Scenario steps
4. @After hooks             (e.g., screenshot on failure, quit the browser)
```

So the browser already exists when the Background's `Given the shopper is logged in` executes. This ordering is why **technical setup** (creating the driver) belongs in **hooks**, and **business context** (being logged in) belongs in the **Background**: the Background is *visible to the business reader*, hooks are not.

#### Trace 1: a feature with a Background and two scenarios

Feature as above (Background has one step; scenario A has two steps, scenario B has three). The run is:

```
-- Scenario A: Adding a product increases the cart count --
@Before                                  browser A opens
  Background: Given the shopper is logged in
  Scenario:   When the shopper adds "Sauce Labs Backpack" to the cart
  Scenario:   Then the cart count shows 1
@After                                   browser A closes

-- Scenario B: Removing the only product empties the cart --
@Before                                  browser B opens
  Background: Given the shopper is logged in        <- runs AGAIN
  Scenario:   Given the shopper has "Sauce Labs Backpack" in the cart
  Scenario:   When the shopper removes ...
  Scenario:   Then the cart is empty
@After                                   browser B closes
```

#### Trace 2: Background with a Scenario Outline

An outline with three `Examples` rows is three scenarios, so the Background runs **three times**:

```
Feature has Background + Scenario Outline with 3 rows
   row 1: @Before -> Background -> outline steps -> @After
   row 2: @Before -> Background -> outline steps -> @After
   row 3: @Before -> Background -> outline steps -> @After
```

The Background steps cannot use `<placeholders>` of the outline, because the Background belongs to the feature, not to the outline. If a Background step needs different data per row, it is not shared context: move it into the outline.

#### Trace 3: when the Background fails

Suppose the shop is down and `Given the shopper is logged in` throws an exception:

```
@Before                    runs, browser opens
  Background: Given the shopper is logged in     FAILED
  When ...                                       SKIPPED
  Then ...                                       SKIPPED
@After                     STILL runs (screenshot, quit browser)
```

Important consequence: **every scenario in the feature fails at the same step**. When you see a whole feature turn red with the same message in the Background, suspect the environment or the login step, not ten separate bugs.

### 3. What Belongs in a Background (and What Does Not)

**Good backgrounds:**

- Are **short**, 1-4 lines.
- Contain only **Given** steps (context), not When or Then.
- Contain only context that is **relevant to every** scenario in the feature.
- Describe **business** context ("the shopper is logged in", "the catalog contains 6 products"), not technical setup.

**Rules of thumb:**

1. If **only some** scenarios need a step, keep it in those scenarios (or in a `Rule` with its own Background, see below).
2. A background step should **matter to the reader**. If readers would not care ("the browser is open"), use a hook.
3. Do **not** put a `When` or `Then` in the Background. A Background is *not* a scenario; it sets the scene.
4. **Keep it close to the scenarios**: if the Background is long, readers must scroll to remember what the context is. A background of 10 lines is a smell.
5. Do not use it for **data that the scenarios need to see** to understand the rule: if the *amount in the cart* determines the outcome, put it in each scenario where it is visible.

**Bad background (too long, mixed purposes):**

```gherkin
Background:
  Given the browser is open
  And the database has been reset
  And the user "standard_user" exists
  And the shopper is on the login page
  And the shopper logs in with "standard_user" and "secret_sauce"
  And the shopper adds "Sauce Labs Backpack" to the cart
  And the shopper opens the cart
  And a coupon "SAVE10" exists
```

Problems: browser/database setup is technical (hooks), the cart steps are needed by only some scenarios, and the sheer length hides what each scenario is about. A better version:

```gherkin
Background:
  Given the shopper is logged in
```

and a higher-level step inside scenarios that need a prefilled cart (`Given the shopper has "Sauce Labs Backpack" in the cart`), whose Java implementation does the several UI actions.

#### Good-versus-bad rewrite: hiding the key data

Bad:

```gherkin
Background:
  Given the shopper has products worth 100.00 in the cart

Scenario: Free shipping
  When the shopper views the shipping cost
  Then the shipping cost is 0.00

Scenario: Shipping charged below the threshold
  When the shopper views the shipping cost
  Then the shipping cost is 5.99
```

The second scenario is wrong (or magical): the cart value that *causes* the result is hidden in the Background, and the two scenarios cannot both be right with the same context. Good: move the value into each scenario (or an outline), where it is visible next to the result it explains.

#### Good-versus-bad rewrite: a When in the Background

Bad: `Background: When the shopper adds a product`. Business readers cannot tell whether adding is "context" or "the thing being tested". Good: express the starting state as a Given: `Given the shopper has "Sauce Labs Backpack" in the cart`.

### 4. Background vs. Alternatives

| Need | Best tool | Why |
|---|---|---|
| Start the browser, quit it, take screenshots | **Hooks** (`@Before`, `@After`) | Technical, not business-visible |
| The same business context for **every** scenario | **Background** | Visible, removes repetition |
| Context needed by **some** scenarios | A **high-level Given step** in each, or a `Rule` with its own Background | Keeps the other scenarios clean |
| Heavy, slow setup (create test data via API) | A Given step that calls an API, or a tagged hook | Fast and targeted |
| The same steps with different values | **Scenario Outline** | Repeats the scenario with data |

Quick decision questions, in order:

1. Would the business reader care? **No** means a hook.
2. Does **every** scenario in the feature (or rule) need it? **No** means put it in the scenarios or a `Rule`.
3. Is it a **precondition** (Given)? **No** means it is not Background material.
4. Is it under about four lines? **No** means create a higher-level Given step.

### 5. Rule

**Definition.** Gherkin 6 added the **`Rule`** keyword to organize scenarios under the **business rule** they illustrate. A Rule is a heading with a sentence stating one business rule; the scenarios below it are examples of that rule.

```gherkin
Feature: Shipping costs
  As a shopper
  I want to know the shipping cost
  so that I can decide whether to add more items

  Rule: Orders of $100 or more ship free

    Example: Order exactly at the threshold
      Given the shopper has products worth 100.00 in the cart
      When the shopper views the shipping cost
      Then the shipping cost is 0.00

    Example: Order just below the threshold
      Given the shopper has products worth 99.99 in the cart
      When the shopper views the shipping cost
      Then the shipping cost is 5.99

  Rule: Express shipping costs 15.00 extra

    Example: Express shipping on a small order
      Given the shopper has products worth 20.00 in the cart
      When the shopper selects express shipping
      Then the shipping cost is 20.99
```

**Line-by-line explanation**

| Line | Meaning |
|---|---|
| `Rule: Orders of $100 or more ship free` | States a business rule as a sentence; everything below, until the next `Rule`, illustrates it |
| `Example: Order exactly at the threshold` | A scenario (identical in behavior to `Scenario:`). Using `Example` under a `Rule` reads naturally: "an example of this rule" |
| The three steps | Given the cart value, When the shopper views the shipping cost, Then the cost is as the rule dictates. The boundary value 100.00 is a classic choice |
| `Example: Order just below the threshold` | The other side of the boundary (99.99), where the rule does *not* apply |
| `Rule: Express shipping costs 15.00 extra` | A second, independent rule with its own example |

Details:

| Aspect | Explanation |
|---|---|
| **Purpose** | Group scenarios (examples) under a business rule; the Rule's title *states* the rule |
| **Where** | Directly inside `Feature:`; contains scenarios |
| **`Example:`** | A synonym of `Scenario:`; Gherkin writers often use `Example` under a `Rule` because each example illustrates the rule |
| **Execution** | **No effect on how tests run.** Cucumber runs the examples as ordinary scenarios; `Rule` is for **organization and documentation** |
| **Reports** | The rule name is shown in reports above its scenarios (depending on the reporter) |
| **Tags** | Can be tagged (tags on a `Rule` apply to all its scenarios) |
| **Description** | May contain free text under the `Rule:` line explaining it |

Rule titles should state the **business rule as a sentence**: "Orders of $100 or more ship free", not "Shipping tests".

**Why use `Rule`?** It mirrors the **example mapping** technique from the BDD lesson: blue cards (rules) with green cards (examples) underneath. Features with many scenarios become **navigable**: you can see the rules first, then the examples. It also exposes gaps: a rule with only one example is probably under-tested, and a rule with no examples is not yet specified.

**When to use it:** when a feature contains **two or more distinct rules**, each with several examples. For a feature with a single rule, it adds nothing.

### 6. Background Inside a Rule

A `Rule` may have **its own Background**, which applies only to the scenarios in that rule, **in addition to** the feature-level Background:

```gherkin
Feature: Checkout

  Background:
    Given the shopper is logged in

  Rule: A shipping address is required

    Background:
      Given the shopper has "Sauce Labs Backpack" in the cart
      And the shopper is on the checkout information page

    Example: Postal code is missing
      When the shopper continues with first name "Ada", last name "Lovelace" and no postal code
      Then the error message "Error: Postal Code is required" is displayed

    Example: Last name is missing
      When the shopper continues with first name "Ada", no last name and postal code "10001"
      Then the error message "Error: Last Name is required" is displayed

  Rule: An empty cart cannot be checked out

    Example: Checkout with an empty cart is not offered
      Given the shopper has an empty cart
      When the shopper opens the cart
      Then the checkout button is not available
```

Execution order for the first example: **feature Background** (`logged in`) then **rule Background** (cart + checkout page) then **scenario steps**. In the second rule only the feature Background applies.

Expanded trace for "Postal code is missing":

```
@Before
  1. Given the shopper is logged in                                 (feature Background)
  2. Given the shopper has "Sauce Labs Backpack" in the cart        (rule Background)
  3. And   the shopper is on the checkout information page          (rule Background)
  4. When  the shopper continues with ... no postal code            (scenario)
  5. Then  the error message "Error: Postal Code is required" ...   (scenario)
@After
```

Constraints: **one Background per feature and per rule**, and the feature Background must come **before** the first `Rule`. (Saucedemo's error texts for the checkout information form are "Error: First Name is required", "Error: Last Name is required" and "Error: Postal Code is required".)

### 7. Choosing the Structure of a Feature

```
Small feature (3-6 scenarios, one rule)        -> Feature + (optional Background) + Scenarios
Medium feature with repetitive data            -> add Scenario Outline(s)
Large feature with several business rules      -> Feature + (Background) + Rules (each with Examples)
```

Also remember the review question from earlier lessons: *"Is this still one feature?"* If rules are unrelated to each other, split the file.

Outlines and Rules combine well: put a `Scenario Outline` inside a `Rule` when a single rule is illustrated by a table of boundary values.

```gherkin
Rule: Orders of $100 or more ship free

  Scenario Outline: Shipping cost around the threshold
    Given the shopper has products worth <subtotal> in the cart
    When the shopper views the shipping cost
    Then the shipping cost is <shipping>

    Examples:
      | subtotal | shipping |
      | 99.99    | 5.99     |
      | 100.00   | 0.00     |
```

### 8. Step Definitions Do Not Change

Neither `Background` nor `Rule` requires anything new in Java. The background's steps are ordinary steps matched by ordinary step definitions. (You can see this in the output: the background steps appear as normal steps in each scenario.)

Here is the full Java for the Background step used throughout this lesson, to show there is nothing special:

```java
public class LoginSteps {

    private final TestContext context;

    public LoginSteps(TestContext context) {            // injected by PicoContainer
        this.context = context;
    }

    @Given("the shopper is logged in")
    public void theShopperIsLoggedIn() {
        new LoginPage(context.driver())
                .open()
                .login("standard_user", "secret_sauce");
    }
}
```

Line by line: the constructor receives the per-scenario `TestContext` (the dependency injection you set up on Thursday). `@Given("the shopper is logged in")` binds the step text. `context.driver()` returns this scenario's browser. The `LoginPage` page object opens saucedemo.com, enters the credentials, and clicks Login. Nothing in the method knows or cares whether the step was written in a Background or in a scenario.

### 9. Troubleshooting

| Symptom | Likely cause | Diagnosis and fix |
|---|---|---|
| Parse error mentioning "Background" after a scenario | The Background was placed **after** a scenario | Move it directly below the `Feature:` description |
| Parse error with a second Background | Two backgrounds in one feature (or rule) | Merge them, or move the extra into a `Rule` |
| Every scenario fails at the first step | The Background step is failing (wrong URL, site down, changed locator) | Read the first failing step; fix once |
| Suite is very slow | A long Background (login + several UI steps) repeated for every scenario and row | Shorten it; use a faster way to reach the state in the step implementation |
| Scenario passes alone, fails after others | Background does not reset a state | Make the Background establish the full starting state (for example, `has an empty cart`) |
| `Rule` title appears but nothing changes in execution | Expected: Rule is organizational only | Use tags if you want to select by rule |
| Steps in the Background do not accept an outline placeholder | The Background is outside the outline | Move the step into the outline |

---

## Hands-On Lab: Refactor the Cart Feature and Watch the Order

Goal: remove repeated lines with a Background, group scenarios with Rules, and **prove** the execution order with console output.

1. Open `src/test/resources/features/shopping-cart.feature` from Thursday (or create it with the "Complete Example" content below, minus the Background and Rule keywords, to see the "before" state).
2. Add a temporary demo class that prints when hooks run. (Hooks are explained in the next lesson; for now just copy it into `src/test/java/com/revature/qea/steps/OrderDemoHooks.java`.)

   ```java
   package com.revature.qea.steps;

   import io.cucumber.java.After;
   import io.cucumber.java.Before;

   public class OrderDemoHooks {

       @Before
       public void before() {
           System.out.println("[HOOK] @Before");
       }

       @After
       public void after() {
           System.out.println("[HOOK] @After");
       }
   }
   ```

   Explanation: `@Before` and `@After` are Cucumber hooks, methods that Cucumber calls automatically before and after every scenario.
3. In your `shopper is logged in` step, add `System.out.println("[STEP] logged in");` as the first line, and add a similar print to one `When` step: `System.out.println("[STEP] when");`.
4. Move the repeated `Given the shopper is logged in` into a `Background:` (see the complete example) and save.
5. Run only the cart feature: `mvn test -Dcucumber.features=src/test/resources/features/shopping-cart.feature`. (If your runner already selects features through a resource path, simply run `mvn test`.)
6. Expected console order for **each** scenario (the first scenario shown):

   ```
   [HOOK] @Before
   [STEP] logged in
   [STEP] when
   [HOOK] @After
   ```

   Confirm that `[STEP] logged in` appears once per scenario, not once per feature, and that `[HOOK] @Before` always comes first.
7. Add the `Rule:` headings and, in the second rule, the rule-level Background with `Given the shopper has "Sauce Labs Backpack" in the cart`. Rerun and note that the Backpack step now also appears at the top of both removal scenarios.
8. Change the Background so its step fails on purpose (for example, use the wrong password inside the step) and rerun. Confirm the pattern from Trace 3: every scenario fails at the Background, the other steps are skipped, and `[HOOK] @After` still prints.
9. Restore the step, delete the print statements and `OrderDemoHooks` (or keep it for the next lesson), and commit with a message such as `Use Background and Rules in the cart feature`.

---

## Complete Example

`src/test/resources/features/shopping-cart.feature`

```gherkin
Feature: Shopping cart
  As a shopper
  I want to manage the products in my cart
  so that I only buy the items I really want

  Background:
    Given the shopper is logged in

  Rule: Adding a product puts it in the cart

    Example: Adding one product
      When the shopper adds "Sauce Labs Backpack" to the cart
      Then the cart count shows 1
      And the cart contains "Sauce Labs Backpack"

    Example: Adding two different products
      When the shopper adds "Sauce Labs Bike Light" to the cart
      And the shopper adds "Sauce Labs Onesie" to the cart
      Then the cart count shows 2

  Rule: Removing a product takes it out of the cart

    Background:
      Given the shopper has "Sauce Labs Backpack" in the cart

    Example: Removing the only product empties the cart
      When the shopper removes "Sauce Labs Backpack" from the cart
      Then the cart is empty

    Example: Removing one of two products keeps the other
      Given the shopper has "Sauce Labs Onesie" in the cart
      When the shopper removes "Sauce Labs Backpack" from the cart
      Then the cart contains "Sauce Labs Onesie"
      And the cart count shows 1
```

**Reading it step by step**

1. `Background` (feature level): the login runs before all four examples.
2. First rule: two examples, no rule-level Background, so each runs *login*, then its own steps.
3. Second rule: has its own Background, so each of its two examples runs *login*, then *Backpack in the cart*, then its own steps.
4. In the last example the scenario adds a **second** product with its own `Given`; a scenario can add to the context established by backgrounds.

Total: four scenarios, four logins, and two extra "Backpack in the cart" setups. Compare with the Thursday version: no repeated login lines, and the structure of rules is visible at a glance.

---

## Practice Exercises

1. **Refactor.** Take Thursday's `shopping-cart.feature` and move the repeated `Given the shopper is logged in` into a `Background`. Run it and observe where the background steps appear in the output.
2. **Run order.** Add print statements to a `@Before` hook (hooks are the next lesson; use the demo class from the lab), a Background step, and a scenario step. Confirm the order.
3. **Good or bad?** For each candidate step, decide Background, scenario, or hook: (a) "the browser is Chrome", (b) "the shopper is logged in", (c) "the shopper has two products in the cart" (only 3 of 8 scenarios need it), (d) "the shop's database is reset".
4. **Rules.** Take the acceptance criteria for sorting from the *User Stories* lesson and organize them into **three `Rule`s**, each with at least two examples.
5. **Nested background.** Write a checkout feature with a feature-level Background and a Rule-level Background. Predict the order of the executed steps for one scenario and verify with a run.
6. **Find the smell.** What is wrong with a Background that contains `When the shopper adds a product` and `Then the cart count shows 1`?
7. **Compare outputs.** Run a feature with Background and one with the steps copied into each scenario. What is the same, and what differs?
8. **Count the runs.** A feature has a one-step Background, 3 plain scenarios, and one outline with 4 rows. How many times does the Background run?
9. **Fix the structure.** The Background below sits in the wrong place and contains a mix of problems. Rewrite the file.

   ```gherkin
   Feature: Wishlist
     Scenario: Add item
       Given the shopper is logged in
       When the shopper wishes for "Sauce Labs Onesie"
       Then the wishlist has 1 item

     Background:
       Given the browser is open
       And the shopper is logged in
       When the shopper opens the wishlist
   ```
10. **State the rule.** Rewrite these three poor Rule titles as business-rule sentences: "Shipping", "Cart tests", "Checkout validation".
11. **Outline inside a Rule.** Take your shipping boundaries from the *Scenario Outline and Examples* lesson and place the outline inside a `Rule: Orders of $100 or more ship free`.
12. **Project 2.** Apply `Background` (and `Rule` where several rules exist) to your Project 2 features. Keep each Background to four lines or fewer, and run the whole suite to prove nothing broke.

---

## Solutions and Hints

**1.** The Background lines appear at the top of every scenario in the console output, identical to the step lines you removed, because Cucumber prepends them.

**2.** Order per scenario: `[HOOK] @Before`, Background step, scenario steps, `[HOOK] @After`.

**3.** (a) Hook or configuration: it is a technical choice (browser), not a business step. (b) Background, if all scenarios need it. (c) In the scenarios that need it (or in a Rule containing only those scenarios): not everyone needs it. (d) Hook (or an API call in a tagged hook): technical, not business-visible.

**4.** A sample structure: `Rule: Products can be sorted by name` (A to Z, Z to A examples), `Rule: Products can be sorted by price` (low to high, high to low), `Rule: The chosen sort order is shown` (the dropdown displays the selected option). Each Rule needs two examples; check that each title is a sentence.

**5.** Expected order: feature Background steps, rule Background steps, scenario steps. If your run shows a different order, check that the feature Background is above the first `Rule`.

**6.** A Background is for **context (Given)**. A `When` and a `Then` turn it into a hidden test that runs before every scenario, making failures confusing and duplicating assertions. Fix: remove them; put the add action into the scenarios that need it, expressed as `Given the shopper has "<product>" in the cart`.

**7.** The step results and order are the same, because Cucumber prepends the Background. Differences: the feature file is shorter, and the report may mark the Background steps as background steps.

**8.** 3 + 4 = **7** times (each plain scenario and each outline row).

**9.**

```gherkin
Feature: Wishlist
  As a shopper
  I want to keep a wishlist
  so that I can buy things later

  Background:
    Given the shopper is logged in

  Scenario: Adding an item to the wishlist
    When the shopper wishes for "Sauce Labs Onesie"
    Then the wishlist has 1 item
```

Fixes: Background moved directly under the Feature; `the browser is open` removed (hook); the `When` removed (not a Given); the duplicate login line from the scenario removed.

**10.** For example: "Orders of $100 or more ship free"; "Removing a product takes it out of the cart"; "Checkout requires first name, last name, and postal code".

**11.** See the outline inside a Rule in Section 7. Keep the Rule title as the business sentence.

**12.** If the suite's runtime grows noticeably, check whether the Background does more than login.

---

## Self-Check Questions

**Q1. When does the Background run?**
Before every scenario (and every outline row) in its feature or rule, after the `@Before` hooks.

**Q2. Where does a Background go in the file?**
Directly after the `Feature:` line and description, before the first scenario or rule.

**Q3. Which keywords belong in a Background?**
Given steps (And/But continuing them). Not When or Then.

**Q4. Does `Rule` change how tests execute?**
No. It organizes and documents; scenarios run as before.

**Q5. A feature has a Background and a Rule with its own Background. In what order do they run for a scenario in that Rule?**
Feature Background, then Rule Background, then the scenario steps.

**Q6. Why is "the browser is open" a poor Background step?**
It is technical, not business context; put it in a `@Before` hook.

**Q7. If a Background step fails, what happens?**
The scenario fails, the remaining steps are skipped, and `@After` hooks still run.

**Q8. Why might a long Background slow your suite?**
It runs again for every scenario and every outline row, so its cost is multiplied by the number of runs.

---

## Summary

- **`Background`** holds **shared Given steps** that Cucumber runs **before every scenario** (and every outline row) in the feature or rule; it removes repetition while keeping scenarios independent.
- Execution order per scenario: **`@Before` hooks, Background, scenario steps, `@After` hooks**.
- A failing Background fails every scenario at the same point; `@After` still runs.
- Good backgrounds are **short**, **Given-only**, **business-relevant**, and needed by **all** scenarios; technical setup belongs in **hooks**, scenario-specific setup in the scenario.
- **`Rule`** groups scenarios (usually written as `Example`) under a **business rule stated as a sentence**; it affects **organization and reports**, not execution.
- A `Rule` can have its **own Background**, applied after the feature Background; there is **at most one Background per feature and per rule**.
- No new Java code is needed for either keyword.

---

## Additional Resources

- Cucumber documentation, *Gherkin reference: Background*: https://cucumber.io/docs/gherkin/reference/#background
- Cucumber documentation, *Gherkin reference: Rule*: https://cucumber.io/docs/gherkin/reference/#rule
- Cucumber documentation, *Example Mapping*: https://cucumber.io/docs/bdd/example-mapping/
