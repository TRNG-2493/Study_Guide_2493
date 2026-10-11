# Reading and Writing Files

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why file handling is essential in test automation.
- Open files with `open()` and choose the correct **mode** (`"r"`, `"w"`, `"a"`, `"x"`, `"r+"`, and the binary variants).
- Read a file in different ways: all at once (`read()`), line by line (iteration, `readline()`), or into a list (`readlines()`).
- Write and append text with `write()` and `writelines()`.
- Explain **encoding** (UTF-8) and why you should always specify it.
- Understand why files must be **closed**, and use `with` for automatic closing (previewed here; explored fully in *Context Managers*).
- Work with file paths safely using `os.path` and the modern `pathlib` module.
- Check whether files and folders exist, create folders, list directory contents, and delete files.
- Handle the common file-related exceptions (`FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `UnicodeDecodeError`).
- Read very large files efficiently, and understand file positions with `seek()` and `tell()`.

---

## Why This Matters

Almost every real test-automation task involves files:

- **Input:** test data (users, products, orders) stored in text, CSV, JSON or XML files.
- **Configuration:** environment settings such as URLs, browsers and timeouts.
- **Output:** test-result reports, logs, screenshots, exported data.
- **Evidence:** saved API responses, HTML snapshots and database dumps for investigating failures.

In the QE Foundations project you are building a **data-ingestion module**: a piece of code that reads test data from disk, checks it, and hands clean records to the rest of the system. Everything starts with being able to open, read and write a file correctly and safely.

Files are also where *things go wrong*: the file might not exist, might be locked, might use an unexpected character set, might be enormous, or might be half-written. That is why this lesson is paired with today's exception-handling lessons: reading a file is the classic situation that demands `try`/`except`.

On Monday you toured built-in modules like `os`; you will use that knowledge again here, alongside `pathlib`, another built-in module.

---

## The Concept

### 1. Text Files vs Binary Files

All files on disk are bytes. Python distinguishes two ways of looking at them:

- **Text mode** (the default): Python decodes bytes into **strings** (`str`) using an encoding, and converts line endings for you. Use it for `.txt`, `.csv`, `.json`, `.xml`, `.log`, `.py`, `.md` and so on.
- **Binary mode** (add `b` to the mode): you get raw **bytes** (`bytes`) with no decoding. Use it for images, PDFs, ZIP files, Excel workbooks, or anything not plain text.

This lesson focuses on text files, with a short section on binary at the end.

### 2. Opening a File with `open()`

```python
file = open("results.txt", "r", encoding="utf-8")
```

The `open()` function returns a **file object** (also called a *file handle*), which you use to read or write. The most important parameters:

| Parameter | Meaning |
|-----------|---------|
| `file` | Path to the file (a string or a `pathlib.Path`) |
| `mode` | What you want to do (default `"r"`, read text) |
| `encoding` | How to translate between bytes and characters (e.g. `"utf-8"`) |
| `newline` | How to handle line endings (use `newline=""` when working with CSV, covered later today) |

### 3. File Modes

| Mode | Name | Behaviour | If the file does not exist | If the file exists |
|------|------|-----------|----------------------------|--------------------|
| `"r"` | Read (default) | Read text; cannot write | `FileNotFoundError` | Opens at the start |
| `"w"` | Write | Write text | **Creates it** | **Erases all content**, then writes |
| `"a"` | Append | Write at the end | **Creates it** | Keeps content, adds to the end |
| `"x"` | Exclusive create | Write text | Creates it | `FileExistsError` (protects against overwriting) |
| `"r+"` | Read and write | Both | `FileNotFoundError` | Opens at the start, content kept |
| `"rb"`, `"wb"`, `"ab"` | Binary variants | Work with `bytes` | as above | as above |

> **Warning:** Mode `"w"` destroys existing content the instant you open the file, before you write anything. If you mean to add to a results file, use `"a"`. If you want to make sure you never overwrite by accident, use `"x"`.

### 4. Closing Files and Why It Matters

When you finish with a file you must **close** it:

```python
file = open("results.txt", "w", encoding="utf-8")
file.write("hello\n")
file.close()
```

Why?

1. **Data may still be sitting in a memory buffer.** Python (and the operating system) batch writes for speed. `close()` flushes everything to disk. Without it, your last few lines may never be saved.
2. **Resources are limited.** Each open file uses an operating-system handle. A test run that opens thousands of files without closing them can hit the limit ("Too many open files").
3. **Locks.** On some systems (Windows especially), an open file cannot be deleted or renamed by other programs.

If an exception occurs between `open()` and `close()`, the `close()` line is skipped. You saw in the previous lessons that `try`/`finally` can guarantee cleanup:

```python
file = open("results.txt", "w", encoding="utf-8")
try:
    file.write("hello\n")
finally:
    file.close()
```

This works, but it is verbose. Python provides a much better way: the **`with` statement**.

### 5. The `with` Statement (Preview)

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("hello\n")
# the file is automatically closed here, even if an error occurred
```

**How it reads:** "With this file open (call it `file`), do the following; when the indented block ends, close it automatically."

This is the **recommended way** to work with files. Use it in nearly every case. Later today the lesson on *Context Managers* explains exactly how `with` works and how you can build your own. For now, treat it as: *open + guaranteed close in one neat package*.

All the examples below use `with`.

### 6. Writing Text Files

**`write(text)`** writes a string and returns the number of characters written. It does **not** add a newline for you:

```python
with open("greeting.txt", "w", encoding="utf-8") as f:
    f.write("Hello, QA team!\n")
    f.write("Second line\n")
    f.write("Third line without newline at the end")
```

File content:

```
Hello, QA team!
Second line
Third line without newline at the end
```

`\n` is the **newline character**. Without it, the next `write` continues on the same line.

**`writelines(list_of_strings)`** writes each string in the list, again **without** adding newlines:

```python
lines = ["alpha\n", "beta\n", "gamma\n"]
with open("letters.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
```

**Using `print()` to write:** `print` accepts a `file=` argument and adds the newline automatically, which is convenient:

```python
with open("report.txt", "w", encoding="utf-8") as f:
    print("Test Report", file=f)
    print("=" * 11, file=f)
    print("Passed:", 8, file=f)
```

File content:

```
Test Report
===========
Passed: 8
```

**Writing non-strings:** `write()` accepts only strings. Convert numbers first:

```python
with open("count.txt", "w", encoding="utf-8") as f:
    f.write(str(42))          # f.write(42) would raise TypeError
    f.write("\n")
    f.write(f"pass rate: {66.6667:.1f}%\n")
```

**Appending:**

```python
with open("run_log.txt", "a", encoding="utf-8") as f:
    f.write("Run started\n")

with open("run_log.txt", "a", encoding="utf-8") as f:
    f.write("Run finished\n")
```

After both blocks, the file has two lines. Had we used `"w"` the second block would have erased the first line.

### 7. Reading Text Files

First create a sample file to read (`sample.txt`):

```python
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("id,name,status\n")
    f.write("1,Login,pass\n")
    f.write("2,Search,fail\n")
    f.write("3,Checkout,pass\n")
```

**`read()`: the whole file as one string**

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(type(content))
print(repr(content))
```

Output:

```
<class 'str'>
'id,name,status\n1,Login,pass\n2,Search,fail\n3,Checkout,pass\n'
```

`repr()` shows the hidden `\n` characters. `read(n)` reads only `n` characters.

**`readline()`: one line at a time**

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    first = f.readline()
    second = f.readline()

print(repr(first))     # 'id,name,status\n'
print(repr(second))    # '1,Login,pass\n'
```

Each call returns the next line, **including its trailing `\n`**. At the end of the file `readline()` returns an empty string `""`.

**`readlines()`: all lines as a list**

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(lines)
# ['id,name,status\n', '1,Login,pass\n', '2,Search,fail\n', '3,Checkout,pass\n']
```

**Iterating over the file: the best way for line-by-line processing**

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

Output:

```
id,name,status
1,Login,pass
2,Search,fail
3,Checkout,pass
```

A file object is **iterable**: the `for` loop asks for one line at a time. Python reads the file in small pieces, so even a 5 GB log file uses very little memory. `line.strip()` removes leading/trailing whitespace including the `\n`; otherwise `print` would add a second newline and produce blank lines between your rows.

Which to use?

| Method | Use when | Memory |
|--------|----------|--------|
| `for line in f:` | Processing line by line (default choice) | Very low |
| `f.read()` | The file is small and you need the whole text (e.g. JSON, covered next) | Whole file |
| `f.readlines()` | You need a list of lines and the file is small | Whole file |
| `f.readline()` | You need to read a header or a few lines manually | Very low |

**Splitting into lines without trailing newlines:**

```python
with open("sample.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()

print(lines)
# ['id,name,status', '1,Login,pass', '2,Search,fail', '3,Checkout,pass']
```

(When the mode is omitted, it defaults to `"r"`.)

### 8. Processing Lines: A Mini Parser

```python
passed = 0
failed = 0

with open("sample.txt", "r", encoding="utf-8") as f:
    header = f.readline()                     # skip the header row
    for line in f:                            # continues from line 2
        line = line.strip()
        if not line:                          # skip blank lines
            continue
        test_id, name, status = line.split(",")
        if status == "pass":
            passed += 1
        else:
            failed += 1

print(f"passed={passed} failed={failed}")
```

Output:

```
passed=2 failed=1
```

**Explanation:** `readline()` consumes the first line; the `for` loop then carries on from where the file position currently is. `line.split(",")` breaks a line into a list of strings at each comma, and we unpack it into three variables. (Real CSV data has quoting and edge cases; the `csv` module in the next lesson handles those properly, so use this hand-made approach only to understand the idea.)

### 9. Encoding: Always Say `utf-8`

A computer stores characters as numbers. An **encoding** defines the mapping. **UTF-8** is the modern universal standard, able to represent every language and symbol (`é`, `ü`, `日本語`, `€`, emoji).

If you omit `encoding`, Python uses a **platform-dependent default** (historically often a legacy encoding on Windows). A file written on one machine might then fail or show garbled characters on another. The fix is simple: **always write `encoding="utf-8"`.**

```python
with open("names.txt", "w", encoding="utf-8") as f:
    f.write("José\nZoë\n日本語\n")

with open("names.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

Reading with the wrong encoding fails or produces nonsense:

```python
try:
    with open("names.txt", "r", encoding="ascii") as f:
        f.read()
except UnicodeDecodeError as error:
    print("Decoding failed:", error)
```

Output (details may vary):

```
Decoding failed: 'ascii' codec can't decode byte 0xc3 in position 3: ordinal not in range(128)
```

If you must read a file with unknown or messy content, you can tell Python how to treat undecodable bytes with the `errors` parameter, for example `errors="replace"` (substitutes a placeholder) or `errors="ignore"` (drops them). Use these deliberately and note that they can hide data corruption.

Some files from Excel begin with an invisible "byte order mark" (BOM). Opening with `encoding="utf-8-sig"` removes it automatically; this is handy for CSV files exported from spreadsheets.

### 10. Newlines Across Operating Systems

Windows ends lines with `\r\n`; Linux and macOS use `\n`. In text mode, Python translates them to `\n` when reading and to the platform's convention when writing, so your code stays portable. (When working with the `csv` module you will pass `newline=""` to avoid interfering with this, as you will see in the CSV lesson.)

### 11. File Paths

A **path** says where a file lives.

- **Absolute path:** the full location from the root, e.g. `/home/qa/data/users.csv` (Linux/macOS) or `C:\Users\qa\data\users.csv` (Windows).
- **Relative path:** relative to the **current working directory** (the folder from which the program was started), e.g. `data/users.csv`.

A very common beginner problem: the script works in your editor but fails with `FileNotFoundError` when run from another folder, because the *working directory* differs. Check it with:

```python
import os
print(os.getcwd())
```

**Windows backslashes.** In a normal string, `\` begins an escape sequence: `"C:\new\test.txt"` contains a newline (`\n`) and a tab (`\t`)! Solutions: use forward slashes (Python accepts them on Windows), use a *raw string* `r"C:\new\test.txt"`, or (best) use `pathlib`.

### 12. `os.path`: the Classic Tools

```python
import os

path = os.path.join("data", "users.csv")     # builds 'data/users.csv' (or data\users.csv on Windows)
print(path)
print(os.path.exists(path))                   # True / False
print(os.path.isfile(path))
print(os.path.isdir("data"))
print(os.path.basename(path))                 # users.csv
print(os.path.dirname(path))                  # data
print(os.path.splitext("report.final.txt"))   # ('report.final', '.txt')
print(os.path.abspath(path))                  # full absolute path
```

`os.path.join` inserts the correct separator for the operating system; never join paths with `+ "/" +` by hand.

Other useful `os` functions:

```python
os.makedirs("output/reports", exist_ok=True)   # create nested folders; no error if they exist
print(os.listdir("."))                         # names of items in a folder
os.rename("old.txt", "new.txt")                # rename or move
os.remove("temp.txt")                          # delete a file
os.path.getsize("sample.txt")                  # size in bytes
```

### 13. `pathlib`: the Modern Way

`pathlib` represents paths as **objects**, which is neater and more readable. The `/` operator joins parts.

```python
from pathlib import Path

base = Path("data")
file_path = base / "users.csv"          # data/users.csv

print(file_path)
print(file_path.name)                   # users.csv
print(file_path.stem)                   # users
print(file_path.suffix)                 # .csv
print(file_path.parent)                 # data
print(file_path.exists())
print(file_path.is_file())
```

Convenience methods for reading and writing small files in one call:

```python
from pathlib import Path

p = Path("note.txt")
p.write_text("Hello from pathlib\n", encoding="utf-8")   # create/overwrite
print(p.read_text(encoding="utf-8"))                      # Hello from pathlib
```

Creating folders, listing and searching:

```python
from pathlib import Path

out = Path("output") / "reports"
out.mkdir(parents=True, exist_ok=True)       # like mkdir -p

(out / "a.txt").write_text("A", encoding="utf-8")
(out / "b.txt").write_text("B", encoding="utf-8")
(out / "c.log").write_text("C", encoding="utf-8")

for item in sorted(out.glob("*.txt")):        # wildcard search
    print(item.name)
```

Output:

```
a.txt
b.txt
```

A `Path` can be passed straight to `open()`:

```python
with open(out / "a.txt", encoding="utf-8") as f:
    print(f.read())
```

**Making a script independent of the working directory:** `__file__` holds the location of the current script. Combine it with `Path` to find data files that sit next to your code:

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent          # folder containing this script
DATA_FILE = HERE / "data" / "users.csv"
```

This is the professional way to avoid "works on my machine" path problems. (`__file__` is not defined in some interactive environments, such as the plain Python prompt; it works in scripts.)

### 14. Handling File Errors

File operations fail often. Here are the exceptions to expect (all are subclasses of `OSError`, which you met in the exception hierarchy):

| Exception | Cause |
|-----------|-------|
| `FileNotFoundError` | The file or a folder in the path does not exist |
| `PermissionError` | No rights to read/write that path |
| `IsADirectoryError` | You tried to open a folder as a file |
| `FileExistsError` | Mode `"x"` or `mkdir` on something already existing |
| `UnicodeDecodeError` | File bytes do not match the encoding (this one is a `ValueError`, not an `OSError`) |

A robust reading function:

```python
def read_text_file(path):
    """Return the text of a file, or None if it cannot be read."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
    except PermissionError:
        print(f"No permission to read: {path}")
    except IsADirectoryError:
        print(f"That is a directory, not a file: {path}")
    except UnicodeDecodeError as error:
        print(f"File is not valid UTF-8: {path} ({error.reason})")
    return None


print(read_text_file("does_not_exist.txt"))
print(read_text_file("."))
```

Output (the second line's result depends on the operating system; on Linux/macOS you see the directory message):

```
File not found: does_not_exist.txt
None
That is a directory, not a file: .
None
```

> In the demo and exercise you will go further and raise your own **custom exceptions** from a file reader, so callers see consistent, meaningful errors.

### 15. Reading Large Files Efficiently

Never `read()` a multi-gigabyte log into memory. Iterate:

```python
error_count = 0
with open("server.log", "r", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            error_count += 1
print("Errors found:", error_count)
```

Or read in fixed-size chunks (useful for binary files):

```python
CHUNK = 64 * 1024
total = 0
with open("big.bin", "rb") as f:
    while True:
        chunk = f.read(CHUNK)
        if not chunk:
            break
        total += len(chunk)
print("bytes:", total)
```

### 16. Binary Files

Add `b` to the mode. You read and write `bytes` objects, and you must not pass an `encoding`:

```python
data = bytes([72, 101, 108, 108, 111])     # the ASCII codes for "Hello"

with open("raw.bin", "wb") as f:
    f.write(data)

with open("raw.bin", "rb") as f:
    content = f.read()

print(content)             # b'Hello'
print(content.decode())    # Hello
```

A typical QE use: copying a screenshot or attachment byte-for-byte:

```python
with open("source.png", "rb") as src, open("copy.png", "wb") as dst:
    dst.write(src.read())
```

(Opening two files in one `with` statement by separating them with a comma is perfectly fine.) For copying files in practice, the built-in `shutil` module offers `shutil.copy("source.png", "copy.png")`.

### 17. The File Position: `tell()` and `seek()`

A file object remembers a **position**: where the next read or write takes place. Reading advances it.

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    print(f.tell())            # 0
    f.readline()
    print(f.tell())            # 15 (after the first line)
    f.seek(0)                  # jump back to the beginning
    print(f.readline().strip())  # id,name,status
```

That is why reading a file a second time returns nothing unless you `seek(0)` or reopen it:

```python
with open("sample.txt", encoding="utf-8") as f:
    first_pass = f.read()
    second_pass = f.read()      # empty: position is already at the end
print(len(first_pass), len(second_pass))   # 58 0
```

(The exact counts depend on the sample file's contents and line endings.)

---

## Real-World QA Scenarios

### Scenario 1: Writing a test-run report

```python
from datetime import datetime

results = [
    ("Login", "pass"),
    ("Search", "fail"),
    ("Checkout", "pass"),
]

with open("run_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Test run at {datetime.now():%Y-%m-%d %H:%M}\n")
    f.write("-" * 30 + "\n")
    for name, status in results:
        f.write(f"{name:<12} {status.upper()}\n")
    passed = sum(1 for _, status in results if status == "pass")
    f.write("-" * 30 + "\n")
    f.write(f"{passed}/{len(results)} passed\n")
```

The resulting file looks like:

```
Test run at 2025-06-03 14:05
------------------------------
Login        PASS
Search       FAIL
Checkout     PASS
------------------------------
2/3 passed
```

`datetime` (from Monday's tour of built-ins) formats the timestamp. `{name:<12}` left-aligns the name in a 12-character-wide column. `sum(1 for ... if ...)` counts the passes.

### Scenario 2: Searching a log file for failures

```python
from pathlib import Path

Path("app.log").write_text(
    "INFO start\nERROR db timeout\nINFO retry\nERROR db timeout\nWARN slow\n",
    encoding="utf-8",
)

errors = []
with open("app.log", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        if line.startswith("ERROR"):
            errors.append((number, line.strip()))

for number, text in errors:
    print(f"line {number}: {text}")
```

Output:

```
line 2: ERROR db timeout
line 4: ERROR db timeout
```

### Scenario 3: Loading a simple key=value configuration file

```python
from pathlib import Path

Path("settings.cfg").write_text(
    "# test settings\nbrowser=chrome\ntimeout=30\n\nbase_url=https://example.test\n",
    encoding="utf-8",
)

settings = {}
with open("settings.cfg", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):     # skip blanks and comments
            continue
        key, _, value = line.partition("=")      # split at the first '='
        settings[key.strip()] = value.strip()

print(settings)
```

Output:

```
{'browser': 'chrome', 'timeout': '30', 'base_url': 'https://example.test'}
```

`str.partition("=")` splits at the **first** `=` only and returns a 3-tuple `(before, separator, after)`. This is safer than `split("=")` because a URL value might itself contain `=`. Note that all values come back as strings; `timeout` would need `int(...)` before use.

### Scenario 4: Safely creating output folders and avoiding overwrite

```python
from pathlib import Path
from datetime import datetime

run_folder = Path("results") / datetime.now().strftime("run_%Y%m%d_%H%M%S")
run_folder.mkdir(parents=True, exist_ok=True)

try:
    with open(run_folder / "summary.txt", "x", encoding="utf-8") as f:   # "x" refuses to overwrite
        f.write("summary created\n")
except FileExistsError:
    print("Summary already exists, refusing to overwrite")
else:
    print("Wrote", run_folder / "summary.txt")
```

Each run gets its own timestamped folder, so earlier results are never lost: a good habit for test evidence.

---

## Code Examples: Putting It All Together

A utility that copies the "ERROR" lines from a log into a report and returns statistics, with careful error handling. Save as `log_filter.py`.

```python
"""log_filter.py - Extract error lines from a log file into a report."""

from pathlib import Path


def extract_errors(log_path, report_path):
    """Write every line containing 'ERROR' from log_path into report_path.

    Returns (lines_read, errors_found). Raises FileNotFoundError if
    the log does not exist.
    """
    lines_read = 0
    errors_found = 0

    with open(log_path, "r", encoding="utf-8") as log, \
         open(report_path, "w", encoding="utf-8") as report:
        for line in log:
            lines_read += 1
            if "ERROR" in line:
                errors_found += 1
                report.write(f"{lines_read}: {line}")
    return lines_read, errors_found


# --- demo ---
sample_log = Path("sample.log")
sample_log.write_text(
    "INFO boot\nERROR disk full\nINFO ok\nERROR timeout\n", encoding="utf-8"
)

try:
    read, found = extract_errors("sample.log", "errors_report.txt")
except FileNotFoundError as error:
    print("Cannot continue:", error)
else:
    print(f"Read {read} lines, found {found} errors")
    print(Path("errors_report.txt").read_text(encoding="utf-8"))

try:
    extract_errors("missing.log", "errors_report.txt")
except FileNotFoundError as error:
    print("Handled:", error.filename)
```

Output:

```
Read 4 lines, found 2 errors
2: ERROR disk full
4: ERROR timeout

Handled: missing.log
```

**Walkthrough:**

1. We open the input for reading and the output for writing in one `with` (the backslash continues the statement on the next line; wrapping the two items in parentheses is an alternative in modern Python).
2. The loop reads lazily line by line and counts them.
3. Because the line still contains its `\n`, `report.write(f"{lines_read}: {line}")` needs no extra newline.
4. If the log does not exist, `open` raises `FileNotFoundError` **before** the output file is created, and the caller handles it.
5. The function *returns* data and *raises* errors; it does not print: this keeps it reusable.

---

## Practice Exercises

**Exercise 1.** Write a program that creates `numbers.txt` containing the numbers 1 to 10, one per line, then reads it back and prints the sum.

**Exercise 2.** Append the line `"Run complete"` to a file `log.txt` three times, then print how many lines the file contains.

**Exercise 3.** Write `count_words(path)` that returns the number of words in a text file (hint: `str.split()` with no arguments splits on any whitespace). Handle a missing file by returning `0` and printing a message.

**Exercise 4.** Given a file `users.txt` with lines like `ada,36`, write code that builds a dictionary `{"ada": 36, ...}`, skipping blank lines.

**Exercise 5.** Using `pathlib`, create the folder structure `output/2025/reports`, write `index.txt` inside it, then print every `.txt` file found under `output` (hint: `rglob("*.txt")`).

**Exercise 6.** Explain what is wrong, and fix it:

```python
f = open("data.txt", "w")
f.write("score: " + 95)
f.close()
```

**Exercise 7.** Write `safe_copy(src, dst)` that copies a text file, refuses to overwrite an existing destination (use mode `"x"`), and returns `True` on success or `False` with a printed reason on failure.

### Answers

**Exercise 1:**

```python
with open("numbers.txt", "w", encoding="utf-8") as f:
    for n in range(1, 11):
        f.write(f"{n}\n")

total = 0
with open("numbers.txt", encoding="utf-8") as f:
    for line in f:
        total += int(line)
print(total)    # 55
```

**Exercise 2:**

```python
for _ in range(3):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("Run complete\n")

with open("log.txt", encoding="utf-8") as f:
    print(len(f.readlines()))     # 3 if the file was new
```

(If `log.txt` already existed, appending adds to its existing lines.)

**Exercise 3:**

```python
def count_words(path):
    try:
        with open(path, encoding="utf-8") as f:
            return len(f.read().split())
    except FileNotFoundError:
        print("File not found:", path)
        return 0
```

**Exercise 4:**

```python
ages = {}
with open("users.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        name, age = line.split(",")
        ages[name] = int(age)
print(ages)
```

**Exercise 5:**

```python
from pathlib import Path

folder = Path("output") / "2025" / "reports"
folder.mkdir(parents=True, exist_ok=True)
(folder / "index.txt").write_text("index\n", encoding="utf-8")

for p in Path("output").rglob("*.txt"):
    print(p)
```

**Exercise 6:** Two problems. `"score: " + 95` raises `TypeError` because you cannot add a string and an integer, and because the exception occurs before `f.close()` the file is never closed. Also the encoding is not given. Fixed:

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("score: " + str(95))
```

**Exercise 7:**

```python
def safe_copy(src, dst):
    try:
        with open(src, "r", encoding="utf-8") as source:
            text = source.read()
        with open(dst, "x", encoding="utf-8") as target:
            target.write(text)
    except FileNotFoundError:
        print("Source file not found:", src)
        return False
    except FileExistsError:
        print("Destination already exists, not overwriting:", dst)
        return False
    return True
```

---

## Summary / Key Takeaways

- Use `open(path, mode, encoding="utf-8")`. Modes: `"r"` read, `"w"` write (**erases**), `"a"` append, `"x"` create-only, add `"b"` for binary.
- Always close files. The best way is `with open(...) as f:`, which closes automatically even on errors (full explanation in *Context Managers* later today).
- Read with `for line in f` (best for most work and for large files), `read()`, `readline()`, `readlines()`. Write with `write()`, `writelines()` or `print(..., file=f)`; remember `write` needs strings and does not add newlines.
- Always specify `encoding="utf-8"`; use `"utf-8-sig"` for spreadsheet exports with a BOM.
- Build paths with `os.path.join` or, preferably, `pathlib.Path` and the `/` operator; anchor to your script with `Path(__file__).resolve().parent`.
- Expect failures: `FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `UnicodeDecodeError`. Catch them specifically.
- Next: **CSV, JSON and XML**: structured formats read through the same `open()` fundamentals, and handled with dedicated modules.

---

## Additional Resources

- Python Tutorial, "Reading and Writing Files": https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
- Python Library Reference, `pathlib`: https://docs.python.org/3/library/pathlib.html
- Python Library Reference, built-in `open()`: https://docs.python.org/3/library/functions.html#open
