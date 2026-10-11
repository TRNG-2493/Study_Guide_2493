# Encapsulation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain encapsulation and why controlling access to an object's data matters.
- Describe how Python signals **public**, **protected** (`_name`) and **private** (`__name`) attributes, and why Python relies on convention.
- Explain name mangling and what `__name` really does.
- Write getter and setter methods, and understand why Python prefers properties.
- Use the `@property` decorator, and `@name.setter`, to expose attributes safely.
- Validate data when it is set, using `raise ValueError`.
- Create read-only and computed properties.
- Design a class with a small public interface and hidden internal details.

---

## Why This Matters

Imagine a `TestSuite` object that keeps a list of test cases and a running count of how many passed. If any code anywhere can write `suite.passed = 9999`, or set a test's status to `"PSAS"`, the object can reach a state that makes no sense: more passes than tests, or a status that no report knows how to handle. The bug may only show up much later, far from the line that caused it.

**Encapsulation** means **keeping an object's internal data protected and only allowing it to be changed through well-defined, controlled routes.** It has two sides:

1. **Bundling** data and the methods that work on it into one unit (the class), which you have been doing since this morning.
2. **Restricting direct access** so the object can protect its own rules (its **invariants**), for example "status is always one of PASS, FAIL or NOT RUN".

**Analogy:** a car's engine is enclosed under the bonnet. You use the steering wheel, pedals and gear stick, a small, safe **interface**, and the car handles the complicated internal details. You *can* open the bonnet and reach in, but you shouldn't need to, and if you do, you accept responsibility for what happens.

For test automation, this matters because test frameworks are used by many people. A well-encapsulated `TestResult` or `Browser` class gives your teammates a clear public interface and the freedom for you to change internal details later without breaking their tests. It's also what makes the Page Object Model work: the test calls `login_page.login(user, password)` and doesn't care how the page finds its fields.

---

## The Concept

### 1. Public, Protected and Private: Python's Conventions

Many languages (Java, C#) have keywords such as `public` and `private` that *enforce* access rules. Python takes a different approach, summed up in its community motto: **"We're all consenting adults here."** Python trusts programmers to respect conventions marked by **underscores**.

| Naming | Called | Meaning | Enforced? |
|---|---|---|---|
| `name` | **Public** | Part of the official interface; use freely | n/a |
| `_name` | **Protected** (internal) | "Internal use; please don't touch from outside the class (or subclasses)" | **No**, convention only |
| `__name` | **Private** | "Really internal to this class"; name is altered to discourage access | Partly (name mangling) |
| `__name__` | **Special** | Python's own hooks (`__init__`, `__str__`) | Never create your own |

#### 1.1 Public attributes

Everything you've written so far is public:

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self.status = "NOT RUN"

case = TestCase("TC-001", "Login")
case.status = "PSAS"          # nothing stops this typo from being stored
```

#### 1.2 Protected: a single leading underscore

A leading underscore is a **signal to other programmers**: "this is an implementation detail; don't use it from outside."

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self._tests = []              # internal list

    def add(self, test):
        self._tests.append(test)

    def count(self):
        return len(self._tests)
```

Nothing prevents `suite._tests.append(...)` from outside, but anyone who does so is knowingly ignoring the warning. Editors and tools respect the convention (for example by not suggesting `_names` in autocomplete or by flagging their use). Subclasses are expected to use protected attributes.

This is the **most common** approach in real Python code: use `_name` for internals.

#### 1.3 Private: double leading underscores and name mangling

Two leading underscores trigger **name mangling**: Python silently renames the attribute to `_ClassName__name`, which makes accidental access (and accidental overriding by subclasses) harder.

```python
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance          # "private"

    def get_balance(self):
        return self.__balance

acc = Account("Priya", 100)

print(acc.owner)               # Priya
print(acc.get_balance())       # 100
print(acc.__balance)           # AttributeError: 'Account' object has no attribute '__balance'
```

Python hides it behind a different name:

```python
print(acc._Account__balance)   # 100  -> still reachable if you really want to
print(acc.__dict__)            # {'owner': 'Priya', '_Account__balance': 100}
```

So double-underscore attributes are **not truly private**; they're just awkward to reach. They are meant mainly to avoid name clashes in subclasses, and are rarely needed. **Beginners should default to a single underscore** for internals, and only use `__` when there is a specific reason.

---

### 2. The Problem With Direct Access

Without protection, validation is impossible:

```python
class TestResult:
    def __init__(self, test_id, duration):
        self.test_id = test_id
        self.duration = duration

result = TestResult("TC-001", 1.5)
result.duration = -20          # nonsense: negative duration. Nothing complains.
```

We want to **check values when they are set**. The traditional technique is to make the attribute internal and provide methods.

---

### 3. Getters and Setters (the Traditional Approach)

A **getter** method returns a value; a **setter** method changes it, after checking it.

```python
class TestResult:
    def __init__(self, test_id, duration):
        self._test_id = test_id
        self._duration = 0.0
        self.set_duration(duration)

    def get_duration(self):
        return self._duration

    def set_duration(self, value):
        if value < 0:
            raise ValueError("duration cannot be negative")
        self._duration = value
```

```python
result = TestResult("TC-001", 1.5)
print(result.get_duration())         # 1.5
result.set_duration(2.0)             # fine
result.set_duration(-5)              # ValueError: duration cannot be negative
```

**`raise ValueError("message")`** deliberately stops the program with an error: here it rejects an invalid value instead of storing it. (You will learn how to *catch* and recover from errors like this later in the program. For now, treat `raise` as "refuse bad data loudly".)

This works, but `result.get_duration()` and `result.set_duration(2.0)` are clunky compared to the clean `result.duration` and `result.duration = 2.0`. Languages such as Java require getters and setters everywhere. Python has a more elegant tool.

> **Python tip:** don't write getters and setters "just in case". Start with a plain public attribute. If you later need validation or a computed value, you can switch to a property **without changing any code that uses the class**, which is the beauty of the next section.

---

### 4. Properties: The Pythonic Way

A **property** lets you write methods but use them like attributes. You create one with the **`@property`** decorator, which is the same decorator idea from Thursday applied to a method.

#### 4.1 A read-only property (the getter)

```python
class TestResult:
    def __init__(self, test_id, duration):
        self._test_id = test_id
        self._duration = duration

    @property
    def test_id(self):
        return self._test_id
```

```python
result = TestResult("TC-001", 1.5)
print(result.test_id)          # TC-001   <- no parentheses!
result.test_id = "TC-002"      # AttributeError: property 'test_id' of 'TestResult' object has no setter
```

The stored value is `_test_id` (internal), and `test_id` (public, no underscore) is the doorway. Since no setter was defined, the attribute is **read-only**. That's a powerful, simple way to express "this must never change after creation".

#### 4.2 A property with validation (getter + setter)

Add a setter with `@attribute_name.setter`:

```python
class TestResult:
    def __init__(self, test_id, duration):
        self._test_id = test_id
        self.duration = duration           # goes through the setter, so it is validated

    @property
    def duration(self):
        """Duration in seconds (never negative)."""
        return self._duration

    @duration.setter
    def duration(self, value):
        if value < 0:
            raise ValueError("duration cannot be negative")
        self._duration = value
```

```python
result = TestResult("TC-001", 1.5)
print(result.duration)          # 1.5
result.duration = 2.25          # uses the setter
print(result.duration)          # 2.25
result.duration = -1            # ValueError: duration cannot be negative
TestResult("TC-002", -3)        # ValueError (the constructor is validated too)
```

Rules for the pattern:

1. The **getter** (`@property`) comes first; the method name is the public name.
2. The **setter** uses `@<name>.setter` and must have the **same method name**.
3. The real data is stored in a differently named internal attribute (`_duration`).
4. In `__init__`, assign through the **public name** (`self.duration = duration`) so the setter's validation also protects construction.

From outside, `result.duration` looks like a plain attribute. Code written before you added validation keeps working, which is exactly why you don't need getters and setters up front.

#### 4.3 Validating text choices

```python
class TestCase:
    VALID_STATUSES = ("NOT RUN", "PASS", "FAIL", "SKIPPED")

    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        self._status = "NOT RUN"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"invalid status {value!r}; choose from {self.VALID_STATUSES}")
        self._status = value
```

```python
case = TestCase("TC-001", "Login")
case.status = "PASS"        # fine
case.status = "PSAS"        # ValueError: invalid status 'PSAS'; choose from (...)
```

The typo is now caught **at the exact line where it happens**, which is far better than discovering a corrupt report later. (`VALID_STATUSES` is a *class variable*, covered in the next lesson. For now read it as "a constant shared by the class".)

#### 4.4 Computed properties

A property needn't store anything; it can calculate a value on demand, so it can never be out of date:

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self._results = []          # internal

    def add(self, result):
        self._results.append(result)

    @property
    def total(self):
        return len(self._results)

    @property
    def passed(self):
        return sum(1 for r in self._results if r.status == "PASS")

    @property
    def pass_rate(self):
        if self.total == 0:
            return 0.0
        return self.passed / self.total * 100
```

```python
print(suite.total, suite.passed, suite.pass_rate)     # no parentheses, reads like data
suite.pass_rate = 50                                  # AttributeError: no setter, can't be assigned
```

Because `pass_rate` is computed from the results, it can't drift out of sync with them, and no one can set it to a nonsense value. This is encapsulation at its best: **the public face is simple; the rules stay inside.**

#### 4.5 Deleters (rarely needed)

There is also `@name.deleter` for `del obj.name`, but it's rarely used, so we'll skip it.

---

### 5. Protecting Mutable Internals

Encapsulating a *list* needs extra care. If a method returns the internal list itself, outsiders can change it directly and bypass your rules:

```python
class TestSuite:
    def __init__(self, name):
        self.name = name
        self._tests = []

    def add(self, test):
        self._tests.append(test)

    @property
    def tests(self):
        return self._tests               # leaks the real list!

suite = TestSuite("Smoke")
suite.tests.append("garbage")            # bypasses add()! 
```

Return a **copy** (or an immutable tuple) to keep control:

```python
    @property
    def tests(self):
        return list(self._tests)         # a copy; changes to it don't affect the suite

    # or an immutable version
    @property
    def tests_readonly(self):
        return tuple(self._tests)
```

Now `suite.tests.append("garbage")` modifies only a throw-away copy. Callers must use `suite.add(test)`, which can validate its input. (Remember the shallow-copy reminder: the *objects inside* are still shared, which is usually what you want.)

---

### 6. Designing the Public Interface

A good class has a **small, stable public interface** and keeps the rest hidden. A checklist:

1. **What does the outside world need to do?** (add a test, run, get the pass rate) These become public methods and properties.
2. **What are the internal details?** (the list, helper calculations, temporary state) Prefix with `_`.
3. **What rules must always hold?** (status is valid; duration ≥ 0) Enforce with properties and validation.
4. **What should never change after creation?** (an ID) Make it a read-only property.
5. **Does it return internal mutable data?** Return a copy.

A worked example, a result collector that guards its own rules:

```python
class ResultCollector:
    """Collects test results and reports statistics."""

    def __init__(self):
        self._results = {}               # internal: test_id -> status

    def record(self, test_id, status):
        """Record the outcome of a test."""
        if status not in ("PASS", "FAIL", "SKIPPED"):
            raise ValueError(f"unknown status {status!r}")
        self._results[test_id] = status

    @property
    def total(self):
        return len(self._results)

    @property
    def failed_ids(self):
        return sorted(tid for tid, status in self._results.items() if status == "FAIL")

    def _count(self, status):            # internal helper
        return list(self._results.values()).count(status)

    @property
    def pass_rate(self):
        if not self._results:
            return 0.0
        return self._count("PASS") / self.total * 100
```

```python
collector = ResultCollector()
collector.record("TC-001", "PASS")
collector.record("TC-002", "FAIL")
collector.record("TC-003", "PASS")

print(collector.total)          # 3
print(collector.failed_ids)     # ['TC-002']
print(f"{collector.pass_rate:.1f}%")     # 66.7%
collector.record("TC-004", "PSAS")        # ValueError: unknown status 'PSAS'
```

The public interface is just `record`, `total`, `failed_ids` and `pass_rate`. We could later change `_results` from a dictionary to something else without breaking any user.

---

### 7. Encapsulation and Inheritance

- **Protected** (`_name`) attributes are meant to be used by **subclasses**; the convention says "internal to this class family".
- **Private** (`__name`) names are mangled per class, so a subclass using `__balance` won't clash with its parent's `__balance`, but also can't easily access it. Because of that, prefer `_name` unless you specifically want mangling.
- Properties are inherited, and a subclass can override them like any method.

---

### 8. Good Practice Summary

| Do | Don't |
|---|---|
| Use public attributes for simple data | Write getters/setters "just in case" |
| Use `_name` for internal details | Rely on `__name` for security (it is not secure) |
| Use `@property` for validation, read-only or computed values | Make everything read-only without need |
| Validate on the way **in** (setters, constructor) | Wait until the data is used to discover it's bad |
| Return copies of internal lists/dictionaries | Leak the internal mutable object |
| Keep the public interface small and documented | Expose every attribute and helper |
| Raise `ValueError` with a clear message | Silently fix or ignore bad data |

Remember that encapsulation in Python is about **communication and good design**, not hard security. Nothing here would stop a determined programmer, and it isn't meant to; never store real secrets in "private" attributes expecting protection.

---

### 9. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Getter and setter use different names | `@property def x` then `@value.setter` | Setter name must match: `@x.setter def x` |
| Setter defined without a getter | `@x.setter` first | Define the `@property` getter first |
| Storing the value in the property name | `self.duration = v` inside the `duration` setter | Store in `self._duration` (infinite recursion otherwise) |
| Calling a property with parentheses | `result.duration()` | `result.duration` |
| Forgetting that the constructor bypasses validation | `self._duration = duration` in `__init__` | `self.duration = duration` |
| Returning the internal list | Callers can corrupt it | Return a copy or tuple |
| Thinking `__x` is truly private | `obj._Class__x` works | It's only name mangling |
| Using `__x` everywhere | Needless complexity | Use `_x` |
| Trying to set a read-only property | `AttributeError` | Add a setter if it should be writable |
| Over-validating | Every attribute has a setter | Only validate where rules exist |
| Trying to catch/handle errors now | `try/except` isn't covered yet | Just `raise`; error handling comes later |

**The recursion trap in detail:**

```python
class Bad:
    @property
    def value(self):
        return self.value        # calls itself forever -> RecursionError
```

The property getter must return the **underscored** attribute (`self._value`).

---

### 10. Practice Activities

1. **Conventions.** Create a class with a public, a `_protected` and a `__private` attribute. Print `__dict__` and find all three. Try to read the private one from outside and then via the mangled name.
2. **Break the rules.** Show that a plain `TestCase.status` accepts `"PSAS"`. Then make `status` a validated property that raises `ValueError`.
3. **Read-only ID.** Make `test_id` a read-only property and demonstrate the `AttributeError` when assigning to it.
4. **Validated number.** Create `Account` with a `balance` property that cannot be negative. Add `deposit(amount)` and `withdraw(amount)` methods that use the property.
5. **Computed property.** Add `pass_rate` as a computed property of a suite (no setter). Show it changes automatically when results are added.
6. **Leak and fix.** Create a class that returns its internal list, show how an outsider can corrupt it, then fix it by returning a copy.
7. **Recursion.** Reproduce the `RecursionError` from a property that returns itself, then fix it.
8. **Design.** Write down the public interface (methods and properties), the internal details and the rules for a `Browser` class that can `open(url)`, `close()`, and knows its `current_url` and whether it `is_open`. Then implement it.
9. **Validation message.** Improve a `ValueError` so that it tells the caller what was received and what is allowed.
10. **Refactor.** Take the `TestCase` from this morning's lesson on inheritance and encapsulate `status` (validated property) and `id` (read-only property). Check that your subclasses still work.
11. **Discuss.** Why does Python use conventions rather than strict `private` keywords? List one advantage and one risk.

---

## Summary

- **Encapsulation** = bundling data with methods **and** controlling access so an object can protect its own rules.
- Python uses **conventions**: `name` (public), `_name` (internal/protected, a polite warning), `__name` (private-ish via **name mangling** to `_Class__name`, still reachable). Prefer a single underscore.
- Getter/setter *methods* work but are clunky; Python's idiom is the **`@property`** decorator: the getter makes an attribute **read-only**, and `@name.setter` adds **validation** when assigning.
- Store the real data in `_name`, expose `name`; assign through the property in `__init__` so construction is validated too; never return `self.name` from the `name` getter (recursion).
- Use **`raise ValueError(...)`** to reject bad data at the moment it appears (catching errors comes later).
- **Computed properties** (no stored value) can't go stale.
- Protect **mutable internals** by returning copies or tuples.
- Design a **small public interface**, hide helpers, and enforce invariants. Don't over-engineer: start with plain attributes and add properties when a rule appears.
- Next: **class vs instance variables**, data shared by all objects of a class versus data belonging to each object.

---

## Additional Resources

- Python Tutorial: Private Variables: https://docs.python.org/3/tutorial/classes.html#private-variables
- Python documentation: `property`: https://docs.python.org/3/library/functions.html#property
- Real Python: Python's `property()`: Add Managed Attributes to Your Classes: https://realpython.com/python-property/
