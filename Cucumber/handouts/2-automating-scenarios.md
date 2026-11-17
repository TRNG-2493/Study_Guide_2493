# Cucumber In-Class Handout 2: Automating Scenarios

**Topics:** 2.1 Given/When/Then · 2.2 Cucumber framework setup · 2.3 Step definitions

**How to use this handout:** the same layout as before. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on:** Cucumber Handout 1 (the feature files `login.feature`, `cart.feature`, `sorting.feature`) and the Selenium handouts (the Maven project, JUnit, `BaseTest`, and the page objects `LoginPage` and `InventoryPage` from Selenium Handout 5).

> **Order note:** the full notes teach *Cucumber framework setup* last on Thursday. Here it comes **before** step definitions, so you can run every step as soon as you write it.

---

## 2.1 Given/When/Then

### Definition

**Given/When/Then** is the structure of every scenario. **Given** describes the starting situation (the **context**) and puts the system into a known state. **When** describes the **action** or event the scenario is about, normally one per scenario. **Then** describes the expected **outcome**, something a user can observe. `And` and `But` continue whichever kind of step came before them. When Cucumber looks for the code behind a step, it **ignores the keyword** and matches only the text after it.

### Key terms

| Keyword | Answers the question | Good example | Wrong for this keyword |
|---|---|---|---|
| **Given** | What is already true? | `Given I am logged in as "standard_user"` | `Given I click Login` (an action) |
| **When** | What does the user do? | `When I add "Sauce Labs Onesie" to the cart` | `When I add X and open the cart and check out` (several actions) |
| **Then** | What can the user see now? | `Then the cart badge should show 1` | `Then the database contains the order` (invisible to the user) |
| **And / But** | Continues the previous step's kind | `And I add "Sauce Labs Bike Light" to the cart` | |

**Other terms:**

- **Step text:** everything after the keyword, e.g. `I add "Sauce Labs Onesie" to the cart`.
- **Parameter:** a value in a step that can change, such as `"Sauce Labs Onesie"` or `2`. One step definition serves every value.
- **Step definition:** the Java method that runs a step (topic 2.3).

### Key ideas

- Each step will call **one short Java method**, which calls a **page object**, which drives the **browser**. Plan this chain before writing code.
- Because the keyword is ignored, `Given I add "X" to the cart` and `When I add "X" to the cart` run the **same** code. Phrase preconditions in the past tense ("I have added") so scenarios read well.
- Put changing values in **quotes** (text) or as **numbers**, so the step can be reused.

### Worked example: tracing a cart scenario through the layers

**Step 1: Start from one scenario** in `cart.feature`.

```gherkin
Scenario: Adding products shows the count on the cart badge
  Given I am logged in as "standard_user"
  When I add "Sauce Labs Backpack" to the cart
  And I add "Sauce Labs Bike Light" to the cart
  Then the cart badge should show 2
```

**Step 2: Check the shape.** One `Given` (context), one kind of action (`When` + `And`), one `Then` (visible outcome). ✔

**Step 3: Find the parameters** that will become method arguments.

| Step text | Parameter |
|---|---|
| `I am logged in as "standard_user"` | username: `"standard_user"` |
| `I add "Sauce Labs Backpack" to the cart` | product name: `"Sauce Labs Backpack"` |
| `the cart badge should show 2` | count: `2` |

**Step 4: Trace each step down to the browser** before writing any code.

| Gherkin step | Step definition (2.3) | Page object call | What the browser does |
|---|---|---|---|
| `Given I am logged in as "standard_user"` | `iAmLoggedInAs("standard_user")` | `loginPage.open().loginAs(...)` | Opens Swag Labs, types, clicks Login |
| `When I add "Sauce Labs Backpack" to the cart` | `iAddToTheCart("Sauce Labs Backpack")` | `inventory.addProductToCart(...)` | Clicks that product's *Add to cart* |
| `Then the cart badge should show 2` | `theCartBadgeShouldShow(2)` | `inventory.cartCount()` | Reads the badge |

### Checkpoint

You have a four-column trace table for the scenario, and none of the Gherkin steps mention a locator, id or CSS class.

### Your turn

