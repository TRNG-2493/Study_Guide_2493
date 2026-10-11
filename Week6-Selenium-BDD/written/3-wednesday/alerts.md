# Alerts

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish the three **JavaScript dialogs** (alert, confirm, prompt) from ordinary HTML pop-ups, modals, and browser-level dialogs.
- Switch to a JavaScript dialog with `driver.switchTo().alert()` and use `getText()`, `accept()`, `dismiss()`, and `sendKeys()`.
- Wait for an alert to appear with `ExpectedConditions.alertIsPresent()`.
- Explain and handle `NoAlertPresentException` and `UnhandledAlertException`, reading their messages to diagnose problems.
- Automate **HTML modal dialogs** with ordinary locators (they are *not* alerts).
- Explain how authentication pop-ups differ and how to handle basic-auth dialogs with the URL format or Selenium 4 features.
- Write a small reusable alert helper and use it from page objects.
- Test both branches of a confirm dialog and verify the outcome on the page.

---

## Why This Matters

Web applications use dialogs to warn and confirm: "Are you sure you want to delete this record?", "You have unsaved changes", "Please enter your name". A test that clicks "Delete" and then tries to do anything else while a JavaScript dialog is open will fail, because **the browser blocks all interaction with the page until the dialog is dismissed**.

**Analogy.** Imagine you are filling in a form at a bank counter and the clerk suddenly holds up a hand and says "Wait, do you really want to close this account?" Nothing else can happen until you answer. A JavaScript dialog is that raised hand. If your test keeps "writing on the form" (calling `findElement`, `click`, and so on) without answering, the browser refuses, and Selenium reports an error.

The failure message `UnhandledAlertException` confuses many beginners because the page looks fine in a screenshot, except the screenshot itself may fail too. Understanding alerts removes this mystery.

Real-world scenarios where you meet dialogs:

1. **Destructive actions.** "Delete account", "Cancel order", "Remove all items". Many sites show a `confirm()` first. A good test checks both that **OK** deletes and that **Cancel** keeps the data.
2. **Validation messages.** Older forms call `alert("Please enter your email")` when a field is empty. The test must read this text and assert it.
3. **Unsaved changes.** An editor warns before you navigate away.
4. **Legacy systems.** Internal company tools often use `alert`, `confirm`, and `prompt` heavily, and those are exactly the systems QA teams are asked to automate.

In **Project 2**, destructive-action tests (delete an account, cancel an order) very commonly involve confirm dialogs. Later today you will place alert handling inside **page-object methods**, so that a test reads `inventoryPage.clearAll(true)` rather than showing dialog mechanics.

---

## The Concept

### 1. Three Kinds of JavaScript Dialogs

**Definition.** A **JavaScript dialog** is a small window created by one of three built-in JavaScript functions and drawn by the **browser**, not by the page's HTML.

| Type | JavaScript | What the user sees | User choices |
|---|---|---|---|
| **Alert** | `alert("Saved!")` | A message and an OK button | OK |
| **Confirm** | `confirm("Delete this item?")` | A message with OK and Cancel | OK (returns true) / Cancel (returns false) |
| **Prompt** | `prompt("Your name?", "Guest")` | A message, a text box, OK and Cancel | Type text, then OK (returns the text) / Cancel (returns null) |

**Why the distinction matters to a tester.**

- An **alert** only informs. Your test reads the text and accepts.
- A **confirm** asks a yes/no question. The page's JavaScript takes different paths depending on the answer, so you must test both.
- A **prompt** asks for text. The page then uses what was typed.

**Key property:** because the browser draws them, **you cannot inspect them with DevTools or locate them with `By`**. They are not part of the DOM (the tree of HTML elements that you search with locators since Monday). Selenium handles them through a dedicated `Alert` interface.

**What the page's code looks like (so you understand what you are testing).**

```html
<button onclick="alert('Saved!')">Save</button>
<button onclick="if (confirm('Delete?')) { document.getElementById('row').remove(); }">Delete</button>
```

