# Element Interactions

## Learning Objectives

By the end of this lesson you will be able to:

- Perform the core user actions with Selenium: `click()`, `sendKeys()`, `clear()`, and `submit()`.
- Send **special keys** (Enter, Tab, Escape, arrows) and key combinations using the `Keys` class.
- Work with **text inputs, textareas, checkboxes, radio buttons, and links**.
- Upload a file using `sendKeys` on a file input.
- Read element state (`getText`, `getAttribute`, `isDisplayed`, `isEnabled`, `isSelected`) **before and after** an interaction to verify results.
- Scroll an element into view and use the **JavaScript executor** as a last resort.
- Explain and fix the main interaction exceptions: `ElementNotInteractableException`, `ElementClickInterceptedException`, `StaleElementReferenceException`, and `InvalidElementStateException`.
- Write safe, reusable interaction helpers that combine waits (from the previous lesson) with actions.

---

## Why This Matters

Finding an element is only half of automation; the other half is *doing* something with it: typing a username, ticking a box, clicking Submit. These actions are what make an automated test imitate a real user. A well-written interaction does what a human would do (clicks the visible button, types into the focused field), which means your test finds the same bugs a human would.

You already used `click()` and `sendKeys()` in Monday's login example. Today we study them properly: what exactly they do, when they fail, and how to write them robustly. In your **Project 2 milestone**, login, search, and form-filling flows are built entirely from these actions combined with the waits you learned in the previous lesson (`WebDriverWait`, `ExpectedConditions`).

### Connecting to what you know

| You learned | Used today for |
|---|---|
| Monday: `By` locators and `findElement` | Getting the element we then act on |
| Monday: `driver.get`, `getCurrentUrl`, `getTitle` | Verifying that an action (login, link click) really navigated |
| Monday: screenshots | Capturing evidence when an interaction fails |
| Today: explicit waits | Making sure the element is ready *before* we act on it |

### Real-world scenario

A registration page has: username, password, a "Remember me" checkbox, a terms checkbox, a country list, and a Submit button. A manual tester completes it in 30 seconds. To automate it you need to type into inputs, toggle checkboxes **only if needed**, choose from the list (the next lesson), click Submit, and then verify a welcome message. Every one of those actions is covered here, and each can fail in a specific, predictable way that you will learn to recognise.

---

## The Concept

### 1. What "Interacting" Means in Selenium

**What it is.** An *interaction* is any command that changes the page or the element's state as a user would: clicking, typing, clearing, uploading, scrolling. These are methods on the `WebElement` interface (for example `element.click()`).

**Why Selenium is strict.** Selenium tries to behave like a real user. Before it acts on an element it checks that the action is possible:

- The element is **displayed** (visible, non-zero size).
- The element is **enabled** (not `disabled`).
- For clicks, the element's click point is **not covered** by another element.

If these checks fail Selenium throws an exception rather than "cheating". That is a feature: if a real user could not click it, your test should not be able to either.

> **Analogy:** Selenium is a very literal robot hand at a vending machine. It will not press a button it cannot see, a button that is greyed out, or a button hidden behind a glass panel. It reports exactly which of those problems it hit.

**The two kinds of `WebElement` methods.**

| Kind | Methods | Changes the page? |
|---|---|---|
| **Actions** | `click()`, `sendKeys()`, `clear()`, `submit()` | Yes |
| **Queries** | `getText()`, `getAttribute()`, `isDisplayed()`, `isEnabled()`, `isSelected()`, `getTagName()`, `getCssValue()` | No |

A good test uses both: an action, then a query to confirm the effect.

### 2. `click()`

```java
driver.findElement(By.id("login-button")).click();
```

What happens when this line runs:

1. `driver.findElement(By.id("login-button"))` asks the browser for the element; you receive a `WebElement` reference.
2. `.click()` asks the driver to scroll the element into view if needed.
3. The driver computes the element's **center point** and checks that the element at that point is the target (or its child). If something else is there, `ElementClickInterceptedException`.
4. The driver sends a real mouse press and release to that point.
5. If the click starts a page navigation, the command waits until the page load finishes (according to the page load strategy). If the click only triggers JavaScript, it returns at once, which is why the waits from the previous lesson matter.

Facts to remember:

- Works on buttons, links, checkboxes, radio buttons, options (in a list), images, and any other clickable element.
- Clicks the **center**; if the center is covered by a small badge or tooltip but the edges are free, the click is still "intercepted".
- `click()` returns `void`; to check the result you must query something else (URL, text, badge).

**Typical failures:**

| Exception | Meaning | Fix |
|---|---|---|
| `ElementNotInteractableException` | Element exists but is hidden, disabled, or has no size | Wait for it to become clickable; check if another step reveals it |
| `ElementClickInterceptedException` | Another element is on top of it (cookie banner, modal, sticky header) | Wait for the overlay to close; scroll the target to the middle of the screen; close the banner |
| `StaleElementReferenceException` | The page re-rendered; your element reference is dead | Find the element again |

**Troubleshooting walk-through: intercepted click.** You run a test and see:

```
org.openqa.selenium.ElementClickInterceptedException: element click intercepted:
Element <button id="checkout"> is not clickable at point (512, 610).
Other element would receive the click: <div id="cookie-banner" class="sticky-bottom">...</div>
```

Read it in three parts: (1) *what you tried* - `<button id="checkout">`; (2) *where* - point (512, 610); (3) *what is in the way* - `cookie-banner`. The fix is to deal with the banner (accept it as part of test setup, or wait until it is gone), not to force the click.

```java
wait.until(ExpectedConditions.elementToBeClickable(By.id("accept-cookies"))).click();
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id("cookie-banner")));
wait.until(ExpectedConditions.elementToBeClickable(By.id("checkout"))).click();
```

### 3. `sendKeys()`: Typing Text

```java
WebElement username = driver.findElement(By.id("user-name"));
username.sendKeys("standard_user");
```

- Simulates typing, character by character, into the element (the element receives focus first).
- **It appends** to whatever is already in the field. If the field already contains "abc" and you type "xyz", it becomes "abcxyz".
- Works on `<input>` and `<textarea>`; not on non-editable elements (error: `ElementNotInteractableException` or `InvalidElementStateException`).
- Can accept several arguments, which are typed in order: `sendKeys("hello", " ", "world")`.

Signature: `void sendKeys(CharSequence... keysToSend)`. `CharSequence...` is a **varargs** parameter: "zero or more text values". `String` and `Keys` are both `CharSequence`, which is why you can mix them in one call: `sendKeys("abc", Keys.TAB)`.

**What happens when `sendKeys("standard_user")` runs:** the element is focused; for each character the browser receives a key-down, a key-press that inserts the character, and a key-up; the field's `input` event fires for each character, so JavaScript validation ("username too short") reacts as it would for a human.

**Special input types.**

| Input type | How to use `sendKeys` |
|---|---|
| `type="text"`, `"email"`, `"password"`, `"search"` | Type normally |
| `type="number"` | Type digits (`"42"`); letters are ignored by the browser |
| `type="date"` | Browser-dependent; for Chrome type digits in the browser's locale format, e.g. `"12252026"` for `mm/dd/yyyy` |
| `type="file"` | Send an absolute path (section 10) |
| `<textarea>` | Type normally; `"\n"` inserts a newline, `Keys.ENTER` also works |
| `readonly` or `disabled` fields | Not allowed; fails with an exception |

### 4. `clear()`

```java
username.clear();
```

- Erases the contents of an editable text field and fires the `change` event.
- Fails with `InvalidElementStateException` if the element is not editable (for example, a read-only field).
- Some modern JavaScript-heavy inputs (React-controlled fields) do not respond properly to `clear()`. Workarounds: select-all and delete using keys.

```java
// Reliable alternative for stubborn inputs (Windows/Linux: CONTROL, macOS: COMMAND)
field.sendKeys(Keys.chord(Keys.CONTROL, "a"), Keys.BACK_SPACE);
```

Explanation: `Keys.chord(Keys.CONTROL, "a")` builds a single string meaning "hold Control, press a, release", i.e. select all; `Keys.BACK_SPACE` then deletes the selection. On macOS use `Keys.COMMAND` instead of `Keys.CONTROL`. A portable trick: choose the key at run time with `System.getProperty("os.name").toLowerCase().contains("mac") ? Keys.COMMAND : Keys.CONTROL`.

**Safe typing pattern** (clear first, then type):

```java
public void type(WebElement field, String text) {
    field.clear();
    field.sendKeys(text);
}
```

**Worked example: why clear matters.** SauceDemo remembers nothing, but many forms are pre-filled (an "edit profile" page shows your existing email). If you run `email.sendKeys("new@test.com")` without clearing, the value becomes `old@test.comnew@test.com`, the server rejects it, and the test fails on a line that looks perfectly fine. Printing `getAttribute("value")` right after typing makes this obvious.

### 5. The `Keys` Class: Special Keys

`sendKeys` can send non-text keys via the `Keys` enum:

| Key constant | Effect |
|---|---|
| `Keys.ENTER` / `Keys.RETURN` | Press Enter (submits many forms) |
| `Keys.TAB` | Move focus to the next field |
| `Keys.ESCAPE` | Close dialogs, cancel editing |
| `Keys.BACK_SPACE`, `Keys.DELETE` | Delete characters |
| `Keys.ARROW_DOWN`, `ARROW_UP`, `ARROW_LEFT`, `ARROW_RIGHT` | Move in lists, sliders |
| `Keys.PAGE_DOWN`, `Keys.PAGE_UP`, `Keys.HOME`, `Keys.END` | Scroll / move caret |
| `Keys.SPACE` | Space bar (toggles checkboxes, presses buttons) |
| `Keys.F5` | Refresh |

```java
searchBox.sendKeys("selenium tutorial", Keys.ENTER);       // type and press Enter
passwordField.sendKeys("secret_sauce", Keys.TAB);          // type, then move to next field
```

`Keys` is an **enum**: a fixed list of named constants. You refer to a constant as `Keys.ENTER`. Because each constant is also a `CharSequence`, it can follow ordinary text in the same `sendKeys` call.

**Key combinations** with `Keys.chord(...)`:

```java
String selectAll = Keys.chord(Keys.CONTROL, "a");
field.sendKeys(selectAll);
field.sendKeys(Keys.chord(Keys.CONTROL, "c"));   // copy
```

**When to use keys instead of clicking:**

- To submit a form in a field where pressing Enter is the real user behaviour (search boxes).
- To move through a form with Tab when testing keyboard accessibility.
- To close a dialog with Escape when that is the feature under test.

> Press-and-hold sequences, drag and drop, and mouse hover use the **Actions API**, which is the subject of **Wednesday's lesson**. Today we only use `sendKeys` with `Keys`.

### 6. `submit()`

```java
passwordField.submit();   // submits the enclosing <form>
```

- Works only on an element inside a `<form>` (or the form itself). If there is no enclosing form you get `NoSuchElementException: Element was not in a form`.
- It is a legacy convenience. If the page uses JavaScript to handle the button, `submit()` may skip that logic. **Prefer clicking the actual Submit button** (or pressing `Keys.ENTER`), which mirrors what a user does.

| Way to submit | Mirrors a user? | Runs the button's JavaScript? | Recommended |
|---|---|---|---|
| `click()` on the Submit button | Yes | Yes | **Yes, default choice** |
| `sendKeys(..., Keys.ENTER)` in a field | Yes | Usually | Yes, for search boxes |
| `element.submit()` | No | Not always | Only for old plain-HTML forms |

### 7. Reading Back: Verifying an Interaction

After acting, confirm the effect. Combine the find-method knowledge from Monday:

```java
username.sendKeys("standard_user");
String typed = username.getAttribute("value");        // what's in the box?
// assertion: typed.equals("standard_user")

WebElement checkbox = driver.findElement(By.id("remember"));
checkbox.click();
boolean ticked = checkbox.isSelected();               // did it toggle?
```

The query methods in detail:

| Method | Returns | Use it to check |
|---|---|---|
| `getText()` | Visible text of the element | Messages, labels, button captions |
| `getAttribute("value")` | The current value of an input | What was typed; `getText()` on an `<input>` returns empty |
| `getAttribute("class")` / `("href")` / `("disabled")` | Other attributes | Active CSS class, link target, disabled state |
| `isDisplayed()` | `true` if visible | Presence of banners, spinners |
| `isEnabled()` | `false` if `disabled` | Whether a button can be pressed |
| `isSelected()` | Checked state | Checkboxes, radio buttons, selected options |
| `getCssValue("color")` | A computed CSS value | Visual checks like error text turning red |

Why `getText()` does not work on an input: an `<input>` has no text between tags; its content lives in the `value` attribute/property, hence `getAttribute("value")`. (Selenium 4 also offers `getDomProperty("value")`, which reads the live property; for beginners `getAttribute("value")` is sufficient and returns the current text.)

### 8. Checkboxes and Radio Buttons

A checkbox's `click()` **toggles** it. Therefore "tick this box" must check the current state first, or running the test twice would untick it:

```java
public void setCheckbox(WebElement checkbox, boolean shouldBeChecked) {
    if (checkbox.isSelected() != shouldBeChecked) {
        checkbox.click();
    }
}
```

Reading the logic: `isSelected()` is the *current* state, `shouldBeChecked` the *desired* state. If they differ, one click fixes it; if they are equal, do nothing. The `!=` between two booleans acts as "are they different?".

| Current | Desired | `!=` result | Action |
|---|---|---|---|
| unchecked | check | true | click |
| checked | check | false | nothing |
| checked | uncheck | true | click |
| unchecked | uncheck | false | nothing |

Radio buttons: clicking an unselected radio selects it (and deselects the others in the same group); clicking a selected radio does nothing. Verify with `isSelected()`.

```java
List<WebElement> radios = driver.findElements(By.name("shipping"));
radios.get(1).click();
System.out.println(radios.get(1).isSelected());   // true
System.out.println(radios.get(0).isSelected());   // false - same group
```

**Styled checkboxes:** many modern sites hide the real `<input type="checkbox">` and display a styled `<label>` or `<span>` instead. The hidden input throws `ElementNotInteractableException`, so you click the **label** (or the styled element), then check `isSelected()` on the real input.

### 9. Links

```java
driver.findElement(By.linkText("Forgot password?")).click();
```

Links navigate; you will then typically check the URL (see *Navigation Methods*) or wait for a key element on the new page. If the link opens in a new tab or window, you must switch to it; this is covered on **Wednesday (Window Handling)**.

To check where a link goes **without** clicking it, read its `href`:

```java
String target = driver.findElement(By.linkText("Forgot password?")).getAttribute("href");
```

This is useful for broken-link checks and for links that open new tabs.

### 10. Uploading a File

For a standard `<input type="file">`, do **not** try to click it (that opens a native operating-system dialog that Selenium cannot control). Instead, send the **absolute path** of the file directly to the input:

```java
WebElement upload = driver.findElement(By.id("file-upload"));
upload.sendKeys("C:\\temp\\test-data\\sample.txt");   // absolute path
driver.findElement(By.id("file-submit")).click();
```

To build a portable path:

```java
String path = new java.io.File("src/test/resources/sample.txt").getAbsolutePath();
upload.sendKeys(path);
```

The file must exist on the machine where the **browser** runs; this is important later for remote/CI setups.

Why this works: the file input is a text-like control that accepts a file path; setting it directly bypasses the operating-system picker. In Java strings a backslash must be doubled (`"C:\\temp"`), which is why `File.getAbsolutePath()` is friendlier: it builds the right separator for your OS. A good place to store test files is `src/test/resources`, which Maven creates for you.

### 11. Scrolling and the JavaScript Executor

Selenium scrolls automatically before a click. Sometimes you need explicit control, or an element is covered by a sticky header after auto-scroll. Selenium can run JavaScript in the page through `JavascriptExecutor`:

```java
JavascriptExecutor js = (JavascriptExecutor) driver;

// Scroll an element to the center of the viewport (avoids sticky headers)
js.executeScript("arguments[0].scrollIntoView({block: 'center'});", element);

// Scroll to the bottom of the page
js.executeScript("window.scrollTo(0, document.body.scrollHeight);");
```

`arguments[0]` is how you pass a Java `WebElement` into the script.

Line by line: the cast `(JavascriptExecutor) driver` tells Java "this driver also supports running scripts" (every browser driver does, but the `WebDriver` interface does not declare it). `executeScript(String script, Object... args)` runs the text as JavaScript inside the page; extra arguments are available as `arguments[0]`, `arguments[1]`, and so on. `scrollIntoView({block:'center'})` is a browser function that scrolls so the element sits in the middle of the window.

**JavaScript click, a last resort:**

```java
js.executeScript("arguments[0].click();", element);
```

This bypasses Selenium's checks (it will "click" an element a user cannot see or reach). It may hide **real bugs** (for example a button permanently covered by a modal). Use it only when you have confirmed that the underlying UI is working and there is a legitimate technical reason; add a comment explaining why.

**Order of escalation when a click fails:**

1. Wait for `elementToBeClickable`.
2. Wait for overlays/spinners to disappear.
3. Scroll the element to the center, then click.
4. Close any banner or modal that is in the way.
5. Only then, JavaScript click with a comment, and mention it in code review.

### 12. Interaction Exceptions Summary

| Exception | Common cause | What to try |
|---|---|---|
| `NoSuchElementException` | Wrong locator or element not yet present | Check locator; wait for presence/visibility |
| `ElementNotInteractableException` | Hidden, disabled, zero-size, off-screen, or behind a styled replacement | Wait for clickable; click the visible label; scroll into view |
| `ElementClickInterceptedException` | Another element covers the target | Wait for overlay to disappear; close the banner; scroll to center |
| `StaleElementReferenceException` | DOM re-rendered | Re-locate right before using it |
| `InvalidElementStateException` | Typing/clearing into non-editable element | Verify it is an editable field (not read-only/disabled) |
| `TimeoutException` | An explicit wait expired | Check locator/condition; increase timeout if appropriate |

**Diagnosis flow when an interaction fails:**

1. Read the exception class; use the table above.
2. Read the message; Selenium often names the covering element or the problem.
3. Take a screenshot (Monday) at the failure point to see what the user would see.
4. Reproduce by hand in the browser with DevTools open.
5. Fix the cause (wait, locator, overlay), re-run several times.

### 13. Combining Waits and Actions: Robust Helpers

The most stable interaction pattern is **wait -> act -> verify**:

```java
public class SafeActions {
    private final WebDriverWait wait;

    public SafeActions(WebDriver driver) {
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void click(By locator) {
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
    }

    public void type(By locator, String text) {
        WebElement field = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        field.clear();
        field.sendKeys(text);
    }

    public void setCheckbox(By locator, boolean shouldBeChecked) {
        WebElement box = wait.until(ExpectedConditions.presenceOfElementLocated(locator));
        if (box.isSelected() != shouldBeChecked) {
            box.click();
        }
    }

    public String text(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText();
    }
}
```

Each method *waits first*, using locators (not stored elements) so there is no stale-reference problem.

Why this shape: a method takes a `By` (a recipe for finding the element) instead of a `WebElement` (a one-time reference). The method can therefore re-find the element at the exact moment it needs it. This class is a **helper class**; tomorrow you will see how helpers like this become the foundation for Page Objects (covered on Wednesday). Note `setCheckbox` waits for *presence*, not visibility, so it also works for styled checkboxes whose real input is hidden (but then `click()` on it would fail; in that case click the label instead).

---

## Code Example: A Complete Login and Search-Style Flow

```java
package com.revature.qea.interactions;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class InteractionsDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        try {
            driver.manage().window().maximize();

            // --- 1. Typing, clearing, special keys: the login form ---
            driver.get("https://www.saucedemo.com");
            WebElement username = wait.until(
                    ExpectedConditions.visibilityOfElementLocated(By.id("user-name")));
            username.sendKeys("wrong_user");
            username.clear();                                   // remove the wrong text
            username.sendKeys("standard_user");
            System.out.println("Typed: " + username.getAttribute("value"));

            WebElement password = driver.findElement(By.id("password"));
            password.sendKeys("secret_sauce", Keys.ENTER);      // Enter submits the form

            wait.until(ExpectedConditions.urlContains("inventory"));
            System.out.println("Logged in: " + driver.getCurrentUrl());

            // --- 2. Click and verify state change ---
            By addBackpack = By.id("add-to-cart-sauce-labs-backpack");
            wait.until(ExpectedConditions.elementToBeClickable(addBackpack)).click();
            String badge = wait.until(ExpectedConditions.visibilityOfElementLocated(
                    By.className("shopping_cart_badge"))).getText();
            System.out.println("Cart badge: " + badge);                    // 1

            // --- 3. Scroll to the footer using JavaScript ---
            WebElement footer = driver.findElement(By.className("footer"));
            ((JavascriptExecutor) driver)
                    .executeScript("arguments[0].scrollIntoView({block:'center'});", footer);

            // --- 4. Checkboxes: toggle safely ---
            driver.get("https://the-internet.herokuapp.com/checkboxes");
            for (WebElement box : driver.findElements(By.cssSelector("#checkboxes input"))) {
                if (!box.isSelected()) {
                    box.click();
                }
                System.out.println("Checked? " + box.isSelected());
            }

            // --- 5. File upload ---
            driver.get("https://the-internet.herokuapp.com/upload");
            String path = new java.io.File("pom.xml").getAbsolutePath();
            driver.findElement(By.id("file-upload")).sendKeys(path);
            driver.findElement(By.id("file-submit")).click();
            String uploaded = wait.until(ExpectedConditions.visibilityOfElementLocated(
                    By.id("uploaded-files"))).getText();
            System.out.println("Uploaded file: " + uploaded);

        } finally {
            driver.quit();
        }
    }
}
```

**Walkthrough notes:**

- Step 1 shows `sendKeys`, `clear`, then `sendKeys(..., Keys.ENTER)`.
- Step 2 waits for clickability, clicks, then **verifies** the effect by reading the cart badge.
- Step 3 uses the JavaScript executor purely to scroll.
- Step 4 uses `isSelected()` before clicking, so the result does not depend on the starting state.
- Step 5 uploads a file by sending its absolute path (here, the project's own `pom.xml`, which always exists).

**Line-by-line commentary on the trickier parts.**

- `driver.manage().window().maximize();` makes the window large so that responsive layouts do not hide elements behind a mobile menu. Many "element not interactable" errors in CI come from small default window sizes.
- `username.sendKeys("wrong_user"); username.clear();` is deliberate: it proves that clear removes text, and the printed value `standard_user` (not `wrong_userstandard_user`) shows that it worked.
- `password.sendKeys("secret_sauce", Keys.ENTER)` types and then presses Enter in one call; the browser treats Enter in a form field as "submit the form", as for a human.
- `wait.until(ExpectedConditions.urlContains("inventory"))` is the **evidence** that login worked. Without it, the next line could run while the page is still the login page.
- The `for (WebElement box : driver.findElements(...))` loop is an *enhanced for loop*: it visits each element in the list. Inside, `if (!box.isSelected())` means "if not already ticked", so the loop is safe to run repeatedly. On the-internet's checkboxes page, the first box starts unchecked and the second starts checked, so you will see `true` printed twice at the end.
- `new java.io.File("pom.xml").getAbsolutePath()` converts a path relative to the project folder (where you run the program) into a full path such as `/home/user/project/pom.xml`.

**Expected output (approximately):**

```
Typed: standard_user
Logged in: https://www.saucedemo.com/inventory.html
Cart badge: 1
Checked? true
Checked? true
Uploaded file: pom.xml
```

---

## Hands-On Lab: Form-Filling Flow for Project 2 (about 45 minutes)

**Goal:** build and verify a reusable login-plus-form flow using `SafeActions`.

1. In your Project 2 Maven project, create `SafeActions` (section 13). Add a `uploadFile(By locator, String relativePath)` method that converts the path to absolute and calls `sendKeys` (wait for **presence**, not visibility: file inputs are sometimes hidden).
2. Create `LoginLab` with a `main` method. Using `SafeActions`, log in to `https://the-internet.herokuapp.com/login` with `tomsmith` / `SuperSecretPassword!` (locators: `#username`, `#password`, `button[type='submit']`).
3. After clicking, read the flash message `By.id("flash")` and print it. **Expected:** it contains `You logged into a secure area!`.
4. Add a **negative case**: log out (click `a[href='/logout']`), log in with the password `wrong`, and verify that the flash text contains `Your password is invalid!`.
5. Navigate to `/checkboxes` and use `setCheckbox` twice for each box (desired state `true` then `false`); print `isSelected()` after each call. **Expected:** `true`, `false` repeatedly, never an exception, whatever the starting state.
6. Navigate to `/inputs` (a number field). Type `42`, press `Keys.ARROW_UP` twice, and read `getAttribute("value")`. **Expected:** `44`.
7. Navigate to `/key_presses`, click the input, send `Keys.TAB`, and read `#result`. **Expected:** `You entered: TAB`.
8. Deliberately break one locator (change `#flash` to `#flsh`), observe the `TimeoutException` (message names the locator), then fix it.
9. Add a `try/catch` that takes a screenshot (your Monday helper) when any step fails, then rethrows.

If step 6 prints something else, check that you clicked the field first so it has focus; `sendKeys` focuses it automatically, but only if the element was found correctly.

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Assuming `sendKeys` replaces text | Text appended to existing content | `clear()` first |
| Clicking a checkbox without checking its state | Toggles it off if already on | Check `isSelected()` first |
| Using `submit()` on non-form elements | Exception or skipped JS logic | Click the Submit button / press Enter |
| Trying to click a file input | Native dialog opens; test hangs | `sendKeys(absolutePath)` |
| Using a relative path for upload | File not found | `new File(...).getAbsolutePath()` |
| Reusing a stored `WebElement` across page updates | Stale reference | Locate again, or wait on a `By` |
| Overusing JavaScript clicks | Hides real UI bugs | Fix the cause (wait, scroll, close overlay) |
| Acting immediately after navigation | Element not ready | Wait first (previous lesson) |
| Using `getText()` to read what was typed into an input | Returns empty string | `getAttribute("value")` |
| Forgetting `Keys.COMMAND` on macOS | Select-all chord does nothing | Pick the key by operating system |

---

## Practice Exercises

1. **Login variations.** Automate SauceDemo logins for `standard_user` (success), `locked_out_user` (error message), and a wrong password. For each, assert on the URL or the error text. Try submitting by clicking the button and by pressing `Keys.ENTER`.
2. **Clear vs. chord.** Type text into a field, then erase it using (a) `clear()` and (b) `Keys.chord(Keys.CONTROL, "a"), Keys.BACK_SPACE`. Confirm with `getAttribute("value")`.
3. **Safe checkbox.** Write `setCheckbox(By, boolean)` and call it twice with `true`; verify the box remains ticked.
4. **Add three items.** On the SauceDemo inventory page, add three products to the cart and assert that the cart badge equals "3". Then remove one and assert "2".
5. **Upload test.** Upload a small text file on `https://the-internet.herokuapp.com/upload` and assert the displayed file name.
6. **Key presses.** On `https://the-internet.herokuapp.com/key_presses`, send several keys (`Keys.TAB`, `Keys.SPACE`, `"a"`) and read the "You entered:" result text each time.
7. **Intercepted click.** On `https://the-internet.herokuapp.com/entry_ad` (a modal on first load), try clicking the page content while the modal is visible. What exception do you get? Fix it properly (close the modal) rather than with a JavaScript click.
8. **Reflect:** why is a JavaScript click considered a risk to test quality? Give an example of a bug it could hide.
9. **Number field.** On `/inputs`, type `5`, press `ARROW_UP` three times, and assert the value is `8`. Then `clear()` and assert that the value is empty.
10. **State queries.** On `/dynamic_controls`, record `isEnabled()` for the text input before and after clicking "Enable" (with a wait in between). Why is a wait required?
11. **Typo hunt.** The following snippet fails on the second run of a test. Explain why and fix it: `driver.findElement(By.id("remember")).click(); assertTrue(box.isSelected());`
12. **Project 2 milestone.** Add `SafeActions` (or merge with yesterday's `WaitUtils`) to Project 2 and refactor one existing test to use only helper methods, with zero direct `findElement(...).click()` calls and zero sleeps.

---

## Solutions and Hints

**Exercise 1 hint.** Locked-out error locator: `By.cssSelector("[data-test='error']")`. Expected text contains `Sorry, this user has been locked out.` For the Enter-key variation: `password.sendKeys("secret_sauce", Keys.ENTER);`.

**Exercise 2.**

```java
field.sendKeys("hello");
field.clear();
System.out.println("[" + field.getAttribute("value") + "]");   // []
field.sendKeys("hello");
field.sendKeys(Keys.chord(Keys.CONTROL, "a"), Keys.BACK_SPACE);
System.out.println("[" + field.getAttribute("value") + "]");   // []
```

**Exercise 3.** Calling the helper twice with `true` must leave the box ticked, because the second call sees `isSelected() == true` and does nothing. A version that always clicks would untick it.

**Exercise 4.** Locators: `add-to-cart-sauce-labs-backpack`, `add-to-cart-sauce-labs-bike-light`, `add-to-cart-sauce-labs-bolt-t-shirt`; remove button for the backpack: `remove-sauce-labs-backpack`. Wait for the badge text with `textToBe(By.className("shopping_cart_badge"), "3")`.

**Exercise 5 hint.** After the click, the page shows the file name in `#uploaded-files`. Assert `uploaded.equals("pom.xml")` (or your file name).

**Exercise 6 hint.** Click the `#target` input first. Each `sendKeys` shows `You entered: TAB`, `You entered: SPACE`, `You entered: A`. Read `By.id("result")`.

**Exercise 7.** Expect `ElementClickInterceptedException` naming the modal. Proper fix: wait for the modal's close button (`.modal-footer p`) to be clickable, click it, wait for `invisibilityOfElementLocated(By.id("modal"))`, then continue. (The modal appears after a short delay on the first visit, so also wait for it to appear before closing.)

**Exercise 8.** A JavaScript click ignores visibility and overlays. If a modal permanently covers the Pay button, a real user can never pay, but `js.click` still "pays" and the test passes, hiding a severe bug.

**Exercise 9.** Expected value `8`; after `clear()` the value is `""`.

**Exercise 10.** `isEnabled()` is `false` initially. After clicking Enable the page shows a loading indicator and only then enables the input; reading immediately would still return `false`. Use `wait.until(ExpectedConditions.elementToBeClickable(input))` or `wait.until(d -> input.isEnabled())`.

**Exercise 11.** The checkbox toggles on every click. On the second run its state is already ticked, so the click un-ticks it and the assertion fails. Fix: `setCheckbox(box, true)`. (Also the snippet uses `box` without declaring it; always store the element in a variable first.)

**Exercise 12 hint.** Search your test sources for `findElement(` and `Thread.sleep`; each should vanish. If a method does not exist in the helper yet, add it there, not in the test.

---

## Self-Check Questions

1. **Does `sendKeys` replace or append?** It appends; use `clear()` first.
2. **How do you read what was typed into an input?** `getAttribute("value")`, not `getText()`.
3. **Why check `isSelected()` before clicking a checkbox?** A click toggles; the check makes the result independent of the starting state.
4. **How do you upload a file?** Send the absolute path to the `<input type="file">` with `sendKeys`; do not click it.
5. **What does `ElementClickInterceptedException` tell you?** Another element covers the target; the message names it.
6. **When is a JavaScript click acceptable?** Only as a documented last resort after waits, scrolling, and closing overlays have been tried.
7. **Why do helpers take a `By` instead of a `WebElement`?** A `By` can be re-evaluated at the moment of use, avoiding stale references.
8. **Which key constant would you use to move to the next field?** `Keys.TAB`.

---

## Summary

- `click()`, `sendKeys()`, `clear()` and `submit()` are the core interaction methods; Selenium verifies that the element is visible, enabled, and unobstructed, as a real user would experience.
- `sendKeys` **appends**; use `clear()` (or a select-all chord) first. Use `Keys` for Enter, Tab, Escape, arrows, and `Keys.chord` for combinations.
- Checkboxes toggle: always check `isSelected()` before clicking. Styled checkboxes may require clicking the label.
- Upload files by sending an **absolute path** to `<input type="file">`.
- Prefer clicking real buttons over `submit()`; use the **JavaScript executor** only for scrolling or as a documented last resort.
- Combine **wait -> act -> verify**, and wrap this in reusable helpers.
- Know the five interaction exceptions and their usual cures.
- Mouse hover, drag-and-drop, and keyboard press-and-hold belong to the Actions API (Wednesday).

---

## Additional Resources

- Selenium documentation, *Interacting with web elements*: https://www.selenium.dev/documentation/webdriver/elements/interactions/
- Selenium documentation, *Keyboard actions and the Keys class*: https://www.selenium.dev/documentation/webdriver/actions_api/keyboard/
- Selenium documentation, *File upload*: https://www.selenium.dev/documentation/webdriver/elements/file_upload/
