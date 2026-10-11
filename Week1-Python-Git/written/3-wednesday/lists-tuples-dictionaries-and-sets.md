# Lists, Tuples, Dictionaries and Sets

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a collection is and why single variables are not enough for real data.
- Create and use **lists**, **tuples**, **dictionaries** and **sets**.
- Explain the difference between **mutable** and **immutable** data types.
- Describe the key properties of each collection: ordering, duplicates, mutability and how items are accessed.
- Loop over each kind of collection with `for`.
- Convert between collection types, for example removing duplicates with a set.
- Choose the right collection for a given test-data problem.

---

## Why This Matters

Until now, each variable held **one** value: one test ID, one score, one status. Real work involves *many* values at once:

- 200 test case IDs in a regression suite.
- The login credentials for 5 different test users, each with a username, password and role.
- A set of browsers to test on: Chrome, Firefox, Edge.
- The status codes your API is allowed to return.

You could create `test_1`, `test_2`, `test_3`, ... but that doesn't scale; you could never loop over them or count them. **Collections** are Python's way of holding many values under one name.

In test automation, collections are the backbone of **test data**. Data-driven tests run the same steps over a collection of inputs; reports are built from collections of results. Today's lessons (and the demo and exercise) show how to model and manage test data with these tools. You'll use loops from yesterday to walk through them, and conditionals to decide what to do with each item.

---

## The Concept

### 1. The Four Built-in Collections at a Glance

| Collection | Syntax | Ordered? | Duplicates? | Changeable? | Accessed by |
|---|---|---|---|---|---|
| **List** | `[1, 2, 3]` | Yes | Allowed | **Yes** (mutable) | Position (index) |
| **Tuple** | `(1, 2, 3)` | Yes | Allowed | **No** (immutable) | Position (index) |
| **Dictionary** | `{"a": 1, "b": 2}` | Yes (insertion order) | Keys must be unique | **Yes** | **Key** |
| **Set** | `{1, 2, 3}` | No | **Not allowed** | Yes (add/remove) | Membership only |

Two important ideas used in that table:

- **Mutable** means "can be changed after it is created". A list is mutable: you can add, remove or replace items. **Immutable** means it cannot be changed once created. You met an immutable type already: strings. A tuple is the collection equivalent.
- **Ordered** means items keep a fixed position, so "the first item" and "the third item" have meaning.

**Analogies:**

- A **list** is a shopping list: ordered, you can add and cross off items, duplicates are fine (two bottles of milk).
- A **tuple** is a row of seats in a theatre bought with a ticket: fixed positions, not meant to be rearranged.
- A **dictionary** is a phone book: you look up a *name* (key) to find a *number* (value).
- A **set** is a bag of unique badges: no duplicates and no order; you only care whether a badge is in the bag.

---

### 2. Lists

A **list** is an ordered, changeable sequence of items, written in square brackets, separated by commas.

```python
browsers = ["Chrome", "Firefox", "Edge"]
status_codes = [200, 201, 404, 500]
mixed = ["TC-001", 3, True, 4.5]       # lists can hold different types
empty = []                              # an empty list
```

Lists usually hold items of the same kind, but Python doesn't force this.

#### 2.1 Basic properties

```python
browsers = ["Chrome", "Firefox", "Edge"]

print(browsers)             # ['Chrome', 'Firefox', 'Edge']
print(len(browsers))        # 3   -> number of items
print(type(browsers))       # <class 'list'>
print("Edge" in browsers)   # True  -> membership test
print("Safari" in browsers) # False
```

`len()` works on every collection. `in` checks whether an item is present.

#### 2.2 Getting an item by position (index)

Each item has a numbered position called an **index**, starting at **0**:

```
 index:      0          1           2
 browsers = ["Chrome", "Firefox", "Edge"]
```

```python
print(browsers[0])    # Chrome
print(browsers[2])    # Edge
```

(The next lesson, **Indexing and slicing**, covers negative indexes, slices and errors in depth. For now, `[number]` gets one item.)

#### 2.3 Lists are mutable

You can change a list after creating it:

```python
browsers[1] = "Safari"          # replace the item at index 1
print(browsers)                 # ['Chrome', 'Safari', 'Edge']

browsers.append("Opera")        # add to the end
print(browsers)                 # ['Chrome', 'Safari', 'Edge', 'Opera']
```

A list is a **single object that changes in place**. Contrast this with a string, where `name.upper()` gives back a *new* string.

#### 2.4 Looping over a list

This is where yesterday's `for` loop becomes powerful. Instead of `range()`, loop directly over the items:

