# Web Tables

## Learning Objectives

By the end of this lesson you will be able to:

- Describe the structure of an HTML table (`table`, `thead`, `tbody`, `tr`, `th`, `td`) and how ARIA roles (`table`, `row`, `columnheader`, `cell`) map onto it.
- Recognise "div-based" grids built from `div` elements with ARIA roles and explain why role-based locators work for both.
- Count rows and columns, read cell text, and read whole columns or rows into Python lists.
- Locate one specific row by its content (for example "the row for user Maria") using `locator.filter()` and then act on elements inside that row.
- Convert a table to Python data (a list of dictionaries) so you can assert on it with ordinary Python.
- Verify sorting, filtering, and search behaviour in table-based UIs.
- Walk through paginated tables and collect data across pages.
- Handle tables whose rows are loaded or re-rendered dynamically without introducing flaky waits.
- Avoid the most common table-testing pitfalls: positional selectors, strict mode violations, and asserting before data is loaded.

---

## Why This Matters

Tables are the workhorse of business software. Admin consoles, order lists, banking statements, audit logs, inventory screens, and reporting dashboards all present data in rows and columns. As a Quality Engineer you will constantly need to answer questions such as:

- Did the new customer appear in the list after I created them?
- Is the list sorted by "Created date" when I click the header?
- After I filter by "Status = Pending", do *all* the visible rows say Pending?
- If I delete "Order 1042", is that row really gone and are the other rows untouched?

These are exactly the kinds of checks that make up the UI portion of **Project 1 - QE Foundations**. They are also a direct application of the Week 5 epic: *complex UI interactions*. Monday's lessons taught you to operate individual controls. Today you learn to operate and verify a **collection** of controls arranged in a structured grid, where the challenge is finding "the right row" rather than "the right button".

Tables also teach a central automation idea: **locate by content and relationship, not by position.** Writing `tr[3]/td[2]` works today and breaks the moment someone inserts a row or the data is re-sorted. Locating "the row that contains 'Maria', then the Delete button in that row" survives all of those changes.

---

## The Concept

### 1. Anatomy of an HTML table

A classic HTML table looks like this:

```html
<table id="users">
  <caption>Registered users</caption>
  <thead>
    <tr>
      <th>Name</th>
      <th>Role</th>
      <th>Status</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Maria Lopez</td>
      <td>Admin</td>
      <td>Active</td>
      <td><button>Edit</button> <button>Delete</button></td>
    </tr>
    <tr>
      <td>John Smith</td>
      <td>Viewer</td>
      <td>Inactive</td>
      <td><button>Edit</button> <button>Delete</button></td>
    </tr>
  </tbody>
</table>
```

| Element | Meaning |
| --- | --- |
| `<table>` | The whole table. |
| `<caption>` | An optional title for the table. |
| `<thead>` | Group of header rows. |
| `<tbody>` | Group of data rows. |
| `<tfoot>` | Optional footer (totals, for example). |
| `<tr>` | **T**able **r**ow. |
| `<th>` | **T**able **h**eader cell (column or row header). |
| `<td>` | **T**able **d**ata cell. |

Think of a spreadsheet: `tr` is a row, `td` is a cell, `th` is a header, and the whole `table` is the sheet.

### 2. ARIA roles: the accessibility view of a table

Playwright's recommended locators (`get_by_role`) use the **accessibility tree**, which exposes semantic roles. A native table maps to:

| HTML | Role |
| --- | --- |
| `<table>` | `table` |
| `<tr>` | `row` |
| `<th>` (in a header row) | `columnheader` |
| `<th scope="row">` | `rowheader` |
| `<td>` | `cell` |

Many modern UIs (React data grids, Angular Material, AG Grid, and so on) do not use `<table>` at all. They use `<div>` elements decorated with ARIA attributes such as `role="grid"`, `role="row"`, and `role="gridcell"`. The great news is that role-based locators treat both the same way. `page.get_by_role("row")` finds `<tr>` and `<div role="row">` alike. (Note the `grid` and `gridcell` roles: a `td` inside a `role="grid"` table is a `gridcell`, not a `cell`. If `get_by_role("cell")` finds nothing in a grid, try `"gridcell"`.)

**Tip:** When in doubt about what role something has, open Chrome DevTools, select the element, and look at the **Accessibility** tab. Or use the Playwright Inspector's **Pick locator**, which suggests role-based locators.

### 3. Strategy: three levels of table locators

You can address table content at three levels. Understanding when to use each is the heart of this lesson.

1. **Whole table / whole column:** read everything and assert in bulk.
2. **One row, found by content:** `filter` the rows by text, then work with that row only.
3. **One cell, found by header and row key:** map a column name ("Status") to its position, then read that cell of a row.

#### Level 1: counting and bulk reading

```python
rows = page.get_by_role("row")           # all rows (including header)
body_rows = page.locator("table#users tbody tr")   # CSS alternative: data rows only

print(body_rows.count())                 # number of data rows right now
print(body_rows.all_inner_texts())       # list of visible text per row
print(page.locator("table#users tbody td:nth-child(1)").all_inner_texts())   # first column
```

- `locator.count()` returns the number of matches *at that instant*; it does not wait. Prefer `expect(locator).to_have_count(n)` when you need to wait for rows to appear.
- `all_inner_texts()` and `all_text_contents()` return Python lists of strings, one per matched element. Neither waits for the list to be "complete" - they snapshot whatever is there at the moment you call them. If the table loads asynchronously, assert on something that proves loading is finished *first* (for example `expect(rows).to_have_count(5)`), then read the list.
- `inner_text` reflects rendered text (respecting CSS such as `display:none`), while `text_content` returns the raw DOM text. For tables, `all_inner_texts()` is usually what a human sees.
- `td:nth-child(1)` is a CSS pseudo-class. It is 1-based: `nth-child(1)` is the first column. Contrast with Playwright's `locator.nth(i)`, which is 0-based.

#### Level 2: find a row by its content

The most important table technique in Playwright is `locator.filter()`:

```python
row = page.get_by_role("row").filter(has_text="Maria Lopez")
row.get_by_role("button", name="Delete").click()
```

- `get_by_role("row")` selects all rows.
- `.filter(has_text="Maria Lopez")` narrows to the rows that contain that text anywhere (case-insensitive substring match by default).
- `row.get_by_role("button", name="Delete")` searches *inside* that row only.

You can also filter by the presence of a child element using `has=`:

```python
row = page.get_by_role("row").filter(
    has=page.get_by_role("cell", name="Maria Lopez", exact=True)
)
```

and exclude rows with `has_not_text=` / `has_not=`. These filtering options exist on every Locator and are the cornerstone of "locate by relationship".

**Substring danger:** `has_text="Ann"` also matches "Joanna" and "Hannah". If the key could be a substring of another key, be precise:

```python
import re
row = page.get_by_role("row").filter(has_text=re.compile(r"^\s*Ann\b"))   # starts with Ann
# or
row = page.get_by_role("row").filter(has=page.get_by_role("cell", name="Ann", exact=True))
```

The second form requires a cell whose accessible name is exactly "Ann".

#### Level 3: map header names to columns

Often you want "the Status of Maria's row" without hard-coding that Status is column 3. Read the headers once, find the index, and use it:

```python
headers = page.locator("table#users thead th").all_inner_texts()
status_idx = headers.index("Status")                 # 0-based index in Python
row = page.get_by_role("row").filter(has_text="Maria Lopez")
status = row.get_by_role("cell").nth(status_idx).inner_text()
```

Because the index comes from the header, the test survives a column being added or reordered.

### 4. Turning a table into Python data

Python is excellent at data manipulation. A powerful pattern is to extract the table into a **list of dictionaries** and then use ordinary Python (list comprehensions, `sorted`, `all`, `any`) for your assertions.

```python
def read_table(table_locator):
    headers = [h.strip() for h in table_locator.locator("thead th").all_inner_texts()]
    data = []
    rows = table_locator.locator("tbody tr")
    for i in range(rows.count()):
        cells = rows.nth(i).locator("td").all_inner_texts()
        data.append(dict(zip(headers, [c.strip() for c in cells])))
    return data
```

Result:

```python
[
  {"Name": "Maria Lopez", "Role": "Admin",  "Status": "Active",   "Actions": "Edit Delete"},
  {"Name": "John Smith",  "Role": "Viewer", "Status": "Inactive", "Actions": "Edit Delete"},
]
```

Now assertions become expressive:

```python
users = read_table(page.locator("#users"))
assert all(u["Status"] == "Active" for u in users)      # filter check
assert [u["Name"] for u in users] == sorted(u["Name"] for u in users)   # sort check
```

**Performance tip:** `rows.nth(i).locator("td").all_inner_texts()` makes one round trip per row. For very large tables (hundreds of rows), you can retrieve everything in one call using `evaluate`:

```python
data = page.locator("#users").evaluate("""
  table => Array.from(table.querySelectorAll('tbody tr'))
              .map(tr => Array.from(tr.cells).map(c => c.innerText.trim()))
""")
```

That runs JavaScript in the page and returns a list of lists to Python in one go. Use it when speed matters; prefer locators when readability and auto-waiting matter.

### 5. Waiting for table data

Tables are frequently filled by an API call after the page loads. Common failure: you call `count()` before data arrives and get `0`. Remedies, best first:

1. **Assert on the outcome:** `expect(page.locator("tbody tr")).to_have_count(10)` retries until there are exactly 10 rows or it times out.
2. **Wait for a known row:** `expect(page.get_by_role("row", name="Maria Lopez")).to_be_visible()`.
3. **Wait for a loading indicator to vanish:** `expect(page.get_by_test_id("spinner")).to_be_hidden()`.
4. **Wait for the network response** that fills the table: `with page.expect_response("**/api/users*"): ...` (more on this in the *Dynamic Element Handling* and *Navigation Events* lessons).

Never use `time.sleep()`; it makes tests slow *and* flaky.

You can also assert on a list of row texts in one step; `to_have_text` accepts a list for multi-element locators and compares them in order:

```python
expect(page.locator("#users tbody td:nth-child(1)")).to_have_text(["Maria Lopez", "John Smith"])
```

If the number of elements differs or any text differs, the assertion fails (and retries until timeout).

### 6. Sorting

A sortable column header usually toggles ascending/descending on click. To test:

1. Click the header.
2. Wait for the table to update (assert something that changes, for instance the first row's text).
3. Read the column and compare to a Python-sorted copy.

```python
page.get_by_role("columnheader", name="Name").click()
names = page.locator("#users tbody td:nth-child(1)").all_inner_texts()
assert names == sorted(names)
```

**Subtleties:** sorting rules differ. Python's `sorted()` on strings is case-sensitive and uses Unicode code points ("Zed" sorts before "alice"). The UI may use locale-aware, case-insensitive sorting. Compare using the same rule: `sorted(names, key=str.lower)`. For numbers and dates, convert before comparing (`int(x)`, `datetime.strptime`), or you will sort "10" before "2" as text.

Also verify the **ARIA state** when it exists: accessible headers often have `aria-sort="ascending"`.

```python
expect(page.get_by_role("columnheader", name="Name")).to_have_attribute("aria-sort", "ascending")
```

### 7. Filtering and searching

A search box above a table typically filters rows after typing. Test pattern:

```python
page.get_by_placeholder("Search users").fill("maria")
expect(page.locator("#users tbody tr")).to_have_count(1)
expect(page.locator("#users tbody tr")).to_contain_text("Maria")
```

Also test the empty state ("No results found") and clearing the filter (`.fill("")`), because those are common bug locations.

### 8. Pagination

Large tables are split across pages. To collect everything:

```python
all_rows = []
while True:
    all_rows += page.locator("#users tbody tr").all_inner_texts()
    next_btn = page.get_by_role("button", name="Next")
    if next_btn.is_disabled():
        break
    next_btn.click()
    # wait for the table to change: see below
```

The subtle problem: after clicking Next you must **wait until the new page has rendered** before reading, otherwise you read the old rows again. Options:

- Compare to something that must change, e.g. a "Page 2 of 5" label: `expect(page.get_by_text("Page 2 of 5")).to_be_visible()`.
- Keep track of the first row's text and use `expect(first_row).not_to_have_text(previous_text)`.
- Wait for the API response that loads the next page.

A robust version:

```python
def collect_all_rows(page):
    collected = []
    body_rows = page.locator("#users tbody tr")
    while True:
        expect(body_rows.first).to_be_visible()
        collected += body_rows.all_inner_texts()
        nxt = page.get_by_role("button", name="Next")
        if nxt.is_disabled():
            return collected
        first_before = body_rows.first.inner_text()
        nxt.click()
        expect(body_rows.first).not_to_have_text(first_before)
```

Add a safety limit (`for _ in range(100):` instead of `while True`) to prevent infinite loops in case of a bug.

### 9. Row-level actions: edit, delete, select

The pattern "find row by key, then act inside the row" applies to all row actions:

```python
row = page.get_by_role("row").filter(has_text="John Smith")
row.get_by_role("checkbox").check()                 # select the row
row.get_by_role("button", name="Delete").click()    # delete it
page.get_by_role("button", name="Confirm").click()  # confirm in dialog
expect(page.get_by_role("row").filter(has_text="John Smith")).to_have_count(0)
```

Notice the last line: to prove something is gone, assert **count 0** on a locator that matches it. `to_have_count(0)` waits for removal; `to_be_hidden()` also passes if the element does not exist.

Monday's checkboxes and dialogs combine naturally here: a table row may have a checkbox (`check()`), and a delete button may open a confirm dialog (`page.on("dialog", ...)` or a modal).

### 10. Special structures

- **Merged cells (`colspan`, `rowspan`):** cell index no longer equals column index. Locate by content, not by position, or use the cell's `aria-colindex`.
- **Nested tables:** a table inside a cell. Scope to the outer row first, then the inner table.
- **Fixed headers / virtual scrolling:** the grid renders only visible rows (AG Grid, for example). `count()` returns just the rendered subset. Scroll the grid (`locator.scroll_into_view_if_needed()`, or `page.mouse.wheel`) or use the grid's own search/filter instead of iterating all rows.
- **Editable cells:** double-click to enter edit mode, type, press Enter (Monday: keyboard and mouse actions).
- **Row hover actions:** the Delete button may appear only on hover; call `row.hover()` first (also from Monday).

---

## Code Examples

The examples build their own table with `page.set_content()` so they run offline. The same code works on practice sites such as `https://the-internet.herokuapp.com/tables` (which has IDs `table1` and `table2`) or `https://demoqa.com/webtables`.

### Example 1: The sample page

```python
from playwright.sync_api import sync_playwright, expect

HTML = """
<input id="search" placeholder="Search users">
<table id="users">
  <thead>
    <tr><th>Name</th><th>Role</th><th>Status</th><th>Actions</th></tr>
  </thead>
  <tbody>
    <tr><td>Maria Lopez</td><td>Admin</td><td>Active</td>
        <td><button>Edit</button> <button class="del">Delete</button></td></tr>
    <tr><td>John Smith</td><td>Viewer</td><td>Inactive</td>
        <td><button>Edit</button> <button class="del">Delete</button></td></tr>
    <tr><td>Ann Brown</td><td>Editor</td><td>Active</td>
        <td><button>Edit</button> <button class="del">Delete</button></td></tr>
    <tr><td>Joanna Green</td><td>Viewer</td><td>Active</td>
        <td><button>Edit</button> <button class="del">Delete</button></td></tr>
  </tbody>
</table>
<script>
  // Delete: remove the row
  document.querySelectorAll('.del').forEach(b =>
    b.addEventListener('click', () => b.closest('tr').remove()));
  // Search: hide rows not matching
  document.getElementById('search').addEventListener('input', e => {
    const q = e.target.value.toLowerCase();
    document.querySelectorAll('#users tbody tr').forEach(tr => {
      tr.style.display = tr.innerText.toLowerCase().includes(q) ? '' : 'none';
    });
  });
</script>
"""
```

This is just a Python string containing HTML plus a few lines of JavaScript that make Delete and Search work like a real application. Later examples assume a `page` that has run `page.set_content(HTML)`.

### Example 2: Counting and reading

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    table = page.locator("#users")
    body_rows = table.locator("tbody tr")

    expect(body_rows).to_have_count(4)
    print(table.locator("thead th").all_inner_texts())
    # ['Name', 'Role', 'Status', 'Actions']
    print(table.locator("tbody td:nth-child(1)").all_inner_texts())
    # ['Maria Lopez', 'John Smith', 'Ann Brown', 'Joanna Green']
    print(body_rows.nth(1).locator("td").nth(2).inner_text())
    # Inactive
    print(body_rows.first.inner_text())   # 'Maria Lopez\tAdmin\tActive\tEdit Delete'
    browser.close()
```

**Line-by-line**

- `table = page.locator("#users")`: a Locator for the table element. Saving it in a variable lets us scope further searches to this table (important when a page has several).
- `body_rows = table.locator("tbody tr")`: all data rows inside the table; chained locators search only within `table`.
- `expect(body_rows).to_have_count(4)`: waits until exactly four rows are present. This also acts as a "table has finished loading" gate.
- `table.locator("thead th").all_inner_texts()`: returns a list of header strings.
- `td:nth-child(1)`: the first cell of each row (1-based CSS).
- `body_rows.nth(1)`: the second row (`nth` is 0-based). `.locator("td").nth(2)`: its third cell. `.inner_text()` reads it. "Inactive" confirms John Smith's status.
- `body_rows.first`: the first row. `inner_text()` of a whole row joins cell texts with tab characters, which is why you see `\t` characters.

### Example 3: Finding a row and acting in it

```python
    row = page.get_by_role("row").filter(has_text="John Smith")
    expect(row).to_have_count(1)                     # make sure we matched exactly one row
    row.get_by_role("button", name="Delete").click()
    expect(page.get_by_role("row").filter(has_text="John Smith")).to_have_count(0)
    expect(body_rows).to_have_count(3)
```

- `get_by_role("row")` selects every row including the header row. `.filter(has_text="John Smith")` leaves only John's row.
- `expect(row).to_have_count(1)` is a **guard**: it confirms the key is unique, so a click on the wrong row would be detected before it happens. It is optional but good practice in destructive actions.
- `row.get_by_role("button", name="Delete").click()`: the search scope is only John's row, so it cannot accidentally click another row's Delete.
- The next line re-creates the locator and asserts it matches zero elements: the row is gone.
- `expect(body_rows).to_have_count(3)`: the count dropped from four to three, and nothing else disappeared.

### Example 4: Precise matching (the "Ann" problem)

```python
import re

# "Ann" is a substring of "Joanna" => the loose filter matches 2 rows
loose = page.get_by_role("row").filter(has_text="Ann")
print(loose.count())   # 2  (Ann Brown, Joanna Green)

# Exact cell match: only the row whose Name cell is exactly "Ann Brown"
exact = page.get_by_role("row").filter(
    has=page.get_by_role("cell", name="Ann Brown", exact=True)
)
print(exact.count())   # 1

# Regex anchored to the start of the row text
anchored = page.get_by_role("row").filter(has_text=re.compile(r"^Ann\b"))
print(anchored.count())  # 1
```

- `has_text` is a substring match by default, so shorter keys can match unintended rows. This is why the count is 2.
- `get_by_role("cell", name=..., exact=True)` requires the cell's accessible name to match exactly. (`name=` for a `cell` is computed from the cell's text content.)
- `re.compile(r"^Ann\b")`: `^` anchors to the start; `\b` is a word boundary so "Anna" would not match but "Ann Brown" would. Regular expressions are passed directly to `has_text`.

### Example 5: Read a table into dictionaries and assert on data

```python
def read_table(table):
    headers = [h.strip() for h in table.locator("thead th").all_inner_texts()]
    rows = table.locator("tbody tr")
    out = []
    for i in range(rows.count()):
        cells = [c.strip() for c in rows.nth(i).locator("td").all_inner_texts()]
        out.append(dict(zip(headers, cells)))
    return out

users = read_table(page.locator("#users"))
print(users[0])
# {'Name': 'Maria Lopez', 'Role': 'Admin', 'Status': 'Active', 'Actions': 'Edit Delete'}

active = [u["Name"] for u in users if u["Status"] == "Active"]
assert "Maria Lopez" in active
assert len(active) == 3
```

**Line-by-line**

- `def read_table(table):` accepts a Locator pointing at a `<table>`.
- The first list comprehension reads every header text and removes surrounding whitespace with `.strip()`.
- `rows.count()` is the number of data rows at this moment; we assume the table has already loaded (guard with `expect(...).to_have_count(...)` before calling).
- `for i in range(rows.count()):` iterates row positions. `rows.nth(i)` addresses row `i`.
- `dict(zip(headers, cells))` pairs each header with its cell: `zip(["Name","Role"], ["Maria","Admin"])` gives `("Name","Maria"), ("Role","Admin")`, and `dict(...)` converts the pairs into `{"Name": "Maria", "Role": "Admin"}`.
- `out.append(...)` collects the dictionaries and the function returns the list.
- The assertions use plain Python on the extracted data.

### Example 6: Search and sort checks

```python
page.get_by_placeholder("Search users").fill("viewer")
visible_rows = page.locator("#users tbody tr:visible")
expect(visible_rows).to_have_count(1)
expect(visible_rows).to_contain_text("John Smith")   # note: John was deleted in Example 3 in a combined run
```

- `fill("viewer")` types into the search box and fires `input` events, which our script listens to.
- `tr:visible` is a Playwright CSS extension that matches only visible elements. It is helpful here because our fake search hides rows with `display: none` instead of removing them.
- If you are running examples separately, John Smith still exists; in a combined run he was deleted earlier. Always make each test independent by reloading the page content at the start of the test.

Sorting check on a column (assuming a clickable header):

```python
names = page.locator("#users tbody td:nth-child(1)").all_inner_texts()
assert names == sorted(names, key=str.lower), f"Not sorted: {names}"
```

- `sorted(names, key=str.lower)` sorts case-insensitively. `key=` takes a function that produces the sorting key for each item; `str.lower` is the unbound method that lower-cases a string.
- The f-string message prints the actual list if the assertion fails, which makes debugging far easier.

### Example 7: Header-driven cell access

```python
def cell(page, row_key, column_name):
    headers = [h.strip() for h in page.locator("#users thead th").all_inner_texts()]
    col = headers.index(column_name)                       # raises ValueError if missing
    row = page.get_by_role("row").filter(has_text=row_key)
    return row.get_by_role("cell").nth(col)

expect(cell(page, "Maria Lopez", "Status")).to_have_text("Active")
cell(page, "Maria Lopez", "Role").click()
```

- The function returns a **Locator**, not a string, so callers can use `expect(...)` (auto-retrying) or actions.
- `headers.index(column_name)`: Python's list `.index` returns the first position of a value; it raises `ValueError` if the header does not exist, a clear signal that the column was renamed.
- `row.get_by_role("cell").nth(col)`: the cell in the same position in that row.

### Example 8: Pagination loop (pattern)

```python
def collect_all_rows(page, max_pages=50):
    collected = []
    body_rows = page.locator("#users tbody tr")
    for _ in range(max_pages):
        expect(body_rows.first).to_be_visible()
        collected.extend(body_rows.all_inner_texts())
        nxt = page.get_by_role("button", name="Next")
        if nxt.is_disabled():
            return collected
        first_before = body_rows.first.inner_text()
        nxt.click()
        expect(body_rows.first).not_to_have_text(first_before)
    raise AssertionError("Pagination did not finish; possible infinite loop")
```

- `for _ in range(max_pages)`: `_` is the conventional name for a loop variable we do not use; the cap protects against infinite loops.
- `collected.extend(list)` adds all items of a list; `append` would add the list as a single item.
- `nxt.is_disabled()`: an immediate check (no waiting) of whether the button is disabled; on the last page the app typically disables Next.
- `expect(...).not_to_have_text(first_before)`: waits until the first row is different from before, a reliable "the page changed" signal. If page 2's first row accidentally equals page 1's, this would hang; in real data, rows are unique so it is fine. If they might not be, wait on a page-number label instead.

### Example 9: Practice site (real page)

```python
page.goto("https://the-internet.herokuapp.com/tables")
table = page.locator("#table1")
expect(table.locator("tbody tr")).to_have_count(4)

# Sort by "Last Name": click the header and verify
table.get_by_role("columnheader", name="Last Name").click()
last_names = table.locator("tbody td:nth-child(1)").all_inner_texts()
assert last_names == sorted(last_names)

# Delete link for the row with "Doe" and "Jason"
row = table.get_by_role("row").filter(has_text="Jason").filter(has_text="Doe")
row.get_by_role("link", name="delete").click()
```

- Chaining two `.filter()` calls means "has text Jason **and** has text Doe", narrowing step by step.
- On this site the header cells are `<span>` elements within `th`, and the first column is Last Name; check what is on screen when you run it, because public sites change over time.

---

## Real-World Scenarios

### Scenario 1: Admin console - create then verify

After creating a user through a form, the new user should appear in the user table. A reliable test:

```python
page.get_by_role("button", name="Add user").click()
page.get_by_label("Name").fill("Priya Nair")
page.get_by_label("Role").select_option("Editor")        # Monday: dropdowns
page.get_by_role("button", name="Save").click()

new_row = page.get_by_role("row").filter(has_text="Priya Nair")
expect(new_row).to_have_count(1)
expect(new_row).to_contain_text("Editor")
```

Notice we do not care *where* the row appears (first, last, or on page 2 after sorting); we only care that exactly one row exists with the expected content. If the table is paginated and new rows land on a later page, search for the user first.

### Scenario 2: Financial statement - totals check

A bank statement table lists transactions with a running total in a footer. Verify the sum:

```python
amounts = page.locator("#statement tbody td.amount").all_inner_texts()   # ['$10.50', '-$3.25', ...]
values = [float(a.replace("$", "").replace(",", "")) for a in amounts]
total_text = page.locator("#statement tfoot td.total").inner_text()
expected = float(total_text.replace("$", "").replace(",", ""))
assert round(sum(values), 2) == round(expected, 2)
```

Always round when comparing floating-point numbers, and strip currency symbols and thousands separators before conversion. For money in production code prefer `decimal.Decimal`; here `float` plus `round` keeps the example simple.

### Scenario 3: Filters - every visible row must match

Apply a "Status: Pending" filter and verify that **no** row violates it:

```python
page.get_by_label("Status").select_option("Pending")
rows = page.locator("#orders tbody tr")
expect(rows.first).to_be_visible()
statuses = page.locator("#orders tbody td:nth-child(4)").all_inner_texts()
assert statuses, "Expected at least one Pending order"
assert set(statuses) == {"Pending"}
```

Asserting a non-empty list matters: `all()` over an empty list is `True`, so a filter that wrongly returns nothing could otherwise pass silently.

### Scenario 4: Bulk select and delete

```python
rows = page.get_by_role("row").filter(has_text="Inactive")
for i in range(rows.count()):
    rows.nth(i).get_by_role("checkbox").check()
page.get_by_role("button", name="Delete selected").click()
expect(page.get_by_role("row").filter(has_text="Inactive")).to_have_count(0)
```

Because `rows` is a lazy locator, `rows.nth(i)` is re-resolved on each use, so the loop still works even if the DOM changes slightly. Be careful about loops that *delete* rows one at a time: the count shrinks as you go. Use `while locator.count() > 0: locator.first....click()` for that pattern.

---

## Common Pitfalls and Best Practices

1. **Positional selectors** such as `tr:nth-child(3) td:nth-child(2)` or XPath `//table/tbody/tr[3]/td[2]`. They break when data is sorted, paginated, or when rows are inserted. Locate by content.
2. **Substring matches.** `has_text="Ann"` also matches "Joanna". Use exact cell matches or anchored regular expressions when keys could overlap.
3. **Reading before the data loads.** `count()` and `all_inner_texts()` do not wait. Gate them with `expect(...).to_have_count(...)` or by waiting for a known row.
4. **Including the header row accidentally.** `get_by_role("row")` includes the header row. If you count rows, either use `tbody tr` or subtract 1 deliberately and comment why.
5. **Strict mode violations.** If a row filter matches two rows and you click inside it, Playwright raises an error instead of guessing. That is helpful; make the key unique (combine two columns with chained `filter` calls).
6. **Brittle assertions on whole-row text.** Row text includes button labels, extra whitespace, and tab separators. Assert on specific cells where possible.
7. **Assuming `td`.** Some tables use `th` for the first column (`rowheader`), or use `gridcell`. Check roles in the Accessibility tab.
8. **Comparing sorted data incorrectly.** Be explicit about case sensitivity, locale, numeric versus text, and date parsing.
9. **Infinite pagination loops.** Always include a page cap.
10. **Virtualised grids.** Only rendered rows exist in the DOM; do not assume `count()` equals total records. Use the grid's total label or scroll.
11. **Dependent tests.** Deleting "John Smith" in one test and expecting him in another makes the suite order-dependent. Each test should arrange its own data (via API setup where possible; fixtures are covered in depth on Wednesday).
12. **Over-fetching with many round trips.** For huge tables use a single `evaluate` call to pull data, but only when profiling shows you need it.

**Best practices summary:** scope with a table locator variable; locate by content and relationship; assert counts to prove loading and uniqueness; extract to dictionaries for data-heavy assertions; keep table helpers in one module so every test reuses them.

---

## Mini Practice Exercises

### Exercise 1: Warm-up counts

Using the sample page (Example 1), assert there are exactly 4 data rows and that the header texts equal `["Name", "Role", "Status", "Actions"]`.

*Hint:* `expect(locator).to_have_count()` and `expect(headers).to_have_text([...])` with a list.

<details>
<summary>Solution</summary>

```python
expect(page.locator("#users tbody tr")).to_have_count(4)
expect(page.locator("#users thead th")).to_have_text(["Name", "Role", "Status", "Actions"])
```
</details>

### Exercise 2: Find and act

Delete "Maria Lopez" and verify that the row count is now three and Maria is gone.

<details>
<summary>Solution</summary>

```python
row = page.get_by_role("row").filter(has_text="Maria Lopez")
row.get_by_role("button", name="Delete").click()
expect(row).to_have_count(0)
expect(page.locator("#users tbody tr")).to_have_count(3)
```

`row` is lazy, so after the click it re-evaluates and finds nothing; `to_have_count(0)` passes.
</details>

### Exercise 3: The "Ann" problem

Write a helper `row_for_name(page, name)` that returns the row whose first cell is **exactly** `name`. Prove it returns one row for "Ann Brown" and not two.

*Hint:* `filter(has=page.get_by_role("cell", name=name, exact=True))`.

### Exercise 4: Column extraction

Write `column(page, header)` that returns a list of all values in the column with that header text, found via the header index. Use it to assert that every Role value is one of `{"Admin", "Editor", "Viewer"}`.

*Hint:* Combine `headers.index(...)` with `td:nth-child(index + 1)`.

<details>
<summary>Solution</summary>

```python
def column(page, header):
    headers = [h.strip() for h in page.locator("#users thead th").all_inner_texts()]
    idx = headers.index(header) + 1            # CSS nth-child is 1-based
    return page.locator(f"#users tbody td:nth-child({idx})").all_inner_texts()

assert set(column(page, "Role")) <= {"Admin", "Editor", "Viewer"}
```

`<=` between sets means "is a subset of".
</details>

### Exercise 5: Search behaviour

Test the search box: typing "joanna" leaves one visible row; typing "zzz" leaves none; clearing the box brings back all four.

*Hint:* Use `tr:visible` and `to_have_count`.

### Exercise 6: Real site

On `https://the-internet.herokuapp.com/tables`, click the "Due" header of `#table1`, read the Due column (strip `$`, convert to `float`), and assert it is sorted ascending (or descending if it toggles; print what you see first, then decide).

*Hint:* `float(x.replace("$", ""))`.

### Exercise 7 (stretch): Pagination

Write your own small paginated table in `set_content` (10 rows, 3 per page, Next/Previous buttons that re-render the tbody with JavaScript). Use the pagination pattern from Example 8 to collect all rows and assert you got 10 unique rows.

---

## Summary / Key Takeaways

- Tables are rows of cells. Roles `table`, `row`, `columnheader`, `cell` (or `gridcell`) let you locate them in both native and div-based grids.
- Locate by **content and relationship**: `get_by_role("row").filter(has_text=...)`, then work inside that row. Avoid positional selectors.
- Use `count()`, `all_inner_texts()`, and `nth()` for reading, but remember they do not wait; gate them with `expect(...).to_have_count()`.
- Convert tables to lists of dictionaries to do powerful assertions in plain Python (sorting, filtering, totals).
- Map header names to column indexes so tests survive layout changes.
- For sorting, filtering, and pagination, always wait for a *change* before reading, and be exact about comparison rules.
- Prove deletion with `to_have_count(0)` and prove uniqueness with `to_have_count(1)`.
- These skills feed directly into the UI tests in **Project 1 - QE Foundations**. Wrapping table logic in reusable helpers or page objects is covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Locators (filtering, chaining, `nth`): https://playwright.dev/python/docs/locators
- Playwright Python docs, Assertions (`to_have_count`, `to_have_text` with lists): https://playwright.dev/python/docs/test-assertions
- Playwright Python API reference, Locator: https://playwright.dev/python/docs/api/class-locator
- MDN Web Docs, HTML table basics: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics
