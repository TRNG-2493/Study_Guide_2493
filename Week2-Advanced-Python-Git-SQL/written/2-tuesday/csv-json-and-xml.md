# CSV, JSON and XML

## Learning Objectives

By the end of this lesson you will be able to:

- Describe what CSV, JSON and XML are, how each is structured, and the strengths and weaknesses of each.
- Choose the right format for a given kind of test data.
- Read and write CSV with the `csv` module using both `reader`/`writer` (lists) and `DictReader`/`DictWriter` (dictionaries).
- Explain why `newline=""` is used with CSV files and what a delimiter and quoting are.
- Read, parse and write JSON with the `json` module (`load`, `loads`, `dump`, `dumps`), and map JSON types to Python types.
- Handle malformed JSON (`json.JSONDecodeError`).
- Parse XML with `xml.etree.ElementTree`: navigate elements, attributes and text, search with `find`/`findall`, and build and write XML.
- Convert data between the three formats.
- Validate and clean data read from these formats, and handle bad input robustly using the exception techniques from earlier today.
- Be aware of basic safety considerations when parsing untrusted XML.

---

## Why This Matters

Test data and test results do not live inside Python code. They arrive as files and responses in a handful of standard formats:

| Format | Where QEs meet it |
|--------|-------------------|
| **CSV** | Spreadsheet exports, bulk test data (hundreds of users/orders), database exports, data-driven testing tables |
| **JSON** | REST API requests and responses, configuration files, modern test-data fixtures, test reports |
| **XML** | Older web services (SOAP), configuration files, test-result reports (a very common report format in CI tools), Android/Java ecosystem files |

A data-driven test suite can run the *same* test logic across 500 rows of data. Reading those rows reliably is the **data ingestion** step, which is the Project 1 milestone for today. Real-world files are messy: missing columns, blank cells, wrong types, odd characters. This lesson shows the tools Python provides, and combines them with your exception-handling skills to read them defensively.

Yesterday's lessons on modules paid off here: `csv`, `json` and `xml.etree.ElementTree` are all **built-in modules**. There is nothing to `pip install`.

---

## The Concept

## Part 1: CSV (Comma-Separated Values)

### 1.1 What is CSV?

A CSV file is plain text where each line is a **row** and values within a row are separated by a **delimiter** (usually a comma). The first row is usually a **header** naming the columns.

`users.csv`:

```
id,name,email,age,active
1,Ada Lovelace,ada@example.com,36,true
2,Grace Hopper,grace@example.com,45,true
3,Alan Turing,alan@example.com,41,false
```

It is just a table: columns across, records down. Excel and Google Sheets can open and save it.

**Strengths:** simple, compact, universally supported, great for flat tables.
**Weaknesses:** no data types (everything is text), no nesting (cannot represent lists inside a cell cleanly), and edge cases (commas or line breaks inside values, different delimiters, encodings).

### 1.2 Why Not Just Use `split(",")`?

In the previous lesson we parsed with `line.split(",")`. That breaks as soon as a value contains a comma:

```
id,name,comment
1,Ada,"Loves maths, logic, and engines"
```

`split(",")` would cut the comment into three pieces. CSV solves this by **quoting** values that contain special characters: surrounding them with `"..."`, and doubling a literal quote (`""`). Quoted values may even contain line breaks. The `csv` module understands all these rules, so always use it.

### 1.3 Reading with `csv.reader`

First create a sample file:

```python
import csv

rows = [
    ["id", "name", "email", "age", "active"],
    ["1", "Ada Lovelace", "ada@example.com", "36", "true"],
    ["2", "Grace Hopper", "grace@example.com", "45", "true"],
    ["3", "Alan Turing", "alan@example.com", "41", "false"],
]

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
```

Now read it:

```python
import csv

with open("users.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

Output:

```
['id', 'name', 'email', 'age', 'active']
['1', 'Ada Lovelace', 'ada@example.com', '36', 'true']
['2', 'Grace Hopper', 'grace@example.com', '45', 'true']
['3', 'Alan Turing', 'alan@example.com', '41', 'false']
```

**Explanation:**

- `import csv` loads the built-in module.
- **`newline=""`** is required by the `csv` documentation when opening files. It stops Python's automatic newline translation from interfering with the module's own handling of line endings and with line breaks inside quoted values. If you forget it you may see blank lines between rows on Windows, or corrupted multi-line values.
- `csv.reader(f)` wraps the file and yields each row as a **list of strings**.
- **Every value is a string**, including `'36'`. You must convert types yourself (`int(row[3])`).

Typical pattern: skip the header with `next(reader)`:

```python
with open("users.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)          # first row
    for row in reader:
        name = row[1]
        age = int(row[3])
        print(f"{name} is {age}")
```

```
Ada Lovelace is 36
Grace Hopper is 45
Alan Turing is 41
```

Accessing columns by number (`row[3]`) is fragile: if someone inserts a column, your code silently reads the wrong data. That is why `DictReader` exists.

### 1.4 Reading with `csv.DictReader` (Recommended)

`DictReader` uses the header row to give each row as a dictionary keyed by column name:

```python
import csv

with open("users.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("Columns:", reader.fieldnames)
    for row in reader:
        print(row["name"], "-", row["email"])
```

Output:

```
Columns: ['id', 'name', 'email', 'age', 'active']
Ada Lovelace - ada@example.com
Grace Hopper - grace@example.com
Alan Turing - alan@example.com
```

Now columns can be reordered and your code still works. Each `row` is a dictionary (in modern Python, a regular `dict`). Values are still strings.

**Converting types** is your responsibility:

```python
import csv

users = []
with open("users.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        users.append({
            "id": int(row["id"]),
            "name": row["name"],
            "email": row["email"],
            "age": int(row["age"]),
            "active": row["active"].strip().lower() == "true",
        })

print(users[2])
```

```
{'id': 3, 'name': 'Alan Turing', 'email': 'alan@example.com', 'age': 41, 'active': False}
```

Note `row["active"].strip().lower() == "true"`: the CSV holds the *text* `"true"`; we compare to get a real boolean. Never use `bool("false")`; any non-empty string is `True`!

### 1.5 Writing with `csv.writer` and `csv.DictWriter`

**`writer`** takes lists:

```python
import csv

results = [("Login", "pass", 1.2), ("Search", "fail", 3.4)]

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["test", "status", "seconds"])   # header
    writer.writerows(results)                         # many rows at once
```

`results.csv`:

```
test,status,seconds
Login,pass,1.2
Search,fail,3.4
```

**`DictWriter`** takes dictionaries and needs the column names:

```python
import csv

records = [
    {"test": "Login", "status": "pass", "seconds": 1.2},
    {"test": "Search", "status": "fail", "seconds": 3.4},
]

with open("results2.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["test", "status", "seconds"])
    writer.writeheader()
    writer.writerows(records)
```

Quoting is automatic: a value like `He said "hi", then left` is written as `"He said ""hi"", then left"`.

### 1.6 Delimiters and Dialects

Not every "CSV" uses commas. Some use semicolons (common in European locales where the comma is the decimal separator), tabs (TSV) or pipes. Specify the `delimiter`:

```python
csv.reader(f, delimiter=";")
csv.writer(f, delimiter="\t")
```

Other parameters: `quotechar`, `quoting` (for example `csv.QUOTE_ALL`), `skipinitialspace=True` (ignore spaces after delimiters). A bundle of such settings is called a **dialect**.

### 1.7 Handling Messy CSV

Real files have blank lines, missing cells, and short rows. With `DictReader`, a short row gets `None` for missing columns, and extra cells are collected under the key `None` (or `restkey`).

```python
import csv, io

messy = io.StringIO("id,name,age\n1,Ada,36\n2,Grace\n3,Alan,41,EXTRA\n")
for row in csv.DictReader(messy):
    print(row)
```

Output:

```
{'id': '1', 'name': 'Ada', 'age': '36'}
{'id': '2', 'name': 'Grace', 'age': None}
{'id': '3', 'name': 'Alan', 'age': '41', None: ['EXTRA']}
```

(`io.StringIO` lets you treat a string like a file: handy for experiments and for tests that should not touch the disk.) A robust loader would detect `None` values and report the row number. You will practise that in the exercise.

---

## Part 2: JSON (JavaScript Object Notation)

### 2.1 What is JSON?

JSON is a text format for **structured, nested data**, originally from JavaScript but now universal. It is the standard language of web APIs.

```json
{
  "id": 1,
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "active": true,
  "roles": ["admin", "tester"],
  "address": {
    "city": "London",
    "postcode": "N1 1AA"
  },
  "manager": null
}
```

JSON has only a few building blocks:

| JSON | Python equivalent |
|------|-------------------|
| object `{ "key": value }` | `dict` |
| array `[ ... ]` | `list` |
| string `"text"` | `str` |
| number `42`, `3.14` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

**Strict syntax rules** (frequent sources of errors): keys and strings use **double quotes** only; **no trailing commas**; no comments; no `True`/`None` (those are Python, not JSON).

**Strengths:** supports nesting and basic types, human-readable, ubiquitous in APIs.
**Weaknesses:** no comments, no date type (dates are just strings), larger than CSV for flat tables.

### 2.2 Parsing JSON Text into Python: `json.loads`

`loads` ("load string") converts a JSON **string** into Python objects:

```python
import json

text = '{"id": 1, "name": "Ada", "active": true, "roles": ["admin", "tester"], "manager": null}'
data = json.loads(text)

print(type(data))            # <class 'dict'>
print(data["name"])          # Ada
print(data["roles"][0])      # admin
print(data["active"])        # True
print(data["manager"])       # None
```

### 2.3 Reading JSON from a File: `json.load`

`load` (no "s") reads from a **file object**:

First, create the file:

```python
import json

config = {
    "browser": "chrome",
    "timeout": 30,
    "headless": False,
    "urls": ["https://example.test/login", "https://example.test/search"],
}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
```

Then read it back:

```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["browser"], config["timeout"], config["headless"])
print(len(config["urls"]), "urls")
```

Output:

```
chrome 30 False
2 urls
```

**Remember the names:** `load`/`dump` work with **files**; `loads`/`dumps` work with **strings** (the "s" = string).

### 2.4 Writing JSON: `json.dump` and `json.dumps`

```python
import json

report = {"total": 3, "passed": 2, "failed": 1, "tests": ["a", "b", "c"], "note": "café"}

print(json.dumps(report))
print(json.dumps(report, indent=2, sort_keys=True))
print(json.dumps(report, ensure_ascii=False))
```

Output:

```
{"total": 3, "passed": 2, "failed": 1, "tests": ["a", "b", "c"], "note": "café"}
{
  "failed": 1,
  "note": "café",
  "passed": 2,
  "tests": [
    "a",
    "b",
    "c"
  ],
  "total": 3
}
{"total": 3, "passed": 2, "failed": 1, "tests": ["a", "b", "c"], "note": "café"}
```

Useful options:

| Option | Effect |
|--------|--------|
| `indent=2` | Pretty-print with 2-space indentation (readable) |
| `sort_keys=True` | Alphabetical keys (stable output, easier to compare) |
| `ensure_ascii=False` | Keep non-ASCII characters as they are instead of `\uXXXX` escapes (open the file with `encoding="utf-8"`) |

### 2.5 Python Objects JSON Cannot Handle

JSON only supports the types in the table. Trying to dump others fails:

```python
import json
from datetime import datetime

try:
    json.dumps({"when": datetime.now()})
except TypeError as error:
    print("Cannot serialise:", error)
```

```
Cannot serialise: Object of type datetime is not JSON serializable
```

Solutions: convert to a string first (`datetime.now().isoformat()`), or pass `default=str`:

```python
print(json.dumps({"when": datetime(2025, 1, 15, 9, 30)}, default=str))
# {"when": "2025-01-15 09:30:00"}
```

Also note that dictionary keys become strings (`{1: "a"}` becomes `{"1": "a"}`), and tuples become lists.

### 2.6 Navigating Nested JSON

```python
import json

api_response = json.loads("""
{
  "status": "ok",
  "data": {
    "users": [
      {"id": 1, "name": "Ada", "tags": ["admin"]},
      {"id": 2, "name": "Grace", "tags": []}
    ],
    "total": 2
  }
}
""")

print(api_response["data"]["total"])               # 2
print(api_response["data"]["users"][1]["name"])    # Grace

for user in api_response["data"]["users"]:
    print(user["id"], user["name"], len(user["tags"]))
```

Chains of `[...]` go one level deeper each time. A missing key raises `KeyError`; for optional data use `.get()`:

```python
nickname = api_response["data"]["users"][0].get("nickname", "n/a")
print(nickname)    # n/a
```

### 2.7 Handling Invalid JSON

Malformed JSON raises `json.JSONDecodeError`, a subclass of `ValueError`:

```python
import json

bad_samples = [
    "{'name': 'Ada'}",          # single quotes
    '{"name": "Ada",}',         # trailing comma
    '{"name": "Ada"',           # unclosed brace
    "",                          # empty
]

for text in bad_samples:
    try:
        json.loads(text)
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error.msg} (line {error.lineno}, column {error.colno})")
```

Output:

```
Invalid JSON: Expecting property name enclosed in double quotes (line 1, column 2)
Invalid JSON: Illegal trailing comma before end of object (line 1, column 16)
Invalid JSON: Expecting ',' delimiter (line 1, column 15)
Invalid JSON: Expecting value (line 1, column 1)
```

(The exact wording of messages differs between Python versions; for instance older versions say "Expecting property name enclosed in double quotes" for the trailing-comma case.) The error object offers `msg`, `lineno` and `colno`, so you can tell a data owner exactly where the file is broken.

---

## Part 3: XML (eXtensible Markup Language)

### 3.1 What is XML?

XML structures data as a **tree of elements** written with opening and closing **tags**, optionally with **attributes**.

`testsuite.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="LoginTests" tests="3">
  <testcase id="TC1" status="pass">
    <title>Valid login</title>
    <duration>1.2</duration>
  </testcase>
  <testcase id="TC2" status="fail">
    <title>Wrong password</title>
    <duration>0.8</duration>
    <message>Expected error banner not shown</message>
  </testcase>
  <testcase id="TC3" status="pass">
    <title>Logout</title>
    <duration>0.5</duration>
  </testcase>
</testsuite>
```

Vocabulary:

- **Element:** a unit like `<title>Valid login</title>`.
- **Root element:** the single outermost element (`testsuite`).
- **Attribute:** a name/value inside an opening tag (`id="TC1"`).
- **Text:** content between tags ("Valid login").
- **Children:** elements nested inside another.
- Documents must be **well-formed**: every opening tag closed, tags properly nested, one root, attribute values quoted, special characters escaped (`&lt;` for `<`, `&amp;` for `&`).

**Strengths:** supports attributes, nesting, mixed content, namespaces, schemas; widely used in enterprise systems and CI test reports.
**Weaknesses:** verbose, harder to read than JSON, more complex to parse. Everything is text.

### 3.2 Parsing with `ElementTree`

Python's built-in `xml.etree.ElementTree` module (usually imported as `ET`) turns XML into a tree of `Element` objects.

First, create the sample file from the example above:

```python
xml_text = """<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="LoginTests" tests="3">
  <testcase id="TC1" status="pass">
    <title>Valid login</title>
    <duration>1.2</duration>
  </testcase>
  <testcase id="TC2" status="fail">
    <title>Wrong password</title>
    <duration>0.8</duration>
    <message>Expected error banner not shown</message>
  </testcase>
  <testcase id="TC3" status="pass">
    <title>Logout</title>
    <duration>0.5</duration>
  </testcase>
</testsuite>
"""

with open("testsuite.xml", "w", encoding="utf-8") as f:
    f.write(xml_text)
```

Parse it:

```python
import xml.etree.ElementTree as ET

tree = ET.parse("testsuite.xml")      # reads and parses the file
root = tree.getroot()                  # the <testsuite> element

print(root.tag)                        # testsuite
print(root.attrib)                     # {'name': 'LoginTests', 'tests': '3'}
print(root.get("name"))                # LoginTests

for case in root:                      # iterate over direct children
    print(case.tag, case.attrib)
```

Output:

```
testsuite
{'name': 'LoginTests', 'tests': '3'}
LoginTests
testcase {'id': 'TC1', 'status': 'pass'}
testcase {'id': 'TC2', 'status': 'fail'}
testcase {'id': 'TC3', 'status': 'pass'}
```

Key members of an `Element`:

| Member | Meaning |
|--------|---------|
| `.tag` | The element's name |
| `.attrib` | Dictionary of attributes (values are strings) |
| `.get("name", default)` | Read one attribute |
| `.text` | Text directly inside the element (can be `None`) |
| iteration / `list(elem)` | The direct children |

To parse XML that is already in a **string**, use `ET.fromstring(xml_text)`, which returns the root element directly.

### 3.3 Finding Elements

```python
import xml.etree.ElementTree as ET

root = ET.parse("testsuite.xml").getroot()

# find: first matching direct child; findall: all matching direct children
first_case = root.find("testcase")
print(first_case.get("id"))                    # TC1

for case in root.findall("testcase"):
    title = case.find("title").text            # text of the <title> child
    duration = float(case.find("duration").text)
    print(f"{case.get('id')}: {title} ({duration}s) -> {case.get('status')}")
```

Output:

```
TC1: Valid login (1.2s) -> pass
TC2: Wrong password (0.8s) -> fail
TC3: Logout (0.5s) -> pass
```

More ways to search:

```python
# iter(): search ALL descendants at any depth
for d in root.iter("duration"):
    print(d.text)

# findtext(): text of a child, with a default if missing
for case in root.findall("testcase"):
    message = case.findtext("message", default="(no message)")
    print(case.get("id"), message)

# Simple XPath-style patterns
failed = root.findall(".//testcase[@status='fail']")     # any depth, attribute filter
print([c.get("id") for c in failed])                      # ['TC2']
```

**Careful with missing elements:** `case.find("message")` returns `None` when nothing matches, and `None.text` raises `AttributeError`. Either check for `None` or use `findtext` with a default.

**Careful with `if element:`:** An `Element` with no children is treated as false in a boolean test. Compare with `is not None` explicitly.

```python
msg = case.find("message")
if msg is not None:        # correct
    print(msg.text)
```

### 3.4 Building and Writing XML

```python
import xml.etree.ElementTree as ET

suite = ET.Element("testsuite", name="Demo", tests="2")

for tid, status in [("TC1", "pass"), ("TC2", "fail")]:
    case = ET.SubElement(suite, "testcase", id=tid, status=status)
    ET.SubElement(case, "title").text = f"Case {tid}"

tree = ET.ElementTree(suite)
ET.indent(tree, space="  ")             # pretty-print (Python 3.9+)
tree.write("demo_out.xml", encoding="utf-8", xml_declaration=True)

print(open("demo_out.xml", encoding="utf-8").read())
```

Output:

```
<?xml version='1.0' encoding='utf-8'?>
<testsuite name="Demo" tests="2">
  <testcase id="TC1" status="pass">
    <title>Case TC1</title>
  </testcase>
  <testcase id="TC2" status="fail">
    <title>Case TC2</title>
  </testcase>
</testsuite>
```

- `ET.Element("testsuite", name="Demo")` creates an element with attributes.
- `ET.SubElement(parent, "tag", attr=...)` creates a child attached to its parent.
- Setting `.text` assigns the element's text. Special characters (`<`, `&`) are escaped for you.
- `ET.tostring(element, encoding="unicode")` gives a string rather than a file.

### 3.5 Handling Malformed XML

```python
import xml.etree.ElementTree as ET

bad_xml = "<testsuite><testcase></testsuite>"      # tags not properly nested

try:
    ET.fromstring(bad_xml)
except ET.ParseError as error:
    print("XML is not well-formed:", error)
```

Output (the column number can vary slightly between Python versions):

```
XML is not well-formed: mismatched tag: line 1, column 23
```

`ET.ParseError` has a `.position` attribute `(line, column)`.

### 3.6 Security Note

`ElementTree` is fine for trusted files such as your own test data. But XML parsers can be abused with specially crafted documents (for example, "billion laughs" entity-expansion attacks). If you ever parse XML from an **untrusted** source, consult the official documentation's "XML vulnerabilities" section; the third-party `defusedxml` package is the commonly recommended mitigation.

---

## Part 4: Comparing and Choosing Formats

| Aspect | CSV | JSON | XML |
|--------|-----|------|-----|
| Structure | Flat table | Nested objects/arrays | Nested tree with attributes |
| Data types | None (all text) | string, number, bool, null, list, object | None (all text) |
| Human readability | High for tables | High | Medium (verbose) |
| Size | Smallest | Medium | Largest |
| Python module | `csv` | `json` | `xml.etree.ElementTree` |
| Typical QA use | Bulk data-driven test input | API payloads, configs | Legacy services, test reports |
| Comments allowed | No | No | Yes (`<!-- -->`) |

Guidelines:

- Many similar records with the same fields: **CSV**.
- Nested data or API payloads: **JSON**.
- A system or tool that demands it, or data needing attributes/schemas: **XML**.

### Converting between formats

All three end up as ordinary Python structures (lists/dicts), so conversion is "read with one module, write with another":

```python
import csv, json

# CSV -> JSON
with open("users.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("users.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

# JSON -> CSV
with open("users.json", encoding="utf-8") as f:
    records = json.load(f)

with open("users_copy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
```

Note that CSV-to-JSON gives every value as a string, because CSV has no types. Convert specific columns afterwards if the consumer expects numbers.

---

## Real-World QA Scenarios

### Scenario 1: Data-driven test input from CSV

```python
import csv
import io

csv_data = io.StringIO(
    "username,password,expected\n"
    "ada,correct,success\n"
    "ada,wrong,failure\n"
    ",correct,failure\n"
)

def fake_login(username, password):
    return "success" if username and password == "correct" else "failure"

for number, row in enumerate(csv.DictReader(csv_data), start=1):
    actual = fake_login(row["username"], row["password"])
    verdict = "PASS" if actual == row["expected"] else "FAIL"
    print(f"case {number}: user={row['username']!r:7} -> {actual:8} expected {row['expected']:8} {verdict}")
```

Output:

```
case 1: user='ada'   -> success  expected success  PASS
case 2: user='ada'   -> failure  expected failure  PASS
case 3: user=''      -> failure  expected failure  PASS
```

One piece of logic, many rows of data: the essence of data-driven testing. Adding a case means adding a line to the file, not editing code.

### Scenario 2: Checking an API response saved as JSON

```python
import json

response_text = """
{"status": 201, "user": {"id": 77, "email": "new@example.com", "roles": ["tester"]}}
"""

response = json.loads(response_text)

assert response["status"] == 201, f"unexpected status {response['status']}"
assert "@" in response["user"]["email"], "email looks invalid"
assert "tester" in response["user"]["roles"], "tester role missing"
print("API response checks passed")
```

Output:

```
API response checks passed
```

(This uses the `assert` statement from the previous lesson as a simple check.)

### Scenario 3: Summarising a test-result XML report

```python
import xml.etree.ElementTree as ET

report = ET.fromstring("""
<testsuite name="Checkout">
  <testcase name="add_item" time="0.4"/>
  <testcase name="apply_coupon" time="1.1"><failure message="Coupon rejected"/></testcase>
  <testcase name="pay" time="2.3"><skipped/></testcase>
</testsuite>
""")

summary = {"passed": 0, "failed": 0, "skipped": 0}
total_time = 0.0

for case in report.findall("testcase"):
    total_time += float(case.get("time", 0))
    if case.find("failure") is not None:
        summary["failed"] += 1
        print("FAILED:", case.get("name"), "-", case.find("failure").get("message"))
    elif case.find("skipped") is not None:
        summary["skipped"] += 1
    else:
        summary["passed"] += 1

print(summary, f"total {total_time:.1f}s")
```

Output:

```
FAILED: apply_coupon - Coupon rejected
{'passed': 1, 'failed': 1, 'skipped': 1} total 3.8s
```

This mirrors the structure of real-world JUnit-style test reports that many CI systems produce, so the same skills let you write tools that analyse them.

### Scenario 4: A defensive CSV loader

```python
import csv
import io

REQUIRED = ["id", "name", "age"]

def load_users(file_obj):
    reader = csv.DictReader(file_obj)

    missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
    if missing:
        raise ValueError(f"missing columns: {missing}")

    good, errors = [], []
    for line_no, row in enumerate(reader, start=2):      # line 1 is the header
        try:
            good.append({
                "id": int(row["id"]),
                "name": row["name"].strip(),
                "age": int(row["age"]),
            })
        except (ValueError, TypeError, AttributeError) as error:
            errors.append(f"line {line_no}: {type(error).__name__}: {error}")
    return good, errors


data = io.StringIO("id,name,age\n1,Ada,36\n2,Grace,forty\n3,Alan,\n4,Linus,55\n")
users, problems = load_users(data)
print(users)
for p in problems:
    print(p)
```

Output:

```
[{'id': 1, 'name': 'Ada', 'age': 36}, {'id': 4, 'name': 'Linus', 'age': 55}]
line 3: ValueError: invalid literal for int() with base 10: 'forty'
line 4: ValueError: invalid literal for int() with base 10: ''
```

The loader reports structural problems (missing columns) by raising, but collects row-level problems and keeps going. Choosing which failures stop everything and which are collected is a design decision you will make in the Project 1 data-ingestion milestone.

---

## Code Examples: Putting It All Together

This script writes the same dataset in all three formats, reads each back, and checks they agree. Save it as `formats_roundtrip.py`.

```python
"""formats_roundtrip.py - Write and re-read test data as CSV, JSON and XML."""

import csv
import json
import xml.etree.ElementTree as ET

TESTS = [
    {"id": "TC1", "title": "Valid login", "status": "pass"},
    {"id": "TC2", "title": "Wrong password", "status": "fail"},
    {"id": "TC3", "title": "Logout", "status": "pass"},
]

# ---- CSV ----
with open("tests.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "title", "status"])
    writer.writeheader()
    writer.writerows(TESTS)

with open("tests.csv", newline="", encoding="utf-8") as f:
    from_csv = list(csv.DictReader(f))

# ---- JSON ----
with open("tests.json", "w", encoding="utf-8") as f:
    json.dump(TESTS, f, indent=2)

with open("tests.json", encoding="utf-8") as f:
    from_json = json.load(f)

# ---- XML ----
root = ET.Element("tests")
for t in TESTS:
    case = ET.SubElement(root, "test", id=t["id"], status=t["status"])
    case.text = t["title"]
ET.ElementTree(root).write("tests.xml", encoding="utf-8", xml_declaration=True)

from_xml = [
    {"id": e.get("id"), "title": e.text, "status": e.get("status")}
    for e in ET.parse("tests.xml").getroot().findall("test")
]

# ---- Compare ----
for name, loaded in (("CSV", from_csv), ("JSON", from_json), ("XML", from_xml)):
    print(f"{name:5} round-trip matches original:", loaded == TESTS)
```

Output:

```
CSV   round-trip matches original: True
JSON  round-trip matches original: True
XML   round-trip matches original: True
```

**Walkthrough:**

1. The same list of dictionaries is the "source of truth".
2. CSV: `DictWriter` writes with a header, `DictReader` brings back dictionaries. It matches because all our values are strings. A numeric field would come back as text.
3. JSON: `dump`/`load` preserve structure and types.
4. XML: we choose to put `id` and `status` in attributes and the title in the element text; reading back, we rebuild dictionaries with a list comprehension. XML has no built-in dictionary mapping, so *you* define the layout.
5. The final loop proves all three retained the data.

---

## Practice Exercises

**Exercise 1.** Create `products.csv` with columns `sku,name,price,stock` and four rows. Read it with `DictReader`, convert `price` to `float` and `stock` to `int`, and print the total inventory value (`price * stock` summed).

**Exercise 2.** Write a function `write_report(path, results)` that takes a list of `(test_name, status)` tuples and writes a CSV with a header. Make sure a test name containing a comma (`"Login, valid"`) survives a round trip.

**Exercise 3.** Given this JSON string, print each user's name and the number of roles. Use `.get()` so a user with no `roles` key prints 0.

```python
text = '{"users": [{"name": "Ada", "roles": ["a", "b"]}, {"name": "Grace"}]}'
```

**Exercise 4.** Write `safe_load_json(path)` that returns the parsed data, or `None` after printing a helpful message with line/column for each of: missing file, invalid JSON.

**Exercise 5.** Using `ElementTree`, parse this and print the IDs of products that cost more than 20:

```xml
<catalog>
  <product id="p1"><price>9.99</price></product>
  <product id="p2"><price>24.50</price></product>
  <product id="p3"><price>31.00</price></product>
</catalog>
```

**Exercise 6.** Convert `users.csv` (from the lesson) into an XML file where each row becomes `<user id="...">` with child elements `<name>` and `<email>`.

**Exercise 7.** Explain why each of these would be a bug:

1. `open("data.csv", "r")` followed by `csv.reader(f)` on Windows, without `newline=""`.
2. `bool(row["active"])` to convert the text `"false"`.
3. `json.loads("{'a': 1}")`.
4. `root.find("missing").text`.

### Answers

**Exercise 1:**

```python
import csv

with open("products.csv", "w", newline="", encoding="utf-8") as f:
    f.write("sku,name,price,stock\nA1,Mouse,9.99,10\nA2,Keyboard,24.5,4\nA3,Cable,2.5,100\nA4,Monitor,150,2\n")

total = 0.0
with open("products.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total += float(row["price"]) * int(row["stock"])
print(f"Inventory value: {total:.2f}")      # 747.90
```

(9.99 x 10 + 24.5 x 4 + 2.5 x 100 + 150 x 2 = 99.9 + 98 + 250 + 300 = 747.9.)

**Exercise 2:**

```python
import csv

def write_report(path, results):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["test", "status"])
        writer.writerows(results)

write_report("r.csv", [("Login, valid", "pass"), ("Logout", "fail")])
with open("r.csv", newline="", encoding="utf-8") as f:
    print(list(csv.reader(f)))
# [['test', 'status'], ['Login, valid', 'pass'], ['Logout', 'fail']]
```

The writer automatically quotes the value containing a comma.

**Exercise 3:**

```python
import json
text = '{"users": [{"name": "Ada", "roles": ["a", "b"]}, {"name": "Grace"}]}'
for user in json.loads(text)["users"]:
    print(user["name"], len(user.get("roles", [])))
# Ada 2
# Grace 0
```

**Exercise 4:**

```python
import json

def safe_load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found:", path)
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {path}: {error.msg} at line {error.lineno}, column {error.colno}")
    return None
```

**Exercise 5:**

```python
import xml.etree.ElementTree as ET

xml = """<catalog>
  <product id="p1"><price>9.99</price></product>
  <product id="p2"><price>24.50</price></product>
  <product id="p3"><price>31.00</price></product>
</catalog>"""

root = ET.fromstring(xml)
print([p.get("id") for p in root.findall("product") if float(p.findtext("price")) > 20])
# ['p2', 'p3']
```

**Exercise 6:**

```python
import csv
import xml.etree.ElementTree as ET

root = ET.Element("users")
with open("users.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        user = ET.SubElement(root, "user", id=row["id"])
        ET.SubElement(user, "name").text = row["name"]
        ET.SubElement(user, "email").text = row["email"]

tree = ET.ElementTree(root)
ET.indent(tree)
tree.write("users.xml", encoding="utf-8", xml_declaration=True)
```

**Exercise 7:** (1) Without `newline=""`, Python's newline translation can add blank lines between rows on Windows and can corrupt line breaks inside quoted cells. (2) `bool("false")` is `True` because any non-empty string is truthy; compare to the text instead. (3) JSON requires double quotes, so this raises `JSONDecodeError`. (4) `find` returns `None` when there is no match, so `.text` raises `AttributeError`; check for `None` or use `findtext`.

---

## Summary / Key Takeaways

- **CSV** is a flat table of text values: use `csv.reader`/`csv.writer`, or preferably `DictReader`/`DictWriter`; always open with `newline=""` and `encoding="utf-8"`; everything read is a string, so convert types yourself.
- **JSON** is nested data with objects, arrays, strings, numbers, booleans and null that map to `dict`, `list`, `str`, `int/float`, `bool`, `None`. Use `json.load`/`json.dump` for files and `json.loads`/`json.dumps` for strings. Catch `json.JSONDecodeError`.
- **XML** is a tree of elements with attributes and text; use `xml.etree.ElementTree` (`parse`, `fromstring`, `find`, `findall`, `iter`, `.attrib`, `.text`). Beware `None` from `find` and catch `ET.ParseError`. Treat untrusted XML with caution.
- None of these formats is "best"; match the format to the data (flat tables, nested/API data, legacy/report formats).
- Real data is messy: validate, convert types, report row/line numbers, and decide which problems stop processing and which are collected.
- Next: **context managers**, the `with` mechanism behind all the `with open(...)` lines you have been writing.

---

## Additional Resources

- Python Library Reference, `csv`: https://docs.python.org/3/library/csv.html
- Python Library Reference, `json`: https://docs.python.org/3/library/json.html
- Python Library Reference, `xml.etree.ElementTree`: https://docs.python.org/3/library/xml.etree.elementtree.html
