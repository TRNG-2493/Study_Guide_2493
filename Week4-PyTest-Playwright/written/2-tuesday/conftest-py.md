# conftest.py: Shared Configuration and Fixtures

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what `conftest.py` is, why PyTest treats it specially, and where it can be placed.
- Move fixtures from a test file into `conftest.py` so many test files can use them without imports.
- Describe how multiple `conftest.py` files in a directory tree interact (lookup and override rules).
- Use `conftest.py` for hooks such as `pytest_configure`, `pytest_addoption`, and `pytest_collection_modifyitems`.
- Register custom markers and command-line options from `conftest.py`.
- Avoid common pitfalls: importing from conftest, name clashes, and bloated conftest files.

## Why This Matters

The weekly epic: turn manual test design into a reporting **framework**. A framework is not a pile of test files; it is a structure in which setup, configuration, and helpers are defined once and shared. In PyTest, `conftest.py` is the backbone of that structure.

In **Project 1 (QE Foundations)** you will have several test files (validators, pricing, reports). All need the same sample data and temp folders. Without `conftest.py` you would copy fixtures to every file or write fragile imports. With it, you place the fixture in one file and every test below it can use it automatically.

Later this week, Playwright's PyTest plugin ships its own fixtures (such as `page`) and you will add your own in `conftest.py` to customise them. We will cover Playwright in depth on Thursday and Friday. Also on Wednesday we build a framework skeleton, which is built on today's `conftest.py` knowledge (we will cover this in depth on Wednesday).

Recap before we start: *Fixtures* (`@pytest.fixture`), *Fixture scopes*, *Parametrization*, and Monday's *Test discovery and organization* (naming rules, `pytest.ini`, markers).

## The Concept

### 1. What is conftest.py?

`conftest.py` is an ordinary Python file with a **special name** that PyTest looks for automatically while collecting tests. Anything you define in it is available to tests in the same directory and all subdirectories. Think of it as the "local settings and shared toolbox" file for a folder.

Key facts:

- The name must be exactly `conftest.py` (lowercase).
- PyTest **loads it automatically**; you never import it.
- It can contain **fixtures**, **hooks** (functions with names starting `pytest_`), and plain helper code.
- It is *not* a test file; PyTest does not collect tests from it (it does not match `test_*.py`).
- You can have **many** of them, one per directory if needed.

### 2. The problem it solves

Without conftest, two test files that need the same fixture look like this:

```python
# test_pricing.py
import pytest
from pricing import discounted_price

@pytest.fixture
def sample_prices():
    return [10, 20, 30]

def test_total(sample_prices):
    assert sum(sample_prices) == 60
```

```python
# test_reports.py
import pytest

@pytest.fixture
def sample_prices():           # duplicate!
    return [10, 20, 30]

def test_max(sample_prices):
    assert max(sample_prices) == 30
```

Duplication again. A tempting wrong fix is `from test_pricing import sample_prices` in the second file. That works for fixtures only through side effects, triggers lint warnings, and creates coupling between test files. `conftest.py` is the proper way.

### 3. Moving a fixture into conftest.py

Project layout:

```
project/
├── pytest.ini
├── src/
│   ├── pricing.py
│   └── report_utils.py
└── tests/
    ├── conftest.py
    ├── test_pricing.py
    └── test_reports.py
```

`tests/conftest.py`:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_prices():
    return [10, 20, 30]

@pytest.fixture(scope="session")
def app_config():
    print("\n[loading config once]")
    return {"env": "test", "currency": "USD"}
```

`tests/test_pricing.py`:

```python
def test_total(sample_prices):
    assert sum(sample_prices) == 60
```

`tests/test_reports.py`:

```python
def test_max(sample_prices, app_config):
    assert max(sample_prices) == 30
    assert app_config["env"] == "test"
