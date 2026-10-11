# Classes and Objects

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what object-oriented programming (OOP) is and why it exists.
- Describe the difference between a **class** (a blueprint) and an **object** (an instance built from it).
- Define a simple class with `class` and create objects from it.
- Recognise that you have been using objects all along (strings, lists, dictionaries).
- Give objects data (attributes) and behaviour (methods) at a basic level.
- Explain why `self` appears in methods.
- Create several independent objects from one class and store them in collections.
- Compare objects with `==` and `is`, and check an object's type with `type()` and `isinstance()`.
- Decide when a class is a better choice than a dictionary or a set of functions.

---

## Why This Matters

This week you have gone from single variables to collections (Wednesday) to functions (Thursday). Each step gave you a better way to organise code. Today's step answers a question that appears the moment programs get bigger:

> *How do I keep related **data** and the **functions that work on that data** together in one tidy package?*

Consider a test case. It has data (an ID, a title, a priority, a status) and behaviour (run itself, mark itself passed or failed, describe itself). With what you know so far, you might use a dictionary for the data and separate functions for the behaviour:

```python
test_case = {"id": "TC-001", "title": "Valid login", "status": "NOT RUN"}

def mark_passed(case):
    case["status"] = "PASS"
```

This works, but nothing connects `mark_passed` to test cases, and nothing stops someone from building a broken dictionary with the key `"staus"`. **Classes** solve this by bundling data and behaviour into a single, named concept: a `TestCase`.

Why a test automation engineer cares:

- **Every major test framework is object-oriented.** Selenium has `WebDriver` and `WebElement` objects. Pytest and unittest use classes for test groups. The "Page Object Model", the most common pattern in UI automation, is simply a class per web page.
- **Test suites are naturally object-shaped:** suites contain test cases, which produce results, which are collected by reporters.
- Understanding classes lets you **read and extend other people's code**, which is most of what you will do on a real project.

Today's demo builds a `TestCase` / `TestSuite` hierarchy, and the exercise models a test-report system with `TestResult`, `Suite` and `Reporter` classes. This first lesson lays the foundation.

---

## The Concept

### 1. You Have Already Been Using Objects

In Python, **everything is an object**. When you wrote this on Wednesday:

```python
browsers = ["Chrome", "Firefox"]
browsers.append("Edge")
```

`browsers` is an **object** of the type (class) `list`. It holds **data** (the items) and has **behaviour** (methods such as `append`, `sort` and `pop`). Strings, dictionaries, sets, even integers are objects:

```python
print(type("hello"))        # <class 'str'>
print("hello".upper())      # HELLO      -> the string object has a method
print(type(42))             # <class 'int'>
print(type([1, 2]))         # <class 'list'>
print(type({"a": 1}))       # <class 'dict'>
```

So far you have only *used* classes that Python provides. Today you learn to **write your own**, creating new kinds of objects that fit your problem: a `TestCase`, a `User`, a `Browser`, a `Report`.

---

### 2. Core Terms

| Term | Meaning | Analogy |
|---|---|---|
| **Class** | A blueprint or template that defines what data and behaviour its objects have | A cookie cutter; an architect's house plan |
| **Object** (or **instance**) | One concrete thing built from the class | A cookie; an actual house built from the plan |
| **Attribute** | A piece of data stored in an object | A house's colour, number of rooms |
| **Method** | A function that belongs to an object/class | What the house can do: open the door, turn on lights |
| **Instantiation** | Creating an object from a class | Building the house |

```
          CLASS: TestCase (blueprint)
          ┌────────────────────────────┐
          │ attributes: id, title,     │
          │             status         │
          │ methods:    run(), pass()  │
          └─────────────┬──────────────┘
                        │  create objects
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   ┌──────────┐   ┌──────────┐    ┌──────────┐
   │ TC-001   │   │ TC-002   │    │ TC-003   │
   │ Login    │   │ Search   │    │ Logout   │
   │ NOT RUN  │   │ PASS     │    │ FAIL     │
   └──────────┘   └──────────┘    └──────────┘
        objects (instances), each with its own data
```

One class can produce as many objects as you like, and each object has **its own** data. A blueprint doesn't live in the house; the houses are separate from each other.

---

### 3. Defining Your First Class

Syntax:

```python
class ClassName:
    # body: attributes and methods
```

A class that does nothing yet:

```python
class TestCase:
    pass
```

- **`class`** is the keyword (like `def` for functions).
- **`TestCase`** is the class name. By convention, class names use **CapWords** (also called PascalCase): each word starts with a capital letter, with no underscores: `TestCase`, `TestResult`, `LoginPage`. This differs from variables and functions, which use `snake_case`, and it lets you tell them apart at a glance.
- The colon and the **indented body** follow the usual rules. `pass` is a placeholder, as before.

#### Creating objects (instantiation)

Call the class like a function:

```python
case_1 = TestCase()
case_2 = TestCase()

print(case_1)             # <__main__.TestCase object at 0x000001E5A3B4C2D0>
print(type(case_1))       # <class '__main__.TestCase'>
```

`TestCase()` builds a new object. Each call builds a **different** one. The strange text printed is Python's default description: "a `TestCase` object living at this memory address". (We will learn how to make objects print nicely in the next lesson.)

---

### 4. Giving Objects Data: Attributes

An **attribute** is a variable that belongs to an object. You can read or set one with **dot notation**: `object.attribute`.

```python
case_1 = TestCase()
case_1.id = "TC-001"
case_1.title = "Valid login"
case_1.status = "NOT RUN"

case_2 = TestCase()
case_2.id = "TC-002"
case_2.title = "Invalid password"
case_2.status = "NOT RUN"

print(case_1.title)       # Valid login
print(case_2.title)       # Invalid password
```

Each object keeps **its own** values: changing one does not affect the other.

```python
case_1.status = "PASS"
print(case_1.status)      # PASS
print(case_2.status)      # NOT RUN
```

This is like a dictionary's `case["status"]`, but written `case.status`. Setting attributes one by one after creating an object is clumsy and easy to get wrong (forgetting one, mistyping `staus`). In the next lesson you will learn the **constructor** (`__init__`), which sets up every new object correctly in one step. For now, the point is the concept: *objects carry their own data*.

Reading an attribute that doesn't exist gives an error:

```python
print(case_1.owner)
```

```text
AttributeError: 'TestCase' object has no attribute 'owner'
```

You will see `AttributeError` often. It usually means a typo or an attribute that was never set.

---

### 5. Giving Objects Behaviour: Methods

A **method** is a function defined **inside a class**. Objects of that class can call it with dot notation, just like `my_list.append(...)`.

```python
class TestCase:
    def describe(self):
        print(f"{self.id}: {self.title} [{self.status}]")

    def mark_passed(self):
        self.status = "PASS"

    def mark_failed(self):
        self.status = "FAIL"
```

Use it:

```python
case_1 = TestCase()
case_1.id = "TC-001"
case_1.title = "Valid login"
case_1.status = "NOT RUN"

case_1.describe()          # TC-001: Valid login [NOT RUN]
case_1.mark_passed()
case_1.describe()          # TC-001: Valid login [PASS]
```

#### What is `self`?

Every method's **first parameter** is `self`. When you call `case_1.mark_passed()`, Python automatically passes the object `case_1` as the first argument, so inside the method `self` **is that object**.

```python
case_1.mark_passed()
# behind the scenes it is like:  TestCase.mark_passed(case_1)
```

That's why `self.status = "PASS"` changes the status of *that particular* test case. If you call `case_2.mark_passed()`, then `self` refers to `case_2`.

Important details:

- You **write** `self` in the `def` line, but you **don't pass it** in the call; Python does that.
- `self` is a naming **convention** (not a keyword), but every Python developer uses it. Always call it `self`.
- Forgetting `self` in the definition gives a confusing error:

```python
class Broken:
    def hello():           # forgot self
        print("hi")

Broken().hello()
```

```text
TypeError: Broken.hello() takes 0 positional arguments but 1 was given
```

"But I gave zero!" is exactly what you think; Python passed the object automatically, so it counts as one.

---

### 6. Objects Are Independent

```python
a = TestCase()
b = TestCase()

a.id = "TC-001"
b.id = "TC-002"

print(a.id, b.id)         # TC-001 TC-002
```

Two objects from the same class share the **same methods** (the behaviour is defined once in the class) but have **separate data**.

#### Variables hold references

Recall the aliasing lesson from Wednesday: `b = a` for a list makes two names for **one** list. Objects behave the same way:

```python
x = TestCase()
x.status = "NOT RUN"

y = x                      # NOT a copy: y refers to the same object
y.status = "PASS"

print(x.status)            # PASS   <- x changed too!
print(x is y)              # True
```

`is` checks **identity**, "are these literally the same object?", while `==` checks whether two objects are **equal** according to the class. For your own simple classes, `==` defaults to identity unless you tell Python otherwise:

```python
p = TestCase()
q = TestCase()
print(p == q)       # False (two different objects, even if they hold the same data)
print(p is q)       # False
print(p is p)       # True
```

(You will see how to define your own equality later in the program; for now, remember that two separate objects are not equal just because they look alike.)

---

### 7. Checking Types: `type()` and `isinstance()`

```python
case = TestCase()

print(type(case))                      # <class '__main__.TestCase'>
print(isinstance(case, TestCase))      # True
print(isinstance(case, str))           # False
print(isinstance("hello", str))        # True
```

`isinstance(object, Class)` answers "is this object an instance of that class?" It is the preferred way to check types, and in the inheritance lesson you'll see it also recognises *related* classes.

---

### 8. Inspecting an Object

Handy tools for exploring:

```python
case = TestCase()
case.id = "TC-001"
case.status = "NOT RUN"

print(hasattr(case, "id"))           # True   -> does the attribute exist?
print(hasattr(case, "owner"))        # False
print(getattr(case, "owner", "n/a")) # n/a    -> read with a default (like dict.get)
setattr(case, "owner", "Priya")      # same as case.owner = "Priya"
print(case.__dict__)                 # {'id': 'TC-001', 'status': 'NOT RUN', 'owner': 'Priya'}
print(dir(case)[-3:])                # a peek at the available names
```

`__dict__` shows the attributes as an ordinary dictionary: a reminder that an object's data really is just a dictionary of names and values. Use `help(TestCase)` to see a class's documentation.

---

### 9. Objects in Collections

Since an object is a value like any other, you can store objects in lists and dictionaries and loop over them, combining everything from the week:

```python
class TestCase:
    def describe(self):
        print(f"{self.id}: {self.title} [{self.status}]")

    def mark_passed(self):
        self.status = "PASS"

def make_case(test_id, title):
    case = TestCase()
    case.id = test_id
    case.title = title
    case.status = "NOT RUN"
    return case

suite = [
    make_case("TC-001", "Valid login"),
    make_case("TC-002", "Search by keyword"),
    make_case("TC-003", "Logout"),
]

suite[0].mark_passed()
suite[2].mark_passed()

for case in suite:
    case.describe()

passed = [case.id for case in suite if case.status == "PASS"]
print(passed)
```

```text
TC-001: Valid login [PASS]
TC-002: Search by keyword [NOT RUN]
TC-003: Logout [PASS]
['TC-001', 'TC-003']
```

(The `make_case` helper function exists only because we don't have constructors yet. The next lesson replaces it with `__init__`. The last line uses a list comprehension, a compact loop that you'll learn properly in a later lesson.)

Lambdas and sorting work with objects too:

```python
by_title = sorted(suite, key=lambda case: case.title)
```

You use the same `key` idea as on Thursday, but with `case.title` (attribute access) instead of `case["title"]` (dictionary lookup).

---

### 10. Class vs Dictionary vs Functions: When to Use What

| Situation | Good choice |
|---|---|
| A quick, one-off record | Dictionary |
| A fixed, simple record that never changes | `namedtuple` or tuple |
| Data **and** behaviour that belong together; many similar things; rules about valid states | **Class** |
| A single operation with no state | Function |

Some benefits of classes:

1. **Structure:** the class defines exactly what a `TestCase` has and does.
2. **Behaviour next to data:** `case.mark_passed()` reads naturally and lives with the data it changes.
3. **Reuse and extension:** new kinds of test case can be built from existing ones (inheritance, the next-but-one lesson).
4. **Protection:** a class can control how its data is changed (encapsulation).
5. **Vocabulary:** your code mirrors the real concepts of the domain: suites, cases, results, reports, pages.

Don't overuse classes. A small script that needs one calculation doesn't need a class. Reach for one when you notice that **several pieces of data and several functions keep travelling together.**

---

### 11. The Four Pillars of OOP (A Roadmap)

You will hear these four terms constantly. This lesson introduced the vocabulary; the rest of the day covers the details:

| Pillar | Idea | Lesson |
|---|---|---|
| **Encapsulation** | Bundle data and methods; control access to the data | Attributes/methods/constructors; Encapsulation |
| **Abstraction** | Hide complexity behind a simple interface (you call `driver.get(url)` without knowing how a browser works) | Throughout |
| **Inheritance** | A new class reuses and extends an existing one | Inheritance and polymorphism |
| **Polymorphism** | Different classes respond to the same method call in their own way | Inheritance and polymorphism |

---

### 12. A Realistic Mini-Model

Putting it all together, a tiny model of a test run:

```python
class TestCase:
    def describe(self):
        return f"{self.id}: {self.title} [{self.status}]"

    def mark(self, outcome):
        self.status = outcome

login = TestCase()
login.id = "TC-001"
login.title = "Valid login"
login.status = "NOT RUN"

print(login.describe())        # TC-001: Valid login [NOT RUN]
login.mark("PASS")
print(login.describe())        # TC-001: Valid login [PASS]
```

Notice that `describe` **returns** a string instead of printing it: the same design principle as yesterday's reusable functions. The caller decides what to do with the text. Methods follow all the function rules you learned on Thursday: parameters, defaults, return values, docstrings. They just have `self` first.

---

### 13. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Forgetting `self` in a method definition | `def describe():` | `def describe(self):` |
| Passing `self` when calling | `case.describe(case)` | `case.describe()` |
| Forgetting parentheses when creating an object | `case = TestCase` | `case = TestCase()` |
| Forgetting parentheses when calling a method | `case.describe` (nothing happens) | `case.describe()` |
| Using a variable instead of `self.variable` in a method | `status = "PASS"` (local variable) | `self.status = "PASS"` |
| Misspelling an attribute | `case.staus` | Use an editor with autocomplete; consider `__init__` (next lesson) |
| Assuming `b = a` copies an object | Changes appear on both | Create a new object |
| Class name in `snake_case` | `class test_case:` | `class TestCase:` |
| Reading an attribute before setting it | `AttributeError` | Set attributes in `__init__` (next lesson) |
| Expecting `==` to compare contents | Two separate objects are not equal | Compare attributes explicitly for now |

---

### 14. Practice Activities

1. **Explore built-in objects.** Use `type()` on a string, an integer, a list, a dictionary and a function (for example `print`). List two methods of each (`dir(...)` helps).
2. **First class.** Create an empty class `User`. Create two users and give each `username` and `role` attributes. Print them.
3. **Independence.** Change one user's role and show the other is unchanged.
4. **Methods.** Add a method `describe(self)` to `User` that returns text like `alice (admin)`. Call it for both users.
5. **A state-changing method.** Create a class `Counter` with a method `increment(self)` that adds 1 to `self.count`. Set `count = 0` on a new object manually, call `increment` three times and print the result.
6. **Identity.** Create `x = User()`, `y = x` and `z = User()`. Predict then print `x is y`, `x is z`, `x == z`.
7. **hasattr and getattr.** Use them to safely read an `email` attribute that some users have and others don't.
8. **A collection.** Make a list of three `TestCase` objects. Loop over them, count how many have status `"PASS"`, and sort them by title.
9. **Dictionary vs class.** Take a test case represented as a dictionary from Wednesday and write the equivalent class. List two things that are easier with the class, and one that is easier with the dictionary.
10. **Spot the bug.** What is wrong with this class and its use? Fix it.
    ```python
    class Greeter:
        def hello():
            print("Hello")

    g = Greeter
    g.hello()
    ```
11. **Model.** On paper, choose a real-world thing (a web page, a browser, a bank account). List three pieces of data and three actions. Which are attributes and which are methods?

---

## Summary

- **Object-oriented programming** organises code around **objects** that bundle **data (attributes)** and **behaviour (methods)**. Everything in Python is an object; you have already used lists, strings and dictionaries.
- A **class** is a blueprint (`class TestCase:`; names in **CapWords**); an **object/instance** is created by calling the class: `case = TestCase()`. Each object has its own data.
- Read and write attributes with **dot notation** (`case.status`). A missing attribute raises `AttributeError`.
- A **method** is a function inside a class whose first parameter is **`self`**, the object the method is called on. You write `self` in the `def`, but Python passes it for you.
- `b = a` makes two names for **one** object; `is` tests identity; `==` on simple custom objects is identity unless defined otherwise.
- Use `type()`, `isinstance()`, `hasattr()`, `getattr()`, `setattr()` and `__dict__` to inspect objects.
- Objects can be stored in lists and dictionaries, sorted with `key=lambda`, and passed to functions.
- Use a class when data and behaviour belong together; use a dictionary for quick records and a function for stateless operations.
- Next: **attributes, methods and constructors**, where `__init__` sets up every object properly.

---

## Additional Resources

- Python Tutorial: Classes: https://docs.python.org/3/tutorial/classes.html
- Python documentation: Data model (objects, values and types): https://docs.python.org/3/reference/datamodel.html
- Real Python: Object-Oriented Programming (OOP) in Python: https://realpython.com/python3-object-oriented-programming/
