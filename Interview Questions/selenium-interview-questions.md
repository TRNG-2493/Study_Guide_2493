# Selenium Interview Questions

**For self-study after Selenium Handouts 1–5.** Each question has a difficulty (**Easy**, **Medium**, **Hard**), a type (**Concept**, **Code**, **Design**, **Scenario**), and a model answer. Try to answer out loud or on paper **first**, then click **Show answer** to check: interviewers listen for clear explanations, not memorised text.

**How to read this file:** open it in VS Code's Markdown preview (`Ctrl+Shift+V`) or on GitHub, where each answer is hidden behind **Show answer**.

**Sections**

1. Selenium architecture, setup and JUnit (Handout 1)
2. Navigation, locators and find methods (Handout 2)
3. Interactions, waits and dropdowns (Handout 3)
4. Actions, alerts, windows and frames (Handout 4)
5. Screenshots, Page Object Model and Page Factory (Handout 5)
6. Scenario-based questions

---

## 1. Selenium architecture, setup and JUnit

### Q1. What is Selenium, and what can it test? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Selenium is a free, open-source suite of tools for automating web browsers. A Selenium program can open pages, click, type and read the screen like a user. It tests **web applications** in real browsers (Chrome, Firefox, Edge, Safari). It cannot test desktop applications or native mobile apps (Appium, which is built on WebDriver, does mobile), and it doesn't solve CAPTCHAs.

</details>

### Q2. Name the tools in the Selenium suite and what each is for. `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

- **Selenium WebDriver:** a library you call from code to control browsers; used to write automated tests.
- **Selenium IDE:** a browser extension that records and replays clicks; good for quick experiments.
- **Selenium Grid:** a server that runs tests on many machines and browsers in parallel.
- Historically: **Selenium Core** (JavaScript injected into the page) and **Selenium RC** (Selenium 1), both retired.

</details>

### Q3. What is the difference between Selenium RC and Selenium WebDriver? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

RC needed a **server** between the test and the browser and drove the browser by **injecting JavaScript** into the page, which was slow and limited by browser security rules. WebDriver controls the browser **directly** through a browser-specific **driver** (such as chromedriver), with no injected JavaScript and no server in between. RC was removed in Selenium 3; WebDriver is the standard.

</details>

### Q4. Explain the Selenium WebDriver architecture. `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Four parts:
1. **Your test code** (e.g. Java).
2. The **client library** / language binding (`selenium-java`), which turns each method call into a standard message.
3. The **browser driver** (e.g. `chromedriver`), which receives the message and controls one kind of browser.
4. The **browser** itself.

Messages between the client library and the driver follow the **W3C WebDriver protocol**, which is why the same code works across browsers. Every command is a round trip: code → library → driver → browser, and the answer comes back the same way.

</details>

### Q5. What is the W3C WebDriver protocol, and why does it matter? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

It is the official web standard for how a client talks to a browser driver. Since Selenium 4, Selenium speaks only this standard. Because every browser vendor implements it, tests behave consistently across browsers, and browser vendors maintain their own drivers.

</details>

### Q6. What is Selenium Manager? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A tool built into Selenium (since 4.6) that, when you create a driver, checks the installed browser version and downloads the matching driver if needed. You no longer download or configure `chromedriver` yourself: `new ChromeDriver()` is enough. Drivers are cached in the `.cache/selenium` folder.

</details>

### Q7. Why must the driver version match the browser version, and what happens if it doesn't? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

The driver is built for one browser version and uses that browser's internals. If an old `chromedriver` is used with a newer Chrome, starting the driver fails with `SessionNotCreatedException` ("This version of ChromeDriver only supports Chrome version ..."). The usual cause is an old driver left on the `PATH`; removing it lets Selenium Manager supply the right one.

</details>

### Q8. What is the difference between `driver.close()` and `driver.quit()`? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

`close()` closes **only the current window or tab**; the session stays alive if other windows are open. `quit()` closes **all** windows and **ends the session** (and stops the driver process). Use `quit()` at the end of every test; use `close()` only when working with several windows.

</details>

### Q9. Why should `quit()` be in a `finally` block (or `@AfterEach`)? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

If the test throws an exception before reaching `quit()`, the browser and driver stay open, and windows pile up. A `finally` block always runs, so the browser is closed whether the code succeeded or failed. In JUnit, `@AfterEach` gives the same guarantee for every test.

</details>

### Q10. What are browser options? Give three you would use. `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Start-up settings for the browser, collected in `ChromeOptions` and passed with `new ChromeDriver(options)`. Examples: `--headless=new` (no visible window), `--window-size=1280,800` (fixed size), `--start-maximized`, `--incognito`. They must be set **before** the browser starts.

</details>

### Q11. What is headless mode, and why should you set a window size with it? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Headless mode runs the browser without a visible window, which is useful on build servers that have no screen. Without a window size, headless Chrome uses a small default window, so responsive pages may show a different (mobile) layout and elements may be hidden. Setting `--window-size` makes headless runs look the same as normal runs.

</details>

### Q12. Why use JUnit instead of `main()` programs for Selenium tests? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A `main()` program only prints values for a person to read. JUnit **decides pass or fail** with assertions, runs many independent tests, reports the results, and manages set-up and clean-up with `@BeforeEach`/`@AfterEach`. It also integrates with Maven (`mvn test`), IDEs and build servers.

</details>

### Q13. What does `assertEquals(expected, actual)` do, and why does the order of arguments matter? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

It fails the test if the two values are not equal and reports both. The failure message reads "expected: <...> but was: <...>", so swapping the arguments makes the message misleading: it would claim the wrong value was expected.

</details>

### Q14. What is a `BaseTest`, and what goes in it? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

A parent class that every test class extends, holding code they all share: a `protected WebDriver driver`, `@BeforeEach` that creates the browser, and `@AfterEach` that quits it. It removes duplication and guarantees each test gets a **fresh** browser and that it is always closed. Later it can host extras such as a screenshot-on-failure extension.

</details>

### Q15. Why should each test get its own fresh browser? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

So tests are **independent**: no test depends on the login, cart or cookies left by another, and tests can run in any order or alone. It is slower than sharing one browser, but shared state is the most common cause of tests that pass alone and fail together.

</details>

---

## 2. Navigation, locators and find methods

### Q16. What is the difference between `driver.get(url)` and `driver.navigate().to(url)`? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

They do the same thing: open the URL and wait until the page has loaded. `navigate()` also gives `back()`, `forward()` and `refresh()`. A common style is `get()` to open a page and `navigate()` for history.

</details>

### Q17. Why is `getCurrentUrl()` often a better check than `getTitle()`? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Many sites use the same title on every page (the-internet's title is always "The Internet"), so a title check can pass on the wrong page. The URL usually identifies the page uniquely. Also, `get()` doesn't report redirects or error pages, so checking the URL or a heading proves you are where you meant to be.

</details>

### Q18. What is a locator? List the eight locator strategies. `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A locator is a description of how to find an element, a `By` object in Java. The eight strategies: `By.id`, `By.name`, `By.className`, `By.tagName`, `By.linkText`, `By.partialLinkText`, `By.cssSelector`, `By.xpath`. (Selenium 4 also has relative locators such as `below(...)`.)

</details>

### Q19. In what order would you choose locators, and why? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

Unique and stable first: **id** or a test attribute such as `data-test` → **name** → **CSS selector** → **XPath**. Ids and test attributes rarely change when the page is restyled. CSS is fast and readable. XPath is powerful (text, parents) but easier to make fragile. Avoid absolute XPath like `/html/body/div[2]/...`.

</details>

### Q20. CSS selector vs XPath: when would you use each? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

**CSS** for most cases: ids (`#id`), classes (`.cls`), attributes (`[data-test='x']`), children (`div > h4`); it is concise and fast. **XPath** when you need what CSS can't do: find by **visible text** (`//h4[text()='...']`) or move **up** to a parent/ancestor. Both should be short and based on stable attributes.

</details>

### Q21. How do you check a locator before using it in code? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Open DevTools (F12), go to the Elements tab, press **Ctrl+F**, and type the CSS selector or XPath. It should report **1 of 1** match. In a test, `driver.findElements(by).size()` should be 1.

</details>

### Q22. What is the difference between `findElement` and `findElements`? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

`findElement` returns the **first** matching `WebElement` and throws `NoSuchElementException` if nothing matches. `findElements` returns a **list** of all matches and returns an **empty list** (no exception) if nothing matches. Use `findElements(...).isEmpty()` to check that something is absent.

</details>

### Q23. What is a scoped search? Give an example. `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

Calling `findElement`/`findElements` on a `WebElement` searches **only inside** that element. Example: reading one table row:

```java
WebElement firstRow = driver.findElements(By.cssSelector("#table1 tbody tr")).get(0);
List<WebElement> cells = firstRow.findElements(By.tagName("td"));
String lastName = cells.get(0).getText();
```

</details>

### Q24. Why might `getText()` return an empty string? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Two common reasons: the element is an **input** (text boxes have no visible text; read `getDomProperty("value")` or an attribute instead), or the element is **hidden** (`getText()` returns only visible text). Check `isDisplayed()` and wait for visibility.

</details>

### Q25. What is the difference between `getDomAttribute` and `getDomProperty`? `Hard` · Concept

<details>
<summary><b>Show answer</b></summary>

`getDomAttribute("value")` returns the attribute **as written in the HTML** (or `null`). `getDomProperty("value")` returns the **live** value in the browser, e.g. what the user has typed. After typing "tom" into an empty box, the attribute is `null` and the property is `"tom"`. The older `getAttribute` mixed the two and is deprecated.

</details>

### Q26. How do you assert that an element is **not** on the page? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

`assertTrue(driver.findElements(by).isEmpty())`. Alternatively `assertThrows(NoSuchElementException.class, () -> driver.findElement(by))`, but `findElements` is clearer and doesn't rely on exceptions. If the element may take time to disappear, wait with `invisibilityOfElementLocated` first.

</details>

### Q27. Which `NoSuchElementException` should you import, and why does it matter? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

`org.openqa.selenium.NoSuchElementException`. Java also has `java.util.NoSuchElementException`; if you import that one, `assertThrows` fails because Selenium throws a different class.

</details>

---

## 3. Interactions, waits and dropdowns

### Q28. What checks does Selenium make before `click()` or `sendKeys()`? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

It scrolls the element into view and checks it is **interactable**: visible, enabled and not covered by another element. If not, it throws an exception (`ElementNotInteractableException`, `ElementClickInterceptedException`) instead of pretending the action happened.

</details>

### Q29. Why might a text box end up containing `tomsmithtomsmith`? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

`sendKeys` **adds** to the text already in the box. Typing "tomsmith" twice appends it. Call `clear()` first to replace the text.

</details>

### Q30. How do you press special keys such as Enter or Tab? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

With the `Keys` enum: `element.sendKeys(Keys.ENTER)`, or `element.sendKeys("password", Keys.ENTER)` to type and then press Enter. For key combinations (Ctrl+A), use the Actions API.

</details>

### Q31. Why do tests need waits? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

Pages change after loading: requests finish, spinners disappear, elements are added later. Find methods search **once, immediately**, so without a wait the test can look too early and fail with `NoSuchElementException`, or find a hidden element. A wait pauses until a condition is true.

</details>

### Q32. Compare `Thread.sleep`, implicit wait and explicit wait. `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

- **`Thread.sleep`** always waits the full time: slow, and still flaky if the time is too short. Avoid it in tests.
- **Implicit wait:** one driver-wide setting; every `findElement` retries until the element **exists**. It doesn't wait for visibility or clickability and slows down "is it absent?" checks.
- **Explicit wait:** `WebDriverWait` + a condition for **one** specific thing (visible, clickable, URL contains...). It returns as soon as the condition is true. This is the recommended default.

</details>

### Q33. Why should you not mix implicit and explicit waits? `Hard` · Concept

<details>
<summary><b>Show answer</b></summary>

An explicit wait's condition calls `findElement` internally; with an implicit wait set, each of those calls can itself block for the implicit timeout. The two times combine unpredictably, so a "wait at most 5 seconds" can take much longer. Teams usually keep implicit wait at 0 and use explicit waits.

</details>

### Q34. What is the difference between `presenceOfElementLocated` and `visibilityOfElementLocated`? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

**Presence** is true as soon as the element is **in the page's HTML**, even if hidden. **Visibility** requires it to be in the page **and visible** (displayed, with a size). Waiting only for presence can return a hidden element whose `getText()` is `""`. For anything the user must see or click, wait for visibility or clickability.

</details>

### Q35. Write an explicit wait for an element with id `finish` to become visible, then read its text. `Easy` · Code

<details>
<summary><b>Show answer</b></summary>


```java
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
WebElement finish = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("finish")));
assertEquals("Hello World!", finish.getText());
```

</details>

### Q36. What is a fluent wait? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

An explicit wait where you also set the **polling interval** and which exceptions to **ignore** while waiting, e.g. `new FluentWait<>(driver).withTimeout(...).pollingEvery(...).ignoring(NoSuchElementException.class)`. Used for special cases; `WebDriverWait` is a fluent wait with sensible defaults.

</details>

### Q37. How do you choose an option from an HTML dropdown? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

Wrap the `<select>` element in Selenium's `Select` class and choose by visible text, value or index:

```java
Select dropdown = new Select(driver.findElement(By.id("dropdown")));
dropdown.selectByVisibleText("Option 1");
String chosen = dropdown.getFirstSelectedOption().getText();
```

</details>

### Q38. Select by visible text, value or index: which is best? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

**Visible text** reads like the requirement but breaks if the wording changes; **value** survives wording and translation changes; **index** breaks when options are added or reordered and should be avoided. Choose text or value, and check the result afterwards.

</details>

### Q39. What happens if you use `Select` on a dropdown built from `<div>` elements? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

`new Select(...)` throws `UnexpectedTagNameException`, because `Select` only works on real `<select>` elements. Custom dropdowns are handled like any other elements: click to open them, then click the option.

</details>

---

## 4. Actions, alerts, windows and frames

### Q40. When do you need the Actions API instead of `click()`/`sendKeys()`? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

For gestures plain commands can't do: **hover** (`moveToElement`), **right-click** (`contextClick`), **double-click**, **drag and drop**, **key combinations** (`keyDown`/`keyUp`), and **scrolling**. For ordinary clicks and typing, use the element commands, which include Selenium's interactability checks.

</details>

### Q41. What is `perform()`, and what happens if you forget it? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

Actions are built as a **chain** of steps; `perform()` sends the whole chain to the browser. Without it, nothing happens: the chain is only a description. Example: `new Actions(driver).moveToElement(menu).click(item).perform();`

</details>

### Q42. How do you test a menu that only appears on hover? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

Hover over the visible parent with `new Actions(driver).moveToElement(parent).perform()`, **wait** for the menu or caption to become visible (`ExpectedConditions.visibilityOf(...)`), then interact with it or check its text.

</details>

### Q43. What is a JavaScript alert, and why can't `findElement` find it? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A pop-up dialog created by page JavaScript (`alert`, `confirm`, `prompt`) but drawn by the **browser**, not as part of the page's HTML. Because it isn't in the HTML, `findElement` can't see it. You switch to it with `driver.switchTo().alert()`.

</details>

### Q44. Show how to accept an alert safely and check its text. `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

Wait for it, read it, answer it, then check the page:

```java
Alert alert = new WebDriverWait(driver, Duration.ofSeconds(5))
        .until(ExpectedConditions.alertIsPresent());
assertEquals("I am a JS Alert", alert.getText());
alert.accept();     // OK; alert.dismiss() = Cancel; alert.sendKeys("...") types into a prompt
```

</details>

### Q45. How do you tell a JavaScript alert from an HTML modal? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

If you can **inspect** the pop-up in DevTools, it is HTML: use `findElement` and click its buttons. If you can't inspect it and the whole page is frozen, it is a JavaScript dialog: use `switchTo().alert()`. Using the wrong approach gives `NoAlertPresentException` or `NoSuchElementException`.

</details>

### Q46. What happens if a test ignores an open alert? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

While a dialog is open the page is frozen, so the next page command fails with `UnhandledAlertException`. Every dialog must be accepted or dismissed right after the action that opens it.

</details>

### Q47. A link opens a new tab. How do you switch to it and back? `Medium` · Code

<details>
<summary><b>Show answer</b></summary>

Save the original handle, wait for two windows, switch to the handle that isn't the original, then switch back:

```java
String original = driver.getWindowHandle();
link.click();
new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.numberOfWindowsToBe(2));
for (String handle : driver.getWindowHandles()) {
    if (!handle.equals(original)) {
        driver.switchTo().window(handle);
    }
}
// ... work in the new tab ...
driver.close();
driver.switchTo().window(original);
```

</details>

### Q48. Why do you get `NoSuchWindowException` after `driver.close()`? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

`close()` closes the current window but **doesn't switch** Selenium anywhere else, so it still points at the closed window. Switch back to a window that is still open, e.g. `driver.switchTo().window(original)`.

</details>

### Q49. An element is clearly visible on screen, but `findElement` can't find it. What could it be? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Most often it is inside an **iframe/frame**: elements in a frame belong to a separate page. Switch in with `driver.switchTo().frame(nameOrIdOrElement)`, find the element, then return with `driver.switchTo().defaultContent()`. Other causes: the element appears later (needs a wait) or it is in another window/tab.

</details>

---

## 5. Screenshots, Page Object Model and Page Factory

### Q50. How do you take a screenshot in Selenium? `Easy` · Code

<details>
<summary><b>Show answer</b></summary>

Cast the driver to `TakesScreenshot` and save the file:

```java
File source = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
Path target = Path.of("screenshots", "login-page.png");
Files.createDirectories(target.getParent());
Files.copy(source.toPath(), target, StandardCopyOption.REPLACE_EXISTING);
```

For one element only: `element.getScreenshotAs(OutputType.FILE)`.

</details>

### Q51. How would you take a screenshot automatically whenever a JUnit test fails? `Hard` · Design

<details>
<summary><b>Show answer</b></summary>

Write a JUnit **extension** implementing `AfterTestExecutionCallback`. It runs right after the test method and **before** `@AfterEach`, so the browser is still open. In it, check `context.getExecutionException().isPresent()`; if the test failed, take and save the screenshot (named after the test). Register it once with `@ExtendWith(...)` on `BaseTest`. A `TestWatcher` would run too late, after `@AfterEach` has quit the browser.

</details>

### Q52. What is the Page Object Model? `Easy` · Concept

<details>
<summary><b>Show answer</b></summary>

A design pattern where each page (or part of a page) gets its own class, a **page object**, holding that page's **locators** and **methods** for what a user can do there (`loginAs`, `addToCart`). Tests call those methods instead of using `By` and `findElement` directly, so tests read like user behaviour and a UI change is fixed in **one** class.

</details>

### Q53. What are the rules of a good page object? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

- Locators are **private** inside the page.
- Methods are named after **user intent** (`loginAs`), not mechanics (`clickButton3`).
- A method that moves to another page **returns that page's object** (`loginAs` returns `InventoryPage`).
- **No assertions** in page objects: they return values, and tests decide pass/fail.
- Waits that belong to the page (e.g. waiting for the page to load) go inside the page.

</details>

### Q54. Why shouldn't page objects contain assertions? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

A page object describes **what the page can do and show**; deciding whether that is correct belongs to the **test**. The same page method is used by many tests with different expectations (a successful login in one, an error in another). Assertions inside pages make them less reusable and hide what a test checks.

</details>

### Q55. Why does `loginAs(...)` return an `InventoryPage` but `loginExpectingError(...)` return a `LoginPage`? `Medium` · Design

<details>
<summary><b>Show answer</b></summary>

Each method returns the page the user ends up on. A successful login leads to the products page, so the test can continue with `InventoryPage` methods; a failed login stays on the login page, where the test reads the error. This makes tests read like the user's journey and lets the compiler stop you from calling methods on the wrong page.

</details>

### Q56. What is Page Factory? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

Selenium's annotation-based way to write page objects. Fields are `WebElement`s annotated with `@FindBy(id = "...")`, and `PageFactory.initElements(driver, this)` in the constructor connects them. The elements are found when the field is used.

</details>

### Q57. `By`-based page objects or Page Factory: which would you choose? `Hard` · Design

<details>
<summary><b>Show answer</b></summary>

Both are valid page objects. **`By`-based** pages work naturally with explicit waits (`visibilityOfElementLocated(by)`) and with **dynamic locators** built from data (e.g. a product name), and have no hidden behaviour. **Page Factory** gives compact field declarations but can't build locators from data, makes waits on the locator awkward, and `@CacheLookup` can cause stale elements. Many teams prefer `By`-based pages but should be able to read Page Factory code.

</details>

### Q58. What is the `@CacheLookup` trap? `Hard` · Concept

<details>
<summary><b>Show answer</b></summary>

`@CacheLookup` makes Page Factory find an element **once** and reuse it. If the page then **replaces** that element (e.g. Swag Labs swaps "Add to cart" for a new "Remove" button), the cached reference points at an element that no longer exists, and the next use throws `StaleElementReferenceException`. Only cache elements that never change.

</details>

### Q59. What is a `StaleElementReferenceException`? `Medium` · Concept

<details>
<summary><b>Show answer</b></summary>

It means a `WebElement` you found earlier no longer exists in the page: the page reloaded, navigated, or redrew that element. The fix is to **find the element again** right before using it (page objects that store `By` locators, not `WebElement`s, do this naturally).

</details>

---

## 6. Scenario-based questions

### Q60. Your tests pass on your laptop but fail on the CI server. How do you investigate? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

1. Read the failure and the **screenshot** saved on failure (screenshot-on-failure extension).
2. Check **timing**: the server is often slower. Look for `Thread.sleep` or missing waits, and replace them with explicit waits for the real condition.
3. Check **environment differences**: headless mode without a window size (different layout), a different browser version, test data, or network access.
4. Check **test independence**: tests that pass alone but fail when run together on CI usually share state.

</details>

### Q61. A test sometimes passes and sometimes fails, without code changes. What do you do? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

It is **flaky**, usually because of timing or shared state. Run it several times to reproduce, read the failing step and screenshot, and look for: waiting for presence instead of visibility, `Thread.sleep`, an implicit + explicit wait mix, elements that are redrawn (stale references), or data left by another test. Fix the cause; don't just add retries or longer sleeps.

</details>

### Q62. After clicking "Add to cart", clicking the same stored button again throws `StaleElementReferenceException`. Why, and how do you fix it? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

The page **replaced** the button: on Swag Labs, "Add to cart" is swapped for a new "Remove" button element. The stored `WebElement` refers to the old one. Find the element again before each use, e.g. `driver.findElement(By.id("remove-sauce-labs-backpack")).click()`, ideally inside a page object method that stores `By` locators.

</details>

### Q63. A click on "Submit" fails with `ElementClickInterceptedException`. What is happening? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Another element is **on top** of the button at the click point: a cookie banner, a loading overlay, a sticky header or a modal. Close or wait for the covering element to disappear (`invisibilityOfElementLocated`), or wait for the button to be clickable. Don't "fix" it with a JavaScript click, which hides a real usability problem.

</details>

### Q64. Your locator `//div[3]/div[2]/button` worked last sprint and fails today. What do you change? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

It is a **position-based** XPath that breaks whenever the layout changes. Replace it with a stable locator: an id, a `data-test` attribute, a name, or a short CSS/XPath using meaningful attributes or text. If the page has no stable hooks, ask developers to add `data-test` attributes.

</details>

### Q65. A test fails with `NoSuchElementException` right after clicking Login. The element is there when you look. Why? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

The test looked **too early**: the next page or element appears a moment after the click, and `findElement` searches only once. Add an explicit wait for the element (or the URL) on the next page. In a page object, put that wait inside the page, e.g. `InventoryPage.title()` waits for the title to be visible.

</details>

### Q66. Many tests repeat the same login code. What is the problem, and how would you fix it? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Duplication: if the login page changes, every test must be edited, and tests are hard to read. Move the login locators and steps into a **`LoginPage` page object** with a `loginAs(user, password)` method, and call it from the tests. Shared browser start/quit goes into **`BaseTest`**.

</details>

### Q67. A teammate added `Thread.sleep(10000)` to fix a failing test. What do you say? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

It hides the problem and slows every run by 10 seconds, and the test will still fail whenever the page needs 11 seconds. Find what the test is really waiting for (an element visible, a button clickable, a URL change) and use an explicit wait for that condition with a sensible timeout.

</details>

### Q68. Chrome windows keep piling up on the build server after test runs. What's wrong? `Easy` · Scenario

<details>
<summary><b>Show answer</b></summary>

Tests aren't calling `driver.quit()` when they fail, usually because `quit()` is at the end of the test instead of in `finally` or `@AfterEach`. Move browser clean-up into `@AfterEach` in `BaseTest`, so it runs for every test, pass or fail.

</details>

### Q69. After a test handles a new tab, the following steps act on the wrong page. Why? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Selenium sends commands to one window at a time. After working in the new tab (and perhaps closing it), the test didn't **switch back** to the original window, or switched to the wrong handle by assuming an order. Save the original handle first, find the new one by difference, and switch back explicitly.

</details>

### Q70. How would you test that a product list is sorted correctly after choosing "Price (low to high)"? `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Choose the option with `Select.selectByVisibleText(...)`, read all prices (`findElements` on the price elements, convert "$7.99" to `BigDecimal`), make a sorted copy in Java, and assert the list equals its sorted copy. Also assert the first and last products for readability. Compare numbers, not strings, so "$15.99" vs "$7.99" sorts correctly.

</details>

### Q71. You are asked to automate a page that shows a CAPTCHA on login. What do you do? `Hard` · Scenario

<details>
<summary><b>Show answer</b></summary>

CAPTCHAs are designed to stop automation, so Selenium shouldn't try to solve them. Ask for a **test environment** where the CAPTCHA is disabled or uses a test key, a test user that bypasses it, or a test hook from developers. Test the CAPTCHA itself manually or in lower-level tests.

</details>

### Q72. Your manager asks: "Why not record tests with Selenium IDE instead of writing code?" `Medium` · Scenario

<details>
<summary><b>Show answer</b></summary>

Selenium IDE is good for quick experiments and demos, but recorded scripts are hard to maintain: duplicated steps, fragile locators, no page objects, limited assertions and reuse. Coded WebDriver tests with page objects, waits and a test framework are maintainable, run in CI and scale to large suites. IDE can still help explore a page or produce a first draft.

</details>
