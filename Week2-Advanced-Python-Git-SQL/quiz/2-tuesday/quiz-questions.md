# Daily Knowledge Check: Week2-Advanced-Python-Git-SQL — Tuesday: Exception Handling & File Processing

Try each question before opening the solution. Every question names the written lesson it comes from, so you can go back and re-read. Questions use only Monday and Tuesday content.

---

## Part 1: Multiple Choice

### 1. A script runs `{}["x"]` inside a `try` that has `except LookupError:` listed first and `except KeyError:` listed second. Which handler runs?
- [ ] A) The `KeyError` handler, because it is the more specific match
- [ ] B) The `LookupError` handler, because Python runs the first `except` that matches and `KeyError` is a child of `LookupError`
- [ ] C) Both handlers, from top to bottom
- [ ] D) Neither, because two handlers for related exceptions raise a `SyntaxError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The `LookupError` handler, because Python runs the first `except` that matches and `KeyError` is a child of `LookupError`

**Explanation:** Python checks `except` blocks from top to bottom and runs only the first match. A parent class also catches all its children, so the `KeyError` handler below it is unreachable. Put the most specific handler first.
- **Why others are wrong:**
  - A) Specificity does not matter to Python; order does. The specific handler only wins if it is listed first.
  - C) Only one `except` block ever runs for a single exception.
  - D) The code is valid; the handler order is a logic mistake, not a syntax error.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 2. A helper returns `-1` when it cannot divide (`b == 0`). Why does the lesson recommend raising an exception instead?
- [ ] A) Returning a value from a function is not allowed after an `if` statement
- [ ] B) Exceptions run faster than return values
- [ ] C) `-1` is not a valid Python number
- [ ] D) A caller cannot tell `-1` (error) from a legitimate `-1.0` result, and if the caller forgets to check, the bad value silently flows onward

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A caller cannot tell `-1` (error) from a legitimate `-1.0` result, and if the caller forgets to check, the bad value silently flows onward

**Explanation:** "Magic" error values are ambiguous and easy to ignore. An exception cannot be ignored by accident: if nobody handles it, the program stops loudly ("fail fast and fail loudly").
- **Why others are wrong:**
  - A) Returning from inside an `if` is perfectly normal.
  - B) Speed is not the reason given in the lesson.
  - C) `-1` is a valid number; the problem is its ambiguous meaning.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 3. Which definition follows the lesson's guidance for a custom exception that stores structured data and still prints a readable message?
- [ ] A) `class RowError(BaseException):` with `__init__` that sets attributes and never calls the parent
- [ ] B) `class RowError:` with an `__init__` that sets `self.row` and `self.message`
- [ ] C) `class RowError(Exception):` with an `__init__` that stores attributes such as `self.row`, then calls `super().__init__(message)`
- [ ] D) `class RowError(Exception):` with `__init__` that stores attributes only, because `str(error)` is built from the attributes automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `class RowError(Exception):` with an `__init__` that stores attributes such as `self.row`, then calls `super().__init__(message)`

**Explanation:** A custom exception inherits from `Exception`, stores any extra data as attributes, and calls `super().__init__(message)` so `str(error)` and the traceback show the message.
- **Why others are wrong:**
  - A) `BaseException` is reserved for things like `KeyboardInterrupt` and `SystemExit`; inheriting from it lets your errors escape `except Exception`. It also skips the parent call.
  - B) A class that does not inherit from `Exception` cannot be raised at all.
  - D) Without `super().__init__(message)` the printed message may be empty or show only raw arguments; Python does not build it from your attributes.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 4. A loader runs `assert age >= 0, "age must be non-negative"` on values read from a customer-supplied CSV. What is the main problem?
- [ ] A) Running Python with `-O` removes `assert` statements, so the check vanishes and bad data passes through; external data needs `if` plus `raise`
- [ ] B) `assert` can only compare strings, not numbers
- [ ] C) `assert` always stops the program, so no other rows could ever be processed
- [ ] D) A failed `assert` raises `ValueError`, which the loader cannot catch

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Running Python with `-O` removes `assert` statements, so the check vanishes and bad data passes through; external data needs `if` plus `raise`

**Explanation:** Assertions are developer aids for catching bugs in your own code and can be switched off. Bad external data can legitimately happen, so it is validation and must use an exception that is always active.
- **Why others are wrong:**
  - B) `assert` evaluates any condition.
  - C) An `AssertionError` can be caught; the real issue is that the check can be disabled.
  - D) A failed `assert` raises `AssertionError`, not `ValueError`.

**Source:** `assertions.md`
</details>

---

### 5. A nightly job must add a line to `run_log.txt` each run while keeping all earlier lines. Which `open()` mode should it use?
- [ ] A) `"w"`
- [ ] B) `"a"`
- [ ] C) `"x"`
- [ ] D) `"r"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `"a"`

**Explanation:** Append mode writes at the end of the file, keeps existing content, and creates the file if it does not exist.
- **Why others are wrong:**
  - A) `"w"` erases all existing content the moment the file is opened.
  - C) `"x"` raises `FileExistsError` if the file already exists, so the second run would fail.
  - D) `"r"` is read-only and raises `FileNotFoundError` if the file is missing.

**Source:** `reading-and-writing-files.md`
</details>

---

### 6. Why do the lessons tell you to open CSV files with `newline=""`?
- [ ] A) It makes Python skip the header row automatically
- [ ] B) It converts every value to an integer where possible
- [ ] C) It is only needed when the CSV uses a semicolon delimiter
- [ ] D) It stops Python's automatic newline translation from interfering with the `csv` module's own handling of line endings and line breaks inside quoted values

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It stops Python's automatic newline translation from interfering with the `csv` module's own handling of line endings and line breaks inside quoted values

**Explanation:** The `csv` documentation requires `newline=""`. Forgetting it can produce blank lines between rows on Windows or corrupt multi-line values.
- **Why others are wrong:**
  - A) Skipping the header is done with `next(reader)` or by using `DictReader`.
  - B) The `csv` module returns every value as a string; type conversion is your job.
  - C) It applies to all CSV files, whatever the delimiter.

**Source:** `csv-json-and-xml.md`
</details>

---

### 7. Given `<testcase id="TC1" status="pass"><title>Valid login</title></testcase>` parsed with `case = ET.fromstring(...)`, which expressions return `"TC1"` and `"Valid login"` respectively?
- [ ] A) `case.get("id")` and `case.find("title").text`
- [ ] B) `case.text` and `case.attrib`
- [ ] C) `case.find("id").text` and `case.get("title")`
- [ ] D) `case.attrib("id")` and `case.title`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `case.get("id")` and `case.find("title").text`

**Explanation:** Attributes live inside the opening tag and are read with `.get("name")` (or the `.attrib` dictionary). Text sits between tags and is read from the child element with `.find("title").text`.
- **Why others are wrong:**
  - B) `case.text` is the text directly inside `<testcase>` (not the id), and `.attrib` is the whole dictionary of attributes, not one value.
  - C) `id` is an attribute, not a child element, so `find("id")` returns `None`; `title` is a child element, not an attribute.
  - D) `.attrib` is a dictionary attribute, not a method, so it is not called; and `case.title` is not how children are accessed.

**Source:** `csv-json-and-xml.md`
</details>

---

