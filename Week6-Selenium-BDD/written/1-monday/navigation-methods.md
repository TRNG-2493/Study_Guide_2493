# Navigation Methods

## Learning Objectives

By the end of this lesson you will be able to:

- Open a URL with `driver.get()` and with `driver.navigate().to()`, and explain the (small) difference.
- Move through browser history with `back()`, `forward()`, and `refresh()`, and predict what the browser does after any sequence of these calls.
- Read information about the current page: `getTitle()`, `getCurrentUrl()`, and `getPageSource()`, and choose the right one for a given check.
- Control the browser window: maximize, minimize, fullscreen, set size and position.
- Use basic navigation facts to write simple verifications (for example, "after login the URL contains `/inventory`").
- Understand what "page load" means to Selenium, recognise its limits, and set a page load timeout.
- Close one window vs. the whole session (`close()` / `quit()`).
- Diagnose common navigation problems from the exception text.

---

## Why This Matters

Every automated test begins by getting to the right place in the application, and most tests also *prove* that a user ended up in the right place. "After clicking Login the user lands on the inventory page" is a navigation check. "The Back button returns the user to the product list" is another.

Navigation methods are simple, but they are used in nearly every test you will write in **Project 2**. Misusing them is a frequent source of bugs: for example, reading `getCurrentUrl()` before the browser has finished navigating, or running tests in a browser window so small that the page shows a mobile layout and hides the buttons your test needs.

### A tester's day

A QA engineer at an online shop is asked to automate this check: *"A customer who logs in should land on the product list, and after opening the cart and pressing the browser's Back button they should return to the product list with their login intact."* Look at what that single sentence needs:

1. Open the shop's address (`get`).
2. Check the URL after login (`getCurrentUrl`).
3. Open the cart (a click, covered Tuesday).
4. Press the browser's Back button (`navigate().back()`).
5. Check again where the user is (`getCurrentUrl`, `getTitle`).

Four of the five steps are navigation methods. If you master this lesson, you can already write the skeleton of that test.

### How this connects to previous lessons

- *Architecture:* each navigation call is one HTTP request to the driver (`POST /url`, `POST /back`, `POST /refresh`, `GET /url`, `GET /title`). They are synchronous: the call returns only after the browser has done the work.
- *Driver configuration:* you learned `quit()` ends the session; here we compare it again with `close()`.
- *Locator strategies:* after navigating, you will usually locate elements on the new page. We use that carefully here, because elements found *before* a navigation become unusable after it.

---

## The Concept

### 1. Opening a Page: `get()` and `navigate().to()`

Both open a URL in the current browser window:

```java
driver.get("https://www.saucedemo.com");
driver.navigate().to("https://www.saucedemo.com");
```

| | `driver.get(url)` | `driver.navigate().to(url)` |
|---|---|---|
| Purpose | Load a URL | Load a URL |
| Waits for page load? | Yes (by default) | Yes (by default) |
| Accepts `String` | Yes | Yes |
| Accepts `java.net.URL` object | No | Yes (overload) |
| Part of a history API? | No | Yes, belongs to the `Navigation` object together with `back()`, `forward()`, `refresh()` |

In practice they behave identically. Convention: use `get()` for the first load of a test and `navigate()` methods when you are thinking in terms of *history* (back/forward/refresh).

**Always include the protocol** (`https://` or `http://`). `driver.get("www.saucedemo.com")` throws an `InvalidArgumentException` ("invalid argument").

**What happens when `driver.get("https://www.saucedemo.com")` runs (step by step):**

1. The Java client sends `POST /session/{id}/url` with `{"url": "https://www.saucedemo.com"}` to chromedriver.
2. Chromedriver tells Chrome to navigate.
3. Chrome sends a network request, receives the HTML, builds the DOM, loads styles, scripts and images.
4. When Chrome fires the document `load` event, chromedriver answers the HTTP request.
5. `get` returns and your next line runs.

Your Java thread sits idle during steps 2 to 4. That is why `get` can take anywhere from 100 ms to many seconds depending on the site.

#### Where do the `Navigation` methods live?

`driver.navigate()` returns an object of type `WebDriver.Navigation`. That object has the methods `to(String)`, `to(URL)`, `back()`, `forward()` and `refresh()`. So `driver.navigate().back()` is two steps chained: first get the navigation object, then call `back()` on it. The same pattern appears with `driver.manage()` (window and timeouts) later in this lesson.

```java
WebDriver.Navigation nav = driver.navigate();   // same thing, split in two lines
nav.to("https://www.saucedemo.com");
nav.refresh();
```

#### Building URLs sensibly

In a real framework you rarely type full URLs in every test. You keep the base address in one place so you can point the same tests at development, staging or production:

```java
String baseUrl = System.getProperty("baseUrl", "https://www.saucedemo.com");
driver.get(baseUrl);
driver.get(baseUrl + "/inventory.html");   // note: the site requires login first; shown only for URL building
```

Run with `-DbaseUrl=https://staging.example.com` to change it. This is the same `-D` system property idea you used in the driver factory.

#### Other kinds of addresses

| Address | What it does | Example use |
|---|---|---|
| `https://...` / `http://...` | Normal web page | Everything |
| `file:///C:/work/page.html` | Local file in the browser | Practising on your own HTML file |
| `about:blank` | Empty page | Resetting the browser between steps |
| URL with credentials | `https://admin:admin@the-internet.herokuapp.com/basic_auth` | Pages protected by browser basic authentication |

The `basic_auth` trick is useful: the-internet site has a page that normally shows a browser login popup, which Selenium cannot type into (native popups are outside the page). Putting the username and password into the URL avoids the popup in Chrome. After `get`, `driver.findElement(By.cssSelector(".example p")).getText()` should show `Congratulations! You must have the proper credentials.`

#### What does "waits for page load" mean?

By default Selenium blocks until the browser reports the document's `load` event: the HTML and its resources (images, stylesheets, scripts) have finished loading. This is called the **page load strategy** `normal`.

Important limitations:

- Modern pages built with React, Angular, or Vue often show a skeleton and then fetch data in the background after the `load` event. Selenium considers the page "loaded", while content may still be arriving. The fix is a *wait*, which is Tuesday's topic.
- If a page never finishes loading (a stuck ad script), `get()` can hang until the **page load timeout** (default 300 seconds) and throw a `TimeoutException`. You can configure a shorter timeout (see the code example and the *Browser Options* lesson):

```java
driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
```

(`Duration` is from `java.time.Duration`.)

**Line by line:**

- `driver.manage()` returns an `Options` object that groups browser settings (timeouts, window, cookies).
- `.timeouts()` narrows to timeout settings.
- `.pageLoadTimeout(...)` sets the maximum time a navigation may wait.
- `Duration.ofSeconds(30)` is the Java way to say "30 seconds" as an object. Selenium 4 uses `Duration` instead of the old `(30, TimeUnit.SECONDS)` pair.

**What the exception looks like when the timeout fires:**

```
org.openqa.selenium.TimeoutException: timeout: Timed out receiving message from renderer: 30.000
```

This means the page did not finish loading in 30 seconds. It is *not* a locator error. The best response is to find out *why* the page is slow (network, test environment, a third-party script), not to raise the timeout blindly.

**Page load strategies (awareness).** Selenium supports three strategies, selected through browser options (the *Browser Options* lesson shows how to configure options):

| Strategy | `get()` returns when | Use |
|---|---|---|
| `normal` (default) | The `load` event has fired | Almost always |
| `eager` | The DOM is ready (`DOMContentLoaded`), before images and stylesheets finish | Image-heavy pages when you only need the DOM |
| `none` | Immediately, without waiting | Advanced scenarios with your own waiting logic |

Beginners should stay on `normal`. Using `none` or `eager` without understanding waits creates flaky tests.

### 2. Moving Through History

The browser keeps a history list, exactly like when you use the Back and Forward buttons.

```java
driver.get("https://www.saucedemo.com");                 // page A
driver.navigate().to("https://the-internet.herokuapp.com"); // page B

driver.navigate().back();      // returns to page A
driver.navigate().forward();   // returns to page B
driver.navigate().refresh();   // reloads the current page
```

| Method | Real-world meaning | Typical test use |
|---|---|---|
| `back()` | Browser Back button | Verify that returning from the cart restores the product list |
| `forward()` | Browser Forward button | Rare; test history behavior |
| `refresh()` | F5 / Reload | Verify data persists after reload; reset page state |

Notes:

- `back()` when there is no history does nothing (no error).
- After `refresh()`, any `WebElement` you found earlier is **stale** because the page was rebuilt. You must find elements again. (This is the "reference" idea from the architecture lesson.)
- `driver.navigate().refresh()` reloads the current page in place. Calling `driver.get(driver.getCurrentUrl())` has a similar visible effect, but it is a new navigation rather than a reload, so prefer `refresh()` when you mean "reload".

**Think of history as a list with a bookmark.** Imagine a row of cards, one per visited page, and a bookmark on the current card:

```
Start:               [A]
get(B):              [A] [B]*              (* = current page)
get(C):              [A] [B] [C]*
back():              [A] [B]* [C]
back():              [A]* [B] [C]
forward():           [A] [B]* [C]
get(D):              [A] [B] [D]*          (C is thrown away: new navigation after going back erases the "forward" part)
```

The last row is important: once you navigate somewhere new after going back, the forward pages are lost, exactly as in a real browser. `forward()` then does nothing.

**Why does `refresh()` make elements stale?** Remember that a `WebElement` is a reference ID pointing to a node in the current DOM. A refresh throws the DOM away and builds a new one, so the old ID points at nothing:

```java
WebElement heading = driver.findElement(By.tagName("h1"));
driver.navigate().refresh();
heading.getText();    // throws StaleElementReferenceException
```

The fix is to find the element again after the refresh:

```java
driver.navigate().refresh();
WebElement heading = driver.findElement(By.tagName("h1"));   // fresh reference
```

**When to use `refresh()` in tests:** to confirm data was saved (add an item, refresh, check it is still there); to recover a page after an intermittent glitch while debugging; to reset a page to a known state. **When not to:** as a cure for flaky timing; reloading hides the real problem.

### 3. Getting Information About the Page

```java
String title  = driver.getTitle();         // text inside <title>
String url    = driver.getCurrentUrl();    // the address now loaded
String source = driver.getPageSource();    // the page's HTML as a String
```

| Method | Returns | Example result |
|---|---|---|
| `getTitle()` | Title text shown on the browser tab | `"Swag Labs"` |
| `getCurrentUrl()` | The URL of the current page, including any redirect or query string | `"https://www.saucedemo.com/inventory.html"` |
| `getPageSource()` | The HTML of the current DOM, as seen by the browser | `"<!DOCTYPE html><html lang=..."` |

**Use cases:**

- Confirm login success by checking the URL: `driver.getCurrentUrl().contains("inventory")`.
- Confirm page identity by title.
- `getPageSource()` is useful for debugging or checking that some text exists anywhere on the page (`driver.getPageSource().contains("Thank you")`), but it is a **blunt** tool: it finds text inside scripts and hidden elements too. Prefer locating a visible element and reading its text.

**Warning about timing:** if you click a button and immediately call `getCurrentUrl()` the page may not have navigated yet, so you read the *old* URL. Selenium's click normally waits for navigation that the click itself starts, but not for client-side redirects that JavaScript performs a moment later. When you see random failures on URL checks, a wait (Tuesday) is the correct cure; do not use `Thread.sleep`.

#### Choosing how to compare a URL

URLs often contain parts that change (domain in each environment, query strings, session tokens). Pick the weakest comparison that still proves the point:

| Check | Code | When to use |
|---|---|---|
| Exact | `url.equals("https://www.saucedemo.com/inventory.html")` | Fixed, known address; breaks across environments |
| Ends with | `url.endsWith("/inventory.html")` | Same page in dev/stage/prod |
| Contains | `url.contains("inventory")` | Loose check; risk of false positives (`/inventory-error`) |
| Starts with | `url.startsWith(baseUrl)` | Confirm you stayed in the right site |

A good habit is `endsWith("/inventory.html")` rather than `contains("inventory")`, because it is exact about the page but independent of the host name.

#### Title vs. URL vs. visible heading

| Evidence | Strength | Weakness |
|---|---|---|
| URL | Reliable, cheap | Does not prove the page rendered correctly |
| Title | Cheap, human-readable | Often the same on many pages (SauceDemo's title is `Swag Labs` everywhere) |
| A visible element (e.g. page heading) | Strongest proof the user sees the right page | Needs a locator |

For a rigorous test, combine URL (right address) with a visible element (right content).

#### A redirect example

On `https://the-internet.herokuapp.com/redirector` there is a link that triggers a server redirect. After clicking it (clicking is covered in depth Tuesday), `getCurrentUrl()` reports the **final** address (`.../status_codes`), not the one you clicked. This is why `getCurrentUrl()` is the way to learn *where you actually ended up*.

### 4. Controlling the Browser Window

Window size changes layouts! Many sites are *responsive*: on narrow windows the menu collapses into a hamburger icon and your normal locators disappear. For reliable tests, set the window state explicitly.

```java
driver.manage().window().maximize();              // fill the screen (most common)
driver.manage().window().fullscreen();            // like pressing F11
driver.manage().window().minimize();              // minimize to taskbar
driver.manage().window().setSize(new Dimension(1280, 800));
driver.manage().window().setPosition(new Point(0, 0));

Dimension size = driver.manage().window().getSize();
System.out.println(size.getWidth() + " x " + size.getHeight());
```

(`Dimension` and `Point` are in `org.openqa.selenium`.)

| Method | Use |
|---|---|
| `maximize()` | Default choice for desktop tests |
| `setSize(...)` | Reproduce a particular screen resolution, test responsive layout |
| `fullscreen()` | Kiosk-like testing |
| `minimize()` | Rare |
| `getSize()` / `getPosition()` | Report or assert window state |

> **Headless mode and maximize:** In a headless browser (no visible window, see *Browser Options*), `maximize()` has no effect because there is no screen. Use `setSize(...)` or the `--window-size` option instead.

**Line by line:**

- `driver.manage().window()` returns a `Window` object for the current browser window.
- `new Dimension(1280, 800)` is a small Selenium class holding width and height in pixels.
- `new Point(0, 0)` holds x and y screen coordinates. `(0, 0)` is the top-left corner of the screen.
- `getSize()` returns a `Dimension`, whose `getWidth()` and `getHeight()` we print.

**Why window size matters, with an example.** Open `https://www.saucedemo.com/inventory.html` (after logging in) at 1366 x 768 and you see a normal "burger" menu icon at top left and a cart at top right. At 400 x 800 the layout compresses; some elements may wrap or hide. A locator that worked at 1366 wide may fail at 400 wide because the element is not displayed. When a test passes on your laptop and fails on the CI server, a different default window size is a classic reason: servers often start browsers at 800 x 600.

**Choosing a size strategy:**

| Situation | Recommendation |
|---|---|
| Local development with a visible browser | `maximize()` |
| CI server, headless | `setSize(new Dimension(1920, 1080))` or `--window-size=1920,1080` |
| Testing a "mobile" layout on purpose | `setSize(new Dimension(390, 844))` |
| Visual comparisons / screenshots | Fixed size for repeatable images (see the *Screenshots* lesson) |

### 5. Closing Windows: `close()` and `quit()` Revisited

```java
driver.close();  // closes the window that currently has focus
driver.quit();   // closes everything and ends the session
```

On Wednesday you will open multiple windows and tabs and use `close()` deliberately. For now, always finish a test with `quit()`.

**Why `close()` on a single-window test is a trap:** with one window open, `close()` closes it, but the session and the chromedriver process may stay alive. Subsequent commands throw `NoSuchWindowException` or similar, and the process lingers. `quit()` is the complete cleanup.

### 6. Navigation Within the Same Page: Fragments and Links

A URL such as `https://example.com/page#section2` has a **fragment** (`#section2`) that scrolls the page but does not reload it. Selenium treats `driver.get("https://example.com/page#section2")` after already being on `https://example.com/page` as an in-page jump; it may return immediately without a full reload. Be aware of this if your test seems to "not navigate".

More commonly, you navigate by **clicking links** (`element.click()`); you will practice clicking in the next lessons and in depth tomorrow.

**Single-page applications (SPAs).** SauceDemo is built as a single-page application: moving from the login page to the inventory page changes the URL *without* a full page reload; JavaScript redraws the page. For navigation methods this has two consequences: (1) `back()` and `forward()` still work as in a normal site, because the app uses the browser's history; (2) the moment the URL changes and the moment the new content is drawn may differ slightly, which is another reason that waits exist.

### 7. Putting the Methods Together: a Mental Model

```
 get / navigate().to    ---> go somewhere NEW (adds to history)
 back / forward         ---> move the bookmark in history
 refresh                ---> reload the CURRENT page (history unchanged)
 getTitle / getCurrentUrl / getPageSource ---> ASK where we are, change nothing
 manage().window()      ---> change the WINDOW, not the page
 close / quit           ---> end the window / end everything
```

Three groups: *go*, *ask*, *window/cleanup*. Almost every test follows the order: set up window, go, (interact), ask, clean up.

---

## Code Example: A Navigation Tour

```java
package com.revature.qea.navigation;

import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

public class NavigationDemo {

    public static void main(String[] args) throws MalformedURLException {
        WebDriver driver = new ChromeDriver();

        try {
            // Safety net: do not hang for 5 minutes on a broken page
            driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));

            // Deterministic window size
            driver.manage().window().setSize(new Dimension(1366, 768));

            // 1. Open the first page
            driver.get("https://www.saucedemo.com");
            System.out.println("1. Title: " + driver.getTitle());
            System.out.println("   URL  : " + driver.getCurrentUrl());

            // 2. Open a second page using navigate().to(String)
            driver.navigate().to("https://the-internet.herokuapp.com");
            System.out.println("2. Title: " + driver.getTitle());

            // 3. navigate().to(URL) overload
            driver.navigate().to(new URL("https://the-internet.herokuapp.com/login"));
            System.out.println("3. URL  : " + driver.getCurrentUrl());

            // 4. Go back twice: login page -> home page -> SauceDemo
            driver.navigate().back();
            System.out.println("4. After back: " + driver.getCurrentUrl());
            driver.navigate().back();
            System.out.println("   After 2nd back: " + driver.getCurrentUrl());

            // 5. Go forward once
            driver.navigate().forward();
            System.out.println("5. After forward: " + driver.getCurrentUrl());

            // 6. Reload
            driver.navigate().refresh();
            System.out.println("6. Reloaded: " + driver.getTitle());

            // 7. Length of the page's HTML
            System.out.println("7. Page source length: " + driver.getPageSource().length());

            // 8. A simple navigation-based verification
            String expected = "the-internet";
            String actual = driver.getCurrentUrl();
            System.out.println(actual.contains(expected) ? "PASS" : "FAIL: " + actual);

        } finally {
            driver.quit();
        }
    }
}
```

**Explanation:**

- `pageLoadTimeout(Duration.ofSeconds(30))` limits how long `get`/`navigate().to` may wait.
- `setSize(new Dimension(1366, 768))` gives every run the same layout.
- The history calls demonstrate the stack-like nature: two `back()` calls retrace both visited pages; `forward()` moves one step ahead.
- The final check shows the typical use of `getCurrentUrl()` in a test: confirm *where we ended up*.

**Line-by-line notes on the new syntax:**

| Code | Meaning |
|---|---|
| `throws MalformedURLException` | `new URL(String)` can fail with this *checked* exception if the text is not a valid URL, so Java forces us to declare or catch it. |
| `import java.net.URL;` | The standard Java URL class, not a Selenium class. |
| `try { ... } finally { driver.quit(); }` | Guarantees cleanup, as in earlier lessons. |
| `actual.contains(expected) ? "PASS" : "FAIL: " + actual` | The *ternary operator*: `condition ? valueIfTrue : valueIfFalse`. A compact `if/else` that produces a value. |

**Step-by-step trace with expected output.**

| Step | Browser history after the step (`*` = current) | Printed |
|---|---|---|
| 1 | `[Sauce]*` | `1. Title: Swag Labs` and `URL  : https://www.saucedemo.com/` |
| 2 | `[Sauce] [Internet]*` | `2. Title: The Internet` |
| 3 | `[Sauce] [Internet] [Login]*` | `3. URL  : https://the-internet.herokuapp.com/login` |
| 4a | `[Sauce] [Internet]* [Login]` | `4. After back: https://the-internet.herokuapp.com/` |
| 4b | `[Sauce]* [Internet] [Login]` | `After 2nd back: https://www.saucedemo.com/` |
| 5 | `[Sauce] [Internet]* [Login]` | `5. After forward: https://the-internet.herokuapp.com/` |
| 6 | unchanged | `6. Reloaded: The Internet` |
| 7 | unchanged | a number (the length of the HTML) |
| 8 | unchanged | `PASS` |

If your output differs, check each step against the table; the difference tells you which assumption about history was wrong.

### A second example: a login-landing check

```java
package com.revature.qea.navigation;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class LoginLandingCheck {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        try {
            driver.manage().window().maximize();
            driver.get("https://www.saucedemo.com");

            String before = driver.getCurrentUrl();

            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.id("password")).sendKeys("secret_sauce");
            driver.findElement(By.id("login-button")).click();

            String after = driver.getCurrentUrl();
            System.out.println("Before: " + before);
            System.out.println("After : " + after);

            if (after.endsWith("/inventory.html")) {
                System.out.println("PASS: landed on the inventory page");
            } else {
                System.out.println("FAIL: unexpected page " + after);
            }
        } finally {
            driver.quit();
        }
    }
}
```

**What it does:** opens the login page, records the URL, types the credentials (typing and clicking are covered in depth on Tuesday; here we only need them to cause a navigation), presses Login, and compares the new URL.

**Expected output:**

```
Before: https://www.saucedemo.com/
After : https://www.saucedemo.com/inventory.html
PASS: landed on the inventory page
```

**Negative test:** change the password to `wrong` and re-run. The URL stays `https://www.saucedemo.com/`, an error banner appears, and the program prints `FAIL: unexpected page https://www.saucedemo.com/`. A test that can fail for the right reason is just as valuable as one that passes.

### A third example: a reusable helper

```java
static void open(WebDriver driver, String url) {
    driver.get(url);
    System.out.println("Opened: " + driver.getTitle() + " (" + driver.getCurrentUrl() + ")");
}
```

Small helpers like this reduce repetition and give consistent log lines for debugging. Later in the week you will organise such helpers into classes.

---

## Troubleshooting Navigation Problems

### Walk-through 1: `InvalidArgumentException`

```
org.openqa.selenium.InvalidArgumentException: invalid argument
  (Session info: chrome=126.0...)
```

Cause: the URL text is not valid, most often a missing protocol such as `www.saucedemo.com`. Fix: add `https://`. Check for stray spaces or a pasted newline at the end of the string; `url.trim()` helps when the value comes from a file or property.

### Walk-through 2: the page "loads" but my next step fails

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: {"method":"css selector","selector":"[id="x"]"}
```

right after `get`. Diagnosis: (1) print `driver.getCurrentUrl()` and `driver.getTitle()` just before the failing line: did you land where you expected (a redirect to a login or an error page)? (2) If the page is correct, the element may be drawn by JavaScript after the `load` event, so this is a timing problem: **Tuesday's waits** are the cure, not `Thread.sleep`.

### Walk-through 3: `TimeoutException` on `get`

```
org.openqa.selenium.TimeoutException: timeout: Timed out receiving message from renderer: 30.000
```

Diagnosis: open the same URL manually in a browser. If it is also slow, the site (or a third-party script such as analytics) is the issue; report it or accept a longer timeout deliberately. If it is fast manually but slow in the test, check the test environment (a firewall blocking third-party hosts, a VPN).

### Walk-through 4: `StaleElementReferenceException` after navigation

```
org.openqa.selenium.StaleElementReferenceException: stale element reference: stale element not found
```

Diagnosis: you hold a `WebElement` found *before* `refresh()`, `back()`, `forward()`, a link click, or a page redraw. The DOM node it referred to no longer exists. Fix: do not store elements across navigations; store the *locator* (`By`) and call `findElement` again when you need the element. This is another reason to keep locators, not elements, in constants.

### Walk-through 5: the layout is different on CI

Symptom: a click fails with `ElementNotInteractableException` or `NoSuchElementException` only on the build server. Diagnosis: print `driver.manage().window().getSize()` in the CI log. If it is small (for example 800 x 600), the site switched to a compact layout. Fix: set the size explicitly at the start of every test (see the *Browser Options* lesson for headless settings).

---

## Guided Lab: Navigation and History

**Goal:** prove your understanding of history behaviour by predicting, then running, a sequence of navigation calls.

**Step 1.** Create `HistoryLab.java` with this body (add a `try/finally` and `quit()` as in the other examples):

```java
driver.get("https://the-internet.herokuapp.com/");
print(driver, "A");
driver.navigate().to("https://the-internet.herokuapp.com/login");
print(driver, "B");
driver.navigate().to("https://the-internet.herokuapp.com/checkboxes");
print(driver, "C");
driver.navigate().back();
print(driver, "after back");
driver.navigate().back();
print(driver, "after back");
driver.navigate().forward();
print(driver, "after forward");
driver.navigate().to("https://the-internet.herokuapp.com/dropdown");
print(driver, "D");
driver.navigate().forward();
print(driver, "after forward (nothing to go forward to)");
```

and this helper in the same class:

```java
static void print(WebDriver driver, String label) {
    System.out.println(label + " -> " + driver.getCurrentUrl() + " | " + driver.getTitle());
}
```

**Step 2. Predict first.** Before running, write down the URL you expect after each line, using the "cards with a bookmark" model from section 2.

**Step 3. Run and compare.** Expected URL sequence: `/`, `/login`, `/checkboxes`, `/login`, `/`, `/login`, `/dropdown`, `/dropdown` (the last `forward()` does nothing because a new navigation erased the forward history).

**Step 4.** Add `driver.navigate().refresh();` before the last `print`. Confirm the URL does not change but the line still prints.

**Step 5. Window experiment.** Insert before the first `get`:

```java
driver.manage().window().setSize(new Dimension(500, 700));
```

Open `https://www.saucedemo.com`, log in, and compare how the page looks with 500 x 700 versus `maximize()`. Print `driver.manage().window().getSize()` in each case. Note one element whose visibility could differ.

**Step 6. Timeout experiment.** Set `pageLoadTimeout(Duration.ofSeconds(2))` and open `https://httpbin.org/delay/5` inside a `try/catch (TimeoutException e)` that prints a friendly message. Expected output: your message, not a stack trace. (If that site is unreachable from your network, skip this step.)

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| `driver.get("www.site.com")` (no protocol) | `InvalidArgumentException` | Include `https://` |
| Reusing a `WebElement` after `refresh()`/`back()` | `StaleElementReferenceException` | Find the element again after navigation |
| Reading `getCurrentUrl()` right after a JavaScript redirect | Old URL returned intermittently | Use a wait (Tuesday), never `Thread.sleep` |
| Running tests in a small default window | Elements hidden in a mobile layout | `maximize()` or `setSize()` first |
| Calling `maximize()` in headless mode and expecting a large screen | No effect | Use `--window-size` option or `setSize` |
| Using `getPageSource().contains(...)` as a main assertion | Matches hidden/script text, false passes | Locate a visible element and assert on `getText()` |
| Forgetting `quit()` | Orphaned browser processes | `try/finally` |
| Using `close()` as final cleanup | Driver process may survive | `quit()` |
| Expecting `forward()` to work after a new `get()` | Nothing happens | Remember new navigation erases forward history |
| Hard-coding the host name in every test | Cannot run against another environment | Keep a `baseUrl` setting |

---

## Practice Exercises

1. **History walk.** Visit three different pages in a row. Print the URL after each. Use `back()` twice and `forward()` once, printing the URL each time. Predict the output before running.
2. **Login landing check.** On SauceDemo, log in using `standard_user` / `secret_sauce` (you may find the fields using the previous lesson). Then print the URL and verify it contains `inventory`. Next, use `back()` and print the URL again. What do you observe, and why?
3. **Responsive experiment.** Set the window size to 400 x 800, open `https://www.saucedemo.com/inventory.html` after login, and take note of how the layout changes. Then set it to 1366 x 768. Why does this matter for locators?
4. **Timeout test.** Set `pageLoadTimeout` to 1 second and open a slow page (for example `https://httpbin.org/delay/5`). Catch `TimeoutException` and print a clear message. Restore a sensible timeout afterwards.
5. **Compare `get()` and `navigate().to()`.** Measure the elapsed time (use `System.currentTimeMillis()`) for each on the same URL. Are they meaningfully different?
6. **Think:** Why is `getPageSource().contains("Welcome")` a weaker check than locating the heading element and comparing its text?
7. **Negative login.** Write a program that logs in to SauceDemo with a wrong password and prints PASS if the URL did **not** change to the inventory page.
8. **Stale on purpose.** Find the `<h1>` on `https://the-internet.herokuapp.com/` (or `By.tagName("h1")`), call `refresh()`, then call `getText()` on the old reference. Catch `StaleElementReferenceException`, print its name, and then find the element again and print its text.
9. **Window report.** Write a method `static String windowReport(WebDriver d)` that returns text such as `1366 x 768 at (0, 0)` using `getSize()` and `getPosition()`. Call it after `setSize`/`setPosition` and after `maximize()`.
10. **URL checker helper.** Write `static boolean urlEndsWith(WebDriver d, String suffix)` and use it to check three different pages of the-internet site.
11. **Basic auth.** Open `https://admin:admin@the-internet.herokuapp.com/basic_auth` and print the text inside `.example p`. What would happen without the credentials in the URL?
12. **Base URL.** Refactor your login-landing program so the base address comes from `System.getProperty("baseUrl", "https://www.saucedemo.com")`. Run it once with the default and once with `-DbaseUrl=https://www.saucedemo.com/` and confirm that it works either way. Which comparison method (`equals`, `endsWith`) is safer, and why?

---

## Solutions and Hints

**1.** Hint: draw the history cards. After A, B, C: back gives B, back gives A, forward gives B.

**2.** Expected: URL contains `inventory`; after `back()` the app typically returns to the login address (`https://www.saucedemo.com/`). SauceDemo is a single-page app that tracks history itself; the exact outcome (login page or a bounce back to the inventory) depends on the site's current behaviour, so record what you actually see and explain it in terms of the history list.

**3.** At 400 px the layout is compressed and some elements may wrap, shrink or hide, so a locator that finds a visible element at 1366 px might return an element that is not displayed, causing interaction errors. Set a fixed size at the start of tests.

**4.**

```java
driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(1));
try {
    driver.get("https://httpbin.org/delay/5");
} catch (TimeoutException e) {
    System.out.println("Page took longer than 1 second to load");
} finally {
    driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
}
```

Import `org.openqa.selenium.TimeoutException` (not `java.util.concurrent.TimeoutException`).

**5.** Differences are within normal noise; they send the same protocol command.

**6.** The page source contains hidden elements, scripts, comments and attributes, so the word can be present even when the user cannot see it; a heading check proves what the user sees and where.

**7.**

```java
driver.get("https://www.saucedemo.com");
driver.findElement(By.id("user-name")).sendKeys("standard_user");
driver.findElement(By.id("password")).sendKeys("wrong");
driver.findElement(By.id("login-button")).click();
System.out.println(driver.getCurrentUrl().endsWith("/inventory.html") ? "FAIL" : "PASS");
```

**8.**

```java
WebElement h1 = driver.findElement(By.tagName("h1"));
driver.navigate().refresh();
try {
    h1.getText();
} catch (StaleElementReferenceException e) {
    System.out.println("Caught: " + e.getClass().getSimpleName());
}
h1 = driver.findElement(By.tagName("h1"));
System.out.println(h1.getText());
```

**9.**

```java
static String windowReport(WebDriver d) {
    Dimension s = d.manage().window().getSize();
    Point p = d.manage().window().getPosition();
    return s.getWidth() + " x " + s.getHeight() + " at (" + p.getX() + ", " + p.getY() + ")";
}
```

**10.**

```java
static boolean urlEndsWith(WebDriver d, String suffix) {
    return d.getCurrentUrl().endsWith(suffix);
}
```

**11.** Output is `Congratulations! You must have the proper credentials.` Without credentials, Chrome shows a native login popup that Selenium cannot operate, and the page shows an "Not authorized" message once cancelled.

**12.** `endsWith("/inventory.html")` is safer than `equals(...)` because it does not depend on the host name or a trailing slash in the base URL.

---

## Self-Check Q&A

1. **What is the difference between `get(url)` and `navigate().to(url)`?** Practically none; `navigate().to` also has a `URL` overload and belongs to the history API.
2. **What does `navigate().back()` do if there is no history?** Nothing, and no error.
3. **Why do elements become stale after `refresh()`?** The DOM is rebuilt; old element references no longer point to anything.
4. **When does `get()` return by default?** After the browser's `load` event, with a maximum wait set by the page load timeout (default 300 s).
5. **Why set the window size in tests?** Responsive layouts change which elements exist or are visible, so the size must be deterministic.
6. **Why is `getCurrentUrl()` good for detecting redirects?** It returns the final address the browser ended up on.
7. **Which cleanup method ends the session and driver process?** `quit()`.
8. **Why is `Thread.sleep` the wrong answer to timing issues?** It wastes time when the page is fast and still fails when it is slow; waits (Tuesday) respond to the actual page state.

---

## Summary

- `driver.get(url)` and `driver.navigate().to(url)` both load a URL and (by default) wait for the page `load` event; `navigate()` also gives `back()`, `forward()`, and `refresh()`.
- History behaves like a list with a bookmark: a new navigation after `back()` erases the forward pages.
- `getTitle()`, `getCurrentUrl()`, and `getPageSource()` provide information used for simple verifications; prefer visible elements as strong evidence, and avoid timing issues with waits (Tuesday), not sleeps.
- Window methods (`maximize`, `setSize`, `fullscreen`, `minimize`) make the layout deterministic; this matters because responsive pages change their elements.
- After navigation or refresh, previously found elements may become stale; find them again, and keep locators rather than elements.
- `close()` closes one window; `quit()` ends the session. Always `quit()`.
- Always supply the full URL including `https://`; configure a page load timeout to avoid very long hangs; keep the base URL in one setting. These habits go straight into the Project 2 framework.

---

## Additional Resources

- Selenium documentation, *Browser navigation*: https://www.selenium.dev/documentation/webdriver/interactions/navigation/
- Selenium documentation, *Windows and tabs*: https://www.selenium.dev/documentation/webdriver/interactions/windows/
- Selenium documentation, *Page loading strategy*: https://www.selenium.dev/documentation/webdriver/drivers/options/#pageloadstrategy
- Practice sites: https://www.saucedemo.com and https://the-internet.herokuapp.com
