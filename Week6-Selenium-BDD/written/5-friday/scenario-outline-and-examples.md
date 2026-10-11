# Scenario Outline and Examples

## Learning Objectives

By the end of this lesson you will be able to:

- Recognize the **copy-paste problem** in feature files and explain how a **Scenario Outline** solves it.
- Write a `Scenario Outline` with `<placeholders>` and an `Examples` table, and name each part correctly.
- Explain how Cucumber **expands** an outline into one scenario per example row, and trace what runs (hooks, steps) for every row.
- Write step definitions that work for outlines (Cucumber Expressions with `{string}`, `{int}`, `{double}`).
- Use **multiple `Examples` blocks** (with names and tags) to group data, while keeping **one outcome type per outline**.
- Use placeholders in **scenario titles**, **data tables**, and **doc strings**.
- Distinguish an **`Examples` table** from a step-level **data table**, and know when to choose each.
- Read console output and error messages for outlines, and diagnose the typical failures.
- Decide when an outline is the right tool and when it is overused.

---

## Why This Matters

### The problem: the same scenario, again and again

On Thursday you wrote the login feature with a separate scenario for each wrong-credential case. Look at how repetitive it becomes:

```gherkin
Scenario: Wrong password is rejected
  Given the customer is on the login page
  When the customer logs in with username "standard_user" and password "wrong_password"
  Then the error message "Epic sadface: Username and password do not match any user in this service" is displayed

Scenario: Unknown user is rejected
  Given the customer is on the login page
  When the customer logs in with username "nobody" and password "secret_sauce"
  Then the error message "Epic sadface: Username and password do not match any user in this service" is displayed

Scenario: Locked-out user is rejected
  Given the customer is on the login page
  When the customer logs in with username "locked_out_user" and password "secret_sauce"
  Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed
```

Three scenarios, **identical structure**, different data. Read them again and notice that only two or three words change from one scenario to the next. With ten data combinations the file would be 40+ lines of near-duplicates. If the wording of one step changes (say, "logs in" becomes "signs in"), you must edit it ten times, and you will eventually miss one. This is exactly the copy-paste explosion described in the *Features and Scenarios* lesson.

### The idea: a form letter with blanks

Think of a **form letter** used by a school office: "Dear ______, your exam on ______ is at ______." The office writes the letter **once** and fills in the blanks for every student. A **Scenario Outline** is the same thing for tests: you write the scenario **once** with blanks (placeholders) and supply a table of values. Cucumber "mails" one copy of the scenario for every row.

### Where it fits in your project

A Scenario Outline is one of the most heavily used features of Gherkin. It is part of the **BDD layer you complete in the Project 2 milestone today**: the exercise "complete the Project 2 BDD layer with tags and a report" expects your saucedemo.com login validation and sorting scenarios to be compact, readable outlines that you can then tag (the *Tags* lesson) and report on (the *Cucumber Reporting* lesson).

### What you already know that this builds on

