# CSS vs. XPath

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what XPath is and how it differs from CSS selectors in purpose, syntax, and capability.
- Write basic XPath expressions: absolute vs relative paths, `//`, `/`, `*`, `.`, `..`, predicates `[...]`, and attributes with `@`.
- Use XPath functions such as `contains()`, `starts-with()`, `text()`, `normalize-space()`, `position()`, `last()`, and `not()`.
- Navigate XPath **axes**: `parent`, `ancestor`, `following-sibling`, `preceding-sibling`, `child`, `descendant`.
- Translate common selectors between CSS and XPath in both directions.
- Name the strengths and weaknesses of each language, and choose between them for a given situation.
- Test both in Chrome DevTools and in Playwright Python.

## Why This Matters

By now you can write good CSS selectors. Your weekly epic, converting manual test design into automation, will put you on teams with large existing suites, many written in Selenium-based frameworks where **XPath is extremely common**. Interviewers ask "CSS or XPath, and why?" almost every time. And there are real scenarios where CSS cannot do the job, such as finding an element by its visible text in standard syntax or navigating to a **parent** element.

For Project 1: QE Foundations, your locator catalog should record a verified selector for each important element. Knowing both languages means you can pick the sturdiest one rather than the only one you know. Importantly, **Playwright prefers neither**: its recommended built-in locators (`get_by_role`, `get_by_text`, `get_by_test_id`, introduced on Friday) are better than both. But CSS and XPath remain the universal fallback, and everyone should be fluent in them.

---

## The Concept

### 1. What is XPath?

**XPath (XML Path Language)** is a query language, standardised by the W3C, for selecting nodes in an XML document. HTML pages are (loosely) tree-structured, so browsers can evaluate XPath against the DOM. Think of it as a file-path notation for a document tree: `/html/body/div/a` is to the DOM what `/home/user/file.txt` is to a file system, with extra power for filtering.

CSS selectors were designed to **style** elements. XPath was designed to **query** a tree. That difference explains most of the contrasts below.

### 2. Sample HTML for this lesson

Save as `xpath.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>XPath Practice</title></head>
<body>
  <h1>Orders</h1>
  <table id="orders">
    <thead><tr><th>ID</th><th>Customer</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>
      <tr class="row" data-id="1001">
        <td>1001</td><td>Alice Smith</td><td class="status">Shipped</td>
        <td><a href="/orders/1001" class="view">View</a></td>
      </tr>
      <tr class="row" data-id="1002">
        <td>1002</td><td>Bob Jones</td><td class="status">Pending</td>
        <td><a href="/orders/1002" class="view">View</a></td>
      </tr>
      <tr class="row" data-id="1003">
        <td>1003</td><td>Carol White</td><td class="status">Cancelled</td>
        <td><a href="/orders/1003" class="view disabled">View</a></td>
      </tr>
    </tbody>
  </table>

  <form id="filter">
    <label for="cust">Customer</label>
    <input id="cust" name="customer" type="text" placeholder="Name">
    <label>
      <input type="checkbox" name="open"> Only open orders
    </label>
    <button type="submit" class="btn primary">Apply filter</button>
    <button type="reset" class="btn">Clear</button>
  </form>
</body>
</html>
```

### 3. XPath Syntax Basics

#### 3.1 Absolute vs. relative paths

- **Absolute path** starts with a single `/` from the document root: `/html/body/table/tbody/tr[1]/td[2]`. It is long and breaks when anything in the chain changes. **Avoid it.**
- **Relative path** starts with `//` and means "anywhere in the document": `//td`, `//button`. This is what you will use almost always.

#### 3.2 Steps: `/` versus `//`

| Symbol | Meaning | Example |
|--------|---------|---------|
| `/` | direct child (one level) | `//table/tbody` |
| `//` | descendant at any depth | `//table//a` |
| `.` | the current node | `.//a` (inside the current context) |
| `..` | the parent node | `//td[@class='status']/..` (the row) |
| `*` | any element | `//form/*` (all children of form) |
| `@` | attribute | `//@href` (the attribute nodes) |

Memorise: **`//` is the XPath equivalent of the CSS descendant space, and `/` is the equivalent of `>`.**

#### 3.3 Predicates: filters in square brackets

A predicate narrows a step.

```text
//button[@type='submit']              attribute equals value
//a[@href]                           attribute exists
//tr[3]                               third tr (1-based!)
//tr[last()]                          the last tr
//tr[position() < 3]                  first two tr's
//tr[@data-id='1002']                 attribute value
//input[@type='text' and @name='customer']     AND
//a[@class='view' or @class='edit']             OR
//input[not(@disabled)]               NOT
```

Notes:

- Indexes are **1-based**, like CSS `nth-child`, unlike Python lists.
- Use single quotes for XPath string literals inside Python strings that use double quotes (or vice versa).
- Operators: `=`, `!=`, `<`, `>`, `and`, `or`, `not()`.

#### 3.4 Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `contains(a, b)` | substring | `//a[contains(@href, 'orders')]` |
| `starts-with(a, b)` | prefix | `//input[starts-with(@id, 'mat-input-')]` |
| `ends-with` | **Not available in XPath 1.0** (browsers) | use `substring()` tricks or CSS `$=` |
| `text()` | the text node | `//button[text()='Clear']` |
| `normalize-space()` | trims and collapses whitespace | `//button[normalize-space()='Apply filter']` |
| `position()`, `last()` | position tests | `//tr[position()=last()]` |
| `not()` | negation | `//a[not(contains(@class,'disabled'))]` |
| `count()` | number of nodes | `//tr[count(td)=4]` |

**Important about class matching.** In XPath, `@class='view'` matches only when the attribute is **exactly** `view`. For `class="view disabled"` it fails. The safe pattern is:

```text
//a[contains(concat(' ', normalize-space(@class), ' '), ' view ')]
```

This surrounds the class list with spaces, so ` view ` is matched as a whole word. It is verbose; this is one place CSS (`.view`) is far nicer. A shorter but sloppier form is `contains(@class, 'view')`, which also matches `preview`.

#### 3.5 Text matching: XPath's superpower (in standard syntax)

Standard CSS cannot select by text content. XPath can:

```text
//button[text()='Clear']                      exact text of the node
//button[normalize-space()='Apply filter']    robust to whitespace
//td[contains(text(),'Smith')]                partial text
//label[contains(.,'Only open')]              '.' is the string value including children
```

Why `contains(., 'x')` can be better than `contains(text(), 'x')`: `text()` refers to the element's **own direct text nodes** (and in XPath 1.0 comparisons use the first one); if the text is split by child tags (like `<a>Hello <b>World</b></a>`), `.` (the full string value) is more reliable.

#### 3.6 Axes: moving in every direction

An **axis** says in which direction to walk from the current node. The general form is `axis::node-test[predicate]`.

| Axis | Direction | Example |
|------|-----------|---------|
| `child::` | direct children (default; `/`) | `//tr/child::td` |
| `descendant::` | any depth (like `//`) | `//table/descendant::a` |
| `parent::` | the parent (like `..`) | `//td[@class='status']/parent::tr` |
| `ancestor::` | all ancestors | `//a[@class='view']/ancestor::tr` |
| `following-sibling::` | later siblings | `//td[.='Alice Smith']/following-sibling::td[1]` |
| `preceding-sibling::` | earlier siblings | `//td[.='Shipped']/preceding-sibling::td[2]` |
| `following::` / `preceding::` | anywhere after/before in document order | rarely needed |

**This is the main reason XPath is still used:** it can go **up** (`..`, `parent::`, `ancestor::`) and **backwards** (`preceding-sibling::`), which CSS combinators cannot do (CSS gained `:has()` for some of these cases, but XPath's axes are more general).

Example: "the View link in the same row as the customer Bob Jones":

```text
//td[normalize-space()='Bob Jones']/following-sibling::td//a[@class='view']
```

or by going up and down:

```text
//td[normalize-space()='Bob Jones']/parent::tr//a
```

Reading the second: find the `td` with text Bob Jones; go to its parent `tr`; then any `a` below it.

### 4. CSS and XPath Side by Side

| Goal | CSS | XPath |
|------|-----|-------|
| By id | `#cust` | `//*[@id='cust']` |
| By class | `.view` | `//*[contains(concat(' ', normalize-space(@class), ' '), ' view ')]` |
| By tag + attribute | `input[name='customer']` | `//input[@name='customer']` |
| Starts with | `[id^='mat-']` | `//*[starts-with(@id,'mat-')]` |
| Ends with | `a[href$='.pdf']` | no direct function in 1.0; use `substring(@href, string-length(@href)-3)='.pdf'` |
| Contains | `a[href*='orders']` | `//a[contains(@href,'orders')]` |
| Direct child | `tr > td` | `//tr/td` |
| Descendant | `table a` | `//table//a` |
| Adjacent sibling | `label + input` | `//label/following-sibling::input[1]` |
| Nth child | `td:nth-child(2)` | `//td[2]` (position among same-name siblings) |
| First / last | `tr:first-child` / `tr:last-child` | `//tr[1]` / `//tr[last()]` |
| Not | `a:not(.disabled)` | `//a[not(contains(@class,'disabled'))]` |
| Has child | `tr:has(td.status)` | `//tr[td[@class='status']]` |
| By text | not in standard CSS | `//button[normalize-space()='Clear']` |
| Parent | `:has()` workaround only | `//a/..` or `//a/parent::td` |
| Previous sibling | not possible | `//td[.='x']/preceding-sibling::td` |

Subtle point: XPath's `//td[2]` means "a `td` that is the second `td` among its siblings" (for each parent), not "the second td in the document". Wrap in parentheses for the latter: `(//td)[2]`.

### 5. Comparison: Strengths and Weaknesses

| Criterion | CSS | XPath |
|-----------|-----|-------|
| **Readability** | Short, familiar to anyone who has styled a page | Verbose, especially for classes |
| **Speed** | Browsers optimise CSS heavily; typically fastest | Usually fine; can be slower on big DOMs |
| **Go to parent / backwards** | No (except `:has()`) | Yes (axes) |
| **Select by text** | Not in standard CSS (Playwright adds `:has-text`) | Yes, built in |
| **Ends-with, regex** | `$=` supported; no regex | No `ends-with` in 1.0; no regex |
| **Class matching** | Simple `.class` | Awkward |
| **Tooling** | Works in `querySelectorAll`, DevTools search, Playwright, Cypress | Works in DevTools search and `$x()`, Selenium, Playwright; not Cypress natively |
| **Learning curve** | Gentle | Steeper |
| **Maintainability** | Often better (shorter) | Long expressions are hard to read |
| **Shadow DOM** | Playwright CSS pierces open shadow roots | Playwright XPath does **not** pierce shadow roots |

**Rule of thumb:**

1. Prefer the **most stable and readable** locator, which in Playwright is often a built-in locator (Friday).
2. Of the two, use **CSS by default** for attributes, classes, and structure.
3. Use **XPath** when you need to move up or backward in the tree, select by text in a way the framework lacks, or you are working in a codebase that already uses XPath.
4. Never use absolute XPath or long positional chains from the root (`/html/body/div[2]/div[1]/...`); these are the most fragile locators there are.

### 6. Using XPath in the Browser

**DevTools Elements search:** `Ctrl+F` and type an XPath (it detects the `//` prefix). The match count shows beside the box.

**Console:**

```js
$x("//button[@type='submit']")                         // array of matching nodes
$x("//td[normalize-space()='Bob Jones']/parent::tr")   // the row
```

`$x()` is a Chrome Console helper that evaluates XPath and returns an array.

### 7. Using XPath in Playwright Python

Playwright treats a selector that starts with `//` or `..` as XPath. You can also be explicit with the `xpath=` prefix:

```python
page.locator("//button[@type='submit']")
page.locator("xpath=//button[@type='submit']")
page.locator("css=button[type='submit']")
```

You can also mix by chaining: `page.locator("#orders").locator("xpath=.//a")`. When starting an XPath from an existing locator, use `.//` (dot-slash-slash) so it searches within that element. A plain `//` always starts from the document root, escaping your chain, a common bug.

---

## Code Examples

### Example 1: DevTools checks

```js
$x("//tr[@class='row']").length                                    // 3
$x("//td[@class='status']").map(n => n.textContent)                // ["Shipped","Pending","Cancelled"]
$x("//tr[td[@class='status' and .='Pending']]/@data-id").map(a => a.value)   // ["1002"]
$x("//a[not(contains(@class,'disabled'))]").length                 // 2
$x("(//a)[last()]").map(a => a.className)                           // ["view disabled"]
```

**Explanations:**

- The third expression finds a `tr` that has a child `td` (class `status`) whose string value is `Pending`, then asks for the row's `@data-id` attribute node. Attribute nodes expose `.value`.
- `(//a)[last()]` parenthesises first, so `last()` means "last of all anchors in the document". Without parentheses `//a[last()]` would return the last `a` within *each* parent.

### Example 2: The same task in CSS, XPath, and Playwright's built-in style

Task: click the View link of Bob Jones's order.

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

url = Path("xpath.html").resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)

    # 1. XPath: walk sideways from the cell with the customer name
    xpath_link = page.locator(
        "xpath=//td[normalize-space()='Bob Jones']/following-sibling::td//a[@class='view']"
    )

    # 2. XPath: go up to the row, then down to the link
    xpath_link_2 = page.locator("xpath=//td[normalize-space()='Bob Jones']/parent::tr//a")

    # 3. CSS using Playwright's :has-text extension (no XPath needed)
    css_link = page.locator("tr:has-text('Bob Jones') a.view")

    # 4. Chaining with filter-style keyword (modern, preferred; see Friday)
    chained_link = page.locator("tr", has_text="Bob Jones").locator("a.view")

    for name, loc in [("xpath1", xpath_link), ("xpath2", xpath_link_2),
                      ("css", css_link), ("chained", chained_link)]:
        print(name, "->", loc.count(), loc.get_attribute("href"))

    browser.close()
```

**Explanation:**

1. `normalize-space()` with no argument trims the current node's string value, so the match survives accidental extra spaces or newlines in the HTML.
2. `following-sibling::td` selects the cells after the name cell in the same row; `//a[@class='view']` then finds the link inside them. Note `@class='view'` is exact: Bob's link has only `view`. Carol's link (`view disabled`) would not match; this illustrates the exact-class gotcha.
3. `parent::tr` goes up one level to the row; `//a` after it searches *below that row* (a path step after `/parent::tr` continues relative from the row, because we are still in a single expression). This is cleaner than counting cells.
4. The CSS version relies on Playwright's `:has-text()`; remember it is not standard CSS.
5. The chained version is the style we recommend long term: filter rows by text, then search inside.
6. We print the count (should be `1` for each) and the `href` attribute (`/orders/1002`). `get_attribute` requires exactly one match under strict mode.

### Example 3: Data-driven locator comparison test

```python
# test_css_vs_xpath.py
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

URL = Path("xpath.html").resolve().as_uri()

@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        pg.goto(URL)
        yield pg
        browser.close()

EQUIVALENT_PAIRS = [
    # (description, css, xpath, expected_count)
    ("rows",            "tbody tr",                  "//tbody/tr",                       3),
    ("view links",      "a.view",                    "//a[contains(@class,'view')]",     3),
    ("enabled links",   "a.view:not(.disabled)",     "//a[not(contains(@class,'disabled'))]", 2),
    ("text input",      "input[name='customer']",    "//input[@name='customer']",        1),
    ("pdf-like href",   "a[href^='/orders/']",       "//a[starts-with(@href,'/orders/')]", 3),
    ("status cells",    "td.status",                 "//td[@class='status']",            3),
]

@pytest.mark.parametrize("desc, css, xpath, expected", EQUIVALENT_PAIRS)
def test_css_and_xpath_agree(page, desc, css, xpath, expected):
    css_count = page.locator(f"css={css}").count()
    xpath_count = page.locator(f"xpath={xpath}").count()
    assert css_count == xpath_count == expected, desc
```

**Explanation:** this test proves that two different languages find the same elements. The chained comparison `a == b == c` is valid Python: it is true only if all are equal. The message after the comma (`desc`) shows which pair failed. We use `css=` and `xpath=` prefixes explicitly so intent is clear.

---

## Real-World Scenarios

1. **Legacy Selenium suite.** A bank's suite has 3,000 XPath locators. You will read them daily. Understanding axes and `normalize-space()` is what lets you maintain them.
2. **Row actions in a grid.** "Click the edit pencil on the row where Customer is Bob Jones" is classic XPath (`//td[.='Bob Jones']/following-sibling::td//button`) or Playwright filtering (`row.filter(has_text=...)`).
3. **Finding an input by its label text** in old pages without `for/id` associations: `//label[normalize-space()='Email']/following-sibling::input`. Playwright's `get_by_label()` is the modern replacement.
4. **Finding the container of an error.** The message is in a `<span>`, but the test wants the whole form-group to assert its CSS state: `//span[.='Required']/ancestor::div[contains(@class,'form-group')]`.
5. **Performance on huge pages.** A page with 50,000 DOM nodes: CSS locators evaluate faster; use them for repeated queries.

---

## Common Mistakes

1. **Absolute XPath** copied from DevTools (`/html/body/div[2]/...`). Always fragile.
2. **Exact class matching with `@class='x'`** when the element has several classes.
3. **Forgetting that XPath indexes start at 1**, and that `//td[2]` is per parent.
4. **Starting an XPath with `//` inside a chain** (it searches the whole document). Use `.//`.
5. **Using `text()=` on elements whose text is split across children or padded with whitespace.** Use `normalize-space()` or `.`.
6. **Expecting `ends-with()`** in browser XPath (it is XPath 2.0).
7. **Mixing quote styles** and creating invalid Python strings.
8. **Using XPath for everything out of habit.** CSS is shorter and faster for attributes and structure.
9. **Using either when a built-in Playwright locator exists.** For buttons, links, and labelled inputs, `get_by_role` and `get_by_label` are more readable and accessibility-aware (Friday).
10. **Assuming XPath pierces shadow DOM** in Playwright. It does not; CSS does (for open shadow roots).

---

## Practice Exercises

Use `xpath.html`. Test each in DevTools with `$x()` (XPath) or `$$()` (CSS) and then in Playwright.

**Exercise 1.** Write XPath and CSS for the "Clear" button using its attributes (not text). *Solutions:* `//button[@type='reset']` and `button[type='reset']`.

**Exercise 2.** Write an XPath for the Status cell of Alice Smith's row. *Solution:* `//td[normalize-space()='Alice Smith']/following-sibling::td[@class='status']`. Expected text: Shipped.

**Exercise 3.** Write an XPath that returns the row (`tr`) containing the text `Cancelled`. *Solutions:* `//tr[td[normalize-space()='Cancelled']]` or `//td[.='Cancelled']/parent::tr`.

**Exercise 4.** Translate to XPath: (a) `tr.row:last-child`, (b) `a:not(.disabled)`, (c) `input[type='checkbox']`. *Solutions:* (a) `//tr[@class='row'][last()]`, (b) `//a[not(contains(@class,'disabled'))]`, (c) `//input[@type='checkbox']`.

**Exercise 5.** Translate to CSS (or say it is impossible): (a) `//td[@class='status']`, (b) `//td[.='Pending']/..`, (c) `//button[text()='Clear']`. *Solutions:* (a) `td.status`; (b) not possible in standard CSS, but approximated with `tr:has(td.status)` if you can filter by something other than text; (c) not possible in standard CSS (use Playwright's `button:has-text("Clear")` or `get_by_role`).

**Exercise 6.** Explain the difference between `//a[last()]` and `(//a)[last()]`. Test both with `$x()`. *Answer:* the first returns the last `a` of every parent (three, one per row); the second returns the single last `a` in the document.

**Exercise 7.** Write the XPath for the checkbox inside the label "Only open orders" without using `name`. *Solution:* `//label[contains(.,'Only open orders')]/input[@type='checkbox']`.

**Exercise 8 (decision log).** For five elements of https://www.saucedemo.com (username, password, login button, a product title, a product price), write one CSS and one XPath locator, then circle the one you would keep, and write one sentence of justification. Bring this to your pair's locator catalog.

---

## Summary

- **CSS** selectors style and select; **XPath** queries a tree. Both can locate elements in the DOM, and Playwright supports both.
- XPath essentials: `//` (any depth), `/` (child), `@attr`, predicates `[...]`, functions (`contains`, `starts-with`, `normalize-space`, `not`), and axes (`parent::`, `following-sibling::`, `ancestor::`).
- XPath's unique abilities: select by text in standard syntax, move **up** and **backward**.
- CSS's advantages: shorter, faster, more readable for classes and attributes, shadow-DOM piercing in Playwright.
- Avoid absolute paths and positional chains in both languages.
- Use `.//` when chaining XPath from a locator.
- Playwright's built-in locators are generally preferable to both; we start using them in depth on Friday.
- Next: *Playwright architecture and setup*, where we install Playwright and run our first script.

---

## Additional Resources

- MDN, XPath: https://developer.mozilla.org/en-US/docs/Web/XPath
- MDN, XPath axes: https://developer.mozilla.org/en-US/docs/Web/XPath/Axes
- Playwright Python, Other locators (CSS and XPath): https://playwright.dev/python/docs/other-locators
