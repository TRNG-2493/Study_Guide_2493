# Lab 3 (Wednesday): Actions, Alerts, Windows, and Converting Project 2 to Page Objects

**Week 6 · Day 3 · Advanced Selenium: Actions, Windows & POM · Mode A (Code Lab, individual)**
**Estimated time:** 3 hours (Part 1: ~60 min, Part 2: ~75 min, Parts 3-4: ~35 min, wrap-up: ~10 min)
**Project lane:** Project 2 - Test Automation Framework (Milestone 3: Page Object layer)

---

## The Scenario

Your Project 2 suite now has five tests, and they are **stable** (Tuesday) but **hard to maintain**. Open `tests/ScriptStyleTests.java` and count how many times `By.id("user-name")` and the login steps appear. If SauceDemo renames one button, five tests break at once. The QA lead has asked for two things:

1. **Skills first:** prove you can handle the awkward browser features real apps use: hover menus, JavaScript dialogs, new windows and nested frames.
2. **Refactor:** convert the five script-style tests to the **Page Object Model**, put locators in exactly one class per page, and try the **Page Factory** variant on the login page.

## Learning Objectives

By the end of this lab you will be able to:

- Chain mouse and keyboard input with the **Actions** API and always finish with `perform()`.
- Handle `alert`, `confirm` and `prompt` dialogs (and read their text *before* closing them).
- Switch safely between windows/tabs (snapshot, act, wait, switch) and between frames.
- Design a `BasePage` and page objects whose methods describe user intent and return the next page.
- Keep assertions out of pages and locators out of tests.
- Write the same page in **Page Factory** style and explain its trade-offs (proxies do not wait).

## Prerequisites and Source Material

| Need | Where |
|---|---|
| Actions: hover, chords, drag, scroll | `written/3-wednesday/actions-api.md` |
| Alerts: accept, dismiss, prompt | `written/3-wednesday/alerts.md` |
| Windows, tabs, frames | `written/3-wednesday/window-handling.md` |
| POM rules and Page Factory | `written/3-wednesday/page-object-model-and-page-factory.md` |
| Worked examples (same pages) | `demos/3-wednesday/` (Instructor Guide and `code/demo_advanced_selenium_actions_windows_pom.java`) |
| Your framework so far | Monday and Tuesday work (`DriverFactory`, `ScreenshotUtil`, `WaitUtils`, `DropdownUtils`) |

**Practice sites:** <https://the-internet.herokuapp.com> (`hovers`, `javascript_alerts`, `windows`, `nested_frames`) and <https://www.saucedemo.com> (`standard_user`, `locked_out_user`, password `secret_sauce`).

---

## Getting Started

**Option A (recommended):** continue in your `qea-framework` repo. Copy the new files from `starter_code/` into it: `AlertUtils.java`, `WindowUtils.java`, `InteractionsLab.java`, the `pages/` folder, and the `tests/` folder.

**Option B (if Tuesday is incomplete):** copy the entire `starter_code/` folder as a fresh project. It contains **working** Monday and Tuesday classes, so today's tasks are fully doable.

Run `mvn -q compile` to confirm it builds, then follow the TODOs:

```
src/main/java/com/revature/qea/
├── utils/
│   ├── WaitUtils.java, DropdownUtils.java, Check.java, ...   (given - Tuesday)
│   ├── AlertUtils.java            (TODO - Task 1.1)
│   └── WindowUtils.java           (TODO - Task 1.2)
├── flows/InteractionsLab.java     (TODO - Tasks 1.3-1.7)
├── pages/
│   ├── BasePage.java              (TODO - Task 2.1)
│   ├── LoginPage.java             (TODO - Task 2.2)
│   ├── InventoryPage.java         (TODO - Task 2.3)
│   ├── CartPage.java              (TODO - Task 2.4)
│   └── PfLoginPage.java           (TODO - Task 3.1, Page Factory)
└── tests/
    ├── ScriptStyleTests.java      (given - the "before"; do not edit)
    └── PomTests.java              (TODO - Task 4.1, the "after")
```

> **Run order:** first run `ScriptStyleTests` (it passes today), so you have a reference output of PASS lines. Your `PomTests` must reproduce the same lines (plus T6).

---

## Part 1 - Actions, Alerts, Windows and Frames (~60 min)

### Ground rules
- All waiting goes through `WaitUtils` / `AlertUtils` / `WindowUtils`. No sleeps, no implicit wait.
- Every `Actions` chain ends with `perform()`.
- One method per task, each with its own driver, so one failure cannot hide another.

### Task 1.1 - `AlertUtils` (~10 min)
Implement the helper in `utils/AlertUtils.java`: wait with `alertIsPresent()`, **read the text before closing**, and make `isPresent()` non-waiting (`switchTo().alert()` and catch `NoAlertPresentException`). `noAlertAppears()` returns `true` when a wait **times out**, a rare case where the timeout is the success path.

### Task 1.2 - `WindowUtils` (~10 min)
Implement `switchToNewWindowAfter(Runnable)` with the four-step snapshot pattern (remember handles, run the action, wait for a new handle, switch to the one that was not in the snapshot), plus `closeCurrentAndSwitchTo`, `switchToWindowByTitleContains`, `switchToFrame` (wait for the frame) and `backToMainPage`.

### Task 1.3 - Hover (`/hovers`) (~8 min)
The caption is hidden until the pointer is over the figure. Verify it is hidden before, hover with `Actions.moveToElement(...).perform()`, then verify the caption text contains `user1`. Use a **scoped** lookup from the figure element.

### Task 1.4 - Alerts (`/javascript_alerts`) (~8 min)
Handle one of each: accept an alert, dismiss a confirm, answer a prompt with `Revature QEA`. After each, verify the page's `result` text (for example `You clicked: Cancel`). Finally verify no alert is left open.

### Task 1.5 - New window (`/windows`) (~8 min)
Click the link that opens a new window, verify its title/heading, close it, switch back, and verify you are on the original page with exactly one window handle.

### Task 1.6 - Keyboard chord (~5 min)
On SauceDemo's username field, build a **single** Actions chain: click, `keyDown(SHIFT)`, type `standard`, `keyUp(SHIFT)`. Verify the field value is `STANDARD`.

### Task 1.7 - Nested frames (`/nested_frames`) (~8 min)
Switch into `frame-top` then `frame-middle`, verify the text is `MIDDLE`, and switch back to the main page. Verify you are back on the document that owns the frames.

Run it: `mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.InteractionsLab -Dheadless=true`. Every line must be `PASS`.

---

## Part 2 - Project 2 Milestone: Build the Page Objects (~75 min)

**Milestone 3:** the framework gets a `pages` layer. Read the Javadoc in each page for locators and rules.

### Task 2.1 - `BasePage` (~15 min)
Holds the `WebDriver` and a `WaitUtils` (reuse Tuesday's class - no new `WebDriverWait`). Provide `click`, `type`, `textOf`, `isDisplayed` (non-waiting, uses `findElements`), `textsOf` (non-waiting; empty list is valid) and `waitForUrlContaining`.

### Task 2.2 - `LoginPage` (~15 min)
Private `By` locators; `open()`, `enterUsername`, `enterPassword` (fluent: return `this`), `loginAs` (returns `InventoryPage`), `loginExpectingFailure` (returns `this`), `getErrorMessage`, `isErrorDisplayed`.

### Task 2.3 - `InventoryPage` (~25 min)
The constructor **waits** for the URL to contain `inventory`. Implement title, names, prices (as doubles), `sortBy` (using `DropdownUtils`), `addToCart`/`removeFromCart` (id built from the product name: lower-case, spaces to dashes), `getCartCount` (the badge is **absent**, not `0`, when empty) and `openCart` (returns `CartPage`). Apply Tuesday's lesson: `addToCart` must not return until the add is *done*, so wait for the matching `remove-...` button to appear.

### Task 2.4 - `CartPage` (~20 min)
The constructor waits for `cart` in the URL. Implement names, count, `removeItem` (then **wait** until the row count drops) and `continueShopping`.

> **The five page-object rules (graded):** (1) locators are private and live only in the page; (2) methods are named for user intent; (3) **no assertions** inside pages; (4) navigation methods return the next page object; (5) tests never touch `By`.

---

## Part 3 - Page Factory (~15 min)

### Task 3.1 - `PfLoginPage`
Rewrite the login page **with `@FindBy`**: four `WebElement` fields (not `final`), `PageFactory.initElements(driver, this)` in the constructor, and explicit waits (`ExpectedConditions.visibilityOf(element)`) around every use, because the proxies do **not** wait. Provide `open()`, `loginExpectingFailure(...)` and `getErrorMessage()`.

Then write three sentences in `README_PROJECT.md` comparing it with `LoginPage`: what got shorter, what got riskier, and which one you would keep in a team framework and why.

---

## Part 4 - Convert the Tests (~20 min)

### Task 4.1 - `PomTests`
Implement `t1`-`t6` in `tests/PomTests.java` using only page objects. **Strict rules for this file:** no `By`, no `driver.findElement(s)`, no waits, no sleeps. Use the same `Check` labels as `ScriptStyleTests`. Then run both classes and compare the PASS lines side by side.

### Task 4.2 - Prove the benefit
Pretend SauceDemo renamed the login button id to `login-btn`. Make that change in **one** place in your `LoginPage` and note how many files you edited. Then count how many places you would have changed in `ScriptStyleTests`. Put both numbers in `README_PROJECT.md`. Revert the change afterwards.

### Task 4.3 - Update documentation and commit
Add today's run commands and a short "Page Object rules" section to `README_PROJECT.md`. Commit with a meaningful message.

---

## Stretch Goals (optional)

1. **Header component:** extract the cart link and badge into a `HeaderComponent` class used by `InventoryPage` and `CartPage` (preview of Friday's component idea).
2. **Drag and drop:** automate `https://jqueryui.com/droppable/` (it lives **inside an iframe**) with `Actions.dragAndDrop` and verify the target text becomes `Dropped!`.
3. **Fluent test:** write a T7 that logs in, adds three products, sorts by name Z to A, opens the cart and verifies the names, all in one fluent chain.
4. **Tab handling:** use `driver.switchTo().newWindow(WindowType.TAB)` to open SauceDemo in a second tab and verify two handles exist.

---

## Definition of Done

- [ ] `mvn -q compile` succeeds.
- [ ] `InteractionsLab` prints only `PASS` for tasks 1.3-1.7; `AlertUtils` reads the text before closing; `WindowUtils` never indexes handles by position.
- [ ] `BasePage`, `LoginPage`, `InventoryPage`, `CartPage` implemented; all locators private; **no assertions in pages**.
- [ ] `PfLoginPage` uses `@FindBy`, non-final fields, `initElements`, and explicit waits.
- [ ] `PomTests` contains **no** `By` and no `findElement(s)`, and its T1-T5 output matches `ScriptStyleTests` line for line.
- [ ] `grep -rn "Thread.sleep" src` and `grep -rn "implicitlyWait" src` return nothing.
- [ ] Task 4.2 numbers and the Page Factory comparison are in `README_PROJECT.md`; work is committed.

## Grading Rubric (100 points)

| Area | Points | Full marks looks like |
|---|---|---|
| `AlertUtils` + `WindowUtils` | 15 | Text read before closing, snapshot pattern, frame wait |
| `InteractionsLab` tasks | 20 | All five tasks PASS, scoped hover lookup, single chord chain |
| `BasePage` + page objects | 25 | Intent-named methods, private locators, return types chain correctly, no assertions |
| Page Factory page | 10 | `@FindBy`, non-final, `initElements`, explicit waits |
| `PomTests` conversion | 15 | No `By` in tests, same checks, T6 included |
| Maintainability evidence (Task 4.2) | 5 | Correct counts; one-place change demonstrated |
| README, commits, code quality | 10 | Rules documented, comparison paragraph, meaningful commits |

## Hints (open only if stuck)

<details>
<summary>The caption never becomes visible after the hover</summary>
Make sure the chain ends with <code>perform()</code> and that you hover the <b>figure</b> element, not the image inside a different figure. In headless mode a window size is set by your <code>DriverFactory</code>, so layout is stable.
</details>

<details>
<summary><code>NoAlertPresentException</code> or <code>UnexpectedAlertPresentException</code></summary>
Wait with <code>alertIsPresent()</code> before touching the alert, and always close the alert before any other command. While an alert is open, every other driver command fails.
</details>

<details>
<summary>After closing the new window every command fails with NoSuchWindowException</summary>
Closing a window does not move focus. Switch back to the original handle explicitly (<code>closeCurrentAndSwitchTo</code>).
</details>

<details>
<summary>InventoryPage constructor times out after a failed login</summary>
The constructor waits for the inventory URL. That is intended: only create <code>InventoryPage</code> on the success path. On the failure path stay on <code>LoginPage</code>.
</details>

<details>
<summary>Page Factory: <code>NullPointerException</code> on a field</summary>
You forgot <code>PageFactory.initElements(driver, this)</code>, or the field is <code>final</code>.
</details>

<details>
<summary>T4 reads the wrong item count</summary>
The DOM updates after the click. <code>removeItem</code> must wait until the number of rows has dropped before returning.
</details>

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `NoSuchWindowException` | Focus is on a closed window; switch to a live handle. |
| Hover test flaky | The pointer was not moved onto the figure; ensure you use the element from `allVisible` and `perform()`. |
| Frame lookup fails | You are still inside another frame; call `backToMainPage()` first or switch frame by frame. |
| `StaleElementReferenceException` in a page | A `WebElement` stored in a field; store `By` instead (except Page Factory proxies, which re-locate). |
| `PomTests` and `ScriptStyleTests` differ | Check labels and expected values; the point of the refactor is *no behaviour change*. |

## Submission

1. Commit to your `qea-framework` repository (at least four commits: utils, interactions lab, page objects, tests/README).
2. Submit the repository link.
3. Include a terminal screenshot showing the PASS lines of `ScriptStyleTests` and `PomTests` side by side.

## Reflection (answer in `README_PROJECT.md`, 3-5 sentences each)

1. Which page-object rule did you break first while converting, and what made you notice?
2. Why do navigation methods return page objects, and what does that do for test readability?
3. When would you choose Page Factory over plain POM, and when not?

## Project 2 Milestone Checkpoint (Day 3)

- `AlertUtils` and `WindowUtils` in the utility layer: done
- `BasePage` + `LoginPage`, `InventoryPage`, `CartPage`: done
- Page Factory login variant: done
- Five tests converted to Page Objects, no locators in tests: done
- Maintainability evidence recorded: done

**Tomorrow (Thursday)** you move to BDD: in a **pair**, you will write user stories and Gherkin features for Project 2 and wire step definitions to the page objects you built today.

---

*Instructor material:* the reference implementation is in `solution/` (not distributed to trainees).
