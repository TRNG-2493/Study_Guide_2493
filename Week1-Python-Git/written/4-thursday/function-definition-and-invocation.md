# Function Definition and Invocation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a function is and why programs are built from functions.
- Define a function with `def` and call (invoke) it.
- Describe the difference between **defining** a function and **calling** it.
- Follow the order in which Python runs code when functions are involved.
- Write a docstring that documents what a function does.
- Explain local and global scope and why variables created inside a function are not visible outside.
- Call one function from another and organise a program around a `main` function.
- Refactor a repetitive script into small, named functions.
- Recognise and fix the most common beginner errors with functions.

---

## Why This Matters

You have already been using functions all week: `print()`, `input()`, `len()`, `int()`, `range()`, `sorted()`. Each one packages some work behind a name, so you can say *what* you want without repeating *how* it is done every time.

Today you learn to **write your own**. Why does that matter?

- **No copy and paste.** If a script formats a test ID in five places, a bug in the format means five fixes. With a function, there is one place to fix.
- **Readability.** A program that reads `validate_test_id(...)`, then `calculate_pass_rate(...)`, then `print_summary(...)` explains itself.
- **Testability.** Small functions can be checked on their own.
- **Reuse.** The same function can serve many scripts and many teammates.

In test automation this is everything. Test frameworks are built from functions: one logs in, one opens a page, one checks a title, one generates random test data. Tomorrow you learn classes, which group functions and data. Today's demo asks you to refactor a script into functions, and today's pair-programming exercise builds a reusable test-utility library, so function skills are the foundation of the whole day.

This lesson builds on yesterday's collections and on Tuesday's loops and conditionals, which you will place *inside* functions.

---

## The Concept

### 1. The Problem: Repetition

Look at this script, which prints a banner before each test:

```python
print("=" * 30)
print("Running: Login test")
print("=" * 30)

# ... login test steps ...

print("=" * 30)
print("Running: Search test")
print("=" * 30)

# ... search test steps ...

print("=" * 30)
print("Running: Checkout test")
print("=" * 30)
```

The same three lines repeat. If you want to change the banner width or style, you must edit each copy and not miss one. Programmers have a rule for this: **DRY, "Don't Repeat Yourself."**

A function lets us write the three lines **once**, give them a name, and run them whenever we like.

---

### 2. Defining a Function

Syntax:

```python
def function_name():
    # indented block: the function body
```

Our banner as a function:

```python
def print_banner():
    print("=" * 30)
    print("Running a test")
    print("=" * 30)
```

Let's examine each part:

1. **`def`** is the keyword that means "I am defining a function".
2. **`print_banner`** is the **function name**. It follows the same rules and conventions as variable names: letters, digits and underscores, `snake_case`, meaningful. Good function names are usually **verbs**, because functions *do* something (`print_banner`, `calculate_total`, `is_valid`).
3. **`()`** parentheses come after the name. They hold the function's inputs, called parameters (next lesson). They are empty for now, but they are **required**.
4. **The colon `:`** ends the line, as with `if` and `for`.
5. **The indented body** (4 spaces) is the code that belongs to the function.

> **Defining does not run.** When Python reads a `def`, it only *remembers* the function under that name. Nothing inside is executed until you call the function.

Try this:

```python
def print_banner():
    print("=" * 30)
    print("Running a test")
    print("=" * 30)

print("Program starts")
```

Output:

```text
Program starts
```

The banner did not appear, because we haven't *called* the function.

---

### 3. Calling (Invoking) a Function

To run a function, write its name followed by parentheses:

```python
def print_banner():
    print("=" * 30)
    print("Running a test")
    print("=" * 30)

print_banner()
print_banner()
```

```text
==============================
Running a test
==============================
==============================
Running a test
==============================
```

Each call runs the body from top to bottom, then returns to where it was called from.

The **parentheses matter**:

```python
print_banner()     # CALLS the function: runs the body
print_banner       # just refers to the function object; nothing runs
```

Forgetting the parentheses is a very common mistake; the program doesn't crash, but nothing happens.

#### The function must be defined before it is called

Python reads top to bottom. This fails:

```python
greet()                # NameError: name 'greet' is not defined

def greet():
    print("Hello")
```

The call happens before Python has seen the definition. Define first, call after.

---

### 4. How Python Runs a Program With Functions

Follow this program carefully:

```python
def say_hello():
    print("  Inside say_hello: start")
    print("  Hello, tester!")
    print("  Inside say_hello: end")

print("1. Program begins")
say_hello()
print("2. Back in the main program")
say_hello()
print("3. Program ends")
```

Output:

```text
1. Program begins
  Inside say_hello: start
  Hello, tester!
  Inside say_hello: end
2. Back in the main program
  Inside say_hello: start
  Hello, tester!
  Inside say_hello: end
3. Program ends
```

The order of execution:

1. Python reads the `def` and remembers `say_hello` (no output).
2. It runs `print("1. Program begins")`.
3. At the call `say_hello()`, **execution jumps into the function**, runs its three lines, then **jumps back** to the line after the call.
4. And so on for the second call.

```
 main program                 say_hello()
 ┌─────────────┐
 │ print "1."  │
 │ say_hello() ├────────────▶ ┌──────────────┐
 │             │              │ body runs    │
 │ print "2."  │◀──────────── └──────────────┘
 └─────────────┘     returns here
```

Understanding this "jump in, jump back" is the key to reading programs made of functions. When you debug, `print` statements inside functions help you see the flow.

---

### 5. Functions Can Do Anything Normal Code Can

The body can contain variables, conditionals, loops, even calls to other functions.

```python
def print_test_ids():
    for number in range(1, 6):
        print(f"TC-{number:03d}")

print_test_ids()
```

```text
TC-001
TC-002
TC-003
TC-004
TC-005
```

```python
def check_status():
    status_code = 404
    if status_code == 200:
        print("OK")
    else:
        print(f"Problem: {status_code}")

check_status()      # Problem: 404
```

Right now these functions are rigid: they always use the same data. In the next lesson you will learn **parameters** (to give a function different inputs) and **return values** (to get results back). Together they make functions truly reusable.

---

### 6. Docstrings: Documenting a Function

A **docstring** is a string placed as the first statement in the function body. It documents what the function does. Use triple quotes:

```python
def print_banner():
    """Print a three-line banner used to separate test runs."""
    print("=" * 30)
    print("Running a test")
    print("=" * 30)
```

Why bother?

- Teammates (and future you) can read what the function is for without studying the code.
- Editors such as VS Code show the docstring when you hover over the function name.
- Python can display it with `help()`:

```python
help(print_banner)
```

```text
Help on function print_banner in module __main__:

print_banner()
    Print a three-line banner used to separate test runs.
```

Guidelines:

- Start with a short one-line summary in the imperative mood ("Print...", "Return...", "Check...").
- For longer functions, add a blank line and more details, such as what the parameters mean and what is returned (we'll see this in the next lessons).

**Comments vs docstrings:** a *comment* (`# ...`) explains a specific line of code; a *docstring* describes the whole function from the outside.

---

### 7. Variable Scope: Where Do Names Live?

Variables created **inside** a function are **local**: they exist only while the function runs and cannot be seen from outside.

```python
def make_greeting():
    message = "Hello from inside"
    print(message)

make_greeting()
print(message)
```

```text
Hello from inside
NameError: name 'message' is not defined
```

`message` was born when the function started and disappeared when it finished. This is a **feature**: functions don't accidentally overwrite each other's variables.

```python
def first():
    count = 10
    print("first:", count)

def second():
    count = 99               # a different, separate variable
    print("second:", count)

first()        # first: 10
second()       # second: 99
```

Both functions have a variable called `count`, and they don't interfere.

#### Global variables

A variable created **outside** any function is **global**; it can be *read* from inside functions:

```python
BASE_URL = "https://example.com"

def show_url():
    print(f"Testing {BASE_URL}")

show_url()        # Testing https://example.com
```

Reading a global is fine, especially for constants (named in `UPPER_CASE` by convention). But **assigning** to a name inside a function creates a *new local variable* rather than changing the global:

```python
counter = 0

def add_one():
    counter = counter + 1      # UnboundLocalError

add_one()
```

Python sees the assignment and decides `counter` is local, so the right-hand `counter` hasn't been given a value yet. There is a `global` keyword to override this, but modifying globals from functions makes programs hard to understand and test, so avoid it. The better approach is to **pass values in** and **return results out**. That is exactly what the next lesson covers.

**Scope summary (the LEGB rule, simplified):** when Python sees a name, it looks first in the **L**ocal scope (the current function), then any **E**nclosing function (you'll meet this with closures), then **G**lobal (the file), then **B**uilt-ins (`print`, `len`...). The first match wins.

---

### 8. Functions Calling Functions

Functions can call other functions, which lets you build big behaviour from small pieces:

```python
def print_line():
    print("-" * 30)

def print_header():
    print_line()
    print("TEST REPORT")
    print_line()

def print_footer():
    print_line()
    print("End of report")

def print_report():
    print_header()
    print("Login ......... PASS")
    print("Search ........ FAIL")
    print_footer()

print_report()
```

```text
------------------------------
TEST REPORT
------------------------------
Login ......... PASS
Search ........ FAIL
------------------------------
End of report
```

`print_report` reads like an outline of what the report contains. A function should do **one clear job**, and its name should tell you what that job is.

---

### 9. The `main()` Pattern

As programs grow, it helps to put the "main flow" in a function called `main`, and call it once at the bottom:

```python
def print_header():
    print("=== Test Run ===")

def run_tests():
    print("Running tests...")

def print_summary():
    print("All done.")

def main():
    print_header()
    run_tests()
    print_summary()

main()
```

Benefits: the top-level story of the program is in one place, and variables created in `main` are local rather than global.

You will often see this version in Python files, which you will understand fully in the last lesson of the day:

```python
if __name__ == "__main__":
    main()
```

For now, treat it as "run `main()` when this file is executed directly".

---

### 10. Refactoring: From a Script to Functions

**Refactoring** means restructuring code *without changing what it does*, to make it clearer. This is the heart of today's demo.

**Before:** one long script.

```python
print("=" * 30)
print("TEST REPORT")
print("=" * 30)

results = ["PASS", "FAIL", "PASS", "PASS"]

passed = 0
for r in results:
    if r == "PASS":
        passed += 1

print(f"Passed: {passed}")
print(f"Total: {len(results)}")

print("=" * 30)
print("End of report")
print("=" * 30)
```

**After:** the same behaviour with named steps.

```python
def print_header():
    print("=" * 30)
    print("TEST REPORT")
    print("=" * 30)

def print_footer():
    print("=" * 30)
    print("End of report")
    print("=" * 30)

def print_counts():
    results = ["PASS", "FAIL", "PASS", "PASS"]
    passed = 0
    for r in results:
        if r == "PASS":
            passed += 1
    print(f"Passed: {passed}")
    print(f"Total: {len(results)}")

def main():
    print_header()
    print_counts()
    print_footer()

main()
```

The output is identical, but the program is organised. In the next lesson, with parameters and return values, we will improve it further, so that `print_counts` takes the results as an input instead of hard-coding them.

**How to refactor, step by step:**

1. Look for blocks of code that do one identifiable thing.
2. Give the block a clear, verb-based name.
3. Move it into a `def`.
4. Replace the original block with a call.
5. Run the program and confirm the output is unchanged.
6. **Commit** the working refactor (a nice Git habit: one refactor, one commit).

---

### 11. The Empty Function and `pass`

You can sketch the structure of a program before writing the details by using `pass` as a placeholder (you saw it with `if` on Tuesday):

```python
def check_login():
    pass          # TODO: implement later

def check_search():
    pass
```

Python needs *something* in the body, and `pass` does nothing. This is handy for planning.

---

### 12. Built-in vs User-defined Functions

| | Built-in | User-defined |
|---|---|---|
| Who wrote it? | Python's creators | You |
| Examples | `print`, `len`, `sorted`, `input` | `print_banner`, `check_status` |
| Needs `def`? | No, always available | Yes |

Remember also the **methods** from yesterday (`my_list.append(...)`): they are functions that belong to an object. Friday's lessons on classes explain how you can define your own.

**Don't reuse built-in names** for your functions or variables. For example, avoid naming something `list`, `print`, `sum` or `input`, because you will hide the original and break code that relies on it.

---

### 13. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Forgetting the colon | `def greet()` | `def greet():` |
| Forgetting the parentheses on a call | `greet` | `greet()` |
| Calling before defining | Call at the top, `def` below | Define first |
| Bad indentation | Body not indented | Indent the body by 4 spaces |
| Expecting local variables outside | `NameError` | Keep variables inside, or return them (next lesson) |
| Trying to change a global without `global` | `UnboundLocalError` | Pass in and return values instead |
| Giving a function the same name as a built-in | `def print():` | Choose a unique, descriptive name |
| Defining a function but never calling it | Nothing happens | Call it |
| A function doing too many things | 80-line function | Split into smaller ones |
| Vague names | `def do_it():` | `def print_summary():` |

---

### 14. Practice Activities

1. **Hello.** Write `greet()` that prints a greeting, and call it three times.
2. **Order.** Predict the exact output before running:
   ```python
   def a():
       print("A start")
       b()
       print("A end")

   def b():
       print("B")

   print("Begin")
   a()
   print("Finish")
   ```
3. **Banner.** Create `print_banner()` that prints a line of 40 dashes. Use it before and after a three-line message.
4. **Scope.** Create a function that sets a local variable, then try to print it outside. Read the error, then fix the program.
5. **Docstrings.** Add a docstring to each of your functions and view one with `help()`.
6. **Test IDs.** Write `print_test_ids()` that prints `TC-001` to `TC-010` with a loop.
7. **Composition.** Write `print_header()`, `print_body()` and `print_footer()`, and a `print_report()` that calls all three.
8. **Refactor.** Take any script from Monday or Tuesday (for example the test summary calculator) and break it into at least three functions plus a `main()`. Confirm the output is unchanged, then commit it to Git with a message like `Refactor summary script into functions`.
9. **Spot the bug.** Why does this print nothing, and how do you fix it?
   ```python
   def show():
       print("Hello")
   show
   ```
10. **Plan.** On paper, list 5 small jobs a login test would do (for example "open page", "enter username"). Turn each into a function name using `verb_noun` style.

---

## Summary

- A **function** is a named, reusable block of code. It removes repetition (DRY), improves readability and makes testing easier.
- **Define** with `def name():` followed by an indented body; **call** with `name()`. Defining does not run the code; **calling** does.
- Functions must be defined before they are called. When a function is called, execution jumps into the body and returns to the line after the call.
- A **docstring** (triple-quoted string first in the body) documents the function and is shown by `help()` and by editors.
- Variables created inside a function are **local**; they disappear when the function ends. Globals can be read inside functions, but avoid changing them there.
- Functions can call other functions; a **`main()`** function holds the top-level flow.
- **Refactoring** turns repetitive scripts into small, named steps without changing behaviour; commit each step.
- Next: **parameters, arguments and return values** let functions receive inputs and send results back, which is what makes them truly reusable.

---

## Additional Resources

- Python Tutorial: Defining Functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Python documentation: Naming and binding (scope rules): https://docs.python.org/3/reference/executionmodel.html#naming-and-binding
- Real Python: Defining Your Own Python Function: https://realpython.com/defining-your-own-python-function/
