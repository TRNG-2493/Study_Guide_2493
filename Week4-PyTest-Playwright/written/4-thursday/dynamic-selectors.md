# Dynamic Selectors

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what makes a selector "dynamic" and why dynamic page content breaks naive locators.
- Recognise the most common sources of instability: auto-generated IDs, hashed class names, positional dependence, changing text, and content that appears or disappears.
- Write resilient selectors using partial attribute matching (`^=`, `$=`, `*=`), stable attributes, and structural anchors.
- Use `:has()`, `:not()`, and relational anchoring to find elements without relying on volatile values.
- Build selectors from variables in Python safely (f-strings, parametrization), and understand quoting pitfalls.
- Distinguish between a **bad selector** problem and a **timing** problem (element not there *yet*).
- Apply a decision checklist to choose the most stable locator for any element.

## Why This Matters

The weekly epic asks you to turn manual tests into automation that actually keeps working. The number one reason UI automation gets abandoned is **flakiness and maintenance cost**: tests that pass on Monday and fail on Tuesday although nothing is wrong with the product. A major source of that pain is selectors tied to details that change without any change in behaviour.

On modern web applications (React, Angular, Vue, Material UI) the page you inspect today may carry different IDs, class names, and element order tomorrow. In Project 1: QE Foundations, your pair's locator catalog will be useful only if its selectors survive page reloads and reasonable releases. This lesson gives you the techniques to make that happen.

It builds on the previous lessons: basic and attribute selectors, pseudo-classes, and combinators.

---

## The Concept

### 1. What is a "dynamic" selector problem?

"Dynamic" can mean three different things. Separating them is the first step to fixing any broken locator.

| Type | Description | Example |
|------|-------------|---------|
| **Dynamic attributes** | An id/class/attribute value changes between loads or builds | `id="input-83921"` becomes `id="input-17254"` |
| **Dynamic structure** | Elements are added, removed, or re-ordered | A promo banner pushes everything down; new row inserted at top |
| **Dynamic timing** | The element does not exist in the DOM *yet* (or no longer) | A toast appears 300 ms after a click and disappears after 3 s |

