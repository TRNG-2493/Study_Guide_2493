# Scope and Namespaces

## Learning Objectives

By the end of this lesson you will be able to:

- Define what a **namespace** is and explain how Python uses namespaces to keep names from colliding.
- Define **scope** and describe the four scopes Python searches, in order, using the **LEGB rule** (Local, Enclosing, Global, Built-in).
- Predict, before running the code, which variable a given line of Python will use.
- Use the `global` and `nonlocal` keywords correctly, and explain why you should usually avoid `global`.
- Recognise and fix the classic `UnboundLocalError`, accidental shadowing of built-in names, and the "late binding" surprise in loops and lambdas.
- Inspect namespaces at runtime with `globals()`, `locals()`, `dir()` and `vars()`.
- Apply these ideas to everyday test-automation code: shared configuration, counters, helper functions, closures, and why test helpers should avoid hidden global state.

---

## Why This Matters

This week's epic is to **harden your Python**: modules, exceptions, files, debugging and unit testing. On Monday you split code into modules and packages, and on Tuesday you made code safer with exceptions, assertions and context managers. Both of those ideas quietly depend on **scope and namespaces**:

- When you wrote `import utils` on Monday, you created a *name* (`utils`) inside your module's namespace. When two modules each define a function called `load`, Python keeps them apart *because* each module has its own namespace.
- When you wrote `except ValueError as e:` on Tuesday, you created a variable `e`. Whether that variable is visible after the `except` block, and which other `e` it might overwrite, is a scope question.

Why does it matter to a **Quality Engineer / Test Automation Engineer** in particular?

1. **Debugging.** Today's later topics are debugging and logging. A huge share of "impossible" bugs are scope bugs: a variable that is not what you think it is, a name that was silently overwritten, or a value that changes between tests. You cannot debug what you cannot reason about.
2. **Test isolation.** A good automated test must not depend on the result of another test. Global variables that tests share (a "current user", a cached token, a counter) are the number one cause of flaky tests, tests that pass alone but fail in a suite.
3. **Reading other people's code.** Test frameworks, fixtures, decorators and callbacks rely heavily on closures (functions that remember variables from the place they were defined). You will meet these everywhere in the weeks ahead.
4. **Avoiding silent corruption.** Naming a variable `list`, `id`, `input` or `max` can break code that worked a minute ago. Knowing the built-in scope tells you why.

Think of scope as the "visibility rules" of your code. If you understand them, a whole category of confusing errors becomes predictable.

---

## The Concept

### 1. What is a name? What is a namespace?

In Python, a **name** (also called an *identifier* or *variable name*) is a label you attach to an object. When you write:

```python
age = 30
```

Python creates the integer object `30` and then binds the name `age` to it. (We go deeper into this "names are labels, not boxes" idea in the next lesson, *Mutability and memory*.)

A **namespace** is the place where those bindings are stored. You can picture it as a dictionary that maps names to objects:

```
{ "age": 30, "greet": <function greet>, "username": "qa_user" }
```

This is not just an analogy; for the global and class namespaces Python really uses a dictionary, and you can look at it (we will do so below).

**Analogy.** Think of a large office building. Each department (Finance, Engineering, QA) has its own phone directory. There can be a person named "Sam" in Finance and another "Sam" in QA. If you are *in* QA and say "call Sam", everyone assumes you mean QA's Sam. Namespaces are the separate directories; they allow the same name to exist in many places without conflict.

Python has several kinds of namespaces, created at different moments and living for different lengths of time:

| Namespace | Created when | Lives until | Example contents |
|---|---|---|---|
| **Built-in** | The interpreter starts | The interpreter exits | `print`, `len`, `int`, `ValueError`, `True` |
| **Global (module)** | A module is first imported or a script starts | The interpreter exits | Functions, classes, variables you define at the top level of a file |
| **Enclosing** | An outer function is called | That call returns (unless captured by a closure) | Variables of the outer function, seen by an inner function |
| **Local** | A function is called | That call returns | Parameters and variables inside the function |

Two more namespaces exist (class bodies and instance attributes) and we will mention them briefly later.

### 2. What is scope?

A **namespace** is where a name is stored. A **scope** is the *region of the program text* in which a namespace can be reached directly without any prefix. In plain words:

> Scope answers the question: "At this line of code, which names can I use, and which object does each name mean?"

