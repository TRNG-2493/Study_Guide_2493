# Lambda Functions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a lambda function is and how it relates to a regular `def` function.
- Write lambda expressions with zero, one or several parameters, and with conditional logic.
- Understand that functions are values that can be stored in variables and passed to other functions.
- Use lambdas as the `key` for `sorted()`, `.sort()`, `min()` and `max()`.
- Use lambdas with `map()` and `filter()`.
- Sort lists of dictionaries and tuples by a field using a lambda.
- Decide when to use a lambda and when a named `def` function is the better choice.
- Avoid common lambda mistakes.

---

## Why This Matters

Yesterday you sorted simple lists, and you ran into a limitation. How do you sort a list of **test-case dictionaries** by priority, or by duration? Python's `sorted` can do it, but it needs to be told *what to compare*:

```python
sorted(test_cases, key=???)
```

You *could* write a small `def` function for that rule, but a one-line job doesn't deserve four lines and a name you'll never use again. A **lambda** is a tiny, unnamed function written inline right where it is needed. In the demo you will use "lambda sorting" to order test results, and in test code you'll constantly meet short throw-away rules: "sort by duration, longest first", "keep only failures", "pick the slowest test".

The lesson also introduces a powerful idea that you will need again in the next lesson on decorators: **functions are objects** that can be passed around like any other value.

---

## The Concept

### 1. Functions Are Values

Before lambdas, one important idea. In Python, a function is an *object*, like a number or a string. You can:

- store it in a variable,
- put it in a list or dictionary,
- pass it as an argument to another function,
- return it from a function.

```python
def shout(text):
    return text.upper() + "!"

say = shout                 # no parentheses: we copy the function, we don't call it
print(say("hello"))         # HELLO!
print(shout)                # <function shout at 0x...>
```

Recall from the first lesson: `shout` (no parentheses) *refers* to the function; `shout("hi")` *calls* it.

Passing a function to another function:

```python
def apply_twice(func, value):
    return func(func(value))

def add_ten(n):
    return n + 10

print(apply_twice(add_ten, 5))     # 25   (5 -> 15 -> 25)
```

`apply_twice` doesn't know or care *which* function it receives; it just calls it. This pattern, handing a function to another function so it can decide what to do, is the key to `sorted(key=...)`, `map`, `filter`, and decorators.

---

### 2. What Is a Lambda?

A **lambda** is a small **anonymous function** (one with no name) defined in a single expression.

Syntax:

```python
lambda parameters: expression
```

- `lambda` is the keyword.
- `parameters` is a comma-separated list, just like in `def` (it can be empty).
- After the colon is **one expression**. Its value is automatically **returned**. You don't write `return`.

Compare a `def` function with the equivalent lambda:

```python
def double(n):
    return n * 2

double_lambda = lambda n: n * 2

print(double(5))            # 10
print(double_lambda(5))     # 10
```

The two behave the same. More lambda examples:

```python
add = lambda a, b: a + b
print(add(3, 4))                      # 7

greet = lambda: "Hello"               # no parameters
print(greet())                        # Hello

is_even = lambda n: n % 2 == 0
print(is_even(10))                    # True

first_char = lambda text: text[0]
print(first_char("TC-001"))           # T
```

You can even call a lambda immediately (rarely useful):

```python
print((lambda x: x * x)(6))           # 36
```

#### Defaults and keywords work too

```python
power = lambda base, exp=2: base ** exp
print(power(5))         # 25
print(power(2, 10))     # 1024
```

#### Conditional expressions inside lambdas

A lambda can only contain **one expression**: no statements such as `if` blocks, loops, assignments or `return`. But you can use the one-line conditional expression you learned on Tuesday:

```python
grade = lambda score: "PASS" if score >= 50 else "FAIL"
print(grade(72))       # PASS
print(grade(30))       # FAIL
```

#### A note on naming lambdas

Assigning a lambda to a variable, as above (`double_lambda = lambda n: ...`), is fine for learning, but **style guides recommend a normal `def` when you want a named function**. The real strength of lambdas is **inline use**, where you pass them straight into another function without naming them. That is what the rest of this lesson is about.

---

### 3. Lambdas as Sort Keys

`sorted()`, `.sort()`, `min()` and `max()` accept a `key` argument: a function that is called on **each item** to produce the value used for comparison.

#### 3.1 Sorting simple values

```python
words = ["login", "API", "search", "UI"]

print(sorted(words, key=len))                      # ['UI', 'API', 'login', 'search']
print(sorted(words, key=lambda w: w.lower()))      # ['API', 'login', 'search', 'UI']
print(sorted(words, key=lambda w: w[-1]))          # sorted by last letter
```

The lambda receives each word and returns the thing to sort *by*. The items themselves are unchanged in the output; only the ordering uses the key.

#### 3.2 Sorting a list of tuples

```python
results = [("TC-003", 2.5), ("TC-001", 0.8), ("TC-002", 1.7)]

by_time = sorted(results, key=lambda r: r[1])           # by duration (index 1)
print(by_time)
# [('TC-001', 0.8), ('TC-002', 1.7), ('TC-003', 2.5)]

slowest_first = sorted(results, key=lambda r: r[1], reverse=True)
print(slowest_first[0])         # ('TC-003', 2.5)
```

#### 3.3 Sorting a list of dictionaries (the most common use)

```python
test_cases = [
    {"id": "TC-001", "title": "Valid login",     "priority": 1, "duration": 1.2},
    {"id": "TC-002", "title": "Search",          "priority": 3, "duration": 0.7},
    {"id": "TC-003", "title": "Checkout",        "priority": 2, "duration": 4.1},
    {"id": "TC-004", "title": "Logout",          "priority": 1, "duration": 0.4},
]

# By duration, shortest first
by_duration = sorted(test_cases, key=lambda case: case["duration"])
for case in by_duration:
    print(f"{case['id']}  {case['duration']}s")
```

```text
TC-004  0.4s
TC-002  0.7s
TC-001  1.2s
TC-003  4.1s
```

Sorting **in place** with `.sort()` works the same way:

```python
test_cases.sort(key=lambda case: case["priority"])
```

#### 3.4 Sorting by more than one field

Return a **tuple**; Python compares tuples element by element, so the second item breaks ties in the first:

```python
by_priority_then_time = sorted(test_cases, key=lambda c: (c["priority"], c["duration"]))

for case in by_priority_then_time:
    print(case["id"], case["priority"], case["duration"])
```

```text
TC-004 1 0.4
TC-001 1 1.2
TC-003 2 4.1
TC-002 3 0.7
```

To sort one field ascending and another descending, negate a **number**: `key=lambda c: (c["priority"], -c["duration"])` sorts priority up and, within a priority, longest duration first.

#### 3.5 Dictionaries: sorting by value

Yesterday you counted statuses with a dictionary. How do you rank the entries by count? Sort the `.items()` (which are `(key, value)` tuples):

```python
counts = {"PASS": 12, "FAIL": 3, "SKIP": 5}

ranking = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
print(ranking)        # [('PASS', 12), ('SKIP', 5), ('FAIL', 3)]
```

#### 3.6 `min()` and `max()` with a key

```python
slowest = max(test_cases, key=lambda c: c["duration"])
fastest = min(test_cases, key=lambda c: c["duration"])

print(f"Slowest: {slowest['id']} ({slowest['duration']}s)")      # Slowest: TC-003 (4.1s)
print(f"Fastest: {fastest['id']} ({fastest['duration']}s)")      # Fastest: TC-004 (0.4s)
```

No loops needed to find "the test with the longest duration".

---

### 4. `map()`: Transform Every Item

`map(function, collection)` applies a function to **every item** and produces the results. Wrap in `list()` to see them:

```python
durations = [1.2, 0.7, 4.1]

in_ms = list(map(lambda s: s * 1000, durations))
print(in_ms)       # [1200.0, 700.0, 4100.0]

ids = ["tc-001", "tc-002"]
print(list(map(lambda text: text.upper(), ids)))      # ['TC-001', 'TC-002']
print(list(map(str.upper, ids)))                       # same, using an existing method
print(list(map(int, ["10", "20", "30"])))              # [10, 20, 30] -> built-ins work too
```

`map` returns a lazy iterator rather than a list, so you convert it with `list(...)` or loop over it directly.

With several collections, the lambda takes several parameters:

```python
passed = [8, 5]
total = [10, 10]
rates = list(map(lambda p, t: p / t * 100, passed, total))
print(rates)       # [80.0, 50.0]
```

---

### 5. `filter()`: Keep Only Some Items

`filter(function, collection)` keeps the items for which the function returns a **true** value.

```python
numbers = [3, 8, 11, 14, 20]

evens = list(filter(lambda n: n % 2 == 0, numbers))
print(evens)       # [8, 14, 20]
```

Testing examples:

```python
slow_tests = list(filter(lambda c: c["duration"] > 1.0, test_cases))
print([c["id"] for c in slow_tests])      # ['TC-001', 'TC-003']

high_priority = list(filter(lambda c: c["priority"] == 1, test_cases))
```

(In that print statement, `[c["id"] for c in slow_tests]` is a list comprehension, a compact loop notation covered in a later lesson. A normal `for` loop with `append` does the same.)

`filter(None, items)` removes all falsy items (empty strings, zeros, `None`):

```python
raw = ["TC-001", "", "TC-002", "", ""]
print(list(filter(None, raw)))       # ['TC-001', 'TC-002']
```

#### A word on readability

`map` and `filter` with lambdas are legitimate, but many Python developers prefer **list comprehensions** for these jobs because they read more naturally. For example, `[s * 1000 for s in durations]`. You will learn them later in the program. Meanwhile, understand both styles, because you'll see each in real code. **Sorting with a `key=lambda` has no such alternative and remains the most important use.**

---

### 6. Other Places Lambdas Appear

**A dictionary of actions (a simple dispatch table):**

```python
operations = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
}

print(operations["add"](6, 3))          # 9
print(operations["multiply"](6, 3))     # 18
```

You look up a function by name and call it, replacing a long `if/elif` chain.

**Callbacks:** many libraries accept a function to call later (for example "wait until this condition is true"). Test automation libraries use this idea heavily: a short lambda describes the condition, such as `lambda: page_is_loaded()`.

**Customising behaviour of your own functions:**

```python
def filter_results(results, condition):
    matching = []
    for result in results:
        if condition(result):
            matching.append(result)
    return matching

failures = filter_results(test_cases, lambda c: c["duration"] > 2)
print(len(failures))         # 1
```

The caller supplies the rule; the function does the looping.

---

### 7. Lambda vs `def`: When to Use Which

| Use a **lambda** when... | Use **`def`** when... |
|---|---|
| The logic fits in one short expression | You need several statements or lines |
| It's used once, inline (a sort key, a filter rule) | You'll reuse it in several places |
| The meaning is obvious at a glance | It needs a docstring or a descriptive name |
| | You need loops, `if` blocks, assignments or `return` |
| | It must be easy to debug (named functions show up clearly in error messages) |

A good test: **if you have to think hard to read the lambda, replace it with a named function.**

```python
# Hard to read
sorted(cases, key=lambda c: (c["priority"], -c["duration"], c["title"].lower()))

# Clearer
def sort_rule(case):
    """Order by priority, then longest duration, then title."""
    return (case["priority"], -case["duration"], case["title"].lower())

sorted(cases, key=sort_rule)
```

Both do the same thing. The second has a name and a docstring explaining intent.

---

### 8. Limitations of Lambdas

- **One expression only.** No statements: you cannot write `lambda x: print(x); return x`.
- **No annotations or docstrings.**
- **Anonymous:** tracebacks show `<lambda>` rather than a helpful name.
- **Late binding in loops:** a lambda that uses an outer variable looks that variable up *when it is called*, not when it is created. A common surprise:

```python
functions = []
for n in range(3):
    functions.append(lambda: n)

print(functions[0](), functions[1](), functions[2]())    # 2 2 2   (not 0 1 2!)
```

Each lambda sees the final value of `n`. A fix is to capture the current value as a default argument: `lambda n=n: n`. You don't need this often, but when a lambda inside a loop behaves oddly, this is why. (The next lesson on closures explains the underlying idea.)

---

### 9. Working Example: A Mini Report

```python
results = [
    {"id": "TC-001", "module": "login",    "status": "PASS", "duration": 1.2},
    {"id": "TC-002", "module": "search",   "status": "FAIL", "duration": 3.4},
    {"id": "TC-003", "module": "checkout", "status": "PASS", "duration": 0.8},
    {"id": "TC-004", "module": "login",    "status": "FAIL", "duration": 2.1},
    {"id": "TC-005", "module": "search",   "status": "PASS", "duration": 1.5},
]

# 1. Failures, slowest first
failures = sorted(
    filter(lambda r: r["status"] == "FAIL", results),
    key=lambda r: r["duration"],
    reverse=True,
)
print("Failures (slowest first):")
for r in failures:
    print(f"  {r['id']} in {r['module']}: {r['duration']}s")

# 2. Slowest test overall
slowest = max(results, key=lambda r: r["duration"])
print(f"Slowest overall: {slowest['id']} ({slowest['duration']}s)")

# 3. Results ordered by module name, then ID
for r in sorted(results, key=lambda r: (r["module"], r["id"])):
    print(f"{r['module']:<10}{r['id']}")
```

```text
Failures (slowest first):
  TC-002 in search: 3.4s
  TC-004 in login: 2.1s
Slowest overall: TC-002 (3.4s)
checkout  TC-003
login     TC-001
login     TC-004
search    TC-002
search    TC-005
```

Notice how `sorted` accepts the output of `filter` directly, and how three tiny lambdas replace three named helpers.

---

### 10. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Writing `return` in a lambda | `lambda x: return x` → `SyntaxError` | The expression's value is returned automatically |
| Calling the function instead of passing it | `sorted(items, key=len())` | `key=len` (no parentheses) |
| Multiple statements | `lambda x: (y = x)` | Use `def` |
| Forgetting `list()` around `map`/`filter` | Prints `<map object ...>` | `list(map(...))` |
| Sorting dictionaries without a key | `TypeError: '<' not supported` | `key=lambda d: d["field"]` |
| Overly complex lambdas | Unreadable | Write a named `def` |
| Using the key's result instead of the item | Expecting the key in the output | `sorted` returns the **original items** |
| Late-binding surprise in loops | All lambdas share the last value | `lambda n=n: n` |
| Comparing different types in a key | `TypeError` | Make sure the key returns comparable values |

---

### 11. Practice Activities

1. **Basic lambdas.** Write lambdas for: doubling a number; checking whether a number is positive; joining first and last name with a space; returning the last character of a string. Call each.
2. **Convert.** Rewrite `def cube(n): return n ** 3` as a lambda and call both.
3. **Sort by length.** Sort `["login", "api", "checkout", "ui"]` by length, then by length descending.
4. **Sort dictionaries.** Using the `test_cases` list in section 3.3, sort by priority, then by title (case-insensitive) and print the IDs.
5. **Two-level sort.** Sort by priority ascending, and within the same priority by duration descending.
6. **Rank counts.** Given `{"login": 5, "search": 9, "cart": 2}`, print the entries ranked from highest to lowest.
7. **max/min.** Find the test with the longest title and the one with the shortest duration using `max` and `min` with lambda keys.
8. **map.** Convert a list of durations in seconds to a list of strings like `"1.2s"` using `map` and a lambda.
9. **filter.** From a list of IDs, keep only those that start with `"API-"`. Then keep only the results that are `"FAIL"`.
10. **Dispatch table.** Build a dictionary of lambdas for `upper`, `lower` and `title` (using the string methods) and apply the chosen one to a text from `input()`.
11. **Refactor.** Take the complex sort key from section 7 and make it a named function with a docstring. Which version would you rather maintain?
12. **Predict the output.** Without running, predict what `functions = [lambda: i for i in range(3)]` followed by calling each one would show, and then explain why. (Run it to check.)

---

## Summary

- Functions are **values**: they can be stored, passed to other functions and returned.
- A **lambda** is a small anonymous function: `lambda params: expression`. The expression's value is returned automatically; no `return` and no statements are allowed.
- Use conditional expressions (`a if cond else b`) for simple branching inside a lambda.
- The most common use is as a **`key`** for `sorted()`, `.sort()`, `min()` and `max()`, particularly with lists of dictionaries or tuples; return a tuple to sort by several fields.
- `map(func, items)` transforms every item; `filter(func, items)` keeps matching items; wrap them in `list()`. List comprehensions (later) are often preferred for these jobs.
- Lambdas also power dispatch tables and callbacks.
- Prefer a named `def` when the logic is long, reused, needs a docstring or is hard to read.
- Watch for late binding when creating lambdas in loops.
- Next: **closures and decorators** build on the idea that functions can be passed in, returned and wrapped.

---

## Additional Resources

- Python Tutorial: Lambda Expressions: https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
- Python documentation: Sorting HOW TO: https://docs.python.org/3/howto/sorting.html
- Real Python: How to Use Python Lambda Functions: https://realpython.com/python-lambda/
