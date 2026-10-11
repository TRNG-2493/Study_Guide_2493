# Weekly Knowledge Check: [Week5-Advanced-Web-Automation] - Tuesday: Playwright Advanced Interactions

**Topics covered:** Frames and nested frames, Web tables, Date pickers, Multiple tabs and windows, Shadow DOM, Dynamic element handling, Navigation events, File upload and download.

**How to use this quiz:** Answer each question first, then click the solution to check your reasoning and read why the other options are wrong. All code uses the Python sync API of Playwright. Where a snippet mentions `BASE`, it is the address of a small local test server like the one used in the lessons.

---

## Part 1: Multiple Choice

### 1. A "Pay now" button is clearly visible on screen, but `page.get_by_role("button", name="Pay now").click()` fails with `Timeout 30000ms exceeded ... waiting for get_by_role(...)`. What is the most likely cause?
- [ ] A) The button's accessible name contains a space, so `get_by_role` cannot match it.
- [ ] B) Playwright requires a `time.sleep()` before it can interact with embedded content.
- [ ] C) The button is inside an `<iframe>`, and locators created from `page` only search the main frame's document.
- [ ] D) `click()` is not supported inside iframes, so `evaluate` must be used instead.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The button is inside an `<iframe>`, and locators created from `page` only search the main frame's document.

**Explanation:** An iframe is a separate document, and from the main frame's point of view it is a single opaque element, so the lesson's "visible on screen but times out" symptom is the classic sign of a missed frame. The fix is `page.frame_locator("...").get_by_role("button", name="Pay now").click()`.
- **Why others are wrong:**
  - A) Accessible names with spaces match normally; the lesson's own example uses `name="Pay now"` successfully inside a frame.
  - B) Playwright auto-waits; sleeping cannot make a main-frame locator see into another document.
  - D) `click()` works fine inside frames when called on a locator obtained via `frame_locator()`; `evaluate` skips actionability checks and is not needed.
</details>

---

### 2. An `<iframe id="outer">` contains a second `<iframe id="inner">`, and `inner` contains `<button id="deep">`. Which locator reaches the button?
- [ ] A) `page.frame_locator("#inner").locator("#deep")`
- [ ] B) `page.locator("#outer #inner #deep")`
- [ ] C) `page.frame_locator("#outer, #inner").locator("#deep")`
- [ ] D) `page.frame_locator("#outer").frame_locator("#inner").locator("#deep")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `page.frame_locator("#outer").frame_locator("#inner").locator("#deep")`

**Explanation:** Chained `frame_locator()` calls read left to right as "go into `#outer`, then go into `#inner`, then find `#deep`". Each call searches inside the document produced by the previous one.
- **Why others are wrong:**
  - A) `#inner` does not exist in the main document (it lives inside `#outer`), so this resolves to nothing.
  - B) A CSS descendant combinator does not cross from one document into another; the main document only contains the `#outer` iframe element, not its contents.
  - C) A selector list matches only elements in the main document, so it can only select `#outer`; the locator then looks for `#deep` one document too shallow.
</details>

---

### 3. Why does the lesson recommend `page.frame_locator()` over `page.frame(name=...)` as the default tool?
- [ ] A) A FrameLocator is lazy: it re-resolves the iframe on each use and auto-waits for it, whereas `page.frame()` is evaluated immediately and returns `None` if the frame is not attached yet.
- [ ] B) `page.frame()` cannot enter cross-origin frames, but `frame_locator()` can.
- [ ] C) `page.frame()` has been removed from current Playwright versions.
- [ ] D) `frame_locator()` returns a `Frame` object with `.url`, whereas `page.frame()` returns a `Locator`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A FrameLocator is lazy: it re-resolves the iframe on each use and auto-waits for it, whereas `page.frame()` is evaluated immediately and returns `None` if the frame is not attached yet.

**Explanation:** Laziness and auto-waiting make `frame_locator()` safe for frames that load late or get re-created, while a `Frame` object is a snapshot that can be `None` or go stale. `page.frame()` is still useful for framesets and for reading `frame.url` or `child_frames`.
- **Why others are wrong:**
  - B) Playwright controls the browser from outside, so it is not subject to the same-origin policy; both APIs work across origins.
  - C) `page.frame()` still exists and is used in the lesson (for example with `the-internet.herokuapp.com/nested_frames`).
  - D) The types are the other way round: `page.frame()` returns a `Frame` (with `.url`, `.name`, `.child_frames`), and `frame_locator()` returns a `FrameLocator`.
</details>

---

### 4. A users table has the rows "Maria Lopez", "Ann Brown", and "Joanna Green", and users can re-sort it. Which locator reliably targets only the "Ann Brown" row?
- [ ] A) `page.get_by_role("row").filter(has_text="Ann")`
- [ ] B) `page.get_by_role("row").filter(has_text="ann")`
- [ ] C) `page.locator("tbody tr").nth(1)`
- [ ] D) `page.get_by_role("row").filter(has=page.get_by_role("cell", name="Ann Brown", exact=True))`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `page.get_by_role("row").filter(has=page.get_by_role("cell", name="Ann Brown", exact=True))`

**Explanation:** Requiring a cell whose accessible name is exactly "Ann Brown" locates by content and relationship, so it is unaffected by sorting and cannot match "Joanna Green". Running this kind of filter on the sample table gives 1 match, versus 2 for the loose substring version.
- **Why others are wrong:**
  - A) `has_text` is a substring match, and "Joanna" contains "Ann", so two rows match and a click inside would raise a strict mode violation.
  - B) `has_text` is already case-insensitive, so lower-casing changes nothing; "Joanna" still matches.
  - C) A positional locator happens to be correct only for the current order and breaks as soon as the table is sorted or a row is inserted.
</details>

---

### 5. Right after clicking "Load report", `page.locator("tbody tr").count()` returns `0` because the table is filled by an API call. What is the correct way to make sure the data has arrived before reading it?
- [ ] A) Call `count()` again; it waits until at least one row exists.
- [ ] B) Call `page.wait_for_timeout(2000)` and then read the rows.
- [ ] C) Use `expect(page.locator("tbody tr")).to_have_count(10)` and then read the rows.
- [ ] D) Call `all_inner_texts()`; it waits until the list is non-empty.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Use `expect(page.locator("tbody tr")).to_have_count(10)` and then read the rows.

**Explanation:** `expect(...).to_have_count(n)` is a web-first assertion that retries until the table has exactly `n` rows, so it acts as a "table has finished loading" gate before you read data.
- **Why others are wrong:**
  - A) `count()` is an instant snapshot and never waits.
  - B) A fixed sleep is too slow when the data is ready early and still flaky when the machine is slow.
  - D) `all_inner_texts()` also snapshots whatever exists at that moment and happily returns `[]`.
</details>

---

### 6. Which statement about `td:nth-child(1)` and `locator.nth(1)` is correct?
- [ ] A) Both are 0-based, so `td:nth-child(1)` selects the second column and `.nth(1)` selects the second match.
- [ ] B) `td:nth-child(1)` is a 1-based CSS pseudo-class that selects the first column, while `.nth(1)` is 0-based and selects the second match.
- [ ] C) Both are 1-based, so `.nth(1)` selects the first match.
- [ ] D) `td:nth-child(1)` is 0-based and `.nth(1)` is 1-based.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `td:nth-child(1)` is a 1-based CSS pseudo-class that selects the first column, while `.nth(1)` is 0-based and selects the second match.

**Explanation:** CSS counts from 1, Playwright's `nth()` counts from 0. This is why the lesson's helper uses `headers.index(header) + 1` when building an `nth-child` selector from a Python index.
- **Why others are wrong:**
  - A) CSS `nth-child` is not 0-based.
  - C) Playwright's `nth()` is 0-based; `.nth(0)` is the first match.
  - D) This reverses the two conventions.
</details>

---

### 7. Which call correctly sets `<input type="date" id="dob">` to 21 July 1995?
- [ ] A) `page.locator("#dob").fill("07/21/1995")`
- [ ] B) Click the field, then click "21" in the browser's native calendar popup.
- [ ] C) `page.locator("#dob").fill("21-07-1995")`
- [ ] D) `page.locator("#dob").fill("1995-07-21")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `page.locator("#dob").fill("1995-07-21")`

**Explanation:** A native date input's value is always ISO `YYYY-MM-DD`, regardless of how the browser displays it for the user's locale. `fill()` sets that value and fires the `input` and `change` events.
- **Why others are wrong:**
  - A) The US display format is not the value format; Playwright raises `Malformed value`.
  - B) The native calendar popup is drawn by the browser and is not part of the page DOM, so Playwright cannot click it.
  - C) Day-first order is also not the ISO value format and is rejected as `Malformed value`.
</details>

---

### 8. A booking page highlights "today" using JavaScript's `new Date()`. Which option makes the page's idea of "today" a constant on every run?
- [ ] A) `context.set_default_timeout(0)`
- [ ] B) `browser.new_context(locale="en-GB")`
- [ ] C) `page.clock.set_fixed_time(datetime(2025, 3, 14, 10, 0))` before the page's scripts read the time
- [ ] D) `browser.new_context(timezone_id="UTC")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `page.clock.set_fixed_time(datetime(2025, 3, 14, 10, 0))` before the page's scripts read the time

**Explanation:** `page.clock.set_fixed_time()` makes `Date.now()` and `new Date()` return a constant moment. It must be called before `goto` or `set_content` so the page scripts see it, and it affects only the browser, not server-side date logic.
- **Why others are wrong:**
  - A) That setting only changes how long Playwright waits; it has nothing to do with the page's clock.
  - B) `locale` changes how dates are formatted and displayed, not which instant the clock reports.
  - D) `timezone_id` pins the time zone, which is good practice, but time still advances with the real clock, so "today" would change from day to day.
</details>

---

### 9. A custom calendar currently shows "January 2025". The target date is 5 December 2024. What does `(target.year - shown.year) * 12 + (target.month - shown.month)` return, and what should the helper do?
- [ ] A) `-1`; click "Previous month" once.
- [ ] B) `1`; click "Next month" once.
- [ ] C) `11`; click "Next month" 11 times.
- [ ] D) `-13`; click "Previous month" 13 times.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `-1`; click "Previous month" once.

**Explanation:** `(2024 - 2025) * 12 + (12 - 1) = -12 + 11 = -1`. A negative result means the target is earlier, so the helper clicks "Previous month" `abs(diff)` times.
- **Why others are wrong:**
  - B) The sign is wrong; a positive result would mean the target is in the future.
  - C) `11` is what you get if you compare only the month numbers and forget the year difference.
  - D) `-13` would mean 13 months back; December 2024 is only one month before January 2025.
</details>

---

### 10. Clicking a link with `target="_blank"` opens a new tab. Which code captures the new tab reliably?
- [ ] A) Click the link, then call `page.expect_popup()` to retrieve the tab.
- [ ] B) Click the link, then immediately read `context.pages[-1]`.
- [ ] C) Click the link, `time.sleep(2)`, then `page.switch_to.window(...)`.
- [ ] D) `with page.expect_popup() as info:` click the link, then `popup = info.value`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `with page.expect_popup() as info:` click the link, then `popup = info.value`.

**Explanation:** The "register first, then act" pattern starts listening before the click, so the popup event cannot be missed. After the `with` block, `info.value` is the new `Page`.
- **Why others are wrong:**
  - A) Starting to listen after the click risks missing the event, which may already have fired.
  - B) The tab opens asynchronously, so the new page may not exist yet when the list is read; `context.pages` is also only a snapshot.
  - C) Playwright has no `switch_to.window` and no "current window" pointer, and a fixed sleep is both slow and unreliable.
</details>

---

### 11. A chat-app test needs two independently logged-in users (Alice and Bob) at the same time. What is the right setup?
- [ ] A) Two tabs created with `context.new_page()` in the same browser context.
- [ ] B) Two browser contexts from `browser.new_context()`, each with its own page.
- [ ] C) One page that logs out and logs in between each step.
- [ ] D) Two tabs in one context, switching with `bring_to_front()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Two browser contexts from `browser.new_context()`, each with its own page.

**Explanation:** Each context has its own cookies and storage, so Alice and Bob are truly separate sessions. Pages in the same context share cookies, like tabs in a normal browser profile.
- **Why others are wrong:**
  - A) Tabs in one context share cookies and storage, so both would be the same user.
  - C) That serialises the two users and cannot test live interaction between them.
  - D) `bring_to_front()` only activates a tab; it does not change which session the tab belongs to.
</details>

---

### 12. You wrap `page.expect_popup(timeout=2000)` around a click on `<a href="/about">About</a>` (no `target` attribute). What happens?
- [ ] A) It returns the same `Page` that was clicked.
- [ ] B) It returns a new blank `Page`.
- [ ] C) It times out, because no popup is ever created; the correct tools are `page.wait_for_url()` or `expect(page).to_have_url(...)`.
- [ ] D) It raises an error immediately saying the link is not a popup link.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It times out, because no popup is ever created; the correct tools are `page.wait_for_url()` or `expect(page).to_have_url(...)`.

**Explanation:** A plain link navigates in place, so there is no popup event for `expect_popup` to capture. Playwright simply waits until the timeout expires.
- **Why others are wrong:**
  - A) `expect_popup` only ever resolves with a newly opened page.
  - B) Nothing opens a blank page, so there is nothing to return.
  - D) Playwright does not inspect the link; it just waits for an event that never arrives.
</details>

---

### 13. A `<user-card>` component has an open shadow root containing a `<button>`. Which locator does NOT see that button?
- [ ] A) `page.get_by_role("button", name="Follow")`
- [ ] B) `page.locator("css=button")`
- [ ] C) `page.locator("xpath=//button")`
- [ ] D) `page.get_by_text("Follow")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `page.locator("xpath=//button")`

**Explanation:** Playwright's CSS, text, role, label, and test-id engines pierce open shadow roots, but XPath works on the light DOM only. Running the three variants on a shadow-based page gives CSS = found, XPath = 0 matches.
- **Why others are wrong:**
  - A) Role locators use the flattened accessibility tree and pierce open roots.
  - B) The CSS engine deliberately crosses open shadow boundaries, unlike the browser's own `querySelector`.
  - D) Text locators also pierce open shadow roots.
</details>

---

### 14. A third-party widget uses a CLOSED shadow root, and its button cannot be reached with any locator. What does the lesson recommend as the first approach?
- [ ] A) Switch to XPath selectors.
- [ ] B) Use the `css:light=` prefix.
- [ ] C) Wrap the call in `page.frame_locator()`.
- [ ] D) Ask developers for a stable test interface (for example a `data-testid` on the host, ARIA attributes, or a public method) and test through the host's observable behaviour; patching `attachShadow` with an init script is a last resort.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Ask developers for a stable test interface (for example a `data-testid` on the host, ARIA attributes, or a public method) and test through the host's observable behaviour; patching `attachShadow` with an init script is a last resort.

**Explanation:** For a closed root, `host.shadowRoot` is `null` and locators cannot go inside. Negotiating a testable surface keeps the test faithful to production, whereas the init-script patch changes the component's mode and should be used sparingly.
- **Why others are wrong:**
  - A) XPath never pierces shadow roots, open or closed.
  - B) `css:light` is a way to opt out of piercing, so it can only see less, not more.
  - C) `frame_locator()` is for iframes; a shadow root is not an iframe.
</details>

---

### 15. `page.evaluate("document.querySelector('button.follow')")` returns `None`, yet `page.locator("button.follow").count()` returns `2` on the same page. Why?
- [ ] A) The browser's own `querySelector` does not cross shadow boundaries, but Playwright's CSS engine pierces open shadow roots.
- [ ] B) `evaluate` runs before the page has loaded, so nothing exists yet.
- [ ] C) `count()` waits for elements, while `evaluate` does not.
- [ ] D) The buttons are hidden, and `querySelector` skips hidden elements.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The browser's own `querySelector` does not cross shadow boundaries, but Playwright's CSS engine pierces open shadow roots.

**Explanation:** Shadow DOM is a query boundary inside one document. To reach shadow content with raw JavaScript you must walk `host.shadowRoot` yourself, while Playwright locators do it for you.
- **Why others are wrong:**
  - B) The page is fully loaded; the same `evaluate` for the host element would succeed.
  - C) `count()` does not wait either; it is an instant snapshot.
  - D) `querySelector` does not filter by visibility; the buttons are visible and simply live behind the shadow boundary.
</details>

---

### 16. A toast with `role="status"` appears about 300 ms after clicking Save and shows "Saved". Which line keeps retrying until the toast text is correct (up to the default timeout)?
- [ ] A) `assert page.get_by_role("status").inner_text() == "Saved"`
- [ ] B) `assert page.get_by_role("status").is_visible()`
- [ ] C) `expect(page.get_by_role("status")).to_have_text("Saved")`
- [ ] D) `assert page.get_by_role("status").count() == 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `expect(page.get_by_role("status")).to_have_text("Saved")`

**Explanation:** `expect(...)` assertions are web-first: they poll until the condition holds or the assertion timeout (5 s by default) expires. Plain Python `assert` on a value reads it once.
- **Why others are wrong:**
  - A) `inner_text()` reads the text one time; if the element exists but still shows older text, the comparison fails without retrying.
  - B) `is_visible()` returns immediately and does not wait; it would be `False` in the first 300 ms.
  - D) `count()` is an instant snapshot as well, and it checks existence rather than text.
</details>

---

### 17. In Selenium a "found element" can become stale after a framework re-renders the page. Why does a Playwright `Locator` not suffer from this?
- [ ] A) Playwright caches nodes and refreshes them every 30 seconds.
- [ ] B) Playwright disables re-rendering while a test runs.
- [ ] C) Playwright keeps a background poll that patches references.
- [ ] D) A Locator is a recipe for finding the element, re-run at the moment of each action or assertion, rather than a reference to one DOM node.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A Locator is a recipe for finding the element, re-run at the moment of each action or assertion, rather than a reference to one DOM node.

**Explanation:** If the DOM is re-rendered between two lines, the next use of the locator simply finds the new node. `ElementHandle` objects (from `query_selector`) are real references and do go stale, which is why Locators are preferred.
- **Why others are wrong:**
  - A) There is no timed node cache.
  - B) Playwright never interferes with the application's rendering.
  - C) No background patching exists; the lookup just happens lazily at use time.
</details>

---

### 18. A button's id is regenerated on every build (`btn-8f3a2`, `btn-1c9d7`, ...) and its visible label is "Generated". Which locator is the most stable choice?
- [ ] A) `page.locator("#btn-8f3a2")`
- [ ] B) `page.get_by_role("button", name="Generated")`
- [ ] C) `page.locator("div > div:nth-child(3) > button")`
- [ ] D) `page.locator("button").first`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `page.get_by_role("button", name="Generated")`

**Explanation:** Role plus accessible name reflects what the user sees and survives id and class changes. If no good user-facing option exists, a prefix selector such as `[id^='btn-']` is the lesson's fallback for generated ids.
- **Why others are wrong:**
  - A) The hard-coded id changes on every build, so the test breaks after the next deploy.
  - C) A deep structural path breaks with any layout change and communicates nothing.
  - D) Positional locators are a last resort; the first button on the page may not be the one you want.
</details>

---

### 19. What does `response = page.goto("/missing")` do when the server answers with HTTP 404?
- [ ] A) It raises a `playwright.sync_api.Error`.
- [ ] B) It returns `None`.
- [ ] C) It retries until the server returns 200 or the timeout expires.
- [ ] D) It returns a `Response` whose `status` is 404 and `ok` is `False`; no exception is raised.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It returns a `Response` whose `status` is 404 and `ok` is `False`; no exception is raised.

**Explanation:** The navigation technically succeeded in loading a page, so `goto` only raises for network-level problems such as DNS failure, refused connections, certificate errors, or timeouts. Check `response.status` and the page content yourself.
- **Why others are wrong:**
  - A) Errors are reserved for failures like `net::ERR_NAME_NOT_RESOLVED`, not HTTP error statuses.
  - B) `None` is returned only when there is no network response, for example `about:blank` or hash-only changes.
  - C) Playwright does not retry navigations on HTTP errors.
</details>

---

### 20. In a single-page app, clicking "Orders" calls `history.pushState` and the content updates a moment later. Which approach is the most reliable way to wait?
- [ ] A) `page.wait_for_load_state("load")` and nothing else.
- [ ] B) `page.wait_for_load_state("networkidle")`.
- [ ] C) `page.wait_for_url("**/orders")` followed by an assertion on the rendered content.
- [ ] D) `with page.expect_navigation():` as the recommended modern approach for any URL change.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `page.wait_for_url("**/orders")` followed by an assertion on the rendered content.

**Explanation:** `wait_for_url` recognises History API changes, and the content assertion confirms the view has actually rendered, which matters because the URL changes before the data arrives.
- **Why others are wrong:**
  - A) No new document loads in an SPA, so the `load` event does not fire again and `wait_for_load_state()` returns immediately without proving anything.
  - B) `networkidle` is discouraged: it can be slow or never reached on pages with polling or analytics, and it is not a signal that your view is ready.
  - D) `expect_navigation` is legacy and racy; for same-document changes it may hang until timeout.
</details>

---

### 21. Which `wait_until` value does the lesson discourage, and why?
- [ ] A) `"load"`, because it fires before the HTML is parsed.
- [ ] B) `"networkidle"`, because pages with analytics, polling, or websockets may never become network-idle.
- [ ] C) `"domcontentloaded"`, because it always waits for images.
- [ ] D) `"commit"`, because it always waits the full 30 seconds.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `"networkidle"`, because pages with analytics, polling, or websockets may never become network-idle.

**Explanation:** `networkidle` means no network connections for 500 ms, which many modern sites never reach. Waiting for the specific element or content you need is the recommended alternative.
- **Why others are wrong:**
  - A) `load` is the default and fires after the page and its resources have loaded, which is after parsing.
  - C) `domcontentloaded` fires when the HTML is parsed, without waiting for images or stylesheets.
  - D) `commit` is the earliest stage (the response has started arriving) and returns quickly.
</details>

---

### 22. An upload widget has a real `<input type="file">` in the DOM that is hidden with `display: none`. What is the simplest correct way to upload a file?
- [ ] A) `page.locator("input[type=file]").set_input_files("data/resume.pdf")`
- [ ] B) Force-click the input and type the path into the operating system dialog.
- [ ] C) Make the input visible with `evaluate`, then call `fill()` with the path.
- [ ] D) `page.keyboard.type("data/resume.pdf")` while the dialog is open.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `page.locator("input[type=file]").set_input_files("data/resume.pdf")`

**Explanation:** `set_input_files` assigns the file directly to the input and dispatches `input` and `change` events. It does not click, so it works even when the input is hidden.
- **Why others are wrong:**
  - B) Playwright never needs, and cannot drive, the native OS file dialog.
  - C) No workaround is needed for visibility, and `fill()` does not work on file inputs.
  - D) The keyboard cannot reach the OS dialog, and typing into it would be fragile even if it could.
</details>

---

### 23. A "Choose avatar" button creates an `<input type="file">` in JavaScript only when clicked. Which technique handles this?
- [ ] A) Call `page.locator("input[type=file]").set_input_files(...)` before clicking the button.
- [ ] B) Call `page.keyboard.type("avatar.png")` after clicking.
- [ ] C) Call `page.set_input_files("button", "avatar.png")` on the button element.
- [ ] D) `with page.expect_file_chooser() as fc:` click the button, then `fc.value.set_files("avatar.png")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `with page.expect_file_chooser() as fc:` click the button, then `fc.value.set_files("avatar.png")`.

**Explanation:** When the input does not exist until the click, you listen for the file chooser event (register first, then act) and then set the files on the `FileChooser`. Playwright suppresses the native dialog.
- **Why others are wrong:**
  - A) The input does not exist in the DOM before the click, so the locator finds nothing.
  - B) Keystrokes cannot be sent to the native dialog.
  - C) `set_input_files` needs an `<input type="file">` (or its label), not a button.
</details>

---

### 24. The server sends `Content-Disposition: attachment; filename="orders.csv"` for the link `/export.csv`. What is `download.suggested_filename`?
- [ ] A) `export.csv`
- [ ] B) `None` until `save_as()` is called
- [ ] C) `orders.csv`
- [ ] D) The full URL of the link

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `orders.csv`

**Explanation:** `suggested_filename` comes from the `Content-Disposition` header (or the `download` attribute), not from the URL path. The URL is available separately as `download.url`, which would end in `/export.csv`.
- **Why others are wrong:**
  - A) That is the last segment of the URL, which is not what the browser uses when a header supplies a filename.
  - B) The property is available as soon as the download starts; `save_as()` is only needed to copy the file.
  - D) The URL is exposed through `download.url`, not through `suggested_filename`.
</details>

---

## Part 2: True or False (Common Misconceptions)

### 25. True or False: Just like Selenium's `switch_to.frame()`, Playwright keeps a "current frame" that you must switch into before using locators inside an iframe, and switch back out of afterwards.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Playwright has no "current frame" state. Every locator is explicit about where it searches: use `page` for the main document and a `FrameLocator` for the iframe, and the two can be mixed freely in one test with nothing to switch back from.
</details>

---

### 26. True or False: `page.frame_locator()` works on cross-origin iframes (for example a payment form served from another domain) in the same way as on same-origin iframes.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The same-origin policy restricts JavaScript running inside web pages, but Playwright drives the browser from the outside through its automation protocol. The practical limit is that third-party frames (CAPTCHAs, 3-D Secure pages) may deliberately block automation, so use a test mode for them.
</details>

---

### 27. True or False: For a table with one header row and four data rows, `page.get_by_role("row").count()` returns `4`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `get_by_role("row")` matches every `<tr>`, including the header row, so it returns `5`. To count only data rows use `table.locator("tbody tr")` (or subtract the header deliberately and comment why).
</details>

---

### 28. True or False: For `<input type="date">`, the value Playwright sets and reads is always in `YYYY-MM-DD` format, even if the browser displays the field as `dd/mm/yyyy` for an `en-GB` locale.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The display format depends on the user's locale, but the underlying value is always ISO-like. This is why `fill("2025-03-14")` and `to_have_value("2025-03-14")` work regardless of the `locale` you emulate.
</details>

---

### 29. True or False: Two tabs created in the same browser context are isolated from each other, so a cookie set in one tab is not visible in the other.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** All pages in one `BrowserContext` share cookies and storage, exactly like tabs in one browser profile. Isolation exists between contexts, which is why separate contexts are used to simulate separate users.
</details>

---

### 30. True or False: Because Playwright has no "switch to window" command, after a popup opens you can keep using both the original `page` and the popup `Page` object, in any order.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Each `Page` object is an independent handle, so there is no pointer that can be left on the wrong window. The lesson's analogy is "two remote controls, two TVs".
</details>

---

### 31. True or False: Shadow DOM and iframes are the same kind of boundary, so elements inside an open shadow root also require `frame_locator()`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** An iframe is a separate document with its own `window`, whereas shadow DOM hides part of the same document's tree. Playwright's ordinary locators pierce open shadow roots automatically, while iframes need `frame_locator()`. The two can be combined, for example `frame_locator(...).locator("user-card button")`.
</details>

---

### 32. True or False: `page.locator("xpath=//button")` does not find buttons that live inside an open shadow root.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** XPath works on the light DOM only and does not pierce shadow roots, which is one more reason to prefer role, text, label, test-id, or CSS locators on component-based sites.
</details>

---

### 33. True or False: `page.get_by_text("Done").is_visible()` waits up to the default timeout for the text to become visible before returning.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `is_visible()` is an instant snapshot and returns `True` or `False` immediately. To wait, use `expect(...).to_be_visible()` or `locator.wait_for()`. The same is true of `count()` and `is_checked()`.
</details>

---

### 34. True or False: `page.goto()` does not raise an exception when the server responds with 404 or 500; you must check `response.status` or `response.ok` yourself.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** A 404 or 500 page still loads, so the navigation counts as successful. `goto` raises only for network-level failures (DNS, refused connection, certificate errors) and timeouts.
</details>

---

### 35. True or False: After a `history.pushState` route change in a single-page app, `page.wait_for_load_state()` returns immediately because no new `load` event fires.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Same-document navigations keep the document alive, so the page is already in the `load` state. Use `wait_for_url()` and a content assertion instead; waiting for a load state proves nothing in an SPA.
</details>

---

### 36. True or False: If an input has `accept=".pdf"`, `set_input_files` will refuse to attach a `.exe` file, so you do not need to test server-side file-type validation.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `accept` is only a UI hint; `set_input_files` can attach any file, just as a malicious client could. If the server accepts a disallowed file, that is a real defect, so negative tests with violating files are worthwhile.
</details>

---

## Part 3: Code Prediction

### 37. What does this code print?
```python
page.set_content("""
<iframe id="pay" srcdoc="<button>Pay now</button>"></iframe>
""")
main_count = page.get_by_role("button", name="Pay now").count()
frame_count = page.frame_locator("#pay").get_by_role("button", name="Pay now").count()
print(main_count, frame_count)
```
- [ ] A) `1 1`
- [ ] B) `0 0`
- [ ] C) `0 1`
- [ ] D) A `TimeoutError` is raised on the first `count()` line.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `0 1`

**Explanation:** A main-page locator cannot see into the iframe, so the first count is `0`, while the FrameLocator resolves the iframe and finds the one button. `count()` never waits, so it returns `0` instead of timing out.
- **Why others are wrong:**
  - A) The main frame does not see the button inside the iframe.
  - B) The frame locator does find the button, so its count is 1.
  - D) `count()` returns an instant number and does not raise a timeout; only actions and assertions wait.
</details>

---

### 38. What does this code print (three lines)?
```python
page.set_content("""
<iframe name="left"  srcdoc="<p id='who'>LEFT</p>"></iframe>
<iframe name="right" srcdoc="<p id='who'>RIGHT</p>"></iframe>
""")
print(len(page.frames))
print(page.frame(name="right").locator("#who").inner_text())
print(page.frame(name="nope"))
```
- [ ] A) `2`, `RIGHT`, `None`
- [ ] B) `3`, `RIGHT`, a `TimeoutError` because the frame never appears
- [ ] C) `3`, `LEFT`, `None`
- [ ] D) `3`, `RIGHT`, `None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `3`, `RIGHT`, `None`

**Explanation:** `page.frames` includes the main frame plus both iframes, so there are 3. `page.frame(name="right")` matches the `name` attribute, and the duplicate id `who` is not a problem because each frame is its own document. `page.frame()` is evaluated immediately and returns `None` when no frame matches.
- **Why others are wrong:**
  - A) That forgets the main frame, which is counted in `page.frames`.
  - B) `page.frame()` does not wait or raise; it returns `None` right away.
  - C) The `name="right"` frame contains "RIGHT", not "LEFT".
</details>

---

### 39. Two iframes both contain `<p id="who">`. What does this code print?
```python
page.set_content("""
<iframe name="left"  srcdoc="<p id='who'>LEFT</p>"></iframe>
<iframe name="right" srcdoc="<p id='who'>RIGHT</p>"></iframe>
""")
fl = page.frame_locator("iframe")
try:
    fl.locator("#who").inner_text(timeout=2000)
    print("ok")
except Exception as e:
    print("strict" if "strict mode violation" in str(e) else "other")
print(fl.last.locator("#who").inner_text())
```
- [ ] A) `strict` then `RIGHT`
- [ ] B) `ok` then `LEFT`
- [ ] C) `other` then `RIGHT`
- [ ] D) `strict` then `LEFT`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `strict` then `RIGHT`

**Explanation:** `frame_locator("iframe")` matches both iframes, so performing an action through it raises a strict mode violation. Choosing explicitly with `.last` (or `.first` / `.nth(n)`) picks the second iframe, whose paragraph says RIGHT.
- **Why others are wrong:**
  - B) The first call does not succeed, and `.last` is the second iframe, not the first.
  - C) The error message is specifically a strict mode violation, not some other error.
  - D) `.last` selects the last iframe (RIGHT); `.first` would give LEFT.
</details>

---

### 40. Given this table, what does the code print?
```python
page.set_content("""
<table><tbody>
  <tr><td>Maria Lopez</td><td>Admin</td></tr>
  <tr><td>Ann Brown</td><td>Editor</td></tr>
  <tr><td>Joanna Green</td><td>Viewer</td></tr>
</tbody></table>
""")
loose = page.get_by_role("row").filter(has_text="Ann")
exact = page.get_by_role("row").filter(
    has=page.get_by_role("cell", name="Ann Brown", exact=True))
print(loose.count(), exact.count())
```
- [ ] A) `1 1`
- [ ] B) `2 2`
- [ ] C) `2 1`
- [ ] D) `1 2`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `2 1`

**Explanation:** `has_text="Ann"` is a substring match, so it matches "Ann Brown" and "Joanna Green" (J-o-**ann**-a). The `has=` filter with an exact cell name matches only the row containing a cell named exactly "Ann Brown".
- **Why others are wrong:**
  - A) The loose filter matches two rows, not one.
  - B) The exact cell match does not match "Joanna Green".
  - D) The counts are reversed: the substring filter is the broad one.
</details>

---

### 41. What does this code print (two lines)? It mirrors checking a UI sort order in Python.
```python
names = ["alice", "Zed", "bob"]
print(sorted(names))
print(sorted(names, key=str.lower))
```
- [ ] A) `['alice', 'bob', 'Zed']` then `['alice', 'bob', 'Zed']`
- [ ] B) `['alice', 'Zed', 'bob']` then `['alice', 'bob', 'Zed']`
- [ ] C) `['Zed', 'alice', 'bob']` then `['Zed', 'alice', 'bob']`
- [ ] D) `['Zed', 'alice', 'bob']` then `['alice', 'bob', 'Zed']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `['Zed', 'alice', 'bob']` then `['alice', 'bob', 'Zed']`

**Explanation:** Python sorts strings by Unicode code point, so uppercase "Z" comes before lowercase "a". With `key=str.lower` the comparison is case-insensitive. A UI that sorts case-insensitively would fail an assertion built on plain `sorted()`, so compare using the same rule as the UI.
- **Why others are wrong:**
  - A) Plain `sorted()` is case-sensitive, so the first line is not alphabetical-ignoring-case.
  - B) Neither call produces this order: the code-point sort puts `Zed` first, and the case-insensitive sort puts `Zed` last.
  - C) The second call uses `key=str.lower`, which changes the order.
</details>

---

### 42. A test fixes the browser clock before loading the page. What does `#out` contain? (14 March 2025 was a Friday; JavaScript's `getDay()` returns 0 for Sunday.)
```python
context = browser.new_context(timezone_id="UTC", locale="en-US")
page = context.new_page()
page.clock.set_fixed_time(datetime(2025, 3, 14, 10, 0, 0))
page.set_content("""
<p id="out"></p>
<script>
  const d = new Date();
  document.getElementById('out').textContent =
    d.toISOString().slice(0, 10) + ' ' + d.getDay();
</script>
""")
print(page.locator("#out").inner_text())
```
- [ ] A) `2025-03-14 4`
- [ ] B) `2025-03-14 5`
- [ ] C) The real current date, because the fixed time only affects timers
- [ ] D) `2025-03-13 5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `2025-03-14 5`

**Explanation:** `set_fixed_time` makes `new Date()` return the chosen moment for scripts that run afterwards. With the time zone pinned to UTC, the date is 2025-03-14, and Friday is day 5 when Sunday is 0.
- **Why others are wrong:**
  - A) That would be Thursday; Friday is 5.
  - C) `set_fixed_time` freezes `Date.now()` and `new Date()`, not just timers (timers keep running normally).
  - D) 10:00 UTC on the 14th is still the 14th in UTC, so the date does not shift to the 13th.
</details>

---

### 43. A calendar helper starts from "January 2025". What does this print?
```python
from datetime import datetime, date

shown = datetime.strptime("January 2025", "%B %Y")
target = date(2028, 2, 29)
print((target.year - shown.year) * 12 + (target.month - shown.month))
```
- [ ] A) `36`
- [ ] B) `38`
- [ ] C) `37`
- [ ] D) `1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `37`

**Explanation:** `(2028 - 2025) * 12 + (2 - 1) = 36 + 1 = 37`, so the helper clicks "Next month" 37 times (this is the lesson's own leap-day example).
- **Why others are wrong:**
  - A) `36` forgets the extra month between January and February.
  - B) `38` over-counts by one.
  - D) `1` ignores the three-year gap and uses only the month numbers.
</details>

---

### 44. A page at `BASE + "/"` contains `<a target="_blank" href="/terms">Terms</a>`. What does this print (two lines)?
```python
context = browser.new_context()
page = context.new_page()
page.goto(BASE + "/")
with page.expect_popup() as info:
    page.get_by_role("link", name="Terms").click()
popup = info.value
print(len(context.pages))
popup.close()
print(len(context.pages), popup.is_closed())
```
- [ ] A) `1` then `1 True`
- [ ] B) `2` then `2 False`
- [ ] C) `2` then `1 False`
- [ ] D) `2` then `1 True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `2` then `1 True`

**Explanation:** The original tab plus the popup make two pages in the context. Closing the popup leaves one page, and `is_closed()` reports `True` for the closed one.
- **Why others are wrong:**
  - A) The popup is a separate page, so the first count is 2.
  - B) After `popup.close()` the popup is removed from `context.pages` and is marked closed.
  - C) `is_closed()` is `True` after `close()`.
</details>

---

### 45. Two tabs share one context, and a third tab belongs to a second context. What does this print?
```python
ctx_a, ctx_b = browser.new_context(), browser.new_context()
t1 = ctx_a.new_page(); t2 = ctx_a.new_page(); t3 = ctx_b.new_page()
for t in (t1, t2, t3):
    t.goto(BASE + "/about")
t1.evaluate("document.cookie = 'theme=dark; path=/'")
print(repr(t2.evaluate("document.cookie")), repr(t3.evaluate("document.cookie")))
```
- [ ] A) `'theme=dark' ''`
- [ ] B) `'' ''`
- [ ] C) `'theme=dark' 'theme=dark'`
- [ ] D) `'' 'theme=dark'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `'theme=dark' ''`

**Explanation:** `t2` is in the same context as `t1`, so it shares the cookie. `t3` is in another context, which is isolated and starts with no cookies.
- **Why others are wrong:**
  - B) Tabs in the same context do share cookies, so `t2` sees the cookie.
  - C) Separate contexts never share cookies, so `t3` stays empty.
  - D) This reverses the sharing rule.
</details>

---

### 46. Two `<user-card>` components each render `<h2>` and a button inside an open shadow root. What does this print?
```python
page.set_content("""
<user-card name="Maria"></user-card>
<user-card name="John"></user-card>
<script>
  class UserCard extends HTMLElement {
    connectedCallback() {
      this.attachShadow({ mode: 'open' }).innerHTML =
        `<h2>${this.getAttribute('name')}</h2><button>Follow</button>`;
    }
  }
  customElements.define('user-card', UserCard);
</script>
""")
print(page.evaluate("document.querySelectorAll('h2').length"),
      page.locator("h2").count(),
      page.locator("xpath=//h2").count(),
      page.locator("css:light=h2").count())
```
- [ ] A) `2 2 2 2`
- [ ] B) `0 2 2 0`
- [ ] C) `0 2 0 0`
- [ ] D) `0 0 0 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `0 2 0 0`

**Explanation:** The browser's `querySelectorAll`, XPath, and `css:light` all stop at the shadow boundary (0 each). Only Playwright's default CSS engine pierces the open roots and finds both headings.
- **Why others are wrong:**
  - A) That would mean every engine pierces the shadow roots, which is not the case.
  - B) XPath does not pierce shadow roots.
  - D) Playwright's default CSS locator does pierce open roots, so it finds 2.
</details>

---

### 47. A component attaches a CLOSED shadow root containing `<button>Reveal</button>`. What does this print?
```python
page.set_content("""
<secret-box></secret-box>
<script>
  class SecretBox extends HTMLElement {
    connectedCallback() {
      this.attachShadow({ mode: 'closed' }).innerHTML = '<button>Reveal</button>';
    }
  }
  customElements.define('secret-box', SecretBox);
</script>
""")
print(page.get_by_role("button", name="Reveal").count(),
      page.locator("secret-box").evaluate("el => el.shadowRoot"))
```
- [ ] A) `1 None`
- [ ] B) `1` followed by a ShadowRoot object
- [ ] C) `0` followed by a ShadowRoot object
- [ ] D) `0 None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `0 None`

**Explanation:** For a closed root, `host.shadowRoot` is `null` (Python `None`) and Playwright's locators cannot reach inside, so the role locator finds nothing even though a user sees the button.
- **Why others are wrong:**
  - A) Closed roots are not pierced, so the count is 0.
  - B) Neither part is right: the count is 0 and `shadowRoot` is null.
  - C) The `shadowRoot` property returns null for closed roots.
</details>

---

### 48. The page fills `#users` 800 ms after the Load button is clicked. What does this print (two lines)?
```python
page.set_content("""
<button id="load" onclick="setTimeout(() => {
  document.getElementById('users').innerHTML = '<li>Maria</li><li>John</li>';
}, 800)">Load</button>
<ul id="users"></ul>
""")
page.get_by_role("button", name="Load").click()
print(page.locator("#users li").all_inner_texts())
expect(page.locator("#users li")).to_have_count(2)
print(page.locator("#users li").all_inner_texts())
```
- [ ] A) `['Maria', 'John']` then `['Maria', 'John']`
- [ ] B) `[]` then `['Maria', 'John']`
- [ ] C) A `TimeoutError` on the first `print`
- [ ] D) `[]` then `[]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[]` then `['Maria', 'John']`

**Explanation:** `all_inner_texts()` is a snapshot, so right after the click the list is still empty. The `to_have_count(2)` assertion retries until the items exist, and after that the second read sees both names.
- **Why others are wrong:**
  - A) The first read happens about 800 ms before the data exists.
  - C) `all_inner_texts()` returns an empty list rather than waiting or raising.
  - D) After the assertion passes, the items are in the DOM.
</details>

---

### 49. What does this print? (An `ElementHandle` is the object returned by `query_selector`.)
```python
page.set_content("""
<button onclick="
  const ul = document.getElementById('items');
  ul.innerHTML = '';
  ['Alpha', 'Beta'].forEach(t => {
    const li = document.createElement('li'); li.textContent = t; ul.appendChild(li);
  });
">Re-render</button>
<ul id="items"><li>Alpha</li><li>Beta</li></ul>
""")
first = page.locator("#items li").first
handle = page.query_selector("#items li")
page.get_by_role("button", name="Re-render").click()
print(first.inner_text(), handle.is_visible())
```
- [ ] A) `Alpha True`
- [ ] B) It raises a stale element error.
- [ ] C) `Alpha False`
- [ ] D) `None False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Alpha False`

**Explanation:** The Locator is re-resolved at use time and finds the new first `<li>` ("Alpha"). The handle still points at the old, detached node, so `is_visible()` is `False`.
- **Why others are wrong:**
  - A) The old node was removed from the DOM, so the handle is not visible.
  - B) Playwright does not raise a stale element exception here; the locator works and the handle simply reports not visible.
  - D) `inner_text()` on the locator returns the string "Alpha", not `None`.
</details>

---

### 50. A local server answers `/old` with `301 Location: /products`. What does this print? (`BASE` is stripped from URLs to keep the output short.)
```python
r = page.goto(BASE + "/old")
print(r.status, r.url.replace(BASE, ""), r.request.redirected_from.url.replace(BASE, ""))
```
- [ ] A) `301 /old /old`
- [ ] B) `301 /products /old`
- [ ] C) `200 /old /products`
- [ ] D) `200 /products /old`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `200 /products /old`

**Explanation:** The browser follows the redirect, and `goto` returns the response for the final document: status 200 at `/products`. `request.redirected_from` links back to the original request for `/old`.
- **Why others are wrong:**
  - A) `goto` returns the final response, not the 301, and its URL is the final one.
  - B) The status of the returned response is the final 200; the 301 belongs to the earlier request in the chain.
  - C) The URLs are swapped: the response URL is `/products` and the redirected-from URL is `/old`.
</details>

---

### 51. What does this print? It is the lesson's recommended way to check query-string parts of a redirect URL.
```python
from urllib.parse import urlparse, parse_qs

u = urlparse("http://h/login?next=%2Fprotected&ref=email")
print(u.path, parse_qs(u.query))
```
- [ ] A) `/login {'next': ['/protected'], 'ref': ['email']}`
- [ ] B) `/login {'next': '/protected', 'ref': 'email'}`
- [ ] C) `/login?next=%2Fprotected&ref=email {}`
- [ ] D) `/login {'next': ['%2Fprotected'], 'ref': ['email']}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `/login {'next': ['/protected'], 'ref': ['email']}`

**Explanation:** `urlparse` separates the path from the query, and `parse_qs` returns a dictionary whose values are lists, with percent-encoding decoded (`%2F` becomes `/`). This is more robust than matching the raw string when parameter order or encoding may vary.
- **Why others are wrong:**
  - B) `parse_qs` always returns lists of values, even for a single value.
  - C) `urlparse` puts the query string in a separate attribute, so `path` is just `/login`.
  - D) `parse_qs` decodes percent-encoded characters.
</details>

---

### 52. The SPA's click handler calls `history.pushState` immediately and changes the heading text 400 ms later. What does this most likely print?
```python
page.goto(BASE + "/spa")          # <h1>Home view</h1> and an "Orders" button
page.get_by_role("button", name="Orders").click()
page.wait_for_url("**/spa/orders")
print(page.get_by_role("heading").inner_text())
```
- [ ] A) `Orders view`
- [ ] B) A `TimeoutError` from `wait_for_url`
- [ ] C) `Home view`
- [ ] D) `Orders (direct load)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Home view`

**Explanation:** `wait_for_url` recognises History API changes and returns as soon as the URL changes, which is before the 400 ms content update. `inner_text()` is an immediate read, so it still sees the old heading. The fix is `expect(page.get_by_role("heading", name="Orders view")).to_be_visible()`.
- **Why others are wrong:**
  - A) That text appears only 400 ms after the URL changed, after the read has already happened.
  - B) `wait_for_url` supports pushState navigations and does not time out here.
  - D) That heading belongs to a direct (full page) load of `/spa/orders`, which does not happen when the click handler uses `pushState`.
</details>

---

### 53. This input has the `multiple` attribute. What does the code print?
```python
page.set_content('<input id="many" type="file" multiple>')
page.locator("#many").set_input_files([
    {"name": "a.csv", "mimeType": "text/csv", "buffer": b"id\n1\n"},
    {"name": "b.txt", "mimeType": "text/plain", "buffer": "bonjour".encode("utf-8")},
])
print(page.locator("#many").evaluate(
    "el => Array.from(el.files).map(f => f.name + ':' + f.size)"))
```
- [ ] A) `['a.csv:4', 'b.txt:7']`
- [ ] B) `['a.csv:5', 'b.txt:7']`
- [ ] C) `['a.csv:5', 'b.txt:8']`
- [ ] D) An `Error` is raised because the input is not visible.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['a.csv:5', 'b.txt:7']`

**Explanation:** `b"id\n1\n"` is 5 bytes (`i`, `d`, newline, `1`, newline) and "bonjour" is 7 bytes in UTF-8. A list of in-memory file dictionaries uploads several files without touching the disk.
- **Why others are wrong:**
  - A) The two newline characters each count as one byte, giving 5, not 4.
  - C) "bonjour" has 7 letters, not 8.
  - D) `set_input_files` does not need the input to be visible, and multiple files are allowed here because of `multiple`.
</details>

---

### 54. A downloaded CSV is parsed as shown. What does this print?
```python
import csv, io

data = "id,name,total\n1,Maria,10.50\n2,John,20.00\n3,Ann,5.25\n"
rows = list(csv.DictReader(io.StringIO(data)))
print(len(rows), rows[0]["total"], type(rows[0]["total"]).__name__,
      sum(float(r["total"]) for r in rows))
```
- [ ] A) `4 10.50 str 35.75`
- [ ] B) `3 10.5 float 35.75`
- [ ] C) `3 10.50 int 35.75`
- [ ] D) `3 10.50 str 35.75`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `3 10.50 str 35.75`

**Explanation:** `DictReader` uses the first line as headers, so there are 3 data rows, and every CSV value is a string (`'10.50'`). Converting to `float` is needed for arithmetic: 10.50 + 20.00 + 5.25 = 35.75.
- **Why others are wrong:**
  - A) The header row is consumed as field names, not counted as a data row.
  - B) The value stays the string `'10.50'`; the csv module does not convert types.
  - C) The value is a string, not an `int`.
</details>

---

## Part 4: Fill-in-the-Blank

### 55. To reach a button inside an iframe `#inner` that itself sits inside an iframe `#outer`, chain the same method twice: `page._____("#outer")._____("#inner").locator("#deep")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `frame_locator` (both blanks)

**Explanation:** Each `frame_locator()` call steps into one more iframe document, so the chain reads "go into `#outer`, then go into `#inner`, then find `#deep`".
</details>

---

### 56. To keep only the table rows whose text contains "Maria Lopez", use `page.get_by_role("row")._____(_____="Maria Lopez")`. (Give the method and the keyword argument.)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `filter` and `has_text`

**Explanation:** `locator.filter(has_text=...)` narrows a set of locators to those containing the text (a case-insensitive substring match by default), and you can then act inside that row, for example `row.get_by_role("button", name="Delete").click()`.
</details>

---

### 57. After deleting a row, the lesson proves it is gone with `expect(row).to_have_count(_____)`, because the assertion waits for the row to be removed.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `0`

**Explanation:** `to_have_count(0)` retries until no element matches the row locator. Because the locator is lazy, it is re-evaluated each time and passes once the row has disappeared (use `to_have_count(1)` to prove a key is unique).
</details>

---

### 58. A `datetime-local` input takes values in the format `YYYY-MM-DD_HH:MM`, where the blank is the single separator character that belongs between the date and the time, for example `2025-03-14_14:30`. What character goes in the blank?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `T` (as in `2025-03-14T14:30`)

**Explanation:** `datetime-local` values are ISO-style with a `T` between date and time, so you call `fill("2025-03-14T14:30")`. A plain space or other separator is rejected as a malformed value.
</details>

---

### 59. To make `new Date()` and `Date.now()` in the page return a constant moment while timers still run normally, call `page.clock._____(datetime(2025, 3, 14, 10, 0, 0))` before the page's scripts read the time.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `set_fixed_time`

**Explanation:** `set_fixed_time` freezes the browser's notion of "now" without stopping timers, which is the simplest way to make date-picker tests deterministic. It affects only browser JavaScript, not server-side date logic.
</details>

---

### 60. To simulate two independent users, each with their own cookies and storage, create two separate contexts with `browser.new_____()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `context` (that is, `browser.new_context()`)

**Explanation:** Each browser context is isolated like a fresh incognito profile, whereas pages inside one context share cookies. Note that `browser.new_page()` quietly creates a context for you.
</details>

---

### 61. The selector prefix `_____=button` is the non-piercing CSS variant: it behaves like the browser's plain `querySelector` and does not look into shadow roots.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `css:light`

**Explanation:** `css:light=` exists to opt out of shadow-root piercing, which is rarely needed because piercing is the right default. On a page whose only buttons live in shadow roots it finds 0 matches.
</details>

---

### 62. `spinner.wait_for(state="_____")` waits until the spinner is either not visible or removed from the DOM entirely.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `hidden`

**Explanation:** The `hidden` state is satisfied both by an element that is invisible and by one that does not exist. The other states are `visible` (default), `attached`, and `detached` (removed from the DOM).
</details>

---

### 63. By default, an `expect(...)` web-first assertion retries for _____ seconds, whereas a locator action such as `click()` waits up to 30 seconds.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `5`

**Explanation:** The assertion timeout defaults to 5 seconds and the action timeout to 30 seconds. Override one assertion with `timeout=10_000` or all of them with `expect.set_options(timeout=...)`; do not raise global timeouts to hide flakiness.
</details>

---

### 64. After a click triggers a redirect chain, the recommended way to wait for the final destination is `page._____("**/dashboard")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `wait_for_url`

**Explanation:** `wait_for_url` accepts a glob, regular expression, or predicate and waits until the page URL matches, however many hops occurred in between. It replaces the legacy, racy `expect_navigation` for this purpose.
</details>

---

### 65. To clear a file input's current selection, call `locator.set_input_files(_____)` with an empty list literal. (Write the literal.)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `[]`

**Explanation:** `set_input_files([])` removes the selected files and fires `change` again, so the application can react to the cleared selection. In a quick check the input's `files.length` becomes 0.
</details>

---

### 66. To capture a download triggered by clicking "Export CSV", wrap the click in `with page._____() as download_info:` and read `download_info.value` afterwards.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `expect_download`

**Explanation:** This is the "register first, then act" pattern applied to downloads: the listener is active before the click, so the download event cannot be missed. Afterwards use `suggested_filename`, `save_as()`, `path()`, and `failure()` on the `Download` object, and verify the file's content.
</details>

---
