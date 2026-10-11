# Page Object Model and Page Factory

## Learning Objectives

By the end of this lesson you will be able to:

- Describe the maintenance problem of "scripts with locators everywhere" and how the **Page Object Model (POM)** solves it.
- Explain the principles of POM: one class per page/component, locators and actions inside the page class, **assertions in tests**, methods that return page objects.
- Refactor a script-style test into page objects step by step.
- Build a complete page-class set for a real application (SauceDemo login, inventory, cart, three checkout pages, and a header component) and write clean tests that use them.
- Create a **`BasePage`** that holds the shared driver, waits, and helper methods.
- Choose good locators for page objects and handle **dynamic elements** (parameterized locators, lists, loading states).
- Use **method chaining** and **return types** to model navigation between pages.
- Use **Page Factory** (`@FindBy`, `PageFactory.initElements`) and explain how it uses **lazy lookup via proxies**.
- Compare plain POM (`By` fields) with Page Factory using a decision table, including caveats such as stale elements and the library's changing status.
- Organise a project into `pages`, `tests`, `utils`, and `drivers` packages, ready for **Project 2**.

---

## Why This Matters

Consider an automation suite of 100 tests, each one logging in through its own copy of these lines:

```java
driver.findElement(By.id("user-name")).sendKeys(user);
driver.findElement(By.id("password")).sendKeys(pass);
driver.findElement(By.id("login-button")).click();
```

One day a developer renames the login button's id from `login-button` to `submit-login`. Suddenly **100 tests fail**, and you must search and edit 100 places. This scenario is real and is the reason that unstructured automation suites collapse under their own weight after a few months.

**Analogy.** Think of a school with 100 classrooms and no central phone directory: every teacher keeps a private list of phone numbers. When the head teacher's number changes, 100 lists need correcting. A **single directory** at the front desk fixes this: change one entry and everyone benefits. A page object is that directory entry for one page of the application.

The **Page Object Model** is the design pattern that fixes the problem. It is the most widely used pattern in Selenium frameworks, it appears in virtually every automation job interview, and it is the structure of **Project 2: Test Automation Framework**. Today's exercise (converting your Project 2 tests to POM/Page Factory) is the milestone of the week, and Thursday's BDD step definitions will call these same page classes (covered in depth on Thursday). Time invested here pays off for the rest of the course.

Real-world scenarios where POM pays off:

1. **Redesign.** The company changes its login screen. With POM, one class changes; the 100 tests do not.
2. **New teammate.** A new tester reads `checkout.fillInfo("Ada", "Lovelace", "12345").continueToOverview()` and understands it immediately, without reading locators.
3. **Parallel work.** One engineer writes page classes for the new checkout while another writes tests against the agreed method names.
4. **Flaky tests.** Waiting logic lives in one base class, so improving stability once improves every test.

---

## The Concept

### 1. The Idea of POM

> **Create one class for each page (or significant component) of the application. The class contains (a) the locators of the elements on that page and (b) methods describing what a user can *do* on that page. Tests call those methods and never touch locators directly.**

Analogy: a **TV remote control**. You press "Volume Up" without knowing which circuit, wire, or infrared code is used. If the manufacturer changes the internals, you still press the same button. The page class is the remote: tests press buttons (`loginPage.loginAs(...)`), and only the page class knows the wiring (locators).

**Before POM (script style):**

```java
@Test
void validLogin() {
    driver.get("https://www.saucedemo.com");
    driver.findElement(By.id("user-name")).sendKeys("standard_user");
    driver.findElement(By.id("password")).sendKeys("secret_sauce");
    driver.findElement(By.id("login-button")).click();
    Assertions.assertTrue(driver.getCurrentUrl().contains("inventory"));
}
```

**After POM:**

```java
@Test
void validLogin() {
    InventoryPage inventory = new LoginPage(driver)
            .open()
            .loginAs("standard_user", "secret_sauce");
    Assertions.assertTrue(inventory.isLoaded());
}
```

The test now reads like a business description. Its locators live in exactly **one** place.

**What, why, when, where (summary).**

- **What:** a design pattern; classes that model pages.
- **Why:** to reduce duplication and make UI changes cheap.
- **When:** from the first test you write for an application, since converting later costs more.
- **Where:** in every UI automation framework, in any language (Java, Python, C#, JavaScript).

### 2. Benefits

| Benefit | Explanation |
|---|---|
| **Maintainability** | A UI change is fixed in one class, not in 100 tests |
| **Reusability** | `loginAs` is written once and used by every test |
| **Readability** | Tests describe *what*, not *how* |
| **Separation of concerns** | Page classes know the UI; test classes know the business expectations |
| **Collaboration** | Several engineers can work on pages and tests in parallel |
| **Stability** | Waits and retries are centralised and consistent |

### 3. The Rules of Good Page Objects

1. **One page class per page (or reusable component such as a header or navigation bar).**
2. **Locators are private**; tests should never see `By` objects.
3. **Methods represent user actions or queries** with business names: `addToCart(item)`, `getErrorMessage()`, not `clickButton3()`.
4. **No assertions in page classes.** Page objects *report* state (`isLoaded()`, `getTitleText()`); the **test** decides pass or fail with an assertion library. This keeps pages reusable for both positive and negative tests.
5. **Navigation methods return the next page object** (`loginAs` returns `InventoryPage`), modelling the user journey and enabling **method chaining**. Methods that stay on the same page return `this` (or `void`).
6. **Waits belong in the page object** (or its base class), so tests are free of timing code.
7. **Do not expose `WebElement`s** from public methods where avoidable; expose behaviours and data.
8. A page class should be **small and focused**. If it grows huge, split it into components.

**Why rule 4 matters, with an example.** Suppose `LoginPage.loginAs` contained `assertTrue(url.contains("inventory"))`. A negative test (wrong password) could never reuse it, because the assertion would fail by design. If the page only *reports* ("which page am I on?"), the positive test asserts "inventory" and the negative test asserts "error shown".

### 4. Project Structure

```
selenium-framework/
 ├── pom.xml
 └── src/
     ├── main/java/com/revature/qea/
     │    ├── drivers/DriverFactory.java        (Monday's factory)
     │    ├── pages/
     │    │    ├── BasePage.java
     │    │    ├── HeaderComponent.java
     │    │    ├── LoginPage.java
     │    │    ├── InventoryPage.java
     │    │    ├── CartPage.java
     │    │    ├── CheckoutInfoPage.java
     │    │    ├── CheckoutOverviewPage.java
     │    │    └── CheckoutCompletePage.java
     │    └── utils/
     │         ├── WaitUtils.java, ScreenshotUtils.java, ...
     └── test/java/com/revature/qea/tests/
          ├── BaseTest.java
          ├── LoginTest.java
          └── CheckoutTest.java
```

Putting page classes under `src/main` and tests under `src/test` is one common convention; some teams place pages under `src/test` too, since only tests use them. Either is acceptable; choose one and stay consistent. (The test runner integration with Cucumber/JUnit is covered later in the week. Today you can run tests from simple `main` methods or from the JUnit setup your instructor provides; the page objects are independent of the runner.)

### 5. Before/After Refactor Walkthrough

This section takes one realistic script-style test and refactors it into POM in six small steps, so you can see *why* each change is made. The test: log in, add a backpack, open the cart, check the item is there.

#### Step 0: the script

```java
@Test
void backpackAppearsInCart() throws InterruptedException {
    driver.get("https://www.saucedemo.com");
    driver.findElement(By.id("user-name")).sendKeys("standard_user");
    driver.findElement(By.id("password")).sendKeys("secret_sauce");
    driver.findElement(By.id("login-button")).click();
    Thread.sleep(2000);
    driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();
    driver.findElement(By.className("shopping_cart_link")).click();
    Thread.sleep(1000);
    String item = driver.findElement(By.className("inventory_item_name")).getText();
    Assertions.assertEquals("Sauce Labs Backpack", item);
}
```

Problems you can already see: locators mixed with the test logic; `Thread.sleep` (slow and flaky); nothing reusable; the test says *how*, not *what*.

#### Step 1: extract locators into one place

Move every locator into named fields of a class (still no methods):

```java
private final By usernameField = By.id("user-name");
private final By passwordField = By.id("password");
private final By loginButton   = By.id("login-button");
```

**Why.** A name such as `loginButton` documents intent and gives one place to edit.

#### Step 2: wrap multi-step actions in methods

Group the three login lines into `loginAs(username, password)`. **Why.** The test should say "log in", not "type, type, click".

#### Step 3: replace sleeps with waits inside a base class

Put `waitVisible`, `click`, `type`, `textOf` in `BasePage` (next section). The page methods call these, so each interaction waits for the element to be ready. **Why.** The waits from Tuesday are now written once and used everywhere.

#### Step 4: return the next page

`loginAs` returns `new InventoryPage(driver)`. **Why.** The return type teaches both the compiler and the reader where the user ends up, and enables chaining.

#### Step 5: repeat for other pages

Create `InventoryPage` (`addToCart`, `openCart`) and `CartPage` (`getItemNames`).

#### Step 6: the final test

```java
@Test
void backpackAppearsInCart() {
    CartPage cart = new LoginPage(driver)
            .open()
            .loginAs("standard_user", "secret_sauce")
            .addToCart("Sauce Labs Backpack")
            .openCart();

    Assertions.assertEquals(List.of("Sauce Labs Backpack"), cart.getItemNames());
}
```

**What changed.**

| Aspect | Script | POM |
|---|---|---|
| Lines in test | 10 | 7 (and shorter in meaning) |
| Locators in test | 5 | 0 |
| `Thread.sleep` | 2 | 0 |
| Where to fix a changed id | every test | one page class |
| Readability | "how" | "what" |

The same refactor with a changed locator: if SauceDemo renamed the cart link class, you would edit `InventoryPage` only.

### 6. Building a `BasePage`

All pages need the same ingredients: the driver, a wait, and common actions. Put them in a parent class:

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;

public abstract class BasePage {

    protected final WebDriver driver;
    protected final WebDriverWait wait;

    protected BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    protected WebElement waitVisible(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    protected void click(By locator) {
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
    }

    protected void type(By locator, String text) {
        WebElement field = waitVisible(locator);
        field.clear();
        field.sendKeys(text);
    }

    protected String textOf(By locator) {
        return waitVisible(locator).getText();
    }

    protected boolean isDisplayed(By locator) {
        return !driver.findElements(locator).isEmpty()
                && driver.findElement(locator).isDisplayed();
    }

    protected List<String> textsOf(By locator) {
        return driver.findElements(locator).stream()
                .map(WebElement::getText)
                .collect(Collectors.toList());
    }

    protected void waitForUrlContaining(String fragment) {
        wait.until(ExpectedConditions.urlContains(fragment));
    }
}
```

**Line-by-line explanation.**

- `public abstract class BasePage`: `abstract` means nobody can write `new BasePage(...)`; it exists only to be extended by `LoginPage` and the others.
- `protected final WebDriver driver;`: `protected` means visible to subclasses (and the same package) but not to tests in other packages. `final` means assigned once.
- The constructor receives the driver. The **same** driver instance is handed from page to page (`new InventoryPage(driver)`), so the whole test uses one browser.
- `waitVisible(By)`: wraps `visibilityOfElementLocated`, returning the element once displayed.
- `click(By)`: waits for `elementToBeClickable` (visible and enabled) and then clicks. This avoids both "not found" and "click intercepted" timing failures.
- `type(By, String)`: waits, clears old text, then types. Clearing prevents text from being appended to existing content.
- `textOf(By)`: waits and returns visible text.
- `isDisplayed(By)`: uses `findElements` (plural), which returns an empty list rather than throwing if nothing matches. The check "list is not empty AND the first match is displayed" is a safe way to ask "is it there?" without waiting.
- `textsOf(By)`: a helper that turns a list of elements into a list of strings using a Java stream: `.map(WebElement::getText)` applies `getText` to each element; `.collect(Collectors.toList())` builds the result list.
- `waitForUrlContaining`: used by page constructors to verify navigation.

These helpers combine the waits and interactions from Tuesday, so every page gets stable behaviour for free. Your Monday/Tuesday `WaitUtils` can be reused here instead of re-writing the waits.

### 7. Complete Page Classes for SauceDemo (Plain POM)

SauceDemo (`https://www.saucedemo.com`) is a practice shop. The flow is: **Login, Inventory, Cart, Checkout step one (your information), Checkout step two (overview), Checkout complete.** We build a class for each, plus a header component shared by the logged-in pages.

Test accounts on the site's login page include `standard_user` and `locked_out_user`; the password for all is `secret_sauce`.

#### 7.1 `HeaderComponent`

The burger menu and the cart icon appear on every logged-in page. Rather than duplicating their locators, put them in one class:

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class HeaderComponent extends BasePage {

    private final By menuButton   = By.id("react-burger-menu-btn");
    private final By logoutLink   = By.id("logout_sidebar_link");
    private final By resetLink    = By.id("reset_sidebar_link");
    private final By allItemsLink = By.id("inventory_sidebar_link");
    private final By cartLink     = By.className("shopping_cart_link");
    private final By cartBadge    = By.className("shopping_cart_badge");

    public HeaderComponent(WebDriver driver) {
        super(driver);
    }

    public LoginPage logout() {
        click(menuButton);
        click(logoutLink);
        return new LoginPage(driver);
    }

    public HeaderComponent resetAppState() {
        click(menuButton);
        click(resetLink);
        return this;
    }

    public int getCartCount() {
        return isDisplayed(cartBadge) ? Integer.parseInt(textOf(cartBadge)) : 0;
    }

    public CartPage openCart() {
        click(cartLink);
        return new CartPage(driver);
    }
}
```

**Explanation.** The badge only exists when the cart is not empty, so `getCartCount` returns 0 when the badge is missing (using the non-waiting `isDisplayed`). `logout` opens the menu, then clicks the link; `click` waits for the link to become clickable while the menu slides open.

#### 7.2 `LoginPage`

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage extends BasePage {

    private static final String URL = "https://www.saucedemo.com";

    // Locators: private, in one place
    private final By usernameField = By.id("user-name");
    private final By passwordField = By.id("password");
    private final By loginButton   = By.id("login-button");
    private final By errorMessage  = By.cssSelector("[data-test='error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage open() {
        driver.get(URL);
        waitVisible(loginButton);          // page is ready when the button is visible
        return this;
    }

    public LoginPage enterUsername(String username) {
        type(usernameField, username);
        return this;                        // same page: return this (enables chaining)
    }

    public LoginPage enterPassword(String password) {
        type(passwordField, password);
        return this;
    }

    /** Successful login moves the user to the inventory page. */
    public InventoryPage loginAs(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        click(loginButton);
        return new InventoryPage(driver);
    }

    /** For negative tests: we expect to STAY on the login page. */
    public LoginPage loginExpectingFailure(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        click(loginButton);
        return this;
    }

    public String getErrorMessage() {
        return textOf(errorMessage);
    }

    public boolean isErrorDisplayed() {
        return isDisplayed(errorMessage);
    }
}
```

**Explanation.**

- `private static final String URL` is a constant: one copy for the class (`static`), never reassigned (`final`). In Project 2 you will later read the base URL from configuration.
- `open()` navigates and waits for a known element, so the page is "ready" before the test continues. It returns `this` so we can chain `.loginAs(...)`.
- `enterUsername` and `enterPassword` return `this`; they stay on the same page.
- `loginAs` returns `InventoryPage` because on success the user lands there. Its constructor verifies the URL (below), so a failed login is detected immediately with a clear error rather than later.
- `loginExpectingFailure` returns `LoginPage` because the user stays. Two methods, two return types: the type documents the outcome.
- The locked-out user receives an error such as `Epic sadface: Sorry, this user has been locked out.`

#### 7.3 `InventoryPage`

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.Select;

import java.util.List;
import java.util.stream.Collectors;

public class InventoryPage extends BasePage {

    private final By pageTitle      = By.className("title");
    private final By productNames   = By.className("inventory_item_name");
    private final By productPrices  = By.className("inventory_item_price");
    private final By sortDropdown   = By.className("product_sort_container");

    public InventoryPage(WebDriver driver) {
        super(driver);
        waitForUrlContaining("inventory");     // fail fast if we are on the wrong page
    }

    public HeaderComponent header() {
        return new HeaderComponent(driver);
    }

    public boolean isLoaded() {
        return textOf(pageTitle).equals("Products");
    }

    public List<String> getProductNames() {
        return textsOf(productNames);
    }

    public List<Double> getProductPrices() {
        return textsOf(productPrices).stream()
                .map(t -> Double.parseDouble(t.replace("$", "")))
                .collect(Collectors.toList());
    }

    public InventoryPage sortBy(String visibleText) {
        new Select(waitVisible(sortDropdown)).selectByVisibleText(visibleText);
        return this;
    }

    public InventoryPage addToCart(String productName) {
        click(addButton(productName));
        return this;
    }

    public InventoryPage removeFromCart(String productName) {
        click(removeButton(productName));
        return this;
    }

    public int getCartCount() {
        return header().getCartCount();
    }

    public CartPage openCart() {
        return header().openCart();
    }

    // ---- dynamic locator builders (private) ----
    private By addButton(String productName) {
        return By.id("add-to-cart-" + slug(productName));
    }

    private By removeButton(String productName) {
        return By.id("remove-" + slug(productName));
    }

    private String slug(String productName) {
        return productName.toLowerCase().replace(' ', '-');
    }
}
```

**Explanation.**

- The constructor calls `super(driver)` first (required), then `waitForUrlContaining("inventory")`. If someone constructs `InventoryPage` while on the wrong page, the test fails after 10 seconds with a `TimeoutException` naming the URL condition: a far clearer signal than a later `NoSuchElementException`.
- `header()` returns a **component**. The inventory page *has a* header (composition), rather than *being* one.
- `getProductPrices` converts "$29.99" to `29.99`: `replace("$", "")` removes the symbol; `Double.parseDouble` converts text to a number. Tests can then check sort order numerically.
- `sortBy` uses Tuesday's `Select` class. Valid texts include `Name (A to Z)`, `Name (Z to A)`, `Price (low to high)`, `Price (high to low)`.
- `addButton(String)` builds a locator from data. SauceDemo gives each button an id made from the product name: "Sauce Labs Backpack" becomes `add-to-cart-sauce-labs-backpack`. `slug` lowercases and replaces spaces with hyphens. (Products with dots or brackets in their names need a more careful slug; a lookup map is an alternative.)
- The cart badge and cart link live in the header, so `getCartCount` and `openCart` delegate. Tests do not care where they are implemented.

#### 7.4 `CartPage`

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

public class CartPage extends BasePage {

    private final By cartItemNames   = By.className("inventory_item_name");
    private final By cartItems       = By.className("cart_item");
    private final By continueShopping = By.id("continue-shopping");
    private final By checkoutButton  = By.id("checkout");

    public CartPage(WebDriver driver) {
        super(driver);
        waitForUrlContaining("cart");
    }

    public HeaderComponent header() {
        return new HeaderComponent(driver);
    }

    public List<String> getItemNames() {
        return textsOf(cartItemNames);
    }

    public int getItemCount() {
        return driver.findElements(cartItems).size();
    }

    public CartPage removeItem(String productName) {
        click(By.id("remove-" + productName.toLowerCase().replace(' ', '-')));
        return this;
    }

    public InventoryPage continueShopping() {
        click(continueShopping);
        return new InventoryPage(driver);
    }

    public CheckoutInfoPage proceedToCheckout() {
        click(checkoutButton);
        return new CheckoutInfoPage(driver);
    }
}
```

**Explanation.** `getItemCount` uses `findElements(...).size()`, which is `0` for an empty cart (no exception). `proceedToCheckout` navigates forward; `continueShopping` navigates back to a page we already know.

#### 7.5 `CheckoutInfoPage` (checkout step one)

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CheckoutInfoPage extends BasePage {

    private final By firstName  = By.id("first-name");
    private final By lastName   = By.id("last-name");
    private final By postalCode = By.id("postal-code");
    private final By continueBtn = By.id("continue");
    private final By cancelBtn   = By.id("cancel");
    private final By error       = By.cssSelector("[data-test='error']");

    public CheckoutInfoPage(WebDriver driver) {
        super(driver);
        waitForUrlContaining("checkout-step-one");
    }

    public CheckoutInfoPage fillInfo(String first, String last, String zip) {
        type(firstName, first);
        type(lastName, last);
        type(postalCode, zip);
        return this;
    }

    public CheckoutOverviewPage continueToOverview() {
        click(continueBtn);
        return new CheckoutOverviewPage(driver);
    }

    /** Negative path: we expect validation to keep us on this page. */
    public CheckoutInfoPage continueExpectingError() {
        click(continueBtn);
        return this;
    }

    public CartPage cancel() {
        click(cancelBtn);
        return new CartPage(driver);
    }

    public String getErrorMessage() {
        return textOf(error);
    }
}
```

**Explanation.** Same pattern as login: a "happy" method returning the next page and an "expecting error" method returning `this`. With empty fields the site shows `Error: First Name is required`.

#### 7.6 `CheckoutOverviewPage` (checkout step two)

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

public class CheckoutOverviewPage extends BasePage {

    private final By itemNames  = By.className("inventory_item_name");
    private final By subtotal   = By.className("summary_subtotal_label");
    private final By tax        = By.className("summary_tax_label");
    private final By total      = By.className("summary_total_label");
    private final By finishBtn  = By.id("finish");
    private final By cancelBtn  = By.id("cancel");

    public CheckoutOverviewPage(WebDriver driver) {
        super(driver);
        waitForUrlContaining("checkout-step-two");
    }

    public List<String> getItemNames() {
        return textsOf(itemNames);
    }

    public double getItemTotal() {
        return moneyIn(textOf(subtotal));      // "Item total: $39.98"
    }

    public double getTax() {
        return moneyIn(textOf(tax));           // "Tax: $3.20"
    }

    public double getGrandTotal() {
        return moneyIn(textOf(total));         // "Total: $43.18"
    }

    public CheckoutCompletePage finish() {
        click(finishBtn);
        return new CheckoutCompletePage(driver);
    }

    public InventoryPage cancel() {
        click(cancelBtn);
        return new InventoryPage(driver);
    }

    private double moneyIn(String label) {
        return Double.parseDouble(label.substring(label.indexOf('$') + 1));
    }
}
```

**Explanation.** `moneyIn` is a private helper: `label.indexOf('$')` finds the dollar sign; `substring(position + 1)` keeps the text after it; `Double.parseDouble` converts it. Tests can then assert `itemTotal + tax == grandTotal` (with a tolerance, since money in `double` can have rounding noise; real frameworks often use `BigDecimal`).

#### 7.7 `CheckoutCompletePage`

```java
package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CheckoutCompletePage extends BasePage {

    private final By header     = By.className("complete-header");
    private final By backHome   = By.id("back-to-products");

    public CheckoutCompletePage(WebDriver driver) {
        super(driver);
        waitForUrlContaining("checkout-complete");
    }

    public String getConfirmationHeader() {
        return textOf(header);                   // "Thank you for your order!"
    }

    public InventoryPage backToProducts() {
        click(backHome);
        return new InventoryPage(driver);
    }
}
```

**Design points to notice across the set:**

- Constructors of destination pages **verify they are on the right page** (`urlContains`). A wrong navigation fails immediately with a clear message.
- `loginAs` and `loginExpectingFailure` are two methods because the outcome differs; the **return type tells the story**.
- `addToCart(String)` builds a locator from data, showing that one method can serve every product.
- There are **no assertions** in these pages.
- The page classes form a small **graph**: each navigation method returns the page that follows it.

### 8. Using Page Objects in Tests

A shared base test creates and closes the browser (JUnit 5 shown; any runner works the same way):

```java
package com.revature.qea.tests;

import com.revature.qea.drivers.DriverFactory;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.WebDriver;

public abstract class BaseTest {

    protected WebDriver driver;

    @BeforeEach
    void setUp() {
        driver = DriverFactory.createDriver("chrome", false);   // Monday's factory
    }

    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
```

- `@BeforeEach` runs before every test method; `@AfterEach` runs after it, even if the test failed.
- `DriverFactory.createDriver(browser, headless)` is the factory from Monday. The test class does not know how Chrome is configured.

The tests:

```java
package com.revature.qea.tests;

import com.revature.qea.pages.*;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.List;

class CheckoutTest extends BaseTest {

    @Test
    void userCanCompleteAPurchase() {
        CheckoutOverviewPage overview = new LoginPage(driver)
                .open()
                .loginAs("standard_user", "secret_sauce")
                .addToCart("Sauce Labs Backpack")
                .addToCart("Sauce Labs Bike Light")
                .openCart()
                .proceedToCheckout()
                .fillInfo("Ada", "Lovelace", "12345")
                .continueToOverview();

        Assertions.assertEquals(
                List.of("Sauce Labs Backpack", "Sauce Labs Bike Light"),
                overview.getItemNames());
        Assertions.assertEquals(39.98, overview.getItemTotal(), 0.001);

        CheckoutCompletePage done = overview.finish();
        Assertions.assertEquals("Thank you for your order!", done.getConfirmationHeader());
    }

    @Test
    void lockedOutUserSeesAnError() {
        LoginPage login = new LoginPage(driver)
                .open()
                .loginExpectingFailure("locked_out_user", "secret_sauce");

        Assertions.assertTrue(login.isErrorDisplayed());
        Assertions.assertTrue(login.getErrorMessage().contains("locked out"));
    }

    @Test
    void missingFirstNameShowsValidationError() {
        CheckoutInfoPage info = new LoginPage(driver)
                .open()
                .loginAs("standard_user", "secret_sauce")
                .addToCart("Sauce Labs Backpack")
                .openCart()
                .proceedToCheckout()
                .fillInfo("", "Lovelace", "12345")
                .continueExpectingError();

        Assertions.assertEquals("Error: First Name is required", info.getErrorMessage());
    }
}
```

**Explanation.**

- The big chain reads like a user story: *open the login page, log in, add two products, open the cart, proceed to checkout, fill in details, continue.*
- **Assertions live in the tests** (`Assertions.assertEquals`). The `0.001` third argument is the tolerance for comparing decimals.
- `lockedOutUserSeesAnError` uses `loginExpectingFailure`, so no exception is thrown for the missing inventory page.
- Prices of 29.99 plus 9.99 give 39.98; the price data of a practice site may change, so if a test fails on an amount, check the live site first.
- (Behaviour-driven tests written in Gherkin, which call these same page methods from step definitions, are covered in depth on Thursday and Friday; nothing in the page classes needs to change for that.)

### 9. Locator Strategies Inside Page Objects

Locators are the most fragile part of any page object, so choose them deliberately. You met the eight `By` strategies on Monday; here is how to choose among them *for page objects*.

| Priority | Strategy | Example | Why / when |
|---|---|---|---|
| 1 | Stable dedicated test attribute | `By.cssSelector("[data-test='error']")` | Developers add it for testing; survives redesigns |
| 2 | `id` | `By.id("login-button")` | Unique by specification, fast |
| 3 | `name` | `By.name("q")` | Common on form fields |
| 4 | Short CSS selector | `By.cssSelector(".inventory_item_name")` | Readable and fast; tied to class names |
| 5 | Link text | `By.linkText("Terms")` | Good for links with stable text; breaks with translation |
| 6 | XPath (relative) | `//div[@class='cart_item']//button` | Needed for parent/sibling navigation and text matching |
| Avoid | Absolute XPath, long chains | `/html/body/div[2]/div/div[3]/button` | Breaks on any layout change |
| Avoid | Auto-generated classes | `.css-1x9h2k` | Changes with every build |

**Practices inside page classes.**

1. **Name locators by role, not by type**: `loginButton`, not `button1` or `blueBtn`.
2. **Keep every locator as a private field** at the top of the class, so a maintainer sees them all together.
3. **Scope searches**: for repeated structures (cart rows, product cards), locate the container first and search *inside* it:

```java
WebElement card = driver.findElements(By.className("inventory_item")).stream()
        .filter(c -> c.findElement(By.className("inventory_item_name")).getText().equals(productName))
        .findFirst()
        .orElseThrow(() -> new NoSuchElementException("No product named " + productName));
card.findElement(By.tagName("button")).click();
```

This version does not rely on any button id pattern; it finds the card whose name matches and clicks the button inside it. Slower, but robust when ids are unpredictable.

4. **Prefer a few strong locators to many weak ones.** If you must use XPath, make it relative and anchored on stable text or attributes.
5. **Ask developers for `data-test` attributes** (or `data-testid`) when the page lacks stable hooks. Many teams agree on this as a convention.
6. **Selenium 4 relative locators** (`RelativeLocator.with(By.tagName("input")).below(By.id("user-name"))`) exist, but they depend on layout and are best kept for cases with no better hook.

### 10. Handling Dynamic Elements

Real pages change while you test. Page objects are the right place to absorb that complexity.

**10.1 Parameterised locators.** When the element depends on data (product name, row number), build the `By` from parameters, as `addButton(String)` did. A general helper:

```java
private By rowCell(int row, int column) {
    return By.xpath(String.format("//table[@id='data']/tbody/tr[%d]/td[%d]", row, column));
}
```

`String.format` replaces each `%d` with an integer. The XPath index is 1-based.

**10.2 Elements that appear later.** Waiting is already in `BasePage` (`waitVisible`, `click`). For something that must disappear (a spinner), add:

```java
protected void waitUntilGone(By locator) {
    wait.until(ExpectedConditions.invisibilityOfElementLocated(locator));
}
```

and call it from page methods that trigger loading: `click(searchButton); waitUntilGone(spinner);`.

**10.3 Lists whose size changes.** Never store a `List<WebElement>` in a field of a plain page object; call `findElements` inside the method each time, so you read the current page. The cart count after adding items is the classic example.

**10.4 Content that re-renders (stale elements).** When a page re-draws part of itself (sorting a list, filtering a table), a `WebElement` found earlier becomes stale, and using it throws `StaleElementReferenceException`. The plain-POM habit of **locating at the moment of use** (via `By`) avoids this. Example: after `sortBy("Price (low to high)")`, call `getProductNames()` again; it re-finds the elements.

**10.5 Elements that may or may not exist.** Optional banners and badges: use the non-waiting `isDisplayed(By)` helper (based on `findElements`), not `waitVisible`, which would wait and then throw.

**10.6 Unstable timing.** Where a UI really is slow, give the specific method a longer wait rather than raising the global timeout:

```java
protected WebElement waitVisible(By locator, Duration timeout) {
    return new WebDriverWait(driver, timeout).until(ExpectedConditions.visibilityOfElementLocated(locator));
}
```

**10.7 Actions inside page objects.** Gestures from the Actions API lesson belong here, for example `header().hoverMenu()` containing `new Actions(driver).moveToElement(menu).perform();`. Likewise, alert and window handling (earlier lessons today) are wrapped so that a test calls `cart.deleteAllConfirming()` or `footer.openTwitterAndReturn()` rather than touching `switchTo()`.

### 11. Components: Reusing Parts of Pages

A header or menu that appears on many pages should be its own class, to avoid duplicating its locators in every page (see `HeaderComponent` in section 7). Pages then **compose** it: `public HeaderComponent header() { return new HeaderComponent(driver); }`. Similarly, a table, a modal dialog, or a product card can be a component that is created with a **root element**:

```java
public class ProductCard {
    private final WebElement root;
    public ProductCard(WebElement root) { this.root = root; }
    public String name()  { return root.findElement(By.className("inventory_item_name")).getText(); }
    public String price() { return root.findElement(By.className("inventory_item_price")).getText(); }
    public void addToCart() { root.findElement(By.tagName("button")).click(); }
}
```

Searches inside `root` cannot match another card. `InventoryPage` could then offer `List<ProductCard> cards()`. Use components when the same structure repeats on a page or across pages.

### 12. Page Factory

**Page Factory** is a Selenium support class that offers a different style of declaring elements: instead of `By` fields, you declare `WebElement` fields annotated with `@FindBy`, and Selenium **initialises** them for you. (An *annotation* is a label starting with `@` that attaches information to a field or method; Selenium reads it at run time.)

```java
package com.revature.qea.pf;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class LoginPageFactory {

    private final WebDriver driver;

    @FindBy(id = "user-name")
    private WebElement usernameField;

    @FindBy(id = "password")
    private WebElement passwordField;

    @FindBy(id = "login-button")
    private WebElement loginButton;

    @FindBy(css = "[data-test='error']")
    private WebElement errorMessage;

    public LoginPageFactory(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);     // <-- the key line
    }

    public void loginAs(String username, String password) {
        usernameField.sendKeys(username);
        passwordField.sendKeys(password);
        loginButton.click();
    }

    public String getErrorMessage() {
        return errorMessage.getText();
    }
}
```

**How it works:**

1. `@FindBy` records *how* to find each field: `id`, `name`, `className`, `css`, `xpath`, `linkText`, `partialLinkText`, `tagName` (the same eight strategies from Monday).
2. `PageFactory.initElements(driver, this)` inspects the object's annotated fields and assigns each a **proxy**: a stand-in object that implements `WebElement`.
3. The proxy does **not** search for the element when the page object is created. It searches **every time you use the field** (`usernameField.sendKeys(...)` triggers a fresh `findElement` behind the scenes). This is called **lazy initialisation**.

Consequences of the proxy design:

- You can create page objects **before** the elements exist (before navigation), without errors.
- Each use performs a new lookup, which reduces `StaleElementReferenceException` for ordinary fields (the element is re-found).
- Annotated fields must **not be `final`**; Selenium assigns them after construction.
- If you forget `initElements`, the fields stay `null` and the first use throws `NullPointerException`.

**Lists of elements:**

```java
@FindBy(className = "inventory_item_name")
private List<WebElement> productNames;       // a List<WebElement> field becomes a findElements lookup
```

**Multiple locators:**

```java
@FindBys({@FindBy(id = "menu"), @FindBy(tagName = "a")})   // AND chain: an <a> inside #menu
private List<WebElement> menuLinks;

@FindAll({@FindBy(id = "login"), @FindBy(name = "login")}) // OR: either locator matches
private WebElement loginAlt;
```

**Caching:** `@CacheLookup` makes the proxy remember the first found element:

```java
@CacheLookup
@FindBy(id = "logo")
private WebElement logo;
```

Use it **only for truly static elements**; on a page that re-renders it causes `StaleElementReferenceException`.

**Waits with Page Factory:** the proxies do not wait by default. Combine them with explicit waits that accept `WebElement`s:

```java
wait.until(ExpectedConditions.visibilityOf(usernameField));
wait.until(ExpectedConditions.elementToBeClickable(loginButton)).click();
```

Alternatively, `AjaxElementLocatorFactory` makes each lookup wait up to a number of seconds for the element to be present **and displayed**:

```java
PageFactory.initElements(new AjaxElementLocatorFactory(driver, 10), this);
```

Caution: because it waits for the element to be displayed, a lookup of an element that is *supposed* to be absent (such as an error message in a success test) waits the full 10 seconds and then throws. Do not combine it with long implicit waits.

**Page Factory as a base class.** Put the initialisation in the base class so each page needs no boilerplate:

```java
public abstract class BasePageFactory {
    protected final WebDriver driver;
    protected final WebDriverWait wait;

    protected BasePageFactory(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);   // "this" is the concrete page being constructed
    }
}
```

Because `this` refers to the actual subclass object, its annotated fields are initialised, even though the call is in the parent constructor.

### 13. A Worked Page Factory Version of the Same Pages

Here is the SauceDemo set again in Page Factory style, in a separate package `com.revature.qea.pf` (a real project would pick one style, not keep both). Names are shortened where the pattern repeats.

```java
// LoginPage (PF)
public class LoginPage extends BasePageFactory {
    @FindBy(id = "user-name")             private WebElement usernameField;
    @FindBy(id = "password")              private WebElement passwordField;
    @FindBy(id = "login-button")          private WebElement loginButton;
    @FindBy(css = "[data-test='error']")  private WebElement errorMessage;

    public LoginPage(WebDriver driver) { super(driver); }

    public LoginPage open() {
        driver.get("https://www.saucedemo.com");
        wait.until(ExpectedConditions.visibilityOf(loginButton));
        return this;
    }

    public InventoryPage loginAs(String user, String pass) {
        usernameField.clear();  usernameField.sendKeys(user);
        passwordField.clear();  passwordField.sendKeys(pass);
        wait.until(ExpectedConditions.elementToBeClickable(loginButton)).click();
        return new InventoryPage(driver);
    }

    public LoginPage loginExpectingFailure(String user, String pass) {
        usernameField.sendKeys(user);
        passwordField.sendKeys(pass);
        loginButton.click();
        return this;
    }

    public String getErrorMessage() {
        wait.until(ExpectedConditions.visibilityOf(errorMessage));
        return errorMessage.getText();
    }
}
```

```java
// HeaderComponent (PF)
public class HeaderComponent extends BasePageFactory {
    @FindBy(id = "react-burger-menu-btn")   private WebElement menuButton;
    @FindBy(id = "logout_sidebar_link")     private WebElement logoutLink;
    @FindBy(className = "shopping_cart_link") private WebElement cartLink;
    @FindBy(className = "shopping_cart_badge") private List<WebElement> cartBadge;  // list: may be empty

    public HeaderComponent(WebDriver driver) { super(driver); }

    public LoginPage logout() {
        menuButton.click();
        wait.until(ExpectedConditions.elementToBeClickable(logoutLink)).click();
        return new LoginPage(driver);
    }

    public int getCartCount() {
        return cartBadge.isEmpty() ? 0 : Integer.parseInt(cartBadge.get(0).getText());
    }

    public CartPage openCart() {
        cartLink.click();
        return new CartPage(driver);
    }
}
```

Note the trick: the badge is declared as a **`List<WebElement>`** so an absent badge gives an empty list rather than an exception. This is the Page Factory equivalent of the `findElements`-based `isDisplayed` helper.

```java
// InventoryPage (PF)
public class InventoryPage extends BasePageFactory {
    @FindBy(className = "title")                 private WebElement pageTitle;
    @FindBy(className = "inventory_item")        private List<WebElement> items;
    @FindBy(className = "inventory_item_name")   private List<WebElement> names;
    @FindBy(className = "product_sort_container") private WebElement sortDropdown;

    public InventoryPage(WebDriver driver) {
        super(driver);
        wait.until(ExpectedConditions.urlContains("inventory"));
    }

    public boolean isLoaded() { return pageTitle.getText().equals("Products"); }

    public List<String> getProductNames() {
        return names.stream().map(WebElement::getText).collect(Collectors.toList());
    }

    public InventoryPage sortBy(String visibleText) {
        new Select(sortDropdown).selectByVisibleText(visibleText);
        return this;
    }

    // Dynamic case: annotations are constants, so we fall back to a normal locator
    public InventoryPage addToCart(String productName) {
        String id = "add-to-cart-" + productName.toLowerCase().replace(' ', '-');
        wait.until(ExpectedConditions.elementToBeClickable(By.id(id))).click();
        return this;
    }

    public HeaderComponent header() { return new HeaderComponent(driver); }
    public CartPage openCart()      { return header().openCart(); }
}
```

The `addToCart` method shows the main limitation: the product name is only known at run time, but `@FindBy` values must be compile-time constants. The common workaround is the one shown: use `driver.findElement(By...)` for that one dynamic case, or search within the `items` list.

```java
// CartPage, CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage (PF), condensed
public class CartPage extends BasePageFactory {
    @FindBy(className = "inventory_item_name") private List<WebElement> itemNames;
    @FindBy(id = "checkout")                   private WebElement checkoutButton;

    public CartPage(WebDriver driver) {
        super(driver);
        wait.until(ExpectedConditions.urlContains("cart"));
    }
    public List<String> getItemNames() {
        return itemNames.stream().map(WebElement::getText).collect(Collectors.toList());
    }
    public CheckoutInfoPage proceedToCheckout() {
        checkoutButton.click();
        return new CheckoutInfoPage(driver);
    }
}

public class CheckoutInfoPage extends BasePageFactory {
    @FindBy(id = "first-name")  private WebElement firstName;
    @FindBy(id = "last-name")   private WebElement lastName;
    @FindBy(id = "postal-code") private WebElement postalCode;
    @FindBy(id = "continue")    private WebElement continueBtn;

    public CheckoutInfoPage(WebDriver driver) {
        super(driver);
        wait.until(ExpectedConditions.urlContains("checkout-step-one"));
    }
    public CheckoutInfoPage fillInfo(String first, String last, String zip) {
        firstName.sendKeys(first);
        lastName.sendKeys(last);
        postalCode.sendKeys(zip);
        return this;
    }
    public CheckoutOverviewPage continueToOverview() {
        continueBtn.click();
        return new CheckoutOverviewPage(driver);
    }
}

public class CheckoutOverviewPage extends BasePageFactory {
    @FindBy(className = "summary_subtotal_label") private WebElement subtotal;
    @FindBy(id = "finish")                        private WebElement finishBtn;

    public CheckoutOverviewPage(WebDriver driver) {
        super(driver);
        wait.until(ExpectedConditions.urlContains("checkout-step-two"));
    }
    public double getItemTotal() {
        String label = subtotal.getText();
        return Double.parseDouble(label.substring(label.indexOf('$') + 1));
    }
    public CheckoutCompletePage finish() {
        finishBtn.click();
        return new CheckoutCompletePage(driver);
    }
}

public class CheckoutCompletePage extends BasePageFactory {
    @FindBy(className = "complete-header") private WebElement header;

    public CheckoutCompletePage(WebDriver driver) {
        super(driver);
        wait.until(ExpectedConditions.urlContains("checkout-complete"));
    }
    public String getConfirmationHeader() { return header.getText(); }
}
```

**Observations.**

- The **tests are identical** to the plain-POM tests; only the `import` of the page package differs. This shows that the *pattern* (pages expose actions, tests assert) matters more than the *mechanism* for finding elements.
- The Page Factory pages are shorter to read for static elements, but need extra code for dynamic locators, optional elements (a `List` field), and waiting.
- Explicit waits still use `ExpectedConditions.visibilityOf(WebElement)` and `elementToBeClickable(WebElement)`, the overloads that accept elements rather than locators.

### 14. Plain POM (`By` fields) vs. Page Factory

| Aspect | Plain POM with `By` | Page Factory with `@FindBy` |
|---|---|---|
| Declaration | `private final By loginButton = By.id("...")` | `@FindBy(id = "...") private WebElement loginButton;` |
| Lookup time | When your code calls `driver.findElement(by)` | Lazily, each use, via proxy |
| Waiting | Natural: wait on the `By` | Need `visibilityOf(WebElement)` or the Ajax factory |
| Dynamic locators (product name in XPath) | Easy: build a `By` from parameters | Awkward: annotations are constants |
| Optional elements | `findElements` helper | `List<WebElement>` field |
| Readability | Explicit | Compact, annotation-based |
| Stale elements | Avoided when waiting by locator | Mostly avoided (re-lookup), except with `@CacheLookup` |
| Status in the Selenium project | Always the recommended basis | Support class that exists in the library; the project documentation emphasises plain page objects, and newer Selenium versions may mark `PageFactory` as deprecated, so check the release notes of the version you use |

**Decision table: which should I use?**

| Situation | Recommended |
|---|---|
| Brand-new framework, mostly dynamic or data-driven pages | Plain POM |
| Joining a team whose code base already uses `@FindBy` | Follow the team's style; learn Page Factory |
| Many pages with a few static elements each, and your team likes annotations | Page Factory is acceptable |
| Heavy need for waits, optional elements, and parameterised locators | Plain POM |
| You will upgrade Selenium often and want to avoid deprecated APIs | Plain POM |
| Job interview question "what is Page Factory?" | Be able to explain `@FindBy`, `initElements`, lazy proxies, `@CacheLookup` |
| Today's exercise | Convert to **both**, compare, and note which you found easier |

**Practical guidance:** Both are acceptable in interviews and many existing projects use Page Factory, so you must be able to read and write it. For new frameworks, many teams prefer the plain `By`-based approach with waits in a base page, because it handles dynamic content and waiting more naturally.

### 15. Common POM Anti-Patterns

| Anti-pattern | Why it's bad | Better |
|---|---|---|
| Assertions inside page methods | Pages cannot be reused for negative tests | Return data, assert in tests |
| One giant `AllPages` class | Hard to navigate and maintain | One class per page/component |
| Public locators / exposing `WebElement`s | Tests depend on UI details again | Expose actions |
| `Thread.sleep` in pages | Slow, flaky | Explicit waits |
| Creating a new driver inside a page | Multiple browsers, leaks | Pass the shared `driver` in the constructor |
| Static `driver` shared by every test class | Breaks parallel runs, hidden coupling | Pass driver explicitly (injection) |
| Page methods named after UI mechanics (`clickBlueButton`) | Break when the UI changes | Name by intent (`submitOrder`) |
| Duplicating header/menu code in every page | The original problem again | Component classes |
| Every method returns `void` | Tests must create the next page manually | Return the next page object |

### 16. Troubleshooting Walk-Throughs

**Problem 1: `NullPointerException` in a Page Factory page.**

```text
java.lang.NullPointerException: Cannot invoke "org.openqa.selenium.WebElement.sendKeys(java.lang.CharSequence[])" because "this.usernameField" is null
```

**Diagnosis.** The message names the field that is `null`. The field was never initialised: `PageFactory.initElements(driver, this)` was not called, or was called on a different object, or the field is `final`. **Fix.** Call `initElements` in the constructor (or base constructor) and remove `final`.

**Problem 2: wrong page during navigation.**

```text
org.openqa.selenium.TimeoutException: Expected condition failed: waiting for url to contain "inventory" (tried for 10 second(s) with 500 milliseconds interval)
```

**Diagnosis.** The `InventoryPage` constructor guard fired: the login did not succeed (wrong password, locked-out user, or the click failed). Print `driver.getCurrentUrl()` and look for the on-page error. This is exactly why constructors verify the page: the message points at the real cause.

**Problem 3: `StaleElementReferenceException` with `@CacheLookup`.**

```text
org.openqa.selenium.StaleElementReferenceException: stale element reference: stale element not found
```

**Diagnosis.** The element was cached, then the page re-rendered. Remove `@CacheLookup`, or re-create the page object after navigation.

**Problem 4: `NoSuchElementException` on the right locator.** Check the earlier lesson causes: wrong window (`getTitle()` shows the old page), an iframe ancestor, or missing wait.

---

## Guided Lab: Refactor a Script Test to POM and Page Factory

**Goal.** Convert one script-style Project 2 test into POM, then into Page Factory, proving that only page classes change when a locator breaks.

1. Create a Maven package structure `drivers`, `pages`, `utils`, `tests` under `com.revature.qea`.
2. Copy your script-style SauceDemo test (login, add item, open cart, assert) into `tests/ScriptStyleTest.java`. Run it; note it passes.
3. Create `BasePage` (section 6). Re-use `DriverFactory` from Monday.
4. Create `LoginPage`, `InventoryPage`, `CartPage` (section 7). Create `HeaderComponent`.
5. Write `PomStyleTest` using the chain from section 5, step 6. Run it; it should pass.
6. **Break a locator on purpose.** In `LoginPage` change `By.id("login-button")` to `By.id("login-btn")`. Run `PomStyleTest`, read the exception (a `TimeoutException` waiting for the clickable element), and fix it in the one place. Count the files you edited: 1.
7. Create the `pf` package with `BasePageFactory`, `LoginPage`, `InventoryPage`, `CartPage`, `HeaderComponent`. Write `PageFactoryStyleTest` with the same flow.
8. **Lazy proxy experiment.** In `PageFactoryStyleTest`, construct `new LoginPage(driver)` *before* `open()`. Observe no exception.
9. Add `CheckoutInfoPage`, `CheckoutOverviewPage`, `CheckoutCompletePage` in plain POM and extend the test to a full purchase.
10. Commit with `refactor: introduce page objects`.

**Expected result.**

```text
ScriptStyleTest         PASS
PomStyleTest            PASS (and 1 file edited to repair the broken locator)
PageFactoryStyleTest    PASS
CheckoutTest            PASS
```

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Putting assertions in page methods | Cannot reuse for negative tests | Return state; assert in tests |
| Making locators `public` | Tests start using `By` again | Keep them `private` |
| Forgetting `PageFactory.initElements` | `NullPointerException` | Call it in the constructor/base class |
| Declaring `@FindBy` fields as `final` | Fields are not initialised | Remove `final` |
| `@CacheLookup` on a dynamic page | `StaleElementReferenceException` | Remove it |
| Not returning the next page from navigation methods | Tests cannot chain; manual `new Page(driver)` everywhere | Return the destination page |
| Creating a driver in each page | Many browsers open | Pass one shared driver |
| Using `Thread.sleep` | Slow, flaky | Explicit waits in `BasePage` |
| Using absolute XPath | Breaks on layout change | Short, stable locators |
| Storing `List<WebElement>` in plain page fields | Stale data | Call `findElements` in methods |

---

## Practice Exercises

1. **Convert.** Convert your SauceDemo login/search flow to page objects: `BasePage`, `LoginPage`, `InventoryPage`, `CartPage`. The test class must contain **no** `By`, no `findElement`, and no waits.
2. **Add the checkout pages.** Add `CheckoutInfoPage`, `CheckoutOverviewPage`, and `CheckoutCompletePage`, and chain a full purchase ending with the confirmation header.
3. **Negative tests.** Write tests for locked-out user, wrong password, and empty username. Which `LoginPage` method do they use, and why?
4. **Component.** Use `HeaderComponent` from `InventoryPage` and `CartPage`, and test `logout()` returns a usable `LoginPage`.
5. **Page Factory version.** Re-implement `LoginPage` and `InventoryPage` using `@FindBy` and `PageFactory.initElements`. Use a `List<WebElement>` field for the products.
6. **Lazy proxy experiment.** In a Page Factory class, create the page object **before** calling `driver.get(...)`. Show that no exception occurs until you use a field. Explain why.
7. **`@CacheLookup` trap.** Add `@CacheLookup` to a field on a page that refreshes; reproduce `StaleElementReferenceException` and explain it.
8. **Maintenance drill.** Change one locator in a page class and show that every test using it still passes. Count how many files you edited.
9. **Sort test.** Add `InventoryPage.sortBy` tests: after "Price (low to high)", assert that `getProductPrices()` is in ascending order; after "Name (Z to A)", assert names are in reverse alphabetical order.
10. **Dynamic locator.** Add `CartPage.removeItem(String)` and a test that adds three items, removes one, and checks both the cart contents and the header badge.
11. **the-internet page object.** Create `DynamicLoadingPage` for `https://the-internet.herokuapp.com/dynamic_loading/1` with `start()` returning `this` and `getFinishText()` that waits for the result. The test asserts "Hello World!".
12. **Project 2 milestone.** Apply the structure of section 4 to your Project 2 repository: convert existing tests (to plain POM, then try Page Factory for one page), commit with a message such as `refactor: introduce page objects`, and add a short README paragraph describing the layout.

---

## Solutions and Hints

**1. Convert.** Follow sections 5-7. Check: search the test file for `By.` and `findElement`; there should be none.

**2. Checkout pages.** Use the classes in section 7.5-7.7 and the chain in section 8.

**3. Negative tests.** They use `loginExpectingFailure`, because the user stays on the login page; `loginAs` would try to construct `InventoryPage` and fail with a `TimeoutException`. Expected errors: `Epic sadface: Sorry, this user has been locked out.`, `Epic sadface: Username and password do not match any user in this service`, `Epic sadface: Username is required`.

**4. Component.**

```java
LoginPage login = inventory.header().logout();
Assertions.assertFalse(login.isErrorDisplayed());
```

Better: add `isLoaded()` to `LoginPage` (returning `isDisplayed(loginButton)`) and assert that it is true.

**5. Page Factory version.** See section 13. Hint: `@FindBy(className = "inventory_item_name") private List<WebElement> names;`.

**6. Lazy proxy.** Because the proxy stores *how* to find the element, not the element itself, and only calls `findElement` when you invoke a method on the field, creating the object earlier is harmless.

**7. `@CacheLookup` trap.** Cache a field such as `sortDropdown`, use it, reload the page (`driver.navigate().refresh()`), use it again. The cached element belongs to the old DOM and is stale.

**8. Maintenance drill.** Expected answer: one file edited. If you needed more, a locator was duplicated outside a page object.

**9. Sort test.**

```java
List<Double> prices = inventory.sortBy("Price (low to high)").getProductPrices();
List<Double> sorted = new ArrayList<>(prices);
Collections.sort(sorted);
Assertions.assertEquals(sorted, prices);
```

For names reversed, compare with `sorted.sort(Comparator.reverseOrder())`.

**10. Dynamic locator.** `removeItem` is in section 7.4. Test chain: `inventory.addToCart("Sauce Labs Backpack").addToCart("Sauce Labs Bike Light").addToCart("Sauce Labs Onesie").openCart().removeItem("Sauce Labs Onesie")`; assert `getItemNames()` has two entries and `header().getCartCount()` is 2.

**11. DynamicLoadingPage.**

```java
public class DynamicLoadingPage extends BasePage {
    private final By startButton = By.cssSelector("#start button");
    private final By finishText  = By.cssSelector("#finish h4");

    public DynamicLoadingPage(WebDriver driver) { super(driver); }

    public DynamicLoadingPage start() {
        click(startButton);
        return this;
    }

    public String getFinishText() {
        return textOf(finishText);   // waitVisible handles the delay
    }
}
```

**12. Project 2.** Keep a checklist: no `By` in tests, no assertions in pages, shared `BasePage`, one component for repeated areas, README updated, and a commit per logical step.

---

## Self-Check Questions

1. **What problem does POM solve?** It removes duplicated locators and steps from tests, so a UI change is fixed in one class.
2. **Why should page classes not contain assertions?** Pages must work for positive and negative tests; the test decides pass or fail.
3. **What should a navigation method return?** The page object of the page the user lands on (or `this` if they stay).
4. **What does `PageFactory.initElements(driver, this)` do?** It assigns lazy proxies to the annotated `WebElement` fields of the object.
5. **When is the element actually looked up in Page Factory?** Each time a method is called on the field, not when the page object is created.
6. **When is `@CacheLookup` safe?** Only for elements that never get re-rendered, such as a static logo.
7. **Why are dynamic locators awkward with Page Factory?** `@FindBy` values are constants; run-time data cannot be inserted.
8. **Is Page Factory guaranteed to stay in Selenium?** Not guaranteed; its status may change in newer versions, so check the release notes of your version.

---

## Summary

- Without structure, UI changes break many tests at once; the **Page Object Model** puts each page's **locators and actions** in one class so tests stay short, readable, and stable.
- Good page objects: private locators, intention-revealing action methods, **no assertions**, return the **next page object** (or `this`), internal waits, small focused classes, and reusable **components**.
- A **`BasePage`** supplies the shared driver, waits, and helper methods.
- Choose stable locators (`data-test`, `id`, short CSS), parameterise locators for dynamic data, and locate at the moment of use to avoid stale elements.
- **Page Factory** declares elements with `@FindBy` and initialises them with `PageFactory.initElements`; proxies look up elements **lazily** on each use; `@CacheLookup` is for static elements only; lists, `@FindAll`, and `@FindBys` extend it.
- Plain `By`-based POM handles dynamic locators and waits more naturally; Page Factory is compact and common in existing code, but check your Selenium version's release notes because its status may change.
- Use a clean package layout (`pages`, `tests`, `utils`, `drivers`); this is the backbone of Project 2.
- Thursday's BDD step definitions will simply call these page objects, so the Gherkin layer stays free of Selenium details (covered in depth on Thursday).

---

## Additional Resources

- Selenium documentation, *Page object models*: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
- Martin Fowler, *PageObject* (the original description of the pattern): https://martinfowler.com/bliki/PageObject.html
- Selenium Java API, `PageFactory`: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/support/PageFactory.html
