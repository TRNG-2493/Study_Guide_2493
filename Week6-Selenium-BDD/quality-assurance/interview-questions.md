# Interview Questions: Week 6 - Selenium, BDD

Self-quiz bank for technical interviews. Say your answer out loud first, check that you used the keywords, then click **Click to Reveal Answer**. Each day has 18 questions (13 beginner, 4 intermediate, 1 advanced) based strictly on that day's written lessons.

---

# Day 1 - Monday: Selenium WebDriver

## Beginner (Foundational)

### Q1: What is Selenium, and where does Selenium WebDriver fit in the Selenium suite?
**Keywords:** suite, WebDriver, IDE, Grid, browsers
**Hint:** Think of three tools under one name; which one do people mean in a job interview?
<details>
<summary>Click to Reveal Answer</summary>

Selenium is not one tool but a suite for automating web browsers. Selenium WebDriver is a library (API) and protocol for controlling browsers programmatically, and it is the core of modern test automation. Selenium IDE is a browser extension that records and replays actions, good for quick prototypes. Selenium Grid runs tests on many machines and browsers in parallel. When people say "Selenium" at work, they almost always mean WebDriver. Selenium automates web applications in browsers; it does not decide pass/fail, so you add assertions and a runner around it.
</details>

---

### Q2: Walk me through the Selenium architecture. What happens between `driver.get(...)` in Java and the browser opening the page?
**Keywords:** client library, W3C WebDriver protocol, browser driver, HTTP, browser
**Hint:** Four cooperating parts, and the answer travels back along the same path.
<details>
<summary>Click to Reveal Answer</summary>

The architecture has four parts: the Selenium client library (language bindings), the W3C WebDriver protocol, the browser driver, and the browser itself. The client library does not open the browser; it builds a JSON HTTP request such as `POST /session/{id}/url` and sends it to the browser driver, which is a small local HTTP server (chromedriver, geckodriver, msedgedriver). The driver converts it into browser-specific commands and the real browser navigates. The result travels back as an HTTP response and either returns normally or becomes a Java exception. The Java thread blocks until the reply arrives.
</details>

---

### Q3: Why do we write `WebDriver driver = new ChromeDriver();` instead of `ChromeDriver driver = new ChromeDriver();`?
**Keywords:** interface, implements, programming to an interface, one line, WebDriver
<details>
<summary>Click to Reveal Answer</summary>

`WebDriver` is an interface listing what a driver can do, and `ChromeDriver`, `FirefoxDriver` and `EdgeDriver` are classes that implement it. If the variable is typed as the interface, everything after that line only uses `WebDriver` methods, so switching browsers means changing one line (`new FirefoxDriver()`). Helper methods can also accept a `WebDriver` parameter and work with any browser. You would only hold the concrete `ChromeDriver` type when you need something Chrome-specific.
</details>

---

### Q4: What is a browser driver, why must its version match the browser, and how does Selenium Manager help?
**Keywords:** browser driver, version, major version, Selenium Manager, Selenium 4.6
<details>
<summary>Click to Reveal Answer</summary>

A browser driver is an executable (such as chromedriver) that implements the WebDriver protocol for one specific browser; your code talks to the driver and the driver talks to the browser. It is built against specific browser internals, and browsers change often, so the driver's major version must match the browser's major version. Selenium Manager, built into Selenium 4.6 and later, detects the installed browser, downloads the matching driver into a cache folder the first time, and reuses it afterwards, so `new ChromeDriver()` is usually all you need.
</details>

---

### Q5: What is the difference between `driver.close()` and `driver.quit()`, and which should end a test?
**Keywords:** close, quit, current window, session, driver process
<details>
<summary>Click to Reveal Answer</summary>

`close()` closes only the current window or tab; if it was the last window the browser closes but the driver process may keep running. `quit()` closes all windows, ends the session and stops the driver process. Use `quit()` at the end of every test, ideally in a `finally` block so it runs even when an exception occurs. After `quit()` the driver object is dead, and any further call throws an exception such as `NoSuchSessionException`.
</details>

---

### Q6: What is a locator in Selenium, and does creating one contact the browser?
**Keywords:** By, DOM, findElement, description, strategy
<details>
<summary>Click to Reveal Answer</summary>

A locator describes how to find an element in the page's DOM, and in Selenium Java it is an object of type `By`, for example `By.id("login-button")`. It is only a description holding a strategy and a value, so creating it does not contact the browser at all. The search happens only when you pass it to `driver.findElement(...)` or `findElements(...)`, at which point the browser returns a `WebElement` reference or Selenium throws `NoSuchElementException`.
</details>

---

### Q7: Name the eight `By` strategies and tell me which you would try first and why.
**Keywords:** id, name, cssSelector, xpath, data-test
<details>
<summary>Click to Reveal Answer</summary>

The eight are `id`, `name`, `className`, `tagName`, `linkText`, `partialLinkText`, `cssSelector` and `xpath`. The recommended order is a stable, unique `id` or a test attribute such as `data-test` first, then a unique `name`, then a short CSS selector with meaningful attributes, then relative XPath when you need visible text or parent/sibling navigation. Positional locators are the last resort because they break when the layout changes. `id` is fastest and clearest, as long as it is not dynamically generated.
</details>

---

### Q8: When would you need XPath instead of CSS, and why is relative XPath preferred over absolute?
**Keywords:** XPath, visible text, parent, relative, absolute
<details>
<summary>Click to Reveal Answer</summary>

CSS cannot match on an element's visible text and has no practical way to go up to a parent, while XPath can do both, for example `//a[text()='Sauce Labs']` or `/ancestor::form`. Absolute XPath such as `/html/body/div[2]/...` starts at the root and breaks when any wrapper element is added, so it is fragile. Relative XPath starts anywhere with `//` and anchors on attributes or text, so it survives layout changes. DevTools "Copy full XPath" gives absolute paths, which should not be used as-is.
</details>

---

### Q9: What is the difference between `driver.get(url)` and `driver.navigate().to(url)`, and what do `back()`, `forward()` and `refresh()` do?
**Keywords:** get, navigate, history, back, refresh, load event
<details>
<summary>Click to Reveal Answer</summary>

In practice both load a URL and, by default, wait for the page's `load` event. `navigate().to` also has an overload accepting a `java.net.URL` and belongs to the `Navigation` object that holds the history methods. `back()` and `forward()` move through browser history like the browser buttons, and `refresh()` reloads the current page. History works like a list with a bookmark: a new navigation after going back erases the forward pages. After a refresh, previously found elements are stale and must be found again.
</details>

---

### Q10: Why do we set the browser window size explicitly in tests?
**Keywords:** window size, responsive, maximize, layout, headless
<details>
<summary>Click to Reveal Answer</summary>

Many sites are responsive, so on a narrow window the layout changes and elements such as the menu may collapse or hide, which makes locators fail. Servers often start browsers at a small default size like 800 x 600, so a test can pass on your laptop and fail on CI. For desktop runs you use `maximize()` or `setSize(new Dimension(...))`. In headless mode `maximize()` has no effect because there is no screen, so you use `setSize` or the `--window-size` option.
</details>

---

### Q11: Explain the difference between `findElement` and `findElements`, especially when nothing matches.
**Keywords:** findElement, findElements, NoSuchElementException, empty list, first match
<details>
<summary>Click to Reveal Answer</summary>

`findElement` returns a single `WebElement`, the first match in document order, and throws `NoSuchElementException` if nothing matches. If several elements match it silently returns only the first, which hides bugs when a locator is not unique. `findElements` returns a `List<WebElement>` of all matches, and if nothing matches it returns an empty list instead of throwing. That is why `!driver.findElements(locator).isEmpty()` is the clean way to check existence, and why it suits counting and looping.
</details>

---

### Q12: What is the difference between an element being present and being displayed, and why does `getText()` return an empty string on an `<input>`?
**Keywords:** present, displayed, DOM, getText, value
<details>
<summary>Click to Reveal Answer</summary>

Present means the element exists in the DOM; displayed means it exists and is visible to the user, so not `display:none`, not `visibility:hidden` and not zero size. A spare tyre in the boot is present but not displayed. `getText()` returns visible text between the tags, and an `<input>` is a void element with no such text; its label or typed text lives in the `value` attribute. So for `<input>` elements you use `getAttribute("value")`, while `<button>`, `<a>` and `<span>` keep their label as text.
</details>

---

### Q13: What are capabilities and Options classes, and why must you pass the options object into the driver constructor?
**Keywords:** capabilities, ChromeOptions, new ChromeDriver(options), session, headless
**Hint:** Think of a booking form sent when the session is created.
<details>
<summary>Click to Reveal Answer</summary>

Capabilities are the JSON description of the requested browser and its settings sent in the new-session request (`POST /session`). An Options class such as `ChromeOptions`, `FirefoxOptions` or `EdgeOptions` is a Java builder that fills in that JSON for you, using methods like `addArguments("--headless=new")`. The options only take effect if you pass them in at construction time with `new ChromeDriver(options)`. Creating the options and then calling `new ChromeDriver()` with empty parentheses silently ignores everything you configured.
</details>

