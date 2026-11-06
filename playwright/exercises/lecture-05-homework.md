# Lecture 5: Homework

**Time:** 60 minutes
**Goal:** practise reading and acting on tables, pagination, and both kinds of date picker.

## Setup

1. Copy `widgets_practice.html` from the Lecture 5 demo into your `homework/` folder.
2. Create `homework/test_lecture05_homework.py` with the starter code below. The helpers are already written for you.
3. Open `widgets_practice.html` in your browser and try each section by hand first.

**Rules:** no `sleep`; look up columns by header name (`column_index`), not by hard-coded numbers.

## Starter code

```python
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
from playwright.sync_api import Locator, Page, expect

PRACTICE_PAGE = Path(__file__).parent / "widgets_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ---------- Helpers (already done) ----------

def column_index(table: Locator, header: str) -> int:
    headers = [h.strip() for h in table.get_by_role("columnheader").all_text_contents()]
    return headers.index(header)


def column_values(table: Locator, header: str) -> list[str]:
    index = column_index(table, header)
    return [row.get_by_role("cell").nth(index).text_content()
            for row in table.locator("tbody tr").all()]


def to_number(money: str) -> int:
    """'$95,000' -> 95000"""
    return int(money.replace("$", "").replace(",", ""))


def go_to_next_page(page: Page) -> None:
    page_info = page.locator("#page-info")
    before = page_info.text_content()
    page.get_by_role("button", name="Next", exact=True).click()
    expect(page_info).not_to_have_text(before)


def pick_calendar_date(page: Page, target: date) -> None:
    page.get_by_label("Delivery date").click()
    header = page.locator("#month-year")
    target_month = target.replace(day=1)
    while True:
        shown = datetime.strptime(header.text_content(), "%B %Y").date()
        if shown == target_month:
            break
        if shown < target_month:
            page.get_by_role("button", name="Next month").click()
        else:
            page.get_by_role("button", name="Previous month").click()
    page.get_by_role("button", name=f"{target:%B} {target.day}, {target.year}", exact=True).click()


# ================= PART 1: Tables (Employees) =================

def test_01_fatima_department(store: Page):
    # TODO: Fatima Khan's Department is "HR"
    pass


def test_02_ethan_start_date(store: Page):
    # TODO: Ethan Brown's Start date is "2023-05-22"
    pass


def test_03_sales_count(store: Page):
    # TODO: exactly 2 employees are in Sales
    pass


def test_04_total_salary(store: Page):
    # TODO: the total of all salaries is 458000
    # Hint: column_values + to_number + sum()
    pass


def test_05_started_before_2021(store: Page):
    # TODO: the employees who started before 2021-01-01 are
    #       ["Ben Carter", "Chen Wei", "Fatima Khan"]
    pass


def test_06_delete_all_sales(store: Page):
    # TODO: delete EVERY Sales employee (don't hard-code their names)
    # TODO: 4 rows remain and #employee-count says "4 employees"
    # Hint: read the "delete-loop" warning in the notes
    pass


def test_07_sort_salary_descending(store: Page):
    # TODO: click the Salary header TWICE (ascending, then descending)
    # TODO: the first row is now Chen Wei
    # TODO: the salaries are in descending order
    pass


# ================= PART 2: Pagination (Orders) =================

def test_08_find_order_2008(store: Page):
    # TODO: find order 2008 (it's not on page 1)
    # TODO: its cells are ["2008", "Ben", "Cancelled", "$62.50"]
    # TODO: we're on "Page 2 of 3"
    pass


def test_09_count_pending_orders(store: Page):
    # TODO: count the "Pending" orders across ALL pages; there are 3
    pass


def test_10_previous_button(store: Page):
    # TODO: go to page 3, then click Previous
    # TODO: we're on "Page 2 of 3" and Next is enabled
    pass


# ================= PART 3: Date pickers =================

def test_11_native_birthday(store: Page):
    # TODO: set Birthday to 31 January 2001 using a Python date object
    # TODO: #birthday-summary says "Birthday: 2001-01-31"
    pass


def test_12_new_years_eve(store: Page):
    # TODO: pick 31 December 2026 in the Delivery date calendar
    # TODO: the input says "12/31/2026"
    pass


def test_13_one_week_from_today(store: Page):
    # TODO: pick the date 7 days from today
    # TODO: #delivery-summary says "Delivery: <Month> <day>, <year>"
    #       e.g. "Delivery: November 6, 2026" (no leading zero on the day)
    pass


def test_14_first_of_next_month(store: Page):
    # TODO: pick the 1st day of NEXT month
    # TODO: check the input's value (MM/DD/YYYY)
    # Hint: this must also work when you run it in December!
    pass
```

---

## Parts 1–3 (required)

Complete all 14 tests, then run:

```bash
pytest homework -v
```

All 14 should pass, today and on any other day.

**Hints:**

- Test 05: `"2019-07-01" < "2021-01-01"` works on text, because `YYYY-MM-DD` sorts correctly.
- Test 07: after each click, `expect` the first row before reading the column.
- Test 09: what goes wrong if you count straight after clicking Next?
- Test 14: what is `today.month + 1` in December?

---

## Part 4: Bonus (optional) — a live website

Create `homework/test_lecture05_bonus.py` for **https://the-internet.herokuapp.com/tables**, using the first table (`#table1`):

1. Find the person with the **highest amount due** (the "Due" column). Check it's **Jason Doe**.
2. Click the **Last Name** header to sort, and check the last names are now in alphabetical order.

*Hint:* this table's headers are `<th>` elements; use `table.locator("thead th")` to read them.

---

## Submission checklist

- [ ] `test_lecture05_homework.py`: 14 passing tests
- [ ] No hard-coded column numbers, no `sleep`
- [ ] (Optional) Part 4 bonus tests
