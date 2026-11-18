# Cucumber Self-Study Handout 5: Putting It Together

**For self-study after Cucumber Handouts 1–4.** You keep working in the **same project**. In Handouts 2–3 the step definitions contained the Selenium code themselves (`driver.findElement(...)`). Here you **refactor** them to use **page objects** (Selenium Handout 5), and then add a third feature, the shopping cart, the way a real team would. There are **no new Cucumber features** in this handout; what is new is the **structure**.

**Practice site:** Swag Labs, `https://www.saucedemo.com` (password `secret_sauce`).

**What changes compared with Handouts 1–4**

| In Handouts 2–4 | In this handout |
|---|---|
| Steps call Selenium directly (`driver.findElement(By.id("user-name"))`) | Steps call **page objects**: `LoginPage`, `InventoryPage`, `CartPage` |
| Locators and waits are spread over the step classes | Locators and waits live in **one** page class per page |
| Two features: `login`, `sorting` | Three features: `cart.feature` is new |
| Two step classes | Three: `CartSteps` is new, and reuses the login steps |

**How to use it:** work through Parts 1–5 in order, running the scenarios after each part: they must stay green while you refactor. Then try the "Your turn" exercises. Compare your code with the complete code here when you get stuck.

---

## How the framework fits together

```text
 Feature files (what)        login.feature, sorting.feature, cart.feature
        │  each step matches
        ▼
 Step definitions (glue)     LoginSteps, SortSteps, CartSteps   ── extend BaseSteps (shared driver)
        │  call                                                    Hooks: open/close browser, screenshots
        ▼
 Page objects (how)          LoginPage, InventoryPage, CartPage  (locators + waits live here)
        │  use
        ▼
 Selenium WebDriver  ──>  chromedriver  ──>  Chrome  ──>  Swag Labs
```

Each layer changes for a different reason: **features** when requirements change, **steps** when wording changes, **page objects** when the web page changes. A changed button id is fixed in **one** page class, and no feature file or step changes.

**Project layout at the end of this handout** (NEW = created in this handout)

```text
src/test/
├── java/com/qea/selenium/
│   ├── RunCucumberTest.java                     from Handout 4
│   ├── pages/
│   │   ├── LoginPage.java                       NEW (based on Selenium Handout 5)
│   │   ├── InventoryPage.java                   NEW
│   │   └── CartPage.java                        NEW
│   └── steps/
│       ├── BaseSteps.java, Hooks.java           unchanged from Handout 3
│       ├── LoginSteps.java, SortSteps.java      refactored in Part 3
│       └── CartSteps.java                       NEW
└── resources/
    ├── junit-platform.properties                from Handout 4
    └── features/
        ├── login.feature, sorting.feature       unchanged from Handout 4
        └── cart.feature                         NEW
```

---

## Part 1: Where you start

You need the project as it was at the end of Cucumber Handout 4. Nothing in `pom.xml`, `junit-platform.properties` or `RunCucumberTest` changes in this handout. Check that your feature files match these **final versions** (`login.feature` version 3.2 from Handout 3, with the tags from Handout 4):

```gherkin
# src/test/resources/features/login.feature   (final: version 3.2 + tags from Handout 4)
@SL-101
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

    @wip
    Scenario: Account is locked after three wrong passwords
      When I log in 3 times with username "standard_user" and a wrong password
      Then I should see the error "Epic sadface: Your account is locked"

  @SL-102
  Rule: A logged-in user can log out

    @smoke
    Scenario: Logged-in user logs out
      Given I have logged in with username "standard_user" and password "secret_sauce"
      When I log out
      Then I should be back on the login page
```

```gherkin
# src/test/resources/features/sorting.feature   (final: Handout 3 + tags from Handout 4)
@SL-104
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

    @smoke
    Examples: Sorting by price
      | order               | first                    |
      | Price (low to high) | Sauce Labs Onesie        |
      | Price (high to low) | Sauce Labs Fleece Jacket |
```

Run `mvn test -Dtest=RunCucumberTest` before you change anything: **13 scenarios pass**. That is your safety net for the refactoring.

