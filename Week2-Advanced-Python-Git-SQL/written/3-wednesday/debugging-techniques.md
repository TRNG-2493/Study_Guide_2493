# Debugging Techniques

## Learning Objectives

By the end of this lesson you will be able to:

- Define a **bug**, a **defect**, a **failure** and **debugging**, and explain the difference between a *syntax error*, a *runtime error* (exception) and a *logic error*.
- Follow a repeatable, scientific **debugging process**: reproduce, isolate, form a hypothesis, test it, fix, and verify.
- **Read a Python traceback** from the bottom up and extract the exception type, message, file, line and call chain.
- Use **print debugging** effectively (and know its limits).
- Use **assertions** as debugging aids to catch bad assumptions early.
- Use Python's built-in interactive debugger, **`pdb`**, including `breakpoint()`, stepping, inspecting variables, the call stack, conditional breakpoints and **post-mortem debugging**.
- Describe how to use the visual debugger in an IDE (VS Code / PyCharm): breakpoints, watches, step over/into/out.
- Apply techniques such as **minimal reproducible examples**, **binary search (divide and conquer)** and **rubber-duck debugging**.
- Debug failing automated tests: tell apart a defect in the product from a defect in the test.

---

## Why This Matters

Writing code is only part of an engineer's job. Studies of professional developers repeatedly find that a very large share of working time goes into *understanding why something does not behave as expected*. For a **Quality Engineer / Test Automation Engineer**, debugging is even more central, because your whole job is to find the gap between expected and actual behaviour, and then work out whether the cause lies in:

1. the **product** (a real defect to report),
2. the **test code** (a bug in your automation),
3. the **test data or environment** (stale data, missing config, a service that is down).

Being able to answer that question quickly, with evidence, separates a junior who says "the test failed" from an engineer who says "the test fails because the `discount` key is missing from the second cart item; the fixture is wrong, not the pricing function."

This lesson fits the weekly epic ("harden your Python with modules, exceptions, files, debugging and unit testing") as the bridge between what you did on Tuesday and what comes next:

- On **Tuesday** you learned exceptions and assertions. Those are the *signals* a program gives when something is wrong. Today you learn how to *read* those signals and *investigate* them.
- Earlier today you learned **scope** and **mutability**: they explain a large share of confusing bugs and give you vocabulary for debugging them.
- Next you will learn **logging** (a permanent, structured form of print debugging) and **unit testing** (a way to keep a bug from ever coming back). Debugging is the first half of that cycle: find the bug now, then protect against it forever.

---

## The Concept

### 1. Vocabulary: bug, defect, failure, debugging

| Term | Meaning |
|---|---|
| **Defect / bug** | A mistake in the code (or data, or configuration), e.g. `- 1` that should not be there |
| **Failure** | The visible wrong behaviour caused by the defect, e.g. "the average prints 89 instead of 90" |
| **Error (exception)** | Python's way of signalling that something went wrong while running |
| **Debugging** | The process of finding the defect behind a failure and fixing it |
| **Root cause** | The *original* reason, not just the line where the crash appeared |

A failure may appear far from its cause. A function may crash on line 40 because a different function on line 5 returned the wrong value. Good debugging is about finding the **root cause**, not silencing the symptom.

### 2. Three families of problems

| Type | When detected | Example | Typical sign |
|---|---|---|---|
| **Syntax error** | Before the program starts running (compile time) | A missing colon: `if x > 1` | `SyntaxError`, `IndentationError`, program does not start |
| **Runtime error** | While running | `int("abc")`, dividing by zero, a missing key | Traceback with an exception name |
| **Logic error** | Never, Python cannot know what you *meant* | `total / len(values) - 1` instead of `total / len(values)` | No error at all, just wrong results |

Logic errors are the hardest because nothing crashes. This is why *automated tests with expected values* exist: they are the way you tell the computer what "correct" means.

### 3. The debugging mindset: a scientific method

Random changes ("let me try this...") waste time and often introduce new bugs. Debug like a scientist:

1. **Reproduce.** Make the failure happen reliably. If you cannot reproduce a bug you cannot know whether you have fixed it. Note exact inputs, data, versions, commands.
2. **Read the evidence.** Read the *whole* error message and traceback before touching code (section 4).
3. **Isolate.** Narrow down where the problem lives (which function? which input? which line?). Section 8 describes how.
4. **Hypothesise.** State a specific, testable guess: "I think `item` has no `discount` key for the second item."
5. **Test the hypothesis.** Check using a print, an assertion or the debugger. Do not change the code yet; first confirm or reject your guess.
6. **Fix the root cause.** Make the smallest sensible change.
7. **Verify.** Re-run the original failing scenario *and* related scenarios. Better still, write a test that fails before the fix and passes after (you will do this in the unit testing lesson).
8. **Reflect.** Why did it happen? Could the same mistake exist elsewhere? Could a better check (validation, assertion) have caught it earlier?

Change **one thing at a time**. If you change three things and the bug disappears, you will not know which change fixed it.

### 4. Reading a traceback

When a Python program stops because of an uncaught exception, it prints a **traceback**: a report of the chain of function calls that led to the error. Consider this program:

```python
# cart.py
def apply_discount(price, percent):
    discount = price * percent / 100
    return price - discount


def cart_total(items):
    total = 0
    for item in items:
        total += apply_discount(item["price"], item["discount"])
    return total


if __name__ == "__main__":
    cart = [
        {"name": "pen", "price": 2.0, "discount": 10},
        {"name": "book", "price": 15.0},          # <-- no "discount" key
    ]
    print(cart_total(cart))
```

Running `python cart.py` prints (paths shortened):

```
Traceback (most recent call last):
  File "cart.py", line 18, in <module>
    print(cart_total(cart))
          ~~~~~~~~~~^^^^^^
  File "cart.py", line 9, in cart_total
    total += apply_discount(item["price"], item["discount"])
                                           ~~~~^^^^^^^^^^^^
KeyError: 'discount'
```

**How to read it: start at the bottom.**

1. **The last line** is the *what*: the exception type (`KeyError`) and the message (`'discount'`, the missing key).
2. **The frame just above it** is the *where*: file `cart.py`, line 9, inside function `cart_total`, and the exact code on that line. Newer Python versions (3.11+) add `~~~~^^^^` markers underneath that point at the part of the line that failed, here `item["discount"]`.
3. **The frames above that** are the *how we got here*: the chain of calls, outermost first. `<module>` means the top level of the script. Here the script called `cart_total(cart)` on line 18, which executed line 9.
4. The crash line is not always the defect. Here the line that raised the error is correct code; the **data** (the second cart item) is the real culprit. A hypothesis follows: "the second dictionary has no `discount` key." Verify with a quick print, an assertion, or the debugger.

Possible root-cause fixes, depending on what the requirement says:

- If a discount is optional, use `item.get("discount", 0)`.
- If a discount is required, the test data or input validation is wrong: raise a clear custom exception when it is missing (you learned how on Tuesday).

#### Common exception types and what they usually mean

| Exception | Typical cause | First thing to check |
|---|---|---|
| `SyntaxError` / `IndentationError` | Typo, missing colon/bracket, mixed tabs and spaces | The line reported *and the one before it* |
| `NameError` | Using a name that does not exist (typo, wrong scope, not imported) | Spelling; scope (previous lesson); the import |
| `UnboundLocalError` | Assigning to a variable inside a function before reading it | `global`/`nonlocal`, or pass it in |
| `TypeError` | Wrong type or wrong number of arguments: `"a" + 1`, `len(5)`, calling a non-callable | `type()` / `repr()` of the values |
| `ValueError` | Right type, wrong value: `int("abc")` | The actual data (`repr` it) |
| `KeyError` | Dict key not found | Which key? Print the dict's `keys()` |
| `IndexError` | List index out of range | `len()` of the list; off-by-one |
| `AttributeError` | Object has no such attribute/method (often `None`) | Is the object `None`? Is the name misspelled? |
| `ModuleNotFoundError` / `ImportError` | Module not installed or wrong name/path | Active virtual environment (Monday), `pip list`, spelling |
| `FileNotFoundError` | Wrong path or working directory | `os.getcwd()`, the full path |
| `ZeroDivisionError` | Dividing by zero | Is a list/denominator empty? |
| `AssertionError` | An `assert` failed | The message, and the values compared |
| `RecursionError` | Function calls itself without stopping | Missing/incorrect base case |

`AttributeError: 'NoneType' object has no attribute 'append'` is extremely common. It nearly always means a function that should have returned an object returned `None` instead (for example `x = my_list.sort()`; see the *Mutability* lesson).

#### Chained exceptions

If an exception is raised while handling another one (or you use `raise ... from ...`, which you saw on Tuesday), Python prints both tracebacks, separated by a line like *"The above exception was the direct cause of the following exception"*. Read from the **top** group to find the original problem and the **bottom** group for the final error that surfaced.

#### Capturing a traceback in your own code

When you catch an exception but still want the details (for a report or a log), use the `traceback` module:

```python
import traceback

try:
    {}["missing"]
except KeyError:
    traceback.print_exc()            # prints the full traceback to the screen
    text = traceback.format_exc()    # or get it as a string, e.g. to log or attach to a report
```

(The *Logging* lesson shows an even more convenient way: `logger.exception(...)`.)

### 5. Technique 1: Print debugging

The simplest technique: temporarily add `print` statements to see the values of variables and the path the code takes.

```python
def average(values):
    total = 0
    for v in values:
        total += v
        print(f"DEBUG v={v!r} total={total!r}")   # temporary
    print(f"DEBUG len={len(values)!r}")           # temporary
    return total / len(values) - 1
```

Tips for useful prints:

- **Label** every value (`total=`), otherwise you will not know which line produced which number.
- Use `!r` (the `repr`) to reveal hidden whitespace and distinguish `'5'` (text) from `5` (number) from `None`.
- Print **types** when unsure: `print(type(x), x)`.
- Mark the entry and exit of functions to confirm they actually run: `print(">> entering cart_total")`.
- Print at the **boundaries**: inputs before a function and outputs after it, to see which side is wrong.
- **Always remove** debug prints afterwards, or convert the valuable ones into proper log statements (next lesson).

Strengths: instant, needs no tools. Weaknesses: you must edit and re-run the program each time you want to see something new; output can be overwhelming; you may forget to remove prints; and it is easy to print the wrong thing. That is why a real debugger is worth learning.

### 6. Technique 2: Assertions as debugging aids

An `assert` states something you *believe must be true*. If it is not, Python stops immediately with an `AssertionError` at the first point where reality differs from your belief, instead of letting bad data travel on and cause a puzzling failure later. You met assertions on Tuesday; here is how they help debug:

```python
# cart4.py
def average(values):
    total = 0
    for v in values:
        total += v
    return total / len(values) - 1

assert average([80, 90, 100]) == 90, f"average wrong: {average([80, 90, 100])}"
```

```
Traceback (most recent call last):
  File "cart4.py", line 7, in <module>
    assert average([80, 90, 100]) == 90, f"average wrong: {average([80, 90, 100])}"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: average wrong: 89.0
```

The message after the comma is printed when the assertion fails. Include the *actual* value so the failure explains itself. Inside functions, assertions document and enforce assumptions such as `assert len(values) > 0, "values must not be empty"`.

Remember (from Tuesday) that assertions are for catching **programmer mistakes** and can be switched off with the `python -O` flag, so they must never be the only protection for validating user input or file data. For that, raise proper exceptions.

### 7. Technique 3: The interactive debugger, `pdb`

A **debugger** lets you pause a running program, look at all its variables, and execute it one line at a time. Python includes one in the standard library: **`pdb`** ("Python DeBugger"). It runs in your terminal, so it works anywhere, even on a remote server or a CI machine where no graphical editor is available.

#### 7.1 Starting the debugger

**Option A: `breakpoint()` (recommended).** Add this call at the line where you want the program to pause. It is built into Python 3.7+.

```python
# cart3.py
def apply_discount(price, percent):
    discount = price * percent / 100
    breakpoint()                      # execution pauses here
    return price - discount

print(apply_discount(15.0, 20))
```

Run it normally (`python cart3.py`) and you will land at a `(Pdb)` prompt.

**Option B: run the whole script under the debugger.**

```
python -m pdb cart.py
```

The program stops at the first line; you then set breakpoints and continue.

**Option C: post-mortem debugging (after a crash).** Run:

```
python -m pdb -c continue cart.py
```

The program runs until it crashes with an uncaught exception, then pdb opens *at the crash site* with all the variables still alive, so you can inspect the state that caused the error.

> **Turning breakpoints off.** `breakpoint()` is controlled by the environment variable `PYTHONBREAKPOINT`. Setting `PYTHONBREAKPOINT=0` makes every `breakpoint()` call do nothing, handy in CI. Still, never commit stray `breakpoint()` calls into shared code.

#### 7.2 A first debugging session

Running `python cart3.py`, you see (path shortened):

```
> cart3.py(3)apply_discount()
-> breakpoint()
(Pdb)
```

The line starting with `>` tells you the file, line number and function where execution is **paused**. The line starting with `->` is the *next line about to run* (it has not run yet). `(Pdb)` is the prompt where you type commands. Let's type some:

```
(Pdb) p price
15.0
(Pdb) p percent
20
(Pdb) n
> cart3.py(4)apply_discount()
-> return price - discount
(Pdb) p discount
3.0
(Pdb) pp locals()
{'discount': 3.0, 'percent': 20, 'price': 15.0}
(Pdb) c
12.0
```

What happened:

- `p price` prints the expression's value. `p` accepts any expression (`p price * 2`, `p len(items)`).
- `n` ("next") ran one line and stopped again.
- `pp locals()` pretty-prints a dictionary of all local variables (you met `locals()` in the scope lesson).
- `c` ("continue") let the program run on; it printed the final answer `12.0`.

#### 7.3 Essential pdb commands

| Command | Full name | What it does |
|---|---|---|
| `h` or `h cmd` | help | List commands, or explain one |
| `l` | list | Show source code around the current line (repeat `l` for more) |
| `ll` | longlist | Show the whole current function |
| `n` | next | Run the current line; **step over** function calls |
| `s` | step | Run the current line; **step into** a function call |
| `r` | return | Run until the current function returns |
| `c` | continue | Run until the next breakpoint (or the end) |
| `unt` | until | Continue until a line greater than the current one (useful to leave loops) |
| `p expr` | print | Print the value of an expression |
| `pp expr` | pretty-print | Print nicely formatted (good for dicts/lists) |
| `a` | args | Show the current function's arguments |
| `w` | where | Show the call stack (how we got here) |
| `u` / `d` | up / down | Move up/down one frame in the call stack to inspect its variables |
| `b` | break | List breakpoints; `b 12` sets one on line 12; `b func` on a function |
| `b 12, cond` | conditional break | Stop at line 12 only when `cond` is true |
| `tbreak 12` | temporary break | A breakpoint that removes itself after one hit |
| `cl n` | clear | Delete breakpoint number `n` |
| `disable n` / `enable n` | | Temporarily switch a breakpoint off/on |
| `!stmt` | execute | Run a Python statement, e.g. `!total = 0` to change a variable and see what happens |
| `display expr` | | Re-print `expr` automatically every time execution stops |
| `interact` | | Open an interactive Python prompt in the current scope (Ctrl-D to return) |
| `q` | quit | Exit the debugger (and stop the program) |

Pressing **Enter** on an empty line repeats the previous command, which is handy when stepping with `n`.

**`n` versus `s`:** if the current line is `result = average(scores)`, `n` runs the *entire* `average` call and stops on the next line of the current function. `s` instead enters `average` and stops on its first line. Use `n` when you trust the called function; use `s` when you suspect it.

#### 7.4 Stepping through a logic bug

Take this program, where the defect is a silent logic error:

```python
# cart2.py
def average(values):
    total = 0
    for v in values:
        total += v
    return total / len(values) - 1

def main():
    scores = [80, 90, 100]
    result = average(scores)
    print("Average:", result)

main()
```

It prints `Average: 89.0`, but the correct answer is `90.0`. There is no exception to read, so we debug. Start the debugger and set a breakpoint on the function:

```
$ python -m pdb cart2.py
> cart2.py(1)<module>()
-> def average(values):
(Pdb) b average
Breakpoint 1 at cart2.py:2
(Pdb) c
> cart2.py(2)average()
-> total = 0
(Pdb) n
> cart2.py(3)average()
-> for v in values:
(Pdb) n
> cart2.py(4)average()
-> total += v
(Pdb) n
> cart2.py(3)average()
-> for v in values:
(Pdb) p total
80
```

After one loop turn `total` is `80`, as expected. Instead of stepping through every iteration we can jump to the return statement:

```
(Pdb) r
--Return--
> cart2.py(5)average()->89.0
-> return total / len(values) - 1
```

The `--Return--` banner shows the function is about to return `89.0` (the `->89.0` part). We can evaluate the pieces of the expression interactively to test our hypothesis:

```
(Pdb) p total
270
(Pdb) p total / len(values)
90.0
(Pdb) p total / len(values) - 1
89.0
```

Hypothesis confirmed: the `- 1` is wrong. The loop and the division were fine; the defect is in the final expression. That is a textbook example of using *evidence* to locate the problem.

#### 7.5 The call stack: `w`, `u`, `d`

Using `w` (where) inside `average` shows the chain: `<module>` -> `main` -> `average`. Typing `u` moves *up* to `main`'s frame, where you can `p scores` to see what `main` passed in, without leaving the debugger. Use `d` to come back down. When a function receives a surprising argument, "go up a frame and see who called me and with what" is a very powerful move.

#### 7.6 Conditional breakpoints: stop only when it matters

Imagine a loop over 10,000 test records where only a few are bad. Stopping on every iteration is hopeless. A **conditional breakpoint** pauses only when a condition is true:

```python
# loop.py
def check(values):
    bad = []
    for i, v in enumerate(values):
        if v < 0:
            bad.append(i)
    return bad

print(check([5, 3, -1, 8, -4]))
```

```
$ python -m pdb loop.py
(Pdb) b 4, v < 0
Breakpoint 1 at loop.py:4
(Pdb) c
> loop.py(4)check()
-> if v < 0:
(Pdb) p i, v
(2, -1)
(Pdb) c
> loop.py(4)check()
-> if v < 0:
(Pdb) p i, v
(4, -4)
(Pdb) c
[2, 4]
```

The debugger skipped the values `5`, `3` and `8` and stopped only when `v < 0` was true.

#### 7.7 Post-mortem debugging

For the earlier `cart.py` crash:

```
$ python -m pdb -c continue cart.py
Traceback (most recent call last):
  ...
KeyError: 'discount'
Uncaught exception. Entering post mortem debugging
Running 'cont' or 'step' will restart the program
> cart.py(9)cart_total()
-> total += apply_discount(item["price"], item["discount"])
(Pdb) p item
{'name': 'book', 'price': 15.0}
```

Instead of guessing, we see the exact object that lacks the key: **the second item**, `{'name': 'book', 'price': 15.0}`. You can also type `import pdb; pdb.pm()` in an interactive Python session after a crash to inspect the last exception.

### 8. Technique 4: Isolating the problem

#### 8.1 Minimal reproducible example (MRE)

Strip away everything that is not needed to trigger the bug until you have the *smallest* piece of code that still fails. Often you will find the cause while shrinking. If you do need to ask a colleague or search online, an MRE is the thing they will ask for. It is also an excellent basis for a unit test later.

```python
# From a 500-line test suite down to this:
cart = [{"name": "book", "price": 15.0}]
cart[0]["discount"]          # KeyError: 'discount'
```

#### 8.2 Binary search ("divide and conquer")

If you have no idea where the problem is: check the state at the *middle* of the process. If the data is already wrong there, the bug is in the first half; otherwise it is in the second half. Repeat on the half that contains the problem. Ten checks can locate a bug among a thousand lines. The same idea works on test data (does it fail with the first half of the rows or the second half?) and on code changes (comment out half of the new code).

#### 8.3 Compare working and failing cases

"It works for user A but fails for user B." What differs between the inputs, data, environment, versions, time? List the differences and test each one. This works especially well for flaky tests: run them 20 times and compare passes with failures.

#### 8.4 Check the obvious first

A surprising share of bugs are mundane. Before deep investigation, ask:

- Is the **correct virtual environment** active, and is the package installed there? (Monday)
- Am I running the **file I think I am running**, from the **directory I think I am in**? Are my edits **saved**?
- Is there a stale `.pyc`, an old copy of the module, or a module named like a standard library one (a file called `random.py` or `logging.py` in your project will shadow the real module!)?
- Did I misspell a name? Is the data text when I expect a number (`"5"` versus `5`)?
- Did the environment, test data or an external service change?

#### 8.5 Rubber-duck debugging

Explain the code, line by line and out loud, to a rubber duck (or a colleague, or a text box). The act of putting what you *expect* each line to do into words often exposes the line where reality differs. It sounds silly and works astonishingly well.

### 9. Technique 5: Using an IDE debugger

Editors such as **Visual Studio Code** (with the Python extension) and **PyCharm** provide a graphical front end to the same ideas as `pdb`:

- **Breakpoint:** click in the left margin (the "gutter") next to a line number; a red dot appears. Run the program in **Debug** mode (not Run).
- **Variables panel:** shows all local and global variables and lets you expand lists/dicts/objects.
- **Watch expressions:** type any expression (`total / len(values)`) and see it re-evaluated every time you stop.
- **Call stack panel:** the same information as `w`, clickable.
- **Stepping buttons:** *Step Over* (like `n`), *Step Into* (like `s`), *Step Out* (like `r`), *Continue* (like `c`).
- **Conditional breakpoints / logpoints:** right-click a breakpoint to set a condition or print a message without editing code.
- **Debugging tests:** most editors can start a *single* test under the debugger, very useful for failing automated tests.

Which to use? The IDE debugger is faster to work with for exploring. `pdb` is available everywhere (servers, containers, CI, remote shells) with no setup. Learn the concepts once (breakpoint, step over, step into, step out, inspect, call stack) and they transfer between tools.

### 10. Debugging test automation specifically

Your day-to-day bugs will be failing tests. Some extra guidance:

1. **Decide whose fault it is.** Test failed -> product defect, test defect, data defect or environment defect? Reproduce manually to find out whether the product really misbehaves.
2. **Rerun in isolation.** If a test passes alone but fails in a suite, suspect **shared state** (global variables, mutable default arguments, data left over by an earlier test): exactly the issues from the scope and mutability lessons.
3. **Read the assertion message.** A good message states expected and actual values. Write yours that way.
4. **Capture evidence.** Save the inputs, outputs, logs and (for UI tests later) screenshots. A failure you cannot reproduce or explain is a lost investment.
5. **Be wary of "fixing" a test by loosening it.** Changing an expected value to make the test pass hides defects. Change a test only when you have *proven* the test was wrong.
6. **Flaky tests are bugs.** Timing assumptions, random data, order dependence, and shared state are typical causes. Do not just rerun until green.

### 11. Common debugging pitfalls

| Pitfall | Better approach |
|---|---|
| Changing code before understanding the error | Read the traceback; form a hypothesis first |
| Changing several things at once | One change, then re-test |
| Ignoring the first (top) error and chasing later ones | Fix the earliest error first; later ones may vanish |
| Catching an exception and doing nothing (`except: pass`) | Catch specific exceptions; log or re-raise (Tuesday) |
| Debugging in the wrong environment/version | Verify interpreter, venv, versions |
| Leaving `print` and `breakpoint()` in committed code | Remove them or use logging |
| Fixing the symptom, not the cause | Ask "why" repeatedly until you reach the root cause |

---

## Code Examples

### Example A: A guided bug hunt, from symptom to fix

A small utility is supposed to return the percentage of passed tests:

```python
# pass_rate.py
def pass_rate(results):
    passed = 0
    for outcome in results:
        if outcome == "pass":
            passed += 1
    return passed / len(results) * 100

print(pass_rate(["pass", "fail", "pass", "pass"]))   # expect 75.0
print(pass_rate(["PASS", "Pass", "pass"]))           # expect 100.0 but...
print(pass_rate([]))
```

Run it:

```
75.0
33.33333333333333
Traceback (most recent call last):
  File "pass_rate.py", line 11, in <module>
    print(pass_rate([]))
          ~~~~~~~~~^^^^
  File "pass_rate.py", line 7, in pass_rate
    return passed / len(results) * 100
           ~~~~~~~^~~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

Two separate problems:

1. **Logic error (no exception).** `33.33...` rather than `100.0`. Hypothesis: the comparison is case-sensitive. Evidence: add `print(repr(outcome))` or break inside the loop and see that `outcome` is `'PASS'` and `'PASS' == 'pass'` is `False`.
2. **Runtime error.** `ZeroDivisionError` for an empty list. Read the traceback bottom-up: `len(results)` is `0`.

Fix the root causes, deciding what the requirements should be (here: an empty list gives `0.0`, and comparison ignores case):

```python
def pass_rate(results):
    if not results:                      # guard: avoid division by zero
        return 0.0
    passed = sum(1 for outcome in results if outcome.lower() == "pass")
    return passed / len(results) * 100

print(pass_rate(["pass", "fail", "pass", "pass"]))   # 75.0
print(pass_rate(["PASS", "Pass", "pass"]))           # 100.0
print(pass_rate([]))                                 # 0.0
```

Note how the debugging process (reproduce, read, hypothesise, verify, fix) was applied to *two different kinds* of defect in one small function. In the unit testing lesson you will turn these three print lines into permanent test cases.

### Example B: Using `breakpoint()` in a loop with a condition

```python
rows = [{"id": 1, "qty": 3}, {"id": 2, "qty": -5}, {"id": 3, "qty": 2}]

for row in rows:
    if row["qty"] < 0:
        breakpoint()          # pause only for the suspicious row
    print(row["id"], row["qty"] * 10)
```

Pausing inside an `if` is the code-level equivalent of a conditional breakpoint. At the `(Pdb)` prompt you can `p row`, `w`, and `c` to continue.

### Example C: A debugging checklist function

```python
import sys

def describe_environment():
    """Print facts that often explain 'works on my machine' problems."""
    print("Python    :", sys.version.split()[0])
    print("Executable:", sys.executable)          # which interpreter / venv is running?
    print("Prefix    :", sys.prefix)              # inside a virtual environment this differs from base_prefix
    print("In venv   :", sys.prefix != sys.base_prefix)
    print("Path[0]   :", sys.path[0])              # where imports are searched first

describe_environment()
```

On Monday you worked with virtual environments; this snippet confirms which one a failing test run is actually using. (Sample output differs per machine.)

---

## Summary / Key Takeaways

- A **bug** is a defect in code or data; a **failure** is its visible effect. Find the **root cause**, not just the crash line.
- Problems come in three flavours: syntax errors (before running), runtime errors (exceptions) and logic errors (silently wrong results).
- Debug **scientifically**: reproduce, read the evidence, isolate, hypothesise, test the hypothesis, fix one thing, verify, and reflect.
- **Read tracebacks from the bottom up**: exception type and message, then the failing line, then the call chain above.
- **Print debugging** is quick but limited: label values, use `!r`, remove prints afterwards.
- **Assertions** catch wrong assumptions at the earliest point, with a helpful message including actual values.
- **`pdb`** (`breakpoint()`, `python -m pdb`, post-mortem) lets you pause, inspect (`p`, `pp`, `a`, `w`, `u`, `d`), step (`n`, `s`, `r`, `c`) and set conditional breakpoints (`b 12, cond`).
- IDE debuggers provide the same capabilities with a graphical interface: breakpoints, watches, step over/into/out, call stack.
- Isolation techniques: minimal reproducible examples, binary search, comparing working vs failing cases, checking the environment, and rubber-duck debugging.
- For failing tests, decide whether the cause is the product, the test, the data or the environment; never loosen a test just to turn it green.
- Next: **Logging** replaces ad-hoc prints with a permanent, controllable record, and **unit testing** turns every fixed bug into a safeguard against its return.

---

## Practice Questions and Mini-Exercises

**Q1.** Read this traceback (bottom-up) and answer: (a) What is the exception type? (b) Which function raised it? (c) Which line number? (d) What is the likely cause?

```
Traceback (most recent call last):
  File "report.py", line 20, in <module>
    summary = build_summary(data)
  File "report.py", line 11, in build_summary
    return names[3].upper()
IndexError: list index out of range
```

**Q2.** Which kind of problem (syntax, runtime or logic) is each? (a) `print("hi"` (b) `average = total * count` when you wanted division (c) `open("missing.txt")` where the file does not exist.

**Q3.** In `pdb`, what is the difference between `n` and `s`? When would you use `s`?

**Q4.** You suspect a loop misbehaves only when `user_id == 4242` in a list of 50,000 users. How do you avoid pressing `c` thousands of times? Give the command or code.

**Q5.** A test passes when run alone and fails when the whole suite runs. List three likely causes related to what you learned earlier today.

**Q6 (hands-on).** Save the following as `bug1.py`. It should print `[2, 4, 6]` but does not. Debug it using (a) print debugging, then (b) `pdb`. Identify and fix the defect.

```python
def double_all(numbers):
    result = []
    for n in numbers:
        result.append(n * 2)
        return result

print(double_all([1, 2, 3]))
```

**Q7 (hands-on).** This function should return the second-largest value, but a call crashes. Run it, read the traceback, state your hypothesis, and fix it so that `second_largest([4])` returns `None`.

```python
def second_largest(values):
    ordered = sorted(values, reverse=True)
    return ordered[1]

print(second_largest([4, 9, 2]))
print(second_largest([4]))
```

**Q8 (hands-on).** Use `python -m pdb -c continue` on a script that crashes, find the offending variable value with `p`, and use `u` to inspect the caller's variables. (Use `cart.py` from this lesson.)

**Q9.** Why is `except Exception: pass` considered harmful for debugging?

**Q10.** Give three "check the obvious" questions you should ask before diving deep into a failing import such as `ModuleNotFoundError: No module named 'requests'`.

### Answers

**A1.** (a) `IndexError`. (b) `build_summary`. (c) Line 11 of `report.py` (the frame closest to the error); the call came from line 20. (d) The list `names` has fewer than four elements, and the code asks for index 3. Check `len(names)` and where `names` is produced (off-by-one or short data).

**A2.** (a) Syntax error (missing closing parenthesis). (b) Logic error (no exception; wrong result). (c) Runtime error (`FileNotFoundError`).

**A3.** `n` runs the current line and stops at the next line in the *same* function (calls are stepped over). `s` steps *into* a called function and stops on its first line. Use `s` when you suspect the called function contains the bug.

**A4.** Use a conditional breakpoint such as `b 12, user_id == 4242` in `pdb` (replace 12 with the line number), or in code: `if user_id == 4242: breakpoint()`. IDEs offer the same in the breakpoint's right-click menu.

**A5.** (1) Shared global state modified by an earlier test (scope lesson). (2) A mutable default argument or a mutable "constant" test-data object that an earlier test altered (mutability lesson). (3) Tests depend on execution order or leftover data/files. (Also possible: a name shadowing a built-in at module level.)

**A6.** The `return result` is indented *inside* the `for` loop, so the function returns after the first element, giving `[2]`. Fix: dedent `return result` to align with `for`. With `pdb`: `b 5`, `c`, `p result` shows `[2]` right before the early return, and `n` shows the function returning instead of looping again.

```python
def double_all(numbers):
    result = []
    for n in numbers:
        result.append(n * 2)
    return result
```

**A7.** `second_largest([4])` raises `IndexError: list index out of range` because `ordered` has one element. Hypothesis: the list is too short. Fix:

```python
def second_largest(values):
    ordered = sorted(set(values), reverse=True)   # set(...) ignores duplicates
    if len(ordered) < 2:
        return None
    return ordered[1]

print(second_largest([4, 9, 2]))   # 4
print(second_largest([4]))         # None
```

(Using `set` is a design choice: it treats duplicates of the maximum as one value. If your requirement differs, say so and test it.)

**A8.** After the crash, `p item` shows `{'name': 'book', 'price': 15.0}`, the dictionary lacking `'discount'`; `u` moves to the caller's frame (`<module>`) where `p cart` shows the full list, confirming the second element is the incomplete one.

**A9.** It swallows the exception and its traceback, so the program continues in a bad state, and you lose the evidence of what and where the failure occurred. Catch specific exceptions and log or re-raise.

**A10.** (1) Is the correct virtual environment active (compare `which python` / `sys.executable`)? (2) Was the package installed *in that environment* (`pip list`)? (3) Is the name spelled correctly (the import name can differ from the pip name) and is there a local file with the same name shadowing it?

---

## Additional Resources

- Python Standard Library, `pdb` (The Python Debugger): https://docs.python.org/3/library/pdb.html
- Python Tutorial, "Errors and Exceptions": https://docs.python.org/3/tutorial/errors.html
- Python Standard Library, `traceback` (print or retrieve a stack traceback): https://docs.python.org/3/library/traceback.html
