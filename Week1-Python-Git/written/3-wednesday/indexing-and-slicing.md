# Indexing and Slicing

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an index is and why Python counts from 0.
- Access single items in lists, tuples and strings using positive and negative indexes.
- Avoid and understand `IndexError`.
- Extract sub-parts of a sequence using slices: `[start:stop]`, `[start:stop:step]`.
- Use shortcuts such as `[:3]`, `[2:]`, `[-3:]` and `[::-1]`.
- Modify a list through indexing and slice assignment.
- Understand that slicing creates a new object and use it to copy a list.
- Apply indexing and slicing to realistic test-data tasks, such as parsing test IDs and picking out parts of a log line.

---

## Why This Matters

Last lesson you stored many values in collections. Now you need to **pick out exactly the piece you want**: the first test in a queue, the last character of an ID, the three most recent results, or the module name in the middle of `TC-LOGIN-007`.

Test data is full of structured text and ordered groups: IDs with prefixes, dates written as `2025-06-15`, log lines with a timestamp at the front, a list of results where only the last five matter. Indexing and slicing are the precise tools for extracting these parts. Without them you would resort to clumsy loops.

This builds on strings (Monday), loops (Tuesday) and the collections from the previous lesson. Strings, lists and tuples are all **sequences**, so everything in this lesson works identically on all three.

---

## The Concept

### 1. Sequences and Indexes

A **sequence** is an ordered collection where each item has a numbered position. Lists, tuples and strings are sequences. (Dictionaries are accessed by key, and sets have no order, so they don't support indexing.)

The position number is called the **index**. Python starts counting at **0**:

```
 value:   "T"  "C"  "-"  "0"  "4"  "2"
 index:    0    1    2    3    4    5
 negative: -6   -5   -4   -3   -2   -1
```

Why start at 0? It's a convention shared by most programming languages. A helpful way to think about it: the index is the **distance from the start**: the first item is 0 steps from the start.

---

### 2. Indexing: Getting One Item

Use square brackets after the sequence: `sequence[index]`.

```python
browsers = ["Chrome", "Firefox", "Edge", "Safari"]

print(browsers[0])     # Chrome   (first)
print(browsers[1])     # Firefox
print(browsers[3])     # Safari   (last)
```

Strings and tuples work the same way:

```python
test_id = "TC-042"
print(test_id[0])      # T
print(test_id[3])      # 0

size = (1920, 1080)
print(size[1])         # 1080
```

#### 2.1 Negative indexes: counting from the end

Negative numbers count backwards from the end: `-1` is the last item, `-2` the second last, and so on.

```python
browsers = ["Chrome", "Firefox", "Edge", "Safari"]

print(browsers[-1])    # Safari  (last)
print(browsers[-2])    # Edge
print(browsers[-4])    # Chrome  (same as index 0)
```

`[-1]` is the standard idiom for "the last item", and is much better than `[len(browsers) - 1]`.

#### 2.2 `IndexError`: going out of range

For a sequence with `n` items, valid indexes are `0` to `n - 1` (and `-1` to `-n`). Anything else raises an error:

```python
browsers = ["Chrome", "Firefox", "Edge"]
print(browsers[3])
```

```text
IndexError: list index out of range
```

A very common bug is the "off-by-one": thinking a 3-item list has an index 3. It doesn't: its indexes are 0, 1, 2.

Empty sequences have no valid index at all, so `[][0]` also fails. Guard with a check:

```python
results = []

if results:                       # an empty list is falsy
    print(results[0])
else:
    print("No results yet")
```

#### 2.3 Indexing nested structures

Chain the brackets, working from outside in:

```python
suite = [
    ["TC-001", "PASS"],
    ["TC-002", "FAIL"],
]

print(suite[1])         # ['TC-002', 'FAIL']
print(suite[1][0])      # TC-002
print(suite[-1][-1])    # FAIL
```

Dictionaries use the same brackets, but the thing inside is a **key**, not a position:

```python
cases = [
    {"id": "TC-001", "status": "PASS"},
    {"id": "TC-002", "status": "FAIL"},
]

print(cases[1]["status"])     # FAIL   (list index, then dictionary key)
```

---

### 3. Slicing: Getting a Range of Items

A **slice** extracts a *portion* of a sequence, producing a **new sequence of the same type**.

Syntax:

```python
sequence[start:stop]
```

- `start`: the index where the slice begins (**included**).
- `stop`: the index where the slice ends (**excluded**).

This is the same "stop is not included" rule as `range()` from Tuesday.

```python
numbers = [10, 20, 30, 40, 50, 60]
#  index:   0   1   2   3   4   5

print(numbers[1:4])    # [20, 30, 40]   -> indexes 1, 2, 3
print(numbers[0:2])    # [10, 20]
```

**A mental trick:** imagine the indexes pointing at the *gaps before* each item:

```
   | 10 | 20 | 30 | 40 | 50 | 60 |
   0    1    2    3    4    5    6
```

`[1:4]` takes everything between gap 1 and gap 4. The number of items returned is `stop - start` (4 - 1 = 3).

#### 3.1 Leaving out start or stop

| Slice | Meaning | `numbers = [10,20,30,40,50,60]` gives |
|---|---|---|
| `[:3]` | From the beginning up to index 3 | `[10, 20, 30]` |
| `[3:]` | From index 3 to the end | `[40, 50, 60]` |
| `[:]` | Everything (a copy) | `[10, 20, 30, 40, 50, 60]` |
| `[-2:]` | The last 2 items | `[50, 60]` |
| `[:-1]` | Everything except the last item | `[10, 20, 30, 40, 50]` |
| `[1:-1]` | Remove first and last | `[20, 30, 40, 50]` |

Useful pair: `s[:n]` is the **first n** items, `s[-n:]` is the **last n** items.

#### 3.2 Slices never raise `IndexError`

Unlike single-item indexing, slices quietly stop at the ends:

```python
numbers = [10, 20, 30]

print(numbers[1:100])    # [20, 30]
print(numbers[5:])       # []
```

That's convenient, but it can also hide mistakes, so check your results when you slice.

#### 3.3 The step: `[start:stop:step]`

A third number lets you skip items:

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[::2])      # [0, 2, 4, 6, 8]  -> every second item
print(numbers[1::2])     # [1, 3, 5, 7, 9]  -> every second item, starting at 1
print(numbers[2:8:3])    # [2, 5]
```

#### 3.4 Negative step: reversing

A negative step walks backwards. The classic way to reverse any sequence:

```python
print(numbers[::-1])           # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

word = "automation"
print(word[::-1])              # noitamotua
```

---

### 4. Slicing Strings

Slicing strings is perhaps the most practical application in test automation, because IDs, dates, filenames and log lines are all strings with a predictable layout.

```python
test_id = "TC-LOGIN-007"

print(test_id[:2])      # TC        -> the prefix
print(test_id[3:8])     # LOGIN     -> the module
print(test_id[-3:])     # 007       -> the number
```

Dates:

```python
date_text = "2025-06-15"

year = date_text[:4]       # "2025"
month = date_text[5:7]     # "06"
day = date_text[8:]        # "15"

print(f"{day}/{month}/{year}")        # 15/06/2025
```

Remember that slices of strings are strings; convert if you need numbers:

```python
year_number = int(date_text[:4])
print(year_number + 1)        # 2026
```

File names:

```python
filename = "login_report.html"

print(filename[-5:])           # .html
print(filename[:-5])           # login_report
print(filename[-5:] == ".html")    # True
```

(For files, there are dedicated methods such as `.endswith(".html")`, and you'll meet more string methods in the next lesson. Slicing is the general tool underneath.)

Log lines with fixed-width fields:

```python
log_line = "2025-06-15 10:42:07 ERROR Database timeout"

timestamp = log_line[:19]       # 2025-06-15 10:42:07
level = log_line[20:25]         # ERROR
message = log_line[26:]         # Database timeout

print(timestamp)
print(level)
print(message)
```

> **Strings are immutable:** you can read `text[0]`, but `text[0] = "X"` raises a `TypeError`. To "change" a string, build a new one: `new_text = "X" + text[1:]`.

---

### 5. Modifying Lists with Indexing and Slicing

Lists are mutable, so you can assign to an index or to a whole slice:

```python
results = ["PASS", "PASS", "FAIL", "PASS"]

results[2] = "RETEST"               # replace one item
print(results)                      # ['PASS', 'PASS', 'RETEST', 'PASS']

results[0:2] = ["SKIP", "SKIP"]     # replace a range
print(results)                      # ['SKIP', 'SKIP', 'RETEST', 'PASS']

results[1:3] = ["A", "B", "C"]      # slice and replacement can differ in length
print(results)                      # ['SKIP', 'A', 'B', 'C', 'PASS']
```

Deleting by index or slice:

```python
numbers = [10, 20, 30, 40, 50]

del numbers[0]           # remove first item
print(numbers)           # [20, 30, 40, 50]

del numbers[1:3]         # remove a slice
print(numbers)           # [20, 50]
```

Tuples and strings can't be changed this way, only read.

---

### 6. Slices Are New Objects: Copying a List

A slice produces a **new** list. This gives an easy way to copy:

```python
original = [1, 2, 3]
copy = original[:]

copy.append(4)

print(original)    # [1, 2, 3]       -> unchanged
print(copy)        # [1, 2, 3, 4]
```

Compare that with using `=`:

```python
original = [1, 2, 3]
alias = original          # NOT a copy: two names for the SAME list

alias.append(4)

print(original)    # [1, 2, 3, 4]   -> changed too!
print(alias)       # [1, 2, 3, 4]
```

`alias = original` doesn't copy anything; it just gives the same list a second name. This is a classic source of bugs. We'll explore copying properly in the collection methods lesson. For now: **use `[:]` (or `.copy()`) when you need an independent copy.**

One more subtlety: slicing makes a *shallow* copy. If the list contains other lists, those inner lists are still shared between the original and the copy. You don't need to worry about it yet, but remember it exists.

---

### 7. Handy Patterns

#### 7.1 First, last and middle

```python
items = ["a", "b", "c", "d", "e"]

first = items[0]
last = items[-1]
middle = items[len(items) // 2]       # 'c'
```

#### 7.2 The last N results

```python
results = ["P", "P", "F", "P", "F", "F", "P"]

recent = results[-3:]
print(recent)                         # ['F', 'F', 'P']
print(recent.count("F"))              # 2   (.count() is covered in the next lesson)
```

#### 7.3 Splitting into batches

```python
all_tests = ["T1", "T2", "T3", "T4", "T5", "T6"]

first_half = all_tests[:3]
second_half = all_tests[3:]
```

Using `len() // 2` as the cut point works for lists of any size:

```python
mid = len(all_tests) // 2
print(all_tests[:mid], all_tests[mid:])
```

#### 7.4 Skipping a header row

Imagine data copied from a spreadsheet where the first row is a header:

```python
rows = ["id,title", "TC-001,Login", "TC-002,Logout"]

for row in rows[1:]:           # skip the header
    print(row)
```

#### 7.5 Pairs and every-other-item

```python
data = ["TC-001", "PASS", "TC-002", "FAIL"]

ids = data[::2]         # ['TC-001', 'TC-002']
statuses = data[1::2]   # ['PASS', 'FAIL']
```

#### 7.6 Checking for a palindrome (a classic exercise)

```python
word = "level"
print(word == word[::-1])      # True
```

---

### 8. Indexing and Slicing Cheat Sheet

Given `s = "PYTHON"`:

| Expression | Result | Explanation |
|---|---|---|
| `s[0]` | `'P'` | First |
| `s[-1]` | `'N'` | Last |
| `s[2:4]` | `'TH'` | Indexes 2 and 3 |
| `s[:2]` | `'PY'` | First two |
| `s[-2:]` | `'ON'` | Last two |
| `s[::2]` | `'PTO'` | Every second character |
| `s[::-1]` | `'NOHTYP'` | Reversed |
| `s[10]` | `IndexError` | Out of range |
| `s[2:100]` | `'THON'` | Slices are forgiving |

---

### 9. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Thinking counting starts at 1 | `items[1]` to get the first item | The first item is `items[0]` |
| Off-by-one at the end | `items[len(items)]` | Use `items[-1]` or `items[len(items) - 1]` |
| Forgetting `stop` is excluded | `s[0:3]` has 3 items, not 4 | Remember: indexes 0, 1, 2 |
| Indexing an empty list | `[][0]` | Check with `if items:` first |
| Trying to index a set | `my_set[0]` → `TypeError` | Convert to a list or sort it first |
| Changing a string by index | `text[0] = "X"` | Build a new string |
| Thinking `b = a` copies | Both names change | Use `a[:]` or `a.copy()` |
| Mixing `:` and `,` | `items[1, 3]` | Slices use a colon: `items[1:3]` |
| Using a float index | `items[1.0]` | Indexes must be integers; use `//` or `int()` |

---

### 10. Practice Activities

Use `numbers = [5, 10, 15, 20, 25, 30, 35, 40]` for 1 to 6.

1. Print the first item, the last item and the item at index 3.
2. Print the first three items and the last three items.
3. Print every second item, then every second item starting at index 1.
4. Print the list reversed without modifying the original.
5. Print the list without its first and last items.
6. Replace the slice `numbers[2:4]` with `[0, 0, 0]` and print the result.
7. **IDs.** For `test_id = "TC-PAYMENT-0125"`, extract the prefix, the module name and the number. Convert the number to an `int` and add 1.
8. **Dates.** From `"2025-12-31"`, print `31.12.2025`.
9. **Log line.** From `"10:42:07 WARNING Slow response"`, extract the time, the level and the message with slicing.
10. **File name.** Given `"screenshot_login.png"`, get the extension and the name without the extension.
11. **Copy test.** Create a list, copy it with `[:]`, change the copy and show that the original is unchanged. Repeat with `copy = original` and describe the difference.
12. **Spot the bug.** Why does `results[len(results)]` fail? Fix it two different ways.
13. **Parity.** Given `["TC-1", "PASS", "TC-2", "FAIL", "TC-3", "PASS"]`, use extended slices to create one list of IDs and one list of statuses.

---

## Summary

- **Indexes** number the items of a sequence (list, tuple, string), starting at **0**; **negative indexes** count from the end (`-1` is last).
- `sequence[i]` returns one item; an index outside the valid range raises **`IndexError`**.
- **Slicing** `sequence[start:stop:step]` returns a **new** sequence; `start` is included, `stop` is **excluded**; any part can be omitted.
- Handy forms: `[:n]` first n, `[-n:]` last n, `[1:-1]` without first and last, `[::2]` every second, `[::-1]` reversed, `[:]` a copy.
- Slices are forgiving; single indexes are not.
- Lists can be modified by index and by slice assignment; strings and tuples are read-only.
- `b = a` makes two names for one list; `a[:]` creates an independent (shallow) copy.
- Slicing is ideal for parsing IDs, dates, file names and fixed-format log lines.
- Next: **collection operations and methods** such as `append`, `sort`, `get` and `update`.

---

## Additional Resources

- Python Tutorial: Lists (indexing and slicing) and strings: https://docs.python.org/3/tutorial/introduction.html#lists
- Python documentation: Common sequence operations: https://docs.python.org/3/library/stdtypes.html#common-sequence-operations
- Real Python: Indexing and Slicing in Python: https://realpython.com/lessons/indexing-and-slicing/
