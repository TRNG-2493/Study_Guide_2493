# Knowledge Check: Python Data Structures & Git Branching (Week 1 – Wednesday)

Answer each question first, then open the solution to check your understanding.

---

## Part 1: Multiple Choice

### Question 1

Which of these values can be used as a **dictionary key**?

- [ ] A) `["Chrome", 120]` (a list)
- [ ] B) `("Chrome", 120)` (a tuple)
- [ ] C) `{"Chrome", 120}` (a set)
- [ ] D) Only strings; no other type is allowed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `("Chrome", 120)` (a tuple)

**Explanation:** Dictionary keys must be immutable (hashable). Strings, numbers and tuples work; lists do not.
- **Why others are wrong:**
  - A) Lists are mutable, so using one as a key raises `TypeError: unhashable type`.
  - C) A set is mutable, so it cannot be a key; the lesson lists only strings, numbers and tuples as valid keys.
  - D) Keys are not limited to strings; numbers and tuples are valid too.
</details>

---

### Question 2

You want to start with an **empty set** of failed test IDs. Which line does that?

- [ ] A) `failed = {}`
- [ ] B) `failed = []`
- [ ] C) `failed = set()`
- [ ] D) `failed = ()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `failed = set()`

**Explanation:** `set()` is the only way to create an empty set; empty curly braces create a dictionary.
- **Why others are wrong:**
  - A) `{}` creates an empty dictionary, not a set.
  - B) `[]` creates an empty list.
  - D) `()` creates an empty tuple.
</details>

---

### Question 3

A list `results` holds the outcome of every test run so far. Which expression gives only the **last 3** results?

- [ ] A) `results[-3:]`
- [ ] B) `results[:3]`
- [ ] C) `results[-3]`
- [ ] D) `results[3:-1]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `results[-3:]`

**Explanation:** `s[-n:]` returns the last n items as a new list.
- **Why others are wrong:**
  - B) `results[:3]` returns the first 3 items.
  - C) `results[-3]` returns a single item (the third from the end), not a list slice.
  - D) `results[3:-1]` skips the first 3 items and also drops the last one.
</details>

---

### Question 4

A beginner writes `ids = ids.sort()` and then `print(ids[0])`. What goes wrong?

- [ ] A) `sort()` only works on tuples, so Python raises a `SyntaxError`
- [ ] B) `sort()` returns a sorted copy, but strings such as `"TC-3"` cannot be sorted
- [ ] C) `sort()` sorts a list from highest to lowest by default, so `ids[0]` is the wrong item
- [ ] D) `sort()` sorts in place and returns `None`, so `ids` becomes `None` and `ids[0]` fails

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `sort()` sorts in place and returns `None`, so `ids` becomes `None` and `ids[0]` fails

**Explanation:** In-place list methods such as `sort()` return `None`. Use `ids.sort()` on its own, or `ids = sorted(ids)`.
- **Why others are wrong:**
  - A) `sort()` is a list method; tuples cannot be sorted in place, and there is no `SyntaxError` here.
  - B) `sort()` does not return a copy (that is `sorted()`), and strings sort alphabetically without problems.
  - C) The default order is ascending; `reverse=True` is needed for descending.
</details>

---

### Question 5

You have `defaults = {"browser": "Chrome", "timeout": 30}` and `overrides = {"browser": "Firefox"}`. Which approach merges them so overrides win, without changing `defaults`?

- [ ] A) `settings = defaults.pop(overrides)`
- [ ] B) `settings = defaults.items(overrides)`
- [ ] C) `settings = defaults.copy()` then `settings.update(overrides)`
- [ ] D) `settings = defaults.get(overrides)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `settings = defaults.copy()` then `settings.update(overrides)`

**Explanation:** `update` adds new keys and overwrites existing ones; calling it on a copy leaves `defaults` untouched.
- **Why others are wrong:**
  - A) `pop` removes a single key and returns its value; it does not merge dictionaries.
  - B) `items()` returns key-value pairs and takes no argument; it does not merge.
  - D) `get` looks up one key safely; it does not merge dictionaries.
</details>

---

### Question 6

Which line correctly creates a dictionary that automatically starts an **empty list** for every new module name?

- [ ] A) `groups = defaultdict(list)`
- [ ] B) `groups = defaultdict(list())`
- [ ] C) `groups = defaultdict[list]`
- [ ] D) `groups = Counter(list)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `groups = defaultdict(list)`

**Explanation:** `defaultdict` takes the type name **without parentheses** as its factory; it calls it whenever a key is missing.
- **Why others are wrong:**
  - B) Passing `list()` (with parentheses) is a listed common mistake; pass `list` without `()`.
  - C) `defaultdict` is called with parentheses like a function; square brackets are not the way to set the factory.
  - D) `Counter` counts items; it does not create lists for grouping.
</details>

---

### Question 7

A suite has thousands of test cases, and your script must repeatedly fetch the full record for a given ID such as `TC-4021`. Which structure fits best?

- [ ] A) A list of dictionaries, searched with a loop each time
- [ ] B) A dictionary keyed by test ID
- [ ] C) A set of test IDs
- [ ] D) A tuple of test IDs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A dictionary keyed by test ID

**Explanation:** A dictionary keyed by ID jumps straight to the record instead of checking every item, so lookups are fast.
- **Why others are wrong:**
  - A) Looping through the list works but is clumsy and slow when lookups are frequent.
  - C) A set only answers "is it there?"; it cannot return the full record.
  - D) A tuple is for fixed data and is found by position, not by ID.
</details>

---

### Question 8

When does `git merge feature` perform a **fast-forward** merge?

- [ ] A) When both `main` and `feature` have new commits
- [ ] B) When the two branches changed the same line
- [ ] C) When you use the `--no-ff` option
- [ ] D) When `main` has not moved since `feature` branched off

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) When `main` has not moved since `feature` branched off

**Explanation:** If the target branch has no new commits, Git simply slides its pointer forward along the straight line of commits; no merge commit is created.
- **Why others are wrong:**
  - A) That is a diverged history, which needs a three-way merge with a merge commit.
  - B) That produces a merge conflict that you must resolve.
  - C) `--no-ff` does the opposite: it forces a merge commit even when a fast-forward is possible.
</details>

---

### Question 9

During a merge conflict, `config.py` contains the markers below. What does the text between `<<<<<<< HEAD` and `=======` represent?

```text
<<<<<<< HEAD
browser = "edge"
=======
browser = "firefox"
>>>>>>> feature/firefox
```

- [ ] A) The version from the branch you are currently on
- [ ] B) The version from the incoming branch being merged
- [ ] C) The original version from the common ancestor
- [ ] D) Lines that Git has already deleted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The version from the branch you are currently on

**Explanation:** The section after `<<<<<<< HEAD` is your current branch's version; the part after `=======` is the incoming branch's version.
- **Why others are wrong:**
  - B) The incoming branch's version is between `=======` and `>>>>>>> feature/firefox`.
  - C) Git's markers in this lesson show only the two competing versions, not the common ancestor.
  - D) The markers show competing content, not deleted lines.
</details>

---

### Question 10

A teammate deleted `feature/api-tests` on GitHub, but `git branch -r` still lists `origin/feature/api-tests` on your machine. Which command tidies this up?

- [ ] A) `git merge --abort`
- [ ] B) `git push -u origin main`
- [ ] C) `git fetch --prune`
- [ ] D) `git switch -c origin/feature/api-tests`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `git fetch --prune`

**Explanation:** `git fetch --prune` removes remote-tracking references whose branches no longer exist on the remote.
- **Why others are wrong:**
  - A) `git merge --abort` cancels an in-progress merge; it does not touch remote-tracking references.
  - B) `push -u` publishes a branch and sets its upstream; it does not remove stale references.
  - D) `switch -c` creates a new local branch; it does not remove stale references.
</details>

---

### Question 11

Which built-in collection is **ordered**, allows **duplicate** items, and **cannot be changed** after it is created?

- [ ] A) List
- [ ] B) Tuple
- [ ] C) Set
- [ ] D) Dictionary

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Tuple

**Explanation:** A tuple keeps a fixed order, allows duplicates and is immutable, which makes it good for data that should never change by accident, such as a screen resolution.
- **Why others are wrong:**
  - A) A list is ordered and allows duplicates, but it is mutable, so you can add, remove and replace items.
  - C) A set is unordered and does not allow duplicates (and it can be changed with `add` and `remove`).
  - D) A dictionary requires unique keys and can be changed freely.
</details>

---

### Question 12

Your test users are stored like this:

```python
users = {
    "admin": {"password": "Admin#123", "role": "administrator"},
    "guest": {"password": "Guest#123", "role": "viewer"},
}
```

Which expression gives the role of the `guest` user?

- [ ] A) `users["role"]["guest"]`
- [ ] B) `users[1]["role"]`
- [ ] C) `users.get("guest", "role")`
- [ ] D) `users["guest"]["role"]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `users["guest"]["role"]`

**Explanation:** Work from the outside in: the first key selects the inner dictionary for `guest`, and the second key selects the `role` field inside it.
- **Why others are wrong:**
  - A) The keys are in the wrong order; `"role"` is not a key of the outer dictionary, so this raises `KeyError`.
  - B) Dictionaries are accessed by key, not by position, so `1` is not a valid key here (`KeyError`).
  - C) `.get("guest", "role")` returns the whole inner `guest` dictionary; `"role"` is only the default used when `guest` is missing.
</details>

---

### Question 13

```python
browsers = {"Chrome", "Firefox", "Edge"}
```

Which of the following lines raises a `TypeError`?

- [ ] A) `print(browsers[0])`
- [ ] B) `print("Edge" in browsers)`
- [ ] C) `print(len(browsers))`
- [ ] D) `browsers.add("Safari")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `print(browsers[0])`

