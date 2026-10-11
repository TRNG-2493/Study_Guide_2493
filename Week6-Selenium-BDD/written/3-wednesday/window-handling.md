# Window Handling

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **window handle** is and why Selenium needs one.
- Get the current handle with `getWindowHandle()` and all handles with `getWindowHandles()`.
- Switch between windows and tabs with `driver.switchTo().window(handle)`.
- Handle a link or button that opens a **new tab or window**, including waiting for it to open.
- Open a new tab or window on purpose with `driver.switchTo().newWindow(...)`.
- Close a single window with `close()` while keeping the session alive, and return to the original window.
- Switch into and out of **iframes** using `switchTo().frame(...)`, `parentFrame()`, and `defaultContent()`.
- Diagnose `NoSuchWindowException`, `NoSuchFrameException`, and "element not found" errors caused by a wrong window or frame context.
- Write a reusable window-switching helper and use it from page objects.

---

## Why This Matters

Real workflows span multiple browser windows. Click "Terms and Conditions" and a new tab opens. Click "Pay with PayPal" and a pop-up window appears. A help page opens in a separate tab. An embedded video player or payment form lives in an `<iframe>`.

A critical fact about Selenium: **it controls only one window or frame at a time.** When the browser opens a new tab, your `driver` still points at the *old* one. Commands like `findElement` will keep searching the old page and fail with `NoSuchElementException` even though you can see the new tab on screen. You must **explicitly switch** to the new window.

**Analogy.** Picture a call-centre agent with several phones on the desk. Selenium is the agent, and it can talk into only **one phone at a time**. When a new call (tab) arrives, the agent keeps talking into the old phone until someone says "pick up line 2". The `switchTo()` methods are how you tell the agent which phone to pick up. Frames are the same idea at a smaller scale: a page inside a page is a second conversation on the same phone line, and you must tell the agent to "listen to the inner conversation".

Real-world scenarios:

1. **Legal links.** A checkout page has "Terms and Conditions" opening in a new tab. A test verifies the heading, closes the tab, and continues paying.
2. **Social login.** "Sign in with Google" opens a pop-up window. The test fills credentials in the pop-up, and the pop-up closes itself.
3. **Payment form in an iframe.** Card-number fields are served inside a frame by the payment provider, so the test must enter the frame to type.
4. **Rich-text editors.** Comment boxes and CMS editors typically live in an iframe.

This is one of the most common stumbling points for new automation engineers, and it will appear in any serious **Project 2** flow (checkout, payment, help links, social logins, footer links). On SauceDemo, for instance, the footer social links (Twitter/X, Facebook, LinkedIn) open **new tabs**, which is a natural practice target.

You have already used pieces of this: on Tuesday you used `driver.get`, locators, and waits; earlier today the Alerts lesson used `switchTo().alert()`. `switchTo()` is the family of methods that moves Selenium's attention, and this lesson covers its remaining members.

---

## The Concept

### 1. Window Handles

**Definition.** When a window or tab opens, the browser gives it a unique identifier called a **window handle**, a string like `"CDwindow-4F2E1A5B6C7D8E9F0A1B2C3D4E5F6A7B"`. A handle is like a **cloakroom ticket**: it does not describe the coat (the window's title or URL); it simply identifies which one is yours.

**Why it exists.** Titles and URLs can be duplicated (two tabs may show the same page). A handle is guaranteed unique within a session, so Selenium uses it to know exactly which window you mean.

```java
String currentHandle = driver.getWindowHandle();            // handle of the window Selenium controls now
Set<String> allHandles = driver.getWindowHandles();         // handles of ALL open windows/tabs
```

**Line-by-line.**

- `getWindowHandle()` returns a single `String`: the handle of the window Selenium currently controls.
- `getWindowHandles()` returns a `Set<String>` (`java.util.Set`). A `Set` is a collection with **no duplicates and no guaranteed order**, so never assume that "the last element" is the newest window. Compare with the original handle instead.
- Handles are **valid only for that session**; do not store them between runs.

You will need `import java.util.Set;` at the top of the file.

**Quick experiment.** Print `driver.getWindowHandle()` right after opening a page. You will see something like `CDwindow-...`. Run twice: the value differs, which proves handles are not constant.

### 2. Switching Windows

```java
driver.switchTo().window(handle);
```

**Explanation.** `switchTo()` returns a `TargetLocator` object (Selenium's "switch remote control"). Its `window(String)` method tells the driver "from now on, act on the window with this handle". After this call, `driver` commands act on that window. Nothing visibly changes on screen (Selenium does not necessarily bring the tab to the foreground); only Selenium's focus moves. If the handle no longer exists (the window was closed), you get `NoSuchWindowException`.

**Summary of the `switchTo()` family.**

| Method | Moves focus to | Return to previous with |
|---|---|---|
| `switchTo().window(handle)` | Another window/tab | `switchTo().window(originalHandle)` |
| `switchTo().newWindow(type)` | A brand new tab/window | `switchTo().window(originalHandle)` |
| `switchTo().frame(...)` | An iframe | `parentFrame()` / `defaultContent()` |
| `switchTo().alert()` | A JavaScript dialog (previous lesson) | `accept()` / `dismiss()` |
| `switchTo().activeElement()` | The element with keyboard focus | n/a |
| `switchTo().defaultContent()` | The top-level page of the current window | n/a |

### 3. The Standard Pattern: Handle a Link That Opens a New Tab

```java
String originalWindow = driver.getWindowHandle();
Set<String> before = driver.getWindowHandles();

driver.findElement(By.linkText("Click Here")).click();      // opens a new tab/window

// 1. Wait until there are two windows
new WebDriverWait(driver, Duration.ofSeconds(10))
        .until(ExpectedConditions.numberOfWindowsToBe(2));

// 2. Find the new handle (the one that was not there before)
for (String handle : driver.getWindowHandles()) {
    if (!handle.equals(originalWindow)) {
        driver.switchTo().window(handle);
        break;
    }
}

// 3. Work in the new window
System.out.println("New window title: " + driver.getTitle());

// 4. Close the new window and go back
driver.close();                                  // closes ONLY the current (new) window
driver.switchTo().window(originalWindow);        // MUST switch back, or the driver points at a closed window
```

**Step-by-step explanation.**

1. **Remember the original.** `getWindowHandle()` is stored in `originalWindow`. This is your "way home".
2. **Take a snapshot** of existing handles in `before` (used for the by-exclusion approach in the helper later).
3. **Click** the link. The browser opens the tab, but the driver still points at the original.
4. **Wait.** `ExpectedConditions.numberOfWindowsToBe(2)` polls until exactly two windows exist. Without this, `getWindowHandles()` immediately after the click may still return one handle, and the loop would find no new window.
5. **Loop through handles.** For each handle, if it is not the original, it must be the new one. `switchTo().window(handle)` moves focus; `break` leaves the loop.
6. **Work** with the new page normally: `getTitle()`, `findElement`, assertions.
7. **Close and return.** `driver.close()` closes only the current window. Then switch back to `originalWindow`.

Why each step matters:

- **Wait** for `numberOfWindowsToBe(2)`: the new window may take a moment to appear.
- **Identify the new handle by exclusion**: "not the original" is deterministic, unlike picking an element out of an unordered Set.
- **`close()` then `switchTo().window(original)`**: after closing the current window, Selenium does **not** automatically go back to another; any further command throws `NoSuchWindowException` until you switch.

**Troubleshooting walk-through: forgot to switch back.**

```text
org.openqa.selenium.NoSuchWindowException: no such window: target window already closed
from unknown error: web view not found
```

**Diagnosis.** "target window already closed" tells you the driver's current target is a window that no longer exists. This happens when your code called `driver.close()` and then used the driver without calling `switchTo().window(...)`. **Fix.** Always follow `close()` with a switch to a window that is still open.

**Troubleshooting walk-through: forgot to switch to the new tab.**

```text
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: {"method":"css selector","selector":"h3"}
```

**Diagnosis.** The locator is right and the element is visible on screen, but the driver is still looking at the **old** tab. Check `driver.getTitle()` or `driver.getCurrentUrl()` just before the failing line: if it shows the old page, you have not switched.

### 4. Finding a Window by Its Title or URL

When several windows are open and you want a particular one:

```java
public void switchToWindowWithTitle(WebDriver driver, String expectedTitle) {
    for (String handle : driver.getWindowHandles()) {
        driver.switchTo().window(handle);
        if (driver.getTitle().equals(expectedTitle)) {
            return;                                  // stay on this window
        }
    }
    throw new NoSuchWindowException("No window with title: " + expectedTitle);
}
```

**Explanation.** The method loops through all windows, switching to each and checking the title (or `getCurrentUrl()`). If one matches, `return` ends the method immediately, leaving the driver on that window. If nothing matches, it throws a clear exception with a helpful message (better than a mysterious failure later). Remember that this **leaves the driver on the last window it visited** if the loop fails, so keep the original handle to restore if needed.

**When to prefer title/URL over exclusion.** When three or more windows are open and several are new, "not the original" is ambiguous; title or URL narrows it. Wait for the page to load before reading the title; a new tab can briefly have an empty title or `about:blank` as its URL. A robust version waits: `wait.until(d -> { d.switchTo().window(handle); return d.getTitle().contains(partial); })`.

### 5. Opening a New Tab or Window Deliberately (Selenium 4)

```java
import org.openqa.selenium.WindowType;

String original = driver.getWindowHandle();

driver.switchTo().newWindow(WindowType.TAB);       // opens a blank new tab AND switches to it
driver.get("https://the-internet.herokuapp.com");

driver.switchTo().newWindow(WindowType.WINDOW);    // or a separate window
driver.get("https://www.saucedemo.com");
```

**Explanation.**

- `WindowType` is an enum with two values, `TAB` and `WINDOW`.
- Unlike clicking a link, here you **already are** in the new window: `newWindow` both opens and switches. No waiting loop is needed.
- Typical uses: log in as a second user in another tab (to test chat or collaboration), compare two pages side by side, or open a utility page (such as a temporary-email site) without leaving the main flow.

**Important.** Tabs in the same browser profile **share cookies**, so logging in as `standard_user` in one tab usually logs you in in the other tab too. For genuinely separate users, create a second `WebDriver` instance (a separate browser), which has its own cookies.

### 6. `close()` vs. `quit()` (A Final Look)

| Method | Effect | Afterwards |
|---|---|---|
| `driver.close()` | Closes the **current** window only | You must `switchTo().window(...)` another window. If it was the last window, the session ends as well. |
| `driver.quit()` | Closes **all** windows, ends the session, stops the driver | The `driver` object is unusable |

Use `close()` to tidy up pop-ups mid-test; use `quit()` in the final cleanup (the `@AfterMethod` / `@AfterEach` method, or the `finally` block). If your test leaves extra windows open and you call `quit()`, they are all closed, so no leak occurs.

### 7. Pop-Up Windows

Pop-ups opened with `window.open(...)` are small separate windows. Selenium handles them exactly like tabs: they appear in `getWindowHandles()`. (Pop-up *blockers* may stop them opening; the `--disable-popup-blocking` Chrome argument from the *Browser Options* lesson allows them.) Treat a pop-up like a tab: wait for the count, switch, act, close, switch back.

**Do not confuse** a pop-up window with a JavaScript alert (previous lesson) or an HTML modal. If it has its own title bar or appears in `getWindowHandles()`, it is a window.

### 8. Window Size and Position of Each Window

Each window has its own size and position, which you can read or set after switching:

```java
driver.switchTo().window(popupHandle);
driver.manage().window().setSize(new Dimension(800, 600));
```

(See the *Navigation Methods* lesson for the window methods.) `Dimension` comes from `org.openqa.selenium`. `maximize()` also applies to the window you are currently focused on, not to all windows.

### 9. iFrames

**Definition.** An **iframe** (inline frame) embeds one HTML page inside another. Examples: a payment form, an embedded video, a rich-text editor, an advertisement, a map. The inner document is a **separate DOM** from the outer page.

**Analogy.** A framed photograph hanging on a wall: you can see the picture from the room, but to read the small writing inside the picture you must "step into" it. The page is the room; the iframe is the picture.

Consequently:

> If an element is inside an iframe, `driver.findElement` on the main page will **not** find it. You get `NoSuchElementException` even though the element is visible on screen.

Like windows, frames need explicit switching:

```java
// Switch IN: by index, by name/id, or by WebElement (most robust)
driver.switchTo().frame(0);                                             // by index (0-based)
driver.switchTo().frame("mce_0_ifr");                                   // by name or id
driver.switchTo().frame(driver.findElement(By.cssSelector("iframe.editor")));   // by element

// Work inside the frame
driver.findElement(By.id("tinymce")).sendKeys("Hello from Selenium");

// Switch OUT
driver.switchTo().parentFrame();        // up ONE level (for nested frames)
driver.switchTo().defaultContent();     // all the way back to the top-level page
```

**Choosing how to enter a frame.**

| Form | Example | When to use | Risk |
|---|---|---|---|
| Index | `frame(0)` | Quick experiments, only one frame | Breaks if another frame is added before it |
| Name or id | `frame("mce_0_ifr")` | Frame has a stable `id` or `name` | Fails if the id is generated dynamically |
| WebElement | `frame(driver.findElement(By.cssSelector("iframe.editor")))` | Most cases; any locator strategy works | Element must exist; wrap in a wait |
| Wait and switch | `wait.until(frameToBeAvailableAndSwitchToIt(By.id("x")))` | Frame loads late | None; recommended default |

Details:

- **Nested frames**: an iframe within an iframe requires one `switchTo().frame(...)` per level, and `parentFrame()` to climb one level at a time. To reach a sibling frame, go up first (`parentFrame()` or `defaultContent()`), then down.
- **Waiting for frames**: `ExpectedConditions.frameToBeAvailableAndSwitchToIt(By)` waits and switches in one step:

```java
wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(By.id("payment-frame")));
```

- Frame switching is **independent of window switching**: switching to another window resets the frame context to that window's top level.
- A common sign that you need to switch: the element is plainly visible in DevTools, your locator is correct, and Selenium still cannot find it. Look upward in the DOM tree in DevTools for an `<iframe>` ancestor.
- The reverse mistake also happens: after working inside the frame, you forget to leave it, and a locator for a main-page element fails.

**Troubleshooting walk-through: frame errors.**

```text
org.openqa.selenium.NoSuchFrameException: no such frame: element is not a frame
```

or

```text
org.openqa.selenium.NoSuchFrameException: no such frame
```

**Diagnosis.** The first message means you passed a `WebElement` that is not an `<iframe>`/`<frame>` (perhaps a wrapper `div`). Choose the `<iframe>` tag itself. The second means a name, id, or index did not match any frame in the *current context*. If you are already inside a frame, you are searching for frames inside that frame; go back with `defaultContent()` first.

**Counting frames.** `driver.findElements(By.tagName("iframe")).size()` tells you how many iframes are in the current document.

### 10. A Reusable Window Helper

```java
package com.revature.qea.utils;

import org.openqa.selenium.NoSuchWindowException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.Set;

public class WindowUtils {

    private final WebDriver driver;
    private final WebDriverWait wait;

    public WindowUtils(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    /** Runs an action expected to open a new window, then switches to the new window. Returns the ORIGINAL handle. */
    public String switchToNewWindowAfter(Runnable actionThatOpensWindow) {
        String original = driver.getWindowHandle();
        Set<String> before = driver.getWindowHandles();

        actionThatOpensWindow.run();

        wait.until(d -> d.getWindowHandles().size() > before.size());

        for (String handle : driver.getWindowHandles()) {
            if (!before.contains(handle)) {
                driver.switchTo().window(handle);
                return original;
            }
        }
        throw new NoSuchWindowException("Expected a new window but none was found");
    }

    /** Closes the current window and returns to the given one. */
    public void closeCurrentAndSwitchTo(String handle) {
        driver.close();
        driver.switchTo().window(handle);
    }

    public void switchToWindowByTitleContains(String partialTitle) {
        for (String handle : driver.getWindowHandles()) {
            driver.switchTo().window(handle);
            if (driver.getTitle().contains(partialTitle)) {
                return;
            }
        }
        throw new NoSuchWindowException("No window title contains: " + partialTitle);
    }

    public void switchToFrame(org.openqa.selenium.By frameLocator) {
        wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(frameLocator));
    }

    public void backToMainPage() {
        driver.switchTo().defaultContent();
    }
}
```

**Line-by-line explanation of the key method `switchToNewWindowAfter`.**

1. It stores the original handle and a snapshot `before` of all handles.
2. `actionThatOpensWindow.run()` executes the code you passed in (the click). `Runnable` is a Java interface with one method `run()`; passing a lambda `() -> ...` lets the helper **take a snapshot of the window list, perform your click, and then compare**, which is the reliable way to detect the new window.
3. `wait.until(d -> d.getWindowHandles().size() > before.size())` is a lambda condition: "the number of windows is now greater than before". `d` is the driver the wait passes in. The wait polls until true or until 10 seconds pass.
4. The loop finds the handle that is **not in the snapshot**, switches to it, and returns the original handle so the caller can come back.
5. If no new handle appears, an informative `NoSuchWindowException` is thrown.

**Why a `final` snapshot.** The lambda in step 3 reads `before`; Java requires variables used inside lambdas to be *effectively final* (never reassigned). `before` is assigned once, so it qualifies.

Usage:

```java
WindowUtils windows = new WindowUtils(driver);
String original = windows.switchToNewWindowAfter(
        () -> driver.findElement(By.linkText("Click Here")).click());

System.out.println("Child title: " + driver.getTitle());
windows.closeCurrentAndSwitchTo(original);
```

**Using it from a page object (preview).** A page object method might read:

```java
public PrivacyPolicyPage openPrivacyPolicy() {
    String original = windows.switchToNewWindowAfter(() -> driver.findElement(privacyLink).click());
    return new PrivacyPolicyPage(driver, windows, original);
}
```

The test then never touches handles. The later lesson on the Page Object Model explains this pattern in full.

---

## Code Example: Windows, Tabs, and Frames

```java
package com.revature.qea.windows;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WindowType;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.Set;

public class WindowsDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        try {
            driver.manage().window().maximize();

            // ---------- Part 1: link that opens a new tab ----------
            driver.get("https://the-internet.herokuapp.com/windows");
            String original = driver.getWindowHandle();
            System.out.println("Original title: " + driver.getTitle());

            driver.findElement(By.linkText("Click Here")).click();
            wait.until(ExpectedConditions.numberOfWindowsToBe(2));

            for (String handle : driver.getWindowHandles()) {
                if (!handle.equals(original)) {
                    driver.switchTo().window(handle);
                    break;
                }
            }
            System.out.println("New window title: " + driver.getTitle());
            System.out.println("New window heading: " + driver.findElement(By.tagName("h3")).getText());

            driver.close();                              // close the new tab
            driver.switchTo().window(original);          // back to the first
            System.out.println("Back on: " + driver.getTitle());

            // ---------- Part 2: open our own tab ----------
            driver.switchTo().newWindow(WindowType.TAB);
            driver.get("https://www.saucedemo.com");
            Set<String> handles = driver.getWindowHandles();
            System.out.println("Open windows now: " + handles.size());
            driver.close();
            driver.switchTo().window(original);

            // ---------- Part 3: an iframe ----------
            driver.get("https://the-internet.herokuapp.com/iframe");
            wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(By.id("mce_0_ifr")));
            WebElement editor = driver.findElement(By.id("tinymce"));
            editor.clear();
            editor.sendKeys("Typed inside an iframe");
            System.out.println("Editor text: " + editor.getText());

            driver.switchTo().defaultContent();           // leave the frame
            System.out.println("Page heading: " + driver.findElement(By.tagName("h3")).getText());
        } finally {
            driver.quit();
        }
    }
}
```

**Explanation by part.**

- **Part 1** is the standard pattern from section 3, using the-internet's "Click Here" link, which opens a new tab titled "New Window". The `h3` of that page reads "New Window".
- **Part 2** opens a blank tab ourselves. `newWindow` already switches, so `get(...)` loads SauceDemo in the new tab. `handles.size()` is 2 (original plus new). Closing it and switching back restores the original.
- **Part 3** uses the frame wait. `mce_0_ifr` is the id of the TinyMCE iframe on that page. Inside the frame, the editable body has the id `tinymce`. After typing, `defaultContent()` returns to the main page, where the `h3` heading lives.
- `WebElement editor = ...` stores the element so we can reuse it.

**Expected console output (approximate).**

```text
Original title: The Internet
New window title: New Window
New window heading: New Window
Back on: The Internet
Open windows now: 2
Editor text: Typed inside an iframe
Page heading: An iFrame containing the TinyMCE WYSIWYG Editor
```

(The exact wording on third-party practice sites can change; adapt the assertions if so.)

**Observations to make while running it:**

- The title printed before and after the switch differs, proving the driver follows your switches.
- Without `switchTo().frame(...)` the `tinymce` lookup throws `NoSuchElementException`; try deleting that line and see.
- If you comment out `driver.switchTo().window(original)` after the `close()`, the next command throws `NoSuchWindowException`.

---

## Guided Lab: Three Windows and a Frame

**Goal.** Build a test class that proves you can control multiple windows, find them by title, and work inside nested frames.

1. Create `WindowLabTest` in `src/test/java`. Set up Chrome with a 10-second wait.
2. Add the `WindowUtils` class (section 10) to your utilities package.
3. **Test 1, one new tab.** Open `https://the-internet.herokuapp.com/windows`. Call `switchToNewWindowAfter` with a lambda that clicks "Click Here". Assert that the title is `New Window`. Call `closeCurrentAndSwitchTo(original)`. Assert the title is `The Internet`.
4. **Test 2, several tabs.** Open the same page. Click the link three times, waiting for the window count each time (`numberOfWindowsToBe(2)`, then 3, then 4). Print the title and URL of each handle. Then, for every handle that is not the original, switch to it and `close()`. Finally switch to the original and assert `getWindowHandles().size() == 1`.
5. **Test 3, nested frames.** Open `https://the-internet.herokuapp.com/nested_frames`. Switch to `frame-top`, then to `frame-middle`, read the `#content` text (expected `MIDDLE`). Call `parentFrame()` (now in top), switch to `frame-left` and read `LEFT`. Call `defaultContent()` and switch to `frame-bottom` to read `BOTTOM`.
6. Run the class.

**Expected output.**

```text
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
```

**Hint for step 5.** Frame names on that page are `frame-top`, `frame-left`, `frame-middle`, `frame-right`, `frame-bottom`. The top frame contains the left, middle, and right frames as children, so you must enter `frame-top` first. The bottom frame is a sibling of the top one at the page level, so you must leave with `defaultContent()` before entering it.

**Reference sketch for step 5.**

```java
driver.switchTo().frame("frame-top");
driver.switchTo().frame("frame-middle");
Assert.assertEquals(driver.findElement(By.id("content")).getText(), "MIDDLE");
driver.switchTo().parentFrame();
driver.switchTo().frame("frame-left");
Assert.assertTrue(driver.findElement(By.tagName("body")).getText().contains("LEFT"));
driver.switchTo().defaultContent();
driver.switchTo().frame("frame-bottom");
Assert.assertTrue(driver.findElement(By.tagName("body")).getText().contains("BOTTOM"));
```

**Stretch.** Switch to a window by URL instead of by title and compare which approach is more stable.

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Not switching after a new tab opens | `NoSuchElementException` on the new page's elements | `switchTo().window(newHandle)` |
| Assuming the new handle is "the last in the Set" | Random failures | Choose the handle that is not the original |
| Reading `getWindowHandles()` immediately after the click | Only one handle yet | Wait with `numberOfWindowsToBe(n)` |
| Closing the current window and not switching back | `NoSuchWindowException` | `switchTo().window(original)` |
| Forgetting that `quit()` closes **all** windows | Surprise when other windows vanish | Use `close()` for a single window |
| Searching for an element inside an iframe from the top-level page | `NoSuchElementException` | `switchTo().frame(...)` first |
| Not leaving a frame after use | Later steps search the wrong document | `defaultContent()` or `parentFrame()` |
| Switching by frame index when the page adds a frame | Wrong frame | Switch by locator/element |
| Storing handles across test runs | Invalid handles | Get handles fresh in each run |
| Reading the title of a new tab before it loads | Empty title or `about:blank` | Wait for the title or URL to contain the expected text |
| Expecting two tabs to behave as two users | Shared login | Use two driver instances for separate sessions |

---

## Practice Exercises

1. **New tab.** On `https://the-internet.herokuapp.com/windows`, click the link, switch to the new tab, assert its heading is "New Window", close it, and verify you are back on the original page by title.
2. **Multiple windows.** On the same page open the link three times (so there are 4 windows). Loop through all handles and print each title and URL. Then close all but the original window.
3. **Switch by title.** Write `switchToWindowByTitleContains` and test it with the windows from exercise 2.
4. **Own tab.** Use `newWindow(WindowType.TAB)` to log in to SauceDemo as `standard_user` in one tab and open the login page in another tab, then switch between them to observe session behaviour. (Hint: look at what each tab shows, and think about cookies.)
5. **Frames.** On `https://the-internet.herokuapp.com/nested_frames`, read the text in the **left**, **middle**, **right**, and **bottom** frames. Use `parentFrame()` and `defaultContent()` appropriately.
6. **Editor.** On `/iframe`, clear the editor and type a sentence, then read it back and assert equality.
7. **Break it.** Remove each critical line in the new-tab example (the wait, the switch, the switch back) one at a time, and record the exception each produces.
8. **Social link.** On SauceDemo (after login), scroll to the footer and click the Twitter/X link. Switch to the new tab, assert the URL contains the expected domain, close it, and confirm the cart icon is still reachable on the original page.
9. **Window count helper.** Write `int openWindowCount()` and use it to assert that no extra windows remain after a test.
10. **Frame helper.** Write `String textInFrame(By frameLocator, By elementLocator)` that enters a frame, reads text, and always returns to the main page, even if reading fails (use `try/finally`).
11. **Think.** A colleague says "I will just use `Thread.sleep(3000)` after clicking the link and then take the last handle." List three things that can go wrong with that approach.
12. **Project 2 prep.** List every place in your Project 2 site where a new window, a pop-up, or an iframe could appear. For each, decide which page object will own the switching code.

---

## Solutions and Hints

**1. New tab.** Use the pattern from section 3. Assertions: `Assert.assertEquals(driver.findElement(By.tagName("h3")).getText(), "New Window");` after switching; after returning, `Assert.assertEquals(driver.getTitle(), "The Internet");`.

**2. Multiple windows.**

```java
String original = driver.getWindowHandle();
for (int i = 2; i <= 4; i++) {
    driver.findElement(By.linkText("Click Here")).click();
    wait.until(ExpectedConditions.numberOfWindowsToBe(i));
}
for (String h : driver.getWindowHandles()) {
    driver.switchTo().window(h);
    System.out.println(driver.getTitle() + " | " + driver.getCurrentUrl());
}
for (String h : driver.getWindowHandles()) {
    if (!h.equals(original)) {
        driver.switchTo().window(h);
        driver.close();
    }
}
driver.switchTo().window(original);
```

Note that iterating over `getWindowHandles()` while closing is safe here because that call returned a new `Set` snapshot that is not tied to the live browser state.

**3. Switch by title.** Use the method in section 10. Note that all new windows share the same title, so the first match wins; this exercise shows the limits of title-based switching.

**4. Own tab.** Tabs share cookies in one browser profile, so after logging in in tab one, the second tab may already show the inventory page when you open the site. For truly independent sessions you need a second `WebDriver`.

**5. Frames.** See the reference sketch in the lab. If the right frame text lookup fails, check that you went back to `frame-top` first: `defaultContent()` then `frame("frame-top")` then `frame("frame-right")`.

**6. Editor.**

```java
wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(By.id("mce_0_ifr")));
WebElement body = driver.findElement(By.id("tinymce"));
body.clear();
body.sendKeys("Selenium frames");
Assert.assertEquals(body.getText(), "Selenium frames");
driver.switchTo().defaultContent();
```

**7. Break it.** Expected results: without the wait, intermittent failure where no new handle is found (your loop never switches and later lookups fail with `NoSuchElementException`); without the switch, `NoSuchElementException` on the new page's elements; without switching back after `close()`, `NoSuchWindowException: target window already closed`.

**8. Social link.** Hint: use `By.cssSelector(".social_twitter a")` after confirming it in DevTools; use `WindowUtils.switchToNewWindowAfter`; check `driver.getCurrentUrl().contains("twitter.com")` or `x.com` (the site may redirect; accept either). Close with `closeCurrentAndSwitchTo(original)`.

**9. Window count helper.**

```java
public int openWindowCount() {
    return driver.getWindowHandles().size();
}
```

Use `Assert.assertEquals(windows.openWindowCount(), 1)` in teardown logic or at the end of the test.

**10. Frame helper.**

```java
public String textInFrame(By frameLocator, By elementLocator) {
    wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(frameLocator));
    try {
        return driver.findElement(elementLocator).getText();
    } finally {
        driver.switchTo().defaultContent();
    }
}
```

The `finally` block guarantees the driver leaves the frame even when `findElement` throws, so one failing lookup does not corrupt later steps.

**11. Think.** (a) The window may open faster or slower than three seconds, so the test is either slow or flaky. (b) `Set` order is not guaranteed, so "the last handle" may be the original. (c) If the link opens nothing (a bug), the test just takes the wrong handle with no clear error, hiding the real defect.

**12. Project 2 prep.** Answers vary; typical: footer social links (footer component or base page), payment or terms links (checkout page), embedded editors (the page that owns the form). Keep switching code in the page object whose action causes the new window, and return the next page object.

---

## Self-Check Questions

1. **How many windows can Selenium control at once?** One window (and, within it, one frame) at a time; you must switch explicitly.
2. **Why is `getWindowHandles()` a `Set` and why does that matter?** It is unordered, so you cannot rely on position; compare with the original handle or a snapshot instead.
3. **What happens if you call `driver.close()` on the only open window?** The window closes and the session ends, like `quit()` in effect.
4. **What is the difference between `parentFrame()` and `defaultContent()`?** `parentFrame()` climbs one level; `defaultContent()` returns to the top-level document.
5. **How do you wait for a frame to be ready and enter it in one step?** `ExpectedConditions.frameToBeAvailableAndSwitchToIt(locator)`.
6. **Why must you wait before reading `getWindowHandles()` after clicking a link?** The new window may not exist yet; waiting for `numberOfWindowsToBe(n)` prevents missing it.
7. **Do two tabs in the same driver represent two separate user sessions?** No, they share cookies and storage.
8. **Your locator is correct and visible in DevTools yet not found. What should you check first?** Whether the element is inside an `<iframe>`, or the driver is on the wrong window.

---

## Summary

- Every window/tab has a unique **handle**; Selenium controls **one window at a time** and does not follow new windows automatically.
- `getWindowHandle()` returns the current handle; `getWindowHandles()` returns a **Set** of all (unordered).
- Pattern: remember the original, trigger the new window, **wait** for the count to rise, switch to the handle that is not the original, work, `close()`, switch back.
- `switchTo().newWindow(WindowType.TAB/WINDOW)` opens and switches in one step.
- `close()` closes the current window; `quit()` ends the whole session.
- **iFrames** are separate documents: use `switchTo().frame(...)` to enter and `parentFrame()` / `defaultContent()` to leave.
- Encapsulate switching logic in a helper or page-object method to keep tests readable.

---

## Additional Resources

- Selenium documentation, *Windows and tabs*: https://www.selenium.dev/documentation/webdriver/interactions/windows/
- Selenium documentation, *Working with iframes and frames*: https://www.selenium.dev/documentation/webdriver/interactions/frames/
- Selenium Java API, `WebDriver.TargetLocator`: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebDriver.TargetLocator.html
