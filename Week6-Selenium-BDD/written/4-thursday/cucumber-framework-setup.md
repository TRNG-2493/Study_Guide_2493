# Cucumber Framework Setup

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the building blocks of a Cucumber-JVM project: **feature files**, **step definitions (glue)**, **runner**, and **configuration**, and how they find each other.
- Create a **Maven project** with the right dependencies (Cucumber, JUnit Platform, JUnit Jupiter, Selenium, PicoContainer) and explain what each one does.
- Lay out a project with the standard folder structure for features, steps, pages, and support classes.
- Create a minimal **test runner** with the JUnit Platform Suite engine and understand each annotation.
- Configure Cucumber through **`cucumber.properties`** or runner annotations (glue, plug-ins, features location).
- Set up the project in **IntelliJ IDEA** step by step, including the Gherkin and Cucumber for Java plugins.
- Run your first feature from the IDE and from the command line, and read the console output.
- Use the **dry run** to find undefined steps without opening a browser.
- Verify a finished setup with a complete checklist, and diagnose the most common setup problems (no scenarios found, steps not found, version conflicts) from the console messages.

---

## Why This Matters

You now know *what* BDD, Gherkin, and step definitions are. This lesson is where they become a **running framework**. A solid setup saves hours of frustration: a mismatched dependency, a wrong glue package, or a feature file in the wrong folder produces cryptic messages such as "No tests found" or all steps "undefined", even though your code is correct.

An analogy: you have written a play (feature files) and trained the actors (step definitions). Setup is **building the theatre**: the stage (JUnit), the director who reads the script aloud (Cucumber), the address on the invitations that tells everyone which building to go to (the glue and features locations), and the lights (the plugins that print results). If the address on the invitation is wrong, the actors never arrive, and the performance silently does not happen, even though every actor knows their lines. That is exactly what "all steps undefined" feels like.

For **Project 2**, the setup you create today is the foundation of the BDD layer. Your pair will write user stories and features for the Sauce Demo shop (`saucedemo.com`), and this skeleton is what runs them. Tomorrow (Friday) you will add outlines, hooks, tags, reports, and the Maven/JUnit integration in depth; today the goal is simple and concrete: **run one scenario end to end** and see it pass.

This lesson reuses what you already have: the `DriverFactory` from Monday, the browser options, and the page objects from Wednesday. Nothing is thrown away; Cucumber is added on top.

---

## The Concept

### 1. The Four Building Blocks

```
 ┌───────────────────────────┐
 │ 1. Feature files (.feature)│   What to test (Gherkin)           src/test/resources/features/
 └─────────────┬─────────────┘
               │ matched by text
 ┌─────────────▼─────────────┐
 │ 2. Step definitions (glue) │   How to perform each step (Java)  src/test/java/.../steps/
 └─────────────┬─────────────┘
               │ call
 ┌─────────────▼─────────────┐
 │ 3. Page objects + support  │   UI knowledge, helpers            src/main/java or src/test/java
 └─────────────┬─────────────┘
               │ drive
 ┌─────────────▼─────────────┐
 │    Selenium WebDriver      │
 └───────────────────────────┘

 4. Runner + configuration:  tells Cucumber WHERE the features are, WHICH package is the glue,
                             and WHICH reports/plugins to use; started by JUnit/Maven.
```

| Block | What it is | Who writes it | Where it lives |
|---|---|---|---|
| Feature files | Plain-text scenarios in Gherkin | The whole team (three amigos) | `src/test/resources/features` |
| Step definitions (glue) | Java methods matched by step text | Automation engineer | `src/test/java/.../steps` |
| Page objects / support | Selenium code, `DriverFactory`, `TestContext` | Automation engineer | `src/main/java` and `src/test/java/.../support` |
| Runner + configuration | A small class and/or properties file that starts everything | Set up once | `src/test/java/.../runners`, `src/test/resources` |

**What happens when you press Run (the big picture):**

1. Maven (or the IDE) starts JUnit Platform.
2. JUnit finds the `RunCucumberTest` class marked `@Suite` and asked to use the `cucumber` engine.
3. The Cucumber engine reads every `.feature` file in the configured folder.
4. For each scenario it matches each step to a step definition in the **glue** package.
5. It creates the step classes (injecting the `TestContext`), and calls the methods in order.
6. Your methods drive page objects, which drive Selenium, which drives Chrome.
7. Cucumber prints results through the **plugins** (here `pretty`) and JUnit reports pass/fail to Maven.

### 2. Prerequisites

- **JDK 17** (or the version specified for the course), `java -version`.
- **Maven 3.8+**, `mvn -version`.
- An IDE: **IntelliJ IDEA** (Community is enough) or **Eclipse**/**VS Code** with Java support.
- Google Chrome (or another browser).
- Internet access for dependency downloads.

**Check them now** (open a terminal; on Windows use PowerShell or Command Prompt):

```
java -version
mvn -version
```

Expected: `java -version` prints a line containing `17` (for example `openjdk version "17.0.12"`), and `mvn -version` prints `Apache Maven 3.8.x` or higher together with the **same Java version**. If Maven reports a different (older) Java, Maven will compile with that one and fail later with `release version 17 not supported`. Fix the `JAVA_HOME` environment variable so it points to the JDK 17 folder.

### 3. Create the Maven Project

Create a Maven project (IDE wizard or command line):

```
mvn archetype:generate -DgroupId=com.revature.qea -DartifactId=bdd-framework \
    -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

Or simply create a folder with a `pom.xml` and the structure below. If your Wednesday Selenium project already exists, **extend it** rather than starting over: the page objects and `DriverFactory` are reused.

**What is Maven doing for you?** Maven is a *build tool and dependency manager*. You list the libraries you need in `pom.xml`; Maven downloads them (and the libraries they need) from the internet into a local cache (`~/.m2`) and adds them to the classpath when compiling and running. Without it you would download dozens of JAR files by hand and keep their versions compatible yourself.

### 4. The `pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.revature.qea</groupId>
  <artifactId>bdd-framework</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

    <selenium.version>4.25.0</selenium.version>
    <cucumber.version>7.20.1</cucumber.version>
    <junit.version>5.11.0</junit.version>
    <junit.platform.version>1.11.0</junit.platform.version>
  </properties>

  <dependencies>
    <!-- Selenium -->
    <dependency>
      <groupId>org.seleniumhq.selenium</groupId>
      <artifactId>selenium-java</artifactId>
      <version>${selenium.version}</version>
    </dependency>

    <!-- Cucumber core for Java: annotations such as @Given, @When, @Then -->
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-java</artifactId>
      <version>${cucumber.version}</version>
      <scope>test</scope>
    </dependency>

    <!-- Lets JUnit Platform discover and run Cucumber features -->
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-junit-platform-engine</artifactId>
      <version>${cucumber.version}</version>
      <scope>test</scope>
    </dependency>

    <!-- Dependency injection for sharing state between step classes -->
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-picocontainer</artifactId>
      <version>${cucumber.version}</version>
      <scope>test</scope>
    </dependency>

    <!-- JUnit 5: assertions and the platform suite (runner) -->
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>${junit.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.platform</groupId>
      <artifactId>junit-platform-suite</artifactId>
      <version>${junit.platform.version}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <!-- Runs the tests during "mvn test" -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.0</version>
      </plugin>
    </plugins>
  </build>
</project>
```

**Reading the pom.xml, section by section:**

| Part | Meaning |
|---|---|
| `<project ...>` and `<modelVersion>` | The standard wrapper and POM format version. Copy as is. |
| `groupId`, `artifactId`, `version`, `packaging` | The project's identity. `groupId` matches your Java package root; `jar` means it builds a JAR. |
| `<properties>` | Named values reused below. `maven.compiler.source/target` = the Java language level (17). `project.build.sourceEncoding` avoids encoding warnings. The `*.version` properties hold library versions in **one place**. |
| `${cucumber.version}` | A *placeholder* replaced by the property value. All `io.cucumber` libraries must share one version, so one property is used for all three. |
| `<scope>test</scope>` | The library is available only for test code (not packaged as part of the main app). |
| `<build><plugins>` | Extra build tools. Surefire is the plugin that runs tests on `mvn test`. |

**What each dependency does:**

| Dependency | Purpose |
|---|---|
| `selenium-java` | Browser automation (Monday to Wednesday) |
| `cucumber-java` | The Java annotations and runtime (`@Given`, `DataTable`, ...) |
| `cucumber-junit-platform-engine` | A *test engine* so JUnit can discover `.feature` files and run them as tests |
| `cucumber-picocontainer` | Dependency injection so step classes can share a context object |
| `junit-jupiter` | JUnit 5 assertions (`Assertions.assertEquals`) and the Jupiter engine |
| `junit-platform-suite` | The `@Suite` annotations used by the runner class |

**Important notes:**

- Version numbers above are **examples**; use the versions your instructor gives you or the latest stable ones. All `io.cucumber` artifacts should have the **same version** (that is why we use one `cucumber.version` property).
- Mixing **old JUnit 4** Cucumber dependencies (`cucumber-junit`, `@RunWith(Cucumber.class)`) with the new JUnit Platform engine causes confusing conflicts. This course uses **JUnit 5 and the Platform engine**. (Friday's *JUnit Integration* lesson explains the runner options in depth, including how JUnit 4 differs.)
- Selenium is a normal (compile) dependency here so that page objects in `src/main` can use it. Cucumber and JUnit are `test` scope.
- JUnit Jupiter `5.11.0` pairs with JUnit Platform `1.11.0`; when you upgrade, move both together.
- If your Wednesday project already has a `pom.xml`, **add** the Cucumber and JUnit dependencies to it instead of replacing it, and keep a single copy of each library.
- Valid XML matters: every `<dependency>` must be closed, and every opening tag needs its closing tag. IntelliJ shows red underlines on malformed XML, and Maven fails with `Non-parseable POM` if you break it.

### 5. The Folder Structure

```
bdd-framework/
 ├── pom.xml
 └── src/
     ├── main/java/com/revature/qea/
     │     ├── drivers/DriverFactory.java          (Monday/browser options)
     │     ├── pages/                              (Wednesday: BasePage, LoginPage, ...)
     │     └── utils/                              (WaitUtils, ScreenshotUtil, ...)
     └── test/
          ├── java/com/revature/qea/
          │     ├── runners/RunCucumberTest.java   (the runner, Section 6)
          │     ├── steps/                         (step definition classes)
          │     │     ├── LoginSteps.java
          │     │     └── CartSteps.java
          │     └── support/TestContext.java       (shared state, injected by PicoContainer)
          └── resources/
                ├── features/                      (all .feature files)
                │     ├── login.feature
                │     └── shopping-cart.feature
                ├── cucumber.properties            (Cucumber configuration, Section 7)
                └── junit-platform.properties      (optional JUnit configuration)
```

Two **rules** that cause most setup problems:

1. **Feature files** must be on the **classpath**: under `src/test/resources`. The folder name `features` is a convention you declare in the runner.
2. The **glue package** must be the Java package that contains your step definitions (here `com.revature.qea.steps`), and the runner must name it.

**Why `src/test/resources`?** Maven copies everything in `src/test/resources` to `target/test-classes` when building. Cucumber looks for features on the *classpath*, which includes `target/test-classes`. A feature file placed anywhere else (for example next to your Java files in `src/test/java`) is **not copied**, so Cucumber never sees it.

**Why a package for the glue?** Cucumber scans a *package name*, not a folder path. The package name in the `package` line of each Java file must match the folder it sits in, and the glue setting must use the dotted package name (`com.revature.qea.steps`), not a slash path.

### 6. The Runner Class

The **runner** is a small class that tells JUnit Platform: "run Cucumber, look for features *here*, and find glue code *there*."

```java
package com.revature.qea.runners;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty")
public class RunCucumberTest {
    // intentionally empty: annotations do all the work
}
```

**Annotation by annotation:**

| Annotation | Meaning |
|---|---|
| `@Suite` | Marks this class as a JUnit Platform test suite |
| `@IncludeEngines("cucumber")` | Use the Cucumber engine to discover and execute tests |
| `@SelectClasspathResource("features")` | Look for `.feature` files in the classpath folder `features` (that is `src/test/resources/features`); you may repeat it for several folders, or use a path to a single file (`"features/login.feature"`) |
| `@ConfigurationParameter(key = GLUE_PROPERTY_NAME, ...)` | **Glue:** comma-separated list of packages with step definitions (and, later, hooks) and `TestContext` |
| `@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty")` | **Plugins:** output formatters. `pretty` prints each step to the console, in color where supported |

**Naming:** Maven's default Surefire configuration runs classes whose names match `*Test`, `Test*`, `*Tests`, or `*TestCase`. `RunCucumberTest` matches, so `mvn test` finds it. (Test filtering, tags, and report plug-ins are Friday topics.)

The runner class itself has **no code**: JUnit runs it, the Cucumber engine reads the features, and calls your step definitions.

**Line by line, in plain words:**

- `package com.revature.qea.runners;` puts the runner in its own package, separate from steps.
- The `import org.junit.platform.suite.api.*` lines bring in the four annotations used.
- The two `import static ... Constants.*` lines bring in readable constant names (`GLUE_PROPERTY_NAME` is just the string `"cucumber.glue"`) so you do not mistype keys.
- Each annotation is a *setting*: engine, where features are, where glue is, how to print results. The class body is empty because JUnit reads the annotations by reflection.
- The glue value lists **two** packages separated by a comma: the steps and the support package that contains `TestContext`. (If `TestContext` is outside the glue, PicoContainer can still instantiate it when asked, but listing it avoids surprises with some versions.)

### 7. Cucumber Configuration Options

Settings can live in three places; they all set the same *configuration parameters*:

1. **Runner annotations** (as above): version-controlled with the code.
2. **`src/test/resources/cucumber.properties`**: a properties file Cucumber reads automatically:

   ```properties
   cucumber.glue=com.revature.qea.steps,com.revature.qea.support
   cucumber.plugin=pretty
   cucumber.publish.quiet=true
   cucumber.features=src/test/resources/features
   ```
3. **Command line / system properties**, which **override** the file: `mvn test -Dcucumber.plugin=pretty`

Commonly used options:

| Property | Purpose |
|---|---|
| `cucumber.glue` | Packages containing step definitions/hooks |
| `cucumber.features` | Where to find features (path or classpath) |
| `cucumber.plugin` | Output formatters/report plug-ins (Friday covers reporting) |
| `cucumber.publish.quiet` | Hides the "Share your Cucumber Report" banner |
| `cucumber.execution.dry-run` | `true` = check that every step has a definition, without running them. Very useful when writing a new feature |
| `cucumber.snippet-type` | `underscore` or `camelcase` for generated method names |
| `cucumber.filter.tags` | Run only scenarios matching a tag expression (**Friday**) |

If you set a value both in the runner and in the properties file, they are merged or the runner takes precedence depending on the key; keep a **single source of truth** to avoid confusion.

**Which should you use?** For this course, put **glue, features, and plugin** in the runner (visible, versioned) and use `-D` options for things that change per run (browser, dry run). The properties file is handy for settings you want every developer to share without touching Java. A common beginner mistake is to define glue in both places with a typo in one of them, and then spend an hour debugging which one is winning.

### 8. A Minimal End-to-End Example

Create these four files and run them.

**1. `src/test/resources/features/login.feature`**

```gherkin
Feature: Login
  As a registered customer
  I want to log in
  so that I can see the products

  Scenario: Successful login with valid credentials
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "secret_sauce"
    Then the customer sees the products page
```

**2. `src/test/java/com/revature/qea/support/TestContext.java`**: holds the driver for a scenario.

```java
package com.revature.qea.support;

import com.revature.qea.drivers.DriverFactory;
import org.openqa.selenium.WebDriver;

public class TestContext {

    private WebDriver driver;

    /** Lazily creates the browser on first use. */
    public WebDriver driver() {
        if (driver == null) {
            driver = DriverFactory.createDriver(
                    System.getProperty("browser", "chrome"),
                    Boolean.parseBoolean(System.getProperty("headless", "false")));
        }
        return driver;
    }

    public void quitDriver() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }
}
```

**3. `src/test/java/com/revature/qea/steps/LoginSteps.java`**

```java
package com.revature.qea.steps;

import com.revature.qea.pages.InventoryPage;
import com.revature.qea.pages.LoginPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class LoginSteps {

    private final TestContext context;
    private LoginPage loginPage;
    private InventoryPage inventoryPage;

    public LoginSteps(TestContext context) {         // PicoContainer injects the context
        this.context = context;
    }

    @Given("the customer is on the login page")
    public void theCustomerIsOnTheLoginPage() {
        loginPage = new LoginPage(context.driver()).open();
    }

    @When("the customer logs in with username {string} and password {string}")
    public void theCustomerLogsIn(String username, String password) {
        inventoryPage = loginPage.loginAs(username, password);
    }

    @Then("the customer sees the products page")
    public void theCustomerSeesTheProductsPage() {
        assertTrue(inventoryPage.isLoaded(), "The products page was not displayed");
        context.quitDriver();    // TEMPORARY cleanup so the browser closes; hooks (Friday) replace this
    }
}
```

> **Why is cleanup inside a `Then` step?** That is a deliberate, **temporary** shortcut. A `Then` step is the wrong place for cleanup (it will not run if the scenario fails earlier, leaving the browser open). The proper solution is an **`@After` hook** that always runs, which is a **Friday** topic. Until then, close the browsers manually if a scenario fails. This shows concretely *why* hooks exist.

**4. `src/test/java/com/revature/qea/runners/RunCucumberTest.java`**, as in Section 6.

**What each file does, and how they connect:**

- `login.feature` states the behavior. Its three step lines are *text only*.
- `LoginSteps` supplies one method for each of those texts. Its constructor asks for a `TestContext`, so PicoContainer creates and injects it.
- `TestContext` creates the Chrome browser the first time a step asks for `context.driver()`, using the `DriverFactory` you wrote on Monday. `System.getProperty("browser", "chrome")` means: use the `-Dbrowser=...` value if given, otherwise `chrome`. `headless` works the same way and defaults to `false`.
- `RunCucumberTest` points JUnit at the `features` folder and at the glue packages.
- `LoginPage` and `InventoryPage` are your Wednesday page objects. `loginAs(...)` is assumed to type the credentials, click Login, and return an `InventoryPage`; adapt the names if yours differ.

**Run it:**

- **IntelliJ:** right-click the runner class → *Run 'RunCucumberTest'*, or right-click the `.feature` file → *Run* (needs the Cucumber for Java plugin).
- **Command line** (from the folder containing `pom.xml`):

  ```
  mvn clean test
  ```

**Expected console output (abridged):**

```
Scenario: Successful login with valid credentials          # features/login.feature:6
  Given the customer is on the login page                  # LoginSteps.theCustomerIsOnTheLoginPage()
  When the customer logs in with username "standard_user" and password "secret_sauce"
  Then the customer sees the products page

1 Scenarios (1 passed)
3 Steps (3 passed)
0m4.215s

[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

A browser window opens, the login happens, and the browser closes. Congratulations: you have a working BDD framework.

**How to read the output:** `Scenario: ... # features/login.feature:6` shows the scenario and where it is defined (file and line). Each step is followed by the Java method that handled it, which proves the matching worked. `1 Scenarios (1 passed)` and `3 Steps (3 passed)` summarise Cucumber's result; the `[INFO] Tests run` lines come from Maven/JUnit, which treat each scenario as one test.

### 9. Dry Run and Snippet Generation

When you write a new feature, first verify that every step is defined **without opening any browser**:

```
mvn test -Dcucumber.execution.dry-run=true
```

Cucumber prints each step as *skipped* if a definition exists, or **undefined** with a snippet if not. Copy the snippets into your step classes. This gives a fast feedback loop: write the feature → dry run → implement missing steps → real run.

**Why this is valuable:** in a dry run Cucumber still does the *matching* (including checking for ambiguous and undefined steps), but it never calls your methods, so no browser opens, no test data is changed, and the run takes about a second. It is the quickest way to check that your three-amigos feature files have glue behind them.

Expected output when everything is defined (abridged):

```
Scenario: Successful login with valid credentials   # features/login.feature:6
  Given the customer is on the login page
  When the customer logs in with username "standard_user" and password "secret_sauce"
  Then the customer sees the products page

1 Scenarios (1 skipped)
3 Steps (3 skipped)
```

"Skipped" here simply means "not executed because this is a dry run". If you see `undefined` instead, that is the signal to copy a snippet.

### 10. IDE Support

| IDE | Plugins | Benefits |
|---|---|---|
| **IntelliJ IDEA** | *Cucumber for Java* and *Gherkin* (bundled/Ultimate; install from Marketplace on Community) | Syntax highlighting, auto-completion of steps, **Ctrl+click navigation** from a step to its definition, "Create step definition" quick-fix, run a single scenario from the gutter |
| **Eclipse** | *Cucumber Eclipse Plugin* | Highlighting, step navigation |
| **VS Code** | *Cucumber (Gherkin) Full Support* by Alexander Krechik | Highlighting, step autocompletion, navigation |

Use the **"Create step definition"** quick-fix, then adjust the generated code.

#### Step-by-step: setting up the project in IntelliJ IDEA

1. **Install a JDK 17** if `java -version` did not show it. In IntelliJ you can do this from *File → Project Structure → SDKs → + → Download JDK* (choose version 17).
2. **Create the project.** *File → New → Project*. Choose **Maven** on the left (or *Java* with build system *Maven*). Set the **JDK** to 17, **GroupId** to `com.revature.qea`, **ArtifactId** to `bdd-framework`. Click *Create*. (To extend your Wednesday project instead, use *File → Open* and select its folder or `pom.xml`, then choose *Open as Project*.)
3. **Replace the `pom.xml` content** with the one in Section 4 (or merge the dependencies into your existing file).
4. **Reload Maven.** A small *Maven* icon (an "m" with a refresh arrow) appears at the top-right of the editor after you edit `pom.xml`: click it, or open the *Maven* tool window on the right and click the circular *Reload All Maven Projects* button. Watch the progress bar at the bottom while dependencies download. When finished, expand *External Libraries*: you should see `io.cucumber:cucumber-java` and `selenium-java`.
5. **Check the folder roles.** In the *Project* view, `src/main/java` should show a blue folder, `src/test/java` a green folder, and `src/test/resources` a folder with a stack icon. If a folder has the wrong colour, right-click it → *Mark Directory as* → *Sources Root* / *Test Sources Root* / *Test Resources Root*.
6. **Create the packages.** Right-click `src/test/java` → *New → Package* and create `com.revature.qea.runners`, `com.revature.qea.steps`, and `com.revature.qea.support` (the main source tree needs `drivers` and `pages`; copy your Wednesday classes there).
7. **Create the feature folder.** Right-click `src/test/resources` → *New → Directory* → `features`. Then right-click `features` → *New → File* → `login.feature`. (IntelliJ shows Gherkin colouring once the plugin is active.)
8. **Install the plugins.** *File → Settings* (on macOS: *IntelliJ IDEA → Settings*) → *Plugins* → *Marketplace*. Search for **Cucumber for Java** and click *Install*; search for **Gherkin** and install it if it is not already listed as installed (Ultimate bundles both; Community needs the Marketplace). Click *Restart IDE* if asked.
9. **Check that the plugin works.** Open `login.feature`. Step lines whose text matches a definition appear normal; undefined steps are **underlined or coloured differently** until you write the definition. Hold *Ctrl* (macOS: *Cmd*) and click a step to jump to its method; if nothing happens, the glue package is not visible to the plugin (see Troubleshooting).
10. **Create the Java files.** Add `TestContext`, `LoginSteps` and `RunCucumberTest` from Sections 6 and 8 by right-clicking the package → *New → Java Class*. Paste the code and let IntelliJ add any missing imports (*Alt+Enter* on a red name).
11. **Run the runner.** Right-click `RunCucumberTest` in the editor tab or the *Project* view → *Run 'RunCucumberTest'*. The *Run* panel at the bottom shows a green tree with one node per scenario.
12. **Run a single scenario or feature file (optional).** Click the green arrow in the gutter next to a `Scenario:` line, or right-click the `.feature` file → *Run*. IntelliJ then starts Cucumber *directly*, which needs the glue to be specified in the *Run Configuration* (*Edit Configurations → Glue*: `com.revature.qea.steps com.revature.qea.support`). If you do not want to configure that, run through the runner class, which already carries the settings.
13. **Run Maven from the IDE (optional).** Open the *Maven* tool window → *Lifecycle* → double-click `test`. This runs the same command as `mvn test`.

**Tip:** if IntelliJ reports `Cannot resolve symbol 'cucumber'` on imports even though Maven downloaded everything, use *File → Invalidate Caches → Invalidate and Restart*, then reload Maven.

### 11. Verification Checklist: Is My Setup Complete?

Work through this list in order. Each item states what you should see.

| # | Check | How | Expected |
|---|---|---|---|
| 1 | JDK 17 active | `java -version` and `mvn -version` | Both show 17 |
| 2 | `pom.xml` is valid | IDE shows no red XML errors; `mvn -q validate` | No output / no errors |
| 3 | Dependencies download | `mvn -q compile` (first run is slow) | No `ERROR`; `~/.m2` is populated |
| 4 | Same Cucumber version everywhere | Look at the `<properties>` block: single `cucumber.version` | Three `io.cucumber` artifacts use `${cucumber.version}` |
| 5 | No JUnit 4 Cucumber artifacts | Search the pom for `cucumber-junit` (not `-platform-engine`) | Not present |
| 6 | Folder structure matches Section 5 | Compare the tree | Features under `src/test/resources/features`; steps under `src/test/java/.../steps` |
| 7 | Package names match folders | Open a step file | `package com.revature.qea.steps;` matches its folder |
| 8 | Glue lists the right packages | Read the runner | `com.revature.qea.steps,com.revature.qea.support` |
| 9 | Runner name ends with `Test` | Check the class name | `RunCucumberTest` |
| 10 | Page objects and `DriverFactory` compile | `mvn -q test-compile` | No compile errors |
| 11 | Dry run finds all steps | `mvn test -Dcucumber.execution.dry-run=true` | `1 Scenarios (1 skipped)`; no `undefined` |
| 12 | Real run passes | `mvn clean test` | `1 Scenarios (1 passed)`, `BUILD SUCCESS` |
| 13 | Browser closes after the run | Watch the desktop | No leftover Chrome window (the temporary cleanup in `Then`) |
| 14 | Failure is visible | Change the expected text so a step fails | `FAILED`, `BUILD FAILURE`; revert after |
| 15 | IDE plugin works | Ctrl+click a step | Jumps to the step definition |
| 16 | Project hygiene | `.gitignore` contains `target/` | Build output is not committed |
| 17 | README has "How to run" | Open README | Commands for `mvn clean test` and the dry run are documented |

Item 14 is important and often skipped: a test framework that cannot fail is not a test framework. Always see one red result.

### 12. Troubleshooting Setup Problems

| Symptom | Likely cause | Fix |
|---|---|---|
| `[WARNING] No tests found` / `Tests run: 0` | Runner not matching Surefire's naming pattern; wrong engine; missing `junit-platform-suite`; feature folder not found | Name the class `*Test`; check `@IncludeEngines("cucumber")`; confirm the dependencies; check `@SelectClasspathResource("features")` points to `src/test/resources/features` |
| All steps **undefined** although you wrote them | Wrong **glue** package; step class not under the glue; typo in the text | Check `GLUE_PROPERTY_NAME`; run the dry run; compare text character by character (watch curly quotes) |
| `Could not resolve ... io.cucumber` / version conflicts | Different Cucumber artifact versions or an old JUnit 4 artifact | Use one `cucumber.version`; remove `cucumber-junit` (JUnit 4) |
| `AmbiguousStepDefinitionsException` | Two patterns match one step | Make patterns distinct, delete duplicates |
| `NullPointerException` on `driver` | `TestContext` not injected (no PicoContainer dependency) or the driver never created | Add `cucumber-picocontainer`; use the lazy `driver()` accessor |
| `ObjectFactory` / "Failed to instantiate step class" | The step class has no public constructor that Cucumber can satisfy | Provide a no-argument constructor, or a constructor with injectable parameters (`TestContext`) |
| Chrome/driver errors | See Monday's *Driver Configuration* lesson | Selenium Manager/updating Selenium |
| Cucumber prints a "Share your report" banner | Default publish behavior | Set `cucumber.publish.quiet=true` |
| `release version 17 not supported` | JDK older than 17 | Use a JDK that matches `maven.compiler.source/target` |

#### Detailed diagnoses with the actual messages

**1. Nothing runs.**

```
[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0
[WARNING] No tests were executed!
```

(The exact wording differs between Maven versions.) Walk through: Is the runner named `*Test`? Does it carry `@Suite` and `@IncludeEngines("cucumber")`? Are `cucumber-junit-platform-engine` and `junit-platform-suite` in the pom with `test` scope? Is the folder under `src/test/resources`? Also run `mvn clean test` rather than `mvn test`; a stale `target` folder sometimes hides new resource files.

**2. Every step is undefined, the scenario runs but nothing happens.**

```
1 Scenarios (1 undefined)
3 Steps (3 undefined)
```

The features were found but no glue matched. Check, in order: (a) the glue string in the runner exactly equals the package name in your step files (watch `step` vs `steps`), (b) the step class is `public` with a public constructor, (c) the annotation imports are from `io.cucumber.java.en`, (d) the text matches character for character.

**3. Feature file not found.**

```
io.cucumber.core.resource.ResourceNotFoundException ... or
Tests run: 0 (a runner with a classpath resource that does not exist runs nothing)
```

Verify that `features/login.feature` exists under `target/test-classes/features` after a build. If it is missing there, the file is in the wrong source folder or Maven did not copy it (do `mvn clean test`).

**4. PicoContainer cannot create a step class.**

```
io.cucumber.core.backend.CucumberBackendException: Failed to instantiate class com.revature.qea.steps.LoginSteps
Caused by: ... Unsatisfied dependency ... TestContext
```

Typical causes: `cucumber-picocontainer` is missing from the pom; the step class has a constructor parameter that PicoContainer cannot create (for example `WebDriver`, an interface); the constructor is not public. Fix: ask only for plain classes with a public no-argument constructor, such as `TestContext`.

**5. Two object factories.**

```
Found multiple ObjectFactory implementations ... cucumber-picocontainer and cucumber-spring
```

Only one dependency-injection library may be on the classpath. Remove the extra one (this course uses only PicoContainer).

**6. Version mismatch.**

```
java.lang.NoSuchMethodError: io.cucumber....
```

or `ClassNotFoundException` for an `io.cucumber` class. One Cucumber artifact is at a different version from the others. In IntelliJ's Maven tool window, expand *Dependencies* and look for two versions of `io.cucumber`. Set every artifact to `${cucumber.version}`.

**7. Chrome starts but the test fails immediately.**

```
org.openqa.selenium.SessionNotCreatedException: Could not start a new session ...
```

or `WebDriverException` mentioning the driver. This is not a Cucumber problem; see Monday's driver-configuration lesson (Selenium Manager downloads the driver; update Selenium and Chrome).

**8. Maven says the POM is malformed.**

```
[ERROR] Non-parseable POM ... Unrecognised tag / expected START_TAG or END_TAG
```

An XML tag is not closed or a `</dependency>` is missing. Compare with Section 4 and count the opening and closing tags of the block that the line number points to.

**9. The test runs twice (or the browser opens twice per scenario).** Cause: a second runner class, or a hand-made `new TestContext()` in addition to the injected one. Keep a single runner and receive the context only through the constructor.

**10. The feature file text is red in IntelliJ even though the run passes.** The Cucumber plugin cannot find the glue (it indexes step definitions by annotation, not by your runner). Check that the step file compiles and that its imports come from `io.cucumber.java.en`; use *File → Invalidate Caches* if needed.

**11. Works in the IDE but not from the command line (or the reverse).** The IDE and Maven may use different JDKs. Compare *Project Structure → SDK* with the Java shown by `mvn -version`, and make them the same.

**12. "Share your Cucumber Report" banner.** Harmless advertising for the Cucumber Reports service; set `cucumber.publish.quiet=true` in `cucumber.properties` to hide it.

---

## Guided Lab: From Empty Folder to Green Scenario

Follow these numbered steps with your pair partner (one types, one reads, then swap after step 8). Expected results are given for each.

1. **Check the toolchain.** Run `java -version` and `mvn -version`. *Expected:* Java 17; Maven 3.8 or newer.
2. **Create or open the project** (Section 3 or Section 10). *Expected:* IntelliJ shows the Maven project; `pom.xml` is open.
3. **Add the dependencies** from Section 4 and reload Maven. *Expected:* *External Libraries* now lists Cucumber, JUnit, and Selenium.
4. **Copy your Wednesday code.** Bring `DriverFactory`, `BasePage`, `LoginPage` and `InventoryPage` into `src/main/java/...`. Run `mvn -q compile`. *Expected:* no errors (fix package names if it complains).
5. **Create the folders** from Section 5. *Expected:* the tree matches.
6. **Write the feature file** (`login.feature`, Section 8). *Expected:* IntelliJ colours the Gherkin; the step lines are underlined as undefined.
7. **Write the runner** (Section 6) and run the **dry run**: `mvn test -Dcucumber.execution.dry-run=true`. *Expected:* `1 Scenarios (1 undefined)`, `3 Steps (3 undefined)`, plus three snippets. This is correct and proves Cucumber can *find the feature*.
8. **Create `TestContext` and `LoginSteps`.** Paste the snippets into `LoginSteps`, implement them as in Section 8. Dry-run again. *Expected:* `1 Scenarios (1 skipped)`; no `undefined`.
9. **Run for real:** `mvn clean test`. *Expected:* Chrome opens, logs in on `saucedemo.com`, closes; `1 Scenarios (1 passed)`; `BUILD SUCCESS`.
10. **Prove it can fail.** Temporarily change the password in the feature to `"wrong"`. Run again. *Expected:* the `Then` step fails (the page object cannot reach the products page), `BUILD FAILURE`. Restore the password.
11. **Break the glue on purpose.** Change the glue in the runner to `com.revature.qea.step` (missing "s") and run the dry run. *Expected:* `3 Steps (3 undefined)`. Fix it. You have just reproduced the most common setup error and will recognise it instantly in future.
12. **Add the second scenario.** Add the wrong-password scenario from the *Step Definitions* lesson and the new `Then` step for the error message (with `{string}`). Run. *Expected:* `2 Scenarios (2 passed)`; the first two steps were reused without new code.
13. **Commit.** Add a `.gitignore` containing `target/` and commit with a clear message such as "Add Cucumber skeleton with login scenario".

---

## Hands-On Checklist

1. Create (or extend) the Maven project with the `pom.xml` above and run `mvn -q compile` to download the dependencies.
2. Copy `DriverFactory` and the Wednesday page objects into the project.
3. Create the folder structure from Section 5.
4. Write `login.feature` (one scenario), `TestContext`, `LoginSteps`, and `RunCucumberTest`.
5. Run `mvn clean test` and read the output.
6. Break something on purpose: rename the glue package in the runner and observe the "undefined" steps; fix it.
7. Run the dry run and see what the output looks like.
8. Add a second scenario (wrong password) and the matching `Then` step for the error message. Notice that the first two steps are **reused**.

---

## Practice Exercises

1. **Explain the pieces.** In your own words, explain what each of these does: feature file, step definition, glue, runner, plugin.
2. **Add a scenario.** Add the negative login scenario (locked-out user) and implement any new steps. Which steps did you reuse?
3. **Dry run.** Write a new scenario with three **new** steps, run the dry run, and use the snippets to create the step definitions.
4. **Properties file.** Move the glue and plugin settings from the runner annotations to `cucumber.properties`. Does the run still work? What is the benefit and the risk of this approach?
5. **Command-line override.** Run with `-Dbrowser=firefox` (if installed) and `-Dheadless=true`. Which class reads those properties?
6. **Folder detective.** Move a feature file out of `src/test/resources/features` to `src/test/resources/other`. Predict what happens and verify. Then fix it by adding a second `@SelectClasspathResource`.
7. **IDE navigation.** Install the Cucumber plugin and use *Go to step definition* on three steps; use "Create step definition" for a new one.
8. **Project 2 milestone.** Set up the BDD skeleton in your pair's Project 2 repository: dependencies, folder structure, runner, `TestContext`, and one passing scenario. Add a README section "How to run the tests".
9. **Version hunt.** Deliberately set `cucumber-java` to `7.20.1` and `cucumber-picocontainer` to a different version (for example `7.18.0`). Run `mvn clean test` and record the error or warning. Then restore the single `cucumber.version` property. Why does one property prevent this class of problem?
10. **Diagnose from output.** Given this console result, state the cause and the fix: `1 Scenarios (1 undefined)` / `3 Steps (3 undefined)` where `LoginSteps` exists in package `com.revature.qea.step` and the runner glue says `com.revature.qea.steps`.
11. **Mini-project tree.** Draw (on paper) the folder tree for a project with `login.feature`, `shopping-cart.feature`, three step classes, a `TestContext`, a runner, and the page objects. Place every file in the right source folder and say which are on the test classpath.
12. **Temporary cleanup.** Run a scenario that fails on its first `Then` before the cleanup line. Observe the open browser. In two sentences, explain what this tells you about why Friday's hooks are needed.

---

## Solutions and Hints

**1. Pieces (model answers).** *Feature file:* Gherkin text describing behavior. *Step definition:* a Java method bound to a step text. *Glue:* the package(s) Cucumber scans for step definitions (and later hooks). *Runner:* a small class that starts Cucumber under JUnit and holds the settings. *Plugin:* an output formatter (for example `pretty`) that prints or writes results.

**2. Locked-out scenario (hint).** The Given and When are reused as they are; the only new step is a `Then` with `{string}` for the error message `Epic sadface: Sorry, this user has been locked out.`. If your `loginAs` method assumes success, add a page-object method that stays on the login page.

**3. Dry run (hint).** Three `undefined` steps with three snippets. Copy them into a step class and rerun the dry run until the output says `skipped`, not `undefined`.

**4. Properties file.** It works if the file is in `src/test/resources/cucumber.properties` and the keys are correct. Benefit: settings can be changed without editing Java. Risk: the settings are now in two possible places (annotations and file); if both exist, one can silently override the other. Keep one source of truth.

**5. Command-line override.** `TestContext.driver()` reads `System.getProperty("browser", ...)` and `System.getProperty("headless", ...)`. If you pass `-D` options through Maven and Surefire does not forward them to the forked test JVM, configure `<systemPropertyVariables>` in Surefire or use environment variables (a Friday integration topic); in the IDE you can add them as VM options.

**6. Folder detective.** `other/` is not selected, so the scenario is not found: `Tests run: 0` or fewer scenarios than expected. Add `@SelectClasspathResource("other")` (repeatable annotation) to include it.

**7. IDE navigation (hint).** If Ctrl+click does nothing, the plugin has not indexed the step definitions: confirm the imports are `io.cucumber.java.en.*`.

**8. Project 2 milestone (hint).** Use the verification checklist (Section 11) as your acceptance test. Commit only when items 11 and 12 pass.

**9. Version hunt.** Typical result: a `NoSuchMethodError`/`NoClassDefFoundError` or a failure to create the object factory. With one property every artifact moves together, so mismatches cannot occur by accident.

**10. Diagnose from output.** The glue package is wrong (`steps` vs `step`) or the package line of `LoginSteps` does not match what the runner names. Make the runner glue and the `package` declaration agree, rerun the dry run.

**11. Tree (model).** Main source tree: `drivers`, `pages`, `utils`. Test source tree: `runners/RunCucumberTest.java`, `steps/*.java`, `support/TestContext.java`. Test resources: `features/login.feature`, `features/shopping-cart.feature`, optional `cucumber.properties`. All `src/test` content is on the test classpath; `src/main` is also on it for tests because tests depend on the main code.

**12. Temporary cleanup.** The browser stays open because `quitDriver()` sits in the last step, which never ran. Cleanup tied to a step that may be skipped is unreliable; Friday's `@After` hook runs after every scenario regardless of result.

---

## Self-Check Questions

1. **What is the glue?**
   The Java package(s) Cucumber scans for step definitions (and later hooks). It must match the package name in your step files.
2. **Where must feature files be located in a Maven project?**
   On the classpath, normally under `src/test/resources` (for example `src/test/resources/features`).
3. **Why must all `io.cucumber` dependencies use the same version?**
   They are released together; mixing versions can cause `NoSuchMethodError` or failures to create objects. A single `cucumber.version` property prevents it.
4. **What does `@IncludeEngines("cucumber")` do?**
   It tells the JUnit Platform suite to use the Cucumber test engine to discover and run the features.
5. **What is a dry run for?**
   To check that every step has exactly one definition without executing anything or opening a browser.
6. **Why is `context.quitDriver()` inside a `Then` step considered a temporary workaround?**
   It is skipped if an earlier step fails, leaving the browser open. Hooks (Friday) run regardless of the outcome.
7. **Why does the runner class have an empty body?**
   All configuration is in its annotations; JUnit reads them and the Cucumber engine does the work.
8. **A run shows `Tests run: 0`. Name three things to check.**
   The runner name ends in `Test`; `@IncludeEngines("cucumber")`, `@Suite` and the dependencies are present; the feature folder under `src/test/resources` matches `@SelectClasspathResource`.

---

## Summary

- A Cucumber-JVM project consists of **feature files** (`src/test/resources/features`), **step definitions** (the **glue** package), **page objects/support code**, and a **runner** with **configuration**.
- Use a **Maven** `pom.xml` with `cucumber-java`, `cucumber-junit-platform-engine`, `cucumber-picocontainer`, JUnit Jupiter, `junit-platform-suite`, and Selenium, **all Cucumber artifacts at the same version**.
- The **runner** (`@Suite`, `@IncludeEngines("cucumber")`, `@SelectClasspathResource`, glue and plugin `@ConfigurationParameter`s) tells JUnit where the features and the glue are; Surefire finds it when its name ends in `Test`.
- Configuration can be in runner annotations, `cucumber.properties`, or `-D` options; **dry run** checks that all steps are defined without launching browsers.
- Share the driver per scenario with a PicoContainer-injected **`TestContext`**; the `quitDriver()` call inside the `Then` step is **temporary**, and proper browser startup/cleanup is the job of **hooks (Friday)**.
- Use the verification checklist after setup, including making one scenario fail on purpose.
- Most setup issues come from the **glue package**, **feature location**, **dependency versions**, and **runner naming**; the console messages in the troubleshooting section map each symptom to a cause.
- Tomorrow: Scenario Outlines, Background, Rule, hooks, tags, deeper JUnit/Maven integration, and reports (covered in depth on Friday).

---

## Additional Resources

- Cucumber documentation, *Cucumber-JVM: Installation and Guides*: https://cucumber.io/docs/installation/java/
- Cucumber-JVM repository, *cucumber-junit-platform-engine README* (runner and configuration parameters): https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-junit-platform-engine
- Cucumber documentation, *Cucumber Reference: Configuration options*: https://cucumber.io/docs/cucumber/api/#options
