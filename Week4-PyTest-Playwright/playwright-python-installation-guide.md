# Playwright with Python: Installation Guide

Please complete this setup **before Lecture 1**. It takes about 15–20 minutes, most of it waiting for downloads.

If you get stuck, see [Troubleshooting](#troubleshooting) at the end, or bring the error message to class.

---

## What you will install

| Item | What it is |
|---|---|
| **Python** | The language we write tests in |
| **pytest** | The test runner that finds and runs your tests |
| **playwright** | The Python library that controls the browser |
| **pytest-playwright** | The plugin that connects pytest and Playwright (gives you the `page` fixture) |
| **Browsers** | Special builds of Chromium, Firefox and WebKit that Playwright drives |

> **Note:** Playwright also has a JavaScript test runner called "Playwright Test" (`npx playwright test`). We are **not** using it. In Python, we use **pytest**. If you see tutorials with `npx`, `.ts` files or `playwright.config.ts`, skip them and use the Python docs at <https://playwright.dev/python>.

---

## Step 1: Check Python

You need **Python 3.9 or newer** (3.11 or newer recommended).

Open a terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux) and run:

```bash
python --version
```

On macOS/Linux, if that doesn't work, try:

```bash
python3 --version
```

If Python is missing or too old, download it from <https://www.python.org/downloads/>.
**Windows users:** during installation, tick **"Add python.exe to PATH"**.

> On macOS/Linux, use `python3` and `pip3` wherever this guide says `python` and `pip`, unless `python` already points to Python 3.

---

## Step 2: Create a project folder

```bash
mkdir playwright-course
cd playwright-course
```

---

## Step 3: Create and activate a virtual environment

A virtual environment keeps this course's packages separate from the rest of your computer.

**Create it:**

```bash
python -m venv venv
```

**Activate it:**

| System | Command |
|---|---|
| Windows (Command Prompt) | `venv\Scripts\activate` |
| Windows (PowerShell) | `.\venv\Scripts\Activate.ps1` |
| macOS / Linux | `source venv/bin/activate` |

When it's active, you'll see `(venv)` at the start of your terminal prompt.

> **Activate the virtual environment every time you open a new terminal** for this course.

---

## Step 4: Install the Python packages

```bash
pip install pytest-playwright
```

This one command installs three packages:

- `pytest-playwright` (the plugin)
- `playwright` (the library)
- `pytest` (the test runner)

We will also use these later in the course. You can install them now:

```bash
pip install pytest-html pytest-rerunfailures
```

---

## Step 5: Install the browsers

```bash
playwright install chromium
```

This downloads the Chromium browser that Playwright controls. It is **not** your normal Chrome; it is a special build matched to your Playwright version.

To install all three browsers (Chromium, Firefox and WebKit) instead:

```bash
playwright install
```

**Where the browsers are stored** (shared by all your projects):

| System | Location |
|---|---|
| Windows | `%USERPROFILE%\AppData\Local\ms-playwright` |
| macOS | `~/Library/Caches/ms-playwright` |
| Linux | `~/.cache/ms-playwright` |

**Linux only:** if the browser fails to start because of missing system libraries, run:

```bash
playwright install --with-deps chromium
```

(This may ask for your password, because it installs system packages.)

---

## Step 6: Check the versions

```bash
pytest --version
playwright --version
```

Both commands should print a version number.

---

## Step 7: Run a test to confirm everything works

Create a file named `test_setup.py` in your project folder:

```python
import re
from playwright.sync_api import Page, expect


def test_playwright_homepage(page: Page):
    page.goto("https://playwright.dev/python")
    expect(page).to_have_title(re.compile("Playwright"))
```

Run it with the browser visible:

```bash
pytest --headed
```

You should see a browser window open briefly, and then:

```
1 passed
```

**If you see `1 passed`, you're ready for Lecture 1.**

---

## Step 8 (optional): Add a `pytest.ini` file

Create a file named `pytest.ini` in your project folder so you don't have to type options every time:

```ini
[pytest]
addopts = --browser chromium
```

Now `pytest` uses Chromium by default. We will add more options in class.

---

## Recommended editor: VS Code

1. Download VS Code from <https://code.visualstudio.com/>.
2. Install the **Python** extension (by Microsoft).
3. Open your `playwright-course` folder in VS Code.
4. Press `Ctrl+Shift+P` (`Cmd+Shift+P` on macOS), choose **Python: Select Interpreter**, and pick the one inside your `venv` folder.

---

## Quick reference

```bash
# Every time you start working
cd playwright-course
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

# Run all tests
pytest

# Run with the browser visible
pytest --headed

# Run one file
pytest test_setup.py

# Run slowly (500 ms between actions), to watch what happens
pytest --headed --slowmo 500
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Executable doesn't exist... Please run playwright install` | You skipped Step 5, or upgraded Playwright. Run `playwright install chromium`. |
| `playwright: command not found` / `'playwright' is not recognized` | Run `python -m playwright install chromium` instead. Also check the venv is active. |
| `fixture 'page' not found` | The venv isn't active, or `pytest-playwright` isn't installed. Activate the venv and run `pip install pytest-playwright`. |
| `python: command not found` (macOS/Linux) | Use `python3` and `pip3`. |
| `'python' is not recognized` (Windows) | Reinstall Python and tick **"Add python.exe to PATH"**, or try `py` instead of `python`. |
| PowerShell says **running scripts is disabled** when activating | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`, then activate again. Or use Command Prompt instead. |
| Browser download fails or times out (office/school network) | Ask IT for the proxy address and set it, for example `set HTTPS_PROXY=http://proxy:8080` (Windows) or `export HTTPS_PROXY=http://proxy:8080` (macOS/Linux), then retry. As a fallback, use your installed Chrome: `pytest --browser-channel chrome`. |
| Linux: browser crashes with missing library errors | Run `playwright install --with-deps chromium`. |
| Test fails with a timeout on `page.goto` | Check your internet connection and that you can open the site in a normal browser. |

Still stuck? Copy the **full error message** and bring it to class, or send it to your instructor before Lecture 1.
