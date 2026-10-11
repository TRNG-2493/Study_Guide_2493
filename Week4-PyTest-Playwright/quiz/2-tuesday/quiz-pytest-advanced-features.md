# Weekly Knowledge Check: Tuesday (Day 2) - PyTest Advanced Features

**Week 4: PyTest and Playwright** | Quiz file: `quiz-pytest-advanced-features.md`

## Topics covered today

1. **Fixtures in PyTest**: `@pytest.fixture`, requesting by parameter name, `yield` setup/teardown, fixture chains, factory fixtures, built-in fixtures (`tmp_path`, `capsys`, `monkeypatch`, `request`), `autouse`, `params`, `name=`
2. **Fixture scopes**: `function`, `class`, `module`, `package`, `session`, the scope-dependency rule (`ScopeMismatch`), shared mutable state, `tmp_path_factory`, `--setup-show`
3. **Parametrization**: `@pytest.mark.parametrize`, `ids`, `pytest.param` with marks, stacked decorators, loading data, selecting cases, `parametrize` vs fixture `params`
4. **conftest.py**: auto-loading, hierarchy and overriding, hooks (`pytest_configure`, `pytest_addoption`, `pytest_collection_modifyitems`), helpers vs fixtures
5. **Sharing fixtures across tests**: module, class and directory levels, `usefixtures`, `pytest_plugins`, overriding, layering, safe sharing of values
6. **Combining fixtures and parametrization**: parametrized fixtures, `request.param`, `indirect`, Cartesian products, scope interactions
7. **Mocking with `unittest.mock`**: test doubles, `Mock`/`MagicMock`, `side_effect`, call assertions, `patch` (and where to patch), `autospec`

## Instructions

- This quiz has **66 questions** in four parts: Multiple Choice, True/False, Code Prediction, and Fill-in-the-Blank.
- Try to answer each question on your own first (tick the box you think is right, or write the blank on paper).
- Then click **"Click for Solution"** to reveal the correct answer and the reasoning. Read the explanation even when you were right: it also explains why the other options are wrong.
- Every answer is based only on today's lessons. Topics may appear more than once, asked in a different way.
- The Code Prediction answers were checked by actually running the snippets with `python3 -m pytest`.

---

## Part 1: Multiple Choice

### 1. What is a fixture in PyTest?

- [ ] A) A marker that tells PyTest to skip a test when a condition is met
- [ ] B) A function marked with `@pytest.fixture` that prepares (and optionally cleans up) something a test needs, and hands it to the test
- [ ] C) A helper that compares floating-point numbers with a tolerance
- [ ] D) A command-line flag that runs tests in parallel

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A function marked with `@pytest.fixture` that prepares (and optionally cleans up) something a test needs, and hands it to the test

**Explanation:** A fixture is a function PyTest runs for you to prepare what a test needs (the arrange step) and optionally clean up afterwards. The returned value is injected into the test.
- **Why others are wrong:**
  - A) Skipping is done with markers such as `skip`; a fixture is a setup/teardown provider, not a marker.
  - C) That describes `pytest.approx`, not a fixture.
  - D) Fixtures are code in your test files or conftest, not command-line flags.

</details>

---
### 2. How does a test function request a fixture called `filled_cart`?

- [ ] A) By calling `cart = filled_cart()` inside the test body
- [ ] B) By writing `@pytest.fixture(filled_cart)` above the test
- [ ] C) By importing `filled_cart` into `conftest.py`
- [ ] D) By adding `filled_cart` as a parameter of the test function

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) By adding `filled_cart` as a parameter of the test function

**Explanation:** PyTest sees the parameter name, finds a fixture with that name, runs it, and passes the result in. You never call the fixture yourself.
- **Why others are wrong:**
  - A) Calling a fixture directly raises an error in modern PyTest ("Fixture called directly"); you must request it as a parameter.
  - B) `@pytest.fixture` marks a function as a fixture provider; it is not how a test requests one.
  - C) Where a fixture lives does not request it; a test or fixture must still name it as a parameter (or use `autouse`/`usefixtures`).

</details>

---
### 3. Why would you write a fixture with `yield` instead of `return`?

- [ ] A) Code after the `yield` runs as teardown after the test, even if the test failed
- [ ] B) `yield` makes the fixture run faster than `return`
- [ ] C) `return` cannot hand an object to a test, only `yield` can
- [ ] D) `yield` automatically makes the fixture `autouse=True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Code after the `yield` runs as teardown after the test, even if the test failed

**Explanation:** With `return` the function ends and there is nowhere to put cleanup. With `yield`, everything after it runs when the test finishes, whether it passed or failed.
- **Why others are wrong:**
  - B) `yield` is about teardown, not speed.
  - C) `return` works fine for setup-only fixtures; it just gives you no place for cleanup.
  - D) `autouse` is a separate argument of `@pytest.fixture`; `yield` does not change it.

</details>

---
### 4. Fixtures `cart` -> `cart_with_pen` -> `cart_with_pen_and_book` are set up in that order for one test. In what order is teardown done?

- [ ] A) In the same order as setup: `cart` first
- [ ] B) In alphabetical order of the fixture names
- [ ] C) In reverse order: `cart_with_pen_and_book`, then `cart_with_pen`, then `cart`
- [ ] D) In random order, because fixtures are independent

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) In reverse order: `cart_with_pen_and_book`, then `cart_with_pen`, then `cart`

**Explanation:** Teardown order is the reverse of setup order (last in, first out). The base `cart` fixture is created first, so it is torn down last.
- **Why others are wrong:**
  - A) Teardown is last-in, first-out, like unstacking plates, not the same order as setup.
  - B) Alphabetical order plays no role; the dependency order is reversed.
  - D) The fixtures depend on each other, and PyTest tears them down in the reverse of the setup order.

</details>

---
### 5. Which built-in fixture captures text written to stdout and stderr so a test can assert on a `print` call?

- [ ] A) `tmp_path`
- [ ] B) `monkeypatch`
- [ ] C) `caplog`
- [ ] D) `capsys`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `capsys`

**Explanation:** `capsys.readouterr()` returns an object with `.out` and `.err` attributes holding what was written to stdout and stderr.
- **Why others are wrong:**
  - A) `tmp_path` gives each test a unique temporary directory, not captured output.
  - B) `monkeypatch` safely changes attributes, dict items, or environment variables for one test.
  - C) `caplog` captures log records, not text printed to stdout/stderr.

</details>

---
### 6. A test needs to build several different `ShoppingCart` objects with different contents. Which fixture design fits best?

- [ ] A) An `autouse=True` fixture that returns one cart
- [ ] B) A factory fixture that returns a function the test can call many times
- [ ] C) A `return` fixture with a module-level list as the cart
- [ ] D) A fixture that calls `assert` on each cart it builds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A factory fixture that returns a function the test can call many times

**Explanation:** A factory fixture returns a function (like `_make`), so the test can create as many instances as it needs. It can also remember them for teardown.
- **Why others are wrong:**
  - A) `autouse` applies a fixture automatically; it gives one object, not many differently configured ones, and it hides what the test needs.
  - C) A module-level mutable object is shared by every test, which is a common mistake (shared mutable state).
  - D) Fixtures should prepare, not verify; asserts in fixtures show up as errors rather than failures.

</details>

---
### 7. Which list shows the five fixture scopes from narrowest to widest?

- [ ] A) `function`, `class`, `module`, `package`, `session`
- [ ] B) `function`, `module`, `class`, `package`, `session`
- [ ] C) `session`, `package`, `module`, `class`, `function`
- [ ] D) `function`, `class`, `package`, `module`, `session`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `function`, `class`, `module`, `package`, `session`

**Explanation:** The order from narrowest to widest is `function` < `class` < `module` < `package` < `session`; `function` is the default.
- **Why others are wrong:**
  - B) `class` is narrower than `module`; a module can contain several classes.
  - C) That is widest to narrowest, the reverse of what was asked.
  - D) A `module` (one `.py` file) is narrower than a `package` (a directory of tests).

</details>

---
### 8. You have an expensive, read-only `app_config` fixture needed in many test files, and it must be created only once per `pytest` run. What is the best choice?

- [ ] A) `scope="module"` defined in each test file
- [ ] B) The default `function` scope
- [ ] C) `scope="session"`, defined in a shared `conftest.py`
- [ ] D) `scope="class"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `scope="session"`, defined in a shared `conftest.py`

