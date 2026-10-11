# Introduction to the Collections Module

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a module is and import one with `import` and `from ... import ...`.
- Describe what the `collections` module provides and why it exists.
- Use **`Counter`** to count items and find the most common ones.
- Use **`defaultdict`** to group and count without checking whether a key exists.
- Use **`deque`** for efficient queues and for keeping only the most recent N items.
- Use **`namedtuple`** to give names to the fields of a tuple.
- Know that `OrderedDict` and `ChainMap` exist and when you might see them.
- Choose between a plain dictionary and the `collections` tools for common test-data tasks.

---

## Why This Matters

In the previous lesson you wrote this counting code by hand:

```python
counts = {}
for status in statuses:
    counts[status] = counts.get(status, 0) + 1
```

It works, but it is the kind of pattern that appears over and over: *count things*, *group things*, *keep the last few things*. Python's standard library includes the **`collections`** module, which provides specialised containers that do exactly these jobs in less code with fewer bugs.

For a test engineer this means: counting failures by type, grouping tests by module or by status, keeping the last 5 log lines before a failure, or representing a test result as a readable record. Today's demo ("Model test data with lists/dicts/sets and Counter/defaultdict") and exercise (de-duplicate, group, look up) apply these tools directly.

---

## The Concept

### 1. What Is a Module?

A **module** is a file of ready-made Python code that you can bring into your program. Python ships with a large **standard library**, a collection of modules for maths, dates, random numbers, files, and much more, so you don't have to write everything yourself. (You get them automatically when you install Python; no `pip install` needed.)

To use a module you **import** it.

#### Style 1: import the module, use dotted names

```python
import collections

counts = collections.Counter(["a", "b", "a"])
print(counts)
```

You write `module_name.thing`.

#### Style 2: import specific names

```python
from collections import Counter

counts = Counter(["a", "b", "a"])
```

Now you can use `Counter` directly. You can import several names at once: `from collections import Counter, defaultdict, deque`.

#### Style 3: rename on import

```python
import collections as col
```

Used for modules with long names (you'll see it often in data and testing libraries).

**Where to put imports:** at the very top of your file, before other code. In Tuesday's guessing-game exercise you may have used `import random`, which is exactly this idea.

You can read a module's documentation from the terminal with `python -m pydoc collections`, or look at the official docs online (linked below).

The `collections` module contains several tools. Today's focus: **`Counter`**, **`defaultdict`**, **`deque`** and **`namedtuple`**.

---

### 2. `Counter`: Counting Things

`Counter` is a special dictionary designed for counting. Give it any collection (or a string) and it returns a dictionary mapping each distinct item to how many times it appeared.

```python
from collections import Counter

statuses = ["PASS", "FAIL", "PASS", "PASS", "FAIL", "SKIP"]

summary = Counter(statuses)
print(summary)
```

```text
Counter({'PASS': 3, 'FAIL': 2, 'SKIP': 1})
```

That's the whole counting loop from before, in one line.

#### 2.1 Using the counts

A `Counter` behaves like a dictionary:

```python
print(summary["PASS"])          # 3
print(summary["FAIL"])          # 2
print(summary["BLOCKED"])       # 0   <- a missing item gives 0, NOT a KeyError
print(len(summary))             # 3  -> distinct items
print(sum(summary.values()))    # 6  -> total count

for status, count in summary.items():
    print(f"{status}: {count}")
```

The "missing key gives 0" behaviour is really convenient for reports. (It does *not* add the key; it just returns 0.)

#### 2.2 `most_common()`

```python
print(summary.most_common())       # [('PASS', 3), ('FAIL', 2), ('SKIP', 1)]
print(summary.most_common(1))      # [('PASS', 3)]   -> the single most common
print(summary.most_common(2))      # the top 2
```

It returns a **list of `(item, count)` tuples**, sorted from highest to lowest count. To get just the top item:

```python
top_status, top_count = summary.most_common(1)[0]
print(top_status, top_count)       # PASS 3
```

(That line combines indexing, from the previous lessons: `[0]` takes the first tuple, which is then unpacked.)

#### 2.3 Counting characters and words

```python
letters = Counter("automation")
print(letters)
# Counter({'a': 2, 't': 2, 'o': 2, 'u': 1, 'm': 1, 'i': 1, 'n': 1})

words = "error timeout error retry error timeout".split()
print(Counter(words).most_common(2))
# [('error', 3), ('timeout', 2)]
```

#### 2.4 Updating and arithmetic

```python
run1 = Counter(["PASS", "PASS", "FAIL"])
run2 = Counter(["PASS", "FAIL", "FAIL"])

run1.update(run2)          # add run2's counts into run1
print(run1)                # Counter({'PASS': 3, 'FAIL': 3})

run1.update(["SKIP"])      # you can also update with a list of items
```

Counters can also be added, subtracted and compared:

```python
print(run1 + run2)         # combined totals
print(run1 - run2)         # subtract (negative/zero results are dropped)
```

```python
before = Counter({"PASS": 8, "FAIL": 2})
after = Counter({"PASS": 9, "FAIL": 1})
print(after - before)      # Counter({'PASS': 1})   -> what increased
print(before - after)      # Counter({'FAIL': 1})   -> what decreased
```

#### 2.5 Counter for finding duplicates

```python
test_ids = ["TC-001", "TC-002", "TC-001", "TC-003", "TC-002", "TC-001"]

counts = Counter(test_ids)

for test_id, count in counts.items():
    if count > 1:
        print(f"{test_id} appears {count} times")
```

```text
TC-001 appears 3 times
TC-002 appears 2 times
```

This is a very practical data-quality check for test suites.

---

### 3. `defaultdict`: Dictionaries With Automatic Defaults

Recall the problem with regular dictionaries: reading a missing key raises `KeyError`, and building a "group" requires a check first.

Grouping test IDs by module with a normal dictionary:

```python
tests = [("TC-001", "login"), ("TC-002", "search"), ("TC-003", "login")]

groups = {}
for test_id, module in tests:
    if module not in groups:
        groups[module] = []          # must create the list first
    groups[module].append(test_id)

print(groups)    # {'login': ['TC-001', 'TC-003'], 'search': ['TC-002']}
```

A **`defaultdict`** removes the check. You tell it what kind of *default value* to create whenever a missing key is accessed:

```python
from collections import defaultdict

groups = defaultdict(list)           # missing keys automatically get an empty list

for test_id, module in tests:
    groups[module].append(test_id)   # no "if" needed!

print(groups)
# defaultdict(<class 'list'>, {'login': ['TC-001', 'TC-003'], 'search': ['TC-002']})
print(dict(groups))                  # convert to a plain dictionary for tidy output
```

How it works: `defaultdict(list)` means "if a key doesn't exist, call `list()` to create a new empty list and store it under that key". `list`, `int`, `set` and `str` are all valid factories: you pass the **type name without parentheses**.

| Factory | Default value | Typical use |
|---|---|---|
| `defaultdict(list)` | `[]` | **Grouping** items under a key |
| `defaultdict(int)` | `0` | **Counting** (like `Counter`) |
| `defaultdict(set)` | `set()` | Grouping with **unique** values |
| `defaultdict(float)` | `0.0` | Summing amounts |

#### 3.1 Counting with `defaultdict(int)`

```python
counts = defaultdict(int)

for status in ["PASS", "FAIL", "PASS"]:
    counts[status] += 1             # a missing key starts at 0

print(dict(counts))                 # {'PASS': 2, 'FAIL': 1}
```

`Counter` is usually nicer for pure counting, but `defaultdict(int)` is useful when you count something *other* than a simple list of items, such as adding up times:

#### 3.2 Totalling per group

```python
results = [
    ("login", 1.2), ("search", 0.8), ("login", 2.0), ("checkout", 3.1), ("search", 1.0),
]

total_time = defaultdict(float)
for module, seconds in results:
    total_time[module] += seconds

for module, total in total_time.items():
    print(f"{module:<10} {total:.1f}s")
```

```text
login      3.2s
search     1.8s
checkout   3.1s
```

#### 3.3 Grouping unique values with `defaultdict(set)`

```python
browsers_by_module = defaultdict(set)

runs = [("login", "Chrome"), ("login", "Edge"), ("login", "Chrome"), ("search", "Chrome")]

for module, browser in runs:
    browsers_by_module[module].add(browser)

print(dict(browsers_by_module))
# {'login': {'Chrome', 'Edge'}, 'search': {'Chrome'}}
```

#### 3.4 A caution

Because reading a missing key **creates** it, even a harmless lookup adds an entry:

```python
groups = defaultdict(list)
print(groups["unknown"])        # [] ... and now 'unknown' exists in groups
print(len(groups))              # 1
```

If you only want to *check* whether a key exists, use `"key" in groups` rather than `groups["key"]`.

---

### 4. `deque`: A Double-Ended Queue

A **`deque`** (pronounced "deck", short for *double-ended queue*) is like a list that is fast to add or remove items at **both ends**. A plain list is slow when you insert or remove at the front (`pop(0)`), because everything has to shift along.

```python
from collections import deque

queue = deque(["TC-001", "TC-002", "TC-003"])

queue.append("TC-004")        # add to the right end
queue.appendleft("TC-000")    # add to the left end
print(queue)                  # deque(['TC-000', 'TC-001', 'TC-002', 'TC-003', 'TC-004'])

first = queue.popleft()       # remove from the left end (returns it)
last = queue.pop()            # remove from the right end
print(first, last)            # TC-000 TC-004
print(queue)                  # deque(['TC-001', 'TC-002', 'TC-003'])
```

| Method | Meaning |
|---|---|
| `append(x)` | Add on the right |
| `appendleft(x)` | Add on the left |
| `pop()` | Remove and return from the right |
| `popleft()` | Remove and return from the left |
| `extend(it)` / `extendleft(it)` | Add many |
| `rotate(n)` | Rotate items |
| `clear()` | Empty it |

A deque supports `len`, `in`, looping and `queue[0]`, but not slices.

**A test queue:** tests waiting to run, taken from the front in first-in-first-out order.

```python
waiting = deque(["TC-1", "TC-2", "TC-3"])

while waiting:                         # an empty deque is falsy
    current = waiting.popleft()
    print(f"Running {current}")
```

#### 4.1 `maxlen`: keep only the most recent items

Give a deque a maximum length, and old items fall off automatically when new ones are added:

```python
recent_logs = deque(maxlen=3)

for line in ["line 1", "line 2", "line 3", "line 4", "line 5"]:
    recent_logs.append(line)

print(recent_logs)       # deque(['line 3', 'line 4', 'line 5'], maxlen=3)
```

This is perfect for **"what happened just before the failure?"**: keep the last 5 log lines and print them when an error appears.

```python
history = deque(maxlen=2)

for line in ["INFO start", "INFO login", "INFO search", "ERROR crash", "INFO end"]:
    if line.startswith("ERROR"):
        print("Context before error:", list(history))
        print("Error:", line)
    history.append(line)
```

```text
Context before error: ['INFO login', 'INFO search']
Error: ERROR crash
```

---

### 5. `namedtuple`: Tuples With Names

A normal tuple record needs you to remember which index means what:

```python
result = ("TC-001", "PASS", 1.2)
print(result[1])        # was index 1 the status? or the title?
```

A **`namedtuple`** lets you access the fields by name while keeping tuple behaviour (immutable, unpackable, light-weight):

```python
from collections import namedtuple

TestResult = namedtuple("TestResult", ["test_id", "status", "duration"])

result = TestResult("TC-001", "PASS", 1.2)

print(result.test_id)       # TC-001
print(result.status)        # PASS
print(result[2])            # 1.2   (index still works)
print(result)               # TestResult(test_id='TC-001', status='PASS', duration=1.2)

test_id, status, duration = result    # unpacking works
```

`namedtuple("TestResult", [...])` builds a **new tuple type** named `TestResult` with those field names; you then create records by calling it like a function. You can also pass the field names as a string: `namedtuple("TestResult", "test_id status duration")`.

Useful extras:

```python
print(result._asdict())            # {'test_id': 'TC-001', 'status': 'PASS', 'duration': 1.2}
slower = result._replace(duration=2.5)    # a modified COPY (tuples can't change)
```

`namedtuple` sits between a tuple (light but unlabeled) and a dictionary (labeled but looser), and it is a gentle step toward **classes**, which you'll meet on Friday.

---

### 6. Other Tools You May See

- **`OrderedDict`**: a dictionary that remembers insertion order. Regular dictionaries have done this since Python 3.7, so you rarely need it today, but you'll see it in older code. It still offers extras such as `move_to_end()`.
- **`ChainMap`**: groups several dictionaries into one searchable "view" (for example, command-line options, then environment settings, then defaults). It's useful in configuration handling, and an advanced topic for later.
- Later in the program you will also meet other standard-library modules for dates, files and randomness. The `import` mechanism is the same.

---

### 7. Choosing the Right Tool

| Task | Plain Python | `collections` tool |
|---|---|---|
| Count occurrences | Dictionary with `.get()` | **`Counter`** |
| Top N most common | Manual sort | **`Counter.most_common(n)`** |
| Group items by key | Dictionary with `if key not in` | **`defaultdict(list)`** |
| Group unique items by key | Same | **`defaultdict(set)`** |
| Queue (add right, take left) | `list.pop(0)` (slow for big lists) | **`deque`** |
| Last N items only | Slicing a growing list | **`deque(maxlen=N)`** |
| Readable fixed record | Tuple or dict | **`namedtuple`** |

Don't use these tools just to look clever. A short plain dictionary is fine for a tiny job; use `collections` when it makes the code **shorter and clearer**.

---

### 8. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Forgetting to import | `NameError: name 'Counter' is not defined` | Add `from collections import Counter` |
| Naming your file `collections.py` | Python imports *your* file instead | Choose a different file name |
| Parentheses on the factory | `defaultdict(list())` | Pass `list` without `()` |
| Expecting `Counter` to hold the original list | It stores only counts | Keep the original data separately |
| Unwanted keys in `defaultdict` | A lookup creates the key | Use `in` to check |
| Slicing a `deque` | `TypeError` | Convert with `list(d)[...]` |
| Changing a `namedtuple` field | `AttributeError` | Use `._replace()` to make a copy |
| Printing a `defaultdict` raw | Messy output | `dict(my_defaultdict)` |
| Using `Counter` on unhashable items | Lists can't be counted | Convert items to tuples or strings |

---

### 9. Practice Activities

1. **Import styles.** Import `Counter` three ways: `import collections`, `from collections import Counter`, and `import collections as col`. Count `["a", "b", "a"]` with each.
2. **Status summary.** Given a list of 12 test statuses of your own (`PASS`, `FAIL`, `SKIP`, `ERROR`), use `Counter` to print each count, the most common status and the percentage of passes.
3. **Missing key.** Show what happens when you look up a status that wasn't counted. Compare it with a regular dictionary.
4. **Duplicates.** Given `["TC-1", "TC-2", "TC-1", "TC-3", "TC-3", "TC-3"]`, print only the IDs that appear more than once and how many times.
5. **Word frequency.** Split the sentence `"the login failed and the retry failed and the test stopped"` into words and print the top 3 words.
6. **Grouping.** Given pairs like `("TC-001", "login")`, `("TC-002", "search")`, `("TC-003", "login")`, `("TC-004", "cart")`, group IDs by module using `defaultdict(list)` and print each module with its tests.
7. **Totals.** Given `(module, seconds)` pairs, compute the total time and the average per module using `defaultdict`.
8. **Queue.** Use a `deque` to process a queue of five test IDs, printing `Running ...` for each. Then add two high-priority tests to the *front* of a new queue with `appendleft`.
9. **Context.** Use `deque(maxlen=3)` to remember the last three log lines and print them when a line contains `"ERROR"`.
10. **Records.** Create a `namedtuple` called `TestCase` with `id`, `title` and `priority`. Create three records, print one field by name, and use `_replace` to change a priority.
11. **Compare tools.** Re-write the counting loop from the practice in the previous lesson using `Counter` and describe how many lines you saved.

---

## Summary

- A **module** is reusable code you bring in with `import`; the **standard library** comes with Python. Use `import x`, `from x import y` or `import x as z`, at the top of the file.
- **`Counter`**: counts items automatically; missing items give `0`; `most_common(n)` lists the top items; counters can be updated, added and subtracted.
- **`defaultdict(factory)`**: a dictionary that creates default values for missing keys; `list` for grouping, `set` for unique grouping, `int`/`float` for totals. Pass the type **without parentheses**, and beware that lookups create keys.
- **`deque`**: fast adds and removes at both ends; `popleft()` for queues; `deque(maxlen=n)` keeps just the most recent items.
- **`namedtuple`**: lightweight, immutable records with named fields; `._replace()` and `._asdict()` are helpers.
- `OrderedDict` and `ChainMap` exist but are less common today.
- Use these tools when they make code shorter and clearer than plain lists and dictionaries.
- Next: apply everything to realistic **test-data scenarios**.

---

## Additional Resources

- Python documentation: `collections` module: https://docs.python.org/3/library/collections.html
- Python Tutorial: Modules: https://docs.python.org/3/tutorial/modules.html
- Real Python: The Python `collections` Module: https://realpython.com/python-collections-module/
