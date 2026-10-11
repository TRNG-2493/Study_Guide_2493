# Hooks

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **hooks** are, why they exist, and how they differ from `Background` and from steps.
- Write `@Before` and `@After` hooks to **start and quit the browser** for every scenario.
- Use the `Scenario` object to **detect failure**, read names and tags, **attach screenshots** and **log text** to reports.
- Use `@BeforeStep` / `@AfterStep`, and `@BeforeAll` / `@AfterAll`, and describe when each runs.
- Control **execution order** with the `order` attribute, and explain why `@After` hooks run in the **reverse** order of `@Before` hooks.
- Trace what runs, and in which order, for a passing scenario, a failing scenario, and a scenario outline.
- Write **tagged hooks** that run only for selected scenarios.
- Share the driver with step definitions through the dependency-injected `TestContext` introduced on Thursday.
- Remove the temporary browser cleanup from the `Then` step and replace it with a proper `@After` hook.
- Diagnose common hook problems from their console symptoms (hooks not running, wrong order, leaked browsers).

---

## Why This Matters

### The problem from Thursday

On Thursday you built a working scenario, but its `Then` step contained a comment saying the browser cleanup there was **temporary**. The reason: if a scenario fails halfway, a cleanup in the final step **never runs**, because Cucumber skips the remaining steps after a failure. Browsers then pile up in memory (and on a build server, in processes that never end). You also had no way to take a **screenshot at the moment of failure**, as you learned on Monday.

### What a hook is

**Hooks** solve both problems. A **hook** is a block of Java code that Cucumber runs **automatically** at defined moments of the test lifecycle: before and after each scenario, before and after each step, and before and after the whole run. Hooks always run, even if the scenario failed, which makes them the right home for **technical setup and cleanup**: starting and quitting the browser, capturing evidence, resetting data, logging.

### An analogy: the stage crew

Picture a theatre. The actors (your steps) perform the story the audience came to see. Before every performance a stage crew sets the stage and switches on the lights; after every performance, **whatever happened on stage, even if the play was stopped halfway**, the crew switches off the lights and clears the stage. The audience (the business reader) does not watch the crew, and the script does not mention them, but the show cannot run safely without them. Hooks are the stage crew. The Background (previous lesson) is part of the play: the audience sees it.

### Where it fits in your project

Hooks are what make your Project 2 BDD layer *robust*: every scenario gets a fresh browser, every failure leaves a screenshot in the report, and no browser is left behind. Today's milestone ("complete the Project 2 BDD layer with tags and a report") needs hooks first, because the screenshots you attach here are what appear in the Cucumber report later today.

### What you already know that this builds on

| Earlier topic | How it is used here |
|---|---|
| `WebDriver`, `driver.quit()` | The hook decides *when* the browser starts and quits |
| Screenshots (Monday) | The failure hook uses `TakesScreenshot` |
| `TestContext` and PicoContainer (Thursday) | The hook class receives the same context as the steps |
| Background (previous lesson) | Runs after `@Before` hooks and before the scenario steps |

---

## The Concept

### 1. The Scenario Lifecycle

```
@BeforeAll                                   once, before the first scenario
 |
 +-- for EACH scenario (and each Examples row):
 |      @Before hooks                         e.g., start the browser
 |      Background steps
 |      +-- @BeforeStep -> step -> @AfterStep   around EVERY step
 |      scenario steps
 |      @After hooks                          e.g., screenshot if failed, quit the browser
 |
@AfterAll                                    once, after the last scenario
```

All hooks are Java methods annotated with annotations from the package `io.cucumber.java`:

| Annotation | Runs | Typical use |
|---|---|---|
| `@BeforeAll` | **Once**, before any scenario (static method) | Read configuration, start a shared service |
| `@Before` | Before **each scenario** | Start the browser, prepare data |
| `@BeforeStep` | Before **each step** | Logging, step counters |
| `@AfterStep` | After **each step** | Screenshot after every step (use sparingly) |
| `@After` | After **each scenario**, pass or fail | Screenshot on failure, quit the browser |
| `@AfterAll` | **Once**, after all scenarios (static method) | Clean up shared resources |

### 2. Hooks vs. Background vs. Steps

