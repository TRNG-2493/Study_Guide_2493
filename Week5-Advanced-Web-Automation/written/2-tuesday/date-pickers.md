# Date Pickers

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish the three families of date inputs: native `<input type="date">` (and related types), text inputs with a mask or parser, and custom calendar widgets.
- Set a value in a native date input correctly using `fill()` with the required `YYYY-MM-DD` format, and explain why the *displayed* format differs from the *value* format.
- Drive a custom calendar widget by clicking: open it, navigate months and years, and select a day by its accessible name rather than its position.
- Write reusable helpers that select any date, including dates in other months or years, by looping with a stopping condition.
- Handle date ranges (start and end dates), disabled dates, and "today" relative dates in a way that does not break tomorrow.
- Use Python's `datetime` module to compute dates and format them for the UI.
- Control the browser's notion of "now" with Playwright's `page.clock` API so tests that depend on the current date are deterministic.
- Avoid common problems: locale/format confusion, time zones, off-by-one months, stale month views, and selecting a "day 5" from the previous or next month's overflow cells.

---

## Why This Matters

Date entry is one of the most error-prone parts of any application. Think about the bookings, deadlines, birthdays, invoices, appointments, and reports that your own life depends on: all of them depend on a date being captured and stored correctly. For a Quality Engineer, date pickers are interesting for two reasons:

1. **They are hard to automate well.** There are dozens of third-party calendar widgets, each with different markup. Some are simple `<input>` elements, others render a pop-up grid of day buttons with arrows for the previous/next month. A beginner who tries to "just click the 15th" will hit a wall within a day.
2. **They are a rich source of bugs.** Leap years, month lengths, time zones, daylight saving, locale formats (`03/04/2025` is March 4 in the US and April 3 in much of the world), min/max date constraints, and "today" relative logic are common sources of production defects.

This is squarely within the Week 5 epic, *complex UI interactions*. On Monday you handled dropdowns, keyboard and mouse actions, and auto-suggestions; a date picker uses **all** of those ideas: a popup that opens on click, navigation buttons, keyboard entry, and a list of selectable options (days). It also directly supports **Project 1 - QE Foundations**: any realistic booking or registration flow you automate will include at least one date field.

---

## The Concept

### 1. Three kinds of date pickers

Before you write a line of automation, **identify what kind of date control you face**. Right-click it, choose Inspect, and look at the markup.

#### Kind A: Native HTML date input

```html
<label for="dob">Date of birth</label>
<input type="date" id="dob" name="dob" min="1900-01-01" max="2025-12-31">
```

The browser itself draws the calendar popup. In Chrome, you see `mm/dd/yyyy` segments (in a US locale) and a calendar icon. The related input types are:

| Type | Value format | Example value |
| --- | --- | --- |
| `date` | `YYYY-MM-DD` | `2025-03-14` |
| `time` | `HH:MM` (or `HH:MM:SS`) | `14:30` |
| `datetime-local` | `YYYY-MM-DDTHH:MM` | `2025-03-14T14:30` |
| `month` | `YYYY-MM` | `2025-03` |
| `week` | `YYYY-Www` | `2025-W11` |

The crucial concept is that **the value (what is stored and submitted) is always in an ISO-like format regardless of how the browser *displays* it.** The display depends on the user's locale; the value does not. Playwright talks about the *value*, so you always use the ISO format.

You do **not** click through the browser's native calendar popup. Playwright cannot interact with that browser-drawn UI like normal DOM elements (it is not part of the page DOM). Instead you call `fill("2025-03-14")`, which sets the value and fires the right events.

#### Kind B: Text input with a mask, parser, or readonly attribute

```html
<input type="text" id="start" placeholder="DD/MM/YYYY">
```

Here the app expects typed text in a specific format, sometimes with an input mask that inserts slashes automatically, and sometimes with a library that converts text to a date on blur or Enter. Use `fill()` if the app accepts it; if a mask interferes, use `press_sequentially()` (types key by key, as you practised on Monday with keyboard actions) or select-all then type. Sometimes the field is `readonly` to force users to click the calendar; then `fill()` fails ("element is not editable") and you must use the widget.

#### Kind C: Custom calendar widget (JavaScript library)

Libraries such as flatpickr, jQuery UI Datepicker, react-datepicker, Material UI, Angular Material, Bootstrap Datepicker, and Pikaday render their own calendar in the DOM. A typical structure:

```html
<div class="calendar" role="dialog" aria-label="Choose date">
  <div class="header">
    <button aria-label="Previous month">&lt;</button>
    <span class="month-label">March 2025</span>
    <button aria-label="Next month">&gt;</button>
  </div>
  <table>
    <thead><tr><th>Mo</th> ... </tr></thead>
    <tbody>
      <tr>
        <td class="outside">24</td> ... <td><button aria-label="March 1, 2025">1</button></td> ...
      </tr>
    </tbody>
  </table>
</div>
```

Because it is regular DOM, Playwright can click it like any other element. The challenge is navigating to the correct month and choosing the correct day cell.

**Decision rule:**

1. Is it `<input type="date">` (or datetime-local, month, time)? Use `fill()` with the ISO value.
2. Is it an editable text input and typing a date works for a human? Prefer typing (`fill()`), since it is faster and less brittle than clicking a calendar. But also include at least one test that uses the calendar widget, because the click path is a separate code path that can break independently.
3. Is it readonly, or typing is not allowed? Drive the widget.

### 2. Filling native date inputs

```python
page.get_by_label("Date of birth").fill("1995-07-21")
expect(page.get_by_label("Date of birth")).to_have_value("1995-07-21")
```

Important rules:

- The string must be a valid date in `YYYY-MM-DD` form. Otherwise Playwright raises an error such as "Malformed value".
- The value must respect `min`/`max` if the page's validation relies on them; `fill()` will still set an out-of-range value, and the browser's form validation will flag it on submit. That is useful for negative tests.
- `to_have_value` reads the `value` property, not the displayed text.
- For `datetime-local` use `"2025-03-14T14:30"`. For `time` use `"14:30"`.

### 3. Typing into text-style date inputs

```python
field = page.get_by_placeholder("DD/MM/YYYY")
field.fill("14/03/2025")
field.press("Enter")          # some pickers parse on Enter or blur
```

If the library listens to `keydown`/`keyup` events and `fill()` does not trigger its logic, simulate typing:

```python
field.clear()
field.press_sequentially("14/03/2025", delay=50)   # delay in ms between keystrokes
```

`fill()` sets the value in one step and dispatches an `input` event. `press_sequentially()` presses each key, which is slower but matches what a real user triggers. (Older tutorials use `type()`, which is deprecated in favour of `press_sequentially()`.)

### 4. Driving a custom calendar

The generic algorithm for a human is:

1. Click the field to open the calendar.
2. Look at the header: which month and year is showing?
3. Click "Next" or "Previous" until the target month shows.
4. Click the target day.
5. Check that the field now shows the chosen date.

A good automation helper does exactly the same. The pieces:

**Scoping to the calendar.** The calendar is often appended at the end of `<body>` (outside your form), so find it by role or label, not by position:

```python
calendar = page.get_by_role("dialog", name="Choose date")
```

**Reading the displayed month.** Use a locator for the label and parse it with `datetime.strptime`:

```python
from datetime import datetime
label = calendar.locator(".month-label").inner_text()      # "March 2025"
shown = datetime.strptime(label, "%B %Y")                  # datetime(2025, 3, 1)
```

`%B` means the full month name (March), `%Y` the four-digit year, `%b` is the abbreviated month (Mar), `%d` the day of the month, `%m` the month as a number. The full list is in Python's `datetime` documentation.

**Deciding which direction to navigate.** Convert the month to a single comparable number: `year * 12 + month`. The difference between target and shown tells you how many clicks, and in which direction:

```python
months_diff = (target.year - shown.year) * 12 + (target.month - shown.month)
```

If `months_diff > 0` click "Next month" that many times, otherwise "Previous month" `abs(months_diff)` times. Deterministic arithmetic beats a `while` loop that compares text, but a loop with a safety limit is a good alternative when the widget's label is hard to parse.

**Selecting the day.** Prefer an accessible name or `aria-label` that includes the full date, which many widgets provide (`aria-label="March 14, 2025"`). If only the day number is available, you must exclude **overflow days** (days from the neighbouring months that fill the first and last rows of the grid). A typical technique is to exclude cells with a CSS class such as `.outside`, `.disabled`, or `.prevMonthDay`:

```python
calendar.locator("td:not(.outside) button", has_text=re.compile(r"^14$")).click()
```

Use an **exact** match for the day. `has_text="1"` matches 1, 10, 11, ... 31. Use a regular expression `^1$` or `get_by_role("button", name="1", exact=True)`.

**Verifying.** Always assert the input's value or the displayed summary after selection:

```python
expect(page.get_by_label("Check-in")).to_have_value("03/14/2025")
```

Note the *format of the display*, which may differ from the ISO value (see Section 7).

### 5. Month and year dropdowns

Many pickers add a `<select>` for month and year in the header (jQuery UI with `changeMonth`/`changeYear`, for instance). This turns a 300-click journey to a birth year such as 1960 into two actions:

```python
calendar.locator("select.ui-datepicker-year").select_option("1960")
calendar.locator("select.ui-datepicker-month").select_option(label="March")
```

You learned `select_option` for dropdowns on Monday; here it is again, applied to a calendar. Selection by `label=` (the visible text) is more readable than the numeric value (note that month values are often zero-based: January is `0`).

### 6. Date ranges, disabled dates, and constraints

- **Range pickers** (check-in/check-out) usually need two clicks in the same calendar or two separate calendars. After selecting the start, the end date's calendar often disables all days before the start. Test that: assert that an earlier day is disabled (`expect(day).to_be_disabled()`), and that selecting an end before a start is rejected.
- **Disabled dates** (weekends, past dates, fully booked days) usually have a `disabled` attribute, `aria-disabled="true"`, or a CSS class. `to_be_disabled()` understands the `disabled` attribute and `aria-disabled`; with a CSS class only, use `to_have_class(re.compile("disabled"))`.
- **Min/Max.** For native inputs, the `min` and `max` attributes can be asserted with `to_have_attribute("min", "2025-01-01")`.

### 7. Display format versus value format

An application might show `14 Mar 2025` but store `2025-03-14`. Know which one your assertion needs:

| What you check | Locator method |
| --- | --- |
| The underlying value | `to_have_value("2025-03-14")` |
| The text a user sees in a label or summary | `to_have_text("14 Mar 2025")` |
| The submitted payload | Intercept the request (`page.expect_request`) and parse the JSON |

When building the expected string from a Python `date`, use `strftime`:

```python
from datetime import date
d = date(2025, 3, 14)
d.strftime("%Y-%m-%d")   # '2025-03-14' (ISO value)
d.strftime("%d/%m/%Y")   # '14/03/2025'
d.strftime("%b %d, %Y")  # 'Mar 14, 2025'
d.isoformat()            # '2025-03-14'
```

On Linux/macOS `%-d` gives a day without a leading zero (`3` instead of `03`), but this is not portable to Windows (`%#d`). To be portable, build it yourself: `str(d.day)`.

### 8. Relative dates and "today"

Tests like "book for tomorrow" are tempting but treacherous:

- They behave differently on the last day of a month, on weekends, and on leap days.
- If tests run just before midnight, "today" can change *during* the test.
- The server may use a different time zone from the machine running the test.

Strategies:

1. **Compute dates from Python** (`date.today() + timedelta(days=7)`) and then format them. Acceptable for simple cases, but remember it uses the *machine's* local date.
2. **Use fixed dates in the future far enough away** (e.g. a specific date next year) when the exact day does not matter. Combine with `min`/`max` rules.
3. **Control the browser's clock with Playwright's `page.clock` API** (available in recent versions; see Section 9). This makes "today" a constant for the page's JavaScript, so a calendar that highlights "today" and disables past dates behaves identically every day.
4. **Seed test data on the backend** (via an API) so the application's own idea of "today" is predictable. That is outside of today's topic but is the most reliable approach for server-side rules.

### 9. Controlling time with `page.clock`

The `page.clock` API (introduced in Playwright 1.45) lets you manipulate the browser's `Date`, `setTimeout`, `setInterval`, `requestAnimationFrame`, and similar timing functions. Important methods:

- `page.clock.install(time=...)`: installs fake timers, starting at the given time. Timers will run as in real time unless you pause them.
- `page.clock.set_fixed_time(time)`: makes `Date.now()` and `new Date()` return a constant value, but timers still run normally.
- `page.clock.pause_at(time)`: jumps to the time and **pauses** the clock; timers do not fire until you advance.
- `page.clock.fast_forward(ticks)` / `page.clock.run_for(ticks)`: advance time. `ticks` is a number of milliseconds or a string such as `"01:00"` (minutes and seconds) or `"02:34:10"` (hours, minutes, seconds). `fast_forward` jumps ahead and fires due timers at most once; `run_for` fires every timer that falls inside the period, as if time had really passed.
- `page.clock.set_system_time(time)`: changes the "system" time without firing timers.

For date pickers, `set_fixed_time` is the simplest and most predictable:

```python
from datetime import datetime
page.clock.set_fixed_time(datetime(2025, 3, 14, 10, 0, 0))
page.goto("https://example.com/booking")     # the page now believes today is 14 March 2025
```

**Caveat:** this controls only the browser's JavaScript clock. A date the *server* computes ("is this date in the past?") is unaffected. Also, call `set_fixed_time` or `install` before the page's scripts read the time (before `goto`, or reload afterwards).

### 10. Time zones and locales

Playwright's browser context can emulate both:

```python
context = browser.new_context(locale="en-GB", timezone_id="Europe/London")
```

- `locale` affects how the browser formats and displays dates in native controls and `Intl` APIs. With `en-US` the native date input shows `mm/dd/yyyy`; with `en-GB` it shows `dd/mm/yyyy`. The `value` stays `YYYY-MM-DD`.
- `timezone_id` changes the time zone seen by JavaScript's `Date`. This is vital when testing a feature near midnight or a user in another zone.

Pin both in your test configuration so results do not depend on the developer's laptop settings or the CI server's region.

---

## Code Examples

All examples are self-contained. We create three pages with `set_content`: a native date input, a text-based date field, and a tiny custom calendar written for demonstration.

### Example 1: Native date input

```python
from playwright.sync_api import sync_playwright, expect

HTML = """
<label for="dob">Date of birth</label>
<input type="date" id="dob" min="1900-01-01" max="2030-12-31">
<output id="shown"></output>
<script>
  document.getElementById('dob').addEventListener('change', e => {
    document.getElementById('shown').textContent = 'You chose ' + e.target.value;
  });
</script>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(locale="en-US")
    page.set_content(HTML)

    dob = page.get_by_label("Date of birth")
    dob.fill("1995-07-21")

    expect(dob).to_have_value("1995-07-21")
    expect(page.locator("#shown")).to_have_text("You chose 1995-07-21")
    expect(dob).to_have_attribute("min", "1900-01-01")

    # Negative: an impossible date is rejected by the browser itself
    try:
        dob.fill("2025-02-30")
    except Exception as e:
        print("Rejected:", type(e).__name__)

    browser.close()
```

**Line-by-line**

- The HTML has a labelled date input and an `<output>` element updated by a `change` event listener, standing in for application logic.
- `browser.new_page(locale="en-US")`: creates a page with a fixed locale. Without it, the display depends on the machine; the value would be unaffected.
- `page.get_by_label("Date of birth")`: finds the input through its `<label for="dob">`. This is user-facing, which is what Playwright recommends.
- `dob.fill("1995-07-21")`: sets the value. Playwright validates the string format for date inputs and dispatches `input` and `change` events, so the listener runs.
- `to_have_value("1995-07-21")`: asserts the `value` property, in ISO format.
- `to_have_text("You chose 1995-07-21")`: confirms the application reacted to the change.
- `to_have_attribute("min", ...)`: shows that attributes can be asserted, e.g. to test constraints.
- The `try/except` block shows that `fill("2025-02-30")` fails; February 30 does not exist, so Playwright raises an error (a "Malformed value" message). Catching bare `Exception` is acceptable for a demonstration but in tests use `pytest.raises(...)` with a specific error class. We will see more of pytest on Wednesday; for now it is enough to know failures are exceptions.

### Example 2: Text-style date field and typing

```python
HTML = """
<label>Start date <input id="start" placeholder="DD/MM/YYYY"></label>
<p id="status"></p>
<script>
  const f = document.getElementById('start');
  f.addEventListener('blur', () => {
    const ok = /^\\d{2}\\/\\d{2}\\/\\d{4}$/.test(f.value);
    document.getElementById('status').textContent = ok ? 'valid' : 'invalid';
  });
</script>
"""
page.set_content(HTML)

start = page.get_by_placeholder("DD/MM/YYYY")
start.fill("14/03/2025")
start.blur()                      # trigger the blur handler
expect(page.locator("#status")).to_have_text("valid")

start.fill("")
start.press_sequentially("1/3/25", delay=30)
start.blur()
expect(page.locator("#status")).to_have_text("invalid")
```

- The script validates the format when the field loses focus (`blur`). The doubled backslashes (`\\d`) are needed because the HTML is inside a normal Python string; Python converts `\\d` to `\d` for the browser's regular expression.
- `get_by_placeholder` locates by placeholder text.
- `start.blur()` removes focus from the field, which triggers the handler; a human would click elsewhere or press Tab.
- `start.fill("")` clears the field. `press_sequentially("1/3/25", delay=30)` types each character with a 30 ms delay, useful for fields with masks or per-key handlers.
- The second assertion is a **negative test**: a badly formatted date must show an error. Negative tests for date fields are valuable.

### Example 3: A custom calendar and a reusable "pick date" helper

First, a miniature calendar widget. It is intentionally simple: it renders a header and a grid of day buttons with `aria-label`s that contain the full date, and it highlights nothing else. (Real widgets are more complicated, but the automation pattern is the same.)

```python
CAL_HTML = """
<label for="d">Check-in</label>
<input id="d" readonly placeholder="Select a date">
<div id="cal" role="dialog" aria-label="Choose date" hidden>
  <button id="prev" aria-label="Previous month">&lt;</button>
  <span id="title" aria-live="polite"></span>
  <button id="next" aria-label="Next month">&gt;</button>
  <div id="grid"></div>
</div>
<script>
  const months = ['January','February','March','April','May','June','July',
                  'August','September','October','November','December'];
  let view = new Date(2025, 0, 1);       // starts on January 2025
  const input = document.getElementById('d');
  const cal = document.getElementById('cal');

  function render() {
    document.getElementById('title').textContent =
      months[view.getMonth()] + ' ' + view.getFullYear();
    const grid = document.getElementById('grid');
    grid.innerHTML = '';
    const days = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
    for (let day = 1; day <= days; day++) {
      const b = document.createElement('button');
      b.textContent = day;
      b.setAttribute('aria-label',
        months[view.getMonth()] + ' ' + day + ', ' + view.getFullYear());
      b.addEventListener('click', () => {
        const mm = String(view.getMonth() + 1).padStart(2, '0');
        const dd = String(day).padStart(2, '0');
        input.value = view.getFullYear() + '-' + mm + '-' + dd;
        cal.hidden = true;
      });
      grid.appendChild(b);
    }
  }
  input.addEventListener('click', () => { cal.hidden = false; render(); });
  document.getElementById('prev').onclick = () => { view.setMonth(view.getMonth() - 1); render(); };
  document.getElementById('next').onclick = () => { view.setMonth(view.getMonth() + 1); render(); };
</script>
"""
```

The helper:

```python
from datetime import date, datetime
from playwright.sync_api import Page, expect

def pick_date(page: Page, field_label: str, target: date) -> None:
    """Open the calendar for `field_label` and select `target`."""
    page.get_by_label(field_label).click()
    calendar = page.get_by_role("dialog", name="Choose date")
    expect(calendar).to_be_visible()

    # 1) What month is displayed?
    shown = datetime.strptime(calendar.locator("#title").inner_text(), "%B %Y")

    # 2) How many months away is the target?
    diff = (target.year - shown.year) * 12 + (target.month - shown.month)

    # 3) Click Previous or Next that many times
    button_name = "Next month" if diff > 0 else "Previous month"
    for _ in range(abs(diff)):
        calendar.get_by_role("button", name=button_name).click()

    # 4) Click the day, using its full accessible name
    label = f"{target.strftime('%B')} {target.day}, {target.year}"
    calendar.get_by_role("button", name=label, exact=True).click()

    # 5) Calendar should close
    expect(calendar).to_be_hidden()
```

Using it:

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(CAL_HTML)

    pick_date(page, "Check-in", date(2025, 3, 14))
    expect(page.get_by_label("Check-in")).to_have_value("2025-03-14")

    pick_date(page, "Check-in", date(2024, 12, 5))     # navigate backwards across a year
    expect(page.get_by_label("Check-in")).to_have_value("2024-12-05")
    browser.close()
```

**Line-by-line explanation of the helper**

- `def pick_date(page: Page, field_label: str, target: date) -> None:` defines the function with type hints: `Page` is Playwright's page type, `date` is Python's `datetime.date`, and `-> None` says the function returns nothing.
- `page.get_by_label(field_label).click()`: clicks the input; in our widget this opens the calendar. The input is `readonly`, so `fill()` would not work, which is why we use the calendar.
- `page.get_by_role("dialog", name="Choose date")`: finds the calendar container via its role and accessible name (`aria-label`). Since the element starts as `hidden`, `expect(calendar).to_be_visible()` waits until the JavaScript has shown it.
- `datetime.strptime(text, "%B %Y")`: *parses* a string into a `datetime`. "March 2025" becomes `datetime(2025, 3, 1)`. (`strptime` = string parse time; `strftime` = string format time.)
- `diff = (target.year - shown.year) * 12 + (target.month - shown.month)`: counts months between the two. For January 2025 to March 2025: `0*12 + (3-1) = 2` clicks forward. For January 2025 to December 2024: `(-1)*12 + (12-1) = -1`, one click back.
- `button_name = "Next month" if diff > 0 else "Previous month"`: a Python conditional expression.
- `for _ in range(abs(diff)):` loops `abs(diff)` times; `abs` removes the sign. If `diff` is 0, the loop does nothing, which is correct.
- `calendar.get_by_role("button", name="Next month").click()`: the click is scoped to the calendar. Each click re-renders the grid; the title updates synchronously in our widget. With real widgets that animate between months, add an assertion on the title after each click, for example `expect(calendar.locator("#title")).to_have_text(...)`, to wait for the animation.
- `label = f"{target.strftime('%B')} {target.day}, {target.year}"`: builds "March 14, 2025" matching our `aria-label`. We avoid `%d` because it zero-pads (`03`).
- `get_by_role("button", name=label, exact=True)`: `exact=True` requires a full match so "March 1, 2025" cannot match "March 14, 2025". (Without `exact`, name matching is a case-insensitive substring match!)
- `expect(calendar).to_be_hidden()`: the calendar closes after selection, confirming the interaction completed.

A common improvement is to read the title **after each click** and loop until it matches the target month, with a maximum of, say, 240 clicks (20 years); that is robust if the widget skips months or the starting point is unknown.

### Example 4: Month/year dropdown pickers

```python
# jQuery-UI-style header: <select class="ui-datepicker-year"> <select class="ui-datepicker-month">
page.locator("#dob").click()
page.locator("select.ui-datepicker-year").select_option("1960")
page.locator("select.ui-datepicker-month").select_option(label="March")
page.locator("#ui-datepicker-div").get_by_role("link", name="14", exact=True).click()
```

- jQuery UI's day cells are `<a>` elements inside `<td>`, so the role is `link`, not `button`.
- `select_option("1960")` picks by option *value*; `label="March"` picks by visible text. Either works; label is easier to read.
- `exact=True` ensures that "14" does not also match "114" (unlikely) but most importantly that "1" does not match "10-19". Always use exact matching with day numbers.

### Example 5: Time control with `page.clock`

```python
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

HTML = """
<p id="today"></p>
<script>
  document.getElementById('today').textContent =
    'Today is ' + new Date().toISOString().slice(0, 10);
</script>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(timezone_id="UTC", locale="en-US")
    page = context.new_page()

    page.clock.set_fixed_time(datetime(2025, 3, 14, 10, 0, 0))
    page.set_content(HTML)

    expect(page.locator("#today")).to_have_text("Today is 2025-03-14")
    browser.close()
```

- `browser.new_context(timezone_id="UTC", locale="en-US")`: creates an isolated context with a fixed time zone and locale. This ensures `new Date()` conversions are not influenced by the machine's zone.
- `page.clock.set_fixed_time(datetime(...))`: Playwright accepts a Python `datetime`, an integer timestamp, or a string. All `Date.now()` and `new Date()` calls from now on return that moment.
- `new Date().toISOString().slice(0, 10)`: JavaScript that returns `YYYY-MM-DD`. The result is deterministic on any day of the year.
- It is called **before** the content loads: the fake time is injected into every page script that runs afterwards.

### Example 6: Range and disabled dates (assertion patterns)

```python
# Suppose start/end calendar days are buttons that become disabled before the start date
start_cal = page.get_by_role("dialog", name="Start date")
end_cal = page.get_by_role("dialog", name="End date")

expect(end_cal.get_by_role("button", name="March 10, 2025", exact=True)).to_be_disabled()
expect(end_cal.get_by_role("button", name="March 20, 2025", exact=True)).to_be_enabled()
```

- `to_be_disabled` passes for the HTML `disabled` attribute and for `aria-disabled="true"`.
- If the widget uses only a CSS class, assert it with `to_have_class(re.compile(r"\bdisabled\b"))`.

---

## Real-World Scenarios

### Scenario 1: Hotel booking

A booking form has Check-in, Check-out, and a rule that the minimum stay is one night. Your tests:

1. Happy path: check-in 14 March, check-out 16 March; the summary says "2 nights".
2. Boundary: check-out equal to check-in is rejected.
3. Rule: check-out before check-in is not selectable (disabled).
4. Past dates: yesterday is disabled (use `page.clock` to fix "today").
5. Leap-year boundary: check-in 28 February 2028, check-out 1 March 2028 gives 2 nights; the same dates in 2027 give 1 night.

```python
from datetime import date

def test_leap_year_nights(page):
    page.goto("/booking")
    pick_date(page, "Check-in", date(2028, 2, 28))
    pick_date(page, "Check-out", date(2028, 3, 1))
    expect(page.get_by_test_id("nights")).to_have_text("2 nights")
```

Computing the expected nights in Python (`(date(2028,3,1) - date(2028,2,28)).days`) gives you an independent oracle rather than a hard-coded number.

### Scenario 2: Date of birth for an age rule

A sign-up form blocks users under 18. Using a fixed clock, you can test the boundary precisely:

```python
page.clock.set_fixed_time(datetime(2025, 3, 14, 12, 0, 0))
page.goto("/signup")
page.get_by_label("Date of birth").fill("2007-03-14")        # turns 18 today
expect(page.get_by_text("You must be at least 18")).to_be_hidden()
page.get_by_label("Date of birth").fill("2007-03-15")        # turns 18 tomorrow
expect(page.get_by_text("You must be at least 18")).to_be_visible()
```

Boundary-value analysis (testing the day before, the day of, and the day after a rule) is one of the most valuable testing techniques you can apply to dates.

### Scenario 3: Reports with a date range

An analytics dashboard has a "Last 30 days" preset and a custom range. Verify the table respects the range: select 1-7 March, read the "Date" column, and assert every date falls inside.

```python
dates = page.locator("#report tbody td:nth-child(1)").all_inner_texts()
parsed = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
assert parsed, "report is empty"
assert all(date(2025, 3, 1) <= d <= date(2025, 3, 7) for d in parsed)
```

This reuses the web-table skills from earlier today, and the Python chained comparison `a <= d <= b` reads like mathematics.

### Scenario 4: Time zones

A scheduling app shows an appointment at 09:00 for a London user but 04:00 for a New York user. Create two contexts with different `timezone_id`s and compare the displayed time in each:

```python
london = browser.new_context(timezone_id="Europe/London")
newyork = browser.new_context(timezone_id="America/New_York")
```

---

## Common Pitfalls and Best Practices

1. **Using a wrong format for native inputs.** `fill("03/14/2025")` on `<input type="date">` fails. Use `YYYY-MM-DD`.
2. **Trying to click the native browser popup.** It is not in the page DOM; use `fill()`.
3. **Clicking day numbers without scoping or exact matching.** You will click the wrong "1" or an overflow day. Use `exact=True`, an anchored regex, or a full-date `aria-label`, and exclude overflow classes.
4. **Not waiting for month transitions.** Animated widgets re-render; assert the title after each navigation click.
5. **Hard-coded relative expectations.** "Tomorrow" tests flake at month boundaries and midnight. Fix the clock or compute expectations from the same source of truth.
6. **Ignoring locale and time zone.** Pin `locale` and `timezone_id` for deterministic results.
7. **Zero-based months.** JavaScript `Date` months are 0-11; some `<option value>` lists are zero-based. Python's `date.month` is 1-12. Mixing them causes off-by-one bugs.
8. **Overlooking readonly inputs.** If `fill()` complains the element is not editable, the app wants clicking.
9. **Only testing typed input, or only the widget.** The two paths are separate code; cover both at least once.
10. **No negative tests.** Test invalid dates, out-of-range dates, wrong formats, and reversed ranges.
11. **Forgetting that `page.clock` only affects the browser.** Server-side validation may still use the real date.
12. **Duplicating the picker logic in every test.** Put it in one helper (later: a page-object component, introduced on Wednesday).

**Best practices:** identify the control type first; prefer `fill()` for native and text inputs; use a single `pick_date` helper for custom widgets; assert both the input value and the visible summary; pin the clock, locale, and time zone; add boundary and negative tests.

---

## Mini Practice Exercises

### Exercise 1: Native date

Create a page with `<input type="date" id="appt">`. Fill it with `2025-12-31` and assert the value. Then set `min="2025-01-01"` via HTML and assert the attribute.

<details>
<summary>Solution</summary>

```python
page.set_content('<label>Appointment <input type="date" id="appt" min="2025-01-01"></label>')
f = page.get_by_label("Appointment")
f.fill("2025-12-31")
expect(f).to_have_value("2025-12-31")
expect(f).to_have_attribute("min", "2025-01-01")
```
</details>

### Exercise 2: Datetime-local

Fill a `datetime-local` input with 14 March 2025 at 14:30 and verify. *Hint:* the format has a `T` between date and time.

<details>
<summary>Solution</summary>

```python
page.set_content('<label>When <input type="datetime-local"></label>')
w = page.get_by_label("When")
w.fill("2025-03-14T14:30")
expect(w).to_have_value("2025-03-14T14:30")
```
</details>

### Exercise 3: Use the helper

Using `CAL_HTML` and `pick_date`, select 29 February 2028 and verify `2028-02-29`. Then select 31 January 2025 in a fresh page. Explain what the navigation arithmetic does in each case.

*Hint:* the widget starts at January 2025. For February 2028 the difference is `(2028-2025)*12 + (2-1) = 37` clicks on Next; for 31 January 2025 it is 0, so the loop does nothing. Both must work. Also notice why the widget keeps `view` on the 1st of the month: calling `setMonth` while the date is the 31st could overflow into the following month.

### Exercise 4: Negative path

Extend the helper into `pick_date_or_fail(...)` that raises `AssertionError` with a clear message if the target day button does not exist or is disabled. Test with the invalid day `date(2025, 2, 29)` (which Python's `date` itself refuses, so catch `ValueError` and discuss where date validity should be checked).

*Hint:* Python raises `ValueError: day is out of range for month` when you construct that `date`, before Playwright is involved.

### Exercise 5: Controlled clock

Write a page that shows "Weekend" or "Weekday" based on `new Date().getDay()`. Use `page.clock.set_fixed_time()` to prove Saturday 15 March 2025 gives "Weekend" and Monday 17 March 2025 gives "Weekday".

<details>
<summary>Solution</summary>

```python
HTML = "<p id='k'></p><script>const d=new Date().getDay();document.getElementById('k').textContent=(d===0||d===6)?'Weekend':'Weekday'</script>"
for when, expected in [(datetime(2025,3,15,12), "Weekend"), (datetime(2025,3,17,12), "Weekday")]:
    page = browser.new_context(timezone_id="UTC").new_page()
    page.clock.set_fixed_time(when)
    page.set_content(HTML)
    expect(page.locator("#k")).to_have_text(expected)
```
</details>

### Exercise 6: Real widgets (stretch)

On `https://demoqa.com/date-picker` (or any jQuery UI datepicker demo such as `https://jqueryui.com/datepicker/`, which lives inside an iframe: use today's frame lesson!), write a helper that selects 14 March 2025 and verifies the field. Record which of the three picker kinds each field uses.

---

## Summary / Key Takeaways

- Identify the control first: native (`type="date"`), text/masked, or custom widget.
- Native inputs: `fill("YYYY-MM-DD")` (ISO value), never click the browser popup. `datetime-local` uses `YYYY-MM-DDTHH:MM`.
- Text inputs: `fill()`, or `press_sequentially()` when key events matter; trigger blur/Enter if the app parses then.
- Custom calendars: scope to the calendar, compute the month difference with arithmetic, click Next/Previous, then click the day by full `aria-label` or an exact match, excluding overflow days.
- Use `datetime.strptime` to parse displayed text and `strftime`/`isoformat` to build expected text.
- Make time deterministic with `page.clock.set_fixed_time(...)`, and pin `locale` and `timezone_id` on the context.
- Test boundaries (leap years, month ends, age limits), disabled dates, and negative inputs.
- Date helpers belong in one reusable place; structuring that code as page objects is covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Clock (`page.clock`): https://playwright.dev/python/docs/clock
- Playwright Python docs, Emulation (locale, timezone): https://playwright.dev/python/docs/emulation
- Playwright Python API reference, Locator `fill`: https://playwright.dev/python/docs/api/class-locator#locator-fill
- MDN Web Docs, `<input type="date">`: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
- Python docs, `datetime` (strftime/strptime codes): https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
