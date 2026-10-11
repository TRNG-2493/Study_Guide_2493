# Weekly Knowledge Check: Week6-Selenium-BDD

Practice quiz for Week 6 (Selenium and BDD): 271 questions, over 50 per day. Every answer is supported by the written lessons in `written/1-monday` to `written/5-friday`. Try each question first, then click **Click for Solution**.

Each day is split into four parts: multiple choice, true/false, code prediction, fill-in-the-blank. Because a day has two sets of questions, the part headings repeat inside a day: part 1 covers the first lessons of the day, part 2 the rest.

---

## Day 1 - Monday: Selenium WebDriver

#### Set 1 of 2

**Part A: Multiple Choice**

### 1. Which component of the Selenium architecture receives standard WebDriver protocol requests and converts them into commands that one specific browser understands?
- [ ] A) The Selenium client library (language bindings)
- [ ] B) The browser driver (for example `chromedriver`)
- [ ] C) The W3C WebDriver specification
- [ ] D) The `WebElement` object

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The browser driver (for example `chromedriver`)

**Explanation:** The driver is a small local HTTP server that speaks the standard protocol on one side and the browser's own native automation commands on the other, acting as a translator. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - A) The client library translates Java calls into HTTP requests; it does not talk to the browser's native automation.
  - C) The specification is the shared language between layers, not a program that performs conversion.
  - D) A `WebElement` only holds a reference ID issued by the browser.
</details>

---

### 2. What does a `WebElement` object actually hold after `driver.findElement(...)` succeeds?
- [ ] A) A full copy of the element's HTML that stays valid after page changes
- [ ] B) The `By` locator, which is re-evaluated on every action
- [ ] C) A live Java object that is the DOM node itself
- [ ] D) A unique element reference ID that the browser issued

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A unique element reference ID that the browser issued

**Explanation:** A `WebElement` is like a luggage claim ticket: each action sends the ID back to the browser. If the element disappears, the ID goes stale and `StaleElementReferenceException` is thrown. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - A) It is not a copy of the HTML; it is only a reference.
  - B) The locator is not stored and re-run; the stored ID is why stale references can occur.
  - C) The DOM node lives inside the browser; Java only holds the ID.
</details>

---

### 3. A CI build fails with `java.net.ConnectException: Connection refused` when the test calls `driver.get(...)`. Which cause fits the architecture best?
- [ ] A) Nobody is listening on the driver's port, for example the driver process died or `quit()` was already called on that driver
- [ ] B) The element is not on the page yet, so a wait is needed
- [ ] C) The XPath expression has an unbalanced bracket
- [ ] D) The page URL is missing `https://`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Nobody is listening on the driver's port, for example the driver process died or `quit()` was already called on that driver

**Explanation:** `ConnectException` is a plain network error: the client library tried to reach the driver's HTTP server and nobody answered. Typical causes are a crashed driver, a firewall, or a shared driver variable that was already quit. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - B) A missing element produces `NoSuchElementException`, which means the driver did answer.
  - C) A malformed XPath gives an invalid selector error, not a connection error.
  - D) A missing protocol gives `InvalidArgumentException` from the driver, which requires a working connection.
</details>

---

### 4. Why does professional code write `WebDriver driver = new ChromeDriver();` instead of `ChromeDriver driver = new ChromeDriver();`?
- [ ] A) Commands sent through the interface type run faster
- [ ] B) `ChromeDriver` is abstract and cannot be assigned to its own type
- [ ] C) Everything after that line uses only interface methods, so switching browser means changing one line
- [ ] D) Selenium Manager only works when the variable is typed as `WebDriver`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Everything after that line uses only interface methods, so switching browser means changing one line

**Explanation:** This is programming to an interface: the rest of the test only depends on `WebDriver`, so replacing `new ChromeDriver()` with `new FirefoxDriver()` leaves the other code untouched. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - A) The lesson gives flexibility, not speed, as the reason.
  - B) The lesson shows `ChromeDriver driver2 = new ChromeDriver();` "works, but less flexible".
  - D) Selenium Manager does not depend on the declared variable type.
</details>

---

### 5. Which HTTP request does the Java client library send when you call `driver.quit()`?
- [ ] A) `POST /session`
- [ ] B) `GET /session/{id}/title`
- [ ] C) `DELETE /session/{id}`
- [ ] D) `POST /session/{id}/element`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `DELETE /session/{id}`

**Explanation:** `quit()` removes the session, which closes all windows and ends the driver process. `DELETE` removes something, `POST` creates or triggers, `GET` reads. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - A) `POST /session` creates a session (`new ChromeDriver()`).
  - B) `GET /session/{id}/title` is `driver.getTitle()`.
  - D) `POST /session/{id}/element` is `driver.findElement(...)`.
</details>

---

### 6. Last night all 120 tests passed. This morning every test fails with `session not created: This version of ChromeDriver only supports Chrome version 124` while the browser is version 126. Nobody changed code. What is the most likely root cause?
- [ ] A) A manually pinned old driver is overriding Selenium Manager while Chrome auto-updated on the build server
- [ ] B) Selenium Manager deliberately chose a driver one version older than the browser
- [ ] C) The tests forgot to call `quit()` at the end of the previous run
- [ ] D) The page load timeout was lowered to 124 seconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A manually pinned old driver is overriding Selenium Manager while Chrome auto-updated on the build server

**Explanation:** An explicitly configured driver always wins over Selenium Manager, so a stale pinned driver breaks when the browser updates. Selenium Manager would never pick a 124 driver for a 126 browser. *(driver-configuration.md)*
- **Why others are wrong:**
  - B) Selenium Manager matches the driver to the installed browser version.
  - C) Leftover processes cause memory and port problems, not a version message.
  - D) The numbers in the message are Chrome and driver versions, not timeouts.
</details>

---

### 7. Where does Selenium Manager store the drivers it downloads so they can be reused on later runs?
- [ ] A) In `~/.m2/repository`, next to the Maven dependencies
- [ ] B) In a `drivers/` folder created inside the project root
- [ ] C) In the Java installation's `bin` folder
- [ ] D) In a cache folder such as `~/.cache/selenium` (Windows: `%USERPROFILE%\.cache\selenium`)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) In a cache folder such as `~/.cache/selenium` (Windows: `%USERPROFILE%\.cache\selenium`)

**Explanation:** Selenium Manager downloads the driver on first use and reuses the cached copy afterwards. The folder also holds `se-metadata.json`. *(driver-configuration.md)*
- **Why others are wrong:**
  - A) `~/.m2/repository` is where Maven caches `selenium-java` and its dependencies, not drivers.
  - B) A `drivers/` folder is only used for manually managed drivers.
  - C) The lessons never place drivers in the Java installation.
</details>

---

### 8. When is `ChromeDriverService.Builder` a better choice than setting the `webdriver.chrome.driver` system property?
- [ ] A) Whenever Selenium Manager is enabled
- [ ] B) When you need per-instance control, such as a specific executable, port or log file
- [ ] C) When you want the page to load faster
- [ ] D) When you want the browser to run without a visible window

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) When you need per-instance control, such as a specific executable, port or log file

**Explanation:** A system property is global and affects every `ChromeDriver` created afterwards, while a service describes one driver process and can set the port or log file. *(driver-configuration.md)*
- **Why others are wrong:**
  - A) The service is a manual configuration; it is not tied to Selenium Manager being enabled.
  - C) The service configures the driver process, not page load speed.
  - D) Headless mode is a browser option, not a driver service setting.
</details>

---

### 9. In `DriverFactory.createDriver`, the `default` branch throws `IllegalArgumentException` with a message listing the valid browsers. What is the main benefit of this design?
- [ ] A) It lets the factory fall back to Chrome silently
- [ ] B) It makes the `switch` statement run faster
- [ ] C) It fails fast on typos such as `"crome"` with a clear message instead of starting the wrong browser or hitting an error later
- [ ] D) It makes Selenium Manager download all three drivers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It fails fast on typos such as `"crome"` with a clear message instead of starting the wrong browser or hitting an error later

**Explanation:** Throwing immediately names the valid choices and no browser window opens, so the typo is easy to spot. *(driver-configuration.md)*
- **Why others are wrong:**
  - A) A silent fallback would hide the typo, the opposite of fail-fast.
  - B) Performance of the `switch` is not the point.
  - D) The factory only creates the browser that was asked for.
</details>

---

### 10. A test passes on a developer laptop but fails only on the build server with `ElementNotInteractableException`. Printing `driver.manage().window().getSize()` on the server shows 800 x 600. What is the most likely explanation?
- [ ] A) The locator uses an absolute XPath
- [ ] B) `getCurrentUrl()` was read before navigation finished
- [ ] C) The page load strategy is set to `eager`
- [ ] D) The small default window made the site switch to a compact layout that hides the needed element

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The small default window made the site switch to a compact layout that hides the needed element

**Explanation:** Responsive sites change which elements are displayed at different sizes, and servers often start browsers at 800 x 600. The fix is to set the size explicitly at the start of every test. *(navigation-methods.md)*
- **Why others are wrong:**
  - A) An absolute XPath would fail on all machines after a layout change, not only on CI with a small window.
  - B) A stale URL read gives wrong URL checks, not a hidden-element error on one machine.
  - C) Nothing in the scenario points to the load strategy.
</details>

---

### 11. A tester writes `driver.findElement(By.className("btn btn_primary"))`. What happens, and what is the recommended fix?
- [ ] A) `InvalidSelectorException`; use `By.cssSelector(".btn.btn_primary")`
- [ ] B) It matches elements that have either class; no fix is needed
- [ ] C) It silently returns the first element that has both classes
- [ ] D) `NoSuchElementException`; switch to `By.linkText`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `InvalidSelectorException`; use `By.cssSelector(".btn.btn_primary")`

**Explanation:** `By.className` accepts a single class name and rejects compound names (spaces), reporting "Compound class names not permitted". Two classes are combined in CSS as `.a.b`. *(locator-strategies.md)*
- **Why others are wrong:**
  - B) A space is not treated as "either"; the locator is rejected.
  - C) There is no silent match; Selenium cannot parse the locator.
  - D) The problem is an invalid selector, and `linkText` works only on `<a>` elements.
</details>

---

### 12. Which task can XPath do that CSS selectors cannot?
- [ ] A) Match an attribute that starts with a given prefix
- [ ] B) Match an element by its visible text
- [ ] C) Select a direct child with `>`
- [ ] D) Select the sibling that follows an element

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Match an element by its visible text

**Explanation:** CSS has no real `:contains()` for visible text and no practical "go to parent" operator, so XPath (`text()`, `contains()`, `..`) is used for those needs. *(locator-strategies.md)*
- **Why others are wrong:**
  - A) CSS does this with `[id^='user']`.
  - C) `form > div` is a direct-child selector in CSS.
  - D) CSS supports `+` and `~` for following siblings.
</details>

---

### 13. According to the recommended priority order for choosing locators, which option is the last resort?
- [ ] A) Relative XPath to search by visible text
- [ ] B) A unique `name` attribute
- [ ] C) A short CSS selector using meaningful attributes
- [ ] D) Positional locators such as `[3]` or `nth-child`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Positional locators such as `[3]` or `nth-child`

**Explanation:** The order is stable `id`/`data-test`, unique `name`, concise CSS, relative XPath, and finally positional locators, which break easily when the layout changes. *(locator-strategies.md)*
- **Why others are wrong:**
  - A) Relative XPath is step 4, used when text or parent/sibling navigation is needed.
  - B) A unique `name` is step 2.
  - C) A short CSS selector is step 3.
</details>

---

**Part B: True/False**

### 14. True or False: Selenium WebDriver decides by itself whether a test has passed or failed.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Selenium only drives the browser the way a user would. It is not a test framework, so you must add assertions and a runner such as JUnit to decide pass or fail. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - A) This is the misconception listed in the common mistakes: expecting Selenium to judge results.
</details>

---

### 15. True or False: After `driver.quit()` has been called, calling `driver.get(...)` on the same driver object throws an exception because the session no longer exists.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** After `quit()` the driver object is dead: the session ID no longer exists on the driver side, so later requests are rejected (for example `NoSuchSessionException`). A new driver must be created for a fresh browser. *(driver-configuration.md)*
- **Why others are wrong:**
  - B) Believing the object can be reused after `quit()` is the misconception; the session has ended.
</details>

---

### 16. True or False: Creating a locator such as `By.id("login-button")` does not contact the browser; the search happens only when the `By` is passed to `findElement` or `findElements`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** A `By` is only a description of how to find an element. The actual search, and any `NoSuchElementException`, happens at the `findElement` call. *(locator-strategies.md)*
- **Why others are wrong:**
  - B) Thinking the `By` constructor searches the page would suggest an exception at declaration time, which does not happen.
</details>

---

### 17. True or False: `url.contains("inventory")` is the best way to verify the landing page across environments, because it is exact about the page and independent of the host name.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `contains` is a loose check with a risk of false positives such as `/inventory-error`. The lesson recommends `endsWith("/inventory.html")`, which is exact about the page yet independent of the host name. *(navigation-methods.md)*
- **Why others are wrong:**
  - A) The "exact yet host-independent" description belongs to `endsWith`, not `contains`.
</details>

---

**Part C: Code Prediction**

### 18. What does this program print?
```java
WebDriver first  = new ChromeDriver();
WebDriver second = new ChromeDriver();
first.get("https://www.saucedemo.com");
second.get("https://the-internet.herokuapp.com");
first.quit();
System.out.println(second.getTitle());
```
- [ ] A) It throws `NoSuchSessionException`, because `quit()` ends every browser
- [ ] B) `Swag Labs`
- [ ] C) `The Internet`
- [ ] D) `null`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `The Internet`

**Explanation:** Two `ChromeDriver` objects mean two driver processes, two browsers and two different session IDs. Commands sent to one never affect the other, so quitting `first` leaves `second` working. *(selenium-webdriver-architecture.md)*
- **Why others are wrong:**
  - A) `quit()` ends only the session of the driver object it is called on.
  - B) `Swag Labs` is the title of the page loaded in `first`.
  - D) `getTitle()` returns the page title text, not `null`.
</details>

---

### 19. Using the `DriverFactory` from the lesson (classic `switch` on `browserName.trim().toLowerCase()`), what happens when this line runs?
```java
WebDriver driver = DriverFactory.createDriver("safari");
```
- [ ] A) An `IllegalArgumentException` is thrown with the message `Unsupported browser: 'safari'. Use chrome, firefox or edge.`, and no browser window opens
- [ ] B) A `SafariDriver` starts if the machine runs macOS
- [ ] C) The method returns `null`
- [ ] D) The factory falls through to the `chrome` case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) An `IllegalArgumentException` is thrown with the message `Unsupported browser: 'safari'. Use chrome, firefox or edge.`, and no browser window opens

**Explanation:** The factory only has cases for chrome, firefox and edge, so `"safari"` reaches `default`, which throws before any browser is started. *(driver-configuration.md)*
- **Why others are wrong:**
  - B) The factory has no Safari case; supporting it would require code changes.
  - C) The `default` branch throws; it never returns `null`.
  - D) Each case returns on its own and nothing falls through to `chrome`.
</details>

---

### 20. On the SauceDemo login page (inputs: username, password, login button; username and password share the class `form_input`), what is printed?
```java
System.out.println(driver.findElements(By.id("user-name")).size());
System.out.println(driver.findElements(By.className("form_input")).size());
System.out.println(driver.findElements(By.tagName("input")).size());
```
- [ ] A) `1`, `1`, `3`
- [ ] B) `1`, `2`, `2`
- [ ] C) `0`, `2`, `3`
- [ ] D) `1`, `2`, `3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1`, `2`, `3`

**Explanation:** The id is unique (1). The class `form_input` is shared by the username and password boxes (2). The page has three `<input>` elements: username, password and the login button (3). *(locator-strategies.md)*
- **Why others are wrong:**
  - A) The class is shared by two inputs, not one.
  - B) The login button is also an `<input>`, so the tag count is three.
  - C) The id `user-name` exists, so the first count is 1.
</details>

---

### 21. Reading the XPath, which element does this locator return on the SauceDemo inventory page?
```java
By.xpath("//div[text()='Sauce Labs Backpack']"
       + "/ancestor::div[@class='inventory_item']//button")
```
- [ ] A) The first button anywhere on the page
- [ ] B) The button inside the same product card as "Sauce Labs Backpack"
- [ ] C) The `div` whose text is "Sauce Labs Backpack"
- [ ] D) The button of the last product in the list

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The button inside the same product card as "Sauce Labs Backpack"

**Explanation:** The XPath finds the product-name div, climbs up with `ancestor::` to the `inventory_item` card, then goes down with `//button`, so it works wherever the Backpack sits in the list. *(locator-strategies.md)*
- **Why others are wrong:**
  - A) The expression is anchored on the product name, not on page order.
  - C) That div is only the starting point; the expression continues to a button.
  - D) The product name chooses the card, not its position in the list.
</details>

---

### 22. What happens with this code on a page that has several `<input>` elements?
```java
driver.findElement(By.xpath("//input[0]"));
```
- [ ] A) It returns the first `input`
- [ ] B) It returns the last `input`
- [ ] C) It throws `NoSuchElementException`, because XPath indexes start at 1 and nothing matches
- [ ] D) It returns a list of all inputs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It throws `NoSuchElementException`, because XPath indexes start at 1 and nothing matches

**Explanation:** The lesson lists "forgetting XPath is 1-based" as a mistake: `//input[0]` matches nothing, and `findElement` throws `NoSuchElementException` when there is no match. *(locator-strategies.md)*
- **Why others are wrong:**
  - A) The first element is `[1]`, not `[0]`.
  - B) Index 0 does not mean "last".
  - D) `findElement` returns a single `WebElement`, never a list.
</details>

---

### 23. Using the history model from the lesson, what is printed by the last line?
```java
driver.get("https://the-internet.herokuapp.com/");                 // A
driver.navigate().to("https://the-internet.herokuapp.com/login");        // B
driver.navigate().to("https://the-internet.herokuapp.com/checkboxes");   // C
driver.navigate().back();
driver.navigate().back();
driver.navigate().to("https://the-internet.herokuapp.com/dropdown");     // D
driver.navigate().forward();
System.out.println(driver.getCurrentUrl());
```
- [ ] A) `https://the-internet.herokuapp.com/checkboxes`
- [ ] B) `https://the-internet.herokuapp.com/dropdown`
- [ ] C) `https://the-internet.herokuapp.com/login`
- [ ] D) `https://the-internet.herokuapp.com/`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `https://the-internet.herokuapp.com/dropdown`

**Explanation:** Two `back()` calls return to page A. Navigating to D then erases the forward pages (B and C), so `forward()` does nothing and the browser stays on `/dropdown`. *(navigation-methods.md)*
- **Why others are wrong:**
  - A) `/checkboxes` was erased from the forward history by the new navigation.
  - C) `/login` was also erased from the forward history.
  - D) The browser left `/` when it navigated to `/dropdown`; `forward()` cannot return there.
</details>

---

### 24. Which exception does this code throw?
```java
WebElement heading = driver.findElement(By.tagName("h1"));
driver.navigate().refresh();
System.out.println(heading.getText());
```
- [ ] A) `NoSuchElementException`
- [ ] B) `NoSuchSessionException`
- [ ] C) `TimeoutException`
- [ ] D) `StaleElementReferenceException`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `StaleElementReferenceException`

**Explanation:** `refresh()` throws the DOM away and builds a new one, so the old element reference ID points at nothing. The fix is to find the element again after the refresh. *(navigation-methods.md)*
- **Why others are wrong:**
  - A) That would come from a `findElement` that matches nothing, not from using an old reference.
  - B) The session is still alive after a refresh.
  - C) `TimeoutException` relates to the page load timeout, not to an old reference.
</details>

---

**Part D: Fill-in-the-Blank**

### 25. The W3C WebDriver protocol is a REST-style API that sends JSON over _____ between the client library and the browser driver.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `HTTP` (also accepted: `HTTPS`, `HTTP requests`)

**Explanation:** Every Selenium command is an HTTP request (such as `POST /session/{id}/url`) to the driver's local web server, which is why drivers can even run on different machines from the tests. *(selenium-webdriver-architecture.md)*
</details>

---

### 26. To tell Selenium manually where chromedriver is, you set the Java system property named `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `webdriver.chrome.driver` (also accepted: `"webdriver.chrome.driver"`)

**Explanation:** This is the exact name Selenium looks up for the chromedriver path; a misspelled name is silently ignored. The Firefox and Edge equivalents are `webdriver.gecko.driver` and `webdriver.edge.driver`. *(driver-configuration.md)*
</details>

---

### 27. When you type a locator into the Chrome DevTools search box and it shows "1 of 5", the locator matches five elements and is therefore not _____.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `unique` (also accepted: `a unique match`, `unambiguous`, `specific`)

**Explanation:** "1 of 1" means exactly one match. With "1 of 5", `findElement` silently returns the first match, which may not be the element you meant. *(locator-strategies.md)*
</details>

---

### 28. If a page never finishes loading, `driver.get()` waits until the page load timeout, whose default is _____ seconds, and then throws a `TimeoutException`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `300` (also accepted: `300 s`, `5 minutes`, `five minutes`)

**Explanation:** The default page load timeout is 300 seconds; it can be shortened with `driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30))`. *(navigation-methods.md)*
</details>

---

#### Set 2 of 2

**Part A: Multiple Choice**

### 29. A page has three buttons that all share the class `btn`. What does `driver.findElement(By.className("btn"))` return?
- [ ] A) It throws `NoSuchElementException` because the locator is ambiguous
- [ ] B) The last matching element in document order
- [ ] C) The first matching element in document order, with no warning
- [ ] D) A `List<WebElement>` holding all three buttons

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The first matching element in document order, with no warning

**Explanation:** `findElement` returns only the first match (top to bottom in the DOM) and stays silent about the others, which is why non-unique locators cause hidden bugs. *(find-methods.md)*
- **Why others are wrong:**
  - A) The exception is only thrown when nothing matches.
  - B) It is the first match, not the last.
  - D) A list is what the plural `findElements` returns, not `findElement`.
</details>

---

### 30. A text box already contains `abc`. The test calls `box.sendKeys("xyz");` immediately, without any other call. What does the box contain afterwards?
- [ ] A) `abcxyz`
- [ ] B) `xyz`
- [ ] C) `abc`
- [ ] D) `xyzabc`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `abcxyz`

**Explanation:** `sendKeys` simulates typing and appends to whatever is already in the box, so `clear()` must be called first if only the new text is wanted. *(find-methods.md)*
- **Why others are wrong:**
  - B) That would only happen if `clear()` ran first.
  - C) `sendKeys` does type the new text; it is not ignored.
  - D) Typing happens at the end of existing content, not at the start.
</details>

---

### 31. In the browser console `$("#login-button")` finds the button, yet the test throws `NoSuchElementException` for `By.id("login-button")`. Which cause fits this situation?
- [ ] A) Selenium 4 no longer supports `By.id`
- [ ] B) DevTools can only find elements that are hidden from users
- [ ] C) The test must always contain a permanent `Thread.sleep` before every `findElement`
- [ ] D) The element sits inside an `<iframe>`, or an earlier step left the test on a different page than expected

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The element sits inside an `<iframe>`, or an earlier step left the test on a different page than expected

**Explanation:** The lesson lists wrong context (iframe/window) and wrong page among the common causes; printing `getCurrentUrl()` and checking for `<iframe>` ancestors in DevTools diagnoses them. *(find-methods.md)*
- **Why others are wrong:**
  - A) `By.id` is supported; Selenium even translates it into a CSS selector `[id="..."]`.
  - B) DevTools has no such limitation.
  - C) `Thread.sleep` is only a temporary experiment to test a timing theory and must never be left in real tests.
</details>

---

### 32. A test stores `WebElement btn` before the page reloads, and `btn.click()` afterwards throws `StaleElementReferenceException`. What is the correct fix?
- [ ] A) Wrap the click in a `try/catch` and ignore the exception
- [ ] B) Find the element again after the reload and click the new reference
- [ ] C) Replace `findElement` with `findElements` for the stored variable
- [ ] D) Call `isDisplayed()` on the old reference first

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Find the element again after the reload and click the new reference

**Explanation:** A `WebElement` is a reference to one element in the DOM; when the page reloads or the DOM section is rebuilt the reference goes stale, so you must re-find it and not keep variables across page changes. *(find-methods.md)*
- **Why others are wrong:**
  - A) Ignoring the exception means the click never happens, hiding the problem.
  - C) A list of old references would be stale in the same way.
  - D) Checking state on a stale reference also fails because it no longer points to anything in the page.
</details>

---

