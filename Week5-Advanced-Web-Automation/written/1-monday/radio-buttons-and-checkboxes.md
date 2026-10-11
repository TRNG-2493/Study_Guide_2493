# Radio Buttons and Checkboxes

## Learning Objectives

By the end of this lesson you will be able to:

- Explain how radio buttons and checkboxes differ in HTML, in user behaviour and in what a test should verify.
- Locate checkboxes and radio buttons reliably using `get_by_label`, `get_by_role`, and scoped locators.
- Use `check()`, `uncheck()` and `set_checked()` to bring a control to the desired state, and explain why these are better than `click()`.
- Read the current state with `is_checked()` and assert it with `expect(locator).to_be_checked()`.
- Understand the "mutual exclusivity" of radio groups and test it.
- Handle select-all checkboxes, groups of checkboxes, disabled controls and indeterminate states.
- Deal with custom-styled controls whose real `<input>` is hidden, and know when `force=True` is (and is not) acceptable.
- Write a data-driven test that fills a preferences form.

---

## Why This Matters

In the Week 5 epic, you are learning to master complex UI interactions. Forms are the backbone of nearly every business application: sign-up flows, checkout pages, patient intake, loan applications, settings screens, surveys. And forms are made largely of *choices*: "Yes, send me the newsletter", "Ship express", "I agree to the Terms", "Gender", "Preferred contact method". Radio buttons and checkboxes encode those choices.

For **Project 1: QE Foundations**, your UI milestone is to automate a complex form flow. Whether the form is registration, checkout or a profile update, you will touch these controls constantly. Mistakes with them are among the most frequent causes of flaky tests. Typical beginner problems include:

- A test that *clicks* a checkbox to tick it, but the box was already ticked, so the click *unticks* it and the test fails later in a confusing way.
- A test that never checks the final state, so it "passes" even if the checkbox did nothing.
- A test that cannot find the checkbox because the site hides the real input behind a stylish custom control.

Playwright gives us simple, **idempotent** methods (*idempotent* means: running it once or ten times gives the same final result) that avoid the first problem entirely, and assertions that solve the second. After this lesson, you will treat checkboxes and radios as *state*, not as *clicks*.

---

## The Concept

### 1. What are checkboxes and radio buttons?

Both are HTML `<input>` elements, distinguished by their `type` attribute.

**Checkbox:** `<input type="checkbox">`. A checkbox represents an independent on/off choice. A group of checkboxes lets the user pick **zero, one, or many** options. Clicking toggles that box and does not affect the others.

**Radio button:** `<input type="radio" name="size">`. A radio button represents one choice from a set. Radios that share the same `name` attribute form a **radio group**, and the browser guarantees that **at most one** is selected at a time. Selecting a different radio automatically deselects the previously selected one. The name comes from old car radios with push-buttons: pressing one button popped the others out.

| Feature | Checkbox | Radio button |
|---|---|---|
| HTML | `<input type="checkbox">` | `<input type="radio" name="group">` |
| Selection rule | Any number may be checked | Exactly one per group (once chosen) |
| Can the user uncheck by clicking it? | Yes | **No**, you select a different one |
| Typical question | "Which extras do you want?" | "Which delivery speed?" |
| Playwright to select | `check()` | `check()` |
| Playwright to unselect | `uncheck()` | Not possible directly; check another radio |

> **Beginner note.** Radio groups start with *none* selected unless the developer adds the `checked` attribute. Once the user selects one, there is no way to return to "none" except by resetting the form.

### 2. State versus action

When you look at a checkbox you see **state**: ticked or not ticked. A tester's job is to bring the form to a *desired state* and verify it. A common but fragile approach is to think in terms of actions ("click the box"). Consider:

```python
page.locator("#newsletter").click()   # fragile
```

If `#newsletter` was unticked, this ticks it. If it was ticked (maybe the site pre-selects it, or a previous step ticked it, or browser autofill did), this **unticks** it, the exact opposite of what you wanted. The test's result now depends on hidden starting conditions.

The better approach is to say *what you want*:

```python
page.locator("#newsletter").check()    # make sure it IS checked
```

`check()` means "ensure this is checked". If it is already checked, Playwright does nothing and moves on. If not, it clicks it, and then **verifies that the state really became checked**; if clicking did not result in a checked state (because JavaScript prevented it), `check()` raises an error. This built-in verification is a significant advantage over `click()`.

### 3. The Playwright methods

#### `locator.check()`

Ensures a checkbox or radio is checked. Steps Playwright performs:

1. Ensures the element is a checkbox or radio input (otherwise it raises an error; see Section 9 for custom controls).
2. If it is already checked, returns immediately.
3. Waits for **actionability**: the element must be attached to the page, visible, stable (not animating), enabled, and able to receive pointer events (nothing covering it).
4. Scrolls it into view and clicks it.
5. Ensures the element is now checked, otherwise throws.

#### `locator.uncheck()`

The mirror image. It ensures a **checkbox** is unchecked. On a radio button it fails, because a user cannot uncheck a radio by clicking it, and Playwright faithfully reproduces user behaviour (the check in step 5 would not be satisfied).

#### `locator.set_checked(checked, ...)`

Takes a boolean. `set_checked(True)` behaves like `check()` and `set_checked(False)` like `uncheck()`. It is perfect for data-driven tests where the desired state comes from a variable:

```python
page.get_by_label("Subscribe").set_checked(user["subscribe"])   # True or False
```

Without it you would need an `if` statement choosing between `check()` and `uncheck()`.

#### `locator.is_checked()`

Returns a Python boolean for the *current* state, **right now**, without waiting or retrying. It is useful in conditions or logic, e.g. `if box.is_checked():`. It is **not** the right tool for assertions in tests, as the next method is better.

#### `expect(locator).to_be_checked()`

The assertion for state. It retries automatically until the box is checked or the timeout expires, so if a script is slow to update the state, the test still passes without arbitrary sleeping. Useful variants:

```python
expect(box).to_be_checked()                # must be checked
expect(box).not_to_be_checked()            # must NOT be checked
expect(box).to_be_checked(checked=False)   # also "not checked"
expect(box).to_be_enabled()                # not disabled
expect(box).to_be_disabled()
```

There is also `expect(box).to_be_checked(indeterminate=True)` (in recent versions) for the special tri-state described below.

#### `locator.click()`

Still valid, and sometimes the right one: when you want to test the toggling behaviour itself ("clicking once checks, clicking twice unchecks"), or the control is custom. But for *setting* a state, prefer `check`/`uncheck`/`set_checked`.

### 4. Locating checkboxes and radios well

A good locator is one that reads like what a user sees. In order of preference:

1. **By label:** `page.get_by_label("Email notifications")`. This works if the `<label>` is associated with the input (via `for`/`id` or by wrapping the input). It reads naturally and keeps working if the markup changes.
2. **By role and accessible name:** `page.get_by_role("checkbox", name="Email notifications")` and `page.get_by_role("radio", name="Express")`. The role distinguishes a checkbox from a text box that happens to have the same label, and the accessible name is the label text. This is the most robust in terms of meaning.
3. **By test id** if your team adds `data-testid`: `page.get_by_test_id("terms-checkbox")`.
4. **By CSS/ID** (`#terms`, `input[name='size'][value='large']`) when the above are not available. Radios in a group often share a name and differ by `value`, which makes `input[name='size'][value='large']` a legitimate precise selector.

`get_by_label` uses **substring, case-insensitive** matching by default. If you have labels "Phone" and "Phone (work)", `get_by_label("Phone")` matches both and Playwright's strict mode will raise an error. Use `exact=True`:

```python
page.get_by_label("Phone", exact=True).check()
```

**Strict mode** is an important idea: if a locator matches more than one element and you perform an action (`check`, `click`, `fill`), Playwright raises an error rather than guessing. This protects you from acting on the wrong element.

### 5. Working with groups of checkboxes

When there are many boxes, for example a list of interests, use one of these patterns.

**Pattern A: a named list.** Simple and explicit; ideal when you know what you want.

```python
for name in ["Hiking", "Cooking", "Gaming"]:
    page.get_by_role("checkbox", name=name).check()
```

**Pattern B: all boxes in a container.** `locator.all()` returns a list of locators, one for each matching element. Use it for "tick everything":

```python
boxes = page.locator("#interests input[type='checkbox']")
for box in boxes.all():
    box.check()
```

(`locator.all()` takes a snapshot of how many elements exist at that moment; make sure the page is fully rendered before calling it. A reliable way is to first `expect(boxes).to_have_count(5)`.)

**Pattern C: by index.** `boxes.nth(0).check()` and `boxes.first`, `boxes.last`. Use sparingly, since position-based selection breaks if the order changes.

**Counting checked boxes** to verify a "select all" feature:

```python
checked = page.locator("#interests input:checked")
expect(checked).to_have_count(5)
```

`:checked` is a standard CSS pseudo-class which matches ticked checkboxes and selected radios.

### 6. Working with radio groups

Select by label or by value:

```python
page.get_by_role("radio", name="Express").check()
page.locator("input[name='shipping'][value='express']").check()
```

To verify exclusivity (only one selected), assert both the chosen one and the others:

```python
expect(page.get_by_role("radio", name="Express")).to_be_checked()
expect(page.get_by_role("radio", name="Standard")).not_to_be_checked()
```

Or count: `expect(page.locator("input[name='shipping']:checked")).to_have_count(1)`.

To *find out* which radio is selected without knowing in advance, evaluate the group:

```python
selected_value = page.locator("input[name='shipping']:checked").input_value()
```

`input_value()` returns the `value` attribute for a checked radio. (For checkboxes, `input_value()` returns the `value` attribute regardless of the checked state, which is usually `"on"` unless the developer set one; do not confuse it with state.)

### 7. Default states, disabled controls and read-only logic

Testing the *initial* state is as valuable as testing the action: "the Terms checkbox is unchecked by default" is a legal requirement in many regions (no pre-ticked consent). Assert it before acting:

```python
expect(page.get_by_label("I agree to the Terms")).not_to_be_checked()
```

A **disabled** control cannot be changed by the user. Playwright's `check()` waits for the element to become enabled and times out if it never does. That is correct behaviour (a user also cannot tick it), but means you should assert disabled status explicitly when the rule is "this option is unavailable":

```python
expect(page.get_by_label("Gift wrap")).to_be_disabled()
```

Conditional UI is common: ticking "Same as billing address" may *disable* and pre-fill the shipping address fields. A test should check the side effects:

```python
page.get_by_label("Same as billing").check()
expect(page.get_by_label("Shipping street")).to_be_disabled()
```

### 8. Indeterminate (tri-state) checkboxes

A "select all" box in a table header often has three visual states: all selected, none selected, and **indeterminate** (some selected, shown as a dash). Indeterminate is a JavaScript property (`input.indeterminate`), not an HTML attribute, and a checkbox that is indeterminate is *not* considered checked. In recent Playwright versions you can assert it with `expect(box).to_be_checked(indeterminate=True)`; in older versions you can read it with `box.evaluate("el => el.indeterminate")`. Mention this to your team when testing bulk-select features.

### 9. Custom-styled controls and hidden inputs

Designers frequently hide the native `<input>` and draw their own pretty switch, tick or radio with CSS. The input is then `opacity: 0` or `display: none`, positioned off-screen, or covered by a `<span>`. Playwright's actionability checks may then report "element is not visible" or "element intercepts pointer events".

You have a ladder of solutions, from best to last resort:

1. **Target the label.** The clickable thing the user sees is often the `<label>`. Clicking a label toggles its input:

   ```python
   page.get_by_text("Remember me").click()
   ```

   Use `click()` here rather than `check()` and then assert with `expect(...).to_be_checked()` on the underlying input. (Be careful: you lose the idempotence of `check()`, so assert the *state before* if it might already be checked.)

2. **Use ARIA roles.** Many component libraries use `<div role="checkbox" aria-checked="false">` or `<button role="switch">`. Playwright's `get_by_role("checkbox")` finds them, and recent versions support `check()`/`uncheck()` and `to_be_checked()` on elements with such ARIA roles as well. If your version rejects it, fall back to `click()` and assert via `expect(el).to_have_attribute("aria-checked", "true")`.

3. **`force=True`.** `box.check(force=True)` skips the actionability checks (visible, not covered, etc.) and clicks anyway. Use it only when you understand *why* the element looks inactive and you have confirmed that a real user's interaction is the same. Overusing it hides real bugs (for instance, a cookie banner that genuinely blocks the checkbox). Add a comment explaining each use.

4. **`set_checked` on the hidden input with `force`** is similar and equally a last resort.

5. **`trial=True`** (available on `check`, `click`, etc.) performs all the checks but **does not actually click**. It answers "could a user check this right now?". Handy for tests such as "the checkbox is not obstructed".

### 10. How `check()` relates to events

When the user ticks a checkbox, the browser fires `click`, then `input`, then `change` events; the application listens for them to update totals, enable buttons, etc. Playwright's `check()` generates a real mouse click, so these events fire exactly as for a user, which is why it is better than manipulating the property via JavaScript (`evaluate("el => el.checked = true")`), which sets the state **without** firing events and therefore may leave the application unaware. Avoid the JavaScript shortcut in UI tests.

---

## Code Examples

The following examples use Python, the sync API and pytest-playwright (the `page` fixture). To keep them self-contained and deterministic, several use `page.set_content()` with a small HTML form. One uses a public practice page, `https://the-internet.herokuapp.com/checkboxes`, which has two checkboxes (the first starts unchecked, the second checked).

### Example 1: `check()`, `uncheck()` and `expect`

```python
from playwright.sync_api import Page, expect


def test_checkboxes_basic(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")

    checkboxes = page.locator("#checkboxes input[type='checkbox']")
    first = checkboxes.nth(0)
    second = checkboxes.nth(1)

    expect(first).not_to_be_checked()
    expect(second).to_be_checked()

    first.check()
    second.uncheck()

    expect(first).to_be_checked()
    expect(second).not_to_be_checked()

    first.check()          # already checked: does nothing, no error
    expect(first).to_be_checked()
```

**Line by line**

1. `from playwright.sync_api import Page, expect`: `Page` for type hints, `expect` for retrying assertions.
2. `def test_checkboxes_basic(page: Page):`: pytest test; `page` is injected by the plugin.
3. `page.goto(...)`: navigate.
4. `checkboxes = page.locator("#checkboxes input[type='checkbox']")`: a CSS locator: an `<input>` of type checkbox inside the element with id `checkboxes`. A locator is only a *description*; nothing is searched yet.
5. `first = checkboxes.nth(0)` / `second = checkboxes.nth(1)`: pick elements by zero-based position. (On this page there is no label text to use, so positions are acceptable.)
6. `expect(first).not_to_be_checked()` and `expect(second).to_be_checked()`: verify the **starting state**. Beginners often skip this, but it documents the assumption and catches a changed page immediately.
7. `first.check()` and `second.uncheck()`: bring both to the opposite state.
8. The next two `expect` lines verify the new state.
9. `first.check()` again: shows idempotence; no click is performed because it is already checked.

### Example 2: A radio group and mutual exclusivity

```python
from playwright.sync_api import Page, expect

SHIPPING_FORM = """
<form>
  <fieldset>
    <legend>Delivery speed</legend>
    <label><input type="radio" name="speed" value="standard" checked> Standard</label>
    <label><input type="radio" name="speed" value="express"> Express</label>
    <label><input type="radio" name="speed" value="overnight"> Overnight</label>
  </fieldset>
</form>
"""


def test_radio_group_is_mutually_exclusive(page: Page):
    page.set_content(SHIPPING_FORM)

    standard = page.get_by_role("radio", name="Standard")
    express = page.get_by_role("radio", name="Express")
    overnight = page.get_by_role("radio", name="Overnight")

    expect(standard).to_be_checked()          # default

    express.check()
    expect(express).to_be_checked()
    expect(standard).not_to_be_checked()      # the browser deselected it

    overnight.check()
    expect(overnight).to_be_checked()
    expect(express).not_to_be_checked()

    expect(page.locator("input[name='speed']:checked")).to_have_count(1)
    assert page.locator("input[name='speed']:checked").input_value() == "overnight"
```

**Line by line**

1. `SHIPPING_FORM = """..."""`: a module-level constant holding HTML. Triple quotes allow multiple lines. Each radio is wrapped in a `<label>`, so the label text is the radio's accessible name. `checked` makes Standard the default.
2. `page.set_content(SHIPPING_FORM)`: renders that HTML in the blank page.
3. `get_by_role("radio", name="Standard")`: finds the radio whose accessible name is "Standard".
4. The first `expect(standard).to_be_checked()` tests the default.
5. `express.check()`: selects Express. The browser, not Playwright, automatically unselects Standard: we are verifying standard browser behaviour here, which is a stand-in for verifying *your application's* radio group (which could be custom and broken).
6. `expect(page.locator("input[name='speed']:checked")).to_have_count(1)`: exactly one radio of the group is selected.
7. `.input_value()`: reads the `value` attribute of the single checked radio, giving `"overnight"`. The plain `assert` is fine because we have already waited with `expect`.

### Example 3: `set_checked` with data

```python
import pytest
from playwright.sync_api import Page, expect

PREFERENCES_FORM = """
<form id="prefs">
  <label><input type="checkbox" name="email"> Email updates</label><br>
  <label><input type="checkbox" name="sms"> SMS alerts</label><br>
  <label><input type="checkbox" name="push" checked> Push notifications</label>
</form>
"""

CASES = [
    {"Email updates": True,  "SMS alerts": False, "Push notifications": False},
    {"Email updates": False, "SMS alerts": True,  "Push notifications": True},
    {"Email updates": True,  "SMS alerts": True,  "Push notifications": True},
]


@pytest.mark.parametrize("prefs", CASES)
def test_set_preferences(page: Page, prefs: dict):
    page.set_content(PREFERENCES_FORM)

    for label, wanted in prefs.items():
        page.get_by_label(label).set_checked(wanted)

    for label, wanted in prefs.items():
        box = page.get_by_label(label)
        if wanted:
            expect(box).to_be_checked()
        else:
            expect(box).not_to_be_checked()
```

**Explanation**

- `CASES` is a list of dictionaries. Each maps a label to the desired state. This is the beginning of **data-driven testing**: the logic is written once and the data varies. (You will formalise this with JSON files later in the week.)
- `@pytest.mark.parametrize("prefs", CASES)` runs the test three times, once per dictionary.
- `for label, wanted in prefs.items()`: `.items()` yields key/value pairs. For each we call `set_checked(wanted)`. Notice that the third checkbox starts **checked** in the HTML; in case 1 `set_checked(False)` unticks it, and in case 2 `set_checked(True)` leaves it untouched. No `if` is needed and starting state does not matter.
- The second loop verifies every final state. The `if/else` could be shortened with `expect(box).to_be_checked(checked=wanted)`; that keyword argument exists and makes the loop a single line. Both are shown so you can see the logic.

### Example 4: "Select all", counting and indeterminate behaviour

```python
from playwright.sync_api import Page, expect

TABLE_HTML = """
<input type="checkbox" id="all" aria-label="Select all">
<ul id="rows">
  <li><label><input type="checkbox"> Row A</label></li>
  <li><label><input type="checkbox"> Row B</label></li>
  <li><label><input type="checkbox"> Row C</label></li>
</ul>
<script>
  const all = document.getElementById('all');
  const rows = [...document.querySelectorAll('#rows input')];
  function sync() {
    const n = rows.filter(r => r.checked).length;
    all.checked = n === rows.length;
    all.indeterminate = n > 0 && n < rows.length;
  }
  all.addEventListener('change', () => { rows.forEach(r => r.checked = all.checked); sync(); });
  rows.forEach(r => r.addEventListener('change', sync));
</script>
"""


def test_select_all_behaviour(page: Page):
    page.set_content(TABLE_HTML)
    select_all = page.get_by_label("Select all")
    row_boxes = page.locator("#rows input[type='checkbox']")

    select_all.check()
    expect(row_boxes).to_have_count(3)                            # sanity: three rows
    expect(page.locator("#rows input:checked")).to_have_count(3)

    page.get_by_label("Row B").uncheck()
    expect(select_all).not_to_be_checked()
    assert select_all.evaluate("el => el.indeterminate") is True

    select_all.uncheck()
    expect(page.locator("#rows input:checked")).to_have_count(0)
```

**Explanation**

- The inline `<script>` simulates a typical "select all" widget. Do not worry about the JavaScript details; what matters is the behaviour.
- `select_all.check()` ticks the master box; the script ticks every row. We confirm with the `:checked` pseudo-class and a count.
- After unticking *Row B*, the master box should no longer be checked and should be *indeterminate*. We read that JavaScript property using `locator.evaluate("el => el.indeterminate")`. `evaluate` runs a JavaScript arrow function in the page with the matched element passed as `el`. (`evaluate` is for **reading** here, not for changing state.)
- `expect(row_boxes).to_have_count(3)` is a sanity check that the page really rendered three row checkboxes before we start interacting.

### Example 5: Custom-styled checkbox, clicking the label

```python
from playwright.sync_api import Page, expect

CUSTOM = """
<style>
  input[type=checkbox] { position:absolute; opacity:0; width:0; height:0; }
  .box { display:inline-block; width:18px; height:18px; border:2px solid #333; vertical-align:middle; }
  input:checked + .box { background:#2a7; }
</style>
<label><input type="checkbox" id="remember"><span class="box"></span> Remember me</label>
"""


def test_custom_checkbox(page: Page):
    page.set_content(CUSTOM)

    remember = page.locator("#remember")
    expect(remember).not_to_be_checked()

    page.get_by_text("Remember me").click()      # the visible label is the click target
    expect(remember).to_be_checked()

    remember.uncheck(force=True)                 # last resort, documented
    expect(remember).not_to_be_checked()
```

**Explanation**

- The CSS makes the native checkbox invisible (`opacity:0`, zero size) and draws a green square using the next sibling `<span class="box">`. This mimics many UI libraries.
- Playwright treats an element with zero size as not visible, so a plain `remember.check()` would wait and then time out with a message about the element not being visible.
- `page.get_by_text("Remember me").click()` clicks the label text; the browser toggles the associated input, exactly as a real user's click does.
- `remember.uncheck(force=True)` shows the last-resort option. In a real project, add a comment such as `# input is visually hidden by design system; label click preferred, force used for cleanup`. Notice that even with `force`, Playwright still verifies the final state.

### Example 6: A realistic mini-flow combining radios and checkboxes

```python
from playwright.sync_api import Page, expect

ORDER_FORM = """
<form id="order">
  <fieldset>
    <legend>Pizza size</legend>
    <label><input type="radio" name="size" value="s"> Small</label>
    <label><input type="radio" name="size" value="m"> Medium</label>
    <label><input type="radio" name="size" value="l"> Large</label>
  </fieldset>
  <fieldset>
    <legend>Toppings</legend>
    <label><input type="checkbox" name="top" value="cheese"> Extra cheese</label>
    <label><input type="checkbox" name="top" value="olives"> Olives</label>
    <label><input type="checkbox" name="top" value="mush"> Mushrooms</label>
  </fieldset>
  <label><input type="checkbox" id="terms"> I accept the terms</label>
  <button id="submit" type="button" disabled>Order</button>
  <p id="summary"></p>
</form>
<script>
  const terms = document.getElementById('terms');
  const btn = document.getElementById('submit');
  terms.addEventListener('change', () => btn.disabled = !terms.checked);
  btn.addEventListener('click', () => {
    const size = document.querySelector('input[name=size]:checked')?.value ?? 'none';
    const tops = [...document.querySelectorAll('input[name=top]:checked')].map(x => x.value);
    document.getElementById('summary').textContent = size + ':' + tops.join(',');
  });
</script>
"""


def test_order_flow(page: Page):
    page.set_content(ORDER_FORM)
    submit = page.get_by_role("button", name="Order")

    expect(submit).to_be_disabled()                         # terms not accepted yet

    page.get_by_role("radio", name="Large").check()
    for topping in ("Extra cheese", "Mushrooms"):
        page.get_by_role("checkbox", name=topping).check()

    expect(submit).to_be_disabled()                         # still disabled
    page.get_by_role("checkbox", name="I accept the terms").check()
    expect(submit).to_be_enabled()

    submit.click()
    expect(page.locator("#summary")).to_have_text("l:cheese,mush")
```

**Explanation**

- The form enables the Order button only after the terms checkbox is ticked. This is a standard "conditional enablement" rule, and the test verifies the rule both before and after.
- We use `get_by_role` with the *visible label text* as the name and use a `for` loop with a tuple of topping names to avoid repetition.
- The final assertion proves the application collected the correct data: one radio (`l`) and two checkbox values (`cheese`, `mush`), in document order.
- This is the shape of the Project 1 UI milestone: set several controls, verify intermediate rules, submit, verify the outcome.

---

## Real-World Scenarios

**Scenario 1: Consent management.** A privacy law requires that marketing consent boxes are *unticked by default* and that the account is created whether or not they are ticked. A test checks the default state, completes sign-up with them untouched, and then repeats with each ticked, verifying the stored preference in the user's profile page.

**Scenario 2: Checkout shipping options.** Selecting "Express" radio updates the order total by a surcharge. The test checks each radio in turn (`check()`), reads the displayed total, and compares against expected values. The "only one selected" check guards against a bug where two radios can be selected because a developer used different `name` attributes by mistake.

**Scenario 3: Bulk actions in an admin table.** A back-office list has a header checkbox "select all" and per-row checkboxes plus "Delete selected". Tests tick the header, assert that the row count of `:checked` boxes equals the row count, untick one row to verify the header becomes indeterminate, and ensure that "Delete selected" is disabled when nothing is ticked.

**Scenario 4: Medical intake form.** A long list of "Do you have any of the following?" checkboxes. The test reads the patient's data from a Python dictionary and uses `set_checked` for each condition, so one test function can fill dozens of boxes concisely. A final assertion confirms the review page lists exactly the selected conditions.

**Scenario 5: Feature toggles in settings.** Modern settings use toggle *switches* implemented as `role="switch"`. The `get_by_role("switch", name="Dark mode")` locator finds them, and `check()` works on elements with ARIA roles `checkbox`, `radio` and `switch` in current versions. Verify the effect (for example the page gets a `dark` class: `expect(page.locator("body")).to_have_class(re.compile("dark"))`).

---

## Common Pitfalls and Best Practices

1. **Using `click()` to set state.** It toggles. Use `check()`, `uncheck()` or `set_checked()`.

2. **Calling `uncheck()` on a radio button.** This fails by design. To change a radio, check a different one. To test "no selection", reload or reset the form.

3. **Not asserting state.** A test that checks a box and moves on proves nothing. Follow with `expect(box).to_be_checked()` at least for the controls that matter.

4. **Using `is_checked()` as an assertion.** `assert box.is_checked()` does not wait. If the page updates the state a moment later (after a network response, for example), your test fails randomly. Prefer `expect(...)` for assertions; keep `is_checked()` for control flow.

5. **Ambiguous locators.** Labels like "Email" can match many controls and cause strict mode violations. Use `exact=True`, a role, or scope within a container: `page.locator("fieldset", has_text="Toppings").get_by_label("Olives")`.

6. **Selecting by index when order can change.** Prefer labels or values.

7. **Overusing `force=True`.** It disables safety checks and may hide a real bug (overlay covering the control). Try label clicks and ARIA roles first and document each exception.

8. **Setting `.checked` with JavaScript.** It skips the events that the application depends on.

9. **Forgetting disabled and hidden states.** If `check()` hangs until timeout, read the error: it will say "element is not enabled" or "not visible". That message tells you which part of the actionability checks failed.

10. **Asserting on the wrong layer.** A custom control may show a green tick (CSS) but the underlying value may not have changed. Assert on both the visible effect (class, text) and, where possible, on the real input or the submitted data.

**Best practices:** express desired *state*; verify initial and final state; locate by label or role; keep one logical behaviour per test; use `parametrize` for variations; comment every `force`.

---

## Mini Practice Exercises

**Exercise 1 (state, not click).** On `https://the-internet.herokuapp.com/checkboxes`, write a test that makes *both* checkboxes checked, regardless of their starting state, and verifies the result. Run it twice in a row in the same browser session (for example by calling the function body twice) to prove it is idempotent.

*Solution:*

```python
def test_both_checked(page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    boxes = page.locator("#checkboxes input")
    for box in boxes.all():
        box.check()
    for box in boxes.all():
        expect(box).to_be_checked()
```

**Exercise 2 (radios).** Using the `SHIPPING_FORM` from Example 2, write a parametrised test that selects each of the three speeds in turn and asserts that exactly one radio is checked and that its value matches.

*Hint:* parametrise on `("Standard", "standard")`, `("Express", "express")`, `("Overnight", "overnight")` and use `input_value()` on the `:checked` locator.

**Exercise 3 (default consent).** Build a small form with a pre-ticked "Subscribe" box and write a test that detects the bug "marketing consent must be unchecked by default". The test should *fail* on this page, proving it detects the problem. Then fix the HTML and watch the test pass.

*Hint:* `expect(page.get_by_label("Subscribe")).not_to_be_checked()`.

**Exercise 4 (data-driven preferences).** Extend Example 3 to read the cases from a Python list of three dictionaries that you define, and add a fourth case with all boxes false. Use `to_be_checked(checked=wanted)` in the verification loop.

*Solution for the verification loop:*

```python
for label, wanted in prefs.items():
    expect(page.get_by_label(label)).to_be_checked(checked=wanted)
```

**Exercise 5 (select-all).** Using Example 4, add a test that checks the master box, then unchecks all rows one by one and asserts the master box becomes unchecked and *not* indeterminate at the end.

*Hint:* `assert select_all.evaluate("el => el.indeterminate") is False`.

**Exercise 6 (custom control).** Modify Example 5 so that the label contains a link ("Remember me (see policy)"). Verify that clicking the link text does *not* toggle the checkbox in your implementation, and decide how to click only the visible square (`page.locator(".box").click()`).

**Exercise 7 (challenge).** Write a test for the order form in Example 6 that tries all combinations of sizes (three) and a *subset* of toppings of your choice using `itertools.product`, verifying the summary each time. Keep the test readable by moving the form fill into a helper function `fill_order(page, size, toppings)`.

---

## Summary / Key Takeaways

- Checkboxes allow any number of selections; radios within one `name` group allow exactly one.
- Think in **state**. Use `check()`, `uncheck()` and `set_checked(bool)` instead of `click()`: they are idempotent and verify the result.
- `uncheck()` does not work on radios; select another radio instead.
- Assert with `expect(...).to_be_checked()` / `not_to_be_checked()` (auto-retrying); use `is_checked()` only for logic.
- Prefer locators by **label** and **role**; use `exact=True` or scoping to avoid strict mode violations.
- Test the initial state, conditional enabling/disabling, select-all behaviour, and the final submitted data.
- For hidden custom inputs: click the visible label, use ARIA roles, and use `force=True` only as a documented last resort.
- Avoid manipulating `.checked` through JavaScript because it skips the application's events.

---

## External Resources

- Playwright for Python, Actions (Checkboxes and radio buttons): https://playwright.dev/python/docs/input#checkboxes-and-radio-buttons
- Playwright for Python API reference, `Locator.check` and `Locator.set_checked`: https://playwright.dev/python/docs/api/class-locator#locator-check
- Playwright for Python assertions, `to_be_checked`: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-checked
