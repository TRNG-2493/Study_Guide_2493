# Lab 5 (Friday): Complete the Project 2 BDD Layer - Tags, Hooks, Profiles and a Report

**Week 6 · Day 5 · Advanced Cucumber · Mode A (Code Lab) · Individual (pairs optional)**
**Estimated time:** 3 hours
**Project lane:** Project 2 - Test Automation Framework (Milestone 5: BDD layer complete, runnable by tag, with a report)
**Deliverable:** the finished framework repository, `docs/TAGS_AND_RUNS.md`, `README_PROJECT.md`, and the report evidence

---

## The Scenario

Yesterday your pair produced a working BDD layer: three features, 14 scenarios, readable Gherkin on top of Page Objects. It works, but a team lead reviewing it this morning has a list of complaints:

- "Every scenario repeats the same login lines, and the five login scenarios differ only in data."
- "I can't run only the important checks after a commit; it is all or nothing."
- "The browser cleanup is a hack in `TestContext` that leaves a window open after a failure, and a failed scenario leaves no evidence."
- "I can't tell from the build output which scenarios failed, and nothing a manager can open."
- "A teammate wants to push a half-finished scenario and it would break the build."
- "Nobody but you knows how to run this."

Today you fix every point. At the end of the day the framework is **Project 2 as a finished first version**: tagged, filtered, hooked, parameterised through Maven, reporting, and documented.

| Day | What it contributes to today |
|---|---|
| Monday | `DriverFactory`, `-Dbrowser` and `-Dheadless` |
| Tuesday | Waits and Select helpers: still no waits in steps |
| Wednesday | Page Objects: steps still call only page object methods; today you add one small component |
| Thursday | Gherkin, steps, `TestContext`, the JUnit 5 runner |
| Friday | Scenario Outline, Background, Rule, Hooks, Tags, Maven properties and profiles, reports |

## Learning Objectives

By the end of this lab you will be able to:

- Replace repetition with **Background**, and group scenarios with **Rule**.
- Collapse data-only duplicates into a **Scenario Outline** with an Examples table.
- Implement **Hooks** (`@BeforeAll`, `@Before`, `@After`, `@AfterAll`) with the right order, a tagged hook, and a failure screenshot attached to the report.
- Design and apply a **tag taxonomy** and select scenarios with tag expressions.
- Configure **Maven**: properties, Surefire `systemPropertyVariables`, and profiles `smoke`, `regression`, `ci`.
- Configure the **JUnit Platform runner** with report plug-ins and generate an HTML report.
- Document how to run the framework so someone else can.

## Prerequisites and Source Material

Everything you need is in this week's written lessons and today's demo. Nothing in this lab needs a library or technique that is not taught there.

| Part | Read first |
|---|---|
| Part 1 | `scenario-outline-and-examples.md`, `background-and-rule.md`, `tags.md` |
| Part 2 | `hooks.md` |
| Part 3 | `junit-integration.md`, `maven-integration.md`, `cucumber-reporting.md` |
| Part 4 | Your own work; the Thursday lesson `cucumber-framework-setup.md` for the project layout |

Tools: JDK 17+, Maven 3.9+, Chrome, an IDE. Practice site: https://www.saucedemo.com (users `standard_user`, `locked_out_user`, password `secret_sauce`).

## Getting Started (10 min)

1. Open `starter_code/`. It is **Thursday's finished framework** (a working solution of the BDD layer) plus today's TODOs. If your own Thursday repo is green and tidy you may use it instead; copy over the new files listed below.
2. Run the baseline once so you know you start green: `mvn clean test -Dheadless=true`. (Needs Maven Central access.)
3. Run the two automated rule tests: `mvn test -Dtest=FeatureStyleTest,BddLayerRulesTest`. They need **no browser**. `FeatureStyleTest` should be green, `BddLayerRulesTest` should be **red**: that red list is today's to-do list. Your goal is to turn it green.
4. Read the new files:

| File | Status |
|---|---|
| `pages/HeaderComponent.java` | GIVEN - cart badge and cart link, shared by every page after login |
| `steps/Hooks.java` | TODO (Part 2) |
| `steps/CommonSteps.java` | TODO: one more shared step |
| `pom.xml`, `runners/RunCucumberTest.java` | TODO (Part 3) |
| `docs/TAGS_AND_RUNS.md`, `README_PROJECT.md` | TODO (Parts 3 and 4) |
| `quality/BddLayerRulesTest.java`, `quality/FeatureStyleTest.java` | GIVEN - **do not edit** |

---

## Part 1 - Refactor the Features (~50 min)

Read `background-and-rule.md`, `scenario-outline-and-examples.md` and `tags.md`. Work one feature at a time and run the scenarios after each (`mvn test -Dheadless=true`).

### Step 1 - Tag taxonomy first (10 min)

Before touching a feature, write the taxonomy in `docs/TAGS_AND_RUNS.md` section 1. Use exactly these tags (the test rejects any other): `@ui`, `@login`, `@cart`, `@sort`, `@smoke`, `@regression`, `@positive`, `@negative`, `@slow`, `@wip`, `@ignore`, `@report-demo`. For each, write the meaning and the rule for using it.

### Step 2 - `login.feature`: Outline and tags (10 min)

1. Put `@ui @login` on the line above `Feature:` (it must be the first line of the file).
2. Keep **Successful login** as its own scenario, tagged `@smoke @positive`.
3. Replace the four rejection scenarios with **one Scenario Outline** whose Examples table has four rows (wrong password, locked-out user, missing username, missing password) and a `description` column so the title reads well (`Login with <description> is rejected`). Tag it `@regression @negative`.
4. Add a **work-in-progress scenario**: "A customer can reset a forgotten password by email" with steps you have not implemented (`the customer asks for a password reset email`, `the customer receives a reset link`). Tag it `@wip`. Do **not** implement those steps.

### Step 3 - `sort.feature`: Background (10 min)

1. Tag the feature `@ui @sort`.
2. Move `Given the shopper is logged in` into a **Background** and delete it from every scenario.
3. Tag exactly one scenario `@smoke`, the rest `@regression`.

### Step 4 - `cart.feature`: Background and Rules (10 min)

1. Tag the feature `@ui @cart`. Add a Background with the login Given.
2. Group the scenarios into two **Rules**: "Adding a product puts it in the cart" and "Removing a product takes it out of the cart". Write each rule's name as the business rule, not a test description.
3. Give the second Rule its own **Background** that puts "Sauce Labs Backpack" in the cart (see step 5). The removal scenarios then no longer repeat that setup.
4. Tag the scenarios: two of them `@smoke @regression`, the rest `@regression`, and the data-table scenario also `@slow`.

### Step 5 - One more shared step, and the header component (10 min)

1. In `CommonSteps`, add `Given the shopper has {string} in the cart` implemented with `InventoryPage.addToCart`. It is used by the cart Rule Background and by the sort scenario "Sorting does not change the cart", where you replace the old `And the shopper adds ... to the cart` with this Given.
2. In `CartSteps`, read the cart count and open the cart through `HeaderComponent` instead of `InventoryPage`. Reason: the badge exists on every page, so the check works whichever page the scenario is on.
3. Delete the step `the cart does not list {string}` and rewrite the scenario that used it so its last Then is `the cart count shows 1`. Fewer steps, fewer places to break.

**Checkpoint:** `mvn test -Dheadless=true` still green with the default (no tag filter yet, so the `@wip` scenario reports undefined steps; that is expected until Part 3 adds the filter). If you want a clean run now: `-Dcucumber.filter.tags="not @wip"`.

---

## Part 2 - Hooks (~30 min)

Read `hooks.md`. Implement `steps/Hooks.java` from the skeleton.

| Hook | What it does | Order |
|---|---|---|
| `@BeforeAll` (static) | prints one banner line with browser, headless and the tag filter | - |
| `@Before` | logs the scenario name (`scenario.log`) and starts the browser (`context.driver()`) | 0 |
| `@Before("@slow")` | tagged hook: logs a warning for `@slow` scenarios only | 5 |
| `@After` | if the scenario failed, attaches a PNG screenshot (`scenario.attach`); logs the URL | 10 |
| `@After` | quits the browser (`context.quitDriver()`) | 0 |
| `@AfterAll` (static) | prints one closing line | - |

