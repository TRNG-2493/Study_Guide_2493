# Handout 05 – Contracts, Data & Independence

> **How to use this handout:** each topic is a small, self-contained example in its own folder inside `week7-demos/`. Nothing carries over from one topic to the next. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- Activate your `week7-demos` virtual environment and run: `pip install requests pytest jsonschema pydantic pytest-randomly`
- Practice API: `https://jsonplaceholder.typicode.com`.

> `pytest-randomly` shuffles test order as soon as it is installed. Add `-p no:randomly` to any command if you want the normal order back.

---

## Topic 1 – Request/Response Validation

📁 Folder: `05-1-contract/`

### Definition

**Request/response validation** checks that both what you send and what you receive match the API's **contract**: its agreed fields, types and rules. A **JSON Schema** is a JSON document that describes that contract with keywords such as `type`, `required`, `enum`, `minimum` and `additionalProperties`. **Pydantic** offers another way: you describe the response as a typed Python class and let Pydantic check and convert the data. Validating both directions catches **API drift**, such as a renamed field, a changed type or a new value, before your users do.

### Key ideas

| Keyword | Example | Catches |
|---------|---------|---------|
| `required` | `["id", "title"]` | A field that went missing |
| `type` | `"integer"` | `"1"` sent instead of `1` |
| `minLength` / `minimum` | `1` | Empty strings, zero or negative ids |
| `enum` / `pattern` | `["open", "closed"]` / `"^\\S+@\\S+$"` | Unexpected values and bad formats |
| `additionalProperties: false` | | Extra or misspelled fields |

- **Schema or model?** A schema is language-neutral, and the same file can be shared with other teams. A Pydantic model gives you typed Python objects to work with in tests.
- Keep schemas in a `schemas/` folder, and do not make them stricter than the API documentation, or your tests become brittle.

### Worked example – A schema file and a Pydantic model

```
05-1-contract/
├── schemas/post.json
├── schema_check.py
└── test_contract.py
```

**Step 1 – Save the contract as `schemas/post.json`.**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "userId", "title", "body"],
  "properties": {
    "id":     { "type": "integer", "minimum": 1 },
    "userId": { "type": "integer", "minimum": 1 },
    "title":  { "type": "string",  "minLength": 1 },
    "body":   { "type": "string" }
  },
  "additionalProperties": false
}
```

**Step 2 – Write a validator that reports every error** (`schema_check.py`).

```python
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


def assert_matches_schema(instance, name):
    schema = json.loads((SCHEMA_DIR / f"{name}.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=str)
    assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors)
```

**Step 3 – Validate a response** (`test_contract.py`).

```python
import requests
from schema_check import assert_matches_schema

BASE = "https://jsonplaceholder.typicode.com"


def test_get_post_matches_contract():
    assert_matches_schema(requests.get(f"{BASE}/posts/1", timeout=5).json(), "post")
```

**Step 4 – Validate the request payload too.**

```python
def test_create_post_contract():
    payload = {"title": "QE", "body": "b", "userId": 1}
    assert_matches_schema({**payload, "id": 1}, "post")   # payload has the right shape
    created = requests.post(f"{BASE}/posts", json=payload, timeout=5).json()
    assert_matches_schema(created, "post")
```

**Step 5 – Do the same check with a Pydantic model.**

```python
from pydantic import BaseModel, Field


class Post(BaseModel):
    id: int = Field(gt=0)
    userId: int = Field(gt=0)
    title: str = Field(min_length=1)
    body: str


def test_post_model():
    post = Post.model_validate(requests.get(f"{BASE}/posts/1", timeout=5).json())
    assert post.userId == 1
```

### Final code

**`schemas/post.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "userId", "title", "body"],
  "properties": {
    "id":     { "type": "integer", "minimum": 1 },
    "userId": { "type": "integer", "minimum": 1 },
    "title":  { "type": "string",  "minLength": 1 },
    "body":   { "type": "string" }
  },
  "additionalProperties": false
}
```

**`schema_check.py`**

```python
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


