# Built-in Locators

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a locator is, why Playwright recommends user-facing locators, and how they relate to the CSS/XPath selectors from Thursday.
- Use all the main built-in locators: `get_by_role`, `get_by_text`, `get_by_label`, `get_by_placeholder`, `get_by_alt_text`, `get_by_title` and `get_by_test_id`.
- Use the most important `get_by_role` options: `name`, `exact`, `checked`, `disabled`, `expanded`, `level`, `pressed`, `selected`.
- Understand roles and accessible names, and how HTML maps to them.
- Choose the best locator for a given element using a priority list.
- Configure a custom test-id attribute.
- Recognize when `page.locator()` with CSS or XPath is still the right tool.

---

## Why This Matters

Thursday you learned CSS selectors and XPath. They are powerful and you will need them, but they have a weakness: they describe **how the page is built** (class names, nesting, positions), and developers change those details constantly. A redesign that renames `.btn-primary` to `.button--main` breaks every test that used it, even though the user sees the same "Login" button.

Playwright's **built-in locators** describe **what the user sees and perceives**: "the button named Login", "the field labelled Email". These are far more stable, are easier to read, and double as a light accessibility check, because if a locator by role cannot find your button, a screen reader probably cannot either.

For this week's epic and Project 1: QE Foundations, you need UI tests that survive normal development churn, so that the maintenance cost of your automation stays low. Choosing the right locator is the most important maintenance decision you make in every test.

---

## The Concept

### 1. What is a locator?

A **locator** is a recipe for finding element(s) on the page, evaluated freshly each time it is used. You met this on Friday's first lesson: locators are lazy and re-queried at action time, which is why Playwright avoids stale-element problems.

All locators return a `Locator` object. Methods are available on `page` (search the whole page) and also on other locators (search inside them, see the next lesson on chaining).

### 2. The recommended priority

Playwright's documentation recommends preferring locators in roughly this order:

1. `get_by_role()` : how assistive technology and users perceive the element (button, link, heading, checkbox...).
2. `get_by_label()` : form fields associated with a visible label.
3. `get_by_placeholder()` : inputs with placeholder text and no label.
4. `get_by_text()` : non-interactive elements located by their visible text.
5. `get_by_alt_text()` : images by their `alt` attribute.
6. `get_by_title()` : elements with a `title` attribute.
7. `get_by_test_id()` : a dedicated testing attribute (such as `data-testid`) when nothing user-facing is stable.
8. CSS/XPath via `page.locator()` : last resort (but sometimes the only practical option).

Think of the list as "most user-like and stable" to "most implementation-coupled".

### 3. `get_by_role()`

**Roles** come from the WAI-ARIA specification (published by the W3C). Every HTML element has an *implicit* role:

| HTML | Implicit role |
|------|---------------|
| `<button>`, `<input type="submit">` | `button` |
| `<a href="...">` | `link` |
| `<h1>` to `<h6>` | `heading` (with a `level`) |
| `<input type="checkbox">` | `checkbox` |
| `<input type="radio">` | `radio` |
| `<input type="text">`, `<input type="email">` (no list) | `textbox` |
| `<select>` | `combobox` |
| `<ul>`, `<ol>` | `list` |
| `<li>` | `listitem` |
| `<table>` | `table` |
| `<tr>` | `row` |
| `<td>` | `cell` |
| `<img alt="...">` | `img` |
| `<nav>` | `navigation` |
| `<dialog>` or `role="dialog"` | `dialog` |

Developers can also set roles explicitly: `<div role="button">`.

The **accessible name** is the text an assistive technology announces for the element: the text inside a button, the `aria-label`, the `<label>` text for an input, the `alt` for an image, and so on.

```python
page.get_by_role("button", name="Login")
page.get_by_role("link", name="Docs")
page.get_by_role("heading", name="Installation")
page.get_by_role("checkbox", name="Remember me")
page.get_by_role("textbox", name="Email")
```

Important options:

| Option | Meaning | Example |
|--------|---------|---------|
| `name` | Accessible name; a substring match, case-insensitive by default. Also accepts a compiled regex. | `name="log in"` |
| `exact` | With `name`, match the whole string, case-sensitive. | `name="Log in", exact=True` |
| `checked` | Filter checkboxes/radios by checked state. | `checked=True` |
| `disabled` | Filter by disabled state. | `disabled=False` |
| `expanded` | For accordions/menus with `aria-expanded`. | `expanded=True` |
| `level` | Heading level (1 to 6). | `level=2` |
| `pressed` | Toggle buttons (`aria-pressed`). | `pressed=True` |
| `selected` | Selected tabs/options. | `selected=True` |
| `include_hidden` | Include elements hidden from the accessibility tree (default False). | `include_hidden=True` |

Examples:

```python
page.get_by_role("heading", name="Sign up", level=1)
page.get_by_role("button", name="Submit", disabled=True)
page.get_by_role("checkbox", name="I agree", checked=False)
page.get_by_role("link", name=re.compile("^Docs$"))
```

Why does the default name match as a *substring, case-insensitively*? Because it makes tests less fragile to small wording changes. If you need precision (say "Sign in" versus "Sign in with Google"), add `exact=True`.

### 4. `get_by_text()`

Finds elements containing the given text. Best for non-interactive content such as paragraphs and labels; for interactive elements prefer role.

```python
page.get_by_text("Welcome, John")                 # substring, case-insensitive
page.get_by_text("Welcome, John", exact=True)     # full string, case-sensitive
page.get_by_text(re.compile("welcome", re.IGNORECASE))
```

Notes: whitespace is normalized; it matches the smallest element containing the text. Do not use it to find `<input>` fields (their "text" is a value, not content).

### 5. `get_by_label()`

Finds a form control by the text of its associated `<label>` (or `aria-label` / `aria-labelledby`).

HTML:

```html
<label for="email">Email address</label>
<input id="email" type="email">
```

Python:

```python
page.get_by_label("Email address").fill("jane@example.com")
```

This is excellent for forms: it mirrors how a user identifies a field. It also forces good HTML: if `get_by_label` cannot find a field, the label is not correctly linked, an accessibility bug worth reporting.

### 6. `get_by_placeholder()`

For inputs that show hint text:

```html
<input placeholder="Username">
```

```python
page.get_by_placeholder("Username").fill("standard_user")
```