```python
test_ids = ["TC-001", "TC-002", "TC-003"]

for test_id in test_ids:
    print(f"Running {test_id}...")
```

```text
Running TC-001...
Running TC-002...
Running TC-003...
```

Read it as "for each `test_id` in `test_ids`". The loop variable takes each item in turn. This is the foundation of **data-driven testing**: one block of code, many pieces of data.

You can use a counter pattern, too:

```python
passed_count = 0
results = [True, True, False, True]

for result in results:
    if result:
        passed_count += 1

print(f"{passed_count} of {len(results)} passed")      # 3 of 4 passed
```

#### 2.5 Lists can contain lists (nesting)

```python
credentials = [
    ["admin", "admin123"],
    ["guest", "guest123"],
]

print(credentials[0])        # ['admin', 'admin123']
print(credentials[0][1])     # admin123   (item 1 of item 0)
```

Writing a collection over multiple lines is fine inside brackets, and it makes long data readable.

#### 2.6 Combining and repeating

```python
smoke = ["TC-001", "TC-002"]
regression = ["TC-010", "TC-011"]

all_tests = smoke + regression       # joins into a NEW list
print(all_tests)                     # ['TC-001', 'TC-002', 'TC-010', 'TC-011']

zeros = [0] * 5                      # [0, 0, 0, 0, 0]
```

---

### 3. Tuples

A **tuple** is an ordered sequence like a list, but **immutable**: once created, you cannot change, add or remove items. It is written with parentheses.

```python
screen_size = (1920, 1080)
point = (3, 4)
test_case = ("TC-001", "Login", "High")
```

```python
print(screen_size[0])          # 1920
print(len(screen_size))        # 2
```

Trying to change one gives an error:

```python
screen_size[0] = 1366
```

```text
TypeError: 'tuple' object does not support item assignment
```

#### 3.1 Single-item tuples need a comma

```python
not_a_tuple = (5)       # just the number 5 in brackets
a_tuple = (5,)          # a tuple with one item - note the comma
print(type(not_a_tuple), type(a_tuple))
```

```text
<class 'int'> <class 'tuple'>
```

Parentheses are optional: `size = 1920, 1080` also creates a tuple. It's the **commas** that make a tuple.

#### 3.2 Tuple unpacking

You can assign each item of a tuple to its own variable in one line:

```python
test_case = ("TC-001", "Login", "High")

test_id, title, priority = test_case

print(test_id)       # TC-001
print(title)         # Login
print(priority)      # High
```

The number of variables must match the number of items. Unpacking also works with lists, and you used it on Monday without knowing it: `x, y = 10, 20` was tuple unpacking! It also lets you swap two variables neatly:

```python
a, b = 1, 2
a, b = b, a
print(a, b)      # 2 1
```

#### 3.3 Why use a tuple instead of a list?

- **Safety:** data that should never change (screen resolutions, a fixed set of valid statuses, coordinates) can't be modified by accident.
- **Meaning:** a tuple often represents *one record* of mixed data (an ID, a title and a priority) whereas a list is typically *many similar things*.
- **Dictionary keys:** tuples can be used as dictionary keys; lists cannot (see below).
- Tuples are slightly lighter and faster than lists.

Looping works the same way:

```python
valid_statuses = ("PASS", "FAIL", "SKIPPED")

for status in valid_statuses:
    print(status)
```

---

### 4. Dictionaries

A **dictionary** (`dict`) stores data as **key-value pairs**. Instead of looking up an item by its position, you look it up by its **key**, like finding a word in a real dictionary.

```python
test_case = {
    "id": "TC-001",
    "title": "Valid login",
    "priority": "High",
    "automated": True,
}
```

- Curly braces `{ }` surround the dictionary.
- Each entry is `key: value`, separated by commas.
- Here the keys are strings, and the values are strings or a boolean, but values can be anything (numbers, lists, even other dictionaries).

This is the most natural way to represent a **record**, like one row of a test-data table, where each field has a name.

#### 4.1 Reading values

```python
print(test_case["title"])       # Valid login
print(test_case["priority"])    # High
```

If the key doesn't exist, you get a `KeyError`:

```python
print(test_case["owner"])
```

```text
KeyError: 'owner'
```

The safer way is `.get()`, which returns `None` (or a default you choose) when the key is missing:

```python
print(test_case.get("owner"))                  # None
print(test_case.get("owner", "Unassigned"))    # Unassigned
```

You can also check first: `"owner" in test_case` gives `False`. Note that `in` on a dictionary checks the **keys**.

#### 4.2 Adding, changing and removing entries

```python
test_case["owner"] = "Priya"          # add a new key
test_case["priority"] = "Critical"    # change an existing value
del test_case["automated"]            # remove a key and its value

print(test_case)
# {'id': 'TC-001', 'title': 'Valid login', 'priority': 'Critical', 'owner': 'Priya'}
```

The same syntax `dict[key] = value` both adds and updates: if the key exists, its value is replaced; otherwise, a new pair is created.

#### 4.3 Rules for keys

- Keys must be **unique**. Assigning an existing key replaces the value.
- Keys must be **immutable** (hashable): strings, numbers and tuples work; lists do not.
- Values have no restrictions and can repeat.

#### 4.4 Looping over a dictionary

```python
test_case = {"id": "TC-001", "title": "Valid login", "priority": "High"}

for key in test_case:                      # loops over keys
    print(key)

for value in test_case.values():           # loops over values
    print(value)

for key, value in test_case.items():       # loops over both
    print(f"{key}: {value}")
```

```text
id: TC-001
title: Valid login
priority: High
```

`.items()` gives pairs which are unpacked into `key` and `value`, the tuple unpacking you just learned.

#### 4.5 Nested dictionaries and a "list of dictionaries"

A dictionary can contain other dictionaries:

```python
users = {
    "admin": {"password": "admin123", "role": "administrator"},
    "guest": {"password": "guest123", "role": "viewer"},
}

print(users["admin"]["role"])      # administrator
```

The most common test-data shape of all is a **list of dictionaries**: a table where each dictionary is one row.

```python
test_cases = [
    {"id": "TC-001", "title": "Valid login", "status": "PASS"},
    {"id": "TC-002", "title": "Invalid password", "status": "FAIL"},
    {"id": "TC-003", "title": "Empty username", "status": "PASS"},
]

for case in test_cases:
    print(f"{case['id']:<8} {case['title']:<20} {case['status']}")
```

```text
TC-001   Valid login          PASS
TC-002   Invalid password     FAIL
TC-003   Empty username       PASS
```

(When using single quotes inside a double-quoted f-string, as in `case['id']`, you avoid clashing quotes.)

---

### 5. Sets

A **set** is an **unordered** collection of **unique** items, written with curly braces but *without* key-value pairs.

```python
browsers = {"Chrome", "Firefox", "Edge", "Chrome"}
print(browsers)          # {'Chrome', 'Edge', 'Firefox'}   (order may vary)
```

Notice what happened:

- The duplicate `"Chrome"` disappeared: sets keep only one of each.
- The printed order may differ from what you typed and can change between runs. Sets have **no index**: `browsers[0]` raises a `TypeError`.

#### 5.1 Creating an empty set

```python
empty_set = set()       # correct
not_a_set = {}          # this is an empty DICTIONARY!
```

#### 5.2 Adding, removing and testing

```python
tags = {"smoke", "login"}

tags.add("regression")       # add an item
tags.add("smoke")            # already there: nothing happens
tags.remove("login")         # remove (KeyError if missing)
tags.discard("missing")      # remove if present, no error if not

print("smoke" in tags)       # True - very fast membership testing
```

#### 5.3 Removing duplicates

The most practical beginner use of a set is to **de-duplicate** data:

```python
raw_ids = ["TC-001", "TC-002", "TC-001", "TC-003", "TC-002"]

unique_ids = set(raw_ids)
print(unique_ids)             # {'TC-003', 'TC-001', 'TC-002'}
print(len(raw_ids), len(unique_ids))      # 5 3
```

`set(...)` converts any collection into a set. To go back to a list, use `list(...)`; adding `sorted()` gives a tidy ordered list:

```python
print(sorted(unique_ids))      # ['TC-001', 'TC-002', 'TC-003']
```

#### 5.4 Set operations (like Venn diagrams)

```python
planned = {"TC-001", "TC-002", "TC-003", "TC-004"}
executed = {"TC-002", "TC-003", "TC-005"}

print(planned | executed)    # union: everything in either
print(planned & executed)    # intersection: in both
print(planned - executed)    # difference: planned but NOT executed
print(planned ^ executed)    # symmetric difference: in one but not both
```

```text
{'TC-001', 'TC-002', 'TC-003', 'TC-004', 'TC-005'}
{'TC-002', 'TC-003'}
{'TC-001', 'TC-004'}
{'TC-001', 'TC-004', 'TC-005'}
```

A great testing use: `planned - executed` gives the tests you **forgot to run**, and `executed - planned` gives tests that ran but weren't planned.

---

### 6. Converting Between Collections

| Conversion | Example | Result |
|---|---|---|
| List to set | `set([1, 2, 2, 3])` | `{1, 2, 3}` |
| Set to list | `list({1, 2, 3})` | `[1, 2, 3]` |
| List to tuple | `tuple([1, 2])` | `(1, 2)` |
| Tuple to list | `list((1, 2))` | `[1, 2]` |
| String to list of characters | `list("abc")` | `['a', 'b', 'c']` |
| Dictionary to list of keys | `list({"a": 1})` | `['a']` |

This is the same idea as casting from the type-conversion lesson: `list()`, `tuple()`, `set()` and `dict()` work like `int()` and `str()`.

---

### 7. Choosing the Right Collection

| You need... | Use |
|---|---|
| An ordered group you will add to or change | **List** |
| A fixed group that should not change, or a single record of mixed data | **Tuple** |
| To look things up by a name/label, or a record with named fields | **Dictionary** |
| Only unique items, fast "is it in there?" checks, or set maths | **Set** |

Examples from testing:

```python
test_queue = ["TC-003", "TC-001", "TC-002"]             # list: order matters, changes over time
viewport = (1366, 768)                                   # tuple: fixed pair
expected = {"status": 200, "content_type": "json"}       # dict: named expectations
seen_failures = {"TC-007", "TC-012"}                     # set: unique, quick membership checks
```

---

### 8. Common Mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Index out of range: `items[3]` on a 3-item list | `IndexError` | Valid indexes are `0` to `len - 1` |
| Missing key in a dictionary | `KeyError` | Use `.get()` or check with `in` |
| Trying to change a tuple | `TypeError` | Use a list if you need changes |
| `{}` for an empty set | Creates a dict | Use `set()` |
| Expecting order from a set | Order is not guaranteed | Use `sorted()` or use a list |
| `(5)` instead of `(5,)` | Not a tuple | Add the trailing comma |
| Using a list as a dictionary key | `TypeError: unhashable type` | Use a tuple or a string |
| Using `=` to "copy" a list | Both names refer to the same list | Covered in the methods lesson (copying) |
| Duplicate keys in a dict literal | The last one silently wins | Keep keys unique |

---

### 9. Practice Activities

1. **List basics.** Create a list of five test case IDs. Print its length, its first item, and whether `"TC-999"` is in it. Add one more ID and print the list.
2. **Loop.** Loop over your list and print `Running <id>` for each.
3. **Tuple.** Store a screen resolution as a tuple. Unpack it into `width` and `height` and print `1920x1080` using an f-string. Try to change an item and read the error message.
4. **Dictionary.** Create a dictionary for one test case with keys `id`, `title`, `priority` and `status`. Print each pair using `.items()`. Then add an `owner` key and change `status`.
5. **Safe lookup.** Use `.get()` to read a key that does not exist and provide a default message.
6. **List of dictionaries.** Create three test case dictionaries in a list. Loop over them and count how many have `status` equal to `"FAIL"`.
7. **Sets.** Given `["Chrome", "Edge", "Chrome", "Firefox", "Edge"]`, find the unique browsers and how many duplicates there were.
8. **Set maths.** Given `planned = {"TC-1", "TC-2", "TC-3"}` and `executed = {"TC-2", "TC-4"}`, print which planned tests were not executed, and which executed tests were not planned.
9. **Choose.** For each of these, say which collection fits and why: (a) the days of the week, (b) a user's profile (name, age, email), (c) all usernames seen so far with no repeats, (d) a queue of tests waiting to run.

---

## Summary

- A **collection** holds many values under one name, essential for handling test data.
- **List** `[ ]`: ordered, changeable, allows duplicates, accessed by index; loop with `for item in my_list`.
- **Tuple** `( )`: ordered, **immutable**; good for fixed values and single records; supports **unpacking**; a one-item tuple needs a trailing comma.
- **Dictionary** `{key: value}`: look up values by **key**; keys are unique and immutable; use `.get()` to avoid `KeyError`; loop with `.items()`; a **list of dictionaries** is the classic test-data table.
- **Set** `{ }`: unordered, **unique** items, no indexing; use `set()` for an empty set; great for de-duplication and set operations (`|`, `&`, `-`, `^`).
- **Mutable** types can change in place (list, dict, set); **immutable** ones cannot (string, tuple, numbers).
- Convert with `list()`, `tuple()`, `set()`; choose the collection that matches how you will use the data.
- Next: **indexing and slicing** in depth, then **collection methods**.

---

## Additional Resources

- Python Tutorial: Data Structures: https://docs.python.org/3/tutorial/datastructures.html
- Python documentation: Built-in types (sequence, set and mapping types): https://docs.python.org/3/library/stdtypes.html
- Real Python: Lists and Tuples in Python: https://realpython.com/python-lists-tuples/
