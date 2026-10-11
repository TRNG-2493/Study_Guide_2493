# Waiting Strategies

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **why** automated tests need waits, and describe the "race condition" between your test and the browser.
- Explain why `Thread.sleep()` is a poor solution and what to use instead.
- Configure and explain an **implicit wait**, including how it behaves and its limitations.
- Use **explicit waits** (`WebDriverWait` with `ExpectedConditions`) and write custom conditions with lambdas.
- Use a **fluent wait** with custom timeout, polling interval, and ignored exceptions.
- Distinguish **page load timeout**, **script timeout**, **implicit wait**, and **explicit wait**.
- Explain why mixing implicit and explicit waits is dangerous.
- Handle `StaleElementReferenceException`, `ElementClickInterceptedException`, and `NoSuchElementException` caused by timing.
- Read a `TimeoutException` message and diagnose whether the cause is a wrong locator, a wrong condition, or a genuinely slow page.
- Choose the right wait strategy and build a reusable wait helper for your framework.

---

## Why This Matters

Yesterday you wrote tests that find and click elements. They probably worked on SauceDemo, which is a fast, simple site. Now imagine a real application: after you click "Search", the page shows a spinner for one or two seconds, then the results appear. Your script, however, runs in a few milliseconds. It asks for the results immediately and gets:

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element
```

Yet if you run the test slowly in a debugger, it passes! This is the infamous **flaky test**: sometimes it passes, sometimes it fails, with no change in the code. Flaky tests destroy trust: when a nightly run shows 12 red tests, the team starts to say "oh, they are probably just flaky" and ignores real bugs.

**The vast majority of flaky Selenium tests are timing problems.** Mastering waits is probably the single most important skill that separates a beginner from a reliable automation engineer. This week's Epic is to build a stable test framework and today is the day you learn how to make it stable. The trainee exercise for today (stabilising flaky tests) and the **Project 2 milestone** depend directly on this lesson: by the end of today your Project 2 skeleton should contain a wait helper and a set of tests that no longer contain a single `Thread.sleep`.

### What you already know that this lesson builds on

- From Monday you can start a driver, navigate with `driver.get(url)`, and locate elements with `By` locators such as `By.id`, `By.cssSelector`, and `By.xpath`.
- You know `findElement` returns one `WebElement` or throws `NoSuchElementException`, while `findElements` returns a (possibly empty) list.
- You know `click()`, `sendKeys()` and `getText()` exist. Today we make sure they are called at the **right moment**.

### A real-world story

A QA team at an online shop had 300 UI tests. On their laptops, 295 passed. On the shared build server (slower, many tests running at once), 40 failed every night, and a different 40 each night. Nobody had changed the code. After a week of investigation they discovered that every failure was a test that read the page 100-300 ms before the application had finished drawing it. The fix was not "run on a faster server"; it was to replace guesses with conditions. After adding explicit waits, the failure rate dropped from 13% to under 1%, and the suite also became **faster**, because the long `Thread.sleep` calls were removed. This lesson teaches you to make that same improvement.

---

## The Concept

### 1. The Root Problem: Your Test vs. the Browser

**What it is.** Your test code (Java, running in the JVM) and the web page (JavaScript, running inside the browser) are two separate programs. They do not share a clock and they do not tell each other what they are doing.

**Why it matters.** Selenium's `click()` returns as soon as the click is performed (and, when the click starts a full page navigation, once that navigation completes). If the page then fetches data in the background using JavaScript (AJAX), builds new elements, or runs an animation, Selenium does **not** know and does **not** wait. Modern single-page applications built with React, Angular, or Vue do this constantly.

```
Test code:   click Search ─► find results ─► read results
Browser:     click Search ─► send request ─► (wait for server) ─► render results
                                       ▲
                      the test is already asking for results here
