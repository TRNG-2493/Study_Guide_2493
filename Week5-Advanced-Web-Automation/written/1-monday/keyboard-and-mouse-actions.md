# Keyboard and Mouse Actions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between the high-level element actions (`click`, `fill`, `press`) and the low-level device APIs (`page.keyboard` and `page.mouse`), and choose between them.
- Type text three different ways (`fill`, `press_sequentially`, `keyboard.type`) and say when each is appropriate.
- Press single keys, special keys (`Enter`, `Tab`, `Escape`, arrow keys) and **shortcuts** (`Control+A`, `Shift+Tab`) with `press()`, and hold keys down with `keyboard.down()` / `keyboard.up()`.
- Perform mouse actions: hover, double-click, right-click, click with modifier keys, click at a position, and scroll with the wheel.
- Drag and drop using `drag_to()`, `page.drag_and_drop()`, and the low-level `mouse.move/down/up` sequence for pages where the high-level call is not enough.
- Test hover menus, tooltips and context menus.
- Verify the effects of keyboard and mouse input using `expect(...)`.
- Recognise the pitfalls: lost focus, missing key events, coordinates that depend on the viewport, and animations.

---

## Why This Matters

The Week 5 epic is about mastering complex UI interactions. So far you have mostly used four verbs: *go to*, *click*, *fill* and *check*. Real users do much more. They press Enter to submit a search, Tab through form fields, use Ctrl+A to select all text, hover over a menu to reveal sub-items, double-click to edit a cell, right-click to open a context menu, and drag cards across a Kanban board. If your automation only knows how to click and fill, entire families of features remain untested, and these features are precisely the ones most likely to have bugs because they involve timing, focus and several events working together.

Keyboard and mouse handling is also directly relevant to **accessibility**. Many users cannot use a mouse at all. A professional QE checks that a form can be completed using only the keyboard (correct Tab order, Enter submits, Escape closes dialogs). Playwright makes these checks straightforward.

For **Project 1: QE Foundations**, the UI milestone asks you to automate a complex form flow. Complex flows include keyboard shortcuts, hover-revealed controls, and sometimes drag-and-drop. This lesson gives you the vocabulary and the working examples.

---

## The Concept

### 1. Two levels of interaction

Playwright offers two layers for simulating user input.

**Level 1: Element actions (high level).** Methods on a locator, such as `locator.click()`, `locator.fill("text")`, `locator.press("Enter")`, `locator.hover()`, `locator.dblclick()`, `locator.drag_to(other)`. These are the ones you should reach for first. Before acting, they automatically perform **actionability checks**: wait until the element exists, is visible, is stable (not moving), is enabled, and is not covered by another element; then scroll it into view and perform the action at the right coordinates. If anything is wrong, they wait and retry until the timeout.

**Level 2: Device APIs (low level).** `page.keyboard` and `page.mouse` simulate the physical keyboard and mouse *without any element awareness*. `page.keyboard.press("Enter")` presses Enter on **whatever currently has focus**. `page.mouse.click(120, 340)` clicks the pixel at x=120, y=340 *whatever is there*. There are no waits, no scrolling, no checks. They are the right tools for things that do not belong to a single element: global shortcuts, canvas drawing, sliders, custom drag operations, and when you want to simulate raw sequences.

A good rule: **use locator methods unless you have a reason not to.** Use the device APIs when you need precise control of the sequence or the page has no useful element to target.

An analogy: locator actions are like asking a helpful assistant, "Please press the 'Save' button" (the assistant finds it and makes sure it is reachable). The device APIs are like grabbing the mouse yourself: "move to coordinates 400, 300 and press"; you get complete control, and complete responsibility.

### 2. Typing text: `fill`, `press_sequentially`, and `keyboard.type`

There are three ways to put text into a field, and they behave differently.

#### `locator.fill(text)`

Focuses the element, selects and replaces its content, and sets the text **in one step**, firing one `input` event. It is fast and reliable and is the default choice for normal form fields. Because it clears existing content first, filling twice does not append. `fill("")` clears a field (or use `locator.clear()`).

Limitation: it does not generate individual `keydown`, `keypress`, `keyup` events for each character. If the page reacts to those (for example an auto-suggest list or a live character counter listening to `keyup`), `fill` may appear to do nothing.

#### `locator.press_sequentially(text, delay=...)`

Focuses the element and presses the keys **one character at a time**, generating the full key event sequence for each character, exactly as a user typing. `delay` is the pause in milliseconds between keystrokes (default 0). It *appends* at the current caret position (it does not clear the field first).

> **Name note.** In older Playwright versions this method was called `type()`. The current name is `press_sequentially()` and `type()` is deprecated. You will see both in older tutorials; write `press_sequentially`.

```python
box.press_sequentially("playwright", delay=100)
```

Use it when the page depends on key events: typeahead, input masks (phone number formatting), live validation, search-as-you-type. The next lesson (auto-suggestions) builds on this.

#### `page.keyboard.type(text)` and `page.keyboard.insert_text(text)`

`keyboard.type` types text into **whatever currently has focus**, character by character, without targeting an element. `keyboard.insert_text` inserts the text in one go **without key events** (like pasting); it only fires an `input` event.

| Method | Targets an element? | Clears first? | Key events per character? | Typical use |
|---|---|---|---|---|
| `locator.fill()` | Yes | Yes | No (one `input` event) | Normal form fields |
| `locator.press_sequentially()` | Yes | No | Yes | Search-as-you-type, masks |
| `page.keyboard.type()` | No (current focus) | No | Yes | When focus is already set |
| `page.keyboard.insert_text()` | No (current focus) | No | No | Simulating paste |

### 3. Pressing keys: `press()`

`locator.press(key)` focuses the element and presses a key; `page.keyboard.press(key)` presses it on the current focus.

```python
page.get_by_role("textbox", name="Search").press("Enter")
page.keyboard.press("Escape")
```

A key is described by a **key name**. The names are those of the DOM `KeyboardEvent.key` and `code` values:

- Letters and digits: `"a"`, `"A"`, `"7"` (lowercase `a` types a lowercase letter; `"A"` types uppercase, and `"Shift+a"` also does).
- Named keys: `"Enter"`, `"Tab"`, `"Escape"`, `"Backspace"`, `"Delete"`, `"Space"` (or `" "`), `"ArrowUp"`, `"ArrowDown"`, `"ArrowLeft"`, `"ArrowRight"`, `"Home"`, `"End"`, `"PageUp"`, `"PageDown"`, `"F1"` to `"F12"`.
- Modifiers: `"Shift"`, `"Control"`, `"Alt"`, `"Meta"` (Command on macOS, Windows key on Windows).
- Special: `"ControlOrMeta"` is a modifier that means Control on Windows/Linux and Meta (Command) on macOS, which is perfect for cross-platform shortcuts such as select all or copy.

**Shortcuts (combinations)** join keys with `+`. The modifiers are held while the final key is pressed, then released:

```python
page.keyboard.press("Control+A")        # select all (Windows/Linux)
page.keyboard.press("ControlOrMeta+A")  # select all on any operating system
page.keyboard.press("Shift+Tab")        # move focus backwards
page.keyboard.press("Control+Shift+T")  # more than one modifier
```

Case matters for names: `"Enter"` is correct, `"enter"` is not. If you mistype a key name, Playwright raises an error listing valid keys.

### 4. Holding keys: `keyboard.down()` and `keyboard.up()`

`press` is really `down` followed by `up`. Use them separately when you need to hold a key while doing something else, for instance, holding **Shift** while clicking items to select a range:

```python
page.keyboard.down("Shift")
page.get_by_text("Item 5").click()
page.keyboard.up("Shift")
```

For clicks with modifiers there is a neater option, `click(modifiers=["Shift"])`, shown below. Remember that anything you hold with `down()` stays held until you `up()` it, even if your test fails midway, which can affect later steps in the same page. Use `try/finally` if you must hold keys across assertions.

### 5. Keyboard navigation and focus

Focus is the browser's idea of *which element receives the keyboard right now*. Typing, Enter and Space go to the focused element. Useful tools:

- `locator.focus()`: moves focus to an element without clicking.
- `locator.blur()`: removes focus (it triggers `blur`/`change` validation on many forms).
- `expect(locator).to_be_focused()`: asserts that the element has focus.
- `page.keyboard.press("Tab")`: moves to the next focusable element in tab order; `"Shift+Tab"` moves backwards.

A classic accessibility test walks the page with Tab and asserts the order of focus:

```python
for expected in ["Name", "Email", "Subscribe"]:
    page.keyboard.press("Tab")
    expect(page.get_by_label(expected)).to_be_focused()
```

### 6. Mouse actions on elements

Locator-level mouse methods:

| Goal | Code |
|---|---|
| Normal click | `locator.click()` |
| Double-click | `locator.dblclick()` |
| Right-click (context menu) | `locator.click(button="right")` |
| Middle-click | `locator.click(button="middle")` |
| Hover (move the mouse over) | `locator.hover()` |
| Click with Shift/Ctrl/Alt/Meta held | `locator.click(modifiers=["Shift"])` or `["ControlOrMeta"]` |
| Click at a point inside the element | `locator.click(position={"x": 10, "y": 5})` |
| Click several times | `locator.click(click_count=3)` (triple-click selects a paragraph) |
| Slow click with delay between down/up | `locator.click(delay=200)` (long-press) |
| Check it can be clicked, but don't | `locator.click(trial=True)` |

**Hover** deserves attention. Many UIs show content only when the mouse is over an element: dropdown navigation menus, tooltips, "edit" icons on table rows, image captions. The standard approach is `hover()` then assert the new element:

```python
page.get_by_role("link", name="Products").hover()
expect(page.get_by_role("link", name="Laptops")).to_be_visible()
page.get_by_role("link", name="Laptops").click()
```

Note that `click()` also moves the mouse over the element first, so hover effects *do* trigger during a click; `hover()` is for when you want to act on the revealed content or assert it.

One important behaviour: Playwright's mouse is a single virtual pointer. After `hover()` it stays there until you move it. If you hover a menu item and then click a sub-item, the mouse moves from the menu to the sub-item; if there is a gap between them that leaves the hover region, the menu may close. That is normal browser behaviour, and a good test sometimes finds real usability bugs this way.

**Scrolling.** Actions scroll elements into view automatically. To scroll explicitly, `locator.scroll_into_view_if_needed()` or the wheel: `page.mouse.wheel(0, 500)` scrolls down 500 pixels (arguments are `delta_x`, `delta_y`). Use the wheel for infinite-scroll features, which load more content as the user nears the bottom.

### 7. The low-level mouse: `page.mouse`

Methods (coordinates are in **CSS pixels relative to the top-left of the viewport**, which is the visible part of the page):

- `page.mouse.move(x, y, steps=1)`: move the pointer. `steps` makes it move in several intermediate steps, which produces intermediate `mousemove` events, essential for drag operations and hover effects triggered by movement.
- `page.mouse.down()` / `page.mouse.up()`: press and release the left button (`button="right"` for others).
- `page.mouse.click(x, y)`: a move, down and up in one call; also `dblclick(x, y)`.
- `page.mouse.wheel(dx, dy)`: scroll.

To get coordinates of an element, use its **bounding box**:

```python
box = page.locator("#slider-handle").bounding_box()
# box is a dict: {"x": ..., "y": ..., "width": ..., "height": ...} or None if not visible
cx = box["x"] + box["width"] / 2
cy = box["y"] + box["height"] / 2
```

`bounding_box()` returns the position relative to the viewport at the moment of the call. If the page scrolls afterwards, the numbers are outdated. Compute immediately before use. It returns `None` if the element is not visible, so guard against that in real code (`assert box is not None`).

### 8. Drag and drop

Dragging means: press the mouse over a source, move to a target, release. There are three Playwright approaches.

**(a) `source.drag_to(target)`**: the simplest. Playwright hovers over the source, presses the mouse, moves to the target and releases. It works for most HTML5 drag-and-drop implementations (the browser's `draggable="true"` mechanism) and for libraries that rely on mouse events.

```python
page.locator("#card-1").drag_to(page.locator("#column-done"))
```

Optional parameters allow positions inside source and target (`source_position={"x": 5, "y": 5}`, `target_position={...}`), useful when you must drop on a specific part of the target, such as the top half of a list item to insert *before* it.

**(b) `page.drag_and_drop(source_selector, target_selector)`**: the same idea using selector strings rather than locators. Both are equivalent; the locator version is preferred in modern code.

**(c) Manual sequence** with the low-level mouse, for sliders, canvases, sortable lists that need extra intermediate movement:

```python
page.locator("#handle").hover()
page.mouse.down()
page.mouse.move(target_x, target_y, steps=15)
page.mouse.up()
```

The `hover()` positions the pointer on the handle; `down()` presses; `move(..., steps=15)` drags in 15 small increments (many drag libraries require several `mousemove` events before they recognise a drag; a single jump is not enough); `up()` drops.

After a drag, always **assert the result**: the order of items changed, the card is in the new column, or the slider value updated. Drag operations fail silently, so assertions are what give them meaning.

### 9. Context menus and double-clicks

A right-click triggers the `contextmenu` event. Custom context menus (rendered in HTML) appear as new elements you then click normally. The *browser's native* context menu is not part of the page and cannot be controlled, and it normally does not appear in automated browsers, so only custom ones are testable.

Double-click triggers `dblclick`, typically to edit a table cell inline or open an item. After `dblclick()`, the typical next step is typing into the now-visible editor and pressing Enter to commit or Escape to cancel.

### 10. Verifying outcomes

An action without verification is only half a test. The standard assertions:

```python
expect(locator).to_have_text("...")        # text content
expect(locator).to_have_value("...")       # input value
expect(locator).to_be_focused()            # keyboard focus
expect(locator).to_be_visible()            # hover-revealed content
expect(locator).to_have_class(re.compile("active"))   # state classes
expect(locator).to_have_css("background-color", "rgb(255, 0, 0)")
expect(page).to_have_url(re.compile("/results"))
```

All of these retry automatically until they pass or time out; this handles small delays from animations and transitions.

---

## Code Examples

All examples use Python with the sync API and pytest-playwright (`page` fixture). Real-site examples use the public practice site **The Internet** (`https://the-internet.herokuapp.com`). To keep a couple of examples deterministic, we use `page.set_content()` with inline HTML.

### Example 1: Key presses on a real page

The page `/key_presses` has an input `#target`; when a key is pressed it writes "You entered: KEYNAME" into `#result`.

```python
from playwright.sync_api import Page, expect


def test_key_presses(page: Page):
    page.goto("https://the-internet.herokuapp.com/key_presses")
    target = page.locator("#target")
    result = page.locator("#result")

    target.press("Enter")
    expect(result).to_have_text("You entered: ENTER")

    target.press("Tab")
    expect(result).to_have_text("You entered: TAB")

    target.press("a")
    expect(result).to_have_text("You entered: A")

    page.keyboard.press("ArrowLeft")
    expect(result).to_have_text("You entered: LEFT")
```

**Line by line**

1. `target = page.locator("#target")`: the input box. `result` is where the page reports the key.
2. `target.press("Enter")`: focuses `#target` and presses Enter. The page's key handler writes the message.
3. `expect(result).to_have_text("You entered: ENTER")`: verifies the effect.
4. `target.press("Tab")`: pressing Tab normally moves focus away from the input (the page still reports the key). Because focus has left, this is why the *next* line, `target.press("a")`, re-focuses the input as part of `locator.press` (a locator action focuses its element first).
5. `page.keyboard.press("ArrowLeft")`: here we use the device keyboard: it sends the key to whatever has focus, which is `#target` after the previous line. Focus is why it works.

### Example 2: Three ways to type

```python
from playwright.sync_api import Page, expect

PAGE = """
<input id="plain" aria-label="Plain">
<input id="live" aria-label="Live">
<p id="keys"></p>
<script>
  live.addEventListener('keyup', e => keys.textContent += e.key + ' ');
</script>
"""


def test_three_ways_to_type(page: Page):
    page.set_content(PAGE)
    plain = page.get_by_label("Plain")
    live = page.get_by_label("Live")

    # 1. fill: sets the whole value at once (one input event, NO keyup events)
    live.fill("abc")
    expect(live).to_have_value("abc")
    expect(page.locator("#keys")).to_have_text("")

    # 2. press_sequentially: real key events, appends to the current value
    live.press_sequentially("de", delay=50)
    expect(live).to_have_value("abcde")
    expect(page.locator("#keys")).to_have_text("d e")

    # 3. keyboard.type goes to the focused element
    plain.focus()
    page.keyboard.type("hello")
    expect(plain).to_have_value("hello")

    # keyboard.insert_text behaves like paste: text appears, but no key events
    page.keyboard.insert_text(" world")
    expect(plain).to_have_value("hello world")
```

**Explanation**

- The page has a `keyup` listener on `#live` that appends every key name to the paragraph. This lets us *see* which approach generates key events.
- `live.fill("abc")`: value changes but the paragraph stays empty. This is the reason `fill` can fail with typeahead widgets.
- `live.press_sequentially("de", delay=50)`: the value appends ("abcde") and the paragraph records `d` and `e`. (`to_have_text` normalises whitespace so "d e " matches "d e".) The 50 ms delay mimics human typing.
- `plain.focus()` places focus; `keyboard.type("hello")` types into it.
- `keyboard.insert_text(" world")` pastes text, with no key events. Notice how all of these lines end in `expect`: after each action we verify.

### Example 3: Shortcuts, select all, and replacing text

```python
from playwright.sync_api import Page, expect


def test_select_all_and_replace(page: Page):
    page.set_content('<textarea id="note" aria-label="Note"></textarea>')
    note = page.get_by_label("Note")

    note.fill("First draft")
    note.focus()
    page.keyboard.press("ControlOrMeta+A")      # select everything in the textarea
    page.keyboard.press("Backspace")            # delete the selection
    expect(note).to_have_value("")

    note.press_sequentially("Second draft")
    page.keyboard.press("Shift+Home")           # select from the caret to the start of the line
    page.keyboard.press("Delete")
    expect(note).to_have_value("")
```

**Explanation**

- `ControlOrMeta+A` works on every operating system; `Control+A` would not select all on macOS.
- `Backspace` deletes the selected text; the `expect` verifies the field is empty.
- After typing again, `Shift+Home` extends the selection from the caret (at the end) to the beginning of the line, and `Delete` removes it. This shows how multi-key shortcuts and navigation keys combine.
- For plain clearing you would use `note.clear()` or `fill("")`; this example is for testing *shortcut behaviour* itself.

### Example 4: Tab order and keyboard-only form completion

```python
from playwright.sync_api import Page, expect

FORM = """
<form>
  <label>Name <input id="n"></label>
  <label>Email <input id="e" type="email"></label>
  <label><input id="s" type="checkbox"> Subscribe</label>
  <button id="go" type="submit">Send</button>
</form>
<p id="out"></p>
<script>
  document.querySelector('form').addEventListener('submit', ev => {
    ev.preventDefault();
    out.textContent = 'Sent ' + n.value + ' ' + e.value + ' ' + s.checked;
  });
</script>
"""


def test_keyboard_only_form(page: Page):
    page.set_content(FORM)

    page.get_by_label("Name").focus()
    page.keyboard.type("Ada")
    page.keyboard.press("Tab")
    expect(page.get_by_label("Email")).to_be_focused()

    page.keyboard.type("ada@example.com")
    page.keyboard.press("Tab")
    expect(page.get_by_label("Subscribe")).to_be_focused()

    page.keyboard.press("Space")               # Space toggles a focused checkbox
    expect(page.get_by_label("Subscribe")).to_be_checked()

    page.keyboard.press("Tab")
    expect(page.get_by_role("button", name="Send")).to_be_focused()
    page.keyboard.press("Enter")               # Enter activates a focused button

    expect(page.locator("#out")).to_have_text("Sent Ada ada@example.com true")
```

**Explanation**

- The test never touches the mouse. It sets the initial focus with `focus()`, types text with `keyboard.type`, and moves through the fields with `Tab`.
- After each Tab it asserts `to_be_focused()`. This checks the **tab order**, an accessibility requirement.
- `Space` toggles a focused checkbox; `Enter` presses the focused button.
- The last assertion confirms the form submitted the right data. A single test thus covers keyboard accessibility *and* functionality.

### Example 5: Hover, using a real page

On `/hovers`, three profile images each reveal a caption ("name: user1" etc.) on hover.

```python
from playwright.sync_api import Page, expect


def test_hover_reveals_caption(page: Page):
    page.goto("https://the-internet.herokuapp.com/hovers")
    figures = page.locator(".figure")
    expect(figures).to_have_count(3)

    for index in range(3):
        figure = figures.nth(index)
        caption = figure.locator(".figcaption")

        expect(caption).to_be_hidden()
        figure.hover()
        expect(caption).to_be_visible()
        expect(caption.locator("h5")).to_have_text(f"name: user{index + 1}")
```

**Line by line**

1. `figures = page.locator(".figure")`: all three cards. `to_have_count(3)` waits until all exist.
2. `for index in range(3):` loops over 0, 1, 2. `figures.nth(index)` selects the card; `figure.locator(".figcaption")` is the caption *inside that card* (scoped locator).
3. `expect(caption).to_be_hidden()`: before hovering the caption should not be visible. Asserting the "before" state proves the hover is what changes things.
4. `figure.hover()`: moves the mouse over the card.
5. `expect(caption).to_be_visible()` then checks the text with an f-string: `f"name: user{index + 1}"` inserts the number into the string (user1, user2, user3).

### Example 6: Double-click, right-click and modifier clicks

```python
from playwright.sync_api import Page, expect

PAGE = """
<button id="dbl">Double</button><p id="d"></p>
<button id="ctx">Context</button><p id="c"></p>
<button id="mod">Modifier</button><p id="m"></p>
<script>
  dbl.addEventListener('dblclick', () => d.textContent = 'double');
  ctx.addEventListener('contextmenu', e => { e.preventDefault(); c.textContent = 'right'; });
  mod.addEventListener('click', e => m.textContent = (e.shiftKey ? 'shift ' : '') + (e.ctrlKey ? 'ctrl' : ''));
</script>
"""


def test_mouse_variants(page: Page):
    page.set_content(PAGE)

    page.get_by_role("button", name="Double").dblclick()
    expect(page.locator("#d")).to_have_text("double")

    page.get_by_role("button", name="Context").click(button="right")
    expect(page.locator("#c")).to_have_text("right")

    page.get_by_role("button", name="Modifier").click(modifiers=["Shift", "Control"])
    expect(page.locator("#m")).to_have_text("shift ctrl")
```

**Explanation**

- Each button has a listener for a different mouse event.
- `dblclick()` generates two quick clicks and a `dblclick` event.
- `click(button="right")` generates a `contextmenu` event; the script calls `preventDefault()` to suppress the browser's own menu and writes "right".
- `click(modifiers=["Shift", "Control"])` presses the modifier keys down, clicks, then releases them, so the click event has `shiftKey` and `ctrlKey` set to `true`. The page's text shows `shift ctrl`.

### Example 7: Context menu on a real page (connecting to dialogs)

The `/context_menu` page shows a box (`#hot-spot`) that, when right-clicked, triggers a JavaScript `alert`.

```python
from playwright.sync_api import Page, expect


def test_context_menu_alert(page: Page):
    page.goto("https://the-internet.herokuapp.com/context_menu")
    messages = []

    def on_dialog(dialog):
        messages.append(dialog.message)
        dialog.accept()

    page.once("dialog", on_dialog)
    page.locator("#hot-spot").click(button="right")

    expect(page.locator("#hot-spot")).to_be_visible()   # gives the handler time to run
    assert messages == ["You selected a context menu"]
```

**Explanation:** This combines this lesson with the previous one on dialogs. We register the dialog handler **before** the action, perform a right-click, and then assert the message. The right-click is made by the locator with `button="right"`.

### Example 8: Drag and drop, high-level

The `/drag_and_drop` page has two boxes, A and B; dragging A onto B swaps them.

```python
from playwright.sync_api import Page, expect


def test_drag_and_drop_swaps_columns(page: Page):
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    column_a = page.locator("#column-a")
    column_b = page.locator("#column-b")

    expect(column_a.locator("header")).to_have_text("A")
    expect(column_b.locator("header")).to_have_text("B")

    column_a.drag_to(column_b)

    expect(column_a.locator("header")).to_have_text("B")
    expect(column_b.locator("header")).to_have_text("A")
```

**Explanation**

- `drag_to(column_b)` performs press, move and release.
- Because drag-and-drop silently does nothing when it fails, the four `expect` lines (two before, two after) are what make the test meaningful.
- This page uses the browser's HTML5 drag-and-drop API, which `drag_to` supports. If a different site's drag does not register, fall back to the manual sequence in the next example.

### Example 9: Manual drag with the low-level mouse (a slider)

```python
from playwright.sync_api import Page, expect

SLIDER = """
<div id="track" style="position:relative;width:300px;height:10px;background:#ccc;margin:40px">
  <div id="handle" style="position:absolute;left:0;top:-8px;width:24px;height:24px;background:#27a;border-radius:50%"></div>
</div>
<p id="pct">0</p>
<script>
  const handle = document.getElementById('handle'), track = document.getElementById('track');
  let dragging = false;
  handle.addEventListener('mousedown', () => dragging = true);
  window.addEventListener('mouseup', () => dragging = false);
  window.addEventListener('mousemove', e => {
    if (!dragging) return;
    const r = track.getBoundingClientRect();
    const x = Math.min(Math.max(e.clientX - r.left, 0), r.width);
    handle.style.left = (x - 12) + 'px';
    document.getElementById('pct').textContent = Math.round(x / r.width * 100);
  });
</script>
"""


def test_slider_drag(page: Page):
    page.set_content(SLIDER)

    handle_box = page.locator("#handle").bounding_box()
    track_box = page.locator("#track").bounding_box()
    assert handle_box is not None and track_box is not None

    start_x = handle_box["x"] + handle_box["width"] / 2
    start_y = handle_box["y"] + handle_box["height"] / 2
    end_x = track_box["x"] + track_box["width"] / 2        # the middle of the track

    page.mouse.move(start_x, start_y)
    page.mouse.down()
    page.mouse.move(end_x, start_y, steps=20)
    page.mouse.up()

    expect(page.locator("#pct")).to_have_text("50")
```

**Line by line**

1. The HTML draws a track and a draggable handle. The script listens for `mousedown` on the handle and `mousemove`/`mouseup` on the window and converts the pointer position into a percentage. Notice that **it only works if it sees real `mousemove` events**; this is why a single jump would fail.
2. `bounding_box()` gives each element's rectangle `{x, y, width, height}` in viewport coordinates. The `assert ... is not None` line protects against a missing/hidden element and makes the type checker happy.
3. `start_x`/`start_y` is the centre of the handle, `end_x` the centre of the track.
4. `page.mouse.move(start_x, start_y)` places the pointer on the handle. `page.mouse.down()` presses.
5. `page.mouse.move(end_x, start_y, steps=20)` drags in 20 small steps, each producing a `mousemove`.
6. `page.mouse.up()` releases.
7. `expect(#pct).to_have_text("50")` verifies the slider moved to the 50 percent mark. Because the handle is centred on the pointer, the pointer is exactly mid-track, giving 50.

### Example 10: Hover menu followed by a click

```python
import re

from playwright.sync_api import Page, expect

MENU = """
<style>
  nav li ul { display:none; position:absolute; margin:0; padding:0; }
  nav li:hover ul { display:block; }
</style>
<nav><ul>
  <li><a href="#">Products</a>
    <ul><li><a id="laptops" href="#laptops">Laptops</a></li></ul>
  </li>
</ul></nav>
"""


def test_hover_menu(page: Page):
    page.set_content(MENU)

    sub_item = page.get_by_role("link", name="Laptops")
    expect(sub_item).to_be_hidden()

    page.get_by_role("link", name="Products").hover()
    expect(sub_item).to_be_visible()

    sub_item.click()
    expect(page).to_have_url(re.compile(r"#laptops$"))
```

**Explanation:** the sub-menu appears only while the pointer is over the `<li>`. `hover()` reveals it; `click()` on the sub-item moves the pointer onto the sub-menu (which is *inside* the hovered `<li>`, so the menu stays open) and clicks. `re.compile(r"#laptops$")` is a regular expression for "URL ends with #laptops", useful because the full URL is `about:blank#laptops` in this demo.

---

## Real-World Scenarios

**Scenario 1: Search-as-you-type with Enter.** A store's search box suggests products as you type and submits on Enter. The test uses `press_sequentially` to trigger suggestions, asserts that they appear, then `press("Enter")` and asserts the URL and the result count. Using `fill` would skip the suggestions.

**Scenario 2: Spreadsheet-style web grid.** Users double-click a cell to edit, type, and press Enter to commit or Escape to cancel. A test covers each: `dblclick()`, `press_sequentially("42")`, `press("Enter")` and verification of the committed cell; then repeat with `Escape` and verify the original value stayed. Arrow-key navigation between cells is another test (`page.keyboard.press("ArrowDown")` then assert focus or an "active" class).

**Scenario 3: Kanban board.** Cards move from "To do" to "Done" by dragging. The test uses `drag_to`, then asserts that the card is a child of the "Done" column (`expect(page.locator("#done .card")).to_have_text([...])`), and reloads the page to confirm persistence. If the board uses a library needing intermediate movement, the manual mouse sequence is used.

**Scenario 4: Navigation menus on a retail site.** Mega-menus open on hover. A test hovers each top-level category and checks the sub-categories are visible; another test verifies that the same menu works with the keyboard (Tab to the item, Enter or arrow keys to open, Escape to close), which is an accessibility requirement.

**Scenario 5: Rich text editor.** Typing, formatting shortcuts (`ControlOrMeta+B` for bold), undo (`ControlOrMeta+Z`) and selection (`Shift+ArrowRight` repeated). The test types text, selects a word with a double-click, applies bold via the shortcut, and verifies the HTML contains `<strong>`.

**Scenario 6: Image or map canvas.** A drawing app has a `<canvas>`; there are no elements to target inside it. The test uses `bounding_box()` of the canvas and the low-level mouse to draw a line (`move`, `down`, `move`, `up`), then checks the exported data or a screenshot. (Screenshot comparison is a topic for later in the week.)

---

## Common Pitfalls and Best Practices

1. **Using `fill` where key events are needed.** If a typeahead or mask "does nothing", switch to `press_sequentially`.

2. **Using the deprecated `type()`.** Use `press_sequentially()`; `keyboard.type()` is a different, still-valid method on the keyboard object.

3. **Forgetting focus with `page.keyboard`.** `page.keyboard.press("Enter")` goes to whatever is focused, possibly nothing. Either use `locator.press()`, which focuses the element, or call `locator.focus()` / click first.

4. **Wrong key names.** `"enter"`, `"esc"`, `"Ctrl"` are errors; use `"Enter"`, `"Escape"`, `"Control"` (or `"ControlOrMeta"`).

5. **OS-specific shortcuts.** `Control+A` fails to select all on macOS. Use `ControlOrMeta`.

6. **Leaving a key held.** `keyboard.down("Shift")` without `up` affects all later actions. Prefer `click(modifiers=[...])` or wrap in `try/finally`.

7. **Hard-coded coordinates.** `page.mouse.click(500, 300)` breaks when the viewport size or layout changes. Derive coordinates from `bounding_box()` at the moment of use, and set a fixed viewport when coordinates matter (`page.set_viewport_size({"width": 1280, "height": 720})`).

8. **Not using `steps` when dragging.** Many libraries need multiple `mousemove` events; one jump will not start a drag.

9. **Hover that closes before the click.** If a menu closes when moving to the sub-item, there may be a real usability bug (a gap between the menu and the sub-menu), or your path crosses another element. Check by moving in steps.

10. **No assertion after the action.** Drag, hover and keyboard actions fail quietly. Always assert something observable.

11. **Using `time.sleep` for animations.** `expect` retries; actionability checks wait for stable elements.

12. **Using `force=True` to push through an overlay.** If something covers a button, a real user cannot click it either. Investigate before forcing.

**Best practices:** prefer locator methods; reach for `page.keyboard`/`page.mouse` only when needed; use `ControlOrMeta`; compute coordinates from `bounding_box()`; assert before *and* after; keep drag helpers in small functions.

---

## Mini Practice Exercises

**Exercise 1 (keys).** On `/key_presses`, write a parametrised test that presses `Enter`, `Tab`, `Escape`, `Space` and `ArrowDown`, and asserts the text. *Hint:* the result text names keys in upper case: `ENTER`, `TAB`, `ESCAPE`, `SPACE`, `DOWN`. Run it and adjust the expectations to what the page reports.

**Exercise 2 (typing styles).** Using Example 2's page, write one test that proves `press_sequentially` appends while `fill` replaces.

*Solution:*

```python
def test_fill_replaces_and_type_appends(page):
    page.set_content('<input aria-label="X">')
    x = page.get_by_label("X")
    x.fill("abc")
    x.press_sequentially("def")
    expect(x).to_have_value("abcdef")
    x.fill("z")
    expect(x).to_have_value("z")
```

**Exercise 3 (hover).** On `/hovers`, add a check that clicking the "View profile" link on user 2 navigates to `/users/2`. *Hint:* hover the second figure first, then `figure.get_by_role("link", name="View profile").click()`, then `expect(page).to_have_url(re.compile(r"/users/2$"))`.

**Exercise 4 (keyboard-only).** Extend Example 4 so that it also tests that pressing `Shift+Tab` from the Subscribe checkbox returns focus to Email.

**Exercise 5 (double-click edit).** Build a page with a `<span>` that becomes an `<input>` on double-click, saves on Enter and cancels on Escape. Write two tests, one for each outcome.

*Hint:* after `dblclick()`, use `expect(input).to_be_focused()` before typing; after Enter assert the span's text; after Escape assert it did not change.

**Exercise 6 (drag).** On `/drag_and_drop`, write a test that drags A onto B twice, and asserts that after the second drag the headers are back to "A" and "B".

**Exercise 7 (challenge: sortable list).** Create a page with three `<li draggable="true">` items and the minimal JavaScript for HTML5 reordering (search MDN's "HTML Drag and Drop API" for the example), then write a test that drags the last item above the first with `drag_to(..., target_position={"x": 5, "y": 2})` and asserts the new order with `expect(page.locator("li")).to_have_text(["C", "A", "B"])`. If `drag_to` does not work for your implementation, implement the manual `mouse` sequence.

---

## Summary / Key Takeaways

- Use **locator actions** (`click`, `fill`, `press`, `hover`, `dblclick`, `drag_to`) by default: they wait, scroll and check actionability. Use `page.keyboard` and `page.mouse` for global shortcuts, canvases, sliders and custom drags.
- `fill` replaces text in one event; `press_sequentially` types key by key (use it for typeahead and masks); `keyboard.type` types into the focused element; `insert_text` pastes.
- `press()` accepts key names (`Enter`, `Tab`, `Escape`, `ArrowDown`) and combos (`ControlOrMeta+A`, `Shift+Tab`). Use `down()`/`up()` to hold keys.
- Mouse variants: `dblclick()`, `click(button="right")`, `click(modifiers=[...])`, `click(position=...)`, `hover()`, `mouse.wheel()`.
- `drag_to()` handles most drags; for sliders and custom widgets use `hover`, `mouse.down`, `mouse.move(..., steps=N)`, `mouse.up`, with coordinates from `bounding_box()`.
- Assert before and after: `to_be_focused`, `to_be_visible`, `to_have_text`, `to_have_value`, and so on.
- Keyboard-only tests double as accessibility checks.

---

## External Resources

- Playwright for Python, Actions (keys, mouse click, drag and drop): https://playwright.dev/python/docs/input
- Playwright for Python API reference, `Keyboard`: https://playwright.dev/python/docs/api/class-keyboard
- Playwright for Python API reference, `Mouse`: https://playwright.dev/python/docs/api/class-mouse
