# Gherkin

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **Gherkin** is, how it is related to Cucumber, and where `.feature` files live in a Maven project.
- Describe the structure of a feature file and the purpose of each keyword: `Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`, and `*`.
- Write **comments**, **descriptions**, and use correct **indentation** and file conventions.
- Use **data tables** and **doc strings** to pass structured and multi-line data to steps.
- Explain how Gherkin is parsed: line-based, keyword-driven, free text after the keyword.
- Predict the result Cucumber reports for a step: passed, failed, skipped, undefined, pending, or ambiguous.
- Write Gherkin in other languages using the `# language:` header.
- Follow Gherkin **style rules** (declarative wording, one behavior per scenario), turn a user story into a feature file, and spot and fix common syntax errors.

---

## Why This Matters

**Gherkin** is the language of BDD. It is what the three amigos write together and what Cucumber executes. If the Gherkin is clear, the whole BDD chain works: the business can validate it, developers can implement it, and the tests remain readable for years. If it is messy, you will get a suite nobody wants to read or maintain.

Think about learning a new spoken language. Before you can write a poem you must learn the alphabet, a few hundred words, and the basic grammar. Gherkin is a *tiny* language: about ten keywords and a few punctuation rules. That is good news, because you can learn the whole grammar in one lesson. The hard part, writing sentences that express behavior clearly, comes with practice, and the following lessons provide it.

This lesson covers the **grammar** of Gherkin: the keywords and the syntax. The following lessons look at how to structure features and scenarios (*Features and Scenarios*), how to apply the Given/When/Then pattern well (*Given/When/Then*), and how to link the text to code (*Step Definitions*). Advanced keywords such as `Scenario Outline`, `Background`, `Rule`, and tags are saved for **Friday's** lessons; today we learn the core language.

**Where you will use this:**

- **Today** in the Project 2 pair activity, when you turn the stories you wrote into `.feature` files for saucedemo.com.
- **Every day on a BDD project**: reading a colleague's feature file, reviewing it, fixing a parse error, or updating wording when a business rule changes.
- **In interviews**: "Explain the difference between `Given`, `When`, and `Then`" and "How does Cucumber match a step?" are very common questions.

---

## The Concept

### 1. What Is Gherkin?

**Gherkin** is a **line-oriented, plain-text language** with a small set of keywords used to describe software behavior without detailing how it is implemented. It was designed by the Cucumber project and is now used by many BDD tools.

Key characteristics:

- Files have the extension **`.feature`** and are stored with the project (typically `src/test/resources/features/`).
- Gherkin is **structured** (a parser reads it), but the text you write after keywords is **free-form natural language**.
- Gherkin documents have **two jobs**: they are *documentation* readable by non-programmers *and* *automated tests* that Cucumber runs.
- The name "Gherkin" is a pun on "Cucumber": a gherkin is a small pickled cucumber.

**Analogy: a form with fixed headings.** A hospital admission form has fixed headings (Name, Symptoms, Allergies) but free text beside each. Anyone can read the form and a clerk (or a computer) can find each section quickly because the headings are always in the same place. Gherkin works the same way: fixed keywords tell the parser *what role a line plays*, while the free text tells humans *what is meant*.

A first complete example:

```gherkin
Feature: Shopping cart
  As a shopper
  I want to add products to my cart
  so that I can buy several items in one order

  Scenario: Add one product to an empty cart
    Given the shopper is logged in
    And the shopping cart is empty
    When the shopper adds "Sauce Labs Backpack" to the cart
    Then the cart contains 1 item
    And the cart contains "Sauce Labs Backpack"
```

**Line-by-line explanation:**

| Line | What it is | Explanation |
|---|---|---|
| `Feature: Shopping cart` | Feature title | The keyword `Feature:` followed by the name of the capability. Exactly one per file. |
| `As a shopper` / `I want to add products to my cart` / `so that I can buy several items in one order` | Description | Free text. Not executed. Holds the user story so people know *why* the file exists. |
| (blank line) | Separator | Ignored. Used for readability. |
| `Scenario: Add one product to an empty cart` | Scenario title | One concrete example of behavior. The title states what is being demonstrated. |
| `Given the shopper is logged in` | Step (context) | Sets up the starting state. |
| `And the shopping cart is empty` | Step (context) | `And` continues the previous keyword, so this is a second `Given`. |
| `When the shopper adds "Sauce Labs Backpack" to the cart` | Step (action) | The one thing the user does. The quoted text is data. |
| `Then the cart contains 1 item` | Step (outcome) | An observable result. The number `1` is data. |
| `And the cart contains "Sauce Labs Backpack"` | Step (outcome) | A second outcome; `And` continues `Then`. |

### 2. The Parts of a Feature File

```
+-- Feature: title                     <- exactly one per file
|     free-text description            <- optional (the story goes here)
|
|   +-- Scenario: title                <- one or more per feature
|   |     Given ...                    <- steps
|   |     When ...
|   |     Then ...
|   +--
|
|   +-- Scenario: another title
|   |     ...
+-- +--
```

- A feature file contains **one `Feature`**.
- A feature contains **one or more scenarios**.
- A scenario contains **steps**.

**Where the file lives.** In a standard Maven project (the structure you will create in the *Cucumber Framework Setup* lesson) the files go under the test resources folder, because they are test inputs, not Java code:

```
project-root/
  pom.xml
  src/
    test/
      java/
        ...                  <- step definitions, page objects, runner (Java)
      resources/
        features/
          login.feature      <- Gherkin files
          cart.feature
          checkout.feature
```

Cucumber-JVM scans for feature files on the classpath or in a path you configure. Putting them under `src/test/resources/features` is the convention the course (and most teams) follows.

### 3. Keywords

Gherkin has a handful of primary keywords. Each is followed by a colon (for structural keywords) or a space (for step keywords).

#### Structural keywords

| Keyword | Purpose |
|---|---|
| `Feature:` | Names the feature and starts the file. The text on the same line is the feature's title. Following free text is the description. |
| `Scenario:` (or `Example:`) | A concrete example of behavior; a single test case. `Scenario` and `Example` are synonyms. |

(Additional structural keywords, `Background`, `Scenario Outline`/`Scenario Template` with `Examples`, and `Rule`, exist and are covered on Friday.)

#### Step keywords

| Keyword | Role | Typical meaning |
|---|---|---|
| `Given` | **Context / precondition** | The state of the world before the behavior |
| `When` | **Action / event** | What the user or system does |
| `Then` | **Outcome / assertion** | What should be observable afterward |
| `And` | Continues the previous step type | Another Given, When, or Then |
| `But` | Same as `And`, reads naturally for negatives | "But the cart is not empty" |
| `*` | A bullet-like step | Neutral alternative to And/But (rarely used) |

A key point: **Cucumber treats all step keywords identically when matching to code.** `Given the user is logged in` and `When the user is logged in` would match the same step definition. The keywords exist for the *human reader* and to enforce a readable structure. The *Given/When/Then* lesson explores how to use them properly.

**A memory aid for the three main keywords** using a vending machine:

| Keyword | Vending machine | Online shop |
|---|---|---|
| Given | The machine is stocked and powered on | The shopper is logged in and the cart is empty |
| When | You insert a coin and press B4 | The shopper adds the backpack to the cart |
| Then | A bag of crisps drops into the tray | The cart contains one item |

Context, action, outcome. Every scenario tells that little story.

**Why `And` and `But` exist.** Without them you would have to repeat `Given Given Given`, which reads badly. `And` simply means "the same kind of step as the one above". `But` means the same, but signals a contrast ("Then the order is saved. But no email is sent."). Cucumber does not distinguish them in any way.

**The `*` bullet.** It can replace any step keyword:

```gherkin
Scenario: Items in the cart
  Given the shopper has these items in the cart
  * the Sauce Labs Backpack
  * the Sauce Labs Bike Light
```

It is rarely used; this course will not use it. You need to recognize it only when you read someone else's files.

### 4. Scenario Anatomy

A scenario is built from a **title** and **steps**. Here is the earlier example with each line explained. Note that comments are written on their own lines, never at the end of a step line (the reason is explained in Section 6):

```gherkin
  # Title: describes the behavior in business terms
  Scenario: Locked-out user cannot log in
    # Context
    Given the user "locked_out_user" exists
    # More context (And continues Given)
    And the user is on the login page
    # One action
    When the user logs in with a valid password
    # Outcome
    Then an error message is displayed
    # A negative outcome (But continues Then)
    But the user is not logged in
```

- **Title:** A short sentence that states the behavior in business language.
- **Steps:** One line each, beginning with a step keyword.
- **Order:** Typically Given, then When, then Then, but you can have multiple of each (see the *Given/When/Then* lesson for when that is wise).

**What happens when this scenario runs.** Cucumber starts a fresh test, executes the five steps top to bottom, and stops at the first failure (marking the rest as skipped). If all five pass, the scenario passes.

### 5. Indentation, Whitespace, and Line Rules

- **Indentation is not significant** to the Gherkin parser (unlike Python), but it is a strong convention for readability: indent scenarios two spaces under the feature, and steps two more under the scenario.
- **One step per line.** Steps cannot span multiple lines (use doc strings for multi-line text).
- **Blank lines** are ignored; use them to separate scenarios.
- Use **spaces** (not tabs) consistently.
- File encoding: **UTF-8**.
- The file name should describe the feature in lowercase with hyphens or underscores: `login.feature`, `shopping-cart.feature`.

**Good formatting versus poor formatting** of the same content:

```gherkin
Feature: Login
Scenario: Valid login
Given the customer is on the login page
When the customer logs in with valid credentials
Then the customer sees the products page
Scenario: Locked-out login
Given the customer is on the login page
When the customer logs in as a locked-out user
Then the customer sees a lock message
```

This is valid Gherkin, and Cucumber would run it, but humans struggle to see where one scenario ends. Compare with proper formatting:

```gherkin
Feature: Login

  Scenario: Valid login
    Given the customer is on the login page
    When the customer logs in with valid credentials
    Then the customer sees the products page

  Scenario: Locked-out login
    Given the customer is on the login page
    When the customer logs in as a locked-out user
    Then the customer sees a lock message
```

Many IDEs (IntelliJ with the Cucumber plugin, VS Code with the Cucumber extension) auto-format and highlight Gherkin; use them.

### 6. Comments and Descriptions

**Comments** begin with `#` at the start of a line (after optional whitespace) and are ignored by Cucumber:

```gherkin
# Smoke test for the SauceDemo login: owner: QA team
Feature: Login
  ...
  Scenario: Valid login
    # The password is the shared demo password
    Given ...
```

> **Important:** a comment must be on **its own line**. Gherkin does **not** support comments at the end of a step line. If you write `Given the user is logged in  # context`, the text `# context` becomes part of the step text, and your step definition will fail to match (you would see an *undefined* step). Always put comments on their own line above the step.

Comments are for **authors**, not for describing requirements. If something is important for the business, put it in the **description** or in the scenario.

**Descriptions** are free-form text under `Feature:` or `Scenario:` lines. They can contain any text (except lines that begin with a Gherkin keyword):

```gherkin
Feature: Product sorting
  Shoppers need to find items quickly.
  The default order is by name, A to Z.

  Scenario: Sort by price
    This scenario checks the ascending price order only.
    Given ...
```

A common use: put the **user story** ("As a... I want... so that...") in the feature description, so that the file documents *why* it exists. This is the bridge from the *User Stories and Acceptance Criteria* lesson: the story goes into the description, each acceptance criterion becomes one scenario.

**Comment or description?**

| Use a comment (`#`) when... | Use a description when... |
|---|---|
| The note is for people editing the file (owner, TODO, link to a ticket) | The note explains the business context for every reader |
| You want Cucumber to ignore it completely | You want the text to show in reports and documentation |
| It is short | It may take several lines |

### 7. Data Tables

Sometimes a step needs **structured data**, such as several rows of related values. Use a **data table**: lines starting with `|` immediately after a step.

```gherkin
Scenario: Add several products to the cart
  Given the shopper is on the products page
  When the shopper adds the following products to the cart:
    | product                | quantity |
    | Sauce Labs Backpack    | 1        |
    | Sauce Labs Bike Light  | 2        |
  Then the cart summary shows:
    | product                | quantity |
    | Sauce Labs Backpack    | 1        |
    | Sauce Labs Bike Light  | 2        |
```

Rules:

- Columns are separated by `|`; whitespace around cell values is trimmed, so you can **align the columns** for readability.
- The **first row is typically the header**, but it is up to the step definition whether it treats it as one.
- The table belongs to the **step directly above it** and is passed to that step's Java method as a `DataTable` object (covered in *Step Definitions*).
- A literal pipe inside a cell is written `\|`; a newline is `\n`; a backslash is `\\`.

> **Do not confuse** data tables with `Scenario Outline` `Examples` tables, which run the *whole scenario once per row*. A data table is simply **data for one step** in a single run. (Outlines are covered on Friday.)

**Line-by-line:**

- `When the shopper adds the following products to the cart:` is a normal step; the trailing colon is only a convention that signals "a table follows". It is part of the step text.
- The first `|` row (`product`, `quantity`) names the columns.
- Each following row is one record: one product and how many.
- `Then the cart summary shows:` begins a second step with its own table, which will be compared with the real cart.

**A preview of how Java receives the table.** You will study this in the *Step Definitions* lesson; here is only the idea, so that tables do not feel magical:

```java
@When("the shopper adds the following products to the cart:")
public void theShopperAddsTheFollowingProductsToTheCart(io.cucumber.datatable.DataTable table) {
    java.util.List<java.util.Map<String, String>> rows = table.asMaps();
    for (java.util.Map<String, String> row : rows) {
        String product = row.get("product");
        int quantity = Integer.parseInt(row.get("quantity"));
        // call the page object here
    }
}
```

`table.asMaps()` turns every row after the header into a map from column name to cell value. The first row `product | quantity` supplies the keys.

**When to use a data table.** Use one when a single step carries several values of the same shape (a list of items, a form with many fields). Do not use one to hide a long script of separate actions; those should be separate steps.

### 8. Doc Strings

For **multi-line text** (an email body, a JSON message, a paragraph), use a **doc string**, delimited by three double quotes (`"""`) or three backticks:

```gherkin
Scenario: Show the welcome email text
  Given a new customer registers with the email "ada@example.com"
  Then the customer receives an email with the following content:
    """
    Welcome to the Swag Labs shop!

    Your account has been created.
    Please log in at https://www.saucedemo.com
    """
```

- Everything between the delimiters is passed as **one `String`** to the step definition (indentation relative to the opening delimiter is preserved).
- A **content type** can follow the opening delimiter for documentation, e.g. `"""json`.

**Line-by-line:**

- The step line introduces the text with a trailing colon (a convention).
- The opening `"""` starts the doc string; it must be on its own line.
- The lines in between are the text. The blank line inside is preserved as a blank line in the string.
- The closing `"""` ends it. If you forget it, the parser treats the rest of the file as part of the string and reports an error.

**Data table or doc string?**

| Data | Choose |
|---|---|
| A grid of values (rows and columns) | Data table |
| One block of free text or JSON | Doc string |
| One or two single values | Neither: put them in quotes inside the step text |

### 9. Step Text, Quotes, and Parameters

The text of a step after its keyword is free, but conventions help the step-definition layer (and readers):

- Put **variable values in double quotes**: `When the shopper searches for "backpack"`.
- Put **numbers** unquoted: `Then the cart contains 3 items`.
- Keep wording consistent across scenarios, so one step definition can serve many scenarios. `the user is on the login page` in ten files should always read **exactly** the same.

Cucumber matches the **text** against patterns in the step definitions; those patterns can extract the quoted/numeric parts as parameters. The matching mechanism is explained in the *Step Definitions* lesson.

**A quick preview of the matching (Cucumber Expressions).** In Cucumber 7 for Java the pattern of a step uses **Cucumber Expressions**. The three you will see most:

| In the pattern | Matches in the feature text | Java parameter type |
|---|---|---|
| `{string}` | A value in double (or single) quotes, such as `"backpack"` | `String` (quotes removed) |
| `{int}` | A whole number such as `3` or `-1` | `int` |
| `{double}` | A decimal number such as `29.99` | `double` |

So the feature line `When the shopper searches for "backpack"` can be matched by the pattern `the shopper searches for {string}`, and `Then the cart contains 3 items` by `the cart contains {int} items`. Note that `1 item` (singular) would **not** match `{int} items`; it is a typical beginner surprise. Keeping wording consistent is therefore not just good style; it decides whether the match succeeds.

### 10. Tags (A Short Preview)

Lines starting with `@` placed above `Feature` or `Scenario` are **tags** used to group and filter scenarios:

```gherkin
@smoke
Scenario: Valid login
```

We mention tags only so that you recognize them when you see them in the sample code. **Using tags (running subsets, hooks per tag) is a Friday topic.**

### 11. Gherkin in Other Languages

Gherkin supports many natural languages. Add a language header on the first line:

```gherkin
# language: es
Característica: Inicio de sesión
  Escenario: Inicio de sesión válido
    Dado que el usuario está en la página de inicio
    Cuando introduce credenciales válidas
    Entonces ve la lista de productos
```

The keywords are translated; step definitions can use the same language. For this course we use English.

**Why this matters.** In multinational teams, the business may prefer to write scenarios in its own language. The `# language:` header (a special comment on the first line) tells the parser which keyword dictionary to use. The Cucumber documentation lists the supported languages.

### 12. How Cucumber Reads a Feature File

1. The **Gherkin parser** reads the file line by line, recognizing keywords at the start of lines.
2. It builds a structure: feature, scenarios, steps (with tables/doc strings attached).
3. For every scenario Cucumber **creates a fresh test run**, executes each step in order by finding the matching step definition, and records the result.
4. Step results:
   - **Passed:** the step's code ran without exception.
   - **Failed:** an exception/assertion error occurred; the rest of the scenario's steps are **skipped**.
   - **Skipped:** not executed because an earlier step failed.
   - **Undefined:** no step definition matches the text; Cucumber prints a **snippet** showing the code to write.
   - **Pending:** a step definition exists but is marked as not yet implemented.
   - **Ambiguous:** more than one step definition matches the text (an error you must fix).

Seeing "undefined" and "ambiguous" is normal while learning; they are Cucumber's way of guiding you.

**A worked example of the outcomes.** Suppose the scenario below runs and the code for the first two steps exists, the third step's code throws an assertion error, the fourth is fine, and the fifth has no code:

```gherkin
Scenario: Checkout shows the correct total
  Given the shopper has the "Sauce Labs Backpack" in the cart
  When the shopper starts checkout
  Then the item total is 29.99
  And the tax is 2.40
  And the order can be confirmed
```

| Step | Status | Why |
|---|---|---|
| `Given the shopper has ...` | Passed | Code ran without error |
| `When the shopper starts checkout` | Passed | Code ran without error |
| `Then the item total is 29.99` | **Failed** | An assertion failed (for example, the page showed 31.99) |
| `And the tax is 2.40` | Skipped | An earlier step failed, so it is not executed |
| `And the order can be confirmed` | Skipped (or Undefined) | Not executed because of the earlier failure. Cucumber may still flag it as undefined, because it knows no definition exists; fix the failure and the undefined step in turn |

The scenario as a whole is marked **failed**. Look at the **first** failing step; everything after it is a consequence.

**Why "undefined" is a gift.** When you write feature files *before* step definitions (which is the BDD order), every step is undefined at first. Cucumber prints Java snippets, for example:

```text
Undefined scenarios:
file:///project/src/test/resources/features/login.feature:3 # Successful login

1 Scenarios (1 undefined)
3 Steps (3 undefined)

You can implement missing steps with the snippets below:

@Given("the customer is on the login page")
public void the_customer_is_on_the_login_page() {
    // Write code here that turns the phrase above into concrete actions
    throw new io.cucumber.java.PendingException();
}

@When("the customer logs in with username {string} and password {string}")
public void the_customer_logs_in_with_username_and_password(String string, String string2) {
    // Write code here that turns the phrase above into concrete actions
    throw new io.cucumber.java.PendingException();
}
```

Notice how Cucumber has already noticed the quoted values and turned them into `{string}` parameters. You can copy these into a class and replace the `PendingException` line with real code. This is exactly what the *Step Definitions* lesson does.

### 13. Style Rules for Good Gherkin

1. **Write in the business language**, not UI mechanics ("logs in", not "clicks the button with id").
2. **One scenario = one behavior.** If a scenario has two Whens, it probably contains two behaviors.
3. **Keep scenarios short**, usually 3-7 steps.
4. **Use present tense** and consistent voice (third person: "the shopper adds...").
5. **Title scenarios by the behavior or rule**, e.g. "Locked-out user sees an error", not "Test 3".
6. **Avoid implementation details**: no URLs, element ids, or SQL in steps (a *base URL* or demo password belongs in configuration).
7. **Reuse step wording** exactly to keep the step-definition set small.
8. **Do not chain scenarios**: every scenario must be able to run alone and in any order.
9. **Prefer meaningful example data** ("Ada", "locked_out_user") over meaningless ("abc", "test1").
10. **Keep descriptions short**: the story, perhaps one or two business notes.

**Good versus bad, with reasons:**

| Bad | Why it is bad | Good |
|---|---|---|
| `Given I open Chrome and go to https://www.saucedemo.com` | Browser and URL are implementation and configuration details | `Given the customer is on the login page` |
| `When I type "standard_user" in id "user-name"` | Locator in the feature; breaks on UI change | `When the customer logs in as "standard_user"` |
| `Then it works` | Not checkable | `Then the customer sees the products page` |
| `Scenario: Test 1` | Title says nothing | `Scenario: Locked-out customer cannot log in` |
| `Given I log in` then `When I log in again` | Repeats the action in context and action | `Given the customer is logged in` then `When the customer logs out` |
| `Scenario` that depends on the cart state left by the previous scenario | Scenarios become order dependent; one failure cascades | Each scenario sets up its own state in its `Given` |

**A style test: the "read aloud" rule.** Read the scenario aloud to a non-technical colleague. If you have to say "id", "xpath", "click the third button", or "wait three seconds", rewrite the step.

### 14. Common Syntax Errors

| Error | Example | Fix |
|---|---|---|
| Missing colon after structural keyword | `Scenario Valid login` | `Scenario: Valid login` |
| Two `Feature:` lines in one file | | One feature per file |
| Step text before any scenario | `Given ...` directly under `Feature:` | Put it under a `Scenario:` |
| Misaligned table with a different number of cells per row | `\| a \| b \|` then `\| c \|` | Every row must have the same number of cells |
| Unclosed doc string | missing closing `"""` | Add the closing delimiter |
| Description line starting with a keyword | `Given you are a shopper` in a description | Rephrase so the line does not begin with a keyword |
| Tabs and spaces mixed | | Use spaces only |
| Special quotes copied from a word processor (`“ ”`) | Step matching fails because the quotes differ | Use plain `"` |
| Comment at the end of a step line | `Given the user is logged in # context` | Move the comment to its own line |
| Wrong keyword capitalization or spelling | `given the user...` or `Scenerio:` | Keywords are case-sensitive: `Given`, `Scenario:` |

**Reading a parse error.** When the parser fails, the message gives the file name, a line number, and a description. Example:

```text
Error: (CompositeParserException) Parser errors:
(2:1): expected: #EOF, #Language, #TagLine, #FeatureHeader, #Comment, #Empty, got 'Scenario Pay by card'
```

How to read it: `(2:1)` means line 2, column 1. The parser was expecting one of the listed things (a feature header, a tag, a comment, and so on) but found `Scenario Pay by card`, which is not a valid line there (the colon is missing and, in the earlier example, the feature line itself has no colon). Go to that line and compare it with the grammar. The *first* error is the one to fix; later errors are often just consequences.

---

## Complete Example: Login Feature File

File: `src/test/resources/features/login.feature`

```gherkin
# Smoke and negative tests for the login page of the Swag Labs demo shop
Feature: Login
  As a registered customer
  I want to log in with my credentials
  so that I can see the products and place orders

  Scenario: Successful login with valid credentials
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "secret_sauce"
    Then the customer sees the products page

  Scenario: Login is rejected for a wrong password
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "wrong_password"
    Then the error message "Epic sadface: Username and password do not match any user in this service" is displayed
    And the customer remains on the login page

  Scenario: Locked-out customer cannot log in
    Given the customer is on the login page
    When the customer logs in with username "locked_out_user" and password "secret_sauce"
    Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed
    But the customer does not see the products page

  Scenario: Username is required
    Given the customer is on the login page
    When the customer logs in with an empty username and password "secret_sauce"
    Then the error message "Epic sadface: Username is required" is displayed
```

**Reading guide:**

- Line 1 is a comment. The `Feature:` title is "Login"; the next three lines are the story description.
- There are four scenarios, each testing a different behavior (a rule from the acceptance criteria).
- Quoted values are variable data; the wording of repeated steps (`Given the customer is on the login page`) is identical, so one step definition will serve all four scenarios.
- No scenario mentions a locator or a URL.

**Line-by-line for the second scenario:**

| Line | Explanation |
|---|---|
| `Scenario: Login is rejected for a wrong password` | States the rule being shown: a wrong password leads to refusal |
| `Given the customer is on the login page` | Context. The step definition will open the site and create the `LoginPage` page object |
| `When the customer logs in with username "standard_user" and password "wrong_password"` | The action. The two quoted values will be passed to the Java method as two `String` parameters |
| `Then the error message "..." is displayed` | Outcome. The exact text is the acceptance criterion; the method will compare it to the text of the error element |
| `And the customer remains on the login page` | A second outcome in the same behavior: still no login |

**How this file maps to the Project 2 stack.** The words in these lines will be matched to Java methods that call the `LoginPage` page object from Wednesday (typing into the fields and clicking the button with the locators you already wrote). The feature file itself never changes when locators change.

In the *Step Definitions* lesson you will write the Java code that gives these lines their behavior.

---

## From User Story to Feature File: A Worked Transformation

Let us transform a story and its acceptance criteria into a feature file, following the steps you would use in the Project 2 pair activity.

**Story:** As a shopper, I want to remove an item from my cart, so that I only buy what I want.

**Acceptance criteria:**

1. Removing an item deletes it from the cart list.
2. The cart badge shows the number of items still in the cart.
3. When the last item is removed, the cart is empty and the badge disappears.

**Step 1: Create the file** `src/test/resources/features/remove-from-cart.feature`.

**Step 2: Write the title and the story as the description.**

```gherkin
Feature: Remove items from the cart
  As a shopper
  I want to remove an item from my cart
  so that I only buy what I want
```

**Step 3: One scenario per criterion.** For criterion 1:

```gherkin
  Scenario: Removing an item deletes it from the cart
    Given the shopper has the "Sauce Labs Backpack" and the "Sauce Labs Bike Light" in the cart
    When the shopper removes the "Sauce Labs Backpack" from the cart
    Then the cart contains only the "Sauce Labs Bike Light"
```

For criterion 2:

```gherkin
  Scenario: The cart badge shows the remaining items
    Given the shopper has the "Sauce Labs Backpack" and the "Sauce Labs Bike Light" in the cart
    When the shopper removes the "Sauce Labs Backpack" from the cart
    Then the cart badge shows 1
```

For criterion 3:

```gherkin
  Scenario: Removing the last item empties the cart
    Given the shopper has the "Sauce Labs Backpack" in the cart
    When the shopper removes the "Sauce Labs Backpack" from the cart
    Then the cart is empty
    And the cart badge is not shown
```

**Step 4: Review against the style rules.**

- Each scenario has one `When`: good.
- Quoted values are data; numbers are unquoted: good.
- Each scenario sets up its own cart in the `Given`: they can run in any order.
- The first two scenarios share their `Given` and `When` lines; this repetition is fine for now. (Gherkin has features to remove such repetition, which you will meet on Friday. Do not use them yet.)

**Step 5: Note the likely step definitions.** The distinct step texts are:

| Step text (pattern) | Used by |
|---|---|
| `the shopper has the {string} and the {string} in the cart` | Scenarios 1, 2 |
| `the shopper has the {string} in the cart` | Scenario 3 |
| `the shopper removes the {string} from the cart` | All three |
| `the cart contains only the {string}` | Scenario 1 |
| `the cart badge shows {int}` | Scenario 2 |
| `the cart is empty` | Scenario 3 |
| `the cart badge is not shown` | Scenario 3 |

Seven step definitions serve three scenarios, and further scenarios will reuse several of them. That is the economy of consistent wording.

---

## Hands-On Guided Lab: Write, Break, and Fix a Feature File

**Goal:** Create a valid feature file for saucedemo.com, break it on purpose to see parser messages, and (if your Cucumber project from the *Cucumber Framework Setup* lesson is ready) see the "undefined" output.

**Time:** 40 minutes.

**Steps:**

1. **Create the folder and file.** In your project, create `src/test/resources/features/` if it does not exist, and inside it a file `products.feature`. (If you have not yet created the Maven project, create the file in any folder; you only need a text editor for steps 1-6.)
2. **Write the feature header and story.**
   ```gherkin
   Feature: Browse products
     As a shopper
     I want to see the list of products after logging in
     so that I can choose what to buy
   ```
3. **Add the first scenario.**
   ```gherkin
     Scenario: Shopper sees six products after logging in
       Given the shopper is logged in as "standard_user"
       When the shopper opens the products page
       Then the shopper sees 6 products
   ```
   (On saucedemo.com the standard user sees six products on the inventory page. Verify this in your browser first: open the site, log in as `standard_user` / `secret_sauce`, and count.)
4. **Add a second scenario with a data table.**
   ```gherkin
     Scenario: Product names are listed
       Given the shopper is logged in as "standard_user"
       Then the products page lists these products:
         | product                           |
         | Sauce Labs Backpack               |
         | Sauce Labs Bike Light             |
         | Sauce Labs Bolt T-Shirt           |
         | Sauce Labs Fleece Jacket          |
         | Sauce Labs Onesie                 |
         | Test.allTheThings() T-Shirt (Red) |
   ```
5. **Add a comment** on its own line above the second scenario: `# The product list is fixed demo data`.
6. **Read the file aloud** to your partner. Fix any step that sounds technical.
7. **Break it on purpose (one change at a time) and note the error or behavior.** If you have an IDE plugin you will see red underlines; otherwise run Cucumber later.
   - Remove the colon after `Scenario` in scenario 1. Expected: a parser error naming that line.
   - Add a second `Feature:` line at the end. Expected: a parser error.
   - Add a row to the table with a different number of cells. Expected: an inconsistent cell count error.
   - Write `Given the shopper is logged in as "standard_user" # comment` (trailing comment). Expected: the file parses, but the step text now includes `# comment`, so a step definition would not match.
8. **Restore the file** to its valid state.
9. **Run it with no step definitions** (only if your Cucumber project is ready). From the project root run `mvn test`. Expected output (abbreviated): both scenarios reported as *undefined*, with Java snippets such as `@Given("the shopper is logged in as {string}")`, `@When("the shopper opens the products page")`, and `@Then("the shopper sees {int} products")`. The data table step produces a snippet with a `io.cucumber.datatable.DataTable` parameter.
10. **Save the snippets** in a scratch file; you will turn them into step definitions in the next lesson.

**Self-check:** Can you identify every keyword in your file and say whether it is structural, a step keyword, a comment, or free text? Does each scenario have exactly one `When` (the second scenario has none; discuss why that is acceptable here, since it only checks a state)?

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Parser error at line N | Syntax error at or just before line N (missing colon, extra Feature, unclosed doc string) | Compare the line with the grammar in this lesson |
| Step is reported *undefined* although you wrote a definition | Text differs (extra space, different quotes, trailing comment, singular vs. plural) | Copy the text from the feature into the pattern; check quotes and trailing characters |
| Step reported *ambiguous* | Two step definitions match the same text | Make one pattern more specific or remove the duplicate |
| Feature file is ignored | It is not under the scanned path or does not end in `.feature` | Check folder `src/test/resources/features` and the file extension |
| Table step receives wrong data | Header row treated as data, or wrong column names | Use `asMaps()` with correct headers or `asLists()` consistently |
| Doc string content has odd indentation | Doc string lines indented differently from the opening delimiter | Indent all lines consistently relative to the opening `"""` |
| Non-ASCII characters show as `?` | File not saved as UTF-8 | Save the file as UTF-8 |

---

## Common Mistakes

1. **Writing UI mechanics instead of behavior.** "Click", "type", and ids belong to step definitions and page objects.
2. **Several behaviors in one scenario.** If the title needs the word "and", split it.
3. **Inconsistent wording.** "the user", "the customer", "the shopper" for the same role cause duplicate step definitions. Pick one term and keep it.
4. **Trailing comments on step lines.** They become part of the step text.
5. **Assuming `Given`, `When`, `Then` matter to the matching.** Cucumber ignores the keyword when matching; keep them correct for readers anyway.
6. **Copying smart quotes** from word processors.
7. **Depending on scenario order.** Each scenario must be self-contained.
8. **Using Friday's features too early.** Scenario Outlines, Background, Rules, and tags come later; copying them without understanding creates confusion.

---

## Practice Exercises

1. **Anatomy.** Label each line of the example feature file above as one of: comment, feature title, description, scenario title, Given, When, Then, And, or But.
2. **Write a feature file.** Write `cart.feature` with a story description and three scenarios (add one item, add two items, remove an item) in the business language. Use at least one `And` and one `But`.
3. **Data table.** Rewrite the "add two items" scenario to use a data table for the products and quantities. What would the Java step method receive?
4. **Doc string.** Write a scenario in which the confirmation email's text is checked using a doc string.
5. **Find the errors.** Fix every syntax error in this snippet:

   ```gherkin
   Feature Checkout
   Given the shopper has an item in the cart
   Scenario Pay by card
     When the shopper pays
     | card | 4111 |
     Then "Thank you" is displayed
   ```
6. **Imperative to declarative.** Rewrite in declarative style: *"When I click on //button[@id='login-button'] and wait 3 seconds, Then I verify that the text of the div with class 'title' equals 'Products'."*
7. **Undefined steps.** In your project with Cucumber (see *Cucumber Framework Setup*), run the login feature without step definitions. Copy the generated snippets and describe what Cucumber is telling you.
8. **Peer review.** Swap your `cart.feature` with a partner. Check it against the ten style rules, and write down three improvement suggestions.
9. **Predict the statuses.** A scenario has five steps; step 2 throws an exception; step 4 has no matching definition. State the status of each step and of the scenario.
10. **Story to feature.** Convert this story into a feature file with three scenarios: *"As a shopper, I want to log out, so that nobody else can use my account on a shared computer."* Use the site <https://www.saucedemo.com> (the logout link is in the side menu) to make your examples accurate.
11. **Banking feature.** Write a feature file (title, description, and two scenarios) for withdrawing cash: one scenario for a successful withdrawal, one for insufficient funds. Use concrete amounts.
12. **Tricky text.** Which of these step lines would be matched by the expression `the cart contains {int} items`? (a) `Then the cart contains 3 items`, (b) `Then the cart contains 1 item`, (c) `And the cart contains "3" items`, (d) `Then the cart contains 2.5 items`.

---

## Solutions and Hints

**1. Anatomy.** Line 1: comment. Line 2: feature title. Lines 3-5: description. Each `Scenario:` line: scenario title. `Given the customer is on the login page`: Given. `When the customer logs in ...`: When. `Then the error message ...` / `Then the customer sees ...`: Then. `And the customer remains ...`: And (continuing Then). `But the customer does not see ...`: But (continuing Then).

**2. Write a feature file.** Sample:

```gherkin
Feature: Shopping cart
  As a shopper
  I want to manage the items in my cart
  so that I can buy exactly what I want

  Scenario: Add one item
    Given the shopper is on the products page
    When the shopper adds the "Sauce Labs Backpack" to the cart
    Then the cart contains 1 item

  Scenario: Add two items
    Given the shopper is on the products page
    When the shopper adds the "Sauce Labs Backpack" to the cart
    And the shopper adds the "Sauce Labs Bike Light" to the cart
    Then the cart contains 2 items
    But the cart does not contain "Sauce Labs Onesie"

  Scenario: Remove an item
    Given the shopper has the "Sauce Labs Backpack" in the cart
    When the shopper removes the "Sauce Labs Backpack" from the cart
    Then the cart is empty
```

Hint: note the plural "2 items" and singular "1 item" would need either two step definitions or consistent wording (for example `the cart contains {int} item(s)` using optional text, which you will see in the Step Definitions lesson).

**3. Data table.**

```gherkin
Scenario: Add two items using a table
  Given the shopper is on the products page
  When the shopper adds the following products to the cart:
    | product               | quantity |
    | Sauce Labs Backpack   | 1        |
    | Sauce Labs Bike Light | 1        |
  Then the cart badge shows 2
```

The Java method receives an `io.cucumber.datatable.DataTable`; `asMaps()` gives a list of two maps, each with the keys `product` and `quantity`.

**4. Doc string.** Sample:

```gherkin
Scenario: Customer receives a welcome email
  Given a new customer registers with the email "ada@example.com"
  Then the customer receives an email with this text:
    """
    Welcome to the shop, Ada!
    Your account is ready.
    """
```

**5. Find the errors.** Corrected:

```gherkin
Feature: Checkout

  Scenario: Pay by card
    Given the shopper has an item in the cart
    When the shopper pays with the following card:
      | card | 4111 |
    Then the message "Thank you" is displayed
```

Errors fixed: missing colons after `Feature` and `Scenario`; a step directly under `Feature` (moved into the scenario); a table attached to a step that did not introduce it (made the table belong to the step it describes); a `Then` that had no subject. Also note that the table has no header row, which is allowed here because the step definition decides how to read it.

**6. Imperative to declarative.** `When the customer logs in with valid credentials` and `Then the customer sees the products page`. Remove the locator, the explicit wait (waits are in the code, as you learned earlier this week), and the CSS class.

**7. Undefined steps.** Cucumber is saying: "I read your scenario, I found no Java method matching these lines; here is a starting point for each." The snippets contain annotation, expression, method signature, and a pending exception.

**8. Peer review.** Check: business language, single `When`, consistent wording, plain quotes, titles that name behavior, no locators.

**9. Predict the statuses.** Step 1 passed; step 2 failed; step 3 skipped; step 4 undefined; step 5 skipped. The scenario as a whole is failed. Fix the failing step first, then write the missing definition.

**10. Story to feature.** Sample scenarios: "Logged-in shopper logs out and sees the login page"; "After logout, the products page cannot be reached with the Back button" (verify the real behavior on the site and adjust); "After logout, the username field is empty". Hint: do not write the "Back button" scenario until you have checked what the site does.

**11. Banking feature.** Sample:

```gherkin
Feature: Cash withdrawal
  As an account holder
  I want to withdraw cash
  so that I can pay in cash

  Scenario: Withdraw within the balance
    Given the account holder has a balance of 200.00
    When the account holder withdraws 50.00
    Then the balance is 150.00

  Scenario: Withdraw more than the balance
    Given the account holder has a balance of 40.00
    When the account holder withdraws 50.00
    Then the withdrawal is refused with the message "Insufficient funds"
    And the balance is 40.00
```

**12. Tricky text.** (a) matches. (b) does not match: `item` is not `items`. (c) does not match: `{int}` does not accept a quoted value. (d) does not match: `2.5` is not an integer (`{double}` or `{float}` would be needed).

---

## Self-Check Questions

1. **What file extension do Gherkin files use, and where do they usually live in a Maven project?** `.feature`, under `src/test/resources/features`.
2. **How many `Feature:` lines can a file contain?** One.
3. **Does Cucumber treat `Given` differently from `When` when matching a step to code?** No. The keywords are for readers; matching uses only the text.
4. **What is the difference between a data table and a doc string?** A data table passes a grid of rows and columns to one step; a doc string passes a block of multi-line text as a single string.
5. **Why does `Given the user is logged in # context` cause trouble?** Gherkin comments cannot follow a step on the same line; `# context` becomes part of the step text, so matching fails.
6. **What does an *undefined* step mean, and what does Cucumber give you?** No step definition matches the text; Cucumber prints a snippet that you can copy and complete.
7. **When a step fails, what happens to the steps after it?** They are skipped.
8. **Name two style rules for good Gherkin.** For example: write in business language rather than UI mechanics; one scenario describes one behavior.

---

## Summary

- **Gherkin** is a line-based, plain-text language, with files ending in `.feature`, used to write executable specifications that both business people and Cucumber can read.
- A file holds **one `Feature`**, one or more **`Scenario`s**, and each scenario holds **steps** starting with **`Given`**, **`When`**, **`Then`**, **`And`**, **`But`** (or `*`).
- Cucumber matches steps by their **text**, not by the keyword; keywords are for human readability. Consistent wording is what lets one step definition serve many scenarios.
- **Comments** use `#` on their own line; **descriptions** are free text under `Feature`/`Scenario`; **data tables** (`|`) pass structured data to one step; **doc strings** (`"""`) pass multi-line text.
- Gherkin works in many languages via `# language:`.
- Step results are **passed, failed, skipped, undefined, pending, or ambiguous**. A failure skips the rest of that scenario.
- Write **declarative, business-language, one-behavior** scenarios with consistent wording and no implementation details.
- A user story becomes a feature description and each acceptance criterion becomes one or more scenarios.
- `Scenario Outline`, `Background`, `Rule`, and **tags** are covered in depth on Friday.

---

## Additional Resources

- Cucumber documentation, *Gherkin Reference*: https://cucumber.io/docs/gherkin/reference/
- Cucumber documentation, *Gherkin: Better Gherkin*: https://cucumber.io/docs/bdd/better-gherkin/
- Cucumber documentation, *Gherkin Syntax overview*: https://cucumber.io/docs/gherkin/
- Cucumber documentation, *Cucumber Expressions*: https://cucumber.io/docs/cucumber/cucumber-expressions/