| | **Hooks** | **Background** | **Step** |
|---|---|---|---|
| Written in | Java | Gherkin | Gherkin (+ Java definition) |
| Visible to the business reader | No | Yes | Yes |
| Purpose | **Technical** setup/cleanup | **Business** context shared by all scenarios | The behavior itself |
| Runs when failures occurred earlier? | **Yes** (`@After` always runs) | No | No (skipped) |
| Example | Start/quit the browser | `Given the shopper is logged in` | `When the shopper adds ...` |

Rule of thumb: **if the business reader would not care, put it in a hook; if it is part of the story, put it in Gherkin.**

### 3. `@Before` and `@After`: Managing the Browser

Create the hooks class in the **glue package** (so Cucumber finds it):

```java
package com.revature.qea.steps;

import com.revature.qea.support.TestContext;
import io.cucumber.java.After;
import io.cucumber.java.Before;

public class Hooks {

    private final TestContext context;

    public Hooks(TestContext context) {          // injected by PicoContainer, shared with step classes
        this.context = context;
    }

    @Before
    public void startBrowser() {
        context.driver();                         // creates the browser (lazy accessor from Thursday)
    }

    @After
    public void quitBrowser() {
        context.quitDriver();                     // ALWAYS runs, even when the scenario failed
    }
}
```

**Line-by-line explanation**

| Line | What it does |
|---|---|
| `package com.revature.qea.steps;` | The hooks class must be inside a package that your runner lists as **glue**, or Cucumber never scans it |
| `import io.cucumber.java.After; ... Before;` | The Cucumber annotations (not the JUnit ones of the same name) |
| `public class Hooks` | A plain class; no class-level annotation is needed |
| `private final TestContext context;` | Field holding the per-scenario shared object from Thursday |
| `public Hooks(TestContext context)` | Constructor injection: PicoContainer sees the parameter type and passes in the **same** `TestContext` it gives to the step classes of the same scenario |
| `@Before public void startBrowser()` | Marks the method as a hook that runs before each scenario (and before the Background) |
| `context.driver();` | Calls the lazy accessor; the first call creates the browser (through `DriverFactory`) and stores it in the context |
| `@After public void quitBrowser()` | Runs after each scenario, whether it passed or failed |
| `context.quitDriver();` | Calls `driver.quit()` (if a driver exists) and clears the field |

Key points:

- Hook classes are normal classes in the **glue** path.
- Because the **same `TestContext` instance** is injected into `Hooks` and into the step classes **for a scenario**, the browser started in `@Before` is the browser the steps use, and `@After` closes that very browser.
- **A new `TestContext` (and thus a new browser) is created for each scenario**, so scenarios cannot affect each other.
- Hook methods may declare **no parameters** or a single **`Scenario`** parameter.

#### Removing the Thursday temporary cleanup

On Thursday your final `Then` step looked something like this:

```java
@Then("the customer sees the products page")
public void theCustomerSeesTheProductsPage() {
    assertTrue(new InventoryPage(context.driver()).isLoaded());
    context.quitDriver();      // TEMPORARY: remove when the @After hook exists
}
```

Now that `Hooks.quitBrowser()` exists, **delete the `context.quitDriver();` line** (and its comment) from that step and from any other step where you added the same temporary call:

```java
@Then("the customer sees the products page")
public void theCustomerSeesTheProductsPage() {
    assertTrue(new InventoryPage(context.driver()).isLoaded());
}
```

Why it matters: a step should only *check*. If the assertion on the line above fails, it throws an `AssertionError`, and the line below it never executes: the browser stays open. The `@After` hook runs in every case. Leaving both in place would not break anything (`quitDriver()` is safe to call twice because it checks for `null`), but it would hide the real design and confuse the next reader. Search your project for the text `quitDriver` and make sure only the hook calls it.

### 4. The `Scenario` Object

Cucumber can pass an `io.cucumber.java.Scenario` into a hook (and also into step definitions):

```java
@After
public void afterScenario(Scenario scenario) {
    String name   = scenario.getName();             // scenario title
    boolean failed = scenario.isFailed();           // true if any step failed
    Status status = scenario.getStatus();           // PASSED, FAILED, SKIPPED, UNDEFINED, PENDING, ...
    Collection<String> tags = scenario.getSourceTagNames();   // e.g. ["@smoke", "@login"]
    String id     = scenario.getId();
    String line   = scenario.getUri() + ":" + scenario.getLine();
}
```

