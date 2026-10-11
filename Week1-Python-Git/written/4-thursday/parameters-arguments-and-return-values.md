# Parameters, Arguments and Return Values

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between a **parameter** and an **argument**.
- Write functions that accept one or several inputs.
- Call functions with **positional** and **keyword** arguments.
- Use `return` to send a result back to the caller and store it in a variable.
- Explain the difference between `return` and `print`, and why returning is usually better.
- Return multiple values and unpack them.
- Use early returns to simplify logic.
- Explain what a function returns when there is no `return` statement (`None`).
- Understand how mutable arguments (such as lists) behave when a function changes them.
- Document parameters and return values with docstrings and optional type hints.

---

## Why This Matters

In the previous lesson, your functions were rigid: `print_banner()` always printed the same text, and `check_status()` always checked the same status code. Useful functions are like machines with an input slot and an output chute:

```
   inputs (parameters) ──▶ [ function ] ──▶ output (return value)
```

Think of the built-in functions you already know: `len("hello")` takes a value and gives back `5`. `int("42")` takes text and gives back a number. You don't care how they work inside; you give an input and get a result.

For test automation, this is the core skill:

- `is_valid_test_id("TC-007")` takes an ID and **returns** `True` or `False`.
- `calculate_pass_rate(passed, total)` takes two numbers and **returns** a percentage.
- `format_duration(125)` takes seconds and returns `"2m 5s"`.

Today's pair-programming exercise has you build a test-utility library full of exactly these. This lesson is what turns your functions from fixed scripts into reusable building blocks.

---

## The Concept

### 1. Parameters and Arguments

A **parameter** is a variable *name* listed in the function's definition: a placeholder for an input. An **argument** is the actual *value* you pass in when you call the function.

```python
def greet(name):              # 'name' is a PARAMETER
    print(f"Hello, {name}!")

greet("Priya")                # "Priya" is an ARGUMENT
greet("Marco")
```

```text
Hello, Priya!
Hello, Marco!
```

**Analogy:** a parameter is like the blank on a form ("Name: ______"). The argument is what a particular person writes in it.

What happens during the call `greet("Priya")`:

1. Python jumps into `greet`.
2. It creates a local variable `name` and sets it to `"Priya"`.
3. The body runs using that value.
4. When the function ends, `name` disappears.

People often use "parameter" and "argument" interchangeably in casual conversation, and you will be understood either way. But it helps to know the difference when reading documentation and error messages.

#### Multiple parameters

Separate them with commas:

```python
def print_test_result(test_id, status, duration):
    print(f"{test_id}: {status} ({duration:.1f}s)")

print_test_result("TC-001", "PASS", 1.234)
print_test_result("TC-002", "FAIL", 3.5)
```

```text
TC-001: PASS (1.2s)
TC-002: FAIL (3.5s)
```

#### Arguments can be anything

Literals, variables, expressions, results of other functions, even collections:

```python
name = "Dana"
greet(name)                    # a variable
greet("Mr. " + name)           # an expression
greet(input("Your name: "))    # a function call's result
```

---

### 2. Passing Arguments: Positional and Keyword

#### 2.1 Positional arguments

Arguments are matched to parameters **by position**: first argument to first parameter, and so on.

```python
def print_test_result(test_id, status, duration):
    print(f"{test_id}: {status} ({duration:.1f}s)")

print_test_result("TC-001", "PASS", 1.2)       # correct
print_test_result("PASS", "TC-001", 1.2)       # runs, but the meaning is swapped!
```

Python can't know the second call is wrong; the order is your responsibility.

#### 2.2 Keyword arguments

You can name the parameters in the call, in which case the order no longer matters:

```python
print_test_result(status="PASS", duration=1.2, test_id="TC-001")
```

Keyword arguments make calls **self-documenting**, which is especially valuable when a function has several parameters. Compare `create_user("admin", True, 30)` with `create_user(role="admin", active=True, timeout=30)`.

You can mix them, but **positional arguments must come first**:

```python
print_test_result("TC-001", status="PASS", duration=1.2)    # fine
print_test_result(test_id="TC-001", "PASS", 1.2)            # SyntaxError
```

#### 2.3 Wrong number of arguments

```python
print_test_result("TC-001", "PASS")
```

```text
TypeError: print_test_result() missing 1 required positional argument: 'duration'
```

```python
print_test_result("TC-001", "PASS", 1.2, "extra")
```

```text
TypeError: print_test_result() takes 3 positional arguments but 4 were given
```

These messages are helpful: they tell you exactly which function and which parameter. (Optional parameters with default values come in the next lesson.)

---

### 3. Return Values

So far, our functions *displayed* something. Often you want a function to **compute a result and hand it back** so the caller can use it. That's what **`return`** does.

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)               # 7
print(add(10, 5) * 2)       # 30
```

How it works:

1. `add(3, 4)` runs the function with `a = 3`, `b = 4`.
2. `return a + b` **ends the function immediately** and sends `7` back.
3. The call `add(3, 4)` is **replaced by the value** `7`, as if you had written `7` there. So `result = add(3, 4)` becomes `result = 7`.

**Examples of useful return values in testing:**

```python
def calculate_pass_rate(passed, total):
    return passed / total * 100

rate = calculate_pass_rate(22, 25)
print(f"Pass rate: {rate:.1f}%")      # Pass rate: 88.0%
```

```python
def make_test_id(prefix, number):
    return f"{prefix.upper()}-{number:03d}"

print(make_test_id("login", 7))       # LOGIN-007
```

```python
def is_success(status_code):
    return 200 <= status_code < 300

print(is_success(204))   # True
print(is_success(404))   # False
```

The last one returns a **boolean** directly: no need for `if ...: return True else: return False`. Functions that answer yes/no questions are often named with `is_`, `has_` or `can_` prefixes.

#### `return` ends the function

Any code after `return` in the same path is never run:

```python
def example():
    return "done"
    print("This never runs")
```

---

### 4. `return` vs `print`: A Critical Difference

Beginners often confuse these two, because in the REPL both seem to "show" a result.

| | `print(x)` | `return x` |
|---|---|---|
| Purpose | **Display** something to a human | **Send a value back** to the calling code |
| Can the result be reused? | No; the text is just on screen | Yes: store it, calculate with it, test it |
| Ends the function? | No | Yes |

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)       # prints 5
y = add_return(2, 3)      # prints nothing

print(x)       # None   -> add_print gave nothing back!
print(y)       # 5
print(add_return(2, 3) * 10)     # 50
# print(add_print(2, 3) * 10)    # would crash: None * 10
```

**Rule of thumb:** *functions that calculate or decide should return; the code that calls them decides whether to print.* This makes functions reusable (the same `calculate_pass_rate` can feed a console report, a file, or an assertion) and testable (a test can compare the returned value with the expected one). Functions whose *whole job* is to display output, such as `print_report`, may of course print.

---

### 5. Functions Without a `return`: `None`

If a function finishes without hitting a `return`, Python quietly returns **`None`**. You met `None` on Monday; here is where it comes from most often.

```python
def log_message(message):
    print(f"[LOG] {message}")

result = log_message("Starting")
print(result)       # None
```

A classic bug: forgetting the `return` and then wondering why you got `None`:

```python
def square(n):
    n * n               # calculated, then thrown away!

print(square(4))        # None
```

Fix: `return n * n`.

---

### 6. Returning Multiple Values

A function can return several values separated by commas. Python packs them into a **tuple** (yesterday's lesson), and you can **unpack** them into separate variables.

```python
def summarise(results):
    passed = 0
    failed = 0
    for status in results:
        if status == "PASS":
            passed += 1
        else:
            failed += 1
    return passed, failed

p, f = summarise(["PASS", "FAIL", "PASS", "PASS"])
print(f"Passed: {p}, Failed: {f}")      # Passed: 3, Failed: 1
```

If you don't unpack, you get the tuple:

```python
outcome = summarise(["PASS", "FAIL"])
print(outcome)         # (1, 1)
print(outcome[0])      # 1
```

For many return values, a dictionary with named keys is clearer than a long tuple, because the reader doesn't have to remember the order:

```python
def summarise(results):
    passed = results.count("PASS")
    total = len(results)
    return {"passed": passed, "failed": total - passed, "total": total}

summary = summarise(["PASS", "FAIL", "PASS"])
print(summary["failed"])       # 1
```

---

### 7. Early Returns

Because `return` ends the function, you can use it to handle special cases first and keep the main logic un-nested. This is the function equivalent of `break` from Tuesday.

```python
def calculate_pass_rate(passed, total):
    if total == 0:
        return 0.0                 # avoid dividing by zero
    return passed / total * 100

print(calculate_pass_rate(0, 0))       # 0.0
print(calculate_pass_rate(3, 4))       # 75.0
```

Without the early return, you'd need an `else` and an extra level of indentation. Another example, validating an ID:

```python
def is_valid_test_id(test_id):
    if not test_id.startswith("TC-"):
        return False
    number_part = test_id[3:]
    if not number_part.isdigit():
        return False
    return len(number_part) == 3

print(is_valid_test_id("TC-007"))     # True
print(is_valid_test_id("TC-7"))       # False
print(is_valid_test_id("XX-007"))     # False
print(is_valid_test_id("TC-ABC"))     # False
```

Each `if` rejects one kind of bad input; if the ID survives all checks, the final line decides. This "guard clause" style reads clearly and is easy to extend.

**Make sure every path returns something.** If a path ends without `return`, that path gives `None`:

```python
def grade(score):
    if score >= 50:
        return "PASS"
    # forgot the failing case: returns None for scores below 50
```

Write `return "FAIL"` for the other case (or an `else`).

---

### 8. Using Functions Inside Expressions and Conditions

Because a call produces a value, you can use it anywhere a value fits:

```python
if is_valid_test_id(user_input):
    print("Valid ID")

total = calculate_pass_rate(8, 10) + calculate_pass_rate(4, 5)

message = f"Rate: {calculate_pass_rate(22, 25):.1f}%"

print(max(calculate_pass_rate(1, 2), calculate_pass_rate(3, 4)))
```

**Nesting calls** works from the inside out, like the `int(input(...))` pattern you know.

---

### 9. Parameters Are Local Variables (and Mutable Arguments)

Parameters behave like local variables: reassigning one inside the function does **not** change the caller's variable.

```python
def double(n):
    n = n * 2
    return n

value = 5
result = double(value)
print(value)      # 5   (unchanged)
print(result)     # 10
```

But with **mutable** objects (lists, dictionaries, sets), the function receives a reference to the *same object*. If it modifies the object in place, the caller sees the change:

```python
def add_test(queue, test_id):
    queue.append(test_id)          # changes the caller's list!

my_queue = ["TC-001"]
add_test(my_queue, "TC-002")
print(my_queue)                    # ['TC-001', 'TC-002']
```

This is the same aliasing behaviour you saw with `b = a` for lists. It is sometimes what you want (like `append`), but it can cause surprises. Good practice:

- Make it clear in the **name and docstring** if a function modifies its argument ("add_test_to_queue").
- If you don't want to modify the original, work on a copy:

```python
def sorted_unique(ids):
    return sorted(set(ids))        # builds a new list, input untouched

def with_extra(ids, extra):
    new_list = ids.copy()
    new_list.append(extra)
    return new_list
```

Prefer functions that **return new values** over ones that silently change their inputs; they're easier to reason about.

Reassigning (as in `queue = [...]`) rebinds the *local name* and does not affect the caller's list. Only in-place operations such as `append`, `sort` or item assignment modify the shared object.

---

### 10. Documenting Parameters and Return Values

A good docstring says what goes in and what comes out:

```python
def calculate_pass_rate(passed, total):
    """Return the pass percentage as a float.

    passed: number of tests that passed
    total: total number of tests run
    Returns 0.0 when total is 0.
    """
    if total == 0:
        return 0.0
    return passed / total * 100
```

#### Type hints (optional but valuable)

Python lets you *annotate* parameters and return values with types:

```python
def calculate_pass_rate(passed: int, total: int) -> float:
    ...

def is_valid_test_id(test_id: str) -> bool:
    ...
```

`name: type` describes a parameter; `-> type` describes the return value. **Python does not enforce hints when running**, but editors use them to catch mistakes and to give better suggestions, and teammates can see what is expected at a glance. Many professional teams require them. We'll use them lightly from now on.

---

### 11. Putting It Together: The Refactored Report

Recall the report script from the previous lesson, which hard-coded its data. Now with parameters and returns:

```python
def count_passed(results):
    """Return how many results are 'PASS'."""
    return results.count("PASS")

def calculate_pass_rate(passed, total):
    """Return the pass percentage (0.0 if total is 0)."""
    if total == 0:
        return 0.0
    return passed / total * 100

def format_summary(suite_name, results):
    """Return a one-line summary string for a suite."""
    passed = count_passed(results)
    total = len(results)
    rate = calculate_pass_rate(passed, total)
    return f"{suite_name}: {passed}/{total} passed ({rate:.1f}%)"

def main():
    login_results = ["PASS", "FAIL", "PASS", "PASS"]
    search_results = ["PASS", "PASS"]
    print(format_summary("Login", login_results))
    print(format_summary("Search", search_results))

main()
```

```text
Login: 3/4 passed (75.0%)
Search: 2/2 passed (100.0%)
```

Notice what improved:

- Each function does **one thing** and **returns** a value.
- `format_summary` is reused for two suites with different data.
- Nothing prints except where we choose to (`main`).
- Each small function can be tested on its own.

---

### 12. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Using `print` where `return` is needed | Result is `None` | Return the value; print outside |
| Forgetting `return` | Function gives `None` | Add `return` |
| Code after `return` | Never runs | Place it before the return |
| Wrong argument count | `TypeError` | Match the parameters |
| Wrong argument order | Silent wrong results | Use keyword arguments |
| Positional after keyword | `SyntaxError` | Positional first |
| Expecting reassignment to change the caller's variable | `n = n * 2` has no effect outside | Return the new value |
| Modifying an argument unexpectedly | Caller's list changed | Copy first, or document it |
| Not storing the return value | `add(2, 3)` on its own line | `result = add(2, 3)` |
| Not all paths return | Sometimes `None` | Cover every path |
| Using a global instead of a parameter | Hidden dependency | Pass the data in |

---

### 13. Practice Activities

1. **Square.** Write `square(n)` that returns `n * n`. Print `square(4)`, `square(square(2))` and `square(1.5)`.
2. **Greeting.** Write `make_greeting(name, role)` that *returns* `"Welcome, <name> (<role>)"`. Print the result of two calls.
3. **Even.** Write `is_even(n)` returning a boolean. Use it in an `if` to print "even" or "odd" for a number from `input()`.
4. **Pass rate.** Write `calculate_pass_rate(passed, total)` with an early return for `total == 0`. Test with `(0, 0)`, `(5, 10)` and `(10, 10)`.
5. **Print vs return.** Write `add_print` and `add_return`. Try `result * 10` with each. Explain the difference.
6. **Keyword arguments.** Write `make_test_id(prefix, number)`. Call it three ways: positionally, with keywords in order, and with keywords in reversed order.
7. **Multiple returns.** Write `min_and_max(numbers)` returning the smallest and largest value; unpack the result into two variables. (You may use `min()` and `max()`.)
8. **Validator.** Extend `is_valid_test_id` to also accept IDs like `TC-LOGIN-007` (prefix, module in capitals, 3-digit number). Test with five good and five bad IDs.
9. **Spot the bug.** Why does `grade(30)` return `None`? Fix it:
   ```python
   def grade(score):
       if score >= 50:
           return "PASS"
   ```
10. **Mutable argument.** Write `remove_duplicates(items)` in two versions: one that modifies the original list in place, and one that returns a new list. Show the difference by printing the original afterwards.
11. **Refactor.** Take your summary calculator from Monday's exercise: move the calculation into `calculate_pass_rate`, move the formatting into `format_summary`, and keep input/printing in `main`. Commit with a clear message.
12. **Docstrings and hints.** Add docstrings and type hints to all of the functions you wrote today.

---

## Summary

- A **parameter** is the name in the `def` line; an **argument** is the value you pass in a call.
- Pass arguments **by position** or **by keyword** (`name=value`); positional ones come first. The wrong number of arguments gives a `TypeError`.
- **`return value`** ends the function and sends the value back; the call is replaced by that value, so you can store it or use it in an expression.
- **`print` shows, `return` hands back.** Functions that compute or decide should return; callers decide what to display.
- A function without `return` gives **`None`**. Make sure every code path returns what you intend.
- Return several values with commas (a tuple) and unpack them; use a dictionary when there are many.
- **Early returns** (guard clauses) handle special cases first and keep functions flat.
- Parameters are local; reassigning them doesn't affect the caller, but **mutating** a list or dictionary does. Prefer returning new values or copy first.
- Use docstrings and optional **type hints** to document inputs and outputs.
- Next: **default and variable-length arguments** make functions flexible with optional inputs.

---

## Additional Resources

- Python Tutorial: More on Defining Functions: https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions
- Python documentation: Glossary entries for "argument" and "parameter": https://docs.python.org/3/glossary.html#term-argument
- Real Python: The Python `return` Statement: https://realpython.com/python-return-statement/
