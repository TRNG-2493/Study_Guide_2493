# AI-Assisted Automation Development

## Learning Objectives

By the end of this lesson you will be able to:

- Describe the **AI-assisted automation workflow**: from a reviewed manual test case to committed, reviewed automation code, and say what the human owns at every step.
- Give an AI assistant the three things it needs to write good automation code: the **test case**, a trimmed **DOM snippet** and your team's **conventions**.
- Explain why an AI's first draft of a Playwright test can **pass while testing nothing**, and show it happening.
- Choose **resilient locators** (`get_by_role`, `get_by_label`, `get_by_test_id`) over positional XPath and loose text selectors, and ask the AI to do the same.
- Use AI to generate and refactor the building blocks of a test automation framework: **Page Objects**, **pytest fixtures** in `conftest.py` and **data-driven tests** with `pytest.mark.parametrize`.
- Review AI-generated automation code against a list of common **automation smells**, with help from a small `ast`-based **review linter** you write in Python.
- Run a **sabotage check** to prove a test can actually fail before you trust it.

---

## Why This Matters

Earlier today you saw how AI can help analyse requirements, draft test cases and generate test data. Sooner or later, all of that has to become **code that runs in a pipeline**. That is the job of test automation, and it is where many QE teams first meet AI in their daily work: an IDE assistant that completes the next line, a chat assistant that turns a manual test case into a Playwright script, or a "please refactor this into page objects" request.

The productivity gain is real. A test that takes 30 minutes to write by hand (look up the locators, remember the fixture names, type the boilerplate) can be drafted in under a minute. But automation code has a special property that makes AI mistakes expensive: **a broken test does not always look broken.** A test with a weak assertion goes green every night. Nobody reads green tests. Months later a real defect ships, and the team discovers that the test "covering" it could never fail. In this lesson you will watch exactly that happen with a realistic AI draft, and then learn the review habits that catch it.

This connects directly to the **Weekly Epic**. This week moves from AI fundamentals (Monday) and prompt engineering (Tuesday) to using AI across the QA lifecycle **with human validation and responsible use** (today), and then to building your first QA agent (Thursday and Friday). An agent that writes automation code would face every problem in this lesson, so you need to recognise the problems by hand first. It also feeds **Project 2 (Test Automation Framework)** directly: the Page Objects, fixtures, data-driven tests and review linter in this lesson are pieces you can drop into your Project 2 framework for the e-commerce app (login, search, cart and checkout).

> **Scope note.** Tuesday's *AI-Assisted Coding and Debugging* lesson covered general habits for coding and debugging with AI (explain-this-code, debug prompts, the weakened-assertion trap). Today is about **building automation framework pieces** with AI: Page Objects, fixtures, data-driven tests, and reviewing that code. The formal **human validation checklist** for all AI output comes later today in *Human Validation of AI Output*, and keeping secrets and customer data out of prompts is covered in *Responsible Use of AI in QE*. Agents that do this work for you are covered on **Thursday** and **Friday**.

---

## The Concept

### 1. What "AI-Assisted Automation Development" Means

**Test automation development** is the work of turning test cases into code that a machine can run repeatedly: locating elements, performing actions, checking results and reporting. **AI-assisted** means an AI tool helps with some of that work while a human engineer stays in charge.

In practice you will meet AI assistance in three forms:

| Form | What it looks like | Typical use in automation |
|---|---|---|
| **Inline completion** | An IDE assistant (for example GitHub Copilot) suggests the next line or block as you type | Boilerplate: imports, fixture signatures, repetitive `expect(...)` lines |
| **Chat assistant** | You paste a test case, DOM and conventions, and ask for code | Drafting a new test, a Page Object or a `conftest.py` |
| **Refactoring request** | You paste existing code and ask for a change | "Move these locators into a Page Object", "Turn these five copy-pasted tests into one parametrized test" |

It is worth separating these from a non-AI tool you met in Week 4: **Playwright codegen** (`playwright codegen <url>`). Codegen records your clicks and writes code with real locators taken from the live page. It does not guess; it observes. A good combination is: record with codegen to get trustworthy locators, then ask an AI assistant to **refactor** the recording into your framework's structure. The AI is better at restructuring code than at guessing what a page it has never seen contains.

What AI-assisted automation development is **not**: pressing a button and getting a finished, trustworthy test suite. Every line still needs a reviewer who understands Playwright, pytest and the requirement.

### 2. The Workflow and the Division of Labour

Here is the workflow we will follow in this lesson. Each step has a clear owner.

| Step | What happens | AI can help with | Human owns |
|---|---|---|---|
| 1. Pick a reviewed test case | A manual test case with a clear expected result and trace to an AC | Nothing new; the test case was reviewed earlier | That the test case is correct and worth automating |
| 2. Gather context | Copy a trimmed DOM snippet; write down team conventions | Suggesting what context is missing | Removing anything sensitive from the DOM; correct conventions |
| 3. Prompt for code | Build a prompt with test case, DOM and conventions | Drafting Page Object, fixtures and test | Choosing what to ask for and how much at once |
| 4. Review the draft | Read every line; run a linter | Explaining unfamiliar lines; flagging smells | The decision to accept, fix or reject |
| 5. Run it | `pytest` locally | Explaining an error message | Interpreting the result |
| 6. Sabotage check | Break the app (or the expectation) on purpose; the test must fail | Suggesting sabotage ideas | Confirming the test catches the defect |
| 7. Commit | Code goes into the framework repo via a pull request | Writing the PR description | Code review sign-off |

A useful mental model is the **apprentice and the senior engineer**. The apprentice (the AI) types fast and knows a lot of syntax, but has never seen your app, does not know your conventions unless told, and wants the test to go green. The senior engineer (you) decides what "done" means. Notice that two whole steps, 4 and 6, exist only because the apprentice cannot be trusted to grade its own work.

### 3. The Running Example: Two Pages of the Project 2 App

We need a web page to automate. In Project 2 you will point Playwright at the real running app with `page.goto(...)`. For this lesson we use tiny **offline stand-ins** loaded with `page.set_content(html)`, so every example runs on your machine with no server. The pages implement the requirements you have been using all day:

- **US-101 Login.** AC1: valid email and password open "My Account". AC2: a wrong password (or unknown email) shows "Invalid email or password". AC3: after 5 consecutive failed attempts the account is locked for 15 minutes.
- **US-205 Apply coupon at checkout.** AC1: SAVE10 gives 10% off a subtotal of $50.00 or more. AC2: under $50.00 the total is unchanged and the page shows "Spend $50.00 to use SAVE10". AC3: unknown codes show "Coupon code not recognised". AC4: only one coupon per order.

Create a project folder with this layout (the same shape you will use in Project 2):

```text
automation-demo/
├── pytest.ini
├── conftest.py
├── app_pages.py          # offline stand-in pages (Project 2: the real app)
├── pages/
│   ├── __init__.py       # empty file; makes "pages" a package
│   ├── login_page.py
│   └── coupon_page.py
└── tests/
    ├── test_login.py
    └── test_coupon.py
```

Install the tools once (Week 4):

```text
pip install pytest pytest-playwright
playwright install chromium
```

Here is `app_pages.py`. You do not need to understand every line of the JavaScript; the comments tell you what each page does.

```python
# app_pages.py
# Tiny offline stand-ins for the Project 2 web app pages.
# In the real project these pages come from the running app (page.goto(BASE_URL + "/login")).

LOGIN_HTML = """
<h1>Log in</h1>
<form id="login-form">
  <label for="email">Email</label>
  <input id="email" type="email">
  <label for="password">Password</label>
  <input id="password" type="password">
  <button type="submit">Log in</button>
</form>
<p role="alert" id="message"></p>
<script>
  let failures = 0;
  document.getElementById("login-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    // Simulate a slow server: the answer arrives after 300 ms.
    setTimeout(() => {
      const message = document.getElementById("message");
      if (failures >= 5) {
        message.textContent = "Account locked. Try again in 15 minutes.";
      } else if (email === "shopper@example.com" && password === "Correct-Horse-1") {
        document.body.innerHTML = "<h1>My Account</h1>";
      } else {
        failures += 1;
        message.textContent = failures >= 5
          ? "Account locked. Try again in 15 minutes."
          : "Invalid email or password";
      }
    }, 300);
  });
</script>
"""


def coupon_html(subtotal: float) -> str:
    """Return a checkout page whose cart subtotal is `subtotal`."""
    return f"""
<h1>Checkout</h1>
<p>Subtotal: <span data-testid="subtotal">${subtotal:.2f}</span></p>
<label for="coupon">Coupon code</label>
<input id="coupon">
<button id="apply">Apply</button>
<p>Total: <span data-testid="total">${subtotal:.2f}</span></p>
<p role="status" id="coupon-message"></p>
<script>
  const subtotal = {subtotal};
  let applied = false;
  document.getElementById("apply").addEventListener("click", () => {{
    const code = document.getElementById("coupon").value;
    const message = document.getElementById("coupon-message");
    const total = document.querySelector("[data-testid=total]");
    setTimeout(() => {{
      if (applied) {{
        message.textContent = "Only one coupon per order";
      }} else if (code !== "SAVE10") {{
        message.textContent = "Coupon code not recognised";
      }} else if (subtotal < 50) {{
        message.textContent = "Spend $50.00 to use SAVE10";
      }} else {{
        applied = true;
        total.textContent = "$" + (Math.round(subtotal * 0.9 * 100) / 100).toFixed(2);
        message.textContent = "Coupon applied";
      }}
    }}, 200);
  }});
</script>
"""
```

Two details matter for later:

- **Both pages answer after a delay** (`setTimeout(..., 300)` and `200`). Real web apps are asynchronous too: you click, a request goes to the server, and the page updates a moment later. A test that reads the page immediately after clicking will see the *old* page. This is why waiting strategy matters.
- **The login page has two elements with the text "Log in"**: the `<h1>` heading and the submit button. Remember this; it will trap the AI draft.

In `coupon_html`, notice the doubled braces `{{` and `}}`. The function returns an **f-string**, in which single braces mean "insert a Python value here" (as in `{subtotal}`). JavaScript also uses braces, so each literal JavaScript brace is written twice to tell Python "this is a real brace, not a placeholder".

### 4. Giving the AI What It Needs: Test Case, DOM and Conventions

On Tuesday you learned that **specificity and context** decide the quality of an AI answer. For automation code, three pieces of context matter more than anything else.

**1. The test case.** Paste the reviewed manual test case, including its ID, trace and expected result. If you only say "write a login test", the AI has to invent the expected result, and an invented oracle is the root of most bad tests.

**2. A trimmed DOM snippet.** The AI has never seen your app. If you do not show it the HTML, it will **guess** locators like `#username` or `.login-btn` that may not exist. To get a snippet: open the page in Chrome, right-click the form, choose *Inspect*, right-click the `<form>` element in the Elements panel, and choose *Copy → Copy outerHTML*. Then trim it to the elements the test needs. Before pasting, check that it contains no real customer data, tokens or internal URLs; this is covered properly later today in *Responsible Use of AI in QE*.

**3. Your team conventions.** Every framework has rules: which locator methods, where locators live, how tests are named, where credentials come from. The AI cannot know them unless you write them down. A short conventions block, reused in every prompt, is one of the highest-value things a team can maintain.

Here is a small Python helper that assembles those three pieces into a role/content message list, the same structure you used on Tuesday. No AI is called; we only build the prompt.

```python
# automation_prompt.py
MANUAL_TEST_CASE = """\
ID: TC-101-02
Title: Wrong password shows a generic error
Trace: US-101 AC2
Preconditions: Registered shopper account exists (shopper@example.com)
Steps:
  1. Open the Log in page
  2. Enter the registered email
  3. Enter a wrong password
  4. Click "Log in"
Expected result: The message "Invalid email or password" is shown and the
shopper stays on the Log in page."""

DOM_SNIPPET = """\
<form id="login-form">
  <label for="email">Email</label>
  <input id="email" type="email">
  <label for="password">Password</label>
  <input id="password" type="password">
  <button type="submit">Log in</button>
</form>
<p role="alert" id="message"></p>"""

CONVENTIONS = """\
- Python 3.12, pytest 8+, Playwright for Python (sync API) with the pytest-playwright plugin.
- Use the `page` fixture from pytest-playwright. Never launch a browser inside a test.
- Page Object Model: locators live in pages/login_page.py, class LoginPage. Tests contain no locators.
- Locators: get_by_role, get_by_label, get_by_test_id. No XPath. No CSS unless nothing else works.
- Assertions: playwright.sync_api.expect (web-first). Never time.sleep or wait_for_timeout.
- No credentials in code: use the `shopper` fixture from conftest.py.
- Name tests test_tc_<story>_<nn>_<short_description> and put the trace in the docstring."""


def build_automation_prompt(test_case: str, dom: str, conventions: str) -> list[dict]:
    system = ("You are a senior test automation engineer. You write maintainable, "
              "reviewable Playwright + pytest code that follows the team conventions exactly.")
    user = (
        "Automate the manual test case below.\n\n"
        f"<test_case>\n{test_case}\n</test_case>\n\n"
        f"<dom>\n{dom}\n</dom>\n\n"
        f"<conventions>\n{conventions}\n</conventions>\n\n"
        "Return exactly two Python code blocks: first pages/login_page.py, then "
        "tests/test_login.py. After the code, list any assumption you made under the "
        "heading ASSUMPTIONS. If the DOM does not contain an element you need, say so "
        "instead of guessing a locator."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


if __name__ == "__main__":
    messages = build_automation_prompt(MANUAL_TEST_CASE, DOM_SNIPPET, CONVENTIONS)
    for message in messages:
        print(f"--- {message['role']} ({len(message['content'])} characters)")
    print(messages[1]["content"][:160])
```

Output:

```text
--- system (145 characters)
--- user (1620 characters)
Automate the manual test case below.

<test_case>
ID: TC-101-02
Title: Wrong password shows a generic error
Trace: US-101 AC2
Preconditions: Registered shopper
```

How it works:

- `"""\` starts a triple-quoted multi-line string. The backslash right after the opening quotes stops the string from beginning with an empty line.
- The three constants are the three kinds of context. Keeping them separate means you can reuse `CONVENTIONS` for every automation prompt and swap only the test case and DOM.
- `build_automation_prompt` wraps each piece in **XML-style delimiters** (`<test_case>`, `<dom>`, `<conventions>`), Tuesday's technique for keeping data and instructions apart.
- The last instruction does three jobs from Tuesday's lessons at once: it **locks the format** (exactly two code blocks, in a fixed order), it asks for **ASSUMPTIONS** so guesses become visible, and it gives the model permission to say "I don't know" instead of inventing a locator.
- The function returns a list of `{"role": ..., "content": ...}` dictionaries, the message structure that chat-style AI APIs accept.

Notice what the conventions do: each line is a **rule you can check later**. "No XPath" is checkable. "Write good code" is not. When you write conventions, prefer rules a reviewer (or a linter) can verify.

### 5. The First Draft: A Test That Passes and Proves Nothing

Suppose a teammate asked an AI assistant for "a Playwright test for login and wrong password", **without** the DOM or the conventions. Here is a typical draft. It is **illustrative**, written for this lesson to show patterns that AI assistants commonly produce, not the output of a specific tool.

```python
# ai_draft_test_login.py  -- ILLUSTRATIVE AI draft. Do not copy: it contains deliberate problems.
import time
from playwright.sync_api import sync_playwright
from app_pages import LOGIN_HTML


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(LOGIN_HTML)
        page.fill("//form/input[1]", "shopper@example.com")
        page.fill("//form/input[2]", "Correct-Horse-1")
        page.click("text=Log in")
        time.sleep(2)
        assert page.locator("h1").is_visible()
        browser.close()


