# Find Methods

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **what** `findElement()` and `findElements()` are, **why** Selenium has two of them, and **when** to choose each.
- Explain precisely what happens when no element matches (`NoSuchElementException` versus an empty list) and read the exception text to diagnose the cause.
- Read data from a found element: `getText()`, `getAttribute()`, `getDomProperty()`, `getDomAttribute()`, `getCssValue()`, `getTagName()`, `getSize()`, `getLocation()`, and `getRect()`.
- Check element state with `isDisplayed()`, `isEnabled()`, and `isSelected()`, and explain the difference between "present" and "displayed".
- Narrow a search by finding elements **inside** other elements (scoped or chained search) and explain why `.//` matters in XPath.
- Use `findElements` safely to test whether something exists, and write a small reusable helper for it.
- Perform the first basic interactions, `click()`, `sendKeys()`, and `clear()`, so that you can automate a real login flow (these are covered in depth on Tuesday).
- Run a complete guided lab against saucedemo.com and predict its output.

---

## Why This Matters

In the previous lessons you learned to *describe* an element with a locator (`By.id`, `By.cssSelector`, `By.xpath`, and so on). A `By` object is only a description. It is like writing "the red door on the left side of the house" on a piece of paper. Nothing has been found yet. This lesson is where Selenium actually walks up to the house, finds the door, and hands you a reference to it so you can read it and act on it.

Almost every line of a real test is some form of: **find this element, then do something with it**. Examples from a tester's normal day:

- "Find the username box and type a name into it."
- "Find all product cards and check that there are six."
- "Find the error banner and check that its text says *Epic sadface*."
- "Find the Submit button and check that it is disabled until the form is valid."

Find methods are also where beginners meet Selenium's most famous exception, `NoSuchElementException`. It is the single most common red line in a test report. Knowing exactly why it is thrown, and when a list-returning method is the better tool, will save you hours of confusion.

**A tester's morning.** Imagine you come in on Monday and the nightly run has 14 red tests. Twelve of them show `NoSuchElementException`. A beginner opens each test and starts changing locators at random. An experienced tester asks first: *Did the locator stop matching because the page changed? Did the element load later than the code looked for it? Is the element inside an iframe? Is the application actually broken?* By the end of this lesson you will be able to ask those four questions in the right order.

In **Project 2** (the Test Automation Framework), the helper methods in your base page class will wrap these calls (for example `click(By locator)` and `getTextOf(By locator)`). A wrapper is only as good as your understanding of what is inside it, so this lesson is the foundation under that framework. This week's Epic is to build a Selenium test framework with BDD; every step definition you write on Thursday and Friday will, deep down, call `findElement`.

---

## The Concept

### 1. `findElement()`: One Element

**What it is.** `findElement` is a method on the `WebDriver` object. You give it a `By` locator; it asks the browser to search the current page's DOM and returns **one** element.

**Why it exists.** Most actions in a test target exactly one thing: one text box, one button, one link. This method gives you that one thing as a Java object you can work with.

**How it works.**

```java
WebElement username = driver.findElement(By.id("user-name"));
```

Step-by-step, "what happens when this line runs":

1. Java evaluates `By.id("user-name")`. This creates a small `By` object that only stores the strategy (`id`) and the value (`user-name`). Nothing has touched the browser yet.
2. `driver.findElement(...)` sends an HTTP request to the browser driver (for Chrome, `chromedriver`) saying "find an element using this strategy and value". You learned this request/response flow in the architecture lesson.
3. The driver asks the browser to search the page's DOM, from the top of the document downward.
4. If a match is found, the driver replies with a **unique element identifier** (an internal id such as `f.1234.5678`). Selenium wraps that id in a `WebElement` object and returns it to your code.
5. If no match is found, the driver replies with an error, and Selenium throws `NoSuchElementException` in your Java code.

Facts to remember:

- **Signature:** `WebElement findElement(By locator)`
- **Returns:** the **first** element in the DOM that matches the locator (document order, top to bottom).
- **If nothing matches:** throws `NoSuchElementException`.
- **If several match:** returns only the first one, **silently**. No warning is given. That is a common source of hidden bugs; make your locators unique.

**What a `WebElement` really is.** A `WebElement` is a *reference* (a handle) to a specific element living inside the browser. It is not a copy of the HTML and it does not contain the text. Think of it as a **TV remote control** that is paired to one particular TV. When you press `click()` on the remote, the signal goes to the real TV (the browser). If the TV is replaced by a new one (the page reloads), the old remote no longer works, and Selenium says so with a `StaleElementReferenceException` (see the Common Mistakes section).

**When to use it.** Use `findElement` whenever you are going to interact with, or read, exactly one element that you expect to exist.

### 2. `findElements()`: Many Elements

**What it is.** The plural version returns a Java `List` of every matching element.