(`Status` is `io.cucumber.java.Status`; `Collection` is `java.util.Collection`.)

| Method | Returns / does |
|---|---|
| `getName()` | The scenario name (for outlines, the expanded name) |
| `isFailed()` | `true` if the scenario has failed |
| `getStatus()` | An enum value, `Status.PASSED`, `FAILED`, and so on |
| `getSourceTagNames()` | Tags (including inherited tags) with the `@` |
| `getUri()` / `getLine()` | Feature file location |
| `attach(byte[] data, String mediaType, String name)` | **Attach a file** (e.g. a PNG screenshot) to the report |
| `attach(String data, String mediaType, String name)` | Attach text (JSON, HTML, plain text) |
| `log(String text)` | Add a text log line to the report |

Think of the `Scenario` object as the scenario's **notebook and name tag**: you can read who it is (name, tags) and how it is going (status), and you can paste evidence into it (attachments, log lines) which the report later displays.

### 5. Screenshot on Failure

This is the hook you have been waiting for since Monday's *Screenshots* lesson:

```java
package com.revature.qea.steps;

import com.revature.qea.support.TestContext;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

public class Hooks {

    private final TestContext context;

    public Hooks(TestContext context) {
        this.context = context;
    }

    @Before(order = 0)
    public void startBrowser(Scenario scenario) {
        scenario.log("Starting scenario: " + scenario.getName());
        context.driver();
    }

    @After(order = 10)                                         // runs BEFORE the quit hook (see Section 7)
    public void captureScreenshotOnFailure(Scenario scenario) {
        if (scenario.isFailed()) {
            WebDriver driver = context.driver();
            byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            scenario.attach(png, "image/png", "Failure: " + scenario.getName());
        }
    }

    @After(order = 0)                                          // runs AFTER the screenshot hook
    public void quitBrowser() {
        context.quitDriver();
    }
}
```

**Line-by-line explanation**

| Line | What it does |
|---|---|
| `@Before(order = 0)` | A before-hook with an explicit order position (lower numbers run earlier for `@Before`) |
| `scenario.log(...)` | Adds a text line to this scenario's report entry |
| `@After(order = 10)` | An after-hook with a **higher** number, so it runs **earlier** than order 0 (see Section 7) |
| `if (scenario.isFailed())` | Only take a picture when something went wrong; passing scenarios skip the cost |
| `((TakesScreenshot) driver)` | Selenium's interface for screenshots; the browser driver implements it, so we cast |
| `getScreenshotAs(OutputType.BYTES)` | Returns the PNG as a `byte[]` (instead of a file) |
| `scenario.attach(png, "image/png", name)` | Pastes the bytes into the report with the media type that tells the report how to show them |
| `@After(order = 0) quitBrowser()` | Runs last, closing the browser after the picture was taken |

What happens when a scenario fails: the failing step throws, remaining steps are skipped, then `@After` hooks run. The screenshot hook sees `isFailed() == true`, takes the picture **while the browser is still open**, and **attaches** it to the scenario's result; the report shows it (see the *Cucumber Reporting* lesson). Finally the quit hook closes the browser.

You can reuse the `ScreenshotUtil.captureBytes(driver)` helper from Monday instead of casting inline.

**Caveat:** if the browser itself crashed, taking a screenshot throws an exception. An exception inside a hook fails the hook and can hide the real failure. Wrap it in `try/catch` so a screenshot problem does not hide the cause:

```java
try {
    // take and attach the screenshot
} catch (Exception e) {
    scenario.log("Could not capture screenshot: " + e.getMessage());
}
```

### 6. `@BeforeStep` and `@AfterStep`

They run around **every step** (including Background steps):

```java
@AfterStep
public void afterEachStep(Scenario scenario) {
    // Example: attach a screenshot after EVERY step (slow; use only for debugging or demos)
    byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
    scenario.attach(png, "image/png", "After step");
}
```

Use them with care: they multiply the cost by the number of steps. Good uses: step-level logging, a "slow motion" delay for a demo, capturing the screenshot **only when a step fails** (check `scenario.isFailed()` in `@AfterStep`, which becomes true as soon as a step has failed, to get a screenshot of the precise failing state before later hooks):

