# Knowledge Check: Python Fundamentals & Git Intro (Week 1 – Monday)

Answer each question on your own first, then click "Click for Solution" to check your answer and read the explanation.

---

## Part 1: Multiple Choice

### Question 1

Which statement best describes the Python **interpreter**?

- [ ] A) The application where you type and edit your code, such as VS Code
- [ ] B) The program that reads your `.py` file and carries out its instructions line by line
- [ ] C) A text window where you type commands, such as PowerShell
- [ ] D) A package installer used to download third-party libraries

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Python is an interpreted language, so the interpreter (`python` / `python3`) is the program that reads and executes your code. The editor, terminal and installer are separate things.
- **Why others are wrong:**
  - A) That describes an editor/IDE, not the interpreter.
  - C) That describes a terminal (shell).
  - D) That describes `pip`, Python's package installer.
</details>

---

### Question 2

A teammate installs Python on Windows, opens PowerShell and runs `python --version`. They get: `'python' is not recognized`. What is the most likely cause and fix?

- [ ] A) Python 2 is installed; they should uninstall it
- [ ] B) VS Code has the wrong interpreter selected; they should use the Command Palette
- [ ] C) The `.py` file is saved in the wrong folder; they should use `cd`
- [ ] D) Python is not on the PATH; they should reinstall and tick "Add python.exe to PATH" (or try `py`)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** "Not recognized" means the computer cannot find `python` in the PATH folders. Reinstalling with "Add python.exe to PATH" ticked, or using the `py` launcher, fixes it.
- **Why others are wrong:**
  - A) A Python 2 install would show a `Python 2.x` version, not "not recognized".
  - B) Interpreter selection is a VS Code issue, not a terminal one.
  - C) A wrong folder gives `can't open file`, which is a different error.
</details>

---

### Question 3

Which of these is a **valid** Python variable name?

- [ ] A) `test_1`
- [ ] B) `1st_test`
- [ ] C) `test-id`
- [ ] D) `class`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Names may contain letters, digits and underscores, cannot start with a digit, cannot contain symbols such as `-`, and cannot be Python keywords.
- **Why others are wrong:**
  - B) It starts with a digit.
  - C) A hyphen is not allowed in a name (use `_`).
  - D) `class` is a Python keyword.
</details>

---

### Question 4

A script has `total_tests = 40` and `passed_tests = 40`. What does `passed_tests / total_tests` give?

- [ ] A) `1`, because both values are integers
- [ ] B) `True`, because the numbers are equal
- [ ] C) `1.0`, because `/` always returns a float
- [ ] D) `0`, because the remainder is zero

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The `/` operator always returns a `float`, even when the result is a whole number (for example `10 / 2` gives `5.0`).
- **Why others are wrong:**
  - A) `//` or `int()` would give an integer; `/` does not.
  - B) `/` is arithmetic; only comparison operators such as `==` give booleans.
  - D) The remainder is given by `%`, not `/`.
</details>

---

### Question 5

A test report stores the response time as the text `"3.5"`. Which expression correctly produces the whole number `3`?

- [ ] A) `int("3.5")`
- [ ] B) `int(float("3.5"))`
- [ ] C) `round("3.5")`
- [ ] D) `str(3.5)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `int("3.5")` fails with a `ValueError`, so you convert to `float` first (giving `3.5`) and then `int()` truncates it to `3`.
- **Why others are wrong:**
  - A) A decimal string cannot be converted directly by `int()`; it raises `ValueError`.
  - C) `round()` needs a number, not text, and would not be the right tool for a string.
  - D) `str(3.5)` produces the text `"3.5"`, not a whole number.
</details>

---

### Question 6

A QE writes this script and the user types `25` when prompted:

```python
total = input("Total tests: ")
print(total - 3)
```

What happens?

- [ ] A) A `TypeError`, because `input()` always returns a string
- [ ] B) It prints `22`
- [ ] C) It prints `"22"`
- [ ] D) A `SyntaxError`, because `input()` cannot be used in arithmetic

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `input()` always returns text, even if the user types digits. Subtracting a number from a string raises a `TypeError`; you need `int(input(...))`.
- **Why others are wrong:**
  - B) Python does not automatically convert text to numbers.
  - C) No output is produced because the program crashes first.
  - D) The syntax is valid; the problem appears at run time as a `TypeError`.
</details>

---

### Question 7

In Git's three-area model, what does `git add hello.py` do?

- [ ] A) Permanently saves a snapshot of `hello.py` in the history
- [ ] B) Uploads `hello.py` to GitHub
- [ ] C) Moves the changes from the working directory to the staging area
- [ ] D) Deletes `hello.py` from the working directory

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `git add` stages changes, meaning "include this in my next commit". It does not save anything permanently; `git commit` does that.
- **Why others are wrong:**
  - A) That is what `git commit` does.
  - B) `git add` works locally; it never contacts GitHub.
  - D) `git add` never deletes your file.
</details>

---

### Question 8

You run `git init` inside a new folder called `qa-practice`. What does Git create?

- [ ] A) A file called `README.md` describing the project
- [ ] B) A copy of the project on GitHub
- [ ] C) A first commit named "Initial commit"
- [ ] D) A hidden `.git` folder that stores the repository's history and settings

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `git init` creates the hidden `.git` folder, which *is* the repository. The folder starts with "No commits yet".
- **Why others are wrong:**
  - A) A README must be created by you; Git does not create it.
  - B) GitHub is a separate online service; `git init` is local only.
  - C) No commit exists until you run `git commit`.
</details>

---

### Question 9

Which commit message best follows the course guidelines?

- [ ] A) `fixed stuff`
- [ ] B) `Fix zero-padding for single-digit test numbers`
- [ ] C) `final version!!`
- [ ] D) `update`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Good messages use a short summary in the imperative mood ("Fix...", "Add...") and say specifically what changed.
- **Why others are wrong:**
  - A) Vague and not in imperative mood.
  - C) Says nothing about what changed.
  - D) Too vague; the guidelines say to avoid "update".
</details>

---

### Question 10

You edit `hello.py`, which is already tracked, but have not run `git add`. Under which heading does `git status` list it?

- [ ] A) `Changes to be committed`
- [ ] B) `Untracked files`
- [ ] C) `Changes not staged for commit`
- [ ] D) `nothing to commit, working tree clean`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** A tracked file that changed but is not staged is *modified*, which `git status` shows under "Changes not staged for commit".
- **Why others are wrong:**
  - A) That heading is for staged changes.
  - B) The file is already tracked, so it is not untracked.
  - D) The tree is clean only when everything matches the last commit.
</details>

---

### Question 11

A QE writes a small check that they want to save, re-run tomorrow and share with a teammate. What is the best way to do this?

- [ ] A) Type the code into the REPL each time it is needed
- [ ] B) Keep the REPL window open and rely on it to remember the code
- [ ] C) Save the code in a `.py` script file and run it with `python filename.py`
- [ ] D) Type the code in the terminal and copy the printed output to a notes file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The REPL is for quick experiments; anything you want to keep, repeat or share belongs in a script file saved with the `.py` extension.
- **Why others are wrong:**
  - A) Retyping works against repeatability; the REPL is not meant for code you want to keep.
  - B) The lesson says the REPL is for experiments, not for anything you want to keep or share.
  - D) Copying the output saves the results, not the code that produced them.
</details>

---

### Question 12

On macOS, a new team member opens Terminal, types `python --version` and sees `python: command not found`. What should they try first?

- [ ] A) Run `python3 --version`, because on macOS and Linux the command is usually `python3`
- [ ] B) Reinstall Python and tick "Add python.exe to PATH"
- [ ] C) Use the Command Palette to run *Python: Select Interpreter*
- [ ] D) Install Python 2, because it provides the `python` command

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The troubleshooting table says `python: command not found` on macOS/Linux usually means the command is named `python3`, so use that instead.
- **Why others are wrong:**
  - B) The "Add python.exe to PATH" option belongs to the Windows installer.
  - C) Selecting an interpreter is a VS Code fix and does not change what the terminal can find.
  - D) Python 2 is retired (end of life in 2020); this course uses Python 3.
</details>

---

### Question 13

Python stops your script and prints an error message. Which approach to reading it does the course recommend?

- [ ] A) Ignore the message and re-run the script until it passes
- [ ] B) Read only the first line, because it holds the full explanation
- [ ] C) Search for the file name and ignore the rest of the message
- [ ] D) Read from the bottom: the last line gives the type of error and what went wrong, and the lines above give the file name and line number

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Python errors are helpful when read from the bottom up. The final line names the error type and the problem, while the lines above show where it happened.
- **Why others are wrong:**
  - A) Re-running without reading the message does not fix the cause.
  - B) The explanation of the problem is on the last line, not the first.
  - C) The file name only tells you where; the error type and message tell you why.
</details>

---

### Question 14

Which statement about the names `Status`, `status` and `STATUS` is correct?

- [ ] A) They refer to the same variable because they use the same letters
- [ ] B) They are three different variables, because variable names are case-sensitive
- [ ] C) Python raises a `SyntaxError` as soon as two of them exist in one script
- [ ] D) Only `status` is allowed, because Python forces snake_case

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Python treats uppercase and lowercase letters as different, so these are three separate names. `snake_case` is a convention, not a rule.
- **Why others are wrong:**
  - A) Case matters, so the letters being the same is not enough.
  - C) All three are valid names; no error occurs.
  - D) Naming conventions are not enforced by Python, only the naming rules are.
</details>

---

### Question 15

A test should pass only when the status code is 200 **and** the response time is under 2.0 seconds. Which expression does this?

- [ ] A) `status_code = 200 and response_time < 2.0`
- [ ] B) `status_code == 200 or response_time < 2.0`
- [ ] C) `status_code == 200 and response_time > 2.0`
- [ ] D) `status_code == 200 and response_time < 2.0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `==` compares the status code, `<` checks the time, and `and` requires both conditions to be true.
- **Why others are wrong:**
  - A) A single `=` assigns a value instead of comparing, so it does not test the status code.
  - B) `or` passes the test if only one condition is true.
  - C) `> 2.0` would require the response to be slow, which is the opposite of the goal.
</details>

---

### Question 16

A script contains the line `MAX_RETRIES = 3`. What does the UPPER_CASE name tell other developers?

- [ ] A) It is a constant by convention: the value should not be modified, although Python will not stop you
- [ ] B) Python will raise an error if the value is changed later
- [ ] C) Python requires UPPER_CASE names for every integer variable
- [ ] D) The value is automatically converted to a `float`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** UPPER_CASE is a convention for values that should never change. The capital letters are a message to other developers, not something Python enforces.
- **Why others are wrong:**
  - B) Python does not stop you from changing it.
  - C) Naming style has no effect on types, and integers can use any valid name.
  - D) The value stays an `int`; capitals do not change its type.
</details>

---

### Question 17

A QE reads the text `"false"` from a settings file and needs a real boolean that is `False` for `"false"` and `True` for `"true"`. Which line is correct?

- [ ] A) `is_enabled = bool(text)`
- [ ] B) `is_enabled = str(text)`
- [ ] C) `is_enabled = text.lower() == "true"`
- [ ] D) `is_enabled = int(text)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Comparing the lower-cased text with `"true"` produces a real boolean and ignores capitalisation. `bool()` only checks whether text is empty, not what it says.
- **Why others are wrong:**
  - A) `bool("false")` is `True` because any non-empty string is truthy.
  - B) `str()` returns text again, not a boolean.
  - D) `int("false")` raises a `ValueError`.
</details>

---

### Question 18

A response time is stored as the text `"1.85"`. Which line correctly checks that it is under 2.0 seconds?

- [ ] A) `"1.85" < 2.0`
- [ ] B) `float("1.85") < 2.0`
- [ ] C) `int("1.85") < 2.0`
- [ ] D) `"1.85" < str(2.0)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `float()` turns the text into the number `1.85`, so the comparison is between two numbers. Comparisons should be done with numbers, not text.
- **Why others are wrong:**
  - A) Text and numbers cannot be compared with `<`; this raises a `TypeError`.
  - C) `int("1.85")` raises a `ValueError` because a decimal string cannot be converted directly.
  - D) This compares text character by character, which is the trap the lesson warns about.
</details>

---

### Question 19

Which of these expressions raises a `ValueError`?

- [ ] A) `str(None)`
- [ ] B) `bool("")`
- [ ] C) `float("10")`
- [ ] D) `int("")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** An empty string has no content that can be read as a whole number, so `int("")` raises a `ValueError`.
- **Why others are wrong:**
  - A) `str()` works on nearly anything; `str(None)` gives `"None"`.
  - B) `bool("")` safely gives `False` because an empty string is falsy.
  - C) `float("10")` is valid and gives `10.0`.
</details>

---

### Question 20

Which statement prints exactly `2025/10/07`?

- [ ] A) `print("2025", "10", "07", sep="/")`
- [ ] B) `print("2025", "10", "07", end="/")`
- [ ] C) `print("2025", "10", "07")`
- [ ] D) `print("2025" + "10" + "07")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `sep` sets the text placed between the values, so `sep="/"` joins them as `2025/10/07`.
- **Why others are wrong:**
  - B) `end` changes what comes after the last value, so the values would still be separated by spaces.
  - C) The default separator is a space, giving `2025 10 07`.
  - D) Joining with `+` gives `20251007` with no separator at all.
</details>

---

### Question 21

Given `name = "Login Test"`, what does `print("Hello {name}")` display?

- [ ] A) `Hello Login Test`
- [ ] B) A `NameError`
- [ ] C) `Hello {name}`
- [ ] D) `Hello name`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Without the `f` before the opening quote this is an ordinary string, so the braces are printed literally. It needs `f"Hello {name}"`.
- **Why others are wrong:**
  - A) That output needs the `f` prefix.
  - B) The braces are plain text, so Python never looks up `name` and no error occurs.
  - D) The curly braces are kept in the output.
</details>

---

### Question 22

Why does the lesson write a Windows path as `"C:\\tests\\reports"` in a normal string?

- [ ] A) Python cannot type a single backslash on a keyboard
- [ ] B) A single `\t` would be read as a tab, while `\\` produces one literal backslash
- [ ] C) Doubling the backslashes makes Python convert them to forward slashes
- [ ] D) Doubling is required so the path is stored as a raw string

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Backslash starts an escape sequence, so `\t` in `C:\tests` would become a tab. Doubling gives a literal backslash; a raw string such as `r"C:\tests\reports"` is another solution.
- **Why others are wrong:**
  - A) A backslash can be typed; the issue is how Python interprets it inside strings.
  - C) Python does not change the slashes; they are printed as backslashes.
  - D) A raw string uses the `r` prefix instead; doubling is the alternative to it.
</details>

---

### Question 23

A user types `  smoke  ` (with spaces) at this prompt. What value is stored?

```python
suite = input("Suite name: ").strip().upper()
```

- [ ] A) `"SMOKE"`
- [ ] B) `"  SMOKE  "`
- [ ] C) `"smoke"`
- [ ] D) A `ValueError` is raised

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Methods are chained left to right: `.strip()` removes the surrounding spaces first, then `.upper()` capitalises the result, giving `"SMOKE"`.
- **Why others are wrong:**
  - B) `.strip()` removes the spaces.
  - C) `.upper()` converts the text to capitals, not lower case.
  - D) No number conversion happens here, so there is no `ValueError`.
</details>

---

### Question 24

A teammate is on a flight with no internet. Can they still run `git commit` on their laptop?

- [ ] A) No, Git needs a live GitHub connection to record a commit
- [ ] B) Yes, but only after creating a GitHub account
- [ ] C) No, the history is stored only on the server
- [ ] D) Yes, because Git is distributed and every computer holds a complete copy of the history

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Git is a tool installed on your computer, and each developer has the full project history, so you can work and commit offline. GitHub is only an online hosting service.
- **Why others are wrong:**
  - A) Committing is a local action and does not contact GitHub.
  - B) No account is needed to use Git on your own machine.
  - C) The full history lives on every computer, not only on a server.
</details>

---

### Question 25

A commit fails with the message "Please tell me who you are". What is the fix?

- [ ] A) Run `git init` again in the same folder
- [ ] B) Run `git add .` to stage all files
- [ ] C) Set your identity with `git config --global user.name` and `git config --global user.email`
- [ ] D) Reinstall Python

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Every commit records who made it, so Git needs `user.name` and `user.email` configured. This is a one-time setup per computer.
- **Why others are wrong:**
  - A) The repository already exists; the problem is missing identity settings.
  - B) Staging files does not tell Git who you are.
  - D) Python is unrelated to Git's identity settings.
</details>

---

### Question 26

Which term is another name for Git's **staging area**?

- [ ] A) The repository
- [ ] B) The index
- [ ] C) The working directory
- [ ] D) The remote

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** The staging area, where you collect changes for the next commit, is also called the index.
- **Why others are wrong:**
  - A) The repository is the permanent history of commits.
  - C) The working directory is the project folder where you edit files.
  - D) A remote is an online service such as GitHub and is not one of the three local areas.
</details>

---

### Question 27

You ran `git commit` without `-m` and are stuck in the Vim editor. How do you quit without saving?

- [ ] A) Press `Ctrl + Z` and then Enter
- [ ] B) Type `exit()` and press Enter
- [ ] C) Type `git quit` and press Enter
- [ ] D) Press `Esc`, type `:q!` and press Enter

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** In Vim, press `Esc`, then type `:q!` and Enter to leave without saving, then retry with `-m`. Setting `core.editor` to VS Code avoids this situation.
- **Why others are wrong:**
  - A) `Ctrl + Z` was mentioned for leaving the Python REPL on Windows, not Vim.
  - B) `exit()` is a Python REPL command.
  - C) There is no `git quit` command.
</details>

---

### Question 28

A team wants a compact history with one line per commit showing the short hash and the message. Which command should they run?

- [ ] A) `git log -p`
- [ ] B) `git log --stat`
- [ ] C) `git log --oneline`
- [ ] D) `git log -3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `git log --oneline` prints one compact line per commit, which is easy to scan and the option the lesson says you will use most.
- **Why others are wrong:**
  - A) `-p` shows the full diff for each commit, which is long.
  - B) `--stat` lists changed files and line counts for each commit.
  - D) `-3` limits the history to the last three commits but keeps the full format.
</details>

---

## Part 2: True/False

### Question 29

**True or False:** In Python, spaces at the start of a line do not matter, because Python uses `{ }` curly braces to group code.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Python uses indentation instead of curly braces, so leading spaces matter. A stray indent causes `IndentationError: unexpected indent`.
</details>

---

### Question 30

**True or False:** `bool("0")` evaluates to `True`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Truthiness only checks whether a string is empty, not what it says. `"0"` is a non-empty string, so it is `True` (the same trap applies to `bool("False")`).
</details>

---

### Question 31

**True or False:** You need a GitHub account and an internet connection to run `git init` and make commits on your own computer.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Git is a tool installed on your computer and works offline. GitHub is a separate online service for hosting repositories, and you can use Git without it.
</details>

---

### Question 32

**True or False:** Running `git restore --staged notes.txt` removes `notes.txt` from the staging area without deleting the file or its content.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `--staged` only affects the staging area. The file goes back to untracked (or modified) and its content is untouched.
</details>

---

### Question 33

**True or False:** If you forget to tick "Add python.exe to PATH" during installation on Windows, Python has not been installed at all.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Python is installed, but its folder is not in the PATH, so the computer says `'python' is not recognized`. Reinstalling with the box ticked (or using `py`) fixes it.
</details>

---

### Question 34

**True or False:** The REPL is best for quick experiments, while anything you want to keep, repeat or share should be saved in a `.py` script file.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The REPL reads, evaluates and prints one line at a time, which is perfect for trying things out. A script file keeps your code so you can rerun and share it.
</details>

---

### Question 35

**True or False:** Calling `name.upper()` on its own line changes the value stored in `name`, because strings can be modified in place.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Strings are immutable. `.upper()` returns a new string, so unless you store it (`name = name.upper()`) the result is thrown away and `name` is unchanged.
</details>

---

### Question 36

**True or False:** `int(9.99)` gives `10` because `int()` rounds to the nearest whole number.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `int()` truncates (cuts off) the decimal part, so `int(9.99)` is `9`. Use `round(9.99)` to get `10`.
</details>

---

### Question 37

**True or False:** Writing `int(age)` on its own line, where `age = "30"`, leaves `age` as text, because casting returns a new value rather than changing the original.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Casting gives back a new value and does not alter the variable. You must store it with `age = int(age)` to make `age` a number.
</details>

---

### Question 38

**True or False:** If a user types `30` at an `input()` prompt, the value returned is the integer `30`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `input()` always returns a string, even when the user types digits. Wrap it as `int(input(...))` when you need a number.
</details>

---

### Question 39

**True or False:** `print("Suite:", suite, "| Tests:", count)` needs `str(count)` first, because `print()` cannot display a number next to text.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** When you separate values with commas, `print()` converts each one to text and puts a space between them, so `str()` is not needed. `str()` is only required when joining with `+`.
</details>

---

### Question 40

**True or False:** `git diff` (with no options) shows the changes that are already staged for the next commit.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Plain `git diff` shows changes that are not yet staged. Use `git diff --staged` to see what will go into the next commit.
</details>

---

### Question 41

**True or False:** A Git commit stores a snapshot of the project together with its author, date, message and a reference to the commit before it.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Each commit points back to its parent, which is how commits form a chain of history. Each one is identified by a unique hash.
</details>

---

### Question 42

**True or False:** `git add .` stages everything that changed in the current folder, including files you may not have meant to commit, so you should check `git status` before committing.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The dot means "the current folder and everything inside it". It is convenient but can stage temporary files, large data or secrets, so run `git status` first or name files explicitly.
</details>

---

## Part 3: Code Prediction

### Question 43

What is the output of this code?

```python
total_tests = 8
passed_tests = 7
pass_rate = passed_tests / total_tests * 100
release_ready = pass_rate >= 90
print(pass_rate)
print(release_ready)
```

- [ ] A) `87.5` and `False`
- [ ] B) `87` and `False`
- [ ] C) `87.5` and `True`
- [ ] D) `0.875` and `False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `7 / 8` is `0.875`, times 100 gives `87.5`. Since `87.5 >= 90` is false, `release_ready` is `False`.
- **Why others are wrong:**
  - B) `/` returns a float, so the value is `87.5`, not `87`.
  - C) `87.5` is below 90, so the comparison is `False`.
  - D) The code multiplies by 100 before printing.
</details>

---

### Question 44

What is the output of this code?

```python
retries = 17
print(retries // 5)
print(retries % 5)
retries += 3
print(retries * 2 ** 2)
```

- [ ] A) `3`, `2`, `1600`
- [ ] B) `3.4`, `2`, `80`
- [ ] C) `3`, `2`, `80`
- [ ] D) `3`, `3`, `80`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `17 // 5` is `3` and `17 % 5` is `2`. After `+= 3`, `retries` is `20`; the exponent runs first (`2 ** 2 = 4`), so `20 * 4 = 80`.
- **Why others are wrong:**
  - A) `1600` comes from `(20 * 2) ** 2`; precedence does the exponent first.
  - B) `//` drops the decimal part, so it gives `3`, not `3.4`.
  - D) The remainder of `17 % 5` is `2`, not `3`.
</details>

---

### Question 45

What is the output of this code?

```python
a = "10"
b = "9"
print(a > b)
print(int(a) > int(b))
print(a + b)
```

- [ ] A) `True`, `True`, `19`
- [ ] B) `False`, `True`, `109`
- [ ] C) `False`, `False`, `109`
- [ ] D) `True`, `False`, `19`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Text is compared character by character, and `"1"` comes before `"9"`, so `"10" > "9"` is `False`. As numbers, `10 > 9` is `True`, and `+` on strings joins them into `"109"`.
- **Why others are wrong:**
  - A) Strings are not compared numerically, and `+` joins text rather than adding.
  - C) `int("10") > int("9")` is `True`.
  - D) Both the text comparison and the `+` result are wrong here.
</details>

---

### Question 46

What is the output of this code?

```python
print(int(9.99))
print(round(9.99))
print(int(-3.7))
print(round(88.456, 1))
```

- [ ] A) `10`, `10`, `-4`, `88.5`
- [ ] B) `9`, `10`, `-3`, `88.4`
- [ ] C) `9`, `9`, `-3`, `88.5`
- [ ] D) `9`, `10`, `-3`, `88.5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `int()` truncates towards zero (`9`, and `-3` for `-3.7`), while `round()` gives the nearest value (`10`, and `88.5` to one decimal place).
- **Why others are wrong:**
  - A) `int()` does not round; it cuts off decimals, and `-3.7` goes towards zero.
  - B) `88.456` rounded to one decimal is `88.5`, not `88.4`.
  - C) `round(9.99)` is `10`, not `9`.
</details>

---

### Question 47

What is the output of this code?

```python
print("TC", "007", sep="-")
print("Loading", end="...")
print("done")
print(f"{7:03d}")
```

- [ ] A) Three lines: `TC-007`, `Loading...done`, `007`
- [ ] B) Four lines: `TC-007`, `Loading...`, `done`, `007`
- [ ] C) Three lines: `TC 007`, `Loading...done`, `7`
- [ ] D) Three lines: `TC-007`, `Loading done`, `007`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `sep="-"` joins the values with a hyphen. `end="..."` replaces the newline, so `Loading` and `done` share one line. `:03d` pads `7` to `007`.
- **Why others are wrong:**
  - B) `end="..."` removes the line break after `Loading`.
  - C) The separator is `-`, and `:03d` zero-pads the number.
  - D) The end text is `...`, not a space.
</details>

---

### Question 48

What is the output of this code?

```python
passed = 22
total = 25
print(f"Pass rate: {passed / total:.1%}")
print(f"Failed: {total - passed}")
print(f"{'Login':<8}|{'PASS':>6}|")
```

- [ ] A) `Pass rate: 88.0%`, `Failed: 3`, `Login   |  PASS|`
- [ ] B) `Pass rate: 0.88%`, `Failed: 3`, `Login   |  PASS|`
- [ ] C) `Pass rate: 88.0%`, `Failed: 3`, `   Login|PASS  |`
- [ ] D) `Pass rate: 88%`, `Failed: {total - passed}`, `Login   |  PASS|`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `:.1%` multiplies by 100 and adds `%` (giving `88.0%`). Expressions work inside f-string braces (`25 - 22 = 3`). `:<8` left-aligns and `:>6` right-aligns.
- **Why others are wrong:**
  - B) `:.1%` already multiplies by 100.
  - C) The alignment is reversed: `<` is left, `>` is right.
  - D) The `f` prefix makes Python evaluate the braces, and `.1%` shows one decimal.
</details>

---

### Question 49

What is the output of this code?

```python
name = "login test"
name.upper()
print(name)
name = name.upper()
print(name)
print(len(name))
```

- [ ] A) `LOGIN TEST`, `LOGIN TEST`, `10`
- [ ] B) `login test`, `LOGIN TEST`, `10`
- [ ] C) `login test`, `login test`, `10`
- [ ] D) `login test`, `LOGIN TEST`, `9`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Strings are immutable, so the first `name.upper()` result is thrown away and `name` still prints as `login test`. After `name = name.upper()` it holds `LOGIN TEST`, which has 10 characters including the space.
- **Why others are wrong:**
  - A) The first `print` runs before `name` is reassigned, so it still shows lower case.
  - C) The reassignment `name = name.upper()` does change the stored value.
  - D) `len` counts the space, giving 10 and not 9.
</details>

---

### Question 50

What is the output of this code?

```python
x, y = 10, 20
a = b = 0
a += 5
print(a, b)
print(x + y * 2)
print((x + y) * 2)
```

- [ ] A) `5 5`, `50`, `60`
- [ ] B) `5 0`, `60`, `50`
- [ ] C) `5 0`, `50`, `60`
- [ ] D) `5 0`, `60`, `60`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `a += 5` changes only `a` (to 5) while `b` stays 0. Multiplication happens before addition, so `10 + 20 * 2` is `50`, and the parentheses in `(10 + 20) * 2` give `60`.
- **Why others are wrong:**
  - A) `a = b = 0` sets both names to 0, but `a += 5` updates only `a`.
  - B) The two results are swapped; without parentheses, `y * 2` is calculated first.
  - D) `x + y * 2` does not add first; precedence gives `50`.
</details>

---

### Question 51

What is the output of this code?

```python
status_code = 404
response_time = 0.4
print(status_code == 200 and response_time < 1.0)
print(status_code == 200 or response_time < 1.0)
print(not (status_code == 200))
print("TC" in "TC-001", "BUG" not in "TC-001")
```

- [ ] A) `True`, `False`, `False`, `True False`
- [ ] B) `False`, `False`, `True`, `True True`
- [ ] C) `False`, `True`, `True`, `True False`
- [ ] D) `False`, `True`, `True`, `True True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `status_code == 200` is `False` and `response_time < 1.0` is `True`. So `and` gives `False`, `or` gives `True`, and `not False` gives `True`. `"TC"` is in the ID and `"BUG"` is not, so both membership checks are `True`.
- **Why others are wrong:**
  - A) The status code is 404, so the `and` expression cannot be `True`.
  - B) `or` needs only one true side, and the response time is under 1.0.
  - C) `"BUG" not in "TC-001"` is `True`, not `False`.
</details>

---

### Question 52

What is the output of this code?

```python
print(True + True)
print(5 + 2.5)
print(type(5 + 2.5))
print(int("  7  ") + 1)
```

- [ ] A) `2`, `7.5`, `<class 'float'>`, `8`
- [ ] B) `2`, `7.5`, `<class 'int'>`, `8`
- [ ] C) `2`, `7`, `<class 'int'>`, `8`
- [ ] D) `2`, `7.5`, `<class 'float'>`, then a `ValueError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Booleans act as numbers in arithmetic (`True` is 1), so `True + True` is `2`. Mixing `int` and `float` promotes the `int`, giving the float `7.5`. `int()` allows surrounding spaces, so `int("  7  ")` is `7` and the sum is `8`.
- **Why others are wrong:**
  - B) Implicit conversion promotes the result to a `float`, not an `int`.
  - C) Python does not drop the decimal part when adding an `int` and a `float`.
  - D) `int("  7  ")` is valid because surrounding spaces are allowed.
</details>

---

### Question 53

What is the output of this code?

```python
print(bool(""), bool(" "), bool("0"), bool(0.0))
print(round(2.5), round(3.5))
print(int(True), float(True), str(None))
```

- [ ] A) `False True False False`, then `2 4`, then `1 1.0 None`
- [ ] B) `False True True False`, then `2 4`, then `1 1.0 None`
- [ ] C) `False True True False`, then `3 4`, then `1 1.0 None`
- [ ] D) `False True True False`, then `2 4`, then `1 1 None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Empty text and `0.0` are falsy, while `" "` and `"0"` are non-empty strings and so truthy. `round()` uses banker's rounding for exact halves, so `2.5` gives `2` and `3.5` gives `4`. `float(True)` is `1.0` and `str(None)` is `"None"`.
- **Why others are wrong:**
  - A) `"0"` is a non-empty string, so `bool("0")` is `True`.
  - C) `round(2.5)` is `2`, because Python rounds exact halves to the nearest even number.
  - D) `float(True)` gives `1.0`, not `1`.
</details>

---

### Question 54

What is the output of this code?

```python
total_text = "40"
passed_text = "34"
total = int(total_text)
passed = int(passed_text)
pass_rate = round(passed / total * 100, 1)
print("Failed tests: " + str(total - passed))
print("Pass rate: " + str(pass_rate) + "%")
```

- [ ] A) `Failed tests: 6` and `Pass rate: 85%`
- [ ] B) `Failed tests: 6` and `Pass rate: 0.85%`
- [ ] C) A `TypeError`, because text and numbers are mixed
- [ ] D) `Failed tests: 6` and `Pass rate: 85.0%`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `40 - 34` is `6`. `34 / 40 * 100` is `85.0`, and `round(85.0, 1)` stays the float `85.0`, which `str()` turns into `"85.0"` before it is joined to the text.
- **Why others are wrong:**
  - A) `/` returns a float, so the value prints as `85.0`, not `85`.
  - B) The code multiplies by 100, so the value is `85.0`, not `0.85`.
  - C) Both numbers are converted with `str()` before joining, so no `TypeError` occurs.
</details>

---

### Question 55

What is the output of this code?

```python
age = "30"
int(age)
print(type(age))
age = int(age)
print(type(age))
print(age + 1)
```

- [ ] A) `<class 'int'>`, `<class 'int'>`, `31`
- [ ] B) `<class 'str'>`, `<class 'str'>`, a `TypeError`
- [ ] C) `<class 'str'>`, `<class 'int'>`, `31`
- [ ] D) `<class 'str'>`, `<class 'int'>`, `301`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The first `int(age)` result is not stored, so `age` is still text. After `age = int(age)` it is an `int`, and `30 + 1` is `31`.
- **Why others are wrong:**
  - A) Casting returns a new value, so the first `int(age)` does not change `age`.
  - B) The reassignment makes `age` an `int`, so the addition works.
  - D) `301` would come from joining text; by then `age` is a number, so it adds.
</details>

---

### Question 56

What is the output of this code?

```python
attempts = 3
print("A", "B", "C", sep="")
print("Section 1")
print()
print("Section 2")
print("C:\\tests\\reports")
print(f"{attempts=}")
```

- [ ] A) `A B C`, `Section 1`, `Section 2`, `C:\\tests\\reports`, `attempts=3`
- [ ] B) `ABC`, `Section 1`, a blank line, `Section 2`, `C:\tests\reports`, `attempts=3`
- [ ] C) `ABC`, `Section 1`, a blank line, `Section 2`, `C:` followed by a tab and `ests\reports`, `attempts=3`
- [ ] D) `ABC`, `Section 1`, a blank line, `Section 2`, `C:\tests\reports`, `3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `sep=""` joins the letters with nothing between them, an empty `print()` outputs a blank line, `\\` prints as a single backslash, and `{attempts=}` prints both the name and the value.
- **Why others are wrong:**
  - A) `sep=""` removes the spaces, an empty `print()` adds a blank line, and `\\` is printed as one backslash.
  - C) The path is written with `\\`, so there is no tab; a single `\t` would have caused that.
  - D) The `=` after the variable makes the output `attempts=3`, not just `3`.
</details>

---

### Question 57

What is the output of this code?

```python
rate = 87.456789
print(f"Rate: {rate:.2f}")
print(f"{1250000:,}")
print(f"TC-{7:05d}")
print(f"{{done}}")
print(f"{0.8768:.1%}")
```

- [ ] A) `Rate: 87.46`, `1,250,000`, `TC-00007`, `{done}`, `87.7%`
- [ ] B) `Rate: 87.46`, `1250000`, `TC-007`, `{done}`, `87.7%`
- [ ] C) `Rate: 87.5`, `1,250,000`, `TC-00007`, `{done}`, `87.7%`
- [ ] D) `Rate: 87.46`, `1,250,000`, `TC-00007`, `{{done}}`, `0.877%`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `:.2f` gives two decimals (`87.46`), `:,` adds thousands separators, `:05d` pads to width 5, doubled braces print literal braces, and `:.1%` multiplies by 100 and adds `%` (`87.7%`).
- **Why others are wrong:**
  - B) `:,` adds the commas, and `:05d` pads to five characters rather than three.
  - C) `:.2f` keeps two decimal places, so it is `87.46`, not `87.5`.
  - D) Doubled braces print as single braces, and `:.1%` already multiplies by 100.
</details>

---

### Question 58

What is the output of this code? (Spaces matter in the last line.)

```python
prefix = "login"
number = 42
test_id = f"{prefix.upper()}-{number:04d}"
print(test_id)
print("TC" + "-" + str(7).zfill(3))
print("=" * 10)
print(f"{'ab':^6}|")
```

- [ ] A) `LOGIN-42`, `TC-007`, `==========`, then two spaces, `ab`, two spaces and `|`
- [ ] B) `LOGIN-0042`, `TC-7`, `==========`, then two spaces, `ab`, two spaces and `|`
- [ ] C) `LOGIN-0042`, `TC-007`, `==========`, then two spaces, `ab`, two spaces and `|`
- [ ] D) `LOGIN-0042`, `TC-007`, `==========`, then `ab`, four spaces and `|`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `.upper()` works inside the braces and `:04d` pads 42 to `0042`. `.zfill(3)` pads `"7"` to `007`, `"=" * 10` repeats the character ten times, and `:^6` centres `ab` in six characters.
- **Why others are wrong:**
  - A) `:04d` pads the number to four digits, giving `0042`.
  - B) `.zfill(3)` pads the text to `007`.
  - D) `:^6` centres the text; left alignment would be `:<6`.
</details>

---

## Part 4: Fill-in-the-Blank

### Question 59

The interactive Python mode that shows the `>>>` prompt is called the ________ (Read, Evaluate, Print, Loop).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** REPL

**Explanation:** The REPL reads one line you type, evaluates it, prints the result and loops back. It is ideal for quick experiments, while `.py` script files are for code you want to keep.
</details>

---

### Question 60

To build the test ID `TC-007` from `number = 7`, complete the f-string: `f"TC-{number:________}"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `03d`

**Explanation:** `:03d` means an integer, at least 3 characters wide, padded with zeros, so `7` becomes `007`.
</details>

---

### Question 61

To make `main` the default name of the first branch, run: `git config --global ________ main`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `init.defaultBranch`

**Explanation:** The `init.defaultBranch` setting controls the first branch name for new repositories. `main` is the modern standard (older Git defaulted to `master`).
</details>

---

### Question 62

Before committing, you can see exactly what will go into the commit (the staged changes) with `git diff ________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--staged`

**Explanation:** Plain `git diff` shows only changes that are not yet staged. `git diff --staged` shows what is staged and will be in the next commit.
</details>

---
### Question 63

On Windows, if `python --version` says `'python' is not recognized`, the Python launcher command ________ `--version` often works instead.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `py`

**Explanation:** Windows also installs the Python launcher, so `py --version` works even when `python` is not on the PATH. Reinstalling with "Add python.exe to PATH" ticked is the permanent fix.
</details>

---

### Question 64

The operator that gives the remainder of a division, so that `7 ________ 2` is `1`, is the modulus operator.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `%`

**Explanation:** `%` returns what is left over after division (7 = 2 x 3 + 1). A classic use is `number % 2`, which is `0` for even numbers.
</details>

---

### Question 65

To turn the text `"3.5"` into the whole number `3`, you convert to a float first: `int(________("3.5"))`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `float`

**Explanation:** `int("3.5")` raises a `ValueError`, so `float("3.5")` gives `3.5` and then `int()` truncates it to `3`.
</details>

---

### Question 66

Because Python's `round()` uses banker's rounding for exact halves (it rounds to the nearest even number), `round(2.5)` gives ________.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `2`

**Explanation:** Exact halves round to the nearest even number, so `2.5` becomes `2` and `3.5` becomes `4`. This is intentional behaviour.
</details>

---

### Question 67

To print `TC-001` from `print("TC", "001", ...)`, add the keyword argument ________`="-"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `sep`

**Explanation:** The `sep` option sets the text placed between the printed values; by default it is a single space. `end` controls what comes after the last value.
</details>

---

### Question 68

To show a float `rate` with two decimal places inside an f-string, write `f"Rate: {rate:________}"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `.2f`

**Explanation:** `:.2f` means "float with 2 digits after the decimal point", so `87.456789` is shown as `87.46`.
</details>

---

### Question 69

Git's staging area, where changes wait for the next commit, is also known as the ________.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** index

**Explanation:** The staging area (index) sits between the working directory and the repository. `git add` moves changes into it and `git commit` saves them from it.
</details>

---

### Question 70

To save the staged changes with a message directly on the command line, run `git commit ________ "Add README"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-m`

**Explanation:** The `-m` option supplies the commit message in quotes. Without it, Git opens a text editor such as Vim.
</details>

---

### Question 71

To list the history with one compact line per commit, run `git log ________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--oneline`

**Explanation:** `git log --oneline` shows the short hash and message of each commit on a single line, with the newest at the top.
</details>

---

### Question 72

To list the files in a folder including hidden ones, such as `.git`, run `ls ________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-a`

**Explanation:** `ls -a` includes files whose names start with a dot. It is how you confirm that `git init` created the hidden `.git` folder.
</details>

---