Placeholders disappear when typing and are weaker for accessibility than labels, so use this when no label exists. (SauceDemo's login fields have placeholders only; that is why the earlier lessons used `get_by_placeholder`.)

### 7. `get_by_alt_text()` and `get_by_title()`

```html
<img src="logo.png" alt="Company logo">
<span title="Issues count">25 issues</span>
```

```python
page.get_by_alt_text("Company logo").click()
expect(page.get_by_title("Issues count")).to_have_text("25 issues")
```

### 8. `get_by_test_id()`

Developers add a dedicated attribute for tests:

```html
<button data-testid="directions">Itinerary</button>
```

```python
page.get_by_test_id("directions").click()
```

By default Playwright looks for `data-testid`. Some applications use another, such as SauceDemo's `data-test`. Configure it once (in `conftest.py`):

```python
import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")
```

After this, `page.get_by_test_id("login-button")` matches `data-test="login-button"`. Test ids are the most stable choice when the visible text changes often (translations, A/B tests) or when there is no meaningful role/label. They require cooperation from developers, which a good QE team requests as part of "testability".

### 9. `page.locator()`: CSS and XPath

Everything you learned Thursday still applies:

```python
page.locator("#login-button")
page.locator("input[name='user-name']")
page.locator("ul.inventory_list > li:nth-child(2)")
page.locator("xpath=//div[@class='cart_item']")
```

Use it when: no role/label/text exists (a plain `<div>` wrapper), you need structural logic, or the app offers no better hooks. Playwright's CSS engine also adds powerful extras like `:has-text()`, `:visible` and `text=` selectors; but built-in locators plus filtering (next lesson) cover most of these cases more readably.

### 10. How to choose: a worked decision process

Given this HTML:

```html
<form>
  <h1>Create account</h1>
  <label for="fn">First name</label>
  <input id="fn" name="first">
  <label><input type="checkbox" name="terms"> I accept the terms</label>
  <button type="submit" class="btn btn-primary btn-lg">Sign up</button>
  <a href="/login">Already registered? Log in</a>
</form>
```

| Element | Good locator | Why |
|---------|-------------|-----|
| Heading | `get_by_role("heading", name="Create account")` | Role + name. |
| First name field | `get_by_label("First name")` | Linked label. |
| Terms checkbox | `get_by_role("checkbox", name="I accept the terms")` | Role + name from wrapping label. |
| Submit | `get_by_role("button", name="Sign up")` | Not `.btn-primary`. |
| Login link | `get_by_role("link", name="Log in")` | Substring match works. |

Notice that none uses the CSS classes. If the designers change `btn-lg` to `btn-xl`, nothing breaks.

### 11. Verifying locators while writing them

- In the **Playwright Inspector** or codegen (covered in the next lessons today), the "Pick locator" tool suggests a locator for any element you click.
- In a script, `locator.count()` tells you how many elements match; `expect(locator).to_have_count(1)` verifies uniqueness.
- In browser DevTools you can test CSS and XPath (Thursday), but not Playwright's `get_by_*` methods.

### 12. Locators and accessibility

Because role/name locators use the browser's accessibility tree, a failing `get_by_role("button", name="Save")` sometimes reveals a real defect: a clickable `<div>` that has no role, an icon-only button with no `aria-label`, or an input without a label. Raise these defects; they help real users. We will not dive deeper into accessibility testing here.

---

## Code Examples

### Example 1: A form using only built-in locators

Use this self-contained page so you can practice without any external site:

```python
# test_builtin_locators.py
import re
from playwright.sync_api import Page, expect

FORM_HTML = """
<h1>Create account</h1>
<form onsubmit="event.preventDefault(); document.getElementById('ok').hidden = false;">
  <label for="fn">First name</label>
  <input id="fn" name="first">

  <label for="em">Email</label>
  <input id="em" type="email" placeholder="you@example.com">

  <label><input type="checkbox" name="terms"> I accept the terms</label>

  <button type="submit">Sign up</button>
  <a href="/login">Already registered? Log in</a>
</form>
<p id="ok" hidden>Account created!</p>
<img src="x.png" alt="Company logo">
"""


def test_signup_form_with_builtin_locators(page: Page):
    page.set_content(FORM_HTML)

    expect(page.get_by_role("heading", name="Create account", level=1)).to_be_visible()

    page.get_by_label("First name").fill("Jane")
    page.get_by_label("Email").fill("jane@example.com")
    page.get_by_role("checkbox", name="I accept the terms").check()
    page.get_by_role("button", name="Sign up").click()

    expect(page.get_by_text("Account created!")).to_be_visible()
    expect(page.get_by_alt_text("Company logo")).to_be_attached()
    expect(page.get_by_role("link", name="Log in")).to_have_attribute("href", "/login")
```

**Explanation line by line:**

- `FORM_HTML` is a triple-quoted string with a small page. `page.set_content()` loads it, so the test needs no server.
- `get_by_role("heading", name="Create account", level=1)` matches the `<h1>`.
- `get_by_label("First name")` finds the `<input id="fn">` via `<label for="fn">`.
- `get_by_label("Email")` also matches the input. Note: the placeholder is `you@example.com`; label matching uses the label text.
- `get_by_role("checkbox", ...).check()` ticks the checkbox; `check()` also verifies it became checked.
- Clicking Sign up reveals the hidden paragraph; `get_by_text("Account created!")` waits until it is visible.
- `to_be_attached()` asserts the image exists in the DOM (it has no real source, so it might not "render"; attached is the right check here).
- `to_have_attribute("href", "/login")` verifies link target.

### Example 2: SauceDemo with built-in locators

```python
from playwright.sync_api import Page, expect


def test_login_and_add_to_cart(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Products")).to_be_visible()

    page.get_by_role("button", name="Add to cart").first.click()
    expect(page.get_by_role("button", name="Remove").first).to_be_visible()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
```

**Explanation:** The login form uses placeholders, so `get_by_placeholder` is appropriate. The page has six "Add to cart" buttons, so `get_by_role("button", name="Add to cart")` matches six elements; calling `.click()` directly would raise a strict mode error, hence `.first`. (The next lesson shows a better, more precise way: filtering to the specific product.) The cart badge has no role, label or text association, so we fall back to a CSS class.

### Example 3: Exact versus substring

```python
page.set_content("""
<button>Sign in</button>
<button>Sign in with Google</button>
""")

page.get_by_role("button", name="Sign in")                  # matches BOTH (substring)
page.get_by_role("button", name="Sign in", exact=True)      # matches only the first

expect(page.get_by_role("button", name="Sign in")).to_have_count(2)
expect(page.get_by_role("button", name="Sign in", exact=True)).to_have_count(1)
```

**Explanation:** the first locator would cause a strict-mode error if clicked. `exact=True` makes it unambiguous. Always check how many elements your locator matches.

### Example 4: Custom test id

```python
# conftest.py
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_test_id(playwright):
    playwright.selectors.set_test_id_attribute("data-test")

# test_file.py
def test_with_test_ids(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_test_id("username").fill("standard_user")
    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    expect(page).to_have_url(re.compile("inventory"))
```

**Explanation:** SauceDemo uses `data-test="username"` etc. After setting the attribute name, `get_by_test_id("username")` is shorter and more stable than a CSS selector.

### Example 5: Role options

```python
page.set_content("""
<button aria-pressed="true">Bold</button>
<button aria-pressed="false">Italic</button>
<button disabled>Save</button>
<h2>Section</h2><h3>Sub-section</h3>
""")

expect(page.get_by_role("button", name="Bold", pressed=True)).to_have_count(1)
expect(page.get_by_role("button", name="Italic", pressed=True)).to_have_count(0)
expect(page.get_by_role("button", disabled=True)).to_have_text("Save")
expect(page.get_by_role("heading", level=3)).to_have_text("Sub-section")
```

---

## Real-World Scenarios

1. **Redesign without test breakage.** The company redesigns the site with a new CSS framework. Tests using `get_by_role("button", name="Checkout")` keep working; tests using `.btn-checkout-v2` break. The team learns to prefer user-facing locators.
2. **Localization.** An international site changes the button text per language. Text-based locators would fail in French; `get_by_test_id("checkout")` works for all locales.
3. **Accessibility defect found by accident.** A test using `get_by_role("button", name="Close")` fails because the close icon is a `<div>` with no role or label. The tester files a bug, and the fix improves the experience for screen reader users.

---

## Common Mistakes

1. **Defaulting to CSS/XPath for everything** because it feels familiar. Reach for built-in locators first.
2. **Forgetting that `name` is a substring match**, then clicking the wrong button ("Sign in with Google"). Use `exact=True` when needed.
3. **Using `get_by_text` for buttons and links.** Use `get_by_role` so you also verify the element's role.
4. **Using `get_by_role("textbox")` for a password field.** Password inputs do not expose the `textbox` role; use `get_by_label` or `get_by_placeholder`.
5. **Expecting `get_by_label` to match placeholders.** Label and placeholder are different attributes; use the matching method.
6. **Ignoring strict mode**, then sprinkling `.first` everywhere. Make locators specific instead (next lesson).
7. **Mistyping the role** (`"btn"` instead of `"button"`). Roles must be valid ARIA role names; the editor's type hints help.
8. **Setting the test-id attribute inside a test** after locators were created. Set it once in a session-level fixture.
9. **Matching on long dynamic text** such as order numbers. Use regex or `exact=False` partial matches.

---

## Practice Exercises

**Exercise 1.** For each HTML snippet, write the best built-in locator:

a) `<button class="x1">Add to basket</button>`
b) `<input type="search" placeholder="Search products">`
c) `<label for="pw">Password</label><input id="pw" type="password">`
d) `<h2>Order summary</h2>`
e) `<img src="a.png" alt="Product photo">`

