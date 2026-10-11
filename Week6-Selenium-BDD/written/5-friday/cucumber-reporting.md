# Cucumber Reporting

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **why** reports matter and who reads them (testers, developers, managers, business stakeholders).
- Configure Cucumber's built-in **plug-ins**: `pretty`, `summary`, `progress`, `html`, `json`, `junit`, `message`, `rerun`, and `usage`, and say when each is the right choice.
- Generate an **HTML report** and read its sections (features, scenarios, steps, tags, attachments, failure details).
- Attach **screenshots** and **text logs** to the report from hooks and steps, including how a step reaches the `Scenario` object.
- Read the structure of the **JSON** output and generate an enhanced report from it with the **maven-cucumber-reporting** plug-in, and describe alternatives (Allure, ExtentReports).
- Understand what **Cucumber Reports / publish** does and how to disable it.
- Use the **JUnit XML** output for CI servers.
- Interpret results and distinguish **real failures** from **undefined/pending** steps and **flaky** scenarios, and classify failures.
- Complete the **Project 2 requirement**: a BDD layer with tags and a viewable report.

---

## Why This Matters

A test suite is only as useful as its **results are understandable**. A console wall of text tells *you* something; it tells the product owner nothing. The reasons teams invest in reporting:

- **Developers** need the failing step, the exception message, and a **screenshot** to reproduce a failure quickly.
- **Testers** need trends: which scenarios fail repeatedly (flaky), how long the suite takes.
- **Managers** want a one-page answer: *"Is the build healthy? How much is covered?"*
- **Business stakeholders** can read **living documentation**: the report shows the features in plain language, with the current pass/fail status.
- **Auditors/compliance** need evidence that tests were run and what they showed.

An analogy: a test run without a report is like a **medical check-up where the doctor says only "something is wrong"**. A good report is the **lab result sheet**: which measurement, what value, what the normal range is, and a photo (the screenshot). Everyone downstream (the patient, the specialist, the insurer) can act on it without redoing the examination.

Cucumber is strong here because the features are already readable; a good report is simply the **feature files with colored results**. In today's Project 2 milestone ("complete the Project 2 BDD layer with tags and a report") you must produce a report from your own saucedemo.com scenarios, including a failure screenshot, and document the command that produces it.

**Where you will use this:** after every local run (the HTML file is the first thing you open when something is red), in every CI job (attached as an artifact), in sprint reviews (to show the business what is covered), and in bug reports (the screenshot and step list go straight into the ticket).

---

## The Concept

### 1. Plug-ins: How Cucumber Produces Output

Cucumber emits **events** while it runs (test run started, scenario started, step finished, and so on). **Plug-ins** listen to these events and write them in some format. Think of a sports match: the match produces events (goal, foul, substitution); one reporter writes a live text commentary (the `pretty` plug-in), another keeps the final scoreboard (`summary`), a third produces the full statistics database (`json`). The match does not change; only the listeners differ.

You choose plug-ins with the **`cucumber.plugin`** configuration property (or `@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, ...)` in the runner). Multiple plug-ins are separated by commas; each can write to the **console** or to a **file** (`name:path`).

```java
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value =
    "pretty, summary, "
  + "html:target/cucumber-reports/report.html, "
  + "json:target/cucumber-reports/cucumber.json, "
  + "junit:target/cucumber-reports/cucumber.xml, "
  + "rerun:target/rerun.txt")
```

or in `cucumber.properties`:

```properties
cucumber.plugin=pretty, summary, html:target/cucumber-reports/report.html, json:target/cucumber-reports/cucumber.json
```

**Line-by-line:**

| Part | Meaning |
|---|---|
| `PLUGIN_PROPERTY_NAME` | The constant for the key `cucumber.plugin`. |
| `"pretty, summary, "` | Two plug-ins **without a path**: they print to the console. |
| `"html:target/cucumber-reports/report.html"` | The format name, a colon, then the output file. Missing folders are created automatically. |
| `+` between the string pieces | Plain Java string concatenation, used only so the long value fits on several lines. The **commas** inside the string are what separate plug-ins; spaces around them are ignored. |
| `rerun:target/rerun.txt` | A plug-in that writes the failed scenario locations (see the *JUnit Integration* lesson). |

**Where and when to configure:** put the plug-in list in **one place**. A good habit is `cucumber.properties` for the project defaults (so IDE and Maven runs behave the same) and the runner annotation only when one runner needs a different report file (for example `smoke.html`).

### 2. The Built-in Plug-ins

| Plug-in | Output | Used for |
|---|---|---|
| `pretty` | Console: every scenario and step, with colors and the matching step-definition location | Development, debugging |
| `summary` | Console: the totals at the end (scenarios and steps passed/failed/skipped) | Quick overview |
| `progress` | Console: one character per step (`.` pass, `F` fail, `-` skip, `U` undefined) | Compact output for big suites |
| `html:path` | A **single self-contained HTML file**, including screenshots | Sharing results with anyone; opens in a browser |
| `json:path` | A JSON file with **all** scenario and step details (including embedded attachments) | Input for report generators and dashboards |
| `junit:path` | An XML file in the **JUnit XML** format | CI servers that display test results |
| `message:path` | NDJSON "Cucumber messages" (the raw event stream) | Cucumber Reports service, advanced tools |
| `rerun:path` | Text file listing the **locations of failed scenarios** | Re-running only failures |
| `usage:path` | Which step definitions are used, how often, and how long they take; reveals **unused** step definitions | Maintenance |
| `timeline:dir` | An interactive **timeline** of parallel execution | Analyzing parallel runs |

(The exact set available can depend on the Cucumber version; `pretty`, `summary`, `html`, `json`, `junit`, `message`, `rerun`, and `usage` are standard in Cucumber 7.)

**Choosing plug-ins (when and why):**

| Situation | Recommended plug-ins | Reason |
|---|---|---|
| Writing a new scenario in the IDE | `pretty` | You see every step and where it matched |
| Local full run before a pull request | `pretty, summary, html:...` | Details plus a shareable file |
| Large suite in CI | `summary, html:..., json:..., junit:..., rerun:...` | Compact log, full artifacts |
| Parallel runs | `summary, html:..., timeline:target/timeline` | Interleaved console output is unreadable; use files |
| Maintenance day | add `usage:target/usage.json` | Find unused step definitions |

**Console output example (`pretty` + `summary`):**

```
Scenario: Locked-out customer cannot log in           # features/login.feature:20
  Given the customer is on the login page             # LoginSteps.theCustomerIsOnTheLoginPage()
  When the customer logs in with username "locked_out_user" and password "secret_sauce"
  Then the error message "Epic sadface: Sorry, this user has been locked out." is displayed

Failed scenarios:
file:///.../features/login.feature:20 # Scenario: Locked-out customer cannot log in

2 Scenarios (1 failed, 1 passed)
6 Steps (1 failed, 5 passed)
0m12.456s
```

**How to read it:**

| Part | Meaning |
|---|---|
| `Scenario: ... # features/login.feature:20` | The scenario name and its **file and line**; the line number is what `rerun.txt` stores. |
| `# LoginSteps.theCustomerIsOnTheLoginPage()` | The Java method that matched the step: a quick way to navigate from the text to the code. |
| `Failed scenarios:` | The list of locations of failed scenarios, ready to copy. |
| `2 Scenarios (1 failed, 1 passed)` | Totals at **scenario** level. |
| `6 Steps (1 failed, 5 passed)` | Totals at **step** level; skipped, undefined, and pending counts appear here too when present. |
| `0m12.456s` | Total wall-clock time of the run. |

**The `progress` plug-in** prints a character per step, for example `....F--.......`. It is compact but you must scroll to find the failure; prefer `summary` plus a file report.

### 3. The Built-in HTML Report

With `html:target/cucumber-reports/report.html` Cucumber 7 writes a **single HTML file** with no extra assets, so you can email it, attach it to a ticket, or upload it as a CI artifact. Open it in any browser.

What you can do in it:

- See **all features and scenarios** as a tree with pass/fail icons, plus totals.
- Expand a scenario to see each **step** (keyword and text), its **location**, and **duration**.
- For **failed steps**, read the **exception message and stack trace**.
- View **attachments**: screenshots, text, and logs that you attached from hooks/steps (Section 4).
- Filter by **status**, and search by scenario name or **tag**.
- See **Rule** names, **data tables**, and **doc strings** rendered nicely.
- See the **Examples** rows of an outline as separate scenarios.

Treat this report as the **default deliverable** of a test run.

**A guided tour of what you will see** (the layout can vary a little between Cucumber versions):

1. **Header and totals**: counts of passed, failed, skipped scenarios and the total duration. First question answered: *is this run green?*
2. **Feature list** (left or top): each `.feature` file by its `Feature:` title. A feature is red if any of its scenarios failed.
3. **Scenario blocks**: scenario title, its **tags** (`@smoke`, `@negative`), and each step in order with the keyword (`Given`, `When`, `Then`). Passed steps are green; the failed step is red with the error text below it; skipped steps after it are shown in a lighter color.
4. **Scenario Outline rows**: each Examples row appears as its own scenario with the placeholder values filled in, which is why meaningful outline titles (for example `Login as <username>`) matter.
5. **Attachments**: a small expandable item under the step or hook where `scenario.attach` or `scenario.log` was called. Screenshots display inline.

**Everyday uses:**

| Question | Where to look |
|---|---|
| "Which scenarios failed?" | Filter by failed status |
| "Why did this one fail?" | Red step, error message, screenshot |
| "Do we have any `@checkout` coverage?" | Search by tag |
| "Which step is slow?" | Step durations |

### 4. Attaching Screenshots and Text

Anything you attach with the `Scenario` object appears in the HTML (and JSON) report on the scenario or step where it was added.

```java
// Screenshot (PNG bytes)
byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
scenario.attach(png, "image/png", "Failure screenshot");

// Plain text and logs
scenario.log("Logged in as standard_user");                       // quick text line
scenario.attach("Browser: chrome 130", "text/plain", "Environment");

// JSON, HTML snippets, and so on
scenario.attach("{\"orderId\": 42}", "application/json", "Order response");
```

**Line-by-line:**

| Line | Explanation |
|---|---|
| `(TakesScreenshot) driver` | A **cast**: the `WebDriver` object is told to behave as a `TakesScreenshot` (Selenium's interface for screenshots), which the main browser drivers implement. |
| `getScreenshotAs(OutputType.BYTES)` | Takes the screenshot and returns it as raw bytes (`byte[]`) in memory rather than writing a file. |
| `scenario.attach(png, "image/png", "Failure screenshot")` | Three arguments: the **data**, its **media type** (MIME type, which tells the report how to display it), and a **name** shown in the report. |
| `scenario.log("...")` | The simplest attachment: a line of text. It is shown in the report next to the step where you logged it. |
| `scenario.attach("...", "text/plain", "Environment")` | The text overload: data as a `String`, with a media type and a name. |
| `"application/json"` | A different media type, so the report formats it as JSON. Use `text/plain` when unsure. |

The most important use is the **screenshot on failure**, done in the `@After` hook from the *Hooks* lesson:

```java
@After(order = 10)
public void screenshotOnFailure(Scenario scenario) {
    if (scenario.isFailed() && context.hasDriver()) {
        byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", "Failure: " + scenario.getName());
    }
}
```

**Line-by-line:**

| Line | Explanation |
|---|---|
| `@After(order = 10)` | Runs after every scenario. For `@After` hooks, a **higher `order` runs first**, so this hook (10) runs **before** the hook that quits the browser (for example `order = 1`). The order matters: a screenshot of a closed browser is impossible. |
| `Scenario scenario` | Cucumber **injects the current scenario** into the hook method parameter. |
| `scenario.isFailed()` | `true` when any step failed (it is `false` for passed scenarios). |
| `context.hasDriver()` | A guard: if the scenario failed before a browser ever started (for example a configuration error), there is nothing to photograph and no `NullPointerException` to mask the real problem. |
| `scenario.getName()` | The scenario title, so each screenshot is named in the report. |

You can also attach evidence in a **step definition** when you want proof of a *successful* key moment (for example, the order confirmation page). Cucumber passes the `Scenario` object only to **hooks** (a step definition method cannot receive it as a parameter), so the simple approach is to store it in the `TestContext` from a `@Before` hook (for example `context.setScenario(scenario)`, a small field and setter you add to `TestContext`) and use it from steps:

```java
// TestContext
private Scenario scenario;
public void setScenario(Scenario scenario) { this.scenario = scenario; }
public Scenario scenario() { return scenario; }

// Hooks
@Before(order = 0)
public void rememberScenario(Scenario scenario) {
    context.setScenario(scenario);
}

// A step definition
@Then("the order confirmation is displayed")
public void confirmationDisplayed() {
    assertTrue(confirmation.isDisplayed(), "Confirmation message");
    byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
    context.scenario().attach(png, "image/png", "Order confirmation page");
}
```

This is the same per-scenario `TestContext` that holds your driver: PicoContainer creates one per scenario, so each scenario attaches to **its own** report entry, even in parallel runs.

Cautions:

- Attach on **failure** (or at key milestones), not after every step; screenshots enlarge the report and slow the run.
- Do not capture screens that show **sensitive data**.
- Wrap capture code in `try/catch` so a screenshot error does not mask the real failure.

A safe version of the capture code:

```java
private void attachScreenshot(Scenario scenario, String title) {
    try {
        byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", title);
    } catch (Exception e) {
        scenario.log("Could not capture screenshot: " + e.getMessage());
    }
}
```

If the browser crashed, `getScreenshotAs` throws; the `catch` records that fact in the report and the original failure stays the headline.

### 5. Reading the Results: Statuses

| Status | Meaning | Action |
|---|---|---|
| **Passed** | Step/scenario succeeded | None |
| **Failed** | Assertion failed or exception thrown | Look at the message, stack trace, screenshot. Product defect, test defect, or environment problem? |
| **Skipped** | Not run because an earlier step failed | Fix the failing step first |
| **Undefined** | No matching step definition | Implement from the snippet |
| **Pending** | Step definition throws `PendingException` | Finish the implementation |
| **Ambiguous** | More than one definition matches | Make patterns distinct |

In Cucumber 7 (JVM) **undefined and pending** steps are treated as **errors** by default, so a scenario containing them makes the run fail instead of passing silently, which is what you want. Always check all the totals, not just the failure count.

Why this default is good: imagine the old behavior, where an undefined step was merely "yellow". A team writes ten scenarios, forgets the glue for the last step of each, and the build is **green** while nothing was verified. Treating undefined as an error closes that gap.

**Reading a failure:** work from the top: the *first* failed step is the cause; later steps are *skipped*. Look at the **exception type**:

| Exception | Usually means |
|---|---|
| `AssertionFailedError` (JUnit) | Expected and actual differ: possible product bug |
| `NoSuchElementException` / `TimeoutException` | Locator or timing problem, or the page is not what you expected: check the screenshot |
| `StaleElementReferenceException` | Test synchronization problem |
| `WebDriverException` (session, connection) | Environment/driver problem |

Learn to **classify**: *product defect* (the app is wrong), *test defect* (the test is wrong or flaky), or *environment issue*. Each has a different owner.

**Worked examples of reading failures** (messages shortened):

1. ```
   org.opentest4j.AssertionFailedError: Error message ==>
   expected: <Epic sadface: Sorry, this user has been locked out.> but was: <Epic sadface: Username and password do not match any user in this service>
   ```
   Reading: the page showed a message; it differs from the expectation. Open the screenshot. If the credentials in the scenario are wrong (a typo in the username), it is a **test defect**. If the credentials are right and the site changed its text, it is a **product change** to be confirmed with the owner of the requirement.

2. ```
   org.openqa.selenium.TimeoutException: Expected condition failed: waiting for visibility of element located by By.id: shopping_cart_badge (tried for 10 second(s) with 500 milliseconds interval)
   ```
   Reading: your explicit wait gave up. The screenshot shows the products page with no badge: the add-to-cart click did not happen (test defect, maybe an overlay) or the product was not added (product defect). Compare with a manual check.

3. ```
   org.openqa.selenium.NoSuchSessionException: invalid session id
   ```
   Reading: the browser or driver was closed or crashed before this step. Check whether an earlier hook quit the browser too early, whether parallel scenarios share a driver, or whether the machine ran out of memory: an **environment or framework** problem, not the app.

4. ```
   io.cucumber.junit.platform.engine.UndefinedStepException ... The step "the cart contains 2 items" is undefined
   ```
   Reading: no definition matches. Implement it from the suggested snippet, or fix the wording of the step so it matches the existing expression.

**A classification record** helps teams see patterns. In your bug tracker or your notes keep: scenario, status, first failed step, classification (product/test/environment), owner, action. After a week you will know which kind of failure dominates and where to invest.

### 6. The JSON Report and Beautiful Reports

The `json` plug-in records everything in machine-readable form; **report generators** transform it into richer dashboards. A simplified view of what the JSON contains (field names shown for orientation; open your own file to see the exact structure):

```json
[
  {
    "uri": "classpath:features/login.feature",
    "name": "Login",
    "elements": [
      {
        "keyword": "Scenario",
        "name": "Locked-out customer cannot log in",
        "tags": [ { "name": "@negative" } ],
        "steps": [
          {
            "keyword": "Given ",
            "name": "the customer is on the login page",
            "result": { "status": "passed", "duration": 523000000 }
          },
          {
            "keyword": "Then ",
            "name": "the error message \"...\" is displayed",
            "result": { "status": "failed", "duration": 31000000,
                        "error_message": "org.opentest4j.AssertionFailedError: ..." },
            "embeddings": [ { "mime_type": "image/png", "data": "iVBORw0KGgo..." } ]
          }
        ]
      }
    ]
  }
]
```

How to read it: the file is a **list of features**; each feature has `elements` (scenarios); each scenario has `steps`; each step has a `result` with `status` and `duration` (in **nanoseconds**, so 523000000 is about half a second) and, when a screenshot was attached, `embeddings` with the **Base64-encoded** image. This is why the JSON file can become large when you attach many screenshots.

A popular generator for Cucumber with Maven is **maven-cucumber-reporting** (`net.masterthought`):

```xml
<plugin>
  <groupId>net.masterthought</groupId>
  <artifactId>maven-cucumber-reporting</artifactId>
  <version>5.8.1</version>   <!-- example version: check for the latest stable release -->
  <executions>
    <execution>
      <id>execution</id>
      <phase>verify</phase>
      <goals>
        <goal>generate</goal>
      </goals>
      <configuration>
        <projectName>QEA BDD Framework</projectName>
        <outputDirectory>${project.build.directory}/cucumber-html-reports</outputDirectory>
        <inputDirectory>${project.build.directory}/cucumber-reports</inputDirectory>
        <jsonFiles>
          <param>**/*.json</param>
        </jsonFiles>
      </configuration>
    </execution>
  </executions>
</plugin>
```

**Line-by-line:**

| Element | Meaning |
|---|---|
| `<groupId>net.masterthought</groupId>` ... `<artifactId>maven-cucumber-reporting` | The coordinates of the plug-in (from the Maven lesson: how any Maven artifact is identified). |
| `<version>5.8.1</version>` | An **example** version; check the project page for the current one. |
| `<executions><execution>` | One scheduled use of the plug-in; `<id>` names it. |
| `<phase>verify</phase>` | Run in the `verify` phase, which comes **after** `test`, so the JSON already exists. |
| `<goal>generate</goal>` | The plug-in task that builds the report site. |
| `<projectName>` | Title shown in the report header. |
| `<outputDirectory>` | Where the multi-page report is written. `${project.build.directory}` is Maven's name for `target`. |
| `<inputDirectory>` | Where to look for input files: the folder where the `json` plug-in writes. |
| `<jsonFiles><param>**/*.json</param>` | Pattern of input files: any `.json` below the input directory. |

Run it with the **`verify`** phase, which comes after `test`:

```
mvn clean verify
```

Result: a multi-page HTML site in `target/cucumber-html-reports/` with an **overview**, **feature/tag statistics**, **trends**, and **failure lists**; open `overview-features.html`. (Note: with `verify` and Surefire's default `testFailureIgnore=false`, a **failing test stops the build before the `verify` phase**, so the report would not be generated. Teams either set `<testFailureIgnore>true</testFailureIgnore>` in Surefire for this purpose or bind the report plug-in to a phase that always runs, or generate the report in a CI step with `if: always()`. Be aware that ignoring failures makes the **build status green** even with failed tests, so another step must fail the pipeline.)

**The three practical options, compared:**

| Option | How | Pro | Con |
|---|---|---|---|
| A. Ignore failures in Maven | `<testFailureIgnore>true</testFailureIgnore>` or `-Dmaven.test.failure.ignore=true` on the command line | Report is always generated, one command | Build is green despite failures; you need an extra check (for example a step that reads `rerun.txt` or the surefire XML and fails) |
| B. Always-run CI step | Run tests, then a separate step with `if: always()` (GitHub Actions) or `post { always { ... } }` (Jenkins) that calls `mvn cucumber-reporting:generate` or publishes the files | Pipeline status stays honest | Needs CI configuration |
| C. Use only the built-in HTML | No generator at all | Written during `test`, so it exists after failures | Fewer dashboards and trend pages |

For this course, option C is always available (the `html` plug-in writes the file during the test run, even on failure), and option A is fine for the local experiment below.

Other well-known options (brief mentions; your instructor may demonstrate one):

| Tool | Notes |
|---|---|
| **Allure Report** | Very popular, rich dashboards, history trends, attachments; uses an adapter (`allure-cucumber7-jvm`) |
| **ExtentReports** | Polished HTML reports with a Cucumber adapter, widely used in industry |
| **Serenity BDD** | A full framework that includes "living documentation" reports and its own page-object tooling |
| **Cucumber Reports (cloud)** | Cucumber's hosted sharing service (see below) |

For this course the **built-in HTML plus JSON/maven-cucumber-reporting** is enough.

### 7. "Publish" and Cucumber Reports

By default, newer Cucumber versions can print a banner suggesting you **publish your report** online:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ View your Cucumber Report at:                                            │
│ https://reports.cucumber.io/reports/...                                   │
│ This report will self-destruct in 24h.                                    │
```

This happens when publishing is **enabled** (`cucumber.publish.enabled=true`, or the token `CUCUMBER_PUBLISH_TOKEN` is set), and the report is uploaded to a **third-party service**: do **not** enable it for confidential projects. To silence the message and avoid publishing set:

```properties
cucumber.publish.quiet=true
```

(and do not set `cucumber.publish.enabled`). The built-in HTML file stays entirely **local**.

**Why a beginner should care:** the banner is easy to mistake for a normal message and the link looks convenient, but the report may contain screenshots of your application and test data. For a public demo site such as saucedemo.com there is no secret, yet the habit of keeping reports local transfers to client projects where it matters. Put `cucumber.publish.quiet=true` in `cucumber.properties` once, and the banner is gone for everyone on the team.

### 8. JUnit XML and CI

Two sources of XML are available:

1. **Surefire's own XML** in `target/surefire-reports/` (written automatically by Maven); it contains each Cucumber scenario as a JUnit test case, with names controlled by `cucumber.junit-platform.naming-strategy`.
2. The **`junit` Cucumber plug-in** (`junit:target/cucumber-reports/cucumber.xml`), one XML per run in the standard JUnit XML schema.

A simplified example of the XML shape:

```xml
<testsuite name="Cucumber" tests="2" failures="1" skipped="0" time="12.4">
  <testcase classname="Login" name="Valid login" time="5.1"/>
  <testcase classname="Login" name="Locked-out customer cannot log in" time="7.3">
    <failure message="expected: &lt;...&gt; but was: &lt;...&gt;" type="AssertionFailedError">stack trace...</failure>
  </testcase>
</testsuite>
```

Reading: each `testcase` is a scenario; a `failure` child marks it as failed; the attributes on `testsuite` hold the totals. CI servers (Jenkins "Publish JUnit test result report", GitHub Actions test reporters, GitLab, Azure DevOps) read these to show **pass/fail counts, trends, and failing test names** on the build page. Use the **HTML/JSON** report as the detailed attachment.

Which XML should you publish? Surefire's XML is already there and needs no configuration; add the Cucumber `junit` plug-in only when a tool specifically expects one file in a given place. Do not publish both to the same dashboard, or tests are counted twice.

### 9. From `mvn clean test` to a Report: Step by Step

Combining this lesson with the *Maven Integration* and *JUnit Integration* lessons:

1. `mvn clean test -Psmoke` starts; Maven deletes `target/` and compiles.
2. Surefire launches the JUnit Platform with `RunCucumberTest`.
3. The Cucumber engine selects `@smoke` scenarios and starts running them. Plug-ins from `cucumber.plugin` are created **before** the first scenario and open their output files.
4. For each scenario: `@Before` hooks run (browser starts, `TestContext` stores the `Scenario`), steps run, `@After` hooks run (screenshot if failed, then browser quit). The plug-ins receive events for each step and result.
5. When the run ends, the plug-ins **finish writing**: the HTML file is completed, JSON is closed, `rerun.txt` is written.
6. Surefire writes its XML. Maven prints the summary and exits with 0 or non-zero.
7. *You* open `target/cucumber-reports/report.html`.

A tip: if the HTML file is missing or empty, the JVM probably crashed or was killed before the plug-ins could finish writing; check the console for a stack trace and for `OutOfMemoryError`.

### 10. Organizing Report Files

```
target/
 ├── cucumber-reports/
 │     ├── report.html            built-in HTML (single file)
 │     ├── cucumber.json          input for generators
 │     └── cucumber.xml           JUnit XML
 ├── cucumber-html-reports/       generated by maven-cucumber-reporting (optional)
 ├── surefire-reports/            Maven's XML/TXT test reports
 └── rerun.txt                    failed scenario locations
```

Practical points:

- `mvn clean` **deletes** all of this; copy or archive reports (CI artifacts) if you need history.
- Do not commit `target/` to Git.
- Use a **timestamp or build number** in the report folder name when you need to keep several runs side by side.
- Never let **passwords, tokens, or personal data** appear in logs or attachments.

### 11. Making Reports Better

1. **Meaningful scenario titles** (including outline placeholders) make the report self-explanatory.
2. **Tags** let you filter and group results by suite or module.
3. **Screenshots on failure** plus the browser/environment as a `scenario.log` give instant context.
4. **Stable names**: do not rename features casually if you track history.
5. **Remove noise**: avoid printing huge debug text.
6. **Review failures daily**; classify and fix flaky tests so the report stays trusted.
7. **Keep the suite green**: a report that is always red gets ignored.

**Before and after example.** A weak outline title: `Scenario Outline: Login test` with rows reported as `Login test` repeated five times. A strong one: `Scenario Outline: Login attempt as <username>` which the report shows as `Login attempt as locked_out_user`, `Login attempt as problem_user`, and so on. The reader of the report knows immediately **which row** failed without opening anything.

### 12. Troubleshooting Reporting

| Symptom | Likely cause | Fix |
|---|---|---|
| No `report.html` | The `html` plug-in is not in `cucumber.plugin`, or the path is wrong, or the run crashed | Check the plug-in string for typos (`html:` needs the colon) and read the console |
| Report is empty or shows 0 scenarios | The tag filter selected nothing | Check tags; run with `summary` to see counts |
| Screenshot missing in the report | `@After` hook ordering, `isFailed()` false, driver already quit, or exception swallowed | Give the screenshot hook a higher `order` than the quit hook; log the exception |
| Report shows steps as `undefined` | Glue path or step text mismatch | See the *JUnit Integration* lesson |
| Banner "View your Cucumber Report at ..." | Publishing is suggested or enabled | Set `cucumber.publish.quiet=true` |
| `maven-cucumber-reporting` produces nothing after a failed run | Build stopped before `verify` | Use `testFailureIgnore` or an always-run CI step (Section 6) |
| `maven-cucumber-reporting`: "No JSON files found" | `inputDirectory` does not match where the `json` plug-in writes | Align the two paths |
| Duplicated scenarios in the report | Two runners both ran, or both Surefire and the plug-in XML were published | One runner per purpose; publish one XML source |
| Huge JSON/HTML file | Screenshot after every step | Attach on failure or milestones only |

---

## Complete Example: Configure, Run, and Read

**1. Runner configuration** (`RunCucumberTest`):

```java
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME,
        value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "not @wip and not @ignore")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value =
        "pretty, summary, "
      + "html:target/cucumber-reports/report.html, "
      + "json:target/cucumber-reports/cucumber.json, "
      + "junit:target/cucumber-reports/cucumber.xml, "
      + "rerun:target/rerun.txt")
@ConfigurationParameter(key = "cucumber.publish.quiet", value = "true")
public class RunCucumberTest { }
```

**2. Hook that attaches evidence** (from the *Hooks* lesson):

```java
@After(order = 10)
public void attachEvidence(Scenario scenario) {
    if (context.hasDriver()) {
        scenario.log("URL at end of scenario: " + context.driver().getCurrentUrl());
        if (scenario.isFailed()) {
            byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
            scenario.attach(png, "image/png", "Failure: " + scenario.getName());
        }
    }
}
```

**3. Make one scenario fail on purpose** (for example, change the expected error message in an example row), then run:

```
mvn clean test
```

**4. Open `target/cucumber-reports/report.html`** and check that you can:

- see the totals (for example, 7 scenarios: 6 passed, 1 failed);
- find the failed scenario and read the assertion message ("expected: <...> but was: <...>");
- see the **screenshot** attached to the failed scenario;
- filter by a tag such as `@negative`.

**5. Optional: generate the enhanced report**

```
mvn clean verify -Dmaven.test.failure.ignore=true
```

(`maven.test.failure.ignore` is the command-line property behind Surefire's `testFailureIgnore`.) Then open `target/cucumber-html-reports/overview-features.html`.

**6. Restore the expected message** and rerun to confirm the report turns green.

---

## Guided Lab: A Complete Report for Project 2

**Goal:** Produce, read, and share a report for your saucedemo.com BDD suite, including one deliberate failure with a screenshot, and document the command.

**Prerequisites:** the Project 2 BDD framework with runner, hooks, `TestContext`, and at least 6 scenarios with tags (`@smoke`, `@regression`, `@negative`).

1. **Configure plug-ins.** In `src/test/resources/cucumber.properties` write:

   ```properties
   cucumber.plugin=pretty, summary, html:target/cucumber-reports/report.html, json:target/cucumber-reports/cucumber.json, junit:target/cucumber-reports/cucumber.xml, rerun:target/rerun.txt
   cucumber.publish.quiet=true
   ```

   Remove any plug-in annotation from the runner so there is a single source of truth.
2. **Store the scenario.** Add a `scenario` field with getter and setter to `TestContext`. Add an `@Before(order = 0)` hook that calls `context.setScenario(scenario)`.
3. **Add the failure hook.** Create the `@After(order = 10)` screenshot hook from Section 4 (with `try/catch`). Confirm the browser-quit hook has a **lower** order.
4. **Green run.** `mvn clean test`. **Expected:** `summary` prints something like `7 Scenarios (7 passed)`; `report.html` exists; `rerun.txt` exists and is empty.
5. **Read the report.** Open `report.html`. Note the total, the duration, and the tags you can find.
6. **Break one scenario.** Change the expected message of one login Examples row to a wrong text. Run `mvn clean test`.
7. **Expected output:** `BUILD FAILURE`, `Tests run: 7, Failures: 1`, and in the console a `Failed scenarios:` block. `rerun.txt` now has one line with `login.feature:` and a line number.
8. **Investigate as a tester.** In `report.html`: find the failed step, read `expected: <...> but was: <...>`, view the screenshot. Write a classification (product, test, or environment) and a one-line reason.
9. **Add a step-level attachment.** In the checkout confirmation step, attach a screenshot via `context.scenario().attach(...)`. Rerun and find it in the report.
10. **Undefined step.** Add a step without a definition to a scenario. Run. **Expected:** the step is reported **undefined**, snippets are printed, and the build **fails** (Cucumber 7 default). Remove the step.
11. **Enhanced report (optional).** Add `maven-cucumber-reporting` as in Section 6 (check the version). Run `mvn clean verify -Dmaven.test.failure.ignore=true` and open `overview-features.html`. Find the tag statistics page.
12. **Restore** the correct message; rerun; confirm green.
13. **Document.** Add to the README: the command, where the report is, how to open it, and a screenshot of the failing report.

**Deliverable:** the README section plus the HTML report (or screenshot) from step 7 showing the failure and its attached screenshot. This is the Project 2 "BDD layer with tags and a report" evidence.

---

## Practice Exercises

1. **Console formats.** Run the suite once with `progress` and once with `pretty, summary`. When would you prefer each?
2. **HTML report.** Generate the HTML report and answer: how many scenarios ran, how long did the slowest scenario take, and which tags exist?
3. **Failure evidence.** Make a scenario fail. Find in the report: the failed step, the exception message, and the screenshot. Write two sentences classifying the failure (product defect, test defect, or environment).
4. **Attachments.** Use `scenario.log` and `scenario.attach` to add the browser name and the final URL to each scenario's report.
5. **JSON.** Open `cucumber.json` in an editor. Find a step's `result.status` and `duration`. Where did the screenshot go?
6. **Enhanced report.** Add `maven-cucumber-reporting` and generate the multi-page report. Which pages show tag statistics?
7. **Undefined vs. failed.** Add a scenario with a new, undefined step. How is it displayed, and does the build fail? Explain why that is desirable.
8. **Usage plug-in.** Add `usage:target/usage.json` and find a step definition that is never used. Should it be deleted?
9. **Publish.** Explain why `cucumber.publish.quiet=true` matters for a confidential project.
10. **Project 2 milestone.** Deliver a BDD layer with tags and a report: include the HTML report (or a screenshot of it) showing at least one failure screenshot, and document the command that produces it.
11. **Hook order.** Set the quit hook to a higher `order` than the screenshot hook and observe the result. Explain what you see and fix it.
12. **Scenario in steps.** Explain in your own words why a step definition cannot simply take a `Scenario` parameter, and show the `TestContext` approach.

---

## Solutions and Hints

1. **Console formats.** `pretty, summary` while developing or debugging (you see steps and the matching Java methods). `progress` (or only `summary`) for long suites where per-step output is noise; rely on the HTML report for details.
2. **HTML report.** Totals are at the top; durations are shown per scenario and step; tags are visible beside scenarios and searchable. Hint: use the status filter and the search box.
3. **Failure evidence.** Sample answer: "The `Then` step failed with `expected: <Epic sadface: ...> but was: <...>`. The screenshot shows the correct error banner with different wording, so the test expectation is outdated: a **test defect**." Always cite the screenshot as evidence.
4. **Attachments.** In an `@After` hook: `scenario.log("Browser: " + System.getProperty("browser", "chrome"))` and `scenario.log("URL: " + context.driver().getCurrentUrl())`, guarded by `context.hasDriver()`.
5. **JSON.** `result.status` is `passed`/`failed`/...; `duration` is in nanoseconds. The screenshot is inside the step's `embeddings` entry as Base64 `data` with `mime_type` `image/png`.
6. **Enhanced report.** The overview and the tag statistics pages (look for "Tags" in the site's navigation). It must be generated with `mvn clean verify` (JSON must exist and the build must reach `verify`).
7. **Undefined vs. failed.** The step is shown as undefined and snippets are printed; in Cucumber 7 the build fails by default. Desirable because a scenario that silently verifies nothing gives false confidence.
8. **Usage plug-in.** The JSON lists each definition with usage counts; an unused definition has none. Before deleting, check that no feature file in another branch or tag-filtered run uses it; unused code is a maintenance cost, so removing it is normally right.
9. **Publish.** Publishing uploads the report (with screenshots and test data) to a third-party service; for confidential applications this is a data leak. The quiet setting prevents the prompt and the upload.
10. **Project 2 milestone.** Checklist: tags on scenarios (`@smoke`, `@regression`, `@negative`); a runner and `cucumber.properties`; failure screenshot visible in `report.html`; README with `mvn clean test -Psmoke` and the report path.
11. **Hook order.** With the quit hook running first, `context.hasDriver()` is false (or the driver is dead), so no screenshot is attached. Fix: for `@After`, higher order values run **first**, so give the screenshot hook the higher value.
12. **Scenario in steps.** Cucumber supplies `Scenario` only to hook methods. The workaround: store it in `TestContext` in a `@Before` hook, then read `context.scenario()` in steps. Because PicoContainer creates one `TestContext` per scenario, it is safe in parallel runs.

---

## Self-Check Questions

1. **What does a Cucumber plug-in do?** It listens to events during the run and writes them in a format: console output (`pretty`, `summary`) or a file (`html`, `json`, `junit`, `rerun`).
2. **How do you get a screenshot into the report?** Take it with Selenium's `TakesScreenshot` as bytes and call `scenario.attach(bytes, "image/png", "name")` from an `@After` hook when `scenario.isFailed()`.
3. **How can a step definition attach evidence if it cannot receive `Scenario`?** Store the `Scenario` in `TestContext` from a `@Before` hook and use it from the step.
4. **What happens to a scenario with an undefined or pending step in Cucumber 7?** It is treated as an error by default, so the run fails instead of passing silently.
5. **Why might `maven-cucumber-reporting` produce no report after a failed test run?** With the default Surefire behavior the build stops at `test` and never reaches `verify`; use `testFailureIgnore` (and another step to fail the pipeline) or an always-run CI step.
6. **How do you avoid publishing your report to the Cucumber Reports service?** Set `cucumber.publish.quiet=true` and do not enable `cucumber.publish.enabled`.
7. **Which exception types suggest a test defect rather than a product defect?** `NoSuchElementException`, `TimeoutException`, and `StaleElementReferenceException` usually point to locator or synchronization issues; confirm with the screenshot.
8. **Which report file would you email to a manager, and which would you feed to a generator?** The single self-contained `report.html` for the manager; `cucumber.json` for generators.

---

## Summary

- **Reports** turn test runs into information for developers, testers, managers, and the business; Cucumber's readable scenarios make them a form of **living documentation**.
- Output is produced by **plug-ins** configured with `cucumber.plugin`: `pretty`, `summary`, `progress` (console); `html`, `json`, `junit`, `message` (files); `rerun` and `usage` (maintenance).
- The built-in **HTML report** is a single, shareable file with scenario/step details, tags, failure messages, and **attachments**.
- **Attach screenshots and logs** from hooks using `scenario.attach(...)` and `scenario.log(...)`; `Scenario` is passed **only to hooks**, so store it in `TestContext` if steps need it; capture on failure, protect against capture errors, avoid sensitive data.
- The **JSON** output feeds generators such as **maven-cucumber-reporting**, which needs `testFailureIgnore` or an always-run CI step to produce a report after failures; **Allure** and **ExtentReports** are common alternatives. **JUnit XML** lets CI servers display results.
- **Publish** uploads to a third-party service: use `cucumber.publish.quiet=true` and keep confidential data local.
- In Cucumber 7, **undefined and pending** steps are **errors** by default; read results by **status** (passed, failed, skipped, undefined, pending, ambiguous), start from the **first failed step**, and classify failures as product, test, or environment issues.
- The plug-in versions and library versions in this lesson are **examples**: check current releases.

---

## Additional Resources

- Cucumber documentation, *Reporting*: https://cucumber.io/docs/cucumber/reporting/
- Cucumber-JVM, *cucumber-junit-platform-engine README: plugin configuration*: https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-junit-platform-engine
- maven-cucumber-reporting project (Masterthought): https://github.com/damianszczepanik/maven-cucumber-reporting
