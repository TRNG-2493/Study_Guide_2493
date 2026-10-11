# Weekly Knowledge Check: Web Locators and Playwright Introduction (Day 4, Thursday)

**Topics covered today:**

1. CSS fundamentals: HTML, the DOM, CSS rules, specificity, and testing selectors in Chrome DevTools
2. Basic and attribute selectors: type, ID, class, universal, compound, attribute operators, choosing stable attributes
3. Pseudo-classes: positional, state, logical (`:not()`, `:is()`, `:has()`) and Playwright's extended pseudo-classes
4. Combinators: descendant, child, adjacent sibling and general sibling, plus anchoring strategy
5. Dynamic selectors: unstable ids and classes, partial matching, identity-based selection, timing versus selector problems
6. CSS vs. XPath: XPath syntax, functions, axes, and when to choose each language
7. Playwright architecture and setup: client, driver and browser, the object model, installation, launch options

**How to use this quiz:**

- There are 67 questions in four parts: Multiple Choice, True or False, Code Prediction, and Fill in the Blank.
- Answer each question on your own first (tick a box or write your answer), then open **Click for Solution** to check it.
- Read the explanation even when you were right: it explains why each wrong option fails.
- If you miss a question, reread the matching lesson from today before moving on.

---

## Part 1: Multiple Choice

### 1. What is the DOM?

- [ ] A) The original HTML text exactly as the server sent it
- [ ] B) A CSS file that lists every selector used on the page
- [ ] C) A Playwright object that stores all the locators of a test
- [ ] D) A live in-memory tree the browser builds from the HTML, which JavaScript can change while the page is open

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A live in-memory tree the browser builds from the HTML, which JavaScript can change while the page is open

**Explanation:** The browser turns HTML into the DOM, and selectors (including Playwright locators) work against the DOM, not the original source.

- **Why others are wrong:**
  - A) That is what View Source shows. The DOM is the current, possibly modified, tree.
  - B) CSS is the styling language; the DOM is the page structure the browser builds.
  - C) The DOM belongs to the browser. Playwright and CSS selectors work against it, they do not own it.

</details>

---

### 2. A teammate says: "`#login-button` is more specific than `button`, so it will win as a locator." What is the right response?

- [ ] A) Correct, Playwright always prefers ID selectors over type selectors
- [ ] B) Specificity only settles styling conflicts; both selectors can match the same element and neither "wins" in a locator context
- [ ] C) Correct, but only when the element also has a class
- [ ] D) Wrong, because specificity only applies to inline styles

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Specificity only settles styling conflicts; both selectors can match the same element and neither "wins" in a locator context

**Explanation:** Specificity is about styling conflicts. It does not affect which elements a selector matches, so do not treat it as locator priority.

- **Why others are wrong:**
  - A) Playwright has no such priority; specificity is not used when locating.
  - C) Classes do not change this; specificity is irrelevant to which elements a selector matches.
  - D) Specificity applies to all selector types (inline, ID, class, type), but only for resolving styling conflicts.

</details>

---

### 3. Which element is the known gotcha: invisible to the eye, yet still counted as visible by Playwright's visibility check?

- [ ] A) An element with `opacity: 0`
- [ ] B) An element with `display: none`
- [ ] C) An element with `visibility: hidden`
- [ ] D) An element with zero width or height

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) An element with `opacity: 0`

**Explanation:** `opacity: 0` makes an element invisible to the eye, but Playwright's check still counts it as visible.

- **Why others are wrong:**
  - B) `display: none` removes the element from layout entirely, so it is not visible.
  - C) It hides the element while keeping its space. The lesson names `opacity: 0` as the gotcha, not this.
  - D) Such an element is usually treated as not visible.

</details>

---

### 4. According to the lesson, what is the fastest way to validate a CSS selector in Chrome DevTools?

- [ ] A) Search for the selector text in View Source (`Ctrl+U`)
- [ ] B) Right-click the element and use Copy > Copy selector, then trust the result
- [ ] C) Press `Ctrl+F` in the Elements panel, type the selector, and read the match count (for example "1 of 1")
- [ ] D) Write the Playwright test first and see whether it fails

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Press `Ctrl+F` in the Elements panel, type the selector, and read the match count (for example "1 of 1")

**Explanation:** The Elements panel search box evaluates the selector and shows how many elements match, so you can confirm it matches exactly one.

- **Why others are wrong:**
  - A) View Source shows the original HTML, not the current DOM, and does not evaluate selectors.
  - B) Generated selectors are long and brittle; they are only a starting point, never a final answer.
  - D) That is slow. Senior engineers prove a locator in DevTools before putting it in code.

</details>

---

### 5. What does the selector `.card .btn` (with a space between the two parts) match?

- [ ] A) An element that has both the classes `card` and `btn`
- [ ] B) Any element with class `btn` that is inside an element with class `card`
- [ ] C) Only `.btn` elements that are direct children of `.card`
- [ ] D) Every element with class `card` and every element with class `btn`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Any element with class `btn` that is inside an element with class `card`

**Explanation:** A space is the descendant combinator: the right-most part (`.btn`) is returned when it sits anywhere inside `.card`.

- **Why others are wrong:**
  - A) That is `.card.btn`, written with no space.
  - C) Direct children need the `>` combinator, not a space.
  - D) That would be a comma-separated list: `.card, .btn`.

