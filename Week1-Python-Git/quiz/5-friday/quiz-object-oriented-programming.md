# Knowledge Check: Object-Oriented Programming (Week 1 – Friday)

Answer each question on your own first, then click "Click for Solution" to check your answer and read the explanation.

---

## Part 1: Multiple Choice

### Question 1

In a test framework you call `case_1.mark_passed()`, where `mark_passed` is defined as `def mark_passed(self): self.status = "PASS"`. What does `self` refer to inside the method?

- [ ] A) The `TestCase` class itself
- [ ] B) The object `case_1` that the method was called on
- [ ] C) A copy of `case_1` made for the duration of the call
- [ ] D) The string `"PASS"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Python automatically passes the object before the dot as the first argument, so `case_1.mark_passed()` behaves like `TestCase.mark_passed(case_1)`. That is why `self.status = "PASS"` changes that particular test case.
- **Why others are wrong:**
  - A) The class is passed only to class methods (as `cls`), not to instance methods.
  - C) No copy is made; `self` is the very same object, which is why the change is visible afterwards.
  - D) `"PASS"` is just the value being assigned; it is not passed as `self`.
</details>

---

### Question 2

A trainee writes this class and then runs `Broken().hello()`:

```python
class Broken:
    def hello():
        print("hi")
```

What happens?

- [ ] A) It prints `hi`
- [ ] B) It prints nothing because `hello` is never executed
- [ ] C) `AttributeError: 'Broken' object has no attribute 'hello'`
- [ ] D) `TypeError`, because Python passes the object automatically and `hello` accepts no parameters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** When a method is called on an object, Python passes the object as the first argument. Since `hello` was defined without `self`, it takes 0 positional arguments but 1 was given.
- **Why others are wrong:**
  - A) The call fails before the `print` line can run.
  - B) The method is called (the parentheses are present), so it fails with an error rather than silently doing nothing.
  - C) `hello` does exist on the class, so the attribute lookup succeeds; the failure happens at the call.
</details>

---

### Question 3

A trainee writes this constructor, then reads `b.name`:

```python
class Broken:
    def __init__(self, name):
        name = name

b = Broken("x")
print(b.name)
```

Why does this raise an `AttributeError`?

- [ ] A) `name = name` only creates a local variable; it never stores anything on the object (it needs `self.name = name`)
- [ ] B) `name` is a reserved word in Python and cannot be used as an attribute
- [ ] C) `__init__` must return the object for attributes to be saved
- [ ] D) Attributes can only be created outside `__init__`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** A parameter is a local variable that disappears when `__init__` ends. Only `self.name = name` attaches the value to the object so it lives as long as the object does.
- **Why others are wrong:**
  - B) `name` is not a reserved word; `self.name = name` is perfectly normal and very common.
  - C) `__init__` should not return a value at all; it implicitly returns `None`.
  - D) The recommended practice is the opposite: create all attributes in `__init__`.
</details>

---

### Question 4

You have a list of `TestResult` objects that defines both `__str__` and `__repr__`. What do you see when you run `print(results)` (the list itself)?

- [ ] A) The default text such as `<__main__.TestResult object at 0x...>` for each item
- [ ] B) Each item shown using its `__str__` text
- [ ] C) Each item shown using its `__repr__` text
- [ ] D) An error, because lists cannot hold objects

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `__repr__` is used when an object is shown inside a list, in the REPL and in debugging output. `__str__` is used only when the object itself is printed or converted with `str()`.
- **Why others are wrong:**
  - A) That default text appears only when neither special method is defined.
  - B) `__str__` is used by `print(obj)` for a single object, not for items displayed inside a list.
  - D) Objects can be stored in lists like any other value.
</details>

---

### Question 5

A `BadUITest` subclass defines its own `__init__` that sets `self.browser`, but it does **not** call `super().__init__(...)`. What happens when you read `bad.status` on a new `BadUITest` object, where `status` is normally set by the parent `TestCase.__init__`?

- [ ] A) It returns `"NOT RUN"` because children automatically run the parent constructor
- [ ] B) `AttributeError`, because the parent's constructor never ran so `status` was never created
- [ ] C) It returns `None`
- [ ] D) Python raises an error as soon as the class is defined

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** If a child defines `__init__`, it replaces the parent's one, so the parent's attributes are only created if the child calls `super().__init__(...)`. The rule is to call it first in the child's `__init__`.
- **Why others are wrong:**
  - A) The parent constructor runs automatically only when the child does not define its own `__init__`.
  - C) A missing attribute raises `AttributeError`; Python does not fill in `None`.
  - D) The class definition is valid; the problem only appears when the missing attribute is read.
</details>

---

### Question 6

Your team's `TestSuite` keeps an internal list of tests that other code should not modify directly. Which naming convention is the most common Python way to mark it as internal?

- [ ] A) A single leading underscore: `self._tests`
- [ ] B) A trailing underscore: `self.tests_`
- [ ] C) Double underscores on both sides: `self.__tests__`
- [ ] D) The keyword `private`: `private self.tests`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** A single leading underscore signals "internal use, please don't touch from outside" and is the most common approach in real Python code. It is a convention only and is not enforced.
- **Why others are wrong:**
  - B) A trailing underscore has no special meaning for marking internals.
  - C) Names like `__x__` are reserved for Python's own special methods; you should never create your own.
  - D) Python has no `private` keyword; it relies on naming conventions.
</details>

---

### Question 7

A `TestResult` has a `test_id` that must never change after the object is created. Which approach is the Pythonic way to enforce this?

- [ ] A) Write `get_test_id()` and `set_test_id()` methods and ask teammates not to call the setter
- [ ] B) Name the attribute `__test_id` and rely on it being truly private
- [ ] C) Store it as a public attribute and add a comment saying "do not change"
- [ ] D) Store the value in `_test_id` and expose it through an `@property` with no setter

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** A getter-only `@property` makes the attribute read-only, and assigning to it raises `AttributeError`. It is described as a powerful, simple way to express "this must never change after creation".
- **Why others are wrong:**
  - A) A setter method would allow the value to be changed, and getter/setter methods are the clunky traditional approach.
  - B) `__name` is not truly private; name mangling only makes it awkward to reach (`obj._Class__name` still works).
  - C) A comment is not enforced, so anyone can still assign a new value.
</details>

---

### Question 8

A trainee writes the following class and creates two suites, `smoke` and `regression`:

```python
class TestSuite:
    cases = []

    def __init__(self, name):
        self.name = name

    def add(self, case):
        self.cases.append(case)
```

After `smoke.add("TC-001")` and `regression.add("TC-100")`, what is the problem?

- [ ] A) `add` raises an error because `cases` is not defined in `__init__`
- [ ] B) Each suite gets its own list, so the code works as intended
- [ ] C) Both suites share one class-level list, so each suite sees both test cases
- [ ] D) The list is copied on every call, so the cases are lost

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `cases = []` in the class body creates one list shared by every suite, and `self.cases.append(...)` changes that one list in place. The fix is to create `self.cases = []` inside `__init__` so each suite gets a new list.
- **Why others are wrong:**
  - A) `self.cases` finds the class variable through the lookup (instance, then class), so no error occurs.
  - B) That is exactly the misconception; per-object lists must be created in `__init__`.
  - D) `append` modifies the existing shared list in place and nothing is copied or lost.
</details>

---

### Question 9

You need `TestCase.from_csv_line("TC-003,Search,High")` to build a test case from a line of text, and it should also create the right type when called on a subclass such as `UITest`. Which kind of method should it be?

- [ ] A) An instance method, because it creates an object
- [ ] B) A class method (`@classmethod`) that returns `cls(...)`
- [ ] C) A static method (`@staticmethod`) that returns `TestCase(...)`
- [ ] D) A plain method with no decorator that takes no parameters

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** A class method receives the class as `cls`, so it works as an alternative constructor (factory method), and `cls(...)` creates the subclass type when called through a subclass.
- **Why others are wrong:**
  - A) An instance method needs an existing object (`self`), but here no object exists yet.
  - C) A static method receives neither the object nor the class, and hard-coding `TestCase(...)` would wrongly give subclasses parent objects.
  - D) Without the decorator and without parameters, calling it would fail because Python would pass the object or class automatically.
</details>

---

### Question 10

A teammate is creating a Page Object class for the login screen of the application under test. Which class name follows the naming convention taught in the course?

- [ ] A) `login_page`
- [ ] B) `Login_Page`
- [ ] C) `LoginPage`
- [ ] D) `loginPage`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Class names use CapWords (PascalCase): each word starts with a capital letter and there are no underscores, as in `TestCase` or `LoginPage`. This lets you tell classes apart from `snake_case` variables and functions at a glance.
- **Why others are wrong:**
  - A) `snake_case` is the style for variables, functions, methods and attributes, not classes.
  - B) CapWords uses no underscores between words.
  - D) The first word must also start with a capital letter, otherwise it is not CapWords.
</details>

---

### Question 11

You are modelling test cases in a framework. Which situation is the strongest sign that a class is a better choice than a dictionary plus loose functions?

- [ ] A) Several pieces of data and several functions keep travelling together, and you want rules about valid states
- [ ] B) You need a quick, one-off record that you will use once and discard
- [ ] C) You need a single operation that keeps no state between calls
- [ ] D) You have a fixed, simple record that never changes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Classes are the right tool when data and behaviour belong together, there are many similar things, and there are rules about valid states. A test case with an ID, a status and methods like `mark_passed()` is exactly that.
- **Why others are wrong:**
  - B) A quick, one-off record is the typical use of a dictionary.
  - C) A single operation with no state is simply a function.
  - D) A fixed, simple record that never changes suits a `namedtuple` or tuple.
</details>

---

### Question 12

A `TestCase` object has no `owner` attribute. What does `getattr(case, "owner", "n/a")` do?

- [ ] A) Raises `AttributeError`
- [ ] B) Returns `None`
- [ ] C) Creates an `owner` attribute on the object with the value `"n/a"`
- [ ] D) Returns `"n/a"` and leaves the object unchanged

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `getattr` with a third argument reads an attribute and falls back to that default when it is missing, much like `dict.get`. It only reads, so the object is not modified.
- **Why others are wrong:**
  - A) The error appears only with plain `case.owner` or `getattr` without a default.
  - B) The supplied default (`"n/a"`) is returned, not `None`.
  - C) Creating or changing an attribute by name is the job of `setattr`, not `getattr`.
</details>

---

### Question 13

Python executes `TestCase("TC-001", "Valid login")` for a class that defines `__init__(self, test_id, title)`. Which description of what happens is correct?

- [ ] A) `__init__` runs first on the class, and the object is created afterwards from whatever it set up
- [ ] B) A new empty object is created, then `__init__` is called with that object as `self` plus the two arguments
- [ ] C) The two arguments are stored on the object automatically, and `__init__` then runs only to validate them
- [ ] D) `__init__` builds the object and must `return` it so that `case_1` receives it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Python first creates a new empty object, then calls `__init__` passing that object as `self` and the other arguments as parameters. Inside `__init__`, `self.id = test_id` stores values on the object, and the finished object is returned to the caller.
- **Why others are wrong:**
  - A) The object exists before `__init__` runs; `__init__` only initialises it.
  - C) Nothing is stored automatically; you must assign `self.id = test_id` yourself.
  - D) `__init__` should not return a value (it implicitly returns `None`); Python hands back the object itself.
</details>

---

### Question 14

A trainee writes `def __init__(self, test_id, title, tags=[])` so that each test case can have tags. Which fix does the course recommend?

- [ ] A) Keep `tags=[]` and add a comment asking teammates not to modify it
- [ ] B) Declare `tags = []` in the class body so it is defined in one place
- [ ] C) Use `tags=None` and write `self.tags = [] if tags is None else list(tags)`
- [ ] D) Keep `tags=[]` and write `self.tags = tags` so the caller's list is used directly

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** A mutable default is created once and shared, so the course says never to write `tags=[]`. Using `None` and creating a fresh list (or a copy with `list(tags)`) inside `__init__` gives every object its own list.
- **Why others are wrong:**
  - A) A comment does not stop the shared default list from being reused by every object.
  - B) A list in the class body is shared by all objects, which is the mutable class variable trap.
  - D) That keeps the shared default and also shares the caller's own list; `list(tags)` makes a copy instead.
</details>

---

### Question 15

A test script contains this line on a `TestCase` object created with a normal constructor that sets `status`:

```python
case.staus = "PASS"
```

What happens, and what is the consequence for the report?

- [ ] A) A brand-new attribute `staus` is silently created, and `case.status` is unchanged (still `"NOT RUN"`)
- [ ] B) Python raises `AttributeError` because `staus` does not exist
- [ ] C) Python corrects the typo and updates `status`
- [ ] D) Python raises a `SyntaxError` before the script runs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Python allows attributes to be added to an object at any time, so a typo silently creates a new attribute instead of failing. The real `status` stays as it was, which is one reason to define attributes in `__init__` and use a validated property where rules exist.
- **Why others are wrong:**
  - B) `AttributeError` appears when you read a missing attribute, not when you assign to a new name.
  - C) Python never guesses or corrects names.
  - D) The line is valid syntax; the problem is a logic bug, not a syntax error.
</details>

---

### Question 16

`UITest` inherits from `TestCase`, and `TestCase` defines this factory:

```python
@classmethod
def from_dict(cls, data):
    return cls(data["id"], data["title"])