1. Classify each step as a good **Given**, **When** or **Then**, or as wrong for its keyword: (a) `Given I click "Add to cart"`; (b) `When I sort the products by "Price (low to high)"`; (c) `Then the first product should be "Sauce Labs Onesie"`; (d) `Then the sort() method is called`.
2. Build the trace table for "Removing the only product hides the badge" from `cart.feature`.
3. `Given I have added "Sauce Labs Onesie" to the cart` and `When I add "Sauce Labs Onesie" to the cart` do the same thing. Will Cucumber need one step definition or two? Why?

### Common errors

| Mistake | Symptom | Fix |
|---|---|---|
| Actions in a `Given` ("Given I click ...") | The scenario reads like a script | Describe the resulting state ("Given I am logged in") |
| Several unrelated `When`s | Unclear what the scenario is about | One behaviour per scenario |
| `Then` checks something the user can't see | Business readers can't verify it | Check what is shown on screen |
| Two wordings for the same thing ("add" / "put in") | Duplicate step definitions | Agree one wording and reuse it |

---

## 2.2 Cucumber Framework Setup

### Definition

**Cucumber** is an open-source tool that **runs Gherkin scenarios as automated tests**. It reads the `.feature` files, matches each step to a Java method (a **step definition**), runs those methods in order, and reports which steps passed and failed. Cucumber was created in 2008 for Ruby; **Cucumber-JVM** is the version for Java. Cucumber itself does not drive a browser: our step definitions call the **Selenium** page objects for that and use **JUnit** assertions to check results, and Cucumber runs **through JUnit**, so scenarios run with `mvn test` and the IDE's Run button, like the Selenium tests. Setting Cucumber up means adding its dependencies, putting feature files and step definitions in the right folders, and telling Cucumber where they are.

### Key terms

| Term | Meaning |
|---|---|
| **Cucumber-JVM** | Cucumber for Java. Added with the `cucumber-java` dependency. |
| **Cucumber engine** | `cucumber-junit-platform-engine`: lets JUnit run feature files |
| **Suite class** | An empty test class with annotations that tells JUnit to run the feature files: `RunCucumberTest` |
| **Glue** | The Java package where Cucumber looks for step definitions |
| **`@ConfigurationParameter`** | An annotation on the suite class that gives Cucumber one setting: a **key** (e.g. the glue) and a **value** |
| **Plugin** | A Cucumber output: `pretty` prints each step in colour, `summary` prints the totals |
| **Snippet** | Ready-to-paste Java that Cucumber prints for a step without a step definition |

**Where everything goes** (all of it is test code, so all of it is under `src/test`):

```text
src/test/java/com/qea/selenium/
├── RunCucumberTest.java     tells JUnit to run the feature files, with Cucumber's settings
├── pages/                   page objects (from Selenium Handout 5)
└── steps/                   step definitions: BaseSteps, LoginSteps, CartSteps, SortSteps
src/test/resources/
└── features/              login.feature, cart.feature, sorting.feature
```

### Key ideas

- **One step file per area** (`LoginSteps`, `CartSteps`, `SortSteps`), like one page object per page.
- The step classes share **one browser** through a parent class, `BaseSteps`, the Cucumber version of `BaseTest`.
- Run Cucumber, read the **undefined** steps it reports, and paste its **snippets** as the start of your step definitions.

### Worked example: a running Cucumber project

**Step 1: The complete `pom.xml`.** It has everything the project needs: Selenium (from the Selenium handouts), JUnit, and the three new Cucumber dependencies marked **NEW**.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.qea</groupId>
    <artifactId>selenium-week6</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <selenium.version>4.51.0</selenium.version>
        <junit.version>6.1.3</junit.version>
        <cucumber.version>8.0.4</cucumber.version>                <!-- NEW -->
    </properties>

    <dependencies>
        <!-- Selenium: controls the browser -->
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>${selenium.version}</version>
        </dependency>

        <!-- JUnit: @Test, assertions such as assertEquals, and the engine that runs @Test methods -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- NEW: JUnit suites (@Suite, @IncludeEngines, @SelectPackages) -->
        <dependency>
            <groupId>org.junit.platform</groupId>
            <artifactId>junit-platform-suite</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- NEW: Cucumber for Java: reads feature files, @Given/@When/@Then -->
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-java</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- NEW: lets JUnit run Cucumber scenarios -->
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-junit-platform-engine</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Runs the tests (JUnit tests and Cucumber scenarios) with: mvn test -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.6.0</version>
            </plugin>
        </plugins>
    </build>
</project>
```

| Dependency | What it gives you |
|---|---|
| `selenium-java` | `WebDriver`, `ChromeDriver`, `By`, waits: everything for the browser |
| `junit-jupiter` | `@Test` and assertions such as `assertEquals`, used in the `Then` steps |
| `junit-platform-suite` | The suite annotations used by `RunCucumberTest` |
| `cucumber-java` | Reads feature files; `@Given`, `@When`, `@Then` |
| `cucumber-junit-platform-engine` | Connects Cucumber to JUnit, so scenarios run with `mvn test` and the IDE |

Keep `cucumber-java` and `cucumber-junit-platform-engine` on the **same** version (`${cucumber.version}`), and both JUnit dependencies on `${junit.version}`. After saving the file, accept VS Code's prompt to **synchronize the Java classpath**, so the new libraries are loaded.

**Step 2: Create the folders** shown above. Move your three feature files into `src/test/resources/features`, and the page objects into `src/test/java/com/qea/selenium/pages`.

**Step 3: The suite class.** It has no code. The first three annotations say: "use the Cucumber engine, and run the feature files in the `features` folder".

```java
@Suite
@IncludeEngines("cucumber")
@SelectPackages("features")
public class RunCucumberTest {
}
```

**Step 4: Give Cucumber its settings** with `@ConfigurationParameter`: where the step definitions are (**glue**), what to print (**plugins**), and the style of the snippets. The keys come from Cucumber's `Constants` class.

```java
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.qea.selenium.steps")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty, summary")
@ConfigurationParameter(key = SNIPPET_TYPE_PROPERTY_NAME, value = "camelcase")
```

Add these three lines under `@SelectPackages("features")`. (Complete code below.)

**Step 5: `BaseSteps`: the shared browser.** Every step class will extend it, just as every test class extends `BaseTest`. `static` means all step classes share the same `driver`.

```java
public class BaseSteps {

    protected static WebDriver driver;

    protected void openBrowser() {
        driver = new ChromeDriver();
    }

    protected void closeBrowser() {
        driver.quit();
    }
}
```

**Step 6: Add the methods the steps will need to the page objects.** `InventoryPage` gets methods that take a **product name** (as written in the feature files), plus remove, open-cart, sort and first-product methods. There is also a new `CartPage`. (Complete code below.)

**Step 7: Run it.** Click the green ▷ in the margin next to `RunCucumberTest`, or from VS Code's terminal:

```bash
mvn test -Dtest=RunCucumberTest
```

No step definitions exist yet, so expect **undefined** steps and snippets.

**Complete code**

```java
// src/test/java/com/qea/selenium/RunCucumberTest.java
package com.qea.selenium;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.SNIPPET_TYPE_PROPERTY_NAME;

/** Runs every feature file in src/test/resources/features with Cucumber. */
@Suite
@IncludeEngines("cucumber")
@SelectPackages("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.qea.selenium.steps")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty, summary")
@ConfigurationParameter(key = SNIPPET_TYPE_PROPERTY_NAME, value = "camelcase")
public class RunCucumberTest {
}
```

```java
// src/test/java/com/qea/selenium/steps/BaseSteps.java
package com.qea.selenium.steps;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/** Parent of every step class: holds the one browser they all share. */
public class BaseSteps {

    protected static WebDriver driver;

    protected void openBrowser() {
        driver = new ChromeDriver();
    }

    protected void closeBrowser() {
        driver.quit();
    }
}
```

```java
// src/test/java/com/qea/selenium/pages/InventoryPage.java   (Selenium Handout 5 version + new methods)
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
    private final By title = By.cssSelector("[data-test='title']");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");
    private final By cartLink = By.cssSelector("[data-test='shopping-cart-link']");
    private final By sortMenu = By.cssSelector("[data-test='product-sort-container']");
    private final By productNames = By.cssSelector("[data-test='inventory-item-name']");

    /** Waits until the products page is shown, so every method can be used straight away. */
    public InventoryPage(WebDriver driver) {
        this.driver = driver;
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.urlContains("inventory"));
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

    /** "Sauce Labs Backpack" -> clicks the button with id "add-to-cart-sauce-labs-backpack". */
    public InventoryPage addProductToCart(String productName) {
        return addToCart("add-to-cart-" + idPart(productName));
    }

    /** "Sauce Labs Onesie" -> clicks the button with id "remove-sauce-labs-onesie". */
    public InventoryPage removeProductFromCart(String productName) {
        driver.findElement(By.id("remove-" + idPart(productName))).click();
        return this;
    }

    public int cartCount() {
        List<WebElement> badge = driver.findElements(cartBadge);
        return badge.isEmpty() ? 0 : Integer.parseInt(badge.get(0).getText());
    }

    public CartPage openCart() {
        driver.findElement(cartLink).click();
        return new CartPage(driver);
    }

    /** Sorts by the visible text of the sort menu, e.g. "Price (low to high)". */
    public InventoryPage sortBy(String label) {
        new Select(driver.findElement(sortMenu)).selectByVisibleText(label);
        return this;
    }

    public String firstProductName() {
        return driver.findElements(productNames).get(0).getText();
    }

    /** Swag Labs builds button ids from the product name in lower case, with spaces as dashes. */
    private static String idPart(String productName) {
        return productName.toLowerCase().replace(" ", "-");
    }
}
```

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

### Checkpoint

No browser opens yet. Cucumber reports every step as **undefined**, and the `summary` output ends with snippets:

```text
Scenario: Standard user logs in                                   # classpath:features/login.feature:6
  ■ Given I am on the Swag Labs login page
  ↷ When I log in as "standard_user" with password "secret_sauce"
  ↷ Then I should see the "Products" page
...
8 scenarios (8 undefined)

You can implement missing steps with the snippets below:

@Given("I am on the Swag Labs login page")
public void iAmOnTheSwagLabsLoginPage() {
    // Write code here that turns the phrase above into concrete actions
    throw new io.cucumber.java.PendingException();
}
...
```

■ means **undefined**; ↷ means **skipped** (an earlier step didn't pass). The scenarios are not green in the IDE yet; that is expected.

### Your turn

1. Run only the login feature: `mvn test -Dtest=RunCucumberTest -Dcucumber.features=src/test/resources/features/login.feature`. How many scenarios are reported?
2. Do a **dry run**, which checks the steps without opening a browser: `mvn test -Dtest=RunCucumberTest -Dcucumber.execution.dry-run=true`. How long does it take compared with a normal run?
3. After you have written a step definition in 2.3, change the glue value to `com.qea.selenium.step` (no "s"). What happens to it? Put it back.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `Tests run: 0` | `cucumber-junit-platform-engine` is missing, or `@IncludeEngines("cucumber")` is missing | Check the `pom.xml` and the suite class |
| "No features found" | Feature files not in `src/test/resources/features` | Move them; `@SelectPackages("features")` must match the folder name |
| Every step undefined even after writing step definitions | The glue value doesn't match the package of the step classes | Make the package names identical |
| Red underlines under `@Given` in VS Code | The new dependencies weren't loaded | Accept the "synchronize classpath" prompt, or run **Java: Clean Java Language Server Workspace** |

---

## 2.3 Step Definitions

### Definition

A **step definition** is a Java method that runs one kind of Gherkin step. It is marked with `@Given`, `@When` or `@Then` and contains a **Cucumber Expression**: the step text, with placeholders such as `{string}` or `{int}` for the parameters. When a scenario runs, Cucumber finds the method whose expression matches each step, passes the parameter values to it, and runs it. Step definitions should stay **thin**: a line or two that calls page objects, plus a JUnit **assertion** in `Then` steps. They live in the **glue** package, in classes such as `LoginSteps`.

### Key terms

**Cucumber Expressions:**

| Placeholder | Matches in the step | Java parameter |
|---|---|---|
| `{string}` | Text in double quotes: `"standard_user"` | `String` (without the quotes) |
| `{int}` | A whole number: `2` | `int` |
| `{bigdecimal}` | A decimal number: `29.99` | `BigDecimal` |
| `{word}` | One word without spaces | `String` |

**Step results:**

| Symbol | Result | Meaning |
|---|---|---|
| ✔ | **passed** | The method ran without an exception |
| ✘ | **failed** | The method threw an exception (often a failed assertion) |
| ↷ | **skipped** | An earlier step in the scenario didn't pass |
| ■ | **undefined** | No step definition matches the step |
| | **ambiguous** | More than one step definition matches |

**Other terms:**

- **Data table argument:** a one-column table under a step arrives as `List<String>`.
- **Thin step definition:** calls page objects; contains no locators or waits.

### Key ideas

- Start from Cucumber's **snippet**, then replace the `throw new PendingException()` line with page object calls.
- **The browser, for now:** the **first** step of every scenario (`I am on the Swag Labs login page` / `I am logged in as ...`) opens the browser, and the **last** step, always one `Then` in our scenarios, closes it. A `Then` step reads the value, closes the browser, **then** asserts, so the browser is closed even when the check fails. Cucumber Handout 3 replaces this with **hooks**.
- One step definition serves every scenario whose step text matches, so `iAddToTheCart` handles every product.

### Worked example: `LoginSteps`, `CartSteps` and `SortSteps`

**Step 1: Paste the first snippet and make it real.** Create `LoginSteps` in `com.qea.selenium.steps`, extending `BaseSteps`.

```java
public class LoginSteps extends BaseSteps {

    @Given("I am on the Swag Labs login page")
    public void iAmOnTheLoginPage() {
        openBrowser();
        new LoginPage(driver).open();
    }
}
```

Run `login.feature`. A browser opens for each scenario and the first step is **✔ passed**; the rest are still undefined. (The browsers stay open for now; step 3 closes them.)

**Step 2: A step with two `{string}` parameters.** The step doesn't know whether the login should work, so it uses `loginExpectingError`, which stays on the login page; the `Then` step decides what should be seen.

```java
@When("I log in as {string} with password {string}")
public void iLogInAs(String username, String password) {
    new LoginPage(driver).loginExpectingError(username, password);
}
```

**Step 3: `Then` steps: read, close the browser, assert.**

```java
@Then("I should see the {string} page")
public void iShouldSeeThePage(String expectedTitle) {
    String actualTitle = new InventoryPage(driver).title();
    closeBrowser();
    assertEquals(expectedTitle, actualTitle);
}

@Then("I should see the login error {string}")
public void iShouldSeeTheLoginError(String expectedMessage) {
    String actualMessage = new LoginPage(driver).errorMessage();
    closeBrowser();
    assertEquals(expectedMessage, actualMessage);
}
```

Run `login.feature` again: all three scenarios pass, and every browser closes.

**Step 4: The "logged in" step** that the cart and sorting features start from.

```java
@Given("I am logged in as {string}")
public void iAmLoggedInAs(String username) {
    openBrowser();
    new LoginPage(driver).open().loginAs(username, "secret_sauce");
}
```

**Step 5: `CartSteps`: `{int}`, a data table, and one action phrased two ways.**

```java
public class CartSteps extends BaseSteps {

    @When("I add {string} to the cart")
    public void iAddToTheCart(String product) {
        new InventoryPage(driver).addProductToCart(product);
    }

    @Given("I have added {string} to the cart")
    public void iHaveAddedToTheCart(String product) {
        iAddToTheCart(product);                // the same action, phrased as a precondition
    }

    @Given("I have added these products to the cart:")
    public void iHaveAddedTheseProducts(List<String> products) {
        for (String product : products) {
            iAddToTheCart(product);
        }
    }

    @Then("the cart badge should show {int}")
    public void theCartBadgeShouldShow(int expected) {
        int actual = new InventoryPage(driver).cartCount();
        closeBrowser();
        assertEquals(expected, actual);
    }
}
```

**Step 6: `SortSteps`.**

```java
public class SortSteps extends BaseSteps {

    @When("I sort the products by {string}")
    public void iSortTheProductsBy(String order) {
        new InventoryPage(driver).sortBy(order);
    }

    @Then("the first product should be {string}")
    public void theFirstProductShouldBe(String expected) {
        String actual = new InventoryPage(driver).firstProductName();
        closeBrowser();
        assertEquals(expected, actual);
    }
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/steps/LoginSteps.java
package com.qea.selenium.steps;

import com.qea.selenium.pages.InventoryPage;
import com.qea.selenium.pages.LoginPage;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for login.feature, plus the "logged in" step other features start from. */
public class LoginSteps extends BaseSteps {

    @Given("I am on the Swag Labs login page")
    public void iAmOnTheLoginPage() {
        openBrowser();
        new LoginPage(driver).open();
    }

    @Given("I am logged in as {string}")
    public void iAmLoggedInAs(String username) {
        openBrowser();
        new LoginPage(driver).open().loginAs(username, "secret_sauce");
    }

    @When("I log in as {string} with password {string}")
    public void iLogInAs(String username, String password) {
        new LoginPage(driver).loginExpectingError(username, password);
    }

    @Then("I should see the {string} page")
    public void iShouldSeeThePage(String expectedTitle) {
        String actualTitle = new InventoryPage(driver).title();
        closeBrowser();
        assertEquals(expectedTitle, actualTitle);
    }

    @Then("I should see the login error {string}")
    public void iShouldSeeTheLoginError(String expectedMessage) {
        String actualMessage = new LoginPage(driver).errorMessage();
        closeBrowser();
        assertEquals(expectedMessage, actualMessage);
    }
}
```

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

/** Step definitions for cart.feature. */
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
        int actual = new InventoryPage(driver).cartCount();
        closeBrowser();
        assertEquals(expected, actual);
    }

    @Then("the cart badge should not be shown")
    public void theCartBadgeShouldNotBeShown() {
        int actual = new InventoryPage(driver).cartCount();
        closeBrowser();
        assertEquals(0, actual);
    }

    @Then("the cart should contain exactly:")
    public void theCartShouldContainExactly(List<String> expected) {
        List<String> actual = new CartPage(driver).itemNames();
        closeBrowser();
        assertEquals(expected, actual);
    }
}
```

```java
// src/test/java/com/qea/selenium/steps/SortSteps.java
package com.qea.selenium.steps;

import com.qea.selenium.pages.InventoryPage;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for sorting.feature. */
public class SortSteps extends BaseSteps {

    @When("I sort the products by {string}")
    public void iSortTheProductsBy(String order) {
        new InventoryPage(driver).sortBy(order);
    }

    @Then("the first product should be {string}")
    public void theFirstProductShouldBe(String expected) {
        String actual = new InventoryPage(driver).firstProductName();
        closeBrowser();
        assertEquals(expected, actual);
    }
}
```

### Checkpoint

Run `RunCucumberTest`. A browser opens and closes for each scenario, and every step is ✔:

```text
Scenario: Locked-out user is refused                                                        # classpath:features/login.feature:11
  ✔ Given I am on the Swag Labs login page                                                  # com.qea.selenium.steps.LoginSteps.iAmOnTheLoginPage()
  ✔ When I log in as "locked_out_user" with password "secret_sauce"                         # com.qea.selenium.steps.LoginSteps.iLogInAs(java.lang.String,java.lang.String)
  ✔ Then I should see the login error "Epic sadface: Sorry, this user has been locked out." # com.qea.selenium.steps.LoginSteps.iShouldSeeTheLoginError(java.lang.String)
...
8 scenarios (8 passed)
27 steps (27 passed)

[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0
```

Each step line shows **which Java method** ran it, and JUnit counts each scenario as one test.

### Your turn

1. **Make one fail:** in `sorting.feature`, change `"Sauce Labs Onesie"` to `"Sauce Labs Backpack"`. Run it: which step fails, and what does the assertion message say? Does the browser still close? Put it back.
2. Add the scenario from Handout 1, "Name (Z to A)" puts "Test.allTheThings() T-Shirt (Red)" first. Do you need a new step definition? Why not?
3. **Ambiguous step:** in a new class, add a second method with `@When("I add {string} to the cart")`. Run, read the error, then delete it.
4. Add the "empty username" scenario from Handout 1 to `login.feature`. Which step definitions does it use?

### Common errors

| You see | Why | Fix |
|---|---|---|
| ■ undefined although the method exists | The expression text differs (even by one character), or the class isn't in the glue package | Copy the step text exactly; check the glue value in `RunCucumberTest` |
| `AmbiguousStepDefinitionsException` | Two expressions match the same step | Delete or reword one |
| `NullPointerException` on `driver` | The scenario doesn't start with a step that calls `openBrowser()` | Start with `Given I am on the Swag Labs login page` or `Given I am logged in as ...` |
| Browsers left open | A step failed before the `Then` that closes the browser | Close them by hand for now; hooks fix this in Handout 3 |
| Step definitions full of `By` and `findElement` | Logic in the wrong layer | Move it into page objects; keep steps thin |

---

**End of Cucumber Handout 2.** Cucumber runs your feature files through JUnit, and the login, cart and sorting scenarios are green. **Next:** Cucumber Handout 3, Reusable Scenarios: outlines, backgrounds, rules, and hooks that take care of the browser for you.