```java
@AfterStep
public void screenshotAfterFailingStep(Scenario scenario) {
    if (scenario.isFailed() && context.hasDriver()) {
        byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", "State right after the failing step");
    }
}
```

Be aware that the `@AfterStep` hook also runs for the steps that are *skipped* after a failure, so with this code you could attach the same picture several times. A common refinement is to track a flag in the `TestContext` so the picture is taken only once. For most projects the single `@After` screenshot is enough.

A simple step counter with `@BeforeStep`:

```java
private int stepNumber = 0;

@BeforeStep
public void countStep() {
    stepNumber++;
    System.out.println("   step #" + stepNumber);
}
```

(A new `Hooks` object is created for every scenario, so the field starts at 0 each time.)

### 7. Execution Order

Several hooks of the same type can exist (in several classes). Control their order with the **`order`** attribute (default is `10000`):

- **`@Before` hooks run in ascending order** (`order = 0` before `order = 10`).
- **`@After` hooks run in descending order** (`order = 10` before `order = 0`): the **reverse**.

The reverse order of `@After` mirrors how setup and teardown are normally nested: the thing set up **first** is torn down **last**. Think of getting dressed: socks, then shoes; undressing: shoes first, then socks. In the example above: browser started at `order = 0`; the screenshot hook at `order = 10` runs first on the way out (while the browser still exists); the quit hook at `order = 0` runs last.

| Hook | `order` | Runs |
|---|---|---|
| `@Before startBrowser` | 0 | 1st before |
| `@Before loadTestData` | 10 | 2nd before |
| `@After captureScreenshot` | 10 | 1st after |
| `@After quitBrowser` | 0 | 2nd after |

If you do not use `order`, the sequence between hooks in different classes is **not defined**; whenever one hook depends on another, **set the order explicitly**. Between hooks and Background: all `@Before` hooks complete before the Background starts.

#### Execution trace: passing scenario

Assume the `Hooks` class from the Complete Example, a Background `Given the shopper is logged in`, and a scenario with two steps:

```
@Before(order=0)  setUp                        browser opens
Background        Given the shopper is logged in
   @BeforeStep / @AfterStep                    (if you wrote them)
Scenario          When the shopper adds "Sauce Labs Backpack" to the cart
Scenario          Then the cart count shows 1
@After(order=10)  screenshotOnFailure          isFailed() == false -> does nothing
@After(order=0)   tearDown                     browser quits
```

#### Execution trace: failing scenario

Now the `Then` step fails (the cart shows 0):

```
@Before(order=0)  setUp                        browser opens
Background        Given the shopper is logged in         PASSED
Scenario          When ... adds Backpack                 PASSED
Scenario          Then the cart count shows 1            FAILED  (AssertionError)
@After(order=10)  screenshotOnFailure          isFailed() == true -> PNG attached
@After(order=0)   tearDown                     browser quits
```

#### Execution trace: scenario outline with two rows

```
@BeforeAll                                      once
  Row 1:  @Before -> Background -> steps -> @After      (browser 1)
  Row 2:  @Before -> Background -> steps -> @After      (browser 2, new TestContext)
@AfterAll                                       once
```

#### Execution trace: three hooks with orders 5, 1, 10

```
@Before orders 5, 1, 10  run as   1, 5, 10
@After  orders 5, 1, 10  run as   10, 5, 1
```

### 8. Tagged Hooks

A hook can be limited to scenarios whose **tags** match an expression:

```java
@Before("@api")
public void prepareApiData() { ... }                // only for scenarios tagged @api

@Before("@ui and not @slow")
public void startFastBrowser() { ... }

@After("@cleanup")
public void deleteTestUser() { ... }
```

This is very effective for heavy setup that only some scenarios need: tag the scenarios, tag the hook, and the cost is paid only where needed. Tag expressions use `and`, `or`, `not`, and parentheses; they are explained fully in the next lesson, *Tags*. With attributes: `@Before(value = "@ui", order = 5)`.

An important design point: if you restrict the browser start to `@Before("@ui")`, then **every scenario that uses the browser must be tagged `@ui`** (usually once, on the Feature). A UI scenario that forgets the tag will still work, because `context.driver()` is lazy and creates the browser on first use, but the hook-based screenshot and quit logic should then also be written so that it checks `context.hasDriver()`, as in the Complete Example.

### 9. `@BeforeAll` and `@AfterAll`