def test_wrong_password():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(LOGIN_HTML)
        page.fill("//form/input[1]", "shopper@example.com")
        page.fill("//form/input[2]", "wrong")
        page.click("button")
        message = page.locator("#message").inner_text()
        print("Message was:", repr(message))
        browser.close()
```

It looks reasonable. It even runs. Here is the real result (run with `-s` so `print` output is shown, and with the pytest-playwright plugin switched off because this draft launches its own browser):

```text
$ python -m pytest ai_draft_test_login.py -q -s -p no:playwright
.Message was: ''
.
2 passed in 3.53s
```

Two green tests. Now look closer.

**`test_login` never logs in.** `page.click("text=Log in")` is an older selector style that matches *any* element containing the text "Log in". There are two: the `<h1>Log in</h1>` heading and the button. This page-level `click(selector)` call is not strict by default, so it silently clicks the **first** match: the heading. Clicking a heading does nothing. The form is never submitted. We can prove it by printing the heading after the click and a one-second wait:

```text
h1 now: Log in
```

Still on the login page. So why did the test pass? Because the assertion `assert page.locator("h1").is_visible()` only checks that **some** `<h1>` is visible. The login page has an `<h1>` ("Log in") and so does My Account ("My Account"). The assertion is true whether login worked or not. The test **cannot fail** on a login defect.

**`test_wrong_password` checks nothing at all.** It reads the message with `inner_text()` immediately after clicking. The page answers after 300 ms, so the message is still empty (`''`). Then it *prints* the message instead of asserting on it. A test with no assertion passes as long as nothing crashes.

There are more problems, each a common AI habit:

| Line in the draft | Problem | Why it matters |
|---|---|---|
| `with sync_playwright() as p: ... browser.close()` inside each test | Browser lifecycle managed by hand in every test | Duplicated boilerplate; if an assertion fails before `browser.close()`, cleanup is skipped. The `pytest-playwright` plugin's `page` fixture does this correctly for you (Week 4). |
| `"//form/input[1]"` | Positional XPath | Breaks the day a developer adds a hidden input or reorders fields. Says nothing about *which* field it means. |
| `"Correct-Horse-1"` in the test | Hard-coded credential | Secrets end up in Git history. Every test must be edited when the password changes. |
| `time.sleep(2)` | Hard-coded wait | Wastes 2 seconds on every run when the page answers in 0.3; still fails on a slow CI machine that needs 2.5. |
| `assert ...is_visible()` | One-off check | Checks once, right now, with no waiting. Combined with a vague locator it is meaningless. |
| `inner_text()` straight after `click` | Reads before the page updates | Returns stale content; the classic source of flaky tests. |
| `print(...)` instead of `assert` | No assertion | The test passes regardless of behaviour. |
| No trace to an AC, generic names | `test_login` | When it fails, nobody knows which requirement is at risk. |

This is why "it runs and it's green" is **not** a review. The rest of this lesson rebuilds these tests properly, then gives you tools to catch these smells automatically.

### 6. Locator Strategy: Teach the AI to Find Elements Like a User

A **locator** is the instruction that tells Playwright which element to act on. Choosing locators is the single biggest factor in whether an automated UI test is stable, and it is where AI drafts go wrong most often, because the AI either guesses (no DOM given) or copies whatever attribute it sees first.

Playwright's documentation recommends **user-facing locators**: find elements the way a user or assistive technology (such as a screen reader) would. In priority order:

| Priority | Locator | Finds elements by | Example for our pages |
|---|---|---|---|
| 1 | `page.get_by_role(role, name=...)` | Accessibility role and accessible name | `page.get_by_role("button", name="Log in")` |
| 2 | `page.get_by_label(text)` | The `<label>` linked to a form control | `page.get_by_label("Email")` |
| 3 | `page.get_by_placeholder`, `get_by_text`, `get_by_alt_text`, `get_by_title` | Other visible text | `page.get_by_text("Coupon applied")` |
| 4 | `page.get_by_test_id(id)` | A `data-testid` attribute added for testing | `page.get_by_test_id("total")` |
| Last resort | `page.locator("css=...")` or `page.locator("xpath=...")` | DOM structure | Avoid; the DOM changes often |

Why this order?

- **Role and label locators test what the user experiences.** If a developer accidentally removes the `<label for="email">`, a screen-reader user can no longer tell what the field is for, and `get_by_label("Email")` fails too. Your locator doubles as a small accessibility check.
- **`get_by_role("button", name="Log in")` is precise.** The role `button` excludes the heading, so the trap from section 5 disappears. The `<h1>` has the role `heading`, which you can target separately with `get_by_role("heading", name="My Account")`.
- **Test IDs are stable** when there is no good user-facing handle, such as the total price `<span>`. They are an agreement between developers and testers: "we will not rename this without telling you".
- **Positional XPath** (`//form/input[2]`) describes the *shape* of the page, not its meaning. Shapes change constantly.

Playwright locators created with `get_by_*` or `page.locator(...)` are also **strict**: if a locator matches more than one element when you act on it, Playwright raises an error instead of silently picking one. That is a feature. The draft's `page.click("text=Log in")` used the older page-level selector method, which picks the first match without complaint, and that is exactly how it clicked the heading.

**How to get the AI to use good locators:**

1. Always include the DOM snippet. With the real HTML, the AI can see `<label for="email">Email</label>` and use `get_by_label("Email")`.
2. State the locator rule in your conventions (as in section 4).
3. Add: "If no role, label or test ID identifies an element, stop and tell me; do not invent a CSS selector." Then ask a developer to add a `data-testid` rather than accepting a brittle locator.
4. For an existing page, record locators with **Playwright codegen** (it prefers role and test-ID locators too), then ask the AI to restructure the recording.

### 7. Page Objects: Generating the Structure with AI

The **Page Object Model (POM)**, which you met in Weeks 4 and 6, is a design pattern in which each page (or significant part of a page) gets a class. The class holds the page's **locators** and offers **actions** as methods. Tests then talk to the page object, never to raw locators.

Why it matters even more with AI-generated code: when every test contains its own locators, an AI that drafts ten tests may invent ten slightly different locators for the same button. With a Page Object there is **one** place to review, and one place to fix when the UI changes.

Asking an AI to generate a Page Object from a DOM snippet is one of the most reliable automation tasks you can give it, because the input (HTML) and the output (a class with one locator per element) map almost one to one. Here is the reviewed result for the login page:

```python
# pages/login_page.py
from playwright.sync_api import Page, Locator


class LoginPage:
    """Page Object for the Log in page (US-101)."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators are defined once, here, using user-facing attributes.
        self.email_input: Locator = page.get_by_label("Email")
        self.password_input: Locator = page.get_by_label("Password")
        self.submit_button: Locator = page.get_by_role("button", name="Log in")
        self.message: Locator = page.get_by_role("alert")

    def login(self, email: str, password: str) -> None:
        """Fill the form and submit it. No assertions here."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
```