**Explanation:** Sets are unordered and have no index, so `browsers[0]` raises a `TypeError`. Convert to a list or use `sorted()` first if you need positions.
- **Why others are wrong:**
  - B) Membership testing with `in` is exactly what sets are good at (and it is very fast).
  - C) `len()` works on every collection.
  - D) `add` is the normal way to put a new item into a set.
</details>

---

### Question 14

A queue contains duplicates:

```python
queue = ["TC-1", "TC-2", "TC-1", "TC-3"]
queue.remove("TC-1")
```

What does `queue` contain afterwards?

- [ ] A) `['TC-2', 'TC-3']`
- [ ] B) `['TC-1', 'TC-2', 'TC-3']`
- [ ] C) `['TC-2', 'TC-1', 'TC-3']`
- [ ] D) A `ValueError` is raised

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `['TC-2', 'TC-1', 'TC-3']`

**Explanation:** `remove(x)` deletes only the **first** item equal to `x`; later copies stay in the list.
- **Why others are wrong:**
  - A) That would require removing every match, but `remove` removes only one (you would need a loop or a new list).
  - B) This assumes the second `"TC-1"` was removed; `remove` always takes the first match.
  - D) `ValueError` is raised only when the value is not in the list at all, and `"TC-1"` is present.
</details>

---

### Question 15

A record must contain the fields in `required`. You want to know which fields are **missing** from `provided`:

```python
required = {"id", "title", "status"}
provided = {"id", "title"}
```

Which expression gives `{'status'}`?

- [ ] A) `provided - required`
- [ ] B) `required | provided`
- [ ] C) `provided & required`
- [ ] D) `required - provided`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `required - provided`

**Explanation:** The difference `a - b` keeps what is in `a` but not in `b`, so `required - provided` leaves only the field that was never supplied.
- **Why others are wrong:**
  - A) `provided - required` gives an empty set, because everything provided is also required.
  - B) `|` is the union (everything in either set), which returns all three fields.
  - C) `&` is the intersection (items in both), which returns `{'id', 'title'}`.
</details>

---

### Question 16

You need a **sorted copy** of a tuple of test IDs and must leave the original untouched. Which approach works?

- [ ] A) `ids.sort()`
- [ ] B) `sorted(ids)`
- [ ] C) `ids = ids.sort()`
- [ ] D) `ids.reverse()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `sorted(ids)`

**Explanation:** `sorted()` works on any collection and returns a new list, leaving the original alone. For a tuple the result is a list.
- **Why others are wrong:**
  - A) `.sort()` is a list method that sorts in place; tuples only have the methods `count` and `index`.
  - C) Even on a list this is the classic bug: `.sort()` returns `None`, so the variable would become `None`.
  - D) Tuples have no `reverse` method, and reversing is not the same as sorting anyway.
</details>

---

### Question 17

Which expression reverses the string `word` **without changing** it?

- [ ] A) `word[::-1]`
- [ ] B) `word[-1]`
- [ ] C) `word[:-1]`
- [ ] D) `word.reverse()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `word[::-1]`

**Explanation:** A negative step walks backwards through the sequence, which is the classic way to reverse any sequence, and it produces a new object. For example `"automation"[::-1]` is `"noitamotua"`.
- **Why others are wrong:**
  - B) `word[-1]` returns only the last character.
  - C) `word[:-1]` returns everything except the last character, in the original order.
  - D) `reverse()` is a list method that changes the list in place; it is not a way to reverse a string.
</details>

---

### Question 18

```python
results = ["P", "F", "P"]
print(results[len(results)])
```

This raises `IndexError`. What is the correct explanation and fix?

- [ ] A) Counting starts at 1, so the first item is `results[1]`
- [ ] B) `len()` returns one too many, so subtract it from the result
- [ ] C) Only slices can reach the last item of a list
- [ ] D) Valid indexes run from `0` to `len - 1`, so use `results[-1]` for the last item

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Valid indexes run from `0` to `len - 1`, so use `results[-1]` for the last item

**Explanation:** A 3-item list has indexes 0, 1 and 2, so index 3 is out of range (the classic off-by-one). `results[-1]` or `results[len(results) - 1]` both reach the last item.
- **Why others are wrong:**
  - A) Python counts from 0, so the first item is `results[0]`; thinking it starts at 1 is the root of the off-by-one bug.
  - B) `len()` correctly returns the number of items (3); the bug is using that count as an index.
  - C) Single-item indexing can reach the last item (with `-1` or `len - 1`); slices are not required.
</details>

---

### Question 19

Data copied from a spreadsheet has a header row first:

```python
rows = ["id,title", "TC-001,Login", "TC-002,Logout"]
```

Which loop header processes only the data rows?

- [ ] A) `for row in rows[:1]:`
- [ ] B) `for row in rows[1:]:`
- [ ] C) `for row in rows[-1]:`
- [ ] D) `for row in rows[::2]:`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `for row in rows[1:]:`

**Explanation:** `rows[1:]` starts at index 1, so the header at index 0 is skipped and every remaining row is visited.
- **Why others are wrong:**
  - A) `rows[:1]` returns only the first item, which is the header.
  - C) `rows[-1]` is a single string (the last row), so the loop would run over its characters.
  - D) `rows[::2]` takes every second item starting at index 0, so it includes the header and skips `TC-001`.
</details>

---

### Question 20

```python
summary = Counter(["PASS", "FAIL", "PASS", "PASS", "FAIL", "SKIP"])
```

Which call returns exactly `[('PASS', 3)]`?

- [ ] A) `summary.most_common()`
- [ ] B) `summary.top(1)`
- [ ] C) `summary.most_common(1)`
- [ ] D) `summary["PASS"]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `summary.most_common(1)`

**Explanation:** `most_common(n)` returns a list of the top `n` `(item, count)` tuples, highest count first.
- **Why others are wrong:**
  - A) With no argument it returns all items: `[('PASS', 3), ('FAIL', 2), ('SKIP', 1)]`.
  - B) A `Counter` has no `top` method; the lesson's tool is `most_common(n)`.
  - D) Indexing a `Counter` by item returns just the count, the number `3`, not a list of tuples.
</details>

---

### Question 21

**QE scenario:** your framework must remember only the **last 5 log lines** so it can print them when a test fails. Which tool fits best?

- [ ] A) `deque(maxlen=5)`
- [ ] B) A `Counter` of the log lines
- [ ] C) A `namedtuple` with five fields
- [ ] D) A plain list that grows forever, using `pop(0)` to trim it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `deque(maxlen=5)`

**Explanation:** With `maxlen`, old items fall off automatically as new ones are appended, which is perfect for "what happened just before the failure?".
- **Why others are wrong:**
  - B) `Counter` counts how often items occur; it does not keep the most recent lines in order.
  - C) A `namedtuple` is a fixed, labelled record; it is not a rolling buffer.
  - D) A plain list does not trim itself, and `pop(0)` is slow because all items have to shift along; `deque(maxlen=N)` is the tool the lesson recommends for "last N items".
</details>

---

### Question 22

```python
TestResult = namedtuple("TestResult", ["test_id", "status", "duration"])
result = TestResult("TC-001", "PASS", 1.2)
```

Which line produces a **modified copy** with `duration` set to `2.5`?

- [ ] A) `result.duration = 2.5`
- [ ] B) `result[2] = 2.5`
- [ ] C) `result.update(duration=2.5)`
- [ ] D) `result._replace(duration=2.5)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `result._replace(duration=2.5)`

**Explanation:** A `namedtuple` is immutable, so `._replace()` builds a modified copy instead of changing the original.
- **Why others are wrong:**
  - A) Changing a `namedtuple` field raises `AttributeError`; use `._replace()` instead.
  - B) A `namedtuple` is still a tuple, so item assignment raises `TypeError`.
  - C) `update` is a dictionary/set method; a `namedtuple` does not have it.
</details>

---

### Question 23

**QE scenario:** after a test run you want the tests that **ran but were never planned**.

```python
planned = {"TC-001", "TC-002", "TC-003"}
executed = {"TC-001", "TC-002", "TC-099"}
```

Which expression gives `{'TC-099'}`?

- [ ] A) `planned - executed`
- [ ] B) `executed - planned`
- [ ] C) `planned & executed`
- [ ] D) `planned | executed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `executed - planned`

**Explanation:** `executed - planned` keeps items that were executed but are not in the plan. (The reverse, `planned - executed`, gives the tests you forgot to run.)
- **Why others are wrong:**
  - A) `planned - executed` gives the **missed** tests: `{'TC-003'}`.
  - C) `&` is the intersection, the tests that were both planned and executed.
  - D) `|` is the union, every test that appears in either set.
</details>

---

### Question 24

A spreadsheet export contains rows (dictionaries) with repeated `"id"` values. What is the correct way to keep only the first row for each ID?

- [ ] A) `unique_rows = set(rows)`
- [ ] B) `rows.sort()`
- [ ] C) Keep a `seen_ids` set and append a row only if its `"id"` is not in it
- [ ] D) `Counter(rows)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Keep a `seen_ids` set and append a row only if its `"id"` is not in it

**Explanation:** Dictionaries are mutable and unhashable, so they cannot go into a set. Track uniqueness with a set of the field's values (the IDs) instead.
- **Why others are wrong:**
  - A) Putting dictionaries in a set raises `TypeError: unhashable`.
  - B) Sorting only reorders the rows; it never removes duplicates.
  - D) `Counter` cannot count unhashable items such as dictionaries.
</details>

---

### Question 25

**QE scenario:** a data-driven test loops over a table of `(input, expected)` tuples. Your team wants to add a new check case. What should change?

- [ ] A) Add a new `if` branch to the loop for that case
- [ ] B) Copy the whole loop and edit the copy
- [ ] C) Write a new function for the case and call it separately
- [ ] D) Add one more line (row) of data to the table

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Add one more line (row) of data to the table

**Explanation:** Data-driven tests keep the logic fixed and put the variety in the data, so adding a case means adding a row, not new logic.
- **Why others are wrong:**
  - A) Adding branches puts the variety into the logic, the opposite of the data-driven idea.
  - B) Copying the loop duplicates logic; the same loop already handles every row.
  - C) A separate function per case also multiplies logic instead of growing the table.
</details>

---

### Question 26

In Git, what exactly is a **branch**?

- [ ] A) A movable label (pointer) that points at a commit
- [ ] B) A complete copy of every file in the project
- [ ] C) A separate repository stored on the server
- [ ] D) A list of the files you changed since the last commit

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A movable label (pointer) that points at a commit

**Explanation:** Creating a branch does not copy files; it only creates a lightweight pointer, which is why branches are cheap and fast. `HEAD` marks which branch you are on.
- **Why others are wrong:**
  - B) Branches do not copy your files; they are only pointers to commits.
  - C) A branch lives inside the same repository; it is not a separate repository.
  - D) Changed files are shown by `git status`; a branch is a pointer, not a list of changes.
</details>

---

### Question 27

You finished `feature/data-manager` and want its commits merged into `main` **locally**. Which sequence is correct?

- [ ] A) `git switch feature/data-manager`, then `git merge main`
- [ ] B) `git switch -c main`, then `git merge feature/data-manager`
- [ ] C) `git switch main`, then `git merge feature/data-manager`
- [ ] D) `git branch -d feature/data-manager`, then `git merge`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `git switch main`, then `git merge feature/data-manager`

**Explanation:** You always run `git merge` while on the branch that should **receive** the changes, so switch to `main` first and merge the feature branch into it.
- **Why others are wrong:**
  - A) This does the reverse: it brings `main`'s commits into the feature branch.
  - B) `main` already exists, so `-c` would fail with "a branch named ... already exists"; you only need `git switch main`.
  - D) `-d` deletes a branch and refuses if it is not merged; deleting is a clean-up step after merging, not a way to merge.
</details>

---

### Question 28

You run `git branch -d feature/experiment` and Git says `error: The branch is not fully merged`. If you still want to keep the work, what should you do?

- [ ] A) Run `git branch -D feature/experiment` straight away
- [ ] B) Merge the branch first; use `-D` only if you really want to discard it
- [ ] C) Run `git fetch --prune`
- [ ] D) Run `git merge --abort`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Merge the branch first; use `-D` only if you really want to discard it

**Explanation:** `-d` is the safe delete and refuses to delete unmerged work. Merge first; force-delete with `-D` only when you are certain you want to throw the work away.
- **Why others are wrong:**
  - A) `-D` force-deletes and would throw the unmerged work away.
  - C) `git fetch --prune` only removes stale remote-tracking references; it does not affect local branches.
  - D) `git merge --abort` cancels a merge in progress; no merge is in progress here.
</details>

---

## Part 2: True / False

### Question 29

`single = (5)` creates a tuple containing one item.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Without a trailing comma, `(5)` is just the integer 5 in brackets. It is the comma that makes a tuple: `(5,)`.
</details>

---

### Question 30

Reading a missing key from a `defaultdict(list)`, for example `groups["unknown"]`, adds that key to the dictionary.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A `defaultdict` creates the default value and stores it on lookup, so even a harmless read adds an entry. Use `"key" in groups` to check without creating.
</details>

---

### Question 31

Running `git branch feature/login` creates the new branch **and** switches you onto it.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `git branch name` only creates the branch and you stay on your current one. Use `git switch -c name` (or `git checkout -b name`) to create and switch.
</details>

---

### Question 32

For `numbers = [10, 20, 30]`, the slice `numbers[1:100]` runs without error and returns `[20, 30]`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Slices never raise `IndexError`; they quietly stop at the end of the sequence. Single-item indexing such as `numbers[100]` would raise it.
</details>

---

### Question 33

For `c = Counter(["PASS", "FAIL"])`, reading `c["BLOCKED"]` raises a `KeyError` because `"BLOCKED"` was never counted.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A `Counter` returns `0` for a missing item instead of raising `KeyError`, and it does not add the key. That is handy for reports.
</details>

---

### Question 34

Calling `discard("missing")` on a set that does not contain `"missing"` raises no error.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `discard` removes an item if present and silently does nothing if not. `remove`, by contrast, raises `KeyError` when the item is missing.
</details>

---

### Question 35