```

This is a **race condition**: whether the test passes depends on who "wins" the race. A **wait** instructs the test to pause *until a condition is true*, up to a maximum time.

> **Analogy:** You order food at a restaurant and, after one second, tell the waiter "this is not on my table, I'm leaving". A good diner waits for the dish, up to a reasonable limit (say 20 minutes), and complains only if it never arrives. Waiting *with a limit and a condition* is the whole idea.

#### Timeline of a race: what actually happens

Suppose the server needs 800 ms to answer. Times are measured from the moment of the click.

| Time | Browser | Your test (no wait) |
|---|---|---|
| 0 ms | Click received, JavaScript sends the request | `click()` returns immediately |
| 2 ms | Spinner shown, results list still empty | `findElement(By.id("results"))` runs |
| 3 ms | (still waiting for server) | **`NoSuchElementException`**, test fails |
| 800 ms | Server replies, results drawn | (test already finished) |

Now the same test on a fast day when the server answers in 1 ms: the results appear at 1 ms, the test looks at 2 ms and passes. **Same code, different outcome.** That is exactly what "flaky" means, and now you can see that the code is not random; the *timing* is.

With a wait, the timeline becomes:

| Time | Browser | Your test (with explicit wait) |
|---|---|---|
| 0 ms | Request sent | `click()` returns, `wait.until(visibility of results)` starts |
| 2 ms | Spinner shown | Poll 1: results not visible, keep waiting |
| 502 ms | (waiting) | Poll 2: not visible, keep waiting |
| 800 ms | Results drawn | |
| 1002 ms | | Poll 3: results visible, `until` returns the element, test continues |

The test waits only as long as it needs to (about 1 second here) and never longer than the limit you set.

### 2. The Bad Solution: `Thread.sleep()`

**What it is.** `Thread.sleep(milliseconds)` is a standard Java method that freezes the current thread (your test) for a fixed time. It has nothing to do with Selenium and knows nothing about the page.

```java
driver.findElement(By.id("search-btn")).click();
Thread.sleep(5000);                      // wait 5 seconds, no matter what
driver.findElement(By.id("results"));
```

Line by line:

- Line 1 finds the Search button and clicks it.
- Line 2 `Thread.sleep(5000)` pauses for exactly 5000 milliseconds. It also forces you to handle a checked `InterruptedException` (add `throws InterruptedException` to the method or wrap in try/catch), which clutters your code.
- Line 3 looks for the results, hoping five seconds was enough.

Problems:

| Problem | Explanation |
|---|---|
| **Too slow** | If the results appear after 0.3 s, you still waste 4.7 s. Across 500 tests, that is over 40 minutes. |
| **Still flaky** | If the server is slow today and needs 6 s, the test fails anyway. |
| **Hides problems** | A fixed number is a guess; nobody knows why "5" was chosen. |
| **Maintenance** | Teams end up multiplying sleeps "just to be safe". |

**Worked arithmetic.** A suite of 200 tests, each with three `Thread.sleep(3000)` calls, wastes 200 x 3 x 3 s = 1,800 s = **30 minutes** in every run, even when nothing is slow. If it runs on every code commit, 10 times a day, that is 5 hours of pure waiting per day.

Occasionally, `Thread.sleep` is acceptable for *debugging* (to watch what the browser is doing) or in very rare cases where no condition can be observed. In real test code, **do not use it**. Smart waits poll the page and continue **as soon as the condition is true**.

> **Analogy:** `Thread.sleep` is like setting an oven timer for one hour for every dish, whether it is toast or a roast. A smart wait is like looking through the oven window and taking the dish out the moment it is ready.

### 3. Timeouts at a Glance

Selenium has several different timeouts. Beginners confuse them, so here is the whole picture:

| Timeout | Controls | Default | Set with |
|---|---|---|---|
| **Page load timeout** | How long `get()`/`navigate()` may wait for page load | 300 s | `driver.manage().timeouts().pageLoadTimeout(Duration)` |
| **Script timeout** | How long an asynchronous script may run | 30 s | `driver.manage().timeouts().scriptTimeout(Duration)` |
| **Implicit wait** | How long `findElement(s)` retries to find an element | 0 s (disabled) | `driver.manage().timeouts().implicitlyWait(Duration)` |
| **Explicit wait** | How long to wait for a *specific condition* | none until you create one | `new WebDriverWait(driver, Duration)` |
| **Fluent wait** | An explicit wait with custom polling and ignored exceptions | none | `new FluentWait<>(driver)` |

All Selenium 4 timeouts use `java.time.Duration`. (Older Selenium 3 code used `(long, TimeUnit)`; if you see `implicitlyWait(10, TimeUnit.SECONDS)` in an old tutorial, it is deprecated.)

**Reading `Duration`.** `Duration` is a Java class that represents an amount of time. `Duration.ofSeconds(10)` means ten seconds; `Duration.ofMillis(250)` means a quarter of a second. You need `import java.time.Duration;` at the top of the file.

**Setting the two non-wait timeouts** (usually right after creating the driver):

```java
WebDriver driver = new ChromeDriver();
driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(45));
driver.manage().timeouts().scriptTimeout(Duration.ofSeconds(20));
```

- `driver.manage()` returns an `Options` object that controls settings of the browser session.
- `.timeouts()` returns the `Timeouts` object that holds all timeout settings.
- `.pageLoadTimeout(...)` says: if `driver.get(...)` has not finished loading within 45 s, throw a `TimeoutException`. This protects your suite from a hung page; the default of five minutes is far too long.
- `.scriptTimeout(...)` applies to `executeAsyncScript`, a JavaScript feature you will rarely need now.

**When do you meet each?** You will set the page load timeout once in your driver setup. You will use implicit waits only when reading older code. You will write explicit waits every day.

### 4. Implicit Wait

An **implicit wait** tells the driver: *"whenever you look for an element and do not find it, keep trying for up to N seconds before giving up."*

```java
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
```

Key behavior:

- It is set **once per driver session** (usually right after creating the driver) and applies to **every** `findElement` and `findElements` call afterwards.
- The driver polls (roughly every 250-500 ms) and returns the element **as soon as it appears**. If the element appears after 2 s, you do not wait for the remaining 8 s.
- If the element never appears within 10 s, `NoSuchElementException` is thrown.
- `findElements` with an implicit wait: waits until **at least one** element is found, or returns an empty list after the timeout. That means checking for absence can cost the **full** timeout.

```java
WebDriver driver = new ChromeDriver();
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));

driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
driver.findElement(By.cssSelector("#start button")).click();

// The text appears after ~5 seconds. The implicit wait polls until it exists.
String text = driver.findElement(By.id("finish")).getText();
System.out.println(text);   // Hello World!
```

#### What happens when each line runs

1. `new ChromeDriver()` starts Chrome. At this point implicit wait is 0: any missing element fails instantly.
2. `implicitlyWait(Duration.ofSeconds(10))` sends a command to the driver: "from now on, `find` calls may retry for 10 s." Nothing visibly happens.
3. `driver.get(...)` loads the page. On `/dynamic_loading/2` the "Hello World!" element does not exist yet.
4. `findElement(By.cssSelector("#start button"))` finds the Start button immediately (it is already on the page) and `click()` presses it. The page now shows a loading bar for several seconds.
5. `findElement(By.id("finish"))` does not find the element at once. Instead of failing, the driver retries every few hundred milliseconds. About five seconds later the element appears, the driver returns it, and `getText()` reads "Hello World!". If the page had been broken and the element never appeared, you would get `NoSuchElementException` after exactly 10 s.

**Advantages:** extremely simple; one line fixes many failures.

**Limitations:**

1. It only waits for **presence in the DOM**. An element can exist but be invisible, disabled, or covered by an overlay. The next `click()` can then fail even though `findElement` succeeded.
2. It is **global**: a single value for every lookup in the session. Some elements need 2 s, others 30 s; one number does not fit all.
3. It slows down negative checks (asserting that something is *not* there).
4. It cannot wait for conditions such as "text changed", "URL contains", "alert present", or "element is clickable".

#### Case study: where the implicit wait silently fails

Open `https://the-internet.herokuapp.com/dynamic_loading/1`. In this variant, the "Hello World!" element is **already in the HTML but hidden** (`display: none`) and is only made visible after the loading bar. Now repeat the code above with the implicit wait:

```java
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");
driver.findElement(By.cssSelector("#start button")).click();
String text = driver.findElement(By.id("finish")).getText();
System.out.println("[" + text + "]");     // prints [] (empty!)
```

The implicit wait is satisfied immediately because the element is **present**. But `getText()` returns only *visible* text, so you get an empty string and a failing assertion later. This is the most important limitation to remember: **implicit waits wait for existence, not for readiness.** An explicit wait for visibility solves both pages with the same code.

**The cost of checking absence.** With a 10-second implicit wait, this line takes a full 10 seconds when the element really is not there:

```java
boolean gone = driver.findElements(By.id("spinner")).isEmpty();
```

because the driver keeps retrying hoping the element will show up. Multiply by many assertions and the suite crawls.

Because of these limits, professional frameworks prefer explicit waits.

### 5. Explicit Wait: `WebDriverWait` and `ExpectedConditions`

An **explicit wait** waits for a **specific condition** on a **specific element**, for a maximum time that you choose for that situation.

```java
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

WebElement results = wait.until(
        ExpectedConditions.visibilityOfElementLocated(By.id("finish")));
```

How it works:

1. `new WebDriverWait(driver, Duration.ofSeconds(10))` creates a waiter with a 10-second limit. It polls **every 500 ms by default**.
2. `wait.until(condition)` evaluates the condition repeatedly.
3. When the condition returns a "truthy" value (a non-null object or `true`), `until` returns that value immediately. Here, the located `WebElement`.
4. If the time runs out, it throws a `TimeoutException` whose message explains what was awaited.

Create **one** `WebDriverWait` object and reuse it for many `until` calls.

#### Vocabulary for beginners

- **Condition:** a yes/no question about the page ("is the element visible?"). In Selenium it is an object with a method that returns a value or `false`/`null`.
- **Polling:** asking the question again and again at regular intervals.
- **Timeout:** the maximum total time you are willing to keep asking.
- **`ExpectedConditions`:** a ready-made toolbox of common conditions. Every method in it is `static`, so you call it as `ExpectedConditions.something(...)` without creating an object.

#### Walk-through: the life of one `until` call

```java
WebElement msg = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("message")));
```

1. Java first runs the inner part: `ExpectedConditions.visibilityOfElementLocated(By.id("message"))` does **not** look at the page. It only builds a condition object that remembers the locator.
2. `wait.until(...)` records the start time and runs the condition for the first time. The condition calls `driver.findElement(By.id("message"))`. If the element does not exist, the resulting `NoSuchElementException` is caught and ignored; if it exists but is hidden, the condition returns `null`.
3. `until` sees "not truthy", sleeps for the polling interval (500 ms), and runs the condition again.
4. When the element exists **and** is displayed, the condition returns that `WebElement`; `until` returns it at once to your variable `msg`.
5. If 10 s pass first, `until` throws `TimeoutException` and your test fails with a useful message.

#### Commonly used `ExpectedConditions`

| Condition | Waits until... | Returns |
|---|---|---|
| `visibilityOfElementLocated(By)` | The element is present **and visible** | `WebElement` |
| `visibilityOf(WebElement)` | An already-found element becomes visible | `WebElement` |
| `presenceOfElementLocated(By)` | The element exists in the DOM (even if hidden) | `WebElement` |
| `elementToBeClickable(By)` / `(WebElement)` | The element is visible **and enabled** | `WebElement` |
| `invisibilityOfElementLocated(By)` | The element is gone or hidden (great for spinners) | `Boolean` |
| `visibilityOfAllElementsLocatedBy(By)` | All matching elements are visible | `List<WebElement>` |
| `presenceOfAllElementsLocatedBy(By)` | At least one matching element exists | `List<WebElement>` |
| `textToBePresentInElementLocated(By, String)` | The element's text contains the string | `Boolean` |
| `textToBe(By, String)` | The element's text equals the string exactly | `Boolean` |
| `attributeToBe(By, attr, value)` | An attribute has a given value | `Boolean` |
| `urlContains(String)` / `urlToBe(String)` | The current URL matches | `Boolean` |
| `titleIs(String)` / `titleContains(String)` | The title matches | `Boolean` |
| `stalenessOf(WebElement)` | An old element has been removed/replaced | `Boolean` |
| `numberOfElementsToBe(By, int)` | Exactly N elements match | `List<WebElement>` |
| `frameToBeAvailableAndSwitchToIt(...)` | An iframe is available (and switches into it) | `WebDriver` |
| `alertIsPresent()` | A JavaScript alert appears | `Alert` (covered Wednesday) |

> **Presence vs. visibility vs. clickability**, the trio that matters most:
>
> - **Presence:** exists in the HTML (could be hidden).
> - **Visibility:** exists and has a size greater than zero and is not `display:none`/`visibility:hidden`; the user can see it.
> - **Clickable:** visible *and* enabled. Note that it does **not** guarantee that nothing is covering it (an overlay can still intercept the click).

**Use the right one:** wait for `elementToBeClickable` before clicking, `visibilityOfElementLocated` before reading text, and `invisibilityOfElementLocated` for loading indicators.

**When to use which, with scenarios:**

| Scenario | Best condition | Why |
|---|---|---|
| Click "Login" on SauceDemo | `elementToBeClickable(By.id("login-button"))` | You are about to click |
| Read the error banner after bad login | `visibilityOfElementLocated(By.cssSelector("[data-test='error']"))` | You need visible text |
| Check a hidden `<input type="hidden">` value | `presenceOfElementLocated` | It is never visible, so visibility would time out |
| Wait for a "Saving..." overlay to finish | `invisibilityOfElementLocated` | You are waiting for something to go away |
| Search results list reloaded | `visibilityOfAllElementsLocatedBy` | You need all rows ready |
| After login, confirm you reached the products page | `urlContains("inventory")` | The URL is the evidence |

#### Example: the "dynamic loading" page

