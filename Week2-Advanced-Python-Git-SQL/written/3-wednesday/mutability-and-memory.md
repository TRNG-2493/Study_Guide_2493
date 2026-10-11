# Mutability and Memory

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the Python **object model**: every value is an object with an identity, a type and a value, and a variable is a *name* (label) bound to an object.
- Use `id()`, `is`, `==` and `type()` correctly, and explain the difference between **identity** and **equality**.
- Classify common types as **mutable** (list, dict, set, most user-defined objects) or **immutable** (int, float, bool, str, tuple, frozenset, bytes, None).
- Predict what happens when two names refer to the same mutable object (aliasing), and when a function receives a mutable argument.
- Explain and avoid the **mutable default argument** bug.
- Make correct **shallow** and **deep** copies using `copy.copy`, `copy.deepcopy`, slicing and `list()`/`dict()`.
- Describe at a high level how Python manages memory with **reference counting** and **garbage collection**.
- Recognise why only immutable (hashable) objects can be dictionary keys.
- Apply all of this to realistic test-automation problems: shared test data, fixtures that "leak" between tests, and configuration dictionaries that get modified by accident.

---

## Why This Matters

This week's epic is about hardening your Python so that automated tests are **trustworthy**. Few things destroy trust in a test suite faster than **shared state that changes when you did not expect it to**. Mutability is the root cause of a large fraction of those surprises:

- A test modifies a "shared" list of sample users, and the next test starts with the wrong data.
- A helper function with a default argument `results=[]` quietly accumulates values across calls, so test 5 sees the output of tests 1 to 4.
- A configuration dictionary copied with `.copy()` still shares an inner dictionary with the original, so changing "the staging config" changes "the production config" too.

On Tuesday you read and wrote files and handled exceptions; the data you loaded (lists of rows, dictionaries from JSON) is exactly the kind of mutable data that gets passed around and modified. In the previous lesson you learned that *names* live in namespaces; today you learn what those names are *pointing at*. Together, these two lessons give you the mental model you need for the next topics in today's schedule: debugging (you will inspect `id()`s and values in a debugger), logging, and writing unit tests (where every test must start from a clean, predictable state).

If you only remember one sentence from this lesson, make it this:

> **In Python, a variable is not a box that holds a value; it is a label attached to an object. Assignment never copies an object; it just attaches another label.**

---

## The Concept

### 1. Everything is an object

In Python, every piece of data, whether a number, a string, a list, a function or a class, is an **object** stored somewhere in memory. Every object has three things:

1. **Identity**: a unique ID for the object's lifetime. In the standard CPython interpreter this is the object's memory address. Get it with `id(obj)`.
2. **Type**: what kind of object it is (`int`, `str`, `list`...). Get it with `type(obj)`. It decides which operations are allowed.
3. **Value**: the data it contains.

```python
x = [10, 20]
print(type(x))    # <class 'list'>
print(x)          # [10, 20]
print(id(x))      # some large integer such as 140101300110704 (differs on every run)
```

The identity and type never change during an object's life. The *value* of some objects can change; those are the **mutable** ones.

### 2. Names are labels, not boxes

Many languages teach "a variable is a box that stores a value". That picture works badly in Python. A better picture:

```
   names                objects in memory
  +------+            +-----------------+
  |  a   |----------->|  [1, 2, 3]      |
  +------+      +---->|  (a list object)|
  |  b   |------+     +-----------------+
  +------+
```

After `a = [1, 2, 3]` and `b = a`, there is **one** list and **two** names pointing at it. Nothing was copied.

```python
a = [1, 2]
b = a              # attach a second label to the SAME list
b.append(3)        # change the list through label b
print(a)           # [1, 2, 3]   <-- a "changed" too, because it is the same object
print(a is b)      # True
print(id(a) == id(b))   # True
```

Line by line:

- `a = [1, 2]` creates a list object and binds the name `a` to it.
- `b = a` does **not** make a new list. It binds the name `b` to the object `a` already refers to.
- `b.append(3)` asks the list object to change itself. Both names see the change.
- `a is b` asks: "are these two names bound to the exact same object?" Yes.

**Analogy.** Imagine a shared online document. Giving a colleague "the link" (`b = a`) does not create a second document; if they edit it, you see the edits. To get an independent document you must explicitly *make a copy* (we will do that in section 8).

