# Input and Output Operations

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what input and output mean in a program.
- Display information with `print()`, including multiple values and the `sep` and `end` options.
- Use escape characters to control line breaks and tabs.
- Format output cleanly with **f-strings**, including number formatting, padding and alignment.
- Read user input with `input()` and understand that it always returns text.
- Combine `input()` with type conversion to build interactive console programs.
- Build a simple interactive program that asks questions and shows a formatted result.

---

## Why This Matters

A program is only useful if it can **receive** information and **show** results. This is called **I/O (Input/Output)**.

- **Output** is anything the program shows or produces: text on a screen, a message, a report line.
- **Input** is anything the program receives: what a user types, data from a file, values from another system.

In test automation, output is how a test tells you what happened (`PASS`, `FAIL`, an error message, a summary table). Clear, well-formatted output is the difference between a failure you can fix in two minutes and one that wastes an afternoon. Input is how you make a script flexible: instead of hard-coding every value, you can ask for it.

Today's exercise, a console *test-case ID formatter*, uses exactly the skills in this lesson plus the last two: variables, operators and type conversion.

---

## The Concept

### 1. Output with `print()`

`print()` is a **built-in function** that displays values on the screen (in the terminal). We have used it already; now let's learn it properly.

#### 1.1 Basic use

```python
print("Starting test run")
print(42)
print(3.14)
print(True)
```

```text
Starting test run
42
3.14
True
```

`print()` can display any type. Each call to `print()` normally ends by moving to a **new line**.

#### 1.2 Printing variables

```python
suite = "Smoke Tests"
count = 12

print(suite)
print(count)
```

#### 1.3 Printing several values at once

Separate values with commas. `print()` automatically puts a **space** between them and converts each value to text for you, so no `str()` is needed:

```python
suite = "Smoke Tests"
count = 12
print("Suite:", suite, "| Tests:", count)
```

```text
Suite: Smoke Tests | Tests: 12
```

Compare with using `+`, where you must convert manually:

```python
print("Tests: " + str(count))     # works, but needs str()
print("Tests:", count)            # simpler: commas handle conversion
```

#### 1.4 The `sep` option: choose the separator

By default the separator is a single space. Change it with `sep`:

```python
print("2025", "06", "15", sep="-")
print("TC", "001", sep="-")
print("a", "b", "c", sep="")
```

```text
2025-06-15
TC-001
abc
```

`sep="..."` is called a **keyword argument**: you name the option and give it a value. (Functions and their arguments are covered in depth on Thursday; for now just copy the pattern.)

#### 1.5 The `end` option: choose what comes at the end

By default, `print()` ends with a newline (`"\n"`). Change it with `end`:

```python
print("Loading", end="...")
print("done")
```

```text
Loading...done
```

Both `print` calls appear on the same line because the first one didn't end with a newline.

#### 1.6 Blank lines

```python
print("Section 1")
print()
print("Section 2")
```

```text
Section 1

Section 2
```

An empty `print()` outputs a blank line. Handy for readability.

---

### 2. Escape Characters Revisited

Inside strings, a backslash `\` introduces a special character:

| Code | Result |
|---|---|
| `\n` | New line |
| `\t` | Tab (a wide gap, useful for simple columns) |
| `\\` | A single backslash |
| `\'` / `\"` | A quote character |

```python
print("Name\tStatus")
print("Login\tPASS")
print("Search\tFAIL")
```

```text
Name    Status
Login   PASS
Search  FAIL
```

```python
print("Line 1\nLine 2\nLine 3")
print("Path: C:\\tests\\reports")
```

```text
Line 1
Line 2
Line 3
Path: C:\tests\reports
```

Notice that Windows file paths contain backslashes, which is why you must double them (`\\`) in normal strings; otherwise `\t` inside `C:\tests` would be read as a tab!

A **raw string** (prefix `r`) tells Python to treat backslashes literally: `print(r"C:\tests\reports")` prints the same path without doubling.

---

### 3. Formatted Output with f-strings

Joining text and numbers using `+` and `str()` becomes messy fast. Python has a much nicer way: **f-strings** (formatted string literals). You put the letter `f` before the opening quote and place variables or expressions inside **curly braces `{ }`**.

```python
name = "Login Test"
duration = 2.5

print(f"Test '{name}' finished in {duration} seconds")
```

```text
Test 'Login Test' finished in 2.5 seconds
```

Python replaces each `{...}` with the value of what's inside. No `str()` needed.

**Compare the old way:**

```python
print("Test '" + name + "' finished in " + str(duration) + " seconds")   # hard to read
print(f"Test '{name}' finished in {duration} seconds")                    # much clearer
```

#### 3.1 Expressions inside braces

You can put calculations (any expression) inside the braces:

```python
passed = 22
total = 25

print(f"{passed} of {total} tests passed")
print(f"Failed: {total - passed}")
print(f"Pass rate: {passed / total * 100}%")
```

```text
22 of 25 tests passed
Failed: 3
Pass rate: 88.0%
```

You can also call string methods inside the braces: `f"{name.upper()}"`.

#### 3.2 Format specifiers: control how a value looks

After the value, add a colon `:` and a **format specifier**.

**Decimal places:** `:.2f` means "float with 2 digits after the decimal point".

```python
rate = 87.456789
print(f"Rate: {rate:.2f}")      # Rate: 87.46
print(f"Rate: {rate:.0f}")      # Rate: 87
print(f"Rate: {rate:.1f}%")     # Rate: 87.5%
```

**Leading zeros:** `:03d` means "integer, at least 3 characters wide, padded with zeros".

```python
number = 7
print(f"TC-{number:03d}")       # TC-007
print(f"TC-{number:05d}")       # TC-00007
```

This is perfect for test-case IDs.

**Thousands separator:** `:,`

```python
print(f"{1250000:,}")           # 1,250,000
```

**Percentage:** `:.1%` multiplies by 100 and adds a `%`:

```python
print(f"{0.8768:.1%}")          # 87.7%
```

**Width and alignment:** `:<10` left-aligns in 10 characters, `:>10` right-aligns, `:^10` centres.

```python
print(f"{'Name':<12}{'Status':>8}")
print(f"{'Login':<12}{'PASS':>8}")
print(f"{'Search':<12}{'FAIL':>8}")
```

```text
Name          Status
Login           PASS
Search          FAIL
```

(When you use quotes inside an f-string, use the *other* kind of quote than the one wrapping the f-string: here `'Name'` inside `f"..."`.)

**Quick reference:**

| Specifier | Meaning | Example (value → output) |
|---|---|---|
| `:.2f` | 2 decimal places | `3.14159` → `3.14` |
| `:03d` | zero-padded to width 3 | `7` → `007` |
| `:,` | thousands separator | `1500` → `1,500` |
| `:.1%` | percentage, 1 decimal | `0.256` → `25.6%` |
| `:<10` | left-align, width 10 | `'ab'` → `ab        ` |
| `:>10` | right-align, width 10 | `'ab'` → `        ab` |
| `:^10` | centre, width 10 | `'ab'` → `    ab    ` |

#### 3.3 Debugging shortcut: `=`

Adding `=` after a variable inside braces prints both the name and the value, great for quick debugging:

```python
attempts = 3
print(f"{attempts=}")     # attempts=3
```

#### 3.4 Printing braces literally

Double them: `print(f"{{not a variable}}")` prints `{not a variable}`.

#### 3.5 Other formatting styles you may see

Older code may use `.format()` (`"Hello {}".format(name)`) or `%` formatting (`"Hello %s" % name`). They still work, but **f-strings are the modern standard**, and we will use them.

---

### 4. Input with `input()`

`input()` is a built-in function that **pauses the program, waits for the user to type something and press Enter**, and then **returns what they typed**.

```python
name = input("Enter your name: ")
print(f"Hello, {name}!")
```

Running it:

```text
Enter your name: Priya
Hello, Priya!
```

How it works:

1. `input("Enter your name: ")` displays the **prompt** text (the message in quotes) and waits.
2. The user types `Priya` and presses Enter.
3. The function returns the text `"Priya"`, which is stored in `name`.

Always make your prompt clear, with a space or colon at the end so the user's typing doesn't touch the message.

#### 4.1 The most important rule: `input()` ALWAYS returns a string

Even if the user types a number, you get **text**:

```python
age = input("Enter your age: ")
print(type(age))
```

```text
Enter your age: 30
<class 'str'>
```

So this goes wrong:

```python
age = input("Enter your age: ")
print(age + 1)       # TypeError: can only concatenate str (not "int") to str
```

This is where the previous lesson pays off. Convert it:

```python
age = int(input("Enter your age: "))
print(age + 1)       # 31
```

Read `int(input(...))` from the inside out: `input(...)` collects text, then `int(...)` converts it to a whole number. Use `float(input(...))` for decimals.

If the user types something that cannot be converted (like `abc` for an `int`), Python raises a `ValueError` and the program stops. We will learn how to handle bad input gracefully later in the program; for now, when you test your own programs, type valid values.

#### 4.2 Cleaning input

Users add stray spaces and unpredictable capitalization. Clean text input immediately:

```python
suite = input("Suite name: ").strip().upper()
print(suite)
```

If the user types `  smoke  `, the result is `SMOKE`. This is called **chaining** methods: `.strip()` runs first, then `.upper()` on its result.

---

### 5. Putting It Together

#### Example 1: Simple test summary calculator

```python
suite_name = input("Suite name: ").strip()
total = int(input("Total tests: "))
passed = int(input("Passed tests: "))

failed = total - passed
pass_rate = passed / total

print()
print(f"=== {suite_name} Summary ===")
print(f"Total   : {total}")
print(f"Passed  : {passed}")
print(f"Failed  : {failed}")
print(f"Pass %  : {pass_rate:.1%}")
```

Sample run:

```text
Suite name: Login Suite
Total tests: 25
Passed tests: 22

=== Login Suite Summary ===
Total   : 25
Passed  : 22
Failed  : 3
Pass %  : 88.0%
```

Walkthrough:

1. Three `input()` calls collect text. The two numbers are converted with `int()`.
2. Arithmetic computes `failed` and `pass_rate` (a decimal such as `0.88`).
3. `print()` with no arguments adds a blank line.
4. f-strings format everything; `:.1%` converts `0.88` into `88.0%`.

#### Example 2: A mini test-case ID builder (a preview of today's exercise)

```python
prefix = input("Module prefix (e.g. login): ").strip().upper()
number = int(input("Test number: "))
test_id = f"{prefix}-{number:04d}"

print(f"Generated ID: {test_id}")
```

```text
Module prefix (e.g. login): login
Test number: 42
Generated ID: LOGIN-0042
```

#### Example 3: Pretty table

```python
print(f"{'ID':<10}{'Title':<25}{'Result':>8}")
print("-" * 43)
print(f"{'TC-001':<10}{'Valid login':<25}{'PASS':>8}")
print(f"{'TC-002':<10}{'Invalid password':<25}{'FAIL':>8}")
```

```text
ID        Title                      Result
-------------------------------------------
TC-001    Valid login                  PASS
TC-002    Invalid password             FAIL
```

---

### 6. A Note on Other Kinds of Input and Output

Today we use the **console** (keyboard in, screen out), the simplest form of I/O. Programs can also read from and write to **files**, receive data from the **network** and so on. Reading and writing files is a larger topic that we will cover later in the program. Everything you learned here about text formatting will still apply.

---

### 7. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Forgetting `int()` on numeric input | `age + 1` where `age = input()` | `age = int(input(...))` |
| Forgetting the `f` before the string | `print("Hello {name}")` prints `{name}` literally | `print(f"Hello {name}")` |
| Reusing the same quote inside an f-string (Python 3.11 and earlier) | `f"{'a'}"` is fine, `f"{"a"}"` is not | Use a different quote type inside the braces |
| Missing closing parenthesis | `print("Hi"` | Check bracket pairs |
| Using `+` with numbers and text | `"Total: " + 5` | Use commas or an f-string |
| Not stripping input | `"  yes"` is not `"yes"` | `.strip()` the input |

---

### 8. Practice Activities

1. **Output basics.** Print your name, role and one goal on three lines, using `\n` in a single `print()` call.
2. **sep and end.** Print `2025`, `10`, `07` as `2025/10/07` using `sep`. Then print `Loading` and `done` on one line using `end`.
3. **f-strings.** Given `name = "Search Test"`, `duration = 1.23456`, print `Search Test took 1.23 seconds`.
4. **Zero padding.** Given `n = 5`, print `TC-0005`.
5. **Greeting.** Ask for the user's name and favourite programming topic, then print a greeting using both.
6. **Calculator.** Ask for two numbers (as `float`), then print their sum, difference, product and quotient, each rounded to 2 decimals with f-strings.
7. **Report card.** Ask for suite name, total and passed tests; print a summary similar to Example 1, plus a line showing whether the pass rate is at least 90% (a `True`/`False` value).
8. **Table.** Print a 3-row aligned table of test IDs, titles and statuses of your own design.

---

## Summary

- **Output** shows information; **input** receives it. In testing, clear output tells you what happened.
- `print()` can show several values separated by commas; `sep` changes the separator and `end` changes what ends the line.
- Escape characters: `\n` (new line), `\t` (tab), `\\` (backslash).
- **f-strings** (`f"... {value} ..."`) are the modern way to build text; they accept expressions and format specifiers like `:.2f`, `:03d`, `:,`, `:.1%` and alignment `:<10`, `:>10`, `:^10`.
- `input("prompt")` waits for the user and **always returns a string**. Convert with `int()` or `float()` when you need numbers.
- Clean text input with `.strip()`, `.lower()` or `.upper()`.
- Combining input, conversion, arithmetic and f-strings lets you build interactive console programs, and that is exactly what today's exercise requires.

---

## Additional Resources

- Python Tutorial: Input and Output (formatted string literals): https://docs.python.org/3/tutorial/inputoutput.html
- Python documentation: Format Specification Mini-Language: https://docs.python.org/3/library/string.html#format-specification-mini-language
- Real Python: Python Input and Output: https://realpython.com/python-input-output/
