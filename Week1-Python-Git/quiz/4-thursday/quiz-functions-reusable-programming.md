# Knowledge Check: Functions & Reusable Programming (Week 1 – Thursday)

Answer each question on your own first, then click "Click for Solution" to check your answer and read the explanation.

---

## Part 1: Multiple Choice

### Question 1

You define `def show_summary():` with three `print` lines in its body. Later, a teammate writes the line `show_summary` on its own. The script runs with no error, but nothing is displayed. Why?

- [ ] A) Python needs the function to be defined a second time before it can run
- [ ] B) Without parentheses the line only refers to the function object; it does not call it
- [ ] C) Functions can only print when they are called from inside another function
- [ ] D) The body of a function is skipped unless it has a `return` statement

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** A function runs only when it is called with parentheses, `show_summary()`. Writing the bare name just refers to the function object, so nothing happens and no error is raised.
- **Why others are wrong:**
  - A) A function is defined once; defining it never runs it, and defining it again would not help.
  - C) Functions can be called from top-level code; no enclosing function is needed.
  - D) A `return` statement is optional; a function without one still runs its body when called.
</details>

---

### Question 2

Given this definition and call, which statement is correct?

```python
def check_status(code):
    return 200 <= code < 300

check_status(404)
```

- [ ] A) `code` is an argument and `404` is a parameter
- [ ] B) Both `code` and `404` are parameters
- [ ] C) Both `code` and `404` are arguments
- [ ] D) `code` is a parameter and `404` is an argument

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** A parameter is the name listed in the `def` line (a placeholder), and an argument is the actual value passed in the call. Here `code` is the parameter and `404` is the argument.
- **Why others are wrong:**
  - A) This reverses the two terms.
  - B) Only names in the `def` line are parameters; `404` is a value supplied by the caller.
  - C) `code` is a placeholder name in the definition, not a value passed in.
</details>

---

### Question 3

Given `def print_test_result(test_id, status, duration):`, which call is a **SyntaxError**?

- [ ] A) `print_test_result(test_id="TC-001", "PASS", 1.2)`
- [ ] B) `print_test_result("TC-001", status="PASS", duration=1.2)`
- [ ] C) `print_test_result(duration=1.2, status="PASS", test_id="TC-001")`
- [ ] D) `print_test_result("TC-001", "PASS", duration=1.2)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Positional arguments must come before keyword arguments. Call A puts a keyword argument first and then positional ones, which Python rejects with a SyntaxError.
- **Why others are wrong:**
  - B) Positional first, then keywords, is the allowed pattern.
  - C) When every argument is a keyword, the order does not matter.
  - D) Two positional arguments followed by one keyword argument is valid.
</details>

---

### Question 4

Which function signature is valid Python?

- [ ] A) `def make_id(prefix="TC", number):`
- [ ] B) `def log(**kwargs, *args):`
- [ ] C) `def make_user(username, role="viewer", **extra):`
- [ ] D) `def build(**extra, role="viewer"):`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The required order is required parameters, then parameters with defaults, then `*args`, then keyword-only parameters, then `**kwargs`. Option C follows it: `username` (required), `role` (default), `**extra` (last).
- **Why others are wrong:**
  - A) A parameter without a default (`number`) cannot follow one with a default.
  - B) `**kwargs` must be the last parameter, so `*args` cannot come after it.
  - D) Nothing may follow `**extra`, so `role="viewer"` after it is a SyntaxError.
</details>

---

### Question 5

A QE helper is defined as `def run_suite(*test_ids):` and called with `run_suite("TC-001", "TC-002", "TC-003")`. What type is `test_ids` inside the function?

- [ ] A) A list
- [ ] B) A tuple
- [ ] C) A dictionary
- [ ] D) A string

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `*` gathers all extra positional arguments into a **tuple**. It can be looped over, measured with `len()` and indexed, but it is not a list.
- **Why others are wrong:**
  - A) A common mistake; if you need a list you must convert with `list(test_ids)`.
  - C) Dictionaries are produced by `**kwargs` (extra keyword arguments), not `*args`.
  - D) The three values are kept as separate items, not joined into one string.
</details>

---

### Question 6

You have a list of test-case dictionaries, each with a `"duration"` key. Which line returns them ordered **slowest first**?

- [ ] A) `sorted(tests, key=lambda t: t["duration"])`
- [ ] B) `sorted(tests, lambda t: t["duration"], reverse=True)`
- [ ] C) `sorted(tests, key=lambda t: return t["duration"], reverse=True)`
- [ ] D) `sorted(tests, key=lambda t: t["duration"], reverse=True)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `key` takes a function that extracts the value to compare, and `reverse=True` puts the largest duration first. A lambda's expression value is returned automatically.
- **Why others are wrong:**
  - A) This is valid but sorts shortest first because `reverse=True` is missing.
  - B) The lambda is passed positionally instead of as `key=`, which causes a `TypeError`.
  - C) A lambda cannot contain `return`; writing it is a SyntaxError.
</details>

---

### Question 7

Which statement best defines a **closure**?

- [ ] A) An inner function that remembers variables from the enclosing scope in which it was created, even after the outer function has finished
- [ ] B) A function that runs automatically when the program ends
- [ ] C) A function written with the `lambda` keyword instead of `def`
- [ ] D) A decorator that takes its own arguments

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** A closure "closes over" variables of its enclosing scope and carries them along. For example, `double = make_multiplier(2)` still knows `factor` is 2 after `make_multiplier` has returned.
- **Why others are wrong:**
  - B) Nothing in closures involves running at program end.
  - C) Being a lambda is about syntax and anonymity; a lambda is not automatically a closure.
  - D) A decorator with arguments uses closures internally, but that is not the definition of one.
</details>

---

### Question 8

You write `@timer` on the line above `def slow_task():`. What is this exactly equivalent to?

- [ ] A) `timer = slow_task(timer)`
- [ ] B) `slow_task = timer()`
- [ ] C) `slow_task = timer(slow_task)`
- [ ] D) `timer(slow_task())`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `@decorator` is syntactic sugar for `func = decorator(func)`: the decorator receives the original function and the name is rebound to the wrapped version.
- **Why others are wrong:**
  - A) This passes the decorator into the function and rebinds the wrong name.
  - B) This calls `timer` with no function, and `@timer` does not do that.
  - D) This would call `slow_task` first and give its result to `timer`, instead of passing the function itself.
