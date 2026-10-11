# Day 5 (Friday) Exercise: Test-Report System and Week 1 Git Summary Push

**Course:** AI enabled Test Automation Engineer (QEA v1) | **Week 1:** Python Programming and Git Foundations
**Format:** individual code lab | **Time budget:** 2 to 3 hours | **Level:** beginner

---

## 1. Scenario

Your team runs hundreds of tests every night. The raw results arrive as loose dictionaries and CSV lines: sometimes with a typo in the status (`"PSAS"`), a negative duration, or a duplicated test ID. Nobody trusts the numbers.

Your job is to build the small, trustworthy core of a **test-report system**:

- `TestResult` is one validated outcome (it refuses nonsense).
- `Suite` holds the results of one run and answers questions about them (pass rate, failures, slowest tests).
- `Reporter` turns a suite into text. Different reporters (`TextReporter`, `CsvReporter`) produce different formats from the same suite.

Then you close the week like a professional: one clean repository, a README that summarises Monday to Friday, a pull request, a tag and a push.

You saw a 40-line preview of these three class names in the demo. **Your version goes well beyond it**: stricter validation, class-level counters, two alternative constructors, static helpers and a reporter hierarchy.

## 2. Learning objectives

By the end you can:

1. Design a small set of classes on paper (and in a Mermaid diagram) before coding.
2. Write constructors and use properties with validation to protect attributes (encapsulation).
3. Use a class variable as a shared counter and a constant, and explain why it is updated through the class.
4. Choose correctly between an instance method, `@classmethod` (alternative constructors) and `@staticmethod` (helpers).
5. Build a base class and subclasses; override `render()`; rely on polymorphism.
6. Consolidate a week of work into one repo: clean commits, README, feature branch, pull request, tag, push.

## 3. Prerequisites

Everything here comes from Monday to Friday:

| Topic | Where you met it |
|---|---|
| f-strings, string methods (`strip`, `upper`, `startswith`, `isdigit`, `replace`, `splitlines`) | Mon-Tue |
| `if`/`elif`/`else`, `for`, `try`/`except` | Tue |
| lists, dicts (`.get`), `sorted(..., key=..., reverse=True)` | Wed |
| functions, default arguments, `lambda` | Thu |
| classes, `__init__`, `self`, `__str__`/`__repr__`, properties and setters, class vs instance variables, `@classmethod`, `@staticmethod`, `super()`, inheritance, `isinstance` | Fri |
| `git init/add/commit/status/log`, `.gitignore`, `clone/push/pull`, pull requests, `git switch -c`, `git merge` | Mon-Wed |

Setup: Python 3.8+, `git` configured (name and email), and your Week 1 repo(s) from this week available on your machine. A remote (the GitHub/GitLab account you used on Tuesday) must exist.

## 4. What you are given

```
starter_code/
  report_system.py     class skeletons with numbered TODOs (you edit this)
  run_report.py        small driver program with TODOs (you edit this)
  check_exercise.py    self-check, plain asserts, DO NOT EDIT
  .gitignore           ready to use
templates/
  class-diagram.mermaid      blank class diagram (fill in during Step 1)
  WEEK1_SUMMARY_TEMPLATE.md  README template for Step 6
```

Work in a **copy** of `starter_code/` (it becomes your `friday/` folder in Step 6). `check_exercise.py` has three parts; run one at a time while you build: `python3 check_exercise.py 1`, then `2`, then `3`, and finally with no number. A finished skeleton method no longer says `TODO`; `FAIL` lines tell you exactly what is wrong.

## 5. Step-by-step tasks

> Draw First, Code Second: Step 1 comes before any code.

### Step 1: Design (about 15 min)

1. On paper, draw three boxes: `TestResult`, `Suite`, `Reporter`. Ask, for each: what **data** does it hold, what **actions** does it have, and which things are **shared by the whole class** (class variables)?
2. Add `TextReporter` and `CsvReporter` under `Reporter` (hollow arrow = "is-a").
3. Decide the relationships: a `Suite` **has many** `TestResult` objects; a `Reporter` **has one** `Suite`.
4. Mark with letters: `C` class variable, `_` internal attribute, `P` property, `K` classmethod, `S` staticmethod.
5. Copy `templates/class-diagram.mermaid` to `docs/class-diagram.mermaid` and fill it in. Preview it (VS Code Mermaid preview, mermaid.live, or GitHub rendering).

**Checkpoint 1:** Your diagram shows one inheritance arrow and one "has-a" line, and every `TODO` in the template is replaced. Add one note for the thing you are least sure about.

*Do not look at the starter's TODO list for answers while drawing; it will not match your drawing exactly, and that is fine. Revisit the diagram at the end and correct it (Step 5).*

### Step 2: `TestResult` (about 40 min)

Open `report_system.py` and work through TODO 1.1 to 1.12. Run `python3 check_exercise.py 1` often.

Required behaviour:

| Item | Specification |
|---|---|
| `VALID_STATUSES` | Given: `"PASS"`, `"FAIL"`, `"SKIPPED"`, `"ERROR"` |
| `TestResult(test_id, status, duration=0.0, message="")` | Validates everything; a bad object is never created |
| `test_id` | Property, **read-only**. Must look like `TC-001` (`"TC-"` + one or more digits), else `ValueError` |
| `is_valid_id(x)` | `@staticmethod`; returns `True`/`False`, never raises (works for `None`, numbers) |
| `status` | Property with setter. Text only; `strip()` and `upper()` first (`" pass "` becomes `"PASS"`); must be in `VALID_STATUSES`, else `ValueError` that includes the bad value. A rejected assignment leaves the old value |
| `duration` | Property with setter. Number only (not text, not `True`): else `TypeError`. Negative: `ValueError`. Stored as `float` |
| `is_passed` | Read-only property |
| `total_created`, `how_many()` | Class variable counter and `@classmethod`. Count **only objects that were created successfully** |
| `from_dict(data)` | `@classmethod`; requires `test_id` and `status` (`ValueError` naming the missing key); `duration` and `message` optional. Must build with `cls(...)` |
| `from_csv_line(line)` | `@classmethod`; `"TC-010, PASS, 1.5, Slow login, but fine"`; the message may contain commas; only first two fields required |
| `__str__` | `TC-001 PASS 1.2s`, plus ` - <message>` if there is a message |
| `__repr__` | `TestResult('TC-001', 'PASS', 1.2)` using `type(self).__name__` |

**Checkpoint 2:** `python3 check_exercise.py 1` shows 10/10. **Commit now** (see Step 6 for message advice), for example: `Add TestResult with validation and alternative constructors`.

### Step 3: `Suite` (about 25 min)

TODO 2.1 to 2.8. Run `python3 check_exercise.py 2`.

| Item | Specification |
|---|---|
| `Suite(name)` | Name must be non-empty text after `strip()`, else `ValueError`. Each suite owns its own `_results` list |
| `Suite.from_rows(name, rows)` | `@classmethod`; builds a suite from a list of dictionaries |
| `add(result)` | `TypeError` if not a `TestResult`; `ValueError` if the `test_id` is already in the suite |
| `results` | Property returning a **copy** of the list |
| `count()` | Number of results |
| `pass_rate` | Read-only property, percent 0 to 100, `PASS` count divided by **all** results (skipped ones count in the total). Empty suite: `0.0` |
| `total_duration` | Property, sum of durations |
| `counts_by_status()` | Dict with **every** valid status as a key: `{"PASS": 2, "FAIL": 1, "SKIPPED": 1, "ERROR": 0}` |
| `failures()` | List of `FAIL` and `ERROR` results in suite order |
| `slowest(n=1)` | The `n` slowest results, slowest first (use `sorted` with a key) |

**Checkpoint 3:** `python3 check_exercise.py 2` shows 7/7. Commit: `Add Suite with pass rate and failure queries`.

### Step 4: Reporters and polymorphism (about 30 min)

TODO 3.1 to 3.6. Run `python3 check_exercise.py 3`.

- `Reporter(suite)`: `TypeError` unless given a `Suite`. `render()` in the base class raises `NotImplementedError` with a helpful message. `line_count()` is written **once** in the base class and calls `self.render()`.
- `pad(text, width)` and `format_percent(value)` are `@staticmethod`s. `CsvReporter.clean_cell(text)` too.

`TextReporter.render()` for the sample data in `run_report.py` must give exactly:

```
=== Login ===
TC-001  PASS       1.2s
TC-002  FAIL       3.4s
TC-003  PASS       0.8s
TC-004  SKIPPED    0.0s
Pass rate: 50.0%
```

(Each row is: id padded to 8, status padded to 9, then the duration right-aligned in 5 characters with one decimal, then `s`.)

`CsvReporter.render()` must give exactly (note the `;` in place of the comma inside the message):

```
test_id,status,duration,message
TC-001,PASS,1.2,
TC-002,FAIL,3.4,Timeout; retry failed
TC-003,PASS,0.8,
TC-004,SKIPPED,0.0,
```

Lines are joined with `"\n"` and there is no trailing newline.

**Checkpoint 4:** `python3 check_exercise.py 3` shows 7/7. Commit: `Add Reporter hierarchy with text and CSV output`.

### Step 5: Driver and final check (about 15 min)

1. Complete `run_report.py` (TODO 4.1 to 4.4). The loop over `[TextReporter(suite), CsvReporter(suite)]` calling `reporter.render()` is the polymorphism moment: **one call, different behaviour**.
2. Expected output includes three `Rejected ...` lines, both reports, and `Results created: 4`.
3. Run `python3 check_exercise.py` (no number): all checks pass.
4. Look at your Step 1 diagram again. Correct it so it matches what you really built, and commit it.

**Checkpoint 5:** `24/24 checks passed` and the driver prints both formats.

### Step 6: Week 1 Git summary push (about 30 min)

Goal: **one repository** that tells the story of your week, with a clean history, a README summary, a tag, and everything on the remote.

1. **Inspect.** In your repo run `git status`, `git branch` and `git log --oneline`. Is anything uncommitted? Does the log read like a story of the week?
2. **One repo.**
   - If you used one repo all week, use it.
   - If you used several, create (or choose) one repo and copy each day's *final* program into its own folder (for example `monday/`, `tuesday/`, ...). Use your own folder names; just be consistent and list them in the README.
3. **Branch.** `git switch -c feature/week1-summary`.
4. **Add Friday.** Put your finished work in `friday/`: `report_system.py`, `run_report.py`, `check_exercise.py`, `.gitignore` (or merge its lines into the repo's `.gitignore`), and `docs/class-diagram.mermaid`. Confirm `git status` shows **no** `__pycache__/`, no virtual environment, no editor folders. Your `.gitignore` handles it.
5. **README.** Copy `templates/WEEK1_SUMMARY_TEMPLATE.md` to `README.md` at the repo root and complete it: a table listing the Monday to Friday programs, how to run Friday's, what you learned, and an honest look at your own commit messages.
6. **Commit with meaning.** Use one logical change per commit and messages that say what and why. Good: `Add Suite pass_rate property`. Weak: `stuff`, `fix`, `final final`. You should have **at least 4 commits** on this branch (the Step 2 to 4 commits plus README). Do not rewrite old history; if an old message was vague, name it in the README and say what you would write now.
7. **Push and PR.**
   ```bash
   git push -u origin feature/week1-summary
   ```
   Open a pull request into `main` (as on Tuesday). Write a short description: what the repo contains and how to run Friday's checks. Merge it.
8. **Update main.**
   ```bash
   git switch main
   git pull
   git branch -d feature/week1-summary
   ```
9. **Tag.** This is the one new command today, given in full. An annotated tag is a permanent, named label on a commit:
   ```bash
   git tag -a week1-complete -m "Week 1 complete: Python and Git foundations"
   git push origin week1-complete
   ```
   Check it with `git tag` and `git show week1-complete`. The tag must sit on the commit of `main` that contains your README and `friday/`.
10. **Final check.** `git status` is clean; `git log --oneline --graph --all` looks tidy; the remote page shows your README, `friday/`, and the tag (look under Tags/Releases).

**Checkpoint 6:** Someone who clones your repo, reads the README and runs `python3 friday/check_exercise.py` sees `24/24 checks passed`.

## 6. Time budget

| Step | Minutes |
|---|---|
| 1 Design | 15 |
| 2 TestResult | 40 |
| 3 Suite | 25 |
| 4 Reporters | 30 |
| 5 Driver and final check | 15 |
| 6 Git summary push | 30 |
| **Total (core)** | **155 (about 2 h 35 min)** |

Stretch goals are optional and take extra time. If you are behind at 2 h 30 min, finish Step 6 first and return to unfinished TODOs afterwards.

## 7. Stretch goals (optional)

1. **`MarkdownReporter`.** A third subclass whose `render()` produces a heading, a table (`| Test | Status | Duration |`) and a bold pass-rate line. Add it to your driver loop without changing any existing class.
2. **Comparison operators.** Add `__eq__` (same `test_id`, `status`, `duration`) and `__lt__` (compare by duration) to `TestResult`. What can you do with `sorted(results)` now?
3. **Read results from text.** Add `Suite.from_csv_text(name, text)` using `splitlines()` and `TestResult.from_csv_line`. Report which lines were rejected instead of crashing.
4. **Timing decorator.** Reuse Thursday's timing decorator on `render()`. Does it work on a method? What does `self` do to your wrapper's arguments?
5. **Second hierarchy level.** `ColorTextReporter(TextReporter)` that calls `super().render()` and wraps FAIL lines with a marker such as `!!`.
6. **Git extra.** Add a second tag `week1-review` on an earlier commit with `git tag week1-review <commit-id>`, and describe the difference between a branch and a tag in two sentences in your README.

## 8. Hints

- **Properties:** the setter must be named exactly like the getter; the stored value lives in `self._status`. In `__init__` write `self.status = status` (no underscore) so the setter validates.
- **Counter:** `TestResult.total_created += 1` as the **last** line of `__init__`. In a subclass, `self.total_created += 1` would create an instance attribute instead (shadowing).
- **`is_valid_id`:** `isinstance(x, str)`, then `startswith("TC-")`, then `x[3:].isdigit()` (an empty string is not "digits": `"".isdigit()` is `False`).
- **`bool` trap:** `isinstance(True, int)` is `True`, so test `bool` first.
- **`from_csv_line`:** `line.split(",", 3)` splits at most 3 times, so the 4th piece keeps any commas. (`split(sep, maxsplit)` is the one new detail here.)
- **`pad`:** `str(text).ljust(width)` (used in the demo) or an f-string such as `f"{text:<8}"`. A width held in a variable can be written `f"{text:<{width}}"`.
- **`slowest`:** `sorted(self._results, key=lambda r: r.duration, reverse=True)[:n]`.
- **`from_dict` with `cls`:** if you hard-code `TestResult(...)`, a subclass's `from_dict` returns the wrong type. The check tests for this.
- **`line_count` in the base class:** `self.render()` finds the right `render` for each object at run time.
- **Why does `t3_base_class` still fail after I wrote `render`?** The base `render` must *raise* `NotImplementedError`, not `return` or `pass`.
- **Git:** `git status` before every commit; `git add <file>` rather than `git add .` if unsure. If `__pycache__/` was already committed, tell your instructor; do not rewrite history on your own.
- **Stuck?** Re-read the matching Friday topic, run the single check part, read the first `FAIL` message only, fix it, run again.

## 9. Definition of Done

- [ ] `docs/class-diagram.mermaid` filled in, matches the final code, and renders.
- [ ] `python3 check_exercise.py` prints `24/24 checks passed`.
- [ ] `run_report.py` prints three `Rejected` lines, both reports, and `Results created: 4`.
- [ ] `TestResult` has: validated properties, read-only `test_id`, class counter, `from_dict`, `from_csv_line`, static `is_valid_id`, `__str__`, `__repr__`.
- [ ] `Suite` returns a copy from `results`; `pass_rate` is a property.
- [ ] `Reporter` has a base `render()` that raises `NotImplementedError`; `TextReporter` and `CsvReporter` override it; `line_count()` exists only in the base class.
- [ ] One repo contains Monday to Friday programs; the README table lists all five days.
- [ ] At least 4 meaningful commits for Friday; no junk files (`__pycache__/`, virtual environments) committed.
- [ ] Work went through `feature/week1-summary` and a merged pull request; `main` is up to date locally.
- [ ] Annotated tag `week1-complete` exists locally and on the remote.
- [ ] `git status` is clean.

## 10. Submission

Submit the following through the channel your instructor names (form, LMS or chat):

1. The URL of your repository.
2. The URL of your merged pull request.
3. The name of your tag (`week1-complete`) and the output of `git log --oneline --graph --all` (paste as text).
4. The full output of `python3 friday/check_exercise.py` (paste as text or screenshot).
5. One sentence: which part of the exercise was hardest, and why.

Your instructor will clone your repo and run the check script.

## 11. Rubric (100 points)

| Area | Points | Full marks when |
|---|---|---|
| TestResult | 20 | All Part 1 checks pass; validation lives in properties; counter correct; `cls` used in alternative constructors (2 points per check) |
| Suite | 15 | All Part 2 checks pass; list is protected; no shared mutable list |
| Reporters and polymorphism | 20 | All Part 3 checks pass; subclasses override only what differs; `line_count` inherited |
| Design | 10 | Diagram has the right boxes, inheritance and has-a lines, class-level members marked, and matches the final code |
| Git wrap-up | 25 | One repo; README table complete; PR merged; at least 4 meaningful commits; clean `.gitignore` use; tag `week1-complete` on the remote; clean status (5 points each) |
| Code quality and README | 10 | Readable names, short docstrings, no copy-pasted blocks, README honest and clear |
| **Total** | **100** | Stretch goals: up to 5 bonus points |

Bands: 90+ ready for Week 2; 75 to 89 solid, review the weak area; below 75 meet your instructor for a short review.
