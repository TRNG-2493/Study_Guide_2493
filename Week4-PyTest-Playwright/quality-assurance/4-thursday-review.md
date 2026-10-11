# Interview Questions: Week 4 - PyTest-Playwright - Thursday

Topics covered: CSS fundamentals, basic and attribute selectors, pseudo-classes, combinators, dynamic selectors, CSS vs. XPath, and Playwright architecture and setup. Try to answer out loud before you reveal each answer.

## Beginner (Foundational)

### Q1: What is the difference between "View Page Source" and the DOM you see in DevTools, and why does it matter for locators?
**Keywords:** DOM, View Source, original HTML, JavaScript, live tree
**Hint:** Which one does a selector actually run against?
<details>
<summary>Click to Reveal Answer</summary>

"View Page Source" shows the original HTML text the server sent. The DOM is the live in-memory tree the browser builds from that HTML, and JavaScript can change it afterwards by adding, removing or modifying elements. DevTools' Elements panel shows the current DOM. CSS selectors and Playwright work against the DOM, not the source, so an element created by JavaScript will not appear in View Source but can still be located once it is in the DOM.
</details>

---

### Q2: What does a CSS selector return, and what is the difference between `querySelector` and `querySelectorAll`? What should a good test locator match?
**Keywords:** list of matches, first match, null, exactly one element, strict mode
<details>
<summary>Click to Reveal Answer</summary>

A selector does not return "the" element, it matches all elements that fit, which can be zero, one or many. `document.querySelector(sel)` returns the first match or `null`, while `document.querySelectorAll(sel)` returns a list of all matches. A good test locator should match exactly one element, the right one, every time. If it matches several, Playwright raises a strict-mode error when you try an action like `click()`.

```js
document.querySelectorAll('button[type="submit"]').length   // how many matches?
```
</details>

---

### Q3: What is the difference between `.btn.btn-primary` and `.card .btn`? Why does whitespace matter in selectors?
**Keywords:** compound selector, no space, descendant, same element, inside
<details>
<summary>Click to Reveal Answer</summary>

`.btn.btn-primary` has no space, so it is a compound selector: one single element must have both classes. `.card .btn` has a space, which is the descendant combinator: any `.btn` located anywhere inside a `.card`. Whitespace changes the meaning completely, so an accidental space is a classic mistake. In the same way `.product.sale` means one element with both classes, while `.product .sale` means a `.sale` inside a `.product`.
</details>

---

### Q4: Explain the difference between the attribute selectors `[attr^="v"]`, `[attr$="v"]`, `[attr*="v"]`, and `[attr~="v"]`.
**Keywords:** starts with, ends with, contains, whole word, class list
**Hint:** Think about regular-expression anchors for the first two.
<details>
<summary>Click to Reveal Answer</summary>

`^=` means the value starts with the text, `$=` means it ends with it, and `*=` means it contains it anywhere, so `*=` is the broadest. `~=` matches the value as one whole word in a space-separated list, which is how `.class` works behind the scenes. For example `[class~="btn"]` matches `class="btn large"` but not `class="btn-primary"`, whereas `[class*="btn"]` matches both. I would use `a[href$=".pdf"]` for links ending in `.pdf`, and be careful with `*=` because short substrings match too much.
</details>

---

### Q5: What is a pseudo-class, and how does it differ from a pseudo-element?
**Keywords:** single colon, state or position, double colon, not in the DOM, cannot be located
<details>
<summary>Click to Reveal Answer</summary>

A pseudo-class starts with a single colon and selects elements in a particular state or position that tag, id, class or attributes do not express, for example `button:disabled` or `li:first-child`. The browser computes that status on the fly; there is no real `class="first-child"` in the HTML. A pseudo-element uses a double colon, like `::before` or `::after`, and targets a generated part of an element. Pseudo-elements are not DOM nodes, so Playwright cannot locate them, and seeing one in a test selector is a warning sign.
</details>

---

### Q6: What is the difference between `:nth-child()` and `:nth-of-type()`, and where does CSS counting start?
**Keywords:** counts from 1, all siblings, same tag, mixed tags
<details>
<summary>Click to Reveal Answer</summary>

CSS counts from 1, not 0. `:nth-child(n)` counts all sibling elements regardless of tag, while `:nth-of-type(n)` only counts siblings with the same tag. In `<div><h3/><p/><p/></div>`, `p:nth-child(2)` matches the first `p`, because it is the second child overall, but `p:nth-of-type(2)` matches the second `p`. When a parent holds mixed tags, `:nth-of-type` is less surprising.
</details>

---

### Q7: Why is `:checked` better than `[checked]` for asserting the current state of a checkbox?
**Keywords:** HTML attribute, initial state, live property, current state
<details>
<summary>Click to Reveal Answer</summary>

