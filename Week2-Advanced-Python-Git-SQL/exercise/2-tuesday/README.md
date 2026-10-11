# Exercise: Build the Data Ingestion Module (Week 2, Day 2 - Tuesday)

**Topic:** Exception Handling & File Processing  
**Mode:** A - Code Lab (individual)  
**Time:** 2 to 3 hours (a time-boxed plan is below)  
**You need:** Python 3.8+, your Monday `qe-foundations` repo with its `.venv`, Git. Standard library only. Nothing to `pip install`.

---

## Project 1 milestone: data ingestion module

> **Project 1 - QE Foundations.** On Monday you created the `qe-foundations` repository with the package `qe_foundations/` and the folders `utils/`, `tests/`, `data/` and `docs/`.
> **Today's milestone:** add the **data ingestion module** `qe_foundations/ingestion/`:
> - loaders for **CSV, JSON and XML** test data,
> - a **custom exception hierarchy** (`IngestionError`, `UnsupportedFormatError`, `RecordValidationError`, ...),
> - **context managers** for safe file handling,
> - **assertions** for internal invariants,
> - a **summary of valid vs rejected records** (plus a CSV file of the rejected ones).
>
> This module is the front door for all later Project 1 work. Wednesday you add logging and unit tests to it (and resolve a merge conflict on it), Thursday and Friday you validate the same data with SQL. **Keep the public names in this README exactly as written** so tomorrow's work fits.

## The scenario

Your team receives test cases and results from three places: spreadsheets (CSV), an API tool (JSON) and the CI server (XML). Real files are messy: missing columns, a stray BOM from Excel, a trailing comma, a duration of `n/a`. Your loader must **never crash on bad data and never silently accept it**. It must:

1. refuse an unusable *file* with a precise, catchable exception (and say why);
2. reject an unusable *record* but keep loading the others, remembering exactly what was wrong with each;
3. report a clear summary: how many records were seen, valid and rejected.

---

## Time-boxed plan

| # | Task | Minutes | You practise (Tuesday lessons) |
|---|------|--------:|--------------------------------|
| 1 | Set up: copy starter files, run the check, create a branch | 15 | Monday: venv, packages, Git |
| 2 | `exceptions.py`: the hierarchy | 25 | raising-and-creating-custom-exceptions |
| 3 | `contexts.py`: `open_source` and `LoadSession` | 25 | context-managers, reading-and-writing-files |
| 4 | `readers.py`: CSV, JSON, XML readers | 35 | csv-json-and-xml, try-except-else-and-finally |
| 5 | `validation.py`: `validate_record` | 25 | raising exceptions, assertions vs validation |
| 6 | `loader.py`: report, assertions, batch loading, rejected CSV | 30 | all of the above |
| 7 | Notes, Definition of Done, commit and push | 10 | Git, reflection |
| | **Total** | **165 (2 h 45)** | |
| | Stretch goals (optional) | +30 | |

If you are stuck for more than **10 minutes** on one item, read the next hint, then ask. Do not skip ahead: Task 4 needs Tasks 2 and 3; Task 6 needs everything.

---

## What you receive

```
starter_code/
|-- check_exercise.py                 <- self-check script (do not edit)
|-- qe_foundations/ingestion/         <- skeleton with TODOs
|   |-- __init__.py                   <- PROVIDED (public interface)
|   |-- __main__.py                   <- PROVIDED (command line runner)
|   |-- exceptions.py                 <- Task 2
|   |-- contexts.py                   <- Task 3
|   |-- readers.py                    <- Task 4
|   |-- validation.py                 <- Task 5
|   `-- loader.py                     <- Task 6
|-- data/ingestion/                   <- 14 sample files, several deliberately bad
`-- docs/ingestion_notes.md           <- four reflection questions (Task 7)
```

The skeleton assumes Monday's structure already exists in your repo:

```
qe-foundations/
|-- qe_foundations/        (with __init__.py, utils/, ...)
|-- tests/
|-- data/
|-- docs/
|-- requirements.txt, .gitignore, .venv/ (not committed)
```

> The starter does **not** contain `qe_foundations/__init__.py`. It is already in your repo from Monday, and the starter must not overwrite it.

---

## Task 1 - Set up (15 min)

Open a terminal **in your `qe-foundations` folder** and activate the virtual environment.

| Step | PowerShell (Windows) | bash / zsh (macOS, Linux, Git Bash) |
|------|----------------------|--------------------------------------|
| Go to repo | `cd C:\path\to\qe-foundations` | `cd ~/path/to/qe-foundations` |
| Activate venv | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` (Git Bash on Windows: `source .venv/Scripts/activate`) |
| Latest main | `git switch main` then `git pull` | same |
| Work branch | `git switch -c feature/data-ingestion` | same |
| Where is the starter? | `$Starter = "C:\path\to\2-tuesday\starter_code"` | `STARTER=~/path/to/2-tuesday/starter_code` |
| Copy the module | `Copy-Item -Recurse "$Starter\qe_foundations\ingestion" .\qe_foundations\` | `cp -r "$STARTER/qe_foundations/ingestion" qe_foundations/` |
| Copy sample data | `Copy-Item -Recurse "$Starter\data\ingestion" .\data\` | `cp -r "$STARTER/data/ingestion" data/` |
| Copy notes + checker | `Copy-Item "$Starter\docs\ingestion_notes.md" .\docs\`<br>`Copy-Item "$Starter\check_exercise.py" .` | `cp "$STARTER/docs/ingestion_notes.md" docs/`<br>`cp "$STARTER/check_exercise.py" .` |

Then look around and run the checker. **It should fail almost everything.** That is the starting line.

| | PowerShell | bash |
|---|---|---|
| See the structure | `Get-ChildItem qe_foundations\ingestion` | `ls qe_foundations/ingestion` |
| Run the self-check | `python check_exercise.py` | `python3 check_exercise.py` |
| Run the CLI (will fail until Task 6) | `python -m qe_foundations.ingestion data\ingestion\test_cases_clean.csv` | `python3 -m qe_foundations.ingestion data/ingestion/test_cases_clean.csv` |

(On Windows, if `python` opens the Microsoft Store, use `py` instead. Inside the activated venv `python` is correct.)

**Rules for sample files:** do **not** open and re-save the files in `data/ingestion/` with an editor. Some are deliberately broken at byte level (a BOM, a Latin-1 character). Re-saving "fixes" them and destroys the test.

**Done when:** the checker runs and prints a list of FAIL lines, you are on branch `feature/data-ingestion` (`git branch --show-current`).

### The sample data (what each file is for)

| File | Contains | What your loader should do |
|------|----------|----------------------------|
| `test_cases_clean.csv` | 5 good rows | 5 valid |
| `test_cases_excel_bom.csv` | Excel "CSV UTF-8" file: BOM + CRLF | 3 valid (the BOM must not break the `id` column) |
| `test_cases_messy.csv` | 10 rows, 7 of them bad in different ways | 3 valid, 7 rejected |
| `test_cases_missing_column.csv` | no `duration` column | `MissingColumnsError` |
| `test_cases_empty.csv` | 0 bytes | `MissingColumnsError` (no header at all) |
| `test_cases_latin1.csv` | saved as Latin-1, not UTF-8 | `MalformedSourceError` |
| `test_results_clean.json` | 4 good tests | 4 valid |
| `test_results_messy.json` | 8 items: a missing key, `null`, `true`, a bare string, a numeric id... | 3 valid, 5 rejected |
| `test_results_malformed.json` | trailing comma | `MalformedSourceError` (with line number) |
| `test_results_wrong_shape.json` | a bare list instead of `{"tests": [...]}` | `MalformedSourceError` |
| `test_results_clean.xml` | 3 good testcases | 3 valid |
| `test_results_messy.xml` | two suites inside `<testsuites>`, 4 bad testcases | 2 valid, 4 rejected |
| `test_results_malformed.xml` | an unclosed `<duration>` tag | `MalformedSourceError` |
| `notes.txt` | not test data | `UnsupportedFormatError` |

When everything works, loading the whole folder gives: **7 files OK, 7 files failed, 23 valid, 16 rejected.**

> The checker uses **different** bad files from the ones above (it generates them on the fly). Passing the sample files is not enough: handle the *kind* of problem, not just the file.

---

## The data contract (shared by all three formats)

A **test case** has four required fields:

| Field | Rule |
|-------|------|
| `id` | required, not blank. Whitespace around it is trimmed. A number (JSON `708`) becomes the string `"708"`. Must be unique within one file. |
| `title` | required, not blank. Trimmed. |
| `status` | required. After trimming and lower-casing it must be one of `pass`, `fail`, `blocked`. (`PASS` is fine; `passed` is not.) |
| `duration` | required. Seconds, as a **finite** number `>= 0`. Strings like `"1.7"` and `"1e2"` are accepted and converted to `float`. `n/a`, `-4`, `nan`, `inf`, JSON `true` are rejected. |

Formats:

| Format | Where the records are |
|--------|-----------------------|
| CSV | header line `id,title,status,duration`, one record per line |
| JSON | `{"suite": "...", "tests": [ {record}, {record}, ... ]}` |
| XML | every `<testcase id="..." status="...">` element **at any depth**, with `<title>` and `<duration>` child elements |

**Row numbers** are 1-based positions among the records (CSV: the header line does *not* count; JSON: position in `tests`; XML: document order).

## The error policy (the idea of the whole milestone)

| Problem | Meaning | What the code does |
|---------|---------|--------------------|
| `SourceError` family | The **file** is unusable (not found, not UTF-8, malformed, wrong columns, unsupported type) | **raise** it; stop loading that file |
| `RecordValidationError` family | **One record** is bad | **collect** it in the report; keep loading |
| `AssertionError` | A bug **in your own code** (the bookkeeping is inconsistent) | let it crash loudly; never use `assert` to check input data |

---

## Task 2 - The exception hierarchy (25 min)  `exceptions.py`

Open `qe_foundations/ingestion/exceptions.py`. Four classes are already written and show the pattern. Complete the others.

```
IngestionError
+-- SourceError(path, detail)                  .path  .detail
|   +-- SourceNotFoundError(path)              (given)
|   +-- SourceUnreadableError(path, os_error)  message names the OS error class
|   +-- UnsupportedFormatError(path, suffix)   .suffix
|   +-- MalformedSourceError(path, detail)
|   `-- MissingColumnsError(path, missing)     .missing (a list)
`-- RecordValidationError(row, field, msg)     .row  .field   message starts "Row N: ..."
    +-- MissingFieldError(row, field)
    +-- InvalidValueError(row, field, value, expected)   .value  .expected
    `-- DuplicateIdError(row, test_id)         .test_id ; field is "id"
```

**Requirements**
- Exactly this tree. `SourceError` and `RecordValidationError` are **siblings**.
- Messages are human-readable and contain the file name (source errors) or `Row N` and the field (record errors).
- No bare `pass` should remain in a class that needs attributes.

<details><summary>Hint 1 - where to look</summary>

Re-read `raising-and-creating-custom-exceptions.md`, the sections on adding attributes (section 8) and on designing a hierarchy with one base class (section 12). Look at how `SourceNotFoundError` calls `super().__init__`.
</details>

<details><summary>Hint 2 - the pattern</summary>

Each subclass `__init__` (a) stores its own extra attributes on `self`, then (b) calls the parent's `__init__` with arguments that build the message. A class that needs no extra data, such as `MalformedSourceError`, does not need an `__init__` at all.
</details>

<details><summary>Hint 3 - one worked class</summary>

```python
class UnsupportedFormatError(SourceError):
    def __init__(self, path, suffix):
        self.suffix = suffix
        super().__init__(path, f"unsupported file type {suffix!r} (use .csv, .json or .xml)")
```
Write the other six in the same style.
</details>

**Self-check:** `python check_exercise.py` (Task 2 section should be 4/4).

---

## Task 3 - Context managers (25 min)  `contexts.py`

### 3A. `open_source(path)` - a generator-based context manager

```python
with open_source("data/ingestion/test_cases_clean.csv") as handle:
    text = handle.read()
```

**Requirements**
1. Opens the file for reading with `encoding="utf-8-sig"` (a UTF-8 file, **without** the BOM that Excel adds) and `newline=""` (what the `csv` module wants).
2. A file that does not exist -> `SourceNotFoundError`.
3. Any other `OSError` while opening (it is a folder, permission denied, ...) -> `SourceUnreadableError`.
4. If reading the text later fails with `UnicodeDecodeError` (the `with` body raises it) -> `MalformedSourceError`.
5. The original error is kept as `__cause__` (`raise ... from error`).
6. The file is **always** closed, also when the body raises, and other exceptions from the body are **not** swallowed.