def assert_matches_schema(instance, name):
    schema = json.loads((SCHEMA_DIR / f"{name}.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=str)
    assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors)
```

**`test_contract.py`**

```python
import requests
from pydantic import BaseModel, Field
from schema_check import assert_matches_schema

BASE = "https://jsonplaceholder.typicode.com"


class Post(BaseModel):
    id: int = Field(gt=0)
    userId: int = Field(gt=0)
    title: str = Field(min_length=1)
    body: str


def test_get_post_matches_contract():
    assert_matches_schema(requests.get(f"{BASE}/posts/1", timeout=5).json(), "post")


def test_create_post_contract():
    payload = {"title": "QE", "body": "b", "userId": 1}
    assert_matches_schema({**payload, "id": 1}, "post")   # payload has the right shape
    created = requests.post(f"{BASE}/posts", json=payload, timeout=5).json()
    assert_matches_schema(created, "post")


def test_post_model():
    post = Post.model_validate(requests.get(f"{BASE}/posts/1", timeout=5).json())
    assert post.userId == 1
```

### How to run

```bash
cd week7-demos/05-1-contract
pytest -v -p no:randomly test_contract.py
```

### Checkpoint

The run shows `3 passed`. Now break the contract: in `schemas/post.json`, change `"title"` to `{"type": "integer"}`. The failure lists the exact path:

```
AssertionError: ['title']: 'sunt aut facere ...' is not of type 'integer'
```

Change it back afterwards.

### Your turn

1. Call `assert_matches_schema({"id": 0, "userId": "1", "title": "", "body": "x", "extra": 1}, "post")` in a test. How many errors are listed, and what are they?
2. Write `schemas/user.json` for `/users/1` that requires `id`, `name`, `email` and a nested `address` object that requires `city`.
3. Pass `{"id": "abc", "userId": 1, "title": "t", "body": "b"}` to `Post.model_validate` inside `pytest.raises(ValidationError)`. Print `str(excinfo.value)`.
4. JSONPlaceholder sometimes adds fields in the future. Which keyword would make your tests fail, and should you keep it?

### Common errors

- **The schema path breaks when you run PyTest from another folder.** Build the path from `Path(__file__)`, as in Step 2.
- **Using `validate()` and seeing only the first error.** Use `iter_errors` to see all of them at once.
- **Copying the schema from one response.** That locks in example values. Write the schema from the API documentation instead.

---

## Topic 2 – Data-Driven API Testing

📁 Folder: `05-2-ddt/`, file `test_ddt.py`

### Definition

**Data-driven testing (DDT)** separates **test logic** (the steps: send, then check) from **test data** (the inputs and expected outputs). One test function is written once and run once for each row of a data table. Adding a new scenario means adding a row, not writing another function. Good data tables cover **positive**, **negative** and **boundary** cases, and each row has a readable name, so a failure tells you exactly which row broke.

### Key ideas

| Column | Example | Why |
|--------|---------|-----|
| `case` (id) | `"title-empty"` | The readable test name in the report |
| inputs | `title`, `userId` | What you send |
| expected | `status`, `error_field` | What must come back |

- **Data sources, from simple to complex:** an inline list → a CSV or JSON file (Topic 3) → a database.
- **A builder (factory)** fills in default values, so each row only lists what is different about it.
- **Pitfalls:** hundreds of near-identical rows, rows that depend on each other, and shared mutable data.

### Worked example – A data table for `POST /posts`

**Step 1 – Write the data table.**

```python
import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"

CASES = [
    {"case": "valid",          "overrides": {},                   "status": 201},
    {"case": "long-title",     "overrides": {"title": "x" * 255}, "status": 201},
    {"case": "unicode-title",  "overrides": {"title": "Café ✓"},  "status": 201},
    {"case": "user-zero",      "overrides": {"userId": 0},        "status": 201},
]
```

**Step 2 – Add a builder so rows stay short.**

```python
def make_post(**overrides):
    payload = {"title": "default title", "body": "default body", "userId": 1}
    payload.update(overrides)
    return payload
```

**Step 3 – Write the logic once and feed it the rows.**

```python
@pytest.mark.parametrize("row", CASES, ids=[c["case"] for c in CASES])
def test_create_post(row):
    payload = make_post(**row["overrides"])
    r = requests.post(f"{BASE}/posts", json=payload, timeout=5)
    assert r.status_code == row["status"], f"{row['case']}: {r.text}"
```

**Step 4 – Add an echo check** so every row also checks the body.

```python
    if r.status_code == 201:
        for key, value in payload.items():
            assert r.json()[key] == value
```

### Final code

**`test_ddt.py`**

```python
import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"

CASES = [
    {"case": "valid",          "overrides": {},                   "status": 201},
    {"case": "long-title",     "overrides": {"title": "x" * 255}, "status": 201},
    {"case": "unicode-title",  "overrides": {"title": "Café ✓"},  "status": 201},
    {"case": "user-zero",      "overrides": {"userId": 0},        "status": 201},
]


def make_post(**overrides):
    payload = {"title": "default title", "body": "default body", "userId": 1}
    payload.update(overrides)
    return payload


@pytest.mark.parametrize("row", CASES, ids=[c["case"] for c in CASES])
def test_create_post(row):
    payload = make_post(**row["overrides"])
    r = requests.post(f"{BASE}/posts", json=payload, timeout=5)
    assert r.status_code == row["status"], f"{row['case']}: {r.text}"
    if r.status_code == 201:
        for key, value in payload.items():
            assert r.json()[key] == value
```

### How to run

```bash
cd week7-demos/05-2-ddt
pytest -v -p no:randomly test_ddt.py
```

### Checkpoint

```
test_ddt.py::test_create_post[valid] PASSED
test_ddt.py::test_create_post[long-title] PASSED
test_ddt.py::test_create_post[unicode-title] PASSED
test_ddt.py::test_create_post[user-zero] PASSED
```

> JSONPlaceholder accepts anything, so `user-zero` returns `201`. On a real API, the specification would say `400`, and that row would catch a missing validation bug.

### Your turn

1. Add two boundary rows: an empty title and a title of exactly one character. On a real API, what status would you expect for each?
2. Add a row that should fail on a real API and mark it with `pytest.param(..., marks=pytest.mark.xfail(reason="no validation on fake API"))`. (Hint: build the `argvalues` list with `pytest.param(row, id=row["case"])`.)
3. Run `pytest -v -k unicode`. How many tests run?
4. List two signs that a data table has grown too large and should be split.

---

## Topic 3 – CSV/JSON Parametrization

📁 Folder: `05-3-files/`

### Definition

**CSV/JSON parametrization** moves the data table out of the Python file into **external files** in a `data/` folder. This lets testers, business analysts or other tools edit the cases without touching code. **CSV** suits flat tables (one row per case, and every value is read as a string). **JSON** suits nested payloads and keeps real types such as numbers and booleans. A small **loader** module reads the files, cleans and converts the values, and turns each row into a test case with a readable id.

### Key ideas

| | CSV | JSON |
|---|---|---|
| Best for | Flat inputs | Nested payloads |
| Types | Everything is a `str`, so convert it | Real types are kept |
| Read with | `csv.DictReader` | `json.load` |

- **Locate files with `pathlib`**, relative to the loader file, so tests work from any folder.
- Open CSV files with `encoding="utf-8-sig"` (this removes the Excel BOM character) and `newline=""`.
- **Never put secrets** (passwords, tokens) in data files.

### Worked example – Loading cases from CSV and JSON

```
05-3-files/
├── data/
│   ├── posts_create.csv
│   └── users_create.json
├── data_loader.py
└── test_files.py
```

**Step 1 – Create `data/posts_create.csv`.**

```
case,title,body,user_id,status
valid,First post,Hello world,1,201
accent,Accent é title,Body ✓,2,201
long-body,Long body,Lorem ipsum dolor sit amet,3,201
```

**Step 2 – Write the loader** (`data_loader.py`).

```python
import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_csv(filename):
    with (DATA_DIR / filename).open(newline="", encoding="utf-8-sig") as f:
        return [row for row in csv.DictReader(f) if any(row.values())]


def load_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8-sig") as f:
        return json.load(f)
```

**Step 3 – Feed the CSV rows to a test and convert the strings** (`test_files.py`).

```python
import pytest
import requests
from data_loader import load_csv, load_json

BASE = "https://jsonplaceholder.typicode.com"
ROWS = load_csv("posts_create.csv")


@pytest.mark.parametrize("row", ROWS, ids=[r["case"] for r in ROWS])
def test_create_from_csv(row):
    payload = {"title": row["title"], "body": row["body"], "userId": int(row["user_id"])}
    r = requests.post(f"{BASE}/posts", json=payload, timeout=5)
    assert r.status_code == int(row["status"])
    assert r.json()["userId"] == payload["userId"]
```

**Step 4 – Add a JSON file for nested payloads** (`data/users_create.json`).

```json
[
  {"case": "full", "payload": {"name": "Ana", "address": {"city": "Reston"}}, "status": 201},
  {"case": "no-address", "payload": {"name": "Bo"}, "status": 201}
]
```

**Step 5 – Use the JSON rows.**

```python
USERS = load_json("users_create.json")


@pytest.mark.parametrize("row", USERS, ids=[u["case"] for u in USERS])
def test_create_user_from_json(row):
    r = requests.post(f"{BASE}/users", json=row["payload"], timeout=5)
    assert r.status_code == row["status"]
```

### Final code

**`data/posts_create.csv`**

```
case,title,body,user_id,status
valid,First post,Hello world,1,201
accent,Accent é title,Body ✓,2,201
long-body,Long body,Lorem ipsum dolor sit amet,3,201
```

**`data/users_create.json`**

```json
[
  {"case": "full", "payload": {"name": "Ana", "address": {"city": "Reston"}}, "status": 201},
  {"case": "no-address", "payload": {"name": "Bo"}, "status": 201}
]
```

**`data_loader.py`**

```python
import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_csv(filename):
    with (DATA_DIR / filename).open(newline="", encoding="utf-8-sig") as f:
        return [row for row in csv.DictReader(f) if any(row.values())]


def load_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8-sig") as f:
        return json.load(f)
```

**`test_files.py`**

```python
import pytest
import requests
from data_loader import load_csv, load_json

BASE = "https://jsonplaceholder.typicode.com"
ROWS = load_csv("posts_create.csv")
USERS = load_json("users_create.json")


@pytest.mark.parametrize("row", ROWS, ids=[r["case"] for r in ROWS])
def test_create_from_csv(row):
    payload = {"title": row["title"], "body": row["body"], "userId": int(row["user_id"])}
    r = requests.post(f"{BASE}/posts", json=payload, timeout=5)
    assert r.status_code == int(row["status"])
    assert r.json()["userId"] == payload["userId"]


@pytest.mark.parametrize("row", USERS, ids=[u["case"] for u in USERS])
def test_create_user_from_json(row):
    r = requests.post(f"{BASE}/users", json=row["payload"], timeout=5)
    assert r.status_code == row["status"]
```

### How to run

```bash
cd week7-demos/05-3-files
pytest -v -p no:randomly test_files.py
```

### Checkpoint

```
test_files.py::test_create_from_csv[valid] PASSED
test_files.py::test_create_from_csv[accent] PASSED
test_files.py::test_create_from_csv[long-body] PASSED
test_files.py::test_create_user_from_json[full] PASSED
test_files.py::test_create_user_from_json[no-address] PASSED
```

### Your turn

1. Add a blank line at the end of the CSV file and a row with an extra comma. What does the loader do with each?
2. Add a `flag` column (`xfail` or empty) and change the test to wrap flagged rows in `pytest.param(..., marks=pytest.mark.xfail)`.
3. Write a test that checks the data file itself: every row has a non-empty `case`, and the ids are unique.
4. Would you store a nested `address` object in CSV or JSON? Explain why.

### Common errors

- **`FileNotFoundError` when running from another folder.** The path must be built from `__file__`, not from the current folder.
- **`assert 201 == '201'`.** You forgot to convert a CSV string to an `int`.
- **`'﻿case'` as a column name.** The file has an Excel BOM, so open it with `utf-8-sig`.

---

## Topic 4 – Test Isolation

📁 Folder: `05-4-isolation/`, file `test_isolation.py`

### Definition

**Test isolation** means every test is **independent** (it does not need another test to run first), **order-independent** (it passes in any order), and **repeatable** (it gives the same result every run). Coupled tests share **state**, such as a global variable, a file, an environment variable or a record on the server. That causes the classic symptom "passes alone, fails in the suite" (or the other way round). Isolation comes from creating data per test, giving it a **unique** name, and **cleaning up** in a fixture's teardown.

### Key ideas

| Shared-state source | Isolation tool |
|---------------------|----------------|
| Module or global variables | Build data inside a function-scoped fixture |
| Environment variables | `monkeypatch.setenv` (undone automatically) |
| Files | `tmp_path` (a fresh folder for each test) |
| Records on the server | Unique names (`uuid4`) + `yield` cleanup |

- **Expose hidden coupling:** `pytest-randomly` shuffles test order on every run.
- **Other tools:** `pytest-xdist` (parallel runs) and `pytest-repeat` (repeat tests to catch flakiness).

### Worked example – Breaking and fixing isolation

**Step 1 – Write two coupled tests.**

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"
CREATED = {}


def test_a_create():
    CREATED["post"] = requests.post(f"{BASE}/posts",
                                    json={"title": "a", "body": "b", "userId": 1},
                                    timeout=5).json()


def test_b_uses_created():
    assert CREATED["post"]["id"] == 101
```

**Step 2 – Run test B on its own and watch it fail.**

```bash
pytest -q test_isolation.py::test_b_uses_created
```

**Step 3 – Fix it with a fixture**, so each test gets its own data. Replace both tests and `CREATED` with:

```python
import uuid
import pytest


@pytest.fixture
def created_post():
    title = f"iso-{uuid.uuid4().hex[:8]}"           # unique for every test
    post = requests.post(f"{BASE}/posts",
                         json={"title": title, "body": "b", "userId": 1}, timeout=5).json()
    yield post
    requests.delete(f"{BASE}/posts/{post['id']}", timeout=5)


def test_b_uses_created(created_post):
    assert created_post["id"] == 101
    assert created_post["title"].startswith("iso-")
```

**Step 4 – Isolate an environment variable with `monkeypatch`.**

```python
import os


def test_reads_base_url_from_env(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://staging.example.test")
    assert os.getenv("BASE_URL") == "https://staging.example.test"
    # monkeypatch restores the original value after the test
```

**Step 5 – Run twice to prove the tests pass in any order.**

```bash
pytest -v test_isolation.py
pytest -v test_isolation.py      # a different order, same result
```

### Final code

This is the fixed version, after Step 3 replaced the coupled tests.

**`test_isolation.py`**

```python
import os
import uuid

import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def created_post():
    title = f"iso-{uuid.uuid4().hex[:8]}"           # unique for every test
    post = requests.post(f"{BASE}/posts",
                         json={"title": title, "body": "b", "userId": 1}, timeout=5).json()
    yield post
    requests.delete(f"{BASE}/posts/{post['id']}", timeout=5)


def test_b_uses_created(created_post):
    assert created_post["id"] == 101
    assert created_post["title"].startswith("iso-")


def test_reads_base_url_from_env(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://staging.example.test")
    assert os.getenv("BASE_URL") == "https://staging.example.test"
    # monkeypatch restores the original value after the test
```

### How to run

```bash
cd week7-demos/05-4-isolation
pytest -v test_isolation.py
pytest -v test_isolation.py      # run again: the order changes, the result does not
```

### Checkpoint

- Step 2 fails with `KeyError: 'post'`.
- After Step 3, the same command passes: `1 passed`.
- Step 5 prints `Using --randomly-seed=NNNN` and shows **2 passed** on both runs, even though the order differs.

### Your turn

1. Write a test that writes `report.txt` into `tmp_path` and reads it back. Where on disk does the file go?
2. Find the coupling in this test: `def test_count(): assert len(requests.get(f"{BASE}/posts").json()) == 100`. When would it break on a **real** API, and how would you make it robust?
3. Run `pytest -q --randomly-seed=1234` twice. What is the point of a fixed seed?
4. A test passes alone but fails in the full suite. List the first three things you would check.

### Common errors

- **Using `autouse=True` to hide shared setup.** Every test pays for it, and the coupling becomes invisible.
- **Cleaning up at the end of the test body.** If an assertion fails first, the cleanup never runs. Put cleanup after `yield` instead.
- **Hard-coded names such as `"test_user"`.** Two parallel runs collide, so add a `uuid`.

---

## Answers

<details>
<summary><strong>Topic 1 – Request/Response Validation</strong></summary>

1. Four errors: `['id']` is less than the minimum of 1, `['userId']` `'1'` is not of type `integer`, `['title']` `''` is too short, and `[]` *Additional properties are not allowed ('extra' was unexpected)*.
2. ```json
   {
     "type": "object",
     "required": ["id", "name", "email", "address"],
     "properties": {
       "id": {"type": "integer"},
       "name": {"type": "string", "minLength": 1},
       "email": {"type": "string", "pattern": "^\\S+@\\S+$"},
       "address": {"type": "object", "required": ["city"],
                   "properties": {"city": {"type": "string"}}}
     }
   }
   ```
3. ```python
   from pydantic import ValidationError
   with pytest.raises(ValidationError) as excinfo:
       Post.model_validate({"id": "abc", "userId": 1, "title": "t", "body": "b"})
   print(str(excinfo.value))   # id: Input should be a valid integer ...
   ```
4. `additionalProperties: false`. Keep it only if the contract really forbids extra fields. For third-party APIs, `true` (the default) is usually safer.

</details>

<details>
<summary><strong>Topic 2 – Data-Driven API Testing</strong></summary>

1. On a real API, an empty title → `400`/`422`, and a one-character title → `201` (the minimum valid boundary).
2. ```python
   PARAMS = [pytest.param(c, id=c["case"]) for c in CASES] + [
       pytest.param({"case": "no-title", "overrides": {"title": None}, "status": 400},
                    id="no-title",
                    marks=pytest.mark.xfail(reason="no validation on fake API")),
   ]

   @pytest.mark.parametrize("row", PARAMS)
   def test_create_post(row): ...
   ```
3. **1** test (`unicode-title`).
4. Many rows differ only in values that don't change the behaviour being tested, and the rows test different behaviours that need different assertions.

</details>

<details>
<summary><strong>Topic 3 – CSV/JSON Parametrization</strong></summary>

1. The blank line is skipped by `if any(row.values())`. The extra comma puts the extra value under a `None` key, so a strict loader should raise an error for it.
2. ```python
   PARAMS = [
       pytest.param(r, id=r["case"],
                    marks=[pytest.mark.xfail(reason="flagged")] if r.get("flag") == "xfail" else [])
       for r in ROWS
   ]
   ```
3. ```python
   def test_csv_is_valid():
       ids = [r["case"] for r in load_csv("posts_create.csv")]
       assert all(ids)
       assert len(ids) == len(set(ids))
   ```
4. JSON. CSV has no way to represent a nested object, and JSON keeps the real types.

</details>

<details>
<summary><strong>Topic 4 – Test Isolation</strong></summary>

1. ```python
   def test_tmp(tmp_path):
       f = tmp_path / "report.txt"
       f.write_text("ok")
       assert f.read_text() == "ok"
   ```
   It goes into a unique temporary folder per test, for example `.../pytest-of-you/pytest-N/test_tmp0/`.
2. It assumes nobody else has created or deleted posts. On a shared real API, other tests or users change the count. A more robust test checks `len > 0` and validates the items, or it creates its own data and checks for that.
3. A fixed seed reproduces the **same** shuffled order, so you can debug an order-dependent failure.
4. Shared globals or class attributes, leftover server data or files from an earlier test, and environment variables or fixture scope (session or module data being changed).

</details>