```java
WebDriver driver = new ChromeDriver();
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
try {
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");

    wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("#start button"))).click();

    // 1) wait for the loading bar to disappear
    wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id("loading")));

    // 2) wait for the result to be visible, then read it
    String message = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.id("finish"))).getText();

    System.out.println("Message: " + message);
} finally {
    driver.quit();
}
```

Notice that `until(...)` **returns** the element, so you can chain `.click()` or `.getText()` directly. This is the most common idiom.

Line by line:

- `new WebDriverWait(driver, Duration.ofSeconds(15))` creates the waiter with a 15 s limit (the page's loading bar takes about 5 s, so 15 s is a comfortable margin).
- `try { ... } finally { driver.quit(); }` guarantees the browser closes even if a wait times out. Without it a failing test leaves a Chrome window and a driver process running.
- The first `wait.until(...elementToBeClickable...).click()` waits for the Start button to be usable and then clicks it; the returned element is clicked immediately.
- `invisibilityOfElementLocated(By.id("loading"))` blocks until the loading bar is hidden or removed. We ignore the `Boolean` it returns.
- `visibilityOfElementLocated(By.id("finish")).getText()` waits for the result to show and reads it. Because step 2 already waited for the spinner, this wait usually returns on its first poll.

#### Custom conditions with lambdas

`ExpectedConditions` cannot cover everything. In Selenium 4, `until` accepts any `Function<WebDriver, T>`, so you can write your own condition as a lambda:

```java
// Wait until the cart badge shows "3"
wait.until(d -> d.findElement(By.className("shopping_cart_badge")).getText().equals("3"));

// Wait until there are at least 5 product cards
wait.until(d -> d.findElements(By.className("inventory_item")).size() >= 5);

// Wait until JavaScript reports that the document is fully loaded
wait.until(d -> ((JavascriptExecutor) d)
        .executeScript("return document.readyState").equals("complete"));
```

Reading the lambda: `d -> condition` means "given the driver `d`, return the condition's result". `until` re-runs it every 500 ms; `false` or `null` means "not yet".

Explanation of each example:

- **Cart badge:** `d` is the driver Selenium passes in. `d.findElement(...)` may throw `NoSuchElementException` while the badge does not exist yet (that is ignored by default), then `getText().equals("3")` returns `true` or `false`.
- **At least five cards:** `findElements` never throws; it returns a list. `size() >= 5` is `false` until enough cards exist.
- **`document.readyState`:** `JavascriptExecutor` lets Java run JavaScript in the page; the cast `(JavascriptExecutor) d` tells Java that `d` supports that. `readyState` becomes `"complete"` when the browser has finished loading the page. This is a good extra check for older, non-SPA pages.

A custom message makes failures easier to understand:

```java
wait.withMessage("Cart badge never reached 3 items")
    .until(d -> d.findElement(By.className("shopping_cart_badge")).getText().equals("3"));
```

`withMessage` stores text that is added to the `TimeoutException` if the wait expires, so that the report says *what you were waiting for* instead of just "Expected condition failed".

**Writing a reusable named condition.** If you use the same custom condition in several tests, create a method that returns it:

```java
public static Function<WebDriver, Boolean> cartCountIs(int expected) {
    return d -> {
        List<WebElement> badges = d.findElements(By.className("shopping_cart_badge"));
        if (expected == 0) {
            return badges.isEmpty();            // badge disappears when cart is empty
        }
        return !badges.isEmpty() && badges.get(0).getText().equals(String.valueOf(expected));
    };
}

// usage
wait.until(cartCountIs(2));
```

Here `Function<WebDriver, Boolean>` (from `java.util.function.Function`) is the type of "a thing that takes a driver and answers true/false". The method builds the lambda; the block body `{ ... }` allows several lines and needs an explicit `return`. Note the special case for zero: on SauceDemo the badge element is removed when the cart is empty, so we test for an empty list instead of text.

#### What does `WebDriverWait` ignore?

By default, `WebDriverWait` ignores `NotFoundException` (the parent of `NoSuchElementException`) while polling, which is why `visibilityOfElementLocated` works for elements that do not exist yet. If you need it to tolerate other exceptions, use `.ignoring(...)`:

```java
wait.ignoring(StaleElementReferenceException.class)
    .until(ExpectedConditions.elementToBeClickable(By.id("save")));
```

Any exception that is **not** on the ignore list immediately ends the wait and is thrown to your test. For example, a typo in a CSS selector produces `InvalidSelectorException`, which is not ignored, so you see the real problem straight away instead of waiting 10 s.

### 6. Fluent Wait

A **fluent wait** is the more configurable parent of `WebDriverWait`. You choose:

- the **maximum time** (`withTimeout`),
- the **polling interval** (`pollingEvery`),
- which **exceptions to ignore** (`ignoring`),
- a **timeout message** (`withMessage`).

```java
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.Wait;

Wait<WebDriver> fluentWait = new FluentWait<>(driver)
        .withTimeout(Duration.ofSeconds(30))
        .pollingEvery(Duration.ofMillis(250))
        .ignoring(NoSuchElementException.class, StaleElementReferenceException.class)
        .withMessage("The results table never appeared");

WebElement table = fluentWait.until(d -> d.findElement(By.id("results-table")));
```

Line by line:

- `new FluentWait<>(driver)` creates the waiter around the driver. The `<>` ("diamond") lets Java infer the type `WebDriver`.
- `.withTimeout(...)` sets the maximum: 30 s.
- `.pollingEvery(...)` sets the check interval: every 250 ms instead of 500 ms.
- `.ignoring(A.class, B.class)` lists exception types to swallow during polling. The `.class` suffix is how Java refers to the type itself.
- `.withMessage(...)` is the failure text.
- The result is stored in a variable of type `Wait<WebDriver>`, the interface shared by `FluentWait` and `WebDriverWait`.
- `fluentWait.until(d -> d.findElement(...))` runs the lambda until it returns a non-null value. Here the lambda returns the element itself, so no extra `true/false` is needed: finding it **is** the success.

When to prefer `FluentWait`:

- A slow operation (report generation) for which polling every 500 ms is wasteful; poll every 2 s instead.
- A very quick UI for which 500 ms is too coarse; poll every 100 ms.
- You need to ignore several exception types.

> `WebDriverWait` **is** a `FluentWait` with sensible defaults (500 ms polling, ignoring `NotFoundException`). Use `WebDriverWait` normally; reach for `FluentWait` when you need tuning.

**Choosing between them:**

| Situation | Choose |
|---|---|
| 95% of everyday waits | `WebDriverWait` |
| Need a non-default poll rate | `FluentWait` (or `WebDriverWait` with `.pollingEvery(...)`, which it inherits) |
| Need to ignore `StaleElementReferenceException` only in one place | `WebDriverWait(...).ignoring(...)` |
| Wait for a non-driver object (e.g. a file or API response) | `FluentWait<File>` or `FluentWait<String>`; the generic type is whatever you pass in |

### 7. Implicit vs. Explicit: Do Not Mix Them

The Selenium documentation explicitly warns: **do not mix implicit and explicit waits.** Because the implicit wait is applied inside every `findElement` call, and the explicit wait calls `findElement` repeatedly while polling, the timeouts can combine in surprising ways. For example, an implicit wait of 10 s and an explicit wait of 10 s can make a failing condition take 20 s or more to time out, and the behavior varies between drivers.

**Why does this happen? A walk-through.** You set implicit = 10 s and explicit = 10 s, then wait for an element that never appears:

1. `until` starts its 10 s clock and runs the condition; the condition calls `findElement`.
2. `findElement` does not fail at once; the implicit wait makes it retry for up to 10 s inside that **one** call.
3. After those 10 s, `findElement` throws `NoSuchElementException`, which `until` ignores. But 10 s have now passed, so the explicit limit is nearly reached; `until` runs one more poll (another 10 s inside `findElement`) before checking the clock and giving up.
4. Total: around 20 s, not the 10 s you asked for. Your 3-second "quick check" with a 10 s implicit wait could take 10 s per attempt.

| | Implicit | Explicit |
|---|---|---|
| Scope | Global, all `find` calls | Specific condition, specific place |
| Conditions | Only "element present" | Many: visible, clickable, text, URL, custom... |
| Configuration | One timeout | Different timeouts per situation |
| Failure message | Generic `NoSuchElementException` | Clear `TimeoutException` explaining the condition |
| Recommended in frameworks | Not recommended | **Recommended** |

**Practical rule for this course:** learn the implicit wait because you will meet it in existing code and interviews, but **in your own framework use explicit waits and leave the implicit wait at 0.** If you inherit a project that already sets an implicit wait, a safe migration is to set it back to `Duration.ZERO` in a single place and replace failing lookups with explicit waits one at a time.

### 8. Waits and Typical Exceptions

| Exception | Timing-related cause | Smart-wait fix |
|---|---|---|
| `NoSuchElementException` | Element not yet in DOM | `presenceOfElementLocated` / `visibilityOfElementLocated` |
| `ElementNotInteractableException` | Element exists but is hidden/disabled/not yet animated into place | `elementToBeClickable` |
| `ElementClickInterceptedException` | Another element (overlay, spinner, cookie banner) covers the target | `invisibilityOfElementLocated(overlay)` then click |
| `StaleElementReferenceException` | DOM was rebuilt; your old reference is dead | Re-locate; or `stalenessOf(old)` then find again |
| `TimeoutException` | Your wait ran out | Inspect: wrong locator? Condition never true? Timeout too short? |

**Stale element pattern:** if a click triggers a re-render of a list, wait for the old element to go stale, then find the fresh one:

```java
WebElement oldRow = driver.findElement(By.cssSelector("tr.row"));
driver.findElement(By.id("refresh")).click();
wait.until(ExpectedConditions.stalenessOf(oldRow));
WebElement newRow = wait.until(
        ExpectedConditions.visibilityOfElementLocated(By.cssSelector("tr.row")));
```

Line by line: line 1 stores a reference to the current row. Line 2 triggers a refresh that throws the old rows away and builds new ones. Line 3 waits until the saved reference is "stale" (its element is no longer attached to the page), which proves the refresh really happened. Line 4 then locates the new row by locator, getting a fresh reference. Skipping line 3 is a classic bug: you might grab the *old* row a moment before it is replaced and then fail with stale-element errors.

> **Analogy for "stale":** your saved `WebElement` is like a photo of a house. If the house is demolished and rebuilt, the photo still exists, but it no longer points at a real house. Selenium throws `StaleElementReferenceException` when you try to use the photo.

#### Troubleshooting walk-throughs

**Case 1: `NoSuchElementException` right after a click.**

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: {"method":"css selector","selector":"#finish"}
```

Diagnosis: (1) Is the locator right? Test it in DevTools console with `document.querySelector("#finish")` after the page finishes. (2) If it works there, the element simply arrives late: add `visibilityOfElementLocated`. If it never works, fix the locator; do not increase the wait.

**Case 2: `TimeoutException` after your wait.**

```
org.openqa.selenium.TimeoutException: Expected condition failed: waiting for visibility of element located by By.id: finish (tried for 10 second(s) with 500 milliseconds interval)
```

Read it like a sentence: *what* it waited for (visibility of `By.id: finish`), *how long* (10 s), *how often* (500 ms). Possible causes: wrong locator; element exists but never becomes visible (check for `display:none` or an iframe); a real application bug; or a timeout genuinely too short.

**Case 3: `ElementClickInterceptedException`.**

```
org.openqa.selenium.ElementClickInterceptedException: element click intercepted: Element <button id="save"> is not clickable at point (640, 380). Other element would receive the click: <div class="modal-backdrop fade show"></div>
```

Diagnosis: the second sentence names the culprit, a modal backdrop. The button was "clickable" by Selenium's rules (visible and enabled), but another element is on top. Fix: wait for the overlay to disappear, then click.

```java
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.cssSelector(".modal-backdrop")));
wait.until(ExpectedConditions.elementToBeClickable(By.id("save"))).click();
```

**Case 4: `StaleElementReferenceException` in a loop.**

```
org.openqa.selenium.StaleElementReferenceException: stale element reference: stale element not found
```

Typical cause: you saved a list of elements, clicked one (which re-rendered the list), and then used the next saved element. Fix: do not keep element references across actions that change the page; re-find by locator each time (for example, by index: `driver.findElements(By.cssSelector(".item")).get(i)`).

#### Spinner and overlay patterns

Many real sites show a full-screen loading layer. A robust click helper waits for it first:

```java
public void clickWhenReady(By target) {
    // 1) overlay gone (wait returns true immediately if it never existed)
    wait.until(ExpectedConditions.invisibilityOfElementLocated(By.cssSelector(".loading-overlay")));
    // 2) target ready
    wait.until(ExpectedConditions.elementToBeClickable(target)).click();
}
```

`invisibilityOfElementLocated` returns `true` both when the element is hidden and when it is not in the page at all, so it is safe even if the overlay never appears. One subtle race: if you check **before** the overlay has appeared, you pass instantly and then the overlay arrives. For such sites, first wait for it to appear (short timeout), then for it to disappear, or wait for a visible result that only exists when loading is finished.

#### Quick form scenario: SauceDemo checkout

On `https://www.saucedemo.com`, after `login-button` is clicked the products page loads. Even on this fast site it is a good habit to confirm the new state before acting:

```java
wait.until(ExpectedConditions.urlContains("inventory"));
wait.until(ExpectedConditions.elementToBeClickable(By.id("add-to-cart-sauce-labs-backpack"))).click();
wait.until(ExpectedConditions.textToBe(By.className("shopping_cart_badge"), "1"));
```

Each action is followed by a check on the *effect* of that action: URL after login, badge text after adding an item. This "act, then wait for evidence" rhythm is the core habit of stable tests.

### 9. Build a Reusable Wait Helper

In a framework you do not want `new WebDriverWait(...)` scattered everywhere. A small helper class keeps the timeout in one place:

```java
package com.revature.qea.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

public class WaitUtils {

    private static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(10);

    private final WebDriver driver;
    private final WebDriverWait wait;

    public WaitUtils(WebDriver driver) {
        this(driver, DEFAULT_TIMEOUT);
    }

    public WaitUtils(WebDriver driver, Duration timeout) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, timeout);
    }

    public WebElement visible(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    public WebElement clickable(By locator) {
        return wait.until(ExpectedConditions.elementToBeClickable(locator));
    }

    public void click(By locator) {
        clickable(locator).click();
    }

    public void type(By locator, String text) {
        WebElement element = visible(locator);
        element.clear();
        element.sendKeys(text);
    }

    public String textOf(By locator) {
        return visible(locator).getText();
    }

    public boolean disappears(By locator) {
        return wait.until(ExpectedConditions.invisibilityOfElementLocated(locator));
    }

    public List<WebElement> allVisible(By locator) {
        return wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(locator));
    }

    public void waitForUrlContains(String fragment) {
        wait.until(ExpectedConditions.urlContains(fragment));
    }
}
```

