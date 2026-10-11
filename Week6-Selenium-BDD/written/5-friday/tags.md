# Tags

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **tags** are and the problems they solve (organizing, selecting, and customizing the behavior of scenarios).
- Place tags on `Feature`, `Scenario`, `Scenario Outline`, `Examples`, and `Rule`, and explain **tag inheritance** with worked counts.
- Write **tag expressions** with `and`, `or`, `not`, and parentheses, and evaluate them by hand.
- Run subsets of scenarios from the **runner**, the **command line** with Maven, and a **properties file**, and know which setting wins.
- Combine tags with **hooks** (`@Before("@ui")`) to run setup only for selected scenarios.
- Apply a sensible **tagging strategy** for Project 2: `@smoke`, `@regression`, `@negative`, `@wip`, `@ignore`, and so on.
- Use tags to **skip** unfinished or broken scenarios without deleting them.
- Diagnose problems from console output (zero scenarios run, shell quoting errors, unexpected selections).
- Avoid common mistakes (typos, too many tags, tags that encode implementation details).

---

## Why This Matters

### The problem: you cannot run everything every time

A real suite grows quickly: 20 scenarios this week, 200 next month, 2,000 next year. You cannot run everything every time:

- A developer who just changed the login page wants to run **only login tests**, in seconds.
- The pipeline that runs after **every commit** should run a fast **smoke** subset (5 minutes).
- The **nightly** build runs the full **regression** pack (2 hours).
- A scenario for a feature that is still under construction must not break the build: mark it **work in progress**.
- Some scenarios need a special setup (an API user, a mobile viewport): only those should pay the cost.

### The idea: luggage labels and playlist labels

**Tags** are the single mechanism for all of this. They are plain labels attached to features and scenarios, and the test runner uses them to **filter**; hooks use them to **customize**.

Think of the colored labels on airport luggage: "priority", "fragile", "heavy". The label does not change the suitcase; it tells the handling system what to do with it, and staff can say "send all fragile bags to belt 3". Or think of tagging songs in a music app (`#workout`, `#chill`): you build a playlist by asking for songs with a certain tag, or "workout but not slow". Test tags work exactly this way, and a **tag expression** is the playlist query.

### Where it fits in your project

Your Project 2 BDD layer requirement today ("complete the BDD layer with tags and a report") depends on this lesson. By the end of the day your saucedemo.com features should carry a documented set of tags, you should be able to run a smoke subset, a module subset, and "everything except work in progress" from the command line, and your report (the *Cucumber Reporting* lesson) will show those tags next to the scenarios. The same tags are used again in the *Maven Integration* lesson to build profiles, and in the *JUnit Integration* lesson to configure runners.

### What you already know that this builds on

| Earlier topic | How it is used here |
|---|---|
| Features, Scenarios, Examples | These are the elements that receive tags |
| Runner class and `cucumber.properties` (Thursday) | Where the tag filter is configured |
| Hooks (previous lesson) | Tagged hooks add behavior only where needed |
| Maven `mvn test` | The command line that carries `-Dcucumber.filter.tags` |

---

## The Concept

### 1. What Is a Tag?

**Definition.** A **tag** is a word starting with `@`, written on the line(s) **before** a Gherkin keyword:

```gherkin
@login @smoke
Feature: Login

  @positive
  Scenario: Successful login
    ...

  @negative @regression
  Scenario: Wrong password is rejected
    ...
```

**Line-by-line explanation**

| Line | Meaning |
|---|---|
| `@login @smoke` | Two tags on the Feature: every scenario below belongs to the login area and is part of the smoke suite (by inheritance) |
| `Feature: Login` | The tagged element |
| `@positive` | One tag on the next scenario, describing the type of check |
| `@negative @regression` | Two tags on the scenario below them; this scenario will also inherit `@login` and `@smoke` |

Rules of syntax:

- A tag starts with `@` and contains **no spaces** (`@smoke`, `@sprint-12`, `@JIRA-1234`).
- Several tags can be on one line (separated by spaces) or on several lines.
- Tags go **immediately above** the element they tag.
- Tag names are **case-sensitive**: `@Smoke` and `@smoke` are different.
- Tags have **no built-in meaning** (apart from conventions you or your tools define); they are just labels you choose.

### 2. Where Tags Can Be Placed

