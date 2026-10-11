# Locator Strategies

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a locator is and why choosing the right one decides whether your tests are stable or fragile.
- Describe the DOM as a tree and read basic HTML to identify the best attribute to target.
- Use all eight Selenium `By` strategies: `id`, `name`, `className`, `tagName`, `linkText`, `partialLinkText`, `cssSelector`, and `xpath`.
- Write CSS selectors (tag, id, class, attribute, partial-match, child/descendant, sibling, `nth-child`, `:not`).
- Write XPath expressions (absolute vs. relative, attributes, `contains()`, `text()`, `starts-with()`, `and`/`or`, indexes, axes such as `parent`, `ancestor` and `following-sibling`) and read them piece by piece.
- Use browser DevTools to inspect elements and test locators before writing code.
- Apply a priority order for locator choice, refactor a fragile locator into a robust one, and avoid common mistakes.
- Diagnose `NoSuchElementException` and `InvalidSelectorException` caused by locator problems.

---

## Why This Matters

Every Selenium action starts with the same question: **"Which element on the page do I mean?"** A test cannot click a button until it can unambiguously point to it. Locators are how we point.

In practice, most flaky and high-maintenance test suites are not caused by Selenium. They are caused by weak locators, for example:

```java
// Fragile: breaks when a designer adds one <div> above the button
By.xpath("/html/body/div[2]/div[1]/form/div[3]/button")
```

versus a robust one:

```java
By.id("login-button")
```

Teams that spend half of every sprint repairing broken tests usually have a locator problem. In **Project 2** you will build a framework other people maintain; stable locators are what make it maintainable. Today you learn all the strategies and, just as importantly, which to prefer.

### A tester's story

Maya joins a project that has 300 automated tests. On her first Monday the nightly run shows 85 failures. The developers shipped a redesign: nothing a user would call broken, but a wrapper `<div>` was added around the page content. All 85 failing tests used absolute XPaths copied from DevTools. Two weeks of her sprint go on repairing locators. A senior engineer then rewrites the 85 locators using `id` and `data-test` attributes. At the next redesign, three tests fail instead of 85.

Same tests, same application, same Selenium. The only difference is the quality of the locators. This lesson is about writing locators that survive a redesign.

### How this connects to what you know

- *Architecture lesson:* when you call `driver.findElement(By.id("x"))`, the client library sends `POST /session/{id}/element` with a *strategy* and a *value*. The `By` class is simply the object that carries those two pieces of information.
- *Earlier web basics:* HTML tags, attributes and nesting. We refresh them below, because locators are built from them.

---

## The Concept

### 1. What Is a Locator?

A **locator** describes *how to find an element* in the page's DOM (Document Object Model, the browser's tree representation of the HTML). In Selenium Java, a locator is an object of type `By`:

```java
By loginButton = By.id("login-button");
WebElement element = driver.findElement(loginButton);   // finding methods are covered in the next lessons
```

**Line by line:**

- `By` is a class in `org.openqa.selenium`. It is a *description*, not a search. Creating a `By` does not contact the browser at all.
- `By.id("login-button")` is a *static factory method*: it returns a `By` object that means "the element whose id is `login-button`".
- `driver.findElement(loginButton)` is the moment the search actually happens. The browser looks through the page and returns a `WebElement` reference (remember the "luggage ticket" from the architecture lesson), or Selenium throws `NoSuchElementException` if there is no match.

In this lesson we focus on *building* `By` objects. The next lessons (*Navigation*, *Find Methods*) show how to use them in `findElement` and `findElements`.

> **Analogy:** a locator is an address. `By.id` is like a unique national ID number: one person, no ambiguity. `By.className` is like "a person who wears a red hat": many people may match. `By.xpath("/html/body/div[2]/...")` is like directions "go down the street, take the second left, third door": it works until the town builds a new street.

**Why are there eight strategies?** Web pages differ. Some elements have unique IDs, some only have visible text, some can only be reached through their relationship to a neighbour. Selenium gives you eight tools so that you can pick the clearest one for each situation.

### 2. A Quick HTML Refresher

Locators rely on HTML structure. Consider this simplified SauceDemo login form:

```html
<form>
  <div class="form_group">
    <input class="input_error form_input" placeholder="Username" type="text"
           data-test="username" id="user-name" name="user-name" autocorrect="off">
  </div>
  <div class="form_group">
    <input class="input_error form_input" placeholder="Password" type="password"
           data-test="password" id="password" name="password">
  </div>
  <input type="submit" class="submit-button btn_action" data-test="login-button"
         id="login-button" name="login-button" value="Login">
</form>
<a href="https://saucelabs.com/">Sauce Labs</a>
```

Vocabulary:

- **Tag:** `input`, `div`, `form`, `a`.
- **Attribute:** `id="user-name"`, `class="form_input"`, `type="text"`. An attribute is a `name="value"` pair written inside the opening tag.
- **Text content:** the visible text between tags, for example `Sauce Labs`.
- **Parent / child / sibling:** the nesting relationships. `input` is a child of `div`; the two `div`s are siblings.

**The DOM as a tree.** The browser reads the HTML and builds a family tree. The example above becomes:

```
form
 ├── div.form_group
 │     └── input#user-name
 ├── div.form_group
 │     └── input#password
 └── input#login-button
a (sibling of form)
```

Every locator strategy is just a different way to describe a position or characteristic in this tree: "the node with this id", "any node of this tag", "the node under this parent whose text is X".

**Reading attributes with an eye for stability.** When you look at an element, ask of each attribute: *could this value change without anyone changing what the element does?*

| Attribute in the example | Stable? | Reasoning |
|---|---|---|
| `id="login-button"` | Yes | Purposeful name, set by developers |
| `data-test="login-button"` | Very | Exists only for testing |
| `name="login-button"` | Yes | Used for form submission |
| `class="submit-button btn_action"` | Medium | Styling names, may change in a restyle |
| `value="Login"` | Medium | Visible label, may be reworded or translated |
| `placeholder="Username"` | Medium | Visible hint, may be reworded |
| Position (third child of `form`) | Low | Changes when layout changes |

### 3. The Eight `By` Strategies

#### 3.1 `By.id`

```java
driver.findElement(By.id("user-name"));
```

- Matches the element whose `id` attribute equals the value.
- IDs are meant to be **unique** on a page, so this is the fastest and clearest locator.
- **Caution:** some frameworks generate dynamic IDs such as `id="input_83719"` that change on every page load. If an ID looks random or contains long numbers, do not rely on it.
- **When to use:** always check for an `id` first.
- **When not to:** when the ID is generated, or when two elements on the page wrongly share it (invalid HTML, but it happens; you get the first).

What happens if there is no such element: Selenium throws

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: {"method":"css selector","selector":"[id="user-nam"]"}
```

Read this message carefully: it shows the *strategy* and *selector* Selenium sent, so a typo like `user-nam` is easy to spot. (Selenium 4 typically translates `id`, `name` and `className` into CSS selectors before sending them; this is why the message says "css selector".)

#### 3.2 `By.name`

```java
driver.findElement(By.name("password"));
```

- Matches the `name` attribute. Common on form fields.
- Names are *often* but *not always* unique (radio buttons in the same group share a name).
- **When to use:** form inputs when no `id` exists. A group of radio buttons with the same name is a legitimate use of `findElements(By.name("size"))`.

#### 3.3 `By.className`

```java
driver.findElement(By.className("submit-button"));
```

- Matches **one** CSS class name.
- **Does not accept multiple classes or spaces**. `By.className("submit-button btn_action")` throws an `InvalidSelectorException`. To use two classes, use CSS: `By.cssSelector(".submit-button.btn_action")`.
- Classes are mainly for styling and are shared by many elements, so the first match may not be the one you want.
- **When to use:** when a class is meaningful and unique (for example `login_logo`), or with `findElements` to collect a family of similar elements (all `inventory_item_name` elements on the product page).

A real example: on the SauceDemo inventory page, `By.className("inventory_item_name")` matches six product titles, one per product. With `findElement` you get the first (Sauce Labs Backpack); with `findElements` you get all six.

#### 3.4 `By.tagName`

```java
List<WebElement> links = driver.findElements(By.tagName("a"));
```

- Matches elements by HTML tag. Rarely unique, so it is typically used with `findElements` to count or iterate (for example, all links, all images, all table rows).
- **When to use:** collecting things: "how many images are broken?", "list all link addresses", "are there exactly five rows?".

#### 3.5 `By.linkText`

```java
driver.findElement(By.linkText("Sauce Labs"));
```

- Works **only on `<a>` (link) elements**.
- Matches the **complete visible text exactly** (case-sensitive; extra spaces matter).
- Breaks if the wording or language changes.
- **When to use:** navigation menus and footers in simple pages, for example the example links on `https://the-internet.herokuapp.com`, such as `By.linkText("Checkboxes")`.

#### 3.6 `By.partialLinkText`

```java
driver.findElement(By.partialLinkText("Sauce"));
```

- Like `linkText` but matches a **substring**. If several links contain the substring, you get the first one, so be specific.
- **When to use:** when the link text includes changing parts, for example `By.partialLinkText("Order #")` for links whose full text is `Order #5821`.

**Quick comparison of the simple strategies on one page.** Suppose a page has `<a id="home" class="nav" href="/">Home</a>`:

| Locator | Matches? |
|---|---|
| `By.id("home")` | Yes |
| `By.className("nav")` | Yes (if it is the first `nav` element) |
| `By.tagName("a")` | Yes (if it is the first link) |
| `By.linkText("Home")` | Yes |
| `By.linkText("home")` | No (case-sensitive) |
| `By.partialLinkText("Hom")` | Yes |

---

#### 3.7 `By.cssSelector`

CSS selectors are the same patterns web developers use to style pages. They are powerful, fast, and readable.

| Goal | CSS selector | Example in Java |
|---|---|---|
| By tag | `input` | `By.cssSelector("input")` |
| By id | `#user-name` | `By.cssSelector("#user-name")` |
| By class | `.submit-button` | `By.cssSelector(".submit-button")` |
| Tag + class | `input.submit-button` | `By.cssSelector("input.submit-button")` |
| Multiple classes | `.submit-button.btn_action` | `By.cssSelector(".submit-button.btn_action")` |
| By attribute | `[data-test='username']` | `By.cssSelector("[data-test='username']")` |
| Tag + attribute | `input[type='password']` | `By.cssSelector("input[type='password']")` |
| Attribute **starts with** | `input[id^='user']` | `By.cssSelector("input[id^='user']")` |
| Attribute **ends with** | `input[id$='name']` | `By.cssSelector("input[id$='name']")` |
| Attribute **contains** | `input[id*='ser-na']` | `By.cssSelector("input[id*='ser-na']")` |
| Direct child | `form > div` | `By.cssSelector("form > div")` |
| Descendant | `form input` | `By.cssSelector("form input")` |
| nth child | `div.form_group:nth-child(2) input` | `By.cssSelector("div.form_group:nth-child(2) input")` |

Remember: in Java strings, use single quotes inside CSS attribute values so you do not need to escape double quotes: `"[data-test='username']"`.

> **Why `data-test` attributes are gold:** Many teams add attributes such as `data-test`, `data-testid`, or `data-qa` to elements *specifically for automation*. They never change for styling reasons, so they are the most stable locators. If your application is under your team's control, ask developers to add them.

**Reading a CSS selector piece by piece.** Take `form > div.form_group:nth-child(2) input[type='password']`:

1. `form` : start at any `<form>`.
2. `>` : go to a **direct child** (one level down only).
3. `div.form_group` : the child must be a `<div>` with class `form_group`.
4. `:nth-child(2)` : and it must be the *second* child of its parent.
5. (a space) : now look at **any descendant** (any depth below).
6. `input[type='password']` : an `<input>` whose `type` attribute is `password`.

Read left to right, each part narrows the search. That is how every CSS (and XPath) expression works: *start wide, narrow step by step*.

**More CSS you will need:**

| Goal | CSS selector | Notes |
|---|---|---|
| Next sibling immediately after | `label + input` | The input right after a label |
| Any later sibling | `h2 ~ p` | All paragraphs after an `h2` at the same level |
| First / last child | `ul > li:first-child`, `ul > li:last-child` | Position-based, use sparingly |
| nth of that tag | `tr:nth-of-type(3)` | Counts only `tr` siblings |
| Exclude something | `input:not([type='hidden'])` | Everything except hidden inputs |
| Several alternatives | `#user-name, #password` | Comma means OR; returns elements matching either |
| Attribute exists | `[disabled]` | No value required |
| Case-insensitive value | `[data-test='Login' i]` | The `i` flag ignores case |

**What CSS cannot do:** CSS selectors cannot match on an element's visible **text** (there is no `:contains()` in real CSS, even though some older tutorials show one), and they have no general "go to parent" operator (`:has()` exists in modern browsers but is not something to depend on in a test framework). For those needs, use XPath.

**Special characters.** If an id contains characters that are special in CSS, such as `.` or `:` (for example `id="user.name"`), `By.cssSelector("#user.name")` means "id `user` with class `name`". Use the attribute form instead: `By.cssSelector("[id='user.name']")`, or simply `By.id("user.name")`.

#### 3.8 `By.xpath`

XPath is a query language for navigating XML/HTML trees. It can do things CSS cannot: select by **visible text**, travel **up** to a parent, or follow siblings.

**Absolute vs. relative XPath**

```text
Absolute:  /html/body/div/div/form/div[1]/input     (starts at the root; breaks on any structural change)
Relative:  //input[@id='user-name']                  (starts anywhere with //; much more robust)
```

**Always prefer relative XPath.** Browser DevTools can generate absolute XPaths ("Copy full XPath"), which are fragile; never use them as-is.

**Core syntax:** `//tagname[@attribute='value']`

| Goal | XPath |
|---|---|
| Any element with an attribute | `//*[@id='user-name']` |
| Tag + attribute | `//input[@type='password']` |
| Two attributes (AND) | `//input[@type='text' and @name='user-name']` |
| Either attribute (OR) | `//input[@id='user-name' or @name='username']` |
| Attribute contains | `//input[contains(@class,'form_input')]` |
| Attribute starts with | `//input[starts-with(@id,'user')]` |
| By exact visible text | `//a[text()='Sauce Labs']` |
| By partial visible text | `//a[contains(text(),'Sauce')]` or `//a[contains(.,'Sauce')]` |
| Normalized whitespace | `//button[normalize-space()='Add to cart']` |
| By position (1-based) | `(//input)[2]` |
| Parent of an element | `//input[@id='user-name']/..` or `/parent::div` |
| Following sibling | `//label[text()='Username']/following-sibling::input` |
| Preceding sibling | `//input[@id='password']/preceding-sibling::input` |
| Ancestor | `//input[@id='user-name']/ancestor::form` |
| Child by position | `//form/div[2]/input` |

Notes:

- `*` means "any tag".
- XPath indexes start at **1**, not 0.
- `text()` matches the element's own text node; `.` matches the combined text of the element and descendants. If `text()` fails on an element with nested tags, try `contains(.,'...')`.
- XPath is a little slower than CSS in some browsers but the difference is rarely noticeable.

**Reading an XPath piece by piece.** Take `//div[text()='Sauce Labs Backpack']/ancestor::div[@class='inventory_item']//button`:

1. `//div` : anywhere in the page, a `<div>`...
2. `[text()='Sauce Labs Backpack']` : ...whose own text is exactly "Sauce Labs Backpack". Square brackets are a *filter* (a condition).
3. `/ancestor::div[@class='inventory_item']` : from that div, climb **up** to the ancestor `<div>` whose class is `inventory_item` (the product card).
4. `//button` : from that card, go **down** to any `<button>` inside it.

The result is "the button that belongs to the Backpack card", no matter where in the list the Backpack sits.

**Axes in XPath: a travel guide.** An *axis* tells XPath which direction to travel from the current element.

| Axis | Direction | Example |
|---|---|---|
| `child::` (or `/`) | Direct children | `//form/input` |
| `descendant::` (or `//`) | Any depth below | `//form//input` |
| `parent::` (or `..`) | One level up | `//input[@id='password']/..` |
| `ancestor::` | All levels up | `//input/ancestor::form` |
| `following-sibling::` | Later siblings, same parent | `//label[.='Username']/following-sibling::input` |
| `preceding-sibling::` | Earlier siblings, same parent | `//input[@id='password']/preceding-sibling::input` |

**Case study: a data table.** On `https://the-internet.herokuapp.com/tables` the first table (`id="table1"`) lists people with columns for last name, first name, email, due and actions. To click the "edit" link on the row whose last name is `Smith`:

```java
By editSmith = By.xpath("//table[@id='table1']//td[text()='Smith']/following-sibling::td//a[text()='edit']");
```

Reading: find the table by id, go to any `td` whose text is `Smith`, move to its following sibling cells, and in them find the link with text `edit`. The row position does not matter: if the data is re-sorted the locator still works. This "anchor on stable data, then move sideways" pattern is the most valuable XPath skill in tables and lists. (Verify the exact markup in DevTools; sites can change.)

**Quoting text that contains an apostrophe.** If the text is `Women's Shirt`, you cannot write `text()='Women's Shirt'`. Wrap the XPath value in double quotes and escape them in Java: `By.xpath("//a[text()=\"Women's Shirt\"]")`. Or avoid the issue with `contains(text(),'Shirt')`.

### 4. Comparing the Strategies

| Strategy | Speed | Typical stability | Readability | Notes |
|---|---|---|---|---|
| `id` | Fastest | High (if not dynamic) | Excellent | First choice |
| `name` | Fast | Medium–High | Good | Good for forms |
| `className` | Fast | Medium | Good | One class only; often non-unique |
| `tagName` | Fast | Low (non-unique) | Good | For collections |
| `linkText` / `partialLinkText` | Fast | Medium | Excellent | Links only; text can change |
| `cssSelector` | Fast | High (if attribute-based) | Good | Best all-rounder |
| `xpath` | Medium | Varies | Medium | Most powerful; needed for text/parent traversal |

**CSS vs. XPath at a glance:**

| Need | CSS | XPath |
|---|---|---|
| Match by attribute | Yes | Yes |
| Match by visible text | No | Yes |
| Go up to a parent | No (practically) | Yes |
| Follow a sibling | Yes (forward only) | Yes (forward and backward) |
| Readability for simple cases | Better | Longer |

### 5. Recommended Priority Order

When inspecting an element, ask these questions in order:

1. Does it have a **stable, unique `id`** or a **test attribute** (`data-test`)? → use it.
2. Does it have a unique **`name`**? → use it.
3. Can a short **CSS selector** with meaningful attributes identify it? → use CSS.
4. Do you need to search by **visible text** or navigate to a **parent/sibling**? → use **relative XPath**.
5. Last resort: positional locators (`[3]`, `nth-child`), which break easily when the layout changes.

**Avoid:**

- Absolute XPath.
- Auto-generated class names (for example `css-1x2y3z`) and numeric/random IDs.
- Long chains copied from DevTools.
- Locators based on text that gets translated or changed by marketing.

#### Worked example: improving a locator step by step

Starting point, copied from DevTools ("Copy full XPath") for the SauceDemo login button:

```text
/html/body/div/div/div[2]/div[1]/div/div/form/input
```

| Version | Locator | Problem |
|---|---|---|
| v1 | `/html/body/div/div/div[2]/div[1]/div/div/form/input` | Breaks if any wrapper is added; unreadable |
| v2 | `//form/input` | Matches several inputs; ambiguous (the first is the username box) |
| v3 | `//input[@type='submit']` | Better, but any other submit input would also match |
| v4 | `//input[@value='Login']` | Depends on visible label; breaks if reworded |
| v5 | `//input[@id='login-button']` | Stable and unique |
| v6 | `By.id("login-button")` | Same meaning, shorter, fastest |

Each step trades length for stability. The final answer is the simplest one that is still unique.

#### Real-world decision flow

```
Element has id? (and it is not random) ----------- yes --> By.id
        | no
Element has data-test / data-testid / data-qa? --- yes --> By.cssSelector("[data-test='x']")
        | no
Form field with unique name? --------------------- yes --> By.name
        | no
Can class/attribute combos make it unique? ------- yes --> By.cssSelector
        | no
Need text or a parent/sibling relationship? ------ yes --> relative By.xpath
        | no
Ask developers to add an id or data-test attribute.
```

The last line is not a joke. Asking the developers for a stable attribute (a two-minute change for them) is often the best fix, and it is normal teamwork in quality engineering.

### 6. Using DevTools to Find and Test Locators

1. Open the page in Chrome. Right-click the element → **Inspect** (or press `F12`).
2. The **Elements** panel highlights the HTML. Read its attributes.
3. Press `Ctrl+F` inside the Elements panel. This search box accepts **text, CSS selectors, and XPath**. Type a candidate locator, such as `#user-name` or `//input[@name='password']`, and Chrome shows **"1 of 1"** when it matches exactly one element. If it says "0 of 0" it matches nothing; "1 of 5" means it is not unique.
4. In the **Console** you can also test:

```javascript
$$("input[type='password']")          // CSS: returns all matches
$x("//input[@type='password']")       // XPath: returns all matches
```

Always verify that your locator matches **exactly one** element (unless you deliberately want a list) *before* putting it in code. This habit saves hours.

**A DevTools walk-through, click by click**, on `https://www.saucedemo.com`:

1. Right-click inside the Username box and choose **Inspect**. The Elements panel opens with the `<input ... id="user-name">` line selected.
2. Read the attributes: `id`, `name`, `data-test`, `class`. Note that `id` and `data-test` both look purposeful.
3. Click into the Elements panel and press `Ctrl+F` (`Cmd+F` on macOS). Type `#user-name`. The counter shows `1 of 1`. Good.
4. Now type `.form_input`. The counter shows `1 of 2`, because the password box shares the class. This is a live demonstration of why classes are poor unique locators.
5. Type `//input`. You will see several matches, so `//input` alone is not usable.
6. Open the **Console** tab, type `$x("//input[@id='user-name']").length` and press Enter. The answer `1` confirms uniqueness a second way.

**Caution about DevTools:** DevTools shows the DOM *after* JavaScript has run, which is what Selenium sees too. It differs from "View page source", which shows the original HTML. Elements created by JavaScript appear in DevTools but not in page source. Always test locators in DevTools, not in page source.

### 7. Storing Locators: Keep Them Out of the Middle of Your Logic

Beginners often scatter strings throughout test steps. Better, declare them once:

```java
public class LoginLocators {
    static final By USERNAME   = By.id("user-name");
    static final By PASSWORD   = By.id("password");
    static final By LOGIN_BTN  = By.id("login-button");
    static final By ERROR_MSG  = By.cssSelector("[data-test='error']");
}
```

Now a change to the page is fixed in one place. On **Wednesday** you will formalize this idea into the *Page Object Model*; today we only practice the discipline of naming locators.

**Why `static final`?** `static` means one copy shared by the whole class (no object needed). `final` means the variable cannot be reassigned. The upper-case names are the Java convention for constants. Creating a `By` object is cheap and has no side effects, so holding it in a constant is safe.

### 8. A Glimpse of Selenium 4 Relative Locators

Selenium 4 added *relative locators* that describe an element by its position relative to another, in plain words. For example, "the input below the Username label":

```java
import static org.openqa.selenium.support.locators.RelativeLocator.with;

WebElement field = driver.findElement(
        with(By.tagName("input")).below(By.id("some-label")));
```

Other helpers include `above`, `toLeftOf`, `toRightOf` and `near`. They are handy when a page has no usable attributes but a clear visual layout. Treat them as a supplement: they depend on how the page is *drawn*, so a responsive layout change can alter the result. Prefer the strategies above.

---

## Code Example: Locating Elements on the SauceDemo Login Page

```java
package com.revature.qea.locators;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.util.List;

public class LocatorDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        try {
            driver.get("https://www.saucedemo.com");

            // 1. id
            WebElement username = driver.findElement(By.id("user-name"));

            // 2. name
            WebElement password = driver.findElement(By.name("password"));

            // 3. cssSelector using a test attribute (most stable here)
            WebElement loginBtn = driver.findElement(By.cssSelector("[data-test='login-button']"));

            // 4. xpath with two attributes
            WebElement usernameViaXpath =
                driver.findElement(By.xpath("//input[@type='text' and @name='user-name']"));

            // 5. tagName: count all inputs
            List<WebElement> inputs = driver.findElements(By.tagName("input"));
            System.out.println("Number of <input> elements: " + inputs.size());

            // 6. className
            WebElement logo = driver.findElement(By.className("login_logo"));
            System.out.println("Logo text: " + logo.getText());

            // Use the elements: typing and clicking are covered in depth Tuesday;
            // here we only need a taste of them.
            username.sendKeys("standard_user");
            password.sendKeys("secret_sauce");
            loginBtn.click();

            // 7. After login, find a product by visible text with XPath
            WebElement backpack =
                driver.findElement(By.xpath("//div[text()='Sauce Labs Backpack']"));
            System.out.println("Found product: " + backpack.getText());

            // 8. XPath relationship: the Add to cart button inside the same product card
            WebElement addBackpack = driver.findElement(
                By.xpath("//div[text()='Sauce Labs Backpack']"
                       + "/ancestor::div[@class='inventory_item']//button"));
            System.out.println("Button label: " + addBackpack.getText());

        } finally {
            driver.quit();
        }
    }
}
```

