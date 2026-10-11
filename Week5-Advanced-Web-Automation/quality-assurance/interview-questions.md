# Interview Questions: Week 5 - Advanced Web Automation

Self-quiz bank: 100 questions, 20 per day, roughly 70% beginner, 25% intermediate and 5% advanced. Cover the answer, say yours out loud, then reveal it and check the **Keywords**.

---

## Day 1 (Monday): Playwright Web Interactions

### Beginner (Foundational)

#### Q1: [Dialogs] What are `alert`, `confirm` and `prompt`, and what happens to the page while one of them is open?
**Keywords:** native browser dialog, modal, blocking, OK/Cancel, not in the DOM
**Hint:** Think about who draws the box: the page's HTML or the browser?
<details>
<summary>Click to Reveal Answer</summary>

They are the three JavaScript dialogs. A page opens one by calling `alert()`, `confirm()` or `prompt()`, but the box is drawn by the browser itself, not by the page's HTML. That is why you can't inspect it in DevTools.

An `alert` shows a message and an OK button. A `confirm` has OK and Cancel and gives the page `true` or `false`. A `prompt` adds a text box and gives the page the typed text, or `null` on Cancel.

They are modal and blocking. The user can't touch the page behind them, and the page's JavaScript stops on the line that called the dialog until someone answers. For automation that means an unanswered dialog freezes the page, and any further action on it hangs until the timeout.

There is also a fourth type, `beforeunload`, the "Leave site?" warning. And an HTML pop-up built with a `<div role="dialog">` is not one of these. That is an ordinary DOM element that I'd handle with locators.
</details>

---

#### Q2: [Dialogs] What does Playwright do with a dialog if you haven't registered a handler, and how does that change once you register one?
**Keywords:** auto-dismiss, no listener, accept(), dismiss(), page.on("dialog"), hang
**Hint:** There are two rules, one for "no listener" and one for "at least one listener".
<details>
<summary>Click to Reveal Answer</summary>

With no `dialog` listener on the page, Playwright automatically dismisses every dialog so the test doesn't hang. That means pressing Cancel. A `confirm` returns `false` and a `prompt` returns `null`. So if I click "Delete" and never register a handler, the delete is cancelled for me, and my later assertion that the row is gone fails with a confusing message.

As soon as I register any listener with `page.on("dialog", ...)` or `page.once(...)`, that auto-dismiss stops. My handler is now responsible for calling `accept()` or `dismiss()` on every dialog. If it forgets, for example an `if` that only handles `confirm` and an `alert` shows up, the dialog stays open, the page is frozen, and the next action times out.

```python
page.once("dialog", lambda dialog: dialog.accept())   # register first
page.get_by_role("button", name="Delete").click()     # then trigger
```

The handler must be registered before the action that opens the dialog, because the dialog appears during the click.
</details>

---

#### Q3: [Dialogs] How do you answer a `prompt` dialog from Playwright, and what does the page receive for OK with text, OK with nothing, and Cancel?
**Keywords:** accept(text), dismiss(), default_value, null, empty string
**Hint:** Be careful with `accept()` when you pass no argument.
<details>
<summary>Click to Reveal Answer</summary>

I read what the page asked through the `Dialog` object. `dialog.type`, `dialog.message` and `dialog.default_value` are properties, while `accept()` and `dismiss()` are methods.

To type into the prompt I pass the text to `accept()`:

```python
page.once("dialog", lambda d: d.accept("Customer asked to cancel"))
```

The page then gets that string. If I call `dismiss()`, the page gets `null`. If I call `accept()` with no argument, the page gets an empty string. It does not get the prefilled default. I've verified this in Chromium: with `prompt("Name?", "Guest")`, a bare `accept()` produces `""`, even though `dialog.default_value` is `"Guest"`. If I want the default, I pass it explicitly: `dialog.accept(dialog.default_value)`.

A good test checks both Cancel and OK-with-empty-text, because well-written apps treat `null` and `""` differently.
</details>

---

#### Q4: [Radio/Checkbox] How do radio buttons and checkboxes differ in HTML and in user behaviour?
**Keywords:** type="checkbox", type="radio", name attribute, one per group, zero or many
**Hint:** What makes a set of radios a "group"?
<details>
<summary>Click to Reveal Answer</summary>

Both are `<input>` elements, told apart by `type`. A checkbox is an independent on/off choice, so a group of them allows zero, one or many to be checked, and clicking one doesn't affect the others.

A radio button is "pick one from a set". Radios that share the same `name` attribute form a group, and the browser guarantees at most one is selected. Selecting another one automatically deselects the previous one. A user can't uncheck a radio by clicking it, and a group starts with nothing selected unless an option has the `checked` attribute.

So in a test, a checkbox can be turned on or off with `check()` and `uncheck()`. A radio can only be turned on, and you "unselect" it by selecting a different one. If two radios in the same visual group can both be selected, I suspect someone used different `name` values by mistake.
</details>

---

#### Q5: [Radio/Checkbox] Why should you use `check()` / `uncheck()` / `set_checked()` instead of `click()` to set a checkbox?
**Keywords:** idempotent, state not action, toggles, verifies state, set_checked
**Hint:** What happens if the box is already ticked when you `click()` it?
<details>
<summary>Click to Reveal Answer</summary>

`click()` toggles. If the box was already ticked, because the site pre-selects it or an earlier step ticked it, my click unticks it, which is the opposite of what I wanted. The result depends on a hidden starting state.

`check()` means "make sure this is checked". It is idempotent: if the box is already checked it does nothing, otherwise it clicks it. After clicking it also verifies the state really changed, and raises an error if it didn't. For example, I saw "Clicking the checkbox did not change its state" on a box whose click handler returned false.

`set_checked(True/False)` is the same idea driven by a variable, which is handy in data-driven tests:

```python
page.get_by_label("Subscribe").set_checked(user["subscribe"])
```

`uncheck()` on a radio button raises an error, "Radio buttons can only be unchecked by selecting another radio button", because a user couldn't do it either. I still use `click()` when the click itself is what I'm testing, such as "click once checks, click twice unchecks".
</details>

---

#### Q6: [Radio/Checkbox] How do you assert checkbox state, and why is `expect(...).to_be_checked()` better than `assert box.is_checked()`?
**Keywords:** to_be_checked, auto-retry, is_checked, no waiting, get_by_label
**Hint:** One of them retries and one doesn't.
<details>
<summary>Click to Reveal Answer</summary>

`expect(box).to_be_checked()` is a web-first assertion. It retries until the box is checked or the timeout expires, so if the app updates the state a moment later, for example after a network call, the test still passes without a sleep. `not_to_be_checked()` and `to_be_checked(checked=False)` cover the opposite.

`is_checked()` returns a Python boolean for the state right now, with no waiting. `assert box.is_checked()` can fail randomly if the page is slightly slow. I keep `is_checked()` for control flow like `if box.is_checked():`.

To find the box I prefer `get_by_label("Email updates")` or `get_by_role("checkbox", name="Email updates")`. Label matching is a case-insensitive substring match, so "Box" would match "Box1" and "Box2" and strict mode raises an error. Then I'd use `exact=True`, a role, or scope within a fieldset.

I also assert the initial state, such as "marketing consent is unchecked by default", and the final state.
</details>

---

#### Q7: [Dropdowns] What is the difference between a native `<select>` and a custom dropdown, and how do you automate each?
**Keywords:** select_option, role="option", open then click, not a `<select>` element, combobox
**Hint:** What error do you get if you call `select_option` on a `<div>`?
<details>
<summary>Click to Reveal Answer</summary>

A native dropdown is a real `<select>` with `<option>` children. Playwright has a special method for it, `select_option()`, which sets the selection and fires the `input` and `change` events.

A custom dropdown from React-Select, Material UI and similar libraries is built from `<div>`s, `<button>`s and `<li>`s. Calling `select_option` on it fails with "Element is not a `<select>` element". For those I do what a user does: open it, then click the option.

```python
page.get_by_role("combobox", name="Country").click()
page.get_by_role("option", name="Canada").click()
expect(page.get_by_role("combobox", name="Country")).to_have_text("Canada")
```

The first step is always to inspect the HTML to see which kind I have. For custom ones, the option list is often rendered in a portal at the end of `<body>`, so I search from `page` rather than from the trigger's container. I also don't `click()` an `<option>` inside a native select. It times out, so native lists should always go through `select_option`.
</details>

---

#### Q8: [Dropdowns] How can `select_option()` match an option, and what does it return?
**Keywords:** value, label, index, returns values, change event
**Hint:** Think of the three keyword arguments, and what a bare string does.
<details>
<summary>Click to Reveal Answer</summary>

There are three explicit forms:

```python
select.select_option(value="us")             # the value attribute
select.select_option(label="United States")  # the visible text
select.select_option(index=1)                # zero-based position
```

A plain string such as `select_option("us")` tries the value first and then the label, so it works, but it hides what I meant. I prefer the keyword forms. `label=` must be the full visible text, and a partial label like `"Canad"` doesn't match. An option with no `value` attribute uses its text as its value. `index=` is the most fragile, since adding a placeholder shifts everything.

It returns a list of the values that are now selected, for example `["ca"]`, and it dispatches the real `input` and `change` events. It also waits for the select to be enabled and for the option to exist, so selecting a disabled or missing option times out rather than failing instantly.

To verify, I use `expect(select).to_have_value("ca")`, or `expect(page.locator("#country option:checked")).to_have_text("Canada")` for the visible text.
</details>

---

#### Q9: [Dropdowns] How do you work with a `<select multiple>`: selecting, clearing, adding to a selection, and asserting?
**Keywords:** list of values, replaces selection, select_option([]), to_have_values, document order
**Hint:** Does `select_option` add to the existing selection or replace it?
<details>
<summary>Click to Reveal Answer</summary>

For a multi-select I pass a list:

```python
skills.select_option(["py", "sql"])
skills.select_option(label=["Git", "CI/CD"])
```

No Ctrl key is needed. `select_option` replaces the selection, so after the second call only Git and CI/CD are selected. `select_option([])` clears everything. If I need to add to the current selection, I first read it, for example with `evaluate("el => [...el.selectedOptions].map(o => o.value)")`, then pass the union.

To assert, I use `to_have_values`. It compares against the selected options in document order, not the order I selected them in. In my run, selecting `["git", "py"]` where Python comes first in the HTML gave `["py", "git"]`, and `to_have_values(["git", "py"])` failed. So I list expected values in document order.

On a single `<select>`, passing several values doesn't select them all. Only one option ends up selected, and in my check it was the first matching option in document order.
</details>

---

#### Q10: [Keyboard/Mouse] What is the difference between locator actions and the `page.keyboard` / `page.mouse` APIs, and when would you use each?
**Keywords:** actionability checks, auto-wait, current focus, coordinates, canvas
**Hint:** One layer knows about elements and one doesn't.
<details>
<summary>Click to Reveal Answer</summary>

Locator actions such as `click()`, `fill()`, `press()`, `hover()`, `dblclick()` and `drag_to()` are the high-level layer. Before acting they run actionability checks: the element must be attached, visible, stable, enabled and not covered. They scroll it into view and retry until the timeout. I use them by default.

`page.keyboard` and `page.mouse` are the low-level device APIs. They have no element awareness and no waiting. `page.keyboard.press("Enter")` goes to whatever currently has focus, and `page.mouse.click(120, 340)` clicks that pixel regardless of what is there.

I use them for things that don't belong to one element: global shortcuts, canvases, sliders, custom drags and raw event sequences. The risks are that focus might not be where I think, and hard-coded coordinates break when the viewport or layout changes. So I take coordinates from `locator.bounding_box()` at the moment of use, and I use `locator.focus()` before keyboard calls.
</details>

---

#### Q11: [Keyboard/Mouse] How do you press special keys and shortcuts in Playwright, and what are common key-name mistakes?
**Keywords:** press, Enter, ControlOrMeta, Shift+Tab, key names are case-sensitive, down/up
**Hint:** `"enter"`, `"esc"` and `"Ctrl"` all fail.
<details>
<summary>Click to Reveal Answer</summary>

I use `press()` on a locator, which focuses the element first, or on `page.keyboard`, which uses the current focus:

```python
page.get_by_role("textbox", name="Search").press("Enter")
page.keyboard.press("Escape")
page.keyboard.press("Shift+Tab")
page.keyboard.press("ControlOrMeta+A")   # select all on any OS
```

Key names follow DOM key names and are case-sensitive: `Enter`, `Tab`, `Escape`, `Backspace`, `ArrowDown`, `Space`. I tried `"enter"`, `"esc"` and `"Ctrl"` and each raised "Unknown key". `Control+A` doesn't select all on macOS, so I use `ControlOrMeta`.

For a capital letter I press `"A"`. `"Shift+a"` still types a lowercase `a`, so it isn't a reliable way to get uppercase.

`press` is `down` followed by `up`. If I need to hold a key while doing something else, I use `keyboard.down("Shift")` and `keyboard.up("Shift")`, but the key stays held until released even if the test fails, so I'd rather use `click(modifiers=["Shift"])` or a `try/finally`.
</details>

---

#### Q12: [Keyboard/Mouse] How do you perform hover, double-click, right-click, modifier-click and drag-and-drop in Playwright?
**Keywords:** hover, dblclick, click(button="right"), modifiers, drag_to
**Hint:** Most of these are options of `click()` or dedicated locator methods.
<details>
<summary>Click to Reveal Answer</summary>

```python
locator.hover()                              # reveal menus, tooltips, captions
locator.dblclick()                           # e.g. edit a cell
locator.click(button="right")                # contextmenu event
locator.click(modifiers=["Shift", "Control"])# click with keys held
source.drag_to(target)                       # drag and drop
page.mouse.wheel(0, 500)                     # scroll down 500px
```

For hover I assert what it reveals, and ideally the hidden state before it: `expect(caption).to_be_hidden()`, then `hover()`, then `expect(caption).to_be_visible()`. Right-click only triggers the `contextmenu` event. A custom HTML context menu appears as normal elements I can click, but the browser's own native menu isn't something I can control.

`drag_to` hovers the source, presses, moves and releases. It worked for HTML5 `draggable` drag-and-drop in my check. Drag and hover fail quietly, so I always assert the outcome, such as the order of items or the column a card ended up in.
</details>

---

#### Q13: [Auto-suggestions] Why does `fill()` often fail on an auto-suggest field, and what should you use instead?
**Keywords:** press_sequentially, keyup, key events, input event, delay, clear
**Hint:** Compare the events fired by `fill` and by typing.
<details>
<summary>Click to Reveal Answer</summary>

`fill()` sets the whole value in one step and fires a single `input` event. It doesn't fire `keydown` or `keyup` per character. If the widget listens to `keyup` or `keydown`, which is common in older and jQuery-style widgets, `fill` produces no suggestions at all, and the test waits for a list that never comes. I confirmed this: after `fill("Py")` a `keyup`-driven list stayed hidden, while `press_sequentially` worked. A widget that listens to `input` may be fine with `fill`.

So the safe default is `press_sequentially`, which types one character at a time with the full key event sequence, like a user:

```python
box.press_sequentially("Py", delay=80)
```

`delay` is the pause between keystrokes in milliseconds. It mimics human speed and helps debounced widgets, but it isn't a wait for the list. `press_sequentially` appends at the caret and doesn't clear the field, so I call `box.clear()` first if there might be old text. `type()` is the old, deprecated name.
</details>

---

#### Q14: [Auto-suggestions] How do you wait for suggestions to appear and then select one reliably?
**Keywords:** expect to_have_text, wait for content not time, exact=True, get_by_role("option"), no sleep
**Hint:** Which is better to wait on: seconds, visibility, or content?
<details>
<summary>Click to Reveal Answer</summary>

I wait for the condition I care about, never for a number of seconds. `expect` assertions retry (5 seconds by default), so one line covers debounce, network and rendering:

```python
options = page.get_by_role("option")
expect(options).to_have_text(["Python", "PyPy"])   # exact list, in order
page.get_by_role("option", name="Python", exact=True).click()
expect(box).to_have_value("Python")
```

Waiting only for the list to be visible is risky, because it might still be the list from the previous keystroke. Waiting for exact content proves the list belongs to my input. When I don't know the full list, I wait for `expect(options.first).to_contain_text("Pyth")` and then click the specific option.