Usage:

```java
WaitUtils waitUtils = new WaitUtils(driver);
waitUtils.type(By.id("user-name"), "standard_user");
waitUtils.type(By.id("password"), "secret_sauce");
waitUtils.click(By.id("login-button"));
waitUtils.waitForUrlContains("inventory");
```

Explaining the design:

- `package com.revature.qea.utils;` places the class in a package; match it to your own Maven folder structure (`src/main/java/com/revature/qea/utils/` or the test source folder).
- `private static final Duration DEFAULT_TIMEOUT` is a constant: `static` (one copy for the class), `final` (cannot change). Constants avoid "magic numbers".
- Two constructors: the first uses the default and delegates with `this(driver, DEFAULT_TIMEOUT)`; the second lets a test choose a custom timeout (for example `new WaitUtils(driver, Duration.ofSeconds(60))` for a slow export page).
- Each method wraps **one** wait idea and returns the element, so callers stay short.
- `type` waits for visibility, clears old text, and types; this prevents "text appended to existing value" bugs.
- The `driver` field is stored for future helpers (for example, taking a screenshot on timeout); currently only `wait` is used.

This helper is a perfect piece for the **Project 2 milestone** today. On Wednesday you will see how to place helpers like this at the base of the Page Object Model (helper classes that become the foundation of page objects).

**Extension: friendlier failures.** Wrap the wait so that a timeout also saves a screenshot (you learned screenshots on Monday):

```java
public WebElement visible(By locator) {
    try {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    } catch (TimeoutException e) {
        // e.g. ScreenshotUtils.capture(driver, "timeout-" + locator);  (your Monday helper)
        throw e;   // rethrow: the test must still FAIL
    }
}
```

The `catch` is used to **add information**, then the exception is thrown again with `throw e;`. Never swallow it.

### 10. Choosing the Right Wait: A Decision Guide

1. Waiting for a **page to load after a navigation** -> Selenium already waits (page load strategy); confirm with `urlContains` or the presence of a key element.
2. Waiting for **an element to appear** -> `visibilityOfElementLocated`.
3. About to **click** -> `elementToBeClickable`.
4. Waiting for a **spinner/overlay to disappear** -> `invisibilityOfElementLocated`.
5. Waiting for **text or attribute changes** -> `textToBe...` or a custom lambda.
6. **Unusual polling** needs -> `FluentWait`.
7. **Never** -> `Thread.sleep` as your normal strategy, or implicit + explicit together.

### 11. Choosing Timeout Values

- Start with **10 seconds** as a default for explicit waits. It is long enough for most pages and short enough that a real failure is reported promptly.
- Use longer waits (30-60 s) only for known slow operations (file export, report generation), as a **separate** wait object.
- The timeout is a *maximum*, not a delay. A generous timeout costs nothing when the page is fast; it only matters when something is genuinely broken.
- Store timeouts in configuration (a properties file) so they can change per environment: a slow test environment may need a larger value than production.

