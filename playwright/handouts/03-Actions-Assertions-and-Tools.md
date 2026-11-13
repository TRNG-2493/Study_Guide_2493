# 03 — Actions, Assertions and Tools

> **Before you start**
>
> - **By the end you can:** click, type and press keys; read values from the page; check results with `expect`; explain auto-waiting; test elements that change over time; and use the Inspector, codegen and Trace Viewer.
> - **Practice sites:**
>   - Swag Labs — <https://www.saucedemo.com/> (`standard_user` / `secret_sauce`)
>   - The Internet — <https://the-internet.herokuapp.com/> (Topic 4 only: pages that change after a delay)
> - **Create:** a folder `lecture03/` with the same `pytest.ini` and `conftest.py` as Lecture 2, and `test_actions.py` starting with:
>
> ```python
> import re
> from playwright.sync_api import Page, expect
>
>
> def log_in(page, username="standard_user"):
>     page.goto("/")
>     page.get_by_placeholder("Username").fill(username)
>     page.get_by_placeholder("Password").fill("secret_sauce")
>     page.get_by_role("button", name="Login").click()
> ```
>
> - **Run tests with:** `pytest -s` (add `--headed` to watch)

---

## Topic 1 — Actions

### Definition

Actions are the things a user does: click, type, clear, press keys and tick boxes. You call them on a locator, and Playwright waits for the element to be ready before doing them.

### Key ideas

| Action | Example |
|---|---|
| `click()` | `page.get_by_role("button", name="Login").click()` |
| `fill(text)` | `page.get_by_placeholder("Username").fill("standard_user")` |
| `clear()` | `page.get_by_placeholder("Username").clear()` |
| `press(key)` | `password.press("Enter")` |
| `press_sequentially(text, delay=100)` | Types one key at a time |
| `check()` / `uncheck()` | Tick / untick a checkbox (Lecture 4) |

- Use **`fill()`** almost always. Use `press_sequentially()` only when the page reacts to each key (e.g. auto-suggestions).
- `type()` from older tutorials is deprecated.

### Worked example — log in and add to cart

**Step 1.** Open the login page:

```python
def test_login_and_add(page: Page):
    page.goto("/")
```

**Step 2.** Fill the username and password:

```python
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
```

**Step 3.** Submit by pressing **Enter** in the password field (instead of clicking):

```python
    page.get_by_placeholder("Password").press("Enter")
```

**Step 4.** Add the Backpack and check the cart badge:

```python
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
```

> **Predict:** Step 4 runs straight after the login. Will it fail because the products page hasn't loaded yet?

### Checkpoint

Run `pytest --headed --slowmo 500`: the form is filled, the products page opens, the Backpack button changes to **Remove** and the cart shows **1**. `1 passed`.

### Your turn

1. Write `test_wrong_password` with password `oops` and check the URL is **not** `/inventory.html`.
   *Hint: `expect(page).not_to_have_url(re.compile("inventory"))`.*
2. Fill the username, then `clear()` it, and check it is empty with `to_be_empty()`.
3. Type the username with `press_sequentially(..., delay=100)` and watch it in `--headed` mode.

---

## Topic 2 — Reading values from the page

### Definition

Reading methods return a value from the page **once, right now**, without waiting. Use them when you need the value itself — for example to print it or use it later in the test — not to check it.

### Key ideas

| Method | Returns |
|---|---|
| `text_content()` / `inner_text()` | Text inside / visible text |
| `input_value()` | Current value of an input |
| `get_attribute("placeholder")` | An attribute's value |
| `count()` | Number of matches |
| `is_visible()`, `is_checked()`, `is_enabled()` | `True` / `False` right now |

### Worked example — read and reuse values

**Step 1.** Fill the username and read it back:

```python
def test_read_values(page: Page):
    page.goto("/")
    page.get_by_placeholder("Username").fill("standard_user")
    value = page.get_by_placeholder("Username").input_value()
    print("Username field:", value)
```

**Step 2.** Read an attribute:

```python
    field_type = page.get_by_placeholder("Password").get_attribute("type")
    print("Password field type:", field_type)
```

**Step 3.** Log in and read a price you can reuse:

```python
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    price = page.get_by_test_id("inventory-item-price").first.text_content()
    print("First price:", price)
```

**Step 4.** Check plain Python values with `assert` (they're already read, so that's fine):

```python
    assert value == "standard_user"
    assert float(price.replace("$", "")) > 0
```

### Checkpoint

```
Username field: standard_user
Password field type: password
First price: $29.99
.
1 passed
```

### Your turn

1. Print the `id` attribute of the Login button.
2. After logging in, print the number of products with `count()`.
3. Print the currently selected sort option with `page.get_by_role("combobox").input_value()`.

---

## Topic 3 — Assertions with `expect`

### Definition

`expect(...)` is a **web-first assertion**: it keeps checking until the condition is true or the timeout (5 seconds by default) runs out. Plain `assert` checks once, immediately.

### Key ideas

| Category | Assertions |
|---|---|
| Page | `to_have_title`, `to_have_url` |
| Visibility | `to_be_visible`, `to_be_hidden`, `to_be_attached` |
| Text | `to_have_text`, `to_contain_text` |
| Inputs | `to_have_value`, `to_be_empty`, `to_be_editable`, `to_be_focused` |
| State | `to_be_enabled`, `to_be_disabled`, `to_be_checked` |
| Attributes / count | `to_have_attribute`, `to_have_class`, `to_have_count` |

- Add `not_` for the opposite: `not_to_be_visible()`.
- Use `re.compile(...)` for partial matches.
- Add `timeout=10_000` (ms) for slow elements, and a message as the second argument to `expect`.

### Worked example — check a shopping session

**Step 1.** Log in and check where you are:

```python
def test_assertions(page: Page):
    log_in(page)
    expect(page).to_have_url(re.compile("inventory.html"))
    expect(page.get_by_test_id("title")).to_have_text("Products")
```

**Step 2.** The cart badge is not shown while the cart is empty:

```python
    badge = page.get_by_test_id("shopping-cart-badge")
    expect(badge).to_be_hidden()
```

**Step 3.** Add two items and check the button text and badge:

```python
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    page.get_by_test_id("add-to-cart-sauce-labs-onesie").click()
    expect(page.get_by_test_id("remove-sauce-labs-backpack")).to_have_text("Remove")
    expect(badge).to_have_text("2")
```

**Step 4.** Add a custom message:

```python
    expect(badge, "Cart should show two items").to_have_text("2")
```

> **Predict:** change the last line to expect `"3"`. What does the failure message show?

### Checkpoint

`1 passed`. With `"3"`, the failure shows your custom message plus `Expected "3"` / `Received "2"`.

### Your turn

1. On the login page, click **Login** with empty fields and check the alert contains "Username is required".
2. Check the username field has the attribute `placeholder="Username"` with `to_have_attribute`.
3. Remove the Backpack again and check the badge says `"1"`.
4. Check the page title matches `re.compile("swag", re.IGNORECASE)`.

### Common errors

| Error | Fix |
|---|---|
| `assert locator.is_visible()` right after a click | Use `expect(locator).to_be_visible()` |
| `NameError: name 're' is not defined` | `import re` |

---

## Topic 4 — Auto-waiting and dynamic elements

### Definition

Before every action, Playwright runs **actionability checks** — attached, visible, stable, receives events, enabled, editable — and waits until they pass. Together with `expect`, this handles elements that appear later, change, or disappear, so you never need `sleep`.

### Key ideas

| Default timeout | Value |
|---|---|
| Actions (`click`, `fill`…) | 30 s |
| Navigation (`goto`) | 30 s |
| `expect` | 5 s |

- **Never** use `time.sleep()` or `page.wait_for_timeout()` in real tests.
- `is_visible()`, `count()`, `is_enabled()` **don't wait** — don't `assert` them right after an action.
- Rule of thumb: **after an action, assert the result you expect.**

### Worked example — loading, enabling and disappearing (The Internet)

**Step 1.** Click **Start** on a page that loads "Hello World!" after 5 seconds, and try `assert`:

```python
def test_dynamic_loading(page: Page):
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()
    assert page.get_by_text("Hello World!").is_visible()
```

> **Predict:** what will `is_visible()` return straight after the click?

**Step 2.** Run it and read the failure. Then replace the `assert`:

```python
    expect(page.get_by_text("Loading...")).to_be_visible()
    expect(page.get_by_text("Hello World!")).to_be_visible(timeout=10_000)
```

**Step 3.** A new test: a disabled input that becomes enabled:

```python
def test_dynamic_controls(page: Page):
    page.goto("https://the-internet.herokuapp.com/dynamic_controls")
    text_box = page.locator("#input-example input")
    expect(text_box).to_be_disabled()
    page.get_by_role("button", name="Enable").click()
    expect(page.get_by_text("It's enabled!")).to_be_visible()
    text_box.fill("Playwright waits for me")
```

**Step 4.** An element that disappears:

```python
    page.get_by_role("button", name="Remove").click()
    expect(page.locator("#checkbox")).to_be_hidden()
    expect(page.get_by_text("It's gone!")).to_be_visible()
```

### Checkpoint

Step 1 fails with `assert False`. After Step 2, `2 passed`, with no `sleep` anywhere.

### Your turn

1. Remove `timeout=10_000` from Step 2 and run it several times. Why does it sometimes fail?
   *Hint: the default `expect` timeout is 5 s and the page takes 5 s.*
2. In `test_dynamic_controls`, try `text_box.fill(...)` **before** clicking Enable, with `timeout=3000`. Read the error.
   *Hint: look for "element is not enabled".*
3. Log in to Swag Labs as `performance_glitch_user`. How long does it take? Write a check that waits long enough for the products page.

### Common errors

| Error | Fix |
|---|---|
| Fails after exactly 5 seconds on a slow element | Add `timeout=` to that `expect` |
| Action times out after 30 seconds on a disabled field | Do whatever enables it first |
| Flaky test with `sleep` | Remove the sleep; assert the result |

---

## Topic 5 — Tools: Inspector, codegen and Trace Viewer

### Definition

Playwright ships three tools: the **Inspector** steps through a test one action at a time, **codegen** records your clicks as test code, and the **Trace Viewer** replays a finished test run with snapshots of every step.

### Key ideas

| Tool | Command |
|---|---|
| Inspector (PowerShell) | `$env:PWDEBUG=1; pytest -s -k login` |
| Inspector (macOS/Linux) | `PWDEBUG=1 pytest -s -k login` |
| Pause at a line | `page.pause()` + `--headed` |
| Codegen | `playwright codegen --target python-pytest -o test_recorded.py URL` |
| Record traces | `pytest --tracing retain-on-failure` |
| Open a trace | `playwright show-trace test-results/<folder>/trace.zip` |

- Codegen is a **starting point**: add assertions, rename, remove extra clicks.
- Reset `PWDEBUG` afterwards: `$env:PWDEBUG=""` (PowerShell).

### Worked example — record, debug, replay

**Step 1.** Record a purchase with codegen:

```bash
playwright codegen --target python-pytest -o test_recorded.py https://www.saucedemo.com/
```

Log in as `standard_user`, add the Bike Light, open the cart, then use the toolbar to **assert text** on the item name. Close the browser.

**Step 2.** Open `test_recorded.py`. Rename the test to `test_bike_light_in_cart`. Notice which locators codegen chose.

**Step 3.** Step through it with the Inspector:

```bash
$env:PWDEBUG=1; pytest -s test_recorded.py
```

Click **Step over** for each action. Try **Pick locator** on the **Checkout** button.

**Step 4.** Reset `PWDEBUG`, break the test (change the expected text), and record a trace:

```bash
$env:PWDEBUG=""
pytest test_recorded.py --tracing retain-on-failure
```

**Step 5.** Open the trace:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

> **Predict:** with `retain-on-failure`, will a trace be saved if the test passes?

### Checkpoint

The Trace Viewer opens with a timeline of actions; clicking an action shows before/after snapshots and the failing assertion.

### Your turn

1. Add `page.pause()` after logging in, run with `--headed`, and use **Pick locator** on the sort dropdown. Then remove the pause.
2. Compare a codegen locator with one you'd write yourself. Which would you keep, and why?
3. Drag a `trace.zip` onto <https://trace.playwright.dev> and find the network tab.

### Common errors

| Error | Fix |
|---|---|
| Every test opens the Inspector | `PWDEBUG` is still set; reset it |
| Test run stops and waits | A `page.pause()` was left in |
| No trace file | Test passed with `retain-on-failure`, or you forgot `--tracing` |

---

## Stretch challenge

Write one Swag Labs test that logs in, adds three items, opens the cart, removes one, and checks the badge — with **no** `sleep` and every check done with `expect`. Then run it as `performance_glitch_user` and adjust only the timeouts that need it.

## Exit ticket

1. Why does `expect(...).to_be_visible()` pass where `assert ...is_visible()` fails?
2. Name three actionability checks Playwright does before a click.
3. Which tool would you use to find out why a test failed on a classmate's computer?

## Cheat sheet

| Code / command | Purpose |
|---|---|
| `click()`, `fill()`, `clear()`, `press("Enter")` | Actions |
| `press_sequentially(text, delay=100)` | Type key by key |
| `input_value()`, `text_content()`, `get_attribute()` | Read values (no waiting) |
| `expect(loc).to_have_text()` / `to_contain_text()` | Text checks |
| `expect(loc).to_be_visible()` / `to_be_hidden()` | Visibility |
| `expect(loc).to_be_enabled()` / `to_be_disabled()` | State |
| `expect(loc).to_have_count(n)` | Count |
| `expect(loc).not_to_...` | Opposite check |
| `expect(loc).to_be_visible(timeout=10_000)` | Longer wait |
| `re.compile("text", re.IGNORECASE)` | Partial match |
| `page.pause()` | Pause in the Inspector |
| `playwright codegen --target python-pytest URL` | Record a test |
| `pytest --tracing retain-on-failure` | Save traces of failures |
| `playwright show-trace path/trace.zip` | Open a trace |