### 33. A company laptop has an outdated Chrome that you may not update, but Chrome Beta is installed in another folder and you want to test with it. What should you use?
- [ ] A) `options.addArguments("--chrome-beta")`
- [ ] B) `options.setPageLoadStrategy(PageLoadStrategy.EAGER)`
- [ ] C) `options.setBinary("<path to the Beta chrome executable>")`
- [ ] D) Run Maven with `-Dbrowser=beta` and rely on the factory

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `options.setBinary("<path to the Beta chrome executable>")`

**Explanation:** `setBinary` points the session at a non-default browser executable, and Selenium Manager then matches the driver to that binary's version. *(browser-options.md)*
- **Why others are wrong:**
  - A) That is not a documented switch; and unknown switches are silently ignored.
  - B) Page load strategy only changes when `get()` returns, not which browser starts.
  - D) The factory's `switch` only knows chrome, firefox and edge, so `beta` would throw `IllegalArgumentException`.
</details>

---

### 34. A page's own content appears quickly, but `driver.get()` takes very long because of slow advertisement and tracking scripts. Which page load strategy is the suggested fix?
- [ ] A) `NORMAL`, because it waits for every resource
- [ ] B) `NONE`, because it needs no extra waiting code
- [ ] C) `NORMAL` with a page load timeout of ten minutes
- [ ] D) `EAGER`, which returns once the DOM is ready

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `EAGER`, which returns once the DOM is ready

**Explanation:** `EAGER` returns at `DOMContentLoaded`, so slow third-party resources no longer delay `get()`. *(browser-options.md)*
- **Why others are wrong:**
  - A) Waiting for every resource (the `load` event) is exactly what causes the delay.
  - B) `NONE` returns immediately after navigation starts, so you must add your own waits; it is advanced and not recommended before learning waits.
  - C) A longer timeout only lets the test wait longer; it does not shorten the load.
</details>

---

### 35. Why does a download setup include the preference `download.prompt_for_download` set to `false`?
- [ ] A) The "Save as" prompt is an operating-system dialog Selenium cannot control, so files must go straight to the folder
- [ ] B) It compresses downloaded files to save disk space
- [ ] C) It is required for the browser to start in headless mode
- [ ] D) It makes Chrome open every download in a new tab

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The "Save as" prompt is an operating-system dialog Selenium cannot control, so files must go straight to the folder

**Explanation:** The Save-as dialog is not a web page, so Selenium cannot interact with it; disabling the prompt saves files directly to `download.default_directory`. *(browser-options.md)*
- **Why others are wrong:**
  - B) The preference has nothing to do with compression.
  - C) Headless mode is selected with an argument, not with this preference.
  - D) It controls the prompt only, not how downloads are displayed.
</details>

---

### 36. A test passes headed but throws `NoSuchElementException` for the cart link only in headless mode. Printing `driver.manage().window().getSize()` shows `(800, 600)`. What is the best fix?
- [ ] A) Call `driver.manage().window().maximize()`
- [ ] B) Add `--no-sandbox`
- [ ] C) Add `--window-size=1920,1080`
- [ ] D) Add `--incognito`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Add `--window-size=1920,1080`

**Explanation:** The small default headless window triggers a mobile layout that hides the cart link; setting an explicit window size restores the desktop layout. *(browser-options.md)*
- **Why others are wrong:**
  - A) `maximize()` does nothing in headless mode because there is no display.
  - B) `--no-sandbox` is for certain Linux/Docker environments and is unrelated to layout.
  - D) `--incognito` gives a clean state but does not change window size.
</details>

---

### 37. A staging site uses a self-signed HTTPS certificate, so Chrome shows "Your connection is not private" and the `findElement` calls fail. Which is the preferred, cross-browser way to proceed?
- [ ] A) `options.addArguments("--disable-extensions")`
- [ ] B) `options.setAcceptInsecureCerts(true)`
- [ ] C) `options.setBinary(...)`
- [ ] D) `options.addArguments("--lang=en-US")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `options.setAcceptInsecureCerts(true)`

**Explanation:** `setAcceptInsecureCerts(true)` is the W3C standard capability and works the same in Firefox; `--ignore-certificate-errors` is the Chrome/Edge-specific alternative. Use it only for test environments. *(browser-options.md)*
- **Why others are wrong:**
  - A) Extensions are unrelated to certificate warnings.
  - C) The binary path selects which browser executable is used, not certificate handling.
  - D) The language switch only affects the UI language.
</details>

---

### 38. Why must you cast a `WebDriver` variable to `TakesScreenshot` before taking a screenshot?
- [ ] A) The cast turns the driver into a headless driver
- [ ] B) The cast converts the returned `File` into a `byte[]`
- [ ] C) `getScreenshotAs` is a private method of `ChromeDriver`
- [ ] D) The ability lives in a separate interface that `WebDriver` does not declare

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The ability lives in a separate interface that `WebDriver` does not declare

**Explanation:** Optional abilities are placed in extra interfaces; `ChromeDriver`, `FirefoxDriver` and `EdgeDriver` implement `TakesScreenshot`, and the cast just views the same object through that interface. *(screenshots.md)*
- **Why others are wrong:**
  - A) A cast changes how the object is viewed, not its mode.
  - B) The result type is chosen by `OutputType`, not by the cast.
  - C) The method belongs to the public `TakesScreenshot` interface.
</details>

---

### 39. A failure listener tries to take a screenshot and gets `NoSuchSessionException: invalid session id`. The base class closes the browser in another method. What is the likely cause?
- [ ] A) Headless Chrome cannot take screenshots
- [ ] B) The screenshot file name contained invalid characters
- [ ] C) `driver.quit()` ran before the screenshot, so no browser session exists
- [ ] D) The timestamp pattern used `mm` instead of `MM`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `driver.quit()` ran before the screenshot, so no browser session exists

**Explanation:** A picture needs a living browser; capture first and call `quit()` last. *(screenshots.md)*
- **Why others are wrong:**
  - A) Headless runs can take screenshots (window size is the issue to watch).
  - B) Bad file names cause save problems, not an invalid session id.
  - D) A wrong pattern only produces odd file names.
</details>

---

### 40. You want one self-contained HTML report that can be emailed as a single file with the screenshot embedded in an `<img>` tag. Which `OutputType` fits best?
- [ ] A) `OutputType.BASE64`
- [ ] B) `OutputType.FILE`
- [ ] C) `OutputType.BYTES`
- [ ] D) `getFullPageScreenshotAs`, which is a method rather than an `OutputType`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `OutputType.BASE64`

**Explanation:** Base64 is plain text, so it can be placed in `<img src="data:image/png;base64,...">` without a separate image file. *(screenshots.md)*
- **Why others are wrong:**
  - B) `FILE` gives a temporary file on disk, which makes the report depend on a separate image file.
  - C) `BYTES` is raw binary data for report libraries and cannot be put directly into an HTML `src` string.
  - D) It is a Firefox-only way to capture the entire page, not a format for embedding.
</details>

---

**Part B: True/False**

### 41. True or False: If `driver.findElements(By.id("banner")).isEmpty()` is `false`, the banner is guaranteed to be visible to the user.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A non-empty list only proves the element is present in the DOM. It may still be hidden (for example `display:none`); visibility needs `isDisplayed()`, like a spare tyre that is present in the boot but not displayed. *(find-methods.md)*
- **Why others are wrong:**
  - A) This confuses "present" with "displayed", a misconception that leads to asserting on hidden elements.
</details>

---

### 42. True or False: `options.setExperimentalOption("excludeSwitches", new String[]{"enable-automation"})` removes the "controlled by automated test software" bar, and it is cosmetic and optional.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** By default Selenium launches Chrome with the `enable-automation` switch that shows the bar; excluding it tidies your own test runs, but it is optional and should not be used to hide automation from sites you do not own. *(browser-options.md)*
- **Why others are wrong:**
  - B) Believing the line is mandatory or that it does nothing are both wrong; it removes that switch and the bar.
</details>

---

### 43. True or False: `getScreenshotAs(OutputType.FILE)` returns a permanent file in your project folder, so copying it with `Files.copy` is unnecessary.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `OutputType.FILE` writes to a temporary file in the system's temp folder that may be deleted later, so you copy it to your own folder to keep it. *(screenshots.md)*
- **Why others are wrong:**
  - A) The misconception is assuming the returned file is already saved where you want it; it is only temporary.
</details>

---

### 44. True or False: A default Selenium screenshot captures only the visible viewport of the current tab, not the browser's address bar or tabs.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The default capture is the visible viewport, so content below the fold and browser chrome are not included. *(screenshots.md)*
- **Why others are wrong:**
  - B) Expecting the whole scrollable page or the browser window frame is the misconception; full-page capture needs extra work (Firefox's method, a taller window, or DevTools).
</details>

---

**Part C: Code Prediction**

### 45. SauceDemo's login button is `<input type="submit" id="login-button" value="Login">`. What does this code print?
```java
WebElement btn = driver.findElement(By.id("login-button"));
System.out.println("[" + btn.getText() + "]" + btn.getAttribute("value"));
```
- [ ] A) `[Login]Login`
- [ ] B) `[]`
- [ ] C) `[submit]Login`
- [ ] D) `[]Login`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `[]Login`

**Explanation:** An `<input>` has no text content, so `getText()` returns an empty string, while its label is stored in the `value` attribute that `getAttribute("value")` reads. *(find-methods.md)*
- **Why others are wrong:**
  - A) `getText()` would only return `Login` for a `<button>Login</button>`.
  - B) The second part of the concatenation still prints `Login`.
  - C) `submit` is the `type` attribute, not the text.
</details>

---

### 46. What does this loop do on the inventory page?
```java
List<WebElement> cards = driver.findElements(By.className("inventory_item"));
for (WebElement card : cards) {
    System.out.println(card.findElement(By.xpath("//button")).getText());
}
```
- [ ] A) Every pass searches the whole document, so it returns the first button on the page each time
- [ ] B) Each pass returns the button that belongs to the current card
- [ ] C) The second pass throws `NoSuchElementException`
- [ ] D) It fails to compile because `card` has no `findElement`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Every pass searches the whole document, so it returns the first button on the page each time

**Explanation:** An XPath starting with `//` searches from the document root even inside a scoped search; it needs `.//` to be relative to the card. *(find-methods.md)*
- **Why others are wrong:**
  - B) That is what `.//button` would do.
  - C) Buttons exist on the page, so the search succeeds each time.
  - D) `WebElement` has its own `findElement` (via `SearchContext`).
</details>

---

### 47. What happens when this code runs?
```java
ChromeOptions options = new ChromeOptions();
options.addArguments("--incognito", "--window-size=1280,720");
WebDriver driver = new ChromeDriver();
```
- [ ] A) Chrome starts incognito but with its default window size
- [ ] B) Chrome starts with neither argument applied, and no error is shown
- [ ] C) An `IllegalArgumentException` is thrown
- [ ] D) The code does not compile

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Chrome starts with neither argument applied, and no error is shown

**Explanation:** Options only take effect when passed to the constructor; `new ChromeDriver()` with empty parentheses silently ignores everything set on `options`. *(browser-options.md)*
- **Why others are wrong:**
  - A) No part of the options is applied, including `--incognito`.
  - C) Nothing validates the unused object, so no exception occurs.
  - D) The code is valid Java; the problem is logical, not syntactic.
</details>

---

### 48. A pipeline runs `mvn test -Dbrowser=opera`. The code is:
```java
String browser = System.getProperty("browser", "chrome");
WebDriver driver = DriverFactory.createDriver(browser, false);
```
The factory's `switch` has cases for chrome, firefox and edge, and a `default` that throws. What happens?
- [ ] A) Chrome launches because it is the default
- [ ] B) `createDriver` returns `null` and a `NullPointerException` appears later
- [ ] C) A `SessionNotCreatedException` is thrown by `chromedriver`
- [ ] D) An `IllegalArgumentException` with the message `Unsupported browser: opera`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) An `IllegalArgumentException` with the message `Unsupported browser: opera`

**Explanation:** The `default` branch fails fast with a clear message instead of returning `null`; the `chrome` default of `getProperty` only applies when no `-Dbrowser` is given. *(browser-options.md)*
- **Why others are wrong:**
  - A) The default value is used only when the property is absent, and here it is set to `opera`.
  - B) Failing fast avoids exactly this confusing later `NullPointerException`.
  - C) No driver is started at all for an unsupported name.
</details>

---

### 49. What file-name stem does this produce?
```java
String name = "Login with \"wrong\" password?";
String safe = name.replaceAll("[^a-zA-Z0-9-_]", "_");
```
- [ ] A) `Login with "wrong" password?`
- [ ] B) `Login_with_wrong_password`
- [ ] C) `Login_with__wrong__password_`
- [ ] D) `Login_with__wrong__password?`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Login_with__wrong__password_`

**Explanation:** The `^` inside `[...]` means "not", so every character that is not a letter, digit, hyphen or underscore (spaces, quotes, the question mark) becomes one underscore each. *(screenshots.md)*
- **Why others are wrong:**
  - A) That is the unchanged input; the regex replaces the invalid characters.
  - B) Each replaced character becomes its own underscore; none are dropped, so the double underscores remain.
  - D) The question mark is also not allowed and is replaced.
</details>

---

### 50. What is the outcome of this test code when the element does not exist?
```java
try {
    driver.findElement(By.id("does-not-exist"));
} catch (Exception e) {
    ScreenshotUtil.capture(driver, "checkoutTest_FAILED");
} finally {
    driver.quit();
}
```
- [ ] A) The test is reported as failed with `NoSuchElementException`
- [ ] B) A screenshot is saved, but the swallowed exception makes the test appear to pass
- [ ] C) `NoSuchSessionException` occurs because `quit()` runs before the `catch`
- [ ] D) No screenshot is saved because `finally` runs first

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A screenshot is saved, but the swallowed exception makes the test appear to pass

**Explanation:** The `catch` captures the picture but never rethrows, so the failure is hidden; `throw e;` is required. *(screenshots.md)*
- **Why others are wrong:**
  - A) Without a rethrow the exception does not leave the `catch`.
  - C) `finally` runs after the `catch`, so the browser is still open during capture.
  - D) `finally` always runs last, after the `catch` block.
</details>

---

### 51. Given the two overloads `capture(WebDriver driver, String name)` and `capture(WebElement element, String name)` in `ScreenshotUtil`, what happens here?
```java
WebElement logo = driver.findElement(By.className("login_logo"));
Path p = ScreenshotUtil.capture(logo, "02_logo");
```
- [ ] A) The viewport overload runs and the element is cast to a driver
- [ ] B) The call is ambiguous and does not compile
- [ ] C) The element overload runs and the image is cropped to the logo
- [ ] D) `UnsupportedOperationException` is thrown because an element cannot take screenshots

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The element overload runs and the image is cropped to the logo

**Explanation:** Java picks the overload from the argument type; the `WebElement` version calls `element.getScreenshotAs`, which crops to the element's bounds. *(screenshots.md)*
- **Why others are wrong:**
  - A) A `WebElement` is not a `WebDriver`, so that overload is not chosen.
  - B) The parameter types differ, so only one overload matches.
  - D) That exception is only thrown by the driver overload when the driver lacks `TakesScreenshot`; `WebElement` has `getScreenshotAs` itself.
</details>

---

**Part D: Fill-in-the-Blank**

### 52. Both `WebDriver` and `WebElement` implement the _____ interface, which is why each one has `findElement` and `findElements`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `SearchContext` (also accepted: `org.openqa.selenium.SearchContext`)

**Explanation:** `SearchContext` defines the two find methods; one searches the whole page, the other only an element's descendants. *(find-methods.md)*
</details>

---

### 53. If you never set it, the default page load timeout is _____ seconds (5 minutes), so a broken page could stall a build; 30 to 60 seconds is typical.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `300` (also accepted: three hundred)

**Explanation:** The default of 300 seconds is far too long for tests, so `pageLoadTimeout` should be set explicitly. *(browser-options.md)*
</details>

---

### 54. To emulate a phone in Chrome, you put a `deviceName` in a map and call `options.setExperimentalOption("_____", mobile)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `mobileEmulation` (also accepted: mobileEmulation, case as written)

**Explanation:** The `mobileEmulation` experimental option makes the page believe it is on a phone (narrow screen, touch events, mobile user agent). *(browser-options.md)*
</details>

---

### 55. In a Java timestamp pattern such as `yyyyMMdd_HHmmss`, `MM` means month, while minutes are written with lowercase _____.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `mm` (also accepted: lowercase mm)

**Explanation:** Mixing them up puts minutes where the month should be; month is `MM`, minutes is `mm`. *(screenshots.md)*
</details>

---

## Day 2 - Tuesday: Advanced Selenium

#### Set 1 of 2

**Part A: Multiple Choice**

### 56. A test passes when run slowly in a debugger but fails on a busy build server with no code changes. What is the underlying cause?
- [ ] A) The browser driver randomly skips some commands
- [ ] B) A race condition between the test code and the page, which run independently
- [ ] C) Java evaluates locators in a different order on each run
- [ ] D) The locator is wrong, and the debugger silently corrects it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A race condition between the test code and the page, which run independently

**Explanation:** The test (JVM) and the page (browser JavaScript) do not share a clock, so whether the element exists when the test looks depends on timing. That is what makes a test flaky. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) The lesson attributes flakiness to timing, not to dropped commands.
  - C) Locator evaluation order is not mentioned and is not the cause; the code is the same each run.
  - D) A wrong locator would fail every time, not only on slow runs.
</details>

---

### 57. A suite has 200 tests, each containing three `Thread.sleep(3000)` calls. How much time is spent sleeping in one run?
- [ ] A) About 10 minutes
- [ ] B) About 20 minutes
- [ ] C) About 1 hour
- [ ] D) About 30 minutes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) About 30 minutes

**Explanation:** 200 x 3 x 3 s = 1,800 s, which is 30 minutes of pure waiting per run, even if nothing is slow. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) 10 minutes would be 600 s, which is too small.
  - B) 20 minutes would be 1,200 s; the arithmetic gives 1,800 s.
  - C) One hour would be 3,600 s, double the real total.
</details>

---

### 58. Which timeout limits how long `driver.get(url)` may wait for a page to finish loading, and what is its default?
- [ ] A) The page load timeout, 300 seconds
- [ ] B) The script timeout, 30 seconds
- [ ] C) The implicit wait, 0 seconds
- [ ] D) The explicit wait, 10 seconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The page load timeout, 300 seconds

**Explanation:** The page load timeout controls `get()`/`navigate()` and defaults to 300 s (five minutes), which the lesson calls far too long, so it is usually set once in driver setup. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) The script timeout applies to asynchronous scripts (`executeAsyncScript`).
  - C) The implicit wait governs how long `findElement(s)` retries, and is disabled by default.
  - D) An explicit wait has no default; it exists only when you create one.
</details>

---

### 59. With a 10-second implicit wait set, a tester clicks Start on `/dynamic_loading/1`, then calls `findElement(By.id("finish")).getText()`. The assertion later fails because the text is empty. Why?
- [ ] A) The implicit wait timed out after 10 seconds
- [ ] B) `getText()` cannot read text from elements found with `By.id`
- [ ] C) The element was already in the DOM but hidden, so the implicit wait was satisfied immediately
- [ ] D) The implicit wait only applies to `findElements`, not `findElement`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The element was already in the DOM but hidden, so the implicit wait was satisfied immediately

**Explanation:** Implicit waits wait for existence, not readiness. `getText()` returns only visible text, so a present-but-hidden element yields an empty string. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) If it had timed out, a `NoSuchElementException` would be thrown, not an empty string.
  - B) `getText()` works with any locator; the problem is visibility.
  - D) The implicit wait applies to both `findElement` and `findElements`.
</details>

---

### 60. An implicit wait of 10 seconds is set. What is the cost of `driver.findElements(By.id("spinner")).isEmpty()` when no spinner exists?
- [ ] A) It returns instantly because `findElements` never waits
- [ ] B) It takes the full 10 seconds before returning an empty list
- [ ] C) It throws `NoSuchElementException` after 10 seconds
- [ ] D) It takes about 500 ms, one polling interval

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It takes the full 10 seconds before returning an empty list

**Explanation:** With an implicit wait, `findElements` waits for at least one match and returns an empty list only after the timeout, so checking for absence costs the full timeout. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) `findElements` is affected by the implicit wait.
  - C) `findElements` returns an empty list; it does not throw `NoSuchElementException`.
  - D) The driver keeps retrying until the whole timeout is used up.
</details>

---

### 61. What is the default polling interval of a `WebDriverWait`?
- [ ] A) 500 milliseconds
- [ ] B) 100 milliseconds
- [ ] C) 1 second
- [ ] D) It has no default and must be configured

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 500 milliseconds

**Explanation:** `WebDriverWait` polls every 500 ms by default, and the `TimeoutException` message even reports "with 500 milliseconds interval". *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) 100 ms is something you would configure with `FluentWait` for a very quick UI.
  - C) One second is not the default.
  - D) A sensible default exists; configuring is optional.
</details>

---

### 62. A tester needs to read the value of an `<input type="hidden">` on a page. Which condition should they wait on?
- [ ] A) `visibilityOfElementLocated`
- [ ] B) `elementToBeClickable`
- [ ] C) `textToBePresentInElementLocated`
- [ ] D) `presenceOfElementLocated`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `presenceOfElementLocated`

**Explanation:** A hidden input is never visible, so only presence (existence in the DOM) can succeed. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) Visibility would always time out, since the element is never visible.
  - B) Clickable requires the element to be visible and enabled.
  - C) That waits for text inside an element, which a hidden input does not display.
</details>

---

### 63. After `elementToBeClickable(By.id("save"))` returns, `click()` still throws `ElementClickInterceptedException`. What does this tell you?
- [ ] A) Clickable only means visible and enabled; another element such as an overlay may still cover it
- [ ] B) The locator for the button is wrong
- [ ] C) The wait polled too slowly and missed the clickable state
- [ ] D) The element must have become stale during the wait

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Clickable only means visible and enabled; another element such as an overlay may still cover it

**Explanation:** Clickability does not guarantee nothing is on top of the element. The fix is to wait for the overlay to become invisible and then click. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) A wrong locator would have caused a timeout in the wait itself.
  - C) The condition was met; the problem is what is covering the button.
  - D) Staleness produces `StaleElementReferenceException`, a different exception.
</details>

---

### 64. A tester has a typo in a CSS selector and uses `wait.until(ExpectedConditions.visibilityOfElementLocated(...))` with a 10-second timeout. What happens?
- [ ] A) An `InvalidSelectorException` is thrown straight away, because it is not on the ignore list
- [ ] B) The wait keeps polling and throws `TimeoutException` after 10 seconds
- [ ] C) The wait returns `null` and the test continues
- [ ] D) The wait converts the selector error into a `NoSuchElementException` and retries

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) An `InvalidSelectorException` is thrown straight away, because it is not on the ignore list

**Explanation:** `WebDriverWait` ignores only `NotFoundException` by default. Any other exception ends the wait immediately, so you see the real problem right away. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) The wait only keeps polling for ignored exceptions.
  - C) The wait never returns null on failure; it either returns a truthy value or throws.
  - D) No such conversion happens.
</details>

---

### 65. Implicit wait = 10 s and explicit wait = 10 s are both set, and the awaited element never appears. Roughly how long until the failure?
- [ ] A) Exactly 10 seconds
- [ ] B) Around 20 seconds or more
- [ ] C) Instantly, because the two waits cancel each other
- [ ] D) Exactly 5 seconds, the average of the two

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Around 20 seconds or more

**Explanation:** Each poll calls `findElement`, which itself retries for up to 10 s because of the implicit wait. The explicit clock is nearly spent after the first call, and one more poll takes another 10 s. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) That would be the result only if the implicit wait were 0.
  - C) The waits do not cancel; they compound.
  - D) No averaging occurs.
</details>

---

### 66. The error says `element click intercepted ... Other element would receive the click: <div class="modal-backdrop fade show">`. What is the best fix?
- [ ] A) Increase the implicit wait to 30 seconds
- [ ] B) Replace the click with `Thread.sleep(5000)` followed by the same click
- [ ] C) Catch the exception and ignore it
- [ ] D) Wait for `invisibilityOfElementLocated` on the backdrop, then wait for the button to be clickable and click

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Wait for `invisibilityOfElementLocated` on the backdrop, then wait for the button to be clickable and click

**Explanation:** The message names the covering element. Waiting for that overlay to disappear addresses the real cause. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) The implicit wait only waits for presence; the button is already present.
  - B) A fixed sleep is a guess: slow and still flaky.
  - C) Ignoring it would hide the problem and the click would not happen.
</details>

---

### 67. A `TimeoutException` reads: `waiting for visibility of element located by By.id: finish (tried for 10 second(s) with 500 milliseconds interval)`. Which statement about diagnosing it is correct?
- [ ] A) The page must be broken, so the timeout should be raised to 60 seconds
- [ ] B) The polling interval of 500 ms is too coarse and caused the failure
- [ ] C) The message tells what was awaited, for how long and how often; possible causes include a wrong locator or an element that never becomes visible
- [ ] D) It always means the element does not exist in the DOM

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The message tells what was awaited, for how long and how often; possible causes include a wrong locator or an element that never becomes visible

**Explanation:** The message reads like a sentence: what (visibility of `By.id: finish`), how long (10 s) and how often (500 ms). Causes include a wrong locator, an element that is hidden or in an iframe, a real bug, or a too-short timeout. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) Lengthening the timeout is not a default fix; it would not help a wrong locator.
  - B) A 500 ms interval does not cause a 10 s wait to fail.
  - D) The element may exist but remain hidden (`display:none`) or sit in an iframe.
</details>

---

### 68. Which approach to choosing a timeout matches the lesson?
- [ ] A) Use 1-2 seconds so failures are reported quickly
- [ ] B) Start with 10 seconds, since the timeout is a maximum and costs nothing when the page is fast
- [ ] C) Use 120 seconds everywhere so tests never time out
- [ ] D) Set a different random value per test to avoid synchronized failures

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Start with 10 seconds, since the timeout is a maximum and costs nothing when the page is fast

**Explanation:** The timeout is a maximum, not a delay. Ten seconds is long enough for most pages and short enough to report real failures promptly; use 30-60 s only for known slow operations, in a separate wait object. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) A tiny timeout fails on normal slow responses (listed under common mistakes).
  - C) The lesson reserves long waits for known slow operations only.
  - D) Random values are not advised; timeouts belong in configuration.
</details>

---

**Part B: True/False**

### 69. True or False: Selenium's `click()` automatically waits until any AJAX request triggered by the click has finished and the new elements are drawn.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `click()` returns once the click is performed (and, for a full page navigation, once that navigation completes). Selenium does not know about background AJAX, rendering or animations, which is the source of the race condition. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) This is the misconception: only full page navigations are waited for, not JavaScript-driven updates.
</details>

---

### 70. True or False: `invisibilityOfElementLocated` returns `true` even if the element is not in the page at all, so it is safe to use for an overlay that may never appear.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** It returns `true` both when the element is hidden and when it is absent from the page. The subtle caveat is that checking before an overlay has appeared passes instantly. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) The misconception is that a missing element makes the condition fail or time out; absence counts as invisible.
</details>

---

### 71. True or False: `WebDriverWait` is essentially a `FluentWait` preconfigured with a 500 ms polling interval that ignores `NotFoundException`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `WebDriverWait` is a `FluentWait` with sensible defaults. You use `FluentWait` directly when you need tuned polling, several ignored exceptions or a non-driver object. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) The misconception is that they are unrelated mechanisms; in fact `WebDriverWait` inherits `.pollingEvery(...)` and `.ignoring(...)`.
</details>

---

### 72. True or False: In a wait helper that saves a screenshot on timeout, it is fine to catch the `TimeoutException` in the `catch` block and not rethrow it, because the screenshot already reports the problem.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The `catch` is only used to add information, then the exception must be rethrown with `throw e;` so the test still fails. Swallowing it makes a test pass when it should fail. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) The misconception is that capturing evidence replaces failing; the lesson says never swallow the exception.
</details>

---

**Part C: Code Prediction**

### 73. What is printed? An implicit wait of 10 s is set; on `/dynamic_loading/1` the `#finish` element is already in the HTML but hidden until the loading bar completes.
```java
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");
driver.findElement(By.cssSelector("#start button")).click();
String text = driver.findElement(By.id("finish")).getText();
System.out.println("[" + text + "]");
```
- [ ] A) `[Hello World!]`
- [ ] B) A `NoSuchElementException` after 10 seconds
- [ ] C) `[]`
- [ ] D) A `TimeoutException` after 10 seconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `[]`

**Explanation:** The element is present immediately, so the implicit wait is satisfied at once; `getText()` returns only visible text, which is still empty. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) The text would only be returned after the element becomes visible, which was not waited for.
  - B) The element exists in the DOM, so it is found immediately.
  - D) `TimeoutException` is thrown by explicit waits, and none is used here.
</details>

---

### 74. On SauceDemo the cart badge element is removed when the cart is empty and the cart is currently empty. What does this do?
```java
public static Function<WebDriver, Boolean> cartCountIs(int expected) {
    return d -> {
        List<WebElement> badges = d.findElements(By.className("shopping_cart_badge"));
        if (expected == 0) {
            return badges.isEmpty();
        }
        return !badges.isEmpty() && badges.get(0).getText().equals(String.valueOf(expected));
    };
}

wait.until(cartCountIs(0));
```
- [ ] A) The condition is true on the first poll, so `until` returns immediately
- [ ] B) It throws `NoSuchElementException` because the badge does not exist
- [ ] C) It throws `IndexOutOfBoundsException` from `badges.get(0)`
- [ ] D) It waits the full timeout and then throws `TimeoutException`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The condition is true on the first poll, so `until` returns immediately

**Explanation:** For `expected == 0` the lambda returns `badges.isEmpty()`, and `findElements` returns an empty list when the badge is gone, so the result is `true`. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) `findElements` never throws for missing elements; it returns an empty list.
  - C) The `get(0)` line is never reached when `expected` is 0.
  - D) The condition is already true, so there is nothing to wait for.
</details>

---

### 75. A list is re-rendered by clicking Refresh. What happens at the last line?
```java
WebElement oldRow = driver.findElement(By.cssSelector("tr.row"));
driver.findElement(By.id("refresh")).click();
wait.until(ExpectedConditions.stalenessOf(oldRow));
System.out.println(oldRow.getText());
```
- [ ] A) It prints the text of the new first row
- [ ] B) It prints the old row's text, since the variable still holds it
- [ ] C) It throws `TimeoutException`
- [ ] D) It throws `StaleElementReferenceException`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It throws `StaleElementReferenceException`

**Explanation:** `stalenessOf` succeeds because the old element was removed or replaced, which means the saved reference is dead. Using `oldRow` afterward fails; you must re-locate by locator to get a fresh reference. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) A saved reference does not automatically point at the new element.
  - B) Like a photo of a demolished house, the reference no longer points at a real element.
  - C) The wait itself succeeded since the old row went stale; the exception comes from the later line.
</details>

---

### 76. The results table appears about 1 second after the call starts. What best describes the behavior?
```java
Wait<WebDriver> fluentWait = new FluentWait<>(driver)
        .withTimeout(Duration.ofSeconds(30))
        .pollingEvery(Duration.ofMillis(250))
        .ignoring(NoSuchElementException.class, StaleElementReferenceException.class)
        .withMessage("The results table never appeared");

WebElement table = fluentWait.until(d -> d.findElement(By.id("results-table")));
```
- [ ] A) It always waits the full 30 seconds before returning
- [ ] B) It returns the element at the first 250 ms poll after the table exists, about 1 second in
- [ ] C) It throws `NoSuchElementException` on the first poll because the table is missing
- [ ] D) It returns `null` until the 30 seconds are over

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It returns the element at the first 250 ms poll after the table exists, about 1 second in

**Explanation:** The lambda returns the element itself, which is a non-null value, so finding it is the success. `NoSuchElementException` during early polls is ignored, and 30 s is only a maximum. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) The timeout is a maximum, not a delay.
  - C) `NoSuchElementException` is on the ignore list, so polling continues.
  - D) `until` does not return until the condition is truthy; it otherwise throws `TimeoutException` with the custom message.
</details>

---

### 77. After the page re-renders the card list, this wait never succeeds even though cards are visibly on screen. What is the most likely cause?
```java
WebElement card = driver.findElement(By.className("inventory_item"));
// ... page re-renders the list ...
wait.until(d -> card.isDisplayed());
```
- [ ] A) `isDisplayed()` cannot be used inside a lambda
- [ ] B) `until` only accepts `ExpectedConditions`, not lambdas
- [ ] C) The lambda reuses the same stored (stale) reference on every poll instead of locating inside the lambda
- [ ] D) The polling interval is too short to read the element

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The lambda reuses the same stored (stale) reference on every poll instead of locating inside the lambda

**Explanation:** The saved `card` points at the old element each poll. Locating inside the lambda, with `d.findElement(...).isDisplayed()`, gets a fresh reference each time. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) Any boolean expression can be a custom condition.
  - B) In Selenium 4, `until` accepts any `Function<WebDriver, T>`.
  - D) The interval is not the issue; the reference is dead on every poll.
</details>

---

### 78. What does this single statement do on its own (no `until` call around it)?
```java
ExpectedConditions.visibilityOfElementLocated(By.id("message"));
```
- [ ] A) It only builds a condition object remembering the locator; it does not look at the page or wait
- [ ] B) It waits up to the default timeout for the message to be visible
- [ ] C) It returns the `WebElement` after locating it immediately
- [ ] D) It throws `NoSuchElementException` if the message is not present

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It only builds a condition object remembering the locator; it does not look at the page or wait

**Explanation:** The condition is only evaluated when `wait.until(...)` runs it repeatedly; creating it does not touch the page. *(waiting-strategies.md)*
- **Why others are wrong:**
  - B) Waiting is done by `until`, not by the condition factory.
  - C) A `WebElement` is returned only by `until` after the condition is satisfied.
  - D) Nothing is looked up, so nothing can be missing.
</details>

---

### 79. The wait times out inside the `try` block. What happens?
```java
WebDriver driver = new ChromeDriver();
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
try {
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
    wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("nope")));
} finally {
    driver.quit();
}
```
- [ ] A) The browser stays open because the exception skips `finally`
- [ ] B) The exception is swallowed and the program ends normally
- [ ] C) `finally` runs first, but the exception is converted into `NoSuchElementException`
- [ ] D) `driver.quit()` runs and closes the browser, then the `TimeoutException` still reaches the caller

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `driver.quit()` runs and closes the browser, then the `TimeoutException` still reaches the caller

**Explanation:** `try/finally` guarantees the browser closes even if a wait times out, which prevents leftover Chrome windows and driver processes. There is no `catch`, so the exception propagates. *(waiting-strategies.md)*
- **Why others are wrong:**
  - A) `finally` always runs; that is its purpose here.
  - B) With no `catch` block nothing swallows the exception.
  - C) Exceptions are not converted, and the wait throws `TimeoutException` after 15 s.
</details>

---

**Part D: Fill-in-the-Blank**

### 80. An implicit wait only waits for the _____ of an element in the DOM, not for it to be visible or clickable.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `presence` (also accepted: existence, being present, appearing in the DOM)

**Explanation:** Implicit waits wait for existence, not readiness, so hidden or disabled elements still satisfy them. *(waiting-strategies.md)*
</details>

---

### 81. Before clicking an element, wait with `ExpectedConditions._____(...)` so that the element is both visible and enabled.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `elementToBeClickable` (also accepted: `elementToBeClickable(By)` or `elementToBeClickable(WebElement)`)

**Explanation:** The lesson's rule of thumb is clickable before clicking, visible before reading text, and invisible for loading indicators. *(waiting-strategies.md)*
</details>

---

### 82. To prove that a click really re-rendered a row, wait for the saved old element to be replaced using `ExpectedConditions._____(oldRow)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `stalenessOf` (also accepted: stalenessOf(oldRow))

**Explanation:** `stalenessOf` succeeds once the old element is no longer attached to the page, after which you locate the fresh element by locator. *(waiting-strategies.md)*
</details>

---

### 83. Because the Selenium documentation warns against combining them, in your own framework you should use explicit waits and leave the implicit wait at _____ (for example `Duration.ZERO`).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `0` (also accepted: zero, 0 seconds, `Duration.ZERO`, disabled)

**Explanation:** Keeping the implicit wait at 0 avoids the compounding timeouts that appear when both kinds of wait are active. *(waiting-strategies.md)*
</details>

---

#### Set 2 of 2

**Part A: Multiple Choice**

### 84. A test fails with `ElementClickInterceptedException`. The message says the target `<button id="checkout">` is not clickable at point (512, 610) and that `<div id="cookie-banner">` would receive the click. What is the correct fix?
- [ ] A) Replace `click()` with `submit()` so the banner is ignored
- [ ] B) Deal with the banner (accept it in setup or wait for it to disappear), then click the button
- [ ] C) Change the locator of the button to an XPath expression
- [ ] D) Catch the exception and retry the same click immediately

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Deal with the banner (accept it in setup or wait for it to disappear), then click the button

**Explanation:** The message names the covering element, so the cause is the overlay, not the button or its locator. The lesson says to handle the banner rather than force the click. *(element-interactions.md)*
- **Why others are wrong:**
  - A) `submit()` is a legacy form method and does not remove an overlay covering the button.
  - C) The element was found correctly; the locator type is not the problem.
  - D) Retrying immediately hits the same covering element and fails again.
</details>

---

### 85. A tester automates an "edit profile" page that is pre-filled with `old@test.com`. The test runs `email.sendKeys("new@test.com")`, the server rejects the value, and the line looks correct. What is the most likely cause?
- [ ] A) `sendKeys` cannot type the `@` character
- [ ] B) The email field must be submitted with `submit()` before typing
- [ ] C) `sendKeys` appended to the existing text, giving `old@test.comnew@test.com`
- [ ] D) `sendKeys` replaced the text but the page cached the old value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `sendKeys` appended to the existing text, giving `old@test.comnew@test.com`

**Explanation:** `sendKeys` appends to whatever is already in the field, so pre-filled forms need `clear()` first. Printing `getAttribute("value")` after typing exposes the problem. *(element-interactions.md)*
- **Why others are wrong:**
  - A) Typing is character by character and normal text input works for email fields.
  - B) `submit()` sends the form; it is not a prerequisite for typing.
  - D) `sendKeys` never replaces text, it appends.
</details>

---

### 86. After typing `standard_user` into a username `<input>`, which call reliably returns what is in the box?
- [ ] A) `getAttribute("value")`
- [ ] B) `getText()`
- [ ] C) `getTagName()`
- [ ] D) `isSelected()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `getAttribute("value")`

**Explanation:** An `<input>` has no text between tags; its content lives in the `value` attribute/property, so `getAttribute("value")` reads it. *(element-interactions.md)*
- **Why others are wrong:**
  - B) `getText()` on an `<input>` returns an empty string.
  - C) `getTagName()` returns the tag name (`input`), not its content.
  - D) `isSelected()` reports checked state for checkboxes, radios and options.
</details>

---

### 87. How should you upload a file through a standard `<input type="file">`?
- [ ] A) Click the input and drive the operating-system dialog with Selenium
- [ ] B) Send a path relative to the browser's installation folder
- [ ] C) Call `submit()` on the input with the file name
- [ ] D) Call `sendKeys` on the input with the absolute path of the file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Call `sendKeys` on the input with the absolute path of the file

**Explanation:** Clicking opens a native dialog Selenium cannot control; sending the absolute path directly bypasses the picker. The file must exist on the machine where the browser runs. *(element-interactions.md)*
- **Why others are wrong:**
  - A) Selenium cannot control the native operating-system dialog and the test hangs.
  - B) A relative path leads to "file not found"; an absolute path is required.
  - C) `submit()` submits a form and does not attach a file.
</details>

---

### 88. Why do the `SafeActions` helper methods accept a `By` locator instead of a `WebElement`?
- [ ] A) A `WebElement` cannot be passed to a method in Java
- [ ] B) A `By` can be re-evaluated at the moment of use, which avoids stale references
- [ ] C) A `By` makes `click()` skip the visibility checks
- [ ] D) A `By` is faster to type than a `WebElement`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A `By` can be re-evaluated at the moment of use, which avoids stale references

**Explanation:** A `By` is a recipe for finding the element, so the helper finds it fresh right after waiting. A stored `WebElement` is a one-time reference that can go stale. *(element-interactions.md)*
- **Why others are wrong:**
  - A) Methods can take a `WebElement`; the issue is staleness, not legality.
  - C) Selenium's checks still apply; the helper does not bypass them.
  - D) Typing convenience is not the reason given for this design.
</details>

---

### 89. A click keeps failing. According to the lesson's order of escalation, which step comes only after waiting for clickability, waiting for overlays to go, scrolling to the center and closing banners have all been tried?
- [ ] A) Wait for `elementToBeClickable` again with a longer timeout
- [ ] B) Scroll the element to the center of the viewport
- [ ] C) A JavaScript click, with an explaining comment, mentioned in code review
- [ ] D) Close the modal that is in the way

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A JavaScript click, with an explaining comment, mentioned in code review

**Explanation:** The JavaScript click is the last step because it bypasses Selenium's checks and can hide real bugs such as a permanently covered button. *(element-interactions.md)*
- **Why others are wrong:**
  - A) Waiting for clickability is step 1 of the escalation, not the last.
  - B) Scrolling to the center is step 3.
  - D) Closing banners or modals is step 4, before any JavaScript click.
</details>

---

### 90. A multilingual site changes the label text of its dropdown options depending on the language, but each `<option>` keeps a stable code such as `US`. Which method fits best?
- [ ] A) `selectByValue`
- [ ] B) `selectByVisibleText`
- [ ] C) `selectByIndex(0)`
- [ ] D) `getFirstSelectedOption`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `selectByValue`

**Explanation:** The lesson's decision guide recommends `selectByValue` when the label changes by language, because the `value` attribute is usually a stable code. *(select-elements.md)*
- **Why others are wrong:**
  - B) Visible text changes with the language and would break the test.
  - C) Index 0 is often a placeholder and position is fragile.
  - D) That method reads the current selection; it does not choose anything.
</details>

---

### 91. `new Select(driver.findElement(By.cssSelector(".country-dropdown")))` throws `UnexpectedTagNameException: Element should have been "select" but was "div"`. What does this tell you?
- [ ] A) The `<select>` is disabled and must be enabled first
- [ ] B) The page needs a longer explicit wait before wrapping
- [ ] C) The `selenium-java` dependency is missing the `Select` class
- [ ] D) The element is not a native `<select>`, so it is a custom dropdown (or the locator points to the wrong element)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The element is not a native `<select>`, so it is a custom dropdown (or the locator points to the wrong element)

**Explanation:** The constructor checks the tag name immediately. The error means you found a `<div>`: either look for a real `<select>` inside, or automate the custom widget by click-open-click. *(select-elements.md)*
- **Why others are wrong:**
  - A) A disabled `<select>` would still be a `select` tag, so this error would not occur.
  - B) The tag check happens at construction; waiting longer does not change a `div` into a `select`.
  - C) A missing class would be a compile error ("cannot find symbol"), not this exception.
</details>

---

### 92. A registration dropdown starts with `<option value="" disabled selected>Select a country</option>`. A test calls `selectByIndex(0)` expecting the first country. What happens?
- [ ] A) It selects the first real country because indexes start at 1
- [ ] B) It throws `UnexpectedTagNameException`
- [ ] C) It targets the placeholder, which is index 0 and disabled, so the intended choice is not made
- [ ] D) It selects the last option in the list

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It targets the placeholder, which is index 0 and disabled, so the intended choice is not made

**Explanation:** Indexes are 0-based and the placeholder occupies index 0. A disabled option cannot be chosen, so the lesson advises printing the option list first. *(select-elements.md)*
- **Why others are wrong:**
  - A) Indexing is 0-based, so the placeholder is index 0.
  - B) That exception occurs only when wrapping a non-`<select>` element.
  - D) There is no wrap-around behaviour described; index 0 means the first option.
</details>

---

### 93. A test chooses "Canada" in a country dropdown, then immediately calls `selectByVisibleText("Ontario")` on the state dropdown and gets `Cannot locate option with text: Ontario`. What is the best fix?
- [ ] A) Use `selectByIndex` instead of `selectByVisibleText`
- [ ] B) Wait (for example with a lambda) until the state list contains the "Ontario" option, then select it
- [ ] C) Store the `Select` object once and reuse it for every state
- [ ] D) Call `deselectAll()` before choosing the state

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Wait (for example with a lambda) until the state list contains the "Ontario" option, then select it

**Explanation:** The state list loads by AJAX after the country choice, so the placeholder is the only option at first. Waiting for the specific option avoids the race. *(select-elements.md)*
- **Why others are wrong:**
  - A) An index would hit the same unloaded list and is more fragile.
  - C) Reusing a stored `Select` risks staleness; a fresh one is created inside the wait.
  - D) `deselectAll()` is for multi-selects and throws on single-selects.
</details>

---

### 94. On SauceDemo, why must prices like `$9.99` and `$29.99` be converted to numbers before checking that a "Price (low to high)" sort is correct?
- [ ] A) `findElements` cannot return text for price elements
- [ ] B) `Collections.sort` only works on `double` values that came from a stream
- [ ] C) The `$` sign makes `getText()` return an empty string
- [ ] D) Compared as text, `"$9.99"` would sort after `"$29.99"`, giving a wrong verdict

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Compared as text, `"$9.99"` would sort after `"$29.99"`, giving a wrong verdict

**Explanation:** Text comparison is character by character, so the numerically smaller value can sort later. The lesson strips `$` and parses to `double` first. *(select-elements.md)*
- **Why others are wrong:**
  - A) `getText()` returns the displayed price text normally.
  - B) `Collections.sort` works on any comparable list; the issue is text versus number ordering.
  - C) `getText()` returns the visible text including the `$`.
</details>

---

**Part B: True/False**

### 95. True or False: `sendKeys("xyz")` on a field that already contains "abc" replaces the content, leaving "xyz".
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `sendKeys` appends, producing "abcxyz". You must `clear()` first (or use a select-all chord) to replace the text. *(element-interactions.md)*
- **Why others are wrong:**
  - A) The misconception is that typing overwrites; it simulates real typing and appends to existing content.
</details>

---

### 96. True or False: Calling `getText()` on an `<input>` element after typing into it returns an empty string, because the typed content lives in the `value` attribute.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** An `<input>` has no text between its tags, so `getText()` is empty; use `getAttribute("value")` to read what was typed. *(element-interactions.md)*
- **Why others are wrong:**
  - B) The misconception is that `getText()` returns typed input; it only returns visible text of the element, which is empty for an input.
</details>

---

### 97. True or False: Calling `deselectAll()` on a single-select dropdown is harmless and simply leaves the selection unchanged.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Any `deselect...` method on a single-select throws `UnsupportedOperationException` ("You may only deselect options of a multi-select"). Guard with `isMultiple()`. *(select-elements.md)*
- **Why others are wrong:**
  - A) The misconception is that it is a no-op; a normal dropdown always has exactly one chosen option, so Selenium refuses the operation.
</details>

---

### 98. True or False: Calling `selectByVisibleText` for an option that is already selected is harmless and nothing changes.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** If the option is already selected, `Select` does not change anything, so selecting the same option twice is harmless. *(select-elements.md)*
- **Why others are wrong:**
  - B) The misconception is that a repeat selection toggles the option off or throws; that does not happen for a single-select.
</details>

---

**Part C: Code Prediction**

### 99. A checkbox starts **checked**. Using the `setCheckbox` helper from the lesson, what is printed?
```java
public void setCheckbox(WebElement checkbox, boolean shouldBeChecked) {
    if (checkbox.isSelected() != shouldBeChecked) {
        checkbox.click();
    }
}

setCheckbox(box, true);
setCheckbox(box, false);
setCheckbox(box, false);
System.out.println(box.isSelected());
```
- [ ] A) `true`
- [ ] B) `false`
- [ ] C) An `ElementNotInteractableException` is thrown
- [ ] D) `true`, because the third call clicks again

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `false`

**Explanation:** Call 1: already checked and desired true, no click. Call 2: checked but desired false, one click unchecks it. Call 3: unchecked and desired false, no click. *(element-interactions.md)*
- **Why others are wrong:**
  - A) That would be the result of a helper that always clicks an odd number of times; here the state ends unchecked.
  - C) A standard visible checkbox is interactable; nothing in the code triggers that exception.
  - D) The third call finds `isSelected() == false` equal to the desired `false`, so it does nothing.
</details>

---

### 100. `radios` holds two radio buttons from the same group (`By.name("shipping")`), neither selected. What is printed?
```java
radios.get(1).click();
System.out.println(radios.get(1).isSelected());
System.out.println(radios.get(0).isSelected());
radios.get(1).click();
System.out.println(radios.get(1).isSelected());
```
- [ ] A) `true`, `true`, `false`
- [ ] B) `true`, `false`, `false`
- [ ] C) `true`, `false`, `true`
- [ ] D) `false`, `false`, `false`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `true`, `false`, `true`

**Explanation:** Clicking an unselected radio selects it and deselects others in its group; clicking an already selected radio does nothing, so it stays selected. *(element-interactions.md)*
- **Why others are wrong:**
  - A) Radios in the same group are mutually exclusive, so button 0 is not selected.
  - B) The second click on a selected radio does not deselect it (unlike a checkbox toggle).
  - D) The first click does select radio 1.
</details>

---

### 101. What do the two `println` lines print?
```java
username.sendKeys("wrong_user");
username.clear();
username.sendKeys("standard_user");
System.out.println("[" + username.getAttribute("value") + "]");
System.out.println("[" + username.getText() + "]");
```
- [ ] A) `[wrong_userstandard_user]` and `[standard_user]`
- [ ] B) `[standard_user]` and `[standard_user]`
- [ ] C) `[]` and `[standard_user]`
- [ ] D) `[standard_user]` and `[]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `[standard_user]` and `[]`

**Explanation:** `clear()` removes the wrong text, so the value is `standard_user` (not appended). `getText()` on an `<input>` returns an empty string. *(element-interactions.md)*
- **Why others are wrong:**
  - A) `clear()` removed the first text, so nothing is appended; and `getText()` is empty for an input.
  - B) `getText()` does not read an input's value.
  - C) The value attribute holds the typed text, so it is not empty, and `getText()` is the one that is empty.
</details>

---

### 102. A `/dropdown` page has options: "Please select an option" (value empty, index 0), "Option 1" (value `1`), "Option 2" (value `2`). What does this print?
```java
Select dropdown = new Select(driver.findElement(By.id("dropdown")));
dropdown.selectByValue("2");
dropdown.selectByIndex(1);
System.out.println(dropdown.getFirstSelectedOption().getText());
```
- [ ] A) `Option 1`
- [ ] B) `Option 2`
- [ ] C) `Please select an option`
- [ ] D) `NoSuchElementException` is thrown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `Option 1`

**Explanation:** `selectByValue("2")` selects "Option 2", then `selectByIndex(1)` selects the option at index 1, which is "Option 1" because the placeholder is index 0. In a single-select the last choice wins. *(select-elements.md)*
- **Why others are wrong:**
  - B) That is the state after the first call only; the second call changes the selection.
  - C) The placeholder is index 0, not 1.
  - D) Both the value `2` and index 1 exist, so nothing is missing.
</details>

---

### 103. A multi-select `languages` has options Java (`java`), Python (`py`), JavaScript (`js`). What is printed?
```java
Select langs = new Select(driver.findElement(By.id("languages")));
langs.selectByVisibleText("Java");
langs.selectByValue("py");
langs.deselectByValue("java");
List<String> texts = new ArrayList<>();
for (WebElement o : langs.getAllSelectedOptions()) texts.add(o.getText());
System.out.println(texts);
```
- [ ] A) `[Java, Python]`
- [ ] B) `[Python, JavaScript]`
- [ ] C) `[Python]`
- [ ] D) `[]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `[Python]`

**Explanation:** In a multi-select each `selectBy...` call adds to the selection, giving Java and Python. `deselectByValue("java")` then removes Java, leaving Python. *(select-elements.md)*
- **Why others are wrong:**
  - A) That is the state before the deselect call.
  - B) JavaScript was never selected.
  - D) Only Java was deselected; Python remains selected.
</details>

---

### 104. SauceDemo's page order after choosing "Price (low to high)" is shown. What does this print?
```java
List<Double> prices = Arrays.asList(7.99, 9.99, 15.99, 15.99, 29.99, 49.99);
List<Double> sorted = new ArrayList<>(prices);
Collections.sort(sorted);
System.out.println(prices.equals(sorted) ? "PASS: ascending" : "FAIL: not ascending");
```
- [ ] A) `FAIL: not ascending`, because two prices are equal
- [ ] B) A compile error, because `Arrays.asList` returns a fixed list
- [ ] C) `PASS: ascending`
- [ ] D) `PASS: ascending` only if the list contains no duplicates

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `PASS: ascending`

**Explanation:** `equals` on two lists compares size and elements in order, so ties are allowed; the sorted copy equals the original. The lesson uses this instead of a "strictly increasing" check. *(select-elements.md)*
- **Why others are wrong:**
  - A) Equal neighbouring prices do not break list equality.
  - B) Only the copy (`new ArrayList<>(prices)`) is sorted, and the original is never modified.
  - D) There is no such duplicate restriction; ties are explicitly tolerated.
</details>

---

**Part D: Fill-in-the-Blank**

### 105. To upload a file with Selenium you call `sendKeys` on the `<input type="file">` with the _____ path of the file, because a relative path leads to "file not found".

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `absolute` (also accepted: full, complete path, `getAbsolutePath()`)

**Explanation:** The lesson sends the absolute path (for example from `new File(...).getAbsolutePath()`); the file must exist on the machine where the browser runs. *(element-interactions.md)*
</details>

---

### 106. Clicking a checkbox _____ its state, so a safe "tick this box" helper must check `isSelected()` first.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `toggles` (also accepted: flips, switches, inverts)

**Explanation:** Because a click toggles the box, clicking without checking could untick an already ticked box, for example on a second test run. *(element-interactions.md)*
</details>

---

### 107. Passing a `<div>` element to `new Select(...)` immediately throws `_____`, which tells you the dropdown is custom and should be automated with ordinary clicks.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `UnexpectedTagNameException` (also accepted: `org.openqa.selenium.support.ui.UnexpectedTagNameException`)

**Explanation:** The `Select` constructor checks the tag name once; a non-`<select>` element is rejected at once. Custom dropdowns use click to open, wait, click the option. *(select-elements.md)*
</details>

---

## Day 3 - Wednesday: Actions, Windows and POM

#### Set 1 of 2

**Part A: Multiple Choice**

### 108. Why is `element.click()` not enough to express a gesture such as "press here, move there, release"?
- [ ] A) It can only be used on links and buttons, never on other elements
- [ ] B) It does exactly one thing, clicking the middle of an element, while real gestures are sequences
- [ ] C) It always waits for the page to reload before returning
- [ ] D) It is removed in Selenium 4 and replaced by `Actions`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It does exactly one thing, clicking the middle of an element, while real gestures are sequences

**Explanation:** A single method call cannot describe "move, press, move, release", so Selenium provides the Actions API to describe sequences. *(actions-api.md)*
- **Why others are wrong:**
  - A) `click()` works on any clickable element; the limitation is about sequences, not element type.
  - C) `click()` does not wait for reloads; that is unrelated to the limitation.
  - D) `click()` still exists and the lesson recommends it when it is enough.
</details>

---

### 109. A tester runs `driver.findElement(By.linkText("Laptops")).click();` on a shop and gets `ElementNotInteractableException`. What is the most likely cause?
- [ ] A) The `Actions` import is missing
- [ ] B) `perform()` was never called
- [ ] C) The locator type `linkText` cannot be used with menus
- [ ] D) The item exists but stays hidden until the parent menu is hovered

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The item exists but stays hidden until the parent menu is hovered

**Explanation:** The element is in the page but hidden (for example `display:none`), so Selenium refuses to click it. Hover the parent, wait for visibility, then click. *(actions-api.md)*
- **Why others are wrong:**
  - A) A missing import is a compile error (`cannot find symbol`), not this runtime exception.
  - B) No `Actions` chain is used in this code, so `perform()` is irrelevant.
  - C) The lesson gives no such restriction; the element was found but not interactable.
</details>

---

### 110. In Selenium 4, what does `moveToElement(chart, 100, -20)` do?
- [ ] A) Moves the pointer 100 pixels right of and 20 pixels above the element's center
- [ ] B) Moves the pointer 100 pixels right of and 20 pixels below the element's top-left corner
- [ ] C) Moves the pointer 100 pixels from its current position, ignoring the element
- [ ] D) Moves the pointer to the element's center and then clicks twice

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Moves the pointer 100 pixels right of and 20 pixels above the element's center

**Explanation:** In Selenium 4 offsets are measured from the element's center; Selenium 3 used the top-left corner. *(actions-api.md)*
- **Why others are wrong:**
  - B) That describes the old Selenium 3 behaviour (and the sign of y would also differ).
  - C) Relative-to-current-position movement is `moveByOffset(x, y)`.
  - D) `moveToElement` only moves; it does not click.
</details>

---

### 111. You need to move a slider handle 50 pixels to the right and there is no target element. Which method fits best?
- [ ] A) `dragAndDrop(slider, target)`
- [ ] B) `contextClick(slider)`
- [ ] C) `dragAndDropBy(slider, 50, 0)`
- [ ] D) `scrollByAmount(50, 0)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `dragAndDropBy(slider, 50, 0)`

**Explanation:** `dragAndDropBy` takes x and y pixel offsets and is meant for sliders and resize handles where the "target" is just a position. *(actions-api.md)*
- **Why others are wrong:**
  - A) It needs a target element, which does not exist here.
  - B) That is a right-click and does not move anything.
  - D) Scrolling moves the page view, not a slider handle.
</details>

---

### 112. When is `scrollFromOrigin` the right choice instead of `scrollByAmount`?
- [ ] A) When the page must be scrolled to the very top
- [ ] B) When an inner scrollable container, such as a chat panel, must scroll rather than the whole page
- [ ] C) When Selenium 3 is used, because wheel input is unavailable
- [ ] D) When you want to scroll a negative number of pixels

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) When an inner scrollable container, such as a chat panel, must scroll rather than the whole page

**Explanation:** `scrollFromOrigin` starts the wheel at a chosen origin element, so it scrolls that inner element; scrolling the page would not move it. *(actions-api.md)*
- **Why others are wrong:**
  - A) Nothing in the lesson ties it to scrolling to the top.
  - C) Scroll actions are a Selenium 4 feature, so they are not available in Selenium 3.
  - D) Negative amounts already work with `scrollByAmount` (they scroll up or left).
</details>

---

### 113. A tester automates the-internet's HTML5 drag-and-drop page with `dragAndDrop`. No exception appears, but the two columns do not swap. What is the best practice from the lesson?
- [ ] A) Add a long `Thread.sleep` after `perform()`
- [ ] B) Wrap the call in `try/catch` and treat the missing exception as success
- [ ] C) Switch to `contextClick` on the target
- [ ] D) Assert the outcome (such as the header text), and use the manual sequence or a JavaScript fallback

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Assert the outcome (such as the header text), and use the manual sequence or a JavaScript fallback

**Explanation:** HTML5 native drag events may not fire for synthetic pointer movements, so Actions can fail silently. Asserting the result exposes the failure; the manual sequence or JavaScript are the workarounds. *(actions-api.md)*
- **Why others are wrong:**
  - A) The problem is that the events never fire, not timing, and long delays make tests slow and flaky.
  - B) Silent failure means no exception is thrown, so no exception proves nothing about success.
  - C) A right-click does not perform a drop.
</details>

---

### 114. Which statement best separates an HTML modal from a JavaScript alert?
- [ ] A) A modal always has an OK button and an alert never does
- [ ] B) An alert is always a separate browser window
- [ ] C) If you can right-click the pop-up and choose "Inspect", it is HTML, not an alert
- [ ] D) A modal can only be closed with `accept()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) If you can right-click the pop-up and choose "Inspect", it is HTML, not an alert

**Explanation:** JavaScript dialogs are drawn by the browser and are not in the DOM, so DevTools cannot inspect them; HTML modals can be inspected and located with `By`. *(alerts.md)*
- **Why others are wrong:**
  - A) Button labels do not decide the type; the DOM presence does.
  - B) A separate window is a pop-up window handled with window handles, not an alert.
  - D) `accept()` belongs to the `Alert` interface; modals use ordinary locators and clicks.
</details>

---

### 115. A test clicks a button that opens an alert and immediately calls `driver.findElement(By.id("result"))`. By default, what does Selenium do?
- [ ] A) Dismisses the alert and throws `UnhandledAlertException` that includes the alert text
- [ ] B) Accepts the alert silently and returns the element
- [ ] C) Waits indefinitely until the alert is closed manually
- [ ] D) Throws `NoAlertPresentException`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Dismisses the alert and throws `UnhandledAlertException` that includes the alert text

**Explanation:** The default unhandled prompt behaviour is to dismiss the open dialog and throw `UnhandledAlertException`, with the dialog text in the message. *(alerts.md)*
- **Why others are wrong:**
  - B) Silent accepting only happens if you configure `ACCEPT` through capabilities.
  - C) Selenium does not wait for manual action; it errors out.
  - D) `NoAlertPresentException` is thrown when you try to switch to an alert that does not exist.
</details>

---

### 116. Which Selenium 4 feature supplies basic-auth credentials on Chromium-based drivers?
- [ ] A) `driver.switchTo().alert().sendKeys("admin")`
- [ ] B) `ExpectedConditions.alertIsPresent()`
- [ ] C) `ChromeOptions.setUnhandledPromptBehaviour`
- [ ] D) `((HasAuthentication) driver).register(UsernameAndPassword.of(user, pass))`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `((HasAuthentication) driver).register(UsernameAndPassword.of(user, pass))`

**Explanation:** The basic-auth box is not a JavaScript alert; `HasAuthentication.register(...)` stores credentials the browser supplies when the server challenges. *(alerts.md)*
- **Why others are wrong:**
  - A) `switchTo().alert()` does not work for the browser's login box.
  - B) It waits for JavaScript dialogs, which basic auth is not.
  - C) That only configures what happens to unexpected JavaScript alerts.
</details>

---

### 117. A delete feature shows a confirm dialog. Which pairing correctly describes the Cancel branch test?
- [ ] A) `accept()`, then assert the item is gone
- [ ] B) `dismiss()`, then assert the item is still in the list and no success message appears
- [ ] C) `sendKeys("cancel")`, then assert the item is gone
- [ ] D) `dismiss()`, then assert a success message appears

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `dismiss()`, then assert the item is still in the list and no success message appears

**Explanation:** `dismiss()` presses Cancel, so the data must remain unchanged; the OK branch uses `accept()` and the opposite assertions. *(alerts.md)*
- **Why others are wrong:**
  - A) That is the OK branch.
  - C) `sendKeys` only works on prompts, and typing text does not press Cancel.
  - D) A success message belongs to the OK branch, not Cancel.
</details>

---

### 118. A test gets `NoAlertPresentException` right after clicking a button. According to the lesson, which cause should you check first?
- [ ] A) Timing: the switch happened before the dialog appeared, so `alertIsPresent()` is needed
- [ ] B) The browser is headless, which cannot show dialogs
- [ ] C) The `Alert` interface was not imported
- [ ] D) The dialog has too many buttons

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Timing: the switch happened before the dialog appeared, so `alertIsPresent()` is needed

**Explanation:** The lesson lists timing first, followed by "it is not an alert", wrong click, and already handled. *(alerts.md)*
- **Why others are wrong:**
  - B) Headless Chrome handles JavaScript dialogs the same way as headed Chrome.
  - C) A missing import is a compile-time error, not this runtime exception.
  - D) The number of buttons is irrelevant to this exception.
</details>

---

### 119. How should a cookie banner be handled in a test?
- [ ] A) With `driver.switchTo().alert().accept()`
- [ ] B) With `HasAuthentication`
- [ ] C) As an HTML modal in disguise, using ordinary locators and waits
- [ ] D) It cannot be automated

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) As an HTML modal in disguise, using ordinary locators and waits

**Explanation:** Cookie banners are regular page elements, so locators and waits apply; a "dismiss banner if present" step can sit in the page-object base class. *(alerts.md)*
- **Why others are wrong:**
  - A) It is not a JavaScript dialog, so `switchTo().alert()` would fail.
  - B) That is for basic-auth login boxes.
  - D) It is automatable like any other HTML element.
</details>

---

**Part B: True/False**

### 120. True or False: In Selenium 4 you must always call `build()` before `perform()`, otherwise the chain will not run.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** In Selenium 4, `perform()` calls `build()` for you. `build()` is only useful when you want to keep the compiled `Action` and run it more than once. *(actions-api.md)*
- **Why others are wrong:**
  - A) This is the misconception: older tutorials show `build().perform()`, but both forms are valid.
</details>

---

### 121. True or False: When `UnhandledAlertException` occurs, the alert is still open, so retrying the same line will fail again in the same way.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The browser has already dismissed the alert by the time you read the exception, so retrying the same line may succeed. That makes the failure look random. *(alerts.md)*
- **Why others are wrong:**
  - A) This is the misconception; the exception does not mean the dialog is still open.
</details>

---

### 122. True or False: Calling `sendKeys("text")` on the `Alert` of a plain alert or confirm dialog types into it, because every dialog has a text box.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Only a prompt has a text box. Calling `sendKeys` on a plain alert or confirm throws an exception. *(alerts.md)*
- **Why others are wrong:**
  - A) This is the misconception; alerts have only OK and confirms have OK and Cancel, with no input field.
</details>

---

### 123. True or False: If a chain uses `keyDown(Keys.CONTROL)` without a matching `keyUp`, the key stays logically pressed and can affect later steps.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Every `keyDown` needs a matching `keyUp`; otherwise the key remains "pressed" for later steps. *(actions-api.md)*
- **Why others are wrong:**
  - B) The misconception is that the key is released automatically at the end of `perform()`; the lesson says it is not.
</details>

---

**Part C: Code Prediction**

### 124. What happens when this code runs?
```java
Actions actions = new Actions(driver);
actions.moveToElement(menu).click(submenuItem);
```
- [ ] A) The submenu item is clicked after the hover
- [ ] B) A `NoSuchElementException` is thrown
- [ ] C) Nothing happens in the browser and no error is raised
- [ ] D) The code does not compile

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Nothing happens in the browser and no error is raised

**Explanation:** The chain only adds steps to the recipe. Without `perform()`, the browser never receives the instruction, and the code compiles and runs without error. *(actions-api.md)*
- **Why others are wrong:**
  - A) No step is executed without `perform()`.
  - B) No element lookup fails; nothing is sent to the browser at all.
  - D) The chain is valid Java; ending without `perform()` is simply a silent bug.
</details>

---

### 125. What text does the field contain after this runs (assume the field is empty and focused)?
```java
new Actions(driver)
    .keyDown(Keys.SHIFT)
    .sendKeys("lab")
    .keyUp(Keys.SHIFT)
    .sendKeys("x")
    .perform();
```
- [ ] A) `LABx`
- [ ] B) `LABX`
- [ ] C) `labx`
- [ ] D) `lab`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `LABx`

**Explanation:** Shift is held while "lab" is typed, so it comes out in capitals; Shift is released before "x", which is typed in lower case. *(actions-api.md)*
- **Why others are wrong:**
  - B) Shift is released by `keyUp` before "x" is sent.
  - C) That would be the result without the `keyDown(Keys.SHIFT)`.
  - D) The final `sendKeys("x")` is also performed, and "lab" is capitalized.
</details>

---

### 126. A tester runs the code below on a chart whose bar is far below the visible area. The error contains "move target out of bounds". Which exception is it?
```java
new Actions(driver)
    .moveToElement(driver.findElement(By.id("chart-bar-7")))
    .perform();
```
- [ ] A) `StaleElementReferenceException`
- [ ] B) `UnhandledAlertException`
- [ ] C) `NoAlertPresentException`
- [ ] D) `MoveTargetOutOfBoundsException`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `MoveTargetOutOfBoundsException`

**Explanation:** "Out of bounds" means the pointer was asked to go outside the visible window, for example to an element below the fold or via a large offset. The fix is to `scrollToElement` first. *(actions-api.md)*
- **Why others are wrong:**
  - A) That occurs when the page re-rendered between steps, not for off-screen elements.
  - B) That relates to an open JavaScript dialog.
  - C) That relates to switching to a dialog that is not there.
</details>

---

### 127. What does the page most likely display after this code (on the-internet's JavaScript alerts page)?
```java
driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();
wait.until(ExpectedConditions.alertIsPresent()).dismiss();
String r = driver.findElement(By.id("result")).getText();
```
- [ ] A) `You clicked: Ok`
- [ ] B) `You clicked: Cancel`
- [ ] C) `You entered: null`
- [ ] D) `UnhandledAlertException` is thrown on the last line

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `You clicked: Cancel`

**Explanation:** `dismiss()` presses Cancel on the confirm, the dialog closes and focus returns to the page, and the page shows "You clicked: Cancel". *(alerts.md)*
- **Why others are wrong:**
  - A) That is the result of `accept()`.
  - C) That is the prompt result after cancelling a prompt, not a confirm.
  - D) The alert was already closed by `dismiss()`, so the lookup works normally.
</details>

---

### 128. What happens on the last line of this code?
```java
driver.findElement(By.cssSelector("button[onclick='jsAlert()']")).click();
driver.findElement(By.id("result")).getText();
```
- [ ] A) It returns the empty string
- [ ] B) It throws `NoSuchElementException`
- [ ] C) It throws `UnhandledAlertException` with the alert text in the message
- [ ] D) It waits for the alert to disappear and then returns the result text

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It throws `UnhandledAlertException` with the alert text in the message

**Explanation:** The alert is still open when the next command runs, so Selenium dismisses it and throws `UnhandledAlertException` with `{Alert text : ...}`. *(alerts.md)*
- **Why others are wrong:**
  - A) The command does not run normally while the dialog blocks the page.
  - B) The element exists in the DOM; the problem is the open dialog.
  - D) Selenium does not wait; it dismisses and throws.
</details>

---

### 129. What does the page most likely display after this code?
```java
driver.findElement(By.cssSelector("button[onclick='jsPrompt()']")).click();
Alert prompt = wait.until(ExpectedConditions.alertIsPresent());
prompt.sendKeys("Revature");
prompt.dismiss();
```
- [ ] A) `You entered: Revature`
- [ ] B) `You entered: ` (empty)
- [ ] C) `You clicked: Cancel`
- [ ] D) `You entered: null`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `You entered: null`

**Explanation:** Dismissing a prompt (Cancel) makes JavaScript's `prompt()` return `null`, even though text was typed first. *(alerts.md)*
- **Why others are wrong:**
  - A) That requires `accept()` to submit the typed text.
  - B) Cancelling returns `null`, not an empty string.
  - C) That text is shown for confirm dialogs, not prompts.
</details>

---

**Part D: Fill-in-the-Blank**

### 130. The Actions method that adds a delay inside the gesture sequence, for example to let a hover animation finish, is `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `pause` (also accepted: `pause(Duration)`, `pause(Duration.ofMillis(...))`)

**Explanation:** `pause` is only for the timing of the gesture; page state should still be awaited with explicit waits. *(actions-api.md)*
</details>

---

### 131. On macOS, cross-platform suites use `Keys.COMMAND` instead of `Keys._____` for shortcuts.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `CONTROL` (also accepted: `Keys.CONTROL`, Ctrl)

**Explanation:** The lesson says to use `Keys.COMMAND` instead of `Keys.CONTROL` on macOS, often chosen by checking `System.getProperty("os.name")`. *(actions-api.md)*
</details>

---

### 132. `ExpectedConditions._____()` waits for a JavaScript dialog to exist and returns the `Alert` object, so no separate `switchTo().alert()` call is needed.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `alertIsPresent` (also accepted: `alertIsPresent()`)

**Explanation:** It returns the `Alert` once the dialog exists and throws `TimeoutException` if none appears in time. *(alerts.md)*
</details>

---

### 133. When the user cancels a prompt, JavaScript's `prompt()` returns _____, which some pages display as "You entered: _____".

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `null` (also accepted: null value)

**Explanation:** Dismissing a prompt gives the page's JavaScript `null`, a legitimate branch to test. *(alerts.md)*
</details>

---

#### Set 2 of 2

**Part A: Multiple Choice**

### 134. What does a Selenium window handle identify?
- [ ] A) The title text of a window, so that windows with the same title can be grouped
- [ ] B) A string that uniquely identifies one window or tab within the current session
- [ ] C) The URL currently loaded in a window
- [ ] D) The position of a window in the order the browser opened them

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A string that uniquely identifies one window or tab within the current session

**Explanation:** A handle is like a cloakroom ticket: it does not describe the window, it only identifies it, and it is guaranteed unique within a session. *(window-handling.md)*
- **Why others are wrong:**
  - A) Handles do not describe a window's title; titles can be duplicated, which is exactly why handles exist.
  - C) A handle does not describe the URL either; two tabs may show the same page.
  - D) A handle is an identifier string, not an index, and window order is not guaranteed.
</details>

---

### 135. What does `driver.getWindowHandles()` return, and what must you remember about it?
- [ ] A) A `List<String>` in opening order, so the last element is always the newest window
- [ ] B) A single `String` holding the handle of the newest window
- [ ] C) A `Set<String>` sorted so that the first element is always the original window
- [ ] D) A `Set<String>` with no guaranteed order, so you should compare against the original handle instead of picking "the last" one

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A `Set<String>` with no guaranteed order, so you should compare against the original handle instead of picking "the last" one

**Explanation:** `getWindowHandles()` returns a `Set<String>`, which has no duplicates and no guaranteed order. The reliable way to find a new window is to pick the handle that is not the original. *(window-handling.md)*
- **Why others are wrong:**
  - A) It is a `Set`, not an ordered `List`, so "last is newest" is a false assumption.
  - B) A single `String` is what `getWindowHandle()` (singular) returns, and it is the current window, not the newest.
  - C) A `Set` has no guaranteed order, so nothing is guaranteed to be first.
</details>

---

### 136. A tester clicks a link that opens a new tab. The new page's `h3` is plainly visible on screen, but `driver.findElement(By.tagName("h3"))` throws `NoSuchElementException`. What is the most likely cause?
- [ ] A) The driver still points at the original tab because no `switchTo().window(...)` was done
- [ ] B) Window handles expire after a few seconds, so the new tab's handle is no longer valid
- [ ] C) `getWindowHandles()` returned a `List`, which cannot be searched
- [ ] D) The new tab must be closed with `close()` before its elements can be found

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The driver still points at the original tab because no `switchTo().window(...)` was done

**Explanation:** Selenium controls one window at a time and does not follow new tabs automatically, so `findElement` keeps searching the old page even though the new tab is visible. Checking `getTitle()` or `getCurrentUrl()` before the failing line would show the old page. *(window-handling.md)*
- **Why others are wrong:**
  - B) Handles stay valid for the session; the lesson only warns against storing them between runs.
  - C) `getWindowHandles()` returns a `Set`, and the problem is the missing switch, not a collection type.
  - D) Closing the new tab would remove the page you want to inspect; it is unrelated to finding elements.
</details>

---

### 137. After `driver.close()` is called on a child tab, the next `driver.getTitle()` throws `NoSuchWindowException: target window already closed`. What is the correct fix?
- [ ] A) Call `driver.quit()` before the next command
- [ ] B) Wait with `numberOfWindowsToBe(1)` before the next command
- [ ] C) Call `driver.switchTo().window(originalHandle)` right after `close()`
- [ ] D) Call `driver.switchTo().defaultContent()` right after `close()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Call `driver.switchTo().window(originalHandle)` right after `close()`

**Explanation:** After `close()`, Selenium does not automatically move to another window, so any command fails until you switch to a window that is still open. *(window-handling.md)*
- **Why others are wrong:**
  - A) `quit()` ends the whole session and makes the driver unusable.
  - B) A wait checks the window count but does not move the driver's focus.
  - D) `defaultContent()` returns to the top-level document of the current window, which is the closed one; it does not switch windows.
</details>

---

### 138. Which statement about `driver.switchTo().newWindow(WindowType.TAB)` is correct?
- [ ] A) It opens a blank tab, and you must then loop through the handles to switch to it
- [ ] B) It opens a blank tab, but the driver stays on the original tab until you call `switchTo().window(...)`
- [ ] C) It opens a blank tab and switches to it, so no waiting loop is needed
- [ ] D) It opens a tab with its own cookies, so it can act as a second logged-in user

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It opens a blank tab and switches to it, so no waiting loop is needed

**Explanation:** Unlike clicking a link, `newWindow` both opens and switches, so you are already in the new window and can call `get(...)` directly. *(window-handling.md)*
- **Why others are wrong:**
  - A) No handle loop is needed because the switch is already done.
  - B) The driver does move to the new tab as part of the call.
  - D) Tabs in the same browser profile share cookies; separate users need a second `WebDriver` instance.
</details>

---

### 139. A locator is correct and the element is visible in DevTools, yet `findElement` throws `NoSuchElementException`. No new window or tab was opened. What should you check first?
- [ ] A) Whether the element sits inside an `<iframe>` ancestor in the DOM
- [ ] B) Whether `getWindowHandles()` returns the handles as a `Set`
- [ ] C) Whether the browser's window is maximized
- [ ] D) Whether `quit()` was called before `close()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Whether the element sits inside an `<iframe>` ancestor in the DOM

**Explanation:** An iframe embeds a separate DOM, so a lookup from the main page will not find elements inside it. Look upward in DevTools for an `<iframe>` ancestor and use `switchTo().frame(...)`. *(window-handling.md)*
- **Why others are wrong:**
  - B) The `Set` return type does not affect finding an element on the current page.
  - C) The lesson does not link maximizing to this error, and a visible element is not hidden by window size.
  - D) The order of `quit()` and `close()` does not cause a visible element to go missing, and the lesson does not suggest it.
</details>

---

### 140. A test calls `driver.switchTo().frame(driver.findElement(By.id("editor-wrapper")))` and gets `NoSuchFrameException: no such frame: element is not a frame`. What is the likely cause?
- [ ] A) The frame's name was misspelled
- [ ] B) The `WebElement` passed is not an `<iframe>` or `<frame>` tag, for example a wrapper `div`
- [ ] C) The frame has not finished loading, so a wait is needed
- [ ] D) `defaultContent()` was called before entering the frame

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The `WebElement` passed is not an `<iframe>` or `<frame>` tag, for example a wrapper `div`

**Explanation:** The "element is not a frame" message means the element you passed is not the iframe itself; choose the `<iframe>` tag. *(window-handling.md)*
- **Why others are wrong:**
  - A) A name, id or index that matches no frame in the current context produces the plain "no such frame" message, not "element is not a frame".
  - C) The message does not describe a timing problem; late-loading frames are handled with `frameToBeAvailableAndSwitchToIt`.
  - D) Calling `defaultContent()` earlier would not turn a `div` into a frame.
</details>

---

### 141. Why should page classes NOT contain assertions?
- [ ] A) Selenium forbids importing an assertion library inside classes that extend `BasePage`
- [ ] B) Assertions make element lookups slower
- [ ] C) Assertion libraries cannot access a `WebDriver` object
- [ ] D) Pages must stay reusable for positive and negative tests, so they report state and the test decides pass or fail

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Pages must stay reusable for positive and negative tests, so they report state and the test decides pass or fail

**Explanation:** If `loginAs` asserted that the URL contains "inventory", a wrong-password test could never reuse it because the assertion would fail by design. Pages report; tests assert. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) The lesson states a design reason, not a library restriction.
  - B) Speed is not the reason given in the lesson.
  - C) Nothing in the lesson says assertion libraries cannot work with a driver; the point is reusability.
</details>

---

### 142. Why does `LoginPage.loginAs(...)` return an `InventoryPage` rather than `void`?
- [ ] A) Java requires a method to return a different class from the one that declares it
- [ ] B) So that tests can reach the page's private locators
- [ ] C) Because the return type tells the compiler and the reader where the user lands, and it enables method chaining
- [ ] D) So that the page can create a second `WebDriver` for the next page

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Because the return type tells the compiler and the reader where the user lands, and it enables method chaining

**Explanation:** Navigation methods return the next page object, modelling the user journey; methods that stay on the same page return `this`. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) No such Java rule exists; same-page methods such as `enterUsername` return `this`.
  - B) Locators stay private; tests should never see `By` objects.
  - D) The same driver instance is passed from page to page; creating a new driver inside a page is an anti-pattern.
</details>

---

### 143. In Page Factory, when is the element behind an `@FindBy` field actually looked up?
- [ ] A) When `PageFactory.initElements(driver, this)` runs in the constructor
- [ ] B) Each time a method is called on the field, through a lazy proxy
- [ ] C) Once on first use, and then remembered for every later use by default
- [ ] D) When `driver.get(...)` finishes loading the page

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Each time a method is called on the field, through a lazy proxy

**Explanation:** `initElements` assigns a proxy that stores how to find the element; the real `findElement` happens on each use. That is why a page object can be created before the elements exist. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) `initElements` only assigns proxies; it does not search when the object is created.
  - C) Remembering the first result happens only with `@CacheLookup`, which is opt-in.
  - D) Lookups are tied to field use, not to page-load events.
</details>

---

### 144. What does `@FindAll({@FindBy(id = "login"), @FindBy(name = "login")})` mean?
- [ ] A) Both locators must match the same element
- [ ] B) Only the first locator is used; the second is a comment
- [ ] C) Find an element matching `name="login"` inside the element with id `login`
- [ ] D) Either locator may match (an OR)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Either locator may match (an OR)

**Explanation:** `@FindAll` is the OR form; `@FindBys` is the AND chain, such as an `<a>` inside `#menu`. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) Requiring all locators to match is not what `@FindAll` does.
  - B) Both annotations are active locators, not comments.
  - C) Searching inside a container is the chained behaviour of `@FindBys`.
</details>

---

### 145. Why are dynamic locators, such as a button id built from a product name, awkward with Page Factory?
- [ ] A) `@FindBy` values must be compile-time constants, so run-time data cannot be inserted
- [ ] B) `@FindBy` does not support the `id` strategy
- [ ] C) Proxy objects cannot call `click()`
- [ ] D) A Page Factory class may contain only one `WebElement` field

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `@FindBy` values must be compile-time constants, so run-time data cannot be inserted

**Explanation:** The product name is only known at run time, so the lesson's workaround is to use `driver.findElement(By...)` for that one case or to search within a list. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - B) `id` is one of the supported strategies listed for `@FindBy`.
  - C) Proxies implement `WebElement` and work with `click()`.
  - D) Classes declare many annotated fields, including lists.
</details>

---

### 146. Why does `BasePage.isDisplayed(By)` use `findElements` (plural) instead of `findElement`?
- [ ] A) `findElements` waits up to 10 seconds for the element to appear
- [ ] B) `findElement` cannot be used with `By.id`
- [ ] C) It returns an empty list instead of throwing when nothing matches, so it can ask "is it there?" without waiting
- [ ] D) It automatically scrolls the element into view before checking

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It returns an empty list instead of throwing when nothing matches, so it can ask "is it there?" without waiting

**Explanation:** The helper checks "list is not empty AND the first match is displayed". It is used for optional elements such as the cart badge. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) The helper is described as non-waiting; waiting is done by `waitVisible`.
  - B) `findElement` works with any `By`; the difference is the missing-element behaviour.
  - D) Scrolling is not part of what the lesson describes.
</details>

---

**Part B: True/False**

### 147. True or False: Two tabs opened by the same driver behave as two separate user sessions with independent logins.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Tabs in the same browser profile share cookies, so logging in as `standard_user` in one tab usually logs you in in the other. Truly separate users need a second `WebDriver` instance. *(window-handling.md)*
- **Why others are wrong:**
  - A) The misconception is that a new tab is a fresh session; cookies and storage are shared.
</details>

---

### 148. True or False: After `driver.switchTo().window(handle)`, the tab does not necessarily come to the foreground on screen; only Selenium's focus moves.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The lesson says nothing visibly changes on screen when you switch; only Selenium's focus moves, so you cannot judge the active window by what you see. *(window-handling.md)*
- **Why others are wrong:**
  - B) Believing a visible tab change confirms the switch is the misconception; use `getTitle()` or `getCurrentUrl()` to check instead.
</details>

---

### 149. True or False: Fields annotated with `@FindBy` must not be declared `final`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Selenium assigns the proxies after construction, so annotated fields cannot be `final`; declaring them `final` leaves them uninitialised. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - B) Copying the `private final By` style from plain POM onto `WebElement` fields is the mistake; plain `By` fields can be `final` because they are assigned in place.
</details>

---

### 150. True or False: Putting `@CacheLookup` on every field is a good default because it makes Page Factory faster with no downside.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `@CacheLookup` should be used only for truly static elements such as a logo; on a page that re-renders it causes `StaleElementReferenceException`. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) The misconception ignores that the cached element belongs to the old DOM once the page re-renders, so later use fails.
</details>

---

**Part C: Code Prediction**

### 151. The page starts with one window. What happens when this code runs?
```java
String original = driver.getWindowHandle();
driver.findElement(By.linkText("Click Here")).click();
new WebDriverWait(driver, Duration.ofSeconds(10))
        .until(ExpectedConditions.numberOfWindowsToBe(2));
for (String h : driver.getWindowHandles()) {
    if (!h.equals(original)) { driver.switchTo().window(h); break; }
}
driver.close();
System.out.println(driver.getTitle());
```
- [ ] A) It prints the original page's title, because `close()` returns to the first window
- [ ] B) It prints `New Window`, the title of the page that was just closed
- [ ] C) It throws `NoSuchWindowException` (target window already closed)
- [ ] D) It throws `NoSuchElementException` because no locator matches

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It throws `NoSuchWindowException` (target window already closed)

**Explanation:** `close()` closes only the current (new) window, and Selenium does not automatically go back to another one. Without `switchTo().window(original)`, `getTitle()` fails. *(window-handling.md)*
- **Why others are wrong:**
  - A) There is no automatic return to the original window after `close()`.
  - B) The window is closed, so its title cannot be read.
  - D) No element lookup happens; the error is about the window target.
</details>

---

### 152. The driver is on the page `nested_frames`, where `frame-left` and `frame-middle` are children of `frame-top`. What happens?
```java
driver.switchTo().frame("frame-top");
driver.switchTo().frame("frame-middle");
String middle = driver.findElement(By.id("content")).getText();
driver.switchTo().defaultContent();
driver.switchTo().frame("frame-left");
```
- [ ] A) It enters `frame-left` and the next lookup reads `LEFT`
- [ ] B) It throws `NoSuchWindowException`
- [ ] C) It throws `NoSuchElementException` on the `frame-left` line
- [ ] D) It throws `NoSuchFrameException`, because `frame-left` is not in the top-level context

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It throws `NoSuchFrameException`, because `frame-left` is not in the top-level context

**Explanation:** `defaultContent()` goes all the way back to the top-level page, where only `frame-top` and `frame-bottom` exist. `frame-left` is a child of `frame-top`, so the name matches no frame in the current context. `parentFrame()` would have been the right call. *(window-handling.md)*
- **Why others are wrong:**
  - A) That would work only after `parentFrame()`, which stays inside `frame-top`.
  - B) No window is involved; the failing context is a frame.
  - C) The failure is at the frame switch, and a frame lookup that finds no match raises `NoSuchFrameException`.
</details>

---

### 153. The browser starts with one window. What is printed?
```java
String original = driver.getWindowHandle();
driver.switchTo().newWindow(WindowType.TAB);
driver.get("https://www.saucedemo.com");
System.out.println(driver.getWindowHandles().size());
driver.close();
driver.switchTo().window(original);
System.out.println(driver.getWindowHandles().size());
```
- [ ] A) `1` then `1`
- [ ] B) `2` then `1`
- [ ] C) `2` then `2`
- [ ] D) `3` then `1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `2` then `1`

**Explanation:** The original plus the new tab make 2 handles. `close()` closes only the current (new) tab, so after switching back one window remains. *(window-handling.md)*
- **Why others are wrong:**
  - A) The new tab is open at the first print, so the count is 2, not 1.
  - C) `close()` removes the new tab, so the second print is not 2.
  - D) Only one new tab was created, so the first count is 2, not 3.
</details>

---

### 154. The cart is empty, so the badge element does not exist. What does `getCartCount()` return?
```java
public int getCartCount() {
    return isDisplayed(cartBadge) ? Integer.parseInt(textOf(cartBadge)) : 0;
}
// isDisplayed(By) = !driver.findElements(locator).isEmpty() && driver.findElement(locator).isDisplayed()
```
- [ ] A) It throws `NoSuchElementException`
- [ ] B) It throws `TimeoutException` after 10 seconds
- [ ] C) It throws `NumberFormatException`
- [ ] D) It returns `0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It returns `0`

**Explanation:** `findElements` returns an empty list, so `isDisplayed` is `false` without throwing or waiting, and the ternary returns `0`. `textOf` is never called. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) `findElements` does not throw when nothing matches.
  - B) The waiting `textOf` is not reached; `isDisplayed` is the non-waiting check.
  - C) `parseInt` is never called because the false branch is taken.
</details>

---

### 155. A test uses `loginAs` with the locked-out user. What happens?
```java
InventoryPage inventory = new LoginPage(driver)
        .open()
        .loginAs("locked_out_user", "secret_sauce");
// InventoryPage constructor: super(driver); waitForUrlContaining("inventory");
```
- [ ] A) It returns an `InventoryPage` and `isLoaded()` later returns `false`
- [ ] B) It throws `NoSuchElementException` on the error message
- [ ] C) It throws `TimeoutException` from the `InventoryPage` constructor after the wait fails
- [ ] D) It throws `NullPointerException` because the page was not initialised

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It throws `TimeoutException` from the `InventoryPage` constructor after the wait fails

**Explanation:** `loginAs` always constructs `InventoryPage`, whose constructor waits for the URL to contain "inventory". The locked-out user stays on the login page, so the wait times out. Negative tests should use `loginExpectingFailure`. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) The constructor guard stops the object from being returned when the URL is wrong.
  - B) No error-message lookup happens inside `loginAs`.
  - D) The plain POM classes use `By` fields, not proxies, so no `null` field is involved.
</details>

---

### 156. What happens when `enterUser("standard_user")` is called?
```java
public class LoginPageFactory {
    private final WebDriver driver;

    @FindBy(id = "user-name")
    private WebElement usernameField;

    public LoginPageFactory(WebDriver driver) {
        this.driver = driver;
    }

    public void enterUser(String u) { usernameField.sendKeys(u); }
}
```
- [ ] A) It throws `NullPointerException` because `usernameField` was never initialised
- [ ] B) It throws `NoSuchElementException` because the proxy cannot find the element
- [ ] C) It throws `StaleElementReferenceException`
- [ ] D) It types the text normally; `@FindBy` initialises the field automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It throws `NullPointerException` because `usernameField` was never initialised

**Explanation:** The constructor never calls `PageFactory.initElements(driver, this)`, so the annotated field stays `null` and the first use throws `NullPointerException`. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - B) No proxy was ever assigned, so no lookup occurs.
  - C) Staleness applies to a previously found element, which does not exist here.
  - D) The annotation only records how to find the element; `initElements` must be called.
</details>

---

### 157. Which locator does this code build?
```java
String name = "Sauce Labs Bike Light";
By add = By.id("add-to-cart-" + name.toLowerCase().replace(' ', '-'));
```
- [ ] A) `By.id("add-to-cart-Sauce-Labs-Bike-Light")`
- [ ] B) `By.id("add-to-cart-sauce labs bike light")`
- [ ] C) `By.id("add-to-cart-saucelabsbikelight")`
- [ ] D) `By.id("add-to-cart-sauce-labs-bike-light")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `By.id("add-to-cart-sauce-labs-bike-light")`

**Explanation:** `toLowerCase()` lowercases the name and `replace(' ', '-')` swaps each space for a hyphen, matching SauceDemo's id pattern. *(page-object-model-and-page-factory.md)*
- **Why others are wrong:**
  - A) The name is lowercased, so capital letters do not remain.
  - B) Spaces are replaced with hyphens, so none remain.
  - C) Spaces become hyphens; they are not deleted.
</details>

---

**Part D: Fill-in-the-Blank**

### 158. To open a blank new tab and switch to it in one step, call `driver.switchTo()._____(WindowType.TAB)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `newWindow` (also accepted: `newWindow()`)

**Explanation:** `newWindow(WindowType.TAB)` or `WindowType.WINDOW` both opens and switches, so no waiting loop is needed. *(window-handling.md)*
</details>

---

### 159. After clicking a link that opens a second tab, wait for exactly two windows with `ExpectedConditions._____(2)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `numberOfWindowsToBe` (also accepted: `numberOfWindowsToBe()`)

**Explanation:** It polls until exactly the given number of windows exist; without it `getWindowHandles()` right after the click may still show one handle. *(window-handling.md)*
</details>

---

### 160. In Page Factory, the call `PageFactory._____(driver, this)` assigns lazy proxies to the annotated `WebElement` fields.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `initElements` (also accepted: `initElements()`)

**Explanation:** `initElements` inspects the annotated fields and gives each a proxy; forgetting it leaves the fields `null` and causes `NullPointerException`. *(page-object-model-and-page-factory.md)*
</details>

---

### 161. In the Page Object Model, assertions belong in the _____, while page classes only report state.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `tests` (also accepted: test classes, test methods, the test, test code)

**Explanation:** Page objects report state such as `isLoaded()`; the test decides pass or fail, which keeps pages reusable for positive and negative tests. *(page-object-model-and-page-factory.md)*
</details>

---

## Day 4 - Thursday: BDD and Cucumber

#### Set 1 of 2

**Part A: Multiple Choice**

### 162. Which problem was BDD invented to solve at its root?
- [ ] A) Developers writing code too slowly to meet sprint deadlines
- [ ] B) Business people, developers and testers misunderstanding each other about what should be built
- [ ] C) Selenium scripts that take too long to run in a pipeline
- [ ] D) A shortage of tools for running automated tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Business people, developers and testers misunderstanding each other about what should be built

**Explanation:** The lesson says projects rarely fail because developers cannot code; they fail because people misunderstand each other, and BDD attacks this by agreeing on behavior through examples before code is written. *(bdd-fundamentals.md)*
- **Why others are wrong:**
  - A) Speed of coding is not the problem the lesson describes.
  - C) Test execution time is not the motivation for BDD.
  - D) The lesson stresses that tools are the least important part of BDD.
</details>

---

### 163. According to the Features and Scenarios lesson, which feature file is "just right" in size and scope?
- [ ] A) `store.feature` containing login, cart, checkout and sorting scenarios
- [ ] B) `add-to-cart-button-color.feature`
- [ ] C) `login-and-shipping-and-reports.feature`
- [ ] D) `shopping-cart.feature` with 5-12 scenarios about one capability

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `shopping-cart.feature` with 5-12 scenarios about one capability

**Explanation:** A feature file should cover one cohesive capability that has one clear user goal; the lesson rates `shopping-cart.feature` as just right. *(features-and-scenarios.md)*
- **Why others are wrong:**
  - A) Too big: several user goals and around 60 scenarios make it impossible to navigate.
  - B) Too small: a button colour is a detail of the cart, not a capability.
  - C) Mixes unrelated functionality, which the lesson explicitly warns against.
</details>

---

### 164. In an example-mapping session, which card colour is used for a question that nobody in the room can answer yet?
- [ ] A) Red
- [ ] B) Yellow
- [ ] C) Blue
- [ ] D) Green

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Red

**Explanation:** Red cards capture questions that nobody can answer yet; they are parked and must be resolved before development starts. *(bdd-fundamentals.md)*
- **Why others are wrong:**
  - B) Yellow is the single story card.
  - C) Blue cards hold the rules.
  - D) Green cards hold the examples illustrating each rule.
</details>

---

### 165. After an example-mapping session the table has one yellow card and a very large number of blue cards, but no red cards. What does the lesson say this means?
- [ ] A) The story is well understood and ready for development
- [ ] B) The story is not understood and must go back to the product owner
- [ ] C) The story is too big and should be split into several stories
- [ ] D) The team should add more green cards before splitting anything

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The story is too big and should be split into several stories

**Explanation:** Too many blue (rule) cards is the sign of an oversized story, so it is split. *(bdd-fundamentals.md)*
- **Why others are wrong:**
  - A) "Ready" corresponds to few cards, mostly green, and no red.
  - B) "Not understood" is the signal of lots of red cards, not lots of blue.
  - D) The lesson's remedy for many rules is splitting, not adding examples.
</details>

---

### 166. A story says "The checkout should be quick." Which rewrite is a testable acceptance criterion?
- [ ] A) "Checkout should feel fast and responsive on all devices"
- [ ] B) "A logged-in customer with items in the cart can complete checkout in at most 3 screens"
- [ ] C) "Checkout runs at an appropriate speed for the customer"
- [ ] D) "Checkout is easy to use"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) "A logged-in customer with items in the cart can complete checkout in at most 3 screens"

**Explanation:** The lesson replaces vague words with numbers, lists and exact messages; a limit of 3 screens can be checked objectively. *(user-stories-and-acceptance-criteria.md)*
- **Why others are wrong:**
  - A) "Fast" and "responsive" are vague words with no measurable value.
  - C) "Appropriate" is a suspicious word that gives no exact value.
  - D) "Easy" is untestable until it is tied to steps or success rates.
</details>

---

### 167. Which description matches the role of Cucumber in the BDD toolchain?
- [ ] A) The tool that reads Gherkin files and executes them by matching each step to code
- [ ] B) The plain-language syntax in which scenarios are written
- [ ] C) A Java method annotated with `@Given`, `@When` or `@Then`
- [ ] D) The library that drives the browser inside the step definitions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The tool that reads Gherkin files and executes them by matching each step to code

**Explanation:** Cucumber is the execution tool; Gherkin is the syntax, step definitions are the Java methods, and Selenium with page objects drives the browser. *(bdd-fundamentals.md)*
- **Why others are wrong:**
  - B) That is Gherkin.
  - C) That is a step definition.
  - D) That is Selenium (and the page objects around it).
</details>

---

### 168. A backlog contains the story "As a developer, I want to create the `orders` table." Which INVEST quality does it most clearly violate?
- [ ] A) Independent
- [ ] B) Small
- [ ] C) Testable
- [ ] D) Valuable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Valuable

**Explanation:** Creating a database table is a technical task that delivers no value to a user; the lesson uses exactly this as its example of a Valuable violation. *(user-stories-and-acceptance-criteria.md)*
- **Why others are wrong:**
  - A) Nothing in the text says it depends on another story.
  - B) A single table is small; size is not the issue.
  - C) The lesson's Testable violations are things like "user friendly", not a table.
</details>

---

### 169. Which of the following is an example of the team-wide Definition of Done rather than an acceptance criterion?
- [ ] A) A locked-out user sees an error message
- [ ] B) A 10% discount applies to orders of $100 or more
- [ ] C) All automated regression tests pass
- [ ] D) Remembering the selected sort order is out of scope

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) All automated regression tests pass

**Explanation:** The Definition of Done is a quality standard applied to every story; acceptance criteria describe the functional behavior of one specific story. *(user-stories-and-acceptance-criteria.md)*
- **Why others are wrong:**
  - A) Specific functional behavior of one story: acceptance criterion.
  - B) A concrete business rule for one story: acceptance criterion.
  - D) An explicit out-of-scope line belongs to a story's criteria.
</details>

---

### 170. A step definition exists for the text `the user is logged in`, and a feature file contains `When the user is logged in`. What does Cucumber do?
- [ ] A) Reports the step as undefined because the keyword differs from `Given`
- [ ] B) Matches the step definition, because only the text is used for matching
- [ ] C) Reports the step as ambiguous because two keywords are possible
- [ ] D) Reports the step as pending until the keyword is corrected

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Matches the step definition, because only the text is used for matching

**Explanation:** Cucumber treats all step keywords identically when matching; the keywords exist for human readers. *(gherkin.md)*
- **Why others are wrong:**
  - A) Keywords do not take part in matching, so the step is not undefined.
  - C) Ambiguous means more than one definition matches the text, which is not the case here.
  - D) Pending means a definition exists but is marked not yet implemented.
</details>

---

### 171. How does the Features and Scenarios lesson recommend grouping feature files into folders?
- [ ] A) By sprint number, such as `sprint-12/`
- [ ] B) By the technical layer they exercise
- [ ] C) By test purpose, such as `smoke/` and `regression/`
- [ ] D) By business domain, such as `authentication/`, `catalog/`, `ordering/`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) By business domain, such as `authentication/`, `catalog/`, `ordering/`

**Explanation:** Folders follow business domains so that anyone can find the behavior of a capability. *(features-and-scenarios.md)*
- **Why others are wrong:**
  - A) "sprint-12" means nothing after a year.
  - B) The lesson says to group by business domain, not by technical layer.
  - C) Smoke and regression are purposes handled with tags (a later topic), not with folders.
</details>

---

### 172. Which scenario title best follows the "subject + behavior + condition" recipe?
- [ ] A) Checkout is rejected when the postal code is missing
- [ ] B) Verify that the negative checkout test works
- [ ] C) Test 7
- [ ] D) Click the continue button with an empty field

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Checkout is rejected when the postal code is missing

**Explanation:** It names a subject (checkout), a behavior (is rejected) and a condition (postal code missing), so a failing report is understood at a glance. *(features-and-scenarios.md)*
- **Why others are wrong:**
  - B) "Verify that..." talks about testing instead of behavior.
  - C) Numbered titles say nothing about the behavior.
  - D) It mentions the UI instead of stating the behavior.
</details>

---

### 173. According to the "scale of abstraction", which step is at the right level of detail?
- [ ] A) `When I click the element with id "checkout"`
- [ ] B) `When the shopper buys a product`
- [ ] C) `When the shopper checks out with the shipping details:` followed by a table of first name, last name and postal code
- [ ] D) `When I click the third button and wait 3 seconds`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `When the shopper checks out with the shipping details:` followed by a table of first name, last name and postal code

**Explanation:** The right level is the lowest one at which the business still recognizes the behavior, showing only the data that matters. *(features-and-scenarios.md)*
- **Why others are wrong:**
  - A) Level 1, mechanics: UI detail that belongs in page objects.
  - B) Level 3, whole journey: often hides data that matters.
  - D) Also mechanics, plus a wait that belongs in code.
</details>

---

### 174. The criterion says "Free shipping applies to orders of $50 or more." Which set of order totals best tests the boundary?
- [ ] A) 49.99, 50.00 and 50.01
- [ ] B) 10.00, 20.00 and 30.00
- [ ] C) 100.00, 200.00 and 500.00
- [ ] D) 0.00, 25.00 and 1000.00

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 49.99, 50.00 and 50.01

**Explanation:** Whenever a criterion contains a number, test the value exactly at it, one below and one above, because defects hide where "more than" and "at least" are confused. *(user-stories-and-acceptance-criteria.md)*
- **Why others are wrong:**
  - B) All values are far below the limit; no boundary is exercised.
  - C) All values are far above the limit.
  - D) These values are far from $50, so the "or more" question stays untested.
</details>

---

**Part B: True/False**

### 175. True or False: Writing `Given the user is logged in  # context` is a valid way to add a comment, because Cucumber ignores everything after the `#`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A comment must start at the beginning of a line (after optional whitespace). A `#` after step text becomes part of the step text, so the step will not match its definition and is reported as undefined. *(gherkin.md)*
- **Why others are wrong:**
  - A) This is the misconception: Gherkin has no end-of-line comments.
</details>

---

### 176. True or False: A team that runs example-mapping workshops and writes plain-text scenarios, without using any automation tool, is already getting most of the benefit of BDD.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** BDD is a conversation first, a documentation format second and an automation tool third; a team that installs Cucumber but never talks to the business is not doing BDD. *(bdd-fundamentals.md)*
- **Why others are wrong:**
  - B) Believing that Cucumber is what makes BDD is the "BDD is just testing with Cucumber" myth.
</details>

---

### 177. True or False: A scenario may rely on the cart contents left behind by the previous scenario, as long as the scenarios always run in file order.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Each scenario must create its own starting state in its `Given` steps so it can run alone, in any order or in parallel; dependent scenarios cause cascading false failures. *(features-and-scenarios.md)*
- **Why others are wrong:**
  - A) Order dependence is an anti-pattern; re-running one failing scenario or parallel runs would break it.
</details>

---

### 178. True or False: A technical task such as "create the `orders` table" belongs inside a user story that delivers user value, rather than being a story of its own.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Tasks are hours of technical work done to implement a story and need no "so that"; the table is a task inside a story such as "customer's completed order is recorded". *(user-stories-and-acceptance-criteria.md)*
- **Why others are wrong:**
  - B) The misconception is that any piece of work can be written as "As a developer, I want...", which describes a task, not a story.
</details>

---

**Part C: Code Prediction**

### 179. A scenario has five steps. Step 2's code throws an assertion error, and step 4 has no matching step definition. What is reported for step 3 and for the scenario?

```gherkin
Scenario: Checkout shows the correct total
  Given the shopper has the "Sauce Labs Backpack" in the cart
  When the shopper starts checkout
  Then the item total is 29.99
  And the tax is 2.40
  And the order can be confirmed
```
- [ ] A) Step 3 passed; the scenario passed
- [ ] B) Step 3 skipped; the scenario failed
- [ ] C) Step 3 undefined; the scenario undefined
- [ ] D) Step 3 failed; the scenario failed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Step 3 skipped; the scenario failed

**Explanation:** After a step fails, the remaining steps are skipped; the scenario as a whole is failed, and you fix the first failing step first. *(gherkin.md)*
- **Why others are wrong:**
  - A) Steps after a failure are never executed, and one failure fails the scenario.
  - C) Step 3 has a definition; only step 4 is undefined.
  - D) Step 3 is not executed at all, so it cannot fail.
</details>

---

### 180. The step definition pattern is `the cart contains {int} items`. What does Cucumber report for the feature line below?

```gherkin
Then the cart contains 1 item
```
- [ ] A) Passed, with the value 1 passed to the method
- [ ] B) Ambiguous, because singular and plural both match
- [ ] C) Undefined, because `item` does not match `items`
- [ ] D) Pending, because the number is not quoted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Undefined, because `item` does not match `items`

**Explanation:** Matching is done on the text, and `1 item` (singular) does not match `{int} items`; the lesson calls this a typical beginner surprise and the reason to keep wording consistent. *(gherkin.md)*
- **Why others are wrong:**
  - A) The literal text `items` is part of the pattern and is absent.
  - B) Ambiguous requires two matching definitions, but none matches.
  - D) Pending applies to an existing but unimplemented definition; numbers are written unquoted anyway.
</details>

---

### 181. The step definitions use exactly the texts `the customer is on the login page`, `the customer logs in with username {string} and password {string}` and `the customer sees the products page`. Which step of this scenario is reported as undefined?

```gherkin
Scenario: Valid login
  # Shared demo password
  Given the customer is on the login page
  When the customer logs in with username "standard_user" and password "secret_sauce"
  Then the customer sees the products page # landing page
```
- [ ] A) None, because all three texts have definitions
- [ ] B) The `Given` step
- [ ] C) The `When` step
- [ ] D) The `Then` step

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The `Then` step

**Explanation:** The comment on its own line is ignored, but `# landing page` after the `Then` text becomes part of the step text, so it no longer matches its definition. *(gherkin.md)*
- **Why others are wrong:**
  - A) The trailing `# landing page` changes the text of the last step.
  - B) The `Given` line has no trailing text.
  - C) The `When` step matches with two `{string}` values; the comment line above `Given` is ignored.
</details>

---

### 182. Given this feature step and Java method, what is printed?

```gherkin
When the shopper adds the following products to the cart:
  | product               | quantity |
  | Sauce Labs Backpack   | 1        |
  | Sauce Labs Bike Light | 2        |
```
```java
for (java.util.Map<String, String> row : table.asMaps()) {
    System.out.println(row.get("quantity") + " x " + row.get("product"));
}
```
- [ ] A) `1 x Sauce Labs Backpack` then `2 x Sauce Labs Bike Light`
- [ ] B) `quantity x product`, then `1 x Sauce Labs Backpack`, then `2 x Sauce Labs Bike Light`
- [ ] C) Nothing is printed, because `asMaps()` needs an `Examples` table
- [ ] D) Only `2 x Sauce Labs Bike Light`, the last row

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `1 x Sauce Labs Backpack` then `2 x Sauce Labs Bike Light`

**Explanation:** `asMaps()` turns every row after the header into a map from column name to cell value; the header row supplies the keys, so two lines are printed. *(gherkin.md)*
- **Why others are wrong:**
  - B) The header row provides keys and is not a data row.
  - C) A data table attached to a step is passed to its method; no `Examples` table is involved.
  - D) The loop visits every row, not just the last.
</details>

---

### 183. The Gherkin parser reports an error at `(2:1)` for this file. What is the cause?

```gherkin
Feature: Checkout
Scenario Pay by card
  Given the shopper has an item in the cart
```
- [ ] A) The `Feature` has no description
- [ ] B) The `Given` should be an `And`
- [ ] C) The colon after `Scenario` is missing
- [ ] D) Two `Feature` lines are present

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The colon after `Scenario` is missing

**Explanation:** Structural keywords need a colon; `(2:1)` means line 2, column 1, where the parser found `Scenario Pay by card`, which is not a valid line there. *(gherkin.md)*
- **Why others are wrong:**
  - A) The description is optional.
  - B) A first step in a scenario is normally a `Given`; `And` continues a previous step.
  - D) Only one `Feature:` line exists in this snippet.
</details>

---

### 184. What is the main problem with this scenario, and why does it matter if the first `Then` fails?

```gherkin
Scenario: Cart works
  Given the shopper is logged in
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1
  When the shopper removes "Sauce Labs Backpack" from the cart
  Then the cart count shows 0
```
- [ ] A) Two `When` steps need a `Background`, otherwise the scenario cannot run
- [ ] B) Product names may not be quoted in a `When` step
- [ ] C) Numbers must be quoted so that Cucumber can read them
- [ ] D) It tests two behaviors (adding and removing); the later steps are then skipped and never tested, and the title says nothing precise

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It tests two behaviors (adding and removing); the later steps are then skipped and never tested, and the title says nothing precise

**Explanation:** One scenario should describe one behavior. If an early step fails, the rest are skipped, so you do not know whether removing works, and "Cart works" does not tell you what broke. *(features-and-scenarios.md)*
- **Why others are wrong:**
  - A) The scenario is valid Gherkin; the lesson's fix is to split it, not to share setup.
  - B) Quoted text is the convention for variable data such as product names.
  - C) Numbers are written unquoted.
</details>

---

### 185. Cucumber prints the snippet below for an undefined step. Which feature line produced it?

```java
@When("the customer logs in with username {string} and password {string}")
public void the_customer_logs_in_with_username_and_password(String string, String string2) {
    throw new io.cucumber.java.PendingException();
}
```
- [ ] A) `When the customer logs in with username standard_user and password secret_sauce`
- [ ] B) `When the customer logs in with username "standard_user" and password "secret_sauce"`
- [ ] C) `When the customer logs in with username 3 and password 4`
- [ ] D) `When the customer logs in with the following credentials:` followed by a table

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `When the customer logs in with username "standard_user" and password "secret_sauce"`

**Explanation:** Cucumber noticed the quoted values and turned them into `{string}` parameters of type `String`. *(gherkin.md)*
- **Why others are wrong:**
  - A) Unquoted words would not be detected as `{string}` values.
  - C) Unquoted whole numbers would produce `{int}` parameters.
  - D) A table step would give a `DataTable` parameter instead.
</details>

---

**Part D: Fill-in-the-Blank**

### 186. The BDD cycle consists of Discovery, _____, and Automation, in that order.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Formulation` (also accepted: Formulate, Formulating)

**Explanation:** In the second phase the examples found in discovery are written down as structured Gherkin scenarios, producing readable `.feature` files. *(bdd-fundamentals.md)*
</details>

---

### 187. A story should be split into _____ slices: thin pieces that deliver something usable from the screen through to the data, rather than a horizontal layer such as "all the screens".

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `vertical` (also accepted: end-to-end vertical, vertical slices)

**Explanation:** A vertical slice such as "log in and see the product list" works end to end, so the team gets early feedback. *(user-stories-and-acceptance-criteria.md)*
</details>

---

### 188. In Gherkin, multi-line text such as an email body or a JSON message is passed to a step using a block delimited by `"""`, which is called a _____.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `doc string` (also accepted: docstring, DocString)

**Explanation:** Everything between the opening and closing delimiters is passed to the step definition as one `String`. *(gherkin.md)*
</details>

---

### 189. Feature files are called _____ documentation because executable scenarios go red as soon as the description and the system disagree.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `living` (also accepted: living documentation)

**Explanation:** Because the scenarios are run regularly, they stay as accurate as the passing tests, unlike a requirements document that goes stale. *(bdd-fundamentals.md)*
</details>

---

#### Set 2 of 2

**Part A: Multiple Choice**

### 190. Which of these is the best-formed **Given** step for a cart scenario?
- [ ] A) `Given the shopper clicks the login button`
- [ ] B) `Given the shopper is logged in`
- [ ] C) `Given I open Chrome`
- [ ] D) `Given the system is working`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `Given the shopper is logged in`

**Explanation:** A Given describes a *state* that is already true ("It is already true that the shopper is logged in" reads fine), so it is the precondition and not the behavior under test. *(given-when-then.md)*
- **Why others are wrong:**
  - A) It is an action, not a state; it belongs in a When or should be reworded as "is on the login page".
  - C) Opening the browser is a technical environment detail that should be hidden in setup code.
  - D) It is vague and untestable; the lesson says to remove it or state a specific precondition.
</details>

---

### 191. Why is `Then an error is shown` a weaker outcome than `Then the error message "Epic sadface: Password is required" is displayed`?
- [ ] A) It cannot be mapped to a step definition at all
- [ ] B) Cucumber rejects any Then step that has no quoted string
- [ ] C) A Then step must always contain a number to be valid
- [ ] D) It would still pass if a different error (for example a missing-username message) appeared

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It would still pass if a different error (for example a missing-username message) appeared

**Explanation:** A Then should state the expected result specifically (exact message, exact number); the vague version does not pin down the behavior the story promised. *(given-when-then.md)*
- **Why others are wrong:**
  - A) A vague step can be matched and implemented like any other; the problem is its precision, not mappability.
  - B) The lesson never says Cucumber requires quotes in a Then; it is about specificity.
  - C) Nothing requires a number in a Then step.
</details>

---

### 192. A feature file contains `Then the shopper adds "Sauce Labs Backpack" to the cart`, and the only matching definition is `@When("the shopper adds {string} to the cart")`. What happens when it runs?
- [ ] A) The step matches and the method runs, because Cucumber strips the keyword and matches only the text
- [ ] B) The step is undefined, because `Then` does not match a `@When` annotation
- [ ] C) The step is reported ambiguous, because two keywords claim the same text
- [ ] D) The project fails to compile, because the keyword and annotation disagree

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The step matches and the method runs, because Cucumber strips the keyword and matches only the text

**Explanation:** Matching is based on the text only; `Given`, `When` and `Then` are for humans, so the discipline of using them correctly is on the team, not the tool. *(given-when-then.md, step-definitions.md)*
- **Why others are wrong:**
  - B) The annotation type does not restrict matching, so the step is not undefined.
  - C) Ambiguity needs two definitions matching the same text; here there is only one.
  - D) The feature file is not compiled against annotations, so nothing fails to compile.
</details>

---

### 193. The Sauce Demo team renames its login button from "Login" to "Sign in". Which step wording would force **no** changes in any feature file?
- [ ] A) `When the user clicks the Login button`
- [ ] B) `When the user types "ada" in the username field and clicks Login`
- [ ] C) `When the customer logs in as "ada"`
- [ ] D) `When the user clicks the element with id "login-button"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `When the customer logs in as "ada"`

**Explanation:** Declarative steps say *what* the user wants to achieve, so only one page-object method changes when the UI changes; imperative steps tied to the UI must be edited everywhere they appear. *(given-when-then.md)*
- **Why others are wrong:**
  - A) It names the button text, so it becomes wrong after the rename.
  - B) It is imperative and mentions "Login", so every scenario using it needs editing.
  - D) It embeds a locator, which is UI-level detail that does not belong in business text.
</details>

---

### 194. Which of these is a best practice for step definitions?
- [ ] A) Keep each method thin: call a page-object method or two and, in `Then`, assert
- [ ] B) Add `Thread.sleep` after clicks so the page has time to update
- [ ] C) Store the `WebDriver` in a static variable so every step class can reach it
- [ ] D) Put the final assertion inside the `When` that performs the action

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Keep each method thin: call a page-object method or two and, in `Then`, assert

**Explanation:** Steps should do one thing, with business logic and locators in page objects; assertions belong only in `@Then` methods. *(step-definitions.md)*
- **Why others are wrong:**
  - B) The lesson says no `Thread.sleep`; waiting belongs to the page objects' explicit waits.
  - C) Static variables should be avoided: they survive across scenarios and make tests depend on each other.
  - D) Assertions in a `When` mix Arrange/Act/Assert; assertions belong in `@Then`.
</details>

---

### 195. A team puts `cucumber.plugin=pretty` in `cucumber.properties` and then runs `mvn test -Dcucumber.plugin=pretty`. What does the lesson say about the command-line value?
- [ ] A) It is ignored, because the properties file is always read last
- [ ] B) It is added to a list together with the file value and runs twice
- [ ] C) It overrides the value in the properties file
- [ ] D) It causes an error because a key may not be set twice

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It overrides the value in the properties file

**Explanation:** Settings can come from runner annotations, `cucumber.properties`, or command-line/system properties, and the command-line ones override the file. *(cucumber-framework-setup.md)*
- **Why others are wrong:**
  - A) The lesson states the opposite: the command line overrides the file.
  - B) Nothing in the lesson says values are accumulated or run twice.
  - D) Setting the same key in several places is allowed; the lesson only advises a single source of truth to avoid confusion.
</details>

---

### 196. A run fails with a `NullPointerException` on `context` inside a step method. Which cause does the lesson list?
- [ ] A) The glue package in the runner has a typo
- [ ] B) The constructor injection was not used because `cucumber-picocontainer` is missing from the `pom.xml`
- [ ] C) The feature file was placed under `src/test/java`
- [ ] D) The runner class name does not end in `Test`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The constructor injection was not used because `cucumber-picocontainer` is missing from the `pom.xml`

**Explanation:** Without the PicoContainer dependency the `TestContext` is not injected, so the field stays null; the fix is to add `cucumber-picocontainer`. *(step-definitions.md)*
- **Why others are wrong:**
  - A) A wrong glue package makes steps *undefined*; it does not produce a null `context`.
  - C) A misplaced feature file means the scenario is not found, not a null field in a step.
  - D) A bad runner name leads to no tests being found, so no step would run at all.
</details>

---

### 197. Why must feature files live under `src/test/resources` in a Maven project?
- [ ] A) Maven refuses to open text files that sit next to Java source
- [ ] B) JUnit requires every test resource to be in a folder named `features`
- [ ] C) Files in `src/test/java` are deleted during `mvn clean`
- [ ] D) Maven copies that folder to `target/test-classes`, which is on the classpath where Cucumber looks

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Maven copies that folder to `target/test-classes`, which is on the classpath where Cucumber looks

**Explanation:** Cucumber looks for features on the classpath; a feature file next to the Java files is not copied, so Cucumber never sees it. *(cucumber-framework-setup.md)*
- **Why others are wrong:**
  - A) The lesson gives no such Maven restriction; the issue is copying to the classpath.
  - B) The name `features` is a convention declared in the runner, not a JUnit requirement.
  - C) The lesson's reason is that such files are not copied, not that they are deleted.
</details>

---

### 198. What does `@IncludeEngines("cucumber")` do in the runner class?
- [ ] A) It names the package that contains the step definitions
- [ ] B) It chooses the console formatter, such as `pretty`
- [ ] C) It tells the JUnit Platform suite to use the Cucumber engine to discover and execute the features
- [ ] D) It lists the folders in which `.feature` files are searched

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It tells the JUnit Platform suite to use the Cucumber engine to discover and execute the features

**Explanation:** Each runner annotation is a setting; this one selects the engine, so JUnit hands the work to Cucumber. *(cucumber-framework-setup.md)*
- **Why others are wrong:**
  - A) The glue is set with `@ConfigurationParameter(key = GLUE_PROPERTY_NAME, ...)`.
  - B) Plugins are set with `PLUGIN_PROPERTY_NAME`.
  - D) The feature location is set with `@SelectClasspathResource`.
</details>

---

### 199. A tester's step classes are in package `com.revature.qea.steps`, but the runner's glue says `com.revature.qea.step`. What does the console most likely show?
- [ ] A) The feature is found, but `3 Steps (3 undefined)`
- [ ] B) `Tests run: 0` because the feature file is no longer found
- [ ] C) An `AmbiguousStepDefinitionsException` for every step
- [ ] D) `1 Scenarios (1 passed)` because Cucumber falls back to scanning all packages

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The feature is found, but `3 Steps (3 undefined)`

**Explanation:** The features location is configured separately from the glue, so the scenario is found, but no step definitions are scanned and every step is undefined. This is the most common setup error. *(cucumber-framework-setup.md)*
- **Why others are wrong:**
  - B) The glue setting does not affect where features are found.
  - C) Ambiguity needs more than one matching definition; here there are none.
  - D) A class outside the glue package is invisible to Cucumber; there is no fallback.
</details>

---

### 200. A reviewer flags `Then the shopper clicks the cart and sees 1 item`. What is the recommended fix?
- [ ] A) Change the keyword to `When` for the whole line
- [ ] B) Join the two halves with `And` so they read as separate steps
- [ ] C) Delete the line, since Then steps are optional
- [ ] D) Move the click into a `When` in a scenario about opening the cart and keep the `Then` purely observational

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Move the click into a `When` in a scenario about opening the cart and keep the `Then` purely observational

**Explanation:** This is "action in Then": a Then states an observable outcome and performs no actions. *(given-when-then.md)*
- **Why others are wrong:**
  - A) The line would still mix an action with an observation.
  - B) Splitting with `And` leaves the click inside the Then section, so an action is still part of the outcome.
  - C) Deleting it removes the check instead of repairing it.
</details>

---

### 201. A scenario passes when run alone but fails when run after another scenario that left items in the cart. What is the likely wording cause?
- [ ] A) Too many `And` steps in the Then section
- [ ] B) A missing Given, so the scenario depends on invisible leftover state
- [ ] C) Imperative wording tied to the UI
- [ ] D) A wrong glue package

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A missing Given, so the scenario depends on invisible leftover state

**Explanation:** The fix is to add explicit Givens (for example a logged-in shopper with an empty cart) and never rely on scenario order. *(given-when-then.md)*
- **Why others are wrong:**
  - A) A long chain of `And`s means too many checks, not order dependence.
  - C) Imperative wording makes a UI change break many scenarios; it does not cause order-dependent results.
  - D) A glue typo would make steps undefined in every run, not only after another scenario.
</details>

---

**Part B: True/False**

### 202. True or False: To Cucumber, `And` and `But` have no special meaning; steps are matched by their text only.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `And` and `But` only continue the previous keyword's role for readability; Cucumber does not use any keyword for matching. *(given-when-then.md)*
- **Why others are wrong:**
  - B) The misconception is that `But` (or `And`) triggers different behavior; it is purely for human readers.
</details>

---

### 203. True or False: A scenario may never contain more than one `When`, under any circumstances.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Normally there is one When, but one cohesive action may be written in two lines (for example adding two products). The real question is "one behavior or two?", and a `When ... Then ... When ... Then` pattern should be split. *(given-when-then.md)*
- **Why others are wrong:**
  - A) Treating "exactly one When" as an absolute rule overlooks that a cohesive action can span two lines.
</details>

---

### 204. True or False: A Given step may be implemented in code with actions (such as opening a URL, an API call, or a database insert), as long as it is *worded* as a state.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The specification states where the scenario starts; the automation decides how to reach that state (for example `driver.get(...)`). Givens just must not be worded as actions of the behavior under test. *(given-when-then.md)*
- **Why others are wrong:**
  - B) The misconception is that a state-style Given must be implemented without any action in code; the scenario does not care how the state is reached.
</details>

---

### 205. True or False: Cucumber artifacts such as `cucumber-java` and `cucumber-picocontainer` can safely use different versions, as long as the project compiles.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** All `io.cucumber` artifacts should share one version (hence a single `cucumber.version` property); mismatches can cause `NoSuchMethodError`, `ClassNotFoundException` or failures to create objects. *(cucumber-framework-setup.md)*
- **Why others are wrong:**
  - A) Compiling is not enough: a version mismatch can show up only at run time as errors such as `NoSuchMethodError`.
</details>

---

**Part C: Code Prediction**

### 206. Does this step match the expression, and what happens?

```java
@Then("the cart shows {int} item(s)")
public void theCartShows(int n) { ... }
```

```gherkin
Then the cart shows two items
```

- [ ] A) It matches and `n` is `2`
- [ ] B) It matches and `n` receives the text `two`
- [ ] C) It does not match, so the step is undefined
- [ ] D) It is reported as ambiguous

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It does not match, so the step is undefined

**Explanation:** `{int}` captures digits only, so `two` cannot be captured. With zero matching definitions the step is *undefined*, and Cucumber prints a snippet. *(step-definitions.md)*
- **Why others are wrong:**
  - A) Cucumber does not convert number words to integers.
  - B) The parameter is an `int`, and the text never matches in the first place.
  - D) Ambiguous means two or more definitions match; here none does.
</details>

---

### 207. What is printed when this scenario step runs?

```java
@When("the customer logs in with username {string} and password {string}")
public void logIn(String password, String username) {
    System.out.println(username);
}
```

```gherkin
When the customer logs in with username "standard_user" and password "secret_sauce"
```

- [ ] A) `secret_sauce`
- [ ] B) `standard_user`
- [ ] C) `"secret_sauce"` (with the quotes)
- [ ] D) Nothing: it fails to compile

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `secret_sauce`

**Explanation:** Parameters are passed in the order they appear; Java parameter names do not matter, only order and type. The first `{string}` (`standard_user`) goes to the first Java parameter, named `password`, and the second goes to `username`. The values are swapped. *(step-definitions.md)*
- **Why others are wrong:**
  - B) That would require the Java names to be matched to the expression, which Cucumber does not do.
  - C) The quotes are not included in a `{string}` value.
  - D) The code compiles; the parameter names are unrelated to the expression.
</details>

---

### 208. Two step definitions exist in `CartSteps`. What happens for the feature step below?

```java
@Then("the cart shows {int} items")
public void a(int n) { ... }

@Then("the cart shows {word} items")
public void b(String s) { ... }
```

```gherkin
Then the cart shows 3 items
```

- [ ] A) Method `a` runs, because `{int}` is the more specific type
- [ ] B) An `AmbiguousStepDefinitionsException` is raised, listing both definitions
- [ ] C) Method `b` runs, because it is declared last
- [ ] D) The step is undefined

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An `AmbiguousStepDefinitionsException` is raised, listing both definitions

**Explanation:** `3` is also a word, so both expressions match the same text; more than one match means *ambiguous*, and the fix is to remove or tighten one pattern. *(step-definitions.md)*
- **Why others are wrong:**
  - A) The lesson describes no "most specific wins" rule; two matches are an error.
  - C) Declaration order does not decide the match.
  - D) Undefined means zero matches; here there are two.
</details>

---

### 209. What does this code print?

```gherkin
When the shopper adds the following products to the cart:
  | product               |
  | Sauce Labs Bike Light |
  | Sauce Labs Onesie     |
```

```java
@When("the shopper adds the following products to the cart:")
public void add(DataTable table) {
    List<String> products = table.asList();
    System.out.println(products.size());
}
```

- [ ] A) `0`
- [ ] B) `1`
- [ ] C) `2`
- [ ] D) `3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `3`

**Explanation:** `DataTable` does not know which row is a header, so `asList()` on a one-column table returns every row, including the header `product`: three elements. *(step-definitions.md)*
- **Why others are wrong:**
  - A) The table has content, so the list is not empty.
  - B) The list holds one element per row, not one per table.
  - C) This forgets that the header row is included in `asList()`.
</details>

---

### 210. All three steps of one scenario have definitions. What does the end of the console output look like for `mvn test -Dcucumber.execution.dry-run=true`?
- [ ] A) `1 Scenarios (1 passed)` and `3 Steps (3 passed)`
- [ ] B) `1 Scenarios (1 skipped)` and `3 Steps (3 skipped)`
- [ ] C) `1 Scenarios (1 undefined)` and `3 Steps (3 undefined)`
- [ ] D) `Tests run: 0`, because a dry run does not load features

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `1 Scenarios (1 skipped)` and `3 Steps (3 skipped)`

**Explanation:** A dry run still matches steps (finding undefined or ambiguous ones) but never calls the methods, so no browser opens. "Skipped" here means "not executed because this is a dry run". *(cucumber-framework-setup.md)*
- **Why others are wrong:**
  - A) Passed requires the methods to be executed, which a dry run does not do.
  - C) Undefined would be shown only if a step had no definition.
  - D) The dry run reads the feature and reports its scenario; it does not skip loading.
</details>

---

### 211. `LoginSteps` and `CartSteps` both have a constructor taking a `TestContext`, and both are used in one scenario with `cucumber-picocontainer` on the classpath. What happens?
- [ ] A) Each class gets its own `TestContext`, so two browsers open
- [ ] B) A new `TestContext` is created for every step method call
- [ ] C) Both receive the same `TestContext` instance, so they use the same browser
- [ ] D) One `TestContext` is shared by all scenarios in the feature file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Both receive the same `TestContext` instance, so they use the same browser

**Explanation:** PicoContainer creates one `TestContext` per scenario and passes the same instance to every step class that asks for it, then discards it so scenarios stay isolated. *(step-definitions.md, given-when-then.md)*
- **Why others are wrong:**
  - A) Two browsers would appear if `TestContext` objects were created by hand with `new`, which is the lesson's cause for a browser opening twice.
  - B) Scope is per scenario, not per step method.
  - D) A new context per scenario is exactly what keeps scenarios isolated.
</details>

---

### 212. A scenario has three steps. The first runs normally, the second throws an `AssertionFailedError`, and the third is untouched. What are the statuses of steps 1, 2 and 3?
- [ ] A) passed, failed, passed
- [ ] B) passed, failed, failed
- [ ] C) passed, failed, undefined
- [ ] D) passed, failed, skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) passed, failed, skipped

**Explanation:** Steps run top to bottom and stop at the first failure; later steps become skipped. *(given-when-then.md, step-definitions.md)*
- **Why others are wrong:**
  - A) Later steps are not executed once an earlier step has failed.
  - B) Only the step that threw is failed; the rest are not run.
  - C) Undefined means no matching definition exists, which is not the case here.
</details>

---

**Part D: Fill-in-the-Blank**

### 213. To avoid dozens of near-duplicate step definitions, a team should agree a _____ of consistent wording for the shared concepts and parameterize the values.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `glossary` (also accepted: vocabulary, shared vocabulary, team glossary)

**Explanation:** Identical meaning should use identical phrasing, because Cucumber matches by text and reuse depends on consistent wording. *(given-when-then.md)*
</details>

---

### 214. The package (or packages) in which Cucumber searches for step definitions is called the _____.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `glue` (also accepted: glue package)

**Explanation:** The glue setting tells Cucumber which packages to scan; a step class outside it is invisible to Cucumber, and the setting uses the dotted package name. *(step-definitions.md, cucumber-framework-setup.md)*
</details>

---

### 215. A doc string in a feature step is passed to the step method as a _____ (Java type).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `String` (also accepted: java.lang.String; `DocString` from io.cucumber.docstring)

**Explanation:** The text between the `"""` lines arrives as a single multi-line string, with the indentation of the quotes removed. *(step-definitions.md)*
</details>

---

### 216. Maven's _____ plugin runs the tests on `mvn test` and finds the runner class when its name ends in `Test`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Surefire` (also accepted: maven-surefire-plugin)

**Explanation:** Surefire's default configuration runs classes named `*Test`, `Test*`, `*Tests` or `*TestCase`, so `RunCucumberTest` is picked up. *(cucumber-framework-setup.md)*
</details>

---

## Day 5 - Friday: Advanced Cucumber

#### Set 1 of 2

**Part A: Multiple Choice**

### 217. A `Hooks` class starts a browser in an `@Before` hook. A `Scenario Outline` has one `Examples` table with a header row and 50 data rows. How many browsers are started for this outline in one run?
- [ ] A) `1`, because all rows of an outline share one scenario
- [ ] B) `50`
- [ ] C) `51`, because the header row also runs
- [ ] D) `2`, one for the template and one shared by the rows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `50`

**Explanation:** Every data row expands into a full, independent scenario, so `@Before` and `@After` (and any Background) run once per row; an outline with 50 rows launches 50 browsers. *(scenario-outline-and-examples.md)*
- **Why others are wrong:**
  - A) Rows do not share state or a browser; each gets a fresh `TestContext`.
  - C) The header row only names the placeholders and is never executed as data.
  - D) The template itself is not run; only the expanded rows are.
</details>

---

### 218. Why must the template line be written as `When the customer logs in with username "<username>"` (with quotes) when the step definition uses `{string}`?
- [ ] A) The quotes tell Cucumber that the cell value is a column header
- [ ] B) Quotes are required around every placeholder, including those for `{int}` steps
- [ ] C) Cucumber substitutes only the cell value and does not add quotes, and `{string}` needs the quotes in the step text after substitution
- [ ] D) The quotes make Cucumber skip the hooks for that row

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Cucumber substitutes only the cell value and does not add quotes, and `{string}` needs the quotes in the step text after substitution

**Explanation:** After substitution the engine matches plain text, so the quotes must already be in the template; forgetting them produces an undefined step. *(scenario-outline-and-examples.md)*
- **Why others are wrong:**
  - A) Header names are matched to the placeholder name inside `<>`, not to quotes.
  - B) For `{int}` the quotes must be left off; `"<count>"` would not match.
  - D) Quotes have nothing to do with hooks.
</details>

---

### 219. Why does the lesson recommend putting successful logins and rejected logins in two separate outlines?
- [ ] A) All rows of one outline should lead to the same kind of outcome, so the `Then` step can stay precise and readable
- [ ] B) Cucumber allows only one `Examples` block per outline
- [ ] C) A `Then` step in an outline cannot contain a placeholder
- [ ] D) Outlines with a mix of rows run faster when split

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) All rows of one outline should lead to the same kind of outcome, so the `Then` step can stay precise and readable

**Explanation:** "One outline, one outcome type": mixing page-expected and error-expected rows forces a vague `Then` step and conditional code. *(scenario-outline-and-examples.md)*
- **Why others are wrong:**
  - B) An outline may have several `Examples` blocks.
  - C) `Then` steps may use placeholders (e.g. `"<message>"`).
  - D) The reason is readability, not speed.
</details>

---

### 220. A scenario must add three listed products to a single cart and then check that the cart count is 3. Which construct fits best?
- [ ] A) A `Scenario Outline` with three rows, one per product
- [ ] B) Three `Examples` blocks with one row each
- [ ] C) A `Background` listing the three products
- [ ] D) A data table attached to the `When` step

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A data table attached to the `When` step

**Explanation:** A step-level data table gives structured data to one step in a single run (one cart, one browser); an outline would repeat the whole scenario per row. *(scenario-outline-and-examples.md)*
- **Why others are wrong:**
  - A) Three rows give three scenarios, each with its own cart.
  - B) Multiple `Examples` blocks still produce separate scenarios per row.
  - C) A Background is for shared context, not for the action under test.
</details>

---

### 221. When does a feature-level `Background` run?
- [ ] A) Once, before the first scenario of the feature
- [ ] B) Before every scenario and every outline row, after the `@Before` hooks
- [ ] C) Before the `@Before` hooks of each scenario
- [ ] D) Only before scenarios that start with a `When`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Before every scenario and every outline row, after the `@Before` hooks

**Explanation:** The per-scenario order is `@Before` hooks, Background steps, scenario steps, `@After` hooks, which keeps each scenario independent. *(background-and-rule.md)*
- **Why others are wrong:**
  - A) It is not once per feature; it re-runs for each scenario.
  - C) The browser must already exist, so hooks run first.
  - D) The first keyword of the scenario is irrelevant.
</details>

---

### 222. Which step is the best candidate for the `Background` of a cart feature in which 8 scenarios exist and all of them need a logged-in user?
- [ ] A) `Given the browser is open`
- [ ] B) `When the shopper adds a product to the cart`
- [ ] C) `Given the shopper is logged in`
- [ ] D) `Given the shopper has two products in the cart` (needed by 3 of the 8 scenarios)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Given the shopper is logged in`

**Explanation:** A Background should hold short, business-relevant Given steps needed by every scenario. *(background-and-rule.md)*
- **Why others are wrong:**
  - A) Technical setup belongs in a hook.
  - B) A `When` does not belong in a Background; it is not context.
  - D) Needed by only some scenarios, so keep it in those scenarios or in a `Rule`.
</details>

---

### 223. What effect does adding `Rule:` headings to a feature have on test execution?
- [ ] A) None; Cucumber runs the examples as ordinary scenarios and `Rule` only organizes and documents
- [ ] B) Each rule is run in a separate browser session shared by its examples
- [ ] C) Scenarios outside any rule are skipped
- [ ] D) The feature-level Background no longer runs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) None; Cucumber runs the examples as ordinary scenarios and `Rule` only organizes and documents

**Explanation:** `Rule` is for organization and reports; to select by rule you would use tags. *(background-and-rule.md)*
- **Why others are wrong:**
  - B) Scenarios stay independent; nothing is shared per rule.
  - C) Nothing is skipped because of `Rule`.
  - D) The feature Background still applies to rule scenarios.
</details>

---

### 224. A step in the middle of a scenario throws an `AssertionError`. Which hook is still guaranteed to run afterwards?
- [ ] A) `@BeforeStep`
- [ ] B) `@Before`
- [ ] C) `@BeforeAll`
- [ ] D) `@After`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `@After`

**Explanation:** `@After` runs after each scenario whether it passed or failed, which is why browser cleanup belongs there rather than in the last `Then` step. *(hooks.md)*
- **Why others are wrong:**
  - A) `@BeforeStep` runs before steps, not after the scenario ends.
  - B) `@Before` runs before the scenario starts.
  - C) `@BeforeAll` runs once before any scenario.
</details>

---

### 225. Why should the failure-screenshot `@After` hook use a higher `order` than the hook that quits the browser?
- [ ] A) Higher numbers run later, so the screenshot is taken after everything else
- [ ] B) `@After` hooks run in descending order, so the higher number runs first while the browser still exists
- [ ] C) Cucumber requires every hook to have a unique number
- [ ] D) The screenshot must be taken before the scenario is marked failed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `@After` hooks run in descending order, so the higher number runs first while the browser still exists

**Explanation:** `@After` order is the reverse of `@Before`: order 10 runs before order 0, so the screenshot (10) precedes the quit (0). *(hooks.md)*
- **Why others are wrong:**
  - A) That is the ascending rule for `@Before`, not `@After`.
  - C) Uniqueness is not required.
  - D) The screenshot hook checks `isFailed()`, so the scenario must already be failed.
</details>

---

### 226. How do the `Hooks` class and the step classes end up using the same browser during one scenario?
- [ ] A) Both read a `static WebDriver` field
- [ ] B) The hooks call the step methods directly
- [ ] C) PicoContainer injects the same per-scenario `TestContext` into each through its constructor
- [ ] D) JUnit shares the driver between all classes of a package

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) PicoContainer injects the same per-scenario `TestContext` into each through its constructor

**Explanation:** One object graph is built per scenario, so hooks and steps share one `TestContext` (and driver), and everything is discarded afterwards. *(hooks.md)*
- **Why others are wrong:**
  - A) Static drivers leak state across scenarios and break parallel runs.
  - B) Hooks and steps are independent; Cucumber calls them.
  - D) JUnit plays no part in sharing the driver.
</details>

---

### 227. `cucumber.properties` contains `cucumber.filter.tags=not @wip and not @ignore`. A CI job runs `mvn test -Dcucumber.filter.tags="@wip"`. Which scenarios run (no hard-coded tags in a runner)?
- [ ] A) Only the `@wip` scenarios, because the command line overrides the properties file
- [ ] B) Everything except `@wip` and `@ignore`, because the file is the repository default
- [ ] C) No scenarios, because the two expressions are combined with `and`
- [ ] D) The build fails because two sources define the same key

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Only the `@wip` scenarios, because the command line overrides the properties file

**Explanation:** The command-line value takes precedence over the properties file, letting a build server choose a subset while the file protects everyone else by default. *(tags.md)*
- **Why others are wrong:**
  - B) The file value is only the default.
  - C) The values are not merged.
  - D) Overriding is normal and causes no error.
</details>

---

### 228. How is the tag expression `@smoke or @login and not @wip` evaluated?
- [ ] A) `(@smoke or @login) and not @wip`
- [ ] B) `@smoke or @login`, with `not @wip` ignored
- [ ] C) `not (@smoke or @login and @wip)`
- [ ] D) `@smoke or (@login and not @wip)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `@smoke or (@login and not @wip)`

**Explanation:** Precedence is `not` > `and` > `or`, so a `@smoke @wip` scenario is still selected; add parentheses to say what you mean. *(tags.md)*
- **Why others are wrong:**
  - A) That would require parentheses, which are not written.
  - B) `not` is part of the expression and is evaluated.
  - C) `not` binds only to the single tag after it.
</details>

---

### 229. Why does the lesson prefer tagging an unfinished scenario `@wip` (and filtering it out) over deleting it or commenting it out?
- [ ] A) Cucumber refuses to parse commented-out scenarios
- [ ] B) A tagged scenario stays in the repository and living documentation and can be counted, while a commented-out one is invisible to reports
- [ ] C) Tagged scenarios still run but their failures are ignored
- [ ] D) Deleting a scenario causes a parse error in the remaining file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A tagged scenario stays in the repository and living documentation and can be counted, while a commented-out one is invisible to reports

**Explanation:** Excluding by tag keeps the knowledge that the behavior was specified, and "12 scenarios are ignored" is a number a team can act on. *(tags.md)*
- **Why others are wrong:**
  - A) Comments parse fine; the problem is lost visibility.
  - C) Filtered scenarios are excluded before the run, not run and ignored.
  - D) Deleting causes no parse error; it loses information.
</details>

---

**Part B: True/False**

### 230. True or False: A feature-level `Background` runs once per feature, before the first scenario only.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The Background runs before every scenario and every outline row, so a login Background logs in again each time. This costs time but keeps scenarios independent. *(background-and-rule.md)*
- **Why others are wrong:**
  - A) The misconception is treating it like a one-time `@BeforeAll`; a shared single login would pass a dirty cart to the next scenario.
</details>

---

### 231. True or False: If a `Background` step fails, the scenario's remaining steps are skipped but the `@After` hooks still run.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The failure skips the `When`/`Then` steps, while `@After` still takes the screenshot and quits the browser; every scenario in the feature then fails at the same step, pointing to the environment or login step. *(background-and-rule.md)*
- **Why others are wrong:**
  - B) The misconception is that a failure stops everything; hooks run regardless.
</details>

---

### 232. True or False: In an ordinary `Scenario` (not a `Scenario Outline`), the text `<username>` is just literal text and is not substituted.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Placeholders are only substituted in Scenario Outlines, which is also why `Examples` with a plain `Scenario` is a parse error. *(scenario-outline-and-examples.md)*
- **Why others are wrong:**
  - B) The misconception is that angle brackets are substituted anywhere in a feature file.
</details>

---

### 233. True or False: A `@BeforeAll` method may be an ordinary instance method that receives the injected `TestContext` through the constructor.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `@BeforeAll` and `@AfterAll` must be `static` and cannot take a `Scenario`; they run once before any scenario exists, so no per-scenario injected context is available. *(hooks.md)*
- **Why others are wrong:**
  - A) The misconception is treating run-level hooks like `@Before`; a non-static method is rejected when Cucumber loads the glue.
</details>

---

**Part C: Code Prediction**

### 234. How many times does the Background step run for this feature?
```gherkin
Feature: Cart
  Background:
    Given the shopper is logged in

  Scenario: One
    When the shopper adds "Sauce Labs Backpack" to the cart
    Then the cart count shows 1

  Scenario: Two
    When the shopper adds "Sauce Labs Onesie" to the cart
    Then the cart count shows 1

  Scenario Outline: Adding <product>
    When the shopper adds "<product>" to the cart
    Then the cart count shows 1

    Examples:
      | product               |
      | Sauce Labs Bike Light |
      | Sauce Labs Onesie     |
      | Sauce Labs Backpack   |
```
- [ ] A) `1`
- [ ] B) `3`
- [ ] C) `2`
- [ ] D) `5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `5`

**Explanation:** The Background runs before each plain scenario (2) and each outline row (3), giving 5 runs. *(background-and-rule.md)*
- **Why others are wrong:**
  - A) It is not once per feature.
  - B) That counts only the outline rows.
  - C) That counts only the plain scenarios.
</details>

---

### 235. What is the order of steps executed for the example below (after `@Before`)?
```gherkin
Feature: Checkout
  Background:
    Given the shopper is logged in

  Rule: Removing a product empties a one-item cart
    Background:
      Given the shopper has "Sauce Labs Backpack" in the cart

    Example: Remove the only product
      When the shopper removes "Sauce Labs Backpack" from the cart
      Then the cart is empty
```
- [ ] A) has Backpack in the cart, logged in, removes, cart is empty
- [ ] B) logged in, removes, has Backpack in the cart, cart is empty
- [ ] C) logged in, has Backpack in the cart, removes, cart is empty
- [ ] D) has Backpack in the cart, removes, cart is empty (the feature Background is replaced)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) logged in, has Backpack in the cart, removes, cart is empty

**Explanation:** The feature Background runs first, then the Rule Background, then the scenario steps; the Rule Background is in addition to, not instead of, the feature one. *(background-and-rule.md)*
- **Why others are wrong:**
  - A) The Rule Background does not run before the feature Background.
  - B) Background steps always precede the scenario's own steps.
  - D) The feature Background is not replaced.
</details>

---

### 236. What does this program print (letters printed with `System.out.print`) for one passing scenario?
```java
@Before(order = 5)  public void a() { System.out.print("a"); }
@Before(order = 1)  public void b() { System.out.print("b"); }
@After(order = 5)   public void c() { System.out.print("c"); }
@After(order = 1)   public void d() { System.out.print("d"); }
```
- [ ] A) `abcd`
- [ ] B) `badc`
- [ ] C) `bacd`
- [ ] D) `abdc`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `bacd`

**Explanation:** `@Before` runs in ascending order (1 then 5: `b`, `a`); `@After` runs in descending order (5 then 1: `c`, `d`). *(hooks.md)*
- **Why others are wrong:**
  - A) That is declaration order, ignoring `order`.
  - B) The after-hooks are not ascending.
  - D) The before-hooks are not run in declaration order.
</details>

---

### 237. Four scenarios have these effective tags. How many are selected by `@login and not @smoke`?
```text
1: @ui @login @smoke @positive
2: @ui @login @regression @negative
3: @ui @login @regression @negative
4: @ui @login @wip
```
- [ ] A) `1`
- [ ] B) `2`
- [ ] C) `4`
- [ ] D) `3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `3`

**Explanation:** All four have `@login`; only scenario 1 has `@smoke`, so scenarios 2, 3 and 4 are selected (the `@wip` one too, since the expression does not exclude it). *(tags.md)*
- **Why others are wrong:**
  - A) That is the count for `@smoke`, not `not @smoke`.
  - B) This forgets that the `@wip` scenario has `@login` and no `@smoke`.
  - C) Scenario 1 carries `@smoke` and is excluded.
</details>

---

### 238. Given these hooks, which run, and in what order, for a scenario whose effective tags are `@ui @slow`?
```java
@Before(value = "@ui", order = 0)    public void startBrowser() { }
@Before(value = "@slow", order = 5)  public void warnSlow() { }
@After(value = "@createsUser")       public void deleteUser() { }
```
- [ ] A) `startBrowser`, then `warnSlow`
- [ ] B) `warnSlow`, then `startBrowser`
- [ ] C) `startBrowser` only
- [ ] D) None, because tagged hooks need `@Before` without arguments

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `startBrowser`, then `warnSlow`

**Explanation:** The tag decides whether a hook runs and `order` decides when: both `@Before` hooks match and 0 runs before 5; `deleteUser` does not match. *(tags.md)*
- **Why others are wrong:**
  - B) Ascending order puts 0 before 5.
  - C) The scenario also has `@slow`, so `warnSlow` runs.
  - D) Tagged hooks are supported and run when the expression matches.
</details>

---

### 239. An outline uses `<user>` in its title and step, but the `Examples` header is `username`. What does the run most likely show?
```gherkin
Scenario Outline: Login with <user> is rejected
  When the customer logs in with username "<user>" and password "<password>"
  Examples:
    | username      | password |
    | standard_user | wrong    |
```
- [ ] A) A parse error saying the placeholder is unknown
- [ ] B) The row runs using the `username` value anyway
- [ ] C) An undefined scenario whose title still shows `<user>` literally
- [ ] D) The step runs with an empty string

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) An undefined scenario whose title still shows `<user>` literally

**Explanation:** Cucumber does not reject this at parse time; `<user>` stays in the text, so the step does not match, and angle brackets in the output signal an unreplaced placeholder. *(scenario-outline-and-examples.md)*
- **Why others are wrong:**
  - A) No parse-time validation of placeholder names happens.
  - B) Names must match exactly (case-sensitive); nothing is guessed.
  - D) Empty strings come from empty cells, not unmatched names.
</details>

---

### 240. The hooks below run for a failing scenario. The `TestContext` has a lazy `driver()` and no `hasDriver()` guard is used. What happens?
```java
@After(order = 0)
public void screenshotOnFailure(Scenario scenario) {
    if (scenario.isFailed()) {
        byte[] png = ((TakesScreenshot) context.driver()).getScreenshotAs(OutputType.BYTES);
        scenario.attach(png, "image/png", "Failure");
    }
}

@After(order = 10)
public void quitBrowser() { context.quitDriver(); }
```
- [ ] A) A `NoSuchSessionException` is always thrown
- [ ] B) A correct screenshot of the failing page is attached
- [ ] C) The screenshot hook is silently skipped
- [ ] D) A brand-new browser is started, a blank page is photographed, and that browser is left open

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A brand-new browser is started, a blank page is photographed, and that browser is left open

**Explanation:** The quit hook has the higher order so it runs first and clears the field; the lazy `driver()` then silently creates a new browser. *(hooks.md)*
- **Why others are wrong:**
  - A) That exception appears only if the code held a direct reference to the quit driver.
  - B) The original browser is already closed.
  - C) The hook runs; it just uses a new browser.
</details>

---

**Part D: Fill-in-the-Blank**

### 241. In a `Scenario Outline`, an empty cell under `username` makes `"<username>"` become `""`, which `{string}` matches as an empty _____.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `string` (also accepted: `String`, `string value`)

**Explanation:** An empty cell gives an empty string, a convenient way to test empty input. *(scenario-outline-and-examples.md)*
</details>

---

### 242. In a feature with a feature-level Background and a Rule that has its own Background, the steps run in this order: feature Background, then the _____ Background, then the scenario steps.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Rule` (also accepted: `rule-level`)

**Explanation:** The Rule Background applies in addition to the feature Background, after it. *(background-and-rule.md)*
</details>

---

### 243. Because `@BeforeAll` and `@AfterAll` run before any scenario exists, their methods must be declared _____.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `static`

**Explanation:** They cannot use a per-scenario injected context, and a non-static method is rejected at load. *(hooks.md)*
</details>

---

### 244. The configuration key that holds a tag expression to select scenarios, usable in `cucumber.properties` or with `-D` on the Maven command line, is `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `cucumber.filter.tags` (also accepted: `FILTER_TAGS_PROPERTY_NAME` as the runner constant)

**Explanation:** The command-line value overrides the properties file. *(tags.md)*
</details>

---

#### Set 2 of 2

**Part A: Multiple Choice**

### 245. When `mvn test` runs a Cucumber suite, which party decides which classes are handed to JUnit and starts the Java process for the tests?
- [ ] A) The Cucumber engine
- [ ] B) Maven Surefire (or the IDE)
- [ ] C) The glue code
- [ ] D) The JUnit Platform launcher

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Maven Surefire (or the IDE)

**Explanation:** Surefire (or the IDE) decides which classes to hand to JUnit and starts the Java process; the platform then launches engines. *(junit-integration.md)*
- **Why others are wrong:**
  - A) The Cucumber engine is a plug-in that discovers and runs `.feature` files; it does not pick the classes.
  - C) Glue code is the steps, hooks and page objects, the "film itself".
  - D) The JUnit Platform provides the launcher and common vocabulary, but Surefire starts it.
</details>

---

### 246. What is the effect of `@IncludeEngines("cucumber")` on a `@Suite` class?
- [ ] A) It tells Cucumber where the step definitions are
- [ ] B) It selects the folder that contains the feature files
- [ ] C) It chooses which report formats are produced
- [ ] D) It limits the suite to the Cucumber test engine so other engines do not take part

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It limits the suite to the Cucumber test engine so other engines do not take part

**Explanation:** Without it the suite may also try other engines on the classpath, such as Jupiter. *(junit-integration.md)*
- **Why others are wrong:**
  - A) Glue packages are set with `GLUE_PROPERTY_NAME` via `@ConfigurationParameter`.
  - B) The feature folder is selected by `@SelectClasspathResource`.
  - C) Report formats come from the plug-in property.
</details>

---

### 247. A project has 3 feature files containing 7 scenarios in total (no outlines). After `mvn clean test`, what does `Tests run:` show?
- [ ] A) 1, because the single runner class is one test
- [ ] B) 3, because each feature file is one test
- [ ] C) 7, because each scenario is reported as one test
- [ ] D) 10, because features and scenarios are both counted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 7, because each scenario is reported as one test

**Explanation:** The "Tests run" number counts scenarios, not feature files. *(junit-integration.md)*
- **Why others are wrong:**
  - B) Feature files become containers, not counted tests.
  - A) The runner class is only the entry point; its scenarios are the tests.
  - D) Features are not added to the count.
</details>

---

### 248. Why does the lesson say parallel scenario execution is a normal, supported feature with JUnit 5 but awkward with JUnit 4?
- [ ] A) JUnit 5 needs Surefire forking tricks while JUnit 4 does not
- [ ] B) JUnit 4 runs only on Java 5 and cannot start threads
- [ ] C) It is built into the Cucumber engine via `cucumber.execution.parallel.*`
- [ ] D) JUnit 5 starts one browser for all scenarios by default

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is built into the Cucumber engine via `cucumber.execution.parallel.*`

**Explanation:** For JUnit 4, parallelism needs Surefire forking tricks or third-party runners, and Cucumber's JUnit 4 module has no built-in scenario-level parallelism. *(junit-integration.md)*
- **Why others are wrong:**
  - A) That is reversed: the forking tricks belong to JUnit 4.
  - B) The lesson only says JUnit 4 supports Java 5+, not that it lacks threads.
  - D) Parallel safety requires one WebDriver per scenario, not a shared browser.
</details>

---

### 249. A trainee names the runner `CucumberRunner`. `mvn test` finishes with `Tests run: 0`. What is the most likely cause?
- [ ] A) The class name does not match Surefire's default patterns (`*Test`, `Test*`, `*Tests`, `*TestCase`)
- [ ] B) Cucumber does not allow the word "Runner" in class names
- [ ] C) The `@Suite` annotation must be removed when the class is renamed
- [ ] D) Maven only runs classes that are inside `src/main/java`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The class name does not match Surefire's default patterns (`*Test`, `Test*`, `*Tests`, `*TestCase`)

**Explanation:** Surefire would silently not find the class, producing `Tests run: 0`; rename it or configure `includes`. *(junit-integration.md)*
- **Why others are wrong:**
  - B) Cucumber has no restriction on class names; Surefire's pattern is the issue.
  - C) `@Suite` is required for the JUnit 5 runner.
  - D) Tests and runners belong in `src/test/java`.
</details>

---

### 250. Your page objects in `src/main/java` import `org.openqa.selenium`, while Cucumber and JUnit are used only by tests. Which scopes fit the framework?
- [ ] A) `compile` (default) for Selenium, `test` for Cucumber and JUnit
- [ ] B) `test` for Selenium, `compile` for Cucumber and JUnit
- [ ] C) `provided` for Selenium, `runtime` for Cucumber
- [ ] D) `test` for all of them, because the project is a test project

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `compile` (default) for Selenium, `test` for Cucumber and JUnit

**Explanation:** The decision rule: if code in `src/main/java` imports it, use `compile`; if only tests use it, use `test`. *(maven-integration.md)*
- **Why others are wrong:**
  - B) Reversed: main code could not see a test-scope Selenium.
  - C) `provided` and `runtime` are for container-supplied or run-only libraries, not these.
  - D) A test-scope Selenium breaks compilation of `src/main`.
</details>

---

### 251. `library-A` needs `guava 31` and `library-B` needs `guava 33`, both at the same depth in the tree. Neither is declared directly. Which Guava version does Maven use?
- [ ] A) The highest version number, `guava 33`
- [ ] B) Both, loaded side by side
- [ ] C) None; the build fails immediately with a conflict error
- [ ] D) The one found first (declared first in the POM), here `guava 31`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The one found first (declared first in the POM), here `guava 31`

**Explanation:** Maven's rule is "nearest definition wins"; when equally near, the first one declared wins. B may then fail at runtime with `NoSuchMethodError`. *(maven-integration.md)*
- **Why others are wrong:**
  - A) Maven does not choose by highest version.
  - B) Only one version can be on the classpath.
  - C) The build compiles fine; the conflict appears at runtime.
</details>

---

### 252. The POM has `<cucumber.filter.tags>not @wip and not @ignore</cucumber.filter.tags>`, and a `smoke` profile sets it to `@smoke and not @wip`. What is the effective value for `mvn test -Psmoke -Dcucumber.filter.tags="@cart"`?
- [ ] A) `@smoke and not @wip`
- [ ] B) `@cart`
- [ ] C) `not @wip and not @ignore`
- [ ] D) `@smoke and @cart`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `@cart`

**Explanation:** Precedence is command-line `-D`, then profile properties, then top-level `<properties>`. *(maven-integration.md)*
- **Why others are wrong:**
  - A) The profile value is overridden by the command line.
  - C) The top-level value is the lowest precedence.
  - D) Values are replaced, not combined.
</details>

---

### 253. Which statement correctly contrasts Surefire and Failsafe?
- [ ] A) Failsafe is required for any Cucumber runner to work
- [ ] B) Surefire runs `*IT` classes; Failsafe runs `*Test` classes
- [ ] C) Both run in the `test` phase, but Failsafe is quieter
- [ ] D) Failsafe runs `*IT` classes in `integration-test`/`verify` and fails the build after teardown; Surefire runs `*Test` classes in `test`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Failsafe runs `*IT` classes in `integration-test`/`verify` and fails the build after teardown; Surefire runs `*Test` classes in `test`

**Explanation:** Surefire with `RunCucumberTest` is sufficient for the course; Failsafe suits setups that start and stop an environment. *(maven-integration.md)*
- **Why others are wrong:**
  - B) The name patterns are swapped.
  - C) Failsafe uses different phases.
  - A) Surefire is enough for this course.
</details>

---

### 254. A tester runs `mvn test -Dcucumber.features=@target/rerun.txt` and the summary shows the same number of scenarios as the full suite. What is the likely explanation?
- [ ] A) The `rerun.txt` file was empty
- [ ] B) The `@` prefix means the value is a tag, so every scenario matched
- [ ] C) Maven ignores all `-D` flags that start with `cucumber.`
- [ ] D) The suite's `@SelectClasspathResource` selection took precedence, so the whole `features` folder ran again

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The suite's `@SelectClasspathResource` selection took precedence, so the whole `features` folder ran again

**Explanation:** This is the documented limitation; a dedicated rerun runner may be needed, and the scenario count is how you verify. *(junit-integration.md)*
- **Why others are wrong:**
  - A) An empty file is not what the lesson links to a full-suite count.
  - B) The leading `@` means "read locations from the file", not a tag.
  - C) Other `-D` properties work; this one conflicts with the suite selector.
</details>

---

### 255. Why must the screenshot `@After` hook have a higher `order` than the hook that quits the browser?
- [ ] A) Higher `order` values run last, so the screenshot is taken after reporting
- [ ] B) For `@After` hooks a higher `order` runs first, and a closed browser cannot be photographed
- [ ] C) Cucumber refuses to run two `@After` hooks with the same order
- [ ] D) The quit hook must run before `scenario.isFailed()` becomes true

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) For `@After` hooks a higher `order` runs first, and a closed browser cannot be photographed

**Explanation:** Screenshot at `order = 10` runs before quit at `order = 1`. *(cucumber-reporting.md)*
- **Why others are wrong:**
  - A) It is the opposite for `@After`: higher runs first.
  - C) The lesson says nothing of the kind; ordering is about when each hook runs.
  - D) `isFailed()` depends on the steps, not on the quit hook.
</details>

---

### 256. A trainee writes `public void confirmationDisplayed(Scenario scenario)` in a step definition to attach a screenshot. What is the problem and the lesson's workaround?
- [ ] A) Steps may take `Scenario`, but only as the first parameter
- [ ] B) `Scenario` can only be used with `scenario.log`, never `attach`
- [ ] C) Cucumber passes `Scenario` only to hooks; store it in `TestContext` from a `@Before` hook and use it in steps
- [ ] D) Steps must use a static `Scenario` field shared by all scenarios

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Cucumber passes `Scenario` only to hooks; store it in `TestContext` from a `@Before` hook and use it in steps

**Explanation:** PicoContainer creates one `TestContext` per scenario, so each scenario attaches to its own report entry, even in parallel. *(cucumber-reporting.md)*
- **Why others are wrong:**
  - A) A step method cannot receive `Scenario` at all.
  - B) `attach` works fine once you hold the `Scenario`.
  - D) A static field would be shared between parallel scenarios.
</details>

---

**Part B: True/False**

### 257. In Cucumber 7, a scenario containing an undefined step is shown as a harmless warning and the run still passes.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Undefined and pending steps are treated as errors by default, so the run fails instead of passing silently. *(cucumber-reporting.md)*
- **Why others are wrong:**
  - A) The misconception is that undefined steps are tolerated; if they were, a build could be green while verifying nothing.
</details>

---

### 258. During a migration, it is fine to keep both `cucumber-junit` (JUnit 4) and `cucumber-junit-platform-engine` in the same module because they will share the work.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Both would try to run the same features, giving duplicates or conflicts; choose one per module. *(junit-integration.md)*
- **Why others are wrong:**
  - A) Vintage can run old JUnit 4 tests alongside JUnit 5, but that does not extend to mixing the two Cucumber modules.
</details>

---

### 259. In JUnit 5, the assertion message is the last argument: `assertEquals(expected, actual, message)`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** In JUnit 4 the message came first; in JUnit 5 it is last, and a silent swap can produce confusing failure output. *(junit-integration.md)*
- **Why others are wrong:**
  - B) The misconception is carrying the JUnit 4 order into JUnit 5.
</details>

---

### 260. With Surefire's `testFailureIgnore` set to `true`, a run with a failed scenario can still end with `BUILD SUCCESS`, so another step must fail the pipeline.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Failures are recorded but the build continues; it ends successfully if nothing else is wrong. *(maven-integration.md)*
- **Why others are wrong:**
  - B) The misconception is that failed scenarios always fail the build; that is only the default (`false`).
</details>

---

**Part C: Code Prediction**

### 261. Two runners exist. A scenario is tagged `@smoke` and `@regression`. What happens with plain `mvn test`?

```java
@Suite @IncludeEngines("cucumber") @SelectClasspathResource("features")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "@smoke")
public class RunSmokeTest { }

@Suite @IncludeEngines("cucumber") @SelectClasspathResource("features")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "@regression")
public class RunRegressionTest { }
```
- [ ] A) It runs once, because Cucumber removes duplicates
- [ ] B) It does not run, because two runners conflict
- [ ] C) It runs twice, once per runner
- [ ] D) It runs only under `RunSmokeTest`, because it is listed first alphabetically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It runs twice, once per runner

**Explanation:** Plain `mvn test` runs all matching runner classes; control with `includes`, profiles, or `and not @smoke`. *(junit-integration.md)*
- **Why others are wrong:**
  - A) There is no de-duplication across runners.
  - B) Runners do not conflict; they simply both run.
  - D) Both classes match Surefire's naming pattern.
</details>

---

### 262. A step contains the code below. The cart shows 2 items. What failure message appears?

```java
assertEquals(3, cart.getCount(), "Cart count");
```
- [ ] A) `NullPointerException` at the first line
- [ ] B) `AssertionFailedError: Cart count ==> expected: <2> but was: <3>`
- [ ] C) `AssertionFailedError: Cart count ==> expected: <3> but was: <2>`
- [ ] D) No failure; the step passes with a warning

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `AssertionFailedError: Cart count ==> expected: <3> but was: <2>`

**Explanation:** The first value is the expected one from the Gherkin text; the second is actual from the page. *(junit-integration.md)*
- **Why others are wrong:**
  - B) That would appear only if the arguments were swapped.
  - A) Nothing in the code suggests a null.
  - D) Unequal values fail the step.
</details>

---

### 263. The POM defines default properties `browser=chrome`, `headless=false`. A profile `ci` sets `headless=true`. Surefire forwards both via `systemPropertyVariables`. What does the test JVM see for `mvn test -Pci -Dbrowser=edge`?

```java
System.getProperty("browser", "chrome");
System.getProperty("headless", "false");
```
- [ ] A) `chrome` and `false`
- [ ] B) `edge` and `false`
- [ ] C) `chrome` and `true`
- [ ] D) `edge` and `true`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `edge` and `true`

**Explanation:** `-D` overrides the top-level browser; the active profile replaces the top-level headless. *(maven-integration.md)*
- **Why others are wrong:**
  - A) That ignores both the command line and the profile.
  - B) The profile's headless value would still apply.
  - C) The `-Dbrowser` override would still apply.
</details>

---

### 264. Four threads run scenarios with this driver manager. What is the likely symptom?

```java
public class DriverManager {
    private static WebDriver driver;
    public static WebDriver getDriver() {
        if (driver == null) { driver = new ChromeDriver(); }
        return driver;
    }
}
```
- [ ] A) Each scenario gets its own private browser automatically
- [ ] B) Random failures such as `NoSuchElementException`, because scenarios share one browser
- [ ] C) A compile error because `driver` is static
- [ ] D) Every scenario fails with `Tests run: 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Random failures such as `NoSuchElementException`, because scenarios share one browser

**Explanation:** One static driver is shared by the whole JVM, so threads overwrite each other, and the null check is not thread-safe either. *(junit-integration.md)*
- **Why others are wrong:**
  - A) The static field means one shared driver.
  - C) It compiles; the problem is at runtime.
  - D) `Tests run: 0` is a discovery problem.
</details>

---

### 265. `selenium-java` is given `<scope>test</scope>`, while a page object in `src/main/java` imports Selenium. What happens on `mvn compile`?

```xml
<dependency>
  <groupId>org.seleniumhq.selenium</groupId>
  <artifactId>selenium-java</artifactId>
  <scope>test</scope>
</dependency>
```
- [ ] A) It compiles and Selenium is added at runtime
- [ ] B) Compilation of main code fails with `package org.openqa.selenium does not exist`
- [ ] C) Maven silently promotes the scope to `compile`
- [ ] D) The compile passes but tests fail with `Tests run: 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Compilation of main code fails with `package org.openqa.selenium does not exist`

**Explanation:** The compiler for `src/main` cannot see test-scope libraries. *(maven-integration.md)*
- **Why others are wrong:**
  - A) Test scope is not available to main code at all.
  - C) Maven does not change scopes for you.
  - D) The failure happens at compile time, before tests.
</details>

---

### 266. What does the `duration` value in this JSON step result mean?

```json
"result": { "status": "passed", "duration": 523000000 }
```
- [ ] A) 523 million milliseconds
- [ ] B) 523 seconds
- [ ] C) 523 microseconds
- [ ] D) About half a second, because the unit is nanoseconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) About half a second, because the unit is nanoseconds

**Explanation:** The lesson states durations are in nanoseconds, so 523000000 is about half a second. *(cucumber-reporting.md)*
- **Why others are wrong:**
  - A) Milliseconds would be absurdly long.
  - B) That would require seconds as the unit.
  - C) Microseconds would give about 523 seconds.
</details>

---

### 267. Surefire is configured to include only `**/RunCucumberTest.java`. Which runner executes for `mvn test -Dtest=RunSmokeTest`?

```xml
<includes>
  <include>**/RunCucumberTest.java</include>
</includes>
```
- [ ] A) Only `RunSmokeTest`, because `-Dtest` overrides `includes`
- [ ] B) Only `RunCucumberTest`, because `includes` always wins
- [ ] C) Both runners
- [ ] D) Neither, because the settings conflict

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Only `RunSmokeTest`, because `-Dtest` overrides `includes`

**Explanation:** `-Dtest=...` on the command line overrides `includes` and runs that class. *(maven-integration.md)*
- **Why others are wrong:**
  - B) The command-line value wins over `includes`.
  - C) Only the named class runs.
  - D) There is no conflict error; `-Dtest` takes precedence.
</details>

---

**Part D: Fill-in-the-Blank**

### 268. In the JUnit 4 style runner, `@RunWith(_____.class)` hands the class to Cucumber, and in JUnit 5 it is replaced by `@Suite`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Cucumber` (also accepted: `Cucumber.class`, `io.cucumber.junit.Cucumber`)

**Explanation:** `@RunWith(Cucumber.class)` tells JUnit 4 to hand the class to the Cucumber runner. *(junit-integration.md)*
</details>

---

### 269. A library that one of your dependencies needs, and that Maven downloads automatically, is called a _____ dependency.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `transitive` (also accepted: `Transitive`)

**Explanation:** Maven reads the dependency's own POM and downloads what it needs; `mvn dependency:tree` shows them. *(maven-integration.md)*
</details>

---

### 270. To hide the "View your Cucumber Report at..." banner and avoid publishing the report to a third-party service, set `cucumber.publish._____=true`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `quiet` (also accepted: `cucumber.publish.quiet`)

**Explanation:** `cucumber.publish.quiet=true` silences the message; the built-in HTML file stays local. *(cucumber-reporting.md)*
</details>

---

### 271. The `maven-cucumber-reporting` plug-in is bound to the _____ phase, which comes after `test`, so the JSON already exists when it runs.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `verify` (also accepted: `Verify`)

**Explanation:** The execution uses `<phase>verify</phase>`, run with `mvn clean verify`; a failing test stops the build before it unless failures are ignored. *(cucumber-reporting.md)*
</details>

---

