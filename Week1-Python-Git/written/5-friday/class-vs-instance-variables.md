# Class vs. Instance Variables

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between an **instance variable** (one per object) and a **class variable** (one shared by all objects).
- Define class variables in the class body and instance variables in `__init__`.
- Read and change class variables correctly, using the class name or an instance.
- Predict what happens when an instance assignment **shadows** a class variable.
- Use class variables for constants, defaults and counters (such as counting created objects).
- Avoid the **mutable class variable** trap.
- Understand how Python looks up attributes (instance first, then class, then parents).
- Choose between a class variable and an instance variable for a given piece of data.

---

## Why This Matters

Since this morning, every attribute you created used `self.something = value` inside `__init__`. That gives each object **its own copy** of the data. But some data doesn't belong to any single object. It belongs to the **concept as a whole**:

- The list of valid test statuses (`PASS`, `FAIL`, `NOT RUN`, `SKIPPED`) is the same for every test case.
- The default timeout for every browser session.
- How many test cases have been created so far.
- A base URL that all page objects in the framework share.

Storing such data separately in every object wastes memory and, worse, makes it easy for objects to disagree ("this test thinks the timeout is 30, that one thinks 60"). **Class variables** hold one shared copy at the class level.

Understanding this distinction prevents a family of subtle bugs (particularly shared mutable lists) and is also essential for reading framework code, where class-level configuration is common. It also sets up the final lesson of the week on static and class methods.

---

## The Concept

### 1. Two Places to Store Data

```python
class TestCase:
    # CLASS VARIABLE: defined in the class body, shared by all objects
    valid_statuses = ("NOT RUN", "PASS", "FAIL", "SKIPPED")

    def __init__(self, test_id, title):
        # INSTANCE VARIABLES: defined with self., separate for each object
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"
```

| | Instance variable | Class variable |
|---|---|---|
| Defined | Inside methods (usually `__init__`) with `self.name = ...` | Directly in the class body, outside any method |
| Belongs to | **One object** | **The class** (shared by all its objects) |
| Number of copies | One per object | **One in total** |
| Typical use | Data that differs between objects: ID, title, status | Data common to all: constants, defaults, counters |
| Access | `object.name` | `ClassName.name` or `object.name` |

```
 CLASS TestCase
 ┌───────────────────────────────────────────┐
 │ valid_statuses = ("NOT RUN","PASS",...)   │  ◀── ONE copy, shared
 └─────────────────────────────────────────┘
        ▲                      ▲
 ┌──────┴────────┐     ┌───────┴───────┐
 │ case_1        │     │ case_2        │
 │ id  = TC-001  │     │ id  = TC-002  │   ◀── separate copies per object
 │ title = Login │     │ title = Logout│
 └───────────────┘     └───────────────┘
```

---

### 2. Reading Class Variables

You can read a class variable through the **class** or through any **instance**:

```python
print(TestCase.valid_statuses)       # ('NOT RUN', 'PASS', 'FAIL', 'SKIPPED')

case = TestCase("TC-001", "Login")
print(case.valid_statuses)           # the same tuple
print(case.valid_statuses is TestCase.valid_statuses)    # True: literally the same object
```

Using the **class name** (`TestCase.valid_statuses`) is clearer when you mean the shared value, because it tells the reader it isn't per-object data.

#### How Python finds an attribute

When you write `case.valid_statuses`, Python searches in this order and stops at the first match:

1. **The instance** itself (`case.__dict__`).
2. **The instance's class** (`TestCase.__dict__`).
3. **The parent classes**, following the MRO from Friday's inheritance lesson.

```python
print("valid_statuses" in case.__dict__)        # False -> not stored on the instance
print("valid_statuses" in TestCase.__dict__)     # True  -> stored on the class
```

This lookup order is the key to everything that follows.

---

### 3. Changing Class Variables

#### 3.1 Change it through the class: all objects see the change

```python
class Browser:
    default_timeout = 30                  # class variable

    def __init__(self, name):
        self.name = name

chrome = Browser("Chrome")
firefox = Browser("Firefox")

print(chrome.default_timeout, firefox.default_timeout)    # 30 30

Browser.default_timeout = 60              # change the shared value, via the CLASS

print(chrome.default_timeout, firefox.default_timeout)    # 60 60  <- both see it
```

One assignment changed the value for every object (including ones created later).

#### 3.2 The shadowing trap: assigning through an instance

Assigning to `object.name` **never** changes a class variable. Instead it **creates a new instance variable** with that name, which **shadows** (hides) the class variable for that one object:

```python
chrome.default_timeout = 5               # creates an INSTANCE variable on chrome only

print(chrome.default_timeout)            # 5    -> found on the instance first
print(firefox.default_timeout)           # 60   -> still the class variable
print(Browser.default_timeout)           # 60   -> unchanged
print(chrome.__dict__)                   # {'name': 'Chrome', 'default_timeout': 5}
```

This can be useful intentionally (**a per-object override of a shared default**) but is a source of confusing bugs when it happens by accident. A frequent mistake:

```python
class Counter:
    count = 0
    def increment(self):
        self.count += 1       # reads the class value, then creates an instance variable!

a = Counter()
b = Counter()
a.increment()
a.increment()
b.increment()

print(a.count, b.count, Counter.count)    # 2 1 0   <- the class variable never changed!
```

`self.count += 1` means `self.count = self.count + 1`: Python *reads* `count` (finding the class value 0) and then *assigns* to `self.count`, which creates an instance variable. To change the class variable, write `Counter.count += 1`.

**Rule of thumb:** to **modify** a class variable, always use the **class name** (`ClassName.variable`). Use `self.variable` for instance data.

---

### 4. Common Uses of Class Variables

#### 4.1 Constants

```python
class TestCase:
    MAX_TITLE_LENGTH = 80
    VALID_STATUSES = ("NOT RUN", "PASS", "FAIL", "SKIPPED")

    def __init__(self, test_id, title):
        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValueError(f"title longer than {self.MAX_TITLE_LENGTH} characters")
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def set_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"invalid status {status!r}")
        self.status = status
```

By convention, constants are written in **UPPER_CASE**. Inside methods, you read them with `self.NAME` (or `TestCase.NAME`). It's more flexible, because a subclass can override the constant by defining its own, and `self.MAX_TITLE_LENGTH` will pick up the subclass's version:

```python
class ShortTitleTest(TestCase):
    MAX_TITLE_LENGTH = 20            # override for this subclass
```

#### 4.2 Shared defaults

```python
class ApiClient:
    BASE_URL = "https://api.example.com"
    TIMEOUT_SECONDS = 10

    def __init__(self, token):
        self.token = token

    def url_for(self, path):
        return f"{self.BASE_URL}{path}"

client = ApiClient("abc")
print(client.url_for("/users"))       # https://api.example.com/users
```

Configuration shared by the whole framework often lives in class variables.

#### 4.3 Counting objects

A class variable is the natural place to count how many objects have been created, because the count belongs to the class, not any one object:

```python
class TestCase:
    total_created = 0                  # shared counter

    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        TestCase.total_created += 1    # modify via the CLASS name

a = TestCase("TC-001", "Login")
b = TestCase("TC-002", "Logout")
c = TestCase("TC-003", "Search")

print(TestCase.total_created)         # 3
print(a.total_created)                # 3 (readable through any instance)
```

A related use is generating **unique IDs** automatically:

```python
class TestRun:
    _next_number = 1

    def __init__(self, name):
        self.run_id = f"RUN-{TestRun._next_number:04d}"
        TestRun._next_number += 1
        self.name = name

r1 = TestRun("nightly")
r2 = TestRun("smoke")
print(r1.run_id, r2.run_id)           # RUN-0001 RUN-0002
```

(The leading underscore signals that `_next_number` is internal, as in the previous lesson.)

#### 4.4 Keeping a registry of all instances

```python
class Browser:
    all_browsers = []                 # shared list: intentional!

    def __init__(self, name):
        self.name = name
        Browser.all_browsers.append(self)

Browser("Chrome")
Browser("Firefox")
print([b.name for b in Browser.all_browsers])      # ['Chrome', 'Firefox']
```

Sharing a list on purpose is fine, but you must be very clear that you *want* sharing; see the next section for what happens when you don't.

---

### 5. The Mutable Class Variable Trap

This is the object-oriented cousin of the mutable-default-argument bug from Thursday. If you put a **list or dictionary** in the class body when each object was supposed to have its **own**, all objects share the same one:

```python
class TestSuite:
    cases = []                        # BUG: one list shared by every suite

    def __init__(self, name):
        self.name = name

    def add(self, case):
        self.cases.append(case)       # modifies the shared list in place

smoke = TestSuite("Smoke")
regression = TestSuite("Regression")

smoke.add("TC-001")
regression.add("TC-100")

print(smoke.cases)         # ['TC-001', 'TC-100']   <- regression's test leaked in!
print(regression.cases)    # ['TC-001', 'TC-100']
print(smoke.cases is regression.cases)    # True
```

`self.cases.append(...)` doesn't *assign* to `self.cases`; it finds the one class-level list and changes it in place. Every suite shares it.

**Fix:** create per-object mutable data in `__init__`:

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self.cases = []               # a NEW list for every suite

    def add(self, case):
        self.cases.append(case)
```

**Rule:** *if each object needs its own list, dictionary or set, create it in `__init__` with `self.`.* Reserve mutable class variables for data you truly mean to share (and document that intention).

Immutable class variables (numbers, strings, tuples) are safe to share, because you can't change them in place; you can only rebind them, which (via an instance) creates a shadow rather than altering the shared value.

---

### 6. Class Variables and Inheritance

Subclasses inherit class variables, and can override them:

```python
class TestCase:
    default_timeout = 30

class UITest(TestCase):
    default_timeout = 60              # overrides for UITest and its objects

class APITest(TestCase):
    pass                              # inherits 30

print(TestCase.default_timeout)       # 30
print(UITest.default_timeout)         # 60
print(APITest.default_timeout)        # 30
```

Be careful when modifying through a parent or child class:

```python
TestCase.default_timeout = 45
print(APITest.default_timeout)        # 45  -> APITest has no own value, so it follows the parent
print(UITest.default_timeout)         # 60  -> UITest has its own, unaffected

APITest.default_timeout = 5           # now APITest has its OWN value
TestCase.default_timeout = 99
print(APITest.default_timeout)        # 5   -> no longer follows the parent
```

The same lookup rule as before (instance, class, then parents) explains every result.

A counter shared across a hierarchy works the same way: `TestCase.total_created += 1` in the base constructor counts every kind of test, since the subclasses' `super().__init__()` runs that line.

---

### 7. Putting It All Together: A Test Case With Both Kinds of Data

Here is one class that uses both kinds of variable, each for the right job:

```python
class TestCase:
    VALID_STATUSES = ("NOT RUN", "PASS", "FAIL", "SKIPPED")
    DEFAULT_PRIORITY = "Medium"
    _created = 0

    def __init__(self, test_id, title, priority=None):
        self.id = test_id
        self.title = title
        self.priority = priority if priority is not None else self.DEFAULT_PRIORITY
        self.status = "NOT RUN"
        self.history = []
        TestCase._created += 1

    def set_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"invalid status {status!r}")
        self.history.append((self.status, status))
        self.status = status


a = TestCase("TC-001", "Login")
b = TestCase("TC-002", "Checkout", priority="High")

a.set_status("PASS")
b.set_status("FAIL")
b.set_status("SKIPPED")

print(a.priority, b.priority)       # Medium High
print(a.history)                    # [('NOT RUN', 'PASS')]
print(b.history)                    # [('NOT RUN', 'FAIL'), ('FAIL', 'SKIPPED')]
print(TestCase._created)            # 2
```

Which variable is which?

| Variable | Kind | Why |
|---|---|---|
| `VALID_STATUSES`, `DEFAULT_PRIORITY` | Class | Same for every test case; constants |
| `_created` | Class | A counter for the whole class |
| `id`, `title`, `priority`, `status` | Instance | Different for each test case |
| `history` | Instance | A mutable list each test needs its own copy of |

---

### 8. Decision Guide: Class or Instance?

Ask: **"Would two different objects ever need different values for this?"**

- **Yes** → **instance variable** (set in `__init__` with `self.`).
- **No, it's the same for all** → **class variable**.
- **It's a list/dict/set** and each object needs its own → **instance** (definitely `__init__`).
- **It's a constant** → class variable in `UPPER_CASE`.
- **It counts or tracks things across all objects** → class variable, changed via the class name.
- **Most objects use a default, but some may override** → class variable as the default; assign on an instance to override that one object (and know that you're shadowing).

---

### 9. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Shared mutable class attribute | `cases = []` in the class body | `self.cases = []` in `__init__` |
| Changing a class variable via `self` | `self.count += 1` | `ClassName.count += 1` |
| Expecting instance assignment to change all objects | `obj.default = 5` affects only `obj` | `ClassName.default = 5` |
| Forgetting `self.` when reading instance data | `status` | `self.status` |
| Forgetting `ClassName.`/`self.` when reading class data | `VALID_STATUSES` inside a method → `NameError` | `self.VALID_STATUSES` or `ClassName.VALID_STATUSES` |
| Putting per-object data in the class body | `title = ""` as a "default" then assigning later | Initialise in `__init__` |
| Confusing the two lookups | Surprising values after assignment | Inspect `obj.__dict__` and `Class.__dict__` |
| Hard-coding the class name where inheritance matters | `TestCase._created += 1` in a hierarchy where you want per-subclass counts | Knowing which you want; per-subclass counts need other techniques (next lesson's class methods help) |
| Using class variables as hidden global state | Tests influence each other | Reset them, or avoid mutable shared state in tests |

**Test-isolation note:** shared mutable state is a favourite source of "flaky" tests, tests that pass alone but fail when run together (or the reverse), because an earlier test changed a class-level value that a later test relies on. Prefer instance state, and if you must use class-level counters or registries, reset them between tests.

---

### 10. Practice Activities

1. **Predict.** Without running, predict the output, then verify:
   ```python
   class A:
       x = 1

   a = A()
   b = A()
   A.x = 2
   a.x = 3
   print(a.x, b.x, A.x)
   ```
2. **Inspect.** Print `a.__dict__` and `A.__dict__` for the example above and match each to your explanation.
3. **Constants.** Add `VALID_STATUSES` to your `TestCase` and use it to validate in a `set_status` method.
4. **Counter.** Add a class-level counter that records how many `TestCase` objects were created, and print it after creating five.
5. **The `self.count` trap.** Reproduce the `Counter` bug where `self.count += 1` leaves `Counter.count` at 0. Fix it two ways.
6. **Unique IDs.** Write a `User` class that gives each new user an automatic ID such as `U-001`, `U-002`.
7. **Shared list bug.** Reproduce the `TestSuite.cases = []` bug, then fix it. Explain in one sentence why the first version misbehaves.
8. **Override.** Create a base class with `TIMEOUT = 30` and two subclasses, one overriding it. Print the timeout through instances of each.
9. **Per-object override.** Create two browsers and give just one a custom `default_timeout` by instance assignment. Explain what `__dict__` shows.
10. **Registry.** Make a `Browser` class that records every instance in a class-level list on purpose, with a comment explaining why the sharing is intentional.
11. **Classify.** For a `TestRun` class, decide for each whether it is a class or instance variable: run ID, start time, list of results, maximum allowed duration, number of runs so far, valid status names.
12. **Flaky-test thinking.** Describe a scenario in which a class-level counter used by tests would make test results depend on the order they run in. How would you prevent it?

---

## Summary

- **Instance variables** (`self.x = ...` in `__init__`) hold data that belongs to **one object**; each object has its own copy.
- **Class variables** (assigned in the class body) belong to the **class** and are shared by **all** objects, ideal for **constants** (`UPPER_CASE`), **defaults**, **counters** and **shared configuration**.
- Attribute lookup order: **instance, then class, then parent classes**.
- **Read** a class variable via the class or an instance; **modify** it via the **class name**. Assigning through an instance creates an instance variable that **shadows** the class one (so `self.count += 1` doesn't update a class counter).
- Never put per-object **mutable** data (lists, dictionaries, sets) in the class body; create it in `__init__`.
- Subclasses inherit class variables and may override them.
- Decide with: *"Would two objects need different values?"* Yes means instance; no means class.
- Shared mutable class state is a classic cause of flaky tests, so keep tests isolated.
- Next: **static and class methods**, methods that belong to the class rather than to a particular object.

---

## Additional Resources

- Python Tutorial: Class and Instance Variables: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables
- Python documentation: Data model, class instances and attribute lookup: https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy
- Real Python: Python Class Attributes vs Instance Attributes: https://realpython.com/lessons/class-and-instance-attributes/
