# Built-in Python Functions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **built-in function** is, where it comes from (the built-in scope from the previous lesson), and how to discover and read documentation for one (`help()`, `dir()`, the official docs).
- Use the most important built-ins confidently, grouped by purpose:
  - **Type conversion and inspection:** `int`, `float`, `str`, `bool`, `list`, `tuple`, `set`, `dict`, `type`, `isinstance`, `repr`, `id`, `callable`.
  - **Numbers:** `abs`, `round`, `divmod`, `pow`, `sum`, `min`, `max`.
  - **Sequences and iteration:** `len`, `range`, `enumerate`, `zip`, `sorted`, `reversed`, `map`, `filter`, `any`, `all`, `iter`, `next`.
  - **Objects and attributes:** `hasattr`, `getattr`, `setattr`, `vars`, `dir`.
  - **Input / output and text:** `print`, `input`, `format`, `chr`, `ord`.
- Choose between a built-in and a hand-written loop, and explain why the built-in is usually clearer and faster.
- Predict the results (and the errors) that built-ins produce for edge cases such as empty lists or bad input.
- Apply built-ins to real QA tasks: validating test data, comparing expected and actual results, building lookup tables, and writing readable assertions.

---

## Why This Matters

Python ships with a toolbox of around 70 functions that are available in **every** program without a single `import`. They are written in optimised C, thoroughly tested, and they express common ideas ("how many items?", "is any value negative?", "pair these two lists") in one readable line.

The weekly epic is about hardening your Python so that test code is robust and maintainable. Built-in functions help in three concrete ways:

1. **Less code, fewer bugs.** `all(row["status"] == "ok" for row in rows)` replaces a five-line loop with a flag variable. Every line of test code you do not write is a line that cannot be wrong.
2. **Better validation.** `isinstance`, `int()` with `try/except`, `len`, `min`/`max`, `sorted` and `zip` are the daily tools for checking that data coming from a file (Tuesday) or from an API has the right type, size, range and order.
3. **Better debugging.** In the next two lessons you will debug and log. `repr()`, `type()`, `id()`, `dir()`, `vars()` and `help()` are the first things you reach for when you ask "what *is* this object?".

In the previous two lessons you saw that built-in names live in the **built-in scope** (the "B" in LEGB) and that it is a mistake to shadow them by naming a variable `list` or `max`. Here you will learn what is actually *in* that scope and how to use it well.

---

## The Concept

### 1. What is a built-in function?

A **function** is a named, reusable block of code that you *call* with arguments, e.g. `len("hello")`. A **built-in function** is one that Python provides automatically, so there is nothing to import. The complete official list is at the link in *Additional Resources*; you will learn the most important ones here.

```python
print(len("hello"))   # 5
```

- `len` is the function name.
- `"hello"` is the **argument**, the input value.
- The result (`5`) is the **return value**, which `print` then displays.

Some built-ins are actually **classes** that you call to create objects (`int`, `str`, `list`, `dict`, `set`, `range`, `enumerate`, `zip`...). In daily use they look and feel like functions, so we will treat them together.

### 2. How to discover and learn built-ins yourself

You do not need to memorise everything. Python can document itself:

```python
help(len)              # prints documentation for len
print(len.__doc__)     # the same docstring, as a string
print(dir(str)[:5])    # first few attribute names of the str type
```

Inside an interactive session (`python` with no arguments) or a debugger, `help(sorted)` is often faster than a web search. The `dir(obj)` function lists the attributes and methods of an object, which is the quickest way to answer "what can I do with this?".

### 3. Printing and input: `print`, `input`, `format`

#### `print(*objects, sep=" ", end="\n")`

Displays values on screen. It accepts any number of arguments, converts each one with `str()`, and puts `sep` between them and `end` after the last.

```python
print("a", "b", "c")                 # a b c
print("a", "b", "c", sep="-")        # a-b-c
print("Loading", end="...")          # no newline after
print("done")                        # Loading...done
```

`print` *returns* `None`; its job is the side effect of showing output. A very common beginner mistake is `result = print(x)`.

`print` is fine for quick checks, but in real test projects you will replace it with **logging** (the lesson after *Debugging techniques*) because logs have levels, timestamps and destinations.

#### `input(prompt)`

Pauses and reads one line typed by the user, **always returning a string**.

```python
age_text = input("Enter your age: ")   # user types 30 -> '30' (a string!)
age = int(age_text)                     # convert before doing arithmetic
```

Automated tests normally cannot wait for a human, so you will rarely call `input` in test code, but you should know it returns text.

#### `format(value, spec)` and f-strings

`format` applies a *format specification*. It is the engine behind f-strings (`f"..."`) and `str.format`.

```python
print(format(3.14159, ".2f"))      # 3.14   (2 decimal places)
print(f"{1234567:,}")              # 1,234,567 (thousands separator)
print(f"{'id':<6}|{'status':>8}")  # id    |  status  (left/right alignment)
```

### 4. Type conversion functions

Data from files and APIs usually arrives as text. These functions convert one type into another.

| Function | Purpose | Examples |
|---|---|---|
| `int(x)` | To integer (truncates floats toward zero) | `int("42")` -> `42`, `int(3.9)` -> `3`, `int(-3.9)` -> `-3`, `int("ff", 16)` -> `255` |
| `float(x)` | To floating point | `float("3.5")` -> `3.5` |
| `str(x)` | To text | `str(10)` -> `'10'` |
| `bool(x)` | To `True`/`False` | `bool("")` -> `False`, `bool([0])` -> `True` |
| `list(x)` | To a list | `list("abc")` -> `['a', 'b', 'c']` |
| `tuple(x)` | To a tuple | `tuple([1, 2])` -> `(1, 2)` |
| `set(x)` | To a set (removes duplicates) | `set([1, 1, 2])` -> `{1, 2}` |
| `dict(x)` | To a dict | `dict([("a", 1)])` -> `{'a': 1}` |

#### Conversions can fail

```python
int("abc")    # ValueError: invalid literal for int() with base 10: 'abc'
int("3.7")    # ValueError: invalid literal for int() with base 10: '3.7'
int(None)     # TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

Notice that `int("3.7")` fails even though `int(3.7)` works; a *string* must look exactly like an integer. Use `int(float("3.7"))` if that is what you mean. These failures are exactly what you learned to catch on Tuesday:

```python
def to_int(text, default=None):
    """Convert text to int; return default if impossible."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(to_int("42"))       # 42
print(to_int("4x2"))      # None
print(to_int(None, 0))    # 0
```

#### Truthiness: how `bool()` decides

Python treats these as **falsy**: `False`, `None`, `0`, `0.0`, `""` (empty string), `[]`, `()`, `{}`, `set()`, `range(0)`. Almost everything else is **truthy**, including the *string* `"0"` and the *list* `[0]`. This is why `if items:` is a Pythonic "is the list non-empty?" test, and also why `bool("False")` is `True` (a non-empty string)! When reading booleans from a CSV or JSON file, compare against explicit text (`value.lower() == "true"`).

### 5. Inspecting objects: `type`, `isinstance`, `repr`, `id`, `callable`

#### `type(obj)` and `isinstance(obj, classinfo)`

```python
print(type(1))                      # <class 'int'>
print(isinstance(1, int))           # True
print(isinstance(1, (int, float)))  # True  (a tuple of types means "any of these")
print(isinstance(True, int))        # True  (bool is a subclass of int!)
print(type(True) == int)            # False
```

Prefer `isinstance` for checks: it respects inheritance, and it accepts a tuple of types. Note the quirk: `True` is an `int`, so `isinstance(True, int)` is `True`. If you must reject booleans when validating a count, check `isinstance(x, int) and not isinstance(x, bool)`.

#### `repr(obj)` versus `str(obj)`

- `str(obj)` is for **humans**: readable output.
- `repr(obj)` is for **developers**: an unambiguous representation, ideally one you could paste back into code. Strings in `repr` have quotes and escape characters, so hidden whitespace becomes visible.

```python
text = "a\n"
print(str(text))     # prints 'a' followed by a real line break
print(repr(text))    # 'a\n'   <-- the \n is visible
print(repr(1.0))     # 1.0
```

In debugging and logging, `repr` is your friend: `"Expected 'ok' but got 'ok '"` is invisible with `str` but obvious with `repr` (`'ok '` has a trailing space). In f-strings use the `!r` flag: `f"value={value!r}"`.

#### `id(obj)`, `callable(obj)`

`id` returns an object's identity (see *Mutability and memory*). `callable(obj)` answers "can I call this with `()`?":

```python
print(callable(len))     # True
print(callable("abc"))   # False
```

### 6. Number functions

```python
print(abs(-3), abs(-2.5))          # 3 2.5
print(divmod(17, 5))               # (3, 2)   -> quotient and remainder together
print(pow(2, 10), 2 ** 10)         # 1024 1024
print(pow(2, 10, 1000))            # 24       -> (2**10) % 1000, efficient modular power
print(round(3.14159, 2))           # 3.14
print(round(1234, -2))             # 1200     -> negative digits round to hundreds
```

#### `round()` uses "banker's rounding"

```python
print(round(0.5), round(1.5), round(2.5), round(-2.5))   # 0 2 2 -2
```

Python rounds exact halves to the **nearest even** number. In addition, many decimals cannot be stored exactly in binary floating point:

```python
print(round(2.675, 2))        # 2.67  (not 2.68, because 2.675 is stored as 2.67499999...)
print(0.1 + 0.2)              # 0.30000000000000004
print(0.1 + 0.2 == 0.3)       # False
```

**QA implication:** never compare floats with `==` in assertions about calculated values. Use `math.isclose(a, b)` (from the standard library's `math` module) or compare rounded values:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))   # True
```

(For exact money calculations, the `decimal` module exists; you will see it when needed.)

#### `sum`, `min`, `max`

```python
scores = [72, 88, 95, 60]
print(sum(scores))            # 315
print(min(scores), max(scores))   # 60 95
print(sum(scores) / len(scores))  # 78.75   (average)
```

Useful options:

```python
print(max(["bb", "a", "ccc"], key=len))        # ccc   (largest by length)
print(max([], default=None))                   # None  (avoid an error for empty input)
print(sum([[1], [2]], []))                     # [1, 2] (second arg is the start value)
```

Edge cases to know:

```python
max([])            # ValueError: max() iterable argument is empty
sum(["a", "b"])    # TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

`sum` is for numbers; to join strings use `"".join(list_of_strings)`.

### 7. Sequence and iteration functions

#### `len(x)`: how many items?

```python
print(len("abc"), len([1, 2, 3]), len({"a": 1}))   # 3 3 1
len(5)    # TypeError: object of type 'int' has no len()
```

#### `range(stop)`, `range(start, stop)`, `range(start, stop, step)`

Produces a lazy sequence of integers; the `stop` value is **excluded**.

```python
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(2, 10, 3)))   # [2, 5, 8]
print(list(range(5, 0, -2)))   # [5, 3, 1]
```

`range` does not build the whole list in memory; it generates numbers as needed, so `range(10_000_000)` is cheap.

#### `enumerate(iterable, start=0)`: index plus item

Instead of managing a counter yourself:

```python
for number, name in enumerate(["login", "search"], start=1):
    print(number, name)
# 1 login
# 2 search
```

Test scenario: report "row 7 is invalid" while looping over a data file, using `enumerate(rows, start=2)` if row 1 of the file is a header.

#### `zip(*iterables)`: walk several sequences in step

```python
names = ["a", "b", "c"]
scores = [1, 2, 3]
print(list(zip(names, scores)))        # [('a', 1), ('b', 2), ('c', 3)]
print(dict(zip(names, scores)))        # {'a': 1, 'b': 2, 'c': 3}
```

`zip` stops at the **shortest** input silently, which can hide missing data. Since Python 3.10 you can add `strict=True` to raise an error on mismatched lengths:

```python
list(zip([1, 2, 3], "ab", strict=True))
# ValueError: zip() argument 2 is shorter than argument 1
```

Perfect for comparing an *expected* list with an *actual* list in a test:

```python
expected = [200, 201, 404]
actual = [200, 201, 500]
for exp, act in zip(expected, actual, strict=True):
    if exp != act:
        print(f"Mismatch: expected {exp}, got {act}")
# Mismatch: expected 404, got 500
```

`itertools.zip_longest` (standard library) pads the shorter input instead if that is what you want.

#### `sorted(iterable, key=None, reverse=False)` and `reversed(seq)`

`sorted` returns a **new list**; the original is unchanged (unlike `list.sort()`).

```python
print(sorted([3, 1, 2], reverse=True))             # [3, 2, 1]
print(sorted(["b", "A", "c"]))                     # ['A', 'b', 'c']   (uppercase sorts first)
print(sorted(["b", "A", "c"], key=str.lower))      # ['A', 'b', 'c']  -> case-insensitive via key
print(list(reversed([1, 2, 3])))                   # [3, 2, 1]
```

The `key` argument is a function applied to each item to decide its sort position, e.g. `sorted(users, key=lambda u: u["age"])`. Sorting mixed types fails: `sorted([3, "a"])` raises `TypeError: '<' not supported between instances of 'str' and 'int'`.

#### `map` and `filter`

```python
print(list(map(str, [1, 2])))              # ['1', '2']
print(list(filter(None, [0, 1, "", 2])))   # [1, 2]  (None means: keep truthy values)
```

Most Python programmers prefer list comprehensions for the same job (`[str(n) for n in nums]`, `[n for n in nums if n]`); you will see both styles in real code. Both `map` and `filter` return **lazy iterators**, which can be consumed only once:

```python
m = map(str, [1, 2])
print(list(m))     # ['1', '2']
print(list(m))     # []   <-- already used up
```

#### `any` and `all`

- `any(iterable)`: `True` if **at least one** item is truthy.
- `all(iterable)`: `True` if **every** item is truthy.

```python
print(any([0, 0, 1]))        # True
print(all([1, 2]))           # True
print(all([]), any([]))      # True False   <-- empty input: all is True, any is False
```

Combined with a generator expression these make superb validation one-liners:

```python
rows = [{"id": 1, "status": "ok"}, {"id": 2, "status": "ok"}]
print(all(row["status"] == "ok" for row in rows))     # True
print(any(row["id"] < 0 for row in rows))             # False
```

Watch out: `all([])` being `True` means "no counter-examples were found". A test that "verifies all results are valid" will pass on an empty result set! Pair it with `assert len(rows) > 0` or `assert rows` when emptiness would be a defect.

#### `iter` and `next`

These expose the machinery behind `for` loops:

```python
it = iter([10, 20])
print(next(it))              # 10
print(next(it))              # 20
print(next(it, "no more"))   # no more   (default value instead of StopIteration)
```

`next(iterator, default)` is a handy way to get "the first match or a default": `first_admin = next((u for u in users if u["role"] == "admin"), None)`.

### 8. Attribute and object introspection: `hasattr`, `getattr`, `setattr`, `vars`, `dir`

```python
class Config:
    pass

cfg = Config()
setattr(cfg, "timeout", 30)                 # same as cfg.timeout = 30
print(getattr(cfg, "timeout"))              # 30
print(getattr(cfg, "retries", 3))           # 3  (default when missing)
print(hasattr(cfg, "timeout"))              # True
print(vars(cfg))                            # {'timeout': 30}
```

They let you work with attribute **names stored in strings**, which is common when data-driven tests describe checks by name. `dir(obj)` lists available attributes, while `vars(obj)` gives the object's own attribute dictionary.

### 9. Character and number representations

```python
print(ord("A"), chr(65))             # 65 A
print(hex(255), bin(5), oct(8))      # 0xff 0b101 0o10
```

`ord` and `chr` convert between a character and its Unicode code point; `hex`, `bin`, `oct` give text representations of an integer. Handy for decoding status bytes or checking character handling in input-validation tests.

### 10. Other built-ins worth recognising

| Function | What it does |
|---|---|
| `open(path, mode)` | Opens a file (you used it on Tuesday, ideally with `with`) |
| `isinstance`, `issubclass` | Type relationship checks |
| `slice(start, stop, step)` | Object form of `a[start:stop:step]` |
| `bytes`, `bytearray`, `frozenset` | Immutable/mutable binary data and immutable set |
| `eval`, `exec` | Run text as code; **dangerous with untrusted input; avoid** |
| `help`, `dir` | Built-in documentation and introspection |
| `breakpoint()` | Drops into the debugger (covered in *Debugging techniques*) |

---

## Code Examples

### Example A: A reusable data-validation helper using built-ins

```python
def validate_scores(raw_scores):
    """Validate a list of text scores; return (clean_numbers, error_messages)."""
    clean = []
    errors = []
    for line_no, text in enumerate(raw_scores, start=1):
        try:
            value = float(text)
        except (ValueError, TypeError):
            errors.append(f"line {line_no}: {text!r} is not a number")
            continue
        if not 0 <= value <= 100:
            errors.append(f"line {line_no}: {value} out of range 0-100")
            continue
        clean.append(value)
    return clean, errors

good, bad = validate_scores(["88", "x7", "101", "75.5", None])
print(good)    # [88.0, 75.5]
for message in bad:
    print(message)
```

Output:

```
[88.0, 75.5]
line 2: 'x7' is not a number
line 3: 101.0 out of range 0-100
line 5: None is not a number
```

How it works:

- `enumerate(raw_scores, start=1)` supplies human-friendly line numbers.
- `float(text)` converts; `ValueError` covers bad text and `TypeError` covers `None`.
- `!r` in the f-string applies `repr`, so `'x7'` is printed with quotes and `None` is printed as `None` (not the word "none" in disguise).
- `0 <= value <= 100` is a *chained comparison*, a compact range check.
- The function returns both values and problems so a caller (or a test) can assert on them separately.

### Example B: Summarising results with `sum`, `min`, `max`, `sorted`, `zip`

```python
tests = ["login", "search", "checkout", "logout"]
durations = [1.2, 0.8, 3.4, 0.5]          # seconds

print("Total  :", round(sum(durations), 2))                 # 5.9
print("Average:", round(sum(durations) / len(durations), 2)) # 1.48
print("Fastest:", min(zip(durations, tests)))               # (0.5, 'logout')
print("Slowest:", max(zip(durations, tests)))               # (3.4, 'checkout')

for duration, name in sorted(zip(durations, tests), reverse=True):
    print(f"{name:<10}{duration:>5.1f}s")
```

Output:

```
Total  : 5.9
Average: 1.48
Fastest: (0.5, 'logout')
Slowest: (3.4, 'checkout')
checkout    3.4s
login       1.2s
search      0.8s
logout      0.5s
```

Explanation: `zip(durations, tests)` pairs each time with its test name. Tuples compare element by element, so `min`/`max` of those tuples pick by duration first. `{name:<10}` left-aligns in a width of 10 and `{duration:>5.1f}` right-aligns a float with 1 decimal in width 5.

### Example C: Expected versus actual, with `zip(strict=True)`, `all` and `any`

```python
expected = {"id": 7, "name": "Widget", "price": 9.99}
actual   = {"id": 7, "name": "Widget", "price": 9.99, "extra": True}

missing = [key for key in expected if key not in actual]
mismatched = [key for key in expected if key in actual and expected[key] != actual[key]]
unexpected = [key for key in actual if key not in expected]

print("missing   :", missing)       # []
print("mismatched:", mismatched)    # []
print("unexpected:", unexpected)    # ['extra']
print("core fields match:", all(actual.get(k) == v for k, v in expected.items()))   # True
```

This pattern, building small lists of *what is wrong*, produces much more helpful failure messages than a single `False`.

### Example D: Looking up the first match safely

```python
users = [
    {"name": "ann", "role": "viewer"},
    {"name": "bob", "role": "admin"},
]
first_admin = next((u for u in users if u["role"] == "admin"), None)
print(first_admin)    # {'name': 'bob', 'role': 'admin'}

none_found = next((u for u in users if u["role"] == "owner"), None)
print(none_found)     # None
```

`(u for u in users if ...)` is a generator expression: it checks users one by one and `next` stops at the first match instead of scanning everything and building a list.

### Example E: Exploring an unknown object

```python
obj = "QA"
print(type(obj), repr(obj))
print([name for name in dir(obj) if not name.startswith("_")][:5])
print(hasattr(obj, "upper"), callable(obj.upper))
```

Output:

```
<class 'str'> 'QA'
['capitalize', 'casefold', 'center', 'count', 'encode']
True True
```

When debugging an object you did not create, this three-line routine tells you what it is, what it can do, and whether a method exists.

---

## Summary / Key Takeaways

- Built-in functions are always available (built-in scope) and are fast, tested and readable. Do not shadow their names.
- Use `help()`, `dir()` and the official docs to learn more; you do not need to memorise every one.
- Conversion functions (`int`, `float`, `str`, `bool`, `list`...) can raise `ValueError`/`TypeError`: wrap external data in `try/except`. `int("3.7")` fails; `int(3.7)` truncates.
- Truthiness: empty containers, `0`, `None`, `""` are falsy; the string `"False"` is truthy.
- `round` uses banker's rounding and floats are imprecise: compare floats with `math.isclose`, not `==`.
- `sum`, `min`, `max` have `key=`/`default=`/start-value options; `max([])` raises `ValueError` unless you give `default`.
- `enumerate` for index+item, `zip` for parallel iteration (use `strict=True` to catch length mismatches), `sorted` returns a new list, `reversed`/`map`/`filter`/`zip` return one-shot iterators.
- `any` / `all` plus generator expressions give compact validation. `all([])` is `True`; guard against empty data.
- `repr` (and `!r`) exposes hidden whitespace and quotes: ideal in debugging and failure messages. `isinstance` is preferred over `type ==`.
- `getattr`/`setattr`/`hasattr`/`vars`/`dir` allow attribute work by name and quick exploration of unknown objects.

---

## Practice Questions and Mini-Exercises

**Q1.** What does each line print?

```python
print(int(7.9), int(-7.9), round(7.5), round(8.5))
print(bool("False"), bool(0), bool([]), bool([0]))
```

**Q2.** Why does `int("12.5")` fail? Write one expression that converts the text `"12.5"` to the integer `12`.

**Q3.** What is the value of `result`?

```python
result = [3, 1, 2].sort()
```

**Q4.** Given `names = ["a", "b", "c"]` and `ages = [30, 25]`, what does `list(zip(names, ages))` return? How would you make Python raise an error instead of silently dropping `"c"`?

**Q5.** Predict the output:

```python
print(all([]), any([]), all([1, 0]), any([0, 2]))
```

**Q6.** Why is `assert all(r["ok"] for r in results)` a risky test on its own? How do you make it safer?

**Q7 (mini-exercise).** Given `words = ["pear", "Apple", "fig", "banana"]`, produce (a) a list sorted case-insensitively and (b) the longest word, using only built-ins.

**Q8 (mini-exercise).** Write `safe_average(values)` that returns the average of a list of numbers or `None` if the list is empty. Use `sum` and `len`.

**Q9 (mini-exercise).** Given the headers `["id", "name", "age"]` and a row `["7", "Sam", "31"]`, build the dictionary `{"id": 7, "name": "Sam", "age": 31}` using `zip` and `dict`, converting `id` and `age` to integers.

**Q10.** What is the difference between `repr("ok ")` and `str("ok ")` when printed, and why does it matter in a failing test's message?

**Q11.** Explain why `0.1 + 0.2 == 0.3` is `False` and write an assertion-friendly comparison.

### Answers

**A1.**

```
7 -7 8 8
True False False True
```

`int` truncates toward zero. `round(7.5)` is `8` and `round(8.5)` is `8`, because exact halves go to the nearest even number. `bool("False")` is `True` (non-empty string); `bool([0])` is `True` (non-empty list).

**A2.** `int()` on a string requires an integer literal; `"12.5"` has a decimal point. Convert via float: `int(float("12.5"))` gives `12`.

**A3.** `None`. `list.sort()` sorts in place and returns `None`. Use `sorted([3, 1, 2])` if you need the sorted list returned.

**A4.** `[('a', 30), ('b', 25)]`; `"c"` is dropped silently. Use `zip(names, ages, strict=True)` (Python 3.10+), which raises `ValueError: zip() argument 2 is shorter than argument 1`.

**A5.** `True False False True`.

**A6.** If `results` is empty, `all(...)` is `True`, so the test passes even though nothing was verified. Add `assert results` (or `assert len(results) > 0`) before it.

**A7.**

```python
words = ["pear", "Apple", "fig", "banana"]
print(sorted(words, key=str.lower))   # ['Apple', 'banana', 'fig', 'pear']
print(max(words, key=len))            # banana
```

**A8.**

```python
def safe_average(values):
    if not values:
        return None
    return sum(values) / len(values)

print(safe_average([2, 4, 9]))   # 5.0
print(safe_average([]))          # None
```

**A9.**

```python
headers = ["id", "name", "age"]
row = ["7", "Sam", "31"]
record = dict(zip(headers, row))
record["id"] = int(record["id"])
record["age"] = int(record["age"])
print(record)    # {'id': 7, 'name': 'Sam', 'age': 31}
```

**A10.** `print(str("ok "))` shows `ok ` with an invisible trailing space; `print(repr("ok "))` shows `'ok '`, making the space visible. In failure messages, `repr` (or `!r`) makes whitespace, quotes and escape characters obvious so that "expected 'ok' got 'ok '" can be diagnosed instantly.

**A11.** Floats are stored in binary, and `0.1` and `0.2` cannot be represented exactly, so their sum is `0.30000000000000004`. Use `math.isclose(0.1 + 0.2, 0.3)` (after `import math`) or `abs(a - b) < 1e-9`.

---

## Additional Resources

- Python Standard Library, "Built-in Functions" (full official list with signatures): https://docs.python.org/3/library/functions.html
- Python Tutorial, "Floating-Point Arithmetic: Issues and Limitations": https://docs.python.org/3/tutorial/floatingpoint.html
- Python Standard Library, "Built-in Types" (truth value testing, sequence and dict operations): https://docs.python.org/3/library/stdtypes.html