```

**Explanation**

- No `import` of `sample_prices` appears anywhere. PyTest finds the fixture because it lives in `conftest.py` in the `tests` directory (the tests' directory or above).
- `app_config` is session scoped: "loading config once" prints once, even across two files. This is the *right* way to share a wide-scope fixture across files (recall: module scope is per file).
- `pytest.ini` at the project root typically contains `[pytest]` and `testpaths = tests`, and `pythonpath = src` so tests can `import pricing` (PyTest 7+ supports the `pythonpath` ini option).

An example `pytest.ini`:

```ini
[pytest]
testpaths = tests
pythonpath = src
addopts = -ra
markers =
    slow: tests that take longer to run
    smoke: quick sanity tests
```

### 4. Nested conftest files: hierarchy and override

You can place a `conftest.py` in subfolders:

```
tests/
├── conftest.py              # level 1
├── unit/
│   ├── conftest.py          # level 2
│   └── test_math.py
└── api/
    └── test_orders.py
```

Rules:

1. Tests see fixtures from **their own folder's `conftest.py` and every parent** up to the rootdir (the folder containing `pytest.ini`) .
2. If two levels define the **same fixture name**, the **closest** to the test wins (the child overrides the parent).
3. Sibling folders do **not** see each other's conftest: `api/` cannot use fixtures defined in `unit/conftest.py`.

Demonstration:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def greeting():
    return "hello from root"
```

```python
# tests/unit/conftest.py
import pytest

@pytest.fixture
def greeting():
    return "hello from unit"
```

```python
# tests/unit/test_greeting.py
def test_greeting_unit(greeting):
    assert greeting == "hello from unit"
```

```python
# tests/api/test_greeting_api.py
def test_greeting_api(greeting):
    assert greeting == "hello from root"
```

The unit test sees the nearer definition; the api test sees the root one.

An override can also **wrap the parent version** by requesting a fixture with the same name:

```python
# tests/unit/conftest.py
import pytest

@pytest.fixture
def greeting(greeting):          # requests the parent's greeting
    return greeting + " (unit-flavoured)"
```

Here the child `greeting` takes the parent `greeting` as input. This is a clean way to extend, not replace.

A test *file* can also override a conftest fixture: the module's own definition is nearer than any conftest.

### 5. Fixtures vs. plain helpers in conftest

Put **fixtures** in conftest, but avoid putting regular helper functions there and importing them (`from conftest import helper`). Importing from conftest is fragile because PyTest imports conftest in a special way, and different rootdir/`sys.path` settings can load it twice or fail. For reusable helpers, create a normal module, e.g. `tests/helpers.py` or `tests/utils/builders.py`, and import it. Better still, expose the helper **through a fixture** (a factory fixture) so tests need no imports at all.

```python
# tests/conftest.py
import pytest

@pytest.fixture
def make_user():
    def _make(name="Test", age=25):
        return {"name": name, "age": age}
    return _make
```

### 6. Hooks in conftest.py

A **hook** is a function with a reserved name that PyTest calls at a defined moment in its life cycle. Defining a hook in `conftest.py` customises PyTest's behaviour for that directory tree. You do not call hooks; PyTest does. Here are the beginner-friendly ones.

**6.1 `pytest_configure(config)`** runs once at startup. Perfect for registering markers programmatically:

```python
# tests/conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: quick sanity checks")
    config.addinivalue_line("markers", "regression: full regression tests")
```

This is an alternative to the `markers =` section in `pytest.ini`. Registered markers stop `PytestUnknownMarkWarning` and show in `pytest --markers`.

**6.2 `pytest_addoption(parser)`** adds your own command-line options:

```python
# tests/conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target environment: dev, staging or prod",
    )

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")
```

```python
# tests/test_env.py
def test_env_is_known(env):
    assert env in {"dev", "staging", "prod"}
```

Run `pytest --env staging`. **Explanation:** `parser.addoption` mimics Python's `argparse`. The `env` fixture reads the value from `request.config.getoption("--env")`. The `pytest_addoption` hook must be in a *top-level* conftest (at the rootdir or in the directory you invoke pytest from) so PyTest knows the option before parsing the command line. Also verify with `pytest --help`; your option appears under "custom options".

**6.3 `pytest_collection_modifyitems(config, items)`** lets you edit the list of collected tests, e.g. add markers or skip tests based on options:

```python
# tests/conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False,
                     help="run tests marked slow")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return                      # do not skip anything
    skip_slow = pytest.mark.skip(reason="need --runslow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```

**Explanation:** `items` is the list of test objects. `item.keywords` contains marker names. By default every `@pytest.mark.slow` test gets a skip marker; `pytest --runslow` runs them. This mirrors an official recipe in the PyTest documentation.

**6.4 `pytest_runtest_makereport`** (awareness only): used to attach results to reports, for example capturing a screenshot on failure. We will cover reporting in depth on Wednesday.

### 7. Autouse fixtures in conftest

An `autouse` fixture in a conftest applies to **all tests under that directory**:

```python
# tests/conftest.py
import pytest

@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
```

Every test now runs with `APP_ENV=test` and the variable is restored afterwards. This is a clean way to guarantee a consistent environment, but remember to use `autouse` sparingly.

### 8. `rootdir`, `conftest` discovery, and `__init__.py`

- PyTest finds conftest files by walking from each test's directory upwards.
- If your test folders have no `__init__.py`, test files must have **unique basenames** in the whole run (two `test_utils.py` files in different folders clash under the default "prepend" import mode). Adding `__init__.py` files or using unique names solves this.
- `conftest.py` in a folder **outside** your tests (for instance the project root) applies only if the tests are beneath it.
- `pytest --fixtures` lists fixtures, including ones from conftest files, with their file location. Add `-v` to see where each comes from. Use `pytest --fixtures-per-test` for a per-test view.

### 9. Typical contents of a good conftest.py

1. A few shared fixtures (config, sample data, factories).
2. Marker registrations.
3. A small number of hooks (options, collection tweaks).
4. A docstring at the top explaining the file.

Avoid: business logic, long helper functions, deep imports of application internals, and hundreds of lines. When it grows, split fixtures into modules and load them with `pytest_plugins` in the top-level conftest (covered in the next lesson, *Sharing fixtures across tests*).

## Code Examples: a Project 1 scenario

Complete small project:

```
project1/
├── pytest.ini
├── src/
│   └── textutils.py
└── tests/
    ├── conftest.py
    ├── test_slugify.py
    └── test_counts.py
```

`src/textutils.py`:

```python
import re

def slugify(text):
    """Convert 'Hello, World!' to 'hello-world'."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def word_count(text):
    return len(text.split())
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
pythonpath = src
markers =
    smoke: quick sanity checks
    slow: slower tests
```

`tests/conftest.py`:

```python
"""Shared fixtures for Project 1 utility tests."""
import pytest

@pytest.fixture(scope="session")
def sample_sentences():
    """Read-only sample data used by several test files."""
    return (
        "Hello, World!",
        "  PyTest   is FUN  ",
        "Already-a-slug",
    )

@pytest.fixture
def make_text():
    def _make(words, sep=" "):
        return sep.join(words)
    return _make
```

`tests/test_slugify.py`:

```python
import pytest
from textutils import slugify

@pytest.mark.smoke
def test_slugify_samples(sample_sentences):
    results = [slugify(s) for s in sample_sentences]
    assert results == ["hello-world", "pytest-is-fun", "already-a-slug"]
```

`tests/test_counts.py`:

```python
from textutils import word_count

def test_word_count(make_text):
    text = make_text(["alpha", "beta", "gamma"])
    assert word_count(text) == 3

def test_word_count_extra_spaces(sample_sentences):
    assert word_count(sample_sentences[1]) == 3
```

**Explanation**

- `sample_sentences` returns a **tuple** (immutable) at session scope: safe to share.
- Neither test file imports from `conftest`; both use fixtures by name.
- The `smoke` marker is registered in `pytest.ini`, so `pytest -m smoke` works without warnings.
- `pythonpath = src` lets tests `import textutils` without installing the package.
- Verify slugify manually: `"Hello, World!"` -> lower `"hello, world!"` -> regex replaces `", "` with `-` and `"!"` with `-` -> `"hello-world-"` -> `strip("-")` -> `"hello-world"`. And `"  PyTest   is FUN  "` becomes `"pytest-is-fun"`.

## Real-World Scenarios

1. **Company-wide base URL:** a `--base-url` option added in conftest, read by an `base_url` fixture; CI passes the environment.
2. **Per-layer setup:** `tests/api/conftest.py` creates an API client; `tests/ui/conftest.py` creates a browser page (we will cover Playwright on Thursday and Friday).
3. **Quarantine:** `pytest_collection_modifyitems` skips tests marked `flaky` unless a flag is passed.
4. **Test data bootstrap:** session fixture seeds a database once.
5. **Failure artefacts:** a hook captures logs or screenshots on failure (we will cover reporting on Wednesday).

## Common Mistakes

1. **Misnaming the file** (`conftest.PY`, `confest.py`, `conf_test.py`). It silently does nothing.
2. **Importing from conftest** (`from conftest import x`). Use fixtures.
3. **Adding `pytest_addoption` in a non-top-level conftest.** You get `unrecognized arguments`.
4. **Forgetting that sibling folders do not share conftest fixtures.**
5. **Placing conftest at the wrong level**: a fixture needed by `tests/api` and `tests/ui` must be in `tests/conftest.py`, not in one of them.
6. **Overriding a fixture unintentionally** by reusing a name in a nested conftest. Use `pytest --fixtures-per-test` to see which definition applies.
7. **Putting everything into one giant conftest.** It becomes unreadable; split and document.
8. **Using hooks with the wrong signature** (misspelling a parameter name). PyTest raises a validation error: parameter names must match the hook specification.
9. **Duplicate test file names without `__init__.py`**, causing "import file mismatch".

## Practice Exercises

**Exercise 1.** Create `tests/conftest.py` with a fixture `colors` returning `("red", "green", "blue")`. Write two test files, each with a test asserting `len(colors) == 3`. Run `pytest -v`. Confirm no imports are needed.

**Exercise 2.** Create `tests/sub/conftest.py` that overrides `colors` to return `("cyan", "magenta")`. Add `tests/sub/test_sub.py` asserting length 2. Confirm the other tests still pass.

**Exercise 3.** In the sub-conftest, change the override to wrap the parent: `def colors(colors): return colors + ("black",)` and assert length 4.

**Exercise 4.** Register markers `smoke` and `regression` using `pytest_configure`. Run `pytest --markers` to confirm they appear.

**Exercise 5.** Implement `--env` as in section 6.2 and a test that prints it. Run `pytest --env staging -s`.

*Hint:* add a default of `dev` so the plain `pytest` run works.

**Exercise 6.** Implement the `--runslow` recipe. Create one test marked `slow`. Run `pytest -rs` (skipped, with reason) and then `pytest --runslow`.

**Exercise 7 (Project 1 link).** Create a `tests/conftest.py` for your Project 1 repository, move at least two shared fixtures into it, register your markers, and delete the duplicated fixtures from the test files. Run the whole suite before and after to confirm the same number of passes.

## Summary

- `conftest.py` is auto-loaded by PyTest and holds fixtures, hooks, and configuration shared by a directory tree.
- You never import it; tests just request fixtures by name.
- Multiple conftest files form a hierarchy: closest definition wins; siblings do not share.
- A child fixture can extend a parent by requesting the same name.
- Useful hooks: `pytest_configure`, `pytest_addoption`, `pytest_collection_modifyitems`.
- Share helper functions via normal modules or factory fixtures rather than importing from conftest.
- Keep conftest focused and documented; split when it grows.
- Next: other ways of sharing fixtures across tests.

## Additional Resources

- Using `conftest.py` and fixture sharing: https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
- Writing hook functions and plugins: https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html
- Control skipping of tests according to command line option (recipe): https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option
