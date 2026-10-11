# Static and Class Methods

## Learning Objectives

By the end of this lesson you will be able to:

- Distinguish **instance methods**, **class methods** and **static methods**, and say what each receives as its first argument.
- Write a **static method** with `@staticmethod` for helper logic related to a class that needs neither the object nor the class.
- Write a **class method** with `@classmethod` that receives the class as `cls`.
- Use class methods as **alternative constructors** (factory methods) such as `from_dict` and `from_string`.
- Use class methods to work with class variables, including in subclasses.
- Call these methods through the class or through an instance.
- Decide when to use an instance method, class method, static method, or a plain module-level function.
- Review the whole of Week 1 and prepare a clean Git summary push.

---

## Why This Matters

All the methods you wrote earlier today were **instance methods**: they take `self` and work with one particular object. But some behaviour belongs to the **class as a whole**, or is a helper that is related to the class without needing any object at all:

- *"Create a `TestCase` from a line of CSV text."* There's no object yet. You're trying to make one.
- *"Is this string a valid test ID?"* It needs no particular test case, just the text.
- *"How many test cases have been created so far?"* That's a fact about the class, not about one object.

Python provides two more kinds of method for these jobs: **static methods** and **class methods**. They use the same decorator idea you met on Thursday (`@something` above a function), and they are very common in test frameworks (for example, factory methods that build test data objects, and helper checks grouped with the class that uses them).

This is also the last lesson of Week 1, so at the end you'll find a short wrap-up of everything you've built, and how to prepare your Git summary push for today's exercise.

---

## The Concept

### 1. Three Kinds of Methods

| Kind | Decorator | First parameter | Can access | Typical job |
|---|---|---|---|---|
| **Instance method** | none | `self` (the object) | Instance data **and** class data | Work with one object's data |
| **Class method** | `@classmethod` | `cls` (the class) | Class data (not a specific object) | Alternative constructors; operate on class-level data |
| **Static method** | `@staticmethod` | nothing special | Neither, unless you pass them in | Utility logic that is related to the class but independent of it |

A single class can have all three:

```python
class Example:
    def instance_method(self):              # gets the object
        ...

    @classmethod
    def class_method(cls):                  # gets the class
        ...

    @staticmethod
    def static_method():                    # gets nothing automatic
        ...
```

---

### 2. Static Methods

A **static method** is a plain function that lives inside a class for organisational reasons. Python doesn't pass `self` or `cls`.

```python
class TestCase:
    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title

    @staticmethod
    def is_valid_id(test_id):
        """Return True for IDs like 'TC-007'."""
        return (
            test_id.startswith("TC-")
            and test_id[3:].isdigit()
            and len(test_id) == 6
        )
```

Call it on the class (no object required):

```python
print(TestCase.is_valid_id("TC-007"))      # True
print(TestCase.is_valid_id("XX-7"))        # False
```

Or on an instance (it behaves the same, since `self` is not passed):

```python
case = TestCase("TC-001", "Login")
print(case.is_valid_id("TC-099"))          # True
```

Key points:

- The **`@staticmethod`** line goes directly above the `def`.
- There is **no `self`** parameter. The arguments are exactly those you write.
- Inside, you can't use `self.something`, because there's no object.
- It's essentially a regular function, "filed" inside the class because it's conceptually related.

#### Why not just write a normal function outside the class?

You could. Static methods are a **namespacing and discoverability** choice:

- `TestCase.is_valid_id(...)` tells the reader exactly which concept the check belongs to.
- Subclasses and importers get the helper together with the class.
- The class remains a self-contained package.

If a helper is general-purpose and used by many unrelated classes (like Thursday's `format_duration`), keep it as a **module-level function** in a utility module instead. Use a static method when the function is closely tied to **this** class.

More static method examples:

```python
class Temperature:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return celsius * 9 / 5 + 32

print(Temperature.celsius_to_fahrenheit(100))     # 212.0
```

```python
class TestResult:
    STATUSES = ("PASS", "FAIL", "SKIPPED")

    @staticmethod
    def percent(part, whole):
        return 0.0 if whole == 0 else part / whole * 100
```

---

### 3. Class Methods

A **class method** receives **the class itself** as its first argument, conventionally named **`cls`** (just as `self` is conventional for objects). Use the `@classmethod` decorator.

```python
class TestCase:
    total_created = 0

    def __init__(self, test_id, title):
        self.id = test_id
        self.title = title
        TestCase.total_created += 1

    @classmethod
    def how_many(cls):
        return cls.total_created

TestCase("TC-001", "Login")
TestCase("TC-002", "Logout")

print(TestCase.how_many())       # 2
```

When you call `TestCase.how_many()`, Python passes `TestCase` as `cls`. Inside, `cls.total_created` reads the class variable. This is the link to the previous lesson: **class methods are the natural way to read and update class variables.**

#### What makes `cls` special: subclasses

If a subclass calls an inherited class method, `cls` is **the subclass**, not the parent:

```python
class Animal:
    @classmethod
    def describe(cls):
        return f"I am a {cls.__name__}"

class Dog(Animal):
    pass

print(Animal.describe())        # I am a Animal
print(Dog.describe())           # I am a Dog     <- cls is Dog here
```

That's the crucial difference from a static method, which cannot know which class it was called through. It is also what makes the next technique work.

---

### 4. Class Methods as Alternative Constructors (Factory Methods)

A class has only one `__init__`. But data arrives in many formats: a dictionary, a line of text, a JSON record, a spreadsheet row. A **class method that builds and returns an object** gives you extra, well-named ways to create it. These are called **alternative constructors** or **factory methods**; their names conventionally start with `from_`.

```python
class TestCase:
    def __init__(self, test_id, title, priority="Medium"):
        self.id = test_id
        self.title = title
        self.priority = priority

    @classmethod
    def from_dict(cls, data):
        """Build a TestCase from a dictionary."""
        return cls(data["id"], data["title"], data.get("priority", "Medium"))

    @classmethod
    def from_csv_line(cls, line):
        """Build a TestCase from text like 'TC-001,Valid login,High'."""
        test_id, title, priority = line.strip().split(",")
        return cls(test_id, title, priority)

    def __repr__(self):
        return f"TestCase({self.id!r}, {self.title!r}, {self.priority!r})"
```

```python
a = TestCase("TC-001", "Valid login")
b = TestCase.from_dict({"id": "TC-002", "title": "Logout", "priority": "Low"})
c = TestCase.from_csv_line("TC-003,Search by keyword,High")

print(a)      # TestCase('TC-001', 'Valid login', 'Medium')
print(b)      # TestCase('TC-002', 'Logout', 'Low')
print(c)      # TestCase('TC-003', 'Search by keyword', 'High')
```

Why `cls(...)` instead of hard-coding `TestCase(...)`? Because of inheritance:

```python
class UITest(TestCase):
    pass

ui = UITest.from_dict({"id": "UI-001", "title": "Login page"})
print(type(ui).__name__)        # UITest
```

Since `cls` is `UITest` when called through the subclass, `cls(...)` creates a `UITest`, not a plain `TestCase`. Had we written `TestCase(...)` inside the method, subclasses would wrongly get parent objects.

You've already seen this pattern in Python itself: `dict.fromkeys(["a", "b"], 0)` is a class method that builds a dictionary in a different way from `dict()`.

#### Test-data factories

Factory class methods are a favourite in test automation, where you often need ready-made objects:

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
        return f"User({self.username!r}, role={self.role!r})"

print(User.admin())             # User('admin', role='admin')
print(User.guest())             # User('guest', role='viewer')
print(User.admin("priya"))      # User('priya', role='admin')
```

Reading `User.admin()` in a test is much clearer than `User("admin", "admin")`.

---

### 5. Class Methods and Class Variables Together

A class method can read **and modify** class variables safely (using `cls`), avoiding the shadowing trap from the previous lesson:

```python
class Browser:
    default_timeout = 30
    _instances = 0

    def __init__(self, name):
        self.name = name
        Browser._instances += 1

    @classmethod
    def set_default_timeout(cls, seconds):
        if seconds <= 0:
            raise ValueError("timeout must be positive")
        cls.default_timeout = seconds        # changes the class variable

    @classmethod
    def instance_count(cls):
        return cls._instances

Browser("Chrome")
Browser("Firefox")

Browser.set_default_timeout(60)
print(Browser.default_timeout)       # 60
print(Browser.instance_count())      # 2
```

This gives the class a controlled way to change shared configuration (encapsulation again): the validation lives in the method, rather than anyone being able to assign `Browser.default_timeout = -5`.

---

### 6. Comparing the Three Side by Side

```python
class Report:
    format_name = "text"                # class variable

    def __init__(self, title):
        self.title = title              # instance variable

    def header(self):                   # INSTANCE method: needs this report's title
        return f"== {self.title} =="

    @classmethod
    def with_default_title(cls):        # CLASS method: builds an object via the class
        return cls("Untitled report")

    @classmethod
    def describe_format(cls):           # CLASS method: reads class data
        return f"Format: {cls.format_name}"

    @staticmethod
    def underline(text):                # STATIC method: pure helper, needs nothing
        return "-" * len(text)
```

```python
r = Report("Regression")
print(r.header())                          # == Regression ==
print(Report.underline(r.header()))        # ----------------
print(Report.describe_format())            # Format: text
print(Report.with_default_title().header())    # == Untitled report ==
```

**Decision guide:**

```
Does the method need data from a specific object (self)?
 ├─ Yes ──▶ instance method
 └─ No
     ├─ Does it need the class (class variables, or to create objects of the class/subclass)?
     │    └─ Yes ──▶ class method (@classmethod, cls)
     └─ No, it needs neither
          ├─ Is it closely tied to this class? ──▶ static method (@staticmethod)
          └─ Is it general-purpose / used elsewhere? ──▶ plain function in a module
```

---

### 7. How These Relate to Decorators

On Thursday you learned that `@decorator` above a function means `func = decorator(func)`. `@staticmethod` and `@classmethod` are **built-in decorators**: they wrap the function so that Python knows *not* to pass the object (static) or to pass the *class* instead (class). Likewise `@property` from the encapsulation lesson. Nothing mystical: it is the same wrapping idea, built into the language.

Decorator order matters when stacking: the `@classmethod`/`@staticmethod` decorators should usually be the **outermost** (top) line.

---

### 8. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Forgetting the decorator | `def from_dict(cls, data):` without `@classmethod` | Add `@classmethod`; otherwise `cls` receives the object |
| Putting `self` in a static method | `@staticmethod def f(self, x)` | Remove `self` |
| Using `self` inside a class method | `self.x` → `NameError` | Use `cls.x` |
| Hard-coding the class in a factory | `return TestCase(...)` | `return cls(...)` |
| Using static methods for everything | Helper functions in classes needlessly | Use a module-level function if it isn't tied to the class |
| Using a class method when the object's data is needed | Can't reach `self` | Make it an instance method |
| Forgetting to `return` the new object in a factory | Gives `None` | `return cls(...)` |
| Calling a class method on an instance and expecting object state | `cls` is still the class | Use an instance method |
| Modifying class variables with `self.` in an instance method | Creates a shadow | Use a class method or `ClassName.variable` |
| Wrong decorator order | `@staticmethod` under another decorator | Put it at the top |

---

### 9. Week 1 Wrap-Up

You have covered a great deal in five days. Here is the arc of the week:

| Day | Python | Git | Test-automation hook |
|---|---|---|---|
| Monday | Setup, variables, types, operators, casting, input/output | `init`, `add`, `commit`, `status`, `log` | Test-case ID formatter |
| Tuesday | `if`/`elif`/`else`, `for`, `while`, `break`, `continue` | `.gitignore`, clone, push, pull, fetch, pull requests | Pass/fail grader, log scanner |
| Wednesday | Lists, tuples, dicts, sets, slicing, methods, `collections` | Branching, merging, conflicts, remote branches | Test-data manager |
| Thursday | Functions, arguments, lambdas, closures, decorators, utilities | Pair-programming workflow | Reusable test-utility library |
| Friday | Classes, constructors, inheritance, encapsulation, class members | Week summary push | Test-report system |

**How the pieces connect.** A realistic mini framework uses almost everything:

- **Variables, types and f-strings** to represent and print data.
- **Conditionals and loops** to decide and repeat.
- **Collections** to hold test data and results.
- **Functions and decorators** for reusable helpers (validators, generators, a timer).
- **Classes** to model test cases, suites, results and reporters.
- **Git** to track every step, collaborate and review.

#### Preparing your Git summary push

Today's exercise ends with a clean "Week 1 summary" push. A good routine:

1. **Check where you are:**
   ```bash
   git status
   git branch
   ```
2. **Make sure everything you want is committed**, with sensible messages (`git log --oneline` should read like a story of the week).
3. **Check your `.gitignore`** covers `__pycache__/` and any virtual environment or secrets, and that no such files are staged.
4. **Tidy up the README:** list what's in the repository (folders and scripts for each day), how to run the main programs, and a short "What I learned this week" section.
5. **Work on a branch and open a pull request** if that is your team's process:
   ```bash
   git switch -c feature/week1-summary
   git add README.md
   git commit -m "Add Week 1 summary to README"
   git push -u origin feature/week1-summary
   ```
6. **Merge** (after review), then update `main` and delete the branch:
   ```bash
   git switch main
   git pull
   git branch -d feature/week1-summary
   ```
7. **Final check:** `git log --oneline --graph --all` and open the repository on GitHub to confirm everything arrived.

If you notice something you'd like to remember about each day's Git commands, consider adding a "Git cheat sheet" section to your README. Writing things in your own words is the best revision.

---

### 10. Practice Activities

1. **Static.** Add `is_valid_id(test_id)` as a static method of `TestCase`. Call it through the class and through an instance.
2. **Class method counter.** Add a class-level counter, and a `@classmethod` `how_many()` returning it. Create several objects and print the count.
3. **from_dict.** Write `TestCase.from_dict(data)` with a default priority when the key is missing. Build three cases from three dictionaries.
4. **from_csv_line.** Write `from_csv_line(line)`. Process the multi-line text below with a loop to create a list of objects (use `splitlines()` and skip blank lines):
   ```text
   TC-001,Valid login,High
   TC-002,Logout,Low

   TC-003,Search,Medium
   ```
5. **cls vs the class name.** Make `UITest(TestCase)` and compare `UITest.from_dict(...)` when the factory uses `cls(...)` versus `TestCase(...)`. Print the type of the result in each case.
6. **User factories.** Write `User.admin()`, `User.guest()` and `User.random()` (using `random` for the name). Use them to build a small list of test users.
7. **Configuration.** Write a `Browser.set_default_timeout(seconds)` class method that validates its input, and show that invalid values raise `ValueError`.
8. **Sort it.** For each of these, decide: instance, class or static method? (a) `Suite.add(test)`; (b) `Suite.from_file_lines(lines)`; (c) `Suite.is_valid_name(name)`; (d) `Suite.total_suites_created()`; (e) `Result.passed()`. Explain each choice.
9. **Refactor.** Move one helper function from your Thursday utility library into the class it belongs to as a static method. Was it a good fit, or does it belong in the utilities module? Justify your answer.
10. **Explain.** In your own words, describe what `cls` is and why a class method can build objects of subclasses correctly.
11. **Mini project: test-report system.** Build `TestResult` (with a `from_dict` class method and validated status), `Suite` (holding results, computed pass rate property) and `Reporter` (formats a text report; static helper for alignment). Add `__str__`/`__repr__` methods, and one subclass of your choice.
12. **Week 1 summary.** Follow the Git routine in section 9: clean commit history, README update, branch, push, PR and merge.

---

## Summary

- **Instance methods** take `self` and work on one object; **class methods** (`@classmethod`) take `cls` and work with the class; **static methods** (`@staticmethod`) take neither and are plain helper functions filed inside the class.
- Call class and static methods through the **class** (`TestCase.from_dict(...)`); instances can call them too.
- **Class methods** shine as **alternative constructors** (`from_dict`, `from_csv_line`, `User.admin()`), and for reading or safely changing **class variables**. Use **`cls(...)`**, not the hard-coded class name, so subclasses get the right type.
- **Static methods** group related helpers (like `is_valid_id`) with the class; use a plain module-level function if the helper is general-purpose.
- Choose by asking what the method needs: the object (`self`), the class (`cls`), or nothing.
- `@classmethod`, `@staticmethod` and `@property` are built-in **decorators**, the same idea as Thursday's.
- Week 1 took you from "Hello, world" to classes, with Git recording each step. Finish by tidying your commit history, README and `.gitignore`, then push your summary through a branch and pull request.
- Later weeks build on all of this: the Python and Git habits from this week carry through the rest of the program.

---

## Additional Resources

- Python documentation: `classmethod`: https://docs.python.org/3/library/functions.html#classmethod
- Python documentation: `staticmethod`: https://docs.python.org/3/library/functions.html#staticmethod
- Real Python: Python's Instance, Class, and Static Methods Demystified: https://realpython.com/instance-class-and-static-methods-demystified/