*Solutions:*

```python
page.get_by_role("button", name="Add to basket")
page.get_by_placeholder("Search products")
page.get_by_label("Password")
page.get_by_role("heading", name="Order summary", level=2)
page.get_by_alt_text("Product photo")
```

**Exercise 2.** Rewrite the SauceDemo login test from Friday's first lesson (which used `#user-name`, `#password`, `#login-button`) using only built-in locators.

**Exercise 3.** Using Example 3's HTML, write tests proving that `name="Sign in"` matches two buttons while `exact=True` matches one.

**Exercise 4.** Use `playwright.selectors.set_test_id_attribute("data-test")` and automate: login, add the backpack to the cart (its attribute is `data-test="add-to-cart-sauce-labs-backpack"`), and assert the cart badge shows 1.

**Exercise 5.** Visit https://playwright.dev/python/ . Write three different locators (role, text, CSS) for the main page heading. Which would you keep? Explain in two sentences.

**Exercise 6 (Project 1).** For three of your Project 1 UI scenarios, build a locator table: *Element | Locator chosen | Priority level (1-8) | Reason*. Aim for no entry below priority 5 unless you justify it.

---

## Summary

- Built-in locators find elements the way users do: by role, label, placeholder, text, alt text, title or test id.
- `get_by_role` is the first choice; its `name` is a case-insensitive substring unless `exact=True`.
- Use `get_by_label` and `get_by_placeholder` for forms, `get_by_text` for static content, `get_by_test_id` when user-facing hooks are unstable.
- Reserve CSS/XPath (`page.locator()`) for cases where nothing more meaningful exists.
- Always make sure your locator matches exactly the element(s) you intend; strict mode is your friend.
- Better locators mean lower maintenance and a more accessible application.

---

## Additional Resources

- Playwright for Python: Locators: https://playwright.dev/python/docs/locators
- WAI-ARIA Roles (W3C): https://www.w3.org/TR/wai-aria-1.2/#role_definitions
- MDN: ARIA roles: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles
