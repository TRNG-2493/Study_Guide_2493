# Weekly Knowledge Check: [Week5-Advanced-Web-Automation]

## Day 1 (Monday): Playwright Web Interactions

**Covers:** Alerts, dialogs and pop-ups | Radio buttons and checkboxes | Dropdowns and multi-selects | Keyboard and mouse actions | Auto-suggestions

**How to use this quiz:** Answer each question first, then open the *Click for Solution* block to check your answer and read the reasoning. All code uses **Python**, the Playwright **sync API**, and a blank `page` (a fresh Playwright `Page`). Do not skip the explanations: the *why* matters more than the score.

---

## Part 1: Multiple Choice

### 1. A page's Delete button opens a styled overlay (`<div role="dialog">` with a dimmed background and **Cancel** / **Confirm** buttons). Which technique should your test use?
- [ ] A) `page.once("dialog", lambda d: d.accept())`
- [ ] B) `http_credentials` when creating the browser context
- [ ] C) Locators and `expect`, for example `page.get_by_role("dialog").get_by_role("button", name="Confirm").click()`
- [ ] D) `permissions=["geolocation"]` when creating the browser context

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Locators and `expect`, for example `page.get_by_role("dialog").get_by_role("button", name="Confirm").click()`

**Explanation:** A modal drawn with HTML and CSS is part of the DOM (you can inspect it in DevTools), so you handle it like any other element with locators and `expect`.
- **Why others are wrong:**
  - A) The `dialog` event only fires for native browser dialogs (`alert`, `confirm`, `prompt`, `beforeunload`). An HTML overlay is ordinary DOM, so this handler would never run.
  - B) That option answers HTTP Basic Auth login boxes, which have nothing to do with in-page overlays.
  - D) Permissions pre-answer browser prompts such as location or notifications, not modals drawn by the page.

</details>

---

### 2. The checkbox `#newsletter` might already be ticked (the site pre-selects it for some users). Which call guarantees it ends up ticked whatever its starting state?
- [ ] A) `page.locator("#newsletter").check()`
- [ ] B) `page.locator("#newsletter").click()`
- [ ] C) `page.locator("#newsletter").is_checked()`
- [ ] D) `page.locator("#newsletter").set_checked(False)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `page.locator("#newsletter").check()`

**Explanation:** `check()` means "ensure checked": it does nothing if the box is already checked, otherwise it clicks and then verifies the new state.
- **Why others are wrong:**
  - B) `click()` toggles. On a pre-ticked box it would untick it.
  - C) `is_checked()` only reads the current state and returns a boolean; it changes nothing.
  - D) `set_checked(False)` ensures the box is unchecked, which is the opposite of what is wanted.

</details>

---

### 3. A UI library renders a country picker as `<div role="combobox">` plus a list of `<li role="option">` elements. What is the right way to choose "Canada"?
- [ ] A) `page.get_by_role("combobox").select_option(label="Canada")`
- [ ] B) `page.get_by_role("combobox").check()`
- [ ] C) `page.keyboard.insert_text("Canada")` straight away
- [ ] D) Click the combobox to open it, then click `page.get_by_role("option", name="Canada")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Click the combobox to open it, then click `page.get_by_role("option", name="Canada")`.

**Explanation:** Custom dropdowns are ordinary elements, so you automate them the way a user does: open, then click the option.
- **Why others are wrong:**
  - A) `select_option` only works on a native `<select>`. Here it raises "Element is not a <select> element".
  - B) `check()` is for checkboxes, radios and switches, not dropdowns.
  - C) Inserting text does not open a list or choose an option. A custom dropdown needs the same open-then-click steps a user performs.

</details>

---

### 4. Which call inserts text into the focused field in one go, **without** generating `keydown`/`keyup` events (like a paste)?
- [ ] A) `locator.press_sequentially("hello")`
- [ ] B) `page.keyboard.insert_text("hello")`
- [ ] C) `page.keyboard.type("hello")`
- [ ] D) `locator.press("h")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `page.keyboard.insert_text("hello")`

**Explanation:** `insert_text` only fires an `input` event, like pasting.
- **Why others are wrong:**
  - A) It presses each key in turn, firing the full key-event sequence for every character.
  - C) It types character by character with key events; the only difference from `press_sequentially` is that it uses whatever has focus.
  - D) It presses a single key with key events; it is not a paste-like insertion.

</details>

---

### 5. A search box shows suggestions only on `keyup`. Why does `locator.fill("Py")` often produce no suggestions?
- [ ] A) `fill` types too slowly, so the widget gives up waiting.
- [ ] B) `fill` appends to the field instead of replacing it, so the term is wrong.
- [ ] C) `fill` only works on password fields.
- [ ] D) `fill` sets the whole value at once and fires a single `input` event, but no `keydown`/`keyup` events, so the widget's listener never runs.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `fill` sets the whole value at once and fires a single `input` event, but no `keydown`/`keyup` events, so the widget's listener never runs.

**Explanation:** For typeahead widgets, use `press_sequentially`, which generates the full key-event sequence for every character.
- **Why others are wrong:**
  - A) `fill` is instantaneous, the opposite of slow.
  - B) `fill` clears first and replaces the content. It is `press_sequentially` that appends.
  - C) It works on any text field. The problem is the missing key events.

</details>

---

### 6. A test clicks a button whose JavaScript calls `confirm("Delete this?")`. No `dialog` listener has been registered. What happens?
- [ ] A) Playwright automatically accepts the dialog, so `confirm()` returns `true`.
- [ ] B) The page freezes and the test hangs until the timeout.
- [ ] C) Playwright automatically dismisses the dialog (presses Cancel), so `confirm()` returns `false` and the test carries on.
- [ ] D) Playwright raises an error immediately because the dialog is unhandled.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Playwright automatically dismisses the dialog (presses Cancel), so `confirm()` returns `false` and the test carries on.

**Explanation:** With no listener Playwright auto-dismisses every dialog so tests do not hang by accident, but the Cancel answer means the delete never happens.
- **Why others are wrong:**
  - A) The default is dismiss, not accept. To confirm a deletion you must call `accept()` yourself.
  - B) Hanging happens when a listener exists but fails to answer. With no listener, Playwright answers for you.
  - D) An unhandled dialog is not an error; it is silently dismissed, which is why "Delete" appears to do nothing.

</details>

---

### 7. A form has labels **Phone** and **Phone (work)**, and `page.get_by_label("Phone").fill("555")` raises a strict mode violation. Which locator targets only the first field?
- [ ] A) `page.get_by_label("Phone", exact=True)`
- [ ] B) `page.get_by_label("phone")`
- [ ] C) `page.get_by_label("^Phone$")`
- [ ] D) `page.get_by_label("Phone*")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `page.get_by_label("Phone", exact=True)`

