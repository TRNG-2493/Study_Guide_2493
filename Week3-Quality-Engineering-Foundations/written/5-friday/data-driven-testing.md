# Data-Driven Testing

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain the problem that data-driven testing (DDT) solves: copy-pasted tests that differ only in their values.
2. Define data-driven testing as the separation of test logic from test data, and use its core vocabulary correctly (test data, data set, data row, data source, parameterization, expected result column, data provider).
3. Describe the benefits and the risks of DDT, including data quality, debugging difficulty, large data volumes, over-engineering, and flaky data dependencies.
4. Show how Thursday's design techniques (boundary value analysis, equivalence partitioning, decision tables) produce the data that DDT executes.
5. Compare data-driven, keyword-driven, behavior-driven (BDD), and model-based testing at a name level.
6. Choose a suitable data source (inline list, CSV, JSON, YAML, Excel, database, API, generated data, environment-specific data) for a given situation.
7. Apply best practices for test data design: unique IDs, descriptive names, expected results stored with the data, data independence, clean-up, privacy, naming conventions, and version control.
8. Write data-driven tests in Python with pytest using `@pytest.mark.parametrize`, `ids`, `pytest.param` with marks, CSV and JSON files, fixtures with `params`, stacked parametrization, and seeded random data.
9. Read a pytest report and identify exactly which data row failed.
10. Build and run a CSV-driven test for the Project 1 registration feature.

---

## Why This Matters

Imagine you have just finished your test design for the Project 1 registration page. Using Thursday's techniques you have a list of 23 combinations of usernames and passwords: valid ones, too-short ones, too-long ones, ones with spaces, boundary values on both sides. Now you need to run them.

You could write 23 separate test functions. Each would be almost identical: call the registration check, compare the answer to what you expect. Then a developer changes the minimum password length from 8 to 10, and you have to open and edit a dozen of those functions by hand, hoping you do not miss one. A month later the product owner asks for six more cases. You copy, paste, and edit again. Before long, your test suite is a wall of near-identical code that nobody wants to touch.

Data-driven testing is the professional answer to this problem. You write the test steps once, and you keep the values in a separate table. Adding a test case becomes adding a row. Changing a rule becomes editing a few cells. A colleague who does not write Python can still contribute by adding rows to a spreadsheet.

This idea is everywhere in quality engineering. Manual testers use it when they write a test case with a table of input values. Test management tools such as Jira-based plugins use it in "examples" tables. Automation frameworks in later weeks (Selenium, Playwright, Postman, API testing frameworks) rely on it constantly. This is your first formal look at it, and the skill you build today, expressing test cases as data, will carry through the rest of the program and your career.

Today's exercise completes the Project 1 test-design document and the regression and risk plan. The data tables you design in this lesson become part of that document, and they feed directly into the regression work in the next lesson.

---

## The Concept

### 1. The problem: the copy-paste test suite

Let us start with a small function so everything stays concrete. A parcel delivery company calculates shipping cost from weight:

- Weight must be greater than 0 and at most 30 kg, otherwise the function raises an error.
- Up to and including 1 kg costs 5.00.
- Over 1 kg and up to and including 5 kg costs 8.00.
- Over 5 kg costs 15.00.
- Express delivery adds 10.00 to any of the above.

Here is the code under test. Every code block in this lesson was actually run, and the output shown is real output copied from a pytest session (Python 3.13, pytest 9.1.1).

```python
# src/shipping.py
def calculate_shipping(weight_kg, express=False):
    """Return the shipping cost in dollars for a parcel."""
    if weight_kg <= 0 or weight_kg > 30:
        raise ValueError("weight must be greater than 0 and at most 30 kg")
    if weight_kg <= 1:
        cost = 5.00
    elif weight_kg <= 5:
        cost = 8.00
    else:
        cost = 15.00
    if express:
        cost += 10.00
    return cost
```

Line by line:

- `def calculate_shipping(weight_kg, express=False):` defines a function with two inputs. `express=False` is a default value: if the caller does not say, we assume standard delivery.
- The triple-quoted line is a docstring, a short description of what the function does.
- `if weight_kg <= 0 or weight_kg > 30:` checks the invalid weights. `raise ValueError(...)` stops the function and signals an error with a message.
- The `if / elif / else` chain picks the base price from the weight band. `elif` means "else if".
- `if express: cost += 10.00` adds the express surcharge. `+=` means "add to the existing value".
- `return cost` hands the answer back to whoever called the function.

Now the first attempt at testing it, the way many beginners do it. This is the "before" picture:

```python
# tests/test_shipping_before.py
import pytest
from shipping import calculate_shipping


def test_shipping_half_kg_standard():
    assert calculate_shipping(0.5) == 5.00


def test_shipping_one_kg_standard():
    assert calculate_shipping(1) == 5.00


def test_shipping_just_over_one_kg_standard():
    assert calculate_shipping(1.01) == 8.00


def test_shipping_five_kg_standard():
    assert calculate_shipping(5) == 8.00


def test_shipping_just_over_five_kg_standard():
    assert calculate_shipping(5.01) == 15.00


def test_shipping_thirty_kg_standard():
    assert calculate_shipping(30) == 15.00


def test_shipping_half_kg_express():
    assert calculate_shipping(0.5, express=True) == 15.00


def test_shipping_zero_weight_rejected():
    with pytest.raises(ValueError):
        calculate_shipping(0)
```

What is each part doing?

- `import pytest` loads the pytest library so we can use `pytest.raises`.
- `from shipping import calculate_shipping` brings the function under test into this file.
- Each `def test_...():` is one test. pytest finds functions whose names start with `test_` and runs them automatically.
- `assert calculate_shipping(0.5) == 5.00` calls the function with 0.5 kg and checks that the result equals 5.00. If it does not, the test fails.
- `with pytest.raises(ValueError):` says "the code inside this block must raise a ValueError; if it does not, fail."

These tests work. But look at the pattern: eight functions, each with the same shape and a different value. Now count the pain:

- To add a case you copy a whole function, rename it, and edit two numbers.
- If the function signature changes (say `calculate_shipping` gains a required `destination` argument), you edit every single test.
- Names get long and inconsistent, and a reviewer must read all eight to see which weights are covered.
- The test data (the interesting part, since that is the test design) is buried in code.

This is the maintenance pain that data-driven testing removes. A helpful analogy: imagine writing 200 individual letters that all say "Dear ..., your appointment is on ..." and retyping the whole letter each time. Nobody does that. They write one letter template and use mail merge to fill in the names and dates from a list. Data-driven testing is mail merge for tests.

### 2. Definition: separate the logic from the data

**Data-driven testing (DDT)** is a test design and automation approach in which the **test logic** (the steps and checks) is written once and kept separate from the **test data** (the input values and expected results), and the same logic is run repeatedly against many rows of data.

Another analogy: one recipe, many ingredient lists. The recipe says "combine, heat, check the taste." The ingredient list says what goes in this time. A single recipe card serves a hundred different dishes if you change the list. In testing, the recipe is the test script and the ingredient list is the data table.

Here is the same idea as a picture in words:

```
        +----------------------+          +------------------------------+
        |  TEST LOGIC (once)   |          |  TEST DATA (many rows)       |
        |                      |  <-----  |  weight | express | expected |
        |  call the function   |          |  0.5    | no      | 5.00     |
        |  compare result with |          |  1.01   | no      | 8.00     |
        |  expected            |          |  5.01   | no      | 15.00    |
        +----------------------+          +------------------------------+
                    |
                    v
        One pass/fail result PER ROW in the report
```

The two halves can now change independently. Testers can improve the data without touching the logic, and engineers can change the logic without rewriting the data.

### 3. Vocabulary you must know

| Term | Plain-language meaning | Example from today |
|---|---|---|
| **Test data** | Any values a test uses: inputs, and the results you expect. | `weight_kg = 1.01` |
| **Data set / data row** | One complete group of values for one run of the test. A row in a table. | `SH-03, 1.01, false, 8.00` |
| **Data source** | Where the rows live: a list in code, a CSV or JSON file, a spreadsheet, a database, an API. | `data/shipping_rates.csv` |
| **Test script / test logic** | The steps and checks, written once. | `test_shipping_cost(...)` |
| **Parameterization** | Turning fixed values inside a test into named placeholders (parameters) that receive different values each run. | `weight, express, expected` |
| **Expected result column** | The column holding what the correct answer should be for that row. | `expected_cost` |
| **Data provider** | Any piece of code or tool that hands rows to the test. In pytest this is `parametrize` or a fixture with `params`. | `@pytest.fixture(params=...)` |
| **Test ID** | A unique label for each row so you can find it in reports. | `SH-03` |

A note on the word "parameter": in programming, a parameter is a named input slot of a function. In DDT, parameterization means the test function itself has parameters, and the framework calls it once per data row, filling the slots.

### 4. Benefits of data-driven testing

1. **Better coverage with little effort.** Adding a row costs seconds, so you are far more likely to include the awkward boundary and negative cases that Thursday's techniques produced.
2. **Maintainability.** The logic exists in one place. When the interface changes, you edit one function, not forty.
3. **Reusability.** One test can serve many scenarios, and the same data file can often be reused by tests at different levels (a unit test and later an API test).
4. **Fast addition of cases.** When a bug is found in production, adding a regression case is one new row.
5. **Contributions from non-programmers.** Business analysts, manual testers, and product owners can read and edit a CSV or spreadsheet. They know the rules even if they do not know Python.
6. **Clear visibility of coverage.** A table is easy to review: you can see at a glance which boundaries are tested and which are missing.

### 5. Drawbacks and risks

DDT is powerful, but it is not free. Know the risks so you can manage them.

1. **Data quality.** The test is only as good as its rows. A wrong expected value produces a false failure (the test says the product is broken when it is the data) or, worse, a false pass.
2. **Debugging is harder.** When 200 rows run through one function, you need good names and IDs to know which row failed and why. A vague report wastes time.
3. **Large data volumes.** Thousands of rows slow the suite down and make reviews impossible. More data is not automatically more coverage; many rows may test the same partition over and over.
4. **Over-engineering.** Building a sophisticated data framework for three test cases is wasteful. A plain test is sometimes the better choice.
5. **Flaky data dependencies.** If a row depends on something outside the file (a user that must already exist in a database, today's date, another row having run first), the test passes on one day and fails the next.
6. **Hidden coupling.** If the data file silently changes (someone edits a shared spreadsheet), tests change behavior with no code change to review. This is why data belongs under version control.

A good rule of thumb: use DDT when the same steps are repeated with different values and the number of cases is at least a handful. Do not use it to hide complex, different scenarios behind one cryptic function with a dozen flags.

### 6. Relationship to test design techniques

Here is the key insight to take away from this week: **test design techniques decide which data to use; data-driven testing is the machinery that runs that data.** They are partners, not alternatives.

On Thursday you learned boundary value analysis (BVA), equivalence partitioning (EP), and decision tables. Each produces a table of inputs and expected results. That table is exactly a DDT data set.

**Example A: an age field (BVA and EP).** Suppose registration accepts ages 18 to 65 inclusive. BVA says test just below, on, and just above each boundary. EP says add one typical value from the middle of the valid partition.

| Test ID | Technique | age | Expected |
|---|---|---|---|
| AGE-01 | BVA, below lower boundary | 17 | rejected |
| AGE-02 | BVA, lower boundary | 18 | accepted |
| AGE-03 | BVA, above lower boundary | 19 | accepted |
| AGE-04 | EP, typical valid value | 40 | accepted |
| AGE-05 | BVA, below upper boundary | 64 | accepted |
| AGE-06 | BVA, upper boundary | 65 | accepted |
| AGE-07 | BVA, above upper boundary | 66 | rejected |

Here is that exact table, run as a data-driven test:

```python
# src/age.py
def is_valid_age(age):
    """Registration accepts ages 18 to 65 inclusive."""
    return 18 <= age <= 65
```

```python
# tests/test_age_bva.py
import pytest
from age import is_valid_age


@pytest.mark.parametrize(
    "age, expected",
    [
        (17, False),   # just below lower boundary
        (18, True),    # lower boundary
        (19, True),    # just above lower boundary
        (40, True),    # typical value (equivalence partition)
        (64, True),    # just below upper boundary
        (65, True),    # upper boundary
        (66, False),   # just above upper boundary
    ],
)
def test_age_boundaries(age, expected):
    assert is_valid_age(age) == expected
```

Real output:

```
tests/test_age_bva.py::test_age_boundaries[17-False] PASSED
tests/test_age_bva.py::test_age_boundaries[18-True] PASSED
tests/test_age_bva.py::test_age_boundaries[19-True] PASSED
tests/test_age_bva.py::test_age_boundaries[40-True] PASSED
tests/test_age_bva.py::test_age_boundaries[64-True] PASSED
tests/test_age_bva.py::test_age_boundaries[65-True] PASSED
tests/test_age_bva.py::test_age_boundaries[66-False] PASSED
============================== 7 passed in 0.02s ==============================
```

(We explain `parametrize` line by line in the hands-on section below. For now, notice that the seven rows of the design table became seven test runs from one four-line function.)

**Example B: the login decision table.** Thursday's login decision table had conditions such as "username valid?" and "password valid?" with an outcome for each combination. Each column of a decision table (each rule) becomes one data row:

| Test ID | Username valid? | Password valid? | Expected outcome |
|---|---|---|---|
| LOG-01 | yes | yes | login succeeds |
| LOG-02 | yes | no | error: invalid credentials |
| LOG-03 | no | yes | error: invalid credentials |
| LOG-04 | no | no | error: invalid credentials |

The logic is the same four steps every time (open the login page, type the username, type the password, click the button and read the message), and the table feeds in the variation.

**Example C: error guessing.** Even the values you think of from experience (empty fields, a very long string, a name with an apostrophe) are just additional rows. A row costs almost nothing, which makes it easy to capture every idea.

### 7. Related approaches compared

You will meet several approaches whose names sound similar. They are not rivals; many real projects mix them. Here are name-level definitions with tiny examples.

| Approach | One-sentence definition | Tiny example | What varies | Typical strength |
|---|---|---|---|---|
| **Data-driven** | Same test steps run against many rows of data. | One login test, 20 username/password rows. | The data. | Many input variations with little code. |
| **Keyword-driven** | Tests are written as sequences of reusable action words ("keywords") kept in a table; code behind each keyword does the work. | Rows: `open_page`, `type username`, `click login`, `verify_text`. | The steps themselves, assembled from keywords. | Non-programmers can assemble new tests from existing keywords. |
| **Behavior-driven (BDD)** | Tests are written as plain-language scenarios (Given / When / Then) that the whole team can read, linked to code. | `Given a registered user, When they log in with a wrong password, Then an error is shown.` | Scenarios in business language. | Shared understanding between business, development, and testing. |
| **Model-based** | A model (for example a state machine) of the system is drawn, and tests are generated from the model automatically. | A state-transition diagram of the login lockout; a tool produces paths through it. | The model; tests are generated. | Systematic coverage of complex behavior. |

Some details worth noting:

- **Keyword-driven example (conceptual):**

  | Step | Keyword | Argument 1 | Argument 2 |
  |---|---|---|---|
  | 1 | open_page | /login | |
  | 2 | type_text | username | alice_01 |
  | 3 | type_text | password | Passw0rdOK |
  | 4 | click | login_button | |
  | 5 | verify_text | welcome_message | Welcome, alice_01 |

  Notice that this table describes steps, not just data. Data-driven testing varies values in fixed steps; keyword-driven testing varies the steps.

- **BDD** often includes its own examples tables ("Scenario Outline" with "Examples"), which is a data-driven idea inside a readable scenario. You will see this again in the Jira section below.

- **Model-based** fits the state transition technique from Thursday: if you model login attempts and lockout as states, a tool can walk the model and generate the test paths.

Remember: the approaches combine well. A BDD scenario outline with an examples table is data-driven. A keyword-driven framework can read its arguments from a data file. Data-driven testing is the simplest of these and the one you will use most often.

### 8. Data sources

Where can the rows live? Here is the menu, from simplest to most sophisticated.

| Source | What it is | Good for | Watch out for |
|---|---|---|---|
| **Inline lists / tuples** | Rows written directly in the test file as Python lists. | Small tables (under about 15 rows), unit tests, quick starts. | Non-programmers cannot easily edit; mixes data with code. |
| **CSV** | "Comma-separated values": a plain text table, one row per line. | Flat tables, easy to open in Excel, easy to diff in Git. | No data types (everything is text); commas inside values need quotes. |
| **JSON** | A text format with named fields, supports numbers, true/false, lists, nesting. | Structured data, API request bodies, nested data. | Syntax errors from a missing comma or quote; harder for non-programmers. |
| **YAML** | A human-friendly text format similar to JSON, using indentation. Needs the `pyyaml` package. | Configuration-like data, readable multi-line data. | Indentation mistakes; extra install. |
| **Excel (.xlsx)** | A spreadsheet. Python can read it with the `openpyxl` library (or `pandas`). | Business teams already maintaining test sheets. | Binary format, so Git cannot show line-by-line changes; hidden formulas or formatting surprises. |
| **Database** | Rows fetched with a query, for example with Python's `sqlite3` or a database driver. | Large or shared data, checking what the application stored. | Data changes over time; needs a known, controlled state. |
| **API** | Data fetched from a service at test time. | Dynamic data such as a list of valid product IDs. | Network dependency; the service can be down or change. |
| **Generated data** | Values produced by code: random numbers with a fixed seed, or fake realistic names and emails with the `Faker` library. | Unique values (new email per run), volume, privacy-safe realistic data. | Randomness can make failures hard to reproduce unless seeded. |
| **Environment-specific data** | Different data per environment (dev, test, staging), chosen with a setting. | Different base URLs, test accounts, and IDs that exist only in one environment. | Hard-coded values that silently point at the wrong environment. |

You will practice inline lists, CSV, JSON, fixtures, and generated data in this lesson. Here are short, name-level illustrations of the remaining sources. These snippets are illustrative and were not part of the executed lab, because they need extra packages that you will install in later weeks.

```python
# YAML (needs: pip install pyyaml) -- illustrative only
import yaml

with open("data/login_cases.yaml", encoding="utf-8") as f:
    cases = yaml.safe_load(f)      # becomes a normal Python list of dictionaries
```

```python
# Excel (needs: pip install openpyxl) -- illustrative only
from openpyxl import load_workbook

workbook = load_workbook("data/login_cases.xlsx")
sheet = workbook.active
for row in sheet.iter_rows(min_row=2, values_only=True):   # min_row=2 skips the header row
    test_id, username, password, expected = row
```

```python
# Generated data with Faker (needs: pip install faker) -- illustrative only
from faker import Faker

fake = Faker()
Faker.seed(1234)                    # fixed seed: the same fake values every run
print(fake.user_name(), fake.email())
```

For databases, you would use something like `sqlite3.connect("test.db")` and run a `SELECT` query to fetch rows. For APIs, you would use a library such as `requests` to fetch data. Both are covered when we reach API and database testing.

**Environment-specific data** deserves a sentence of explanation. Your application may run on a developer's machine, a shared test server, and a staging server. The URL differs, and so may the test accounts. Rather than hard-code these, keep one data file per environment (for example `data/env_test.json` and `data/env_staging.json`) and choose which to load by an environment variable or command-line option.

### 9. Best practices for test data design

1. **Give every row a unique test ID.** `REG-001`, `SH-03`. The ID lets you refer to a row in a defect report, in a Jira ticket, and in a pytest filter.
2. **Use descriptive names and descriptions.** A row called `case7` tells you nothing. A row described as "password one below minimum (7)" tells you what it checks and why.
3. **Store the expected result with the data.** Every row carries its own expected outcome, so the test logic can stay generic.
4. **Derive expected results from the requirement, never from the code.** (See Common Mistakes below; this is the most important rule.)
5. **Keep data independent.** No row should depend on another row having run first. Tests must pass in any order and individually.
6. **Clean up and reset.** If a row creates something (a user account, an order), the test must remove it or use a unique value each time, so the next run starts from a known state.
7. **Protect privacy and sensitive data.** Never use real personal data (real names, emails, phone numbers, card numbers, passwords) in test data files. Use synthetic data (made-up values that look realistic) or masked data (real data with identifying parts scrambled). Test data files often end up in Git and in shared reports, so treat them as public.
8. **Follow naming conventions.** Consistent column names (`test_id`, `username`, `expected_result`), consistent file names (`registration.csv`, `shipping_rates.csv`), and consistent value formats (`true` / `false`, not a mix of `yes`, `Y`, and `1`).
9. **Keep data under version control (Git).** Treat data files like code: commit them, review changes, and write meaningful commit messages. CSV and JSON are line-based text, so Git shows exactly which row changed.
10. **Include a `test_id` column.** Yes, it is also rule one; it is so useful that it deserves repeating. It links your data to the test design document, the defect log, and the pytest report.
11. **Keep rows small and focused.** One row, one purpose. If a row fails, you should know immediately what was being tested.
12. **Document the columns.** A short note or header comment explaining each column and allowed values saves time for newcomers.

### 10. Hands-on: data-driven testing in Python with pytest

We now build the idea in code, step by step, using real files that I ran in a scratch folder. The project layout we use is explained in a later section. Install pytest if you do not have it:

```
pip install pytest
```

(On some managed Linux systems you may need `pip install --break-system-packages pytest`; inside a virtual environment the plain command works.)

The tiny configuration file `pytest.ini` below tells pytest where to look so imports work:

```ini
[pytest]
pythonpath = src utils
testpaths = tests
```

- `[pytest]` is the section name pytest looks for.
- `pythonpath = src utils` adds the `src` and `utils` folders to Python's import search path so `from shipping import ...` works.
- `testpaths = tests` tells pytest to look for tests in the `tests` folder by default.

#### Step 1: the "before" (copy-paste tests)

You saw this earlier: eight near-identical functions. Running it:

```
tests/test_shipping_before.py::test_shipping_half_kg_standard PASSED
tests/test_shipping_before.py::test_shipping_one_kg_standard PASSED
tests/test_shipping_before.py::test_shipping_just_over_one_kg_standard PASSED
tests/test_shipping_before.py::test_shipping_five_kg_standard PASSED
tests/test_shipping_before.py::test_shipping_just_over_five_kg_standard PASSED
tests/test_shipping_before.py::test_shipping_thirty_kg_standard PASSED
tests/test_shipping_before.py::test_shipping_half_kg_express PASSED
tests/test_shipping_before.py::test_shipping_zero_weight_rejected PASSED
```

It works, but about 24 lines of code carry only seven small facts.

#### Step 2: refactor to a loop

The first improvement is to pull the values into one list and loop over them:

```python
# tests/test_shipping_loop.py
from shipping import calculate_shipping


def test_shipping_with_a_loop():
    rows = [
        (0.5, False, 5.00),
        (1, False, 5.00),
        (1.01, False, 8.00),
        (5, False, 8.00),
        (5.01, False, 15.00),
        (30, False, 15.00),
        (0.5, True, 15.00),
    ]
    for weight, express, expected in rows:
        assert calculate_shipping(weight, express) == expected
```

Line by line:

- `rows = [ ... ]` is a list of tuples. A tuple is a fixed group of values in parentheses. Each tuple is one data row: weight, express flag, expected cost.
- `for weight, express, expected in rows:` repeats the indented line once per row, and "unpacks" each tuple into three named variables.
- `assert calculate_shipping(weight, express) == expected` is the single, shared check.

This is already data-driven in spirit: logic once, data in a table. But the loop has real weaknesses. Let us see them by deliberately breaking one row (we changed the expected value for 1.01 kg to 9.00, which is wrong):

```python
# tests/test_shipping_loop_bad.py
from shipping import calculate_shipping


def test_shipping_with_a_loop_bad():
    rows = [
        (0.5, False, 5.00),
        (1.01, False, 9.00),   # deliberately wrong expected value
        (5.01, False, 15.00),
    ]
    for weight, express, expected in rows:
        assert calculate_shipping(weight, express) == expected
```

Real output:

```
tests/test_shipping_loop_bad.py::test_shipping_with_a_loop_bad FAILED    [100%]

=================================== FAILURES ===================================
________________________ test_shipping_with_a_loop_bad _________________________

    def test_shipping_with_a_loop_bad():
        rows = [
            (0.5, False, 5.00),
            (1.01, False, 9.00),   # deliberately wrong expected value
            (5.01, False, 15.00),
        ]
        for weight, express, expected in rows:
>           assert calculate_shipping(weight, express) == expected
E           assert 8.0 == 9.0
E            +  where 8.0 = calculate_shipping(1.01, False)

tests/test_shipping_loop_bad.py:11: AssertionError
```

Three problems with a plain loop:

1. **One test, one result.** The report says one test failed. You do not see which of the rows passed, and there is no per-row line.
2. **The loop stops at the first failure.** Row three (5.01 kg) was never run, so you do not know if it would have passed. Hidden failures stay hidden until you fix the first one.
3. **No row names.** You have to read the traceback to deduce which row failed.

We need a tool that treats each row as its own test. That tool is parameterization.

#### Step 3: `@pytest.mark.parametrize` with ids

```python
# tests/test_shipping_parametrize.py
import pytest
from shipping import calculate_shipping


@pytest.mark.parametrize(
    "weight, express, expected",
    [
        (0.5, False, 5.00),
        (1, False, 5.00),
        (1.01, False, 8.00),
        (5, False, 8.00),
        (5.01, False, 15.00),
        (30, False, 15.00),
        (0.5, True, 15.00),
    ],
    ids=[
        "light-standard",
        "boundary-1kg-standard",
        "just-over-1kg-standard",
        "boundary-5kg-standard",
        "just-over-5kg-standard",
        "boundary-30kg-standard",
        "light-express",
    ],
)
def test_shipping_cost(weight, express, expected):
    assert calculate_shipping(weight, express) == expected


@pytest.mark.parametrize("bad_weight", [0, -1, 30.01], ids=["zero", "negative", "over-max"])
def test_shipping_rejects_bad_weight(bad_weight):
    with pytest.raises(ValueError):
        calculate_shipping(bad_weight)
```

Line by line:

- `@pytest.mark.parametrize(...)` is a **decorator**: a line starting with `@` placed above a function that changes how that function behaves. This one tells pytest "run the function below once per data row."
- The first argument, `"weight, express, expected"`, is a string naming the parameters. These names must match the parameters of the test function exactly.
- The second argument is the list of rows. Each tuple supplies values in the same order as the names.
- `ids=[...]` gives each row a human-readable label. Without `ids`, pytest invents labels from the values such as `0.5-False-5.0`, which is hard to read. With `ids`, the report names the purpose of each row. The list must have the same number of entries as the rows.
- `def test_shipping_cost(weight, express, expected):` is the test logic. It has no loop and no hard-coded values; pytest fills in the three parameters each time.
- The second test shows a single parameter (`"bad_weight"`) and a list of single values. Because the expected result is always the same here (a `ValueError`), no expected-result column is needed. Not every DDT test needs one.

Real output:

```
tests/test_shipping_parametrize.py::test_shipping_cost[light-standard] PASSED
tests/test_shipping_parametrize.py::test_shipping_cost[boundary-1kg-standard] PASSED
tests/test_shipping_parametrize.py::test_shipping_cost[just-over-1kg-standard] PASSED
tests/test_shipping_parametrize.py::test_shipping_cost[boundary-5kg-standard] PASSED
tests/test_shipping_parametrize.py::test_shipping_cost[just-over-5kg-standard] PASSED
tests/test_shipping_parametrize.py::test_shipping_cost[boundary-30kg-standard] PASSED
tests/test_shipping_parametrize.py::test_shipping_cost[light-express] PASSED
tests/test_shipping_parametrize.py::test_shipping_rejects_bad_weight[zero] PASSED
tests/test_shipping_parametrize.py::test_shipping_rejects_bad_weight[negative] PASSED
tests/test_shipping_parametrize.py::test_shipping_rejects_bad_weight[over-max] PASSED
```

Each row is now a separate test with its own name in square brackets, and all rows run even if one fails. Ten test results come from two functions.

#### Step 4: `pytest.param` with marks (xfail and skip)

Sometimes a row needs special treatment. Maybe a known bug makes it fail and you do not want it to turn the whole run red until the bug is fixed. Maybe a feature is not built yet. `pytest.param` wraps a single row so you can attach an id and marks to it individually.

```python
# tests/test_shipping_marks.py
import pytest
from shipping import calculate_shipping


@pytest.mark.parametrize(
    "weight, express, expected",
    [
        pytest.param(0.5, False, 5.00, id="light-standard"),
        pytest.param(5.01, False, 15.00, id="just-over-5kg"),
        pytest.param(
            12, False, 12.00,
            id="mid-weight-rate-change",
            marks=pytest.mark.xfail(reason="BUG-101: spec says 12.00 for 5-15kg, code returns 15.00"),
        ),
        pytest.param(
            2, True, 18.00,
            id="express-international",
            marks=pytest.mark.skip(reason="International express not built yet"),
        ),
    ],
)
def test_shipping_with_marks(weight, express, expected):
    assert calculate_shipping(weight, express) == expected
```

Line by line:

- `pytest.param(0.5, False, 5.00, id="light-standard")` is one row, with its id attached right next to its values. This keeps the name and the data together, so they cannot drift out of sync the way a separate `ids=[...]` list can.
- `marks=pytest.mark.xfail(reason=...)` means "expected failure." pytest runs the row; if it fails, it reports `XFAIL` (expected) rather than a failure. If it unexpectedly passes, pytest reports `XPASS`, which is a signal that the bug was fixed and the mark should be removed. Always put a defect ID in the reason.
- `marks=pytest.mark.skip(reason=...)` means "do not run this row at all." Use it for features that do not exist yet.

Real output (with `-rxs`, which prints a short reason summary for xfail and skip):

```
tests/test_shipping_marks.py::test_shipping_with_marks[just-over-5kg] PASSED [ 50%]
tests/test_shipping_marks.py::test_shipping_with_marks[mid-weight-rate-change] XFAIL [ 75%]
tests/test_shipping_marks.py::test_shipping_with_marks[express-international] SKIPPED [100%]

=========================== short test summary info ============================
XFAIL tests/test_shipping_marks.py::test_shipping_with_marks[mid-weight-rate-change] - BUG-101: spec says 12.00 for 5-15kg, code returns 15.00
SKIPPED [1] tests/test_shipping_marks.py:5: International express not built yet
=================== 2 passed, 1 skipped, 1 xfailed in 0.03s ====================
```

In a team, that XFAIL line is documentation: "We know about this defect, it is tracked as BUG-101, and the data row will turn into XPASS the day it is fixed."

#### Step 5: reading data from a CSV file

Now we move the data out of the Python file altogether. First a small reusable helper in the `utils` folder:

```python
# utils/data_loader.py
import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv_rows(filename):
    """Read a CSV file from the data folder and return a list of dict rows."""
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_json(filename):
    """Read a JSON file from the data folder and return the parsed data."""
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)
```

Line by line:

- `import csv` and `import json` load Python's built-in modules for reading those formats. `from pathlib import Path` loads a tool for working with file paths.
- `DATA_DIR = Path(__file__).resolve().parent.parent / "data"` computes the location of the `data` folder relative to this file: `__file__` is this file's own path, `.parent` goes up one folder (to `utils`), the second `.parent` goes up again (to the project root), and `/ "data"` adds the folder name. Doing it this way means the tests work no matter which folder you run pytest from.
- `def load_csv_rows(filename):` defines a helper that takes a file name.
- `open(..., newline="", encoding="utf-8")` opens the file for reading. `newline=""` is what the `csv` module's documentation recommends so line endings and quoted newlines are handled correctly. `encoding="utf-8"` makes sure non-English characters read properly. `with ... as f:` closes the file automatically afterwards.
- `csv.DictReader(f)` reads the first line as column headers and turns every later line into a dictionary such as `{"test_id": "SH-01", "weight_kg": "0.5", ...}`. `list(...)` collects all the rows into a list.
- `load_json` does the same job for JSON: `json.load(f)` parses the file into Python lists, dictionaries, numbers, and booleans.

The data file:

```
test_id,weight_kg,express,expected_cost,description
SH-01,0.5,false,5.00,light parcel standard
SH-02,1,false,5.00,boundary at 1 kg
SH-03,1.01,false,8.00,just over 1 kg
SH-04,5,false,8.00,boundary at 5 kg
SH-05,5.01,false,15.00,just over 5 kg
SH-06,30,false,15.00,maximum weight
SH-07,0.5,true,15.00,light parcel express
```

And the test that consumes it:

```python
# tests/test_shipping_csv.py
import pytest
from data_loader import load_csv_rows
from shipping import calculate_shipping

ROWS = load_csv_rows("shipping_rates.csv")


@pytest.mark.parametrize("row", ROWS, ids=[f"{r['test_id']}-{r['description']}" for r in ROWS])
def test_shipping_from_csv(row):
    weight = float(row["weight_kg"])
    express = row["express"].lower() == "true"
    expected = float(row["expected_cost"])
    assert calculate_shipping(weight, express) == expected
```

Line by line:

- `ROWS = load_csv_rows("shipping_rates.csv")` runs once when pytest imports the file and stores the list of row dictionaries. Constants are written in capital letters by convention.
- `@pytest.mark.parametrize("row", ROWS, ids=[...])` uses a single parameter called `row`, and each data row (a dictionary) becomes its value. The `ids` list is built with a **list comprehension**: `[ ... for r in ROWS]` builds a new list by doing the expression for every item. `f"{r['test_id']}-{r['description']}"` is an f-string that builds a label such as `SH-03-just over 1 kg`.
- `float(row["weight_kg"])` converts text to a decimal number. **This conversion is essential.** CSV stores everything as text, so `"0.5"` is a string until you convert it. Forgetting this is the number one beginner mistake with CSV data.
- `row["express"].lower() == "true"` turns the text `"false"` / `"true"` into a real `False` / `True`. A common trap is writing `bool(row["express"])`; any non-empty string, including `"false"`, is truthy in Python, so that would give `True` for everything.
- The `assert` line is the shared check.

Real output:

```
tests/test_shipping_csv.py::test_shipping_from_csv[SH-01-light parcel standard] PASSED
tests/test_shipping_csv.py::test_shipping_from_csv[SH-02-boundary at 1 kg] PASSED
tests/test_shipping_csv.py::test_shipping_from_csv[SH-03-just over 1 kg] PASSED
tests/test_shipping_csv.py::test_shipping_from_csv[SH-04-boundary at 5 kg] PASSED
tests/test_shipping_csv.py::test_shipping_from_csv[SH-05-just over 5 kg] PASSED
tests/test_shipping_csv.py::test_shipping_from_csv[SH-06-maximum weight] PASSED
tests/test_shipping_csv.py::test_shipping_from_csv[SH-07-light parcel express] PASSED
```

Now a business analyst can add `SH-08` by typing one line in a spreadsheet and saving as CSV. No Python edit is needed.

#### Step 6: a JSON data file

JSON keeps the data types, so we do not need conversions:

```json
[
  {"test_id": "SH-01", "weight_kg": 0.5,  "express": false, "expected_cost": 5.00,  "description": "light parcel standard"},
  {"test_id": "SH-02", "weight_kg": 1,    "express": false, "expected_cost": 5.00,  "description": "boundary at 1 kg"},
  {"test_id": "SH-03", "weight_kg": 1.01, "express": false, "expected_cost": 8.00,  "description": "just over 1 kg"},
  {"test_id": "SH-04", "weight_kg": 5,    "express": false, "expected_cost": 8.00,  "description": "boundary at 5 kg"},
  {"test_id": "SH-05", "weight_kg": 5.01, "express": false, "expected_cost": 15.00, "description": "just over 5 kg"},
  {"test_id": "SH-06", "weight_kg": 30,   "express": false, "expected_cost": 15.00, "description": "maximum weight"},
  {"test_id": "SH-07", "weight_kg": 0.5,  "express": true,  "expected_cost": 15.00, "description": "light parcel express"}
]
```

```python
# tests/test_shipping_json.py
import pytest
from data_loader import load_json
from shipping import calculate_shipping

CASES = load_json("shipping_rates.json")


@pytest.mark.parametrize("case", CASES, ids=[c["test_id"] for c in CASES])
def test_shipping_from_json(case):
    actual = calculate_shipping(case["weight_kg"], case["express"])
    assert actual == case["expected_cost"], case["description"]
```

Line by line:

- `CASES = load_json(...)` returns a list of dictionaries, with numbers already numbers and `true`/`false` already booleans.
- `ids=[c["test_id"] for c in CASES]` uses the test ID alone as the label.
- `assert actual == case["expected_cost"], case["description"]`: the text after the comma is the **assertion message**. If the assert fails, pytest prints it, so the failure explains itself.

Real output:

```
tests/test_shipping_json.py::test_shipping_from_json[SH-01] PASSED
tests/test_shipping_json.py::test_shipping_from_json[SH-02] PASSED
tests/test_shipping_json.py::test_shipping_from_json[SH-03] PASSED
tests/test_shipping_json.py::test_shipping_from_json[SH-04] PASSED
tests/test_shipping_json.py::test_shipping_from_json[SH-05] PASSED
tests/test_shipping_json.py::test_shipping_from_json[SH-06] PASSED
tests/test_shipping_json.py::test_shipping_from_json[SH-07] PASSED
```

**CSV or JSON?** CSV is friendlier for flat tables and for people who live in spreadsheets. JSON is better when values have types or when rows have nested structure (for example an API request body with an address object inside). Choose the simplest format your audience can maintain.

#### Step 7: data providers via fixtures with `params`

A **fixture** is a reusable piece of setup that pytest hands to tests that ask for it by name. A fixture can also act as a data provider. The big advantage over `parametrize`: several test functions can share the same set of rows without repeating the list.

```python
# tests/test_fixture_provider.py
import pytest
from shipping import calculate_shipping

WEIGHT_CASES = [
    {"id": "light", "weight": 0.5, "expected": 5.00},
    {"id": "medium", "weight": 3, "expected": 8.00},
    {"id": "heavy", "weight": 20, "expected": 15.00},
]


@pytest.fixture(params=WEIGHT_CASES, ids=lambda case: case["id"])
def weight_case(request):
    """Data provider: hands one weight case to each test that asks for it."""
    return request.param


def test_standard_cost(weight_case):
    assert calculate_shipping(weight_case["weight"]) == weight_case["expected"]


def test_express_adds_ten(weight_case):
    standard = calculate_shipping(weight_case["weight"])
    express = calculate_shipping(weight_case["weight"], express=True)
    assert express == standard + 10.00
```

Line by line:

- `WEIGHT_CASES` is a list of dictionaries; each is one data set.
- `@pytest.fixture(params=WEIGHT_CASES, ids=lambda case: case["id"])` declares a fixture that runs once per entry in `params`. The `ids` argument here is a small function (a **lambda**, written `lambda case: ...`) that pytest calls on each entry to get its label.
- `def weight_case(request):` the special argument `request` is provided by pytest. `request.param` is the current entry.
- `return request.param` hands the current case to whichever test asked for it.
- Both `test_standard_cost` and `test_express_adds_ten` simply list `weight_case` as a parameter. pytest runs each of them three times, once per case.
- `test_express_adds_ten` also shows a useful style: instead of a stored expected value, it checks a **relationship** (express = standard + 10). This works well when the rule is a clear relationship, and it avoids copying the code's own arithmetic.

Real output:

```
tests/test_fixture_provider.py::test_standard_cost[light] PASSED
tests/test_fixture_provider.py::test_standard_cost[medium] PASSED
tests/test_fixture_provider.py::test_standard_cost[heavy] PASSED
tests/test_fixture_provider.py::test_express_adds_ten[light] PASSED
tests/test_fixture_provider.py::test_express_adds_ten[medium] PASSED
tests/test_fixture_provider.py::test_express_adds_ten[heavy] PASSED
```

Two functions times three rows gives six tests. Use `parametrize` when the data belongs to one test; use a fixture with `params` when several tests share the same data.

#### Step 8: stacking decorators for combinations (and the explosion warning)

You can stack several `parametrize` decorators on one test. pytest then runs every **combination** (the Cartesian product) of the values:

```python
# tests/test_stacking.py
import pytest
from shipping import calculate_shipping


@pytest.mark.parametrize("express", [False, True], ids=["standard", "express"])
@pytest.mark.parametrize("weight", [0.5, 1, 3, 5, 20, 30], ids=lambda w: f"{w}kg")
def test_cost_is_positive_for_every_combination(weight, express):
    assert calculate_shipping(weight, express) > 0
```

- Two decorators: one with 2 values, one with 6 values. The test count is 2 x 6 = **12**.
- `ids=lambda w: f"{w}kg"` builds labels like `3kg`.
- The check here is deliberately general ("cost is positive") because with combinations you cannot easily list an exact expected value per pair.

Real output:

```
tests/test_stacking.py::test_cost_is_positive_for_every_combination[0.5kg-standard] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[0.5kg-express] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[1kg-standard] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[1kg-express] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[3kg-standard] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[3kg-express] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[5kg-standard] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[5kg-express] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[20kg-standard] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[20kg-express] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[30kg-standard] PASSED
tests/test_stacking.py::test_cost_is_positive_for_every_combination[30kg-express] PASSED
```

**The explosion warning.** Counts multiply, they do not add. I tested this with a deliberately silly example: 4 browsers, 3 operating systems, 5 languages, and 3 user roles, each as its own stacked decorator. The multiplication is 4 x 3 x 5 x 3 = **180 tests**, and pytest confirmed it:

```
180 passed in 0.14s
```

Four short lists produced 180 tests. Add one more list of five items and you have 900. With a real browser taking several seconds per test, that is the difference between a one-minute run and an hour-long one. Stacking is the right tool for a small, well-chosen combination (a few values on two or three dimensions). For larger spaces, do not run every combination. Use pairwise (all-pairs) selection or risk-based selection, the techniques for choosing a smaller set that still covers the interesting interactions; you may meet these in more advanced courses. For now, always **count before you stack**.

#### Step 9: reporting, and a failing row clearly identified

The point of `ids` really shines when something fails. We use the Project 1 registration data (shown in full in the next section) and add one deliberately wrong row to a copy of the CSV:

```
REG-024,pat,Passw0rd9,password_contains_username,password should contain username
```

This row claims that the password `Passw0rd9` for user `pat` should be rejected because it contains the username. It does not (the letters p-a-t do not appear in the password), so the code correctly accepts it, and the row's expected value is wrong. Real output:

```
tests/test_registration_bad.py::test_registration_from_csv[REG-024] FAILED

=================================== FAILURES ===================================
_____________________ test_registration_from_csv[REG-024] ______________________
row = {'test_id': 'REG-024', 'username': 'pat', 'password': 'Passw0rd9', 'expected_result': 'password_contains_username', ...}

    @pytest.mark.parametrize("row", ROWS, ids=[r["test_id"] for r in ROWS])
    def test_registration_from_csv(row):
        result = validate_registration(row["username"], row["password"])
>       assert result == row["expected_result"], row["description"]
E       AssertionError: password should contain username
E       assert 'success' == 'password_contains_username'
E
E         - password_contains_username
E         + success

tests/test_registration_bad.py:11: AssertionError
=========================== short test summary info ============================
FAILED tests/test_registration_bad.py::test_registration_from_csv[REG-024] - ...
========================= 1 failed, 23 passed in 0.05s =========================
```

How to read this report:

1. **The summary line** says `1 failed, 23 passed`. The 23 good rows were not affected by the bad one. That is the benefit of one test per row.
2. **The header `test_registration_from_csv[REG-024]`** names the exact row. Open the CSV and search for `REG-024`.
3. **The `row = {...}` line** shows the full data of that row, so you do not even need to open the file.
4. **The `E` lines** show the assertion message (our row description) and the comparison: the function returned `'success'` but the row expected `'password_contains_username'`.

Now the important thinking step: **is the code wrong or the data wrong?** Go back to the requirement. The rule says the password must not contain the username. "pat" is not inside "Passw0rd9", so `success` is correct and the data row was wrong. The fix is in the data:

```
REG-024,pat,Passw0rd9,success,username not contained in password
```

(Had the requirement said the opposite, we would have logged a defect against the code instead.) You can also run just the rows you care about with `-k`:

```
python -m pytest tests/test_registration_csv.py -k "REG-018 or REG-019" -v
```

```
tests/test_registration_csv.py::test_registration_from_csv[REG-018] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-019] PASSED
======================= 2 passed, 21 deselected in 0.02s =======================
```

`-k` selects tests whose names match an expression, and because our ids are the test IDs, selecting a row is easy. Other handy options: `-v` (verbose, one line per test), `-q` (quiet), `--collect-only -q` (list the tests without running them, useful for counting), and `-x` (stop at first failure).

#### Step 10: simple data generation

Sometimes you need many values, or values that must be unique, and typing them is pointless. Python's `random` module can generate values. The key trick is a **seed**: a starting number that makes the "random" sequence repeat exactly. A seeded generator gives you varied data and reproducible failures.

```python
# tests/test_random_seeded.py
import random
import pytest
from shipping import calculate_shipping

rng = random.Random(42)  # fixed seed: same values on every run
RANDOM_WEIGHTS = [round(rng.uniform(0.01, 30), 2) for _ in range(5)]


@pytest.mark.parametrize("weight", RANDOM_WEIGHTS, ids=lambda w: f"w{w}")
def test_generated_weight_in_valid_range_has_valid_cost(weight):
    assert calculate_shipping(weight) in (5.00, 8.00, 15.00)
```

- `random.Random(42)` creates a random number generator with seed 42. Using your own generator object (instead of the global one) keeps this test's values independent of anything else.
- `rng.uniform(0.01, 30)` picks a decimal number between 0.01 and 30. `round(..., 2)` keeps two decimals. The list comprehension builds five of them. The underscore `_` is a conventional name for a loop variable we do not use.
- `ids=lambda w: f"w{w}"` labels each row by its value, so a failure tells you the exact weight.
- The assertion checks a **property** (the result must be one of the three legal prices), because we have no individual expected values for random inputs.

Real output (the same five weights appear every run because of the seed):

```
tests/test_random_seeded.py::test_generated_weight_in_valid_range_has_valid_cost[w19.19] PASSED
tests/test_random_seeded.py::test_generated_weight_in_valid_range_has_valid_cost[w0.76] PASSED
tests/test_random_seeded.py::test_generated_weight_in_valid_range_has_valid_cost[w8.26] PASSED
tests/test_random_seeded.py::test_generated_weight_in_valid_range_has_valid_cost[w6.7] PASSED
tests/test_random_seeded.py::test_generated_weight_in_valid_range_has_valid_cost[w22.1] PASSED
```

Random data is a supplement, not a replacement, for designed data. It cannot tell you the correct expected value, and it will almost never hit an exact boundary by chance. The Faker library (shown at name level earlier) generates realistic fake names, emails, addresses, and phone numbers, and supports seeding too. Both are excellent for privacy-safe volume data, for example creating a unique email for every registration test so that "email already exists" never interferes.

---

### 11. Data-driven API and UI testing (conceptual)

You have not installed any browser or API tools yet; those come in later weeks. The pattern, however, is identical to what you just did.

- **UI testing with Selenium or Playwright.** The test script opens the login page, types a username, types a password, clicks Login, and reads the message. Only the username, password, and expected message change. You would put these in a CSV or JSON file and feed them through `parametrize`, exactly as above. The cost per row is much higher (a real browser takes seconds), so keep UI data tables small and put the exhaustive combinations at the faster unit or API level.
- **API testing with Postman or Python.** In Postman, a "collection runner" can take a CSV or JSON file and run the same request once per row, using the columns as variables in the request. In Python, you would use the same `parametrize` pattern to send each row as a request and check the status code and response body.

Test levels and data size follow a simple principle: the lower the level, the faster the test, and the more rows you can afford. Put the many-row tables where the tests are cheap.

### 12. A project structure suggestion

A tidy layout keeps the three concerns (tests, data, helpers) apart:

```
project1-qe-foundations/
|-- pytest.ini                 <- pytest settings (paths, options)
|-- src/                       <- code under test (or a link to the real app)
|   |-- shipping.py
|   |-- registration.py
|   `-- age.py
|-- tests/                     <- test logic only
|   |-- test_shipping_parametrize.py
|   |-- test_shipping_csv.py
|   |-- test_registration_csv.py
|   `-- test_age_bva.py
|-- data/                      <- test data only, versioned in Git
|   |-- registration.csv
|   |-- shipping_rates.csv
|   |-- shipping_rates.json
|   `-- discount_rules.csv
`-- utils/                     <- helpers shared by tests
    `-- data_loader.py
```

Rules of thumb: tests contain logic and no big data tables; `data/` contains no logic; `utils/` contains small, well-named helpers that every test can reuse. Later weeks will add folders such as `pages/` (page objects) and `config/` (environment settings).

---

## Examples

### Project 1: registration data-driven test

Here is the function under test: a simple `validate_registration(username, password)` for the Project 1 registration page. It returns a result code string.

The rules (the "requirements" we test against):

| Field | Rule | Result code if violated |
|---|---|---|
| Username | Required | `username_required` |
| Username | At least 3 characters | `username_too_short` |
| Username | At most 15 characters | `username_too_long` |
| Username | Letters, digits, underscore only | `username_invalid_chars` |
| Password | Required | `password_required` |
| Password | At least 8 characters | `password_too_short` |
| Password | At most 20 characters | `password_too_long` |
| Password | No spaces | `password_has_space` |
| Password | At least one uppercase letter | `password_no_uppercase` |
| Password | At least one digit | `password_no_digit` |
| Password | Must not contain the username (ignoring case) | `password_contains_username` |
| Both valid | | `success` |

If more than one rule is broken, the function reports the first violation in the order shown (username rules before password rules).

```python
# src/registration.py
import re


def validate_registration(username, password):
    """Check a registration attempt and return a result code."""
    if username == "":
        return "username_required"
    if len(username) < 3:
        return "username_too_short"
    if len(username) > 15:
        return "username_too_long"
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return "username_invalid_chars"
    if password == "":
        return "password_required"
    if len(password) < 8:
        return "password_too_short"
    if len(password) > 20:
        return "password_too_long"
    if " " in password:
        return "password_has_space"
    if not any(c.isupper() for c in password):
        return "password_no_uppercase"
    if not any(c.isdigit() for c in password):
        return "password_no_digit"
    if username.lower() in password.lower():
        return "password_contains_username"
    return "success"
```

Explanations:

- `import re` loads the regular expression module (a mini-language for matching text patterns).
- Each `if ...: return "..."` is a **guard**: the first rule violated ends the function with its code. The order of the guards is the order of precedence.
- `re.fullmatch(r"[A-Za-z0-9_]+", username)` checks that the **whole** username consists only of letters, digits, and underscores (`[A-Za-z0-9_]`), one or more times (`+`). The `r"..."` prefix makes it a raw string so backslashes are left alone. `not` flips the result, so a failing match returns the invalid-characters code.
- `any(c.isupper() for c in password)` is true if at least one character is an uppercase letter. `c.isdigit()` does the same for digits.
- `username.lower() in password.lower()` compares in lowercase so "MIA" inside "xxMIAxx9Q" is found.

The test data, designed with Thursday's techniques. It has 23 rows: seven valid and sixteen invalid rows, with the boundaries covered on both sides. Boundaries are tested on both sides (username lengths 2, 3, 15, 16; password lengths 7, 8, 20, 21), and error guessing contributes the symbol, space, and digits-only rows. Save this as `data/registration.csv`:

```
test_id,username,password,expected_result,description
REG-001,alice_01,Passw0rdOK,success,valid typical user
REG-002,bob,Secret123,success,username at minimum length 3
REG-003,abcdefghijklmno,Secret123,success,username at maximum length 15
REG-004,carol,Abcdefg1,success,password at minimum length 8
REG-005,dave,Abcdefghijklmnopqrs1,success,password at maximum length 20
REG-006,ev_e_9,Valid1234,success,underscore and digit in username
REG-007,,Secret123,username_required,empty username
REG-008,ab,Secret123,username_too_short,username one below minimum (2)
REG-009,abcdefghijklmnop,Secret123,username_too_long,username one above maximum (16)
REG-010,bad name,Secret123,username_invalid_chars,space in username
REG-011,john@doe,Secret123,username_invalid_chars,symbol in username
REG-012,frank,,password_required,empty password
REG-013,grace,Abcdef1,password_too_short,password one below minimum (7)
REG-014,heidi,Abcdefghijklmnopqrst1,password_too_long,password one above maximum (21)
REG-015,ivan,Pass word1,password_has_space,space inside password
REG-016,judy,password1,password_no_uppercase,no uppercase letter
REG-017,karl,Passwordd,password_no_digit,no digit
REG-018,liam,Liam12345,password_contains_username,password contains username
REG-019,mia,xxMIAxx9Q,password_contains_username,username inside password ignoring case
REG-020,nina,12345678,password_no_uppercase,digits only password
REG-021,oscar,ABCDEFGH,password_no_digit,uppercase only password
REG-022,x,y,username_too_short,both fields invalid - username reported first
REG-023,pam_p,Z9z9Z9z9,success,mixed case with digits
```

Notes on the data:

- Every value here is synthetic. The usernames are made-up first names, and the passwords are invented patterns, not real credentials. No real person's data appears.
- REG-007 and REG-012 contain **empty** values. In CSV an empty field is simply two commas next to each other (`REG-007,,Secret123,...`). DictReader reads it as an empty string `""`, which is exactly what the function's `== ""` check expects.
- REG-010 has a space inside the username. CSV handles this fine, since only commas, quotes, and line breaks are special. (If a value itself contained a comma, you would wrap it in double quotes.)
- REG-022 documents the precedence rule: with two broken fields, the username error is reported first.
- The rows cover three kinds of cases (valid, invalid, boundary) in one place, with a description for each.

The test:

```python
# tests/test_registration_csv.py
import pytest
from data_loader import load_csv_rows
from registration import validate_registration

ROWS = load_csv_rows("registration.csv")


@pytest.mark.parametrize("row", ROWS, ids=[r["test_id"] for r in ROWS])
def test_registration_from_csv(row):
    result = validate_registration(row["username"], row["password"])
    assert result == row["expected_result"], row["description"]
```

- `ROWS = load_csv_rows("registration.csv")` reads all 23 rows at import time.
- The `ids` list uses the `test_id` column, so the report shows `REG-001` through `REG-023`.
- The test calls the function with the username and password cells (already strings, so no conversion is needed here) and compares the returned code to the `expected_result` cell. The `description` becomes the assertion message.

Real output:

```
tests/test_registration_csv.py::test_registration_from_csv[REG-001] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-002] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-003] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-004] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-005] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-006] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-007] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-008] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-009] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-010] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-011] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-012] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-013] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-014] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-015] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-016] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-017] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-018] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-019] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-020] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-021] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-022] PASSED
tests/test_registration_csv.py::test_registration_from_csv[REG-023] PASSED
```

Twenty-three tests, three lines of test logic. The table is also the design document: it can be pasted into the Project 1 test-design document as it stands.

#### Mapping the techniques onto the data

| Technique from Thursday | Rows it produced |
|---|---|
| Boundary value analysis (username length) | REG-002 (3), REG-003 (15), REG-008 (2), REG-009 (16) |
| Boundary value analysis (password length) | REG-004 (8), REG-005 (20), REG-013 (7), REG-014 (21) |
| Equivalence partitioning (valid, empty, wrong characters) | REG-001, REG-006, REG-007, REG-010, REG-012 |
| Decision table (rule precedence, both fields wrong) | REG-022 |
| Error guessing (symbols, spaces, digits-only, uppercase-only, case-insensitive match) | REG-011, REG-015, REG-019, REG-020, REG-021 |

### Data-driven testing in manual test case design

DDT is not only for automation. A manual test case can have one set of steps and a data table:

**Test case TC-REG-01: Register with various credentials**

| Step | Action | Expected |
|---|---|---|
| 1 | Open the registration page | Registration form is displayed |
| 2 | Enter the **username** and **password** from the data table below | Values appear in the fields (password masked) |
| 3 | Click **Register** | The **expected result** from the data table is shown |

Data table:

| Data ID | Username | Password | Expected result |
|---|---|---|---|
| D1 | alice_01 | Passw0rdOK | Account created; welcome message shown |
| D2 | ab | Secret123 | Error: username too short |
| D3 | grace | Abcdef1 | Error: password too short |
| D4 | john@doe | Secret123 | Error: invalid characters in username |

The tester executes the three steps once per data row and records pass or fail per row. This keeps the test case short and the coverage visible. Many teams keep such data in an **Excel test sheet**: one tab per test case or feature, columns for Test ID, input values, expected result, actual result, status, and defect ID. When automation arrives, the same sheet can be exported to CSV and become the data source for the automated test, a smooth path from manual to automated.

### Data-driven testing in Jira and test management

Most test management approaches inside or alongside Jira support the same idea in different words:

- **Scenario Outline with Examples (BDD style).** A single scenario with placeholders, followed by an examples table:

  ```
  Scenario Outline: Registration validation
    Given I am on the registration page
    When I register with username "<username>" and password "<password>"
    Then I see the result "<expected_result>"

    Examples:
      | username | password   | expected_result    |
      | alice_01 | Passw0rdOK | success            |
      | ab       | Secret123  | username_too_short |
      | grace    | Abcdef1    | password_too_short |
  ```

  Each row of the Examples table is run as its own test. This is the same pattern as `parametrize`, written in readable business language.

- **Test case with a data table in the test management tool.** Many tools let you attach a table of data sets to a single test case, or repeat a test case with a "dataset" or "parameter" feature.
- **Defect linking.** Because every row has a test ID, a defect can say "Failed for REG-014" and point straight to the data row. The xfail reason in our earlier example (`BUG-101`) does the reverse: it links the row back to the defect.
- **Traceability.** A `test_id` column or a requirement-ID column (for example `REQ-REG-03`) links a row to a requirement, which supports the traceability you learned on Tuesday.

The exact menu names differ among tools, so check the documentation of the tool your team uses. The concept stays the same.

### How DDT supports regression testing

Regression testing means re-running existing tests after a change to make sure nothing that used to work is now broken. It is the topic of the next lesson, but the connection is worth previewing:

- A data-driven suite is **cheap to rerun**: one command executes every row.
- Every defect becomes a **new row**. Once a bug is fixed, its row stays in the data file forever as a guard against the bug returning.
- The data table is a **readable inventory** of what is being protected, which helps when you select a risk-based subset for regression.
- Test IDs and tags make it easy to select a **smaller regression pack** (for example the boundary rows only) when time is short.

Keep this in mind for the regression and risk plan you complete today and expand in the next lesson.

### Common mistakes

1. **Hard-coding expected results derived from the code under test.** If you run the function, see that it returns 8.0, and paste `8.0` into the data as "expected," you have not tested anything. You have recorded what the code does, bugs included. Expected results must come from the requirement, the specification, or the business rule, ideally worked out before running the code.
2. **Hidden data dependencies.** A row expects a user `alice_01` to already exist in the database, or expects today's date to be a weekday. The test is green on your machine and red on a colleague's. Make dependencies explicit and create your own data (or use unique generated values).
3. **Huge datasets run on every commit.** Ten thousand rows on every code change slows the team and gets the suite ignored. Keep a small, high-value set for every commit and run the big set on a schedule (for example nightly).
4. **Vague row names.** `test1`, `case_a`, `row 7`. When it fails, nobody knows what it was checking. Use IDs plus descriptions, and meaningful pytest `ids`.
5. **Forgetting type conversion.** CSV values are text. `"1.01" == 1.01` is false in Python. Convert with `float()`, `int()`, and explicit boolean handling.
6. **Mismatched ids and rows.** A separate `ids=[...]` list that is shorter or longer than the rows causes an error, and one in the wrong order silently mislabels results. Building ids from the data (as we did) avoids this.
7. **Duplicate rows.** Ten rows that all test the same partition give a false sense of coverage. Each row should earn its place by testing something distinct.
8. **Real personal data.** Copying a production export into a test file leaks real people's information into Git. Always use synthetic or properly masked data.
9. **Mixing too much into one test.** If different rows need different steps, they belong in different tests. One data-driven test should do one job.
10. **Not checking the data file itself.** A stray blank line, a missing column, or a misspelled header such as `expected_reslt` causes confusing errors. Review data changes like code.

---

## Try it: Project 1 activity

You will now apply data-driven testing to Project 1 and move the work forward for today's deliverable.

**Part A: run the registration data (about 20 minutes).**

1. Create the folder layout shown in the directory tree (`src/`, `tests/`, `data/`, `utils/`) and a `pytest.ini`.
2. Save `registration.py`, `data_loader.py`, `registration.csv`, and `test_registration_csv.py` exactly as shown. Run `python -m pytest -v`. All 23 rows should pass.
3. Run `python -m pytest --collect-only -q` and confirm that 23 tests are listed.

**Part B: extend the data (about 25 minutes).**

4. Add at least four new rows with IDs `REG-024` onward. Ideas: a username with a hyphen, a password of exactly 20 characters containing a space, a username that is only digits, a password with a leading space. Work out the expected result from the rules table before you run anything.
5. Run again. If a row fails, apply the "code or data?" check from Step 9: go back to the rules table and decide whether your expected value or the function is wrong. Record any genuine defect in your defect log using the row ID.

**Part C: login data table (about 20 minutes).**

6. Using Thursday's login decision table, build `data/login.csv` with columns `test_id, username, password, expected_result, description`, with at least eight rows (valid login, wrong password, unknown user, empty fields, and so on). You do not have a login function yet, so write the expected results from the requirements. Add this table to the Project 1 test-design document.

**Part D: connect to the regression and risk plan (about 15 minutes).**

7. In your regression and risk plan, mark which rows are "must run every commit" (for example the boundary rows REG-002, REG-003, REG-004, REG-005, REG-008, REG-009, REG-013, REG-014) and which are "nightly only." Give a one-sentence risk reason for each group.

Deliverables: the CSV files, the passing pytest output, and the updated sections in your test-design document.

---

## Practice Exercises

Try each exercise yourself before you read the answer key.

### Exercise 1: parametrize a shipping calculator

Write a pytest file that tests `calculate_shipping` for these rows using one parametrized test, with a readable `id` for each row. Include express rows.

| weight_kg | express | expected |
|---|---|---|
| 0.1 | False | 5.00 |
| 1 | True | 15.00 |
| 5 | True | 18.00 |
| 5.01 | True | 25.00 |
| 30 | True | 25.00 |

### Exercise 2: build a CSV for a discount rule table

Business rule: an order total under 50 gets no discount; 50 up to (but not including) 100 gets 5 percent; 100 or more gets 10 percent. Members get an extra 2 percent on top. A negative total is invalid. Here is the function:

```python
# src/discount.py
def discount_percent(total, is_member):
    """Return the discount percentage for an order total."""
    if total < 0:
        raise ValueError("total cannot be negative")
    if total < 50:
        percent = 0
    elif total < 100:
        percent = 5
    else:
        percent = 10
    if is_member:
        percent += 2
    return percent
```

Design a CSV `data/discount_rules.csv` with columns `test_id,total,is_member,expected_percent,description`, using boundary value analysis, with at least 8 rows. Then write the test that reads it.

### Exercise 3: convert duplicated tests

Convert these three duplicated tests into one parametrized test:

```python
from age import is_valid_age

def test_age_17():
    assert is_valid_age(17) == False

def test_age_18():
    assert is_valid_age(18) == True

def test_age_66():
    assert is_valid_age(66) == False
```

### Exercise 4: add ids

The test below produces ids like `test_pw[Abcdef1-password_too_short]`. Rewrite it so each row has a meaningful id using `pytest.param`, and explain why this helps.

```python
@pytest.mark.parametrize("password, expected", [
    ("Abcdef1", "password_too_short"),
    ("Abcdefg1", "success"),
])
def test_pw(password, expected):
    assert validate_registration("zed", password) == expected
```

### Exercise 5: find the bad data row

This is a copy of the discount CSV with one row edited. The function is correct according to the rules above. Run the test mentally (or really) and find the bad row. Decide whether the code or the data is wrong, and give the fixed row.

```
test_id,total,is_member,expected_percent,description
DS-01,0,false,0,zero total
DS-02,49.99,false,0,just below 50
DS-03,50,false,5,boundary at 50
DS-04,99.99,false,5,just below 100
DS-05,100,false,10,boundary at 100
DS-06,49.99,true,2,member bonus only
DS-07,99.99,true,5,member in middle band
DS-08,100,true,12,member in top band
```

### Exercise 6 (stretch): count the combinations

A test is decorated with three stacked `parametrize` decorators with 4, 5, and 6 values. How many tests does pytest generate? Suggest one way to reduce the number without losing the important cases.

---

### Answer keys

**Answer 1**

```python
# tests/test_shipping_exercise.py
import pytest
from shipping import calculate_shipping


@pytest.mark.parametrize(
    "weight, express, expected",
    [
        pytest.param(0.1, False, 5.00, id="very-light-standard"),
        pytest.param(1, True, 15.00, id="boundary-1kg-express"),
        pytest.param(5, True, 18.00, id="boundary-5kg-express"),
        pytest.param(5.01, True, 25.00, id="just-over-5kg-express"),
        pytest.param(30, True, 25.00, id="max-weight-express"),
    ],
)
def test_shipping_rows(weight, express, expected):
    assert calculate_shipping(weight, express) == expected
```

Why these expected values: 1 kg is in the first band (5.00) plus 10.00 express gives 15.00. 5 kg is in the middle band (8.00) plus 10.00 gives 18.00. 5.01 and 30 kg are in the top band (15.00) plus 10.00 gives 25.00. Check yourself that you derived these from the rules, not by running the code. Using `pytest.param(..., id=...)` keeps each name next to its data.

**Answer 2**

```
test_id,total,is_member,expected_percent,description
DS-01,0,false,0,zero total
DS-02,49.99,false,0,just below 50
DS-03,50,false,5,boundary at 50
DS-04,99.99,false,5,just below 100
DS-05,100,false,10,boundary at 100
DS-06,49.99,true,2,member bonus only
DS-07,99.99,true,7,member in middle band
DS-08,100,true,12,member in top band
```

```python
# tests/test_discount_csv.py
import pytest
from data_loader import load_csv_rows
from discount import discount_percent

ROWS = load_csv_rows("discount_rules.csv")


@pytest.mark.parametrize("row", ROWS, ids=[r["test_id"] for r in ROWS])
def test_discount_from_csv(row):
    total = float(row["total"])
    is_member = row["is_member"].lower() == "true"
    assert discount_percent(total, is_member) == int(row["expected_percent"])
```

I ran this file; the result was `8 passed`. Each member row is the non-member value plus 2: 0+2 = 2, 5+2 = 7, 10+2 = 12. Note the conversions: `float` for the total, a text comparison for the boolean, `int` for the percentage. The negative-total case is best tested separately with `pytest.raises(ValueError)`, because it expects an exception rather than a number; adding a `-0.01` row to this table would break the "number" shape of the expected column. (Bonus: a separate small parametrized test `[-0.01, -100]` for the error case is the cleanest design.)

**Answer 3**

```python
import pytest
from age import is_valid_age


@pytest.mark.parametrize(
    "age, expected",
    [(17, False), (18, True), (66, False)],
    ids=["below-min", "min-boundary", "above-max"],
)
def test_age(age, expected):
    assert is_valid_age(age) == expected
```

Three functions became one, with named rows. Adding the missing boundaries (19, 64, 65) is now three more tuples.

**Answer 4**

```python
@pytest.mark.parametrize("password, expected", [
    pytest.param("Abcdef1", "password_too_short", id="boundary-7-chars"),
    pytest.param("Abcdefg1", "success", id="boundary-8-chars"),
])
def test_pw(password, expected):
    assert validate_registration("zed", password) == expected
```

(I ran both versions; each gives two passing tests.) The new ids say what each row is for. In a long report, `test_pw[boundary-7-chars]` tells you immediately that a minimum-length boundary failed; the default id forces you to decode the password string.

**Answer 5**

The bad row is **DS-07**. The row says a member with a 99.99 total gets 5 percent. By the rules, 99.99 is in the 50-to-under-100 band (5 percent), and members get an extra 2 percent, so the expected value is 7. The function returns 7, so the **data** is wrong, not the code. When I ran this file, pytest reported:

```
E       AssertionError: assert 7 == 5
E        +  where 7 = discount_percent(99.99, True)
E        +  and   5 = int('5')
FAILED tests/test_discount_bad.py::test_discount_from_csv[DS-07] - AssertionE...
1 failed, 7 passed in 0.02s
```

Fixed row: `DS-07,99.99,true,7,member in middle band`. The thinking process matters: you compared the failing row with the requirement, not with the code.

**Answer 6**

4 x 5 x 6 = **120** tests. To reduce: keep full combinations only for the dimensions that truly interact, test the other dimensions one at a time against a default (4 + 5 + 6 minus overlaps is far fewer), or use pairwise selection so every pair of values appears together at least once, which typically needs a small fraction of the full 120.

---

## Knowledge Check

Answer these without looking back, then check your answers below.

1. In one sentence, what is data-driven testing?
2. What is the difference between a data set (row) and a data source?
3. Name three benefits and three risks of DDT.
4. Which of Thursday's techniques produces the data that DDT executes? Give two examples.
5. Why is a plain `for` loop over test rows a weaker design than `@pytest.mark.parametrize`? Give two reasons.
6. What is the purpose of the `ids` argument, and what does `-k` allow you to do with it?
7. What does `marks=pytest.mark.xfail(reason="BUG-101: ...")` do, and what does `XPASS` signal?
8. In a CSV-driven test, why must you convert values with `float()` and handle `"false"` carefully?
9. Four stacked parametrize decorators have 3, 4, 5, and 2 values. How many tests run?
10. Name three data-independence or privacy rules for test data.
11. What is the difference between data-driven and keyword-driven testing?
12. A teammate fills the `expected_result` column by running the code and copying the output. What is wrong with that?
13. When would a fixture with `params` be a better choice than `parametrize`?
14. Why do we seed random data generators?

### Answers

1. DDT is an approach where the test logic is written once and kept separate from test data, and the same logic runs against many rows of data.
2. A data set (row) is one complete group of values for one test run; a data source is the place that holds all the rows, such as a CSV file, JSON file, spreadsheet, or database.
3. Benefits: better coverage, easier maintenance, reusability, fast addition of cases, non-programmer contributions. Risks: poor data quality, harder debugging, large data volumes, over-engineering, flaky data dependencies (any three of each).
4. Boundary value analysis, equivalence partitioning, decision tables (also error guessing). Examples: the age table (17, 18, 19, 40, 64, 65, 66) from BVA and EP; the login decision table's four rules, each becoming a row.
5. A loop is one test with one result, so you cannot see which rows passed; and it stops at the first failed assertion, so later rows never run. It also gives no per-row name in the report.
6. `ids` gives each row a readable name in the report. Because the id is part of the test name, `-k "REG-018"` runs only that row (or `-k "REG-018 or REG-019"` for several).
7. It runs the row and reports `XFAIL` if it fails as expected, so a known defect does not turn the run red. `XPASS` means the row passed unexpectedly, signalling that the bug may be fixed and the mark can be removed.
8. CSV stores everything as text, so `"1.01"` is not equal to `1.01`. And any non-empty string, including `"false"`, is truthy in Python, so `bool("false")` is `True`; compare the text to `"true"` instead.
9. 3 x 4 x 5 x 2 = 40 tests.
10. Any three of: never use real personal data; use synthetic or masked data; keep rows independent of each other; clean up or use unique values so reruns start from a known state; do not store real passwords or card numbers; keep data in Git but never commit secrets.
11. Data-driven varies the values while the steps stay the same; keyword-driven builds tests from reusable action words, so the steps themselves vary.
12. The test only confirms that the code does what it already does, including its bugs. Expected results must come from the requirements.
13. When several tests need the same set of rows (the fixture is defined once and shared), or when you want setup logic along with the data.
14. A seed makes the "random" sequence repeat, so a failure can be reproduced exactly. Without a seed, a test might fail once and never again.

---

## Key Takeaways

- Data-driven testing separates test logic from test data: write the steps once, run them against many rows. Think "mail merge for tests" and "one recipe, many ingredient lists."
- Test design techniques (BVA, EP, decision tables, error guessing) decide which data to use; DDT is how you run it. A design table is already a data set.
- In pytest, `@pytest.mark.parametrize` gives you one test per row, with readable names via `ids` or `pytest.param(..., id=...)`, and every row runs even if another fails.
- Use `pytest.param` with `xfail` and `skip` to handle known defects and unbuilt features, always giving a reason that points to a defect ID.
- CSV and JSON files move data out of code so non-programmers can contribute; remember that CSV values are text and need converting.
- Fixtures with `params` act as data providers that many tests can share. Stacked decorators multiply: always count the combinations first.
- A good data row has a unique `test_id`, a clear description, and an expected result taken from the requirements, never from the code under test.
- Keep data independent, clean, privacy-safe (synthetic or masked, never real personal data), consistently named, and in version control.
- When a row fails, ask "is the code wrong or is the data wrong?" and answer by checking the requirement.
- Avoid the common traps: copied expected results, hidden dependencies, huge datasets on every commit, vague names, and over-engineering.
- DDT supports regression: every defect becomes a new row that protects against its return. Regression testing is the topic of the next lesson.

---

## Additional Resources

- pytest documentation, "How to parametrize fixtures and test functions": https://docs.pytest.org/en/stable/how-to/parametrize.html
- Python documentation, the `csv` module (CSV File Reading and Writing): https://docs.python.org/3/library/csv.html
- Ministry of Testing, a community with articles, courses, and discussion on test design and automation: https://www.ministryoftesting.com/
