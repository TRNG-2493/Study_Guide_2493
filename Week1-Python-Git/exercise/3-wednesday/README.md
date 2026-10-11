# Day 3 (Wednesday) Exercise: Build a Test-Data Manager on a Feature Branch

**Course:** AI enabled Test Automation Engineer (QEA v1), Week 1 "Python Programming and Git Foundations"
**Mode:** Individual code lab | **Time:** 2 to 3 hours (about 2 h 25 min for the core, up to 30 min extra for stretch goals)

## 1. Scenario

You have joined a QE team. Every night a test-management tool exports test cases as raw records. The export is messy:

- the same test case appears more than once (and one was re-run with a different status),
- one record has no `status` yet,
- nobody can quickly answer "what is the status of TC-107?", "which tests belong to the checkout module?" or "which planned tests have not run?".

You will build a small **test-data manager** in plain Python, and you will build it the way professional teams do: on a **feature branch**, one commit per feature, then **merged into `main`**.

## 2. Learning Objectives

By the end you can:

1. Represent test cases as a list of dictionaries and read them with a loop.
2. Use **slicing** (`[:3]`, `[-2:]`, `[::2]`) to take parts of a list.
3. Remove duplicates while keeping order, using a **set** and a **list**.
4. Group records with `defaultdict(list)`, count with `Counter`, and look up records with a **dict** and `.get()`.
5. Compare collections with **set difference** (planned vs executed).
6. Create a feature branch, commit once per feature, merge into `main`, and read the history with `git log --graph`.

## 3. Prerequisites (written topics to review)

| Topic (written material) | Day | You need it for |
|---|---|---|
| Variables, Data Types and Operators; Input and Output Operations | Mon | variables, `print` |
| Introduction to Git and Repository Setup; Git add, commit, status and log | Mon | `git init`, `add`, `commit`, `status`, `log` |
| Conditional Statements (if, elif, else); Loops (for and while) | Tue | the `for` and `if` in every part |
| .gitignore | Tue | the starter already contains one |
| Clone, Pull, Push and Fetch; Basic Pull Request / Merge Request Workflow | Tue | optional push at the end |
| Lists, Tuples, Dictionaries and Sets | Wed | records, set of seen IDs, lookup dict |
| Indexing and Slicing | Wed | Part 1 |
| Collection Operations and Methods | Wed | `append`, `add`, `.get`, `sorted` |
| Introduction to the Collections Module | Wed | `defaultdict`, `Counter` |
| Applying Data Structures to Test-Data Scenarios (sections 4 to 7 and 11) | Wed | the plan for this exercise |
| Git Branching Fundamentals: Branch Creation, Checkout and Merge; Working With Remote Repositories and Branches (section 8, "Complete Workflow for the Exercise") | Wed | the whole Git workflow |

**No functions needed.** Functions come on Thursday. Write plain statements (variables, `for`, `if`) like the Tuesday material. (If you already know `def`, see stretch goal S1.)

**Tools:** Python 3.10+ (`python3 --version`), Git 2.23+ (`git --version`), `git config user.name` and `user.email` set.

## 4. What is in `starter_code/`

| File | What it is |
|---|---|
| `manager.py` | The file you edit. Sample data plus numbered `TODO`s in 5 parts |
| `check_exercise.py` | Self-check: run `python3 check_exercise.py`. Do not edit it |
| `PROJECT_NOTES.md` | A small notes file you will use to practise merging |
| `.gitignore` | Ignores `__pycache__/`, `*.pyc`, `.venv/` |

## 5. Time Plan

| Part | Task | Time |
|---|---|---|
| 0 | Set up the repo and the feature branch | 15 min |
| 1 | Raw IDs and slicing | 15 min |
| 2 | Remove duplicates | 25 min |
| 3 | Group by module | 20 min |
| 4 | Lookup by ID | 20 min |
| 5 | Counts by status and planned-vs-executed | 25 min |
| 6 | Merge into `main`, check, (optional) push, submission | 25 min |
| | **Core total** | **145 min (2 h 25 min)** |
| S | Stretch goals (optional) | up to 30 min |

