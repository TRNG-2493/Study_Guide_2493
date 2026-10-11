# Weekly Knowledge Check: Week 5 Advanced Web Automation, Wednesday: Playwright Framework Design

**Topics covered:** fixtures and custom fixtures, hooks, Page Object Model, converting scripts to POM, data-driven testing with JSON, test retries, Playwright reporting.

**How to use this quiz:** answer each question before opening the solution. Every solution explains *why* the answer is right and, for multiple choice, why each distractor is wrong. Code-prediction answers were checked by actually running the snippets with pytest, pytest-playwright, pytest-rerunfailures and pytest-html.

**Structure:** Part 1 Multiple Choice (Q1-24), Part 2 True/False (Q25-36), Part 3 Code Prediction (Q37-54), Part 4 Fill-in-the-Blank (Q55-66).

---

## Part 1: Multiple Choice

### 1. pytest-playwright launches the browser once per run but gives every test a new context and page. Which scope combination makes this possible, and what does it buy you?
- [ ] A) `browser` is function-scoped and `page` is session-scoped; you get isolation but slow runs
- [ ] B) `context` and `page` are session-scoped; you get speed because everything is shared
- [ ] C) `browser` is session-scoped and `context`/`page` are function-scoped; you get speed (one browser process) and isolation (fresh cookies and storage per test)
- [ ] D) `browser` is function-scoped and `context` is session-scoped; you get a new browser per test but shared cookies

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `browser` is session-scoped and `context`/`page` are function-scoped; you get speed (one browser process) and isolation (fresh cookies and storage per test)

**Explanation:** Launching a browser is expensive, so it happens once per session; creating a context is nearly instant, so each test gets a brand-new one, like a new incognito profile.
- **Why others are wrong:**
  - A) The scopes are inverted. A session-scoped `page` could not be created from a function-scoped `browser`, and it would share state between tests.
  - B) A shared context and page would make cookies and local storage leak from one test into the next.
  - D) Launching a new browser for every test is the slow approach fixtures were designed to avoid, and a session-scoped `context` would leak state between tests.
</details>

---

### 2. Which statement about a fixture that uses `yield` is correct?
- [ ] A) Code after `yield` runs after the test finishes, even if the test failed
- [ ] B) Code after `yield` runs only when the test passes
- [ ] C) `return` and `yield` are interchangeable because both support teardown
- [ ] D) Code after `yield` runs before the test body, in reverse order of setup

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Code after `yield` runs after the test finishes, even if the test failed

**Explanation:** Everything before `yield` is setup, the yielded value goes to the test, and everything after `yield` is teardown that runs regardless of the test outcome.
- **Why others are wrong:**
  - B) Teardown is guaranteed on failure too, which is exactly why cleanup (deleting a test user, closing a context) belongs there.
  - C) A fixture that uses `return` can only do setup; code written after a `return` never runs.
  - D) Code after `yield` runs after the test, not before it. Only the *order between fixtures* is reversed during teardown.
</details>

---

### 3. Which fixture definition raises `ScopeMismatch`?
- [ ] A) A function-scoped fixture that requests `browser`
- [ ] B) A session-scoped fixture that requests `playwright`
- [ ] C) A module-scoped fixture that requests `browser`
- [ ] D) A session-scoped fixture that requests `page`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A session-scoped fixture that requests `page`

**Explanation:** A fixture can only depend on fixtures with the same or a wider scope. `page` is function-scoped (destroyed after each test), so a session-scoped fixture would be left holding a dead object; pytest refuses with `ScopeMismatch`.
- **Why others are wrong:**
  - A) A narrower fixture may depend on a wider one; `browser` is session-scoped, so this is fine.
  - B) `playwright` is session-scoped, the same scope as the requesting fixture, which is allowed.
  - C) `browser` is session-scoped, wider than module scope, so this is allowed.
</details>

---

### 4. A `conftest.py` contains `def browser_context_args(browser_context_args): return {**browser_context_args, "locale": "en-US"}`. Why does the parameter share the fixture's own name?
- [ ] A) It causes infinite recursion, so pytest raises an error
- [ ] B) The parameter refers to the original (plug-in) fixture, so the override extends the defaults instead of replacing them
- [ ] C) It converts the fixture to function scope automatically
- [ ] D) It is ignored unless the fixture is also imported into every test file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The parameter refers to the original (plug-in) fixture, so the override extends the defaults instead of replacing them

**Explanation:** When a `conftest.py` fixture has the same name as a plug-in fixture, the parameter with that name resolves to the parent version. Unpacking it with `**` keeps options such as `--device` and `base_url` while adding yours.
- **Why others are wrong:**
  - A) pytest resolves the parameter to the parent fixture, not to itself, so there is no recursion.
  - C) Scope comes from the `scope=` argument, not from the parameter name.
  - D) Fixtures in `conftest.py` are discovered automatically; importing them is an anti-pattern.
</details>

---

### 5. Which of these is a *plug-in hook* (pytest calling your function at a lifecycle moment) rather than a setup/teardown mechanism you write for your tests?
- [ ] A) `@pytest.fixture(autouse=True) def clean_state(): ...`
- [ ] B) `def pytest_runtest_makereport(item, call): ...` in `conftest.py`
- [ ] C) `def setup_method(self, method): ...` inside a test class
- [ ] D) A fixture with `yield` that clears local storage

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `def pytest_runtest_makereport(item, call): ...` in `conftest.py`

**Explanation:** Plug-in hooks are functions whose *name* is the contract (`pytest_*`); pytest calls them when it builds a report, starts a session, and so on. The helpful question is "am I preparing something for a test, or reacting to something pytest is doing?"
- **Why others are wrong:**
  - A) An autouse fixture is setup/teardown that you write for your tests.
  - C) `setup_method` is an xunit-style setup/teardown hook for your tests.
  - D) A `yield` fixture is the recommended way to write setup and teardown, not a plug-in hook.
</details>

---

### 6. In the `page_with_evidence` fixture, why does the fixture take `page` as a parameter instead of fishing it out of the test later?
- [ ] A) pytest-playwright refuses to create a page unless a fixture asks for it by name
- [ ] B) `pytest_runtest_makereport` only runs for fixtures that request `page`
- [ ] C) `page.screenshot()` can only be called from inside the test body
- [ ] D) Requesting `page` makes it set up first and torn down last, so the page is still open when the code after `yield` takes the screenshot

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Requesting `page` makes it set up first and torn down last, so the page is still open when the code after `yield` takes the screenshot