**Explanation:** Session scope lives for the whole run, and putting the fixture in `conftest.py` is the right way to share it across files because module scope is only per file.
- **Why others are wrong:**
  - A) Module scope is per file, so the fixture would be created once per file and defined repeatedly.
  - B) Function scope creates the fixture again for every test, repeating the expensive work.
  - D) Class scope creates the fixture once per test class, which does not span multiple files.

</details>

---
### 9. Which fixture dependency is allowed by PyTest's scope rule?

- [ ] A) A `session`-scoped fixture that requests a `function`-scoped fixture
- [ ] B) A `function`-scoped fixture that requests a `session`-scoped fixture
- [ ] C) A `module`-scoped fixture that requests a `function`-scoped fixture
- [ ] D) A `session`-scoped fixture that requests a `class`-scoped fixture

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A `function`-scoped fixture that requests a `session`-scoped fixture

**Explanation:** A fixture can only depend on fixtures with the same or wider scope; the opposite direction (narrow depends on wide) is perfectly fine.
- **Why others are wrong:**
  - A) This raises `ScopeMismatch`: a long-lived fixture cannot depend on one destroyed after each test.
  - C) Also a `ScopeMismatch`; a fixture may only request fixtures of the same or wider scope.
  - D) `class` is narrower than `session`, so this is also a `ScopeMismatch`.

</details>

---
### 10. A team keeps one `database` connection for the whole run but wants each test to start with empty tables. Which pattern from the lesson fits?

- [ ] A) A session-scoped `database` fixture only, and tests clean up after themselves manually
- [ ] B) A function-scoped `database` fixture that reconnects for every test
- [ ] C) A module-scoped `database` fixture shared by all files
- [ ] D) A session-scoped `database` fixture plus a function-scoped `clean_db` fixture that clears the data before and after each test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A session-scoped `database` fixture plus a function-scoped `clean_db` fixture that clears the data before and after each test

**Explanation:** Wide expensive resource plus narrow reset fixture gives speed and isolation. The `clean_db` fixture (function scope) may depend on the session-scoped `database` because narrow may depend on wide.
- **Why others are wrong:**
  - A) That risks order-dependent tests if any test forgets to clean; the pattern uses a narrow reset fixture.
  - B) That is safe but repeats the expensive connection for every test, losing the speed benefit.
  - C) Module scope is per file, so it would not give one connection for the whole run.

</details>

---
### 11. Which option lets you watch fixture setup and teardown, with the scope letter (S, M, C, F) of each fixture, without adding `print` calls?

- [ ] A) `pytest --setup-show`
- [ ] B) `pytest --fixtures`
- [ ] C) `pytest --collect-only -q`
- [ ] D) `pytest -s`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `pytest --setup-show`

**Explanation:** `--setup-show` prints lines like `SETUP    S session_fx` and `TEARDOWN F function_fx`; the letters denote the scope. It is the best debugging tool for scope questions.
- **Why others are wrong:**
  - B) `--fixtures` lists the available fixtures and where they are defined; it does not show run-time setup/teardown.
  - C) `--collect-only` lists generated test IDs without running them.
  - D) `-s` only shows `print` output that PyTest would otherwise capture.

</details>

---
### 12. A parametrized test has five parameter sets and the case `(18, True)` fails. What happens to the other four cases?

- [ ] A) They are skipped because the first failure stops the test function
- [ ] B) They are marked `xfail` automatically
- [ ] C) They still run and are reported individually as passed or failed
- [ ] D) They all fail too, because they share one test function body

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) They still run and are reported individually as passed or failed

**Explanation:** Parametrization creates separate tests, one per parameter set, reported individually. A failure in one case does not affect the others.
- **Why others are wrong:**
  - A) PyTest generates five separate tests, so one failure does not stop the others.
  - B) `xfail` must be attached explicitly to a case; it is not applied after a failure.
  - D) Each parameter set becomes its own test with its own result.

</details>

---
### 13. What does the `ids=` argument of `@pytest.mark.parametrize` do?

- [ ] A) It assigns a unique database ID to each test result
- [ ] B) It selects which parameter sets to run
- [ ] C) It converts the parameter values to strings before the test receives them
- [ ] D) It gives each case a readable test ID, and the list must be the same length as the data

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It gives each case a readable test ID, and the list must be the same length as the data

