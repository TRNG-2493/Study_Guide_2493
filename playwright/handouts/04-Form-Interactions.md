# 04 — Form Interactions

> **Before you start**
>
> - **By the end you can:** tick checkboxes and select radio buttons, choose from normal and custom dropdowns, press keys and shortcuts, hover/right-click/drag, and test auto-suggestion boxes.
> - **Practice sites:**
>   - The Internet — <https://the-internet.herokuapp.com/> (most topics)
>   - jQuery UI demos — <https://jqueryui.com/resources/demos/> (custom dropdown and auto-suggestions)
> - **Create:** a folder `lecture04/` with `pytest.ini`:
>
> ```ini
> [pytest]
> base_url = https://the-internet.herokuapp.com
> ```
>
> and `test_forms.py` starting with:
>
> ```python
> from playwright.sync_api import Page, expect
> ```
>
> - **Run tests with:** `pytest -s` (add `--headed --slowmo 500` to watch)

---

## Topic 1 — Checkboxes and radio buttons

### Definition

Checkboxes can be ticked independently; radio buttons let the user pick **one** option from a group. In Playwright you set them with `check()`, `uncheck()` or `set_checked()`, and verify them with `to_be_checked()`.

### Key ideas

| Method | Does |
|---|---|
| `check()` | Tick a box / select a radio — safe to run twice |
| `uncheck()` | Untick a checkbox (**not** allowed on radios) |
| `set_checked(True/False)` | Tick or untick from a value |

- Prefer `check()` over `click()`: `click()` **toggles**, so a ticked box becomes unticked.
- Best locator: `get_by_label("...")`. If there's no label (as on The Internet), use `get_by_role("checkbox")` plus `first`/`nth`.
- Radios in one group: selecting one unselects the others — test both sides.

### Worked example — The Internet's checkboxes

**Step 1.** Open the page and count the checkboxes:

```python
def test_checkboxes(page: Page):
    page.goto("/checkboxes")
    boxes = page.get_by_role("checkbox")
    expect(boxes).to_have_count(2)
```

**Step 2.** Check their starting state:

```python
    expect(boxes.first).not_to_be_checked()
    expect(boxes.last).to_be_checked()
```

**Step 3.** Tick the first one — twice, to show `check()` is safe:

```python
    boxes.first.check()
    boxes.first.check()
    expect(boxes.first).to_be_checked()
```

**Step 4.** Loop over all of them and untick:

```python
    for box in boxes.all():
        box.uncheck()
        expect(box).not_to_be_checked()
```

> **Predict:** what would happen in Step 3 if you used `click()` twice instead of `check()` twice?

### Checkpoint

`1 passed`. In `--headed` mode you see both boxes end up unticked.

### Your turn

1. Use `set_checked(True)` on the second box, then `set_checked(False)`.
2. There are no radio buttons on The Internet, so make some! Paste this into a new test:

```python
page.set_content("""
  <label><input type="radio" name="ship" value="std"> Standard</label>
  <label><input type="radio" name="ship" value="exp"> Express</label>
""")
```

Select **Express** with `get_by_label`, then check **Standard** is not selected.
3. Try `uncheck()` on a radio button and read the error.

### Common errors

| Error | Fix |
|---|---|
| Box ends up unticked | You used `click()` on a ticked box; use `check()` |
| Error from `uncheck()` on a radio | Select a different radio instead |

---

## Topic 2 — Dropdowns: native and custom

### Definition

A normal dropdown is an HTML `<select>`; you choose from it with `select_option()`. A **custom** dropdown is built from other elements, so you click it open and click the option like a user.

### Key ideas

| Choose by | Code |
|---|---|
| Value attribute | `select_option("1")` |
| Visible label | `select_option(label="Option 1")` |
| Index (from 0) | `select_option(index=2)` |
| Several (multi-select) | `select_option(["s", "m"])` → check with `to_have_values` |

- `to_have_value` checks the **value** (`"1"`), not the label (`"Option 1"`).
- Right-click → Inspect: `<select>` → `select_option()`; anything else → click.

### Worked example — native, then custom

**Step 1.** Choose from The Internet's dropdown by label and check the value:

```python
def test_native_dropdown(page: Page):
    page.goto("/dropdown")
    dropdown = page.locator("#dropdown")
    dropdown.select_option(label="Option 2")
    expect(dropdown).to_have_value("2")
```

**Step 2.** Check all the options, in order:

```python
    expect(dropdown.locator("option")).to_have_text(
        ["Please select an option", "Option 1", "Option 2"]
    )
```

**Step 3.** A custom dropdown (jQuery UI). The real `<select>` is hidden; a `combobox` is shown instead:

```python
def test_custom_dropdown(page: Page):
    page.goto("https://jqueryui.com/resources/demos/selectmenu/default.html")
    page.get_by_role("combobox", name="Select a speed").click()
```

**Step 4.** Click the option and check the result:

```python
    page.get_by_role("option", name="Fast", exact=True).click()
    expect(page.get_by_role("combobox", name="Select a speed")).to_have_text("Fast")
```

> **Predict:** why is `exact=True` needed on "Fast"?

### Checkpoint

`2 passed`.

### Your turn

1. Select **Option 1** by value and then by index. Check the value both times.
2. Try `page.get_by_role("combobox", name="Select a speed").select_option("Slow")`. Read the error.
3. Make a multi-select with `page.set_content('<select multiple aria-label="Sizes"><option>S</option><option>M</option><option>L</option></select>')`, choose S and L, and check with `to_have_values`.
   *Hint: with no `value=` attribute, the value is the text.*

### Common errors

| Error | Fix |
|---|---|
| `select_option` fails with "not a `<select>` element" | Custom dropdown: click to open, click the option |
| `to_have_value("Option 2")` fails | Use the value: `"2"` |
| `to_have_value` on a multi-select | Use `to_have_values` |

---

## Topic 3 — Keyboard actions

### Definition

`locator.press(key)` focuses an element and presses a key or combination. `page.keyboard` is the keyboard itself: it presses keys or types text wherever the focus currently is — useful for shortcuts and Tab navigation.

### Key ideas

- Key names: `Enter`, `Tab`, `Escape`, `Backspace`, `ArrowUp`, `Home`, `F1`, `a`, `A`.
- Combinations use `+`: `Shift+A`, `ControlOrMeta+A`.
- **`ControlOrMeta`** = Ctrl on Windows/Linux, Cmd on macOS — use it for shortcuts.

| Method | Use when |
|---|---|
| `fill("text")` | Normal text entry (default) |
| `press_sequentially("text")` | Page reacts to each key |
| `locator.press("Enter")` | One key on an element |
| `page.keyboard.press()` / `.type()` | Shortcuts, or typing where focus is |

### Worked example — key presses and Tab navigation

**Step 1.** The Key Presses page reports the last key:

```python
def test_keyboard(page: Page):
    page.goto("/key_presses")
    page.locator("#target").press("Enter")
    expect(page.locator("#result")).to_have_text("You entered: ENTER")
```

**Step 2.** Try another key:

```python
    page.locator("#target").press("Escape")
    expect(page.locator("#result")).to_have_text("You entered: ESCAPE")
```

**Step 3.** On the login page, fill the username and Tab to the next field:

```python
    page.goto("/login")
    page.get_by_label("Username").fill("tomsmith")
    page.keyboard.press("Tab")
    expect(page.get_by_label("Password")).to_be_focused()
```

**Step 4.** Type into the focused field and submit with Enter:

```python
    page.keyboard.type("SuperSecretPassword!")
    page.keyboard.press("Enter")
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
```

> **Predict:** in Step 3, which element has focus if you press Tab **twice**?

### Checkpoint

`1 passed`, ending on the Secure Area page.

### Your turn

1. On `/inputs`, click the number field, press `ArrowUp` three times and check the value is `"3"`.
   *Hint: `press("ArrowUp")` in a loop, or `repeat` it yourself.*
2. On `/key_presses`, press `Shift+A`. What does the page report?
3. Type `hello` into `#target`, press `ControlOrMeta+A`, then `Backspace`. Check it is empty.

---

## Topic 4 — Mouse actions

### Definition

Mouse actions beyond a plain click — hover, double-click, right-click and drag and drop — are methods on a locator. `page.mouse` gives low-level control (down, up, move) when the high-level methods don't work.

### Key ideas

| Action | Code |
|---|---|
| Hover | `locator.hover()` |
| Double-click | `locator.dblclick()` |
| Right-click | `locator.click(button="right")` |
| Click with Shift | `locator.click(modifiers=["Shift"])` |
| Drag and drop | `source.drag_to(target)` |

- Prefer locators over pixel coordinates — layouts change.

### Worked example — hover, right-click and drag

**Step 1.** Captions on `/hovers` are hidden until you hover:

```python
def test_hover(page: Page):
    page.goto("/hovers")
    caption = page.get_by_text("name: user1")
    expect(caption).to_be_hidden()
```

**Step 2.** Hover over the first avatar:

```python
    page.get_by_alt_text("User Avatar").first.hover()
    expect(caption).to_be_visible()
    expect(page.get_by_role("link", name="View profile").first).to_be_visible()
```

**Step 3.** Drag box A onto box B:

```python
def test_drag_and_drop(page: Page):
    page.goto("/drag_and_drop")
    page.locator("#column-a").drag_to(page.locator("#column-b"))
```

**Step 4.** The boxes swap places:

```python
    expect(page.locator("#column-a header")).to_have_text("B")
    expect(page.locator("#column-b header")).to_have_text("A")
```

> **Predict:** in Step 2, why is `.first` needed on the avatar?

### Checkpoint

`2 passed`. In `--headed` mode you see the caption appear and the boxes swap.

### Your turn

1. Hover over the **third** avatar and check `name: user3` is visible.
2. Rewrite Step 3 using `page.mouse.down()` / `page.mouse.up()`.
   *Hint: hover the source, press down, hover the target, release.*
3. On `/context_menu`, right-click the box. It opens a browser alert — accept it with `page.once("dialog", lambda d: d.accept())` **before** the right-click (dialogs are covered in Lecture 6).

---

## Topic 5 — Auto-suggestions

### Definition

An auto-suggestion box (autocomplete, type-ahead) shows matching options **while you type**. To test one: type, wait for the list, pick an option, check the result.

### Key ideas

1. Type with `press_sequentially` (or `fill`, if the box reacts to it).
2. **Wait for the list** with `expect(...).to_have_count(n)`.
3. Pick by clicking, or with `ArrowDown` + `Enter`.
4. Check the input's value.

- **Scope your locator** to the suggestions list, not the whole page.

### Worked example — pick a language (jQuery UI)

**Step 1.** Open the demo and type into **Tags**:

```python
AUTOCOMPLETE = "https://jqueryui.com/resources/demos/autocomplete/default.html"


def test_pick_with_mouse(page: Page):
    page.goto(AUTOCOMPLETE)
    page.get_by_label("Tags").press_sequentially("ja")
```

**Step 2.** Wait for the list:

```python
    suggestions = page.locator("ul.ui-autocomplete li")
    expect(suggestions).to_have_count(2)
    expect(suggestions).to_have_text(["Java", "JavaScript"])
```

**Step 3.** Pick one and check the result:

```python
    suggestions.filter(has_text="JavaScript").click()
    expect(page.get_by_label("Tags")).to_have_value("JavaScript")
```

> **Predict:** what would `suggestions.filter(has_text="Java").click()` do?

### Checkpoint

`1 passed`. The Tags box shows "JavaScript".

### Your turn

1. Write `test_pick_with_keyboard`: type `ja`, wait for 2 suggestions, then `ArrowDown` + `Enter`. Which one is picked?
2. Type `sc`. How many suggestions appear? Pick **Scala**.
   *Hint: matches can be anywhere in the word.*
3. Replace `press_sequentially` with `fill`. Does it still work on this page?

### Common errors

| Error | Fix |
|---|---|
| Strict mode error when picking | `has_text` matched two options; be more specific or use `get_by_text(..., exact=True)` |
| Click happens before the list appears | `expect` the list first |
| `fill` shows no suggestions on another site | Use `press_sequentially` |

---

## Stretch challenge

On The Internet's `/dynamic_controls`, click **Remove**, wait for the checkbox to disappear, click **Add**, wait for it to return, then tick it with `check()`. Then on `/dropdown`, write a `for` loop that selects each option in turn and checks its value.

## Exit ticket

1. Why is `check()` safer than `click()` for a checkbox?
2. How can you tell whether to use `select_option()` or two clicks for a dropdown?
3. Why use `ControlOrMeta` instead of `Control`?

## Cheat sheet

| Code | Purpose |
|---|---|
| `check()` / `uncheck()` / `set_checked(bool)` | Radios and checkboxes |
| `expect(loc).to_be_checked()` | Is ticked / selected |
| `select_option("value")` / `(label=...)` / `(index=...)` | Native dropdown |
| `select_option(["a", "b"])` + `to_have_values` | Multi-select |
| Click `combobox` → click `option` | Custom dropdown |
| `page.set_content("<html>...")` | Quick practice HTML, no file needed |
| `loc.press("ControlOrMeta+A")` | Key combination |
| `page.keyboard.press("Tab")` / `.type("text")` | Keyboard itself |
| `expect(loc).to_be_focused()` | Has focus |
| `hover()`, `dblclick()`, `click(button="right")` | Mouse actions |
| `source.drag_to(target)` | Drag and drop |
| `page.mouse.down()` / `.up()` | Low-level mouse |
| `press_sequentially("ja")` → `expect(list).to_have_count(n)` → click | Auto-suggestions |
