# Introduction to Decorators and Closures

## Learning Objectives

By the end of this lesson you will be able to:

- Define a nested (inner) function and explain when it can see variables of the outer function.
- Explain what a **closure** is and how it "remembers" values.
- Use `nonlocal` to update a variable held by a closure.
- Explain what a **decorator** is and what problem it solves.
- Write a simple decorator using a wrapper function and apply it with the `@` syntax.
- Write wrappers that accept any arguments using `*args` and `**kwargs`, and that pass the result through.
- Use `functools.wraps` to preserve a function's name and docstring.
- Build a **timing decorator** and a **logging decorator**, the two classic test-automation examples.
- Write a decorator that takes its own arguments, and stack several decorators.
- Recognise decorators in real test frameworks.

---

## Why This Matters

Imagine you have 30 test helper functions and your manager asks: "Can we log when each one starts and finishes, and measure how long it takes?" The naive approach is to open every function and paste timing and logging code into it. That is repetitive, error-prone, and clutters each function with code unrelated to its real job.

A **decorator** lets you write that extra behaviour **once** and attach it to any function with a single line, leaving the original function untouched. This idea is called a *cross-cutting concern*, behaviour such as timing, logging, retries or permission checks that applies to many functions.

Decorators are everywhere in the Python testing world. When you later write tests with a framework like pytest you will see lines such as `@pytest.fixture` and `@pytest.mark.parametrize`, and those `@` lines are decorators. Today's demo builds a timing decorator, and the exercise includes one in the test-utility library. To understand how decorators work, we first need **closures**, which in turn build on what you learned in the last lesson: functions are values.

> **Note on difficulty.** This is the most abstract topic of the week. It is normal to need to read it twice. Run every example yourself, and use `print` statements to follow the flow. You don't need to be able to *invent* decorators from scratch today, just to understand them, read them and write simple ones.

---

## The Concept

### 1. Quick Recap: Functions Are Values

From the lambda lesson, you know that you can pass a function to another function and store a function in a variable:

```python
def shout(text):
    return text.upper()

action = shout          # no parentheses; just another name for the function
print(action("hi"))     # HI
```

Today we add two more abilities: **defining a function inside a function**, and **returning a function from a function**.

---

### 2. Nested (Inner) Functions

You can define a function inside another function. The inner function exists only while the outer function runs, and it can **see the outer function's variables**.

```python
def outer():
    message = "Hello from outer"

    def inner():
        print(message)          # inner can read outer's variable

    inner()

outer()        # Hello from outer
```

Rules:

- `inner` is **local** to `outer`; you can't call `inner()` from outside.
- `inner` can *read* `message`, a variable of the enclosing function. This is the "E" in the **LEGB** scope rule from the first lesson of the day: **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in.

---

### 3. Returning a Function

Because functions are values, an outer function can **return** the inner one (without calling it):

```python
def make_greeter():
    def greeter():
        print("Hello!")
    return greeter           # return the function itself: no parentheses

hello = make_greeter()       # hello is now the inner function
hello()                      # Hello!
hello()                      # Hello!
```

`make_greeter()` runs once and hands back a new function. We store it as `hello` and call it whenever we like. Be careful to tell apart:

- `return greeter`: hand back the function (not run).
- `return greeter()`: run it now and hand back its result.

---

### 4. Closures: Functions That Remember

Now combine both ideas, and a surprising thing happens:

```python
def make_multiplier(factor):
    def multiply(number):
        return number * factor      # uses 'factor' from the outer function
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(10))      # 20
print(triple(10))      # 30
```

Look carefully. By the time we call `double(10)`, the outer function `make_multiplier` **has already finished**; normally its local variable `factor` would be gone. Yet `double` still knows `factor` is `2`, and `triple` knows its `factor` is `3`.

This is a **closure**: *an inner function that remembers the variables from the enclosing scope in which it was created, even after that scope has ended.* The function "closes over" those variables and carries them along.

```
 make_multiplier(2) ──creates──▶ double   [remembers factor = 2]
 make_multiplier(3) ──creates──▶ triple   [remembers factor = 3]
```

Each call to the outer function creates a **separate** inner function with its **own** remembered values.

#### A testing-flavoured closure: configurable validators

```python
def make_range_checker(minimum, maximum):
    def check(value):
        return minimum <= value <= maximum
    return check

is_valid_port = make_range_checker(1, 65535)
is_valid_percent = make_range_checker(0, 100)

print(is_valid_port(8080))        # True
print(is_valid_port(70000))       # False
print(is_valid_percent(101))      # False
```

One recipe, several specialised checkers. (Using a closure to configure a function in advance is a very common pattern.)

#### A closure that changes its remembered state: `nonlocal`

An inner function can **read** an outer variable freely. To **reassign** it, you must declare it `nonlocal`; otherwise Python creates a new local variable (the same trap as with globals in the first lesson):

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count          # "I mean the count from the enclosing function"
        count += 1
        return count

    return increment

counter_a = make_counter()
counter_b = make_counter()

print(counter_a())    # 1
print(counter_a())    # 2
print(counter_a())    # 3
print(counter_b())    # 1   -> independent state
```

Each counter keeps its own private `count`, without using global variables. This will come in handy for counting how many times a function is called.

---

### 5. Decorators: The Idea

Suppose we have a simple function and want to announce when it runs:

```python
def run_login_test():
    print("Executing login test...")
```

We could edit the function. But what if we want the same announcement for many functions? Let's use what we know: write a function that **takes a function, wraps extra behaviour around it, and returns the new function**.

```python
def announce(func):
    def wrapper():
        print(">>> Starting")
        func()                       # call the original function
        print("<<< Finished")
    return wrapper

def run_login_test():
    print("Executing login test...")

run_login_test = announce(run_login_test)    # replace the name with the wrapped version

run_login_test()
```

```text
>>> Starting
Executing login test...
<<< Finished
```

Let's break that down:

- `announce` is the **decorator**: a function that takes a function (`func`) as input.
- Inside, `wrapper` is a new function that does extra work before and after calling the original `func`. It's a closure: it remembers `func`.
- `announce` returns `wrapper`.
- The line `run_login_test = announce(run_login_test)` swaps the original function for the wrapped one. Anyone calling `run_login_test()` now gets the extra behaviour, and the function's own code is unchanged.

```
   caller ──▶ wrapper ──▶ (before-code) ──▶ original func ──▶ (after-code) ──▶ caller
```

---

### 6. The `@` Syntax

Because that "reassign the name" pattern is so common, Python gives it a shortcut. Place `@decorator_name` on the line directly above the `def`:

```python
@announce
def run_login_test():
    print("Executing login test...")

run_login_test()
```

This is **exactly equivalent** to writing `run_login_test = announce(run_login_test)` after the definition. Nothing more magical than that. The `@` line is "syntactic sugar".

Apply the same decorator to many functions with no repeated code:

```python
@announce
def run_search_test():
    print("Executing search test...")

@announce
def run_checkout_test():
    print("Executing checkout test...")
```

---

### 7. Making Wrappers Work With Any Function

Our `wrapper()` has no parameters, so it can't wrap functions that take arguments or return values:

```python
@announce
def add(a, b):
    return a + b

add(2, 3)      # TypeError: wrapper() takes 0 positional arguments but 2 were given
```

The fix uses the `*args` / `**kwargs` from earlier today: accept anything, and pass everything straight through. And we must **return** the original function's result.

```python
def announce(func):
    def wrapper(*args, **kwargs):
        print(">>> Starting")
        result = func(*args, **kwargs)      # forward all arguments
        print("<<< Finished")
        return result                        # pass the result back
    return wrapper

@announce
def add(a, b):
    return a + b

print(add(2, 3))
```

```text
>>> Starting
<<< Finished
5
```

**This is the standard decorator template.** Memorise its shape:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # code BEFORE
        result = func(*args, **kwargs)
        # code AFTER
        return result
    return wrapper
```

---

### 8. Preserving Function Identity with `functools.wraps`

After decoration, the name of the function is no longer what you expect:

```python
@announce
def add(a, b):
    """Return the sum of a and b."""
    return a + b

print(add.__name__)     # wrapper         <- not 'add'!
print(add.__doc__)      # None            <- docstring lost
```

`add` is now really `wrapper`, which breaks debugging, `help()` and documentation. The standard fix is the **`functools.wraps`** decorator, applied to the wrapper:

```python
from functools import wraps

def announce(func):
    @wraps(func)                           # copy name, docstring, etc. from func
    def wrapper(*args, **kwargs):
        print(">>> Starting")
        result = func(*args, **kwargs)
        print("<<< Finished")
        return result
    return wrapper

@announce
def add(a, b):
    """Return the sum of a and b."""
    return a + b

print(add.__name__)     # add
print(add.__doc__)      # Return the sum of a and b.
```

(Here is a decorator used inside a decorator: `@wraps(func)` is itself a decorator that takes an argument, as we will see in section 11.) **Always include `@wraps(func)` in the decorators you write.**

---

### 9. Classic Example 1: A Timing Decorator

This one is today's demo and a staple of test utilities: measure how long a function takes.

```python
import time
from functools import wraps

def timer(func):
    """Decorator that prints how long the function takes to run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()               # high-resolution clock
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def slow_task(delay):
    """Pretend to do some work."""
    time.sleep(delay)             # pause the program for 'delay' seconds
    return "done"

print(slow_task(0.5))
```

```text
[timer] slow_task took 0.5005 seconds
done
```

(The exact time varies slightly.) How it works:

1. `time.perf_counter()` returns a precise time in seconds; taking it before and after gives the **elapsed** time.
2. `func.__name__` is the original function's name, which is why `@wraps` matters.
3. The wrapper returns the original result so that `slow_task` still behaves like before.

You can now time **any** function by adding `@timer` above it, and remove it by deleting the line. Test suites use this to find slow tests and to enforce "this check must finish within N seconds".

---

### 10. Classic Example 2: A Logging Decorator

Log each call with its arguments and its result:

```python
from functools import wraps

def log_call(func):
    """Decorator that logs calls, arguments and results."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_text = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        print(f"[log] calling {func.__name__}({arg_text})")
        result = func(*args, **kwargs)
        print(f"[log] {func.__name__} returned {result!r}")
        return result
    return wrapper

@log_call
def make_test_id(number, prefix="TC"):
    return f"{prefix}-{number:03d}"

make_test_id(7)
make_test_id(12, prefix="API")
```

```text
[log] calling make_test_id(7)
[log] make_test_id returned 'TC-007'
[log] calling make_test_id(12, prefix='API')
[log] make_test_id returned 'API-012'
```

(The long `arg_text` line uses list comprehensions, which you'll learn properly in a later lesson; it just builds a readable text of the arguments. You can treat it as a given for now and focus on the pattern: print before, call, print after, return the result.)

---

### 11. Classic Example 3: A Call Counter (Using State)

This combines closures and decorators. The wrapper keeps count of calls using a function attribute (a simple way to store state on the wrapper):

```python
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"{func.__name__} has been called {wrapper.calls} time(s)")
        return func(*args, **kwargs)
    wrapper.calls = 0               # attach a counter to the wrapper function
    return wrapper

@count_calls
def say_hello():
    print("Hello!")

say_hello()
say_hello()
print(say_hello.calls)      # 2
```

Functions are objects, so you can attach attributes to them. A `nonlocal` counter, as in section 4, works as well.

---

### 12. Decorators That Take Arguments

What if you want `@repeat(3)` to run a function three times? You need **one more layer**: an outer function that takes the decorator's arguments and *returns the actual decorator*.

```python
from functools import wraps

def repeat(times):                      # layer 1: receives the decorator argument
    def decorator(func):                # layer 2: the real decorator, receives the function
        @wraps(func)
        def wrapper(*args, **kwargs):   # layer 3: the wrapper, receives the call arguments
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def ping(host):
    print(f"Pinging {host}...")

ping("example.com")
```

```text
Pinging example.com...
Pinging example.com...
Pinging example.com...
```

`@repeat(3)` first **calls** `repeat(3)`, which returns `decorator`, and then Python applies `decorator` to `ping`. So the two forms:

```python
@repeat(3)
def ping(host): ...

# is the same as
ping = repeat(3)(ping)
```

Three layers feel heavy at first. The pattern is always: *argument-taking function → decorator → wrapper.* A typical test-automation use is a retry decorator ("retry up to N times"), which also needs error handling that you'll learn later in the program. Another is `@slow_threshold(2.0)` to flag functions slower than a limit:

```python
import time
from functools import wraps

def max_seconds(limit):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed > limit:
                print(f"WARNING: {func.__name__} took {elapsed:.2f}s (limit {limit}s)")
            return result
        return wrapper
    return decorator

@max_seconds(0.1)
def sluggish():
    time.sleep(0.3)

sluggish()        # WARNING: sluggish took 0.30s (limit 0.1s)
```

---

### 13. Stacking Decorators

You can apply several decorators to one function. They are applied from the **bottom up** (the one closest to the function wraps it first):

```python
@timer
@log_call
def make_test_id(number, prefix="TC"):
    return f"{prefix}-{number:03d}"
```

This is equivalent to `make_test_id = timer(log_call(make_test_id))`. When called, the outermost wrapper (`timer`) runs first, then `log_call`'s, then the function itself. The output order follows that nesting.

---

### 14. Where You Will See Decorators

- **Test frameworks:** `@pytest.fixture`, `@pytest.mark.skip`, `@pytest.mark.parametrize(...)`, `@unittest.skip(...)`. When you later write `@pytest.mark.parametrize`, you are using a decorator with arguments.
- **Web frameworks:** `@app.route("/login")`.
- **Built-in decorators:** `@staticmethod`, `@classmethod` and `@property`, which you will meet **tomorrow** in the object-oriented programming lessons. They work on the same principle, applied to methods inside classes.
- **Standard library:** `functools.lru_cache` for caching results, and `functools.wraps` (used today).

---

### 15. Summary of Terms

| Term | Meaning |
|---|---|
| **Nested function** | A function defined inside another function |
| **Closure** | An inner function that remembers variables from its enclosing scope |
| **`nonlocal`** | Lets an inner function reassign an enclosing variable |
| **Decorator** | A function that takes a function and returns a (usually wrapped) function |
| **Wrapper** | The inner function that adds behaviour around the original |
| **`@decorator`** | Shorthand for `func = decorator(func)` |
| **`functools.wraps`** | Keeps the original name and docstring on the wrapper |

---

### 16. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Calling the function when returning it | `return wrapper()` | `return wrapper` |
| Forgetting to return the result in the wrapper | The decorated function gives `None` | `return result` |
| Not accepting arguments in the wrapper | `TypeError` for functions with parameters | `wrapper(*args, **kwargs)` |
| Forgetting `@wraps(func)` | Name becomes `wrapper` | Add `@wraps(func)` |
| Forgetting the parentheses for a decorator with arguments | `@repeat` instead of `@repeat(3)` | Use `@repeat(3)` |
| Using parentheses for a plain decorator | `@timer()` | `@timer` |
| Assigning to a closure variable without `nonlocal` | `UnboundLocalError` | Declare `nonlocal` |
| Forgetting that decorators run at definition time | Decorator code runs when the function is defined | Put per-call behaviour inside the wrapper |
| Over-decorating | Many layers of decorators | Keep it simple and readable |

---

### 17. Practice Activities

1. **Nested.** Write `outer()` containing `inner()`, where `inner` prints a variable defined in `outer`. Call it.
2. **Closure.** Write `make_adder(n)` that returns a function adding `n` to its argument. Create `add5` and `add100` and call them.
3. **Counter.** Write `make_counter()` using `nonlocal`. Create two counters and show their states are independent.
4. **Range checker.** Write `make_range_checker(low, high)` and create validators for HTTP status codes (100 to 599) and for percentages.
5. **First decorator.** Write `announce` (no arguments version) and apply it with `@` to two functions with no parameters.
6. **Generic wrapper.** Rewrite it using `*args` and `**kwargs` and returning the result. Apply it to a function with parameters and a return value, and check the value is not lost.
7. **Wraps.** Show `__name__` and `__doc__` of a decorated function with and without `@wraps`.
8. **Timer.** Write the `timer` decorator and use it on a function that loops 1,000,000 times, and on one that calls `time.sleep(0.2)`. Compare the times.
9. **Logger.** Write a `log_call` decorator and apply it to three of your earlier functions (such as `make_test_id` or `calculate_pass_rate`).
10. **Repeat.** Write `@repeat(n)` and apply it to a function that prints a message.
11. **Threshold.** Write `@max_seconds(limit)` and test it with a fast and a slow function.
12. **Explain.** In your own words, describe what the `@` line does, using the phrase "`func = decorator(func)`". Draw the call flow of a decorated function.
13. **Read the code.** Without running it, predict the output (then verify):
    ```python
    def shout(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).upper()
        return wrapper

    @shout
    def greet(name):
        return f"hello, {name}"

    print(greet("priya"))
    ```

---

## Summary

- A function can be **defined inside another function** and can read the outer function's variables. An outer function can **return** an inner function.
- A **closure** is an inner function that **remembers** the variables of the scope it was created in, even after the outer function has finished. Each call to the outer function creates an independent closure. Use **`nonlocal`** to reassign a remembered variable.
- A **decorator** is a function that takes a function, wraps extra behaviour around it and returns the wrapper. `@decorator` above a `def` is shorthand for `func = decorator(func)`.
- Standard template: `def decorator(func): @wraps(func) def wrapper(*args, **kwargs): ...; result = func(*args, **kwargs); ...; return result; return wrapper`.
- Always use **`@functools.wraps(func)`** and always **return the result**.
- Useful testing decorators: **timing**, **logging**, **call counting**, **time limits**. Decorators with arguments (`@repeat(3)`) need one extra layer.
- Several decorators can be **stacked**; they apply from the bottom up.
- You'll see decorators constantly in test frameworks (`@pytest.fixture`, `@pytest.mark...`) and in tomorrow's `@staticmethod`, `@classmethod` and `@property`.
- Next: put all of today's tools together by **writing reusable utility functions**.

---

## Additional Resources

- Python documentation: Function definitions and decorators: https://docs.python.org/3/reference/compound_stmts.html#function-definitions
- Python documentation: `functools.wraps`: https://docs.python.org/3/library/functools.html#functools.wraps
- Real Python: Primer on Python Decorators: https://realpython.com/primer-on-python-decorators/