</details>

---

### Question 9

In your team's shared test-utility library, a colleague writes `format_duration(seconds)` so that it **prints** `"2m 5s"` instead of returning it. Why is returning the string the better design?

- [ ] A) Functions that print cannot be imported from another module
- [ ] B) Python raises an error whenever a helper function calls `print`
- [ ] C) Returning makes the function run faster than printing
- [ ] D) The caller can decide what to do with the value: show it, put it in a report or file, compare it in an assertion, or pass it to another function

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** A function that only prints can only serve the console, while one that returns can feed reports, files, comparisons and other functions. It is also easy to test: you compare the returned value with the expected one.
- **Why others are wrong:**
  - A) Printing functions can be imported like any other.
  - B) `print` is allowed anywhere; it is just a poor fit for helpers that calculate or format.
  - C) Speed is not the reason; the benefit is reusability and testability.
</details>

---

### Question 10

When Python meets a name inside a function, in which order does it search for it?

- [ ] A) Global, then Local, then Enclosing, then Built-in
- [ ] B) Built-in, then Global, then Enclosing, then Local
- [ ] C) Local, then Enclosing, then Global, then Built-in
- [ ] D) Local, then Global, then Built-in, then Enclosing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The LEGB rule searches the Local scope (the current function) first, then any Enclosing function, then Global (the file), then Built-ins such as `print` and `len`. The first match wins.
- **Why others are wrong:**
  - A) Global is not searched before Local; the current function's own names come first.
  - B) This is the reverse of LEGB; built-ins are the last place Python looks.
  - D) The Enclosing scope is checked right after Local, before Global and Built-in.
</details>

---

### Question 11

A test script contains the following code. What happens when `add_one()` is called?

```python
counter = 0

def add_one():
    counter = counter + 1

add_one()
```

- [ ] A) An `UnboundLocalError`, because the assignment makes `counter` local and its right-hand side has no value yet
- [ ] B) `counter` becomes `1` because functions can change globals freely
- [ ] C) A `NameError`, because `counter` does not exist outside the function
- [ ] D) Nothing happens because the function is never allowed to read `counter`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Python sees an assignment to `counter` inside the function and treats the name as local, so the `counter` on the right-hand side has not been given a value yet. The recommended fix is to pass values in and return results out rather than change globals.
- **Why others are wrong:**
  - B) Assigning inside a function creates a new local variable; it does not change the global.
  - C) `counter` does exist globally; the error is about it being treated as local, and the error type is `UnboundLocalError`.
  - D) Reading a global inside a function is fine; the problem is the assignment.
</details>

---

### Question 12

A login-test script prints the same three banner lines (`"=" * 30`, a title, `"=" * 30`) before each of 20 tests. What is the strongest reason to move them into a `print_banner()` function?

- [ ] A) Python cannot execute the same `print` line more than once in a script
- [ ] B) A change to the banner width or style is then made in one place instead of 20 copies (DRY, "Don't Repeat Yourself")
- [ ] C) Functions make `print` calls produce output faster
- [ ] D) A script is only allowed to contain print statements inside functions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** The DRY principle says to write repeated code once and give it a name. With `print_banner()`, one edit updates every banner and no copy can be missed.
- **Why others are wrong:**
  - A) Python can run the same line any number of times; repetition is just tedious and error-prone.
  - C) Speed is not the benefit; maintainability and readability are.
  - D) Top-level `print` statements are perfectly legal.
</details>

---

### Question 13

Your team's `summarise(results)` helper needs to give back the passed count, the failed count, the total and a few more figures. Why might you return a dictionary such as `{"passed": 3, "failed": 1, "total": 4}` rather than a long tuple?

- [ ] A) Python does not allow a function to return more than three values in a tuple
- [ ] B) A dictionary makes the function run faster than a tuple would
- [ ] C) A tuple cannot be unpacked into separate variables
- [ ] D) Named keys mean the caller does not have to remember the order of the values

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** For many return values, a dictionary with named keys is clearer than a long tuple because the reader does not have to remember the order. `summary["failed"]` explains itself.
- **Why others are wrong:**
  - A) There is no such limit; commas can return any number of values.
  - B) Speed is not the reason; readability is.
  - C) Tuples can be unpacked, as in `p, f = summarise(results)`; unpacking just becomes harder to read when there are many values.
</details>

---

### Question 14

What do `value` and `result` hold after this code runs?

```python
def double(n):
    n = n * 2
    return n

value = 5
result = double(value)
```

- [ ] A) `value` is `5` and `result` is `10`
- [ ] B) `value` is `10` and `result` is `10`
- [ ] C) `value` is `5` and `result` is `None`
- [ ] D) `value` is `10` and `result` is `None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Parameters behave like local variables, so reassigning `n` inside the function does not change the caller's `value`. The doubled number reaches the caller only through `return`.
- **Why others are wrong:**
  - B) Reassigning a parameter does not change the caller's variable.
  - C) The function does contain `return n`, so `result` is `10`, not `None`.
  - D) Both parts are wrong: `value` is unchanged and `result` receives the returned `10`.
</details>

---

### Question 15

A grading helper is written like this. What does `grade(30)` give back?

```python
def grade(score):
    if score >= 50:
        return "PASS"
```

- [ ] A) `"FAIL"`
- [ ] B) `False`
- [ ] C) `None`
- [ ] D) A `NameError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** When a code path finishes without hitting a `return`, Python quietly returns `None`. Scores below 50 skip the only `return`, so the fix is to cover the other case with `return "FAIL"` (or an `else`).
- **Why others are wrong:**
  - A) Python never invents a `"FAIL"` value; you must write it.
  - B) `False` is not the default return value; `None` is.
  - D) No name is missing; the function simply ends without returning anything on that path.
</details>

---

### Question 16

Why is `def add_result(result, results=None):` followed by `if results is None: results = []` the recommended pattern instead of `results=[]`?