```

When you call `UITest.from_dict({...})`, what does `cls` refer to inside the method?

- [ ] A) `TestCase`, because that is where the method is defined
- [ ] B) The new object being created
- [ ] C) The string `"UITest"`
- [ ] D) `UITest`, the class the method was called through

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** When a subclass calls an inherited class method, `cls` is the subclass, not the parent. That is why `cls(...)` builds a `UITest`, which a static method (or hard-coded `TestCase(...)`) could not do.
- **Why others are wrong:**
  - A) That would be true only if the method were called through `TestCase`; the calling class is what counts.
  - B) The object (instance) is what `self` refers to in instance methods; a class method receives the class.
  - C) `cls` is the class itself, not its name; the name is available as `cls.__name__`.
</details>

---

### Question 17

You are designing a `TestCase` class. Which piece of data is the best candidate for a **class variable** rather than an instance variable?

- [ ] A) Each test's current `status`
- [ ] B) Each test's `failure_reason`
- [ ] C) The tuple of valid status names (`"NOT RUN"`, `"PASS"`, `"FAIL"`, `"SKIPPED"`) used by every test
- [ ] D) Each test's own history of status changes (a list)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Ask "would two different objects ever need different values?" The valid status names are the same for every test case, so one shared copy at class level (an `UPPER_CASE` constant) is ideal.
- **Why others are wrong:**
  - A) Status differs from test to test, so it is an instance variable.
  - B) A failure reason belongs to one particular test, so it is per-object data.
  - D) A list that each object needs its own copy of must be created in `__init__`, not shared in the class body.
</details>

---

### Question 18

Given `print(case.valid_statuses)`, in which order does Python search for `valid_statuses`?

- [ ] A) The instance, then the instance's class, then the parent classes
- [ ] B) The class, then the instance, then the parent classes
- [ ] C) The parent classes, then the class, then the instance
- [ ] D) The class only; instances never store their own attributes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Python stops at the first match in this order: the instance (`case.__dict__`), the instance's class, then the parent classes following the MRO. This lookup order explains shadowing and inheritance of class variables.
- **Why others are wrong:**
  - B) The instance is always checked before the class, which is why an instance assignment can shadow a class variable.
  - C) Parents are searched last, so a child's own value wins over the parent's.
  - D) Instances do store their own attributes (see `case.__dict__`), and those are checked first.
</details>

---

### Question 19

`chrome` and `firefox` are `Browser` objects, and `Browser.default_timeout` is a class variable equal to `60`. A test then runs `chrome.default_timeout = 5`. What is the effect?

- [ ] A) Every `Browser` object now has a timeout of 5
- [ ] B) A new instance variable is created on `chrome` only; `firefox` and `Browser.default_timeout` still give 60
- [ ] C) The class variable becomes 5, but only `chrome` sees the change
- [ ] D) `AttributeError`, because class variables are read-only through an instance

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Assigning through an object never changes a class variable; it creates a new instance variable that shadows the class one for that object only. Use `Browser.default_timeout = 5` to change the shared value for everyone.
- **Why others are wrong:**
  - A) Only an assignment through the class name changes the shared value.
  - C) The class variable is untouched; the new value lives on the `chrome` instance.
  - D) Assignment is allowed; it just creates an instance variable instead of modifying the class one.
</details>

---

### Question 20

Your automated tests pass when run one at a time but some fail when the whole suite runs. You discover a `TestSession` class with a class-level `results = []` that every test appends to. What is the likely cause and the best remedy?

- [ ] A) Python caches the list between tests, so restart the interpreter between each test
- [ ] B) The list is copied for each test, so use a deeper copy
- [ ] C) Class variables are slower than instance variables, so tests time out; raise the timeouts
- [ ] D) Shared mutable class-level state leaks between tests; prefer per-object (instance) state, or reset the shared state between tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Shared mutable state at class level is a favourite source of flaky tests, because an earlier test changes something a later test relies on. The remedies are to prefer instance state and, if class-level counters or registries are unavoidable, to reset them between tests.
- **Why others are wrong:**
  - A) Nothing is cached; the one list simply persists on the class and everything appends to it.
  - B) The list is not copied at all; every test shares the single class-level list.
  - C) Speed is not the issue; the problem is test results depending on run order.
</details>

---

### Question 21

A class stores a value as `self.__balance`. From outside the class, which expression can still read it, given `acc = Account("Priya", 100)`?

- [ ] A) `acc.__balance`
- [ ] B) `acc._Account__balance`
- [ ] C) `acc._balance`
- [ ] D) `acc.balance__`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Double leading underscores trigger name mangling: Python silently renames the attribute to `_ClassName__name`, here `_Account__balance`. It is awkward to reach but not truly private, so it must never be used to protect secrets.
- **Why others are wrong:**
  - A) The original name no longer exists, so this raises `AttributeError`.
  - C) A different name; no such attribute was created.
  - D) A trailing double underscore is not how mangling renames attributes.
</details>

---

### Question 22

A `TestResult` class has a validated `duration` property. In `__init__`, the trainee writes `self.duration = duration` rather than `self._duration = duration`. Why is this the recommended choice?

- [ ] A) The assignment goes through the property setter, so construction is validated too
- [ ] B) It is faster than assigning to the underscored attribute
- [ ] C) Python requires it, otherwise the property is never created
- [ ] D) It stores the value under the public name, so the getter and setter no longer need `_duration`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Assigning through the public name runs the setter, so `TestResult("TC-002", -3)` is rejected with `ValueError` just like `result.duration = -3`. Assigning `self._duration` directly in `__init__` would bypass the validation.
- **Why others are wrong:**
  - B) Speed is not the reason; the goal is validation.
  - C) The property exists because of the decorators, regardless of how `__init__` assigns.
  - D) The real data is still stored in `_duration`; storing it as `self.duration` inside the setter would cause infinite recursion.
</details>

---

### Question 23

A `TestSuite` has this property, and an outside script runs `suite.tests.append("garbage")`, bypassing `add()`:

```python
@property
def tests(self):
    return self._tests
```

What is the best fix?

- [ ] A) Rename `_tests` to `__tests` so nobody can reach it
- [ ] B) Remove the property and make `tests` a plain public attribute
- [ ] C) Add a comment saying "do not append to this list"
- [ ] D) Return a copy (`list(self._tests)`) or a tuple, so callers must use `add()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Returning the internal list itself leaks it, so outsiders can bypass your rules. Returning a copy or an immutable tuple means appending to the result changes only a throw-away copy, and callers have to use `add()`, which can validate input.
- **Why others are wrong:**
  - A) The property would still return the real list, and `__` mangling is only awkwardness, not protection.
  - B) That exposes the list even more directly.
  - C) A comment is not enforced; anyone can still modify the list.
</details>

---

### Question 24

Two separate `TestCase` objects are created with `p = TestCase()` and `q = TestCase()`, and the class does not define `__eq__`. Which expression evaluates to `True`?

- [ ] A) `p == q`
- [ ] B) `p is q`
- [ ] C) `p is p`
- [ ] D) `p == q and p is q`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `is` checks identity, and an object is always the same object as itself. For simple custom classes `==` defaults to identity, so two different objects are not equal even if they hold the same data.
- **Why others are wrong:**
  - A) `==` defaults to identity here, and `p` and `q` are different objects.
  - B) `p` and `q` are two separate objects, so they are not identical.
  - D) Both parts are `False`, so the combined expression is `False`.
</details>

---

### Question 25

Which design best models the relationship between a test suite and its test cases?

- [ ] A) `class TestSuite(list):`
- [ ] B) `class TestSuite:` with `self.tests = []` created in `__init__`
- [ ] C) `class TestSuite(TestCase):`
- [ ] D) `class TestCase(TestSuite):`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** A suite **has** test cases, which is a "has-a" relationship, so it calls for composition: store the tests as an attribute. Inheritance is for "is-a" relationships such as a `UITest` is a `TestCase`.
- **Why others are wrong:**
  - A) The course calls this a bad idea: a suite is not really "a list".
  - C) A suite is not a kind of test case, so "is-a" does not hold.
  - D) A test case is not a kind of suite either; the relationship is "has-a", not "is-a".
</details>

---

### Question 26

A `TestSuite.run_all()` loops over its tests and calls `test.run()`. Your team adds a new `DatabaseTest` class with its own `run()` method. What must change in `TestSuite`?

- [ ] A) Add an `elif isinstance(test, DatabaseTest):` branch to `run_all`
- [ ] B) Rewrite `run_all` so that it knows about all three kinds of test
- [ ] C) Add `DatabaseTest` to the body of the `TestSuite` class
- [ ] D) Nothing; write the new class with its own `run()` and add instances to the suite

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Because the suite relies only on the shared interface (`run()`, `summary()`, `status`), polymorphism means the same call works for any new kind of test. Adding a new kind of test requires no change to the loop at all.
- **Why others are wrong:**
  - A) `isinstance` chains defeat polymorphism and would have to be edited for every new kind of test.
  - B) Nothing needs rewriting, since the loop does not care which kind each test is.
  - C) A suite holds test objects (composition); it does not need the class defined inside it.
</details>

---

### Question 27

`TestCase.run()` is written as `raise NotImplementedError("Subclasses must implement run()")`. A subclass `BrokenTest(TestCase)` forgets to override `run`. What happens on `BrokenTest("X-1", "oops").run()`?

- [ ] A) `NotImplementedError` is raised straight away with the clear message
- [ ] B) It silently returns `None` and the test is marked as passed
- [ ] C) Python refuses to create the `BrokenTest` object at all
- [ ] D) The parent's generic `run` executes and marks the test as `PASS`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The child inherits the parent's `run`, which deliberately raises an error, so the problem shows up immediately with a clear message instead of a mysterious failure later. This is the simple "required method" convention.
- **Why others are wrong:**
  - B) The inherited method raises an error; it does not return quietly.
  - C) With this convention, creating the object works; only the `abc` module can prevent creating incomplete objects.
  - D) In this version of the base class there is no generic behaviour; `run` just raises.
</details>

---

### Question 28

`Suite.is_valid_name(name)` checks whether a piece of text is an acceptable suite name. It needs no particular suite and no class data, and it is closely tied to `Suite`. Which kind of method fits best?

- [ ] A) An instance method taking `self`
- [ ] B) A class method taking `cls`
- [ ] C) A static method (`@staticmethod`)
- [ ] D) It must always be a module-level function

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The decision guide asks what the method needs: an object (`self`), the class (`cls`), or nothing. It needs neither, and it is closely tied to this class, so a static method keeps the helper with the class it belongs to.
- **Why others are wrong:**
  - A) There is no particular suite whose data is needed, so `self` would be unused.
  - B) The method does not read class variables or create objects of the class, so `cls` is not needed.
  - D) A module-level function is the better choice only for general-purpose helpers used by many unrelated classes.
</details>

---

## Part 2: True/False

### Question 29

**True or False:** In Python, two separate `TestCase` objects holding identical attribute values are considered equal by `==` by default (for a simple class that does not define `__eq__`).

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** For simple custom classes, `==` defaults to identity unless the class defines its own equality. Two separate objects are not equal just because they look alike.
</details>

---

### Question 30

**True or False:** If `ui` is a `UITest` object and `UITest` inherits from `TestCase`, then `type(ui) == TestCase` evaluates to `True`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `type()` returns the exact class only and ignores inheritance, so it gives `UITest`. That is why `isinstance(ui, TestCase)` is preferred, because it respects inheritance and returns `True`.
</details>

---

### Question 31

**True or False:** An attribute named with two leading underscores, such as `self.__balance`, is truly private and cannot be accessed from outside the class in any way.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Double underscores only trigger name mangling: Python renames the attribute to `_ClassName__balance`, which is still reachable if you really want it. It is meant mainly to avoid name clashes in subclasses, not for security.
</details>

---

### Question 32

**True or False:** Inside a factory class method, it makes no difference whether you write `return cls(...)` or `return TestCase(...)`; subclasses such as `UITest` will get `UITest` objects either way.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Through a subclass, `cls` is the subclass, so `cls(...)` builds a `UITest`. Hard-coding `TestCase(...)` would wrongly give subclasses plain parent objects.
</details>

---

### Question 33

**True or False:** After `y = x` (where `x` is a `TestCase` object), setting `y.status = "PASS"` leaves `x.status` unchanged because `y` is a copy.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Assignment is not a copy: `y` and `x` are two names for the same object, so the change is visible through both and `x is y` is `True`. To get an independent object you must create a new one.
</details>

---

### Question 34

**True or False:** It is fine to create `failure_reason` for the first time inside `mark_failed`, because every `TestCase` object will have the attribute afterwards.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Only objects on which `mark_failed` has been called get the attribute, so other objects raise `AttributeError` when it is read. The rule is to define all of an object's attributes in `__init__` (for example `self.failure_reason = ""`).
</details>

---

### Question 35

**True or False:** If a class defines `__repr__` but no `__str__`, then `print(obj)` shows the `__repr__` text.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** When only `__repr__` is defined, Python also uses it for `print`, which is why the course advises defining `__repr__` if you only define one. The default `<... object at 0x...>` text appears only when neither is defined.
</details>

---

### Question 36

**True or False:** Writing `chrome.default_timeout = 5` changes the timeout of every `Browser` object, because `default_timeout` is a class variable.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Assigning through an object never changes a class variable; it creates an instance variable that shadows the class one for that object only. To change the shared value, assign through the class: `Browser.default_timeout = 5`.
</details>

---

### Question 37

**True or False:** A class variable holding a tuple of valid statuses is safe to share between objects, because a tuple cannot be changed in place; the shared-data trap comes from mutable values such as lists.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Immutable class variables (numbers, strings, tuples) can only be rebound, not altered in place, and rebinding through an instance creates a shadow instead of changing the shared value. Lists, dictionaries and sets in the class body are the ones that leak between objects.
</details>

---

### Question 38

**True or False:** If `pass_rate` is a computed `@property` with no setter, then `suite.pass_rate = 50` stores 50 and overrides the calculation.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A property without a setter cannot be assigned, so this line raises `AttributeError`. That is a benefit: the value is always calculated from the results, so nobody can set it to a nonsense value.
</details>

---

### Question 39

**True or False:** Python raises an `AttributeError` when code outside a class reads an attribute named with a single leading underscore, such as `suite._tests`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A single leading underscore is only a convention that says "internal, please don't touch"; it is not enforced. Anyone who accesses it is knowingly ignoring the warning.
</details>

---

### Question 40

**True or False:** If a child class does not define its own `__init__`, the parent's `__init__` runs automatically when a child object is created.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The child inherits everything from the parent, including its constructor, so `UITest("UI-001", "Login")` works even when `UITest` has no code of its own. The parent's setup is skipped only when the child defines its own `__init__` without calling `super().__init__(...)`.
</details>

---

### Question 41

**True or False:** Polymorphism only works when the classes involved inherit from a common parent class.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Python uses duck typing: if an object has the method being called, it works, even if the classes share no parent. Inheritance is one way to get polymorphism, and simply having the right methods is another.
</details>

---

### Question 42

**True or False:** A static method can only be called through the class itself; calling it through an instance raises an error.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A static method can be called on the class or on an instance and behaves the same, because `self` is not passed either way. For example, both `TestCase.is_valid_id("TC-007")` and `case.is_valid_id("TC-099")` work.
</details>

---

## Part 3: Code Prediction

### Question 43

What does this code print?

```python
class TestCase:
    pass

x = TestCase()
x.status = "NOT RUN"
y = x
y.status = "PASS"
z = TestCase()
z.status = "PASS"
print(x.status, x is y, x == z)
```

- [ ] A) `NOT RUN True False`
- [ ] B) `PASS True False`
- [ ] C) `PASS False False`
- [ ] D) `PASS True True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `y = x` is not a copy: both names refer to the same object, so setting `y.status` changes `x.status` and `x is y` is `True`. `z` is a different object, and `==` defaults to identity, so `x == z` is `False`.
- **Why others are wrong:**
  - A) That would require `y` to be a copy; assignment only creates a second name.
  - C) `x is y` is `True` because they are the same object.
  - D) `x == z` is `False` because separate objects are not equal by default.
</details>

---

### Question 44

What does this code print?

```python
class TestResult:
    def __init__(self, test_id, status):
        self.test_id = test_id
        self.status = status

    def __str__(self):
        return f"{self.test_id}: {self.status}"

    def __repr__(self):
        return f"TestResult({self.test_id!r}, {self.status!r})"


r = TestResult("TC-001", "PASS")
print(r)
print([r])
```

- [ ] A) `TC-001: PASS` then `[TestResult('TC-001', 'PASS')]`
- [ ] B) `TestResult('TC-001', 'PASS')` then `[TestResult('TC-001', 'PASS')]`
- [ ] C) `TC-001: PASS` then `[TC-001: PASS]`
- [ ] D) `TC-001: PASS` then `[<__main__.TestResult object at 0x...>]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `print(r)` uses `__str__` when it exists, giving the readable text. Inside a list, Python uses `__repr__`, giving the developer-style form with quoted values.
- **Why others are wrong:**
  - B) When both exist, `print` of a single object uses `__str__`, not `__repr__`.
  - C) List items are displayed with `__repr__`, not `__str__`.
  - D) The default object text only appears when `__repr__` is not defined.
</details>

---

### Question 45

What does this code print?

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

    def summary(self):
        return f"{self.id} [{self.status}]"


class UITest(TestCase):
    def __init__(self, test_id, title, browser="Chrome"):
        super().__init__(test_id, title)
        self.browser = browser

    def summary(self):
        return super().summary() + f" ({self.browser})"


t = UITest("UI-001", "Login", "Firefox")
print(t.summary())
print(isinstance(t, TestCase), type(t) == TestCase)
```

- [ ] A) `UI-001 [NOT RUN] (Firefox)` then `True True`
- [ ] B) `UI-001 [NOT RUN]` then `True False`
- [ ] C) `UI-001 [NOT RUN] (Firefox)` then `True False`
- [ ] D) `UI-001 [NOT RUN] (Firefox)` then `False False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The child's `summary` calls `super().summary()` to get the parent's text and then appends the browser. `isinstance` respects inheritance (`True`), while `type(t) == TestCase` compares the exact class only (`False`).
- **Why others are wrong:**
  - A) `type(t)` is `UITest`, so comparing it to `TestCase` is `False`.
  - B) The overriding `summary` in `UITest` is used, so the browser text is appended.
  - D) A `UITest` is a `TestCase`, so `isinstance` is `True`.
</details>

---

### Question 46

What does this code print?

```python
class TestCase:
    def run(self):
        return "generic"


class UITest(TestCase):
    def run(self):
        return "ui"


class APITest(TestCase):
    pass


tests = [TestCase(), UITest(), APITest()]
print([t.run() for t in tests])
```

- [ ] A) `['generic', 'generic', 'generic']`
- [ ] B) `['generic', 'ui', 'ui']`
- [ ] C) `['ui', 'ui', 'ui']`
- [ ] D) `['generic', 'ui', 'generic']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Python looks for `run` in the object's own class first. `UITest` overrides it, while `APITest` has none of its own and inherits the parent's version, so the same call behaves differently per class (polymorphism).
- **Why others are wrong:**
  - A) `UITest` defines its own `run`, which takes priority over the parent's.
  - B) `APITest` does not override `run`, so it uses the parent's `"generic"`.
  - C) Only `UITest` overrides `run`; the other two classes use `"generic"`.
</details>

---

### Question 47

What does this code print?

```python
class TestResult:
    def __init__(self, test_id, duration):
        self.test_id = test_id
        self._retries = 0
        self.__duration = duration


result = TestResult("TC-001", 1.5)
print(result.__dict__)
print(result._TestResult__duration)
print(hasattr(result, "__duration"))
```

- [ ] A) `{'test_id': 'TC-001', '_retries': 0, '__duration': 1.5}` then `1.5` then `True`
- [ ] B) `{'test_id': 'TC-001', '_retries': 0, '_TestResult__duration': 1.5}` then `1.5` then `False`
- [ ] C) `{'test_id': 'TC-001', '_retries': 0, '_TestResult__duration': 1.5}` then an `AttributeError`
- [ ] D) `{'test_id': 'TC-001'}` then `1.5` then `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Name mangling stores `__duration` as `_TestResult__duration`, and `_retries` stays unchanged because a single underscore is only a convention. The mangled name is still reachable (`1.5`), but the original name `__duration` does not exist, so `hasattr` returns `False`.
- **Why others are wrong:**
  - A) Python renames the double-underscore attribute, so `__duration` does not appear in `__dict__` or satisfy `hasattr`.
  - C) The mangled name works, so no `AttributeError` is raised.
  - D) `__dict__` contains all instance attributes, including `_retries` and the mangled one.
</details>

---

### Question 48

What does this code print?

```python
class RunCounter:
    count = 0

    def increment(self):
        self.count += 1


a = RunCounter()
b = RunCounter()
a.increment()
a.increment()
b.increment()
print(a.count, b.count, RunCounter.count)
```

- [ ] A) `3 3 3`
- [ ] B) `2 1 3`
- [ ] C) `2 1 0`
- [ ] D) `2 2 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `self.count += 1` reads the class value and then assigns to `self.count`, which creates an instance variable that shadows the class variable. So `a` gets 2, `b` gets 1, and `RunCounter.count` never changes from 0.
- **Why others are wrong:**
  - A) That would be the result if the class variable were modified, which requires `RunCounter.count += 1`.
  - B) The class variable is never touched, so it stays at 0, not 3.
  - D) `b` has only been incremented once, so its own instance variable is 1.
</details>

---

### Question 49

What does this code print?

```python
class TestCase:
    timeout = 30


class UITest(TestCase):
    timeout = 60


class APITest(TestCase):
    pass


TestCase.timeout = 45
t = APITest()
t.timeout = 5
print(TestCase.timeout, UITest.timeout, APITest.timeout, t.timeout)
```

- [ ] A) `45 45 45 5`
- [ ] B) `45 60 45 5`
- [ ] C) `45 60 5 5`
- [ ] D) `30 60 30 5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Lookup goes instance, then class, then parents. `UITest` has its own `timeout` (60), `APITest` has none so it follows the parent's new value (45), and `t.timeout = 5` only creates an instance variable on `t` without changing `APITest`.
- **Why others are wrong:**
  - A) `UITest` defines its own value, so it is not affected by changing the parent.
  - C) Assigning through the instance `t` creates a shadow on `t` only; `APITest.timeout` remains 45.
  - D) `TestCase.timeout` was reassigned to 45, and `APITest` follows the parent, so neither is 30.
</details>

---

### Question 50

What does this code print?

```python
class TestCase:
    def __init__(self, test_id):
        self.id = test_id

    @classmethod
    def from_line(cls, line):
        return cls(line.strip().split(",")[0])

    @staticmethod
    def is_valid_id(test_id):
        return test_id.startswith("TC-") and len(test_id) == 6


class UITest(TestCase):
    pass


ui = UITest.from_line("TC-007,Login")
print(type(ui).__name__, ui.id, ui.is_valid_id(ui.id))
```

- [ ] A) `TestCase TC-007 True`
- [ ] B) `UITest TC-007,Login True`
- [ ] C) `UITest TC-007 False`
- [ ] D) `UITest TC-007 True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Called through `UITest`, `cls` is `UITest`, so the factory builds a `UITest`; the line is split on the comma and the first part (`TC-007`) becomes the ID. The static method can be called on an instance too, and `"TC-007"` is valid (starts with `TC-` and has length 6).
- **Why others are wrong:**
  - A) `cls` is the subclass when called through `UITest`, so the type is `UITest`.
  - B) `split(",")[0]` keeps only the first field, so the ID is `TC-007`.
  - C) `"TC-007"` starts with `TC-` and has 6 characters, so the check returns `True`.
</details>

---

### Question 51

What does this code print?

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"


case = TestCase("TC-001", "Login")
case.staus = "PASS"
print(case.status, hasattr(case, "staus"), getattr(case, "owner", "n/a"))
setattr(case, "owner", "Priya")
print(case.__dict__)
```

- [ ] A) `NOT RUN True n/a` then `{'id': 'TC-001', 'title': 'Login', 'status': 'NOT RUN', 'staus': 'PASS', 'owner': 'Priya'}`
- [ ] B) `PASS False n/a` then `{'id': 'TC-001', 'title': 'Login', 'status': 'PASS', 'owner': 'Priya'}`
- [ ] C) `NOT RUN False n/a` then `{'id': 'TC-001', 'title': 'Login', 'status': 'NOT RUN', 'owner': 'Priya'}`
- [ ] D) An `AttributeError` on the `case.staus = "PASS"` line

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The typo `case.staus = "PASS"` creates a brand-new attribute, so `status` stays `"NOT RUN"` and `hasattr(case, "staus")` is `True`. `getattr` returns the default `"n/a"` for the missing `owner`, and `setattr` then adds `owner`, so `__dict__` shows all five attributes.
- **Why others are wrong:**
  - B) The misspelled name does not update `status`, and `hasattr` finds `staus` because the assignment created it.
  - C) `hasattr(case, "staus")` is `True` and `__dict__` includes the stray `staus` attribute.
  - D) Assigning to a new attribute name is allowed, so no error occurs.
</details>

---

### Question 52

What does this code print?

```python
class TestSuite:
    def __init__(self, name, owner="QA"):
        self.name = name
        self.owner = owner
        self.cases = []

    def add_case(self, case):
        self.cases.append(case)
        return self

    def count(self):
        return len(self.cases)


smoke = TestSuite("Smoke")
regression = TestSuite("Regression", owner="Priya")
smoke.add_case("TC-001").add_case("TC-002")
regression.add_case("TC-100")
print(smoke.count(), regression.count(), smoke.owner, regression.owner)
print(smoke.cases[1])
```

- [ ] A) `3 3 QA Priya` then `TC-002`
- [ ] B) `2 1 QA QA` then `TC-002`
- [ ] C) `2 1 QA Priya` then `TC-002`
- [ ] D) `2 1 QA Priya` then `TC-001`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Each suite creates its own `cases` list in `__init__`, so `smoke` holds 2 cases and `regression` holds 1. `add_case` returns `self`, which makes the chained call work. The default `owner="QA"` applies to `smoke`, while `regression` was given `"Priya"`, and `smoke.cases[1]` is the second case.
- **Why others are wrong:**
  - A) The lists are not shared, because `self.cases = []` runs separately for every suite.
  - B) `regression` was created with `owner="Priya"`, so its owner is not the default.
  - D) Index `1` is the second item, `"TC-002"`, not the first.
</details>

---

### Question 53

What does this code print?

```python
class TestCase:
    total_created = 0

    def __init__(self, test_id):
        self.id = test_id
        TestCase.total_created += 1


class UITest(TestCase):
    def __init__(self, test_id, browser):
        super().__init__(test_id)
        self.browser = browser


class APITest(TestCase):
    pass


TestCase("TC-001")
UITest("UI-001", "Firefox")
a = APITest("API-001")
print(TestCase.total_created, UITest.total_created, a.total_created)
print("total_created" in a.__dict__)
```

- [ ] A) `1 1 1` then `False`
- [ ] B) `3 1 1` then `False`
- [ ] C) `3 3 3` then `True`
- [ ] D) `3 3 3` then `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `UITest` calls `super().__init__`, and `APITest` inherits `__init__`, so all three constructions run `TestCase.total_created += 1` on the shared counter, giving 3. Reading `UITest.total_created` or `a.total_created` finds the class variable through attribute lookup, and nothing was ever assigned on `a`, so it is not in `a.__dict__`.
- **Why others are wrong:**
  - A) The counting line runs for every object because the subclasses' constructors reach `TestCase.__init__`.
  - B) `UITest` has no counter of its own, so it follows the parent through the lookup and also reports 3.
  - C) The counter was changed through the class name, so no instance variable was created on `a`.
</details>

---

### Question 54

What does this code print?

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self._tests = []

    def add(self, status):
        self._tests.append(status)

    @property
    def tests(self):
        return list(self._tests)

    @property
    def pass_rate(self):
        if not self._tests:
            return 0.0
        return self._tests.count("PASS") / len(self._tests) * 100


suite = TestSuite("Smoke")
suite.add("PASS")
suite.add("FAIL")
suite.add("PASS")
suite.tests.append("garbage")
print(len(suite.tests), f"{suite.pass_rate:.1f}%")
suite.add("FAIL")
print(len(suite.tests), f"{suite.pass_rate:.0f}%")
```

- [ ] A) `3 66.7%` then `4 50%`
- [ ] B) `4 66.7%` then `5 50%`
- [ ] C) `3 66.7%` then `3 67%`
- [ ] D) An `AttributeError` on the `suite.tests.append("garbage")` line

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The `tests` property returns a copy, so appending `"garbage"` changes only a throw-away list and the suite still holds 3 results (2 of 3 passed, 66.7%). After another `add`, there are 4 results and `pass_rate`, being computed on demand, gives 2 of 4 = 50%.
- **Why others are wrong:**
  - B) The garbage was added to a copy, not to the suite's internal list.
  - C) The suite now holds 4 results, and a computed property is recalculated every time, so the rate is 50%.
  - D) `append` modifies the returned list; it is not an assignment to the property, so no error occurs.
</details>

---

### Question 55

What does this code print?

```python
class User:
    def __init__(self, username, role="viewer"):
        self.username = username
        self.role = role

    @classmethod
    def admin(cls, username="admin"):
        return cls(username, role="admin")

    @classmethod
    def guest(cls):
        return cls("guest", role="viewer")

    def __repr__(self):
        return f"{type(self).__name__}({self.username!r}, role={self.role!r})"


class TrialUser(User):
    pass


print(User.admin())
print(TrialUser.admin("priya"))
print([User.guest(), User("bob")])
```

- [ ] A) `User('admin', role='admin')`, then `User('priya', role='admin')`, then `[User('guest', role='viewer'), User('bob', role='viewer')]`
- [ ] B) `User('admin', role='admin')`, then `TrialUser('priya', role='admin')`, then `[<__main__.User object at 0x...>, <__main__.User object at 0x...>]`
- [ ] C) `TrialUser('admin', role='admin')`, then `TrialUser('priya', role='admin')`, then `[User('guest', role='viewer'), User('bob', role='viewer')]`
- [ ] D) `User('admin', role='admin')`, then `TrialUser('priya', role='admin')`, then `[User('guest', role='viewer'), User('bob', role='viewer')]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Called through `User`, `cls` is `User`; called through `TrialUser`, `cls` is the subclass, so the factory builds a `TrialUser` and `type(self).__name__` reports it. `User.guest()` and `User("bob")` are plain `User` objects, shown with `__repr__` inside the list.
- **Why others are wrong:**
  - A) `TrialUser.admin("priya")` creates a `TrialUser` because `cls` is the subclass.
  - B) The class defines `__repr__`, which is what list items use, so the default object text does not appear.
  - C) `User.admin()` is called through `User`, so `cls` is `User`, not `TrialUser`.
</details>

---

### Question 56

What does this code print?

```python
class Report:
    format_name = "text"

    def __init__(self, title):
        self.title = title

    def header(self):
        return f"== {self.title} =="

    @classmethod
    def with_default_title(cls):
        return cls("Untitled")

    @classmethod
    def describe_format(cls):
        return f"Format: {cls.format_name}"

    @staticmethod
    def underline(text):
        return "-" * len(text)


class HtmlReport(Report):
    format_name = "html"


r = Report.with_default_title()
print(r.header(), Report.underline(r.header()))
print(HtmlReport.describe_format(), type(HtmlReport.with_default_title()).__name__)
```

- [ ] A) `== Untitled == --------------` then `Format: text Report`
- [ ] B) `== Untitled == --------------` then `Format: html Report`
- [ ] C) `== Untitled == --------------` then `Format: html HtmlReport`
- [ ] D) `== Untitled == --------------` then `Format: text HtmlReport`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `HtmlReport` overrides `format_name`, and the class method `describe_format` reads it through `cls`, so it prints `html`. `with_default_title` returns `cls(...)`, so called through `HtmlReport` it builds an `HtmlReport`. The static `underline` just returns one dash per character of the 14-character header.
- **Why others are wrong:**
  - A) Both parts are wrong: `cls` is `HtmlReport`, so its own `format_name` and its own type are used.
  - B) The factory uses `cls(...)`, so the object is an `HtmlReport`, not a plain `Report`.
  - D) `HtmlReport` defines its own `format_name = "html"`, which takes priority over the parent's value.
</details>

---

### Question 57

What does this code print?

```python
class TestCase:
    def run(self):
        print("generic")


class APITest(TestCase):
    def run(self):
        print("sending request")


class TimedAPITest(APITest):
    def run(self):
        print("start timer")
        super().run()
        print("stop timer")


t = TimedAPITest()
t.run()
print(issubclass(TimedAPITest, TestCase), issubclass(TestCase, TimedAPITest))
print([c.__name__ for c in TimedAPITest.__mro__])
```

- [ ] A) `start timer / sending request / stop timer`, then `True False`, then `['TimedAPITest', 'APITest', 'TestCase', 'object']`
- [ ] B) `start timer / generic / stop timer`, then `True False`, then `['TimedAPITest', 'APITest', 'TestCase', 'object']`
- [ ] C) `sending request`, then `True False`, then `['TimedAPITest', 'APITest', 'TestCase', 'object']`
- [ ] D) `start timer / sending request / stop timer`, then `True True`, then `['TimedAPITest', 'APITest', 'TestCase', 'object']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `super().run()` inside `TimedAPITest` calls the next class in the MRO, `APITest.run`, which prints `sending request`, so the timer messages wrap around it. A subclass is a subclass of its ancestor (`True`) but not the other way round (`False`), and `__mro__` lists the lookup chain: child, parent, grandparent, `object`.
- **Why others are wrong:**
  - B) `APITest` overrides `run`, so `super().run()` reaches its version, not the generic one in `TestCase`.
  - C) The override prints its own messages and then also runs the parent's version via `super()`.
  - D) `issubclass(TestCase, TimedAPITest)` is `False`, because a parent is not a subclass of its child.
</details>

---

### Question 58

What does this code print?

```python
class ManualTest:
    def run(self):
        return "human"


class RobotTest:
    def run(self):
        return "robot"


class Dashboard:
    pass


tests = [ManualTest(), RobotTest()]
print([t.run() for t in tests])
print(isinstance(tests[0], RobotTest), hasattr(tests[1], "run"), hasattr(Dashboard(), "run"))
```

- [ ] A) `['human', 'robot']` then `True True False`
- [ ] B) `['human', 'robot']` then `False True False`
- [ ] C) An `AttributeError`, because `ManualTest` and `RobotTest` share no parent class
- [ ] D) `['human', 'robot']` then `False True True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Duck typing means both objects work in the list comprehension because each has a `run()` method, even though they share no parent. `isinstance` is `False` because a `ManualTest` is not a `RobotTest`, `hasattr` is `True` for `RobotTest`, and `Dashboard` has no `run`, so its `hasattr` is `False`.
- **Why others are wrong:**
  - A) `tests[0]` is a `ManualTest`, which is not an instance of the unrelated `RobotTest`.
  - C) Polymorphism works through duck typing: having the right method is enough, no shared parent is needed.
  - D) `Dashboard` defines no `run` method, so `hasattr(Dashboard(), "run")` is `False`.
</details>

---

## Part 4: Fill-in-the-Blank

### Question 59

In Python, the constructor method that runs automatically every time a new object is created is named `____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__init__`

**Explanation:** `__init__` (two underscores, `init`, two underscores) initialises the new object by setting its starting attributes. It always takes `self` first and should not return a value.
</details>

---

### Question 60

To add validation when a value is assigned, you define a getter with `@property` and then a setter with the decorator `@duration.____` on a method of the same name.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `setter`

**Explanation:** The setter is written as `@duration.setter` and must use the same method name as the property getter. The real data is stored in a differently named internal attribute such as `_duration`.
</details>

---

### Question 61

To count how many `TestCase` objects have been created, the constructor should update the shared class variable with `____.total_created += 1` rather than `self.total_created += 1`, which would create a shadowing instance variable.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `TestCase` (the class name)

**Explanation:** To modify a class variable, always use the class name. Assigning through `self` creates an instance variable that shadows the class one, leaving the shared counter unchanged.
</details>

---

### Question 62

A helper such as `is_valid_id(test_id)` needs neither the object nor the class, but is closely tied to `TestCase`. You define it inside the class under the `@____` decorator, and it receives no automatic first argument.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `staticmethod`

**Explanation:** `@staticmethod` marks a plain helper function filed inside the class; Python passes neither `self` nor `cls`. It can be called on the class or an instance.
</details>

---

### Question 63

By convention, Python class names such as `TestCase` and `LoginPage` are written in `____` style (also called PascalCase).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `CapWords`

**Explanation:** Each word starts with a capital letter and there are no underscores. This differs from variables and functions, which use `snake_case`, so you can tell them apart at a glance.
</details>

---

### Question 64

In a class method, the first parameter is conventionally named `____`, and it receives the class itself (the subclass when the method is called through one).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `cls`

**Explanation:** Just as `self` is the conventional name for the object in instance methods, `cls` is the conventional name for the class in methods decorated with `@classmethod`. It is what lets a factory call `cls(...)` and build the right type.
</details>

---

### Question 65

To control how an object is displayed inside a list, in the REPL and in debugging output, define the special method `____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `__repr__`

**Explanation:** `__repr__` is the developer-friendly description, conventionally text that looks like the code to recreate the object. If you define only one of the two printing methods, define `__repr__`.
</details>

---

### Question 66

To give each object its own copy of an optional list, a constructor can write `self.tags = [] if tags is None else ____(tags)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `list`

**Explanation:** `list(tags)` makes a copy, so the object does not share the caller's list. Combined with `tags=None` as the default, every object gets a fresh list.
</details>

---

### Question 67

When Python evaluates `case.valid_statuses`, it searches the instance first, then the instance's `____`, then the parent classes, and stops at the first match.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `class`

**Explanation:** This lookup order (instance, then class, then parents) explains why class variables can be read through instances and why an instance assignment shadows a class variable.
</details>

---

### Question 68

By convention, constants stored as class variables, such as `MAX_TITLE_LENGTH` and `VALID_STATUSES`, are written in `____` naming style.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `UPPER_CASE`

**Explanation:** Constants use `UPPER_CASE`, which makes them easy to recognise. Inside methods they can be read with `self.NAME` or `ClassName.NAME`.
</details>

---

### Question 69

A name that starts with two underscores, such as `self.__balance`, triggers name `____`, where Python renames it to `_ClassName__balance`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `mangling`

**Explanation:** Name mangling makes accidental access and accidental overriding by subclasses harder, but the attribute is still reachable under the new name, so it is not real security.
</details>

---

### Question 70

To refuse a negative duration inside a setter, write `raise ____("duration cannot be negative")`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `ValueError`

**Explanation:** `raise ValueError(...)` deliberately stops the program with an error so bad data is rejected the moment it appears, instead of being stored and discovered later.
</details>

---

### Question 71

Inside an overriding method, calling `____().summary()` runs the parent's version so you can extend its behaviour instead of replacing it.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `super`

**Explanation:** `super()` means "the parent class, as seen from this object". It is used both in `__init__` and in overridden methods, for example `super().summary() + f" ({self.browser})"`.
</details>

---

### Question 72

A base class can force subclasses to provide their own `run()` method by making the parent's `run()` raise `____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `NotImplementedError`

**Explanation:** If a subclass forgets to override `run`, the inherited method raises this error immediately with a clear message, which is better than a mysterious failure later.
</details>

---
