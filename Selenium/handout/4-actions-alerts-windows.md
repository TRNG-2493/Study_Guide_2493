# Selenium In-Class Handout, Group 4: Actions, Alerts and Windows

**Topics:** 4.1 Actions API · 4.2 Alerts · 4.3 Window handling and frames

**How to use this handout:** the same layout as Handouts 1–3. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Handouts 1–3:** every example is a JUnit test class that `extends BaseTest`. You can already find elements, click, type, wait with `WebDriverWait`, and choose from dropdowns. **This handout covers what those commands can't do on their own:** mouse and keyboard gestures, JavaScript pop-up dialogs, and working with several windows, tabs and frames.

**Practice site:** the-internet `https://the-internet.herokuapp.com`.

---

## 4.1 Actions API

### Definition

The **Actions API** lets a test use the mouse and keyboard in ways that `click()` and `sendKeys()` cannot: **hovering** over an element, **right-clicking**, **double-clicking**, **dragging and dropping**, pressing **key combinations** such as Ctrl+A, and **scrolling**. In Java you use the `Actions` class: you describe the gesture as a **chain** of steps, then call **`perform()`** to send them to the browser. Nothing happens until `perform()` is called. For ordinary clicks and typing, keep using `click()` and `sendKeys()`; use Actions only when you need a gesture.

### Key terms

| Method | Gesture |
|---|---|
| `moveToElement(element)` | **Hover**: move the mouse over the element |
| `click(element)` | Click (often used to focus an element before typing) |
| `doubleClick(element)` | Double-click |
| `contextClick(element)` | **Right-click** (opens a "context menu") |
| `dragAndDrop(source, target)` | Drag one element onto another |
| `keyDown(Keys.CONTROL)` / `keyUp(Keys.CONTROL)` | Hold / release a key (for combinations) |
| `sendKeys(Keys.TAB)` | Press keys, sent to whichever element has focus |
| `scrollToElement(element)` | Scroll until the element is visible |
| `perform()` | **Send the whole chain to the browser** |

**Other terms:**

- **Chain:** several steps joined with dots, e.g. `new Actions(driver).moveToElement(a).click().perform()`.
- **Hover:** resting the mouse over an element without clicking. Menus and captions that appear only on hover need `moveToElement`.
- **Focus:** the element that receives keyboard input, e.g. the text box you last clicked.

### Key ideas

- Build the chain, then **always end with `perform()`**.
- After a gesture, **check the result** the user would see (a caption appears, columns swap), as with any interaction.
- Every `keyDown` needs a matching `keyUp`, or the key stays "held down" for the rest of the test.

### Worked example: `ActionsTest`

We use three pages on the-internet:

- `/hovers`: three user pictures (`.figure`); each has a caption (`.figcaption`) that appears only on hover, e.g. **name: user1**.
- `/key_presses`: a text box (`id="target"`); the page shows the last key pressed in `id="result"`, e.g. **You entered: TAB**.
- `/drag_and_drop`: two boxes, **A** (`id="column-a"`) and **B** (`id="column-b"`).

**Step 1: Hover.** Find the first picture and its caption; the caption starts hidden.

```java
@Test
void hoverShowsTheCaption() {
    driver.get("https://the-internet.herokuapp.com/hovers");
    WebElement firstPicture = driver.findElements(By.cssSelector(".figure")).get(0);
    WebElement caption = firstPicture.findElement(By.cssSelector(".figcaption"));
    assertFalse(caption.isDisplayed());
}
```

**Step 2: Perform the hover, wait for the caption, check its text.** Add to the same test:

```java
    new Actions(driver).moveToElement(firstPicture).perform();

    new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.visibilityOf(caption));
    assertEquals("name: user1", caption.findElement(By.tagName("h5")).getText());
```

**Step 3: Keyboard.** Click into the box to give it focus, then press Tab, in one chain.

```java
@Test
void pressTabInTheTextBox() {
    driver.get("https://the-internet.herokuapp.com/key_presses");
    WebElement box = driver.findElement(By.id("target"));

    new Actions(driver).click(box).sendKeys(Keys.TAB).perform();

    assertEquals("You entered: TAB", driver.findElement(By.id("result")).getText());
}
```

**Step 4: Drag and drop.** Drag box A onto box B; the boxes swap places, so the first box now shows **B**.

```java
@Test
void dragAOntoB() {
    driver.get("https://the-internet.herokuapp.com/drag_and_drop");
    WebElement boxA = driver.findElement(By.id("column-a"));
    WebElement boxB = driver.findElement(By.id("column-b"));
    assertEquals("A", boxA.getText());

    new Actions(driver).dragAndDrop(boxA, boxB).perform();

    assertEquals("B", driver.findElement(By.id("column-a")).getText());
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/ActionsTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class ActionsTest extends BaseTest {

    @Test
    void hoverShowsTheCaption() {
        driver.get("https://the-internet.herokuapp.com/hovers");
        WebElement firstPicture = driver.findElements(By.cssSelector(".figure")).get(0);
        WebElement caption = firstPicture.findElement(By.cssSelector(".figcaption"));
        assertFalse(caption.isDisplayed());

        new Actions(driver).moveToElement(firstPicture).perform();

        new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.visibilityOf(caption));
        assertEquals("name: user1", caption.findElement(By.tagName("h5")).getText());
    }

    @Test
    void pressTabInTheTextBox() {
        driver.get("https://the-internet.herokuapp.com/key_presses");
        WebElement box = driver.findElement(By.id("target"));

        new Actions(driver).click(box).sendKeys(Keys.TAB).perform();

        assertEquals("You entered: TAB", driver.findElement(By.id("result")).getText());
    }

    @Test
    void dragAOntoB() {
        driver.get("https://the-internet.herokuapp.com/drag_and_drop");
        WebElement boxA = driver.findElement(By.id("column-a"));
        WebElement boxB = driver.findElement(By.id("column-b"));
        assertEquals("A", boxA.getText());

        new Actions(driver).dragAndDrop(boxA, boxB).perform();

        assertEquals("B", driver.findElement(By.id("column-a")).getText());
    }
}
```

### Checkpoint

You see the mouse "rest" on the first picture and its caption appear, then the two boxes swap.

```text
✔ ActionsTest
   ✔ hoverShowsTheCaption()
   ✔ pressTabInTheTextBox()
   ✔ dragAOntoB()
```

### Your turn

1. Hover over the **third** picture and check its caption is `name: user3`.
2. On `/key_presses`, press `Keys.ESCAPE` instead of Tab, and check the result text.
3. Remove `.perform()` from `pressTabInTheTextBox` and run it. What fails, and why? Put it back.
4. After dragging A onto B, drag them back (B onto A) in the same test and check the first box shows `A` again.

### Common errors

| You see | Why | Fix |
|---|---|---|
| Nothing happens | `.perform()` is missing | End every chain with `perform()` |
| Hover caption never appears | Hovered the wrong element (e.g. the caption itself, which is hidden) | Hover the visible parent (the picture) |
| Later typing comes out in capitals | `keyDown(Keys.SHIFT)` without `keyUp(Keys.SHIFT)` | Release every key you hold |
| `MoveTargetOutOfBoundsException` | The gesture moves the mouse outside the window | Use `moveToElement` on a visible element |

---

## 4.2 Alerts

### Definition

An **alert** is a pop-up dialog created by the page's JavaScript and drawn by the **browser**, not by the page itself. There are three kinds: an **alert** (a message with an OK button), a **confirm** (OK and Cancel) and a **prompt** (a text box with OK and Cancel). While a dialog is open the page is frozen, and because the dialog is not part of the page's HTML, `findElement` cannot find it. Instead you **switch to it** with `driver.switchTo().alert()`, which gives you an `Alert` object to read, type into, accept or dismiss.

### Key terms

| Dialog | JavaScript | Buttons |
|---|---|---|
| **Alert** | `alert('...')` | OK |
| **Confirm** | `confirm('...')` | OK, Cancel |
| **Prompt** | `prompt('...')` | Text box, OK, Cancel |

| Method | What it does |
|---|---|
| `driver.switchTo().alert()` | Returns the open dialog as an `Alert` |
| `alert.getText()` | Reads the dialog's message |
| `alert.accept()` | Presses **OK** |
| `alert.dismiss()` | Presses **Cancel** |
| `alert.sendKeys("text")` | Types into a **prompt**'s text box |
| `ExpectedConditions.alertIsPresent()` | Wait condition: waits until a dialog is open and returns it |

**Other terms:**

- **HTML modal:** a pop-up built from ordinary page elements (often a `<div>`). You **can** inspect it in DevTools, so you use `findElement`, not `switchTo().alert()`.

### Key ideas

- The pattern is **click → wait for the dialog → read → answer**.
- Answer **every** dialog before doing anything else on the page; while it is open, other commands fail.
- **Test the page's reaction** too: after accepting or dismissing, check what the page shows.

### Worked example: `AlertsTest`

The page `https://the-internet.herokuapp.com/javascript_alerts` has three buttons: **Click for JS Alert**, **Click for JS Confirm** and **Click for JS Prompt**. After each dialog, the page shows what happened in `id="result"`.

**Step 1: Open the page before each test, and a helper to click a button by its text.**

```java
class AlertsTest extends BaseTest {

    @BeforeEach
    void openPage() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");
    }

    private void clickButton(String text) {
        driver.findElement(By.xpath("//button[text()='" + text + "']")).click();
    }
}
```

**Step 2: A simple alert: wait, read, accept, check the page.**

```java
@Test
void acceptAnAlert() {
    clickButton("Click for JS Alert");

    Alert alert = new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.alertIsPresent());
    assertEquals("I am a JS Alert", alert.getText());
    alert.accept();

    assertEquals("You successfully clicked an alert", driver.findElement(By.id("result")).getText());
}
```

**Step 3: A confirm, answered with Cancel.**

```java
@Test
void dismissAConfirm() {
    clickButton("Click for JS Confirm");

    Alert confirm = driver.switchTo().alert();
    assertEquals("I am a JS Confirm", confirm.getText());
    confirm.dismiss();

    assertEquals("You clicked: Cancel", driver.findElement(By.id("result")).getText());
}
```

**Step 4: A prompt: type an answer, then OK.**

```java
@Test
void answerAPrompt() {
    clickButton("Click for JS Prompt");

    Alert prompt = driver.switchTo().alert();
    prompt.sendKeys("Selenium");
    prompt.accept();

    assertEquals("You entered: Selenium", driver.findElement(By.id("result")).getText());
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/AlertsTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AlertsTest extends BaseTest {

    @BeforeEach
    void openPage() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");
    }

    private void clickButton(String text) {
        driver.findElement(By.xpath("//button[text()='" + text + "']")).click();
    }

    @Test
    void acceptAnAlert() {
        clickButton("Click for JS Alert");

        Alert alert = new WebDriverWait(driver, Duration.ofSeconds(5))
                .until(ExpectedConditions.alertIsPresent());
        assertEquals("I am a JS Alert", alert.getText());
        alert.accept();

        assertEquals("You successfully clicked an alert", driver.findElement(By.id("result")).getText());
    }

    @Test
    void dismissAConfirm() {
        clickButton("Click for JS Confirm");

        Alert confirm = driver.switchTo().alert();
        assertEquals("I am a JS Confirm", confirm.getText());
        confirm.dismiss();

        assertEquals("You clicked: Cancel", driver.findElement(By.id("result")).getText());
    }

    @Test
    void answerAPrompt() {
        clickButton("Click for JS Prompt");

        Alert prompt = driver.switchTo().alert();
        prompt.sendKeys("Selenium");
        prompt.accept();

        assertEquals("You entered: Selenium", driver.findElement(By.id("result")).getText());
    }
}
```