Python decides scope **by where you write the code** (this is called *lexical* or *static* scoping), not by who calls the function. That is important: the scope of a variable is determined by the structure of the source file, not by the order in which functions happen to run.

### 3. The LEGB rule

When Python sees a name such as `total` on a line of code, it searches for it in this order and **stops at the first match**:

1. **L - Local:** the current function (parameters and anything assigned inside).
2. **E - Enclosing:** the function(s) that wrap the current function, from the innermost outward. (Only applies to nested functions.)
3. **G - Global:** the top level of the current module (file).
4. **B - Built-in:** names Python provides everywhere (`print`, `len`, `range`, ...).

If the name is found in none of the four, Python raises `NameError: name 'total' is not defined`.

```
+------------------------------------------------------+
| Built-in      print, len, range, ValueError, ...     |
|  +------------------------------------------------+  |
|  | Global (module)   config, helper functions     |  |
|  |  +------------------------------------------+  |  |
|  |  | Enclosing  (outer function's variables)  |  |  |
|  |  |  +------------------------------------+  |  |  |
|  |  |  | Local   (this function's variables)|  |  |  |
|  |  |  +------------------------------------+  |  |  |
|  |  +------------------------------------------+  |  |
|  +------------------------------------------------+  |
+------------------------------------------------------+
   Search starts in the innermost box and moves outward.
```

#### Walking through the layers with one example

```python
# scope_demo.py
base_url = "https://staging.example.com"        # Global

def build_endpoint(path):                       # 'path' is Local to build_endpoint
    version = "v1"                              # Local

    def with_query(params):                     # 'params' is Local to with_query
        # 'version' is Enclosing (belongs to build_endpoint)
        # 'base_url' is Global
        # 'len' and 'str' are Built-in
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}/{version}/{path}?{query}" if len(params) else f"{base_url}/{version}/{path}"

    return with_query

make = build_endpoint("users")
print(make({"active": "true", "page": 2}))
print(make({}))
```

Output:

```
https://staging.example.com/v1/users?active=true&page=2
https://staging.example.com/v1/users
```

Line-by-line:

- `base_url = ...` at the top level is a **global** variable of the module `scope_demo`.
- `def build_endpoint(path):` defines a function. Its parameter `path` and the variable `version` live in the **local** namespace of each *call* to `build_endpoint`.
- Inside it we define `with_query`. This inner function uses `version` and `path`. They are not local to `with_query`, so Python looks outward and finds them in `build_endpoint`'s namespace: the **enclosing** scope.
- `base_url` is not in `with_query` or `build_endpoint`, so Python continues outward and finds it in the **global** scope.
- `len` is not found anywhere in our code, so Python finds it in the **built-in** scope.
- `make = build_endpoint("users")` returns the inner function. Even though `build_endpoint` has finished running, `make` still remembers `version` and `path`. That remembering is called a **closure**, covered in section 8.

### 4. Local scope

Anything you assign inside a function (including its parameters) is **local** to that function by default.

```python
def calculate_total(prices):
    total = 0
    for price in prices:
        total += price
    return total

print(calculate_total([10, 20, 30]))   # 60
print(total)                           # NameError!
```

The last line fails:

```
NameError: name 'total' is not defined
```

Why? `total` was created when `calculate_total` ran and was thrown away when it returned. The outside world never had a name `total`. This is a *feature*: it means function internals cannot accidentally interfere with the rest of your program.

**Each call gets a fresh local namespace.** If you call a function twice, the two calls do not share locals. This is why a function can safely be called many times (and even recursively).

### 5. Global scope and reading globals

A variable created at the top level of a module (outside any function or class) is a **global** variable. "Global" here really means *module-level*; each file has its own global namespace. A name that is global in `config.py` is not automatically visible in `tests.py` unless you import it.

Functions can **read** a global variable without any special syntax:

```python
BASE_URL = "https://staging.example.com"

def get_login_url():
    return BASE_URL + "/login"       # reads the global

print(get_login_url())
```

Output:

```
https://staging.example.com/login
```

Note the convention: names in `UPPER_CASE` signal "this is a constant; do not change it". Python does not enforce it, but it communicates intent to the next reader.

### 6. Assignment creates a local name: the key rule

Here is the single most important and most confusing rule about scope:

> **If a function assigns to a name *anywhere* in its body, Python treats that name as local to the *whole* function** (unless you declare it `global` or `nonlocal`).

Python decides this when the function is *compiled*, before any line runs. Consider:

```python
x = "global"

def f():
    print(x)        # works: reads the global

f()
```

Output: `global`

Now change it very slightly:

```python
x = "global"

def g():
    print(x)        # <-- error
    x = "local"     # this assignment makes x local for the WHOLE function

g()
```

Output (Python 3.11 and newer):

```
UnboundLocalError: cannot access local variable 'x' where it is not associated with a value
```

(On older versions of Python the message reads `local variable 'x' referenced before assignment`; it is the same error.)

Why does it fail? Because the line `x = "local"` exists in the body, Python marks `x` as a local variable of `g`. So `print(x)` looks for a *local* `x`, finds that it has not been given a value yet, and raises `UnboundLocalError`. It does **not** fall back to the global `x`.

This is the standard "augmented assignment" trap too:

```python
passed = 0

def record_pass():
    passed += 1      # UnboundLocalError: this is passed = passed + 1, and 'passed' is local

record_pass()
```

`passed += 1` means "read `passed`, add one, assign to `passed`". The assignment makes `passed` local, but the read happens before any local value exists. Two ways to fix it:

1. Prefer: **return** the new value and let the caller store it (no hidden state).
2. If you really must change a module-level variable, declare `global passed` inside the function.

### 7. The `global` keyword

`global name` tells Python: "In this function, `name` refers to the module-level variable; assignments should change that one."

```python
tests_run = 0

def run_test(name):
    global tests_run
    tests_run += 1
    print(f"Running {name} (test #{tests_run})")

run_test("login")
run_test("logout")
print("Total:", tests_run)
```

Output:

```
Running login (test #1)
Running logout (test #2)
Total: 2
```

- `global tests_run` has to appear **before** `tests_run` is used in the function.
- Without the declaration, `tests_run += 1` would raise `UnboundLocalError` as shown in section 6.

**When should you use `global`?** Rarely. Global mutable state has real costs:

- **Hidden coupling:** a function's behaviour now depends on something that is not in its parameter list.
- **Hard to test:** one test changes the variable, and the next test sees the changed value. (Flaky test factory.)
- **Hard to debug:** any function in the file might have changed it.

Better alternatives: pass values as parameters, return results, keep state in an object (a class instance), or use a closure (section 8). A module-level *constant* that is never reassigned is perfectly fine.

> **Note: mutating is not the same as rebinding.** If a global is a list or dict, a function can call `results.append(...)` on it **without** the `global` keyword, because it is not assigning to the name; it is changing the object the name points to. `global` is needed only when you want to *rebind* the name to a new object. This distinction is central to the next lesson.

```python
results = []

def add_result(r):
    results.append(r)        # no 'global' needed: we mutate, we do not rebind

add_result("pass")
print(results)               # ['pass']
```

### 8. Enclosing scope, closures and `nonlocal`

When a function is defined inside another function, the inner function can read the outer function's variables (the *enclosing* scope), exactly as in the `build_endpoint` example.

A function that carries its enclosing variables along with it, even after the outer function has returned, is a **closure**. Closures are a neat way to keep a little private state without a global or a class:

```python
def make_counter():
    count = 0                      # lives in make_counter's namespace

    def increment():
        nonlocal count             # refer to the enclosing 'count'
        count += 1
        return count

    return increment

counter_a = make_counter()
counter_b = make_counter()

print(counter_a(), counter_a(), counter_a())   # 1 2 3
print(counter_b())                              # 1
```

Output:

```
1 2 3
1
```

Explained step by step:

1. `make_counter()` runs. A local namespace is created with `count = 0`.
2. It defines `increment` and returns it. Normally `count` would vanish when `make_counter` finishes, but `increment` references it, so Python keeps it alive inside the function object (a "cell").
3. `counter_a` and `counter_b` are two independent closures; each has its **own** `count`. That is why `counter_b()` prints `1`.
4. `nonlocal count` tells Python that `count += 1` should rebind the **enclosing** variable instead of creating a new local. Without it you would get `UnboundLocalError`, for the same reason as the global case.

`nonlocal` vs `global`:

| Keyword | Refers to | Must already exist? |
|---|---|---|
| `global x` | The module-level `x` | No (it will be created on assignment) |
| `nonlocal x` | `x` in the nearest enclosing *function* | **Yes**; otherwise `SyntaxError: no binding for nonlocal 'x' found` |

### 9. Built-in scope and the danger of shadowing

The built-in scope holds the names Python provides: `print`, `len`, `list`, `dict`, `str`, `sum`, `max`, `min`, `id`, `type`, `input`, `open`, `range`, and all the standard exception names. You can see them:

```python
import builtins
print(len(dir(builtins)) > 100)   # True
print(builtins.len is len)        # True
```

Because LEGB searches Local, Enclosing and Global *before* Built-in, any variable you create with the same name **hides** (shadows) the built-in:

```python
list = [1, 2]            # oops: shadows the built-in 'list' in this module
list((1, 2))             # TypeError: 'list' object is not callable
```

Output:

```
TypeError: 'list' object is not callable
```

The built-in `list` has not been destroyed; your global name is just found first. You can restore normal behaviour by deleting your variable:

```python
del list                 # removes the global; lookup falls through to the built-in again
print(list((1, 2)))      # [1, 2]
```

Common accidental shadowing seen in test code, and sensible replacements:

| Avoid | Prefer |
|---|---|
| `list`, `dict`, `set`, `str` | `items`, `mapping`, `unique_ids`, `text` |
| `id` | `user_id`, `order_id` |
| `type` | `kind`, `test_type` |
| `input`, `max`, `min`, `sum` | `raw_input`, `max_value`, `lowest`, `total` |
| `file` / `open` | `file_path`, `fh` |

A good linter (we will use these later in the programme) warns about this; for now, make it a habit to choose descriptive names.

### 10. Inspecting namespaces at runtime

Because namespaces are real objects, you can look at them. This is a great debugging trick.

```python
def show_locals():
    a = 1
    b = 2
    return locals()

print(show_locals())               # {'a': 1, 'b': 2}
print(__name__)                    # __main__  (when run as a script)
print("show_locals" in globals())  # True
```

| Function | What it returns |
|---|---|
| `globals()` | A dictionary of the current module's global namespace |
| `locals()` | A dictionary of the current local namespace (inside a function: its local variables) |
| `dir(obj)` | A sorted list of names available on an object; with no argument, the names in the current scope |
| `vars(obj)` | The `__dict__` (attribute dictionary) of an object |

Use `locals()` for **reading** while debugging. Do not try to assign into the dictionary it returns inside a function; that does not change the real variables.

### 11. Scope of loop variables, comprehensions, and `except ... as`

**Loops do not create a new scope.** A variable used by a `for` loop is an ordinary variable of the surrounding function or module and it survives after the loop ends:

```python
for k in range(3):
    pass
print(k)       # 2  (the last value is still there)
```

This can hide bugs: if the loop body never runs (empty list), the variable would never exist and a later use raises `NameError`.

**Comprehensions do create their own scope.** Their loop variable does not leak:

```python
squares = [n * n for n in range(3)]
print(squares)       # [0, 1, 4]
print(n)             # NameError: name 'n' is not defined
```

**`except ... as e`:** the name `e` is *deleted* automatically at the end of the `except` block (Python does this to avoid reference cycles). If you need the exception afterward, copy it to another variable:

```python
try:
    int("abc")
except ValueError as e:
    saved = e          # keep it
print(saved)           # invalid literal for int() with base 10: 'abc'
# print(e)             # would raise NameError
```

**Blocks like `if` and `with` do not create a scope either.** Only functions, lambdas, comprehensions/generators, classes and modules do.

### 12. Late binding: a famous closure surprise

A closure remembers the *variable*, not the *value at the time the function was created*. Look at this:

```python
checks = [lambda: i for i in range(3)]
print([check() for check in checks])    # [2, 2, 2]  <-- not [0, 1, 2]!
```

All three lambdas refer to the **same** variable `i`. By the time you call them, the loop is finished and `i` is `2`. The fix is to capture the current value as a default argument (defaults are evaluated immediately, at definition time):

```python
checks = [lambda i=i: i for i in range(3)]
print([check() for check in checks])    # [0, 1, 2]
```

Test-automation example: generating a callback per test-case in a loop. If you forget this rule, every callback checks the *last* test-case. (`functools.partial` is another common fix.)

### 13. Classes and modules: a brief note

- **Module namespace.** Every `.py` file has its own global namespace. `import helpers` binds the name `helpers` in your namespace; `helpers.fn` looks inside that module's namespace using attribute access. This is the reason two modules can both define `load()`, which is exactly what you saw on Monday. `from helpers import fn` copies the *binding* of `fn` into your namespace.
- **Class namespace.** The body of a class has its own namespace, but methods **cannot** see class-level names as bare variables; they must use `self.name` or `ClassName.name`. This is an exception to LEGB: class bodies are skipped when searching for enclosing scopes.
- **`if __name__ == "__main__":`** works because when you run a file directly, Python sets the module's global `__name__` to the string `"__main__"`; when imported, it is the module's name instead. You saw this idea when you built importable modules.

---

## Code Examples

### Example A: Why test helpers should not rely on hidden global state

A tiny test-utility that keeps a "current user" in a global variable:

```python
# fragile_helpers.py
current_user = None            # shared by every test that imports this module

def login(username):
    global current_user
    current_user = username

def greet_banner():
    return f"Welcome, {current_user}!"

# Imagine two tests running one after another:
login("alice")
print(greet_banner())          # Welcome, alice!

# A later test forgets to log in:
print(greet_banner())          # Welcome, alice!   <-- stale state from the earlier test
```

The second call returns data left over by the first test. In a large suite this produces tests that pass or fail depending on *order*.

A more robust version keeps state in an object, so each test makes its own:

```python
# robust_helpers.py
class Session:
    def __init__(self):
        self.current_user = None

    def login(self, username):
        self.current_user = username

    def greet_banner(self):
        return f"Welcome, {self.current_user}!"

s1 = Session()
s1.login("alice")
print(s1.greet_banner())       # Welcome, alice!

s2 = Session()                 # a brand-new test starts with a clean slate
print(s2.greet_banner())       # Welcome, None!
```

Explanation: `Session` bundles the state and the behaviour. There is no module-level variable to leak, and each `Session` instance has its own namespace (`self.__dict__`). Later in this programme, test fixtures give you this isolation automatically, and you will see why they exist.

### Example B: Counting results with a closure

```python
def make_result_tracker():
    results = {"passed": 0, "failed": 0}

    def record(ok):
        key = "passed" if ok else "failed"
        results[key] += 1                  # mutation: no 'nonlocal' required
        return dict(results)               # return a copy so callers cannot alter our state

    return record

tracker = make_result_tracker()
tracker(True)
tracker(True)
print(tracker(False))                      # {'passed': 2, 'failed': 1}
```

Explanation:

- `results` is created once per `make_result_tracker()` call and stays alive inside the closure.
- `results[key] += 1` changes the dictionary's *contents*; it does not rebind the name `results`, so `nonlocal` is not needed. (If we wrote `results = {...}` inside `record`, we *would* need `nonlocal`.)
- Returning `dict(results)` hands out a copy, protecting the internal state.

### Example C: Spot the shadowing bug

```python
def average(numbers):
    sum = 0                       # shadows built-in sum, but only locally
    for n in numbers:
        sum += n
    return sum / len(numbers)

print(average([2, 4, 6]))         # 4.0  (works, but is poor style)
```

This works because the shadowing is *local*. The harm appears when someone later edits the function and tries to call `sum(numbers)`:

```python
def average_v2(numbers):
    sum = 0
    sum = sum(numbers)            # TypeError: 'int' object is not callable
    return sum / len(numbers)
```

Rename the variable to `total` and the problem cannot occur.

### Example D: Inspecting scope while debugging

```python
API_TIMEOUT = 30

def fetch(path, retries=3):
    attempt = 1
    print("locals :", locals())
    print("timeout:", API_TIMEOUT, "| in globals?", "API_TIMEOUT" in globals())

fetch("/health")
```

Output:

```
locals : {'path': '/health', 'retries': 3, 'attempt': 1}
timeout: 30 | in globals? True
```

When you cannot understand why a variable has a given value, printing `locals()` shows everything available to the function.

---

## Summary / Key Takeaways

- A **namespace** maps names to objects; a **scope** is the region of code where a namespace is directly accessible.
- Python looks up names by **LEGB**: Local, Enclosing, Global, Built-in, and stops at the first match. Not found anywhere means `NameError`.
- Scope is decided by **where code is written** (lexical), not by who calls it.
- **Assigning** to a name inside a function makes it local to that whole function. That is why reading a global and then assigning to it in the same function raises `UnboundLocalError`.
- Use `global` to rebind a module-level name and `nonlocal` to rebind an enclosing function's name. Prefer parameters, return values and objects to global mutable state.
- Mutating (e.g. `list.append`) is not rebinding, so it needs neither keyword.
- Never name variables after built-ins (`list`, `id`, `type`, `sum`...). Shadowing silently breaks later code.
- Loops, `if` and `with` do **not** create scopes; functions, lambdas, comprehensions, classes and modules do.
- Closures capture variables, not values; use default arguments (`lambda i=i: ...`) to freeze a value.
- `globals()`, `locals()`, `dir()` and `vars()` let you inspect namespaces while debugging.
- For test code: hidden global state creates flaky, order-dependent tests. Keep state explicit.

---

## Practice Questions and Mini-Exercises

Try each one before reading the answer. Where code is shown, predict the output first, then run it.

**Q1.** What does this print?

```python
value = 10

def change():
    value = 20

change()
print(value)
```

**Q2.** Why does the following raise an error, and give two different ways to fix it?

```python
attempts = 0

def retry():
    attempts += 1
    return attempts

retry()
```

**Q3.** Which scope (L, E, G or B) does each name belong to on the marked lines?

```python
limit = 5

def outer():
    prefix = "test_"
    def inner(name):
        return prefix + name.upper() + str(limit)   # prefix? name? limit? str? upper?
    return inner
```

**Q4.** What is printed?

```python
funcs = []
for n in range(3):
    funcs.append(lambda: n * 10)
print([f() for f in funcs])
```

Then change one line so it prints `[0, 10, 20]`.

**Q5.** A teammate wrote `input = "admin"` at the top of a test file and later `input("Press Enter")` fails. Explain what happened and the fix.

**Q6 (mini-exercise).** Write `make_logger_prefix(prefix)` that returns a function `log(message)` which returns `prefix + ": " + message`. Show that two loggers with different prefixes do not interfere. Which scope does `prefix` live in when `log` runs?

**Q7 (mini-exercise).** Write a `make_call_limiter(max_calls)` function that returns a function `call()`. It returns `True` for the first `max_calls` calls and `False` afterwards. Use `nonlocal`.

**Q8.** True or false: after `for i in []: pass`, `print(i)` prints `None`. Explain.

### Answers

**A1.** `10`. Inside `change`, `value = 20` creates a new *local* variable. The global `value` is untouched.

**A2.** `attempts += 1` means `attempts = attempts + 1`; the assignment makes `attempts` local, but it has no value yet, so `UnboundLocalError`. Fix 1: add `global attempts` as the first line of `retry`. Fix 2 (preferred): pass the value in and return the new one: `def retry(attempts): return attempts + 1`, then `attempts = retry(attempts)`.

**A3.** `prefix` is **E** (enclosing, from `outer`). `name` is **L** (parameter of `inner`). `limit` is **G**. `str` is **B**. `upper` is not a variable lookup at all: it is an attribute of the string object found via `name.upper`.

**A4.** `[20, 20, 20]` (late binding; all lambdas see the final `n` which is `2`). Fix: `funcs.append(lambda n=n: n * 10)`.

**A5.** The global assignment `input = "admin"` shadows the built-in `input` function. `input("Press Enter")` then tries to call a string: `TypeError: 'str' object is not callable`. Rename the variable (e.g. `role_input` or `username`) or `del input`.

**A6.**

```python
def make_logger_prefix(prefix):
    def log(message):
        return prefix + ": " + message
    return log

api_log = make_logger_prefix("API")
db_log = make_logger_prefix("DB")
print(api_log("started"))   # API: started
print(db_log("started"))    # DB: started
```

`prefix` is in the **enclosing** scope of `log`. Each call to `make_logger_prefix` creates its own enclosing namespace, so the loggers are independent.

**A7.**

```python
def make_call_limiter(max_calls):
    used = 0
    def call():
        nonlocal used
        if used < max_calls:
            used += 1
            return True
        return False
    return call

limiter = make_call_limiter(2)
print(limiter(), limiter(), limiter())   # True True False
```

**A8.** False. The loop body never ran, so `i` was never bound. `print(i)` raises `NameError: name 'i' is not defined`.

---

## Additional Resources

- Python Tutorial, "Python Scopes and Namespaces": https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces
- Python Language Reference, "Naming and binding": https://docs.python.org/3/reference/executionmodel.html#naming-and-binding
- Python Reference, the `global` and `nonlocal` statements: https://docs.python.org/3/reference/simple_stmts.html#the-global-statement