Then clean up Thursday's workaround: delete `OPEN_DRIVERS`, the static initialiser with the shutdown hook, and `closeLeftovers()` from `TestContext`. The `@After` hook owns cleanup now.

Check yourself: the AFTER hook with the **higher** number runs **first**. The screenshot must be taken before the browser is closed.

---

## Part 3 - Maven, Runner and Reports (~45 min)

Read `junit-integration.md`, `maven-integration.md`, `cucumber-reporting.md`.

### Step 1 - Runner plug-ins (10 min)

In `RunCucumberTest`, extend the plug-in value to: `pretty, summary`, an HTML report, a JSON report, a JUnit XML report and a rerun file, all under `target/` (the exact strings are in the TODO comment). Do **not** add a tag filter here.

### Step 2 - POM properties, Surefire and profiles (20 min)

1. Add the properties `browser` (chrome), `headless` (false) and `cucumber.filter.tags` (`not @wip and not @ignore`).
2. Forward all three into the test JVM with Surefire `<systemPropertyVariables>`.
3. Add profiles: `smoke` (`@smoke and not @wip`), `regression` (`@regression and not @wip`), `ci` (headless true).
4. Add the `maven-cucumber-reporting` plug-in on the `verify` phase reading the JSON report.
5. Add `src/test/resources/junit-platform.properties` with `cucumber.junit-platform.naming-strategy=long` and `cucumber.execution.parallel.enabled=false`.

### Step 3 - Prove every run mode (10 min)

Run each command and write the result (scenario count, pass/fail) in section 2 of `docs/TAGS_AND_RUNS.md`:

    mvn clean test
    mvn clean test -Psmoke
    mvn clean test -Pregression
    mvn clean test -Pci
    mvn clean test -Dcucumber.filter.tags="@cart and not @slow"
    mvn clean verify -Psmoke -Pci

Notice which setting wins when a profile and a `-D` disagree.

### Step 4 - Failure evidence (5 min)

1. Temporarily add a scenario tagged `@report-demo` to `sort.feature` with a **wrong** expectation (sort by price low to high, then assert "listed from most expensive to cheapest").
2. Run it: `mvn clean test -Dcucumber.filter.tags="@report-demo"`. It must be **red**.
3. Open `target/cucumber-reports/report.html`: find the red step and the attached screenshot. Read `target/rerun.txt`.
4. Describe what you saw in section 4 of `docs/TAGS_AND_RUNS.md`. Then **delete the scenario** and the tag and confirm the suite is green again.

---

## Part 4 - Project 2 Wrap-up (~25 min)

1. Complete `README_PROJECT.md`: requirements, run commands, project structure, tag strategy, reports, and tick the milestone checklist honestly.
2. Complete `docs/TAGS_AND_RUNS.md` (every `<<FILL>>` replaced).
3. Run `mvn test -Dtest=FeatureStyleTest,BddLayerRulesTest`: both green.
4. Run the full default suite headless once more. Note the result in the README.

### Project 2 Milestone Checkpoint (Day 5)

| Milestone | Evidence |
|---|---|
| M1 Monday: skeleton and DriverFactory | `drivers/`, `ScreenshotUtil` |
| M2 Tuesday: stable waits and Select helper | `WaitUtils`, `DropdownUtils` |
| M3 Wednesday: Page Objects | `pages/` |
| M4 Thursday: BDD layer v1 | features, steps, `TestContext` |
| **M5 Friday: BDD layer complete** | tags, Outline/Background/Rule, Hooks, profiles, reports, docs |

Next week Project 2 continues from exactly this repository: keep it clean and committed.

---

## Stretch Goals (optional)

1. Add a Scenario Outline to `sort.feature` that runs the three sort options from one Examples table, and decide which rows deserve `@smoke`.
2. Add a second Examples table to the login Outline with its own tag (`@smoke` rows) and observe how tags on `Examples:` select rows.
3. Run the `@regression` profile twice and compare the report totals; discuss why a flaky test would show here.
4. Use `target/rerun.txt` to re-run only the failed scenarios (`-Dcucumber.features=@target/rerun.txt`).
5. Add a `@Before("not @slow")` hook that logs "fast scenario" and explain which scenarios it runs for.

## Definition of Done

- [ ] `BddLayerRulesTest` and `FeatureStyleTest` are green.
- [ ] Every feature starts with a tag line containing `@ui`; only taxonomy tags are used; every scenario is `@smoke`, `@regression` or `@wip`.
- [ ] 3 to 6 `@smoke` scenarios spanning at least 3 features; one `@wip` scenario excluded by default.
- [ ] Background in at least 2 features, at least 1 Rule, and an Outline with at least 4 Examples rows.
- [ ] `Hooks.java` has the six hooks with the specified orders; `TestContext` has no static safety net.
- [ ] `pom.xml`: properties, `systemPropertyVariables`, profiles smoke/regression/ci, reporting plug-in.
- [ ] Runner has html, json, junit, rerun and summary plug-ins and no tag filter.
- [ ] `docs/TAGS_AND_RUNS.md` and `README_PROJECT.md` are complete, with no `<<FILL>>` left.
- [ ] The failing-scenario evidence is described; the temporary scenario and `@report-demo` are removed.
- [ ] No `Thread.sleep`, no `By`/`findElement` in steps or hooks.

## Grading Rubric (100 points)

| Area | Points |
|---|---|
| Feature refactor (Outline, Background, Rules, readable Gherkin) | 20 |
| Tag taxonomy applied consistently, `@wip` excluded | 15 |
| Hooks (order, tagged hook, failure screenshot, cleanup) | 15 |
| Maven properties, Surefire forwarding, profiles | 15 |
| Runner and reports (all plug-ins, evidence of a failing run) | 10 |
| Documentation (`TAGS_AND_RUNS.md`, `README_PROJECT.md`) | 15 |
| Automated rule tests green, clean code, no waits or locators in steps | 10 |

## Hints (open only if stuck)

<details><summary>Tag placement</summary>
A tag line goes directly above `Feature:`, `Rule:`, `Scenario:` or `Examples:`. Tags on a Feature are inherited by every scenario in it. A blank line between the tag line and the keyword is allowed by Gherkin but keep them together for readability.
</details>

<details><summary>Scenario Outline placeholders</summary>
Placeholders in angle brackets (`<username>`) must match a column header exactly. An empty cell gives an empty string, so `"<username>"` becomes `""`. Placeholders also work in the scenario title.
</details>

<details><summary>Hook order</summary>
`@Before(order=0)` runs before `@Before(order=5)`. For `@After` it is reversed: `order=10` runs before `order=0`. Use that to take the screenshot before the browser quits.
</details>

<details><summary>Tag expression syntax</summary>
`@smoke and not @wip`, `@cart or @sort`, `(@smoke or @regression) and not @slow`. Quote the whole expression on the command line.
</details>

<details><summary>-D is ignored</summary>
Surefire runs the tests in a separate JVM. Properties must be forwarded with `<systemPropertyVariables>`; a `-D` on the Maven command line overrides the pom property, which overrides nothing else.
</details>

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| The `@wip` scenario still runs / undefined steps reported | The filter is not reaching Cucumber: check `systemPropertyVariables` and the property name `cucumber.filter.tags` |
| Profile has no effect | Profile id typed wrong, or the `-D` on the command line is overriding it |
| Report folder empty | Plug-in paths must start with `target/`; run `mvn clean test` again |
| `cucumber-html-reports` missing | It is built in the `verify` phase: use `mvn clean verify` |
| Screenshot missing from the report | The `@After` screenshot hook runs after the quit hook: swap the `order` values |
| `AmbiguousStepDefinitionsException` | The same step text exists in two classes: keep one definition in `CommonSteps` |
| Browser window stays open after a failure | The `quitDriver()` hook is missing or throws before it runs |
| `BddLayerRulesTest` fails on "first line" | The tag line must be the very first line of the feature file, with `@ui` in it |

## Submission

Zip or push the whole repository (without `target/`). Include a short note with the output of the six run commands from Part 3 step 3 and a screenshot of the failing-scenario report. Submit by the end of the day.
