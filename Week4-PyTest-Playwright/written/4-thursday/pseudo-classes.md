# CSS Pseudo-classes

## Learning Objectives

By the end of this lesson you will be able to:

- Define a pseudo-class and explain how it differs from a class and from a pseudo-element.
- Select elements by **position** with `:first-child`, `:last-child`, `:nth-child()`, `:nth-of-type()`, `:only-child`, and understand `an+b` formulas.
- Select elements by **state** with `:checked`, `:disabled`, `:enabled`, `:required`, `:optional`, `:focus`, `:hover`, and `:read-only`.
- Use logical pseudo-classes `:not()`, `:is()`, `:where()`, and `:has()`.
- Use Playwright's own extended pseudo-classes: `:has-text()`, `:text()`, `:text-is()`, `:visible`, `:nth-match()`, and `:right-of()` family (overview).
- Decide when a pseudo-class makes a locator more robust and when it makes it fragile.

## Why This Matters

Your weekly epic is converting manual test design into dependable automation. Manual test cases are full of *state and position* wording: "click the **first** product", "verify the **last** row", "the **checked** option", "the button that is **not disabled**". Pseudo-classes are the CSS vocabulary for exactly those phrases.

For Project 1: QE Foundations, you will need to pick items from lists and tables, check form state, and exclude noisy elements. Without pseudo-classes you would end up writing Python loops to filter lists; with them, one selector does the job and the test reads clearly.

This lesson builds on *CSS fundamentals* and *Basic and attribute selectors* from earlier today. Make sure you can already write `.class`, `#id`, and `[attr="value"]`.

---

## The Concept

### 1. What is a pseudo-class?

A **pseudo-class** is a keyword added to a selector, introduced by a single colon `:`, that selects elements **in a particular state or position** that is not expressed by their tag, id, class, or attributes.

```css
button:disabled        /* buttons in the disabled state */
li:first-child         /* list items that are first among their siblings */
input:checked          /* checkboxes/radios currently checked */
```

The word "pseudo" means "pretend". There is no real `class="first-child"` in the HTML; the browser computes that class-like status on the fly.

**Pseudo-class vs pseudo-element.** A pseudo-element uses a **double colon**, e.g. `::before`, `::after`, `::placeholder`. It targets a *part* of an element (generated content). Pseudo-elements are not elements in the DOM, so they **cannot** be located by Playwright. If you see `::before` in a selector for a test, something is wrong.

### 2. Sample HTML for this lesson

Save as `pseudo.html` and open it in Chrome.

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Pseudo-class Practice</title></head>
<body>
  <h1>Task Board</h1>

  <ul id="tasks">
    <li class="task done">Write test plan</li>
    <li class="task">Create locators</li>
    <li class="task">Run smoke tests</li>
    <li class="task done">Review report</li>
    <li class="task">Retrospective</li>
  </ul>

  <table id="results">
    <thead><tr><th>Test</th><th>Status</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>Login</td><td class="pass">PASS</td><td>1.2s</td></tr>
      <tr><td>Search</td><td class="fail">FAIL</td><td>3.4s</td></tr>
      <tr><td>Checkout</td><td class="pass">PASS</td><td>2.0s</td></tr>
      <tr><td>Logout</td><td class="pass">PASS</td><td>0.8s</td></tr>
    </tbody>
  </table>

  <form id="signup">
    <input id="email" type="email" required placeholder="Email">
    <input id="nick" type="text" placeholder="Nickname (optional)">
    <input id="agree" type="checkbox" checked>
    <input id="news" type="checkbox">
    <input id="locked" type="text" value="fixed" readonly>
    <select id="plan">
      <option>Free</option>
      <option selected>Pro</option>
      <option>Team</option>
    </select>
    <button id="go" type="submit">Sign up</button>
    <button id="cancel" type="button" disabled>Cancel</button>
  </form>

  <div class="card"><p>Intro</p><p>Details</p></div>
  <div class="card"><h3>Alone</h3></div>
</body>
</html>
```

### 3. Structural (Position) Pseudo-classes

These select by where an element sits among its **siblings** (elements with the same parent).

#### 3.1 `:first-child` and `:last-child`

```css
li:first-child     /* "Write test plan" */
li:last-child      /* "Retrospective" */
tr:first-child     /* first row inside each parent: thead's row AND tbody's first row */
```

A very common trap: `tr:first-child` matches the first `<tr>` of **each** parent (`thead` and `tbody`), so you get 2 elements, not 1. Be specific: `tbody tr:first-child`.

#### 3.2 `:nth-child(n)`

Selects the element that is the *n*th child of its parent, **counting from 1** (not 0!), and counting *all* sibling element types.

```css
li:nth-child(2)           /* "Create locators" */
tbody tr:nth-child(3)     /* the Checkout row */
tr td:nth-child(2)        /* every Status cell */
```

**Formulas (`an+b`).** The argument can be a keyword or a formula:

| Argument | Meaning | Matches in a list of 5 |
|----------|---------|------------------------|
| `3` | exactly the third | 3 |
| `odd` | 1st, 3rd, 5th... | 1, 3, 5 |
| `even` | 2nd, 4th... | 2, 4 |
| `2n` | every second | 2, 4 |
| `3n+1` | 1st, 4th, 7th... | 1, 4 |
| `n+3` | third and onward | 3, 4, 5 |
| `-n+2` | first two | 1, 2 |

Here `n` starts at 0 and counts up: 0, 1, 2, ... The browser keeps results that fall in the valid range.

#### 3.3 `:nth-last-child(n)`

Same but counting from the end. `li:nth-last-child(1)` equals `li:last-child`; `li:nth-last-child(2)` is the second to last ("Review report").

#### 3.4 `:nth-of-type(n)`, `:first-of-type`, `:last-of-type`

These count only siblings **with the same tag**. In the `.card` div, `<p>Intro</p>` and `<p>Details</p>` are both `p`. `p:nth-of-type(2)` matches "Details". If an `<h3>` were between them, `:nth-child(2)` would behave differently, but `:nth-of-type(2)` would still find the second `p`.

Rule of thumb: when a parent holds mixed tags, `:nth-of-type` is less surprising.

#### 3.5 `:only-child` and `:only-of-type`

```css
.card :only-child      /* the h3 in the second card: it is the only child */
```

#### 3.6 `:empty` and `:root`

`:empty` matches elements with no children and no text (useful to find unpopulated containers, e.g. an empty error `<div>`). `:root` is the `<html>` element.

### 4. Form-State Pseudo-classes

These reflect the **current** state of form controls (live property values, not just HTML attributes).

| Pseudo-class | Matches | In our form |
|--------------|---------|-------------|
| `:checked` | checked checkboxes/radios and selected `<option>`s | `#agree`, option "Pro" |
| `:disabled` | disabled form controls | `#cancel` |
| `:enabled` | form controls that are not disabled | all other inputs, `#go` |
| `:required` | controls with `required` | `#email` |
| `:optional` | controls without `required` | `#nick`, etc. |
| `:read-only` | readonly or non-editable | `#locked` |
| `:read-write` | editable | `#email`, `#nick` |
| `:placeholder-shown` | input currently showing its placeholder | empty `#email`, `#nick` |
| `:valid` / `:invalid` | validation state per HTML5 constraints | `#email` is `:invalid` while empty |
| `:focus` | element with keyboard focus | whichever you click |
| `:hover` | pointer is over the element | only while hovering |

**Why `:checked` beats `[checked]`.** When a user ticks a box, the HTML attribute `checked` does not change, but the `:checked` state does. Therefore use `:checked` to assert the current state.

```css
input[type="checkbox"]:checked      /* #agree initially; after clicking #news, both */
option:checked                      /* the selected option (Pro) */
```

**Note on `:hover` and `:focus`.** They are real states, but a selector using them depends on mouse position or focus at the very moment of evaluation. Use them to *verify* style states or in DevTools debugging. For triggering hover in a test, use Playwright's `hover()` method on the target instead of putting `:hover` into the locator.

### 5. Logical (Functional) Pseudo-classes

#### 5.1 `:not(selector)`

Excludes elements matching the inner selector.

```css
li.task:not(.done)                    /* tasks still open: 3 items */
input:not([type="checkbox"])          /* all non-checkbox inputs */
button:not(:disabled)                 /* only enabled buttons */
tr:not(:first-child)                  /* all rows except first-in-parent */
```

You can chain several: `input:not([readonly]):not([type="checkbox"])`. Modern browsers also accept a list inside `:not(a, b)`.

#### 5.2 `:is(list)` and `:where(list)`

Shorthand that avoids repetition.

```css
:is(h1, h2, h3)            /* any heading from the list */
#results :is(th, td)       /* every header or data cell in the table */
```

`:where()` behaves the same but with zero specificity; for locators they are equivalent, so you can treat them as one idea.

#### 5.3 `:has(selector)` ("the parent selector")

For decades CSS could not select a parent based on its children. `:has()` finally can.

```css
tr:has(td.fail)              /* the row that contains a failing cell */
div.card:has(h3)             /* the card that contains an h3 */
li:has(> a)                  /* li with a direct child link */
form:has(input:invalid)      /* form that currently has an invalid field */
```

`:has()` is available in Chrome, Edge, Safari, and Firefox in current versions, and Playwright supports it. It is extremely useful for tests: "find the *row* that contains the text 'Search', then click its button". See *Combinators* next for the "direct child" `>` marker.

### 6. Playwright's Extended Pseudo-classes

Playwright augments CSS with extra pseudo-classes that are **not part of standard CSS** and will not work in DevTools' `$$()`. They work only inside Playwright (`page.locator()`).

| Pseudo-class | Purpose | Example |
|--------------|---------|---------|
| `:has-text("text")` | Element whose text contains the string (case-insensitive substring) | `tr:has-text("Search")` |
| `:text("text")` | The smallest element containing the text | `:text("Sign up")` |
| `:text-is("text")` | Exact, case-sensitive full-text match | `button:text-is("Sign up")` |
| `:text-matches("regex", "flags")` | Regex text match | `:text-matches("^Log\\s?in$", "i")` |
| `:visible` | Only visible elements | `button:visible` |
| `:nth-match(selector, n)` | The nth overall match of a selector (1-based) | `:nth-match(.task, 3)` |
| `:right-of()`, `:left-of()`, `:above()`, `:below()`, `:near()` | Layout-based relations | `input:right-of(:text("Email"))` |

Playwright's own documentation notes that many of these are being superseded by `get_by_text`, `filter(has_text=...)`, and `locator.nth()`, which we meet on Friday. But you will see them in older code, so you should know them.

**Gotcha:** `:has-text("Search")` on `tr` selects any row whose combined text contains "Search". If you wrote only `:has-text("Search")` without a tag, an ancestor like `<table>` or even `<body>` would match too. Always attach it to a tag or class: `tr:has-text("Search")`.

### 7. Choosing between positional and descriptive selectors

Positional selectors (`:nth-child(3)`) are **brittle**. If the product team inserts a new first item, "the third" is now a different row. Prefer meaning:

| Weak | Stronger |
|------|----------|
| `tbody tr:nth-child(2)` | `tr:has(td:text-is("Search"))` |
| `li:nth-child(1)` | `li.task:has-text("test plan")` |

Use positions when position *is* the requirement ("first result is shown first", "last item should be the newest", "sort order check").

---

## Code Examples

### Example 1: DevTools Console checks (standard CSS only)

```js
$$('li.task:not(.done)').map(li => li.textContent)
// ["Create locators", "Run smoke tests", "Retrospective"]

$$('li:nth-child(odd)').map(li => li.textContent)
// ["Write test plan", "Run smoke tests", "Retrospective"]

$$('tbody tr:has(.fail)').length            // 1
$$('input:checked').map(i => i.id)           // ["agree"]
$$('button:disabled').map(b => b.id)         // ["cancel"]
$$('input:required').map(i => i.id)          // ["email"]
```

**Explanation:** each line asks the browser for all matches (`$$`), then `.map` converts element objects into plain text or ids so you can read the result easily. Try changing the state (tick the "news" checkbox) and re-run `input:checked` to see the live state.

### Example 2: Python and Playwright using pseudo-classes

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

url = Path("pseudo.html").resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)

    # 1. Position
    first_task = page.locator("#tasks li:first-child").inner_text()
    last_task = page.locator("#tasks li:last-child").inner_text()
    print("First:", first_task, "| Last:", last_task)

    # 2. nth-child formula: every even row of the results table body
    even_rows = page.locator("#results tbody tr:nth-child(even)")
    print("Even rows:", even_rows.count())        # 2

    # 3. Logical: open tasks
    open_tasks = page.locator("li.task:not(.done)")
    print("Open tasks:", open_tasks.all_inner_texts())

    # 4. Has: the failing row's test name
    failing_row = page.locator("#results tbody tr:has(td.fail)")
    print("Failing test:", failing_row.locator("td").first.inner_text())

    # 5. State: interact with a checkbox, then check live state
    print("Checked before:", page.locator("input:checked").count())    # 1 (agree)
    page.locator("#news").check()
    print("Checked after:", page.locator("input:checked").count())     # 2

    # 6. Playwright extension: has-text
    search_row_time = page.locator('tr:has-text("Search") td:last-child').inner_text()
    print("Search took:", search_row_time)                              # 3.4s

    browser.close()
```

**Line-by-line:**

- `page.locator("#tasks li:first-child")` combines an id, a descendant space (covered next lesson), a tag, and a pseudo-class.
- `.inner_text()` returns the visible text of the (single) element. If the selector matched more than one element, Playwright would raise a strict-mode error, a helpful safety net.
- `nth-child(even)` counts rows 2 and 4 in the `tbody` (Search, Logout), so `.count()` is 2.
- `.all_inner_texts()` returns a Python list of strings, one per match. We can print it directly.
- `failing_row.locator("td").first` is a **chained locator**: starting from the row, find its `td` descendants, then `.first` picks the first one (the test name). Chaining is the main subject of Friday's lessons.
- `page.locator("#news").check()` ticks the checkbox. Afterwards `input:checked` finds two elements: this shows that `:checked` reflects live state.
- `tr:has-text("Search") td:last-child` uses Playwright's `:has-text`, then drills down to the last cell of that row.

### Example 3: Replacing a position with a meaning (refactor)

```python
# Fragile: breaks if rows are re-ordered or new rows are added at the top
status = page.locator("#results tbody tr:nth-child(2) td:nth-child(2)").inner_text()

# Robust: find the row about "Search" no matter where it is
row = page.locator("#results tbody tr", has_text="Search")
status = row.locator("td").nth(1).inner_text()
```

**Explanation:** the first version says "row 2, cell 2": correct today, wrong next sprint. The second asks for the row that *contains* Search. It uses `has_text=` as a keyword parameter of `locator()`, a standard Playwright feature we will study on Friday in *Filtering and chaining locators*, and `.nth(1)` (zero-based!) for the second cell. Notice the different counting: CSS `:nth-child` starts at 1, Playwright `.nth()` starts at 0.

---

## Real-World Scenarios

1. **Latest-first sorting.** A "News" page should show the newest article on top. Your test asserts that `article:first-child time` has the greatest date. Here position is the requirement, so `:first-child` is appropriate.
2. **Pagination.** `li.page:not(.active)` finds clickable page links while ignoring the one you are on.
3. **Form readiness.** Before submitting, assert `form:has(input:invalid)` has count 0. After clearing the email field, it has count 1.
4. **Reports.** On a results dashboard, `tr:has(.fail)` immediately highlights failing rows, and a test can count them to compare with the API's number.
5. **Disabled vs hidden.** `button:disabled` vs `button:not(:visible)` (the latter being Playwright-specific) represent different bugs: a visible but locked button vs an invisible one.

---

## Common Mistakes

1. **Zero-based thinking.** CSS `:nth-child(1)` is the first. Playwright's `.nth(0)` is the first. Do not mix the two.
2. **`:nth-child` counts all element types.** In `<div><h3/><p/><p/></div>`, `p:nth-child(2)` matches the *first* `p` (it is the second child overall). Use `:nth-of-type` to count same-tag siblings.
3. **`tr:first-child` matching header rows too** when both `thead` and `tbody` exist.
4. **Using `[checked]` instead of `:checked`** for live state.
5. **Putting `:hover` in a locator** instead of calling `.hover()`.
6. **Using Playwright-only pseudo-classes in DevTools.** `:has-text()` will give a syntax error in the browser's console, because it is not CSS.
7. **Using `::before`/`::after`.** Pseudo-elements are not DOM nodes, so locators cannot target them.
8. **Unanchored `:has-text`.** Always attach to a tag so you do not match huge ancestor containers.
9. **Relying on position in dynamic lists** such as search results whose order changes.

---

## Practice Exercises

Use `pseudo.html`. Write the selector first, then verify in DevTools (standard CSS) or Playwright (extended).

**Exercise 1.** Select the third task item. *Solution:* `#tasks li:nth-child(3)` ("Run smoke tests").

**Exercise 2.** Select all rows in the table body except the last. *Hint:* combine `tbody tr` with `:not(:last-child)`. *Solution:* `tbody tr:not(:last-child)` (3 rows).

**Exercise 3.** Select every enabled button. *Solution:* `button:enabled` (only `#go`).

**Exercise 4.** Select the `<td>` with the time for the failing test using `:has()`. *Solution:* `tr:has(td.fail) td:last-child` → "3.4s".

**Exercise 5.** Predict the output of each, then run.

| Selector | Matches |
|----------|---------|
| `li:nth-child(3n+1)` | ? |
| `li:nth-child(-n+2)` | ? |
| `input:read-only` | ? |
| `.card :only-child` | ? |

*Solutions:* items 1 and 4 ("Write test plan", "Review report"); items 1 and 2; `#locked` (plus any other read-only); the `h3` in the second card (the first card has two `p`s so neither is only-child).

**Exercise 6.** Write a Playwright script that:
1. opens `pseudo.html`,
2. clicks the "news" checkbox,
3. prints how many checkboxes are checked,
4. prints the text of the selected option in `#plan` (hint: `#plan option:checked`).

*Sample solution:*

```python
page.locator("#news").check()
print(page.locator('input[type="checkbox"]:checked').count())   # 2
print(page.locator("#plan option:checked").inner_text())        # Pro
```

**Exercise 7 (challenge).** Write a PyTest parametrized test that asserts the count of `li.task:not(.done)` is 3 and `li.task.done` is 2 after loading the page.

*Hint:* reuse the module-scoped `page` fixture pattern from Example 3 of *Basic and attribute selectors* (point it at `pseudo.html`).

---

## Summary

- A **pseudo-class** (single colon) selects elements by state or position that attributes alone cannot describe; pseudo-elements (double colon) are not locatable.
- **Structural** pseudo-classes: `:first-child`, `:last-child`, `:nth-child(an+b)`, `:nth-of-type`, `:only-child`. CSS counts from 1.
- **State** pseudo-classes: `:checked`, `:disabled`, `:enabled`, `:required`, `:read-only`, `:invalid`, `:focus`, `:hover`.
- **Logical** pseudo-classes: `:not()`, `:is()`, `:where()`, `:has()`.
- **Playwright extras**: `:has-text()`, `:text()`, `:text-is()`, `:visible`, `:nth-match()`, layout selectors; these work only in Playwright.
- Prefer meaning over position unless position is the requirement.
- Next: *Combinators*, which describe relationships between elements (descendant, child, sibling).

---

## Additional Resources

- MDN, Pseudo-classes: https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-classes
- MDN, `:nth-child()`: https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child
- Playwright Python, Other locators (CSS extensions): https://playwright.dev/python/docs/other-locators