<details><summary>Hint 1</summary>

`FileNotFoundError` is a *child* of `OSError`. In a list of `except` clauses Python uses the first one that matches (try-except-else-and-finally.md, section 7). Which must come first?
</details>

<details><summary>Hint 2</summary>

Two separate `try` blocks: one around `open(...)` (translate `OSError`s), one around `yield handle` (translate `UnicodeDecodeError`, and `finally: handle.close()`). The decoding error happens *later*, when somebody calls `.read()`, so it surfaces at the `yield`.
</details>

<details><summary>Hint 3 - skeleton</summary>

```python
@contextmanager
def open_source(path):
    try:
        handle = open(path, encoding=..., newline=...)
    except FileNotFoundError as error:
        raise ... from error
    except OSError as error:
        raise ... from error
    try:
        yield handle
    except UnicodeDecodeError as error:
        raise MalformedSourceError(path, "...") from error
    finally:
        handle.close()
```
Delete the `raise NotImplementedError(...)` and the dummy `yield` that the starter contains.
</details>

### 3B. `LoadSession(path)` - a class-based context manager

Records how a load went. After the `with` block ends:
- `session.outcome` is `"completed"` or `"failed"`;
- `session.elapsed` is the number of seconds the block took (a `float`, `>= 0`; use `time.perf_counter()`);
- an exception raised inside the block **keeps propagating** (`__exit__` must not swallow it).

<details><summary>Hint</summary>

`__enter__` records the start time and returns `self`. `__exit__(self, exc_type, exc_value, traceback)` receives `exc_type = None` when the block succeeded. Return `False` to let an exception continue (context-managers.md, section 5).
</details>

**Self-check:** Task 3 section 7/7.

---

## Task 4 - Readers (35 min)  `readers.py`

Each reader takes a path, opens it **with `open_source`**, and returns a **list of raw records**. Readers deal only with *format* problems. They do not check statuses or durations, and they do not convert types (a CSV `1.5` stays the string `"1.5"`).

| Reader | Returns | Raises `MalformedSourceError` / other when |
|--------|---------|--------------------------------------------|
| `read_csv_records(path)` | one `dict` per data row (`csv.DictReader`) | `MissingColumnsError(path, missing)` if any of the four required columns is absent from the header (`missing` in the order `id,title,status,duration`); an **empty file** has no header, so all four are missing. A header-only file returns `[]`. |
| `read_json_records(path)` | the list stored under `"tests"`, **untouched** (even if an item is not an object) | invalid JSON (message includes `line` and `column`); the top level is not an object; `"tests"` is missing or not a list; an empty file |
| `read_xml_records(path)` | one dict per `<testcase>` at any depth: `{"id", "status", "title", "duration"}`. `id` and `status` come from **attributes**, `title` and `duration` from **child elements**. Anything absent is `None`. | the XML is not well-formed (message includes line and column); an empty file |

Also: a CSV row with too few fields must **not** crash the reader: return it, and let validation reject it. Bad encoding in a CSV or JSON file must surface as `MalformedSourceError` (your `open_source` already does that). Keep the original parser error as `__cause__`.

<details><summary>Hint 1 - CSV</summary>

`csv.DictReader(handle)` exposes the header as `reader.fieldnames` (it is `None` for an empty file). Compare it to `REQUIRED_FIELDS` (imported from `validation.py`). See csv-json-and-xml.md, sections 1.4 and 1.7.
</details>

<details><summary>Hint 2 - JSON and XML</summary>

`json.load(handle)` raises `json.JSONDecodeError`, which has `.lineno` and `.colno`. `ET.parse(handle)` raises `ET.ParseError`, whose `.position` is a `(line, column)` tuple. Wrap each in `try/except ... as error` and `raise MalformedSourceError(...) from error`. Do the shape checks *after* the `with` block, once the file is closed (csv-json-and-xml.md, sections 2.7 and 3.5).
</details>

<details><summary>Hint 3 - XML</summary>

```python
root = ET.parse(handle).getroot()
for case in root.iter("testcase"):          # iter() = this tag at ANY depth
    case.get("id")                          # attribute -> None if absent
    case.findtext("title")                  # child text -> None if the tag is absent
```
`root.findall("testcase")` only finds *direct* children, which is not enough for `test_results_messy.xml`.
</details>

**Self-check:** Task 4 section 11/11. Quick manual look, e.g. in the REPL:

| PowerShell / bash (venv active) |
|---|
| `python -c "from qe_foundations.ingestion.readers import read_xml_records as r; print(r('data/ingestion/test_results_messy.xml'))"` |

(On macOS/Linux outside a venv use `python3`. In PowerShell the double quotes in that command are fine as written.)

---

## Task 5 - Validate one record (25 min)  `validation.py`

`validate_record(row, raw)` returns a clean dict `{"id": str, "title": str, "status": str, "duration": float}` or raises a `RecordValidationError` subclass. It must **not modify** `raw`.

Checks, **in this order** (the first problem found is the one reported):

1. `raw` is not a `dict` (e.g. the bare string `"TC-707"` in JSON) -> `InvalidValueError(row, "record", raw, ...)`.
2. For each of `id`, `title`, `status`, `duration` in that order: absent, `None`, empty or whitespace-only -> `MissingFieldError`.
3. `status` (trimmed, lower-cased) not in `VALID_STATUSES` -> `InvalidValueError` for field `"status"`.
4. `duration`: a `bool`, not convertible to a number, `nan`, `inf`, or negative -> `InvalidValueError` for field `"duration"`.

**Important:** these are validations of *external data*, so you **raise exceptions**. Do not use `assert` in this file. The checker even re-runs your code with `python -O`, which switches assertions off, to prove it.

<details><summary>Hint 1</summary>

Guard clauses: check what is wrong first, `raise` early, and let the happy path run straight down at the end (raising-and-creating-custom-exceptions.md, section 13). Re-read assertions.md, section 6: "assertions vs exceptions".
</details>

<details><summary>Hint 2 - traps the checker knows about</summary>

- `float("nan")` and `float("inf")` do **not** raise `ValueError`. The standard `math` module has a function that tells you whether a float is finite.
- `True` is an `int` in Python (`isinstance(True, int)` is `True`), so `float(True)` happily returns `1.0`. Decide explicitly.
- `float([])` raises `TypeError`, not `ValueError`. Catch both.
- Keep the original error as the cause: `raise InvalidValueError(...) from error`.
</details>

<details><summary>Hint 3 - skeleton</summary>

```python
def validate_record(row, raw):
    if not isinstance(raw, dict):
        raise InvalidValueError(row, "record", raw, "an object with the test fields")
    for name in REQUIRED_FIELDS:
        value = raw.get(name)
        if value is None or str(value).strip() == "":
            raise MissingFieldError(row, name)
    status = str(raw["status"]).strip().lower()
    ...                      # status rule
    ...                      # duration rule (try/except + finiteness + sign)
    return {...}
```
</details>

**Self-check:** Task 5 section 8/8.

---

## Task 6 - Put it together (30 min)  `loader.py`

The classes `IngestionReport` and `BatchResult` exist; their methods are TODOs.

### 6A. `IngestionReport.summary()` and `.rejected_rows()`
- `summary()` returns exactly: `test_cases_messy.csv: 10 rows seen, 3 valid, 7 rejected`.
- `rejected_rows()` returns a list of dicts with the keys `source`, `row`, `field`, `reason` (`reason = str(error)`), ordered by row number.

### 6B. `IngestionReport.check_invariants()` - assertions for internal invariants
Write three `assert` statements, each with a helpful message:
1. `len(valid) + len(rejected) == rows_seen`
2. no duplicate ids in `valid`
3. everything in `rejected` is a `RecordValidationError`

These can only fail if **your own code** is wrong. That is what assertions are for (assertions.md, sections 6 and 7).

### 6C. `load_test_cases(path)`
1. Wrap the whole job in `with LoadSession(path):`.
2. Pick the reader from `READERS` using the lower-cased suffix. No reader -> `UnsupportedFormatError`.
3. Call the reader. Any `SourceError` must propagate unchanged.
4. For each record (numbering from 1): `validate_record`; if the id was already seen **earlier in this file**, raise `DuplicateIdError` for the later one (the first stays valid).
5. A `RecordValidationError` is caught and appended to `report.rejected`; a good record goes to `report.valid`.
6. Call `report.check_invariants()`, then return the report.
7. It accepts `str` or `Path`. Extensions like `.CSV` work.

<details><summary>Hint 1</summary>

The try/except/else shape from try-except-else-and-finally.md (section 8, "else = success path"): `try:` validate and check the duplicate; `except RecordValidationError as error:` collect it; `else:` remember the id and keep the clean record. Only catch the *record* family here. Catching `IngestionError` would also swallow file-level errors raised inside the loop's helpers.
</details>

<details><summary>Hint 2</summary>

`seen_ids = set()` before the loop. Use `enumerate(raw_records, start=1)` to get row numbers.
</details>

### 6D. `load_directory(folder)` and `BatchResult.totals()`
- Loads every **file** directly inside `folder` in sorted-name order. Sub-folders are skipped.
- A bad **file** never stops the batch: catch its `SourceError` and append it to `failed_sources`; good files' reports go to `reports`.
- A folder that does not exist -> `SourceNotFoundError(folder)`.
- `totals()` returns `{"files_ok": ..., "files_failed": ..., "valid": ..., "rejected": ...}`.

### 6E. `write_rejected_csv(report, out_path)`
Writes `report.rejected_rows()` with `csv.DictWriter`. Header exactly `source,row,field,reason`. Creates missing parent folders, opens the file with `newline=""` (otherwise Windows adds a blank line between rows), returns the `Path`. No rejected records -> header only.

<details><summary>Hint (6E)</summary>

`out_path.parent.mkdir(parents=True, exist_ok=True)`, then `with open(out_path, "w", encoding="utf-8", newline="") as handle:` and `writer.writeheader()` / `writer.writerows(...)` (reading-and-writing-files.md; csv-json-and-xml.md, section 1.5).
</details>

### Try it for real
| | PowerShell | bash |
|---|---|---|
| One file | `python -m qe_foundations.ingestion data\ingestion\test_cases_messy.csv` | `python3 -m qe_foundations.ingestion data/ingestion/test_cases_messy.csv` |
| Whole folder | `python -m qe_foundations.ingestion data\ingestion` | `python3 -m qe_foundations.ingestion data/ingestion` |

Expected tail for the whole folder: `TOTAL for ingestion: {'files_ok': 7, 'files_failed': 7, 'valid': 23, 'rejected': 16}`.
The CLI exits with `0` when every file was readable (rejected *records* are not a failure) and `1` when at least one file failed.

**Self-check:** Task 6 section 11/11 and Task 7 section.

---

## Task 7 - Notes, Definition of Done, commit and push (10 min)

1. Answer the four questions in `docs/ingestion_notes.md` (2 to 4 sentences each, your own words). Remove every `TODO:` line.
2. Run `python check_exercise.py` (add `-v` to see tracebacks). All **core** checks must pass.
3. Tick every box in the Definition of Done below.
4. Commit and push:

| | PowerShell | bash |
|---|---|---|
| Review | `git status` | `git status` |
| Stage only your work | `git add qe_foundations/ingestion data/ingestion docs/ingestion_notes.md` | same |
| Check what is staged | `git status` | `git status` |
| Commit | `git commit -m "Add data ingestion module with custom exceptions and CSV/JSON/XML loaders"` | same |
| Push your branch | `git push -u origin feature/data-ingestion` | same |

- Do **not** `git add .` blindly: `check_exercise.py`, `.venv/`, `__pycache__/` and any `rejected*.csv` you produced should not be committed.
- Windows may print `warning: LF will be replaced by CRLF`. That is normal.
- If the push is rejected, run `git pull` and push again (Monday's collaborative workflow).
- Push the **branch**. Whether to merge it into `main` is decided in class: tomorrow's session starts from this module, so keep your public names unchanged.

---

## Definition of Done

- [ ] `python check_exercise.py` reports **all core checks passed** (stretch checks are optional)
- [ ] `python -m qe_foundations.ingestion data/ingestion` prints 7 files OK / 7 failed / 23 valid / 16 rejected
- [ ] The exception tree matches the diagram; no bare `except:`; every translated error uses `raise ... from error`
- [ ] Every `open()` is inside a `with` (or hidden in `open_source`)
- [ ] Validation uses exceptions; `assert` appears **only** for internal invariants (`check_invariants`)
- [ ] Library modules do not `print` (only `__main__.py` does). No `logging` yet: that is Wednesday
- [ ] Functions have a one-line docstring; names follow PEP 8; no leftover `TODO` or `NotImplementedError`
- [ ] `docs/ingestion_notes.md` is answered
- [ ] Work is on `feature/data-ingestion`, committed with a meaningful message, and **pushed**
- [ ] `git status` is clean; `.venv/` and `__pycache__/` are not tracked

---

## Stretch goals (optional, about 30 min)

Run `python check_exercise.py --stretch` to check the first two.

1. **Strict mode.** `load_test_cases(path, strict=False)`. With `strict=True` the *first* `RecordValidationError` is raised instead of collected.
2. **Error budget.** Add `TooManyErrorsError(IngestionError)` with `.source`, `.limit` and `.count`. `load_test_cases(path, max_errors=N)` raises it as soon as more than `N` records have been rejected (exactly `N` is allowed; `None` means unlimited).
3. **Prove the assertion rule.** Run `python -O -c "..."` against `check_invariants` with an inconsistent report and see nothing happen. Write two sentences in your notes: why is that acceptable for invariants but not for validation?
4. **A third context manager.** `temp_fixture(filename, content)` that writes a temporary file, yields its path and always deletes it, and use it to try your own nastiest input file.

---

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `ModuleNotFoundError: No module named 'qe_foundations'` | You are not in the repo root, or the package folder is missing `__init__.py` from Monday. `cd` to the repo root. |
| `ImportError: attempted relative import with no known parent package` | You ran a module as a script (`python loader.py`). Run it as `python -m qe_foundations.ingestion ...` from the repo root. |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, or call `.venv\Scripts\python.exe` directly (Monday's lesson). |
| First CSV column is called `\ufeffid` | You opened the file without `encoding="utf-8-sig"`. |
| Blank line between rows in the rejected CSV | Missing `newline=""` in `open()`. |
| `UnicodeDecodeError` escapes as a raw traceback | Translate it into `MalformedSourceError` inside `open_source`. |
| Checker says "unfinished: `raise NotImplementedError` still present" | Delete that line in every function you have implemented. |
| `check_exercise.py: cannot find qe_foundations/ingestion` | Run it from the repo root, or `python check_exercise.py --repo <path>`. |

---

## Grading rubric (100 points, +10 bonus)

| Category | Points | How it is graded |
|----------|-------:|------------------|
| **Behaviour** (automatic) | 50 | `check_exercise.py`: `50 x passed core checks / total core checks` |
| **Exception design and handling** | 15 | Tree matches the spec (4); specific `except` clauses in the right order, no bare/swallowing handlers (4); `raise ... from` preserves causes (4); SourceError-vs-RecordValidationError policy applied correctly (3) |
| **Files and context managers** | 10 | `with` everywhere; correct encoding and `newline`; `open_source` and `LoadSession` clean and reusable |
| **Assertions vs validation** | 5 | `assert` only for the invariants, with messages; no `assert` validating input |
| **Code quality** | 5 | Readable, PEP 8 names, docstrings, no dead code or leftover TODOs |
| **Git submission** | 10 | Branch `feature/data-ingestion`; focused commit(s) with a clear message; only relevant files; pushed; no `.venv`/`__pycache__` tracked |
| **Reflection notes** | 5 | All four answers present, specific, in the trainee's own words |
| **Stretch goals** (bonus) | up to +10 | 5 points each for stretch 1 and 2 (checker-verified); 0 for others unless the reviewer sees sound work |

Bands: 90+ excellent; 75-89 solid, ready for Wednesday; 60-74 review the failing task before tomorrow; below 60 see the instructor for a catch-up session.

---

## Next steps in Project 1 (do not build these today)

- **Wednesday:** add logging and unit tests to `qe_foundations/ingestion/`, plus a merge conflict on this module to resolve.
- **Thursday / Friday:** load the valid records into SQL tables, validate them with queries and joins.