**Explanation:** Teardown runs in reverse order of setup. An explicit dependency on `page` guarantees `page` outlives the evidence fixture; a fixture without that dependency could be torn down after `page` is already closed.
- **Why others are wrong:**
  - A) Any test or fixture may request `page`; nothing forbids other access patterns, the problem is *ordering*.
  - B) The makereport hook runs for every test regardless of which fixtures it uses.
  - C) A screenshot can be taken from fixture teardown as long as the page is still open, which is what the explicit dependency guarantees.
</details>

---

### 7. You want a custom `--env` command-line option. Which hook registers it, and where must it live?
- [ ] A) `pytest_addoption(parser)` in the root-level `conftest.py`
- [ ] B) `pytest_configure(config)` in any test file
- [ ] C) `pytest_sessionstart(session)` in a nested `conftest.py`
- [ ] D) `pytest_generate_tests(metafunc)` in the root `conftest.py`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `pytest_addoption(parser)` in the root-level `conftest.py`

**Explanation:** Options are registered before collection starts, so `pytest_addoption` belongs in a root-level `conftest.py` (or a plug-in). Tests and fixtures read the value with `request.config.getoption("--env")` or `pytestconfig.getoption("env")`.
- **Why others are wrong:**
  - B) `pytest_configure` is for startup configuration such as registering markers, not for adding options.
  - C) `pytest_sessionstart` runs once at session start and cannot add options; a nested `conftest.py` is also not reliably honoured for options.
  - D) `pytest_generate_tests` is for dynamic parametrisation.
</details>

---

### 8. For a Playwright suite, what is the idiomatic pytest equivalent of a "before each / after each" hook?
- [ ] A) Functions named `beforeEach` and `afterEach` in `conftest.py`
- [ ] B) `setup_method(self, page)` requesting `page` in its signature
- [ ] C) A function-scoped fixture with `yield` (add `autouse=True` to apply it to every test)
- [ ] D) The `pytest_runtest_setup` hook alone, without teardown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A function-scoped fixture with `yield` (add `autouse=True` to apply it to every test)

**Explanation:** Function scope runs once per test, code before `yield` is the "before", code after is the "after", and both halves live side by side so cleanup cannot be forgotten.
- **Why others are wrong:**
  - A) Those names belong to Mocha/Jasmine/Cypress style runners; pytest does not recognise them.
  - B) xunit-style methods cannot request built-in fixtures such as `page` in their signature.
  - D) `pytest_runtest_setup` has no matching teardown half and is meant for reacting to a run, for example skipping tests dynamically.
</details>

---

### 9. According to the lesson's recommended convention, what belongs in a page object class?
- [ ] A) Raw `page.locator(...)` calls repeated in each test
- [ ] B) Assertions for every business rule, executed after each action
- [ ] C) Code that launches the browser with `sync_playwright()`
- [ ] D) The page's locators defined once, plus methods named after user intent such as `login_as(...)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The page's locators defined once, plus methods named after user intent such as `login_as(...)`

**Explanation:** A page object owns the locators for its page and exposes what a user can do there; tests call those methods and keep the assertions that express expected behaviour.
- **Why others are wrong:**
  - A) Locators leaking into tests is a listed anti-pattern; it means the page object is incomplete.
  - B) Assertion-heavy page objects hide test logic and hurt reuse; at most use clearly named `expect_*` readiness checks.
  - C) Page objects receive a `Page` (dependency injection) and never launch the browser; fixtures own the browser lifecycle.
</details>

---

### 10. Why is it safe to create every locator in a page object's `__init__`, even for elements that are not on the page yet?
- [ ] A) Playwright copies the DOM when the locator is created and keeps it cached
- [ ] B) Constructors only run after the page has fully loaded
- [ ] C) A `Locator` is lazy: it stores how to find the element and searches only when you act on it or assert on it, with auto-waiting
- [ ] D) Locators created early are validated and removed if the element does not exist

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A `Locator` is lazy: it stores how to find the element and searches only when you act on it or assert on it, with auto-waiting

**Explanation:** Because resolution happens at action or assertion time, locators never go stale, unlike old Selenium-style element references.
- **Why others are wrong:**
  - A) No DOM snapshot is taken at creation; that would make locators stale.
  - B) A page object can be constructed at any time, before or after navigation.
  - D) Nothing is validated at creation; a missing element only matters when you act on it.
</details>

---

### 11. The `Header.cart_count()` method checks `self.cart_badge.count() == 0` before calling `inner_text()`. Why?
- [ ] A) `count()` waits for the badge to appear, which makes `inner_text()` faster
- [ ] B) The badge disappears when the cart is empty, and `inner_text()` on a missing element would wait and time out
- [ ] C) `inner_text()` cannot return numbers, so `count()` converts them
- [ ] D) `count()` is required before any locator can be clicked

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The badge disappears when the cart is empty, and `inner_text()` on a missing element would wait and time out

**Explanation:** `count()` reports how many elements match right now without waiting, so it lets the method return `0` for an empty cart instead of timing out.
- **Why others are wrong:**
  - A) `count()` does not wait; it returns the current number of matches immediately.
  - C) Converting the text to a number is done by `int(...)`, not by `count()`.
  - D) Click and other actions auto-wait; no `count()` call is required first.
</details>

---

### 12. `InventoryPage.open_cart()` returns a `CartPage`, and you now add `CartPage.continue_shopping()` that must return an `InventoryPage`. A module-level import in both files would create a circular import. What is the standard fix?
- [ ] A) Import `InventoryPage` inside the body of `continue_shopping()`, so it is imported only when the method runs
- [ ] B) Move both classes into one giant file called `app_page.py`
- [ ] C) Wrap the import in `try/except ImportError: pass`
- [ ] D) Import `CartPage` at module level in `InventoryPage` and again in every test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Import `InventoryPage` inside the body of `continue_shopping()`, so it is imported only when the method runs

**Explanation:** Forward navigation (login to inventory to cart) can import at module level; a page that navigates *back* imports lazily inside the method to avoid a loop.
- **Why others are wrong:**
  - B) A single giant file is the "God page" anti-pattern and does not fit one-class-per-page design.
  - C) Swallowing `ImportError` hides the real problem and leaves the name undefined.
  - D) Repeating imports in tests does not break the cycle between the two page modules.
</details>

---

### 13. You inherit a flat Playwright script and must refactor it into POM. What should you do first?
- [ ] A) Run the tests to confirm they are green, and commit that baseline
- [ ] B) Delete duplicated assertions to make the script shorter
- [ ] C) Convert every page in one go, then run the tests once at the end
- [ ] D) Create a large `BasePage` with every helper you might need

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Run the tests to confirm they are green, and commit that baseline

