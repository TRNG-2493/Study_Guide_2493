# Selenium In-Class Handout, Group 3: Interacting and Waiting

**Topics:** 3.1 Element interactions · 3.2 Waiting strategies · 3.3 Select elements

**How to use this handout:** the same layout as Handouts 1 and 2. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Handouts 1 and 2:** every example is a JUnit test class that `extends BaseTest`, and you already know how to open pages and find and read elements. **In this handout you start acting on the page**: typing, clicking, waiting for the page to catch up, and choosing from dropdowns.

> **Order note:** the full notes teach *Waiting strategies* before *Element interactions*. Here interactions come first, because every waiting example starts with a click.

**Practice sites:** the-internet `https://the-internet.herokuapp.com` (login: `tomsmith` / `SuperSecretPassword!`) and Swag Labs `https://www.saucedemo.com` (login: `standard_user` / `secret_sauce`).

---

## 3.1 Element Interactions

### Definition

An **interaction** is an action a test performs on a web element, the way a user would: **clicking** a button, link or checkbox, **typing** into a text box, or **clearing** a text box. In Selenium you first find the element (Handout 2), then call an interaction method on the `WebElement`: `click()`, `sendKeys(...)` or `clear()`. Before acting, Selenium checks that a user could do the same: the element must be **visible**, **enabled**, and **not covered** by another element; Selenium also scrolls it into view. If a check fails, Selenium throws an exception instead of pretending the action happened.

### Key terms

| Method | What it does | Example |
|---|---|---|
| `click()` | Clicks the element, like a mouse click | `loginButton.click()` |
| `sendKeys("text")` | Types text into a text box. **Adds** to what is already there. | `username.sendKeys("tomsmith")` |
| `sendKeys(Keys.ENTER)` | Presses a special key (`ENTER`, `TAB`, `BACK_SPACE`, ...) | `password.sendKeys(Keys.ENTER)` |
| `clear()` | Empties a text box | `username.clear()` |

**Other terms:**

- **`Keys`:** a Java enum (`org.openqa.selenium.Keys`) with every special keyboard key.
- **Interactable:** visible, enabled, and not covered, so a user could use it. Only interactable elements accept `click()` and `sendKeys(...)`.
- **Flash message:** a short message the page shows after an action, e.g. "You logged into a secure area!".

### Key ideas

- The pattern is always **find → act → check the result**: after typing and clicking, assert what the user should now **see** (a new URL, a message, a ticked box).
- `sendKeys` **adds** text. To replace the text in a box, call `clear()` first.
- Prefer **clicking the button** to submit a form; pressing `ENTER` is a separate test for keyboard users.

### Worked example: `LoginInteractionTest` on the-internet

The login page at `https://the-internet.herokuapp.com/login` has a username box (`id="username"`), a password box (`id="password"`) and a **Login** button. A correct login opens `/secure` and shows a green message.

**Step 1: Open the login page before each test.**

```java
class LoginInteractionTest extends BaseTest {

    @BeforeEach
    void openLoginPage() {
        driver.get("https://the-internet.herokuapp.com/login");
    }
}
```

**Step 2: Type into the two boxes.**

```java
@Test
void validLoginOpensSecureArea() {
    driver.findElement(By.id("username")).sendKeys("tomsmith");
    driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
}
```

**Step 3: Click Login, then check the result.** Add these lines to the same test:

```java
    driver.findElement(By.cssSelector("button[type='submit']")).click();

    assertEquals("https://the-internet.herokuapp.com/secure", driver.getCurrentUrl());
    String message = driver.findElement(By.id("flash")).getText();
    assertTrue(message.contains("You logged into a secure area!"));
```

**Step 4: A wrong password shows an error.**

```java
@Test
void wrongPasswordShowsError() {
    driver.findElement(By.id("username")).sendKeys("tomsmith");
    driver.findElement(By.id("password")).sendKeys("wrong");
    driver.findElement(By.cssSelector("button[type='submit']")).click();

    String message = driver.findElement(By.id("flash")).getText();
    assertTrue(message.contains("Your password is invalid!"));
}
```

