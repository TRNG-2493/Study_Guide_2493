# Type Conversion and Casting

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why Python needs type conversion and what happens when types are mixed.
- Distinguish between **implicit** conversion (done automatically by Python) and **explicit** conversion/casting (done by you).
- Use `int()`, `float()`, `str()` and `bool()` correctly.
- Predict which conversions succeed, which lose information and which raise a `ValueError`.
- Understand the truthiness rules used by `bool()`.
- Use `round()` and understand the difference between truncating and rounding.
- Recognize and fix `TypeError` caused by mixing text and numbers.

---

## Why This Matters

Data rarely arrives in the type you need. In test automation:

- A value typed by a user (or read from a file, a web page or an API response) is almost always **text**, even if it looks like a number. The text `"200"` is not the number `200`.
- A test report needs to *combine* numbers and text into messages like `"Passed 22 of 25 tests"`.
- A comparison such as "is the response time under 2 seconds?" only works if both sides are numbers.

If you don't convert correctly, your tests either crash with an error or, worse, quietly give wrong answers. Tomorrow's lesson on input and output depends directly on this one, because everything a user types in is text.

This also supports the week's goal of writing small, reliable programs: knowing how to move safely between types is a core skill of every programmer.

---

## The Concept

### 1. A Reminder: Types Are Different Things

From the previous lesson, `42` (an `int`) and `"42"` (a `str`) are different. Python treats them differently:

```python
print(42 + 8)         # 50     -> numbers add together
print("42" + "8")     # 428    -> text is joined together
```

And mixing the two is an error:

```python
print("42" + 8)
```

```text
TypeError: can only concatenate str (not "int") to str
```

Python is telling you: "I'm not going to guess whether you wanted `50` or `"428"`. Convert one side so we are talking about the same type." That is what type conversion is for.

---

### 2. Two Kinds of Conversion

| Kind | Who does it | Also called |
|---|---|---|
| **Implicit conversion** | Python, automatically, when it is safe | Type coercion |
| **Explicit conversion** | You, using a function such as `int()` | Type casting |

#### 2.1 Implicit conversion

Python automatically converts when no information would be lost. The most common case is mixing `int` and `float`; the `int` is promoted to a `float`:

```python
whole = 5          # int
decimal = 2.5      # float

result = whole + decimal
print(result)          # 7.5
print(type(result))    # <class 'float'>
```

Python converted `5` to `5.0` behind the scenes, so the sum is a `float`. Booleans also behave as numbers in arithmetic (`True` acts as `1`, `False` as `0`), though you should rarely rely on this:

```python
print(True + True)   # 2
```

Implicit conversion does **not** apply between text and numbers, as seen in the `TypeError` above.

#### 2.2 Explicit conversion (casting)

When you deliberately convert a value to another type, it is called **casting**. You do it by calling the type's name like a function: `int(...)`, `float(...)`, `str(...)`, `bool(...)`. Each one takes a value and gives you back a *new value* of that type. The original is unchanged.

```python
text_number = "42"
real_number = int(text_number)

print(text_number, type(text_number))   # 42 <class 'str'>
print(real_number, type(real_number))   # 42 <class 'int'>
```

---

### 3. Converting to Integer: `int()`

`int()` produces a whole number.

**From a string containing a whole number:**

```python
print(int("100"))        # 100
print(int("  7  "))      # 7     (surrounding spaces are allowed)
print(int("-15"))        # -15
```

**From a float, which truncates (cuts off) the decimal part. It does NOT round:**

```python
print(int(9.99))     # 9
print(int(9.01))     # 9
print(int(-3.7))     # -3   (towards zero, not down to -4)
```

**From a boolean:**

```python
print(int(True))     # 1
print(int(False))    # 0
```

**What fails: text that is not a plain whole number:**

```python
int("abc")        # ValueError: invalid literal for int() with base 10: 'abc'
int("3.5")        # ValueError  (a decimal string cannot be directly converted)
int("")           # ValueError
```

Notice `int("3.5")` fails. To handle that, go through `float` first:

```python
print(int(float("3.5")))     # 3
```

Read this from the inside out: `float("3.5")` gives `3.5`, then `int(3.5)` gives `3`.

> **What is a `ValueError`?** It means "you gave me the right *type* of thing (text), but its *content* can't be converted". In a later lesson you'll learn how to catch errors like this and handle them gracefully. For now, understand why they happen and avoid them by checking your data.

---

### 4. Converting to Float: `float()`

`float()` produces a number with a decimal point.

```python
print(float("3.14"))     # 3.14
print(float("10"))       # 10.0
print(float(7))          # 7.0
print(float("-0.5"))     # -0.5
print(float(True))       # 1.0
```

It fails for non-numeric text:

```python
float("fast")     # ValueError: could not convert string to float: 'fast'
```

Real-world use: converting a response time read as text:

```python
response_time_text = "1.85"
response_time = float(response_time_text)

print(response_time < 2.0)     # True
```

Without `float()`, comparing `"1.85" < 2.0` would raise a `TypeError`, because text and numbers can't be compared with `<`.

---

### 5. Converting to String: `str()`

`str()` converts almost anything into text. It **never fails** for the basic types, because every value has a text form.

```python
print(str(42))        # "42"
print(str(3.14))      # "3.14"
print(str(True))      # "True"
print(str(None))      # "None"
```

This is the fix for the `TypeError` we saw in section 1 when you want *joining*:

```python
passed = 22
message = "Tests passed: " + str(passed)
print(message)        # Tests passed: 22
```

Without `str(passed)`, Python would raise `TypeError: can only concatenate str (not "int") to str`.

> **Better alternative coming up:** in the next lesson on input and output you will learn **f-strings**, which format numbers inside text without you having to call `str()` manually, for example `f"Tests passed: {passed}"`. Knowing why `str()` is needed helps you appreciate why f-strings are so convenient.

---

### 6. Converting to Boolean: `bool()` and Truthiness

`bool()` answers: "Does this value count as true or false?" Python has a simple rule set. A value is **falsy** (converts to `False`) when it is "empty" or "zero". Almost everything else is **truthy** (converts to `True`).

| Value | `bool(value)` | Why |
|---|---|---|
| `0` | `False` | Zero |
| `0.0` | `False` | Zero |
| `""` (empty string) | `False` | Empty |
| `None` | `False` | No value |
| `False` | `False` | Already false |
| `42`, `-1`, `0.1` | `True` | Non-zero |
| `"hello"` | `True` | Non-empty |
| `" "` (one space) | `True` | Not empty; it has a character |
| `"False"` | `True` | A non-empty string, regardless of its meaning! |
| `"0"` | `True` | Non-empty string |

```python
print(bool(0))          # False
print(bool(25))         # True
print(bool(""))         # False
print(bool("Pass"))     # True
print(bool("False"))    # True   <-- surprising!
```

The last line is a very common trap: `bool("False")` is `True`, because Python only checks whether the string is empty, not what it says. When converting text such as `"yes"`/`"no"` or `"true"`/`"false"` to a boolean, you need to *compare* the text instead:

```python
text = "true"
is_enabled = text.lower() == "true"
print(is_enabled)        # True
```

Here `.lower()` makes the check case-insensitive and `==` gives a real boolean.

---

### 7. Rounding vs Truncating

You saw that `int(9.99)` gives `9`, which truncates. If you want the nearest whole number, use `round()`:

```python
print(round(9.99))      # 10
print(round(9.4))       # 9
print(round(3.14159, 2))   # 3.14   (second argument = decimal places)
print(round(88.456, 1))    # 88.5
```

| Goal | Tool | `9.99` becomes |
|---|---|---|
| Cut off the decimals | `int(9.99)` | `9` |
| Nearest whole number | `round(9.99)` | `10` |
| Two decimal places | `round(9.99, 2)` | `9.99` |

A small surprise: Python's `round()` uses "banker's rounding" for exact halves (it rounds to the nearest even number), so `round(2.5)` is `2` and `round(3.5)` is `4`. It rarely matters for beginners, but if you see it, you now know it is intentional.

For testers, rounding is useful when you want a tidy percentage in a report:

```python
passed = 22
total = 25
pass_rate = round(passed / total * 100, 1)
print(pass_rate)       # 88.0
```

---

### 8. Conversion Summary Table

| From → To | `int()` | `float()` | `str()` | `bool()` |
|---|---|---|---|---|
| `"25"` | `25` | `25.0` | `"25"` | `True` |
| `"2.5"` | **ValueError** | `2.5` | `"2.5"` | `True` |
| `"abc"` | **ValueError** | **ValueError** | `"abc"` | `True` |
| `""` | **ValueError** | **ValueError** | `""` | `False` |
| `7` | `7` | `7.0` | `"7"` | `True` |
| `0` | `0` | `0.0` | `"0"` | `False` |
| `7.9` | `7` (truncated) | `7.9` | `"7.9"` | `True` |
| `True` | `1` | `1.0` | `"True"` | `True` |
| `None` | **TypeError** | **TypeError** | `"None"` | `False` |

---

### 9. Putting It Together: Realistic Examples

#### Example A: Cleaning data that arrives as text

Imagine a test report where all values are text (this is exactly what you'd get when reading from a file or user input):

```python
total_text = "40"
passed_text = "34"

total = int(total_text)
passed = int(passed_text)
failed = total - passed
pass_rate = round(passed / total * 100, 1)

print("Failed tests: " + str(failed))
print("Pass rate: " + str(pass_rate) + "%")
```

Output:

```text
Failed tests: 6
Pass rate: 85.0%
```

Step-by-step:

1. `int("40")` gives `40`; `int("34")` gives `34`.
2. `failed = 40 - 34` gives `6`.
3. `34 / 40 * 100` gives `85.0`; `round(85.0, 1)` is `85.0`.
4. `str(failed)` and `str(pass_rate)` make the numbers joinable with text.

#### Example B: Building a test ID

```python
prefix = "TC"
number = 7

test_id = prefix + "-" + str(number).zfill(3)
print(test_id)       # TC-007
```

`str(number)` gives `"7"`, and the string method `.zfill(3)` pads it with leading zeros to a width of 3. Combining conversion with string methods is exactly what you'll need for tomorrow's practical exercise.

#### Example C: Same-looking values, different results

```python
a = "10"
b = "9"
print(a > b)               # False   (text comparison: "1" comes before "9")
print(int(a) > int(b))     # True    (number comparison: 10 > 9)
```

Text is compared character by character, so `"10"` is "smaller" than `"9"`. This is a classic cause of wrong test results. Convert first, then compare.

---

### 10. Common Mistakes and How to Avoid Them

| Mistake | What happens | Fix |
|---|---|---|
| Adding text and a number | `TypeError` | Convert with `str()` or `int()`/`float()` |
| `int("3.7")` | `ValueError` | `int(float("3.7"))` |
| Expecting `int(9.9)` to round | You get `9` | Use `round(9.9)` |
| Assuming `bool("False")` is `False` | It is `True` | Compare the text: `text == "False"` |
| Comparing numbers stored as text | Wrong ordering | Convert both to numbers first |
| Forgetting to store the result | Original unchanged | `value = int(value)` |

**Remember:** casting does not change the original variable. It gives you a new value, so store it:

```python
age = "30"
int(age)            # result is thrown away
print(type(age))    # <class 'str'>   still text!

age = int(age)      # stored
print(type(age))    # <class 'int'>
```

---

### 11. Practice Activities

1. **Predict, then check.** Predict the result of each, then run it:
   `int("12")`, `int(12.9)`, `float("5")`, `str(5) + "5"`, `int("5") + 5`, `bool("")`, `bool("0")`.
2. **Fix the error.** This code crashes. Fix it so it prints `Total: 15`:
   ```python
   a = "10"
   b = 5
   print("Total: " + a + b)
   ```
3. **Percentages.** Given `passed = "18"` and `total = "24"` as text, calculate the pass rate rounded to 1 decimal place and print it as `Pass rate: 75.0%`.
4. **Truncate vs round.** For `7.5` and `7.49`, print both `int()` and `round()` results and explain the differences.
5. **Safe boolean.** Given `flag = "TRUE"`, write one line that produces a real boolean `True` from it regardless of upper/lower case.
6. **Error spotting.** Run `int("seven")` and `int("3.5")`, read each error message and describe in one sentence what went wrong.
7. **ID builder.** Given `suite = "login"` and `number = 12`, produce `LOGIN-012`.

---

## Summary

- Python won't silently mix text and numbers; you must convert. The result is a **new value**, so store it.
- **Implicit conversion** happens automatically and safely (for example `int` + `float` gives a `float`).
- **Explicit conversion (casting)** uses `int()`, `float()`, `str()` and `bool()`.
- `int()` **truncates** decimals; `round()` rounds. `int("3.5")` fails; use `int(float("3.5"))`.
- Text that isn't a valid number raises a `ValueError`.
- `str()` works on nearly anything and is how you join numbers into text (f-strings, next lesson, make this easier).
- `bool()` follows truthiness: zero, empty text and `None` are `False`, nearly everything else is `True`. Note `bool("False")` is `True`.
- Compare numbers as numbers, not as text.

---

## Additional Resources

- Python documentation: Built-in functions (`int`, `float`, `str`, `bool`, `round`): https://docs.python.org/3/library/functions.html
- Python documentation: Numeric types: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
- Real Python: Basic Data Types in Python: https://realpython.com/python-data-types/
