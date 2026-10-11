# Variables, Data Types and Operators

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a variable is and create variables using assignment.
- Follow Python's naming rules and naming conventions.
- Identify and use the core data types: `int`, `float`, `str`, `bool` and `None`.
- Use `type()` to inspect a value's type.
- Perform calculations with arithmetic operators and understand operator precedence.
- Compare values with comparison operators and combine conditions with logical operators.
- Use compound assignment operators such as `+=`.
- Apply these ideas to small test-automation scenarios.

---

## Why This Matters

Every program, from a ten-line script to a full test framework, works with **data**: a test case ID, an expected result, a response time, a pass or fail flag. To work with data you must be able to (1) *store* it, (2) know *what kind* of data it is, and (3) *calculate with or compare* it.

- **Variables** are how you store data.
- **Data types** describe what kind of data it is.
- **Operators** are how you calculate, compare and combine data.

In test automation you constantly do things like: store the expected page title, compare it to the actual title, calculate the percentage of tests that passed, or check that a response time is below a limit. All of those use exactly what you learn in this lesson.

---

## The Concept

### 1. What Is a Variable?

A **variable** is a *name that refers to a value stored in the computer's memory*.

**Analogy:** think of a labelled box. The label is the variable name, and the thing inside is the value. You can look inside the box by using its label, and you can replace what is inside.

```python
test_name = "Login with valid credentials"
```

Reading this line:

- `test_name` is the **variable name** (the label).
- `=` is the **assignment operator**. It does **not** mean "equals" as in maths. It means "store the value on the right into the name on the left".
- `"Login with valid credentials"` is the **value**.

Now you can use the name instead of repeating the value:

```python
test_name = "Login with valid credentials"
print(test_name)
```

Output:

```text
Login with valid credentials
```

Notice there are **no quotes** around `test_name` inside `print`. With quotes, Python prints the *text* "test_name"; without quotes, it prints the *value stored under that name*.

```python
print("test_name")   # prints: test_name
print(test_name)     # prints: Login with valid credentials
```

#### Variables can change (re-assignment)

They are called *variables* because the value can vary:

```python
attempts = 1
print(attempts)   # 1

attempts = 2
print(attempts)   # 2
```

Python always works on the **right side first**, then stores it. That is why this works:

```python
attempts = 1
attempts = attempts + 1   # right side: 1 + 1 = 2, then store 2 in attempts
print(attempts)           # 2
```

#### Multiple assignment

```python
passed = 8
failed = 2          # one per line (clearest)

x, y = 10, 20       # two variables in one line
a = b = 0           # both set to 0
```

Use these sparingly; one assignment per line is usually most readable.

---

### 2. Naming Variables

#### Rules (Python enforces these; breaking them causes an error)

1. Names may contain **letters, digits and underscores** only.
2. Names **cannot start with a digit**. `1st_test` is invalid, `test_1` is fine.
3. Names **cannot contain spaces or symbols** like `-`, `$`, `@`. Use `_` instead.
4. Names are **case-sensitive**: `Status`, `status` and `STATUS` are three different variables.
5. Names **cannot be Python keywords** such as `if`, `for`, `class`, `True`, `None`.

```python
test_id = 101        # valid
test_id_2 = 102      # valid
2nd_test = 5         # SyntaxError: starts with a digit
test-id = 3          # SyntaxError: hyphen is not allowed
```

#### Conventions (not enforced, but every Python developer follows them)

- Use **snake_case**: all lowercase, words separated by underscores: `expected_title`, `response_time_ms`.
- Choose **meaningful names**. Compare:

```python
x = 3000                 # What is x?
response_time_ms = 3000  # Clear immediately
```

- For values that should never change (constants), use **UPPER_CASE**: `MAX_RETRIES = 3`. Python will not stop you from changing it; the capital letters are a message to other developers: "do not modify this".

Good names make your test code self-documenting, which matters when a teammate has to read it six months from now.

---

### 3. Data Types

Every value in Python has a **type** that decides what you can do with it. You can ask Python for a value's type with the built-in `type()` function:

```python
print(type(42))
print(type("hello"))
```

```text
<class 'int'>
<class 'str'>
```

Python is **dynamically typed**: you do not declare a variable's type in advance. Python works it out from the value. The same name can later hold a different type (legal, but usually confusing, so avoid it).

The core types for today:

| Type | Name | What it stores | Example |
|---|---|---|---|
| `int` | integer | Whole numbers | `42`, `-7`, `0` |
| `float` | floating-point | Numbers with a decimal point | `3.14`, `-0.5`, `2.0` |
| `str` | string | Text | `"TC-001"`, `'Pass'` |
| `bool` | boolean | `True` or `False` | `True` |
| `NoneType` | None | "no value" | `None` |

(Python also has collections such as lists and dictionaries. Those are covered on Wednesday.)

#### 3.1 Integers (`int`)

Whole numbers, positive or negative, with no decimal point and no size limit that you'll practically meet.

```python
total_tests = 120
passed_tests = 114
temperature = -5
big_number = 1_000_000      # underscores can make big numbers readable
```

#### 3.2 Floats (`float`)

Numbers with a decimal part.

```python
pass_rate = 95.5
response_time_seconds = 0.75
price = 19.99
```

**Float precision warning.** Computers store decimals in binary, so some decimals can't be stored exactly:

```python
print(0.1 + 0.2)
```

```text
0.30000000000000004
```

This is not a Python bug; it happens in almost every language. It matters to testers: comparing two floats with exact equality can produce surprising failures. For now, remember that floats are *approximations* and you'll later use rounding or tolerance when comparing them.

#### 3.3 Strings (`str`)

A **string** is a sequence of characters (text) enclosed in quotes. You can use single `'...'` or double `"..."` quotes; they behave the same. Choose one style and be consistent.

```python
test_id = "TC-001"
status = 'PASS'
message = "It's working"      # double quotes let you include an apostrophe
quote = 'He said "go"'         # single quotes let you include double quotes
```

**Multi-line strings** use triple quotes:

```python
description = """This test checks that
a registered user can log in
with valid credentials."""
```

**Escape sequences** are special codes beginning with a backslash `\`:

| Code | Meaning |
|---|---|
| `\n` | New line |
| `\t` | Tab |
| `\\` | A literal backslash |
| `\"` | A literal double quote inside a double-quoted string |

```python
print("Step 1\nStep 2")
```

```text
Step 1
Step 2
```

**Combining strings:**

```python
prefix = "TC"
number = "001"
test_id = prefix + "-" + number      # concatenation (joining)
print(test_id)                       # TC-001

divider = "=" * 20                   # repetition
print(divider)                       # ====================
```

**Useful string tools** (called *methods*, written as `value.method()`; you will learn the full story of methods on Friday, for now just use them):

```python
name = "  login Test  "

print(len(name))        # 14   -> number of characters (including spaces)
print(name.strip())     # "login Test"   -> removes spaces at both ends
print(name.upper())     # "  LOGIN TEST  "
print(name.lower())     # "  login test  "
print(name.replace("login", "logout"))   # "  logout Test  "
```

An important property: **strings are immutable**, which means you cannot change them in place. Methods like `.upper()` give you a *new* string. If you want to keep it, store it:

```python
name = "login test"
name.upper()             # result thrown away! name is unchanged
name = name.upper()      # now name holds "LOGIN TEST"
```

You can also check whether text appears inside other text with `in`:

```python
print("TC" in "TC-001")      # True
print("API" in "TC-001")     # False
```

#### 3.4 Booleans (`bool`)

A boolean has exactly two possible values: `True` and `False` (capital first letter, no quotes).

```python
is_logged_in = True
has_errors = False
```

Booleans usually come from **comparisons** and are the foundation of decisions in code (decisions are covered tomorrow in conditional statements). In testing, the ultimate question of any test is a boolean: *did it pass (`True`) or not (`False`)?*

#### 3.5 None

`None` is a special value meaning "nothing here / not set yet". It is not zero, not an empty string and not `False`; it is the explicit absence of a value.

```python
actual_result = None      # test has not run yet
```

#### 3.6 Checking a type

```python
print(type(95.5))       # <class 'float'>
print(type(True))       # <class 'bool'>
print(type(None))       # <class 'NoneType'>
print(type("42"))       # <class 'str'>   <- a number in quotes is TEXT
```

That last line is a classic beginner trap: `42` and `"42"` look alike but are completely different types. The next lesson, **Type conversion and casting**, shows how to convert between them.

---

### 4. Operators

An **operator** is a symbol that performs an operation on values (called **operands**). In `5 + 3`, the `+` is the operator and `5` and `3` are the operands.

#### 4.1 Arithmetic operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `7 + 2` | `9` |
| `-` | Subtraction | `7 - 2` | `5` |
| `*` | Multiplication | `7 * 2` | `14` |
| `/` | Division (always gives a float) | `7 / 2` | `3.5` |
| `//` | Floor division (drops the decimal part) | `7 // 2` | `3` |
| `%` | Modulus (the remainder) | `7 % 2` | `1` |
| `**` | Exponent (power) | `7 ** 2` | `49` |

Things to notice:

- `/` **always returns a float**, even when the result is whole: `10 / 2` gives `5.0`.
- `//` is handy when you want a whole-number result. `7 // 2` is `3` because 2 fits into 7 three times.
- `%` gives what is left over: `7 % 2` is `1` because 7 = 2×3 + 1. A classic use: `number % 2` is `0` for even numbers.

A testing example, calculating the pass rate:

```python
total_tests = 40
passed_tests = 34

pass_rate = passed_tests / total_tests * 100
print(pass_rate)    # 85.0
```

#### 4.2 Operator precedence

When an expression has several operators, Python follows an order (like BODMAS/PEMDAS in maths):

1. Parentheses `( )`
2. Exponent `**`
3. Multiplication, division, floor division, modulus (`* / // %`), left to right
4. Addition and subtraction (`+ -`), left to right

```python
print(2 + 3 * 4)       # 14  (multiplication first)
print((2 + 3) * 4)     # 20  (parentheses first)
```

**Best practice:** when in doubt, add parentheses. They cost nothing and make your intent obvious.

#### 4.3 Assignment operators (shortcuts)

Updating a variable based on its own value is so common that Python gives shortcuts:

| Shortcut | Same as |
|---|---|
| `x += 5` | `x = x + 5` |
| `x -= 5` | `x = x - 5` |
| `x *= 5` | `x = x * 5` |
| `x /= 5` | `x = x / 5` |
| `x //= 5` | `x = x // 5` |
| `x %= 5` | `x = x % 5` |
| `x **= 5` | `x = x ** 5` |

```python
executed = 0
executed += 1        # 1
executed += 1        # 2
print(executed)      # 2
```

`+=` also works with strings: `log = "Start"` then `log += " > Login"` gives `"Start > Login"`.

#### 4.4 Comparison operators

Comparison operators compare two values and give back a **boolean**.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `4 <= 3` | `False` |

**The biggest beginner mistake:** `=` and `==` are different.

- `=` **assigns** a value: `status = "PASS"`
- `==` **compares** two values: `status == "PASS"` gives `True` or `False`

```python
expected_title = "Dashboard"
actual_title = "Dashboard"

print(expected_title == actual_title)     # True
print(expected_title != actual_title)     # False
```

This is the heart of a test: *compare expected to actual*. Note that string comparison is **case-sensitive**: `"Pass" == "PASS"` is `False`.

```python
response_time = 1.8
max_allowed = 2.0
print(response_time <= max_allowed)       # True  (within the limit)
```

#### 4.5 Logical operators

Logical operators combine boolean values.

| Operator | Meaning | Result is True when... |
|---|---|---|
| `and` | Both sides must be true | `True and True` |
| `or` | At least one side is true | `True or False` |
| `not` | Reverses the value | `not False` |

```python
status_ok = True
time_ok = False

print(status_ok and time_ok)    # False  (one side is False)
print(status_ok or time_ok)     # True   (at least one is True)
print(not status_ok)            # False
```

A realistic example. A test passes only if the status code is 200 **and** the response is fast enough:

```python
status_code = 200
response_time = 1.2

test_passed = status_code == 200 and response_time < 2.0
print(test_passed)     # True
```

Python evaluates the comparisons first (`status_code == 200` gives `True`, `response_time < 2.0` gives `True`) and then applies `and`.

**Truth table for `and` / `or`:**

| A | B | A and B | A or B |
|---|---|---|---|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

#### 4.6 A first look at membership

You already met `in`, which checks whether something is inside something else (so far, text inside text). It returns a boolean, and `not in` is its opposite:

```python
test_id = "TC-001"
print("TC" in test_id)         # True
print("BUG" not in test_id)    # True
```

---

### 5. Putting It Together: A Small Test Summary

```python
# Test run summary
suite_name = "Login Suite"
total_tests = 25
passed_tests = 22
failed_tests = total_tests - passed_tests
pass_rate = passed_tests / total_tests * 100
all_passed = failed_tests == 0
release_ready = pass_rate >= 90

print(suite_name)
print(total_tests)
print(failed_tests)
print(pass_rate)
print(all_passed)
print(release_ready)
```

Let's trace it step by step:

| Line | What happens | Value |
|---|---|---|
| `failed_tests = total_tests - passed_tests` | 25 - 22 | `3` |
| `pass_rate = passed_tests / total_tests * 100` | 22 / 25 = 0.88, then times 100 | `88.0` |
| `all_passed = failed_tests == 0` | Is 3 equal to 0? | `False` |
| `release_ready = pass_rate >= 90` | Is 88.0 at least 90? | `False` |

Output of the prints:

```text
Login Suite
25
3
88.0
False
False
```

> Tip: when a result surprises you, print each intermediate variable. That is the simplest and most effective debugging technique for a beginner.

---

### 6. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Using `=` instead of `==` in a comparison | `status = "PASS"` when you meant to compare | Use `==` to compare |
| Forgetting quotes around text | `name = Alice` (NameError) | `name = "Alice"` |
| Using a variable before assigning it | `print(score)` first | Assign before use |
| Treating `"5"` as a number | `"5" + 3` (TypeError) | Convert first (next lesson) |
| Wrong case in a name | `Total` vs `total` | Be consistent; use snake_case |
| Expecting `/` to give an int | `10 / 2` is `5.0` | Use `//` for whole-number division |

---

### 7. Practice Activities

1. **Variables.** Create variables for a test case: `test_id`, `title`, `priority` (a number), `is_automated` (boolean). Print each.
2. **Types.** Use `type()` on each of your variables and write down what you see. Then print `type("100")` and `type(100)` and explain the difference in your own words.
3. **Arithmetic.** A suite has 48 tests and 9 failed. Calculate passed tests, pass percentage and fail percentage.
4. **Remainder.** Print `17 % 5`, `17 // 5` and `17 / 5`. Explain each result.
5. **Strings.** Given `raw = "  tc-045  "`, produce `"TC-045"` using `.strip()` and `.upper()`. Print its length.
6. **Comparisons.** Given `expected = "Welcome"` and `actual = "welcome"`, print whether they are equal. Then make them equal using `.lower()` on both.
7. **Logic.** With `status_code = 404` and `response_time = 0.4`, write one expression that is `True` only when the status is 200 and the time is under 1 second. Predict the result before running.

---

## Summary

- A **variable** is a name referring to a value; create it with `=` (assignment). It can be reassigned.
- Follow naming rules (letters, digits, underscores; not starting with a digit; no keywords) and conventions (`snake_case`, meaningful names, `UPPER_CASE` for constants).
- Core data types: `int` (whole numbers), `float` (decimals), `str` (text), `bool` (`True`/`False`), `None` (no value). Use `type()` to inspect them.
- `42` and `"42"` are different types.
- Floats are approximate (`0.1 + 0.2` is not exactly `0.3`). Strings are immutable.
- Arithmetic operators: `+ - * / // % **`. Remember precedence; use parentheses for clarity.
- Compound assignment (`+=`, `-=`, ...) updates a variable using its own value.
- Comparison operators (`== != > < >= <=`) produce booleans. `=` assigns; `==` compares.
- Logical operators `and`, `or`, `not` combine booleans; `in` checks membership.

---

## Additional Resources

- Python Tutorial: An Informal Introduction to Python: https://docs.python.org/3/tutorial/introduction.html
- Python documentation: Built-in Types: https://docs.python.org/3/library/stdtypes.html
- Real Python: Variables in Python: https://realpython.com/python-variables/