### 3. Identity versus equality: `is` versus `==`

| Operator | Question it answers | How it works |
|---|---|---|
| `==` | Do these two objects have the same **value**? | Calls the object's equality logic (`__eq__`) |
| `is` | Are these the **same object**? | Compares identities (like `id(a) == id(b)`) |

```python
l1 = [1, 2]
l2 = [1, 2]
print(l1 == l2)    # True   (same contents)
print(l1 is l2)    # False  (two separate list objects)
```

Rules of thumb:

- Use `==` to compare **values** (the vast majority of cases, including in test assertions).
- Use `is` only for singletons, mainly `None`, `True`, `False`: write `if result is None:`, not `if result == None:`.
- Never use `is` to compare numbers or strings. It may appear to work (small integers are cached in CPython, so `256 is 256` is `True`) but this is an implementation detail and Python 3.8+ even emits a `SyntaxWarning` when you compare a literal with `is`. It will betray you the day the value is 257.

### 4. Mutable versus immutable

An object is **immutable** if its value cannot change after creation. It is **mutable** if it can be modified in place.

| Immutable | Mutable |
|---|---|
| `int`, `float`, `complex` | `list` |
| `bool` | `dict` |
| `str` | `set` |
| `tuple` | `bytearray` |
| `frozenset` | Most instances of your own classes |
| `bytes` | `collections.deque`, `collections.defaultdict`, ... |
| `None` | |

#### Immutable objects: "changing" creates a new object

```python
x = 5
y = x
y += 1             # not "change the 5", but "make 6 and re-label y"
print(x, y)        # 5 6   <-- x is unaffected
```

Strings behave the same way:

```python
s = "qa"
print(id(s))       # e.g. 140101300110704
s += "e"           # builds a NEW string "qae" and re-binds s
print(id(s))       # a different number: it is a different object
```

You cannot modify a string character by character:

```python
name = "test"
name[0] = "T"      # TypeError: 'str' object does not support item assignment
```

To "change" a string, create a new one: `name = "T" + name[1:]`, or use methods such as `.upper()`, `.replace()`, which **return** new strings and leave the original alone.

#### Mutable objects: methods change them in place

```python
tests = ["login", "logout"]
print(id(tests))
tests.append("search")     # modifies the same object
print(id(tests))           # same id as before
print(tests)               # ['login', 'logout', 'search']
```

Methods like `append`, `extend`, `insert`, `remove`, `pop`, `sort`, `reverse` (list), `update`, `setdefault`, `pop`, `clear` (dict), `add`, `discard` (set) all change the object they are called on, and, importantly, most return `None`:

```python
data = [3, 1, 2]
result = data.sort()       # sorts IN PLACE and returns None
print(result, data)        # None [1, 2, 3]
print(sorted([3, 1, 2]))   # [1, 2, 3]   sorted() builds a NEW list
```

A frequent beginner bug is writing `data = data.sort()`, which sets `data` to `None`. Remember: *in-place methods return `None`; functions that return new objects (`sorted`, `reversed`, `str.upper`) do not alter the original.*

#### The tuple subtlety: immutable container, mutable contents

A tuple is immutable, meaning you cannot add, remove or replace its items. But if an item is itself a mutable object, that inner object can still change:

```python
t = (1, [2, 3])
t[1].append(4)              # allowed! we are changing the inner list, not the tuple
print(t)                    # (1, [2, 3, 4])

t[0] = 9                    # TypeError: 'tuple' object does not support item assignment
```

The tuple still holds the same two objects (the integer `1` and *that* list); only the list's own value changed. Even odder:

```python
t = (1, [2, 3])
try:
    t[1] += [5]
except TypeError as e:
    print(e)                # 'tuple' object does not support item assignment
print(t)                    # (1, [2, 3, 5])   <-- the list WAS extended anyway
```

`t[1] += [5]` first extends the inner list in place (succeeds), then tries to assign the result back into the tuple slot (fails). This is a well-known Python gotcha; just remember "immutable" describes the container's slots, not the objects inside.

### 5. Passing arguments: "pass by object reference"

When you call a function, Python binds the **parameter name** to the **same object** the caller passed in. (Often called "pass by assignment" or "pass by object reference".) The consequences depend on mutability:

```python
def add_marker(items):
    items.append("done")        # mutates the caller's list

def rebind(items):
    items = items + ["done"]    # builds a NEW list; only the local name changes

a = []
add_marker(a)
print(a)        # ['done']   <-- caller's list was changed

b = []
rebind(b)
print(b)        # []         <-- caller's list untouched
```

- In `add_marker`, `items` is another label for the caller's list, so `append` changes it for everyone.
- In `rebind`, `items + ["done"]` creates a new list and the *local* name `items` is re-bound to it. The caller's name `b` still points at the original empty list. (This ties directly to the previous lesson: assignment inside a function creates/rebinds a **local** name.)
- With immutable arguments (ints, strings, tuples) a function simply cannot change the caller's object, because the object cannot be changed at all.

**Practical rule:** if a function is not *supposed* to modify its input, either do not mutate it, or copy it first. If it *is* meant to modify it, say so in the function name and docstring (`sort_in_place`, `normalize_inplace`), or return a new object instead.

### 6. The mutable default argument trap

Default values are evaluated **once**, when the `def` statement runs, not on every call. If the default is a mutable object, every call that uses the default shares the *same* object.

```python
def add_item(item, bucket=[]):      # BUG: one shared list for all calls
    bucket.append(item)
    return bucket

print(add_item(1))     # [1]
print(add_item(2))     # [1, 2]   <-- surprise! the first call's data is still there
```

Output:

```
[1]
[1, 2]
```

Test-automation scenario: a helper `collect_errors(message, errors=[])`. Test A adds an error, test B (which should start clean) sees it and fails. The tests pass individually and fail together: a nightmare to debug.

**The standard fix:** use `None` as a sentinel and create the list inside the function.

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []                 # a fresh list on every call that needs one
    bucket.append(item)
    return bucket

print(add_item(1))     # [1]
print(add_item(2))     # [2]
```

You can even *see* the shared default: `add_item.__defaults__` (for the buggy version) shows the one list that accumulates items.

### 7. Aliasing traps inside data structures

#### Multiplying a list of lists

```python
rows = [[0] * 2] * 3
rows[0][0] = 1
print(rows)           # [[1, 0], [1, 0], [1, 0]]   <-- all three rows changed!
```

`[[0] * 2] * 3` repeats the **same inner list object** three times. The outer list contains three references to one inner list. The fix is a list comprehension, which runs the inner expression for each row and creates a new list each time:

```python
rows = [[0] * 2 for _ in range(3)]
rows[0][0] = 1
print(rows)           # [[1, 0], [0, 0], [0, 0]]
```

Test scenario: building a grid or a table of expected results (a "matrix" of test data). Using `*` on nested lists is the classic way to corrupt it.

#### Shared test data

```python
BASE_USER = {"name": "alice", "roles": ["viewer"]}

def make_admin():
    user = BASE_USER              # alias, not a copy!
    user["roles"].append("admin")
    return user

make_admin()
print(BASE_USER)                  # {'name': 'alice', 'roles': ['viewer', 'admin']}  <-- constant corrupted
```

A constant that is mutated is no longer constant. Section 8 shows how to copy correctly.

### 8. Copying: shallow versus deep

Because assignment does not copy, you must copy explicitly when you need an independent object.

#### Shallow copy

A **shallow copy** makes a new outer container but fills it with references to the **same inner objects**. Ways to make one:

```python
import copy

original = [1, 2, 3]
c1 = original[:]            # slice copy
c2 = list(original)         # constructor copy
c3 = original.copy()        # list/dict/set method
c4 = copy.copy(original)    # generic function

print(c1 is original, c1 == original)    # False True
```

For a list of immutable items (numbers, strings) that is all you need. With nested mutable objects, the shallow copy's inner objects are still shared:

```python
orig = {"user": {"name": "a", "roles": ["x"]}}
shallow = orig.copy()                      # new outer dict, same inner dict
shallow["user"]["roles"].append("y")
print(orig)       # {'user': {'name': 'a', 'roles': ['x', 'y']}}   <-- original changed!
```

#### Deep copy

A **deep copy** recursively copies everything, producing a completely independent structure:

```python
import copy

