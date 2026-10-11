# Lab: Debug It, Log It, Test It, Merge It

**Week 2, Day 3 (Wednesday): Python Debugging & Testing Foundations** | Individual Code Lab (Mode A) | **2 h 40 min** of focused work (plan for 3 h)
**Project lane:** Project 1, QE Foundations (milestone in Part E)

## Scenario

You have joined the QE team. The nightly **test-run report** is wrong: wrong medians, a crash on the morning dashboard, report ids that will not generate. The helper module is `run_stats.py` and seven tickets are open against it. Your job, in the order a real QE works:

**Debug** (find the cause with evidence) > **Log** (make the program tell its own story) > **Test** (lock the fixes in) > **Merge** (resolve a teammates' conflict) > **Project 1** (apply logging and tests to your own ingestion module).

This is *new* code: it is not the module from the demo, so you cannot copy the demo's fixes. The same *kinds* of bugs appear, so the **method** you saw today works here.

## What you need (from Monday, Tuesday and today's reading)

| Skill | Lesson |
|---|---|
| `breakpoint()`, pdb commands, tracebacks, post-mortem | `debugging-techniques.md` |
| names that become local, `global` | `scope-and-namespaces.md` |
| mutable default arguments, in-place changes | `mutability-and-memory.md` |
| `sorted`, `sum`, `len`, `enumerate` | `built-in-python-functions.md` |
| loggers, levels, handlers, `getLogger(__name__)` | `logging.md` |
| `unittest`, `assertRaises`, `setUp`, `subTest`, `assertLogs` | `introduction-to-unit-testing.md` |
| conflict markers, resolve, `git add`, `git commit` | `git-merge-conflicts-and-resolution.md` |
| Tuesday's ingestion module (for Part E) | Tuesday exercise |

No `pip install`, no pytest, no SQL: standard library only. Python 3.9 or newer, Git 2.28 or newer.

## Time boxes

| Part | What | Time |
|---|---|---|
| Setup | copy the starter, check Python and Git | 5 min |
| **A** | Debug `run_stats.py` (7 tickets) and fill the debug log | 35 min |
| **B** | Add logging | 20 min |
| **C** | Write unit tests | 30 min |
| **D** | Resolve the staged merge conflict | 20 min |
| **E** | **Project 1 milestone**: logging + first test suite in `qe-foundations` | 40 min |
| Wrap-up | self-check, commit, submit | 10 min |

If you are stuck for more than **10 minutes** on a ticket, open the next hint (they are in a section at the end, in three levels). Using hints costs nothing in the rubric; sitting stuck does.

## Setup (5 min)

Create a working folder **outside** your `qe-foundations` repository (two Git repos must never be nested) and copy the starter into it.

PowerShell:
```powershell
mkdir week2-wed ; cd week2-wed
Copy-Item -Recurse <path-to-this-exercise>\starter_code .\starter_code
py --version ; git --version
```
bash / macOS / Linux:
```bash
mkdir week2-wed && cd week2-wed
cp -r <path-to-this-exercise>/starter_code ./starter_code
python3 --version; git --version
```
Use `py` instead of `python` on Windows if `python` opens the Microsoft Store. Commands below are written with `python`.

Starter files (all in `starter_code/`):

| File | Part | Purpose |
|---|---|---|
| `run_stats.py` | A, B | the buggy module (**you edit this**) |
| `run_report.py` | A, B | reproduces each ticket; you add the logging setup to `main()` |
| `debug_log.md` | A | the evidence log you fill in |
| `test_run_stats.py` | C | a skeleton with one worked example |
| `conflict_lab/setup_conflict.sh` and `.ps1` | D | build the conflicted repo |
| `project1_templates/` | E | a `logging_setup.py` skeleton and `.gitignore` lines |
| `check_exercise.py` | all | the self-check |
| `_baseline/run_stats_buggy.py` | C | an untouched copy of the buggy file used by the checker. **Do not edit it.** |

---

## Part A: Debug (35 min)

### The tickets

Each ticket is a bug report from a teammate. Reproduce one with `python run_report.py N`; run all with `python run_report.py`.

| Ticket | Report from the QA lead | Expected |
|---|---|---|
| **BUG-1** | "Median of four durations `[4, 1, 3, 2]` shows 3." | 2.5 |
| **BUG-2** | "I asked for the 3 slowest tests and got 2. Asking for 0 gives me almost the whole list." | 3 items; `[]` for 0 |
| **BUG-3** | "Counting outcomes per suite crashes: `KeyError`." | `{"login": {"pass": 2, "fail": 1}, "search": {"pass": 1}}` |
| **BUG-4** | "Two different reports show the same flaky list." | `["t2"]` and `["t9"]` |
| **BUG-5** | "The report id never gets created: `UnboundLocalError`." | `RUN-0001`, then `RUN-0002` |
| **BUG-6** | "The dashboard shows the wrong number for the latest test (the last timing recorded was 150 ms). Also my own timing list comes back in a different order after the report runs." | `latest_ms` is 150 and my list is unchanged |
| **BUG-7** | "On a night with no timings the report crashes." | `median_ms` is `None`; `median([])` raises a clear `ValueError` |

The **spec for every function is its docstring** in `run_stats.py`. Read it first. **Bugs hide behind each other** (a crash in BUG-5 stops you from ever seeing BUG-6), so fix in ticket order and re-run after each fix.

### Tasks

1. **Reproduce** ticket 1: `python run_report.py 1`. Write the wrong answer in `debug_log.md`.
2. **Form a hypothesis before you touch the code**, and write it down.
3. **Gather evidence** with at least **one `breakpoint()`** session (use `p`, `pp locals()`, `n`, `s`, `c`, `w`) **and** at least **one post-mortem** of a crash (`python -m pdb run_report.py 3`, then `c`, or `import pdb; pdb.pm()`). Print debugging is allowed too: you need at least one *pdb* session and one *traceback* read.
4. **Fix one defect at a time.** Re-run the ticket after each fix.
5. Fill in the debug log for each ticket (symptom, family, hypothesis, evidence, root cause, fix, how you verified).
6. **Remove every `breakpoint()`** before you finish (the checker looks).

### Part A result
`python check_exercise.py --part A` shows **all 7 BUG lines PASS**, no `breakpoint()` left, debug log filled.

---

## Part B: Add logging (20 min)

Logging has two sides: **library code creates a logger and logs**; the **entry point configures where messages go**.

1. In `run_stats.py` add a **module logger named `logger`**: `logger = logging.getLogger(__name__)`. Do not call `basicConfig` or add handlers here. No `print()` calls.
2. Add log calls at the right levels:

| Where | Level | Message should say |
|---|---|---|
| `median()`, `slowest()`, `next_run_id()` | DEBUG | the inputs' size and the result |
| `note_flaky()` | INFO | which test was flagged and how many are flagged |
| `group_by_suite()`, result has no `"suite"` | **WARNING** | which test was affected and that it went to `"unknown"` |
| `summarise_run()` | **INFO** | run id, number of results, number of suites |

   Use `%` arguments (`logger.debug("median of %d values = %s", len(v), result)`), not f-strings.
3. In `run_report.py`, in the `main()` TODO block, configure logging **once**: a console handler at **INFO**, a file handler at **DEBUG** writing `run_report.log`, a format with time, level, logger name and message, and a guard so calling the setup twice adds no duplicate handlers.
4. Run `python run_report.py`. Open `run_report.log`: you should see DEBUG lines there that the console did not show.

### Part B result
`python check_exercise.py --part B` shows **all checks PASS**. Also: open `run_report.log` and find the WARNING you cause with `group_by_suite([{"test": "x", "status": "skip"}])`.

---

## Part C: Unit tests (30 min)

Open `test_run_stats.py` (a skeleton with one worked Arrange-Act-Assert example). Complete it.

**What to write**

- At least **12 test methods**, grouped in the `TestCase` classes provided. Delete or fill every `pass` placeholder class.
- **One regression test per ticket (7)**: each must **fail on the buggy `_baseline` file and pass on your fix**. That is how you know the test earns its keep.
- At least **3 tests of bad or unusual input** whose names contain a hint word (`empty`, `zero`, `missing`, `unknown`, `none`), for example `test_empty_raises_value_error`, `test_n_zero_returns_empty_list`, `test_missing_suite_goes_to_unknown`.
- At least one `assertRaises` (the `with` form), one `assertLogs` (it proves your Part B WARNING/INFO exists), and a `setUp` that resets shared state (`run_stats.run_counter = 0`) so tests are **independent** (the "I" in FIRST).
- Use `assertAlmostEqual` for floats and `subTest` for any table of inputs.
- Name tests for behaviour: `test_even_count_averages_two_middle_values`, not `test1`.

Run: `python -m unittest -v test_run_stats` (from `starter_code`).

### Part C result
`python check_exercise.py --part C` shows **all PASS**, including "your tests FAIL against the original buggy file (7 or more)".

---

## Part D: Resolve a staged merge conflict (20 min)

Two teammates edited the same nightly settings. **Priya** (on `main`) lowered the gate and added a `checkout` suite. **Sam** (on `feature/strict-gate`) raised the gate and added a `payments` suite. Both also added a helper function to `report.py`. You are merging Sam's branch.

**Build the repo.** From your `week2-wed` folder (NOT inside another repo):

PowerShell:
```powershell
.\starter_code\conflict_lab\setup_conflict.ps1
# if scripts are blocked:  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
cd conflict-lab
```
bash:
```bash
bash starter_code/conflict_lab/setup_conflict.sh
cd conflict-lab
```
The script creates `conflict-lab`, runs `git merge feature/strict-gate`, and leaves you **in the middle of a conflicted merge**. To start over: re-run the script with `-Force` (PowerShell) or `--force` (bash).
Git needs your identity for the merge commit: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"` if you have not set them.

**The team decision (from the QA lead): follow it exactly.**
1. `PASS_THRESHOLD` is **95**.
2. `SUITES` contains **all four** suites in this order: `login`, `search`, `checkout`, `payments`.
3. `report.py` keeps **both** new functions, `summary_line` and `failing_suites`.
4. Do not lose anything from `CHANGELOG.md` (Git merged it automatically; look at it, but do not edit it).

**Tasks**
1. `git status` and `git log --oneline --graph --all`: write down which files are in conflict and which merged cleanly.
2. Open `settings.py`. It has **two** conflict regions. Resolve each by hand, deleting every `<<<<<<<`, `=======`, `>>>>>>>` line.
3. Resolve `report.py` (an add/add situation: both sides added a function in the same place).
4. Run `python report.py`. The output must be:
   ```
   Suites: login, search, checkout, payments
   Verdict for 93.0%: RED
   ```
   (93.0 is below the new 95 gate: that is the decision at work.)
5. `git add settings.py report.py`, `git status`, then `git commit` (accept or edit the merge message).
6. Write `conflict_notes.md` in `conflict-lab`'s **parent** folder (`week2-wed`), 4 to 6 sentences: why did `CHANGELOG.md` not conflict? What would have gone wrong if you had picked "accept current" in the editor for both files? How did you know the resolved code was right?
7. Save the history for your mentor: `git log --oneline --graph --all > ..\conflict_graph.txt` (PowerShell) or `... > ../conflict_graph.txt` (bash).

### Part D result
`python check_exercise.py --part D --conflict-repo ..\conflict-lab` (from `starter_code`) shows all PASS: no markers, merge commit with two parents, correct values.

---

## Project 1 milestone (Part E, 40 min)

> **Project 1: QE Foundations.** One repository, `qe-foundations`. Mon: structure + package. Tue: ingestion module. **Wed (today): logging for ingestion + the first `tests/` suite.** Thu: SQL validation queries. Fri: joins + integration.

Work in your own `qe-foundations` repository on a new branch: `git switch -c wed-logging-tests`. You are adding to the package you already built; your Tuesday ingestion code is the thing under test. Expected layout after today:

```
qe-foundations/
  qe_foundations/
    utils/        __init__.py, validators.py (or your helper module), logging_setup.py   <- NEW file
    ingestion/    __init__.py, <your loader module(s)>                                  <- now logs
  tests/          test_utils.py, test_ingestion.py                                      <- NEW
  data/           your sample files from Tuesday
  docs/           testing.md                                                            <- NEW
  .gitignore                                                                            <- add *.log
```

### E1. Logging setup (15 min)

1. Copy `project1_templates/logging_setup.py` to `qe_foundations/utils/logging_setup.py` and finish `setup_logging(level="INFO", logfile=None)` following the contract in its docstring: it configures the logger named **`qe_foundations`**, adds a console handler at `level` and (if `logfile` is given) a file handler at DEBUG, returns that logger, and **adds no duplicate handlers on a second call**.
2. In your ingestion module(s): `logger = logging.getLogger(__name__)`, **no** `basicConfig`, and at least **3 log calls using at least 2 levels**, for example INFO "loading ... / loaded N good rows, M bad rows", WARNING "row 7 skipped: ...", ERROR "file not found". Replace progress `print()`s with these.
3. Call `setup_logging()` once from your entry point (your `main()` or the script that runs the loader). Run it and look at the console and the log file.
4. Add the lines from `project1_templates/gitignore_additions.txt` to `.gitignore`. Never commit `*.log`.

### E2. The first test suite (20 min)

Create `tests/test_utils.py` and `tests/test_ingestion.py`. **Exactly what to test** (at least **8** tests in total, and the check counts by file name):

| File | Minimum | What |
|---|---|---|
| `tests/test_utils.py` | **4 tests** | at least 3 normal cases for your helpers (for example status normalisation, a percentage, a validator) and **at least 1 bad-input test with `assertRaises`** (empty/`None`/wrong type/zero division, whichever your helper rejects) |
| `tests/test_ingestion.py` | **4 tests** | a good file loads all rows; a file with a bad row reports it and keeps the good rows; a **missing file** raises your exception (`assertRaises`); a file with a **missing column or malformed content** raises or reports (`assertRaises`); **at least 1 `assertLogs`** proving the WARNING for a bad row is logged |

Rules for these tests: they create their own input files with `tempfile` (`TemporaryDirectory` plus `addCleanup`, or a `with` block); they never depend on a file on your laptop; each test checks one behaviour; no test calls another.

Run exactly this, from the repository root:
```
python -m unittest discover -s tests
```
It must report **at least 8 tests, all OK**. If you get `ModuleNotFoundError: qe_foundations`, you are not in the repository root.

### E3. Document and commit (5 min)

1. Create `docs/testing.md` (5 lines is enough): how to run the tests (the exact command above, containing the words `unittest discover`), and where the log file goes.
2. Commit in small steps with clear messages (for example `Add setup_logging to utils`, `Log from ingestion loader`, `Add utils and ingestion unit tests`).

### Part E result
`python check_exercise.py --part E --project <path-to-qe-foundations>` shows **all PASS**. Push the branch and open a pull request into `main` (Monday's workflow).

---

## Self-check (all parts)

From `starter_code`:

PowerShell:
```powershell
python check_exercise.py --conflict-repo ..\conflict-lab --project ..\..\qe-foundations
```
bash:
```bash
python3 check_exercise.py --conflict-repo ../conflict-lab --project ../../qe-foundations
```
(Adjust the paths to where your folders really are. With no options it checks Parts A, B and C only. `--part D` runs one part.) Read each `hint:` line under a FAIL. **Green means the automatic checks pass; your mentor still reads your debug log and code.**

---

## Definition of Done

- [ ] **A.** All 7 tickets fixed; `check_exercise.py --part A` passes; `debug_log.md` complete with real evidence for every ticket and a reflection; no `breakpoint()` left.
- [ ] **B.** `run_stats.py` has a `logger`, no `print`, DEBUG/INFO/WARNING calls as in the table; `run_report.py` configures console INFO + file DEBUG once; `run_report.log` exists locally and is **not** committed.
- [ ] **C.** `test_run_stats.py` has at least 12 independent, well-named tests, at least one per ticket, 3+ bad-input tests, `assertRaises`, `setUp`, `assertLogs`; passes on your fix and fails on `_baseline`.
- [ ] **D.** `conflict-lab` merged, no markers, two-parent merge commit, `python report.py` prints the two expected lines; `conflict_notes.md` and `conflict_graph.txt` written.
- [ ] **E.** `qe_foundations/utils/logging_setup.py`, ingestion logging, `tests/` with at least 8 tests passing under `python -m unittest discover -s tests`, `docs/testing.md`, `*.log` ignored; branch pushed and PR opened.
- [ ] `python check_exercise.py ...` is green for every part you submitted.

## Submission

1. **Parts A to C**: from `week2-wed`, create a repo (`git init -b main`), commit `starter_code/run_stats.py`, `run_report.py`, `test_run_stats.py`, `debug_log.md`, plus `conflict_notes.md` and `conflict_graph.txt`; do **not** commit `run_report.log`, `__pycache__`, or `conflict-lab`. Push to your personal repository (or the cohort submission repo if your mentor named one).
2. **Part D** evidence is `conflict_graph.txt`, `conflict_notes.md`, and (optional) your `conflict-lab` folder zipped.
3. **Part E**: push branch `wed-logging-tests` of `qe-foundations` and open a PR. Paste the link and the final lines of `python -m unittest discover -s tests` in the PR description.
4. Post the repo and PR links to your mentor. Paste the **Summary** block from `check_exercise.py` as proof.

## Grading rubric (100 points)

| Area | Points | Full marks | Partial credit |
|---|---|---|---|
| **A. Debugging** | 25 | 7/7 tickets fixed (2 pts each = 14); debug log has genuine evidence (pdb command and output) and root cause for each (9); one post-mortem or traceback read and reflection (2) | 1 pt per ticket if the symptom is fixed but the root cause in the log is wrong or vague |
| **B. Logging** | 15 | module logger, correct levels, no `print`/`basicConfig` in the module (8); entry point: console INFO + file DEBUG, no duplicate handlers (7) | f-strings in log calls or wrong level: -1 each |
| **C. Unit tests** | 20 | 12+ tests, independent, well named (6); every ticket has a regression test that fails on `_baseline` (8); bad input, `assertRaises`, `assertLogs`, `setUp` used correctly (6) | untested edge cases or tests that depend on order: -1 each |
| **D. Merge conflict** | 15 | correct resolution and the 4 team decisions followed (8); finished merge commit with two parents, history intact (4); `conflict_notes.md` shows understanding (3) | markers left or decision #1 or #2 wrong: lose that line's points |
| **E. Project 1 milestone** | 20 | `setup_logging` contract met (5); ingestion logs at 2+ levels (4); 8+ tests meeting the table, all passing under `unittest discover` (8); docs and `.gitignore` (3) | tests that pass but test nothing (no assertion on behaviour): -2 each |
| **Git and professionalism** | 5 | small commits with clear messages, no `.log`/`__pycache__` committed, PR description complete | |

**Bands:** 90-100 ready to build on Thursday | 75-89 solid, fix the listed gaps | 60-74 re-do the weakest part before Thursday | under 60 mentor session needed.

---

## Stretch goals (optional, only after the Definition of Done)

1. **Conditional breakpoint.** In `median`, pause only when `len(values) % 2 == 0` using `if ...: breakpoint()` and note what you saw (see the conditional breakpoints lesson section).
2. **Table-driven tests.** Rewrite BUG-1 and BUG-2 tests with `subTest` over a table of at least 5 cases each.
3. **Test the log text.** Use `assertLogs` to assert the exact WARNING wording for a missing suite, and `assertNoLogs` (Python 3.10+) for a clean input.
4. **diff3 markers.** Re-run `setup_conflict` with `-Force`/`--force`, run `git config merge.conflictstyle diff3`, and compare the markers: what does the extra `|||||||` section show? Write 3 sentences.
5. **Abort and redo.** `git merge --abort` in a fresh lab, then resolve using only `git checkout --ours/--theirs` for `settings.py` and hand-edit for the rest. Which approach was safer?
6. **Rotating log.** Replace the file handler in `run_report.py` with `logging.handlers.RotatingFileHandler(maxBytes=50_000, backupCount=2)`.
7. **Project 1 extra.** Make your loader log one summary line at the end (`rows=120 good=117 bad=3 elapsed=0.04s`) and test it with `assertLogs`.

---

## Progressive hints

Open **one level at a time**, only after at least 10 minutes on the ticket.

<details>
<summary>BUG-1 (median)</summary>

- **Level 1 (where):** Run `python run_report.py 1`. Put `breakpoint()` before the `return` in `median` and print `ordered`, then `len(ordered)`, then `len(ordered) // 2`.
- **Level 2 (what):** For four numbers, which positions are the two middle ones? Does the code ever use more than one of them?
- **Level 3 (how):** Even length needs the mean of `ordered[mid - 1]` and `ordered[mid]`; odd length keeps the single middle value.
</details>

<details>
<summary>BUG-2 (slowest)</summary>

- **Level 1:** In pdb, `p durations[:3]`, then `p durations[:2]`. Which one matches the code's slice, and what is `n - 1` when `n` is 0?
- **Level 2:** A slice `[:k]` returns `k` items. What `k` do you want?
- **Level 3:** Only the slice end is wrong. (BUG-6 is a *different* defect on the line above it; leave it for ticket 6.)
</details>

<details>
<summary>BUG-3 (group_by_suite)</summary>

- **Level 1:** `python -m pdb run_report.py 3`, type `c`; pdb stops at the crash. `p grouped` and `p result["suite"]`.
- **Level 2:** `grouped["login"]["pass"] += 1` first *reads* `grouped["login"]`. Does that key exist at that moment? Then the count.
- **Level 3:** `dict.setdefault(key, {})` and `dict.get(key, 0)` are the two tools. A result without `"suite"` should land under `"unknown"`: `result.get("suite", "unknown")`.
</details>

<details>
<summary>BUG-4 (note_flaky)</summary>

- **Level 1:** Add `print(id(flaky))` (or `p id(flaky)`) and call it twice without passing a list. Also `p note_flaky.__defaults__` after the first call.
- **Level 2:** When does Python create the default value: each call, or once?
- **Level 3:** Use `None` as the default and create the list inside the function (`mutability-and-memory.md`). Compare with `is None`, not truthiness.
</details>

<details>
<summary>BUG-5 (next_run_id)</summary>

- **Level 1:** Read the last line of the traceback aloud. Then `pp locals()` at the line before it.
- **Level 2:** `run_counter += 1` is an assignment. What does an assignment inside a function do to the name's scope (LEGB)?
- **Level 3:** Tell Python the name lives at module level with the `global` statement, or restructure so no assignment to a module name is needed.
</details>

<details>
<summary>BUG-6 (latest_ms is wrong, list reordered)</summary>

- **Level 1:** Put a `breakpoint()` at the top of `summarise_run`; `p durations`. Step with `n` over each line and `p durations` again after each call. When does it change?
- **Level 2:** One of the functions it calls changes the list that *you* passed in. Which list method sorts in place, and which function returns a sorted copy?
- **Level 3:** `sorted(...)` returns a new list; `.sort()` changes the original.
</details>

<details>
<summary>BUG-7 (empty durations)</summary>

- **Level 1:** `python run_report.py 7` after fixing 1 to 6. Read the traceback bottom-up; post-mortem it.
- **Level 2:** Two places need a decision: what should `median([])` do (the docstring says), and what should `summarise_run` do when there is nothing to take a median of or a `[-1]` of?
- **Level 3:** `median` raises `ValueError("median() needs at least one value")`; `summarise_run` guards with a conditional expression and uses `None` for `median_ms` and `latest_ms`.
</details>

<details>
<summary>Part B (logging) is not showing what I expect</summary>

- Nothing appears at all: the logger or handler level is above your message. The **logger** must allow DEBUG (gate 1) and each **handler** filters again (gate 2).
- Lines appear twice: you added handlers more than once. Guard with `if logger.handlers: return`.
- `basicConfig` seems ignored: something already logged before it ran (the `logging.md` trap). Configure handlers explicitly instead.
- `assertLogs` fails in Part C: the logger name must match; with `getLogger(__name__)` in `run_stats.py` it is `"run_stats"`.
</details>

<details>
<summary>Part D (conflict) is stuck</summary>

- `git status` lists `both modified` files: those are the ones with markers. A file listed as modified in green merged fine.
- Between `<<<<<<< HEAD` and `=======` is **your side (main)**; between `=======` and `>>>>>>> feature/strict-gate` is **Sam's**. Decide, then delete all three marker lines.
- "Your merge commit failed, who are you?" Set `git config --global user.name` and `user.email`.
- You made a mess: `git merge --abort`, then re-run the setup script with `-Force` / `--force`.
- Still stuck on `report.py`: the final file has `verdict`, then `summary_line`, then `failing_suites`, then `main`.
</details>

<details>
<summary>Part E (Project 1) is stuck</summary>

- **Tests cannot import your package:** run from the repo root and use `python -m unittest discover -s tests` (not `python tests/test_x.py`).
- **No `__init__.py` in `utils` or `ingestion`:** add an empty one.
- **Tests that need a file:** write it in `setUp` into a `tempfile.TemporaryDirectory()` and register `self.addCleanup(tmp.cleanup)`.
- **Your Tuesday module has no custom exceptions or returns a different shape:** test *your* behaviour. Read your own docstrings and test what they promise; fix the code if a test shows it does not keep the promise.
- **Do not have a Tuesday module?** Build the smallest loader that reads a CSV, skips bad rows and raises on a missing file (Tuesday's lessons and demo), then do E1 and E2 on it.
</details>