---

## Intermediate (Application)

### Q14: Your test passes when you run it headed but fails on the CI server in headless mode with `NoSuchElementException` for the cart link. How do you diagnose and fix it?
**Keywords:** headless, window size, --window-size, responsive layout, getSize
**Hint:** Print something about the window before the failing step.
<details>
<summary>Click to Reveal Answer</summary>

Print `driver.manage().window().getSize()` before the failing step. A result like `(800, 600)` suggests a small default window that triggers the responsive layout, hiding the cart link inside a menu. `maximize()` does nothing without a display, so set the size explicitly with `options.addArguments("--headless=new", "--window-size=1920,1080")`. Re-run and confirm, for example with a screenshot, that the full layout is shown. Also debug such failures headed so you can watch.
</details>

---

### Q15: Your suite has 85 tests failing after a redesign that only added a wrapper `<div>`. They all use locators like `/html/body/div[2]/div[1]/form/div[3]/button`. How would you fix them and prevent a repeat?
**Keywords:** absolute XPath, id, data-test, relative XPath, centralized locators
**Hint:** Which attributes would not change when the layout changes?
<details>
<summary>Click to Reveal Answer</summary>

The absolute XPaths depend on the full page structure, so one extra wrapper breaks all of them. Rewrite each locator to use something stable: a unique `id` (`By.id("login-button")`), a `data-test` attribute through CSS, or a unique `name`; use relative XPath only when you need visible text or a parent/sibling relationship. Verify each locator shows "1 of 1" in DevTools before using it. Keep locators named in one place as `static final By` constants so a change is fixed once, and ask developers to add `data-test` attributes if no stable attribute exists.
</details>

---

### Q16: After Chrome auto-updated overnight, all your tests fail with "This version of ChromeDriver only supports Chrome version 124, current browser version is 126". Nobody changed code. How do you find the cause and fix it?
**Keywords:** SessionNotCreatedException, Selenium Manager, webdriver.chrome.driver, precedence, PATH
**Hint:** An explicitly configured driver always beats the automatic mechanism.
<details>
<summary>Click to Reveal Answer</summary>

`SessionNotCreatedException` means the failure happened during session creation, so the driver started but is the wrong version. Selenium Manager would never choose a 124 driver for a 126 browser, so something overrode it, because an explicitly configured driver always takes precedence. Search the project for `webdriver.chrome.driver` and `usingDriverExecutable`, and check the machine's `PATH` for an old chromedriver; also confirm the Selenium version is 4.6 or later. Delete the stale setting so Selenium Manager downloads and uses the matching driver.
</details>

---

### Q17: You want a failing test to leave a screenshot behind as evidence. How would you structure the code, and what mistakes must you avoid?
**Keywords:** TakesScreenshot, catch, rethrow, quit, timestamp
**Hint:** Think about order: the browser must still be alive, and the test must still fail.
<details>
<summary>Click to Reveal Answer</summary>

Wrap the steps in `try/catch/finally`: in the `catch`, cast the driver to `TakesScreenshot`, call `getScreenshotAs(OutputType.FILE)`, copy the temp file to your own folder with a name containing the test name and a timestamp, then `throw e;` so the test still fails. `driver.quit()` goes in `finally`, which runs after the capture. Mistakes to avoid are capturing after `quit()` (throws `NoSuchSessionException`), swallowing the exception (the test would appear to pass), and using a fixed file name that overwrites earlier images.
</details>

---

## Advanced (Deep Dive)

### Q18: Describe in detail what happens under the hood when your code runs `new ChromeDriver()` and then `driver.get(url)` and `driver.quit()`. How does that explain why a "Connection refused" error occurs?
**Keywords:** Selenium Manager, POST /session, session ID, chromedriver process, DELETE /session
**Hint:** Follow the lifecycle step by step, including which HTTP request each call becomes.
<details>
<summary>Click to Reveal Answer</summary>

On `new ChromeDriver()`, Selenium Manager checks the installed Chrome version and ensures a matching chromedriver exists (downloading it to a cache the first time). The client library launches the chromedriver process, waits for its local HTTP server, then sends `POST /session` with the capabilities; chromedriver starts Chrome and returns a session ID, which the `ChromeDriver` object stores. Each later call, such as `get`, becomes an HTTP request carrying that session ID (`POST /session/{id}/url`) and blocks until the reply arrives. `quit()` sends `DELETE /session/{id}`, closing all windows and ending the driver process. Because everything is plain HTTP to a local server, "Connection refused" means nobody is listening: the driver process died, a firewall blocked it, or an earlier `quit()` already ended it.
</details>

---

# Day 2 - Tuesday: Advanced Selenium

## Beginner (Foundational)

### Q19: Why do automated Selenium tests need waits at all? What is the "race condition" people talk about?
**Keywords:** race condition, flaky test, AJAX, wait, condition
**Hint:** Think about your test code and the page being two separate programs.
<details>
<summary>Click to Reveal Answer</summary>

Your test (Java in the JVM) and the web page (JavaScript in the browser) are separate programs that do not share a clock. `click()` returns as soon as the click is performed, so if the page then fetches data in the background (AJAX) and renders results later, Selenium does not know and does not wait. Whether the test passes depends on who "wins" the race between the test and the browser, which is a **race condition**. The same code can pass on a fast day and fail on a slow one, which is exactly what a **flaky test** is. A **wait** tells the test to pause until a **condition** is true, up to a maximum time.
</details>

---

### Q20: Why is `Thread.sleep()` considered a poor solution for waiting in Selenium tests, and what should you use instead?
**Keywords:** Thread.sleep, fixed time, too slow, still flaky, explicit wait
**Hint:** Think about what happens if the page is faster, and what happens if it is slower, than the number you picked.
<details>
<summary>Click to Reveal Answer</summary>

`Thread.sleep` freezes the thread for a **fixed time** and knows nothing about the page. It is **too slow** when the page is ready early (a 5 s sleep wastes 4.7 s if results appear after 0.3 s, and this adds up across hundreds of tests), and it is **still flaky** when the server is slower than the guess. The number is also just a guess that teams tend to multiply "to be safe". Instead use smart waits, such as an **explicit wait** (`WebDriverWait` with `ExpectedConditions`), which poll the page and continue as soon as the condition is true.
</details>

---

### Q21: What is an implicit wait, how does it behave, and what are its limitations?
**Keywords:** implicit wait, findElement, presence, global, NoSuchElementException
<details>
<summary>Click to Reveal Answer</summary>

An implicit wait tells the driver to keep retrying for up to N seconds when `findElement`/`findElements` does not find an element. It is set once per driver session, applies **globally** to every lookup, and returns the element as soon as it appears; if it never appears, `NoSuchElementException` is thrown. Its limitations are that it only waits for **presence** in the DOM (not visibility or clickability, so `getText()` on a present-but-hidden element returns an empty string), it is one value for all lookups, it makes absence checks cost the full timeout, and it cannot wait for conditions like text changes or URL changes.
</details>

---

### Q22: What is an explicit wait and how does `wait.until(...)` actually work?
**Keywords:** WebDriverWait, ExpectedConditions, polling, 500 ms, TimeoutException
**Hint:** Consider what `until` does repeatedly, what it returns, and what happens when time runs out.
<details>
<summary>Click to Reveal Answer</summary>

An explicit wait waits for a specific condition on a specific element, with a timeout you choose for that situation. You create `new WebDriverWait(driver, Duration.ofSeconds(10))` and call `wait.until(ExpectedConditions.something(...))`. `until` evaluates the condition repeatedly (**polling** every **500 ms** by default), ignoring `NoSuchElementException` while it polls. When the condition returns a truthy value it returns that value immediately, often the `WebElement`, so you can chain `.click()` or `.getText()`. If the time runs out first, it throws a `TimeoutException` whose message says what it was waiting for.
</details>

---

### Q23: Selenium has several timeouts: page load timeout, script timeout, implicit wait, and explicit wait. How do you tell them apart?
**Keywords:** page load timeout, script timeout, implicit wait, explicit wait, Duration
<details>
<summary>Click to Reveal Answer</summary>

The **page load timeout** controls how long `get()`/`navigate()` may wait for a page to load (default 300 s, so you usually set something like 30-60 s once in driver setup). The **script timeout** controls how long an asynchronous script (`executeAsyncScript`) may run (default 30 s). The **implicit wait** controls how long `findElement(s)` retries to find an element (default 0, disabled). An **explicit wait** waits for a specific condition and only exists when you create one. In Selenium 4 all of them take a `java.time.Duration`, for example `Duration.ofSeconds(10)`.
</details>

---

### Q24: What does `sendKeys()` do when a field already contains text, and how do you type into a field safely?
**Keywords:** sendKeys, appends, clear, getAttribute("value"), Keys
**Hint:** Think about a pre-filled "edit profile" form.
<details>
<summary>Click to Reveal Answer</summary>

`sendKeys` simulates typing character by character and **appends** to whatever is already in the field, so typing `new@test.com` into a field holding `old@test.com` gives `old@test.comnew@test.com`. The safe pattern is to call `clear()` first and then `sendKeys(text)`. You can verify with `getAttribute("value")`. For stubborn fields where `clear()` does not respond, send a select-all chord and delete, for example `field.sendKeys(Keys.chord(Keys.CONTROL, "a"), Keys.BACK_SPACE)` (use `Keys.COMMAND` on macOS). `sendKeys` can also send special keys from the `Keys` class, such as `Keys.ENTER` or `Keys.TAB`.
</details>

---

### Q25: What is the difference between the "action" methods and the "query" methods on a `WebElement`, and how would you read back what was typed into an input?
**Keywords:** action, query, getText, getAttribute("value"), isSelected
<details>
<summary>Click to Reveal Answer</summary>

**Action** methods (`click()`, `sendKeys()`, `clear()`, `submit()`) change the page; **query** methods (`getText()`, `getAttribute()`, `isDisplayed()`, `isEnabled()`, `isSelected()`, `getCssValue()`) only read state. A good test does an action and then a query to confirm the effect. For an `<input>`, `getText()` returns an empty string because its content is in the `value` attribute, so you use `getAttribute("value")`. For checkboxes and radio buttons you check the state with `isSelected()`.
</details>

---

### Q26: Why do you check `isSelected()` before clicking a checkbox, and what is a gotcha with styled checkboxes?
**Keywords:** toggle, isSelected, current state, desired state, label
<details>
<summary>Click to Reveal Answer</summary>

A checkbox's `click()` **toggles** it, so blindly clicking would untick a box that is already ticked, for example on the second run of a test. The helper compares the **current state** (`isSelected()`) with the **desired state** and clicks only if they differ: `if (checkbox.isSelected() != shouldBeChecked) checkbox.click();`. This makes the result independent of the starting state. With styled checkboxes, the real `<input>` is hidden and throws `ElementNotInteractableException`, so you click the visible **label** (or styled element) and then check `isSelected()` on the real input.
</details>

---

### Q27: How do you upload a file with Selenium, and why shouldn't you just click the file input?
**Keywords:** input type file, sendKeys, absolute path, native dialog, getAbsolutePath
<details>
<summary>Click to Reveal Answer</summary>

For a standard `<input type="file">` you send the **absolute path** of the file straight to the input with `sendKeys`, then click the upload/submit button. Clicking the input opens a **native** operating-system dialog that Selenium cannot control, so the test would hang. A relative path fails because the file will not be found, so build it with `new java.io.File("src/test/resources/sample.txt").getAbsolutePath()`, which also uses the right separator for your OS. The file must exist on the machine where the browser runs, which matters for remote/CI setups.
</details>

---

### Q28: How do you choose an option with Selenium's `Select` class, and what are the trade-offs between the three ways of choosing?
**Keywords:** Select, selectByVisibleText, selectByValue, selectByIndex, NoSuchElementException
**Hint:** Think about what changes when wording changes, when the language changes, or when the list is reordered.
<details>
<summary>Click to Reveal Answer</summary>

You wrap the `<select>` element with `new Select(element)` and then call `selectByVisibleText(...)`, `selectByValue(...)`, or `selectByIndex(...)`. Visible text is the most readable and matches what the user sees, but breaks if the wording or translation changes. The `value` attribute is usually a stable code (`"lohi"`, `"US"`) but can be unreadable. The 0-based index is quick but breaks if the list is reordered, and index 0 is often a placeholder. If nothing matches, Selenium throws `NoSuchElementException` such as `Cannot locate option with text: ...`.
</details>

---

### Q29: How can you tell a native dropdown from a custom one, and what happens if you wrap a custom one with `Select`?
**Keywords:** select tag, option, custom dropdown, UnexpectedTagNameException, DevTools
<details>
<summary>Click to Reveal Answer</summary>

Inspect the element in DevTools. A native dropdown is a `<select>` tag with `<option>` children; a custom dropdown (Bootstrap, Material UI, React-Select, Select2) is built from `<div>`, `<ul>`, `<li>` or `<button>` elements. Wrapping a non-select with `new Select(...)` immediately throws `UnexpectedTagNameException: Element should have been "select" but was "div"`, which itself tells you it is a custom dropdown. You then automate it like a user: click to open it, wait for the options to be visible, and click the option by its text.
</details>

---

### Q30: How do multi-select lists differ from single-select ones in the `Select` class?
**Keywords:** multiple, isMultiple, getAllSelectedOptions, deselectAll, UnsupportedOperationException
<details>
<summary>Click to Reveal Answer</summary>

A multi-select is a `<select multiple>`, where several options can be chosen at once; `isMultiple()` returns `true` for it. In a multi-select each `selectBy...` call **adds** to the selection (like holding Ctrl), you read the choices with `getAllSelectedOptions()`, and you can remove them with `deselectByVisibleText`, `deselectByValue`, `deselectByIndex`, or `deselectAll()`. Calling any `deselect...` method on a single-select throws `UnsupportedOperationException` ("You may only deselect options of a multi-select"), because a normal dropdown always has exactly one chosen option. Guard with `isMultiple()` if the code must handle both.
</details>

---

### Q31: Explain the parts of a native `<select>`: what are an option's visible text, value, and index, and why do placeholders matter when automating?
**Keywords:** visible text, value attribute, index, placeholder, getOptions
<details>
<summary>Click to Reveal Answer</summary>

Each `<option>` has **visible text** (what the user reads), a **value** attribute (what is submitted to the server, usually a stable code), and an implicit 0-based **index**. `selected` marks the default option and `disabled` makes an option unselectable. Many dropdowns start with a **placeholder** like `<option value="" disabled selected>Select a country</option>` at index 0, so picking index 0 selects the placeholder instead of a real choice, and selecting a disabled option fails. That is why, the first time you automate a new dropdown, you print the `getOptions()` list with texts and values.
</details>

---

## Intermediate (Application)

### Q32: You need to (a) click a Login button, (b) read an error banner after a bad login, (c) read the value of an `<input type="hidden">`, and (d) wait for a "Saving..." overlay to finish. Which wait condition would you use for each, and why?
**Keywords:** elementToBeClickable, visibilityOfElementLocated, presenceOfElementLocated, invisibilityOfElementLocated, visible
**Hint:** Compare presence, visibility, and clickability.
<details>
<summary>Click to Reveal Answer</summary>

(a) `elementToBeClickable`, because you are about to click and the element must be visible and enabled. (b) `visibilityOfElementLocated`, because you need visible text to read. (c) `presenceOfElementLocated`, because a hidden input is never **visible**, so waiting for visibility would always time out. (d) `invisibilityOfElementLocated`, because you are waiting for something to go away (it also returns true if the element is not in the page at all). Presence means it exists in the HTML, visibility means it exists and the user can see it, and clickable means visible and enabled, though it does not guarantee that nothing covers it.
</details>

---

### Q33: A checkout test fails with `ElementClickInterceptedException` naming a cookie banner as the element that would receive the click. How do you diagnose and fix it, and when, if ever, would you use a JavaScript click?
**Keywords:** ElementClickInterceptedException, overlay, invisibilityOfElementLocated, scrollIntoView, JavaScript click
**Hint:** Read the exception message in three parts and follow the order of escalation.
<details>
<summary>Click to Reveal Answer</summary>

The message tells you what you tried, where, and which element is in the way (the cookie banner covering the button's center point). The proper fix is to deal with the **overlay**: accept the banner as part of setup or wait with `invisibilityOfElementLocated`, then wait for `elementToBeClickable` and click. The order of escalation is: wait for clickable, wait for overlays to disappear, scroll the element to the center (`scrollIntoView({block:'center'})`), close banners/modals, and only then a **JavaScript click** with a comment, mentioned in code review. A JavaScript click bypasses Selenium's checks and can hide real bugs, such as a button permanently covered by a modal that a real user could never click.
</details>

---

### Q34: In a registration form, you pick "Canada" in a country dropdown and immediately select "Ontario" in the state dropdown, but the test fails with `Cannot locate option with text: Ontario`. What is going on and how do you fix it?
**Keywords:** dependent dropdown, AJAX, wait, lambda, new Select
**Hint:** Think about when the state options arrive compared with when the test looks for them.
<details>
<summary>Click to Reveal Answer</summary>

The state dropdown is **dependent**: choosing the country triggers an **AJAX** request that loads the states, and the test looks for "Ontario" while the list still holds only the placeholder. The fix is to **wait** with a custom lambda until the options have loaded, for example `wait.until(d -> new Select(d.findElement(By.id("state"))).getOptions().size() > 1)`, or more precisely wait until an option with the text "Ontario" exists using `anyMatch`. Then select it. Create a **new Select** inside the lambda and again afterwards, because the old element reference may be stale if the page re-renders the list.
</details>

---

### Q35: Your test saves a table row, clicks a "Refresh" button that re-renders the list, and then fails intermittently with `StaleElementReferenceException`. Explain why and show how you would make it reliable.
**Keywords:** StaleElementReferenceException, stalenessOf, re-locate, locator, re-render
**Hint:** Think of a saved element as a photo of a house that has been rebuilt.
<details>
<summary>Click to Reveal Answer</summary>

Your saved `WebElement` is a reference to an old element; when the page re-renders the DOM, that element is no longer attached, so using it throws `StaleElementReferenceException`. The pattern is to save the old row, click refresh, `wait.until(ExpectedConditions.stalenessOf(oldRow))` to prove the re-render really happened, and then **re-locate** the new row by **locator** with `visibilityOfElementLocated`. Skipping the staleness wait is a classic bug because you may grab the old row just before it is replaced. More generally, do not keep element references across actions that change the page, and have helpers take a `By` rather than a `WebElement`.
</details>

---

## Advanced (Deep Dive)

### Q36: A project sets an implicit wait of 10 s and also uses an explicit `WebDriverWait` of 10 s. A test waits for an element that never appears. What happens under the hood, how long does it take to fail, and what do you do about it?
**Keywords:** implicit wait, explicit wait, findElement, poll, 20 seconds, Duration.ZERO
**Hint:** Ask where the implicit wait is applied while the explicit wait is polling.
<details>
<summary>Click to Reveal Answer</summary>

`until` starts its 10 s clock and runs the condition, which calls `findElement`. Because the implicit wait is applied inside every `findElement`, that single call retries for up to 10 s before throwing `NoSuchElementException`, which `until` ignores. By then the explicit limit is nearly reached, but `until` still does one more poll (another 10 s inside `findElement`) before checking the clock, so the failure takes about **20 seconds** or more, not the 10 you asked for, and the behavior varies between drivers. The Selenium documentation warns not to mix them. The fix is to use explicit waits in your framework and keep the implicit wait at 0; for an inherited project, set it back to `Duration.ZERO` in a single place and replace failing lookups with explicit waits one at a time.
</details>

---

# Day 3 - Wednesday: Actions, Windows and POM

## Beginner (Foundational)

### Q37: What is the Actions API in Selenium, and why isn't `click()` and `sendKeys()` enough for some user gestures?
**Keywords:** low-level input devices, pointer, keyboard, wheel, sequence
**Hint:** Think about what a real user does besides clicking and typing.
<details>
<summary>Click to Reveal Answer</summary>

The Actions API is the part of Selenium that lets you describe low-level input devices and their movements, then execute that description as one continuous gesture. The devices are a pointer (the mouse), a keyboard, and a wheel for scrolling (new in Selenium 4). `element.click()` does exactly one thing: it clicks the middle of an element. Real gestures such as hover or drag are a sequence ("move here, press the button, move there, release"), and a single method call cannot express that. In Java the entry point is `new Actions(driver)`.
</details>

---

### Q38: In the Actions API, what do `build()` and `perform()` do, and what happens if you forget `perform()`?
**Keywords:** perform, build, Action, chain, no error
<details>
<summary>Click to Reveal Answer</summary>

Methods like `moveToElement` and `click` only add steps to the chain (the "recipe") and return the same `Actions` object, which is the fluent style. `build()` compiles the steps into a single `Action` object, and `perform()` sends them to the browser to be executed. In Selenium 4, `perform()` calls `build()` for you, so `build()` is only needed if you want to keep the compiled `Action` and run it more than once. If you forget `perform()`, nothing happens and there is no error, which is the most common beginner mistake.
</details>

---

### Q39: How would you test a menu that only shows its submenu items when the mouse hovers over it? Why do you need a wait afterwards?
**Keywords:** moveToElement, hover, hidden, explicit wait, visibility
**Hint:** A plain click on the hidden item fails with `ElementNotInteractableException`.
<details>
<summary>Click to Reveal Answer</summary>

Use `new Actions(driver).moveToElement(menu).perform()` to move the pointer to the center of the parent element, which triggers the hover and makes the hidden content visible. The hidden item is in the page but not visible, so Selenium refuses to click it until the hover happens. After the hover you must use an explicit wait, such as `visibilityOfElementLocated`, because the revealed element may take a moment to appear (animations are common). Then a normal `click()` on the item is enough; Actions is only needed for the hover.
</details>

---

### Q40: What are the three kinds of JavaScript dialogs, and why can't you find them with `driver.findElement`?
**Keywords:** alert, confirm, prompt, DOM, browser
<details>
<summary>Click to Reveal Answer</summary>

The three are `alert` (a message with OK only), `confirm` (OK and Cancel, returning true or false), and `prompt` (a text box with OK and Cancel, returning the text or null). They are drawn by the browser, not by the page's HTML, so they are not part of the DOM and you cannot inspect them with DevTools or locate them with `By`. Selenium handles them through a dedicated `Alert` interface obtained with `driver.switchTo().alert()`.
</details>

---

### Q41: Walk me through the methods of the `Alert` interface and what each one does.
**Keywords:** getText, accept, dismiss, sendKeys, switchTo().alert()
<details>
<summary>Click to Reveal Answer</summary>

You first get the dialog with `driver.switchTo().alert()`. `getText()` returns the message shown, `accept()` clicks OK, `dismiss()` clicks Cancel (on a plain alert with only OK it behaves like OK), and `sendKeys("text")` types into a prompt's text box. After `accept()` or `dismiss()` the dialog closes and focus returns to the page automatically. You should read the text before closing, because the `Alert` object can no longer be used afterwards.
</details>

---

### Q42: What happens if a JavaScript alert is open and your test calls another command like `findElement`? How do you read and fix that failure?
**Keywords:** UnhandledAlertException, dismiss, alert text, alertIsPresent, explicit
**Hint:** Selenium's default "unhandled prompt behaviour" does something to the alert for you.
<details>
<summary>Click to Reveal Answer</summary>

By default Selenium dismisses the alert and throws `UnhandledAlertException`, with the dialog's text in the message, for example `unexpected alert open: {Alert text : I am a JS Alert}`. That text tells you which dialog it was. Because the alert is already dismissed, a retry of the same line may succeed, which makes the failure look random. The fix is to handle the dialog explicitly first, waiting for it with `alertIsPresent()`, then `accept()` or `dismiss()`. You can change the default with `setUnhandledPromptBehaviour`, but normal tests should handle alerts explicitly and assert on the text.
</details>

---

### Q43: What is a window handle, and why does Selenium need one?
**Keywords:** window handle, unique, getWindowHandle, getWindowHandles, Set
<details>
<summary>Click to Reveal Answer</summary>

A window handle is a unique string identifier the browser gives to each window or tab, a bit like a cloakroom ticket: it identifies the window rather than describing it. Titles and URLs can be duplicated, so Selenium uses the handle to know exactly which window you mean. `getWindowHandle()` returns the handle of the window currently controlled, and `getWindowHandles()` returns a `Set<String>` of all open handles. A `Set` has no guaranteed order, and handles are valid only for that session.
</details>

---

### Q44: Selenium controls only one window at a time. What does that mean when a link opens a new tab, and what is the standard pattern to handle it?
**Keywords:** switchTo().window, original handle, numberOfWindowsToBe, close, wait
**Hint:** The driver does not follow the new tab on its own.
<details>
<summary>Click to Reveal Answer</summary>

After the click, the driver still points at the old window, so `findElement` keeps searching the old page and fails with `NoSuchElementException`. The pattern is: store the original handle, click the link, wait with `ExpectedConditions.numberOfWindowsToBe(2)`, loop through `getWindowHandles()` and `switchTo().window(handle)` for the one that is not the original, do your work, then `driver.close()` and `switchTo().window(original)`. The wait is needed because the new window may not exist yet right after the click.
</details>

---

### Q45: What is an iframe, and why can't `driver.findElement` on the main page find an element inside it? How do you get in and out?
**Keywords:** iframe, separate DOM, switchTo().frame, parentFrame, defaultContent
<details>
<summary>Click to Reveal Answer</summary>

An iframe embeds one HTML page inside another, for example a payment form or rich-text editor, and the inner document is a separate DOM from the outer page. So a main-page `findElement` throws `NoSuchElementException` even though the element is visible on screen. You enter with `switchTo().frame(...)` using an index, a name or id, or a `WebElement`, and the robust option is `frameToBeAvailableAndSwitchToIt`. To leave, `parentFrame()` climbs one level and `defaultContent()` returns to the top-level page.
</details>

---

### Q46: What problem does the Page Object Model solve, and what is the basic idea?
**Keywords:** page object, locators, duplication, maintainability, one class per page
<details>
<summary>Click to Reveal Answer</summary>

Without structure, a suite of 100 tests may each repeat the same locators and steps, so a single renamed button id breaks 100 tests and you must edit 100 places. POM fixes this by creating one class for each page (or significant component) that contains the locators of its elements and methods describing what a user can do there. Tests call those methods and never touch locators directly, so a UI change is fixed in one class. The result is better maintainability, reusability, and readability.
</details>

---

### Q47: What are the main rules of a good page object?
**Keywords:** locators are private, no assertions, next page object, waits, business names
<details>
<summary>Click to Reveal Answer</summary>

Locators are private and tests never see `By` objects. Methods represent user actions or queries with business names such as `addToCart(item)`, not `clickButton3()`. Page classes contain no assertions; they report state and the test decides pass or fail. Navigation methods return the next page object (and methods that stay on the same page return `this`), which enables method chaining. Waits belong in the page object or its base class, and each class should be small and focused, with reusable parts split into components.
</details>

---

### Q48: Why should page classes not contain assertions? Give an example.
**Keywords:** assertions, reuse, negative test, report state, test decides
<details>
<summary>Click to Reveal Answer</summary>

Page objects should report state (for example `isLoaded()` or `getErrorMessage()`) while the test decides pass or fail with an assertion library. If `LoginPage.loginAs` contained `assertTrue(url.contains("inventory"))`, a negative test with a wrong password could never reuse it, because the assertion would fail by design. When the page only reports, the positive test asserts "inventory" and the negative test asserts that an error is shown. This keeps pages reusable for both positive and negative tests.
</details>

---

### Q49: What is Page Factory, and how do `@FindBy` and `PageFactory.initElements` work?
**Keywords:** @FindBy, initElements, proxy, lazy, WebElement
<details>
<summary>Click to Reveal Answer</summary>

Page Factory is a Selenium support class where you declare `WebElement` fields annotated with `@FindBy` (recording how to find each element) instead of `By` fields. `PageFactory.initElements(driver, this)` assigns each annotated field a proxy that implements `WebElement`. The proxy does not search when the page object is created; it performs a fresh `findElement` every time you use the field. This is lazy initialisation. If you forget `initElements`, the fields stay null and the first use throws `NullPointerException`.
</details>

---

## Intermediate (Application)

### Q50: Your test clicks a Delete button and a confirm dialog appears. How would you write a test for this feature, and what would you assert?
**Keywords:** accept, dismiss, both branches, alertIsPresent, assert the page result
**Hint:** A confirm has two outcomes, and each is a different code path.
<details>
<summary>Click to Reveal Answer</summary>

Click Delete, wait with `alertIsPresent()` to get the `Alert`, read and assert its text, then close it. Write two tests covering both branches. With `accept()`, assert the item is gone from the list, the count dropped by one, and a success message appears. With `dismiss()`, assert the item is still in the list and no success message shows. Asserting only that an alert appeared is a weak test; you must also assert the page result, because that proves the page's JavaScript reacted to the choice.
</details>

---

### Q51: A drag-and-drop test using `dragAndDrop` runs without errors, but nothing changes on the page. What could be going on, and what would you try?
**Keywords:** HTML5 native drag, manual sequence, clickAndHold, release, assert the result
**Hint:** There are two families of drag and drop on the web.
<details>
<summary>Click to Reveal Answer</summary>

The page may use HTML5 native drag and drop (`draggable="true"` with `dragstart` / `drop` events), which browsers sometimes do not fire for synthetic pointer movements. Actions may then do nothing and Selenium reports no error, so you should always assert the result of a drag. Try the manual sequence, which gives more control: `clickAndHold(source).moveToElement(target).pause(...).release().perform()`. Other options are trying offsets, a JavaScript fallback that dispatches the drag events, or testing the behaviour through an API. Mouse-event libraries like jQuery UI work with plain `dragAndDrop`.
</details>

---

### Q52: A test clicks "Terms and Conditions", which opens a new tab, but then fails with `NoSuchElementException` on an element you can see on screen. Diagnose and fix it.
**Keywords:** switchTo().window, still pointing at the old tab, getTitle, numberOfWindowsToBe, handle not the original
**Hint:** Check what `driver.getTitle()` returns just before the failing line.
<details>
<summary>Click to Reveal Answer</summary>

The locator is probably right, but the driver is still pointing at the old tab, because Selenium does not follow new windows automatically. Check `getTitle()` or `getCurrentUrl()` before the failing line; if it shows the old page, you have not switched. Fix it by remembering the original handle, waiting with `numberOfWindowsToBe(2)`, and calling `switchTo().window(handle)` for the handle that is not the original. Do not assume the new handle is the last in the `Set`, since it is unordered. When finished, `close()` the tab and switch back to the original, otherwise you get `NoSuchWindowException`.
</details>

---

### Q53: Your team has a Page Factory page where a field marked `@CacheLookup` throws `StaleElementReferenceException` after a sort. Why, and when would you choose plain POM over Page Factory?
**Keywords:** @CacheLookup, stale, re-render, dynamic locators, By fields
**Hint:** Think about what the proxy remembers when caching is on.
<details>
<summary>Click to Reveal Answer</summary>

`@CacheLookup` makes the proxy remember the first found element instead of looking it up on each use. When the page re-renders, as it does after sorting, the cached element belongs to the old DOM and becomes stale; the fix is to remove `@CacheLookup`, which should only be used on truly static elements such as a logo. Plain POM with `By` fields locates at the moment of use, so it avoids this. It is also preferable when you have many dynamic locators (such as a product name in a locator, since `@FindBy` values must be constants), optional elements, and heavy waiting needs.
</details>

---

## Advanced (Deep Dive)

### Q54: Design a window helper so that a page-object method can click a link that opens a new window and return the next page object, without the test touching window handles. What steps would it perform?
**Keywords:** snapshot, Runnable, wait, not in the snapshot, return original handle
**Hint:** Take a snapshot of the handles before the click and compare afterwards.
<details>
<summary>Click to Reveal Answer</summary>

A `WindowUtils` method such as `switchToNewWindowAfter(Runnable action)` stores the original handle and a snapshot `before` of `getWindowHandles()`. It then runs the click passed in as a lambda, and waits with a lambda condition until the number of handles is greater than the snapshot size. It loops through the handles, switches to the one that is not in the snapshot (deterministic, unlike picking from an unordered `Set`), and returns the original handle so the caller can come back. If no new handle appears it throws a clear `NoSuchWindowException`. A page-object method like `openPrivacyPolicy()` calls it and returns a new page object for the new window, so tests never handle handles.
</details>

---

# Day 4 - Thursday: BDD and Cucumber

## Beginner (Foundational)

### Q55: Can you explain what BDD is and what problem it was invented to solve?
**Keywords:** collaborative, concrete examples, misunderstanding, plain-language, automate
<details>
<summary>Click to Reveal Answer</summary>

Behavior-Driven Development is a **collaborative** approach in which a team discusses **concrete examples** of how the system should behave, documents them in a structured **plain-language** format, and then **automates** them as tests. It was invented to attack **misunderstanding** between business people, developers and testers, because a bug in the requirement is the most expensive kind: the team builds, tests and ships it with confidence. The tools (Cucumber, Gherkin) are the least important part; BDD is a conversation first, a documentation format second and an automation tool third, so a team that installs Cucumber but never talks to the business is not really doing BDD.
</details>

---

### Q56: What are the Three Amigos, and why do we hold that meeting before development starts?
**Keywords:** business, development, testing, concrete examples, before development
<details>
<summary>Click to Reveal Answer</summary>

The Three Amigos is a short, time-boxed meeting (typically 25-30 minutes) held **before development** of a story begins, with three perspectives: **business** (what problem we solve and the business rule), **development** (what is feasible and how it might be built) and **testing** (the skeptical "what if" mindset). Together they produce **concrete examples**, including edge cases and rules, which later become scenarios. Each amigo catches a different kind of mistake: without business you build something nobody wants, without development you agree to something impossible, without testing you cover only the happy path. If you hold it after coding, it is a review, not discovery.
</details>

---

### Q57: Walk me through the BDD cycle. What are the phases and what does each one produce?
**Keywords:** Discovery, Formulation, Automation, Gherkin, step definitions
<details>
<summary>Click to Reveal Answer</summary>

The cycle is **Discovery**, **Formulation** and **Automation**. In Discovery the team explores the story through workshops and produces shared understanding, rules, concrete examples and open questions. In Formulation the examples are written as scenarios in **Gherkin**, giving readable `.feature` files. In Automation, **step definitions** turn each Gherkin line into executable code, giving an automated test and a living specification. The order matters, because teams that jump straight to automation end up with automated tests of the wrong behavior, and feedback from automation flows back into the conversation.
</details>

---

### Q58: What is "living documentation" and why do feature files stay accurate?
**Keywords:** executable, green, red, stay accurate, CI
<details>
<summary>Click to Reveal Answer</summary>

Living documentation means the feature files are **executable**: the same scenarios that describe behavior are run as tests. A **green** scenario proves the behavior works today; a **red** one signals either a bug or an out-of-date specification, so the description and the system cannot silently drift apart. That is how they **stay accurate**, unlike a Word requirements document. To keep it alive, run the scenarios regularly (ideally on every change in a **CI** pipeline), fix or retire failing scenarios rather than ignoring them, and keep the feature files in the same repository as the code and review them like code.
</details>

---

### Q59: What is a user story, what are its parts, and why is the "so that" part important?
**Keywords:** role, goal, benefit, Card, Conversation, Confirmation
<details>
<summary>Click to Reveal Answer</summary>

A user story is a short, plain-language description of a feature from the perspective of the person who wants it, in the template "As a `<role>`, I want `<goal>`, so that `<benefit>`". The **role** says who benefits, the **goal** says what they want to do (not the solution), and the **benefit** says why it matters. The "so that" is the most often skipped but most valuable part, because it helps decide priority and alternatives, and if nobody can say why a feature is wanted it may not need building. A story is a promise for a conversation, described by the 3 Cs: **Card** (the short description), **Conversation** (the discussion that fills in details) and **Confirmation** (the acceptance criteria that prove it is done).
</details>

---

### Q60: What does INVEST stand for, and why is it useful when reviewing a story?
**Keywords:** Independent, Negotiable, Valuable, Estimable, Small, Testable
<details>
<summary>Click to Reveal Answer</summary>

INVEST is a checklist of six qualities of a good story: **Independent** (can be delivered without another story), **Negotiable** (details open to discussion, not a contract), **Valuable** (delivers value to a user or the business), **Estimable** (the team can roughly size it), **Small** (fits in one iteration) and **Testable** (you can write tests that prove it works). You go through the letters like a pre-flight checklist and repair or split stories that fail. Testable is the quality closest to the tester's role: if you cannot write at least one passing and one failing example, the story is not ready.
</details>

---

### Q61: What is the difference between acceptance criteria and the Definition of Done?
**Keywords:** acceptance criteria, Definition of Done, one specific story, every story, team-wide
<details>
<summary>Click to Reveal Answer</summary>

**Acceptance criteria** are the conditions that **one specific story** must satisfy to be accepted by the business; they describe functional behavior specific to that story, for example "a locked-out user sees an error message". The **Definition of Done** applies to **every story** as a **team-wide** quality standard, for example code reviewed, unit tests passing, or all regression tests passing. The lesson's analogy is a restaurant: the customer's order ("steak, medium-rare, no mushrooms") is the acceptance criteria, while the kitchen's hygiene rules are the Definition of Done, and you need both. Acceptance criteria also form the basis of the BDD scenarios.
</details>

---

### Q62: What is Gherkin, and how does it relate to Cucumber? Can you describe the structure of a feature file?
**Keywords:** Gherkin, .feature, Cucumber, Feature, Scenario, text
<details>
<summary>Click to Reveal Answer</summary>

**Gherkin** is a line-oriented, plain-text language with a small set of keywords, stored in **.feature** files (typically under `src/test/resources/features`); **Cucumber** is the tool that reads those files and executes them against step definitions. A file contains exactly one **Feature** (title plus an optional free-text description, where the user story usually goes), one or more **Scenario**s, and each scenario contains steps starting with `Given`, `When`, `Then`, `And` or `But`. Cucumber matches steps by their **text** only; the keywords are for human readers. Comments start with `#` at the start of a line, and a `#` after step text becomes part of the step text.
</details>

---

### Q63: When would you use a data table in a step, and when a doc string? How does each reach the Java code?
**Keywords:** data table, doc string, DataTable, asMaps, String
<details>
<summary>Click to Reveal Answer</summary>

Use a **data table** (lines starting with `|` directly under a step) when one step carries a grid of values of the same shape, such as several products with quantities. It reaches Java as an `io.cucumber.datatable.DataTable`, and `table.asMaps()` turns each row after the header into a map from column name to cell value. Use a **doc string**, delimited by `"""`, for one block of multi-line text such as an email body or JSON; it arrives as a single `String`. For just one or two values, use neither and put them in quotes inside the step text. Both belong to the step directly above them.
</details>

---

### Q64: What is the difference between a feature and a scenario, and why should each scenario test only one behavior?
**Keywords:** feature, scenario, one behavior, description, user story
<details>
<summary>Click to Reveal Answer</summary>

A **feature** is a cohesive capability that provides value to a user (such as Shopping cart), specified in one feature file whose **description** holds the **user story**. A **scenario** is one concrete example of one rule or acceptance criterion; in test terms it is one test case. Each scenario should test **one behavior** so that when it fails the title tells you exactly what is broken. A scenario with several unrelated Whens is like driving London to Paris and only checking whether you arrived: if you did not, you cannot tell whether the engine, tyres or map failed, and later steps are skipped after the first failure.
</details>

---

### Q65: Explain the roles of Given, When and Then, and how they relate to Arrange-Act-Assert.
**Keywords:** Given, When, Then, Arrange, Act, Assert
<details>
<summary>Click to Reveal Answer</summary>

**Given** sets the context, a state that is already true (for example "the shopper is logged in"), which corresponds to **Arrange**. **When** describes the one action or event under test (for example "the shopper adds a product"), which is **Act**. **Then** states the observable, specific outcome (for example "the cart count shows 1"), which is **Assert**. `And` and `But` continue the previous keyword's role. Given should be worded as state, not action, and Then must be something observable from outside, with no actions in it. Cucumber ignores the keyword when matching, so this discipline is for readers and for keeping scenarios precise.
</details>

---

### Q66: What is a step definition, and how does Cucumber decide which one to run for a step?
**Keywords:** step definition, annotation, Cucumber Expression, {string}, undefined, ambiguous
<details>
<summary>Click to Reveal Answer</summary>

A **step definition** is a Java method marked with an **annotation** (`@Given`, `@When` or `@Then`) holding a pattern, usually a **Cucumber Expression**. Cucumber strips the keyword, compares the remaining text with every definition's pattern, extracts parameters such as `{string}` (quoted text, quotes removed) or `{int}`, converts them to the method's Java types and calls the method. Only the text matters, not the keyword or the method name. If zero definitions match the step is **undefined** and Cucumber prints a snippet; if more than one matches it is **ambiguous** and must be fixed.

```java
@When("the shopper adds {string} to the cart")
public void theShopperAddsToTheCart(String product) { ... }
```
</details>

---

### Q67: What are the main building blocks of a Cucumber-JVM project, and what does the runner class do?
**Keywords:** feature files, step definitions, runner, glue, src/test/resources
<details>
<summary>Click to Reveal Answer</summary>

There are four blocks: **feature files** (Gherkin, under `src/test/resources/features`), **step definitions** (Java glue, under `src/test/java/.../steps`), page objects and support code (such as `TestContext`), and the **runner** plus configuration. The runner is a small class with an empty body whose annotations do the work: `@Suite` and `@IncludeEngines("cucumber")` tell JUnit Platform to use the Cucumber engine, `@SelectClasspathResource("features")` says where the features are, and `@ConfigurationParameter` entries set the **glue** package and the plugin such as `pretty`. Its name ends in `Test` so Maven's Surefire finds it.
</details>

---

## Intermediate (Application)

### Q68: A scenario passes when run alone but fails when run after another scenario that left items in the cart. What is wrong and how do you fix it?
**Keywords:** independent, Given, hidden state, any order, fresh browser
**Hint:** Ask where the starting state of the failing scenario comes from.
<details>
<summary>Click to Reveal Answer</summary>

The scenario has **hidden state**: it never states its own starting point, so its result depends on what ran before it. Each scenario must be **independent** and create its own context in its **Given** steps, so it can run alone, in **any order** or in parallel, and one failure does not cascade into false failures. Fix it by adding explicit Givens such as "the shopper is logged in" and "the shopper has an empty cart", hidden behind business-level steps whose Java implementation may do several UI actions. Because each scenario gets a **fresh browser** state (a new WebDriver and a clean session, arranged in the setup), the cart really starts empty each time.
</details>

---

### Q69: A colleague's scenario titled "Test 7" has twelve steps that type into fields by id and click selectors. How would you review and improve it?
**Keywords:** declarative, business language, locators, page objects, one behavior
**Hint:** Think about what must change when the UI is redesigned.
<details>
<summary>Click to Reveal Answer</summary>

It is imperative: it scripts UI mechanics instead of describing behavior. Rewrite it in **declarative** steps in **business language**, for example "the shopper checks out without a first name", so that no **locators**, URLs or waits appear in the feature; those move into step definitions and **page objects**. Rename the title to state the behavior (subject, behavior, condition), keep **one behavior** per scenario, collapse the setup into a business-level Given, and make the Then specific, such as the exact error message. The payoff is the redesign test: if a button id or label changes, only a page object changes and the feature files, which the business signed off, stay the same.
</details>

---

### Q70: You wrote step definitions, but the run shows "3 Steps (3 undefined)". How do you diagnose it?
**Keywords:** glue, package, text, dry run, undefined
**Hint:** The features were found, so look at how Cucumber finds and matches the Java code.
<details>
<summary>Click to Reveal Answer</summary>

Since the scenario ran and reported **undefined**, the features were found, but no definitions matched. Check in order: whether the **glue** value in the runner exactly equals the **package** name of the step classes (for example `step` versus `steps`) and that the package line matches the folder; whether the step class is public with a usable constructor; whether the annotations are imported from `io.cucumber.java.en`; and whether the **text** matches character for character (curly quotes, extra spaces, singular versus plural, or a trailing `# comment` that became part of the step text). Use a **dry run** (`-Dcucumber.execution.dry-run=true`) to re-check matching quickly without opening a browser.
</details>

---

### Q71: A product owner hands you the story "As a user, I want the system to be fast." How do you handle it?
**Keywords:** INVEST, Testable, acceptance criteria, measurable, out of scope
**Hint:** Ask what a tester could actually check.
<details>
<summary>Click to Reveal Answer</summary>

Push back in refinement, because the story fails **INVEST**: "user" names no real role, "fast" is vague, so it is not **Testable** or estimable, and it has no benefit. Replace vague words with numbers, lists and exact messages, for example "As a shopper, I want search results to appear within 2 seconds, so that I do not abandon the site". Then write **acceptance criteria** that are specific and **measurable** (how fast, measured how, on what environment), unambiguous, atomic, and complete with boundaries, and state what is **out of scope**. Use the "two testers" test: if two testers could write different tests that both satisfy a criterion, it is still ambiguous.
</details>

---

## Advanced (Deep Dive)

### Q72: A scenario has steps implemented in two different classes, `LoginSteps` and `CartSteps`, yet both use the same browser. What happens under the hood from the moment the scenario starts?
**Keywords:** text, Cucumber Expression, PicoContainer, TestContext, constructor, new instance
**Hint:** Think about how the step classes get their dependency and when the browser is created.
<details>
<summary>Click to Reveal Answer</summary>

Cucumber reads the scenario and, for each step, strips the keyword and matches the **text** against the **Cucumber Expression** of every definition, capturing and converting parameters such as `{string}` or `{int}`. It creates a **new instance** of each needed step class per scenario, so fields never leak between scenarios. Both classes declare a **constructor** that takes a `TestContext`, so **PicoContainer** (from `cucumber-picocontainer`) creates one `TestContext` per scenario and passes the same instance to both. The browser is created lazily the first time a step calls `context.driver()`, so every step class gets the same WebDriver. When the scenario ends the objects are discarded; static variables should be avoided because they survive across scenarios.

```java
public CartSteps(TestContext context) { this.context = context; }
```
</details>

---

# Day 5 - Friday: Advanced Cucumber

## Beginner (Foundational)

### Q73: What is a Scenario Outline, and what problem does it solve?
**Keywords:** Scenario Outline, placeholders, Examples table, once per row
**Hint:** Think about three scenarios that are identical except for a few words of data.
<details>
<summary>Click to Reveal Answer</summary>

A Scenario Outline is a template scenario containing placeholders in angle brackets, such as `<username>`, followed by an Examples table that supplies the values. Cucumber runs the template once for every data row, replacing the placeholders with that row's values. It solves the copy-paste problem: near-identical scenarios that differ only in data, where one wording change would otherwise need editing in many places. The header row of the Examples table names the columns, which must equal the placeholder names, and the header itself never runs as data.

```gherkin
Scenario Outline: Login with <description> is rejected
  When the customer logs in with username "<username>" and password "<password>"
  Examples:
    | description      | username      | password       |
    | a wrong password | standard_user | wrong_password |
```
</details>

---

### Q74: Walk me through what Cucumber does with an outline that has three Examples rows. What actually runs for each row?
**Keywords:** expands, one scenario per row, hooks, Background, fresh TestContext
<details>
<summary>Click to Reveal Answer</summary>

Before running, Cucumber expands the outline into ordinary scenarios, one per data row, and replaces each placeholder with the cell value before the step text is matched to a step definition. That is why no special step definitions are needed for outlines. Each expanded scenario is a full scenario, so the `@Before` hooks, the Background, the steps and the `@After` hooks run three times, with a fresh `TestContext` and a fresh browser for every row. The rows do not share state, and if one row fails the others still run and keep their own results.
</details>

---

### Q75: What is the difference between an Examples table in a Scenario Outline and a data table attached to a step? How do you decide which to use?
**Keywords:** whole scenario repeats, one step, DataTable, one execution per row
<details>
<summary>Click to Reveal Answer</summary>

An Examples table belongs to an outline and makes the entire scenario run once per row, so the step definitions receive ordinary parameters such as `String` or `int`. A data table is attached to a single step and gives structured data to that one step in a single run; the Java method reads it as a `DataTable`. The quick test is to ask whether the whole scenario should repeat for each row. If yes, use an outline, for example checking five different users are locked out. If the rows are all inputs to the same action, use a data table, for example adding three listed products to one cart. The cost differs too: the outline launches one browser per row, the data table only one.
</details>

---

### Q76: What is a Background in Gherkin, and when does it run?
**Keywords:** shared Given steps, before each scenario, every outline row, at most one, independent
<details>
<summary>Click to Reveal Answer</summary>

A Background holds shared context steps, usually Given steps, that Cucumber runs before every scenario in the feature, or in the Rule if it sits inside one. It removes repeated lines such as `Given the shopper is logged in`. It runs before each scenario and before every row of a Scenario Outline, not once per feature, which keeps scenarios independent at the cost of some time. A feature or Rule may have at most one Background, and it goes directly after the Feature description, before the first scenario. If a Background step fails, the scenario fails, the remaining steps are skipped and `@After` hooks still run.
</details>

---

### Q77: What is a Rule in Gherkin, and does it change how tests execute?
**Keywords:** business rule, groups scenarios, Example, organization, no effect on execution
<details>
<summary>Click to Reveal Answer</summary>

A Rule is a heading, written as a sentence, that states one business rule, and the scenarios below it (often written with the `Example` keyword) illustrate that rule. Its purpose is organization and documentation: features with several rules become easier to navigate, and gaps show up, such as a rule with only one example. A Rule has no effect on execution; Cucumber runs its examples as ordinary scenarios. A Rule can be tagged, which applies the tag to all its scenarios, and it can have its own Background that runs after the feature-level Background.
</details>

---

### Q78: What are Cucumber hooks, and why do we use them instead of putting setup in a Background or in the last step?
**Keywords:** hooks, technical setup, @Before, @After, always runs, Background
<details>
<summary>Click to Reveal Answer</summary>

A hook is a Java method that Cucumber runs automatically at defined lifecycle points, such as before and after each scenario. Hooks hold technical setup and cleanup, for example starting and quitting the browser or capturing a screenshot. The Background is business-visible Gherkin context, while hooks are invisible to the business reader, so the rule of thumb is: if the business reader would not care, use a hook. Cleanup in the last `Then` step is a mistake because after a failure the remaining steps are skipped and the cleanup never runs, leaving the browser open. An `@After` hook runs whether the scenario passed or failed.
</details>

---

### Q79: When there are several `@Before` and several `@After` hooks, how does Cucumber order them, and why is `@After` different?
**Keywords:** order attribute, ascending, descending, reverse, screenshot before quit
<details>
<summary>Click to Reveal Answer</summary>

You control hook order with the `order` attribute, whose default is 10000. `@Before` hooks run in ascending order, so order 0 runs before order 10. `@After` hooks run in descending order, the reverse, so order 10 runs before order 0. This mirrors nested setup and teardown: what was set up first is torn down last, like socks on first and off last. It matters in practice because the screenshot hook needs the higher `@After` order so it runs while the browser still exists, and the quit hook needs the lower order so it runs last.
</details>

---

### Q80: What is a tag, where can you put it, and what is tag inheritance?
**Keywords:** @ label, Feature, Rule, Examples, inherited downward
<details>
<summary>Click to Reveal Answer</summary>

A tag is a word starting with `@`, with no spaces, written on the line above a Gherkin keyword. Tags can be placed above Feature, Rule, Scenario, Scenario Outline and Examples, but not on a Background or on individual steps. They are inherited downward: a scenario carries its own tags plus those of its Rule and Feature, and a tag on an Examples block applies only to that block's rows. Tags never bubble up, so a `@smoke` tag on one scenario does not make its neighbors smoke tests. Tag names are case-sensitive, so `@Smoke` and `@smoke` differ.
</details>

---

### Q81: Explain how a tag expression works and what `@smoke and not @slow` selects.
**Keywords:** and, or, not, parentheses, cucumber.filter.tags
<details>
<summary>Click to Reveal Answer</summary>

A tag expression is a small Boolean language using `and`, `or`, `not` and parentheses to select scenarios by their full, inherited tag set. `@smoke and not @slow` selects scenarios that carry `@smoke` and do not carry `@slow`. Precedence is `not`, then `and`, then `or`, so you should use parentheses to state your intent. You supply the expression through the `cucumber.filter.tags` key, for example `mvn test -Dcucumber.filter.tags="@smoke and not @slow"`, and you quote it in the shell. Filtered-out scenarios are excluded before the run and do not appear in the results at all.
</details>

---

### Q82: Why does Cucumber need JUnit, and what do the main annotations on the JUnit 5 runner class do?
**Keywords:** JUnit Platform, Cucumber engine, @Suite, @IncludeEngines, @ConfigurationParameter
<details>
<summary>Click to Reveal Answer</summary>

Cucumber executes feature files but does not know how to be started by an IDE or build tool or how to report results to them; JUnit supplies discovery, execution and standard result reporting. The Cucumber engine is a plug-in for the JUnit Platform that turns each feature into a container and each scenario into a test. On the runner, `@Suite` marks a class that describes a run, `@IncludeEngines("cucumber")` limits it to the Cucumber engine, and `@SelectClasspathResource("features")` selects the feature files on the classpath. `@ConfigurationParameter` lines pass settings such as the glue packages, plug-ins and tag filter, and the class body is empty.
</details>

---

### Q83: What is the difference between JUnit 4 and JUnit 5 as far as Cucumber runners are concerned?
**Keywords:** @RunWith, @CucumberOptions, JUnit Platform, cucumber-junit-platform-engine, assertion message
<details>
<summary>Click to Reveal Answer</summary>

JUnit 4 was a single library; JUnit 5 was redesigned as a platform so many test engines, including Cucumber's, can plug in. A JUnit 4 Cucumber runner uses `@RunWith(Cucumber.class)` with `@CucumberOptions` and the `cucumber-junit` module. The JUnit 5 runner uses `@Suite` with `@ConfigurationParameter` and the `cucumber-junit-platform-engine` module, and it is the current standard with built-in parallel execution. You must not mix `cucumber-junit` and the Platform engine in one module. A classic migration trap is the assertion message position: it is the first argument in JUnit 4 but the last argument in JUnit 5.
</details>

---

### Q84: What is Maven doing for a test automation project, and what are dependency scopes and transitive dependencies?
**Keywords:** pom.xml, dependency management, scope, transitive, mvn dependency:tree
<details>
<summary>Click to Reveal Answer</summary>

Maven is a build and dependency management tool: the `pom.xml` declares the project's coordinates, properties, dependencies and plugins, and Maven downloads the libraries from Maven Central into the local repository and gives a repeatable command such as `mvn clean test`. A scope says when a dependency is needed. Cucumber and JUnit use `test` scope, while Selenium keeps the default `compile` scope because page objects in `src/main` use it. A transitive dependency is a dependency of your dependency, which Maven fetches automatically. You can see the whole tree with `mvn dependency:tree`, and when versions conflict the nearest definition wins.
</details>

---

### Q85: What does the built-in HTML report give you, and how do screenshots get into it?
**Keywords:** plug-ins, html, cucumber.plugin, scenario.attach, @After hook
<details>
<summary>Click to Reveal Answer</summary>

Cucumber plug-ins listen to run events and write them in a format; they are chosen with the `cucumber.plugin` property, for example `html:target/cucumber-reports/report.html`. The html plug-in writes a single self-contained file showing features, scenarios, steps, tags, failure messages and attachments, which you can email or upload as a CI artifact. To put a screenshot in it, an `@After` hook takes the picture with Selenium's `TakesScreenshot` as bytes when `scenario.isFailed()` is true and calls `scenario.attach(png, "image/png", "name")`. The JSON plug-in carries the same data for report generators.
</details>

---

## Intermediate (Application)

### Q86: A teammate wrote one Scenario Outline for login where some rows should log in successfully and others should show an error, using `Then the customer sees "<result>"`. Another outline has 40 UI rows of price calculations. How would you improve both?
**Keywords:** one outcome type, split into two outlines, key examples, unit test, slow browser
**Hint:** Think about what makes the Then step precise, and what each row costs.
<details>
<summary>Click to Reveal Answer</summary>

For the first, I would apply the rule of one outline, one outcome type. Mixed outcomes force a vague `Then` step and conditional code, so I would split it into one outline for successful logins (Then the customer sees the products page) and one for rejected logins (Then the error message "<message>" is displayed), using named Examples blocks to group rows by reason. Constants such as a shared password stay in the template rather than the table. For the second, each UI row launches a full browser scenario, so 40 rows is slow. I would keep a handful of key examples, such as typical, boundary and failure cases, and move the exhaustive calculation to a fast unit or API test.
</details>

---

### Q87: Your failure screenshot is blank, or a second browser window is left open after a failed run. The hooks are `@After` hooks in the same class. What is probably wrong and how do you fix it?
**Keywords:** order, quit hook, screenshot hook, higher order, hasDriver
**Hint:** Remember which `@After` order runs first.
<details>
<summary>Click to Reveal Answer</summary>

The quit hook is probably running before the screenshot hook. `@After` hooks run in descending order, so the screenshot hook needs the higher `order` (for example 10) and the quit hook the lower one (for example 0). With the lazy `TestContext.driver()`, a screenshot taken after `quitDriver()` silently starts a brand new browser, photographs a blank page and leaves that browser open. I would fix the orders and guard the screenshot with `context.hasDriver()`, and also wrap the capture in try/catch so a screenshot problem cannot hide the real failure. If the hooks never run at all, I would check that the Hooks class is in a glue package.
</details>

---

### Q88: A CI job runs `mvn test -Dcucumber.filter.tags="@smoek"` and the build is green, but you suspect nothing was tested. What is happening and how would you diagnose and prevent it?
**Keywords:** typo, 0 scenarios, BUILD SUCCESS, grep, minimum number of scenarios
**Hint:** Does Cucumber validate tag names?
<details>
<summary>Click to Reveal Answer</summary>

Cucumber does not validate tag names, so a mistyped tag matches no scenario. The run reports `0 Scenarios`, `Tests run: 0`, and may still end in `BUILD SUCCESS`, which is a green build that tested nothing. To diagnose, I would read the scenario count in the log and grep the features folder for the tag, for example `grep -r "@smoek" src/test/resources`. To prevent it, I would have the pipeline fail when fewer than an expected number of scenarios ran, or compare the count with the previous run. I would also check that the expression is quoted properly in the shell.
</details>

---

### Q89: Your team uses maven-cucumber-reporting, but after a failed test run no enhanced report appears. Why, and what options do you have?
**Keywords:** verify phase, testFailureIgnore, always-run CI step, built-in HTML, build status
**Hint:** Think about which phase the report plug-in is bound to.
<details>
<summary>Click to Reveal Answer</summary>

The report plug-in is bound to the `verify` phase, which comes after `test`. With Surefire's default `testFailureIgnore=false`, a failing test stops the build before `verify`, so the report is never generated. One option is `testFailureIgnore=true` or `-Dmaven.test.failure.ignore=true`, which always produces the report but leaves the build green despite failures, so another step must fail the pipeline. A second option is an always-run CI step, such as `if: always()`, that generates or publishes the report, which keeps the pipeline status honest. A third is to rely on the built-in `html` plug-in, which is written during the test run and so exists even after failures.
</details>

---

## Advanced (Deep Dive)

### Q90: Describe what happens under the hood when you run `mvn clean test` on a Cucumber project, from Maven starting to the first scenario's steps running. Where do the hooks and the Background fit?
**Keywords:** Surefire, JUnit Platform, Cucumber engine, tag filter, @Before, Background
**Hint:** Start with the phases Maven runs, then who finds the runner class, then what the engine does per scenario.
<details>
<summary>Click to Reveal Answer</summary>

Maven reads the `pom.xml`, resolves dependencies, `clean` deletes `target/`, and the compile phases build the main and test code and copy features and properties to `target/test-classes`, which is why the runner can use `@SelectClasspathResource("features")`. Surefire then scans for classes matching its name patterns such as `*Test`, finds the runner, and starts a forked JVM with the JUnit Platform. The platform sees `@Suite`, and `@IncludeEngines("cucumber")` means only the Cucumber engine takes part. The engine reads the configuration parameters, finds the feature files, applies the tag filter, expands outlines into one scenario per row, and creates fresh step objects through PicoContainer. For each scenario it runs the `@Before` hooks, then the Background steps, then the scenario steps, then the `@After` hooks, and reports results to the platform. Finally, Surefire writes its reports, the plug-ins write the Cucumber reports, and Maven prints BUILD SUCCESS or FAILURE.
</details>

---
