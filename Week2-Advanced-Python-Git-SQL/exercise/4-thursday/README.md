# Pair Project: Data Validation Queries for the Test-Run Database

**Week 2, Day 4 (Thursday): SQL Fundamentals**  |  Collaborative project  |  Pair programming (Driver / Navigator)  |  3 hours

> **Project 1 milestone (QE Foundations).** Today your pair adds the **data validation queries** to the `qe-foundations` repo: a `sql/validation_queries.sql` file plus a Python runner in `qe_foundations/validation/` that loads the sample data, executes every query and prints **PASS / FAIL** per rule. Friday adds joins and integrates it all.

---

## 1. The scenario

Your team runs thousands of automated tests. Every execution is stored as one row in a SQLite table called `test_runs`: which test, which suite, which environment, how long it took, who ran it, which build, and why it failed. Dashboards and flaky-test reports are built on this table.

The data feed is flaky, and the table accepts almost anything. Last week a report said "average run time: -4 minutes". Your pair has been asked to build a **validation suite** that proves, rule by rule, what is wrong with the data, and that can run automatically on every build.

You are not fixing the data (changing data is Friday). You are **finding and proving** the problems, like a QA engineer reading behind the UI.

## 2. What you will produce (the shared artifact)

One shared **repository and feature branch** (`feature/sql-validation-<names>`) of `qe-foundations` that contains:

| # | Artifact | Where | Built with |
|---|---|---|---|
| 1 | **12 violation queries + 2 expectation queries** | `sql/validation_queries.sql` | Thursday: SELECT / WHERE / IN / BETWEEN / LIKE / IS NULL / TRIM / ORDER BY / LIMIT |
| 2 | **A Python runner** that loads the seed data, runs each query, prints `PASS`/`FAIL` per rule with the offending rows, and sets an exit code | `qe_foundations/validation/runner.py` | Mon: package, `python -m` |
| 3 | **Logging**: console at INFO, file at DEBUG (`logs/validation.log`) | `setup_logging()` in `runner.py` | Wed: `logging` |
| 4 | **A custom exception** `ValidationFailedError` that carries the rule id and the violating rows | `qe_foundations/validation/exceptions.py` | Tue: custom exceptions |
| 5 | **At least 5 `unittest` tests** (one with `assertRaises`, one proving a rule catches a known bad row) | `qe_foundations/tests/test_validation.py` | Wed: unittest |
| 6 | **Docs**: defect checklist, 2 defect reports, pairing log, **retrospective** | `qe_foundations/docs/` | Thu: reporting |
| 7 | **Good Git collaboration**: feature branch, both partners committing under their own names, `pull`/`fetch`/`push`, a pull request (or equivalent) | the repo history | Mon + Wed: Git |

### How the week fits together

| Day | Skill | Where you use it today |
|---|---|---|
| Monday | Packages, imports, venv, `git pull` / `fetch` / `push` | `qe_foundations/validation/` is a package run with `python -m`; you share one branch |
| Tuesday | Exceptions, files, context managers | `ValidationFailedError`; the runner reads `.sql` files |
| Wednesday | Logging, `unittest`, debugging, merge conflicts | `setup_logging()`, `test_validation.py`; if you both edit the same line, you resolve it |
| **Thursday** | **SQL: SELECT, WHERE, ORDER BY, QA validation** | **the queries (the heart of today)** |
| Friday (preview) | JOINs, GROUP BY, DML, constraints | not today: you will extend this suite then |

> **Only Monday-Thursday material is needed.** If you find yourself wanting `JOIN`, `GROUP BY`, `HAVING`, a sub-query, `INSERT`, `UPDATE` or `DELETE`, stop: there is a Thursday way (usually `OR`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`).

## 3. Before you start: read these

You will need the **Using SQL for QA Data Validation** lesson open all day (especially sections 4, 5, 9, 10 and 14), plus **Filtering and Sorting Data** for `NULL`, `LIKE`, `BETWEEN`. Our table is *not* the lesson's `orders` table, so you cannot copy its queries, but the *method* is identical. (Optional warm-up: before Block 1, the navigator reads aloud rules V-01 to V-05 of the lesson and the driver predicts which rows the lesson's `orders` queries return. Five minutes, no repo needed.)

## 4. Timeline (3 hours, swap every 30 minutes)

| Clock (offset) | Block | Driver | Navigator | Goal |
|---|---|---|---|---|
| 0:00-0:10 | **Kickoff** | both | both | Read this README together; agree who is **Partner A** and **Partner B**; create the branch and set up (section 5) |
| 0:10-0:40 | **Block 1** | **A** | B | Explore `test_runs`; fill the "Predicted" column; write **R-01 to R-04** |
| 0:40-1:10 | **Block 2** | **B** | A | **R-05 to R-08** |
| 1:10-1:40 | **Block 3** | **A** | B | **R-09 to R-12**, then **E-01 and E-02** |
| 1:40-2:10 | **Block 4** | **B** | A | Python: `ValidationFailedError`, `run_rule`, `run_all`, `setup_logging`, `main` (the runner) |
| 2:10-2:40 | **Block 5** | **A** | B | Unit tests, defect checklist, 2 defect reports; run `check_exercise.py` and fix FAILs |
| 2:40-3:00 | **Wrap-up** | both | both | Fill the retrospective; final check; pull request; push |

**How a swap works (every 30 minutes, even mid-rule):**

1. The driver finishes the current thought (do not leave the file broken), saves and runs the suite once.
2. Driver commits **with their own name** and pushes: `git add -A`, `git commit -m "..."`, `git push`.
3. The navigator becomes the driver: `git pull` (or `git fetch` then `git log origin/<branch>` to look, then `git pull`), then runs the suite to confirm it works on their machine.
4. The old driver fills one row of `docs/pairing_log.md`.

If the work is behind schedule, the **blocks do not move**: swap on time and carry the unfinished rules over. Stuck on one rule for more than 8 minutes? Take the next hint level (section 9), or skip and come back.

## 5. Setup (kickoff, about 10 minutes)

The commands differ a little by shell. **PowerShell** is shown first, **bash** (macOS / Linux / Git Bash) second. Where there is only one block, it works in both.

Let `EX` be the folder holding this exercise (the folder with `starter_code/` and `templates/`).

### 5.1 One shared repo, one shared branch

Pick **one** `qe-foundations` repo from your Monday-Wednesday work as the *host* (the owner is Partner A). Partner B needs write access (GitHub: **Settings > Collaborators**) and clones it.

```text
# Partner B only
git clone <host-repo-url> qe-foundations
cd qe-foundations
```

**Both partners**, on your own laptop, set your identity. This is what makes `git log` show who did what:

```text
git config user.name "Your Real Name"
git config user.email "you@example.com"
git config user.name        # prints it back: check!
```

**Partner A** creates the branch and pushes it; **Partner B** then fetches it:

```text
# Partner A
git switch -c feature/sql-validation-<a>-<b>
git push -u origin feature/sql-validation-<a>-<b>

# Partner B
git fetch origin
git switch feature/sql-validation-<a>-<b>
```

> **No GitHub access?** Use a local shared remote. Same room, shared folder: `git init --bare ..\pair-remote.git` (PowerShell) or `git init --bare ../pair-remote.git` (bash), then `git remote add origin <that path>` and `git push -u origin <branch>`. Everything else is identical.
>
> **One laptop only?** Set the committer per commit: `git commit --author="Partner Name <p@example.com>" -m "..."`, alternating at each swap. Two real machines are strongly preferred.

### 5.2 Copy the starter files into the repo (Partner A, once)

Run from the **root of your `qe-foundations` repo** (the folder containing `qe_foundations/`).

PowerShell:

```powershell
$EX = "C:\path\to\exercise\4-thursday"          # edit this
Copy-Item -Recurse -Force "$EX\starter_code\*" .\
Get-Content "$EX\starter_code\gitignore_additions.txt" | Add-Content .gitignore
Remove-Item .\gitignore_additions.txt
Copy-Item "$EX\templates\retrospective_template.md"   .\qe_foundations\docs\retrospective.md
Copy-Item "$EX\templates\pairing_roles_swap_log.md"   .\qe_foundations\docs\pairing_log.md
Copy-Item "$EX\templates\defect_report_template.md"   .\qe_foundations\docs\defect_reports.md
```

bash:

```bash
EX=/path/to/exercise/4-thursday                 # edit this
cp -r "$EX"/starter_code/. ./
cat "$EX/starter_code/gitignore_additions.txt" >> .gitignore
rm gitignore_additions.txt
cp "$EX/templates/retrospective_template.md"  qe_foundations/docs/retrospective.md
cp "$EX/templates/pairing_roles_swap_log.md"  qe_foundations/docs/pairing_log.md
cp "$EX/templates/defect_report_template.md"  qe_foundations/docs/defect_reports.md
```

You should now have `sql/`, `check_exercise.py`, `qe_foundations/validation/`, `qe_foundations/data/`, `qe_foundations/docs/` and `qe_foundations/tests/test_validation.py`. (If your repo has no `qe_foundations/__init__.py` or `qe_foundations/tests/__init__.py` from Monday, create empty ones.)

### 5.3 Smoke test, then the first commit

Activate your virtual environment from Monday (`.\.venv\Scripts\Activate.ps1` in PowerShell, `source .venv/bin/activate` in bash). **No `pip install` is needed**: SQLite ships with Python. On Windows use `py` instead of `python` if `python` is not found.

```text
python -m qe_foundations.validation --query "SELECT COUNT(*) AS runs FROM test_runs"
python check_exercise.py
```

The first prints `60`. The second shows **many FAIL lines**: that is correct, it is your to-do list. Partner A commits and pushes the starter; Partner B pulls:

```text
git add -A
git commit -m "Add starter files for the SQL validation milestone"
git push
```

### 5.4 Looking at the data (three ways, pick any)

```text
python -m qe_foundations.validation --query "SELECT * FROM test_runs ORDER BY run_id"
python -m qe_foundations.validation --show R-03          # rows the current R-03 query returns
python -m qe_foundations.validation --setup-only --db test_runs.db     # then open test_runs.db in DB Browser for SQLite
```

(`test_runs.db` is git-ignored; never commit it.)

## 6. The data and the rules

### 6.1 The table `test_runs` (60 rows, `qe_foundations/data/`)

| Column | Meaning | Allowed |
|---|---|---|
| `run_id` | unique id (primary key) | integer |
| `test_name` | e.g. `test_login_valid_user` | text, no leading/trailing spaces |
| `suite` | grouping | `SMOKE`, `REGRESSION`, `API` (no stray spaces) |
| `environment` | where it ran | exactly `DEV`, `QA`, `STAGING` |
| `status` | outcome | exactly `PASSED`, `FAILED`, `SKIPPED`, `ERROR` |
| `duration_ms` | run time in milliseconds | present, `>= 0`, plausible |
| `retries` | automatic re-runs used | present, `0` to `3` |
| `started_at`, `finished_at` | timestamps | text `YYYY-MM-DD HH:MM:SS` (SQLite has no date type) |
| `executed_by` | e-mail of the person or bot | present, looks like an e-mail |
| `build_id` | build under test | `B-` + 4 characters, e.g. `B-1042` |
| `failure_message` | why it failed or was skipped | NULL when none |

Do **not** read `test_runs_seed.sql` to find the defects: that defeats the exercise. (You will, however, need to read the data **through queries**.)

### 6.2 The rule catalogue (the business requirements)

Each rule has an id you must keep. Write a **violation query** for each `R-xx` (a query that returns the *bad* rows, so **0 rows = PASS**). `E-xx` are **expectation queries** (they return the row you *expect*, so **1 row = PASS**).

| Id | Dimension | The rule in plain English |
|---|---|---|
| **R-01** | Completeness | `executed_by` must be present: not NULL, not blank, not spaces only |
| **R-02** | Validity | `executed_by`, **when present**, must look like an e-mail: contain `@` and a `.` after it |
| **R-03** | Validity | `status` must be exactly `PASSED`, `FAILED`, `SKIPPED` or `ERROR` (upper case, exact) |
| **R-04** | Validity | `duration_ms` must be present and not negative. **0 is legal** (a skipped test takes no time) |
| **R-05** | Accuracy | `duration_ms` above **600000** (10 minutes) is an outlier that needs review |
| **R-06** | Validity | `retries` must be present and between 0 and 3, inclusive |
| **R-07** | Validity | `environment` must be exactly `DEV`, `QA` or `STAGING` |
| **R-08** | Consistency | `test_name`, `suite` and `status` must have no leading or trailing spaces |
| **R-09** | Validity | `started_at` and `finished_at` must both be present and shaped `YYYY-MM-DD HH:MM:SS` |
| **R-10** | Consistency | a run cannot finish before it starts, and cannot start in the future |
| **R-11** | Consistency | `FAILED`/`ERROR` runs need a non-blank `failure_message`; `PASSED` runs must have none (`SKIPPED` may keep a skip reason) |
| **R-12** | Validity | `build_id` must be present and look like `B-1042`: upper-case `B`, a dash, 4 characters |
| **E-01** | Expectation | run `5001` was saved as expected: `test_login_valid_user`, suite `SMOKE`, env `QA`, status `PASSED`, build `B-1042` (**1 row**) |
| **E-02** | Expectation | test-data discovery: the **most recent FAILED run in QA** (by `started_at`) exists: return exactly that one row |

### 6.3 Rules of the format (the check script depends on them)

- Keep every `-- @rule <ID> | <Dimension> | <description>` header line and every `-- @expect N` line exactly as in the starter. Never edit `@expect` to make a rule pass.
- **One** read-only `SELECT` per rule, ending in `;`.
- The **first selected column must be `run_id`** (the evidence). Add any other columns that show *why* a row is bad.
- Each rule is judged **on its own** (a run may legitimately appear in two rules).
- Beware of **false alarms**: a few rows look odd but are *legal*. A good rule does not flag them. The check script tells you if a query returns too many or too few rows.

## 7. What each block does

### Kickoff (0:00-0:10)
Section 5. Read the rule table aloud. Agree on how you will name commits (`Add R-03 status check`).

### Block 1 (A drives): explore, then R-01 to R-04
1. **Look before you query.** `PRAGMA table_info(test_runs)`, `SELECT * ... LIMIT 10`, `SELECT DISTINCT status ...`. Which columns allow NULL? What values does `status` really hold?
2. For each rule: **the navigator reads the rule, both predict the defect rows aloud**, and the driver writes the prediction in `docs/defect_checklist.md` (column "Predicted"). *Then* write the query, run it (`--show R-01`), fill "Defects found".
3. Compare your prediction and the result. A surprise is the interesting part: note it.

### Block 2 (B drives): R-05 to R-08
Same ritual. Watch the traps: inclusive `BETWEEN`, `NOT IN` and NULL, exact-case matching, whitespace.

### Block 3 (A drives): R-09 to R-12, E-01, E-02
The trickiest rules: patterns, comparing two columns of the same row, `AND`/`OR` precedence, and the case-insensitivity of `LIKE`. Then the two expectation queries. Run `python check_exercise.py`: the **SQL section** should now be green (the `-- @expect` of E-01 and E-02 is **1**).

### Block 4 (B drives): the Python runner
Open `qe_foundations/validation/runner.py`; `parse_rules`, `connect`, `load_seed`, `fetch_rows` are provided. You implement the four `TODO`s:

1. `ValidationFailedError` in `exceptions.py` (Tuesday): attributes `rule_id`, `description`, `rows`; a one-line message naming the rule and row count.
2. `setup_logging()`: console at INFO, file at DEBUG, create the `logs/` folder, no duplicate handlers if called twice (Wednesday).
3. `run_rule(conn, rule)`: raise `ValidationFailedError(rule, rows)` when the row count differs from `rule.expect`; informational rules (`expect is None`) never raise.
4. `run_all(...)`: print exactly `PASS  R-01  ...` / `FAIL  R-02  ...` / `INFO ...` lines (see the docstring), log each result (`INFO` for pass, `WARNING` for fail, `logger.exception` + re-raise for a broken query), print evidence rows indented under each FAIL, finish with a summary; and in `main()`: exit code `1` if any rule FAILs, unless `--allow-failures`.

Target output (yours will differ in wording):

```text
PASS  E-01  Expectation   run 5001 was saved as expected ...
FAIL  R-02  Validity      executed_by, when present, must look like an e-mail ...  (2 row(s) returned)
      (5011, 'priya.nair')
      ...
Summary: 2 PASS, 12 FAIL, 0 INFO
```

12 FAIL is **correct** for this data: the suite has found the problems. A runner that prints all PASS is a bug in your SQL.

### Block 5 (A drives): tests, checklist, reports
1. **Tests** (`test_validation.py`): replace the four `self.fail("TODO")` stubs. Arrange / act / assert, one idea per test. You need **>= 5 passing tests**, including one `assertRaises(ValidationFailedError)` and one that proves a rule catches **specific known bad run_ids**. Add more if time allows (e.g. "a legal 0 ms SKIPPED run is *not* flagged by R-04").
2. **Defect checklist**: every R-xx row has its run_ids; list at least two **decoys** (legal rows that look odd).
3. **Defect reports** (`docs/defect_reports.md`): choose the two most serious findings and write each as a real bug report with the exact query, evidence, impact and a "could this be a false alarm?" question.
4. Run `python check_exercise.py`, fix every FAIL.

### Wrap-up (last 20 minutes, both)
1. Fill `docs/retrospective.md` **together** (about 15 minutes).
2. Both partners: `git pull`, run `python check_exercise.py`, run the suite once more.
3. Open a **pull request** from your feature branch into `main` (GitHub) with the text from `templates/pr_branch_checklist.md`; with a local bare remote, tick the checklist in the PR text file instead. The partner who did **not** open the PR reviews it. **Do not merge** unless your instructor says so.

## 8. Pair-programming guide

### The two roles

| | DRIVER | NAVIGATOR |
|---|---|---|
| Hands | the **only** one typing | off the keyboard (no "just let me..." grabs) |
| Thinks about | the next few lines, syntax | the big picture: the rule, edge cases, the next 2-3 steps, the clock |
| Says | what they are typing and why, aloud | "Read the rule again." "Predict: which run_ids?" "What about NULL?" "Run it." |
| Must not | type silently, or ignore the navigator | dictate every character, or check their phone |

**Habits that make validation work better**

- **Predict before you run**: "I expect 5006, 5019 and 5025." Surprises are where you learn.
- **Navigator explains the query back in plain English** before it is committed. If they cannot, it is not ready.
- **Catch the false pass**: a query returning 0 rows may mean "no defects" *or* "wrong query". The checklist and `check_exercise.py` exist for exactly this.
- **Small commits**: roughly every rule or two, and always at a swap.
- Disagree with evidence, not volume: put both versions in a query and run them.

### Ground rules

1. **One keyboard.** Only the driver types, including into the docs. The navigator's laptop may be open on the lesson, never on the repo.
2. **Swap on the clock**, every 30 minutes. Log it.
3. **Both partners understand every line** that goes into `main`. You may be asked to explain any query.
4. **Own names on commits**: `git log` should show two authors. Never share one Git identity.
5. **Pull before you type**, push when you stop.
6. **Use hints** (section 9) freely, but record which ones in the pairing log.
7. **Respect the pace of both partners**: the stronger partner navigates as a coach (asks questions), not as a typist. Help each other; do not split the work into "your half / my half".
8. **No copy-pasting from the lesson's `orders` queries or from other pairs**: it will not match this data anyway.
9. Thursday toolkit only (section 2). Read-only queries only.

## 9. Progressive hints

Take them in order. Level 1 first; each level gives away more. Record what you used.

### Level 1: which idea to reach for

| Rule | Hint |
|---|---|
| R-01 | "Missing" has more than one spelling in a text column. Which ones can you list? |
| R-02 | Describe a valid e-mail as a `LIKE` pattern, then negate it. What should happen to rows R-01 already caught? |
| R-03 | A list of allowed values means `IN`, the opposite means `NOT IN`. What does `NOT IN` do with a NULL? |
| R-04 | Write down which numbers are illegal. Is 0 one of them? Which rows have 0 and what status do they have? |
| R-05 | One comparison and a sort that shows the worst first. |
| R-06 | A closed range: is `BETWEEN` inclusive? |
| R-07 | Same family as R-03. Is `'qa'` equal to `'QA'` with `=` in SQLite? |
| R-08 | What changes a value when you `TRIM` it? Compare a column with its trimmed self. |
| R-09 | Timestamps are 19 characters of a fixed shape. `_` in `LIKE` matches exactly one character. Also: NULL. |
| R-10 | ISO-formatted text sorts in time order, so `<` and `>` compare timestamps. What does `date('now')` return? |
| R-11 | Two separate sub-rules, one for each status group. How do you combine them safely? |
| R-12 | Build a `LIKE` pattern for `B-1042`. Then ask: does `LIKE` care about letter case in SQLite? |
| E-01 | An expectation query lists every value you *expect*. How many rows should come back? |
| E-02 | Filter, sort newest first, keep only the top row. |

### Level 2: the pattern

<details>
<summary>Open only after Level 1 (spoilers: query shapes, not full answers)</summary>

- **Missing text:** `col IS NULL OR TRIM(col) = ''`
- **Pattern check, ignoring missing values:** `col IS NOT NULL AND TRIM(col) <> '' AND col NOT LIKE '<pattern>'`
- **Domain list incl. NULL:** `col NOT IN ('A', 'B', 'C') OR col IS NULL`
- **Range incl. NULL:** `col NOT BETWEEN low AND high OR col IS NULL`
- **Stray spaces:** `col <> TRIM(col)`, repeated with `OR` for each column
- **Same-row comparison:** `finished_at < started_at` (both ISO text)
- **Grouped conditions:** `(a AND (b OR c)) OR (d AND e)`: parentheses are your friend
- **Case-sensitive check despite LIKE:** compare the value with `UPPER(value)` (they differ when it contains lower-case letters)
- **Newest first, one row:** `ORDER BY started_at DESC LIMIT 1`

</details>

### Level 3: a skeleton for the hardest rules

<details>
<summary>Open only after Level 2 (R-09, R-11, R-12 outlines with blanks)</summary>

```sql
-- R-09 (fill the blanks)
SELECT run_id, started_at, finished_at
FROM test_runs
WHERE started_at IS NULL
   OR started_at NOT LIKE '____-__-__ __:__:__'
   OR finished_at ______ ...;          -- same two ideas for finished_at

-- R-11 (fill the blanks)
SELECT run_id, status, failure_message
FROM test_runs
WHERE (status IN (...) AND (failure_message ______ OR TRIM(failure_message) = ''))
   OR (status = 'PASSED' AND failure_message ______);

-- R-12 (fill the blanks)
SELECT run_id, build_id
FROM test_runs
WHERE build_id IS NULL
   OR build_id NOT LIKE 'B-____'
   OR build_id <> ______(build_id);    -- which function exposes 'b-1048'?
```

</details>

### Python hints

- Cannot find where to start: `run_rule` is five lines; read the docstring and the `Rule` dataclass.
- `ModuleNotFoundError: qe_foundations`: run from the **repo root**, with `python -m ...` (Monday).
- Duplicate log lines: you attached handlers twice (Wednesday). Guard with `if logger.handlers: return logger`.
- `sqlite3.OperationalError`: a typo in your SQL. Do **not** catch it as "bad data": log it with `logger.exception` and let it propagate.
- Windows console shows odd characters: keep your messages ASCII.

## 10. Self-check

From the repo root:

```text
python check_exercise.py              # Windows: py check_exercise.py
python check_exercise.py --verbose    # more detail
```

It checks, in order: required **files**; each **SQL rule** against the data (it tells you how many rows a rule should return, not which); the **runner** (PASS/FAIL lines, exit codes, log file, the exception, `run_rule` behaviour); your **unit tests**; the **docs**; and your **Git** history (branch, authors, commit count, pushed). Results are `PASS`, `WARN` (should fix), `FAIL` (must fix) or `SKIP`. Exit code 0 means no FAIL. It never changes your files.

The check is a safety net, not the grader: an instructor still reads your queries, your retrospective and your Git history.

## 11. Stretch goals (only when Definition of Done is met)

Each is worth bonus points (max +5 in total).

1. **S-01: the combined dirty-rows query.** One query returning every `run_id` that breaks *any* of R-01 to R-12, each run once (an `OR` chain with parentheses). Add it to the SQL file under the `S-01` header with `-- @expect any`.
2. **S-02: duplicate hunting.** Two runs look like the same execution saved twice (same test, environment, build and start time). Find them with `WHERE` / `ORDER BY` only. Friday's `GROUP BY` will do this automatically; write down what you wish you had.
3. **S-03: test-data discovery.** The 3 slowest runs with a *plausible* duration (0 to 600000 ms).
4. **Reason column.** Make `run_all` print, for every dirty run in the combined list, *which* rules it violates (Python dictionary of `run_id -> [rule ids]`).
5. **Refactor to one base error.** Make `ValidationFailedError` inherit from your project's own base exception from Tuesday (e.g. `QEFoundationsError`), and write a test for it.
6. **`--only R-03 R-04`** option for the runner to run selected rules.
7. **CI-ready**: add a short `docs/validation.md` explaining how to run the suite on a build server, including exit codes.

## 12. Definition of Done

You are done when **all** of these are true:

- [ ] Everyone on the team can explain any query in `sql/validation_queries.sql` in plain English
- [ ] All 14 rules (R-01 to R-12, E-01, E-02) return exactly the rows the check script expects; no `@expect` or header line was edited
- [ ] `python -m qe_foundations.validation` prints one PASS/FAIL line per rule, shows evidence rows under every FAIL, exits `1` on failures and `0` with `--allow-failures`
- [ ] `logs/validation.log` is created; console shows INFO, file shows DEBUG; no duplicated lines
- [ ] `ValidationFailedError` exists, carries `rule_id`, `description` and `rows`, and is raised by `run_rule`
- [ ] `python -m unittest qe_foundations.tests.test_validation` passes with at least 5 tests (including `assertRaises(ValidationFailedError)` and a known-bad-rows test)
- [ ] `docs/defect_checklist.md` (all rules, 2+ decoys), `docs/defect_reports.md` (2 reports), `docs/pairing_log.md` (5 blocks) and `docs/retrospective.md` are complete
- [ ] Work is on `feature/sql-validation-<names>`, pushed, with **both partners' commits** (at least 6, descriptive messages); no `.db`, log or cache files committed; no conflict markers
- [ ] A pull request (or the filled PR checklist) exists and was reviewed by the partner who did not open it
- [ ] `python check_exercise.py` shows **no FAIL**

## 13. Submission

Submit the **link to the pull request or branch** (or, with a local remote, the output of `git log --oneline --format="%h %an %s"` plus a zip of the repo), and paste the final output of `python check_exercise.py` into the PR description. Both partners submit the same link.

## 14. Grading rubric (100 points, plus up to 5 bonus)

| Area | Points | What earns full marks |
|---|---|---|
| **SQL validation queries** | **30** | R-01 to R-12: 2 points each (24); E-01 and E-02: 2 points each (4); first column is `run_id`, no false alarms on legal rows, readable layout (one condition per line, comments where a rule is subtle), Thursday toolkit only, read-only (2) |
| **Python runner, logging, exception** | **20** | `run_rule`/`run_all`/`main` correct (8); logging to console + file, no duplicates, WARNING on failure (6); `ValidationFailedError` well designed and used (6) |
| **Unit tests** | **10** | at least 5 meaningful, independent tests; assertRaises on the custom exception; a known-bad-rows test; a legal-row (no false alarm) test; clear test names |
| **Git collaboration and artifact hygiene** (collaboration) | **15** | feature branch; two authors with real contributions in the history; commits at each swap with good messages; fetch/pull/push used; branch pushed; PR with checklist; clean tree, nothing generated committed; conflicts (if any) resolved properly |
| **Pairing process** (collaboration) | **10** | pairing log complete and plausible (5 blocks, drivers alternate, predictions recorded); evidence both partners drove and navigated (git authorship + log); hint usage honestly recorded; disagreement example |
| **Defect analysis and retrospective** | **10** | checklist consistent with the queries and shows decoys (3); 2 professional defect reports (3); retrospective specific, honest and self-critical, names a real learning (4) |
| **Definition-of-Done / self-check** | **5** | `check_exercise.py` has no FAIL on the submitted branch; README items satisfied |
| **Bonus (stretch goals)** | **+5 max** | S-01 to S-03 correct, extra Python features |

**Collaboration criteria total 25 points.** The instructor may adjust an *individual's* mark by up to 10 points either way, based on the commit authorship, the pairing log and a short individual explanation of any query ("walk me through R-11"): the team score is shared, individual understanding is not.

**Indicators of a weak submission:** all commits by one author; one partner never drove; queries that return nothing (false passes) left as they were; edited `@expect` values; a retrospective that says "it went well" without an example.

## 15. After today: what comes next

Friday adds `INSERT`/`UPDATE`/`DELETE`, constraints, **JOINs**, **GROUP BY/HAVING** and sub-queries. Your suite will then gain real duplicate detection (S-02), cross-table checks (does every run belong to a known test?), and the Project 1 integration. Keep your branch tidy: you will merge it first thing tomorrow.