- [ ] A) Python forbids lists in a `def` line
- [ ] B) Default values are created once when the function is defined, so `None` plus a fresh list inside gives each call its own list
- [ ] C) `None` is faster to compare with than a list
- [ ] D) A default list is deleted after the first call, so later calls would crash

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** A default is evaluated only once, at definition time, so a `[]` default is shared by every call that omits the argument. Using `None` and creating the list inside the function gives each call a fresh one.
- **Why others are wrong:**
  - A) Python allows it, but it causes the shared-list trap.
  - C) Speed is not the reason; avoiding shared state is.
  - D) The list is not deleted; it persists and keeps growing, which is exactly the bug.
</details>

---

### Question 17

Given `def create_session(username, *, browser="Chrome", headless=False):`, what happens with the call `create_session("alice", "Firefox")`?

- [ ] A) `browser` is set to `"Firefox"`
- [ ] B) `"Firefox"` is ignored and the default browser is used
- [ ] C) A `TypeError`, because the function takes 1 positional argument but 2 were given
- [ ] D) A `SyntaxError`, because the bare `*` is invalid

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** A bare `*` means everything after it must be passed by keyword. `create_session("alice", browser="Firefox")` works, but passing `"Firefox"` positionally raises a `TypeError`. This keeps calls like `headless=True` readable.
- **Why others are wrong:**
  - A) Parameters after the bare `*` cannot be filled by position.
  - B) Python does not silently ignore the extra value; it raises an error.
  - D) A bare `*` is valid syntax; the error occurs when the function is called.
</details>

---

### Question 18

With `def create_user(username, role="viewer", **extra):`, a tester mistypes the option and calls `create_user("bob", rol="admin")`. What is the result?

- [ ] A) A `TypeError` for an unexpected keyword argument `rol`
- [ ] B) The user gets role `"viewer"` and an extra key `rol` with the value `"admin"`; no error is raised
- [ ] C) The user gets role `"admin"` because Python corrects the spelling
- [ ] D) Python prints a warning and ignores `rol`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `**extra` gathers every unrecognised keyword argument into a dictionary, so the typo just becomes a new key. This is the caution about `**kwargs`: it hides which options are valid, so mistakes pass silently.
- **Why others are wrong:**
  - A) A `TypeError` would occur only if the function had no `**extra` to absorb the keyword.
  - C) Python never auto-corrects names.
  - D) No warning is issued and the key is not discarded; it is stored in the dictionary.
</details>

---

### Question 19

You have `numbers = [3, 8, 11]` and a function `def add_all(*numbers):`. Which call passes the three items as three separate arguments?

- [ ] A) `add_all(numbers)`
- [ ] B) `add_all(**numbers)`
- [ ] C) `add_all(numbers*)`
- [ ] D) `add_all(*numbers)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** When calling a function, `*` unpacks a list or tuple into separate positional arguments, so `add_all(*numbers)` means `add_all(3, 8, 11)`.
- **Why others are wrong:**
  - A) This passes the whole list as one single argument.
  - B) `**` unpacks a dictionary into keyword arguments, not a list.
  - C) The star goes before the name; this is not valid syntax.
</details>

---

### Question 20

A QE engineer has a list `words` of test-area names and wants them sorted from shortest to longest with `sorted`. Which call is correct?

- [ ] A) `sorted(words, key=len())`
- [ ] B) `sorted(words, key="len")`
- [ ] C) `sorted(words, key=len)`
- [ ] D) `sorted(words, len)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `key` expects the function itself so that `sorted` can call it on each item. You pass `len` without parentheses; with parentheses you would call it immediately, with no argument.
- **Why others are wrong:**
  - A) `len()` is a call with no argument and fails before sorting starts; pass the function, not its result.
  - B) A string is not a function; `key` needs a callable object.
  - D) `key` is a keyword-only option of `sorted` (`sorted(iterable, *, key=None, reverse=False)`), so it must be written as `key=len`.
</details>

---

### Question 21

A tester writes `print(map(lambda s: s * 1000, durations))` and sees `<map object at 0x...>` instead of the converted values. What is the fix?

- [ ] A) Wrap the call in `list(...)`, because `map` returns a lazy iterator rather than a list
- [ ] B) Add `return` inside the lambda
- [ ] C) Replace the lambda with a named `def`, because `map` rejects lambdas
- [ ] D) Use `filter` instead, since `map` cannot transform numbers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `map` produces a lazy iterator, so printing it shows the object itself. Converting with `list(map(...))` (or looping over it) reveals the results.
- **Why others are wrong:**
  - B) A lambda returns its expression automatically, and writing `return` is a SyntaxError.
  - C) `map` accepts lambdas, named functions and even built-ins such as `int`.
  - D) `filter` keeps items; `map` is the tool that transforms every item.
</details>

---

### Question 22

Which situation calls for a named `def` function rather than a lambda?

- [ ] A) Sorting a list of dictionaries once by a single field
- [ ] B) Keeping only results whose duration is above 1.0 in a single `filter` call
- [ ] C) Finding the slowest test with `max(..., key=...)`
- [ ] D) A rule that needs several statements, a docstring, and reuse in several places

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** A lambda holds one short expression and has no docstring, so logic that needs several statements, documentation or reuse belongs in a `def`. A good test: if you have to think hard to read the lambda, replace it with a named function.
- **Why others are wrong:**
  - A) A single-field sort key used once is the classic lambda use case.
  - B) A one-line filter rule is short and used once, which suits a lambda.
  - C) A `max` key that picks one field is a short inline expression.
</details>

---

### Question 23

A factory function is written as follows. What happens at `hello = make_greeter()`?

```python
def make_greeter():
    def greeter():
        print("Hello!")
    return greeter()

hello = make_greeter()
```

- [ ] A) `Hello!` is printed immediately and `hello` is `None`, because `return greeter()` runs the function and returns its result
- [ ] B) `hello` holds the `greeter` function and `Hello!` is printed only when `hello()` is called
- [ ] C) A `SyntaxError`, because a function cannot return a call
- [ ] D) `Hello!` is printed twice, once by `make_greeter()` and once by `hello`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `return greeter` hands back the function without running it, but `return greeter()` runs it now and returns its result. Because `greeter` prints and returns nothing, `hello` ends up as `None`.
- **Why others are wrong:**
  - B) This describes `return greeter` (no parentheses), which is the version that returns the function.
  - C) Returning a call's result is valid Python; it is just not what a factory function wants.
  - D) `Hello!` is printed once, during `make_greeter()`; `hello` is `None` and cannot be called.
</details>

---

### Question 24

What is the purpose of applying `@wraps(func)` to the `wrapper` inside a decorator?

- [ ] A) It makes the wrapper run faster than the original function
- [ ] B) It copies the original function's name and docstring onto the wrapper, so `add.__name__` stays `"add"` instead of `"wrapper"`
- [ ] C) It lets the decorator accept its own arguments
- [ ] D) It applies the decorator to every function in the module

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** After decoration, the name points at `wrapper`, which breaks debugging, `help()` and documentation. `functools.wraps` preserves the original name and docstring, and it is recommended in every decorator you write.
- **Why others are wrong:**
  - A) It has no effect on speed.
  - C) Decorators that take arguments need an extra outer layer, as in `@repeat(3)`; `@wraps` does not provide that.
  - D) A decorator is applied only where its `@` line is written.
</details>

---

### Question 25

A team's timing decorator is written as shown. After `@timer` is placed on `get_status_code()`, which returns `200`, the line `assert get_status_code() == 200` fails. Why?

```python
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"took {time.perf_counter() - start:.4f}s")
    return wrapper
```

- [ ] A) The missing `@wraps(func)` changes the return value of the function
- [ ] B) A plain decorator must be written as `@timer()` to work
- [ ] C) The wrapper never returns `result`, so the decorated function now returns `None`
- [ ] D) `func` is called with the wrong arguments because of `*args`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The wrapper calls the original function but throws away its result, so every call gives `None`. A wrapper must end with `return result` so the decorated function still behaves as before.
- **Why others are wrong:**
  - A) Without `@wraps`, only the name and docstring are lost; the return value is not affected.
  - B) A plain decorator is written `@timer`; using `@timer()` is a listed mistake.
  - D) `*args, **kwargs` forwards every argument correctly; that is the standard template.
</details>

---

### Question 26

In a pair-programming session you are about to swap driver and navigator roles. Which Git routine does the lesson recommend?

- [ ] A) Nothing special is needed; the new driver just starts typing
- [ ] B) The new driver force-pushes their own copy over the shared branch
- [ ] C) Each partner switches to a personal branch for their turn
- [ ] D) The current driver commits and pushes, and the new driver runs `git pull` before typing a single line

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** The pair shares one repository and branch. At each swap the current driver commits and pushes, and the new driver pulls first, which avoids conflicts.
- **Why others are wrong:**
  - A) Skipping the pull is a listed mistake because it leads to conflicts.
  - B) Force-pushing could overwrite your partner's work; the lesson never suggests it.
  - C) The exercise asks the pair to share one repository and branch, not to split into personal ones.
</details>

---

### Question 27

You save your helper library as `random.py` and also use `import random` inside it for test data. What is the problem with this file name?

- [ ] A) Python refuses to import any file whose name matches a built-in function
- [ ] B) Your module shadows the standard-library `random` module, causing confusing errors
- [ ] C) Git automatically ignores files named after standard-library modules
- [ ] D) Modules must have the same name as the first function they contain

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Naming a module after a standard-library module (`random.py`, `time.py`, `collections.py`) shadows the real one. Use lowercase names with underscores, such as `test_utils.py`, and avoid spaces and hyphens.
- **Why others are wrong:**
  - A) Python does not forbid the name; the trouble is that your file gets imported in place of the real module.
  - C) Git ignores only what you list in `.gitignore`, such as `__pycache__/`.
  - D) There is no such naming rule; the file name (without `.py`) is simply the module name.
</details>

---

### Question 28

A utility is written as follows. Which rewrite removes its hidden dependency, following the lesson's guidance?

```python
THRESHOLD = 90

def passes(rate):
    return rate >= THRESHOLD
```

- [ ] A) Rename `THRESHOLD` to `threshold`
- [ ] B) Add `global THRESHOLD` as the first line of `passes`
- [ ] C) `def passes(rate, threshold=90): return rate >= threshold`
- [ ] D) Add a docstring that mentions `THRESHOLD`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** A reusable function receives what it needs through parameters. With `threshold=90` as a parameter the dependency is visible and adjustable, and the same inputs always give the same outputs, which makes the function predictable and testable.
- **Why others are wrong:**
  - A) Renaming still leaves the function reading a global.
  - B) The `global` keyword is discouraged because modifying or relying on globals makes programs hard to understand and test.
  - D) A docstring documents the dependency but does not remove it.
</details>

---

## Part 2: True/False

### Question 29

**True or False:** `sorted(cases, key=lambda c: c["duration"])` returns a list of the duration numbers, because the key function's results are what end up in the output.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The key function is used only to decide the ordering. `sorted` returns the original items (here, the dictionaries) in the new order.
</details>

---

### Question 30

**True or False:** A variable created inside a function is *local*, so after the function finishes you can still read it from the main program as long as you spell the name correctly.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Local variables exist only while the function runs. Reading one from outside raises `NameError: name '...' is not defined`; to get a value out, return it from the function.
</details>

---

### Question 31

**True or False:** In a data generator, calling `random.seed(42)` before generating values makes the "random" sequence repeatable, which helps you reproduce a test failure that used random data.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Setting the same seed gives the same sequence every run. Logging the seed (or letting the caller pass one in) lets you rerun a failing test with identical data.
</details>

---

### Question 32

**True or False:** With `def add_result(result, results=[]):`, Python creates a fresh empty list for `results` each time the function is called without that argument.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Default values are created **once**, when the function is defined, so every call that omits `results` shares the same list. The fix is to use `results=None` and create the list inside the function.
</details>

---

### Question 33

**True or False:** A script can call `greet()` on its first line, as long as `def greet():` appears somewhere lower down in the same file.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Python reads top to bottom, so a call made before the `def` has been seen raises `NameError: name 'greet' is not defined`. Define first, call after.
</details>

---

### Question 34

**True or False:** After running `value = 5` and `double(value)`, where `def double(n): n = n * 2; return n`, the variable `value` in the main program is `10`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Parameters behave like local variables, so reassigning `n` inside the function does not change the caller's `value`; it stays `5`. The new number only gets out through the returned value.
</details>

---

### Question 35

**True or False:** Adding type hints, as in `def calculate_pass_rate(passed: int, total: int) -> float:`, does not stop Python from running a call that passes strings; the hints help editors and teammates but are not enforced when the program runs.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Python does not enforce type hints at run time. Their value is that editors use them to catch mistakes and teammates can see what is expected at a glance.
</details>

---

### Question 36

**True or False:** Inside `def run_suite(*test_ids):`, the name `test_ids` is a list, so you can call `.append()` on it directly.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `*` gathers the extra positional arguments into a **tuple**, which has no `.append()`. If you need to modify the items, convert with `list(test_ids)` first.
</details>

---

### Question 37

**True or False:** The signature `def demo(a, b=2, *args, c=3, **kwargs):` is valid because the parameter kinds appear in the required order: required, defaults, `*args`, keyword-only, `**kwargs`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is exactly the order the lesson gives. `a` is required, `b` has a default, `*args` collects extras, `c` is keyword-only because it follows `*args`, and `**kwargs` comes last.
</details>

---

### Question 38

**True or False:** If you build several lambdas in a loop with `functions.append(lambda: n)`, each lambda remembers the value `n` had at the moment it was created.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A lambda looks up an outer variable when it is *called*, not when it is created, so all of them see the final value of `n` (for `range(3)`, they all return `2`). Capturing the current value as a default argument, `lambda n=n: n`, is the fix.
</details>

---

### Question 39

**True or False:** A lambda cannot contain any branching at all, so `lambda score: "PASS" if score >= 50 else "FAIL"` is a SyntaxError.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A lambda cannot contain `if` *blocks* (statements), but it can contain the one-line conditional expression `a if condition else b`, because that is a single expression.
</details>

---

### Question 40

**True or False:** In a closure, an inner function can freely read an enclosing variable, so `count += 1` on that variable inside the inner function works without any extra keyword.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Reading is free, but reassigning needs `nonlocal count`. Without it Python treats `count` as a new local variable and raises an `UnboundLocalError`.
</details>

---

### Question 41

**True or False:** When a function is decorated with `@timer` placed above `@log_call`, the `log_call` decorator is applied to the function first, and `timer` wraps the result.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Stacked decorators apply from the bottom up, so this is `make_test_id = timer(log_call(make_test_id))`. When called, the outermost wrapper (`timer`) runs first.
</details>

---

### Question 42

**True or False:** Code placed under `if __name__ == "__main__":` in `test_utils.py` also runs when another file does `import test_utils`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** When the file is imported, `__name__` is the module's name (`"test_utils"`), not `"__main__"`, so the block is skipped. This is what lets one file act as both a library and a script without running demo code on import.
</details>

---

## Part 3: Code Prediction

### Question 43

What is the exact output?

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

- [ ] A) `Begin`, `A start`, `A end`, `B`, `Finish` (one per line)
- [ ] B) `Begin`, `A start`, `B`, `A end`, `Finish` (one per line)
- [ ] C) `A start`, `B`, `A end`, `Begin`, `Finish` (one per line)
- [ ] D) A `NameError`, because `b` is defined after `a`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Both functions are defined before `a()` is called, so `b` exists by then. Execution jumps into `a`, jumps into `b` at the call, returns to `a`, and then returns to the main program.
- **Why others are wrong:**
  - A) This ignores that the call `b()` runs `B` before `A end`.
  - C) Definitions produce no output, and `Begin` prints first.
  - D) `b` only needs to exist when `a()` is *called*, not when `a` is defined.
</details>

---

### Question 44

What does this code print?

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)
y = add_return(2, 3)
print(x, y)
```

- [ ] A) `5` then `5 5`
- [ ] B) `5` then `None 5`
- [ ] C) `None 5`
- [ ] D) `5` then `5 None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `add_print(2, 3)` prints `5` and, having no `return`, hands back `None`, so `x` is `None`. `add_return(2, 3)` prints nothing and returns `5`, so the last line shows `None 5`.
- **Why others are wrong:**
  - A) `x` is `None`, not 5, because `add_print` returns nothing.
  - C) This leaves out the `5` printed during the call `add_print(2, 3)`.
  - D) This swaps the values: `x` is `None` and `y` is `5`.
</details>

---

### Question 45

What is the output?

```python
def add_test(queue, test_id):
    queue.append(test_id)

def with_extra(ids, extra):
    new_list = ids.copy()
    new_list.append(extra)
    return new_list

q = ["TC-001"]
add_test(q, "TC-002")
r = with_extra(q, "TC-003")
print(q)
print(r)
```

- [ ] A) `['TC-001']` then `['TC-001', 'TC-002', 'TC-003']`
- [ ] B) `['TC-001']` then `['TC-001', 'TC-003']`
- [ ] C) `['TC-001', 'TC-002']` then `['TC-001', 'TC-002', 'TC-003']`
- [ ] D) `['TC-001', 'TC-002', 'TC-003']` then `['TC-001', 'TC-002', 'TC-003']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `add_test` mutates the caller's list in place with `append`, so `q` becomes `['TC-001', 'TC-002']`. `with_extra` works on a copy, so `q` is unchanged by it and `r` is the new three-item list.
- **Why others are wrong:**
  - A) This assumes `add_test` did not change `q`, but lists are passed by reference and `append` modifies them.
  - B) This ignores both the in-place change to `q` and that `r` is built from the updated `q`.
  - D) `with_extra` copies the list first, so `q` does not receive `'TC-003'`.
</details>

---

### Question 46

What does this code print?

```python
def add_result(result, results=[]):
    results.append(result)
    return results

first = add_result("PASS")
second = add_result("FAIL")
print(first)
print(second)
print(first is second)
```

- [ ] A) `['PASS']`, `['FAIL']`, `False`
- [ ] B) `['PASS']`, `['PASS', 'FAIL']`, `False`
- [ ] C) `['PASS', 'FAIL']`, `['FAIL']`, `True`
- [ ] D) `['PASS', 'FAIL']`, `['PASS', 'FAIL']`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** The default list is created once and shared by both calls, so `first` and `second` are the very same object. By the time anything is printed it already holds `'PASS'` and `'FAIL'`, and `first is second` is `True`.
- **Why others are wrong:**
  - A) This describes the behaviour with a `None` default, not a `[]` default.
  - B) It forgets that `first` refers to the same list, which was later extended by the second call.
  - C) `first` and `second` are one object, so they show identical contents.
</details>

---

### Question 47

What does this code print?

```python
def create_user(username, role="viewer", **extra):
    user = {"username": username, "role": role}
    user.update(extra)
    return user

config = {"role": "admin", "active": True}
print(create_user("bob", **config))
print(create_user("amy", "tester", locale="en-GB"))
```

- [ ] A) `{'username': 'bob', 'role': 'admin', 'active': True}` then `{'username': 'amy', 'role': 'tester', 'locale': 'en-GB'}`
- [ ] B) `{'username': 'bob', 'role': 'viewer', 'config': {'role': 'admin', 'active': True}}` then `{'username': 'amy', 'role': 'tester', 'locale': 'en-GB'}`
- [ ] C) `{'username': 'bob', 'role': 'admin', 'active': True}` then `{'username': 'amy', 'role': 'viewer', 'tester': 'en-GB'}`
- [ ] D) A `TypeError`, because a dictionary cannot be passed to a function call

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `**config` unpacks the dictionary into `role="admin", active=True`; `role` fills the named parameter and `active` goes into `extra`. In the second call, `"tester"` fills `role` positionally and `locale` lands in `extra`.
- **Why others are wrong:**
  - B) The `**` unpacks the dictionary into keyword arguments; it is not passed as a single value.
  - C) The second positional argument fills `role` (the next parameter), not `extra`.
  - D) `**` is exactly how a dictionary is fed into a call as keyword arguments.
</details>

---

### Question 48

What is printed?

```python
cases = [
    {"id": "TC-A", "priority": 2, "duration": 1.5},
    {"id": "TC-B", "priority": 1, "duration": 0.5},
    {"id": "TC-C", "priority": 2, "duration": 3.0},
    {"id": "TC-D", "priority": 1, "duration": 2.0},
]
ordered = sorted(cases, key=lambda c: (c["priority"], -c["duration"]))
print([c["id"] for c in ordered])
```

- [ ] A) `['TC-B', 'TC-D', 'TC-A', 'TC-C']`
- [ ] B) `['TC-C', 'TC-A', 'TC-D', 'TC-B']`
- [ ] C) `['TC-B', 'TC-D', 'TC-C', 'TC-A']`
- [ ] D) `['TC-D', 'TC-B', 'TC-C', 'TC-A']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** The tuple key sorts by priority ascending, and within the same priority the negated duration puts the longest first. Priority 1 gives `TC-D` (2.0) then `TC-B` (0.5); priority 2 gives `TC-C` (3.0) then `TC-A` (1.5).
- **Why others are wrong:**
  - A) This sorts both fields ascending, with the shortest duration first.
  - B) This sorts by priority descending.
  - C) Priority 1 is right but `TC-B` and `TC-D` are in shortest-first order.
</details>

---

### Question 49

What is the exact output?

```python
from functools import wraps

def tag(label):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"<{label}>")
            result = func(*args, **kwargs)
            print(f"</{label}>")
            return result
        return wrapper
    return decorator

@tag("outer")
@tag("inner")
def check(x):
    print("x =", x)
    return x * 2

print(check(4))
```

- [ ] A) `<inner>`, `<outer>`, `x = 4`, `</outer>`, `</inner>`, `8`
- [ ] B) `<outer>`, `<inner>`, `x = 4`, `</inner>`, `</outer>`, `None`
- [ ] C) `<outer>`, `x = 4`, `</outer>`, `8`
- [ ] D) `<outer>`, `<inner>`, `x = 4`, `</inner>`, `</outer>`, `8`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Decorators apply bottom-up, so `inner` wraps `check` first and `outer` wraps that. On a call the outermost wrapper runs first, giving the nested order shown. Each wrapper returns `result`, so `print` shows `8`.
- **Why others are wrong:**
  - A) This puts the inner wrapper outermost, which reverses the nesting.
  - B) The wrappers return the result, so the final line is `8`, not `None`.
  - C) Both decorators are applied; the `inner` tags are not skipped.
</details>

---

### Question 50

A teammate's validator is shown below. What are the four printed lines?

```python
def is_valid_test_id(test_id, prefix="TC", digits=3):
    start = f"{prefix}-"
    if not test_id.startswith(start):
        return False
    number = test_id[len(start):]
    return number.isdigit() and len(number) == digits

print(is_valid_test_id("TC-007"))
print(is_valid_test_id("TC-7"))
print(is_valid_test_id("API-0042", prefix="API", digits=4))
print(is_valid_test_id("tc-007"))
```

- [ ] A) `True`, `False`, `True`, `False`
- [ ] B) `True`, `False`, `False`, `False`
- [ ] C) `True`, `True`, `True`, `True`
- [ ] D) `True`, `False`, `True`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `"TC-007"` has three digits (True). `"TC-7"` has only one digit (False). With `prefix="API"` and `digits=4`, `"API-0042"` matches (True). `"tc-007"` fails because `startswith` is case-sensitive and the prefix is `"TC-"` (False).
- **Why others are wrong:**
  - B) The third call overrides the defaults, so `"API-0042"` is valid.
  - C) The validator rejects the wrong digit count and the lowercase prefix.
  - D) `startswith("TC-")` is case-sensitive, so `"tc-007"` is rejected.
</details>

---

### Question 51

What is the exact output?

```python
BASE = "prod"

def show():
    BASE = "test"
    print("inside:", BASE)

show()
print("outside:", BASE)
```

- [ ] A) `inside: test`, `outside: test` (one per line)
- [ ] B) `inside: prod`, `outside: prod` (one per line)
- [ ] C) `inside: test`, `outside: prod` (one per line)
- [ ] D) `inside: test`, then a `NameError` for `BASE`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Assigning to `BASE` inside the function creates a new local variable instead of changing the global one. The function prints its local `"test"`, while the global `BASE` stays `"prod"`.
- **Why others are wrong:**
  - A) This assumes the assignment changed the global, but it only created a local variable.
  - B) Inside the function the local `BASE` exists, so `"test"` is printed, not `"prod"`.
  - D) `BASE` still exists globally, so the last line prints normally; no error occurs.
</details>

---

### Question 52

What does this code print?

```python
def summarise(results):
    passed = results.count("PASS")
    return passed, len(results) - passed

outcome = summarise(["PASS", "FAIL", "PASS"])
p, f = outcome
print(outcome)
print(p, f)
print(outcome[1])
```

- [ ] A) `(2, 1)`, then `2 1`, then `2`
- [ ] B) `(2, 1)`, then `2 1`, then `1`
- [ ] C) `[2, 1]`, then `2 1`, then `1`
- [ ] D) A `TypeError`, because a stored tuple cannot be unpacked

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Returning two values with a comma packs them into a tuple, `(2, 1)`. Unpacking it gives `p = 2` and `f = 1`, and `outcome[1]` is the second item, `1`.
- **Why others are wrong:**
  - A) Index `1` is the second item (`1`), not the first (`2`).
  - C) Multiple return values are packed into a tuple, which prints with round brackets, not a list.
  - D) A tuple can be unpacked whether or not it was first stored in a variable.
</details>

---

### Question 53

What are the two printed lines?

```python
def demo(a, b=2, *args, c=3, **kwargs):
    print(f"a={a}, b={b}, args={args}, c={c}, kwargs={kwargs}")

demo(5, 6, 7, c=8, z=9)
demo(5, z=1)
```

- [ ] A) `a=5, b=6, args=(7,), c=8, kwargs={'z': 9}` then `a=5, b=2, args=(), c=3, kwargs={'z': 1}`
- [ ] B) `a=5, b=6, args=[7], c=8, kwargs={'z': 9}` then `a=5, b=2, args=[], c=3, kwargs={'z': 1}`
- [ ] C) `a=5, b=6, args=(7,), c=8, kwargs={}` then `a=5, b=2, args=(), c=3, kwargs={}`
- [ ] D) A `TypeError`, because `z` is not a declared parameter

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** In the first call `5` and `6` fill `a` and `b`, the extra positional `7` goes into the `args` tuple, `c` is set by keyword, and the unknown keyword `z` is collected in `kwargs`. In the second call the defaults apply for `b` and `c`, `args` is an empty tuple, and `z=1` lands in `kwargs`.
- **Why others are wrong:**
  - B) `*args` is always a tuple, never a list.
  - C) The keyword `z` is gathered into `kwargs`; it is not discarded.
  - D) `**kwargs` exists precisely to accept keyword arguments that are not declared parameters.
</details>

---

### Question 54

What is the output of this decorator-with-arguments example?

```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(2)
def ping(host):
    print(f"Pinging {host}")
    return host.upper()

print(ping("a.com"))
print(ping.__name__)
```

- [ ] A) `Pinging a.com`, `Pinging a.com`, `A.COM`, `wrapper`
- [ ] B) `Pinging a.com`, `A.COM`, `ping`
- [ ] C) `Pinging a.com`, `Pinging a.com`, `None`, `ping`
- [ ] D) `Pinging a.com`, `Pinging a.com`, `A.COM`, `ping`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `@repeat(2)` is `ping = repeat(2)(ping)`, so the wrapper calls `ping` twice and returns the last result, `"A.COM"`. Because `@wraps(func)` is used, `ping.__name__` is still `"ping"`.
- **Why others are wrong:**
  - A) The name would be `wrapper` only if `@wraps(func)` were missing; here it is present.
  - B) With `times=2` the function runs twice, so the line is printed twice.
  - C) The wrapper ends with `return result`, so `A.COM` is printed, not `None`.
</details>

---

### Question 55

What does this code print?

```python
durations = [0.5, 1.5, 2.5, 0.2]
slow = list(filter(lambda d: d > 1.0, durations))
in_ms = list(map(lambda d: d * 1000, slow))
print(slow)
print(in_ms)
```

- [ ] A) `[0.5, 0.2]` then `[500.0, 200.0]`
- [ ] B) `[1500.0, 2500.0]` then `[1.5, 2.5]`
- [ ] C) `[1.5, 2.5]` then `[1500.0, 2500.0]`
- [ ] D) `[0.5, 1.5, 2.5, 0.2]` then `[500.0, 1500.0, 2500.0, 200.0]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `filter` keeps the items for which the lambda is true, which are `1.5` and `2.5`. `map` then multiplies each kept item by 1000, giving `[1500.0, 2500.0]`.
- **Why others are wrong:**
  - A) This keeps the items for which the condition is false.
  - B) The two printed lines are swapped; `slow` holds the seconds and `in_ms` holds the converted values.
  - D) `filter` removes the items that are not above `1.0`, so the lists are shorter.
</details>

---

### Question 56

What is printed?

```python
fs = []
for n in range(3):
    fs.append(lambda: n)

gs = []
for n in range(3):
    gs.append(lambda n=n: n)

print(fs[0](), fs[2]())
print(gs[0](), gs[2]())
```

- [ ] A) `2 2` then `0 2`
- [ ] B) `0 2` then `0 2`
- [ ] C) `2 2` then `2 2`
- [ ] D) `0 2` then `2 2`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The lambdas in `fs` look up `n` when they are called, after the loop has finished, so they all see `2`. Writing `lambda n=n: n` captures the current value of `n` as a default argument, so `gs` returns `0` and `2` for the first and last lambdas.
- **Why others are wrong:**
  - B) This would be right only if the first group captured its values, which needs the default-argument trick.
  - C) The second group does capture each value, so it does not show `2 2`.
  - D) This swaps the two behaviours.
</details>

---

### Question 57

What does this code print?

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

a = make_counter()
b = make_counter()
print(a(), a(), b(), a())
```

- [ ] A) `1 2 3 4`
- [ ] B) `1 2 1 3`
- [ ] C) `1 1 1 1`
- [ ] D) `1 2 2 3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Each call to `make_counter()` creates a separate closure with its own private `count`. Counter `a` runs 1, 2, then 3, while counter `b` starts independently at 1.
- **Why others are wrong:**
  - A) This treats both counters as sharing one `count`, but each closure has independent state.
  - C) `nonlocal` lets `increment` update the remembered `count`, so it keeps growing instead of resetting.
  - D) `b` does not continue from `a`'s value; it starts at `1` and does not affect `a`.
</details>

---

### Question 58

What are the four printed lines?

```python
def format_duration(seconds):
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"

print(format_duration(45))
print(format_duration(125))
print(format_duration(3725))
print(format_duration(3600))
```

- [ ] A) `45s`, `2m 5s`, `1h 2m 5s`, `60m 0s`
- [ ] B) `45s`, `2m 5s`, `62m 5s`, `60m 0s`
- [ ] C) `45s`, `2m 5s`, `1h 2m 5s`, `0s`
- [ ] D) `45s`, `2m 5s`, `1h 2m 5s`, `1h 0m 0s`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `divmod(3725, 3600)` gives `(1, 125)` and `divmod(125, 60)` gives `(2, 5)`, so the third result is `1h 2m 5s`. For `3600`, `hours` is `1`, which is true, so the first branch is used and the minutes and seconds are shown as `0m 0s`.
- **Why others are wrong:**
  - A) The `hours` branch is used when `hours` is non-zero, so `3600` is shown as `1h`, not `60m`.
  - B) Hours are split off before minutes, so `3725` is not shown as `62m`.
  - C) `hours` is `1` for `3600`, so the function does not fall through to the final `return`.
</details>

---

## Part 4: Fill-in-the-Blank

### Question 59

A string placed as the first statement in a function body, written with triple quotes, is shown by `help()` and by editors. It is called a ____.

```python
def print_banner():
    """Print a three-line banner used to separate test runs."""
    print("=" * 30)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** docstring

**Explanation:** A docstring documents what the whole function does, unlike a `#` comment, which explains one specific line.
</details>

---

### Question 60

In `double = lambda n: n * 2`, the value of the expression after the colon is sent back automatically, so a lambda never uses the keyword ____ (and writing it causes a SyntaxError).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** return

**Explanation:** A lambda holds a single expression whose value is returned automatically. Statements such as `return`, loops and assignments are not allowed inside it.
</details>

---

### Question 61

Complete the closure so each counter keeps its own running total. The missing keyword lets the inner function **reassign** the enclosing variable.

```python
def make_counter():
    count = 0

    def increment():
        ____ count
        count += 1
        return count

    return increment
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** nonlocal

**Explanation:** An inner function can read an enclosing variable freely, but to reassign it, it must declare it `nonlocal`. Without it, `count += 1` would fail with an `UnboundLocalError`.
</details>

---

### Question 62

To let a utility file work as an importable library **and** as a runnable script, put the demo code under `if ____ == "__main__":`. When the file is imported instead, this built-in variable holds the module's name.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__name__`

**Explanation:** When a file is run directly, `__name__` is `"__main__"` and the block runs. When it is imported, `__name__` is the module's name, so the demo code does not execute on import.
</details>

---

### Question 63

If a function finishes without ever reaching a `return` statement, Python quietly gives back the value ____.

```python
def log_message(message):
    print(f"[LOG] {message}")

result = log_message("Starting")
print(result)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `None`

**Explanation:** A function without `return` hands back `None`, so `print(result)` shows `None`. This is the most common source of the "why did I get `None`?" bug.
</details>

---

### Question 64

When a function writes `return passed, failed`, Python packs the two values into a ____, which the caller can unpack into separate variables.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** tuple

**Explanation:** Returning several values separated by commas produces a tuple, for example `(3, 1)`. Unpacking with `p, f = summarise(results)` splits it back into variables.
</details>

---

### Question 65

Complete the signature so that `browser` and `headless` can only be passed by keyword. The missing symbol is a bare ____ placed after `username`.

```python
def create_session(username, ____, browser="Chrome", headless=False):
    return f"{username} using {browser} (headless={headless})"
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `*`

**Explanation:** A bare `*` in the parameter list means everything after it must be given by keyword, so calls read clearly (`headless=True`) and `create_session("alice", "Firefox")` raises a `TypeError`.
</details>

---

### Question 66

Fill in the safe default that avoids the mutable default argument trap:

```python
def add_result(result, results=____):
    if results is None:
        results = []
    results.append(result)
    return results
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `None`

**Explanation:** Default values are created once at definition time, so a `[]` default would be shared by all calls. With `None` as the default, a fresh list is created inside the function on every call that does not supply one.
</details>

---

### Question 67

To rank a status-count dictionary from highest to lowest count, you sort its `.items()` and use the second element of each `(key, value)` pair. Fill in the index:

```python
counts = {"PASS": 12, "FAIL": 3, "SKIP": 5}
ranking = sorted(counts.items(), key=lambda pair: pair[____], reverse=True)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `1`

**Explanation:** Each item from `.items()` is a `(key, value)` tuple, so index `1` is the count. The result is `[('PASS', 12), ('SKIP', 5), ('FAIL', 3)]`.
</details>

---

### Question 68

`@repeat(3)` placed above `def ping(host):` is shorthand for `ping = ____(3)(ping)`. Fill in the name of the function that is called first with the decorator's argument.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `repeat`

**Explanation:** `repeat(3)` is called first and returns the real decorator, which is then applied to `ping`. This is why a decorator with arguments needs one extra layer.
</details>

---

### Question 69

The decorator that copies the original function's name and docstring onto the wrapper is `functools.____`, used as `@____(func)` above the `wrapper` definition.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `wraps`

**Explanation:** Without `@wraps(func)`, a decorated function reports its name as `wrapper` and loses its docstring. With it, `add.__name__` is still `"add"`.
</details>

---

### Question 70

A QE engineer wants a data generator to produce the same "random" values on every run so a failure can be reproduced. Before generating values, they call `random.____(42)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `seed`

**Explanation:** `random.seed(42)` makes the sequence repeatable: calling it again with the same value restarts the identical sequence. Log the seed used, or let the caller pass one in, so a failing run can be repeated with the same data.
</details>

---

### Question 71

While sketching the structure of a test library, you want empty function bodies that do nothing until you implement them. Fill in the placeholder statement:

```python
def check_login():
    ____          # TODO: implement later
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `pass`

**Explanation:** Python needs something in a function body, and `pass` does nothing. It is handy for planning a program before writing the details.
</details>

---

### Question 72

A quick way to check your own utility functions is the ____ statement: if its condition is `False`, Python raises an `AssertionError`, and if it is `True`, nothing happens.

```python
____ percent(1, 4) == 25.0
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `assert`

**Explanation:** `assert condition` (optionally with a message) stays silent when the condition holds and raises `AssertionError` when it does not. Good checks cover normal values, boundaries, invalid input and empty input.
</details>
