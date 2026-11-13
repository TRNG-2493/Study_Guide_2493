# 06 — Events, Frames and Windows

> **Before you start**
>
> - **By the end you can:** handle alerts, confirms and prompts; work inside frames; work with Shadow DOM; follow navigation and listen to page events; handle new tabs and pop-ups; upload and download files.
> - **Practice site:** The Internet — <https://the-internet.herokuapp.com/>
> - **Create:** a folder `lecture06/` with `pytest.ini`:
>
> ```ini
> [pytest]
> base_url = https://the-internet.herokuapp.com
> ```
>
> and `test_events.py` starting with:
>
> ```python
> import re
> from playwright.sync_api import Page, expect
> ```
>
> - **Run tests with:** `pytest -s` (add `--headed` to watch)
>
> **One idea for the whole lecture — listen *before* you act:**
>
> | Pattern | Used for | Shape |
> |---|---|---|
> | Listener `page.on(...)` | Things that can happen any time (dialogs, errors) | Register **before** the action |
> | Expect block `with page.expect_...() as info:` | One thing you're waiting for (tab, download) | Do the action **inside** the `with`, then use `info.value` |

---

## Topic 1 — Alerts and dialogs

### Definition

Browsers have three built-in dialog boxes: `alert` (OK), `confirm` (OK/Cancel) and `prompt` (text box + OK/Cancel). They aren't part of the page, so you can't locate them — you handle them with a `"dialog"` listener.

### Key ideas

- **By default Playwright clicks Cancel** on every dialog.
- `page.once("dialog", handler)` handles only the **next** dialog; `page.on(...)` handles **every** one.

| Method / property | Meaning |
|---|---|
| `dialog.accept()` / `dialog.accept("text")` | OK / type into a prompt, then OK |
| `dialog.dismiss()` | Cancel |
| `dialog.message`, `dialog.type`, `dialog.default_value` | Text, kind, prompt's pre-filled text |

### Worked example — confirm, then check an alert's message

**Step 1.** See the default behaviour on a confirm:

```python
def test_confirm(page: Page):
    page.goto("/javascript_alerts")
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(page.locator("#result")).to_have_text("You clicked: Cancel")
```

**Step 2.** Now accept it — register the handler **before** clicking:

```python
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(page.locator("#result")).to_have_text("You clicked: Ok")
```

**Step 3.** A new test that records the alert's message with a normal function:

```python
def test_alert_message(page: Page):
    page.goto("/javascript_alerts")
    messages = []

    def handle(dialog):
        messages.append(dialog.message)
        dialog.accept()
```

**Step 4.** Register it, click, check:

```python
    page.once("dialog", handle)
    page.get_by_role("button", name="Click for JS Alert").click()
    assert messages == ["I am a JS Alert"]
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")
```

> **Predict:** what happens if you move `page.once(...)` in Step 2 to **after** the click?

### Checkpoint

`2 passed`.

### Your turn

1. Accept the **JS Prompt** with the text `Playwright` and check the result says "You entered: Playwright".
2. Leave the prompt unhandled. What does the result say?
   *Hint: Cancel on a prompt returns `null`.*
3. Write a handler that only prints the message (no accept/dismiss). What happens?

### Common errors

| Error | Fix |
|---|---|
| Handler never runs | Register it **before** the click |
| Click times out, page frozen | The handler must call `accept()` or `dismiss()` |

---

## Topic 2 — Frames and nested frames

### Definition

A frame (`<iframe>` or `<frame>`) is a **separate web page inside the page** — payment forms, maps, chat widgets, rich-text editors. Locators on `page` can't see inside it; `frame_locator()` steps into the frame and returns something you can locate on as usual.

### Key ideas

- `page.frame_locator("frame[name='frame-top']")` — takes a CSS selector for the frame element.
- Best selectors: `title`, then `name`, then id, then plain `iframe` if there's only one.
- Nested frames: chain `.frame_locator(...)` again.
- From an existing locator: `page.locator("#mce_0_ifr").content_frame`.

### Worked example — read the middle of the nested frames

**Step 1.** Show that `page` can't see inside:

```python
def test_nested_frames(page: Page):
    page.goto("/nested_frames")
    expect(page.get_by_text("MIDDLE")).to_have_count(0)
```

**Step 2.** Step into the top frame:

```python
    top = page.frame_locator("frame[name='frame-top']")
```

**Step 3.** Then into the middle frame inside it:

```python
    middle = top.frame_locator("frame[name='frame-middle']")
    expect(middle.locator("#content")).to_have_text("MIDDLE")
```

**Step 4.** The bottom frame is directly under the page:

```python
    bottom = page.frame_locator("frame[name='frame-bottom']")
    expect(bottom.locator("body")).to_contain_text("BOTTOM")
```

> **Predict:** how many items are in `page.frames` on this page?

### Checkpoint

`1 passed`. Print `len(page.frames)` to confirm your prediction.

### Your turn

1. Read the **LEFT** and **RIGHT** frames the same way.
2. On `/iframe`, read the editor's text inside the frame with id `mce_0_ifr`.
   *Hint: the text is inside `#tinymce`. Check the id in DevTools if it fails.*
3. Try `page.frame_locator("frame[name='frame-middle']")` directly from `page`. Why does it find nothing?

### Common errors

| Error | Fix |
|---|---|
| Locator finds nothing for text you can see | It's inside a frame; use `frame_locator` |
| Nested frame not found | Chain from the **outer** frame |

---

## Topic 3 — Shadow DOM

### Definition

**Shadow DOM** hides a component's inner HTML from the rest of the page (you see `#shadow-root` in DevTools). Playwright's built-in locators and CSS selectors look inside **open** shadow roots automatically.

### Key ideas

- Nothing special needed for `get_by_role`, `get_by_text` or CSS.
- **XPath does not** cross into shadow roots.
- **Closed** shadow roots can't be reached (rare).

### Worked example — find paragraphs inside web components

**Step 1.** Open the page:

```python
def test_shadow_dom(page: Page):
    page.goto("/shadowdom")
```

**Step 2.** Each `<my-paragraph>` has a `<p>` **inside its shadow root**. CSS finds them:

```python
    expect(page.locator("my-paragraph p")).to_have_count(2)
```

**Step 3.** Try XPath:

```python
    expect(page.locator("//my-paragraph//p")).to_have_count(0)
```

**Step 4.** Built-in locators work too:

```python
    expect(page.get_by_text("In a list!")).to_be_visible()
```

> **Predict:** will Step 3 pass? What does that tell you about XPath?

### Checkpoint

`1 passed` — XPath found zero paragraphs, CSS found two.

### Your turn

1. Open DevTools on `/shadowdom` and find a `#shadow-root`. Is it open or closed?
2. How many elements does `page.get_by_text("Let's have some different text!")` match? Why?

---

## Topic 4 — Navigation and page events

### Definition

Navigation is moving between pages — by clicking links, browser buttons or redirects. Page **events** (errors, console messages, network responses) can be captured with the same `page.on(...)` listener pattern used for dialogs.

### Key ideas

- After clicking a link, check with `expect(page).to_have_url(...)`.
- `page.go_back()`, `go_forward()`, `reload()`.
- For navigation that happens **later**: `page.wait_for_url("**/status_codes")`.
- Glob: `**` = anything incl. `/`; `*` = anything except `/`.

| Event | Fires when |
|---|---|
| `"pageerror"` | An uncaught JavaScript error |
| `"console"` | The page writes to the console |
| `"request"` / `"response"` | A network request / answer |

### Worked example — follow a redirect, go back, catch an error

**Step 1.** Follow the redirect link:

```python
def test_navigation(page: Page):
    page.goto("/redirector")
    page.get_by_role("link", name="here").click()
    page.wait_for_url("**/status_codes")
    expect(page.get_by_role("heading", name="Status Codes")).to_be_visible()
```

**Step 2.** Go back:

```python
    page.go_back()
    expect(page).to_have_url(re.compile("redirector"))
```

**Step 3.** A new test: listen for JavaScript errors **before** opening the page:

```python
def test_page_error(page: Page):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto("/javascript_error")
```

**Step 4.** Check it was caught:

```python
    print(errors)
    assert len(errors) == 1
```

### Checkpoint

`2 passed`, and the printed list contains one error message from the page.

### Your turn

1. After going back in Step 2, call `page.go_forward()` and check the URL.
2. On `/status_codes`, record every response with `page.on("response", ...)`, click **404**, and check one recorded response has `status == 404`.
   *Hint: `lambda r: statuses.append(r.status)`.*
3. Move Step 3's `page.on(...)` to **after** `goto`. What happens to the test?

---

## Topic 5 — New tabs and pop-ups

### Definition

A `target="_blank"` link or a `window.open()` call creates a **new page**. Your `page` still points at the original tab, so you catch the new page with `page.expect_popup()` (or `context.expect_page()`) and use it through its own variable.

### Key ideas

- Click **inside** the `with` block; get the new page from `info.value`.
- **No switching** like Selenium — just use the right variable.
- `context.pages` lists every open page; `new_page.close()` closes one.

### Worked example — open a new window

**Step 1.** Catch the pop-up:

```python
def test_new_window(page: Page):
    page.goto("/windows")
    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Click Here").click()
```

**Step 2.** Get the new page and check it:

```python
    new_window = popup_info.value
    expect(new_window).to_have_title("New Window")
    expect(new_window.get_by_role("heading")).to_have_text("New Window")
```

**Step 3.** The original page is unchanged:

```python
    expect(page.get_by_role("heading", name="Opening a new window")).to_be_visible()
```

**Step 4.** Close the pop-up:

```python
    new_window.close()
    assert len(page.context.pages) == 1
```

> **Predict:** before Step 4, how many pages does `page.context.pages` contain?

### Checkpoint

`1 passed`.

### Your turn

1. Rewrite the test using `context.expect_page()`.
   *Hint: ask for the `context` fixture too.*
2. Open the new window **twice** and print `len(context.pages)`.
3. What goes wrong if you click the link **outside** the `with` block?

### Common errors

| Error | Fix |
|---|---|
| Checks run on the old tab | Use the new page from `info.value` |
| Timeout waiting for popup | The click must be **inside** the `with` block |

---

## Topic 6 — File upload and download

### Definition

**Upload:** `set_input_files()` sets a file on an `<input type="file">` without opening a file dialog. **Download:** `page.expect_download()` catches a download so you can save it and check it.

### Key ideas

| Task | Code |
|---|---|
| One / several files | `set_input_files(path)` / `set_input_files([a, b])` |
| Clear | `set_input_files([])` |
| Hidden input with a styled button | `with page.expect_file_chooser() as info:` |
| Download | `with page.expect_download() as info:` → `info.value.save_as(path)` |

- `tmp_path` (built into pytest) gives each test its own empty temporary folder.
- Never hard-code `C:\Users\...` paths.

### Worked example — upload a file, download a file

**Step 1.** Create a file in `tmp_path` and upload it:

```python
def test_upload(page: Page, tmp_path):
    notes = tmp_path / "my-notes.txt"
    notes.write_text("Uploaded by Playwright")
    page.goto("/upload")
    page.locator("#file-upload").set_input_files(notes)
    page.get_by_role("button", name="Upload").click()
```

**Step 2.** Check the result page:

```python
    expect(page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
    expect(page.locator("#uploaded-files")).to_contain_text("my-notes.txt")
```

**Step 3.** Download the first file on the download page:

```python
def test_download(page: Page, tmp_path):
    page.goto("/download")
    first_link = page.locator("#content a").first
    link_text = first_link.text_content()
    with page.expect_download() as download_info:
        first_link.click()
    download = download_info.value
```

**Step 4.** Save it and check it:

```python
    assert download.suggested_filename == link_text
    saved = tmp_path / download.suggested_filename
    download.save_as(saved)
    assert saved.exists() and saved.stat().st_size > 0
```

> **Predict:** why do we read the link text instead of hard-coding a file name? (Look at the page — the list changes as people upload files.)

### Checkpoint

`2 passed`.

### Your turn

1. Upload a file created **in memory**: `{"name": "hello.txt", "mimeType": "text/plain", "buffer": b"Hello"}`.
2. On `/upload`, use `expect_file_chooser()` by clicking the file input, then `chooser_info.value.set_files(...)`.
3. Download the link named `sample.csv` (if it's listed) and print its rows with `csv.reader`.

### Common errors

| Error | Fix |
|---|---|
| Can't get at the downloaded file | Wrap the click in `expect_download()` |
| Test works only on your laptop | Use `tmp_path` or relative paths |
| `set_input_files` fails on a button | It's not a file input; use `expect_file_chooser()` |

---

## Stretch challenge

In one test: accept a confirm, enter text in a prompt, read all four nested frames into a list (`["LEFT", "MIDDLE", "RIGHT", "BOTTOM"]`), open and close the new window, and upload two files at once to `/upload` — then check what the page reports.

## Exit ticket

1. What does "listen before you act" mean? Give one listener and one expect-block example.
2. Why can't `page.get_by_text("MIDDLE")` find the text in the nested frames?
3. What does Playwright do with a dialog if you don't handle it?

## Cheat sheet

| Code | Purpose |
|---|---|
| `page.once("dialog", lambda d: d.accept())` | Accept the next dialog |
| `d.accept("text")` / `d.dismiss()` / `d.message` | Prompt / cancel / read text |
| `page.frame_locator("frame[name='x']")` | Step into a frame |
| `.frame_locator(...).frame_locator(...)` | Nested frames |
| `locator.content_frame` | Frame from a frame locator |
| Built-in locators / CSS | Work in open Shadow DOM (XPath doesn't) |
| `expect(page).to_have_url(re.compile(...))` | Check URL |
| `page.wait_for_url("**/path")` | Wait for later navigation |
| `page.go_back()` / `go_forward()` / `reload()` | Browser buttons |
| `page.on("pageerror", handler)` | Capture JavaScript errors |
| `with page.expect_popup() as info:` | Catch a new tab / window |
| `set_input_files(path)` | Upload |
| `with page.expect_file_chooser() as info:` | Hidden file input |
| `with page.expect_download() as info:` → `save_as()` | Download |
| `tmp_path` | Per-test temp folder |
