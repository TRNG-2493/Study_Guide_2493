# JUnit Integration

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why Cucumber needs a **test runner** and what role JUnit plays (**discovering** and **executing** the Cucumber tests and reporting results to IDEs and build tools).
- Describe the difference between **JUnit 4** and **JUnit 5 (JUnit Platform)** in depth, and justify why this course uses the **JUnit Platform Suite** with the **Cucumber engine**.
- Configure and understand the JUnit 5 runner line by line: `@Suite`, `@IncludeEngines`, `@SelectClasspathResource`, and `@ConfigurationParameter`.
- Use `Constants` for configuration keys: glue, plug-ins, tag filters, naming strategy, dry run, parallelism.
- Recognize and read the equivalent **JUnit 4 runner** (`@RunWith(Cucumber.class)` and `@CucumberOptions`) found in existing projects and translate it to JUnit 5.
- Use **JUnit 5 assertions** inside step definitions with clear failure messages.
- Create **multiple runners** (smoke, regression, one feature) and **re-run only failed scenarios**, including the known limitation of the rerun mechanism.
- Describe **parallel execution** of scenarios and the rules for **thread safety** (no static drivers, `ThreadLocal`, isolated test data).
- Trace what happens from `mvn clean test` to the first scenario starting.
- Diagnose common integration issues (no tests found, wrong engine, version conflicts, IDE problems) from the actual console messages.

---

## Why This Matters

Cucumber on its own is an **execution engine for feature files**; it does not know how to be started by an IDE, how to report results to a build server, or how to plug into the Java testing ecosystem. **JUnit** supplies that: when you click "Run" in IntelliJ, or when Jenkins runs `mvn test`, it is JUnit (through Maven Surefire) that finds your tests, runs them, and records pass/fail results in standard formats that every tool understands.

A useful analogy: Cucumber is a **film projector** that knows how to play one specific kind of film (feature files). JUnit is the **cinema building**: the ticket desk, the schedule, the lights, the fire exits, and the staff that every visitor and inspector already knows how to deal with. Without the building, nobody can walk in and watch the film, and no inspector can write a report about the evening.

On Thursday you copied a runner class and trusted that it worked. Today you learn how it works and how to adjust it. This is what lets you build a **smoke runner**, run only failed tests, speed up the suite with **parallel execution**, and wire the whole thing into **Maven** (next lesson), which is part of the Project 2 requirement for the end of this week: *"complete the Project 2 BDD layer with tags and a report."* A BDD layer that can only be started by right-clicking in one person's IDE does not meet that requirement. A layer that starts with one documented command, selects scenarios by tag, and produces a report does.

**Where you will use this:**

- Every time you press the green arrow beside a scenario in IntelliJ or Eclipse (the IDE uses the JUnit Platform).
- Every time a CI job runs `mvn test` for a nightly regression or a smoke check before a release.
- Every time you add a new purpose to your suite (a "checkout only" run, a "failed only" rerun), because each purpose is usually a small runner class.

---

## The Concept

### 1. The Division of Labor

Three different parties cooperate when a scenario runs. It helps to name each one and say what it is **responsible for**:

```
 You (or Jenkins) run:   mvn test   /  click "Run" in the IDE
                               |
                               v
                 +-----------------------------+
                 | Surefire / IDE              |   finds test classes, starts the JUnit Platform
                 +--------------+--------------+
                                v
                 +-----------------------------+
                 | JUnit Platform              |   test engine launcher; reports results
                 +--------------+--------------+
                                | uses engine "cucumber"
                                v
                 +-----------------------------+
                 | Cucumber JUnit Platform     |   reads .feature files, finds glue,
                 | Engine                      |   runs each scenario as a JUnit test
                 +--------------+--------------+
                                v
                    step definitions -> page objects -> Selenium
```

| Party | Responsibility | Analogy |
|---|---|---|
| **Maven Surefire** (or the IDE) | Decide *which classes* to hand to JUnit and start a Java process | The person who unlocks the cinema and switches on the projector |
| **JUnit Platform** | Provide the **launcher** and the common vocabulary (test, container, result) | The cinema's schedule and ticketing system |
| **Cucumber engine** | A **plug-in ("test engine")** for the platform that understands `.feature` files | The projector that can play this specific film format |
| **Your glue code** | Steps, hooks, page objects | The film itself |

Benefits of this integration:

- IDE **test tree** showing features and scenarios with green/red icons.
- Standard **XML result files** (`target/surefire-reports`) understood by Jenkins, GitHub Actions, GitLab, and others.
- Use of the usual Java tooling: assertions, `mvn test`, filtering, parallelism.

**What is a "test engine"?** The JUnit Platform does not know how to run any particular kind of test. It asks *engines* to **discover** tests (turn files and classes into a tree of tests) and then **execute** them. Jupiter is the engine for `@Test` methods. The Cucumber engine (engine id `cucumber`) turns each `.feature` file into a container and each scenario into a test. That is why a scenario shows up in the IDE tree exactly like a normal JUnit test.

### 2. What Happens From `mvn clean test` to the First Scenario

Understanding the chain makes troubleshooting much easier. Here is the sequence, step by step, for the command `mvn clean test`:

1. **Maven reads `pom.xml`** and resolves dependencies (Selenium, Cucumber, JUnit) from the local cache or Maven Central.
2. **`clean`** deletes the old `target/` folder.
3. **Compile phases** compile `src/main/java` (page objects) and `src/test/java` (runners, steps, hooks). Files from `src/test/resources` (features, properties) are copied to `target/test-classes`. This is why the runner says `@SelectClasspathResource("features")`: it looks in `target/test-classes/features`, which is on the **classpath**.
4. **Surefire starts** in the `test` phase. It scans `target/test-classes` for classes matching its name patterns (`*Test`, `Test*`, `*Tests`, `*TestCase`) and finds `RunCucumberTest`.
5. Surefire detects that the **JUnit Platform** is on the classpath and starts a **forked JVM** (a separate Java process for the tests) that launches the platform.
6. The platform sees `@Suite` on `RunCucumberTest` and asks the **suite engine** to run it. The suite reads `@IncludeEngines("cucumber")`, so only the Cucumber engine takes part.
7. The Cucumber engine reads the **configuration parameters** (glue, plug-ins, tag filter) and scans the selected classpath folder for `.feature` files.
8. It applies the **tag filter**, builds the list of scenarios (expanding Scenario Outlines into one scenario per Examples row), and for each scenario creates **fresh step-definition objects** (via PicoContainer, which is how `TestContext` is shared in one scenario).
9. For each scenario it runs the **`@Before` hooks**, the steps, then the **`@After` hooks**, and reports a result to the platform.
10. At the end, Surefire writes `target/surefire-reports`, the Cucumber plug-ins write their reports, and Maven prints `BUILD SUCCESS` or `BUILD FAILURE`.

