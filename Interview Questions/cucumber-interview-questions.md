# Cucumber and BDD Interview Questions

**For self-study after Cucumber Handouts 1–4.** Each question has a difficulty (**Easy**, **Medium**, **Hard**), a type (**Concept**, **Code**, **Design**, **Process**, **Scenario**), and a model answer. Try to answer out loud or on paper **first**, then click **Show answer** to check.

**How to read this file:** open it in VS Code's Markdown preview (`Ctrl+Shift+V`) or on GitHub, where each answer is hidden behind **Show answer**.

**Sections**

1. BDD, user stories and acceptance criteria (Handout 1)
2. Gherkin, features and scenarios (Handout 1)
3. Cucumber setup and step definitions (Handout 2)
4. Outlines, backgrounds, rules and hooks (Handout 3)
5. Tags, JUnit, Maven and reports (Handout 4)
6. Framework design: Selenium + Cucumber
7. Scenario-based questions

---

## 1. BDD, user stories and acceptance criteria

### Q1. What is BDD? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Behaviour-Driven Development is a way of working in which the team agrees how the system should **behave** by discussing **concrete examples** in a **shared, plain language** before coding, then uses those examples as automated checks. It has three practices: **Discovery** (talk through examples), **Formulation** (write them as scenarios, usually in Gherkin) and **Automation** (make them run, e.g. with Cucumber).

</details>

### Q2. Is BDD the same as using Cucumber? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

No. BDD is a **way of working**; Cucumber is a **tool** that supports the Automation part. A team can practise BDD with index cards and no tool. A team that writes Cucumber tests without talking to the business isn't doing BDD; it's just writing tests in a more verbose format.

</details>

### Q3. What is the difference between TDD, ATDD and BDD? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

- **TDD:** developers write a failing **unit** test, then the code that makes it pass; focused on code design.
- **ATDD:** the team agrees **acceptance tests** before development; focused on meeting requirements.
- **BDD:** grew out of TDD and is a form of ATDD that stresses **behaviour**, **examples** and a **shared language** readable by business people, typically written as Given/When/Then.

</details>

### Q4. Who are the Three Amigos, and why do they meet? `Easy` · Process

<details>
<summary><b>Show answer</b></summary>

Three viewpoints that discuss a user story before development: **business** (product owner/BA), **development** and **testing**. Each spots different gaps: the PO knows the rules, developers know the constraints, testers ask "what if...?". The output is shared understanding, agreed examples and open questions.

</details>

### Q5. What is "living documentation"? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Scenarios that both **describe** how the system behaves and are **run** as automated tests. Unlike a Word specification, they can't silently go out of date: if the system stops matching them, the build fails.

</details>

### Q6. What is the difference between a rule and an example? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A **rule** is general: "locked-out users cannot log in". An **example** is concrete, with real values: "`locked_out_user` with `secret_sauce` sees *Epic sadface: Sorry, this user has been locked out.*" Everyone can agree with a rule but mean different things; examples expose those differences.

</details>

### Q7. What is a user story? Describe its usual format. `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A short description of a user need from the user's point of view: **As a** (who) **I want** (what) **So that** (why). It is a placeholder for a conversation, not a full specification. The *so that* part states the value and helps choose the right solution.

</details>

### Q8. What does INVEST stand for? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

A good story is **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall and **T**estable.

</details>

### Q9. What makes a good acceptance criterion? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

It is **testable** (pass/fail can be decided), **clear** (one meaning), **outcome-focused** (what happens, not how it's built), independent of UI details, and concise. "Tax is 8% of the item total, rounded to the nearest cent" is good; "tax is added" is not.

</details>

### Q10. What is the difference between acceptance criteria and the Definition of Done? `Medium` · Process

<details>
<summary><b>Show answer</b></summary>

**Acceptance criteria** belong to **one story** ("tax is 8%..."). The **Definition of Done** applies to **every** story ("code reviewed, tests pass, no critical bugs"). A story is finished only when it meets both.

</details>

### Q11. Describe Example Mapping. `Medium` · Process

<details>
<summary><b>Show answer</b></summary>

A ~25-minute workshop with coloured cards: **yellow** = the story, **blue** = rules (acceptance criteria), **green** = examples under each rule, **red** = open questions. Many red cards → the story isn't ready; many blue cards → it's too big and should be split; a rule with no examples → nobody really understands it yet.

</details>

---

## 2. Gherkin, features and scenarios

### Q12. What is Gherkin? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

The structured, plain-language format for BDD scenarios, in `.feature` files. It uses keywords (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`, `Background`, `Rule`, `Scenario Outline`, `Examples`) and is strict about structure but free about the words after each keyword. Cucumber, Reqnroll/SpecFlow and Behave all read it.

</details>

### Q13. What do Given, When and Then each mean? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

**Given** is the starting situation (context). **When** is the action or event the scenario is about, normally one. **Then** is the expected outcome a user can observe. `And` and `But` continue the previous kind of step.

</details>

### Q14. Does Cucumber care whether a step starts with Given, When or Then? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Not when matching. Cucumber ignores the keyword and matches only the text after it, so `Given I add "X" to the cart` and `When I add "X" to the cart` run the **same** step definition. The keywords matter for **readers**.

</details>

### Q15. What is the difference between declarative and imperative scenarios? Which is better? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

**Imperative** steps describe UI mechanics: "I type standard_user into #user-name, I click #login-button". **Declarative** steps describe intent: "Given I am logged in as standard_user". Declarative is better: business people can read it, and it survives UI changes because the details live in step definitions and page objects.

</details>

### Q16. Why should scenarios be independent? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

So each scenario can run **alone and in any order** and a failure points to one cause. A scenario that relies on another having run first fails whenever the order changes, a single scenario is rerun, or scenarios run in parallel. Each scenario sets up its own state with `Given` steps (or a Background).

</details>

### Q17. Why should a scenario usually have only one `When`? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

One `When` = one behaviour. Several actions usually mean several behaviours mixed together, which makes the scenario long and the cause of a failure unclear. Split it, or move earlier actions into `Given` steps that describe the resulting state.

</details>

### Q18. What are data tables and doc strings in Gherkin? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Extra arguments under a step. A **data table** is rows of `| ... |` values, e.g. a list of products; a one-column table arrives in Java as `List<String>`. A **doc string** is a block of text between `"""` lines, for longer text such as a message or JSON.

</details>

### Q19. What happens if you forget the colon after `Scenario`? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Gherkin may not report an error: the line can be treated as **description text** of the previous block, so the scenario silently disappears from the run. Every block keyword must end with a colon: `Feature:`, `Scenario:`, `Background:`, `Examples:`.

</details>

---

## 3. Cucumber setup and step definitions

### Q20. What is Cucumber, and what does it need to test a web application? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Cucumber runs Gherkin scenarios as automated tests: it reads `.feature` files, matches each step to a step definition, runs them and reports results. It doesn't drive browsers itself: step definitions call **Selenium** (through page objects) for that, and use **JUnit** assertions to check results.

</details>

### Q21. Which Maven dependencies does a Cucumber + JUnit + Selenium project need? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

`selenium-java` (browser), `junit-jupiter` (assertions), `junit-platform-suite` (suite annotations), `cucumber-java` (Cucumber and `@Given/@When/@Then`) and `cucumber-junit-platform-engine` (lets JUnit run scenarios). The two Cucumber modules must share one version, as must the JUnit modules; BOMs help with that.

</details>

### Q22. What is "glue" in Cucumber? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

The Java package(s) where Cucumber looks for step definitions and hooks, set with the `cucumber.glue` setting. If the glue doesn't match the package of the step classes, every step is reported as undefined.

</details>

### Q23. What is a step definition? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A Java method annotated with `@Given`, `@When` or `@Then` containing a **Cucumber Expression** that matches step text. Cucumber passes the values from the step to the method's parameters and runs it.

</details>

### Q24. Explain Cucumber Expressions with an example. `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

The step text with **placeholders** for values:

```java
@When("I log in as {string} with password {string}")
public void iLogInAs(String username, String password) { ... }

@Then("the cart badge should show {int}")
public void theCartBadgeShouldShow(int expected) { ... }
```

`{string}` matches text in double quotes, `{int}` a whole number, `{bigdecimal}` a decimal (good for money), `{word}` a single word.

</details>

### Q25. What are the possible step results? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

**passed** (ran without an exception), **failed** (threw, often a failed assertion), **skipped** (an earlier step didn't pass), **undefined** (no step definition matches) and **ambiguous** (more than one matches). Pending steps (`PendingException`) are also reported.

</details>

### Q26. What is a snippet, and how do you use it? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

When a step is undefined, Cucumber prints ready-to-paste Java with the right annotation, expression and parameters. Paste it into a step class and replace the `throw new PendingException()` line with page object calls.

</details>

### Q27. What is an ambiguous step, and how do you fix it? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

Two step definitions whose expressions both match the same step text; Cucumber stops with `AmbiguousStepDefinitionsException`. Delete the duplicate or reword one expression so each step matches exactly one method.

</details>

### Q28. What does "keep step definitions thin" mean? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

A step definition should be a line or two that **calls page objects**, plus an assertion in `Then` steps. Locators, waits and page details belong in page objects. Thin steps are reusable, readable, and a UI change is fixed in one page class instead of many steps.

</details>

### Q29. Why can't Cucumber step classes simply extend `BaseTest`? `Hard` · Design

<details>
<summary><b>Show answer</b></summary>

`BaseTest` uses JUnit's `@BeforeEach`/`@AfterEach`, which Cucumber step classes don't use; Cucumber creates step classes itself and uses its own lifecycle (hooks). Several step classes also take part in one scenario, so they need to **share** one browser. A common beginner solution is a `BaseSteps` parent class with a `protected static WebDriver driver`, plus Cucumber hooks to open and close it. (Cucumber also refuses to let a class extend another class that contains step definitions or hooks.)

</details>

### Q30. What is a dry run? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A run that only checks every step has a matching step definition, **without executing** them (no browser opens). Useful after writing feature files: `-Dcucumber.execution.dry-run=true`.

</details>

---

## 4. Outlines, backgrounds, rules and hooks

### Q31. What is a Scenario Outline? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A template for several scenarios with the **same steps** but **different data**. Steps contain placeholders such as `<username>`, and an `Examples` table supplies one row per scenario; Cucumber runs the outline once per row.

</details>

### Q32. When should you **not** use a Scenario Outline? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

When the cases have **different behaviour or outcomes**. Successful and refused logins have different `Then` steps, so they belong in two outlines (or scenarios), not one outline with an "expected result" column whose step definition branches with `if`. Also avoid huge outlines with many columns.

</details>

### Q33. A placeholder `<usrname>` doesn't match the column `username`. What happens? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

The placeholder isn't replaced, so the step receives the literal text `<usrname>` and the login fails or the step doesn't match. Placeholders must match the header exactly: spelling, capitals and spaces.

</details>

### Q34. What is a Background? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

`Given` steps that run **before every scenario** in the feature (or rule), so common setup isn't repeated. It runs once **per scenario**, not once per feature, so every scenario still starts fresh. Keep it short and only for context every scenario needs.

</details>

### Q35. What is the `Rule` keyword for? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

It groups the scenarios that illustrate **one business rule** (an acceptance criterion), like a blue card in Example Mapping. A Rule has a title and may have its own Background. It makes feature files mirror the acceptance criteria.

</details>

### Q36. What are hooks? Name the main ones. `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Methods Cucumber runs automatically around scenarios: `@Before` (before each scenario), `@After` (after each scenario, pass or fail), `@BeforeStep`/`@AfterStep` (around every step), `@BeforeAll`/`@AfterAll` (once per run). They are for technical setup and clean-up, e.g. opening/closing the browser and screenshots on failure.

</details>

### Q37. How does hook `order` work for `@Before` and `@After`? `Hard` · Concept

<details>
<summary><b>Show answer</b></summary>

`@Before` hooks run from **low to high** order; `@After` hooks run from **high to low**. So a screenshot hook with `@After(order = 1)` runs **before** a quit hook with `@After(order = 0)`, while the browser is still open.

</details>

### Q38. How do you attach a screenshot to a failed scenario? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

In an `@After` hook that takes a `Scenario`:

```java
@After(order = 1)
public void screenshotIfFailed(Scenario scenario) {
    if (scenario.isFailed()) {
        byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", scenario.getName());
    }
}
```

The image appears in the HTML report next to the failed step.

</details>

### Q39. What is a tagged hook? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

A hook that runs only for scenarios with a given tag, e.g. `@Before("@maximized")` to maximise the window only for scenarios tagged `@maximized`.

</details>

### Q40. Should logging in go in a hook or a Given step? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

In a **Given step** (or a Background). Logging in is **business context** that readers of the feature need to see. Hooks are for technical details readers don't care about, such as browsers and screenshots.

</details>

---

## 5. Tags, JUnit, Maven and reports

### Q41. What are tags used for? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Labels like `@smoke`, `@SL-101`, `@wip` on features, rules, scenarios or examples. They let you **select** what to run (only smoke tests, one story), **trace** scenarios back to stories, exclude unfinished work, and attach **tagged hooks**. Scenarios inherit tags from their feature, rule and examples.

</details>

### Q42. Write a tag expression that runs smoke tests but not work in progress. `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

`@smoke and not @wip`, e.g. `mvn test -Dtest=RunCucumberTest -Dcucumber.filter.tags="@smoke and not @wip"`. Expressions support `and`, `or`, `not` and brackets.

</details>

### Q43. How does Cucumber run through JUnit? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

The JUnit Platform is the layer IDEs and Maven use to run tests. The `cucumber-junit-platform-engine` plugs Cucumber into it as a test engine (next to Jupiter for `@Test`). A suite class with `@Suite`, `@IncludeEngines("cucumber")` and `@SelectPackages("features")` tells JUnit to run the feature files, and each scenario is reported as one JUnit test.

</details>

### Q44. Where can Cucumber's settings (glue, plugins) be configured? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

Two common places:
- **`@ConfigurationParameter`** annotations on the suite class (e.g. `key = GLUE_PROPERTY_NAME`): visible in one place, good for a single suite or per-suite settings.
- **`src/test/resources/junit-platform.properties`**: shared by every suite.

Set each key in one place only; a suite's `@ConfigurationParameter` overrides the file, which can make file changes seem to do nothing.

</details>

### Q45. What is the difference between `@IncludeTags("smoke")` and `cucumber.filter.tags=@smoke`? `Hard` · Concept

<details>
<summary><b>Show answer</b></summary>

`@IncludeTags` (or Maven's `-Dgroups=smoke`) is a **JUnit** tag filter: non-matching scenarios aren't run or reported. `cucumber.filter.tags` is a **Cucumber** filter: Cucumber skips non-matching scenarios, so JUnit may report them as **skipped**. JUnit tags are written without `@`.

</details>

### Q46. What does `mvn test` do? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

It runs Maven's phases up to `test`: validate, compile, test-compile, test. The Surefire plugin runs all tests through the JUnit Platform: the Selenium JUnit tests **and** the Cucumber suites. `mvn clean test` first deletes the `target` folder so nothing old is reused.

</details>

### Q47. What is a BOM in Maven, and why use one? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

A "bill of materials": a list of matching versions for a family of libraries (e.g. `cucumber-bom`, `junit-bom`), imported in `<dependencyManagement>`. Dependencies then omit `<version>`. It keeps related modules on the same version (mixed versions cause errors like `NoSuchMethodError`) and makes upgrading a one-line change.

</details>

### Q48. What is a Maven profile? Give a testing example. `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

A named block of extra configuration switched on with `-P<name>`. Example: a `smoke` profile that sets Surefire's `<groups>smoke</groups>`, so `mvn test -Psmoke` runs only smoke-tagged tests and scenarios.

</details>

### Q49. Which Cucumber reports do you know, and who reads them? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

`pretty` and `summary` (console, for you); `html` (a web page for the team and product owner); `json` (for other reporting tools); `junit` XML (for CI servers); `rerun` (a list of failed scenarios to run again). They are set in `cucumber.plugin`; only one plugin may write to the console.

</details>

### Q50. The run stops with "Cucumber needs a JSON library to write reports". Why? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

Since Cucumber 8, file reports such as `html` and `json` need a JSON library that is no longer bundled. Add **Jackson** as a test dependency (e.g. `tools.jackson.core:jackson-databind`).

</details>

---

## 6. Framework design: Selenium + Cucumber

### Q51. Describe the structure of a Selenium + Cucumber framework you have built. `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

For example:
- **`pages`:** page objects (`LoginPage`, `InventoryPage`, `CartPage`) holding locators, waits and user actions.
- **`steps`:** step definitions per area (`LoginSteps`, `CartSteps`, `SortSteps`) that call page objects; `BaseSteps` holds the shared driver; `Hooks` opens/closes the browser and attaches screenshots on failure.
- **`src/test/resources/features`:** feature files per capability, tagged with story ids and `@smoke`.
- **Runner:** `RunCucumberTest` (JUnit suite); settings in `junit-platform.properties`.
- **Build:** Maven with BOMs, a `smoke` profile, and HTML/JSON/JUnit reports for CI.

</details>

### Q52. Why separate feature files, step definitions and page objects into layers? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

Each layer changes for a different reason: **features** when requirements change, **steps** when wording or flows change, **page objects** when the UI changes. Keeping them separate means a UI change is fixed once in a page object, scenarios stay readable for business people, and steps stay thin and reusable.

</details>

### Q53. How do several step classes share one browser? `Hard` · Design

<details>
<summary><b>Show answer</b></summary>

Cucumber creates each step class itself, so they need a shared place for the driver. Simple approach: a `BaseSteps` parent class with `protected static WebDriver driver`, extended by every step class and by `Hooks`, which opens it in `@Before` and closes it in `@After`. A more advanced approach is **dependency injection** (e.g. `cucumber-picocontainer`), where Cucumber passes one shared context object to every step class's constructor for each scenario; it also supports parallel runs better than a `static` field.

</details>

### Q54. Why is a `static` WebDriver a problem for parallel execution? `Hard` · Design

<details>
<summary><b>Show answer</b></summary>

A `static` field is shared by everything in the JVM. If two scenarios run at the same time, both use and overwrite the same driver, so one scenario's steps act on the other's browser. Parallel frameworks give each thread its own driver (e.g. `ThreadLocal<WebDriver>`) or use dependency injection with one context per scenario.

</details>

### Q55. Where should waits live in a Selenium + Cucumber framework? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

In **page objects**: e.g. `InventoryPage` waits until the products page is shown, and `title()` waits for the title to be visible. Steps and feature files stay free of timing details, and every test that uses the page waits the same way.

</details>

### Q56. What would you put in a smoke suite, and how would you run it in CI? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

A few fast scenarios that prove the most important flows work: login, add to cart, a key sort or checkout. Tag them `@smoke`, and run them with a dedicated profile or suite (`mvn test -Psmoke`) on every commit; run the full suite nightly or before releases. Publish the HTML and JUnit XML reports from the CI job.

</details>

---

## 7. Scenario-based questions

### Q57. You join a team whose Cucumber steps are full of locators and `Thread.sleep`. What would you improve first? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Introduce **page objects** and move locators and actions out of the steps, so steps become one or two lines. Replace `Thread.sleep` with **explicit waits** inside the page objects. Do it gradually, page by page, keeping the suite green, and agree on conventions (thin steps, declarative scenarios) with the team.

</details>

### Q58. Every step in your project is reported as undefined, though the step classes exist. What do you check? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

The **glue** setting: it must match the package of the step classes (and the hooks). Also check the classes are under `src/test/java`, compile without errors, and that the step text matches the expressions exactly. With settings in two places (runner and properties file), check which one is really used.

</details>

### Q59. A product owner says the feature files are "unreadable". What do you change? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Rewrite scenarios **declaratively**: remove locators, button names and click-by-click steps; use business language agreed in Discovery; one behaviour per scenario with clear titles; move repeated setup into a Background; group scenarios by Rule. Review the result with the product owner: they should be able to say whether each scenario is right.

</details>

### Q60. A scenario fails only when run with the full suite, never alone. What is likely wrong? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

**Shared state** between scenarios: a browser, login, cart or test data left by an earlier scenario. Check that each scenario starts with its own `Given` steps, that hooks open a fresh browser per scenario and close it afterwards, and that no `static` data is reused across scenarios.

</details>

### Q61. A scenario failed in last night's CI run. How do you find out why? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

Open the **HTML report**: find the failed scenario, the failed step, the assertion message and the **screenshot** attached by the `@After` hook. Rerun only the failed scenarios using the `rerun` report or by file and line, check the CI logs, then fix the cause (test or application bug) and raise a defect if the application is wrong.

</details>

### Q62. The team adds new scenarios that aren't automated yet, and the build turns red. What do you do? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

Tag them `@wip` and exclude that tag from the main run (`@ExcludeTags("wip")` on the suite, or `not @wip` in the tag expression), so they don't break the build until their step definitions are written. Remove the tag once they're automated.

</details>

### Q63. You need to test login with 15 different users and expected messages. How would you write it? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Use **Scenario Outlines**: one outline for users who log in successfully and one for users who are refused (with the expected message as a column), with an `Examples` table each. Group rows into titled `Examples` blocks if useful, and keep each outline to one kind of outcome. No new step definitions are needed.

</details>

### Q64. Developers change the login button's id, and 40 scenarios fail. How should your framework have limited this? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

With the Page Object Model, the locator lives in **one** place, `LoginPage`, so the fix is one line and all 40 scenarios pass again. If locators were copied into steps, that's the design to fix. Also ask developers for stable test attributes (`data-test`) that don't change with styling.

</details>

### Q65. The smoke suite takes 40 minutes. How do you speed it up? `Hard` · Scenario

<details>
<summary><b>Show answer</b></summary>

Check that it really contains only a **few critical** scenarios. Remove `Thread.sleep` and use explicit waits; use shortcuts in `Given` steps (e.g. deep links instead of clicking through menus). Run headless with a fixed window size on CI. Then consider **parallel** execution, which requires each scenario to have its own driver (not a `static` one) and no shared test data.

</details>

### Q66. The business wants scenarios in another spoken language. Is that possible? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Yes. Gherkin supports 70+ languages: add `# language: es` (for example) at the top of the feature file and use that language's keywords (`Característica`, `Escenario`, `Dado`, `Cuando`, `Entonces`). Step definitions are matched on the step text, so their expressions must use the same language.

</details>

### Q67. In a sprint, when should a QE write the feature files? `Medium` · Process

<details>
<summary><b>Show answer</b></summary>

**Before** development: during or right after the Three Amigos / Example Mapping session in refinement or early in the sprint, so developers build against agreed examples. Automation (step definitions) can be written alongside development, and the scenarios pass when the story is done, which supports the Definition of Done.

</details>

### Q68. A story has many red question cards after Example Mapping. What happens next? `Easy` · Process

<details>
<summary><b>Show answer</b></summary>

The story is **not ready** for development. The product owner (or whoever can answer) resolves the questions, possibly with a short investigation, and the team maps the story again. Starting development with open questions leads to rework.

</details>