| Earlier topic | How it is used today |
|---|---|
| Features and Scenarios | An outline is a special kind of scenario; the Given/When/Then rules still apply |
| Step definitions and Cucumber Expressions (Thursday) | The same `{string}` / `{int}` expressions match the substituted values |
| Page objects and `TestContext` | Each row reuses the same page objects through a fresh `TestContext` |
| `@Before` / `@After` hooks (next lessons in today's sequence) | Run once for every row, because every row is a full scenario |

---

## The Concept

### 1. The Idea

**Definition.** A **Scenario Outline** is a **template** scenario containing **placeholders** written in angle brackets (`<name>`), followed by one or more **`Examples`** tables that supply values. Cucumber runs the template **once for every data row** of the table, substituting the placeholders with that row's values.

```gherkin
Feature: Login validation

  Scenario Outline: Invalid credentials are rejected
    Given the customer is on the login page
    When the customer logs in with username "<username>" and password "<password>"
    Then the error message "<message>" is displayed

    Examples:
      | username        | password       | message                                                                   |
      | standard_user   | wrong_password | Epic sadface: Username and password do not match any user in this service |
      | nobody          | secret_sauce   | Epic sadface: Username and password do not match any user in this service |
      | locked_out_user | secret_sauce   | Epic sadface: Sorry, this user has been locked out.                       |
```

**Line-by-line explanation**

| Line | What it does |
|---|---|
| `Feature: Login validation` | Names the feature; the file can contain any number of scenarios and outlines |
| `Scenario Outline: Invalid credentials are rejected` | Declares a template. Because of the word `Outline`, Cucumber knows to look for an `Examples` table |
| `Given the customer is on the login page` | A normal step with no placeholder: the same text in every run |
| `When ... username "<username>" and password "<password>"` | Two placeholders. `<username>` will be replaced by the cell under the `username` column |
| `Then the error message "<message>" is displayed` | A placeholder for the expected result, so the table documents input and output |
| `Examples:` | Starts the data table that supplies the values |
| First table row (`username`, `password`, `message`) | The **header row**: column names, which must equal the placeholder names |
| Next three rows | Three **examples**; each becomes one executed scenario |

The outline above produces **three scenarios**. The `Examples` table has four lines but only three of them are data; the header never runs.

Anatomy summary:

| Part | Purpose |
|---|---|
| `Scenario Outline:` | Declares a template (`Scenario Template:` is a synonym) |
| `<username>`, `<password>`, `<message>` | **Placeholders**, named after the **column headers** of the table |
| `Examples:` | Introduces the data table (`Scenarios:` is a synonym) |
| First row of the table | **Header row**: the column names |
| Each following row | One **example**: one run of the scenario with those values |

### 2. How Cucumber Expands an Outline

**What happens.** Before running anything, Cucumber turns the outline into ordinary scenarios, one per row. Each placeholder is replaced with the cell value for that row **before the step text is matched** to a step definition. For row 3 the engine effectively sees:

```gherkin
Scenario: Invalid credentials are rejected
  Given the customer is on the login page
  When the customer logs in with username "locked_out_user" and password "secret_sauce"
  Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed
```

**Why this matters.** There are **no special step definitions** for outlines. The same Java methods you wrote for ordinary scenarios work, because by the time matching happens the text is plain:

```java
@When("the customer logs in with username {string} and password {string}")
public void theCustomerLogsIn(String username, String password) {
    loginPage.login(username, password);   // page object from Monday/Thursday
}

@Then("the error message {string} is displayed")
public void theErrorMessageIsDisplayed(String expected) {
    assertEquals(expected, loginPage.errorMessage());
}
```

Explanation of the Java: `@When` tells Cucumber "this method implements a step starting with When"; the quoted text is a **Cucumber Expression**; each `{string}` captures a quoted piece of the step text and passes it, without the quotes, as a `String` parameter, in order. So the first `{string}` becomes `username` and the second becomes `password`.

In console output each row appears as its own scenario with a line reference to the row, for example:

```
Scenario Outline: Invalid credentials are rejected   # login-validation.feature:12
  Given the customer is on the login page
  ...
Scenario Outline: Invalid credentials are rejected   # login-validation.feature:13
```

(The exact layout depends on the plugin; the point is that every row is reported separately with its own line number.) Each expanded scenario is **independent**: a **fresh `TestContext`** (and, with hooks, a fresh browser) is created for every row, and a failure in one row does not stop the others.

#### Execution-order trace for a three-row outline

Assume the `Hooks` class from the next lesson (`@Before` starts the browser, `@After` quits it) and a feature-level Background with one step, `Given the shop is reachable`. For the outline above the run looks like this:

```
Row 1 (standard_user / wrong_password)
  @Before   -> browser 1 starts, new TestContext #1
  Background: Given the shop is reachable
  Given the customer is on the login page
  When  the customer logs in with username "standard_user" and password "wrong_password"
  Then  the error message "Epic sadface: Username and password do not match ..." is displayed
  @After    -> browser 1 quits, TestContext #1 discarded

Row 2 (nobody / secret_sauce)
  @Before   -> browser 2 starts, new TestContext #2
  Background: Given the shop is reachable
  ... same steps with new values ...
  @After    -> browser 2 quits

Row 3 (locked_out_user / secret_sauce)
  ... same pattern ...
```

Key facts from the trace:

1. The hooks and the Background run **three times**, once per row. An outline with 50 rows launches 50 browsers.
2. Rows do **not** share state. Row 2 cannot see a cookie set by row 1.
3. If row 2 fails, rows 1 and 3 still run and keep their own results.

### 3. Placeholders: Where They Can Be Used

Placeholders can appear in:

1. **Step text**: the main use.
2. **The scenario title**: so that each run is identifiable in reports.
3. **Data tables** attached to steps.
4. **Doc strings** attached to steps.

**Placeholder in the title.** Without it, all rows of the login outline would be reported under the same name, "Invalid credentials are rejected", and when a report shows one red row you cannot tell which data failed. With a placeholder:

```gherkin
Scenario Outline: Login with <username> is rejected
  ...
  Examples:
    | username        | ... |
    | locked_out_user | ... |
```

the expanded title becomes `Login with locked_out_user is rejected`. This is very helpful when a row fails in a report, a CI page, or an IDE test tree.

**Placeholder in a data table.** The cell `<product>` inside the step's table is replaced like any other text:

```gherkin
Scenario Outline: Adding <product> twice shows quantity 2
  Given the shopper has an empty cart
  When the shopper adds the following products:
    | product   | quantity |
    | <product> | 2        |
  Then the cart count shows 2

  Examples:
    | product             |
    | Sauce Labs Backpack |
    | Sauce Labs Onesie   |
```

Explanation: the **step's table** (`product`, `quantity`) is attached to the `When` step and is read by the Java method as a `DataTable`. The **`Examples` table** (`product`) belongs to the outline. They are different tables with different jobs (see Section 8). Two scenarios run: one with the Backpack and one with the Onesie.

**Placeholder in a doc string.** The same `<name>` syntax works inside `"""` text:

```gherkin
Scenario Outline: A review for <product> is saved
  When the shopper submits a review for "<product>":
    """
    Great product, would buy again.
    """
```

**Important:** placeholders are **only** substituted in Scenario Outlines. In an ordinary `Scenario`, `<username>` is just literal text.

### 4. Quotes Around Placeholders

Quotes are **not** added by Cucumber. If the step definition uses `{string}`, the quoted text must exist in the step *after substitution*, so put the quotes in the template:

```gherkin
When the customer logs in with username "<username>"     # becomes "standard_user" -> {string} matches
```

For numbers, leave quotes off:

```gherkin
Then the cart count shows <count>                         # becomes 3 -> {int} matches
```

A common mistake is to forget the quotes and then see an **undefined step**, because `{string}` expects them. The mirror-image mistake is to write `"<count>"` for an `{int}` step: the text becomes `"3"` with quotes, which `{int}` does not match.

Which expression fits which kind of cell value:

| Cell value | Template text | Matching expression | Java parameter |
|---|---|---|---|
| `standard_user` | `"<username>"` | `{string}` | `String` |
| `3` | `<count>` | `{int}` | `int` |
| `37.98` | `<total>` | `{double}` | `double` |
| `Sauce Labs Backpack` | `"<product>"` | `{string}` | `String` |

### 5. Empty Cells and Special Characters

- An **empty cell** gives an empty string. With `"<username>"` the step text becomes `""`, which `{string}` matches as an empty string. This is a convenient way to test **empty input**:

  ```gherkin
  Examples:
    | username | password     | message                            |
    |          | secret_sauce | Epic sadface: Username is required |
  ```
- Characters with special meaning in tables need escaping: `\|` (pipe), `\\` (backslash), `\n` (newline).
- Leading and trailing spaces in a cell are trimmed.
- Column widths are cosmetic; align the pipes for readability (your IDE can auto-format).
- A cell **cannot** span lines, so keep cell contents short and readable.

### 6. Multiple `Examples` Blocks

An outline may have **several `Examples` sections**, each with a **name**, optional description, and **tags**. This groups data into meaningful categories and lets you run subsets.

**The golden rule: one outline, one outcome type.** All rows of an outline must lead to the same *kind* of outcome (all rejected with an error message, or all successful). If some rows succeed and others fail, the `Then` step becomes vague ("the customer sees the result") and the scenario stops being readable. Use several `Examples` blocks to group rows that share an outcome but differ in *reason* or *priority*.

**Good: one outcome type (every row is rejected), two blocks for two reasons:**

```gherkin
Scenario Outline: Login with <description> is rejected
  Given the customer is on the login page
  When the customer logs in with username "<username>" and password "<password>"
  Then the error message "<message>" is displayed

  @validation
  Examples: Missing credentials
    | description       | username      | password     | message                            |
    | an empty username |               | secret_sauce | Epic sadface: Username is required |
    | an empty password | standard_user |              | Epic sadface: Password is required |

  @authentication
  Examples: Incorrect credentials
    | description       | username        | password       | message                                                                   |
    | a wrong password  | standard_user   | wrong_password | Epic sadface: Username and password do not match any user in this service |
    | a locked-out user | locked_out_user | secret_sauce   | Epic sadface: Sorry, this user has been locked out.                       |
```

**The successful logins are a different outcome, so they get their own outline:**

```gherkin
Scenario Outline: <username> can log in and sees the products
  Given the customer is on the login page
  When the customer logs in with username "<username>" and password "secret_sauce"
  Then the customer sees the products page

  @smoke
  Examples: Core user
    | username      |
    | standard_user |

  @regression
  Examples: Other valid users
    | username                |
    | visual_user             |
    | performance_glitch_user |
```

Notice that the password `secret_sauce` is a **constant** and therefore stays in the template, not in the table (see "Good practices" below). Each outline has a single outcome type, so each `Then` step is precise.

Rules for multiple blocks:

- Each block has its **own header row** and must supply **every placeholder** used in the template. Keeping the headers identical across blocks is the clearest style.
- The text after `Examples:` is a **name** (shown in some reports). Optional free text lines below the name are a description.
- **Tags on an `Examples` block** apply only to the rows of that block, which is powerful for selecting runs (for example `-Dcucumber.filter.tags="@smoke"` runs only `standard_user` above; see the *Tags* lesson).

### 7. Step-by-Step Walkthrough: Writing an Outline from Scratch

Follow these steps whenever you suspect an outline would help. We will turn sorting checks on saucedemo.com into an outline.

**Step 1: Write one concrete scenario first.**

```gherkin
Scenario: Sort products by name from A to Z
  Given the shopper is logged in
  When the shopper sorts the products by "Name (A to Z)"
  Then the first product is "Sauce Labs Backpack"
```

**Step 2: Write a second concrete scenario and compare.**

```gherkin
Scenario: Sort products by price from low to high
  Given the shopper is logged in
  When the shopper sorts the products by "Price (low to high)"
  Then the first product is "Sauce Labs Onesie"
```

**Step 3: Highlight what differs.** Only the sort option and the expected first product differ. Everything else is identical. Those two values become the placeholders.

**Step 4: Convert to an outline.** Change `Scenario:` to `Scenario Outline:`, replace the differing values with `<option>` and `<first>` (keep the quotes), and add the table:

```gherkin
Scenario Outline: Sorting by <option> puts <first> first
  Given the shopper is logged in
  When the shopper sorts the products by "<option>"
  Then the first product is "<first>"

  Examples:
    | option              | first                             |
    | Name (A to Z)       | Sauce Labs Backpack               |
    | Name (Z to A)       | Test.allTheThings() T-Shirt (Red) |
    | Price (low to high) | Sauce Labs Onesie                 |
    | Price (high to low) | Sauce Labs Fleece Jacket          |
```

**Step 5: Reuse or add step definitions.** The `Given` already exists. Add the other two:

```java
@When("the shopper sorts the products by {string}")
public void theShopperSortsTheProductsBy(String option) {
    inventoryPage.sortBy(option);          // wraps Selenium's Select class from Monday
}

@Then("the first product is {string}")
public void theFirstProductIs(String expectedName) {
    assertEquals(expectedName, inventoryPage.productNames().get(0));
}
```

Line by line: `inventoryPage` is a page object held in the step class (built from the driver in `TestContext`). `sortBy` internally uses `new Select(dropdown).selectByVisibleText(option)`, which is why the table values must match the visible dropdown text exactly. `productNames()` returns a `List<String>` of the product titles; `.get(0)` is the first one.

**Step 6: Run and read the result.** Four scenarios run. If the Z-to-A row fails, the title *Sorting by Name (Z to A) puts Test.allTheThings() T-Shirt (Red) first* tells you instantly which data failed.

### 8. Outline vs. Data Table: Do Not Confuse Them

| | **Scenario Outline + Examples** | **Data table attached to a step** |
|---|---|---|
| Purpose | Run the **entire scenario once per row** | Provide **structured data to one step** in a **single** run |
| Number of scenario executions | One per row | One |
| Placeholders (`<x>`) | Yes | No (unless the table is inside an outline) |
| Step definition receives | Ordinary parameters (`String`, `int`) | A `DataTable` object |
| Example | Test login with five different users | Add *these three* products to one cart |

Quick test: **"Should the whole scenario repeat for each row?"** If yes: outline. If the rows are all inputs to the same action: data table.

Side by side, the same three products used both ways:

```gherkin
# Data table: ONE scenario, ONE cart containing all three products
Scenario: Adding several products at once
  Given the shopper is logged in
  When the shopper adds these products:
    | product                 |
    | Sauce Labs Backpack     |
    | Sauce Labs Bike Light   |
    | Sauce Labs Bolt T-Shirt |
  Then the cart count shows 3

# Outline: THREE scenarios, each with ONE product
Scenario Outline: Adding <product> shows one item in the cart
  Given the shopper is logged in
  When the shopper adds "<product>" to the cart
  Then the cart count shows 1

  Examples:
    | product                 |
    | Sauce Labs Backpack     |
    | Sauce Labs Bike Light   |
    | Sauce Labs Bolt T-Shirt |
```

The tables look nearly identical; their meaning is completely different, and so is the cost (one browser versus three).

### 9. Worked Example: Cart Totals

Business rule: the cart shows the sum of the item prices. Instead of one scenario per combination, use an outline with the key examples. (Saucedemo prices: Backpack 29.99, Bike Light 9.99, Bolt T-Shirt 15.99, Onesie 7.99.)

```gherkin
Feature: Cart total
  As a shopper
  I want to see the total price of my cart
  so that I know what I will pay

  Scenario Outline: Cart total is the sum of the item prices
    Given the shopper is logged in
    When the shopper adds the products "<first>" and "<second>" to the cart
    Then the item total is <total>

    Examples:
      | first                   | second            | total |
      | Sauce Labs Backpack     | Sauce Labs Onesie | 37.98 |
      | Sauce Labs Bike Light   | Sauce Labs Onesie | 17.98 |
      | Sauce Labs Bolt T-Shirt | Sauce Labs Onesie | 23.98 |
```

Check the arithmetic yourself: 29.99 + 7.99 = 37.98; 9.99 + 7.99 = 17.98; 15.99 + 7.99 = 23.98. A table that documents a calculation must be right, so verify the numbers by hand before you trust the test.

Step definitions:

```java
@When("the shopper adds the products {string} and {string} to the cart")
public void theShopperAddsTwoProducts(String first, String second) {
    inventoryPage.addToCart(first);
    inventoryPage.addToCart(second);
}

@Then("the item total is {double}")
public void theItemTotalIs(double expectedTotal) {
    double actual = cartPage.openCheckoutOverview().getItemTotal();   // illustrative page-object call
    org.junit.jupiter.api.Assertions.assertEquals(expectedTotal, actual, 0.001);
}
```

`{double}` converts the text `37.98` into a Java `double`; `assertEquals(expected, actual, delta)` compares decimals with a tolerance, because floating-point numbers are not exact (for example, `0.1 + 0.2` is not exactly `0.3` in Java).

### 10. Troubleshooting with Console Messages

When something is wrong with an outline, Cucumber gives you clues. Learn to recognize them. (Exact wording varies a little between versions and plugins.)

**Case A: Placeholder name does not match the column header**

```gherkin
Scenario Outline: Login with <user> is rejected
  When the customer logs in with username "<user>" and password "<password>"
  ...
  Examples:
    | username      | password |
    | standard_user | wrong    |
```

The header says `username` but the template uses `<user>`. Cucumber does **not** reject this at parse time; `<user>` is simply left in the text, so the step no longer matches a sensible value. You will see output similar to:

```
Undefined scenarios:
file:///.../login-validation.feature:9 # Login with <user> is rejected

1 Scenarios (1 undefined)
```

Diagnosis: the title still contains `<user>` literally. Whenever you see angle brackets in a scenario title or step in the output, a placeholder was not replaced. Fix: make the names identical (they are case-sensitive).

**Case B: Missing quotes**

Template line: `When the customer logs in with username <username> and password "<password>"`. The text becomes `username standard_user and password "wrong"`, which the `{string}` expression cannot match, so the console reports an undefined step and prints a suggested snippet. Fix: add the quotes in the template.

**Case C: Different cell counts**

Gherkin reports a parse error for the file, saying a table row has an inconsistent cell count. Diagnosis: one row has more or fewer `|` separators than the header. Count the pipes on the failing line.

**Case D: `Examples` used with a plain `Scenario`**

A parse error that mentions an unexpected `Examples` token. Fix: change `Scenario:` to `Scenario Outline:`.

**Case E: One row fails, others pass**

```
Failures:
  Scenario: Login with a locked-out user is rejected   # login-validation.feature:21
    ...
    org.opentest4j.AssertionFailedError: expected: <Epic sadface: Sorry, this user has been locked out.> but was: <Epic sadface: Sorry, this user has been locked.>
```

Diagnosis: the title (thanks to the placeholder) points at the exact row, and the message shows the expected value from the table versus the actual page text. Decide whether the table value or the application is wrong.

### 11. Design Advice: Using Outlines Well

**Use an outline when:**

- The **same behavior** is checked with different **inputs and expected outputs** (validation rules, calculations, boundaries).
- The table is a **readable specification** of the rule. The table itself documents the rule.

**Avoid or limit it when:**

- Rows describe **different behaviors** (different outcomes need different Then steps).
- The table gets **huge** (dozens of rows). BDD uses *key examples*. Exhaustive data combinations belong in unit/API tests or data-driven tests that run faster than a browser.
- Every row launches a browser. UI scenarios are slow: 50 rows x 8 seconds is nearly 7 minutes. Choose the **representative** rows.
- The columns are **technical** (element ids, XPath). Examples should use business values.

**Good practices:**

1. **Name columns clearly** (`username`, not `u`).
2. Put **only the values that vary** in the table; keep constants (such as the shared password) in the template.
3. **Group rows** by purpose using named `Examples` blocks, but keep **one outcome type** per outline.
4. Include the **expected result as a column** so the table reads as input to output.
5. Use **meaningful values** that illustrate boundaries (for free shipping at $100: 99.99, 100.00, 100.01).
6. Keep the table **aligned** and well formatted.
7. Use placeholders in the **title** when it helps identify failures.

**Good-versus-bad rewrite 1: constants in the table**

Bad:

```gherkin
Examples:
  | username      | password     | page     |
  | standard_user | secret_sauce | products |
  | visual_user   | secret_sauce | products |
```

The `password` and `page` columns never change, so they add noise. Good:

```gherkin
When the customer logs in with username "<username>" and password "secret_sauce"
Then the customer sees the products page
Examples:
  | username      |
  | standard_user |
  | visual_user   |
```

**Good-versus-bad rewrite 2: technical columns**

Bad: a table with columns `locator` and `text` holding values like `#login-button`. A product owner cannot read it. Good: columns in business words (`username`, `message`).

**Good-versus-bad rewrite 3: one outline, mixed outcomes**

Bad: `Then the customer sees "<result>"` with rows that sometimes expect a page and sometimes an error. The Then step has to be a clever conditional method. Good: two outlines, as in Section 6.

### 12. Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Placeholder name does not match the column header (`<user>` vs `username`) | The step text still contains `<user>` and is undefined | Make them identical (case-sensitive) |
| Forgot quotes around `<placeholder>` for a `{string}` step | Undefined step | Write `"<placeholder>"` |
| Quotes around a placeholder for an `{int}` step | Undefined step | Remove the quotes |
| Using `Scenario:` with an `Examples` table | Parse error | Use `Scenario Outline:` |
| `Examples` table without a header row | First data row treated as header | Always include a header row |
| Rows with different cell counts | Parse error | Same number of cells per row |
| An outline with unrelated outcomes | Vague Then steps | Split into separate outlines |
| Huge tables of UI tests | Slow runs | Reduce to key examples |
| Relying on row order or state from a previous row | Intermittent failures | Each row must be independent |
| Wrong arithmetic in the expected column | A "failing" test that is really a wrong specification | Calculate by hand and compare with the application |

---

## Hands-On Lab: Login Validation Outline on saucedemo.com

Goal: replace the repetitive negative-login scenarios in your Project 2 repository with one outline, run it, and read the result.

**Prerequisites:** the Thursday setup (runner class, `TestContext`, `LoginPage`, login step definitions) and, ideally, the `Hooks` class from the *Hooks* lesson so the browser closes after every row. If you do not have hooks yet, the lab still works, but you must keep the temporary cleanup from Thursday until you add them.

1. Open `src/test/resources/features/login-validation.feature` (create it if missing).
2. Paste the feature from the "Complete Example" section below.
3. Make sure `src/test/resources/cucumber.properties` contains `cucumber.plugin=pretty` so every step prints to the console.
4. Check that your step definitions contain `the customer is on the login page`, `the customer logs in with username {string} and password {string}`, and `the error message {string} is displayed`. Add the new step `the customer remains on the login page`:

   ```java
   @Then("the customer remains on the login page")
   public void theCustomerRemainsOnTheLoginPage() {
       assertFalse(context.driver().getCurrentUrl().contains("inventory"));
   }
   ```

   Explanation: after a rejected login, saucedemo.com stays on the root URL; a successful login moves to `.../inventory.html`. Checking that the URL does **not** contain `inventory` proves the customer was not let in.
5. Run `mvn clean test`.
6. Expected output (shortened):

   ```
   Scenario Outline: Login with an empty username is rejected   # login-validation.feature:12
     Given the customer is on the login page
     When the customer logs in with username "" and password "secret_sauce"
     Then the error message "Epic sadface: Username is required" is displayed
     And the customer remains on the login page
   ...
   5 Scenarios (5 passed)
   20 Steps (20 passed)
   [INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
   ```

   Five rows, four steps each, twenty steps in total.
7. Break one row on purpose: change `locked out.` to `locked.` in the last message cell and rerun. Observe that **exactly one** scenario fails, that its title names the row, and that the other four stay green.
8. Fix the cell, then add a sixth row for `problem_user` with a **wrong password** and run again. Count the scenarios: it should now be 6.
9. Commit the change with a message such as `Convert negative login scenarios to a Scenario Outline`.

---

## Complete Example

`src/test/resources/features/login-validation.feature`

```gherkin
Feature: Login validation
  As the shop owner
  I want invalid login attempts to be rejected with a clear message
  so that customers know what to correct

  Scenario Outline: Login with <description> is rejected
    Given the customer is on the login page
    When the customer logs in with username "<username>" and password "<password>"
    Then the error message "<message>" is displayed
    And the customer remains on the login page

    Examples: Missing credentials
      | description        | username      | password     | message                            |
      | an empty username  |               | secret_sauce | Epic sadface: Username is required |
      | an empty password  | standard_user |              | Epic sadface: Password is required |

    Examples: Incorrect credentials
      | description        | username        | password       | message                                                                   |
      | a wrong password   | standard_user   | wrong_password | Epic sadface: Username and password do not match any user in this service |
      | an unknown user    | nobody          | secret_sauce   | Epic sadface: Username and password do not match any user in this service |
      | a locked-out user  | locked_out_user | secret_sauce   | Epic sadface: Sorry, this user has been locked out.                       |
```

This one outline replaces five scenarios, yields five clearly titled results (for example "Login with an empty username is rejected"), and documents the validation rules in two tidy tables. All five rows share **one outcome type** (rejected with an error message and no access). The existing step definitions from Thursday are reused unchanged, plus one step, `the customer remains on the login page`, that asserts the URL still contains no `inventory`.

---

## Practice Exercises

1. **Convert.** Convert Thursday's three negative login scenarios into one `Scenario Outline` with an `Examples` table.
2. **Title placeholders.** Add a `description` column and use it in the outline title. Run it and check the output names.
3. **Boundary table.** Rule: "Orders of $100.00 or more get free shipping; otherwise shipping is 5.99." Write an outline with the examples 99.99, 100.00, and 100.01 and a column for the expected shipping cost.
4. **Two blocks.** Split the login outline into `Examples: Missing credentials` and `Examples: Incorrect credentials`, as in the complete example. Observe how the output groups the runs.
5. **Spot the difference.** Which of these needs an outline and which a data table? (a) Check that five different usernames are all locked out. (b) Add three listed products to one cart. (c) Check sort orders for four different sort options.
6. **Debug.** Find and fix all errors:

   ```gherkin
   Scenario: Sorting
     When the shopper sorts by "<option>"
     Then the first product is <first>
     Examples:
       | Option             | first               |
       | Name (A to Z)      | Sauce Labs Backpack |
       | Name (Z to A)      | Test.allTheThings() T-Shirt (Red) |
   ```
7. **Reduce.** A teammate wrote an outline with 40 rows of price calculations that each launch a browser. Propose how you would reduce it and what else you would use for the full set.
8. **Split mixed outcomes.** The following outline mixes outcomes. Rewrite it as two outlines:

   ```gherkin
   Scenario Outline: Login attempts
     Given the customer is on the login page
     When the customer logs in with username "<username>" and password "<password>"
     Then the customer sees "<result>"
     Examples:
       | username        | password     | result            |
       | standard_user   | secret_sauce | the products page |
       | locked_out_user | secret_sauce | a lock-out error  |
   ```
9. **Cart totals.** Add a row to the cart-total outline using `Sauce Labs Fleece Jacket` and `Sauce Labs Bike Light`. Calculate the total by hand first, then run.
10. **Placeholder in a doc string.** Write an outline for a feedback form where the doc string message is `<comment>` and three different comments are tried. Which Java type receives a doc string?
11. **Tag a block.** Tag one `Examples` block `@smoke` and another `@regression`, then run with `-Dcucumber.filter.tags="@smoke"` and count the rows executed (use the *Tags* lesson).
12. **Project 2.** Convert at least one group of repetitive scenarios in your Project 2 features into an outline, run it with your runner, and include the outline's console output in your milestone notes.

---

## Solutions and Hints

**1.** Use the first code block in Section 1. Hint: the `username`/`password` pairs and the message are the three varying values.

**2.** Title: `Scenario Outline: Login with <description> is rejected`. In the output you should see distinct titles such as "Login with a wrong password is rejected".

**3.**

```gherkin
Scenario Outline: Shipping cost depends on the order value
  Given the shopper has products worth <subtotal> in the cart
  When the shopper views the shipping cost
  Then the shipping cost is <shipping>

  Examples:
    | subtotal | shipping |
    | 99.99    | 5.99     |
    | 100.00   | 0.00     |
    | 100.01   | 0.00     |
```

The values sit on both sides of the boundary (99.99 below, 100.00 exactly on it, 100.01 above).

**4.** The run itself is the same as with one block; blocks mainly help reading and tagging. Depending on the reporter, the block name may appear next to the rows.

**5.** (a) Outline: the whole scenario repeats per user. (b) Data table: one cart, three products. (c) Outline: each sort option is a separate run of the same scenario.

**6.** Errors: (1) `Scenario:` must be `Scenario Outline:`; (2) there is no `Given` step to set the starting state, so add `Given the shopper is logged in`; (3) `<first>` in the Then step needs quotes for `{string}`: `"<first>"`; (4) the header `Option` does not match `<option>` (case-sensitive), so change it to `option`. Corrected version:

```gherkin
Scenario Outline: Sorting
  Given the shopper is logged in
  When the shopper sorts by "<option>"
  Then the first product is "<first>"
  Examples:
    | option        | first                             |
    | Name (A to Z) | Sauce Labs Backpack               |
    | Name (Z to A) | Test.allTheThings() T-Shirt (Red) |
```

**7.** Keep a handful of key rows per rule (typical, each boundary, one failure case). Move the full 40-row calculation to a fast **unit test** of the pricing code (JUnit with `@ParameterizedTest`) or to an API check, which run in milliseconds instead of launching browsers. Keep the BDD table as a readable specification of the rule.

**8.** Two outlines:

```gherkin
Scenario Outline: <username> can log in and sees the products
  Given the customer is on the login page
  When the customer logs in with username "<username>" and password "secret_sauce"
  Then the customer sees the products page
  Examples:
    | username      |
    | standard_user |

Scenario Outline: <username> is locked out
  Given the customer is on the login page
  When the customer logs in with username "<username>" and password "secret_sauce"
  Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed
  Examples:
    | username        |
    | locked_out_user |
```

(An outline with a single row is legal; in a real suite you would usually write a plain `Scenario` for a single case, or add more users to the table.)

**9.** 49.99 + 9.99 = 59.98. Row: `| Sauce Labs Fleece Jacket | Sauce Labs Bike Light | 59.98 |`.

**10.** A doc string arrives in the step-definition method as a `String` parameter, the last one. Example: `public void submitReview(String product, String comment)`, where `product` comes from `{string}` and `comment` is the doc string.

**11.** Only rows in the `@smoke`-tagged block execute. If your smoke block has one row, the summary shows `1 Scenarios`.

**12.** Hint: look for scenarios whose steps differ only in quoted values. Those are the best candidates.

---

## Self-Check Questions

**Q1. What does Cucumber do with the header row of an `Examples` table?**
It uses it to name the placeholders. The header row is never executed as data.

**Q2. An `Examples` table has a header and 4 data rows. How many scenarios run?**
Four.

**Q3. Why must quotes be written around `<username>` in the template?**
Cucumber substitutes only the value; it does not add quotes. `{string}` requires the quoted text to be present in the step after substitution.

**Q4. You see `<user>` literally in the console output of a scenario title. What is wrong?**
The placeholder name does not match any column header (check spelling and case).

**Q5. When do you choose a data table instead of an outline?**
When the rows are inputs to a single action in one run (for example, a list of products added to one cart), not separate runs of the scenario.

**Q6. Do rows of an outline share a browser?**
No. Each row is a separate scenario with its own `TestContext` and, via hooks, its own browser.

**Q7. Why keep one outcome type per outline?**
So the `Then` step can be precise and readable. Mixed outcomes force vague steps and conditional code.

**Q8. Why do you keep outline tables small for UI tests?**
Every row launches a full browser scenario, so large tables make the suite slow; exhaustive data belongs in faster unit or API tests.

---

## Summary

- A **Scenario Outline** is a **template** with `<placeholders>`; the **`Examples`** table supplies values, and Cucumber runs the scenario **once per row**.
- Placeholders are replaced **before step matching**, so ordinary step definitions with `{string}`, `{int}`, and so on work; put **quotes in the template** for `{string}`.
- Hooks and the Background run **for every row**; rows are fully independent.
- Placeholders may appear in **steps, titles, data tables, and doc strings**; use title placeholders to make reports readable.
- **Multiple named and tagged `Examples` blocks** group data by purpose and allow selective runs, but each outline should have **one outcome type**.
- An **outline repeats the entire scenario per row**; a **data table** gives structured data to **one step**.
- Use outlines for **the same behavior with different data**; keep tables to **key examples**, avoid huge UI-driven tables, and never mix different behaviors in one outline.
- Angle brackets left in the output mean a placeholder name does not match its column header.

---

## Additional Resources

- Cucumber documentation, *Gherkin reference: Scenario Outline*: https://cucumber.io/docs/gherkin/reference/#scenario-outline
- Cucumber documentation, *Gherkin reference: Examples*: https://cucumber.io/docs/gherkin/reference/#examples
- Cucumber documentation, *Better Gherkin*: https://cucumber.io/docs/bdd/better-gherkin/