---

## Part 2: The page objects

A **page object** holds the locators and the waits for one page, and offers methods named after what a user does there (Selenium Handout 5). Create the package `com.qea.selenium.pages` under `src/test/java`.

`LoginPage` is the one from Selenium Handout 5, plus one method, `isShown()`, for the logout scenario.

```java
// src/test/java/com/qea/selenium/pages/LoginPage.java
package com.qea.selenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** The Swag Labs login page. */
public class LoginPage {

    private static final String URL = "https://www.saucedemo.com/";

    private final WebDriver driver;
    private final By username = By.id("user-name");
    private final By password = By.id("password");
    private final By loginButton = By.id("login-button");
    private final By errorMessage = By.cssSelector("[data-test='error']");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public LoginPage open() {
        driver.get(URL);
        return this;
    }

    /** A successful login: the user ends up on the products page. */
    public InventoryPage loginAs(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
        driver.findElement(loginButton).click();
        return new InventoryPage(driver);
    }

    /** A login that may fail: the user may stay on the login page. */
    public LoginPage loginExpectingError(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
        driver.findElement(loginButton).click();
        return this;
    }

    public String errorMessage() {
        return driver.findElement(errorMessage).getText();
    }

    /** Waits for the Login button, then checks that the browser is at the login page address. */
    public boolean isShown() {
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(loginButton));
        return driver.getCurrentUrl().equals(URL);
    }
}
```

`InventoryPage` is the products page. Its **constructor waits** until the products page has loaded, so every method can be used straight away. The logout and sort code moves here from the step classes.

```java
// src/test/java/com/qea/selenium/pages/InventoryPage.java
package com.qea.selenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

/** The Swag Labs products page. */
public class InventoryPage {

    private final WebDriver driver;
    private final WebDriverWait wait;
    private final By title = By.cssSelector("[data-test='title']");
    private final By menuButton = By.id("react-burger-menu-btn");
    private final By logoutLink = By.id("logout_sidebar_link");
    private final By sortMenu = By.cssSelector("[data-test='product-sort-container']");
    private final By productNames = By.cssSelector("[data-test='inventory-item-name']");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");
    private final By cartLink = By.cssSelector("[data-test='shopping-cart-link']");

    /** Waits until the products page is shown. */
    public InventoryPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.visibilityOfElementLocated(title));
    }

    public String title() {
        return driver.findElement(title).getText();
    }

    /** Opens the menu and clicks Logout once the menu has slid in. */
    public LoginPage logout() {
        driver.findElement(menuButton).click();
        wait.until(ExpectedConditions.elementToBeClickable(logoutLink)).click();
        return new LoginPage(driver);
    }

    /** Sorts by the visible text of the sort menu, e.g. "Price (low to high)". */
    public InventoryPage sortBy(String label) {
        new Select(driver.findElement(sortMenu)).selectByVisibleText(label);
        return this;
    }

    /** findElement returns the FIRST matching element: the first product on the page. */
    public String firstProductName() {
        return driver.findElement(productNames).getText();
    }

    /** "Sauce Labs Backpack" -> clicks the button with id "add-to-cart-sauce-labs-backpack". */
    public InventoryPage addProductToCart(String productName) {
        driver.findElement(By.id("add-to-cart-" + idPart(productName))).click();
        return this;
    }

    /** "Sauce Labs Onesie" -> clicks the button with id "remove-sauce-labs-onesie". */
    public InventoryPage removeProductFromCart(String productName) {
        driver.findElement(By.id("remove-" + idPart(productName))).click();
        return this;
    }

    /** 0 when the badge is not shown: an empty cart is a valid answer. */
    public int cartCount() {
        List<WebElement> badge = driver.findElements(cartBadge);
        return badge.isEmpty() ? 0 : Integer.parseInt(badge.get(0).getText());
    }

    public CartPage openCart() {
        driver.findElement(cartLink).click();
        return new CartPage(driver);
    }

    /** Swag Labs builds button ids from the product name in lower case, with spaces as dashes. */
    private static String idPart(String productName) {
        return productName.toLowerCase().replace(" ", "-");
    }
}
```

`CartPage` is needed in Part 4; create it now so all the pages are together.

```java
// src/test/java/com/qea/selenium/pages/CartPage.java
package com.qea.selenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

/** The Swag Labs cart page. */
public class CartPage {

    private final WebDriver driver;
    private final By itemNames = By.cssSelector("[data-test='inventory-item-name']");

    /** Waits until the browser is on the cart page. */
    public CartPage(WebDriver driver) {
        this.driver = driver;
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.urlContains("cart"));
    }

    public List<String> itemNames() {
        List<String> names = new ArrayList<>();
        for (WebElement item : driver.findElements(itemNames)) {
            names.add(item.getText());
        }
        return names;
    }
}
```

---

## Part 3: Refactor the step classes

`BaseSteps` and `Hooks` **do not change** (Cucumber Handout 3). The step classes become **thin**: each method is a line or two that calls a page object, plus an assertion in `Then` steps. The step **text** does not change, so the feature files don't change either.

Replace `LoginSteps` and `SortSteps` with the versions below, one class at a time, and run the scenarios after each: still **13 passed**.

Notice which login method each step uses: `When I log in with ...` is used for **good and bad** logins, so it calls `loginExpectingError`, which doesn't wait for the products page. `Given I have logged in with ...` is always a good login, so it calls `loginAs`, which does.

```java
// src/test/java/com/qea/selenium/steps/LoginSteps.java   (page-object version)
package com.qea.selenium.steps;

import com.qea.selenium.pages.InventoryPage;
import com.qea.selenium.pages.LoginPage;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Step definitions for login.feature; the login steps are also used by sorting.feature and cart.feature. */
public class LoginSteps extends BaseSteps {

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        new LoginPage(driver).open();
    }

    @When("I log in with username {string} and password {string}")
    public void iLogInWith(String username, String password) {
        new LoginPage(driver).loginExpectingError(username, password);
    }

    @Given("I have logged in with username {string} and password {string}")
    public void iHaveLoggedInWith(String username, String password) {
        new LoginPage(driver).loginAs(username, password);
    }

    @When("I log out")
    public void iLogOut() {
        new InventoryPage(driver).logout();
    }

    @Then("I should see the {string} page")
    public void iShouldSeeThePage(String expectedTitle) {
        assertEquals(expectedTitle, new InventoryPage(driver).title());
    }

    @Then("I should see the error {string}")
    public void iShouldSeeTheError(String expectedError) {
        assertEquals(expectedError, new LoginPage(driver).errorMessage());
    }

    @Then("I should be back on the login page")
    public void iShouldBeBackOnTheLoginPage() {
        assertTrue(new LoginPage(driver).isShown());
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/SortSteps.java   (page-object version)
package com.qea.selenium.steps;

import com.qea.selenium.pages.InventoryPage;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for sorting.feature. The login steps come from LoginSteps. */
public class SortSteps extends BaseSteps {

    @When("I sort the products by {string}")
    public void iSortTheProductsBy(String order) {
        new InventoryPage(driver).sortBy(order);
    }

    @Then("the first product should be {string}")
    public void theFirstProductShouldBe(String expectedName) {
        assertEquals(expectedName, new InventoryPage(driver).firstProductName());
    }
}
```

**Compare** with the Handout 3 versions: no `By`, no `findElement`, no `WebDriverWait` left in the step classes. The waits for the products page, the menu and the login page now live in the page objects.

---

## Part 4: A new feature: the shopping cart

A new user story:

```text
SL-103  As a shopper
        I want to collect products in a cart
        So that I can buy them together
```

**The feature file.** It starts from the same two login steps as `sorting.feature`, so they go in a Background. The third scenario uses a **data table** (Handout 1, topic 1.3).

```gherkin
# src/test/resources/features/cart.feature
@SL-103
Feature: Shopping cart
  Shoppers collect products in a cart before checking out.
  The badge on the cart icon shows how many products are in the cart.

  Background:
    Given I am on the login page
    And I have logged in with username "standard_user" and password "secret_sauce"

  @smoke
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

Run it first, without any new Java: the Background steps pass (they are in `LoginSteps`), and Cucumber prints **snippets** for the cart steps. Use them to start `CartSteps`.

**The step class.** A one-column data table arrives as a `List<String>`, one item per row. `{int}` turns `2` into an `int`.

```java
// src/test/java/com/qea/selenium/steps/CartSteps.java
package com.qea.selenium.steps;

import com.qea.selenium.pages.CartPage;
import com.qea.selenium.pages.InventoryPage;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for cart.feature. The login steps come from LoginSteps. */
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

---

## Part 5: Run it

```bash
mvn clean test          # everything
mvn test -Psmoke        # smoke scenarios only
```

### Checkpoint

| Command | Expected |
|---|---|
| `mvn clean test` | **16 scenarios** pass: 9 login, 4 sorting, 3 cart (the `@wip` scenario is excluded). Your Selenium JUnit tests run too. |
| `mvn test -Psmoke` | `Tests run: 4`: the logout, the 2 price sorts and the first cart scenario |
| Open `target/cucumber-reports/cucumber.html` | Three features, every scenario and step, with tags and durations |

`performance_glitch_user` takes a few seconds longer than the others: the wait in the `InventoryPage` constructor handles it.

---

## Your turn

1. **Find the layers:** pick the step `When I add "Sauce Labs Backpack" to the cart` and write down every class and method it passes through, from the feature file to the browser.
2. **Change the UI, fix one place:** in `LoginPage`, change `By.id("login-button")` to `By.id("login-btn")` and run. How many scenarios fail? Fix it, and notice that no feature file or step changed. (In Handout 3, how many places would you have had to fix?)
3. **A failure in the report:** in `cart.feature`, change `Then the cart badge should show 2` to `3`. Run, open the HTML report, and find the failed step and the attached screenshot. Undo the change.
4. **Turn the cart into an outline:** make "Adding products shows the count" add **one**, **two** or **three** products, with the expected count in the Examples table. Do you need any new Java?
5. **A known bug:** log in as `problem_user` and sort by "Name (Z to A)" in a new scenario. Does it pass? Tag it `@wip` with a comment describing the bug, as a team would until it is fixed.
6. **Stretch: checkout.** Add a `checkout.feature` for a new story SL-105 ("the overview adds 8% tax"): create `CheckoutInformationPage` (`continueWith(first, last, postcode)`) and `CheckoutOverviewPage` (`itemTotal()`, `tax()`, `total()`), then `CheckoutSteps`. Expected for Backpack + Bike Light: item total $39.98, tax $3.20, total $43.18.

---

## Common errors

| You see | Why | Fix |
|---|---|---|
| `TimeoutException` in the `InventoryPage` constructor | Login failed, so the products page never appeared | Check the username and password in the scenario; look at the screenshot in the report |
| A refused-login scenario times out | `When I log in with ...` calls `loginAs`, which waits for the products page | That step must call `loginExpectingError` |
| `NoSuchElementException` in `addProductToCart` | Product name differs from the page (e.g. "Backpack" instead of "Sauce Labs Backpack") | Use the full product name, exactly as shown on the page |
| Step definitions full of `By` and `findElement` | Logic in the wrong layer | Move it into page objects; keep steps thin |
| `NullPointerException` on `driver` | A step class doesn't extend `BaseSteps`, or `Hooks` isn't in the glue package | Every step class extends `BaseSteps`; `Hooks` lives in `com.qea.selenium.steps` |
| Cart steps undefined although `CartSteps` exists | `CartSteps` is not in `com.qea.selenium.steps` | Put every step class in the glue package |

---

**End of the BDD block.** You have built a complete Selenium + Cucumber framework: readable feature files, thin step definitions, page objects with waits, hooks with screenshots, tags, suites, profiles and reports. Use it as a starting point for your own projects, and test yourself with `cucumber-interview-questions.md`.
