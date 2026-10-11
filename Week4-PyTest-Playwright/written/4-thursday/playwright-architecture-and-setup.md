# Playwright Architecture and Setup

## Learning Objectives

By the end of this lesson you will be able to:

- Describe what Playwright is and what problems it solves compared with older browser automation tools.
- Explain the architecture: your Python script (client), the Playwright driver, and the browsers, and why this design is fast and reliable.
- Define the core objects: `Playwright`, `BrowserType`, `Browser`, `BrowserContext`, `Page`, and `Locator`, and describe how they nest.
- Install Playwright for Python, install browser binaries, and verify the installation.
- Choose between the synchronous and asynchronous APIs, and know why we use the sync API in this course.
- Launch Chromium, Firefox, and WebKit in headless and headed modes, and use `slow_mo`.
- Write and run a first script that navigates, locates an element with CSS, interacts with it, and takes a screenshot.
- Recognise the `pytest-playwright` plugin and its `page` fixture (a preview; the Playwright test runner is covered in depth on Friday).
- Troubleshoot common installation problems.

## Why This Matters

This week you built PyTest skills Monday through Wednesday, and today you learned how to describe web elements with CSS and XPath. Playwright is the tool that finally *drives a browser* using those locators. It is how this programme's weekly epic comes together: manual test design becomes automated, repeatable, browser-level tests for Project 1: QE Foundations.

Playwright (created by Microsoft) has become one of the most widely adopted end-to-end testing tools because it is fast, reliable, supports multiple browsers with one API, and ships with excellent debugging tools. Employers increasingly list it alongside or instead of Selenium. Understanding its architecture helps you debug sensibly, and a correct setup avoids the most common beginner frustration: "it will not run on my machine".

Today we focus on **understanding and setting up**. On Friday we will go deep on writing Playwright tests, the test runner, auto-waiting, built-in locators, filtering, the Inspector, and codegen. When we mention those today, it is only to say: we will cover this in depth on Friday.

---

## The Concept

### 1. What is Playwright?

**Playwright** is an open-source **browser automation** library. It lets code open a real browser, go to pages, click, type, read content, and check results, exactly as a human would. It is available for several languages (JavaScript/TypeScript, Python, Java, .NET). Because our course language is Python and PyTest, we use **Playwright for Python**.

What it can drive:

| Browser engine | Examples of browsers | Playwright name |
|----------------|----------------------|-----------------|
| Chromium | Google Chrome, Microsoft Edge, Opera | `chromium` |
| Firefox | Mozilla Firefox | `firefox` |
| WebKit | Apple Safari's engine | `webkit` |

One API works across all three, on Windows, macOS, and Linux, locally or in CI (Continuous Integration) servers.

**What it is used for:**

- End-to-end (E2E) UI tests.
- Cross-browser checks.
- Web scraping and automation of repetitive browser tasks.
- Generating screenshots and PDFs.
- Testing mobile layouts through device emulation.

### 2. Why Playwright? (Compared with Selenium)

You may meet Selenium on the job, so here is an honest comparison.

