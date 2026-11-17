# Cucumber In-Class Handout 3: Reusable Scenarios

**Topics:** 3.1 Scenario Outline and Examples · 3.2 Background and Rule · 3.3 Hooks

**How to use this handout:** the same layout as before. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Cucumber Handouts 1–2:** the three feature files, `RunCucumberTest` (with Cucumber's settings), and the step classes `BaseSteps`, `LoginSteps`, `CartSteps` and `SortSteps`. This handout removes **repetition**: from the Gherkin (outlines, backgrounds, rules) and from the Java (hooks).

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
- An outline can have **several** `Examples:` tables, each with its own title, to group cases.
- **One outline per kind of outcome.** Successful and refused logins have different `Then` steps, so they are two outlines, not one big outline with an "expected result" column.

### Worked example: two login outlines, one for success and one for refusal

`login.feature` has two "refused" scenarios that differ only in their data, and Handout 1 asked for more (empty username, empty password). Swag Labs also has **more than one user who can log in**. Each new case would be another copy of the same steps.

**Step 1: Successful logins as one outline.** `standard_user` and `performance_glitch_user` both reach the Products page, so they share one outline. Replace the "Standard user logs in" scenario with:

```gherkin
  Scenario Outline: <username> logs in successfully
    Given I am on the Swag Labs login page
    When I log in as "<username>" with password "secret_sauce"
    Then I should see the "Products" page

    Examples:
      | username                |
      | standard_user           |
      | performance_glitch_user |
```

`performance_glitch_user` is deliberately **slow**: the Products page appears several seconds after the click. The scenario still passes because `InventoryPage.title()` waits up to 10 seconds (Selenium Handout 3).

**Step 2: Refused logins as a second outline.** Their outcome (an error message) is different, so they get their own outline. The values become placeholders.

```gherkin
  Scenario Outline: Login is refused when <reason>
    Given I am on the Swag Labs login page
    When I log in as "<username>" with password "<password>"
    Then I should see the login error "<error>"
```

**Step 3: Add the Examples table: one row per case.** An empty cell gives an empty value (`""`).

```gherkin
    Examples:
      | reason                 | username        | password     | error                                                                     |
      | the user is locked out | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | the password is wrong  | standard_user   | wrong_sauce  | Epic sadface: Username and password do not match any user in this service |
      | the username is empty  |                 | secret_sauce | Epic sadface: Username is required                                        |
      | the password is empty  | standard_user   |              | Epic sadface: Password is required                                        |
```

**Step 4: Two Examples tables** in `sorting.feature`, grouping the sort orders.

```gherkin
Feature: Sorting products
  Shoppers can sort the product list by name or by price.

  Scenario Outline: Sorting by "<order>" puts <first product> first
    Given I am logged in as "standard_user"
    When I sort the products by "<order>"
    Then the first product should be "<first product>"

    Examples: Sorting by name
      | order         | first product                     |
      | Name (A to Z) | Sauce Labs Backpack               |
      | Name (Z to A) | Test.allTheThings() T-Shirt (Red) |

    Examples: Sorting by price
      | order               | first product            |
      | Price (low to high) | Sauce Labs Onesie        |
      | Price (high to low) | Sauce Labs Fleece Jacket |
```

**Complete file**

```gherkin
# src/test/resources/features/login.feature
Feature: Log in to Swag Labs
  Customers must log in before they can browse products.
  Only known, unlocked users with the shared password get in.

  Scenario Outline: <username> logs in successfully
    Given I am on the Swag Labs login page
    When I log in as "<username>" with password "secret_sauce"
    Then I should see the "Products" page

    Examples:
      | username                |
      | standard_user           |
      | performance_glitch_user |

  Scenario Outline: Login is refused when <reason>
    Given I am on the Swag Labs login page
    When I log in as "<username>" with password "<password>"
    Then I should see the login error "<error>"

    Examples:
      | reason                 | username        | password     | error                                                                     |
      | the user is locked out | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | the password is wrong  | standard_user   | wrong_sauce  | Epic sadface: Username and password do not match any user in this service |
      | the username is empty  |                 | secret_sauce | Epic sadface: Username is required                                        |
      | the password is empty  | standard_user   |              | Epic sadface: Password is required                                        |
```

### Checkpoint

Run `login.feature`. The two outlines become **six** scenarios (2 successful, 4 refused), each named from its row. The second one takes a few seconds longer:

```text
Scenario Outline: standard_user logs in successfully             # classpath:features/login.feature:13
  ✔ Given I am on the Swag Labs login page
  ✔ When I log in as "standard_user" with password "secret_sauce"
  ✔ Then I should see the "Products" page
...
Scenario Outline: Login is refused when the user is locked out   # classpath:features/login.feature:23
  ✔ Given I am on the Swag Labs login page
  ✔ When I log in as "locked_out_user" with password "secret_sauce"
  ✔ Then I should see the login error "Epic sadface: Sorry, this user has been locked out."
...
6 scenarios (6 passed)
18 steps (18 passed)
```

Run `sorting.feature`: **4 scenarios (4 passed)**, two from each Examples table.

### Your turn

1. Add `visual_user` to the **successful** outline and `nobody` (password `secret_sauce`) to the **refused** outline. For `nobody`, what is the error message? Run it to find out, then complete the row.
2. Why would one outline with an extra `expected result` column (Products page **or** an error) be a bad idea? What would its `Then` step definition have to contain?
3. Introduce a typo: change `<username>` to `<usrname>` in the `When` step only. Run it: what text does the step receive? Fix it.
4. Add an Examples row to `sorting.feature` that you **know** is wrong (e.g. `Name (A to Z)` → `Sauce Labs Onesie`). Run it: do the other rows still pass? Remove the wrong row.

### Common errors

| You see | Why | Fix |
|---|---|---|
| The step receives the literal text `<usrname>` | The placeholder doesn't match any column header | Same spelling, capitals and spaces as the header |
| The outline runs 0 times | `Examples:` has a header row but no value rows | Add rows |
| Error "inconsistent cell count" | A row has a different number of `\|` than the header | Every row needs the same columns |
| One huge outline with many columns | Different behaviours forced into one template | Split into separate scenarios or outlines |

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

### Worked example: `cart.feature` with a Background, `login.feature` with Rules

**Step 1: Spot the repetition.** All three cart scenarios start with `Given I am logged in as "standard_user"`.

**Step 2: Move it into a Background**, and remove it from the first scenario.

```gherkin
Feature: Shopping cart
  Shoppers collect products in a cart before checking out.
  The badge on the cart icon shows how many products are in the cart.

  Background:
    Given I am logged in as "standard_user"

  Scenario: Adding products shows the count on the cart badge
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show 2
```

**Step 3: Remove it from the other two scenarios as well.** Their first remaining step becomes `Given`.

```gherkin
  Scenario: Removing the only product hides the badge
    Given I have added "Sauce Labs Onesie" to the cart
    When I remove "Sauce Labs Onesie" from the cart
    Then the cart badge should not be shown

  Scenario: The cart lists the products that were added
    Given I have added these products to the cart:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
    When I open the cart
    Then the cart should contain exactly:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
```

**Step 4: Rules in `login.feature`.** Group the scenarios by the acceptance criterion they illustrate (SL-101). Here both rules share a Background at the feature level.

```gherkin
Feature: Log in to Swag Labs

  Background:
    Given I am on the Swag Labs login page

  Rule: Known, unlocked users get in with the shared password

    Scenario Outline: <username> logs in successfully
      When I log in as "<username>" with password "secret_sauce"
      Then I should see the "Products" page

      Examples:
        | username                |
        | standard_user           |
        | performance_glitch_user |

  Rule: Everyone else is refused with a clear error

    Scenario Outline: Login is refused when <reason>
      When I log in as "<username>" with password "<password>"
      Then I should see the login error "<error>"

      Examples:
        | reason                 | username        | password     | error                                               |
        | the user is locked out | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out. |
        | the username is empty  |                 | secret_sauce | Epic sadface: Username is required                  |
```

**Complete file** (`cart.feature`)

```gherkin
# src/test/resources/features/cart.feature
Feature: Shopping cart
  Shoppers collect products in a cart before checking out.
  The badge on the cart icon shows how many products are in the cart.

  Background:
    Given I am logged in as "standard_user"

  Scenario: Adding products shows the count on the cart badge
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart badge should show 2

  Scenario: Removing the only product hides the badge
    Given I have added "Sauce Labs Onesie" to the cart
    When I remove "Sauce Labs Onesie" from the cart
    Then the cart badge should not be shown

  Scenario: The cart lists the products that were added
    Given I have added these products to the cart:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
    When I open the cart
    Then the cart should contain exactly:
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
```

### Checkpoint

Run `cart.feature`. The Background step is shown before **every** scenario, and the browser still logs in three times:

```text
Background:                                   # classpath:features/cart.feature:6
  ✔ Given I am logged in as "standard_user"

Scenario: Adding products shows the count on the cart badge
  ✔ When I add "Sauce Labs Backpack" to the cart
  ...
3 scenarios (3 passed)
12 steps (12 passed)
```

12 steps = 3 Background steps (one per scenario) + 9 scenario steps.

### Your turn

1. Add the Rules version of `login.feature` (step 4), but with all four rows from 3.1 in the refused Examples table. Run it: how many scenarios pass?
2. Make the Background fail: log in as `locked_out_user` in `cart.feature`. Run it: what happens to each scenario's own steps? Change it back.
3. Give `sorting.feature` a Background. Which step moves into it?

### Common errors

| You see | Why | Fix |
|---|---|---|
| Parse error near `Background:` | The Background is after a scenario, or there are two at the same level | One Background, before the first scenario |
| Every scenario fails at the same first step | The Background step failed | Fix the Background; the scenario steps were only skipped |
| A scenario needs a different starting point | It doesn't belong under this Background | Move it to another feature or rule |
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

- **The problem hooks solve:** in Handout 2, the first step opened the browser and the `Then` step closed it. If a step failed **before** the `Then`, the browser stayed open, and every step had to remember its part. An `@After` hook **always** runs.
- With hooks, the **browser leaves the steps**: `@Before` opens it, `@After` closes it, and the steps only use `driver`, just like tests that extend `BaseTest`.
- Take the **screenshot before closing the browser**: give the screenshot hook a **higher** `order` than the closing hook.
- Keep business context (such as logging in) in `Given` steps or a Background, where readers can see it.

### Worked example: a `Hooks` class

**Step 1: Create `Hooks`** in the steps package (the glue). A `@Before` hook opens the browser.

`Hooks` **extends `BaseSteps`** for the same reason the step classes do: the browser it opens must be the **same** `driver` the steps use. Extending `BaseSteps` gives it that shared `driver`, plus `openBrowser()` and `closeBrowser()`. (Without it, `Hooks` would open a browser of its own that the steps never see.)

```java
public class Hooks extends BaseSteps {

    @Before
    public void startBrowser() {
        openBrowser();
    }
}
```

**Step 2: An `@After` hook closes it,** after every scenario, passed or failed.

```java
@After(order = 0)
public void stopBrowser() {
    closeBrowser();
}
```

**Step 3: A second `@After` hook takes a screenshot if the scenario failed.** It has the **higher** order, so it runs **first**, while the browser is still open. `scenario.attach(...)` adds the picture to the scenario's results.

```java
@After(order = 1)
public void screenshotIfFailed(Scenario scenario) {
    if (scenario.isFailed()) {
        byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", scenario.getName());
    }
}
```

**Step 4: The steps stop opening and closing the browser.** In `LoginSteps`, delete the two `openBrowser();` lines. In every `Then` step, go back to a plain assertion:

```java
@Then("I should see the {string} page")
public void iShouldSeeThePage(String expectedTitle) {
    assertEquals(expectedTitle, new InventoryPage(driver).title());
}
```

Do the same for every `Then` step in `CartSteps` and `SortSteps`. (Complete code below.)

**Complete code**

```java
// src/test/java/com/qea/selenium/steps/Hooks.java
package com.qea.selenium.steps;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

/** Opens and closes the browser around every scenario, with a screenshot when one fails. */
public class Hooks extends BaseSteps {

    @Before
    public void startBrowser() {
        openBrowser();
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
    public void stopBrowser() {
        closeBrowser();
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/LoginSteps.java   (hooks version)
package com.qea.selenium.steps;

import com.qea.selenium.pages.InventoryPage;
import com.qea.selenium.pages.LoginPage;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class LoginSteps extends BaseSteps {

    @Given("I am on the Swag Labs login page")
    public void iAmOnTheLoginPage() {
        new LoginPage(driver).open();
    }

    @Given("I am logged in as {string}")
    public void iAmLoggedInAs(String username) {
        new LoginPage(driver).open().loginAs(username, "secret_sauce");
    }

    @When("I log in as {string} with password {string}")
    public void iLogInAs(String username, String password) {
        new LoginPage(driver).loginExpectingError(username, password);
    }

    @Then("I should see the {string} page")
    public void iShouldSeeThePage(String expectedTitle) {
        assertEquals(expectedTitle, new InventoryPage(driver).title());
    }

    @Then("I should see the login error {string}")
    public void iShouldSeeTheLoginError(String expectedMessage) {
        assertEquals(expectedMessage, new LoginPage(driver).errorMessage());
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/CartSteps.java   (hooks version)
package com.qea.selenium.steps;

import com.qea.selenium.pages.CartPage;
import com.qea.selenium.pages.InventoryPage;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CartSteps extends BaseSteps {

    @When("I add {string} to the cart")
    public void iAddToTheCart(String product) {
        new InventoryPage(driver).addProductToCart(product);
    }

    @Given("I have added {string} to the cart")
    public void iHaveAddedToTheCart(String product) {
        iAddToTheCart(product);
    }

    @Given("I have added these products to the cart:")
    public void iHaveAddedTheseProducts(List<String> products) {
        for (String product : products) {
            iAddToTheCart(product);
        }
    }

    @When("I remove {string} from the cart")
    public void iRemoveFromTheCart(String product) {
        new InventoryPage(driver).removeProductFromCart(product);
    }

    @When("I open the cart")
    public void iOpenTheCart() {
        new InventoryPage(driver).openCart();
    }

    @Then("the cart badge should show {int}")
    public void theCartBadgeShouldShow(int expected) {
        assertEquals(expected, new InventoryPage(driver).cartCount());
    }

    @Then("the cart badge should not be shown")
    public void theCartBadgeShouldNotBeShown() {
        assertEquals(0, new InventoryPage(driver).cartCount());
    }

    @Then("the cart should contain exactly:")
    public void theCartShouldContainExactly(List<String> expected) {
        assertEquals(expected, new CartPage(driver).itemNames());
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/SortSteps.java   (hooks version)
package com.qea.selenium.steps;

import com.qea.selenium.pages.InventoryPage;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SortSteps extends BaseSteps {

    @When("I sort the products by {string}")
    public void iSortTheProductsBy(String order) {
        new InventoryPage(driver).sortBy(order);
    }

    @Then("the first product should be {string}")
    public void theFirstProductShouldBe(String expected) {
        assertEquals(expected, new InventoryPage(driver).firstProductName());
    }
}
```

### Checkpoint

1. Run `RunCucumberTest`. Everything is still green, and a Chrome window opens and closes **for each scenario**, now handled by the hooks.
2. Break one example on purpose (e.g. `Sauce Labs Onesie` → `Sauce Labs Backpack` in a sorting row) and run again. The scenario fails, the browser **still closes**, and a screenshot is attached to the failed scenario; you will **see** it in the HTML report in Cucumber Handout 4. Undo the change.

### Your turn

1. Add a `Scenario` parameter to `stopBrowser` and the line `scenario.log("Finished: " + scenario.getName());`. Run one feature and find the logged lines in the output.
2. Swap the `order` numbers of the two `@After` hooks, break a scenario, and run it. Why does taking the screenshot fail now? Swap them back.
3. Write a **tagged hook** `@Before(value = "@maximized", order = 1)` that calls `driver.manage().window().maximize()`. Put `@maximized` on the line above one scenario (tags are covered fully in Handout 4) and watch that scenario run in a maximised window.

### Common errors

| You see | Why | Fix |
|---|---|---|
| Two browsers per scenario | A step still calls `openBrowser()` | Only the `@Before` hook opens the browser |
| `NoSuchSessionException` in a `Then` step | A step still calls `closeBrowser()` | Only the `@After` hook closes it |
| No screenshot on failure | The closing hook ran first (wrong `order`), or `isFailed()` not checked | The screenshot hook gets the **higher** order |
| Hooks never run | `Hooks` is not in the glue package | Put it in `com.qea.selenium.steps` |
| Business steps hidden in a hook | Readers of the feature can't see them | Keep logins etc. in `Given` steps or a Background |

---

**End of Cucumber Handout 3.** Your features use outlines, backgrounds and rules, and hooks open and close the browser and capture a screenshot when a scenario fails. **Next:** Cucumber Handout 4, Running and Reporting: tags, JUnit and Maven integration, and reports.
