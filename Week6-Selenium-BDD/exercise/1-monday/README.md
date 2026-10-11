# Lab 1 (Monday): Automate a Login and Search Flow, and Kick Off Project 2

**Week 6 · Day 1 · Selenium WebDriver · Mode A (Code Lab, individual)**
**Estimated time:** 2.5 hours (Part 1: ~75 min, Part 2: ~60 min, wrap-up: ~15 min)
**Project lane:** Project 2 - Test Automation Framework (Milestone 1: framework skeleton)

---

## The Scenario

Your team has just been handed a new product to test: the **Swag Labs** web shop at <https://www.saucedemo.com>. There is no automation yet. Today you do two things:

1. **Part 1 - Prove you can drive a browser.** Automate a real user journey (log in, find a product, verify it, check the negative path) using the WebDriver skills from today's reading and demo.
2. **Part 2 - Start Project 2.** Turn your throwaway-style code into the first layer of a **reusable test automation framework**: a configurable `DriverFactory`, a `ScreenshotUtil`, a smoke check and a project README. Everything you build this week sits on top of this skeleton.

## Learning Objectives

By the end of this lab you will be able to:

- Create and configure a WebDriver for Chrome, Firefox or Edge (including headless) behind a single factory.
- Choose between `id`, `name`, `className`, `cssSelector` and `xpath` locators and justify the choice.
- Use `findElement` vs `findElements` correctly, including **scoped** searches from a parent element.
- Navigate with `get`, `navigate().back()/forward()/refresh()` and read `getTitle()` / `getCurrentUrl()`.
- Capture page and element screenshots into a predictable folder.
- Structure a Maven project so it can grow into a framework.

## Prerequisites and Source Material

Everything you need is in today's material; nothing from later in the week is required.

| Need | Where |
|---|---|
| Architecture, driver lifecycle | `written/1-monday/selenium-webdriver-architecture.md` |
| `DriverFactory`, headless | `written/1-monday/driver-configuration.md`, `browser-options.md` |
| Locators | `written/1-monday/locator-strategies.md` |
| `findElement(s)` | `written/1-monday/find-methods.md` |
| Navigation | `written/1-monday/navigation-methods.md` |
| Screenshots | `written/1-monday/screenshots.md` |
| Worked example | `demos/1-monday/` (Instructor Guide and `code/demo_selenium_webdriver.java`) |

**Environment:** JDK 17+, Maven 3.9+, Chrome (Firefox or Edge optional), an IDE of your choice, internet access to saucedemo.com.

## Test Data (SauceDemo)

| Item | Value |
|---|---|
| URL | `https://www.saucedemo.com/` |
| Valid user | `standard_user` |
| Locked user | `locked_out_user` |
| Password (all users) | `secret_sauce` |
| Product used in the lab | `Sauce Labs Fleece Jacket` (expected price `$49.99`) |
| Expected product count | `6` |
| Locked-out message | `Epic sadface: Sorry, this user has been locked out.` |

---

## Getting Started

1. Copy the `starter_code/` folder to your own working location and name it `qea-framework` (this is your Project 2 repository; run `git init` in it).
2. Open it in your IDE as a Maven project and let it download dependencies.
3. Confirm it compiles: `mvn -q compile`.
4. Read the Javadoc and `TODO` comments in these files - they are your task list:

```
starter_code/
├── pom.xml                         (given: Selenium 4.25.0, exec plugin)
├── README_PROJECT.md               (blank template - you fill it in, Task 2.5)
└── src/main/java/com/revature/qea/
    ├── utils/Check.java            (given: tiny PASS/FAIL printer - no JUnit yet)
    ├── drivers/DriverFactory.java  (TODO - Task 2.1 / 2.2)
    ├── utils/ScreenshotUtil.java   (TODO - Task 2.3)
    └── flows/
        ├── LoginSearchFlow.java    (TODO - Part 1)
        └── SkeletonSmokeCheck.java (TODO - Task 2.4)
```

> **Why `Check` and `main()` instead of JUnit?** JUnit and Cucumber arrive later in the week. `Check.that(...)` / `Check.equal(...)` print `PASS`/`FAIL` lines so you can see results today without any test framework.

> **Suggested order:** do Task 2.1 (`DriverFactory`) first, because Part 1 depends on it.

---

## Part 1 - Automate a Login and Search Flow (individual, ~75 min)

Work in `flows/LoginSearchFlow.java`. Run it with:

```
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.LoginSearchFlow
```

(add `-Dheadless=true` or `-Dbrowser=firefox` once your factory supports them).

### Ground rules

- Create the browser **only** through `DriverFactory.createDriver()`; always `quit()` it in a `finally` block.
- Use **at least four different `By` strategies** across the lab.
- Waits are Tuesday's topic. You may use the single provided `pause(...)` helper where SauceDemo needs a moment, and nowhere else. No other `Thread.sleep`.
- Every check uses `Check.that(...)` / `Check.equal(...)` with a meaningful label.

### Task 1.1 - Open the site and check the title
Open `https://www.saucedemo.com/` and `Check.equal` that the page title is `Swag Labs`.

### Task 1.2 - Log in
Locate the username field, password field and Login button, type the credentials for `standard_user`, click, then `pause(...)` briefly. Verify:

- the URL contains `inventory`;
- the heading text (class `title`) is `Products`.

### Task 1.3 - Search the product list
There is no search box on this page, so "search" means **find a product by scanning the list**:

1. Collect the product cards with `findElements`.
2. Loop through the names to find `Sauce Labs Fleece Jacket`; record its position.
3. Read its price from **the same card** using a scoped lookup (`card.findElement(...)`, not a page-wide search).
4. Verify the price is `$49.99` and the total product count is `6`.

### Task 1.4 - Verify the detail page and navigate back
1. Click the product name; verify the URL contains `inventory-item`.
2. Read the name and price on the detail page and `Check.equal` them against the values from the list page.
3. Use `navigate().back()` and verify you are on the inventory page again.
4. Save a screenshot named `monday-search-pass` with `ScreenshotUtil`.

### Task 1.5 - The negative path
In `lockedOutUser()`:

1. Open the site and use `findElements` to verify that **no** error banner exists yet (size `0`).
2. Log in as `locked_out_user`.
3. Read the error text (`[data-test='error']`) and check it equals the locked-out message.
4. Save a screenshot named `monday-locked-out`.

> Tip: `findElement` throws when nothing matches; `findElements` returns an empty list. That is the whole trick behind "assert absent".

---

## Part 2 - Project 2 Kickoff: Framework Skeleton (individual, ~60 min)

**Milestone 1:** By the end of today your repository must have a working, configurable foundation that every later lab (waits, Page Objects, Cucumber) will build on.

### Task 2.1 - Create the Maven project
Verify `pom.xml` builds (`mvn -q compile`), then initialise git and make a first commit (`git init`, `git add .`, `git commit -m "Project 2: framework skeleton"`). Check that `.gitignore` excludes `target/`.

### Task 2.2 - Implement `DriverFactory`
In `drivers/DriverFactory.java` implement:

- `createDriver()` - reads system properties `browser` (default `chrome`) and `headless` (default `false`) and delegates to the next method.
- `createDriver(String browserName, boolean headless)`:
  - supports `chrome`, `firefox`, `edge` (case-insensitive);
  - Chrome headless uses `--headless=new` plus a fixed window size (e.g. 1920x1080); Firefox headless uses `-headless`;
  - when **not** headless, maximise the window;
  - throws `IllegalArgumentException` with a helpful message for a null or unknown browser name.

### Task 2.3 - Implement `ScreenshotUtil`
In `utils/ScreenshotUtil.java` implement:

- `capture(WebDriver, String name)` - saves a PNG to `target/screenshots/<safe-name>-<timestamp>.png`, creating the folder if needed, sanitising unsafe filename characters, and returning the saved `Path`;
- `capture(WebElement, String name)` - same, for a single element;
- `captureBytes(WebDriver)` - returns the raw bytes (used later for reports).

### Task 2.4 - The skeleton smoke check
In `flows/SkeletonSmokeCheck.java` open the site through `DriverFactory`, check the title, save a screenshot and quit. Then run it **three ways** and record what happened:

```
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck -Dheadless=true
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck -Dbrowser=firefox
```

(Skip the Firefox run if it is not installed, but note that you skipped it.)

### Task 2.5 - Document it
Fill in `README_PROJECT.md`: what the framework is, requirements, the exact run commands you verified, the project structure, and your name. A teammate must be able to run your project using only this file.

---

## Stretch Goals (optional)

1. **Edge support check:** run the smoke check with `-Dbrowser=edge` and note the result.
2. **Element screenshot:** take an element screenshot of the Fleece Jacket card on the list page.
3. **Locator comparison:** locate the Login button using four different strategies and write one sentence on which you would keep in a framework and why.
4. **Refactor:** extract a private `login(driver, user)` helper in `LoginSearchFlow` so both flows share it (a preview of tomorrow's utilities and Wednesday's Page Objects).

---

## Definition of Done

You are done when **all** of these are true:

- [ ] `mvn -q compile` succeeds with no errors.
- [ ] `LoginSearchFlow` runs end to end and prints only `PASS` lines (zero `FAIL`).
- [ ] At least four different `By` strategies are used and every browser is `quit()` in a `finally` block.
- [ ] The Fleece Jacket price was read via a **scoped** lookup from the product card.
- [ ] Both screenshots (`monday-search-pass`, `monday-locked-out`) exist under `target/screenshots/`.
- [ ] `DriverFactory` works for the default browser, with `-Dheadless=true`, and rejects an unknown browser with `IllegalArgumentException`.
- [ ] `SkeletonSmokeCheck` was run in at least two configurations and the results are recorded in the README.
- [ ] `README_PROJECT.md` is complete and the project has a first git commit.
- [ ] The only `Thread.sleep` in the project is inside `pause(...)` and is commented as temporary.

## Grading Rubric (100 points)

| Area | Points | What full marks looks like |
|---|---|---|
| Part 1 - correctness | 30 | All checks pass; correct data verified; negative path works |
| Part 1 - locator and find skills | 15 | 4+ strategies, scoped lookup, `findElements` used for "absent" |
| `DriverFactory` | 15 | 3 browsers, headless, properties, clear error for bad input |
| `ScreenshotUtil` | 10 | Folder created, safe/unique names, element and bytes variants |
| Smoke check + runs | 10 | Run in 2+ ways, results documented |
| Code quality | 10 | `finally`/`quit()`, no stray sleeps, clear labels, no duplication beyond `pause` |
| README and git | 10 | Another trainee could run it from the README; clean first commit |

## Hints (open only if stuck)

<details>
<summary>My Chrome headless run shows a tiny or wrong-sized page</summary>
Headless browsers have no window to maximise. Set an explicit window size on the options (see <code>browser-options.md</code>).
</details>

<details>
<summary><code>NoSuchElementException</code> right after login</summary>
The page needs a moment to render. Use the single <code>pause(...)</code> helper after clicking Login. Tomorrow you will replace it with a proper wait.
</details>

<details>
<summary>How do I get the price for one specific product?</summary>
Find the product cards (<code>inventory_item</code>), loop through them, and for the matching card call <code>card.findElement(...)</code> so the search is limited to that card (see <code>find-methods.md</code>).
</details>

<details>
<summary>My screenshot filename contains characters Windows rejects</summary>
Replace anything that is not a letter, digit, dash or underscore before building the file name.
</details>

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `SessionNotCreatedException` | Browser and driver mismatch. Selenium Manager normally fixes this; update your browser or check network/proxy access. |
| `exec:java` cannot find the main class | Run `mvn -q compile` first and check the package name in `-Dexec.mainClass`. |
| Browser window stays open after a failure | A `driver.quit()` is missing from a `finally` block. |
| Every check fails after login | Credentials typed into the wrong fields, or no pause after clicking Login. |

## Submission

1. Commit your work to your `qea-framework` repository (git history should show at least two commits).
2. Submit the repository link (or a zip of the folder without `target/`) to your instructor.
3. Include a screenshot of your terminal showing the three `SkeletonSmokeCheck` runs.

## Reflection (answer in `README_PROJECT.md`, 3-5 sentences each)

1. Which locator strategy did you trust most today and why?
2. What would break first in your flow if the page were slower, and how will tomorrow's material help?
3. Why is it better to have a `DriverFactory` than calling `new ChromeDriver()` in every test?

## Project 2 Milestone Checkpoint (Day 1)

- Repository with Maven structure: done
- Configurable `DriverFactory` (browser, headless): done
- `ScreenshotUtil`: done
- Smoke check proven in 2+ configurations: done
- Project README started: done

**Tomorrow (Tuesday)** you will add `WaitUtils` and stabilise flaky scenarios on this same repository.

---

*Instructor material:* the full reference implementation is in `solution/` (not distributed to trainees).