**Step 5: `sendKeys` adds text; `clear()` empties the box.** `getDomProperty("value")` reads what is currently typed in a box.

```java
@Test
void sendKeysAddsAndClearEmpties() {
    WebElement username = driver.findElement(By.id("username"));

    username.sendKeys("tom");
    username.sendKeys("smith");
    assertEquals("tomsmith", username.getDomProperty("value"));

    username.clear();
    assertEquals("", username.getDomProperty("value"));
}
```

**Step 6: Clicking a checkbox.** On `/checkboxes` the first box starts unticked.

```java
@Test
void clickTicksACheckbox() {
    driver.get("https://the-internet.herokuapp.com/checkboxes");
    WebElement first = driver.findElements(By.cssSelector("input[type='checkbox']")).get(0);

    assertFalse(first.isSelected());
    first.click();
    assertTrue(first.isSelected());
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/LoginInteractionTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LoginInteractionTest extends BaseTest {

    @BeforeEach
    void openLoginPage() {
        driver.get("https://the-internet.herokuapp.com/login");
    }

    @Test
    void validLoginOpensSecureArea() {
        driver.findElement(By.id("username")).sendKeys("tomsmith");
        driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
        driver.findElement(By.cssSelector("button[type='submit']")).click();

        assertEquals("https://the-internet.herokuapp.com/secure", driver.getCurrentUrl());
        String message = driver.findElement(By.id("flash")).getText();
        assertTrue(message.contains("You logged into a secure area!"));
    }

    @Test
    void wrongPasswordShowsError() {
        driver.findElement(By.id("username")).sendKeys("tomsmith");
        driver.findElement(By.id("password")).sendKeys("wrong");
        driver.findElement(By.cssSelector("button[type='submit']")).click();

        String message = driver.findElement(By.id("flash")).getText();
        assertTrue(message.contains("Your password is invalid!"));
    }

    @Test
    void sendKeysAddsAndClearEmpties() {
        WebElement username = driver.findElement(By.id("username"));

        username.sendKeys("tom");
        username.sendKeys("smith");
        assertEquals("tomsmith", username.getDomProperty("value"));

        username.clear();
        assertEquals("", username.getDomProperty("value"));
    }

    @Test
    void clickTicksACheckbox() {
        driver.get("https://the-internet.herokuapp.com/checkboxes");
        WebElement first = driver.findElements(By.cssSelector("input[type='checkbox']")).get(0);

        assertFalse(first.isSelected());
        first.click();
        assertTrue(first.isSelected());
    }
}
```

### Checkpoint

You see the browser type, click and change page.

```text
✔ LoginInteractionTest
   ✔ validLoginOpensSecureArea()
   ✔ wrongPasswordShowsError()
   ✔ sendKeysAddsAndClearEmpties()
   ✔ clickTicksACheckbox()
```

### Your turn

1. Write `wrongUsernameShowsError`: log in as `nobody` with any password and check the message contains `Your username is invalid!`.
2. Log in by pressing **Enter** in the password box instead of clicking: `sendKeys("SuperSecretPassword!", Keys.ENTER)`. Check you reach `/secure`.
3. On `/checkboxes`, click the **second** box (which starts ticked) and check it is now unticked.
4. **Swag Labs:** open `https://www.saucedemo.com/`, log in as `standard_user` / `secret_sauce` (ids: `user-name`, `password`, `login-button`), and check the URL is `https://www.saucedemo.com/inventory.html`. Run it a few times: if it sometimes fails because the URL hasn't changed yet, you have met the problem topic 3.2 solves.

### Common errors

| You see | Why | Fix |
|---|---|---|
| Box contains `tomsmithtomsmith` | `sendKeys` adds to existing text | `clear()` before typing |
| `ElementNotInteractableException` | The element is hidden or zero-sized (often you found the wrong one) | Check the locator matches the visible element |
| `ElementClickInterceptedException` | Another element (banner, pop-up) covers it | Close the covering element first |
| `NoSuchElementException` right after a click | The next page or message was not there yet | Wait for it (topic 3.2) |

