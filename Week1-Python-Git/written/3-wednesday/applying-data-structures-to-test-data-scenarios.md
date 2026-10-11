# Applying Data Structures to Test-Data Scenarios

## Learning Objectives

By the end of this lesson you will be able to:

- Represent test cases, test users and test results using lists, dictionaries, sets and tuples.
- Choose the most suitable data structure for a given test-data problem and justify the choice.
- Solve typical QA data tasks: removing duplicates, grouping, looking up, filtering, counting and summarising.
- Validate test data (required fields, allowed values, missing and unexpected items) using sets and dictionaries.
- Build a small data-driven test loop from a table of inputs and expected outputs.
- Combine loops, conditionals, collection methods and the `collections` module in one program.
- Plan the structure of a small "test-data manager" program (the focus of today's exercise).

---

## Why This Matters

The last four lessons gave you tools. This lesson is where they come together on the kind of data you'll meet every day as a test automation engineer.

Test data is rarely clean. A spreadsheet export might contain duplicate test IDs. A results file has a mix of passes, failures and skips and you need a summary per module. A test needs the credentials for one specific user *quickly*. A requirements list says 12 tests are planned, but only 10 ran: which two were missed?

Knowing **which structure fits which question** is the real skill. A wrong choice makes code long and slow; a right choice makes it nearly trivial. This lesson shows the thought process: look at the data, ask what you will do with it, and then choose.

---

## The Concept

### 1. A Method for Choosing: Ask Three Questions

Before writing code, ask:

1. **What does one item look like?** (a single value, a record with named fields, a pair?)
2. **How will I find things?** (by position, by a name/key, or just "is it there?")
3. **Does order matter, do duplicates matter, will it change?**

| If the answer is... | Use |
|---|---|
| One record with named fields | **Dictionary** |
| Many similar records, in order | **List of dictionaries** |
| Fixed record that must not change | **Tuple** (or `namedtuple`) |
| Quick lookup by ID | **Dictionary keyed by ID** |
| Uniqueness / "have I seen this?" | **Set** |
| Count or group by category | **`Counter`** / **`defaultdict`** |
| First-come-first-served processing | **`deque`** (or a list) |

---

### 2. Scenario 1: Representing Test Cases (Records and Tables)

**Problem:** store a set of test cases with an ID, title, module, priority and automation status.

A **list of dictionaries** is the natural "table":

```python
test_cases = [
    {"id": "TC-001", "title": "Valid login",       "module": "login",    "priority": "High",   "automated": True},
    {"id": "TC-002", "title": "Invalid password",  "module": "login",    "priority": "High",   "automated": True},
    {"id": "TC-003", "title": "Search by keyword", "module": "search",   "priority": "Medium", "automated": False},
    {"id": "TC-004", "title": "Add to cart",       "module": "checkout", "priority": "High",   "automated": False},
    {"id": "TC-005", "title": "Empty search",      "module": "search",   "priority": "Low",    "automated": True},
]
```

Printing as a table:

```python
print(f"{'ID':<8}{'Title':<20}{'Module':<10}{'Priority':<9}")
print("-" * 47)
for case in test_cases:
    print(f"{case['id']:<8}{case['title']:<20}{case['module']:<10}{case['priority']:<9}")
```

```text
ID      Title               Module    Priority 
-----------------------------------------------
TC-001  Valid login         login     High     
TC-002  Invalid password    login     High     
TC-003  Search by keyword   search    Medium   
TC-004  Add to cart         checkout  High     
TC-005  Empty search        search    Low      
```

We'll reuse `test_cases` in the next scenarios.

---

### 3. Scenario 2: Filtering and Counting

**Question:** which high-priority tests are still **not automated**?

```python
to_automate = []

for case in test_cases:
    if case["priority"] == "High" and not case["automated"]:
        to_automate.append(case["id"])

print(f"High-priority tests to automate: {to_automate}")
```

```text
High-priority tests to automate: ['TC-004']
```

**Question:** what percentage of tests is automated?

```python
automated_count = 0
for case in test_cases:
    if case["automated"]:
        automated_count += 1

percentage = automated_count / len(test_cases) * 100
print(f"Automation coverage: {percentage:.0f}%")        # 60%
```

**Question:** how many tests per priority?

```python
from collections import Counter

priority_counts = Counter()
for case in test_cases:
    priority_counts[case["priority"]] += 1

print(priority_counts)    # Counter({'High': 3, 'Medium': 1, 'Low': 1})
```

(Adding to a `Counter` with `+=` works, because a missing key starts at 0.)

---

### 4. Scenario 3: Grouping

**Question:** list the test IDs for each module.

A grouping job is a `defaultdict(list)`:

```python
from collections import defaultdict

by_module = defaultdict(list)

for case in test_cases:
    by_module[case["module"]].append(case["id"])

for module, ids in by_module.items():
    print(f"{module:<10} {len(ids)} tests: {', '.join(ids)}")
```

```text
login      2 tests: TC-001, TC-002
search     2 tests: TC-003, TC-005
checkout   1 tests: TC-004
```

**Grouping results and computing a summary per group** (pass rate per module):

```python
results = [
    {"id": "TC-001", "module": "login",    "status": "PASS"},
    {"id": "TC-002", "module": "login",    "status": "FAIL"},
    {"id": "TC-003", "module": "search",   "status": "PASS"},
    {"id": "TC-004", "module": "checkout", "status": "FAIL"},
    {"id": "TC-005", "module": "search",   "status": "PASS"},
]

totals = defaultdict(int)
passes = defaultdict(int)

for result in results:
    totals[result["module"]] += 1
    if result["status"] == "PASS":
        passes[result["module"]] += 1

for module in totals:
    rate = passes[module] / totals[module] * 100
    print(f"{module:<10} {passes[module]}/{totals[module]} passed ({rate:.0f}%)")
```

```text
login      1/2 passed (50%)
search     2/2 passed (100%)
checkout   0/1 passed (0%)
```

Note `passes["checkout"]` is `0` even though no checkout test passed: a `defaultdict(int)` supplies a 0 for the missing key.

---

### 5. Scenario 4: Fast Lookup by ID

**Problem:** you often need "the test case with ID `TC-004`". Searching a list each time is clumsy:

```python
wanted = "TC-004"
found = None
for case in test_cases:
    if case["id"] == wanted:
        found = case
        break
print(found["title"] if found else "Not found")
```

(This uses `break` from Tuesday, and the one-line conditional expression.)

Better: build a **dictionary keyed by ID** once, then look up instantly:

```python
by_id = {}
for case in test_cases:
    by_id[case["id"]] = case

print(by_id["TC-004"]["title"])             # Add to cart
print(by_id.get("TC-999", "Not found"))     # Not found
```

When data is large and lookups are frequent, a dictionary is dramatically faster than searching a list, because a dictionary jumps straight to the key instead of checking every item.

**Test users as a lookup table:**

```python
users = {
    "admin": {"password": "Admin#123", "role": "administrator"},
    "guest": {"password": "Guest#123", "role": "viewer"},
}

wanted_user = "guest"
if wanted_user in users:
    print(f"Logging in as {wanted_user} with role {users[wanted_user]['role']}")
```

(These are fake, demonstration-only credentials. Real passwords must never be written into code or committed to Git. Remember the `.gitignore` lesson about secrets.)

---

### 6. Scenario 5: Removing Duplicates

**Problem:** a list of IDs pulled from several spreadsheets contains duplicates.

```python
raw_ids = ["TC-003", "TC-001", "TC-002", "TC-001", "TC-003", "TC-004", "TC-001"]
```

**Option A: a set** (fast, but loses order):

```python
unique_ids = set(raw_ids)
print(sorted(unique_ids))        # ['TC-001', 'TC-002', 'TC-003', 'TC-004']
```

**Option B: keep the first-seen order** using a `seen` set and a result list:

```python
seen = set()
ordered_unique = []

for test_id in raw_ids:
    if test_id not in seen:
        seen.add(test_id)
        ordered_unique.append(test_id)

print(ordered_unique)            # ['TC-003', 'TC-001', 'TC-002', 'TC-004']
```

**Option C: report what was duplicated** using `Counter`:

```python
from collections import Counter

counts = Counter(raw_ids)
duplicates = {test_id: count for test_id, count in counts.items() if count > 1}
```

That last line is a *dictionary comprehension*, a compact loop-in-brackets you will learn in a later lesson. The plain-loop version below is equivalent:

```python
duplicates = {}
for test_id, count in counts.items():
    if count > 1:
        duplicates[test_id] = count

print(duplicates)                # {'TC-003': 2, 'TC-001': 3}
```

**Duplicate *records*:** dictionaries can't go into a set (they are mutable and unhashable). If you need uniqueness by **a field** (like ID), keep a `seen` set of the field's values:

```python
rows = [
    {"id": "TC-001", "title": "Login"},
    {"id": "TC-001", "title": "Login (copy)"},
    {"id": "TC-002", "title": "Logout"},
]

seen_ids = set()
unique_rows = []
for row in rows:
    if row["id"] in seen_ids:
        continue
    seen_ids.add(row["id"])
    unique_rows.append(row)

print(len(unique_rows))          # 2
```

---

### 7. Scenario 6: Comparing Collections (Planned vs Executed)

**Problem:** the plan lists the tests that should have run; the results show what did run.

```python
planned = {"TC-001", "TC-002", "TC-003", "TC-004", "TC-005"}
executed = {"TC-001", "TC-002", "TC-004", "TC-099"}

missed = planned - executed
unexpected = executed - planned
completed = planned & executed

print(f"Missed:     {sorted(missed)}")
print(f"Unexpected: {sorted(unexpected)}")
print(f"Completed:  {len(completed)} of {len(planned)}")
```

```text
Missed:     ['TC-003', 'TC-005']
Unexpected: ['TC-099']
Completed:  3 of 5
```

Four lines replace what would otherwise be nested loops, showing why sets matter.

---

### 8. Scenario 7: Validating Test Data

**Problem:** make sure each record has the required fields and allowed values before using it.

```python
required_fields = {"id", "title", "priority"}
allowed_priorities = ("High", "Medium", "Low")

records = [
    {"id": "TC-010", "title": "Reset password", "priority": "High"},
    {"id": "TC-011", "title": "Change email"},                            # missing priority
    {"id": "TC-012", "title": "Delete account", "priority": "Urgent"},    # invalid value
]

for record in records:
    problems = []

    missing = required_fields - set(record.keys())
    if missing:
        problems.append(f"missing fields {sorted(missing)}")

    if "priority" in record and record["priority"] not in allowed_priorities:
        problems.append(f"invalid priority '{record['priority']}'")

    if problems:
        print(f"{record['id']}: INVALID -> {'; '.join(problems)}")
    else:
        print(f"{record['id']}: OK")
```

```text
TC-010: OK
TC-011: INVALID -> missing fields ['priority']
TC-012: INVALID -> invalid priority 'Urgent'
```

Notice the tools used: a **set** for fields (difference), a **tuple** for fixed allowed values, a **list** for collecting problems, `in` checks, and `join`. Each structure plays the role it is best at.

---

### 9. Scenario 8: A Data-Driven Test Loop

**Data-driven testing** means running the same check against many input/expected pairs. A list of tuples (or dictionaries) holds the table:

```python
# (input text, expected result) for a "title-case" check
test_data = [
    ("login test", "Login Test"),
    ("API CHECK", "Api Check"),
    ("  spaced  ", "Spaced"),
    ("already Good", "Already Good"),
]

passed = 0
failed = 0

for raw, expected in test_data:
    actual = raw.strip().title()
    if actual == expected:
        passed += 1
        print(f"PASS: {raw!r} -> {actual!r}")
    else:
        failed += 1
        print(f"FAIL: {raw!r} -> expected {expected!r}, got {actual!r}")

print(f"\nPassed {passed}, failed {failed}")
```

```text
PASS: 'login test' -> 'Login Test'
PASS: 'API CHECK' -> 'Api Check'
PASS: '  spaced  ' -> 'Spaced'
PASS: 'already Good' -> 'Already Good'

Passed 4, failed 0
```

(`!r` inside an f-string shows the value with quotes, which helps reveal stray spaces.)

Tuple unpacking in the loop header (`for raw, expected in test_data`) is neat. Adding a new case means adding **one line of data**, not new logic. That is the power of data-driven tests, and the idea behind the parametrised tests of professional test frameworks you will meet later.

**Generating combinations** (a test matrix) with nested loops:

```python
browsers = ["Chrome", "Firefox"]
screens = [(1920, 1080), (1366, 768)]

matrix = []
for browser in browsers:
    for width, height in screens:
        matrix.append((browser, width, height))

for index, (browser, width, height) in enumerate(matrix, start=1):
    print(f"Run {index}: {browser} at {width}x{height}")
```

```text
Run 1: Chrome at 1920x1080
Run 2: Chrome at 1366x768
Run 3: Firefox at 1920x1080
Run 4: Firefox at 1366x768
```

---

### 10. Scenario 9: Parsing Raw Text Into Structures

Data usually arrives as text. Convert it into structures first, then analyse.

```python
raw_report = """TC-001,login,PASS,1.2
TC-002,login,FAIL,3.4
TC-003,search,PASS,0.8
TC-004,search,FAIL,2.1
TC-005,checkout,PASS,1.5"""

results = []

for line in raw_report.splitlines():
    test_id, module, status, seconds = line.split(",")
    results.append({
        "id": test_id,
        "module": module,
        "status": status,
        "seconds": float(seconds),           # convert text to number
    })

failures = [r["id"] for r in results if r["status"] == "FAIL"]
```

The last line is a *list comprehension*, a compact filter we'll learn properly later; it is equivalent to:

```python
failures = []
for r in results:
    if r["status"] == "FAIL":
        failures.append(r["id"])

slowest = results[0]
for r in results:
    if r["seconds"] > slowest["seconds"]:
        slowest = r

print(f"Failures: {failures}")                        # ['TC-002', 'TC-004']
print(f"Slowest: {slowest['id']} ({slowest['seconds']}s)")   # TC-002 (3.4s)
```

Pattern: **parse (split, convert types), store in structures, then summarise**. This also shows why Monday's type conversion matters: without `float(seconds)`, the numbers would still be text.

---

### 11. Planning a Test-Data Manager (Preview of the Exercise)

Today's exercise asks for a program that can **de-duplicate**, **group** and **look up** test data. Before coding, plan the structures:

| Requirement | Structure to use | Why |
|---|---|---|
| Hold all test cases | List of dictionaries | Ordered table of records |
| Remove duplicate IDs | `set` of seen IDs | Fast membership checks |
| Group tests by module or status | `defaultdict(list)` | Grouping without `if` checks |
| Count tests by status/priority | `Counter` | Counting built in |
| Look up a case by ID | Dictionary keyed by ID | Instant lookup |
| Show a menu repeatedly | `while True` + `break` | Loop until the user quits |

A good approach to the build: **start tiny**. First hard-code the data and print it. Then add one feature at a time (de-duplicate, then group, then lookup), running and **committing** after each working step. That also gives you clean Git history on your feature branch.

---

### 12. Common Mistakes in Practice

| Mistake | Example | Fix |
|---|---|---|
| Searching a list repeatedly for lookups | Loop inside a loop | Build a dictionary keyed by ID |
| Using a list for uniqueness | `if x not in big_list` | Use a set for membership checks |
| Putting dictionaries in a set | `TypeError: unhashable` | Use a set of IDs instead |
| Forgetting type conversion after parsing | `"3.4" > 2.0` | `float()` after `split()` |
| Using `dict["key"]` on optional data | `KeyError` | `.get()` or `in` |
| Modifying a list while filtering it | Skipped items | Build a new list |
| Losing order with sets | Output order changes | `sorted()` or the ordered de-dup pattern |
| Hard-coding secrets in test data | Passwords in code | Keep secrets out of Git (`.env`, `.gitignore`) |
| Copying a list of dictionaries with `[:]` | Inner dicts are shared | Remember the copy is shallow |

---

### 13. Practice Activities

Use the `test_cases` table from Scenario 1 unless told otherwise.

1. **Filter.** Print the titles of all tests in the `search` module.
2. **Coverage.** Calculate and print the percentage of High-priority tests that are automated.
3. **Group.** Build a `defaultdict(list)` of titles per priority, and print each group sorted alphabetically.
4. **Lookup.** Build a dictionary keyed by `id`. Ask the user for an ID with `input()` and print its details, or `"Not found"`.
5. **Duplicates.** Given `["TC-5", "TC-2", "TC-5", "TC-9", "TC-2", "TC-2"]`, print (a) the unique IDs in sorted order, (b) the unique IDs in first-seen order, and (c) each duplicated ID with its count.
6. **Plan vs run.** Make up two sets of test IDs for "planned" and "executed". Print what was missed, what was unexpected, and the completion percentage.
7. **Validate.** Add a rule to the validation scenario: `id` must start with `"TC-"`. Test it with a bad ID like `"X-1"`.
8. **Data-driven.** Create a table of `(text, expected_length)` pairs and check `len(text)` against each, printing PASS/FAIL per row and a summary.
9. **Parse.** Take the raw report in Scenario 9. Compute the total and average duration per module using `defaultdict`.
10. **Matrix.** Generate every combination of 3 browsers and 2 operating systems, number the runs and print them.
11. **Design.** Without coding, write down which structure you would use for each: (a) the list of test users with passwords and roles, (b) test IDs already executed today, (c) the last 5 failed test names, (d) count of failures per module, and explain why.

---

## Summary

- Choose a data structure by asking: *What does one item look like? How will I find things? Does order, uniqueness or change matter?*
- **List of dictionaries** = the standard "table" of records; **dictionary keyed by ID** = fast lookup; **set** = uniqueness and comparison; **tuple** = fixed groups, such as input/expected pairs; **`Counter`** and **`defaultdict`** = counting and grouping; **`deque`** = queues and "last N".
- Typical QA tasks reduce to a few patterns: **filter** (loop + `if`), **count**, **group**, **look up**, **de-duplicate**, **compare** (set maths), **validate** (required fields and allowed values), **parse** (`split` + type conversion) and **data-driven loops**.
- Set operations quickly answer "what is missing / unexpected / done?".
- Data-driven tests keep logic fixed and put variety into the data: adding a case is adding a row.
- Plan before you code, build in small steps and commit each working step: exactly the habit for today's exercise and the Git lesson that follows.

---

## Additional Resources

- Python Tutorial: Data Structures: https://docs.python.org/3/tutorial/datastructures.html
- Python documentation: `collections`: https://docs.python.org/3/library/collections.html
- Real Python: Python Data Structures (overview): https://realpython.com/python-data-structures/