Run **once per test run**. They must be **`static`** and cannot take a `Scenario` (there is none yet):

```java
public class RunHooks {

    @BeforeAll
    public static void beforeAll() {
        System.out.println("Test run started. Browser = " + System.getProperty("browser", "chrome"));
        // e.g., create the folder for screenshots, clear old report files
    }

    @AfterAll
    public static void afterAll() {
        System.out.println("Test run finished");
        // e.g., summarize results, shut down shared services
    }
}
```

Use them for **expensive one-time work** (loading configuration, starting an embedded service). Do not start a *shared* browser here: scenarios would then share state, which breaks independence. Because they are static, they cannot use the injected `TestContext`.

(Note: the JUnit Jupiter annotations `org.junit.jupiter.api.BeforeAll` look similar; make sure you import the Cucumber ones from `io.cucumber.java`.)

### 10. Dependency Injection and Hooks

Because `Hooks` takes `TestContext` in its constructor, PicoContainer builds **one object graph per scenario**:

```
Scenario starts
   +- PicoContainer creates:  TestContext (1 instance)
                              +-> Hooks(TestContext)
                              +-> LoginSteps(TestContext)
                              +-> CartSteps(TestContext)
Scenario ends -> all instances are discarded
```

So everything in a scenario shares the same driver, and nothing leaks into the next scenario. **Avoid `static` WebDriver fields**, which would be shared across scenarios (and across threads when running in parallel, see the *JUnit Integration* lesson).

This relies on the `cucumber-picocontainer` dependency in your `pom.xml`, which you added on Thursday. If it were missing, Cucumber could not construct a `Hooks` object with a constructor parameter.

### 11. Other Useful Hook Ideas

| Use | Hook | Notes |
|---|---|---|
| Add the browser name/version to the report | `@Before` with `scenario.log(...)` | Handy when running several browsers |
| Reset data to a known state | `@Before("@db")` | Tag-driven |
| Clear cookies between scenarios | Not needed with a fresh browser per scenario | |
| Capture browser console logs on failure | `@After` | Attach as text |
| Record scenario duration | `@Before` start time / `@After` compute | Store in `TestContext` |
| Delete test data created by the scenario | `@After("@cleanup")` | Must not fail the scenario |

### 12. Troubleshooting with Console Symptoms

**Symptom 1: The hooks never run (no banner printed, no failure screenshot, browsers left open).**

Because the driver is created lazily, the steps may still work (the first `context.driver()` call opens the browser), which makes this bug easy to miss. Cause: the `Hooks` class is not in a package listed in the runner's `glue`. Cucumber only scans the glue packages, and it does not warn you about classes outside them. Diagnosis: add a `System.out.println` in the hook; if it never prints, check the `GLUE_PROPERTY_NAME` value against the package name of the class (`com.revature.qea.steps`).

**Symptom 2: A screenshot hook runs after the quit hook.**

With the lazy `TestContext.driver()` from Thursday, calling it after `quitDriver()` would silently start a **brand new** browser (because the field was cleared), take a screenshot of a blank page, and leave that new browser open. If your code held the driver directly instead you would see something like:

```
org.openqa.selenium.NoSuchSessionException: invalid session id
```

or `Session ID is null. Using WebDriver after calling quit()?`. Diagnosis: print the hook names when they run, and check that the screenshot hook has the **higher** `order` among the `@After` hooks. This is also why the guard `context.hasDriver()` is useful.

**Symptom 3: A static-method error at start-up.**

A `@BeforeAll` or `@AfterAll` method that is not `static` is rejected when Cucumber loads the glue, with an error saying the method must be static. Fix: add `static`.

**Symptom 4: Lots of Chrome or chromedriver processes remain after a failing run.**

The browser was only closed in a step, or the `@After` hook threw an exception before `quitDriver()` (for example, a screenshot failure). Fix: keep `quitBrowser()` as its own hook with the lowest `order`, and wrap risky work in `try/catch`.

**Symptom 5: The hook runs but "does nothing useful" for a scenario.**

Check the tag expression on the hook: `@Before("@ui")` will skip scenarios without that tag. Print `scenario.getSourceTagNames()` to see which tags the scenario really has.

**Symptom 6: Duplicate hooks run twice.**

Two classes in the glue define the same logic (for example, an old `Hooks` and a new `Hooks2`). Search the project for `@Before` and `@After`.

### 13. Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Cleanup in the last `Then` step | Browser left open after failures | `@After` hook |
| `static WebDriver` shared by all scenarios | State leaks; breaks parallel runs | Per-scenario `TestContext` |
| Screenshot hook running **after** the quit hook | Blank screenshot from a new browser, or `NoSuchSessionException` | Give the screenshot hook a **higher** `order` for `@After` |
| Hook class not in the glue package | Hooks silently do not run | Put it under a package listed in `glue` |
| Importing `org.junit.jupiter.api.Before...` instead of `io.cucumber.java.Before` | Hook never runs or compile error | Check imports |
| Putting business steps (login) in a hook | Hidden behavior, confusing reports | Use `Background` or steps |
| Throwing exceptions in `@After` | Masks the real failure | Catch and log |
| Heavy `@AfterStep` screenshots in every run | Very slow, huge reports | Only on failure/debug |
| Assuming `@Before` order across classes without `order` | Random behavior | Set `order` explicitly |
| `@BeforeAll` method not static | Error | Make it `static` |

---

## Hands-On Lab: From Temporary Cleanup to Robust Hooks

Goal: replace the Thursday cleanup with hooks, prove they run when a scenario fails, and see a screenshot attached.

1. **Find the old cleanup.** In your project, search for `quitDriver()` and open the step that contains the temporary call.
2. **Create `Hooks.java`** in `src/test/java/com/revature/qea/steps/` using the Complete Example below. Check the import list: every annotation must come from `io.cucumber.java`.
3. **Delete the temporary call** from the `Then` step.
4. **Run a green suite:** `mvn clean test`. Expected console output (shortened):

   ```
   === Test run started (browser=chrome) ===
   ...
   3 Scenarios (3 passed)
   ...
   === Test run finished ===
   [INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
   ```
   Watch the desktop: a browser opens and closes for each scenario.
5. **Force a failure.** In the login feature, change an expected message to something wrong, for example `Epic sadface: Wrong text`. Run again.
6. **Read the failure.** Expected output (shortened):

   ```
   Failures:
     Scenario: ...
       Then the error message "Epic sadface: Wrong text" is displayed
       org.opentest4j.AssertionFailedError: expected: <Epic sadface: Wrong text> but was: <Epic sadface: Username and password do not match any user in this service>
   ```
   Confirm that the browser **still closed** (no window left behind), even though the failing `Then` step never reached any cleanup of its own.
7. **Confirm the attachment.** Cucumber's HTML report (set up in the *Cucumber Reporting* lesson) will show the PNG. For now, confirm that your `scenario.log` line ("Scenario: ...") appears in the pretty output, and temporarily write the PNG bytes to `target/failure.png` with `Files.write(Path.of("target/failure.png"), png)` inside the hook to see the picture directly. Remove that line afterwards.
8. **Swap the order.** Change the screenshot hook to `order = 0` and the quit hook to `order = 10`, remove the `hasDriver()` check, and rerun the failing scenario. Observe the symptom described in "Symptom 2". Then restore the correct orders.
9. **Add a tag.** Tag the Feature `@ui` and change `setUp` to `@Before(value = "@ui", order = 0)` as in the *Tags* lesson. Run again to confirm nothing changed.
10. Commit: `Add Cucumber hooks for browser lifecycle and failure screenshots`.

---

## Complete Example

**`TestContext`** (from Thursday, final version)

```java
package com.revature.qea.support;

import com.revature.qea.drivers.DriverFactory;
import org.openqa.selenium.WebDriver;

public class TestContext {

    private WebDriver driver;

    public WebDriver driver() {
        if (driver == null) {
            driver = DriverFactory.createDriver(
                    System.getProperty("browser", "chrome"),
                    Boolean.parseBoolean(System.getProperty("headless", "false")));
        }
        return driver;
    }

    public boolean hasDriver() {
        return driver != null;
    }

    public void quitDriver() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }
}
```

Reading `TestContext`: `driver()` is a **lazy accessor**: the browser is created the first time somebody asks for it. `hasDriver()` lets a hook ask "is there a browser?" **without** accidentally creating one. `quitDriver()` closes the browser if present and sets the field to `null`, so calling it twice is harmless. The browser name and headless flag come from system properties (`-Dbrowser=firefox -Dheadless=true`), with defaults.

**`Hooks`**

```java
package com.revature.qea.steps;

import com.revature.qea.support.TestContext;
import io.cucumber.java.After;
import io.cucumber.java.AfterAll;
import io.cucumber.java.Before;
import io.cucumber.java.BeforeAll;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

public class Hooks {

    private final TestContext context;

    public Hooks(TestContext context) {
        this.context = context;
    }

    @BeforeAll
    public static void beforeAll() {
        System.out.println("=== Test run started (browser="
                + System.getProperty("browser", "chrome") + ") ===");
    }

    @Before(order = 0)
    public void setUp(Scenario scenario) {
        scenario.log("Scenario: " + scenario.getName());
        context.driver();                                   // start the browser
    }

    @After(order = 10)
    public void screenshotOnFailure(Scenario scenario) {
        if (scenario.isFailed() && context.hasDriver()) {
            try {
                byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
                scenario.attach(png, "image/png", "Failure screenshot");
            } catch (Exception e) {
                scenario.log("Could not take screenshot: " + e.getMessage());
            }
        }
    }

    @After(order = 0)
    public void tearDown() {
        context.quitDriver();
    }

    @AfterAll
    public static void afterAll() {
        System.out.println("=== Test run finished ===");
    }
}
```

Walkthrough of one failing scenario, hook by hook:

1. `beforeAll` prints the banner once, before any scenario.
2. `setUp` logs the scenario name into the report and creates the browser.
3. The steps run; one throws, and the rest are skipped.
4. `screenshotOnFailure` (order 10, runs first among the `@After` hooks) sees the failure and the live browser, takes a PNG, and attaches it. The `try/catch` protects the real failure from being replaced by a screenshot problem.
5. `tearDown` (order 0, runs last) quits the browser.
6. After the last scenario, `afterAll` prints the closing banner.

Run `mvn clean test`. Then deliberately break one scenario (for example, change an expected error message) and rerun. You should see the scenario fail, the browser close, and a failure screenshot attached to the report (next lessons show how to view it).

---

## Practice Exercises

1. **Replace the temporary cleanup.** Remove `context.quitDriver()` from your `Then` step, add the `Hooks` class, and run the whole suite. Confirm that no browser is left open even when you force a failure.
2. **Order experiment.** Add three `@Before` hooks with orders 5, 1, and 10 that print their number, and three `@After` hooks with the same orders. Predict the output, then run to verify the ascending/descending rule.
3. **Screenshot order bug.** Swap the `order` values so the quit hook runs before the screenshot hook, and remove the `hasDriver()` guard. What do you observe and why?
4. **Scenario info.** Print the scenario name, status, and tags in an `@After` hook. What do you get for a `Scenario Outline` row?
5. **Tagged hook.** Create a hook `@Before("@slow")` that prints a warning and observe that it only runs for scenarios tagged `@slow` (tags are explained in the next lesson; use the example tag now).
6. **BeforeStep logging.** Use `@BeforeStep` to print each step number and `@AfterStep` to attach a screenshot only if the scenario has failed so far.
7. **Run-level hooks.** Use `@BeforeAll` to print the run configuration and `@AfterAll` to print how many scenarios ran (use a static counter updated in `@After`).
8. **Safe hook.** Rewrite the failure screenshot hook so that a crash of the browser does not hide the original failure. Which statements go inside the `try` block?
9. **Explain it.** In two or three sentences, explain to a classmate why cleanup belongs in `@After` and not in the last `Then` step.
10. **Duration hook.** Store `System.currentTimeMillis()` in a field in `@Before` and, in `@After`, log the scenario duration with `scenario.log`.
11. **Hook or Background?** Decide for each: (a) start the browser, (b) log in as `standard_user`, (c) attach a screenshot on failure, (d) "the cart is empty".
12. **Project 2 milestone.** Add `Hooks` to your Project 2 repository, remove all manual browser cleanup, and show a failure screenshot in your run output.

---

## Solutions and Hints

**1.** After the change, `grep -r quitDriver src` (or the IDE search) should find it only in `TestContext` and `Hooks`. A forced failure should still leave no browser window open.

**2.** Output: `@Before` hooks print 1, 5, 10; `@After` hooks print 10, 5, 1. Ascending for before, descending for after.

**3.** With the lazy accessor: after `tearDown` clears the field, `screenshotOnFailure` calls `context.driver()`, which silently starts a **new** browser, photographs a blank page, and leaves the new browser open (a leaked process). If you instead kept a direct reference to the quit driver, you would get a `NoSuchSessionException`. The cause is the order: `@After` runs highest `order` first, so the screenshot hook needs the higher number.

**4.** The name is the **expanded** title of the row; `scenario.getStatus()` prints `PASSED` or `FAILED`; `getSourceTagNames()` shows the inherited tags with `@`.

**5.** Output only appears for scenarios whose (inherited) tags include `@slow`.

**6.**

```java
private int step = 0;

@BeforeStep
public void beforeStep() { System.out.println("step " + (++step)); }

@AfterStep
public void afterStep(Scenario scenario) {
    if (scenario.isFailed() && context.hasDriver()) {
        scenario.attach(((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES),
                "image/png", "After failing step");
    }
}
```

**7.** Use `private static int count;` incremented in an `@After` hook, and print it in `@AfterAll`. Remember `@AfterAll` must be static.

**8.** Put everything that touches the browser (`getScreenshotAs` and `attach`) inside `try`, and log in `catch` with `scenario.log`. Do not rethrow.

**9.** Example: "A step after a failing step is skipped, so cleanup in the last step does not run. `@After` always runs, so the browser is closed no matter what happens."

**10.**

```java
private long start;

@Before(order = 0)
public void begin() { start = System.currentTimeMillis(); }

@After(order = 5)
public void end(Scenario scenario) {
    scenario.log("Duration ms: " + (System.currentTimeMillis() - start));
}
```

**11.** (a) Hook: technical. (b) Background: business context. (c) Hook: technical evidence. (d) Gherkin step or Background: it is business context.

**12.** Hint: keep screenshots for failures only, so passing runs stay fast.

---

## Self-Check Questions

**Q1. Which hook runs even when a step fails?**
`@After` (and `@AfterStep` for the failing step itself).

**Q2. In what order do `@Before` hooks with `order` 0 and 10 run?**
0 first, then 10.

**Q3. In what order do `@After` hooks with `order` 0 and 10 run?**
10 first, then 0 (reverse).

**Q4. Why must a screenshot hook have a higher `@After` order than the quit hook?**
So it runs first, while the browser is still open.

**Q5. How does the `Hooks` class get the same browser as the steps?**
PicoContainer injects the same per-scenario `TestContext` into both through their constructors.

**Q6. Why must `@BeforeAll` methods be static?**
They run once before any scenario exists, so no per-scenario object (with its injected context) is available.

**Q7. Does a hook run once per outline row?**
Yes: `@Before` and `@After` run for each row; `@BeforeAll` and `@AfterAll` run once per run.

**Q8. When should a login be a hook?**
Almost never: login is business context and belongs in a Background or step.

---

## Summary

- **Hooks** are Java methods that Cucumber runs automatically at lifecycle points: `@BeforeAll`, `@Before`, `@BeforeStep`, `@AfterStep`, `@After`, `@AfterAll`. They hold **technical** setup and cleanup; business context belongs in `Background` and steps.
- `@After` runs **even when the scenario fails**, so it is the right place to **quit the browser** and **capture evidence**.
- The **`Scenario`** parameter provides `isFailed()`, `getStatus()`, `getName()`, tags, and `attach(...)`/`log(...)` for adding **screenshots and text to the report**.
- `@Before` runs in **ascending** `order`, `@After` in **descending** `order`; use `order` whenever hooks depend on each other (screenshot **before** quit).
- **Tagged hooks** (`@Before("@api")`) run only for matching scenarios.
- Share the driver through the **per-scenario `TestContext`** injected into hooks and steps; avoid **static drivers**.
- Remove the temporary cleanup from the `Then` step; the `@After` hook replaces it. Protect hooks from throwing exceptions that hide the real failure.

---

## Additional Resources

- Cucumber documentation, *Hooks*: https://cucumber.io/docs/cucumber/api/#hooks
- Cucumber-JVM documentation, *Cucumber Java: hooks and the Scenario object*: https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-java
- Cucumber documentation, *Tag expressions*: https://cucumber.io/docs/cucumber/api/#tag-expressions