Like a list, a string can be changed in place: `text[0] = "X"` replaces its first character.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Strings are immutable, so `text[0] = "X"` raises a `TypeError`. To "change" a string, build a new one, for example `"X" + text[1:]`.
</details>

---

### Question 36

A `deque` supports slicing such as `recent[0:2]`, just like a list.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A `deque` supports `len`, `in`, looping and `queue[0]`, but slicing raises a `TypeError`. Convert it first with `list(d)[...]`.
</details>

---

### Question 37

Calling `sorted()` on a tuple returns another tuple.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `sorted()` always returns a new **list**, whatever collection you give it. Convert back with `tuple(...)` if you need a tuple.
</details>

---

### Question 38

A tuple such as `("Chrome", 120)` can be used as a dictionary key, but a list such as `["Chrome", 120]` cannot.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Dictionary keys must be immutable (hashable). Tuples qualify, while a list raises `TypeError: unhashable type`.
</details>

---

### Question 39

A merge conflict means something has gone wrong and the repository is now broken.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A conflict is not an error and nothing is broken; Git is simply asking a human to decide because the same lines were changed differently on both branches. You can resolve it, or back out with `git merge --abort`.
</details>

---

### Question 40

A fast-forward merge does not create a new commit.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** In a fast-forward merge Git just slides the target branch's pointer forward, so history stays linear and no merge commit is created. Only a three-way merge (or `--no-ff`) records a merge commit.
</details>

---

### Question 41

You can store several test-case dictionaries in a set to remove duplicate test cases automatically.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Dictionaries are mutable and unhashable, so they cannot go into a set (`TypeError: unhashable`). Keep a set of IDs instead.
</details>

---

### Question 42

`test_case["owner"] = "Priya"` adds the key `owner` if it does not exist, and replaces its value if it does.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The same `dict[key] = value` syntax both adds and updates: an existing key has its value replaced, otherwise a new pair is created.
</details>

---

## Part 3: Code Prediction

*Predict the exact output, then open the solution.*

### Question 43

**QE scenario:** de-duplicating test IDs while keeping first-seen order. What is printed?

```python
raw = ["TC-003", "TC-001", "TC-003", "TC-002", "TC-001"]
seen = set()
unique = []

for test_id in raw:
    if test_id not in seen:
        seen.add(test_id)
        unique.append(test_id)

print(unique, len(raw) - len(unique))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
['TC-003', 'TC-001', 'TC-002'] 2
```

**Explanation:** The `seen` set filters repeats while the list keeps first-seen order; 5 raw items minus 3 unique items leaves 2 duplicates.
</details>

---

### Question 44

What is printed?

```python
test_id = "TC-LOGIN-007"

print(test_id[3:8], int(test_id[-3:]) + 1)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
LOGIN 8
```

**Explanation:** `[3:8]` takes indexes 3 to 7 (the module name; the stop index is excluded), and `[-3:]` gives `"007"`, which `int()` turns into 7 before adding 1.
</details>

---

### Question 45

What is printed?

```python
results = ["PASS", "PASS", "FAIL", "PASS"]

results[1:3] = ["A", "B", "C"]

print(results, len(results))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
['PASS', 'A', 'B', 'C', 'PASS'] 5
```

**Explanation:** Assigning to a slice replaces indexes 1 and 2 with the three new items; the replacement can be a different length, so the list grows from 4 to 5 items.
</details>

---

### Question 46

What is printed?

```python
a = [1, 2]
a.append([3, 4])

b = [1, 2]
b.extend([3, 4])

print(len(a), len(b), a[-1])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
3 4 [3, 4]
```

**Explanation:** `append` adds the whole list as ONE item (length 3, last item is `[3, 4]`), while `extend` adds each item individually (length 4).
</details>

---

### Question 47

**QE scenario:** summarising test statuses. What is printed?

```python
from collections import Counter

statuses = ["PASS", "FAIL", "PASS", "SKIP", "PASS", "FAIL"]
c = Counter(statuses)

print(c.most_common(2))
print(c["BLOCKED"], len(c))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
[('PASS', 3), ('FAIL', 2)]
0 3
```

**Explanation:** `most_common(2)` returns a list of `(item, count)` tuples from highest to lowest count. A missing item such as `"BLOCKED"` gives 0 (no `KeyError`) and is not added, so `len(c)` stays 3 distinct statuses.
</details>

---

### Question 48

**QE scenario:** grouping tests by module. What is printed?

```python
from collections import defaultdict

tests = [("TC-001", "login"), ("TC-002", "search"),
         ("TC-003", "login"), ("TC-004", "cart")]

groups = defaultdict(list)
for test_id, module in tests:
    groups[module].append(test_id)

print(groups["profile"])
print(len(groups), groups["login"])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
[]
4 ['TC-001', 'TC-003']
```

**Explanation:** Looking up the missing key `"profile"` returns an empty list and also creates that key, so `groups` ends up with 4 keys (login, search, cart, profile).
</details>

---

### Question 49

**QE scenario:** keeping only the most recent log lines. What is printed?

```python
from collections import deque

recent = deque(maxlen=3)
for n in range(1, 6):
    recent.append(f"log{n}")

print(list(recent), recent[0])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
['log3', 'log4', 'log5'] log3
```

**Explanation:** With `maxlen=3`, old items fall off the left as new ones are appended, so only `log3`, `log4` and `log5` remain; `recent[0]` is the oldest remaining line.
</details>

---

### Question 50

**QE scenario:** editing one test-case record. What is printed?

```python
test_case = {"id": "TC-001", "priority": "High"}
test_case["priority"] = "Critical"
test_case["owner"] = "Priya"
del test_case["id"]

print(test_case, len(test_case))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
{'priority': 'Critical', 'owner': 'Priya'} 2
```

**Explanation:** `priority` is replaced, `owner` is added as a new key, and `del` removes `id`, leaving two entries in insertion order.
</details>

---

### Question 51

What is printed?

```python
original = [1, 2, 3]
alias = original
backup = original.copy()

alias.append(4)

print(original, backup)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
[1, 2, 3, 4] [1, 2, 3]
```

**Explanation:** `alias = original` is just a second name for the same list, so appending through `alias` changes `original` too. `.copy()` made an independent list, so `backup` is unchanged.
</details>

---

### Question 52

A flat list alternates test IDs and statuses. What is printed?

```python
data = ["TC-001", "PASS", "TC-002", "FAIL", "TC-003", "PASS"]

print(data[::2])
print(data[1::2][::-1])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
['TC-001', 'TC-002', 'TC-003']
['PASS', 'FAIL', 'PASS']
```

**Explanation:** `data[::2]` takes every second item starting at index 0 (the IDs). `data[1::2]` takes every second item starting at index 1 (`['PASS', 'FAIL', 'PASS']`), and `[::-1]` reverses that, which happens to read the same.
</details>

---

### Question 53

Reformatting a date by slicing. What is printed?

```python
date_text = "2025-12-31"

print(f"{date_text[8:]}.{date_text[5:7]}.{date_text[:4]}")
print(int(date_text[:4]) + 1)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
31.12.2025
2026
```

**Explanation:** `[8:]` gives the day `"31"`, `[5:7]` the month `"12"` and `[:4]` the year `"2025"`. Slices of strings are strings, so `int()` is needed before adding 1 to the year.
</details>

---

### Question 54

**QE scenario:** comparing two runs with `Counter` subtraction. What is printed?

```python
from collections import Counter

before = Counter({"PASS": 8, "FAIL": 2})
after = Counter({"PASS": 9, "FAIL": 1})

print(after - before)
print(before - after)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
Counter({'PASS': 1})
Counter({'FAIL': 1})
```

**Explanation:** Subtracting counters keeps only positive results: `after - before` shows what increased (one more PASS) and `before - after` shows what decreased (one fewer FAIL). Zero and negative results are dropped.
</details>

---

### Question 55

What is printed?

```python
from collections import namedtuple

TestResult = namedtuple("TestResult", ["test_id", "status", "duration"])

result = TestResult("TC-001", "PASS", 1.2)
slower = result._replace(duration=2.5)

print(result.duration, slower.duration)
print(slower.status, slower[0])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
1.2 2.5
PASS TC-001
```

**Explanation:** `_replace` returns a modified **copy**, so the original keeps `1.2`. Fields can be read by name (`slower.status`) or by index (`slower[0]`).
</details>

---

### Question 56

**QE scenario:** validating records against required fields. What is printed?

```python
required = {"id", "title", "priority"}
records = [
    {"id": "TC-010", "title": "Reset"},
    {"id": "TC-011", "title": "Email", "priority": "Low"},
]

for rec in records:
    missing = required - set(rec.keys())
    print(rec["id"], sorted(missing))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
TC-010 ['priority']
TC-011 []
```

**Explanation:** Set difference gives the required fields each record lacks. The first record has no `priority`; the second has all required fields, so its difference is empty.
</details>

---

### Question 57

What is printed?

```python
names = ["login", "Search", "api", "Checkout"]

print(sorted(names))
print(sorted(names, key=len))
print(names)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
['Checkout', 'Search', 'api', 'login']
['api', 'login', 'Search', 'Checkout']
['login', 'Search', 'api', 'Checkout']
```

**Explanation:** Sorting strings is case-sensitive, so uppercase names come before lowercase ones. With `key=len` the names are ordered by length. `sorted()` returns a new list, so `names` is unchanged.
</details>

---

### Question 58

**QE scenario:** parsing one CSV-style result line. What is printed?

```python
line = "TC-004,search,FAIL,2.1"

test_id, module, status, seconds = line.split(",")

print(module, status == "FAIL", float(seconds) * 2)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 
```text
search True 4.2
```

**Explanation:** `split(",")` returns four pieces that unpack into four variables. `seconds` is still text, so `float()` converts it before multiplying (2.1 * 2 = 4.2).
</details>

---

## Part 4: Fill-in-the-Blank

### Question 59

A test case is stored as `test_case = {"id": "TC-001"}`. To read the owner safely and get `"Unassigned"` when the key is missing (instead of a `KeyError`), write:

```python
owner = test_case.________("owner", "Unassigned")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `get`

**Explanation:** `.get(key, default)` returns the default when the key is absent instead of raising `KeyError`.
</details>

---

### Question 60

`queue` is a list of test IDs. To add **each item** of `["TC-005", "TC-006"]` to it individually (not as one nested list), call:

```python
queue.________(["TC-005", "TC-006"])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `extend`

**Explanation:** `extend` adds each item from another collection, whereas `append` would add the whole list as a single nested item.
</details>

---

### Question 61

Which set operator finds the tests that were planned but **not** executed?

```python
planned = {"TC-001", "TC-002", "TC-003"}
executed = {"TC-002"}
missed = planned ___ executed
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-` (set difference)

**Explanation:** `planned - executed` gives items in `planned` but not in `executed`, which is exactly the tests you forgot to run.
</details>

---

### Question 62

Complete the Git command that creates a new branch called `feature/data-manager` **and** switches to it:

```bash
git switch ____ feature/data-manager
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-c`

**Explanation:** `git switch -c name` creates the branch and switches to it in one step; the older equivalent is `git checkout -b name`.
</details>

---

### Question 63

Create a tuple that holds exactly **one** item, the number 5. Complete the line:

```python
a_tuple = (5__)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `,` (a trailing comma, giving `(5,)`)

**Explanation:** It is the comma that makes a tuple. `(5)` is just the integer 5 in brackets.
</details>

---

### Question 64

Which operator finds the tests that were **both** planned and executed?

```python
planned = {"TC-001", "TC-002", "TC-003"}
executed = {"TC-002", "TC-003", "TC-099"}
completed = planned ___ executed
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `&` (intersection)

**Explanation:** `planned & executed` keeps the items present in both sets, here `{'TC-002', 'TC-003'}`, the tests that were completed as planned.
</details>

---

### Question 65

Complete the counting pattern so that a missing key is inserted with the value `0` before the increment:

```python
counts = {}
for status in ["PASS", "FAIL", "PASS"]:
    counts.________(status, 0)
    counts[status] += 1
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `setdefault`

**Explanation:** `setdefault(key, default)` returns the value for the key and, if the key is absent, first inserts it with the default, so `counts[status] += 1` never hits a `KeyError`.
</details>

---

### Question 66

Fill in the slice that returns only the **last 3** results:

```python
recent = results[____]
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-3:`

**Explanation:** `s[-n:]` returns the last n items as a new list, so `results[-3:]` gives the three most recent results.
</details>

---

### Question 67

Fill in the slice that reverses the word without changing it:

```python
word = "automation"
print(word[::____])    # noitamotua
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-1`

**Explanation:** A step of `-1` walks backwards through the sequence, producing a reversed copy.
</details>

---

### Question 68

**QE scenario:** tests waiting to run must be taken from the **front** of a `deque` in first-in-first-out order. Complete the call:

```python
from collections import deque

waiting = deque(["TC-1", "TC-2", "TC-3"])
current = waiting.________()
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `popleft`

**Explanation:** `popleft()` removes and returns the item at the left end, so tests run in the order they were queued. Plain `pop()` takes from the right end.
</details>

---

### Question 69

To group **unique** browsers under each module name (no repeated browser per module), create the dictionary with:

```python
from collections import defaultdict

browsers_by_module = defaultdict(________)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `set`

**Explanation:** `defaultdict(set)` creates an empty set for each new key, so adding the same browser twice keeps only one. Pass the type name without parentheses.
</details>

---

### Question 70

Publish a new local branch to GitHub and link it to its remote counterpart so later `git push` and `git pull` need no arguments:

```bash
git push ____ origin feature/data-manager
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-u`

**Explanation:** `-u` sets the upstream, linking the local branch to `origin/feature/data-manager`.
</details>

---

### Question 71

After `feature/data-manager` has been merged into `main`, delete it safely (Git refuses if it is not merged):

```bash
git branch ____ feature/data-manager
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-d`

**Explanation:** `-d` deletes a branch only if it has been merged. The capital `-D` forces deletion even when unmerged, so use it only when you want to throw the work away.
</details>

---

### Question 72

A teammate deleted a branch on GitHub, but your machine still lists `origin/feature/api-tests`. Complete the command that removes stale remote-tracking references:

```bash
git fetch ________
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--prune`

**Explanation:** `git fetch --prune` removes remote-tracking references whose branches no longer exist on the remote.
</details>

---