`[checked]` matches the HTML attribute, which reflects only the initial state. When a user ticks the box, the attribute does not change, but the live state does. The `:checked` pseudo-class reflects that live state, so it is the right choice to know whether the box is currently checked. In Playwright you can also use `is_checked()` for the live state.

```css
input[type="checkbox"]:checked
```
</details>

---

### Q8: Name the four CSS combinators and what each one means.
**Keywords:** descendant, child, adjacent sibling, general sibling, right-most
<details>
<summary>Click to Reveal Answer</summary>

The descendant combinator is a space and matches an element anywhere inside another, at any depth. The child combinator `>` matches only direct children. The adjacent sibling `+` matches the element immediately after another one with the same parent, and the general sibling `~` matches any later sibling with the same parent. In all of them the right-most part is the subject, so `.card button` returns buttons, not cards.
</details>

---

### Q9: What is the difference between `#email + .error` and `#email ~ .error`?
**Keywords:** immediately after, any later sibling, same parent, in between
<details>
<summary>Click to Reveal Answer</summary>

`+` requires the `.error` element to come immediately after `#email`, with no other element in between. `~` only requires it to be a later sibling with the same parent, so other elements can sit between them. If a `.hint` span sits between the input and the error span, `#email + .error` matches nothing, but `#email ~ .error` matches. Neither can look backward, because CSS only goes forward.
</details>

---

### Q10: What are the three meanings of "dynamic" in dynamic selectors, and why does separating them matter?
**Keywords:** dynamic attributes, dynamic structure, dynamic timing, selector problem, synchronisation problem
<details>
<summary>Click to Reveal Answer</summary>

Dynamic attributes means an id, class or other value changes between loads or builds, for example `id="input-83921"`. Dynamic structure means elements are added, removed or reordered, such as a banner pushing everything down. Dynamic timing means the element is not in the DOM yet, or no longer. The first two are selector problems, while timing is a synchronisation problem fixed by waiting correctly. Diagnosing first avoids the beginner mistake of rewriting a selector when the issue is timing, or adding a sleep when the selector is bad.
</details>

---

### Q11: In what order of preference would you pick an attribute for a stable locator?
**Keywords:** data-test, static id or name, aria-label, short structure, position last
<details>
<summary>Click to Reveal Answer</summary>

First choice is a dedicated test attribute such as `data-test`, `data-testid` or `data-qa`, because its only purpose is testing. Next are static, meaningful ids and names, then accessibility attributes like `aria-label`, `role`, `title` or `alt`. After that I would use meaningful structure with a short path, then visible text through Playwright's text-based locators, and positional selectors only as a last resort. If the app has no `data-test` attributes, I would ask the developers to add them.
</details>

---

### Q12: What can XPath do that standard CSS cannot, and what do `//` and `/` mean in XPath?
**Keywords:** parent, backward, text, axes, descendant, direct child
<details>
<summary>Click to Reveal Answer</summary>

XPath can select by text content in standard syntax and can move up to a parent (`..`, `parent::`, `ancestor::`) or backward (`preceding-sibling::`). Standard CSS combinators only go down and forward, although `:has()` covers some upward cases. `//` means a descendant at any depth, like the CSS descendant space, and `/` means a direct child, like `>`. A relative path starting with `//` is what you use almost always, and absolute paths from the root should be avoided.

```text
//td[normalize-space()='Bob Jones']/parent::tr//a
```
</details>

---

### Q13: What is Playwright, and how does its architecture differ from Selenium's?
**Keywords:** browser automation, client, driver, persistent connection, auto-waiting
<details>
<summary>Click to Reveal Answer</summary>

Playwright is an open-source browser automation library from Microsoft that drives Chromium, Firefox and WebKit through one API. Your Python client sends messages to a bundled Playwright driver (a Node.js process), which talks to the browser over its debugging protocol. This gives a persistent connection with events streamed, instead of Selenium's HTTP commands to a separate driver executable per browser. As a result Playwright is faster, has built-in auto-waiting, and uses pinned browser builds downloaded by `playwright install`.
</details>

---

### Q14: Explain the difference between a Browser and a BrowserContext in Playwright, and why contexts matter for tests.
**Keywords:** isolated profile, cookies, cheap, incognito, new page
<details>
<summary>Click to Reveal Answer</summary>

A Browser is one running browser process, and it is expensive to create. A BrowserContext is like an incognito window inside it, with its own cookies, local storage and cache, and creating one is very cheap. Two contexts do not share state, so one can be logged in as a user while the other is not. This is why test runners create one browser and a fresh context per test, which keeps tests independent and fast. Calling `browser.new_page()` quietly creates a context and a page for you.
</details>

---

## Intermediate (Application)

### Q15: Your test uses `#mat-input-83921` for the email field and fails after a reload because the id is now `mat-input-17254`. How do you fix it?
**Keywords:** auto-generated id, stable prefix, `^=`, additional attribute, data-test
**Hint:** Part of the value is stable.
<details>
<summary>Click to Reveal Answer</summary>

