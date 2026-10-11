# Inheritance and Polymorphism

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what inheritance is and the "is-a" relationship it models.
- Create a **child (subclass)** from a **parent (base class)** and reuse the parent's attributes and methods.
- Use `super()` to call the parent's constructor and methods.
- **Override** a method to change or extend its behaviour in a subclass.
- Explain **polymorphism** and use it to treat different objects uniformly through a shared method name.
- Use `isinstance()` and `issubclass()` with inheritance.
- Define a base class that requires subclasses to implement a method (using `NotImplementedError`).
- Understand duck typing, method resolution order (MRO) and why to prefer composition when "is-a" doesn't fit.
- Build a `TestCase` / `TestSuite` class hierarchy for a test framework.

---

## Why This Matters

Test suites contain *different kinds* of tests: UI tests, API tests, database tests, performance tests. They share a lot (every test has an ID, a title and a status, and can be run and reported) but each runs in its own way. If you wrote four independent classes, you'd copy and paste the shared parts four times, and a change to the shared logic would need four edits.

**Inheritance** lets you write the shared parts once, in a parent class, and have specialised child classes build on them. **Polymorphism** lets the rest of the program treat all those different tests identically: "run every test in the suite", without caring which kind each one is.

This is the pattern behind nearly every test framework: pytest and unittest have base classes, Selenium has a family of element and driver classes, and the Page Object Model often uses a `BasePage` that every page inherits from. Today's demo builds exactly this: a `TestCase` / `TestSuite` class hierarchy showing inheritance and polymorphism.

---

## The Concept

### 1. The Idea of Inheritance

**Inheritance** is a way to create a new class based on an existing class. The new class (the **child**, **subclass** or **derived class**) automatically gets all the attributes and methods of the existing class (the **parent**, **superclass** or **base class**), and can add or change things.

The relationship is **"is-a"**:

- A `UITest` **is a** `TestCase`.
- An `APITest` **is a** `TestCase`.
- A `Dog` is an `Animal`; a `Car` is a `Vehicle`.

```
              ┌────────────┐
              │  TestCase  │   shared: id, title, status,
              │  (parent)  │           mark_passed(), summary()
              └─────┬──────┘
          ┌─────────┴──────────┐
   ┌──────┴─────┐        ┌─────┴──────┐
   │   UITest   │        │  APITest   │   each adds its own data and behaviour
   │  (child)   │        │  (child)   │
   └────────────┘        └────────────┘
```

(The arrows in a class diagram point from child to parent. Conceptually: "inherits from".)

---

### 2. Creating a Subclass

Put the parent's name in parentheses after the child's name:

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def mark_passed(self):
        self.status = "PASS"

    def mark_failed(self):
        self.status = "FAIL"

    def summary(self):
        return f"{self.id}: {self.title} [{self.status}]"


class UITest(TestCase):
    pass
```

`UITest` has no code of its own, yet it already works completely, because it inherited everything:

```python
test = UITest("UI-001", "Login page loads")
test.mark_passed()
print(test.summary())          # UI-001: Login page loads [PASS]
print(isinstance(test, UITest))     # True
print(isinstance(test, TestCase))   # True  <- a UITest IS a TestCase
```

---

### 3. Extending a Subclass: New Attributes and Methods

A subclass usually adds its own data. To do that it must write its own constructor, **and call the parent's constructor** so that the inherited attributes are still set up. That's the job of **`super()`**:

```python
class UITest(TestCase):
    def __init__(self, test_id, title, browser="Chrome"):
        super().__init__(test_id, title)      # let the parent set id, title, status
        self.browser = browser                # then add what is specific to UI tests

    def take_screenshot(self):
        return f"screenshot_{self.id}_{self.browser}.png"
```

```python
ui = UITest("UI-001", "Login page loads", browser="Firefox")
print(ui.id)                    # UI-001        (set by the parent's __init__)
print(ui.browser)               # Firefox       (set by the child's __init__)
print(ui.take_screenshot())     # screenshot_UI-001_Firefox.png
print(ui.status)                # NOT RUN
```

**`super()`** means "the parent class, as seen from this object". `super().__init__(test_id, title)` runs the parent's constructor on this same object (note you don't pass `self` explicitly).

If you *forget* the `super().__init__(...)` call, the parent's attributes are never created:

```python
class BadUITest(TestCase):
    def __init__(self, test_id, title, browser):
        self.browser = browser            # forgot super().__init__ !

bad = BadUITest("UI-001", "x", "Chrome")
print(bad.status)      # AttributeError: 'BadUITest' object has no attribute 'status'
```

**Rule:** if a child defines `__init__`, call `super().__init__(...)` first (almost always).

And a second subclass with different extras:

```python
class APITest(TestCase):
    def __init__(self, test_id, title, endpoint, expected_status=200):
        super().__init__(test_id, title)
        self.endpoint = endpoint
        self.expected_status = expected_status

    def check_response(self, actual_status):
        if actual_status == self.expected_status:
            self.mark_passed()
        else:
            self.mark_failed()
```

Notice that `check_response` calls `self.mark_passed()`, a method **inherited** from `TestCase`. The child freely uses the parent's methods as if they were its own.

---

### 4. Method Overriding

A child can **override** (replace) a method it inherits by defining a method with **the same name**. Python looks for a method in the child first; if it finds one, it uses it.

Suppose each kind of test runs differently. The parent offers a `run()` method with generic behaviour:

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def run(self):
        print(f"{self.id}: running generic test")
        self.mark_passed()

    def mark_passed(self):
        self.status = "PASS"

    def mark_failed(self):
        self.status = "FAIL"

    def summary(self):
        return f"{self.id}: {self.title} [{self.status}]"


class UITest(TestCase):
    def __init__(self, test_id, title, browser="Chrome"):
        super().__init__(test_id, title)
        self.browser = browser

    def run(self):                                  # overrides TestCase.run
        print(f"{self.id}: opening {self.browser} and clicking through the UI")
        self.mark_passed()


class APITest(TestCase):
    def __init__(self, test_id, title, endpoint):
        super().__init__(test_id, title)
        self.endpoint = endpoint

    def run(self):                                  # overrides TestCase.run
        print(f"{self.id}: sending a request to {self.endpoint}")
        self.mark_passed()
```

```python
TestCase("TC-001", "Generic").run()
UITest("UI-001", "Login page", "Firefox").run()
APITest("API-001", "Get users", "/users").run()
```

```text
TC-001: running generic test
UI-001: opening Firefox and clicking through the UI
API-001: sending a request to /users
```

Each class provides its own version of `run`.

#### Extending instead of replacing: `super().method()`

Sometimes you want to **add to** the parent's behaviour, not replace it. Call the parent's version with `super()`:

```python
class TimedAPITest(APITest):
    def run(self):
        print("Starting timer")
        super().run()                    # do everything the parent does
        print("Stopping timer")
```

Overriding `__str__` or `summary` and calling `super().summary()` to append extra details is a very common use:

```python
class UITest(TestCase):
    ...
    def summary(self):
        return super().summary() + f" (browser: {self.browser})"
```

---

### 5. Polymorphism

**Polymorphism** (Greek for "many forms") means *the same method call behaves differently depending on the object's class*. It is the payoff of overriding.

Put different kinds of tests in **one list** and call the **same method** on each. The loop doesn't need `if` statements to check which kind each is; every object knows how to run itself:

```python
tests = [
    TestCase("TC-001", "Generic check"),
    UITest("UI-001", "Login page", "Firefox"),
    APITest("API-001", "Get users", "/users"),
    UITest("UI-002", "Checkout page", "Chrome"),
]

for test in tests:
    test.run()           # same call, different behaviour each time
```

```text
TC-001: running generic test
UI-001: opening Firefox and clicking through the UI
API-001: sending a request to /users
UI-002: opening Chrome and clicking through the UI
```

Compare this with the alternative that doesn't use polymorphism:

```python
# Without polymorphism: ugly, and must be edited for every new kind of test
for test in tests:
    if isinstance(test, UITest):
        ...
    elif isinstance(test, APITest):
        ...
    else:
        ...
```

With polymorphism, **adding a new kind of test (say `DatabaseTest`) requires no change to the loop** at all; you just write the new class with its own `run`. This is a major reason that OOP code is easier to extend.

#### A suite that works with any test

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run_all(self):
        for test in self.tests:
            test.run()             # polymorphic call

    def results(self):
        return [test.summary() for test in self.tests]

    def passed_count(self):
        return sum(1 for test in self.tests if test.status == "PASS")
```

```python
suite = TestSuite("Regression")
suite.add(UITest("UI-001", "Login page", "Firefox"))
suite.add(APITest("API-001", "Get users", "/users"))
suite.run_all()

for line in suite.results():
    print(line)
print(f"{suite.passed_count()} of {len(suite.tests)} passed")
```

`TestSuite` doesn't know or care about `UITest` or `APITest`. It only relies on the fact that each test has `run()`, `summary()` and `status`: a shared **interface**.

---

### 6. Defining a Required Interface (Abstract-style Base Class)

Sometimes the base class has no sensible default behaviour, and you want to *require* every subclass to implement a method. A simple convention: have the parent method raise **`NotImplementedError`**.

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")
```

`raise` is how a program signals an error on purpose; it stops execution with an error message. (You'll learn how programs can *catch* and handle such errors later in the program. For now, just know that `raise` deliberately stops the program.) If someone forgets to override `run`:

```python
class BrokenTest(TestCase):
    pass

BrokenTest("X-1", "oops").run()
```

```text
NotImplementedError: Subclasses must implement run()
```

The error appears right away, with a clear message, rather than some mysterious failure later. (Python also has an official "abstract base class" feature in the `abc` module that stops you even *creating* an incomplete object. You may meet it later.)

---

### 7. Inspecting Inheritance

```python
ui = UITest("UI-001", "Login page")

print(isinstance(ui, UITest))        # True
print(isinstance(ui, TestCase))      # True   -> also an instance of the parent
print(isinstance(ui, APITest))       # False
print(type(ui))                      # <class '__main__.UITest'>   (exact class only)
print(type(ui) == TestCase)          # False  -> type() ignores inheritance

print(issubclass(UITest, TestCase))  # True
print(issubclass(TestCase, UITest))  # False
print(UITest.__mro__)                # the chain Python searches (see below)
print(UITest.__bases__)              # (<class '__main__.TestCase'>,)
```

Prefer **`isinstance()`** over `type(x) == ...`, because `isinstance` respects inheritance.

#### Method Resolution Order (MRO)

When you call `ui.summary()`, Python looks for `summary` in this order: the object's own class (`UITest`), then its parent (`TestCase`), then `object`, the ultimate base of every class in Python. The first match wins. You can see this chain in `UITest.__mro__`:

```text
(<class '__main__.UITest'>, <class '__main__.TestCase'>, <class 'object'>)
```

Every class implicitly inherits from `object`, which provides default `__str__`, `__repr__`, `__eq__` and so on. That's where the default `<... object at 0x...>` description came from.

---

### 8. Multi-level Inheritance

Inheritance can go several levels deep:

```python
class TestCase: ...
class UITest(TestCase): ...
class LoginUITest(UITest): ...         # is-a UITest, which is-a TestCase
```

```
   TestCase  ──▶  UITest  ──▶  LoginUITest
```

`LoginUITest` inherits from both of its ancestors. Keep hierarchies **shallow** (two or three levels). Deep trees are hard to follow, because to understand one method you may have to read four classes.

#### Multiple inheritance (a brief mention)

Python also allows a class to have more than one parent: `class C(A, B):`. It's powerful but easily confusing, and is best avoided at this stage. If you meet it in other people's code, `__mro__` tells you the lookup order.

---

### 9. Duck Typing

Python doesn't force classes to be related to be used polymorphically. If an object has the method you call, it works. This is called **duck typing**: *"If it walks like a duck and quacks like a duck, it's a duck."*

```python
class ManualTest:
    def run(self):
        print("A human runs this test")

class RobotTest:
    def run(self):
        print("A robot runs this test")

for test in [ManualTest(), RobotTest()]:
    test.run()          # works: both have run(), though they share no parent
```

Inheritance is one way to get polymorphism; simply having the right methods is another. Inheritance is most useful when classes **share real code** and a clear "is-a" relationship, not just a method name.

---

### 10. Inheritance or Composition?

A common beginner mistake is to use inheritance whenever one class uses another. Use this test:

- **"Is-a"** relationship, such as a `UITest` is a `TestCase`, calls for **inheritance**.
- **"Has-a"** relationship, such as a `TestSuite` has `TestCase`s, or a `LoginPage` has a `Browser`, calls for **composition**: store the other object as an attribute.

```python
class TestSuite(list):      # BAD idea: a suite is not really "a list"
    ...

class TestSuite:            # GOOD: a suite HAS a list of tests
    def __init__(self):
        self.tests = []
```

Another rule of thumb: prefer composition when in doubt. It is more flexible, because you can swap the contained object without restructuring your classes.

---

### 11. A Complete Hierarchy: Test Framework Skeleton

```python
class TestCase:
    """Base class for all tests."""

    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")

    def mark_passed(self):
        self.status = "PASS"

    def mark_failed(self):
        self.status = "FAIL"

    def summary(self):
        return f"{self.id}: {self.title} [{self.status}]"

    def __repr__(self):
        return f"{type(self).__name__}({self.id!r}, {self.title!r})"


class UITest(TestCase):
    def __init__(self, test_id, title, browser="Chrome"):
        super().__init__(test_id, title)
        self.browser = browser

    def run(self):
        print(f"  [UI] {self.id} in {self.browser}")
        self.mark_passed()

    def summary(self):
        return super().summary() + f" ({self.browser})"


class APITest(TestCase):
    def __init__(self, test_id, title, endpoint, expected_status=200, actual_status=200):
        super().__init__(test_id, title)
        self.endpoint = endpoint
        self.expected_status = expected_status
        self.actual_status = actual_status      # pretend the server answered with this

    def run(self):
        print(f"  [API] {self.id} GET {self.endpoint}")
        if self.actual_status == self.expected_status:
            self.mark_passed()
        else:
            self.mark_failed()


class TestSuite:
    def __init__(self, name):
        self.name = name
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run_all(self):
        print(f"Running suite: {self.name}")
        for test in self.tests:
            test.run()

    def report(self):
        for test in self.tests:
            print(test.summary())
        passed = sum(1 for t in self.tests if t.status == "PASS")
        print(f"{passed}/{len(self.tests)} passed")


suite = TestSuite("Regression")
suite.add(UITest("UI-001", "Login page loads", "Firefox"))
suite.add(APITest("API-001", "List users", "/users"))
suite.add(APITest("API-002", "Missing page", "/nope", expected_status=404, actual_status=200))
suite.add(UITest("UI-002", "Checkout page loads"))

suite.run_all()
suite.report()
```

```text
Running suite: Regression
  [UI] UI-001 in Firefox
  [API] API-001 GET /users
  [API] API-002 GET /nope
  [UI] UI-002 in Chrome
UI-001: Login page loads [PASS] (Firefox)
API-001: List users [PASS]
API-002: Missing page [FAIL]
UI-002: Checkout page loads [PASS] (Chrome)
3/4 passed
```

Adding a `DatabaseTest` later means writing one new class and adding instances to the suite, with **no changes** to `TestSuite`.

---

### 12. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Forgetting `super().__init__()` | Parent attributes missing | Call it first in the child's `__init__` |
| Passing `self` to `super().__init__` | `super().__init__(self, ...)` | `super().__init__(...)` |
| Wrong parent in the class line | `class UITest:` (no parent) | `class UITest(TestCase):` |
| Overriding with a different signature | Callers break | Keep the same parameters (or compatible ones) |
| Forgetting to return a value in an overridden method | Gives `None` | Return it, like the parent |
| Using `type(x) == Parent` | False for subclasses | Use `isinstance(x, Parent)` |
| Using inheritance for "has-a" | `class Suite(list)` | Use composition |
| Deep inheritance trees | Hard to follow | Keep to 2 to 3 levels |
| Using `if isinstance(...)` chains everywhere | Defeats polymorphism | Put the behaviour in each class's method |
| Calling a parent method by hard-coded name | `TestCase.run(self)` works but is brittle | `super().run()` |
| Not implementing the required method | `NotImplementedError` | Override it in each subclass |
| Changing the parent without thinking | Breaks all the children | Remember that children depend on the parent |

---

### 13. Practice Activities

1. **First subclass.** Create `Animal` (with `name` and a `speak()` method returning `"..."`) and subclasses `Dog` and `Cat` overriding `speak`. Put one of each in a list and call `speak()` on all of them.
2. **super().** Add an extra attribute to each subclass (for example `breed`) using `super().__init__`. Then deliberately omit the `super()` call and read the error.
3. **TestCase hierarchy.** Implement `TestCase`, `UITest` and `APITest` as in section 11, with your own extra attributes.
4. **Override.** Override `summary()` in one subclass to add extra detail by calling `super().summary()`.
5. **Polymorphism.** Create a list of five mixed tests and loop `test.run()`. Then add a new `DatabaseTest` class and verify that the loop needed no changes.
6. **Suite.** Write `TestSuite` with `add`, `run_all`, `passed_count` and `report`. Run it with a mix of passing and failing tests.
7. **Required method.** Make `TestCase.run` raise `NotImplementedError`. Create a subclass that forgets to override it and read the message.
8. **isinstance.** Print `isinstance` and `issubclass` results for several combinations; explain why `type(ui) == TestCase` is `False` but `isinstance(ui, TestCase)` is `True`.
9. **MRO.** Print `UITest.__mro__` and explain it in your own words.
10. **Duck typing.** Create two unrelated classes with the same method name and call it in a loop.
11. **Design choice.** For each, decide inheritance or composition and why: (a) `ChromeBrowser` and `FirefoxBrowser` vs `Browser`; (b) `TestSuite` and `TestCase`; (c) `LoginPage` and `Browser`; (d) `AdminUser` and `User`.
12. **Extension.** Add a `skip()` method to `TestCase` that sets status to `"SKIPPED"`, and change `TestSuite.report` to count skipped tests separately. Verify that all subclasses automatically get `skip()`.

---

## Summary

- **Inheritance** lets a **child class** reuse and extend a **parent class**; write `class Child(Parent):`. It models an **"is-a"** relationship.
- A child inherits all attributes and methods; it can **add** its own. If the child defines `__init__`, call **`super().__init__(...)`** so the parent's setup runs.
- **Overriding** means redefining a method with the same name in the child; use `super().method()` to extend rather than replace the parent's version.
- **Polymorphism**: the same method call (`test.run()`) behaves differently depending on the object's class, letting code treat different objects uniformly and making programs easy to extend.
- A base class can require a method by raising **`NotImplementedError`**.
- Use **`isinstance()`** / **`issubclass()`** (not `type() ==`) to check relationships; the **MRO** is the lookup order (child, parent, `object`).
- **Duck typing**: if the object has the method, it works, even without a shared parent.
- Choose **inheritance** for "is-a", **composition** for "has-a"; keep hierarchies shallow.
- Next: **encapsulation** protects an object's data and controls how it is changed.

---

## Additional Resources

- Python Tutorial: Inheritance: https://docs.python.org/3/tutorial/classes.html#inheritance
- Python documentation: `super()`: https://docs.python.org/3/library/functions.html#super
- Real Python: Inheritance and Composition, A Python OOP Guide: https://realpython.com/inheritance-composition-python/
