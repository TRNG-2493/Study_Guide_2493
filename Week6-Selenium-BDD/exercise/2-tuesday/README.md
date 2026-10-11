# Lab 2 (Tuesday): Stabilise Flaky Tests with Waits, and Grow the Project 2 Framework

**Week 6 · Day 2 · Advanced Selenium · Mode A (Code Lab, individual)**
**Estimated time:** 2.5-3 hours (Part 1: ~90 min, Part 2: ~60 min, wrap-up: ~20 min)
**Project lane:** Project 2 - Test Automation Framework (Milestone 2: stable waits layer)

---

## The Scenario

Your team lead opens the CI dashboard: the same tests pass in the morning and fail in the afternoon, and nobody changed the code. A colleague wrote four quick scenarios ("they passed when I ran them once") and one of them is already in your framework. Your job today is to find out **why they are flaky**, fix them properly, and prove the fix with numbers. Then you promote the fix into the Project 2 framework as reusable utilities: `WaitUtils` and `DropdownUtils`.

> **A test that passed once is not a stable test. A test is stable when it passes 10 out of 10 runs.**

## Learning Objectives

By the end of this lab you will be able to:

- Diagnose a flaky test from its exception (or wrong value) and name the root cause.
- Choose between presence, visibility, clickability, invisibility, count and URL conditions.
- Replace every `Thread.sleep` with an explicit wait, and explain why implicit and explicit waits must not be mixed.
- Build a reusable `WaitUtils` and `DropdownUtils` that take a `By` (not a stored `WebElement`).
- Use the `Select` class on a real dropdown and verify sorted data.
- Measure stability with a repeat-run harness instead of guessing.

## Prerequisites and Source Material

Everything is from today's reading and demo (and Monday's, which this lab builds on).

| Need | Where |
|---|---|
| Sleep vs implicit vs explicit vs fluent | `written/2-tuesday/waiting-strategies.md` |
| Reusable wait helper | `waiting-strategies.md`, section 9; `demos/2-tuesday` Stage 6 |
| Click, type, clear, checkbox, stale/intercepted exceptions | `written/2-tuesday/element-interactions.md` |
| `Select`, options, sort verification | `written/2-tuesday/select-elements.md`; `demos/2-tuesday` Stage 8 |
| Worked example on the same pages | `demos/2-tuesday/` (Instructor Guide and `code/demo_advanced_selenium.java`) |
| Monday framework you are extending | Your Monday `qea-framework` repo |

**Practice sites:** <https://the-internet.herokuapp.com> (dynamic loading, dynamic controls) and <https://www.saucedemo.com> (`standard_user` / `secret_sauce`).

---

## Getting Started

**Option A (recommended): keep working in your Monday repo.** Copy these new files from `starter_code/` into your `qea-framework` project: `WaitUtils.java`, `DropdownUtils.java`, `RepeatRunner.java`, `ThrowingRunnable.java`, `FlakyScenarios.java`, `FlakinessRun.java`, `SortFlow.java`, `FLAKINESS_REPORT.md`, and replace `Check.java` (it now counts failures).

**Option B (if Monday is incomplete):** copy the entire `starter_code/` folder as a fresh project. It contains a **working Monday framework** (`DriverFactory`, `ScreenshotUtil`, `LoginSearchFlow`) plus today's TODOs, so you can still do all of today's tasks.

Verify with `mvn -q compile`. Then read the `TODO` and `// BUG?` comments:

```
src/main/java/com/revature/qea/
├── drivers/DriverFactory.java      (given - Monday)
├── utils/
│   ├── Check.java                  (given - now counts failures)
│   ├── RepeatRunner.java           (given - runs a flow N times, prints pass rate)
│   ├── ThrowingRunnable.java       (given)
│   ├── ScreenshotUtil.java         (given - Monday)
│   ├── WaitUtils.java              (TODO - Task 1.2)
│   └── DropdownUtils.java          (TODO - Task 2.2)
└── flows/
    ├── FlakinessRun.java           (given - the harness)
    ├── FlakyScenarios.java         (TODO - Part 1: four flaky scenarios to fix)
    ├── LoginSearchFlow.java        (TODO - Task 2.1: remove every pause())
    └── SortFlow.java               (TODO - Task 2.3)
FLAKINESS_REPORT.md                 (fill in - Task 1.5)
```

---

## Part 1 - Stabilise the Flaky Scenarios (individual, ~90 min)

### Ground rules

- **No `Thread.sleep`**, no `pause(...)`, **no implicit wait** (`implicitlyWait`) - not even "temporarily".
- Do not change what a scenario *checks*; change *how it waits*.
- `new WebDriverWait(...)` may appear **only** inside `WaitUtils` (and `DropdownUtils` if you use it there).
- Never catch and swallow a `TimeoutException`.

### Task 1.1 - Baseline: measure the flakiness first (~10 min)