In the second button, the row is removed only if the user pressed OK. Selenium's `accept()` and `dismiss()` choose that answer for you.

### 2. Not Everything That Looks Like a Pop-Up Is an Alert

This distinction is critical, and it is the first thing to check when a pop-up test misbehaves:

| Looks like | Really is | How to automate |
|---|---|---|
| A grey box from the browser with OK/Cancel, with the site's address in its title | **JavaScript alert/confirm/prompt** | `driver.switchTo().alert()` |
| A white box in the page with a dark overlay behind it (Bootstrap modal, cookie banner, "Subscribe to our newsletter") | **HTML modal** (ordinary elements) | Normal locators and waits; **inspectable with DevTools** |
| A separate small browser window | **Pop-up window** | Window handling (next lesson) |
| A "Sign in" box asking for username and password at the top of the browser | **HTTP basic-auth dialog** | Special handling (Section 9) |
| File-open dialog from an upload button | **Native OS dialog** | `sendKeys` path on `<input type="file">` (Tuesday) |

**Quick test:** if you can right-click the pop-up and choose "Inspect", it is HTML, not an alert.

**Decision flow when you meet a pop-up.**

1. Can you inspect it with DevTools? Yes: it is HTML. Use `By` locators and waits.
2. No, and it blocks the page with OK/Cancel? Use `switchTo().alert()`.
3. No, and it is a separate window with its own tab or title bar? Use window handles (next lesson).
4. No, and it asks for a username and password before the page loads? Basic auth.
5. No, and it is the operating system's file chooser? Send the path to the file input.

### 3. The `Alert` Interface

```java
import org.openqa.selenium.Alert;

Alert alert = driver.switchTo().alert();
```

**Line-by-line.**

- `import org.openqa.selenium.Alert;` imports the interface. (An *interface* is a Java contract listing methods; Selenium supplies the real object for you.)
- `driver.switchTo()` returns a `TargetLocator`, an object that moves Selenium's attention. You will meet the same `switchTo()` for frames and windows in the next lesson. `.alert()` moves attention to the open dialog and returns an `Alert` object.

If there is no dialog open at that moment, it throws `NoAlertPresentException`.

| Method | Does | Typical use |
|---|---|---|
| `alert.getText()` | Returns the message shown | Assert the warning text |
| `alert.accept()` | Clicks **OK** (also works as "Yes") | Confirm the action |
| `alert.dismiss()` | Clicks **Cancel** (for a plain alert with only OK, behaves like OK) | Test the "No" path |
| `alert.sendKeys("text")` | Types into a **prompt** box | Answer a prompt |

After `accept()` or `dismiss()` the dialog closes and focus returns to the page automatically; you can continue with normal `driver.findElement(...)`.

**Analogy.** `switchTo().alert()` is like turning your head to look at the person who interrupted you. `accept()` / `dismiss()` is your answer; afterwards you turn back to the form (the page) automatically.

### 4. Handling Each Type

#### 4.1 Simple alert

```java
driver.findElement(By.cssSelector("button[onclick='jsAlert()']")).click();

Alert alert = wait.until(ExpectedConditions.alertIsPresent());
System.out.println("Alert says: " + alert.getText());
alert.accept();
```

**Line-by-line.**

1. The CSS selector `button[onclick='jsAlert()']` means "a `button` element whose `onclick` attribute equals `jsAlert()`". This is the attribute selector you practiced in the locators lesson on Monday.
2. `click()` runs the page's JavaScript, which opens the alert.
3. `wait.until(ExpectedConditions.alertIsPresent())` pauses until the dialog exists and **returns** the `Alert` object, so no separate `switchTo().alert()` call is needed.
4. `getText()` reads the message; `accept()` presses OK.

#### 4.2 Confirm

```java
driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();

Alert confirm = wait.until(ExpectedConditions.alertIsPresent());
confirm.dismiss();     // user pressed Cancel; the page usually displays "You clicked: Cancel"
```

Test both branches. A good test suite verifies that **OK** performs the action and **Cancel** leaves everything unchanged. For example, in a delete scenario:

