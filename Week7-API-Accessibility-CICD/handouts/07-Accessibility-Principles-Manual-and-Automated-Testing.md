# Handout 07 – Accessibility: Principles, Manual & Automated Testing


**Before class**

- A screen reader: **NVDA** (free, Windows) or **VoiceOver** (built into macOS, toggled with `Cmd + F5`).
- Chrome or Edge.
- In your `week7-demos` folder, run:
  ```bash
  mkdir 07-a11y && cd 07-a11y
  pip install pytest pytest-playwright axe-playwright-python
  playwright install chromium
  mkdir demo-site
  ```

> **How to use this handout:** all three topics use the same two tiny demo pages in `07-a11y/demo-site/`, which you create in Topic 1. Nothing else carries over. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

---

## Topic 1 – Accessibility Principles

### Definition

**Accessibility (a11y)** means people with disabilities can perceive, understand, navigate and use a product. This includes people with visual, hearing, motor and cognitive disabilities, as well as anyone with a temporary or situational limit, such as a broken arm or bright sunlight. The international standard is **WCAG** (Web Content Accessibility Guidelines). Its success criteria are graded at levels **A**, **AA** and **AAA**, and most laws (ADA, Section 508, the European Accessibility Act) point to **WCAG 2.x AA**. For testers, every WCAG criterion is a requirement that can be tested.

### Key ideas

| POUR principle | Means | Example check |
|----------------|-------|---------------|
| **P**erceivable | Users can see or hear the content | Images have `alt` text; contrast is at least 4.5:1 (1.4.3) |
| **O**perable | Users can use it with any input | Everything works with a keyboard (2.1.1); focus is visible (2.4.7) |
| **U**nderstandable | Content and errors are clear | Form errors explain how to fix them (3.3.x) |
| **R**obust | Works with assistive technology | Controls have a name, role and state (4.1.2) |

- **Semantic HTML first:** `<button>`, `<label>`, `<h1>` and `<main>` give assistive technology the meaning for free. A "div soup" page does not.
- **The first rule of ARIA:** don't use ARIA if a native HTML element can do the job. Wrong ARIA is worse than no ARIA.

### Worked example – Fixing an inaccessible sign-up page

**Step 1 – Save the broken page** as `demo-site/bad.html`.

```html
<!DOCTYPE html>
<html>
<head><title>Sign up</title></head>
<body>
  <div class="title">Sign up</div>
  <img src="logo.png">
  <input type="email" name="email">
  <div class="btn" onclick="alert('sent')">Submit</div>
  <p style="color:#aaaaaa; background:#ffffff">Terms apply</p>
</body>
</html>
```

**Step 2 – Copy it to `demo-site/index.html` and fix the language and structure.**

```html
<html lang="en">
...
<main id="main">
  <h1>Sign up</h1>
```

**Step 3 – Give the image a text alternative.**

```html
<img src="logo.png" alt="Demo Co">
```

**Step 4 – Label the input and use a real button.**

```html
<form>
  <label for="email">Email</label>
  <input id="email" type="email" autocomplete="email" required>
  <button type="submit">Submit</button>
</form>
```

**Step 5 – Fix contrast and add a status message region.**

```html
<p style="color:#595959; background:#ffffff">Terms apply</p>
<div id="status" aria-live="polite"></div>
</main>
```

**Step 6 – Add a skip link and a visible focus style** at the start of `<body>`, with the style in `<head>`.

```html
<style>:focus-visible { outline: 3px solid #1a4fd6; }</style>
...
<a href="#main">Skip to main content</a>
```