Line by line:

- `from playwright.sync_api import Page, Locator` imports two **types** from Playwright's sync API. They are used in type hints (`page: Page`, `-> None`) so readers and IDEs know what each value is.
- `__init__(self, page)` receives the Playwright `Page` that pytest-playwright created for this test and keeps it in `self.page` so tests can still reach it.
- Each `self.<name> = page.get_by_...(...)` line creates a **Locator**. Creating a locator does not search the page yet; it is a *recipe* for finding the element. Playwright runs the recipe each time you act, which is why locators stay valid even after the page re-renders.
- `page.get_by_role("alert")` finds the `<p role="alert">`. The `alert` role tells assistive technology to announce changes, which suits an error message.
- `login(...)` is an **action method**: it groups the three steps a user performs. `fill` clears the field and types the value; `click` clicks the button. Both **auto-wait** (Week 4): before acting, Playwright waits until the element is attached, visible, stable and enabled.
- The docstring says **"No assertions here."** Many teams keep assertions in tests and actions in page objects, so a page object can be reused by tests that expect different outcomes (login success *and* login failure). AI drafts often put `assert` statements inside page object methods; if your team follows this rule, put it in your conventions.

The coupon box gets its own small page object:

```python
# pages/coupon_page.py
from playwright.sync_api import Page


class CouponPage:
    """Page Object for the coupon box on the Checkout page (US-205)."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.code_input = page.get_by_label("Coupon code")
        self.apply_button = page.get_by_role("button", name="Apply")
        self.total = page.get_by_test_id("total")
        self.message = page.get_by_role("status")

    def apply(self, code: str) -> None:
        self.code_input.fill(code)
        self.apply_button.click()
```

`get_by_test_id("total")` finds `<span data-testid="total">`, the case from section 6 where no label or role identifies the element well. `get_by_role("status")` finds the `<p role="status">` used for polite, non-urgent messages.

**Reviewing an AI-generated Page Object** is quick if you check four things:

1. **One locator per element the tests need**, each traceable to something in the DOM snippet. A locator for an element that is not in your snippet is invented; delete it or confirm it.
2. **Locator types follow the conventions** (role, label, test ID).
3. **Methods are user actions** (`login`, `apply`), not single clicks wrapped in a method for every element.
4. **No assertions, no sleeps, no data** (emails, codes) inside the class.

### 8. Fixtures and `conftest.py`: Shared Setup the AI Should Reuse

A **fixture** in pytest (Week 4) is a function marked with `@pytest.fixture` that prepares something a test needs. A test requests a fixture simply by naming it as a parameter. Fixtures placed in a file called **`conftest.py`** are automatically available to every test in that folder and below, with no import needed.

The pytest-playwright plugin already provides fixtures such as `browser`, `context` and **`page`** (a fresh browser page for each test, closed automatically afterwards, even when the test fails). Our own `conftest.py` builds on top of `page`:

```python
# conftest.py
import pytest
from playwright.sync_api import Page

from app_pages import LOGIN_HTML, coupon_html
from pages.login_page import LoginPage
from pages.coupon_page import CouponPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """A LoginPage object on a fresh login screen.
    `page` comes from the pytest-playwright plugin: a new browser page per test."""
    page.set_content(LOGIN_HTML)   # real project: page.goto(f"{base_url}/login")
    return LoginPage(page)


@pytest.fixture
def open_checkout(page: Page):
    """Factory fixture: call open_checkout(60.00) to get a CouponPage
    for a cart with that subtotal."""
    def _open(subtotal: float) -> CouponPage:
        page.set_content(coupon_html(subtotal))
        return CouponPage(page)
    return _open


@pytest.fixture
def shopper() -> dict:
    """Test account data. Real project: read from environment variables or a
    secrets store, never hard-coded in test files."""
    return {"email": "shopper@example.com", "password": "Correct-Horse-1"}
```

How it works:

- `login_page(page)` asks pytest-playwright for its `page` fixture, loads the login page, and returns a ready-to-use `LoginPage`. A test that names `login_page` as a parameter starts on the login screen with zero setup code.
- `open_checkout` is a **factory fixture**: instead of returning a page object, it returns a function (`_open`) that the test calls with its own subtotal. Use this pattern when tests need the same setup with different inputs. The inner function can use `page` because it is defined inside the fixture (a *closure*).
- `shopper()` keeps the test account in **one place**. In this offline demo the values are written out, but the docstring states the real rule. In Project 2 it would look like this:

```python
import os

@pytest.fixture
def shopper() -> dict:
    return {"email": os.environ["SHOP_TEST_EMAIL"],
            "password": os.environ["SHOP_TEST_PASSWORD"]}
```

`os.environ["NAME"]` reads an environment variable, which your CI system fills from its secret store; a missing variable raises a `KeyError`, so the problem is obvious rather than silent.

**What to watch for in AI-generated fixtures:**

- The AI ignores fixtures you already have and launches its own browser (the section 5 draft). Tell it which fixtures exist, by name, in your conventions.
- Fixture **scope** errors. `@pytest.fixture(scope="session")` creates one object for the whole run. AI drafts sometimes make a page or login fixture session-scoped "for speed", which makes tests share state: one test's failed login attempts then lock the account for the next test. Keep page-level fixtures at the default function scope unless you have a clear reason.
- Fixtures that do too much (log in, add three items to the cart, apply a coupon) so that every test silently depends on all of it. Small fixtures that compose are easier to review.

### 9. The Reviewed Tests

With page objects and fixtures in place, the tests become short and readable. This is what the corrected login tests look like:

```python
# tests/test_login.py
from playwright.sync_api import expect


def test_tc_101_01_valid_login_opens_my_account(login_page, shopper):
    """Trace: US-101 AC1."""
    login_page.login(shopper["email"], shopper["password"])
    expect(login_page.page.get_by_role("heading", name="My Account")).to_be_visible()


def test_tc_101_02_wrong_password_shows_generic_error(login_page, shopper):
    """Trace: US-101 AC2."""
    login_page.login(shopper["email"], "Wrong-Pass-9")
    expect(login_page.message).to_have_text("Invalid email or password")
    expect(login_page.page.get_by_role("heading", name="My Account")).to_have_count(0)


def test_tc_101_03_unknown_email_shows_same_error(login_page):
    """Trace: US-101 AC2 (same message for unknown email)."""
    login_page.login("nobody@example.com", "Whatever-1")
    expect(login_page.message).to_have_text("Invalid email or password")


def test_tc_101_04_account_locks_after_five_failures(login_page, shopper):
    """Trace: US-101 AC3."""
    for attempt in range(1, 6):
        login_page.login(shopper["email"], f"Wrong-{attempt}")
        expected = ("Account locked. Try again in 15 minutes." if attempt == 5
                    else "Invalid email or password")
        expect(login_page.message).to_have_text(expected)
    # Even the correct password is now refused.
    login_page.login(shopper["email"], shopper["password"])
    expect(login_page.message).to_have_text("Account locked. Try again in 15 minutes.")
```

What changed compared with the draft, and why:

- **`expect(...)` web-first assertions.** `expect(locator).to_have_text("...")` keeps re-checking the element until the text matches or a timeout (5 seconds by default) expires. That handles the 300 ms delay with no `sleep`, and it finishes as soon as the text appears. Compare the draft's `inner_text()`, which read once, too early.
- **Specific expectations.** `get_by_role("heading", name="My Account")` can only be satisfied by the My Account page. The draft's "any `h1` is visible" was satisfied by the login page itself.
- **Checking what should *not* happen.** `to_have_count(0)` in TC-101-02 asserts that no "My Account" heading exists, matching the second half of the expected result ("stays on the Log in page"). AI drafts usually check only the positive half of an expected result; read the test case's expected result and make sure *every* part is asserted.
- **Traceability.** Each test name carries the test case ID, and each docstring the AC. When `test_tc_101_04...` fails in CI, anyone can see that the lockout rule is at risk.
- **TC-101-04 checks every step**, not only the end state. The loop asserts the message after each of the five attempts, so it would catch a lockout that happens after 4 attempts, or 6. Then it confirms the strongest consequence of AC3: even the *correct* password is refused while locked.

A note on the wrong passwords: values like `"Wrong-Pass-9"` are deliberately invalid test inputs, not secrets. Real credentials come from the `shopper` fixture.

### 10. Data-Driven Tests: Let the AI Write the Plumbing, Check the Rows Yourself

When several test cases share the same steps and differ only in data, write **one** test function and feed it a table of data. In pytest this is `@pytest.mark.parametrize` (Week 4). It is an excellent task for AI: give it the test case table from earlier today and ask it to convert the rows into a parametrize list. The **plumbing** (decorator, ids, function signature) is mechanical and AI does it well. The **rows** (inputs and expected results) are the test oracle and must be checked against the requirement by you.

```python
# tests/test_coupon.py
import pytest
from playwright.sync_api import expect

# (test id, subtotal, code, expected total text, expected message) -- trace: US-205
COUPON_CASES = [
    ("TC-205-01", 50.00, "SAVE10", "$45.00", "Coupon applied"),               # AC1 boundary
    ("TC-205-02", 120.00, "SAVE10", "$108.00", "Coupon applied"),             # AC1
    ("TC-205-03", 49.99, "SAVE10", "$49.99", "Spend $50.00 to use SAVE10"),   # AC2 boundary
    ("TC-205-04", 60.00, "SAVE99", "$60.00", "Coupon code not recognised"),   # AC3
]


@pytest.mark.parametrize(
    "subtotal, code, expected_total, expected_message",
    [case[1:] for case in COUPON_CASES],
    ids=[case[0] for case in COUPON_CASES],
)
def test_apply_coupon(open_checkout, subtotal, code, expected_total, expected_message):
    checkout = open_checkout(subtotal)
    checkout.apply(code)
    expect(checkout.message).to_have_text(expected_message)
    expect(checkout.total).to_have_text(expected_total)


def test_tc_205_05_only_one_coupon_per_order(open_checkout):
    """Trace: US-205 AC4."""
    checkout = open_checkout(80.00)
    checkout.apply("SAVE10")
    expect(checkout.message).to_have_text("Coupon applied")
    checkout.apply("SAVE10")
    expect(checkout.message).to_have_text("Only one coupon per order")
    expect(checkout.total).to_have_text("$72.00")
```

How it works:

- `COUPON_CASES` is a list of **tuples**, one per test case. Keeping the ID in the tuple keeps the data and its traceability together.
- `"subtotal, code, expected_total, expected_message"` names the parameters, in order. pytest passes each row's values into the function arguments with the same names.
- `[case[1:] for case in COUPON_CASES]` is a **list comprehension** that drops the first item (the ID) from each tuple: `case[1:]` is a *slice* from index 1 to the end.
- `ids=[case[0] for case in COUPON_CASES]` gives each generated test a readable name, so the report shows `TC-205-03` rather than `49.99-SAVE10-$49.99-...`.
- The test function itself is four lines: open checkout with the row's subtotal, apply the row's code, check the message, check the total.
- AC4 ("only one coupon per order") needs two actions in sequence, so it does not fit the table; it gets its own test. Do not force every case into one parametrized function just because the AI suggested it.

**Checking the rows by hand** (this is the part you must not delegate):

| ID | Subtotal | Rule that applies | Expected total | Check |
|---|---|---|---|---|
| TC-205-01 | 50.00 | AC1: 50.00 is "50.00 or more" | 50.00 × 0.9 = 45.00 | Correct; this is the boundary from Tuesday's BVA |
| TC-205-02 | 120.00 | AC1 | 120.00 × 0.9 = 108.00 | Correct |
| TC-205-03 | 49.99 | AC2: under 50.00, unchanged | 49.99 | Correct; the value just below the boundary |
| TC-205-04 | 60.00 | AC3: unknown code | 60.00, unchanged | Correct |
| TC-205-05 | 80.00 | AC1 then AC4 | 80.00 × 0.9 = 72.00, second code refused | Correct |

A typical AI slip in exactly this kind of table is an expected total computed for the wrong rule (for example "$44.99" for 49.99, as if the discount applied below the threshold) or a boundary row silently missing. Recomputing each expected value takes a minute and is the most valuable minute of the review.

### 11. Running the Suite

`pytest.ini` tells pytest where things are:

```text
[pytest]
pythonpath = .
testpaths = tests
```

- `pythonpath = .` adds the project folder to Python's import path, so `from pages.login_page import LoginPage` and `from app_pages import ...` work from inside `tests/`.
- `testpaths = tests` tells pytest to look for tests in the `tests` folder.

Run it with `-v` (verbose) to see each test:

```text
$ python -m pytest -v
tests/test_coupon.py::test_apply_coupon[chromium-TC-205-01] PASSED       [ 11%]
tests/test_coupon.py::test_apply_coupon[chromium-TC-205-02] PASSED       [ 22%]
tests/test_coupon.py::test_apply_coupon[chromium-TC-205-03] PASSED       [ 33%]
tests/test_coupon.py::test_apply_coupon[chromium-TC-205-04] PASSED       [ 44%]
tests/test_coupon.py::test_tc_205_05_only_one_coupon_per_order[chromium] PASSED [ 55%]
tests/test_login.py::test_tc_101_01_valid_login_opens_my_account[chromium] PASSED [ 66%]
tests/test_login.py::test_tc_101_02_wrong_password_shows_generic_error[chromium] PASSED [ 77%]
tests/test_login.py::test_tc_101_03_unknown_email_shows_same_error[chromium] PASSED [ 88%]
tests/test_login.py::test_tc_101_04_account_locks_after_five_failures[chromium] PASSED [100%]
============================== 9 passed in 6.47s ===============================
```

The `[chromium-...]` part of each name is added by pytest-playwright (which browser) and by our `ids` (which test case). Your timing will differ slightly.

Nine green tests. But the draft in section 5 was green too. Green is necessary, not sufficient. The next two sections give you two independent ways to gain confidence: a static review of the code, and a sabotage check of its behaviour.

### 12. Reviewing AI Automation Code: The Smell Catalogue

A **code smell** is a pattern that is not necessarily a bug but often indicates one. Automation code has its own smells, and AI-generated automation code has a predictable set. Learn this catalogue; it is your review checklist for automation code.

| # | Smell | How it shows up in AI drafts | What to do instead |
|---|---|---|---|
| 1 | **Hard-coded waits** | `time.sleep(2)`, `page.wait_for_timeout(3000)` | Web-first `expect(...)` assertions and Playwright auto-waiting |
| 2 | **Brittle locators** | Positional XPath, long CSS chains, auto-generated class names like `.css-1x2y3z` | `get_by_role`, `get_by_label`, `get_by_test_id` |
| 3 | **Missing assertion** | `print(...)`, or actions with no check at the end | Assert every part of the expected result |
| 4 | **Weak or non-waiting assertion** | `assert locator.is_visible()`, `assert "Error" in page.content()`, `assert len(items) > 0` | `expect(locator).to_have_text("exact text")`, `to_have_count(n)` |
| 5 | **Hard-coded secrets and environment details** | Passwords, API keys, `https://staging.internal...` in the test | Fixtures that read environment variables or config |
| 6 | **Manual browser management** | `sync_playwright()`, `launch()`, `close()` in each test | The pytest-playwright `page` fixture |
| 7 | **Debug leftovers** | `print`, commented-out code, `page.pause()` | Remove before commit |
| 8 | **Swallowed failures** | `try: ... except Exception: pass` around an assertion | Let assertions fail; that is their job |
| 9 | **Test interdependence** | Test B assumes test A already logged in or added an item | Each test sets up its own state via fixtures |
| 10 | **Framework mix-ups** | Selenium's `driver.find_element(By.ID, ...)` (Week 6) inside a Playwright test; async `await page.click()` in a sync project | State framework, API style and versions in your conventions |
| 11 | **Invented APIs** | A method that does not exist, such as `locator.type_text(...)` or `expect(...).to_be_shown()` | Check unfamiliar methods in the official Playwright docs; run the code |
| 12 | **Over-reaching scope** | You asked for one test; the AI also "improved" your conftest, renamed fixtures and changed an expected value | Ask for small, scoped changes; review the full diff |

Smells 3, 4 and 11 are the most dangerous. Smells 1, 2 and 6 make suites slow and flaky; a flaky suite is one the team stops trusting, which is almost as bad as having no suite.

#### A small review linter with `ast`

Several of these smells can be detected mechanically. Python's built-in **`ast` module** (Abstract Syntax Tree) parses source code into a tree of objects: a `Call` node for each function call, an `Assert` node for each `assert`, a `FunctionDef` for each function, and so on. Walking that tree lets you find patterns **without running the code**, and much more reliably than searching the text, because comments and strings that merely mention `time.sleep` are not calls.

```python
# review_linter.py
"""A tiny reviewer's assistant for AI-generated Playwright + pytest code.
It reads Python source as a syntax tree (ast) and flags common smells.
It never replaces a human review; it makes sure the obvious things are not missed."""
import ast
import re
import sys

NON_WAITING = {"is_visible", "is_enabled", "is_checked", "inner_text", "text_content"}
SECRET_LIKE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d\s])\S{8,64}$")


def call_name(node: ast.Call) -> str:
    """Return 'time.sleep' for time.sleep(...), 'fill' for page.fill(...), etc."""
    func = node.func
    if isinstance(func, ast.Attribute):
        if isinstance(func.value, ast.Name):
            return f"{func.value.id}.{func.attr}"
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def review(source: str, filename: str = "<code>") -> list[str]:
    findings = []

    def flag(node, rule, text):
        findings.append(f"{filename}:{node.lineno} {rule} {text}")

    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = call_name(node)
            short = name.split(".")[-1]
            if name == "time.sleep" or short == "wait_for_timeout":
                flag(node, "R1", "hard-coded wait; rely on auto-waiting or expect()")
            if short == "sync_playwright":
                flag(node, "R6", "browser started inside the test; use the pytest-playwright `page` fixture")
            if name == "print":
                flag(node, "R7", "print() in a test; assert instead")
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if arg.value.startswith(("//", "xpath=")):
                        flag(node, "R2", f"brittle XPath locator {arg.value!r}")
                    elif SECRET_LIKE.match(arg.value):
                        flag(node, "R5", f"possible hard-coded secret {arg.value!r}")
        if isinstance(node, ast.Assert):
            for inner in ast.walk(node.test):
                if isinstance(inner, ast.Call) and call_name(inner).split(".")[-1] in NON_WAITING:
                    flag(node, "R4", "assert on a one-off check; use expect(...) web-first assertion")
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(node))
            has_expect = any(isinstance(n, ast.Call) and call_name(n) == "expect"
                             for n in ast.walk(node))
            if not (has_assert or has_expect):
                flag(node, "R3", f"{node.name} has no assertion")
    return sorted(findings, key=lambda f: int(f.split(":")[1].split()[0]))


if __name__ == "__main__":
    total = 0
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as handle:
            results = review(handle.read(), path)
        for line in results:
            print(line)
        total += len(results)
    print(f"{total} finding(s)")
    sys.exit(1 if total else 0)
```

Walking through the important parts:

- **`ast.parse(source)`** turns the source text into a tree. **`ast.walk(tree)`** yields every node in the tree, one by one, so a single `for` loop visits every call, assert and function in the file.
- **`call_name(node)`** works out what is being called. In the tree, `time.sleep(2)` is a `Call` whose `func` is an `Attribute` (`.sleep`) on a `Name` (`time`), so the helper returns `"time.sleep"`. For `page.locator("h1").is_visible()`, the `func` is an `Attribute` on another call, so the helper returns just `"is_visible"`. `short = name.split(".")[-1]` keeps the last part, so `page.wait_for_timeout` and `wait_for_timeout` are both caught.
- **Rules R1, R6 and R7** look at what is called: sleeps and timeouts, a hand-started browser, `print`.
- **Rules R2 and R5** look at **string arguments** (`ast.Constant` nodes holding a `str`). Strings starting with `//` or `xpath=` are XPath. The **secret heuristic** is a regular expression: `(?=.*[A-Za-z])`, `(?=.*\d)` and `(?=.*[^A-Za-z\d\s])` are *lookaheads* meaning "somewhere there is a letter / a digit / a symbol", and `\S{8,64}` means "8 to 64 non-space characters". Password-shaped strings match; normal sentences (which contain spaces) do not.
- **Rule R4** looks inside each `assert` for a call to a non-waiting method such as `is_visible` or `inner_text`.
- **Rule R3** looks at each function whose name starts with `test_` and checks whether it contains any `assert` or any `expect(...)` call. If neither, the test cannot fail on behaviour.
- The results are **sorted by line number**: `f.split(":")[1]` takes the text after the filename, and `.split()[0]` takes the number.
- `sys.exit(1 if total else 0)` returns a non-zero **exit code** when there are findings. That makes the script usable as a CI step or a Git pre-commit hook: the pipeline stops on findings.

Run it on the AI draft:

```text
$ python review_linter.py ai_draft_test_login.py
ai_draft_test_login.py:8 R6 browser started inside the test; use the pytest-playwright `page` fixture
ai_draft_test_login.py:12 R2 brittle XPath locator '//form/input[1]'
ai_draft_test_login.py:13 R2 brittle XPath locator '//form/input[2]'
ai_draft_test_login.py:13 R5 possible hard-coded secret 'Correct-Horse-1'
ai_draft_test_login.py:15 R1 hard-coded wait; rely on auto-waiting or expect()
ai_draft_test_login.py:16 R4 assert on a one-off check; use expect(...) web-first assertion
ai_draft_test_login.py:20 R3 test_wrong_password has no assertion
ai_draft_test_login.py:21 R6 browser started inside the test; use the pytest-playwright `page` fixture
ai_draft_test_login.py:25 R2 brittle XPath locator '//form/input[1]'
ai_draft_test_login.py:26 R2 brittle XPath locator '//form/input[2]'
ai_draft_test_login.py:29 R7 print() in a test; assert instead
11 finding(s)
```

Eleven findings, covering most of the problems from section 5. Now run it on the reviewed code:

```text
$ python review_linter.py tests/test_login.py tests/test_coupon.py pages/login_page.py pages/coupon_page.py
tests/test_login.py:13 R5 possible hard-coded secret 'Wrong-Pass-9'
tests/test_login.py:20 R5 possible hard-coded secret 'Whatever-1'
2 finding(s)
```

Two findings, and both are **false positives**: these are deliberately wrong passwords used as test inputs, not real secrets. This is normal and important to understand:

- A linter finds **suspects**; a human decides. Here the reviewer reads the two lines, confirms they are invalid test inputs, and moves on (or the team adds a way to mark a line as reviewed).
- The linter also has **false negatives**: it did *not* flag the most serious bug in the draft, `page.click("text=Log in")` clicking the heading, nor the meaningless `h1` locator. Those are about **meaning**, and only a human comparing the test to the requirement and the DOM can see them.

So the linter makes the review faster and more consistent; it does not make it optional. The full human review checklist for AI output is the subject of *Human Validation of AI Output* later today.

### 13. The Sabotage Check: Can This Test Fail?

The strongest single question you can ask about any test, AI-written or not, is: **"If the feature were broken, would this test fail?"** You answered it on Tuesday with a hand-rolled mutation check on a Python function. For UI automation the same idea is called a **sabotage check**: deliberately break the application (or, in a real project, point the test at a known-broken build or temporarily change the expected value) and confirm the test goes red.

Our offline pages make sabotage easy: we can edit the HTML. Below, `BROKEN_HTML` is the login page with one defect injected: a successful login no longer opens My Account. We run the draft's assertion and the reviewed assertion against both the working and the broken page.

```python
# sabotage_check.py -- does each check notice when login is broken?
from playwright.sync_api import sync_playwright, expect
from app_pages import LOGIN_HTML
from pages.login_page import LoginPage

# Sabotage: successful login no longer opens My Account.
BROKEN_HTML = LOGIN_HTML.replace("<h1>My Account</h1>", "<h1>Log in</h1>")


def draft_style_check(page) -> bool:
    """What the AI draft asserted: 'some h1 is visible'."""
    return page.locator("h1").is_visible()


def reviewed_check(page) -> bool:
    """What the reviewed test asserts: the My Account heading appears."""
    try:
        expect(page.get_by_role("heading", name="My Account")).to_be_visible(timeout=2000)
        return True
    except AssertionError:
        return False


with sync_playwright() as p:
    browser = p.chromium.launch()
    for label, html in [("working app", LOGIN_HTML), ("broken app", BROKEN_HTML)]:
        for check in (draft_style_check, reviewed_check):
            page = browser.new_page()
            page.set_content(html)
            LoginPage(page).login("shopper@example.com", "Correct-Horse-1")
            page.wait_for_timeout(500)  # only so draft_style_check sees the final page
            result = "PASS" if check(page) else "FAIL"
            print(f"{label:12} {check.__name__:18} {result}")
            page.close()
    browser.close()
```

Output:

```text
working app  draft_style_check  PASS
working app  reviewed_check     PASS
broken app   draft_style_check  PASS
broken app   reviewed_check     FAIL
```

How to read it:

- On the **working** app both checks pass. That alone tells you nothing about which is better.
- On the **broken** app the draft's check **still passes**. It cannot detect the defect it was written to catch. The reviewed check **fails**, which is exactly what we want: a test that fails when the feature is broken.
- `LOGIN_HTML.replace(old, new)` is ordinary Python string replacement; it creates a copy of the page with the injected defect.
- The `try / except AssertionError` around `expect(...)` turns a failed web-first assertion into `False` so the script can print a table instead of stopping. In a real pytest test you would **not** catch the error; you let it fail the test.
- `timeout=2000` shortens the default 5-second wait so the script finishes quickly.
- `page.wait_for_timeout(500)` appears here deliberately, because this is a **demonstration harness**, not a test: the draft's non-waiting check needs the page to have settled before it looks. The review linter would flag this line (rule R1), and that is correct: it is the kind of line you must justify or remove.

Make sabotage a habit for every new AI-generated test: break it once on purpose, see it go red, then restore. It takes two minutes and it is the only way to know the test has teeth.

### 14. Iterating with the AI: Re-Asks, Refactors and Small Steps

You rarely accept an AI automation draft as is. The skill is in **how you ask for changes**.

**Feed review findings back as a re-ask.** Tuesday's format-locking lesson introduced the *one re-ask*: when output breaks a rule, send the specific failure back once. For code, the linter output is a ready-made re-ask:

```text
Your code has these review findings:
<findings>
ai_draft_test_login.py:12 R2 brittle XPath locator '//form/input[1]'
ai_draft_test_login.py:15 R1 hard-coded wait; rely on auto-waiting or expect()
ai_draft_test_login.py:20 R3 test_wrong_password has no assertion
</findings>
Fix only these findings. Do not change test names, expected results or any
other line. Return the full corrected file.
```

Note the scope fence: "Fix only these findings ... do not change expected results". Without it, the AI may "fix" a failing test by weakening the expected value (Tuesday's weakened-assertion trap).

**Use AI for refactoring existing suites.** Some of the best uses of AI in automation are not new tests but **restructuring** old ones:

- "Move every locator in these four test files into a `CheckoutPage` class. Keep the tests' behaviour identical."
- "These six tests differ only in data. Convert them into one `parametrize` test, keeping the original test names as `ids`."
- "Replace every `time.sleep` in this file with an appropriate `expect` assertion; explain each replacement."

For refactors, the safety net is simple: **run the suite before and after**. The same tests should pass, and a sabotage check on one or two of them should still fail. A refactor that changes the pass/fail picture is not a refactor.

**Keep changes small.** Ask for one page object, or one test file, at a time. A 400-line AI change is hard to review properly, and reviewers start skimming, which is exactly when the `h1` bug slips through. Small changes keep the review honest.

**Ask the AI to explain, then verify one claim.** When the AI uses a method you have not seen (say `to_have_count`), ask what it does, then check that claim in the Playwright API docs. If the method does not exist, you have caught smell 11 (invented API) before it reaches the repo.

### 15. Connecting to Project 2

In Project 2 you are building a test automation framework for the e-commerce app. Today's lesson gives you a concrete way to grow it with AI help, safely:

1. **Write a `CONVENTIONS.md`** in your framework repo containing the rules from section 4 (framework and versions, POM location, locator priority, `expect` only, no sleeps, fixtures for credentials, naming and traceability). Paste it into every automation prompt.
2. **One page object per page or component**: `LoginPage`, `SearchPage`, `CartPage`, `CheckoutPage`. Generate each from a trimmed DOM snippet (or a codegen recording), then review with the four checks in section 7.
3. **Shared fixtures in `conftest.py`**, with credentials and the base URL read from environment variables.
4. **Data-driven tests** generated from the reviewed test cases and test data you produce in today's exercise, with every expected value recomputed by hand.
5. **Add `review_linter.py` to the repo** and run it before each commit (and later in CI). Extend it with rules for your own conventions.
6. **Sabotage each new test once** and note in the pull request how you did it.

Today's exercise asks you to generate and review AI test cases and data for Project 2 and to document your corrections. The automation code you write from those reviewed cases should follow exactly this flow.

---

## Practice Exercises

1. **Spot the smells.** Without running anything, list every smell from section 12 in this AI-generated snippet, and say how you would fix each one:

   ```python
   import time
   def test_search(page):
       page.goto("https://staging.shop.internal/search")
       page.fill("#q", "headphones")
       page.click("//div[3]/button")
       time.sleep(3)
       results = page.locator(".result").count()
       assert results > 0
   ```

2. **Locator upgrade.** Given this DOM, write a `SearchPage` page object using only `get_by_role`, `get_by_label` or `get_by_test_id`:

   ```text
   <label for="q">Search products</label>
   <input id="q" type="search">
   <button type="submit">Search</button>
   <ul data-testid="results"><li>...</li></ul>
   <p role="status">3 results for "headphones"</p>
   ```

3. **Prompt it properly.** Use `build_automation_prompt` from section 4 with a new test case, TC-205-03 (subtotal $49.99, code SAVE10, expected "Spend $50.00 to use SAVE10" and total unchanged), the checkout DOM, and the same conventions (changed to `CouponPage`). Print the prompt and check that it contains the test case, DOM, conventions and the ASSUMPTIONS instruction.

4. **Extend the linter.** Add a rule **R8** to `review_linter.py` that flags Selenium-style calls (`find_element`, `find_elements`) in Playwright code. Test it on a small string containing `driver.find_element(By.ID, "email")` by calling `review(source)` directly.

5. **Sabotage it.** Create a sabotaged coupon page in which SAVE10 gives 20% off instead of 10% (hint: replace `0.9` in the output of `coupon_html(...)` with `0.8`). Confirm by running it that TC-205-01 would fail. Then write a deliberately weak version of the test that only asserts `expect(checkout.message).to_have_text("Coupon applied")`, and show that it still passes on the sabotaged page. What does this tell you about which parts of the expected result must be asserted?

6. **Refactor request.** Write a scoped refactoring prompt asking an AI to merge `test_tc_101_02` and `test_tc_101_03` into one parametrized test. Include a scope fence that protects the expected messages and the trace docstrings.

---

## Knowledge Check

1. Name the three pieces of context an AI assistant needs to write good automation code for your framework.
2. The AI draft's `test_login` passed even though it never logged in. Give the two reasons.
3. Why is `page.get_by_role("button", name="Log in")` better than `page.click("text=Log in")` on our login page?
4. What is the difference between `assert page.locator("#message").inner_text() == "..."` and `expect(page.locator("#message")).to_have_text("...")`?
5. In a data-driven test generated by AI, which part can you largely trust to the AI and which part must you check yourself?
6. The review linter reported two findings on the reviewed code. What were they, and what should a reviewer do about them?
7. What is a sabotage check, and why is "the test passes" not enough evidence that a test is good?
8. Why might an AI-generated fixture with `scope="session"` cause the account-lockout test to interfere with other tests?

<details><summary>Answers</summary>

1. The reviewed **test case** (with expected result and trace), a trimmed **DOM snippet** of the page, and the team's **conventions** (framework and versions, POM location, locator rules, assertion style, fixtures, naming).
2. (a) `page.click("text=Log in")` matched the `<h1>Log in</h1>` heading first and clicked it, so the form was never submitted. (b) The assertion `page.locator("h1").is_visible()` is true on the login page as well as on My Account, so it cannot fail on a login defect.
3. The role `button` excludes the heading, so the locator identifies exactly the submit button. `get_by_*` locators are also strict (they raise an error if they match more than one element), whereas the page-level `click("text=...")` call silently picked the first of two matches. Role locators also reflect what users and assistive technology see.
4. `inner_text()` reads the text **once, immediately**; if the page has not updated yet, it reads stale text and the test is flaky. `expect(...).to_have_text(...)` is a **web-first assertion** that keeps re-checking until the text matches or the timeout expires, so it handles asynchronous pages without sleeps.
5. The **plumbing** (the `parametrize` decorator, parameter names, `ids`, function signature) is mechanical and AI does it well. The **rows**, meaning the inputs and especially the **expected results**, are the test oracle and must be recomputed and checked against the requirement by a human.
6. Two R5 "possible hard-coded secret" findings for `'Wrong-Pass-9'` and `'Whatever-1'`. They are **false positives**: deliberately invalid test inputs, not real credentials. The reviewer confirms that and accepts them (or marks the lines as reviewed). Linters find suspects; humans decide.
7. A sabotage check deliberately breaks the feature (or the expectation) and confirms the test fails. A test that passes on a working app may also pass on a broken one, as the draft's `h1` check did; only a failing run on a broken app proves the test can detect the defect.
8. A session-scoped fixture is created once and shared by every test in the run. If the page (or browser context, or logged-in state) is shared, the five failed logins in TC-101-04 could leave the account locked, so later tests that expect a successful login would fail, depending on test order. Tests must not share state; keep page-level fixtures at function scope.

</details>

---

## Glossary

- **AI-assisted automation development:** Writing test automation code with help from AI tools (inline completion, chat, refactoring), while a human engineer reviews, runs and owns the result.
- **Playwright codegen:** Playwright's recorder; it writes test code from your real interactions with a page, using locators taken from the live DOM. Not an AI tool.
- **DOM snippet:** A trimmed copy of a page's HTML (for example via *Copy outerHTML* in DevTools) given to the AI so it can use real locators instead of guessing.
- **Team conventions:** Written, checkable rules for a test framework (framework versions, locator priority, assertion style, fixtures, naming) reused in every automation prompt.
- **Locator:** Playwright's description of how to find an element; evaluated each time it is used.
- **User-facing locator:** A locator based on what users perceive: role, accessible name, label, text (`get_by_role`, `get_by_label`, ...).
- **Strictness:** The Playwright locator behaviour of raising an error when a locator matches more than one element during an action.
- **Page Object Model (POM):** A design pattern in which each page or component is a class holding its locators and user actions; tests use the class instead of raw locators.
- **Fixture:** A pytest function (`@pytest.fixture`) that prepares something a test needs; requested by naming it as a test parameter.
- **`conftest.py`:** A pytest file whose fixtures are automatically available to tests in its folder and subfolders.
- **Factory fixture:** A fixture that returns a function, so each test can perform the same setup with its own inputs.
- **Web-first assertion:** A Playwright `expect(...)` assertion that retries until the condition is met or a timeout expires.
- **Data-driven test:** One test function run against a table of inputs and expected results (`@pytest.mark.parametrize`).
- **Code smell:** A code pattern that often indicates a problem, such as hard-coded waits or missing assertions.
- **Abstract Syntax Tree (AST):** A tree representation of source code; Python's `ast` module parses code into one so tools can inspect it without running it.
- **False positive / false negative (linter):** A reported problem that is not real / a real problem the linter did not report.
- **Sabotage check:** Deliberately breaking the application or expectation to confirm that a test fails, proving it can detect the defect.

---

## Summary

- AI can draft automation code in seconds, but **a broken test does not look broken**: an AI draft can be green while testing nothing, as the `h1` example showed.
- Give the AI the **test case, a trimmed DOM snippet and your conventions**. Write conventions as checkable rules and reuse them in every prompt.
- Prefer **user-facing locators** (`get_by_role`, `get_by_label`, then `get_by_test_id`); avoid positional XPath and loose text selectors. Playwright locators are strict, which protects you from silent wrong matches.
- AI is good at generating **Page Objects** from a DOM snippet, **fixtures** and **parametrize plumbing**. You own the locators' correctness, fixture scope and, above all, the **expected results** in every data row.
- Use **web-first `expect` assertions**, assert **every part** of the expected result (including what should *not* happen), and keep **traceability** in test names and docstrings.
- Review AI automation code against the **smell catalogue**. A small **`ast` review linter** catches mechanical smells quickly, with some false positives and important false negatives, so it supports human review rather than replacing it.
- Before trusting any new test, run a **sabotage check**: it must fail when the feature is broken.
- Iterate with **scoped re-asks** and **small changes**, and run the suite before and after any AI refactor.

---

## Additional Resources

- Playwright for Python, *Locators* (the recommended built-in locators, strictness, and why CSS/XPath are discouraged): https://playwright.dev/python/docs/locators
- Playwright for Python, *Page object models* (official sync and async examples of the pattern used in this lesson): https://playwright.dev/python/docs/pom
- Playwright, *Best Practices* (test isolation, user-facing locators, web-first assertions, linting tests; examples are in JavaScript but every principle applies to Python): https://playwright.dev/docs/best-practices