| Topic | Selenium (WebDriver) | Playwright |
|-------|----------------------|------------|
| Architecture | Your code sends HTTP commands to a separate driver executable per browser | A persistent connection to the browser; commands are streamed |
| Waiting | You write explicit waits often | **Auto-waiting** built into actions (Friday's topic) |
| Browser setup | You must install matching driver versions (modern Selenium Manager helps) | `playwright install` downloads tested browser builds |
| Isolation | Typically new browser or profile per test | Lightweight **browser contexts** isolate sessions in milliseconds |
| Debugging tools | Basic | Inspector, trace viewer, codegen, video, screenshots |
| Network control | Limited | Built-in interception and mocking |
| Language support | Many | JS/TS, Python, Java, .NET |
| Maturity | Very mature, enormous install base | Newer, growing quickly |

Neither is "wrong". Many teams run both. The skill of designing good tests transfers between them.

### 3. Architecture

Playwright has three main parts that work together.

```
 +----------------------+        +----------------------+        +------------------+
 |  Your Python code    |        |  Playwright driver   |        |  Browser         |
 |  (client library)    | <----> |  (Node.js process,   | <----> |  Chromium /      |
 |  pytest, scripts     |  JSON  |   bundled with the   | browser|  Firefox /       |
 |                      | over   |   Python package)    | protocol|  WebKit         |
 +----------------------+ pipe   +----------------------+        +------------------+
```

1. **Client library (your code).** The Python package `playwright` provides classes like `Page` and `Locator`. When you call `page.click(...)` it does not click anything itself. It serialises your request as a message.
2. **The driver.** The Python package bundles a small Node.js-based driver process. It receives your messages, applies Playwright's logic (auto-waiting, retries, actionability checks), and talks to the browser. You do not install Node.js separately; it ships inside the package.
3. **The browser.** Playwright talks to browsers over each engine's debugging protocol. For Chromium it uses the Chrome DevTools Protocol (CDP). For Firefox and WebKit, Playwright ships patched browser builds that expose an equivalent protocol, which is why `playwright install` downloads special builds rather than using the ones installed on your computer.

**Consequences you can feel as a tester:**

- **Speed.** One long-lived connection with events pushed from the browser is faster than request/response HTTP per command.
- **Reliability.** The driver can ask the browser about layout, visibility, and stability right before acting, so it can wait for the right moment automatically.
- **Out-of-process.** The browser runs separately; if it crashes, your script gets a clear error rather than hanging forever.
- **Pinned browser versions.** Each Playwright release works with a specific browser build, so a browser auto-update will not silently break your suite.

### 4. The Object Model

Playwright organises everything in a hierarchy. Learn these five names; they appear in every script.

```
Playwright
 └── BrowserType   (p.chromium / p.firefox / p.webkit)
      └── Browser          (one running browser process)
           └── BrowserContext   (an isolated "profile": cookies, storage, sessions)
                └── Page        (one tab)
                     └── Locator     (a way to find element(s) on that page)
```

- **Playwright:** the entry point (what `sync_playwright()` gives you as `p`).
- **BrowserType:** a browser engine; has `.launch()`.
- **Browser:** a started browser. Expensive to create (hundreds of milliseconds to seconds).
- **BrowserContext:** like an **incognito window**. Each context has its own cookies, local storage, and cache. Creating one is very cheap. This is the key to fast, isolated tests: one browser, a fresh context per test. Two contexts can be logged in as different users at the same time.
- **Page:** a single tab. Methods: `goto`, `title`, `url`, `screenshot`, `locator`, and so on.
- **Locator:** a description of how to find elements. A locator is *lazy*: creating it does not search the page. The search happens at the moment of an action or assertion, every time. That is why locators do not go "stale" (a common Selenium headache).

When you call `browser.new_page()`, Playwright quietly creates a new context and a page in it. It is a convenient shortcut for simple scripts. For tests you will usually manage contexts explicitly or let the test runner do it (Friday).

### 5. Sync vs. Async API

Playwright for Python offers two styles.

**Synchronous (what we use):**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ...
```

Code runs top to bottom, one statement at a time. Easy to read and debug. Ideal for beginners and fits PyTest naturally.

**Asynchronous:**

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ...

asyncio.run(main())
```

Uses Python's `async`/`await` and `asyncio`. It is useful when integrating into async applications or running many browsers concurrently. For test suites the sync API is the norm, and we use it throughout this week. Do not mix the two styles in the same script, and do not call the sync API from inside a running asyncio event loop (e.g. in Jupyter without care), or you will get an error such as "It looks like you are using Playwright Sync API inside the asyncio loop".

### 6. Installing Playwright for Python

**Prerequisites:**

- Python 3.9 or newer (check with `python --version`; Playwright Python's supported versions evolve, so check the docs if you are on a very old or very new Python).
- `pip` (Python's package installer).
- Internet access for the first install (browsers are downloaded, roughly 100-200 MB each).

**Step 1: Create and activate a virtual environment.** A virtual environment keeps this project's packages separate from other projects.

Windows (PowerShell):

```powershell
mkdir pw-intro
cd pw-intro
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell refuses to run the activation script because of execution policy, use Command Prompt (`.venv\Scripts\activate.bat`) or run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` for the current window only.

macOS / Linux:

```bash
mkdir pw-intro && cd pw-intro
python3 -m venv .venv
source .venv/bin/activate
```

When active, your prompt shows `(.venv)`.

**Step 2: Install the package.** There are two common choices:

```bash
# Option A: the Playwright library only (for scripts)
pip install playwright

# Option B: the PyTest plugin (includes the library as a dependency)
pip install pytest-playwright
```

We will install **pytest-playwright**, because it brings both the library and PyTest integration, which our course uses on Friday:

```bash
pip install pytest-playwright
```

**Step 3: Install the browsers.** The Python package does **not** include the browser binaries. Download them with:

```bash
playwright install
```

This downloads Chromium, Firefox, and WebKit (plus a headless shell and FFmpeg for video). To save time and disk space install only one:

```bash
playwright install chromium
```

If the `playwright` command is not found, run it as a module: `python -m playwright install`.

On Linux (and in CI containers) the browsers need system libraries. Playwright can install them for you:

```bash
playwright install --with-deps chromium
```

(This uses `sudo` or must be run as root on Debian/Ubuntu.)

**Step 4: Verify.**

```bash
python -c "import playwright; print('playwright imported')"
playwright --version
pip show playwright
```

**Step 5: Save dependencies.**

```bash
pip freeze > requirements.txt
```

so a teammate (or your pair) can recreate the environment with `pip install -r requirements.txt` followed by `playwright install`.

> Browser files are stored in a cache folder on your machine (e.g. `%USERPROFILE%\AppData\Local\ms-playwright` on Windows, `~/Library/Caches/ms-playwright` on macOS, `~/.cache/ms-playwright` on Linux). They are shared by all projects. Every Playwright version expects specific browser builds, so after upgrading the package, run `playwright install` again.

### 7. Launching Browsers: Options That Matter

```python
browser = p.chromium.launch(headless=False, slow_mo=500)
```

| Option | Meaning |
|--------|---------|
| `headless` | `True` (default): no visible window; faster, used in CI. `False`: a visible window so you can watch. |
| `slow_mo` | Milliseconds to pause between actions: use only while learning/debugging, so you can follow along. |
| `channel` | Use an installed branded browser, e.g. `channel="chrome"` or `"msedge"`, instead of the bundled Chromium. |
| `args` | Extra command-line flags for the browser (advanced). |

Context options (set in `browser.new_context(...)`) include `viewport={"width": 1280, "height": 720}`, `locale="en-US"`, `timezone_id`, `geolocation`, `permissions`, `user_agent`, and `record_video_dir`. Device emulation uses `p.devices["iPhone 13"]`.

### 8. A Preview of the PyTest Plugin

`pytest-playwright` supplies ready-made fixtures such as `page`, `context`, and `browser`, plus command-line options (`--headed`, `--browser firefox`, `--slowmo 500`). A test then looks like this:

```python
def test_has_title(page):
    page.goto("https://playwright.dev/")
    assert "Playwright" in page.title()
```

You write `pytest`; the plugin starts the browser, gives your test a fresh page, and cleans up afterwards. This idea builds directly on the fixtures you mastered on Tuesday. **We will cover the test runner, its options, assertions, and configuration in depth on Friday**; today we use plain scripts so you can see the moving parts.

### 9. Getting Ready for Friday (What You Do Not Need Yet)

Playwright has many features: auto-waiting, built-in locators like `get_by_role`, the Inspector, codegen, tracing, network mocking. You will meet auto-waiting, built-in locators, filtering/chaining, the Inspector, and codegen on **Friday**. Today the goal is a working installation and a mental model of the architecture.

---

## Code Examples

### Example 1: Smoke test of the installation

Create `smoke.py`:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    print("Title:", page.title())
    browser.close()
```

Run:

```bash
python smoke.py
```

Expected output similar to: `Title: Fast and reliable end-to-end testing for modern web apps | Playwright`

**Line-by-line:**

1. `from playwright.sync_api import sync_playwright`: import the sync entry point.
2. `with sync_playwright() as p:` starts the driver process and gives the `Playwright` object `p`. The `with` block guarantees cleanup (stopping the driver) even if an error occurs.
3. `p.chromium.launch()` starts a Chromium browser process in headless mode and returns a `Browser`.
4. `browser.new_page()` creates a new context and a tab, returning a `Page`.
5. `page.goto(url)` navigates and waits for the page's `load` event by default.
6. `page.title()` reads the document title.
7. `browser.close()` closes the browser and all its pages.

If this prints a title, your installation works.

### Example 2: A first real interaction with CSS locators

This uses a stable, public practice site for automation (Sauce Demo). Credentials are published on the site's login page.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=700)   # visible and slowed for learning
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()

    page.goto("https://www.saucedemo.com/")
    print("URL:", page.url)

    # CSS locators from today's lessons
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # After login the URL changes and the inventory list appears
    print("URL after login:", page.url)
    items = page.locator(".inventory_item")
    print("Number of products:", items.count())
    print("First product:", items.first.locator(".inventory_item_name").inner_text())

    page.screenshot(path="inventory.png")
    print("Screenshot saved to inventory.png")

    context.close()
    browser.close()
```

**Line-by-line:**

- `launch(headless=False, slow_mo=700)` shows a real window and waits 700 ms between actions so you can follow what happens.
- `browser.new_context(viewport=...)` creates an isolated session with a fixed window size (consistent size = consistent layout = more reliable tests).
- `context.new_page()` opens a tab in that context.
- `page.locator("#user-name").fill("standard_user")`: finds the element by ID and types into it. `fill()` clears the field first and sets the value.
- `.click()` clicks the login button. Playwright first waits until the element is attached, visible, stable, enabled, and receiving events (this is auto-waiting; we study it in depth on Friday).
- `page.url` is a property (no parentheses) containing the current URL.
- `items = page.locator(".inventory_item")` defines a locator for all product cards. `items.count()` runs the search now and returns the number found (6 on the live site at the time of writing).
- `items.first` narrows the locator to the first match; `.locator(".inventory_item_name")` searches inside it (a chained locator); `.inner_text()` reads the text.
- `page.screenshot(path=...)` saves a PNG of the current viewport.
- We close the context first, then the browser.

If the site changes its markup, you may need to adjust selectors: a good reminder of the previous lessons on dynamic selectors. Use DevTools to confirm each selector.

### Example 3: All three browsers in a loop

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for browser_type in (p.chromium, p.firefox, p.webkit):
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto("https://playwright.dev/")
        print(f"{browser_type.name:9} -> {page.title()}")
        browser.close()
```

**Explanation:** `browser_type.name` returns `'chromium'`, `'firefox'`, or `'webkit'`. The loop proves the same API drives all three engines. This requires `playwright install` (with no browser name) so that all three are present. If you installed only Chromium, Firefox and WebKit will raise an error telling you to run `playwright install`.

### Example 4: Isolation with browser contexts

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()

    ctx_a = browser.new_context()
    ctx_b = browser.new_context()

    page_a = ctx_a.new_page()
    page_b = ctx_b.new_page()

    page_a.goto("https://www.saucedemo.com/")
    page_a.locator("#user-name").fill("standard_user")
    page_a.locator("#password").fill("secret_sauce")
    page_a.locator("#login-button").click()

    page_b.goto("https://www.saucedemo.com/inventory.html")   # not logged in in this context

    print("A URL:", page_a.url)
    print("B URL:", page_b.url)       # redirected back to the login page

    ctx_a.close()
    ctx_b.close()
    browser.close()
```

**Explanation:** two contexts in one browser do not share cookies or storage, so context B is "not logged in" although A is. This is how test runners keep tests independent and fast: new context per test, not new browser. (The exact redirect behaviour of the site may vary; the point is the isolation.)

### Example 5: A first PyTest test with the plugin (preview)

Create `test_first.py`:

```python
import re
from playwright.sync_api import Page, expect

def test_playwright_site_title(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
```

Run:

```bash
pytest                       # headless Chromium by default
pytest --headed              # watch it
pytest --browser firefox     # run with Firefox
pytest --slowmo 500 --headed # slow-motion
```

**Explanation:** `page` is a fixture supplied by `pytest-playwright`; the annotation `Page` is only for editor help. `expect(page).to_have_title(...)` is a Playwright assertion that retries until it passes or times out. The `expect` assertions, fixtures supplied by the plugin, and the full command-line options are explained **in depth on Friday**.

---

## Real-World Scenarios

1. **Cross-browser regression.** A retail company must support Chrome, Safari, and Firefox. One Playwright test suite runs against all three engines by changing a command-line option instead of writing three suites.
2. **CI pipelines.** Tests run headless inside a Docker container on every pull request. Setup is `pip install -r requirements.txt` and `playwright install --with-deps`.
3. **Multi-user flows.** A chat feature needs two users at once. The test creates two browser contexts in one browser and sends messages between them.
4. **Mobile layout.** The team emulates a phone using a device descriptor to ensure the hamburger menu appears.
5. **Onboarding new testers.** A checked-in `requirements.txt` plus a README with the two install commands means a new teammate is productive in minutes.

---

## Common Mistakes

1. **Forgetting `playwright install`.** `pip install` gives you the library, not the browsers. The error message says "Executable doesn't exist ... please run playwright install".
2. **Installing outside the virtual environment**, so `pytest` or `playwright` is not found, or versions clash.
3. **Naming your file `playwright.py`** (or `pytest.py`). Python then imports your file instead of the library. Name scripts differently.
4. **Mixing sync and async APIs**, or running the sync API in an environment with an event loop (Jupyter).
5. **Forgetting `browser.close()`**, leaving processes running (with `with` blocks and the test runner this is handled).
6. **Launching a new browser for every test**: slow. Prefer new contexts.
7. **Using `time.sleep()` to wait.** Playwright auto-waits for actions; Friday explains how.
8. **Running headed tests on a server without a display.** CI should use headless.
9. **Behind a corporate proxy or firewall**, the browser download fails. Ask IT for the proxy settings, or set `HTTPS_PROXY` before running `playwright install`.
10. **Not re-running `playwright install` after upgrading** the package.

---

## Practice Exercises

**Exercise 1: Install and verify.** Create a new folder and virtual environment, install `pytest-playwright`, install Chromium, and run `smoke.py`. Paste your output into your notes. *Checkpoint:* the title line prints with no error.

**Exercise 2: Explain the architecture.** In three or four sentences, explain what happens, step by step, when your script runs `page.click("#login-button")`. *Model answer:* the Python client serialises the call and sends it to the Playwright driver; the driver finds the element and checks it is ready (visible, stable, enabled); the driver sends the click to the browser through its protocol; the browser performs it and reports the result back.

**Exercise 3: Object hierarchy.** Draw the hierarchy from `Playwright` to `Locator` and write one sentence on each level. Which level would you create once per test run and which once per test? *Hint:* browser per run (or session), context and page per test.

**Exercise 4: Launch options.** Modify Example 2 so that it (a) uses Firefox, (b) uses a 375x667 viewport (a phone), and (c) saves a screenshot named `mobile-login.png` *before* logging in. *Solution sketch:*

```python
browser = p.firefox.launch(headless=False)
context = browser.new_context(viewport={"width": 375, "height": 667})
page = context.new_page()
page.goto("https://www.saucedemo.com/")
page.screenshot(path="mobile-login.png")
```

**Exercise 5: Use today's locators.** Open the practice pages you saved earlier today (`shop.html`, `pseudo.html`, `combinators.html`, `xpath.html`). Write a script that opens each file, prints its `title()`, and prints the number of elements matching one CSS selector and one XPath of your choice. Make the script loop over a list of `(file, css, xpath)` tuples.

*Solution sketch:*

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

CHECKS = [
    ("shop.html", "button", "//button"),
    ("xpath.html", "tr.row", "//tr[@class='row']"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for file, css, xpath in CHECKS:
        page.goto(Path(file).resolve().as_uri())
        print(page.title(), page.locator(css).count(), page.locator(f"xpath={xpath}").count())
    browser.close()
```

**Exercise 6: Isolation.** Reproduce Example 4. Then add a third context and give it a different viewport. Print `page.viewport_size` for each page. What do you observe? *Answer:* each context carries its own settings and state.

**Exercise 7: Breaking things on purpose.** (a) Rename `smoke.py` to `playwright.py` and run it. What happens, and why? (b) Uninstall browsers' cache (or run on a machine without them) and read the error. Write down the exact fix suggested in the message. *Hint for (a):* the file shadows the library; rename it back.

**Exercise 8 (pair task preview).** With your partner, decide: which practice site will you use for this afternoon's locator catalog? Install Playwright on **both** laptops and share the `requirements.txt` through your shared repo or branch, so both can run each other's code.

---

## Summary

- **Playwright** drives real Chromium, Firefox, and WebKit browsers with one API; we use **Playwright for Python** with the **sync API**.
- **Architecture:** your Python client talks to a bundled Playwright driver, which talks to the browser through its debugging protocol. This gives speed, reliability, and pinned browser builds.
- **Object model:** `Playwright` > `BrowserType` > `Browser` > `BrowserContext` > `Page` > `Locator`. Contexts are cheap, isolated sessions; locators are lazy and never go stale.
- **Setup:** create a virtual environment, `pip install pytest-playwright`, run `playwright install` (or `playwright install chromium`), and verify with a smoke script. Use `--with-deps` on Linux.
- **Options:** `headless`, `slow_mo`, viewport, and browser choice help you debug and scale.
- The `pytest-playwright` plugin provides a `page` fixture; we will cover the test runner, auto-waiting, built-in locators, filtering and chaining, the Inspector, and codegen in depth on **Friday**.
- CSS and XPath locators from today's lessons work directly in `page.locator()`.

---

## Additional Resources

- Playwright for Python, Installation: https://playwright.dev/python/docs/intro
- Playwright for Python, Library (sync and async, browsers): https://playwright.dev/python/docs/library
- Playwright for Python, Browser contexts: https://playwright.dev/python/docs/browser-contexts
