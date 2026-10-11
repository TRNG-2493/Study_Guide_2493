# Conditional Statements: if, elif, else

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a conditional statement is and why programs need to make decisions.
- Write `if`, `if-else` and `if-elif-else` statements with correct syntax and indentation.
- Build conditions using comparison operators, logical operators (`and`, `or`, `not`) and membership (`in`).
- Predict which branch of a decision chain will run, and why order matters.
- Nest conditions and know when to simplify them.
- Use truthiness to write concise conditions.
- Use a one-line conditional expression.
- Recognize and fix the most common beginner errors with conditionals.

---

## Why This Matters

So far, every program you've written ran straight from the first line to the last. Real programs must **decide**. A login page behaves differently for a correct password and a wrong one. A test either **passes or fails**. A response with status 200 is success, 404 means "not found", and 500 means the server broke.

Decision-making is the heart of test automation. Every check a test performs is a decision:

> *If the actual result matches the expected result, report PASS. Otherwise, report FAIL.*

This week's goal is to go from zero to writing small, useful Python programs. Today's pass/fail grader in the demo, and the number-guessing game in the exercise, both depend on the statements you learn here. In the last lesson on Monday, you learned that comparisons produce `True` or `False`. Today we use those booleans to **control which code runs**.

---

## The Concept

### 1. Control Flow: Choosing a Path

**Control flow** is the order in which a program's lines execute. By default it is top to bottom. A **conditional statement** lets the program choose between different paths depending on a condition.

**Analogy:** think of a fork in the road with a sign. "If the bridge is open, go straight; otherwise, take the detour." The condition (bridge open?) decides which road you take.

```
              ┌───────────────┐
              │  condition?   │
              └───────┬───────┘
          True        │        False
      ┌───────────────┴──────────────┐
      ▼                              ▼
 run this block                 run other block
```

---

### 2. The `if` Statement

Syntax:

```python
if condition:
    # code that runs only when the condition is True
```

Example:

```python
status_code = 200

if status_code == 200:
    print("Request succeeded")

print("Done")
```

Output:

```text
Request succeeded
Done
```

Let's examine each part, because the syntax rules are strict:

1. **`if`** is a keyword that starts the statement.
2. **`status_code == 200`** is the **condition**, any expression that is `True` or `False`.
3. **The colon `:`** at the end of the line is required. Forgetting it causes a `SyntaxError`.
4. **The indented block** (4 spaces) holds the code that runs only if the condition is `True`. This is where the indentation rule from Monday finally becomes essential. Python uses indentation, not curly braces, to know which lines belong to the `if`.
5. `print("Done")` is **not indented**, so it is outside the `if` and always runs.

If we change `status_code` to `404`, the condition is `False`, the indented line is skipped, and only `Done` is printed.

#### Indentation is meaning

```python
score = 40

if score >= 50:
    print("Passed")
    print("Well done")     # also part of the if block
print("Finished")           # always runs
```

All lines at the same indentation after the colon belong to the same block. Use exactly **4 spaces** per level (VS Code's Tab key does this). Never mix tabs and spaces.

---

### 3. The `if-else` Statement

What should happen when the condition is **not** true? Add `else`:

```python
actual_title = "Dashboard"
expected_title = "Home"

if actual_title == expected_title:
    print("PASS: page title matches")
else:
    print("FAIL: page title does not match")
```

```text
FAIL: page title does not match
```

- Exactly **one** of the two blocks runs, never both, never neither.
- `else` has no condition; it means "everything that wasn't covered by the `if`".
- `else` also needs a colon and an indented block, and it lines up vertically with its `if`.

A pattern you'll see in every test script:

```python
expected = 5
actual = 2 + 3

if actual == expected:
    print(f"PASS: expected {expected}, got {actual}")
else:
    print(f"FAIL: expected {expected}, got {actual}")
```

---

### 4. The `if-elif-else` Chain

Often there are more than two possibilities. `elif` (short for "else if") adds extra conditions to check in order:

```python
score = 72

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(f"Score {score} gets grade {grade}")
```

```text
Score 72 gets grade C
```

**How Python reads this:**

1. Is `score >= 90`? No (72). Move on.
2. Is `score >= 75`? No. Move on.
3. Is `score >= 60`? **Yes.** Run that block, set `grade = "C"`.
4. **Skip everything else.** Once one branch runs, the rest of the chain is ignored.

#### Order matters

Because the first matching branch wins, the order of your conditions is part of the logic. Look at this incorrect version:

```python
score = 95

if score >= 60:          # True for 95! This wins, and the rest is never checked
    grade = "C"
elif score >= 75:
    grade = "B"
elif score >= 90:
    grade = "A"
```

A score of 95 gets a `C` because the loosest condition was checked first. **Order your conditions from most specific to most general**, or make them mutually exclusive.

#### Rules for the chain

- You can have **one** `if`, **any number** of `elif`s, and **at most one** `else` (which must be last).
- `else` is optional. Without it, nothing happens if no condition matches.
- Separate `if` statements are **not** the same as an `elif` chain. Compare:

```python
x = 10

# Chain: only one block can run
if x > 5:
    print("greater than 5")
elif x > 8:
    print("greater than 8")      # never runs, even though it is true

# Separate ifs: each is checked independently
if x > 5:
    print("greater than 5")
if x > 8:
    print("greater than 8")      # also runs
```

Use `elif` when the options are alternatives; use separate `if`s when several things can be true together.

---

### 5. Building Conditions

#### 5.1 Comparison operators (recap)

`==`, `!=`, `>`, `<`, `>=`, `<=` each give a boolean.

```python
age = 20
if age >= 18:
    print("Adult")
```

#### 5.2 Logical operators: combining conditions

```python
status_code = 200
response_time = 1.4

if status_code == 200 and response_time < 2.0:
    print("PASS: OK and fast")
else:
    print("FAIL: wrong status or too slow")
```

- `and`: both conditions must be true.
- `or`: at least one must be true.
- `not`: flips a condition.

```python
role = "admin"

if role == "admin" or role == "manager":
    print("Access to reports granted")

is_locked = False
if not is_locked:
    print("Account is active")
```

**Common mistake:** you cannot write `if role == "admin" or "manager":`. That doesn't mean what it looks like. Python reads `"manager"` as a separate condition and, because a non-empty string is always truthy, the whole condition is always true. Write the full comparison on each side of `or`, as shown above.

#### 5.3 Chained comparisons

Python lets you write ranges naturally:

```python
temperature = 22

if 18 <= temperature <= 25:
    print("Comfortable")
```

This is the same as `18 <= temperature and temperature <= 25` and reads like maths.

#### 5.4 Membership with `in` and `not in`

```python
status = "FAIL"

if status in ("FAIL", "ERROR", "BLOCKED"):
    print("Needs attention")

filename = "login_test.py"
if "test" in filename:
    print("This looks like a test file")
```

The `("FAIL", "ERROR", "BLOCKED")` is a group of values; we will study these groups (called tuples, lists and sets) properly on Wednesday. For now, you can read it as "is `status` one of these three?". This is far tidier than three `==` comparisons joined by `or`.

#### 5.5 Comparing strings

Remember that string comparison is **case-sensitive** and cares about spaces. Normalize before comparing:

```python
answer = input("Continue? (yes/no): ").strip().lower()

if answer == "yes":
    print("Continuing...")
elif answer == "no":
    print("Stopping.")
else:
    print("Please type yes or no.")
```

If the user types `  YES  `, `.strip().lower()` turns it into `"yes"` and the comparison works. This is a pattern you'll reuse constantly.

---

### 6. Truthiness in Conditions

From the type-conversion lesson: zero, empty text and `None` are **falsy**; most other things are **truthy**. An `if` automatically applies this rule, so you can write shorter conditions:

```python
username = input("Username: ").strip()

if username:                  # True when the text is not empty
    print(f"Hello, {username}")
else:
    print("Username cannot be empty")
```

`if username:` is equivalent to `if username != "":`. Likewise:

```python
failed_count = 0

if failed_count:              # 0 is falsy
    print("Some tests failed")
else:
    print("No failures")
```

For beginners, explicit comparisons (`failed_count > 0`) are often clearer. Use truthiness when it reads naturally, especially for empty-text checks.

#### Comparing with None

Use `is None` / `is not None` to check for "no value":

```python
actual_result = None

if actual_result is None:
    print("Test has not run yet")
```

---

### 7. Nested Conditionals

You can place an `if` inside another `if`. Each level needs more indentation:

```python
is_logged_in = True
role = "admin"

if is_logged_in:
    if role == "admin":
        print("Show admin dashboard")
    else:
        print("Show user dashboard")
else:
    print("Redirect to login page")
```

Nesting is sometimes needed, but deep nesting becomes hard to read. Often you can flatten it using `and`:

```python
if is_logged_in and role == "admin":
    print("Show admin dashboard")
elif is_logged_in:
    print("Show user dashboard")
else:
    print("Redirect to login page")
```

As a guideline, if you find yourself nesting more than two or three levels, look for a simpler structure.

---

### 8. Conditional Expressions (One-Line `if-else`)

For choosing between **two values**, Python offers a compact form:

```python
value_if_true  if  condition  else  value_if_false
```

```python
passed = 22
total = 25

result = "PASS" if passed == total else "FAIL"
print(result)         # FAIL

age = 17
category = "adult" if age >= 18 else "minor"
```

It is great for simple assignments. Don't use it for complicated logic or to run multiple statements; use a regular `if` for those.

---

### 9. The `pass` Placeholder

Python does not allow an empty block. If you want to write the structure now and fill in the details later, use `pass`, which does nothing:

```python
if status_code == 500:
    pass        # TODO: handle server errors later
```

---

### 10. Realistic Examples

#### Example A: HTTP status classifier

```python
status_code = int(input("Enter HTTP status code: "))

if 200 <= status_code < 300:
    category = "Success"
elif 300 <= status_code < 400:
    category = "Redirection"
elif 400 <= status_code < 500:
    category = "Client error"
elif 500 <= status_code < 600:
    category = "Server error"
else:
    category = "Unknown"

print(f"{status_code}: {category}")
```

Sample runs: `201` prints `201: Success`; `404` prints `404: Client error`; `999` prints `999: Unknown`.

#### Example B: Pass/fail grader (similar to today's demo)

```python
student = input("Name: ").strip()
score = int(input("Score (0-100): "))

if score < 0 or score > 100:
    print("Invalid score; it must be between 0 and 100")
elif score >= 50:
    print(f"{student}: PASS ({score})")
else:
    print(f"{student}: FAIL ({score})")
```

Notice we **validate first**. Checking for invalid input at the top of the chain prevents the other branches from treating a nonsense score like 150 as a pass.

#### Example C: Test result evaluator

```python
expected_status = 200
actual_status = 404
expected_time_limit = 2.0
actual_time = 0.8

if actual_status != expected_status:
    result = "FAIL"
    reason = f"status {actual_status}, expected {expected_status}"
elif actual_time > expected_time_limit:
    result = "FAIL"
    reason = f"too slow: {actual_time}s"
else:
    result = "PASS"
    reason = "all checks passed"

print(f"{result} - {reason}")
```

```text
FAIL - status 404, expected 200
```

Because the first check failed, the others weren't even evaluated. This mirrors how many real tests stop reporting at the first failed assertion.

---

### 11. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Using `=` instead of `==` | `if x = 5:` (SyntaxError) | `if x == 5:` |
| Missing colon | `if x == 5` | `if x == 5:` |
| Forgetting to indent | `if x:` then `print()` at the left margin | Indent the block 4 spaces |
| Inconsistent indentation | 4 spaces on one line, 3 on the next | Use 4 spaces consistently |
| `or` shortcut | `if x == 1 or 2:` | `if x == 1 or x == 2:` |
| Wrong condition order | General case first | Order from most specific to most general |
| Comparing text with numbers | `"5" > 3` TypeError | Convert with `int()` first |
| Using `if` where `elif` is needed | Two blocks both run | Use `elif` for alternatives |
| Unreachable `else` | Conditions overlap logic | Trace with sample values |

**Debugging tip:** when a branch isn't behaving as expected, print the values being compared right before the `if`. Often you'll spot an extra space, wrong case or wrong type.

---

### 12. Practice Activities

1. **Even or odd.** Ask for a whole number and print whether it is even or odd (hint: `%`).
2. **Login check.** Store a username and password in variables. Ask the user for both and print `Login successful` only if both match, otherwise `Invalid credentials`.
3. **Grade ranges.** Convert a numeric score into A, B, C, D or F using `if-elif-else`. Test each boundary (90, 89, 75, 74, 60, 59).
4. **Order bug.** The following always prints "Low". Explain why and fix it.
   ```python
   price = 500
   if price > 10:
       print("Low")
   elif price > 100:
       print("Medium")
   elif price > 400:
       print("High")
   ```
5. **Leap year.** A year is a leap year if divisible by 4, except years divisible by 100, unless also divisible by 400. Write a program that tests this using `and`, `or` and `%`.
6. **Response checker.** Given `status_code` and `response_time` (as input), print `PASS` only if the status is 200 and time is under 2 seconds. Otherwise print which check failed.
7. **Ternary.** Rewrite Practice 1 using a conditional expression.
8. **Test table.** For Example C above, change the values to exercise all three outcomes (status mismatch, too slow, all good), and write down what you expect before each run.

---

## Summary

- Conditionals let a program **choose** which code runs, the basis of every test check (PASS or FAIL).
- Syntax: `if condition:` followed by an **indented block**. The **colon** and **indentation** are mandatory.
- `else` handles "everything else"; `elif` adds more conditions. Python runs **only the first matching** branch, so **order matters**.
- Build conditions with comparisons (`== != < > <= >=`), logical operators (`and`, `or`, `not`), chained comparisons (`18 <= x <= 25`) and membership (`in`).
- Normalize text (`.strip().lower()`) before comparing; remember `=` assigns while `==` compares.
- Truthiness lets `if value:` replace explicit checks for empty or zero values; use `is None` for `None`.
- Nested conditionals work but are easier to read when flattened; a conditional expression (`a if cond else b`) handles simple two-way choices.
- Next lessons: **loops** (repeat code) and **break/continue** (control loops), the other half of control flow.

---

## Additional Resources

- Python Tutorial: `if` Statements: https://docs.python.org/3/tutorial/controlflow.html#if-statements
- Python documentation: Truth Value Testing: https://docs.python.org/3/library/stdtypes.html#truth-value-testing
- Real Python: Conditional Statements in Python: https://realpython.com/python-conditional-statements/