Before changing anything, run the harness so you have evidence:

```
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.FlakinessRun -Dtimes=5 -Dheadless=true -Donly=1
```

Run it for scenarios `1` to `4` (change `-Donly`; `5` and `6` come later). Write the `>>> ... x/5 passed` lines into the **Baseline** column of `FLAKINESS_REPORT.md`. Also note, for every scenario, **the exception name or wrong value** you saw: that is your clue.

> `S4` will often pass at baseline. Record it honestly. "It passed" is a data point, not a proof.

### Task 1.2 - Implement `WaitUtils` (~25 min)

Implement every method in `utils/WaitUtils.java` (the Javadoc says what each must do):

| Method | Condition to use |
|---|---|
| `visible(By)` | element present **and** displayed |
| `clickable(By)` | displayed **and** enabled |
| `click(By)` / `type(By, text)` / `textOf(By)` | built on the two above (`type` must `clear()` first) |
| `disappears(By)` | invisibility of the locator |
| `allVisible(By)` | all matches visible |
| `countToBe(By, n)` | number of matches equals `n` |
| `waitForUrlContains(fragment)` | URL contains fragment |
| `setCheckbox(By, boolean)` | present, then click only if the state differs |

Default timeout: 10 seconds, with a second constructor taking a `Duration`.

### Task 1.3 - Fix the four scenarios (~35 min)

For each scenario in `FlakyScenarios.java`:

1. Predict (in a comment) which line fails and with which exception.
2. Fix it using `WaitUtils` (everything: opening the page is fine with `driver.get`, but every click, type and read goes through a wait).
3. Run just that scenario: `-Donly=<n> -Dtimes=1`.

Specific traps (one per scenario, on purpose):

- **S1** - the heading *exists* but is hidden. What does `getText()` return? Is it an exception?
- **S2** - the heading does *not exist* yet. Same check, different failure. Is the wait the same?
- **S3** - three different problems in one scenario: a message that appears later, a **stale** reference to an element that left the page, and a **disabled** input. Which wait solves each?
- **S4** - looks fine. Make it stable anyway.

### Task 1.4 - Prove it: 10 out of 10 (~10 min)

```
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.FlakinessRun -Dtimes=10 -Dheadless=true -Donly=3
```

Repeat for scenarios 1-4. Record the **After** column. Every scenario must reach `10/10`. If one does not, read the failing exception again; do not "fix" it with a bigger timeout.

### Task 1.5 - Diagnose in writing (~10 min)

Complete the root-cause table and the four decision questions in `FLAKINESS_REPORT.md`. One sentence per cell; name the exact exception class where there is one.

---

## Part 2 - Project 2 Milestone: The Waits Layer (individual, ~60 min)

**Milestone 2:** By the end of today the framework has no sleeps, a shared `WaitUtils`, a `DropdownUtils`, and every flow has a measured stability score.

### Task 2.1 - Refactor Monday's `LoginSearchFlow` (~15 min)
Replace **every** `pause(...)` with a wait from `WaitUtils`, route all typing/clicking/reading through `WaitUtils` where timing matters, and delete the `pause` helper. All `Check` labels and expectations must stay identical.

