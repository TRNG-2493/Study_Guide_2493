# Selenium In-Class Handout, Group 2: Navigating and Finding Elements

**Topics:** 2.1 Navigation methods · 2.2 Locator strategies · 2.3 Find methods

**How to use this handout:** the same layout as Handout 1. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Handout 1:** every example is a JUnit test class in `src/test/java/com/qea/selenium/tests` that `extends BaseTest`. `BaseTest` opens a fresh Chrome before each test and quits it afterwards, so a test only contains the steps that matter.

```java
class SomethingTest extends BaseTest {

    @Test
    void someCheck() {
        driver.get("https://...");          // driver comes from BaseTest
        assertEquals("...", driver.getTitle());
    }
}
```

Every test file starts with these imports (your IDE adds most of them for you):

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
```

**In this handout you learn to move between pages and to find elements and read them.** Typing, clicking and logging in come in Handout 3, so every page used here works **without logging in**.

**Practice sites:** Swag Labs `https://www.saucedemo.com` (its login page) and the-internet `https://the-internet.herokuapp.com`.

---

## 2.1 Navigation Methods

### Definition

**Navigation** means moving the browser from page to page, the way a user does with the address bar and the Back, Forward and Reload buttons. Selenium's navigation methods open a URL (`get` or `navigate().to`), move through the browser's **history** (`navigate().back()` and `navigate().forward()`), and reload the current page (`navigate().refresh()`). Three more methods tell you **where you are**: `getCurrentUrl()`, `getTitle()` and `getPageSource()`. A test uses them to reach the page it wants to check and to prove that it really got there.

### Key terms

| Method | What it does | Browser equivalent |
|---|---|---|
| `driver.get(url)` | Opens a URL and waits until the page has loaded | Typing in the address bar + Enter |
| `driver.navigate().to(url)` | Exactly the same as `get(url)` | Same |
| `driver.navigate().back()` | Goes one page back in history | Back button |
| `driver.navigate().forward()` | Goes one page forward in history | Forward button |
| `driver.navigate().refresh()` | Reloads the current page | Reload button / F5 |
| `driver.getCurrentUrl()` | Returns the URL in the address bar | Reading the address bar |
| `driver.getTitle()` | Returns the page title | Reading the tab's name |
| `driver.getPageSource()` | Returns the page's HTML as one long `String` | *View page source* |

**Other terms:**

- **History:** the list of pages visited in this tab. `back()` and `forward()` move along it.
- **Page load:** `get()` returns only when the browser reports the page has finished loading.

### Key ideas

- Use `get()` to open a page and `navigate()` for history; most teams use this style.
- **Check where you are with the URL.** Many sites use the same title on every page (the-internet's title is always "The Internet"), so the URL is the more reliable check.
- `refresh()` reloads the page but is **not** a reset: the site still remembers you (cookies stay).
- New tabs and windows do **not** use `back()`/`forward()`; they are covered in Handout 4.

### Worked example: `NavigationTest`

**Step 1: Create the test class with the URLs we'll use.** Constants keep the URLs in one place.

```java
class NavigationTest extends BaseTest {

    static final String HOME  = "https://the-internet.herokuapp.com/";
    static final String LOGIN = "https://the-internet.herokuapp.com/login";
}
```

**Step 2: Open a page and check where we are.**

```java
@Test
void getOpensThePage() {
    driver.get(HOME);
    assertEquals(HOME, driver.getCurrentUrl());
    assertEquals("The Internet", driver.getTitle());
}
```

**Step 3: Back and forward through history.** Visit two pages, then move between them.

```java
@Test
void backAndForwardMoveThroughHistory() {
    driver.get(HOME);
    driver.navigate().to(LOGIN);
    assertEquals(LOGIN, driver.getCurrentUrl());

    driver.navigate().back();
    assertEquals(HOME, driver.getCurrentUrl());

    driver.navigate().forward();
    assertEquals(LOGIN, driver.getCurrentUrl());
}
```

**Step 4: Refresh stays on the same page.**

```java
@Test
void refreshStaysOnTheSamePage() {
    driver.get(LOGIN);
    driver.navigate().refresh();
    assertEquals(LOGIN, driver.getCurrentUrl());
}
```

**Step 5: The page source.** It contains the page's HTML, so we can check a piece of text is in it.

```java
@Test
void pageSourceContainsTheHeading() {
    driver.get(LOGIN);
    assertTrue(driver.getPageSource().contains("Login Page"));
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/NavigationTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NavigationTest extends BaseTest {

    static final String HOME  = "https://the-internet.herokuapp.com/";
    static final String LOGIN = "https://the-internet.herokuapp.com/login";

    @Test
    void getOpensThePage() {
        driver.get(HOME);
        assertEquals(HOME, driver.getCurrentUrl());
        assertEquals("The Internet", driver.getTitle());
    }

    @Test
    void backAndForwardMoveThroughHistory() {
        driver.get(HOME);
        driver.navigate().to(LOGIN);
        assertEquals(LOGIN, driver.getCurrentUrl());

        driver.navigate().back();
        assertEquals(HOME, driver.getCurrentUrl());

        driver.navigate().forward();
        assertEquals(LOGIN, driver.getCurrentUrl());
    }

    @Test
    void refreshStaysOnTheSamePage() {
        driver.get(LOGIN);
        driver.navigate().refresh();
        assertEquals(LOGIN, driver.getCurrentUrl());
    }

    @Test
    void pageSourceContainsTheHeading() {
        driver.get(LOGIN);
        assertTrue(driver.getPageSource().contains("Login Page"));
    }
}
```

### Checkpoint

Four browsers open and close, one per test:

```text
✔ NavigationTest
   ✔ getOpensThePage()
   ✔ backAndForwardMoveThroughHistory()
   ✔ refreshStaysOnTheSamePage()
   ✔ pageSourceContainsTheHeading()
```

### Your turn

1. **Predict, then test.** Open `HOME`, then `.../checkboxes`, then `.../dropdown`. Call `back()` twice and `forward()` once. Write the URL you expect in an `assertEquals` **before** you run the test.
2. Write a test that opens `https://www.saucedemo.com/` and then `https://the-internet.herokuapp.com/`, goes `back()`, and checks that the title is `Swag Labs`.
3. Write a test that uses `navigate().to(...)` instead of `get(...)` for every page in step 3 of the worked example. Does anything change?

### Common errors

| You see | Why | Fix |
|---|---|---|
| `expected: <https://the-internet.herokuapp.com> but was: <https://the-internet.herokuapp.com/>` | The browser adds a `/` at the end of a site's home address | Include the trailing `/` in the expected URL |
| `back()` seems to do nothing | Nothing was visited before, so there is no history | Visit at least two pages before going back |
| Title check passes on the wrong page | Same title on every page | Check `getCurrentUrl()` instead |

---

## 2.2 Locator Strategies

### Definition

A **web element** is anything on a page: a heading, a text box, a button, a link. A **locator** is a description that tells Selenium **how to find** one element on the page, for example "the element whose id is `user-name`". In Selenium Java, a locator is a `By` object, created with methods such as `By.id(...)`, `By.name(...)` or `By.cssSelector(...)`. A locator does nothing on its own: Selenium only searches the page when you pass it to `driver.findElement(locator)`. The way you choose to describe an element (by id, name, CSS, XPath and so on) is the **locator strategy**.

### Key terms

**HTML you need to read:**

```html
<input id="user-name" name="user-name" class="input_error form_input" placeholder="Username" type="text">
```

| Part | Example | Meaning |
|---|---|---|
| Tag | `input` | The kind of element |
| Attribute | `id="user-name"` | A name/value pair inside the tag |
| `id` | `user-name` | Should be unique on the page |
| `class` | `input_error form_input` | One or more class names, separated by spaces |

**The eight locator strategies:**

| Strategy | Finds the element... | Example on Swag Labs' login page |
|---|---|---|
| `By.id` | with this `id` | `By.id("user-name")` |
| `By.name` | with this `name` attribute | `By.name("password")` |
| `By.className` | with this **one** class name | `By.className("submit-button")` |
| `By.tagName` | of this type | `By.tagName("input")` |
| `By.linkText` | link (`<a>`) with **exactly** this text | `By.linkText("Form Authentication")` (the-internet) |
| `By.partialLinkText` | link whose text **contains** this | `By.partialLinkText("Dynamic")` (the-internet) |
| `By.cssSelector` | matching a CSS selector | `By.cssSelector("[data-test='login-button']")` |
| `By.xpath` | matching an XPath expression | `By.xpath("//div[@class='login_password']/h4")` |

**CSS and XPath patterns for beginners:**

| You want | CSS selector | XPath |
|---|---|---|
| By id | `#user-name` | `//*[@id='user-name']` |
| By class | `.submit-button` | `//*[contains(@class,'submit-button')]` |
| By attribute | `[data-test='login-button']` | `//*[@data-test='login-button']` |
| Tag + attribute | `input[type='submit']` | `//input[@type='submit']` |
| Child of a parent | `div.login_password > h4` | `//div[@class='login_password']/h4` |
| By visible text | (not possible) | `//h4[text()='Password for all users:']` |

**Two methods we use to see results** (Topic 2.3 explains them fully):

- `driver.findElement(locator)` asks the browser for the element and returns it as a `WebElement`.
- `element.getText()` returns its visible text; `element.getDomAttribute("name")` returns one of its attributes.

### Key ideas

- **Choose in this order:** `id` or a test attribute like `data-test` → `name` → CSS selector → XPath. Prefer what is unique and unlikely to change.
- **Avoid** long, position-based paths such as `/html/body/div[2]/div/div[3]/input`: they break when the page layout changes.
- **Check a locator before using it:** open DevTools (F12), go to the *Elements* tab, press **Ctrl+F**, and type your CSS selector or XPath. It should say **1 of 1**.

### Worked example: `LocatorTest` on Swag Labs' login page

**Step 1: Find the HTML.** Open `https://www.saucedemo.com/` in Chrome, right-click the **Username** box and choose **Inspect**. The *Elements* tab highlights its HTML; note the `id`, `name` and `data-test` attributes. Do the same for the **Login** button.

**Step 2: Create the test class; open the page before each test.** This `@BeforeEach` runs **after** the one in `BaseTest`, so the browser already exists.

```java
class LocatorTest extends BaseTest {

    @BeforeEach
    void openLoginPage() {
        driver.get("https://www.saucedemo.com/");
    }
}
```

**Step 3: `id` and `name`.**

```java
@Test
void findByIdAndName() {
    WebElement username = driver.findElement(By.id("user-name"));
    assertEquals("Username", username.getDomAttribute("placeholder"));

    WebElement password = driver.findElement(By.name("password"));
    assertEquals("password", password.getDomAttribute("type"));
}
```

**Step 4: `className` and `cssSelector`.** Both find the Login button.

```java
@Test
void findByClassNameAndCss() {
    WebElement byClass = driver.findElement(By.className("submit-button"));
    assertEquals("Login", byClass.getDomAttribute("value"));

    WebElement byCss = driver.findElement(By.cssSelector("[data-test='login-button']"));
    assertEquals("login-button", byCss.getDomAttribute("id"));
}
```

**Step 5: `xpath`.** The text under the password list on the right of the page.

```java
@Test
void findByXpath() {
    WebElement heading = driver.findElement(By.xpath("//div[@class='login_password']/h4"));
    assertEquals("Password for all users:", heading.getText());
}
```

**Step 6: Links, on the-internet's home page.**

```java
@Test
void findLinksByText() {
    driver.get("https://the-internet.herokuapp.com/");

    WebElement exact = driver.findElement(By.linkText("Form Authentication"));
    assertEquals("Form Authentication", exact.getText());

    WebElement partial = driver.findElement(By.partialLinkText("Dynamic"));
    assertEquals("Dynamic Content", partial.getText());
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/LocatorTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import static org.junit.jupiter.api.Assertions.assertEquals;

class LocatorTest extends BaseTest {

    @BeforeEach
    void openLoginPage() {
        driver.get("https://www.saucedemo.com/");
    }

    @Test
    void findByIdAndName() {
        WebElement username = driver.findElement(By.id("user-name"));
        assertEquals("Username", username.getDomAttribute("placeholder"));

        WebElement password = driver.findElement(By.name("password"));
        assertEquals("password", password.getDomAttribute("type"));
    }

    @Test
    void findByClassNameAndCss() {
        WebElement byClass = driver.findElement(By.className("submit-button"));
        assertEquals("Login", byClass.getDomAttribute("value"));

        WebElement byCss = driver.findElement(By.cssSelector("[data-test='login-button']"));
        assertEquals("login-button", byCss.getDomAttribute("id"));
    }

    @Test
    void findByXpath() {
        WebElement heading = driver.findElement(By.xpath("//div[@class='login_password']/h4"));
        assertEquals("Password for all users:", heading.getText());
    }

    @Test
    void findLinksByText() {
        driver.get("https://the-internet.herokuapp.com/");

        WebElement exact = driver.findElement(By.linkText("Form Authentication"));
        assertEquals("Form Authentication", exact.getText());

        WebElement partial = driver.findElement(By.partialLinkText("Dynamic"));
        assertEquals("Dynamic Content", partial.getText());
    }
}
```

### Checkpoint

```text
✔ LocatorTest
   ✔ findByIdAndName()
   ✔ findByClassNameAndCss()
   ✔ findByXpath()
   ✔ findLinksByText()
```

In DevTools, `[data-test='login-button']` and `//div[@class='login_password']/h4` each show **1 of 1**.

### Your turn

1. Find the **Password** box three more ways: by `id`, by a CSS selector and by an XPath. Check each one in DevTools first (1 of 1), then in a test.
2. On the-internet's home page, find the link "Checkboxes" with `By.linkText`, and the link "Drag and Drop" with `By.partialLinkText("Drag")`. Assert their text.
3. On Swag Labs' login page, write an XPath that finds the `h4` "Accepted usernames are:" by its **text**, and assert it.
4. Which locator is better, and why? (a) `By.id("login-button")` or `By.xpath("/html/body/div/div/div[2]/div[1]/div/div/form/input")`. (b) `By.className("submit-button")` or `By.cssSelector("[data-test='login-button']")`.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoSuchElementException` | The locator matches nothing: a typo, or wrong page | Copy the value from DevTools; check the URL |
| `InvalidSelectorException` | Broken CSS/XPath, or two class names in `By.className("a b")` | Test it in DevTools; for two classes use `By.cssSelector(".a.b")` |
| `By.linkText` finds nothing | The text must match **exactly** (spaces, capital letters) | Copy the text, or use `partialLinkText` |
| Test works today, fails next sprint | Position-based XPath or generated ids (`id="ember123"`) | Use stable ids, `data-test` attributes or meaningful text |

---

## 2.3 Find Methods

### Definition

**Find methods** ask the browser to search the page with a locator. `driver.findElement(locator)` returns the **first** element that matches, as a `WebElement`; if nothing matches it throws a `NoSuchElementException`. `driver.findElements(locator)` returns a **list** of every match; if nothing matches the list is simply **empty**. A `WebElement` is Selenium's handle on one element: you can read it (text, attributes, state) and, in Handout 3, act on it. Both find methods search **once, immediately**; they do not wait for elements that appear later (Handout 3).

### Key terms

| Method | Returns | If nothing matches |
|---|---|---|
| `driver.findElement(by)` | One `WebElement` (the first match) | Throws `NoSuchElementException` |
| `driver.findElements(by)` | `List<WebElement>` (all matches) | Empty list, no exception |
| `element.findElement(by)` / `element.findElements(by)` | Searches **inside** that element only (**scoped search**) | Same rules |

**Reading a `WebElement`:**

| Method | Returns | Example |
|---|---|---|
| `getText()` | The visible text | `"Data Tables"` |
| `getDomAttribute("type")` | An attribute exactly as written in the HTML | `"checkbox"` |
| `getTagName()` | The tag name | `"td"` |
| `isDisplayed()` | Can a user see it? | `true` |
| `isSelected()` | Is a checkbox or radio button ticked? | `false` |
| `isEnabled()` | Can it be used (not disabled)? | `true` |

### Key ideas

- Use `findElement` when you expect **exactly one** element; use `findElements` for **many**, or to check that something is **absent**: `findElements(by).isEmpty()`.
- A **scoped search** (`row.findElements(...)`) only looks inside one element, such as one row of a table. It is how you read structured data.
- Text boxes have no visible text, so `getText()` on an input returns `""`. Read their attributes instead.

### Worked example: `FindTest` on the-internet's tables and checkboxes

`https://the-internet.herokuapp.com/tables` shows a table (`id="table1"`) of four people. The first row is **Smith, John**.

**Step 1: `findElement` returns one element.**

```java
@Test
void findElementReturnsOne() {
    driver.get("https://the-internet.herokuapp.com/tables");
    WebElement heading = driver.findElement(By.tagName("h3"));
    assertEquals("Data Tables", heading.getText());
}
```

**Step 2: `findElements` returns a list.** One `<tr>` per person in the table body.

```java
@Test
void findElementsReturnsAll() {
    driver.get("https://the-internet.herokuapp.com/tables");
    List<WebElement> rows = driver.findElements(By.cssSelector("#table1 tbody tr"));
    assertEquals(4, rows.size());
}
```

**Step 3: A scoped search inside the first row.** `firstRow.findElements(...)` only finds the cells of that row.

```java
@Test
void scopedSearchReadsOneRow() {
    driver.get("https://the-internet.herokuapp.com/tables");
    WebElement firstRow = driver.findElements(By.cssSelector("#table1 tbody tr")).get(0);
    List<WebElement> cells = firstRow.findElements(By.tagName("td"));

    assertEquals("Smith", cells.get(0).getText());
    assertEquals("John", cells.get(1).getText());
}
```

**Step 4: When nothing matches.** `findElement` throws; `findElements` returns an empty list.

```java
@Test
void nothingMatches() {
    driver.get("https://the-internet.herokuapp.com/tables");
    By missing = By.id("does-not-exist");

    assertThrows(NoSuchElementException.class, () -> driver.findElement(missing));
    assertTrue(driver.findElements(missing).isEmpty());
}
```

**Step 5: Reading state on `/checkboxes`.** The page has two checkboxes; the second starts ticked.

```java
@Test
void readCheckboxState() {
    driver.get("https://the-internet.herokuapp.com/checkboxes");
    List<WebElement> boxes = driver.findElements(By.cssSelector("input[type='checkbox']"));

    assertEquals(2, boxes.size());
    assertFalse(boxes.get(0).isSelected());
    assertTrue(boxes.get(1).isSelected());
    assertEquals("checkbox", boxes.get(0).getDomAttribute("type"));
}
```

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/FindTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebElement;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FindTest extends BaseTest {

    @Test
    void findElementReturnsOne() {
        driver.get("https://the-internet.herokuapp.com/tables");
        WebElement heading = driver.findElement(By.tagName("h3"));
        assertEquals("Data Tables", heading.getText());
    }

    @Test
    void findElementsReturnsAll() {
        driver.get("https://the-internet.herokuapp.com/tables");
        List<WebElement> rows = driver.findElements(By.cssSelector("#table1 tbody tr"));
        assertEquals(4, rows.size());
    }

    @Test
    void scopedSearchReadsOneRow() {
        driver.get("https://the-internet.herokuapp.com/tables");
        WebElement firstRow = driver.findElements(By.cssSelector("#table1 tbody tr")).get(0);
        List<WebElement> cells = firstRow.findElements(By.tagName("td"));

        assertEquals("Smith", cells.get(0).getText());
        assertEquals("John", cells.get(1).getText());
    }

    @Test
    void nothingMatches() {
        driver.get("https://the-internet.herokuapp.com/tables");
        By missing = By.id("does-not-exist");

        assertThrows(NoSuchElementException.class, () -> driver.findElement(missing));
        assertTrue(driver.findElements(missing).isEmpty());
    }

    @Test
    void readCheckboxState() {
        driver.get("https://the-internet.herokuapp.com/checkboxes");
        List<WebElement> boxes = driver.findElements(By.cssSelector("input[type='checkbox']"));

        assertEquals(2, boxes.size());
        assertFalse(boxes.get(0).isSelected());
        assertTrue(boxes.get(1).isSelected());
        assertEquals("checkbox", boxes.get(0).getDomAttribute("type"));
    }
}
```

### Checkpoint

```text
✔ FindTest
   ✔ findElementReturnsOne()
   ✔ findElementsReturnsAll()
   ✔ scopedSearchReadsOneRow()
   ✔ nothingMatches()
   ✔ readCheckboxState()
```

### Your turn

1. In the same table, read the **third** row and assert the last name (`Doe`) and first name (`Jason`).
2. Count the **columns** of `#table1` (the `th` elements in its `thead`) and assert there are 6.
3. On Swag Labs' login page, use `findElements(By.tagName("input"))` and assert there are 3 inputs. Then use `isDisplayed()` to check the first one is visible.
4. Write a test that proves the-internet's home page has **no** element with the id `user-name` (without using `assertThrows`).

### Common errors

| You see | Why | Fix |
|---|---|---|
| `NoSuchElementException` | `findElement` found nothing | Check the locator in DevTools; for "is it absent?" use `findElements(...).isEmpty()` |
| `assertThrows` reports the wrong exception type | You imported `java.util.NoSuchElementException` | Import `org.openqa.selenium.NoSuchElementException` |
| `IndexOutOfBoundsException` | `rows.get(5)` on a list with fewer items | Check `rows.size()` first |
| `getText()` returns `""` | The element is an input (no text), or hidden | Read an attribute, or check `isDisplayed()` |
| Found the wrong cell | Searched the whole page (`driver.findElements`) instead of the row | Use a scoped search: `row.findElements(...)` |

---

**End of Handout 2.** You can move between pages and check where you are, write locators with all eight strategies, and find and read elements one at a time or in lists. **Next:** Handout 3, Waiting and Interacting: waiting for elements, typing, clicking, and choosing from dropdowns.