If you are behind at the 2 h mark, finish Parts 1 to 5 and the merge. Skip the push and the stretch goals.

## 6. Core Tasks

**Rule for the whole exercise:** do one part, run `python3 manager.py` and `python3 check_exercise.py`, then **commit**. One part = one commit.

### Part 0: Set up (15 min)

```bash
# copy the starter_code folder somewhere outside any other repo, e.g.
cp -r starter_code test-data-manager
cd test-data-manager
git init -b main
git status                       # see the untracked files
git add .
git commit -m "Initial commit: starter files"
git switch -c feature/test-data-manager
git branch                       # the * must be on feature/test-data-manager
python3 check_exercise.py        # expect 0/5 passing: that is your starting point
```

**Checkpoint 0:** `git log --oneline` shows 1 commit and `git branch` shows you on `feature/test-data-manager`. If `git switch` is not found, your Git is older than 2.23: use `git checkout -b feature/test-data-manager`.

### Part 1: Raw IDs and slicing (15 min)
Topics: *Loops (for and while)*, *Indexing and Slicing*.

In `manager.py`:
- **1a** Fill `raw_ids` with the `"id"` of every record in `RAW_TEST_CASES` (a `for` loop and `append`).
- **1b** `first_three_ids`: the first 3 IDs (slice).
- **1c** `last_two_ids`: the last 2 IDs (negative start).
- **1d** `every_other_id`: every 2nd ID (step).

**Checkpoint 1:** `python3 manager.py` prints `First three : ['TC-101', 'TC-102', 'TC-103']` and `Last two    : ['TC-110', 'TC-111']`. Part 1 passes in the self-check.

```bash
git add manager.py
git commit -m "Add raw ID list and slicing preview"
```

### Part 2: Remove duplicates (25 min)
Topics: *Lists, Tuples, Dictionaries and Sets*; *Applying Data Structures*, Scenario 5 "Removing Duplicates".

The export has 14 records but only 11 distinct IDs. Fill `unique_cases` so that:
- each ID appears **once**,
- the **original order** is kept,
- the **first** record for an ID wins (TC-106 was `fail`, then re-run as `pass`: you keep `fail`).

Use `seen_ids` (a set) for the "have I seen this ID?" question and `unique_cases` (a list) to keep the records. Then **delete** the `unique_cases = None` placeholder line.

**Checkpoint 2:** `len(unique_cases)` is 11 (print it). `RAW_TEST_CASES` is still 14 long (you must not change it). Part 2 passes.

```bash
git add manager.py
git commit -m "Add duplicate removal with a set"
```

### Part 3: Group by module (20 min)
Topics: *Introduction to the Collections Module* (`defaultdict`); *Applying Data Structures*, Scenario 3 "Grouping".

Fill `ids_by_module` as a `defaultdict(list)` that maps each module to the list of its test IDs (use `unique_cases`, not the raw list). Expected shape:

```python
{'login': ['TC-101', 'TC-102', 'TC-103'], 'search': [...], 'checkout': [...], 'profile': [...]}
```

**Checkpoint 3:** 4 modules; `profile` has 2 IDs; Part 3 passes.

```bash
git add manager.py
git commit -m "Add grouping by module with defaultdict"
```

### Part 4: Lookup by ID (20 min)
Topics: *Lists, Tuples, Dictionaries and Sets* (dict, `.get`); *Applying Data Structures*, Scenario 4 "Fast Lookup by ID".

- **4a** `lookup`: a dict `{id: whole record}` built from `unique_cases`.
- **4b** `found_case`: the record for `"TC-107"` using `.get`.
- **4c** `missing_case`: ask for `"TC-999"` so that you get the text `"not found"` instead of a `KeyError`.

**Checkpoint 4:** `TC-107` prints a dict with `'module': 'checkout'`; `TC-999` prints `not found`; the program does not crash. Part 4 passes.

```bash
git add manager.py
git commit -m "Add lookup by test ID with dict.get"
```

### Part 5: Counts by status and planned-vs-executed (25 min)
Topics: *Introduction to the Collections Module* (`Counter`); *Collection Operations and Methods*; *Applying Data Structures*, Scenarios 2 and 6.

- **5a** `status_counts`: how many unique cases per status. A record **without** a `status` key counts as `"unknown"`.
- **5b** `executed_ids`: a **set** of IDs of unique cases that **have** a `status`.
- **5c** `not_run_ids`: a **sorted list** of IDs in `PLANNED_IDS` that are not in `executed_ids` (set difference, then `sorted`).

**Checkpoint 5:** `By status` shows pass 5, fail 3, skip 2, unknown 1 (total 11). `Not run` shows `['TC-110', 'TC-112']`. **All 5 parts pass.**

```bash
git add manager.py
git commit -m "Add status counts and planned-vs-executed check"
```

### Part 6: Merge into main, verify, hand in (25 min)
Topics: *Git Branching Fundamentals* sections 4, 5 and 8.

1. On the feature branch, edit `PROJECT_NOTES.md`: change `Status: not started` to `Status: done`. Under "Your name", put your name. Commit:
   ```bash
   git add PROJECT_NOTES.md
   git commit -m "Mark status done in PROJECT_NOTES"
   ```
2. **Parallel work on main** (this makes a real merge commit, like a teammate working at the same time):
   ```bash
   git switch main
   ls                      # manager.py is still the starter version
   ```
   Edit `PROJECT_NOTES.md` under "How to run": replace its `TODO` with `Run: python3 manager.py`. Then:
   ```bash
   git add PROJECT_NOTES.md
   git commit -m "Document how to run (parallel work on main)"
   ```
3. **Merge** the feature branch into `main`:
   ```bash
   git merge feature/test-data-manager --no-edit
   ```
4. **Verify** on `main`:
   ```bash
   python3 check_exercise.py          # must say 5/5 parts passing
   git log --oneline --graph --all    # compare with the diagram in the Git Branching lesson
   git status                         # must say: working tree clean
   ```
5. **Clean up:** `git branch -d feature/test-data-manager`

**Checkpoint 6:** the graph shows two lines that join in a merge commit, and `check_exercise.py` passes while you are on `main`.

#### If Git reports a conflict (the trivial case)
A conflict only happens if both branches changed the **same lines**. In the steps above they changed different lines, so you should *not* get one. If you do (for example you edited `Status:` on both branches), Git stops with `CONFLICT (content): Merge conflict in PROJECT_NOTES.md`. Do not panic: nothing is lost.

1. `git status` lists the file under "both modified".
2. Open the file. You will see:
   ```
   <<<<<<< HEAD
   Status: in review          <- the version on main (where you are)
   =======
   Status: done               <- the version on the feature branch
   >>>>>>> feature/test-data-manager
   ```
3. Decide the final text, keep **only** that line, and delete the three marker lines (`<<<<<<<`, `=======`, `>>>>>>>`).
4. `git add PROJECT_NOTES.md` then `git commit --no-edit` (the merge message is prepared for you).
5. Want out instead? `git merge --abort` returns you to before the merge.
6. Run `python3 check_exercise.py` once more, because a bad resolution can break code too.

#### Optional: push to a remote (+10 min, only if you have an empty GitHub repo or a bare local repo)
Topics: *Clone, Pull, Push and Fetch*; *Git Branching Fundamentals* section 7.

Push the feature branch **before** you delete it (so the remote shows the history), then push `main`:
```bash
git remote add origin <url-of-your-empty-repo>
git push -u origin feature/test-data-manager   # run this BEFORE deleting the branch (step 5 above)
git push -u origin main
git branch -a                                  # you should see remotes/origin/...
```
If the push is rejected or asks for credentials, ask your instructor; do not use `--force`.

## 7. Stretch Goals (optional, up to 30 min)

Each stretch goal gets **its own branch** (for example `feature/stretch-duplicates`), its own commits, and a merge into `main`.