**Explanation:** `exact=True` turns off substring matching, so only the label whose text is exactly "Phone" matches.
- **Why others are wrong:**
  - B) Label matching is a case-insensitive substring match by default, so lowercase still matches both fields.
  - C) Plain strings are not regular expressions. This searches for the literal text `^Phone$` and finds nothing (use `re.compile` for a regex).
  - D) The `*` is not a wildcard in these string locators. It is literal text, so nothing matches.

</details>

---

### 8. A `<select multiple>` currently has **Python** (`py`) and **SQL** (`sql`) selected. You call `select_option(["git"])`. What is selected afterwards?
- [ ] A) Python, SQL and Git, because the new value is added.
- [ ] B) Python and SQL, because Git is ignored when a selection already exists.
- [ ] C) Nothing changes and an error is raised.
- [ ] D) Only Git, because `select_option` replaces the whole selection.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Only Git, because `select_option` replaces the whole selection.

**Explanation:** To keep existing choices you must read the current selection first and pass the combined list.
- **Why others are wrong:**
  - A) `select_option` does not add. To add, you must pass the union of the old and new values.
  - B) Existing selections do not block the call; they are simply replaced.
  - C) No error occurs; the call succeeds and the selection is replaced.

</details>

---

### 9. You need a select-all shortcut that works on Windows, Linux and macOS. Which call is correct?
- [ ] A) `page.keyboard.press("Control+A")`
- [ ] B) `page.keyboard.press("ControlOrMeta+A")`
- [ ] C) `page.keyboard.press("Ctrl+A")`
- [ ] D) `page.keyboard.press("Cmd+A")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `page.keyboard.press("ControlOrMeta+A")`

**Explanation:** `ControlOrMeta` means Control on Windows/Linux and Meta (Command) on macOS, which makes cross-platform shortcuts possible.
- **Why others are wrong:**
  - A) It works on Windows and Linux, but macOS uses Command+A for select-all, so it fails there.
  - C) `Ctrl` is not a valid key name. Playwright raises "Unknown key"; the correct name is `Control`.
  - D) `Cmd` is not a valid key name either; the Command key is called `Meta`.

</details>

---

### 10. A debounced, server-driven suggestion list changes as you type. What is the most reliable thing to wait for before clicking an option?
- [ ] A) `time.sleep(3)`
- [ ] B) `expect(listbox).to_be_visible()` and nothing else
- [ ] C) `expect(options).to_have_text([...])` (or `to_contain_text(...)`), so you wait for the right content.
- [ ] D) A larger `delay` in `press_sequentially`, with no assertion

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `expect(options).to_have_text([...])` (or `to_contain_text(...)`), so you wait for the right content.

**Explanation:** The core rule: wait for the condition you care about, not for a number of seconds.
- **Why others are wrong:**
  - A) A fixed sleep is either too short (flaky) or too long (slow).
  - B) The list may still be visible from an earlier keystroke, so you could click an option from a stale list.
  - D) `delay` controls typing speed. It is not a wait for the list to render.

</details>

---

### 11. You register `page.on("dialog", handler)`, and `handler` calls `dialog.accept()` only `if dialog.type == "confirm"`. The page then calls `alert("Saved")`. What happens?
- [ ] A) Playwright still auto-dismisses the alert because the handler did not answer it.
- [ ] B) Playwright auto-accepts the alert because alerts only have an OK button.
- [ ] C) The handler raises an exception, and that closes the dialog.
- [ ] D) Nobody answers the alert, so the page stays frozen and the action hangs until it times out.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Nobody answers the alert, so the page stays frozen and the action hangs until it times out.

**Explanation:** A listener makes your code responsible for calling `accept()` or `dismiss()` on every code path. Add an `else: dialog.dismiss()` to be safe.
- **Why others are wrong:**
  - A) Once at least one listener exists, Playwright stops auto-dismissing. Your listener is responsible for every dialog.
  - B) There is no such special case; any dialog nobody answers stays open.
  - C) The `if` simply does not match, so no exception occurs and nothing closes the dialog.

</details>

---

### 12. Why is `expect(box).to_be_checked()` preferred over `assert box.is_checked()` in a test?
- [ ] A) `expect` retries until the box is checked or the timeout expires, while `is_checked()` reads the state once, immediately.
- [ ] B) `is_checked()` works only on radio buttons, not on checkboxes.
- [ ] C) `expect(...).to_be_checked()` clicks the box if it is not checked yet.
- [ ] D) `is_checked()` raises an exception when the box is unchecked.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `expect` retries until the box is checked or the timeout expires, while `is_checked()` reads the state once, immediately.

**Explanation:** If the page updates the state a moment later, `assert box.is_checked()` fails randomly, whereas `expect` waits. Keep `is_checked()` for control-flow logic.
- **Why others are wrong:**
  - B) It works on both. The problem is that it does not wait.
  - C) Assertions never change the page; they only observe it. Use `check()` to act.
  - D) It simply returns `False`; no exception is raised.

</details>

---

### 13. The HTML is `<option value="ca">Canada</option>`. Which call selects it by the text the user sees?
- [ ] A) `select_option(label="ca")`
- [ ] B) `select_option(index="Canada")`
- [ ] C) `select_option(label="Canada")`
- [ ] D) `select_option(text="Canada")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `select_option(label="Canada")`