</details>

---

### 6. An element has `id="user:name"`. Which selector targets it without escaping problems?

- [ ] A) `#user:name`
- [ ] B) `.user:name`
- [ ] C) `[id="user:name"]`
- [ ] D) `user:name`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `[id="user:name"]`

**Explanation:** When an ID contains special characters, the attribute form `[id="..."]` is easier than escaping inside `#...`.

- **Why others are wrong:**
  - A) A special character such as the colon needs escaping in the ID form (`#user\:name`), so this is not the simple option.
  - B) That is a class selector; the element has an id, not a class.
  - D) With no prefix this is a type (tag) selector and matches no such tag.

</details>

---

### 7. An element has `class="btn-primary"`. Which selector matches it?

- [ ] A) `[class~="btn"]`
- [ ] B) `[class="btn"]`
- [ ] C) .btn
- [ ] D) `[class*="btn"]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `[class*="btn"]`

**Explanation:** `*=` matches the substring anywhere, while `~=` and `.class` need a whole word and `=` needs an exact match.

- **Why others are wrong:**
  - A) `~=` matches a whole space-separated word; `btn-primary` is a different word from `btn`.
  - B) `=` needs the whole attribute value to equal `btn` exactly.
  - C) `.btn` needs a class named exactly `btn`; this element's class is `btn-primary`.

</details>

---

### 8. On a form, the Reset button is `<button class="btn btn-secondary" type="reset" disabled>`. Which selector finds it the way the lesson recommends for boolean attributes?

- [ ] A) `button[disabled]`
- [ ] B) `button[disabled="true"]`
- [ ] C) `button.disabled`
- [ ] D) `button[type="disabled"]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `button[disabled]`

**Explanation:** Attributes such as `required`, `disabled` and `checked` have no value, so match them by presence: `[disabled]`.

- **Why others are wrong:**
  - B) Boolean attributes have no value in HTML, so presence is the correct test.
  - C) That looks for a class named `disabled`; this button's classes are `btn` and `btn-secondary`.
  - D) The `type` attribute is `reset`; `disabled` is a separate attribute.

</details>

---

### 9. Which selector matches `data-test="login-button"` regardless of upper or lower case in the attribute value?

- [ ] A) `[data-test="LOGIN-BUTTON"]i`
- [ ] B) `[data-test="LOGIN-BUTTON" i]`
- [ ] C) `[data-test="LOGIN-BUTTON" /i]`
- [ ] D) `[data-test^="LOGIN-BUTTON"]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[data-test="LOGIN-BUTTON" i]`

**Explanation:** Add a space and `i` before the closing bracket to make the value comparison case-insensitive.

- **Why others are wrong:**
  - A) The flag goes inside the brackets, before the closing bracket.
  - C) There is no slash; the flag is a space followed by `i`.
  - D) `^=` means "starts with" and is still case-sensitive.

</details>

---

### 10. Which of these is a pseudo-element, which Playwright cannot locate?

- [ ] A) `::before`
- [ ] B) `:first-child`
- [ ] C) `:checked`
- [ ] D) `:has()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `::before`

**Explanation:** Pseudo-elements use a double colon and target a part of an element. They are not DOM nodes, so locators cannot target them.

- **Why others are wrong:**
  - B) A single colon means pseudo-class; it selects a real element by position.
  - C) This is a state pseudo-class that selects real elements.
  - D) This is a logical pseudo-class that selects real elements.

</details>

---

### 11. A table has a `thead` with 1 row and a `tbody` with 4 rows. How many elements does `tr:first-child` match?

- [ ] A) 1
- [ ] B) 4
- [ ] C) 5
- [ ] D) 2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 2

**Explanation:** `tr:first-child` matches the first `tr` of each parent (the `thead` and the `tbody`), so be specific: `tbody tr:first-child`.

- **Why others are wrong:**
  - A) `:first-child` is evaluated per parent, not once for the whole table.
  - B) That would be all body rows; only the first row of each parent matches.
  - C) That would be every row in the table.

</details>

---

### 12. What can `:has()` do that ordinary combinators cannot?

- [ ] A) Select elements by their visible text in standard CSS
- [ ] B) Match only form controls that are not disabled
- [ ] C) Select an element based on what it contains, such as the row that contains a failing cell (`tr:has(td.fail)`)
- [ ] D) Select a pseudo-element such as `::after`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Select an element based on what it contains, such as the row that contains a failing cell (`tr:has(td.fail)`)

**Explanation:** `:has()` is the "parent selector": it lets a selector choose an element by its children.

- **Why others are wrong:**
  - A) Text matching needs Playwright extensions such as `:has-text()`; `:has()` checks for matching descendants.
  - B) That is the job of `:enabled`.
  - D) Pseudo-elements are not DOM nodes and cannot be located.

</details>

---

### 13. Which pseudo-class works only inside Playwright and causes an error in the DevTools `$$()` helper?

- [ ] A) `:not()`
- [ ] B) `:has()`
- [ ] C) `:nth-child()`
- [ ] D) `:has-text()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `:has-text()`

**Explanation:** `:has-text()` and the other Playwright extras (`:text-is()`, `:visible`, `:nth-match()`) are not part of standard CSS.

