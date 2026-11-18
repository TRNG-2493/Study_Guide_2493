# Cucumber In-Class Handout 2: Automating Scenarios

**Topics:** 2.1 Given/When/Then · 2.2 Cucumber framework setup · 2.3 Step definitions

**How to use this handout:** the same layout as before. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on:** Cucumber Handout 1 and the Selenium handouts (Maven, JUnit assertions, `findElement`, `sendKeys`, `click`, explicit waits).

**Which `login.feature`?** Use the **final version from Cucumber Handout 1, topic 1.4**: 4 scenarios (valid user, locked-out user, wrong password, log out). Copy it exactly; the step text must match the Java code below character for character. The step definitions in this handout use **plain Selenium** calls, so all the attention is on how Cucumber works. Page objects come back in Cucumber Handout 5.

> **Order note:** the full notes teach *Cucumber framework setup* last on Thursday. Here it comes **before** step definitions, so you can run every step as soon as you write it.

**Practice site:** Swag Labs, `https://www.saucedemo.com` (password `secret_sauce` for every user). The locators used in this handout:

| Element | Locator |
|---|---|
| Username field | `By.id("user-name")` |
| Password field | `By.id("password")` |
| Login button | `By.id("login-button")` |
| Error message | `By.cssSelector("[data-test='error']")` |
| Page title ("Products") | `By.cssSelector("[data-test='title']")` |
| Menu button (☰) | `By.id("react-burger-menu-btn")` |
| Logout link (inside the menu) | `By.id("logout_sidebar_link")` |

---

## 2.1 Given/When/Then

### Definition

**Given/When/Then** is the structure of every scenario. **Given** describes the starting situation (the **context**) and puts the system into a known state. **When** describes the **action** or event the scenario is about, normally one per scenario. **Then** describes the expected **outcome**, something a user can observe. `And` and `But` continue whichever kind of step came before them. When Cucumber looks for the code behind a step, it **ignores the keyword** and matches only the text after it.

### Key terms

| Keyword | Answers the question | Good example | Wrong for this keyword |
|---|---|---|---|
| **Given** | What is already true? | `Given I am on the login page` | `Given I click Login` (an action) |
| **When** | What does the user do? | `When I log in with username "standard_user" and password "wrong_sauce"` | `When I log in and log out` (two actions) |
| **Then** | What can the user see now? | `Then I should see the error "Epic sadface: Username and password do not match any user in this service"` | `Then the session cookie is deleted` (invisible to the user) |
| **And / But** | Continues the previous step's kind | `And I have logged in with username "standard_user" ...` | |

**Other terms:**

- **Step text:** everything after the keyword, e.g. `I log in with username "standard_user" and password "wrong_sauce"`.
- **Parameter:** a value in a step that can change, such as `"standard_user"`. One step definition serves every value.
- **Step definition:** the Java method that runs a step (topic 2.3).

### Key ideas

- Each step will call **one short Java method**, which uses **Selenium** to drive the **browser**. Plan this chain before writing code.
- Because the keyword is ignored, a `Given` and a `When` with the **same text** run the **same** method. Phrase preconditions in the past tense ("I have logged in") so scenarios read well.
- Put changing values in **quotes**, so the step can be reused with different data.

### Worked example: tracing a scenario through the layers

**Step 1: Start from one scenario** in `login.feature`.

```gherkin
Scenario: Wrong password is refused
  Given I am on the login page
  When I log in with username "standard_user" and password "wrong_sauce"
  Then I should see the error "Epic sadface: Username and password do not match any user in this service"
```

**Step 2: Check the shape.** One `Given` (context), one `When` (action), one `Then` (visible outcome). ✔

**Step 3: Find the parameters** that will become method arguments.

| Step text | Parameters |
|---|---|
| `I am on the login page` | none |
| `I log in with username "standard_user" and password "wrong_sauce"` | `"standard_user"`, `"wrong_sauce"` |
| `I should see the error "Epic sadface: Username ..."` | `"Epic sadface: Username and password do not match any user in this service"` |

**Step 4: Trace each step down to the browser** before writing any code.

| Gherkin step | Java method (2.3) | Selenium | What the browser does |
|---|---|---|---|
| `Given I am on the login page` | `iAmOnTheLoginPage()` | `new ChromeDriver()`, `driver.get(...)` | Opens Chrome on the login page |
| `When I log in with username ... and password ...` | `iLogInWith(username, password)` | `sendKeys` ×2, `click()` | Types and clicks Login |
| `Then I should see the error ...` | `iShouldSeeTheError(expectedError)` | `findElement(By.cssSelector("[data-test='error']")).getText()` | Reads the red error box |

### Checkpoint

You have a four-column trace table for the scenario, and none of the Gherkin steps mentions an id, CSS selector or "click".

### Your turn

1. Classify each step as a good **Given**, **When** or **Then**, or as wrong for its keyword: (a) `Given I click the Login button`; (b) `When I log out`; (c) `Then I should be back on the login page`; (d) `Then the logout() method is called`.
2. Build the trace table for "Logged-in user logs out" from `login.feature`.
3. `And I have logged in with username "standard_user" ...` and `When I log in with username "standard_user" ...` do the same thing but have different text. How many Java methods will they need?

### Common errors

| Mistake | Symptom | Fix |
|---|---|---|
| Actions in a `Given` ("Given I click ...") | The scenario reads like a script | Describe the resulting state ("Given I am on the login page") |
| Several unrelated `When`s | Unclear what the scenario is about | One behaviour per scenario |
| `Then` checks something the user can't see | Business readers can't verify it | Check what is shown on screen |
| Two wordings for the same thing ("log in" / "sign in") | Duplicate step definitions | Agree one wording and reuse it |

---

## 2.2 Cucumber Framework Setup

### Definition

**Cucumber** is an open-source tool that **runs Gherkin scenarios as automated tests**. It reads the `.feature` files, matches each step to a Java method (a **step definition**), runs those methods in order, and reports which steps passed and failed. Cucumber was created in 2008 for Ruby; **Cucumber-JVM** is the version for Java. Cucumber itself does not drive a browser: our step definitions use **Selenium** for that and **JUnit** assertions to check results, and Cucumber runs **through JUnit**, so scenarios run with `mvn test` and the IDE's Run button, like the Selenium tests. Setting Cucumber up means adding its dependencies, putting the feature file and step definitions in the right folders, and telling Cucumber where they are.

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
└── steps/
    └── LoginSteps.java      step definitions for login.feature (topic 2.3)
src/test/resources/
└── features/
    └── login.feature        final version from Cucumber Handout 1, topic 1.4
```

### Key ideas

- **Two files make it work:** the **feature file** (what to test, in Gherkin) and the **step class** (how, in Java). The **suite class** connects them to JUnit.
- **One step class per feature** to start: `login.feature` → `LoginSteps`.
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
| `selenium-java` | `WebDriver`, `ChromeDriver`, `By`: everything for the browser |
| `junit-jupiter` | Assertions such as `assertEquals`, used in the `Then` steps |
| `junit-platform-suite` | The suite annotations used by `RunCucumberTest` |
| `cucumber-java` | Reads feature files; `@Given`, `@When`, `@Then` |
| `cucumber-junit-platform-engine` | Connects Cucumber to JUnit, so scenarios run with `mvn test` and the IDE |

Keep the two Cucumber dependencies on the **same** version (`${cucumber.version}`), and both JUnit dependencies on `${junit.version}`. After saving the file, accept VS Code's prompt to **synchronize the Java classpath**.

**Step 2: Create the folders** shown above and put the **final** `login.feature` from Handout 1 (topic 1.4, 4 scenarios) in `src/test/resources/features`.

**Step 3: The suite class.** It has no code. The first three annotations say: "use the Cucumber engine, and run the feature files in the `features` folder".

```java
@Suite
@IncludeEngines("cucumber")
@SelectPackages("features")
public class RunCucumberTest {
}
```

**Step 4: Give Cucumber its settings** with `@ConfigurationParameter`: where the step definitions are (**glue**), what to print (**plugins**), and the style of the snippets. The keys come from Cucumber's `Constants` class. Add these lines under `@SelectPackages("features")` (complete code below):

```java
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.qea.selenium.steps")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty, summary")
@ConfigurationParameter(key = SNIPPET_TYPE_PROPERTY_NAME, value = "camelcase")
```

**Step 5: Run it.** Click the green ▷ in the margin next to `RunCucumberTest`, or from VS Code's terminal:

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

### Checkpoint

No browser opens yet. Cucumber reports every step as **undefined**, and the output ends with snippets:

```text
Scenario: Valid user logs in                                               # classpath:features/login.feature:6
  ■ Given I am on the login page
  ↷ When I log in with username "standard_user" and password "secret_sauce"
  ↷ Then I should see the "Products" page
...
4 scenarios (4 undefined)

You can implement missing steps with the snippets below:

@Given("I am on the login page")
public void iAmOnTheLoginPage() {
    // Write code here that turns the phrase above into concrete actions
    throw new io.cucumber.java.PendingException();
}
...
```

■ means **undefined**; ↷ means **skipped** (an earlier step didn't pass).

### Your turn

1. Count the snippets Cucumber printed. Why are there fewer snippets than steps in `login.feature`?
2. Do a **dry run**, which checks the steps without opening a browser: `mvn test -Dtest=RunCucumberTest -Dcucumber.execution.dry-run=true`.
3. Move `login.feature` to `src/test/resources` (outside `features`) and run again. What does Cucumber report? Move it back.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `Tests run: 0` | `cucumber-junit-platform-engine` is missing, or `@IncludeEngines("cucumber")` is missing | Check the `pom.xml` and the suite class |
| "No features found" | Feature file not in `src/test/resources/features` | Move it; `@SelectPackages("features")` must match the folder name |
| Red underlines under the Cucumber imports | The new dependencies weren't loaded | Accept the "synchronize classpath" prompt, or run **Java: Clean Java Language Server Workspace** |
| `Constants` can't be found | Wrong import | `import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;` |

---

## 2.3 Step Definitions

### Definition

A **step definition** is a Java method that runs one kind of Gherkin step. It is marked with `@Given`, `@When` or `@Then` and contains a **Cucumber Expression**: the step text, with placeholders such as `{string}` or `{int}` for the parameters. When a scenario runs, Cucumber finds the method whose expression matches each step, passes the parameter values to it, and runs it. Step definitions live in the **glue** package, in a class such as `LoginSteps`. Cucumber creates a **new object** of the step class for every scenario, so a field such as `driver` belongs to one scenario only.

### Key terms

**Cucumber Expressions:**

| Placeholder | Matches in the step | Java parameter |
|---|---|---|
| `{string}` | Text in double quotes: `"standard_user"` | `String` (without the quotes) |
| `{int}` | A whole number: `2` | `int` |
| `{word}` | One word without spaces | `String` |

**Step results:**

| Symbol | Result | Meaning |
|---|---|---|
| ✔ | **passed** | The method ran without an exception |
| ✘ | **failed** | The method threw an exception (often a failed assertion) |
| ↷ | **skipped** | An earlier step in the scenario didn't pass |
| ■ | **undefined** | No step definition matches the step |
| | **ambiguous** | More than one step definition matches |

### Key ideas

- Start from Cucumber's **snippet**, then replace the `throw new PendingException()` line with Selenium code.
- `Given` and `When` steps **act**; `Then` steps **check** with JUnit assertions.
- **The browser, for now:** the **first** step (`I am on the login page`) opens the browser, and the `Then` step, the last step of every scenario, closes it. The `Then` step reads the value, closes the browser, **then** asserts, so the browser is closed even when the check fails. Cucumber Handout 3 replaces this with **hooks**.

### Worked example: `LoginSteps`

**Step 1: Create the class with a `driver` field and paste the first snippet.** Make it open Chrome on the Swag Labs login page.

```java
public class LoginSteps {

    private WebDriver driver;

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        driver = new ChromeDriver();
        driver.get("https://www.saucedemo.com/");
    }
}
```

Run it. A browser opens for each scenario and the first step is **✔ passed**; the rest are still undefined. (The browsers stay open for now; step 3 closes them.)

**Step 2: A step with two `{string}` parameters.** The values in quotes arrive as `username` and `password`.

```java
@When("I log in with username {string} and password {string}")
public void iLogInWith(String username, String password) {
    driver.findElement(By.id("user-name")).sendKeys(username);
    driver.findElement(By.id("password")).sendKeys(password);
    driver.findElement(By.id("login-button")).click();
}
```

**Step 3: The two `Then` steps: read, close the browser, assert.** After a successful login the Products page needs a moment to appear, so we **wait** for its title (Selenium Handout 3). The error message appears on the same page straight away, so no wait is needed.

```java
@Then("I should see the {string} page")
public void iShouldSeeThePage(String expectedTitle) {
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    String actualTitle = wait.until(ExpectedConditions.visibilityOfElementLocated(
            By.cssSelector("[data-test='title']"))).getText();
    driver.quit();
    assertEquals(expectedTitle, actualTitle);
}

@Then("I should see the error {string}")
public void iShouldSeeTheError(String expectedError) {
    String actualError = driver.findElement(By.cssSelector("[data-test='error']")).getText();
    driver.quit();
    assertEquals(expectedError, actualError);
}
```

Run again: the three login scenarios pass, and every browser closes. Only the logout scenario still has undefined steps.

**Step 4: The logout scenario's steps.** "I have logged in" is the same action as "I log in", so it simply calls that method. Logging out takes two clicks: open the menu (☰), then click **Logout**. The menu slides in, so we wait until the link is clickable.

```java
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
```

**Step 5: The last `Then`: back on the login page.** Wait for the Login button, read the URL, close the browser, assert.

```java
@Then("I should be back on the login page")
public void iShouldBeBackOnTheLoginPage() {
    new WebDriverWait(driver, Duration.ofSeconds(10))
            .until(ExpectedConditions.visibilityOfElementLocated(By.id("login-button")));
    String url = driver.getCurrentUrl();
    driver.quit();
    assertEquals("https://www.saucedemo.com/", url);
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/steps/LoginSteps.java
package com.qea.selenium.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Step definitions for login.feature (final version from Cucumber Handout 1, topic 1.4). */
public class LoginSteps {

    private WebDriver driver;

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        driver = new ChromeDriver();
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
        driver.quit();
        assertEquals(expectedTitle, actualTitle);
    }

    @Then("I should see the error {string}")
    public void iShouldSeeTheError(String expectedError) {
        String actualError = driver.findElement(By.cssSelector("[data-test='error']")).getText();
        driver.quit();
        assertEquals(expectedError, actualError);
    }

    @Then("I should be back on the login page")
    public void iShouldBeBackOnTheLoginPage() {
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(By.id("login-button")));
        String url = driver.getCurrentUrl();
        driver.quit();
        assertEquals("https://www.saucedemo.com/", url);
    }
}
```

### Checkpoint

Run `RunCucumberTest`. A browser opens and closes for each scenario, and every step is ✔:

```text
Scenario: Locked-out user is refused                                                   # classpath:features/login.feature:11
  ✔ Given I am on the login page                                                       # com.qea.selenium.steps.LoginSteps.iAmOnTheLoginPage()
  ✔ When I log in with username "locked_out_user" and password "secret_sauce"          # com.qea.selenium.steps.LoginSteps.iLogInWith(java.lang.String,java.lang.String)
  ✔ Then I should see the error "Epic sadface: Sorry, this user has been locked out."  # com.qea.selenium.steps.LoginSteps.iShouldSeeTheError(java.lang.String)
...
4 scenarios (4 passed)
13 steps (13 passed)

[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
```

Each step line shows **which Java method** ran it, and JUnit counts each scenario as one test.

### Your turn

1. **Make one fail:** in `login.feature`, change `"Products"` to `"Shop"`. Run it: which step fails, and what does the assertion message say? Does the browser still close? Put it back.
2. Add a scenario for an **empty password**: `standard_user` with password `""` should see *Epic sadface: Password is required*. Do you need a new step definition? Why not?
3. **Ambiguous step:** add a second method with `@When("I log in with username {string} and password {string}")`. Run, read the error, then delete it.
4. Add a scenario where `performance_glitch_user` logs in and sees the Products page. It is slow: does it still pass? Which line in `LoginSteps` makes that possible?

### Common errors

| You see | Why | Fix |
|---|---|---|
| ■ undefined although the method exists | The expression text differs (even by one character), or the class isn't in the glue package | Copy the step text exactly; check the glue value in `RunCucumberTest` |
| Steps undefined for some scenarios only | You used an older version of `login.feature` | Use the final version from Handout 1, topic 1.4 |
| `AmbiguousStepDefinitionsException` | Two expressions match the same step | Delete or reword one |
| `NullPointerException` on `driver` | The scenario doesn't start with `Given I am on the login page` | Start every scenario with the step that opens the browser |
| `NoSuchElementException` for `logout_sidebar_link` / `ElementClickInterceptedException` | Clicked before the menu finished sliding in | Wait with `elementToBeClickable`, as in the example |
| Browsers left open | A step failed before the `Then` that closes the browser | Close them by hand for now; hooks fix this in Handout 3 |

---

**End of Cucumber Handout 2.** Cucumber runs `login.feature` through JUnit, and all 4 scenarios are green. **Next:** Cucumber Handout 3, Reusable Scenarios: outlines, backgrounds, rules, and hooks that take care of the browser for you.