**Explanation:** Without `ids`, PyTest generates cryptic IDs like `[0-False]`. With `ids=["just-below-limit", ...]` reports become readable.
- **Why others are wrong:**
  - A) `ids` only affects the text inside `[...]` of the test ID.
  - B) Selection is done with `-k`, `-m` or a node ID on the command line.
  - C) The test still receives the original values; `ids` only names the cases.

</details>

---
### 14. You want one parameter set, `(-1, False)`, to count as an expected failure only if it raises `ValueError`, while the other cases run normally. What do you write?

- [ ] A) `@pytest.mark.skip` on the whole test function
- [ ] B) `pytest.param(-1, False, marks=pytest.mark.xfail(raises=ValueError))`
- [ ] C) `ids=["xfail"]` on the decorator
- [ ] D) `pytest.param(-1, False, marks=pytest.mark.skip)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `pytest.param(-1, False, marks=pytest.mark.xfail(raises=ValueError))`

**Explanation:** `pytest.param` wraps one parameter set so you can attach an `id` and `marks`. With `raises=ValueError`, only that exception counts as the expected failure and the case is reported as `xfailed`.
- **Why others are wrong:**
  - A) That skips every case, not just one.
  - C) `ids` only renames cases; it cannot change their outcome.
  - D) `skip` excludes the case entirely instead of running it and expecting a `ValueError` failure.

</details>

---
### 15. A test is decorated with `@pytest.mark.parametrize("x", [1, 2, 3])` and also with `@pytest.mark.parametrize("y", [10, 20, 30, 40])`. How many tests are generated?

- [ ] A) 12, because stacked decorators create a Cartesian product
- [ ] B) 7, because the lists are added together
- [ ] C) 4, because only the bottom decorator is used
- [ ] D) 3, because the top decorator decides the count

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 12, because stacked decorators create a Cartesian product

**Explanation:** Stacking multiple `parametrize` decorators produces every combination: 3 x 4 = 12 tests. Combinations grow multiplicatively, so watch the count.
- **Why others are wrong:**
  - B) Stacked decorators multiply the possibilities; they do not add them.
  - C) Both decorators contribute; every combination is generated.
  - D) Both lists multiply: 3 x 4 = 12.

</details>

---
### 16. What is the main difference between `@pytest.mark.parametrize` and `@pytest.fixture(params=...)`?

- [ ] A) `parametrize` applies to every test using it, while fixture `params` applies to one test only
- [ ] B) Only `params=` generates separate tests; `parametrize` runs all values inside one test
- [ ] C) `parametrize` applies to one test function or class, while fixture `params` apply to every test that uses the fixture
- [ ] D) `params=` can only be used with strings, while `parametrize` accepts any object

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `parametrize` applies to one test function or class, while fixture `params` apply to every test that uses the fixture

**Explanation:** `parametrize` keeps the data visible at the test and suits input/expected tables. Fixture `params` hide the data in the fixture and suit running everything under each environment, such as a browser.
- **Why others are wrong:**
  - A) That is reversed.
  - B) Both generate separate tests, one per value.
  - D) Both accept any Python objects; the difference is reach and visibility.

</details>

---
### 17. Which statement about `conftest.py` is correct?

- [ ] A) You must write `import conftest` in each test file that wants its fixtures
- [ ] B) PyTest loads it automatically, so you never import it, and it is not collected as a test file
- [ ] C) PyTest collects test functions from it because it contains fixtures
- [ ] D) Any file whose name contains the word `conf` is treated the same way

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) PyTest loads it automatically, so you never import it, and it is not collected as a test file

**Explanation:** `conftest.py` is auto-loaded and can hold fixtures, hooks and helper code for its directory and everything below it.
- **Why others are wrong:**
  - A) Tests simply request fixtures by name; importing from conftest is fragile and unnecessary.
  - C) It does not match `test_*.py`, so PyTest does not collect tests from it.
  - D) The name must be exactly `conftest.py` (lowercase); `confest.py` or `conf_test.py` silently do nothing.

</details>

---
### 18. `greeting` is defined in `tests/conftest.py` and again in `tests/unit/conftest.py`. A test in `tests/unit/` requests `greeting`. Which definition does it get?

- [ ] A) The one in `tests/conftest.py`, because parent files take priority
- [ ] B) Neither; PyTest raises an ambiguity error
- [ ] C) Both are executed and the results are combined
- [ ] D) The one in `tests/unit/conftest.py`, because the closest definition wins

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The one in `tests/unit/conftest.py`, because the closest definition wins

**Explanation:** Tests see the fixtures of their own folder's conftest and every parent, and when names clash the closest one wins. A child can also wrap the parent by requesting a fixture of the same name.
- **Why others are wrong:**
  - A) The child (closest) definition overrides the parent.
  - B) PyTest has a clear rule: the closest definition wins, so there is no ambiguity.
  - C) Only one definition is used for a given request.

</details>

---
### 19. A fixture `unit_only` is defined in `tests/unit/conftest.py`. A test in the sibling folder `tests/api/` requests it. What happens?

- [ ] A) The test errors with "fixture 'unit_only' not found", because sibling folders do not share conftest fixtures
- [ ] B) It works, because both folders are under `tests/`
- [ ] C) It falls back to the root conftest version automatically
- [ ] D) The test is silently skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The test errors with "fixture 'unit_only' not found", because sibling folders do not share conftest fixtures

**Explanation:** A fixture needed by both `api` and `unit` tests belongs in a conftest at the common parent, such as `tests/conftest.py`.
- **Why others are wrong:**
  - B) Only the test's own folder and its parents are searched, not siblings.
  - C) There is no root version; and fallback only applies when a parent defines the same name.
  - D) A missing fixture is an error at setup, not a skip.

</details>

---
### 20. Which hook lets you edit the list of collected tests, for example to add a skip marker to every test marked `slow` unless `--runslow` is passed?

- [ ] A) `pytest_configure(config)`
- [ ] B) `pytest_addoption(parser)`
- [ ] C) `pytest_collection_modifyitems(config, items)`
- [ ] D) `pytest_runtest_makereport`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `pytest_collection_modifyitems(config, items)`

**Explanation:** `pytest_collection_modifyitems` receives `items`, the list of test objects; you can inspect `item.keywords` and call `item.add_marker(...)` to skip tests.
- **Why others are wrong:**
  - A) That runs once at startup and is good for registering markers, not for editing the collected test list.
  - B) That adds command-line options such as `--runslow`; it does not modify collected items.
  - D) That is used to attach results to reports (awareness-level) and is not for editing collection.

</details>

---
### 21. What is the recommended way to reuse a plain helper function across many test files?

- [ ] A) Define it in `conftest.py` and write `from conftest import helper` in each test file
- [ ] B) Copy and paste it into every test file
- [ ] C) Register it in `pytest.ini` under `markers`
- [ ] D) Put it in a normal module like `tests/helpers.py`, or expose it through a factory fixture

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Put it in a normal module like `tests/helpers.py`, or expose it through a factory fixture

**Explanation:** Conftest is for fixtures, hooks and configuration. Helpers live in a regular module, or better, in a factory fixture so tests need no imports.
- **Why others are wrong:**
  - A) Importing from conftest is fragile because PyTest imports conftest in a special way and it can load twice or fail.
  - B) Duplication is exactly what shared structure is meant to avoid.
  - C) `markers` only registers custom marker names; it does not share code.

</details>

---
### 22. Which statement correctly separates "sharing the definition" from "sharing the value" of a fixture?

- [ ] A) Sharing the value is decided by where the fixture file is located
- [ ] B) Sharing the definition is code reuse (each test gets its own result), while sharing the value comes from a wider scope
- [ ] C) Sharing the definition always gives every test the same object
- [ ] D) They are the same thing; wider scope only changes the name of the fixture

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Sharing the definition is code reuse (each test gets its own result), while sharing the value comes from a wider scope

**Explanation:** Where a fixture is placed concerns reuse of code; its scope decides whether tests receive the same object, which is faster but dangerous if the object is mutable.
- **Why others are wrong:**
  - A) Location decides who can use the definition; scope decides whether the same object is shared.
  - C) With the default function scope each test gets a fresh result.
  - D) They are two different ideas, and mixing them up is a common beginner mistake.

</details>

---
### 23. What does `@pytest.mark.usefixtures("clean_env")` on a test class do?

- [ ] A) It runs the `clean_env` fixture for every method in the class, but does not pass its value to the tests
- [ ] B) It passes the fixture's return value to each method as an extra argument
- [ ] C) It makes `clean_env` session scoped
- [ ] D) It applies only to the first method in the class

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It runs the `clean_env` fixture for every method in the class, but does not pass its value to the tests

**Explanation:** Use `usefixtures` when you need only the effect of a fixture. At module level you can write `pytestmark = pytest.mark.usefixtures("clean_env")`.
- **Why others are wrong:**
  - B) `usefixtures` cannot pass the value; request the fixture as an argument if you need it.
  - C) `usefixtures` does not change the fixture's scope.
  - D) Applied to a class, it covers all its methods.

</details>

---
### 24. How do you load several fixture modules (for example `tests.fixtures.users`) into your test suite using `pytest_plugins`?

- [ ] A) Assign a list of file paths such as `"tests/fixtures/users.py"` in any nested conftest
- [ ] B) Add the module names under `markers =` in `pytest.ini`
- [ ] C) Assign a list of importable module names to `pytest_plugins` in the top-level `conftest.py`
- [ ] D) Write `from tests.fixtures.users import *` in every test file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Assign a list of importable module names to `pytest_plugins` in the top-level `conftest.py`

**Explanation:** PyTest imports each listed module and registers its fixtures as if they were defined in the conftest. If you see `ModuleNotFoundError`, check `__init__.py` files and `pythonpath`.
- **Why others are wrong:**
  - A) The list holds importable dotted module names, and it belongs in the top-level conftest, not any nested one.
  - B) `markers` registers custom marker names only.
  - D) Wildcard imports can bring surprises and linters complain; `pytest_plugins` is the supported way for bulk sharing.

</details>

---
### 25. A session-scoped `_template_user` fixture returns a dict containing a list of tags. Which design lets each test safely mutate its user without affecting other tests?

- [ ] A) A function-scoped `user` fixture that returns `copy.copy(_template_user)`
- [ ] B) A function-scoped `user` fixture that returns `copy.deepcopy(_template_user)`
- [ ] C) Return `_template_user` directly from each test's fixture
- [ ] D) Make `user` an `autouse` fixture with no return value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A function-scoped `user` fixture that returns `copy.deepcopy(_template_user)`

**Explanation:** Copy on request is one of the safe patterns for sharing values. `copy.deepcopy` copies nested objects too, so both tests pass in any order.
- **Why others are wrong:**
  - A) A shallow copy shares the inner list, so appending to the tags would still leak between tests.
  - C) That shares the same mutable object by reference and causes order-dependent failures.
  - D) `autouse` does not create per-test copies; tests would have nothing to mutate safely.

</details>

---
### 26. Which guideline for placing a shared fixture does the lesson give?

- [ ] A) Always put every fixture in the root `conftest.py` so everyone can find it
- [ ] B) Put every fixture in the test file that uses it first, and copy it later
- [ ] C) Make shared fixtures `autouse` so nobody can forget to request them
- [ ] D) Put each fixture at the lowest level that still covers all the tests that need it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Put each fixture at the lowest level that still covers all the tests that need it

**Explanation:** Keeping a fixture as close as possible to its users keeps the scope of knowledge small and discoverable.
- **Why others are wrong:**
  - A) That makes the root file bloated; a fixture used only by `api` tests belongs in `tests/api/conftest.py`.
  - B) Copy-pasting the same fixture in several files is listed as a common mistake.
  - C) `autouse` in shared files affects everyone below it and is discouraged; prefer explicit over implicit.

</details>

---
### 27. What does `@pytest.mark.parametrize("cart_with_qty, expected", [...], indirect=["cart_with_qty"])` do with the first value of each tuple?

- [ ] A) It delivers the value to the `cart_with_qty` fixture as `request.param`, and the test receives whatever the fixture returns
- [ ] B) It passes the raw value straight to the test and ignores the fixture
- [ ] C) It also sends `expected` through a fixture named `expected`
- [ ] D) It runs the fixture once and reuses the first value for every case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It delivers the value to the `cart_with_qty` fixture as `request.param`, and the test receives whatever the fixture returns

**Explanation:** `indirect` routes the value through the fixture first, so the table stays short (`1, 3, 10`) while the building logic and any teardown live in the fixture.
- **Why others are wrong:**
  - B) That is what happens without `indirect`; with it, the value goes through the fixture.
  - C) `expected` is not in the `indirect` list, so it is passed to the test as a plain value.
  - D) The fixture runs for each parameter set (function scope by default), receiving each value in turn.

</details>

---
### 28. A fixture uses `request.param`, but the test requesting it has no parametrization and the fixture has no `params`. What do you get?

- [ ] A) A `ScopeMismatch` error
- [ ] B) The test runs once with `request.param` equal to `None`
- [ ] C) `AttributeError: 'SubRequest' object has no attribute 'param'`
- [ ] D) PyTest silently skips the test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `AttributeError: 'SubRequest' object has no attribute 'param'`

**Explanation:** Fix it by adding `params=[...]` to the fixture, or by using `@pytest.mark.parametrize("name", [...], indirect=True)` on the test.
- **Why others are wrong:**
  - A) `ScopeMismatch` is about requesting a narrower-scope fixture from a wider one.
  - B) There is no default; the attribute simply does not exist.
  - D) PyTest raises an error instead of skipping.

</details>

---
### 29. A module-scoped fixture has `params=["db_a", "db_b"]`, and the file has two tests that use it. How many times is the fixture set up in that module?

- [ ] A) Four times, once per generated test
- [ ] B) Once in total, because it is module scoped
- [ ] C) Never, because parametrized fixtures cannot be module scoped
- [ ] D) Twice, once per parameter value, because PyTest groups the tests to minimise setups

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Twice, once per parameter value, because PyTest groups the tests to minimise setups

**Explanation:** PyTest connects `db_a`, runs both tests for `db_a`, disconnects, then does the same for `db_b`. For function scope there is no grouping.
- **Why others are wrong:**
  - A) That would be function-scope behaviour; module scope plus grouping reduces it to one setup per value.
  - B) A parametrized fixture is created once per parameter value per module.
  - C) Scope still applies to parametrized fixtures.

</details>

---
### 30. You want every UI test in the suite to run once under each of three browsers without touching the tests. Which technique fits best?

- [ ] A) Add `@pytest.mark.parametrize` manually to every test
- [ ] B) A parametrized fixture with `params=` for the browser
- [ ] C) An `autouse` fixture without `params`
- [ ] D) Use `indirect=True` on one test only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A parametrized fixture with `params=` for the browser

**Explanation:** A parametrized fixture reaches every test that uses it, which suits "run everything under each browser/database". The trade-off is hidden multiplication, so use `--setup-show` or `--collect-only` to inspect.
- **Why others are wrong:**
  - A) That works but repeats the table on every test; the fixture approach is written once and applies everywhere.
  - C) Without `params` the fixture runs once per test and gives a single value.
  - D) That affects only that test, not every test using the fixture.

</details>

---
### 31. In the vocabulary of test doubles, what is an in-memory dictionary used instead of a real database?

- [ ] A) A fake, a simplified working implementation
- [ ] B) A dummy
- [ ] C) A stub
- [ ] D) A spy

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A fake, a simplified working implementation

**Explanation:** A fake is a simplified but working implementation. In everyday talk people say "mock" for all of these doubles.
- **Why others are wrong:**
  - B) A dummy only fills a parameter and is never really used.
  - C) A stub returns canned answers (like `get_price()` always returning `9.99`) rather than working like the real thing.
  - D) A spy is a real object wrapped so calls are recorded.

</details>

---
### 32. Which of these is a good reason to replace a dependency with a mock?

- [ ] A) You want to avoid testing your own function, so you mock the function under test
- [ ] B) Mocks remove the need for any integration tests
- [ ] C) You need to simulate a hard-to-trigger state such as an HTTP 500 error or a timeout
- [ ] D) Mocks make the test pass without writing any assertions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) You need to simulate a hard-to-trigger state such as an HTTP 500 error or a timeout

**Explanation:** Mock dependencies that are slow, non-deterministic, unavailable, costly or dangerous, or hard to put in a specific state.
- **Why others are wrong:**
  - A) You should not mock the thing you are testing; the test would prove nothing.
  - B) The lesson recommends unit tests mock boundaries while a few integration tests use real components.
  - D) A mock never verified, with no assertion on result or call, may prove nothing.

</details>

---
### 33. `module_a.py` does `from requests import get` and calls `get(...)`. Which patch target makes your test intercept that call?

- [ ] A) `patch("requests.get")`
- [ ] B) `patch("module_a.get")`
- [ ] C) `patch("requests")`
- [ ] D) `patch("module_a.requests.get")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `patch("module_a.get")`

**Explanation:** Golden rule: patch where the name is looked up, not where it is defined. In short, patch the name in the namespace of the code under test.
- **Why others are wrong:**
  - A) That changes the original, but `module_a` still holds its own reference to the real function.
  - C) That does not replace the name `get` that lives inside `module_a`.
  - D) `module_a` has no attribute `requests`, because it imported only `get`.

</details>

---
### 34. How does `side_effect` differ from `return_value` on a mock?

- [ ] A) `side_effect` can only be used with `patch`, not with `Mock`
- [ ] B) They are aliases; both always return one fixed value
- [ ] C) `return_value` raises exceptions, `side_effect` returns values
- [ ] D) `return_value` always returns the same thing, whereas `side_effect` can raise an exception, return a different value each call, or compute the result with a function

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `return_value` always returns the same thing, whereas `side_effect` can raise an exception, return a different value each call, or compute the result with a function

**Explanation:** For example `Mock(side_effect=ConnectionError("network down"))` raises when called, and `Mock(side_effect=[1, 2, 3])` returns 1, 2, 3 on successive calls.
- **Why others are wrong:**
  - A) `Mock(side_effect=...)` works directly, as in `Mock(side_effect=[1, 2, 3])`.
  - B) `side_effect` is more flexible: errors, sequences and functions.
  - C) That is reversed.

</details>

---
### 35. A notifier mock was called twice: `send("a@x.com", "Hi")` and then `send("b@x.com", "Hi")`. Which assertion checks that the MOST RECENT call used `("b@x.com", "Hi")`?

- [ ] A) `notifier.send.assert_called_with("b@x.com", "Hi")`
- [ ] B) `notifier.send.assert_any_call("b@x.com", "Hi")`
- [ ] C) `notifier.send.assert_called_once_with("b@x.com", "Hi")`
- [ ] D) `notifier.send.assert_not_called()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `notifier.send.assert_called_with("b@x.com", "Hi")`

**Explanation:** `assert_called_with` checks the last call, `assert_any_call` checks that some call matched, and `assert_has_calls` checks calls in order.
- **Why others are wrong:**
  - B) `assert_any_call` passes if any call matched; it does not say the call was the last one.
  - C) It requires exactly one call in total, but there were two.
  - D) It checks the mock was never called, which is false here.

</details>

---
### 36. What is the main benefit of `create_autospec(EmailGateway, instance=True)` over a plain `Mock()`?

- [ ] A) It makes the tests run faster than a plain `Mock`
- [ ] B) It automatically asserts that every method was called
- [ ] C) Calls with the wrong attribute names or wrong arguments fail (for example `TypeError` for a missing required argument), so the mock cannot drift from the real API
- [ ] D) It sends the call to the real gateway to compare results

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Calls with the wrong attribute names or wrong arguments fail (for example `TypeError` for a missing required argument), so the mock cannot drift from the real API

**Explanation:** A plain `Mock` accepts any attribute or call, so a typo like `mock.sned(...)` passes silently. Autospec checks names and signatures against the real class.
- **Why others are wrong:**
  - A) Speed is not the point; safety is.
  - B) Autospec does not add assertions; you still write them.
  - D) No real call is made; it only copies the real signatures.

</details>

---
## Part 2: True or False

### 37. True or False: By default, two different tests that request the same function-scoped fixture receive the very same object, so changes made in one test are visible in the other.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** By default a fixture runs once per test that requests it, and each test gets a fresh object. This isolation is a core principle of reliable tests.

</details>

---
### 38. True or False: Using `autouse=True` is a good way to create objects that tests need, because the tests then do not have to name them.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `autouse` is hidden magic. It suits resetting global state or logging, but objects a test needs should be explicit arguments so the test documents its own dependencies.

</details>

---
### 39. True or False: A fixture with `scope="module"` is created once and shared by all test files in the whole run.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Module scope is per `.py` file. Use `session` scope (ideally in `conftest.py`) to share across files.

</details>

---
### 40. True or False: A session-scoped fixture is created lazily: if no test requests it (and it is not `autouse`), it never runs.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Fixtures are created when first requested, not at the start of the run, unless they are `autouse`.

</details>

---
### 41. True or False: `@pytest.mark.parametrize("x", "abc")` generates three tests, one for each character.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Passing a string instead of a list iterates over its characters. Use `["abc"]` if you want one case with the whole string.

</details>

---
### 42. True or False: When two `parametrize` decorators are stacked, the value from the TOP decorator appears first in the generated test ID.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The bottom decorator's value appears first in the ID (for example `[10-1]` when `y` is the bottom decorator and `x` the top).

</details>

---
### 43. True or False: To use a fixture defined in `tests/conftest.py`, each test file must contain `from conftest import fixture_name`.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** PyTest loads conftest automatically and finds fixtures by name. Importing from conftest is fragile and unnecessary.

</details>

---
### 44. True or False: A child `conftest.py` can define a fixture with the same name as its parent's and request the parent's version as an argument to extend it.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** For example `def greeting(greeting): return greeting + " (unit-flavoured)"` wraps the parent's fixture rather than replacing it.

</details>

---
### 45. True or False: A fixture defined inside a test class (with `self`) can be requested by plain test functions outside that class.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A class-level fixture is only visible to the methods of that class. A function outside gets `fixture 'wallet' not found`.

</details>

---
### 46. True or False: When mixing raw and fixture-backed parametrized arguments, it is better to write `indirect=["name"]` than `indirect=True`.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `indirect=True` redirects all parametrized arguments through fixtures with matching names, which is rarely what you want when mixing; the explicit list is preferred.

</details>

---
### 47. True or False: `MagicMock` is a `Mock` that also supports Python's magic methods such as `__len__` and `__enter__`, so it can be used as a context manager.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `MagicMock` supports magic methods, and `patch` creates a `MagicMock` by default.

</details>

---
### 48. True or False: Writing `mock.send.assert_called_once` without parentheses verifies that `send` was called exactly once.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Without the parentheses the method is not called, so nothing is checked. Always include parentheses on assertion methods.

</details>

---
## Part 3: Code Prediction

### 49. A test fails with `assert False`. What is printed, and in what order, when you run `pytest -s`?

```python
import pytest

@pytest.fixture
def res():
    print("setup")
    yield 1
    print("teardown")

def test_a(res):
    print("test")
    assert False
```

- [ ] A) `setup`, `test` (teardown is skipped because the test failed)
- [ ] B) `test`, `setup`, `teardown`
- [ ] C) `setup`, `teardown`, `test`
- [ ] D) `setup`, `test`, `teardown`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `setup`, `test`, `teardown`

**Explanation:** The code before `yield` is setup, the test body runs at the `yield`, and the code after it is teardown, even when the test fails.
- **Why others are wrong:**
  - A) Teardown after `yield` runs whether the test passed or failed.
  - B) The fixture's setup runs before the test body.
  - C) Teardown runs after the test body, not before it.

</details>

---
### 50. Does this test pass?

```python
import pytest
from cart import ShoppingCart

@pytest.fixture
def cart():
    return ShoppingCart()

@pytest.fixture
def cart_with_pen(cart):
    cart.add("pen", 2.0)
    return cart

@pytest.fixture
def cart_with_pen_and_book(cart_with_pen):
    cart_with_pen.add("book", 10.0)
    return cart_with_pen

def test_chain(cart, cart_with_pen, cart_with_pen_and_book):
    assert cart is cart_with_pen_and_book
    assert cart.count() == 2
```

(`ShoppingCart` is the class from the lesson: `add` stores `(price, quantity)` per name and `count()` sums the quantities.)

- [ ] A) No, `cart is cart_with_pen_and_book` fails because each fixture builds a new cart
- [ ] B) Yes, it passes: all three names refer to the same `ShoppingCart` within one test
- [ ] C) No, it errors because a test cannot request three fixtures from one chain
- [ ] D) No, `cart.count()` is 3, not 2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Yes, it passes: all three names refer to the same `ShoppingCart` within one test

**Explanation:** The base `cart` fixture is only created once per test even if several fixtures request it (fixture caching within a test). Both items end up in that single cart.
- **Why others are wrong:**
  - A) Fixtures that depend on `cart` receive the same object; the base fixture is created once per test.
  - C) A test can request any number of fixtures.
  - D) Two items are added (`pen` and `book`, quantity 1 each), so the count is 2.

</details>

---
### 51. Run in this order (the default). What is the result?

```python
import pytest

@pytest.fixture(scope="module")
def shared_list():
    return []

def test_first(shared_list):
    shared_list.append("a")
    assert shared_list == ["a"]

def test_second(shared_list):
    shared_list.append("b")
    assert len(shared_list) == 1
```

- [ ] A) `1 failed, 1 passed`: `test_second` sees `['a', 'b']`
- [ ] B) `2 passed`, because each test gets a fresh list
- [ ] C) `2 failed`, because the fixture is mutable
- [ ] D) `1 error`, because a module fixture cannot return a list

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `1 failed, 1 passed`: `test_second` sees `['a', 'b']`

**Explanation:** A wide-scoped fixture returning a mutable object is shared, so the second test sees the first test's change. This is an order-dependent test.
- **Why others are wrong:**
  - B) A module-scoped fixture is shared by reference; the list persists across the tests.
  - C) `test_first` passes: the list is empty when it runs first.
  - D) Fixtures can return any object; the problem is shared mutable state, not an error.

</details>

---
### 52. What does PyTest report for this file?

```python
import pytest

@pytest.fixture
def per_test():
    return 1

@pytest.fixture(scope="session")
def long_lived(per_test):
    return per_test + 1

def test_x(long_lived):
    pass

def test_y():
    pass
```

- [ ] A) `2 passed`
- [ ] B) `2 errors`
- [ ] C) `1 passed, 1 error`: `test_x` errors with `ScopeMismatch`
- [ ] D) `1 failed, 1 passed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1 passed, 1 error`: `test_x` errors with `ScopeMismatch`

**Explanation:** A fixture can only request fixtures of the same or wider scope. Fix it by widening `per_test` or narrowing `long_lived`.
- **Why others are wrong:**
  - A) A session fixture cannot depend on a function-scoped one; PyTest raises `ScopeMismatch` for `test_x`.
  - B) `test_y` requests no fixtures, so it is unaffected and passes.
  - D) The problem occurs at fixture setup, so it is reported as an error, not a test failure.

</details>

---
### 53. Run with `pytest --collect-only -q`. What is the FIRST test ID listed (and how many tests are there)?

```python
import pytest

@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_mult(x, y):
    assert x * y == y * x
```

- [ ] A) `test_mult[1-10]`, with 6 tests in total
- [ ] B) `test_mult[10-1]`, with 6 tests in total
- [ ] C) `test_mult[10-1]`, with 5 tests in total
- [ ] D) `test_mult[1]`, with 3 tests in total

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `test_mult[10-1]`, with 6 tests in total

**Explanation:** Stacked decorators give a Cartesian product (3 x 2 = 6), and the bottom decorator's value appears first in the ID.
- **Why others are wrong:**
  - A) The bottom decorator's value (`y`) appears first in the ID.
  - C) The count is the product 3 x 2 = 6, not the sum.
  - D) Both decorators contribute to the ID and to the count.

</details>

---
### 54. What is the summary line when you run this file?

```python
import pytest

def is_adult(age):
    if age < 0:
        raise ValueError("negative")
    return age >= 18

@pytest.mark.parametrize("age, expected", [
    pytest.param(17, False, id="a"),
    pytest.param(18, True, id="b"),
    pytest.param(-1, False, id="c", marks=pytest.mark.xfail(raises=ValueError)),
    pytest.param(30, True, id="d", marks=pytest.mark.skip(reason="demo")),
    pytest.param(10, True, id="e"),
])
def test_it(age, expected):
    assert is_adult(age) is expected
```

- [ ] A) `4 passed, 1 skipped`
- [ ] B) `2 passed, 1 skipped, 2 xfailed`
- [ ] C) `1 failed, 3 passed, 1 xfailed`
- [ ] D) `1 failed, 2 passed, 1 skipped, 1 xfailed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1 failed, 2 passed, 1 skipped, 1 xfailed`

**Explanation:** `a` and `b` pass, `c` raises the expected `ValueError` (xfailed), `d` is skipped, and `e` fails because 10 is not an adult age.
- **Why others are wrong:**
  - A) Case `e` fails (`is_adult(10)` is `False`, expected `True`), and case `c` raises `ValueError` so it is `xfailed`, not passed.
  - B) Only case `c` carries `xfail`; case `e` is an ordinary failure.
  - C) Case `d` is skipped, not passed.

</details>

---
### 55. Three files; `pytest` is run from the project root. What is the result? (Layout: `tests/conftest.py`, `tests/unit/conftest.py`, `tests/unit/test_u.py`, `tests/api/test_a.py`.)

```python
# tests/conftest.py
import pytest

@pytest.fixture
def greeting():
    return "root"

# tests/unit/conftest.py
import pytest

@pytest.fixture
def greeting(greeting):
    return greeting + "+unit"

@pytest.fixture
def unit_only():
    return "u"

# tests/unit/test_u.py
def test_u(greeting):
    assert greeting == "root+unit"

# tests/api/test_a.py
def test_a(greeting):
    assert greeting == "root"

def test_b(unit_only):
    pass
```

- [ ] A) `2 passed, 1 error` (`test_b` cannot find `unit_only`)
- [ ] B) `3 passed`
- [ ] C) `1 passed, 2 failed`
- [ ] D) `1 passed, 2 errors`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `2 passed, 1 error` (`test_b` cannot find `unit_only`)

**Explanation:** The unit override wraps the root `greeting` (so `test_u` gets `"root+unit"`), the api test sees the root version, and sibling folders do not share conftest fixtures.
- **Why others are wrong:**
  - B) `tests/api` is a sibling of `tests/unit`, so it cannot see `unit_only`.
  - C) `test_u` and `test_a` both pass; the missing fixture is reported as an error.
  - D) `test_a` passes: it gets the root `greeting`, and the unit override does not affect it.

</details>

---
### 56. How many tests does PyTest generate and run for this file?

```python
import pytest

@pytest.fixture(params=["USD", "EUR"])
def currency(request):
    return request.param

@pytest.mark.parametrize("amount", [1, 100])
def test_format(currency, amount):
    assert currency and amount
```

- [ ] A) 2 tests, because the fixture and the decorator share the same values
- [ ] B) 3 tests, one per distinct value
- [ ] C) 4 tests (2 x 2), all passing
- [ ] D) 8 tests, because each is run twice

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 4 tests (2 x 2), all passing

**Explanation:** A parametrized fixture and a `parametrize` decorator multiply into a Cartesian product: 2 x 2 = 4 tests.
- **Why others are wrong:**
  - A) They are independent dimensions that multiply.
  - B) PyTest does not de-duplicate or add; it takes the product.
  - D) The product of 2 currencies and 2 amounts is 4.

</details>

---
### 57. What is the result?

```python
import pytest

@pytest.fixture
def number():
    return 1

@pytest.mark.parametrize("number", [10, 20])
def test_override(number):
    assert number in (10, 20)
```

- [ ] A) `1 passed`: the fixture is used and parametrize is ignored
- [ ] B) `2 failed`: `number` is `1` in both cases
- [ ] C) An error: a name cannot be both a fixture and a parameter
- [ ] D) `2 passed`: the parametrize values override the fixture, so the fixture value `1` is never used

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `2 passed`: the parametrize values override the fixture, so the fixture value `1` is never used

**Explanation:** Without `indirect`, parametrizing an argument that matches a fixture name overrides that fixture with the raw values for the test.
- **Why others are wrong:**
  - A) Parametrizing an argument that is also a fixture name overrides the fixture with the raw values.
  - B) The fixture's `1` is not used; the test receives 10 and 20.
  - C) It is legal (though confusing); prefer unique names.

</details>

---
### 58. What does this test print (the `-s` flag is used so output is shown)?

```python
from unittest.mock import Mock

def test_seq():
    m = Mock(side_effect=[1, ValueError("bad"), 3])
    out = []
    for _ in range(3):
        try:
            out.append(m())
        except ValueError:
            out.append("err")
    print(out)

    m2 = Mock(side_effect=[1, 2])
    m2()
    m2()
    try:
        m2()
    except StopIteration:
        print("stop")
```

- [ ] A) `[1, ValueError('bad'), 3]` then `stop`
- [ ] B) `[1, 'err', 3]` then `stop`
- [ ] C) `[1, 'err', 3]` then nothing; the third `m2()` returns `None`
- [ ] D) The test crashes at the second `m()` call

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[1, 'err', 3]` then `stop`

**Explanation:** An exception in a `side_effect` list is raised at that call, which the loop catches; and a call beyond the end of the list raises `StopIteration`.
- **Why others are wrong:**
  - A) An exception item in a `side_effect` iterable is raised at that call, not returned.
  - C) Once the iterable is exhausted the next call raises `StopIteration`.
  - D) The `ValueError` is raised at that call but caught by the `try/except` in the loop.

</details>

---
## Part 4: Fill-in-the-Blank

### 59. Fill in the blank: A fixture that returns a function, so that tests can create several different objects by calling it, is called a ________ fixture.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `factory`

**Explanation:** A factory fixture (for example `make_cart`) returns an inner function the test can call as many times as it needs.

</details>

---
### 60. Fill in the blank: A module-scoped fixture cannot use `tmp_path` (function scoped), so it uses the wider-scope sibling `tmp_path_factory` and calls `tmp_path_factory.________("data")` to create a temporary directory.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `mktemp`

**Explanation:** `tmp_path_factory.mktemp("data")` creates a new temp directory and returns a `Path`.

</details>

---
### 61. Fill in the blank: To give one parameter set a readable name, write `pytest.param(18, True, ________="boundary")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `id`

**Explanation:** `pytest.param` accepts `id` for the case name and `marks` for attaching `skip`, `xfail` or custom markers.

</details>

---
### 62. Fill in the blank: To add your own command-line option such as `--env`, define the hook `def pytest_________(parser):` in the top-level `conftest.py` and call `parser.addoption(...)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `addoption`

**Explanation:** `pytest_addoption(parser)` mimics `argparse`; if it is in a non-top-level conftest you get `unrecognized arguments`.

</details>

---
### 63. Fill in the blank: To load fixture modules such as `tests.fixtures.users` from the top-level `conftest.py`, assign a list of module names to the variable `________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `pytest_plugins`

**Explanation:** `pytest_plugins` is a list of importable module names; each is imported and its fixtures are registered as if defined in the conftest.

</details>

---
### 64. Fill in the blank: Inside a parametrized fixture, the current value is read with `request.________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `param`

**Explanation:** `request.param` holds the current value for this run, for both `params=` fixtures and `indirect` parametrization.

</details>

---
### 65. Fill in the blank: The golden rule of `patch` is to patch the name where it is ________ up, not where it is defined.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `looked`

**Explanation:** Patch the name in the namespace of the code under test; otherwise the module keeps its own reference to the real object.

</details>

---
### 66. Fill in the blank: To make a mock return `1`, then `2`, then `3` on successive calls, write `Mock(________=[1, 2, 3])`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `side_effect`

**Explanation:** `side_effect` with an iterable returns the next item on each call; a fourth call would raise `StopIteration`.

</details>

---
## Topic Coverage

| Topic (lesson) | Question numbers | Count |
|---|---|---|
| Fixtures (basics, yield, built-ins, autouse, factories) | 1, 2, 3, 4, 5, 6, 37, 38, 49, 50, 59 | 11 |
| Fixture scopes | 7, 8, 9, 10, 11, 39, 40, 51, 52, 60 | 10 |
| Parametrization | 12, 13, 14, 15, 16, 41, 42, 53, 54, 61 | 10 |
| conftest.py (hierarchy, hooks) | 17, 18, 19, 20, 21, 43, 44, 55, 62 | 9 |
| Sharing fixtures across tests | 22, 23, 24, 25, 26, 45, 63 | 7 |
| Combining fixtures and parametrization | 27, 28, 29, 30, 46, 56, 57, 64 | 8 |
| Mocking with unittest.mock | 31, 32, 33, 34, 35, 36, 47, 48, 58, 65, 66 | 11 |

**Total questions: 66** (Multiple Choice: 36, True/False: 12, Code Prediction: 10, Fill-in-the-Blank: 8)