**Explanation:** `label=` mirrors what the user reads, while `value=` (here `ca`) is what the back-end receives.
- **Why others are wrong:**
  - A) `label=` matches the visible text, which is "Canada", so this waits for an option labelled "ca" and times out.
  - B) `index` must be an integer (a zero-based position); a string is rejected.
  - D) There is no `text=` keyword. The valid ones are `value`, `label` and `index`, so Python raises a TypeError.

</details>

---

### 14. `page.keyboard.press("Enter")` seems to have no effect in your test. What is the most likely cause?
- [ ] A) `Enter` is not a valid key name, so it is ignored.
- [ ] B) Nothing relevant has focus: `page.keyboard` sends the key to whatever is currently focused.
- [ ] C) `page.keyboard.press` only works for letters and digits.
- [ ] D) Key presses need a `delay=` argument or they are dropped.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Nothing relevant has focus: `page.keyboard` sends the key to whatever is currently focused.

**Explanation:** Device APIs have no element awareness. Use `locator.press()` (which focuses the element first) or call `locator.focus()` before `page.keyboard.press()`.
- **Why others are wrong:**
  - A) `Enter` is valid. An invalid key name raises an "Unknown key" error rather than being silently ignored.
  - C) It handles named keys such as Enter, Tab, Escape and the arrow keys.
  - D) `delay` is an optional pause between keystrokes; it is not required.

</details>

---

### 15. The suggestion list contains **Java** and **JavaScript**. Which locator clicks only **Java**?
- [ ] A) `page.get_by_role("option", name="Java").click()`
- [ ] B) `page.get_by_role("option", name=re.compile("Java")).click()`
- [ ] C) `page.get_by_role("option").last.click()`
- [ ] D) `page.get_by_role("option", name="Java", exact=True).click()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `page.get_by_role("option", name="Java", exact=True).click()`

**Explanation:** `exact=True` (or an anchored regex) prevents "Java" from also matching "JavaScript".
- **Why others are wrong:**
  - A) Substring matching resolves to both options, so strict mode raises an error.
  - B) An unanchored regex also matches both options. It would need anchors such as `r"^Java$"`.
  - C) `last` is position-based and would pick JavaScript here, and it breaks whenever the order changes.

</details>

---

### 16. Which statement correctly describes `page.once("dialog", handler)`?
- [ ] A) `handler` stays registered for every dialog until the page closes.
- [ ] B) It pauses the test until a dialog appears, then continues.
- [ ] C) `handler` runs for only the next dialog and is then removed, so later dialogs go back to being auto-dismissed.
- [ ] D) It is only valid for `alert` dialogs; `confirm` and `prompt` need `page.on`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `handler` runs for only the next dialog and is then removed, so later dialogs go back to being auto-dismissed.

**Explanation:** Use `once` when you expect exactly one dialog at a step; it cannot leak into later steps.
- **Why others are wrong:**
  - A) That describes `page.on`. `once` removes itself after a single call.
  - B) `once` does not block. It registers a listener and returns immediately, which is why it must come before the click that opens the dialog.
  - D) `once` works for every dialog type. The only difference from `on` is how long the handler stays attached.

</details>

---

### 17. A shipping form has radios Standard, Express and Overnight, with **Standard** selected. What does `page.get_by_role("radio", name="Standard").uncheck()` do?
- [ ] A) It raises an error: a radio can only be unchecked by selecting another radio in the same group.
- [ ] B) It unselects Standard, leaving the group with no selection.
- [ ] C) It silently does nothing and the test continues.
- [ ] D) It automatically selects the next radio (Express).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It raises an error: a radio can only be unchecked by selecting another radio in the same group.

**Explanation:** Only checkboxes support `uncheck()`. For radios you change the state by checking a different option in the group.
- **Why others are wrong:**
  - B) A user cannot untick a radio by clicking it, and Playwright reproduces user behaviour, so it refuses.
  - C) Playwright raises an error instead of silently ignoring the request.
  - D) Playwright never guesses another choice. You must `check()` the radio you want.

</details>

---

### 18. After choosing a country, the **State** dropdown reloads from the server and briefly shows "Loading...". What is the best way to wait before choosing a state?
- [ ] A) `time.sleep(2)`
- [ ] B) Call `page.locator("#state option").all_inner_texts()` and use the result right away.
- [ ] C) `expect(page.locator("#state")).to_be_visible()`
- [ ] D) `expect(page.locator("#state option")).to_have_text([...the expected states...])`, which retries until the real list appears.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `expect(page.locator("#state option")).to_have_text([...the expected states...])`, which retries until the real list appears.

**Explanation:** Wait for the condition you care about (the expected options), not for a fixed number of seconds.
- **Why others are wrong:**
  - A) A fixed sleep is slow when the server is fast and flaky when it is slow. It waits for time, not for the condition.
  - B) `all_inner_texts()` does not wait, so it may return the "Loading..." list.
  - C) The dropdown is visible all along, so this passes immediately and proves nothing about the options having loaded.

</details>

---

### 19. A custom slider only reacts to a real drag. Which sequence best simulates dragging its handle to a target position?
- [ ] A) `page.mouse.click(x, y)` at the target position
- [ ] B) `handle.hover()`, `page.mouse.down()`, `page.mouse.move(x, y, steps=15)`, `page.mouse.up()`
- [ ] C) `page.mouse.wheel(x, y)`
- [ ] D) `handle.hover()` followed by `page.mouse.up()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `handle.hover()`, `page.mouse.down()`, `page.mouse.move(x, y, steps=15)`, `page.mouse.up()`

**Explanation:** A manual drag is press, move (in several `steps`, so intermediate `mousemove` events fire) and release.
- **Why others are wrong:**
  - A) A click presses and releases in one spot. It never presses on the handle and drags.
  - C) `wheel` scrolls by delta amounts; it does not press a button or move the pointer to a position.
  - D) The button is never pressed, so there is nothing to drag and nothing to release.

</details>

---

### 20. An accessible suggestion list marks the keyboard-highlighted option with `aria-selected="true"`. Which assertion checks that **PyPy** is the highlighted option?
- [ ] A) `expect(page.get_by_role("option", name="PyPy")).to_be_checked()`
- [ ] B) `expect(page.locator("option:checked")).to_have_text("PyPy")`
- [ ] C) `expect(page.get_by_role("option", selected=True)).to_have_text("PyPy")`
- [ ] D) `expect(page.get_by_role("option")).to_have_text("PyPy")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `expect(page.get_by_role("option", selected=True)).to_have_text("PyPy")`

**Explanation:** `get_by_role("option", selected=True)` finds the option whose `aria-selected` is true, which is how you assert keyboard navigation step by step.
- **Why others are wrong:**
  - A) `to_be_checked` applies to checkable controls (checkboxes, radios, switches); a highlighted list item is not "checked".
  - B) `option:checked` targets `<option>` elements inside a native `<select>`, not `role="option"` list items.
  - D) That does not filter to the highlighted item; with several options it compares all of them to one string and fails.

</details>

---

### 21. Which call right-clicks an element to trigger its `contextmenu` event?
- [ ] A) `locator.right_click()`
- [ ] B) `locator.click(modifiers=["Control"])`
- [ ] C) `locator.dblclick()`
- [ ] D) `locator.click(button="right")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `locator.click(button="right")`

**Explanation:** Mouse button choice is the `button` argument of `click`: `"left"`, `"right"` or `"middle"`.
- **Why others are wrong:**
  - A) No such method exists. A right-click is `click` with `button="right"`.
  - B) `modifiers` holds keys down during a normal left click; it does not choose the mouse button.
  - C) A double-click fires two clicks and a `dblclick` event, not `contextmenu`.

</details>

---

## Part 2: True or False (Common Misconceptions)

### 22. True or False: If a test clicks "Delete" and never registers a `dialog` listener, the test hangs because the `confirm` dialog stays open.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Playwright auto-dismisses dialogs when no listener exists, so the test does not hang. The catch is that "dismiss" means Cancel, so the delete never happens and a later assertion fails confusingly.

</details>

---

### 23. True or False: Radio buttons that share the same `name` attribute form a group in which the browser lets at most one be selected at a time.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Selecting one radio automatically deselects the previously selected one in the same group. This is why a bug such as two radios with different `name` values lets a user select both.

</details>

---

### 24. True or False: If a dropdown is built from `<div>` and `<li role="option">` elements, `select_option()` still works as long as you pass the right label.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `select_option` only works on a native `<select>` element; on anything else it raises "Element is not a <select> element". Custom dropdowns need click-to-open then click-the-option.

</details>

---

### 25. True or False: A call such as `locator.fill("abc")` sets the value in one step and fires a single `input` event, without a `keydown`/`keyup` for each character.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** That is exactly why `fill` is fast and reliable for normal fields, but may appear to "do nothing" on widgets that listen for key events.

</details>

---

### 26. True or False: Passing `delay=100` to `press_sequentially` means you no longer need to wait for the suggestion list with an assertion.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `delay` only controls the pause between keystrokes (typing speed). The list still needs a proper wait, such as `expect(options).to_have_text([...])`.

</details>

---

### 27. True or False: For a `prompt` dialog, calling `dialog.dismiss()` makes the page's JavaScript receive `null`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Cancel returns `null` for a prompt (and `false` for a confirm). That is different from pressing OK with nothing typed, which returns an empty string, so good tests cover both paths.

</details>

---

### 28. True or False: Setting a checkbox with `locator.evaluate("el => el.checked = true")` is just as good as `check()`, because the box ends up ticked either way.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The JavaScript shortcut changes the property without firing the click/input/change events the application listens for, so the app may stay unaware. `check()` performs a real click.

</details>

---

### 29. True or False: Calling `select_option([])` on a `<select multiple>` clears the selection.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `select_option` replaces the selection with exactly what you list, so an empty list leaves nothing selected. `expect(select).to_have_values([])` confirms it.

</details>

---

### 30. True or False: Key names are case-sensitive: `press("Enter")` is valid, whereas `press("enter")` raises an "Unknown key" error.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Names follow the DOM `KeyboardEvent.key` values. Also remember `Escape` (not `Esc`) and `Control` (not `Ctrl`).

</details>

---

### 31. True or False: Asserting only that the suggestion list is visible proves it shows suggestions for the text you just typed.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The list may be visible from an earlier keystroke. Wait for content that proves it matches your input, for example `expect(options).to_have_text([...])` or `expect(options.first).to_contain_text("Py")`.

</details>

---

### 32. True or False: Putting a failing `assert` inside the dialog handler before `dialog.accept()` can leave the dialog unanswered and the page frozen.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The exception stops the handler before it answers. The robust style is to record the facts, answer the dialog, and assert afterwards in the test body.

</details>

---

### 33. True or False: Calling `check()` on a checkbox that is already ticked does nothing and does not raise an error.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `check()` means "ensure checked". If the box is already checked it returns immediately, which is what makes it idempotent and safer than `click()`.

</details>

---