**Explanation:** Refactoring must preserve behaviour, so you start from green; otherwise you cannot tell whether your change broke a test. Record the list of assertions as your "do not lose these" checklist too.
- **Why others are wrong:**
  - B) Deleting assertions weakens the tests; refactoring must never do that.
  - C) A big-bang conversion makes failures impossible to localise; convert page by page and re-run after each step.
  - D) Introduce `BasePage` once at least two pages share code; over-engineering on day one is an anti-pattern.
</details>

---

### 14. In the converted purchase test, the original `expect(page).to_have_url(...)` checks for the cart and overview pages no longer appear in the test body. Where did those checks go?
- [ ] A) They were removed, because POM makes URL checks unnecessary
- [ ] B) They moved into `expect_loaded()` readiness checks that navigation methods call; assertions are moved, not deleted
- [ ] C) They moved into the JSON data file
- [ ] D) They were replaced by `time.sleep` calls

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) They moved into `expect_loaded()` readiness checks that navigation methods call; assertions are moved, not deleted

**Explanation:** Navigation methods such as `open_cart()` construct the next page object and call `expect_loaded()`, which keeps both the assertion and the synchronisation point. The Step 0 checklist is how you verify nothing was lost.
- **Why others are wrong:**
  - A) POM does not make verification unnecessary, and silently dropping assertions is a listed pitfall.
  - C) JSON holds test data, not assertions or checks.
  - D) Sleeps are an anti-pattern; the readiness check uses auto-retrying `expect`.
</details>

---

### 15. When converting a dialog script into a page method, when must the dialog handler be registered?
- [ ] A) After the click that triggers the dialog, so the dialog exists
- [ ] B) In fixture teardown
- [ ] C) Before the action that triggers the dialog, for example `page.once("dialog", ...)` followed by the click
- [ ] D) Never; Playwright accepts dialogs automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Before the action that triggers the dialog, for example `page.once("dialog", ...)` followed by the click

**Explanation:** Playwright auto-dismisses dialogs that have no handler at the moment they appear, so the handler must already be registered when the click happens.
- **Why others are wrong:**
  - A) By then the dialog has already been dismissed automatically.
  - B) Teardown runs after the test; far too late.
  - D) Without a handler, Playwright *dismisses* the dialog, it does not accept it.
</details>

---

### 16. Which of the following is valid JSON?
- [ ] A) `{'user': "standard_user"}`
- [ ] B) `{"locked": True}`
- [ ] C) `{"users": ["a", "b",]}`
- [ ] D) `{"locked": false, "reason": null}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `{"locked": false, "reason": null}`

**Explanation:** JSON booleans and null are lower case (`true`, `false`, `null`) and keys use double quotes.
- **Why others are wrong:**
  - A) Single quotes are not allowed anywhere in JSON.
  - B) `True` is Python syntax; JSON requires lower-case `true`.
  - C) Trailing commas are invalid and are the most common hand-editing error.
</details>

---

### 17. Why does the data loader build the path with `Path(__file__).resolve().parent.parent / "data"` instead of `open("data/login_data.json")`?
- [ ] A) The `json` module only accepts absolute paths
- [ ] B) Relative paths are slower to open
- [ ] C) The file is found regardless of the directory pytest was launched from
- [ ] D) `parametrize` refuses relative paths

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The file is found regardless of the directory pytest was launched from

**Explanation:** A relative path like `"data/login_data.json"` depends on the current working directory, which differs between an IDE, the project root and a CI runner. Building the path from `__file__` removes that dependency.
- **Why others are wrong:**
  - A) `json.load` takes an open file object; it does not care how the path was built.
  - B) Speed is not the reason.
  - D) `parametrize` takes values, not paths; the issue is `FileNotFoundError` when the working directory changes.
</details>

---

### 18. What does `indirect=True` do in `@pytest.mark.parametrize("inventory_for", users, indirect=True)`?
- [ ] A) It defers the test until all other tests have finished
- [ ] B) It hides the parameter values from test ids
- [ ] C) It parametrises through the command line instead of the decorator
- [ ] D) It sends each value to the fixture named `inventory_for` as `request.param`, and the test receives that fixture's return value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It sends each value to the fixture named `inventory_for` as `request.param`, and the test receives that fixture's return value

**Explanation:** Use `indirect` when setup must happen between the data and the test, such as logging a user in and returning the inventory page.
- **Why others are wrong:**
  - A) `indirect` has nothing to do with execution order.
  - B) Ids are controlled by `ids=`; `indirect` does not hide them.
  - C) The values still come from the decorator; only their destination changes.
</details>

---

### 19. A suite runs with `pytest --reruns 2`. What is the maximum number of times a consistently failing test will be executed?
- [ ] A) 3 (the first run plus two reruns)
- [ ] B) 2
- [ ] C) 4
- [ ] D) Unlimited, until it passes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 3 (the first run plus two reruns)

**Explanation:** `--reruns N` allows N reruns *after* the initial attempt, so there are at most N + 1 attempts.
- **Why others are wrong:**
  - B) That would count only the reruns and forget the original attempt.
  - C) That would be `--reruns 3`.
  - D) Reruns are bounded by N; a test that keeps failing ends as failed.
</details>

---

### 20. A test fails intermittently because it clicks a button before the page is ready. What is the best fix according to the lesson?
- [ ] A) Raise the global setting to `--reruns 5`
- [ ] B) Use Playwright's auto-waiting actions and web-first `expect(...)` assertions, waiting for the specific condition
- [ ] C) Add `time.sleep(5)` before every click
- [ ] D) Re-run the whole CI pipeline whenever it fails

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Use Playwright's auto-waiting actions and web-first `expect(...)` assertions, waiting for the specific condition

**Explanation:** Retry at the lowest layer that fixes the problem. A synchronisation bug is fixed by proper waiting, not by re-running the test.
- **Why others are wrong:**
  - A) Global high retry counts hide problems and multiply suite duration.
  - C) A fixed sleep is either too short (still flaky) or too long (slow).
  - D) Pipeline-level re-runs are blunt and discard information about what failed.
</details>

---

### 21. What does `--self-contained-html` do when generating a pytest-html report?
- [ ] A) It removes passing tests from the report
- [ ] B) It embeds CSS and assets, including images as base64, into the single HTML file so it can be emailed or uploaded
- [ ] C) It also writes a JUnit XML file
- [ ] D) It opens the report in a browser automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It embeds CSS and assets, including images as base64, into the single HTML file so it can be emailed or uploaded

**Explanation:** Without it the report depends on side files and breaks when moved; with it the report is one portable file.
- **Why others are wrong:**
  - A) The flag does not filter results.
  - C) JUnit XML needs `--junitxml=...`.
  - D) pytest-html never auto-opens a browser.
</details>

---

### 22. Why should the GitHub Actions step that uploads reports and traces use `if: always()`?
- [ ] A) Without it, the upload step is skipped when the test step fails, and you would lose exactly the evidence you need
- [ ] B) It makes the upload run faster
- [ ] C) pytest will not create the report unless the upload step is marked `always()`
- [ ] D) It is mandatory syntax for `actions/upload-artifact`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Without it, the upload step is skipped when the test step fails, and you would lose exactly the evidence you need

**Explanation:** By default a step is skipped after an earlier step fails. Failing runs are the ones whose reports and traces matter most.
- **Why others are wrong:**
  - B) The condition affects *whether* the step runs, not its speed.
  - C) The report is produced by pytest during the test step, independent of the upload step.
  - D) The action works without it; you add it to make it run on failure.
</details>

---

### 23. In a Python Playwright project, how do you open a recorded trace file?
- [ ] A) `npx playwright show-report`
- [ ] B) `pytest --show-trace trace.zip`
- [ ] C) `pytest-html --open trace.zip`
- [ ] D) `playwright show-trace test-results/<test-folder>/trace.zip`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `playwright show-trace test-results/<test-folder>/trace.zip`

**Explanation:** The Trace Viewer is opened with `playwright show-trace`, or by dragging `trace.zip` onto https://trace.playwright.dev (which runs entirely in your browser).
- **Why others are wrong:**
  - A) `npx playwright show-report` belongs to the Node.js/TypeScript Playwright Test runner and does not apply to a Python/pytest project.
  - B) pytest has no `--show-trace` option.
  - C) pytest-html generates reports; it is not a trace viewer.
</details>

---

### 24. A test passes on its second attempt under `pytest-rerunfailures`. Which fixtures are set up again for that second attempt?
- [ ] A) None; all fixtures are kept from the first attempt
- [ ] B) Only session-scoped fixtures
- [ ] C) Function-scoped fixtures such as `page` and `context`; session-scoped fixtures are generally not recreated
- [ ] D) All fixtures, including the session-scoped `browser`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Function-scoped fixtures such as `page` and `context`; session-scoped fixtures are generally not recreated

**Explanation:** Each attempt gets a brand-new browser context and page, which is why context-per-test isolation and reruns fit well together. Session-scoped state, however, can carry stale data into a retry.
- **Why others are wrong:**
  - A) Function-scoped fixtures are torn down and set up again, giving a fresh page.
  - B) It is the opposite: higher scopes are generally *not* recreated.
  - D) The session-scoped `browser` stays alive for the whole run.
</details>

---

## Part 2: True/False (Common Misconceptions)

### 25. True or False: To use a fixture defined in `conftest.py` inside a test file, you should write `from conftest import page_fixture` at the top of the test.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** pytest loads `conftest.py` automatically and injects its fixtures by name. Importing from `conftest` is an anti-pattern that causes confusing duplicate-registration behaviour.
</details>

---

### 26. True or False: Any code written after a `return` statement in a fixture never runs, so a fixture that needs teardown must use `yield`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `return` ends the function, so a fixture that returns can only do setup. Use `yield` to hand the value to the test and run cleanup afterwards, even when the test fails.
</details>

---

### 27. True or False: `pytest_addoption` is honoured just as reliably in a nested `tests/ui/conftest.py` as in the root `conftest.py`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Command-line options are registered before test collection starts, so `pytest_addoption` must live in the root-level `conftest.py` (or a plug-in). In a nested `conftest.py` it is not honoured reliably.
</details>

---

### 28. True or False: Even though pytest-playwright offers `--screenshot only-on-failure`, a custom `pytest_runtest_makereport` failure hook is still worth knowing, because it lets you control file names and add extras such as an HTML dump or console log.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The built-in flags cover the common cases. A custom hook is the pattern behind every custom failure behaviour (naming files, saving page HTML and console logs, sending a notification), so you write one only for what the built-ins cannot do.
</details>

---

### 29. True or False: A well-designed `login()` page-object method should also assert that the URL changed and that the title is correct, so tests never need their own assertions.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Assertion-heavy page objects hide test logic inside infrastructure, reduce reuse (the same method cannot serve a test that expects something else) and make failures hard to interpret. Page objects expose actions and state; tests decide what is correct. Clearly named `expect_*` readiness checks are the accepted exception.
</details>

---

### 30. True or False: The Page Object Model starts to pay off as soon as a second test touches the same page, while for a three-test throw-away script it is overkill.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** POM costs extra files and a layer of abstraction. The maintenance saved outweighs that cost once more than one test shares a page; the lesson also warns against building a deep inheritance tree before you have two tests.
</details>

---

### 31. True or False: While converting a flat script to POM, an assertion is allowed to *move* (for example into a page's `expect_loaded()` method) but must never be silently deleted.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Refactoring must not weaken the test. Writing an assertions checklist before you start and ticking each item afterwards proves that every original check still exists somewhere.
</details>

---

### 32. True or False: JSON permits `//` comments and trailing commas, so you can annotate a test-data file freely.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** JSON supports neither comments nor trailing commas. If you need explanations, add a field such as `"description"`. Validate a file with `python -m json.tool file.json`.
</details>

---

### 33. True or False: `json.loads(text)` parses a JSON *string*, while `json.load(f)` reads from an open *file object*.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The trailing `s` stands for "string": `loads`/`dumps` work with strings, `load`/`dump` work with file objects.
</details>

---

### 34. True or False: If a test passes on its second attempt under `--reruns`, nothing more needs to be done, because the build is green.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A test that needs a retry to pass is a defect in the test suite (or an intermittent product bug) and gets a ticket. Retries are a safety net, not a fix; the rerun rate should be reviewed in reports.
</details>

---

### 35. True or False: A `@pytest.mark.flaky(reruns=1)` marker overrides a command-line `--reruns 3` for that one test.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** A marker on a test (or class or module) takes precedence over the command-line value, so that test is attempted at most twice. This was confirmed by running it: the summary is `1 failed, 1 rerun`.
</details>

---

### 36. True or False: For a Python Playwright project, you view results with `npx playwright show-report` and the `--reporter=html` option.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The Playwright HTML reporter belongs to the Node.js/TypeScript Playwright Test runner. In Python the runner is pytest, so reports come from pytest, plug-ins such as pytest-html, JUnit XML, and Playwright's artifacts (screenshots, video, traces).
</details>

---

## Part 3: Code Prediction

### 37. What does this code print, in order? (Run with `pytest -s`.)
```python
import pytest

@pytest.fixture
def a():
    print("A setup")
    yield
    print("A teardown")

@pytest.fixture
def b(a):
    print("B setup")
    yield
    print("B teardown")

def test_demo(b):
    print("TEST")
```
- [ ] A) A setup, B setup, A teardown, B teardown, TEST
- [ ] B) A setup, B setup, TEST, B teardown, A teardown
- [ ] C) B setup, A setup, TEST, A teardown, B teardown
- [ ] D) A setup, B setup, TEST, A teardown, B teardown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A setup, B setup, TEST, B teardown, A teardown

**Explanation:** `b` depends on `a`, so `a` is set up first. Teardown runs in reverse order of setup, so `b` is torn down before `a` (like unstacking plates).
- **Why others are wrong:**
  - A) Teardown happens after the test body, not before it.
  - C) `b` requests `a`, so `a` must be set up first.
  - D) Teardown order is the reverse of setup order, not the same.
</details>

---

### 38. What do the two tests print? (Run with `pytest -s`.)
```python
import pytest

counter = {"n": 0}

@pytest.fixture(scope="module")
def mod_id():
    counter["n"] += 1
    return counter["n"]

@pytest.fixture
def func_id():
    counter["n"] += 1
    return counter["n"]

def test_one(func_id, mod_id):
    print("one", func_id, mod_id)

def test_two(func_id, mod_id):
    print("two", func_id, mod_id)
```
- [ ] A) `one 1 2` and `two 3 4`
- [ ] B) `one 1 2` and `two 3 2`
- [ ] C) `one 2 1` and `two 4 3`
- [ ] D) `one 2 1` and `two 3 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `one 2 1` and `two 3 1`

**Explanation:** pytest instantiates higher-scoped fixtures first, regardless of the order of parameters, so `mod_id` is created first (1) and `func_id` second (2). The module-scoped value is cached for `test_two`, while `func_id` is created again (3).
- **Why others are wrong:**
  - A) Assumes both fixtures are recreated for each test and set up in signature order.
  - B) Assumes `func_id` is created first because it is listed first, but module scope is instantiated before function scope.
  - C) Assumes the module-scoped fixture is recreated for every test; it is created once per file.
</details>

---

### 39. What does this print? (Run with `pytest -s`.)
```python
import pytest

@pytest.fixture
def requested():
    print("requested")

@pytest.fixture(autouse=True)
def auto():
    print("auto")

def test_x(requested):
    print("test")
```
- [ ] A) auto, requested, test
- [ ] B) requested, auto, test
- [ ] C) test, auto, requested
- [ ] D) requested, test (autouse fixtures only run when named)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) auto, requested, test

**Explanation:** `autouse=True` applies the fixture to every test in scope without being named, and autouse fixtures are set up first, followed by the explicitly requested ones.
- **Why others are wrong:**
  - B) Requested fixtures come after autouse ones, not before.
  - C) Fixtures are set up before the test body, never after it.
  - D) That describes a normal fixture; `autouse=True` is precisely what removes the need to name it.
</details>

---

### 40. What does this print? (Run with `pytest -s`.)
```python
import pytest

@pytest.fixture
def make_user():
    created = []
    def _make(name):
        created.append(name)
        print("create", name)
        return name
    yield _make
    for n in created:
        print("delete", n)

def test_users(make_user):
    make_user("a")
    make_user("b")
```
- [ ] A) create a, create b, delete b, delete a
- [ ] B) create a, delete a, create b, delete b
- [ ] C) create a, create b, delete a, delete b
- [ ] D) create a, create b (nothing is deleted)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) create a, create b, delete a, delete b

**Explanation:** The factory returns a function (`yield _make`); both users are created during the test. After the test, the loop after `yield` runs over the list in insertion order, so cleanup happens for `a` then `b`.
- **Why others are wrong:**
  - A) Reverse teardown order applies *between fixtures*; inside this loop the list is iterated forwards.
  - B) Deletion does not happen until the test has finished, so both creates come first.
  - D) Code after `yield` always runs after the test, so the deletes are printed.
</details>

---

### 41. This test fails on its first two attempts and passes on the third. It is run with `pytest --reruns 2 -s`. What is printed on the passing attempt?
```python
import pytest
from pathlib import Path

log = []
COUNTER = Path("attempts.txt")

@pytest.fixture(scope="session")
def sess():
    log.append("S")

@pytest.fixture
def func():
    log.append("F")

def test_flaky(sess, func):
    n = int(COUNTER.read_text()) if COUNTER.exists() else 0
    COUNTER.write_text(str(n + 1))
    if n < 2:
        raise AssertionError("transient")
    COUNTER.unlink()
    print(log)
```
- [ ] A) `['S', 'F', 'F', 'F']`
- [ ] B) `['S', 'S', 'S', 'F', 'F', 'F']`
- [ ] C) `['S', 'F']`
- [ ] D) `['S', 'F', 'S', 'F', 'S', 'F']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `['S', 'F', 'F', 'F']`

**Explanation:** Function-scoped fixtures are torn down and set up again for every attempt (three attempts, three `F`), while the session-scoped fixture is not recreated for a rerun (one `S`). This is why mutable session state can carry stale data into a retry.
- **Why others are wrong:**
  - B) Session fixtures are not rebuilt per attempt, so there is only one `S`.
  - C) That would mean the function fixture also ran only once, but each rerun re-creates it.
  - D) That would mean both scopes are rebuilt every attempt.
</details>

---

### 42. In what order are the lines printed? (Run with `pytest -s`.)
```python
def setup_module(module):
    print("setup_module")

def teardown_module(module):
    print("teardown_module")

class TestCart:
    @classmethod
    def setup_class(cls):
        print("setup_class")

    @classmethod
    def teardown_class(cls):
        print("teardown_class")

    def setup_method(self, method):
        print("setup_method")

    def teardown_method(self, method):
        print("teardown_method")

    def test_one(self):
        print("test_one")

    def test_two(self):
        print("test_two")
```
- [ ] A) setup_module, setup_class, setup_method, test_one, test_two, teardown_method, teardown_class, teardown_module
- [ ] B) setup_class, setup_module, setup_method, test_one, teardown_method, setup_method, test_two, teardown_method, teardown_module, teardown_class
- [ ] C) setup_module, setup_class, setup_method, test_one, teardown_method, setup_method, test_two, teardown_method, teardown_class, teardown_module
- [ ] D) setup_module, setup_class, test_one, test_two, setup_method, teardown_method, teardown_class, teardown_module

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) setup_module, setup_class, setup_method, test_one, teardown_method, setup_method, test_two, teardown_method, teardown_class, teardown_module

**Explanation:** Module hooks run once per file, class hooks once per class, and method hooks around *each* test method. Setup goes from widest to narrowest and teardown unwinds in reverse.
- **Why others are wrong:**
  - A) `setup_method` and `teardown_method` run around every test, not once for the whole class.
  - B) The module-level hook wraps the class-level one, so `setup_module` comes first and `teardown_module` last.
  - D) The method hooks wrap each test; they do not run after all the tests.
</details>

---

### 43. A hook wrapper in `conftest.py` prints one line per report. What is printed for the following failing test?
```python
# conftest.py
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    print(f"{report.when}:{report.outcome}")

# test_hook.py
def test_fails():
    assert False
```
- [ ] A) `call:failed` only
- [ ] B) `setup:passed`, `call:failed`, `teardown:passed`
- [ ] C) `setup:passed`, `call:failed`, `teardown:failed`
- [ ] D) `call:failed`, `teardown:passed` (no report for setup)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `setup:passed`, `call:failed`, `teardown:passed`

**Explanation:** pytest runs each test in three phases (`setup`, `call`, `teardown`) and builds a report after each one. Only the test body failed; the fixtures were set up and torn down successfully.
- **Why others are wrong:**
  - A) The hook fires after every phase, not just the call phase, which is why code in the hook must check `report.when`.
  - C) The failing assertion belongs to the call phase; teardown succeeded.
  - D) Every phase produces a report, including setup.
</details>

---

### 44. Given this hook and these tests (`slow` is registered as a marker), in what order does `pytest --collect-only -q` list the tests?
```python
# conftest.py
def pytest_collection_modifyitems(config, items):
    items.sort(key=lambda it: it.get_closest_marker("slow") is not None)

# test_order.py
import pytest

@pytest.mark.slow
def test_a(): ...

def test_b(): ...

@pytest.mark.slow
def test_c(): ...

def test_d(): ...
```
- [ ] A) test_a, test_b, test_c, test_d
- [ ] B) test_a, test_c, test_b, test_d
- [ ] C) test_d, test_b, test_c, test_a
- [ ] D) test_b, test_d, test_a, test_c

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) test_b, test_d, test_a, test_c

**Explanation:** The key returns `False` (0) for tests without the `slow` marker and `True` (1) for those with it, and `False < True`, so slow tests go to the end. Python's sort is stable, so each group keeps its original relative order.
- **Why others are wrong:**
  - A) That is the original order; the hook sorts the list in place.
  - B) That would put the slow tests first, which is the opposite of the key's effect.
  - C) The sort is stable and does not reverse anything.
</details>

---

### 45. What does this print? (Playwright sync API with the `page` fixture.)
```python
def test_lazy(page):
    badge = page.locator("#badge")
    page.set_content("<span id='badge'>3</span>")
    print(badge.inner_text(), badge.count())
```
- [ ] A) It raises `TimeoutError` because the element did not exist when the locator was created
- [ ] B) `None 0`
- [ ] C) `3 0`
- [ ] D) `3 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `3 1`

**Explanation:** A `Locator` is lazy: creating it does not search the page. The element is looked up when `inner_text()` and `count()` run, and by then the content has been set, so the text is `3` and one element matches.
- **Why others are wrong:**
  - A) Nothing is looked up at creation time, so there is no error.
  - B) The element exists at the time of the calls, so the text is not `None` and the count is not 0.
  - C) `count()` also resolves the locator at call time and finds one element.
</details>

---

### 46. What does this print? (The page contains no cart badge.)
```python
from playwright.sync_api import Page

class Header:
    def __init__(self, page: Page):
        self.cart_badge = page.locator(".cart-badge")

    def cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

def test_empty_cart(page: Page):
    page.set_content("<p>Your cart is empty</p>")
    print(Header(page).cart_count())
```
- [ ] A) It waits for the default timeout and raises `TimeoutError`
- [ ] B) `0`
- [ ] C) `None`
- [ ] D) It raises `ValueError` when converting an empty string

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `0`

**Explanation:** `count()` returns the number of matching elements right now without waiting. It is 0, so the guard returns `0` before `inner_text()` (which would wait and time out) is ever called.
- **Why others are wrong:**
  - A) That would happen if the guard were missing and `inner_text()` were called on the absent badge.
  - C) The method's return type is `int` and the guard returns the integer `0`.
  - D) `int(...)` is never reached.
</details>

---

### 47. What does this print?
```python
def test_card(page):
    page.set_content("""
      <div class="item">Backpack <button onclick="out.textContent='backpack'">Add to cart</button></div>
      <div class="item">Bike Light <button onclick="out.textContent='bike light'">Add to cart</button></div>
      <span id="out">none</span>
    """)
    items = page.locator(".item")
    items.filter(has_text="Bike Light").get_by_role("button", name="Add to cart").click()
    print(page.locator("#out").inner_text(), items.count())
```
- [ ] A) `backpack 2`
- [ ] B) `bike light 1`
- [ ] C) `bike light 2`
- [ ] D) It fails with a strict-mode violation because two "Add to cart" buttons exist

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `bike light 2`

**Explanation:** `.filter(has_text=...)` narrows the list to the card containing "Bike Light", and the chained `get_by_role` is scoped to that card, so only its button is clicked. `items` itself is unfiltered (`filter` returns a new locator), so `items.count()` is still 2.
- **Why others are wrong:**
  - A) The filter selects the Bike Light card, not the first one.
  - B) `filter` does not change `items`; it still matches both cards.
  - D) The chained locator matches exactly one button inside the filtered card, so there is no ambiguity.
</details>

---

### 48. What does this print?
```python
def test_dialog(page):
    page.set_content("<button onclick=\"document.title = confirm('Sure?') ? 'accepted' : 'dismissed'\">Delete</button>")
    page.once("dialog", lambda dialog: dialog.accept())
    button = page.get_by_role("button", name="Delete")
    button.click()
    print(page.title(), end=" ")
    button.click()
    print(page.title())
```
- [ ] A) `accepted dismissed`
- [ ] B) `accepted accepted`
- [ ] C) `dismissed dismissed`
- [ ] D) `accepted`, then a `TimeoutError` on the second click

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `accepted dismissed`

**Explanation:** `page.once` registers a one-time handler, so it accepts only the first dialog. The second dialog has no handler, and Playwright auto-dismisses dialogs without one, so `confirm()` returns false.
- **Why others are wrong:**
  - B) `once` is consumed after the first dialog; use `page.on` for a persistent handler.
  - C) The first dialog was accepted by the handler.
  - D) An unhandled dialog is dismissed automatically; it does not block the click.
</details>

---

### 49. How many tests does pytest collect and run?
```python
import pytest

@pytest.fixture(params=["chrome-like", "firefox-like", "webkit-like"])
def engine(request):
    return request.param

@pytest.mark.parametrize("sort_value", ["az", "za", "lohi", "hilo"])
@pytest.mark.parametrize("user", ["standard_user", "problem_user"])
def test_sort_for_each_user(engine, sort_value, user):
    pass
```
- [ ] A) 9
- [ ] B) 14
- [ ] C) 24
- [ ] D) 8

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 24

**Explanation:** Stacked `parametrize` decorators generate the cross product (4 x 2 = 8), and a parameterised fixture runs every test that uses it once per value (x 3), giving 4 x 2 x 3 = 24.
- **Why others are wrong:**
  - A) 9 would be 4 + 2 + 3; the dimensions multiply, they do not add.
  - B) 14 is not the result of any consistent combination of the three dimensions.
  - D) 8 ignores the parameterised fixture, which multiplies the count by 3.
</details>

---

### 50. What are the test ids that `pytest --collect-only -q` shows for this test?
```python
import pytest

CASES = [
    {"username": "locked_out_user", "expected": "locked out"},
    {"username": "", "expected": "Username is required"},
]

@pytest.mark.parametrize("case", CASES)
def test_invalid_login(case):
    pass
```
- [ ] A) `test_invalid_login[case0]` and `test_invalid_login[case1]`
- [ ] B) `test_invalid_login[{'username': 'locked_out_user', ...}]` and the same for the second dict
- [ ] C) `test_invalid_login[locked_out_user]` and `test_invalid_login[]`
- [ ] D) `test_invalid_login[0]` and `test_invalid_login[1]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `test_invalid_login[case0]` and `test_invalid_login[case1]`

**Explanation:** Without `ids=`, a dictionary value cannot be turned into a readable id, so pytest uses `case0`, `case1`. That is why the lesson recommends an `id` field in the data and `ids=[case["id"] for case in ...]`.
- **Why others are wrong:**
  - B) pytest does not print dictionaries into ids.
  - C) pytest does not pick a dictionary's first value as the id.
  - D) The fallback is the argument name plus index (`case0`), not the bare index.
</details>

---

### 51. What is the final summary line, and what is the id of the fourth test?
```python
import pytest

def cases_from(items):
    params, ids = [], []
    for index, item in enumerate(items):
        marks = []
        if "skip" in item:
            marks.append(pytest.mark.skip(reason=item["skip"]))
        if "xfail" in item:
            marks.append(pytest.mark.xfail(reason=item["xfail"]))
        params.append(pytest.param(item, marks=marks))
        ids.append(item.get("id", f"case-{index}"))
    return params, ids

PARAMS, IDS = cases_from([
    {"id": "ok", "v": 1},
    {"id": "bug", "v": 2, "xfail": "BUG-1"},
    {"v": 3, "skip": "later"},
    {"v": 4},
])

@pytest.mark.parametrize("case", PARAMS, ids=IDS)
def test_value(case):
    assert case["v"] != 2
```
- [ ] A) `3 passed, 1 skipped`; fourth id `case-3`
- [ ] B) `2 passed, 1 skipped, 1 xfailed`; fourth id `case-4`
- [ ] C) `2 passed, 1 skipped, 1 failed`; fourth id `case-3`
- [ ] D) `2 passed, 1 skipped, 1 xfailed`; fourth id `case-3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `2 passed, 1 skipped, 1 xfailed`; fourth id `case-3`

**Explanation:** `ok` and the fourth case pass, the third case is skipped from its JSON-style `skip` field, and `bug` fails as expected so it is reported as `xfailed`, not as a failure. `enumerate` is zero-based, so the id fallback for the fourth item is `case-3`.
- **Why others are wrong:**
  - A) The `bug` case does not pass; it fails and is recorded as `xfailed`.
  - B) `enumerate` starts at 0, so the fourth item has index 3, not 4.
  - C) An expected failure marked `xfail` does not count as a failure.
</details>

---

### 52. This test fails twice and passes on the third attempt (it uses a counter file). What is the final summary line of `pytest --reruns 2 -q`?
```python
from pathlib import Path

COUNTER = Path("retry_counter.txt")

def test_passes_on_third_attempt():
    attempts = int(COUNTER.read_text()) if COUNTER.exists() else 0
    attempts += 1
    COUNTER.write_text(str(attempts))
    if attempts < 3:
        raise AssertionError(f"simulated transient failure on attempt {attempts}")
    COUNTER.unlink()
```
- [ ] A) `1 failed, 2 rerun`
- [ ] B) `1 passed, 2 rerun`
- [ ] C) `1 passed, 1 rerun`
- [ ] D) `1 failed, 1 rerun`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `1 passed, 2 rerun`

**Explanation:** Attempts one and two fail and are shown as `R`, attempt three passes, so the progress line is `RR.` and the final result is passed with two reruns recorded.
- **Why others are wrong:**
  - A) The third attempt passes, so the final outcome is passed.
  - C) Two attempts failed before the pass, so two reruns happened.
  - D) That is the outcome with `--reruns 1`, where only one extra attempt is allowed and the test still fails.
</details>

---

### 53. What is the final summary line of `pytest --reruns 3 -q` for this test?
```python
import pytest

@pytest.mark.flaky(reruns=1)
def test_always_fails():
    assert False
```
- [ ] A) `1 failed, 3 rerun`
- [ ] B) `1 failed, 2 rerun`
- [ ] C) `1 failed, 1 rerun`
- [ ] D) `1 passed, 1 rerun`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1 failed, 1 rerun`

**Explanation:** The marker overrides the command-line value for that test, so it gets one rerun (two attempts in total). It fails both times, so the final result is failed.
- **Why others are wrong:**
  - A) That would use the command-line value, which the marker overrides.
  - B) That would correspond to `reruns=2`.
  - D) The test always fails, so it can never be reported as passed.
</details>

---

### 54. What does this print when the suite is run with `pytest -s`?
```python
# conftest.py
def pytest_sessionfinish(session, exitstatus):
    print(f"[hook] exit status {exitstatus}")

# test_one.py
def test_fails():
    assert 1 == 2
```
- [ ] A) `[hook] exit status 1`
- [ ] B) `[hook] exit status 0`
- [ ] C) `[hook] exit status 5`
- [ ] D) `[hook] exit status 2`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `[hook] exit status 1`

**Explanation:** The exit status is `0` when all tests pass, `1` when some tests failed, `2` when the run was interrupted and `5` when no tests were collected. CI pipelines treat any non-zero code as failure, which is why report-upload steps need `if: always()`.
- **Why others are wrong:**
  - B) `0` means all tests passed.
  - C) `5` means no tests were collected; here one test was collected and failed.
  - D) `2` means the user interrupted the run.
</details>

---

## Part 4: Fill-in-the-Blank

### 55. To log in once and reuse the session, save cookies and local storage with `context._____(path="auth.json")`, then start later contexts already logged in with `browser.new_context(_____="auth.json")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `storage_state` (both blanks)

**Explanation:** `context.storage_state(path=...)` writes the cookies and local storage to a JSON file, and `new_context(storage_state=...)` loads them so the new context starts authenticated. Add `.auth/` to `.gitignore`, because the file may contain session tokens.
</details>

---

### 56. The command `pytest --_____ tests/test_login.py` prints every fixture's SETUP and TEARDOWN with a scope letter (S, M, C or F), which helps when fixture order surprises you.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `setup-show` (that is, `pytest --setup-show`)

**Explanation:** `--setup-show` reveals the otherwise invisible fixture machinery, for example that `browser` is set up once with scope `S` while `page` is set up and torn down per test with scope `F`. (`pytest --fixtures` lists available fixtures with their docstrings.)
</details>

---

### 57. The plug-in hook `pytest_runtest_____` builds the report for each of the three phases (setup, call, teardown). To observe the finished report, you write it as a wrapper using `@pytest.hookimpl(_____=True)` and read the result with `outcome.get_result()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `makereport` and `hookwrapper`

**Explanation:** `pytest_runtest_makereport(item, call)` is the hook; the hook wrapper runs code before and after pytest builds the report (`outcome = yield`), so you can store `rep_setup`, `rep_call` and `rep_teardown` on the test item and detect failures.
</details>

---

### 58. In a `pytest_runtest_makereport` hook, a failure screenshot is attached to the pytest-html report by importing `from pytest_html import _____` and appending `_____.png(encoded, name="Failure screenshot")` to `report.extras`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `extras` (both blanks)

**Explanation:** `extras` provides constructors such as `extras.png`, `extras.url`, `extras.text`, `extras.html`, and `extras.json`. The PNG must be base64 text; get it from `page.screenshot()` bytes with `base64.b64encode(...).decode("utf-8")`. Note that older pytest-html versions used a different API (`extra`), so check your installed version.
</details>

---

### 59. A Playwright `Locator` is _____: creating `page.get_by_test_id("username")` only stores how to find the element, and the search happens when you act on or assert on it, with auto-waiting.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** lazy

**Explanation:** Because locators are lazy, defining all of them once in a page object's `__init__` is safe and idiomatic, even for elements that are not on the page yet or that get re-rendered. This is a major difference from older Selenium-style page objects that held stale element references.
</details>

---

### 60. In a converted page object, a method that moves the user to another screen should construct, run a readiness check on, and return the _____ page object, so a test reads like a user journey (fluent navigation).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** next

**Explanation:** For example `login_successfully()` returns an `InventoryPage` after calling `expect_loaded()`, and `open_cart()` returns a `CartPage`. A method that stays on the same screen returns `self` (enabling chains) or `None`.
</details>

---

### 61. `json._____(text)` parses a JSON *string* into Python objects, while `json._____(f)` reads from an open file object.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `loads`, then `load`

**Explanation:** The `s` in `loads` (and `dumps`) stands for "string"; `load` and `dump` work with file objects. After loading, JSON objects become `dict`, arrays become `list`, `true`/`false` become `True`/`False`, and `null` becomes `None`.
</details>

---

### 62. To expect a failure for one specific data row only, wrap it as `pytest.param("problem_user", marks=pytest.mark._____(reason="BUG-123"))`; if that row fails the result is reported as xfailed, and if it unexpectedly passes it is reported as xpassed.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `xfail`

**Explanation:** `pytest.param(value, marks=..., id=...)` attaches per-row marks or ids. An `xfail` row keeps the suite green while tracking the defect, and an `XPASS` is the signal that the bug may have been fixed and the marker can be removed.
</details>

---

### 63. With pytest-rerunfailures, the option `--_____-rerun "TimeoutError"` (repeatable, takes a regular expression) retries a failed test only when its error output matches.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `only` (that is, `--only-rerun`)

**Explanation:** `--only-rerun REGEX` limits retries to failures that look transient, such as timeouts or `net::ERR_` network errors. Its counterpart `--rerun-except REGEX` excludes matching failures, for example `AssertionError`, from being retried. Retrying deterministic failures only wastes time.
</details>

---

### 64. pytest-rerunfailures records the attempt number on the test item as `request.node._____`: 1 for the first run, 2 for the first rerun, and so on. It is read with `getattr(request.node, "...", 1)` to be safe when the plug-in is not active.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `execution_count`

**Explanation:** Reading `execution_count` lets a fixture collect extra diagnostics (console messages, failed requests) only on retries, so a normal run stays quiet and a retry becomes extra evidence rather than a blind second chance.
</details>

---

### 65. The command `pytest --html=reports/report.html --_____-contained-html` creates a single portable report file with CSS and base64 images embedded.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `self` (that is, `--self-contained-html`)

**Explanation:** Always use it for reports you plan to share, because without it the report depends on side files and breaks when emailed or moved.
</details>

---

### 66. pytest-playwright stores screenshots, videos and traces in the folder chosen with `--_____` (default `test-results`), and that folder is deleted and recreated at the start of every run.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `output` (that is, `--output`)

**Explanation:** Because the default output folder is recreated each run, copy out anything you need (or let CI upload it) and add `test-results/` and `reports/` to `.gitignore`. The artifact options `--screenshot`, `--video` and `--tracing` accept `retain-on-failure` or `only-on-failure` values to keep disk use low.
</details>

---

*End of quiz: 66 questions.*