---

## 3.2 Waiting Strategies

### Definition

Web pages often change **after** they have loaded: a button starts a request, a spinner appears, and the result is drawn a few seconds later. Selenium does not know this; a find method searches **once, immediately** (Handout 2), so a test can look too early and fail. A **wait** pauses the test **until a condition is true**, for example "until the result is visible", or until a time limit runs out. Selenium has three kinds of wait: **implicit**, **explicit** and **fluent**. `Thread.sleep` is not a wait strategy; it is a fixed pause that is either too long or too short.

### Key terms

| Wait | How | When to use |
|---|---|---|
| **`Thread.sleep(ms)`** | Always pauses the full time | Never in tests: slow and still unreliable |
| **Implicit wait** | One setting for the whole driver: `driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10))`. Every find retries until the element exists. | Small scripts only. Only waits for elements to **exist**. |
| **Explicit wait** | `new WebDriverWait(driver, Duration.ofSeconds(10)).until(condition)` for one specific condition | **The default choice** |
| **Fluent wait** | An explicit wait where you also choose how often to check and which exceptions to ignore | Special cases |

**Common conditions** (class `ExpectedConditions`):

| Condition | Waits until the element... |
|---|---|
| `presenceOfElementLocated(by)` | is in the page (may still be hidden) |
| `visibilityOfElementLocated(by)` | is in the page **and visible** |
| `elementToBeClickable(by)` | is visible **and enabled** |
| `invisibilityOfElementLocated(by)` | is hidden or gone |
| `textToBe(by, "...")` | shows exactly this text |
| `urlContains("...")` | (the page URL contains this text) |

- **Timeout:** the most time a wait will spend. An explicit wait returns **as soon as** the condition is true; if the timeout passes first, it throws `TimeoutException`.

### Key ideas

- Wait for **what the user waits for**: the result being **visible**, a button being **clickable**, the URL changing.
- **Presence is not visibility.** An element can be in the page but hidden; `getText()` on it returns `""`.
- **Don't mix** implicit and explicit waits in the same project: wait times become unpredictable. Most teams keep implicit wait at 0 and use explicit waits.

### Worked example: `WaitTest` on the-internet's dynamic loading pages

On `https://the-internet.herokuapp.com/dynamic_loading/2`, clicking **Start** shows a loading bar for about 5 seconds, and then "Hello World!" is **added** to the page (`id="finish"`). On `/dynamic_loading/1` the text is already in the page but **hidden** until loading finishes.

**Step 1: Without a wait, the test fails.**

```java
@Test
void withoutAWaitTheResultIsMissing() {
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
    driver.findElement(By.cssSelector("#start button")).click();

    assertThrows(NoSuchElementException.class, () -> driver.findElement(By.id("finish")));
}
```

**Step 2: An explicit wait.** Wait up to 10 seconds for the result to be visible.

```java
@Test
void explicitWaitSeesTheResult() {
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
    driver.findElement(By.cssSelector("#start button")).click();

    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    WebElement finish = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish")));

    assertEquals("Hello World!", finish.getText());
}
```

**Step 3: Presence vs visibility,** on page 1, where the text is there but hidden.

```java
@Test
void presenceIsNotVisibility() {
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");
    driver.findElement(By.cssSelector("#start button")).click();
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

    WebElement present = wait.until(ExpectedConditions.presenceOfElementLocated(By.id("finish")));
    assertFalse(present.isDisplayed());                 // in the page, but still hidden

    WebElement visible = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish")));
    assertEquals("Hello World!", visible.getText());
}
```

**Step 4: The implicit wait, for comparison.** It makes `findElement` retry until the element exists.

```java
@Test
void implicitWaitAlsoFindsIt() {
    driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
    driver.findElement(By.cssSelector("#start button")).click();

    assertEquals("Hello World!", driver.findElement(By.id("finish")).getText());
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/WaitTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

class WaitTest extends BaseTest {

    @Test
    void withoutAWaitTheResultIsMissing() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
        driver.findElement(By.cssSelector("#start button")).click();

        assertThrows(NoSuchElementException.class, () -> driver.findElement(By.id("finish")));
    }

    @Test
    void explicitWaitSeesTheResult() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
        driver.findElement(By.cssSelector("#start button")).click();

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        WebElement finish = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish")));

        assertEquals("Hello World!", finish.getText());
    }

    @Test
    void presenceIsNotVisibility() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");
        driver.findElement(By.cssSelector("#start button")).click();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        WebElement present = wait.until(ExpectedConditions.presenceOfElementLocated(By.id("finish")));
        assertFalse(present.isDisplayed());

        WebElement visible = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish")));
        assertEquals("Hello World!", visible.getText());
    }

    @Test
    void implicitWaitAlsoFindsIt() {
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
        driver.findElement(By.cssSelector("#start button")).click();

        assertEquals("Hello World!", driver.findElement(By.id("finish")).getText());
    }
}
```

### Checkpoint

You see the loading bar in three of the four browsers. Each of those tests takes about **5 seconds**, not 10: the waits stop as soon as "Hello World!" appears.

```text
✔ WaitTest
   ✔ withoutAWaitTheResultIsMissing()
   ✔ explicitWaitSeesTheResult()
   ✔ presenceIsNotVisibility()
   ✔ implicitWaitAlsoFindsIt()
```

### Your turn

1. Copy `explicitWaitSeesTheResult` and replace the wait with `Thread.sleep(8000)` (add `throws InterruptedException` to the method). Compare the two test times in the IDE. Then delete the sleep version.
2. Change the timeout in `explicitWaitSeesTheResult` to **2 seconds** and run. Read the `TimeoutException` message: which condition and locator does it name? Put it back to 10.
3. On `/dynamic_loading/1`, wait with `invisibilityOfElementLocated(By.id("loading"))` until the loading bar has gone, then check the text of `#finish`.
4. **Swag Labs:** after logging in, wait with `ExpectedConditions.urlContains("inventory")` before checking the URL.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoSuchElementException` right after a click | The page hadn't added the element yet | Explicit wait for visibility |
| `getText()` returns `""` | Waited for **presence**, the element is still hidden | Wait for **visibility** |
| `TimeoutException` | The condition never became true: wrong locator, or the timeout is too short | Check the locator in DevTools; read the message |
| Tests sometimes pass, sometimes fail ("flaky") | `Thread.sleep` with a guessed time | Replace it with an explicit wait |

---

## 3.3 Select Elements

### Definition

A **dropdown** lets a user choose one option from a list. In HTML, a real dropdown is a **`<select>`** element with one **`<option>`** element per choice. Selenium's **`Select`** class wraps a `<select>` element and gives it dropdown methods: choose an option by its **visible text**, its **value** attribute or its **index** (position), and read which option is selected. `Select` only works on real `<select>` elements; many modern sites build dropdowns from ordinary `<div>` elements, which you click like any other element.

### Key terms

```html
<select id="dropdown">
  <option value="" disabled selected>Please select an option</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</select>
```

| Every option has... | Example for "Option 2" |
|---|---|
| **Visible text** (what the user sees) | `Option 2` |
| **Value** (the `value` attribute) | `2` |
| **Index** (position, starting at 0) | `2` |

| Method | What it does |
|---|---|
| `new Select(element)` | Wraps a `<select>` element |
| `selectByVisibleText("Option 1")` | Chooses the option with exactly this text |
| `selectByValue("2")` | Chooses the option with this `value` |
| `selectByIndex(1)` | Chooses the option at this position |
| `getFirstSelectedOption()` | Returns the selected option (a `WebElement`) |
| `getOptions()` | Returns all options as a `List<WebElement>` |
| `isMultiple()` | `true` if several options can be chosen at once |

### Key ideas

- **Visible text** reads like the requirement ("sort by Price (low to high)"); **value** survives wording changes. Avoid **index**: it breaks when options are added or reordered.
- After choosing, **check the result**: read `getFirstSelectedOption().getText()`, or what the page shows.
- If choosing an option changes the page, create a **new** `Select` before using it again.

### Worked example: `DropdownTest` on the-internet

The page `https://the-internet.herokuapp.com/dropdown` has the `<select id="dropdown">` shown above.