I select by text with `exact=True`, because `name="Java"` also matches "JavaScript", not by index, since ranking can change. I use locators, not stored element handles, because the list is often rebuilt on every lookup. `time.sleep()` makes tests either flaky or slow.
</details>

---

### Intermediate (Application)

#### Q15: [Dialogs] Your test clicks "Delete" and asserts the row disappears, but it fails. After you add a handler that only calls `accept()` for `confirm` dialogs, a different test hangs. Explain both problems and give the fix.
**Keywords:** auto-dismiss, no listener, handler must answer every dialog, page.once, test cancel path
**Hint:** Think about the two rules for "no listener" and "some listener".
<details>
<summary>Click to Reveal Answer</summary>

The first failure is because there was no `dialog` listener, so Playwright auto-dismissed the `confirm`, which means it pressed Cancel. The delete never ran, and my assertion failed with a message that didn't mention the dialog. When a flow has a confirm, I have to choose the answer explicitly.

The hang is the other rule. Once any listener exists, Playwright stops auto-dismissing and my handler must answer every dialog. My handler only answered `confirm`. When an `alert` appeared nobody answered it, the page froze, and the next action timed out. The fix is to make every path answer:

```python
def handler(dialog):
    seen.append((dialog.type, dialog.message))   # record first
    dialog.accept() if accept else dialog.dismiss()

page.once("dialog", handler)                      # before the click
page.get_by_role("button", name="Delete").click()
expect(page.get_by_role("row", name="Customer 8841")).to_have_count(0)
assert seen == [("confirm", "Delete customer 8841?")]
```

I'd use `once` so the handler can't leak into later steps, and after it fires the default auto-dismiss returns. I record, answer, then assert, because a failed assertion before `accept()` would also leave the dialog open. I'd also write a second test that dismisses and asserts the row is still there, since that catches the "deletes regardless of the answer" regression.
</details>

---

#### Q16: [Radio/Checkbox] A design system hides the real checkbox input, and `check()` times out. How do you approach it, and does `force=True` fix it?
**Keywords:** actionability, click the label, ARIA role, force=True limits, assert underlying input, no JavaScript .checked
**Hint:** There is a ladder of options, and `force` is last.
<details>
<summary>Click to Reveal Answer</summary>

`check()` waits for the input to be visible and able to receive pointer events. If the design system makes it `opacity:0` with zero size, or `display:none`, the actionability checks never pass and it times out, saying the element isn't visible.

My order of options:

1. Click the visible label, which is what a user does: `page.get_by_text("Remember me").click()`. Then I assert on the real input with `expect(remember).to_be_checked()`. I lose idempotence with `click()`, so I assert the starting state first.
2. If the control is `role="checkbox"` or `role="switch"`, I use `get_by_role` plus `check()`, which worked for ARIA roles in my run. Otherwise I click and assert `aria-checked`.
3. `force=True` only as a documented last resort. It skips actionability checks, but it doesn't rescue every hidden input. On a zero-size hidden checkbox, `check(force=True)` raised "Element is outside of the viewport". On a `display:none` radio it raised "Element is not visible". So it often doesn't help for the truly hidden case, and it can mask a real bug such as an overlay covering the control.

I avoid setting `.checked = true` through `evaluate`. That skips the `change` event, so the app never learns about it. I check the visible effect and the underlying value.
</details>

---

#### Q17: [Dropdowns] A "State" dropdown is repopulated from an API after you pick a "Country". How do you automate it without flakiness, and how would you verify the list?
**Keywords:** dependent dropdown, wait for condition, to_have_text list, no time.sleep, select_option waits
**Hint:** What does the second list contain right after the first change?
<details>
<summary>Click to Reveal Answer</summary>

After the country changes, the state list is briefly empty or shows "Loading...". If I select from it immediately I may hit the wrong list, and `time.sleep(2)` is slow when the server is fast and flaky when it's slow. I wait on the condition instead:

```python
page.locator("#country").select_option(label="Canada")
expect(page.locator("#state option")).to_have_text(
    ["Choose", "Ontario", "Quebec", "Alberta"])      # retries until the real list arrives
page.locator("#state").select_option(label="Ontario")
expect(page.locator("#state")).to_have_value("Ontario")
```

`to_have_text` with a list compares the whole ordered list of options, so it waits for the right data and also verifies content, count and order in one line. `select_option` itself also waits for the option to exist, so calling it directly would often work, but the explicit wait documents the dependency and gives a clearer failure.

I'd parametrise over countries with a dictionary of expected states and add the placeholder state. For a custom component, the same idea applies with `get_by_role("option")`. For clearing or adding to a multi-select I'd use `select_option([])` and the union of the current selection.
</details>

---

#### Q18: [Keyboard/Mouse] A custom slider doesn't respond to `drag_to()`. How do you automate it with the low-level mouse, and how do you verify it worked?
**Keywords:** bounding_box, mouse.move, mouse.down, steps, mouse.up, assert result
**Hint:** Think about which events a drag library needs to see.
<details>
<summary>Click to Reveal Answer</summary>

I fall back to the manual sequence with `page.mouse`, using coordinates from `bounding_box()` computed right before use:

```python
handle = page.locator("#handle").bounding_box()
track = page.locator("#track").bounding_box()
assert handle is not None and track is not None

sx = handle["x"] + handle["width"] / 2
sy = handle["y"] + handle["height"] / 2
ex = track["x"] + track["width"] / 2

page.mouse.move(sx, sy)
page.mouse.down()
page.mouse.move(ex, sy, steps=20)   # many small mousemove events
page.mouse.up()

expect(page.locator("#pct")).to_have_text("50")
```

`bounding_box()` returns `None` for a non-visible element, so I guard for it. The numbers are relative to the viewport, so I compute them immediately before use and may fix the viewport size. `steps=20` generates intermediate `mousemove` events. Many drag libraries need several of them before they recognise a drag, so I use steps by default. In my check this simple slider also worked with a single jump, but I wouldn't rely on that with a real library.

Drag actions fail silently, so the `expect` on the observable result, here the percentage, is what makes it a test.
</details>

---

#### Q19: [Auto-suggestions] Design the key tests for a search box with suggestions. How do you test keyboard selection and a "minimum 2 characters" rule?
**Keywords:** ArrowDown, Enter, get_by_role("option", selected=True), minimum characters, no results, Escape
**Hint:** Don't stop at "type, click, done".
<details>
<summary>Click to Reveal Answer</summary>

I'd cover the happy path with the mouse and a separate keyboard path, because keyboard-only users depend on it, plus the negative paths.

Keyboard path, asserting at each step:

```python
box.press_sequentially("Ja", delay=80)
expect(page.get_by_role("option")).to_have_text(["Java", "JavaScript"])
box.press("ArrowDown")
expect(page.get_by_role("option", selected=True)).to_have_text("Java")
box.press("ArrowDown")
box.press("Enter")
expect(box).to_have_value("JavaScript")
```

For a well-built ARIA widget the highlighted option has `aria-selected="true"`, so `selected=True` finds it. Otherwise I assert whatever class it uses.

For the minimum-characters rule I type one character and assert the listbox is hidden, then type the second and assert it becomes visible. The caveat is that `to_be_hidden()` passes immediately when the list is hidden from the start, so on its own it doesn't prove the widget refused to open. The second half, visible after two characters, is the stronger evidence.

Other tests are no results (`to_contain_text("No results")` with `to_have_count(0)` for options), case-insensitivity via parametrisation, Escape closes the list but keeps the text, clearing the text closes the list, and special characters such as `O'Brien`.
</details>

---

### Advanced (Deep Dive)

#### Q20: [Auto-suggestions] Walk through what happens between a keystroke and a rendered suggestion list, and explain how that causes stale-list flakiness and how your test design prevents it.
**Keywords:** debounce, key events, list rebuilt, stale option, locator re-resolves, wait for exact content
**Hint:** Count the asynchronous steps between the key press and the options in the DOM.
<details>
<summary>Click to Reveal Answer</summary>

Each key press fires `keydown`, `input` and `keyup` on the field. The widget listens to one of those. It usually debounces, waiting a few hundred milliseconds after the last key and restarting the timer on each new key. Then it filters local data or sends a request to the server, which takes unpredictable time. Finally it re-renders the list, often by removing the old `<li>` elements and inserting new ones, and makes it visible. The user then selects by click or by ArrowDown and Enter.

The flakiness comes from the gaps. While typing "Pyth", the list may show results for "P", "Py" and "Pyt" before "Pyth". If my test clicks as soon as a list is visible, I might click an option from an intermediate list. The element I targeted may be detached a moment later, or the same text exists in both lists, so the test passes by luck. And with a server-driven widget a slow response for an older term can arrive after a newer one, which is a real race-condition bug in the app.

My design counters this in layers:

- Type with `press_sequentially` so the widget actually sees key events.
- Wait on content, not time or visibility: `expect(options).to_have_text([...])`, or `to_contain_text` for my full term. That proves the list matches my input.
- Click through a locator such as `get_by_role("option", name="Python", exact=True)`. A locator re-resolves at action time, whereas a stored `ElementHandle` goes stale when the list is rebuilt.
- Assert the outcome, the field value and the list closing.

To test the race in the app itself, I'd make one term slow, type it then change the term, and assert the final list matches only the last input. For that I'd use a bounded `expect` with a longer timeout rather than a fixed sleep.
</details>

---


## Day 2 (Tuesday): Playwright Advanced Interactions

### Beginner (Foundational)

#### Q21: What is an iframe, and why can't a normal `page.get_by_role(...)` locator find a button that is clearly visible inside one? [Frames]
**Keywords:** separate document, main frame, frame_locator, timeout
**Hint:** Think about which document a page-level locator searches.
<details>
<summary>Click to Reveal Answer</summary>

An iframe embeds a completely separate HTML document inside the current page. It has its own DOM, its own `window`, its own CSS and its own URL. In Playwright terms the page has one main frame plus zero or more child frames.

A locator created on `page` only searches the main frame. The iframe shows up there as one opaque element, and its contents are invisible to the query. So the button is on screen, but `page.get_by_role("button", name="Pay now").count()` returns 0, and an action on it just waits and then fails with a `TimeoutError` and a call log saying "waiting for get_by_role(...)".

When I see a timeout on an element I can plainly see, I check DevTools for a `#document` node under an `<iframe>`. If it is there, I go through the frame instead:

```python
card = page.frame_locator('iframe[title="Secure card payment"]')
card.get_by_role("button", name="Pay now").click()
```
</details>

---

#### Q22: How do you interact with elements inside a frame, and how do you reach a frame nested inside another frame? Why is `frame_locator()` preferred over `page.frame()`? [Frames]
**Keywords:** frame_locator, chaining, lazy, auto-wait, strict mode
<details>
<summary>Click to Reveal Answer</summary>

`page.frame_locator(selector)` returns a FrameLocator that points at the `<iframe>` element, and from it I use the normal locator methods: `get_by_label`, `get_by_role`, `locator` and so on.

For a nested frame I chain the calls. Read left to right it means "go into this iframe, then into the iframe inside it":

```python
deep = page.frame_locator("#outer-frame").frame_locator("#inner-frame")
deep.get_by_role("button", name="Deep button").click()
expect(deep.locator("#out")).to_have_text("clicked deep")
```

I prefer it over `page.frame()` for three reasons. It is lazy, so it re-resolves the iframe on every use and survives the frame reloading. It auto-waits for the iframe and for the element inside it. And it works with `expect`.

`page.frame(name="x")` is evaluated immediately and returns `None` if the frame is not attached yet. It also gives a `Frame` object that can go stale. I use it only when I really need a `Frame`, for example with old framesets, `frame.url`, or `child_frames`.

One more rule: `frame_locator()` is strict. If my selector matches two iframes, the action raises a strict mode violation, so I make the selector more specific using `title`, `data-testid`, `name`, or a stable `src*=` fragment. Also, there is no "switch back" step as in Selenium. I just use `page` for the main page and the FrameLocator for the iframe.
</details>

---

#### Q23: In a table of users, how do you click the Delete button for one specific user, and why is that better than `tr:nth-child(3) button`? [Web Tables]
**Keywords:** filter, has_text, scope to row, content over position
**Hint:** Find the row by what it contains, then search inside that row.
<details>
<summary>Click to Reveal Answer</summary>

I locate by content and relationship, not by position. I take all rows, filter down to the one containing the key, and then search for the button inside that row only:

```python
row = page.get_by_role("row").filter(has_text="Maria Lopez")
expect(row).to_have_count(1)        # guard: the key is unique
row.get_by_role("button", name="Delete").click()
expect(row).to_have_count(0)        # proves the row is gone
```

A positional selector like `tr:nth-child(3)` breaks as soon as the data is sorted, paginated, or a row is inserted. The filtered version survives all of that, and because the click is scoped to the row it cannot hit another user's Delete button.

Be careful with `has_text`: it is a case-insensitive substring match, so `has_text="Ann"` also matches "Joanna Green". When keys can overlap I use an exact cell match, `filter(has=page.get_by_role("cell", name="Ann Brown", exact=True))`, or an anchored regex such as `re.compile(r"^Ann\b")`. If a key is still not unique I chain two `filter()` calls on two columns.
</details>

---

#### Q24: A table loads its data from an API. Why does `locator.count()` or `all_inner_texts()` sometimes return 0 or an empty list, and how do you read the table reliably? [Web Tables]
**Keywords:** no auto-wait, snapshot, to_have_count, header row, thead
<details>
<summary>Click to Reveal Answer</summary>

`count()`, `all_inner_texts()`, `all_text_contents()` and `is_visible()` are instant snapshots. They do not wait. If I call them before the API response has rendered, I get `0` or `[]`.

The fix is to gate them with a web-first assertion that proves loading is finished, and only then read:

```python
rows = page.locator("#users tbody tr")
expect(rows).to_have_count(4)                  # retries until 4 rows exist
names = page.locator("#users tbody td:nth-child(1)").all_inner_texts()
```

`to_have_text` also accepts a list, so I can assert the whole column in order in one step: `expect(col).to_have_text(["Maria Lopez", "John Smith"])`. It fails if the length or any text differs, and it retries.

Other things I watch for. `get_by_role("row")` includes the header row, so I use `tbody tr` or subtract one deliberately. `td:nth-child(1)` in CSS is 1-based while Playwright's `.nth(0)` is 0-based. To find a column without hard-coding its position, I read `thead th` texts and use `headers.index("Status")`. If I use `get_by_role("columnheader")`, I remember that a bare `<th>` was not exposed as a column header in my testing, only one with `scope="col"`, so I check the Accessibility tab when role locators return nothing.
</details>

---

#### Q25: How do you set a value in an `<input type="date">`, and why do you not click the browser's calendar popup? [Date Pickers]
**Keywords:** fill, YYYY-MM-DD, value vs display, Malformed value
<details>
<summary>Click to Reveal Answer</summary>

For native date inputs I use `fill()` with the ISO value:

```python
dob = page.get_by_label("Date of birth")
dob.fill("1995-07-21")
expect(dob).to_have_value("1995-07-21")
```

The popup calendar is drawn by the browser, not by the page, so it is not in the DOM and Playwright cannot click it like a normal element. `fill()` sets the value directly and fires the `input` and `change` events, so the app reacts as normal.

The value is always `YYYY-MM-DD` even though the browser displays it by locale, for example `mm/dd/yyyy` for en-US or `dd/mm/yyyy` for en-GB. Playwright works with the value. If I pass the wrong format, `fill("03/14/2025")`, or an impossible date, `fill("2025-02-30")`, it raises an error with "Malformed value". Other types follow the same idea: `datetime-local` takes `2025-03-14T14:30`, `time` takes `14:30`, `month` takes `2025-03`.

One more detail: `min` and `max` are not enforced by `fill()`. It will set an out-of-range value, which is actually handy for negative tests, because the browser's validation then flags it on submit.
</details>

---

#### Q26: How would you select a date in a custom (JavaScript) calendar widget, and what mistakes do you avoid when clicking the day? [Date Pickers]
**Keywords:** scope to calendar, navigate months, exact match, aria-label, overflow days
<details>
<summary>Click to Reveal Answer</summary>

I act like a human, in steps. Click the field to open the calendar. Scope to the calendar by role and name, for example `page.get_by_role("dialog", name="Choose date")`, because many widgets append it at the end of `<body>`. Read the header month, work out how many months away the target is, click Next or Previous that many times, click the day, then assert the field's value.

```python
shown = datetime.strptime(calendar.locator("#title").inner_text(), "%B %Y")
diff = (target.year - shown.year) * 12 + (target.month - shown.month)
name = "Next month" if diff > 0 else "Previous month"
for _ in range(abs(diff)):
    calendar.get_by_role("button", name=name).click()
label = f"{target.strftime('%B')} {target.day}, {target.year}"
calendar.get_by_role("button", name=label, exact=True).click()
```

Mistakes to avoid on the day click:
- Matching by number without `exact=True`. Name matching is a substring match, so `name="1"` matches 1, 10 to 19, 21 and 31. I use `exact=True`, a regex like `^1$`, or a full-date `aria-label`.
- Clicking overflow days from the neighbouring months. I exclude them with a class such as `:not(.outside)` or use the full-date label.
- Not waiting after each navigation click on animated widgets. I assert the title text changes.

If the input is `readonly`, `fill()` just keeps waiting for it to be editable and times out, which tells me the app wants the widget path. If the field is typeable, I prefer `fill()` but still keep one test that uses the widget, because the click path is separate code.
</details>

---

#### Q27: In Playwright, what is the relationship between Browser, BrowserContext and Page, and why is there no "switch to window" command? [Tabs and Windows]
**Keywords:** BrowserContext, Page, isolation, shared cookies, no current window
<details>
<summary>Click to Reveal Answer</summary>

A Browser is the browser process. A BrowserContext is like a fresh incognito profile with its own cookies, storage, cache and permissions. A Page is a single tab or pop-up window. In Playwright a "tab" and a "window" are both just a `Page`.

All pages in the same context share cookies and storage, like real tabs in one profile. Pages in different contexts share nothing. `browser.new_page()` quietly creates a new context with one page. If I want to inspect `context.pages` or attach routes to the whole session, I create the context myself.

There is no switch command because there is no "current window" pointer. Each `Page` object is an independent handle, so if I hold `page` and `popup` I can use either at any time. It is like two remote controls for two TVs rather than one remote I have to re-point. That removes the classic Selenium bug of forgetting to switch back.
</details>

---

#### Q28: A click opens a link in a new tab. How do you capture and use the new tab, and why must the click be inside a `with` block? [Tabs and Windows]
**Keywords:** expect_popup, register first, popup_info.value, same-tab link
<details>
<summary>Click to Reveal Answer</summary>

I use the register-first-then-act pattern:

```python
with page.expect_popup() as popup_info:
    page.get_by_role("link", name="Terms").click()
terms = popup_info.value          # .value is a property, not a method
expect(terms).to_have_title("Terms of Service")
expect(terms.get_by_role("heading", name="Terms of Service")).to_be_visible()
terms.close()
```

The listener starts when the `with` block starts, the click happens inside it, and when the block ends Playwright waits for the event if it has not arrived. If I clicked first and asked for the popup afterwards, the event could fire before I was listening and I would miss it.

A new tab can still be loading, so I confirm I have the right one with a title, URL or heading assertion, which also acts as a wait. After `terms.close()` the original `page` still works because it was never invalidated.

Only use `expect_popup` when the link really opens a new page, with `target="_blank"` or `window.open`. For a normal same-tab link there is no popup, so it fails with a `TimeoutError` waiting for event "popup", and I should use `page.wait_for_url(...)` or `expect(page).to_have_url(...)`. `context.expect_page()` is the wider alternative that catches any new page in the context.
</details>

---

#### Q29: What is Shadow DOM, how is it different from an iframe, and how does Playwright deal with it? [Shadow DOM]
**Keywords:** shadow host, shadow root, open, pierce, same document
<details>
<summary>Click to Reveal Answer</summary>

Shadow DOM is a boundary inside the same document that hides a web component's internal tree and styles. A custom element such as `<user-card>` is the shadow host, `attachShadow({mode: 'open'})` creates the shadow root, and the elements inside it are the shadow tree. In DevTools I see `#shadow-root (open)`.

It differs from an iframe because it is the same document and the same `window`. An iframe is a separate document and needs `frame_locator`. Shadow DOM needs no special handling in Playwright for open roots.

Playwright's CSS, text and role-based locators pierce open shadow roots automatically, so I write the same code as if there were no boundary:

```python
page.get_by_role("button", name="Follow").click()
page.locator("user-card button.follow").click()
```

Piercing is recursive, so nested components work too. Where several components repeat, I scope by the host to avoid strict mode violations:

```python
maria = page.locator("user-card").filter(has_text="Maria Lopez")
maria.get_by_role("button", name="Follow").click()
```

In my test, the unscoped `get_by_role("button", name="Follow")` matched two buttons and an action on it raised a strict mode violation, while the scoped one clicked only Maria's card.
</details>

---

#### Q30: What does NOT pierce shadow DOM in Playwright, and what can you do when an element lives in a closed shadow root? [Shadow DOM]
**Keywords:** XPath, querySelector, css:light, closed root, attachShadow
**Hint:** Think about which selector engines and which raw JavaScript calls stop at the boundary.
<details>
<summary>Click to Reveal Answer</summary>

Four things do not pierce:
1. XPath. `page.locator("xpath=//button").count()` returned 0 for a button inside an open shadow root while `css=button` found it.
2. Raw `document.querySelector` inside `page.evaluate`. It returns `None` because the browser's own query stops at the boundary. I must walk `el.shadowRoot.querySelector(...)` myself.
3. `css:light=`, which deliberately opts out of piercing. It is rarely needed.
4. Closed shadow roots. `host.shadowRoot` is `null` and locators find nothing, even though the user sees the button.

For a closed root I take the least hacky route first:
- Ask developers for a stable test interface, such as a `data-testid` or ARIA attributes on the host, or an open mode in test builds.
- Test through the host's public behaviour.
- As a last resort, add an init script that patches `Element.prototype.attachShadow` so every root is created open. It must run before the page's scripts:

```python
context.add_init_script("""
  const orig = Element.prototype.attachShadow;
  Element.prototype.attachShadow = function (init) {
    return orig.call(this, { ...init, mode: 'open' });
  };
""")
```

With that patch the hidden "Reveal" button went from 0 matches to 1 in my run. It is a test-only hack, since it changes production behaviour. I would not use `evaluate` for clicking either, because it skips actionability checks.
</details>

---

#### Q31: What is auto-waiting in Playwright, and which checks does it run before a click? Why should you not add a wait before an action? [Dynamic Elements]
**Keywords:** actionability, attached, visible, stable, receives events, enabled
<details>
<summary>Click to Reveal Answer</summary>

Before an action such as `click()`, `fill()` or `check()`, Playwright waits until the element is actionable. For a click the checks are: attached to the DOM, visible, stable (same position for two animation frames, so not mid-animation), receives events (nothing covers it at the click point), and enabled. `fill()` also needs the element to be editable, so not `readonly`.

If the checks do not pass within the timeout, 30 seconds by default for actions, I get a `TimeoutError` with a call log saying why, for example "element is not enabled - waiting" or that another element intercepts pointer events. Reading that log tells me exactly which check is failing.

So I do not write `wait_for_selector` or `time.sleep` before an action:

```python
page.get_by_role("button", name="Continue").click()   # waits until the button becomes enabled
```

In my run, a button that became enabled after one second was simply clicked once it was ready, with no extra code. A fixed sleep is the wrong tool because it is too slow when the app is fast and still fails when the app is slower than the sleep.
</details>

---

#### Q32: What are web-first assertions, and why is `expect(locator)` better than reading a value with `inner_text()` and asserting in plain Python? [Dynamic Elements]
**Keywords:** expect, retry, 5 second timeout, snapshot, stale element
<details>
<summary>Click to Reveal Answer</summary>

`expect(locator).to_...()` assertions retry until the condition is true or the assertion timeout expires, 5 seconds by default. `assert locator.inner_text() == "Saved"` reads once, right now. If the toast has not appeared yet I get a timeout or a stale value.

```python
expect(page.get_by_role("alert")).to_have_text("Saved successfully")      # retries
assert page.get_by_role("alert").inner_text() == "Saved successfully"     # one-shot read
```

The same trap applies to `is_visible()`, `count()`, `all_inner_texts()` and `is_checked()`. They are instant. In my test, `is_visible()` on an element that appeared 500 ms later returned `False` immediately, while `expect(...).to_be_visible()` waited and passed. For disappearing things I use `to_be_hidden()`, and I can set a per-assertion timeout, e.g. `timeout=10_000`, for legitimately slow cases.

It also relates to stale elements. A Locator is a recipe that is re-run on every use, so after a framework re-renders the list, the same locator just finds the new node. An `ElementHandle` from `query_selector` is a real reference: after a re-render its `inner_text()` returned the old text, `is_visible()` was `False`, and `click()` failed with "Element is not attached to the DOM". That is why handles are discouraged.
</details>

---

#### Q33: What does `page.goto()` return, does it raise on a 404, and which `wait_until` values exist? [Navigation Events]
**Keywords:** Response, status, ok, wait_until, networkidle
<details>
<summary>Click to Reveal Answer</summary>

`goto` navigates and waits for a lifecycle stage, `load` by default, then returns a `Response` for the main resource, or `None` for things like `about:blank` or hash changes. `status`, `ok`, `url` and `headers` are properties in Python.

`goto` does not raise on HTTP errors. A 404 or 500 still loads a page, so I check it myself:

```python
r = page.goto("/missing")
assert r.status == 404 and not r.ok
expect(page.get_by_role("heading", name="Page not found")).to_be_visible()
```

It raises only for network-level problems such as `net::ERR_NAME_NOT_RESOLVED` (I got exactly that for a `.invalid` domain), certificate errors, or a timeout.

The `wait_until` stages are:
- `commit`: the response started arriving. Earliest.
- `domcontentloaded`: HTML parsed.
- `load`: page and its resources loaded. This is the default and fine for most tests.
- `networkidle`: no network for 500 ms. Discouraged, because pages with analytics, polling or websockets may never reach it. I wait for the element or content I need instead.

With a `base_url` on the context I can write `page.goto("/products")`, so switching environments is one config change.
</details>

---

#### Q34: How do you automate a file upload in Playwright without touching the operating system dialog? What if the input is hidden or created only when a button is clicked? [File Upload and Download]
**Keywords:** set_input_files, expect_file_chooser, in-memory buffer, multiple, clear
<details>
<summary>Click to Reveal Answer</summary>

Playwright never opens the OS dialog. I set the files directly on the `<input type="file">`:

```python
page.get_by_label("Documents").set_input_files(DATA / "resume.pdf")        # pathlib.Path or str
page.get_by_label("Documents").set_input_files([DATA / "a.png", DATA / "b.png"])   # needs `multiple`
page.get_by_label("Documents").set_input_files([])                         # clears the selection
```

It works even if the input is hidden, because nothing is clicked, and it fires the `input` and `change` events. A non-`multiple` input given two files raises "Non-multiple file input can only accept single file". A new call replaces the selection, it does not append.

I can also upload an in-memory file, which keeps test data visible in the test and avoids files in the repo:

```python
page.get_by_label("Documents").set_input_files(
    {"name": "customers.csv", "mimeType": "text/csv", "buffer": b"id,name\n1,Maria\n"}
)
```

If the app creates the input only when a button is clicked, there is nothing to attach to, so I catch the file chooser, again register first and then act:

```python
with page.expect_file_chooser() as fc:
    page.get_by_role("button", name="Choose avatar").click()
fc.value.set_files(DATA / "me.png")
```

Afterwards I assert the app's reaction, such as the file name shown, a preview, or the response. I do not rely on `to_have_value`, since the browser exposes `C:\fakepath\name`. Also, `accept` is only a hint: `set_input_files` happily set an `.exe` on an input with `accept=".txt,.csv"`, which is useful for testing server-side validation.
</details>

---

### Intermediate (Application)

#### Q35: After clicking Log in, the app redirects through several URLs and finally lands on `/dashboard`, and the dashboard is a single-page app. How do you wait for and verify the navigation reliably? [Navigation Events]
**Keywords:** wait_for_url, to_have_url, regex, expect_navigation, SPA content
<details>
<summary>Click to Reveal Answer</summary>

I express the wait as the destination or outcome, not the mechanism. Playwright's click already waits for the navigation it started, so I just click and then wait on the final result:

```python
page.get_by_role("button", name="Log in").click()
page.wait_for_url("**/dashboard")                 # glob, regex or predicate
expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
```

`wait_for_url` does not care how many redirect hops happen in between. It also recognises History API (`pushState`) and hash changes, which matters for SPAs, where no new `load` event fires. `wait_for_load_state()` there returns instantly and proves nothing.

Two traps. First, in an SPA the URL changes before the content. In my test the heading still said "Home view" right after `wait_for_url`, and showed "Orders view" 400 ms later. So I always finish with a content assertion.

Second, `expect(page).to_have_url("...")` with a string is an exact match in Python. A glob like `"**/products"` and a partial string like `"/prod"` both failed in my run, and so did the URL `.../login` against an actual URL of `.../login?next=...`, because the query string is part of the full URL. I use a compiled regex, `re.compile(r"/login\?next=")`, or parse the URL:

```python
u = urlparse(page.url)
assert u.path == "/login" and parse_qs(u.query)["next"] == ["/protected"]
```

I avoid `page.expect_navigation()`. It is legacy and racy: it hangs until timeout when no navigation happens (I saw a `TimeoutError` after clicking a non-navigating element), can resolve on the first hop of a redirect chain, and ties the test to how the page navigates rather than where the user ends up.
</details>

---

#### Q36: Your app has an "Export CSV" button. How do you test the download end to end, and what do you check besides "a file arrived"? [File Upload and Download]
**Keywords:** expect_download, suggested_filename, save_as, content verification, failure
<details>
<summary>Click to Reveal Answer</summary>

I use the same register-first pattern, then verify name, success and content:

```python
with page.expect_download() as info:
    page.get_by_role("link", name="Download CSV").click()
download = info.value

assert download.failure() is None
assert download.suggested_filename == "orders.csv"
dest = tmp_path / download.suggested_filename
download.save_as(dest)

with dest.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 3
assert rows[0]["name"] == "Maria"
```

Points I would call out:
- `suggested_filename` comes from `Content-Disposition` (or the `download` attribute), not the URL. In my run the URL was `/export.csv` but the suggested name was `orders.csv`.
- `save_as()` waits for the download to finish and copies it to a path I control. `download.path()` points at a temporary file with a generated name that is deleted when the context closes, so I do not rely on it long term.
- Checking only that a file exists is weak. I verify content with `csv.DictReader`, `json`, or libraries such as `pypdf` and `openpyxl`. CSV values are strings, so I convert before arithmetic, and I can compare the rows with the table shown on screen.
- JavaScript Blob downloads trigger the same event, so the pattern is identical.
- If the click happens before `expect_download` is registered, the event is missed and I get a timeout.
- If a server sends a PDF inline, the built-in viewer may open and no download event fires. Then I either get the server to send `attachment`, or fetch it with `page.request.get(url)`, which shares the page's cookies.
- For a slow report I raise the timeout on that one call, `expect_download(timeout=60_000)`, not globally.
</details>

---

#### Q37: A test intermittently fails because a newsletter pop-up sometimes covers the Buy button, and the author "fixed" it with `time.sleep(3)` and `force=True`. How would you fix it properly? [Dynamic Elements]
**Keywords:** add_locator_handler, call log, receives events, no sleep, force
<details>
<summary>Click to Reveal Answer</summary>

Both "fixes" hide the problem. The sleep is slow and still flaky, and `force=True` skips the actionability checks, so it can click covered or disabled elements and hide real defects.

First I read the call log. A covered button times out with the button resolved but the click retried, and the log names the intercepting element. That confirms it is the overlay.

For a genuinely unpredictable interruption I register a locator handler once, at the start of the test or in shared setup:

```python
page.add_locator_handler(
    page.get_by_text("Subscribe to our newsletter"),
    lambda: page.get_by_role("button", name="No thanks").click(),
)
page.get_by_role("button", name="Buy now").click()
expect(page.locator("#bought")).to_have_text("Bought!")
```

Whenever Playwright is blocked on an actionability check and that overlay is visible, it runs my handler, then retries. In my test with a full-screen overlay appearing after 300 ms, the Buy click went through and the page showed "Bought". `times=` limits how often it runs and `remove_locator_handler` removes it.

For a banner that always appears on first visit, I would dismiss it deterministically in setup or pre-set the consent cookie rather than use a handler. I would also delete the sleep, and wait on outcomes with `expect`. If an id is generated, like `btn-8f3a2`, I use role and name or a prefix selector such as `[id^='btn-']` instead of the full id.
</details>

---

#### Q38: A sign-up form blocks users under 18, and another test books "tomorrow". Both break at month ends and near midnight. How do you make date-dependent UI tests deterministic? [Date Pickers]
**Keywords:** page.clock, set_fixed_time, boundary values, timezone_id, locale
<details>
<summary>Click to Reveal Answer</summary>

I control the browser's clock and the environment instead of depending on the real date.

```python
ctx = browser.new_context(timezone_id="UTC", locale="en-US")
page = ctx.new_page()
page.clock.set_fixed_time(datetime(2025, 3, 14, 12, 0, tzinfo=timezone.utc))
page.goto("/signup")                                 # after the clock is set

page.get_by_label("Date of birth").fill("2007-03-14")   # turns 18 today
expect(page.get_by_text("You must be at least 18")).to_be_hidden()
page.get_by_label("Date of birth").fill("2007-03-15")   # turns 18 tomorrow
expect(page.get_by_text("You must be at least 18")).to_be_visible()
```

Key details:
- `set_fixed_time` makes `Date.now()` and `new Date()` constant while timers still run. It must be set before the page scripts read the time, so before `goto`. In my test, a page that had already loaded kept the old year, while a fresh evaluation returned the new one.
- I pass a timezone-aware datetime. A naive `datetime(2025, 3, 14, 10, 0)` is interpreted in the Python machine's local time zone, so on a New York machine I observed 14:00 UTC, which can shift the date near midnight.
- It affects only the browser. Server-side checks still use the real date, so those need backend seeding.
- `locale` changes how native inputs display dates but the `fill` value stays `YYYY-MM-DD`; `timezone_id` changes what JavaScript's `Date` sees. I pin both so results do not depend on a laptop or the CI region.
- I apply boundary-value analysis: the day before, the day of, and the day after the rule, plus leap-year cases such as 28 February 2028 to 1 March 2028. I compute expected values from Python rather than hard-coding them.
</details>

---

#### Q39: You must test (a) a chat feature between two users, and (b) a Terms link that the user opens with Ctrl+Click into a background tab. Which Playwright constructs do you use, and what pitfalls apply? [Tabs and Windows]
**Keywords:** two contexts, shared cookies, expect_page, popup event, context.route
<details>
<summary>Click to Reveal Answer</summary>

For two users I use two browser contexts, not two tabs. Tabs in one context share cookies and storage, so they would be the same logged-in user. Contexts are isolated, like two separate profiles:

```python
alice = browser.new_context().new_page()
bob = browser.new_context().new_page()
alice.goto(URL); bob.goto(URL)
alice.get_by_label("Message").fill("Hello Bob")
alice.get_by_role("button", name="Send").click()
expect(bob.get_by_text("Hello Bob")).to_be_visible()
```

I confirmed that a cookie set in one tab was visible in a second tab of the same context, and was an empty string in a different context.

For the Ctrl+Click, I use `context.expect_page()`:

```python
with context.expect_page() as new_page_info:
    page.get_by_role("link", name="Terms").click(modifiers=["ControlOrMeta"])
tab = new_page_info.value
expect(tab).to_have_url(re.compile(r"/terms$"))
```

`modifiers=["ControlOrMeta"]` means Ctrl on Windows or Linux and Cmd on macOS. In my run the page-level `popup` event did not fire for the Ctrl+Click, so `page.expect_popup()` would have timed out, while `context.expect_page()` caught it. I assert on the URL because a background tab may not have loaded yet.

Other pitfalls: register routes and init scripts on the context, not the page. With `page.route(...)` only, my popup could not load the mocked site at all and ended up on an error page. And `context.pages` is a snapshot list, so I re-read it when I need the current count.
</details>

---

### Advanced (Deep Dive)

#### Q40: A checkout page embeds the card field as a third-party iframe. Inside that iframe the field is a web component with an open shadow root, and a "Verify with your bank" link opens a pop-up. Walk through how you would locate and automate each layer, what Playwright is doing under the hood, and what would break. [Frames, Shadow DOM, Tabs and Windows]
**Keywords:** frame_locator, shadow piercing, lazy locator, expect_popup, cross-origin
**Hint:** Treat the iframe boundary and the shadow boundary separately, since they are handled differently.
<details>
<summary>Click to Reveal Answer</summary>

The two boundaries are different, so I handle them differently. The iframe is a separate document, so I must enter it explicitly with `frame_locator`. The shadow root is inside that document and open, so Playwright's selector engine pierces it by itself.

```python
pay = page.frame_locator("iframe[title='Secure payment']")
pay.get_by_label("Card").fill("4242 4242 4242 4242")        # input is inside the shadow root
pay.get_by_role("button", name="Pay now").click()
expect(pay.get_by_role("status")).to_have_text("Paid 4242 4242 4242 4242")

with page.expect_popup() as info:
    pay.get_by_role("link", name="3DS").click()
bank = info.value                                            # opener is the checkout page
expect(bank.get_by_role("heading", name="Verify")).to_be_visible()
```

I ran this shape against a real local server and it worked. Under the hood: a FrameLocator and a Locator are not node references but recipes. On every action Playwright finds the iframe, goes into its document, runs its selector engine, which walks through open shadow roots, then waits for actionability. That is why there is no "switch to frame" state to forget and no stale element after a re-render. `get_by_role` works against the flattened accessibility tree, so slotted content and shadow content are named like a user would see them.

What would break:
- A page-level locator returns 0, because it only searches the main frame.
- `evaluate("document.querySelector('#pay')")` inside the frame returns `None` because the raw browser query stops at the shadow boundary. XPath would also fail there.
- If the root were closed, locators would find nothing. I would ask for a test hook on the host, and only as a last resort patch `attachShadow` with an init script added before the page scripts.
- The popup is opened from a frame, but `page.expect_popup()` still caught it in my run and `popup.opener()` was the page, so it must be registered before the click. If it did not fire, `context.expect_page()` is the wider net.
- Cross-origin is not a problem for Playwright, because it controls the browser from outside, unlike page scripts bound by the same-origin policy. The real limits are providers that block automation (CAPTCHA, real 3-D Secure), where I use a test mode or a stub rather than fight them. I also keep the selectors in one helper, because third-party markup changes without notice.
</details>

---


## Day 3 (Wednesday): Playwright Framework Design

### Beginner (Foundational)

#### Q41: What is a pytest fixture, and how does a test use one? [Fixtures]
**Keywords:** `@pytest.fixture`, dependency injection, parameter name, setup, reuse
**Hint:** Think about how the test asks for something without calling a function.
<details>
<summary>Click to Reveal Answer</summary>

A fixture is a function decorated with `@pytest.fixture` that pytest runs for me to prepare something a test needs, such as a browser page, test data, or a logged-in user.

A test requests a fixture simply by naming it as a parameter. pytest matches the parameter name to the fixture name, runs the fixture, and passes in the result. That is dependency injection, and I never call the fixture myself.

```python
import pytest

@pytest.fixture
def greeting():
    return "hello"

def test_greeting(greeting):
    assert greeting == "hello"
```

In Playwright this removes the repeated boilerplate of starting Playwright, launching a browser, creating a context and closing everything. Setup and teardown live in one central place, so a change like a new viewport is made once instead of in every test.
</details>

---

#### Q42: Which built-in fixtures does pytest-playwright give you, and why are `browser` and `page` scoped differently? [Fixtures]
**Keywords:** `page`, `context`, `browser`, session scope, function scope, isolation
**Hint:** One is about speed, the other is about isolation.
<details>
<summary>Click to Reveal Answer</summary>

pytest-playwright provides `playwright`, `browser_type`, `browser`, `browser_name`, `browser_context_args`, `browser_type_launch_args`, `new_context`, `context`, `page`, and `base_url`, among others. I do not import them; they just exist once the plugin is installed.

`browser` is session scoped, so one browser process is launched for the whole run, which is fast. `context` and `page` are function scoped, so every test gets a fresh, isolated context, like a new incognito profile. Cookies and local storage never leak between tests. That combination gives speed and isolation.

The golden rule of scope is that a fixture can only depend on fixtures with the same or a wider scope. If I write a `scope="session"` fixture that requests `page`, pytest raises `ScopeMismatch: You tried to access the function scoped fixture page with a session scoped request object`. The fix is to depend on `browser` instead and create my own context, or to narrow my fixture's scope.
</details>

---

#### Q43: What is the difference between `return` and `yield` in a fixture, and how do you customise how every test's browser context is created? [Fixtures]
**Keywords:** yield, teardown, reverse order, `conftest.py`, `browser_context_args`
**Hint:** Think about code that must run even when the test fails.
<details>
<summary>Click to Reveal Answer</summary>

A `return` fixture can only do setup. With `yield`, everything before the `yield` is setup, the yielded value goes to the test, and everything after it is teardown. The teardown runs even if the test failed. Teardown order is the reverse of setup order, like unstacking plates.

```python
@pytest.fixture
def temp_user():
    user = create_user_via_api()
    yield user
    delete_user_via_api(user["id"])
```

To customise every context, I override the session-scoped `browser_context_args` fixture in `conftest.py`. I take the parent version as a parameter and extend it, so I do not lose CLI options like `--device`:

```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 768}}
```

`conftest.py` is found automatically, so tests never import from it. `browser_type_launch_args` works the same way for launch options.
</details>

---

#### Q44: When people say "hooks" in pytest, what two different things can they mean? [Hooks]
**Keywords:** setup/teardown, plug-in hooks, `pytest_*` functions, `conftest.py`, fixture
**Hint:** Ask yourself: am I preparing something for a test, or reacting to something pytest is doing?
<details>
<summary>Click to Reveal Answer</summary>

The word is overloaded, so I separate the two meanings.

The first is setup and teardown code I write for my tests, "run this before each test, clean up after". In pytest that is normally a `yield` fixture, or older xunit-style methods like `setup_method`.

The second is plug-in hooks, which are extension points pytest itself defines. pytest announces events such as "a report was just created" or "the session is starting", and any function in `conftest.py` named exactly like the hook, such as `pytest_runtest_makereport`, `pytest_configure`, `pytest_addoption`, or `pytest_sessionfinish`, gets called. The name is the contract.

My rule of thumb: if I am preparing something a test needs, it is a fixture. If I am reacting to something happening in the run, it is a plug-in hook.
</details>

---

#### Q45: pytest has no `beforeEach` or `afterEach`. How do you get that behaviour, and what are the other scopes for? [Hooks]
**Keywords:** `yield` fixture, `autouse`, scope, `setup_method`, session
**Hint:** Same mechanism, different `scope=` value.
<details>
<summary>Click to Reveal Answer</summary>

The idiomatic equivalent is a function-scoped `yield` fixture. Code before the `yield` is "beforeEach", code after is "afterEach". If it should apply to every test without being requested, I add `autouse=True`.

```python
@pytest.fixture(autouse=True)
def boundaries(request):
    print(f"START {request.node.name}")
    yield
    print(f"END {request.node.name}")
```

The same mechanism covers "before all" through scope: `scope="session", autouse=True` runs once per run, `scope="module"` once per file, `scope="class"` once per class.

There are also xunit-style hooks like `setup_module`, `setup_class` and `setup_method`. They work, but they cannot easily pass values or request built-in fixtures like `page`, so I mostly use them for legacy code. One caution: an autouse fixture that requests `page` creates a browser page for every test in scope, including non-UI tests, so I keep it in the UI folder's `conftest.py`.
</details>

---

#### Q46: How would you automatically capture a screenshot when a Playwright test fails? [Hooks]
**Keywords:** `pytest_runtest_makereport`, hookwrapper, `rep_call`, `request.node`, phases
**Hint:** pytest builds a report for three phases of each test.
<details>
<summary>Click to Reveal Answer</summary>

Each test runs in three phases: setup, call (the test body), and teardown. After each, pytest builds a report. I use a hook wrapper on `pytest_runtest_makereport` to store each report on the test item, then read it in a fixture after the test.

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

@pytest.fixture
def page_with_evidence(page, request):
    yield page
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        page.screenshot(path=f"reports/{request.node.name}.png", full_page=True)
```

Two details matter. I use `getattr(..., None)` because if setup failed there is no `rep_call`. And the fixture explicitly requests `page`, so `page` is torn down after my code and is still open when I screenshot. I checked this: the page was not closed at that point.

pytest-playwright can also do it with no code through `--screenshot only-on-failure`. I write the hook when I need custom names, an HTML dump, or console logs.
</details>

---

#### Q47: What is the Page Object Model, and what problem does it solve? [POM]
**Keywords:** page class, locators, user actions, maintainability, separation of concerns
**Hint:** Think about what happens to 120 tests when one locator changes.
<details>
<summary>Click to Reveal Answer</summary>

POM represents each page, or significant component, of the application as a class. The class owns the locators for that page and exposes methods for what a user can do there, like `login_as(...)`. Tests call those methods and never contain raw selectors.

It solves the flat-script problem: duplicated login steps, selectors scattered everywhere, hard-coded values, and low-level clicks hiding the intent. If the username field changes from `#user-name` to a label "Email", I edit one line in `LoginPage` instead of 120 tests.

It gives three clean layers: tests say what to verify, page objects say what a user can do, and Playwright drives the browser. It pays off as soon as a second test touches the same page; for a three-test throw-away script it is overkill.
</details>

---

#### Q48: How do you design a page class in Python for Playwright? Why is it safe to define locators in `__init__`? [POM]
**Keywords:** constructor, lazy locator, `BasePage`, user-intent methods, dependency injection
**Hint:** When does a Playwright `Locator` actually look for the element?
<details>
<summary>Click to Reveal Answer</summary>

The class receives the Playwright `Page` in its constructor (dependency injection, so a fixture controls the browser). It defines locators once in `__init__`, and exposes methods named for user intent rather than UI mechanics.

```python
class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")

    def login_as(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

It is safe to create locators up front because a `Locator` is lazy. It only stores how to find the element and searches at the moment I act or assert, with auto-waiting. So there are no stale element references like in older Selenium page objects.

Other good practices: a small `BasePage` for shared behaviour, `super().__init__(page)` in children, user-facing locators like `get_by_role` or `get_by_test_id`, and methods that return the next page object for navigation.
</details>

---

#### Q49: Should page objects contain assertions? And how do tests get their page objects? [POM]
**Keywords:** assertions in tests, readiness check, `expect_loaded`, fixtures, God page
**Hint:** Page objects may wait; tests decide what is correct.
<details>
<summary>Click to Reveal Answer</summary>

The convention I follow is that page objects expose actions and state queries, such as `get_error_message()`, and the test makes the assertion. A page method that asserts a fixed title cannot be reused by a test that expects something else, and assertion-heavy page objects hide test logic and make failures hard to read.

The accepted exception is a clearly named readiness check like `expect_loaded()`, which confirms we really arrived on the page. I use web-first `expect(...)` there so it auto-retries.

Tests get page objects from fixtures rather than constructing them repeatedly:

```python
@pytest.fixture
def login_page(page):
    return LoginPage(page).open()

@pytest.fixture
def inventory_page(login_page):
    return login_page.login_successfully("standard_user", "secret_sauce")
```

So fixtures decide how we get to a starting point, page objects decide how to act, and tests decide what to verify. Anti-patterns to avoid are locators leaking into tests, a God page with 80 methods, and `time.sleep` inside page methods.
</details>

---

#### Q50: You inherit a pile of flat Playwright scripts. How do you convert them to POM safely? [Converting scripts to POM]
**Keywords:** green baseline, small steps, assertions checklist, commit, page by page
**Hint:** Refactoring changes structure, not behaviour.
<details>
<summary>Click to Reveal Answer</summary>

Refactoring means changing structure without changing observable behaviour, so I work in small, verified steps.

1. Start from green. If tests are already failing or flaky I fix or quarantine them first, then commit a baseline.
2. Write an assertions checklist, a list of every check the tests make, so I can prove I did not weaken them.
3. Set up the skeleton: `pytest.ini` with `base_url`, `pythonpath = .`, and a `conftest.py` that sets the test-id attribute.
4. Analyse the script into pages, components, actions and state reads, on paper first.
5. Convert one page at a time, starting at the top of the journey (login). Replace only those lines, run the tests, commit.
6. Add a `BasePage` and components like a header once code is shared.
7. Make navigation methods return the next page object with a readiness check.
8. Deliver starting points through fixtures, remove hard-coded data, delete the old flat copy.
9. Tick the checklist and mutation-test: deliberately break an expected value and confirm the test fails for the right reason.

The classic mistakes are a big-bang rewrite, refactoring on red, and silently dropping assertions. An assertion may move into `expect_loaded()`, but it must not disappear.
</details>

---

#### Q51: Describe the layers of reporting in Python Playwright and the commands for each. [Playwright reporting]
**Keywords:** console output, `--junitxml`, `pytest-html`, `--self-contained-html`, exit codes
**Hint:** Python uses pytest as the runner, not the Node.js HTML reporter.
<details>
<summary>Click to Reveal Answer</summary>

In Python the runner is pytest, so reporting comes from pytest and its plug-ins plus Playwright's own artifacts. The Node `npx playwright show-report` and `--reporter=html` instructions do not apply.

- Layer 1, console output: `-v` for node ids, `-ra` for a summary of all non-passing outcomes, `--durations=10` for the slowest tests, `--lf` to re-run last failures. Exit code `0` means all passed, `1` some failed, `5` no tests collected. CI treats non-zero as failure.
- Layer 2, JUnit XML: `pytest --junitxml=reports/junit.xml`. CI tools like Jenkins and GitHub Actions parse it. It is for machines, not people.
- Layer 3, pytest-html: `pytest --html=reports/report.html --self-contained-html`. The self-contained flag embeds CSS and images so I can email the one file.
- Layer 4, dashboards like Allure for trends and history.

Readable parametrised ids pay off here, because a failure shows as `[wrong-password]` instead of `case1`.
</details>

---

#### Q52: What is data-driven testing, and how do you drive a Playwright test from a JSON file? [Data-driven testing with JSON]
**Keywords:** `parametrize`, `ids`, `json.load`, `pathlib`, test data separation
**Hint:** One test body, a table of cases.
<details>
<summary>Click to Reveal Answer</summary>

Data-driven testing runs the same test logic against many data sets, each with its own expected result. The data lives outside the test function, so a new scenario is a new row, not a new function, and results are reported per row.

I load the JSON with Python's built-in `json` module and feed it to `@pytest.mark.parametrize`. `json.load` reads from a file object and `json.loads` from a string (the `s` stands for string). I build the file path from `__file__` with `pathlib`, so it works wherever pytest is launched from.

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def load_json(name):
    with (PROJECT_ROOT / "data" / name).open(encoding="utf-8") as f:
        return json.load(f)

CASES = load_json("login_data.json")["invalid_logins"]

@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_invalid_login(login_page, case):
    login_page.login_as(case["username"], case["password"])
    expect(login_page.error_message).to_have_text(case["expected_error"])
```

JSON rules to remember: double-quoted keys, no trailing commas, no comments, and lower-case `true`, `false`, `null`. I validate a file with `python -m json.tool`. The file loads at import time because `parametrize` needs the data during collection.
</details>

---

#### Q53: What is a flaky test, and what does `--reruns` do? [Test retries]
**Keywords:** flaky, `pytest-rerunfailures`, `--reruns`, `--reruns-delay`, attempts
**Hint:** `--reruns 2` means how many total attempts?
<details>
<summary>Click to Reveal Answer</summary>

A flaky test passes and fails on the same code with no intentional change. It always has a cause: timing and synchronisation, shared state, test data, environment, network or third-party scripts, or non-determinism in the app.

`pytest-rerunfailures` re-runs failed tests. `pytest --reruns 2` allows at most three attempts: the first run plus two reruns. Each rerun starts from scratch. If any attempt passes the final result is passed, and the report still records the reruns. `--reruns-delay 3` waits three seconds between attempts. The console shows `R` for each rerun and a summary like `1 passed, 2 rerun`.

The key point I make in an interview is that a retry is a safety net, not a fix. Before reaching for reruns I exhaust Playwright's built-in auto-waiting and web-first `expect` assertions. A test that needs a retry to pass is a defect in the suite and should get a ticket.
</details>

---

#### Q54: Which artifacts can pytest-playwright record on failure, and how do you use the Trace Viewer? [Playwright reporting]
**Keywords:** `--screenshot`, `--video`, `--tracing`, `retain-on-failure`, `trace.zip`
**Hint:** Open the trace before guessing.
<details>
<summary>Click to Reveal Answer</summary>

pytest-playwright records artifacts through command-line options, no hook code needed:

```bash
pytest --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure --output test-results
```

`--screenshot` accepts `on`, `off` and `only-on-failure`. `--video` and `--tracing` accept `on`, `off` and `retain-on-failure`. Artifacts go in `test-results/`, in a folder per test and per browser. I confirmed a failing run produces `test-failed-1.png`, `video.webm` and `trace.zip`. That folder is wiped at the start of each run, so it belongs in `.gitignore`.

A trace records every action with before and after DOM snapshots, network requests, console messages and the source line. I open it with `playwright show-trace trace.zip` or at trace.playwright.dev. To triage, I click the red failing action, read the Errors tab and the call log (what Playwright was waiting for), look at the Before snapshot for overlays, and check Network and Console.

In CI I use `retain-on-failure`, because recording everything costs time and disk. I switch to `on` only when debugging.
</details>

---

### Intermediate (Application)

#### Q55: Your team wants to turn on `--reruns 3` globally because the nightly suite is flaky. What do you recommend and how would you configure it? [Test retries]
**Keywords:** `--only-rerun`, `@pytest.mark.flaky`, root cause, lowest layer, `--reruns 0`
**Hint:** Retry at the lowest layer that fixes the problem, and only for failures a retry can fix.
<details>
<summary>Click to Reveal Answer</summary>

I would push back on a blanket `--reruns 3`. It multiplies suite time, retries deterministic failures that will fail every time, and can hide real defects. I would recommend this order of defence: auto-waiting and web-first `expect`, then explicit waits and sensible timeouts, then a narrow retry helper, and only then whole-test reruns.

For the config I would keep the count small and filter by failure type:

```ini
addopts = --reruns 1 --reruns-delay 1 --only-rerun TimeoutError --only-rerun "net::ERR_"
```

`--only-rerun` retries only when the error text matches a regex, and `--rerun-except AssertionError` does the opposite. For a known unstable test I use `@pytest.mark.flaky(reruns=2, reruns_delay=2)` with a comment and a defect id. A marker overrides the command-line count for that test; I confirmed `reruns=1` gave two attempts even when I passed `--reruns 3`.

One trap I tested: a timed-out `expect(...)` raises `AssertionError`, not `TimeoutError`, so `--only-rerun TimeoutError` does not retry it, while a timed-out `click()` is retried. I would look at real failure output before choosing patterns.

Locally I debug with `--reruns 0`, use a small count in CI, and track the rerun rate as a health metric.
</details>

---

#### Q56: How would you set up reporting for a Playwright suite running in GitHub Actions so a 3 a.m. failure can be diagnosed in the morning? [Playwright reporting]
**Keywords:** `--html`, `--junitxml`, `if: always()`, `retain-on-failure`, upload artifacts
**Hint:** What happens to later steps when the test step fails?
<details>
<summary>Click to Reveal Answer</summary>

No one is watching the browser in CI, so the report and artifacts are the only evidence. I generate both a human report and a machine report, keep evidence only for failures, and make sure it is uploaded even when tests fail.

```yaml
- name: Run tests
  run: pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml --tracing retain-on-failure --screenshot only-on-failure --reruns 1
- name: Upload reports and traces
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-reports
    path: |
      reports/
      test-results/
```

`if: always()` is critical. By default a step is skipped after a failed step, which would throw away exactly the evidence I need. `--self-contained-html` makes the report a single portable file, and JUnit XML lets the CI UI show counts and trends.

I also add metadata (application, base URL, commit SHA) through `pytest_configure`, attach failure screenshots with a `makereport` hook and `extras.png`, and keep `reports/`, `test-results/` and `.auth/` out of Git. Artifacts can contain tokens or personal data, so I treat them as sensitive. In the morning I filter the report to Failed and Rerun, classify each failure as product bug, test bug, data or environment, and open the trace when the cause is not obvious.
</details>

---

#### Q57: When converting a flat script to POM, how do you handle navigation, dialogs and new tabs, and what happens to the URL assertions? [Converting scripts to POM]
**Keywords:** return next page, `expect_loaded`, `page.once("dialog")`, `expect_page`, `base_url`
**Hint:** Assertions are moved, not deleted. Also watch how `to_have_url` behaves once `base_url` is set.
<details>
<summary>Click to Reveal Answer</summary>

Methods that move to a new screen return the next page object and run a readiness check, so the test reads like a journey and the old inline URL assertions live in one consistent place:

```python
def proceed_to_checkout(self) -> CheckoutInfoPage:
    self.checkout_button.click()
    info = CheckoutInfoPage(self.page)
    info.expect_loaded()
    return info
```

A method that stays on the same screen returns `self` or `None`. I split methods by outcome, for example `continue_to_overview` and `continue_expecting_error`, rather than using a boolean flag.

For a dialog, the handler must be registered before the triggering click, because Playwright auto-dismisses unhandled dialogs: `self.page.once("dialog", lambda d: d.accept() if accept else d.dismiss())` then click. For a new tab, I use `with self.page.context.expect_page() as info: self.link.click()` and return a page object bound to `info.value`. The page object boundary follows the browser tab. For back-navigation I import the target class inside the method to avoid circular imports.

A caveat I verified by running it: once `base_url` is configured, `expect(page).to_have_url("**/cart.html")` fails, because the glob is joined onto the base URL and becomes `http://host/**/cart.html`. In `expect_loaded` I use a regex such as `re.compile(r".*/cart\.html")`, a relative path like `"/cart.html"`, or the full URL. `page.wait_for_url("**/cart.html")` is fine.
</details>

---

#### Q58: Your JSON-driven login test has four cases. One is a known defect, and a teammate wants to re-run just one case. How do you handle both? [Data-driven testing with JSON]
**Keywords:** `pytest.param`, `xfail`, `ids`, `-k`, `indirect`
**Hint:** Marks can be attached per row, and ids include the browser name.
<details>
<summary>Click to Reveal Answer</summary>

For the known defect I attach a mark to that row only, so the suite stays green but still tracks the bug. I can do it in a small loader that reads an `"xfail"` field from the JSON:

```python
if "xfail" in item:
    marks.append(pytest.mark.xfail(reason=item["xfail"]))
params.append(pytest.param(item, marks=marks))
```

The row reports as `xfailed`. When the bug is fixed it reports `XPASS`, a signal to remove the marker.

Every case needs a meaningful `id` from the data, such as `empty-username`, otherwise reports show `case0`. To run one case I use `-k`:

```bash
pytest -k "empty-username" --reruns 0
```

Selecting by exact node id from older notes may not work, because pytest-playwright puts the browser in the id. The real id is `test_x[chromium-empty-username]`, which I confirmed with `--collect-only -q`.

If the data must pass through setup, such as logging in as each user, I use `indirect=True` so the value reaches the fixture's `request.param` and the test receives the fixture's return value. I treat loaded data as read-only, keep secrets out of JSON, and avoid stacked `parametrize` decorators that explode into hundreds of browser tests.
</details>

---

#### Q59: A test passes on its second attempt under `--reruns`. What exactly happens to fixtures and external state on a rerun, and how can you capture extra diagnostics? [Test retries]
**Keywords:** function-scoped fixtures, session fixtures, idempotent, `execution_count`, `--tracing`
**Hint:** Which fixtures are rebuilt and which are not?
<details>
<summary>Click to Reveal Answer</summary>

Function-scoped fixtures are torn down after the failed attempt and set up again, so each attempt gets a brand new browser context and page. That is why context-per-test isolation and reruns fit together well. I confirmed this by counting: a function fixture ran setup three times over three attempts, while a session fixture ran once.

Two consequences follow. Session or module fixtures holding mutable state, like a shared cart, carry stale state into the retry, so I keep mutable state function-scoped. And external state is not reset. If the first attempt created an order in the backend, the rerun creates another, so tests must be idempotent or clean up in `yield` teardown.

For diagnostics, the plug-in records the attempt number as `execution_count` on the test item:

```python
@pytest.fixture
def attempt(request):
    return getattr(request.node, "execution_count", 1)

@pytest.fixture(autouse=True)
def verbose_on_retry(page, attempt):
    if attempt > 1:
        page.on("console", lambda m: print(f"[retry] {m.text}"))
    yield
```

With `--tracing retain-on-failure` I also get artifacts for the failed attempt, which I read before dismissing it as "just flaky". It might be a real race condition in the product.
</details>

---

### Advanced (Deep Dive)

#### Q60: Design the page object layer for an app where every page has the same header, one link opens a Help page in a new tab, and pages navigate forward and back. How do you avoid circular imports and keep the framework maintainable? [Converting scripts to POM]
**Keywords:** composition, component, circular import, lazy import, fixtures
**Hint:** "Has a" versus "is a", and which direction imports flow.
<details>
<summary>Click to Reveal Answer</summary>

I would model it in three parts.

First, a small `BasePage` holding only generic behaviour: the `page`, a `PATH`, and a shared `expect_loaded()`. I would keep it small so it does not become a hidden God class. Methods used by only one page stay on that page.

Second, the repeated header becomes a `Header` component class, and pages compose it with `self.header = Header(page)`. Composition ("has a") beats inheritance ("is a") for components. The same idea applies to product cards, tables and footers. A UI change to the header is then a one-file change.

```python
class FooterComponent:
    def open_help(self) -> "HelpPage":
        with self.page.context.expect_page() as new_tab:
            self.help_link.click()
        help_page = HelpPage(new_tab.value)
        help_page.page.wait_for_load_state()
        return help_page
```

Third, imports. Forward navigation follows the user journey (`LoginPage` imports `InventoryPage`, which imports `CartPage`), so module-level imports never form a cycle. For back-navigation, like `CartPage.continue_shopping()` returning `InventoryPage`, I import inside the method body:

```python
def continue_shopping(self):
    from pages.inventory_page import InventoryPage  # avoids a cycle
    ...
```

Fixtures deliver starting points (`login_page`, `inventory_page`, `checkout_info_page`) so tests do not repeat setup, and page objects receive `page` rather than launching browsers. Data such as users and products lives in JSON, not in the classes. Assertions stay in tests, except named readiness checks, and I use relative paths with `base_url` configured once. My review rule is: if one UI change touches more than one file, the design needs another look.
</details>

---


## Day 4 (Thursday): Cypress

### Beginner (Foundational)

#### Q61: What is Cypress, and how is its architecture different from Playwright's? [Architecture]
**Keywords:** Runs inside the browser, Node process, Same run loop, Proxy, JavaScript/TypeScript only
**Hint:** Think about where your test code actually executes.
<details>
<summary>Click to Reveal Answer</summary>

Cypress is an open-source front-end testing tool for JavaScript and TypeScript. It supports end-to-end testing and component testing, and it runs tests in a real browser that you can watch.

The big architectural difference is where the test code runs. Playwright runs your test in a separate process, and that process remote-controls the browser over a protocol. Cypress runs your spec code inside the browser, right next to the application under test. The spec and the app are loaded in two iframes of the same page.

Cypress also has a Node.js process behind the scenes. It reads the config, starts a proxy that all browser traffic passes through, launches the browser and handles files. When a test needs something only Node can do, such as reading a database, it asks that process through `cy.task()`, `cy.readFile()` or `cy.exec()`.

The trade-offs follow from that. Cypress is fast and has deep visibility, because it can reach the app's `window` directly and take DOM snapshots per command. The limits are one tab per test, JavaScript/TypeScript only, and same-origin restrictions that `cy.origin()` relaxes. Playwright supports several languages, multiple tabs and stable WebKit.
</details>

---

#### Q62: Why can't you use `async/await` with Cypress commands, and what is wrong with `const btn = cy.get('button')`? [Command Queue]
**Keywords:** Command queue, Chainable, Not a Promise, `.then()`, Alias
**Hint:** When does `cy.get` actually run?
<details>
<summary>Click to Reveal Answer</summary>

Cypress commands do not run when the line executes. Each `cy.*` call adds a command to an internal queue and returns a Chainable straight away. After the test body has finished, Cypress runs the queue one command at a time.

A Chainable looks like a promise but it is not one, so `await cy.get(...)` does not give you the element. For the same reason `const btn = cy.get('button')` does not put a DOM element in `btn`. It holds a chain object, and the element only exists later, when the command runs.

To get at a value you work inside the chain. You use `.then(($el) => ...)`, an alias with `.as()` and `cy.get('@name')`, or `cy.wrap()`.

```js
cy.get('.title').then(($el) => {
  cy.log(`Title was: ${$el.text()}`);
});
```

Plain JavaScript runs immediately while Cypress commands run later, so a `console.log` in the test body prints before the commands run. If something must run in order with the commands, put it in a `.then()`.
</details>

---

#### Q63: How do you install and set up Cypress, and what do the default folders and `cypress.config.js` do? [Setup]
**Keywords:** `npm install cypress`, `cypress.config.js`, `baseUrl`, `cypress/e2e`, support file
**Hint:** Think about specs, data and shared code.
<details>
<summary>Click to Reveal Answer</summary>

I install it as a dev dependency with `npm install cypress --save-dev`. The first install also downloads the Cypress binary, which is cached globally. Then `npx cypress open` starts the launchpad where I choose E2E testing, and it scaffolds the config and support files.

The default structure is:
- `cypress.config.js` is the central config and uses `defineConfig`.
- `cypress/e2e/` holds the specs. By default files matching `*.cy.js` (and `.ts`, `.jsx`, `.tsx`) are picked up.
- `cypress/fixtures/` holds static data loaded with `cy.fixture()`.
- `cypress/support/e2e.js` runs before every spec, and `commands.js` is where custom commands live.

Inside the `e2e` block of the config I commonly set:
- `baseUrl`, so `cy.visit('/')` resolves against it.
- `specPattern`, `viewportWidth` and `viewportHeight`.
- `defaultCommandTimeout`, which is 4 seconds by default.
- `retries`, with separate `runMode` and `openMode` values.
- `setupNodeEvents`, which runs in Node and is where I register tasks.

Secrets do not go in the config because it is committed. They go in `cypress.env.json` (git-ignored) or `CYPRESS_` environment variables, and are read with `Cypress.env()`.
</details>

---

#### Q64: Which browsers does Cypress support, how do `cypress open` and `cypress run` differ, and how does browser handling compare with Playwright? [Browser Management]
**Keywords:** Chrome/Edge/Firefox/Electron, Installed browsers, Headless, `--browser`, WebKit experimental
**Hint:** Who installs the browsers?
<details>
<summary>Click to Reveal Answer</summary>

Cypress supports Chrome, Chromium, Edge, Firefox and its bundled Electron. WebKit is only experimental.

`cypress open` is the interactive runner. It is headed, it watches files and re-runs on save, and retries default to 0 there. I use it while writing and debugging. `cypress run` is the command-line runner. It is headless by default, uses Electron unless I pass `--browser`, and returns a non-zero exit code on failures, which CI uses to pass or fail the build. Useful flags are `--browser chrome`, `--headed`, `--headless` and `--no-exit`.

```bash
npx cypress run --browser firefox
npx cypress run --headed --no-exit --browser chrome
```

The comparison with Playwright is that Cypress uses the browsers already installed on the machine, plus Electron. Playwright downloads its own patched Chromium, Firefox and WebKit, so versions are consistent everywhere. That means a Cypress run can differ between a laptop and CI. Cypress also runs one browser per command, so cross-browser runs use a CI matrix or a script, whereas Playwright has multiple projects in one run. For Safari-engine coverage I would still use Playwright.

`npx cypress info` lists the browsers Cypress detects.
</details>

---

#### Q65: How do you control the viewport in Cypress, and why does it matter? [Browser Management]
**Keywords:** `viewportWidth`, `cy.viewport`, Presets, Resets per test, Responsive layout
**Hint:** One setting is global, the other is per test.
<details>
<summary>Click to Reveal Answer</summary>

The viewport decides which layout the app renders. At a narrow width a navigation bar may collapse into a hamburger menu, so a locator that works on desktop can fail on mobile.

I set a project default with `viewportWidth` and `viewportHeight` in the config. The built-in default is 1000 x 660. I always set it explicitly, so local runs and CI do not differ. Inside a test I use `cy.viewport`:

```js
cy.viewport(375, 667);
cy.viewport('iphone-x');
cy.viewport('ipad-2', 'landscape');
```

I call it before `cy.visit` so the page renders at that size from the start. `cy.viewport` resets for each test, so I put it in a `beforeEach` if every test needs it. Alternatively I can pass `{ viewportWidth, viewportHeight }` in the test configuration object. Cypress presets only change the size. Playwright's device descriptors also include things like the user agent and touch support.
</details>

---

#### Q66: How is a Cypress spec structured, and what does test isolation mean for the way you write tests? [Writing Tests]
**Keywords:** `describe`/`it`, `beforeEach`, Test isolation, `about:blank`, `cy.visit`
**Hint:** What state does the browser have at the start of each `it`?
<details>
<summary>Click to Reveal Answer</summary>

A spec is a `.cy.js` file with Mocha structure. `describe` or `context` groups tests, `it` is a single test, and hooks are `before`, `beforeEach`, `afterEach` and `after`. I name tests after behaviour and I follow Arrange, Act, Assert.

```js
describe('Cart', () => {
  beforeEach(() => {
    cy.visit('/inventory.html');
  });

  it('adds an item', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');
  });
});
```

Since Cypress 12, test isolation is on by default. Before each test Cypress clears cookies, local storage and session storage, and navigates to `about:blank`. So every test has to visit its own page, and setup that depends on browser state belongs in `beforeEach`, not `before`. To avoid logging in through the UI each time, I use `cy.session()`.

Each test must be able to pass on its own and must not depend on the order of other tests.
</details>

---

#### Q67: What are parent, child and dual commands, and how do you read a value from the page without `await`? [Writing Tests]
**Keywords:** Subject, Parent/child commands, `.then()`, `.as()`, `cy.wrap()`
**Hint:** Each command yields something to the next one.
<details>
<summary>Click to Reveal Answer</summary>

Commands are chained and each one yields a subject to the next. `cy.get('.item').first().find('button').click()` yields elements at each step.

- Parent commands start a chain and need no subject, such as `cy.visit`, `cy.get` and `cy.request`.
- Child commands need a previous subject, such as `.click()`, `.type()` and `.should()`. You cannot call `cy.click()` on its own.
- Dual commands work either way, such as `cy.contains()` and `cy.get('li').contains()`.

Every new `cy.` call starts a new chain.

To work with a value I use `.then()`, which gives me the subject as a jQuery-wrapped element, or `.its()` and `.invoke()` as shortcuts for reading a property or calling a method on the subject. I use `.as()` to name a value and `cy.get('@name')` to read it later, and `cy.wrap()` to put a plain value or element back into the chain.

```js
cy.get('.price').first().invoke('text').then((text) => {
  expect(Number(text.replace('$', ''))).to.be.greaterThan(0);
});
```

I do not use `await` for any of this.
</details>

---

#### Q68: What is the difference between `cy.get()` and `cy.contains()`? [Element Location]
**Keywords:** CSS selector, Visible text, Deepest element, Case-sensitive, Retries
**Hint:** One searches by selector, the other by text.
<details>
<summary>Click to Reveal Answer</summary>

`cy.get(selector)` finds elements by CSS selector, plus a few jQuery extensions like `:contains()`. It retries until the element exists or the timeout passes, 4 seconds by default.

`cy.contains(text)` finds an element by its visible text. Some behaviours worth knowing:
- By default it yields the deepest element that contains the text.
- It is case-sensitive unless I pass `{ matchCase: false }`.
- It matches partial text unless I use an anchored regex.
- With several matches it prefers `input[type=submit]`, `button`, `a` and `label` over other elements.
- Whitespace is normalised before matching.

The most useful form combines a selector and text, which yields the element matching the selector:

```js
cy.contains('[data-test="inventory-item"]', 'Sauce Labs Bike Light')
  .find('button')
  .click();
```

Here I find the card by its text and then work inside it, which is much more stable than `nth-child`. Text locators break when wording changes or the UI is translated, so for actions I prefer test attributes.
</details>

---

#### Q69: What makes a good selector in Cypress, and how do you rank the options? [Element Location]
**Keywords:** `data-*` attributes, Resilient, Brittle, Selector Playground, Testing Library
**Hint:** Which selectors survive a restyle?
<details>
<summary>Click to Reveal Answer</summary>

A good selector survives refactors and restyling, and matches exactly the element I intend. Cypress's best-practices guide recommends dedicated test attributes such as `data-cy`, `data-test` or `data-testid`. They exist only for tests, so styling and copy changes do not affect them. The team just needs to agree on one name.

My rough ranking from best to worst:
1. A `data-*` test attribute.
2. Role or label, which needs the Testing Library plugin.
3. Stable visible text through `cy.contains`.
4. Semantic attributes such as `name` or `aria-label`.
5. A hand-written `id`.
6. Class names, especially generated CSS-in-JS ones.
7. Tag names.
8. Position-based selectors like `div > div:nth-child(3)`.

Cypress has no built-in role or label locator, unlike Playwright's `get_by_role`. The `@testing-library/cypress` plugin adds `findByRole` and `findByLabelText`. For a test id helper, Playwright has `get_by_test_id`, whereas in Cypress I write a small custom command that wraps `cy.get('[data-test="..."]')`.

The Selector Playground in the runner suggests selectors and shows match counts, and I want one match. If the app has no test attributes, I ask developers to add them.
</details>

---

#### Q70: What is the difference between implicit and explicit assertions in Cypress, and why is `.should()` preferred for page state over an `expect` inside `.then()`? [Assertions]
**Keywords:** `.should()`, `expect`, Retry, `.then()` runs once, Chai
**Hint:** Which one keeps trying while the page updates?
<details>
<summary>Click to Reveal Answer</summary>

Cypress bundles Chai, Chai-jQuery and Sinon-Chai. There are three styles:
- Implicit: `.should()` and `.and()` chained on a command.
- BDD explicit: `expect(value).to...`.
- TDD explicit: `assert.equal(...)`.

The safe contrast is that `.should()` retries and `.then()` does not. A `.should()` assertion is retried together with the query before it until it passes or the 4-second timeout ends. An `expect` inside `.then()` runs once, with whatever the value is at that moment.

```js
// Can fail if the text is still "4" when the callback runs
cy.get('.count').then(($el) => {
  expect($el.text()).to.equal('5');
});

// Retries until the text is "5" or the timeout passes
cy.get('.count').should('have.text', '5');
```

For a custom rule, `.should(callback)` re-runs the whole callback until it stops throwing, so it should not contain `cy` commands or side effects. I use `expect` for plain values and computed data.

Some commands also carry built-in assertions. `cy.get` expects the element to exist, `cy.visit` expects a successful response, and actions expect the element to be actionable.
</details>

---

#### Q71: What do `.only`, `.skip` and pending tests do, and in what order do the Mocha hooks run? [Annotations]
**Keywords:** `it.only`, `it.skip`, Pending, `before`/`beforeEach`, Hook order
**Hint:** Think about what happens if `.only` is committed by accident.
<details>
<summary>Click to Reveal Answer</summary>

`it.only` or `describe.only` runs only that test or suite within the spec file. `it.skip` marks a test as skipped, so it shows up as pending in the results and does not run. A test written with no function, like `it('rejects expired coupons')`, is also pending, which makes a handy to-do list. `this.skip()` skips conditionally, and needs a regular `function` because it uses `this`.

`.only` is a development convenience. If it is committed, the rest of the spec silently stops running and CI can still be green. Teams guard against it with the ESLint rule `mocha/no-exclusive-tests`, code review or a CI check.

Hook order for a test: outer `before`, inner `before`, outer `beforeEach`, inner `beforeEach`, the test, inner `afterEach`, outer `afterEach`. The `before` and `after` hooks run once per suite and `beforeEach` and `afterEach` run around every test.

Two cautions. With test isolation, browser state is cleared before each test, so a login done in `before` will not persist. And I do not rely on `after` hooks for critical cleanup, because they may not run if the run is stopped. I reset to a known state at the start instead.
</details>

---

#### Q72: How do you run only some of your Cypress tests? [Test Selection]
**Keywords:** `--spec`, `specPattern`, `.only`, Tags, `grepTags`
**Hint:** There are options at file level and at test level.
<details>
<summary>Click to Reveal Answer</summary>

I think of it in layers:

- Inside a file I use `.only`, `.skip` or `this.skip()`, and the per-test `browser` option for browser-specific tests.
- At file level from the command line I use `--spec` with a quoted glob, and commas separate several patterns:

```bash
npx cypress run --spec "cypress/e2e/smoke/**"
npx cypress run --spec "cypress/e2e/auth/login.cy.js,cypress/e2e/cart/cart.cy.js"
```

- Which files count as specs is set with `specPattern` and `excludeSpecPattern` in the config, and `--config` or `--config-file` can override it per run.
- In `cypress open` I click a spec, or filter by name.
- For selecting by title or tag, the official `@cypress/grep` package adds `grep` for titles and `grepTags` for tags, passed with `--env`. In its expressions, space means OR, `+` means AND and `-` means NOT. I would check the package README for the exact setup of the version in use.

```js
it('logs in', { tags: '@smoke' }, () => { /* ... */ });
```

A sensible strategy is folders for ownership and a small, documented set of tags for purpose, such as `@smoke` on pull requests and everything nightly. I quote globs so the shell does not expand them.
</details>

---

#### Q73: People confuse "fixtures" in Cypress and Playwright. What is the difference? [Fixtures]
**Keywords:** Data file, `cy.fixture()`, Dependency injection, Setup/teardown, Custom commands
**Hint:** One is data, the other is a mechanism.
<details>
<summary>Click to Reveal Answer</summary>

They share a name but not a meaning.

A Cypress fixture is a static data file in `cypress/fixtures`, such as JSON, an image or a CSV. I load it with `cy.fixture('users')`, and JSON is parsed for me. I can use it in `.then()`, as an alias with `.as()`, as `this.users` inside regular `function` callbacks, or as a stub response with `cy.intercept(..., { fixture: 'products.json' })`.

A Playwright fixture is a dependency-injection mechanism. A function builds resources like a logged-in page or a created user, the test receives it by parameter name, and teardown runs after the `yield`.

Cypress has no injection system. The equivalent jobs are done with:
- Custom commands in `commands.js`.
- `cy.session()` for cached login, similar to `storage_state`.
- Hooks, including global ones in `support/e2e.js`.
- `cy.task()` for Node-side work such as seeding a database.

Since after-hooks are not guaranteed, I reset state at the start of a test, not at the end. I also treat fixtures as read-only and keep real secrets out of them, since they are committed.
</details>

---

#### Q74: What are actionability checks in Cypress, and when is `{ force: true }` appropriate? [Element Interaction]
**Keywords:** Actionability, Visible, Not covered, Not disabled, `force: true`
**Hint:** Think of what Cypress verifies before it clicks.
<details>
<summary>Click to Reveal Answer</summary>

Before an action such as `.click()` or `.type()`, Cypress waits, up to the command timeout, for the element to be actionable. It checks that the element exists, is not detached from the DOM, is visible, is not disabled or read-only where relevant, is not animating, is scrolled into view and is not covered by another element. That is why I rarely need `cy.wait(ms)` before an interaction, and the error messages say exactly which check failed, for example "element is being covered by another element".

Actions run once after those checks pass. They are not retried afterwards, unlike queries and the assertions that follow them.

`{ force: true }` skips those checks and fires the event immediately.

```js
cy.get('#hidden-input').click({ force: true });
```

It is reasonable for a legitimately hidden but functional control, such as a visually hidden file or checkbox input, and as a diagnostic: if a test passes with force and fails without it, something is covering or hiding the element. The risk is that a real user cannot click a covered button, so a forced click can hide a real bug. I use it rarely and add a comment explaining why.
</details>

