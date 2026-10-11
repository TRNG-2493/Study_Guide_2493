# File Upload and Download

## Learning Objectives

By the end of this lesson you will be able to:

- Explain how a browser file upload works (`<input type="file">`, the OS file chooser, `multipart/form-data`) and how Playwright automates it without touching the operating system dialog.
- Upload one file, several files, and a whole directory using `locator.set_input_files()`, and clear a selection.
- Upload "virtual" files created in memory (name, MIME type, bytes) so tests do not depend on files lying around on disk.
- Handle upload buttons whose `<input type="file">` is hidden by using `page.expect_file_chooser()`.
- Handle drag-and-drop upload zones and understand the limits.
- Verify uploads: file name displayed, preview, validation errors (wrong type, too large), and server-side confirmation.
- Download files with `page.expect_download()`, and use the `Download` object: `suggested_filename`, `save_as()`, `path()`, `failure()`, `url`, `delete()`.
- Verify downloaded content: file name, size, CSV rows, JSON, and (with Python libraries) PDF or Excel basics.
- Handle downloads that open in a new tab, are triggered by JavaScript, or are inline (PDF viewer) rather than attachments.
- Use pytest-style temporary directories (`tmp_path`) and Python's `pathlib` so your tests are clean and portable.
- Avoid pitfalls: hard-coded absolute paths, race conditions, leftover files, and trying to click the native OS dialog.

---

## Why This Matters

File transfer is a standard feature of business applications: uploading a CV to a job portal, importing customers from a CSV file, attaching evidence to a support ticket, exporting a report to Excel, downloading an invoice as a PDF. In many systems, these are the *highest-risk* features: they involve parsing untrusted data, size limits, security filters, and integrations with storage and email systems. They are also where users complain loudly when something breaks ("the export is empty", "my upload hangs").

Automating them is a classic stumbling block for beginners because the *native file chooser dialog* of the operating system is outside the web page, and tools that drive the page cannot click on it. Playwright solves this elegantly: it never opens the OS dialog. Instead it sets the files directly on the input element (for uploads) and intercepts the download event (for downloads). Once you understand the two patterns, `set_input_files` and `expect_download`, you can test any of these features.

This lesson brings together several ideas from earlier today and from Monday: the **register first, then act** pattern (as with popups, responses, and navigation), **auto-waiting** and assertions (for upload progress and result messages), and the **form controls** you learned on Monday (an upload is a form control too). For **Project 1 - QE Foundations**, a realistic UI test suite should include at least one import/export flow, because it demonstrates end-to-end verification (UI action, file result, data check).

---

## The Concept

### 1. How file upload works in a browser

The HTML for a standard file upload is:

```html
<form action="/upload" method="post" enctype="multipart/form-data">
  <label for="doc">Choose a document</label>
  <input type="file" id="doc" name="doc" accept=".pdf,.png" multiple>
  <button type="submit">Upload</button>
</form>
```

- `type="file"` creates a control which, when activated, opens the operating system's file chooser.
- `accept=".pdf,.png"` is a *hint* (it filters the dialog and is used by some validation) but is not a security control; the server must validate again.
- `multiple` allows selecting more than one file.
- `webkitdirectory` (a non-standard but widely supported attribute) allows choosing a whole folder.
- `enctype="multipart/form-data"` tells the browser to encode the form as multiple parts, which is how binary file content travels in a POST request.
- Modern applications often upload in the background using JavaScript (`fetch` with `FormData`) and show a progress bar.

Many sites hide the real input and show a styled button instead:

```html
<button id="pick">Upload file</button>
<input type="file" id="hidden" hidden>
<script>document.getElementById('pick').onclick = () => document.getElementById('hidden').click();</script>
```

Clicking the button programmatically clicks the hidden input, which opens the file chooser. Two Playwright techniques cover the two situations:

| Situation | Technique |
| --- | --- |
| The `<input type="file">` is in the DOM (even hidden) | `locator.set_input_files(...)` directly on the input |
| Only a button is visible and the input is created on demand | `with page.expect_file_chooser() as fc: click` then `fc.value.set_files(...)` |

### 2. `set_input_files`: the primary technique

```python
page.locator("input[type=file]").set_input_files("data/resume.pdf")
```

What it does:

