# Screenshots

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **why** screenshots are one of the most valuable debugging tools in automated testing, and **when** to take them.
- Explain what the `TakesScreenshot` interface is, why a cast is needed, and what `OutputType` does.
- Capture a **viewport** screenshot with `TakesScreenshot` and `OutputType.FILE`.
- Capture a screenshot of a **single element** (Selenium 4).
- Obtain screenshots as `BYTES` or `BASE64` for reports.
- Save files with unique, meaningful names (timestamp, test name) into an organized folder.
- Write a reusable `ScreenshotUtil` and call it when a test fails.
- Read the Java file-handling code (`Path`, `Files`, `try/catch`) that saving requires, line by line.
- Know the limits of Selenium screenshots (scrolling pages, headless sizing, hidden elements, alerts, sensitive data) and troubleshoot them.

---

## Why This Matters

Imagine your suite runs every night at 2 a.m. In the morning, a test named `loginTest` is red, and the log says `NoSuchElementException`. Why? Did the site go down? Did a pop-up cover the page? Did the layout change? Did the test land on a "503 Service Unavailable" page? Without more information, someone must re-run the test and watch it, and the problem may not reproduce, because "it passes when I run it".

A **screenshot taken at the moment of failure** often answers the question in seconds: you can *see* a maintenance banner or an error page. Think of it as the **black box recorder** of an aeroplane, or a **dashcam** in a car: you cannot be present at every incident, but the recording shows what happened. For this reason, almost every professional framework captures screenshots on failure and attaches them to the test report.

Screenshots are also used for **evidence**: for compliance teams, a captured image of the "order confirmation page" documents that the test truly reached that step. In regulated industries (banking, healthcare) that evidence can be a requirement.

**A tester's day, with and without screenshots.**

| Without screenshots | With screenshots |
|---|---|
| 09:00 Read log: `NoSuchElementException: [data-test='username']` | 09:00 Open the failure image |
| 09:10 Re-run test locally; it passes | 09:01 See a "Scheduled maintenance" banner covering the page |
| 09:40 Re-run five more times; one fails | 09:05 Report to the team: environment was down at 02:00 |
| 10:30 Guess "flaky test" and move on | 09:10 Done; no code change needed |

Later this week, when you add Cucumber hooks and reports (Friday), this lesson's `ScreenshotUtil` becomes the piece that plugs in. Today you learn the underlying capability. For **Project 2**, a failure screenshot in every report is a standard expectation of a professional test framework, and this week's Epic (a Selenium framework with BDD) will include it.

---

## The Concept

### 1. The `TakesScreenshot` Interface

**What it is.** Screenshot support is not part of the basic `WebDriver` interface; it lives in a separate interface called `TakesScreenshot`. `ChromeDriver`, `FirefoxDriver`, and `EdgeDriver` all implement it.

**Why a separate interface?** Not every driver can take pictures. `WebDriver` describes what *all* drivers can do (navigate, find elements). Optional abilities are put in extra interfaces, so a driver without a "camera" is not forced to pretend it has one. This is the "interface segregation" idea from Java design.

**How to use it.** Our variable is typed as `WebDriver`, which does not mention screenshots. To reach the ability, **cast** the `WebDriver` to `TakesScreenshot`:

```java
TakesScreenshot camera = (TakesScreenshot) driver;
```

Think of `TakesScreenshot` as a "camera ability" that the driver may have; the cast says "I know this driver has a camera; use it." The object is the same; we only view it through a different interface. If the object does *not* implement the interface, Java throws `ClassCastException` at this line.

The key method is:

```java
<X> X getScreenshotAs(OutputType<X> target)
```

This is a *generic* method: the return type `X` depends on the `OutputType` you pass. If you pass `OutputType.FILE`, `X` is `File`; if you pass `OutputType.BYTES`, `X` is `byte[]`. That is why you can write `File f = camera.getScreenshotAs(OutputType.FILE);` with no further cast.

| `OutputType` | Returns | Typical use |
|---|---|---|
| `OutputType.FILE` | A temporary `java.io.File` (PNG) | Save to disk |
| `OutputType.BYTES` | `byte[]` | Attach to reports, send over a network |
| `OutputType.BASE64` | `String` (Base64-encoded PNG) | Embed directly in HTML reports |

**What happens when this line runs:** `getScreenshotAs` sends a request to the driver (`GET /session/{id}/screenshot`). The browser renders the current viewport to a PNG image and sends it back, encoded as Base64 text inside the JSON response. Selenium decodes it and returns it in the form you requested. So `BASE64` is the "rawest" form, and `BYTES` and `FILE` are conveniences made from it.

### 2. Taking a Screenshot and Saving It

```java
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

File tempFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);

Path destination = Paths.get("screenshots", "login-page.png");
Files.createDirectories(destination.getParent());            // make the folder if missing
Files.copy(tempFile.toPath(), destination, StandardCopyOption.REPLACE_EXISTING);
```

**Line by line:**

- `((TakesScreenshot) driver)`: the inner parentheses are the cast; the outer parentheses make sure the cast applies *before* we call `.getScreenshotAs`. Without the outer parentheses Java would try to call the method on `driver` first and then cast the result.
- `getScreenshotAs(OutputType.FILE)`: Selenium writes the PNG into a temporary file and returns a `File` object pointing to it.
- `Paths.get("screenshots", "login-page.png")`: builds a `Path` for `screenshots/login-page.png`, using the correct slash for your operating system. The folder is *relative*, meaning relative to the directory where the program runs (your project root when run from the IDE or Maven).
- `destination.getParent()`: the `Path` of the folder part (`screenshots`).
- `Files.createDirectories(...)`: creates the folder, and any missing parent folders. It does nothing if the folder already exists, so it is safe to call every time.
- `Files.copy(source, target, REPLACE_EXISTING)`: copies the file. The third argument says "if a file with that name is already there, overwrite it" (without it, copying onto an existing file throws `FileAlreadyExistsException`).

**Why copy?** With `OutputType.FILE`, Selenium writes the image to a *temporary* file (in your system's temp folder) that may be deleted later. Copying it to your own folder keeps it.

`Files.copy` and `Files.createDirectories` throw a checked `IOException`; either declare `throws IOException` on the method or wrap in `try/catch`. (A *checked* exception is one the Java compiler forces you to deal with.)

**Check yourself:** after running, refresh your project folder. A `screenshots` folder should appear next to `pom.xml`, containing `login-page.png`.

### 3. What Does a Screenshot Capture?

By default, **the visible viewport** of the current tab: what a user would see in the window right now, without scrolling. Consequences:

- Content below the fold is **not** captured unless you scroll to it (or use Firefox's full-page feature, below).
- The window size determines the image size. Use consistent window sizes (see *Navigation Methods* and *Browser Options*) so that screenshots are comparable. The Browser Options lesson showed why headless runs need `--window-size`.
- Browser chrome (address bar, tabs) is **not** included, only the page.
- Pop-up alerts that are native browser dialogs are **not** captured (Wednesday covers alerts).
- The screenshot shows the page **at that instant**. If an animation or spinner is mid-flight, that is what you get.

**Analogy:** the screenshot is a photograph taken through a window. You see only what is inside the frame, only at the moment of the click.

### 4. Element Screenshots (Selenium 4)

**What and why.** You can capture only one element, which is helpful for visual checks of a logo, a chart, or an error message, or to attach a small, focused image to a bug report instead of a whole page.

```java
WebElement logo = driver.findElement(By.className("login_logo"));
File logoFile = logo.getScreenshotAs(OutputType.FILE);
Files.copy(logoFile.toPath(), Paths.get("screenshots", "logo.png"),
           StandardCopyOption.REPLACE_EXISTING);
```

`WebElement` itself has `getScreenshotAs`, no casting needed. Selenium scrolls the element into view and crops the image to its bounds. If the element is not displayed, or has zero size, the call fails.

**When to use which:**

| Need | Use |
|---|---|
| Evidence of the whole screen state at failure | Viewport screenshot |
| Show only the error banner | Element screenshot |
| Visually check that a chart rendered | Element screenshot of the chart |
| Attach to a bug about one component | Element screenshot |

**Remember** the `WebElement` is a reference (from the Find Methods lesson); if the page changed and the element is stale, the call throws `StaleElementReferenceException`. Find the element again right before capturing.

### 5. Full-Page Screenshots

- **Firefox**: `FirefoxDriver` offers `getFullPageScreenshotAs(OutputType.FILE)`, which captures the entire scrollable page. Because it is a method of `FirefoxDriver` (not `WebDriver`), you need a variable typed as `FirefoxDriver`:

```java
FirefoxDriver ff = new FirefoxDriver();
ff.get("https://the-internet.herokuapp.com/large");
File full = ff.getFullPageScreenshotAs(OutputType.FILE);
```

- **Chrome/Edge**: no built-in method in Selenium's standard API. Options include setting the window height large enough before capturing (for pages with predictable length), or using the Chrome DevTools Protocol. The DevTools approach is beyond today's scope; just remember that "full page in Chrome" needs extra work. A simple trick for a known page:

```java
driver.manage().window().setSize(new Dimension(1920, 4000));   // very tall window
File tall = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
```

This needs `import org.openqa.selenium.Dimension;`. It works well in headless mode where window size is under your control, but it is a workaround, not a guarantee.

### 6. BYTES and BASE64

```java
byte[] png    = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
String base64 = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BASE64);
```

- `byte[]` is an array of raw bytes: the exact content of a PNG file held in memory. `BYTES` is useful for report libraries that take a `byte[]` (we will see this with Cucumber's `scenario.attach(bytes, "image/png", "name")` on Friday).
- `BASE64` is the same data converted to plain text using only letters, digits, `+`, `/`, and `=`. Because it is text, it can be placed inside an HTML file:

```html
<img src="data:image/png;base64,{base64String}" />
```

Because it needs no separate file, it is convenient for single-file reports (you can email one HTML file), but it makes the HTML larger (Base64 is about one third bigger than raw bytes).

You can write `BYTES` to disk without a temp file:

```java
Files.write(Paths.get("screenshots", "direct.png"), png);    // throws IOException
```

| Format | Memory | Needs a file on disk? | Best for |
|---|---|---|---|
| `FILE` | Low | Yes (temp file) | Saving images to folders |
| `BYTES` | Medium | No | Passing to report libraries |
| `BASE64` | Highest | No | Embedding in HTML |

### 7. Naming and Organizing Screenshots

Overwriting `screenshot.png` each time defeats the purpose: after 50 failures you have one picture. Use names that tell you *which test, when*:

```
screenshots/
  2026-10-12/
    loginTest_FAILED_20261012_020315.png
    checkoutTest_FAILED_20261012_020342.png
```

A **timestamp** makes names unique:

```java
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

String timestamp = LocalDateTime.now()
        .format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
```

What it does: `LocalDateTime.now()` returns the current date and time; `ofPattern("yyyyMMdd_HHmmss")` describes the text layout (`yyyy` four-digit year, `MM` month, `dd` day, `HH` 24-hour hour, `mm` minutes, `ss` seconds). Beware the capital/lowercase difference: `MM` is month, `mm` is minutes. The result might be `20261012_020315`.

Avoid characters not allowed in file names (`\ / : * ? " < > |`). If your name includes a test title with spaces or symbols, sanitize it: `title.replaceAll("[^a-zA-Z0-9-_]", "_")`. That regular expression means "any character that is **not** a letter, digit, hyphen, or underscore" (the `^` inside `[...]` means "not"), and each is replaced by an underscore. So `Login with "wrong" password?` becomes `Login_with__wrong__password_`.

### 8. A Reusable `ScreenshotUtil`

```java
package com.revature.qea.utils;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public final class ScreenshotUtil {

    private static final String BASE_DIR = "screenshots";

    private ScreenshotUtil() { }

    /** Captures the viewport and returns the saved file's path. */
    public static Path capture(WebDriver driver, String name) {
        if (!(driver instanceof TakesScreenshot)) {
            throw new UnsupportedOperationException("This driver cannot take screenshots");
        }
        File temp = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
        return save(temp, name);
    }

    /** Captures a single element. */
    public static Path capture(WebElement element, String name) {
        File temp = element.getScreenshotAs(OutputType.FILE);
        return save(temp, name);
    }

    /** Returns the screenshot bytes (for report attachments). */
    public static byte[] captureBytes(WebDriver driver) {
        return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
    }

    private static Path save(File temp, String name) {
        String safeName = name.replaceAll("[^a-zA-Z0-9-_]", "_");
        String timestamp = LocalDateTime.now()
                .format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss_SSS"));
        Path target = Paths.get(BASE_DIR, safeName + "_" + timestamp + ".png");
        try {
            Files.createDirectories(target.getParent());
            Files.copy(temp.toPath(), target, StandardCopyOption.REPLACE_EXISTING);
            return target;
        } catch (IOException e) {
            throw new RuntimeException("Could not save screenshot to " + target, e);
        }
    }
}
```

**Explanation, piece by piece:**

- `public final class ScreenshotUtil` with `private ScreenshotUtil() { }`: a *utility class*. `final` prevents subclassing; the private constructor prevents `new ScreenshotUtil()`. Everything is `static`, so you call `ScreenshotUtil.capture(...)` directly.
- `private static final String BASE_DIR = "screenshots";`: one constant for the root folder. If the team later wants `target/screenshots`, only this line changes.
- `capture(WebDriver driver, String name)` and `capture(WebElement element, String name)` are *overloads*: same method name, different parameter types. Java chooses the right one from the argument you pass.
- `driver instanceof TakesScreenshot` is `true` when the object has the camera ability. The `!(...)` negates it, so the exception is thrown only when the driver lacks the ability. `UnsupportedOperationException` is a standard Java exception meaning "this operation is not available".
- The two `capture` overloads share one private `save` method (avoid duplicate code: the "DRY" rule).
- In `save`: sanitizing the name, building a millisecond timestamp, composing the target path (`screenshots/<name>_<timestamp>.png`), creating the folder, copying the file.
- The `catch (IOException e)` converts the checked exception into an unchecked `RuntimeException`, so callers do not need `try/catch` everywhere. Passing `e` as the second argument keeps the *cause*, so the stack trace still shows the original problem. (A screenshot failure should not hide the *real* test failure; later you can catch it separately.)
- Milliseconds (`SSS`) in the timestamp prevent collisions when two screenshots happen in the same second.

### 9. Screenshot on Failure

The pattern: wrap the test steps in `try/catch`, capture in the `catch`, and rethrow so the test still fails.

```java
WebDriver driver = DriverFactory.createDriver("chrome", false);
try {
    driver.get("https://www.saucedemo.com");
    driver.findElement(By.id("user-name")).sendKeys("standard_user");
    driver.findElement(By.id("password")).sendKeys("wrong_password");
    driver.findElement(By.id("login-button")).click();

    // This will fail because the element does not exist
    driver.findElement(By.className("inventory_list"));
} catch (Exception e) {
    Path shot = ScreenshotUtil.capture(driver, "loginTest_FAILED");
    System.out.println("Failure screenshot saved: " + shot.toAbsolutePath());
    throw e;      // do not hide the failure!
} finally {
    driver.quit();
}
```

**What happens, step by step:**

1. The browser opens; the login is attempted with a wrong password.
2. The site stays on the login page and shows a red error banner.
3. `findElement(By.className("inventory_list"))` throws `NoSuchElementException`, because that list exists only after a successful login.
4. Control jumps to the `catch` block, which takes a screenshot *while the browser is still open* (this is why the `driver.quit()` is in `finally`, which runs afterwards).
5. The screenshot shows the red error message, so the reader instantly understands: "login failed with an error message", far more informative than the exception text.
6. `throw e;` rethrows the same exception so the test is still reported as failed. If you forget to rethrow, the test would *pass* despite the failure, which hides real bugs.
7. `finally` closes the browser.

(Because `catch (Exception e)` followed by `throw e;` compiles without a `throws` clause in modern Java, thanks to "precise rethrow", the compiler knows only unchecked exceptions can occur here. If your compiler complains, add `throws Exception` to the enclosing method.)

> **Look ahead:** Writing this `try/catch` in every test would be tedious. On Friday you will see that Cucumber **hooks** (`@After`) can capture a screenshot automatically whenever *any* scenario fails. Today's manual pattern teaches you what the hook will do for you. We explain hooks in depth on Friday; no need to know them now.

### 10. Limitations and Tips

| Situation | Behavior | Tip |
|---|---|---|
| Page longer than window | Only visible part is captured | Scroll first, or resize window; Firefox full-page method |
| Headless with small default window | Small image, cropped layout | Set `--window-size` |
| Native alert box open | `UnhandledAlertException` or no capture of dialog | Handle alert first (Wednesday) |
| Screenshot taken too early | Blank or half-loaded page | Wait for the page to be ready (Tuesday) |
| Many screenshots in long runs | Large disk usage | Capture on failure only; clean old folders |
| Sensitive data on screen (passwords, personal info) | Stored in image files | Do not capture real customer data; mask or restrict access |
| Browser already closed (`quit()` ran) | `NoSuchSessionException` | Capture **before** `quit()` |
| Element is hidden | Element screenshot fails | Check it is displayed first |

**Troubleshooting walk-through 1: a black or blank screenshot.**

Symptom: the PNG is entirely white, though the test was clearly on a page.
Diagnosis: (a) the capture happened right after navigation before rendering finished (timing; Tuesday's waits solve it), or (b) a headless run with an odd window size. Try printing the window size and adding `--window-size`. Take another capture after a short pause as an experiment.

**Troubleshooting walk-through 2: "NoSuchSessionException" when capturing in a failure handler.**

Symptom:

```
org.openqa.selenium.NoSuchSessionException: invalid session id
```

Diagnosis: the browser was already closed, usually because `driver.quit()` ran before the screenshot code (for example, a test base class closes the browser in one method and the failure listener runs later). Fix the order: screenshot first, `quit()` second. Always remember the rule: **a picture needs a living browser**.

**Troubleshooting walk-through 3: `ClassCastException`.**

Symptom: `class ... cannot be cast to class org.openqa.selenium.TakesScreenshot`.
Diagnosis: the driver object is a wrapper (some libraries wrap `WebDriver`) that does not implement the interface. Fix: use `new Augmenter().augment(driver)` (Selenium's helper for remote drivers) before casting:

```java
WebDriver augmented = new Augmenter().augment(driver);
File f = ((TakesScreenshot) augmented).getScreenshotAs(OutputType.FILE);
```

You will mainly need this with remote (grid) drivers, which are not part of this week's content; the key is recognising that the cast is the place where the problem appears.

---

## Code Example: Complete Demo

```java
package com.revature.qea.screenshots;

import com.revature.qea.utils.ScreenshotUtil;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.nio.file.Path;

public class ScreenshotDemo {
    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        try {
            driver.manage().window().maximize();
            driver.get("https://www.saucedemo.com");

            // 1. Whole viewport
            Path p1 = ScreenshotUtil.capture(driver, "01_login_page");
            System.out.println("Saved: " + p1);

            // 2. A single element
            WebElement logo = driver.findElement(By.className("login_logo"));
            Path p2 = ScreenshotUtil.capture(logo, "02_logo");
            System.out.println("Saved: " + p2);

            // 3. After login
            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.id("password")).sendKeys("secret_sauce");
            driver.findElement(By.id("login-button")).click();
            Path p3 = ScreenshotUtil.capture(driver, "03_inventory_page");
            System.out.println("Saved: " + p3);

            // 4. Bytes (e.g., for a report)
            byte[] bytes = ScreenshotUtil.captureBytes(driver);
            System.out.println("Screenshot size in bytes: " + bytes.length);
        } finally {
            driver.quit();
        }
    }
}
```

**Explanation:**

- We import our own utility class from the `utils` package; the file must be compiled in the same project (same Maven module).
- `Path p1 = ScreenshotUtil.capture(driver, "01_login_page");`: Java sees a `WebDriver` argument, so it picks the viewport overload. The returned `Path` tells us where the file went.
- `ScreenshotUtil.capture(logo, "02_logo")`: the argument is a `WebElement`, so the element overload runs, and the image is cropped to the logo.
- The inventory screenshot (step 3) shows the six products. The numeric prefixes (`01_`, `02_`, `03_`) keep the files sorted in the order they were taken.
- `bytes.length` is the number of bytes in the PNG held in memory; a typical full-HD viewport is on the order of 50 to 200 thousand bytes.

**Expected output (paths will differ in the timestamp):**

```
Saved: screenshots/01_login_page_20261012_091503_221.png
Saved: screenshots/02_logo_20261012_091503_540.png
Saved: screenshots/03_inventory_page_20261012_091505_117.png
Screenshot size in bytes: 118342
```

---

## Guided Lab: A Failure Evidence Folder (30 minutes)

**Goal:** build a tiny failing test that automatically leaves behind a screenshot, then prove the screenshot explains the failure.

**Steps:**

1. Create the `ScreenshotUtil` class from section 8 under `src/test/java/com/revature/qea/utils/` (or `src/main/java`, following your Project 2 layout).
2. Create `FailureLab.java` with a `main` method that uses the `DriverFactory` from the Browser Options lesson: `DriverFactory.createDriver("chrome", false)`.
3. Navigate to `https://www.saucedemo.com`. Log in with `locked_out_user` and `secret_sauce`.
4. Add a step that expects the inventory list: `driver.findElement(By.className("inventory_list"))`. This will fail, because that user is locked out.
5. Wrap steps 3 and 4 in `try/catch/finally` as in section 9; in the `catch`, capture a screenshot named `lockedOutUser_FAILED`, print the absolute path, and rethrow.
6. Run the program. **Expected console output:** a line `Failure screenshot saved: /.../screenshots/lockedOutUser_FAILED_<timestamp>.png`, followed by the stack trace with `NoSuchElementException`.
7. Open the PNG. **Expected image:** the login page with a red error banner reading "Epic sadface: Sorry, this user has been locked out."
8. Reflect in writing: what did the *exception* tell you, and what did the *picture* tell you? (The exception says an element is missing; the picture says why.)
9. Stretch: also save an element screenshot of the error banner (`[data-test='error']`) in the same `catch` block. Wrap the extra capture in its own `try/catch` so a failed screenshot does not hide the original error.

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Calling `getScreenshotAs` on a plain `WebDriver` without casting | Compile error "cannot find symbol" | Cast to `TakesScreenshot` |
| Forgetting the extra parentheses in `(TakesScreenshot) driver.getScreenshotAs(...)` | Compile error | Write `((TakesScreenshot) driver).getScreenshotAs(...)` |
| Not copying the temp file | File disappears later | `Files.copy(...)` to your own folder |
| Fixed file name (`screenshot.png`) | Each run overwrites the last | Add test name and timestamp |
| Swallowing the exception in `catch` | Test passes though it failed | `throw e;` after capturing |
| Taking the screenshot after `driver.quit()` | `NoSuchSessionException` | Capture first, quit last |
| Using `mm` instead of `MM` for month in the pattern | Minutes appear where the month should be | Month is `MM`, minutes is `mm` |
| Saving screenshots with real customer data | Privacy and compliance risk | Use test data; restrict folder access |
| Expecting a full-page capture in Chrome | Only the viewport is saved | Resize window, use Firefox method, or DevTools |

---

## Practice Exercises

1. **First capture.** Take a screenshot of the SauceDemo login page and open the PNG to verify it.
2. **Element capture.** Capture only the login button and the error message (trigger the error with a bad password).
3. **Failure hook, by hand.** Write a test that deliberately fails (wrong locator) and saves a screenshot in the `catch` block with the test name in the file name. Confirm the test still reports failure.
4. **Viewport vs. page.** Open `https://the-internet.herokuapp.com/large` (a very large table). Take a screenshot in Chrome, and describe what is missing. Then try `FirefoxDriver.getFullPageScreenshotAs` if Firefox is available.
5. **Compare sizes.** Take screenshots at window sizes 800x600 and 1920x1080 and compare the image dimensions (use `javax.imageio.ImageIO.read(file)` to get width and height).
6. **Folder per run.** Modify `ScreenshotUtil` so screenshots go in a subfolder named with today's date (`yyyy-MM-dd`).
7. **Discussion:** Name two risks of storing screenshots on a shared CI server, and one mitigation for each.
8. **BYTES to disk.** Capture with `OutputType.BYTES` and write the array to `screenshots/bytes.png` with `Files.write`. Confirm the file opens.
9. **BASE64 report.** Capture with `OutputType.BASE64` and generate a one-page `report.html` that embeds the image inside an `<img>` tag. Open it in a browser.
10. **Sanitizer test.** Write a small `main` that passes the name `Login with "wrong" password?` to `ScreenshotUtil.capture` and prints the resulting file name. Explain each replaced character.
11. **Step-by-step evidence.** Add a method `ScreenshotUtil.step(driver, "01_open")` pattern: take a screenshot after each of five actions in the SauceDemo purchase flow (login, add to cart, open cart, checkout info, finish), numbering them so that the folder reads like a storyboard.
12. **Safe capture.** Write `captureSafely(WebDriver driver, String name)` that catches any exception during capture and prints a warning rather than throwing, so it can never hide the real test failure.

---

## Solutions and Hints

**1.** Use the demo code: `ScreenshotUtil.capture(driver, "login_page")` after `driver.get(...)`; open `screenshots/login_page_*.png`.

**2.** Login button: `ScreenshotUtil.capture(driver.findElement(By.id("login-button")), "login_button")`. Error message: first log in with a bad password, then capture `driver.findElement(By.cssSelector("[data-test='error']"))`. Hint: the error element does not exist before you click login, so capture it only afterwards.

**3.** Use the pattern from section 9. Verify the test "fails" by checking the program ends with an exception stack trace (or a red test in JUnit when you move to JUnit later in the week).

**4.** The Chrome image shows only the top rows of the table, because the table is much taller than the window. In Firefox, `getFullPageScreenshotAs` returns a tall image containing the whole table. Hint: remember to type the variable as `FirefoxDriver`, not `WebDriver`.

**5.**

```java
File f = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
BufferedImage img = ImageIO.read(f);
System.out.println(img.getWidth() + " x " + img.getHeight());
```

Needs `import java.awt.image.BufferedImage;`, `import javax.imageio.ImageIO;`, and handling `IOException`. The image size usually matches the viewport size (possibly scaled on high-DPI screens).

**6.** In `save`, change the target to:

```java
String day = java.time.LocalDate.now().toString();          // 2026-10-12
Path target = Paths.get(BASE_DIR, day, safeName + "_" + timestamp + ".png");
```

`LocalDate.now().toString()` already gives `yyyy-MM-dd`. `createDirectories` then creates the dated folder automatically.

**7.** Examples: (1) screenshots may expose personal or confidential data; mitigation: use synthetic test data and restrict access to the artifact folder. (2) Disk fills up over time; mitigation: retention policy that deletes old runs, capture only on failure. Another: screenshots of production credentials; mitigation: never test with real credentials, mask fields.

**8.**

```java
byte[] png = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
Files.createDirectories(Paths.get("screenshots"));
Files.write(Paths.get("screenshots", "bytes.png"), png);
```

**9.**

```java
String b64 = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BASE64);
String html = "<html><body><h1>Evidence</h1><img src=\"data:image/png;base64," + b64 + "\"/></body></html>";
Files.write(Paths.get("screenshots", "report.html"), html.getBytes(java.nio.charset.StandardCharsets.UTF_8));
```

The backslash-quotes (`\"`) are escaped quotation marks inside a Java string.

**10.** The result is `Login_with__wrong__password__<timestamp>.png`: spaces and quotes and the question mark are not letters or digits, so each became `_`. (Check the exact count of underscores in your output.)

**11.** Example:

```java
ScreenshotUtil.capture(driver, "01_login_page");
// ...log in...
ScreenshotUtil.capture(driver, "02_inventory");
driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();
ScreenshotUtil.capture(driver, "03_item_added");
driver.findElement(By.className("shopping_cart_link")).click();
ScreenshotUtil.capture(driver, "04_cart");
```

The timestamps and number prefixes sort files in the order of the story.

**12.**

```java
public static void captureSafely(WebDriver driver, String name) {
    try {
        Path p = capture(driver, name);
        System.out.println("Screenshot saved: " + p);
    } catch (Exception e) {
        System.out.println("WARNING: could not capture screenshot: " + e.getMessage());
    }
}
```

Place this inside `ScreenshotUtil` so that the original test failure is never replaced by a screenshot failure.

---

## Self-Check Questions

**Q1. Why do you cast `WebDriver` to `TakesScreenshot`?**
`WebDriver` does not declare screenshot methods; the ability lives in the separate `TakesScreenshot` interface, which the driver implements.

**Q2. What does a default Selenium screenshot contain?**
The visible viewport of the current tab only, without browser chrome and without native dialogs.

**Q3. What is the difference between `FILE`, `BYTES`, and `BASE64`?**
`FILE` is a temporary file, `BYTES` is the PNG in a `byte[]`, `BASE64` is the PNG as text suitable for embedding in HTML.

**Q4. Why copy the file returned by `OutputType.FILE`?**
It is a temporary file that may be deleted; copying preserves it in your own folder.

**Q5. In a failure handler, why rethrow the exception after taking the screenshot?**
So the test still fails. Without rethrowing, the test would appear to pass and hide the defect.

**Q6. Why is a screenshot after `driver.quit()` impossible?**
The browser session no longer exists, so Selenium throws `NoSuchSessionException`.

**Q7. How can you capture a full page in Chrome?**
Chrome has no built-in standard method: enlarge the window, or use the DevTools protocol. Firefox has `getFullPageScreenshotAs`.

**Q8. Name two things to do to keep screenshots useful in a long-running suite.**
Use unique, meaningful names with test name and timestamp; capture only on failure and clean old folders; avoid sensitive data.

---

## Summary

- Screenshots are a primary debugging and evidence tool; capture them **on failure** at minimum.
- Cast `WebDriver` to **`TakesScreenshot`** and call `getScreenshotAs(OutputType.FILE | BYTES | BASE64)`.
- `WebElement.getScreenshotAs` captures a single element (Selenium 4).
- Default capture is the **visible viewport**; full-page capture needs browser-specific features.
- Save images with **unique, meaningful names** and a predictable folder structure; copy the temp file before it disappears.
- Build a reusable `ScreenshotUtil`; on Friday it will be wired into Cucumber hooks and reports.
- Capture before `quit()`, rethrow after capturing, and never let a screenshot failure hide the real failure.
- Be careful with timing (waits come Tuesday), headless window size, and sensitive data.

---

## Additional Resources

- Selenium documentation, *Taking screenshots*: https://www.selenium.dev/documentation/webdriver/interactions/windows/#takescreenshot
- Selenium documentation, *Element screenshot* (in the same Windows/Elements pages): https://www.selenium.dev/documentation/webdriver/elements/information/
- Selenium Java API, `TakesScreenshot`: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/TakesScreenshot.html