### 34. True or False: The recommended way to pick an option in a native `<select>` is to locate the `<option>` element and `click()` it.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Native option lists cannot be clicked reliably, especially headless. Use `select_option()`, which sets the selection and fires the `input` and `change` events.

</details>

---

### 35. True or False: `page.mouse.click(500, 300)` is a robust choice because pixel coordinates mean the same thing on every viewport size and layout.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Hard-coded coordinates break when the viewport or layout changes. Derive coordinates from `bounding_box()` at the moment of use, or prefer locator actions.

</details>

---

### 36. True or False: A locator such as `page.get_by_role("option", name="Python")` is safer than a stored element handle for a suggestion list that is rebuilt on every lookup.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Locators re-resolve the element each time they act, while a stored handle can point at an option that has since been removed from the DOM (stale reference).

</details>

---

## Part 3: Code Prediction

*Assume `page` is a blank Playwright sync `Page` (for example from the `pytest-playwright` fixture) and `expect` is imported from `playwright.sync_api`. Every snippet in this part was executed against Chromium to confirm the answer.*

### 37. A page's `confirm()` result is written into `#out`. No dialog listener is registered. What does this code print?
```python
page.set_content("""
<button id="b">Delete</button><p id="out"></p>
<script>b.onclick = () => { out.textContent = String(confirm("Sure?")); }</script>
""")
page.get_by_role("button", name="Delete").click()
print(page.locator("#out").inner_text())
```

- [ ] A) `true`
- [ ] B) `null`
- [ ] C) The code raises `TimeoutError` because the dialog is never answered.
- [ ] D) `false`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `false`

**Explanation:** With no `dialog` listener, Playwright auto-dismisses, so `confirm()` returns `false` and `String(false)` is written to the page.
- **Why others are wrong:**
  - A) Returning `true` would need an explicit `dialog.accept()` handler; the default answer is Cancel.
  - B) `null` is what a dismissed `prompt` returns. `confirm` returns a boolean, so a dismissed confirm gives `false`.
  - C) That only happens when a listener exists but fails to answer. With no listener Playwright answers Cancel for you.

</details>

---

### 38. A checkbox starts ticked. What does this print (two lines)?
```python
page.set_content('<input type="checkbox" id="c" checked>')
box = page.locator("#c")

box.click()
print(box.is_checked())

box.check()
print(box.is_checked())
```

- [ ] A) `True` then `True`
- [ ] B) `False` then `False`
- [ ] C) `False` then `True`
- [ ] D) `True` then `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `False` then `True`

**Explanation:** `click()` flips the state (ticked to unticked), whereas `check()` ensures the final state is ticked.
- **Why others are wrong:**
  - A) `click()` toggles, so the pre-ticked box becomes unticked after the first call.
  - B) `check()` ensures the box is checked, so it clicks again and ticks it.
  - D) This is the reverse. `click()` unticks first and `check()` then ticks it.

</details>

---

### 39. What does `select_option` return here?
```python
page.set_content("""
<select id="country">
  <option value="">-- choose --</option>
  <option value="us">United States</option>
  <option value="ca">Canada</option>
</select>
""")
result = page.locator("#country").select_option(label="Canada")
print(result)
```

- [ ] A) `['Canada']`
- [ ] B) `['ca']`
- [ ] C) `['ca', 'Canada']`
- [ ] D) `None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['ca']`

**Explanation:** Selecting by label picks the Canada option, and `select_option` returns the values of the selected options: `['ca']`.
- **Why others are wrong:**
  - A) The return value is the list of selected option **values**, not their labels.
  - C) It returns one value per selected option; the label is not included.
  - D) It returns a list of the values now selected, so a successful call is not `None`.

</details>

---

### 40. The page logs every `keyup`. What does this print?
```python
page.set_content("""
<input id="live" aria-label="Live"><p id="keys"></p>
<script>live.addEventListener("keyup", e => keys.textContent += e.key + " ");</script>
""")
live = page.get_by_label("Live")

live.fill("abc")
live.press_sequentially("de")
print(live.input_value(), "|", page.locator("#keys").inner_text().strip())
```

- [ ] A) `de | d e`
- [ ] B) `abcde | a b c d e`
- [ ] C) `abcde | d e`
- [ ] D) `abcde | ` (nothing logged)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `abcde | d e`

**Explanation:** `fill("abc")` sets the value without `keyup`, and `press_sequentially("de")` appends and fires `keyup` for d and e.
- **Why others are wrong:**
  - A) `press_sequentially` appends at the caret and does not clear the field, so the value keeps the earlier "abc".
  - B) `fill` fires no key events, so only the characters typed afterwards ("d" and "e") are logged.
  - D) `press_sequentially` generates real key events, so "d" and "e" are logged.

</details>

---

### 41. The widget refreshes only on `keyup`. What does this print (two lines)?
```python
page.set_content("""
<input id="q" aria-label="Search"><p id="hits"></p>
<script>q.addEventListener("keyup", () => { hits.textContent = "lookup for " + q.value; });</script>
""")
box = page.get_by_label("Search")

box.fill("Py")
print(repr(page.locator("#hits").inner_text()))

box.press_sequentially("t")
print(repr(page.locator("#hits").inner_text()))
```

- [ ] A) `'lookup for Py'` then `'lookup for Pyt'`
- [ ] B) `''` then `''`
- [ ] C) `'lookup for Py'` then `'lookup for t'`
- [ ] D) `''` then `'lookup for Pyt'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `''` then `'lookup for Pyt'`

**Explanation:** `fill("Py")` does not trigger the `keyup` listener; the real keypress of "t" does, and the field then holds "Pyt".
- **Why others are wrong:**
  - A) `fill` fires no `keyup`, so the first print is still empty.
  - B) `press_sequentially` fires a real `keyup` for "t", so the widget runs.
  - C) The widget reads the whole field value, which after appending is "Pyt".

</details>

---

### 42. The page asks two confirmations in a row and only one `once` handler is registered. What does this print?
```python
page.set_content("""
<button id="b">Go</button><p id="out"></p>
<script>
  b.onclick = () => {
    const a = confirm("First?");
    const c = confirm("Second?");
    out.textContent = a + "," + c;
  };
</script>
""")
page.once("dialog", lambda dialog: dialog.accept())
page.get_by_role("button", name="Go").click()
print(page.locator("#out").inner_text())
```

- [ ] A) `true,false`
- [ ] B) `true,true`
- [ ] C) `false,false`
- [ ] D) The code raises `TimeoutError`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `true,false`

**Explanation:** The first confirm is accepted (`true`). Then the `once` listener is gone, so the second is auto-dismissed (`false`).
- **Why others are wrong:**
  - B) `once` removes the handler after the first dialog, so it cannot accept the second one.
  - C) The first dialog was accepted by the handler, so its answer is `true`.
  - D) After the `once` handler has fired, no listener remains, so Playwright's default auto-dismiss applies again and the page does not freeze.

</details>

---

### 43. Standard starts checked. What does this print: how many radios of the group are checked, and the value of the checked one?
```python
page.set_content("""
<label><input type="radio" name="s" value="std" checked> Standard</label>
<label><input type="radio" name="s" value="exp"> Express</label>
<label><input type="radio" name="s" value="ovn"> Overnight</label>
""")
page.get_by_role("radio", name="Express").check()
page.get_by_role("radio", name="Overnight").check()

checked = page.locator("input[name='s']:checked")
print(checked.count(), checked.input_value())
```

- [ ] A) `2 ovn`
- [ ] B) `1 exp`
- [ ] C) `1 ovn`
- [ ] D) `1 std`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1 ovn`

**Explanation:** Each `check()` replaces the selection within the group, so only Overnight remains, giving a count of 1 and the value `ovn`.
- **Why others are wrong:**
  - A) Radios in one `name` group are mutually exclusive, so the browser deselects the previous one.
  - B) Express was checked first but then replaced when Overnight was checked.
  - D) The `checked` attribute is only the default; checking another radio replaces it.

</details>

---

### 44. What does this code print?
```python
page.set_content("""
<select id="s" multiple>
  <option value="py">Python</option>
  <option value="sql">SQL</option>
  <option value="git">Git</option>
</select>
""")
s = page.locator("#s")
s.select_option(["py", "sql"])
s.select_option(["git"])
print(s.evaluate("el => Array.from(el.selectedOptions).map(o => o.value)"))
```

- [ ] A) `['py', 'sql', 'git']`
- [ ] B) `['py', 'sql']`
- [ ] C) `['sql', 'git']`
- [ ] D) `['git']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `['git']`

**Explanation:** Each call replaces the whole selection, so after the second call only `git` is selected.
- **Why others are wrong:**
  - A) `select_option` replaces the selection rather than adding to it.
  - B) The second call changes the selection, so the first call's values are gone.
  - C) Nothing is partially kept. Only the values passed in the latest call are selected.

</details>

---

### 45. Which events are logged by this double-click?
```python
page.set_content("""
<button id="b">Go</button><p id="log"></p>
<script>
  b.addEventListener("click", () => log.textContent += "click ");
  b.addEventListener("dblclick", () => log.textContent += "dblclick ");
</script>
""")
page.get_by_role("button", name="Go").dblclick()
print(page.locator("#log").inner_text().strip())
```

- [ ] A) `dblclick`
- [ ] B) `click click dblclick`
- [ ] C) `click dblclick`
- [ ] D) `click click`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `click click dblclick`

**Explanation:** `dblclick()` generates two quick clicks and then a `dblclick` event.
- **Why others are wrong:**
  - A) A double-click is two clicks followed by a `dblclick` event, so the two `click` events are logged too.
  - C) Two quick clicks occur, so `click` fires twice before `dblclick`.
  - D) The `dblclick` event is also dispatched after the second click.

</details>

---

### 46. The list has two options, Java and JavaScript. What does this print?
```python
page.set_content("""
<ul>
  <li role="option">Java</li>
  <li role="option">JavaScript</li>
</ul>
""")
try:
    page.get_by_role("option", name="Java").click()
    print("clicked")
except Exception as e:
    print("error:", "strict mode violation" in str(e))
```

- [ ] A) `clicked`, because Java is the closest match
- [ ] B) `clicked`, because the first matching option is used
- [ ] C) `error: True`
- [ ] D) `error: False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `error: True`

**Explanation:** `name="Java"` is a substring match and resolves to both options, so the click raises a strict mode violation.
- **Why others are wrong:**
  - A) Playwright does not look for a "closest" match; the name matches by substring.
  - B) Strict mode raises an error instead of guessing among several matches.
  - D) The error is a strict mode violation, so its message does contain that phrase.

</details>

---

### 47. The page writes the `prompt` result into `#out`. What does this code print (two lines)?
```python
page.set_content("""
<button id="b">Ask</button><p id="out"></p>
<script>b.onclick = () => { out.textContent = "You entered: " + prompt("Name?"); }</script>
""")
page.once("dialog", lambda dialog: dialog.accept("Bob"))
page.get_by_role("button", name="Ask").click()
print(page.locator("#out").inner_text())

page.once("dialog", lambda dialog: dialog.dismiss())
page.get_by_role("button", name="Ask").click()
print(page.locator("#out").inner_text())
```

- [ ] A) `You entered: Bob` then `You entered: ` (nothing after the colon)
- [ ] B) `You entered: Bob` then `You entered: undefined`
- [ ] C) `You entered: null` then `You entered: Bob`
- [ ] D) `You entered: Bob` then `You entered: null`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `You entered: Bob` then `You entered: null`