**Diagnosing a flaky test: a checklist.**

1. Re-run it 10 times. Does it fail at the **same line** each time? (Same line suggests a timing gap at that line.)
2. Read the exception name (table in section 8).
3. Ask: "What does the page do between my previous step and this one?" (AJAX, animation, redirect, spinner.)
4. Add a wait for the **evidence** of that work, not for time.
5. Re-run 20 times. A fix is credible only if it passes repeatedly, including when you throttle the browser (DevTools Network tab, "Slow 3G").

---

## Hands-On Example: Making a Flaky Test Stable

**The flaky version** (fails on a slow day):

```java
driver.get("https://the-internet.herokuapp.com/dynamic_controls");
driver.findElement(By.cssSelector("#checkbox-example button")).click();   // "Remove"
String msg = driver.findElement(By.id("message")).getText();              // may not exist yet!
System.out.println(msg);
```

The "Remove" button triggers an AJAX call; the message "It's gone!" appears about a second later.

**The stable version:**

```java
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

driver.get("https://the-internet.herokuapp.com/dynamic_controls");

wait.until(ExpectedConditions.elementToBeClickable(
        By.cssSelector("#checkbox-example button"))).click();

// wait for the loading indicator to vanish
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id("loading")));

String msg = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("message"))).getText();
System.out.println(msg);   // It's gone!

// the checkbox itself should now be gone from the DOM
wait.until(ExpectedConditions.numberOfElementsToBe(By.id("checkbox"), 0));
```

What changed: every action that depends on the page being ready is preceded by a wait for the specific condition. The test is now both **faster** (no sleeps) and **more reliable**.

### Guided Lab: Stabilise a Flaky Test (about 40 minutes)

**Goal:** turn a failing test into a passing, repeatable one and measure the improvement.

1. In your Project 2 Maven project, create a class `DynamicControlsTest` with a `main` method (or a test method if you already have JUnit; JUnit and Maven integration are covered Friday, so a `main` is fine today).
2. Start a `ChromeDriver`, navigate to `https://the-internet.herokuapp.com/dynamic_controls`, and paste the **flaky** version above. Wrap everything in `try/finally` with `driver.quit()`.
3. Run it. **Expected output:** an exception such as `NoSuchElementException: ... selector "#message"` (it may occasionally pass on a very fast machine; run three times).
4. Replace the code with the **stable** version. Add timing code before and after:
   ```java
   long start = System.currentTimeMillis();
   // ... waits and actions ...
   System.out.println("Took " + (System.currentTimeMillis() - start) + " ms");
   ```
5. Run it again. **Expected output:**
   ```
   It's gone!
   Took 1900 ms
   ```
   (your number will vary between roughly 1,500 and 3,500 ms, including page load).
6. Add a second part: click "Add" (`#checkbox-example button` now reads "Add"), wait for `message` to read "It's back!" using `textToBe(By.id("message"), "It's back!")`, and then verify `driver.findElement(By.id("checkbox")).isDisplayed()` is `true`.
7. Move the `WebDriverWait` creation into `WaitUtils` and rewrite the script using `waitUtils.click(...)` and `waitUtils.textOf(...)`.
8. Replace one wait with a deliberately wrong locator (`By.id("mesage")`) and a timeout of 3 s. **Expected:** after about 3 s a `TimeoutException` whose text names `By.id: mesage`. Fix the typo and confirm green.

If your numbers differ or step 3 does not fail, that is normal: flaky tests are timing dependent. What matters is that the stable version passes every time.

---

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| `Thread.sleep(5000)` everywhere | Slow and still flaky | Use explicit waits |
| Setting implicit wait **and** explicit waits | Unpredictable timeouts | Choose explicit; keep implicit at 0 |
| Waiting for presence, then clicking | Element may be hidden/disabled | `elementToBeClickable` |
| Creating `new WebDriverWait` with a tiny timeout (1-2 s) | Fails on normal slow responses | Start at 10 s |
| Passing a `WebElement` found earlier into `until(...)` after the page re-renders | Stale reference | Wait on a **locator** (`By`) so it is re-evaluated every poll |
| Catching `TimeoutException` and ignoring it | Test passes when it should fail | Let it fail, or assert explicitly |
| Using a wait to hide a wrong locator | Always times out after 10 s | Verify the locator in DevTools first |
| Setting a huge page load timeout | A hung page blocks the suite for minutes | 30-60 s is usually enough |
| Waiting for visibility of a hidden input | Always times out | Use `presenceOfElementLocated` |
| Writing `wait.until(d -> element.isDisplayed())` with a stored `element` | Uses the same (possibly stale) reference every poll | Locate inside the lambda: `d.findElement(...).isDisplayed()` |

---

## Practice Exercises

Use https://the-internet.herokuapp.com for these.

1. **Flaky on purpose.** Open `/dynamic_loading/1` and `/dynamic_loading/2`. Click Start and read the "Hello World!" text **without** any wait. Observe the exception. Then fix it with (a) an implicit wait, and (b) an explicit wait. Describe the difference in how each fix reads. (Hint: try the implicit fix on page 1 too.)
2. **Timing measurement.** Use `System.currentTimeMillis()` to measure how long the explicit wait actually waited. Compare to a `Thread.sleep(10000)` version.
3. **Conditions tour.** On `/dynamic_controls`, use explicit waits to: (a) click Remove and wait for the message, (b) click Add and wait for the checkbox to be present again, (c) click "Enable" for the text box and wait until it `isEnabled()`, using both `elementToBeClickable` and a custom lambda.
4. **Fluent wait.** Rewrite one of the above with `FluentWait` polling every 200 ms and ignoring `NoSuchElementException`. Add a `withMessage`.
5. **Provoke a timeout.** Wait for an element that does not exist using a 3 s `WebDriverWait`. Read the `TimeoutException` message carefully; what information does it give?
6. **Overlay problem.** Try to click an element while a loading indicator covers it. What exception do you get? Fix it by waiting for the indicator to become invisible.
7. **Mixing waits experiment.** Set an implicit wait of 10 s and an explicit wait of 10 s, then wait for a condition that never becomes true. Measure how long until the exception is thrown, and explain why this is a problem.
8. **Build `WaitUtils`.** Create the helper class from this lesson in your Project 2 skeleton and refactor Monday's login script to use it.
9. **Custom condition.** On SauceDemo, add three different items to the cart and use a custom lambda (or a `cartCountIs` method) to wait for the badge to show `3`.
10. **Stale element.** On `/dynamic_content` (content changes on refresh), save the first paragraph element, click the "click here" link, and use `stalenessOf` to confirm the page re-rendered. First reproduce `StaleElementReferenceException` by using the old element.
11. **Project 2 milestone.** Take two existing Project 2 tests that use `Thread.sleep` or are flaky. Replace every sleep with a condition-based wait, run each test 10 times, and record pass counts before and after in your notes.

---

## Solutions and Hints

**Exercise 1.** On page 2, both fixes work. On page 1 the implicit wait fails (empty text), because `#finish` is already in the DOM but hidden; the explicit wait for visibility works for both. Hint: print `"[" + text + "]"`.

```java
// (b) explicit, works on both pages
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
driver.findElement(By.cssSelector("#start button")).click();
System.out.println(wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish"))).getText());
```

**Exercise 2.**

```java
long t0 = System.currentTimeMillis();
wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish")));
System.out.println("Waited " + (System.currentTimeMillis() - t0) + " ms");  // about 5000 ms
```

The smart wait takes roughly as long as the page needs; the sleep always takes 10 s.

**Exercise 3 (c).**

```java
driver.findElement(By.cssSelector("#input-example button")).click();           // "Enable"
WebElement input = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("#input-example input")));
// custom alternative
wait.until(d -> d.findElement(By.cssSelector("#input-example input")).isEnabled());
input.sendKeys("hello");
```

**Exercise 4.**

```java
Wait<WebDriver> fw = new FluentWait<>(driver)
        .withTimeout(Duration.ofSeconds(10))
        .pollingEvery(Duration.ofMillis(200))
        .ignoring(NoSuchElementException.class)
        .withMessage("Message 'It's gone!' never appeared");
String text = fw.until(d -> d.findElement(By.id("message"))).getText();
```

**Exercise 5.** The message contains: the condition type, the locator, the timeout (3 seconds) and polling interval (500 ms). Use these to confirm the locator and time are what you intended.

**Exercise 6.** Expect `ElementClickInterceptedException` naming the covering element. Fix: `invisibilityOfElementLocated(By.id("loading"))` before the click.

**Exercise 7.** Expect about 20 s (varies). Cause: the implicit wait is applied inside each poll of the explicit wait, so the total is not the limit you wrote. Remedy: implicit wait at 0.

**Exercise 9 hint.** Use the IDs `add-to-cart-sauce-labs-backpack`, `add-to-cart-sauce-labs-bike-light`, `add-to-cart-sauce-labs-bolt-t-shirt`, then `wait.until(cartCountIs(3))` from section 5.

**Exercise 10 hint.** Reading text from the old element after the refresh throws `StaleElementReferenceException`; after `stalenessOf(old)` succeeds, re-find the paragraphs by locator. (If this page does not replace the elements in your browser, the exception may not appear; the lesson is to recognise when it can.)

**Exercise 11 hint.** Do not just lengthen sleeps. For each sleep, ask "what am I waiting for?" and write that as a condition. Keep a table: test name, old pass rate, new pass rate, wait conditions added.

---

## Self-Check Questions

1. **Why can the same test pass and fail without code changes?** Because the test and the browser run independently; the outcome depends on whether the page is ready when the test looks (a race condition).
2. **What is the main weakness of an implicit wait?** It only waits for presence, is global for all lookups, and slows down absence checks.
3. **What does `until` return, and why is it useful?** The truthy value from the condition, often the `WebElement`, so you can chain `.click()` or `.getText()`.
4. **Which condition would you use before clicking? Before reading text? For a spinner?** `elementToBeClickable`; `visibilityOfElementLocated`; `invisibilityOfElementLocated`.
5. **Why shouldn't you mix implicit and explicit waits?** The implicit wait runs inside every poll of the explicit wait, so total times add up unpredictably.
6. **Difference between `WebDriverWait` and `FluentWait`?** `WebDriverWait` is a `FluentWait` preset for `WebDriver` with 500 ms polling and `NotFoundException` ignored; `FluentWait` lets you configure everything and works with any object.
7. **When does `StaleElementReferenceException` occur?** When the page rebuilds the element you saved; fix by re-locating or waiting for `stalenessOf`.
8. **Does a longer timeout slow passing tests?** No; a wait returns as soon as the condition is true.

---

## Summary

- Tests and browsers run independently, so reading the page too early is a **race condition** and the main source of **flaky tests**.
- `Thread.sleep` is slow and still unreliable; use smart waits that return **as soon as** a condition is met.
- **Implicit wait:** a global, one-line timeout for `findElement`; waits only for presence; not recommended for frameworks.
- **Explicit wait** (`WebDriverWait` + `ExpectedConditions` or a lambda): waits for a specific condition with a per-situation timeout; clear errors; **the recommended approach**.
- **Fluent wait:** an explicit wait with custom polling interval and ignored exceptions.
- **Never mix** implicit and explicit waits.
- Match the condition to the action: visible before reading, clickable before clicking, invisible for spinners, staleness after re-renders.
- Read exception text carefully; it usually tells you which wait is missing.
- Wrap waits in a reusable helper; this is part of your framework from today onward.

---

## Additional Resources

- Selenium documentation, *Waiting strategies*: https://www.selenium.dev/documentation/webdriver/waits/
- Selenium Java API, `ExpectedConditions`: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/support/ui/ExpectedConditions.html
- The Internet (practice site with dynamic loading/controls pages): https://the-internet.herokuapp.com/
- Java `Duration` documentation: https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Duration.html