**Why it exists.** Pages contain repeated things: rows in a table, product cards, menu items, search results. You often need to count them, loop over them, or find the one with a certain text. A method that returns only the first match cannot do that.

```java
List<WebElement> items = driver.findElements(By.className("inventory_item"));
System.out.println("Products shown: " + items.size());
```

- **Signature:** `List<WebElement> findElements(By locator)`
- **Returns:** a list of **all** matching elements, in document order.
- **If nothing matches:** returns an **empty list** (`size() == 0`). It does **not** throw an exception.
- **Import needed:** `java.util.List`.

**Why the different "not found" behaviour?** The two methods answer different questions. `findElement` says "I need this thing to act on it; if it is not there, something is wrong, so stop the test loudly." `findElements` says "show me everything that matches"; "nothing" is a perfectly valid answer to that question, just like asking for all red cars in a car park and being told "none".

| | `findElement` | `findElements` |
|---|---|---|
| Return type | `WebElement` | `List<WebElement>` |
| No match | Throws `NoSuchElementException` | Returns an empty list |
| Multiple matches | Returns the first | Returns all |
| Waits for the element? | No (see Tuesday) | No (see Tuesday) |
| Typical use | Interact with one specific element | Count, loop, check existence |

**Real-world scenarios.**

| Scenario | Method | Why |
|---|---|---|
| Type into the username box | `findElement` | Exactly one target |
| Verify the shop shows 6 products | `findElements` | You need a count |
| Print every menu item | `findElements` | You need to loop |
| Verify no error banner is shown | `findElements` | Absence is the expected result |
| Click the "Add to cart" button of the third product | `findElements` then `.get(2)` | Choose by position |

**A beginner detail on lists.** `List` indexes start at `0`. `items.get(0)` is the first element, `items.get(items.size() - 1)` is the last. Calling `items.get(10)` on a list with 6 items throws `IndexOutOfBoundsException`. That is a Java exception, not a Selenium one, and it is a hint that your list was shorter than you assumed.

### 3. The `NoSuchElementException`

**What it means.** Selenium looked at the page *right now* and found no element matching your locator.

Suppose the page does not contain `By.id("missing")`:

```java
driver.findElement(By.id("missing"));
```

The console shows something like:

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: {"method":"css selector","selector":"[id="missing"]"}
  (Session info: chrome=126.0.6478.127)
For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
Build info: version: '4.21.0', ...
Driver info: org.openqa.selenium.chrome.ChromeDriver
```

**How to read this message.** Three parts matter:

- `no such element`: the error category.
- `"method":"css selector","selector":"[id=\"missing\"]"`: what Selenium actually searched for. Notice that Selenium 4 translates `By.id("missing")` into the CSS selector `[id="missing"]` behind the scenes. This is useful: it shows you the *exact* locator that failed, so you can paste it into the DevTools console to test it.
- The line number in the stack trace that follows tells you which of your test lines failed.

Common causes (in order of how often they occur):

1. **Typo or wrong locator.** Re-verify in DevTools (`$$("[id='missing']")` in the Console, or Ctrl+F in the Elements tab).
2. **Timing.** The element has not appeared yet (the page is still loading, or JavaScript has not inserted the element). Handling this is the topic of Tuesday's waits.
3. **Wrong context.** The element is inside an `<iframe>` or another browser window or tab; Selenium must switch to it first. Windows and iframes are covered in depth on Wednesday.
4. **The element is genuinely absent**, which may be a real application bug (and a correct test failure!).
5. **Wrong page.** A previous step failed silently and you are not on the page you think you are (for example the login failed, so the inventory list does not exist). Printing `driver.getCurrentUrl()` quickly reveals this.

> **Important:** `NoSuchElementException` is not always a *test* problem. If your test is asserting "the error message must not be displayed", then absence is the *expected* result. That is where `findElements` helps (next section).

**Troubleshooting walk-through 1: "It works in DevTools but not in Selenium."**

Situation: You type `$("#login-button")` in the browser console and it finds the button, yet your test throws `NoSuchElementException` for `By.id("login-button")`.

Diagnosis steps:

1. Print the URL and title right before the failing line: `System.out.println(driver.getCurrentUrl() + " | " + driver.getTitle());`. If the URL is not what you expect, an earlier step took you somewhere else.
2. Take a screenshot at that moment (the Screenshots lesson shows how). Look at the picture: is a cookie banner or an error page showing?
3. Check whether the element sits inside an `<iframe>` in DevTools (the Elements panel shows `<iframe>` ancestors). If it does, the console may be searching inside the frame while Selenium searches the main page.
4. If the page is slow, the element may appear a moment after your code looks. Add a temporary `Thread.sleep(2000)` *only to test the theory*. If the problem disappears, you have a timing problem, and you will fix it properly on Tuesday with waits (never leave `Thread.sleep` in real tests).

**Troubleshooting walk-through 2: "The test passed but clicked the wrong thing."**

Situation: `driver.findElement(By.className("btn"))` clicks a button, but not the one you intended. Cause: `findElement` returns the first match silently. Diagnosis: run `driver.findElements(By.className("btn")).size()`. If the answer is more than 1, your locator is not unique. Fix: use a more specific locator (an id, a `data-test` attribute, or a scoped search, section 8).

### 4. Checking Whether an Element Exists

**What and why.** Sometimes you need a yes/no answer: "is the error banner on the page?" Using `findElement` for this forces you into `try/catch`. A cleaner idiom uses `findElements`, with no exception handling needed:

```java
boolean errorShown = !driver.findElements(By.cssSelector("[data-test='error']")).isEmpty();
```

Reading it from the inside out: `findElements(...)` returns a list; `.isEmpty()` is `true` when the list has no items; the `!` flips it, so `errorShown` is `true` when at least one element was found.

A more readable helper:

```java
private boolean isPresent(WebDriver driver, By locator) {
    return !driver.findElements(locator).isEmpty();
}
```

Line by line:

- `private boolean isPresent(...)`: a method that is only visible inside this class and returns `true` or `false`.
- `WebDriver driver, By locator`: it receives the browser and the description of what to look for, so it works for any element.
- `return !driver.findElements(locator).isEmpty();`: the same idiom as above, packaged under a meaningful name. Later, in Project 2, this kind of method lives in your `BasePage` class.

Distinguish two important ideas:

- **Present:** the element exists in the DOM (the HTML structure of the page).
- **Displayed:** the element exists *and* is visible to the user (not `display:none`, not `visibility:hidden`, not zero size). Use `isDisplayed()` (section 6).

A real-world analogy: a **spare tyre** is *present* in the car boot, but it is not *displayed*; you cannot see it while driving. A test that says "assert the warning is shown" needs *displayed*, not merely *present*.

If you want "present **and** visible" without exceptions:

```java
private boolean isVisible(WebDriver driver, By locator) {
    List<WebElement> found = driver.findElements(locator);
    return !found.isEmpty() && found.get(0).isDisplayed();
}
```

Here `&&` is "short-circuit and": if the list is empty the left side is `false`, so Java never evaluates the right side, and `get(0)` is never called on an empty list (which would crash).

### 5. Reading from a `WebElement`

Once you have an element, you can ask it questions. Think of the element as a person and these methods as questions you can ask them.

| Method | Returns | Example |
|---|---|---|
| `getText()` | The **visible** text (like a user would read), with leading/trailing spaces trimmed | `error.getText()` |
| `getAttribute("name")` | The value of a property or attribute | `input.getAttribute("placeholder")` |
| `getDomProperty("name")` | The live DOM property value (Selenium 4) | `input.getDomProperty("value")` |
| `getDomAttribute("name")` | The HTML attribute exactly as written in the markup (Selenium 4) | `input.getDomAttribute("class")` |
| `getCssValue("prop")` | A computed CSS property | `btn.getCssValue("background-color")` |
| `getTagName()` | The tag name, lowercase | `"input"` |
| `getSize()` | Width and height in pixels (a `Dimension`) | `btn.getSize().getWidth()` |
| `getLocation()` | Top-left corner position (a `Point`) | `btn.getLocation().getY()` |
| `getRect()` | Position and size together (a `Rectangle`) | `btn.getRect()` |
| `getAccessibleName()` / `getAriaRole()` | What assistive technology would announce (Selenium 4) | `btn.getAriaRole()` |

**Details worth knowing:**

- `getText()` returns only what is **visible**. Hidden elements return an empty string. For hidden text use `getAttribute("textContent")`.
- To read what a user **typed into an input box**, use `getAttribute("value")` (or `getDomProperty("value")`). `getText()` on an `<input>` returns empty, because the typed text is a *value*, not the element's text content.
- `getAttribute` is long-standing and tolerant (it checks the property first, then the attribute). In Selenium 4 the more precise `getDomProperty` and `getDomAttribute` were added. For beginners and most tests, `getAttribute` is fine; just know the newer ones exist.
- `getCssValue("color")` returns a computed value such as `rgba(255, 0, 0, 1)`, not `red`. Colors are always returned in `rgba(...)` form, so compare against that format.
- `getText()` on a block such as a `<div>` returns the text of the element **and all its descendants**, with line breaks where the browser would show them.

**Attribute versus property: a plain-language explanation.** An HTML **attribute** is what is written in the page's source: `<input value="abc">` has the attribute `value="abc"`. A DOM **property** is the *live* state in the browser's memory. When a user types "xyz" into that box, the attribute in the source still says `abc`, but the property is now `xyz`.

| Call | After the user typed "xyz" |
|---|---|
| `getDomAttribute("value")` | `"abc"` (what the markup said) |
| `getDomProperty("value")` | `"xyz"` (the live value) |
| `getAttribute("value")` | `"xyz"` (checks property first) |

**Attributes that behave unexpectedly.** For boolean attributes such as `disabled` or `checked`, `getAttribute("disabled")` returns the string `"true"` when set and `null` when not. Always compare safely: `"true".equals(el.getAttribute("disabled"))` or, better, just use `isEnabled()`.

**Worked example: reading the login button.**

SauceDemo's login button is `<input type="submit" id="login-button" value="Login" data-test="login-button">`. Therefore:

```java
WebElement loginBtn = driver.findElement(By.id("login-button"));
System.out.println(loginBtn.getTagName());                 // input
System.out.println(loginBtn.getText());                    // (empty string)
System.out.println(loginBtn.getAttribute("value"));        // Login
System.out.println(loginBtn.getAttribute("type"));         // submit
System.out.println(loginBtn.getCssValue("background-color")); // an rgba(...) value
System.out.println(loginBtn.getSize());                    // (width, height)
```

Line by line: `getTagName()` returns `input` in lowercase regardless of how the HTML was written. `getText()` is empty because an `<input>` has no text content between tags (it is a void element with no closing tag). The label "Login" lives in the `value` attribute, so we read it with `getAttribute("value")`. `getSize()` prints a `Dimension` such as `(340, 49)`, meaning 340 pixels wide and 49 tall.

If the button had been written `<button>Login</button>`, then `getText()` would have returned `Login`. Rule of thumb: **`<input>` elements keep their label in `value`; `<button>`, `<a>`, `<p>`, `<span>`, `<h1>` and similar keep it as text.**

### 6. Checking Element State

```java
boolean visible  = element.isDisplayed();   // can the user see it?
boolean enabled  = element.isEnabled();     // can the user interact with it (not disabled)?
boolean selected = element.isSelected();    // is a checkbox/radio/option selected?
```

| Method | Applies to | Typical assertion |
|---|---|---|
| `isDisplayed()` | Any element | The success banner is displayed |
| `isEnabled()` | Buttons, inputs | The Submit button is disabled until the form is valid |
| `isSelected()` | Checkboxes, radio buttons, `<option>` | "Remember me" is ticked by default |

**Real-world uses.**

- A registration form must keep **Create account** disabled until all required fields are filled. Test: `assertFalse(createBtn.isEnabled())` first, fill the fields, then `assertTrue(createBtn.isEnabled())`.
- A settings page has "Email notifications" ticked by default. Test: `assertTrue(checkbox.isSelected())`.
- After a failed login, an error panel must appear. Test: `assertTrue(error.isDisplayed())`.

**Important edge cases.**

- `isDisplayed()` on an element that does not exist throws `NoSuchElementException` (because `findElement` failed first, before `isDisplayed` could even run). Combine with `findElements` when absence is possible.
- `isSelected()` on something that is not selectable (such as a `<div>`) simply returns `false`; it does not throw.
- `isEnabled()` only reports the HTML `disabled` state. A button that *looks* grey because of CSS but lacks the `disabled` attribute will report `true`.

### 7. First Interactions (Preview)

To use find methods in a realistic flow you need three basic actions. They are explored fully in **Tuesday's Element Interactions** lesson; here is just enough to be productive:

```java
element.sendKeys("text");   // type into an input
element.clear();            // erase an input's content
element.click();            // click a button, link, checkbox
element.submit();           // submit a form (legacy; clicking the button is preferred)
```

What each does, in one sentence:

- `sendKeys("text")` simulates a keyboard: it focuses the element and presses the keys one by one. It **appends** to whatever is already in the box.
- `clear()` empties a text box. Use it before `sendKeys` if the field may already contain text.
- `click()` simulates a real mouse click in the centre of the element.
- `submit()` submits the surrounding form. It is legacy; clicking the real Submit button behaves more like a user.

Tuesday explains what happens when an element cannot be clicked, how keyboard keys such as ENTER are sent, and much more. Today these three are enough.

### 8. Searching *Inside* an Element (Scoped Search)

**What and why.** `WebElement` also has `findElement` and `findElements`. They search **only the element's descendants** (elements nested inside it). This lets you narrow down ambiguous situations such as repeated cards.

Analogy: asking "where is the kitchen?" in the whole city gives many answers. Asking "where is the kitchen *in 12 Oak Street*?" gives one. The house is the scope.

```java
// 1. Find all product cards
List<WebElement> cards = driver.findElements(By.className("inventory_item"));

// 2. For each card, search inside it
for (WebElement card : cards) {
    String name  = card.findElement(By.className("inventory_item_name")).getText();
    String price = card.findElement(By.className("inventory_item_price")).getText();
    System.out.println(name + " -> " + price);
}
```

Line by line:

- `driver.findElements(By.className("inventory_item"))` returns six card elements; each one is a container holding a picture, a name, a description, a price, and a button.
- `for (WebElement card : cards)` is Java's enhanced `for` loop: on each pass, `card` holds the next element from the list.
- `card.findElement(By.className("inventory_item_name"))` searches only inside the current card, so it finds *that card's* name. Without the scope (`driver.findElement(...)`), you would receive the first product name on the page six times.
- `.getText()` converts the found element into the visible string.

**Important XPath detail:** inside a scoped search, an XPath that starts with `//` still searches the **whole document** unless you begin with a dot:

```java
card.findElement(By.xpath(".//button"));   // correct: relative to the card
card.findElement(By.xpath("//button"));    // WRONG: searches the entire page again
```

The `.` means "start from the current node", which is the card. Without it, `//` means "start from the document root". CSS selectors do not have this problem; `card.findElement(By.cssSelector("button"))` is always scoped.

**Scoped search with a chain.** You can also chain calls in one expression:

```java
String firstPrice = driver.findElement(By.id("inventory_container"))
                          .findElement(By.className("inventory_item_price"))
                          .getText();
```

Each `.findElement` runs on the result of the previous one. This is the same as finding the container first and storing it in a variable; the variable version is easier to debug because you can print each step.

**Finding one card by its content.** A very common real-world task: "click Add to cart for the product named Sauce Labs Backpack".

```java
for (WebElement card : driver.findElements(By.className("inventory_item"))) {
    String name = card.findElement(By.className("inventory_item_name")).getText();
    if (name.equals("Sauce Labs Backpack")) {
        card.findElement(By.tagName("button")).click();
        break;                               // stop looping once found
    }
}
```

The `break` leaves the loop immediately. Without it the loop would continue through the remaining cards for no reason. (Tomorrow and later in the week you will see more compact ways to do the same; the loop is the clearest way to understand it first.)

### 9. The `SearchContext` Idea

Both `WebDriver` and `WebElement` implement an interface called `SearchContext`, which defines `findElement` and `findElements`. That is why the same two methods exist in both places: "search in the whole page" versus "search in this part of the page".

You have met interfaces in Java: an interface is a promise that a class has certain methods. Here the promise is "I can be searched". It means any method that needs to search can accept a `SearchContext` parameter and work for both a whole page and a part of it:

```java
private String textOf(SearchContext scope, By locator) {
    return scope.findElement(locator).getText();
}
// textOf(driver, By.id("title"))           -> search the whole page
// textOf(card,   By.className("price"))    -> search inside one card
```

### 10. A Short Word on `StaleElementReferenceException`

You will meet this soon, so here is the idea. A `WebElement` is a remote control paired with an element in the DOM. If the page **reloads** or JavaScript **replaces** that part of the DOM, the old element no longer exists, and the remote is "stale".

```java
WebElement btn = driver.findElement(By.id("login-button"));
driver.navigate().refresh();
btn.click();   // StaleElementReferenceException: stale element reference: element is not attached to the page document
```

Fix: **find the element again** after anything that may rebuild the page. Do not keep `WebElement` variables across page changes. (In Wednesday's Page Object lessons you will see patterns that find elements fresh each time they are needed.)

---

## Code Example: Automating a Login and Reading the Inventory

```java
package com.revature.qea.find;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.util.List;

public class FindMethodsDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        try {
            driver.manage().window().maximize();
            driver.get("https://www.saucedemo.com");

            // --- findElement + interactions ---
            WebElement username = driver.findElement(By.id("user-name"));
            WebElement password = driver.findElement(By.id("password"));
            WebElement loginBtn = driver.findElement(By.id("login-button"));

            // --- reading element state / attributes before acting ---
            System.out.println("Username placeholder: " + username.getAttribute("placeholder"));
            System.out.println("Login button enabled? " + loginBtn.isEnabled());
            System.out.println("Login button text   : " + loginBtn.getAttribute("value")); // an <input>, so use value

            username.sendKeys("standard_user");
            password.sendKeys("secret_sauce");
            System.out.println("Typed username value: " + username.getAttribute("value"));
            loginBtn.click();

            // --- findElements: count and iterate ---
            List<WebElement> cards = driver.findElements(By.className("inventory_item"));
            System.out.println("Products on page: " + cards.size());

            for (WebElement card : cards) {
                String name  = card.findElement(By.className("inventory_item_name")).getText();
                String price = card.findElement(By.className("inventory_item_price")).getText();
                System.out.printf("%-35s %s%n", name, price);
            }

            // --- existence check without exceptions ---
            boolean errorPresent = !driver.findElements(By.cssSelector("[data-test='error']")).isEmpty();
            System.out.println("Error banner present? " + errorPresent);

            // --- what happens with findElement and a missing element? ---
            try {
                driver.findElement(By.id("this-id-does-not-exist"));
            } catch (org.openqa.selenium.NoSuchElementException e) {
                System.out.println("Caught NoSuchElementException as expected");
            }

            // --- CSS value and size ---
            WebElement firstBtn = cards.get(0).findElement(By.tagName("button"));
            System.out.println("First button color: " + firstBtn.getCssValue("color"));
            System.out.println("First button size : " + firstBtn.getSize());

        } finally {
            driver.quit();
        }
    }
}
```

**Explanation, block by block:**

- `package com.revature.qea.find;` places the class in a package folder. It must match the directory path under `src/test/java` (or `src/main/java`).
- The imports bring in the Selenium types (`By`, `WebDriver`, `WebElement`, `ChromeDriver`) and `java.util.List`. Forgetting `java.util.List` gives "cannot find symbol: class List".
- `WebDriver driver = new ChromeDriver();` opens Chrome. We declare the variable with the interface type `WebDriver` so that switching to Firefox later changes only this one line.
- `try { ... } finally { driver.quit(); }` guarantees the browser closes even if a line throws. Without it, a failed run leaves browser processes open in memory.
- `driver.get(...)` navigates and waits for the page `load` event (see Navigation Methods).
- The three `findElement` calls give back `WebElement` references. Nothing has been typed or clicked yet.
- `getAttribute("placeholder")` reads the grey hint text in the box (`Username`). `isEnabled()` should print `true`.
- The login button is an `<input type="submit" value="Login">`, so its label is in the `value` attribute and `getText()` would return an empty string. This illustrates the `getText()` versus `getAttribute("value")` difference.
- `sendKeys` types the credentials; the following `getAttribute("value")` proves what the box now contains (`standard_user`).
- `loginBtn.click()` submits the form; the browser navigates to the inventory page.
- `cards.size()` and the `for` loop show the list-returning method; scoped searches pull the name and price from the correct card each time (without them you would get the *first* name on the page repeatedly).
- The existence check uses `findElements(...).isEmpty()`, with no `try/catch` required. On a successful login, it prints `false`.
- The deliberately failing `findElement` shows the exception so you recognise it later. The `catch` names the Selenium exception by its full package path because `java.util.NoSuchElementException` also exists; writing the full name (or importing the Selenium one) avoids catching the wrong class.
- `System.out.printf("%-35s %s%n", name, price)` formats columns: `%-35s` left-aligns a string in 35 characters, `%s` prints the next string, and `%n` is a platform-safe newline.

**Expected output (abridged):**

```
Username placeholder: Username
Login button enabled? true
Login button text   : Login
Typed username value: standard_user
Products on page: 6
Sauce Labs Backpack                 $29.99
Sauce Labs Bike Light               $9.99
Sauce Labs Bolt T-Shirt             $15.99
Sauce Labs Fleece Jacket            $49.99
Sauce Labs Onesie                   $7.99
Test.allTheThings() T-Shirt (Red)   $15.99
Error banner present? false
Caught NoSuchElementException as expected
First button color: rgba(19, 35, 34, 1)
First button size : (..., ...)
```

The exact colour and size values depend on the site's current styling and your window size.

---

## Guided Lab: Login, Count, and Verify (25 minutes)

**Goal:** write a small class that logs in on SauceDemo with a wrong password, reads the error, then logs in correctly and verifies the product count, using only today's methods.

**Steps:**

1. In your Maven project (from the Project Setup lesson), create `src/test/java/com/revature/qea/find/FindLab.java` with a `main` method.
2. Create the driver in a `try/finally` as shown in the demo, and navigate to `https://www.saucedemo.com`.
3. Find the three login elements and store them in variables named `username`, `password`, and `loginBtn`.
4. Type `standard_user` and `wrong_password`, then click login.
5. Find the error banner with `By.cssSelector("[data-test='error']")`. Print its text with `getText()`. **Expected output:** `Epic sadface: Username and password do not match any user in this service`.
6. Check on the same page that `findElements(By.className("inventory_item"))` has size `0` (you are not logged in).
7. Re-find the password box (do not reuse a stale variable if the page changed), call `clear()`, type `secret_sauce`, and click login.
8. Count the cards with `findElements`. **Expected:** `6`.
9. Check that the error banner is now gone using the `isPresent` helper. **Expected:** `false`.
10. Print the name of the card whose price is `$7.99` by looping over cards with scoped searches.

**Solution sketch for steps 7 to 10:**

```java
WebElement pwd = driver.findElement(By.id("password"));
pwd.clear();
pwd.sendKeys("secret_sauce");
driver.findElement(By.id("login-button")).click();

List<WebElement> cards = driver.findElements(By.className("inventory_item"));
System.out.println("Cards: " + cards.size());                         // 6
System.out.println("Error present: "
        + !driver.findElements(By.cssSelector("[data-test='error']")).isEmpty()); // false

for (WebElement card : cards) {
    if (card.findElement(By.className("inventory_item_price")).getText().equals("$7.99")) {
        System.out.println("Cheapest: " + card.findElement(By.className("inventory_item_name")).getText());
    }
}
```

**If something fails:** read the exception name first. `NoSuchElementException` means a locator did not match (check the URL and spelling). `IndexOutOfBoundsException` means a list was shorter than expected. `StaleElementReferenceException` means you reused an element after the page changed.

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Using `findElement` to check that something is absent | Exception instead of `false` | Use `findElements(...).isEmpty()` |
| Calling `getText()` on an `<input>` and getting `""` | Confusion | Use `getAttribute("value")` |
| Scoped XPath starting with `//` | Searches the whole page | Start with `.//` |
| Storing a `WebElement` and using it after navigating | `StaleElementReferenceException` | Re-find after page changes |
| Locator matches several elements; test uses the first | Wrong element | Refine the locator, then verify in DevTools |
| Assuming `findElements` waits for elements | Returns an empty list immediately | Use waits (Tuesday) when content loads late |
| Confusing "present" and "displayed" | Assertion on hidden element | Use `isDisplayed()` for visibility |
| Calling `list.get(0)` without checking the list | `IndexOutOfBoundsException` | Check `isEmpty()` or `size()` first |
| Catching `java.util.NoSuchElementException` by accident | The Selenium exception is not caught | Import or fully qualify `org.openqa.selenium.NoSuchElementException` |
| Comparing `getCssValue("color")` to `"red"` | Always false | Compare with `rgba(255, 0, 0, 1)` |

---

## Practice Exercises

1. **Login and verify.** Automate the SauceDemo login. After clicking, use `findElements` to verify that the product list contains exactly **6** items.
2. **Negative login.** Log in with a wrong password and read the text of the error message element (`[data-test='error']`). Print it. Then use `findElements` to confirm that **no** error element exists on a successful login.
3. **Product report.** Print every product's name and price, then compute and print the **cheapest** product (parse the price by removing the `$` character and using `Double.parseDouble`).
4. **Attribute detective.** For the username input print: the tag name, the `type` attribute, the `placeholder`, the `id`, and the CSS `font-size`.
5. **State checks.** Open `https://the-internet.herokuapp.com/checkboxes`. Print `isSelected()` for both checkboxes, click the first, and print again.
6. **Scoped vs. global.** On the inventory page, write both `card.findElement(By.xpath("//button"))` and `card.findElement(By.xpath(".//button"))` inside a loop over cards and print each button's text. Explain the difference in results.
7. **Explain the exception.** Write down, in your own words, three different reasons you could get a `NoSuchElementException` for a locator you believe is correct.
8. **Helper method.** Write `isPresent(WebDriver, By)` and `isVisible(WebDriver, By)` as `static` methods in a class `ElementUtil`. Test both on the login page for an existing id and a missing id.
9. **Find by text.** On the inventory page, write a method `clickAddToCart(WebDriver driver, String productName)` that finds the right card by name and clicks its button. Call it for "Sauce Labs Onesie". Verify the cart badge (`.shopping_cart_badge`) shows `1`.
10. **Disabled state.** Open `https://the-internet.herokuapp.com/dynamic_controls`. Find the text input in the second section and print `isEnabled()`. (Do not click anything yet; the "Enable" button's behaviour involves waiting, which is Tuesday's topic.)
11. **Value vs. text.** On `https://the-internet.herokuapp.com/inputs`, type `42` into the number input, then print `getText()` and `getAttribute("value")`. Explain why they differ.

---

## Solutions and Hints

**1.** After login: `List<WebElement> items = driver.findElements(By.className("inventory_item"));` then `System.out.println(items.size() == 6 ? "PASS" : "FAIL");`. Hint: remember `import java.util.List;`.

**2.** Wrong password flow, then:

```java
String msg = driver.findElement(By.cssSelector("[data-test='error']")).getText();
System.out.println(msg);
```

On a successful run, `driver.findElements(By.cssSelector("[data-test='error']")).isEmpty()` is `true`.

**3.**

```java
double cheapest = Double.MAX_VALUE;
String cheapestName = "";
for (WebElement card : driver.findElements(By.className("inventory_item"))) {
    String name = card.findElement(By.className("inventory_item_name")).getText();
    double price = Double.parseDouble(
            card.findElement(By.className("inventory_item_price")).getText().replace("$", ""));
    System.out.println(name + " " + price);
    if (price < cheapest) { cheapest = price; cheapestName = name; }
}
System.out.println("Cheapest: " + cheapestName + " at " + cheapest);
```

Expected cheapest: Sauce Labs Onesie at 7.99.

**4.**

```java
WebElement u = driver.findElement(By.id("user-name"));
System.out.println(u.getTagName());               // input
System.out.println(u.getAttribute("type"));       // text
System.out.println(u.getAttribute("placeholder")); // Username
System.out.println(u.getAttribute("id"));         // user-name
System.out.println(u.getCssValue("font-size"));   // e.g. 14px
```

**5.**

```java
List<WebElement> boxes = driver.findElements(By.cssSelector("#checkboxes input"));
System.out.println(boxes.get(0).isSelected() + " " + boxes.get(1).isSelected()); // false true
boxes.get(0).click();
System.out.println(boxes.get(0).isSelected());   // true
```

**6.** With `//button`, each loop iteration returns the **first button on the whole page** (the same one every time, often the first product's button or the menu button), because the search ignores the card. With `.//button`, each iteration returns that card's own button. Hint: print the button text in both versions and compare.

**7.** Any three of: typo or wrong locator; element not loaded yet (timing); element inside an iframe; element in another window/tab; wrong page because an earlier step failed; the application is actually broken.

**8.**

```java
public final class ElementUtil {
    private ElementUtil() { }

    public static boolean isPresent(WebDriver driver, By locator) {
        return !driver.findElements(locator).isEmpty();
    }

    public static boolean isVisible(WebDriver driver, By locator) {
        List<WebElement> found = driver.findElements(locator);
        return !found.isEmpty() && found.get(0).isDisplayed();
    }
}
```

**9.**

```java
static void clickAddToCart(WebDriver driver, String productName) {
    for (WebElement card : driver.findElements(By.className("inventory_item"))) {
        String name = card.findElement(By.className("inventory_item_name")).getText();
        if (name.equals(productName)) {
            card.findElement(By.tagName("button")).click();
            return;
        }
    }
    throw new IllegalArgumentException("Product not found: " + productName);
}
```

Throwing an exception when nothing matches makes the test fail clearly rather than silently doing nothing. Then `driver.findElement(By.className("shopping_cart_badge")).getText()` should be `1`.

**10.** The input is initially disabled, so `isEnabled()` prints `false`. Hint: select it with `By.cssSelector("#input-example input")`.

**11.** `getText()` returns an empty string because the typed number is the element's *value*, not text between tags. `getAttribute("value")` returns `42`.

---

## Self-Check Questions

**Q1. What does `findElements` return if nothing matches?**
An empty list. It never throws `NoSuchElementException`.

**Q2. You have three buttons with class `btn`. What does `driver.findElement(By.className("btn"))` return?**
The first one in document order, silently. No error or warning.

**Q3. Why does `getText()` return an empty string for a login button written as `<input value="Login">`?**
An `<input>` has no text content; its label is stored in the `value` attribute. Use `getAttribute("value")`.

**Q4. What is the difference between present and displayed?**
Present means the element exists in the DOM. Displayed means it exists and is visible to a user.

**Q5. Why should a scoped XPath start with `.//`?**
`//` searches from the document root even inside an element search. The leading dot makes the search start from the current element.

**Q6. What causes `StaleElementReferenceException` and how do you fix it?**
The page or DOM section was rebuilt after you found the element, so your reference points to something that no longer exists. Find the element again.

**Q7. Which method would you use to check that an error banner does not appear, and why?**
`findElements(...).isEmpty()`, because absence is an expected outcome and should return `true` rather than throw.

**Q8. Both `WebDriver` and `WebElement` have `findElement`. What do they share?**
The `SearchContext` interface; one searches the whole page, the other only the element's descendants.

---

## Summary

- `findElement(By)` returns the **first** matching `WebElement` or throws `NoSuchElementException`; `findElements(By)` returns a **list** (possibly empty) and never throws for "not found".
- Use `findElements(...).isEmpty()` to check whether an element exists.
- A `WebElement` can tell you its **text** (`getText()`), **attributes/properties** (`getAttribute`, `getDomProperty`), **CSS values**, **size**, and **state** (`isDisplayed`, `isEnabled`, `isSelected`).
- `getText()` returns only visible text; for input boxes use the `value` attribute.
- Elements can be searched **within** other elements; in XPath, begin scoped searches with `.//`.
- A `WebElement` is a reference, not a copy; after the page changes, re-find it to avoid `StaleElementReferenceException`.
- `click()`, `sendKeys()`, and `clear()` are enough for a first login automation; element interactions are covered in depth on Tuesday, and timing problems with waits on Tuesday as well.
- In Project 2 these calls will be wrapped in reusable helper methods inside your base page class.

---

## Additional Resources

- Selenium documentation, *Finding web elements*: https://www.selenium.dev/documentation/webdriver/elements/finders/
- Selenium documentation, *Information about web elements*: https://www.selenium.dev/documentation/webdriver/elements/information/
- Selenium Java API docs, `WebElement` interface: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebElement.html