**Step 1: Open the page and wrap the `<select>`.**

```java
class DropdownTest extends BaseTest {

    @BeforeEach
    void openDropdownPage() {
        driver.get("https://the-internet.herokuapp.com/dropdown");
    }

    private Select dropdown() {
        return new Select(driver.findElement(By.id("dropdown")));
    }
}
```

**Step 2: Read the starting state.**

```java
@Test
void startsWithThePlaceholder() {
    assertFalse(dropdown().isMultiple());
    assertEquals(3, dropdown().getOptions().size());
    assertEquals("Please select an option", dropdown().getFirstSelectedOption().getText());
}
```

**Step 3: Choose by visible text.**

```java
@Test
void selectByVisibleText() {
    dropdown().selectByVisibleText("Option 1");
    assertEquals("Option 1", dropdown().getFirstSelectedOption().getText());
}
```

**Step 4: Choose by value and by index.**

```java
@Test
void selectByValueAndIndex() {
    dropdown().selectByValue("2");
    assertEquals("Option 2", dropdown().getFirstSelectedOption().getText());

    dropdown().selectByIndex(1);
    assertEquals("Option 1", dropdown().getFirstSelectedOption().getText());
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/DropdownTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.Select;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class DropdownTest extends BaseTest {

    @BeforeEach
    void openDropdownPage() {
        driver.get("https://the-internet.herokuapp.com/dropdown");
    }

    private Select dropdown() {
        return new Select(driver.findElement(By.id("dropdown")));
    }

    @Test
    void startsWithThePlaceholder() {
        assertFalse(dropdown().isMultiple());
        assertEquals(3, dropdown().getOptions().size());
        assertEquals("Please select an option", dropdown().getFirstSelectedOption().getText());
    }

    @Test
    void selectByVisibleText() {
        dropdown().selectByVisibleText("Option 1");
        assertEquals("Option 1", dropdown().getFirstSelectedOption().getText());
    }

    @Test
    void selectByValueAndIndex() {
        dropdown().selectByValue("2");
        assertEquals("Option 2", dropdown().getFirstSelectedOption().getText());

        dropdown().selectByIndex(1);
        assertEquals("Option 1", dropdown().getFirstSelectedOption().getText());
    }
}
```

### Checkpoint

You see the dropdown change in the browser.

```text
✔ DropdownTest
   ✔ startsWithThePlaceholder()
   ✔ selectByVisibleText()
   ✔ selectByValueAndIndex()
```

### Your turn

1. Loop over `dropdown().getOptions()` and print each option's text and `getDomAttribute("value")`. Which option has an empty value, and why can't a user choose it?
2. Try `selectByVisibleText("Option 3")`. Which exception do you get? Write a test with `assertThrows` for it.
3. **Swag Labs sort:** log in as `standard_user`, wrap the sort menu `By.cssSelector("[data-test='product-sort-container']")` in a `Select`, choose `Price (low to high)` by visible text, and check the first product name (`[data-test='inventory-item-name']`) is `Sauce Labs Onesie`.
4. Try `new Select(driver.findElement(By.id("username")))` on the-internet's login page. Which exception do you get, and why?

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoSuchElementException: Cannot locate option with text: ...` | The text doesn't match exactly | Copy the option text; or use `selectByValue` |
| `UnexpectedTagNameException` | The element is not a `<select>` | Use `Select` only on `<select>`; click custom dropdowns like other elements |
| `StaleElementReferenceException` on the second choice | The page redrew the dropdown after the first choice | Create a new `Select` each time (as `dropdown()` does) |
| `selectByIndex(1)` chose the "wrong" option | Index 0 is the placeholder | Prefer text or value |

---

**End of Handout 3.** You can now type, click and clear, wait for the page with explicit waits, and choose from dropdowns, all inside JUnit tests. **Next:** Handout 4, Actions, Alerts and Windows.
