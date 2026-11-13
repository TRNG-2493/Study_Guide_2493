# 05 — Complex Widgets: Web Tables and Date Pickers

> **Before you start**
>
> - **By the end you can:** read any table cell, find columns by header name, read a table into Python, act on rows, test sorting, search paginated tables, and pick dates in native and custom date pickers.
> - **Practice sites:**
>   - The Internet — <https://the-internet.herokuapp.com/tables> (tables)
>   - DataTables — <https://datatables.net/examples/basic_init/zero_configuration.html> (pagination)
>   - jQuery UI — <https://jqueryui.com/resources/demos/datepicker/default.html> (calendar)
> - **Create:** a folder `lecture05/` with `test_widgets.py` starting with:
>
> ```python
> from datetime import date, datetime, timedelta
> from playwright.sync_api import Page, expect
>
> TABLES = "https://the-internet.herokuapp.com/tables"
> PAGED = "https://datatables.net/examples/basic_init/zero_configuration.html"
> CALENDAR = "https://jqueryui.com/resources/demos/datepicker/default.html"
> ```
>
> - **Run tests with:** `pytest -s` (add `--headed` to watch)

---

## Topic 1 — Locating table cells

### Definition

An HTML table is made of rows (`<tr>`), header cells (`<th>`) and data cells (`<td>`). The reliable way to reach one cell is: **find the row by its content, then the cell by its column.**

### Key ideas

| HTML | Role | Locator |
|---|---|---|
| `<table id="table1">` | `table` | `page.locator("#table1")` |
| `<tr>` | `row` | `table.get_by_role("row")` — **includes the header row** |
| `<th>` | `columnheader` | `table.get_by_role("columnheader")` |
| `<td>` | `cell` | `row.get_by_role("cell")` |

- Body rows only: `table.locator("tbody tr")`.
- Don't hard-code `nth(3)` for a column — look up its index from the header text.
- CSS `nth-child` counts from **1**; Playwright `nth()` counts from **0**.

### Worked example — how much does Jason Doe owe?

**Step 1.** Find the table and count body rows:

```python
def test_read_one_cell(page: Page):
    page.goto(TABLES)
    table = page.locator("#table1")
    expect(table.locator("tbody tr")).to_have_count(4)
```

**Step 2.** Check the headers:

```python
    expect(table.get_by_role("columnheader")).to_have_text(
        ["Last Name", "First Name", "Email", "Due", "Web Site", "Action"]
    )
```

**Step 3.** Find the row, then the 4th cell:

```python
    row = table.get_by_role("row").filter(has_text="Doe")
    expect(row.get_by_role("cell").nth(3)).to_have_text("$100.00")
```

**Step 4.** Replace the hard-coded `3` with a helper (put it **above** the test):

```python
def column_index(table, header):
    headers = [h.strip() for h in table.get_by_role("columnheader").all_text_contents()]
    return headers.index(header)
```

and in the test:

```python
    due = row.get_by_role("cell").nth(column_index(table, "Due"))
    expect(due).to_have_text("$100.00")
```

> **Predict:** what does `table.get_by_role("row").count()` return — 4 or 5?

### Checkpoint

`1 passed`.

### Your turn

1. Check Frank Bach's **Email** using `column_index`.
2. Read row 3, column 4 with CSS: `#table1 tbody tr:nth-child(3) td:nth-child(4)`. Does it match Step 3?
3. Table 2 (`#table2`) has the same data with classes. Find Tim Conway's due amount there with `.dues`.

---

## Topic 2 — Reading table data into Python

### Definition

To check something about the **whole** table — totals, maximums, sort order — read the cells into Python lists or dictionaries, convert text to numbers, and use normal Python.

### Key ideas

- `all_text_contents()` returns a list of strings.
- `dict(zip(headers, cells))` turns a row into a dictionary.
- Cells are **text**: `"$9.00" > "$10.00"` is `True` as text! Convert first.
- Reading methods **don't wait** — make sure the table is ready first.

### Worked example — who owes the most?

**Step 1.** Add a helper that reads one column:

```python
def column_values(table, header):
    index = column_index(table, header)
    return [
        row.get_by_role("cell").nth(index).text_content()
        for row in table.locator("tbody tr").all()
    ]
```

**Step 2.** Read the last names:

```python
def test_highest_due(page: Page):
    page.goto(TABLES)
    table = page.locator("#table1")
    names = column_values(table, "Last Name")
    print(names)
```

**Step 3.** Read the amounts as numbers:

```python
    dues = [float(d.replace("$", "")) for d in column_values(table, "Due")]
    print(dues)
```

**Step 4.** Find who owes the most, and the total:

```python
    assert names[dues.index(max(dues))] == "Doe"
    assert sum(dues) == 251.0
```

### Checkpoint

```
['Smith', 'Bach', 'Doe', 'Conway']
[50.0, 51.0, 100.0, 50.0]
.
1 passed
```

### Your turn

1. Read the whole table into a list of dictionaries and print the first one.
   *Hint: loop over `tbody tr`, use `dict(zip(headers, cells))`.*
2. Count how many people owe exactly `$50.00`.
3. Print every email address that ends with `.com`.

### Common errors

| Error | Fix |
|---|---|
| `ValueError: could not convert string to float` | Remove `$` (and `,`) first |
| Wrong maximum | You compared text, not numbers |

---

## Topic 3 — Acting on rows and testing sorting

### Definition

When every row has the same links or buttons (edit, delete), find the **row** first, then the link inside it. To test sorting: click the header, **wait** for the table to change, then read the column and compare with Python's `sorted()`.

### Key ideas

- `row.get_by_role("link", name="edit")` — chain from the row.
- After sorting, `expect` the change **before** reading.
- On a real app, deleting rows in a loop: don't loop over `.all()` (it's a snapshot); delete `.first` in a `while` loop.

### Worked example — click a row's link, then sort

**Step 1.** Click **edit** in Frank Bach's row:

```python
def test_row_action_and_sort(page: Page):
    page.goto(TABLES)
    table = page.locator("#table1")
    bach = table.get_by_role("row").filter(has_text="Bach")
    bach.get_by_role("link", name="edit").click()
    expect(page).to_have_url(TABLES + "#edit")
```

*(On this demo the links only change the URL — nothing is really edited.)*

**Step 2.** Sort by last name and wait for the change:

```python
    table.get_by_role("columnheader", name="Last Name").click()
    expect(table.locator("tbody tr").first).to_contain_text("Bach")
```

**Step 3.** Check the order with Python:

```python
    names = column_values(table, "Last Name")
    assert names == sorted(names)
```

> **Predict:** why must Step 2's `expect` come before Step 3?

### Checkpoint

`1 passed`. In `--headed` mode the table re-orders to Bach, Conway, Doe, Smith.

### Your turn

1. Sort by **Due** and check the amounts (as numbers) are in ascending order.
2. Click the **Last Name** header a second time. What order do you get? Check it with `sorted(..., reverse=True)`.
3. Click **delete** in Tim Conway's row. Does the row disappear? What does that tell you about testing demo sites?

---

## Topic 4 — Pagination

### Definition

A paginated table shows a few rows per page with Previous/Next controls. To find a row you must check each page, and after clicking **Next** you must wait until the new page has actually loaded.

### Key ideas

- Read straight after **Next** and you may get the **old** page.
- Wait for proof: e.g. "Showing 1 to 10 of 57 entries" changes.
- On DataTables, **Next** is a `link` named "Next". On the last page it isn't truly disabled — it gets `aria-disabled="true"`, so `is_disabled()` won't work. Read the attribute instead.

### Worked example — find Zorita Serrano

**Step 1.** A helper that moves to the next page and waits:

```python
def go_to_next_page(page):
    info = page.locator("#example_info")
    before = info.text_content()
    page.get_by_role("link", name="Next").click()
    expect(info).not_to_have_text(before)
```

**Step 2.** A helper that searches every page:

```python
def find_row_on_any_page(page, text):
    table = page.locator("#example")
    while True:
        row = table.locator("tbody tr").filter(has_text=text)
        if row.count() > 0:
            return row
        if page.get_by_role("link", name="Next").get_attribute("aria-disabled") == "true":
            return None
        go_to_next_page(page)
```

**Step 3.** Use it in a test:

```python
def test_find_on_any_page(page: Page):
    page.goto(PAGED)
    row = find_row_on_any_page(page, "Zorita Serrano")
    assert row is not None
    expect(page.locator("#example_info")).to_have_text("Showing 51 to 57 of 57 entries")
```

> **Predict:** with 57 people, 10 per page, sorted by name, which page holds Zorita Serrano?

### Checkpoint

`1 passed`, and the table shows the last page.

### Your turn

1. Search for a name that doesn't exist and check the result is `None`.
2. Count the total number of rows across all pages. Does it match 57?
3. Change "entries per page" to 100 with `page.get_by_label("entries per page").select_option("100")`. How many pages are there now?

---

## Topic 5 — Native date inputs

### Definition

`<input type="date">` is the browser's built-in date picker. It looks different in each browser, but Playwright skips the pop-up: you `fill()` it with **`YYYY-MM-DD`**.

### Key ideas

- Always `YYYY-MM-DD`, whatever the browser displays.
- `date(1999, 7, 4).isoformat()` gives `"1999-07-04"`.
- Any other format → `Error: Malformed value`.
- No site needed: `page.set_content(...)` creates a quick practice page.

### Worked example — set a birthday

**Step 1.** Create a page with a date input:

```python
def test_birthday(page: Page):
    page.set_content('<label>Birthday <input type="date"></label>')
```

**Step 2.** Fill and check:

```python
    page.get_by_label("Birthday").fill("2000-12-25")
    expect(page.get_by_label("Birthday")).to_have_value("2000-12-25")
```

**Step 3.** Use a Python `date` instead:

```python
    page.get_by_label("Birthday").fill(date(1999, 7, 4).isoformat())
    expect(page.get_by_label("Birthday")).to_have_value("1999-07-04")
```

### Checkpoint

`1 passed`.

### Your turn

1. Try `fill("25/12/2000")` and read the error.
2. Fill the birthday with a date exactly 18 years ago.
   *Hint: `date.today().replace(year=...)`.*

---

## Topic 6 — Custom calendar pickers

### Definition

A custom calendar is a widget a site builds itself. You click through it like a user: open it, move to the right month, click the day, and check the value.

### Key ideas

1. Click the input to open the calendar.
2. Read the header ("November 2026") and convert it: `datetime.strptime(text, "%B %Y").date()`.
3. Click **Next** / **Prev** until it matches.
4. Click the day — use `exact=True` (otherwise "1" matches "10", "11", "21"…).
5. Use dates **relative to today**: `date.today() + timedelta(days=45)`.

| Code | Means |
|---|---|
| `%B` / `%b` / `%m` | November / Nov / 11 |
| `%d` / `%Y` | 05 / 2026 |

### Worked example — a helper to pick any date (jQuery UI)

**Step 1.** Open the calendar and read the header:

```python
def pick_calendar_date(page, target: date):
    page.locator("#datepicker").click()
    header = page.locator(".ui-datepicker-title")
    target_month = target.replace(day=1)
```

**Step 2.** Move to the right month (the arrows have `title="Next"` / `title="Prev"`):

```python
    while True:
        shown = datetime.strptime(header.text_content(), "%B %Y").date()
        if shown == target_month:
            break
        if shown < target_month:
            page.get_by_title("Next").click()
        else:
            page.get_by_title("Prev").click()
```

**Step 3.** Click the day inside the calendar:

```python
    calendar = page.locator(".ui-datepicker-calendar")
    calendar.get_by_role("link", name=str(target.day), exact=True).click()
```

**Step 4.** Use it with a date relative to today:

```python
def test_pick_date(page: Page):
    page.goto(CALENDAR)
    target = date.today() + timedelta(days=45)
    pick_calendar_date(page, target)
    expect(page.locator("#datepicker")).to_have_value(target.strftime("%m/%d/%Y"))
```

> **Predict:** why is `date(2027, 2, 14)` a bad choice for a test that will be run for years?

### Checkpoint

`1 passed`. In `--headed` mode you see the calendar move forward one or two months and the box filled as `MM/DD/YYYY`.

### Your turn

1. Pick a date 3 months **before** today. Does the helper go backwards?
2. Remove `exact=True` and pick the 1st of a month. Read the error.
3. Pick the last day of next month.
   *Hint: first day of the month after next, minus `timedelta(days=1)`.*

### Common errors

| Error | Fix |
|---|---|
| Strict mode error on a day number | Add `exact=True` |
| Test breaks next month | Use `date.today() + timedelta(...)` |
| Comparing month names as text | Convert with `datetime.strptime` |

---

## Stretch challenge

On the DataTables page, read **every** row from every page into a list of dictionaries, then check: (a) there are 57 people, (b) the names are in alphabetical order, and (c) print the person with the highest salary.

## Exit ticket

1. Why is `table.locator("tbody tr")` better than `get_by_role("row")` for counting people?
2. What must you do after clicking **Next** before reading the table?
3. What format does `fill()` need for a native date input?

## Cheat sheet

| Code | Purpose |
|---|---|
| `page.locator("#table1")` | Find a table |
| `table.locator("tbody tr")` | Body rows only |
| `table.get_by_role("columnheader").all_text_contents()` | Header texts |
| `table.get_by_role("row").filter(has_text="X")` | Row by content |
| `row.get_by_role("cell").nth(i)` | Cell by position (from 0) |
| `column_index(table, "Due")` | Column by header text |
| `float(s.replace("$", ""))` | Text → number |
| `dict(zip(headers, cells))` | Row → dictionary |
| `expect(info).not_to_have_text(before)` | Wait for page change |
| `get_attribute("aria-disabled") == "true"` | "Disabled" link-buttons |
| `page.set_content("<input type='date'>")` | Quick practice page |
| `fill("YYYY-MM-DD")` | Native date input |
| `datetime.strptime("November 2026", "%B %Y").date()` | Header → date |
| `date.today() + timedelta(days=45)` | Relative date |
| `d.strftime("%m/%d/%Y")` | Date → `MM/DD/YYYY` |