**Explanation of the interesting parts:**

- `By.cssSelector("[data-test='login-button']")` uses an attribute purpose-built for tests.
- The XPath with `and` shows combining two conditions to narrow to a unique element.
- `findElements(By.tagName("input"))` returns a `List<WebElement>`; `size()` tells us how many matched. (`findElement` vs. `findElements` is the next lessons' topic.)
- The final XPath starts at the product *name*, climbs **up** to its card with `ancestor::`, then goes **down** to that card's button with `//button`. This is the classic way to click the right button in a repeated list, something CSS cannot do easily.

**What happens when each line runs:**

| Line | Result |
|---|---|
| `driver.get(...)` | Browser loads the login page |
| `findElement(By.id("user-name"))` | One request, returns a reference to the Username box |
| `findElements(By.tagName("input"))` | One request, returns a list (three entries on the login page: username, password, login button) |
| `logo.getText()` | Returns the visible text, `Swag Labs` |
| `sendKeys`, `click` | Type into the fields and press Login; the page changes to the inventory |
| Second XPath | Finds the product name, then the card, then the card's button, whose text is `Add to cart` |

**Expected console output:**

```
Number of <input> elements: 3
Logo text: Swag Labs
Found product: Sauce Labs Backpack
Button label: Add to cart
```

(If the site's markup changes, counts or text may differ; that is a good reminder that locators depend on the page.)

**A note on timing.** The code above works because the page has finished loading by the time each command runs. On pages that change after loading, a locator can fail simply because the element is not there *yet*. That is a timing problem, not a locator problem, and it is solved with waits on **Tuesday**.

---

## Troubleshooting Locators

### Walk-through 1: `NoSuchElementException`

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element:
{"method":"css selector","selector":"[id="user-nam"]"}
```

Diagnosis checklist, in order:

1. **Read the selector in the message.** Here it is `user-nam`: a typo. Fix the spelling.
2. If the spelling is right, **test the same locator in DevTools** (`Ctrl+F`). `0 of 0` means the locator is wrong for this page.
3. If DevTools finds it but Selenium does not, ask: *is it inside an iframe?* (Elements inside a frame are invisible to a normal search; iframes are covered in depth on Wednesday.) *Is it created by JavaScript after the page loads?* (A timing problem; see Tuesday.) *Are you on the page you think you are?* (Print `driver.getCurrentUrl()` just before the failure.)
4. If you are on the right page, the element exists, and it is not in a frame, check whether the locator depends on text that differs (language, whitespace, case).

### Walk-through 2: `InvalidSelectorException`

```
org.openqa.selenium.InvalidSelectorException: invalid selector: Compound class names not permitted
```

The word *invalid* means Selenium/the browser could not even parse the locator. The classic cause is `By.className("a b")`. Replace with `By.cssSelector(".a.b")`. A similar error appears for malformed XPath:

```
invalid selector: Unable to locate an element with the xpath expression //input[@id='x' because of the following error: SyntaxError ...
```

Look for a missing closing bracket `]` or an unbalanced quote.

### Walk-through 3: the locator matches, but the *wrong* element is used

Symptom: the test clicks something, but not what you meant, with no exception. You wrote `By.className("btn_inventory")` expecting the Backpack button, and it clicked the Backpack button *by luck* because it was first; after the product order changed, a different one was clicked.

Diagnosis: `findElement` silently returns the **first** match. Test the locator in DevTools: if the count is greater than 1, it is not unique. Fix: anchor on the product name as in the XPath example, or use the unique per-product `id`/`data-test` that SauceDemo provides on each Add to cart button.

### Walk-through 4: it worked yesterday

Possible causes: a redesign changed the structure (absolute XPath), a generated ID changed (dynamic ID), the text was reworded (text-based locator), or a new element now also matches (non-unique locator). Compare yesterday's and today's DOM in DevTools and decide which assumption of your locator broke. Then rewrite it to depend on something more stable.

---

## Guided Lab: Locator Workshop

**Goal:** practise reading a page, choosing strategies, and verifying uniqueness, then confirm them in code.

**Part A: SauceDemo login (id/name/CSS)**

1. Open `https://www.saucedemo.com` in Chrome and press `F12`.
2. For the Username field, Password field and Login button, find in the Elements panel: the `id`, `data-test` and `name` attributes.
3. In the `Ctrl+F` search box type each of these and write down the count (`1 of 1` expected):
   - `#user-name`, `[data-test='username']`, `//input[@name='user-name']`.
4. Create `LocatorLab.java` with a `main` that opens the page and prints the sizes of these `findElements` calls:

```java
System.out.println(driver.findElements(By.id("user-name")).size());
System.out.println(driver.findElements(By.cssSelector("[data-test='username']")).size());
System.out.println(driver.findElements(By.xpath("//input[@name='user-name']")).size());
System.out.println(driver.findElements(By.className("form_input")).size());
```

**Expected output:** `1`, `1`, `1`, and `2` (the class is shared by the username and password boxes). `findElements` returning a size is a safe way to *count* matches without an exception; the Find Methods lesson explains why.

**Part B: the-internet login page**

1. Open `https://the-internet.herokuapp.com/login`.
2. Inspect the fields. Write a locator for each: username input, password input, and the Login button. Hint: the page uses `id="username"` and `id="password"`, and the button has class `radius`. Which is the best locator for the button? (Think: is the class unique? Is there a better route, such as `button[type='submit']`?)
3. Log in with `tomsmith` / `SuperSecretPassword!` in code, then locate the green banner with `By.id("flash")` and print `getText()`. **Expected output** contains `You logged into a secure area!`.

**Part C: a hostile page, `https://the-internet.herokuapp.com/challenging_dom`**

1. Inspect the three coloured buttons on the left. Reload the page twice and compare their `id` attributes. What do you notice? (They change on each load, so `By.id` is not usable.)
2. Write a locator for the *first* button that does not depend on the id, for example using the class combination `a.button:not(.alert):not(.success)`, or `(//a[contains(@class,'button')])[1]`. Verify `1 of 1` in DevTools.
3. Reflect: which is more robust, the class-based CSS or the positional XPath, and why?

**Part D: a table, `https://the-internet.herokuapp.com/tables`**

1. Write an XPath that returns the **email** of the person with last name `Bach` without using a row index.
2. Print it. Hint: the pattern is `//table[@id='table1']//td[text()='Bach']/following-sibling::td[...]`; count which sibling is the email.

**Part E: Wrap-up**

Move your best locators into a `static final By` constants class like `LoginLocators` and re-run Parts A and B using the constants.

---

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| `By.className("btn btn_primary")` | Compound class names (spaces) are not allowed | `By.cssSelector(".btn.btn_primary")` |
| Using absolute XPath copied from DevTools | Breaks when page layout changes | Write a short relative XPath |
| Relying on a dynamic ID (`id="ember1234"`) | ID changes on every load | Use another attribute or `starts-with(@id,'ember')` only if the prefix is stable |
| Forgetting XPath is 1-based | `//input[0]` matches nothing | Use `[1]` for the first element |
| Using `linkText` on a `<button>` | `linkText` only works for `<a>` tags | Use CSS or XPath |
| Double quotes inside Java strings | `"//input[@id="x"]"` is a syntax error | Use single quotes inside: `"//input[@id='x']"` |
| Locator matches 3 elements, test uses first by accident | Wrong element clicked sometimes | Make the locator unique; verify "1 of 1" in DevTools |
| Using text-based locators in a multi-language site | Text differs per language | Prefer attribute-based locators |
| Testing locators in "View page source" | Source is not the live DOM | Use DevTools Elements panel |
| Writing `//div//button[1]` and expecting "the first button on the page" | `[1]` applies per parent, not globally | Use `(//div//button)[1]` |

---

## Practice Exercises

Use https://www.saucedemo.com (log in with `standard_user` / `secret_sauce`) and https://the-internet.herokuapp.com for these.

1. **Locator table.** For the SauceDemo login form, write a table of the Username field, Password field, and Login button, giving **three different valid locators for each** (for example id, CSS, XPath). Verify each in DevTools shows "1 of 1".
2. **CSS challenge.** Write CSS selectors for (a) all product title elements on the inventory page, (b) the shopping-cart link, (c) the second product in the list using `nth-child`.
3. **XPath challenge.** Write an XPath that clicks "Add to cart" **for a product you name** (e.g., "Sauce Labs Bike Light") without using indexes.
4. **Fix these fragile locators:**
   - `/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[1]/input`
   - `By.className("form_input input_error")`
   - `//input[@id='username-4821']` (assume the number changes each load)
5. **Count it.** Using `By.tagName("a")`, print the number of links on `https://the-internet.herokuapp.com`. Then print the text of the first three.
6. **Why does `By.linkText("sauce labs")` fail** to find the link in the earlier example even though the text appears on the page? (Hint: case sensitivity.)
7. **Reflection.** Pick any website you use daily. Find one element where an `id` is available and one where you would have to use XPath. Explain your choice.
8. **Read an XPath.** Explain in words, piece by piece: `//label[normalize-space()='Password']/following-sibling::input[1]`.
9. **Read a CSS selector.** Explain in words: `ul > li:not(.hidden) a[href^='/products']`.
10. **Prefix match.** An application generates ids `order-row-7391`, `order-row-7392`, and so on. Write one CSS and one XPath locator that match all rows, and explain when you would use `findElements`.
11. **Parent navigation.** On the SauceDemo inventory page, write an XPath that returns the *price* element in the same card as "Sauce Labs Onesie".
12. **Refactor.** Create a `InventoryLocators` class with `static final By` constants for the cart link, the product titles and the burger-menu button. Choose each strategy deliberately and justify it in a comment.

---

## Solutions and Hints

**1.** Username: `By.id("user-name")`, `By.cssSelector("[data-test='username']")`, `By.xpath("//input[@name='user-name']")`. Password: `By.id("password")`, `By.name("password")`, `By.xpath("//input[@type='password']")`. Login: `By.id("login-button")`, `By.cssSelector("input[type='submit']")`, `By.xpath("//input[@value='Login']")`.

**2.** (a) `.inventory_item_name` (b) `.shopping_cart_link` (c) `.inventory_item:nth-child(2)` is possible if the cards are siblings in the same parent; verify in DevTools (the container is `.inventory_list`, so `.inventory_list > .inventory_item:nth-child(2)` is the safe form). Positional, so keep it as a last resort.

**3.**

```java
By addButton = By.xpath("//div[text()='Sauce Labs Bike Light']"
        + "/ancestor::div[@class='inventory_item']//button");
```

**4.** (1) `By.id("user-name")` (2) `By.cssSelector(".form_input.input_error")` or better `By.id("user-name")` (3) `By.cssSelector("input[id^='username-']")` or `//input[starts-with(@id,'username-')]`, if the prefix is stable. Ideally ask for a `data-test`.

**5.**

```java
List<WebElement> links = driver.findElements(By.tagName("a"));
System.out.println("Links: " + links.size());
for (int i = 0; i < 3; i++) {
    System.out.println(links.get(i).getText());
}
```

**6.** `linkText` is an exact, case-sensitive match. The page text is `Sauce Labs`, not `sauce labs`. Use `partialLinkText("Sauce")` or fix the case.

**7.** Any reasoned answer: IDs on form fields are common; XPath is needed for "the button in the row whose text is X".

**8.** Find a `label` whose text, after trimming and collapsing extra spaces, is `Password`; move to its following siblings that are `input` elements; take the first of them (`[1]`).

**9.** Start at a `ul`; take its direct `li` children that do **not** have class `hidden`; inside each, any descendant `a` whose `href` begins with `/products`.

**10.** CSS: `[id^='order-row-']`. XPath: `//*[starts-with(@id,'order-row-')]`. Use `findElements` because many elements match.

**11.**

```java
By onesiePrice = By.xpath("//div[text()='Sauce Labs Onesie']"
        + "/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']");
```

**12.**

```java
public class InventoryLocators {
    // data-test attribute is purpose-built for tests
    static final By CART_LINK     = By.cssSelector("[data-test='shopping-cart-link']");
    // one class shared by all titles: used with findElements
    static final By PRODUCT_TITLE = By.className("inventory_item_name");
    // stable id
    static final By MENU_BUTTON   = By.id("react-burger-menu-btn");
}
```

(Verify the attribute values in DevTools; if one differs, use what you observe.)

---

## Self-Check Q&A

1. **What is the type of a locator in Selenium Java, and does creating one contact the browser?** `By`. No; the search happens only when passed to `findElement`/`findElements`.
2. **Why is `By.className("a b")` invalid?** `className` takes a single class; use CSS `.a.b`.
3. **Which can find an element by its visible text, CSS or XPath?** XPath (`text()`, `contains()`); CSS cannot.
4. **Why prefer relative XPath to absolute?** It does not depend on the full page structure, so it survives layout changes.
5. **What does `1 of 5` in DevTools search mean for your locator?** It matches five elements and is not unique; `findElement` would return the first.
6. **In XPath, what does `//input[2]` index start at?** 1; the second `input` child of its parent.
7. **Which attributes are the most stable for automation?** `id` (if not dynamic) and dedicated test attributes such as `data-test`.
8. **Why can a locator work in DevTools yet fail in Selenium?** Frame, timing (element not yet present), or a different page than expected.

---

## Summary

- A **locator** (`By`) tells Selenium which DOM element to act on. Poor locators are the main source of brittle tests.
- Selenium provides eight strategies: `id`, `name`, `className`, `tagName`, `linkText`, `partialLinkText`, `cssSelector`, `xpath`.
- **Prefer** unique, stable attributes (`id`, `data-test`, `name`), then concise CSS, then relative XPath for text/relationship needs.
- CSS selectors use `#id`, `.class`, `[attr='value']`, `^=`, `$=`, `*=`, `>`, `+`, `~` and `:nth-child()`. XPath uses `//tag[@attr='value']`, `contains()`, `text()`, and axes like `ancestor::` and `following-sibling::`.
- Read every selector left to right as "start wide, narrow step by step".
- **Test locators in DevTools** (`Ctrl+F`, `$$`, `$x`) before coding; aim for "1 of 1".
- Avoid absolute XPaths, dynamic IDs, and multi-class `className` locators. Keep locators named and centralized; this habit leads directly to the Page Object Model on Wednesday and to a maintainable Project 2 framework.

---

## Additional Resources

- Selenium documentation, *Locating elements*: https://www.selenium.dev/documentation/webdriver/elements/locators/
- MDN Web Docs, *CSS selectors*: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors
- W3Schools, *XPath Syntax* tutorial: https://www.w3schools.com/xml/xpath_syntax.asp
- Practice sites: https://www.saucedemo.com and https://the-internet.herokuapp.com