orig = {"user": {"name": "a", "roles": ["x"]}}
deep = copy.deepcopy(orig)
deep["user"]["roles"].append("z")
print(orig)       # {'user': {'name': 'a', 'roles': ['x']}}         <-- untouched
print(deep)       # {'user': {'name': 'a', 'roles': ['x', 'z']}}
```

| | Shallow copy | Deep copy |
|---|---|---|
| Outer container | New | New |
| Nested objects | **Shared** | Copied too |
| Speed / memory | Fast, small | Slower, bigger |
| Use when | Contents are all immutable (flat data) | Nested mutable data that must be independent |

For test data, `copy.deepcopy(BASE_USER)` at the start of each test (or fixture) is a common, safe pattern.

### 9. Why dictionary keys must be immutable (hashable)

A dictionary finds entries using a **hash**, a number computed from the key's value. If a key could change, its hash would change and Python would no longer be able to find it. Therefore only **hashable** objects, in practice immutable ones, can be dictionary keys or set members.

```python
d = {}
d[(1, 2)] = "ok"           # tuple of immutables: fine
d["name"] = "also fine"    # string: fine
d[[1, 2]] = "nope"         # TypeError: unhashable type: 'list'
```

Remember the tuple subtlety: a tuple containing a list is also unhashable.

### 10. How Python manages memory (high-level)

You do not allocate or free memory by hand in Python. Two mechanisms work together in the standard CPython interpreter:

1. **Reference counting.** Every object keeps a count of how many names/containers refer to it. When you bind a new name the count goes up; when a name is deleted, re-bound, or goes out of scope (a function returns), the count goes down. When it reaches **zero**, the object is destroyed immediately and its memory is reclaimed.
2. **Garbage collector.** Reference counting cannot free objects that refer to each other in a cycle (`a` points to `b`, `b` points to `a`, nothing else points to either). A background *cyclic garbage collector* (the `gc` module) finds and cleans such groups.

```python
import sys

data = [1, 2, 3]
print(sys.getrefcount(data))   # typically 2: the name 'data' + the temporary argument to getrefcount
other = data
print(sys.getrefcount(data))   # typically 3
del other                      # removes one label; the list stays because 'data' still points to it
print(sys.getrefcount(data))   # back to 2
```

`del name` removes the **name**, not necessarily the object. The object disappears only when nothing refers to it any more.

Why should a tester care?

- **Resource leaks in long test runs.** Holding references to large objects (a big list of results accumulated in a module-level variable) keeps them in memory for the entire run.
- **Files and connections.** You learned on Tuesday that context managers (`with open(...)`) close resources deterministically. You should not rely on memory management to close a file or network connection "eventually".
- **Small-integer and string caching (interning).** CPython reuses some small ints and strings. This is an optimisation, not a promise; never write logic that depends on `is` for values.

### 11. Choosing mutable or immutable on purpose

| Situation | Prefer | Why |
|---|---|---|
| Constants / configuration that must not change | `tuple`, `frozenset`, `str`, or a deep-copied dict | Prevents accidental modification |
| Dictionary keys | `str`, `int`, `tuple` of immutables | Required to be hashable |
| Collecting results as a test runs | `list` | Needs to grow |
| Function parameters | Avoid mutating inputs unless documented | Prevents surprising callers |
| Default arguments | `None` or immutable values | Avoids the shared-default bug |

---

## Code Examples

### Example A: Demonstration script, identity and mutation

```python
# mutability_demo.py
nums = [1, 2, 3]
alias = nums
copy1 = nums.copy()

nums.append(4)

print("nums  :", nums)               # [1, 2, 3, 4]
print("alias :", alias)              # [1, 2, 3, 4]  (same object)
print("copy1 :", copy1)              # [1, 2, 3]     (independent)
print("alias is nums :", alias is nums)   # True
print("copy1 is nums :", copy1 is nums)   # False
print("copy1 == [1, 2, 3] :", copy1 == [1, 2, 3])   # True
```

Output:

```
nums  : [1, 2, 3, 4]
alias : [1, 2, 3, 4]
copy1 : [1, 2, 3]
alias is nums : True
copy1 is nums : False
copy1 == [1, 2, 3] : True
```

### Example B: A test-data factory that does not leak

```python
# user_factory.py
import copy

DEFAULT_USER = {
    "name": "test_user",
    "email": "test@example.com",
    "roles": ["viewer"],
    "profile": {"country": "US", "newsletter": False},
}

def make_user(**overrides):
    """Return a NEW user dict each time; never modifies DEFAULT_USER."""
    user = copy.deepcopy(DEFAULT_USER)      # independent copy, nested data included
    user.update(overrides)                  # apply per-test changes
    return user

admin = make_user(name="alice", roles=["admin"])
viewer = make_user()
viewer["profile"]["newsletter"] = True      # safe: only 'viewer' changes

print(admin["roles"], viewer["roles"])      # ['admin'] ['viewer']
print(DEFAULT_USER["profile"])              # {'country': 'US', 'newsletter': False}
```

Explanation:

- `copy.deepcopy(DEFAULT_USER)` guarantees nested dicts/lists are new, so editing `viewer["profile"]` cannot touch `DEFAULT_USER`.
- `user.update(overrides)` replaces top-level keys with the values given by the caller (`**overrides` collects keyword arguments into a dict).
- Each test calls `make_user()` and receives an independent object: this is the heart of **test isolation**. Later, when you learn test frameworks, "fixtures" will formalise exactly this idea.

Try breaking it: replace `copy.deepcopy(DEFAULT_USER)` with `DEFAULT_USER.copy()` and run the `newsletter` line again. `DEFAULT_USER["profile"]["newsletter"]` becomes `True`, because `.copy()` is shallow.

### Example C: Fixing the mutable-default bug in a result collector

```python
# Buggy version
def record_failure(message, failures=[]):
    failures.append(message)
    return failures

print(record_failure("timeout"))       # ['timeout']
print(record_failure("404"))           # ['timeout', '404']   <- leaked

# Fixed version
def record_failure_fixed(message, failures=None):
    if failures is None:
        failures = []
    failures.append(message)
    return failures

print(record_failure_fixed("timeout")) # ['timeout']
print(record_failure_fixed("404"))     # ['404']
```

### Example D: Detecting aliasing with `id()` while debugging

```python
config = {"retries": 3}
alias = config
clone = dict(config)

for label, obj in [("config", config), ("alias", alias), ("clone", clone)]:
    print(f"{label:7} id={id(obj)} value={obj}")
```

Typical output (the ID numbers differ on your machine):

```
config  id=140101300110704 value={'retries': 3}
alias   id=140101300110704 value={'retries': 3}
clone   id=140101298848608 value={'retries': 3}
```

If two names print the same `id`, they are the same object. When a debugger (covered next in *Debugging techniques*) shows you an unexpected value, comparing ids quickly tells you whether the object you are modifying is also being used elsewhere.

### Example E: Tuple-key lookup table for expected results

```python
expected_status = {
    ("GET", "/users"): 200,
    ("POST", "/users"): 201,
    ("GET", "/missing"): 404,
}

def expected(method, path):
    return expected_status.get((method, path), "unknown")

print(expected("GET", "/users"))      # 200
print(expected("DELETE", "/users"))   # unknown
```

The tuple `("GET", "/users")` is immutable and therefore hashable, so it makes an ideal composite key.

---

## Summary / Key Takeaways

- Every value in Python is an **object** with an identity (`id`), a type and a value. Variables are **names bound to objects**; assignment attaches a label and never copies.
- `==` compares **values**; `is` compares **identity**. Use `is` almost only with `None`.
- **Immutable**: int, float, bool, str, tuple, frozenset, bytes, None. "Modifying" them creates a new object.
- **Mutable**: list, dict, set and most custom objects. They change in place, so every name that refers to them sees the change.
- In-place methods (`list.sort`, `list.append`, `dict.update`) return `None`; do not write `x = x.sort()`.
- A tuple is immutable but can contain mutable objects whose contents can still change.
- Function parameters are bound to the caller's objects. Mutating a mutable argument affects the caller; re-binding the parameter name does not.
- **Never use a mutable default argument.** Use `None` and create the object inside the function.
- `copy` module: slicing/`.copy()`/`copy.copy()` make **shallow** copies; `copy.deepcopy()` makes fully independent copies. Beware `[[0]*n]*m`.
- Only hashable (practically immutable) objects can be dict keys or set elements.
- CPython frees objects with **reference counting** plus a cyclic **garbage collector**; use context managers for deterministic cleanup of files and connections.
- For testers: unexpected mutation of shared data is a leading cause of flaky and order-dependent tests. Give each test its own copy of the data.

---

## Practice Questions and Mini-Exercises

**Q1.** Predict the output:

```python
a = [1, 2, 3]
b = a
b = b + [4]
print(a, b)
```

**Q2.** Predict the output, and explain the difference from Q1:

```python
a = [1, 2, 3]
b = a
b += [4]
print(a, b)
```

**Q3.** Which of these are immutable? `"abc"`, `[1, 2]`, `(1, 2)`, `{1, 2}`, `3.14`, `frozenset({1})`, `{"a": 1}`, `None`.

**Q4.** What is wrong with the function below, and how do you fix it?

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

**Q5.** Predict the output:

```python
original = {"tests": ["a", "b"]}
copy1 = original.copy()
copy1["tests"].append("c")
print(original)
```

What single change to the second line gives an independent copy?

**Q6.** Does `x is y` or `x == y` express "these two lists have the same items"? Which one would you use in an assertion about API response data?

**Q7 (mini-exercise).** Create a 3 by 3 grid of zeros such that setting `grid[1][1] = 5` changes only the middle cell. Show a wrong way and the right way.

**Q8 (mini-exercise).** Write `get_default_config()` that returns a dictionary `{"retries": 3, "hosts": ["a", "b"]}` such that modifying the returned dictionary (including the `hosts` list) never affects later calls. Show it with a test.

**Q9.** Why does the following raise an error?

```python
cache = {}
cache[["GET", "/users"]] = 200
```

Give two ways to make it work.

**Q10.** Explain in your own words what `del x` does when `x` is the only name for a list, and what it does when there are two names for the list.

### Answers

**A1.** `[1, 2, 3] [1, 2, 3, 4]`. `b + [4]` builds a **new** list and re-binds `b`; `a` still points to the old list.

**A2.** `[1, 2, 3, 4] [1, 2, 3, 4]`. For lists, `+=` is an **in-place** operation (it calls `extend` behind the scenes), so the shared list is modified. `b = b + [4]` and `b += [4]` are not equivalent for mutable types. (For immutable types such as ints and tuples, `+=` creates a new object.)

**A3.** Immutable: `"abc"`, `(1, 2)`, `3.14`, `frozenset({1})`, `None`. Mutable: `[1, 2]`, `{1, 2}`, `{"a": 1}`. (`(1, 2)` is immutable, but a tuple containing a list would only be "shallowly" immutable.)

**A4.** The default list `[]` is created once and shared by all calls that omit `tags`, so tags accumulate across calls. Fix:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

**A5.** Prints `{'tests': ['a', 'b', 'c']}` because `.copy()` is shallow and the inner list is shared. Use `copy1 = copy.deepcopy(original)` (after `import copy`).

**A6.** `x == y` compares values/contents. Use `==` (or a dedicated comparison) in assertions about data. `is` would only be true if both names were the very same object.

**A7.**

```python
wrong = [[0] * 3] * 3
wrong[1][1] = 5
print(wrong)    # [[0, 5, 0], [0, 5, 0], [0, 5, 0]]  all rows are the same list

right = [[0] * 3 for _ in range(3)]
right[1][1] = 5
print(right)    # [[0, 0, 0], [0, 5, 0], [0, 0, 0]]
```

**A8.**

```python
def get_default_config():
    return {"retries": 3, "hosts": ["a", "b"]}   # builds fresh objects on every call

c1 = get_default_config()
c1["hosts"].append("c")
c2 = get_default_config()
print(c1["hosts"], c2["hosts"])   # ['a', 'b', 'c'] ['a', 'b']
```

Building the literal inside the function means new objects every call. If the defaults were stored in a module-level constant, you would return `copy.deepcopy(DEFAULTS)` instead.

**A9.** A list is mutable and therefore unhashable, so it cannot be a dictionary key (`TypeError: unhashable type: 'list'`). Use a tuple key (`cache[("GET", "/users")] = 200`) or a string key (`cache["GET /users"] = 200`).

**A10.** `del x` removes the **name** `x`. If it was the only name, the list's reference count drops to zero and the list is freed. If a second name still refers to the list, the list stays alive; only the label `x` is gone.

---

## Additional Resources

- Python Language Reference, "Data model" (objects, values and types): https://docs.python.org/3/reference/datamodel.html#objects-values-and-types
- Python Standard Library, `copy` module (shallow and deep copy operations): https://docs.python.org/3/library/copy.html
- Python Programming FAQ, "Why are default values shared between objects?": https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects
