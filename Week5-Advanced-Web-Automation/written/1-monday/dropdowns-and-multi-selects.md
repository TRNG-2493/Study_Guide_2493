# Dropdowns and Multi-Selects

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish a native HTML `<select>` dropdown from a custom (JavaScript-built) dropdown, and explain why each needs a different technique.
- Select options in a native dropdown using `select_option()` by **value**, by **label** (visible text) and by **index**.
- Select **several** options at once in a `<select multiple>` list, clear a selection, and read what is currently selected.
- Assert on selected values with `expect(...).to_have_value()` and `expect(...).to_have_values()`, and on the list of available options with `to_have_text()`.
- Work with option groups (`<optgroup>`), placeholder options, and disabled options.
- Automate custom dropdowns (React/Angular/Material style) with `click()` plus `get_by_role("option")`.
- Handle searchable dropdowns, dependent dropdowns (country then state), and the timing issues that come with them.
- Write maintainable tests that avoid hard-coded indexes and unnecessary sleeps.

---

## Why This Matters

This week's epic is about mastering complex UI interactions. Dropdowns are among the most common input controls in business software: country, state, time zone, currency, product category, priority, status, role. A registration form without at least one dropdown is rare. In the **Project 1: QE Foundations** UI milestone you will automate a complex form flow, and you will almost certainly have to choose a country, pick a date part, or select a category.

Dropdowns are also a classic place where beginners lose time, for two reasons:

1. **There are two very different kinds.** The native `<select>` element gets special, powerful support from Playwright (`select_option`). But most modern design systems replace it with a custom component made of `<div>`s and `<li>`s. Calling `select_option` on those fails with an error, and you must use ordinary click actions instead. Recognising which kind you face is the first and most important skill.

2. **Dropdowns hide data.** The options are often hidden until opened, loaded from a server, filtered by typing, or dependent on a previous choice. That makes timing and verification more subtle than for a text box.

By the end of the lesson you will approach any dropdown with a clear decision process.

---

## The Concept

### 1. Anatomy of a native dropdown

A native dropdown is written in HTML like this:

```html
<label for="country">Country</label>
<select id="country" name="country">
  <option value="">-- Please choose --</option>
  <option value="us">United States</option>
  <option value="ca">Canada</option>
  <option value="in" disabled>India (coming soon)</option>
</select>
```

Terminology:

- `<select>` is the container, the control the user interacts with.
- `<option>` elements are the choices. Each has **visible text** (what the user reads: "United States") and, optionally, a **value** attribute (what is sent to the server: `us`). If there is no `value` attribute, the browser uses the text as the value.
- The first option is often a **placeholder** (`value=""`) that prompts the user to choose. Validation commonly rejects the empty value.
- `disabled` options cannot be selected.
- `<optgroup label="Europe">` groups options under a heading.
- Adding the attribute `multiple` turns it into a **multi-select list box**, where several options can be highlighted at once (users hold Ctrl or Cmd to select more than one).

Here is a key insight: **the visible text and the value can differ**, and tests must decide which they care about. Users see the *label*; the back-end receives the *value*. A test that selects by label mirrors the user, a test that selects by value is more stable if wording is edited or translated.

### 2. Playwright's `select_option()`

The method to use on a native `<select>` is:

```python
page.locator("#country").select_option("us")
```

This is more than a click. Playwright:

1. Waits for the `<select>` to be visible and enabled (actionability).
2. Looks for options that match what you asked for.
3. Sets them as selected.
4. Dispatches the `input` and `change` events, so that the page's JavaScript reacts as it would for a real user.
5. Returns a list of the values that are now selected.

It does **not** open the dropdown or click individual options; the operating system draws native option lists in a way automation cannot reliably click. `select_option` is the officially supported, reliable alternative.

You can tell Playwright *how* to match in several ways:

```python
select = page.locator("#country")

select.select_option("us")                    # a string: matches by value, or by label if no value matches
select.select_option(value="us")              # explicitly by value attribute
select.select_option(label="United States")   # explicitly by visible text
select.select_option(index=1)                 # by position (zero-based)
```

**Be explicit.** The plain string form first tries the value and then the label; it works, but a reader cannot tell what you meant. The keyword forms `value=`, `label=` and `index=` document intent and avoid accidental matches.

| Match by | When to prefer it | Risk |
|---|---|---|
| `value=` | Stable identifiers (`us`, `P1`) used by the back-end | Not what the user sees; values might be opaque ids |
| `label=` | Mirrors the user's experience; readable tests | Breaks if wording or translation changes |
| `index=` | Quick demos; "pick any option that is not the placeholder" | Breaks when options are reordered or added |

Note that `label=` matches the **full visible text exactly** (after whitespace normalisation). Supply the exact text as the user sees it.

### 3. Multi-select lists

For `<select multiple>` pass a **list**:

```python
page.locator("#toppings").select_option(["cheese", "olives"])           # values
page.locator("#toppings").select_option(label=["Extra cheese", "Olives"])  # labels
```

Important behaviour: `select_option` **replaces** the selection. After the call, exactly the options you listed are selected, and everything else is deselected. If you wanted to *add* to an existing selection, you must read the current selection first and pass the union (see Example 4). To clear everything:

```python
page.locator("#toppings").select_option([])
```

On a *single* `<select>`, passing several values selects only the last one (just as a browser would).

You can also describe options with dictionaries, which is useful for matching more than one attribute at once:

```python
select.select_option({"label": "Canada"})
select.select_option([{"value": "us"}, {"index": 2}])
```

### 4. What `select_option()` returns

It returns a list of strings: the **values** of the options that are selected after the call.

```python
selected = page.locator("#country").select_option(label="Canada")
assert selected == ["ca"]
```

This is occasionally handy, but remember the guidance from last lesson: for assertions, prefer `expect`, which retries.

### 5. Verifying the selection

**Single select:** `to_have_value()` checks the *value* of the selected option.

```python
expect(page.locator("#country")).to_have_value("ca")
```

It accepts a plain string or a regular expression (`re.compile(r"^c")`).

**Multi-select:** `to_have_values()` takes a **list** of values, and checks that precisely those are selected (order-insensitive in the sense of the order of options in the list; supply them in document order to be safe).

```python
expect(page.locator("#toppings")).to_have_values(["cheese", "olives"])
```

To verify the **visible text** of the selected option, use a locator on the *selected option*: `page.locator("#country option:checked")` and then `to_have_text("Canada")`. The `:checked` pseudo-class on `<option>` matches the currently selected option(s).

### 6. Verifying the *available* options

Good tests check what a dropdown offers: all options present, in the right order, no duplicates, disabled options really disabled.

```python
options = page.locator("#country option")
expect(options).to_have_text(["-- Please choose --", "United States", "Canada", "India (coming soon)"])
expect(options).to_have_count(4)
expect(page.locator("#country option[value='in']")).to_be_disabled()
```

Passing a **list** to `to_have_text` compares the entire list of elements to the entire list of strings, in order. This is powerful: one line verifies content, count and order together.

Sometimes you need the options in Python (for example to confirm the list is sorted alphabetically):

```python
labels = page.locator("#country option").all_inner_texts()
assert labels[1:] == sorted(labels[1:])        # skip the placeholder
```

`all_inner_texts()` returns a list of strings for all matching elements. It does not auto-wait for the count to settle, so make sure the options have loaded first (see Section 9).

### 7. Option groups, placeholders and disabled options

- **`<optgroup>`:** Options inside a group are still ordinary options; `select_option` works on them as usual. The group label is not selectable. To verify grouping, locate `optgroup[label='Europe'] option`.
- **Placeholders:** Many forms have `value=""` for the "please choose" option. Test that submitting while it is selected shows a validation error, then select a real value. It is also useful to assert the initial state: `expect(select).to_have_value("")`.
- **Disabled options:** `select_option` of a disabled option fails (Playwright waits for the option to become enabled and times out), mirroring the real user. Test the *disabled* state with `expect(option).to_be_disabled()`.

### 8. Custom dropdowns (the other kind)

Modern component libraries (Material UI, Ant Design, React-Select, Angular Material, Bootstrap dropdowns, Select2) rarely use the native element. They typically render:

```html
<div class="select" role="combobox" aria-expanded="false" tabindex="0">Choose a country</div>
<ul role="listbox" hidden>
  <li role="option">United States</li>
  <li role="option">Canada</li>
</ul>
```

or a `<button>` that opens a floating `<div>` of options appended at the end of the `<body>`. Because there is no `<select>`, **`select_option()` raises an error** such as "Element is not a `<select>` element". The technique is the same as a human's: **open it, then click the option**.

```python
page.get_by_role("combobox", name="Country").click()          # open
page.get_by_role("option", name="Canada").click()             # choose
expect(page.get_by_role("combobox", name="Country")).to_have_text("Canada")
```

Practical advice for custom dropdowns:

1. **Find the trigger** by role (`combobox`, `button`), label, or test id. Inspect the HTML to see which the library uses.
2. **Wait for the options to appear**; `get_by_role("option", ...).click()` auto-waits for visibility, so the open-then-click pattern is naturally reliable.
3. **Options may live elsewhere in the DOM.** Many libraries render the list in a "portal" at the end of `<body>`, not inside the dropdown element. So do not scope the option locator to the trigger's container; search from `page`.
4. **Pick a unique option.** If "Canada" appears in two lists on the page, scope by container: `page.locator("#country-list").get_by_role("option", name="Canada")`.
5. **Use `exact=True`** when one option's name contains another ("India" and "Indiana").
6. **Assert the visible result** (text shown in the trigger, a hidden input value, or a chip/tag in multi-select).

**Multi-select custom components** (a field with "chips" or tags) usually stay open after each click or can be reopened. Repeat the open-click pattern for each value and assert the chips:

```python
for skill in ["Python", "SQL"]:
    page.get_by_role("combobox", name="Skills").click()
    page.get_by_role("option", name=skill, exact=True).click()
expect(page.locator(".chip")).to_have_text(["Python", "SQL"])
```

### 9. Searchable dropdowns, dependent dropdowns and loading data

Two scenarios deserve special thought.

**Searchable (typeahead) dropdown.** The user types to filter. The Playwright pattern is: open or focus, **type with `press_sequentially`** (so key events fire), wait for the filtered options, click one. This is closely related to the next lesson, auto-suggestions, which treats typing-driven lists in depth.

```python
combo = page.get_by_role("combobox", name="Country")
combo.click()
combo.press_sequentially("Can")
page.get_by_role("option", name="Canada").click()
```

**Dependent (cascading) dropdowns.** Choosing "Country" repopulates "State/Province". The second list may load from the server and for a moment be empty or show a loading item. Never select from the second list immediately. Wait for the expected options to exist first, using the auto-retrying assertion:

```python
page.locator("#country").select_option(label="Canada")
expect(page.locator("#state option")).to_have_count(14)  # or: to_have_text([...]) / wait for a specific option
page.locator("#state").select_option(label="Ontario")
```

Better still, wait for the exact option you need: `expect(page.locator("#state option", has_text="Ontario")).to_be_attached()`. In Playwright, `select_option` itself already waits (up to the timeout) for the matching option to exist, so in many cases you can call it straight away, but the explicit wait documents the dependency and gives a better failure message.

> **Anti-pattern.** `time.sleep(2)` between dependent dropdowns. It makes the test slow when the server is fast and flaky when the server is slow. Wait for the *condition* instead.

### 10. Keyboard alternatives

Native selects also respond to the keyboard: focus them and type the first letters of an option, or use arrow keys. Playwright can do this (`select.focus(); page.keyboard.type("Can")`), but it is browser-specific and not needed when `select_option` exists. Keep this approach for **testing keyboard accessibility** of custom dropdowns (a requirement in many organisations): open with Enter or Space, move with the arrow keys, choose with Enter, close with Escape. Keyboard actions are the subject of the next-but-one lesson today, so we only note the connection here.

---

## Code Examples

All examples use Python, Playwright's sync API and pytest-playwright (the `page` fixture). Most use `page.set_content()` so they are self-contained; one uses the public practice page `https://the-internet.herokuapp.com/dropdown`, which contains a native `<select id="dropdown">` with options "Please select an option" (value `""`, disabled), "Option 1" (value `1`) and "Option 2" (value `2`).

### Example 1: Three ways to select, on a real page

```python
from playwright.sync_api import Page, expect


def test_native_dropdown_three_ways(page: Page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    dropdown = page.locator("#dropdown")

    dropdown.select_option(value="1")
    expect(dropdown).to_have_value("1")

    dropdown.select_option(label="Option 2")
    expect(dropdown).to_have_value("2")

    dropdown.select_option(index=1)          # index 0 is the placeholder, so 1 is "Option 1"
    expect(dropdown).to_have_value("1")

    expect(page.locator("#dropdown option:checked")).to_have_text("Option 1")
```

**Line by line**

1. Imports as before: `Page` for typing, `expect` for retrying assertions.
2. `dropdown = page.locator("#dropdown")`: describes the `<select>` by its id. We store it in a variable to avoid repeating the selector.
3. `dropdown.select_option(value="1")`: selects the option whose `value` attribute is `1`. Playwright fires `change` events.
4. `expect(dropdown).to_have_value("1")`: checks that the select's current value is `"1"`.
5. `select_option(label="Option 2")`: selects by visible text; the value becomes `"2"`.
6. `select_option(index=1)`: selects the second option in the list (indexes start at 0). Because index 0 is the placeholder, index 1 is "Option 1". This shows why index is fragile: the number means something only with knowledge of the list's current order.
7. The final line locates `option:checked` (the currently selected `<option>` element) and checks its visible text. This verifies *both* the label and the value are consistent.

### Example 2: Verifying the available options

```python
from playwright.sync_api import Page, expect

COUNTRY_FORM = """
<label for="country">Country</label>
<select id="country" name="country">
  <option value="">-- Please choose --</option>
  <optgroup label="North America">
    <option value="us">United States</option>
    <option value="ca">Canada</option>
  </optgroup>
  <optgroup label="Asia">
    <option value="in" disabled>India (coming soon)</option>
    <option value="jp">Japan</option>
  </optgroup>
</select>
"""


def test_country_options(page: Page):
    page.set_content(COUNTRY_FORM)
    select = page.get_by_label("Country")
    options = select.locator("option")

    expect(select).to_have_value("")                       # placeholder selected initially
    expect(options).to_have_text([
        "-- Please choose --",
        "United States",
        "Canada",
        "India (coming soon)",
        "Japan",
    ])
    expect(page.locator("option[value='in']")).to_be_disabled()
    expect(page.locator("optgroup[label='Asia'] option")).to_have_count(2)

    select.select_option(label="Japan")
    expect(select).to_have_value("jp")
```

**Explanation**

- `page.get_by_label("Country")` finds the `<select>` through its `<label for="country">`, which is the user-facing, recommended way.
- `select.locator("option")` searches *within* the select for option elements; chaining locators narrows the scope.
- `to_have_text([...])` with a list asserts the **exact ordered list** of option texts. A missing, extra or reordered option makes the test fail and the error message shows both lists.
- `to_be_disabled()` applies to `<option>` as well as form controls.
- Finally we select Japan by label; it lives inside an `<optgroup>`, which makes no difference to `select_option`.

### Example 3: Multi-select, replace semantics and clearing

```python
from playwright.sync_api import Page, expect

SKILLS_FORM = """
<label for="skills">Skills</label>
<select id="skills" multiple size="5">
  <option value="py">Python</option>
  <option value="sql">SQL</option>
  <option value="js">JavaScript</option>
  <option value="git">Git</option>
  <option value="ci">CI/CD</option>
</select>
"""


def test_multi_select(page: Page):
    page.set_content(SKILLS_FORM)
    skills = page.get_by_label("Skills")

    skills.select_option(["py", "sql"])
    expect(skills).to_have_values(["py", "sql"])

    skills.select_option(label=["Git", "CI/CD"])     # replaces the selection
    expect(skills).to_have_values(["git", "ci"])

    skills.select_option([])                          # clear
    expect(skills).to_have_values([])
```

**Line by line**

1. `multiple size="5"` makes the select a list box showing five rows at once, with several options selectable.
2. `skills.select_option(["py", "sql"])`: a list means "select these values". No Ctrl key is needed: Playwright sets the selection directly.
3. `expect(skills).to_have_values(["py", "sql"])`: `to_have_values` (plural) is the multi-select assertion; it compares the list of selected values.
4. `select_option(label=["Git", "CI/CD"])`: selection by label with a list. Because select_option **replaces** the selection, "Python" and "SQL" are no longer selected afterwards, and the assertion proves it.
5. `select_option([])`: an empty list clears the selection. `to_have_values([])` confirms no options are selected.

### Example 4: Adding to an existing selection

```python
from playwright.sync_api import Page, expect


def add_to_multiselect(page: Page, select_locator, new_values: list[str]):
    """Select new_values IN ADDITION to whatever is already selected."""
    current = select_locator.evaluate(
        "el => Array.from(el.selectedOptions).map(o => o.value)"
    )
    merged = list(dict.fromkeys(current + new_values))   # union, keeps order, no duplicates
    select_locator.select_option(merged)


def test_add_without_losing_existing(page: Page):
    page.set_content("""
      <select id="s" multiple>
        <option value="a" selected>A</option><option value="b">B</option><option value="c">C</option>
      </select>""")
    s = page.locator("#s")

    add_to_multiselect(page, s, ["c"])
    expect(s).to_have_values(["a", "c"])
```

**Explanation**

- `select_locator.evaluate("el => ...")` runs JavaScript in the page with the element as `el`. `el.selectedOptions` is the list of currently selected `<option>` elements; `Array.from(...).map(o => o.value)` turns it into a plain array of their values, which Playwright returns to Python as a list of strings.
- `current + new_values` concatenates two Python lists. `dict.fromkeys(...)` is a well-known trick: dictionary keys are unique and keep insertion order, so converting to a dict and back to a list removes duplicates without reordering.
- `select_option(merged)` then selects the combined set.
- Why not simply call `select_option(["c"])`? Because that would **replace** the selection and drop "A". This helper encodes the "add" behaviour explicitly.
- `list[str]` is a type hint ("a list of strings"); it documents the function but is not enforced.

### Example 5: A custom (non-native) dropdown

```python
from playwright.sync_api import Page, expect

CUSTOM_SELECT = """
<style>[hidden]{display:none}</style>
<button id="trigger" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-label="Priority">Choose priority</button>
<ul id="menu" role="listbox" hidden>
  <li role="option">Low</li>
  <li role="option">Medium</li>
  <li role="option">High</li>
</ul>
<script>
  const t = document.getElementById('trigger');
  const m = document.getElementById('menu');
  t.onclick = () => { m.hidden = !m.hidden; t.setAttribute('aria-expanded', String(!m.hidden)); };
  m.onclick = e => {
    if (e.target.getAttribute('role') === 'option') {
      t.textContent = e.target.textContent;
      m.hidden = true;
      t.setAttribute('aria-expanded', 'false');
    }
  };
</script>
"""


def test_custom_dropdown(page: Page):
    page.set_content(CUSTOM_SELECT)
    priority = page.get_by_role("combobox", name="Priority")

    expect(priority).to_have_text("Choose priority")
    priority.click()
    expect(page.get_by_role("listbox")).to_be_visible()
    expect(page.get_by_role("option")).to_have_text(["Low", "Medium", "High"])

    page.get_by_role("option", name="High").click()

    expect(priority).to_have_text("High")
    expect(page.get_by_role("listbox")).to_be_hidden()
```

**Explanation**

- The markup imitates a typical custom component: a button with `role="combobox"` and a list with `role="listbox"` whose children are `role="option"`. Accessibility roles are exactly what `get_by_role` uses, so well-built components are easy to automate.
- `page.get_by_role("combobox", name="Priority")`: the accessible name comes from `aria-label`.
- We try `select_option` **nowhere**: it would fail because the trigger is a `<button>`, not a `<select>`.
- `priority.click()` opens the list. `expect(listbox).to_be_visible()` waits for it.
- `expect(page.get_by_role("option")).to_have_text([...])` verifies the available choices, as in the native case.
- `page.get_by_role("option", name="High").click()` chooses. Then we verify the outcome twice: the trigger shows "High" and the list has closed.

### Example 6: Dependent dropdowns with a simulated delay

```python
from playwright.sync_api import Page, expect

DEPENDENT = """
<select id="country"><option value="">Choose</option><option value="us">USA</option><option value="ca">Canada</option></select>
<select id="state"><option value="">Select country first</option></select>
<script>
  const data = { us: ['California', 'Texas'], ca: ['Ontario', 'Quebec', 'Alberta'] };
  country.onchange = () => {
    state.innerHTML = '<option value="">Loading...</option>';
    setTimeout(() => {
      state.innerHTML = '<option value="">Choose</option>' +
        (data[country.value] || []).map(s => `<option>${s}</option>`).join('');
    }, 800);   // simulates a slow network
  };
</script>
"""


def test_dependent_dropdowns(page: Page):
    page.set_content(DEPENDENT)

    page.locator("#country").select_option(label="Canada")
    states = page.locator("#state option")

    # Wait for the REAL options, not for a fixed number of seconds
    expect(states).to_have_text(["Choose", "Ontario", "Quebec", "Alberta"])

    page.locator("#state").select_option("Quebec")
    expect(page.locator("#state")).to_have_value("Quebec")
```

**Explanation**

- The script empties the state list, shows "Loading...", and 800 ms later fills the real options. This reproduces what happens when the list comes from an API.
- `expect(states).to_have_text([...])` **retries** until the whole list equals the expected one (or the 5-second default timeout expires). It handles the delay with no explicit sleep, and has the side benefit of verifying the contents of the dependent list.
- Option elements without a `value` attribute use their text as the value, so `select_option("Quebec")` matches by value (equal to the text) and `to_have_value("Quebec")` passes.
- If you had called `select_option("Quebec")` instantly, Playwright's own waiting would still have helped, but you would not have verified the list, and the error message on failure would be less clear.

### Example 7: Data-driven selection in a form

```python
import pytest
from playwright.sync_api import Page, expect

FORM = """
<select id="size"><option value="">Size</option><option value="s">Small</option><option value="m">Medium</option><option value="l">Large</option></select>
<select id="color"><option value="">Colour</option><option value="r">Red</option><option value="b">Blue</option></select>
<button id="add" type="button">Add</button><p id="cart"></p>
<script>add.onclick = () => cart.textContent = size.value + '-' + color.value;</script>
"""


@pytest.mark.parametrize(
    "size_label, color_label, expected",
    [("Small", "Red", "s-r"), ("Large", "Blue", "l-b"), ("Medium", "Red", "m-r")],
)
def test_variants(page: Page, size_label, color_label, expected):
    page.set_content(FORM)
    page.locator("#size").select_option(label=size_label)
    page.locator("#color").select_option(label=color_label)
    page.get_by_role("button", name="Add").click()
    expect(page.locator("#cart")).to_have_text(expected)
```

**Explanation:** `parametrize` feeds three rows of data into one test. The test is written once, runs three times, and the failure message names the failing combination. This pattern reappears in the project, and Wednesday's lesson on data-driven testing will move such data into external files.

---

## Real-World Scenarios

**Scenario 1: Country and state/province on a checkout.** Selecting "Canada" must replace the state list with provinces and change the postal-code label to "Postal code" (versus "ZIP code" for the USA). A good test selects each country in turn, asserts the dependent list contents with `to_have_text([...])`, and checks the label change. Because the second list is often loaded from an API, waiting on the actual options (instead of sleeping) keeps it stable.

**Scenario 2: Filtering a report.** A BI dashboard has a "Region" multi-select and a "Quarter" single select. The test chooses two regions and one quarter, clicks "Apply", and verifies the table row count. The multi-select uses `select_option([...])`, and a separate test verifies that clearing it (`select_option([])`) shows all regions.

**Scenario 3: Role assignment in an admin screen.** A "Role" dropdown contains "Admin", "Editor", "Viewer". Business rules say a user cannot assign a role higher than their own. The test logs in as an editor, opens the dropdown, and asserts that "Admin" is *disabled* (`to_be_disabled()`) or *absent* (`to_have_count(0)` for that option), then selects "Viewer".

**Scenario 4: A design-system component library.** The company's front-end uses React-Select everywhere. Native `select_option` is useless. The team writes a small helper `choose_option(page, field_label, option_text)` that opens by role and clicks the option. Every test uses the helper, so when the library is upgraded, only one function needs updating. (You will see how to organise helpers like this properly on Wednesday.)

**Scenario 5: Sorted list quality check.** A requirement says the currency dropdown must be alphabetical with "USD" first. A test reads the options with `all_inner_texts()` and compares to the expected ordering. This kind of check is cheap and catches data regressions that no human tester would notice.

---

## Common Pitfalls and Best Practices

1. **Using `select_option` on a custom dropdown.** If the error says the element is not a `<select>`, inspect the HTML. Use open-then-click with roles instead.

2. **Clicking `<option>` elements in a native select.** Do not do `page.locator("option[value='ca']").click()`. Native option lists are not clickable in the normal way, especially in headless mode. Always use `select_option`.

3. **Confusing label with value.** If `select_option("Canada")` unexpectedly fails, check whether the value is `ca` and the label is `Canada`. Use the explicit `label=` or `value=` form to remove ambiguity.

4. **Relying on `index=`.** Adding a placeholder or a new option shifts all indexes. Reserve it for "choose any valid option" scenarios.

5. **Expecting multi-select to add.** `select_option` replaces. Compute the union (Example 4) if you need to add.

6. **Not waiting for dependent or remote options.** Wait for the expected option list with `expect`, not `sleep`.