- **Why others are wrong:**
  - A) This is standard CSS and works in DevTools.
  - B) This is standard CSS, supported in current browsers, so it works in DevTools.
  - C) This is standard CSS and works in DevTools.

</details>

---

### 14. Given `<div class="box"><h3>Title</h3><p>One</p><p>Two</p></div>`, which paragraph does `p:nth-child(2)` match?

- [ ] A) "Two", because it is the second `p`
- [ ] B) Both paragraphs
- [ ] C) "One", because it is the second child overall
- [ ] D) Nothing, because the second child must be an `h3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) "One", because it is the second child overall

**Explanation:** `:nth-child` counts every sibling element, so the `h3` is child 1 and "One" is child 2. Use `:nth-of-type` to count same-tag siblings.

- **Why others are wrong:**
  - A) That would be `p:nth-of-type(2)`; `:nth-child` counts all sibling element types.
  - B) Only one element can be the second child of its parent.
  - D) The element must be both a `p` and the second child; "One" satisfies both.

</details>

---

### 15. What does the selector `.card button` return?

- [ ] A) The buttons inside cards; the right-most part is the subject of the selector
- [ ] B) The cards that contain a button
- [ ] C) Both the cards and their buttons
- [ ] D) Only buttons that are direct children of `.card`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The buttons inside cards; the right-most part is the subject of the selector

**Explanation:** The returned elements are always the right-most part of the selector.

- **Why others are wrong:**
  - B) Left-hand parts are only context filters; the cards are not returned.
  - C) Only the right-most part is returned.
  - D) A space means any depth. Direct children need `>`.

</details>

---

### 16. A card is `<div class="card"><h2>..</h2><p class="price">..</p><div class="actions"><button class="add">..</button><button class="info">..</button></div></div>`. Which selector matches nothing?

- [ ] A) `.card button`
- [ ] B) `.card > button`
- [ ] C) `.card > .actions > button`
- [ ] D) `.card > p`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `.card > button`

**Explanation:** The buttons are grandchildren of `.card` (inside `.actions`), so the child combinator `>` finds nothing.

- **Why others are wrong:**
  - A) The descendant combinator reaches the buttons at any depth.
  - C) This lists every level, so it matches both buttons.
  - D) The price paragraph is a direct child of `.card`, so this matches it.

</details>

---

### 17. A row holds `<input id="a">`, then `<span>hint</span>`, then `<span class="error">Bad</span>`, all siblings. Which selector matches the error span?

- [ ] A) `#a + .error`
- [ ] B) `#a > .error`
- [ ] C) `#a ~ .error`
- [ ] D) `.error ~ #a`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `#a ~ .error`

**Explanation:** The general sibling combinator `~` matches any later sibling, while `+` needs the very next one.

- **Why others are wrong:**
  - A) `+` needs the error to come immediately after the input, but the hint sits between.
  - B) `>` means direct child; the span is a sibling, not a child.
  - D) `~` only looks forward, and this would select the input, not the span.

</details>

---

### 18. Which locator best follows the "stable anchor, short path" strategy to reach the Add button of the Backpack card?

- [ ] A) `[data-test="product-backpack"] button.add`
- [ ] B) `body > div:nth-child(2) > div > div:nth-child(1) > button`
- [ ] C) `.add`
- [ ] D) `button:nth-child(1)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `[data-test="product-backpack"] button.add`

**Explanation:** Anchor on something unique and stable (a `data-test`), then walk a short path to the target.

- **Why others are wrong:**
  - B) An absolute positional chain from `body` breaks at the first layout change.
  - C) It matches the Add button of every card, not just the Backpack one.
  - D) It is position based and matches the first button of every container.

</details>

---

### 19. What does `page.locator(".card").locator("button.add")` do?

- [ ] A) It searches the whole page for `.card` and for `button.add` separately
- [ ] B) It searches for `button.add` only inside the elements matched by `.card`, similar to `page.locator(".card button.add")`
- [ ] C) It returns the `.card` element, not the button
- [ ] D) It is invalid, because a locator cannot call `locator()` again

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It searches for `button.add` only inside the elements matched by `.card`, similar to `page.locator(".card button.add")`

**Explanation:** Each `locator()` call scopes the search to the previous result, which expresses the same relationship as a descendant combinator.

- **Why others are wrong:**
  - A) Each chained call searches inside the previous one.
  - C) The last locator in the chain is what you get.
  - D) Chaining is a core Playwright feature.

</details>

---

### 20. A toast message appears 300 ms after clicking Save and disappears 3 seconds later. Which kind of "dynamic" problem is this?

- [ ] A) Dynamic attributes, fixed by a better selector
- [ ] B) Dynamic structure, fixed by using `:nth-child`
- [ ] C) Not a dynamic problem; the selector is simply wrong
- [ ] D) Dynamic timing, a synchronisation problem rather than a selector problem

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Dynamic timing, a synchronisation problem rather than a selector problem

**Explanation:** Dynamic timing means the element is not there (or not visible) yet. Diagnose first: rewriting the selector will not fix it.

- **Why others are wrong:**
  - A) The attribute values are not changing; the element is just not there yet.
  - B) Nothing is being re-ordered, and positional selectors are the last resort anyway.
  - C) The selector may be fine; the element does not exist in the DOM yet.

</details>

---

### 21. An input is `<input id="mat-input-83921" type="email" placeholder="Email">` and the number changes on every page load. Which selector is the most robust?

- [ ] A) `#mat-input-83921`
- [ ] B) `input[id*="1"]`
- [ ] C) `input[id^="mat-input-"][type="email"]`
- [ ] D) `div > div > input:nth-child(1)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `input[id^="mat-input-"][type="email"]`

**Explanation:** Anchor on the stable prefix with `^=` and add another stable attribute such as `type` to pick the right field.

- **Why others are wrong:**
  - A) The number changes on every load, so this works once and breaks next time.
  - B) A tiny substring will rarely match the right element and matches far too much.
  - D) A positional chain depends on layout and is fragile.

</details>

---

### 22. Search results reorder constantly. Which locator reliably finds the title of one specific result?

- [ ] A) `.result:nth-child(1) .title`
- [ ] B) `.result:last-child .title`
- [ ] C) `.result .title`
- [ ] D) `.result[data-id="SKU-1042"] .title`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `.result[data-id="SKU-1042"] .title`

**Explanation:** Select by identity (a data attribute holding the item id), not by position.

- **Why others are wrong:**
  - A) Position changes whenever the order changes.
  - B) Again position based, so a different item may be last tomorrow.
  - C) It matches every result title, not a specific one.

</details>

---

### 23. An element is visible on the page and in the Elements panel, but your selector never finds it. According to the lesson, what is one likely cause?

- [ ] A) It is inside an `<iframe>`, which is a different document, so you need `page.frame_locator(...)`
- [ ] B) Playwright cannot find elements that are visible
- [ ] C) The element must be using a pseudo-element
- [ ] D) CSS selectors cannot match elements with an `id`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It is inside an `<iframe>`, which is a different document, so you need `page.frame_locator(...)`

**Explanation:** Elements inside an iframe need `frame_locator()`; "it is in the Elements panel but never found" can mean an iframe.

- **Why others are wrong:**
  - B) Visibility is not the issue; the element is in another document.
  - C) Pseudo-elements are not DOM nodes and would not show in the Elements panel as elements.
  - D) ID selectors are among the strongest locators.

</details>

---

### 24. A locator matches 0 elements. According to the debug checklist, what is the first step?

- [ ] A) Add `time.sleep(10)` before the action
- [ ] B) Count it with `page.locator(selector).count()`: zero means no match, more than one means ambiguity
- [ ] C) Copy the absolute selector from DevTools
- [ ] D) Rewrite it with `:nth-child()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Count it with `page.locator(selector).count()`: zero means no match, more than one means ambiguity

**Explanation:** Counting tells you whether the problem is no match or too many; the next checks are timing, iframe/shadow DOM, hidden elements and dynamic values.

- **Why others are wrong:**
  - A) Sleeping slows tests and still fails when the app is slower; diagnose first.
  - C) Generated absolute selectors are brittle.
  - D) Positional selectors are a last resort and do not diagnose anything.

</details>

---

### 25. Which task is impossible with standard CSS combinators but straightforward in XPath?

- [ ] A) Selecting direct children of an element
- [ ] B) Selecting an element by the value of an attribute
- [ ] C) Selecting all descendants of an element
- [ ] D) Selecting an earlier sibling of an element with `preceding-sibling::`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Selecting an earlier sibling of an element with `preceding-sibling::`

**Explanation:** XPath axes can go up and backward; CSS combinators only go down and forward (with `:has()` covering some parent cases).

- **Why others are wrong:**
  - A) CSS does this with `>`.
  - B) CSS does this with `[attr="value"]`.
  - C) CSS does this with the descendant space.

</details>

---

### 26. Which XPath is the equivalent of the CSS selector `tr > td`?

- [ ] A) `//tr//td`
- [ ] B) `/tr/td`
- [ ] C) `//tr/td`
- [ ] D) `//tr/following-sibling::td`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `//tr/td`

**Explanation:** `/` is the XPath equivalent of `>` (direct child) and `//` is the equivalent of the descendant space.

- **Why others are wrong:**
  - A) `//` is the descendant, equivalent to the CSS space.
  - B) A single leading `/` is an absolute path from the document root, so it matches nothing here.
  - D) That selects later siblings of the `tr`, a different relationship.

</details>

---

### 27. You need all links whose `href` ends with `.pdf` in a browser. Why is CSS the better choice here?

- [ ] A) CSS has `[href$=".pdf"]`, while XPath 1.0 in browsers has no `ends-with()`
- [ ] B) XPath cannot read attributes
- [ ] C) CSS supports regular expressions in attribute values
- [ ] D) XPath only works on XML, never on HTML pages

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) CSS has `[href$=".pdf"]`, while XPath 1.0 in browsers has no `ends-with()`

**Explanation:** `ends-with` is XPath 2.0 and unavailable in browsers, so you would need `substring()` tricks; CSS `$=` is simple.

- **Why others are wrong:**
  - B) XPath reads attributes with `@`, for example `@href`.
  - C) Neither CSS nor XPath 1.0 supports regex.
  - D) Browsers evaluate XPath against the DOM of HTML pages.

</details>

---

