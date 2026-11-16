# Playwright with Python – Beginner to Intermediate Interview Guide

## Questions, suggested answers, coding solutions, scenarios, and practical exercises

This guide is designed for candidates who know basic Python and are learning browser automation with Playwright. It assumes the common Python setup: **Playwright Python + Pytest + `pytest-playwright`**.

> **Important distinction:** Playwright has an official Playwright Test Runner for JavaScript/TypeScript. In Python projects, Pytest is commonly used as the test runner, while the Playwright Python library provides browser automation APIs. The `pytest-playwright` plugin integrates Playwright with Pytest and supplies useful fixtures and command-line options.

### Difficulty labels

- **Beginner:** Explain the concept or write a straightforward example.
- **Intermediate:** Apply the concept in a realistic test, understand fixture/framework behavior, or troubleshoot an issue.
- **Advanced basics:** A stretch topic for candidates with more hands-on experience; not normally essential for a true beginner.

---



## Quick navigation

- [Conceptual Playwright questions](#part-1--conceptual-interview-questions-and-suggested-answers)
- [Scenario-based questions (9 scenarios)](#scenario-based-questions)
- [Practical coding exercises](#part-3--practical-coding-exercises)
- [Difficulty classification](#question-by-question-difficulty-classification)


# Part 1 – Conceptual interview questions and suggested answers

## 1. Introduction to Playwright and architecture

### Q1. What is Playwright, and why is it used in automation testing?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Playwright is an open-source browser automation library. It lets testers automate web applications using browsers such as Chromium, Firefox, and WebKit. It supports interactions such as clicking, typing, navigation, screenshots, downloads, and network interception.

It is useful because it provides auto-waiting for actions, browser-context isolation, multiple-browser support, modern locator APIs, and debugging tools.

</details>

### Q2. What are the key features and advantages of Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

- Supports Chromium, Firefox, and WebKit.
- Provides auto-waiting and retrying web-first assertions.
- Supports isolated browser contexts.
- Offers role-, label-, text-, placeholder-, and CSS-based locators.
- Supports frames, multiple pages, downloads, screenshots, and network interception.
- Includes tools such as Inspector, Trace Viewer, and Codegen.
- Can be integrated with Python and Pytest.

</details>

### Q3. Can you explain the architecture of Playwright? How do the browser, browser context, and page objects interact?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

A typical hierarchy is:

```text
Playwright
   └── Browser
         ├── Browser Context A
         │      ├── Page 1 (tab)
         │      └── Page 2 (tab)
         └── Browser Context B
                └── Page 1 (tab)
```

The Playwright library communicates with a browser through its automation protocol/driver connection. A browser represents the browser process. A browser context is an isolated browser session with its own cookies, local storage, and session state. A page represents a tab or page within a context.

A context can contain multiple pages. Separate contexts are useful for isolating users or tests.

</details>

### Q4. What is the difference between a browser, browser context, and page in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

- **Browser:** The launched browser instance, such as Chromium.
- **Browser context:** An isolated session within the browser. It has separate cookies and storage.
- **Page:** A tab within a browser context.

For example, two users can be tested in two separate contexts in the same browser, without sharing their login cookies.

</details>

### Q5. How do you integrate Playwright with Pytest in a Python automation project?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Install Playwright, its browser binaries, Pytest, and the Pytest integration plugin:

```bash
pip install pytest playwright pytest-playwright
playwright install
```

A test can request the plugin-provided `page` fixture:

```python
def test_homepage(page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"
```

Run it with:

```bash
pytest
```

</details>

### Q6. What is the purpose of the `pytest-playwright` plugin?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

It integrates the Playwright Python library with Pytest. It supplies fixtures such as `page`, `context`, and `browser`, and command-line options for browser selection, headed mode, tracing, screenshots, video, and other test settings. Exact options depend on the installed plugin version.

</details>

### Q7. What is the difference between Playwright's Test Runner and Pytest?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Playwright Test is the official test runner for JavaScript/TypeScript. It includes its own test discovery, fixtures, hooks, assertions, retries, and reporting.

In Python, the Playwright library is commonly paired with Pytest. Pytest provides test discovery, fixtures, markers, parameterization, hooks, and plugins; Playwright provides browser automation and Playwright-specific assertions through its Python API.

Do not describe the JavaScript/TypeScript Playwright Test Runner as the default Python test runner.

</details>

---

## 2. Locators and selectors

### Q8. What are locators in Playwright, and why are they important?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

A locator describes how to find one or more elements on a page. Playwright locators are designed to work with dynamic pages: they resolve the matching element when an action or assertion is performed and integrate with auto-waiting.

```python
page.get_by_role("button", name="Sign in").click()
```

</details>

### Q9. What are the different ways to locate web elements in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Common options include:
- `get_by_role()`
- `get_by_label()`
- `get_by_placeholder()`
- `get_by_text()`
- `get_by_alt_text()`
- `get_by_title()`
- `get_by_test_id()`
- `locator()` for CSS and other supported selector strategies

Prefer user-facing, accessible locators such as role and label when they uniquely identify the intended element.

</details>

### Q10. What are CSS selectors, and how do you use them in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

CSS selectors identify elements by tag, class, ID, attributes, relationships, or state.

```python
page.locator("#username").fill("asha")
page.locator(".submit-button").click()
page.locator("input[name='email']").fill("asha@example.com")
```

</details>

### Q11. What are attribute selectors in CSS? Can you provide examples?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Attribute selectors find elements based on HTML attributes.

```python
page.locator("input[type='email']")
page.locator("button[data-testid='save']")
page.locator("a[href^='/account']")
page.locator("input[placeholder*='Search']")
```

Examples: `[attr=value]` exact match, `[attr^=value]` begins with, `[attr*=value]` contains, and `[attr$=value]` ends with.

</details>

### Q12. What are CSS pseudo-classes, and how can you use them to identify elements?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Pseudo-classes select elements based on state or position. Examples include `:first-child`, `:last-child`, `:nth-child()`, `:checked`, `:disabled`, and `:not()`.

```python
page.locator("ul li:first-child")
page.locator("input:checked")
page.locator("button:not([disabled])")
```

For Playwright-specific element state, its locator filters and web-first assertions may be clearer than a complicated selector.

</details>

### Q13. What are dynamic CSS selectors, and how do you handle elements with changing attributes?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Dynamic selectors are locator strategies that avoid relying on values that change between page loads, such as generated IDs. Prefer stable attributes, roles, labels, text, or test IDs. If only part of an attribute is stable, CSS attribute operators such as `^=`, `$=`, or `*=` can help.

Avoid brittle selectors tied to deeply nested DOM structure.

</details>

### Q14. What is the difference between CSS selectors and XPath?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

CSS selectors are concise and commonly used for selecting elements by tag, class, ID, attributes, and relationships. XPath can navigate the DOM using axes and can express some parent/ancestor and text-based relationships.

Examples:

```python
page.locator("input[name='email']")  # CSS
page.locator("//input[@name='email']")  # XPath
```

Neither is automatically best for every case. Playwright's role- and label-based locators are often more resilient and readable than either CSS or XPath.

</details>

### Q15. What is the difference between `locator()` and `get_by_role()` in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

`locator()` accepts CSS selectors and other supported selector syntax. `get_by_role()` locates elements by their accessible role and optionally their accessible name.

```python
page.locator("button.save").click()
page.get_by_role("button", name="Save").click()
```

The role-based locator describes the user's view of the interface and is usually preferable when the accessibility information is correct.

</details>

### Q16. What is the difference between `get_by_text()`, `get_by_label()`, and `get_by_placeholder()`?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

- `get_by_text()` finds elements by visible text.
- `get_by_label()` finds form controls associated with a label.
- `get_by_placeholder()` finds form controls by placeholder text.

```python
page.get_by_text("Welcome")
page.get_by_label("Email address").fill("a@example.com")
page.get_by_placeholder("Enter password").fill("secret")
```

</details>

### Q17. How would you handle multiple elements matching the same locator?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

First make the locator more specific using a role and accessible name, a parent container, a filter, or a stable attribute. If the elements are intentionally repeated, use `.nth()`, `.first`, or `.last` only when their order is meaningful and reliable.

```python
save_buttons = page.get_by_role("button", name="Save")
save_buttons.nth(1).click()
```

</details>

### Q18. What is the difference between `first`, `last`, and `nth()` in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

They select one element from a locator that matches multiple elements:
- `.first` selects the first.
- `.last` selects the last.
- `.nth(index)` selects the element at a zero-based index.

```python
items = page.get_by_role("listitem")
items.first.click()
items.nth(2).click()  # third item
items.last.click()
```

Use these only when position is a valid part of the requirement.

</details>

---

## 3. Auto-waiting and debugging

### Q19. What is auto-waiting in Playwright, and how does it work?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Before performing an action such as `click()`, Playwright waits for the locator to resolve to an appropriate element and for the relevant actionability checks to pass. This reduces the need for fixed sleeps.

Auto-waiting is not a guarantee that every application workflow is complete. For example, after clicking Save, the test may still need to wait for a confirmation message using a web-first assertion.

</details>

### Q20. What are the different actionability checks Playwright performs before interacting with an element?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

For a click, Playwright checks that the element is unique for the locator, visible, stable, receives events, and is enabled. Different actions have different requirements. For example, filling an input has its own checks.

</details>

### Q21. What is the difference between implicit waits and explicit waits? How does Playwright's waiting mechanism differ?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Selenium users often discuss implicit waits configured for element lookup and explicit waits for particular conditions. Playwright instead builds auto-waiting into locator actions and provides retrying assertions such as `expect(locator).to_be_visible()`.

A fixed sleep such as `page.wait_for_timeout(5000)` waits for a fixed period and is usually less reliable than waiting for a meaningful condition.

</details>

### Q22. What is Playwright Inspector, and how can it help with debugging?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Playwright Inspector is an interactive debugging tool. It can pause execution, show the current page, let a tester inspect locators, and step through actions. It is useful for understanding why a locator or action is failing.

With Python, one common way to open the inspector is:

```bash
PWDEBUG=1 pytest -s
```

On Windows PowerShell:

```powershell
$env:PWDEBUG="1"
pytest -s
```

</details>

### Q23. How do you record and play back user interactions using Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use Codegen to record browser interactions and generate code. Review and improve the generated code, then run the saved script or convert the useful actions into Pytest tests. Generated scripts are a starting point, not necessarily production-quality tests.

</details>

### Q24. What is Playwright Codegen, and how do you use it to generate automation scripts?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Codegen opens a browser and records actions, generating Playwright code and locators.

```bash
playwright codegen https://example.com
```

You can also choose a browser or output file, for example:

```bash
playwright codegen --browser chromium -o recorded_test.py https://example.com
```

Review the generated code for robust locators, assertions, reusable functions, and test data before using it in a framework.

</details>

### Q25. What is the difference between Playwright Inspector and Codegen?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Codegen records user actions and generates code. Inspector is primarily an interactive debugging and locator-inspection tool that can pause and step through a running test. They are related tools, but they serve different purposes.

</details>

---

## 4. Handling web elements

### Q26. How do you handle JavaScript alerts, confirmation dialogs, and prompt dialogs in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Playwright emits a `dialog` event. Register a handler before the action that triggers the dialog. Accept or dismiss it, and provide text for a prompt if needed.

```python
def test_confirmation_dialog(page):
    page.goto("https://example.com/dialog-demo")

    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()
```

To dismiss:

```python
page.once("dialog", lambda dialog: dialog.dismiss())
```

</details>

### Q27. How do you handle radio buttons and checkboxes?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use a label, role, or locator and interact with `check()` and `uncheck()`. These methods are idempotent compared with blindly clicking a checkbox.

```python
page.get_by_label("I agree to the terms").check()
page.get_by_label("Email notifications").uncheck()
page.get_by_label("Monthly plan").check()
```

You can verify state with `expect(locator).to_be_checked()`.

</details>

### Q28. How do you handle standard dropdowns and multi-select dropdowns?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

For a native HTML `<select>`, use `select_option()`. A custom dropdown built from `div`, `li`, or buttons should be treated like ordinary web elements: open it and select the desired option.

```python
page.get_by_label("Country").select_option(label="India")
page.locator("#colors").select_option(["red", "blue"])
```

The second example assumes a native multi-select element. `select_option()` does not directly operate a custom JavaScript dropdown.

</details>

### Q29. How do you perform keyboard actions in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `keyboard` or locator keyboard methods.

```python
page.keyboard.press("Enter")
page.keyboard.press("Control+A")
page.get_by_label("Search").press("Enter")
page.get_by_label("Search").press_sequentially("Playwright")
```

Key names and modifier combinations are documented by Playwright.

</details>

### Q30. How do you perform mouse actions such as hover, click, double-click, and right-click?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use locator actions or the page mouse API.

```python
menu = page.get_by_text("Products")
menu.hover()

button = page.get_by_role("button", name="Open")
button.dblclick()

page.get_by_text("Item").click(button="right")
page.mouse.move(200, 300)
```

Prefer locator-based actions when possible because they are tied to a meaningful element.

</details>

### Q31. What are auto-suggestions, and how would you handle an auto-suggestion dropdown?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Auto-suggestions are options displayed as a user types into a field. Fill the input, wait for the suggestions to appear using a locator assertion, then choose the intended suggestion.

```python
search = page.get_by_placeholder("Search city")
search.fill("Jaba")

suggestions = page.get_by_role("option")
expect(suggestions.first).to_be_visible()
page.get_by_role("option", name="Jabalpur").click()
```

The exact role and locator depend on the application's HTML and accessibility structure.

</details>

### Q32. What is Shadow DOM, and how does Playwright interact with elements inside Shadow DOM?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Shadow DOM is a browser feature that lets a component encapsulate its DOM and styles. Playwright's locators generally pierce open shadow roots automatically. XPath does not pierce shadow roots. Closed shadow roots are not accessible through ordinary page locators.

</details>

### Q33. How do you handle dynamic web elements in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use stable attributes, accessible roles, labels, text, test IDs, and locator filters. Avoid generated IDs and fixed sleeps. Use retrying assertions to wait for expected state.

```python
save_button = page.get_by_role("button", name="Save")
expect(save_button).to_be_visible()
save_button.click()
```

</details>

### Q34. How do you handle iframes and nested frames in Playwright?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Use `frame_locator()` to locate elements inside a frame. For nested frames, chain frame locators.

```python
payment_frame = page.frame_locator("iframe#payment")
payment_frame.get_by_label("Card number").fill("4111111111111111")
```

For nested frames:

```python
outer = page.frame_locator("iframe#outer")
inner = outer.frame_locator("iframe#inner")
inner.get_by_role("button", name="Continue").click()
```

Use stable frame selectors or frame APIs if the frame has no useful selector.

</details>

### Q35. How do you identify and interact with elements inside a frame?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `page.frame_locator("iframe-selector")` and then use normal locators within that frame.

```python
frame = page.frame_locator("iframe[name='address']")
frame.get_by_label("Postal code").fill("482001")
```

</details>

### Q36. How do you read data from HTML web tables?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Locate the table, rows, and cells. Use row and cell locators, then read text with `inner_text()` or `text_content()`.

```python
table = page.get_by_role("table", name="Orders")
rows = table.locator("tbody tr")

for row in rows.all():
    print(row.inner_text())
```

</details>

### Q37. How would you retrieve a particular row or column value from a web table?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Find the header index, then read that cell from each row. Check the table structure and account for header cells, hidden columns, and nested tables.

```python
table = page.locator("#orders")
headers = table.locator("thead th").all_text_contents()
column_index = headers.index("Status")

statuses = [
    row.locator("td").nth(column_index).inner_text()
    for row in table.locator("tbody tr").all()
]
```

This example assumes each data row has cells in the same order as the headers.

</details>

### Q38. How do you handle date pickers and select a specific date?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

First determine whether the control is a native date input or a custom calendar widget.

For a native date input:

```python
page.locator("input[type='date']").fill("2026-11-14")
```

For a custom calendar, open it, inspect the displayed month/year, navigate to the target month, and select the date using an accessible name or stable locator. Avoid selecting a day by text alone if the calendar shows dates from adjacent months.

</details>

### Q39. How do you handle multiple tabs and browser windows?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use the `expect_page()` context manager before the action that opens the new page.

```python
with page.expect_popup() as popup_info:
    page.get_by_role("link", name="Open report").click()

popup = popup_info.value
popup.wait_for_load_state()
assert "report" in popup.url
```

In Playwright, a new tab and a popup are both represented as `Page` objects.

</details>

### Q40. How do you identify and switch between newly opened pages in Playwright?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Capture the new page event before triggering the action:

```python
with page.context.expect_page() as new_page_info:
    page.get_by_role("button", name="Open tab").click()

new_page = new_page_info.value
new_page.wait_for_load_state()
new_page.get_by_role("heading", name="Details").wait_for()
```

There is no Selenium-style driver-window switch command. Use the `Page` object returned by the event.

</details>

---

## 5. Navigation and file handling

### Q41. What are navigation events in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Navigation events describe page navigation, such as loading a new document or changing the URL. Playwright offers navigation and load-state waiting APIs. Modern applications may update content without a full document navigation, so a URL or element assertion may be more appropriate than waiting for a load event.

</details>

### Q42. How do you wait for a page navigation or URL change?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

For a navigation caused by a click, register the wait before the action:

```python
with page.expect_navigation():
    page.get_by_role("link", name="Products").click()
```

For URL changes in single-page applications, use a web-first URL assertion:

```python
expect(page).to_have_url("**/products")
```

Depending on the application and Playwright version, `expect_navigation()` may not be the best choice for client-side routing. Prefer waiting for the user-visible destination state.

</details>

### Q43. What is the difference between `page.goto()`, `page.reload()`, and `page.go_back()`?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

- `goto(url)` navigates to a specified URL.
- `reload()` reloads the current page.
- `go_back()` navigates to the previous history entry when one exists.

Related methods include `go_forward()`.

</details>

### Q44. How do you handle file downloads in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Register the download expectation before clicking the download control. Then save the downloaded file.

```python
with page.expect_download() as download_info:
    page.get_by_role("link", name="Download CSV").click()

download = download_info.value
download.save_as("downloads/report.csv")
```

Create the destination directory first if it does not exist.

</details>

### Q45. How can you verify that a downloaded file exists and contains the expected data?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Save the download to a known path, verify the file exists, then inspect its content using the appropriate parser.

```python
from pathlib import Path
import csv

def test_download_csv(page, tmp_path):
    with page.expect_download() as info:
        page.get_by_role("button", name="Export").click()

    download = info.value
    file_path = tmp_path / download.suggested_filename
    download.save_as(file_path)

    assert file_path.exists()

    with file_path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows
    assert "Order ID" in rows[0]
```

The expected column name should match the actual CSV format.

</details>

---

## 6. Assertions in Playwright

### Q46. What are assertions in Playwright, and why are they important?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Assertions verify that the application behaves as expected. They help a test detect incorrect page content, state, navigation, or interaction results.

</details>

### Q47. What is the difference between Pytest assertions and Playwright's built-in assertions?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Pytest assertions are ordinary Python `assert` statements and evaluate immediately. Playwright's `expect()` assertions are web-first assertions: they retry until the condition passes or the assertion timeout expires.

```python
assert page.title() == "Dashboard"  # immediate Python assertion
expect(page.get_by_text("Welcome")).to_be_visible()  # retrying assertion
```

</details>

### Q48. What is the purpose of `expect()` in Playwright?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

`expect()` provides retrying assertions for pages and locators. It is useful for checking conditions that may take time to become true, such as an element becoming visible or a URL changing.

```python
from playwright.sync_api import expect

expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
```

</details>

### Q49. What is the difference between `to_be_visible()`, `to_be_enabled()`, and `to_be_checked()`?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

- `to_be_visible()` verifies that the element is visible.
- `to_be_enabled()` verifies that the element is enabled.
- `to_be_checked()` verifies that a checkbox or radio button is checked.

Each is a retrying assertion.

</details>

### Q50. What are auto-retrying assertions in Playwright?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Auto-retrying assertions repeatedly check a condition until it passes or times out. They help handle asynchronous UI updates without hard-coded sleeps.

Examples include `to_be_visible()`, `to_have_text()`, `to_be_enabled()`, and `to_have_url()`.

</details>

### Q51. How do you verify page titles, URLs, text, and element visibility?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `expect()` for retrying assertions:

```python
expect(page).to_have_title("Dashboard")
expect(page).to_have_url("**/dashboard")
expect(page.get_by_role("heading")).to_have_text("Welcome")
expect(page.get_by_role("button", name="Save")).to_be_visible()
```

</details>

---

## 7. Fixtures and hooks

### Q52. What are fixtures in Playwright with Python?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

In a Playwright Python + Pytest project, fixtures provide reusable setup and resources to tests. The `pytest-playwright` plugin supplies browser-related fixtures, and teams can create custom Pytest fixtures for application setup, login, test data, or cleanup.

</details>

### Q53. What are the built-in fixtures provided by the `pytest-playwright` plugin?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Common fixtures include `page`, `context`, `browser`, `browser_name`, and `playwright`. Other fixtures and behavior may depend on plugin version and configuration. Consult the installed plugin documentation for the exact available fixture set.

</details>

### Q54. What is the purpose of the `page` and `browser` fixtures?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

The `page` fixture provides a page (tab) ready for use in a test. The `browser` fixture provides access to the launched browser instance. A test can use `page` directly for common UI automation; use `browser` when it needs to create contexts or pages with custom settings.

</details>

### Q55. What is the difference between the `page`, `context`, and `browser` fixtures?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

- `page`: a tab.
- `context`: an isolated browser session that can contain multiple pages.
- `browser`: the browser process/instance.

The context controls session-level state such as cookies and permissions.

</details>

### Q56. How do you create custom fixtures in a Playwright Python project?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `@pytest.fixture` and request the built-in `page` fixture or another fixture.

```python
import pytest

@pytest.fixture
def logged_in_page(page):
    page.goto("https://example.com/login")
    page.get_by_label("Username").fill("demo")
    page.get_by_label("Password").fill("password")
    page.get_by_role("button", name="Sign in").click()
    return page
```

In a real project, use test accounts and secure credential handling.

</details>

### Q57. How can you share Playwright fixtures across multiple test files?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Place shared fixtures in a `conftest.py` file in a common parent test directory. Pytest automatically discovers fixtures from applicable `conftest.py` files.

</details>

### Q58. What is the role of `conftest.py` in a Playwright automation framework?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

It holds shared Pytest fixtures and hooks for the test directory tree. It is a common place for reusable login, test-data, configuration, and application setup fixtures. Tests request fixtures by name; they do not import them from `conftest.py`.

</details>

### Q59. What are Pytest hooks, and how can they be used in a Playwright project?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Hooks are extension points in Pytest's execution lifecycle. They let a framework customize collection, setup, reporting, or teardown. For example, a project can add metadata to reports or capture diagnostics on failures. Hooks are different from fixtures: fixtures provide dependencies and manage setup/teardown for tests, while hooks integrate with Pytest's lifecycle.

</details>

### Q60. What is the difference between fixtures and hooks in Pytest?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Fixtures provide reusable values/resources and manage setup and teardown. Hooks are callback functions invoked by Pytest at defined points in its lifecycle. Use fixtures for browser/page/test-data dependencies and hooks for framework-level behavior such as report customization or failure diagnostics.

</details>

### Q61. How do you perform browser and page cleanup after test execution?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

When using `pytest-playwright`'s built-in fixtures, the plugin manages the lifecycle of the browser-related resources it creates. For custom resources, use fixtures with `yield` and put cleanup after the yield. If your test creates additional contexts or pages manually, close resources you own.

```python
import pytest

@pytest.fixture
def extra_context(browser):
    context = browser.new_context()
    yield context
    context.close()
```

Do not close a plugin-managed `page` or `browser` manually unless your framework explicitly owns that lifecycle.

</details>

---

## 8. Framework design and Page Object Model

### Q62. What is the Page Object Model (POM), and why is it used in automation frameworks?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

POM is a design pattern in which each page or major page component is represented by a class. The class contains locators and actions for that part of the application. It improves reuse and keeps test intent separate from page implementation details.

</details>

### Q63. How would you implement the Page Object Model using Playwright with Python?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Create a page class that receives a Playwright `Page`, defines locators, and exposes meaningful actions.

```python

</details>

# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.sign_in = page.get_by_role("button", name="Sign in")

    def open(self):
        self.page.goto("https://example.com/login")

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.sign_in.click()
```

### Q64. How would you convert an existing Playwright test script into a Page Object Model structure?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Identify the page-specific locators and repeated actions. Move them into page classes, pass the `Page` object into each class, and keep test assertions and scenario intent in test files. Avoid moving every assertion into a page class; page objects should model page behavior, while tests should describe expected outcomes.

</details>

### Q65. What are the advantages of separating page locators and page actions from test cases?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

It reduces duplication, improves readability, and makes maintenance easier. If a locator changes, it can often be updated in one page class instead of many tests.

</details>

### Q66. How would you organize a Playwright Python automation framework?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

A simple structure could be:

```text
project/
├── pages/
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   └── test_dashboard.py
├── test_data/
│   └── users.json
├── utils/
│   └── data_reader.py
├── pytest.ini
└── requirements.txt
```

Keep page objects, test cases, test data, configuration, and helper utilities separated without overengineering a small project.

</details>

### Q67. How would you manage common methods such as login, logout, and navigation in a framework?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Place page-specific actions in their relevant page objects. Shared workflows can be represented by a service/workflow helper or a fixture, depending on the use case. Avoid putting every action into one giant base page class.

</details>

---

## 9. Data-driven testing

### Q68. What is data-driven testing, and why is it useful in Playwright automation?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Data-driven testing runs the same test logic with multiple input sets. It is useful for checking valid, invalid, boundary, and alternate user data without duplicating test functions.

</details>

### Q69. How can you implement data-driven testing using Pytest parameterization?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `@pytest.mark.parametrize` to provide multiple data sets to the same test function.

```python
import pytest

@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("valid_user", "valid_pass", "Welcome"),
        ("valid_user", "wrong_pass", "Invalid credentials"),
    ],
)
def test_login(page, username, password, expected):
    # Interact with the real login page and assert the expected result.
    ...
```

</details>

### Q70. How do you read test data from a JSON file in Python?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use Python's built-in `json` module.

```python
import json
from pathlib import Path

data_path = Path("test_data/users.json")
users = json.loads(data_path.read_text(encoding="utf-8"))
```

For a project, build the path relative to a known project location rather than relying on the current working directory.

</details>

### Q71. How would you pass JSON test data to a Playwright test?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Read the JSON data and pass the records to a parameterized test or a fixture. Validate the data structure so missing keys are reported clearly.

```python
import json
from pathlib import Path
import pytest

users = json.loads(
    (Path(__file__).parent / "test_data" / "users.json").read_text(
        encoding="utf-8"
    )
)

@pytest.mark.parametrize("user", users)
def test_login_data(page, user):
    page.goto("https://example.com/login")
    page.get_by_label("Username").fill(user["username"])
    page.get_by_label("Password").fill(user["password"])
    page.get_by_role("button", name="Sign in").click()
    # Add an assertion based on the expected outcome in the JSON record.
```

</details>

### Q72. How would you execute the same login test with multiple sets of usernames and passwords?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use parameterization or load a list of records from JSON. Each record should include the credentials and the expected result, so the test verifies behavior rather than just submitting different values.

</details>

---

## 10. Test execution, retries, and reporting

### Q73. What are test retries, and why might we use them in automation testing?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

A retry reruns a failed test according to a configured policy. It can help identify intermittent failures, but it should not hide real defects or replace fixing flaky tests. Report both the initial failure and retry outcome where possible.

</details>

### Q74. How can you configure test retries when using Pytest with Playwright?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

One option is the `pytest-rerunfailures` plugin:

```bash
pip install pytest-rerunfailures
pytest --reruns 2
```

You can also configure reruns for selected tests using markers supported by the plugin. Check the installed plugin version for its current options.

</details>

### Q75. What is the difference between rerunning failed tests and retrying a test during execution?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

A retry policy reruns a test after a failure within the same test run. A separate rerun may be a later command or CI job that selects failed tests from a previous run. Both can help investigate intermittent failures, but they should preserve the original failure information.

</details>

### Q76. How do you execute Playwright tests across different browsers such as Chromium, Firefox, and WebKit?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Install the browser binaries and use the plugin's browser option:

```bash
playwright install
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

To run the suite separately on all three, invoke the commands in a CI matrix or script. The exact browser names/options are those supported by the installed plugin.

</details>

### Q77. How do you execute tests in headed and headless modes?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

The plugin runs headless by default in common configurations. Use `--headed` to show the browser window:

```bash
pytest --headed
```

</details>

### Q78. How can you generate HTML reports for Playwright tests using Pytest?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Install `pytest-html` and run:

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

Playwright's trace, screenshot, and video artifacts are separate diagnostics and can be attached or linked through suitable plugin configuration or report hooks.

</details>

### Q79. What information can you obtain from a Playwright test execution report?
**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

A report commonly shows test names, pass/fail/skip outcomes, durations, and failure tracebacks. Depending on configuration, it may also include environment details, logs, screenshots, videos, or links to traces.

</details>

### Q80. How can you capture screenshots when a test fails?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

You can take a screenshot explicitly in a fixture or failure hook. The plugin may also support screenshot capture options. For example, a simple fixture can save a screenshot when the test call fails:

```python
import pytest

@pytest.fixture
def page_with_failure_screenshot(page, request):
    yield page
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        page.screenshot(path=f"artifacts/{request.node.name}.png")
```

This illustrative fixture requires the test result to be attached to `request.node` by a `pytest_runtest_makereport` hook and requires the `artifacts` directory to exist. A complete hook example is provided in the practical section.

</details>

### Q81. What is the purpose of tracing in Playwright, and how can it help debug test failures?
**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

A trace records information about a test run, such as actions, snapshots, screenshots, and network activity (depending on configuration). Trace Viewer lets a tester inspect what happened around a failure. With `pytest-playwright`, tracing can be enabled through plugin options such as `--tracing`; check the installed plugin's help/documentation for supported modes.

</details>

---

<a id="scenario-based-questions"></a>

# Part 2 – Scenario-based interview questions with answers and solutions

## Scenario 1 – Element is not immediately available
**Q82. Your test fails because an element is not immediately available after opening a page. How would you handle it?**

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Avoid adding a fixed sleep as the first solution. Use a locator and a retrying assertion, then perform the action. Playwright auto-waits for actionability when performing actions.

```python
from playwright.sync_api import expect

def test_open_dashboard(page):
    page.goto("https://example.com")
    dashboard = page.get_by_role("heading", name="Dashboard")

    expect(dashboard).to_be_visible()
    expect(dashboard).to_have_text("Dashboard")
```

If the page is waiting for a backend response, consider waiting for a meaningful UI state or, when justified, the specific response.

</details>

## Scenario 2 – Login with multiple usernames and passwords
**Q83. You need to test login functionality with multiple usernames and passwords. How would you implement it?**

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use Pytest parameterization. Include expected outcomes with each set of credentials.

```python
import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize(
    "username,password,expected_message",
    [
        ("standard_user", "secret1", "Welcome"),
        ("locked_user", "secret2", "Account locked"),
        ("unknown_user", "wrong", "Invalid credentials"),
    ],
)
def test_login(page, username, password, expected_message):
    page.goto("https://example.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()

    expect(page.get_by_role("alert")).to_contain_text(expected_message)
```

The URL, labels, and expected messages are illustrative; adapt them to the application.

</details>

## Scenario 3 – Multiple buttons with the same name
**Q84. Your application contains multiple buttons named "Submit". How would you identify the correct one?**

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Scope the locator to a meaningful parent section or use a unique accessible name/test ID. Avoid selecting the second button simply because it happens to be second unless position is part of the requirement.

```python
checkout = page.get_by_role("region", name="Checkout")
checkout.get_by_role("button", name="Submit").click()
```

Another option is filtering a parent locator:

```python
payment_panel = page.locator("#payment-panel")
payment_panel.get_by_role("button", name="Submit").click()
```

</details>

## Scenario 4 – API unavailable during testing
**Q85. An external API is unavailable during testing. How would you test the UI without depending on the real API?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Mock the network response with Playwright routing. This lets the UI receive deterministic test data without calling the unavailable service.

```python
def test_products_with_mocked_api(page):
    page.route(
        "**/api/products",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[{"id": 1, "name": "Keyboard"}]',
        ),
    )

    page.goto("https://example.com/products")

    page.get_by_text("Keyboard").wait_for()
    assert page.get_by_text("Keyboard").is_visible()
```

For an API failure scenario, fulfill with a suitable error status or abort the request and assert that the UI displays the expected error state. Mock only the dependency relevant to the test.

</details>

## Scenario 5 – Pytest execution takes too much time
**Q86. Your Playwright test suite takes too long to execute. What would you do?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Possible improvements:
- Identify slow tests using durations and reports.
- Avoid unnecessary fixed waits and repeated setup.
- Use efficient, appropriately scoped fixtures.
- Run independent tests in parallel with a suitable tool such as `pytest-xdist`, after checking test isolation.
- Reduce redundant end-to-end coverage and move suitable checks to API or unit tests.
- Reuse authentication state safely where appropriate.
- Avoid sharing mutable browser state between tests.

Example:

```bash
pip install pytest-xdist
pytest -n auto
```

Parallel execution is not automatically safe: tests must not conflict over shared accounts, records, files, or environment state.

</details>

## Scenario 6 – Test passes individually but fails in the full suite
**Q87. A test passes alone but fails when the entire suite runs. What could be the reason?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Likely causes include shared state, test-order dependency, reused accounts or data, incomplete cleanup, fixture scope problems, parallel test conflicts, or environment/network instability.

Investigate by:
1. Running the failing test with verbose output.
2. Running it with related tests.
3. Checking fixture scopes and cleanup.
4. Ensuring each test creates or owns its test data.
5. Repeating the suite with and without parallel execution.
6. Reviewing traces, screenshots, and logs.

Tests should be independent and repeatable.

</details>

## Scenario 7 – Dynamic element whose ID changes
**Q88. An element's ID changes every time the page loads. How would you locate it reliably?**

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Do not depend on the changing ID. Prefer role, label, placeholder, visible text, stable attributes, or a test ID. If part of an attribute is stable, use a partial CSS attribute selector.

```python
page.get_by_role("button", name="Continue").click()

</details>

# If a stable prefix exists:
page.locator("[id^='customer-field-']").fill("Asha")
```

The best locator depends on the actual DOM and should uniquely identify the intended element.

## Scenario 8 – Cross-browser execution
**Q89. You need to execute the same test cases in Chromium, Firefox, and WebKit. How would you configure the framework?**

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Install the browsers and run the suite once per browser using the plugin option. In CI, define a browser matrix so the same tests execute for each browser.

```bash
playwright install
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

Check browser-specific behavior and avoid assuming all engines render every feature identically.

</details>

## Scenario 9 – Browser and page cleanup
**Q90. You create additional browser contexts and pages during testing. How would you ensure they are cleaned up?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Use a fixture with `yield` and close the context in teardown. Closing a context also closes its pages.

```python
import pytest

@pytest.fixture
def second_context(browser):
    context = browser.new_context()
    yield context
    context.close()

def test_second_user(second_context):
    page = second_context.new_page()
    page.goto("https://example.com")
    assert page.title()
```

The plugin manages the lifecycle of its own `page` and `context` fixtures. Close manually created resources that your test or fixture owns.

</details>

---

# Part 3 – Practical coding exercises with complete solutions

These exercises can be used in a live interview. The sample URLs and locators are illustrative; use a practice application or the candidate's test environment.

## Exercise 1 – Open a website and verify its title
**Level: Beginner**

**Ask:** Write a test that opens a website and verifies its title.

```python
from playwright.sync_api import expect

def test_homepage_title(page):
    page.goto("https://example.com")
    expect(page).to_have_title("Example Domain")
```

**Evaluate:** navigation, fixture usage, and assertion syntax.

## Exercise 2 – Fill a login form and submit it
**Level: Beginner**

**Ask:** Locate username and password fields, enter values, and click Sign in.

```python
def test_login_form(page):
    page.goto("https://example.com/login")
    page.get_by_label("Username").fill("demo_user")
    page.get_by_label("Password").fill("demo_password")
    page.get_by_role("button", name="Sign in").click()
```

**Evaluate:** locator choice, form interactions, and readable code. A complete test should also assert the result.

## Exercise 3 – Select an option from a dropdown
**Level: Beginner**

**Ask:** Select India from a native country dropdown and verify the selection.

```python
from playwright.sync_api import expect

def test_select_country(page):
    page.goto("https://example.com/profile")
    country = page.get_by_label("Country")
    country.select_option(label="India")
    expect(country).to_have_value("IN")
```

This assumes the option's underlying value is `IN`. For a custom dropdown, click the control and select the option as a normal element.

## Exercise 4 – Handle a JavaScript confirmation dialog
**Level: Beginner**

**Ask:** Click Delete, accept the confirmation dialog, and verify the result.

```python
from playwright.sync_api import expect

def test_delete_confirmation(page):
    page.goto("https://example.com/items")
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()
    expect(page.get_by_text("Item deleted")).to_be_visible()
```

**Evaluate:** event registration before the triggering action.

## Exercise 5 – Open a new tab and verify it
**Level: Beginner**

**Ask:** Click a link that opens a new tab and verify the new page.

```python
def test_open_new_tab(page):
    page.goto("https://example.com")

    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Open report").click()

    report_page = popup_info.value
    report_page.wait_for_load_state()
    assert "report" in report_page.url
```

**Evaluate:** event synchronization and page objects.

## Exercise 6 – Read a value from a web table
**Level: Intermediate**

**Ask:** Find the row for order 1002 and verify its status.

```python
from playwright.sync_api import expect

def test_order_status(page):
    page.goto("https://example.com/orders")
    row = page.get_by_role("row").filter(has_text="1002")
    expect(row).to_contain_text("Shipped")
```

This is a concise approach when the row text uniquely identifies the record. For more precise checks, locate the Status cell by its column index.

## Exercise 7 – Select an auto-suggestion
**Level: Beginner**

**Ask:** Enter a city prefix and select the matching suggestion.

```python
from playwright.sync_api import expect

def test_city_autocomplete(page):
    page.goto("https://example.com/search")
    city = page.get_by_label("City")
    city.fill("Jaba")

    suggestion = page.get_by_role("option", name="Jabalpur")
    expect(suggestion).to_be_visible()
    suggestion.click()

    expect(city).to_have_value("Jabalpur")
```

**Evaluate:** waiting for asynchronous suggestions and selecting a specific result.

## Exercise 8 – Create a simple Login Page Object
**Level: Intermediate**

**Ask:** Convert login locators and actions into a page class.

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.submit = page.get_by_role("button", name="Sign in")

    def open(self):
        self.page.goto("https://example.com/login")

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()
```

Test:

```python
from playwright.sync_api import expect
from pages.login_page import LoginPage

def test_valid_login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("demo", "password")
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
```

**Evaluate:** separation of page behavior from test assertions.

## Exercise 9 – Run a login test with multiple data sets
**Level: Beginner**

**Ask:** Use Pytest parameterization to test valid and invalid credentials.

```python
import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize(
    "username,password,message",
    [
        ("valid_user", "valid_pass", "Welcome"),
        ("valid_user", "wrong_pass", "Invalid credentials"),
        ("unknown", "wrong", "Invalid credentials"),
    ],
)
def test_login_data(page, username, password, message):
    page.goto("https://example.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_role("alert")).to_contain_text(message)
```

**Evaluate:** data-driven test design and meaningful expected results.

## Exercise 10 – Handle an iframe
**Level: Intermediate**

**Ask:** Locate a text field inside an iframe and enter a value.

```python
def test_address_frame(page):
    page.goto("https://example.com/address")
    address_frame = page.frame_locator("iframe#address-frame")
    address_frame.get_by_label("Street").fill("10 Main Road")
```

**Evaluate:** frame locator syntax and scoping.

## Exercise 11 – Mock an API response
**Level: Intermediate**

**Ask:** Intercept a products API and provide deterministic data to the UI.

```python
def test_products_api_mock(page):
    page.route(
        "**/api/products",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[{"id": 1, "name": "Keyboard"}]',
        ),
    )
    page.goto("https://example.com/products")
    page.get_by_text("Keyboard").wait_for()
    assert page.get_by_text("Keyboard").is_visible()
```

**Evaluate:** route interception and deterministic UI testing.

## Exercise 12 – Capture a screenshot on test failure
**Level: Intermediate**

**Ask:** Use a Pytest hook to capture a screenshot when a test's call phase fails.

```python
# conftest.py
from pathlib import Path
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

@pytest.fixture
def page_with_screenshot(page, request):
    yield page

    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        artifact_dir = Path("artifacts")
        artifact_dir.mkdir(exist_ok=True)
        page.screenshot(
            path=str(artifact_dir / f"{request.node.name}.png"),
            full_page=True,
        )
```

Test:

```python
def test_example(page_with_screenshot):
    page_with_screenshot.goto("https://example.com")
    assert page_with_screenshot.title() == "An incorrect title"
```

**Important:** This example captures failures in the test call phase. Setup failures and teardown failures need separate handling if the framework must capture those too. In a production framework, use unique artifact names to avoid collisions during parallel execution.

---

# Part 4 – Quick reference commands

| Goal | Command |
|---|---|
| Install Python Playwright | `pip install playwright` |
| Install Pytest integration | `pip install pytest-playwright` |
| Install browser binaries | `playwright install` |
| Run all tests | `pytest` |
| Run one file | `pytest tests/test_login.py` |
| Run one test | `pytest tests/test_login.py::test_valid_login` |
| Run with visible browser | `pytest --headed` |
| Run with Chromium | `pytest --browser chromium` |
| Run with Firefox | `pytest --browser firefox` |
| Run with WebKit | `pytest --browser webkit` |
| Open Codegen | `playwright codegen https://example.com` |
| Debug with Inspector (macOS/Linux) | `PWDEBUG=1 pytest -s` |
| Debug with Inspector (PowerShell) | `$env:PWDEBUG="1"; pytest -s` |
| Generate HTML report | `pytest --html=report.html --self-contained-html` |
| Show slowest tests | `pytest --durations=10` |
| Run in parallel (after checking isolation) | `pytest -n auto` |

For the full set of options supported by the installed plugin, use:

```bash
pytest --help
```

---

# Part 5 – Question-by-question difficulty classification

| Question | Topic (short form) | Level |
|---:|---|---|
| 1 | What is Playwright? | Beginner |
| 2 | Features and advantages | Beginner |
| 3 | Playwright architecture | Intermediate |
| 4 | Browser vs context vs page | Beginner |
| 5 | Integrating Playwright with Pytest | Beginner |
| 6 | `pytest-playwright` plugin | Beginner |
| 7 | Playwright Test Runner vs Pytest | Intermediate |
| 8 | Locators | Beginner |
| 9 | Locator strategies | Beginner |
| 10 | CSS selectors | Beginner |
| 11 | Attribute selectors | Beginner |
| 12 | CSS pseudo-classes | Intermediate |
| 13 | Dynamic selectors | Intermediate |
| 14 | CSS vs XPath | Beginner |
| 15 | `locator()` vs `get_by_role()` | Beginner |
| 16 | Text, label and placeholder locators | Beginner |
| 17 | Multiple matching elements | Beginner |
| 18 | `first`, `last`, `nth()` | Beginner |
| 19 | Auto-waiting | Beginner |
| 20 | Actionability checks | Intermediate |
| 21 | Wait strategies | Intermediate |
| 22 | Inspector | Beginner |
| 23 | Recording and playback | Beginner |
| 24 | Codegen | Beginner |
| 25 | Inspector vs Codegen | Intermediate |
| 26 | Alerts and dialogs | Beginner |
| 27 | Radio buttons and checkboxes | Beginner |
| 28 | Dropdowns and multi-selects | Beginner |
| 29 | Keyboard actions | Beginner |
| 30 | Mouse actions | Beginner |
| 31 | Auto-suggestions | Beginner |
| 32 | Shadow DOM | Intermediate |
| 33 | Dynamic elements | Beginner |
| 34 | Frames and nested frames | Intermediate |
| 35 | Elements inside frames | Beginner |
| 36 | Reading web tables | Beginner |
| 37 | Specific table row/column values | Intermediate |
| 38 | Date pickers | Intermediate |
| 39 | Multiple tabs and windows | Beginner |
| 40 | Capturing new pages | Intermediate |
| 41 | Navigation events | Beginner |
| 42 | Waiting for navigation/URL changes | Intermediate |
| 43 | `goto`, `reload`, `go_back` | Beginner |
| 44 | File downloads | Beginner |
| 45 | Validating downloaded files | Intermediate |
| 46 | Assertions | Beginner |
| 47 | Pytest vs Playwright assertions | Intermediate |
| 48 | `expect()` | Beginner |
| 49 | Visibility, enabled and checked assertions | Beginner |
| 50 | Auto-retrying assertions | Intermediate |
| 51 | Verifying title, URL, text and visibility | Beginner |
| 52 | Fixtures in Playwright Python | Beginner |
| 53 | Plugin-provided fixtures | Intermediate |
| 54 | `page` and `browser` fixtures | Beginner |
| 55 | Page vs context vs browser fixtures | Beginner |
| 56 | Custom fixtures | Beginner |
| 57 | Sharing fixtures | Beginner |
| 58 | `conftest.py` | Beginner |
| 59 | Pytest hooks | Intermediate |
| 60 | Fixtures vs hooks | Intermediate |
| 61 | Browser/page cleanup | Intermediate |
| 62 | Page Object Model | Beginner |
| 63 | Implementing POM | Intermediate |
| 64 | Refactoring scripts into POM | Intermediate |
| 65 | Separating locators/actions from tests | Beginner |
| 66 | Framework organization | Intermediate |
| 67 | Managing common workflows | Intermediate |
| 68 | Data-driven testing | Beginner |
| 69 | Pytest parameterization | Beginner |
| 70 | Reading JSON | Beginner |
| 71 | Passing JSON data to tests | Intermediate |
| 72 | Multiple login data sets | Beginner |
| 73 | Test retries | Beginner |
| 74 | Configuring retries | Intermediate |
| 75 | Retry vs later rerun | Intermediate |
| 76 | Cross-browser execution | Beginner |
| 77 | Headed vs headless | Beginner |
| 78 | HTML reports | Beginner |
| 79 | Report contents | Beginner |
| 80 | Screenshots on failure | Intermediate |
| 81 | Playwright tracing | Intermediate |
| 82 | Element not immediately available | Beginner |
| 83 | Login with multiple credentials | Beginner |
| 84 | Multiple buttons with same name | Beginner |
| 85 | API unavailable / mock response | Intermediate |
| 86 | Slow test suite | Intermediate |
| 87 | Passes alone, fails in suite | Intermediate |
| 88 | Dynamic ID | Beginner |
| 89 | Cross-browser execution scenario | Beginner |
| 90 | Browser/page cleanup scenario | Intermediate |

## Practical exercise difficulty

| Exercise | Topic | Level |
|---:|---|---|
| 1 | Verify page title | Beginner |
| 2 | Fill and submit login form | Beginner |
| 3 | Select dropdown option | Beginner |
| 4 | Handle confirmation dialog | Beginner |
| 5 | Open and verify new tab | Beginner |
| 6 | Read a table value | Intermediate |
| 7 | Select auto-suggestion | Beginner |
| 8 | Build Login Page Object | Intermediate |
| 9 | Parameterized login test | Beginner |
| 10 | Handle iframe | Intermediate |
| 11 | Mock API response | Intermediate |
| 12 | Screenshot on failure | Intermediate |

---

# Part 6 – Suggested beginner interview plan

For a 45–60 minute interview, use a balanced selection rather than asking every question.

| Interview section | Suggested time | What to assess |
|---|---:|---|
| Fundamentals and architecture | 5–8 min | Browser/context/page, Pytest integration |
| Locators and waiting | 10 min | Locator quality, auto-waiting, assertions |
| Element interactions | 10 min | Forms, dropdowns, dialogs, frames or tabs |
| Fixtures and framework basics | 8–10 min | `page`, custom fixtures, `conftest.py`, POM |
| Practical coding | 10–15 min | Candidate can write and explain a test |
| Scenario/troubleshooting | 5–7 min | Reasoning, test isolation, debugging |

## Suggested evaluation weighting

- **Beginner fundamentals – 50%:** Locators, assertions, auto-waiting, common interactions, navigation.
- **Intermediate application – 35%:** Fixtures, POM, frames, data-driven tests, mocking, debugging.
- **Advanced basics – 15%:** Tracing, performance optimization, reporting customization, complex framework design.

For a candidate new to Playwright, prioritize the ability to write a clear test with reliable locators and assertions. Treat deeper fixture internals, advanced network mocking, and report customization as stretch topics.

## Interviewer tips

- Ask the candidate to explain why they chose a locator, not just write its syntax.
- Prefer role- and label-based locators when they are available and unique.
- Ask candidates to explain why fixed sleeps are usually a poor synchronization strategy.
- Check whether they know that Python Playwright projects commonly use Pytest, not the JavaScript/TypeScript Playwright Test Runner.
- During coding, look for readable tests, meaningful assertions, and appropriate cleanup.
- For beginners, give a small hint when needed and assess how they reason through the problem.

## Environment and version note

Examples use the synchronous Playwright Python API with Pytest. The `pytest-playwright` plugin provides the `page`, `context`, and browser-related fixtures used in the examples. Install current compatible versions of Python Playwright, Pytest, and the plugin, then run `playwright install`. Plugin options and some API details can evolve, so verify them against the versions installed in the interview environment.