### Checkpoint

Each dialog flashes up and is answered by the test.

```text
✔ AlertsTest
   ✔ acceptAnAlert()
   ✔ dismissAConfirm()
   ✔ answerAPrompt()
```

### Your turn

1. Write `acceptAConfirm`: press **OK** on the confirm and check the page shows `You clicked: Ok`.
2. Open the prompt, type some text, then press **Cancel**. What does the page show? (Expected: `You entered: null`.)
3. **Right-click alert:** on `https://the-internet.herokuapp.com/context_menu`, right-click the box (`id="hot-spot"`) with `new Actions(driver).contextClick(box).perform()`. A dialog appears: check its text is `You selected a context menu`, then accept it.
4. Click "Click for JS Alert" and, **without** handling the dialog, call `driver.getTitle()`. Which exception do you get? Write a test using `assertThrows` for it.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoAlertPresentException` | Switched before the dialog appeared, or no dialog was opened | Wait with `ExpectedConditions.alertIsPresent()` |
| `UnhandledAlertException` | A dialog was still open when the test used the page | Accept or dismiss the dialog first |
| `findElement` can't find the pop-up | It is a JavaScript dialog, not HTML | Use `driver.switchTo().alert()` |
| `switchTo().alert()` can't find the pop-up | It is an HTML modal, not a dialog | Use `findElement` and click its button |

---

## 4.3 Window Handling and Frames

### Definition

A browser can have several **windows** and **tabs** open at once. Selenium gives each one a **window handle**, a unique ID `String`, but it sends commands to only **one window at a time**. When a link opens a new tab, the test must **switch** to it with `driver.switchTo().window(handle)` before it can use it, and switch back afterwards. A **frame** (`<iframe>` or `<frame>`) is a page shown inside another page; its elements are invisible to `findElement` until you switch into the frame with `driver.switchTo().frame(...)`. Switching back out is done with `driver.switchTo().defaultContent()`.

### Key terms

**Windows and tabs:**

| Method | What it does |
|---|---|
| `driver.getWindowHandle()` | Handle of the **current** window |
| `driver.getWindowHandles()` | Handles of **all** open windows (a `Set<String>`) |
| `driver.switchTo().window(handle)` | Send future commands to that window |
| `driver.switchTo().newWindow(WindowType.TAB)` | Open a new, empty tab **and switch to it** |
| `driver.close()` | Close the current window only |
| `driver.quit()` | Close every window and end the session (done by `BaseTest`) |

**Frames:**

| Method | What it does |
|---|---|
| `driver.switchTo().frame("name")` | Move into a frame by its `name` or `id` |
| `driver.switchTo().frame(0)` | Move into a frame by position (0 = first) |
| `driver.switchTo().parentFrame()` | Move up one level |
| `driver.switchTo().defaultContent()` | Move back to the main page |

### Key ideas

- **Save the original handle** before opening a new window, so you can switch back.
- A new tab opens a moment after the click: **wait** with `ExpectedConditions.numberOfWindowsToBe(2)` before reading the handles.
- After `close()`, Selenium does **not** switch for you; switch back to a window that is still open.
- If an element you can see on screen is "not found", check whether it is inside a frame.

### Worked example: `WindowsTest`

- `https://the-internet.herokuapp.com/windows` has a link **Click Here** that opens a new window titled **New Window**.
- `https://the-internet.herokuapp.com/nested_frames` shows four frames. The top frame (`name="frame-top"`) contains a middle frame (`name="frame-middle"`) whose text is **MIDDLE**.

**Step 1: Save the current handle, then click the link.**

```java
@Test
void switchToANewWindowAndBack() {
    driver.get("https://the-internet.herokuapp.com/windows");
    String original = driver.getWindowHandle();

    driver.findElement(By.linkText("Click Here")).click();
}
```

**Step 2: Wait for the second window, find its handle, switch to it.** Add to the same test:

```java
    new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.numberOfWindowsToBe(2));

    for (String handle : driver.getWindowHandles()) {
        if (!handle.equals(original)) {
            driver.switchTo().window(handle);           // the one that isn't the original
        }
    }
    assertEquals("New Window", driver.getTitle());
```

**Step 3: Close the new window and switch back.**

```java
    driver.close();
    driver.switchTo().window(original);
    assertEquals("The Internet", driver.getTitle());
```

**Step 4: Frames.** The text **MIDDLE** can't be found from the main page; switch into the top frame, then the middle frame.

```java
@Test
void readTextInsideNestedFrames() {
    driver.get("https://the-internet.herokuapp.com/nested_frames");
    assertTrue(driver.findElements(By.id("content")).isEmpty());   // not visible from the main page

    driver.switchTo().frame("frame-top");
    driver.switchTo().frame("frame-middle");
    assertEquals("MIDDLE", driver.findElement(By.id("content")).getText());

    driver.switchTo().defaultContent();                             // back to the main page
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/WindowsTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WindowsTest extends BaseTest {

    @Test
    void switchToANewWindowAndBack() {
        driver.get("https://the-internet.herokuapp.com/windows");
        String original = driver.getWindowHandle();

        driver.findElement(By.linkText("Click Here")).click();

        new WebDriverWait(driver, Duration.ofSeconds(5))
                .until(ExpectedConditions.numberOfWindowsToBe(2));

        for (String handle : driver.getWindowHandles()) {
            if (!handle.equals(original)) {
                driver.switchTo().window(handle);
            }
        }
        assertEquals("New Window", driver.getTitle());

        driver.close();
        driver.switchTo().window(original);
        assertEquals("The Internet", driver.getTitle());
    }

    @Test
    void readTextInsideNestedFrames() {
        driver.get("https://the-internet.herokuapp.com/nested_frames");
        assertTrue(driver.findElements(By.id("content")).isEmpty());

        driver.switchTo().frame("frame-top");
        driver.switchTo().frame("frame-middle");
        assertEquals("MIDDLE", driver.findElement(By.id("content")).getText());

        driver.switchTo().defaultContent();
    }
}
```

### Checkpoint

A second window opens and closes in the first test.

```text
✔ WindowsTest
   ✔ switchToANewWindowAndBack()
   ✔ readTextInsideNestedFrames()
```

### Your turn

1. In the new window, also check the heading: `driver.findElement(By.tagName("h3")).getText()` should be `New Window`.
2. Open a tab yourself: after `driver.get(".../windows")`, call `driver.switchTo().newWindow(WindowType.TAB)` and open `https://the-internet.herokuapp.com/login` in it. Check that `getWindowHandles().size()` is 2 and the new tab's URL is the login page.
3. On `/nested_frames`, read the **bottom** frame: switch to `"frame-bottom"` and check `driver.findElement(By.tagName("body")).getText()` is `BOTTOM`.
4. In `switchToANewWindowAndBack`, remove the line `driver.switchTo().window(original);` and run it. Which exception do you get, and why?

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoSuchWindowException` | Still pointing at a window you closed | `switchTo().window(original)` after `close()` |
| New window's title is wrong / old page's title | Forgot to switch, or switched before it opened | Wait for 2 windows, then switch |
| `NoSuchElementException` for an element you can see | It is inside a frame | `switchTo().frame(...)` first |
| `NoSuchFrameException` | Wrong frame name, or you're not in the parent frame | Check the name in DevTools; go back with `defaultContent()` |

---

**End of Handout 4.** You can perform mouse and keyboard gestures, handle all three kinds of JavaScript dialog, and work with new windows, tabs and frames. **Next:** Handout 5, Framework Design: screenshots and the Page Object Model.