### 28. You already have `table = page.locator("#orders")` and want to search for links inside it with XPath. Which expression stays inside the table?

- [ ] A) `table.locator("xpath=//a")`
- [ ] B) `table.locator("xpath=.//a")`
- [ ] C) `table.locator("xpath=/a")`
- [ ] D) `table.locator("xpath=a//")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `table.locator("xpath=.//a")`

**Explanation:** Start the XPath with `.//` (dot-slash-slash) when chaining so it searches within the existing locator.

- **Why others are wrong:**
  - A) A plain `//` always starts from the document root and escapes your chain.
  - C) A leading `/` is an absolute path from the root.
  - D) This is not a valid XPath expression.

</details>

---

### 29. Which situation matches the lesson's rule of thumb for choosing XPath over CSS?

- [ ] A) You need to match an element by one of its classes
- [ ] B) You want the fastest evaluation on a huge DOM
- [ ] C) The element is inside an open shadow root
- [ ] D) You need to move up to a parent or backward in the tree

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) You need to move up to a parent or backward in the tree

**Explanation:** Use CSS by default and XPath when you need to go up or backward, select by text in standard syntax, or maintain an XPath codebase.

- **Why others are wrong:**
  - A) CSS (`.class`) is far nicer; XPath class matching is awkward.
  - B) CSS is typically faster.
  - C) Playwright's CSS pierces open shadow roots; its XPath does not.

</details>

---

### 30. When your script calls `page.click(...)`, which describes what actually happens first?

- [ ] A) The Python client serialises the call and sends it to the Playwright driver, a bundled Node.js process
- [ ] B) The Python library clicks the element directly with the operating system's mouse
- [ ] C) An HTTP request goes to a separate driver executable for each browser
- [ ] D) The browser pulls the command from your script by polling

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The Python client serialises the call and sends it to the Playwright driver, a bundled Node.js process

**Explanation:** Client library to driver to browser: the driver applies auto-waiting and actionability checks, then talks to the browser over its protocol.

- **Why others are wrong:**
  - B) The client does not click anything itself.
  - C) That is Selenium's design; Playwright keeps one persistent connection.
  - D) Commands are streamed through the driver to the browser.

</details>

---

### 31. You ran `pip install pytest-playwright`, but your first script fails with "Executable doesn't exist ... please run playwright install". What is the fix?

- [ ] A) Reinstall `pytest` with `pip install --upgrade pytest`
- [ ] B) Install Node.js separately from nodejs.org
- [ ] C) Run `playwright install` (or `python -m playwright install`) to download the browser builds
- [ ] D) Install Chrome on your computer and retry

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Run `playwright install` (or `python -m playwright install`) to download the browser builds

**Explanation:** `pip install` gives you the library, not the browsers; `playwright install` downloads the tested builds.

- **Why others are wrong:**
  - A) The problem is missing browser binaries, not PyTest.
  - B) A Node.js-based driver ships inside the Python package.
  - D) Playwright uses its own pinned builds and does not use your installed browsers.

</details>

---

### 32. What is a Playwright `BrowserContext`?

- [ ] A) A single tab inside a browser
- [ ] B) An isolated session, like an incognito window, with its own cookies, storage and cache that is cheap to create
- [ ] C) The running browser process
- [ ] D) A description of how to find elements on a page

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) An isolated session, like an incognito window, with its own cookies, storage and cache that is cheap to create

**Explanation:** One browser with a fresh context per test gives fast, isolated tests.

- **Why others are wrong:**
  - A) A tab is a `Page`.
  - C) That is the `Browser`, which is more expensive to create.
  - D) That is a `Locator`.

</details>

---

### 33. Why do Playwright locators not go "stale" the way elements can in Selenium?

- [ ] A) Playwright caches a reference to the element when the locator is created
- [ ] B) Because pages in Playwright can never reload
- [ ] C) A locator is a lazy description; the search happens every time an action or assertion runs
- [ ] D) Because locators only work with the async API

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A locator is a lazy description; the search happens every time an action or assertion runs

**Explanation:** Because the search is repeated at the moment of each action, a locator never holds an outdated element.

- **Why others are wrong:**
  - A) Creating a locator does not search the page at all.
  - B) Pages reload normally; the locator simply searches again.
  - D) Locators are used throughout the sync API in this course.

</details>

---

### 34. Why does this course use Playwright's synchronous API?

- [ ] A) Code runs top to bottom, which is easy to read and debug and fits PyTest naturally
- [ ] B) The async API cannot drive Firefox or WebKit
- [ ] C) The sync API is faster inside the browser
- [ ] D) Sync and async code can be freely mixed in one script

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Code runs top to bottom, which is easy to read and debug and fits PyTest naturally

**Explanation:** Sync is the norm for test suites; async is for async applications or running many browsers concurrently.

- **Why others are wrong:**
  - B) Both APIs drive all three engines.
  - C) Speed in the browser is not the reason.
  - D) Do not mix the two styles in the same script.

</details>

---

## Part 2: True or False

Decide whether each statement is true or false. These target common misconceptions.

### 35. True or False: A selector such as `#login-button` always beats `button` as a locator, because ID selectors have higher specificity.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Specificity decides which styling rule wins. It does not change which elements a selector matches, so it is not locator priority.

</details>

---

### 36. True or False: "View Page Source" shows the current DOM, including elements added by JavaScript after the page loaded.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** View Source shows the original HTML text; the Elements panel in DevTools shows the current DOM. Selectors work against the DOM.

</details>

---

### 37. True or False: `document.querySelector("button")` returns a list of every button on the page.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `querySelector` returns the first match (or `null`); `querySelectorAll` returns the list of all matches.

</details>

---

### 38. True or False: The selector `[checked]` always reflects whether a checkbox is currently ticked.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `[checked]` reflects the HTML attribute (the initial state), which does not change when the user clicks. Use `:checked` for the live state.

</details>

---

### 39. True or False: CSS `:nth-child()` counts from 1, while Playwright's `.nth()` counts from 0.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is a common source of off-by-one errors: `:nth-child(1)` and `.nth(0)` both mean the first item.

</details>

---

### 40. True or False: The selector `h2 ~ p` can match a `p` that comes before the `h2` inside the same parent.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** CSS cannot look backward. `~` matches only later siblings; `:has()` is used for parent-style reasoning.

</details>

---

### 41. True or False: When content appears late on a page, the recommended fix is to add `time.sleep()` with a generous delay.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Sleeping slows tests and still fails when the app is slower than the guess. Timing problems are solved by waiting properly (Playwright's auto-waiting).

</details>

---

### 42. True or False: Playwright's CSS engine pierces open shadow DOM, but Playwright's XPath does not.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is a CSS advantage; if a selector works in Playwright but not in the DevTools Console, shadow DOM is a likely cause.

</details>

---

### 43. True or False: In XPath, `//a[@class='view']` also matches `<a class="view disabled">`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `@class='view'` requires the attribute to equal `view` exactly; use `contains(concat(' ', normalize-space(@class), ' '), ' view ')` for whole-word matching.

</details>

---

### 44. True or False: A Playwright `Locator` is lazy: creating it does not search the page, and the search happens when an action or assertion runs.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Because the search is repeated each time, locators do not go stale.

</details>

---

### 45. True or False: Running `pip install pytest-playwright` also downloads the Chromium, Firefox and WebKit browser binaries.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The package does not include the browsers. You must run `playwright install` separately.

</details>

---

### 46. True or False: Two browser contexts created from the same browser share cookies and local storage.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Each context is isolated, like an incognito window, so one can be logged in while the other is not.

</details>

---

## Part 3: Code Prediction

Work out the output first. The answers were checked by running the code (Playwright for Python with Chromium, and `python3 -m pytest` for the PyTest question).

### 47. What does this print?

Page: `shop.html` from the *Basic and attribute selectors* lesson (4 buttons: login, reset and two Add; links: logo, cart link and 2 per product).
```python
print(page.locator(".btn, .logo").count())
```

- [ ] A) 4
- [ ] B) 6
- [ ] C) 1
- [ ] D) 5

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 5

**Explanation:** The comma forms a selector list: 4 buttons with class `btn` plus 1 logo link give 5.

- **Why others are wrong:**
  - A) That counts only the four `.btn` buttons and forgets the logo link.
  - B) That is the number of all `a` links, not the match count.
  - C) A comma means OR (a union), not a narrowing; the logo is only one of the matches.

</details>

---

### 48. What does this print?

Page: `shop.html` from the *Basic and attribute selectors* lesson (4 buttons: login, reset and two Add; links: logo, cart link and 2 per product).
```python
print(page.locator('[class*="btn-"]').count())
```

- [ ] A) 4
- [ ] B) 2
- [ ] C) 1
- [ ] D) 0

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 2

**Explanation:** `*=` matches the substring anywhere: `btn-primary` on the login button and `btn-secondary` on the reset button.

- **Why others are wrong:**
  - A) That would be `.btn`. The Add buttons have `btn add`, with no hyphen after `btn`.
  - C) Both `btn-primary` (login) and `btn-secondary` (reset) contain `btn-`.
  - D) The substring `btn-` does appear in two class attributes.

</details>

---

### 49. What does this print?

Page: `combinators.html`, whose menu is `<ul class="menu">` with 3 top-level `li` items; the Products item contains a nested `<ul class="submenu">` with 2 more `li` items.

```python
print(page.locator(".menu li").count(), page.locator(".menu > li").count())
```

- [ ] A) 3 3
- [ ] B) 5 5
- [ ] C) 3 5
- [ ] D) 5 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 5 3

**Explanation:** `.menu li` reaches every depth (3 + 2 = 5); `.menu > li` counts only direct children (3).

- **Why others are wrong:**
  - A) The descendant space also reaches the two submenu items.
  - B) `>` counts only the direct children of `.menu`.
  - C) The counts are the other way round: descendant 5, child 3.

</details>

---

### 50. What does this print?

Page: `combinators.html`, whose field is:

```html
<input id="email" type="email">
<span class="hint">We never share it</span>
<span class="error">Invalid email</span>
```

```python
print(page.locator("#email + .error").count(), page.locator("#email ~ .error").count())
```

- [ ] A) 1 1
- [ ] B) 1 0
- [ ] C) 0 1
- [ ] D) 0 0

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 0 1

**Explanation:** `+` requires immediate adjacency (the hint is first), while `~` matches any later sibling.

- **Why others are wrong:**
  - A) `+` needs the error to be the immediate next sibling, but the hint is in between.
  - B) The values are reversed: `+` finds nothing, `~` finds the error.
  - D) `~` matches any later sibling, so it finds the error span.

</details>

---

### 51. What does this print?

Page: `pseudo.html`, whose list is:

```html
<ul id="tasks">
  <li class="task done">Write test plan</li>
  <li class="task">Create locators</li>
  <li class="task">Run smoke tests</li>
  <li class="task done">Review report</li>
  <li class="task">Retrospective</li>
</ul>
```

```python
print(page.locator("#tasks li:nth-child(3n+1)").all_inner_texts())
```

- [ ] A) ['Write test plan', 'Review report']
- [ ] B) ['Create locators', 'Review report']
- [ ] C) ['Write test plan', 'Run smoke tests', 'Retrospective']
- [ ] D) ['Write test plan']

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) ['Write test plan', 'Review report']

**Explanation:** `3n+1` selects the 1st, 4th, 7th... children, which in a list of five means items 1 and 4.

- **Why others are wrong:**
  - B) That is items 2 and 4, which is not the `3n+1` pattern.
  - C) That is the `odd` pattern (1, 3, 5).
  - D) `3n+1` gives positions 1 and 4 in a list of 5, so two items match.

</details>

---

### 52. What does this print?

Page: `pseudo.html` (the checkbox `#agree` starts checked, `#news` starts unchecked).

```python
print(page.locator("input:checked").count())
page.locator("#news").check()
print(page.locator("input:checked").count())
```

- [ ] A) 0 then 1
- [ ] B) 1 then 2
- [ ] C) 1 then 1
- [ ] D) 2 then 2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 1 then 2

**Explanation:** `:checked` follows the live state: one checked box at first, two after `#news` is ticked.

- **Why others are wrong:**
  - A) `#agree` is already checked at the start, so the first count is 1.
  - C) `:checked` reflects the live state, so ticking `#news` adds a second match.
  - D) Only `#agree` is checked before the action.

</details>

---

### 53. What does this print?

Page: `pseudo.html`, which has two cards: `<div class="card"><p>Intro</p><p>Details</p></div>` and `<div class="card"><h3>Alone</h3></div>`.

```python
el = page.locator(".card :only-child")
print(el.count(), el.inner_text())
```

- [ ] A) 2 Alone
- [ ] B) 2 Intro
- [ ] C) 1 Details
- [ ] D) 1 Alone

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 1 Alone

**Explanation:** Only the `h3` in the second card is the sole child of its parent.

- **Why others are wrong:**
  - A) The two paragraphs in the first card are siblings, so neither is an only child.
  - B) Neither `p` is the only child of its parent.
  - C) "Details" has a sibling, so it does not match.

</details>

---

### 54. What does this print?

Page: `pseudo.html` (the task list from the earlier question, first item "Write test plan", second "Create locators").

```python
print(page.locator("#tasks li").nth(1).inner_text(), "|", page.locator("#tasks li:nth-child(1)").inner_text())
```

- [ ] A) Create locators | Write test plan
- [ ] B) Write test plan | Write test plan
- [ ] C) Create locators | Create locators
- [ ] D) Write test plan | Create locators

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Create locators | Write test plan

**Explanation:** Playwright's `.nth()` is zero-based, while CSS `:nth-child()` starts at 1.

- **Why others are wrong:**
  - B) `.nth()` counts from 0, so `.nth(1)` is the second item.
  - C) CSS `:nth-child(1)` counts from 1, so it selects the first item.
  - D) The two counting styles are swapped in this option.

</details>

---

### 55. What does this print?

Page: `xpath.html`, whose `tbody` has 3 rows, each with 4 `td` cells (the header row uses `th`).

```python
print(page.locator("xpath=//td[2]").count(), page.locator("xpath=(//td)[2]").count())
```

- [ ] A) 1 1
- [ ] B) 3 1
- [ ] C) 3 3
- [ ] D) 1 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 3 1

**Explanation:** `//td[2]` means the second `td` among its siblings (one per row); `(//td)[2]` is the second `td` in the whole document.

- **Why others are wrong:**
  - A) `//td[2]` is evaluated per parent, so each row contributes one match.
  - C) Parentheses make `[2]` apply to the whole list, giving exactly one match.
  - D) The values are reversed.

</details>

---

### 56. What does this print?

Page: `xpath.html`, where the links in the table have classes `view`, `view` and `view disabled` (one per row).

```python
print(page.locator("xpath=(//a)[last()]").get_attribute("class"))
```

- [ ] A) view
- [ ] B) row
- [ ] C) view disabled
- [ ] D) A strict mode violation error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) view disabled

**Explanation:** Parentheses make `last()` apply to all anchors in the document, returning only the final link.

- **Why others are wrong:**
  - A) The last link in the document is Carol's, whose class is `view disabled`.
  - B) `row` is a class of the table rows, not of links.
  - D) That would happen with `//a[last()]` (the last `a` of every parent, three matches). The parentheses leave one match.

</details>

---

### 57. What does this print?

Page: `xpath.html`, with the same three links (`view`, `view`, `view disabled`).

```python
print(page.locator("xpath=//a[@class='view']").count(), page.locator("a.view").count())
```