1. Finds the `<input type="file">` element.
2. Assigns the file(s) to the input's `files` list *as if the user had chosen them in the dialog*.
3. Dispatches the `input` and `change` events, so the application reacts.

Key points:

- It works even when the input is **hidden** (`display: none`); it does not require visibility because it does not click. (It *does* require the element to be an `<input type="file">`, or a `<label>` associated with one.)
- The path is relative to the **current working directory** of your Python process (or absolute). To make tests portable, build paths from the test file's location with `pathlib`:

```python
from pathlib import Path
DATA = Path(__file__).parent / "data"
page.locator("input[type=file]").set_input_files(DATA / "resume.pdf")
```

`Path(__file__)` is the path of the current Python file; `.parent` is its folder; the `/` operator joins path parts. `set_input_files` accepts `str`, `pathlib.Path`, or lists of them.

- **Several files:** pass a list: `set_input_files([DATA / "a.png", DATA / "b.png"])`. The input needs the `multiple` attribute; otherwise Playwright raises an error ("Non-multiple file input can only accept single file").
- **Clear the selection:** `set_input_files([])`.
- **Directory:** pass the directory path to an input with `webkitdirectory`: `set_input_files(DATA / "photos")`. Playwright uploads the folder's files with their relative paths.

### 3. In-memory (virtual) files

Maintaining test files on disk is sometimes inconvenient: large files in the repository, or file contents that must vary per test. Playwright accepts a dictionary describing a file:

```python
page.locator("input[type=file]").set_input_files(
    files={
        "name": "customers.csv",
        "mimeType": "text/csv",
        "buffer": b"id,name\n1,Maria\n2,John\n",
    }
)
```

- `name`: the filename the application will see.
- `mimeType`: the content type.
- `buffer`: the bytes (a Python `bytes` object, note the `b"..."` prefix; strings must be encoded: `"text".encode("utf-8")`).

You can pass a list of such dictionaries for multiple files. This is perfect for generating a CSV with exactly the rows required by a test, or a tiny valid PNG, or a deliberately invalid file for negative tests, without creating files on disk.

### 4. `expect_file_chooser`

When the input is not available (it is created dynamically when the button is clicked, or you simply want to drive the exact user path), listen for the **file chooser event**:

```python
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="Upload file").click()
file_chooser = fc_info.value
file_chooser.set_files(DATA / "resume.pdf")
```

- Again the "register first, then act" idiom.
- `FileChooser` has `set_files(...)` (same arguments as `set_input_files`), `is_multiple()`, `element` (the input element handle), and `page`.
- Playwright suppresses the native dialog. In headless and headed mode, no OS window will appear while a file chooser listener is registered.

Without a registered handler, clicking a button that opens a file chooser simply leaves a pending chooser that is cancelled; the test would then see nothing happen. Do not try to type a file path into a native dialog with OS-level tools; it is unnecessary and fragile.

### 5. Drag-and-drop upload zones

Drop zones often wrap a hidden `<input type="file">` too. Always check the DOM first: if there is a file input anywhere (even hidden), `set_input_files` on it usually triggers the same handler as a drop. If the zone only listens for `drop` events and has no input, you can simulate a drop by constructing a `DataTransfer` in the page:

```python
buffer = Path("data/photo.png").read_bytes()
data_transfer = page.evaluate_handle("""async ({ name, type, bytes }) => {
    const dt = new DataTransfer();
    const file = new File([new Uint8Array(bytes)], name, { type });
    dt.items.add(file);
    return dt;
}""", {"name": "photo.png", "type": "image/png", "bytes": list(buffer)})

page.locator("#dropzone").dispatch_event("drop", {"dataTransfer": data_transfer})
```

This is an advanced technique. For large files, passing bytes through `evaluate_handle` is slow because the content is serialised as JSON; for test purposes small files are enough. A frequently simpler alternative is `set_input_files` on the hidden input. (Playwright also exposes `locator.drag_to` and mouse actions, introduced on Monday, but those cannot drag from the operating system.)

### 6. Verifying an upload

Uploading is only half of the test; confirm the application's reaction. Common checks:

- **File name appears** in the UI: `expect(page.get_by_text("resume.pdf")).to_be_visible()`.
- **Preview/thumbnail** appears: `expect(page.locator("img.preview")).to_be_visible()`.
- **Progress completes**: `expect(page.get_by_role("progressbar")).to_have_attribute("aria-valuenow", "100")`, or wait for a "Upload complete" message.
- **Validation errors**: wrong type ("Only PDF or PNG allowed"), too large ("Max size 5 MB"), empty file, duplicate file name.
- **Server confirmation**: the upload endpoint responded 200/201 (`page.expect_response("**/upload")`), and the file shows up in a list after reload.
- **Input state** (client-side): `expect(locator).to_have_value(...)` is not reliable for file inputs (browsers expose `C:\fakepath\name`); instead, read the files via JavaScript if you must:

```python
names = page.locator("input[type=file]").evaluate("el => Array.from(el.files).map(f => f.name)")
```

### 7. Download basics

A **download** begins when the browser receives a response that it should save rather than display: typically `Content-Disposition: attachment; filename="report.csv"`, or a link with the `download` attribute (`<a href="/files/report.csv" download>`), or a JavaScript-generated `Blob` URL.

Playwright's pattern:

```python
with page.expect_download() as download_info:
    page.get_by_role("button", name="Export CSV").click()
download = download_info.value
```

Then use the `Download` object:

| Member | Meaning |
| --- | --- |
| `download.suggested_filename` | The filename the browser would use (from `Content-Disposition` or the `download` attribute) |
| `download.url` | The URL the file came from |
| `download.save_as(path)` | Copy the downloaded file to a path of your choice; waits for the download to finish |
| `download.path()` | Path of the downloaded file in Playwright's temporary location; waits for completion |
| `download.failure()` | `None` if successful, otherwise an error string (e.g. `"canceled"`) |
| `download.cancel()` | Cancel an in-progress download |
| `download.delete()` | Delete the temporary file |
| `download.page` | The page that initiated the download |

Playwright's contexts accept downloads by default (`accept_downloads=True` is the default in current versions). Files are stored in a temporary directory that is deleted when the browser context closes, so **copy anything you want to keep with `save_as`**.

A recommended approach for tests is to save into a controlled folder with the suggested filename:

```python
dest = tmp_path / download.suggested_filename
download.save_as(dest)
assert dest.exists() and dest.stat().st_size > 0
```

### 8. Verifying downloaded content

Checking that *a* file was downloaded is not enough; check that it contains the correct data.

**Filename and size**

```python
assert download.suggested_filename == "orders-2025-03.csv"
assert dest.stat().st_size > 0
```

**CSV** using Python's built-in `csv` module:

```python
import csv
with dest.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
assert rows[0]["Name"] == "Maria"
assert len(rows) == 3
```

`csv.DictReader` yields each row as a dictionary keyed by the header row. `newline=""` is required by the csv module to handle line endings correctly. Compare with the UI: for example, the number of rows in the downloaded CSV should equal the number of rows in the on-screen table (reuse Web Tables techniques).

**JSON**

```python
import json
data = json.loads(dest.read_text(encoding="utf-8"))
assert data["total"] == 3
```

**Text files / logs:** `dest.read_text()`.

**PDF:** use a library such as `pypdf` (`pip install pypdf`):

```python
from pypdf import PdfReader
reader = PdfReader(dest)
text = reader.pages[0].extract_text()
assert "Invoice #1042" in text
```

**Excel (.xlsx):** use `openpyxl` (`pip install openpyxl`):

```python
from openpyxl import load_workbook
ws = load_workbook(dest).active
assert ws["A1"].value == "Name"
```

Note that Playwright itself does not parse these formats; you choose the right Python library. Keep such parsing in helper functions.

**Binary files / checksums:** `hashlib.sha256(dest.read_bytes()).hexdigest()` compares to a known hash for fixed content.

### 9. Special download situations

- **Download opens in a new tab.** A link with `target="_blank"` that points to an attachment may open a tab and immediately download. The download event is on the *original* page (or the popup). If `page.expect_download()` times out, the download event may have been raised on the new page instead. Capture the new tab first (see the Multiple Tabs and Windows lesson), then wait for the download on it: `with new_page.expect_download() as info:`. If the tab opens and starts the download so quickly that you cannot attach a listener in time, register `page.on("download", handler)` on the original page before clicking, so no event is missed.
- **Inline viewing instead of download.** If the server sends `Content-Disposition: inline` or a PDF with a normal content-type, Chromium may open the built-in PDF viewer instead of downloading. In that case there is no download event. Either configure the server to send `attachment`, or fetch the file directly with the API request client:

```python
response = page.request.get("https://example.com/files/invoice.pdf")
assert response.ok
pdf_bytes = response.body()
```

`page.request` shares cookies with the page, so authenticated downloads work.
- **JavaScript-generated downloads.** Apps that create a `Blob` and click a temporary link trigger a standard download event; `expect_download` works the same.
- **Slow generation.** Reports that take 20 seconds to prepare need a longer timeout: `page.expect_download(timeout=60_000)`.
- **Multiple downloads.** Use one `expect_download` per click, or attach `page.on("download", handler)` to collect them.
- **Headless vs headed.** Downloads work in both. Browser dialogs such as "Save as..." do not appear.
- **Cancelled / failed downloads.** `download.failure()` returns a non-`None` string when the download did not complete.

### 10. Tools for temporary files

When tests create files (uploads) or save files (downloads), avoid polluting your repository:

- Python's `tempfile.TemporaryDirectory()` for general scripts.
- With pytest (which we use for test suites and cover in depth on Wednesday), the built-in `tmp_path` fixture provides a unique empty `pathlib.Path` directory per test. For now, treat `tmp_path` as "a fresh temporary folder".
- Never hard-code absolute paths such as `C:\Users\me\Downloads\file.csv`. They break on other machines and on CI servers.

### 11. Security and test-data considerations

- Use **synthetic data** in test files. Never upload real customer data.
- For upload validation tests, create small files that *claim* to be one type but are another (an `.exe` renamed `.pdf`) to see how the server reacts; coordinate with your team, and only in test environments.
- Do not assume `accept` attributes are enforced: `set_input_files` can set any file regardless of `accept`, just as a malicious client could. If the server accepts a disallowed file, that is a real defect.
- Test large files carefully. Uploading a 1 GB file in a UI test is slow; test limits using the smallest file that crosses the threshold, or mock the size validation layer.

---

## Code Examples

We use a tiny local web server (Python standard library only) so the examples are runnable. A real server is used, rather than `page.route()` mocking, because downloads triggered by a mocked response are not delivered reliably; a real `Content-Disposition` header from a real server behaves exactly like production. The site has a normal upload form, a hidden-input upload button, and two download links.

### The test site and server

```python
from pathlib import Path
import csv, io, json
from playwright.sync_api import sync_playwright, expect

HOME = """
<title>Files</title>
<h1>File demo</h1>

<h2>Upload (visible input)</h2>
<label>Documents <input id="docs" type="file" multiple accept=".txt,.csv"></label>
<ul id="list"></ul>

<h2>Upload (button + hidden input)</h2>
<button id="pick">Choose avatar</button>
<p id="avatar-name"></p>

<h2>Download</h2>
<a id="csv" href="/export.csv" download>Download CSV</a>
<button id="gen">Generate report</button>

<script>
  // 1) show the chosen files
  document.getElementById('docs').addEventListener('change', e => {
    const list = document.getElementById('list');
    list.innerHTML = '';
    for (const f of e.target.files) {
      const li = document.createElement('li');
      li.textContent = f.name + ' (' + f.size + ' bytes)';
      list.appendChild(li);
    }
  });

  // 2) hidden input created on demand
  document.getElementById('pick').onclick = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = () => {
      document.getElementById('avatar-name').textContent = input.files[0].name;
    };
    input.click();
  };

  // 3) JavaScript-generated download
  document.getElementById('gen').onclick = () => {
    const blob = new Blob(['id,name\\n1,Maria\\n2,John\\n'], { type: 'text/csv' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'report.csv';
    a.click();
  };
</script>
"""

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body, ctype, extra = HOME.encode("utf-8"), "text/html; charset=utf-8", {}
        elif self.path == "/export.csv":
            body = b"id,name,total\n1,Maria,10.50\n2,John,20.00\n3,Ann,5.25\n"
            ctype = "text/csv"
            extra = {"Content-Disposition": 'attachment; filename="orders.csv"'}
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        for name, value in extra.items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 0), Handler)          # port 0 = any free port
BASE = f"http://127.0.0.1:{server.server_address[1]}"
threading.Thread(target=server.serve_forever, daemon=True).start()
```

**Explanation**

- The first section is a *visible* multiple-file input with an `accept` hint and a change listener that lists names and sizes.
- The second creates an `<input type="file">` in JavaScript *only when the button is clicked*; at test start the input does not exist, so `set_input_files` on a locator is impossible. This is the case for `expect_file_chooser`.
- The third demonstrates both kinds of download: a normal link (`/export.csv`, served with `Content-Disposition: attachment`) and a JavaScript Blob download. In the Python string, `\\n` becomes `\n` inside the JavaScript string literal, i.e. a newline character in the CSV.
- `Handler.do_GET` serves the page at `/` and the CSV at `/export.csv`. The `Content-Disposition: attachment; filename="orders.csv"` header is what makes the browser download the file instead of displaying it, and it supplies the suggested filename.
- `HTTPServer(("127.0.0.1", 0), Handler)` listens on the local machine on a free port chosen by the operating system; the address is stored in `BASE`. `serve_forever` runs in a daemon thread so the server stops when the script ends.

### Example 1: Upload a file from disk (visible input)

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE + "/")

    # Create a temporary file for the test
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        note = Path(tmp) / "note.txt"
        note.write_text("hello upload", encoding="utf-8")

        page.get_by_label("Documents").set_input_files(note)
        expect(page.locator("#list li")).to_have_text(["note.txt (12 bytes)"])

    browser.close()
```

**Line-by-line**

- `tempfile.TemporaryDirectory()` creates a unique folder that is deleted when the `with` block ends. We never leave files behind.
- `Path(tmp) / "note.txt"`: builds the file path. `write_text` writes the string; "hello upload" is 12 characters, hence 12 bytes in UTF-8.
- `page.get_by_label("Documents")`: finds the input through its wrapping `<label>`. Using `get_by_label` follows the user-facing locator advice.
- `.set_input_files(note)`: assigns the file; the page's `change` listener fires.
- `expect(...).to_have_text(["note.txt (12 bytes)"])`: a list assertion on all matched `li` elements: exactly one item with that text. This proves both the name and that the size was read correctly.

### Example 2: Multiple files, in-memory files, and clearing

```python
    page.get_by_label("Documents").set_input_files([
        {"name": "a.csv", "mimeType": "text/csv", "buffer": b"id\n1\n"},
        {"name": "b.txt", "mimeType": "text/plain", "buffer": "bonjour".encode("utf-8")},
    ])
    expect(page.locator("#list li")).to_have_text(["a.csv (5 bytes)", "b.txt (7 bytes)"])

    page.get_by_label("Documents").set_input_files([])      # clear selection
    expect(page.locator("#list li")).to_have_count(0)
```

- A list of dictionaries uploads several in-memory files: no disk I/O.
- `b"id\n1\n"` is 5 bytes: `i`, `d`, newline, `1`, newline. `"bonjour".encode("utf-8")` converts a string into bytes (7 bytes).
- `set_input_files([])` clears the control and fires `change` again; the page empties its list.
- The input has `multiple`; without it Playwright would raise an error for two files, which is itself a useful check on test data.

### Example 3: Button creates the input dynamically: `expect_file_chooser`

```python
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Choose avatar").click()
    chooser = fc_info.value
    print("multiple?", chooser.is_multiple())             # False
    chooser.set_files({"name": "me.png", "mimeType": "image/png", "buffer": b"\x89PNG..."})

    expect(page.locator("#avatar-name")).to_have_text("me.png")
```

**Explanation**

- Clicking calls `input.click()` on a detached input; the browser raises a file chooser event, which Playwright intercepts.
- `fc_info.value` is the `FileChooser`.
- `is_multiple()` tells whether the chooser permits multiple files.
- `chooser.set_files(...)` accepts the same kinds of arguments as `set_input_files`: paths or dictionaries.
- The bytes `b"\x89PNG..."` are not a valid image, but this page only reads the file name. For a real image preview you would supply valid bytes (for example read a small fixture file).
- We assert the UI reaction.

### Example 4: Download via link and `save_as`

```python
    with tempfile.TemporaryDirectory() as tmp:
        with page.expect_download() as download_info:
            page.get_by_role("link", name="Download CSV").click()
        download = download_info.value

        print(download.suggested_filename)   # orders.csv   (from Content-Disposition)
        print(download.url)                  # http://127.0.0.1:<port>/export.csv
        print(download.failure())            # None

        dest = Path(tmp) / download.suggested_filename
        download.save_as(dest)

        with dest.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        assert len(rows) == 3
        assert rows[0] == {"id": "1", "name": "Maria", "total": "10.50"}
        assert sum(float(r["total"]) for r in rows) == 35.75
```

**Line-by-line**

- `page.expect_download()` registers the listener; clicking the link triggers the download.
- `download.suggested_filename`: `orders.csv`, taken from the response header, not from the URL (`export.csv`). This distinction matters when verifying file names.
- `download.failure()` is `None` when the download succeeded.
- `download.save_as(dest)`: copies the file into our temp folder; `dest` is a `Path`. It waits for the download to complete first.
- `csv.DictReader(f)`: parses the CSV to dictionaries; `list(...)` consumes the reader into a list while the file is open.
- The assertions check the row count, the first row's exact data, and the sum of totals. All CSV values are *strings*; converting to `float` is needed for arithmetic (`10.50 + 20.00 + 5.25 = 35.75`). Floating-point sums can have rounding quirks; here the numbers are exactly representable, but in general use `round(..., 2)` or `decimal.Decimal`.

### Example 5: JavaScript-generated (Blob) download

```python
    with page.expect_download() as info:
        page.get_by_role("button", name="Generate report").click()
    report = info.value
    assert report.suggested_filename == "report.csv"
    content = Path(report.path()).read_text(encoding="utf-8")
    assert content == "id,name\n1,Maria\n2,John\n"
```

- Even though no server response is involved (the file lives in memory as a `Blob`), Playwright treats it as a download.
- `report.path()` returns the path of the temporary file Playwright stored; reading it directly is acceptable when you need only a quick check. The file disappears when the context closes, so `save_as` is better for anything you keep.
- `Path(...)` wraps the path for convenient reading with `read_text`.

### Example 6: A reusable helper for download-and-parse

```python
from pathlib import Path
import csv

def download_csv(page, trigger, dest_dir: Path):
    """Click `trigger` (a Locator), wait for the download, save it, and return rows as dicts."""
    with page.expect_download() as info:
        trigger.click()
    download = info.value
    assert download.failure() is None, f"Download failed: {download.failure()}"
    dest = dest_dir / download.suggested_filename
    download.save_as(dest)
    with dest.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# usage
rows = download_csv(page, page.get_by_role("link", name="Download CSV"), Path(tmp))
```

- The function encapsulates the standard steps; tests read as business actions.
- `assert download.failure() is None, f"..."` uses an assertion message to show the failure reason.
- The `return` inside the `with dest.open(...)` block returns after reading the data; the file is closed automatically.
- This type of helper becomes a method of a page object (Wednesday).

### Example 7: Comparing UI data to exported data

```python
# Suppose the page shows the same data in a table#orders; compare with the exported CSV
ui_names = page.locator("table#orders tbody td:nth-child(2)").all_inner_texts()
csv_names = [r["name"] for r in rows]
assert ui_names == csv_names, f"UI {ui_names} != CSV {csv_names}"
```

- This end-to-end check proves that the export reflects what the user sees; it combines Web Tables skills and file verification.
- If the export has a different order or format by design, compare as sets (`set(ui_names) == set(csv_names)`) or normalise first.

### Example 8: Upload with server confirmation (response + UI)

```python
with page.expect_response("**/api/upload") as resp_info:
    page.get_by_label("Documents").set_input_files(DATA / "resume.pdf")
    page.get_by_role("button", name="Upload").click()
resp = resp_info.value
assert resp.status == 201
expect(page.get_by_text("Upload complete")).to_be_visible()
```

- This pattern is for an application that uploads via an `api/upload` endpoint after clicking Upload.
- The response expectation is registered *before* both steps, since the request occurs after the click; `set_input_files` itself does not send anything unless the app uploads immediately on `change` (in which case drop the click).
- Always assert the UI message too: a 201 response with a broken UI would still be a defect.

### Example 9: Validation (negative) test with an in-memory file

```python
big = b"x" * (6 * 1024 * 1024)       # 6 MB of 'x'
page.get_by_label("Documents").set_input_files(
    {"name": "huge.txt", "mimeType": "text/plain", "buffer": big}
)
expect(page.get_by_role("alert")).to_have_text("File too large (max 5 MB)")
```

- `b"x" * (6 * 1024 * 1024)` builds six megabytes in memory with Python's repeat operator on bytes. This avoids storing a large file in the repository.
- Playwright limits in-memory buffers to about 50 MB per file; for larger test files use real files on disk.
- The error message text depends on your application; the pattern (create a file just over the limit, expect the error) is general.

---

## Real-World Scenarios

### Scenario 1: Bulk customer import

A CRM supports CSV import. Test plan:

1. Valid CSV with 3 rows: success message "3 customers imported", table shows them.
2. CSV with a missing required column: error lists the missing column.
3. CSV with one invalid email: partial import? The product requirement decides; assert accordingly.
4. Empty file: a clear error rather than a crash.
5. Wrong file type (PNG): rejected.

Because every test builds its CSV as an in-memory buffer, the suite is self-contained and each test's data is visible in the test code.

```python
def csv_bytes(*rows):
    out = io.StringIO()
    csv.writer(out).writerows(rows)
    return out.getvalue().encode("utf-8")

page.get_by_label("Import file").set_input_files(
    {"name": "customers.csv", "mimeType": "text/csv",
     "buffer": csv_bytes(["name", "email"], ["Maria", "maria@example.com"])}
)
```

- `io.StringIO()` is an in-memory text file; `csv.writer(...).writerows(...)` writes rows with correct quoting; `getvalue()` returns the text; `.encode("utf-8")` converts to bytes. Using the `csv` module (rather than manual string joins) correctly handles commas and quotes in values.

### Scenario 2: Invoice PDF download

Customers download invoices; finance cares that the invoice number and total are correct.

```python
with page.expect_download() as info:
    page.get_by_role("link", name="Download invoice").click()
pdf = info.value
pdf.save_as(tmp_path / "invoice.pdf")

from pypdf import PdfReader
text = PdfReader(tmp_path / "invoice.pdf").pages[0].extract_text()
assert "Invoice #1042" in text
assert "Total: $35.75" in text
```

Text extraction from PDFs is imperfect (spacing, ordering); assert on short, distinctive phrases, not entire paragraphs.

### Scenario 3: Support ticket attachments

A user attaches up to 3 files, each at most 5 MB, only PNG/JPG/PDF. Boundary tests: 3 files OK, 4 files rejected; 5 MB OK, 5 MB + 1 byte rejected; `.gif` rejected; same file twice handled sensibly. These boundary tests combine well with in-memory buffers.

### Scenario 4: Role-based export access

Admins see "Export all users"; viewers should not. Test visibility (`to_be_hidden`) *and* the server-side rule: as a viewer, request the export URL directly with `page.request.get(...)` and expect 403. Security checks must not rely on hidden buttons alone.

### Scenario 5: Large report generation

A report takes up to 40 seconds. Use `expect_download(timeout=60_000)` and a clear comment. Do not raise the global timeout.

---

## Common Pitfalls and Best Practices

1. **Trying to click the OS file dialog.** Never necessary. Use `set_input_files` or `expect_file_chooser`.
2. **Clicking the upload button, then calling `set_input_files` on an input that does not exist yet.** If the input appears only on click, use `expect_file_chooser`.
3. **Not registering `expect_download` before the click.** The event can be missed. Always wrap the click.
4. **Hard-coded absolute paths.** Use `pathlib` relative to the test file or temporary directories.
5. **Forgetting that downloads live in a temporary folder.** Save with `save_as` if you need the file after the context closes.
6. **Asserting only that "a file was downloaded".** Verify name, size, and content.
7. **Relying on `accept`.** It is a UI hint; test server validation with files that violate it.
8. **Leaving files behind.** Clean temporary folders; do not commit generated downloads.
9. **Large in-memory buffers.** Over ~50 MB, use disk files. Use small files unless testing size limits.
10. **Assuming a download event for PDFs.** Inline viewers may swallow the download; use `page.request.get()` or ensure `Content-Disposition: attachment`.
11. **Ignoring encoding and line endings.** Open text files with `encoding="utf-8"` and `newline=""` for CSV. Windows and Linux differ on line endings.
12. **Reading the CSV while it is still being written.** `save_as` and `path()` wait for completion; reading `download.url` or file system paths directly does not.
13. **Real personal data.** Use synthetic data only.

**Best practices:** use in-memory files for data-driven upload tests; use real fixture files for realistic formats (valid PDFs, images); wrap upload/download steps in helpers; combine UI, network, and file-content assertions; keep timeouts explicit for slow operations; and treat uploads as untrusted input in your test design.

---

## Mini Practice Exercises

### Exercise 1: First upload

On the test site, upload a file named `hello.txt` containing "Hello!" using an in-memory buffer and assert the listing says `hello.txt (6 bytes)`.

<details>
<summary>Solution</summary>

```python
page.get_by_label("Documents").set_input_files(
    {"name": "hello.txt", "mimeType": "text/plain", "buffer": b"Hello!"}
)
expect(page.locator("#list li")).to_have_text(["hello.txt (6 bytes)"])
```
</details>

### Exercise 2: Two files, then remove one

Upload two files, assert both are listed, then re-upload only one (the input's selection is replaced, not appended) and assert only one remains. *Hint:* `set_input_files` replaces the entire selection.

### Exercise 3: File chooser

Use the "Choose avatar" button. Assert the chooser is not multiple, upload `me.png`, and assert the name. Then explain why `set_input_files` on a locator cannot work here. *Answer:* the input does not exist in the DOM until the click, and is never attached to the document.

### Exercise 4: Download and verify

Download the CSV link, save it to a temp folder, and assert: filename `orders.csv`, 3 rows, the maximum `total` is `20.00`. Use `max(float(...))`.

<details>
<summary>Solution</summary>

```python
rows = download_csv(page, page.get_by_role("link", name="Download CSV"), Path(tmp))
assert max(float(r["total"]) for r in rows) == 20.0
```
</details>

### Exercise 5: Round trip

Download the CSV, modify one row's name in Python (using `csv.writer` into a new in-memory buffer), and upload the modified file to a `multiple`-accepting input. Assert the uploaded file's size matches `len(buffer)`.

### Exercise 6: Negative test

Write a helper `make_file(name, size_bytes)` returning the dictionary for `set_input_files`. Use it to produce files at 5 MB, 5 MB + 1 byte, and 0 bytes. Describe what you would assert for each against a hypothetical 5 MB limit.

### Exercise 7: Practice site (stretch)

On `https://the-internet.herokuapp.com/upload`, upload a small generated file via the "Choose File" input (`#file-upload`), click Upload (`#file-submit`), and assert the heading "File Uploaded!" and the uploaded name. On `https://the-internet.herokuapp.com/download`, download the first listed file and assert it is non-empty. The available files on that site change over time, so choose the first link dynamically with `page.locator(".example a").first`.

<details>
<summary>Hint</summary>

```python
page.goto("https://the-internet.herokuapp.com/upload")
page.locator("#file-upload").set_input_files(
    {"name": "demo.txt", "mimeType": "text/plain", "buffer": b"demo"}
)
page.locator("#file-submit").click()
expect(page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
expect(page.locator("#uploaded-files")).to_have_text("demo.txt")
```
</details>

---

## Summary / Key Takeaways

- Playwright never touches the native file dialog. For uploads, set files directly with `locator.set_input_files()` (works even for hidden inputs), or capture the chooser with `page.expect_file_chooser()` when the input appears on click.
- Upload sources can be paths (`str`/`pathlib.Path`), lists, directories (with `webkitdirectory`), or in-memory dictionaries (`name`, `mimeType`, `buffer`). `set_input_files([])` clears.
- Verify the application's reaction: file name, preview, progress, validation messages, network response.
- Downloads use the register-then-act pattern: `with page.expect_download() as info: click`, then use `suggested_filename`, `save_as`, `path`, `failure`.
- Always verify downloaded **content** (CSV via `csv`, JSON via `json`, PDF via `pypdf`, Excel via `openpyxl`), not just existence.
- Use `pathlib`, temporary directories, and synthetic data; avoid hard-coded absolute paths and leftover files.
- Inline viewers and new-tab downloads need special handling; `page.request` is a useful fallback.
- Wrapping file operations in reusable helpers and managing temporary folders with fixtures are covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Input: Upload files: https://playwright.dev/python/docs/input#upload-files
- Playwright Python docs, Downloads: https://playwright.dev/python/docs/downloads
- Playwright Python API reference, FileChooser: https://playwright.dev/python/docs/api/class-filechooser
- Playwright Python API reference, Download: https://playwright.dev/python/docs/api/class-download
- Python docs, `csv` module: https://docs.python.org/3/library/csv.html
