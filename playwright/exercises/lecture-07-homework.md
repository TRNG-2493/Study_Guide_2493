# Lecture 7: Homework

**Time:** 60 minutes
**Goal:** write your own fixtures (autouse, `yield` teardown, session scope) and reuse a saved login.

## Setup

1. Create a folder `homework_07/`.
2. Copy into it from the Lecture 7 demo:
   - the `site/` folder (`login.html` and `account.html`)
   - `conftest.py`
3. Create `homework_07/test_lecture07_homework.py`.

```
homework_07/
├── conftest.py                     ← copied; you'll ADD fixtures to the bottom
├── site/
│   ├── login.html
│   └── account.html
└── test_lecture07_homework.py      ← your tests
```

**Logins:** `student` / `secret123` and `admin` / `secret123`.

Check the setup works before you start:

```bash
pytest homework_07 -v
```

(No tests yet, but there should be no errors.)

---

## Part 1: Hooks the Playwright way (required)

In `test_lecture07_homework.py`, create a class `TestLoginScreen` with:

- An **autouse** fixture that opens `/login.html` before each test
- `test_01_heading`: the main heading is "Log in"
- `test_01_empty_login`: clicking **Log in** with empty fields shows "Invalid username or password"

Neither test should call `page.goto` itself.

---

## Part 2: Custom fixtures (required)

Add these fixtures to the **bottom of `conftest.py`**:

**`wrong_password_page`**
- Uses the existing `login_page` fixture
- Tries to log in as `student` with a wrong password
- Returns the page

**`admin_ui_page`** (setup **and** teardown)
- Logs in as `admin` through the UI (you can use the `log_in` helper in `conftest.py`)
- Gives the page to the test
- **After the test:** clicks **Log out**, but only if the page is still on `account.html`
- Prints a message before and after, so you can see it with `-s`

Then write the tests:

- `test_02_wrong_password`: the error message is shown and the title is still "Practice Store - Log in"
- `test_03_admin_through_ui`: the role says "Role: Administrator"

```bash
pytest homework_07 -v -s -k "02 or 03"
```

---

## Part 3: Saved login state (required)

Add two more fixtures to `conftest.py`, following the `student_state` / `logged_in_page` pattern from the lecture:

**`admin_state`** (session scope)
- Logs in as `admin` **once** and saves the storage state to a file

**`admin_page`**
- Creates a **new context** from `admin_state` for each test
- Opens `/account.html` and returns the page

Then write the tests:

| Test | Check |
|---|---|
| `test_04_admin_role` | Heading "Welcome, admin!" and role "Role: Administrator" |
| `test_04_admin_cart_starts_empty` | "Cart: 0 items" |
| `test_04_admin_adds_three_items` | After 3 clicks: "Cart: 3 items" |
| `test_05_student_and_admin` | Uses **both** `logged_in_page` and `admin_page`; checks each role |

Check the speed:

```bash
pytest homework_07 -v --durations=0
```

The `admin_page` tests should take about 0.1 s to set up, except the first.

---

## Part 4: Questions (required)

Answer as comments at the bottom of your test file:

1. What would happen if `admin_state` were **function**-scoped instead of session-scoped?
2. What would happen if `admin_page` were **session**-scoped?
3. Why should `admin_ui_page` check the URL before clicking **Log out**?

---

## Bonus (optional)

Override `browser_context_args` in `homework_07/conftest.py` so every context in the folder uses:

- a viewport of 1280 × 720
- the locale `"en-GB"`

Then write `test_bonus_context_settings` that checks:

```python
assert page.viewport_size == {"width": 1280, "height": 720}
assert page.evaluate("navigator.language") == "en-GB"
```

> Remember to keep the existing settings (like `base_url`), or every `goto("/...")` will break.

---

## Submission checklist

- [ ] `conftest.py` with 4 new fixtures (5 with the bonus)
- [ ] `test_lecture07_homework.py`: 8 passing tests (9 with the bonus)
- [ ] No `from conftest import ...` in the test file
- [ ] 3 answers to Part 4