A shortened console excerpt, annotated:

```
[INFO] --- surefire:3.5.0:test (default-test) @ bdd-framework ---          <- step 4: Surefire starts
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.revature.qea.runners.RunCucumberTest                    <- the suite class was found

Scenario: Valid login                                                      <- from the "pretty" plug-in
  Given the customer is on the login page
  ...
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0                    <- 7 scenarios = 7 "tests"
[INFO] BUILD SUCCESS
```

Two details to notice: Surefire says it found the **JUnitPlatformProvider** (if it reports a different provider, something is mixed up), and the "Tests run" number counts **scenarios**, not feature files.

> The version numbers shown in this lesson (for example Surefire 3.5.0, Cucumber 7.20.1, JUnit 5.11.0) are **examples**. Check Maven Central or the projects' release pages for current compatible versions before you copy them into a real project.

### 3. JUnit 4 vs. JUnit 5

Beginners often ask: "Why are there two?" The short answer: JUnit 4 was one library, designed before Java 8. JUnit 5 was redesigned as a **platform** so that many kinds of test engines (including Cucumber's) could plug in.

| | **JUnit 4** | **JUnit 5** |
|---|---|---|
| Architecture | Single library | **JUnit Platform** (launcher) + **Jupiter** (new API) + **Vintage** (runs old tests) |
| Annotations | `@Test`, `@Before`, `@RunWith`, `org.junit.Assert` | `@Test`, `@BeforeEach`, `@Suite`, `org.junit.jupiter.api.Assertions` |
| Cucumber integration | `cucumber-junit` with `@RunWith(Cucumber.class)` | `cucumber-junit-platform-engine` with `@Suite` |
| Status | Legacy, widespread in older projects | **Current standard**; supports parallel execution and better configuration |

Deeper differences that matter in practice:

| Topic | JUnit 4 | JUnit 5 | Why it matters to you |
|---|---|---|---|
| **How tests are started** | A *runner* class is named in `@RunWith` and takes over the test class | An *engine* is discovered automatically; `@Suite` merely selects things | In JUnit 5 there is no "runner" in the old sense; the class with `@Suite` is a *description* of a run |
| **Configuration** | `@CucumberOptions` (a Cucumber-specific annotation) | The generic `@ConfigurationParameter`, plus `junit-platform.properties`, plus system properties | The same keys work in annotations, files, and `-D` flags |
| **Parallel execution** | Needs Surefire forking tricks or third-party runners; Cucumber's JUnit 4 module has no built-in scenario-level parallelism | Built into the Cucumber engine (`cucumber.execution.parallel.*`) | Parallel scenarios are a normal, supported feature in JUnit 5 |
| **Extensions** | `@Rule` and `@ClassRule` | The `Extension` model | Relevant if you write custom test lifecycle code |
| **Minimum Java** | Java 5+ | Java 8+ (this course uses 17) | Older projects may be stuck on JUnit 4 because of old Java |
| **Dependencies** | One `junit:junit` artifact | Several: `junit-jupiter`, `junit-platform-suite`, engines | Many "no tests found" problems are one missing artifact |

**Vintage** is a bridge engine that lets JUnit 5 also run JUnit 4 tests. A project can migrate step by step by having both on the classpath, but you must not combine the **Cucumber JUnit 4 module (`cucumber-junit`)** with the **Cucumber JUnit Platform engine** in the same module: both would try to run the same features and you would get duplicates or conflicts.

This course uses **JUnit 5 with the Cucumber JUnit Platform Engine**. You will still meet JUnit 4 runners in existing code bases (job interviews love this question), so Section 6 shows how to read and translate them.

**Which should you choose, when?**

| Situation | Choice |
|---|---|
| New project | JUnit 5 + `cucumber-junit-platform-engine` |
| Existing project already on JUnit 4 and working fine | Keep it; migrate when you need parallelism or new features |
| Project mixing both | Plan a migration; do not add more JUnit 4 code |

### 4. The JUnit 5 Runner in Detail

```java
package com.revature.qea.runners;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.FILTER_TAGS_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME,
        value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty, html:target/cucumber-reports/report.html")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME,
        value = "not @wip and not @ignore")
public class RunCucumberTest {
}
```

**Line-by-line explanation**

| Line | Explanation |
|---|---|
| `package com.revature.qea.runners;` | The runner lives in its own package, separate from steps. It is not part of the glue; it is the *entry point*. |
| `import org.junit.platform.suite.api.*` | The annotations come from `junit-platform-suite-api`, pulled in by the `junit-platform-suite` dependency. If these imports are red in your IDE, that dependency is missing. |
| `import static ...Constants.GLUE_PROPERTY_NAME` etc. | `Constants` is a class of **string constants** holding the property names (for example `"cucumber.glue"`). Using the constant instead of typing the string prevents typos. |
| `@Suite` | Marks this class as a **JUnit Platform test suite**: a class whose only job is to describe a selection of tests and run them as a group. |
| `@IncludeEngines("cucumber")` | Restricts this suite to the engine with id `cucumber`. Without it, the suite may also try other engines on the classpath. |
| `@SelectClasspathResource("features")` | Selects everything under the `features` folder **on the classpath** (`src/test/resources/features` after copying). |
| `@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "...")` | Passes `cucumber.glue=com.revature.qea.steps,com.revature.qea.support`: *"look for steps, hooks, and context classes in these packages"*. A comma separates packages. |
| `@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "...")` | Passes `cucumber.plugin=...`: which report formats to produce. `pretty` prints to the console, `html:path` writes a file. |
| `@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "...")` | Passes `cucumber.filter.tags=not @wip and not @ignore`: the **tag expression** from the *Tags* lesson. Scenarios tagged `@wip` or `@ignore` are not run. |
| `public class RunCucumberTest { }` | The body is **empty**. The annotations are the entire configuration. |

**Choosing what to select (when and where):**

| Need | Annotation | Example |
|---|---|---|
| All features | `@SelectClasspathResource("features")` | Normal full run |
| One feature file | `@SelectClasspathResource("features/login.feature")` | A runner dedicated to login while you develop |
| One scenario in one file by line | Use `cucumber.features` or the IDE's run-scenario button | Debugging |
| A package of features | `@SelectPackages("features.checkout")` (classpath package names) | Module-based runner |

Other useful keys from `Constants`:

| Constant | Property | Purpose |
|---|---|---|
| `EXECUTION_DRY_RUN_PROPERTY_NAME` | `cucumber.execution.dry-run` | Check step definitions without running |
| `PLUGIN_PUBLISH_QUIET_PROPERTY_NAME` | `cucumber.publish.quiet` | Hide the publish banner |
| `JUNIT_PLATFORM_NAMING_STRATEGY_PROPERTY_NAME` | `cucumber.junit-platform.naming-strategy` | `long` shows the feature name in each test name (good for CI reports) |
| `OBJECT_FACTORY_PROPERTY_NAME` | `cucumber.object-factory` | Choose the dependency injection implementation if several are present |
| `PARALLEL_EXECUTION_PROPERTY_NAME` | `cucumber.execution.parallel.enabled` | Parallel execution (Section 10) |

You can also set the same properties in `src/test/resources/cucumber.properties` or `junit-platform.properties` (for the key names without the Java constants); a **single source of truth** avoids confusion.

**The runner class has no body.** The annotations describe the run. The class **name** matters for Maven: Surefire picks up names ending in `Test`/`Tests`, or starting with `Test`, by default (`RunCucumberTest` works). A class called `CucumberRunner` would silently **not** be found by default and you would see `Tests run: 0`.

**Connecting to what you know:** the glue packages are the packages where your `@Given/@When/@Then` classes (Thursday), your `@Before/@After` hooks (earlier today), and your `TestContext` live. PicoContainer creates a fresh `TestContext` per scenario and injects it into every step class that asks for it in its constructor. The runner never mentions `TestContext`; it only tells Cucumber *where to look*.

### 5. Multiple Runners

You may keep several runners, each representing a purpose:

```java
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "@smoke")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty, html:target/cucumber-reports/smoke.html")
public class RunSmokeTest { }
```

and `RunRegressionTest` with `@regression`. Run one by name with Maven: `mvn test -Dtest=RunSmokeTest`.

**Warning:** with plain `mvn test`, **all** matching runner classes run, so scenarios tagged both `@smoke` and `@regression` may run **twice**. Control this with Surefire `includes/excludes` or Maven profiles (next lesson), or use a single runner and select with `-Dcucumber.filter.tags`.

**Real-world scenario: smoke versus nightly**

A team testing saucedemo.com (the same site as your Project 2) might agree:

| Run | Trigger | Content | Time budget | Runner / command |
|---|---|---|---|---|
| **Smoke** | Every commit | `@smoke`: valid login, add to cart, open cart, logout (about 6 scenarios) | Under 3 minutes | `RunSmokeTest`, or `-Dcucumber.filter.tags="@smoke"` |
| **Regression** | Nightly | `@regression`: everything stable, including negative logins and checkout validation (about 60 scenarios) | 30 minutes | `RunCucumberTest` with a tag filter or `-Pregression` |
| **Rerun** | After a failed night | Only scenarios in `target/rerun.txt` | Minutes | A dedicated rerun runner (Section 8) |

The smoke run is a **tripwire**: if login is broken, there is no point running 60 scenarios. A nightly run is a **safety net** across the whole product. Both use the same features and steps; only the selection differs.

A good compromise used in many teams: one default runner for CI, and a small number of extra runners only where the *selection of files* differs (for example a runner for the rerun file).

### 6. Recognizing the JUnit 4 Runner

In older projects you will see:

```java
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"com.revature.qea.steps"},
    plugin = {"pretty", "html:target/cucumber-reports/report.html"},
    tags = "@smoke and not @wip",
    monochrome = true,
    dryRun = false
)
public class RunCucumberTest { }
```

**Line-by-line:**

| Line | Meaning |
|---|---|
| `@RunWith(Cucumber.class)` | Tells JUnit 4: "do not run this class as a normal test; hand it to the Cucumber runner". |
| `features = "src/test/resources/features"` | A **file system path** (JUnit 5 uses a classpath name instead). |
| `glue = {...}` | Array of glue packages. |
| `plugin = {...}` | Array of plug-ins. |
| `tags = "..."` | Tag expression. |
| `monochrome = true` | Print console output without ANSI colour codes, useful on CI logs that show escape characters as garbage. |
| `dryRun = false` | When `true`, Cucumber only checks that every step has a definition. |

Mapping between the styles:

| JUnit 4 `@CucumberOptions` | JUnit 5 equivalent |
|---|---|
| `features = "..."` | `@SelectClasspathResource("features")` (or `@SelectFile`) |
| `glue = {...}` | `@ConfigurationParameter(key = GLUE_PROPERTY_NAME, ...)` |
| `plugin = {...}` | `@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, ...)` |
| `tags = "..."` | `@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, ...)` |
| `dryRun = true` | `cucumber.execution.dry-run=true` |
| `monochrome = true` | `cucumber.ansi-colors.disabled=true` |

**Worked translation.** The JUnit 4 runner above becomes:

```java
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.revature.qea.steps")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty, html:target/cucumber-reports/report.html")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "@smoke and not @wip")
@ConfigurationParameter(key = "cucumber.ansi-colors.disabled", value = "true")
public class RunCucumberTest { }
```

Also note the imports: JUnit 4 uses `org.junit.runner.RunWith` and `org.junit.Assert`, JUnit 5 uses `org.junit.jupiter.api.Assertions`. **Do not mix `cucumber-junit` (JUnit 4) and `cucumber-junit-platform-engine` in one module**; choose one.

**A migration checklist** (useful in interviews and on real teams):

1. Replace the `cucumber-junit` dependency with `cucumber-junit-platform-engine`, `junit-platform-suite`, and `junit-jupiter`.
2. Replace `org.junit.Assert` imports in steps with `org.junit.jupiter.api.Assertions` (note: in JUnit 5 the **message is the last argument**, in JUnit 4 it was the **first**).
3. Rewrite each runner class as a `@Suite`.
4. Remove `@RunWith` and `@CucumberOptions`.
5. Run `mvn clean test` and compare the scenario count before and after; it must match.

The "message position" change in step 2 is a classic trap: `Assert.assertEquals("message", 3, actual)` in JUnit 4 has a different argument order than `Assertions.assertEquals(3, actual, "message")` in JUnit 5. The compiler may not warn you when both arguments are `Object`.

### 7. JUnit Assertions in Step Definitions

Your `@Then` steps use JUnit 5 assertions. They throw `AssertionFailedError` on failure, which Cucumber reports as a **failed step** with the message. All remaining steps in that scenario are reported as skipped, and the `@After` hooks still run (so your screenshot hook sees the failed state).

```java
import static org.junit.jupiter.api.Assertions.*;

assertEquals(3, cart.getCount(), "Cart count");
assertTrue(inventory.isLoaded(), "Products page was not displayed");
assertFalse(login.isErrorDisplayed(), "No error expected");
assertNotNull(order.getNumber());
assertIterableEquals(List.of("A", "B"), actualNames);
assertEquals(29.99, total, 0.001, "Total price");     // decimals need a tolerance
assertAll("cart",                                     // collect several failures in one go
        () -> assertEquals(2, cart.getCount()),
        () -> assertTrue(cart.contains("Sauce Labs Backpack")));
```

**Line-by-line:**

| Line | Explanation |
|---|---|
| `assertEquals(3, cart.getCount(), "Cart count")` | Passes when both numbers are equal. The first value is the **expected** one (from the Gherkin text), the second the **actual** one (from the page). The third argument is the message prefix. |
| `assertTrue(condition, message)` | Passes only when the condition is `true`. Use it for yes/no checks such as "page is displayed". |
| `assertFalse(...)` | The mirror image: passes when the condition is `false`. |
| `assertNotNull(value)` | Fails when the value is `null`, for example if the order number was not found. |
| `assertIterableEquals(expected, actual)` | Compares two lists element by element **in order**. |
| `assertEquals(29.99, total, 0.001, ...)` | Decimal numbers (`double`) are stored approximately, so two values that look equal can differ in the last digits. The third number is the allowed difference (**delta**). |
| `assertAll("cart", ...)` | Runs **every** check even if the first fails, and reports all failures together under the heading `cart`. Each argument is a **lambda** (`() -> ...`), a small piece of code to be run later. |

**What a failure looks like** in the console and in the report:

```
org.opentest4j.AssertionFailedError: Cart count ==> expected: <3> but was: <2>
	at org.junit.jupiter.api.AssertionFailureBuilder.build(...)
	at com.revature.qea.steps.CartSteps.theCartContainsItems(CartSteps.java:41)
```

How to read it: `Cart count` is your message; `expected: <3>` is the first argument; `but was: <2>` is what the page actually showed; the first line from *your* package (`CartSteps.java:41`) is the assertion to look at. If you had swapped the arguments, the message would claim "expected: 2 but was: 3", which sends the investigator in the wrong direction.

Tips:

- **Argument order:** `assertEquals(expected, actual, message)`. Swapping them makes failure messages confusing ("expected: <wrong value>").
- Add a **message** so the report is self-explanatory. Prefer messages that describe the business meaning ("Cart badge count after adding two items") over technical ones ("count").
- Use `assertAll` when several independent checks belong to one Then.
- Use `assertThrows` for negative expectations at code level (rare in step definitions).
- **Keep assertions in step definitions, not in page objects.** A page object answers questions (`getCartCount()`); the step decides what is expected. This was the Wednesday design rule.

Other assertion libraries (AssertJ, Hamcrest) can also be used and are popular for readable fluent assertions: `assertThat(names).containsExactly("A", "B")`. Whichever you choose, keep it **consistent** across the project.

### 8. Rerunning Failed Scenarios

Cucumber has a `rerun` plugin that records the locations of failed scenarios:

```java
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty, rerun:target/rerun.txt")
```

After a run, `target/rerun.txt` contains lines such as:

```
file:///.../features/login.feature:12
file:///.../features/cart.feature:20
```

Each line is a **feature file plus the line number** of a failed scenario (for outline rows, the line of the failing Examples row). The file is rewritten at every run, so it always describes the *latest* run only. If everything passed, the file is empty.

You can then run only those scenarios, with a second runner or the command line:

```
mvn test -Dcucumber.features=@target/rerun.txt
```

(The leading `@` tells Cucumber to read the **list of locations from the file**; this is a file reference, not a tag. If the suite's `@SelectClasspathResource` takes precedence in your setup, create a dedicated "rerun" runner class that selects the files listed in the rerun file, as described in the cucumber-junit-platform-engine documentation.)

**Important caveat, spelled out.** In a JUnit Platform suite, the **selectors** (`@SelectClasspathResource`, and so on) decide *which features are discovered*. The `cucumber.features` property is read by the Cucumber engine's own discovery, but when a suite already names a classpath resource, the suite's selection is what the engine receives. So the command `-Dcucumber.features=@target/rerun.txt` **may not take effect together with `@SelectClasspathResource`**: the run may simply execute the whole `features` folder again. A **dedicated rerun runner** may be needed. The reliable way to find out is to **measure**: after the command, read the number of scenarios in the `summary` output. If it equals the size of the full suite, the rerun mechanism did not take effect. In that case use one of these approaches:

1. Create a **dedicated rerun runner** whose selection is limited to the failed locations (the cucumber-junit-platform-engine README describes how to select specific features and lines; check it for the syntax of your version), with its own glue configuration and without a broad `@SelectClasspathResource`.
2. Run the failed scenarios one by one from the IDE (the *run scenario* button), reading the locations from `target/rerun.txt`.
3. Use a tag such as `@rerun` temporarily on the failed scenarios and run with `-Dcucumber.filter.tags="@rerun"` (simple and dependable, but remember to remove the tag afterwards).

Rerunning failures helps to detect **flaky** scenarios (pass on rerun) from genuine regressions (fail again). Do not use automatic rerun to *hide* instability; investigate flaky tests (see Tuesday's wait strategies).

**Decision guide**

| Result of the rerun | Likely meaning | Next action |
|---|---|---|
| Fails again with the same message | Genuine defect (product or test) | Investigate; raise a bug or fix the test |
| Passes on rerun | Flaky: timing, data, or environment | Check waits, data isolation; log it as flaky |
| Fails with a different message | Unstable environment or order dependency | Check test independence |

### 9. Naming Strategy and the IDE Test Tree

By default the test names in IDE trees and Surefire XML are short (the scenario name). With

```properties
cucumber.junit-platform.naming-strategy=long
```

each test name includes the **feature name** as well. This matters for CI reports where tests from many features are shown in one flat list: two features may both have a scenario called "Valid login", and without the feature name you cannot tell them apart. Outline rows are named by their Examples row so each row is visible as a separate test.

### 10. Parallel Execution

Browser tests are slow; running scenarios **in parallel** can cut total time dramatically. The JUnit Platform engine supports it with properties (in `junit-platform.properties` or as configuration parameters):

```properties
cucumber.execution.parallel.enabled=true
cucumber.execution.parallel.config.strategy=fixed
cucumber.execution.parallel.config.fixed.parallelism=4
```

**Line-by-line:**

| Line | Meaning |
|---|---|
| `cucumber.execution.parallel.enabled=true` | Switch parallel execution on. The default is off. |
| `...config.strategy=fixed` | Use a **fixed-size pool** of worker threads. The alternative `dynamic` computes the number of threads from the number of CPU cores. |
| `...config.fixed.parallelism=4` | Use 4 threads: up to 4 scenarios run at the same time. |

This runs up to **4 scenarios at the same time**. Each running scenario gets its own thread, and therefore (with our design) its own browser. Cucumber's parallelism is at **scenario level**: different scenarios of one feature may run at the same time.

**What "thread" means here.** A *thread* is a separate line of execution inside one Java process. Think of a restaurant kitchen: one cook (single thread) makes one dish at a time; four cooks (four threads) make four dishes at once. That works well as long as the cooks do not fight over the **same** pan. A shared mutable object is the shared pan.

Parallelism is only safe if your framework is **thread-safe**:

| Requirement | Why |
|---|---|
| **One WebDriver per scenario**, never shared | `WebDriver` objects are not thread-safe. Our per-scenario `TestContext` via PicoContainer already ensures this |
| **No static mutable state** (static driver, static page objects, static counters) | Threads would overwrite each other |
| **Independent scenarios** | Cannot depend on execution order or shared data (also required for tags/rerun) |
| **Test data isolation** | Two scenarios must not use the same user/cart at once (e.g., both modifying the same account) |
| **Machine resources** | Four browsers need enough CPU/RAM; start with 2-4 |

**The static driver bug, shown.** This is the classic beginner design:

```java
public class DriverManager {
    private static WebDriver driver;                 // ONE driver for the whole JVM

    public static WebDriver getDriver() {
        if (driver == null) {
            driver = new ChromeDriver();
        }
        return driver;
    }
}
```

With four threads, scenario A and scenario B both call `getDriver()`. Both get the **same** browser. Scenario A types a username while scenario B is navigating to the cart; the page switches under A's feet and A fails with `NoSuchElementException` even though nothing is wrong with the app. Worse, the `if (driver == null)` check is not safe either: two threads can both see `null` and create two browsers, leaving one orphaned. The failures are random, which makes them very hard to debug.

**The per-scenario design that works:**

```java
public class TestContext {
    private WebDriver driver;                        // instance field: one per TestContext

    public void startBrowser(String browser, boolean headless) {
        driver = DriverFactory.create(browser, headless);
    }
    public WebDriver driver() { return driver; }
    public boolean hasDriver() { return driver != null; }
    public void quit() {
        if (driver != null) { driver.quit(); driver = null; }
    }
}
```

PicoContainer creates a **new `TestContext` for every scenario** and injects that instance into every step class and hook class used by that scenario. Different scenarios therefore never share a driver, even when they run at the same time.

**The `ThreadLocal` alternative.** Sometimes code cannot receive the context by injection (for example a utility class called from many places). A `ThreadLocal<WebDriver>` holds **one value per thread**:

```java
public final class DriverHolder {
    private static final ThreadLocal<WebDriver> DRIVER = new ThreadLocal<>();

    public static void set(WebDriver d) { DRIVER.set(d); }
    public static WebDriver get()       { return DRIVER.get(); }
    public static void remove()         { DRIVER.remove(); }   // always call in @After
}
```

Each thread sees only its own value, so the variable is `static` but not *shared*. Always call `remove()` at the end (an `@After` hook) so that a thread reused for the next scenario starts clean. For beginners, **prefer constructor injection with `TestContext`**; use `ThreadLocal` only when injection is not possible.

**Other things that are not thread-safe in a typical framework:**

| Shared thing | Problem | Remedy |
|---|---|---|
| `static` counters or lists in utilities | Lost updates, `ConcurrentModificationException` | Remove, or use thread-safe classes, or keep data per scenario |
| A single shared test account | Two scenarios changing the same cart | Use one account per parallel slot, or create data per scenario |
| Shared files (a log file, a screenshot named `fail.png`) | Overwriting | Include scenario name or a unique id in file names |
| Singletons holding configuration that is *modified* | Races | Load configuration once and keep it **read-only** |
| Reporting to one `StringBuilder` | Garbled text | Use the `Scenario` object per scenario |

**Practical saucedemo.com note:** the shop's demo users (for example `standard_user`) are shared by everybody on the internet and the site resets its state in the browser session, so parallel scenarios in separate browsers do not interfere on the site side. That is convenient for practice; in a real application with server-side carts you would need separate users per thread.

**How many threads?** Start with 2. Compare run time and failure rate. Browsers are heavy: if the machine runs out of memory, scenarios fail with timeouts that look like product problems. More threads is not always faster.

**Order of results.** In parallel runs the console output of different scenarios is **interleaved**. Use the HTML/JSON report (one block per scenario) instead of the console to read results.

Cross-browser or distributed parallel execution (Selenium Grid) is beyond this week's scope.

### 11. Where Settings Come From (Precedence)

The same Cucumber property can appear in several places. To avoid surprises know the places:

| Place | Example | Typical use |
|---|---|---|
| Runner annotation | `@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, ...)` | Settings unique to that runner |
| `src/test/resources/cucumber.properties` | `cucumber.plugin=pretty` | Project-wide defaults |
| `src/test/resources/junit-platform.properties` | `cucumber.execution.parallel.enabled=true` | Same, picked up by the JUnit Platform |
| Environment variable | `CUCUMBER_FILTER_TAGS="@smoke"` (name uppercased, dots become underscores) | CI settings |
| Java system property (`-D`) | `-Dcucumber.filter.tags="@smoke"` | One-off overrides from Maven or the IDE |

Cucumber documents the order for its own configuration (system properties and environment variables override `cucumber.properties`). **Runner annotations inside a JUnit Platform suite are the least predictable**: the suite passes its annotation values to the engine as explicit parameters, and in some setups these win over a `-D` flag. If your `-Dcucumber.filter.tags` seems to be ignored, remove the tag annotation from the runner and keep the default in `cucumber.properties` or in the Maven profile instead. Prove behaviour with a quick experiment (the scenario count printed by `summary`), not by assumption.

### 12. Running Tests

| How | Command / action |
|---|---|
| IDE (IntelliJ) | Right-click the runner class → *Run*; or the green arrow next to a `Scenario` in a `.feature` file (Cucumber plugin) |
| Maven | `mvn clean test` |
| One runner | `mvn test -Dtest=RunSmokeTest` |
| Filter by tag | `mvn test -Dcucumber.filter.tags="@smoke"` |
| Dry run | `mvn test -Dcucumber.execution.dry-run=true` |
| Choose browser | `mvn test -Dbrowser=firefox -Dheadless=true` (system properties read by `TestContext`) |

Maven specifics (Surefire configuration, profiles, passing properties) are in the next lesson.

**IDE tips for beginners**

- If the green arrow beside a scenario produces "no tests found", check that the IDE runs tests with **JUnit 5** and that the Cucumber plug-in for the IDE is installed.
- The IDE run configuration may not include your `-D` options. Add them under *VM options* (for example `-Dbrowser=chrome`), or set defaults in `cucumber.properties` and your `DriverFactory`.
- If the IDE and Maven disagree, trust Maven (it is what CI runs) and align the IDE's JDK and settings.

### 13. Troubleshooting JUnit Integration

| Symptom | Likely cause | Fix |
|---|---|---|
| `Tests run: 0` | No `junit-platform-suite`, wrong engine, runner name not matching Surefire pattern, wrong resource path | Check dependencies, `@IncludeEngines("cucumber")`, class name ends in `Test`, folder path |
| `No tests were executed` in IntelliJ | Using the JUnit 4 runner configuration with JUnit 5 libraries | Use Platform Suite; ensure IDE runs with JUnit 5 |
| `NoClassDefFoundError: org/junit/platform/...` | Mismatched JUnit Platform/Jupiter versions | Align versions (use the BOM `junit-bom`) |
| Steps undefined although they exist | Glue not configured, or step classes outside glue packages | Check `GLUE_PROPERTY_NAME` |
| `@Test` methods not executing | Missing Jupiter engine | Add `junit-jupiter` |
| Duplicate execution of scenarios | Several runner classes selecting the same features | One runner per purpose; exclude classes with Surefire |
| `IllegalStateException: ... Object factory ...` | Several DI containers on the classpath | Add only one (`cucumber-picocontainer`) or set `cucumber.object-factory` |
| Parallel run: random failures, wrong pages | Shared static driver/state | Per-scenario `TestContext`, no statics |
| JUnit 4 and 5 mixed | Class loading and runner conflicts | Standardize on JUnit 5 for new code |

**Actual messages and how to diagnose them**

1. **Nothing runs**

   ```
   [INFO] Running com.revature.qea.runners.RunCucumberTest
   [WARNING] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.02 s
   [ERROR] No tests were executed!  (Set -DfailIfNoTests=false to ignore this error.)
   ```

   Diagnosis: the runner was found but selected no features. Check that `src/test/resources/features` exists, that it contains `.feature` files, and that `@SelectClasspathResource("features")` matches the folder name exactly (case matters on Linux). Also check that your tag filter does not exclude everything (for example `@smoke` when no scenario has that tag).

2. **Steps are reported undefined**

   ```
   Undefined scenarios:
   file:///.../features/login.feature:8 # Valid login

   You can implement missing steps with the snippets below:
   @Given("the customer is on the login page")
   public void the_customer_is_on_the_login_page() {
       // Write code here that turns the phrase above into concrete actions
       throw new io.cucumber.java.PendingException();
   }
   ```

   Diagnosis: the engine found the feature but not the step. Either the step really is missing, or the `cucumber.glue` list does not include the package of your step class. Compare the package line at the top of the step class with the glue value, letter by letter.

3. **Dependency mismatch**

   ```
   java.lang.NoSuchMethodError: org.junit.platform.engine.support.hierarchical.... 
   or
   org.junit.platform.commons.JUnitException: TestEngine with ID 'cucumber' failed to discover tests
   Caused by: java.lang.NoClassDefFoundError: org/junit/platform/engine/...
   ```

   Diagnosis: versions of `junit-platform-engine`, `junit-platform-suite`, and Jupiter do not fit together. Run `mvn dependency:tree` (next lesson) and look for two different JUnit Platform versions; use the `junit-bom` so all JUnit artifacts share one version.

4. **Two object factories**

   ```
   io.cucumber.core.exception.CucumberException: Found multiple ObjectFactory implementations ...
   ```

   Diagnosis: more than one dependency-injection module (for example PicoContainer and Spring) is on the classpath. Remove the extra one, or select one with `cucumber.object-factory`.

5. **Scenario runs twice**

   Diagnosis: the console or the report lists the same scenario twice. Count your runner classes; two runners that select the same features and the same tags both run under plain `mvn test`.

---

## Complete Example: Two Runners and a Rerun File

**`RunCucumberTest`** (default full run, excludes unfinished work)

```java
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME,
        value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "not @wip and not @ignore")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty, summary, html:target/cucumber-reports/report.html, "
              + "json:target/cucumber-reports/cucumber.json, rerun:target/rerun.txt")
@ConfigurationParameter(key = "cucumber.publish.quiet", value = "true")
public class RunCucumberTest { }
```

**`junit-platform.properties`** (in `src/test/resources`)

```properties
cucumber.junit-platform.naming-strategy=long
cucumber.execution.parallel.enabled=false
```

Run:

```
mvn clean test                                   # everything not @wip/@ignore
mvn test -Dcucumber.filter.tags="@smoke"         # override the filter from the command line
```

A command-line `-D` value for a Cucumber property **overrides** values set in `junit-platform.properties`/`cucumber.properties`; whether it overrides an annotation on the runner depends on the key, so when in doubt use **one** place per setting (recommended: defaults in `cucumber.properties`, overrides from the command line, and runner annotations only for what is unique to that runner).

---

## Guided Lab: Build, Run, and Break a Runner for Project 2

**Goal:** Prove you understand every piece of the runner by building it, then breaking it on purpose in a controlled way. Use your Project 2 saucedemo.com BDD project (login, cart, checkout features).

**Prerequisites:** the Maven project from Thursday with Cucumber, PicoContainer, and `TestContext`; at least three feature files with some scenarios tagged `@smoke`.

**Part A: Build the runner**

1. In `src/test/java/com/revature/qea/runners/`, create `RunCucumberTest` exactly as in Section 4. Adjust the glue packages to your real package names.
2. In `pom.xml`, confirm these test-scope dependencies exist: `cucumber-java`, `cucumber-junit-platform-engine`, `cucumber-picocontainer`, `junit-jupiter`, `junit-platform-suite` (versions are examples; check them).
3. Run `mvn clean test`. **Expected output:** `Running com.revature.qea.runners.RunCucumberTest`, `pretty` output for each scenario, and a line like `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`. Write down the number of tests.

**Part B: Select by tag**

4. Run `mvn test -Dcucumber.filter.tags="@smoke"`. **Expected:** a smaller number of tests. If the number is unchanged, the annotation on the runner is winning over `-D`. Move the tag default into `cucumber.properties` (remove the tag annotation from the runner) and retry. Record what you observed.
5. Run with `-Dcucumber.filter.tags="@smoke and not @slow"`. Predict the count before you run.

**Part C: Dry run**

6. Add a new step line to a scenario without implementing it. Run `mvn test -Dcucumber.execution.dry-run=true`. **Expected:** the undefined step is reported, no browser opens, and the run takes seconds. Remove the extra step.

**Part D: Break it on purpose**

7. Rename the runner class to `CucumberRunner`. Run `mvn clean test`. **Expected:** `Tests run: 0` or "No tests were executed". Rename it back. Lesson: Surefire's naming pattern.
8. Change the glue to a package that does not exist (`com.revature.qea.stepz`). **Expected:** every step is reported undefined with snippet suggestions. Fix it. Lesson: glue controls step discovery.
9. Change `@IncludeEngines("cucumber")` to `@IncludeEngines("junit-jupiter")`. **Expected:** zero scenarios run. Fix it. Lesson: the engine id selects the Cucumber engine.

**Part E: Failure and rerun**

10. Add `rerun:target/rerun.txt` to the plug-ins. Make one scenario fail (change an expected text). Run `mvn clean test`.
11. Open `target/rerun.txt`. **Expected:** one line such as `file:///.../features/login.feature:20`. Restore the text.
12. Try `mvn test -Dcucumber.features=@target/rerun.txt` and check the number of tests executed. Did only one scenario run, or the whole suite? Explain which, using the caveat in Section 8.

**Part F: Parallel (optional)**

13. Create `src/test/resources/junit-platform.properties` with the three parallel lines (parallelism 2). Run `mvn clean test` and compare the time to Part A. Note whether console output is interleaved.

**Deliverable:** a short text file (`lab-notes.md`) listing each part, what you predicted, what happened, and the one-sentence lesson.

---

## Practice Exercises

1. **Explain the runner.** For each line of `RunCucumberTest`, write one sentence explaining its purpose.
2. **Two runners.** Create `RunSmokeTest` (`@smoke`) and `RunRegressionTest` (`@regression and not @smoke`). Run each by name with `mvn test -Dtest=...`. What happens with plain `mvn test`?
3. **Dry run.** Use the dry-run configuration to find any undefined steps in your suite without launching a browser.
4. **Assertion messages.** Change three assertions in your steps to include helpful messages, then break a scenario and read the failure output.
5. **Rerun.** Add the `rerun` plug-in, make a scenario fail, and look at `target/rerun.txt`. Then run only that scenario.
6. **Naming strategy.** Compare the IDE/test report with and without `cucumber.junit-platform.naming-strategy=long`.
7. **Parallel experiment.** Enable parallel execution with parallelism 2 on a suite of at least 6 scenarios. Compare the run time. Then temporarily introduce a `static WebDriver` and describe what goes wrong.
8. **Translate.** Convert this JUnit 4 runner to the JUnit 5 form: `@RunWith(Cucumber.class) @CucumberOptions(features="src/test/resources/features", glue="steps", tags="@smoke", plugin={"pretty"})`.
9. **Project 2 milestone.** Provide a single reliable runner for the Project 2 BDD layer, with documented commands for smoke and full runs.
10. **Thread-safety audit.** Search your Project 2 code for the keyword `static`. For each hit, write whether it is constant/read-only (safe) or mutable state (unsafe under parallel runs) and what you would change.
11. **Message order.** Write a JUnit 4 style assertion `assertEquals("Cart count", 3, actual)` and its correct JUnit 5 form. Explain in two sentences why a silent argument swap is dangerous.
12. **Precedence experiment.** Put `cucumber.filter.tags=@smoke` in `cucumber.properties`, and `@regression` in a runner annotation. Predict, then run, which tag wins and record the scenario count.

---

## Solutions and Hints

1. **Explain the runner.** `@Suite`: this class describes a suite. `@IncludeEngines("cucumber")`: only the Cucumber engine participates. `@SelectClasspathResource("features")`: discover feature files in that classpath folder. The three `@ConfigurationParameter` lines supply glue packages, report plug-ins, and the tag expression. The empty body shows that annotations are the whole configuration.
2. **Two runners.** `-Dtest=RunSmokeTest` runs only that class. Plain `mvn test` runs **both** runners; a scenario tagged only `@smoke` runs once (the regression runner excludes it), which is why the regression expression says `and not @smoke`. If you had used `@regression` alone, scenarios with both tags would run twice. Hint: count the "Tests run" lines.
3. **Dry run.** `mvn test -Dcucumber.execution.dry-run=true`. Undefined steps print with snippets; nothing is executed against the browser.
4. **Assertion messages.** Example: `assertEquals(2, cart.getCount(), "Cart badge count after adding two products")`. The failure line then starts with that sentence, followed by `expected: <2> but was: <1>`.
5. **Rerun.** The file holds `file:///.../x.feature:LINE` entries. If `-Dcucumber.features=@target/rerun.txt` still runs everything, you have met the documented limitation: build a dedicated rerun runner or run the scenario from the IDE; check the count.
6. **Naming strategy.** With `long`, each test shows `Feature name - Scenario name`. Useful when different features have the same scenario names.
7. **Parallel experiment.** Expected with a static driver: random `NoSuchElementException`, scenarios landing on the wrong page, or `invalid session id`. The explanation: both threads use the same browser. The fix is the per-scenario `TestContext`.
8. **Translate.**

   ```java
   @Suite
   @IncludeEngines("cucumber")
   @SelectClasspathResource("features")
   @ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "steps")
   @ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "@smoke")
   @ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty")
   public class RunCucumberTest { }
   ```

   `features = "src/test/resources/features"` becomes the classpath name `features` because resources are copied to the classpath.
9. **Project 2 milestone.** A good README section lists `mvn clean test` (full), `mvn clean test -Dcucumber.filter.tags="@smoke"` (smoke), where the HTML report is, and the browser option. Check it by following it on a fresh clone.
10. **Thread-safety audit.** `private static final String BASE_URL = "https://www.saucedemo.com";` is safe (a constant). `private static WebDriver driver;` and `static int counter` that changes are unsafe. Fix: move into `TestContext` (instance field) or use `ThreadLocal`.
11. **Message order.** JUnit 4: `Assert.assertEquals("Cart count", 3, actual)`. JUnit 5: `Assertions.assertEquals(3, actual, "Cart count")`. When both are objects a swap may compile but the message becomes one of the compared values, producing confusing output.
12. **Precedence experiment.** Result depends on the setup; this exercise exists to make you test rather than guess. Record: which scenario count appeared, and which place you will use in future (the answer the course recommends: defaults in `cucumber.properties`, overrides through `-D`).

---

## Self-Check Questions

1. **Why does Cucumber need JUnit?** Cucumber executes features but does not integrate with IDEs, Maven, or CI servers; JUnit (the platform and the Cucumber engine) provides discovery, execution, and standard result reporting.
2. **What does `@IncludeEngines("cucumber")` do?** It limits the suite to the Cucumber test engine so other engines (such as Jupiter) do not take part.
3. **Your runner is named `CucumberRunner` and `mvn test` reports `Tests run: 0`. Why?** The name does not match Surefire's default patterns (`*Test`, `Test*`, `*Tests`, `*TestCase`). Rename it (for example `RunCucumberTest`) or configure `includes`.
4. **Why is a `static WebDriver` dangerous in parallel runs?** All threads share one browser, so scenarios interfere with each other; use a per-scenario `TestContext`, or a `ThreadLocal`.
5. **Does `-Dcucumber.features=@target/rerun.txt` always rerun only failures?** No. With `@SelectClasspathResource` on the suite it may not take effect and a dedicated rerun runner may be needed; check the scenario count.
6. **In JUnit 5, where does the assertion message go?** As the last argument: `assertEquals(expected, actual, message)`.
7. **Can I use `cucumber-junit` and `cucumber-junit-platform-engine` together?** Not in the same module; choose one, and for new work, the Platform engine.
8. **Why use `naming-strategy=long`?** So CI reports show the feature name in each test name, distinguishing scenarios with identical names in different features.

---

## Summary

- **JUnit** provides the test **runner infrastructure**: discovering tests, executing them, and reporting to IDEs and build tools. **Cucumber** supplies an **engine** that turns scenarios into JUnit tests.
- This course uses **JUnit 5 + `cucumber-junit-platform-engine`** with a `@Suite` class (`@IncludeEngines("cucumber")`, `@SelectClasspathResource`, `@ConfigurationParameter` for glue, plug-ins, tag filters); the **JUnit 4** `@RunWith(Cucumber.class)` + `@CucumberOptions` style exists in older projects and maps one-to-one.
- Use **JUnit 5 assertions** with messages in `@Then` steps; compare decimals with a tolerance; remember the message is the last argument in JUnit 5.
- Maintain **one runner per purpose**, avoid accidental double runs, and use the **rerun** plug-in to repeat failed scenarios, remembering that `-Dcucumber.features=@target/rerun.txt` may not work with `@SelectClasspathResource`.
- **Parallel execution** needs per-scenario drivers, independent scenarios, no static mutable state, and isolated test data.
- Most integration problems come from **dependency versions**, **engine selection**, **glue/feature paths**, and **runner naming**.
- All version numbers shown are **examples**; check current compatible versions.

---

## Additional Resources

- Cucumber-JVM, *cucumber-junit-platform-engine README*: https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-junit-platform-engine
- JUnit 5 User Guide: https://junit.org/junit5/docs/current/user-guide/
- Cucumber documentation, *Parallel execution*: https://cucumber.io/docs/cucumber/api/#parallel-execution