Dynamic attributes and structure are *selector* problems (fixed by better selectors). Dynamic timing is a *synchronisation* problem (fixed by waiting correctly; Playwright's auto-waiting makes this much easier and we will study it in depth on Friday). A beginner often rewrites the selector when the real problem is timing, or adds a sleep when the real problem is a bad selector. Always diagnose first.

### 2. Common Sources of Dynamic Values

#### 2.1 Auto-generated IDs

Frameworks and component libraries often create ids with counters or random suffixes:

```html
<input id="mat-input-0">          <!-- Angular Material; the number depends on render order -->
<input id="react-select-3-input"> <!-- React Select -->
<div id="ember1234">              <!-- Ember -->
<input id="j_idt42:username">     <!-- JSF -->
<div id="a1b2c3d4-5678-...">      <!-- GUID -->
```

If you see a number or random token inside an id, assume it is unstable.

#### 2.2 Hashed or generated class names

CSS-in-JS and CSS Modules produce class names such as:

```html
<button class="Button_primary__3xK9a css-1x2y3z">Pay</button>
```

The suffix after the underscores or the `css-` hash changes whenever the styles change, even slightly.

#### 2.3 Positional dependence

`:nth-child(4)` or `div > div > div:nth-child(2)` depends on layout order that product teams modify constantly (A/B tests, banners, cookie notices).

#### 2.4 Changing text

Prices, dates, usernames, counts ("3 items"), localisation (English vs. French), and marketing copy all change.

#### 2.5 Conditional elements

Elements that exist only in some states (logged in vs. anonymous, error vs. success, loading spinner).

### 3. Strategy: Stable Over Volatile

Use this ordered checklist whenever you write a locator.

1. **Dedicated test attributes**: `data-test`, `data-testid`, `data-qa`, `data-cy`. Ask developers to add them. They are the gold standard, because their *only* purpose is testing.
2. **Static, meaningful ids and names**: `#username`, `[name="email"]`.
3. **Accessibility attributes**: `aria-label`, `role`, `title`, `alt`. They are tied to behaviour and accessibility requirements, so they change less often (though wording can change).
4. **Meaningful structure**: a stable semantic container plus a short path, e.g. `form#login input[type="password"]`.
5. **Visible text and labels** (through Playwright's text-based locators, introduced Friday).
6. **Last resort**: positional selectors, only when order is the requirement.

### 4. Technique 1: Partial Attribute Matching for Partially Dynamic Values

When part of a value is stable, anchor on that part.

```html
<input id="mat-input-83921" placeholder="Email">
<div id="order-row-5521" class="order-row">...</div>
<button class="Button_primary__3xK9a css-1x2y3z">Pay</button>
```

```css
[id^="mat-input-"]          /* starts with stable prefix */
[id^="order-row-"]          /* any order row */
button[class*="Button_primary"]   /* contains stable part of hashed class */
a[href$="/checkout"]        /* ends with stable path */
[id$="-submit"]             /* ends with stable suffix */
```

**Trade-off:** `^=` on `mat-input-` matches *every* Material input, not just email. Combine with other stable attributes:

```css
input[id^="mat-input-"][placeholder="Email"]
input[id^="mat-input-"][type="email"]
```

### 5. Technique 2: Use a Stable Neighbour as an Anchor

If the target has no stable attributes but a nearby element does (a label, a heading, a container), anchor on the neighbour and use combinators or `:has()`:

```html
<div class="form-row">
  <label>Email address</label>
  <input id="x-8821" class="css-9f3a">
</div>
```

```css
.form-row:has(label) input                   /* too loose */
```

In standard CSS you cannot match by text, which is why Playwright adds text-aware options. In Playwright:

```python
page.locator(".form-row", has_text="Email address").locator("input")
```

This is robust: the label text is a user-visible, requirement-level fact. Or use the label directly: `page.get_by_label("Email address")` (Friday).

For standard CSS, use stable attributes of the neighbour: `[data-test="email-row"] input`.

### 6. Technique 3: Exclusion with `:not()`

Sometimes you cannot say what the element *is*, but you can say what it is *not*.

```css
tr:not(.header):not(.ad-row)       /* real data rows only */
button:not([disabled])             /* actionable buttons */
li:not(.skeleton)                  /* ignore loading placeholders */
```

### 7. Technique 4: Handling Changing Counts and Order

When item order changes (search results, feeds), avoid position and select by identity:

```python
# Fragile
page.locator(".result:nth-child(1) .title")

# Robust: select by identity (a data attribute holding the item id)
page.locator('.result[data-id="SKU-1042"] .title')
```

When position *is* the thing under test (sorted list), assert on the full list rather than a single index:

```python
titles = page.locator(".result .title").all_inner_texts()
assert titles == sorted(titles)
```

### 8. Technique 5: Build Selectors from Variables

Often the dynamic part is **known by your test** (the product name, user id, order number). Build the selector from it.

```python
def product_card(page, sku: str):
    return page.locator(f'[data-sku="{sku}"]')

product_card(page, "BP-001").locator("button.add").click()
```

**Quoting rules:**

- Use an f-string. Put double quotes around attribute values inside, and use single quotes for the Python string (or vice versa).
- If the variable can contain quotes or backslashes (names such as `O'Brien`), escape or avoid string-building. Use Playwright's keyword filters such as `has_text=` which take plain strings and handle quoting for you.
- Never concatenate untrusted data into selectors for production tooling; for tests with controlled data this is fine.

**Parametrization:** combine this with `@pytest.mark.parametrize` (Tuesday) to run the same flow for many SKUs.

### 9. Technique 6: Attribute Case and Whitespace

Dynamic values may differ by case or spacing (`Login` vs `login`). Use the `i` flag: `[data-test="login" i]`. For text, Playwright's text locators are case-insensitive and whitespace-normalised by default (Friday).

### 10. Technique 7: Shadow DOM and Iframes (Awareness)

Two structures make elements look "missing" to a naive locator:

- **Open Shadow DOM:** Playwright's CSS engine **pierces open shadow roots automatically**, unlike `document.querySelector`. If your selector works in Playwright but not in the DevTools Console, shadow DOM is a likely cause.
- **Iframes:** elements inside an `<iframe>` are in a different document. You need `page.frame_locator("iframe#id").locator(...)`. We will use this in later modules; for now just recognise that "the element is in the Elements panel but my selector never finds it" can mean an iframe.

### 11. Diagnosing a Broken Locator (Debug Checklist)

When a locator fails:

1. **Count it.** `page.locator(sel).count()`. Zero means no match; more than one means ambiguity.
2. **Is it timing?** Does the element appear later? Open DevTools, trigger the action manually, and watch the DOM.
3. **Is it in an iframe or shadow DOM?**
4. **Is it hidden or covered?** Present but not visible are different problems.
5. **Is the value dynamic?** Reload the page and re-inspect; do ids or classes change?
6. **Is it environment-specific?** Different data, A/B variant, language, viewport (responsive layouts change the DOM).
7. **Minimise.** Shorten the selector step by step until it matches, to find which part breaks.

### 12. Coordinating with Developers

The most sustainable fix for dynamic selectors is a conversation. Propose to your team:

- A convention such as `data-test="<feature>-<element>"` (e.g. `login-submit`).
- Adding the attribute in the same pull request as a new UI feature.
- Treating `data-test` values as a public contract; renaming requires notifying QA.

Playwright can also be configured to use a custom attribute for `get_by_test_id()`, for instance `data-test` instead of the default `data-testid`. On Friday we will see `get_by_test_id`; the configuration is done by the `selectors.set_test_id_attribute("data-test")` call in Playwright Python.

---

## Code Examples

### Example 1: A page with dynamic values

Save as `dynamic.html`. It uses JavaScript to produce random ids on each load, simulating a real framework.

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Dynamic Practice</title></head>
<body>
  <div id="app">
    <div class="form-row" data-test="email-row">
      <label>Email address</label>
      <input type="email" placeholder="Email">
    </div>
    <div class="form-row" data-test="pass-row">
      <label>Password</label>
      <input type="password" placeholder="Password">
    </div>
    <button class="Button_primary__abc css-9x" type="submit">Pay</button>

    <ul id="results"></ul>
    <p id="toast" style="display:none">Saved!</p>
    <button id="save" type="button">Save</button>
  </div>

  <script>
    // 1. Randomise ids on every load
    document.querySelectorAll("input").forEach((el, i) => {
      el.id = "mat-input-" + Math.floor(Math.random() * 100000);
    });
    document.querySelector("button[type=submit]").className =
      "Button_primary__" + Math.random().toString(36).slice(2, 7) + " css-" + Math.random().toString(36).slice(2, 6);

    // 2. Items appear after a delay, in shuffled order
    const items = ["Alpha", "Bravo", "Charlie"].sort(() => Math.random() - 0.5);
    setTimeout(() => {
      const ul = document.getElementById("results");
      items.forEach((name, i) => {
        const li = document.createElement("li");
        li.className = "result";
        li.dataset.id = "ID-" + name.toLowerCase();
        li.innerHTML = '<span class="title">' + name + '</span>';
        ul.appendChild(li);
      });
    }, 500);

    // 3. Toast shows after clicking Save, then hides
    document.getElementById("save").addEventListener("click", () => {
      const t = document.getElementById("toast");
      setTimeout(() => { t.style.display = "block"; }, 300);
      setTimeout(() => { t.style.display = "none"; }, 2500);
    });
  </script>
</body>
</html>
```

Reload the page several times and inspect the inputs in DevTools. The ids differ each time, as do the button's class names, and the order of results differs.

### Example 2: Fragile versus robust locators

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

url = Path("dynamic.html").resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)

    # ---- FRAGILE (do NOT do this): works once, breaks on the next load
    # page.locator("#mat-input-83921").fill("a@b.com")

    # ---- ROBUST option 1: prefix + other stable attribute
    page.locator('input[id^="mat-input-"][type="email"]').fill("a@b.com")

    # ---- ROBUST option 2: stable container attribute + short path
    page.locator('[data-test="pass-row"] input').fill("secret")

    # ---- ROBUST option 3: anchor on the label text using has_text
    page.locator(".form-row", has_text="Email address").locator("input").fill("b@c.com")

    # ---- Partial class match for hashed class
    pay = page.locator('button[class*="Button_primary"]')
    print("Pay button text:", pay.inner_text())

    # ---- Wait for dynamic list, then select by identity not position
    page.wait_for_selector("li.result")                      # appears after ~500 ms
    alpha_title = page.locator('li.result[data-id="ID-alpha"] .title').inner_text()
    print("Alpha:", alpha_title)

    # ---- Order-independent assertion
    titles = page.locator("li.result .title").all_inner_texts()
    assert sorted(titles) == ["Alpha", "Bravo", "Charlie"]

    # ---- Timing: toast appears after click
    page.locator("#save").click()
    page.locator("#toast").wait_for(state="visible")
    print("Toast:", page.locator("#toast").inner_text())

    browser.close()
```

**Line-by-line explanation:**

- The first commented line shows what many beginners do: copy the id they see today. It fails tomorrow.
- `input[id^="mat-input-"][type="email"]`: *two* attribute selectors in a row mean both must match. The prefix handles the dynamic id; `type="email"` picks the right field out of the family.
- `[data-test="pass-row"] input`: anchor on a stable attribute on the container; then a descendant combinator reaches the input.
- `page.locator(".form-row", has_text="Email address")`: the second argument filters the located rows to those containing the text; `.locator("input")` then searches within the filtered row. This chaining is explored in detail on Friday.
- `button[class*="Button_primary"]`: matches the hashed class by its stable substring.
- `page.wait_for_selector("li.result")` waits up to the default timeout (30 seconds) for at least one matching element to be attached. It is an older API; you will see it in legacy code. Friday teaches the modern approach where locator actions and assertions wait automatically.
- `li.result[data-id="ID-alpha"] .title`: identity-based, immune to shuffling.
- `all_inner_texts()` returns a list in DOM order, which is random here, so we `sorted()` before comparing. The test remains deterministic despite randomness.
- `page.locator("#toast").wait_for(state="visible")` waits for the toast to be visible (it exists in the DOM the whole time but is hidden with `display:none`). This demonstrates timing versus selector issues: the selector `#toast` was fine from the beginning; the element was merely not visible.

### Example 3: Parametrized, variable-driven selectors

```python
# test_dynamic_selectors.py
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

URL = Path("dynamic.html").resolve().as_uri()

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_selector("li.result")
        yield page
        browser.close()

@pytest.mark.parametrize("name", ["Alpha", "Bravo", "Charlie"])
def test_each_result_is_present(page, name):
    data_id = f"ID-{name.lower()}"
    title = page.locator(f'li.result[data-id="{data_id}"] .title')
    assert title.count() == 1
    assert title.inner_text() == name
```

**Explanation:** `f"ID-{name.lower()}"` builds the identity from the parameter. The fixture function-scoped by default, so each test gets a fresh page and fresh random ids, which proves the selectors do not depend on random values. `title.count() == 1` guards against ambiguity.

---

## Real-World Scenarios

1. **Angular Material forms.** Fields get `mat-input-N` ids; N depends on how many inputs were rendered before. The team adds `data-test="email"` to each field, and the test suite is stable across releases.
2. **A/B testing.** Marketing runs two variants of the homepage. Selectors based on `nth-child` pass in variant A and fail in B. Selectors based on `data-test` pass in both.
3. **Localisation.** The site is tested in English and German. Text-based selectors need parametrization by locale; attribute-based selectors work unchanged.
4. **Search results.** Results change every minute. The test searches for a stable, known product and selects by `data-sku` rather than "first result".
5. **Toast notifications and spinners.** A "Saved" toast shows briefly. The test waits for the toast to become visible instead of sleeping for a guessed number of seconds.

---

## Common Mistakes

1. **Copying generated ids and long auto-generated selectors.** Check for numbers and hashes.
2. **Using `time.sleep()` to cope with dynamic content.** It slows tests and still fails when the app is slower than your guess.
3. **Over-using `*=`.** A very short substring matches too much. Prefer `^=` or `$=` when you know where the stable part sits.
4. **Fixing a timing problem with a new selector** (or vice versa).
5. **Building selectors from data containing quotes** and getting syntax errors.
6. **Selecting by position in a list that changes**, then blaming the tool for "flaky" tests.
7. **Ignoring iframes and shadow DOM.** If the element is visible but never found, check for an iframe.
8. **Forgetting responsive layouts.** A mobile viewport may render a different DOM.
9. **Not telling developers.** Selector pain is a team problem; solve it at the source with test attributes.

---

## Practice Exercises

Use `dynamic.html` and the Python scaffolding from Example 2.

**Exercise 1.** Reload `dynamic.html` three times and write down the ids of the two inputs each time. What do you notice? *Answer:* a fixed prefix `mat-input-` followed by a random number.

**Exercise 2.** Write a selector for the password input that does not use its id or any position. Give two valid options. *Solutions:* `input[type="password"]`; `[data-test="pass-row"] input`.

**Exercise 3.** Rank these selectors from most to least stable and justify.

1. `#mat-input-83921`
2. `input[id^="mat-input-"][type="email"]`
3. `[data-test="email-row"] input`
4. `div#app > div:nth-child(1) > input`

*Answer:* 3 (dedicated attribute), 2 (stable prefix + type), 4 (structure/position), 1 (random id).

**Exercise 4.** Write a function `result_title(page, name)` that returns the locator for a result's title given its name, independent of shuffling. *Hint:* use `data-id`.

**Exercise 5.** Write a PyTest test that clicks Save and asserts the toast text is `Saved!`. Use `wait_for(state="visible")` and then compare. Then add a second assertion that, after about 3 seconds, the toast is hidden again (hint: `page.locator("#toast").wait_for(state="hidden")`).

**Exercise 6.** Intentionally break it: in Example 2 replace the `page.wait_for_selector("li.result")` line with nothing, and run again. What happens when you call `.inner_text()` on `li.result[data-id="ID-alpha"] .title`? *Answer:* Playwright's locator actions auto-wait for the element to appear (up to the timeout), so it will usually still succeed; but `.count()` does **not** wait, and `all_inner_texts()` does not wait either, so the assertion on titles may fail with an empty list. Explain why in your own words. (This is a preview of Friday's auto-waiting lesson.)

**Exercise 7 (challenge).** On https://www.saucedemo.com after login, the inventory page contains products. Write a locator that finds the price of "Sauce Labs Onesie" without using position. *Hint:* find the item container, use `has_text`, then the price class. Compare your solution with a classmate's.

---

## Summary

- "Dynamic" can mean changing **attributes**, changing **structure**, or changing **timing**. Diagnose which one before fixing.
- Avoid auto-generated ids, hashed class names, and positional selectors.
- Prefer `data-test` attributes; negotiate them with developers.
- Use `^=`, `$=`, `*=` for the stable portion of partly dynamic values and combine them with other stable attributes.
- Anchor on stable neighbours, select by identity, build selectors from known data, and use exclusion with `:not()`.
- Waiting for an element to appear is a synchronisation problem; we will cover Playwright's auto-waiting in depth on Friday.
- Next: *CSS vs. XPath*, where we compare the two main selector languages and see when each is best.

---

## Additional Resources

- Playwright Python, Locators (best practices): https://playwright.dev/python/docs/locators
- Playwright Python, Best practices: https://playwright.dev/python/docs/best-practices
- MDN, Attribute selectors: https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors
