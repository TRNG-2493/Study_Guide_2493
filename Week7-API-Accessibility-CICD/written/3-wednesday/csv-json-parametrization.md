# CSV/JSON Parametrization

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why test data lives in external CSV and JSON files, and when that is better than a Python list.
- Lay out a `data/` folder and locate files reliably with `pathlib`, no matter where pytest is launched.
- Read CSV with `csv.DictReader` and JSON with `json.load`, and convert CSV strings into real Python types.
- Write a small loader module that cleans blank lines, BOM characters and empty values.
- Feed loaded rows into `@pytest.mark.parametrize` with readable ids and per-row `skip`/`xfail` marks.
- Choose CSV for flat tables and JSON for nested payloads.
- Validate the data files themselves, and keep secrets out of them.
- Decide between parametrizing at collection time and using fixtures with `params`.

---

## Why This Matters

This is the Week 7 epic: you are building an API test suite that is accessible to the whole team and runs automatically in a pipeline. In the earlier Wednesday lesson you learned data-driven testing: one test function, many input rows, using `@pytest.mark.parametrize`. Those rows lived inside the `.py` file. That works for five cases. It stops working when:

- A manual tester or business analyst wants to add 40 cases and does not want to edit Python.
- The table grows so large that the test file is mostly data and the logic is hard to find.
- A pull request mixes a logic change with a data change, so reviewers cannot see which is which.
- The same data is needed by several tests.

**Real-world scenario.** A QA team tests a "create post" endpoint. The product owner keeps a spreadsheet of boundary cases (empty title, 255-character title, unicode title). Today someone retypes the spreadsheet into Python after every meeting. If the test reads a CSV exported from that spreadsheet, the retyping disappears: the product owner edits a file, the pipeline you will build later in the week runs it, and the test code never changes.

This lesson shows how to do that safely. The tricky parts are not the reading itself (a few lines) but the details: everything in CSV is text, Excel adds invisible characters, blank cells are ambiguous, and a typo in a data file should produce a clear message, not a confusing stack trace. We will use **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`), a free fake API, as the target so you can run everything yourself.

---

## The Concept

### 1. What and Why: External Test Data

**What.** Instead of writing

```python
CASES = [(1, 200), (50, 200), (0, 404)]
```

in the test module, you store the cases in a file, load the file into the same kind of list, and give that list to `parametrize`. The test function is unchanged.

**Why.**

- **Separation of concerns.** Code says *how* to test; data says *what* to test.
- **Accessibility for non-programmers.** CSV opens in Excel; JSON opens in any editor.
- **Reviewability.** A data-only change shows up as a data-only diff.
- **Reuse.** One file can feed several tests.

**When not to.** For two or three cases tied closely to the test's meaning, keep the list in the file; every indirection costs the reader a jump.

### 2. Folder Layout

```
project/
├── data/
│   ├── posts_lookup.csv
│   ├── create_post_cases.json
│   └── README.md
├── utils/
│   ├── __init__.py
│   └── data_loader.py
├── tests/
│   ├── test_posts_csv.py
│   ├── test_create_post_json.py
│   └── test_data_files.py
└── conftest.py
```

- `data/` holds only data. Keep file names descriptive: `posts_lookup.csv` is better than `data1.csv`.
- `utils/data_loader.py` is the single place that knows how to open files. Tests never call `open` directly.
- `data/README.md` (optional) documents each column. Future you will be grateful.
- `test_data_files.py` tests the data itself (section 11).

### 3. Locating Files with `pathlib`

The most common beginner failure is `FileNotFoundError`. It happens when code says `open("data/posts_lookup.csv")`. That is a path relative to the **current working directory**, which is wherever you ran `pytest` from, not where the test file lives. Run from the project root and it works; run from `tests/` or from an IDE with a different setting, and it fails.

The fix is to anchor the path to the **loader file's own location**:

```python
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
```

Line by line:

- `from pathlib import Path` imports the object-oriented path class from the standard library.
- `__file__` is a built-in variable holding the path of the current Python file (`utils/data_loader.py`).
- `Path(__file__)` wraps that string as a `Path` object.
- `.resolve()` turns it into an absolute path and removes `..` pieces and symlinks.
- `.parent` is the folder containing the file (`utils/`); the second `.parent` is the project root.
- `/ "data"` uses the `/` operator, which `Path` overloads to join path segments on any operating system. You never write backslashes or forward slashes yourself.

Now `DATA_DIR / "posts_lookup.csv"` is the same absolute path from anywhere.

### 4. Reading CSV with `csv.DictReader`

#### 4.1 The data file: `data/posts_lookup.csv`

```csv
case_id,post_id,expected_status,expected_user_id,flag,reason
post-1,1,200,1,,
post-50,50,200,5,,
post-100,100,200,10,,
post-0,0,404,,,
post-101,101,404,,,
post-abc,abc,404,,xfail,"API returns 404 here, confirm with team"
legacy-case,7,200,,skip,Replaced by post-50
```

Rules of CSV: the first line is the **header**; each following line is one record; commas separate cells; two commas in a row mean an empty cell; a value that itself contains a comma must be wrapped in double quotes (see the `reason` on `post-abc`).

#### 4.2 Reading it

```python
import csv

with open("data/posts_lookup.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(rows[0])
```

Representative output:

```
{'case_id': 'post-1', 'post_id': '1', 'expected_status': '200', 'expected_user_id': '1', 'flag': '', 'reason': ''}
```

Line by line:

- `import csv` loads the standard-library module. No installation needed.
- `open(..., newline="", encoding="utf-8")`: `newline=""` is what the `csv` documentation requires, so the module can handle line breaks inside quoted cells and avoid doubled blank lines on Windows. `encoding="utf-8"` states the text encoding explicitly instead of relying on the machine default.
- `with ... as f` closes the file automatically, even if an error occurs.
- `csv.DictReader(f)` reads the header and then turns each row into a dictionary keyed by header names. You write `row["post_id"]` instead of remembering "column 2".
- `list(...)` reads everything into memory now, before the file closes. If you returned the reader itself, it would fail later with "I/O operation on closed file".

**The critical fact: every value is a string.** `post_id` is `'1'`, not `1`. A blank cell is `''`, not `None`. If you compare `response.status_code == row["expected_status"]` you compare `200` to `'200'`, which is always `False`, and the test fails for a baffling reason. You must convert.

### 5. Converting Types

Small, named converters are easier to read and test than inline `int(...)` calls.

```python
def to_int(text):
    """'42' -> 42, '' -> None."""
    return int(text) if text else None


def to_bool(text):
    """'true', 'yes', '1', 'y' (any case) -> True; everything else -> False."""
    return text.strip().lower() in {"true", "yes", "1", "y"}


def to_none(text):
    """'' -> None, otherwise the text unchanged."""
    return text if text else None
```

Line by line:

- `to_int`: an empty string is "falsy" in Python, so `if text` is `False` for `''`. We return `None` instead of crashing with `ValueError: invalid literal for int()`. For non-empty text we call `int`. Note that `int('abc')` still raises; that is good, because it means the data file has a mistake (or the row is a deliberate invalid case that you should keep as a string, see the `post-abc` row below).
- `to_bool`: CSV has no booleans. The function defines your team's convention for "true". Everything else, including a blank, becomes `False`. Write the convention down in `data/README.md`.
- `to_none`: used when "no value" must be distinguished from "empty string" later.

**Blank means what?** Decide once and document it. Common convention: a blank cell means "this field is not applicable, do not send it". If you need to send a literal empty string, use an explicit marker such as `<EMPTY>` and translate it in the loader:

```python
def decode_marker(text):
    return "" if text == "<EMPTY>" else text
```

`decode_marker` returns an empty string only when the cell contains the marker; otherwise it passes the text through. Without the marker, "field missing" and "field is empty" would be impossible to tell apart, and those are different test scenarios with different expected API behavior.

### 6. Reading JSON with `json.load`

#### 6.1 The data file: `data/create_post_cases.json`

```json
[
  {
    "id": "minimal-post",
    "body": {"title": "hello", "body": "world", "userId": 1},
    "expected_status": 201,
    "expected_fields": ["title", "userId"]
  },
  {
    "id": "nested-tags",
    "body": {
      "title": "tagged",
      "body": "with nested data",
      "userId": 2,
      "tags": ["qa", "api"],
      "meta": {"draft": true, "priority": null}
    },
    "expected_status": 201,
    "expected_fields": ["title", "userId", "tags", "meta"]
  },
  {
    "id": "unicode-title",
    "body": {"title": "Café ☕ test", "body": "x", "userId": 3},
    "expected_status": 201,
    "expected_fields": ["title"]
  },
  {
    "id": "known-bug-empty-title",
    "body": {"title": "", "body": "x", "userId": 1},
    "expected_status": 400,
    "expected_fields": [],
    "flag": "xfail",
    "reason": "JSONPlaceholder accepts anything; real API should reject"
  }
]
```

Notice what CSV could not express cleanly: a nested object (`meta`), a list (`tags`), a real boolean (`true`), a real `null`, and numbers that are already numbers.

#### 6.2 Reading it

```python
import json

with open("data/create_post_cases.json", encoding="utf-8") as f:
    cases = json.load(f)

print(type(cases), len(cases))
print(cases[1]["body"]["tags"])
```

Representative output:

```
<class 'list'> 4
['qa', 'api']
```

Line by line:

- `json.load(f)` reads from an open file and returns Python objects: JSON array becomes `list`, object becomes `dict`, `true`/`false` become `True`/`False`, `null` becomes `None`, numbers stay numbers.
- Do not confuse `json.load(file)` with `json.loads(string)`: the trailing `s` means "string".
- No `newline=""` is needed for JSON; only the `csv` module asks for it.
- `cases[1]["body"]["tags"]` walks the nesting with ordinary indexing.

Strict JSON rules: double quotes only, no trailing commas, no comments. If you want a note, add a `"note"` key. A `json.JSONDecodeError` message includes the line and column; start there.

### 7. A Helper Loader Module

Put every file-handling decision in one module. Tests then stay short, and when you change a convention (say, how blanks are treated) you change it once.

```python
# utils/data_loader.py
import csv
import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv_rows(filename, required=()):
    """Read data/<filename>; return a list of cleaned dict rows."""
    path = DATA_DIR / filename
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, restkey="_extra")
        reader.fieldnames = [n.strip() for n in (reader.fieldnames or [])]
        missing = set(required) - set(reader.fieldnames)
        if missing:
            raise ValueError(f"{filename}: missing columns {sorted(missing)}")
        rows = []
        for row in reader:
            where = f"{filename} line {reader.line_num}"
            if "_extra" in row:
                raise ValueError(f"{where}: too many cells")
            if None in row.values():
                raise ValueError(f"{where}: too few cells")
            row = {k: v.strip() for k, v in row.items()}
            if not any(row.values()):
                continue
            rows.append(row)
    return rows


def load_json(filename):
    """Read data/<filename>; return the parsed JSON."""
    with (DATA_DIR / filename).open(encoding="utf-8-sig") as f:
        return json.load(f)


def to_params(rows, builder, id_key):
    """Turn rows into pytest.param objects with ids and skip/xfail marks."""
    params = []
    for row in rows:
        marks = []
        flag = str(row.get("flag", "")).lower()
        reason = row.get("reason") or "see data file"
        if flag == "skip":
            marks.append(pytest.mark.skip(reason=reason))
        elif flag == "xfail":
            marks.append(pytest.mark.xfail(reason=reason, strict=True))
        elif flag:
            raise ValueError(f"unknown flag {flag!r} in row {row[id_key]!r}")
        values = builder(row)
        params.append(pytest.param(*values, id=row[id_key], marks=marks))
    return params
```

Line by line:

- Imports: `csv`, `json` and `Path` for reading; `pytest` only because `to_params` builds `pytest.param` objects.
- `DATA_DIR` is the anchored path from section 3.
- `load_csv_rows(filename, required=())`: `required` is a tuple of column names the file must have; the default empty tuple means "no check".
- `path.open(...)` is the `Path` method equivalent of `open(path, ...)`. We use `encoding="utf-8-sig"`: it reads normal UTF-8 and also silently strips the invisible **byte order mark** (BOM) that Excel adds when you choose "CSV UTF-8". Without it the first header becomes `'﻿case_id'` and every `row["case_id"]` raises `KeyError`.
- `csv.DictReader(f, restkey="_extra")`: when a row has more cells than the header, the surplus cells are stored in a list under the key `"_extra"` instead of the default key `None`. A named key is easier to detect.
- `reader.fieldnames = [...]` strips accidental spaces from header names (`" age"` becomes `"age"`). Accessing `reader.fieldnames` reads the header line; `or []` covers a completely empty file.
- `missing = set(required) - set(reader.fieldnames)` uses set subtraction to find required columns that are absent. A clear `ValueError` naming them beats a `KeyError` three layers down.
- The `for row in reader` loop: `reader.line_num` is the physical line number in the file, useful in error messages. Blank lines are skipped by `csv` itself, so they never appear as rows.
- `"_extra" in row` catches a row with too many cells (often an unquoted comma). `None in row.values()` catches too few cells: `DictReader` fills missing trailing cells with `None`.
- `{k: v.strip() ...}` is a dictionary comprehension that trims whitespace from every value, so `" 200"` becomes `"200"`.
- `if not any(row.values()): continue` drops rows where every cell is empty, such as a line containing only `,,,,,` (which Excel often leaves at the end of an export). `any` is `False` when all values are empty strings.
- `load_json` mirrors the same idea; `utf-8-sig` is used here too because some Windows editors save JSON with a BOM, and `json.load` would otherwise fail.
- `to_params`: for each row it builds a list of marks. `row.get("flag", "")` tolerates files with no `flag` column; `str(...)` tolerates a non-string value from JSON; `.lower()` makes `XFAIL` work. An unknown flag raises an error instead of being silently ignored, because a typo like `skpi` would otherwise run a test you meant to skip.
- `pytest.mark.xfail(..., strict=True)` means: expected to fail; if it unexpectedly passes, report that as a failure so someone notices and removes the flag.
- `builder(row)` is a function you pass in that converts a row into the tuple of argument values for the test. This keeps the module generic.
- `pytest.param(*values, id=row[id_key], marks=marks)` makes one test case with a name and its marks. `*values` unpacks the tuple into separate arguments.

### 8. Feeding the Rows into `parametrize`

#### 8.1 CSV: post lookup

```python
# tests/test_posts_csv.py
import pytest
import requests

from utils.data_loader import load_csv_rows, to_params, to_int

BASE_URL = "https://jsonplaceholder.typicode.com"


def build(row):
    return row["post_id"], int(row["expected_status"]), to_int(row["expected_user_id"])


CASES = to_params(
    load_csv_rows(
        "posts_lookup.csv",
        required=("case_id", "post_id", "expected_status", "expected_user_id"),
    ),
    builder=build,
    id_key="case_id",
)


@pytest.mark.parametrize("post_id, expected_status, expected_user_id", CASES)
def test_get_post(post_id, expected_status, expected_user_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)

    assert response.status_code == expected_status, response.text[:200]
    if expected_user_id is not None:
        assert response.json()["userId"] == expected_user_id
```

Line by line:

- `build(row)` returns a tuple of three values in the same order as the parameter names. `post_id` stays a **string** deliberately: it is only placed into a URL, and keeping it text lets the `abc` row work. `expected_status` is converted with `int`. `expected_user_id` uses `to_int`, so a blank becomes `None`.
- `CASES = to_params(...)` runs when the module is imported (at collection time). It reads the file once and produces seven `pytest.param` objects.
- `required=(...)` makes a missing or misspelled header fail immediately with a named column.
- The decorator `@pytest.mark.parametrize("post_id, expected_status, expected_user_id", CASES)` lists three argument names in one comma-separated string; each case must supply three values.
- The test sends a GET using `requests` (Monday's HTTP basics). `timeout=10` stops a hung call from freezing the run.
- `assert ..., response.text[:200]` shows the first 200 characters of the body if the assertion fails.
- `if expected_user_id is not None` guards the check: for 404 rows there is no `userId` to compare.

Representative output of `pytest -v`:

```
tests/test_posts_csv.py::test_get_post[post-1] PASSED
tests/test_posts_csv.py::test_get_post[post-50] PASSED
tests/test_posts_csv.py::test_get_post[post-100] PASSED
tests/test_posts_csv.py::test_get_post[post-0] PASSED
tests/test_posts_csv.py::test_get_post[post-101] PASSED
tests/test_posts_csv.py::test_get_post[post-abc] XFAIL (API returns 404 here, ...)
tests/test_posts_csv.py::test_get_post[legacy-case] SKIPPED (Replaced by post-50)
```

The ids come from the `case_id` column, so a failure reads `[post-101]`, not `[101-404-None]`. `post-abc` is `xfail` with `strict=True`: if the API really returns 404 the case passes unexpectedly (XPASS) and strict mode reports a failure, telling you the data file's claim is stale. Exercise 2 fixes it.

#### 8.2 JSON: create post

```python
# tests/test_create_post_json.py
import pytest
import requests

from utils.data_loader import load_json, to_params

BASE_URL = "https://jsonplaceholder.typicode.com"


def build(case):
    return case["body"], case["expected_status"], case["expected_fields"]


CASES = to_params(load_json("create_post_cases.json"), builder=build, id_key="id")


@pytest.mark.parametrize("body, expected_status, expected_fields", CASES)
def test_create_post(body, expected_status, expected_fields):
    response = requests.post(f"{BASE_URL}/posts", json=body, timeout=10)

    assert response.status_code == expected_status
    echoed = response.json()
    for field in expected_fields:
        assert echoed[field] == body[field], f"{field} not echoed correctly"
```

Line by line:

- `build(case)` pulls the nested request body and the expectations from the dictionary. No type conversion is needed: JSON already holds real numbers and lists.
- `to_params(load_json(...), ...)` works because a JSON file whose top level is an array of objects has the same shape as the list of CSV row dictionaries. The `flag` and `reason` keys in the last case give it an `xfail` mark.
- `requests.post(..., json=body)` serialises the dictionary to JSON and sets the `Content-Type` header for you.
- JSONPlaceholder is a fake API: it echoes back what you send, plus an `id` (always `101`), and does not save anything. So we assert that selected fields came back equal, including the nested `tags` and `meta`.
- The `known-bug-empty-title` case expects 400, but this fake API returns 201, so the assertion fails and the case is reported `XFAIL`. On a real API with validation it would pass, and strict mode would tell you to remove the flag.

Representative output:

```
tests/test_create_post_json.py::test_create_post[minimal-post] PASSED
tests/test_create_post_json.py::test_create_post[nested-tags] PASSED
tests/test_create_post_json.py::test_create_post[unicode-title] PASSED
tests/test_create_post_json.py::test_create_post[known-bug-empty-title] XFAIL
```

### 9. CSV or JSON: Choosing

| | CSV | JSON |
|---|---|---|
| Shape | Flat rows and columns | Nested objects and arrays |
| Types | All text; you convert | Numbers, booleans, `null`, lists preserved |
| Best for | Many simple cases: IDs, boundaries, status codes | Request bodies with nesting, lists, mixed types |
| Edited by | Excel, Google Sheets, non-programmers | Developers, any text editor |
| Git diff | One line per case, easy to scan | Readable if consistently formatted |
| Comments | None standard | None; use a `"note"` key |
| Risk | Excel silently reformats (`007` becomes `7`, dates change) | Strict syntax: one stray comma breaks the file |

Rule of thumb: **flat table of scalar values: CSV. Nested payload or types that matter: JSON.** Avoid putting JSON strings inside CSV cells: every `"` must be doubled and it is miserable to edit. If you are tempted, switch to JSON.

**YAML (brief).** Some teams use YAML because it allows comments and is pleasant to read. It requires a third-party package (`pip install pyyaml`) and `yaml.safe_load(f)`. Beware its implicit typing: an unquoted `no` becomes `False` and `1.10` becomes the float `1.1`. Everything in this lesson (paths, ids, marks, validation) works the same with YAML; only the loading line changes. Always use `safe_load`, never `load`.

### 10. Collection-Time Parametrization vs Fixtures with `params`

There are two ways to turn data into multiple test runs.

**A. `@pytest.mark.parametrize` with a module-level list** (what we did above). The file is read when the module is imported, during collection. All cases are known before any test runs, which is why `pytest --collect-only` can list them and why `-k post-101` can select one.

**B. A fixture with `params`.**

```python
# conftest.py
import pytest
from utils.data_loader import load_json


@pytest.fixture(params=load_json("create_post_cases.json"), ids=lambda case: case["id"])
def post_case(request):
    return request.param
```

```python
# tests/test_create_post_fixture.py
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_create_post_status(post_case):
    response = requests.post(f"{BASE_URL}/posts", json=post_case["body"], timeout=10)
    assert response.status_code in (201, 400)
```

Line by line:

- `@pytest.fixture(params=[...])` tells pytest to run every test that uses this fixture once per item in the list.
- `ids=lambda case: case["id"]` is a function that computes the id for each item, so reports read `[minimal-post]`.
- The fixture function takes pytest's built-in `request` argument; `request.param` is the current item. (This is the one place `request` is the right name. In a plain `parametrize`, never name your own parameter `request`.)
- The test just names the fixture and receives one whole case dictionary, with no unpacking.

**Which to choose.**

| Use `parametrize` when | Use a fixture with `params` when |
|---|---|
| One test needs the data | Many tests should run against the same data set |
| You want values as separate named arguments | You want setup/teardown per case (create a record, then delete it) |
| You want per-case marks easily (`pytest.param`) | The case is passed around as a single object |

Both are decided at collection time: data is read once, when pytest imports the file, not when the test runs. Consequences to remember:

- A missing or invalid data file breaks **collection** of that module (an `ERROR collecting` message), not a single test. This is good: it fails loudly and early.

(There is also a third mechanism, the `pytest_generate_tests` hook in `conftest.py`, which generates parameters programmatically per test. You will not need it in this lesson. The framework lesson later in the week shows where it fits.)

### 11. Validating the Data Files Themselves

A test suite that trusts its data blindly will, sooner or later, fail because someone left a column blank, not because the API broke. Treat data files as code: test them.

```python
# tests/test_data_files.py
from collections import Counter

from utils.data_loader import load_csv_rows, load_json


def test_posts_csv_ids_are_unique():
    rows = load_csv_rows("posts_lookup.csv", required=("case_id",))
    counts = Counter(r["case_id"] for r in rows)
    duplicates = [cid for cid, n in counts.items() if n > 1]
    assert not duplicates, f"Duplicate case_id values: {duplicates}"


def test_posts_csv_values_are_sane():
    for row in load_csv_rows("posts_lookup.csv"):
        assert row["case_id"], f"Blank case_id in {row}"
        assert 100 <= int(row["expected_status"]) <= 599, row
        assert row["flag"] in ("", "skip", "xfail"), row


def test_create_post_json_shape():
    cases = load_json("create_post_cases.json")
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "Duplicate ids"
    for case in cases:
        assert set(case) >= {"id", "body", "expected_status", "expected_fields"}, case["id"]
        assert isinstance(case["body"], dict), case["id"]
```

Line by line:

- `Counter(...)` counts how often each `case_id` appears; any count above 1 is a duplicate. Duplicate ids make pytest rename tests with suffixes (`post-1_0`, `post-1_1`), which breaks `-k` selection and confuses reports.
- The second test checks per-row sanity: ids present, status codes in the valid HTTP range, and the `flag` value limited to known words. `int(...)` raising `ValueError` on bad text also counts as a failed test, which is the intent.
- The third checks JSON shape: unique ids, required keys (`set(case) >= {...}` means "the case's keys include all of these"), and that `body` is an object, not a list or string.
- The failure messages include the id or row, so whoever edited the data sees what to fix.

### 12. Edge Cases and Pitfalls

- **Encoding and BOM.** Excel's "CSV UTF-8" adds a BOM; the default "CSV" on Windows may use a legacy code page (cp1252) and corrupt accented letters when read as UTF-8. Save as UTF-8 and read with `utf-8-sig`. If you see `UnicodeDecodeError` or text like `CafÃ©`, the encoding is the culprit.
- **Blank lines.** `csv` skips entirely empty lines, but a line of only commas (`,,,,,`) is a real row of empty strings. Our loader drops those.
- **Empty values.** `''` is not `None`. Convert explicitly, and document whether blank means "omit field", "send null" or "send empty string".
- **`None` in the data.** In JSON, write `null`; it arrives as `None`. In CSV there is no null; use a blank plus a convention, or an explicit marker such as `NULL` decoded in a converter.
- **Excel auto-formatting.** IDs like `007` lose zeros; long numbers turn into scientific notation; `1/2` becomes a date. Format the column as Text before typing, or put such data in JSON.
- **Empty parameter set.** If a loader returns `[]`, pytest skips the test with "got empty parameter set" and nothing fails. A green run with a skipped test can hide a broken data file; the validation tests above help.

### 13. Secrets and Version Control

**Secrets.** Data files are committed to the repository and read by everyone with access, including CI logs. Never put real passwords, API tokens, personal data or production customer records in them. Use fake users and obviously fake values (`"Passw0rd!"` for a throwaway test account is acceptable only if that account exists solely in a test environment). For values that must be real, store a placeholder in the file and read the secret from an environment variable at load time:

```python
import os
from string import Template


def resolve_env(text):
    return Template(text).safe_substitute(os.environ)
```

Line by line: `Template` treats `${NAME}` in a string as a variable; `safe_substitute(os.environ)` replaces each with the matching environment variable, and leaves unknown placeholders untouched instead of raising an error. So the file holds `"password": "${API_PASSWORD}"`, and you apply `json.loads(resolve_env(json.dumps(case)))` to each case before use. The Friday pipeline lesson covers how CI supplies such variables safely.

**Version control.**

- Commit data files, since the tests are meaningless without them.
- Keep data changes in their own commits or clearly separated, with a message such as `data: add boundary cases for post ids`.
- Prefer stable ordering and consistent JSON indentation so diffs show only real changes. Excel re-saves can reorder quoting or change line endings; review the diff before committing.
- Add a `.gitattributes` line such as `*.csv text eol=lf` so line endings do not flip between Windows and Linux.
- Reviewers should look at data changes as carefully as code: a wrong `expected_status` silently weakens the suite.

### 14. Glossary

#### Data-driven test
One test function executed against many rows of data.

#### Parametrization
The pytest mechanism (`@pytest.mark.parametrize`, or fixtures with `params`) that creates one test case per data row.

#### Collection time
The phase when pytest imports test files and builds the list of tests, before running any of them. Module-level data loading happens here.

#### `csv.DictReader`
A standard-library reader that yields each CSV row as a dictionary keyed by the header names.

#### `json.load`
Reads JSON from a file object and returns Python lists, dictionaries, strings, numbers, booleans and `None`.

#### `pathlib.Path`
Object-oriented file path; `Path(__file__).resolve().parent` is the folder of the current file.

#### BOM (byte order mark)
An invisible character at the start of some UTF-8 files (notably from Excel). Read with `utf-8-sig` to remove it.

#### `pytest.param`
Wraps one set of arguments so you can attach an `id` and `marks` to that case alone.

#### `skip` / `xfail`
Marks: `skip` does not run the test; `xfail` runs it and expects failure. With `strict=True`, an unexpected pass is reported as a failure.

#### Fixture with `params`
A fixture that runs dependent tests once per listed parameter, delivering the current item as `request.param`.

#### Data file validation
Tests that check the data files themselves: unique ids, required columns, allowed values.

---

## Practice Exercises

### Exercise 1: Load and run the posts CSV
Create `data/posts_lookup.csv` and `utils/data_loader.py` from this lesson, plus `tests/test_posts_csv.py`. Run `pytest -v` and `pytest --collect-only -q`. Confirm that seven test ids appear, with one `XFAIL` or failing and one `SKIPPED`.

**Solution.** Copy the files exactly. Run from the project root:

```
pytest -v tests/test_posts_csv.py
```

You should see ids `post-1`, `post-50`, `post-100`, `post-0`, `post-101`, `post-abc` and `legacy-case`. `legacy-case` shows `SKIPPED` with its reason. For `post-abc`, JSONPlaceholder returns 404, which matches the expected status, so with `strict=True` it appears as `FAILED` ("XPASS(strict)"). That is the point of Exercise 2. If you see `ModuleNotFoundError: utils`, add an empty `utils/__init__.py` and an empty `conftest.py` in the project root (this makes pytest add the root to the import path), or run `python -m pytest`.

### Exercise 2: Fix the data, not the code
The `post-abc` row is wrong: the API really returns 404 and the row says it is a known failure. Fix the data so the whole file passes. Then add two new rows, `post-2` (expects user 1) and `post-99` (expects user 10), without touching any `.py` file.

**Solution.** Clear the `flag` and `reason` cells on `post-abc`, giving `post-abc,abc,404,,,`. Append:

```csv
post-2,2,200,1,,
post-99,99,200,10,,
```

Run `pytest -v`: nine test ids, no failures, one skip. The test code did not change, which is the whole benefit of data-driven files. (Posts 1-10 belong to user 1, 91-100 to user 10.)

### Exercise 3: Add a todos JSON file with a nested expectation
Create `data/todos_cases.json` with three cases for `GET /todos/{id}`: id 1 (expects status 200, `completed` false, `userId` 1), id 4 (expects status 200, `completed` true), id 9999 (expects 404). Write a test that uses `load_json` and `to_params` and asserts any expected fields listed in an `expected_json` object.

**Solution.**

```json
[
  {"id": "todo-1",    "todo_id": 1,    "expected_status": 200,
   "expected_json": {"completed": false, "userId": 1}},
  {"id": "todo-4",    "todo_id": 4,    "expected_status": 200,
   "expected_json": {"completed": true}},
  {"id": "todo-9999", "todo_id": 9999, "expected_status": 404,
   "expected_json": {}}
]
```

```python
# tests/test_todos_json.py
import pytest
import requests

from utils.data_loader import load_json, to_params

BASE_URL = "https://jsonplaceholder.typicode.com"


def build(case):
    return case["todo_id"], case["expected_status"], case["expected_json"]


CASES = to_params(load_json("todos_cases.json"), builder=build, id_key="id")


@pytest.mark.parametrize("todo_id, expected_status, expected_json", CASES)
def test_get_todo(todo_id, expected_status, expected_json):
    response = requests.get(f"{BASE_URL}/todos/{todo_id}", timeout=10)
    assert response.status_code == expected_status
    if expected_status == 200:
        body = response.json()
        for key, value in expected_json.items():
            assert body[key] == value, f"{key}: {body[key]!r} != {value!r}"
```

The JSON booleans arrive as Python `False`/`True`, so `body["completed"] == False` compares correctly with no converter. The `expected_json: {}` for the 404 case means the loop would do nothing, and we skip it anyway because there is no body to check.

### Exercise 4: Validate and harden
(a) Write a test that fails if any row in `posts_lookup.csv` has `flag` equal to anything other than blank, `skip` or `xfail`. (b) Deliberately misspell the header `expected_status` as `expected_statu` and describe the error you get.

**Solution.** (a) Already present in `test_posts_csv_values_are_sane` (`assert row["flag"] in ("", "skip", "xfail"), row`); extract it into its own test if you wish. (b) Because `required=("case_id", "post_id", "expected_status", "expected_user_id")` is passed, collection fails with `ValueError: posts_lookup.csv: missing columns ['expected_status']`, naming the file and column. Without `required`, you would get a `KeyError: 'expected_status'` from inside `build`, which is harder to trace. (c) The BOM is the three bytes `EF BB BF` at the start of the file. Opening with `utf-8-sig` removes them before `DictReader` reads the header, so the first column is `case_id`, not `﻿case_id`.

---

## Quiz

**1.** What is the value type of `row["expected_status"]` after `csv.DictReader` reads a cell containing `404`?
a) `int`  b) `str`  c) `float`  d) It depends on the column

**2.** Why use `Path(__file__).resolve().parent.parent / "data"` instead of `"data/file.csv"`?
a) It runs faster
b) The path no longer depends on the working directory pytest was launched from
c) It converts the CSV to JSON
d) It prevents BOM problems

**3.** Which statement about `pytest.param(..., id="x", marks=[pytest.mark.skip(reason="y")])` is correct?
a) The id and mark apply to the whole test function
b) The id and mark apply only to that one case
c) `marks` must be a string
d) `id` is only used for fixtures

**4.** Your request body contains a list and a nested object. Which format is the better fit?
a) CSV, because Excel is easier
b) JSON, because it preserves nesting and types
c) Either, with no difference
d) Neither; it must stay in Python

**5.** A data-file typo causes `ERROR collecting tests/test_posts_csv.py`. What is the most accurate explanation?
a) The API is down
b) The file is read at import time, during collection, so any loading error stops that module being collected
c) pytest does not support CSV
d) `xfail` marks cause collection errors

**Answers.**
1. **b** - `csv` never converts; all cells are strings, and blank cells are `''`.
2. **b** - `__file__` is anchored to the loader's location, so the path is absolute and stable.
3. **b** - `pytest.param` attaches id and marks to a single case.
4. **b** - JSON keeps nested objects, lists, booleans, `null` and numbers.
5. **b** - Module-level loading runs at collection time; the error is raised while building the list of tests, which is why validating data files early is valuable.

---

## Summary

- External CSV and JSON files separate test data from test logic, so more people can contribute cases and reviews stay clear.
- Anchor file locations with `Path(__file__).resolve().parent`; never rely on the working directory.
- `csv.DictReader` returns strings only; convert with named helpers and document what a blank cell means.
- `json.load` preserves types and nesting; use JSON for request bodies, CSV for flat tables.
- A small loader module handles encoding (`utf-8-sig` for Excel BOMs), blank lines, whitespace, column checks and the creation of `pytest.param` objects with ids and `skip`/`xfail` marks from `flag` columns.
- Choose `parametrize` for a single test with a data list; choose a fixture with `params` when many tests share the cases or need per-case setup. Both load at collection time.
- Test your data files: unique ids, required columns, allowed values.
- Keep secrets out of data files; version data like code, with focused commits and careful review. YAML is a workable alternative with the same approach, but beware implicit typing.

## Additional Resources

- Python documentation, *csv: CSV File Reading and Writing*: https://docs.python.org/3/library/csv.html
- Python documentation, *json: JSON encoder and decoder*: https://docs.python.org/3/library/json.html
- Python documentation, *pathlib: Object-oriented filesystem paths*: https://docs.python.org/3/library/pathlib.html
- pytest documentation, *Parametrizing tests* (including `pytest.param`): https://docs.pytest.org/en/stable/how-to/parametrize.html
- pytest documentation, *Parametrizing fixtures*: https://docs.pytest.org/en/stable/how-to/fixtures.html#parametrizing-fixtures
- JSONPlaceholder (free fake API and guide): https://jsonplaceholder.typicode.com/guide/