| Branch | Selenium call | What to assert afterwards |
|---|---|---|
| OK | `accept()` | The item is gone from the list; a success message appears |
| Cancel | `dismiss()` | The item is still in the list; no success message |

#### 4.3 Prompt

```java
driver.findElement(By.cssSelector("button[onclick='jsPrompt()']")).click();

Alert prompt = wait.until(ExpectedConditions.alertIsPresent());
prompt.sendKeys("Revature");
prompt.accept();       // the page typically shows "You entered: Revature"
```

- `sendKeys("Revature")` types into the prompt's text box.
- `accept()` submits it. If you instead call `dismiss()`, the page's JavaScript receives `null`, which many pages display as "You entered: null". That is a legitimate branch to test.
- A plain alert or confirm has no text box, so `sendKeys` there throws an exception.

### 5. Waiting for an Alert

Dialogs may be triggered after a delay (an AJAX call finishing, a timer). Do not call `switchTo().alert()` immediately; use the explicit wait from Tuesday:

```java
Alert alert = new WebDriverWait(driver, Duration.ofSeconds(5))
        .until(ExpectedConditions.alertIsPresent());
```

`alertIsPresent()` returns the `Alert` object once the dialog exists, and throws a `TimeoutException` if it never appears within the time limit. That second behaviour is useful for a **negative test** ("no alert should appear"). A quick, non-waiting check is:

```java
public boolean isAlertPresent(WebDriver driver) {
    try {
        driver.switchTo().alert();
        return true;
    } catch (NoAlertPresentException e) {
        return false;
    }
}
```

- The `try` block attempts to switch. If an alert exists, the method returns `true`.
- If none exists, Selenium throws `NoAlertPresentException`, the `catch` block runs, and the method returns `false`. Here an exception is used as a "no" answer, a common Selenium pattern.

**When to use which.**

| Need | Use |
|---|---|
| Alert is expected soon, you need to handle it | `wait.until(alertIsPresent())` |
| Instant yes/no snapshot | `isAlertPresent()` with try/catch |
| Prove that no alert appears | Wait with a short timeout and treat `TimeoutException` as success |

### 6. What Happens If You Ignore an Open Alert?

When a dialog is open and you call another command (`findElement`, `getTitle`, `click`), Selenium's default behaviour (the **unhandled prompt behaviour**, defined by the W3C standard) is to **dismiss the alert and throw `UnhandledAlertException`**, including the dialog's text in the message. So:

```java
button.click();                       // opens an alert
driver.findElement(By.id("result"));  // UnhandledAlertException: unexpected alert open: {Alert text : ...}
```

**Troubleshooting walk-through: reading the exception.**

```text
org.openqa.selenium.UnhandledAlertException: unexpected alert open: {Alert text : I am a JS Alert}
  (Session info: chrome=...)
Build info: version: '4.x.x' ...
```

- `UnhandledAlertException` tells you a dialog was open when a command ran.
- `{Alert text : I am a JS Alert}` is a free gift: it shows you the dialog's text, so you know which dialog it was and can now write the correct handling code.
- The browser has already dismissed it by the time you read this. If you retry the exact same line, it will now succeed, which makes the failure look "random". That is why many testers are confused: the alert is gone but the first failure remains.

**Fix.** Handle the dialog first, and make sure you waited for it, as in section 5.

You can change the default through capabilities:

```java
ChromeOptions options = new ChromeOptions();
options.setUnhandledPromptBehaviour(UnexpectedAlertBehaviour.ACCEPT);   // auto-accept
WebDriver driver = new ChromeDriver(options);
```

Values include `ACCEPT`, `DISMISS`, `ACCEPT_AND_NOTIFY`, `DISMISS_AND_NOTIFY`, and `IGNORE`. Auto-handling is convenient for suites that do not care about dialogs (for example a long end-to-end flow where a harmless "welcome" alert appears), but it hides them from your assertions. Normal tests should handle alerts **explicitly** and assert on their text.

**Troubleshooting walk-through: `NoAlertPresentException`.**

```text
org.openqa.selenium.NoAlertPresentException: no such alert
```

Possible causes, in the order to check them:

1. **Timing.** You switched before the dialog appeared. Use `alertIsPresent()`.
2. **It is not an alert.** It is an HTML modal. Inspect it; if DevTools can select it, use locators.
3. **Wrong click.** The click did not trigger the JavaScript (the element was covered, or the wrong button).
4. **Already handled.** Auto-accept is on, or an earlier line already closed it.

### 7. HTML Modals (Not Alerts)

A Bootstrap-style modal is regular HTML:

```java
// Open the modal
driver.findElement(By.id("openModal")).click();

// Wait for it to be visible, then work with its elements as normal
WebElement modal = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("myModal")));
String title = modal.findElement(By.cssSelector(".modal-title")).getText();
modal.findElement(By.cssSelector(".btn-primary")).click();

// Wait for it to close before continuing
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id("myModal")));
```

**Line-by-line.**

- The first line opens the modal with an ordinary click.
- `visibilityOfElementLocated` waits until the modal is displayed and returns it as a `WebElement`.
- `modal.findElement(...)` searches **inside** the modal only (scoped search), so a `.btn-primary` on the page behind it is not confused with the one in the modal.
- The last line waits for the closing animation to finish. Without it, the next click may hit the fading overlay.

Pitfalls specific to modals: clicking elements **behind** an open modal causes `ElementClickInterceptedException` (the exception text names the element that "would receive the click", often the overlay `div`); animations can leave the modal "visible" while still sliding in, so wait for the specific button to be clickable with `elementToBeClickable`.

**Example on a practice site.** `https://the-internet.herokuapp.com/entry_ad` shows an HTML modal after a short delay. Close it with:

```java
wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".modal"))); 
driver.findElement(By.cssSelector(".modal-footer p")).click();
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.cssSelector(".modal")));
```

No `switchTo().alert()` anywhere: this is just HTML.

**Cookie banners** are modals in disguise. A common practice is to put "dismiss cookie banner if present" in the page-object base class so every test starts clean.

### 8. Other Dialog-Like Events

- **`onbeforeunload`** ("Leave site? Changes you made may not be saved"). It appears when navigating away or closing the page. `driver.quit()` normally handles it; `driver.get()` away from such a page may throw `UnhandledAlertException`. Accept the dialog and continue. Note that modern Chrome shows this dialog only if the user has interacted with the page, which is why it sometimes does not appear in automation at all.
- **Browser permission pop-ups** (location, notifications, camera) are not alerts. They are controlled with browser options, for example the Chrome preference or argument for disabling notifications. They appear in the browser's own UI, not the page.
- **Headless Chrome** handles JavaScript dialogs the same way as headed Chrome.

### 9. Authentication Pop-Ups (HTTP Basic Auth)

**What it is.** When a server asks for credentials using the browser's built-in login box (the server answers with HTTP status 401 and a `WWW-Authenticate` header), the dialog is **not** a JavaScript alert. `switchTo().alert()` does not work for it. Options:

**Option A: credentials in the URL** (works in many browsers for basic auth on practice and test environments):

```java
driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth");
```

Format: `https://username:password@host/path`. Some modern browsers have restricted this for security; if it fails, use Option B.

**Option B: Selenium 4 `HasAuthentication`** (Chromium-based drivers such as ChromeDriver and EdgeDriver):

```java
import org.openqa.selenium.HasAuthentication;
import org.openqa.selenium.UsernameAndPassword;

((HasAuthentication) driver).register(UsernameAndPassword.of("admin", "admin"));
driver.get("https://the-internet.herokuapp.com/basic_auth");
```

**Line-by-line.**

- The cast `(HasAuthentication) driver` treats the driver as an object that supports authentication. A `ChromeDriver` implements it; a plain `WebDriver` variable type does not expose it, hence the cast. (A cast tells Java "I know the real type of this object".)
- `register(...)` stores the credentials; the browser supplies them automatically whenever a server challenges.
- `UsernameAndPassword.of(user, pass)` builds the credentials object.

Support varies by driver class and version; when running against a remote grid, you may need to wrap the driver with `new Augmenter().augment(driver)` first. Check the Selenium release notes for your version.

**Verification.** After either option, assert that the page text contains "Congratulations".

Never put real passwords in test code or the repository; later in the course you will read credentials from configuration or environment variables.

### 10. A Reusable Alert Helper

```java
package com.revature.qea.utils;

import org.openqa.selenium.Alert;
import org.openqa.selenium.NoAlertPresentException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class AlertUtils {

    private final WebDriver driver;
    private final WebDriverWait wait;

    public AlertUtils(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(5));
    }

    public boolean isPresent() {
        try {
            driver.switchTo().alert();
            return true;
        } catch (NoAlertPresentException e) {
            return false;
        }
    }

    /** Waits for an alert and returns its text without closing it. */
    public String textOfAlert() {
        return wait.until(ExpectedConditions.alertIsPresent()).getText();
    }

    /** Waits for an alert, returns its text, and clicks OK. */
    public String acceptAndGetText() {
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());
        String text = alert.getText();
        alert.accept();
        return text;
    }

    /** Waits for an alert, returns its text, and clicks Cancel. */
    public String dismissAndGetText() {
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());
        String text = alert.getText();
        alert.dismiss();
        return text;
    }

    /** Types into a prompt and accepts it. */
    public void answerPrompt(String answer) {
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());
        alert.sendKeys(answer);
        alert.accept();
    }

    /** True if no alert appears within the wait time (useful for negative tests). */
    public boolean noAlertAppears() {
        try {
            wait.until(ExpectedConditions.alertIsPresent());
            return false;
        } catch (TimeoutException e) {
            return true;
        }
    }
}
```

**Explanation.**

- `private final WebDriver driver;` stores the driver the class works with. `final` means it is assigned once (in the constructor) and never replaced.
- The constructor receives the driver (this is called **constructor injection**: the class is handed what it needs). It also builds a 5-second `WebDriverWait`. This is the same shape as Tuesday's `WaitUtils` and the `DriverFactory` pattern.
- Each public method has one job and a name that says what it does. A test calls `alerts.acceptAndGetText()` and gets the message to assert on.
- `noAlertAppears()` inverts the logic: a `TimeoutException` means "no alert came", which is the **good** result for that question.
- Note: **read the text before closing** the alert; after `accept()` the `Alert` object is no longer usable.

**Using it in a test.**

```java
AlertUtils alerts = new AlertUtils(driver);
driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();
String message = alerts.dismissAndGetText();
Assert.assertEquals(message, "I am a JS Confirm");
Assert.assertEquals(driver.findElement(By.id("result")).getText(), "You clicked: Cancel");
```

**Connecting to Page Objects.** A page object for the-internet's alert page would hold `By` locators for the three buttons and a few methods such as `triggerConfirmAndDismiss()`; it can use `AlertUtils` internally. The test then never mentions `Alert` at all. You will build exactly this style of class later today.

---

## Code Example: All Three Dialogs

The practice page `https://the-internet.herokuapp.com/javascript_alerts` has three buttons, one for each dialog type, and displays a result message.

```java
package com.revature.qea.alerts;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class AlertsDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        try {
            driver.get("https://the-internet.herokuapp.com/javascript_alerts");
            By result = By.id("result");

            // ---- 1. Simple alert ----
            driver.findElement(By.cssSelector("button[onclick='jsAlert()']")).click();
            Alert alert = wait.until(ExpectedConditions.alertIsPresent());
            System.out.println("Alert text  : " + alert.getText());
            alert.accept();
            System.out.println("Result      : " + driver.findElement(result).getText());

            // ---- 2. Confirm: accept, then dismiss ----
            driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();
            wait.until(ExpectedConditions.alertIsPresent()).accept();
            System.out.println("Confirm OK  : " + driver.findElement(result).getText());

            driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();
            wait.until(ExpectedConditions.alertIsPresent()).dismiss();
            System.out.println("Confirm Cancel: " + driver.findElement(result).getText());

            // ---- 3. Prompt ----
            driver.findElement(By.cssSelector("button[onclick='jsPrompt()']")).click();
            Alert prompt = wait.until(ExpectedConditions.alertIsPresent());
            prompt.sendKeys("Selenium rocks");
            prompt.accept();
            System.out.println("Prompt      : " + driver.findElement(result).getText());

            // ---- 4. What if we forget to handle it? ----
            driver.findElement(By.cssSelector("button[onclick='jsAlert()']")).click();
            try {
                driver.findElement(result).getText();    // alert still open
            } catch (org.openqa.selenium.UnhandledAlertException e) {
                System.out.println("Caught UnhandledAlertException as expected");
            }
        } finally {
            driver.quit();
        }
    }
}
```

**Explanation.**

- `By result = By.id("result");` stores a locator (not an element) in a variable. Because we use it many times, a locator object is reused, and the element is looked up fresh each time, avoiding stale references.
- Section 1 shows the full three-step pattern: click, wait for alert, read and accept.
- Section 2 uses the chained form `wait.until(...).accept()` when we do not need the text. Compact, but you lose the chance to assert on the message.
- Section 3 types into the prompt before accepting.
- Section 4 deliberately breaks the rule. Because the alert is open, `findElement` throws `UnhandledAlertException`; the `catch` demonstrates it. In real tests you would never write this, but seeing the exception once teaches you to recognise it.

**Expected console output.**

```text
Alert text  : I am a JS Alert
Result      : You successfully clicked an alert
Confirm OK  : You clicked: Ok
Confirm Cancel: You clicked: Cancel
Prompt      : You entered: Selenium rocks
Caught UnhandledAlertException as expected
```

**What to observe:** the result text on the page changes after each dialog. The test should **assert** on these texts rather than only printing them.

---

## Guided Lab: A Tested Confirm Flow

**Goal.** Write a JUnit/TestNG test class `JsAlertsTest` that verifies all branches and uses `AlertUtils`.

1. Add `AlertUtils` (section 10) to `src/main/java/com/revature/qea/utils` (or your test utilities package).
2. Create `JsAlertsTest`. In the setup method, start Chrome and open `https://the-internet.herokuapp.com/javascript_alerts`; create an `AlertUtils` object.
3. Write `alertShowsMessageAndResult()`: click the first button, call `acceptAndGetText()`, assert the text equals `I am a JS Alert`, assert `#result` equals `You successfully clicked an alert`.
4. Write `confirmOkBranch()` and `confirmCancelBranch()`: same pattern with the second button; expected results `You clicked: Ok` and `You clicked: Cancel`.
5. Write `promptWithText()`: click the third button, call `answerPrompt("QEA")`, assert `#result` equals `You entered: QEA`.
6. Write `promptCancelled()`: click the third button, wait for the alert, call `dismiss()`, assert `#result` equals `You entered: null`.
7. Write `noAlertOnOtherPage()`: navigate to `https://the-internet.herokuapp.com/`, assert `noAlertAppears()` is `true`.
8. Run the class. Expected: 6 tests, all green.
9. Break something on purpose: remove the wait in one test and call `driver.switchTo().alert()` directly. Run several times and note whether it fails intermittently. Restore the wait.

**Expected report.**

```text
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
```

**Reflection.** Which assertions protect against the page's JavaScript receiving the wrong answer? (The result-text assertions, because they prove the page reacted to the choice, not only that the dialog existed.)

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Trying to locate an alert with `By` | `NoSuchElementException` | Use `switchTo().alert()` |
| Calling `switchTo().alert()` right after the click without waiting | Intermittent `NoAlertPresentException` | `alertIsPresent()` wait |
| Doing other commands while an alert is open | `UnhandledAlertException` | Accept/dismiss first |
| Reading `getText()` after `accept()` | Error: no alert | Read the text first |
| Treating an HTML modal as an alert | `NoAlertPresentException` | Use normal locators |
| Using `sendKeys` on a plain alert/confirm | Exception (the dialog has no text box) | Only prompts accept text |
| Auto-accepting all alerts globally and never asserting | Hidden unexpected dialogs | Handle explicitly in tests that care |
| Hard-coding real credentials in an auth URL | Security risk | Use test accounts and configuration |
| Testing only the OK branch of a confirm | Cancel regression goes unnoticed | Test both branches |
| Asserting only that an alert appeared, not what happened after | Weak test | Assert the page result as well |

---

## Practice Exercises

1. **Three dialogs.** Automate all three buttons on `the-internet.herokuapp.com/javascript_alerts`. Assert on the alert text **and** the result message for each outcome (OK, Cancel, text entered).
2. **Negative check.** Write a test that clicks a normal button that does *not* open an alert and asserts that `noAlertAppears()` returns `true`.
3. **Handle the exception.** Deliberately trigger `UnhandledAlertException`, catch it, and print its message. What information does it give?
4. **Modal vs. alert.** On `https://the-internet.herokuapp.com/entry_ad` (an HTML modal), close the modal. Explain in two sentences why `switchTo().alert()` is the wrong tool.
5. **Basic auth.** Open `https://the-internet.herokuapp.com/basic_auth` with credentials in the URL (`admin`/`admin`) and assert that the page says "Congratulations".
6. **Basic auth, second way.** Repeat exercise 5 using `HasAuthentication`. Which approach would you prefer on a shared team repository, and why?
7. **Unsaved-changes prompt.** Describe how you would test a page that warns before leaving with unsaved changes. Which method handles the dialog?
8. **Auto-accept.** Configure `UnexpectedAlertBehaviour.ACCEPT` in `ChromeOptions` and show that the `UnhandledAlertException` no longer occurs. Discuss one downside of this setting.
9. **Prompt cancel.** Click the prompt button, dismiss the prompt, and record what the page shows. Explain what value JavaScript received.
10. **Wrapper method.** Write `public String clickAndAcceptAlert(By button)` that clicks a button, waits for the alert, accepts it, and returns the text. Where would it live?
11. **Delete scenario.** Write the outline (comments only) of a test for a "delete item" feature protected by a confirm dialog, covering both branches and listing every assertion.
12. **Add `AlertUtils`** to your Project 2 skeleton and use it for a "delete" scenario in your test site, if it has one.

---

## Solutions and Hints

**1. Three dialogs.** Follow the lab steps; solution outline:

```java
@Test
public void confirmCancel() {
    driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();
    Alert a = wait.until(ExpectedConditions.alertIsPresent());
    Assert.assertEquals(a.getText(), "I am a JS Confirm");
    a.dismiss();
    Assert.assertEquals(driver.findElement(By.id("result")).getText(), "You clicked: Cancel");
}
```

**2. Negative check.** Hint: use a short wait (2 seconds) so the test is fast. `Assert.assertTrue(alerts.noAlertAppears());` after clicking a link such as "Home".

**3. Handle the exception.** The message begins `unexpected alert open: {Alert text : I am a JS Alert}`. It tells you (a) a dialog was open and (b) its text. It does not tell you the dialog is still open: Selenium has already dismissed it.

**4. Modal vs. alert.** The entry ad is made of HTML elements (`div` with class `modal`), so DevTools can inspect it and `By` locators find it. `switchTo().alert()` only targets browser-drawn JavaScript dialogs, so it would throw `NoAlertPresentException`.

**5. Basic auth.**

```java
driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth");
Assert.assertTrue(driver.findElement(By.tagName("p")).getText().contains("Congratulations"));
```

If your browser blocks credentials in URLs, use exercise 6.

**6. HasAuthentication.** Use the code from section 9 before `driver.get`. Preferred on a team repository: `HasAuthentication`, because the credentials are passed as data (easy to read from configuration), while URL credentials leak into logs and browser history.

**7. Unsaved-changes prompt.** Make a change in the form, then navigate away with `driver.get(...)` or click a link; wait for the dialog with `alertIsPresent()`; assert its text; `accept()` to leave or `dismiss()` to stay; assert the URL accordingly. Note that browsers may only show this dialog after user interaction with the page.

**8. Auto-accept.**

```java
ChromeOptions options = new ChromeOptions();
options.setUnhandledPromptBehaviour(UnexpectedAlertBehaviour.ACCEPT);
WebDriver driver = new ChromeDriver(options);
```

Downside: alerts disappear silently, so a test cannot assert on their text, and unexpected dialogs (genuine bugs) are never noticed.

**9. Prompt cancel.** The page shows `You entered: null`. JavaScript's `prompt()` returns `null` when the user cancels.

**10. Wrapper method.**

```java
public String clickAndAcceptAlert(By button) {
    driver.findElement(button).click();
    Alert alert = wait.until(ExpectedConditions.alertIsPresent());
    String text = alert.getText();
    alert.accept();
    return text;
}
```

It would live in a base page class or in `AlertUtils`, so every page object can reuse it.

**11. Delete scenario outline.**

```java
// Test A: confirm OK
// 1. Log in, open the list, count items (before)
// 2. Click Delete on item X
// 3. Wait for alert; assert text mentions the item/asks "Are you sure"
// 4. accept()
// 5. Assert item X is no longer present; count == before - 1; success message shown
// Test B: confirm Cancel
// same steps, dismiss() in step 4
// Assert item X still present; count == before; no success message
```

**12. Project 2.** Hint: keep `AlertUtils` generic and let the relevant page object call it, as shown in section 10.

---

## Self-Check Questions

1. **Why can't you find a JavaScript alert with `driver.findElement`?** It is drawn by the browser and is not part of the page's DOM.
2. **What does `dismiss()` do on a confirm, and what does the page's JavaScript receive?** It presses Cancel; `confirm()` returns `false`.
3. **What is the default Selenium behaviour when you send a command while an alert is open?** It dismisses the alert and throws `UnhandledAlertException` containing the alert text.
4. **How do you tell an HTML modal from an alert?** If you can inspect it with DevTools, it is HTML; use ordinary locators.
5. **Why read `getText()` before `accept()`?** After the dialog closes, the `Alert` object can no longer be used.
6. **Which method waits for an alert, and what does it return?** `ExpectedConditions.alertIsPresent()`, which returns the `Alert`.
7. **Does `switchTo().alert()` handle the browser's username/password login box?** No; that is basic auth, handled with URL credentials or `HasAuthentication`.
8. **Why should a delete test cover both OK and Cancel?** They are two different code paths; each could break independently.

---

## Summary

- JavaScript dialogs (alert, confirm, prompt) are drawn by the **browser**, are **not in the DOM**, and block the page until handled.
- Use `driver.switchTo().alert()`, then `getText()`, `accept()`, `dismiss()`, or `sendKeys()` (prompt only).
- Use `ExpectedConditions.alertIsPresent()` to wait for dialogs triggered with a delay.
- Ignoring an open alert causes `UnhandledAlertException`; no alert when you need one causes `NoAlertPresentException`.
- **HTML modals** and cookie banners are ordinary elements; use locators and waits. File dialogs use `sendKeys(path)`; basic-auth dialogs need URL credentials or `HasAuthentication`.
- Read the alert text **before** closing it, and test **both** OK and Cancel branches, asserting the page result afterwards.
- Put dialog mechanics inside helpers and page-object methods so tests stay readable.

---

## Additional Resources

- Selenium documentation, *JavaScript alerts, prompts and confirmations*: https://www.selenium.dev/documentation/webdriver/interactions/alerts/
- Selenium Java API, `Alert` interface: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/Alert.html
- MDN Web Docs, *Window.alert(), confirm(), and prompt()*: https://developer.mozilla.org/en-US/docs/Web/API/Window/alert
