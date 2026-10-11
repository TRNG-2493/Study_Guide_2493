# Day 1 (Monday) Exercise: Test-Case ID Formatter

**Course:** AI enabled Test Automation Engineer (QEA v1), Week 1 "Python Programming and Git Foundations"
**Mode:** Individual code lab | **Estimated time:** 2 h 15 min core (up to about 2 h 45 min with stretch goals)

## Scenario

Your QA team keeps test cases in a shared sheet, and every case needs an ID such as `LOGIN-0042`. People type them by hand and get them wrong: `login-42`, `Login 042`, `LOGIN_0042`. Your team lead asks for a small console tool that:

1. asks for a module prefix, a test number and a title,
2. prints a clean, consistent ID (`LOGIN-0042`),
3. takes how many tests ran and how many passed, and prints the failures, the pass rate and a release decision.

You will build it step by step and save your progress with Git in **at least 3 meaningful commits**. This is the first piece of test-data tooling in your week: the same habit (small steps, clear commits) carries through every later day.

## Learning Objectives

By the end you can:

- run a `.py` script from the terminal and read a simple error (topic: *Python Environment and Development Setup*)
- store values in well-named variables and use arithmetic and comparison operators (*Variables, Data Types and Operators*)
- convert text from `input()` into numbers and round a result (*Type Conversion and Casting*)
- read input and print clean output with f-strings and `:04d` (*Input and Output Operations*)
- create a repo and commit in small steps with good messages (*Introduction to Git and Repository Setup*, *Git Add, Commit, Status and Log*)

## Prerequisites

- Python 3 and VS Code working (`python --version` or `python3 --version`)
- Git installed, and `user.name` / `user.email` set (`git config --list` shows them)
- Today's demo is your reference. You do not need anything that was not covered today: **no `if`, loops, functions or lists**.

## What is in this folder

| File | Purpose |
|---|---|
| `starter_code/test_case_id_formatter.py` | Your file to complete. Follow the TODO markers. |
| `starter_code/check_exercise.py` | Self-check. Do not edit it. Run `python check_exercise.py`. |

## Target behavior

```text
=== Test-Case ID Formatter ===
Module prefix (e.g. login): login
Test number: 42
Test title: Valid login
Tests executed: 40
Tests passed: 34
Generated ID: LOGIN-0042
Title: Valid login
Failed: 6
Pass rate: 85.0%
Release ready: False
```

Rules: prefix is trimmed and upper-cased; number is zero-padded to 4 digits; "release ready" means pass rate of **90 or more**. The wording of the output lines must match exactly because the checker looks for them.

---

## Part 0: Set up the project and repository (15 min)

1. Create a new, empty folder outside any other Git project, for example `test-case-id-formatter`.
2. Copy `test_case_id_formatter.py` and `check_exercise.py` from `starter_code/` into it.
3. Open the folder in VS Code (`code .`).
4. In the terminal inside that folder run `git init`, then `git status`.

**Checkpoint 0:** `git status` says `On branch main`, `No commits yet`, and lists both files as untracked. If it says `fatal: not a git repository`, you are in the wrong folder.

## Part 1: Ask the questions (25 min)

Complete TODO 1a to 1e in `test_case_id_formatter.py`. Use `input()` for each question, and cast numbers with `int()` (remember: `input()` always returns text). Use `.strip()` and `.upper()` on the prefix, and `.strip()` on the title.

To see your values while you work, temporarily add a line such as `print(module_prefix, test_number, test_title, total_tests, passed_tests)`. Remove it when you are happy.

**Checkpoint 1:** run `python test_case_id_formatter.py`. Type `  login ` (with spaces) and see `LOGIN` in your debug print. Type `abc` as a number: you should get a `ValueError`. That is expected today; error handling comes later in the week.

**Git, commit 1:**
```bash
git status
git add test_case_id_formatter.py check_exercise.py
git commit -m "Add prompts for module, number, title and test counts"
```

## Part 2: Build and print the ID (25 min)

Complete TODO 2a to 2c. Build `test_id` with an f-string and the `:04d` format spec (topic: *Input and Output Operations*, section on format specifiers). Print the two lines `Generated ID: ...` and `Title: ...`.

**Checkpoint 2:** with `login` and `42` you see `Generated ID: LOGIN-0042`. With `x` and `12345` you see `X-12345` (padding never cuts digits).

**Git, commit 2:**
```bash
git status
git diff
git add test_case_id_formatter.py
git commit -m "Add zero-padded test-case ID output"
```

## Part 3: Summary and release decision (35 min)

Complete TODO 3a to 3d.

- `failed_tests` is a subtraction.
- `pass_rate` is `passed_tests / total_tests * 100`, wrapped in `round(..., 1)` (topic: *Type Conversion and Casting*, rounding).
- `release_ready` is a comparison: `pass_rate >= 90`. A comparison already produces `True` or `False`.
- Print `Failed: ...`, `Pass rate: ...%` and `Release ready: ...`.

**Checkpoint 3:** 34 passed of 40 gives `Failed: 6`, `Pass rate: 85.0%`, `Release ready: False`. Change passed to 36 and predict the result before running (`90.0%`, `True`).

**Git, commit 3:**
```bash
git add test_case_id_formatter.py
git commit -m "Add failed count, pass rate and release decision"
```

## Part 4: Self-check, README and final commit (25 min)

1. Run `python check_exercise.py` (use `python3` on macOS/Linux). Read every FAIL hint, fix, and rerun until the program checks pass.
2. Create `README.md` in your project (VS Code, plain text is fine) with: what the tool does, how to run it, and one example output.
3. Commit it:
```bash
git status
git add README.md
git commit -m "Add README with usage instructions"
```
4. Run the checker once more: the Git checks must pass too.

**Checkpoint 4:** `RESULT: all 8 checks passed` and `git status` says `working tree clean`.

## Part 5: Collect your proof and submit (10 min)

Run `git log --oneline` and keep the output (see Submission).

---

## Required Git workflow

1. `git init` in a clean project folder (Part 0).
2. **At least 3 commits** while building (this README suggests 4: parts 1, 2, 3 and the README). `test_case_id_formatter.py` must change in at least 3 of them.
3. Loop for every commit: edit, `git status`, `git add <file>`, `git commit -m "..."`, `git status` again.
4. Use `git diff` before staging at least once.
5. Finish with a clean working tree and `git log --oneline` as proof.

**Commit message guidance** (topic: *Git Add, Commit, Status and Log*): short summary of about 50 characters, imperative mood ("Add", not "Added"), say what changed, one logical change per commit.

| Good | Avoid |
|---|---|
| `Add zero-padded test-case ID output` | `update` |
| `Add failed count, pass rate and release decision` | `fix`, `stuff`, `final`, `changes` |

If you add stretch goals, make each its own commit.

## Stretch goals (optional, about 30 min)

1. **Next ID:** also print `Next ID: LOGIN-0043` (number plus one, same padding).
2. **ID length:** print `ID length: 10` using `len()` (topic: *Variables, Data Types and Operators*, strings).
3. **Report row:** print a divider (`"-" * 42`) and a table row with `ID`, `Title`, and pass rate aligned using `:<12`, `:<22`, `:>8` (topic: *Input and Output Operations*, alignment).
4. **Practice Git safety:** stage a file, then unstage it with `git restore --staged <file>` and confirm with `git status`.

Each stretch goal is its own commit, for example `Add next-ID line to output`.

## Hints

- `python` vs `python3`: Windows usually `python` or `py`; macOS/Linux `python3`.
- `TypeError: can only concatenate str`: you are joining text and a number. Use an f-string or `str()`.
- `ValueError: invalid literal for int()`: you typed non-numeric text. Expected for bad input.
- Pass rate looks like `85.00000000000001` or has too many decimals: wrap it in `round(..., 1)`.
- `Release ready:` shows `True`/`False` straight from the comparison. No `if` needed.
- Checker says a line is missing: compare spelling, capitals and spaces with the target behavior above.
- `nothing added to commit`: you forgot `git add`. `Please tell me who you are`: set `user.name` and `user.email`.
- Stuck in a commit message editor: you forgot `-m`. Press `Esc`, type `:q!`, Enter, retry.
- Checker says "inside another Git repository": move your project to a clean folder and run `git init` again.

## Definition of Done

- [ ] Project folder is its own Git repository (`git init` done once)
- [ ] `test_case_id_formatter.py` runs without errors and matches the target behavior
- [ ] All TODO comments are replaced by code (and removed); no leftover debug prints
- [ ] Prefix and title are trimmed; prefix is upper-case; ID is zero-padded to 4 digits
- [ ] Pass rate is rounded to 1 decimal; release rule is 90 or more
- [ ] `README.md` exists with purpose, how to run, one example
- [ ] At least 3 commits with specific messages; `git status` says working tree clean
- [ ] `python check_exercise.py` reports all checks passed

## Submission

Submit as your trainer instructs (course channel or LMS), including:

1. The **`git log --oneline`** output, as a screenshot or pasted text (3 or more commits).
2. The full output of **`python check_exercise.py`** (screenshot or pasted).
3. Your project folder as a **.zip including the hidden `.git` folder**, or your final `test_case_id_formatter.py` if the trainer asks for the file only.

There is no remote or push yet; that comes later in the week.

## Time estimate

| Part | Minutes |
|---|---|
| 0 Setup and `git init` | 15 |
| 1 Prompts | 25 |
| 2 ID output | 25 |
| 3 Summary | 35 |
| 4 Check, README, commit | 25 |
| 5 Proof and submit | 10 |
| **Core total** | **135 (2 h 15)** |
| Stretch goals (optional) | up to 30 |

## Self-check rubric

| Area | Needs work | Good | Excellent |
|---|---|---|---|
| Program | Fails several sample runs | All 4 sample runs pass | Also tidy code with clear variable names and a few comments |
| Python skills | Cannot explain why `int()` is needed after `input()` | Can explain `input()` returns text and what `:04d` does | Can also explain `round()` vs `int()` and why `"10" > "9"` is False |
| Git history | Fewer than 3 commits or vague messages | 3+ commits, specific imperative messages | 4+ small commits, each one logical change, `git diff` used before staging |
| Workflow | Used `git add .` without checking | Ran `git status` before and after commits | Clean tree at the end and can explain the three areas |