- [ ] A) 3 3
- [ ] B) 2 2
- [ ] C) 3 2
- [ ] D) 2 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 2 3

**Explanation:** Exact class matching in XPath misses elements with several classes, which is why CSS `.view` is nicer.

- **Why others are wrong:**
  - A) `@class='view'` needs the whole attribute to equal `view`, so `view disabled` is excluded.
  - B) The CSS `.view` matches any element that has the class `view`, including `view disabled`.
  - C) The two values are swapped.

</details>

---

### 58. A trainee saves this as `test_counts.py` (using the module-scoped `page` fixture from the lesson, pointed at `shop.html` from the lesson). What is the summary line of `python3 -m pytest`?

```python
CASES = [
    ("#login-button", 1),
    ("button", 4),
    (".btn", 3),
]

@pytest.mark.parametrize("selector, expected", CASES)
def test_selector_matches_expected_count(page, selector, expected):
    assert page.locator(selector).count() == expected
```

- [ ] A) 3 passed
- [ ] B) 2 passed, 1 failed
- [ ] C) 1 passed, 2 failed
- [ ] D) An error during collection

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 2 passed, 1 failed

**Explanation:** `parametrize` generates one test per pair, and only the `.btn` case has a wrong expectation (it should be 4).

- **Why others are wrong:**
  - A) `.btn` matches 4 elements, so the third case fails (4 != 3).
  - C) Both `#login-button` (1) and `button` (4) match as expected.
  - D) Parametrize creates one test per pair; they are collected and run normally.

</details>

---

### 59. What does this print?

```python
sku = "BP-001"
selector = f'[data-sku="{sku}"]'
print(selector)
```

- [ ] A) [data-sku="{sku}"]
- [ ] B) [data-sku='BP-001']
- [ ] C) [data-sku="BP-001"]
- [ ] D) data-sku="BP-001"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) [data-sku="BP-001"]

**Explanation:** An f-string inserts the variable's value, which is how selectors are built from known test data.

- **Why others are wrong:**
  - A) The `f` prefix substitutes the variable, so the braces do not appear.
  - B) The outer string uses single quotes, so the inner double quotes stay as written.
  - D) The square brackets are part of the string and stay in the output.

</details>

---

## Part 4: Fill in the Blank

Write the missing word or symbol before opening the solution.

### 60. In the Chrome DevTools Console, the helper that evaluates an XPath and returns an array is `_____("//button[@type='submit']")`.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `$x`

**Explanation:** `$x()` is the Chrome Console helper for XPath, as `$$()` is for CSS.

</details>

---

### 61. The attribute selector operator that means "ends with" is `_____`, as in `a[href_____".pdf"]`.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `$=`

**Explanation:** `$` mirrors the end anchor in regular expressions; `^=` is starts-with and `*=` is contains.

</details>

---

### 62. Playwright's extended pseudo-class for an exact, case-sensitive full-text match is `button:_____("Sign up")`.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `text-is` (the pseudo-class `:text-is()`)

**Explanation:** `:has-text()` is a case-insensitive substring match, while `:text-is()` needs the whole text.

</details>

---

### 63. In the selector `.card button`, the elements that are returned are the ______-most part of the selector.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** right

**Explanation:** The right-most part is the subject; the parts on the left only provide context.

</details>

---

### 64. In `//td[@class='status']/_____::tr`, the axis name that goes up exactly one level to the parent is `_____`.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `parent`

**Explanation:** `parent::` is the long form of `..`; `ancestor::` goes up through all ancestors.

</details>

---

### 65. To download only the Chromium browser build, run `playwright _____ chromium`.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `install`

**Explanation:** `playwright install` downloads all browsers; adding a name saves time and disk space.

</details>

---

### 66. In `p.chromium.launch(headless=False, _____=500)`, the option that pauses 500 ms between actions is `_____`.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `slow_mo`

**Explanation:** Use `slow_mo` only while learning or debugging so you can follow the actions.

</details>

---

### 67. A Playwright _____ is like an incognito window: it has its own cookies, local storage and cache and is cheap to create.

- [ ] Your answer: ________

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `BrowserContext`

**Explanation:** One browser with a new context per test keeps tests isolated and fast.

</details>

---

## Topic Coverage

| Topic | Question numbers |
|-------|------------------|
| CSS fundamentals (HTML, DOM, CSS rules, specificity, DevTools) | 1, 2, 3, 4, 35, 36, 37, 60 (8) |
| Basic and attribute selectors | 5, 6, 7, 8, 9, 38, 47, 48, 58, 61 (10) |
| Pseudo-classes | 10, 11, 12, 13, 14, 38, 39, 51, 52, 53, 54, 58, 62 (13) |
| Combinators | 15, 16, 17, 18, 19, 40, 49, 50, 63 (9) |
| Dynamic selectors | 20, 21, 22, 23, 24, 41, 42, 59 (8) |
| CSS vs. XPath | 25, 26, 27, 28, 29, 42, 43, 55, 56, 57, 60, 64 (12) |
| Playwright architecture and setup | 30, 31, 32, 33, 34, 44, 45, 46, 65, 66, 67 (11) |

Every question is tied to at least one of today's lessons; a few questions touch two topics and appear in both rows.