The number is auto-generated, so I would not rely on the whole id. I would anchor on the stable prefix with `^=` and add another stable attribute to pick the right field, because the prefix alone matches every Material input. Even better is a `data-test` attribute on the field or its container, and I would ask developers to add one. I would also confirm in DevTools that the count is exactly one.

```python
page.locator('input[id^="mat-input-"][type="email"]').fill("a@b.com")
page.locator('[data-test="email-row"] input').fill("a@b.com")
```
</details>

---

### Q16: `tr:first-child` returns two elements on a results table that has a `thead` and a `tbody`. Why, and how would you target the first data row, or the row for "Search" more robustly?
**Keywords:** first-child per parent, tbody, has-text, position is brittle, meaning over position
<details>
<summary>Click to Reveal Answer</summary>

`:first-child` matches the first `tr` of each parent, so it returns the header row inside `thead` and the first row inside `tbody`. To get the first data row, scope it with `tbody tr:first-child`. If the requirement is really "the Search row", I would avoid position because it breaks when rows are added or reordered, and select by meaning instead, such as `page.locator("#results tbody tr", has_text="Search")`. Position is only appropriate when the position itself is the requirement, for example "the newest item is first".
</details>

---

### Q17: A table lists users, each with a Delete button. How do you click Delete for "Bob" so the test survives sorting and pagination? Show the CSS and the XPath way.
**Keywords:** anchor, `:has()`, parent, `parent::tr`, stable row
<details>
<summary>Click to Reveal Answer</summary>

I anchor on something stable, the cell with Bob's name, and then go to the row and down to its button. Combinators cannot go up, so in CSS I use `:has()` on the row, and in XPath I can use `parent::`. In Playwright I could also chain a row filtered by text. Either way the locator does not depend on Bob's position.

```text
CSS (Playwright):  #users tr:has(td:first-child:text-is('Bob')) button.delete
XPath:             //td[normalize-space()='Bob']/parent::tr//button
```
</details>

---

### Q18: You chain `page.locator("#orders").locator("xpath=//a")` and get links from the whole page, not only inside `#orders`. What went wrong, and how do you fix it?
**Keywords:** `//` document root, `.//`, chaining, scope, escapes the chain
<details>
<summary>Click to Reveal Answer</summary>

An XPath starting with `//` always starts from the document root, so it escapes the chain and searches the entire page. When starting an XPath from an existing locator, use `.//` (dot-slash-slash) so it searches within that element. The fix is `page.locator("#orders").locator("xpath=.//a")`. This is a common bug, listed among the lesson's common mistakes.
</details>

---

### Q19: A teammate runs `pip install pytest-playwright` and then their script fails with "Executable doesn't exist ... please run playwright install". What is wrong, and what else could cause setup trouble?
**Keywords:** browser binaries, `playwright install`, virtual environment, `--with-deps`, file named playwright.py
<details>
<summary>Click to Reveal Answer</summary>

`pip install` only installs the Python package. The browser binaries are not included, so they must be downloaded with `playwright install`, or `playwright install chromium` to save space. If the `playwright` command is not found, run `python -m playwright install`. Other common causes are installing outside the virtual environment, naming a script `playwright.py` so Python imports your file instead of the library, and forgetting to re-run `playwright install` after upgrading. On Linux and in CI use `playwright install --with-deps`.

```bash
pip install pytest-playwright
playwright install chromium
```
</details>

---

## Advanced (Deep Dive)

### Q20: Walk me through what happens under the hood when your script runs `page.locator("#login-button").click()`, and explain why Playwright locators do not go "stale".
**Keywords:** client serialises, driver, actionability checks, browser protocol, lazy locator
**Hint:** Think of the three parts: client, driver, browser.
<details>
<summary>Click to Reveal Answer</summary>

The Python client does not click anything itself. It serialises the request and sends it to the bundled Playwright driver. The driver applies Playwright's logic, finding the element and waiting until it is attached, visible, stable, enabled and receiving events. Then it sends the click to the browser through its debugging protocol (the Chrome DevTools Protocol for Chromium, or an equivalent in the patched Firefox and WebKit builds), and the browser performs it and reports back. A locator is only a lazy description of how to find elements, so creating one does not search the page. The search runs every time you act or assert, which is why locators do not go stale like Selenium element references can.
</details>

---

## Coverage Table

| Lesson | Questions |
|--------|-----------|
| css-fundamentals | Q1, Q2 |
| basic-and-attribute-selectors | Q3, Q4 |
| pseudo-classes | Q5, Q6, Q7, Q16 |
| combinators | Q8, Q9, Q17 |
| dynamic-selectors | Q10, Q11, Q15 |
| css-vs-xpath | Q12, Q17, Q18 |
| playwright-architecture-and-setup | Q13, Q14, Q19, Q20 |

Distribution: 14 Beginner (70%), 5 Intermediate (25%), 1 Advanced (5%).
