# Select Elements (Dropdowns)

## Learning Objectives

By the end of this lesson you will be able to:

- Recognize the HTML `<select>` element, its `<option>` children, and the difference between single-select and multi-select lists.
- Use the Selenium `Select` class to choose options by **visible text**, **value**, and **index**.
- Read the current selection with `getFirstSelectedOption()` and `getAllSelectedOptions()`.
- List all options with `getOptions()` and verify their contents and order.
- Work with **multi-select** lists and deselect options.
- Recognize **custom dropdowns** (built from `<div>` / `<ul>`) that are **not** `<select>` elements, and automate them with ordinary click interactions.
- Apply waits to dropdowns that load their options dynamically.
- Diagnose the common dropdown exceptions from their messages.
- Write a reusable dropdown helper.

---

## Why This Matters

Dropdown lists are everywhere: country and state pickers on registration forms, sort-by menus on shopping sites ("Price: low to high"), date pickers (day/month/year), department filters in admin screens. Because they combine *several* clicks (open list, find option, choose) manually, a naive Selenium script that clicks each piece separately is lengthy and fragile.

Selenium provides a dedicated helper, the **`Select` class**, which turns that multi-step interaction into one line. It also lets you **verify** dropdown content: for example, "the country list contains 'Canada'" or "the sort options appear in the expected order". In your **Project 2** framework, a form-based test (registration, checkout, search filter) almost always involves at least one dropdown.

### How this connects to earlier lessons

- **Monday:** you find the dropdown with `driver.findElement(By...)`. A `<select>` is located exactly like any other element.
- **Earlier today (Element Interactions):** you learned that `click()` and `sendKeys()` are the core actions and that Selenium refuses to act on hidden or disabled elements. `Select` builds on the same rules.
- **Earlier today (Waiting Strategies):** options can load late, so `Select` is combined with `WebDriverWait`.

### Why not just click the options?

Imagine a physical drop-down menu in a restaurant app: you tap it, a list appears, and you tap your choice. In a *native* browser dropdown, the open list is drawn by the **operating system or browser**, not by the web page, so Selenium cannot reliably click items in it. The `Select` class avoids this by talking to the `<option>` elements directly and telling the browser "this one is now selected". That is why it is both shorter and more reliable than clicking.

### Real-world scenario

An online shop lets users sort products by name or price. A tester has to check that "Price (low to high)" actually puts the cheapest item first. By hand that means choosing the option and scanning prices. With Selenium, one line picks the option and a few lines read all prices and compare them with a sorted copy, so the check runs on every build in seconds. Today you will build exactly this test on SauceDemo.

---

## The Concept

### 1. The HTML Behind a Dropdown

A native dropdown is a `<select>` element containing `<option>` elements:

```html
<select id="sort-by">
  <option value="az">Name (A to Z)</option>
  <option value="za">Name (Z to A)</option>
  <option value="lohi" selected>Price (low to high)</option>
  <option value="hilo">Price (high to low)</option>
</select>
```

- Each `<option>` has **visible text** (what the user reads), a **value** attribute (what is submitted to the server), and an implicit **index** (0-based position).
- `selected` marks the default option.
- Add `multiple` to the `<select>` tag and it becomes a **multi-select** list box where several options can be chosen at once (with Ctrl/Shift).

```html
<select id="languages" multiple>
  <option value="java">Java</option>
  <option value="py">Python</option>
  <option value="js">JavaScript</option>
</select>
```

You can recognize a native select in DevTools by the `<select>` tag. **If you do not see a `<select>` tag, the `Select` class will not work** (see Section 8).

**Reading the HTML, piece by piece.**

| Piece | Meaning |
|---|---|
| `<select id="sort-by">` | The dropdown container; `id` is what you locate it with (`By.id("sort-by")`) |
| `<option value="az">` | One choice; the **value** is the hidden code (`az`) |
| `Name (A to Z)` (between the tags) | The **visible text** the user sees |
| `selected` | This option is chosen when the page loads |
| `multiple` | Several options may be chosen at once |
| `disabled` (on an option) | Shown but cannot be chosen; common for placeholders like "Please select an option" |

**Placeholders.** Many dropdowns start with a placeholder such as `<option value="" disabled selected>Select a country</option>`. It sits at index 0, is the initial selection, and is often disabled. Choosing "the first option" by index 0 therefore picks the placeholder, not a country. Always print the option list the first time you automate a new dropdown.

**Why the difference between text and value exists.** The visible text is for humans and may change ("United States of America" becomes "USA"). The value is for the program and is usually stable (`US`). A good test chooses the one that suits what it verifies: use text to test what users see, use value for stable data.

### 2. Creating a `Select` Object

```java
import org.openqa.selenium.support.ui.Select;

WebElement dropdownElement = driver.findElement(By.id("sort-by"));
Select dropdown = new Select(dropdownElement);
```

- The constructor **wraps** a `WebElement`. Passing an element that is not a `<select>` throws `UnexpectedTagNameException` immediately. That error itself tells you "this is a custom dropdown".
- `Select` is in the package `org.openqa.selenium.support.ui`, provided by the same `selenium-java` dependency.

Line by line:

1. `import ...Select;` makes the class available. Without it Java says "cannot find symbol: class Select".
2. `driver.findElement(By.id("sort-by"))` finds the `<select>` and returns it as a plain `WebElement`.
3. `new Select(dropdownElement)` creates a **wrapper** (also called a decorator): an object that adds dropdown-specific methods around your element. It checks the tag name once, at construction, and stores the element. The wrapper does not copy the options; each method queries the live page.

> **Analogy:** a `WebElement` is a general remote control with only basic buttons (click, type). `Select` is a special adaptor that adds the dropdown buttons (choose by text, list options). The adaptor only fits devices that really are `<select>` tags.

You can combine both lines into one when you do not need the element separately: `new Select(driver.findElement(By.id("sort-by")))`.

### 3. Choosing an Option: Three Ways

```java
dropdown.selectByVisibleText("Price (high to low)");   // by what the user sees
dropdown.selectByValue("hilo");                        // by the value attribute
dropdown.selectByIndex(1);                             // by position (0-based)
```

| Method | Matches | Best used when | Risk |
|---|---|---|---|
| `selectByVisibleText(String)` | The option's exact visible text | Text is stable and meaningful; most readable in tests | Text changes (wording, translation) break the test |
| `selectByValue(String)` | The `value` attribute | Values are stable codes (`"lohi"`, `"US"`) | Values may be unreadable IDs |
| `selectByIndex(int)` | Position in the list, starting at 0 | Quick experiments; "pick any" | Reordering the list changes meaning; index 0 is often a placeholder like "Select..." |

If nothing matches, Selenium throws `NoSuchElementException` (for example `Cannot locate option with text: ...`).

> **Tip:** `selectByVisibleText` is based on exact visible text, with whitespace normalized. Use `selectByValue` or a different approach when the display text contains special characters or changes by language.

**What happens when `dropdown.selectByVisibleText("Price (high to low)")` runs:**

1. `Select` searches the `<option>` children of this `<select>` for one whose visible text equals the string.
2. If none is found, it throws `NoSuchElementException`.
3. If found, it checks that the option is enabled. Disabled options cannot be chosen.
4. If the option is not already selected, `Select` clicks it (for a single-select the browser unselects the previous one). The page's JavaScript receives the `change` event, so features like re-sorting run as for a user.
5. If it was already selected, nothing changes. Selecting the same option twice is harmless.

**Choosing the right method: a decision guide.**

| Situation | Choose |
|---|---|
| Test reads like a user story: "choose Price (low to high)" | `selectByVisibleText` |
| The site is multilingual; the label changes by language | `selectByValue` |
| Dropdown of months/years that you generate in a loop | `selectByIndex` or `selectByValue` |
| Test data comes from a spreadsheet of display names | `selectByVisibleText` |
| You must pick "any valid option" (random choice) | `selectByIndex` with a random index starting at 1 |

**Picking a random valid option** (a common data-variation technique):

```java
Select country = new Select(driver.findElement(By.id("country")));
int count = country.getOptions().size();
int index = 1 + new java.util.Random().nextInt(count - 1);   // skip placeholder at 0
country.selectByIndex(index);
System.out.println("Chose: " + country.getFirstSelectedOption().getText());
```

`nextInt(count - 1)` gives a number from 0 to `count - 2`; adding 1 shifts it to 1 ... `count - 1`, which are all the valid indexes except 0. Printing the choice lets you reproduce a failure later.

### 4. Reading the Dropdown's State

```java
WebElement current = dropdown.getFirstSelectedOption();
System.out.println("Currently selected: " + current.getText());     // text shown
System.out.println("Its value: " + current.getAttribute("value"));

List<WebElement> all = dropdown.getOptions();
System.out.println("Number of options: " + all.size());
for (WebElement option : all) {
    System.out.println(option.getText());
}

boolean multi = dropdown.isMultiple();   // true for <select multiple>
```

| Method | Returns |
|---|---|
| `getOptions()` | `List<WebElement>` of **all** `<option>` elements |
| `getFirstSelectedOption()` | The (first) selected `WebElement`; in a single-select, *the* selected option |
| `getAllSelectedOptions()` | `List<WebElement>` of all selected options (multi-select) |
| `isMultiple()` | `true` if the `<select>` has the `multiple` attribute |

Explanation: `getOptions()` returns ordinary `WebElement`s, so everything you know applies: `getText()` for the visible text, `getAttribute("value")` for the value, `isEnabled()` to see if the option is selectable, `isSelected()` to see if it is chosen. If nothing at all is selected in a multi-select, `getFirstSelectedOption()` throws `NoSuchElementException("No options are selected")`, so for multi-selects prefer `getAllSelectedOptions()` and check whether the list is empty.

**Verifying content**, a very common test:

```java
List<String> actual = dropdown.getOptions().stream()
        .map(WebElement::getText)
        .collect(java.util.stream.Collectors.toList());

List<String> expected = java.util.Arrays.asList(
        "Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)");

if (actual.equals(expected)) {
    System.out.println("PASS: options and order are correct");
} else {
    System.out.println("FAIL: " + actual);
}
```

Explanation: `stream().map(WebElement::getText)` converts each option element to its text; `collect(toList())` builds a `List<String>` that can be compared with `equals` (same elements in the same order). For ordering-insensitive comparisons, compare as sets or sort both.

**If streams are new to you,** here is the same code with an ordinary loop. Both produce an identical list:

```java
List<String> actual = new java.util.ArrayList<>();
for (WebElement option : dropdown.getOptions()) {
    actual.add(option.getText());
}
```

Reading `WebElement::getText`: this is a **method reference**, shorthand for the lambda `option -> option.getText()`. `Arrays.asList(...)` builds a fixed list from the listed values. `List.equals` returns `true` only when both lists have the same size and the same elements in the same positions.

### 5. Multi-Select Lists

Only if `isMultiple()` is true:

```java
Select langs = new Select(driver.findElement(By.id("languages")));

langs.selectByVisibleText("Java");
langs.selectByValue("py");          // adds to the selection (does not replace it)

List<WebElement> chosen = langs.getAllSelectedOptions();   // Java, Python

langs.deselectByVisibleText("Java");
langs.deselectByValue("py");
langs.deselectByIndex(2);
langs.deselectAll();                 // clear the selection
```

Calling any `deselect...` method on a **single-select** dropdown throws `UnsupportedOperationException`: "You may only deselect options of a multi-select". Check `isMultiple()` if the code must handle both.

Notes:

- In a multi-select, each `selectBy...` call **adds** the option to the existing selection; it behaves like holding Ctrl while clicking.
- To select a *range*, call `selectByIndex` repeatedly in a loop.

**Why a single-select cannot be "deselected".** A normal dropdown always has exactly one chosen option (like radio buttons); "none" is not allowed, so the operation makes no sense and Selenium refuses.

**Example: verifying exactly what is selected in a multi-select.**

```java
List<String> selectedTexts = new java.util.ArrayList<>();
for (WebElement o : langs.getAllSelectedOptions()) {
    selectedTexts.add(o.getText());
}
System.out.println(selectedTexts);          // [Java, Python]
```

### 6. Verifying a Selection After the Fact

Always verify the result of your action, especially when selection triggers JavaScript (re-sorting a list, loading new fields):

```java
dropdown.selectByVisibleText("Price (low to high)");

String selected = dropdown.getFirstSelectedOption().getText();
// assert selected equals "Price (low to high)"
```

For a sort dropdown, verify the *effect*, not just the selection: read all prices and confirm they are ascending:

```java
List<Double> prices = driver.findElements(By.className("inventory_item_price")).stream()
        .map(e -> Double.parseDouble(e.getText().replace("$", "")))
        .collect(java.util.stream.Collectors.toList());

List<Double> sorted = new java.util.ArrayList<>(prices);
java.util.Collections.sort(sorted);
System.out.println(prices.equals(sorted) ? "PASS: sorted ascending" : "FAIL: not sorted");
```

Line by line:

1. `findElements(By.className("inventory_item_price"))` returns one element per product price, e.g. text `$29.99`.
2. `.stream().map(e -> Double.parseDouble(e.getText().replace("$", "")))` removes the dollar sign and converts text to a `double`, because `"$9.99"` cannot be compared numerically as text (as strings, `"$9.99"` would sort after `"$29.99"`).
3. `new ArrayList<>(prices)` makes a **copy**; sorting the copy leaves the original in page order.
4. `Collections.sort(sorted)` arranges the copy in ascending order.
5. `prices.equals(sorted)` is `true` only if the page's order already was ascending. The `? :` operator picks which message to print.

For descending order, use `sorted.sort(Collections.reverseOrder())`. For name sorting use `List<String>` and compare with `String.CASE_INSENSITIVE_ORDER` if the site ignores case.

### 7. Dropdowns and Waits

Many dropdowns are **dependent**: choosing a country loads the state list through AJAX. If your test selects a state before the list has loaded, it fails with `NoSuchElementException`. Apply the wait strategies from earlier today:

```java
new Select(driver.findElement(By.id("country"))).selectByVisibleText("Canada");

// wait until the state dropdown has more than the placeholder option
wait.until(d -> new Select(d.findElement(By.id("state"))).getOptions().size() > 1);

new Select(driver.findElement(By.id("state"))).selectByVisibleText("Ontario");
```

Notice we create a **new** `Select` inside the lambda each time, because the old element reference may be stale if the page re-renders the list.

**Timeline of the problem.**

| Time | Page | Test without a wait |
|---|---|---|
| 0 ms | User (test) chooses "Canada"; page requests Canadian states | `selectByVisibleText("Ontario")` runs |
| 1 ms | State list still holds only the placeholder | Error: `Cannot locate option with text: Ontario` |
| 400 ms | Provinces arrive | (too late) |

With the wait, the test polls every 500 ms until there is more than one option, then selects.

**More reliable condition: wait for the specific option.** If you know which text you will choose, wait for exactly that, which also guards against a half-loaded list:

```java
wait.until(d -> new Select(d.findElement(By.id("state")))
        .getOptions().stream()
        .anyMatch(o -> o.getText().equals("Ontario")));
```

`anyMatch` returns `true` as soon as one option satisfies the test.

**Other wait scenarios.**

- *The dropdown itself is hidden until a previous choice:* wait for `visibilityOfElementLocated` (or `elementToBeClickable`) on the `<select>` before wrapping it.
- *The page re-renders after selecting (for example, a sort):* wait for the effect, such as the first product name to change, before reading results. A neat approach is to save the old first item, select, then `wait.until(ExpectedConditions.stalenessOf(oldFirstItem))`.

### 8. Custom Dropdowns (Not `<select>`)

Modern UI libraries (Bootstrap, Material UI, React-Select, Select2) often replace the native `<select>` with custom components built from `<div>`, `<ul>`, `<li>`, or `<button>` elements. They *look* like dropdowns, but:

- Wrapping them with `new Select(...)` throws `UnexpectedTagNameException: Element should have been "select" but was "div"`.
- The options may **not exist in the DOM** until the dropdown is opened.

**How to automate them: do what a user does**

1. Click the dropdown to open it.
2. Wait for the options to become visible.
3. Click the desired option (found by its text).

```java
// Open the custom dropdown
wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".country-dropdown"))).click();

// Choose "Canada" from the options that appear
wait.until(ExpectedConditions.elementToBeClickable(
        By.xpath("//ul[@class='options']//li[normalize-space()='Canada']"))).click();

// Verify
String shown = driver.findElement(By.cssSelector(".country-dropdown .selected-value")).getText();
```

Searchable ("typeahead") dropdowns: click, type the text into the search box (`sendKeys`), then click the filtered option or press `Keys.ENTER`.

**Quick way to tell the difference:** in DevTools, if the element you right-clicked is a `<select>` with `<option>` children, use `Select`. If not, use clicks.

**Explaining the XPath.** `//ul[@class='options']//li[normalize-space()='Canada']` means: anywhere on the page, a `<ul>` whose class is `options`; anywhere inside it, an `<li>` whose text, after trimming leading/trailing spaces and collapsing repeated spaces (`normalize-space()`), equals `Canada`. Using the *text* means the test does not depend on the option's position, and `elementToBeClickable` ensures the list has opened. (Locator rules are from Monday.)

**A reusable method for custom dropdowns:**

```java
public void chooseFromCustomDropdown(By dropdown, String optionText) {
    wait.until(ExpectedConditions.elementToBeClickable(dropdown)).click();
    By option = By.xpath("//li[normalize-space()='" + optionText + "']");
    wait.until(ExpectedConditions.elementToBeClickable(option)).click();
}
```

Here the `By` for the option is built from a parameter, so one method serves every value. (If the text may contain an apostrophe, XPath quoting gets tricky; prefer a stable `data-` attribute then.)

**Typeahead example:**

```java
WebElement box = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".select2-search__field")));
box.sendKeys("Can");
wait.until(ExpectedConditions.elementToBeClickable(
        By.xpath("//li[contains(@class,'result') and normalize-space()='Canada']"))).click();
```

Typing "Can" filters the list to matching entries; you then click the exact one (an alternative is `box.sendKeys(Keys.ENTER)` when the first match is the one you want).

**Hybrid case: a native `<select>` hidden by a styled widget.** Some libraries keep a hidden real `<select>` behind the pretty widget. The hidden `<select>` is not displayed, so `Select` throws `ElementNotInteractableException` when you try to choose. Click the visible widget instead.

### 9. A Reusable Dropdown Helper

```java
package com.revature.qea.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;

public class DropdownUtils {

    private final WebDriverWait wait;

    public DropdownUtils(WebDriver driver) {
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    private Select select(By locator) {
        WebElement element = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        return new Select(element);
    }

    public void chooseByText(By locator, String text) {
        select(locator).selectByVisibleText(text);
    }

    public void chooseByValue(By locator, String value) {
        select(locator).selectByValue(value);
    }

    public String selectedText(By locator) {
        return select(locator).getFirstSelectedOption().getText();
    }

    public List<String> optionTexts(By locator) {
        return select(locator).getOptions().stream()
                .map(WebElement::getText)
                .collect(Collectors.toList());
    }

    public boolean hasOption(By locator, String text) {
        return optionTexts(locator).contains(text);
    }
}
```

Each method creates a `Select` freshly from a waited-for locator, which avoids stale references and gives consistent waiting behavior.

Design notes: the private method `select(By)` is the single place where we wait and wrap. Public methods are one-liners built on it, so changing the timeout or adding logging happens in one spot. This is the same idea as yesterday's `WaitUtils` and is a stepping stone to **Page Objects** (helper classes that become the POM foundation tomorrow; covered in depth on Wednesday). A test using the helper reads like a sentence:

```java
DropdownUtils dd = new DropdownUtils(driver);
dd.chooseByText(By.className("product_sort_container"), "Name (Z to A)");
System.out.println(dd.selectedText(By.className("product_sort_container")));
```

### 10. Troubleshooting Walk-Throughs

**Case 1: wrapping a non-select.**

```
org.openqa.selenium.support.ui.UnexpectedTagNameException: Element should have been "select" but was "div"
```

Diagnosis: inspect the element in DevTools. The locator found a `<div>` (perhaps the container or the visible widget). Either your locator points to the wrong element (look for a `<select>` inside), or the dropdown is custom (use click-open-click).

**Case 2: option text not found.**

```
org.openqa.selenium.NoSuchElementException: Cannot locate option with text: Price (Low to High)
```

Diagnosis: compare to the real text; here the capital letters differ (`low to high`). Print the options (`getOptions()` loop) and copy the text exactly. If the text appears right but still fails, there may be non-breaking spaces or trailing text; try `selectByValue`.

**Case 3: option exists but is disabled.** The `/dropdown` page has a disabled "Please select an option" placeholder at index 0. Trying to select it throws an exception because a user cannot choose a disabled option. Fix the test data: choose a real option.

**Case 4: stale `Select` after a page update.**

```
org.openqa.selenium.StaleElementReferenceException: stale element reference: element is not attached to the page document
```

Diagnosis: you stored a `Select` (which holds the old `<select>` element), the page rebuilt the DOM, and you reused it. Fix: construct a new `Select` from a fresh `findElement` each time (the helper does this).

**Case 5: deselect on single-select.**

```
java.lang.UnsupportedOperationException: You may only deselect options of a multi-select
```

Fix: guard with `if (select.isMultiple())` or remove the call.

---

## Code Example: Dropdowns on a Practice Site and SauceDemo

```java
package com.revature.qea.select;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class SelectDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        try {
            driver.manage().window().maximize();

            // ---------- Part 1: a native single-select ----------
            driver.get("https://the-internet.herokuapp.com/dropdown");
            Select dropdown = new Select(driver.findElement(By.id("dropdown")));

            System.out.println("Is multiple? " + dropdown.isMultiple());
            System.out.println("Default selection: " + dropdown.getFirstSelectedOption().getText());

            for (WebElement option : dropdown.getOptions()) {
                System.out.println("Option: " + option.getText()
                        + " (value=" + option.getAttribute("value") + ")");
            }

            dropdown.selectByVisibleText("Option 1");
            System.out.println("After text:  " + dropdown.getFirstSelectedOption().getText());

            dropdown.selectByValue("2");
            System.out.println("After value: " + dropdown.getFirstSelectedOption().getText());

            dropdown.selectByIndex(1);
            System.out.println("After index: " + dropdown.getFirstSelectedOption().getText());

            // ---------- Part 2: SauceDemo sort dropdown, verify the effect ----------
            driver.get("https://www.saucedemo.com");
            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.id("password")).sendKeys("secret_sauce");
            driver.findElement(By.id("login-button")).click();

            Select sort = new Select(wait.until(ExpectedConditions.visibilityOfElementLocated(
                    By.className("product_sort_container"))));
            sort.selectByVisibleText("Price (low to high)");

            List<Double> prices = driver.findElements(By.className("inventory_item_price")).stream()
                    .map(e -> Double.parseDouble(e.getText().replace("$", "")))
                    .collect(Collectors.toList());
            List<Double> expected = new ArrayList<>(prices);
            Collections.sort(expected);

            System.out.println("Prices: " + prices);
            System.out.println(prices.equals(expected) ? "PASS: ascending" : "FAIL: not ascending");

            // ---------- Part 3: what happens if we try a wrong wrapper ----------
            try {
                new Select(driver.findElement(By.className("inventory_list")));  // a <div>
            } catch (org.openqa.selenium.support.ui.UnexpectedTagNameException e) {
                System.out.println("Not a <select>: " + e.getMessage());
            }
        } finally {
            driver.quit();
        }
    }
}
```

**Key lines explained:**

- `new Select(driver.findElement(By.id("dropdown")))` finds the `<select>` and wraps it.
- The loop prints each option's text and `value` attribute so you can see the difference.
- The three `selectBy...` calls choose the same list in different ways; reading `getFirstSelectedOption()` proves it worked.
- Part 2 verifies the **effect** of choosing a sort order.
- Part 3 shows the exception you get when the element is not a native `<select>`.

**What each part prints (approximately).**

```
Is multiple? false
Default selection: Please select an option
Option: Please select an option (value=)
Option: Option 1 (value=1)
Option: Option 2 (value=2)
After text:  Option 1
After value: Option 2
After index: Option 1
Prices: [7.99, 9.99, 15.99, 15.99, 29.99, 49.99]
PASS: ascending
Not a <select>: Element should have been "select" but was "div" ...
```

Points to notice: the placeholder is option 0 with an empty `value`, so `selectByIndex(1)` is "Option 1"; the same product price may appear twice (so verify with `equals` on sorted lists, which allows ties, instead of "strictly increasing"); and `selectByValue("2")` matched the `value` attribute while the text said "Option 2".

---

## Hands-On Lab: Sort Verification and a Local Multi-Select (about 45 minutes)

**Part A: SauceDemo sort test.**

1. In Project 2, create `SortLabTest` with a `main` method. Log in as `standard_user` (reuse your login helper from earlier today).
2. Wrap the sort dropdown with `DropdownUtils` (section 9). Print `optionTexts(...)`. **Expected:** `[Name (A to Z), Name (Z to A), Price (low to high), Price (high to low)]`.
3. For each option, select it by text and read the resulting products. For name sorts, compare the names list with a sorted copy (`Collections.sort`; for Z to A use `Collections.reverse` on the sorted copy). For price sorts, use the code from section 6.
4. Print `PASS`/`FAIL` for each of the four options. **Expected:** four `PASS` lines.
5. Break it on purpose: use `"Price (Low to High)"` (capital L and H). Read the `NoSuchElementException`, then fix it.

**Part B: a multi-select on a local page.**

6. Create a file `multi.html` in your project folder:
   ```html
   <html><body>
     <select id="languages" multiple size="3">
       <option value="java">Java</option>
       <option value="py">Python</option>
       <option value="js">JavaScript</option>
     </select>
   </body></html>
   ```
7. Open it in your test with `driver.get(new java.io.File("multi.html").toURI().toString());`. (`toURI().toString()` produces a correct `file:///...` address on any operating system.)
8. Create a `Select`, print `isMultiple()` (**expected:** `true`), then select Java and Python and print `getAllSelectedOptions()` texts (**expected:** `[Java, Python]`).
9. Call `deselectByValue("java")` and print again (**expected:** `[Python]`). Call `deselectAll()` and confirm that the list is empty.
10. Call `deselectAll()` on the `/dropdown` page's single-select and read the exception text.

Compare each printed line with the expected output. A mismatch usually means a typo in a value or locator, so print `getOptions()` first.

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Using `Select` on a custom `<div>` dropdown | `UnexpectedTagNameException` | Click to open, then click the option |
| `selectByVisibleText` with extra/missing spaces or wrong case | `NoSuchElementException` | Copy the text exactly; print `getOptions()` text to compare |
| Selecting by index 0 expecting the first real choice | Selects the placeholder ("Select...") | Check the option list first |
| Calling `deselectAll()` on a single-select | `UnsupportedOperationException` | Check `isMultiple()` |
| Not waiting for dependent dropdown options | Option not found | Wait until the options are loaded |
| Reusing an old `Select` after the page changes | Stale reference | Create a new `Select` from a fresh element |
| Verifying only the selected text, not the effect | Misses broken sorting/filtering | Assert on the resulting page content too |
| Clicking `<option>` elements directly | Unreliable across browsers | Use the `Select` class |
| Comparing prices as text (`"$9.99"` vs `"$29.99"`) | Wrong sort verdict | Convert to numbers before comparing |
| Reading `getFirstSelectedOption()` on an empty multi-select | `NoSuchElementException` | Use `getAllSelectedOptions()` and check for empty |

---

## Practice Exercises

1. **Native dropdown tour.** On `https://the-internet.herokuapp.com/dropdown`, select each option using all three methods and print the selection each time.
2. **Option audit.** Print the number of options and their texts for the SauceDemo sort dropdown, and assert that they match the expected list *in order*.
3. **Sort verification.** For each of the four SauceDemo sort options, select it and verify the displayed products are correctly ordered by name or price.
4. **Multi-select.** On a page with a multi-select (for example, the W3Schools "Tryit" `select multiple` example, or your own small HTML file that you open with a `file:///` URL), select two options, print `getAllSelectedOptions()`, deselect one, then `deselectAll()`.
5. **Negative test.** Try `selectByVisibleText("Does not exist")` and catch the exception. Print its message and explain it.
6. **Custom dropdown.** Visit a site that uses a custom dropdown component (for example the React-Select or Bootstrap dropdown demo pages). Confirm that `new Select(...)` throws, and automate it using click, wait, click.
7. **Dependent dropdowns.** Describe (in pseudocode or code) how you would automate "country -> state" dropdowns where the state list loads after the country is chosen. Which wait would you use?
8. **Build `DropdownUtils`.** Add the helper class to your Project 2 skeleton and use it in the SauceDemo sort test.
9. **Selected-state check.** On `/dropdown`, write a method `assertSelected(Select s, String expectedText)` that throws an `AssertionError` with a helpful message when the selected text differs.
10. **Duplicate-free options.** Write a check that the SauceDemo sort dropdown has no duplicate option texts (hint: compare list size with `new HashSet<>(list).size()`).
11. **Random choice with reproducibility.** Write a method that picks a random non-placeholder option from any `<select>`, prints what it chose, and returns the chosen text so a failing run can be reproduced.
12. **Project 2 milestone.** Take a form or filter in your Project 2 application under test (or SauceDemo's sort) and add a test that selects an option, waits for the page to update with an explicit wait, and asserts on the resulting content. No `Thread.sleep` allowed.

---

## Solutions and Hints

**Exercise 1.** The code in the main example is a model answer. Remember index 0 is the disabled placeholder; do not select it.

**Exercise 2.**

```java
List<String> expected = java.util.Arrays.asList(
        "Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)");
List<String> actual = new DropdownUtils(driver).optionTexts(By.className("product_sort_container"));
if (!actual.equals(expected)) throw new AssertionError("Options differ: " + actual);
```

**Exercise 3 hint.** Product names have class `inventory_item_name`. For "Name (Z to A)":

```java
List<String> names = new ArrayList<>();
for (WebElement e : driver.findElements(By.className("inventory_item_name"))) names.add(e.getText());
List<String> sorted = new ArrayList<>(names);
Collections.sort(sorted);
Collections.reverse(sorted);
System.out.println(names.equals(sorted) ? "PASS" : "FAIL");
```

**Exercise 4.** Follow Part B of the lab. Typical output: `[Java, Python]`, then `[Python]`, then `[]`.

**Exercise 5.** The message reads `Cannot locate option with text: Does not exist` (Selenium may append the HTML context). It means: no `<option>` under this `<select>` has exactly that visible text.

**Exercise 6 hint.** Check with `try { new Select(el); } catch (UnexpectedTagNameException e) { ... }`. Then use the helper in section 8. Inspect the page to find the container and option locators; prefer stable attributes (`data-testid`, `id`) over generated class names.

**Exercise 7.**

```java
new Select(driver.findElement(By.id("country"))).selectByVisibleText("Canada");
wait.until(d -> new Select(d.findElement(By.id("state"))).getOptions().size() > 1);
new Select(driver.findElement(By.id("state"))).selectByVisibleText("Ontario");
```

A custom lambda wait is needed because no `ExpectedConditions` method counts `<option>`s inside a `<select>`; waiting on "the specific option exists" is even more precise.

**Exercise 9.**

```java
static void assertSelected(Select s, String expectedText) {
    String actual = s.getFirstSelectedOption().getText();
    if (!actual.equals(expectedText)) {
        throw new AssertionError("Expected selected option '" + expectedText + "' but was '" + actual + "'");
    }
}
```

**Exercise 10.**

```java
List<String> texts = dd.optionTexts(By.className("product_sort_container"));
boolean noDuplicates = new java.util.HashSet<>(texts).size() == texts.size();
```

A `HashSet` drops duplicates, so a smaller set means duplicates existed.

**Exercise 11.**

```java
static String chooseRandom(Select s) {
    List<WebElement> opts = s.getOptions();
    List<Integer> valid = new ArrayList<>();
    for (int i = 0; i < opts.size(); i++) {
        if (opts.get(i).isEnabled()) valid.add(i);
    }
    // skip the first enabled item only if it is a placeholder with an empty value
    if (!valid.isEmpty() && "".equals(opts.get(valid.get(0)).getAttribute("value"))) valid.remove(0);
    int pick = valid.get(new java.util.Random().nextInt(valid.size()));
    s.selectByIndex(pick);
    String text = s.getFirstSelectedOption().getText();
    System.out.println("Randomly chose: " + text);
    return text;
}
```

**Exercise 12 hint.** Capture something that changes (first product name, result count), select, then `wait.until(d -> !firstNameNow(d).equals(oldName))`. Assert on the new content, not just on the selected option.

---

## Self-Check Questions

1. **How can you tell a native dropdown from a custom one?** Inspect it: a native one is a `<select>` with `<option>` children; a custom one is built from `<div>`, `<ul>`, `<li>` or similar.
2. **What does `new Select(element)` throw for a `<div>`?** `UnexpectedTagNameException`.
3. **Name the three ways to choose an option and one risk of each.** Visible text (text changes), value (opaque codes), index (reordering, placeholder at 0).
4. **How do you verify that a sort dropdown really sorted the list?** Read the resulting items, convert prices to numbers, compare with a sorted copy.
5. **Which methods are only valid on multi-selects?** The `deselect...` methods; calling them on a single-select throws `UnsupportedOperationException`.
6. **Why create a new `Select` after the page updates?** The old one wraps an element that may be stale.
7. **How do you handle a dropdown whose options load by AJAX?** Wait (lambda or `ExpectedConditions`) until the needed option exists, then select.
8. **What is the first thing to do when automating an unfamiliar dropdown?** Print `getOptions()` texts and values to see placeholders, exact text, and value codes.

---

## Summary

- A native dropdown is a `<select>` with `<option>` children; a **multi-select** has the `multiple` attribute.
- Wrap the element with `new Select(element)`; if it is not a `<select>`, Selenium throws `UnexpectedTagNameException`.
- Choose with `selectByVisibleText`, `selectByValue`, or `selectByIndex`; read with `getFirstSelectedOption`, `getAllSelectedOptions`, `getOptions`, `isMultiple`.
- Multi-select lists support `deselectBy...` and `deselectAll()`; these fail on single-selects.
- Verify the **selection** and the **effect** of the selection (sorting, filtering).
- Use **waits** for dropdowns whose options load dynamically; create a fresh `Select` after page updates.
- **Custom dropdowns** are not `<select>` elements and are automated by clicking to open and clicking an option.
- Encapsulate dropdown logic in a helper for your framework.

---

## Additional Resources

- Selenium documentation, *Select list elements*: https://www.selenium.dev/documentation/webdriver/support_features/select_lists/
- Selenium Java API, `Select` class: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/support/ui/Select.html
- MDN Web Docs, *The `<select>` element*: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select
