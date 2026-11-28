# AI-Assisted Automation Development

## Learning Objectives

By the end of this lesson you will be able to:

- **Give** an AI the inputs it needs to write useful automated tests: the reviewed test case, the code or page, and your conventions.
- **Recognise** tests that pass but prove nothing, such as `assert result` and `assert result is not None`.
- **Apply** the "break it" check to prove a test can fail, and explain how it relates to mutation testing.
- **Rewrite** weak AI tests so every assert checks the exact expected value.
- **Prefer** user-facing Playwright locators over fragile CSS and XPath, and explain why.

---

## Why This Matters

Automation code is where AI assistants are used most heavily by testers. Ask for "pytest tests for this function" and you get a tidy file in seconds, with good names, a docstring and passing tests. It is easy to feel that the job is done.

The danger is a specific kind of test: one that **passes but proves nothing**. It runs green whether the feature works or not, because its assertion is too weak or checks the wrong thing. A suite full of such tests is worse than no suite at all, because it gives **false confidence**: the dashboard says everything is fine, so nobody looks.

You met a version of this on Tuesday, in *AI-Assisted Coding and Debugging*, where a test could be weakened until it no longer protected anything. Today's version is more common, and harder to spot, because nobody weakened anything: the AI wrote the test that way from the start.

There is also a second, quieter risk: **locators**. When AI writes browser tests, it often finds elements by CSS classes or XPath paths, which break whenever the page layout changes. Playwright's own documentation recommends prioritising **user-facing attributes**, such as an element's role and accessible name, to make tests resilient ([Playwright docs](https://playwright.dev/python/docs/locators)).

This lesson shows how to give the AI the right inputs, how to prove a test can fail, and how to steer it towards locators that last.

> **Using this with the handout:** this lesson goes deeper into **Handout 06, Topic 1**. It uses the same `login_app.py` stand-in, the same AI draft tests, the same "break it" check, the same reviewed tests and the same automation prompt template.

---

## The Concept

### 1. What AI-Assisted Automation Development Means

**AI-assisted automation development** means using AI to help write automated test code: pytest functions, Playwright or Selenium scripts, page objects and fixtures. The AI writes a draft; the tester makes sure every test **can fail** when the feature is broken.

To write a useful draft, the AI needs what a colleague would need:

| Input | Example | What goes wrong without it |
|---|---|---|
| The **reviewed** test case | "TC-07: valid login shows *Welcome back!*" | The AI invents its own cases, including invented rules |
| The page or function | The HTML of the login form, or the function's code | The AI guesses element names and return values |
| Your **conventions** | "pytest; test names start with `test_`; use `get_by_role` locators" | Every file looks different; fragile locators |

Notice the first row says **reviewed**. Automation is phase 4 of the lifecycle you traced in *AI within the QA Lifecycle*. If you give the AI unreviewed test cases, it will faithfully automate whatever mistakes they contain, including the lowercase-coupon rule. The check for this phase was: **does each assert match a reviewed test case?**

### 2. Tests That Cannot Fail

A test that cannot fail when the feature is broken protects nothing. The common patterns, all of which appear in AI-written tests:

| Weak pattern | Why it is weak |
|---|---|
| `assert result` | Passes for **any** non-empty value, including an error message |
| `assert result is not None` | Passes for **any** returned value |
| `assert len(items) > 0` | Passes for any non-empty list, even with the wrong items |
| No `assert` at all | Passes unless the code crashes |
| `try: ... except: pass` around the check | Hides the failure |
| Asserting a value the test itself set | Checks the test, not the feature |

The last row is the easiest to miss. Imagine a test that sets `expected = login(VALID_EMAIL, VALID_PASSWORD)` and then asserts `login(VALID_EMAIL, VALID_PASSWORD) == expected`. It compares the function with **itself**, so it passes whatever the function returns. AI sometimes writes tests like this when it has not been told the expected value, because the code is the only "source of truth" it can see. The expected value must come from the **requirement** or the reviewed test case, never from the code under test.

All of these have the same shape: they check that **something** happened, not that the **right** thing happened. A strong assert compares the actual value with the **exact** expected value, usually with `==`.

### 3. Worked Example: The Test That Proves Nothing

**The situation:** a login page shows *"Welcome back!"* for valid credentials and *"Invalid email or password"* for anything else. So everyone can run this offline, the handout uses a small Python **stand-in** for the page's logic instead of a real browser. A stand-in is a simple replacement for a real system, used for learning or testing. The lesson is exactly the same for Playwright tests.

#### Step 1: The feature

Create `login_app.py`:

```python
USERS = {"tester@example.com": "Test#Pass1"}

def login(email: str, password: str) -> str:
    """Valid credentials show "Welcome back!".
    Anything else shows "Invalid email or password"."""
    if USERS.get(email) == password:
        return "Welcome back!"
    return "Invalid email or password"
```

**What this code does:**

- `USERS` holds one **test-environment** account. These are not real credentials, and the email uses the reserved `example.com` domain.
- `USERS.get(email)` looks up the password for that email, or returns `None` if the email is unknown. If it matches, login succeeds.
- The function returns the **message the user would see**, which is what a browser test would check on the page.

#### Step 2: The AI's draft tests

The handout asked an AI: *"Write pytest tests for the login function."* It returned this. Save it as `test_login_ai_draft.py`:

```python
from login_app import login

def test_login_works():
    result = login("tester@example.com", "Test#Pass1")
    assert result

def test_wrong_password_is_handled():
    result = login("tester@example.com", "wrong")
    assert result is not None
```

Run `python -m pytest -q test_login_ai_draft.py`. **Both tests pass.**

Now read the asserts against the table in section 2:

- `assert result` passes for **any** non-empty text. `"Invalid email or password"` is non-empty, so this test would pass even if valid logins were rejected.
- `assert result is not None` passes for **any** returned value, including `"Welcome back!"` for a wrong password.

Neither test checks **which** message appears. The names promise a lot ("login works", "wrong password is handled"); the asserts check almost nothing.

#### Step 3: Break the feature on purpose

Edit `login_app.py` and change the line `if USERS.get(email) == password:` to:

```python
    if True:  # BUG: everyone gets in
```

Now **everyone** can log in with any password: a serious security bug. Run the AI's tests again:

```text
..                                                                       [100%]
2 passed in 0.00s
```

**The AI's tests still pass.** They cannot detect the very bug they were written to catch.

#### Step 4: Write reviewed tests that can fail

Create `test_login_reviewed.py`:

```python
import pytest
from login_app import login

VALID_EMAIL = "tester@example.com"
VALID_PASSWORD = "Test#Pass1"          # test-environment account, not a real one

def test_valid_login_shows_welcome():
    assert login(VALID_EMAIL, VALID_PASSWORD) == "Welcome back!"

@pytest.mark.parametrize("email, password", [
    (VALID_EMAIL, "wrong"),             # wrong password
    ("nobody@example.com", VALID_PASSWORD),  # unknown user
    (VALID_EMAIL, ""),                  # empty password
])
def test_invalid_login_shows_error(email, password):
    assert login(email, password) == "Invalid email or password"
```

**What this code does:**

- Each assert compares the result with the **exact message** the user should see, using `==`.
- The test data lives in named constants at the top, so it is easy to see and change.
- `parametrize` (from Tuesday's *AI-Assisted Test Design*) runs one test function for three **invalid** situations: wrong password, unknown user and empty password.

With the bug **still in place**, run `python -m pytest -q test_login_reviewed.py`. The key lines:

```text
E       AssertionError: assert 'Welcome back!' == 'Invalid email or password'
FAILED test_login_reviewed.py::test_invalid_login_shows_error[tester@example.com-wrong]
FAILED test_login_reviewed.py::test_invalid_login_shows_error[nobody@example.com-Test#Pass1]
FAILED test_login_reviewed.py::test_invalid_login_shows_error[tester@example.com-]
3 failed, 1 passed in 0.01s
```

Three tests **fail**: they caught the bug. Read the output like a tester. Each `FAILED` line shows which parameters were used inside the square brackets, and the `AssertionError` line shows the actual value (`'Welcome back!'`) against the expected value. The one test that passes is the valid-login test, which is correct: the bug lets everyone in, so the valid user still gets in too.

#### Step 5: Fix the feature and confirm

Change `if True:` back to `if USERS.get(email) == password:` and run **both** files:

```text
......                                                                   [100%]
6 passed in 0.02s
```

Everything passes again. Here is the whole story in one table:

| Situation | AI draft tests | Reviewed tests |
|---|---|---|
| Feature correct | `2 passed` | `4 passed` |
| Feature **broken** | `2 passed` ❌ (missed the bug) | `3 failed, 1 passed` ✅ (caught it) |

On correct code, the two files look equally good: all green. Only the broken-code row shows the difference. **A passing test means nothing until you have seen it fail for the right reason.**

### 4. The "Break It" Check and Mutation Testing

The check in Step 3 has a name in testing: it is a simple, manual form of **mutation testing**. A **mutant** is a copy of the code with one small, deliberate change, such as a flipped condition or a different message. If your tests fail, they have **killed** the mutant. If they all still pass, the mutant **survived**, which means your tests cannot tell the broken code from the correct code.

You have done this several times already this week: changing `>=` to `>` in `cart.py` on Monday, and in `shipping.py` on Tuesday. Useful mutations to try on any feature:

| Mutation | Example in `login_app.py` | What it tests |
|---|---|---|
| Make a condition always true | `if True:` | Do the negative tests check the result? |
| Make a condition always false | `if False:` | Does the positive test check the result? |
| Change a returned value | `return "Welcome!"` | Do asserts compare exact values? |
| Shift a boundary | `>=` to `>` | Is there a test exactly on the boundary? |

Two rules keep the check safe. **Change one thing at a time**, so you know which change a test caught. And **always restore the code** afterwards (Step 5): a forgotten mutation is a real bug you introduced.

Teams also use tools that create and run many mutants automatically. For now, the manual version is enough: one deliberate break per feature, every time an AI writes tests for it.

### 5. Locators: Find Elements Like a User Would

So far we have tested a Python function. In a real browser test, the test must first **find** the email field, the password field and the button. The code that finds an element is called a **locator**. AI assistants often suggest locators based on the page's internal structure:

| ❌ Fragile (AI often suggests) | ✅ User-facing (prefer) |
|---|---|
| `page.locator("#btn-23 > span")` | `page.get_by_role("button", name="Log in")` |
| `page.locator("//div[3]/input[1]")` | `page.get_by_label("Email")` |
| `page.locator(".msg-err")` | `page.get_by_text("Invalid email or password")` |

The fragile versions depend on things a user never sees: an auto-generated ID (`#btn-23`), the position of an element (`div[3]`), a styling class (`.msg-err`). A developer can change any of these without changing what the page does, and the test breaks. Playwright's guidance warns that CSS tied to the implementation could break when the page changes, and recommends prioritising user-visible locators instead ([Playwright docs: other locators](https://playwright.dev/python/docs/other-locators)).

The user-facing versions describe what a **person** sees: a button called "Log in", a field labelled "Email", a message with certain text. They have a second benefit: a test using `get_by_text("Invalid email or password")` checks that the user can **see** the exact message, which is the requirement.

Here is how the login test might look in Playwright, using user-facing locators. It is **illustrative** and not run in this lesson:

```python
from playwright.sync_api import Page, expect

def test_wrong_password_shows_error(page: Page):
    page.goto("https://shop.example.com/login")          # illustrative test site
    page.get_by_label("Email").fill("tester@example.com")
    page.get_by_label("Password").fill("wrong")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_text("Invalid email or password")).to_be_visible()
```

Compare its last line with `test_invalid_login_shows_error` in Step 4. It is the same exact-message check, written for a browser.

### 6. A Prompt Template for Automation Code

When you ask an AI to write automated tests, give it the **reviewed** test cases and your conventions, and tell it what a good assert looks like. Save this template from the handout in `prompts.txt` as `Automation - v1`:

```text
You are a test automation engineer. Write pytest tests for the function below.

### Reviewed test cases (use exactly these; do not add others)
TC-07: valid login (tester@example.com / <valid_password>) shows "Welcome back!"
TC-08: wrong password shows "Invalid email or password"
TC-09: unknown email shows "Invalid email or password"

### Code under test
<paste login_app.py here>

### Conventions
- pytest only; test names start with test_ and describe the behaviour
- every assert compares the EXACT expected message with ==
- never use "assert result" or "is not None" as the only check
- put test data in constants at the top of the file
- use parametrize when several cases share the same check

Reply with one Python file only.
```

Each part prevents a specific problem:

| Part | Prevents |
|---|---|
| "use exactly these; do not add others" | Invented test cases |
| `<valid_password>` placeholder | Real secrets in the prompt |
| "compares the EXACT expected message" | Tests that prove nothing |
| "never use assert result" | The exact weakness from Step 2 |
| "one Python file only" | Extra explanation text you would need to strip out |

The placeholder deserves a note. Even a test-environment password should not be pasted into a public AI tool out of habit; the AI does not need the real value to write the test. You will see why this habit matters in *Responsible Use of AI in QE*.

The template is not only for login. Replace the test cases and the code, keep the conventions, and it works for `apply_coupon` or `shipping_fee` too. The conventions section is the part you will reuse most, so improve it whenever a review finds a new weakness.

For browser tests, add one line to the conventions: *"Use Playwright user-facing locators (get_by_role, get_by_label, get_by_text); do not use CSS or XPath."*

### 7. Reviewing AI Test Code

Even with a good prompt, review every AI-written test file. A short checklist:

1. **Does each test trace to a reviewed test case?** Look for extra tests the AI added.
2. **Does every assert compare an exact expected value?** Search the file for `assert result`, `is not None` and `len(`.
3. **Do the test names match what the asserts check?** `test_login_works` promised more than `assert result` delivered.
4. **Are the locators user-facing?** Search for `#`, `//` and `.locator(`.
5. **Can each test fail?** Apply at least one "break it" mutation and watch the tests go red.
6. **Is there anything sensitive in the file?** Real passwords, keys or personal data do not belong in test code.

Questions 2 and 4 are quick text searches, so you can do them even on a long file. Question 5 is the one you must never skip, because it is the only one that proves the tests work.

### 8. Worked Review: an AI Playwright Draft

Here is the kind of browser test an AI often writes when asked only *"Write a Playwright test for a wrong password on the login page"*, **illustrative** and not run:

```python
import time

def test_wrong_password(page):
    page.goto("https://shop.example.com/login")
    page.locator("#email").fill("tester@example.com")
    page.locator("//form/div[2]/input").fill("wrong")
    page.locator(".btn.btn-primary").click()
    time.sleep(3)
    assert "Invalid" in page.content()
```

It would probably pass today. Review it with the checklist from section 7:

| Line | Problem | Better |
|---|---|---|
| `#email`, `//form/div[2]/input`, `.btn.btn-primary` | Three fragile locators: an ID, a position and styling classes | `get_by_label("Email")`, `get_by_label("Password")`, `get_by_role("button", name="Log in")` |
| `time.sleep(3)` | A fixed wait: too slow when the page is fast, too short when it is slow, which causes flaky tests | Let Playwright wait for the element, as `expect(...)` does |
| `assert "Invalid" in page.content()` | A weak assert: passes if the word "Invalid" appears **anywhere** in the page's HTML, even in hidden text or a script | `expect(page.get_by_text("Invalid email or password")).to_be_visible()` |
| The test name | Fine, but it does not name the reviewed test case | Add a comment such as `# TC-08` |

The rewritten version is the illustrative test in section 5. Notice that two of the problems are about **trust** rather than style. The fixed sleep makes the test flaky, which you met in Monday's flaky-test example. The weak assert makes it unable to fail for the right reason. Ask yourself: if the page showed "Invalid coupon" by mistake, would this test notice? It would not, because "Invalid" is all it checks.

### 9. What the AI Cannot Know About Your App

When an AI writes a browser test without seeing the page, it **guesses**. Its guesses are usually plausible, which makes them hard to spot:

- **Labels and names.** It might write `get_by_label("Email address")` when the page says "Email". The locator finds nothing, and the test fails for a reason that has nothing to do with the feature.
- **Exact messages.** It might expect "Incorrect password" when the requirement says "Invalid email or password". This is the paraphrased-message problem from *AI-Generated Test Cases*, in code.
- **Test environment details.** It does not know your test site's address, which test accounts exist, or how long your environment takes to respond.

The fix is the second row of the inputs table in section 1: **give it the page**. Paste the relevant HTML, or at least the labels, button names and messages, into the prompt. A test written from the real page needs far fewer corrections than one written from imagination.

### 10. Page Objects and Fixtures

As a suite grows, teams organise browser tests with **page objects**: a class for each page that holds its locators and actions, such as a `LoginPage` with a `log_in(email, password)` method. Tests then call `login_page.log_in(...)` instead of repeating locators everywhere. They also use **fixtures**: shared setup that pytest runs before a test, such as opening the browser or creating a test user.

AI is good at writing this kind of structure, because it is repetitive and follows well-known patterns. When you review an AI-generated page object or fixture, three questions cover most problems:

1. **Are the locators inside it user-facing?** One fragile locator in a page object breaks every test that uses it.
2. **Does it hide asserts?** A page object method that quietly asserts something makes failures confusing. Keep the checks in the tests, where the reviewer can see them.
3. **Does every fixture clean up after itself?** A fixture that creates a test user should remove it, or the next run starts from a different state, as you saw with state-dependent data in *AI-Generated Test Data*.

You will build page objects and fixtures properly in your Project 2 framework. For today, the habit is the same as for any AI code: let it write the structure, then check it.

### 11. When the AI Gets It Wrong: One Good Re-Ask

If the AI's file fails your review, do not rewrite everything yourself straight away. A specific re-ask often fixes it:

```text
Two problems with your tests:
1. test_login_works uses "assert result", which passes for any non-empty message.
   Compare the result with "Welcome back!" using ==.
2. There is no test for an unknown email (TC-09). Add it, using parametrize with TC-08.
Reply with the whole corrected file only.
```

This re-ask follows Tuesday's advice from *Common Prompt Failure Modes*: name each problem, say exactly what you want instead, and lock the format. Then review the new file with the same checklist, including the break-it check. A re-ask fixes the problems you named; it may introduce new ones.

If one specific re-ask does not fix the problem, write that part yourself. Handling repeated failures automatically, with retries and error handling, is a topic for Week 9.

### 12. Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `IndentationError` after editing `if True:` | The new line lost its 4-space indent | Keep the same indentation as the line you replaced |
| All tests still pass after "breaking" the code | You did not save the file, or you edited a different copy | Save, and check you are in the right folder |
| Tests still fail after the fix | You forgot to undo the bug | Always **restore** after a break-it check |
| `ModuleNotFoundError: No module named 'login_app'` | The test file and `login_app.py` are in different folders | Keep them in the same folder, and run pytest from there |
| `function uses no argument 'mail'` | A name in the `parametrize` string does not match the function's parameters | Make `"email, password"` match `def ...(email, password)` exactly |

---

## Practice Exercises

1. **A different bug (code, 5 min).** Change `return "Welcome back!"` to `return "Welcome!"` in `login_app.py`. Run both test files. Which file catches the bug, and which test? Restore the code afterwards.

2. **Break-it check on your AI's tests (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** paste `login_app.py` into your AI assistant and ask: *"Write pytest tests for this function. Every assert must check the exact message returned. Include invalid cases."*
   - **Review:** apply the checklist from section 7 before running anything.
   - **Run:** run its tests, then apply the `if True:` mutation and run them again. Do they catch the bug?
   - **Record:** in `prompts.txt`, note which weak patterns (if any) it used, and whether the instruction "exact message" was followed.

3. **User-facing locators (paper, 10 min).** The real login page has this HTML: `<label for="email">Email</label><input id="email">` and `<button class="btn btn-primary">Log in</button>`. Write the two **user-facing** Playwright locators for the email field and the button. No need to run them. Then write the fragile CSS locator an AI might suggest for the button, and say what page change would break it.

4. **Check an old test (code, 15 min).** Find a test you wrote in an earlier week. Apply the break-it check: change the code under test so the feature is wrong. Does your test fail? If not, strengthen its assert and try again.

---

## Knowledge Check

1. What three inputs does an AI need to write useful automated tests?

<details><summary>Answer</summary>

The reviewed test case, the code or page under test, and your team's conventions.

</details>

2. Why is `assert result` a weak assert for `login()`?

<details><summary>Answer</summary>

It passes for any non-empty text, including "Invalid email or password", so it cannot tell a successful login from a failed one.

</details>

3. With the `if True:` bug in place, the AI's tests give `2 passed` and the reviewed tests give `3 failed, 1 passed`. Why does one reviewed test still pass?

<details><summary>Answer</summary>

It is the valid-login test. The bug lets everyone in, so the valid user still sees "Welcome back!", which is the correct result for that test.

</details>

4. What is a mutant, and what does it mean if it "survives"?

<details><summary>Answer</summary>

A copy of the code with one small deliberate change. It survives if all the tests still pass, which means the tests cannot tell the broken code from the correct code.

</details>

5. Why prefer `page.get_by_role("button", name="Log in")` over `page.locator("#btn-23 > span")`?

<details><summary>Answer</summary>

It finds the button the way a user sees it, so it keeps working when IDs or layout change, and it checks the user-visible name. The CSS locator depends on internal details that can change at any time.

</details>

6. Why does the automation prompt use `<valid_password>` instead of the real test password?

<details><summary>Answer</summary>

The AI does not need the real value to write the test, and pasting secrets into AI tools is a bad habit, even for test accounts.

</details>

7. After an AI re-ask fixes the problems you named, what must you still do?

<details><summary>Answer</summary>

Review the new file again with the checklist, including a break-it check, because a re-ask can introduce new problems.

</details>

8. An AI test uses `time.sleep(3)` and then `assert "Invalid" in page.content()`. Name two problems.

<details><summary>Answer</summary>

The fixed sleep makes the test slow or flaky, and the assert is weak: it passes if "Invalid" appears anywhere in the page's HTML. Use `expect(page.get_by_text("Invalid email or password")).to_be_visible()`.

</details>

---

## Glossary

- **AI-assisted automation development:** using AI to help write automated test code such as pytest tests, Playwright scripts, page objects and fixtures.
- **Stand-in:** a simple replacement for a real system, used for learning or testing.
- **Weak assert:** an assert that passes for many wrong results, such as `assert result`.
- **False confidence:** believing a feature works because tests pass, when the tests could not detect a failure.
- **"Break it" check:** deliberately breaking the code to confirm a test fails.
- **Mutation testing:** testing the tests by running them against deliberately changed copies of the code.
- **Mutant:** a copy of the code with one small deliberate change.
- **Killed / survived mutant:** a mutant the tests detect / one they do not.
- **Exact assert:** an assert that compares the actual value with the exact expected value, usually with `==`.
- **Source of truth:** where an expected value comes from: the requirement or reviewed test case, never the code under test.
- **Locator:** code that finds an element on a web page.
- **User-facing locator:** a locator based on what a user sees, such as a role, label or text.
- **Fragile locator:** a locator that depends on internal details such as IDs, classes or element positions.
- **Page object:** a class that holds one page's locators and actions, so tests do not repeat them.
- **Fixture (pytest):** shared setup that runs before a test, such as opening a browser or creating a test user.
- **Fixed wait:** pausing for a set time, such as `time.sleep(3)`, instead of waiting for something to happen.
- **Conventions:** a team's agreed rules for how tests are written.

---

## Summary

- Give the AI **the reviewed test case, the code or page, and your conventions**. Unreviewed cases get automated mistakes and all.
- Watch for tests that **pass but prove nothing**: `assert result`, `is not None`, no assert at all.
- **Break it on purpose.** In the worked example, the AI's tests passed on broken code (`2 passed`); the reviewed tests caught it (`3 failed, 1 passed`).
- Write **exact asserts** with `==`, and prove each test can fail before you trust it.
- Prefer **user-facing locators** (`get_by_role`, `get_by_label`, `get_by_text`) over fragile CSS and XPath.

---

## Additional Resources

- Playwright for Python, *Locators*: https://playwright.dev/python/docs/locators
- Playwright, *Best Practices*: https://playwright.dev/docs/best-practices
- pytest documentation, *How to write and report assertions in tests*: https://docs.pytest.org/en/stable/how-to/assert.html