The complete fixed `demo-site/index.html` looks like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sign up – Demo Co</title>
  <style>:focus-visible { outline: 3px solid #1a4fd6; }</style>
</head>
<body>
  <a href="#main">Skip to main content</a>
  <header><img src="logo.png" alt="Demo Co"></header>
  <main id="main" tabindex="-1">
    <h1>Sign up</h1>
    <form>
      <label for="email">Email</label>
      <input id="email" type="email" autocomplete="email" required>
      <button type="submit">Submit</button>
    </form>
    <p style="color:#595959; background:#ffffff">Terms apply</p>
    <div id="status" aria-live="polite"></div>
  </main>
</body>
</html>
```

### Final code

Your demo folder should contain both pages:

**`demo-site/`**

```
07-a11y/
└── demo-site/
    ├── bad.html      (Step 1)
    └── index.html    (the complete fixed page above)
```

### How to run

From the `07-a11y` folder, start a small web server for the demo pages:

```bash
python -m http.server 8000 --directory demo-site
```

Then open `http://localhost:8000/index.html` and `http://localhost:8000/bad.html` in Chrome or Edge. Leave the server running for Topics 2 and 3.

### Checkpoint

Open `http://localhost:8000/index.html`, press **F12**, go to **Elements → Accessibility**, and select the input. You should see **Name: "Email"** and **Role: textbox**. Selecting the Submit control shows **Role: button**. On `bad.html`, the same control shows **Role: generic** with no keyboard support.

### Your turn

1. For each problem in `bad.html`, write the POUR principle and the WCAG criterion it breaks.
2. Write good `alt` text for: (a) a company logo that links home, (b) a decorative divider line, (c) a chart showing sales up 20%.
3. Why is `<div role="button">Submit</div>` still worse than `<button>`? Name two things you would have to add by hand.
4. Use a contrast checker (for example, the DevTools color picker) to find the ratio of `#aaaaaa` and of `#595959` on white. Which passes AA for normal text?

### Common errors

- **Placeholder used as a label.** It disappears while typing and is often low contrast. Use a real `<label>`.
- **`alt="image"` or `alt="logo.png"`.** Describe the purpose of the image instead. Use `alt=""` for decorative images.
- **`aria-label` on everything.** It overrides the visible text and can confuse users. Use native elements first.

---

## Topic 2 – Keyboard/Screen-Reader Testing

### Definition

Many users never touch a mouse. Some use only a keyboard, and others use a **screen reader** that reads the page aloud and navigates by headings, landmarks, links and form fields. **Manual keyboard testing** checks that every control can be reached and used with Tab, Shift+Tab, Enter, Space, the arrow keys and Esc, in a logical order, with focus always **visible** and no **keyboard trap**. **Screen-reader testing** checks that each element announces a sensible **name, role and state**. Automated scanners cannot judge these things, so manual testing is required even when a scan passes.

### Key ideas

| Key | Expected behaviour |
|-----|--------------------|
| `Tab` / `Shift+Tab` | Move to the next or previous interactive element |
| `Enter` | Follow links and activate buttons |
| `Space` | Activate buttons and toggle checkboxes |
| Arrow keys | Move inside widgets (menus, tabs, radio groups) |
| `Esc` | Close modals and menus, returning focus to the trigger |

- **`tabindex`:** `0` adds an element to the natural Tab order, and `-1` makes it focusable only by script. A **positive value is a defect**, because it breaks the natural order.
- **Screen-reader shortcuts:** NVDA uses `H` (next heading), `D` (next landmark), `F` (next form field), and `Insert+F7` (elements list). VoiceOver uses `Ctrl+Option+U` (rotor).
- **Browse vs focus mode (NVDA):** letter keys jump around the page in browse mode, and they type text in focus mode.

### Worked example – A repeatable manual test script

**Step 1 – Run a keyboard pass on `bad.html`.** Click the address bar, then press `Tab` repeatedly and write down every stop.

| # | Expected stop | Actual | Pass? |
|---|---------------|--------|-------|
| 1 | Email input | Email input | ✅ |
| 2 | Submit button | *(focus leaves the page)* | ❌ |

**Step 2 – Run the same pass on `index.html`.**

| # | Expected stop | Actual | Pass? |
|---|---------------|--------|-------|
| 1 | Skip link | Skip link | ✅ |
| 2 | Email input | Email input | ✅ |
| 3 | Submit button (focus ring visible) | Submit button | ✅ |

**Step 3 – Test the skip link.** On the first Tab stop, press `Enter`. Focus should move to `main`, and the next Tab should land on the Email field.

**Step 4 – Turn on the screen reader** (NVDA: `Ctrl+Alt+N`, VoiceOver: `Cmd+F5`) and navigate with **headings only** (`H` in NVDA, or `Ctrl+Option+Cmd+H` in VoiceOver).

**Step 5 – Tab to each control and write down the exact announcement.**

| Element | `bad.html` announces | `index.html` announces |
|---------|----------------------|------------------------|
| Email field | "edit text" (no name) | "Email, edit, required" |
| Submit | *(not reachable)* | "Submit, button" |
| Logo | "logo.png, graphic" (or "unlabeled graphic") | "Demo Co, graphic" |

**Step 6 – Record each finding** as: *steps · expected · actual · WCAG criterion*. For example: *Tab from Email → Submit should receive focus → focus skips Submit → 2.1.1 Keyboard (A)*.

### Checkpoint

- On `index.html`, every control is reached in a logical order and a **blue focus outline** is always visible.
- NVDA's elements list (`Insert+F7` → Headings) shows **"Sign up"** as heading level 1. On `bad.html` the list is empty.

### Your turn

1. Add `tabindex="3"` to the Email input in `index.html` and Tab through the page. What changes, and which WCAG criterion is affected?
2. Add `outline: none` to `:focus-visible` and repeat the keyboard pass. Write a bug report line for what you see.
3. List the keyboard behaviour you would expect from a modal dialog: opening it, where focus goes, Tab inside it, Esc, and closing it.
4. Name a sensible browser and screen-reader pairing for Windows and one for macOS.

### Common errors

- **Testing with the mouse "just to get there".** Start from the address bar and use only the keyboard.
- **Arrowing through a page with NVDA in focus mode** and thinking the content is missing. Press `Insert+Space` to switch modes.
- **Writing "screen reader doesn't work".** Record what was announced, which screen reader and version, and which browser.

---

## Topic 3 – Automated Accessibility Scanning

### Definition

An **automated accessibility scanner** loads a page and checks it against hundreds of machine-checkable rules, such as missing `alt` text, missing labels, low contrast and invalid ARIA. **axe-core** is the industry-standard engine. You can run it from a browser extension, through Lighthouse, or from Python with **`axe-playwright-python`** inside PyTest. Scans are fast and repeatable, which makes them ideal for regression testing and CI. However, they catch only an estimated **30–40%** of issues, so they **support** manual testing rather than replace it.

### Key ideas

| axe result bucket | Meaning | Action |
|-------------------|---------|--------|
| `violations` | Rules that failed | Fix them, or file a bug |
| `incomplete` | axe couldn't decide | Check manually |
| `passes` | Rules that passed | No action needed |
| `inapplicable` | Nothing on the page to check | No action needed |

- **Impact levels:** `critical`, `serious`, `moderate`, `minor`.
- **Limit to WCAG rules** with tags such as `wcag2a`, `wcag2aa`, `wcag21aa` and `wcag22aa`.
- **Policy options:** zero violations, a baseline (no *new* violations), or an allowlist of known issues that each have a ticket.

### Worked example – Scanning the demo pages with PyTest

Keep `python -m http.server 8000 --directory demo-site` running in a second terminal.

**Step 1 – Run a first scan** (`07-a11y/test_a11y.py`).

```python
from axe_playwright_python.sync_playwright import Axe

BASE = "http://localhost:8000"


def test_index_has_no_violations(page):
    page.goto(f"{BASE}/index.html")
    results = Axe().run(page)
    assert results.violations_count == 0, results.generate_report()
```

**Step 2 – Limit the scan to WCAG A/AA rules.**

```python
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
OPTIONS = {"runOnly": {"type": "tag", "values": WCAG_TAGS}}
```

Change the run line to `Axe().run(page, options=OPTIONS)`.

**Step 3 – Create a reusable `scan` fixture.**

```python
import pytest


@pytest.fixture
def scan(page):
    def _scan(path):
        page.goto(f"{BASE}/{path}")
        return Axe().run(page, options=OPTIONS)
    return _scan
```

**Step 4 – Parametrize over pages and mark the known-bad one.**

```python
@pytest.mark.parametrize("path", [
    "index.html",
    pytest.param("bad.html", marks=pytest.mark.xfail(reason="demo of a broken page")),
])
def test_page_is_accessible(scan, path):
    results = scan(path)
    assert results.violations_count == 0, results.generate_report()
```

**Step 5 – List the rule ids** to triage `bad.html`.

```python
def test_list_bad_page_rules(scan):
    ids = sorted(v["id"] for v in scan("bad.html").response["violations"])
    print(ids)
```

Run it with `pytest -s -k list_bad`.

### Final code

This is the finished test file. It uses the WCAG-only options from Step 2 everywhere.

**`test_a11y.py`**

```python
import pytest
from axe_playwright_python.sync_playwright import Axe

BASE = "http://localhost:8000"
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
OPTIONS = {"runOnly": {"type": "tag", "values": WCAG_TAGS}}


@pytest.fixture
def scan(page):
    def _scan(path):
        page.goto(f"{BASE}/{path}")
        return Axe().run(page, options=OPTIONS)
    return _scan


def test_index_has_no_violations(page):
    page.goto(f"{BASE}/index.html")
    results = Axe().run(page, options=OPTIONS)
    assert results.violations_count == 0, results.generate_report()


@pytest.mark.parametrize("path", [
    "index.html",
    pytest.param("bad.html", marks=pytest.mark.xfail(reason="demo of a broken page")),
])
def test_page_is_accessible(scan, path):
    results = scan(path)
    assert results.violations_count == 0, results.generate_report()


def test_list_bad_page_rules(scan):
    ids = sorted(v["id"] for v in scan("bad.html").response["violations"])
    print(ids)
```

### How to run

Use two terminals, both in the `07-a11y` folder:

```bash
# Terminal 1 – keep the demo site running
python -m http.server 8000 --directory demo-site

# Terminal 2 – run the scans
pytest -v test_a11y.py
pytest -s -k list_bad test_a11y.py
```

### Checkpoint

```
test_index_has_no_violations PASSED
test_page_is_accessible[index.html] PASSED
test_page_is_accessible[bad.html] XFAIL (demo of a broken page)
test_list_bad_page_rules PASSED
```

The `-s -k list_bad` run prints:

```
['color-contrast', 'html-has-lang', 'image-alt', 'label']
```

> axe did **not** report the `<div onclick>` "button". It is invisible to the keyboard, yet the scan cannot detect it. That is why Topic 2 exists.

### Your turn

1. Remove the WCAG tags (run all rules) and list the rule ids again. Which extra rules appear, and are they WCAG failures?
2. Change the scan to exclude the `<p>` element (`context={"exclude": [["p"]]}`). Which violation disappears? When is excluding acceptable?
3. Save `results.response` as JSON in `reports/a11y/<page>.json` for every page scanned.
4. Write the team's scanning policy in two sentences: zero violations or a baseline, and what happens with `incomplete` results.

### Common errors

- **`net::ERR_CONNECTION_REFUSED`.** The local server is not running, or it is serving a different folder.
- **A green scan treated as "accessible".** A scan is a smoke alarm, not a certificate.
- **Scanning before dynamic content loads.** Open the modal or log in *first*, then scan.

---

## Answers

<details>
<summary><strong>Topic 1 – Accessibility Principles</strong></summary>

1. | Problem | POUR | WCAG |
   |---|---|---|
   | No `lang` | Understandable | 3.1.1 Language of Page (A) |
   | `div` used as a title | Perceivable | 1.3.1 Info and Relationships (A) |
   | `img` without `alt` | Perceivable | 1.1.1 Non-text Content (A) |
   | Input without a label | Perceivable / Robust | 1.3.1, 4.1.2, 3.3.2 (A) |
   | `div` as a button | Operable / Robust | 2.1.1 Keyboard (A), 4.1.2 Name, Role, Value (A) |
   | `#aaa` text | Perceivable | 1.4.3 Contrast (Minimum) (AA) |
2. (a) `alt="Demo Co home"` (describe what the link does). (b) `alt=""`. (c) `alt="Sales rose 20% from Q1 to Q2"`, or a short alt plus a data table nearby.
3. A `div` has no keyboard focus or Enter/Space behaviour. You would need `tabindex="0"`, key handlers for Enter and Space, and possibly disabled-state handling, all of which `<button>` gives you for free.
4. `#aaaaaa` ≈ 2.3:1 (fails). `#595959` ≈ 7.0:1 (passes AA and AAA).

</details>

<details>
<summary><strong>Topic 2 – Keyboard/Screen-Reader Testing</strong></summary>

1. Email now receives focus **before** the skip link, so the order no longer matches the visual order. This breaks 2.4.3 Focus Order (A).
2. *"On index.html, after Tab moves to Submit there is no visible focus indicator; the user cannot tell which element is focused. Expected a visible outline. WCAG 2.4.7 Focus Visible (AA)."*
3. Opening it moves focus into the dialog (the first field or the title). Tab and Shift+Tab cycle **inside** the dialog. Esc closes it. On close, focus returns to the button that opened it. The background is not reachable while the dialog is open.
4. Windows: NVDA + Chrome or Firefox (JAWS + Chrome in enterprises). macOS: VoiceOver + Safari.

</details>

<details>
<summary><strong>Topic 3 – Automated Accessibility Scanning</strong></summary>

1. Best-practice rules such as `landmark-one-main`, `page-has-heading-one` and `region` appear. They are axe best practices, not WCAG failures, so report them at a lower priority.
2. `color-contrast` disappears. Excluding is acceptable only for third-party widgets you cannot fix, and there should be a ticket that tracks it.
3. ```python
   import json
   from pathlib import Path
   OUT = Path("reports/a11y")

   def _scan(path):
       page.goto(f"{BASE}/{path}")
       results = Axe().run(page, options=OPTIONS)
       OUT.mkdir(parents=True, exist_ok=True)
       (OUT / f"{path}.json").write_text(json.dumps(results.response, indent=2))
       return results
   ```
4. Example: *"New pages must have zero WCAG A/AA violations; existing pages may not add new ones above the stored baseline. Every `incomplete` item is reviewed manually by a QE before release."*

</details>
