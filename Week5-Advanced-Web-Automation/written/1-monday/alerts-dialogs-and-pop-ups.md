# Alerts, Dialogs and Pop-ups

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between the three JavaScript dialogs (`alert`, `confirm`, `prompt`) and the special `beforeunload` dialog, and recognise each one in a real application.
- Describe what Playwright does with a dialog when you do nothing, and why that default is often not what your test needs.
- Register a dialog handler with `page.on("dialog", ...)` and `page.once("dialog", ...)`, and choose the right one for a given situation.
- Use the `Dialog` object (`dialog.type`, `dialog.message`, `dialog.default_value`, `dialog.accept()`, `dialog.dismiss()`) to read what the page said and to answer it.
- Type text into a `prompt` dialog and verify that the application reacted correctly to "OK" and "Cancel".
- Tell the difference between a real browser dialog, an in-page HTML modal, a pop-up window, and a browser permission prompt, and pick the correct technique for each.
- Avoid the most common causes of "hanging" and flaky dialog tests.

---

## Why This Matters

Week 5 is about **mastering complex UI interactions**. In earlier weeks you learned how to find elements with locators and perform the basic actions: navigate, click, fill, and assert. Those skills carry you through simple "happy path" pages. Real applications, however, are full of moments where the browser or the page interrupts the user and asks a question: *"Are you sure you want to delete this?"*, *"You have unsaved changes, do you really want to leave?"*, *"Please enter a reason for cancelling."* If your automation cannot respond to these interruptions, a large portion of real-world workflows simply cannot be tested.

This lesson is the first of five on Monday, and it fits directly into **Project 1: QE Foundations**. The Project 1 UI milestone asks you to automate a complex form flow. In real forms, destructive actions (deleting a record, cancelling an order, resetting a form) are very frequently protected by a confirmation dialog. A test that cannot deal with the dialog cannot complete the flow, and a test that silently dismisses the dialog without checking it may let a serious bug through: imagine the "Delete" button deleting the record even when the user presses "Cancel". Learning to handle dialogs *and verify them* is therefore both a mechanical skill (so your test does not hang) and a quality skill (so your test actually proves something).

There is also an important professional point. A hanging test is one of the most expensive kinds of failure in a CI pipeline: it consumes a runner for the entire timeout, blocks the queue, and gives a vague error. Understanding how Playwright and the browser cooperate around dialogs is how you prevent that.

---

## The Concept

### 1. What is a JavaScript dialog?

A **dialog** (sometimes called a *native dialog* or *browser dialog*) is a small window drawn **by the browser itself**, not by the web page's HTML. A page asks the browser to display one by calling a built-in JavaScript function. There are three of these functions:

| JavaScript call | Dialog type | What the user sees | What the page gets back |
|---|---|---|---|
| `alert("Saved!")` | `alert` | A message and a single **OK** button | Nothing (`undefined`) |
| `confirm("Delete this?")` | `confirm` | A message with **OK** and **Cancel** | `true` for OK, `false` for Cancel |
| `prompt("Your name?", "Guest")` | `prompt` | A message, a text box (pre-filled with the default), **OK** and **Cancel** | The typed text for OK, `null` for Cancel |

There is a fourth kind, **`beforeunload`**, which the browser shows when a user tries to close or leave a page that has registered a "you have unsaved changes" warning. We will look at it later in this lesson.

**An analogy.** Think of the web page as an office and the browser as the building's security desk. When the office wants to ask the visitor something urgent, it can pick up an intercom (`alert`, `confirm`, `prompt`). The security desk, not the office, makes the announcement, and **the whole building stops until the visitor answers**. That last point is the key to everything in this lesson.

### 2. Dialogs are *modal* and *blocking*

Native dialogs are **modal**: while one is open, the user cannot interact with the page behind it. They are also **blocking**: the page's JavaScript literally pauses on the line that called `alert()` / `confirm()` / `prompt()` and does not continue until the dialog is closed. The page cannot render updates, run timers or respond to clicks.

For automation this has a very important consequence. If a test clicks a button that triggers a dialog and nobody answers the dialog, the page is frozen. Any further command that needs the page to respond (reading text, clicking something else) cannot finish, and the test hangs until a timeout fires.

### 3. What Playwright does by default

Playwright's designers wanted tests not to hang by accident. So the rule is:

> **If there is no `dialog` listener registered on the page, Playwright automatically dismisses every dialog.**

