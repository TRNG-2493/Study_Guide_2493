# Cucumber In-Class Handout 3: Reusable Scenarios

**Topics:** 3.1 Scenario Outline and Examples · 3.2 Background and Rule · 3.3 Hooks

**How to use this handout:** the same layout as before. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Cucumber Handouts 1–2:** `login.feature` (final version from Handout 1, topic 1.4: 4 scenarios), `RunCucumberTest` (with Cucumber's settings) and `LoginSteps`. This handout removes **repetition**: from the Gherkin (outlines, backgrounds, rules) and from the Java (hooks). At the end you add a **second feature**, `sorting.feature`, and see how two step classes share one browser.

**Which version of each file?** Every complete file in this handout is labelled. `login.feature` changes twice (3.1 and 3.2); the version at the end of **3.2** is the one you keep. `LoginSteps` changes twice (3.3 A and 3.3 B); the version at the end of **3.3 B** is the one you keep.

**Practice site:** Swag Labs, `https://www.saucedemo.com`, same locators as Handout 2. New in 3.3: the sort menu `[data-test='product-sort-container']` and the product names `[data-test='inventory-item-name']`.

**To run everything:** the green ▷ next to `RunCucumberTest`, or `mvn test -Dtest=RunCucumberTest`. **To run one feature** from VS Code's terminal:

```bash
mvn test -Dtest=RunCucumberTest -Dcucumber.features=src/test/resources/features/login.feature
```

---

## 3.1 Scenario Outline and Examples

### Definition

A **Scenario Outline** is a template for several scenarios that have the **same steps** but **different data**. Instead of real values, its steps contain **placeholders** in angle brackets, such as `<username>`. Below the outline, an **Examples** table gives one row of values per scenario; the table's header row names the placeholders. Cucumber runs the outline **once per row**, putting that row's values into the placeholders. Use an outline when only the data changes; when the behaviour is different, write separate scenarios.

### Key terms

| Term | Meaning |
|---|---|
| **`Scenario Outline:`** | A scenario template with placeholders (also written `Scenario Template:`) |
| **Placeholder** | A name in angle brackets, e.g. `<username>`, replaced by a value from the table |
| **`Examples:`** | The table of values; the first row is the header (also written `Scenarios:`) |
| **Example row** | One row of values = one scenario in the results |

### Key ideas

- Step definitions **don't change**: by the time Cucumber matches a step, `<username>` has already been replaced by real text.
- A placeholder must match a column header **exactly** (spelling, capitals, spaces).
- Put a placeholder in the outline's **title** too, so every row gets a readable name in the results.
- **One outline per kind of outcome.** Users who get in all see the Products page: one outline. Users who are refused all see an error: a second outline. The logout stays a separate scenario.

### Worked example: two outlines in `login.feature`

Swag Labs has **several** users who can log in, and **several** ways to be refused. Writing a scenario for each would mean copying the same three steps again and again.

**Step 1: More than one user can log in.** `standard_user`, `problem_user`, `performance_glitch_user` and `visual_user` all reach the Products page. Turn "Valid user logs in" into an outline; the username becomes a placeholder.

```gherkin
  Scenario Outline: <username> logs in
    Given I am on the login page
    When I log in with username "<username>" and password "secret_sauce"
    Then I should see the "Products" page

    Examples:
      | username                |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |
      | visual_user             |
```

**Step 2: Replace the two "refused" scenarios with one outline.** The username, password and error message all change, so all three become placeholders. A `reason` column gives each row a readable name.

```gherkin
  Scenario Outline: Login is refused when <reason>
    Given I am on the login page
    When I log in with username "<username>" and password "<password>"
    Then I should see the error "<error>"
```

**Step 3: Add the Examples table: one row per case.** An **empty cell** gives an empty value (`""`), which is how we test the "required" messages from the Handout 1 example map.

```gherkin
    Examples:
      | reason                  | username        | password     | error                                                                     |
      | the user is locked out  | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | the password is wrong   | standard_user   | wrong_sauce  | Epic sadface: Username and password do not match any user in this service |
      | the username is missing |                 | secret_sauce | Epic sadface: Username is required                                        |
      | the password is missing | standard_user   |              | Epic sadface: Password is required                                        |
```

**Step 4: Run it.** No Java changes: both outlines use the same step definitions as in Handout 2. (`performance_glitch_user` is slow, but the 10-second wait in `iShouldSeeThePage` covers it.)

**Complete file: `login.feature`, version 3.1 (outlines)**

```gherkin
# src/test/resources/features/login.feature   (version 3.1: outlines)
Feature: Log in to Swag Labs
  Shoppers must log in before they can see the products.
  Only known, unlocked users with the shared password get in.

  Scenario Outline: <username> logs in
    Given I am on the login page
    When I log in with username "<username>" and password "secret_sauce"
    Then I should see the "Products" page

    Examples:
      | username                |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |
      | visual_user             |

  Scenario Outline: Login is refused when <reason>
    Given I am on the login page
    When I log in with username "<username>" and password "<password>"
    Then I should see the error "<error>"

    Examples:
      | reason                  | username        | password     | error                                                                     |
      | the user is locked out  | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | the password is wrong   | standard_user   | wrong_sauce  | Epic sadface: Username and password do not match any user in this service |
      | the username is missing |                 | secret_sauce | Epic sadface: Username is required                                        |
      | the password is missing | standard_user   |              | Epic sadface: Password is required                                        |

  Scenario: Logged-in user logs out
    Given I am on the login page
    And I have logged in with username "standard_user" and password "secret_sauce"
    When I log out
    Then I should be back on the login page
```

### Checkpoint

Each outline becomes **one scenario per row**, named from that row:

```text
Scenario Outline: problem_user logs in                     # classpath:features/login.feature:14
  ✔ Given I am on the login page
  ✔ When I log in with username "problem_user" and password "secret_sauce"
  ✔ Then I should see the "Products" page
...
Scenario Outline: Login is refused when the username is missing   # classpath:features/login.feature:27
  ✔ Given I am on the login page
  ✔ When I log in with username "" and password "secret_sauce"
  ✔ Then I should see the error "Epic sadface: Username is required"
...
9 scenarios (9 passed)
28 steps (28 passed)
```

9 scenarios = 4 rows + 4 rows + 1 logout. The line number points to the **row** that produced the scenario.

### Your turn

1. Add `error_user` to the first Examples table. Does it get in? Run it to find out.
2. Introduce a typo: change `<username>` to `<usrname>` in the `When` step of the refused outline only. Run it: what text does the step receive? Fix it.
3. Why would it be a bad idea to merge the two outlines into one, with an extra column saying whether to expect the Products page or an error?

### Common errors

| You see | Why | Fix |
|---|---|---|
| The step receives the literal text `<usrname>` | The placeholder doesn't match any column header | Same spelling, capitals and spaces as the header |
| The outline runs 0 times | `Examples:` has a header row but no value rows | Add rows |
| Error "inconsistent cell count" | A row has a different number of `\|` than the header | Every row needs the same columns |
| One huge outline mixing outcomes | Different behaviours forced into one template | One outline per kind of outcome |

---

## 3.2 Background and Rule

### Definition

A **Background** is a list of `Given` steps that Cucumber runs **before every scenario** in the same feature, so the same setup isn't repeated in every scenario. A **Rule** groups the scenarios that illustrate **one business rule**, exactly like a blue card from Example Mapping; it has a title and may have its own Background that applies only to the scenarios inside it. Both make feature files shorter and easier to read: the Background shows the common starting point, and Rules show which acceptance criterion each scenario belongs to.

### Key terms

| Term | Meaning |
|---|---|
| **`Background:`** | `Given` steps that run before each scenario of the feature (or rule) |
| **`Rule:`** | A business rule with a title; contains the scenarios that illustrate it |
| **Rule Background** | A Background inside a Rule; it runs only for that rule's scenarios |

### Key ideas

- A Background runs **once per scenario**, not once per feature. Every scenario still starts fresh.
- Keep Backgrounds **short** (one to three steps) and only for context **every** scenario needs.
- A Background goes **before the first scenario**, and a feature (or rule) can have only one.

### Worked example: a Background and Rules in `login.feature`

**Step 1: Spot the repetition.** Every scenario starts with `Given I am on the login page`.

**Step 2: Move it into a Background**, and delete it from each scenario. In the logout scenario, the first remaining step changes from `And` to `Given`.

```gherkin
Feature: Log in to Swag Labs
  Shoppers must log in before they can see the products.
  Only known, unlocked users with the shared password get in.

  Background:
    Given I am on the login page

  Scenario Outline: <username> logs in
    When I log in with username "<username>" and password "secret_sauce"
    Then I should see the "Products" page
    ...
```

**Step 3: Group the scenarios by Rule**, one per acceptance criterion from Handout 1 (SL-101 and SL-102). The Background stays at feature level, so it applies to every rule.

```gherkin
  Rule: Known, unlocked users see the products

    Scenario Outline: <username> logs in
      ...

  Rule: Everyone else is refused with a message

    Scenario Outline: Login is refused when <reason>
      ...

  Rule: A logged-in user can log out

    Scenario: Logged-in user logs out
      ...
```

**Complete file: `login.feature`, version 3.2 (Background and Rules). Keep this version.**

```gherkin
# src/test/resources/features/login.feature   (version 3.2: Background and Rules, final)
Feature: Log in to Swag Labs
  Shoppers must log in before they can see the products.
  Only known, unlocked users with the shared password get in.

  Background:
    Given I am on the login page

  Rule: Known, unlocked users see the products

    Scenario Outline: <username> logs in
      When I log in with username "<username>" and password "secret_sauce"
      Then I should see the "Products" page

      Examples:
        | username                |
        | standard_user           |
        | problem_user            |
        | performance_glitch_user |
        | visual_user             |

  Rule: Everyone else is refused with a message

    Scenario Outline: Login is refused when <reason>
      When I log in with username "<username>" and password "<password>"
      Then I should see the error "<error>"

      Examples:
        | reason                  | username        | password     | error                                                                     |
        | the user is locked out  | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
        | the password is wrong   | standard_user   | wrong_sauce  | Epic sadface: Username and password do not match any user in this service |
        | the username is missing |                 | secret_sauce | Epic sadface: Username is required                                        |
        | the password is missing | standard_user   |              | Epic sadface: Password is required                                        |

  Rule: A logged-in user can log out

    Scenario: Logged-in user logs out
      Given I have logged in with username "standard_user" and password "secret_sauce"
      When I log out
      Then I should be back on the login page
```

### Checkpoint

Run `login.feature`. The Background step is shown before **every** scenario:

```text
Background:                                       # classpath:features/login.feature:6
  ✔ Given I am on the login page

Scenario Outline: standard_user logs in
  ✔ When I log in with username "standard_user" and password "secret_sauce"
  ✔ Then I should see the "Products" page
...
9 scenarios (9 passed)
28 steps (28 passed)
```

28 steps = 9 Background steps (one per scenario) + 19 scenario steps. The file is shorter, but the run does exactly the same work.

### Your turn

1. Make the Background fail: change its step text to `Given I am on the logon page`. Run it: what happens to each scenario? Change it back.
2. Under which Rule would a new scenario "Locked-out user cannot log in with any password" go? Write it.
3. Put the Background **after** the first Rule and run. Read the error, then move it back.

### Common errors

| You see | Why | Fix |
|---|---|---|
| Parse error near `Background:` | The Background is after a scenario or rule, or there are two at the same level | One Background, before the first scenario or rule |
| Every scenario fails at the same first step | The Background step failed | Fix the Background; the scenario steps were only skipped |
| The logout scenario reads `And I have logged in ...` as its first step | Leftover `And` from before the Background | The first step of a scenario is `Given` |
| `When`/`Then` steps in a Background | The Background has become a hidden test | Only `Given` context in a Background |

---

## 3.3 Hooks

### Definition

**Hooks** are methods that Cucumber runs **automatically** around every scenario: a method marked **`@Before`** runs before each scenario (even before the Background), and one marked **`@After`** runs after each scenario, **whether it passed or failed**. They are Cucumber's version of JUnit's `@BeforeEach` and `@AfterEach`. Hooks are for **technical** setup and clean-up that readers of the feature file don't need to see: opening and closing the browser, or saving a screenshot when a scenario fails. They live in the glue package, like step definitions. An `@After` hook can take a `Scenario` parameter to find out whether the scenario failed and to **attach** a screenshot to the results.

### Key terms

| Annotation / object | Meaning |
|---|---|
| `@Before` | Runs before every scenario |
| `@After` | Runs after every scenario, pass or fail |
| `@BeforeStep` / `@AfterStep` | Run around every step (rarely needed) |
| `order = ...` | Sets the order when there are several hooks. `@Before`: low numbers first. `@After`: **high numbers first**. |
| `@Before("@tag")` | A **tagged hook**: runs only for scenarios with that tag |
| `Scenario` | Information about the running scenario: `getName()`, `isFailed()`, `attach(...)`, `log(...)` |

### Key ideas

- **The problem hooks solve:** in Handout 2, the first step opened the browser and each `Then` step closed it. If a step failed **before** the `Then`, the browser stayed open. An `@After` hook **always** runs.
- With hooks, opening and closing the browser **leaves the steps**: `@Before` opens it, `@After` closes it.
- **Two step classes, one browser:** when a second feature gets its own step class, both classes need the **same** `driver`. A small parent class, `BaseSteps`, holds it, just as `BaseTest` did for the Selenium tests.

### Worked example A: hooks in `LoginSteps`

**Step 1: A `@Before` hook opens the browser.** Add it to `LoginSteps`, and remove `driver = new ChromeDriver();` from `iAmOnTheLoginPage()`.

```java
@Before
public void openBrowser() {
    driver = new ChromeDriver();
}

@Given("I am on the login page")
public void iAmOnTheLoginPage() {
    driver.get("https://www.saucedemo.com/");
}
```

**Step 2: An `@After` hook closes it,** after every scenario, passed or failed.

```java
@After(order = 0)
public void closeBrowser() {
    driver.quit();
}
```

**Step 3: A second `@After` hook takes a screenshot if the scenario failed.** It has the **higher** order, so it runs **first**, while the browser is still open.

```java
@After(order = 1)
public void screenshotIfFailed(Scenario scenario) {
    if (scenario.isFailed()) {
        byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", scenario.getName());
    }
}
```

**Step 4: The three `Then` steps become plain checks again:** delete the `driver.quit();` line from each. For example:

```java
@Then("I should see the error {string}")
public void iShouldSeeTheError(String expectedError) {
    String actualError = driver.findElement(By.cssSelector("[data-test='error']")).getText();
    assertEquals(expectedError, actualError);
}
```

Run `login.feature`: still 9 scenarios passing, and every browser closes, even when you break a scenario on purpose.

### Worked example B: a second feature, and sharing the browser

**Step 1: A second feature for SL-104 (sort products).** This is the `sorting.feature` you wrote in Handout 1, rewritten with what you learned in 3.1 and 3.2: the two login steps go into a **Background**, and the sorts become an **outline** with **two Examples tables**, one per kind of sort.

```gherkin
# src/test/resources/features/sorting.feature
Feature: Sort the products
  Shoppers can sort the products by name or by price.

  Background:
    Given I am on the login page
    And I have logged in with username "standard_user" and password "secret_sauce"

  Scenario Outline: Sorting by <order>
    When I sort the products by "<order>"
    Then the first product should be "<first>"

    Examples: Sorting by name
      | order         | first                             |
      | Name (A to Z) | Sauce Labs Backpack               |
      | Name (Z to A) | Test.allTheThings() T-Shirt (Red) |

    Examples: Sorting by price
      | order               | first                    |
      | Price (low to high) | Sauce Labs Onesie        |
      | Price (high to low) | Sauce Labs Fleece Jacket |
```

The two Background steps are **already defined** in `LoginSteps`: Cucumber matches step text across **all** classes in the glue package. Only the `When` and `Then` steps need a new class, `SortSteps`.

**Step 2: The problem.** `SortSteps` needs the browser that `LoginSteps` logged in with, but the `driver` field is private to `LoginSteps`, and Cucumber creates each step class **separately**. `SortSteps` can't see it.

**Step 3: Move the shared `driver` into a parent class, `BaseSteps`.** `static` means every class that extends it shares the **same** `driver`.

```java
public class BaseSteps {
    protected static WebDriver driver;
}
```

**Step 4: Move the hooks into their own class, `Hooks`.** `Hooks` **extends `BaseSteps`** so that the browser it opens in `@Before` is the **same shared `driver`** the step classes use, and the one it closes in `@After`. Delete the `driver` field and the three hooks from `LoginSteps`.

**Step 5: Both step classes extend `BaseSteps`** and simply use `driver`. The sort menu is a `<select>`, so `SortSteps` uses `Select` (Selenium Handout 3), after waiting for the Products page to load.

```java
public class LoginSteps extends BaseSteps { ... }

public class SortSteps extends BaseSteps {

    @When("I sort the products by {string}")
    public void iSortTheProductsBy(String order) {
        WebElement sortMenu = new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(
                        By.cssSelector("[data-test='product-sort-container']")));
        new Select(sortMenu).selectByVisibleText(order);
    }
    ...
}
```

**Complete code: the final step classes for Handout 3. Keep these versions.**

```java
// src/test/java/com/qea/selenium/steps/BaseSteps.java
package com.qea.selenium.steps;

import org.openqa.selenium.WebDriver;

/** Parent of every step class and of Hooks: holds the one browser they all share. */
public class BaseSteps {

    protected static WebDriver driver;
}
```

```java
// src/test/java/com/qea/selenium/steps/Hooks.java
package com.qea.selenium.steps;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.chrome.ChromeDriver;

/** Opens and closes the shared browser around every scenario, with a screenshot when one fails. */
public class Hooks extends BaseSteps {

    @Before
    public void openBrowser() {
        driver = new ChromeDriver();
    }

    // @After hooks run from the highest order to the lowest:
    // 1 (screenshot) runs while the browser is still open; 0 (close) runs last.
    @After(order = 1)
    public void screenshotIfFailed(Scenario scenario) {
        if (scenario.isFailed()) {
            byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            scenario.attach(png, "image/png", scenario.getName());
        }
    }

    @After(order = 0)
    public void closeBrowser() {
        driver.quit();
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/LoginSteps.java   (hooks version, final for Handout 3)
package com.qea.selenium.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for login.feature. The browser comes from BaseSteps; Hooks opens and closes it. */
public class LoginSteps extends BaseSteps {

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        driver.get("https://www.saucedemo.com/");
    }

    @When("I log in with username {string} and password {string}")
    public void iLogInWith(String username, String password) {
        driver.findElement(By.id("user-name")).sendKeys(username);
        driver.findElement(By.id("password")).sendKeys(password);
        driver.findElement(By.id("login-button")).click();
    }

    @Given("I have logged in with username {string} and password {string}")
    public void iHaveLoggedInWith(String username, String password) {
        iLogInWith(username, password);
    }

    @When("I log out")
    public void iLogOut() {
        driver.findElement(By.id("react-burger-menu-btn")).click();
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.elementToBeClickable(By.id("logout_sidebar_link")))
                .click();
    }

    @Then("I should see the {string} page")
    public void iShouldSeeThePage(String expectedTitle) {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        String actualTitle = wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.cssSelector("[data-test='title']"))).getText();
        assertEquals(expectedTitle, actualTitle);
    }

    @Then("I should see the error {string}")
    public void iShouldSeeTheError(String expectedError) {
        String actualError = driver.findElement(By.cssSelector("[data-test='error']")).getText();
        assertEquals(expectedError, actualError);
    }

    @Then("I should be back on the login page")
    public void iShouldBeBackOnTheLoginPage() {
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(By.id("login-button")));
        assertEquals("https://www.saucedemo.com/", driver.getCurrentUrl());
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/SortSteps.java
package com.qea.selenium.steps;

import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for sorting.feature. The login steps come from LoginSteps. */
public class SortSteps extends BaseSteps {

    @When("I sort the products by {string}")
    public void iSortTheProductsBy(String order) {
        WebElement sortMenu = new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(
                        By.cssSelector("[data-test='product-sort-container']")));
        new Select(sortMenu).selectByVisibleText(order);
    }

    @Then("the first product should be {string}")
    public void theFirstProductShouldBe(String expectedName) {
        // findElement returns the FIRST matching element: the first product on the page
        String firstName = driver.findElement(By.cssSelector("[data-test='inventory-item-name']")).getText();
        assertEquals(expectedName, firstName);
    }
}
```

### Checkpoint

1. Run `RunCucumberTest`: **13 scenarios (13 passed)** (9 login, 4 sorting) and **44 steps (44 passed)**. A Chrome window opens and closes **for each scenario**, now handled by `Hooks`.
2. Break one example on purpose (e.g. change `Sauce Labs Onesie` to `Sauce Labs Bolt T-Shirt` in `sorting.feature`) and run again. The scenario fails, the browser **still closes**, and a screenshot is attached to the failed scenario; you will **see** it in the HTML report in Cucumber Handout 4. Undo the change.

### Your turn

1. Add a `Scenario` parameter to `closeBrowser` and the line `scenario.log("Finished: " + scenario.getName());`. Run and find the logged lines in the output.
2. Swap the `order` numbers of the two `@After` hooks, break a scenario, and run it. Why does taking the screenshot fail now? Swap them back.
3. Write a **tagged hook** `@Before(value = "@maximized", order = 1)` in `Hooks` that calls `driver.manage().window().maximize()`. Put `@maximized` on the line above one scenario and watch it run in a maximised window. (Tags are covered fully in Handout 4.)
4. Why does `Hooks` extend `BaseSteps`? What would happen if it had its own `driver` field instead?

### Common errors

| You see | Why | Fix |
|---|---|---|
| Two browsers per scenario | A step still creates `new ChromeDriver()` | Only the `@Before` hook opens the browser |
| `NullPointerException` on `driver` in `SortSteps` | The class doesn't extend `BaseSteps`, or `LoginSteps` still has its own `driver` field | Every step class extends `BaseSteps`; only `BaseSteps` declares `driver` |
| `NoSuchSessionException` | A `Then` step still calls `driver.quit()` | Only the `@After` hook closes it |
| `NoSuchElementException: Cannot locate option with text` | The order text in `sorting.feature` doesn't match the menu exactly | Copy the text from the menu: `Price (low to high)` |
| No screenshot on failure | The closing hook ran first (wrong `order`) | The screenshot hook gets the **higher** order |
| Hooks never run | `Hooks` is not in the glue package | Put it in `com.qea.selenium.steps` |

---

**End of Cucumber Handout 3.** Your features use outlines, backgrounds and rules; hooks open and close the browser and capture a screenshot on failure; and two step classes share one browser through `BaseSteps`. **Next:** Cucumber Handout 4, Running and Reporting: tags, JUnit and Maven integration, and reports.