### 8. What is printed by `with announce("outer"), announce("inner"): print("inside")`, if `announce(name)` prints `[enter] name` on entry and `[exit] name` on exit?
- [ ] A) enter outer, exit outer, enter inner, exit inner, inside
- [ ] B) enter outer, enter inner, inside, exit outer, exit inner
- [ ] C) enter outer, enter inner, inside, exit inner, exit outer
- [ ] D) enter inner, enter outer, inside, exit outer, exit inner

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) enter outer, enter inner, inside, exit inner, exit outer

**Explanation:** Managers listed in one `with` are entered left to right and exited in reverse order, like nested blocks. The last resource opened is the first one closed.
- **Why others are wrong:**
  - A) Each manager stays open for the whole block; `outer` does not exit before `inner` starts.
  - B) Exit order is reversed, not the same as entry order.
  - D) Entry is left to right, so `outer` is entered first.

**Source:** `context-managers.md`
</details>

---

### 9. A test parses `<testcase id="2"/>` and runs `case.find("message").text`. The element has no `<message>` child. What happens?
- [ ] A) It returns an empty string `""`
- [ ] B) `find` returns `None`, so `.text` raises `AttributeError`
- [ ] C) `find` raises `KeyError`
- [ ] D) It returns the string `"None"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `find` returns `None`, so `.text` raises `AttributeError`

**Explanation:** `find()` returns `None` when nothing matches, and `None.text` is an `AttributeError`. Check with `is not None` or use `findtext("message", default=...)`.
- **Why others are wrong:**
  - A) No element means no text; nothing is returned as an empty string.
  - C) `KeyError` is for dictionary keys; `find` does not raise it.
  - D) The value is the object `None`, not the text `"None"`.

**Source:** `csv-json-and-xml.md`
</details>

---

### 10. A traceback shows three frames (`<module>`, then `total`, then `parse_price`) followed by the line `ValueError: could not convert string to float: 'abc'`. Where did the error actually occur, and where should you start reading?
- [ ] A) In `<module>`, the top frame, because the first frame listed is the cause
- [ ] B) In `total`, because it is the function that called the failing code
- [ ] C) In `parse_price`, the bottom frame; start at the last line, which gives the exception type and message
- [ ] D) A traceback cannot locate the error; only a debugger can

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) In `parse_price`, the bottom frame; start at the last line, which gives the exception type and message

**Explanation:** Read a traceback from the bottom up: the last line names the exception and its message, and the bottom-most frame is where the error was raised. The frames above it only show the chain of callers that led there.
- **Why others are wrong:**
  - A) The top frame is the outermost caller (the main body of the script); it shows how execution got there, not where it failed.
  - B) `total` merely called `parse_price`; the error was raised one level deeper, in the bottom frame.
  - D) A traceback lists the file, line number, function name and source line for every frame in the call chain.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 11. A function runs `int(record["quantity"])` inside a `try` whose handlers are, in order, `except KeyError`, `except ValueError` and `except TypeError`. The record is `{"quantity": None}`. Which handler runs?
- [ ] A) `TypeError`, because `int(None)` is an operation on the wrong type of object
- [ ] B) `KeyError`, because the value is `None`, which means "missing"
- [ ] C) `ValueError`, because `None` is not a valid number
- [ ] D) None of them; `int(None)` quietly returns `0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `TypeError`, because `int(None)` is an operation on the wrong type of object

**Explanation:** The key exists, so no `KeyError` occurs, and `None` is the wrong kind of object rather than a badly formed string, so Python raises `TypeError`. The lesson's `read_quantity` example prints "Quantity has an unusable type: None" for exactly this record.
- **Why others are wrong:**
  - B) `KeyError` is raised only when the key itself is absent; here the key is present with the value `None`.
  - C) `ValueError` means the right type with an unacceptable value (like `"seven"`); `None` is the wrong type altogether.
  - D) `int(None)` does not return a default; it raises an exception.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 12. Why does the lesson call a bare `except:` one of the worst habits you can form?
- [ ] A) It is a syntax error in Python 3, so the script never starts
- [ ] B) It only catches `ValueError` unless you list other types
- [ ] C) It stops the `finally` block from running
- [ ] D) It catches everything, including `KeyboardInterrupt` and `SystemExit`, and it hides mistakes such as a `NameError` caused by a misspelled variable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It catches everything, including `KeyboardInterrupt` and `SystemExit`, and it hides mistakes such as a `NameError` caused by a misspelled variable

**Explanation:** A bare `except:` has no filter, so Ctrl+C cannot stop the program and genuine bugs are silently swallowed while the code appears to work. Catch specific exceptions instead.
- **Why others are wrong:**
  - A) It is legal syntax; that is exactly why it is dangerous.
  - B) A bare `except:` catches every exception, not just `ValueError`.
  - C) `finally` still runs; the problem is that errors are hidden, not that cleanup is skipped.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 13. A helper `set_browser(name)` should accept only text. A caller passes the integer `42`. Which built-in exception does the lesson recommend raising?
- [ ] A) `ValueError`
- [ ] B) `TypeError`
- [ ] C) `KeyError`
- [ ] D) `NotImplementedError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `TypeError`

**Explanation:** An argument of the wrong type is a `TypeError`; the lesson checks `isinstance(name, str)` first and only then checks the value.
- **Why others are wrong:**
  - A) `ValueError` is for the right type with an unacceptable value, such as the string `"netscape"`.
  - C) `KeyError` is for a missing key in a mapping.
  - D) `NotImplementedError` is a placeholder meaning "a subclass must write this"; it says nothing about bad arguments.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 14. Inside an `except FileNotFoundError:` block, a function prints a log line and then executes a bare `raise`. What does its caller receive?
- [ ] A) The original `FileNotFoundError`, with its original traceback intact
- [ ] B) A new generic `Exception` with an empty message
- [ ] C) Nothing, because the exception is discarded after the log line
- [ ] D) A `SyntaxError`, because `raise` always needs an argument

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The original `FileNotFoundError`, with its original traceback intact

**Explanation:** A bare `raise` re-throws the exception currently being handled. It lets you observe a failure (log it) without deciding its outcome.
- **Why others are wrong:**
  - B) A bare `raise` creates nothing new; it re-throws the same exception object.
  - C) Only finishing the handler without `raise` would swallow it; `raise` deliberately lets it continue.
  - D) A bare `raise` is valid inside an `except` block; that is precisely where it is meant to be used.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 15. A module defines `DataIngestionError` with the children `SourceNotFoundError`, `UnsupportedFormatError` and `ValidationError`; `MissingFieldError` inherits from `ValidationError`. A caller wants one handler for everything the module can raise, without hiding programming bugs such as `NameError`. Which handler fits?
- [ ] A) `except MissingFieldError:`
- [ ] B) `except ValidationError:`
- [ ] C) `except DataIngestionError:`
- [ ] D) `except Exception:`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `except DataIngestionError:`

**Explanation:** Catching the module's base class handles every exception derived from it, while leaving unrelated errors like `NameError` free to surface. This is why one base exception per module is recommended.
- **Why others are wrong:**
  - A) That catches only one grandchild, not the other exceptions in the module.
  - B) It covers `ValidationError` and `MissingFieldError` but misses `SourceNotFoundError` and `UnsupportedFormatError`.
  - D) It also swallows genuine programming bugs such as `NameError`, which is what the base class avoids.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 16. Which of these assertions is unsafe because it contains a side effect that disappears under `python -O`?
- [ ] A) `assert len(queue) == 3, f"expected 3 items, got {len(queue)}"`
- [ ] B) `assert "first" in queue`
- [ ] C) `assert isinstance(queue, list)`
- [ ] D) `assert queue.pop() == "first"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `assert queue.pop() == "first"`

**Explanation:** `-O` removes the whole `assert` statement, so the `pop()` would never happen and the program's behaviour would change. Do the action first, then assert on the result.
- **Why others are wrong:**
  - A) It only reads the list; removing it changes nothing about the data.
  - B) A membership test is read-only, so it has no side effect to lose.
  - C) A type check is read-only and harmless to remove.

**Source:** `assertions.md`
</details>

---

### 17. Which situation should use an `assert` rather than `if` plus `raise`?
- [ ] A) Rejecting an age that a user typed into a form
- [ ] B) After computing an average, confirming that the result lies between the minimum and maximum of the list
- [ ] C) Detecting a negative price in a customer-supplied CSV
- [ ] D) Reporting that a required data file is missing

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) After computing an average, confirming that the result lies between the minimum and maximum of the list

**Explanation:** That is an internal sanity check on our own logic: if it fails, our code is wrong. Situations that can legitimately happen with outside data need exceptions that cannot be disabled.
- **Why others are wrong:**
  - A) User input is external and can legitimately be wrong, so it needs an always-active exception.
  - C) File data comes from outside the program; this is validation, which must work even under `-O`.
  - D) A missing file is an expected runtime problem, handled with `FileNotFoundError` and `try`/`except`.

**Source:** `assertions.md`
</details>

---

### 18. Which failure message is the most actionable for a check on an HTTP status code?
- [ ] A) `"expected status 200 but got 500 for /login"`
- [ ] B) `"bad value"`
- [ ] C) `"Assertion failed!"`
- [ ] D) `"Check the server"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `"expected status 200 but got 500 for /login"`

**Explanation:** A good assertion message states what was expected and what was found, so the reader can act without opening the code.
- **Why others are wrong:**
  - B) It says something is wrong but not which value or what was expected.
  - C) The traceback already says the assertion failed; the message adds no information.
  - D) It guesses a cause without reporting the expected and actual values.

**Source:** `assertions.md`
</details>

---

### 19. You must count the `ERROR` lines in a 5 GB log file without running out of memory. Which approach does the lesson recommend?
- [ ] A) Call `f.read()` and search the resulting string
- [ ] B) Call `f.readlines()` and loop over the list
- [ ] C) Loop with `for line in f:`, which reads the file in small pieces
- [ ] D) Call `f.read().splitlines()` and loop over the result

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Loop with `for line in f:`, which reads the file in small pieces

**Explanation:** A file object is iterable and yields one line at a time, so memory use stays very low however large the file is.
- **Why others are wrong:**
  - A) `read()` loads the entire file into memory as one string.
  - B) `readlines()` builds a list of every line at once, so the whole file sits in memory.
  - D) It still reads the whole file first before splitting it.

**Source:** `reading-and-writing-files.md`
</details>

---

### 20. Why does the lesson say to always write `encoding="utf-8"` when opening text files?
- [ ] A) Without it, `open()` raises an error and refuses to open the file
- [ ] B) UTF-8 is the only encoding that works with mode `"w"`
- [ ] C) It makes Python read and write files faster
- [ ] D) The default encoding depends on the platform, so a file may fail to decode or show garbled characters on another machine

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The default encoding depends on the platform, so a file may fail to decode or show garbled characters on another machine

**Explanation:** Being explicit makes the code behave identically everywhere. UTF-8 is the modern universal standard that can represent every language and symbol.
- **Why others are wrong:**
  - A) Python falls back to a platform default; it does not refuse.
  - B) Any supported encoding works with any mode; the mode controls reading or writing, not the character set.
  - C) Encoding choice is about correct characters, not speed.

**Source:** `reading-and-writing-files.md`
</details>

---

### 21. A script opens the relative path `"data/users.csv"`. It works from the editor but raises `FileNotFoundError` when started from another folder. What is the likely cause and the robust fix?
- [ ] A) Forward slashes do not work on Windows, so switch to backslashes
- [ ] B) Relative paths depend on the current working directory; build the path from `Path(__file__).resolve().parent` instead
- [ ] C) The file is locked by the editor, so open it with mode `"x"`
- [ ] D) The encoding is missing, so add `encoding="utf-8"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Relative paths depend on the current working directory; build the path from `Path(__file__).resolve().parent` instead

**Explanation:** A relative path is resolved against the folder the program was started from. Anchoring the path to the script's own location removes the "works on my machine" problem.
- **Why others are wrong:**
  - A) Python accepts forward slashes on Windows; the slash style is not the problem.
  - C) Mode `"x"` raises `FileExistsError` for existing files and would not help; a lock is not the cause.
  - D) A wrong encoding causes garbled text or `UnicodeDecodeError`, not `FileNotFoundError`.

**Source:** `reading-and-writing-files.md`
</details>

---

### 22. What happens when you run `f.write(42)` on a text file opened for writing?
- [ ] A) It raises `TypeError`, because `write()` accepts only strings; use `str(42)`
- [ ] B) It writes the text `42` to the file
- [ ] C) It writes the character whose code is 42
- [ ] D) It silently writes nothing and returns `0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It raises `TypeError`, because `write()` accepts only strings; use `str(42)`

**Explanation:** `write()` does no automatic conversion, so numbers must be turned into text first, for example `f.write(str(42))`.
- **Why others are wrong:**
  - B) There is no automatic conversion to text.
  - C) `write()` does not interpret integers as character codes.
  - D) Passing a non-string is an error, not a silent no-op.

**Source:** `reading-and-writing-files.md`
</details>

---

### 23. After `data = json.loads('{"active": true, "manager": null, "tags": ["a"]}')`, which statement is correct?
- [ ] A) `data["active"]` is the string `"true"`, because JSON has no booleans
- [ ] B) `data` is a `str`, because `loads` returns the text unchanged
- [ ] C) `data["active"]` is `True`, `data["manager"]` is `None`, and `data["tags"]` is a `list`
- [ ] D) `data["manager"]` raises `KeyError`, because null values are dropped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `data["active"]` is `True`, `data["manager"]` is `None`, and `data["tags"]` is a `list`

**Explanation:** JSON `true`/`false` become `True`/`False`, `null` becomes `None`, arrays become lists and objects become dictionaries.
- **Why others are wrong:**
  - A) JSON does have `true` and `false`; they map to Python booleans.
  - B) `loads` parses the text; a JSON object becomes a `dict`.
  - D) `null` is kept and becomes `None`; the key is present.

**Source:** `csv-json-and-xml.md`
</details>

---

### 24. A test already holds an API response body as a Python string in the variable `text`. Which call turns it into Python objects?
- [ ] A) `json.load(text)`
- [ ] B) `json.loads(text)`
- [ ] C) `json.dumps(text)`
- [ ] D) `json.dump(text)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `json.loads(text)`

**Explanation:** `loads` ("load string") parses JSON text. The functions without the "s" work with file objects.
- **Why others are wrong:**
  - A) `load` expects a file object, not a string.
  - C) `dumps` goes the other way, turning Python objects into JSON text.
  - D) `dump` writes to a file object and needs one as its second argument.

**Source:** `csv-json-and-xml.md`
</details>

---

### 25. In `with Demo() as value:`, what is bound to `value`?
- [ ] A) Whatever the `__enter__` method returns
- [ ] B) The `Demo` object itself, always
- [ ] C) The value returned by `__exit__`
- [ ] D) The result of the last statement in the block

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Whatever the `__enter__` method returns

**Explanation:** The `as` variable receives the return value of `__enter__`. It is often `self`, but it can be any resource, such as an open connection or the number 42.
- **Why others are wrong:**
  - B) That is true only when `__enter__` happens to return `self`.
  - C) `__exit__`'s return value decides whether an exception is suppressed; it is never bound to a name.
  - D) The block's statements have no influence on what `as` receives.

**Source:** `context-managers.md`
</details>

---

### 26. A `with` block raises an exception and the manager's `__exit__` returns `True`. What happens?
- [ ] A) The exception propagates after cleanup, as normal
- [ ] B) The block resumes at the line after the one that failed
- [ ] C) Python raises a `RuntimeError` because `__exit__` must return `None`
- [ ] D) The exception is suppressed and execution continues after the `with` block, although the rest of the block is still skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The exception is suppressed and execution continues after the `with` block, although the rest of the block is still skipped

**Explanation:** Returning a true value from `__exit__` swallows the exception. The block was already abandoned at the point of failure, so its remaining lines never run.
- **Why others are wrong:**
  - A) That is the behaviour when `__exit__` returns `False` or `None`.
  - B) A block is never resumed; it is abandoned at the failing line.
  - C) Returning `True` is a documented feature for deliberately suppressing specific exceptions.

**Source:** `context-managers.md`
</details>

---

### 27. Which style of `@contextmanager` function guarantees cleanup even when the `with` block raises?
- [ ] A) Put the cleanup on the line right after `yield`
- [ ] B) Put the cleanup before the `yield`, with the setup
- [ ] C) Wrap the `yield` in `try` and put the cleanup in `finally`
- [ ] D) Use `return` instead of `yield`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Wrap the `yield` in `try` and put the cleanup in `finally`

**Explanation:** An exception from the block is re-raised at the `yield` line, so only a `finally` around the `yield` is certain to run the cleanup.
- **Why others are wrong:**
  - A) That line is skipped when the exception is re-raised at the `yield`.
  - B) That would tear the resource down before the block has used it.
  - D) A generator-based manager needs its single `yield` to hand control to the `with` block.

**Source:** `context-managers.md`
</details>

## Part 2: True / False

### 28. True or False: If the `else` block of a `try` statement raises an exception, the `except` clauses of that same `try` statement will catch it.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Exceptions raised inside `else` are not caught by the `except` clauses of the same `try`. That is the point of `else`: errors in your follow-up logic are not mistaken for the failure you were guarding against.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 29. True or False: `assert (1 == 2, "this should fail")` raises an `AssertionError` with that message.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Parentheses around both the condition and the message create a tuple, and a non-empty tuple is always truthy, so the assertion always passes. Write `assert 1 == 2, "this should fail"` instead (parentheses around the message only are fine).

**Source:** `assertions.md`
</details>

---

### 30. True or False: Opening an existing file with mode `"w"` erases its content immediately, even if you never write anything.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Mode `"w"` destroys existing content the instant the file is opened, before any write. Use `"a"` to add to a file or `"x"` to refuse to overwrite.

**Source:** `reading-and-writing-files.md`
</details>

---

### 31. True or False: `json.loads("{'name': 'Ada'}")` is valid, because JSON accepts single-quoted keys and strings just like Python.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** JSON has strict syntax: keys and strings must use double quotes, with no trailing commas and no comments. Single quotes raise `json.JSONDecodeError`, which is a subclass of `ValueError`.

**Source:** `csv-json-and-xml.md`
</details>

---

### 32. True or False: After a `with open(...) as f:` block ends, the name `f` still exists, but the file it refers to is closed.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The variable after `as` remains accessible after the block; the file object is merely closed, not deleted. `f.closed` is `True`.

**Source:** `context-managers.md`
</details>

---

### 33. True or False: In a function whose `try` block executes `return`, the `finally` block still runs before the function actually returns.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `finally` runs no matter what, including on the way out through a `return`. That is why `divide()` in the lesson prints `divide() finished` before the returned value appears.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 34. True or False: `raise NewError(...) from None` shows both the original and the new traceback, joined by "The above exception was the direct cause of the following exception".
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `from None` deliberately suppresses the chain, so only the new exception is shown. The "direct cause" wording appears with `raise ... from original`, which stores the original in `__cause__`.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 35. True or False: The message in `assert condition, message` is evaluated only when the assertion fails, so building it with an f-string costs nothing on success.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Python evaluates the message expression only after the condition has turned out false. That is why rich f-string messages are fine in assertions.

**Source:** `assertions.md`
</details>

---

### 36. True or False: `f.writelines(["alpha", "beta"])` writes each item on its own line.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `writelines()` does not add newlines, so the file would contain `alphabeta` on one line. The strings must include `\n` themselves, for example `["alpha\n", "beta\n"]`.

**Source:** `reading-and-writing-files.md`
</details>

---

### 37. True or False: When a CSV cell contains the text `false`, `bool(row["active"])` returns `False`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Every CSV value is a string, and any non-empty string is truthy, so `bool("false")` is `True`. Compare the text instead: `row["active"].strip().lower() == "true"`.

**Source:** `csv-json-and-xml.md`
</details>

---

### 38. True or False: `with suppress(FileNotFoundError):` also silences a `PermissionError` raised inside the block.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `suppress` ignores only the exception types you list, which is why it is safer than a broad `except`. A `PermissionError` is a different `OSError` child and would still propagate.

**Source:** `context-managers.md`
</details>

---

### 39. True or False: In `with A() as a, B() as b:`, `B` is exited before `A`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Managers are entered left to right and exited in reverse order, like nested blocks: the last resource opened is the first one closed.

**Source:** `context-managers.md`
</details>

## Part 3: Code Prediction

### 40. What does this code print?
```python
def lookup(data, key):
    try:
        print("start")
        value = int(data[key])
        print("converted")
    except KeyError:
        print("missing")
        return -1
    except ValueError:
        print("bad number")
        return -2
    else:
        print("ok")
        return value
    finally:
        print("done")

print(lookup({"qty": "seven"}, "qty"))
```
- [ ] A) `start`, `bad number`, `-2`
- [ ] B) `start`, `converted`, `ok`, `done`, `-2`
- [ ] C) `start`, `bad number`, `done`, `-2`
- [ ] D) `start`, `missing`, `done`, `-1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `start`, `bad number`, `done`, `-2`

**Explanation:** The key exists, but `int("seven")` raises `ValueError`, so `converted` is skipped and the `ValueError` handler prints and returns `-2`. `finally` still runs on the way out, so `done` prints before the returned value is printed.
- **Why others are wrong:**
  - A) It forgets that `finally` always runs, even when a handler executes `return`.
  - B) That is the path for a successful conversion; `converted` and `ok` are skipped here.
  - D) `data[key]` succeeds, so `KeyError` is never raised.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 41. What does this code print?
```python
class AppError(Exception):
    pass

def parse(t):
    try:
        return int(t)
    except ValueError as e:
        raise AppError(f"bad {t!r}") from e

try:
    parse("x1")
except AppError as err:
    print(err)
    print(type(err.__cause__).__name__)
    print(err.__cause__ is None)
```
- [ ] A) `bad 'x1'`, `ValueError`, `False`
- [ ] B) `bad 'x1'`, `AppError`, `False`
- [ ] C) the original `int()` error message, `ValueError`, `True`
- [ ] D) `bad 'x1'`, `None`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `bad 'x1'`, `ValueError`, `False`

**Explanation:** `raise ... from e` explicitly chains the exceptions: the new `AppError` carries the original `ValueError` in `__cause__`. `print(err)` shows the new, friendly message.
- **Why others are wrong:**
  - B) `__cause__` is the original low-level exception (`ValueError`), not the new one.
  - C) The caught exception is `AppError`, so its message is `bad 'x1'`; and the cause is present, so `is None` is `False`.
  - D) With `from e` the cause is set; only `from None` would suppress the chain.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 42. What does this code print?
```python
import math

try:
    assert 0.1 + 0.2 == 0.3, "float mismatch"
    print("passed")
except AssertionError as e:
    print("FAIL:", e)

print(math.isclose(0.1 + 0.2, 0.3))
```
- [ ] A) `passed`, `False`
- [ ] B) `FAIL: float mismatch`, `False`
- [ ] C) `passed`, `True`
- [ ] D) `FAIL: float mismatch`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `FAIL: float mismatch`, `True`

**Explanation:** Floating-point arithmetic is slightly inexact, so `0.1 + 0.2 == 0.3` is `False` and the assertion fails with the given message. `math.isclose` compares with a tolerance and returns `True`.
- **Why others are wrong:**
  - A) The assertion does not pass, and `isclose` is `True`.
  - B) `math.isclose(0.1 + 0.2, 0.3)` is `True`; that is its purpose.
  - C) The `==` comparison is `False`, so `passed` never prints.

**Source:** `assertions.md`
</details>

---

### 43. A file is created containing `a` and `b` on separate lines, then reopened in append mode to add `c`, then read as shown. What does this print?
```python
# file content after the write and append steps: "a\nb\nc\n"
with open(path, encoding="utf-8") as f:
    first = f.readline()
    rest = f.read()
    again = f.read()

print(repr(first))
print(len(rest.splitlines()))
print(repr(again))
```
- [ ] A) `'a\n'`, `3`, `''`
- [ ] B) `'a\n'`, `2`, `''`
- [ ] C) `'a'`, `2`, `''`
- [ ] D) `'a\n'`, `2`, `'b\nc\n'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `'a\n'`, `2`, `''`

**Explanation:** `readline()` returns the line including its trailing `\n`. `read()` then returns the rest from the current position (`b` and `c`, so 2 lines). The position is now at the end of the file, so a second `read()` returns an empty string.
- **Why others are wrong:**
  - A) `readline()` already consumed the first line, so only 2 lines remain.
  - C) `readline()` keeps the newline; only `strip()` would remove it.
  - D) File position advances as you read; the second `read()` returns nothing unless you `seek(0)`.

**Source:** `reading-and-writing-files.md`
</details>

---

### 44. What does this code print?
```python
import xml.etree.ElementTree as ET

root = ET.fromstring('<s name="Suite"><c id="1"><m>x</m></c><c id="2"/></s>')
print(root.tag, root.attrib)
for c in root.findall("c"):
    print(c.get("id"), c.findtext("m", default="none"), c.find("m") is not None)
```
- [ ] A) `s {}`, `1 x False`, `2 none True`
- [ ] B) `s {'name': 'Suite'}`, `1 x True`, then `AttributeError` on the second `<c>`
- [ ] C) `s {'name': 'Suite'}`, `1 x True`, `2 none False`
- [ ] D) `Suite {'name': 'Suite'}`, `1 x True`, `2 none False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `s {'name': 'Suite'}`, `1 x True`, `2 none False`

**Explanation:** `.tag` is the element name (`s`) and `.attrib` is a dictionary of its attributes. The first `<c>` has an `<m>` child, so `findtext` returns `x` and `find(...) is not None` is `True`. The second has none, so `findtext` returns the default `none` and the `is not None` test is `False`.
- **Why others are wrong:**
  - A) `.attrib` holds `name`, and the `True`/`False` values are swapped.
  - B) `findtext` with a default and the `is not None` test never touch `.text` on `None`, so nothing raises.
  - D) `.tag` is the tag name `s`; the attribute value `Suite` is not the tag.

**Source:** `csv-json-and-xml.md`
</details>

---

### 45. What does this code print?
```python
def f():
    try:
        print("A")
        {}["k"]
    except ValueError:
        print("B")
    else:
        print("C")
    finally:
        print("D")

try:
    f()
except KeyError:
    print("E")
print("F")
```
- [ ] A) `A`, `B`, `D`, `F`
- [ ] B) `A`, `D`, `E`, `F`
- [ ] C) `A`, `C`, `D`, `F`
- [ ] D) `A`, `E`, `D`, `F`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `A`, `D`, `E`, `F`

**Explanation:** The lookup raises `KeyError`, which does not match `except ValueError`, so neither `except` nor `else` runs. `finally` still runs as the exception leaves `f()`, and then the exception reaches the outer handler.
- **Why others are wrong:**
  - A) `ValueError` is not a parent of `KeyError`, so the `B` handler never matches.
  - C) `else` runs only when the `try` block finishes without an exception, and one was raised.
  - D) `finally` runs inside `f()` while the exception is still travelling upward, so `D` prints before the outer handler prints `E`.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 46. What does this code print?
```python
class InvalidRecordError(Exception):
    def __init__(self, row, field):
        self.row = row
        self.field = field
        super().__init__(f"Row {row}: bad {field!r}")

try:
    raise InvalidRecordError(17, "age")
except InvalidRecordError as e:
    print(e)
    print(e.row + 1)
    print(e.args)
```
- [ ] A) `Row 17: bad 'age'`, `18`, `("Row 17: bad 'age'",)`
- [ ] B) `InvalidRecordError`, `18`, `("Row 17: bad 'age'",)`
- [ ] C) `Row 17: bad 'age'`, `18`, `(17, 'age')`
- [ ] D) `Row 17: bad 'age'`, then a `TypeError` on `e.row + 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `Row 17: bad 'age'`, `18`, `("Row 17: bad 'age'",)`

**Explanation:** `print(e)` shows the message passed to `super().__init__`. `e.row` is the integer `17`, so adding 1 gives `18`, and `e.args` holds the arguments given to the parent constructor, which is just the message.
- **Why others are wrong:**
  - B) `print(e)` shows the message, not the class name.
  - C) `args` contains what was passed to `super().__init__` (the message), not the attributes you stored.
  - D) `row` was stored as the integer `17`, so adding `1` works.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 47. What does this code print?
```python
queue = ["a", "b"]
try:
    assert queue.pop() == "z", f"popped, left {queue}"
except AssertionError as e:
    print(e)
print(queue)
```
- [ ] A) `popped, left ['a', 'b']`, `['a', 'b']`
- [ ] B) `popped, left ['a']`, `['a', 'b']`
- [ ] C) `['a']` only, with no message
- [ ] D) `popped, left ['a']`, `['a']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `popped, left ['a']`, `['a']`

**Explanation:** The condition is evaluated first, so `pop()` removes `"b"` and the comparison with `"z"` fails. The message is built after that, so it shows the shortened list, and the side effect of `pop()` is permanent.
- **Why others are wrong:**
  - A) `pop()` runs while the condition is evaluated, so `"b"` is already gone.
  - B) The list printed at the end is the same list that was modified by `pop()`.
  - C) `"b" == "z"` is false, so the assertion fails and its message is printed.

**Source:** `assertions.md`
</details>

---

### 48. What does this code print?
```python
values = [5 > 3, [], "hello", 0.1 + 0.2 == 0.3, None is None]
for v in values:
    try:
        assert v
        print("ok")
    except AssertionError:
        print("fail")
```
- [ ] A) `ok`, `ok`, `ok`, `fail`, `ok`
- [ ] B) `ok`, `fail`, `ok`, `ok`, `ok`
- [ ] C) `ok`, `fail`, `ok`, `fail`, `ok`
- [ ] D) `ok`, `fail`, `fail`, `fail`, `ok`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `ok`, `fail`, `ok`, `fail`, `ok`

**Explanation:** `assert` passes for any truthy value: `True` and the non-empty string pass, while the empty list is falsy. `0.1 + 0.2 == 0.3` is `False` because of floating-point inexactness, and `None is None` is `True`.
- **Why others are wrong:**
  - A) An empty list is falsy, so the second assertion fails.
  - B) `0.1 + 0.2 == 0.3` evaluates to `False` because floating-point arithmetic is slightly inexact.
  - D) A non-empty string such as `"hello"` is truthy, so its assertion passes.

**Source:** `assertions.md`
</details>

---

### 49. What does this code print?
```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as folder:
    p = Path(folder) / "s.txt"
    p.write_text("id,name\n1,Ada\n", encoding="utf-8")

    with open(p, encoding="utf-8") as f:
        first = f.readline()
        f.seek(0)
        again = f.readline()
        rest = f.read()
    print(first == again, repr(rest))

    with open(p, "a", encoding="utf-8") as f:
        f.write("2,Grace\n")
    print(p.read_text(encoding="utf-8").count("\n"))
    print(p.stem, p.suffix)
```
- [ ] A) `True '1,Ada\n'`, `3`, `s .txt`
- [ ] B) `False '1,Ada\n'`, `3`, `s .txt`
- [ ] C) `True '1,Ada\n'`, `2`, `s .txt`
- [ ] D) `True '1,Ada\n'`, `3`, `.txt s`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `True '1,Ada\n'`, `3`, `s .txt`

**Explanation:** `seek(0)` rewinds the position, so the second `readline()` returns the header again, and `read()` then returns what remains. Append mode keeps the two existing lines and adds one, giving three newlines; `stem` is the name without the extension and `suffix` is the extension.
- **Why others are wrong:**
  - B) After `seek(0)` the next `readline()` returns the first line again, so the comparison is `True`.
  - C) Append mode keeps the existing content and adds a line, so there are three newlines, not two.
  - D) `stem` (`s`) is printed first and `suffix` (`.txt`) second; the order is reversed here.

**Source:** `reading-and-writing-files.md`
</details>

---

### 50. What does this code print?
```python
import csv, io

data = io.StringIO('id,note\n1,"Loves maths, logic"\n2,plain\n')
rows = list(csv.DictReader(data))
print(len(rows))
print(rows[0]["note"])
print(type(rows[0]["id"]).__name__)
print(len('1,"Loves maths, logic"'.split(",")))
```
- [ ] A) `2`, `Loves maths`, `str`, `3`
- [ ] B) `2`, `Loves maths, logic`, `int`, `3`
- [ ] C) `2`, `Loves maths, logic`, `str`, `2`
- [ ] D) `2`, `Loves maths, logic`, `str`, `3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `2`, `Loves maths, logic`, `str`, `3`

**Explanation:** The `csv` module honours the quotes, so the comma stays inside the note, and every value is a string, even `1`. A plain `split(",")` ignores quoting and cuts the line into three pieces, which is why the lesson says to use the module.
- **Why others are wrong:**
  - A) `DictReader` understands the quoted value and keeps the whole note.
  - B) The `csv` module never converts types; the id is the string `'1'`.
  - C) The comma inside the quotes also splits, giving three pieces: `1`, `"Loves maths` and ` logic"`.

**Source:** `csv-json-and-xml.md`
</details>

---

### 51. What does this code print?
```python
import json

data = {1: "a", "t": (1, 2), "ok": True, "n": None}
text = json.dumps(data)
print(text)
print(json.loads(text)["1"])
```
- [ ] A) `{1: 'a', 't': (1, 2), 'ok': True, 'n': None}`, `a`
- [ ] B) `{"1": "a", "t": [1, 2], "ok": true, "n": null}`, `a`
- [ ] C) `{"1": "a", "t": [1, 2], "ok": true, "n": null}`, then a `KeyError`
- [ ] D) `{"1": "a", "t": (1, 2), "ok": True, "n": None}`, `a`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `{"1": "a", "t": [1, 2], "ok": true, "n": null}`, `a`

**Explanation:** `dumps` converts the integer key to the string `"1"`, the tuple to a list, `True` to `true` and `None` to `null`. Because the key is now text, `loads(text)["1"]` finds `"a"`.
- **Why others are wrong:**
  - A) That is the Python `repr`; `dumps` produces JSON with double quotes, lists, `true` and `null`.
  - C) The key was converted to `"1"`, so looking it up with `"1"` works.
  - D) JSON has no tuples, `True` or `None`; they become a list, `true` and `null`.

**Source:** `csv-json-and-xml.md`
</details>

---

### 52. What does this code print?
```python
class Quiet:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        print("exit", exc_type.__name__ if exc_type else None)
        return exc_type is KeyError

with Quiet():
    print("one")
    {}["x"]
    print("two")
print("after")

try:
    with Quiet():
        int("z")
except ValueError:
    print("escaped")
```
- [ ] A) `one`, `two`, `exit None`, `after`, `exit ValueError`, `escaped`
- [ ] B) `one`, `exit KeyError`, `after`, `exit ValueError`, then an uncaught `ValueError`
- [ ] C) `one`, `exit KeyError`, `after`, `exit ValueError`, `escaped`
- [ ] D) `one`, `exit KeyError`, then a `KeyError` crashes the program

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `one`, `exit KeyError`, `after`, `exit ValueError`, `escaped`

**Explanation:** The `KeyError` abandons the first block before `two`, and `__exit__` returns `True` for it, so execution continues at `after`. For the `ValueError`, `__exit__` returns `False`, so the exception continues to the outer `except` after the cleanup message.
- **Why others are wrong:**
  - A) The `KeyError` is raised before `two` is printed, so the block never finishes normally.
  - B) The outer `try` catches the propagated `ValueError`, which is why `escaped` prints.
  - D) `__exit__` returned `True` for the `KeyError`, which suppresses it.

**Source:** `context-managers.md`
</details>

## Part 4: Fill-in-the-Blank

### 53. In a `try` statement, the `_____` clause runs only if the `try` block finished without raising any exception, and it must come after all `except` blocks.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `else`

**Explanation:** `else` means "only if nothing went wrong". `finally`, by contrast, always runs and is placed last.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 54. Starting Python with the `_____` flag (for example `python _____ script.py`) removes all `assert` statements, which is why asserts must never be used to validate external data.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-O`

**Explanation:** The optimised-mode flag `-O` sets `__debug__` to `False` and skips every `assert`. That is deliberate: assertions are developer aids, not input validation.

**Source:** `assertions.md`
</details>

---

### 55. To create a new output file but make Python refuse to overwrite an existing one (raising `FileExistsError`), open it with mode `"_____"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `x` (exclusive create)

**Explanation:** Mode `"x"` creates the file if it is missing and raises `FileExistsError` if it already exists, protecting earlier test evidence from accidental overwrite.

**Source:** `reading-and-writing-files.md`
</details>

---

### 56. To translate a low-level error into your own exception while keeping the original as its cause, write `raise AppError("Invalid quantity") _____ original`. The new exception class itself should inherit from `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `from`, and `Exception`

**Explanation:** `raise NewError(...) from original` explicitly chains the exceptions: the original is stored in `__cause__` and both tracebacks are shown. Custom exceptions inherit from `Exception`, never `BaseException`.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 57. The exception class that is the common parent of both `KeyError` and `IndexError` is `_____`, so `except _____` catches either one.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `LookupError`

**Explanation:** In the exception hierarchy, `LookupError` sits above `IndexError` and `KeyError`, and an `except` for a parent also catches all of its children.

**Source:** `try-except-else-and-finally.md`
</details>

---

### 58. The lesson's rule of thumb for a function that cannot do its job is: fail fast and fail `_____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `loudly`

**Explanation:** Raising an exception means a problem cannot be ignored by accident; if nobody handles it, the program stops visibly instead of passing a bad value onward.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 59. The call `os.makedirs("output/reports", _____=True)` creates nested folders and does not fail if they already exist.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `exist_ok`

**Explanation:** With `exist_ok=True` an already existing folder is not an error. The `pathlib` equivalent is `mkdir(parents=True, exist_ok=True)`.

**Source:** `reading-and-writing-files.md`
</details>

---

### 60. To manage a variable number of context managers, such as opening however many files a test needs and guaranteeing each is closed, use `contextlib._____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `ExitStack`

**Explanation:** `ExitStack` lets you enter context managers dynamically with `enter_context()` and closes all of them when the stack exits.

**Source:** `context-managers.md`
</details>

## Part 5: Scenario-Based

### 61. Scenario: test-data fixture. A teammate writes this fixture to create and remove a temporary test-data file around a test:
```python
from contextlib import contextmanager

@contextmanager
def fixture(name):
    print("setup", name)
    yield name
    print("teardown", name)

try:
    with fixture("users") as f:
        print("using", f)
        raise RuntimeError("boom")
except RuntimeError as e:
    print("caught", e)
```
What is printed, and what is the risk for the test suite?
- [ ] A) `setup users`, `using users`, `teardown users`, `caught boom`; no risk
- [ ] B) `setup users`, `using users`, `caught boom`; teardown is skipped when the test fails, so temporary data is left behind and can corrupt later tests
- [ ] C) `setup users`, `using users`, then an uncaught `RuntimeError` crashes the program
- [ ] D) `setup users`, `teardown users`, `using users`, `caught boom`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `setup users`, `using users`, `caught boom`; teardown is skipped when the test fails, so temporary data is left behind and can corrupt later tests

**Explanation:** With `@contextmanager`, an exception in the block is re-raised at the `yield` line. Without `try`/`finally` around the `yield`, the code after it never runs. The fix is `try: yield name` followed by `finally: print("teardown", name)`.
- **Why others are wrong:**
  - A) Teardown only runs on failure if it is protected by `finally`.
  - C) The outer `except RuntimeError` still catches the error once it propagates out of the `with` statement.
  - D) Teardown cannot run before the block does.

**Source:** `context-managers.md`
</details>

---

### 62. Scenario: bad rows in a test-data CSV. A QA engineer loads ages from a CSV with this code (the data has a valid row, a blank age, a non-numeric age, and a short row with no age column):
```python
import csv, io

class DataError(Exception): pass
class MissingValueError(DataError): pass

def load(text):
    good = []
    for n, row in enumerate(csv.DictReader(io.StringIO(text)), start=1):
        try:
            if row["age"] is None or row["age"] == "":
                raise MissingValueError(f"row {n}: age missing")
            good.append(int(row["age"]))
        except MissingValueError as e:
            print("MISSING", e)
        except DataError as e:
            print("DATA", e)
        except ValueError as e:
            print("BADTYPE")
    return good

print(load("name,age\nAda,36\nGrace,\nAlan,abc\nLin\n"))
```
Which statement describes what happens?
- [ ] A) `MISSING` prints once, `BADTYPE` prints twice, and the result is `[36]`
- [ ] B) The `abc` row is caught by `except DataError`, so `DATA` is printed for it
- [ ] C) The short `Lin` row raises `KeyError` for `age`, which is not handled, so the run crashes
- [ ] D) `MISSING` prints twice (blank age and short row), `BADTYPE` prints once (`abc`), and the result is `[36]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `MISSING` prints twice (blank age and short row), `BADTYPE` prints once (`abc`), and the result is `[36]`

**Explanation:** `DictReader` fills a short row's missing cell with `None`, so the `Lin` row is reported like the blank-age row. `int("abc")` raises `ValueError`, which is not a `DataError`, so it reaches the `ValueError` handler. The loop reports every problem instead of crashing and keeps only the valid age.
- **Why others are wrong:**
  - A) The counts are reversed: two rows are missing an age and only one is non-numeric.
  - B) `ValueError` is a built-in exception and is not a child of the custom `DataError`, so that handler does not match it.
  - C) A short row does not raise `KeyError`; the `age` key exists with the value `None`.

**Source:** `csv-json-and-xml.md`, `raising-and-creating-custom-exceptions.md`
</details>

---

### 63. Scenario: classifying results in a test run. A QE writes this runner so that bad data and environment problems are not reported as product bugs:
```python
class TestRunError(Exception): pass
class BadInputDataError(TestRunError): pass
class EnvironmentUnavailableError(TestRunError): pass

def run_case(case):
    if case.get("server_up") is False:
        raise EnvironmentUnavailableError("server down")
    if "expected" not in case:
        raise BadInputDataError(f"{case['id']} has no expected value")
    return case["actual"] == case["expected"]

cases = [
    {"id": "TC1", "server_up": True, "expected": 5, "actual": 5},
    {"id": "TC2", "server_up": True, "actual": 5},
    {"id": "TC3", "server_up": False},
    {"id": "TC4", "server_up": True, "expected": 5, "actual": 6},
]
for c in cases:
    try:
        ok = run_case(c)
    except BadInputDataError:
        print(c["id"], "DATA")
    except TestRunError:
        print(c["id"], "ENV")
    else:
        print(c["id"], "PASS" if ok else "FAIL")
```
What is printed, and which result is a candidate for a real product defect?
- [ ] A) `TC1 PASS`, `TC2 DATA`, `TC3 ENV`, `TC4 FAIL`; only `TC4` (the check ran and the values differed) is a candidate product defect
- [ ] B) `TC1 PASS`, `TC2 DATA`, then `TC3` crashes with an uncaught `EnvironmentUnavailableError`
- [ ] C) `TC1 PASS`, `TC2 DATA`, `TC3 DATA`, `TC4 FAIL`
- [ ] D) `TC1 PASS`, `TC2 ENV`, `TC3 ENV`, `TC4 PASS`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `TC1 PASS`, `TC2 DATA`, `TC3 ENV`, `TC4 FAIL`; only `TC4` (the check ran and the values differed) is a candidate product defect

**Explanation:** `BadInputDataError` is caught by the first handler. `EnvironmentUnavailableError` is a sibling, not a child, of `BadInputDataError`, so it falls through to the parent handler `except TestRunError`. Only `TC4` ran cleanly and returned a mismatch.
- **Why others are wrong:**
  - B) `EnvironmentUnavailableError` inherits from `TestRunError`, so the second handler catches it.
  - C) The first handler matches only `BadInputDataError` and its children; a sibling class is not matched.
  - D) `TC2` raises `BadInputDataError`, which the first handler catches, and `TC4` compares `6 == 5`, which is `False`, so it prints `FAIL`.

**Source:** `raising-and-creating-custom-exceptions.md`
</details>

---

### 64. Scenario: production hardening. A service reads `settings.json`, which the operations team edits, and checks the timeout like this:
```python
timeout = settings["timeout"]
assert isinstance(timeout, int) and timeout > 0, "timeout must be a positive integer"
```
In CI everything passes, but production starts the service with `python -O service.py`, and someone sets `"timeout": "30"` (a string) in `settings.json`. What happens, and what is the right fix?
- [ ] A) An `AssertionError` is raised at startup in production too, because assertions are part of the language
- [ ] B) Python converts `"30"` to `30` automatically, so nothing goes wrong
- [ ] C) The assertion is removed by `-O`, so the string flows into the program and fails later somewhere confusing; replace the `assert` with `if ...: raise ValueError(...)`
- [ ] D) The check still works, but only the failure message is skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The assertion is removed by `-O`, so the string flows into the program and fails later somewhere confusing; replace the `assert` with `if ...: raise ValueError(...)`

**Explanation:** Settings come from outside the program, so a wrong value is expected to occur sometimes. That is validation, which must use an exception that is always active, not an assertion that `-O` strips out.
- **Why others are wrong:**
  - A) `python -O` removes every `assert` statement, so the check never runs.
  - B) Python does not convert types silently; the value stays a string and will misbehave when used as a number.
  - D) `-O` removes the entire statement, condition included, not just the message.

**Source:** `assertions.md`
</details>

---

### 65. Scenario: configuration leaking between tests. A QE writes this helper so a test can point at a staging URL temporarily. One test fails with a `RuntimeError`, and the next test in the same process reads the variable:
```python
import os
from contextlib import contextmanager

@contextmanager
def temporary_env(name, value):
    original = os.environ.get(name)
    os.environ[name] = value
    yield
    if original is None:
        del os.environ[name]
    else:
        os.environ[name] = original

try:
    with temporary_env("QA_URL", "https://staging.test"):
        raise RuntimeError("test failed")
except RuntimeError:
    pass
print(os.environ.get("QA_URL"))
```
What does the final `print` show, and what is the fix?
- [ ] A) `None`, because a `with` statement always restores everything
- [ ] B) `https://staging.test`; the restore code after `yield` is skipped when the block raises, so wrap the `yield` in `try`/`finally`
- [ ] C) A `KeyError`, because `del os.environ[name]` runs on a missing variable
- [ ] D) `https://staging.test`, and the fix is to catch `RuntimeError` inside the helper

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `https://staging.test`; the restore code after `yield` is skipped when the block raises, so wrap the `yield` in `try`/`finally`

**Explanation:** The exception is re-raised at the `yield`, so the lines after it never run and the variable stays changed, which makes later tests depend on what ran before them. A `try`/`finally` around the `yield` guarantees the restore.
- **Why others are wrong:**
  - A) `with` always calls the manager's exit logic, but in a generator manager the restore code after a bare `yield` is skipped when an exception is re-raised there.
  - C) The restore code never runs here, and the variable does exist, so no deletion happens at all.
  - D) Swallowing the failure would hide a genuine test failure; the cleanup should be guaranteed with `finally`, and the exception left to propagate.

**Source:** `context-managers.md`
</details>

---

## Answer Key

| # | Format | Answer | Lesson |
|---|--------|--------|--------|
| 1 | MCQ | B | try-except-else-and-finally |
| 2 | MCQ | D | raising-and-creating-custom-exceptions |
| 3 | MCQ | C | raising-and-creating-custom-exceptions |
| 4 | MCQ | A | assertions |
| 5 | MCQ | B | reading-and-writing-files |
| 6 | MCQ | D | csv-json-and-xml |
| 7 | MCQ | A | csv-json-and-xml |
| 8 | MCQ | C | context-managers |
| 9 | MCQ | B | csv-json-and-xml |
| 10 | MCQ | C | try-except-else-and-finally |
| 11 | MCQ | A | try-except-else-and-finally |
| 12 | MCQ | D | try-except-else-and-finally |
| 13 | MCQ | B | raising-and-creating-custom-exceptions |
| 14 | MCQ | A | raising-and-creating-custom-exceptions |
| 15 | MCQ | C | raising-and-creating-custom-exceptions |
| 16 | MCQ | D | assertions |
| 17 | MCQ | B | assertions |
| 18 | MCQ | A | assertions |
| 19 | MCQ | C | reading-and-writing-files |
| 20 | MCQ | D | reading-and-writing-files |
| 21 | MCQ | B | reading-and-writing-files |
| 22 | MCQ | A | reading-and-writing-files |
| 23 | MCQ | C | csv-json-and-xml |
| 24 | MCQ | B | csv-json-and-xml |
| 25 | MCQ | A | context-managers |
| 26 | MCQ | D | context-managers |
| 27 | MCQ | C | context-managers |
| 28 | T/F | B (False) | try-except-else-and-finally |
| 29 | T/F | B (False) | assertions |
| 30 | T/F | A (True) | reading-and-writing-files |
| 31 | T/F | B (False) | csv-json-and-xml |
| 32 | T/F | A (True) | context-managers |
| 33 | T/F | A (True) | try-except-else-and-finally |
| 34 | T/F | B (False) | raising-and-creating-custom-exceptions |
| 35 | T/F | A (True) | assertions |
| 36 | T/F | B (False) | reading-and-writing-files |
| 37 | T/F | B (False) | csv-json-and-xml |
| 38 | T/F | B (False) | context-managers |
| 39 | T/F | A (True) | context-managers |
| 40 | Code | C | try-except-else-and-finally |
| 41 | Code | A | raising-and-creating-custom-exceptions |
| 42 | Code | D | assertions |
| 43 | Code | B | reading-and-writing-files |
| 44 | Code | C | csv-json-and-xml |
| 45 | Code | B | try-except-else-and-finally |
| 46 | Code | A | raising-and-creating-custom-exceptions |
| 47 | Code | D | assertions |
| 48 | Code | C | assertions |
| 49 | Code | A | reading-and-writing-files |
| 50 | Code | D | csv-json-and-xml |
| 51 | Code | B | csv-json-and-xml |
| 52 | Code | C | context-managers |
| 53 | Fill | `else` | try-except-else-and-finally |
| 54 | Fill | `-O` | assertions |
| 55 | Fill | `x` | reading-and-writing-files |
| 56 | Fill | `from`, `Exception` | raising-and-creating-custom-exceptions |
| 57 | Fill | `LookupError` | try-except-else-and-finally |
| 58 | Fill | `loudly` | raising-and-creating-custom-exceptions |
| 59 | Fill | `exist_ok` | reading-and-writing-files |
| 60 | Fill | `ExitStack` | context-managers |
| 61 | Scenario | B | context-managers |
| 62 | Scenario | D | csv-json-and-xml, raising-and-creating-custom-exceptions |
| 63 | Scenario | A | raising-and-creating-custom-exceptions |
| 64 | Scenario | C | assertions |
| 65 | Scenario | B | context-managers |
