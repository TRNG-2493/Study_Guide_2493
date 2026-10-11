# Collection Operations and Methods

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a method is and how it differs from a built-in function.
- Use the built-in functions that work on all collections: `len`, `sum`, `min`, `max`, `sorted`, `any`, `all`.
- Add, remove, find, count, sort and reverse items in a list with its methods.
- Read, update, remove and merge dictionary entries safely.
- Add, remove and compare sets with set methods.
- Use the few tuple methods and understand why tuples have so few.
- Understand the difference between `list.sort()` and `sorted()`, and between copying and aliasing.
- Use `enumerate()` and `zip()` to loop more elegantly.
- Convert between strings and lists with `.split()` and `.join()`.

---

## Why This Matters

You can now create collections and pick items out of them. Real programs also need to **change** them: add a new test result, remove a retired test, sort tests by priority, find out whether a value is already there, merge two sets of configuration. Python's built-in operations and **methods** do all of this for you, so you rarely have to write the logic yourself.

For test automation, these are the everyday tools of test-data handling: build up a list of results as tests run, count failures, de-duplicate IDs, look up expected values in a dictionary, merge default settings with overrides. Today's exercise (a test-data manager that de-duplicates, groups and looks up data) will lean on almost every tool in this lesson.

---

## The Concept

### 1. Methods vs Functions

You have already used both without a formal introduction:

```python
len(browsers)             # a function: function(thing)
browsers.append("Edge")   # a method: thing.method()
```

- A **function** (like `len`, `print`, `sorted`) stands alone: you pass the data in.
- A **method** belongs to a particular type of object and is called with a dot after the object: `object.method(arguments)`. A list has list methods, a dictionary has dictionary methods, and so on. (Friday's lessons on classes will explain where methods come from; for now, just learn to call them.)

One crucial habit: **find out whether a method changes the object or returns a new one.** Mutable collections (lists, dicts, sets) mostly change **in place** and return `None`. Immutable types (strings, tuples) can only return new values. Writing `my_list = my_list.append(5)` is a classic bug: `append` returns `None`, so `my_list` becomes `None`.

---

### 2. Built-in Functions for Collections

These work on most collections:

```python
scores = [72, 95, 60, 88, 95]

print(len(scores))      # 5       -> number of items
print(sum(scores))      # 410     -> total of numbers
print(min(scores))      # 60
print(max(scores))      # 95
print(sum(scores) / len(scores))    # 82.0   -> average
```

`sorted()` returns a **new sorted list** and leaves the original alone:

```python
print(sorted(scores))                  # [60, 72, 88, 95, 95]
print(sorted(scores, reverse=True))    # [95, 95, 88, 72, 60]
print(scores)                          # unchanged: [72, 95, 60, 88, 95]
```

It works on strings too (alphabetical), and on any collection, including sets, tuples and dictionary keys.

`any()` and `all()` check a collection of booleans:

```python
results = [True, True, False]

print(all(results))     # False  -> are ALL true?
print(any(results))     # True   -> is AT LEAST ONE true?
```

A great fit for tests: `all(results)` means "every check passed".

---

### 3. List Methods

Let's work with a test queue:

```python
queue = ["TC-001", "TC-002", "TC-003"]
```

#### 3.1 Adding items

| Method | What it does | Example | List afterwards |
|---|---|---|---|
| `append(x)` | Add **one** item at the end | `queue.append("TC-004")` | `[..., 'TC-004']` |
| `insert(i, x)` | Insert at index `i` | `queue.insert(0, "TC-000")` | `['TC-000', 'TC-001', ...]` |
| `extend(iterable)` | Add **each item** from another collection | `queue.extend(["TC-005", "TC-006"])` | adds two items |

The difference between `append` and `extend` trips up many beginners:

```python
a = [1, 2]
a.append([3, 4])
print(a)           # [1, 2, [3, 4]]    -> the whole list as ONE item

b = [1, 2]
b.extend([3, 4])
print(b)           # [1, 2, 3, 4]      -> items added individually
```

`b += [3, 4]` has the same effect as `extend`.

#### 3.2 Removing items

| Method | What it does |
|---|---|
| `remove(x)` | Removes the **first** item equal to `x`; `ValueError` if missing |
| `pop()` | Removes and **returns** the last item |
| `pop(i)` | Removes and returns the item at index `i` |
| `clear()` | Removes everything |
| `del lst[i]` | Statement that removes the item at index `i` (also works with slices) |

```python
queue = ["TC-001", "TC-002", "TC-003", "TC-004"]

queue.remove("TC-002")       # remove by value
print(queue)                 # ['TC-001', 'TC-003', 'TC-004']

last = queue.pop()           # remove and get the last item
print(last)                  # TC-004
print(queue)                 # ['TC-001', 'TC-003']

first = queue.pop(0)         # remove and get the first
print(first)                 # TC-001
```

`pop(0)` makes a list act like a queue (first in, first out), whereas plain `pop()` acts like a stack (last in, first out).

Remember `remove` raises an error if the value isn't there, so guard it:

```python
if "TC-999" in queue:
    queue.remove("TC-999")
```

`remove` deletes **only the first** match. To remove all matches, you'd use a loop (or build a new list), which is a reason to be careful about duplicates.

> **Warning:** do not add or remove items from a list *while looping over it*. Doing so can silently skip items. Loop over a copy (`for x in queue[:]:`) or build a new list instead.

#### 3.3 Searching and counting

```python
statuses = ["PASS", "FAIL", "PASS", "PASS", "FAIL"]

print(statuses.count("FAIL"))       # 2    -> how many times
print(statuses.index("FAIL"))       # 1    -> position of the FIRST match
print("PASS" in statuses)           # True -> membership
```

`index` raises `ValueError` if the value isn't present, so check with `in` first.

#### 3.4 Sorting and reversing

```python
numbers = [30, 10, 20]

numbers.sort()                  # sorts IN PLACE (returns None)
print(numbers)                  # [10, 20, 30]

numbers.sort(reverse=True)
print(numbers)                  # [30, 20, 10]

numbers.reverse()               # reverses IN PLACE
print(numbers)                  # [10, 20, 30]
```

**`.sort()` vs `sorted()`:**

| | `my_list.sort()` | `sorted(my_list)` |
|---|---|---|
| Changes the original? | **Yes** | No |
| Returns | `None` | A new list |
| Works on | Lists only | Any collection |

A classic bug: `numbers = numbers.sort()` sets `numbers` to `None`. Use either `numbers.sort()` or `numbers = sorted(numbers)`.

**Sorting strings** is case-sensitive: uppercase letters sort before lowercase. A built-in function can be used as the *sort key*:

```python
names = ["login", "Search", "api", "Checkout"]

print(sorted(names))                # ['Checkout', 'Search', 'api', 'login']
print(sorted(names, key=str.lower)) # ['api', 'Checkout', 'login', 'Search']
print(sorted(names, key=len))       # ['api', 'login', 'Search', 'Checkout']
```

`key=` tells Python *what to compare* for each item. (More flexible custom sort rules use lambda functions, which we cover on **Thursday**.)

#### 3.5 Copying a list

Back to the aliasing problem from the slicing lesson:

```python
original = [1, 2, 3]

copy1 = original.copy()      # method
copy2 = original[:]          # slice
copy3 = list(original)       # constructor
alias = original             # NOT a copy
```

The first three create independent lists; `alias` is another name for the same one. If your list contains other lists or dictionaries, the copy is *shallow*: the inner objects are shared. (Deep copying is an advanced topic for later.)

#### 3.6 Summary table of list methods

| Method | Changes list? | Returns |
|---|---|---|
| `append(x)` | Yes | `None` |
| `extend(it)` | Yes | `None` |
| `insert(i, x)` | Yes | `None` |
| `remove(x)` | Yes | `None` |
| `pop([i])` | Yes | The removed item |
| `clear()` | Yes | `None` |
| `sort()` | Yes | `None` |
| `reverse()` | Yes | `None` |
| `index(x)` | No | Position |
| `count(x)` | No | Number |
| `copy()` | No | A new list |

---

### 4. Strings and Lists: `split()` and `join()`

Two string methods bridge the world of text and lists.

**`.split()`** breaks a string into a list of pieces:

```python
line = "TC-001,Valid login,PASS"
parts = line.split(",")
print(parts)            # ['TC-001', 'Valid login', 'PASS']

words = "run all smoke tests".split()      # no argument: split on any whitespace
print(words)            # ['run', 'all', 'smoke', 'tests']
```

Combined with unpacking:

```python
test_id, title, status = line.split(",")
```

This is exactly how you parse CSV-style data and log lines.

**`.join()`** does the reverse: it glues a list of strings together using the string it is called on as the separator:

```python
ids = ["TC-001", "TC-002", "TC-003"]

print(", ".join(ids))         # TC-001, TC-002, TC-003
print("\n".join(ids))         # one per line
```

`join` only accepts strings. For numbers, convert first: `", ".join(str(n) for n in numbers)` (that `for` inside is a shortcut we won't study today; you can also build the list of strings with an ordinary loop).

---

### 5. `enumerate()` and `zip()`

#### 5.1 `enumerate()`: item and position

When you need the index as well as the item:

```python
tests = ["Login", "Search", "Checkout"]

for position, name in enumerate(tests):
    print(position, name)
```

```text
0 Login
1 Search
2 Checkout
```

Start counting from 1 for human-friendly numbering:

```python
for number, name in enumerate(tests, start=1):
    print(f"{number}. {name}")
```

```text
1. Login
2. Search
3. Checkout
```

This is much cleaner than `for i in range(len(tests))` with `tests[i]`.

#### 5.2 `zip()`: loop over two collections together

```python
ids = ["TC-001", "TC-002", "TC-003"]
statuses = ["PASS", "FAIL", "PASS"]

for test_id, status in zip(ids, statuses):
    print(f"{test_id}: {status}")
```

```text
TC-001: PASS
TC-002: FAIL
TC-003: PASS
```

`zip` pairs the first with the first, second with second, and so on, stopping at the shortest collection. You can also build a dictionary from two lists: `dict(zip(ids, statuses))`.

---

### 6. Dictionary Methods

```python
test_case = {"id": "TC-001", "title": "Valid login", "priority": "High"}
```

#### 6.1 Looking things up

| Operation | Result |
|---|---|
| `test_case["title"]` | `'Valid login'`; `KeyError` if missing |
| `test_case.get("owner")` | `None` if missing |
| `test_case.get("owner", "n/a")` | `'n/a'` if missing |
| `"owner" in test_case` | `False` (checks keys) |
| `len(test_case)` | `3` |

#### 6.2 Views: `keys()`, `values()`, `items()`

```python
print(list(test_case.keys()))      # ['id', 'title', 'priority']
print(list(test_case.values()))    # ['TC-001', 'Valid login', 'High']
print(list(test_case.items()))
# [('id', 'TC-001'), ('title', 'Valid login'), ('priority', 'High')]
```

These return "views" of the dictionary that stay in sync with it; wrap them in `list()` when you want an ordinary list. Looping with `for key, value in test_case.items():` is the most common use.

Checking values: `"High" in test_case.values()` is `True`.

#### 6.3 Adding, updating, removing

```python
test_case["owner"] = "Priya"                 # add or replace one key

test_case.update({"status": "PASS", "priority": "Critical"})   # many at once
print(test_case)
```

`update` adds new keys and overwrites existing ones. It's perfect for **merging defaults with overrides**:

```python
defaults = {"browser": "Chrome", "timeout": 30, "headless": False}
overrides = {"browser": "Firefox", "headless": True}

settings = defaults.copy()
settings.update(overrides)
print(settings)      # {'browser': 'Firefox', 'timeout': 30, 'headless': True}
```

Removing:

```python
status = test_case.pop("status")             # removes the key and returns its value
test_case.pop("missing", None)               # with a default, no error if absent
del test_case["owner"]                       # statement; KeyError if missing
test_case.clear()                            # removes everything
```

#### 6.4 `setdefault()`

`setdefault(key, default)` returns the value for the key; if the key is absent, it first inserts it with the default:

```python
counts = {}
counts.setdefault("PASS", 0)       # creates "PASS": 0
counts["PASS"] += 1
print(counts)                      # {'PASS': 1}
```

#### 6.5 The counting pattern

Counting how often each item occurs is extremely common:

```python
statuses = ["PASS", "FAIL", "PASS", "PASS", "FAIL", "SKIP"]

counts = {}
for status in statuses:
    counts[status] = counts.get(status, 0) + 1

print(counts)      # {'PASS': 3, 'FAIL': 2, 'SKIP': 1}
```

`counts.get(status, 0)` returns the current count (or 0 if the status hasn't been seen), and we add 1. Python's `collections` module offers a ready-made tool for this, which is the next lesson's topic.

#### 6.6 Dictionary methods summary

| Method | Purpose |
|---|---|
| `get(k, default)` | Safe lookup |
| `keys()`, `values()`, `items()` | Views for looping |
| `update(other)` | Merge/overwrite |
| `pop(k, default)` | Remove and return |
| `setdefault(k, default)` | Get, inserting a default if missing |
| `clear()` | Empty it |
| `copy()` | Shallow copy |

---

### 7. Set Methods

```python
tags = {"smoke", "login"}
```

| Method / operator | Purpose |
|---|---|
| `add(x)` | Add an item |
| `remove(x)` | Remove; `KeyError` if missing |
| `discard(x)` | Remove; no error if missing |
| `pop()` | Remove and return an **arbitrary** item |
| `clear()` | Empty it |
| `update(other)` | Add all items from another collection |
| `a.union(b)` / `a \| b` | Items in either |
| `a.intersection(b)` / `a & b` | Items in both |
| `a.difference(b)` / `a - b` | In `a` but not in `b` |
| `a.symmetric_difference(b)` / `a ^ b` | In exactly one |
| `a.issubset(b)` / `a <= b` | Is every item of `a` in `b`? |
| `a.issuperset(b)` / `a >= b` | Does `a` contain all of `b`? |
| `a.isdisjoint(b)` | Do they share nothing? |

```python
required = {"id", "title", "status"}
provided = {"id", "title"}

print(required - provided)           # {'status'}  -> what is missing
print(provided.issubset(required))   # True
print(required.issubset(provided))   # False
```

This is a neat way to validate that a record has all the required fields.

Note: the method versions (`union`, `intersection`...) accept any collection; the operators need both sides to be sets.

---

### 8. Tuple Methods

Because tuples are immutable, they have only two methods, both read-only:

```python
t = (1, 2, 2, 3, 2)

print(t.count(2))      # 3
print(t.index(3))      # 3
```

Everything else (`len`, `in`, indexing, slicing, `min`, `max`, `sum`, `sorted`, looping) comes from the general sequence tools described above. `sorted(t)` returns a **list**.

To "change" a tuple, convert to a list, change it and convert back, or just build a new tuple: `t = t + (4,)`.

---

### 9. Working Example: Processing a Result Set

```python
results = [
    {"id": "TC-001", "status": "PASS", "time": 1.2},
    {"id": "TC-002", "status": "FAIL", "time": 3.4},
    {"id": "TC-003", "status": "PASS", "time": 0.8},
    {"id": "TC-004", "status": "FAIL", "time": 2.1},
]

failed_ids = []
total_time = 0.0

for result in results:
    total_time += result["time"]
    if result["status"] == "FAIL":
        failed_ids.append(result["id"])

failed_ids.sort()
print(f"Total: {len(results)}")
print(f"Failed: {', '.join(failed_ids)}")
print(f"Average time: {total_time / len(results):.2f}s")
```

```text
Total: 4
Failed: TC-002, TC-004
Average time: 1.88s
```

The program uses a loop, a conditional, a list method (`append`, `sort`), `join`, `len`, dictionary access and an f-string, which is how real test code feels.

---

### 10. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Assigning the result of an in-place method | `items = items.sort()` | Just `items.sort()` (or `sorted`) |
| Confusing `append` and `extend` | `a.append([1, 2])` adds a nested list | Use `extend` to add each item |
| `remove` on a missing value | `ValueError` | Check with `in` first |
| Modifying a list while looping over it | Skipped items | Loop over a copy or build a new list |
| `dict["missing"]` | `KeyError` | `.get()` or `in` |
| `my_set = {}` for an empty set | Creates a dict | `set()` |
| Expecting `pop()` on a set to be predictable | Arbitrary item | Use a list if order matters |
| `"-".join([1, 2, 3])` | `TypeError` | Convert items to strings first |
| Believing `b = a` copies | Shared object | `a.copy()` |
| Sorting mixed types | `[3, "a"]` → `TypeError` | Keep types consistent |

---

### 11. Practice Activities

1. **Queue.** Start with an empty list. Append five test IDs, insert one at the front, remove one by value, pop the last, and print the list after each step.
2. **Stats.** Given `[72, 95, 60, 88, 95, 70]`, print the count, sum, minimum, maximum and average. Print the list sorted high to low without changing the original.
3. **Sort vs sorted.** Show that `sort()` changes the list while `sorted()` doesn't. What does `print(my_list.sort())` print and why?
4. **Counting.** Given a list of statuses, count each distinct status using a dictionary and `.get()`. Also use `.count()` for just `"FAIL"`.
5. **Split and join.** Take `"TC-001;TC-002;TC-003"`, split it on `;`, sort the pieces in reverse order and join them with `" | "`.
6. **Parsing.** Parse the lines `"TC-001,Login,PASS"` and `"TC-002,Logout,FAIL"` into dictionaries with keys `id`, `title`, `status`, using `split` and unpacking. Put both in a list.
7. **Merge.** Merge `defaults = {"browser": "Chrome", "retries": 2}` with `{"retries": 5, "env": "staging"}` without altering `defaults`.
8. **Sets.** Given `required = {"id", "title", "priority"}` and a record with keys `{"id", "title"}`, find the missing fields. Then check if the record has any extra fields beyond the required ones.
9. **enumerate and zip.** Print a numbered list (starting at 1) of test names, and then use `zip` to pair names with statuses.
10. **Safe remove.** Write code that removes `"TC-999"` from a list only if present. Then explain why `remove()` only deletes one copy of a duplicated value.
11. **Spot the bug.**
    ```python
    ids = ["TC-3", "TC-1", "TC-2"]
    ids = ids.sort()
    print(ids[0])
    ```
    What error occurs and why? Fix it.

---

## Summary

- **Functions** take data as an argument (`len(x)`); **methods** belong to an object (`x.append(...)`). In-place methods on mutable types usually return `None`.
- Built-ins: `len`, `sum`, `min`, `max`, `sorted`, `any`, `all` work across many collections; `sorted()` returns a new list, while `list.sort()` sorts in place.
- **List methods:** `append`, `extend`, `insert` (add); `remove`, `pop`, `clear`, `del` (remove); `count`, `index`, `in` (search); `sort`, `reverse`, `copy`.
- Never loop over a list while changing its size; avoid `x = x.sort()`.
- `.split()` turns text into a list, and `separator.join(list)` turns a list of strings back into text.
- `enumerate()` gives index and item; `zip()` walks collections side by side.
- **Dictionary methods:** `get`, `keys`, `values`, `items`, `update`, `pop`, `setdefault`, `copy`; the counting pattern is `counts[k] = counts.get(k, 0) + 1`.
- **Set methods:** `add`, `remove`, `discard`, `update` and operations `union`, `intersection`, `difference`, `issubset`; great for comparing "planned vs executed" or "required vs provided".
- **Tuples** have only `count` and `index`.
- Next: the **`collections` module** gives you ready-made, more powerful versions of counting, grouping and queues.

---

## Additional Resources

- Python Tutorial: More on Lists: https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
- Python documentation: Built-in dictionary and set types: https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
- Real Python: Python Dictionaries: https://realpython.com/python-dicts/