**Acceptance test:** search the whole project for the text `Thread.sleep` - **zero hits** (use your IDE's "Find in files" or `grep -rn "Thread.sleep" src`).

### Task 2.2 - Implement `DropdownUtils` (~15 min)
Implement `chooseByText`, `chooseByValue`, `selectedText` and `optionTexts` in `utils/DropdownUtils.java`. Wait for the `<select>` to be visible first, then wrap it in `Select`.

### Task 2.3 - Build `SortFlow` (~20 min)
In `flows/SortFlow.java` follow the sub-tasks `2.3a`-`2.3f`: log in, verify the four sort options and the default, sort by price ascending and descending and name Z to A, and **verify the order programmatically** (compare against a sorted copy; do not hard-code the whole list). Take a screenshot at the end.

> Hint: after you choose a sort option the list re-renders. Re-read the elements **after** choosing; a list you read before is stale.

### Task 2.4 - Measure and document (~10 min)
Run scenarios 5 and 6 (`-Donly=5`, `-Donly=6`) five times each, then ten. Fill the S5/S6 rows. Finally update `README_PROJECT.md`: the new classes, the new run commands, and a short **"Stability rules"** section (no sleeps, no implicit waits, helpers take a `By`, a flow is "stable" at 10/10). Commit with a meaningful message.

---

## Stretch Goals (optional)

1. **Fluent wait:** add `WaitUtils.textToBe(By, String)` implemented with `FluentWait` (polling every 250 ms, ignoring `NoSuchElementException`, with a helpful `withMessage`) and use it in S1.
2. **Friendly failures:** make `visible()` save a screenshot (via your Monday `ScreenshotUtil`) on `TimeoutException` **and rethrow**.
3. **Cart flow:** open `https://www.saucedemo.com`, log in, and write a short flow that adds an item to the cart and opens the cart using only `WaitUtils`.
4. **Timeouts on purpose:** create `new WaitUtils(driver, Duration.ofSeconds(2))` and wait for an element that never appears (`By.id("never-appears")`). Paste the first line of the `TimeoutException` message into your report and explain what each part tells you.

---

## Definition of Done

- [ ] `mvn -q compile` succeeds.
- [ ] `WaitUtils` and `DropdownUtils` implement every method; neither contains `Thread.sleep` or an implicit wait.
- [ ] S1-S4 each pass **10/10** with `FlakinessRun`, and the baseline numbers are recorded.
- [ ] `LoginSearchFlow` has zero `pause`/`Thread.sleep`, passes 10/10 and keeps its original checks.
- [ ] `SortFlow` verifies options, default, ascending/descending price and Z-A name order, and passes 10/10.
- [ ] `grep -rn "Thread.sleep" src` returns nothing; `implicitlyWait` appears nowhere.
- [ ] `FLAKINESS_REPORT.md` has every table row and all four questions answered.
- [ ] `README_PROJECT.md` is updated and the work is committed.

## Grading Rubric (100 points)

| Area | Points | Full marks looks like |
|---|---|---|
| Scenario fixes (S1-S4) | 25 | Right wait per problem; no sleeps; 10/10 |
| `WaitUtils` design | 15 | Takes `By`, one timeout owner, `clear()` in `type`, nothing swallowed |
| `DropdownUtils` + `SortFlow` | 20 | Waits first, programmatic sort checks, re-read after choose |
| Refactor of `LoginSearchFlow` | 10 | Zero pauses, checks unchanged |
| Evidence (baseline and after numbers) | 10 | Honest baseline, 10/10 after, per scenario |
| Diagnosis quality | 10 | Correct exception names and root causes; reasoning on questions |
| README, commits, code quality | 10 | Clear commands, stability rules, meaningful commits |

## Hints (open only if stuck)

<details>
<summary>S1 never fails with an exception, only with a wrong value</summary>
That is the point. <code>getText()</code> on a hidden element returns an empty string. Wait for <b>visibility</b>, not just presence.
</details>

<details>
<summary>S3: StaleElementReferenceException</summary>
You stored a <code>WebElement</code> and the page then removed it. Do not keep the reference: express the end state as a <b>count</b> (<code>countToBe(By.id("checkbox"), 0)</code>) and re-find by locator.
</details>

<details>
<summary>S3: ElementNotInteractableException on the text box</summary>
The input is <i>disabled</i> until the AJAX call finishes. Which expected condition checks "displayed and enabled"?
</details>

<details>
<summary><code>invisibilityOfElementLocated</code> returns immediately</summary>
It returns true if the element does not exist at that instant. Follow it with a wait for the thing you actually care about (for example the message becoming visible), as in the demo.
</details>

<details>
<summary>My dropdown helper throws StaleElementReferenceException</summary>
Do not keep a <code>Select</code> or <code>WebElement</code> in a field. Locate the element and build the <code>Select</code> inside each method.
</details>

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `TimeoutException` after 10 s | Wrong locator or wrong condition; read the message: it names the locator and the condition. A longer timeout will not fix it. |
| S2 passes but takes 10 s every time | You wait with a sleep-like loop or the wrong condition; the explicit wait should return as soon as the text is visible (~5 s). |
| Everything is slower than yesterday | You mixed an implicit wait with explicit ones. Remove `implicitlyWait`. |
| `FlakinessRun` prints `ERROR NoSuchElementException` | An unfixed scenario; that is the baseline behaviour, not a harness bug. |

## Submission

1. Commit to your `qea-framework` repository (at least three commits: WaitUtils, scenario fixes, SortFlow/README).
2. Submit the repository link plus `FLAKINESS_REPORT.md`.
3. Include a screenshot of the `FlakinessRun` output showing the 10/10 lines.

## Reflection (answer at the end of `FLAKINESS_REPORT.md`, 3-5 sentences each)

1. Which scenario surprised you most, and why?
2. When is a *longer timeout* the wrong answer to a flaky test?
3. What would break in a month if the team added `Thread.sleep` "just this once"?

## Project 2 Milestone Checkpoint (Day 2)

- `WaitUtils` (explicit waits, one timeout owner): done
- `DropdownUtils` on top of `Select`: done
- Monday's flow refactored to zero sleeps: done
- `SortFlow` added and measured: done
- Stability evidence (10/10) recorded: done

**Tomorrow (Wednesday)** you will turn these flows into **Page Objects** (`BasePage`, `LoginPage`, `InventoryPage`, `CartPage`) that reuse `WaitUtils`.

---

*Instructor material:* the reference implementation, including root-cause answers (`solution/FLAKINESS_REPORT.md`), is in `solution/` (not distributed to trainees).