**Explanation:** `accept("Bob")` types the text into the prompt, and `dismiss()` presses Cancel so the page receives `null`.
- **Why others are wrong:**
  - A) Cancel gives `null`, which JavaScript string concatenation prints as the word "null". An empty string would result from OK with no text typed.
  - B) A dismissed prompt returns `null`, not `undefined` (`undefined` is what `alert()` returns).
  - C) The order is reversed. The first click is answered with `accept("Bob")` and the second with `dismiss()`.

</details>

---

### 48. Email starts unticked; SMS and Push start ticked. What does this print?
```python
page.set_content("""
<label><input type="checkbox"> Email</label>
<label><input type="checkbox" checked> SMS</label>
<label><input type="checkbox" checked> Push</label>
""")
page.get_by_label("Email").set_checked(True)
page.get_by_label("SMS").set_checked(False)
page.get_by_label("Push").set_checked(True)

print([page.get_by_label(n).is_checked() for n in ("Email", "SMS", "Push")])
```

- [ ] A) `[True, True, True]`
- [ ] B) `[False, True, True]`
- [ ] C) `[True, False, True]`
- [ ] D) `[True, False, False]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `[True, False, True]`

**Explanation:** `set_checked(wanted)` means "make it so": Email becomes True, SMS False, and Push stays True.
- **Why others are wrong:**
  - A) `set_checked(False)` unticks SMS, so it cannot still be `True`.
  - B) That is the starting state. `set_checked` brings each box to the requested state.
  - D) `set_checked(True)` on an already-ticked box leaves it ticked; it never toggles it off.

</details>

---

### 49. Remember that the first option is a placeholder. What does this print?
```python
page.set_content("""
<select id="country">
  <option value="">-- choose --</option>
  <option value="us">United States</option>
  <option value="ca">Canada</option>
</select>
""")
page.locator("#country").select_option(index=1)
print(page.locator("#country").input_value(), "|",
      page.locator("#country option:checked").inner_text())
```

- [ ] A) `us | United States`
- [ ] B) ` | -- choose --` (empty value, then the placeholder text)
- [ ] C) `ca | Canada`
- [ ] D) `us | us`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `us | United States`

**Explanation:** Index 1 is the second option (United States, value `us`), and `option:checked` exposes the selected option's visible text.
- **Why others are wrong:**
  - B) Indexes are zero-based, so index 0 is the placeholder and index 1 is United States.
  - C) Canada is the third option (index 2), not index 1.
  - D) `option:checked` is the selected `<option>` element, whose visible text is "United States", not its value.

</details>

---

### 50. What does this code print (two lines)?
```python
page.set_content("""
<button id="b" onclick="out.textContent = 'pressed'">Go</button>
<p id="out">idle</p>
""")
page.keyboard.press("Enter")
print(page.locator("#out").inner_text())

page.locator("#b").focus()
page.keyboard.press("Enter")
print(page.locator("#out").inner_text())
```

- [ ] A) `pressed` then `pressed`
- [ ] B) `idle` then `idle`
- [ ] C) `pressed` then `idle`
- [ ] D) `idle` then `pressed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `idle` then `pressed`

**Explanation:** `page.keyboard` has no element awareness: the first Enter hits nothing, but after `focus()` the second Enter activates the button.
- **Why others are wrong:**
  - A) With nothing focused, `page.keyboard.press("Enter")` goes to the page body, not the button.
  - B) After `focus()`, the second Enter press activates the focused button.
  - C) This is the reverse. Nothing is focused during the first press, and the button is focused for the second.

</details>

---

### 51. What does this code print (two lines)?
```python
page.set_content('<input id="q" aria-label="Search">')
box = page.get_by_label("Search")

box.press_sequentially("Py")
box.press_sequentially("Ja")
print(box.input_value())

box.clear()
box.press_sequentially("Ja")
print(box.input_value())
```

- [ ] A) `Ja` then `Ja`
- [ ] B) `PyJa` then `PyJa`
- [ ] C) `PyJa` then `Ja`
- [ ] D) `Py` then `Ja`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `PyJa` then `Ja`

**Explanation:** `press_sequentially` appends to existing text. Clearing first gives a clean start.
- **Why others are wrong:**
  - A) `press_sequentially` appends, so the first print is the combined text.
  - B) `clear()` empties the field, so the second print contains only the newly typed text.
  - D) The second `press_sequentially` appends to the first, so the first print is "PyJa".

</details>

---

### 52. The handler records the dialog's properties and then dismisses it. What does this print?
```python
page.set_content("""
<button id="b">Ask</button>
<script>b.onclick = () => { prompt("Name?", "Guest"); }</script>
""")
seen = []

def handler(dialog):
    seen.append((dialog.type, dialog.message, dialog.default_value))
    dialog.dismiss()

page.once("dialog", handler)
page.get_by_role("button", name="Ask").click()
print(seen)
```

- [ ] A) `[('prompt', 'Name?', '')]`
- [ ] B) `[('prompt', 'Name?', 'Guest')]`
- [ ] C) `[('prompt', 'Guest', 'Name?')]`
- [ ] D) `[]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[('prompt', 'Name?', 'Guest')]`

**Explanation:** `type`, `message` and `default_value` are properties of the `Dialog` object: here `prompt`, the question text and the pre-filled `Guest`.
- **Why others are wrong:**
  - A) `default_value` holds the pre-filled text, which is the second argument of `prompt()`. It is empty only for dialogs that have no default.
  - C) The two values are swapped. `message` is the first argument of `prompt()` and `default_value` the second.
  - D) The handler is called for every dialog (dismissing happens inside it), so the list is filled.

</details>

---

### 53. What does this code print?
```python
page.set_content("""
<input type="checkbox" id="a">
<input type="checkbox" id="b" value="yes" checked>
""")
print(page.locator("#a").input_value(), page.locator("#b").input_value())
```

- [ ] A) `None yes`
- [ ] B) `False True`
- [ ] C) `on on`
- [ ] D) `on yes`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `on yes`

**Explanation:** For checkboxes `input_value()` returns the `value` attribute regardless of checked state: `on` by default, or whatever the developer set.
- **Why others are wrong:**
  - A) A checkbox with no `value` attribute reports the browser default `on`, not `None`.
  - B) `input_value()` returns the `value` attribute, not the checked state (use `is_checked()` for that).
  - C) The second checkbox declares `value="yes"`, so that is what it reports.

</details>

---

### 54. Which element id does this print?
```python
page.set_content("""
<input id="n" aria-label="Name">
<input id="e" aria-label="Email">
<input id="s" type="checkbox" aria-label="Subscribe">
""")
page.get_by_label("Name").focus()
page.keyboard.press("Tab")
page.keyboard.press("Tab")
page.keyboard.press("Shift+Tab")
print(page.evaluate("document.activeElement.id"))
```

- [ ] A) `n`
- [ ] B) `s`
- [ ] C) `e`
- [ ] D) An empty line (focus is on `<body>`)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `e`

**Explanation:** Name to Email to Subscribe with two Tabs, then `Shift+Tab` moves focus backwards to Email (`e`).
- **Why others are wrong:**
  - A) That would need two `Shift+Tab` presses. Focus moved forward twice and back once.
  - B) That is where focus is after two Tab presses, before `Shift+Tab` moves it back.
  - D) Focus always lands on one of the three inputs, each of which has an id.

</details>

---

## Part 4: Fill-in-the-Blank

### 55. Fill in the blank: To answer a `prompt` dialog by typing text, call `dialog._____("my text")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `accept`

**Explanation:** `dialog.accept(prompt_text)` presses OK and enters the given text. `dismiss()` would press Cancel instead.

</details>

---

### 56. Fill in the blank: To assert that a checkbox is not ticked, write `expect(box)._____()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `not_to_be_checked`

**Explanation:** Equivalent: `expect(box).to_be_checked(checked=False)`. Both retry automatically until the state is reached or the timeout expires.

</details>

---

### 57. Fill in the blank: To select an option in a `<select>` by its visible text, use `select_option(_____="Canada")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `label`

**Explanation:** The three keyword forms are `value=`, `label=` and `index=`. `label=` matches the text the user sees.

</details>

---

### 58. Fill in the blank: The current name of the method that types one character at a time, replacing the deprecated `locator.type()`, is `locator._____()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `press_sequentially`

**Explanation:** It generates the full key-event sequence for each character and appends at the caret. Do not confuse it with `page.keyboard.type()`, which is still valid.

</details>

---

### 59. Fill in the blank: To find the keyboard-highlighted suggestion, use `page.get_by_role("option", _____=True)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `selected`

**Explanation:** `get_by_role("option", selected=True)` matches the option whose `aria-selected` attribute is `true`.

</details>

---

### 60. Fill in the blank: The dialog handler must be registered _____ the action (such as a click) that opens the dialog.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `before`

**Explanation:** The dialog opens during the click, so by the time the click has been issued it is too late to start listening.

</details>

---

### 61. Fill in the blank: The CSS pseudo-class `:_____` matches ticked checkboxes and selected radios, for example `input[name='size']:_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `checked`

**Explanation:** Used with `to_have_count`, it counts how many controls are ticked, for example to verify a "select all" feature or that a radio group has exactly one selection.

</details>

---

### 62. Fill in the blank: To clear every selection in a `<select multiple>`, call `select_option(_____)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `[]` (an empty list)

**Explanation:** Because `select_option` replaces the selection with exactly what you pass, an empty list leaves nothing selected.

</details>

---

### 63. Fill in the blank: The modifier that means Control on Windows/Linux and Command on macOS is `_____`, as in `press("_____+A")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `ControlOrMeta`

**Explanation:** It makes shortcuts such as select-all or copy work on every operating system.

</details>

---

### 64. Fill in the blank: The central rule for suggestion lists: wait for the _____ you care about (for example the expected options), not for a number of seconds.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `condition` (the expected content)

**Explanation:** Auto-retrying assertions such as `expect(options).to_have_text([...])` wait for the right content and avoid both flakiness and slowness.

</details>

---

### 65. Fill in the blank: Location and notification questions are not JavaScript dialogs. Pre-answer them when creating the browser context with `_____=["geolocation"]`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `permissions`

**Explanation:** These are browser permission prompts; the `dialog` event does not receive them, so you set permissions up front.

</details>

---

### 66. Fill in the blank: `locator._____(wanted)` takes a boolean and behaves like `check()` for `True` and `uncheck()` for `False`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `set_checked`

**Explanation:** It suits data-driven tests where the desired state comes from a variable, with no `if` needed.

</details>

---

### 67. Fill in the blank: For a `<select multiple>`, verify the chosen values with `expect(select).to_have_____(["py", "sql"])`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `values`

**Explanation:** `to_have_value` (singular) is for a single select and `to_have_values` (plural) takes a list for a multi-select.

</details>

---

### 68. Fill in the blank: To scroll the page down by 500 pixels with the low-level mouse, call `page.mouse._____(0, 500)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `wheel`

**Explanation:** The arguments are `delta_x` and `delta_y`. The wheel is used, for example, for infinite-scroll features.

</details>

---

### 69. Fill in the blank: Because `press_sequentially` appends to existing text, call `locator._____()` first when the search box may already contain text.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `clear`

**Explanation:** `locator.clear()` (or `fill("")`) empties the field so the new term is not appended to old text.

</details>

---

*End of quiz. Review any question you missed by re-reading the matching lesson section, then retry the question in your own test file.*
