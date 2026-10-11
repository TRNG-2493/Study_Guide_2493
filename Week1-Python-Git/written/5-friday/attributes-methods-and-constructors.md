# Attributes, Methods and Constructors

## Learning Objectives

By the end of this lesson you will be able to:

- Write a constructor with `__init__` that sets up each new object correctly.
- Explain what `self` does inside `__init__` and why attributes are assigned with `self.name = ...`.
- Use constructor parameters, default values and keyword arguments.
- Distinguish **instance attributes** from local variables and parameters.
- Write methods that read data, change data and return values.
- Call one method from another using `self`.
- Make objects print nicely with `__str__` and `__repr__`.
- Add and delete attributes dynamically, and understand when that is a bad idea.
- Build small, realistic classes such as `TestCase`, `TestResult` and `TestSuite`.

---

## Why This Matters

Last lesson, creating an object was clumsy: you made an empty object and then added attributes one by one. It was easy to forget one, or mistype `staus`. Real classes need a way to guarantee that **every new object starts life complete and valid**. That job belongs to the **constructor**.

Today you also learn to make your objects *behave* well: methods that change state in controlled ways, and a readable text description so that when you `print` an object or see it in an error message, you see `TC-001: Valid login [PASS]` instead of `<__main__.TestCase object at 0x000001E5A3B4C2D0>`.

This is the lesson where classes become genuinely useful. By the end you will be able to write the `TestResult`, `Suite` and `Reporter` classes needed for today's exercise.

---

## The Concept

### 1. The Constructor: `__init__`

A **constructor** is a special method that Python runs **automatically** every time you create a new object. In Python it is named **`__init__`** (two underscores, `init`, two underscores). Its job is to **initialise** the new object: to set its starting attributes.

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"
```

Create objects by passing the constructor's arguments (without `self`):

```python
case_1 = TestCase("TC-001", "Valid login")
case_2 = TestCase("TC-002", "Search by keyword")

print(case_1.id)           # TC-001
print(case_1.status)       # NOT RUN
print(case_2.title)        # Search by keyword
```

What happens when Python executes `TestCase("TC-001", "Valid login")`:

1. Python creates a new, empty `TestCase` object.
2. It calls `__init__`, passing the new object as `self` and the other arguments as `test_id` and `title`.
3. Inside `__init__`, `self.id = test_id` stores the argument **on the object**.
4. The finished object is returned and stored in `case_1`.

```
 TestCase("TC-001", "Valid login")
         │
         ├─▶ new empty object created  ──▶ self
         ├─▶ __init__(self, "TC-001", "Valid login") runs
         │       self.id     = "TC-001"
         │       self.title  = "Valid login"
         │       self.status = "NOT RUN"
         └─▶ the completed object is returned
```

#### Why `self.id = test_id`?

- `test_id` is a **parameter**: a local variable that disappears when `__init__` ends.
- `self.id` is an **attribute**: it is attached to the object and **lives as long as the object does**.

Writing `id = test_id` (without `self.`) would only create a throw-away local variable. That is the most common beginner bug with constructors.

```python
class Broken:
    def __init__(self, name):
        name = name              # local only! nothing stored on the object

b = Broken("x")
print(b.name)       # AttributeError: 'Broken' object has no attribute 'name'
```

(The attribute and the parameter may have the same name, as in `self.name = name`; that is perfectly normal and very common.)

#### Rules for `__init__`

- The first parameter is always `self`.
- It should **not return a value** (it implicitly returns `None`).
- You don't call it directly; calling the class does that for you.
- Every attribute the object needs should be created here, so that every object has the same "shape".

---

### 2. Default Values and Keyword Arguments in Constructors

Everything you learned on Thursday about parameters applies to `__init__`:

```python
class TestCase:
    def __init__(self, test_id, title, priority="Medium", automated=False):
        self.id = test_id
        self.title = title
        self.priority = priority
        self.automated = automated
        self.status = "NOT RUN"

a = TestCase("TC-001", "Valid login")
b = TestCase("TC-002", "Checkout", priority="High", automated=True)

print(a.priority, a.automated)      # Medium False
print(b.priority, b.automated)      # High True
```

Watch out for the **mutable default trap** from Thursday. Never write `def __init__(self, tags=[])`. If you need a list attribute, either create an empty one inside or accept `None`:

```python
class TestCase:
    def __init__(self, test_id, title, tags=None):
        self.id = test_id
        self.title = title
        self.tags = [] if tags is None else list(tags)    # a fresh list for every object
```

`list(tags)` makes a **copy**, so the object doesn't share the caller's list.

An attribute doesn't have to come from a parameter. Often it starts with a fixed value (`self.status = "NOT RUN"`), is empty (`self.results = []`), or is computed:

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self.cases = []              # starts empty; filled by methods
```

Each `TestSuite` object gets its **own** empty list, because `[]` is evaluated every time `__init__` runs.

---

### 3. Instance Attributes

An **instance attribute** is data stored on one specific object, created with `self.attribute = value` (normally in `__init__`).

```python
class User:
    def __init__(self, username, role="viewer"):
        self.username = username
        self.role = role
        self.logged_in = False
```

```python
alice = User("alice", "admin")
bob = User("bob")

alice.logged_in = True          # change one object's attribute

print(alice.logged_in, bob.logged_in)     # True False
print(alice.__dict__)
# {'username': 'alice', 'role': 'admin', 'logged_in': True}
```

Attributes can hold **any type**, including lists, dictionaries and **other objects**:

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self.cases = []              # a list of TestCase objects

suite = TestSuite("Smoke")
suite.cases.append(TestCase("TC-001", "Valid login"))
suite.cases.append(TestCase("TC-002", "Logout"))

print(len(suite.cases))              # 2
print(suite.cases[0].title)          # Valid login
```

Reading `suite.cases[0].title` works step by step: `suite.cases` is a list, `[0]` picks the first item (a `TestCase` object), and `.title` reads its attribute. This chaining of dots and brackets is typical in OOP code.

---

### 4. Instance Methods

A **method** defined in the class and taking `self` is an **instance method**. Methods fall into some common roles.

#### 4.1 Methods that report information (return a value)

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def is_finished(self):
        return self.status in ("PASS", "FAIL")

    def summary(self):
        return f"{self.id}: {self.title} [{self.status}]"
```

```python
case = TestCase("TC-001", "Valid login")
print(case.is_finished())     # False
print(case.summary())         # TC-001: Valid login [NOT RUN]
```

As in the previous lessons: methods that compute should **return** the result and let the caller print it.

#### 4.2 Methods that change state

```python
    def mark_passed(self):
        self.status = "PASS"

    def mark_failed(self, reason=""):
        self.status = "FAIL"
        self.failure_reason = reason
```

Notice something subtle: `failure_reason` is created inside `mark_failed`, not in `__init__`. It works, but then **some objects have the attribute and others don't**, which leads to `AttributeError`. Better to create it in `__init__` with a starting value:

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"
        self.failure_reason = ""      # always exists

    def mark_failed(self, reason=""):
        self.status = "FAIL"
        self.failure_reason = reason
```

**Rule:** define *all* of an object's attributes in `__init__`.

#### 4.3 Methods that accept data

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self.cases = []

    def add_case(self, case):
        self.cases.append(case)

    def count(self):
        return len(self.cases)

    def count_status(self, status):
        total = 0
        for case in self.cases:
            if case.status == status:
                total += 1
        return total
```

```python
suite = TestSuite("Smoke")
suite.add_case(TestCase("TC-001", "Valid login"))
suite.add_case(TestCase("TC-002", "Logout"))

suite.cases[0].mark_passed()

print(suite.count())                  # 2
print(suite.count_status("PASS"))     # 1
```

#### 4.4 Methods calling other methods

Inside a class, call another method of the same object with `self.method_name()`:

```python
    def pass_rate(self):
        if self.count() == 0:
            return 0.0
        return self.count_status("PASS") / self.count() * 100

    def report_line(self):
        return f"{self.name}: {self.count_status('PASS')}/{self.count()} passed ({self.pass_rate():.0f}%)"
```

Building bigger behaviour out of small methods is the same design principle as with functions.

#### 4.5 Methods returning `self` (method chaining)

A method that modifies the object can return `self` so that calls can be chained:

```python
    def add_case(self, case):
        self.cases.append(case)
        return self

suite = TestSuite("Smoke")
suite.add_case(TestCase("TC-001", "Login")).add_case(TestCase("TC-002", "Logout"))
```

This is optional style, but you will see it in some libraries.

---

### 5. Making Objects Printable: `__str__` and `__repr__`

By default, `print(case)` gives the ugly `<__main__.TestCase object at 0x...>`. Python lets you define the text description with two special ("dunder", short for *double underscore*) methods.

#### `__str__`: the friendly description

Used by `print()` and `str()` and f-strings. It should return a **readable string for humans**.

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def __str__(self):
        return f"{self.id}: {self.title} [{self.status}]"

case = TestCase("TC-001", "Valid login")
print(case)                    # TC-001: Valid login [NOT RUN]
print(f"Running {case}")       # Running TC-001: Valid login [NOT RUN]
```

#### `__repr__`: the developer description

Used when the object is shown inside a list, in the REPL and in debugging output. Convention: return text that looks like the code that would recreate the object.

```python
    def __repr__(self):
        return f"TestCase({self.id!r}, {self.title!r})"
```

```python
cases = [TestCase("TC-001", "Login"), TestCase("TC-002", "Logout")]
print(cases)         # [TestCase('TC-001', 'Login'), TestCase('TC-002', 'Logout')]
```

(`!r` in an f-string gives the quoted "repr" form of a value, seen last week.)

If a class defines only `__repr__`, Python also uses it for `print`. If you only define one, **define `__repr__`**: it is the most useful for debugging. If both exist, `print` uses `__str__`.

A pair like this helps *enormously* when a test fails and you need to see what the objects looked like.

#### Other special methods you will meet

Methods named `__something__` are called **special** (or "magic" or "dunder") methods; Python calls them automatically in certain situations. You already know `__init__`, `__str__` and `__repr__`. Others include `__len__` (so `len(obj)` works), `__eq__` (to define `==`) and `__lt__` (to define `<`). We won't use them today, but it's good to know the pattern: *define the special method and Python's built-in syntax starts working with your class*.

---

### 6. Accessing, Adding and Removing Attributes

```python
case = TestCase("TC-001", "Valid login")

print(case.title)              # read
case.title = "Valid user login"    # change
case.owner = "Priya"           # add a NEW attribute (allowed in Python)
del case.owner                 # remove an attribute
```

Python lets you add attributes to an object at any time, but **this is usually a bad idea**: other objects of the same class won't have it, and typos silently create new attributes:

```python
case.staus = "PASS"      # typo creates a brand-new attribute; status is unchanged!
```

Defining every attribute in `__init__` keeps objects uniform and gives your editor a chance to catch mistakes. (A later technique called `__slots__` can forbid extra attributes, but you don't need it now.)

Dynamic access by *name* is useful when the attribute name comes from data:

```python
field = "title"
print(getattr(case, field))          # Valid user login
setattr(case, "priority", "High")    # create or change by name
print(hasattr(case, "priority"))     # True
```

---

### 7. Objects Containing and Using Other Objects (Composition)

Real programs combine classes: a suite **has** test cases; a report **uses** a suite. "Has-a" relationships are called **composition**. Let's build a small but complete example, similar in spirit to today's exercise.

```python
class TestResult:
    """The outcome of running one test."""

    def __init__(self, test_id, status, duration):
        self.test_id = test_id
        self.status = status           # "PASS" or "FAIL"
        self.duration = duration       # seconds

    def passed(self):
        return self.status == "PASS"

    def __repr__(self):
        return f"TestResult({self.test_id!r}, {self.status!r}, {self.duration})"


class Suite:
    """A named collection of test results."""

    def __init__(self, name):
        self.name = name
        self.results = []

    def add(self, result):
        self.results.append(result)

    def total(self):
        return len(self.results)

    def passed_count(self):
        count = 0
        for result in self.results:
            if result.passed():
                count += 1
        return count

    def total_duration(self):
        return sum(result.duration for result in self.results)

    def slowest(self):
        if not self.results:
            return None
        return max(self.results, key=lambda r: r.duration)


class Reporter:
    """Formats a suite's results as text."""

    def __init__(self, suite):
        self.suite = suite

    def text(self):
        lines = [f"=== {self.suite.name} ==="]
        for result in self.suite.results:
            lines.append(f"{result.test_id:<8} {result.status:<5} {result.duration:>5.1f}s")
        lines.append(f"Passed {self.suite.passed_count()} of {self.suite.total()}")
        slowest = self.suite.slowest()
        if slowest is not None:
            lines.append(f"Slowest: {slowest.test_id} ({slowest.duration}s)")
        return "\n".join(lines)


suite = Suite("Login")
suite.add(TestResult("TC-001", "PASS", 1.2))
suite.add(TestResult("TC-002", "FAIL", 3.4))
suite.add(TestResult("TC-003", "PASS", 0.8))

print(Reporter(suite).text())
```

```text
=== Login ===
TC-001   PASS    1.2s
TC-002   FAIL    3.4s
TC-003   PASS    0.8s
Passed 2 of 3
Slowest: TC-002 (3.4s)
```

Observe the design:

- `TestResult` knows about **one** result.
- `Suite` manages **a group** and answers questions about it.
- `Reporter` takes a suite and is responsible only for **presentation**: another example of "one class, one job".
- The `Reporter` receives the `Suite` through its **constructor** and stores it as an attribute, so every method can use it.
- `sum(... for ...)` inside `total_duration` is a compact loop (a generator expression); you can write it as a regular loop with an accumulator, which does the same thing.

---

### 8. Docstrings in Classes

Document classes and methods with docstrings, just like functions:

```python
class TestCase:
    """A single test case with an ID, title and status."""

    def __init__(self, test_id, title):
        """Create a test case that has not been run yet."""
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"
```

The class docstring goes directly under the `class` line. `help(TestCase)` will show everything.

---

### 9. Naming Conventions

| Item | Style | Example |
|---|---|---|
| Class | CapWords | `TestSuite`, `LoginPage` |
| Method, attribute, function, variable | snake_case | `mark_passed`, `pass_rate` |
| Constant | UPPER_CASE | `MAX_RETRIES` |
| "Special" methods | `__double_underscores__` | `__init__`, `__str__` |
| Attributes meant to be internal | leading underscore | `_cache` (explained in the Encapsulation lesson) |

Attribute names should be **nouns** (`status`, `duration`); method names should be **verbs** (`mark_passed`, `add_case`) or questions (`is_finished`, `passed`).

---

### 10. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Misspelling `__init__` | `def _init_(self)` or `def __int__` | Two underscores each side, `init` |
| Assigning without `self.` | `title = title` | `self.title = title` |
| Forgetting `self` as the first parameter | `def __init__(name):` | `def __init__(self, name):` |
| Passing `self` when creating | `TestCase(self, "TC-001")` | `TestCase("TC-001")` |
| Returning a value from `__init__` | `return x` | Remove it |
| Mutable default for attributes | `tags=[]` | `tags=None`, create inside |
| Forgetting `self.` when calling another method | `count()` | `self.count()` |
| Creating attributes outside `__init__` | Missing on some objects | Initialise them all in `__init__` |
| Printing returns `None` | A method that prints and the caller prints again | Return strings; print outside |
| `__str__` that prints instead of returning | Prints `None` | `return` the text |
| Sharing a list between objects | `self.cases = shared_list` | Copy it or create a new one |
| Wrong number of constructor arguments | `TypeError` | Match the parameters |

---

### 11. Practice Activities

1. **Constructor.** Write a `User` class with `__init__(self, username, role="viewer")`. Create three users and print their attributes.
2. **Fix the bug.** Why does `b.name` fail here? Fix it.
   ```python
   class Broken:
       def __init__(self, name):
           name = name
   ```
3. **Methods.** Add `promote(self)` to `User` (sets the role to `"admin"`) and `is_admin(self)` (returns a boolean). Test them.
4. **`__str__` and `__repr__`.** Give `User` both. Print a single user, print a list of users, and describe the difference in output.
5. **Counter.** Write a `Counter` class with `count` starting at 0 in `__init__`, and methods `increment`, `reset` and `value`. (Name it `RunCounter` if you've imported `collections.Counter`.)
6. **TestCase.** Implement `TestCase` with `id`, `title`, `priority`, `status`, `failure_reason` and methods `mark_passed`, `mark_failed(reason)` and `summary`.
7. **Suite.** Implement `TestSuite` with `add_case`, `count`, `count_status`, `pass_rate` and a `__str__` that returns a one-line summary. Build a suite of five cases, run them (mark outcomes) and print the summary.
8. **Own data.** Create two suites and verify each has its own list of cases (add a case to one and check the other is unchanged).
9. **Composition.** Reproduce the `TestResult`, `Suite` and `Reporter` example and extend `Reporter` with a method `failures_text()` that lists only the failed tests.
10. **Defaults.** Add optional `tags` to `TestCase` using the `None` pattern. Show that two cases created without tags don't share one list.
11. **getattr.** Write code that loops over the field names `["id", "title", "status"]` and prints each value of a case using `getattr`.
12. **Explain.** In your own words: what is the difference between a parameter, a local variable and an attribute? Where does each live and for how long?

---

## Summary

- The constructor **`__init__(self, ...)`** runs automatically when an object is created, to set up its attributes: `self.name = name` stores data **on the object**; plain `name = name` does not.
- Constructors accept **parameters, defaults and keywords** just like functions; avoid mutable defaults (`None` and create inside).
- **Instance attributes** belong to one object; define them all in `__init__`, and they may hold any type, including lists and other objects.
- **Instance methods** take `self`. Methods may report (return) values, change state, accept data and call other methods via `self.method()`.
- **`__str__`** (readable) and **`__repr__`** (developer-friendly) control how objects print; they must **return** strings.
- Dunder methods (`__init__`, `__str__`, `__repr__`, and others such as `__len__` and `__eq__`) let your classes plug into Python's syntax.
- **Composition** means objects containing other objects (a `Suite` has `TestResult`s; a `Reporter` uses a `Suite`); give each class one clear job.
- Avoid creating attributes outside `__init__` and watch for typos that silently create new attributes.
- Next: **inheritance and polymorphism** let new classes reuse and specialise existing ones.

---

## Additional Resources

- Python Tutorial: Class Objects, Instance Objects and Method Objects: https://docs.python.org/3/tutorial/classes.html#class-objects
- Python documentation: Special method names: https://docs.python.org/3/reference/datamodel.html#special-method-names
- Real Python: Python Classes: The Power of Object-Oriented Programming: https://realpython.com/python-classes/