---

### Intermediate (Application)

#### Q75: Every test needs the same login. How would you build reusable setup in Cypress, and keep it fast? [Custom Commands]
**Keywords:** `Cypress.Commands.add`, `cy.session`, Fixture data, `supportFile`, Hooks
**Hint:** Think custom command plus cached session.
<details>
<summary>Click to Reveal Answer</summary>

I would write a custom command in `cypress/support/commands.js` and wrap `cy.session` inside it, so the UI login happens once and is restored afterwards.

```js
Cypress.Commands.add('login', (username = 'standard_user', password = 'secret_sauce') => {
  cy.session([username, password], () => {
    cy.visit('/');
    cy.get('[data-test="username"]').type(username);
    cy.get('[data-test="password"]').type(password, { log: false });
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  });
});

beforeEach(() => {
  cy.login();
  cy.visit('/inventory.html');
});
```

The array is the cache key, so each user gets their own cached session. `cy.session` also accepts a `validate` option to confirm the session is still valid, and `cacheAcrossSpecs: true` to share it across spec files. After `cy.session` the page is cleared, so I visit the page I need. `{ log: false }` keeps the password out of the Command Log.

Credentials come from a fixture or `Cypress.env`, not from test code. I can wrap fixture lookup in a command like `cy.loginAs('editor')`. `commands.js` has to be imported by `support/e2e.js`, and if I see "cy.login is not a function" that import is the first thing I check.

I keep commands small and named by intent. Cypress's own guidance leans towards commands and `cy.session` over heavy Page Objects, though Page Objects work if the team prefers them. A command can also be a child command, with `{ prevSubject: 'element' }`, when it should act on a previous element.
</details>

---

#### Q76: A page has a repeated product list, a web component, and a link that opens in a new tab. How do you locate and handle each in Cypress? [Element Location]
**Keywords:** Scoping with `cy.contains`, `.within`, `includeShadowDom`, `.shadow()`, `target="_blank"`
**Hint:** Find the container first, then work inside it.
<details>
<summary>Click to Reveal Answer</summary>

**Repeated list.** I find the container by its text and then work inside it, rather than by position. `.within()` is useful when I need several commands inside the same container, but it needs a single element as its subject.

```js
cy.contains('[data-test="inventory-item"]', 'Sauce Labs Onesie')
  .find('button')
  .click();
```

**Web component (shadow DOM).** Cypress does not search inside shadow roots by default. I can use `.shadow()` on the host element, or `{ includeShadowDom: true }` on a command, or set `includeShadowDom: true` globally in the config when the app is built on web components.

```js
cy.get('my-widget').shadow().find('button').click();
```

**New tab.** Cypress cannot control a second tab, since the test runs inside the one tab it controls. The workarounds are to remove the `target` attribute so the link opens in the same tab, or to read the `href` and `cy.visit()` it.

```js
cy.get('a.docs').invoke('removeAttr', 'target').click();
```

For iframes there is no built-in "switch to frame". The classic approach reads the iframe's `contentDocument.body` and wraps it with `cy.wrap`, or I use a plugin like `cypress-iframe`. Playwright is easier for all three of these, since it pierces open shadow DOM by default and has frame locators and multi-page support. If a requirement needs real multi-tab flows, that is a point in favour of Playwright.
</details>

---

#### Q77: How would you handle a hover menu, a custom dropdown and a confirm dialog in Cypress, compared with Playwright? [Element Interaction]
**Keywords:** No `.hover()`, `.trigger()`, `.select()` native only, `cy.on('window:confirm')`, Auto-accept
**Hint:** Cypress has no hover command and auto-accepts dialogs.
<details>
<summary>Click to Reveal Answer</summary>

**Hover.** Cypress has no `.hover()`. If the menu listens to JavaScript mouse events, I use `.trigger('mouseover')`. If it opens on CSS `:hover`, dispatched events will not work, so I reveal it with `.invoke('show')`, use `{ force: true }`, or install `cypress-real-events` and use `realHover()` in Chromium-based browsers. Playwright's `hover()` simply works.

**Dropdown.** `.select()` only works on a native `<select>`, and accepts a value, visible text or an index. For a custom dropdown built from divs, I click it open and click the option like any other element.

```js
cy.get('select').select('Price (low to high)');
cy.get('[data-test="country"]').click();
cy.contains('[role="option"]', 'Canada').click();
```

**Dialogs.** Cypress auto-accepts alerts and confirms so tests do not hang, and emits events I can listen to. I register the listener before the click. Returning `false` from a confirm handler means Cancel. There is no prompt event, so I stub `window.prompt`.

```js
cy.on('window:confirm', () => false);
cy.window().then((win) => cy.stub(win, 'prompt').returns('Ada'));
```

In Playwright I register `page.on("dialog", ...)` and have to accept or dismiss, otherwise the action hangs.

Another difference is that Cypress simulates events inside the page, whereas Playwright sends real input through the browser protocol. This is why Cypress needs workarounds for hover and drag and drop.
</details>

---

#### Q78: A test sometimes fails because a total on the page updates after an API call. It uses `.then()` with `expect` and a `cy.wait(5000)`. How do you fix it? [Writing Tests]
**Keywords:** `.should()` retry, `cy.intercept`, Alias, `cy.wait('@alias')`, Fixed sleeps
**Hint:** Wait for what the app is waiting for, not for the clock.
<details>
<summary>Click to Reveal Answer</summary>

There are two problems. The assertion inside `.then()` runs once, so it can read the old value. And `cy.wait(5000)` is a fixed sleep that slows every run and still fails if the app takes slightly longer.

My fix, in order of preference:

1. Assert the final state with a retrying assertion:

```js
cy.get('[data-test="total"]').should('have.text', '$59.98');
```

   The query and assertion retry until the text matches or the 4-second timeout passes. If the app is genuinely slow, I raise the timeout for that one call, such as `cy.get('.slow', { timeout: 10000 })`.

2. Wait on the network call by alias. I register the intercept before the action that triggers the request.

```js
cy.intercept('GET', '**/api/totals*').as('totals');
cy.get('[data-test="apply-coupon"]').click();
cy.wait('@totals').its('response.statusCode').should('eq', 200);
cy.get('[data-test="total"]').should('have.text', '$59.98');
```

3. Use `cy.wait(ms)` only as a last resort and with a comment.

If the backend is unreliable, I can stub the response with `cy.intercept(..., { fixture: 'totals.json' })`, so the UI check is deterministic. Registering the intercept after the click is a common mistake, because the request is already gone by then.
</details>

---

#### Q79: A Cypress test passes in `cypress open` but fails in CI. How do you investigate, and how would you prove a fix for a flaky test? [Debugging]
**Keywords:** `--headed --no-exit`, `retries=0`, Same browser and viewport, `cy.pause`, Command Log
**Hint:** Reproduce the CI conditions first.
<details>
<summary>Click to Reveal Answer</summary>

First I read the full error: the type, the message, the selector and the code frame. Messages usually name the exact cause, for example "covered by another element" or "never found it".

Then I reproduce the CI conditions locally: the same browser, the same viewport and the same spec. I turn retries off, because in `run` mode a test that fails and then passes on retry can look green.

```bash
npx cypress run --browser chrome --headed --no-exit \
  --spec "cypress/e2e/cart/cart.cy.js" \
  --config retries=0,viewportWidth=1280,viewportHeight=720
```

Common CI-only causes are a different viewport collapsing a menu, a different browser version, slower timing, or data differences. `cypress info` shows the detected browsers.

Next I use the debugging actions in `cypress open`:
- The Command Log: hover commands to see the page at that step, and click one to pin it and print details in DevTools.
- `cy.pause()` before the failing command, then step with Next.
- `.debug()` to inspect the subject.
- `debugger` or `console.log`, but inside `.then()`, since in the test body they run before the commands.
- The XHR rows in the Command Log, because a 500 can explain a missing element.

I remember that the DevTools console context should be set to the app iframe, not "top". I change one variable at a time, and I remove `cy.pause()`, `.debug()`, `debugger` and `.only` before committing.

To prove a fix for a flaky test I can run it repeatedly. With `@cypress/grep` that is the `burn` option, and without it I can run the single spec in a loop. I would not use `{ force: true }` or longer sleeps as a fix.
</details>

---

### Advanced (Deep Dive)

#### Q80: Walk me through what happens under the hood when this test runs, and what is wrong with it. [Command Queue]
**Keywords:** Command queue, Synchronous body, Deferred execution, `.then()`, Retry and actionability
**Hint:** Which lines run first: `console.log`, the `expect`, or `cy.get`?
<details>
<summary>Click to Reveal Answer</summary>

```js
it('counts items', () => {
  let count;
  cy.visit('/inventory.html');
  cy.get('.inventory_item').its('length').then((n) => {
    count = n;
  });
  console.log('count is', count);
  expect(count).to.be.greaterThan(0);
});
```

Mocha runs the `it` callback. As it executes, each `cy.*` call only enqueues a command and returns. So the whole body, including `console.log` and the `expect`, runs synchronously first, while `count` is still `undefined`. The `expect(count)` fails straight away, before the page has even been visited.

Only after the callback returns does Cypress run its queue, one command at a time. For `cy.get` it keeps re-querying until the element exists or the timeout passes, and a following `.should` is retried along with it. For an action like `.click()` it first waits for actionability, then fires the events once. Each command yields its subject to the next, and the `.then` callback runs in order, which is the only point where `count` is set.

The fix is to read the variable in a later command, so it runs after the assignment:

```js
cy.get('.inventory_item').its('length').then((n) => {
  expect(n).to.be.greaterThan(0);
});
// or, if I need it later:
cy.then(() => {
  expect(count).to.be.greaterThan(0);
});
```

Better still, if the goal is just to check the count, I skip the variable and assert directly: `cy.get('.inventory_item').should('have.length.greaterThan', 0)`. That retries and never touches a shared variable.
</details>

---


## Day 5 (Friday): Cypress Advanced & Visual Testing

### Beginner (Foundational)

#### Q81: What is time-travel debugging in Cypress, and how do the Command Log and snapshots make it work? [Time-Travel Debugging]
**Keywords:** Command Log, snapshot, hover, DOM and CSS copy, app preview
**Hint:** Think of a DVR for your test run.
<details>
<summary>Click to Reveal Answer</summary>

Time-travel debugging means I can see what the page looked like at any earlier step of a test, without re-running it. In `cypress open`, the left side shows the Command Log, which lists every `cy.*` command, assertion and aliased network request. The right side is the app preview.

It works through snapshots. Cypress saves a copy of the page's DOM and CSS around each command. When I hover over a row in the Command Log, the preview re-renders that saved snapshot, and when I move the mouse away it returns to the final state.

One important point is that a snapshot is a static reconstruction, not the live page. No JavaScript runs in it, so I can look at it but not interact with it. Things the DOM cannot capture, like canvas bitmaps or video frames, are not faithfully rewound.
</details>

---

#### Q82: What is the difference between hovering over and pinning a command in the Command Log, and what are the Before and After snapshots? [Time-Travel Debugging]
**Keywords:** pin, Before/After, DevTools Console, hitbox, action commands
**Hint:** One is temporary, one stays on screen.
<details>
<summary>Click to Reveal Answer</summary>

Hovering shows a command's snapshot only while the mouse is over the row. Clicking the row pins it, so the preview stays frozen and I can study it.

When a command is pinned, Cypress prints details about it to the browser DevTools Console, such as the elements it acted on, the selector and what it yielded. I can also inspect the frozen DOM with the Elements panel.

Action commands like `click`, `type` and `check` get two snapshots, Before and After, so I can flip between them and see exactly what that action changed. Query and assertion commands like `get` and `should` usually get one. For a `click`, Cypress also shows a hitbox, a dot where it clicked. If the dot sits on a cookie banner instead of my button, I have found the bug.
</details>

---

#### Q83: Does Cypress have an equivalent of the Playwright `trace.zip` file? What do you use to debug CI failures instead? [Time-Travel Debugging]
**Keywords:** no trace.zip, Test Replay, Cypress Cloud, screenshots, video
**Hint:** Open-source Cypress time travel is live, not file-based. Mention version and browser requirements.
<details>
<summary>Click to Reveal Answer</summary>

No, open-source Cypress has no `trace.zip`. Its time travel is a live feature of the interactive runner, with snapshots held in browser memory. That works in `cypress open`, but there is nothing to hand off from a headless CI run.

For CI, I have three options. First, the terminal output plus failure screenshots. Second, optional video. Third, Cypress Cloud Test Replay, which needs recording with `cypress run --record`.

Test Replay is version and environment dependent. Per the lesson, it needs Cypress 13 or later, a Chromium-based browser (Chrome, Edge or Electron), and a Cloud plan that includes it. I would verify against the current docs.

Playwright's Trace Viewer is the opposite. It is a portable file you can download from CI and open anywhere for free. So when I triage CI failures without Cloud, Playwright gives me richer evidence.
</details>

---

#### Q84: What are the two kinds of screenshots in Cypress, and when is each one taken? [Screenshots & Video]
**Keywords:** cy.screenshot, screenshotOnRunFailure, cypress run, runner capture, cypress/screenshots
**Hint:** One is requested by your code, the other is automatic.
<details>
<summary>Click to Reveal Answer</summary>

There are manual screenshots and automatic failure screenshots.

Manual ones come from `cy.screenshot()` in my test code. They work in both `cypress open` and `cypress run`. They can capture the full page, the viewport, the runner, or one element when chained off `cy.get()`.

Automatic ones are taken when a test fails, controlled by `screenshotOnRunFailure`, which is on by default. They happen only during `cypress run`, not in `cypress open`. A failure screenshot always uses the `runner` capture, so one image shows the Command Log with the red failed step next to the app state.

Both are saved as PNGs under `cypress/screenshots` by default. I should remember that `cy.screenshot()` only saves an image. It never fails because the page looks wrong.

```js
cy.screenshot('inventory/full-page');
cy.get('[data-test="inventory-item"]').first().screenshot('first-product', { padding: 8 });
```
</details>

---

#### Q85: What are the defaults for Cypress video recording, and when does it record? [Screenshots & Video]
**Keywords:** video, Cypress 13, one MP4 per spec, cypress run only, videoCompression
**Hint:** The default changed between major versions.
<details>
<summary>Click to Reveal Answer</summary>

This is version-dependent. In Cypress 12 and earlier, `video` defaulted to `true`. Since Cypress 13.0 it defaults to `false`, so I must enable it with `video: true`. A pipeline that lost its videos after an upgrade is the classic symptom.

Video is recorded only in `cypress run`, never in `cypress open`. It produces one MP4 per spec file, not per test, saved in `cypress/videos` by default.

For `videoCompression`, the lesson says the documented default has differed across versions, so I should not rely on it. I would set it explicitly, for example `videoCompression: 32`, if I care about file size.

```js
module.exports = defineConfig({
  e2e: { video: true, videoCompression: 32 },
});
```
</details>

---

#### Q86: What does `trashAssetsBeforeRuns` do, and why does it matter for screenshots and visual baselines? [Screenshots & Video]
**Keywords:** trashAssetsBeforeRuns, screenshotsFolder, videosFolder, baselines, deleted before cypress run
**Hint:** Think about where you should store images you want to keep.
<details>
<summary>Click to Reveal Answer</summary>

`trashAssetsBeforeRuns` defaults to `true`. Before each `cypress run`, Cypress deletes everything in the screenshots and videos folders. That keeps old evidence from being confused with new evidence.

The danger is storing anything permanent in those folders. If I commit visual baselines into `cypress/screenshots`, they could be erased at the start of the next run.

So I keep baselines in a separate folder, or I set `trashAssetsBeforeRuns: false` deliberately. In the visual testing setup, `screenshotsFolder` points to an `actual` folder and baselines live in a sibling `base` folder, so trashing the actual images is harmless.
</details>

---

#### Q87: Name the four places a log can go in Cypress, and say which ones appear in the CI terminal. [Logging]
**Keywords:** Command Log, browser console, terminal, cy.task, files
**Hint:** Specs run in the browser, but CI shows the Node process.
<details>
<summary>Click to Reveal Answer</summary>

The four destinations are:

1. The Command Log, written with `cy.log()` or `Cypress.log()`. It is UI only, though it shows up in runner screenshots and videos.
2. The browser DevTools Console, written with `console.log()`, `console.table()` or pinned-row `consoleProps`.
3. The terminal or CI log, which is the Node process. I reach it with `cy.task('log', ...)`.
4. Files on disk, through `cy.task` using Node's `fs`, or `cy.writeFile()`.

Only the Node terminal shows in the `cypress run` output. A `console.log` in a spec goes to the browser console, which nobody sees in headless CI. That is why a teammate's `console.log` produces an empty Jenkins log.
</details>

---

#### Q88: What does this test print, in what order, and why? [Logging]
```js
it('order', () => {
  console.log('A');
  cy.log('B');
  console.log('C');
});
```
**Keywords:** command queue, asynchronous, synchronous, .then(), queue-building
**Hint:** Cypress commands are queued, plain JavaScript is not.
<details>
<summary>Click to Reveal Answer</summary>

The browser console shows `A` and `C` almost instantly, and `B` appears in the Command Log afterwards. So the observable order is A, C, then B.

Cypress runs the test function top to bottom synchronously. Plain JavaScript such as `console.log` executes right away. Every `cy.*` call only adds a command to a queue. After the function finishes, Cypress runs the queue, and only then does `cy.log('B')` execute.

The fix is to put logic that depends on earlier commands inside the queue, usually with `.then()`:

```js
cy.get('[data-test="shopping-cart-badge"]').then(($badge) => {
  console.log('Badge text:', $badge.text());
  cy.log(`Badge: ${$badge.text()}`);
});
```

The same trap explains why mixing direct jQuery queries like `Cypress.$(...)` with queued commands gives stale results.
</details>

---

#### Q89: How does `cy.task()` work, and what rules must a task handler follow? [Logging]
**Keywords:** setupNodeEvents, on('task'), return null, one serialisable argument, Node process
**Hint:** There is a mandatory return value, and a limit on arguments.
<details>
<summary>Click to Reveal Answer</summary>

`cy.task()` is the bridge from the browser-side spec to the Node.js process that launched Cypress. I register handlers in `setupNodeEvents` with `on('task', {...})`. Each key is an event name. The handler runs in Node, where it can use `console.log`, `fs` or a database.

The rules are:

- A handler must return something other than `undefined`. If it has nothing to return, it returns `null`. Returning `undefined` fails the command, which catches typos in event names.
- A task takes one argument, and it must be serialisable. To pass several values, I pass an object.
- Tasks have a timeout (`taskTimeout`, 60 seconds by default), so they should not start long-running processes.

```js
on('task', {
  log({ level = 'info', message }) {
    console.log(`[${level.toUpperCase()}] ${message}`);
    return null;
  },
});
// in a spec
cy.task('log', { level: 'warn', message: 'Hello' });
```
</details>

---

#### Q90: What is "record and playback", and what are the typical weaknesses of recorded tests? [Recording User Actions]
**Keywords:** recorder, generated selectors, no assertions, no structure, starting point
**Hint:** The recorder knows what you did, not what you expected.
<details>
<summary>Click to Reveal Answer</summary>

Record and playback means I perform actions in a real browser, and a tool writes the matching test commands. Under the hood it listens for events, computes a selector for each element and writes lines like `cy.get('[data-test="login-button"]').click()`.

It is fast for first drafts, helps beginners and is good for discovering selectors or reproducing a bug.

The weaknesses are:

- No assertions, because the tool knows what I did but not what I expected. A test with no assertions only proves nothing crashed.
- Selectors can be fragile, such as `nth-child` or long CSS paths.
- No structure: no reuse, no page objects, no separate test data.
- Hidden timing issues, and conditional behaviour like pop-ups is not captured.
- Gaps with iframes, Shadow DOM, multiple origins and drag-and-drop.

So a recording is a draft, not a finished test.
</details>

---

#### Q91: What is Cypress Studio, how do you enable it, and what are its limitations? [Recording User Actions]
**Keywords:** experimentalStudio, Beta, right-click assertions, click/type/check/select, no iframes
**Hint:** Enabling it depends on your Cypress version.
<details>
<summary>Click to Reveal Answer</summary>

Cypress Studio records my interactions inside the Test Runner and writes the commands into my spec file. I can also right-click an element to add an assertion.

How to enable it is version-dependent, per the lesson. On Cypress 10.7 through 14.x, I set `experimentalStudio: true` in the config. According to the lesson, on 15.4.0 and later the flag was removed and Studio is available without it, and the docs still label it Beta. I would check `npx cypress --version` and read the docs for my version.

Limitations in the docs:

- E2E only, and it needs sourcemaps and internet access.
- No recording across multiple origins, and no iframes or Shadow DOM.
- It records only `click`, `type`, `check`, `uncheck` and `select`. Hover, drag-and-drop and file upload I add by hand.
- It appends commands to a test and does not reorganise code.

```js
e2e: { experimentalStudio: true } // Cypress 10.7 - 14.x only
```
</details>

---

#### Q92: Why should you not commit a generated test as it is, and what does a review checklist for generated code cover? [Editing Generated Code]
**Keywords:** assertions, selectors, redundant steps, hard-coded data, test names
**Hint:** Run it first, then go through names, noise, selectors and assertions.
<details>
<summary>Click to Reveal Answer</summary>

A generated test is a draft. It captures actions, not intent, and it is costly to maintain.

My checklist would be:

1. Run it first, so I have a safety net before refactoring.
2. Names: describe business behaviour, not "tests checkout".
3. Noise: remove redundant `.click()` before `.type()`, duplicate queries, viewport calls and absolute URLs (use `baseUrl`).
4. Selectors: replace structural ones with `data-test` style attributes.
5. Assertions: add them, since recordings usually have none.
6. Synchronisation: replace `cy.wait(ms)` with conditions.
7. Data: move hard-coded values to fixtures and secrets to env.
8. Duplication: extract login into a custom command.
9. Structure: use hooks and one behaviour per test.
10. Stability: run it repeatedly, headless.

I would also keep refactoring commits separate from commits that add assertions.
</details>

---

#### Q93: How do you replace a fragile recorded selector like `.inventory_item:nth-child(1) .btn_inventory`? [Editing Generated Code]
**Keywords:** data-test, cy.contains, find, within, selector hierarchy
**Hint:** Think about what survives a redesign or a reordering.
<details>
<summary>Click to Reveal Answer</summary>

Structural and positional selectors are the worst, because they break when layout or order changes. My preference order is:

1. A dedicated test attribute such as `data-test` or `data-cy`, a deliberate contract with developers.
2. Semantic hooks like `cy.contains('button', 'Checkout')` or `aria-label`.
3. A stable `id`.
4. Classes, which are weak.
5. Position or structure, which is the worst.

To target a specific product without `nth-child`, I find the card by its name and search inside it:

```js
cy.contains('[data-test="inventory-item"]', 'Sauce Labs Backpack')
  .find('button')
  .click();
```

This works even if the product order changes. If the app has no test attributes, I ask developers to add them. I can use the Selector Playground to check that the selector matches exactly one element, and I configure `Cypress.SelectorPlayground.defaults({ selectorPriority: [...] })` so recorders prefer stable attributes.
</details>

---

#### Q94: What is visual testing, what bugs does it catch that functional assertions miss, and what are baseline, actual and diff? [Visual Testing]
**Keywords:** baseline, actual, diff, pixel comparison, cy.screenshot, plugin
**Hint:** Cypress captures images but does not compare them on its own.
<details>
<summary>Click to Reveal Answer</summary>

Visual testing compares what the page looks like now against an approved picture of how it should look. It catches presentation bugs where every functional assertion still passes: white text on a white button, a font that failed to load, overlapping elements, or an `<img>` that exists but shows nothing.

The vocabulary:

- Baseline: the approved reference screenshot, normally committed to version control.
- Actual: the screenshot from the current run.
- Diff: an image highlighting where actual differs from baseline.

Cypress core only provides `cy.screenshot()` for capture. Comparison comes from plugins such as `cypress-visual-regression` (`cy.compareSnapshot()`) or from services like Percy and Applitools.

It complements functional tests and never replaces them. A visual test should not be my only check of a business rule.
</details>

---

### Intermediate (Application)

#### Q95: Your visual tests pass locally but fail in CI with small mismatches on every test. What is the likely cause and how do you fix it? [Visual Testing]
**Keywords:** environment, anti-aliasing, same Docker image, baselines, viewport
**Hint:** Fonts and rendering differ between operating systems.
<details>
<summary>Click to Reveal Answer</summary>

The most likely cause is environment differences. Different operating systems, browser versions, fonts and anti-aliasing produce slightly different pixels. A typical story is baselines created on macOS or Windows and compared on Linux in CI, which makes every test fail by a small amount.

My fix is to remove the cause, not to loosen thresholds:

- Generate and compare baselines in the same environment, ideally the same pinned Docker image in CI. Baselines should come from a deliberate "update baselines" job there, not from laptops.
- Use the same browser and version, and keep separate baselines per browser if I test several.
- Set the viewport explicitly.

Then I check the other flakiness causes: wait for fonts, images and network, disable animations and the caret, and stub or freeze dynamic data. Thresholds are the last tool, not the first.
</details>

---

#### Q96: Your visual test fails whenever a timestamp or cart counter on the page changes. How would you handle the dynamic content, and what are the trade-offs of the threshold? [Visual Testing]
**Keywords:** blackout, cy.intercept stub, cy.clock, mask minimum area, strictness vs flakiness
**Hint:** Rank the options from best to last resort, and remember the baseline must match.
<details>
<summary>Click to Reveal Answer</summary>

I would rank the options from best to last resort:

1. Stub the data with `cy.intercept` so the page always shows the same content.
2. Freeze time with `cy.clock(fixedTimestamp, ['Date'])`, called before `cy.visit`.
3. Hide or replace the element with injected CSS. `visibility: hidden` keeps the layout space, while `display: none` can shift other elements.
4. Mask it with `blackout`.
5. Snapshot a narrower element that excludes it.

```js
cy.compareSnapshot('inventory-with-item', {
  errorThreshold: 0.1,
  blackout: ['[data-test="shopping-cart-badge"]'],
});
```

Two cautions. The same mask must be applied when the baseline is generated, otherwise the baseline has no black box and the comparison differs. And I mask the minimum area, because large masks become blind spots where real bugs hide.

On thresholds, the trade-off is strictness versus flakiness. Zero tolerance fails on invisible rendering noise. A generous tolerance can hide a real defect, especially on large images where a small icon is a tiny share of the pixels. That is why element-level snapshots help: a defect is a bigger share of a smaller image. Note that the unit of `errorThreshold` depends on the plugin version (a percentage in some docs, a fraction in other versions), so I check the README for the installed version rather than trusting a number from a tutorial.
</details>

---

#### Q97: You inherit a recorded checkout test that logs in through the UI in every test. How would you refactor it to be fast and maintainable? [Editing Generated Code]
**Keywords:** custom command, cy.session, validate, fixtures, cy.visit after session
**Hint:** Think about duplication, secrets and caching.
<details>
<summary>Click to Reveal Answer</summary>

I would extract the login into a custom command that uses `cy.session()`, so the UI login runs once and the cookies and storage are restored in later tests.

```js
Cypress.Commands.add('login', (username = 'standard_user') => {
  cy.session(['sauce-login', username], () => {
    cy.visit('/');
    cy.get('[data-test="username"]').type(username);
    cy.get('[data-test="password"]').type(Cypress.env('SAUCE_PASSWORD'), { log: false });
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  }, { validate() { cy.getCookie('session-username').should('exist'); } });
});

beforeEach(() => { cy.login(); cy.visit('/inventory.html'); });
```

Key points:

- Give each user a distinct session id.
- Provide `validate` so stale sessions are recreated. The session row shows created, restored or recreated.
- Call `cy.visit()` afterwards, because the page is blank after `cy.session`, with test isolation on.
- Move secrets to `cypress.env.json` or CI secrets, and test data to fixtures.
- Keep assertions visible in the test, not hidden in the command.

I would do this as a refactor commit with the test passing, and add assertions in a separate commit.
</details>

---

#### Q98: When would you choose Cypress Studio versus the Chrome DevTools Recorder with export, and what does Cypress Cloud's "record" have to do with either? [Recording User Actions]
**Keywords:** Studio, Chrome Recorder, @cypress/chrome-recorder, cross-origin, --record
**Hint:** One lives inside the runner, the other is independent of Cypress.
<details>
<summary>Click to Reveal Answer</summary>

I use Studio when I am already inside a Cypress spec and want to add a few steps or assertions. It writes directly into the spec, and I can add assertions with right-click. It is limited to a few commands and has no iframe, Shadow DOM or cross-origin support.

I use the Chrome DevTools Recorder for awkward flows that Studio cannot record, or when I want a shareable JSON recording usable by several tools. I export JSON and convert it with the `@cypress/chrome-recorder` CLI, or use the Cypress Chrome Recorder extension. It adds no assertions, and I should inspect the selectors it generated. Setting its "Selector attribute" to `data-test` helps.

```bash
npx @cypress/chrome-recorder ./recordings/saucedemo-login.json
```

Cypress Cloud "record" is a different thing. `cypress run --record` records a test run (results, screenshots, video, and Test Replay data where supported) to a dashboard. It does not record user actions or write test code. Its only link to recording user actions is Studio's AI assertion suggestions in recent versions (the lesson says 15.11.0 or later with a Cloud account), which is version-dependent.
</details>

---

#### Q99: A test passes in `cypress open` but fails in `cypress run` on CI, and there is no Cypress Cloud. What evidence do you collect and how do you investigate? [Screenshots & Video]
**Keywords:** failure screenshot, video, artifacts, viewport, retries
**Hint:** Interactive time travel is not available in headless runs.
<details>
<summary>Click to Reveal Answer</summary>

Without Cloud, interactive time travel is not available in headless runs, so I rely on artifacts:

1. The terminal error message and the failing spec.
2. The automatic failure screenshot, which uses the runner capture and so shows the Command Log and the page together.
3. Video, if enabled. It is off by default since Cypress 13, so I might turn it on only for that spec with `--config video=true --spec ...`.

Those files must be uploaded as CI artifacts, for example with `actions/upload-artifact` and `if: failure()`, because the machine disappears afterwards. I could also add `cy.log` headings so the screenshot shows which business step failed.

A common cause is a viewport difference. The default `cypress run` viewport is smaller than a typical local window, so the screenshot might show the mobile menu. The fix is to set `viewportWidth` and `viewportHeight` in the config. Another cause is a timing-dependent pop-up that video would reveal. I would fix it with a condition or an intercept, not `cy.wait`, and I would not use retries to hide it.
</details>

---

### Advanced (Deep Dive)

#### Q100: Explain what happens under the hood when a Cypress test runs, and use it to explain both why `console.log` prints "too early" and how time-travel snapshots can show earlier page states. [Time-Travel Debugging]
**Keywords:** command queue, synchronous queue building, DOM snapshot, Cypress.log, retry
**Hint:** Separate the "queue-building" phase from the "execution" phase.
<details>
<summary>Click to Reveal Answer</summary>

There are two phases. In the first, Cypress calls my test function synchronously. Plain JavaScript runs immediately, but each `cy.*` call only adds a command to a queue. In the second phase, Cypress executes the queued commands one at a time, waiting for each to finish. Query commands and their assertions retry until they pass or the `defaultCommandTimeout` (4000 ms by default) expires, and the Command Log shows the final outcome of that retry loop as one row.

That explains the logging behaviour. A `console.log` or `Cypress.$()` call outside a callback runs in phase one, before any command has executed. So it can print `0` for an element count on a page that has not loaded yet. Anything that depends on earlier commands must go inside `.then()`, which runs in the queue at the right time.

During phase two, Cypress saves a snapshot of the DOM and CSS around each command, with Before and After for actions. These are in-memory copies, controlled by `numTestsKeptInMemory`, which defaults to 50 in `open` mode and 0 in `run` mode. Hovering or pinning a row re-renders that copy in the preview. It is static, so JavaScript state, canvas content and animation frames are not preserved.

Custom commands can take part through `Cypress.log({ autoEnd: false, consoleProps })` with `log.snapshot('before')` and `log.snapshot('after').end()`. They need `autoEnd: false` because the work is asynchronous, and the row must be ended by hand.
</details>

---


