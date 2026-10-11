# Step Definitions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **step definition** is and how Cucumber **matches** a Gherkin step to a Java method, including how parameters are extracted.
- Write step definitions using the annotations `@Given`, `@When`, and `@Then` (from `io.cucumber.java.en`).
- Use **Cucumber Expressions** with parameter types `{string}`, `{int}`, `{float}`, `{word}`, and `{}` (anonymous), and use regular expressions when needed.
- Receive **data tables** (`DataTable`) and **doc strings** in step methods.
- Share state between steps in the same scenario safely (instance fields of the step class, and a **shared context object** injected through the constructor).
- Organize step definitions into well-named classes by domain and avoid duplicates and **ambiguous** steps.
- Connect step definitions to **page objects** and keep assertions in `Then` methods.
- Read Cucumber's **undefined-step snippets** and fix **undefined**, **ambiguous**, and **pending** steps using the real console messages.
- Apply best practices: thin step definitions, no logic duplication, no step calling other steps.

---

## Why This Matters

Feature files are only specifications until something **executes** them. **Step definitions** are the **glue** between the plain-language steps and the code that drives the application. They are where BDD meets Selenium: each Gherkin line triggers a Java method that calls your page objects, which call WebDriver.

Think of a feature file as a **script for a play** and the step definitions as the **actors who know how to perform each line**. The script says "the customer logs in"; the actor (a Java method) knows which buttons to press. A script with no actors does nothing; actors with no script have nothing to do. Cucumber is the stage manager that reads each line aloud and finds the actor who can perform it.

Quality here decides whether your BDD suite is maintainable. Well-organized step definitions are short, reusable, and free of locators. Badly organized ones become the same unmaintainable script code the Page Object Model was meant to avoid, only hidden behind Gherkin. In today's pair exercise and the Project 2 milestone (shopping flows on `saucedemo.com`) you will write step definitions for your own features, so this lesson is the one you will keep open on your second monitor.

What you need from earlier in the course: **page objects** (`LoginPage`, `InventoryPage`, and so on) and a **`DriverFactory`** from Monday to Wednesday, and the Given/When/Then roles from the previous lesson. Everything in this lesson *builds on* those; no Selenium code is rewritten.

---

## The Concept

### 1. What Is a Step Definition?

A **step definition** is a Java method annotated with a pattern. When Cucumber executes a step such as

```gherkin
When the shopper adds "Sauce Labs Backpack" to the cart
```

it searches all step definitions for a pattern that matches the step text, then **calls that method** with any values extracted from the text:

```java
@When("the shopper adds {string} to the cart")
public void theShopperAddsToTheCart(String product) {
    new InventoryPage(context.driver()).addToCart(product);
}
```

The relationship:

```
 Feature file line (text)                Step definition (Java)
 ─────────────────────────               ───────────────────────────────────────
 When the shopper adds "Sauce Labs       @When("the shopper adds {string} to the cart")
      Backpack" to the cart       ─────► void theShopperAddsToTheCart(String product)
                                         product = "Sauce Labs Backpack"
```

Key facts:

- Matching is based on the **text only** (after the keyword). The annotation type (`@Given`, `@When`, `@Then`) does **not** restrict matching; they are interchangeable for matching purposes and exist for readability.
- Each step in a scenario is matched **independently**, executed in order.
- A step definition can be used by **any number of steps** in any number of scenarios and files: this is how reuse works.
- The **method name** is irrelevant to matching; use a name that describes the step.

#### How Cucumber matches a step: a trace

Let us follow one step slowly, exactly as Cucumber does.

**Step text in the feature file:** `Then the cart count shows 3`

| Stage | What happens |
|---|---|
| 1. Strip keyword | `Then ` is removed. Text to match: `the cart count shows 3`. |
| 2. Try each definition | Cucumber compiles every annotation text into a matcher and tries them all. `the shopper adds {string} to the cart` fails (different words). `the cart count shows {int}` is tried next. |
| 3. Literal words | `the cart count shows ` must match exactly, character for character. It does. |
| 4. Parameter | `{int}` means "an optional minus sign and digits". `3` qualifies. The text `3` is captured. |
| 5. Convert | The captured text is converted to the type of the method parameter, here `int 3`. |
| 6. Count the matches | Exactly one definition matched. (Zero means *undefined*; two or more means *ambiguous*.) |
| 7. Invoke | Cucumber creates the step class (once per scenario), then calls `theCartCountShows(3)`. |
| 8. Outcome | The method returns: **passed**. It throws `AssertionFailedError` or another exception: **failed**. |

Now the same trace with a step that **does not match**: `Then the cart count shows three`. At stage 4, `{int}` cannot capture `three` (it is not digits), so that definition fails. No other definition matches, so the step is **undefined**. This is why digits in the feature file and `{int}` in the code must agree.

### 2. Where Step Definition Classes Live

By convention they live in a **package of their own** inside `src/test/java`, and the runner is told this package (the **glue**):

```
src/test/java/com/revature/qea/steps/
     ├── LoginSteps.java
     ├── CartSteps.java
     └── CheckoutSteps.java
```

All classes in the glue package (and sub-packages) are scanned automatically. Step definition classes are plain Java classes: no base class and no special annotation on the class itself (a no-argument public constructor, or a constructor for dependency injection, is enough; see Section 9).

**Why "glue"?** The word describes the job: this code sticks the readable text to the executable code. The glue setting tells Cucumber *which packages to search*; a class outside the glue package is invisible to Cucumber, even if it is full of correct step definitions. You will configure it in the next lesson (*Cucumber Framework Setup*).

### 3. The Annotations and Imports

```java
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;    // And and But annotations also exist, but are rarely needed
import io.cucumber.java.en.But;
```

`And`/`But` annotations exist but are **not needed**: a step written with `And` in the feature file matches whichever annotation fits its meaning. Use `@Given`, `@When`, `@Then` to document the role.

**Common import mistake:** IDEs offer several `Given`/`When`/`Then` classes (for other languages such as `io.cucumber.java8` or the older `cucumber.api.java.en`). For Cucumber 7 with Java, the right package is `io.cucumber.java.en`. A wrong import compiles but the steps are never found (or the import fails to resolve).

### 4. Cucumber Expressions and Parameter Types

Patterns are written in **Cucumber Expressions**: readable text with **parameter types** in curly braces, which capture parts of the step text and convert them to Java types.

| Parameter type | Matches | Java type | Example step text | Example expression |
|---|---|---|---|---|
| `{string}` | A quoted string (`"..."` or `'...'`); the quotes are **not** included in the value | `String` | `adds "Sauce Labs Backpack"` | `adds {string}` |
| `{int}` | An integer (`-5`, `0`, `42`) | `int` / `Integer` | `shows 3 items` | `shows {int} items` |
| `{float}` | A decimal (`3.5`, `-0.2`) | `float` / `Float` | `costs 9.99` | `costs {float}` |
| `{double}` | A decimal as double | `double` | `total is 29.99` | `total is {double}` |
| `{word}` | A single word without whitespace | `String` | `the user admin logs in` | `the user {word} logs in` |
| `{bigdecimal}`, `{long}`, `{short}`, `{byte}`, `{biginteger}` | Corresponding numbers | respective Java types | | |
| `{}` | Anything (anonymous parameter) | `String` | | `the {} page` |

Parameters are passed **to the method in the order they appear**:

```java
@When("the customer logs in with username {string} and password {string}")
public void theCustomerLogsIn(String username, String password) { ... }
```

```gherkin
When the customer logs in with username "standard_user" and password "secret_sauce"
```

Here `username` receives `standard_user` (first `{string}`) and `password` receives `secret_sauce` (second `{string}`). Java parameter *names* do not matter to matching; only their **order and type** do. If you swap the order in the method signature, the values swap too.

#### Which parameter type should I choose?

| Situation | Use | Why |
|---|---|---|
| Names, messages, text that may contain spaces ("Sauce Labs Backpack") | `{string}` and quote it in the feature | Quotes mark exactly where the value starts and ends |
| Counts and quantities (3 items) | `{int}` | Cucumber converts to `int` for you; no `Integer.parseInt` |
| Prices (29.99) | `{double}` (or `{bigdecimal}` for money in a real project) | Decimal point is understood |
| A single token without spaces (`admin`) | `{word}` | Rarely needed; prefer `{string}` for clarity |
| Anything, when nothing else fits | `{}` | Use sparingly; it is greedy and can cause ambiguity |

**Optional text and alternatives** in expressions:

```java
@Then("the cart contains {int} item(s)")          // (s) optional: matches "item" and "items"
@Given("the shopper is on the login/home page")   // alternation: "login" or "home"
```

**Escaping:** to match a literal special character (`{`, `}`, `(`, `)`, `/`), put a backslash in front of it. In Java a backslash inside a string must itself be written `\\`, so a step that really contains parentheses is written:

```java
@Then("the price is shown as 29.99 \\(including tax\\)")
```

If this looks ugly, rephrase your step to avoid parentheses; plain language is easier to maintain.

**Regular expressions** are also supported (when the pattern starts with `^` and ends with `$`, Cucumber treats it as a regex):

```java
@Given("^the shopper has (\\d+) products? in the cart$")
public void theShopperHasProducts(int count) { ... }
```

Capture groups become parameters. Prefer Cucumber Expressions for readability; use regex only when you need its extra power.

#### Cucumber Expression vs regular expression, side by side

| Goal | Cucumber Expression | Regular expression |
|---|---|---|
| Quoted text | `adds {string}` | `^adds \"([^\"]*)\"$` |
| A number | `has {int} items` | `^has (\\d+) items$` |
| Optional "s" | `item(s)` | `items?` |

The expression forms are shorter and safer, which is why this course uses them.

### 5. Writing a Step Definition, One Piece at a Time

Take the step `Given the customer is on the login page` and build its definition in five small moves.

1. **Pick the annotation** from the keyword's role: `@Given`.
2. **Copy the text** from the feature file *exactly*, without the keyword: `"the customer is on the login page"`.
3. **Replace the variable parts** with parameter types. This step has none.
4. **Name the method** after the step: `theCustomerIsOnTheLoginPage`. (Names do not affect matching; clear names help reading stack traces.)
5. **Write the body** as a call to a page object (never a locator):

```java
@Given("the customer is on the login page")
public void theCustomerIsOnTheLoginPage() {
    loginPage = new LoginPage(context.driver()).open();
}
```

Line by line: `@Given("...")` registers the method for that text; `public void` is required (step methods are public; return values are ignored); `new LoginPage(context.driver())` builds the page object around this scenario's browser; `.open()` navigates to `https://www.saucedemo.com` and returns the same page object so it can be stored in `loginPage`.

### 6. Step Definition Examples for the Login Feature

```gherkin
Scenario: Successful login with valid credentials
  Given the customer is on the login page
  When the customer logs in with username "standard_user" and password "secret_sauce"
  Then the customer sees the products page

Scenario: Login is rejected for a wrong password
  Given the customer is on the login page
  When the customer logs in with username "standard_user" and password "wrong_password"
  Then the error message "Epic sadface: Username and password do not match any user in this service" is displayed
```

Matching step definitions:

```java
package com.revature.qea.steps;

import com.revature.qea.pages.InventoryPage;
import com.revature.qea.pages.LoginPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class LoginSteps {

    private final TestContext context;   // shared per-scenario state, injected by Cucumber (see Section 9)
    private LoginPage loginPage;
    private InventoryPage inventoryPage;

    public LoginSteps(TestContext context) {
        this.context = context;
    }

    @Given("the customer is on the login page")
    public void theCustomerIsOnTheLoginPage() {
        loginPage = new LoginPage(context.driver()).open();
    }

    @When("the customer logs in with username {string} and password {string}")
    public void theCustomerLogsInWith(String username, String password) {
        // Two possible outcomes, so we use the method that does not assume success
        loginPage.loginExpectingFailure(username, password);
    }

    @Then("the customer sees the products page")
    public void theCustomerSeesTheProductsPage() {
        inventoryPage = new InventoryPage(context.driver());       // constructor verifies the URL
        assertTrue(inventoryPage.isLoaded(), "Products page was not displayed");
    }

    @Then("the error message {string} is displayed")
    public void theErrorMessageIsDisplayed(String expectedMessage) {
        assertEquals(expectedMessage, loginPage.getErrorMessage());
    }
}
```

**Line by line:**

- `package com.revature.qea.steps;` is the glue package. The runner points Cucumber here.
- The imports: the page objects from Wednesday, the `TestContext` (built in the next lesson), the three Cucumber annotations, and two JUnit 5 assertion methods.
- `private final TestContext context;` and the constructor: Cucumber supplies the shared context (Section 9).
- `loginPage` and `inventoryPage` are fields so that the Given/When/Then methods of *this scenario* can pass the current page from one step to the next. Cucumber creates a new `LoginSteps` object per scenario, so the fields start empty each time.
- The `When` calls `loginExpectingFailure(...)`. That is a page-object method that types the credentials, clicks Login, and **stays on the login page object** because the same step has to serve both successful and failed logins. Its name is only a convention for "does not assume success".
- The first `Then` builds an `InventoryPage` and asserts `isLoaded()`. `assertTrue(condition, message)` shows the message if the condition is false.
- The second `Then` receives the expected message from the feature text via `{string}` and compares it with what the page shows. `assertEquals(expected, actual)` takes the **expected value first**, which matters because failure messages say "expected X but was Y".

Design decisions worth noticing:

- **Locators appear nowhere.** Everything goes through the page objects from Wednesday.
- Only the `@Then` methods contain **assertions** (JUnit 5's `Assertions`), keeping page objects assertion-free.
- The `{string}` parameters make a single step definition serve **every** login scenario, regardless of the user.
- The step `the customer logs in with ...` could be implemented through a method that always expects success (`loginAs`) or failure; the choice depends on your page-object design. Here we use a method that stays on the login page so that both outcomes can be checked in the Then steps (a page-object method that returns a generic result is another valid design).

### 7. Cart and Checkout Step Definitions (Second Worked Example)

The following feature uses steps from several domains. Notice how `the shopper is logged in` becomes a **shared** step.

```gherkin
Feature: Shopping cart

  Scenario: Adding a product increases the cart count
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    Then the cart count shows 1

  Scenario: Added product is listed in the cart
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    And the shopper opens the cart
    Then the cart lists "Sauce Labs Backpack"
```

```java
package com.revature.qea.steps;

import com.revature.qea.pages.CartPage;
import com.revature.qea.pages.InventoryPage;
import com.revature.qea.pages.LoginPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class CartSteps {

    private final TestContext context;

    public CartSteps(TestContext context) {
        this.context = context;
    }

    @Given("the shopper is logged in")
    public void theShopperIsLoggedIn() {
        new LoginPage(context.driver()).open().loginAs("standard_user", "secret_sauce");
    }

    @When("the shopper adds {string} to the cart")
    public void theShopperAddsToTheCart(String product) {
        new InventoryPage(context.driver()).addToCart(product);
    }

    @When("the shopper opens the cart")
    public void theShopperOpensTheCart() {
        new InventoryPage(context.driver()).openCart();
    }

    @Then("the cart count shows {int}")
    public void theCartCountShows(int expected) {
        assertEquals(expected, new InventoryPage(context.driver()).getCartCount(),
                "Unexpected number of items in the cart badge");
    }

    @Then("the cart lists {string}")
    public void theCartLists(String product) {
        List<String> names = new CartPage(context.driver()).getItemNames();
        assertTrue(names.contains(product), "Expected " + product + " in the cart but found " + names);
    }
}
```

**Explanation:**

- Each step method creates the page object it needs from `context.driver()`. Page objects hold no state beyond the driver and locators, so recreating them is cheap, and it means *any* step class can work on whatever page the browser is currently showing without receiving a page object from another class.
- `openCart()` (on `InventoryPage`) and `getItemNames()` (on `CartPage`) are examples of what your Wednesday page objects should expose. If your classes use different names, adapt the calls; the step definitions stay thin either way.
- The assertion message `"Expected Sauce Labs Backpack in the cart but found [...]"` explains the failure on its own. Writing messages like this pays off the first time a scenario goes red.

### 8. Data Tables and Doc Strings in Step Definitions

Given a step with a table:

```gherkin
When the shopper adds the following products to the cart:
  | product               |
  | Sauce Labs Bike Light |
  | Sauce Labs Onesie     |
```

the method receives an `io.cucumber.datatable.DataTable` as its **last parameter**:

```java
import io.cucumber.datatable.DataTable;
import java.util.List;
import java.util.Map;

@When("the shopper adds the following products to the cart:")
public void theShopperAddsTheFollowingProducts(DataTable table) {
    List<String> products = table.asList();            // single-column table -> flat list (header row IS included)
    ...
}
```

Common conversions:

| Table shape | Method | Result |
|---|---|---|
| One column, no header | `table.asList()` | `List<String>` |
| Header row + data rows | `table.asMaps()` | `List<Map<String,String>>`, one map per data row, keys from the header |
| Two columns as key/value pairs | `table.asMap()` | `Map<String,String>` |
| Raw cells | `table.asLists()` | `List<List<String>>` |
| With a type conversion | `table.asList(Integer.class)` etc. | typed list |

Example with a header row:

```gherkin
When the shopper adds the following products to the cart:
  | product               | quantity |
  | Sauce Labs Backpack   | 1        |
  | Sauce Labs Bike Light | 2        |
```

```java
@When("the shopper adds the following products to the cart:")
public void theShopperAddsProducts(DataTable table) {
    InventoryPage inventory = new InventoryPage(context.driver());
    for (Map<String, String> row : table.asMaps()) {
        String product = row.get("product");
        int quantity = Integer.parseInt(row.get("quantity"));
        for (int i = 0; i < quantity; i++) {
            inventory.addToCart(product);   // illustrative; real apps may have a quantity control
        }
    }
}
```

**Line by line:** `table.asMaps()` treats the first row as column names and returns one `Map` per remaining row, for example `{product=Sauce Labs Backpack, quantity=1}`. `row.get("product")` looks up the cell by its header. All cells arrive as `String`, so the quantity is converted with `Integer.parseInt`. (Sauce Demo adds one unit per click; the inner loop is purely illustrative of how table data drives the code.)

Be careful: `asList()` on a table that has a header row includes the header as the first element, because `DataTable` has no idea which row is a header. When a table has **only one column and no header** (as in a list of product names), consider adding a header for clarity and using `asMaps()` or skipping the first row.

**Mapping rows to objects:** Cucumber can convert rows to your own class with `@DataTableType` and a registered transformer; this is useful for larger projects, but beyond today's requirements.

**Doc strings.** A doc string is passed as a **`String`** (last parameter), or as `io.cucumber.docstring.DocString`:

```gherkin
Then the confirmation email contains the following text:
  """
  Thank you for your order!
  Your items will ship soon.
  """
```

```java
@Then("the confirmation email contains the following text:")
public void theConfirmationEmailContains(String expectedText) {
    assertTrue(emailBody.contains(expectedText));
}
```

The text between the `"""` lines arrives as a single multi-line string, with the indentation of the quotes removed. Use doc strings for longer text blocks (messages, JSON), and tables for lists of records.

### 9. Sharing State Between Steps

Steps in the same scenario often need to share objects: the driver, the current page, test data. Several mechanisms exist.

**a) Instance fields in one step class.** The simplest: Cucumber creates a **new instance of each step class for every scenario**, so fields are naturally scenario-scoped (as in `LoginSteps` above: `loginPage`, `inventoryPage`). The limitation is that two different step classes cannot see each other's fields.

**b) A shared "context" object via dependency injection.** When `LoginSteps` and `CartSteps` must share the same driver and current page, put the shared data in a plain class and let Cucumber **inject** it into every step class that asks for it in its constructor. The library **cucumber-picocontainer** provides this with no configuration:

```java
package com.revature.qea.support;

import com.revature.qea.drivers.DriverFactory;
import org.openqa.selenium.WebDriver;

public class TestContext {
    private WebDriver driver;

    /** Creates the browser on first use (the full version is built in Cucumber Framework Setup). */
    public WebDriver driver() {
        if (driver == null) {
            driver = DriverFactory.createDriver("chrome", false);
        }
        return driver;
    }
}
```

```java
public class CartSteps {
    private final TestContext context;

    public CartSteps(TestContext context) {     // PicoContainer injects it
        this.context = context;
    }

    @When("the shopper adds {string} to the cart")
    public void addToCart(String product) {
        new InventoryPage(context.driver()).addToCart(product);
    }
}
```

PicoContainer creates **one `TestContext` per scenario** and passes the **same instance** to every step class that requests it in that scenario, then discards it afterwards, so scenarios stay isolated. (The dependency is added in the *Cucumber Framework Setup* lesson. Creating the driver at the start of each scenario and quitting it at the end is the job of **hooks**, covered on **Friday**; for today's work your instructor's skeleton, or a simple helper, will create the driver.)

#### Why dependency injection? The "shared notebook" analogy

Imagine a relay race where each runner (step class) needs the same baton (the browser). Without a rule, each runner might grab a new baton, and the second runner would start with a brand-new, empty browser, losing the login done by the first. With PicoContainer, a referee (Cucumber) hands **the same baton** to every runner in one race (scenario), and a **fresh baton** at the start of the next race. That is constructor injection.

#### What happens, in order, when a scenario starts

1. Cucumber sees that `LoginSteps` and `CartSteps` are needed by the scenario's steps.
2. It notices their constructors take a `TestContext`.
3. PicoContainer creates one `TestContext` (no browser yet, because `driver()` is lazy).
4. The first step that calls `context.driver()` triggers the browser launch.
5. Every other step class receives the same `TestContext`, so `context.driver()` returns the **same** browser.
6. When the scenario ends, the objects are discarded. (Quitting the browser is the part that Friday's hooks will automate.)

**c) Static variables**: avoid them. They survive across scenarios and make tests dependent on each other and unsafe for parallel runs.

### 10. Undefined, Pending, and Ambiguous Steps

When you run a feature with no matching step definition, Cucumber does not crash; it prints a **snippet**:

```
Undefined scenarios:
file:///.../login.feature:6 # Successful login with valid credentials

1 Scenarios (1 undefined)
3 Steps (2 skipped, 1 undefined)

You can implement missing steps with the snippets below:

@Given("the customer is on the login page")
public void the_customer_is_on_the_login_page() {
    // Write code here that turns the phrase above into concrete actions
    throw new io.cucumber.java.PendingException();
}
```

Workflow: **copy the snippet** into a step class, rename the method if you like, and implement it. Until you do, the `PendingException` marks the step as **pending**, which tells you "known, not yet implemented".

Cucumber even *guesses* the expression for you: if the step contains `"standard_user"` it will write `{string}`, and if it contains `3` it will write `{int}`, together with matching method parameters. Always check the guess: a value that is really part of the rule (for example a specific error message) may be better as `{string}` anyway, but a number that should stay literal can be changed by hand.

| Status | Meaning | What to do |
|---|---|---|
| **Undefined** | No step definition matches the text | Copy the generated snippet; write the method |
| **Pending** | A step definition throws `PendingException` | Implement the body |
| **Ambiguous** | **More than one** step definition matches the same text | Make the expressions distinct or delete the duplicate; Cucumber fails the step with an `AmbiguousStepDefinitionsException` listing the matches |
| **Failed** | The method threw an exception or assertion error | Fix the application or the test |
| **Skipped** | An earlier step failed | Fix the earlier step first |

Example of ambiguity:

```java
@Then("the cart shows {int} items")
public void a(int n) { ... }

@Then("the cart shows {word} items")      // also matches "the cart shows 3 items" because "3" is a word
public void b(String s) { ... }
```

Fix by making patterns unambiguous (for example removing the `{word}` version or making it more specific).

#### What the real error messages look like

**Ambiguous step** (the console lists every match so you can find the culprits):

```
io.cucumber.core.runner.AmbiguousStepDefinitionsException: "the cart shows 3 items" matches more than one step definition:
  "the cart shows {int} items" in com.revature.qea.steps.CartSteps.a(int)
  "the cart shows {word} items" in com.revature.qea.steps.CartSteps.b(java.lang.String)
```

Diagnosis: two lines in the list, so two definitions claim the same text. Delete one or tighten one.

**Duplicate definition** (the same expression written twice, often in two files):

```
io.cucumber.core.runtime.DuplicateStepDefinitionException: Duplicate step definitions in
com.revature.qea.steps.LoginSteps.theShopperIsLoggedIn() and
com.revature.qea.steps.CartSteps.theShopperIsLoggedIn()
```

Diagnosis: you put `the shopper is logged in` in two classes. Keep it in exactly one (usually a common domain class).

**Undefined parameter type** (a typo inside the braces):

```
io.cucumber.cucumberexpressions.UndefinedParameterTypeException: Undefined parameter type 'strng'.
Please register a ParameterType for 'strng'.
```

Diagnosis: the text inside `{ }` is not one of the built-in types (`string`, `int`, `float`, ...). Fix the spelling.

**Wrong parameter count or type.** If the expression has two parameters but the method has one, or the method expects `int` but the text captured `3.5`, the step fails or is reported as an error, with a message along these lines (exact wording varies by version):

```
Could not convert arguments for step [the cart count shows {int}] defined at 'CartSteps.theCartCountShows(int)'.
```

Diagnosis: the expression and the Java signature disagree. Count the `{...}` and compare with the method parameters, in order.

**Pending step** (known, not yet implemented):

In the report the step is shown as *pending* (the generated snippet throws `new io.cucumber.java.PendingException()`). Implement the body and remove that line.

### 11. Best Practices for Step Definitions

1. **Keep step definitions thin.** Each method should do one thing: call a page-object method (or two) and, in `Then`, assert. Business logic and locators belong in page objects/services.
2. **No locators, no `driver.findElement`** in step definitions.
3. **Assertions only in `@Then`** (and `@And`/`@But` continuing a Then).
4. **Do not call one step definition from another** (calling step methods like ordinary methods couples them and hides intent). If two steps share logic, extract a shared private method or a page-object method.
5. **Organize by domain**, not by feature file: `LoginSteps`, `CartSteps`, `CheckoutSteps`. A step like `the shopper is logged in` is used in many features, so it belongs to a common domain class.
6. **Phrase patterns by meaning, not by implementation**, so the code can change while the text stays.
7. **Avoid overly generic patterns** such as `{string} {string} {string}` or `{}` that can match many steps and cause ambiguity.
8. **Use meaningful Java parameter names** (`product`, `username`) and types; convert in the signature (`int`) instead of parsing strings.
9. **Do not rely on step order across scenarios** or on static state.
10. **Add descriptive assertion messages** so failures read well in reports.
11. **No `Thread.sleep`.** Waiting belongs to the page objects and their explicit waits (from Wednesday), not to steps.

#### Good vs bad: the same step, rewritten

Bad:

```java
@When("the shopper adds the backpack")
public void add() throws InterruptedException {
    driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();   // locator in a step
    Thread.sleep(3000);                                                      // fixed sleep
    Assert.assertEquals("1", driver.findElement(By.className("shopping_cart_badge")).getText()); // assertion in a When
}
```

Problems: a locator in the step, `Thread.sleep`, an assertion inside a `When`, a hard-coded product that makes the step usable only once, a `driver` that is not obtained from the context, and it mixes Arrange/Act/Assert in one method.

Good:

```java
@When("the shopper adds {string} to the cart")
public void theShopperAddsToTheCart(String product) {
    new InventoryPage(context.driver()).addToCart(product);
}

@Then("the cart count shows {int}")
public void theCartCountShows(int expected) {
    assertEquals(expected, new InventoryPage(context.driver()).getCartCount());
}
```

Result: parameterized, no locators, no sleeps (the page object waits), each method one job.

### 12. The Complete Chain

```
login.feature                    LoginSteps.java               LoginPage.java            Selenium
─────────────                    ───────────────               ──────────────            ────────
When the customer logs in   ──►  theCustomerLogsInWith(...)──► loginExpectingFailure() ─► sendKeys(), click()
  with username "x" and
  password "y"
```

Everything you built Monday-Wednesday is reused as is; the BDD layer adds only the feature text and a thin glue layer.

---

## Guided Lab: Your First Step Definitions

**Goal:** make the login scenarios from Section 6 run (the framework itself is set up in the next lesson, so do this lab together with it, or read it now and run it after that lesson).

1. Make sure you have the Wednesday page objects `LoginPage` and `InventoryPage`, and the `DriverFactory`.
2. Create `src/test/resources/features/login.feature` with the two scenarios from Section 6 under `Feature: Login`.
3. Create the package `com.revature.qea.steps` under `src/test/java`.
4. **Generate snippets first.** Run the feature with no step definitions. Read the console output; you should see something like:

   ```
   2 Scenarios (2 undefined)
   6 Steps (6 undefined)
   ```

   plus snippets. Notice that `{string}` was already guessed for the quoted values.
5. Create `LoginSteps.java`. Paste the four snippets and delete the `PendingException` lines as you implement each method.
6. Add the `TestContext` constructor from Section 9 to `LoginSteps`.
7. Implement the bodies using the code in Section 6.
8. Re-run. **Expected result:**

   ```
   2 Scenarios (2 passed)
   6 Steps (6 passed)
   ```

   Two browsers open in turn (until Friday's hooks you may need to close them manually).
9. **Reuse test.** Add a third scenario that logs in as `locked_out_user` and expects "Epic sadface: Sorry, this user has been locked out.". Write **no new step definitions**. It should pass, which proves that one parameterized step can serve many scenarios.
10. **Break and repair.** In the feature, change `logs in with` to `signs in with` in one step. Run: that step is undefined and the later steps are skipped. Revert it.

---

## Troubleshooting Checklist

| Console symptom | Diagnosis | Fix |
|---|---|---|
| `Undefined` with a snippet for a step you already wrote | Wrong glue package, or a text difference (quotes, double spaces) | Compare text character by character; check the glue configuration |
| `NullPointerException ... loginPage` in the `When` | The `Given` that creates `loginPage` did not run in this class (for example it lives in another class) | Keep related steps in one class, or create the page object in each step from `context.driver()` |
| `NullPointerException ... context` | The constructor was not used (no PicoContainer dependency) | Add `cucumber-picocontainer` to `pom.xml` |
| Browser opens twice per scenario | Two different `TestContext` objects exist (for example `new TestContext()` created by hand) | Receive the context through the constructor only |
| `AmbiguousStepDefinitionsException` | Overlapping patterns | See Section 10 |
| `expected: <Epic sadface: ...> but was: <...>` | Text in the feature differs from the page text (case, punctuation) | Copy the exact message from the page |
| `StaleElementReferenceException` inside a step | A page object reused an element after the page changed | Re-find the element inside the page-object method (Wednesday's lesson) |

---

## Practice Exercises

1. **Write the patterns.** Write Cucumber Expressions for:
   - `the cart count shows 3`
   - `the shopper adds "Sauce Labs Backpack" to the cart`
   - `the order total is 29.99`
   - `the shopper has 1 product in the cart` and `the shopper has 2 products in the cart` (single pattern using `(s)`)
2. **Implement login steps.** Given the login feature in the Gherkin lesson, write `LoginSteps` that uses your Wednesday page objects. Run all four scenarios.
3. **Data table.** Implement a step that takes a table of product names and quantities and adds them to the cart. Print the `asMaps()` result to see its structure.
4. **Break it on purpose.** (a) Misspell a word in a feature step to get an **undefined** step snippet and read it. (b) Create two step definitions that both match one step and observe the **ambiguous** error.
5. **Refactor to a context.** Make `LoginSteps` and `CartSteps` share a `TestContext` with the driver, using constructor injection (`context.driver()`).
6. **Spot the smells.** What is wrong with this step definition, and how do you fix it?

   ```java
   @When("the shopper adds the backpack")
   public void add() throws InterruptedException {
       driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();
       Thread.sleep(3000);
       Assert.assertEquals("1", driver.findElement(By.className("shopping_cart_badge")).getText());
   }
   ```
7. **Reuse count.** Count how many scenarios in your feature files use each step definition. Which definitions are used only once? Could any be merged through parameters?
8. **Project 2 milestone.** Write feature files and step definitions for two Project 2 flows, using page objects only. Commit with a clear message.
9. **Predict the match.** For each pair, say whether the step matches the expression, and what the parameter value is:
   - Expression `the cart shows {int} item(s)`; steps `the cart shows 1 item`, `the cart shows 12 items`, `the cart shows two items`.
   - Expression `the customer logs in as {string}`; steps `the customer logs in as "problem_user"`, `the customer logs in as problem_user`.
10. **Price step.** Write the feature line and the step definition for "the order total is 29.99" using `{double}`. Why might `double` be a poor choice for real money?
11. **Doc string.** Write a step that takes a doc string containing a multi-line error message and asserts that the page error text contains it.
12. **Domain split.** Your `LoginSteps` class has grown to include cart and checkout steps. Describe how you would split it and where `the shopper is logged in` should live.

---

## Solutions and Hints

**1. Patterns.**

- `@Then("the cart count shows {int}")`
- `@When("the shopper adds {string} to the cart")`
- `@Then("the order total is {double}")`
- `@Given("the shopper has {int} product(s) in the cart")`

**2. Login steps (hint).** Reuse the class in Section 6. Check that the `When` uses a page-object method that does not assume success when the same step is used for both valid and invalid credentials. If all four scenarios pass, count the step definitions: there should be four methods for all of them.

**3. Data table (hint).** The header row is the first row (`| product | quantity |`). Use `table.asMaps()`; `row.get("quantity")` is a `String`, so convert with `Integer.parseInt`. Printing the result shows `[{product=Sauce Labs Backpack, quantity=1}, ...]`.

**4. Break it on purpose.** (a) Expect `Undefined` and a snippet containing the *changed* wording. (b) Expect `AmbiguousStepDefinitionsException` listing both methods. Remove one to repair.

**5. Context refactor (hint).** Move `driver()` into `TestContext`. Each steps class gets `private final TestContext context;` and a one-parameter constructor. Replace all `driver` references with `context.driver()`. Verify that `the shopper is logged in` in one class and `the shopper adds ...` in another operate on the **same** browser window.

**6. Smells.** A locator in the step; `Thread.sleep`; an assertion in a When; the product is hard-coded; the `driver` is not obtained from the context; two behaviors in one method. Fix: see the "good" version in Section 11.

**7. Reuse count (hint).** Steps used once are not wrong, but if two once-used steps differ only by a value, merge them with `{string}` or `{int}`.

**8. Project 2 milestone (hint).** Start with the shared `the shopper is logged in` step in a common class, then one feature per flow (for example login and cart). Run the dry-run option from the setup lesson to see undefined steps before opening any browser.

**9. Predict the match.**

- `the cart shows 1 item` matches (`item(s)` with the optional "s" absent), `n = 1`.
- `the cart shows 12 items` matches, `n = 12`.
- `the cart shows two items` does **not** match: `{int}` needs digits.
- `the customer logs in as "problem_user"` matches, value `problem_user` (quotes removed).
- `the customer logs in as problem_user` does **not** match: `{string}` requires quotes.

**10. Price step.**

```gherkin
Then the order total is 29.99
```

```java
@Then("the order total is {double}")
public void theOrderTotalIs(double expected) {
    assertEquals(expected, new CheckoutOverviewPage(context.driver()).getTotal(), 0.001);
}
```

`double` cannot represent many decimal values exactly (for example 0.1 + 0.2 is not exactly 0.3), so comparisons need a tolerance. For real money prefer `{bigdecimal}` and `BigDecimal`. `CheckoutOverviewPage` is an illustrative page-object name.

**11. Doc string (sample).**

```java
@Then("the error text contains:")
public void theErrorTextContains(String expectedText) {
    String actual = new LoginPage(context.driver()).getErrorMessage();
    assertTrue(actual.contains(expectedText), "Expected text: " + expectedText + " but page showed: " + actual);
}
```

**12. Domain split.** Create `LoginSteps` (login/page steps), `CartSteps`, `CheckoutSteps`. Put `the shopper is logged in` in one class that is clearly the owner (commonly `LoginSteps` or a `CommonSteps` class). Because every step class receives the same `TestContext`, the steps in one class operate on the same browser as steps in the others.

---

## Self-Check Questions

1. **What does Cucumber use to decide which step definition to call?**
   The step text after the keyword, compared with each annotation's Cucumber Expression. The keyword and the method name are irrelevant.
2. **What is the difference between `{string}` and `{word}`?**
   `{string}` needs quotes and may contain spaces; `{word}` is a single token without whitespace and without quotes.
3. **What happens when no step definition matches?**
   The step is reported *undefined* and Cucumber prints a snippet; the remaining steps are skipped.
4. **Why does each scenario get a fresh step-class instance?**
   So fields (and the injected `TestContext`) never leak data from one scenario into the next.
5. **How do two step classes share the same browser?**
   Both take a `TestContext` in their constructors; PicoContainer gives them the same instance within a scenario.
6. **Where do assertions belong?**
   In `@Then` step definitions; page objects and Given/When methods perform actions only.
7. **A step has `"Sauce Labs Backpack"` in quotes. Which parameter type captures it?**
   `{string}`, delivered as a `String` without the quotes.
8. **Why avoid calling one step definition method from another?**
   It couples steps and hides intent; extract the shared work into a private helper or a page-object method instead.

---

## Summary

- A **step definition** is a Java method, annotated with `@Given`, `@When`, or `@Then` and a **Cucumber Expression**, that Cucumber calls when a step's **text** matches; keywords do not affect matching.
- Cucumber Expressions use **parameter types** (`{string}`, `{int}`, `{float}`, `{word}`, `{}`), plus optional text `(s)` and alternation `a/b`; regular expressions are supported when needed.
- **Data tables** arrive as `DataTable` (`asList`, `asMaps`, `asMap`), **doc strings** as `String`.
- A **new step-class instance** is created for each scenario; use instance fields or a **dependency-injected context** (`TestContext`, via PicoContainer, accessed as `context.driver()`) to share state; avoid statics.
- Steps can be **undefined** (copy the generated snippet), **pending**, **ambiguous** (fix overlapping patterns), **failed**, or **skipped**; the console messages tell you which.
- Keep step definitions **thin**: call page objects, no locators, no sleeps, **assertions only in Then**, no step-calls-step, organized by domain.
- Creating and closing the browser per scenario is done with **hooks** (covered in depth on Friday).

---

## Additional Resources

- Cucumber documentation, *Step Definitions (Cucumber-JVM)*: https://cucumber.io/docs/cucumber/step-definitions/
- Cucumber documentation, *Cucumber Expressions*: https://cucumber.io/docs/cucumber/cucumber-expressions/
- Cucumber-JVM documentation, *Sharing state / Dependency injection*: https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-picocontainer