"Dismiss" means pressing **Cancel** (or closing it). For an `alert` there is only one button so that is harmless. For a `confirm`, dismissing returns `false`; for a `prompt`, it returns `null`.

So the following surprising thing is true: **if you click "Delete" and never register a handler, Playwright answers "Cancel" on your behalf**. Your test will not hang, but the delete will not happen, and your next assertion ("the row is gone") will fail with an unclear message. Many beginners spend an hour confused about this behaviour. Whenever a flow includes a `confirm` or a `prompt`, you must decide explicitly what answer you want to give.

The second half of the rule is the dangerous one:

> **If you register at least one `dialog` listener, Playwright stops auto-dismissing. Your listener is now responsible for calling `accept()` or `dismiss()` on every dialog.**

If your listener forgets to do either (for example, because of an `if` that does not match), the dialog stays open, the page is frozen, and the test hangs. We will return to this in the pitfalls section.

### 4. The `dialog` event and the `Dialog` object

Playwright exposes dialogs through the page's **event** system. An event is something that happens at an unpredictable moment (a dialog opening) to which your code can attach a function to run when it happens, called a **handler** or **listener**.

```python
page.on("dialog", handler_function)
```

Whenever a dialog opens on that page, Playwright calls `handler_function` and passes it one argument: a **`Dialog`** object. This object has:

| Member | What it gives you |
|---|---|
| `dialog.type` | A string: `"alert"`, `"confirm"`, `"prompt"` or `"beforeunload"` |
| `dialog.message` | The text the page asked to display |
| `dialog.default_value` | For a `prompt`, the pre-filled text (the second argument of `prompt()`); empty string otherwise |
| `dialog.accept(prompt_text=None)` | Press **OK**. For a `prompt`, you can pass the text to type |
| `dialog.dismiss()` | Press **Cancel** (or close) |

Note carefully: `message`, `type` and `default_value` are **properties** (no parentheses), while `accept()` and `dismiss()` are **methods** (with parentheses).

### 5. `page.on` versus `page.once`

Both attach a handler to the `dialog` event. The difference is how long it stays attached.

- `page.on("dialog", handler)` keeps the handler active for **every** dialog from now until you remove it (`page.remove_listener("dialog", handler)`) or the page closes.
- `page.once("dialog", handler)` runs the handler for **only the next** dialog, then removes it automatically.

Which should you use?

- Use **`once`** when you expect exactly one dialog at a specific step and want a different answer at different steps (accept here, dismiss there). It is the safest choice because the handler cannot leak into later steps.
- Use **`on`** when the same behaviour applies to a whole test or fixture ("accept every alert on this page"), or when a flow may open several dialogs in a row.

Because of the "listener makes you responsible" rule above, `once` has another benefit: after it has fired, the page returns to the default "auto-dismiss" behaviour, so an unexpected *second* dialog will not freeze the page.

### 6. Register the handler **before** the action that triggers the dialog

The dialog appears *during* the click. By the time `page.get_by_role("button", name="Delete").click()` has been issued, it is too late to start listening. The correct order is always:

1. Register the handler.
2. Perform the action that opens the dialog.
3. Assert on the outcome.

```python
page.once("dialog", lambda dialog: dialog.accept())   # 1. listen first
page.get_by_role("button", name="Delete").click()      # 2. trigger
expect(page.locator("#status")).to_have_text("Deleted")  # 3. verify
```

### 7. Answering a `prompt`

A `prompt` is the only dialog where you type something. Pass the text to `accept()`:

```python
page.once("dialog", lambda dialog: dialog.accept("Customer asked to cancel"))
```

If you call `dialog.accept()` with no argument on a `prompt`, the browser submits the pre-filled `default_value` (or an empty string if there is none). If you call `dialog.dismiss()`, the page's JavaScript receives `null`. Well-written applications treat `null` (Cancel) differently from an empty string (OK with nothing typed), so a thorough test checks both.

### 8. Reading the message and asserting on the dialog itself

Often you need to prove not only that *you* handled the dialog, but that the application showed the **right** dialog with the **right** text and type. For example, "Are you sure you want to delete invoice 1042?" should name the right invoice. Capture the details inside the handler and check them afterwards:

```python
seen = []

def handle(dialog):
    seen.append((dialog.type, dialog.message))
    dialog.accept()

page.once("dialog", handle)
page.get_by_role("button", name="Delete").click()

assert seen == [("confirm", "Delete invoice 1042?")]
```

We store the information in a list because the handler runs as a separate function; it cannot simply `return` a value to the test body. A list defined outside the function is visible inside it (this is a closure, a concept from your Python weeks).

### 9. The `beforeunload` dialog

Some applications register a `beforeunload` handler so that closing the tab or navigating away from a page with unsaved edits triggers the browser's "Leave site? Changes you made may not be saved." prompt. Modern browsers show this prompt only if the user has *interacted* with the page, and they ignore custom text (they show their own generic message). In Playwright:

- By default, `page.close()` does **not** run `beforeunload` handlers.
- To trigger them, call `page.close(run_before_unload=True)`. The browser then emits a `dialog` event with `dialog.type == "beforeunload"`, which you handle like any other dialog (`accept()` to leave, `dismiss()` to stay).
- Navigating with `page.goto(...)` away from such a page can also raise the dialog if the page has registered the handler and the user has interacted with it.

This is a niche case, but it is valuable for forms with "unsaved changes" protection.

### 10. Things that *look* like dialogs but are not

This is the most useful distinction in the entire lesson, because choosing the wrong technique is the most common beginner mistake.

**(a) In-page HTML modals.** Most modern sites do **not** use `confirm()`. They draw their own pop-up with HTML and CSS: a `<div role="dialog">` with a dark overlay and "Cancel" / "Confirm" buttons (Bootstrap modals, Material UI dialogs, cookie banners, "subscribe to our newsletter" overlays). These are ordinary DOM elements. **`page.on("dialog")` will never fire for them.** You handle them with locators and the normal actions you already know:

```python
modal = page.get_by_role("dialog")
expect(modal).to_be_visible()
modal.get_by_role("button", name="Confirm").click()
expect(modal).to_be_hidden()
```

A reliable quick test: if you can right-click the pop-up and choose "Inspect" in browser DevTools, and you can see it in the HTML, it is an in-page modal. Native dialogs cannot be inspected because they are not part of the page.

**(b) Pop-up windows.** Sometimes clicking a link opens a **new browser window or tab** (for example "Sign in with a provider" or "Print preview"). That is a separate *page*, not a dialog. Playwright reports it with the `popup` event, and you can wait for it with `page.expect_popup()`. Working with several tabs and windows is a topic we will cover in depth on Tuesday, so for today just remember: a new window is not a `dialog`.

**(c) Browser permission prompts.** "example.com wants to know your location" and "Allow notifications?" are browser UI, but they are not JavaScript dialogs and the `dialog` event does not receive them. In Playwright you decide permissions up front when creating a browser context (for example `permissions=["geolocation"]`). We mention it only so you know where to look; you will not need it for today's forms.

**(d) HTTP authentication prompts.** A site protected by "Basic Auth" shows a browser login box. Again, this is not a `dialog` event. Playwright handles it by passing `http_credentials={"username": "...", "password": "..."}` when creating the context.

**(e) File chooser dialogs** (the operating system's "Open file" window) are also not handled by the `dialog` event. File upload and download is a Tuesday topic.

A short decision table:

| What you see | Can you inspect it in DevTools? | Technique |
|---|---|---|
| Grey system-style box with OK / Cancel | No | `page.on/once("dialog", ...)` |
| Styled box over a dimmed page | Yes | Locators + `expect` |
| A new browser tab/window | Yes (it is a page) | `expect_popup` (Tuesday) |
| Location / notification question | No | Context `permissions` |
| Login box before the page loads | No | `http_credentials` |

---

## Code Examples

All examples use **Python** with the **sync API** and the **pytest-playwright** plugin, which supplies a ready-made `page` fixture (a fresh browser page for each test). Install and run like this:

```bash
pip install pytest-playwright
playwright install
pytest -s --headed --slowmo 400 test_dialogs.py
```

`--headed` shows the browser window, `--slowmo 400` waits 400 ms between actions so you can watch, and `-s` shows any `print` output. For the examples we use a public practice site, **The Internet** (`https://the-internet.herokuapp.com/javascript_alerts`), which has three buttons that trigger an alert, a confirm and a prompt, and shows the outcome in an element with `id="result"`.

### Example 1: The simplest case, accepting an alert

```python
from playwright.sync_api import Page, expect


def test_js_alert_is_accepted(page: Page):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()

    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")
```

**Line by line**

1. `from playwright.sync_api import Page, expect`: imports two things. `Page` is the class representing a browser tab; we use it only as a **type hint** so your editor can auto-complete. `expect` is Playwright's assertion helper that automatically retries until the condition is true or a timeout expires.
2. `def test_js_alert_is_accepted(page: Page):`: pytest runs any function whose name starts with `test_`. The parameter named `page` is special: pytest-playwright recognises the name and injects a brand-new page. `: Page` is the type hint.
3. `page.goto(...)`: opens the practice page and waits for it to load.
4. `page.once("dialog", lambda dialog: dialog.accept())`: registers a one-shot listener. `lambda dialog: dialog.accept()` is a tiny anonymous function that takes the `Dialog` object and presses OK. Because this line comes **before** the click, we are ready when the dialog opens.
5. `page.get_by_role("button", name="Click for JS Alert").click()`: finds the button by its accessible role and visible name and clicks it. The page calls `alert(...)`, Playwright fires the `dialog` event, our handler presses OK, and the page resumes.
6. `expect(page.locator("#result")).to_have_text(...)`: verifies that the page's own result line shows the expected sentence. This proves the page *continued correctly after* the dialog, which is the thing a user cares about.

### Example 2: Confirm, testing both OK and Cancel

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    "action, expected_text",
    [
        ("accept", "You clicked: Ok"),
        ("dismiss", "You clicked: Cancel"),
    ],
)
def test_js_confirm_both_answers(page: Page, action: str, expected_text: str):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    def handle(dialog):
        assert dialog.type == "confirm"
        assert dialog.message == "I am a JS Confirm"
        getattr(dialog, action)()          # calls dialog.accept() or dialog.dismiss()

    page.once("dialog", handle)
    page.get_by_role("button", name="Click for JS Confirm").click()

    expect(page.locator("#result")).to_have_text(expected_text)
```

**Line by line**

1. `import pytest`: needed for `@pytest.mark.parametrize`.
2. `@pytest.mark.parametrize("action, expected_text", [...])`: a decorator that runs the same test function twice, once per tuple in the list. This is a way to avoid copy-pasting nearly identical tests. In the first run `action="accept"`; in the second, `action="dismiss"`.
3. `def test_js_confirm_both_answers(page: Page, action: str, expected_text: str):`: besides the `page` fixture, pytest passes the two parametrised values.
4. `def handle(dialog):`: instead of a `lambda`, we define a normal named function because we need several statements.
5. `assert dialog.type == "confirm"` and `assert dialog.message == "I am a JS Confirm"`: check that the application raised the correct *kind* of dialog with the correct text. If the application changed to an `alert`, or the wording changed, the test fails with a clear message.
6. `getattr(dialog, action)()`: `getattr(obj, "accept")` returns the method `obj.accept`; the trailing `()` calls it. This is a compact way of saying "call whichever method the parameter names". If this feels too clever for now, replace it with `if action == "accept": dialog.accept() else: dialog.dismiss()`.
7. `page.once("dialog", handle)`: registers the function (note: we pass `handle`, **not** `handle()`; we want to hand over the function itself, not call it now).
8. The click and `expect` lines work as before. The expected text differs per parametrised case.

> **A gotcha about `assert` inside a handler.** An assertion that fails inside an event handler raises an exception in the handler. Depending on the Playwright version and timing, the error may appear attached to a surrounding call rather than neatly to the test. The dialog may also remain unanswered if the exception occurs before `accept()`/`dismiss()`. The recommended, more robust style is shown in Example 4: *record* the facts in the handler, *answer* the dialog, then assert in the test body.

### Example 3: Prompt, typing text and checking Cancel

```python
from playwright.sync_api import Page, expect


def test_js_prompt_with_text(page: Page):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.accept("Playwright rocks"))
    page.get_by_role("button", name="Click for JS Prompt").click()

    expect(page.locator("#result")).to_have_text("You entered: Playwright rocks")


def test_js_prompt_cancelled(page: Page):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Click for JS Prompt").click()

    expect(page.locator("#result")).to_have_text("You entered: null")
```

**Explanation**

- `dialog.accept("Playwright rocks")`: types the string into the prompt's text box and presses OK. The page's JavaScript receives `"Playwright rocks"`.
- `dialog.dismiss()` on a prompt: the page receives `null`, and this demo page shows it literally as the word `null`. That is a nice illustration of why testing Cancel separately is worthwhile: the code path for "Cancel" is different from "OK with empty text".
- Two separate tests, one behaviour each: if the Cancel test fails, the failure name immediately tells you which behaviour broke.

### Example 4: Capture, answer, then assert (the robust pattern)

```python
from playwright.sync_api import Page, expect


def test_confirm_dialog_details_are_recorded(page: Page):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    dialogs_seen = []

    def record_and_accept(dialog):
        dialogs_seen.append(
            {"type": dialog.type, "message": dialog.message, "default": dialog.default_value}
        )
        dialog.accept()

    page.on("dialog", record_and_accept)
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(page.locator("#result")).to_have_text("You clicked: Ok")
    page.remove_listener("dialog", record_and_accept)

    assert len(dialogs_seen) == 1
    assert dialogs_seen[0]["type"] == "confirm"
    assert dialogs_seen[0]["message"] == "I am a JS Confirm"
```

**Line by line**

1. `dialogs_seen = []`: an empty list that will collect facts.
2. `def record_and_accept(dialog):` appends a dictionary describing the dialog, and **then** calls `dialog.accept()`. Because the answer comes straight after the recording and nothing in between can raise, the page can never be left frozen.
3. `page.on("dialog", record_and_accept)`: we use `on` (not `once`) to demonstrate the longer-lived listener.
4. We click, then use `expect(...)` to wait until the page shows the outcome. This is important: it guarantees the handler has finished running before we look at `dialogs_seen`.
5. `page.remove_listener("dialog", record_and_accept)`: good hygiene. After this, Playwright's default (auto-dismiss) applies again.
6. The final `assert` lines are plain Python `assert`, not Playwright `expect`, because we are checking an ordinary list, not a page element. Plain asserts do not retry, which is fine here because the data is already complete.

### Example 5: A reusable "accept all dialogs" helper

Sometimes a page shows many harmless alerts and you only want them out of the way. A tiny helper keeps tests tidy:

```python
from playwright.sync_api import Page


def auto_accept_dialogs(page: Page) -> list[str]:
    """Accept every dialog on this page. Returns a list that fills with messages."""
    messages: list[str] = []

    def handler(dialog):
        messages.append(dialog.message)
        dialog.accept()

    page.on("dialog", handler)
    return messages
```

**Explanation:** The function registers a persistent listener and returns the list the handler writes to. The caller can later inspect `messages` to confirm which alerts were shown. `list[str]` is a Python type hint ("a list of strings"); it has no effect at run time, but documents your intent. Next week's lesson on fixtures will show a more elegant way to package setup like this; for now a helper function is enough.

### Example 6: In-page modal (not a native dialog)

```python
from playwright.sync_api import Page, expect


def test_custom_modal_confirmation(page: Page):
    page.set_content("""
        <button id="del">Delete</button>
        <p id="status">Idle</p>
        <div role="dialog" aria-label="Confirm delete" id="modal" hidden>
          <p>Delete this item?</p>
          <button id="yes">Yes, delete</button>
          <button id="no">Cancel</button>
        </div>
        <script>
          del.onclick = () => modal.hidden = false;
          yes.onclick = () => { status.textContent = 'Deleted'; modal.hidden = true; };
          no.onclick  = () => { modal.hidden = true; };
        </script>
    """)

    page.get_by_role("button", name="Delete").click()

    modal = page.get_by_role("dialog", name="Confirm delete")
    expect(modal).to_be_visible()
    modal.get_by_role("button", name="Yes, delete").click()

    expect(modal).to_be_hidden()
    expect(page.locator("#status")).to_have_text("Deleted")
```

**Explanation**

- `page.set_content("""...""")` loads a small piece of HTML directly into the page, which is handy for self-contained demonstrations without needing a website. The `<script>` section wires three buttons to behaviour.
- The key learning: **there is no `page.on("dialog")` here.** The "dialog" is an ordinary element with `role="dialog"`. We use `get_by_role("dialog", name=...)` (the `aria-label` provides the accessible name), `to_be_visible()` and `to_be_hidden()`.
- Scoping the second click with `modal.get_by_role(...)` means "look for the button *inside* the modal", which avoids clicking a similarly named button elsewhere on the page.

### Example 7: `beforeunload` (unsaved changes)

```python
from playwright.sync_api import Page


def test_beforeunload_can_be_stayed_on(page: Page):
    page.set_content("""
        <input id="note" />
        <script>
          window.addEventListener('beforeunload', e => { e.preventDefault(); e.returnValue = ''; });
        </script>
    """)
    page.locator("#note").fill("unsaved text")   # user interaction is needed

    seen = []

    def handler(dialog):
        seen.append(dialog.type)
        dialog.dismiss()          # "Stay on page"

    page.on("dialog", handler)
    page.close(run_before_unload=True)

    assert seen == ["beforeunload"]
    assert not page.is_closed()   # we stayed
```

**Explanation:** `run_before_unload=True` asks Playwright to give the page its chance to veto closing. The listener sees a dialog whose type is `"beforeunload"`; dismissing it cancels the close, so the page stays open (`page.is_closed()` is `False`). If you changed it to `dialog.accept()` the page would close. Remember the browser only shows this dialog if the user has interacted with the page, which is why we `fill` something first.

---

## Real-World Scenarios

**Scenario 1: Delete confirmation in an admin console.** A back-office tool lets a support agent delete a customer record. The "Delete" button calls `confirm("Delete customer 8841?")`. A complete test suite includes (a) a test that accepts and verifies the customer disappears from the list, (b) a test that dismisses and verifies the customer is *still there*, and (c) an assertion that the message names the right customer id. Test (b) is the one that catches the nastiest regression: a developer refactors the handler and accidentally deletes regardless of the answer.

**Scenario 2: "Reason for cancellation" prompt.** A booking system calls `prompt("Why are you cancelling?")` before cancelling a reservation. Your tests check that typed text appears in the audit log, that pressing Cancel aborts the cancellation, and that an empty reason is either rejected or stored as designed.

**Scenario 3: Form-level success alert.** After submitting a registration form, a legacy application shows `alert("Registration successful")`. If your test does nothing, Playwright auto-dismisses it and the flow continues; but a good test records the message and asserts it, because the text *is* the user-visible confirmation.

**Scenario 4: Cookie banner and newsletter pop-up in an e-commerce flow.** These are in-page overlays. They often appear after a random delay and cover the buttons your test needs. You handle them with locators (e.g. click "Accept all" if visible). Treating them as dialogs and waiting for a `dialog` event would never succeed. This scenario is also why distinguishing the categories in Section 10 pays off.

**Scenario 5: Unsaved-changes protection.** A long application form warns the user if they navigate away. Your test types into the form, triggers navigation, and verifies the warning appears (type `beforeunload`), then checks that staying keeps the typed values.

---

## Common Pitfalls and Best Practices

1. **Registering the handler too late.** The listener must exist *before* the click. Put the `page.once(...)` line immediately above the line that triggers the dialog, so the pairing is obvious to the next reader.

2. **A handler that does not always answer.** With a listener registered, Playwright no longer auto-dismisses. This code is a trap:

   ```python
   def handler(dialog):
       if dialog.type == "confirm":
           dialog.accept()
   ```

   If an `alert` appears, nobody answers and the page freezes. Always make sure every code path calls `accept()` or `dismiss()`, for example by adding an `else: dialog.dismiss()`.

3. **Forgetting that "no handler" means "Cancel".** If your test clicks "Delete" without a handler and then asserts the row disappeared, it will fail because Playwright pressed Cancel. When you see a confirm in a flow, always decide the answer explicitly.

4. **Using `on` and never removing it.** A leftover `on` listener from step 3 will silently answer a dialog in step 9 that you *wanted* to see fail. Prefer `once`, or pair `on` with `remove_listener`.

5. **Asserting immediately after the click without waiting.** Use `expect(...)` on an observable outcome (the result text, a row disappearing) so Playwright retries until the page has updated. Do not use `time.sleep()`.

6. **Asserting inside the handler.** A failing assertion before `accept()` leaves the dialog open. Record, answer, then assert.

7. **Treating HTML modals as dialogs.** Check with DevTools. If it is in the DOM, use locators.

8. **Testing only the happy answer.** Always test Cancel for destructive confirmations.

9. **Hard-coding fragile message text.** If the wording is likely to change often, use `in` or a regular expression (`re.search`) on `dialog.message`, or assert only the important part (the customer id).

10. **Registering listeners on the wrong page object.** The `dialog` event belongs to a single `Page`. If your test opens a new tab (see Tuesday's lesson), it needs its own listener. A context-level listener (`context.on("dialog", ...)`) exists for more advanced use; for now keep it per page.

**Best-practice checklist:** one `once` handler per expected dialog; handler answers on every path; assert the dialog's `type` and `message`; verify the *outcome* on the page with `expect`; test accept and cancel; keep handlers short.

---

## Mini Practice Exercises

**Exercise 1 (warm-up).** On `https://the-internet.herokuapp.com/javascript_alerts`, write a test that clicks "Click for JS Alert", accepts it, and asserts the result text. Then change the test so it also verifies that `dialog.type` is `"alert"` and the message is `"I am a JS Alert"`.

*Hint:* use the record-then-answer pattern from Example 4.

**Exercise 2 (both branches).** Write one parametrised test for the confirm dialog that covers OK and Cancel, using `if/else` instead of `getattr` for readability.

*Solution sketch:*

```python
@pytest.mark.parametrize("accept, expected", [(True, "You clicked: Ok"), (False, "You clicked: Cancel")])
def test_confirm(page, accept, expected):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    def handler(dialog):
        if accept:
            dialog.accept()
        else:
            dialog.dismiss()

    page.once("dialog", handler)
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(page.locator("#result")).to_have_text(expected)
```

**Exercise 3 (prompt edge cases).** Test the prompt with three inputs: normal text, an empty string, and Cancel. Predict the result text for each before running. (*Hint:* an empty string accepted by OK yields `You entered: ` with nothing after it, while Cancel yields `You entered: null`. Run it and compare to your prediction. Consider how you would assert on text that may have trailing whitespace; `to_have_text` normalises whitespace.)

**Exercise 4 (default value).** Using `page.set_content`, create a page with a button that calls `prompt("Name?", "Guest")` and writes the result into a `<p id="out">`. Write a test that (a) calls `dialog.accept()` with no argument and asserts the output is `Guest`, and (b) asserts `dialog.default_value == "Guest"`.

*Solution:*

```python
def test_prompt_default(page):
    page.set_content("""
      <button id="b">Ask</button><p id="out"></p>
      <script>b.onclick = () => { out.textContent = prompt('Name?', 'Guest'); }</script>
    """)
    defaults = []

    def handler(dialog):
        defaults.append(dialog.default_value)
        dialog.accept()

    page.once("dialog", handler)
    page.get_by_role("button", name="Ask").click()
    expect(page.locator("#out")).to_have_text("Guest")
    assert defaults == ["Guest"]
```

**Exercise 5 (spot the category).** For each of the following, say which technique you would use: (a) a Bootstrap "Are you sure?" overlay, (b) `window.alert()` after saving, (c) "Allow camera?", (d) a login box from Basic Auth, (e) a link that opens a new window. *Answers:* (a) locators + expect, (b) `page.once("dialog")`, (c) context permissions, (d) `http_credentials`, (e) `expect_popup` (Tuesday).

**Exercise 6 (challenge).** Build the unsaved-changes example (Example 7) and write two tests: one that dismisses the dialog and asserts the page is still open, and one that accepts and asserts `page.is_closed()`.

---

## Summary / Key Takeaways

- Native dialogs (`alert`, `confirm`, `prompt`, `beforeunload`) are drawn by the browser, are modal, and **block** the page until answered.
- With **no** listener, Playwright auto-dismisses dialogs (answers Cancel). With **any** listener, **you** must answer every dialog or the test hangs.
- Register the handler **before** the triggering action. Use `page.once("dialog", ...)` for a single expected dialog and `page.on(...)` for persistent behaviour (and remove it when done).
- The `Dialog` object gives `type`, `message`, `default_value`, `accept(prompt_text)` and `dismiss()`.
- For prompts, `accept("text")` types text; `dismiss()` yields `null`. Test both.
- Record details inside the handler, answer immediately, and assert afterwards using `expect` on the page's visible outcome.
- In-page modals, new windows, permission prompts, and HTTP auth boxes are **not** dialogs; each has its own technique.
- This skill is a building block for the Project 1 UI milestone: confirmations are everywhere in real forms.

---

## External Resources

- Playwright for Python, Dialogs: https://playwright.dev/python/docs/dialogs
- Playwright for Python API reference, `Dialog` class: https://playwright.dev/python/docs/api/class-dialog
- MDN Web Docs, `Window.alert()`, `confirm()` and `prompt()`: https://developer.mozilla.org/en-US/docs/Web/API/Window/alert
