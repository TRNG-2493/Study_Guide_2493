# Lab 4 (Thursday): Pair Programming - Three Amigos, Features and Step Definitions for Project 2

**Week 6 · Day 4 · BDD & Cucumber · Mode A (Code Lab) · COLLABORATIVE PROJECT (pairs, Driver / Navigator)**
**Estimated time:** 3 hours (six 30-minute driver slots)
**Project lane:** Project 2 - Test Automation Framework (Milestone 4: BDD layer, first version)
**Deliverable:** one shared repository (or branch) per pair + a short written retrospective

---

## The Scenario

Your product owner has asked the Project 2 team to stop writing tests that only programmers can read. From today the framework gets a **BDD layer**: stories and acceptance criteria are agreed together, written as Gherkin features anyone in the business can read, and automated with step definitions that sit on top of the **Page Objects** you built yesterday.

You work in a **pair**. You will run a small **Three Amigos** session (a pair covers three roles by wearing three hats), turn three user stories into Gherkin, and wire them to real browser actions through Cucumber. Everything you learned this week is used today:

| Day | What it contributes to today's deliverable |
|---|---|
| Monday | `DriverFactory`: the browser behind the scenes; `-Dbrowser` and `-Dheadless` still work |
| Tuesday | `WaitUtils`: pages are stable, so steps contain **no waits** |
| Wednesday | Page Objects: steps call **only** page object methods, never `By` |
| Thursday | Stories, acceptance criteria, Gherkin, step definitions, PicoContainer, JUnit 5 runner |

## Learning Objectives

By the end of this lab you will be able to:

- Turn a one-line requirement into an INVEST user story with testable acceptance criteria.
- Run an example-mapping conversation that surfaces rules, examples and questions.
- Write Gherkin features and scenarios in business language (no clicks, no ids, no locators).
- Implement step definitions with Cucumber expressions, parameters and a data table.
- Share state between steps with PicoContainer (`TestContext`) and avoid ambiguous steps.
- Work as **Driver and Navigator**, swap on schedule, and reflect on the collaboration.

## Prerequisites and Source Material

| Need | Where |
|---|---|
| BDD, Three Amigos, living documentation | `written/4-thursday/bdd-fundamentals.md` |
| Stories, INVEST, acceptance criteria, example mapping | `written/4-thursday/user-stories-and-acceptance-criteria.md` |
| Gherkin grammar, data tables | `written/4-thursday/gherkin.md` |
| Features, scenarios, good scenario style | `written/4-thursday/features-and-scenarios.md` |
| Given / When / Then discipline | `written/4-thursday/given-when-then.md` |
| Step definitions, parameters, sharing state | `written/4-thursday/step-definitions.md` |
| Maven, runner, PicoContainer setup | `written/4-thursday/cucumber-framework-setup.md` |
| Worked example you are extending | `demos/4-thursday/` (Instructor Guide, `code/cucumber-demo/`) |
| Page Objects you will call | Wednesday's `BasePage`, `LoginPage`, `InventoryPage`, `CartPage` (included in `starter_code/`) |

**Not for today (Friday topics):** `Background`, `Scenario Outline` / `Examples`, `Rule`, tags, `@Before`/`@After` hooks and reports. An automated check (below) fails if they appear.

**Practice site:** <https://www.saucedemo.com> (`standard_user`, `locked_out_user`, password `secret_sauce`).

---

## How the Pair Works

**Roles**

- **Driver:** the only person typing. Narrates what they are doing and why.
- **Navigator:** does *not* touch the keyboard. Reviews every line, thinks one step ahead, watches the clock, and keeps the checklist below. Asks "why?" and "what if?", instead of dictating keystrokes.

**Swap every 30 minutes** at the slot boundary (set a timer). **Commit before each swap**, authored by the outgoing driver (`git config user.name` per machine, or `git commit --author="Name <email>"`), so the history shows alternating authors. If you work on one machine, switch seats and update the author.

**Three hats** (a pair has two people, so one person wears two hats at a time and you rotate on purpose):

| Hat | Question |
|---|---|
| Business | What value does the user get, and what is the rule? |
| Developer | How would the system behave, and what would it need? |
| Tester | What could go wrong? What is the awkward example? |

**Navigator checklist** (copy into `docs/PAIR_LOG.md` notes as you go):

- [ ] Does the scenario describe *behaviour*, not clicks?
- [ ] Is every step reusable (parameters instead of hard-coded values)?
- [ ] Does the step class call only page objects?
- [ ] Are assertions only in `@Then` steps?
- [ ] Did we run it, or are we guessing?

## Timeline (six slots)

| Slot | Driver | Task | Output |
|---|---|---|---|
| 1 (0:00-0:30) | A | Setup (clone/copy, run the demo scenarios, pair agreement) and **Three Amigos part 1**: story cards and INVEST check | `docs/THREE_AMIGOS.md` (cards) |
| 2 (0:30-1:00) | B | **Three Amigos part 2**: acceptance criteria, example mapping (rules, examples, questions), list of scenario titles | `docs/THREE_AMIGOS.md` (complete) |
| 3 (1:00-1:30) | A | Login feature: add three scenarios and make them pass (reuse existing steps!) | `login.feature` |
| 4 (1:30-2:00) | B | Sort feature and `SortSteps` | `sort.feature`, `SortSteps` |
| 5 (2:00-2:30) | A | Cart feature (with a data table), `CartSteps`, `CommonSteps` | `cart.feature`, `CartSteps`, `CommonSteps` |
| 6 (2:30-3:00) | B | Integrate: full run, `FeatureStyleTest` green, `README_PROJECT.md`, then both of you write the retrospective | everything green + `docs/RETROSPECTIVE.md` |

---

## Getting Started (slot 1)

1. Copy the `starter_code/` folder, name it `qea-framework-bdd` (or continue in your Project 2 repo if you prefer), run `git init`, and create a shared branch such as `thursday/<name1>-<name2>`. Push it to a remote both of you can access (or work on one machine).
2. Confirm it builds and the two demo scenarios pass: `mvn test -Dtest=RunCucumberTest`.
3. Run the automated rules (they should be **red**): `mvn test -Dtest=FeatureStyleTest`. They turn green as you complete the work.
4. Fill in the pair agreement at the top of `docs/PAIR_LOG.md`.

```
starter_code/
├── pom.xml                                 (Selenium, Cucumber, JUnit 5, PicoContainer: given)
├── README_PROJECT.md                       (finish in slot 6)
├── docs/
│   ├── THREE_AMIGOS.md                     (slots 1-2: stories, criteria, example mapping)
│   ├── PAIR_LOG.md                         (agreement + swap log: every slot)
│   └── RETROSPECTIVE.md                    (slot 6, written together)
└── src/
    ├── main/java/com/revature/qea/         (Monday-Wednesday classes: DriverFactory, WaitUtils, pages ... given)
    └── test/
        ├── resources/features/login.feature        (2 given scenarios; you add more, plus sort + cart)
        └── java/com/revature/qea/
            ├── runners/RunCucumberTest.java        (given)
            ├── support/TestContext.java            (given: browser + sharing between steps)
            ├── quality/FeatureStyleTest.java       (given: the automated Definition of Done)
            └── steps/
                ├── LoginSteps.java                 (given: the pattern to follow)
                ├── CommonSteps.java                (TODO: shared steps)
                ├── SortSteps.java                  (TODO)
                └── CartSteps.java                  (TODO)
```

> **About browser cleanup.** In the demo the last `Then` closed the browser. That breaks when a scenario has more than one `Then`/`And`/`But`. So `TestContext` closes any leftover browser when the **next scenario** starts and the last one when the JVM exits. Your steps need no `try/finally`. (Friday's `@After` hook will do this properly.)

---

## Part A - Three Amigos Workshop (slots 1-2, ~60 min)

Work in `docs/THREE_AMIGOS.md`. Do this **before** writing any Gherkin.

### Task A1 - Story cards (slot 1)
Write three stories: **Login**, **Sort the product list**, **Shopping cart**. Use the form *As a ... I want ... so that ...* with a real role and a real benefit (not "as a user I want a button"). Tick the INVEST checklist, and rewrite any story that fails it.

### Task A2 - Acceptance criteria and example mapping (slot 2)
For each story write 3-5 testable acceptance criteria in business language (no UI words), then complete an example-mapping table: **Rules**, **concrete Examples** (real data such as `locked_out_user`) and **Open questions**. A Three Amigos session that finds no questions was not a real one: the Tester hat must find at least one question per story.

### Task A3 - Scenario list
List the scenario titles you will automate. Minimum for the whole project: **12 scenarios** (login >= 5, sort >= 3, cart >= 4). Decide which steps will be shared across features (these go into `CommonSteps`) and note what is out of scope (checkout, logout).

---

## Part B - Features and Step Definitions (slots 3-5, ~90 min)

### Rules for every feature file
- Start each feature with the **story header**: `As a ... / I want ... / so that ...`.
- Scenarios describe **behaviour**, in the language of the business. No click, button, xpath, css, locator, selector, dropdown or textbox words.
- One behaviour per scenario; at most 8 steps; each scenario has a `Given`, a `When` and a `Then`.
- Wording is **consistent**, so a single step definition (with parameters) serves several scenarios.
- Use at least one **data table** (cart) and at least one `And`/`But`.
- No `Background`, `Scenario Outline`, `Rule`, `Examples` or tags: those are Friday.

### Slot 3 - Login (Driver A)
Add **at least three** more scenarios to `login.feature` from your Three Amigos list (for example a locked-out user, a missing username, a missing password; `{string}` also matches an empty value `""`). First **check whether the existing steps can be reused**: good BDD has few steps and many scenarios. Run `mvn test -Dtest=RunCucumberTest` and fix until green.

### Slot 4 - Sort (Driver B)
Create `sort.feature` (>= 3 scenarios: price low-to-high, price high-to-low, name Z-to-A; a fourth that shows sorting does not change the cart is a good use of `But`). Implement `SortSteps` using `InventoryPage.sortBy(...)`, `getProductPrices()` and `getProductNames()`. Verify order by comparing the list with a sorted copy; never hard-code the full expected list.

### Slot 5 - Cart (Driver A)
Create `cart.feature` (>= 4 scenarios): add one product, product appears in the cart, **several products via a data table**, remove the only item, and (stretch) removing one of two keeps the other. Implement `CartSteps` and move the shared `Given the shopper is logged in` into `CommonSteps`. Remember: create the page object for the page the shopper is **on** (`InventoryPage` waits for the inventory URL, `CartPage` for the cart URL).

### Rules for every step class
- Constructor receives the shared `TestContext` (PicoContainer injects it).
- **Page objects only**: no `By`, no `findElement`, no waits, no `Thread.sleep` in steps.
- Assertions only in `@Then` steps (`org.junit.jupiter.api.Assertions`), with a helpful failure message.
- One step text = one definition, in one class (otherwise `AmbiguousStepDefinitionsException`).
- Use parameters (`{string}`, `{int}`, a `DataTable`) instead of one method per value.

---

## Part C - Integrate and Reflect (slot 6, ~30 min)

1. **Full run:** `mvn test -Dheadless=true` (all scenarios green) and, if Firefox is installed, `mvn test -Dbrowser=firefox -Dheadless=true`.
2. **Definition-of-Done test:** `mvn test -Dtest=FeatureStyleTest` must be **green**.
3. **Week synthesis check:** `grep -rn "Thread.sleep" src` returns nothing; `grep -rn "By\." src/test` returns nothing.
4. Complete `README_PROJECT.md` (how to run, structure, features and scenario counts, both names).
5. **Retrospective:** together, fill `docs/RETROSPECTIVE.md` (what went well, what was hard, what pairing changed, what you learned about BDD, top three actions for Friday).
6. Final commit by the slot-6 driver and push.

---

## Stretch Goals (optional)

1. **Checkout feature:** add a checkout story (new `CheckoutPage` objects, plus a feature with at least three scenarios).
2. **Logout:** a `HeaderComponent`/menu page object and a logout scenario.
3. **Doc string:** add a scenario step with a `"""` doc string and a step definition that reads it.
4. **Living documentation:** run with `-Dcucumber.plugin=pretty,html:target/cucumber.html` and open the report; list in your retrospective what a non-programmer can learn from it.
5. **Three-amigos sanity pass:** swap partners with another pair for 15 minutes and review each other's features against the navigator checklist.

---

## Definition of Done

- [ ] `docs/THREE_AMIGOS.md` complete: three INVEST stories, acceptance criteria, example mapping with open questions.
- [ ] At least **3 feature files**, **12 scenarios**, every feature with an *As a / I want / so that* header.
- [ ] At least one **data table** and at least one `And`/`But` step.
- [ ] No UI mechanics in Gherkin; no `Background`, `Scenario Outline`, `Rule`, `Examples` or tags.
- [ ] Step classes use **only page objects** (no `By`, `findElement`, waits or sleeps) and assertions live only in `@Then`.
- [ ] `mvn test -Dheadless=true` passes; `mvn test -Dtest=FeatureStyleTest` is green.
- [ ] Git history shows **both partners** as authors, alternating at the 30-minute swaps; `docs/PAIR_LOG.md` swap log complete.
- [ ] `docs/RETROSPECTIVE.md` complete and `README_PROJECT.md` updated.
- [ ] One shared repository/branch submitted.

## Grading Rubric (100 points, pair grade, adjusted by the swap log)

| Area | Points | Full marks looks like |
|---|---|---|
| Three Amigos artefacts | 15 | Real roles and benefits, testable criteria with no UI words, concrete examples, genuine open questions |
| Feature files | 25 | 12+ scenarios, business language, consistent wording, data table, And/But used well, story headers |
| Step definitions | 20 | Page objects only, parameters, assertions only in Then, no ambiguity, reuse across scenarios |
| It runs | 15 | Full suite green in Chrome and headless; automated style test green |
| Pairing process | 15 | Swaps on time, alternating commit authors, honest navigator notes in the log |
| Retrospective and README | 10 | Specific, reflective, links back to Monday-Wednesday, actionable next steps |

Individual adjustment: if the swap log or commit history shows one person drove much less than half of the time, the instructor may adjust individual grades.

## Hints (open only if stuck)

<details>
<summary>UndefinedStepException with a snippet printed in the console</summary>
Cucumber could not find a step definition matching the exact step text. Copy the suggested snippet from the console into the right step class, then adjust the method name and body. Check quotes: <code>{string}</code> needs quoted text in the feature.
</details>

<details>
<summary>AmbiguousStepDefinitionsException</summary>
Two step methods match the same text (often a duplicated "the shopper is logged in" in two classes). Keep one definition, in <code>CommonSteps</code>.
</details>

<details>
<summary>My step "the cart count shows 1" times out</summary>
<code>InventoryPage</code> waits for the inventory URL. If the shopper is already on the cart page, create the page object that matches that page (or check the count before opening the cart).
</details>

<details>
<summary>How do I assert sort order?</summary>
Read the list from the page object, copy it, sort the copy (<code>Collections.sort</code> or <code>reverseOrder()</code>) and <code>assertEquals(sortedCopy, original)</code>.
</details>

<details>
<summary>The data table step is not found</summary>
The step text in the feature must match the annotation exactly and must <b>not</b> end with a colon; the table goes on the lines below. The method takes a <code>DataTable</code> parameter; <code>table.asList()</code> returns a one-column table as <code>List&lt;String&gt;</code>.
</details>

<details>
<summary>Empty username/password in a scenario</summary>
<code>{string}</code> matches an empty quoted value, so <code>with username "" and password "secret_sauce"</code> is allowed and reuses the existing step.
</details>

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| Nothing runs / "No tests found" | Runner glue package wrong, or feature files not under `src/test/resources/features` |
| Scenario passes alone, fails in the full run | A step assumes the previous scenario's state. Every scenario starts with its own `Given`. |
| Several browser windows stay open | A scenario failed mid-way; leftovers close at the next scenario's start. Do not add manual `quit()` calls everywhere. |
| `FeatureStyleTest` reports UI words | A step contains words like click or button; rewrite it as user intent ("the shopper adds ... to the cart"). |
| Merge conflict in a feature file | You both edited the same file in different slots; commit at every swap and pull before you start typing. |

## Submission

1. Push your shared branch and submit the repository link (include both names in `README_PROJECT.md`).
2. Include a screenshot of the full `mvn test` result and of the green `FeatureStyleTest`.
3. `docs/PAIR_LOG.md` and `docs/RETROSPECTIVE.md` are part of the deliverable.

## Project 2 Milestone Checkpoint (Day 4)

- Three Amigos notes with INVEST stories and example mapping: done
- Login, sort and cart features (12+ scenarios): done
- Step definitions on top of the Page Object layer, PicoContainer sharing: done
- Automated BDD style rules green: done
- Pair log and retrospective: done

**Tomorrow (Friday)** you extend the BDD layer with `Background`, `Scenario Outline`, hooks, tags, Maven profiles and a Cucumber report, and complete the Project 2 BDD layer.

---

*Instructor material:* the reference implementation, a filled-in Three Amigos document and marking notes are in `solution/` (not distributed to trainees).