7. **Scoping option locators to the wrong container.** Custom dropdown lists are often rendered at the end of the body. If `container.get_by_role("option")` finds nothing, search from `page`.

8. **Ambiguous option names.** Use `exact=True` for names that are substrings of others ("Test" vs "Testing").

9. **Asserting only the trigger text.** For custom controls, the visible text may update but the real form value may not (and the next step receives an empty field). When possible, also assert on the hidden input (`page.locator("input[name='country']")`) or the submitted data.

10. **Ignoring the placeholder.** Always test the unselected state and the validation message that appears when a required dropdown is left on its placeholder.

**Best practices checklist:** identify native versus custom first; prefer `label=` for readability and `value=` for stability; verify the option list as well as the choice; use `to_have_value`/`to_have_values`; wait on conditions, never on time; wrap repeated custom-dropdown steps in a helper function.

---

## Mini Practice Exercises

**Exercise 1 (native basics).** On `https://the-internet.herokuapp.com/dropdown`, write a test that selects "Option 2" by label, asserts the value is `2`, then selects "Option 1" by value and asserts the visible selected text is "Option 1".

*Solution:*

```python
def test_dropdown_basic(page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    dd = page.locator("#dropdown")
    dd.select_option(label="Option 2")
    expect(dd).to_have_value("2")
    dd.select_option(value="1")
    expect(page.locator("#dropdown option:checked")).to_have_text("Option 1")
```

**Exercise 2 (what is disabled?).** On the same page, try `dd.select_option(index=0)` (the placeholder is disabled). Observe the behaviour (it times out waiting for the option to be enabled). Write a test asserting instead that the first option is disabled: `expect(page.locator("#dropdown option").first).to_be_disabled()`.

**Exercise 3 (verify the list).** Using Example 2's `COUNTRY_FORM`, add a second assertion that the options are in alphabetical order, ignoring the placeholder and the disabled one.

*Hint:* `texts = page.locator("#country option:not([disabled])").all_inner_texts()`; compare `texts[1:]` to `sorted(texts[1:])`.

**Exercise 4 (multi-select).** With Example 3's form, write tests for: (a) select three skills and assert them, (b) select none and assert none, (c) select a skill, then verify that selecting a different one replaces it.

**Exercise 5 (custom dropdown).** Extend Example 5 so that selecting "High" also reveals a text paragraph "Escalated" (add the JavaScript). Write the test that selects "High" and asserts the paragraph is visible, then selects "Low" and asserts the paragraph is hidden.

*Hint:* add `esc.hidden = e.target.textContent !== 'High'` to the click handler of the menu.

**Exercise 6 (helper function).** Write `choose_option(page, combobox_name, option_name)` that opens a custom combobox by role/name and clicks the option with `exact=True`. Then rewrite Example 5 to use it.

*Solution:*

```python
def choose_option(page, combobox_name: str, option_name: str):
    page.get_by_role("combobox", name=combobox_name).click()
    page.get_by_role("option", name=option_name, exact=True).click()
```

**Exercise 7 (challenge: dependent dropdowns).** Modify Example 6 to take its data from a Python dictionary and test every country in a loop (or parametrised test), asserting the exact list of states each time. Add a deliberate bug (remove a state in the JavaScript) and make sure your test catches it.

---

## Summary / Key Takeaways

- There are two worlds: **native `<select>`** (use `select_option`) and **custom dropdowns** (open, then click an element with `role="option"`). Always inspect first.
- `select_option` supports `value=`, `label=`, `index=`, lists for multi-select, dictionaries, and returns the selected values. It fires the real `input`/`change` events.
- For multi-selects, `select_option` **replaces** the selection; pass `[]` to clear; compute the union to add.
- Verify with `to_have_value`, `to_have_values`, `to_have_text([...])` on `option` locators, `to_be_disabled`, and `to_have_count`.
- Dependent and remote lists need **condition-based waits** (`expect`) not sleeps.
- Test the initial placeholder state, the available options, the selection, and the downstream effect on the page.
- Wrap repeated custom-dropdown interactions in small helpers for maintainability.

---

## External Resources

- Playwright for Python, Actions (Select options): https://playwright.dev/python/docs/input#select-options
- Playwright for Python API reference, `Locator.select_option`: https://playwright.dev/python/docs/api/class-locator#locator-select-option
- MDN Web Docs, the `<select>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select
