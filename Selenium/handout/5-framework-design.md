# Selenium In-Class Handout, Group 5: Framework Design

**Topics:** 5.1 Screenshots · 5.2 Page Object Model and Page Factory

**How to use this handout:** the same layout as Handouts 1–4. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Handouts 1–4:** every example is a JUnit test class that `extends BaseTest`. You can find elements, interact, wait, and handle dialogs and windows. **This handout turns those skills into a small test framework:** tests that save a picture of the screen when they fail, and page classes that keep locators out of your tests.

**Practice site:** Swag Labs `https://www.saucedemo.com` (login: `standard_user` / `secret_sauce`).

---

## 5.1 Screenshots

### Definition

A **screenshot** is a picture of what the browser was showing at a moment during a test. When a test fails, especially on a build server where nobody is watching, the screenshot is the quickest way to see **what went wrong**. In Selenium, the driver can take a screenshot because it implements the `TakesScreenshot` interface: you cast the driver to `TakesScreenshot` and call `getScreenshotAs(...)`. A single `WebElement` can also take a screenshot of **just itself**. Selenium only captures the image; choosing a file name and saving the file is up to you.

### Key terms

| Term | Meaning |
|---|---|
| **`TakesScreenshot`** | The interface that gives a driver the `getScreenshotAs(...)` method |
| **`OutputType.FILE`** | Returns the image as a temporary `File`, which you then copy to where you want it |
| **`OutputType.BYTES`** / **`BASE64`** | Returns the image as bytes / as text (used by reports) |
| **Viewport** | The visible part of the page. A page screenshot shows the viewport, not the whole scrolled page. |
| **Element screenshot** | `element.getScreenshotAs(OutputType.FILE)`: a picture of one element only |
| **Evidence on failure** | Saving a screenshot automatically whenever a test fails |

### Key ideas

- The basic recipe is three lines: **take** the screenshot → choose a **path** → **copy** the file there.
- Use **meaningful file names** (the test's name, the page) so you know which picture belongs to which failure.
- Evidence must be captured **before** the browser quits. A JUnit **extension** can do this for every test automatically.

### Worked example: `ScreenshotTest`, then screenshots on failure

**Step 1: Take a page screenshot and save it.** The temporary file is copied into a `screenshots` folder in your project.

```java
@Test
void saveAPageScreenshot() throws IOException {
    driver.get("https://www.saucedemo.com/");

    File source = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
    Path target = Path.of("screenshots", "login-page.png");
    Files.createDirectories(target.getParent());
    Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);

    assertTrue(Files.exists(target));
}
```

**Step 2: An element screenshot.** Click **Login** with empty boxes to show the red error banner, then capture just the banner.

```java
@Test
void saveAnElementScreenshot() throws IOException {
    driver.get("https://www.saucedemo.com/");
    driver.findElement(By.id("login-button")).click();
    WebElement error = driver.findElement(By.cssSelector("[data-test='error']"));

    File source = error.getScreenshotAs(OutputType.FILE);
    Path target = Path.of("screenshots", "login-error.png");
    Files.createDirectories(target.getParent());
    Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);

    assertTrue(Files.exists(target));
}
```

Open both files from the `screenshots` folder: the first shows the whole login page, the second only the error banner.

**Step 3: Screenshots on failure, for every test.** A JUnit **extension** is a class that JUnit calls at certain moments. `AfterTestExecutionCallback` is called right after each test method, **before** `@AfterEach` quits the browser. If the test failed, it saves a screenshot named after the test.

```java
public class ScreenshotOnFailure implements AfterTestExecutionCallback {

    @Override
    public void afterTestExecution(ExtensionContext context) throws Exception {
        if (context.getExecutionException().isPresent()) {             // did the test fail?
            BaseTest test = (BaseTest) context.getRequiredTestInstance();
            File source = ((TakesScreenshot) test.driver).getScreenshotAs(OutputType.FILE);
            Path target = Path.of("screenshots", context.getRequiredTestMethod().getName() + ".png");
            Files.createDirectories(target.getParent());
            Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Screenshot saved: " + target);
        }
    }
}
```

**Step 4: Switch the extension on in `BaseTest`.** One annotation, and every test class that extends `BaseTest` gets it.

```java
@ExtendWith(ScreenshotOnFailure.class)
public abstract class BaseTest {
    // ... unchanged ...
}
```

**Step 5: See it work.** In `FirstTest` (Handout 1), change `"Swag Labs"` to `"Swag Lab"` and run it. The test fails, and `screenshots/titleIsSwagLabs.png` appears. Put the title back.

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/ScreenshotTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebElement;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ScreenshotTest extends BaseTest {

    @Test
    void saveAPageScreenshot() throws IOException {
        driver.get("https://www.saucedemo.com/");

        File source = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
        Path target = Path.of("screenshots", "login-page.png");
        Files.createDirectories(target.getParent());
        Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);

        assertTrue(Files.exists(target));
    }

    @Test
    void saveAnElementScreenshot() throws IOException {
        driver.get("https://www.saucedemo.com/");
        driver.findElement(By.id("login-button")).click();
        WebElement error = driver.findElement(By.cssSelector("[data-test='error']"));

        File source = error.getScreenshotAs(OutputType.FILE);
        Path target = Path.of("screenshots", "login-error.png");
        Files.createDirectories(target.getParent());
        Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);

        assertTrue(Files.exists(target));
    }
}
```

```java
// src/test/java/com/qea/selenium/tests/ScreenshotOnFailure.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

/** Saves a screenshot named after the test whenever a test fails, before the browser quits. */
public class ScreenshotOnFailure implements AfterTestExecutionCallback {

    @Override
    public void afterTestExecution(ExtensionContext context) throws Exception {
        if (context.getExecutionException().isPresent()) {
            BaseTest test = (BaseTest) context.getRequiredTestInstance();
            File source = ((TakesScreenshot) test.driver).getScreenshotAs(OutputType.FILE);
            Path target = Path.of("screenshots", context.getRequiredTestMethod().getName() + ".png");
            Files.createDirectories(target.getParent());
            Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Screenshot saved: " + target);
        }
    }
}
```

```java
// src/test/java/com/qea/selenium/tests/BaseTest.java   (final version)
package com.qea.selenium.tests;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/** Every UI test class extends this: a fresh browser per test, a screenshot if it fails, quit after it. */
@ExtendWith(ScreenshotOnFailure.class)
public abstract class BaseTest {

    protected WebDriver driver;

    @BeforeEach
    void startBrowser() {
        driver = new ChromeDriver();
    }

    @AfterEach
    void stopBrowser() {
        driver.quit();
    }
}
```

### Checkpoint

```text
✔ ScreenshotTest
   ✔ saveAPageScreenshot()
   ✔ saveAnElementScreenshot()
```

Your project now has a `screenshots` folder with `login-page.png` and `login-error.png`. After step 5 (the deliberate failure), the console shows `Screenshot saved: screenshots/titleIsSwagLabs.png`, and that file shows the Swag Labs login page.

### Your turn

1. Take a screenshot of the Swag Labs **logo** only (`By.className("login_logo")`) and save it as `logo.png`.
2. Log in as `standard_user` and save a screenshot of the products page as `products.png`.
3. Make `WaitTest` (Handout 3) fail by changing the expected text to `"Hello World"` (no `!`). Which screenshot appears, and what does it show?
4. Why must the screenshot be taken **before** `@AfterEach` runs? What would happen if we tried afterwards?

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoSuchFileException` when copying | The `screenshots` folder doesn't exist | `Files.createDirectories(target.getParent())` first |
| `FileAlreadyExistsException` | A file with that name is already there | Add `StandardCopyOption.REPLACE_EXISTING` |
| No screenshot when a test fails | `@ExtendWith(ScreenshotOnFailure.class)` missing from `BaseTest` | Add the annotation |
| Can't find the file | It's saved relative to the project folder | Look in `<project>/screenshots` |
| `UnhandledAlertException` while capturing | A JavaScript dialog is open; it can't be captured | Handle the dialog first (Handout 4) |

---

## 5.2 Page Object Model and Page Factory

### Definition

The **Page Object Model (POM)** is a design pattern in which every page of the application gets its own Java class, a **page object**. The page object holds that page's **locators** and offers **methods** for what a user can do there, such as `loginAs(user, password)`. Tests then call those methods instead of using `By` and `findElement` directly, so they read like a description of user behaviour, and when the page changes you fix **one** class instead of every test. A method that takes the user to another page **returns the page object** for that page. **Page Factory** is Selenium's annotation-based way of writing page objects, using `@FindBy` and `PageFactory.initElements(...)`.

### Key terms

| Term | Meaning |
|---|---|
| **Page object** | A class for one page: its locators (private) and its actions (public methods) |
| **Page method** | An action in the user's words, e.g. `loginAs(...)`, `addToCart(...)`, `cartCount()` |
| **Page Factory** | A Selenium feature that fills `WebElement` fields for you |
| **`@FindBy(id = "...")`** | Annotation on a `WebElement` field that says how to find it |
| **`PageFactory.initElements(driver, this)`** | Called in the constructor; connects the `@FindBy` fields to the page |

### Key ideas

| Rule | Why |
|---|---|
| Locators are `private` inside the page | Tests can't depend on them; a change is fixed in one place |
| Method names describe **what the user does** | `loginAs(...)`, not `clickButton3()` |
| A method that changes page **returns the next page object** | `loginAs(...)` returns an `InventoryPage` |
| **Assertions stay in tests**, not in page objects | Pages report what they see; tests decide pass or fail |

### Worked example: page objects for Swag Labs

Page objects are only used by tests, so they live with the tests, in `src/test/java/com/qea/selenium/pages`.

**Step 1: The test before POM.** It works, but every locator is inside the test. If the login button's id changes, every test that logs in must be edited.

```java
@Test
void loginWithoutPageObjects() {
    driver.get("https://www.saucedemo.com/");
    driver.findElement(By.id("user-name")).sendKeys("standard_user");
    driver.findElement(By.id("password")).sendKeys("secret_sauce");
    driver.findElement(By.id("login-button")).click();
    assertEquals("Products", driver.findElement(By.cssSelector("[data-test='title']")).getText());
}
```

**Step 2: `LoginPage`: locators become private fields, actions become methods.**

```java
public class LoginPage {

    private final WebDriver driver;
    private final By username = By.id("user-name");
    private final By password = By.id("password");
    private final By loginButton = By.id("login-button");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public LoginPage open() {
        driver.get("https://www.saucedemo.com/");
        return this;
    }

    public InventoryPage loginAs(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
        driver.findElement(loginButton).click();
        return new InventoryPage(driver);              // login takes the user to the products page
    }
}
```

**Step 3: `InventoryPage`.** It waits for the page title, because the products page appears a moment after the click (Handout 3).

```java
public class InventoryPage {

    private final WebDriver driver;
    private final By title = By.cssSelector("[data-test='title']");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");

    public InventoryPage(WebDriver driver) {
        this.driver = driver;
    }

    public String title() {
        return new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(title))
                .getText();
    }

    public InventoryPage addToCart(String buttonId) {
        driver.findElement(By.id(buttonId)).click();
        return this;
    }

    public int cartCount() {
        List<WebElement> badge = driver.findElements(cartBadge);
        return badge.isEmpty() ? 0 : Integer.parseInt(badge.get(0).getText());
    }
}
```

**Step 4: The same test, after POM.** No locators, and it reads like the requirement.

```java
@Test
void standardUserSeesProducts() {
    InventoryPage inventory = new LoginPage(driver).open().loginAs("standard_user", "secret_sauce");
    assertEquals("Products", inventory.title());
}
```

**Step 5: Reuse the pages for a second test.**

```java
@Test
void addingTheBackpackShowsOneInTheCart() {
    InventoryPage inventory = new LoginPage(driver).open().loginAs("standard_user", "secret_sauce");
    assertEquals("Products", inventory.title());          // wait until the products page is there

    inventory.addToCart("add-to-cart-sauce-labs-backpack");
    assertEquals(1, inventory.cartCount());
}
```

**Step 6: The same `LoginPage`, written with Page Factory.** Each field is a `WebElement` with a `@FindBy` annotation; `initElements` fills them in.

```java
public class LoginPageFactory {

    private final WebDriver driver;

    @FindBy(id = "user-name")
    private WebElement username;

    @FindBy(id = "password")
    private WebElement password;

    @FindBy(id = "login-button")
    private WebElement loginButton;

    public LoginPageFactory(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public LoginPageFactory open() {
        driver.get("https://www.saucedemo.com/");
        return this;
    }

    public InventoryPage loginAs(String user, String pass) {
        username.sendKeys(user);
        password.sendKeys(pass);
        loginButton.click();
        return new InventoryPage(driver);
    }
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/pages/LoginPage.java
package com.qea.selenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/** The Swag Labs login page. */
public class LoginPage {

    private final WebDriver driver;
    private final By username = By.id("user-name");
    private final By password = By.id("password");
    private final By loginButton = By.id("login-button");
    private final By errorMessage = By.cssSelector("[data-test='error']");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public LoginPage open() {
        driver.get("https://www.saucedemo.com/");
        return this;
    }

    /** A successful login: the user ends up on the products page. */
    public InventoryPage loginAs(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
        driver.findElement(loginButton).click();
        return new InventoryPage(driver);
    }

    /** A login that should fail: the user stays on the login page. */
    public LoginPage loginExpectingError(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
        driver.findElement(loginButton).click();
        return this;
    }

    public String errorMessage() {
        return driver.findElement(errorMessage).getText();
    }
}
```

```java
// src/test/java/com/qea/selenium/pages/InventoryPage.java
package com.qea.selenium.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

/** The Swag Labs products page. */
public class InventoryPage {

    private final WebDriver driver;
    private final By title = By.cssSelector("[data-test='title']");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");

    public InventoryPage(WebDriver driver) {
        this.driver = driver;
    }

    public String title() {
        return new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(title))
                .getText();
    }

    public InventoryPage addToCart(String buttonId) {
        driver.findElement(By.id(buttonId)).click();
        return this;
    }

    /** 0 when the badge is not shown: an empty cart is a valid answer. */
    public int cartCount() {
        List<WebElement> badge = driver.findElements(cartBadge);
        return badge.isEmpty() ? 0 : Integer.parseInt(badge.get(0).getText());
    }
}
```

```java
// src/test/java/com/qea/selenium/pages/LoginPageFactory.java
package com.qea.selenium.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/** The same login page, written with Page Factory. */
public class LoginPageFactory {

    private final WebDriver driver;

    @FindBy(id = "user-name")
    private WebElement username;

    @FindBy(id = "password")
    private WebElement password;

    @FindBy(id = "login-button")
    private WebElement loginButton;

    public LoginPageFactory(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public LoginPageFactory open() {
        driver.get("https://www.saucedemo.com/");
        return this;
    }

    public InventoryPage loginAs(String user, String pass) {
        username.sendKeys(user);
        password.sendKeys(pass);
        loginButton.click();
        return new InventoryPage(driver);
    }
}
```

```java
// src/test/java/com/qea/selenium/tests/PageObjectTest.java
package com.qea.selenium.tests;

import com.qea.selenium.pages.InventoryPage;
import com.qea.selenium.pages.LoginPage;
import com.qea.selenium.pages.LoginPageFactory;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PageObjectTest extends BaseTest {

    @Test
    void standardUserSeesProducts() {
        InventoryPage inventory = new LoginPage(driver).open().loginAs("standard_user", "secret_sauce");
        assertEquals("Products", inventory.title());
    }

    @Test
    void addingTheBackpackShowsOneInTheCart() {
        InventoryPage inventory = new LoginPage(driver).open().loginAs("standard_user", "secret_sauce");
        assertEquals("Products", inventory.title());

        inventory.addToCart("add-to-cart-sauce-labs-backpack");
        assertEquals(1, inventory.cartCount());
    }

    @Test
    void lockedOutUserSeesAnError() {
        LoginPage login = new LoginPage(driver).open().loginExpectingError("locked_out_user", "secret_sauce");
        assertEquals("Epic sadface: Sorry, this user has been locked out.", login.errorMessage());
    }

    @Test
    void pageFactoryLoginWorksTheSame() {
        InventoryPage inventory = new LoginPageFactory(driver).open().loginAs("standard_user", "secret_sauce");
        assertEquals("Products", inventory.title());
    }
}
```

### Checkpoint

```text
✔ PageObjectTest
   ✔ standardUserSeesProducts()
   ✔ addingTheBackpackShowsOneInTheCart()
   ✔ lockedOutUserSeesAnError()
   ✔ pageFactoryLoginWorksTheSame()
```

Now try the point of POM: in `LoginPage`, change `By.id("login-button")` to `By.id("login-btn")` and run. Three tests fail, and the fix is **one line in one file**. Put it back.

### Your turn

1. Add `lockedOutUser` to the Page Factory version: give `LoginPageFactory` an `@FindBy` field for the error message and a `loginExpectingError` method, and write the test.
2. Add `removeFromCart(String buttonId)` to `InventoryPage` and a test: add the Backpack, remove it (`remove-sauce-labs-backpack`), and check `cartCount()` is 0.
3. Write a test for the wrong password case (`standard_user` / `wrong`): the error is `Epic sadface: Username and password do not match any user in this service`.
4. **Stretch:** create a `CartPage` with an `itemNames()` method that returns a `List<String>` of the product names in the cart (`[data-test='inventory-item-name']`). Add `openCart()` to `InventoryPage` (click `[data-test='shopping-cart-link']`, return a `CartPage`) and test that the Backpack is listed.

### Common errors

| You see | Why | Fix |
|---|---|---|
| Locators duplicated in tests and pages | Some test still uses `By` directly | Move every locator into its page object |
| `assertEquals` inside a page object | The page is deciding pass/fail | Return the value; assert in the test |
| `NullPointerException` on a `@FindBy` field | `PageFactory.initElements(driver, this)` missing in the constructor | Add it |
| `StaleElementReferenceException` with Page Factory | `@CacheLookup` kept an element the page has since replaced | Don't use `@CacheLookup` on elements that change |
| `NoSuchElementException` right after `loginAs` | The products page wasn't there yet | Wait in the page method (as `title()` does) |

---

**End of Handout 5 and the Selenium block.** You can save screenshots, capture evidence automatically when a test fails, and organise tests with page objects, written with `By` locators or with Page Factory. **Next:** BDD and Cucumber, where scenarios in plain English call these page objects.