| Placed above | Applies to |
|---|---|
| `Feature:` | The feature and **all** its scenarios, outlines, and examples |
| `Rule:` | All scenarios in the rule |
| `Scenario:` / `Scenario Outline:` | That scenario (or outline with all of its example rows) |
| `Examples:` | Only the rows of that `Examples` block |

```gherkin
@shopping
Feature: Shopping cart

  @smoke
  Scenario: Adding a product
    ...

  @regression
  Scenario Outline: Adding different products
    ...
    @fast
    Examples: Small catalog
      | product |
      | ...     |

    @slow
    Examples: Large catalog
      | product |
      | ...     |
```

A Background cannot be tagged (it is not a scenario of its own), and neither can individual steps.

### 3. Tag Inheritance

Tags are **inherited** downward: a scenario carries its own tags **plus** those of its rule and feature. In the example above, "Adding a product" has the tags `@shopping` and `@smoke`; the rows of the `@fast` Examples block have `@shopping`, `@regression`, and `@fast`.

Consequence: put **broad** tags (module, type of test) on the **Feature**, and **specific** tags on scenarios. In a hook, `scenario.getSourceTagNames()` returns the combined set.

**Inheritance with a Rule.**

```gherkin
@cart
Feature: Shopping cart

  @pricing
  Rule: Totals are calculated correctly

    @smoke
    Example: Total of one product
      ...

    Example: Total of two products
      ...
```

| Scenario | Effective tags |
|---|---|
| Total of one product | `@cart`, `@pricing`, `@smoke` |
| Total of two products | `@cart`, `@pricing` |

Inheritance only flows **downward**. A tag on a single scenario never "bubbles up" to the Feature, so running `-Dcucumber.filter.tags="@smoke"` selects that one scenario, not its neighbors.

### 4. Tag Expressions

**Definition.** A **tag expression** is a small Boolean language used to **select** scenarios:

| Expression | Meaning |
|---|---|
| `@smoke` | Scenarios tagged `@smoke` |
| `not @wip` | Scenarios **without** `@wip` |
| `@smoke and @login` | Scenarios with **both** tags |
| `@smoke or @regression` | Scenarios with **either** tag |
| `@smoke and not @slow` | Smoke scenarios that are not slow |
| `(@smoke or @sanity) and not @wip` | Parentheses group |
| `@login and (@positive or @negative)` | Mixed grouping |

Notes:

- Operators are lowercase **`and`**, **`or`**, **`not`**; precedence is `not` > `and` > `or`, so use **parentheses** for clarity.
- A scenario with **no tags** is selected only by expressions it satisfies (for example `not @wip` selects it).
- Expressions are evaluated against the scenario's **complete** (inherited) tag set.
- In shells, **quote** the expression: `-Dcucumber.filter.tags="@smoke and not @slow"`.

#### Evaluating an expression by hand

Take four scenarios with these *effective* tags:

| # | Scenario | Effective tags |
|---|---|---|
| 1 | Successful login | `@ui @login @smoke @positive` |
| 2 | Wrong password | `@ui @login @regression @negative` |
| 3 | Locked-out user | `@ui @login @regression @negative` |
| 4 | Remember me | `@ui @login @wip` |

Evaluate `@login and not @wip`:

1. For each scenario ask "has `@login`?" Yes for all four.
2. Ask "does it have `@wip`?" Only scenario 4.
3. `not @wip` is true for 1, 2, 3. Combined with `and @login`: scenarios 1, 2, and 3 run.

Evaluate `@smoke or @negative and not @wip`. Because `and` binds tighter than `or`, this is `@smoke or (@negative and not @wip)`. Scenario 1 matches `@smoke`; scenarios 2 and 3 match the right side; scenario 4 matches neither. Result: 1, 2, 3. If you had meant `(@smoke or @negative) and not @wip`, the answer would be the same here, but the two expressions differ on other data, so **write the parentheses** to say what you mean.

### 5. Running a Subset of Scenarios

The configuration key is **`cucumber.filter.tags`**. You can set it in three places (the same options you saw in *Cucumber Framework Setup*).

**a) In the runner class**

```java
import static io.cucumber.junit.platform.engine.Constants.FILTER_TAGS_PROPERTY_NAME;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.revature.qea.steps,com.revature.qea.support")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "@smoke and not @wip")
public class RunSmokeTest { }
```

**Line-by-line explanation**

| Line | Meaning |
|---|---|
| `import static ...FILTER_TAGS_PROPERTY_NAME` | A constant holding the text `cucumber.filter.tags`, so you avoid typing mistakes |
| `@Suite` | Marks the class as a JUnit Platform suite |
| `@IncludeEngines("cucumber")` | Tells the suite to use the Cucumber engine to find tests |
| `@SelectClasspathResource("features")` | Looks for `.feature` files in the `features` folder on the classpath (`src/test/resources/features`) |
| `@ConfigurationParameter(key = GLUE_...)` | The packages with step definitions **and hooks** |
| `@ConfigurationParameter(key = FILTER_TAGS_..., value = "@smoke and not @wip")` | The tag expression: smoke scenarios that are not work in progress |
| `public class RunSmokeTest { }` | The class body is empty; the annotations do the work. The name ends with `Test` so Maven Surefire picks it up |

You can keep several runner classes (`RunSmokeTest`, `RunRegressionTest`), each with a different expression. Maven's Surefire will run any class matching its naming pattern.

**b) In `cucumber.properties`**

```properties
cucumber.filter.tags=not @wip and not @ignore
```

**c) On the command line** (best for CI because no code change is needed)

```
mvn clean test -Dcucumber.filter.tags="@smoke"
mvn clean test -Dcucumber.filter.tags="@regression and not @slow"
```

On **Windows PowerShell** the quoting often needs the whole argument in quotes: `mvn clean test "-Dcucumber.filter.tags=@smoke and not @slow"`.

**Which setting wins?** The command-line value takes precedence over the properties file, so a build server can choose the subset while your repository default (`not @wip`) protects everyone else. Be careful with the runner class: an expression written into `@ConfigurationParameter` on a suite class is part of that suite's own configuration and is generally **not** overridden by `-Dcucumber.filter.tags`. A practical rule: use **either** hard-coded runner expressions (one runner per suite) **or** command-line/properties selection (one runner, many commands), not both for the same runner, and test the combination once so you know what your project does. The *Maven Integration* lesson shows profiles that wrap these commands.

**JUnit platform tags:** The Cucumber engine also exposes Cucumber tags to JUnit as tags *without* the `@`, so JUnit's `@IncludeTags("smoke")` / `@ExcludeTags("wip")` on a suite class also work. Using `cucumber.filter.tags` is the Cucumber-native, better-documented way, and we use it in this course.

### 6. Tags and Hooks

A hook can restrict itself to scenarios matching an expression:

```java
@Before("@ui")                       // only for scenarios tagged @ui
public void startBrowser() { ... }

@Before("@api and not @ui")
public void prepareApiClient() { ... }

@After("@createsUser")
public void deleteCreatedUser() { ... }
```

This lets one framework support **different kinds of scenarios**: UI scenarios start a browser; API scenarios do not. In `Hooks` from the previous lesson you could replace the unconditional `@Before` with `@Before("@ui")` and tag features `@ui`, saving a browser launch for non-UI scenarios.

Within a hook, you can also *inspect* tags in code:

```java
@Before
public void setUp(Scenario scenario) {
    if (scenario.getSourceTagNames().contains("@mobile")) {
        // start a mobile-emulation browser
    }
}
```

**Trace: which hooks run for which scenario?** Suppose these hooks exist:

```java
@Before(value = "@ui", order = 0)      public void startBrowser() { }
@Before(value = "@slow", order = 5)    public void warnSlow() { }
@After(value = "@createsUser")         public void deleteUser() { }
```

| Scenario tags | Hooks that run, in order |
|---|---|
| `@ui @smoke` | `startBrowser` |
| `@ui @slow` | `startBrowser`, `warnSlow` |
| `@ui @createsUser` | `startBrowser`, ..., `deleteUser` (after) |
| `@api` | none of them |

The tag decides **whether** a hook runs; `order` still decides **when**, among the hooks that do run.

### 7. Typical Tagging Strategy

Tags fall into a few **categories**. Define your team's vocabulary and **document it** (a table in the README):

| Category | Examples | Purpose |
|---|---|---|
| **Test level / suite** | `@smoke`, `@sanity`, `@regression` | Choose how much to run |
| **Feature / module** | `@login`, `@cart`, `@checkout` | Run a feature area |
| **Type of check** | `@positive`, `@negative`, `@boundary` | Select by purpose |
| **Status** | `@wip` (work in progress), `@ignore`/`@skip`, `@flaky`, `@bug-1234` (known defect) | Keep unfinished/broken scenarios out of the main run |
| **Environment / capability** | `@ui`, `@api`, `@mobile`, `@chrome-only` | Drive hooks and routing |
| **Traceability** | `@JIRA-123`, `@REQ-45`, `@story-7` | Link scenarios to tickets/requirements |
| **Speed** | `@fast`, `@slow` | Run quick checks often |

**What each suite usually contains:**

- **`@smoke`**: a handful of the *most critical* paths (can the user log in, add to cart, check out?). Runs on **every commit**, must be fast and stable.
- **`@sanity`**: a slightly wider quick check after a deployment.
- **`@regression`**: the full pack, run nightly or before release.

**A concrete scheme for Project 2 (saucedemo.com):**

| Feature file | Feature-level tags | Example scenario-level tags |
|---|---|---|
| `login.feature` | `@ui @login` | `@smoke @positive`, `@regression @negative` |
| `login-validation.feature` | `@ui @login @negative` | `@regression` |
| `inventory-sorting.feature` | `@ui @inventory` | `@regression` on the outline |
| `shopping-cart.feature` | `@ui @cart` | `@smoke` on "Adding one product" |
| `checkout.feature` | `@ui @checkout` | `@smoke @positive` on the happy path |

With this scheme `@smoke` is a handful of scenarios (login, add to cart, complete checkout), `@cart` selects one module, and `not @wip` selects everything that is ready.

### 8. Skipping and Excluding Scenarios

To **exclude** a scenario from a normal run without deleting it, tag it and filter it out:

```gherkin
@wip
Scenario: Gift-wrap option (feature under construction)
  ...

@ignore @bug-4711
Scenario: Price rounding is correct   # fails because of known defect 4711
  ...
```

and set a default expression in `cucumber.properties`:

```properties
cucumber.filter.tags=not @wip and not @ignore
```

Good practice: always attach the **reason** to a skip (`@bug-4711`), and review skipped scenarios regularly, because ignored tests tend to be forgotten. A `@wip` scenario can still be run on purpose: `-Dcucumber.filter.tags="@wip"`.

Why not just delete or comment out? A deleted scenario loses the knowledge that the behavior was ever specified; a commented-out one is invisible to every report. A tagged scenario stays in the repository, in the living documentation, and can be counted: "12 scenarios are ignored" is a number a team can act on.

Note the difference between *excluded* and *skipped*: excluded scenarios are filtered out before the run and do not appear in the results at all, which is what `cucumber.filter.tags` does.

### 9. Tags in Reports

Tags appear in Cucumber's reports (the *Cucumber Reporting* lesson): scenarios are listed with their tags, and reports can be grouped or filtered by tag, giving management a **per-suite or per-module view** of results. Third-party reporters often include a "Tags" overview page. This is a second reason to keep tags consistent: the report is only as useful as the vocabulary.

### 10. Best Practices

1. **Keep a small, documented vocabulary.** Ten well-understood tags beat fifty ad-hoc ones.
2. **Use lowercase with hyphens** (`@smoke`, `@sprint-12`), consistently.
3. **Tag at the highest sensible level** (Feature) and refine on scenarios.
4. **Do not tag everything** `@smoke`; a smoke suite that takes an hour is not a smoke suite.
5. **Tags describe *what/why*, not *how*:** `@negative`, not `@clicks-button`.
6. **Do not encode secrets or environment URLs** in tags.
7. **Prefer expressions over many combined tags** (`@smoke and @login` rather than a new tag `@smoke-login`).
8. **Treat tags like code:** review them in pull requests, remove obsolete ones.
9. **Beware of typos:** a mistyped tag silently selects nothing. Cucumber does not validate tag names, so if a run executes **0 scenarios**, check the expression first.
10. **Use tags for control, not for logic inside steps.** If a step behaves differently based on a tag, consider two steps or two scenarios.

**Good-versus-bad rewrites**

| Bad | Why | Good |
|---|---|---|
| `@smoke-login-positive-chrome` | One tag encoding four ideas; impossible to combine | `@smoke @login @positive` |
| `@test @important @check` | Meaningless words | `@regression` / `@smoke` |
| `@click-login-button` | Describes *how* | `@positive` |
| `@Smoke` in one file, `@smoke` in another | Case-sensitive; the run misses half | Always lowercase |
| `@bug` without a number | Nobody knows which defect | `@bug-4711` |

### 11. Troubleshooting with Console Output

**Case A: Zero scenarios run.**

You typed `-Dcucumber.filter.tags="@smoek"`. Cucumber does not complain about unknown tags; it finds no scenario that matches, and the run typically reports:

```
0 Scenarios
0 Steps
[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0
```

and the build may still end with `BUILD SUCCESS`, which is dangerous in a pipeline: a green build that tested nothing. Diagnosis: search the features folder for the tag (`grep -r "@smoek" src/test/resources`). Prevention: let the pipeline fail if fewer than an expected number of scenarios ran, or look at the scenario count in the log.

**Case B: Shell strips or splits the expression.**

Without quotes, `mvn test -Dcucumber.filter.tags=@smoke and not @slow` hands Maven three separate arguments (`and`, `not`, `@slow`), which Maven tries to interpret as lifecycle phases:

```
[ERROR] Unknown lifecycle phase "and". You must specify a valid lifecycle phase ...
```

Fix: wrap the whole `-D...` value in quotes.

**Case C: Expression syntax error.**

`@smoke and not@wip` or `@smoke @login` (two tags with no operator) produces an error that the tag expression is invalid, naming the position. Fix: write `@smoke and @login` and put spaces around every operator.

**Case D: More scenarios than expected.**

You wrote `@smoke or @login and not @wip` expecting "smoke or login, but never wip". Because `and` binds tighter than `or`, a `@smoke @wip` scenario is selected. Fix: `(@smoke or @login) and not @wip`.

**Case E: Command line seems ignored.**

The runner class has its own `FILTER_TAGS_PROPERTY_NAME`. Diagnosis: count the scenarios; compare with what the runner expression alone selects; then remove the hard-coded value or use separate runners.

### 12. Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `@smoke, @login` (comma) | The comma becomes part of the tag name | Separate tags with **spaces** |
| `@smoke and not@wip` | Expression error | Space between `not` and the tag |
| Unquoted expression in the shell | The shell splits/interprets the text | Wrap in double quotes |
| Typos (`@smoek`) | **0 scenarios run** | Check spelling; grep the features folder for the tag |
| Tag placed above a **comment** or blank line separated from the keyword | Tag attaches to the next keyword, or is ignored | Put the tag directly above the keyword |
| Expecting a `Rule` or `Examples` tag to apply to the whole feature | Scenarios not selected | Tags only apply **downward** |
| Using `or` when you meant `and` | Too many scenarios selected | Re-read the expression, add parentheses |
| Same expression in runner **and** command line | Confusion about which wins | Keep one source of truth; command line overrides the properties file |

---

## Hands-On Lab: Tag the Project 2 Features and Run Subsets

Goal: tag the saucedemo.com features, run four different subsets, and verify the counts.

1. **Create the example feature.** Put the feature from "Complete Example" below in `src/test/resources/features/login.feature` (merge with your own scenarios if the file exists).
2. **Set the default exclusion.** In `src/test/resources/cucumber.properties` add `cucumber.filter.tags=not @wip and not @ignore`.
3. **Run the default:** `mvn clean test`. Expected: `3 Scenarios` (the successful login and the two outline rows); the `@wip` scenario is not run.
4. **Run smoke:** `mvn test -Dcucumber.filter.tags="@smoke"`. Expected: `1 Scenarios (1 passed)`.
5. **Run negative:** `mvn test -Dcucumber.filter.tags="@negative"`. Expected: 2 scenarios (the two outline rows).
6. **Run the work in progress on purpose:** `mvn test -Dcucumber.filter.tags="@wip"`. Expected: 1 scenario. It will probably fail or be undefined because the steps are not written; that is normal for work in progress, and it shows why `@wip` must be excluded from the default run.
7. **Make a deliberate typo:** `mvn test -Dcucumber.filter.tags="@smoek"`. Note the `0 Scenarios` output, and write down how your pipeline would catch it.
8. **Add a tagged hook.** In `Hooks`, change `@Before(order = 0)` to `@Before(value = "@ui", order = 0)`. Confirm that the login scenarios still run correctly because the Feature carries `@ui`. Then remove `@ui` from the Feature, rerun, and see what changes (the steps still work through the lazy driver, but the hook no longer runs, so the log line from the hook disappears).
9. **Document the vocabulary.** Add a table of your tags (name, meaning, who adds it) to the project README.
10. Commit: `Tag features and add default tag filter`.

---

## Complete Example

`src/test/resources/features/login.feature`

```gherkin
@ui @login
Feature: Login
  As a registered customer
  I want to log in
  so that I can see the products

  @smoke @positive
  Scenario: Successful login with valid credentials
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "secret_sauce"
    Then the customer sees the products page

  @regression @negative
  Scenario Outline: Login with <description> is rejected
    Given the customer is on the login page
    When the customer logs in with username "<username>" and password "<password>"
    Then the error message "<message>" is displayed

    Examples:
      | description       | username        | password       | message                                                                   |
      | a wrong password  | standard_user   | wrong_password | Epic sadface: Username and password do not match any user in this service |
      | a locked-out user | locked_out_user | secret_sauce   | Epic sadface: Sorry, this user has been locked out.                       |

  @wip
  Scenario: Remember me keeps the user logged in
    Given the customer is on the login page
    When the customer logs in with "remember me" selected
    Then the customer is still logged in after restarting the browser
```

**Reading the tags.** The Feature carries `@ui @login`, which every scenario inherits. The first scenario adds `@smoke @positive`. The outline adds `@regression @negative`, and both of its rows inherit these. The last scenario is `@wip`.

Runs:

| Command | Scenarios executed |
|---|---|
| `mvn test -Dcucumber.filter.tags="@smoke"` | 1 (the successful login) |
| `mvn test -Dcucumber.filter.tags="@negative"` | 2 (both outline rows) |
| `mvn test -Dcucumber.filter.tags="@login and not @wip"` | 3 |
| `mvn test -Dcucumber.filter.tags="@wip"` | 1 (the unfinished one) |
| `mvn test -Dcucumber.filter.tags="not @wip"` | 3 |

Tagged hook (in `Hooks`):

```java
@Before(value = "@ui", order = 0)
public void startBrowser() {
    context.driver();
}
```

Because `@ui` is on the Feature, every scenario in it inherits the tag and gets a browser; a future `@api` feature would not start one.

---

## Practice Exercises

1. **Tag your features.** Add `@ui`, a module tag, and `@smoke`/`@regression` tags to your existing features. Document your vocabulary in a README table.
2. **Predict and verify.** For the complete example above, predict the number of scenarios for: `@positive or @negative`, `@login and not @smoke`, and `(@smoke or @negative) and not @wip`. Verify with runs.
3. **Inheritance.** Add a tag only to the `Examples` block of an outline. Run with that tag and count the scenarios. Then move the tag to the outline and compare.
4. **Smoke runner.** Create `RunSmokeTest` and `RunRegressionTest` runner classes with different tag expressions. What happens when you run `mvn test` with no filters? (Hint: all runner classes execute.)
5. **Default exclusions.** Put `not @wip and not @ignore` into `cucumber.properties`, then override it from the command line to run only `@wip`. Which wins?
6. **Tagged hook.** Create `@Before("@slow")` that prints a warning, and `@After("@createsData")` that prints a cleanup message. Tag scenarios accordingly and verify which hooks ran.
7. **Typo detective.** Run with `-Dcucumber.filter.tags="@smoek"`. What does the output say, and how would you notice this mistake in a CI pipeline?
8. **Evaluate by hand.** Given a scenario with effective tags `@ui @cart @regression @slow`, state whether each expression selects it: (a) `@cart and not @slow`, (b) `@smoke or @regression`, (c) `not (@slow or @wip)`, (d) `@ui and (@cart or @checkout)`.
9. **Write the expression.** Write the tag expression for: "all checkout scenarios that are negative tests, except known bugs".
10. **Fix the tags.** Correct these tag lines: `@Smoke, @login`, `@smoke and @login` (written above a Scenario), `@bug` (meant to link a defect).
11. **Wrap it in a script.** Write three Maven commands (smoke, one module, everything except `@wip`) that a teammate could paste into the README of your project.
12. **Project 2 milestone.** Define a tagging scheme for Project 2 (suite, module, type, status), apply it to all scenarios, and show three different filtered runs (smoke, one module, everything except `@wip`).

---

## Solutions and Hints

**1.** Tag the Feature with `@ui` and the module (`@login`, `@cart`, ...). Put `@smoke` only on the few most critical scenarios. Everything else is `@regression`.

**2.** `@positive or @negative`: 3 (one positive, two outline rows). `@login and not @smoke`: 3 (two outline rows plus the `@wip` scenario, all inherit `@login`). `(@smoke or @negative) and not @wip`: 3.

**3.** A tag on one `Examples` block selects only that block's rows; the same tag on the outline selects all rows of all blocks.

**4.** `mvn test` runs every class matching Surefire's naming pattern, so both runners execute and many scenarios run twice. Common remedies: keep only one default runner, or run a specific one with `mvn test -Dtest=RunSmokeTest`.

**5.** The command-line value wins over the properties file. Run `mvn test -Dcucumber.filter.tags="@wip"`.

**6.** The `@Before("@slow")` message appears only for scenarios with `@slow` (inherited or direct); the `@After("@createsData")` message only for `@createsData` scenarios.

**7.** The output shows `0 Scenarios` and the build may be green. In CI, assert a minimum number of executed scenarios, or compare the number with the previous run.

**8.** (a) No: it has `@slow`. (b) Yes: it has `@regression`. (c) No: it has `@slow`. (d) Yes: `@ui` and `@cart`.

**9.** `@checkout and @negative and not @bug-1234` (or, if several bug tags exist, a list of `not` terms; a team convention such as an extra `@known-bug` tag makes this shorter: `@checkout and @negative and not @known-bug`).

**10.** `@smoke @login` (no comma, lowercase). `@smoke and @login` is an expression, not a tag line; above a Scenario write `@smoke @login`. `@bug-4711` (include the ticket number).

**11.**

```
mvn clean test -Dcucumber.filter.tags="@smoke"
mvn clean test -Dcucumber.filter.tags="@cart"
mvn clean test -Dcucumber.filter.tags="not @wip"
```

**12.** Hint: use the table in Section 7 as the starting point and keep the vocabulary to about ten tags.

---

## Self-Check Questions

**Q1. Where can a tag be placed?**
Above `Feature`, `Rule`, `Scenario`, `Scenario Outline`, and `Examples`.

**Q2. A Feature is tagged `@ui` and a scenario `@smoke`. Which tags does the scenario have?**
Both `@ui` and `@smoke` (inheritance flows downward).

**Q3. What does `@smoke and not @slow` select?**
Scenarios that carry `@smoke` and do not carry `@slow`.

**Q4. Which wins: `cucumber.properties` or `-Dcucumber.filter.tags`?**
The command line.

**Q5. A run reports 0 scenarios and a green build. What is the first thing to check?**
The spelling of the tag and the expression (and the quoting in the shell).

**Q6. Why attach a bug number to an ignored scenario?**
So the reason is recorded and the scenario can be found and re-enabled when the defect is fixed.

**Q7. What does `@Before("@ui")` do?**
Runs the hook only for scenarios whose effective tags include `@ui`.

**Q8. Why is `@smoke-login-chrome` a poor tag?**
It packs several ideas into one name; separate tags can be combined with expressions.

---

## Summary

- **Tags** (`@name`) are labels placed above `Feature`, `Rule`, `Scenario`, `Scenario Outline`, and `Examples`; they are **inherited downward**.
- **Tag expressions** (`and`, `or`, `not`, parentheses) select scenarios; set them with `cucumber.filter.tags` in the **runner**, `cucumber.properties`, or the **command line** (which overrides the file); **quote** expressions in the shell.
- Tags drive **selection** (smoke, regression, module runs, exclusion of `@wip`/`@ignore`) and **hook behavior** (`@Before("@ui")`).
- Use a **small, documented, consistent vocabulary** by category: suite, feature, type, status, environment, traceability, speed.
- A mistyped tag silently selects **nothing**; always sanity-check the number of scenarios run.
- Skipped scenarios should carry a **reason tag** and be reviewed regularly.

---

## Additional Resources

- Cucumber documentation, *Tags*: https://cucumber.io/docs/cucumber/api/#tags
- Cucumber documentation, *Tag expressions*: https://cucumber.io/docs/cucumber/api/#tag-expressions
- Cucumber-JVM, *cucumber-junit-platform-engine README (filter tags and configuration)*: https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-junit-platform-engine