- **S1: Wrap in functions (if you already know `def`).** Turn each part into `dedupe_test_cases(cases)`, `group_by_module(cases)`, `build_lookup(cases)`. Keep `check_exercise.py` passing. (Thursday's topic: no pressure.)
- **S2: Duplicate report.** Use `Counter` on `raw_ids` to print every ID that appears more than once and how many times (expect TC-102, TC-104, TC-106). Add `duplicate_ids` as a sorted list.
- **S3: Deliberate conflict.** On `main` and on a new branch, change the `Status:` line in `PROJECT_NOTES.md` to two different texts. Merge, then resolve it with the steps above.
- **S4: Group by priority** (High, Medium, Low) and print how many High-priority cases are failing.
- **S5: Conflicting duplicates.** Find IDs whose duplicate records have **different** statuses (TC-106) and print a warning for each.

## 8. Hints (open only when stuck)

- *Loops:* `for case in RAW_TEST_CASES:` gives you one dict per turn. `case["id"]` reads a value.
- *Dedupe:* "if the ID is **not in** `seen_ids`: add it to the set **and** append the record to the list." Both lines go inside the `if`.
- *`.add` vs `.append`:* sets use `.add`, lists use `.append`.
- *defaultdict:* `ids_by_module[case["module"]].append(case["id"])`: no `if key not in` needed. Import is already at the top.
- *Lookup:* `lookup[case["id"]] = case` inside a loop, or build it with a dict comprehension if you have seen one.
- *`.get` with default:* `lookup.get("TC-999", "not found")`.
- *Counter:* start from `Counter()` and add `1` per case, or build a list of statuses and pass it to `Counter(...)`. A missing status: `case.get("status", "unknown")`.
- *Set difference:* `PLANNED_IDS - executed_ids` gives a set; `sorted(...)` turns it into a list.
- *Slices:* the stop index is **excluded**; `[-2:]` means "from the second-last to the end".
- *Self-check says a value is `None`:* you have not replaced that placeholder yet.
- *Wrong branch?* `git branch` shows it. `git switch <name>` moves. Uncommitted changes? Commit before switching.

## 9. Definition of Done (tick every box)

- [ ] `python3 check_exercise.py` prints **5/5 parts passing** while on `main` after the merge
- [ ] The work was done on `feature/test-data-manager` (not directly on `main`)
- [ ] At least **6 commits** on the feature branch: one per Part 1 to 5 plus the notes commit, each with a clear message (what was added)
- [ ] `main` has its own commit made in parallel, and the merge shows in `git log --oneline --graph --all`
- [ ] `git status` says "working tree clean"; no `__pycache__` committed
- [ ] `RAW_TEST_CASES` and `PLANNED_IDS` are unchanged
- [ ] Code has short comments for each part; no leftover `TODO` or `None` placeholders
- [ ] Reflection (section 10) written
- [ ] (Optional) pushed `feature/test-data-manager` and `main` to a remote

## 10. Submission

Submit **three things** (how: your instructor will tell you the channel; usually a link or a zip in the course portal):

1. **Repository:** the remote URL if you pushed, otherwise a zip of your `test-data-manager` folder **including the `.git` folder**.
2. **Git evidence:** the text output of `git log --oneline --graph --all` (paste it into `git_log.txt` or the submission box).
3. **Reflection (4 to 6 sentences):** (a) Why did you choose a set for `seen_ids` and a dict for `lookup`? (b) What would be slow or messy if `lookup` were a list? (c) What did the feature branch protect you from? (d) One thing that went wrong and how you fixed it.

## 11. Rubric (100 points)

| Area | Points | Full marks when |
|---|---|---|
| Correctness | 40 | 8 points per part; each part passes the self-check (partial credit if the logic is right but one detail is off, for example order) |
| Git workflow | 35 | Feature branch used (5); one commit per feature, at least 6 (10); clear commit messages (5); parallel commit on `main` and merge done with `git merge` (10); clean tree, no `__pycache__` committed (5) |
| Code quality | 15 | Right collection for each job (set for seen IDs, dict for lookup, `defaultdict` for groups, `Counter` for counts) (8); readable names and short comments, no dead code (4); original data not modified (3) |
| Reflection and submission | 10 | All 3 submission items present; reflection answers (a) to (d) in your own words |
| **Stretch (bonus)** | up to +10 | S1 to S5, 2 points each, each done on its own branch and merged |

Typical grade bands: 90+ = ready for Thursday's functions; 70 to 89 = solid, review the weak part; below 70 = book a short review with the instructor.
